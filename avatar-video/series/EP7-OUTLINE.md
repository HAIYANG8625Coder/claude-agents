# Episode 7 outline v2: subagents (for approval; new workflow, 2026-11-19)

Format: article-explainer, landscape, about 7 min, series "从零做 Agent 第 7 集". Same look as ep 6.
Cover: 「Agent 的小助手：子 Agent」 / 「让它去翻几十个文件，只带回一页纸」

## Beginner gate (each term explained before use)
- 子 Agent: a helper the main Agent starts for one side task. Own fresh conversation, brings back only a short result. Picture: send an assistant to the library, get a one-page note. Chapter 2.
- 上下文: the conversation the model can see; every tool result stays in it. One-sentence recap of ep 5. Chapter 1.
- 简报: the task text handed to the helper. It cannot see your chat. Chapter 5.
- 并行: several helpers at once. Only mentioned (docs, Anthropic post). Ours runs one at a time.

## Chapters
0 开场: the real test in one line: "每周发帖汇总", 27 posts, 3 runs per setup, DeepSeek. Three questions: what is a subagent, why, does it help.
1 问题出在哪 [D1 context filling]: every tool result stays. Reading 10+ files for one list leaves them all in the context.
2 什么是子 Agent [D2 main vs sub]: one sentence + library picture.
3 为什么需要 / 代价 [D3]: keeps main context clean, read-only so safer; costs more tokens (Anthropic: agents ~4x chat, multi-agent ~15x), may lose detail. Not always worth it.
4 Claude Code 里的样子 (docs, to re-check): own context, returns a summary; built-ins Explore / Plan / general-purpose; custom = a Markdown file. Anthropic research system: lead + parallel helpers, and where it does not fit.
5 我们自己做的 [D4 code path + code slide]: delegate tool, fresh messages, read-only tools (read_file, grep), turn limit, returns final text only. Brief must hold everything.
6 真实测试 (3 intro slides: task, scoring, setups) then results [D5]. The test runs with EVERY learned part on, and each part is named on screen the moment it acts (this answers your message 626):
   - system prompt + notes (EP3): the task and rules the agent starts with
   - tools read_file / grep (EP2): how it looks at the 27 entries and post files
   - permission gate (EP4): it asks before run_bash (asked counts from the runs)
   - plan mode (EP6): reads first, submit_plan, then edits
   - task list (EP6): todo_write items ticking off
   - context manager (EP5): clear old results / compact (real counts)
   - subagent (EP7): delegate, short answer comes back
   - the loop (EP1): every model call is one turn (39 to 70 per run)
   Results (our runs, 3 each): plain rows 25/27/27, hashtags 20/27/21, calls 39/56/70. Delegate-asked rows 27/27/27, hashtags 27/21/27, calls 34/36/57, helpers started 0/2/1. Honest: 3 runs, helper used in 3 of 9 slots, main peak 11k to 24k either way. Cannot claim it is better; it was a bit faster in 2 of 3.
7 一个真实的坑 (we really hit it): context manager compacted almost every turn (30+ per run), because the fixed part (system prompt, tools, notes) was already near the trigger; the 60-turn cap ended 5 of 6 runs unfinished. Before/after code: compact only after the context grew another 3000 tokens since the last compaction. After the fix about 7 compactions per run and all 6 runs finish (with a 100-turn cap). Honest: the cap also went 60 to 100 at the same time.
8 EP1 到 EP7 总复习 [D6 map]: one line per episode, each tied to where it showed up in the test: 1 loop, 2 tools, 3 prompt + notes, 4 permissions, 5 context, 6 plan + list, 7 subagent. Then: what the agent has now, what is missing (ep 8: hooks).
9 结尾: question for the comments.

## Open points
- Length about 7 min (a bit longer than ep 6 because of the review).
- Syllabus: EP8 is hooks.
- Facts file: numbers computed from demo/*.json by code (not typed).
