#!/usr/bin/env python3
"""Make ESTIMATED timing from script.json so the slides can be built, synced and snapshotted BEFORE any voice exists.

Usage: python3 -I preview_timing.py <video folder>

Writes <folder>/.voice-preview/words.json (one fake word per Chinese character or English word, about 5.5 characters a
second, short pauses at commas and sentence ends) and <folder>/timing.json ({"total", "take_dir": ".voice-preview",
"preview": true, "lines": [...]}). Then the normal build.py, voice-video sync.py and `hyperframes snapshot` work, so Michael
can review the script and the cards together (2026-11-19 request: approve script + cards, then generate the voice).

It writes no vo.wav. When the real voice is built (`build_vo.py`), timing.json is overwritten with real times and
"preview" disappears: rebuild with build.py and run sync.py again. Never render or post from preview timing.
"""
import json, os, re, sys

proj = sys.argv[1]
script = json.load(open(os.path.join(proj, "script.json")))
HAN = 0.18          # seconds per Chinese character (about 5.5 a second at pace 0.92)
LATIN = 0.38        # seconds per English word or number
PAUSE = {"，": 0.25, "、": 0.15, "：": 0.3, "；": 0.3, "。": 0.55, "？": 0.55, "！": 0.55}
GAP = 0.75          # between script items (a chapter break is a bit longer in the real voice)
TOK = re.compile(r"[一-鿿]|[A-Za-z0-9.]+|[，、：；。？！]")

t, words, lines = 0.3, [], []
for i, item in enumerate(script):
    start = t
    for m in TOK.finditer(item["say"]):
        tok = m.group(0)
        if tok in PAUSE:
            t += PAUSE[tok]
            continue
        d = HAN if re.match(r"[一-鿿]", tok) else LATIN
        words.append({"text": tok, "start_time": round(t, 3), "end_time": round(t + d, 3)})
        t += d
    lines.append({"i": i, "start": round(start, 3), "end": round(t, 3), "text": item["say"]})
    t += GAP
total = round(t + 0.9, 3)
d = os.path.join(proj, ".voice-preview")
os.makedirs(d, exist_ok=True)
json.dump(words, open(os.path.join(d, "words.json"), "w"), ensure_ascii=False)
json.dump({"total": total, "take_dir": ".voice-preview", "preview": True, "lines": lines},
          open(os.path.join(proj, "timing.json"), "w"), ensure_ascii=False, indent=1)
print("preview timing: %d items, %.0f s (estimate), %d fake words" % (len(lines), total, len(words)))
