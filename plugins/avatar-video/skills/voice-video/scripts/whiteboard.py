"""Build index.html for a whiteboard hand-drawing video (style preset I), vertical 9:16, one board per sentence.

Usage: python3 -I whiteboard.py <video folder>
       python3 -I whiteboard.py <video folder> --cover renders/<video>.mp4     (3:4 cover from the first board)

Reads from the folder: boards.json, script.json, timing.json (build_vo.py), the take's words.aligned.json (or a
words.json in the folder), assets/vo.wav and assets/raw/sNN.png (NN = board number, 3:4 line drawings on white).
Writes assets/img/ and index.html. Format of boards.json, picture prompts and pitfalls: ../references/whiteboard.md
A white mask is uncovered along a zigzag over each drawing's inked area while a hand with a marker follows:
a right hand for the right column, its mirror image for the left column. Draw times come from the spoken words.
"""
import json, math, pathlib, re, shutil, subprocess, sys

if len(sys.argv) < 2:
    raise SystemExit(__doc__)
H = pathlib.Path(sys.argv[1]).resolve()
REPO = pathlib.Path(__file__).resolve().parents[5]
FF = str(REPO / "avatar-video/node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg")
if not pathlib.Path(FF).exists():
    FF = shutil.which("ffmpeg") or sys.exit("no ffmpeg: run npm install in avatar-video/")
TM = json.loads((H / "timing.json").read_text())
D = TM["total"]
if "--cover" in sys.argv:
    video = H / sys.argv[sys.argv.index("--cover") + 1]
    out = H / "renders/cover-3x4.png"
    out.parent.mkdir(exist_ok=True)
    # the end of the first board, cropped to title + drawings (no captions) and padded to 3:4
    vf = ("format=rgb24,crop=1080:1640:0:35,pad=1230:1640:75:0:color=0xfdfdfd,"
          "drawbox=x=0:y=0:w=iw:h=24:color=0xfdfdfd:t=fill")
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "%.2f" % (TM["lines"][1]["start"] - 0.19), "-i", str(video),
                    "-frames:v", "1", "-vf", vf, str(out)], check=True)
    print(out)
    raise SystemExit
CFG = json.loads((H / "boards.json").read_text())
BOARD_CFG, SHEET = CFG["boards"], CFG.get("sheet")
LINES = [x["say"] for x in json.loads((H / "script.json").read_text())]
assert len(LINES) == len(BOARD_CFG) + bool(SHEET), "one board per sentence (the sheet, if any, takes the last one)"
X0, Y0, IW, IH = 20, 270, 1040, 1393          # where a 3:4 drawing sits
STEP = 62                                     # distance between zigzag strokes

# (column, row, phrase that starts it, label); listed in drawing order
SCENES = [(b.get("num", ""), b["title"], b["sub"], b.get("rows", 2), b["items"]) for b in BOARD_CFG]

(H / "assets/img").mkdir(parents=True, exist_ok=True)
if not (H / "assets/img/hand.png").exists():
    shutil.copy(REPO / "avatar-video/brand/whiteboard/hand.png", H / "assets/img/hand.png")
if (H / "words.json").exists():
    WORDS = json.loads((H / "words.json").read_text())
else:
    WORDS = json.loads((H / TM.get("take_dir", ".voice-heygen-full") / "words.aligned.json").read_text())

# ---- spoken time of every letter and character
def toks(s): return [c.lower() for c in s if c.isalnum()]
spoken = [(c, w["start_time"]) for w in WORDS for c in toks(w["text"])]
LT, k = [], 0
for s in LINES:
    t = toks(s)
    assert [c for c, _ in spoken[k:k + len(t)]] == t, "words do not match the script: " + s
    LT.append([x for _, x in spoken[k:k + len(t)]])
    k += len(t)
assert k == len(spoken)


def at(i, phrase):
    p, seq = toks(phrase), toks(LINES[i])
    for j in range(len(seq) - len(p) + 1):
        if seq[j:j + len(p)] == p:
            return LT[i][j]
    raise SystemExit("phrase %r not in line %d" % (phrase, i + 1))


START = [0.0] + [round(l["start"] - 0.1, 3) for l in TM["lines"][1:]] + [D]


