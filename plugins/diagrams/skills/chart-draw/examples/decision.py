"""Decision tree: questions with yes/no branches. Example: which mode /avatar-video runs in."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from svgkit import Diagram

d = Diagram(1200, 600)
d.title(40, 50, "Decision · which voice and face a video gets")

d.box(470, 90, 260, 70, "/avatar-video topic", "you start a video", kind="main", title_size=20)
d.arrow([(600, 164), (600, 206)], color="ink")

# question 1
d.box(440, 210, 320, 70, "avatar_look_id set?", None, kind="dark", title_size=20)
d.arrow([(436, 245), (250, 245), (250, 316)], color="ink")
d.text(340, 233, "yes", 15, "#1f1f1f", 700, "middle")
d.arrow([(764, 245), (950, 245), (950, 316)], color="accent")
d.text(860, 233, "no (today)", 15, "#d4600b", 700, "middle")

d.box(120, 320, 260, 96, "Avatar mode", "your face, lip-synced\nto the voice · paid", kind="plain")
d.box(820, 320, 260, 96, "No-avatar mode", "your voice over graphics", kind="accent")

# question 2 under no-avatar
d.arrow([(950, 422), (950, 452)], color="accent")
d.box(790, 456, 320, 64, "asked for a default voice?", None, kind="dark", title_size=18)
d.arrow([(786, 488), (640, 488), (640, 546)], color="ink")
d.text(712, 476, "yes", 15, "#1f1f1f", 700, "middle")
d.box(520, 550, 240, 40, "macOS say (Tingting)", None, kind="plain", title_size=15)
d.arrow([(950, 524), (950, 546)], color="accent")
d.text(962, 541, "no", 15, "#d4600b", 700)
d.box(830, 550, 240, 40, "cloned voice, one take", None, kind="accent", title_size=15)

d.note(40, 440, "Paid steps (voice, avatar) only run")
d.note(40, 459, "after you approve the storyboard.")
d.save(os.path.join(HERE, "..", "assets", "decision.svg"))
