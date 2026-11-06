#!/usr/bin/env python3
"""HTML 结构校验：用标准解析器检查 div 嵌套，报告未闭合/多余闭合及行号。

用法:
    python3 check_html.py 图.html

为什么需要：脚本批量改 HTML 后，字符串计数平衡不代表嵌套正确。典型故障是
"某张卡片提前闭合、img 露在卡外"，表现为整页布局塌掉，靠肉眼很难定位。
"""
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []      # (tag, line, cls)
        self.extra = []      # 多余闭合
        self.mismatch = []   # 闭合标签与栈顶不一致

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        cls = dict(attrs).get("class", "")
        self.stack.append((tag, self.getpos()[0], cls))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        line = self.getpos()[0]
        if not self.stack:
            self.extra.append((tag, line))
            return
        if self.stack[-1][0] != tag:
            # 找到最近的同名标签
            idx = next((i for i in range(len(self.stack) - 1, -1, -1)
                        if self.stack[i][0] == tag), None)
            if idx is None:
                self.extra.append((tag, line))
                return
            dropped = self.stack[idx + 1:]
            self.mismatch.append((tag, line, dropped))
            del self.stack[idx:]
            return
        self.stack.pop()


def main():
    if len(sys.argv) < 2:
        sys.exit("用法: check_html.py <html文件>")
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()

    c = Checker()
    c.feed(src)

    ok = True
    if c.mismatch:
        ok = False
        print(f"❌ {len(c.mismatch)} 处嵌套错位（闭合时栈内有未关闭的子元素）：")
        for tag, line, dropped in c.mismatch[:10]:
            inner = ", ".join(f"<{t}> L{l}" for t, l, _ in dropped[:4])
            print(f"   L{line} </{tag}> 之前未闭合: {inner}")

    if c.extra:
        ok = False
        print(f"❌ {len(c.extra)} 处多余闭合标签：")
        for tag, line in c.extra[:10]:
            print(f"   L{line} </{tag}>")

    if c.stack:
        ok = False
        print(f"❌ {len(c.stack)} 个标签未闭合：")
        for tag, line, cls in c.stack[:10]:
            print(f"   L{line} <{tag} class=\"{cls}\">")

    if ok:
        print(f"✅ 结构正常（{path}）")
    else:
        print("\n提示：先修最靠前的问题，后面的报错往往是连带现象。")
        sys.exit(1)


if __name__ == "__main__":
    main()
