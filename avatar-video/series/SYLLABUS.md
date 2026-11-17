# Syllabus: build your own agent (a Claude Code-style agent, in Python)

One agent, built a piece at a time. Every episode is one video (about 7 to 8 minutes), one folder in this repo and one commit, so you can check out a single step. Claude Code behavior in the videos comes from its official documentation, never from its source code; "our version" is always the small one.

**You need:** Python 3.9+, a terminal, and an API key for a model that speaks Anthropic's message format (Claude, or DeepSeek through its Anthropic-compatible endpoint). A Claude Pro subscription does not include an API key.
**You do not need:** any framework. The whole agent is plain Python plus one SDK.
**By the end:** a working command-line coding agent of about 500 lines that reads and edits files, runs commands with your permission, manages its own context, delegates to subagents and remembers things between sessions.

Every published episode has a full article with the code, real run output, diagrams and inline citations: see the **Articles** table in the [README](README.md).

## The big picture

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/img/overview-dark.svg">
  <img alt="Architecture of the finished agent: the REPL feeds the agent loop, which talks to the model API; the system prompt, notes and context manager feed the loop; tool requests pass the permission gate before the tools run; hooks, MCP, memory and subagents are side paths." src="docs/img/overview.svg">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/img/series-map-dark.svg">
  <img alt="Course map: A core (episodes 1-3), B trust and limits (4-5), C working at scale (6-8), D beyond one session (9-11), E ship it (12-13)." src="docs/img/series-map.svg">
</picture>

Each part has its own short introduction with a diagram: [A core](docs/part-a-core.md) · [B trust and limits](docs/part-b-trust.md) · [C working at scale](docs/part-c-scale.md) · [D beyond one session](docs/part-d-beyond-one-session.md) · [E ship it](docs/part-e-ship-it.md).

| Part | Episodes | You learn |
|---|---|---|
| A. The core | 1 to 3 | the loop, tools, the system prompt and notes file |
| B. Trust and limits | 4 to 5 | permissions, context |
| C. Working at scale | 6 to 8 | planning, subagents, hooks |
| D. Beyond one session | 9 to 11 | memory, always-on, extending with MCP |
| E. Ship it | 12 to 13 | testing and debugging an agent, the finished CLI |

## Part A. The core
**Ep 1 · The loop** (published) `ep01`
Goal: see that an agent is a loop. Build: `run()` with one tool, `stop_reason`, a max-turns guard. Claude Code: three phases (gather context, take action, verify), the loop ends when there is no tool call. Pitfalls: not appending the tool result, no turn limit, thinking the model executes code. Check: `python3 ep01/test_loop.py`.

**Ep 2 · Tools** `ep02`
Goal: give the loop real hands. Build: `read_file`, `grep`, `run_bash`, `edit_file` (exact-string replace, why it beats rewriting a whole file), tool descriptions as prompts, output truncation, errors returned as results. Claude Code: its built-in Read, Edit, Write and Bash tools (documented names and which ones ask first). Pitfalls: vague descriptions, 50,000-line outputs, crashing on an exception.

**Ep 3 · The system prompt and the notes file** `ep03`
Goal: steer the agent without retraining it. Build: a short system prompt (role, rules, environment), a project notes file loaded at start, a tiny set of fixed test tasks to compare before and after. Claude Code: CLAUDE.md locations and loading, keeping it short. Pitfalls: long prompts that dilute, rules the agent cannot check, changing the prompt without re-testing.

## Part B. Trust and limits
**Ep 4 · Permissions** `ep04`
Goal: let it act without letting it run wild. Build: a gate between "the model asked" and "we run it": allow, ask, deny rules by pattern, a read-only mode, a confirm prompt. Claude Code: permission modes and the rule order deny, then ask, then allow. Pitfalls: approval fatigue (fix: allow lists), prompt injection (a file that says "ignore your rules" is data, not an instruction).

**Ep 5 · Context** `ep05`
Goal: keep long sessions working. Build: a token counter, output trimming, compaction (summarize old turns, keep recent ones and the task list), a chart of context size over a long run. Claude Code: automatic compaction and what is re-loaded afterwards. Pitfalls: summaries that lose decisions, compacting too late.

## Part C. Working at scale
**Ep 6 · Plans and task lists** `ep06`
Goal: make long tasks visible. Build: a plan-only mode (read-only tools) and a task list tool the model updates. Claude Code: plan mode and its task list. Pitfalls: plans that are never checked off, tasks too big to verify.

**Ep 7 · Subagents** `ep07`
Goal: protect the main context. Build: `run_subagent(task)` starting a fresh loop with its own messages and fewer tools, returning only the final text. Claude Code: subagents with their own context window; the parent sees only the result. Pitfalls: a vague brief (the subagent cannot see your chat), too many tools, no turn limit.

**Ep 8 · Hooks** `ep08`
Goal: run your own code at fixed points. Build: before-tool and after-tool hook points that can allow, block or log. Claude Code: its hook events (for example before and after a tool call) and where hooks are configured. Pitfalls: hooks that slow every call, a blocking hook with no message.

## Part D. Beyond one session
**Ep 9 · Memory** `ep09`
Goal: remember what is worth remembering. Build: a notes folder, write only what cannot be looked up again, load an index at the start (Claude Code loads the first 200 lines or 25 KB of its memory index), an optional offline cleanup pass that checks notes against the transcript. Pairs with the "Components of agent memory" video. Pitfalls: remembering everything, wrong notes believed forever.

**Ep 10 · Always on** `ep10`
Goal: an agent that works while you are away. Build: an inbox queue, a timer, the loop as a daemon, an outbox to a chat app, and what the agent may do when nobody can approve. Pairs with the "always-on agents" video. Pitfalls: two events at once, secrets within reach.

**Ep 11 · Extending with MCP and skills** `ep11`
Goal: add tools you did not write. Build: a minimal client that lists and calls tools from an MCP server, and a folder of skill files loaded on demand. Claude Code: MCP servers and skills as documented. Pitfalls: trusting a tool's description, loading every skill up front.

## Part E. Ship it
**Ep 12 · Testing and debugging an agent** `ep12`
Goal: know when a change helped. Build: 3 to 5 fixed tasks, a saved trace of every message, turns and tokens per task, one change at a time. Pitfalls: judging by one run, reading only the final answer.

**Ep 13 · Putting it together** `ep13`
Goal: one finished command-line agent. Build: a chat loop (REPL) with streaming output, all earlier parts wired in, a README with the architecture diagram. Closing: what Claude Code has that ours does not, and where to go next.

## Rules for every episode
- The code is tested before the script is written, so every run on screen is real.
- Each video follows the same six parts: the problem, the idea, how Claude Code does it (documented), the code, a real run, the pitfalls and a one-line takeaway.
- An architecture diagram and a "save this" summary card in each episode.
- Keys come from environment variables only and never appear in code or video.
