"""Compare: two options side by side and which one won. Example: how the stats agent got file access."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from svgkit import Diagram

d = Diagram(1200, 520)
d.title(40, 50, "Compare · letting a background job read its files")

def side(x, heading, sub, points, chosen):
    d.panel(x, 80, 540, 400)
    d.box(x + 30, 104, 480, 86, heading, sub, kind="accent" if chosen else "faded", title_size=21)
    for i, (good, text) in enumerate(points):
        y = 238 + i * 52
        mark, col = ("✓", "#1e7a3c") if good else ("✗", "#c23b22")
        d.text(x + 46, y, mark, 22, col, 700)
        d.text(x + 82, y - 1, text, 16, "#1f1f1f" if chosen else "#6b6b6b")
    if chosen:
        d.pill(x + 30, 436, "chosen", kind="dark", size=13)

side(40, "A · Full Disk Access", "for Python, in System Settings", [
    (True, "repo stays where it is"),
    (False, "every Python script can read every file"),
    (False, "a security setting only you can change"),
    (False, "still blocked: it checks the /usr/bin shim"),
], False)
side(620, "B · Move out of ~/Documents", "~/Library/Application Support/stats-agent", [
    (True, "no special access at all"),
    (True, "the job sees only its own folder"),
    (True, "worked on the first launchd run"),
    (False, "posts.md gets the numbers via /xhs-post"),
], True)
d.arrow([(586, 280), (614, 280)], color="accent")
d.note(40, 506, "Show the option you rejected too: readers trust a choice more when they see what it beat.")
d.save(os.path.join(HERE, "..", "assets", "compare.svg"))
