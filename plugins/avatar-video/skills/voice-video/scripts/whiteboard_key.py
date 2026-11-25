"""Green-screen key for a new marker hand: hand-green.png (square) -> hand.png with alpha, plus a check picture on white.

Usage: python3 -I whiteboard_key.py <hand-green.png> <hand.png>
Alpha comes from how much greener a pixel is than red/blue. ffmpeg's chromakey made a black marker see-through
and colorkey ate the skin, so this does it by hand. Look at <hand>-check.png before using the result.
"""
import math, pathlib, shutil, subprocess, sys

if len(sys.argv) != 3:
    raise SystemExit(__doc__)
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
FF = str(pathlib.Path(__file__).resolve().parents[5] / "avatar-video/node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
if not pathlib.Path(FF).exists():
    FF = shutil.which("ffmpeg") or sys.exit("no ffmpeg: run npm install in avatar-video/")
raw = subprocess.run([FF, "-loglevel", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
px = bytearray()
for i in range(0, len(raw), 3):
    r, g, b = raw[i], raw[i + 1], raw[i + 2]
    ex = g - max(r, b)
    a = 255 if ex <= 6 else 0 if ex >= 45 else int(255 * (45 - ex) / 39)
    if ex > 0:
        g = max(r, b)
    px += bytes((r, g, b, a))
# trim one pixel off the outline and take the green tint out of the pixels next to it
al = bytes(px[3::4])
W = math.isqrt(len(al))
assert W * W == len(al), "the hand picture must be square"
for y in range(3, W - 3):
    for x in range(3, W - 3):
        i = y * W + x
        if not al[i] or min(al[i - 3], al[i + 3], al[i - 3 * W], al[i + 3 * W]) == 255:
            continue
        j = i * 4
        px[j + 3] = min(al[i], al[i - 1], al[i + 1], al[i - W], al[i + W])
        px[j + 1] = min(px[j + 1], int(0.6 * px[j] + 0.4 * px[j + 2]))
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "%dx%d" % (W, W), "-i", "-", "-frames:v", "1", str(out)], input=bytes(px), check=True)
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=white:s=%dx%d" % (W, W), "-i", str(out), "-filter_complex", "[0][1]overlay=format=auto", "-frames:v", "1", str(out.with_name(out.stem + "-check.png"))], check=True)
