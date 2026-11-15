"""Layers: a stack where each level builds on the one below. Example: how this repo is organised."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from svgkit import Diagram

d = Diagram(1200, 600)
d.title(40, 50, "Layers · this repo, the way Claude Code sees it")

layers = [
    ("Marketplace", ".claude-plugin/marketplace.json", ["lists every plugin", "install from GitHub"], "plain"),
    ("Plugins", "plugins/<name>/.claude-plugin/plugin.json", ["x-assistant", "avatar-video", "outlook-email", "diagrams"], "accent"),
    ("Skills · subagents", "skills/<name>/SKILL.md · agents/<name>.md", ["/x-post", "/xhs-post", "/avatar-video", "/chart-draw"], "plain"),
    ("Data · runtime", "outside the plugins", ["x-assistant/", "avatar-video/", "Application Support/"], "plain"),
]
y, h, gap = 84, 104, 14
for i, (name, path, pills, kind) in enumerate(layers):
    yy = y + i * (h + gap)
    d.panel(40, yy, 860, h, rx=14)
    if kind == "accent":
        d.parts.append('<rect x="40" y="%g" width="860" height="%g" rx="14" fill="none" stroke="#d4600b" stroke-width="2.5"/>' % (yy, h))
    d.text(64, yy + 42, name, 20, "#d4600b" if kind == "accent" else "#1f1f1f", 700)
    d.text(64, yy + 70, path, 13.5, "#6b6b6b")
    px = 400
    for p in pills:
        px += d.pill(px, yy + 34, p, kind="plain", size=13) + 8

# side: how this folder loads them
d.box(950, 280, 210, 110, ".claude/ links", "this folder loads skills\nwith plain names", kind="main", title_size=18, sub_size=13)
d.arrow([(946, 335), (904, 335)], color="ink")
d.text(1055, 420, "Installed elsewhere:", 13.5, "#8a8a8a", 400, "middle")
d.text(1055, 438, "/x-assistant:x-post", 13.5, "#8a8a8a", 400, "middle")
d.note(40, 572, "Each layer only points down: a plugin lists its skills; a skill reads its data folder.")
d.save(os.path.join(HERE, "..", "assets", "layers.svg"))
