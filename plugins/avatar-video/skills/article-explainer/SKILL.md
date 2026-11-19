---
name: article-explainer
description: Make a 4–8 minute horizontal (16:9) deep-dive video that walks through ONE article or 1–3 papers chapter by chapter in Michael's cloned voice, in the style of Xiaohongshu AI-knowledge creators' "论文精读 / 工程解读" videos - a cream slide deck with a chapter bar, the source's own figures and quotes beside rebuilt Chinese diagrams, a source line on every slide, a caption band, a cover as frame 0, a recap table and a closing question. Use when Michael runs /article-explainer <url or file>, or asks for a 长视频 / 精读 / 拆解 / "explain this article (or paper) in a video", a tutorial video about an article, or a long-form version of a short he already made.
---

# Article explainer (长视频精读, style preset H)

What this makes: a 1920×1080 video, 4–8 min, that reads one source the way a good tutor does: chapter bar on top, the original on screen, a rebuilt Chinese picture beside it, a source reference on every slide, then a recap table and a question. The method was learned from a Xiaohongshu creator's article and paper deep-dives on 2026-11-15. The study notes are in `avatar-video/brand/EXPLAINER-PLAYBOOK.md`; read them before the outline. Starter project: `avatar-video/template-explainer/` (it passes `hyperframes check`; its demo slides use the always-on agents article).

This skill uses the `voice-video` skill's scripts for the voice and the sync (call that folder `$V`: `.claude/skills/voice-video/scripts`) plus its own `takes.py` (`$S`: `.claude/skills/article-explainer/scripts`). Run everything from the repo root with Node on the PATH: `export PATH="$HOME/.local/node/bin:$PATH"`.

Flow: **source → research → (real test, if any) → outline → Michael approves the outline → script → reviewer → SLIDES FROM THE SCRIPT with estimated timing → Michael approves SCRIPT + CARDS together → voice (one take per chapter) → re-sync to the real voice → check → ROUGH CUT (voice + post texts) → Michael approves → render → hand to xhs-post / youtube-post → log.** The voice is never generated before Michael has approved both the script and the cards (his rule, 2026-11-19, after ep 8: a late slide cost a HeyGen re-take). Never post without his yes on the exact video and text.

**Status messages (2026-11-19, ep 7: Michael had to ask for them):** Michael only sees Telegram. Send one short message at the start of every step above and after every long wait (a HeyGen take, a render, a copyright check), saying what you're doing and what comes next. Say before every HeyGen call. Never go more than a few minutes silent.

**Commit as you go:** after each approval (outline, script, voice, rough cut, post) commit the new files (`series/EP*-*.md`, the post texts, the code for the episode) and push to main. Video folders are git-ignored on purpose; never stage keys, `AVATAR-*.md` or personal files.

## 0. Setup
Same as `voice-video` step 0: `AVATAR-MICHAEL.md` with `voice_id` and `pace`, `avatar-video/node_modules` present, the HeyGen MCP signed in in the Claude Code CLI. Say before the takes that you're about to call HeyGen (free turbo model).

## 1. The source
- Check the frame against `avatar-video/brand/DESIGN.md` → "Vertical or landscape". If Michael wants a short (3 min or less, one idea, made for phones), this is the wrong skill: use `/avatar-video`.
- Input is a URL (an engineering blog post, an arXiv page) or a file. Ask for one if there's none. One video = one source, or 2–3 papers that answer the same question. Nothing else gets in.
- If the episode is about our own code (the agent series), commit and push that code to its repo at each milestone (first working version, each bug fix) and say so in `RESEARCH.md`; a before/after code slide needs the real old version, and ep 6's was lost because nothing was committed.
- Read all of it, not the abstract. Make `avatar-video/videos/<YYYY-MM-DD>-<slug>/` by copying `avatar-video/template-explainer/` and write `RESEARCH.md`: title, authors, date, URL, then per section its claims and every number **with its location** (section, figure, table, page). This is where the source lines on the slides come from.
- Capture the originals you'll show into `assets/`: the first page (`src-page1.png`), the 3–6 figures that carry the argument (`src-fig2.png`), and short quotes (keep the exact English in `RESEARCH.md`). For a web page, screenshot it with Claude in Chrome (`computer` zoom with `save_to_disk`) or headless Chrome; for a PDF, render the page with the `pdf` skill and crop. Show only figures and short quotes, never whole pages of text you'd be republishing.
- **Our own real test (agent series):** run it BEFORE the outline, from code, and write every number to `facts.json` with one command that regenerates it from the raw run files (`demo/*.json`). If the episode's code changes afterwards (a bug fix, a changed limit), re-run the test and regenerate `facts.json` before the script is final; a fix that was not re-tested must be said so in the video (ep 7: the compaction fix and the 60→100 turn cap were never tested apart).
- Check every number twice against the source. Compute any derived number (a drop from 48% to 28%, a ratio) with code. If the source has few numbers, say so in the video rather than borrowing numbers from elsewhere.

