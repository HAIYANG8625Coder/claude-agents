---
name: xhs-post
description: Write, design and (after the user approves) publish a Chinese image-and-text note (图文笔记) on their Xiaohongshu / rednote account, with swipeable 3:4 cards. Use when the user runs /xhs-post <topic>, or asks to post on Xiaohongshu / 小红书 / rednote.
---

# Xiaohongshu post

Flow: **gather facts → write Chinese note → make cards → review and improve → user approves → publish in Chrome → log.** Never publish without a clear yes.

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
- If the topic points at files ("参考 .claude/agents …"), read those files and take the facts from them. Describe what they actually say: when a claim covers several files ("全是 Markdown"), check every one.
- **News and market topics:** every number comes from a source file (RESEARCH.md, or data pulled by code), and you recompute it yourself before writing; don't estimate a share or a percentage by eye. A price is a 收盘价 only after that market has closed; otherwise label it with the time (11月12日盘中). Stock and crypto notes end with "不构成投资建议" and never say to buy or sell.
- **Video note:** if the user gives a video to post (for example from `/avatar-video`), this is a 视频笔记: skip step 3 (cards) and use the video's first frame as the cover. Every number in the title and body must match what the video says (`script.json` in its folder) and shows.
- Everything in the note must be true and come from the session, the files or the user. No invented numbers. Never include tokens, keys, pairing codes, emails or any other secret, even ones that are already revoked.

## 2. Write the note (Chinese by default)
Read `writing-guide.md` (next to this file) first. It covers what makes a post useful and attractive: topic, search keywords, title, cover, body and closing question. This section covers the format.

Write in Chinese unless the user asks for another language (e.g. "in English", "bilingual"). Their request wins, and covers the title, body and card text. For an English note, keep the keyword people search for (often English already, e.g. "Claude Code"), use English section labels instead of 准备/坑, and still include one Chinese topic such as #AI编程 so Chinese searches find it. English titles are tight at 20 characters, so lead with the keyword and a number; if the user's own word doesn't fit, use a short synonym and say so in the review notes. An English body runs about twice as long as the same Chinese one, so plan for fewer, shorter points from the start.
Save it to `x-assistant/xhs-<slug>-post.md` with `# 标题` and `# 正文` sections. Put the topics on the last line of `# 正文`, as in the worked example.
- **Title: 20 characters max.** Make it concrete and a little personal, e.g. "Telegram遥控Claude踩坑记".
- **Body + topics: 1,000 characters max.** The editor counts the topic tags in the same box and counts each emoji as 2. Check with `python3 -I .claude/skills/xhs-post/scripts/count.py x-assistant/xhs-<slug>-post.md "#tag1 #tag2 ..."`, which counts the way the editor does and prints OK or TOO LONG for both limits. Don't count by eye or with plain `len()`.
- Structure that worked: a one-line personal hook (who I am + why) ending in 👇, then 🧰 准备 (what you need), then numbered steps ①②③ with the exact commands, each pitfall as `⚠️坑N：problem → fix`, and a closing question that invites comments (你们还踩过什么坑？评论区聊聊～).
- That structure fits a "how I set up X" story. For other kinds of posts (lessons, design rules, a checklist), keep the hook, numbered points and closing question, but only call something a 坑 if someone really hit it. Safeguards or rules are 注意 / 💡, not pitfalls. Never invent problems to fill a slot.
- Plain text only: no Markdown. Leave a blank line between sections. Emoji are fine as section markers, but not in every line.
- If the draft is too long, cut filler phrases first (折腾了好几天, 最关键) and the weakest tag. Never cut a command or a fix.
- Pick 3–5 topics (话题), mixing a big one with niche ones, e.g. #ClaudeCode #AI编程 #Telegram #AIAgent.

## 3. Make the cards (3:4, 1080×1440)
Templates live in `templates/` and reuse the x-image brand (`.claude/skills/x-image/templates/brand.css`):

