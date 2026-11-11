---
name: xhs-post
description: Write, design and (after the user approves) publish a Chinese image-and-text note (图文笔记) on their Xiaohongshu / rednote account, with swipeable 3:4 cards. Use when the user runs /xhs-post <topic>, or asks to post on Xiaohongshu / 小红书 / rednote.
---

# Xiaohongshu post

Flow: **gather facts → write Chinese note → make cards → user approves → publish in Chrome → log.** Never publish without a clear yes.

This was first done by hand on 2026-11-11 for the note "Telegram遥控Claude踩坑记". If `x-assistant/xhs-telegram-post.md` and the `x-assistant/images/xhs-tg-*` cards exist, they are the worked example, so look at them before you write.

## 0. Before first use (one-time setup)
Before the first run, check each item below. If one is missing, tell the user exactly what to do and stop. Don't start writing until the setup is complete.

**Computer and tools**
- A Mac with **Google Chrome** installed at `/Applications/Google Chrome.app`. It renders the cards in headless mode and runs the publish step.
- **Python 3** (`python3 --version`). If it's missing, run `xcode-select --install`, which also installs git.
- The **x-image** skill must be installed next to this one (`.claude/skills/x-image/`). This skill uses its `render.sh` and `templates/brand.css`. Copy both skill folders together, keeping the same layout.
- Run Claude Code from the folder that contains `.claude/skills/`, so both skills load. Create `x-assistant/images/` there if it doesn't exist (`mkdir -p x-assistant/images`).

