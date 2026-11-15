# Catalog: which diagram for which question

Pick the type from the question the reader has. Each has a finished SVG in `assets/`. Seven of them also have the Python that drew them in `examples/` (built with `scripts/svgkit.py`). Copy the closest one and change its content.

| Reader's question | Type | Asset | Built with |
|---|---|---|---|
| How do the parts fit together? | Overview | `overview.svg` | hand-written SVG |
| What happens, step by step, and to what data? | Steps + table | `steps.svg` | hand-written SVG |
| What happens over time / when does it wake? | Timeline | `timeline.svg` | hand-written SVG |
| Who calls whom, in what order? | Sequence | `sequence.svg` | `examples/sequence.py` |
| What states does one thing go through? | State machine | `states.svg` | `examples/states.py` |
| Which path do I take? | Decision tree | `decision.svg` | `examples/decision.py` |
| Who does each step (people, services, tools)? | Swimlane | `swimlane.svg` | `examples/swimlane.py` |
| What's in this folder and who reads it? | Folder tree | `tree.svg` | `examples/tree.py` |
| Why this option and not that one? | Compare | `compare.svg` | `examples/compare.py` |
| What sits on top of what? | Layers | `layers.svg` | `examples/layers.py` |

## Recipes

**Overview.** Three beige columns: what starts it, what it works with, what leaves it. The main thing goes in the middle as a black-bordered box, with its helpers below it, each joined by one straight arrow. Orange marks the main path. A thin line round the bottom shows how a person can start it by hand.

**Steps + table.** A source box at the top, a beige table in the middle with 3–4 real example rows, and the worker and run boxes at the bottom. Number the orange arrows 1, 2, 3 … in the order things happen. Put the rows being worked on in one orange frame. Show one faded, dashed "dropped" row, so the reader sees what gets filtered out.

**Timeline.** One dotted axis drawn to scale (write px per hour in a comment). Short orange bars for activity, grey "idle" labels in the gaps, and labels alternating above and below so neighbours never collide. Put a day marker at midnight.

**Sequence.** 3–5 participants as boxes across the top, with dotted lifelines down. Requests are orange and numbered; replies are grey and dashed, with no number. A side note in a dashed box sits beside the lifeline it's about, never on it. Keep each message label under about 30 characters (shorter than the gap between two lifelines).

**State machine.** A black dot for "created". The state the thing spends most time in is the accent box. The happy path runs left to right in orange; failure paths go down in black. A self-loop (retry) arcs over the top of its box, with its label beside the loop. Faded box for states that never really exist ("dropped").

**Decision tree.** The start is a black-bordered box. Questions are dark filled boxes ending in "?", with "yes"/"no" written on the branch just after the split. The branch taken today is orange, and leaves are plain or accent boxes. Stop at 2–3 levels; deeper trees belong in a table.

**Swimlane.** One beige band per actor, with the actor's name on the left. Steps are numbered small boxes, one column per step. Arrows leave a box from its top or bottom edge, turn once, and enter the next box from the left. The person's decisions are black boxes, and the one gate that matters most is the accent box.

**Folder tree.** Monospace names with ├─ └─ guides in grey. Highlight the files the story is about in orange. Group files with a bracket on the right, and an arrow to a box that says what the group is for ("Loaded into every run"). Add a short note on the same row for one-off files.

**Compare.** Two equal panels. The chosen option gets the accent title box and a dark "chosen" pill inside its panel; the rejected one gets a faded title box. 3–4 points each, ✓ in green `#1e7a3c` and ✗ in red `#c23b22`, with the same count on both sides. Be honest: give the winner its ✗ too.

**Layers.** Full-width beige bands stacked top to bottom from most general to most concrete. The layer the reader should care about gets an orange outline. Pills inside each band name real members. Add one side box only if something reaches across layers.

## When none fits
Combine at most two types, for example a sequence with a small table, or an overview with a timeline below it. If a reader would need more than about 30 seconds to read the diagram, split it in two.
