---
name: chart-draw
description: Draw clean, concise diagrams for docs (architecture overviews, step-by-step processes with data tables, timelines, sequence diagrams, state machines, decision trees, swimlanes, folder trees, side-by-side comparisons and layer stacks) as SVG in the style of Anthropic's "Building always-on agents" figures (beige panels, white boxes, one orange accent path with numbered steps, real example rows), check them for overlapping labels with headless Chrome, and embed them in README or docs Markdown. Use whenever someone asks for a diagram, flowchart, architecture picture, workflow chart, "how it works" figure, sequence or state diagram, decision tree, swimlane, folder structure picture, "option A vs B" figure or system overview for a repo, agent, skill or doc; when Mermaid or ASCII diagrams look messy; or when they ask to "draw it like that article". Not for charts of numbers (bar, line, pie: use a data-viz tool) or for slides.
---

# chart-draw

Make a diagram a reader understands in one look: few boxes, one highlighted path, real names, labels that never touch a line. Output is a standalone SVG file (renders on GitHub, in VS Code and in browsers), embedded in Markdown with alt text.

Why hand-written SVG and not Mermaid: Mermaid lays boxes out automatically, so labels collide and wide graphs shrink to unreadable on GitHub. Placing every box yourself is what gives the calm, lucid look. The checker below catches the mistakes hand placement causes.

## 1. Get the facts first
Read the code or docs you're drawing. Every box, arrow and example row must match what really exists: table names, file names, times, counts. Write down the 5–12 things that matter and how they connect. If you can't say what an arrow means in a few words, leave it out.

## 2. Pick the diagram type
Choose from the question the reader has. `references/catalog.md` has a recipe for each type: what goes where, what's orange, and what to leave out.

| Reader's question | Type | Start from |
|---|---|---|
| How do the parts fit together? | Overview | `assets/overview.svg` |
| What happens step by step, to what data? | Steps + table | `assets/steps.svg` |
| What happens over time? | Timeline | `assets/timeline.svg` |
| Who calls whom, in what order? | Sequence | `examples/sequence.py` |
| What states does one thing go through? | State machine | `examples/states.py` |
| Which path do I take? | Decision tree | `examples/decision.py` |
| Who does each step? | Swimlane | `examples/swimlane.py` |
| What's in this folder, who reads it? | Folder tree | `examples/tree.py` |
| Why this option, not that one? | Compare | `examples/compare.py` |
| What sits on top of what? | Layers | `examples/layers.py` |

Most systems need two or three diagrams, for example an overview plus one detail. Avoid one giant chart.

**Two ways to draw.** The first three are hand-written SVG files: copy one next to your Markdown (e.g. `docs/overview.svg`) and edit the text and coordinates. The other seven are short Python scripts using `scripts/svgkit.py`, which draws every box, arrow, label, pill and table in the house style, while you still choose each position. Copy the closest example to a scratch folder, change the content and the `save()` path, and run it with `python3 -I`. For a new type, start a blank `Diagram(1200, h)` and use the kit. Run `python3 -I -c "import sys; sys.path.insert(0, '<skill>/scripts'); import svgkit; help(svgkit.Diagram)"` to see its methods. Use the kit whenever you're not editing one of the three SVGs: it keeps colours and arrowheads consistent for you.

## 3. Draw
Read `references/style.md` once for colours, sizes, arrows and label rules. The rules that matter most:
- Keep the 1200 px wide viewBox and the white background rect.
- Straight horizontal or vertical arrows. Put a label beside its arrow, never on it.
- Orange only on the path you want the reader to follow; everything else black or grey.
- At most two highlighted (orange) boxes.
- Leave about 15% spare width in boxes and labels for wider fallback fonts.

Compute positions instead of guessing when something is to scale (a timeline: pixels per hour; a table: fixed row height), and write the scale in an SVG comment so the next edit can follow it.

## 4. Make the dark version
Light is the default and the only one you edit. Generate the dark twin from it, so the two never drift apart:
- svgkit: `d.save(path)` already writes `<name>-dark.svg` next to `<name>.svg` (pass `dark=False` to skip it).
- Hand-written SVG: `python3 -I <this skill>/scripts/theme.py docs/overview.svg` writes `docs/overview-dark.svg`.

`theme.py` maps every palette colour to its dark partner. It reports any colour it doesn't know, so stick to the palette in `references/style.md`. After any edit to the light file, run it again.

## 5. Check, look, fix
```bash
python3 -I <this skill>/scripts/check.py docs/*.svg --out <scratch dir> --github   # light and dark
```
It needs Chrome (it finds Google Chrome or HyperFrames' headless shell, or set `CHROME`). For each SVG it writes a PNG, plus `-github.png`: the diagram at GitHub's 880 px README width with Arial, which is what Windows and Linux readers see. It lists text overlapping text, a line crossing a label, text spilling over a box or panel edge, boxes cutting into each other (a pill running out of its panel), and anything outside the viewBox. Exit code 1 means fix something.

Then open the PNGs, light and dark, and look yourself. The checker can't see a box that's too crowded, an arrow pointing at the wrong thing, a label too small at 880 px, or a layout that reads in the wrong order. Fix everything, re-run, and look again. Two or three rounds is normal.

## 6. Embed
Use GitHub's light/dark picture, with light as the default. Readers in dark mode get the dark file; everyone else, and every viewer that ignores `<source>` (VS Code preview, most Markdown tools), gets the light one:
```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/overview-dark.svg">
  <img alt="How the stats agent fits together: timers and the inbox start a run; the run reads the creator center and writes stats.md; the outbox sends to Telegram" src="docs/overview.svg">
</picture>
```
If the user wants only one theme, use plain `![alt](docs/overview.svg)` (light), or point it at the `-dark.svg` file when they ask for dark.
- Alt text says what the diagram shows in one sentence, for screen readers and for when the image fails.
- Put one or two sentences under the image for what the picture can't say (where things live, what costs nothing).
- If this replaces a Mermaid block, delete the old block.
- Commit both SVGs (light and `-dark`), not the PNGs (the PNGs are only for checking).

## Worked examples
Every file in `assets/` is a real diagram from the repo this skill came from (the stats agent, the voice-video take, the avatar-video pipeline). `agents/stats-agent/PLAN.md` there shows three of them embedded with alt text.
