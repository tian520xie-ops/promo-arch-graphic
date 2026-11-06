#!/usr/bin/env bash
# 用 Chrome 无头模式把 HTML 截成 PNG
# 用法: bash export_png.sh <html路径> <输出png> [宽] [高] [倍率]
# 例:   bash export_png.sh 图.html out.png 1920 1080 2

set -euo pipefail

HTML="${1:?用法: export_png.sh <html路径> <输出png> [宽] [高] [倍率]}"
OUT="${2:?缺少输出路径}"
W="${3:-1920}"
H="${4:-1080}"
SCALE="${5:-2}"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then
  for c in chromium chromium-browser google-chrome; do
    if command -v "$c" >/dev/null 2>&1; then CHROME="$(command -v "$c")"; break; fi
  done
fi

# 转绝对路径，Chrome 不认相对路径
HTML_ABS="$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"
mkdir -p "$(dirname "$OUT")"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"

"$CHROME" \
  --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size="${W},${H}" \
  --force-device-scale-factor="${SCALE}" \
  --virtual-time-budget=6000 \
  --screenshot="$OUT_ABS" \
  "file://${HTML_ABS}" 2>&1 | tail -1

echo "已出图: $OUT_ABS"
