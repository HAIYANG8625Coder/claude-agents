"""Slow a one-take voice down (pitch kept) and scale its word timestamps to match.

HeyGen ignores `speed` for instant clones, so this stretches the take with ffmpeg atempo instead.
Usage: python3 -I avatar-video/tools/slow-take.py <video folder> <tempo, e.g. 0.92> [--src .voice-heygen-full]
Writes <video>/.voice-heygen-full-<tempo>/{full.raw,words.json}; then run heygen-whole.py with --dir that folder.
"""
import json, os, subprocess, sys

proj, tempo = sys.argv[1], float(sys.argv[2])
src = os.path.join(proj, sys.argv[sys.argv.index("--src") + 1] if "--src" in sys.argv else ".voice-heygen-full")
dst = os.path.join(proj, ".voice-heygen-full-%s" % sys.argv[2]); os.makedirs(dst, exist_ok=True)
ff = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
subprocess.run([ff, "-v", "error", "-y", "-i", os.path.join(src, "full.raw"), "-af", "atempo=%s" % tempo,
                "-c:a", "pcm_s16le", "-f", "wav", os.path.join(dst, "full.raw")], check=True)
words = json.load(open(os.path.join(src, "words.json")))
for w in words:
    w["start_time"] = round(w["start_time"] / tempo, 3); w["end_time"] = round(w["end_time"] / tempo, 3)
json.dump(words, open(os.path.join(dst, "words.json"), "w"), ensure_ascii=False)
print("slowed to %.0f%% -> %s" % (tempo * 100, dst))
