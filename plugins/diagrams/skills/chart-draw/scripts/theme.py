#!/usr/bin/env python3
"""Make a dark-mode copy of a light chart-draw diagram.

Light is the default and the source of truth: draw and edit the light SVG, then generate the
dark one from it, so the two can never drift apart.

Usage:
  python3 -I theme.py docs/overview.svg [more.svg ...]    writes docs/overview-dark.svg, ...

Every colour in the house palette has a dark partner (DARK below). The full-page background
becomes GitHub's dark page colour, boxes become a raised dark card, ink turns light and the
orange accent gets brighter so it keeps its contrast. A colour that isn't in the palette is
reported and left as it is: add it to DARK, or use a palette colour instead.
"""
import os
import re
import sys

PAGE_DARK = "#0d1117"   # GitHub's dark page, so the diagram sits flush on it
DARK = {
    "#ffffff": "#2a2723",  # boxes and cards (the page background is handled separately)
    "#f0ede6": "#1c1a17",  # panels
    "#1f1f1f": "#ece8e1",  # ink: titles, black arrows, people, dark boxes (they flip to light)
    "#d4600b": "#f0883e",  # accent
    "#fcefe5": "#3d2616",  # accent fill
    "#e9c9ae": "#6b4024",  # accent halo
    "#6b6b6b": "#aca69d",  # secondary text
    "#555555": "#b8b2a9",
    "#8a8a8a": "#8f8a82",  # notes
    "#9a968e": "#7f7a72",  # faded text
    "#a8a49c": "#6f6a63",  # dashed / quiet lines
    "#c9c4ba": "#4d4842",  # dotted axes, lifelines
    "#d8d4cc": "#4a4640",  # thin box borders
    "#dedad2": "#45413b",
    "#e3dfd7": "#3d3934",
    "#e6e2da": "#3d3934",
    "#d9d6cf": "#5b5751",  # subtitle inside a dark (now light) box
    "#1e7a3c": "#3fb950",  # ✓
    "#c23b22": "#f85149",  # ✗
    "#e6f4ea": "#12261a",
}
COLOR_ATTR = re.compile(r'((?:fill|stroke|stop-color|color)=")(#[0-9a-fA-F]{3,6})(")')


def norm(c):
    c = c.lower()
    return "#" + "".join(ch * 2 for ch in c[1:]) if len(c) == 4 else c


def to_dark(svg):
    """Return the dark version of a light diagram's SVG text, plus any colours it didn't know."""
    unknown = set()
    # the page background: the first rect with no x/y that fills the whole viewBox
    svg = re.sub(r'(<rect width="[\d.]+" height="[\d.]+" fill=")#ffffff(")', r"\g<1>%s\2" % PAGE_DARK, svg, count=1)

    def swap(m):
        c = norm(m.group(2))
        if c == PAGE_DARK:
            return m.group(0)
        if c not in DARK:
            unknown.add(c)
            return m.group(0)
        return m.group(1) + DARK[c] + m.group(3)
    return COLOR_ATTR.sub(swap, svg), unknown


def dark_path(path):
    root, ext = os.path.splitext(path)
    return root + "-dark" + ext


def main():
    files = [a for a in sys.argv[1:] if a.endswith(".svg") and not a.endswith("-dark.svg")]
    if not files:
        sys.exit(__doc__)
    for f in files:
        out, unknown = to_dark(open(f, encoding="utf-8").read())
        open(dark_path(f), "w", encoding="utf-8").write(out)
        print("%s -> %s%s" % (f, dark_path(f), ("  (unknown colours kept: %s)" % ", ".join(sorted(unknown))) if unknown else ""))


if __name__ == "__main__":
    main()