## 2. Outline (Michael approves)
Write `OUTLINE.md` and show it:
- **Title + cover:** series tag (`论文精读` for papers, `工程解读` for engineering articles) with the running episode number (count earlier ones in `avatar-video/videos.md`), the source date for the date badge, a two-line title, a one-line subtitle that states the surprising point, and one pill per chapter.
- **Opening (ch 0):** the single most surprising number or line, and why the viewer should care. Open on what it means for them, not on a detail they can only understand later (2026-11-15 lesson).
- **Chapters (ch 1…n, 3–6 of them):** one per part of the source, in the source's own order. For each: the original you'll show, the rebuilt picture (boxes and arrows, a mock table, two bars, a code diff with one value boxed), and the one sentence to remember.
- **Teach the basics first (2026-11-19 lesson, ep 6 of the agent series):** assume the viewer has never heard the term. Before any chapter that walks through the source's or the docs' version of a feature, add 1–3 short chapters that answer, in plain words and one everyday picture each: **what is it** (one sentence + an analogy: a blueprint, a shopping list), **why does it exist / what goes wrong without it**, and **how does it help** (and what it does not do). Draw one concept diagram per question. Put these before the docs and the code, not after. Ep 6 v1 skipped this and Michael said the audience "doesn't even know what it is".
- **Introduce a test before its results (same lesson):** a results slide needs three earlier slides: what was tested (the setup, shown as a diagram), the task and how a point is scored, and the setups being compared plus each measure in plain words (what a "turn" is). Only then show the numbers.
- **Beginner gate (run before you show the outline):** list the 3–6 key terms of the episode. For each, write its one-sentence meaning, why it exists, and where in the outline a chapter explains it. A term with no chapter, or explained only after it is used, means the outline fails: add the chapter first. Then ask: could someone who has never used this follow chapter 1 and 2 without pausing?
- **合起来 (ch n+1):** the recap table, one row per chapter.
- **结尾 (ch n+2):** one question for the comments.
- **Length:** ask if he didn't say; suggest 4–6 min. At pace 0.92 his voice reads about 5.5 Chinese characters a second, so 5 min ≈ 1,600 characters.
**Wait for his yes.**

## 3. Script (reviewer first; Michael approves it together with the cards in 3b)
`script.json` is one item per **slide**, each with its chapter: `[{"ch": 0, "say": "…"}, {"ch": 1, "say": "…"}, …]`. A slide's `say` can be several sentences (15–40 s of speech); change the slide when the picture should change, not on every sentence.
- Write for the ear, as in `voice-video` step 1: numbers as Chinese words (百分之四十八), acronyms spaced (`M I T`), English terms kept as English when that's how engineers say them (Agent, worker, token, run).
- Keep the source's terms and say what they mean the first time (`事件收件箱，原文叫 event inbox`).
- Say where a claim comes from at least once per chapter (`论文的表五里`, `文章原话是`), and say when something is your own inference (`这一步是我按文章的规则推演的`).
- No invented numbers, results or experiences. Michael's own opinion goes in one clearly marked line (`我觉得…`), near the end.
- Keep "token" as the English word (spoken and written); never translate it to 词元 (Michael, 2026-11-19: sounds unnatural). Grep the script, diagrams and post texts for 词元 before the take.
- Spoken text: never read a tool or file name aloud (`submit_plan`, `todo_write`, `CLAUDE.md` are misread). Say what it does (提交计划的工具); keep the name on screen. Keep each spoken clause short (about 20 characters).
- Check the script against the question "could someone who has never used this feature follow it?" before showing it to Michael.
- **facts.json:** if the video reports numbers from our own runs or data, write `avatar-video/videos/<folder>/facts.json` first (`{"facts": [{"v": "59", "what": "...", "src": "file or computation"}, ...]}`), computed by code from the raw data, then run `python3 -I $S/check_facts.py avatar-video/videos/<folder> <folder>/script.json x-assistant/xhs-<slug>-post.md x-assistant/yt-<slug>-post.md`. It lists every number in those texts that is not in facts.json; fix the text or the file until it is clean. Give the reviewer the facts.json too.
Run the `video-reviewer` agent on `script.json` + `facts.json` + the outline, apply every must-fix, then go to 3b. Do not ask for the script alone: he approves the script and the cards in one message.

