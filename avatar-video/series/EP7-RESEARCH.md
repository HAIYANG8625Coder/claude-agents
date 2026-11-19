# Episode 7 research: subagents (official sources only; read 2026-11-19)

Sources: CC = code.claude.com/docs/en/sub-agents (read through a fetch agent; the page was cut at ~40k of 116k characters, so points marked [summary] came back as a model-written summary and must be re-checked before they go on screen) ; MA = anthropic.com/engineering/multi-agent-research-system (page text, published Jun 13, 2025, Anthropic engineering).

## Claude Code subagents (CC)
- Intro: "Subagents are specialized AI assistants that handle specific types of tasks." "Each subagent runs in its own context window." Claude Code "includes built-in subagents that Claude automatically uses when appropriate."
- What the parent gets: the subagent does the work in its own context "and returns only the summary" (intro). [summary] Non-fork subagents start fresh and don't see the conversation history.
- Use one "when a side task would flood your main conversation with search results, logs, or file contents you won't reference again." Define a custom one "when you keep spawning the same kind of worker with the same instructions."
- Built-ins (section Built-in subagents): Explore ("A fast, read-only agent optimized for searching and analyzing codebases", Write and Edit denied); Plan (research agent used in plan mode, read-only); general-purpose (all tools, for multi-step tasks that need exploration and action).
- Custom subagent = Markdown file with YAML frontmatter (body = system prompt). Only `name` and `description` required. Fields include `tools` (allowlist; if omitted it inherits all), `disallowedTools`, `model`, `permissionMode`, `maxTurns`. Locations by priority: managed settings, `--agents` flag, `.claude/agents/`, `~/.claude/agents/`, plugin `agents/`.
- Numbers: descriptions of non-built-in subagents over 15,000 tokens together trigger a startup warning; `name` max 256 chars. [summary] default 20 concurrent, spawn depth 3.
- Not read: default `maxTurns`, the full tool-restriction section, verbatim parallel guidance.

## Anthropic multi-agent research system (MA)
- Pattern: "an orchestrator-worker pattern", "a lead agent coordinates the process", "delegating to specialized subagents that operate in parallel". Subagents "act as intelligent filters", own context windows, condense "the most important tokens for the lead".
- Numbers (their internal research eval): Opus 4 lead + Sonnet 4 subagents "outperformed single-agent Claude Opus 4 by 90.2%". Token usage alone explained 80% of the variance on BrowseComp (three factors: 95%). Agents use about 4x the tokens of chat; multi-agent about 15x.
- Brief: each subagent needs "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." Vague brief ("research the semiconductor shortage") made subagents misread the task or run the same searches; 2 of 3 "duplicated work".
- Effort scaling: 1 agent / 3-10 tool calls for simple fact-finding; 2-4 subagents for comparisons; 10+ for complex research; early agents spawned 50 subagents for simple queries (a failure).
- Limits: "these architectures burn through tokens fast"; worth it only when the task value pays for it; a poor fit when agents must share context or have many dependencies; most coding tasks have "fewer truly parallelizable tasks than research"; "LLM agents are not yet great at coordinating and delegating to other agents in real time."

## Ours (to build in agent-from-scratch/ep07, then measure)
- run_subagent(task): a fresh messages list, fewer tools (read-only), a max-turns limit, returns the last text only. Sequential, no parallelism (the post's parallelism is not built).
- Real test: not run yet.
