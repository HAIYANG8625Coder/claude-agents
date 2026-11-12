"""Voice a video's script.json with a HeyGen voice (e.g. Michael's clone), one sentence per call.

Same output as say-voice.py: <video>/assets/vo.wav + <video>/timing.json with exact per-sentence times,
so captions need no transcription. Each sentence costs HeyGen credits (charged per character).

Usage: python3 -I avatar-video/tools/heygen-voice.py <video folder> <voice_id> [--speed 1.0]
Needs: npx hyperframes auth login, and Node on PATH (~/.local/node/bin).
"""
import json, os, subprocess, sys

proj, voice = sys.argv[1], sys.argv[2]
speed = sys.argv[sys.argv.index("--speed") + 1] if "--speed" in sys.argv else None
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(here))
tts = os.path.join(root, ".claude/skills/media-use/audio/scripts/heygen-tts.mjs")
ff = os.path.join(here, "../node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
fp = os.path.join(here, "../node_modules/@ffprobe-installer/darwin-arm64/ffprobe")
lines = json.load(open(os.path.join(proj, "script.json")))
tmp = os.path.join(proj, ".voice-heygen"); os.makedirs(tmp, exist_ok=True)
GAP = 0.22
sil = lambda d, n: subprocess.run([ff, "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(d), n], check=True)
dur = lambda f: float(subprocess.run([fp, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)

t = 0.15; parts = []; out = []
lead = os.path.join(tmp, "lead.wav"); sil(0.15, lead); parts.append(lead)
for i, l in enumerate(lines):
    raw = os.path.join(tmp, "s%02d.raw.wav" % i); wav = os.path.join(tmp, "s%02d.wav" % i)
    if not os.path.exists(raw):  # re-runs reuse finished sentences, so a retry doesn't pay twice
        cmd = ["node", tts, l["say"], "-o", raw, "--voice", voice, "--lang", "zh"]
        if speed: cmd += ["--speed", speed]
        subprocess.run(cmd, check=True)
    # trim the silence HeyGen leaves at both ends, so our own pauses set the rhythm
    trim = "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse"
    subprocess.run([ff, "-v", "error", "-y", "-i", raw, "-af", trim, "-ar", "44100", "-ac", "1", wav], check=True)
    d = dur(wav)
    out.append({"i": i, "start": round(t, 3), "end": round(t + d, 3), "text": l["say"]})
    parts.append(wav); t += d
    pause = l.get("pause", GAP); g = os.path.join(tmp, "g%02d.wav" % i); sil(pause, g); parts.append(g); t += pause

lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join("file '%s'\n" % os.path.abspath(p) for p in parts))
os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
joined = os.path.join(tmp, "joined.wav")
subprocess.run([ff, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:a", "pcm_s16le", joined], check=True)
subprocess.run([ff, "-v", "error", "-y", "-i", joined, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "pcm_s16le",
                os.path.join(proj, "assets/vo.wav")], check=True)
json.dump({"total": round(t, 3), "voice": voice, "lines": out}, open(os.path.join(proj, "timing.json"), "w"), ensure_ascii=False, indent=1)
print("total %.2fs" % t)
for o in out: print("%5.2f-%5.2f %s" % (o["start"], o["end"], o["text"]))
