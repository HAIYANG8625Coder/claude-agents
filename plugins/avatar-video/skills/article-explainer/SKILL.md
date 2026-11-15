---
name: article-explainer
description: Make a 4–8 minute horizontal (16:9) deep-dive video that walks through ONE article or 1–3 papers chapter by chapter in Michael's cloned voice, in the style of Xiaohongshu AI-knowledge creators' "论文精读 / 工程解读" videos - a cream slide deck with a chapter bar, the source's own figures and quotes beside rebuilt Chinese diagrams, a source line on every slide, a caption band, a cover as frame 0, a recap table and a closing question. Use when Michael runs /article-explainer <url or file>, or asks for a 长视频 / 精读 / 拆解 / "explain this article (or paper) in a video", a tutorial video about an article, or a long-form version of a short he already made.
---

# Article explainer (长视频精读, style preset H)

What this makes: a 1920×1080 video, 4–8 min, that reads one source the way a good tutor does: chapter bar on top, the original on screen, a rebuilt Chinese picture beside it, a source reference on every slide, then a recap table and a question. The method was learned from a Xiaohongshu creator's article and paper deep-dives on 2026-11-15. The study notes are in `avatar-video/brand/EXPLAINER-PLAYBOOK.md`; read them before the outline. Starter project: `avatar-video/template-explainer/` (it passes `hyperframes check`; its demo slides use the always-on agents article).

This skill uses the `voice-video` skill's scripts for the voice and the sync (call that folder `$V`: `.claude/skills/voice-video/scripts`) plus its own `takes.py` (`$S`: `.claude/skills/article-explainer/scripts`). Run everything from the repo root with Node on the PATH: `export PATH="$HOME/.local/node/bin:$PATH"`.

Flow: **source → research → outline → Michael approves the outline → script → Michael approves the script → voice (one take per chapter) → slides → sync → check → render → cover + note text → Michael approves → hand to xhs-post → log.** Never post without his yes on the exact video and text.

## 0. Setup
Same as `voice-video` step 0: `AVATAR-MICHAEL.md` with `voice_id` and `pace`, `avatar-video/node_modules` present, the HeyGen MCP signed in in the Claude Code CLI. Say before the takes that you're about to call HeyGen (free turbo model).

## 1. The source
- Input is a URL (an engineering blog post, an arXiv page) or a file. Ask for one if there's none. One video = one source, or 2–3 papers that answer the same question. Nothing else gets in.
- Read all of it, not the abstract. Make `avatar-video/videos/<YYYY-MM-DD>-<slug>/` by copying `avatar-video/template-explainer/` and write `RESEARCH.md`: title, authors, date, URL, then per section its claims and every number **with its location** (section, figure, table, page). This is where the source lines on the slides come from.
- Capture the originals you'll show into `assets/`: the first page (`src-page1.png`), the 3–6 figures that carry the argument (`src-fig2.png`), and short quotes (keep the exact English in `RESEARCH.md`). For a web page, screenshot it with Claude in Chrome (`computer` zoom with `save_to_disk`) or headless Chrome; for a PDF, render the page with the `pdf` skill and crop. Show only figures and short quotes, never whole pages of text you'd be republishing.
- Check every number twice against the source. Compute any derived number (a drop from 48% to 28%, a ratio) with code. If the source has few numbers, say so in the video rather than borrowing numbers from elsewhere.

## 2. Outline (Michael approves)
Write `OUTLINE.md` and show it:
- **Title + cover:** series tag (`论文精读` for papers, `工程解读` for engineering articles) with the running episode number (count earlier ones in `avatar-video/videos.md`), the source date for the date badge, a two-line title, a one-line subtitle that states the surprising point, and one pill per chapter.
- **Opening (ch 0):** the single most surprising number or line, and why the viewer should care. Open on what it means for them, not on a detail they can only understand later (2026-11-15 lesson).
- **Chapters (ch 1…n, 3–6 of them):** one per part of the source, in the source's own order. For each: the original you'll show, the rebuilt picture (boxes and arrows, a mock table, two bars, a code diff with one value boxed), and the one sentence to remember.
- **合起来 (ch n+1):** the recap table, one row per chapter.
- **结尾 (ch n+2):** one question for the comments.
- **Length:** ask if he didn't say; suggest 4–6 min. At pace 0.92 his voice reads about 5.5 Chinese characters a second, so 5 min ≈ 1,600 characters.
**Wait for his yes.**

## 3. Script (Michael approves)
`script.json` is one item per **slide**, each with its chapter: `[{"ch": 0, "say": "…"}, {"ch": 1, "say": "…"}, …]`. A slide's `say` can be several sentences (15–40 s of speech); change the slide when the picture should change, not on every sentence.
- Write for the ear, as in `voice-video` step 1: numbers as Chinese words (百分之四十八), acronyms spaced (`M I T`), English terms kept as English when that's how engineers say them (Agent, worker, token, run).
- Keep the source's terms and say what they mean the first time (`事件收件箱，原文叫 event inbox`).
- Say where a claim comes from at least once per chapter (`论文的表五里`, `文章原话是`), and say when something is your own inference (`这一步是我按文章的规则推演的`).
- No invented numbers, results or experiences. Michael's own opinion goes in one clearly marked line (`我觉得…`), near the end.
Show the script with its length estimate. **Wait for his yes.**

