# Episode 5 research: context (official docs and Anthropic posts only; read 2026-11-18)

Sources: W = https://code.claude.com/docs/en/context-window ; H = /en/how-claude-code-works ; C = /en/costs ; M = /en/memory ; K = /en/commands ; MC = /en/model-config ; E = https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09-29) ; CE = https://platform.claude.com/docs/en/build-with-claude/context-editing ; T = .../token-counting ; CW = .../context-windows
(Read through a fetch agent: short verbatim quotes are exact; items marked (summary) come from a model summary of the unread part of a long page. Verify (summary) items before showing them on screen.)

## What fills the window
- H: "Claude's context window holds your conversation history, file contents, command outputs, CLAUDE.md, auto memory, loaded skills, and system instructions."
- W "Before you type anything" (the page says illustrative): system prompt 4,200 tokens; auto memory 680; environment 280; MCP tool names 120; skill descriptions 450; user CLAUDE.md 320; project CLAUDE.md 1,800. Example session: 22,225 tokens before /compact, 17,095 after.
- CW: everything counts: system prompt, all messages, tool results, tool definitions, output. "Cached prompt prefixes still occupy the context window."
- CW: window "up to 1M tokens, depending on the model"; older models 200k. Over the window: 400 `invalid_request_error` ("prompt is too long").

## Why it matters
- E and CW: "context rot": as tokens grow, recall and accuracy degrade. E: "Context, therefore, must be treated as a finite resource with diminishing marginal returns." It is "a performance gradient rather than a hard cliff". Goal: "the smallest possible set of high-signal tokens". No benchmark numbers on the page.
- W: old conversation "crowds out the files you need next and costs tokens on every message."
- H/C: "A session that's collected three unrelated tasks re-reads all three on every turn of the fourth." (best-practices)

## Seeing it: /context
- K: `/context [all]`: "Visualize current context usage as a colored grid. Shows optimization suggestions for context-heavy tools, memory bloat, and capacity warnings."

## Counting tokens
- T: `POST https://api.anthropic.com/v1/messages/count_tokens`, same body as Messages (model, system, messages, tools); response `{ "input_tokens": 14 }`. "The token count is an estimate." Free, rate-limited separately.
- T: Claude 4.7 and later use a newer tokenizer that gives "approximately 30 percent more tokens" for the same text, so recount per model.
- Our version: every Messages response carries `usage.input_tokens` for the request just sent: that is the count of the whole window at that turn. Plus a rough `chars / 4` estimate for when we need a number before calling (our approximation, not from the docs).

## Automatic compaction in Claude Code
- W: "Claude Code compacts automatically as you approach the limit, so a full context window doesn't end your session."
- MC (summary): models with a 200K window compact "at the 200K boundary"; 1M-native models (Fable, Sonnet 5 and later, Haiku 5.5, Opus 4.7 and later) "compact before the window fills, at about 967K tokens by default". Settings: `/autocompact <tokens>`, `autoCompactWindow`, `--autocompact`, env `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (range 100K to 1M). No percentage or buffer is documented. Do not quote 96.7% as documented.
- H: "The summary keeps your requests and key code snippets, but detailed instructions from early in the conversation may be lost." The summary format is not documented.
- H: if one file or tool output is so large that context refills after each summary, Claude Code "stops auto-compacting after a few attempts and shows an error".
- K: `/compact [instructions]`: "Free up context by summarizing the conversation so far. Optionally pass focus instructions for the summary." W: "The summary keeps what you choose instead of what the automatic pass guesses is important." C: `/compact` "reads the conversation it summarizes, so compacting a large context is itself a large request."
- C/H: a "Compact instructions" section in CLAUDE.md steers what is kept.
- K: `/clear` = new conversation, empty context, project memory kept. `/compact` frees context and continues the same conversation.

## What survives compaction (W table)
- System prompt and output style: still apply. Project-root CLAUDE.md and unscoped rules: "Re-injected from disk." Auto memory: re-injected from disk. Plan from plan mode: re-injected.
- Files Claude read or edited: "Claude Code re-reads up to five, most recently modified first." A file over 5,000 tokens comes back as a path reference. Invoked skill bodies: 5,000 tokens each, 25,000 total.
- M (summary): instructions given only in conversation are lost; fix: put them in CLAUDE.md.
- E: compaction "preserves architectural decisions, unresolved bugs, and implementation details" and the agent continues with the summary plus "the five most recently accessed files." Tune by "maximizing recall" first, then precision.

## Lighter than compaction: clear old tool results
- E: "One of the safest lightest touch forms of compaction is tool result clearing." Why: "once a tool has been called deep in the message history, why would the agent need to see the raw result again?"
- CE: API beta `context-management-2025-06-27`; strategy `clear_tool_uses_20250919` "clears tool results when conversation context grows beyond your configured threshold", oldest first, replaced by placeholder text. Example values on the page (not defaults): trigger 30,000 input tokens, keep 3 tool uses, clear_at_least 5,000. "Your client application maintains the full, unmodified conversation history." Clearing invalidates the cached prefix. CE also says server-side compaction is the primary strategy for most uses.

## Keeping it small (advice)
- W: `/clear` between unrelated tasks. C: CLAUDE.md under 200 lines; workflow instructions into skills (load on demand); delegate verbose output to subagents (W: "Only the summary and a small metadata trailer come back."; E: subagents use tens of thousands of tokens and return "often 1,000-2,000 tokens"); hooks to filter output (C example: keep the last 100 lines of test output).
- No documented general tool-output size limit for Claude Code.

## Not found
Summary format; the full /context output; any compaction percentage; a built-in tool-output limit.

## Our version (what episode 5 builds)
1. Count: `usage.input_tokens` from each response (real) and `chars/4` (estimate). Print it every turn.
2. Trim: replace old tool results (all but the latest N) with a short placeholder; keep the tool_use blocks so the pairs stay valid.
3. Compact: when the count passes a threshold, ask the model to summarize the older turns, with a fixed prompt that must keep the task, decisions, files touched, open problems; replace old turns with that summary; keep the last few turns whole; re-load the notes file (like CLAUDE.md after a compact).
4. Show: tokens per turn over a long run, with and without.