**Claude in Chrome (so Claude can use the browser)**
1. In Chrome, install the **Claude in Chrome** extension (https://chromewebstore.google.com/detail/fcoeoabgfenejglbffodgkkbkcdhcgfn), pin it, and sign in with the same Claude account you use for Claude Code.
2. Connect it to Claude Code: start Claude Code with `claude --chrome`, or run `/chrome` inside a session and turn it on.
3. Check it: Claude should be able to call `tabs_context_mcp` and list the open tabs. If the Chrome tools are missing, the extension isn't connected, so reconnect with `/chrome` and keep Chrome open.

**Xiaohongshu account**
1. Have a Xiaohongshu / rednote account (sign up in the phone app if needed).
2. In **that same Chrome profile**, go to https://www.xiaohongshu.com and log in. Scanning the QR code with the phone app is the easiest way.
3. Open https://creator.xiaohongshu.com once by hand, log in there too if it asks, and finish any first-time prompts (agreements or verification). After that, the 发布 page should open without a login screen.
4. Keep Chrome open and the Mac awake while it publishes.

**Make it yours**
- Change the footer signature in every file in `templates/` (the `<div class="foot">` line, currently "Programmer in Singapore · learning AI agents in public") to your own name or tagline.
- Colors and fonts come from `.claude/skills/x-image/templates/brand.css`. Change them there and every card updates.

**Optional**
- To control it from your phone, set up the Telegram channel plugin (`/telegram:configure`), then start Claude Code with `claude --chrome --channels plugin:telegram@claude-plugins-official`.

## 1. Get the topic and the facts
- Use the text after `/xhs-post` as the topic. If there is none, ask and stop.
- If the topic is "how I did X" or "refer to session …", read the real commands, errors and fixes from that session's transcript (`~/.claude/projects/<project>/<session-id>.jsonl`). Pull out user and assistant text plus tool calls with a small Python script run with `python3 -I`. Don't use f-strings with backslashes inside them, because that's a syntax error on this Python.
- Everything in the note must be true and come from the session or from the user. No invented numbers. Never include tokens, keys, pairing codes, emails or any other secret, even ones that are already revoked.

## 2. Write the note (Chinese)
Save it to `x-assistant/xhs-<slug>-post.md` with `# 标题` and `# 正文` sections.
- **Title: 20 characters max.** Make it concrete and a little personal, e.g. "Telegram遥控Claude踩坑记".
- **Body: 1,000 characters max.** The editor's counter includes the topic tags you add later, so aim for about **950** before tags. Count with Bash: `python3 -I -c "import sys;print(len(sys.argv[1]))" "<body>"`.
- Structure that worked: a one-line personal hook (who I am + why) ending in 👇, then 🧰 准备 (what you need), then numbered steps ①②③ with the exact commands, each pitfall as `⚠️坑N：problem → fix`, and a closing question that invites comments (你们还踩过什么坑？评论区聊聊～).
- Plain text only: no Markdown. Leave a blank line between sections. Emoji are fine as section markers, but not in every line.
- If the draft is too long, cut filler phrases first (折腾了好几天, 最关键) and the weakest tag. Never cut a command or a fix.
- Pick 3–5 topics (话题), mixing a big one with niche ones, e.g. #ClaudeCode #AI编程 #Telegram #AIAgent.

## 3. Make the cards (3:4, 1080×1440)
Templates live in `templates/` and reuse the x-image brand (`.claude/skills/x-image/templates/brand.css`):

| Template | Card |
|---|---|
| `cover.html` | Cover: big hook title plus a subtitle. This is the thumbnail in the feed, so it must read at a glance. |
| `overview.html` | Numbered list of all steps (the "save this" card). |
| `step.html` | One card per step: kicker, a progress bar (`.prog i.on` marks done steps), title, `.do` actions, `.cmd` code boxes and `.pit` pitfall boxes. |
| `pitfalls.html` | Every pitfall on one card (good as the last card). |

1. Copy each template into `x-assistant/images/xhs-<slug>-<name>.html`. The brand.css link is relative to that folder, so keep it as is. Replace the example content.
2. Render: `bash .claude/skills/x-image/render.sh x-assistant/images/<file>.html` writes a PNG next to it at the size in `<meta name="x-size">`.
3. Check each PNG yourself. To review several at once, build a contact sheet in the scratchpad (an HTML grid of the PNGs at 540×720), screenshot it with headless Chrome and Read it. Fix overflow, empty space at the bottom, and lone words on a line, then re-render.
   - Long commands in `.cmd`: use `overflow-wrap:anywhere` (not `word-break:break-all`) and put `<wbr>` after `@` so they break at sensible points.
   - Chinese font: `-apple-system,"PingFang SC",sans-serif`.
4. Order that worked (9 images max): cover, then overview, then step 1…N, then pitfalls.

## 4. Ask the user
Send the cards to them (SendUserFile, or as `files` in the Telegram reply if they're on Telegram) and show the title, the body and the character counts. Ask "Publish?" and **stop and wait**. If they ask for changes, apply them and show the result again.

## 5. Publish in Chrome (Claude in Chrome)
The user must already be logged in (see "Before first use"). This flow uses the website, not the phone app.
1. `tabs_context_mcp`, then open `https://www.xiaohongshu.com/explore` and click **发布 / Post** in the sidebar. It opens the creator center in a **new tab** (`creator.rednote.com`, or `creator.xiaohongshu.com`), so run `tabs_context_mcp` again and switch to that tab ID. Going straight to the creator URL can land on a login page even when he's logged in. Check the screenshot shows their account name.
2. Click the **上传图文** tab (the default tab is video). Use `find` to locate the **hidden file input**, then call `file_upload` with all the PNG paths in order (absolute paths, under about 20 MB total). Wait about 4 seconds and confirm the screenshot shows all the thumbnails.
3. Title: click the title input (find "title input") and `type` the title.
4. Body: the editor is a `.tiptap.ProseMirror` contenteditable. Typing a long text is slow and breaks newlines, so **paste** it with JavaScript:
   ```js
   const ed = document.querySelector('.tiptap.ProseMirror'); ed.focus();
   const dt = new DataTransfer(); dt.setData('text/plain', body);
   ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
   ```
   Put the body in a JS template literal, and escape any backtick or `${` in it. Then read `ed.innerText.length` and the first and last lines back to confirm it landed.
5. Topics: move the cursor to the end (`ed.focus(); getSelection().selectAllChildren(ed); getSelection().collapseToEnd()`), `type` `#ClaudeCode`, wait 2 seconds, then press **Return** (or click the first suggestion) to turn it into a real topic. Repeat for each tag. Verify that each tag shows up as `#name[话题]#` in the editor text. A tag that is still plain text gets no reach.
6. Scroll down and take a screenshot: check the images, the title, the body counter (≤1000) and the topics. Then click **发布** and take a screenshot. Success shows **发布成功**.

## 6. Log and save
- Append to `x-assistant/posts.md`: date, "(Xiaohongshu)", the title, the post file, the topics and the image list.
- If the folder is a git repo, offer to commit the post file and the cards. Don't commit until they say yes, and check for secrets before you push.

## Pitfalls seen
- The draft went to 1,187 characters and had to be cut to under 1,000, and the topic tags take up some of the budget.
- The first cards had text that didn't fit and empty space at the bottom. Always check the renders before showing them.
- The creator center opens in a new tab, so actions on the old tab ID do nothing.
- After the paste, empty paragraphs between sections are normal. They are the blank lines and don't break the note.
