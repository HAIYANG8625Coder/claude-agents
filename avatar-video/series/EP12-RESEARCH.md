# Episode 12 research: testing and debugging an agent (official sources only; read 2026-11-21)

Sources, all read through fetch agents: (1) Anthropic Engineering, "Demystifying evals for AI agents", published 2026-01-09 (anthropic.com/engineering/demystifying-evals-for-ai-agents), full article. (2) Claude Code docs: headless (`claude -p`), costs, troubleshooting, debug-your-config, sessions, and the CLI reference (the CLI reference fetch was cut at 39,942 of 52,984 characters, so entries after `--restricted`, including `--verbose`, `--safe-mode`, `--resume`, are from a summary and must be re-checked on the page before they go on screen). Not read: hooks debugging, agent-sdk cost tracking, agent view. Quotes are short; the rest is paraphrase.

## Anthropic: how to evaluate an agent
- Words: task (one test with inputs and success criteria), trial (one attempt; run several because outputs vary), grader (logic that scores something; a task can have several checks), transcript / trace / trajectory (the complete record of a trial; for the API it is the full messages array), outcome (the final state of the environment, e.g. a reservation row in a database, not the sentence "your flight is booked"), evaluation harness (runs the tasks, records every step, grades, aggregates), agent harness (what makes a model an agent). "Evaluating an agent" means the harness and the model together.
- Grader kinds: code-based (string match, tests, outcome checks, tool-call checks, transcript metrics: fast, cheap, objective, repeatable, but brittle to valid variations); model-based (rubrics: flexible but non-deterministic, costs more, needs calibration against humans); human (gold standard, slow, expensive). Advice: deterministic graders where possible, an LLM grader where needed, humans sparingly. Grade "what the agent produced, not the path it took"; do not check an exact tool order. Give partial credit on multi-part tasks.
- Size: "20-50 simple tasks drawn from real failures is a great start"; early on effect sizes are large, so small samples are enough; start early. Good task: two experts reach the same verdict independently; keep a reference solution that passes every grader. A 0% pass rate over many trials most often means a broken task or grader, not a weak agent (example: a task that omitted a required file path).
- Balanced sets: test when a behavior should happen and when it should not.
- Trials: success varies from run to run. pass@k = at least one success in k tries (goes up with k); pass^k = all k succeed (goes down with k). Example: 75% per trial gives 0.75^3 ≈ 42% for pass^3.
- Read transcripts: "You won't know if your graders are working well unless you read the transcripts and grades from many trials." A failure should seem fair; do not trust a score before someone reads transcripts. Example: a model "failed" a flight task by finding a policy loophole that was better for the user; one benchmark score went from 42% to about 95% after fixing rigid graders, vague specs and unreproducible tasks.
- Isolation: each trial starts from a clean environment; leftover files and shared state cause correlated failures, and in one case the model gained an unfair advantage by reading git history from earlier trials.
- Saturation: an eval at 100% "tracks regressions but provides no signal for improvement". Capability evals start low; regression evals sit near 100%.
- The article does NOT say "do not grade only the final answer"; the closest is: grade the outcome, then also the transcript. Do not attribute that sentence to it.

## Claude Code: what you can read after a run
- `claude -p` (print mode): exit code 0 on success; `--output-format json` returns the result text, session ID, usage and a cost (`total_cost_usd`); `stream-json` (with `--verbose`) gives one JSON event per line and ends with a `result` message. The page does NOT list `num_turns`, `is_error` or the usage fields.
- Caps: `--max-turns` (print mode only, no limit by default), `--max-budget-usd` (estimated spend; can overshoot; subagent spend counts).
- `system/init` lists model, tools and MCP servers; `permission_denials` lists refused tool calls (with permission prompts off).
- Cost is an estimate computed locally from token counts at list price; `/usage` shows it with input, output, cache read and cache write per model; `/context` shows what fills the window.
- Transcripts: `~/.claude/projects/<project>/<session-id>.jsonl` (project = the working directory with non-alphanumerics replaced by `-`). The docs warn: "The entry format is internal to Claude Code and changes between versions"; use `/export` or the JSON and hook interfaces instead. Kept 30 days by default (`cleanupPeriodDays`); `--no-session-persistence` turns saving off in `-p`.
- Debug: `claude --debug` with category filters, `--debug-file <path>`, `/debug`, `/doctor`, `claude doctor`, `/mcp`, `/hooks`, `/permissions`, `/status`. `--safe-mode` (summary only) starts with customizations off: if the problem disappears, one of the turned-off things caused it.
- The docs describe no test harness for your own tasks. Costs page tip: put test cases or expected output in the prompt so Claude can check its own work.

## What this means for our version (to confirm by running it)
- Every earlier episode already counted something (turns, tokens read, tool log). Ep 12 turns that into one reusable harness: fixed tasks, a clean temp copy per trial, the full messages saved as JSON, a code grader on the outcome (files, state), then a table of pass rate, turns and tokens.
- One change at a time, several trials per task, read at least one failed trace.

## Verified on the CLI reference page (read in full 2026-11-21, code.claude.com/docs/en/cli-reference)
These replace the earlier "from a summary" note; the whole page (52,984 characters) was read.
- `--verbose`: "Enable verbose logging, shows full turn-by-turn output. Overrides the `viewMode` setting for this session".
- `--safe-mode`: starts with all customizations disabled (CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands and agents, auto memory and more); auth, model, built-in tools and permissions still work, unlike `--bare`.
- `--resume` / `-r`: resume a session by ID or name, or pick from a list. `--continue` / `-c`: latest conversation in the directory; skips `claude -p` sessions unless you pass `-p`.
- `--debug`: debug mode with optional category filter, e.g. `--debug='mcp,startup'` (filter only works in the `=` form). `--debug-file <path>` writes the log to a file.
- `--max-turns`: "print mode only. No limit by default." `--max-budget-usd`: stops at estimated spend (client-side estimate, print mode only).
- `--output-format`: `text`, `json`, `stream-json`. `--include-hook-events` (needs stream-json) adds hook events. `--no-session-persistence`: print mode only, session not saved.
- `--restricted`: "Intended for evaluation harnesses". `--bare`: minimal start for scripted calls.
- There is no top-level `--dry-run`.
Still unread: hooks debugging, agent-sdk cost tracking, agent view.
