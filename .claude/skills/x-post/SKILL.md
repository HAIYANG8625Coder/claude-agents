---
name: x-post
description: Draft, review and (after Michael approves) publish a post on his X account. Use when Michael asks to post on X, tweet something, or runs /x-post <topic or rough text>.
---

# X assistant

Flow: **draft → review → Michael approves → post → log.** Never skip the approval step.

Both agents use `x-assistant/playbook.md` (what works on X, learned by `/x-research`). If its "Research log" shows no live research yet or nothing in the last 2 weeks, mention once that running `/x-research` would make drafts sharper.

## 1. Get the topic
Use the text after `/x-post` as the topic. If there is none, ask Michael what he wants to post about and stop.

If Michael gives **exact wording** ("post exactly this: ..."), skip step 2 and send that text straight to the reviewer as the only draft.

## 2. Draft
Run the `x-drafter` agent with the topic. If it says the topic is too thin, ask Michael for the missing details and stop.

## 3. Review
Run the `x-reviewer` agent, passing it all drafts verbatim. Then:
- Use the **fixed version** for any draft marked FIX.
- Drop drafts marked REJECT (mention why in one line).
- Count each remaining draft exactly with Bash, e.g. `python3 -c 'import sys;print(len(sys.argv[1]))' "<text>"`. Drop any over 280.
- If nothing is left, run the drafter once more with the reviewer's feedback, review again. If it still fails, tell Michael and stop.

## 4. Ask Michael
Show the surviving drafts, numbered, each with its character count, the reviewer's pick marked ⭐, and any issues the reviewer fixed. Ask which one to post (or edits). **Stop and wait.** Only post after Michael clearly picks a draft or says to post specific text. "Looks good" without saying which counts only if there's one draft.

If he asks for edits, apply them, recount, show the final text once more and wait for a clear yes.

Also offer an image in one line (e.g. "Want an image? A list card would fit this."). If he says yes, follow the `x-image` skill, show him the PNG, and post only after he approves both text and image.

## 5. Post via Chrome
Load the Claude in Chrome tools in one ToolSearch call (tabs_context_mcp, navigate, computer, browser_batch). If Chrome isn't connected, tell Michael and give him the final text to post himself.

1. `tabs_context_mcp` with `createIfEmpty: true`, then navigate to `https://x.com/compose/post`.
2. Screenshot. If it shows a login page, stop and ask Michael to sign in.
3. If there's an approved image: `find` the composer's hidden file-input and upload the PNG with `file_upload` (never click the media button; it opens a native file picker).
   Click the "What's happening?" box and type the approved text **exactly** (use the Enter key for blank lines). Screenshot and check the composer shows exactly that text, plus the image preview if any.
4. Click **Post**, wait 3 seconds, screenshot. Success = the "Your post was sent" notice. If you don't see it, say so; don't claim success and don't post again without asking (avoids a duplicate).
5. Close any "Got it" popup only if it blocks reading the result.

## 6. Log
Append to `x-assistant/posts.md`:

```
## YYYY-MM-DD
<exact posted text>
```

Then tell Michael in one or two lines: posted (or not), and the exact text.
