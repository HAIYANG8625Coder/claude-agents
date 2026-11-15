# Style: concise, lucid diagrams

The look comes from the figures in Anthropic's article "Building always-on agents" (2026-11-13). The assets in `../assets/` follow it exactly, so copy a token from them rather than inventing a new one.

## Tokens
| Use | Value |
|---|---|
| Page background (always set it, so dark-mode GitHub still shows a white card) | `#ffffff` rect covering the viewBox |
| Panel / group background | `#f0ede6`, `rx` 14–20, no border |
| Plain box | white `#ffffff`, border `#d8d4cc` 1.5 px, `rx` 9 |
| Main box (the thing the diagram is about: "A run", "Worker") | white, border `#1f1f1f` 2.5–3 px, `rx` 10–16 |
| Highlighted box (the one or two parts the diagram is teaching) | fill `#fcefe5`, border `#d4600b` 2.5 px, plus a halo: a `#e9c9ae` rect 6 px larger behind it |
| Accent (the main path, numbered steps, part names) | `#d4600b` |
| Ink (titles, black arrows) | `#1f1f1f` |
| Secondary text (subtitles, arrow labels) | `#6b6b6b` (or `#555` on big diagrams) |
| Quiet notes (footnotes, "nothing happens" paths) | `#8a8a8a`; faded rows `#9a968e` |
| Dropped / optional thing | dashed border `#a8a49c`, `stroke-dasharray="9 7"` |
| Font | `font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"` on the root `<svg>` |

## Light and dark
Light is the default theme, and it's the only file you draw or edit. `scripts/theme.py` (or `svgkit`'s `save()`) writes the `-dark.svg` twin by swapping each palette colour for its dark partner:

| Role | Light | Dark |
|---|---|---|
| Page | `#ffffff` | `#0d1117` (GitHub dark) |
| Panel | `#f0ede6` | `#1c1a17` |
| Box / card | `#ffffff` | `#2a2723` |
| Ink | `#1f1f1f` | `#ece8e1` (dark-filled boxes flip to light) |
| Accent | `#d4600b` | `#f0883e` |
| Accent fill / halo | `#fcefe5` / `#e9c9ae` | `#3d2616` / `#6b4024` |
| Secondary / notes | `#6b6b6b` / `#8a8a8a` | `#aca69d` / `#8f8a82` |
| Thin borders | `#d8d4cc` | `#4a4640` |
| ✓ / ✗ | `#1e7a3c` / `#c23b22` | `#3fb950` / `#f85149` |

A colour outside this palette has no dark partner, and `theme.py` warns about it. If you truly need a new colour, add its pair to `DARK` in `theme.py`.

## Type sizes (at a 1200 px wide viewBox)
- Column / panel headings 17 bold; diagram title 21 bold.
- Box title 19–24 bold; box subtitle 14 (12.5 when three lines must fit).
- Arrow labels 13–14 regular, secondary colour. Numbered steps 20–22 bold accent.
- Never below 12.5: on GitHub a 1200-wide diagram is shown at about 880 px, so 12.5 becomes about 9 px.

## Arrows
- Two markers in `<defs>`: a black one (`#1f1f1f`) and an orange one (`#d4600b`), `orient="auto-start-reverse"`, so `marker-start` gives a two-way arrow.
- Orange, thicker (2.5–5 px) for the main path; black 2 px for supporting links; dashed for "later", "optional" or "wakes".
- Straight horizontal or vertical lines. Bend with one rounded corner (`Q`) instead of diagonals. Diagonals were the main source of labels crossing lines.
- Arrows stop 4–6 px short of a box edge, so the head doesn't sit on the border.

## Labels
- An arrow label sits beside its line: to the right of a vertical arrow (x + 10), above a horizontal one (y − 12). Never centred on the line.
- One to four words per line. Break long labels into two `<text>` lines 18 px apart instead of shrinking them.
- Leave about 15% spare width in every box and label. Windows and Linux readers see Arial, which is wider than Inter or the Mac's system font.

## Content rules
- Use real names and example rows from the system you're drawing (table names, times, file names), not "Component A". A table with three example rows teaches faster than a box labelled "database".
- Show what is *not* done too, quietly: a faded "dropped" row, a grey "nothing pending: no tokens" note.
- One idea per diagram. If you need more than about 12 boxes, split it into an overview and a detail diagram.
- Plain English labels. Keep code names (`agent.py`, `stats.md`) where the reader will meet them in the repo.
- Text in Chinese or other scripts is fine, but add a CJK font to the family list (`'PingFang SC', 'Noto Sans CJK SC'`) and check the GitHub render.
