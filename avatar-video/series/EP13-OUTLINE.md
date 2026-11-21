# Episode 13 outline: putting it together (for approval; process of 2026-11-21)

Format: article-explainer, landscape, aim for about 8 min (ep 12 ran 8:20 with 36 slides). Series "从零做 Agent 第 13 集" (the last one). Same look as ep 12. Say "token" and "skill" in English.
Cover: 「从零做出来的 Agent，能日常用了」 / 「一个聊天循环，把前十二集接在一起」
Real test is DONE before this outline (ep13/demos.py: T1 5+5, T2 5+5, T3 5+5, T4 5 = 30 runs, DeepSeek, every earlier part on; 38 no-key checks in test_repl.py; both committed in agent-from-scratch, c371f8e). Sources: EP13-RESEARCH.md (Claude Code docs: interactive mode, how it works, sessions, checkpointing, commands, security, sandboxing, sub-agents, headless; Anthropic streaming page).

## Beginner gate
- 聊天循环 REPL (read-eval-print loop): a loop that reads what you type, runs it, prints the answer, and waits for the next line. Ch 2.
- 流式输出 streaming: the model sends its reply in small pieces as it writes, so the text shows up while it is still working, not all at the end. Ch 2/4.
- 会话 session: the whole conversation saved to a file, so you can come back to it later. Ch 2/4.
- 斜杠命令 slash command: a line that starts with `/` and is a command to the program, not a question for the model. Ch 2/4.
- 中断 (Ctrl+C): stop the current turn without closing the program. Ch 2/4/7.

## Chapters
0 开场: hook: for twelve episodes our agent took one task and quit. A real tool is something you talk to for an hour. What does it take? Three questions: what is missing, does the finished one work, what does Claude Code have that ours does not.
1 问题出在哪 [D1]: one-shot agent: every prompt starts from nothing; "which files did you change?" has no answer. Real number later (fresh: 0 of 5).
2 什么是聊天循环 [D2, 3 slides]: REPL in one picture; streaming (pieces vs all at once); session file and slash commands; interrupt.
3 Claude Code 里的样子 (docs, read): the loop "gather context, take action, verify results" and you can interrupt at any point; Esc stops the turn and keeps the work done; Ctrl+C / Ctrl+D rules (800 ms); history, multiline; sessions as a JSONL file under ~/.claude/projects, --continue and --resume restore history, model, permission mode, interrupted tool calls are not rerun; /clear, /compact, /context, /resume, /rewind; about 130 commands; streaming for scripts: stream-json with --include-partial-messages. Streaming API: event order, text_delta, tool_use arrives as input_json_delta.
4 我们自己做的 [D3 + code]: agent.py changes (run() can continue a conversation, one model call function with stream=True using the SDK's text_stream and get_final_message, blocks are plain dicts so a chat saves to JSON as is); repl.py (Chat class, slash commands, save after every turn, --continue, Ctrl+C closes the half turn: results for open tool calls); which episodes are switched on (EP1 to 9, 11; EP10's always-on runner shares the engine). 38 checks without a key.
5 真实测试 (3 intro slides + one real session): four prompts in a row on the shop project (what does cart.py do / where is the tax rate / change it to 8% / list every file you changed), kept chat vs each prompt from nothing; streaming: time until the first text is on screen (5 runs each, one at a time); Ctrl+C at the first tool call, then another prompt, with and without the repair; resume in a new process with --continue.
6 结果 [D5]: T1: change done 5/5 in both; "list every file you changed" right 5/5 kept, 0/5 fresh (it cannot know); prompt 2 took 2.4 tool calls on average kept vs 4.6 fresh; total tokens read 101,105 vs 88,425, runs vary 59,533 to 153,509, so the kept chat is NOT shown to cost less or more. T2: first text on screen after 5.1 s mean streamed (0.69, 4.41, 6.46, 6.64, 7.30) vs 7.04 s mean not streamed; total time 7.44 vs 7.04 s; the model thinks silently before the first word, so streaming helps by 1 to 7 seconds, not always. T3: with the repair the next prompt worked 4/5; without it 0/5, the API refuses ("tool_use ids were found without tool_result blocks"). T4: resumed in a new process and answered right 5/5. Honest: five runs, one model, our own small project.
7 一个真实的坑 (we really hit it): Ctrl+C leaves a half turn (a tool call with no result); the API answers 400 on the next prompt and the chat is dead: 0/5 without the repair. Fix: close the turn before the next prompt. Second, smaller, and not fixed: in 1 of 5 repaired runs the model read "stopped by the user" as final and answered "I don't know" instead of looking again. Third (found by a check, one line): with --no-stream the first version printed no answer at all.
8 EP1 到 EP13 总复习 [D6 map]: one line per episode, 13 boxes; "what Claude Code has that ours does not" with its source: OS-level sandbox (writes limited to the working directory, network through an allowed-domains proxy; our permission gate only decides whether a command runs, not what it can touch); auto permission mode with a classifier, workspace trust dialog; subagents as files with their own tools, model and memory, plus built-in Explore and Plan; checkpoints and /rewind, session picker, /branch; input editing, history, image paste; about 130 commands, status line, managed settings, cloud sessions. Where to go next: harder test tasks (ep 12), a sandbox, a real terminal UI, your own tools through MCP.
9 结尾: one line takeaway (an agent is a loop plus a few boundaries; the rest is plumbing you can read), then the question for the comments: "做完这十三集，你最想给自己的 Agent 加什么？"

## Notes / open points
- DeepSeek streams text normally but spends a few seconds thinking before the first text delta; our "time to first text" counts only text, as the SDK's text_stream does. Said on screen.
- The Ctrl+C was simulated in the test by raising KeyboardInterrupt when the first tool call is announced (a real key press cannot be scripted); the code path is the same one a real Ctrl+C takes. Said on screen.
- Claude Code facts come from the docs only; the summarized tail of three pages (commands, sandboxing, sub-agents) is not quoted. The status line and Agent SDK streaming pages were not read.
- EP10's always-on runner is not inside the chat loop; stated, not hidden.
- README of the repo updated (usage, progress table); the written article for ep 13 (and 11, 12) is not written yet.
- Length about 8 min; all numbers computed from demo/*.json by code (facts.json).
