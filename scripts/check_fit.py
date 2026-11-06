#!/usr/bin/env python3
"""子卡片 / 卡片是否完整被外层容器包住 —— 出图前的几何体检。

用法:
    python3 check_fit.py <html路径> [--tol 1] [--quiet]

为什么需要：大卡片包住小卡片（分组块、胶囊、mini 卡）看起来是"显而易见"的事，
但 flex/grid 溢出、层高估错时，最后一行小卡片会掉到卡片边框外面或压住边框线，
截图缩略看一眼很难发现。用户每次都要指出来："大卡片要把小卡片包含进去"。
所以把它变成出图前必跑的一道机器检查。

原理：把 HTML 复制到临时文件，注入一段测量 JS，用 Chrome headless
的 --dump-dom 把渲染后的 getBoundingClientRect 结果读回来，不靠肉眼。

检查项：
  1. 子卡片（.grp/.chip/.mini/任意 .card 内子元素）是否越过父卡片的 border box
  2. 子卡片是否侵入父卡片的 padding 区（内边距被吃掉 → 观感"贴着边框/两卡叠加"，用户会指出内间距不一致）
  3. 卡片是否越过所在 .layer
  4. 元素自身内容是否被盒子裁掉（scrollHeight > clientHeight）
  5. 各层卡片的左右边缘是否对齐（层名条宽度不一致会把某些层的卡片整体推右）
  6. 页面是否横向溢出视口

退出码：0 全部通过；1 有越界（会逐条打印 层名 / 卡名 / 偏差像素）
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "chromium",
    "chromium-browser",
    "google-chrome",
]

INJECT = r"""
<script>
(function () {
  function label(el) {
    if (!el) return "";
    const b = el.querySelector(":scope > .head b, :scope > b, :scope > .btxt b");
    return b ? b.textContent.trim().slice(0, 24) : el.className.split(" ")[0];
  }
  function layerName(el) {
    const l = el.closest(".layer");
    if (!l) return "?";
    const n = l.querySelector(".lt .lname, .lt");
    return n ? n.textContent.trim().replace(/\s+/g, "") : "?";
  }
  function cardName(el) {
    const c = el.closest(".card");
    if (!c) return "?";
    return label(c);
  }
  function run() {
    const rows = [];
    const tol = 1.0;

    // 1. 卡片 vs 层
    document.querySelectorAll(".layer").forEach(function (layer) {
      const lr = layer.getBoundingClientRect();
      layer.querySelectorAll(".card").forEach(function (card) {
        const r = card.getBoundingClientRect();
        const d = Math.max(lr.top - r.top, r.bottom - lr.bottom, lr.left - r.left, r.right - lr.right);
        if (d > tol) rows.push(["CARD_ESCAPES_LAYER", layerName(card), cardName(card), d.toFixed(1)]);
      });
    });

    // 2. 卡片内子元素 vs 卡片（border box 内边界）
    document.querySelectorAll(".card").forEach(function (card) {
      const cs = getComputedStyle(card);
      const cr = card.getBoundingClientRect();
      const bt = parseFloat(cs.borderTopWidth) || 0;
      const bb = parseFloat(cs.borderBottomWidth) || 0;
      const bl = parseFloat(cs.borderLeftWidth) || 0;
      const br = parseFloat(cs.borderRightWidth) || 0;
      const inner = {
        top: cr.top + bt, bottom: cr.bottom - bb,
        left: cr.left + bl, right: cr.right - br,
      };
      card.querySelectorAll(".grp, .chip, .mini-tag, .row").forEach(function (kid) {
        const r = kid.getBoundingClientRect();
        if (!r.width && !r.height) return;
        const over = {
          top: inner.top - r.top,
          bottom: r.bottom - inner.bottom,
          left: inner.left - r.left,
          right: r.right - inner.right,
        };
        const worst = Object.keys(over).reduce(function (a, k) {
          return over[k] > over[a] ? k : a;
        }, "top");
        if (over[worst] > tol) {
          rows.push(["CHILD_ESCAPES_CARD:" + worst, layerName(card), cardName(card) + " / " + label(kid), over[worst].toFixed(1)]);
        }
      });
      // 3. 文字被自身盒子裁掉
      card.querySelectorAll(".grp, .chip, .title, h1, h2, b").forEach(function (kid) {
        if (kid.scrollHeight - kid.clientHeight > 1 && kid.clientHeight > 0) {
          rows.push(["TEXT_CLIPPED", layerName(card), cardName(card) + " / " + label(kid), (kid.scrollHeight - kid.clientHeight).toFixed(0)]);
        }
      });
    });

    // 2b. 子元素是否侵入卡片 padding 区（内边距被吃掉 → 观感贴边框/两卡叠加）
    document.querySelectorAll(".card").forEach(function (card) {
      const cs = getComputedStyle(card);
      const cr = card.getBoundingClientRect();
      const pad = {
        top: cr.top + (parseFloat(cs.borderTopWidth) || 0) + (parseFloat(cs.paddingTop) || 0),
        bottom: cr.bottom - (parseFloat(cs.borderBottomWidth) || 0) - (parseFloat(cs.paddingBottom) || 0),
        left: cr.left + (parseFloat(cs.borderLeftWidth) || 0) + (parseFloat(cs.paddingLeft) || 0),
        right: cr.right - (parseFloat(cs.borderRightWidth) || 0) - (parseFloat(cs.paddingRight) || 0),
      };
      card.querySelectorAll(".grp, .chip, .mini-tag, .row").forEach(function (kid) {
        const r = kid.getBoundingClientRect();
        if (!r.width && !r.height) return;
        const over = {
          top: pad.top - r.top,
          bottom: r.bottom - pad.bottom,
          left: pad.left - r.left,
          right: r.right - pad.right,
        };
        const worst = Object.keys(over).reduce(function (a, k) {
          return over[k] > over[a] ? k : a;
        }, "top");
        if (over[worst] > 1.5) {
          rows.push(["EATS_CARD_PADDING:" + worst, layerName(card), cardName(card) + " / " + label(kid), over[worst].toFixed(1)]);
        }
      });
    });

    // 5. 各层卡片左右边缘是否对齐（层名条宽度不一致会把某些层的卡片整体推右）
    //    对称梯形版式（各层卡片行宽不同）本来就居中对齐，跳过本项
    (function () {
      const lefts = [], rights = [], widths = [];
      document.querySelectorAll(".layer").forEach(function (layer) {
        const cards = layer.querySelectorAll(".cards > .card");
        if (!cards.length) return;
        const a = cards[0].getBoundingClientRect().left;
        const b = cards[cards.length - 1].getBoundingClientRect().right;
        lefts.push([layerName(layer), a]);
        rights.push([layerName(layer), b]);
        widths.push(b - a);
      });
      const wMin = Math.min.apply(null, widths), wMax = Math.max.apply(null, widths);
      if (wMax - wMin > 3) return;  // 梯形/非等宽网格版式，跳过
      if (lefts.length > 1) {
        const l0 = lefts[0][1], r0 = rights[0][1];
        lefts.forEach(function (x) {
          if (Math.abs(x[1] - l0) > 3) {
            rows.push(["CARD_LEFT_MISALIGN", x[0], "首卡左边 " + x[1].toFixed(0) + " vs " + l0.toFixed(0), Math.abs(x[1] - l0).toFixed(1)]);
          }
        });
        rights.forEach(function (x) {
          if (Math.abs(x[1] - r0) > 3) {
            rows.push(["CARD_RIGHT_MISALIGN", x[0], "末卡右边 " + x[1].toFixed(0) + " vs " + r0.toFixed(0), Math.abs(x[1] - r0).toFixed(1)]);
          }
        });
      }
    })();

    // 4. 页面横向溢出
    if (document.documentElement.scrollWidth > window.innerWidth + 1) {
      rows.push(["PAGE_OVERFLOW_X", "-", "body", (document.documentElement.scrollWidth - window.innerWidth).toFixed(0)]);
    }

    const pre = document.createElement("pre");
    pre.id = "__FIT_REPORT__";
    pre.textContent = rows.length ? rows.map(function (r) { return r.join(" | "); }).join("\n") : "OK";
    document.body.appendChild(pre);
  }
  if (document.readyState === "complete") run();
  else window.addEventListener("load", run);
})();
</script>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.sep in c:
            if os.access(c, os.X_OK):
                return c
        else:
            p = shutil.which(c)
            if p:
                return p
    sys.exit("找不到 Chrome/Chromium，无法测量")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--tol", type=float, default=1.0, help="允许误差像素，默认 1")
    ap.add_argument("--quiet", action="store_true", help="只输出结论")
    a = ap.parse_args()

    src = os.path.abspath(a.html)
    raw = open(src, encoding="utf-8").read()
    injected = raw.replace("</body>", INJECT + "\n</body>", 1)
    if injected == raw:
        sys.exit("HTML 里没有 </body>，无法注入")

    tmpdir = tempfile.mkdtemp(prefix="fit-")
    tmp = os.path.join(tmpdir, "measure.html")
    open(tmp, "w", encoding="utf-8").write(injected)

    chrome = find_chrome()
    html = subprocess.run(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         "--window-size=1920,1080", "--virtual-time-budget=5000", "--dump-dom",
         "file://" + tmp],
        capture_output=True, text=True, timeout=90,
    ).stdout

    m = re.search(r'<pre id="__FIT_REPORT__">(.*?)</pre>', html, re.S)
    if not m:
        shutil.rmtree(tmpdir, ignore_errors=True)
        sys.exit("测量脚本没跑起来（没拿到报告），检查 HTML 是否有脚本报错")
    report = m.group(1).strip()
    shutil.rmtree(tmpdir, ignore_errors=True)

    name = os.path.basename(a.html)
    if report == "OK":
        if not a.quiet:
            print(f"✅ 几何正常（{name}）：子卡片都在卡片内且不侵占内边距、各层卡片左右对齐、无文字裁切与横向溢出")
        return 0

    lines = [l for l in report.splitlines() if l.strip()]
    hard = []
    for l in lines:
        parts = [p.strip() for p in l.split("|")]
        kind, layer, who, px = (parts + ["", "", "", ""])[:4]
        try:
            d = float(px)
        except ValueError:
            d = 999
        if d > a.tol:
            hard.append((d, kind, layer, who))

    if not hard:
        if not a.quiet:
            print(f"✅ 几何正常（{name}，误差在 {a.tol}px 内）")
        return 0

    print(f"❌ {len(hard)} 处越界（{name}）")
    for d, kind, layer, who in sorted(hard, reverse=True):
        print(f"  - [{layer}] {who}  ←  {kind}  超出 {d:.0f}px")
    print("\n修法：加高该层 / 减小组卡 padding 与 gap / 减少该卡列数或让超长组跨行 / 层名条改固定宽度，不要缩字号。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
