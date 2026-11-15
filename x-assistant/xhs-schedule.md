# Xiaohongshu posting schedule

The `xhs-post` skill reads this file before it asks Michael to publish. All times are Singapore time (same as Beijing time). Change the rules here, not in the skill.

## Rules
- **Slots:** 12:30 and 20:30. Nothing is published between 23:00 and 07:00.
- **One note a day.** If today already has a published or scheduled Xiaohongshu note in `posts.md`, the new one takes the next free slot on a later day.
- **Never publish straight after a render or a draft.** A finished note is scheduled with 定时发布 for its slot.
- **AI declaration:** every note with AI-generated video, images or voice sets 内容类型声明 to the AI-generated option before publishing.
- **Michael's word wins.** If he says "publish now" or names another time, do that, and write `Slot: off-plan` in the log.

## Slot test, 16–29 Nov 2026
Goal: find out whether 12:30 or 20:30 gets more views for this account.

| Day | 16–22 Nov | 23–29 Nov |
|---|---|---|
| Mon | 20:30 | 12:30 |
| Tue | 12:30 | 20:30 |
| Wed | 20:30 | 12:30 |
| Thu | 12:30 | 20:30 |
| Fri | 20:30 | 12:30 |
| Sat | 12:30 | 20:30 |
| Sun | 20:30 | 12:30 |

- **Topic mix per week:** at least 5 of 7 notes on the main topic, at most 2 on the second. No stock notes during the test unless Michael says so.
- **Main topic:** Claude Code / AI (default; Michael may change it after he reads the baseline numbers in the app).
- **Second topic:** Singapore life.

## What to log
Each Xiaohongshu entry in `posts.md` gets two extra lines:

```
Slot: 20:30 Mon 2026-11-16 · Topic: main | second | other
24h: views N · likes N · saves N · comments N (read 2026-11-17 20:40)
```

The `24h:` line is added later, once the note has been live for 24 hours.

## Decision on 30 Nov 2026
- Compare the median 24-hour views of the 12:30 notes with the 20:30 notes. If one slot is ahead by about 30% or more, it becomes the only default slot. If not, use 20:30.
- Compare main topic against second topic the same way.
- Seven notes per slot is a small sample: treat the result as a direction, not proof.
- Then replace the test table above with the chosen slot.

## After the test
Until this file is updated, keep using the table's pattern (alternate 12:30 and 20:30).
