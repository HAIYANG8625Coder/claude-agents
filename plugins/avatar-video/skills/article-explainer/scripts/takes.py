"""Record a long voice-over as one take per chapter, then join the takes into one take for build_vo.py.

A 5-8 min script is too long for one HeyGen create_speech call (and for heygen_take.sh's 580 s timeout).
Chapters are natural pauses, so a fresh intonation per chapter sounds fine; never split inside a chapter.

script.json items carry "ch": the chapter number (0 = opening, 1.. = chapters, last = ending).
  python3 -I takes.py split <video folder>    -> parts/ch<N>/script.json, one folder per chapter
  zsh <voice-video>/scripts/heygen_take.sh <video folder>/parts/ch<N>   (once per chapter)
  python3 -I takes.py merge <video folder> [--gap 0.7]
     -> <video>/.voice-heygen-full/{full.raw,words.json}: the chapter takes joined with <gap> s of silence,
        word times shifted to match. Then run slow_take.py and build_vo.py as for a one-take video.
"""
import json, os, subprocess, sys, wave

cmd, proj = sys.argv[1], sys.argv[2]
gap = float(sys.argv[sys.argv.index("--gap") + 1]) if "--gap" in sys.argv else 0.7
ff = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../../avatar-video/node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
lines = json.load(open(os.path.join(proj, "script.json")))
chs = sorted({l.get("ch", 0) for l in lines})
part = lambda c: os.path.join(proj, "parts", "ch%d" % c)

if cmd == "split":
    for c in chs:
        os.makedirs(part(c), exist_ok=True)
        json.dump([{"say": l["say"]} for l in lines if l.get("ch", 0) == c], open(os.path.join(part(c), "script.json"), "w"),
                  ensure_ascii=False, indent=1)
        n = sum(len(l["say"]) for l in lines if l.get("ch", 0) == c)
        print("ch%d: %d characters -> %s" % (c, n, part(c)))
elif cmd == "merge":
    out = os.path.join(proj, ".voice-heygen-full"); os.makedirs(out, exist_ok=True)
    words, offset, inputs = [], 0.0, []
    for c in chs:
        d = os.path.join(part(c), ".voice-heygen-full")
        if not (os.path.exists(os.path.join(d, "full.raw")) and os.path.exists(os.path.join(d, "words.json"))):
            sys.exit("ch%d has no take yet: run heygen_take.sh %s" % (c, part(c)))
        with wave.open(os.path.join(d, "full.raw")) as w:
            dur = w.getnframes() / w.getframerate()
        for x in json.load(open(os.path.join(d, "words.json"))):
            words.append(dict(x, start_time=round(x["start_time"] + offset, 3), end_time=round(x["end_time"] + offset, 3)))
        inputs.append(os.path.join(d, "full.raw")); offset += dur + gap
    # every take padded with the gap, then concatenated: offsets above use the same durations
    fc = "".join("[%d:a]aformat=sample_rates=44100:channel_layouts=mono,apad=pad_dur=%s[a%d];" % (i, gap, i) for i in range(len(inputs)))
    fc += "".join("[a%d]" % i for i in range(len(inputs))) + "concat=n=%d:v=0:a=1[out]" % len(inputs)
    args = [ff, "-v", "error", "-y"]
    for p in inputs: args += ["-i", p]
    subprocess.run(args + ["-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s16le", "-f", "wav", os.path.join(out, "full.raw")], check=True)
    json.dump(words, open(os.path.join(out, "words.json"), "w"), ensure_ascii=False)
    print("merged %d chapter takes, %.1f s -> %s" % (len(inputs), offset - gap, out))
else:
    sys.exit("usage: takes.py split|merge <video folder> [--gap 0.7]")
