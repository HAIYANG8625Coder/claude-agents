# Series plan: 从零做一个 Claude Code 式 Agent (draft v2, 2026-11-17, waiting for Michael's choices)

Format: 8 episodes + 1 bonus, 4 to 5 minutes each, vertical, Chinese for Xiaohongshu. One public GitHub repo, one commit per episode, Python, about 100 to 250 lines in total. Viewers need an Anthropic API key (say so in episode 1). Sources: Anthropic's public engineering posts and the Claude Code docs only; label "Claude Code does this (documented)" apart from "our small version".

Every episode has the same six parts, so viewers learn the pattern:
1. 问题: what breaks in the previous version.
2. 概念: the idea in plain words, one diagram.
3. Claude Code 怎么做: what the docs say.
4. 我们写: the code, shown on screen (real recording), with the key lines highlighted.
5. 跑一遍: a real run, with the raw messages shown.
6. 坑: 2 to 3 mistakes people make, then a one-line takeaway and a cheat-sheet card.

## 1 Agent 就是一个循环
- Loop: messages list → call the model → if it asks for a tool, run it, append the result → call again → stop when it answers. Show the raw JSON of each turn.
- Build: 40 lines, one fake tool (get_time), a max-turns guard.
- 坑: forgetting to append the tool result; no stop condition; treating the model as the thing that runs code (it only asks).
## 2 工具
- A tool = name + description + input schema + a function. The model reads the description to decide.
- Build: read_file, grep, run_bash, edit_file (exact-string replace, why it beats rewriting a whole file). Return errors as results so the model can recover. Truncate huge output.
- 坑: vague descriptions; crashing on an exception; 50,000-line outputs.
## 3 系统提示和记忆文件
- What goes in the system prompt (role, rules, environment: folder, date) and a CLAUDE.md-style file loaded at start.
- Build: load notes.md into the prompt; test with 3 fixed tasks before and after.
- 坑: long prompts that dilute; rules the agent cannot check; changing the prompt without re-testing.
## 4 权限
- Read-only tools run freely; writes and shell commands ask; allow and deny lists by pattern; a plan-only mode.
- Build: a gate between "model asked" and "we run it", with allow, ask, deny.
- 坑: approval fatigue (fix: allowlist); and tool results are data, not instructions: a file saying "ignore your rules" must not be obeyed (prompt injection).
## 5 上下文
- The window fills with tool output. Count tokens; cut big outputs; compaction = replace old turns with a summary when near the limit and keep the recent turns.
- Build: token counter, a threshold, a summarize-and-replace step; chart of context size over a long run.
- 坑: summaries that lose decisions (keep the task list and files touched); compacting too late.
## 6 子 Agent
- Why: a fresh context for a side task, only a short result comes back. Build: run_subagent(task) starts a new loop with its own messages and fewer tools, returns the final text.
- 坑: a vague brief (the subagent cannot see your chat); giving it too many tools; no turn limit.
## 7 记忆
- Link to the 工程解读 02 video. Build: a notes folder, write only what can't be looked up again, load an index at start (Claude Code loads the first 200 lines or 25 KB of its memory index, per Anthropic's article). Optional "dreaming": a nightly pass that checks notes against the transcript.
- 坑: remembering everything (413 files vs 10); wrong notes believed forever.
## 8 一直在线
- Link to the 工程解读 01 video. Build: an inbox (queue), a timer that drops a message in it, the loop as a daemon, an outbox that sends one message to Telegram. Decide in advance what the agent may do when nobody is there to approve.
- 坑: two events at once; secrets in the agent's reach.
## Bonus 怎么测 Agent
- 3 to 5 fixed tasks, log every message, read one full trace, count turns and tokens. Change one thing at a time.

## Production notes
- Real screen recordings of the terminal (style B) for the code and runs, a drawn diagram and a cheat-sheet card (style G) per episode.
- The code is tested before the script is written, so every run on screen is real.
- Comments: end each episode with "下一集你想看哪一块?" and link the previous episode.

## Open choices for Michael
1. Python or TypeScript (recommended: Python).
2. Pilot episode 1 first (script, working repo, recorded run), then decide on the rest.
3. Length: 4 to 5 minutes each (this plan) or shorter.
