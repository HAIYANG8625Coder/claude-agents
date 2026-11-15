"""State machine: the states one thing moves through. Example: an event in the stats agent's inbox."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from svgkit import Diagram

d = Diagram(1200, 560)
d.title(40, 50, "States · one event in the inbox")
d.panel(30, 80, 1140, 440)

# new event -> pending
d.dot(110, 290, 10)
d.text(110, 326, "new event", 15, "#1f1f1f", 700, "middle")
d.arrow([(124, 290), (366, 290)], color="accent", label="handler writes it")
d.box(370, 240, 220, 100, "pending", "waiting for a run", kind="accent", title_size=24)

# duplicate dropped
d.arrow([(110, 278), (110, 188), (176, 188)], color="grey", dashed=True)
d.text(100, 228, "same id\nagain", 14, "#8a8a8a", 400, "end")
d.box(180, 150, 160, 76, "dropped", "never stored", kind="faded", title_size=18)

# retry loop over pending
d.arrow([(440, 236), (440, 170), (520, 170), (520, 232)], color="ink")
d.text(532, 180, "run failed, attempts < 3:\nretry on the next tick", 14, "#6b6b6b")

# pending -> done
d.arrow([(594, 290), (846, 290)], color="accent", label="run returned JSON")
d.box(850, 240, 220, 100, "done", "follow-ups → timers\nmessage → outbox", kind="main", title_size=24, sub_size=13)

# pending -> failed
d.arrow([(480, 344), (480, 424)], color="ink", label="3rd failure")
d.box(370, 428, 220, 76, "failed", "kept for status", kind="plain", title_size=20)
d.arrow([(594, 466), (846, 466)], color="ink", label="adds a warning")
d.box(850, 428, 220, 76, "outbox", "Telegram: Chrome open?", kind="plain", title_size=20, sub_size=13)
d.save(os.path.join(HERE, "..", "assets", "states.svg"))
