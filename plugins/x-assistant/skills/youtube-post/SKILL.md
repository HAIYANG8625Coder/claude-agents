---
name: youtube-post
description: Write the title, description and tags for a finished video and (after Michael approves) upload and publish it on his YouTube channel through YouTube Studio in Chrome, as a long video or a Short. Use when Michael runs /youtube-post <video path or folder>, asks to post / upload / publish a video on YouTube (油管, YT, Shorts), or when /avatar-video or /article-explainer hands a video over for YouTube.
---

# YouTube post

Flow: **find the video and its facts → write title, description, tags → check → Michael approves the text and the visibility → upload in YouTube Studio → fill the form → publish → log.** Nothing is uploaded before his clear yes, and nothing goes public without it.

This skill only publishes. It doesn't make videos (`/avatar-video`, `/voice-video`, `/article-explainer` do) and it doesn't post to X or Xiaohongshu (`/x-post`, `/xhs-post`). It runs on its own, so the same video can go to several platforms, each with its own approval.

## 0. Before first use
- **Claude in Chrome** connected (`claude --chrome` or `/chrome`), and the YouTube channel logged in, in that same Chrome profile. Check: https://studio.youtube.com opens the Channel dashboard with the channel name under "Your channel" (on 2026-11-17: Michael8625_AI), not a sign-in page. If it asks to sign in, stop and ask Michael to sign in himself.
- Custom thumbnails need a phone-verified channel (studio.youtube.com → Settings → Channel → Feature eligibility). Without it, use one of YouTube's auto thumbnails.
- `ffmpeg` on PATH, or the bundled one at `avatar-video/node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg`.

## 1. Find the video and its facts
- Use the path after `/youtube-post`. It can be an MP4 or a video folder (`avatar-video/videos/<folder>/`; take the newest file in `renders/`). If nothing is given, ask and stop.
- Read what the video says: `script.json` (and `RESEARCH.md`, any `EP*-SCRIPT.md` or post file for it, such as `x-assistant/xhs-<slug>-post.md`). Every number in the title and description must match the video. No invented facts.
- Probe it: `ffprobe -v error -show_entries format=duration:stream=width,height -of json <mp4>` (ffprobe sits next to the bundled ffmpeg, or use `ffmpeg -i`). Note the duration, the shape and the size in MB.
- **Short or long video:** vertical (height > width) and 3 minutes or less → it becomes a **Short** on its own; add `#Shorts` at the end of the description. Anything else is a normal video.
- **Language:** write in the language the video speaks (Chinese video → Chinese title and description). If Michael asks for another language or bilingual, do that. For a Chinese video, add one English line at the end of the description so English search finds it, unless he says no.
- **Series:** if the video is an episode (e.g. "从零做Agent第N集"), look in `x-assistant/posts.md` for the earlier episodes' YouTube entries and keep the same title pattern and playlist.

## 2. Write the post
Save it to `x-assistant/yt-<slug>-post.md` with three sections:

```
# Title
<≤100 characters; keyword first; keep the main point inside the first ~60 characters (the rest is cut in search)>
# Description
<first 2 lines = the hook with the keyword (only these show above "…more")>
<what the video covers; for videos over ~3 min, chapters: "00:00 开场" lines, the first at 00:00, at least 3, each ≥10 s apart, times from script.json>
<sources and links the video uses (real URLs only)>
<1–3 hashtags on the last line; #Shorts for a Short>
# Tags
<comma-separated, ≤500 characters in total>
```

- Rules: title ≤ 100 characters, description ≤ 5,000, and no `<` or `>` anywhere in the title or description (YouTube rejects them). Tags ≤ 500 characters including commas.
- Chapters only if the times come from `script.json` or the edit; never guess a time.
- Same honesty rules as the other skills: no secrets, tokens, emails, IDs or children's names; news and market numbers come from a source file; stock or crypto videos say "不构成投资建议 / Not financial advice".
- **Humanizer pass:** invoke the `humanizer` skill (Skill tool, embedded mode) over the title and description, then check its output (not the earlier draft). Keep every fact, number, link and chapter time exactly.
- Check the limits with `python3 -I .claude/skills/youtube-post/scripts/check.py x-assistant/yt-<slug>-post.md`. It prints OK or a problem for each rule, and checks the chapter list. Fix and re-run until all lines say OK.

## 3. Ask Michael
Show the title, the description, the tags, the check output, and the settings you plan to use:
- **Visibility:** Public by default; Unlisted, Private or **Schedule** (date and time, SGT) if he says so. A render finished late at night: offer to schedule it for the next morning instead.
- **Audience:** "No, it's not made for kids" (his videos are for adults).
- **AI use: Yes** for any video with his cloned voice or HeyGen avatar (every `/avatar-video`, `/voice-video` and `/article-explainer` video), since it makes a real person seem to say something he didn't record. No only for his own real recording.
- **Thumbnail:** YouTube's auto pick, unless he gives a cover image (PNG/JPG, 16:9, ≤ 2 MB).
- **Playlist** (series only) and **category** (Science & Technology for AI topics, Education for tutorials, People & Blogs for life in Singapore).

Ask with the visibility in the question, e.g. "Publish this on YouTube now as Public?" **Stop and wait** for a clear yes. If he asks for changes, apply them, run `check.py` again, and show the final text once more.

