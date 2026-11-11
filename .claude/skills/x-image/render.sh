#!/bin/bash
# Render an x-image HTML file to PNG with headless Chrome.
# Usage: render.sh <file.html> [width] [height]
# Size comes from <meta name="x-size" content="1600x900"> in the HTML, or the args.
set -euo pipefail
html="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
size=$(sed -n 's/.*name="x-size" content="\([0-9][0-9]*x[0-9][0-9]*\)".*/\1/p' "$html" | head -1)
w="${2:-${size%x*}}"; h="${3:-${size#*x}}"
w="${w:-1600}"; h="${h:-900}"
out="${html%.html}.png"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size="$w,$h" --screenshot="$out" "file://$html" >/dev/null 2>&1
echo "$out (${w}x${h})"
