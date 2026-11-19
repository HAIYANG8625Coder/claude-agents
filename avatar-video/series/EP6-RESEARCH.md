# Episode 6 research: plans and task lists (official docs only; read 2026-11-18)

Sources: PM = code.claude.com/docs/en/permission-modes ; IM = /en/interactive-mode ; TR = /en/tools-reference ; BP = /en/best-practices ; HW = /en/how-claude-code-works ; CW = /en/common-workflows ; BEA = anthropic.com/engineering/building-effective-agents ; EH = anthropic.com/engineering/effective-harnesses-for-long-running-agents
(Read through a fetch agent. Quotes under 25 words are verbatim. Anything not marked is a paraphrase.)

## Plan mode (PM)
- Enter: "press `Shift+Tab` to cycle permission modes" (default, acceptEdits, plan). Or prefix one prompt with `/plan`, or start with `claude --permission-mode plan` (also CW). Status bar shows "plan mode on".
- What it does: "Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source."
- Edits "stay blocked until you approve the plan" (except interactive sessions with bypass permissions available).
- Shell commands in plan mode: depends on session (classifier review in auto mode, otherwise prompts for anything outside the built-in read-only set).
- Tools: EnterPlanMode "Switches to plan mode to design an approach before coding" (no permission needed); ExitPlanMode "Presents a plan for approval and exits plan mode" (permission required) (TR).
- Approval: "When the plan is ready, Claude presents it and asks how to proceed." Options: yes with auto mode (or auto-accept edits), yes and approve each edit manually, "No, keep planning" (stay in plan mode, say what to change).
- "Approving a plan exits plan mode and switches the session to the permission mode each approve option describes, so Claude starts editing."
- `Ctrl+G` opens the plan in your editor to edit it before Claude proceeds.
- Optional setting `showClearContextOnPlanAccept`: approve and clear the planning context.
- HW: Plan mode "explores and proposes a plan without editing your source files". Agentic loop = gather context, take action, verify results; they "blend together".

## Task list (IM, TR)
- IM: "The task list is Claude's to-do checklist: items Claude created to plan multi-step work, with indicators showing what's pending, in progress, or complete."
- `Ctrl+T` toggles it: "Show or hide Claude's to-do checklist in the status area." Shows up to five tasks at a time.
- Separate from `/tasks`, which lists running shells and subagents.
- Tasks persist across context compactions (IM). Shared list across sessions: `CLAUDE_CODE_TASK_LIST_ID=my-project claude` (stored in `~/.claude/tasks/`).
- Tools (TR, none need permission): TaskCreate "Creates a new task in the task list."; TaskGet; TaskList "Lists all tasks with their current status."; TaskUpdate "Updates task status, dependencies, details, or deletes tasks."; TodoWrite is the older single tool, "Disabled by default in favor of" the four.
- TR on newer models: "Claude keeps track of multi-step work without a written checklist." Task tools are on by default for some models; others need `CLAUDE_CODE_ENABLE_TODO_TOOLS=1`.
- Subagents have the task tools only when the session has them.

## Longer tasks (EH, paraphrase)
- Problem: "each new session begins with no memory of what came before."
- Fix: a feature list file (JSON, each entry has a `passes` flag; JSON chosen because models edit it less destructively than Markdown), a progress file, git commits. Agent works on one feature at a time and may only change `passes`.
- Failure modes named: "Claude declares victory on the entire project too early." and marking features done prematurely. Fix: verify before marking passing.
- BEA: agents "plan and operate independently" once the task is clear; recommends stopping conditions such as a maximum iteration count; transparency means "explicitly showing the agent's planning steps".
- BP: "Give Claude something it can run that comes back pass or fail."; "Does it know what done looks like?"

## Not found
Task field names and status enum names; TodoWrite input schema; plan file location (a summary mentioned `~/.claude/plans/` but it is unverified, do not use); an explicit allowed-tools list for plan mode; any "when to skip planning" advice in best practices.

## Our version (what episode 6 builds)
1. Plan mode: a mode flag. In plan mode only read-only tools exist (read_file, list_files, search) plus `submit_plan(plan)`, which shows the plan and waits for approval. Write tools are not offered, and are refused if called anyway. Approval switches to normal mode and puts the plan in the context.
2. Task list: a `todo_write(items)` tool with `pending / in_progress / done`; the list is printed each turn and appended to the model's view; rule: only one `in_progress`, mark done only after checking.
3. Real runs: a multi-step edit task in a sandbox (with tests that pass or fail), with and without task list and plan, repeated 3 times. Measure steps missed, false "done", turns.
