#!/usr/bin/env python3
"""插画底色归一化：检测四角底色，把米灰底线性拉成纯白。

用法:
    python3 normalize_illus.py <目录或文件> [--dry] [--target 240]

为什么需要：生成图底色常是 ~235 的米灰而非纯白，直接 mix-blend-mode: multiply
会在浅色卡片上留一块灰斑。线性拉伸 v * 255 / target 把底色推到纯白，深色线稿
几乎不受影响。
"""
import argparse
import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：pip3 install Pillow")


def corners(img):
    w, h = img.size
    px = img.load()
    return [px[3, 3], px[w - 4, 3], px[3, h - 4], px[w - 4, h - 4]]


def process(path, target, dry):
    img = Image.open(path).convert("RGB")
    cs = corners(img)
    darkest = min(min(c) for c in cs)
    if darkest >= 250:
        print(f"  纯白OK    {os.path.basename(path)}")
        return False
    if dry:
        print(f"  需归一化  {os.path.basename(path)}  角部最暗={darkest}")
        return True
    out = img.point(lambda v: min(255, round(v * 255 / target)))
    out.save(path)
    print(f"  已归一化  {os.path.basename(path)}  角部最暗={darkest} → 纯白")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="目录或单个图片")
    ap.add_argument("--dry", action="store_true", help="只检测不写入")
    ap.add_argument("--target", dest="cap", type=int, default=240,
                    help="拉伸阈值，默认 240（底色 ~235 时合适）")
    a = ap.parse_args()

    if os.path.isdir(a.target):
        files = sorted(sum([glob.glob(os.path.join(a.target, e))
                            for e in ("*.png", "*.jpg", "*.jpeg")], []))
    else:
        files = [a.target]

    if not files:
        sys.exit("没找到图片")

    changed = sum(process(f, a.cap, a.dry) for f in files)
    print(f"\n共 {len(files)} 张，处理 {changed} 张")


if __name__ == "__main__":
    main()
