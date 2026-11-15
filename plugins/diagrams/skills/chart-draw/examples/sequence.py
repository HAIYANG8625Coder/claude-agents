"""Sequence: who calls whom, in order. Example: how voice-video records one HeyGen take."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from svgkit import Diagram

d = Diagram(1200, 640)
d.title(40, 50, "Sequence · recording one voice take")
d.note(40, 76, "The HeyGen sign-in only works in the CLI, so the skill relays one call through a nested claude -p.")

cols = [("voice-video", "skill in your session", 170, "main"),
        ("heygen_take.sh", "shell script", 460, "plain"),
        ("claude -p", "nested · Sonnet", 750, "accent"),
        ("HeyGen", "MCP server", 1040, "dark")]
for name, sub, cx, kind in cols:
    d.box(cx - 110, 104, 220, 76, name, sub, kind=kind, title_size=19)
    d.line(cx, 186, cx, 590, color="#c9c4ba", width=2, dash="3 7")

def msg(y, a, b, text, ret=False, num=None):
    xa, xb = cols[a][2], cols[b][2]
    sgn = 1 if xb > xa else -1
    d.arrow([(xa + sgn * 8, y), (xb - sgn * 10, y)], color="grey" if ret else "accent",
            dashed=ret, width=2 if ret else 2.5)
    label = ("%d. " % num if num else "") + text
    d.text((xa + xb) / 2, y - 12, label, 15, "#6b6b6b" if ret else "#d4600b", 400 if ret else 700, "middle")

msg(240, 0, 1, "run with the video folder", num=1)
msg(300, 1, 2, "call create_speech once", num=2)
msg(360, 2, 3, "the whole script, one take", num=3)
msg(420, 3, 2, "audio URL + word timestamps", ret=True)
msg(480, 2, 1, "full.raw + words.json saved", ret=True)
msg(540, 1, 0, "take ok", ret=True)

d.box(780, 440, 200, 66, "Telegram plugin off", "so it can't steal the bot", kind="dashed", title_size=14, sub_size=12.5)
d.note(40, 622, "Orange: requests, numbered in order. Grey dashed: replies.")
d.save(os.path.join(HERE, "..", "assets", "sequence.svg"))
