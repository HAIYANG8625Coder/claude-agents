# Episode 13 research: putting it together (official sources only; read 2026-11-21)

Sources, read through fetch agents. Claude Code docs (code.claude.com/docs/en/): interactive-mode (78,662 chars, read in full), how-claude-code-works (19,967, full), checkpointing (9,499, full), sessions (34,732, full), commands (56,754: the first 39,947 verbatim, the part from `/rename` on is a model summary, so the command list may miss rows), security (15,325, full), headless (38,894, full), sandboxing (111,990: first 79,890 verbatim, last 32,100 summary), sub-agents (116,240: first 79,890 verbatim, last 36,350 summary). Anthropic Messages API streaming page (platform.claude.com/docs/en/build-with-claude/streaming, 53,327 chars: first 39,929 verbatim, last 13,398 summary). Not read: the Agent SDK streaming page, the status line page. Quotes short; the rest is paraphrase.

## A chat loop (what Claude Code does, interactive-mode / how-claude-code-works / sessions)
- The loop has three phases that blend together: "gather context, take action, verify results"; the user can interrupt at any point. `Esc` stops the current response or tool call and keeps work done so far. `Ctrl+C` interrupts a running operation; with nothing running the first Ctrl+C clears the prompt and a second exits. `Ctrl+D` exits on a second press within 800 ms.
- Input: line editing keys (Ctrl+A/E/K/U/W/Y), multiline with `\` + Enter or Ctrl+J, history per working directory (Up/Down), Ctrl+R reverse search, `!` runs a shell command and puts its output in the conversation, `@` completes file paths. Typing while Claude works queues the message.
- Sessions: every message, tool use and result is written to a plaintext JSONL file at `~/.claude/projects/<project>/<session-id>.jsonl`; the format is internal and may change. `claude --continue` (latest in this folder) and `claude --resume` (picker, or a name/ID) reopen it; a resumed session restores history, model, permission mode. Interrupted tool calls are not rerun; background tasks are not restored. `/branch` and `--fork-session` copy a session. Transcripts kept 30 days by default.
- Context: `/clear` starts a new conversation, `/compact [instructions]`, `/context`. Auto compaction.
- Checkpoints: each prompt that starts a turn creates one; only file-edit tool changes are tracked (not bash changes, not subagents, not outside edits); 100 most recent per session; `/rewind` (alias `/undo`) or Esc twice. "Not a replacement for git".
- Commands: `/` opens a menu; about 130 built-in commands. A command is only recognized at the start of a message. Some run at once while Claude works (`/status`, `/tasks`, `/usage`), others queue.
- Permission modes: Auto, Manual, Accept edits, Plan (Shift+Tab cycles). Task list with Ctrl+T (up to five shown). `/btw` side question that does not enter history. Background Bash with Ctrl+B. 

## Streaming (Anthropic Messages API streaming page)
- Event order: `message_start`, then per content block `content_block_start`, zero or more `content_block_delta`, `content_block_stop`, then one or more `message_delta` (stop_reason; usage there is cumulative), then `message_stop`. `ping` events can appear anywhere; an `error` event can come mid-stream (e.g. `overloaded_error`).
- Delta types: `text_delta` (text), `input_json_delta` (partial_json, for tool_use input), `thinking_delta`, `signature_delta`.
- A tool call arrives as `content_block_start` with `tool_use` (id, name, empty input), then `input_json_delta` pieces; accumulate and parse when the block stops. The final `input` is always an object.
- Python SDK: `with client.messages.stream(...) as stream:`; `stream.text_stream` yields text; `stream.get_final_message()` returns the same Message that `create()` returns. The page recommends streaming for large `max_tokens` to avoid HTTP timeouts.
- Claude Code CLI streaming (headless page): `--output-format stream-json --verbose --include-partial-messages` gives tokens as they are generated; the last line is a `result` message.
- Error recovery (summary part of the page): a mid-stream failure can be continued from the last text block; tool_use and thinking blocks cannot be partially recovered.

## What Claude Code has that our small Python agent does not (each item has a page)
1. OS-level Bash sandbox: Seatbelt on macOS, bubblewrap on Linux; writes limited to the working directory; network through a proxy with an allowed-domains list; off by default (sandboxing). Our permission gate only decides whether to run a command; it does not limit what a command can do once it runs.
2. Auto permission mode where a separate classifier model reviews actions; command-injection detection; fail-closed matching; WebFetch results pass through a separate model call (security).
3. Workspace trust dialog and approval of project MCP servers (security; we have neither).
4. Subagents as files with their own tools, model, permission mode, hooks, memory, worktree isolation; built-in Explore and Plan subagents; background subagents (sub-agents).
5. Checkpoints and `/rewind`; session picker, `--resume`, `/branch` (checkpointing, sessions).
6. Input editing, history, multiline, reverse search, image paste, Vim mode, Ctrl+Z (interactive-mode).
7. About 130 commands, a status line, managed (enterprise) settings, cloud and remote sessions (commands, security, sandboxing).
8. A streaming event protocol for scripting (`stream-json`, `system/init`, `api_retry`, `permission_denied`) (headless).
Not in this list: `text_stream` and `get_final_message` are Anthropic SDK features that any Python agent can use, and we use them.

## What this means for our version (to confirm by running it)
- ep 13 adds: a chat loop with a kept conversation, streamed text, a few slash commands, saving and resuming a session, and Ctrl+C that stops the current turn. All earlier parts (permissions, context, plan and todo, subagents, hooks, memory, always-on, MCP, skills) are switched on through one config.
- Open: the real test (multi-turn conversation kept vs fresh runs; streaming first-token time; resume) is not run yet.
