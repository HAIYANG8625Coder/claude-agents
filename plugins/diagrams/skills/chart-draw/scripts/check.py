#!/usr/bin/env python3
"""Render a hand-written SVG diagram to PNG and check its layout, using headless Chrome.

Usage:
  python3 -I check.py diagram.svg [more.svg ...] [--out DIR] [--github]

For each SVG it writes <out>/<name>.png (full size) and prints a report of:
  - text that overlaps other text
  - text crossed by a line or path (labels sitting on an arrow)
  - text that runs outside the viewBox
--github also writes <name>-github.png: the diagram at GitHub's README width (880 px)
with Arial instead of the SVG's fonts, which is what Windows and Linux readers see.
Exit code 1 when any problem is found, so it can gate a commit.
"""
import glob
import html
import json
import os
import re
import subprocess
import sys
import tempfile

CHECK_JS = r"""
const svg = document.querySelector('svg');
const vb = svg.viewBox.baseVal;
const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim());
const box = t => { const b = t.getBBox(); return {x: b.x, y: b.y, w: b.width, h: b.height}; };
const pad = 1.5;
const overlap = (a, b) => a.x < b.x + b.w - pad && b.x < a.x + a.w - pad && a.y < b.y + b.h - pad && b.y < a.y + a.h - pad;
const segHits = (b, x1, y1, x2, y2) => {
  // sample the segment; text boxes are small, so 2 px steps are enough
  const n = Math.max(2, Math.ceil(Math.hypot(x2 - x1, y2 - y1) / 2));
  for (let i = 0; i <= n; i++) {
    const x = x1 + (x2 - x1) * i / n, y = y1 + (y2 - y1) * i / n;
    if (x > b.x + 1 && x < b.x + b.w - 1 && y > b.y + 2 && y < b.y + b.h - 2) return true;
  }
  return false;
};
const strokes = [];
for (const el of svg.querySelectorAll('line, path, polyline')) {
  if (el.closest('marker') || el.closest('defs')) continue;
  const fill = el.getAttribute('fill');
  if (el.tagName === 'path' && fill && fill !== 'none') continue;   // filled shapes (icons) are not strokes
  if (el.tagName === 'line') {
    strokes.push([[+el.getAttribute('x1'), +el.getAttribute('y1')], [+el.getAttribute('x2'), +el.getAttribute('y2')]]);
  } else {
    const len = el.getTotalLength(), pts = [];
    for (let d = 0; d <= len; d += 3) { const p = el.getPointAtLength(d); pts.push([p.x, p.y]); }
    strokes.push(pts);
  }
}
const label = t => t.textContent.trim().slice(0, 40);
const problems = [];
const boxes = texts.map(box);
for (let i = 0; i < texts.length; i++) {
  const a = boxes[i];
  if (a.x < vb.x || a.y < vb.y || a.x + a.w > vb.x + vb.width || a.y + a.h > vb.y + vb.height)
    problems.push('outside the viewBox: "' + label(texts[i]) + '"');
  for (let j = i + 1; j < texts.length; j++)
    if (overlap(a, boxes[j])) problems.push('text overlaps text: "' + label(texts[i]) + '" / "' + label(texts[j]) + '"');
  for (const pts of strokes) {
    let hit = false;
    for (let k = 1; k < pts.length && !hit; k++) hit = segHits(a, pts[k-1][0], pts[k-1][1], pts[k][0], pts[k][1]);
    if (hit) { problems.push('a line crosses: "' + label(texts[i]) + '"'); break; }
  }
}
// rectangles (boxes, panels, pills), ignoring the full-page background
const rects = [...svg.querySelectorAll('rect')].filter(r => !r.closest('defs') && !r.closest('marker'))
  .map(r => ({el: r, x: +r.getAttribute('x') || 0, y: +r.getAttribute('y') || 0, w: +r.getAttribute('width'), h: +r.getAttribute('height')}))
  .filter(r => !(r.w >= vb.width - 1 && r.h >= vb.height - 1));
const inter = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
const inside = (a, b, m) => a.x >= b.x - m && a.y >= b.y - m && a.x + a.w <= b.x + b.w + m && a.y + a.h <= b.y + b.h + m;
const tag = r => r.w + 'x' + r.h + ' box at ' + Math.round(r.x) + ',' + Math.round(r.y);
for (let i = 0; i < texts.length; i++) {
  const a = boxes[i];
  for (const r of rects)
    if (inter(a, r) && !inside(a, r, 1)) { problems.push('text spills over the edge of a ' + tag(r) + ': "' + label(texts[i]) + '"'); break; }
}
for (let i = 0; i < rects.length; i++)
  for (let j = i + 1; j < rects.length; j++) {
    const a = rects[i], b = rects[j];
    if (inter(a, b) && !inside(a, b, 0.5) && !inside(b, a, 0.5))
      problems.push('boxes cut into each other: ' + tag(a) + ' / ' + tag(b));
  }
document.body.setAttribute('data-report', JSON.stringify(problems));
"""


def chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for pat in [os.path.expanduser("~/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-*/chrome-headless-shell"),
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    sys.exit("No Chrome found. Set CHROME=/path/to/chrome or install Google Chrome.")


def run(args):
    return subprocess.run(args, capture_output=True, text=True, timeout=120)


def size_of(svg_text):
    m = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)', svg_text)
    if not m:
        sys.exit("The SVG needs a viewBox.")
    return int(float(m.group(1))), int(float(m.group(2)))


def main():
    argv = sys.argv[1:]
    github = "--github" in argv
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    files = [a for a in argv if a.endswith(".svg")]
    if not files:
        sys.exit(__doc__)
    exe, bad = chrome(), 0
    for f in files:
        f = os.path.abspath(f)
        svg = open(f, encoding="utf-8").read()
        w, h = size_of(svg)
        d = os.path.abspath(out or os.path.dirname(f))
        os.makedirs(d, exist_ok=True)
        name = os.path.splitext(os.path.basename(f))[0]
        png = os.path.join(d, name + ".png")
        run([exe, "--headless", "--hide-scrollbars", "--window-size=%d,%d" % (w, h), "--screenshot=" + png, "file://" + f])
        with tempfile.TemporaryDirectory() as tmp:
            page = os.path.join(tmp, "check.html")
            open(page, "w", encoding="utf-8").write(
                '<!doctype html><meta charset="utf-8"><body style="margin:0">%s<script>%s</script></body>' % (svg, CHECK_JS))
            dom = run([exe, "--headless", "--virtual-time-budget=3000", "--dump-dom", "file://" + page]).stdout
            if github:
                gsvg = re.sub(r'font-family="[^"]*"', 'font-family="Arial, Helvetica, sans-serif"', svg)
                gpage = os.path.join(tmp, "gh.html")
                open(gpage, "w", encoding="utf-8").write(
                    '<!doctype html><meta charset="utf-8"><body style="margin:0;width:880px;background:#fff">%s</body>'
                    % gsvg.replace("<svg ", '<svg style="width:880px;height:auto;display:block" ', 1))
                run([exe, "--headless", "--hide-scrollbars", "--window-size=880,%d" % (h * 880 // w + 4),
                     "--screenshot=" + os.path.join(d, name + "-github.png"), "file://" + gpage])
        m = re.search(r'data-report="([^"]*)"', dom)
        problems = json.loads(html.unescape(m.group(1))) if m else ["could not run the layout check (is the SVG valid XML?)"]
        print("%s -> %s" % (f, png))
        if problems:
            bad += 1
            for p in problems:
                print("  ✗ " + p)
        else:
            print("  ✓ no overlaps, nothing outside the viewBox")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
