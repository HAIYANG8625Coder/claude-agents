---
name: x-image
description: Make an on-brand image for one of Michael's X posts (hook card, list/cheat sheet, code window, before→after, big number). Use when Michael runs /x-image, asks for a picture/image for a post, or when /x-post offers an image.
---

# X image

Makes clean, consistent post images from HTML templates rendered by headless Chrome. Free, no accounts. Every image shares one brand (`templates/brand.css`) and the same footer signature, so people start recognizing Michael's posts in the feed.

The templates follow the image styles that perform best in AI/dev X: quote cards, "save this" cheat sheets, Carbon/ray.so-style code windows, before→after splits, and big-number stat cards.

## 1. Know the post
Use the post text (from `/x-post` or what Michael gives). If there's no post yet, ask what it's about and stop.

## 2. Pick a template
| Template | Use when the post is… | Size |
|---|---|---|
| `hook.html` | a question, opinion, "let's connect", one strong line | 1600×900 |
| `list.html` | tips, steps, lessons, "N things…" (most bookmarked) | 1200×1500 portrait |
| `code.html` | code, a prompt, config, terminal output, a workflow as pseudo-code | 1600×900 |
| `compare.html` | before vs after, old vs new, myth vs reality | 1600×900 |
| `stat.html` | one real number: a result, milestone, benchmark, "Day N" | 1600×900 |

Pick the one that fits; if two fit, say which you chose and why in one line. Vary templates and dark/light (`class="light"` on `<body>`) across posts so the feed doesn't look repetitive — check recent images in `x-assistant/images/`.

## 3. Write the image text
The image should **add** to the post, not repeat it word for word:
- Hook card: the core line, shorter than the post.
- List: the steps themselves (the post can just introduce them).
- Everything on the image must be true and come from the post or from Michael. Same rules as `x-assistant/voice.md` and the playbook's "Never do": no invented numbers, no hype, nothing from the "Avoid" list in voice.md.
- Highlight 2–4 key words with `<span class="hl">`, not more.
- Respect the length limits in each template's `<!--EDIT-->` comments. Big text, few words: it has to read on a phone.

## 4. Build and render
1. Copy the template to `x-assistant/images/<short-slug>.html` (e.g. `evals-tips.html`). Keep the `brand.css` link as is; it's relative to that folder.
2. Replace the content at each `<!--EDIT-->` marker. Don't change the footer or brand colors unless Michael asks.
3. Render: `bash .claude/skills/x-image/render.sh x-assistant/images/<slug>.html` → writes `<slug>.png` next to it.

## 5. Check it yourself
Read the PNG and check: nothing cut off or overflowing, no text touching edges, no awkward line breaks (one word alone on a line), readable at phone size, spelling correct. Fix the HTML and re-render until it's clean. Then send it to Michael with SendUserFile (display: render).

## 6. Hand back
Tell Michael which template you used and offer one tweak (e.g. light/dark, different highlight). If called from `/x-post`, return the PNG path so it can be attached when posting: in Chrome, upload it to the composer's hidden file input with `file_upload` before typing the text, then confirm the preview shows it.

## Changing the brand
Colors, fonts and the footer line live in `templates/brand.css` and each template's `.foot`. If Michael wants a new look, change brand.css once and re-render a sample to show him.
