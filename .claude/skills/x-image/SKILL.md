---
name: x-image
description: Make an on-brand image for one of Michael's X posts (hook card, list/cheat sheet, code window, before→after, big number). Use when Michael runs /x-image, asks for a picture/image for a post, or when /x-post offers an image.
---

# X image

Makes clean, consistent post images from HTML templates rendered by headless Chrome. Free, no accounts. Every image shares one brand (`templates/brand.css`) and the same footer signature, so people start recognizing Michael's posts in the feed.

The templates follow the image styles that perform best in AI/dev X: quote cards, "save this" cheat sheets, Carbon/ray.so-style code windows, before→after splits, and big-number stat cards.

## 1. Know the post
Use the post text (from `/x-post` or what Michael gives). If there's no post yet, ask for the post text, or the topic plus the real facts or numbers to show (the image can't use anything invented), then stop.

## 2. Pick a template
| Template | Use when the post is… | Size |
|---|---|---|
| `hook.html` | a question, opinion, "let's connect", one strong line | 1600×900 |
| `list.html` | tips, steps, lessons, "N things…" (most bookmarked) | 1200×1500 portrait |
| `code.html` | code, a prompt, config, terminal output, a workflow as pseudo-code | 1600×900 |
| `compare.html` | before vs after, old vs new, myth vs reality | 1600×900 |
| `stat.html` | one real number: a result, milestone, benchmark, "Day N" | 1600×900 |

Pick the one that fits; if two fit, say which you chose and why in one line. Vary templates and dark/light (`class="light"` on `<body>`) across posts so the feed doesn't look repetitive. To see what was used last, check the latest X images in `x-assistant/images/` (ignore the `xhs-*` files, which are Xiaohongshu cards).

## 3. Write the image text
The image should **add** to the post, not repeat it word for word:
- Hook card: the core line, shorter than the post.
- List: the steps themselves (the post can just introduce them).
- Everything on the image must be true and come from the post or from Michael. Same rules as `x-assistant/voice.md` and the playbook's "Never do": no invented numbers, no hype, nothing from the "Avoid" list in voice.md.
- Highlight 2–4 key words with `<span class="hl">` in total, title included, not more.
- Respect the length limits in each template's `<!--EDIT-->` comments. Big text, few words: it has to read on a phone.
- Optional lines (like the grey `.d` line under a list item) stay empty when the post doesn't give that detail. Uneven items look fine; invented ones don't. Splitting the post's own sentence into a bold line and a grey line is fine.
- If the post names a count ("4 things…"), the card shows exactly that many items. The list template fits 3–6 and shrinks its text by itself at 5–6.

## 4. Build and render
1. Copy the template to `x-assistant/images/<short-slug>.html` (e.g. `evals-tips.html`). The `brand.css` link is relative to that folder, so keep it as is there; if you build the HTML anywhere else, point it at the absolute path of `templates/brand.css`.
2. Replace the content at each `<!--EDIT-->` marker. Don't change the footer or brand colors unless Michael asks.
3. Render: `bash .claude/skills/x-image/render.sh x-assistant/images/<slug>.html` → writes `<slug>.png` next to it.

## 5. Check it yourself
Read the PNG and check: nothing cut off or overflowing (the footer must be fully visible), no text touching edges, no awkward line breaks (one word alone on a line), no big empty band (if one area is mostly blank, make the text bigger rather than leaving it), readable at phone size, spelling correct. Fix every problem you see in one pass, then re-render; aim for 2 renders at most. For several images, `bash .claude/skills/x-image/contact.sh <sheet.png> <a.png> <b.png> ...` puts them on one sheet, so one Read checks them all.

## 6. Hand back
- **Called on its own:** send the PNG to Michael with SendUserFile (display: render), tell him which template you used, and offer one tweak (e.g. light/dark, different highlight).
- **Called from `/x-post`:** don't send it yourself. Return the PNG path and the template name; x-post shows it once, together with the drafts. When posting, it goes in through the composer's hidden file input with `file_upload` before the text is typed, and the preview is checked.

## Changing the brand
Colors, fonts and the footer line live in `templates/brand.css` and each template's `.foot`. If Michael wants a new look, change brand.css once and re-render a sample to show him.
