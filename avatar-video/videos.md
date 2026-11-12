# Avatar videos

Every video made with `/avatar-video`. The scripter reads this to avoid repeats; the last line of each entry says what to improve next time.

## 2026-11-11 — 新加坡小一｜外国人报名5步 (approved by Michael, not posted yet)
Platform: xhs · Length: 52.8 s · Folder: videos/2026-11-11-sg-p1 · Source: Michael's own note of the same name
Voice: macOS Tingting (no avatar yet, HeyGen not signed in) · Script: reviewer's fixed Script 2 (mistake-first hook, +86 → +65)
What to improve next time: listen for how Tingting reads "M O E / I O I / P D F"; add soft music once signed in to HeyGen.

### 2026-11-12 — re-voiced in Michael's cloned voice (v2, waiting for his review)
Voice: HeyGen instant clone `michael-voice-clone-2min` (made by Michael in the HeyGen web app from voice-samples/michael-voice-clone-2min.mp3), model heygen-voice-1-turbo-free (free). Generated per sentence via the HeyGen MCP in the Claude Code CLI (the desktop app's HeyGen sign-in fails with "Invalid redirect URI"). Joined with tools/heygen-voice.py; scene/caption times remapped from the Tingting timing. Length 48.4 s. Render: renders/2026-11-11-sg-p1_2026-11-12_09-49-09.mp4. Tingting v1 kept in tingting-v1/.

### 2026-11-12 — v3: one-take voice (waiting for Michael's review)
Michael's v2 feedback: "lagging during this video and end of this video, sounds incoherent". Cause: voicing one sentence per call resets the intonation each time and leaves uneven holes (extra 0.4–0.6 s pauses inside 第三步 and 完整清单 plus the added gaps, so the ending stumbled).
Fix: the whole script in ONE HeyGen create_speech call (same clone, free model), sentence times from HeyGen's per-word timestamps (tools/heygen-whole.py), scenes moved with tools/retime.py, captions timed from the word timestamps, scene fades end exactly when the next scene starts. Length 45.6 s. Render: renders/2026-11-11-sg-p1_2026-11-12_21-14-18.mp4. v2 kept in heygen-v2/.
Lesson: always voice the whole script in one take; never stitch sentence-by-sentence TTS.

### 2026-11-12 — v4: same take, 8% slower (APPROVED by Michael: "not bad")
Michael asked to slow down a little. HeyGen ignores `speed` for instant clones (it returned the same 45.2 s take), so the v3 take was stretched to 92% tempo with ffmpeg atempo, pitch kept (tools/slow-take.py), then heygen-whole.py --dir .voice-heygen-full-0.92, retime.py, captions from the scaled word times. Length 49.5 s. Render: renders/2026-11-11-sg-p1_2026-11-12_21-26-14.mp4. v3 kept in heygen-v3/.

### 2026-11-12 — v4.1: captions on the sound (approved v4 + timing fix)
Same voice as v4 (0.92). Captions and scene changes now snap to where the voice actually restarts after a pause (HeyGen's word starts run ~0.15–0.2 s early), via the new voice-video skill (build_vo.py + sync.py). Length 49.5 s. Render: renders/2026-11-11-sg-p1_2026-11-12_21-48-09.mp4. v4 kept in heygen-v4/. Michael asked for this update; waiting for his listen.

## 2026-11-12 — 我怎么做这条视频（克隆声音，免费版）
Platform: xhs · Length: 45.4 s · Folder: videos/2026-11-12-how-i-make · Made with the voice-video skill (one take, 0.92)
Script: Script 1 (reviewer-fixed) with Michael's change: step 1 = "在安静的房间，录两分钟自己的声音" (not the old-video route, since most viewers don't have one).
Render: renders/2026-11-12-how-i-make_2026-11-12_22-12-27.mp4 — waiting for Michael's review.
What to improve next time: the take script used to strip all spaces, so HeyGen read "ClaudeCode"; fixed (only spaced single letters are joined). Matching is now letter by letter.

### 2026-11-12 — 我怎么做这条视频 v2: made more attractive after studying 数字人小米 on Xiaohongshu
Their top tutorial (不会剪辑也能出片, 675 likes / 1571 saves / 169 comments) uses a HUD "studio" frame, a LIVE face picture-in-picture, flow diagrams, real proof visuals, keyword-highlighted captions and a save / comment-keyword call to action. Applied (same voice, same script): HUD frame + timecode + progress bar, a LIVE voice meter that moves with the speech (our face stand-in), karaoke captions, slow zoom per scene, a flow diagram (整篇稿子 → 一次录完 → 慢 8%), the real stitched-vs-one-take waveforms on the 坑 / fix scenes, a "先收藏 · 下次照着做" chip, a quiet music bed and 7 sound effects. v1 kept in v1/. Render: renders/2026-11-12-how-i-make_2026-11-12_22-22-57.mp4 — APPROVED by Michael.
