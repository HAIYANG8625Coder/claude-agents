"""Turn ONE HeyGen take of the whole script into assets/vo.wav + timing.json.

Why: voicing sentence by sentence (heygen-voice.py) resets the intonation at every sentence and
leaves uneven gaps, which sounds choppy. One take flows like real speech; HeyGen's per-word
timestamps (original_words) then give exact sentence times, so captions still need no transcription.

Get the take with the HeyGen MCP create_speech (whole text, one call), saving
  <video>/.voice-heygen-full/full.raw   (the audio)
  <video>/.voice-heygen-full/words.json (original_words: [{text,start_time,end_time}])
Usage: python3 -I avatar-video/tools/heygen-whole.py <video folder> <voice_id> [--tail 0.9] [--dir .voice-heygen-full]
Slower delivery: HeyGen ignores `speed` for instant clones, so stretch afterwards with tools/slow-take.py.
"""
import json, os, re, subprocess, sys

proj, voice = sys.argv[1], sys.argv[2]
tail = float(sys.argv[sys.argv.index("--tail") + 1]) if "--tail" in sys.argv else 0.9
here = os.path.dirname(os.path.abspath(__file__))
ff = os.path.join(here, "../node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
d = os.path.join(proj, sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else ".voice-heygen-full")
lines = json.load(open(os.path.join(proj, "script.json")))
words = [w for w in json.load(open(os.path.join(d, "words.json"))) if re.search(r"\w", w["text"])]

out, k = [], 0
for i, l in enumerate(lines):
    units = re.findall(r"[A-Za-z0-9]+|[一-鿿]", l["say"].replace(" ", ""))
    seg = words[k:k + len(units)]; k += len(units)
    got = "".join(w["text"] for w in seg).replace(" ", "")
    if got != "".join(units):
        sys.exit("sentence %d does not match the timestamps: %r vs %r" % (i, got, "".join(units)))
    out.append({"i": i, "start": round(seg[0]["start_time"], 3), "end": round(seg[-1]["end_time"], 3), "text": l["say"]})
if k != len(words):
    sys.exit("%d timestamp words left over: the take does not match script.json" % (len(words) - k))

total = round(out[-1]["end"] + tail, 3)
os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
subprocess.run([ff, "-v", "error", "-y", "-i", os.path.join(d, "full.raw"),
                "-af", "apad,atrim=0:%s,loudnorm=I=-16:TP=-1.5:LRA=11" % total,
                "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", os.path.join(proj, "assets/vo.wav")], check=True)
json.dump({"total": total, "voice": voice, "take": "whole", "lines": out},
          open(os.path.join(proj, "timing.json"), "w"), ensure_ascii=False, indent=1)
print("total %.2fs" % total)
for o in out: print("%5.2f-%5.2f %s" % (o["start"], o["end"], o["text"]))
