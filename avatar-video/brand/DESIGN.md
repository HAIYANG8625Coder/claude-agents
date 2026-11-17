# Michael's video brand

The video version of `.claude/skills/x-image/templates/brand.css`, so videos, X images and Xiaohongshu cards look like one account. Change colors there first, then copy them here.

**What stays the same in every video (the signature):** Michael's cloned voice, the three dots (indigo, teal, amber) + "Michael · learning AI agents in public" on the end card, Inter / JetBrains Mono type, and a question at the end. **Everything else comes from a style preset** (below), picked to fit the topic. Don't copy the last video's look: on 2026-11-13 Michael noticed his first two X videos looked the same (both copied the dark HUD), and the fix was these presets.

## Format
- **1080×1920, 30 fps, vertical.** Works on Xiaohongshu and X. (Landscape only if Michael asks, or for a long deep-dive in preset H: 1920×1080, 4–8 min.)
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

## Vertical or landscape (decide before the script)
Decide the frame first, because it decides the skill, the length and which presets fit. Write it in the storyboard or outline next to the style (`9:16` or `16:9`).

1. **Michael said it** ("横屏", "landscape", "vertical", "竖屏", "Short") → do that. Nothing below overrides him.
2. **Landscape 16:9** (`article-explainer`, preset H) when **any** of these is true:
   - the video walks through one source: an article, 1–3 papers, docs, or an episode of a series built on one source;
   - it runs over ~3 min (4–8 min is the target);
   - viewers need to read things on screen: the source's figures, tables, code, or diagrams with many boxes (chart-draw diagrams are 16:9 too).
3. **Vertical 9:16** (`avatar-video` / `voice-video`, presets A–G) when the video is:
   - one idea, a hook in 3 s, made for scrolling on a phone (Xiaohongshu feed, X, YouTube Shorts);
   - 3 min or less (X: 30–35 s; news: 45–60 s; default 30–45 s);
   - a talking head (preset D) or a reaction to news.
   A tutorial made of cards (preset G) can stay vertical up to ~6 min if every frame still reads on a phone (e.g. `videos/2026-11-17-sg-work-passes/`, 5:19).
4. **Platform:**
   - X → vertical, unless Michael asks;
   - YouTube → a vertical video of 3 min or less becomes a Short; a long video should be landscape;
   - Xiaohongshu takes both.
