"""Folder tree: files, and what each is for. Example: the stats agent's runtime folder."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from svgkit import Diagram

d = Diagram(1200, 560)
d.title(40, 50, "Folder · what the stats agent keeps, and who reads it")
d.panel(30, 80, 560, 450)

MONO = "Menlo, 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"
rows = [  # (indent text, name, is_folder, note, group)
    ("", "stats-agent/", True, None, None),
    ("├─ ", "agent.py", False, "copied here by install", None),
    ("├─ ", "stats.md", False, "the record · /xhs-post copies it", "run"),
    ("├─ ", "memory/", True, None, None),
    ("│  ├─ ", "instructions.md", False, None, "every"),
    ("│  ├─ ", "notes.md", False, None, "every"),
    ("│  └─ ", "reported.md", False, None, "every"),
    ("└─ ", "state/", True, None, None),
    ("   ├─ ", "agent.db", False, None, "never"),
    ("   └─ ", "launchd.log", False, None, "never"),
]
y0, step = 132, 40
for i, (indent, name, folder, note, group) in enumerate(rows):
    y = y0 + i * step
    d.parts.append('<text x="60" y="%g" font-family="%s" font-size="18" fill="#a8a49c">%s</text>' % (y, MONO, indent.replace(" ", "&#160;")))
    x = 60 + len(indent) * 11
    col = "#1f1f1f" if folder else ("#d4600b" if group == "every" else "#1f1f1f")
    d.parts.append('<text x="%g" y="%g" font-family="%s" font-size="18" font-weight="%d" fill="%s">%s</text>' % (
        x, y, MONO, 700 if folder or group == "every" else 400, col, name))
    if note:
        d.text(330, y, note, 14, "#6b6b6b")

def bracket(i0, i1, x, text, sub, kind):
    ya, yb = y0 + i0 * step - 20, y0 + i1 * step + 8
    col = "#d4600b" if kind == "accent" else "#1f1f1f"
    d.parts.append('<path d="M%g,%g H%g V%g H%g" fill="none" stroke="%s" stroke-width="2.5"/>' % (x, ya, x + 14, yb, x, col))
    d.arrow([(x + 16, (ya + yb) / 2), (x + 96, (ya + yb) / 2)], color="accent" if kind == "accent" else "ink")
    d.box(x + 100, (ya + yb) / 2 - 44, 300, 88, text, sub, kind=kind, title_size=18, sub_size=13)

bracket(4, 6, 600, "Loaded into every run", "rules, what it learned, what it\nalready told you (last 3,000 chars)", "accent")
bracket(8, 9, 600, "Never seen by the model", "inbox · timers · outbox · runs,\nread by the worker and dispatcher", "main")
d.note(40, 548, "Lives in ~/Library/Application Support/, outside the repo, so nothing here is ever committed.")
d.save(os.path.join(HERE, "..", "assets", "tree.svg"))