## 3b. Cards from the script, before any voice (Michael approves script + cards)
The slides do not need the voice, only times. Make estimated times so they can be built, synced and photographed first:
```bash
python3 -I $S/preview_timing.py avatar-video/videos/<folder>     # fake words + timing.json ("preview": true), about 7% longer than the real voice
```
Then do what step 5 says (diagrams, `build.py`, `sync.py`, `npm run check`, snapshots at `end - 0.4` of every scene). Send Michael on Telegram, in this order and in as few messages as possible: the full script text (by chapter, numbered like the slides), the contact sheets of ALL slides with the slide number on each, and the list of numbers with their source (`facts.json`). Say plainly: "nothing is recorded yet; say ok or give slide or sentence numbers to change". Changes to the script or a slide cost nothing now: edit `script.json` / `build.py`, run `preview_timing.py` again, rebuild, resync, send only the changed slides. **Wait for his yes on both.** Only then HeyGen (say before the call).

## 4. Voice: one take per chapter (only after the 3b approval)
A whole 5-minute script is too long for one HeyGen call, and chapter breaks are natural pauses, so record per chapter and join:
```bash
python3 -I $S/takes.py split avatar-video/videos/<folder>
zsh $V/heygen_take.sh avatar-video/videos/<folder>/parts/ch0     # then ch1, ch2, … one at a time
python3 -I $S/takes.py merge avatar-video/videos/<folder>          # 0.7 s between chapters (--gap)
python3 -I $V/slow_take.py avatar-video/videos/<folder> 0.92
python3 -I $V/build_vo.py avatar-video/videos/<folder> --dir .voice-heygen-full-0.92
```
If one chapter's take fails or sounds wrong, redo only that chapter and merge again. `build_vo.py` overwrites the preview `timing.json` with real times (and drops the `preview` flag): re-run `build.py` and `sync.py`, then `npm run check`; the slides are already approved, so only look at any slide whose beats moved. If one chapter's script changes later, re-record only that chapter. A video under ~90 s can use one take (`heygen_take.sh` on the folder itself) and skip `takes.py`.

