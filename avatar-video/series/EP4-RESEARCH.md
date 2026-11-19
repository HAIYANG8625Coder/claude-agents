# Episode 4 research (official docs only; read 2026-11-17)

Sources: P = https://code.claude.com/docs/en/permissions ; M = https://code.claude.com/docs/en/permission-modes ; S = https://code.claude.com/docs/en/security ; B = https://code.claude.com/docs/en/best-practices ; T = https://code.claude.com/docs/en/settings
(The page text was read in part verbatim and in part through a model summary; items marked (summary) come from the summary. The sandboxing page, the classifier internals and the trust-folder section were not read.)

## Modes (M, "Available modes")
- default (shown as "Manual"): runs only reads without asking. P also says it prompts on first use of each tool. The two descriptions do not match exactly, so we say "reads run without asking; edits and commands ask".
- acceptEdits: reads, file edits and common filesystem commands (mkdir, touch, mv, cp...) run without asking, for paths in the working directory.
- plan: Claude reads and explores; edits stay blocked until you approve a plan.
- auto: a classifier model reviews actions before they run. "Auto mode reduces permission prompts but does not guarantee safety."
- dontAsk: auto-denies anything that would otherwise prompt; reads and tools pre-approved by allow rules still run (summary). For CI and scripts.
- bypassPermissions: everything runs without asking; deny rules still block; allow rules have no effect; only for isolated environments (containers or VMs).
- Default mode in the terminal is auto from v2.1.283; `claude -p` and the Agent SDK default to Manual. Say the version when quoting.

## Rules (P, "Permission rule syntax")
- Format: `Tool` or `Tool(specifier)`. A bare tool name matches all uses.
- Examples on the page: `Bash(npm run build)`, `Read(./.env)`, `WebFetch(domain:example.com)`; wildcards `Bash(npm run *)`, `Bash(git commit *)`.
- "A `*` in a Bash rule matches any text, including spaces." Put the `*` after the subcommand: `Bash(git log *)` allows only git log; `Bash(git *)` allows every git command.
- Trailing space matters: `Bash(ls *)` matches `ls` but not `lsof`; `Bash(ls*)` matches `lsof`. `:*` is an equivalent older way to write a trailing wildcard.
- NOT in the docs: the example `Bash(npm run test:*)`. Do not use it.

## Order (P)
- "Rules are evaluated in order: deny, then ask, then allow. The first match in that order determines the outcome, and rule specificity doesn't change the order."
- A broad deny rule blocks every matching call, even one that also matches a narrower allow rule. A matching ask rule prompts even when a more specific allow rule matches.
- Compound commands: `Bash(safe-cmd *)` does not approve `safe-cmd && other-cmd`; every subcommand must be allowed. Separators: &&, ||, ;, |, |&, &, newlines. Deny and ask rules also apply inside subshells and command substitutions.
- Limit stated by the docs: a deny or ask rule "isn't a security boundary around the program" (for example `Bash(curl *)` does not stop `/usr/bin/curl` or `sh -c 'curl ...'`). Use the sandbox for OS-level enforcement.

## Defaults (P, "Permission system" table)
- Read-only tools (file reads, Grep): no approval, inside the working directory.
- Bash: approval required, except a built-in read-only set: ls, cat, echo, pwd, head, tail, grep, find, wc, which, diff, stat, du, cd, and read-only forms of git. The set cannot be configured.
- File edits: approval required; "Don't ask again" lasts until session end.
- Commands the parser cannot analyze prompt (S: "asks before running a Bash command it can't fully analyze"); unmatched commands require approval by default (S, fail closed).

## Settings layering (T, P)
- Files: user ~/.claude/settings.json; project .claude/settings.json; local .claude/settings.local.json; managed settings.
- "Claude Code combines the lists instead of picking one": permissions.allow is a union across files. If a tool is denied at any level, no other level can allow it (summary). deny and ask apply right away; project allow rules wait for the trust dialog.
- "Yes, and don't ask again" on a Bash command saves an allow rule to .claude/settings.local.json.

## Prompt injection and enforcement (S, P)
- Permission rules are enforced by Claude Code, not the model: instructions in the prompt or CLAUDE.md "don't change what Claude Code allows" (P note).
- S: in Manual mode sensitive operations need explicit approval; curl and wget are not auto-approved; WebFetch runs a separate model call over the page so Claude gets the answer, not the raw page.
- S: "no system is completely immune to all attacks". Advice: review suggested commands before approving; avoid piping untrusted content to Claude.
- A Bash command you approve can still write anywhere your user account can (S).

## Approval fatigue (S, B)
- S: "Prompt fatigue mitigation: Support for allowlisting frequently used safe commands per-user, per-codebase, or per-organization."
- B: in Manual mode "after the tenth prompt you start approving without reading". B: for a rule that cannot bend, use a hook or a deny rule. `/fewer-permission-prompts` adds common read-only commands to an allowlist.
- The phrase "approval fatigue" is not in the docs; the words are "prompt fatigue".
