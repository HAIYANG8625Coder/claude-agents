"""Sync a HyperFrames video's scenes and captions to the voice-over's word timestamps.

Conventions in index.html (see SKILL.md):
  - one scene per script sentence:  <div class="scene" id="sc0">…  (elements that pop in carry class "pop")
  - captions:                       <div class="cap" id="c0">…</div>, in spoken order. If the caption text is
    not what is spoken (digits, "+65", English words), add data-say="加六五" with the spoken form.

Two modes:
  - Generated block (new videos): put the lines `// voice-video:sync:begin` and `// voice-video:sync:end`
    inside the <script>; everything between them is rewritten.
  - In place (older videos): existing tl.set/tl.to/tl.fromTo lines for #scN / #cN get new times, and any other
    timeline position is mapped piecewise-linearly from timing.prev.json (written by build_vo.py).
Every data-duration equal to the old root duration becomes the new total.

Usage: python3 -I sync.py <video folder> [--dir .voice-heygen-full-0.92] [--karaoke] [--push]
  --karaoke  captions light up character by character as spoken (needs CSS: .cap .k { opacity:.35 })
  --push     each scene slowly zooms 1 -> 1.04 while it is on screen
  An element with id="progress" gets a bar that fills over the whole video.
  The generated block starts with `const AT = {...}`: each spoken word's start time (lower-case letters and digits;
  repeats as "word.2", "word.3"). Time hand-made tweens below the end marker with AT["fell"] instead of a copied
  number, so they follow a new take. Elements that are gone (e.g. #vbars) lose their lines on the next run.
"""
import html as H, json, os, re, sys

proj = sys.argv[1]
take = os.path.join(proj, sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else json.load(open(os.path.join(proj, "timing.json"))).get("take_dir", ".voice-heygen-full"))
tm = json.load(open(os.path.join(proj, "timing.json")))
wf = os.path.join(take, "words.aligned.json")  # written by build_vo.py: starts snapped to the real pauses
words = [w for w in json.load(open(wf if os.path.exists(wf) else os.path.join(take, "words.json"))) if re.search(r"\w", w["text"])]
U = lambda s: [c.lower() for c in s if c.isalnum()]  # compare letter by letter: "M O E" = "MOE", "Claude Code" = "ClaudeCode"
p = os.path.join(proj, "index.html"); h = open(p).read()
starts = [l["start"] for l in tm["lines"]]
sent_end_idx, n = [], 0
for l in tm["lines"]:
    n += len(U(l["text"])); sent_end_idx.append(n)

# ---- captions: match each caption's spoken units to the word stream
# match on tokens, not HeyGen words: "Claude Code" may come back as one word or two
toks = [{"t": x, "start_time": w["start_time"], "end_time": w["end_time"]} for w in words for x in U(w["text"])]
caps = []
for m in re.finditer(r'<div class="cap" id="c(\d+)"([^>]*)>(.*?)</div>', h):
    say = re.search(r'data-say="([^"]*)"', m.group(2))
    spoken = H.unescape(say.group(1) if say else re.sub(r"<[^>]+>", "", m.group(3)))
    caps.append((int(m.group(1)), spoken))
k, ct = 0, []
for cid, spoken in caps:
    u = U(spoken); seg = toks[k:k + len(u)]
    got = [w["t"] for w in seg]
    if got != u:
        sys.exit("caption c%d %r does not match the voice (heard %r). Add data-say=\"<spoken form>\" to it." %
                 (cid, spoken, "".join(w["t"] for w in seg)))
    sent = next(i for i, e in enumerate(sent_end_idx) if k < e)
    ct.append([cid, seg[0]["start_time"], seg[-1]["end_time"], sent, [w["start_time"] for w in seg], bool(say)]); k += len(u)
if caps and k != len(toks):
    sys.exit("captions cover %d of %d spoken words: a caption is missing or the take differs from script.json" % (k, len(toks)))