## 4. Voice: one take per chapter
A whole 5-minute script is too long for one HeyGen call, and chapter breaks are natural pauses, so record per chapter and join:
```bash
python3 -I $S/takes.py split avatar-video/videos/<folder>
zsh $V/heygen_take.sh avatar-video/videos/<folder>/parts/ch0     # then ch1, ch2, … one at a time
python3 -I $S/takes.py merge avatar-video/videos/<folder>          # 0.7 s between chapters (--gap)
python3 -I $V/slow_take.py avatar-video/videos/<folder> 0.92
python3 -I $V/build_vo.py avatar-video/videos/<folder> --dir .voice-heygen-full-0.92
```
If one chapter's take fails or sounds wrong, redo only that chapter and merge again. Send `assets/vo.wav` and ask Michael to listen to the opening and one chapter before you build all the slides. A video under ~90 s can use one take (`heygen_take.sh` on the folder itself) and skip `takes.py`.

## 5. Slides
Edit `index.html` from the template. Its conventions:
- one `<div class="scene" id="scN" data-ch="K">` per `script.json` item, in order; `data-ch` lights the chapter bar (grey = not yet, crimson = now, ink = done). Rename the `#chap` tabs to the outline's chapters (`data-ch` 1…n+2; the opening has no tab);
- every content slide has a `.sec` section tag when a chapter starts, and a `.src` source line: `原文：<source> · <section / 图 N / 表 N · 第 N 页>`, `同上 图 2`, plus `<span class="note">示意</span>` on anything you inferred or simplified;
- show the original (`<img class="card" src="assets/src-fig2.png">`, or an `.orig` quote card) next to the rebuilt Chinese picture. The rebuilt side is the bigger one;
- captions in the band, about 8–16 characters each (join clauses shorter than 6 characters with the next one, or `check` reports them as unreadable: `事件来了` alone was on screen 0.7 s in the test), in spoken order (`<div class="cap" id="cN">`), with `data-say` when the caption differs from the spoken form (`每题花费少 78%` → `data-say="每题花费少百分之七十八"`);
- beats inside a slide go below the sync block and are timed on words: `pop("#n1b", at("开会话"))`, `grow("#b3b", at("七十八"))`, `draw("#r1a", at("跑循环"))`. Remove the template's fallback times once there's a take;
- the cover card (`#cover`) is frame 0 and lifts away at the first slide change; replace its text, pills and date. `.who` holds Michael's three dots; swap in his photo only if he gives one;
- add the `<audio id="vo">` line (commented at the bottom of the template) and set every `data-duration` to `timing.json`'s total (`sync.py` does this for values equal to the old root);
- keep slides full: the main picture fills most of the stage. Something should change every 3–6 s (a box, an arrow, a bar, a highlight); a 7-minute deck of still cards loses people.

Then sync (soft fades, no karaoke, no zoom: that's the calm look of this format):
```bash
python3 -I $V/sync.py avatar-video/videos/<folder>
```

## 6. Check and render
```bash
cd avatar-video/videos/<folder> && npx hyperframes check --json > /dev/null 2>&1; cd -    # read the saved report, fix every error
cd avatar-video/videos/<folder> && npx hyperframes snapshot --at <one time per slide> && npx hyperframes render; cd -
python3 -I $V/qa.py avatar-video/videos/<folder>
```
Look at the contact sheet and `renders/qa.png` yourself: the cover readable at frame 0, the chapter bar right on every slide, no source line missing, nothing overlapping, captions matching the words. Expected warnings: `nested_structure_needs_subcomposition`, `font_face_local_only`.
Music is optional for this format (the creator used none); if Michael wants it, a quiet catalog bed at ≈ 0.08 as in `voice-video` step 4.

## 7. Cover image, note text, hand over
- **Cover PNG:** `npx hyperframes snapshot --at 0` and copy the frame to `renders/cover.png` (Xiaohongshu uses the first frame anyway; the PNG is for X or a manual cover).
- **Upload copy:** Xiaohongshu's uploader in Chrome takes up to 10 MB per call. Make a 720p copy: `ffmpeg -i <render> -vf scale=1280:-2 -c:v libx264 -crf 28 -preset slow -c:a aac -b:a 96k -movflags +faststart renders/<slug>-xhs.mp4`, and raise `-crf` until it fits.
- **Note text** (`x-assistant/xhs-<slug>-post.md`), Chinese, in the playbook's shape: date + source + one plain sentence; the surprising point; one bullet per chapter with its rule or number; **几点说明** (what the source does and doesn't show, what is your inference); the question; 6–7 topics. Every number must match `script.json` and `RESEARCH.md`.
- Send the MP4 and the note with SendUserFile and say what to check (the numbers, the terms, the ending). **Wait for his verdict.** On a yes, hand the upload copy and note to `xhs-post` (video note, AI-content declaration on). For X, ask: a 6-minute horizontal video fits X, but the text must be English and under 280 characters (`x-post`).

## 8. Log
Append to `avatar-video/videos.md`: date, title, `Style: H · article deep-dive`, platform, length, folder, source (title + URL), chapters, render path, what to improve next time. When Michael corrects something, fix this file or the playbook, not just the chat.
