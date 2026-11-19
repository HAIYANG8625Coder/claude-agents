# Episode 8 research: hooks (official sources only; read 2026-11-19)

Sources: HG = code.claude.com/docs/en/hooks-guide (read through a fetch agent: 40,000 of 66,874 characters verbatim, the rest as a model-written summary); HR = code.claude.com/docs/en/hooks (reference: 39,950 of 294,332 characters verbatim, the rest summary or unread). Points marked [summary] came back as a model-written summary and must be re-checked before they go on screen. The "Security considerations" section was not read in either page.

## What hooks are (HG intro, verbatim)
- "Hooks are user-defined shell commands. Claude Code runs them at specific points in its lifecycle, which gives you deterministic control: certain actions always happen rather than relying on the LLM to choose to run them."

## Events (HR, "Hook lifecycle", paraphrased one-liners)
- Tool events: PreToolUse (before a tool call executes, can block it), PostToolUse (after a call succeeds), PostToolUseFailure, PostToolBatch, PermissionRequest, PermissionDenied.
- Session / prompt: SessionStart, SessionEnd, UserPromptSubmit, Stop (Claude finishes responding), StopFailure, Notification.
- Others: SubagentStart / SubagentStop, TaskCreated / TaskCompleted, PreCompact / PostCompact, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, WorktreeCreate / WorktreeRemove, and more. (More than 25 events in total; we build two.)

## How a hook runs
- Input (HG, verbatim): "When an event fires, Claude Code passes event-specific data as JSON to your script's stdin." PreToolUse gets `tool_name` and `tool_input` (HR example: `{ "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" } }`).
- Exit 0 (HG, verbatim): "if you exit 0 from a `PreToolUse` hook, the tool call still goes through the normal permission flow, because exit 0 doesn't approve it." (HR, verbatim: "The hook can deny the call, but staying silent doesn't approve it.")
- Exit 2 (HG, verbatim): "write a reason to stderr." Some events cannot be blocked ("for `SessionStart` and others, exit 2 shows stderr to the user and execution continues").
- Other exit codes (HG, verbatim): "With an exit code besides 0 and 2 and no valid JSON output, the action proceeds on most events."
- JSON alternative (HG, verbatim): "exit 0 and print a JSON object to stdout instead"; one approach per hook. HR example: `permissionDecision: "deny"` with `permissionDecisionReason`. [summary] allow / deny / ask / defer.
- [summary] PostToolUse cannot undo an action, the tool has already run.
- Timeouts (HR verbatim): defaults 600 s for command, http and mcp_tool hooks; 30 for prompt; 60 for agent. Lowered to 30 on UserPromptSubmit and two model-switch events, 10 on MessageDisplay.
- Several matching hooks (HR, verbatim): "When an event fires, its matching hooks run in parallel." (HG) "Don't rely on one hook's `deny` to suppress side effects in another hook."
- Hook types (HG, verbatim list): command (default), http, mcp_tool, prompt, agent (experimental).
- Matchers (HR, "Matcher patterns"): on tool name for tool events; `Edit|Write`, `Bash`, `mcp__.*`; empty or `*` matches all. Warning (HG): leaving the matcher empty on a permission hook "would auto-approve every tool permission prompt, including file writes and shell commands." `Bash`-only matcher misses file changes made through shell commands.
- Where configured (HG/HR, verbatim table): `~/.claude/settings.json` (all projects, local), `.claude/settings.json` (project, shareable), `.claude/settings.local.json` (project, not shared), managed policy settings, plugin `hooks/hooks.json`, skill and subagent frontmatter. [summary] `/hooks` browses them; `"disableAllHooks": true` turns them off.
- HR verbatim: "Handlers run in the current directory with Claude Code's environment." (so a hook runs with your own permissions; security section not read.)

## Use cases the guide lists (HG, "What you can automate")
Get notified when Claude needs input; auto-format code after edits (PostToolUse on `Edit|Write`); block edits to protected files (PreToolUse, exit code 2); re-inject context after compaction (SessionStart, `compact`); audit configuration changes; reload the environment when files change; auto-approve specific permission prompts. [summary] logging Bash commands, cleanup on SessionEnd.

## Pitfalls the docs name
- Output not starting with `{` can mean shell-profile output corrupts JSON [summary].
- A Stop hook that keeps blocking is overridden after eight times in a row [summary]; check `stop_hook_active`.
- Not read: the security section; the order hooks merge in; full allow/ask/defer semantics.

## Ours (agent-from-scratch/ep08)
- `Hooks` class in `agent.py`: entries `{event, matcher, command}` from `.agent/hooks.json`; the matcher is a full-match regular expression on the tool name; the command gets the event as JSON on stdin; exit 0 = no objection, exit 2 = block (before) or a note to the model (after, the call already ran), any other code or a timeout = logged, the tool still runs; matching hooks run one by one (Claude Code runs them in parallel). Our timeout is 10 s (Claude Code's default is 600 s). A before-hook runs before the permission check and its block beats an allow rule; our hooks cover read_file, grep, run_bash and edit_file.
- Tests: `python3 test_hooks.py` (7 checks, no key).
