# claude-agents

My agents and skills for [Claude Code](https://claude.com/claude-code), built while learning to design and control AI agents in public.

## X assistant

A small multi-agent setup that drafts, reviews, illustrates and publishes posts on X — with a human approval step before anything goes public.

```
/x-research  →  studies popular posts in my niches, updates the playbook
/x-post      →  x-drafter writes 3 drafts → x-reviewer checks them → I pick → posts via Chrome
/x-image     →  on-brand post image from HTML templates, rendered with headless Chrome
```

| Path | What it is |
|---|---|
| `.claude/agents/x-drafter.md` | Writes 3 different drafts using my voice + the playbook |
| `.claude/agents/x-reviewer.md` | Independent review: typos, tone, invented facts, risk, hook strength |
| `.claude/skills/x-post/` | The full flow: draft → review → approve → post → log |
| `.claude/skills/x-research/` | Read-only research of popular posts → `playbook.md` |
| `.claude/skills/x-image/` | 5 templates (hook, list, code, compare, stat), shared `brand.css`, `render.sh` |
| `x-assistant/playbook.md` | What works on X, learned from real posts |
| `x-assistant/posts.md` | Everything posted so far (agents use it to avoid repeats) |
| `x-assistant/voice.example.md` | Template for your own `voice.md` (mine is kept private) |
| `global/CLAUDE.md` | Backup of my global Claude Code rules (`~/.claude/CLAUDE.md`) |

## Use it yourself

1. Clone this repo and open the folder in Claude Code.
2. `cp x-assistant/voice.example.md x-assistant/voice.md` and describe yourself.
3. Install the [Claude in Chrome](https://chromewebstore.google.com/detail/fcoeoabgfenejglbffodgkkbkcdhcgfn) extension and sign in to X in Chrome.
4. Run `/x-research`, then `/x-post <topic>`.

`/x-image` needs Google Chrome on macOS (it renders with headless Chrome).

## Design principles

- One agent per job; a second agent only where it adds a fresh perspective (review).
- Rules live in files, not in chat — improve the files when output is wrong.
- Nothing public happens without explicit human approval.