## 5. Slides (built in step 3b from the preview timing, rebuilt after the real voice)
Edit `index.html` from the template. Its conventions:
- one `<div class="scene" id="scN" data-ch="K">` per `script.json` item, in order; `data-ch` lights the chapter bar (grey = not yet, crimson = now, ink = done). Rename the `#chap` tabs to the outline's chapters (`data-ch` 1…n+2; the opening has no tab);
- every content slide has a `.sec` section tag when a chapter starts, and a `.src` source line: `原文：<source> · <section / 图 N / 表 N · 第 N 页>`, `同上 图 2`, plus `<span class="note">示意</span>` on anything you inferred or simplified;
- show the original (`<img class="card" src="assets/src-fig2.png">`, or an `.orig` quote card) next to the rebuilt Chinese picture. The rebuilt side is the bigger one;
- captions in the band, about 8–16 characters each (join clauses shorter than 6 characters with the next one, or `check` reports them as unreadable: `事件来了` alone was on screen 0.7 s in the test), in spoken order (`<div class="cap" id="cN">`), with `data-say` when the caption differs from the spoken form (`每题花费少 78%` → `data-say="每题花费少百分之七十八"`);
- beats inside a slide go below the sync block and are timed on words: `pop("#n1b", at("开会话"))`, `grow("#b3b", at("七十八"))`, `draw("#r1a", at("跑循环"))`. Remove the template's fallback times once there's a take;
- the cover card (`#cover`) is frame 0 and lifts away at the first slide change; replace its text, pills and date. `.who` holds Michael's three dots; swap in his photo only if he gives one;
- add the `<audio id="vo">` line (commented at the bottom of the template) and set every `data-duration` to `timing.json`'s total (`sync.py` does this for values equal to the old root);
- draw the diagrams with `diagrams.py` and finish it with `save_all(STAGES, OUT)` from `avatar-video/template-explainer/stages.py`: it saves every stage and fails on any box or text outside the frame, before you render a single frame;
- start from `avatar-video/template-explainer/components.py` (`Deck`: scene, cards, diagram, chip, codecmp, recap, and since ep 7 `codeex` for real code lines, `rcards`, `msgcard`, `seqscene` for a chart that grows row by row). Import it; do not copy helper functions into `build.py` (ep 7 did, and re-fixed ep 6's layout bugs) and keep to its SAFE AREA: content ends at about y=680 and nothing goes below 740, because the source line and the caption band sit under it (ep 6 chips collided with both);
- keep slides full: the main picture fills most of the stage. Something should change every 3–6 s (a box, an arrow, a bar, a highlight); a 7-minute deck of still cards loses people.

Then sync (soft fades, no karaoke, no zoom: that's the calm look of this format):
```bash
python3 -I $V/sync.py avatar-video/videos/<folder>
```

## 5b. Rough cut: real voice + post texts (Michael approves before the final render)
The script and the cards were approved in 3b. After the real voice is synced and `npx hyperframes check` passes: write the XHS and YouTube post texts (`xhs-<slug>-post.md`, `yt-<slug>-post.md`), run the humanizer skill over them, then `count.py`, `check.py` and `check_facts.py`. Send Michael `assets/vo.wav` (say what to listen for), both texts with their check output, any slide that changed since 3b, and the planned platforms and visibility. **Wait for his verdict.** One "ok" then covers voice and texts: render, upload copy, and post only to the platforms he names. (Chapter times for the YouTube text come from the real `timing.json`, never the preview.)

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
- Send the MP4 with the texts (already approved in 5b) and ask once: post to XHS, YouTube, or both, public now or a slot? **Wait for his yes.** Then post, one status message per platform. Known quirks (ep 7, 2026-11-19), so you don't rediscover them:
  - XHS: #AI编程 has failed to link every time it was the third topic: after the five tags read the editor text back, and for a plain `#AI编程` delete its 5 characters, retype it, wait 3 s, press Return, wait 3 s more and read again. XHS: use the creator URL `creator.rednote.com/publish/publish?from=menu&target=video` after the Post click opens the creator tab; paste the body with JS; type each topic then press Return, and read the editor text back: a topic missing `[话题]` is plain text (#AI编程 needed a delete and retype); 内容类型声明 → 笔记含AI合成内容 is at the bottom under 内容设置; the first-frame cover stays (no recommended cover appears); the campaign auto-link toast is harmless; 发布成功 page = done.
  - YouTube: dashboard upload arrow → `file_upload` on the hidden input; title box prefilled with the file name (select all first); description by JS paste; playlist 从0到1构建一个AGENT; "No, not made for kids" is a click by coordinate; AI use Yes sits under Show more; tags typed with a trailing comma; language list does not filter by typing (find the item with JS, click by coordinate); category usually stays Science & Technology; the copyright check takes about 2 minutes ("No issues found") before Publish is safe.
  - Hand to `xhs-post` (video note, AI-content declaration on) / `youtube-post` for anything else. For X, ask: a 6-minute horizontal video fits X, but the text must be English and under 280 characters (`x-post`).

## 8. Log
Append to `avatar-video/videos.md`: date, title, `Style: H · article deep-dive`, platform, length, folder, source (title + URL), chapters, render path, what to improve next time. When Michael corrects something, fix this file or the playbook, not just the chat.
