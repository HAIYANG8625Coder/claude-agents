---
name: avatar-video
description: Make a short vertical video where Michael's AI digital twin (HeyGen avatar + his cloned voice) explains a topic, edited with HyperFrames (captions, B-roll, cards), then hand it to xhs-post or x-post. Use when Michael runs /avatar-video <topic> [xhs|x] [NN s], or asks for a 数字人 / digital-twin / avatar / talking-head video of himself.
---

# Avatar video (Michael's digital twin)

Flow: **topic → script → review → Michael approves the script → storyboard → Michael approves the storyboard (this is the cost gate) → voice → Michael approves the voice → avatar A-roll → edit in HyperFrames → preview → Michael approves → render → hand off to publish → log.**

Paid steps are only **voice** (step 6) and **avatar** (step 7). Never run them before the approval in front of them. Same command twice = same HeyGen job, so a retry does not pay twice (see `media-use/references/heygen.md`).

Run every `npx` command with Node 24 on the PATH: `export PATH="$HOME/.local/node/bin:$PATH"` (Node is installed there, not system-wide).

## 0. One-time setup (check every run; stop and tell Michael what's missing)
1. **Node + FFmpeg:** `cd avatar-video/template && npx hyperframes doctor` shows ✓ for FFmpeg, FFprobe and Chrome. If `avatar-video/node_modules` is missing, run `npm install` in `avatar-video/`.
2. **HyperFrames signed in to HeyGen:** `npx hyperframes auth status`. If not signed in, ask Michael to type `! export PATH="$HOME/.local/node/bin:$PATH"; cd avatar-video && npx hyperframes auth login` in the prompt, and wait.
3. **HeyGen MCP** (used by `heygen-avatar`): the `mcp__heygen__*` tools are visible. If not, ask Michael to run `/mcp`, pick **heygen** and sign in, then restart the session.
4. **Pick the mode now:** read `AVATAR-MICHAEL.md` at the repo root. It needs a `voice_id` (his cloned voice). If `avatar_look_id` is empty or "(none yet…)", this run is **no-avatar mode** (voice + graphics, see below). Say so in your first message, plan for no face, and skip the avatar-only checks and steps (punch-in, circle inset, step 7). Run "Make the twin" only when Michael asks for his face.
5. Telemetry stays off: `npx hyperframes telemetry status` says disabled. Don't re-enable it.