for i, c in enumerate(ct):  # on 50 ms early; inside a sentence hand straight over, at a sentence end linger 0.25 s
    nxt = ct[i + 1] if i + 1 < len(ct) else None
    on = max(0.0, c[1] - 0.05)
    off = nxt[1] - 0.05 if nxt and nxt[3] == c[3] else min(c[2] + 0.25, nxt[1] - 0.05 if nxt else tm["total"])
    c[1], c[2] = round(on, 3), round(off, 3)

# ---- scenes: scN on screen from sentence N's start until sentence N+1 starts
scenes = sorted(int(x) for x in re.findall(r'class="scene[^"]*" id="sc(\d+)"', h))
if scenes and len(scenes) != len(starts):
    print("note: %d scenes for %d sentences; scenes past the last sentence are left alone" % (len(scenes), len(starts)))
show = lambda i: 0.0 if i == 0 else starts[i]
has_pop = lambda i: re.search(r'id="sc%d">(?:(?!class="scene).)*?class="[^"]*\bpop\b' % i, h, re.S) is not None

old_root = re.search(r'id="root"[^>]*data-duration="([\d.]+)"', h).group(1)
B, E = "// voice-video:sync:begin", "// voice-video:sync:end"
if B in h and E in h:
    L = []
    for i in [s for s in scenes if s < len(starts)]:
        L.append('tl.set("#sc%d", { visibility: "visible", opacity: 1 }, %.3f);' % (i, show(i)))
        if has_pop(i):
            L.append('tl.fromTo("#sc%d .pop", { opacity: 0, y: 40, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "power2.out", stagger: 0.28 }, %.3f);' % (i, show(i) + 0.04))
        if i + 1 < len(starts):
            L.append('tl.to("#sc%d", { opacity: 0, duration: 0.2, ease: "power2.in" }, %.3f);' % (i, starts[i + 1] - 0.2))
            L.append('tl.set("#sc%d", { visibility: "hidden" }, %.3f);' % (i, starts[i + 1]))
        if "--push" in sys.argv:  # slow zoom while a scene is up: keeps a still card from feeling frozen
            end = starts[i + 1] if i + 1 < len(starts) else tm["total"]
            L.append('tl.fromTo("#sc%d", { scale: 1 }, { scale: 1.04, duration: %.3f, ease: "none" }, %.3f);' % (i, end - show(i), show(i)))
    for cid, on, off, _, _, _ in ct:
        L.append('tl.set("#c%d", { visibility: "visible" }, %.3f);' % (cid, on))
        L.append('tl.set("#c%d", { visibility: "hidden" }, %.3f);' % (cid, off))
    if "--karaoke" in sys.argv:  # each character lights up as it is spoken (captions with data-say just show whole)
        def wrap(cid, inner):
            n = [0]
            def chars(text):
                out = ""
                for ch in text:
                    if ch.isalnum():
                        out += '<span class="k" id="c%dk%d">%s</span>' % (cid, n[0], ch); n[0] += 1
                    else:
                        out += ch
                return out
            return "".join(p if p.startswith("<") else chars(p) for p in re.split(r"(<[^>]+>)", inner))
        for cid, on, off, _, times, has_say in ct:
            if has_say: continue
            m = re.search(r'(<div class="cap" id="c%d"[^>]*>)(.*?)(</div>)' % cid, h)
            if 'class="k"' not in m.group(2):
                h = h[:m.start(2)] + wrap(cid, m.group(2)) + h[m.end(2):]
            for j, t in enumerate(times):
                L.append('tl.to("#c%dk%d", { opacity: 1, duration: 0.08 }, %.3f);' % (cid, j, max(on, t - 0.03)))
    if 'id="vbars"' in h:  # a "live" voice meter: bars jump on every spoken character, rest in the pauses
        HS = [0.55, 0.9, 0.4, 1.0, 0.65, 0.3, 0.8, 0.5, 0.95]
        for n, w in enumerate(toks):
            L.append('tl.to("#vbars i", { scaleY: (j) => [%s][(j * 4 + %d) %% 9], duration: 0.09 }, %.3f);' % (",".join(map(str, HS)), n, w["start_time"]))
            nxt = toks[n + 1]["start_time"] if n + 1 < len(toks) else None
            if nxt is None or nxt - w["end_time"] > 0.18:
                L.append('tl.to("#vbars i", { scaleY: 0.12, duration: 0.15 }, %.3f);' % w["end_time"])
    if 'id="tc"' in h:  # running timecode in the HUD
        L.append('tl.to({ t: 0 }, { t: %.3f, duration: %.3f, ease: "none", onUpdate: function () { const s = this.targets()[0].t; '
                 'document.getElementById("tc").textContent = [Math.floor(s / 60), Math.floor(s %% 60), Math.floor((s %% 1) * 30)].map(v => String(v).padStart(2, "0")).join(":"); } }, 0);'
                 % (tm["total"], tm["total"]))
    # word anchors for hand-made tweens outside the block: AT["fell"], AT["nvidia.2"] (2nd time the word is said)
    seen, at = {}, {}
    for w in words:
        key = "".join(U(w["text"]))
        if not key: continue
        seen[key] = seen.get(key, 0) + 1
        at[key if seen[key] == 1 else "%s.%d" % (key, seen[key])] = round(w["start_time"], 3)
    L.insert(0, "const AT = %s;" % json.dumps(at, separators=(",", ":")))
    if 'id="progress"' in h:  # a thin bar that fills over the whole video
        L.append('tl.fromTo("#progress", { scaleX: 0 }, { scaleX: 1, duration: %.3f, ease: "none" }, 0);' % tm["total"])
    ind = re.search(r"\n([ \t]*)" + re.escape(B), h).group(1)
    h = re.sub(re.escape(B) + r".*?" + re.escape(E), lambda _: B + "\n" + "".join(ind + x + "\n" for x in L) + ind + E, h, flags=re.S)
    mode = "generated block"
