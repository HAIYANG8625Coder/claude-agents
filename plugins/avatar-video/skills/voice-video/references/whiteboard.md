# Style preset I: whiteboard hand-drawing (手绘动画)

A white board per sentence. Line drawings with a little flat colour are uncovered stroke by stroke while a hand with a marker draws them, each one on its spoken word, with a short label under it and karaoke captions at the bottom. The last board can be a list worth saving.

Approved by Michael on 2026-11-25 (AI words, 14 boards, 85 s, `videos/2026-11-25-ai-words-handdraw/`, local only). The idea came from a Xiaohongshu whiteboard-drawing tutorial he sent.

Use it for explaining words or concepts in Chinese. The caption splitting is built for Chinese and has not been tried on English.

`$S` is `.claude/skills/voice-video/scripts`.

## Order of work
1. **Script and boards first.** One sentence per board. For each board write the title, the pill under it, 4 drawings (6 for a longer sentence), the words that start each drawing and its label. Michael approves the script **and** this board list (labels are new text he must see) before the voice.
2. **Voice:** `../SKILL.md` steps 2–3.
3. **Pictures (paid, ask first):** one per board except the sheet. Say how many, then wait. No automatic retries.
4. Write `boards.json`, build, check, render:
   ```bash
   python3 -I $S/whiteboard.py avatar-video/videos/<folder>
   cd avatar-video/videos/<folder> && npx hyperframes check && npx hyperframes render; cd -
   python3 -I $S/qa.py avatar-video/videos/<folder>
   ```
   Don't run `sync.py`: this script places the drawings and captions itself.
5. **Look at frames** across the whole video: each drawing matches its words, no hand with a floating arm end, labels not covering drawings.

The folder needs `hyperframes.json`, `meta.json` and `package.json` from `avatar-video/template/`.

## Pictures
Buzzy, model **Nano Banana 2**, **3:4**, **2k**. Save as `assets/raw/sNN.png`, where NN is the board number (`s01.png` is the first). Pass one earlier picture as the reference image so the style and characters stay the same.

```
Use the reference image only for the line style, the colours and <the characters to keep>. Draw a completely new picture.
Whiteboard hand-drawing illustration on a pure flat white background (#FFFFFF), clean confident black marker line art with a little flat colour accent (pale blue, orange, teal, red), simple and uncluttered, no shadows, no border.
Exactly four separate drawings in a grid of 2 columns and 2 rows, each centred in its own quarter, with very wide empty white space between them, nothing touching or overlapping, no connecting lines, no dividers, no frames.
Top left: <one object or action>.
Top right: <…>.
Bottom left: <…>.
Bottom right: <…>.
Absolutely no letters, no words, no numbers, no logos, no watermark.
```
For six drawings: "six … 2 columns and 3 rows … Row 1 left: …". The characters used so far: a young woman with a short black bob, and a small pale blue helper robot with a dark screen face, cyan eyes, one red-tipped antenna and orange ear knobs. All words are added by the code, never drawn into the picture.

## boards.json
Full example: `avatar-video/brand/whiteboard/boards.example.json`.

| Key | What it is |
|---|---|
| `boards[]` | in spoken order: `num` (badge such as `"01"`, or `""`), `title`, `sub` (the pill), `rows` (2 or 3, the grid of that picture), `items` |
| `items[]` | `[column, row, phrase, label]` in drawing order; column 0 = left, row counts from 0 |
| `phrase` | words from that sentence, spelled as in `script.json` (`"R A G"`), that start the drawing. `null` = already drawn at frame 0: use it for the first drawing of board 1, so the thumbnail isn't blank |
| `show` | spoken spelling → caption spelling, e.g. `["A I", "AI"]` |
| `footer` | small line at the bottom; keep the AI-generated notice |
| `sheet` | optional last board for the last sentence: `title`, `rows` (up to 11 `[word, meaning]`), `ask`, `ask_at`, `star`, `star_at` (the `_at` phrases are words from that sentence) |

## Cover and upload
Xiaohongshu's default 3:4 crop of the first frame cuts off the title. Make the cover from the end of board 1 and upload it under 上传封面:
```bash
python3 -I $S/whiteboard.py avatar-video/videos/<folder> --cover renders/<video>.mp4
```
The browser upload limit is 10 MB; make a smaller copy with ffmpeg `-c:v libx264 -crf 27 -preset slow -c:a aac -b:a 128k -movflags +faststart`. Publishing goes through `xhs-post`, with the AI-content declaration.

## The hand
`avatar-video/brand/whiteboard/hand.png` (AI-generated, 1024×1024, transparent) is copied into the video's `assets/img/` automatically. The right column uses it as it is and the left column uses its mirror image. The pen tip and arm numbers (`TIP`, `HS`, `P`, `U`, `STRETCH` in `whiteboard.py`) fit this picture only.

For a new hand: generate it 1:1 at 1k on solid `#00FF00` (one right hand holding a marker, tip to the upper left in open space, forearm leaving through the bottom right corner, no sleeve, no shadow), then `python3 -I $S/whiteboard_key.py hand-green.png hand.png`, look at `hand-check.png`, and measure the new numbers.

## What went wrong before
- **"The arm is too long" (Michael, demo v1):** one right hand had to stretch ×7 to reach the left column. The mirrored hand fixed it. Don't raise `STRETCH` (2.8) to hide a gap.
- **An extra row in the picture** (3 of 12): if it leaves a clean 3-row grid, set `"rows": 3` and use rows 0 and 2; the unused row stays covered.
- **"drawings touch across cells":** two drawings are joined. That picture needs a new generation (ask first).
- **"runs out of time":** the sentence is too short for its drawings. Use fewer drawings on that board.
- **Labels that flash by:** a drawing that finishes just before the next board shows its label briefly. Move its phrase earlier.
- `check` reports `line_unread` warnings for short captions. They follow the voice, so that is expected.
