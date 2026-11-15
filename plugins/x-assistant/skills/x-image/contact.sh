#!/bin/bash
# Put several rendered PNGs on one contact sheet, so you can check them all with one Read.
# Usage: contact.sh <out.png> <a.png> <b.png> ...
set -euo pipefail
out="$1"; shift
dir="$(cd "$(dirname "$out")" && pwd)"; html="$dir/.contact-sheet.html"
{
  echo '<!doctype html><html><body style="margin:0;background:#888;display:flex;flex-wrap:wrap;gap:12px;padding:12px;width:1752px">'
  for f in "$@"; do
    p="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
    echo "<figure style=\"margin:0\"><img src=\"file://$p\" style=\"width:420px;display:block\"><figcaption style=\"font:18px sans-serif;color:#fff\">$(basename "$f")</figcaption></figure>"
  done
  echo '</body></html>'
} > "$html"
rows=$(( ($# + 3) / 4 ))
h=$(( rows * 600 + 24 ))
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --allow-file-access-from-files --force-device-scale-factor=1 --window-size="1776,$h" \
  --screenshot="$dir/$(basename "$out")" "file://$html" >/dev/null 2>&1
rm -f "$html"
echo "$dir/$(basename "$out") ($# images)"
