---
name: voice-video
description: Voice a short vertical HyperFrames video in Michael's own cloned HeyGen voice (no face): one natural take of the whole script, gently slowed, with scenes and captions synced to every spoken word, then render and check. Use whenever Michael wants a video "in my voice" / 用我的声音, wants an existing video folder re-voiced, says the voice-over sounds choppy, laggy, too fast or too slow, or asks to make another video like the Singapore P1 one, even if he doesn't name this skill. Also use from /avatar-video for the voice step and for any no-avatar (voice + graphics) video.
---

# Voice video (Michael's cloned voice + HyperFrames graphics)

What this makes: a 9:16 video where Michael's cloned voice reads an approved script, one scene card per sentence, captions that change exactly on the spoken words. Worked example: `avatar-video/videos/2026-11-11-sg-p1/` (v4, approved 2026-11-12).

Why it works this way (learned the hard way on that video):
- **One take, never sentence by sentence.** Stitching 12 separate TTS clips reset the intonation every sentence and left uneven holes; Michael heard it as "lagging" and "incoherent". One take of the whole script flows like real speech, and HeyGen's per-word timestamps still give exact sentence and caption times.
- **Slow it afterwards.** HeyGen ignores `speed` for instant clones, so a slower read is made by stretching the take (pitch kept). Michael approved **0.92** (8 % slower). Stay between 0.88 and 1.0; slower than 0.88 starts to sound stretched.
- **Times come from the words, not guesses.** Captions and scene changes are placed from the timestamps, so nothing overlaps, and a scene never leaves the stage blank while the next one waits.

Scripts are in this skill's `scripts/` folder (call it `$S`: `.claude/skills/voice-video/scripts`). Run them from the repo root. Put Node on the PATH for every `npx`: `export PATH="$HOME/.local/node/bin:$PATH"`.

