# Always-on agents

Programs that run on their own schedule and wake a Claude run only when there is work, built on the five parts from Anthropic's [Building always-on agents](https://claude.com/resources/articles/building-always-on-agents): inbox, timers, memory, permissions, outbox.

Each agent gets its own folder:

```
agents/<name>/
├─ PLAN.md                  goal, how it maps to the five parts, decisions, how to use it
├─ agent.py (or similar)    scheduler, worker, dispatcher, install / uninstall
└─ memory/instructions.md   the rules loaded at the start of every run
```

Runtime state (databases, logs, learned memory, anything personal) lives outside the repo, e.g. `~/Library/Application Support/<name>/`, so it never gets committed.

| Agent | What it does |
|---|---|
| [stats-agent](stats-agent/PLAN.md) | Reads my Xiaohongshu note stats 24 h after each note goes live and messages me on Telegram only when it's worth it |
