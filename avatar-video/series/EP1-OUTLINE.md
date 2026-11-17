# Episode 1 (pilot): Agent 就是一个循环 · about 8 minutes, vertical

Sources (all official, read 2026-11-17): code.claude.com/docs/en/how-claude-code-works, /agent-sdk/agent-loop, /tools-reference; anthropic.com/engineering/building-effective-agents (Dec 2024). Claude Code's core source code is not published, so no claim goes beyond the docs; "our version" is labelled as ours.

0 开场 (30 s): "50 行 Python，让 AI 自己查文件、改代码。" What the series builds, what you need (Python, an Anthropic API key, a terminal).
1 Agent 是什么 (60 s): Anthropic's definition: a model using tools in a loop, based on feedback from the environment. Chatbot vs agent in one picture.
2 Claude Code 的循环 (90 s): official three phases gather context → take action → verify, repeated until done; a turn ends when the model answers with no tool call; the Agent SDK runs "the same loop" as Claude Code.
3 一轮到底发生了什么 (120 s): the raw messages, step by step: user asks → model replies with a tool_use block → our code runs the tool → we send back a tool_result → model answers. The model never runs anything itself.
4 写代码 (150 s): the loop in four moves (call, check stop reason, run tools, append results), with a max-turns guard. Real recording of the code.
5 跑一遍 (90 s): "这个文件夹里有什么？" — a real run, with the messages printed each turn.
6 什么时候停 (45 s): ends when no tool call; max turns (Claude Code's maxTurns, SDK error_max_turns); why a guard is needed.
7 三个坑 (45 s): forgetting to append the tool result; no stop condition; thinking the model executes code.
8 我们缺什么 (45 s): Claude Code adds the Read/Edit/Bash tools, permissions, compaction, subagents; episode 2 adds tools. Recap table, closing question.

Blocker for the real run: no ANTHROPIC_API_KEY in this environment, and the anthropic Python package is not installed (Python 3.9.6).