## Using this skill yourself (not Michael)
1. Clone https://github.com/HAIYANG8625Coder/claude-agents and run `npm install` in its `avatar-video/` folder (installs HyperFrames, ffmpeg and ffprobe). Needs Node.js 22+ and the Claude Code CLI.
2. Clone your own voice by hand in the HeyGen web app (https://app.heygen.com/avatar/voices → instant clone, free plan) from 1–2 min of clean speech.
3. In a terminal, run `claude`, type `/mcp`, pick heygen and sign in (the repo's `.mcp.json` already lists HeyGen's MCP server).
4. Create `AVATAR-<yourname>.md` at the repo root (git-ignored) with `voice_id: <your voice id>`, `voice_model: heygen-voice-1-turbo-free` and `pace: 0.92`, or set `VOICE_ID` in the environment.
5. Ask Claude Code: "make a video in my voice from avatar-video/videos/<folder>". Wherever this file says Michael, read "you".

## 0. Check the setup (stop and tell Michael what's missing)
- An `AVATAR-*.md` at the repo root (Michael's is `AVATAR-MICHAEL.md`) has `voice_id`, `voice_model` and `pace`, or `VOICE_ID` is set. It is git-ignored; never copy the id into a tracked file.
- `avatar-video/node_modules` exists (it holds ffmpeg/ffprobe and HyperFrames). If not: `npm install` in `avatar-video/`.
- The HeyGen MCP is signed in **in the Claude Code CLI**. The desktop app's own sign-in is broken ("Invalid redirect URI"), so `heygen_take.sh` calls HeyGen through `claude -p`. If the take fails with an auth error, ask Michael to run `claude` in a terminal, type `/mcp`, sign in to heygen, and tell you when it's done.
- The free model costs nothing, but still say before the take that you are about to call HeyGen.

## 1. The video folder
- **Re-voicing an existing video:** first copy the current `timing.json`, `index.html` and `assets/vo.wav` into a backup subfolder named after the version (e.g. `heygen-v4/`), so Michael can go back.
- **New video:** the script must already be approved (the `/avatar-video` steps 1–4 handle topic, script, review and approval). Make `avatar-video/videos/<YYYY-MM-DD>-<slug>/` and build `index.html` from the worked example's structure (keep its styles and layout), then follow the conventions in step 4.
- `script.json` is the list of sentences: `[{"say": "…"}, …]`. Write it for the ear:
  - numbers as Chinese words (加六五, 十月二十号), because the voice reads what it sees;
  - acronyms letter by letter with spaces (`M O E`, `P D F`), so they aren't read as a word;
  - punctuation sets the breathing: `，` short, `。` / `？` a sentence break. Any `pause` fields are ignored in a one-take voice.
  - **English** (worked example `videos/2026-11-13-nvda-huang/`): dates as spoken ordinals ("November sixth", "the twelfth"), percentages as digits ("31 percent" is read fine), "U.S." with periods, and acronyms written as normal (CEO, AMD, AI). The take script joins spaced capitals back together, so "C E O" gains nothing. Captions can show the same words. Use `data-say` only where a caption shows a form the voice doesn't say (a caption reading "Nov 6" over "November sixth").
  - The take's language is detected from `script.json` (Chinese characters → zh, otherwise en). Set `VOICE_LANG` only to override it.

## 2. Record one take
```bash
zsh $S/heygen_take.sh avatar-video/videos/<folder>
```
It sends the whole script in one `create_speech` call and saves `.voice-heygen-full/full.raw` and `words.json`. If the script changes afterwards, record a new take; the next steps refuse a take that doesn't match `script.json` word for word, which stops silent drift between voice and captions.

## 3. Set the pace, build the voice-over
```bash
python3 -I $S/slow_take.py avatar-video/videos/<folder> 0.92
python3 -I $S/build_vo.py avatar-video/videos/<folder> --dir .voice-heygen-full-0.92
```
Use the `pace` from `AVATAR-MICHAEL.md` (0.92 unless Michael asks otherwise). "Slower" → step down 0.04 at a time (0.88 is the floor); "faster" → up to 1.0, which uses the raw take (`--dir .voice-heygen-full`, skip `slow_take`). `build_vo.py` writes `assets/vo.wav` (loudness −16 LUFS, peaks ≤ −1.5 dB, a 0.9 s tail) and `timing.json`, and keeps the old timing as `timing.prev.json`. It also snaps word starts to the real pauses in the audio (`words.aligned.json`): HeyGen's timestamps run ~0.15–0.2 s early after a pause, which would make captions flash up before the word.

## 4. Sync scenes and captions
`index.html` conventions (the sync script relies on them):
- one scene per sentence: `<div class="scene" id="sc0">`, `sc1`, …; elements that pop in get class `pop` (the hook in `sc0` uses `pop0` so it is visible at frame 0);
- captions in spoken order: `<div class="cap" id="c0">…</div>`. When the caption is not what is said (digits, `+65`, `5步`, `10月20号`), add the spoken form exactly as `script.json` says it: `<div class="cap" id="c3" data-say="要写加六五">要写<b>+65</b></div>`. Acronyms need nothing (`MOE` and `M O E` both match). Phone codes are read digit by digit (`+65` → 加六五), other numbers as Chinese numbers (`10月` → 十月);
- new videos: put `// voice-video:sync:begin` and `// voice-video:sync:end` on their own lines in the timeline script, and the scene and caption timeline lines are generated between them. Keep any extra hand-made tweens outside the block. Older videos without the markers are updated in place.

```bash
python3 -I $S/sync.py avatar-video/videos/<folder>
```
Optional extras (use them for Xiaohongshu; they come from studying a top AI-tutorial creator there, 2026-11-12):
- `--karaoke`: caption characters light up as they are spoken (add `.cap .k { opacity:.35 }` to the CSS);
- `--push`: every scene zooms slowly 1 → 1.04, so a still card never looks frozen;
- an element `#progress` gets a bar filling over the video; `#tc` gets a running timecode; `#vbars` (bars as `<i>`) becomes a "LIVE" voice meter that moves only while the voice speaks: our stand-in for the face picture-in-picture other creators use. **Leave the voice-meter box out on X and English videos**: Michael had it removed on 2026-11-13. It's fine for Xiaohongshu if he wants it. If you remove any synced element (#vbars, #tc, #progress, a caption), run `sync.py` again, so its generated lines go too (a stale block gave 573 lint warnings);
- hand-made tweens (a chart bar growing, a line drawing) go below the `// voice-video:sync:end` line and are timed with the word anchors the block defines: `tl.fromTo("#bar", {...}, {...}, AT["fell"])`. Repeated words are `AT["nvidia.2"]`. Never copy a number from the timing: it goes stale with the next take;
- worked example with all of these, a HUD frame, flow-diagram scenes, real waveform proof images and a save call to action: `avatar-video/videos/2026-11-12-how-i-make/` (v2).
- Music and sound: a quiet catalog track (`media-use` audio engine, `bgm.mode: "retrieve"`, free when HyperFrames is signed in) at volume ≈ 0.11 under the voice, plus 5–7 bundled sound effects only at section changes (pop on the hook, whoosh into a new section, glitch on the mistake, sparkle on the fix, ping on the final question). Mix into `assets/mix.wav` with ffmpeg (`aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo` on every input) and point the `<audio>` at it; keep `vo.wav` for the timing. Any new clip element must use the same `data-duration` as the root.

If it stops on a caption that "does not match the voice", that caption needs `data-say`, or a caption is missing. Fix the HTML, not the script, and run it again.

## 5. Render and check
```bash
cd avatar-video/videos/<folder> && npx hyperframes check && npx hyperframes render; cd -
python3 -I $S/qa.py avatar-video/videos/<folder>
```
Read `renders/qa.png` and look at it yourself. What you're checking:
- the length matches the timing;
- the peak is below −1 dB;
- there are no silences over 0.7 s before the last word;
- the frames show no blank stage, captions that match the words, and the end card visible;
- frame 0 (the thumbnail on X and Xiaohongshu) shows the hook clearly, and the end of the first scene shows that `--push`'s slow zoom hasn't pushed big hook text into the top label. On 2026-11-13 a 190 px hook did; 150 px fits.

Fix what's wrong before Michael sees it.

## 6. Hand over
- Send the MP4 with SendUserFile and say in plain words what changed and what to listen for (acronyms, numbers, the ending).
- **Wait for his verdict.** Never post: publishing goes through `xhs-post` / `x-post` after his yes.
- Log the version in `avatar-video/videos.md`: date, what changed and why, length, render path, backup folder. When Michael approves, mark it APPROVED.
- If he corrects the pace or the voice, update `pace` in `AVATAR-MICHAEL.md` so the next video starts there.
