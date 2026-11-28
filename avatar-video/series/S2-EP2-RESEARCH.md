# Series 2 episode 2 research: a policy nobody can switch off (official sources; read 2026-11-28)

Sources (code.claude.com/docs/en/, fetched by a web-fetch agent that quoted them): permissions, settings, settings-reference, managed-settings, admin-setup, server-managed-settings, hooks, security, permission-modes, agent-sdk/permissions. Quotes below were reported as verbatim. Check any quote on the page before it goes on screen.

## How rules are judged (permissions)
- "Rules are evaluated in order: deny, then ask, then allow."
- "An allow rule can't carve an exception out of a deny rule."
- "If a tool is denied at any level, no other level can allow it."
- "Permission rules are enforced by Claude Code, not by the model."

## The company layer (permissions, settings, managed-settings, admin-setup)
- "with managed settings highest: no other level, including command line arguments, can override a managed permission rule."
- Lists merge: developers can extend managed allow and deny lists, not remove from them (admin-setup).
- `allowManagedPermissionRulesOnly`: "Make managed settings the only settings source of permission rules. Claude Code then ignores `allow`, `ask`, and `deny` rules in user, project, local, and `--settings` files" (settings-reference). **Ours differs:** we ignore only their allow.
- `permissions.disableBypassPermissionsMode: "disable"`: nobody can enter bypass mode; works from any scope, typically set in managed settings.
- File paths: macOS `/Library/Application Support/ClaudeCode/managed-settings.json`; Linux and WSL `/etc/claude-code/managed-settings.json`. Also MDM or registry, and server-managed from the console.

## Where it stops (managed-settings, server-managed-settings)
- "a developer who is an administrator on the machine can edit the managed source itself"
- "managed settings bind Claude Code only."
- Server-managed: "a client-side control, not a security boundary." If the fetch fails, Claude Code by default goes on (with cached settings if it has them); `forceRemoteSettingsRefresh` makes it refuse to start.

## What a repository can bring (permissions, "What runs before you trust a folder")
- Under `claude -p` or the SDK in a folder never trusted: **hooks in settings files: "Used"**. `permissions.allow` in `.claude/settings.json`: "Not used. Claude Code prints a `this workspace has not been trusted` warning to stderr".
- "`deny` and `ask` rules aren't affected, since they only restrict."
- Managed `allowManagedHooksOnly` blocks user, project, local and plugin hooks (hooks page).

## Limits of the rules themselves (permissions)
- "a deny or ask rule covers the invocation Claude usually produces and isn't a security boundary around the program."
- "Bash permission patterns that try to constrain command arguments are fragile."
- Read deny rules reach Grep and Glob as a "best-effort attempt".
- "They also don't apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself."
- "For filesystem and network enforcement that doesn't depend on the command text, use sandboxing."
- Same section, after the sentence about subprocesses: "For OS-level enforcement on sandboxed shell commands, enable the sandbox and turn off the unsandboxed retry."
- Protected paths: writes to `.git` and `.claude` still prompt in accept-edits mode; only bypass mode skips that (permissions warning, permission-modes).

## Trust dialog and client-side limits (verbatim, reported by the web-fetch agent)
- security: "Claude Code shows the workspace trust dialog when you start it in a folder you haven't trusted"; "A `-p` session shows neither prompt."
- permissions: "Claude Code shows the trust dialog in interactive terminal sessions, but not in `claude -p` or SDK sessions."
- server-managed-settings: "Server-managed settings provide centralized policy enforcement, but they operate as a client-side control, not a security boundary." and "A user who can run a modified client can bypass any client-side control."

## Not read or not confirmed
- Whether the agent itself is stopped from editing managed settings files: no statement found.
- Part of the hooks page and of managed-settings were only available as summaries; nothing above relies on those.

## Our own runs (done, `ep02/`, 2026-11-28)
40 trials on DeepSeek flash, 0 failed requests; numbers in `ep02/demo/facts.json`, table in `ep02/README.md`.
