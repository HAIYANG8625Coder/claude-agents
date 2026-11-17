# Episode 3 research (official docs only; read 2026-11-17)

Sources: M = https://code.claude.com/docs/en/memory ; B = https://code.claude.com/docs/en/best-practices ; S = https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/system-prompts (redirect from docs.claude.com; page titled "Prompting best practices")

- S, "Give Claude a role": "Setting a role in the system prompt focuses Claude's behavior and tone for your use case." Example: `"system": "You are a helpful coding assistant specializing in Python."` is a top-level parameter next to model, max_tokens, messages.
- M, locations, in load order broad to specific: managed policy (macOS /Library/Application Support/ClaudeCode/CLAUDE.md, Linux /etc/claude-code/CLAUDE.md), user ~/.claude/CLAUDE.md, project ./CLAUDE.md or ./.claude/CLAUDE.md, local ./CLAUDE.local.md (add to .gitignore).
- M, "How CLAUDE.md files load": loads CLAUDE.md and CLAUDE.local.md from the working directory and every directory above it; ordered from the filesystem root down to the working directory; subdirectory files load "once Claude reads, writes, or edits another file in that subdirectory". All discovered files are concatenated into context rather than overriding each other.
- M, imports: `@path/to/import`, relative to the file containing it; max depth four hops.
- M, length: "target under 200 lines per CLAUDE.md file"; longer files "consume more context and reduce adherence". Imports do not reduce context cost.
- B, "Keep CLAUDE.md short": works best when it only holds what Claude couldn't work out from the code itself. Test: could it find this by reading the code? If yes, leave it out. Keep exact test/lint commands, misleading patterns, decisions not in the repo, anything corrected twice.
- M, "When to add": when Claude makes the same mistake a second time. Instructions "concrete enough to verify" ("Run npm test before committing" over "Test your changes"; "Use 2-space indentation" over "format code nicely").
- M, /init: "Run /init to generate a starting CLAUDE.md automatically"; if one exists it suggests improvements instead of overwriting.
- M: "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself."
- M: Claude treats CLAUDE.md as "context, not enforced configuration". B: "CLAUDE.md is for guidelines, and Claude is allowed to decide a guideline doesn't apply." Must-happen rules belong in hooks.
- M: check what loaded with `/context all`.

Our own measured results (ep03/demo/evals.txt, deepseek-flash, 3 runs per cell, one model, small sample):
- no notes: discount task rounds half up 2/3, docstring 3/3, integer result 3/3, "Done:" line 0/3; helper task file in helpers/ 0/3.
- with notes: discount 3/3 on every check incl. "Done:" line; helper task in helpers/ and works 3/3, "Done:" 3/3.
- First eval run found two problems: (1) max_tokens 1024 was too small (one run ended on max_tokens; raised to 2048), (2) the notes rule "new helper code goes in helpers/" also pulled the discount rounding helper into helpers/, and my check crashed with ModuleNotFoundError (check imported pricing without the folder on the path). Fixed the check to import like the project would.
- Real demo runs: ep03/demo/run-no-notes.txt (helper added into pricing.py, no docstring, no Done line, files: check.py, pricing.py) vs run-with-notes.txt (helpers/round_down_5.py + empty helpers/__init__.py, one-line docstring, a "Done:" line).
