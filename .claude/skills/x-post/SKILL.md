---
name: x-post
description: Draft, review and (after Michael approves) publish a post on his X account, optionally with an image. Use when Michael asks to post on X, tweet something, or runs /x-post <topic> [with image | no image].
---

# X assistant

Flow: **draft → review → Michael approves → post → log.** Never skip the approval step.

Both agents use `x-assistant/playbook.md` (what works on X, learned by `/x-research`). If its "Research log" shows no live research yet or nothing in the last 2 weeks, mention once that running `/x-research` would make drafts sharper.

## 1. Get the topic
Use the text after `/x-post` as the topic. If there is none, ask Michael what he wants to post about and stop. If the topic is off his theme (AI agents, Claude Code, AI video) or only about his own setup, say so in one line and suggest a reader-benefit angle (see the playbook's "Reach for a new account"), then follow his choice.

**Image option.** If the text ends with "with image" / "with picture" / "with pic" (any wording like that), remove it from the topic and set **image mode = on**. If it ends with "no image", image mode = off and don't offer one. Otherwise image mode = ask (offer once in step 4). This applies to exact wording too: a trailing "no image" / "with image" is the option, not part of the post.

**Video option.** If Michael names a video to attach, or `/avatar-video` hands one over, set **media = video** with that MP4's path: no image is offered, and the post goes out with the video (step 5). Find the video's folder (`avatar-video/videos/<folder>/`). Its `script.json` is what the video says, and its `RESEARCH.md`, if there is one, holds the facts. Pass both to the drafter and the reviewer.

**News and market topics.** Every number must come from a source file (RESEARCH.md, or data pulled by code). A price is called a "close" only after that market has closed; otherwise label it with its time ("midday Nov 12"). Stock or crypto topics always say "Not financial advice", spelled out, and never give buy or sell calls.

If Michael gives **exact wording** ("post exactly this: ..."), skip step 2 and send that text straight to the reviewer as the only draft, telling it this is Michael's own wording, so it should flag only real mistakes. His words stay as they are: if the reviewer marks it FIX, show the fix as a suggestion next to his text and let him choose. Only a real mistake (typo, grammar, private info) is worth raising; skip style nitpicks on text he wrote himself.

## 2. Draft
Run the `x-drafter` agent with the topic and any facts Michael gave. If image mode = on, tell it an image will be attached, so a draft can lean on the image (e.g. "here's what I learned 👇" with a list card). If it says the topic is too thin, ask Michael for the missing details and stop.

## 3. Review
Run the `x-reviewer` agent, passing it all drafts verbatim. Then:
- Use the **fixed version** for any draft marked FIX.
- Drop drafts marked REJECT (mention why in one line).
- With media = video, the reviewer also checks that every number in the post matches what the video says (`script.json`) and what it shows. On 2026-11-13 the reviewer rounded −11.6% to "about 12%", while the video said "11 percent". When the two disagree, use the video's number, or drop the number from the post. Pointers like 👇 or "link below" point at nothing when the media is attached, so cut them.
- **Always** invoke the `humanizer` skill (the Skill tool, embedded mode, final text only) over each remaining draft, so it reads like Michael and not a chatbot. This step was skipped on 2026-11-13. The next step counts the humanizer's output, so a draft that skipped it has nothing to count and can't be shown. Watch most for its strongest tells: "not X but Y" contrasts, one-line closers, "Here's the thing" openers, forced triads, dashes (none in the final post), stock AI words (delve, crucial, robust, testament) and bold or labelled lists. Keep every fact, number, @handle, link and hashtag exactly; X posts may keep a short emoji marker or line breaks if the draft had them. Skip this for Michael's own exact wording.
- Count each remaining draft exactly with Bash, e.g. `python3 -c 'import sys;print(len(sys.argv[1]))' "<text>"`. Drop any over 280.
- If nothing is left, run the drafter once more with the reviewer's feedback, review again. If it still fails, tell Michael and stop.

## 4. Ask Michael
**If image mode = on:** before asking, make the image for the reviewer's ⭐ pick by following the `x-image` skill (pick the template, build, render, check it yourself). If the draft names a count ("3 things…"), the image shows exactly that many items. Send the PNG once with SendUserFile (x-image doesn't send it when called from here). This way Michael approves text and image in one go. Say in one line which other draft the image also fits, if any.

Show the surviving drafts, numbered, each with its character count, the reviewer's pick marked ⭐, and any issues the reviewer fixed. Ask which one to post (or edits); with a single draft, just ask "Post this?". **Stop and wait.** Only post after Michael clearly picks a draft or says to post specific text. "Looks good" without saying which counts only if there's one draft.

If he asks for edits, apply them, recount, show the final text once more and wait for a clear yes.

Image handling by mode:
- **on**: if he picks a different draft than ⭐ and the image no longer fits it, re-make the image for his pick and show it before posting. He can say "no image" to post text only.
- **ask**: offer an image in one line (e.g. "Want an image? A list card would fit this."). If yes, follow `x-image`, show the PNG, and post only after he approves both.
- **off**: don't mention images.

## 5. Post via Chrome
Load the Claude in Chrome tools in one ToolSearch call (tabs_context_mcp, navigate, computer, browser_batch). If Chrome isn't connected, tell Michael and give him the final text to post himself.

1. `tabs_context_mcp` with `createIfEmpty: true`, then navigate to `https://x.com/compose/post`.
2. Screenshot. If it shows a login page, stop and ask Michael to sign in.
3. If there's an approved image: `find` the composer's hidden file-input and upload the PNG with `file_upload` (never click the media button; it opens a native file picker).
   If media = video: upload the MP4 the same way (into the hidden file input of the **compose dialog**, the first match; never click the media button). `file_upload` takes at most 10 MB per call. If the MP4 is bigger, first make a smaller copy in the scratchpad with ffmpeg from `avatar-video/node_modules/@ffmpeg-installer/darwin-arm64/ffmpeg` (`-c:v libx264 -crf 26 -preset slow -c:a aac -b:a 128k -movflags +faststart`), check it, and upload that.
   Click the "What's happening?" box and type the approved text **exactly** (use the Enter key for blank lines). Screenshot and check the composer shows exactly that text, plus the image or video preview if any.
   For a video, wait until the preview shows its first frame and the **Post** button is enabled before you click it (check again after about 10 s for a long video). The ring next to the "+" is the character counter, not an upload spinner.
4. Click **Post**, wait 3 seconds, screenshot. Success = the "Your post was sent" notice. If you don't see it, say so; don't claim success and don't post again without asking (avoids a duplicate).
5. Close any "Got it" popup only if it blocks reading the result.

## 6. Log
Append to `x-assistant/posts.md`:

```
## YYYY-MM-DD
<exact posted text>
(with video: <path to the MP4>)   ← only when a video was attached; with an image, its path the same way
```

Then tell Michael in one or two lines: posted (or not), and the exact text.
