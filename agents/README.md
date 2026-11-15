# Always-on agents

Programs that run on their own schedule and wake a Claude run only when there is work, built on the five parts from Anthropic's [Building always-on agents](https://claude.com/resources/articles/building-always-on-agents): inbox, timers, memory, permissions, outbox.

Each agent gets its own folder:

```
agents/<name>/
├─ PLAN.md                  goal, the five parts, architecture + workflow diagrams, decisions, use
├─ agent.py (or similar)    scheduler, worker, dispatcher, install / uninstall
└─ memory/instructions.md   the rules loaded at the start of every run
```

Runtime state (databases, logs, learned memory, anything personal) lives outside the repo, e.g. `~/Library/Application Support/<name>/`, so it never gets committed.

| Agent | What it does |
|---|---|
| [stats-agent](stats-agent/PLAN.md) (architecture + workflow diagrams inside) | Reads my Xiaohongshu note stats 24 h after each note goes live and messages me on Telegram only when it's worth it |
| [ai-podcast](ai-podcast/PLAN.md) | Every morning: captures 113 AI sources, a collector and a separate editor agent read originals and pick ~6 stories, local Qwen3-TTS voices a 10–12 min English episode, sent to Telegram with Chinese–English notes |
| [sg-podcast](sg-podcast/PLAN.md) | The same pipeline for Singapore at 07:30: government newsrooms, local media, r/singapore and big local creators → a 10–12 min English briefing focused on immigration, jobs and finance, plus some entertainment, on Telegram |