| Template | Card |
|---|---|
| `cover.html` | Cover: big hook title plus a subtitle. This is the thumbnail in the feed, so it must read at a glance. |
| `overview.html` | Numbered list of all steps (the "save this" card). |
| `step.html` | One card per step: kicker, a progress bar (`.prog i.on` marks done steps), title, `.do` actions, `.cmd` code boxes and `.pit` boxes. Write the box label yourself in `.pit .t`: "⚠️ 坑：" for a real problem, "💡 注意：" for a rule or tip. |
| `pitfalls.html` | Every pitfall on one card (good as the last card). Optional: skip it when there are no real pitfalls or it would only repeat the overview. |

1. Copy the cover, overview and (if used) pitfalls templates into `x-assistant/images/xhs-<slug>-<name>.html` and replace the example content. The brand.css link is relative to that folder, so keep it as is there.
   For the step cards, don't copy `step.html` N times. Write the steps into a small JSON file and run `python3 -I .claude/skills/xhs-post/scripts/make_steps.py steps.json x-assistant/images`. It builds every card with the right kicker and progress bar, and handles the light/dark alternation and `roomy`. The format is at the top of the script.
2. Render: `bash .claude/skills/x-image/render.sh x-assistant/images/<file>.html` writes a PNG next to it at the size in `<meta name="x-size">`.
3. Check all PNGs on one contact sheet: `bash .claude/skills/x-image/contact.sh <scratchpad>/sheet.png x-assistant/images/xhs-<slug>-*.png`, then Read the sheet. Look for overflow, big empty space, and lone words or characters on a line. Write down every problem across all cards, fix them all in one pass, re-render everything, and check the sheet again. Aim for 2–3 render rounds in total; card fixes are part of these rounds, not extra. A small leftover (one lone word) is fine to mention in the review notes rather than spending another round on it.
   - **Size text to the content.** The template sizes fit the Telegram example (many lines per card). For a step card with less content (about 4 lines or fewer), add `class="roomy"` to `<body>`: it scales up every part at once. On other cards, make the fonts bigger rather than leaving the card half empty. With more text, cut words before you shrink fonts.
   - Long commands in `.cmd`: they already use `overflow-wrap:anywhere`; put `<wbr>` after `@` and `/` so they break at sensible points. Keep short names like "Claude Code" or "posts.md" together with `&nbsp;` (safer than nowrap spans).
   - Chinese font: `-apple-system,"PingFang SC",sans-serif`.
   - A 2-character Chinese word split across lines (前/后, 清/晰): wrap it in `<span style="white-space:nowrap">` or shorten the line.
4. Order that worked (9 images max): cover, then overview, then step 1…N, then pitfalls.

## 4. Review and improve (before showing the user)
Never show a first draft. Check the note and the cards against `writing-guide.md`, fix what fails, then check again.

