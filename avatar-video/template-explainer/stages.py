"""Shared helper for an episode's diagrams.py (2026-11-19). Every episode drew the same save loop by hand.

    sys.path.insert(0, os.path.join(HERE, "../../template-explainer")); from stages import save_all, check_bounds
    STAGES["d1"] = (d1, 2)            # name -> (function(n) -> Diagram, number of stages)
    save_all(STAGES, OUT)             # writes <name>-s<k>.svg and runs the bounds check below

check_bounds: opens each SVG's text and rect elements and fails if one lies outside the viewBox
(the clipped 12-stage sequence chart, the 15x bar and the pit chart in ep 7 were all caught by eye, one render late).
"""
import os, re

def check_bounds(path):
    s = open(path).read()
    m = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', s)
    if not m:
        return []
    W, Hh = float(m.group(1)), float(m.group(2))
    bad = []
    for el in re.finditer(r'<(rect|text)\b([^>]*)>', s):
        a = el.group(2)
        x = re.search(r'\bx="(-?[\d.]+)"', a); y = re.search(r'\by="(-?[\d.]+)"', a)
        w = re.search(r'\bwidth="([\d.]+)"', a); h = re.search(r'\bheight="([\d.]+)"', a)
        if el.group(1) == "rect" and x and y and w and h:
            if float(x.group(1)) < -1 or float(y.group(1)) < -1 or float(x.group(1)) + float(w.group(1)) > W + 1 or float(y.group(1)) + float(h.group(1)) > Hh + 1:
                bad.append("rect %s,%s %sx%s outside %gx%g" % (x.group(1), y.group(1), w.group(1), h.group(1), W, Hh))
        elif el.group(1) == "text" and x and y:
            if float(x.group(1)) > W + 1 or float(y.group(1)) > Hh + 1 or float(y.group(1)) < 0:
                bad.append("text at %s,%s outside %gx%g" % (x.group(1), y.group(1), W, Hh))
    return bad

def save_all(stages, out_dir, dark=False):
    os.makedirs(out_dir, exist_ok=True)
    problems = 0
    for name, (fn, total) in stages.items():
        for k in range(1, total + 1):
            p = os.path.join(out_dir, "%s-s%d.svg" % (name, k))
            fn(k).save(p, dark=dark)
            for b in check_bounds(p):
                problems += 1
                print("OUT OF FRAME", os.path.basename(p), b)
    print("saved", sum(t for _, t in stages.values()), "stages;", problems, "out-of-frame problems")
    return problems