5. **Still unclear** (e.g. a 3–5 min tutorial that isn't a read of one source) → ask once and give a pick: "Vertical (phone-first, preset G) or landscape (deep-dive, preset H)? I'd pick X because …". Don't make both versions unless he asks: the Agent ep 1 vertical version was made and never posted (2026-11-17).

Log the frame in `videos.md` (`· 9:16 ·` or `· 16:9 ·`).

## Style presets (pick one per video, in the storyboard)
Pick the preset that fits the topic and write it at the top of `STORYBOARD.md` (`Style: A · market news`). Don't use the same preset twice in a row on one platform unless Michael asks. The colors and layout below replace the dark tokens above. Only the signature stays.

| | Preset | Use for | Look | Motion | Worked example |
|---|---|---|---|---|---|
| **A** | **Market news** | stocks, earnings, economy, current events | Light paper `#f3efe6` with fine grain, ink `#111`, down `#d62828`, up `#0a8a4a`, highlighter `#ffd23f`. Serif masthead strip ("Market Notes · date · ticker chip"), a black ticker tape below the caption band, full-width charts and bars, a news-clipping card (paraphrased, labeled as such, never a real outlet's logo or headline) with a rubber stamp ("ALLEGED"), calendar tiles for dates | Hard cuts (`sync.py --cut`), snappy pops, bars and lines that grow on the spoken word, a stamp slam, a ticker scrolling the whole video | `videos/2026-11-13-nvda-huang-market/` |
| **B** | **Screen tutorial** | how-to, tools, Claude Code / HeyGen walkthroughs | A real screen recording or screenshots Michael provides, in a rounded window on `--bg`. Zoom-ins on the click, a cursor highlight, the step number as a big corner badge | Zoom/pan on the recording (camera moves), a cut on each step | `videos/2026-11-12-how-i-make/` (v2, HUD look; replace drawn cards with real recordings next time) |
| **C** | **Bold type** | opinions, hot takes, lists, "3 mistakes" | One huge word or number per beat filling ~70% of the width. The full-screen background color changes every scene (indigo → teal → amber → ink) with text in ink or paper | Hard cuts on every beat, scale punches, a word that slams in on its spoken word, no cards | (none yet) |
| **D** | **Talking head** | personal stories, announcements, anything where trust matters | Michael's HeyGen avatar full frame (the dark tokens above), B-roll with the circle inset | Punch-in, pop-in card, circle inset (the three effects in "The edit" above) | (needs the paid avatar) |
| **E** | **Sticky-note whiteboard** | teaching a concept, reading notes, explainers | White board `#f6f7f9` with a dot grid, ink `#17181c`, sticky notes (yellow `#ffe066`, pink `#ffa8cb`, blue `#9bd8ff`, green `#a6eba0`, orange `#ffc078`) tilted 1–3°, taped white paper for quotes and lists, red marker circles for step numbers, Marker Felt for the key English word, a pen tray below the caption band | Soft pops, notes landing with a small tilt, marker rings and circles drawn on the spoken word (SVG `pathLength="1"` + `strokeDashoffset`) | `videos/2026-11-14-harness-sticky/` |
| **F** | **Anime story** | comparing things as characters or "schools", stories, anything that needs a cast | Full-frame AI anime illustrations (Buzzy, Nano Banana 2, 9:16, 2K) with **no text inside the picture**; every word is added in HyperFrames. One color per character for a vertical dojo-sign name banner (teal `#12b3a6`, amber `#f59f00`, indigo `#5c6ef5`, pink `#f0679e`), paper chips with a thick ink border and hard shadow, red warning tags, white captions with a 12 px ink outline over a soft scrim, a footer line saying the pictures are AI-generated | A slow camera push on every picture (GSAP scale with a `transformOrigin` on the subject), manga speed lines + a banner slam when a character enters, hard cuts (`sync.py --cut --push --karaoke`), stamps and strike-throughs on the spoken word | `videos/2026-11-14-harness-anime/` |
| **H** | **Article deep-dive (长视频精读), 16:9** | a 4–8 min read of ONE article or 1–3 papers, made with the `article-explainer` skill (the only landscape preset) | Cream slide deck `#fcf0e4`, ink `#211e1c`, crimson `#9b1b3f` (section tags, "now"), blue `#1f5aa6` (the "before" bar), serif (Songti SC) for big numbers and captions. A **chapter bar** on top, a crimson **section tag**, the source's own figure or English paragraph on a white card **next to** a rebuilt Chinese diagram, a grey **source line on every slide** (`原文 … 图 2 · 第 11 页`, `示意` when inferred), a pale caption band. Frame 0 is a green **cover card** (series tag, date badge, two-line title, chapter pills). Ends on a 合起来 recap table and a 留个问题 card. Rules: `brand/EXPLAINER-PLAYBOOK.md` | Calm: soft fades, boxes and arrows appear on their spoken word, bars grow, a red box lands on the one changed value. No `--push`, no `--cut` | `template-explainer/` |
| **G** | **App-UI tutorial (一图看懂)** | teaching how something works: AI concepts, agent architecture, "N parts of X", any tutorial that should end in a saved cheat sheet | Light iOS-style UI on `#f2f2f7` with a soft colour glow, white cards (36 px radius, soft shadow), one colour per chapter (blue `#0a84ff`, orange `#ff9f0a`, purple `#af52de`, pink-red `#ff375f`, green `#30d158`). A **chapter bar** at the top (one pill per part: grey = not yet, filled = now, white with colour = done) so viewers always know where they are. Every idea is shown as a **mock app screen** (mail list, alarm, file tree, permission dialog, notification banners) with a `01 / 05` badge. A real screenshot of the source in a browser window. Ends on a **一图看懂 cheat-sheet card** with every part in one frame plus "收藏这张图" | Rows slide in, iOS spring pops (`back.out`), buttons light up on their spoken word, a tapping cursor, notifications dropping from the top, soft fades with `sync.py --karaoke --push` | `videos/2026-11-15-always-on-agents/` |

The old dark HUD look (`videos/2026-11-11-sg-p1/`, `2026-11-12-how-i-make/`) is fine for Xiaohongshu tutorials, but on X it reads as dark-on-dark and every video looks alike.

Why G exists (2026-11-15): Michael asked for a style just for tutorials after E, B and the dark HUD started to look alike. Research on short-form tutorials (Xiaohongshu 干货 notes, micro-tutorials on X/TikTok, "X in 100 seconds" explainers) agreed on: one skill per video, a 3-second hook, a visible structure (numbered parts / chapters), something changing every 3–5 s, and an ending worth saving (saves are the strongest signal for tutorials). G builds all of those into the layout. Leave the screen tutorial (B) for real recordings.

**Rules for every preset** (from the 2026-11-13 review):
- Fill the frame: the main element (number, chart, word) takes 60–70% of the width. No small card floating in an empty stage.
- Something changes every 1–2 s (a bar grows, a stamp lands, a line draws, a cut), timed on the spoken word with `AT["word"]`.
- At least 2 real or real-looking visuals per video (Michael's screenshots or recordings, real price data drawn as a chart, a paraphrased news clipping). Never fake a real outlet's page or logo.
- Captions carry the words; the stage carries the data. Don't put the caption sentence on the card too.
- Chinese fonts need an `@font-face { font-family:"PingFang SC"; src: local("PingFang SC"); }` (same for Songti SC), or `check` fails with font_family_without_font_face (2026-11-13).
- Overlapping headline-card collages (preset A, 小Lin style): keep ~135 px between card tops and rotations under 2°, or the cards cover each other's headlines. Chip rows need `white-space:nowrap`.
- On X, aim for 30–35 s.
