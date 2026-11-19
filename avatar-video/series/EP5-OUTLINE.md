# Episode 5 outline: 上下文 (context). Style H, landscape, about 7 min, Chinese

Series tag: 从零做 Agent · 第 5 集. Cover: "Agent 越跑越长，窗口怎么不爆" / subtitle "数 token，清旧结果，再压缩". Source line on slides: Claude Code docs (Context window, How Claude Code works, Costs, Commands), Anthropic engineering post "Effective context engineering for AI agents" (2025-09-29), API docs (token counting, context editing). Code: series/agent-from-scratch/ep05. Research: EP5-RESEARCH.md.

## 0 开场
Hook: the same task, 24 files, one file at a time. Without any care the window grows to about 25,000 tokens by turn 25; with our manager it stays under about 13,000 and gives the same answer. Why care: the window is finite, every turn re-sends all of it, and the docs call the quality loss "context rot".

## 1 窗口里装了什么 (problem + concept)
Everything counts: system prompt, notes, every message, every tool result, tool definitions (docs). Diagram: a bar filling up with colored slices. Claude Code's /context shows it as a grid. Pitfall seed: the loop re-sends the whole history each turn.

## 2 数一数 (build 1: count)
Count with the number the API returns, not a guess. Real finding: on DeepSeek's endpoint `input_tokens` was 225 on a second call, but the window was 1,633, because 1,408 were cache reads; the docs say cached prefixes still fill the window. So we add the cache fields. Also the count_tokens endpoint exists (docs), and our chars/4 estimate is only a rough tool. Diagram: input_tokens + cache_read + cache_creation.

## 3 先清旧结果 (build 2: clear)
Anthropic's post: "one of the safest lightest touch forms of compaction is tool result clearing". Ours: keep the newest 3 results, replace older ones with a one-line note; every call keeps a result. Diagram: before/after message list. Real run: the saw-tooth chart (grows, drops, grows).

## 4 再压缩 (build 3: compact)
When clearing is not enough: ask the model to summarize the old turns with a fixed prompt (task, decisions, files, what is open, next step), keep the last 4 turns whole, re-load notes and the file list. Claude Code (docs): compacts near the limit, summary "keeps your requests and key code snippets" but early instructions may be lost; CLAUDE.md is re-injected from disk; up to five recent files re-read. /compact takes focus instructions. Say clearly: the docs do not give the summary's format or a percentage.

## 5 真实测试 (real runs)
Four setups x 3 real runs (DeepSeek): none / clear / compact / both. Chart of tokens per turn. Numbers (filled from demo/repeat/, checked with code): peak about 25K / 8.8 to 11.5K / 12.7 to 12.9K / 8.9 to 10.9K; answers correct in 3/3, 3/3, 3/3 and 2/3 (one "both" run hit the 60-turn limit). Say that 3 runs is too few to rank them.

## 6 坑
1. Clearing erased the only copy of what it found: the first version started over after reaching the end of the chain (real run, 60 turns). Fix: tell the model to write findings in its own reply; it helped, not a guarantee (one clear run needed 53 turns).
2. Summaries lose decisions (docs: early instructions may be lost); keep the task, decisions, files; put lasting rules in the notes file.
3. Compacting too late, or a single huge output that refills the window: Claude Code stops auto-compacting after a few attempts (docs). Cut big outputs at the tool (ep2).

## 7 合起来
Recap table: count / clear / compact / 坑, with the number for each. Also: /clear between unrelated tasks (docs), subagents next (ep7: fresh window, a summary comes back).

## 8 结尾
Question: 你的 Agent 跑多长会"忘事"？下一集：计划和任务清单。

## Notes for Michael
- Real runs use DeepSeek (like earlier episodes); the slides say so.
- The compaction summary is written by the same model; we do not claim it is as good as Claude Code's.
- Claude Code's default threshold for 1M-window models is about 967K tokens (docs, model config page); our 9,000 to 12,000 is a demo setting.
