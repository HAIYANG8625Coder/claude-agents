"""Turn a one-take voice (full.raw + words.json) into assets/vo.wav + timing.json, sentence times from word timestamps.

Usage: python3 -I build_vo.py <video folder> --dir <take folder, e.g. .voice-heygen-full-0.92> [--tail 0.9]
The old timing.json is kept as timing.prev.json so sync.py can move any hand-made tweens along with the speech.
"""
import json, os, re, shutil, subprocess, sys

proj = sys.argv[1]
take = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else ".voice-heygen-full"
tail = float(sys.argv[sys.argv.index("--tail") + 1]) if "--tail" in sys.argv else 0.9
ff = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../avatar-video/node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
d = os.path.join(proj, take)
lines = json.load(open(os.path.join(proj, "script.json")))
words = [w for w in json.load(open(os.path.join(d, "words.json"))) if re.search(r"\w", w["text"])]
U = lambda s: [c.lower() for c in s if c.isalnum()]  # compare letter by letter: "M O E" = "MOE", "Claude Code" = "ClaudeCode"

# HeyGen's word starts run ~0.15-0.2 s early after a pause. Snap a start that falls inside a real pause to the
# moment the voice comes back, so scenes and captions land on the sound instead of just before it.
err = subprocess.run([ff, "-hide_banner", "-i", os.path.join(d, "full.raw"), "-af", "silencedetect=n=-40dB:d=0.12",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
pauses = list(zip(map(float, re.findall(r"silence_start: ([\d.]+)", err)), map(float, re.findall(r"silence_end: ([\d.]+)", err))))
moved = 0
for w in words:
    for a, b in pauses:
        if a - 0.02 <= w["start_time"] < b and b - w["start_time"] < 0.4:
            w["start_time"] = round(b, 3); moved += 1; break
json.dump(words, open(os.path.join(d, "words.aligned.json"), "w"), ensure_ascii=False)
print("aligned %d word starts to the end of a pause" % moved)

# match on tokens, not HeyGen words: "Claude Code" may come back as one word or two
toks = [{"t": x, "start_time": w["start_time"], "end_time": w["end_time"]} for w in words for x in U(w["text"])]
out, k = [], 0
for i, l in enumerate(lines):
    units = U(l["say"])
    seg = toks[k:k + len(units)]; k += len(units)
    if [w["t"] for w in seg] != units:
        sys.exit("sentence %d does not match the take: heard %r, script %r. Regenerate the take from the current script.json."
                 % (i, "".join(w["t"] for w in seg), l["say"]))
    out.append({"i": i, "start": round(seg[0]["start_time"], 3), "end": round(seg[-1]["end_time"], 3), "text": l["say"]})
if k != len(toks):
    sys.exit("%d spoken words left over: the take does not match script.json" % (len(toks) - k))

total = round(out[-1]["end"] + tail, 3)
tj = os.path.join(proj, "timing.json")
if os.path.exists(tj): shutil.copy(tj, os.path.join(proj, "timing.prev.json"))
os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
subprocess.run([ff, "-v", "error", "-y", "-i", os.path.join(d, "full.raw"),
                "-af", "apad,atrim=0:%s,loudnorm=I=-16:TP=-1.5:LRA=11" % total,
                "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", os.path.join(proj, "assets/vo.wav")], check=True)
json.dump({"total": total, "take_dir": take, "lines": out}, open(tj, "w"), ensure_ascii=False, indent=1)
print("total %.2fs" % total)
for o in out: print("%5.2f-%5.2f %s" % (o["start"], o["end"], o["text"]))
