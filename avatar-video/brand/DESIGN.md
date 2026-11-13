# Michael's video brand

The video version of `.claude/skills/x-image/templates/brand.css`, so videos, X images and Xiaohongshu cards look like one account. Change colors there first, then copy them here.

**What stays the same in every video (the signature):** Michael's cloned voice, the three dots (indigo, teal, amber) + "Michael · learning AI agents in public" on the end card, Inter / JetBrains Mono type, and a question at the end. **Everything else comes from a style preset** (below), picked to fit the topic. Don't copy the last video's look: on 2026-11-13 Michael noticed his first two X videos looked the same (both copied the dark HUD), and the fix was these presets.

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

## Style presets (pick one per video, in the storyboard)
Pick the preset that fits the topic and write it at the top of `STORYBOARD.md` (`Style: A · market news`). Don't use the same preset twice in a row on one platform unless Michael asks. The colors and layout below replace the dark tokens above. Only the signature stays.

| | Preset | Use for | Look | Motion | Worked example |
|---|---|---|---|---|---|
| **A** | **Market news** | stocks, earnings, economy, current events | Light paper `#f3efe6` with fine grain, ink `#111`, down `#d62828`, up `#0a8a4a`, highlighter `#ffd23f`. Serif masthead strip ("Market Notes · date · ticker chip"), a black ticker tape below the caption band, full-width charts and bars, a news-clipping card (paraphrased, labeled as such, never a real outlet's logo or headline) with a rubber stamp ("ALLEGED"), calendar tiles for dates | Hard cuts (`sync.py --cut`), snappy pops, bars and lines that grow on the spoken word, a stamp slam, a ticker scrolling the whole video | `videos/2026-11-13-nvda-huang-market/` |
| **B** | **Screen tutorial** | how-to, tools, Claude Code / HeyGen walkthroughs | A real screen recording or screenshots Michael provides, in a rounded window on `--bg`. Zoom-ins on the click, a cursor highlight, the step number as a big corner badge | Zoom/pan on the recording (camera moves), a cut on each step | `videos/2026-11-12-how-i-make/` (v2, HUD look; replace drawn cards with real recordings next time) |
| **C** | **Bold type** | opinions, hot takes, lists, "3 mistakes" | One huge word or number per beat filling ~70% of the width. The full-screen background color changes every scene (indigo → teal → amber → ink) with text in ink or paper | Hard cuts on every beat, scale punches, a word that slams in on its spoken word, no cards | (none yet) |
| **D** | **Talking head** | personal stories, announcements, anything where trust matters | Michael's HeyGen avatar full frame (the dark tokens above), B-roll with the circle inset | Punch-in, pop-in card, circle inset (the three effects in "The edit" above) | (needs the paid avatar) |

The old dark HUD look (`videos/2026-11-11-sg-p1/`, `2026-11-12-how-i-make/`) is fine for Xiaohongshu tutorials, but on X it reads as dark-on-dark and every video looks alike.

**Rules for every preset** (from the 2026-11-13 review):
- Fill the frame: the main element (number, chart, word) takes 60–70% of the width. No small card floating in an empty stage.
- Something changes every 1–2 s (a bar grows, a stamp lands, a line draws, a cut), timed on the spoken word with `AT["word"]`.
- At least 2 real or real-looking visuals per video (Michael's screenshots or recordings, real price data drawn as a chart, a paraphrased news clipping). Never fake a real outlet's page or logo.
- Captions carry the words; the stage carries the data. Don't put the caption sentence on the card too.
- On X, aim for 30–35 s.