# ---- pictures
def prepare(i):
    src = H / "assets/raw" / ("s%02d.png" % (i + 1))
    out = H / "assets/img" / ("s%02d.png" % (i + 1))
    vf = "scale=%d:%d:flags=lanczos,colorlevels=rimax=0.965:gimax=0.965:bimax=0.965" % (IW, IH)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(src), "-vf", vf, "-frames:v", "1", str(out)], check=True)
    return subprocess.run([FF, "-loglevel", "error", "-i", str(out), "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout


def cells(gray, rows):
    """bounding box (video px, inside the picture) of the ink in each grid cell: connected blobs, assigned by centre"""
    S = 4
    w, h = IW // S, IH // S
    ink = [[False] * w for _ in range(h)]
    for y in range(h * S):
        row = y * IW
        for x in range(w * S):
            if gray[row + x] < 232:
                ink[y // S][x // S] = True
    R = 2
    fat = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if ink[y][x]:
                for yy in range(max(0, y - R), min(h, y + R + 1)):
                    for xx in range(max(0, x - R), min(w, x + R + 1)):
                        fat[yy][xx] = True
    seen, boxes, spans = [[False] * w for _ in range(h)], {}, []
    for y in range(h):
        for x in range(w):
            if not fat[y][x] or seen[y][x]:
                continue
            seen[y][x] = True
            q, xs, ys = [(x, y)], [], []
            while q:
                cx, cy = q.pop()
                if ink[cy][cx]:
                    xs.append(cx)
                    ys.append(cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and fat[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        q.append((nx, ny))
            if len(xs) < 6:
                continue
            b = (min(xs) * S, min(ys) * S, (max(xs) + 1) * S, (max(ys) + 1) * S)
            col = 0 if (b[0] + b[2]) / 2 < IW / 2 else 1
            r = min(rows - 1, int((b[1] + b[3]) / 2 / (IH / rows)))
            if b[2] - b[0] > IW * 0.55 or b[3] - b[1] > IH * 0.55:
                spans.append(b)
            o = boxes.get((col, r), b)
            boxes[(col, r)] = (min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3]))
    assert not spans, "drawings touch across cells: %s" % spans
    return boxes


def zigzag(gray, box):
    """diagonal strokes (x + y = c) across the box, each only as long as the ink in that band"""
    x1, y1, x2, y2 = box
    bands = {}
    for y in range(max(0, y1), min(IH, y2)):
        row = y * IW
        for x in range(max(0, x1), min(IW, x2)):
            if gray[row + x] < 238:
                n = (x - x1 + y - y1) // STEP
                lo, hi = bands.get(n, (x, x))
                bands[n] = (min(lo, x), max(hi, x))
    pts = []
    for j, n in enumerate(sorted(bands)):
        c = x1 + y1 + n * STEP + STEP / 2
        a, b = bands[n][0] - 14, bands[n][1] + 14
        ends = [(a, c - a), (b, c - b)]
        if j % 2:
            ends.reverse()
        pts += [(X0 + x, Y0 + y) for x, y in ends]
    return "M" + " L".join("%.0f %.0f" % p for p in pts)


def width(s, size):
    return sum(size if ord(c) > 255 else size * 0.58 for c in s)


def header(num, title, sub):
    g = ""
    room = 740 if num else 1000                  # a long title shrinks instead of running under the number badge
    size = min(140, int(140 * room / max(1, width(title, 140))))
    if num:
        g += f'<rect x="36" y="86" width="116" height="92" rx="22" fill="#111"/><text x="94" y="150" font-size="52" font-weight="900" text-anchor="middle" fill="#fff">{num}</text>'
    g += f'<text x="540" y="205" font-size="{size}" font-weight="900" text-anchor="middle" fill="#111">{title}</text>'
    w = width(sub, 46) + 70
    return g, (f'<rect x="{540 - w / 2:.0f}" y="240" width="{w:.0f}" height="76" rx="38" fill="#111"/>'
               f'<text x="540" y="293" font-size="46" font-weight="900" text-anchor="middle" fill="#fff">{sub}</text>')


defs, stage, boards = [], [], []
n = 0
for i, (num, title, sub, rows, items) in enumerate(SCENES):
    gray = prepare(i)
    found = cells(gray, rows)
    assert {(c, r) for c, r, _, _ in items} <= set(found), "scene %d cells %s" % (i + 1, sorted(found))
    # draw times: start on the phrase, finish before the next one, leave time to change hands
    mods = []
    for j, (c, r, phrase, label) in enumerate(items):
        if phrase is None:                       # already on the first frame (thumbnail)
            mods.append({"a": -2.0, "b": -1.0, "side": "LR"[c]})
            continue
        a = max(at(i, phrase) - 0.15, START[i] + 0.05)
        prev = next((m for m in reversed(mods) if m["b"] > 0), None)
        if prev:
            a = max(a, prev["b"] + (0.3 if prev["side"] != "LR"[c] else 0.1))
        nxt = at(i, items[j + 1][2]) - 0.45 if j + 1 < len(items) else START[i + 1] - 0.45
        b = max(a + 0.45, min(nxt, a + (2.0 if j == 0 else 1.35)))
        mods.append({"a": round(a, 3), "b": round(b, 3), "side": "LR"[c]})
    assert mods[-1]["b"] < START[i + 1] - 0.15, "scene %d runs out of time: %s" % (i + 1, mods)
    head, pill = header(num, title, sub)
    art, labels = [], []
    for j, ((c, r, phrase, label), m) in enumerate(zip(items, mods)):
        b = found[(c, r)]
        box = (b[0] - 10, b[1] - 10, b[2] + 10, b[3] + 10)
        bx, by, bw, bh = X0 + box[0], Y0 + box[1], box[2] - box[0], box[3] - box[1]
        if (c == 1 and bx < 480) or (c == 0 and bx + bw > 600):
            print("note: scene %d item %d reaches far from its side (%d..%d)" % (i + 1, j + 1, bx, bx + bw))
        rect = f'x="{bx}" y="{by}" width="{bw}" height="{bh}"'
        mid = "%d" % n
        defs.append(f'<clipPath id="cp{mid}"><rect {rect}/></clipPath>'
                    f'<mask id="m{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1080" height="1920">'
                    f'<path id="p{mid}" d="{zigzag(gray, box)}" fill="none" stroke="#fff" stroke-width="{STEP * 1.5:.0f}" stroke-linecap="round" stroke-linejoin="round" visibility="hidden"/>'
                    f'<rect id="full{mid}" {rect} fill="#fff" visibility="hidden"/></mask>')
        art.append(f'<g clip-path="url(#cp{mid})"><image mask="url(#m{mid})" href="assets/img/s{i + 1:02d}.png" x="{X0}" y="{Y0}" width="{IW}" height="{IH}"/></g>')
        half = width(label, 50) / 2
        cx = min(max(bx + bw / 2, half + 14), 1066 - half)
        ly = min(Y0 + b[3] + 62, 1628)
        labels.append(f'<g id="lb{mid}" opacity="0"><text x="{cx:.0f}" y="{ly}" font-size="50" font-weight="900" text-anchor="middle" fill="#111" stroke="#fff" stroke-width="10" paint-order="stroke">{label}</text></g>')
        m["id"] = n
        n += 1
    stage.append(f'<g id="sc{i}" visibility="hidden">{head}<g id="sub{i}" opacity="0">{pill}</g>{"".join(art)}{"".join(labels)}</g>')
    boards.append({"a": START[i], "b": START[i + 1], "sub": -1 if i == 0 else round(START[i] + 0.1, 3), "mods": mods})
    print("scene %2d: " % (i + 1) + "  ".join("%.2f-%.2f%s" % (m["a"], m["b"], m["side"]) for m in mods))

# ---- the last board (optional): a list to save, built from text
pops = []
if SHEET:
    last = len(SCENES)
    rows = SHEET["rows"]
    assert 1 <= len(rows) <= 11, "the sheet holds up to 11 rows"
    pitch = min(130, 1122 // len(rows))
    high = pitch - 16
    g = f'<text x="540" y="205" font-size="110" font-weight="900" text-anchor="middle" fill="#111">{SHEET["title"]}</text>'
    for j, (a, b) in enumerate(rows):
        y = 270 + j * pitch
        mid_y = y + high // 2
        g += (f'<g id="row{j}" opacity="0"><rect x="45" y="{y}" width="990" height="{high}" rx="20" fill="#fff" stroke="#111" stroke-width="5"/>'
              f'<rect x="45" y="{y}" width="270" height="{high}" rx="20" fill="#111"/><text x="180" y="{mid_y + 16}" font-size="44" font-weight="900" text-anchor="middle" fill="#fff">{a}</text>'
              f'<text x="350" y="{mid_y + 15}" font-size="42" font-weight="800" fill="#111">{b}</text></g>')
        pops.append(["row%d" % j, round(START[last] + 0.1 + j * 0.11, 3)])
    g += ('<g id="ask" opacity="0"><rect x="45" y="1425" width="990" height="120" rx="60" fill="#ffd84d" stroke="#111" stroke-width="6"/>'
          f'<text x="540" y="1502" font-size="50" font-weight="900" text-anchor="middle" fill="#111">{SHEET["ask"]}</text></g>')
    g += ('<g id="star" opacity="0"><rect x="800" y="58" width="240" height="88" rx="44" fill="#111"/>'
          f'<text x="920" y="118" font-size="46" font-weight="900" text-anchor="middle" fill="#fff">{SHEET["star"]}</text></g>')
    pops += [["ask", round(at(last, SHEET["ask_at"]) - 0.1, 3)], ["star", round(at(last, SHEET["star_at"]) - 0.1, 3)]]
    stage.append(f'<g id="sc{last}" visibility="hidden">{g}</g>')
    boards.append({"a": START[last], "b": D, "sub": -1, "mods": []})

# ---- hands: the forearm below a cut line is stretched a little, so it reaches the side of the frame
TIP, HS = (274, 340), 0.74
P, U = (720, 790), (0.73, 0.683)
norm = math.hypot(*U)
U = (U[0] / norm, U[1] / norm)
V = (-U[1], U[0])
STRETCH = 2.8


def half_plane(sign, overlap=0):
    base = (P[0] + U[0] * overlap, P[1] + U[1] * overlap)
    q = [(base[0] + V[0] * 1600, base[1] + V[1] * 1600), (base[0] - V[0] * 1600, base[1] - V[1] * 1600)]
    q += [(x + sign * U[0] * 2400, y + sign * U[1] * 2400) for x, y in reversed(q)]
    return " ".join("%.1f,%.1f" % p for p in q)


a_, c_ = 1 + (STRETCH - 1) * U[0] ** 2, (STRETCH - 1) * U[0] * U[1]
d_ = 1 + (STRETCH - 1) * U[1] ** 2
e_, f_ = P[0] - (a_ * P[0] + c_ * P[1]), P[1] - (c_ * P[0] + d_ * P[1])
defs.append(f'<clipPath id="handA"><polygon points="{half_plane(-1, 2)}"/></clipPath><clipPath id="handB"><polygon points="{half_plane(1)}"/></clipPath>')
IMG = '<image href="assets/img/hand.png" x="0" y="0" width="1024" height="1024"/>'
hand = "".join(f'<g id="hand{side}" visibility="hidden"><g transform="matrix({a_:.5f} {c_:.5f} {c_:.5f} {d_:.5f} {e_:.2f} {f_:.2f})" clip-path="url(#handB)">{IMG}</g>'
               f'<g clip-path="url(#handA)">{IMG}</g></g>' for side in "LR")

# ---- captions
SHOW = CFG.get("show", [])                    # spoken spelling -> caption spelling, e.g. ["A I", "AI"]
caps, cap_html = [], []
for i, say in enumerate(LINES):
    parts = [p.strip() for p in re.split(r"[，。：；？、]", say) if p.strip()]
    ln = lambda s: len(re.sub(r"\s", "", s))
    out, cur = [], ""
    for p in parts:
        if cur and ln(cur) + ln(p) > 15:
            out.append(cur)
            cur = ""
        cur = (cur + "，" + p) if cur else p
        if ln(cur) >= 6:
            out.append(cur)
            cur = ""
    if cur:
        if out and ln(out[-1]) + ln(cur) <= 15:
            out[-1] += "，" + cur
        else:
            out.append(cur)
    used = 0
    for c in out:
        shown = c
        for x, y in SHOW:
            shown = shown.replace(x, y)
        html, times = "", []
        for unit in re.findall(r"[A-Za-z0-9]+|.", shown):
            if unit.isalnum() or ord(unit[0]) > 0x3400 and unit.isalpha():
                html += f'<span class="k">{unit}</span>'
                times.append(LT[i][used])
                used += len(toks(unit))
            else:
                html += unit
        caps.append({"from": 0 if not caps else round(times[0] - 0.08, 3), "words": times})
        cap_html.append(f'<div class="cap" id="c{len(cap_html)}">{html}</div>')
    assert used == len(LT[i]), "caption letters do not add up in line %d" % (i + 1)

page = f"""<!doctype html>
<html lang="zh" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "PingFang SC"; src: local("PingFang SC"), local("PingFangSC-Semibold"); }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#ffffff; }}
      #root {{ position:relative; width:100%; height:100%; font-family:"PingFang SC",sans-serif; color:#111; background:#ffffff; }}
      #stage {{ position:absolute; inset:0; }}
      #stage svg {{ display:block; font-family:"PingFang SC",sans-serif; }}
      .cap {{ position:absolute; left:30px; right:30px; top:1690px; text-align:center; font-size:58px; line-height:1.25; font-weight:900; visibility:hidden; }}
      .cap .k {{ opacity:.3; }}
      #progress {{ position:absolute; left:40px; right:40px; top:30px; height:12px; background:#111; transform-origin:left center; }}
      #foot {{ position:absolute; left:0; right:0; top:1825px; text-align:center; font-size:28px; font-weight:700; color:#666; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="progress" class="clip" data-start="0" data-duration="{D}" data-track-index="0"></div>
      <div id="stage" class="clip" data-start="0" data-duration="{D}" data-track-index="1" data-track-kind="graphics">
        <svg viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-allow-overflow>
          <defs>{"".join(defs)}</defs>
          {"".join(stage)}
          <g data-layout-allow-overflow>{hand}</g>
        </svg>
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{D}" data-track-index="2">{"".join(cap_html)}</div>
      <div id="foot" data-layout-ignore class="clip" data-start="0" data-duration="{D}" data-track-index="3">{CFG.get("footer", "手绘动画示意 · 画面由 AI 生成")}</div>
      <audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{D}" data-track-index="4"></audio>
    </div>
    <script>
      const D = {D}, BOARDS = {json.dumps(boards)}, CAPS = {json.dumps(caps)}, POPS = {json.dumps(pops)};
      const $ = (id) => document.getElementById(id);
      const paths = [], lens = [];
      BOARDS.forEach((s) => s.mods.forEach((m) => {{
        const p = $("p" + m.id);
        paths[m.id] = p; lens[m.id] = p.getTotalLength();
        p.setAttribute("stroke-dasharray", lens[m.id] + " " + lens[m.id] * 2);
      }}));
      const clamp = (v) => Math.max(0, Math.min(1, v));
      const ease = (v) => v * v * (3 - 2 * v);
      const mix = (a, b, v) => ({{ x: a.x + (b.x - a.x) * v, y: a.y + (b.y - a.y) * v }});
      // pen position: half on the stroke being uncovered, half on a smoothed path, so the hand does not shake
      function pen(i, p) {{
        const at = (q) => paths[i].getPointAtLength(clamp(q) * lens[i]);
        let sx = 0, sy = 0;
        for (let j = -4; j <= 4; j++) {{ const s = at(p + j * 0.025); sx += s.x; sy += s.y; }}
        return mix(at(p), {{ x: sx / 9, y: sy / 9 }}, 0.5);
      }}
      // off the frame on the hand's own side
      const off = (side, p) => ({{ x: p.x + (side === "L" ? -800 : 800), y: p.y + 220 }});
      function handAt(s, t) {{
        const on = (p, side) => ({{ x: p.x, y: p.y, side: side }});
        const mods = s.mods.filter((m) => m.b > 0);
        if (!mods.length) return null;
        for (let i = 0; i < mods.length; i++) {{
          const m = mods[i];
          if (t < m.a) {{
            if (i === 0) {{
              const g = clamp((t - (m.a - 0.35)) / 0.35), start = pen(m.id, 0);
              return g > 0 ? on(mix(off(m.side, start), start, ease(g)), m.side) : null;
            }}
            const prev = mods[i - 1], gap = m.a - prev.b, g = clamp((t - prev.b) / gap), from = pen(prev.id, 1), to = pen(m.id, 0);
            if (prev.side === m.side && gap < 0.9) return on(mix(from, to, ease(g)), m.side);
            // a long pause or a change of side: leave, stay away, come back
            const leave = Math.min(gap * 0.45, 0.4), back = Math.min(gap * 0.55, 0.4);
            if (t < prev.b + leave) return on(mix(from, off(prev.side, from), ease((t - prev.b) / leave)), prev.side);
            if (t < m.a - back) return null;
            return on(mix(off(m.side, to), to, ease(clamp((t - m.a + back) / back))), m.side);
          }}
          if (t <= m.b) return on(pen(m.id, (t - m.a) / (m.b - m.a)), m.side);
        }}
        const last = mods[mods.length - 1], end = pen(last.id, 1), g = clamp((t - last.b - 0.05) / 0.45);
        return g < 1 ? on(mix(end, off(last.side, end), ease(g)), last.side) : null;
      }}
      function render(t) {{
        $("progress").style.transform = "scaleX(" + clamp(t / D).toFixed(4) + ")";
        let h = null;
        BOARDS.forEach((s, i) => {{
          const on = t >= s.a && (t < s.b || i === BOARDS.length - 1);
          $("sc" + i).setAttribute("visibility", on ? "visible" : "hidden");
          if (!on) {{
            // visibility set on a child would override the hidden board, so reset the strokes
            s.mods.forEach((m) => {{ paths[m.id].setAttribute("visibility", "hidden"); $("full" + m.id).setAttribute("visibility", "hidden"); }});
            return;
          }}
          if ($("sub" + i)) $("sub" + i).setAttribute("opacity", s.sub < 0 ? 1 : ease(clamp((t - s.sub) / 0.25)));
          s.mods.forEach((m) => {{
            const p = clamp((t - m.a) / (m.b - m.a));
            paths[m.id].setAttribute("visibility", p > 0 ? "visible" : "hidden");
            paths[m.id].setAttribute("stroke-dashoffset", lens[m.id] * (1 - p));
            $("full" + m.id).setAttribute("visibility", p >= 1 ? "visible" : "hidden");
            $("lb" + m.id).setAttribute("opacity", ease(clamp((t - m.a - (m.b - m.a) * 0.4) / 0.25)));
          }});
          h = handAt(s, t);
        }});
        POPS.forEach(([id, at]) => $(id).setAttribute("opacity", ease(clamp((t - at) / 0.2))));
        ["L", "R"].forEach((side) => {{
          const el = $("hand" + side), show = h !== null && h.side === side;
          el.setAttribute("visibility", show ? "visible" : "hidden");
          if (show) el.setAttribute("transform", "translate(" + h.x.toFixed(1) + " " + h.y.toFixed(1) + ") scale(" + (side === "L" ? -{HS} : {HS}) + " {HS}) translate({-TIP[0]} {-TIP[1]})");
        }});
        CAPS.forEach((c, i) => {{
          const on = t >= c.from && (i === CAPS.length - 1 || t < CAPS[i + 1].from);
          const el = $("c" + i);
          el.style.visibility = on ? "visible" : "hidden";
          el.querySelectorAll(".k").forEach((s, j) => {{ s.style.opacity = t >= c.words[j] ? 1 : 0.3; }});
        }});
      }}
      // a setter, not onUpdate: it also runs when the renderer seeks with events switched off
      const clock = {{ v: 0, get t() {{ return this.v; }}, set t(x) {{ this.v = x; render(x); }} }};
      const tl = gsap.timeline({{ paused: true }});
      tl.to(clock, {{ t: D, duration: D, ease: "none" }}, 0);
      render(0);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(H / "index.html").write_text(page)
print("built: %d boards, %d drawings, %d captions, %.1f s" % (len(boards), n, len(caps), D))