## 4. Upload in YouTube Studio (Claude in Chrome)
Load the Chrome tools in one ToolSearch call (tabs_context_mcp, tabs_create_mcp, navigate, computer, find, javascript_tool, file_upload, browser_batch).

1. **Size first.** `file_upload` takes at most 10 MB per call. If the MP4 is bigger, make a copy in the scratchpad: `ffmpeg -i in.mp4 -vf "scale=-2:720" -c:v libx264 -crf 26 -preset slow -c:a aac -b:a 128k -movflags +faststart out.mp4` (for a vertical video use `scale=720:-2`). If it is still over 10 MB, raise `-crf` by 2 and try again. Check the copy plays and has the same duration. Name the copy after the slug: YouTube shows the file name as the title until you change it.
2. `tabs_context_mcp`, open a new tab, go to `https://studio.youtube.com`. Screenshot: the Channel dashboard must show the channel name. A sign-in page → stop and ask Michael.
3. Open the upload dialog with the **upload arrow** at the top right of the dashboard (or Create → Upload videos). Don't click "Select files" (it opens a native picker). The dialog (`ytcp-uploads-dialog`) holds a hidden `input[type=file][name=Filedata]` (checked 2026-11-17). `find` it and `file_upload` the MP4's absolute path.
4. The Details page opens while the video uploads. Fill it in this order, screenshot after each block:
   - **Title:** the title box (`#title-textarea #textbox`, a contenteditable) is prefilled with the file name. Click it, select all (cmd+a), and `type` the title.
   - **Description:** click the description box (`#description-textarea #textbox`) and paste it with JavaScript, because typing breaks newlines:
     ```js
     const ed = document.querySelector('#description-textarea #textbox'); ed.focus();
     const dt = new DataTransfer(); dt.setData('text/plain', desc);
     ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
     ```
     Put `desc` in a template literal and escape backticks and `${`. Read back `ed.innerText` and compare its first and last lines (and length) with the file. If the paste did nothing, fall back to `type` with shift+Return for line breaks.
   - **Thumbnail:** only if Michael gave one: `find` the thumbnail file input and `file_upload` it. Otherwise leave YouTube's choice.
   - **Playlist:** series only; open "Select playlists", tick the series playlist, click **Done** (the agent series is in **从0到1构建一个AGENT**, 2026-11-17). Create a playlist only if Michael said so.
   - **Audience:** click **"No, it's not made for kids"**. The form won't go on without it. On 2026-11-17 a click by `ref` didn't select it; click it by coordinate from a screenshot and read the checked radios back with JS (`tp-yt-paper-radio-button[aria-checked=true]`).
   - **Show more** ("Show advanced settings"): under **AI use** ("Was AI used to generate or edit your content…", called Altered content before) click **Yes** as agreed in step 3. Click the **Tags** box and `type` all tags in one go, comma-separated, ending with a comma so the last one becomes a chip; the counter shows N/500. **Video language**: pick from the list (Chinese (Simplified) for Mandarin). **Category** starts as People & Blogs; change it as agreed. Read the title, checked radios, language, category and tag count back with JS before you click Next.
5. Click **Next** to **Video elements** (leave subtitles, end screen and cards unless Michael asked), **Next** to **Checks**: wait for "No issues found". A copyright claim or any other issue → stop and tell Michael before going on.
6. **Next** to **Visibility:** pick Public / Unlisted / Private as agreed, or **Schedule** and set the date, time and time zone; read the time back from the form, it must match exactly.
7. Wait until the bottom of the dialog says the upload finished ("Upload complete" or "Checks complete"). Screenshot the whole dialog and confirm title, visibility and the video preview once more. Then click the final button (**Publish**, **Save** or **Schedule**).
8. Success = the "Video published" (or "Video scheduled") box with a `youtu.be/…` or `youtube.com/shorts/…` link. Copy the link. If you don't see it, say so; don't upload again without asking (a second upload makes a duplicate video).
9. Close the tab you opened.

If the page looks different from these steps, stop and tell Michael what you see rather than guessing.

## 5. Log
Append to `x-assistant/posts.md`:

```
## YYYY-MM-DD (YouTube) — <title>
Link: <youtu.be link> · <Public / Unlisted / Private / scheduled for …> · <Short or video, duration>
Post file: x-assistant/yt-<slug>-post.md
Video: <path to the uploaded MP4> (<size> MB<, 720p copy of …>)
Settings: not made for kids · AI use <Yes/No> · playlist <name or none> · category <name> · thumbnail <auto / file>
```

Then tell Michael in two lines: published or not, the link, and anything left (e.g. "add an end screen in Studio", "pin a first comment"). Offer to commit the post file; commit only on his yes.

## Pitfalls
- First real run on 2026-11-17 (agent ep2, https://youtu.be/aDAciX3ZtKM): the 9 MB upload and YouTube's checks finished while the Details page was being filled, so Checks already said "No issues found" by the time Next was clicked.
- The title box starts with the file name: always select all before typing, or the title becomes "agent-ep2-upload从零做Agent…".
- `<` and `>` in the description make Studio refuse to save ("Invalid characters"); `check.py` catches them.
- Clicking "Select files" or the thumbnail button opens a macOS file picker the tools can't see. Always use the hidden input with `file_upload`.
- Chapters need the first one at 00:00 and at least 3; otherwise YouTube silently ignores them.
