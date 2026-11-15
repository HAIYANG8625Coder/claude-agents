# Working in this repo

This repo is a Claude Code plugin marketplace. Read "Repository layout" and "Rules for this repo" in README.md before you add or move a skill, subagent, plugin or always-on agent, and follow them. The short version:

- A new skill goes in `plugins/<plugin>/skills/<name>/SKILL.md`, and a new subagent in `plugins/<plugin>/agents/<name>.md`. Never create one directly in `.claude/`. Then link it: `ln -s ../../plugins/<plugin>/skills/<name> .claude/skills/<name>` (subagents: `ln -s ../../plugins/<plugin>/agents/<name>.md .claude/agents/<name>.md`).
- A new plugin needs `plugins/<name>/.claude-plugin/plugin.json` (`name` = folder name, `version`, `description`) and an entry in `.claude-plugin/marketplace.json`. Bump a plugin's `version` when its behaviour changes.
- A new always-on agent goes in `agents/<name>/` with `PLAN.md`, its program and `memory/instructions.md`. Its runtime state lives outside the repo. Follow `agents/README.md` and use `agents/stats-agent/` as the worked example.
- Data a skill reads or writes (logs, playbooks, brand files, templates) goes in the top-level data folder named after its plugin (`x-assistant/`, `avatar-video/`), not inside the plugin.
- Don't edit the third-party skills in `.claude/skills/` (`hyperframes*`, `media-use`, `heygen-*`). They are pinned in `skills-lock.json` and updated by their installer.
- Before a commit: `claude plugin validate .` passes, a fresh session lists any new skill or subagent, and no secret or personal file is staged (`.gitignore` lists what stays local). Then update the README: the layout tree and a section for any new plugin or agent.