1. Score each item **pass / fix**:
   - **Topic:** one line each for who it's for, what problem it solves, and what they take away. If it reads like a diary, change the angle.
   - **Keyword:** the main search phrase (in Chinese, or the English name when that's what people type, e.g. Claude Code) is in the first 10–12 characters of the title, in the first line of the body, on the cover, and matched by a topic.
   - **Title:** 20 characters max, keyword first, a specific promise (number, question or result), matches the content, not clickbait.
   - **Cover:** big text, few words, readable at thumbnail size, repeats the keyword and the promise, clear original image.
   - **Hook:** the first line says who I am and what the reader gets, and carries the keyword. One line can do all three, e.g. "在新加坡写代码，用 Claude Code 搭了个 X 发帖助手👇".
   - **Worth saving:** there is a checklist, steps, real numbers, a template or a summary card. Ask "would someone save this?" If not, add the useful part or cut the post.
   - **Specific and true:** real numbers, dates and steps from the facts gathered in step 1. Nothing invented, nothing vague where a number exists.
   - **Scannable:** short lines, numbered steps or ✅ items, blank lines between sections, emoji as markers only.
   - **Closing question:** a real question the reader can answer from their own life, not just "欢迎评论".
   - **Topics:** 3–5, one big plus niche ones, all relevant.
   - **Sounds human (humanizer pass):** invoke the `humanizer` skill (the Skill tool, not from memory) over the title and body in embedded mode, and run `count.py` on its output, not on the earlier draft, applying its structural patterns to Chinese, since they appear in every language: 不是…而是… contrasts that only add weight (§1), a closing line that repeats the point (§2), 说白了/本质上/真正的问题是 sayings (§3), 话不多说/今天来聊聊/直接上干货 run-ups (§4), forced threes (§6), dashes (——) as the all-purpose connector (§8). Also cut Chinese AI stock words: 赋能, 助力, 打造, 全方位, 深度解析, 值得一提的是, 总而言之, 综上所述, 不得不说, and 首先…其次…最后 used on everything. Keep emoji as section markers and the numbered steps: on Xiaohongshu they are the norm, not decoration (this overrides humanizer §19–20 here). Keep every fact and number exactly.
   - **Privacy and safety:** no names, IDs, addresses, children's faces, tokens or other secrets in the text or images.
   - **Limits:** `scripts/count.py` prints OK for the title (≤20) and body + topics (≤1000); 9 images max.
2. Fix every **fix** item (rewrite the line, re-render the card) and run the checklist again. Stop after 2 checklist rounds (separate from the card render rounds in step 3). If something still fails, say so to the user instead of hiding it.
3. Write 2–3 short review notes for the user: what you changed and why, plus any item that still needs their input (e.g. a missing real number only they know).

## 5. Ask the user
Send the cards to them (SendUserFile, or as `files` in the Telegram reply if they're on Telegram; if neither is available, list the full PNG paths in order) and show the title, the body, the character counts and the review notes from step 4. Ask "Publish?" and **stop and wait**. If they ask for changes, apply them and show the result again.

## 6. Publish in Chrome (Claude in Chrome)
The user must already be logged in (see "Before first use"). This flow uses the website, not the phone app.
1. `tabs_context_mcp`, then open `https://www.xiaohongshu.com/explore` and click **发布 / Post** in the sidebar. It opens the creator center in a **new tab** (`creator.rednote.com`, or `creator.xiaohongshu.com`), so run `tabs_context_mcp` again and switch to that tab ID. Going straight to the creator URL can land on a login page even when he's logged in. Check the screenshot shows their account name.
   **Video note:** stay on the default **上传视频** tab. `find` its hidden file input and `file_upload` the MP4 (up to 10 MB per call; for a bigger file, make a smaller copy with ffmpeg first: `-c:v libx264 -crf 26 -preset slow -c:a aac -b:a 128k -movflags +faststart`). Wait until the upload and processing finish and the cover preview appears; this can take 10–30 s, so screenshot again until it does. Then go on with steps 3–6 (title, body, topics, publish). This path hasn't been run end to end yet: take a screenshot after every step, and if the page differs from these steps, stop and tell the user rather than guessing. Afterwards, update this section with what really happened.
2. For an image note, click the **上传图文** tab (the default tab is video). Use `find` to locate the **hidden file input**, then call `file_upload` with all the PNG paths in order (absolute paths, under about 20 MB total). Wait about 4 seconds and confirm the screenshot shows all the thumbnails.
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

## 7. Log and save
- Append to `x-assistant/posts.md`: date, "(Xiaohongshu)", the title, the post file, the topics and the image list.
- Remind the user to reply to comments in the first 1–2 hours after publishing (see `writing-guide.md` §7).
- If the folder is a git repo, offer to commit the post file and the cards. Don't commit until they say yes, and check for secrets before you push.

## Pitfalls seen
- The draft went to 1,187 characters and had to be cut to under 1,000, and the topic tags take up some of the budget.
- The first cards had text that didn't fit and empty space at the bottom. Always check the renders before showing them.
- The creator center opens in a new tab, so actions on the old tab ID do nothing.
- After the paste, empty paragraphs between sections are normal. They are the blank lines and don't break the note.