### Make the twin (only once)
- Michael records: **a 2–5 min video** (front light, plain background, eyes to camera, natural talking, little head movement) and **1–2 min of clean voice** in a quiet room. Clean audio matters more than any setting for the lips.
- Run the `heygen-avatar` skill for **Michael himself** (a real-person digital twin from his footage, not a prompt-designed character). HeyGen asks for a consent recording; Michael does that step himself.
- Clone his voice in HeyGen (the `heygen-avatar` voice step, or HeyGen's web app). Test one Chinese and one English line before keeping it.
- Save the look id and voice id in `AVATAR-MICHAEL.md` (git-ignored; never put ids, photos or recordings in the public repo).

## 1. Get the request
- Topic = the text after `/avatar-video`. No topic → ask and stop.
- Platform: `xhs` → **Chinese**, `x` → **English** (global rule). Michael's explicit language request wins. Default when not said: ask once.
- Length: `NN s` if given, else 30–45 s. With an avatar, make a **10 s test** before the first full avatar render (test small before paying for the whole thing).
- Facts: from Michael, files he points at, or a session transcript (same rules as `xhs-post` step 1). No invented numbers or experiences.
- **News, market or other current-event topics:** research first and write the facts to `videos/<folder>/RESEARCH.md` (timeline, numbers, sources) before any script. Worked example: `videos/2026-11-13-nvda-huang/RESEARCH.md`. Rules learned on that video:
  - Check the core event in a primary source (company press release, SEC filing, official statement), not only news articles.
  - Pull prices with code (e.g. Yahoo's chart API) and compute every percentage and share with code. "Nearly half" was really 71%.
  - Check whether the market is still open before calling a price a "close" (the chart API's `regularMarketTime` vs `currentTradingPeriod`). If it's still trading, label the price with its time ("Nov 12 midday").
  - Compare against the sector and peers (e.g. SMH, QQQ, rivals) to separate company news from a market-wide move.
  - Hedge allegations ("reported", "alleged"). Stock and crypto videos say "Not financial advice" and give no buy or sell calls.

## 2. Script
Run the `video-scripter` agent with topic, language, target seconds and the facts. If it says the topic is too thin, ask Michael for what's missing and stop.

## 3. Review
Run the `video-reviewer` agent with both scripts verbatim, plus the path to `RESEARCH.md` if there is one (it recomputes every number from it). Use the fixed version for FIX, drop REJECT (one-line reason). Count the real length with Bash (Chinese: characters ÷ 4; English: words ÷ 2.5). If nothing survives, re-run the scripter once with the feedback; if it fails again, tell Michael and stop.

## 4. Michael approves the script
Show the surviving scripts numbered, with seconds, the ⭐ pick and what the reviewer fixed. **Stop and wait** for a clear pick or edits. Apply edits, show the final text once more, wait for yes.

## 5. Storyboard (the cost gate)
Make the video folder: `avatar-video/videos/<YYYY-MM-DD>-<slug>/` by copying `avatar-video/template/` (not `node_modules`). Write `STORYBOARD.md` there: one row per sentence → seconds, what's on screen (face only / punch-in / pop-in card text / B-roll + circle inset), and where each B-roll comes from (Michael's screenshot, drawn in HyperFrames, HeyGen asset search). Follow `avatar-video/brand/DESIGN.md`.
- **Pick a style preset first** (`DESIGN.md` → Style presets: A market news, B screen tutorial, C bold type, D talking head) to fit the topic, and put `Style: <letter> · <name>` on the storyboard's first line. Check `videos.md` for the last video on the same platform and don't repeat its preset unless Michael asks. Build `index.html` from that preset's worked example, not from whatever the last video was.
- List any screenshot or recording **Michael must provide**, and ask for it now.
- Show the storyboard and ask: "Approve? This next step spends HeyGen credits (voice + avatar ≈ <seconds> s)." Use `--plan` on the generate commands for your own estimate, but don't quote prices unless Michael asks. **Stop and wait.**

## No-avatar mode (voice + graphics, free)
Without an avatar (no paid HeyGen plan yet), skip step 7 and run the **`voice-video` skill** for voice, sync, render and checks: Michael's cloned voice in one take at his approved pace (approved 2026-11-12, `videos/2026-11-11-sg-p1/` v4).
Only when Michael asks for "default voice" or his clone is unavailable, use the old free fallback:
- Voice: macOS built-in `say` (Chinese: **Tingting**; English: ask). Put the script in `script.json` (`[{"say": "...", "pause": 0.6}, ...]`, default gap 0.22 s), then `python3 -I avatar-video/tools/say-voice.py <video folder>` writes `assets/vo.wav` + `timing.json` with each sentence's exact start/end. Captions use those times (split by punctuation, timed by character count), so no transcription is needed.
- Kokoro (`npx hyperframes tts`) needs Python ≥ 3.10; this Mac has 3.9, so don't use it.
- One scene per sentence in the middle band (y 300–1040), captions at y ≈ 1150, the hook visible at frame 0. The look comes from the chosen style preset, not from the last video.
- The `content_overlap` warning fires for scenes that are never on screen together: judge from rendered frames (a contact sheet with ffmpeg `tile`), not the warning.

## 6. Voice (paid, small)
Use the `voice-video` skill, steps 2–3 (one HeyGen take of the whole script through the CLI MCP, slowed to his `pace`). Don't use `npx hyperframes media-use generate --type voice`: that bills the separate HyperFrames plan (Free) and refuses his clone. Never voice sentence by sentence: Michael heard the stitched version as laggy and incoherent.
Send `assets/vo.wav` to Michael (SendUserFile) and ask him to listen. Mispronounced word → respell it the way it should sound in the script and regenerate only after he agrees. **Wait for yes.**

## 7. Avatar A-roll (paid, the main cost)
Lip-sync his avatar to the approved audio exactly (no rewriting, no HeyGen graphics; editing happens in HyperFrames):
```bash
npx hyperframes media-use generate --type avatar --avatar <look id> --audio assets/vo.wav --aspect 9:16 --out assets/aroll.mp4
```
Check it with ffprobe (length ≈ voice length, 9:16). Snapshot 3 frames and look: face centred, lips moving, no artefacts. If it's wrong, tell Michael what you saw before paying for another try.

## 8. Edit in HyperFrames
Follow the `/hyperframes` skill (read `references/types/vertical.md`, `captions.md`, `overlays.md`, `motion.md`) and `avatar-video/brand/DESIGN.md`:
- Captions from a free local transcript: English `npx hyperframes transcribe assets/aroll.mp4 -l en --json`; Chinese `npx hyperframes transcribe assets/aroll.mp4 -l zh -m small --json` (the default `small.en` model is English-only). Then correct the transcript against the approved script: the script is the truth for every word.
- Build the storyboard: A-roll full frame, the three brand effects only (punch-in, pop-in card, circle inset), B-roll cut on sentences, signature for the last 2 s, soft ducked music only if over 15 s (`/media-use`, catalog music is free when signed in).
- Search `/hyperframes-registry` before hand-building captions or cards.
- Clamp the root `data-duration` to the A-roll's ffprobe length.
- `npx hyperframes check --json` → fix every error. `npx hyperframes snapshot --review` → look at the frames yourself, fix problems.

## 9. Michael approves the preview
Start `npx hyperframes preview` and tell Michael he can watch it (and edit in the HyperFrames desktop app if he likes). **Wait** for approval or changes. Then render: `npx hyperframes render` → MP4 in the video folder. Send the MP4 with SendUserFile.

## 10. Hand off to publish
Ask where to post, then run that platform's skill with the MP4 as its video: `x-post` (media = video, English under 280) or `xhs-post` (video note, Chinese). Both now upload video. Each still waits for Michael's yes on the exact text before publishing. Give them the video folder, so they can check the post's numbers against `script.json` and `RESEARCH.md`.

## 11. Log
Append to `avatar-video/videos.md`:
```
## YYYY-MM-DD — <title>
Platform: xhs | x · Length: NN s · Folder: videos/<folder>
Script: <final script>
What to improve next time: <one line>
```
If something went wrong or Michael corrected you, fix **this file** (or `DESIGN.md`, or the agents), not just the chat.
