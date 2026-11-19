# Episode 9 research: memory between sessions (official source only; read 2026-11-20)

Source: code.claude.com/docs/en/memory, read through a fetch agent: the WHOLE page, verbatim, in two fetches (characters 0 to 55,393). Nothing below rests on a summary. (Hooks pages in ep 8 were partly summary; this one is not.)

## Two kinds of memory ("CLAUDE.md vs auto memory" table)
- CLAUDE.md files: who writes it: "You". Contents: "Instructions and rules". Scope: project, user or org. Loaded: every session.
- Auto memory: who writes it: "Claude". Contents: "Learnings and patterns". Scope: per repository, shared across worktrees. Loaded: "Every session (first 200 lines or 25KB)".
- The page says both are "context, not enforced configuration". CLAUDE.md is "delivered as a user message after the system prompt", and "there's no guarantee of strict compliance, especially for vague or conflicting instructions".

## Where they live and what loads
- CLAUDE.md: `~/.claude/CLAUDE.md` (all your projects), `./CLAUDE.md` or `./.claude/CLAUDE.md` (project), `./CLAUDE.local.md` (personal, project specific), managed policy. Advice: "under 200 lines per CLAUDE.md file". Project-root CLAUDE.md "survives compaction: after /compact, Claude re-reads it from disk and re-injects it". Subdirectory CLAUDE.md files "load on demand".
- Auto memory: `~/.claude/projects/<project>/memory/`, holds `MEMORY.md` plus one topic file per memory (`user_role.md`, `feedback_testing.md` are the page's examples). "Machine-local". One directory per git repository.
- What loads at the start: "The first 200 lines of MEMORY.md, or the first 25KB, whichever comes first"; content beyond that "is not loaded at session start". "Claude Code doesn't load topic files ... at startup": Claude reads them "on demand using its standard file tools". Subagents do not get the main conversation's auto memory.

## How auto memory is written
- Four types, a `type` frontmatter field: user, feedback, project, reference.
- Claude "skips anything it can derive from the codebase, such as architecture, file paths, or debugging fixes", anything CLAUDE.md already says, and "doesn't save something every session". It saves what "would be useful in a future conversation".
- On request: "When you ask Claude to remember something, like 'always use pnpm, not npm'..., Claude saves it to auto memory." Ask "add this to CLAUDE.md" to put it there instead.
- `/memory` lists the memory files, toggles auto memory (saved as `autoMemoryEnabled` in `~/.claude/settings.json`) and opens the folder. On by default in local sessions. "Auto memory files are plain markdown you can edit or delete at any time."
- Limit handling: after a write to MEMORY.md, near the limit Claude Code tells Claude to "keep one line per entry, move detail into topic files, and merge or drop stale entries". Over the limit the write succeeds, but "everything past the limit is dropped on the next load". It records a `modified` timestamp when a note has frontmatter. Messages such as "Saved 2 memories" and "Recalled 2 memories" appear in the interface.

## Advice and pitfalls on the page
- Specific beats vague: "'Use 2-space indentation' works better than 'format code nicely.'" Conflicting files: "Claude may pick one arbitrarily."
- Must-happen steps: use a hook, because hooks "apply regardless of what Claude decides to do" (ties to ep 8).
- Instructions given only in the conversation can disappear; fix: "Add conversation-only instructions to CLAUDE.md to make them persist."
- Stale memories: the page's guidance is the `modified` timestamp and the "merge or drop stale entries" reminder; review with /memory. No guidance on secrets was found on the page.

## Ours (agent-from-scratch/ep09)
- Memory folder `AGENT_MEMORY` or `~/.agent/projects/<folder>-<hash>/memory`; `memory_write(name, type, description, content)` writes one note (frontmatter: name, description, type, modified) and one index line in `MEMORY.md`; `memory_forget(name)` deletes both; the index (first 200 lines or 25 KB, the documented limits) goes into the first message, so it survives compaction like CLAUDE.md; notes are opened on demand with `read_file`; the system prompt rule: save what the user said that you cannot look up again, not code facts; an optional rule: "notes can be out of date, check before you rely on them". Memory tools are offered in plan mode too (a note is not a project edit); a bug we hit: they were hidden there at first.
- Not built: auto-saving without being asked in the main flow beyond the prompt rule, an offline cleanup pass, /memory, CLAUDE.local.md, rules folders.
- Tests: `python3 test_memory.py` (8 checks, no key).
