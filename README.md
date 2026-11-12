# claude-agents

My agents and skills for [Claude Code](https://claude.com/claude-code), built while learning to design and control AI agents in public.

## X assistant

A small multi-agent setup that drafts, reviews, illustrates and publishes posts on X — with a human approval step before anything goes public.

```
/x-research  →  studies popular posts in my niches, updates the playbook
/x-post      →  x-drafter writes 3 drafts → x-reviewer checks them → I pick → posts via Chrome
/x-image     →  on-brand post image from HTML templates, rendered with headless Chrome
/xhs-post    →  Chinese image-and-text note on Xiaohongshu (rednote) with 3:4 swipe cards
```

| Path | What it is |
|---|---|
| `.claude/agents/x-drafter.md` | Writes 3 different drafts using my voice + the playbook |
| `.claude/agents/x-reviewer.md` | Independent review: typos, tone, invented facts, risk, hook strength |
| `.claude/skills/x-post/` | The full flow: draft → review → approve → post → log |
| `.claude/skills/x-research/` | Read-only research of popular posts → `playbook.md` |
| `.claude/skills/x-image/` | 5 templates (hook, list, code, compare, stat), shared `brand.css`, `render.sh` |
| `.claude/skills/xhs-post/` | Xiaohongshu flow + 4 card templates (cover, overview, step, pitfalls) |
| `x-assistant/playbook.md` | What works on X, learned from real posts |
| `x-assistant/posts.md` | Everything posted so far (agents use it to avoid repeats) |
| `x-assistant/voice.example.md` | Template for your own `voice.md` (mine is kept private) |

## Use it yourself

1. Clone this repo and open the folder in Claude Code.
2. `cp x-assistant/voice.example.md x-assistant/voice.md` and describe yourself.
3. Install the [Claude in Chrome](https://chromewebstore.google.com/detail/fcoeoabgfenejglbffodgkkbkcdhcgfn) extension and sign in to X in Chrome.
4. Run `/x-research`, then `/x-post <topic>`.

`/x-image` needs Google Chrome on macOS (it renders with headless Chrome).

**Xiaohongshu (`/xhs-post`):** connect Claude in Chrome to Claude Code (`claude --chrome` or `/chrome`), log in at xiaohongshu.com in that Chrome profile, and open creator.xiaohongshu.com once to finish its first-time prompts. Then change the card footer in `.claude/skills/xhs-post/templates/` to your own name. The full checklist is in the skill's "Before first use" section.

## Avatar video (digital twin)

Short vertical videos where my AI twin (HeyGen avatar + my cloned voice) explains a topic, edited in code with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4).

```
/avatar-video <topic> [xhs|x] [NN s]
  video-scripter writes 2 spoken scripts → video-reviewer checks them → I pick
  → storyboard (I approve before any credits are spent) → voice in one take (I listen)
  → avatar lip-synced to that exact audio → captions, B-roll, cards in HyperFrames
  → preview (I approve) → render → hand off to /xhs-post or /x-post
```

| Path | What it is |
|---|---|
| `.claude/skills/avatar-video/` | The full flow, with approval gates before every paid step |
| `.claude/agents/video-scripter.md`, `video-reviewer.md` | Script writer and independent script check |
| `avatar-video/brand/DESIGN.md` | Video look: colors, safe zones, captions, the 3 effects |
| `avatar-video/videos.md` | Every video made (avoids repeats, notes what to improve) |
| `.claude/skills/hyperframes*`, `media-use`, `heygen-*` | Third-party skills from HeyGen, pinned in `skills-lock.json` |

Setup: Node.js 22+ (`npm install` in `avatar-video/` adds FFmpeg), a HeyGen plan, `npx hyperframes auth login`, and `/mcp` → heygen. Your `AVATAR-*.md`, recordings and renders are git-ignored.

## Design principles

- One agent per job; a second agent only where it adds a fresh perspective (review).
- Rules live in files, not in chat — improve the files when output is wrong.
- Nothing public happens without explicit human approval.
