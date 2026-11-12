"""Move a video's scene/caption times from an old timing.json to a new one (after re-voicing).

Every tl.set/to/from/fromTo position in index.html is mapped piecewise-linearly between the
sentence anchors (start/end of each line, plus 0 and the total), and data-duration="<old total>"
becomes the new total. Durations inside a tween are left alone.
Usage: python3 -I avatar-video/tools/retime.py <video folder> <old timing.json>   (new = <video>/timing.json)
"""
import json, os, re, sys

proj, old_path = sys.argv[1], sys.argv[2]
old, new = json.load(open(old_path)), json.load(open(os.path.join(proj, "timing.json")))
a = [(0.0, 0.0)]
for o, n in zip(old["lines"], new["lines"]):
    a += [(o["start"], n["start"]), (o["end"], n["end"])]
a.append((old["total"], new["total"]))

def m(t):
    for (x0, y0), (x1, y1) in zip(a, a[1:]):
        if t <= x1:
            return y0 if x1 == x0 else y0 + (t - x0) * (y1 - y0) / (x1 - x0)
    return t - old["total"] + new["total"]

p = os.path.join(proj, "index.html"); h = open(p).read()
call = re.compile(r"(tl\.(?:set|to|from|fromTo)\(.*?,\s*)(\d+(?:\.\d+)?)(\);)")
h, n = call.subn(lambda g: "%s%.3f%s" % (g.group(1), m(float(g.group(2))), g.group(3)), h)
h, d = re.subn(r'data-duration="%s"' % re.escape(str(old["total"])), 'data-duration="%s"' % new["total"], h)
open(p, "w").write(h)
print("moved %d timeline positions, %d durations: %.2fs -> %.2fs" % (n, d, old["total"], new["total"]))
