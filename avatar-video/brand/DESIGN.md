# Michael's video brand

The video version of `.claude/skills/x-image/templates/brand.css`, so videos, X images and Xiaohongshu cards look like one account. Change colors there first, then copy them here.

## Format
- **1080×1920, 30 fps, vertical.** Works on Xiaohongshu and X. (Landscape only if Michael asks.)
- Length: 30–45 s by default, never over 60 s for the first videos.
- Safe zone (from HyperFrames `types/vertical.md`): nothing in the top 168 px; all words between y = 168 and y = 1330; below 1330 only texture; nothing under the right-hand action rail.

## Colors and type
| Token | Value | Use |
|---|---|---|
| `--bg` | `#0b0f17` | card and scene backgrounds |
| `--bg-2` | `#121826` | glass card base |
| `--fg` | `#f2f4f8` | main text |
| `--muted` | `#94a3b8` | small labels |
| `--a1` | `#a5b4fc` (indigo) | highlight 1 |
| `--a2` | `#5eead4` (teal) | highlight 2, kicker text, cursor |
| `--a3` | `#fbbf24` (amber) | warnings, "坑" / pitfalls |
| `--grad` | `linear-gradient(90deg, --a1, --a2)` | the highlighted word in a title |

- Sans: `"Inter", "PingFang SC", sans-serif` (Inter is bundled with HyperFrames; PingFang SC covers Chinese). Mono: `"JetBrains Mono"` (bundled) for commands.
- PingFang SC is not bundled, so every composition that uses it declares it (tested 2026-11-11, renders correctly):
  `@font-face { font-family: "PingFang SC"; src: local("PingFang SC"), local("PingFangSC-Regular"); }`
  This gives a `font_face_local_only` warning, which is fine for local renders on this Mac. A cloud render would need a font file in `assets/fonts/` instead.
- Worked example of the look: `videos/0000-toolchain-test/index.html` (local only).
- Signature: the three dots (indigo, teal, amber) + "Michael · learning AI agents in public", shown small for the last 2 s.

## The edit (formula from 数字人小米: A-roll + B-roll + captions + sound)
- **A-roll:** Michael's HeyGen avatar, full frame. The face is never covered by a card (`overlays.md`).
- **B-roll:** cut on the sentence, 1–3 s each. Sources in this order: real screenshots or screen recordings Michael gives → things HyperFrames can draw (code windows, terminal, lists, numbers) → HeyGen asset search. Never invent a product screen.
- **Captions:** burned in, every spoken word, bottom of the safe band (around y = 1100–1330). Max about 8 Chinese characters or 5 English words per line. The key word of each sentence in `--a2`.
- **Three effects only** (keeps the look consistent):
  1. **Punch-in:** zoom the A-roll to ~115% on the key sentence, 0.4 s, `power2.out`.
  2. **Pop-in card:** glass card (`--bg-2` at 78%, blur 22 px, 1.5 px `rgba(255,255,255,.14)` border, 28 px radius) with 3–6 words, in 0.4 s, out 0.35 s.
  3. **Circle inset:** during full-screen B-roll, the avatar shrinks into a 300 px circle bottom-left with a 4 px `--a2` ring, so the face stays on screen.
- **Sound:** the avatar voice is the main track. Soft background music under it (ducked), only if the video is over 15 s.
- **Frame 0** is the thumbnail: Michael's face + the hook line already on screen. Never black, never a logo.

## Script rules
- Spoken words only; one idea per sentence; under ~20 Chinese characters or ~15 English words per sentence.
- Speed budget: ~4 Chinese characters/s, ~2.5 English words/s.
- Hook in the first 3 s; takeaway or question at the end.
- No invented facts. Nothing private.
