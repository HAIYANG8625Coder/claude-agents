"""Check a rendered voice-video: length, peaks, long silences, a 4-frame strip at scene changes and the end.

Usage: python3 -I qa.py <video folder> [render.mp4]   (default: newest file in renders/)
Prints a short report and writes renders/qa.png; open it with Read and look at it.
"""
import glob, json, os, re, subprocess, sys

proj = sys.argv[1]
mp4 = sys.argv[2] if len(sys.argv) > 2 else max(glob.glob(os.path.join(proj, "renders/*.mp4")), key=os.path.getmtime)
nm = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../avatar-video/node_modules")
ff, fp = nm + "/@ffmpeg-installer/darwin-arm64/ffmpeg", nm + "/@ffprobe-installer/darwin-arm64/ffprobe"
tm = json.load(open(os.path.join(proj, "timing.json")))
run = lambda *a: subprocess.run(a, capture_output=True, text=True)
dur = float(run(fp, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4).stdout)
err = run(ff, "-hide_banner", "-i", mp4, "-af", "volumedetect,silencedetect=n=-40dB:d=0.7", "-f", "null", "-").stderr
peak = float(re.search(r"max_volume: (-?[\d.]+)", err).group(1))
sil = re.findall(r"silence_start: ([\d.]+)", err)
print("render: %s" % mp4)
print("length %.2fs (timing says %.2fs) %s" % (dur, tm["total"], "OK" if abs(dur - tm["total"]) < 0.15 else "MISMATCH"))
print("peak %.1f dB %s" % (peak, "OK" if peak <= -1.0 else "CLIPPING RISK"))
inner = [float(s) for s in sil if float(s) < tm["lines"][-1]["end"]]
print("silences > 0.7 s before the last word: %s" % (", ".join("%.2f" % s for s in inner) or "none (good)"))
L = tm["lines"]; pick = [L[1]["start"] - 0.1, L[len(L) // 2]["start"] + 0.5, L[-1]["start"] - 0.1, tm["total"] - 0.3]
fr = []
for i, t in enumerate(pick):
    f = os.path.join(proj, "renders/.qa%d.png" % i); fr.append(f)
    run(ff, "-v", "error", "-y", "-ss", "%.2f" % max(0, t), "-i", mp4, "-frames:v", "1", "-vf", "scale=300:-1", f)
args = [ff, "-v", "error", "-y"] + [x for f in fr for x in ("-i", f)] + ["-filter_complex", "hstack=%d" % len(fr), os.path.join(proj, "renders/qa.png")]
run(*args); [os.remove(f) for f in fr]
print("frames at %s -> renders/qa.png (check: no blank stage, caption matches the words, end card visible)" % ", ".join("%.1fs" % t for t in pick))
