"""Swimlane: who does each step. Example: the /avatar-video pipeline and its approval gates."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from svgkit import Diagram

d = Diagram(1200, 620)
d.title(40, 50, "Swimlane · making one video, and who does each step")

lanes = ["You", "Claude", "HeyGen", "HyperFrames"]
top, lane_h, left = 84, 116, 40
for i, name in enumerate(lanes):
    y = top + i * lane_h
    d.panel(left, y + 4, 1120, lane_h - 8, rx=12)
    d.text(left + 20, y + lane_h / 2 + 6, name, 17, "#1f1f1f", 700)

# (step label, sub, lane, column)
steps = [("1 Script", "2 options", 1, 0), ("2 Pick", "one script", 0, 1), ("3 Storyboard", "scenes", 1, 2),
         ("4 Approve", "cost gate", 0, 3), ("5 Voice", "one take", 2, 4), ("6 Listen", "say yes", 0, 5),
         ("7 Edit", "+ render", 3, 6), ("8 Approve", "then post", 0, 7)]
x0, dx, bw, bh = 196, 120, 104, 70
pos = []
for label, sub, lane, col in steps:
    x, y = x0 + col * dx, top + lane * lane_h + (lane_h - bh) / 2
    kind = "accent" if label.startswith("4") else ("main" if lane == 0 else "plain")
    d.box(x, y, bw, bh, label, sub, kind=kind, title_size=15, sub_size=12.5)
    pos.append((x, y))
for i in range(len(pos) - 1):
    (xa, ya), (xb, yb) = pos[i], pos[i + 1]
    if abs(ya - yb) < 1:
        d.arrow([(xa + bw + 2, ya + bh / 2), (xb - 6, yb + bh / 2)], color="accent")
    else:  # leave from the top or bottom edge, turn once, enter from the left
        sx, sy = xa + bw / 2, (ya + bh + 2) if yb > ya else (ya - 2)
        d.arrow([(sx, sy), (sx, yb + bh / 2), (xb - 6, yb + bh / 2)], color="accent")

d.note(40, 582, "Black boxes are your decisions. Nothing paid (step 5 on) starts before step 4.")
d.save(os.path.join(HERE, "..", "assets", "swimlane.svg"))