else:
    prev = os.path.join(proj, "timing.prev.json")
    if os.path.exists(prev):  # move every other tween with the speech first
        old = json.load(open(prev)); a = [(0.0, 0.0)]
        for o, nw in zip(old["lines"], tm["lines"]): a += [(o["start"], nw["start"]), (o["end"], nw["end"])]
        a.append((old["total"], tm["total"]))
        def mp(t):
            for (x0, y0), (x1, y1) in zip(a, a[1:]):
                if t <= x1: return y0 if x1 == x0 else y0 + (t - x0) * (y1 - y0) / (x1 - x0)
            return t - old["total"] + tm["total"]
        h = re.sub(r"(tl\.(?:set|to|from|fromTo)\(.*?,\s*)(\d+(?:\.\d+)?)(\);)", lambda g: "%s%.3f%s" % (g.group(1), mp(float(g.group(2))), g.group(3)), h)
    def put(pattern, t):
        global h
        h, c = re.subn(pattern, lambda g: g.group(1) + "%.3f" % t, h)
        return c
    for i in [s for s in scenes if s < len(starts)]:
        put(r'(tl\.set\("#sc%d", \{ visibility: "visible", opacity: 1 \}, )[\d.]+' % i, show(i))
        put(r'(tl\.fromTo\("#sc%d \.pop", .*?\}, )[\d.]+(?=\);)' % i, show(i) + 0.04)
        if i + 1 < len(starts):
            put(r'(tl\.to\("#sc%d", \{ opacity: 0, duration: 0\.2, ease: "power2\.in" \}, )[\d.]+' % i, starts[i + 1] - 0.2)
            put(r'(tl\.set\("#sc%d", \{ visibility: "hidden" \}, )[\d.]+' % i, starts[i + 1])
    for cid, on, off, *_ in ct:
        if not (put(r'(tl\.set\("#c%d", \{ visibility: "visible" \}, )[\d.]+' % cid, on) and
                put(r'(tl\.set\("#c%d", \{ visibility: "hidden" \}, )[\d.]+' % cid, off)):
            sys.exit("no tl.set lines for #c%d: add the sync markers (see SKILL.md) so they are generated" % cid)
    mode = "in place"

h = h.replace('data-duration="%s"' % old_root, 'data-duration="%s"' % tm["total"])
open(p, "w").write(h)
print("%s: %d scenes, %d captions synced; duration %s -> %s s" % (mode, len(scenes), len(ct), old_root, tm["total"]))
