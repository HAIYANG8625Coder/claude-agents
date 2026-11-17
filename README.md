# claude-agents

My agents and skills for [Claude Code](https://claude.com/claude-code), built while learning to design and control AI agents in public.

## Repository layout

The repo follows Claude Code's own plugin layout, so each group of skills and subagents is a plugin, and the repo is a plugin marketplace.

```
claude-agents/
├─ .claude-plugin/marketplace.json   the marketplace: lists every plugin below
├─ plugins/                          one folder per plugin (skills + subagents that work together)
│  ├─ x-assistant/                   .claude-plugin/plugin.json, skills/, agents/
│  ├─ avatar-video/
│  ├─ outlook-email/
│  └─ diagrams/                    chart-draw: clean SVG diagrams for docs
├─ agents/                           always-on agents: programs that run on their own schedule
│  ├─ stats-agent/                   PLAN.md, agent.py, memory/instructions.md
│  ├─ ai-podcast/                    PLAN.md, podcast.py, capture.py, ledger.py, tts.py, sources.json, memory/
│  └─ sg-podcast/                    the same agent for Singapore news (own sources, rules and 07:30 timer)
├─ .claude/skills/, .claude/agents/  links into plugins/ (so this folder loads them with plain names),
│                                    plus HeyGen's third-party skills pinned in skills-lock.json
├─ x-assistant/                      data for x-assistant: playbook, posts log, cards
└─ avatar-video/                     data for avatar-video: brand, video templates (9:16 and 16:9), tools
```

**Adding something new**
- A new skill or subagent: put it in `plugins/<plugin>/skills/<name>/SKILL.md` or `plugins/<plugin>/agents/<name>.md`, then link it into `.claude/skills/` or `.claude/agents/` (`ln -s ../../plugins/<plugin>/skills/<name> .claude/skills/<name>`).
- A new plugin: `plugins/<name>/.claude-plugin/plugin.json` (at least `name`), add it to `.claude-plugin/marketplace.json`, and check it with `claude plugin validate .`.
- A new always-on agent: `agents/<name>/` with a `PLAN.md`, its program, and its `memory/`. Its state lives outside the repo.

**Install the plugins somewhere else** (another project, another machine):
```
claude plugin marketplace add HAIYANG8625Coder/claude-agents
claude plugin install x-assistant@claude-agents
```
Installed this way the commands are namespaced (`/x-assistant:x-post`). Some skills still expect this repo's data folders (`x-assistant/`, `avatar-video/`) in the working directory.

## Rules for this repo

Every new feature follows how Claude Code itself organizes skills, subagents and plugins ([plugins](https://code.claude.com/docs/en/plugins), [marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)). When Claude Code changes its conventions, update the layout and this section first, then the features.

1. **Every skill and subagent belongs to a plugin.** Its source lives in `plugins/<plugin>/skills/<name>/SKILL.md` or `plugins/<plugin>/agents/<name>.md`, never directly in `.claude/`.
2. **`.claude/skills/` and `.claude/agents/` only hold links** into `plugins/` (so this folder loads them with plain names), plus third-party skills installed by a tool and pinned in `skills-lock.json`. Don't edit third-party skills; update them with their installer.
3. **Group by job.** Skills and subagents that work together go in the same plugin. Start a new plugin only for a new area of work, not for each skill.
4. **Every plugin has a manifest** at `plugins/<name>/.claude-plugin/plugin.json` (`name` matches the folder, plus `version` and `description`) and an entry in `.claude-plugin/marketplace.json`. Bump `version` when a plugin's behaviour changes.
5. **Plugin files stay inside the plugin.** Use the default folders (`skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, `bin/`, `scripts/`). Scripts refer to their own files relative to the skill (or `${CLAUDE_PLUGIN_ROOT}` in hooks and MCP config), never with `..` out of the plugin.
6. **Data is not code.** Logs, playbooks, brand files and templates a skill reads or writes live in a top-level data folder named after the plugin (`x-assistant/`, `avatar-video/`). Personal data (voice, ids, recordings, renders) is git-ignored.
7. **Always-on agents go in `agents/<name>/`** with a `PLAN.md` (goal, the five parts, decisions), the program, and `memory/instructions.md`. Their runtime state lives outside the repo (see [agents/README.md](agents/README.md)).
8. **Check before every commit:** `claude plugin validate .` passes, a fresh session lists the new skill or subagent, and no secret or personal file is staged.
9. **Document it here.** A new plugin or agent gets a section in this README (what it does, its commands, its paths), and the layout tree above stays current.

## X assistant (plugin `x-assistant`)

A small multi-agent setup that drafts, reviews, illustrates and publishes posts on X, Xiaohongshu and YouTube — with a human approval step before anything goes public.

```
/x-research  →  studies popular posts in my niches, updates the playbook
/x-post      →  x-drafter writes 3 drafts → x-reviewer checks them → I pick → posts via Chrome
/x-image     →  on-brand post image from HTML templates, rendered with headless Chrome
/xhs-post    →  Chinese image-and-text note on Xiaohongshu (rednote) with 3:4 swipe cards
/youtube-post →  title, description, tags for a finished video → I approve → uploads in YouTube Studio
```

| Path | What it is |
|---|---|
| `plugins/x-assistant/agents/x-drafter.md` | Writes 3 different drafts using my voice + the playbook |
| `plugins/x-assistant/agents/x-reviewer.md` | Independent review: typos, tone, invented facts, risk, hook strength |
| `plugins/x-assistant/skills/x-post/` | The full flow: draft → review → approve → post → log |
| `plugins/x-assistant/skills/x-research/` | Read-only research of popular posts → `playbook.md` |
| `plugins/x-assistant/skills/x-image/` | 5 templates (hook, list, code, compare, stat), shared `brand.css`, `render.sh` |
| `plugins/x-assistant/skills/xhs-post/` | Xiaohongshu flow + 4 card templates (cover, overview, step, pitfalls) |
| `plugins/x-assistant/skills/youtube-post/` | YouTube upload flow (long videos and Shorts) + `scripts/check.py` for title, description, tag and chapter limits |
| `x-assistant/playbook.md` | What works on X, learned from real posts |
| `x-assistant/posts.md` | Everything posted so far (agents use it to avoid repeats) |
| `x-assistant/voice.example.md` | Template for your own `voice.md` (mine is kept private) |

## Use it yourself

1. Clone this repo and open the folder in Claude Code.
2. `cp x-assistant/voice.example.md x-assistant/voice.md` and describe yourself.
3. Install the [Claude in Chrome](https://chromewebstore.google.com/detail/fcoeoabgfenejglbffodgkkbkcdhcgfn) extension and sign in to X in Chrome.
4. Run `/x-research`, then `/x-post <topic>`.

`/x-image` needs Google Chrome on macOS (it renders with headless Chrome).

**Xiaohongshu (`/xhs-post`):** connect Claude in Chrome to Claude Code (`claude --chrome` or `/chrome`), log in at xiaohongshu.com in that Chrome profile, and open creator.xiaohongshu.com once to finish its first-time prompts. Then change the card footer in `plugins/x-assistant/skills/xhs-post/templates/` to your own name. The full checklist is in the skill's "Before first use" section.

**YouTube (`/youtube-post <video>`):** the same Chrome profile, signed in to YouTube, with studio.youtube.com opening your channel dashboard. It is a separate skill from the video makers and the other post skills, so one video can go to each platform with its own approval.

## Always-on stats agent (`agents/stats-agent`)

A small always-on agent built on the five parts from Anthropic's [Building always-on agents](https://claude.com/resources/articles/building-always-on-agents). It mostly sleeps. It wakes up to read Xiaohongshu note stats, writes each note's 24-hour numbers to its own `stats.md` (which `/xhs-post` copies into `x-assistant/posts.md`), and messages me on Telegram only when there is something worth knowing.

| Part | Here |
|---|---|
| Inbox | SQLite `inbox` table. `agent.py event check` only adds a row; one worker (file lock) batches every pending event into one run, and events are deduped by id |
| Timers | Separate `timers` table: a daily digest at 21:15, plus a follow-up for each new note at publish time + 24 h. A scheduler turns due timers into inbox events |
| Memory | `memory/`: `instructions.md` (loaded every run), `notes.md` (what it learned), `reported.md` (what it already told me) |
| Permissions | `claude -p` with an allow-list: it can read the note list in Chrome and read or edit only its own folder. No Bash, no clicks, no publishing. The Telegram token never enters the run |
| Outbox | SQLite `outbox` table. The run returns a message or `null`, and a dispatcher sends it |

`python3 -I agents/stats-agent/agent.py install` copies the agent to `~/Library/Application Support/stats-agent/` and adds a launchd job that ticks every 10 minutes while the Mac is awake. A tick with nothing due starts no model and costs nothing. `status` shows its tables, and `event check` asks for the numbers now. It runs entirely outside `~/Documents`, so it needs no Full Disk Access and can't see your private folders. It needs Chrome open with Claude in Chrome connected.

## Always-on AI podcast (`agents/ai-podcast`)

A private 10–12 minute English AI news episode every morning, sent to Telegram with chapter times and English–Chinese notes. A rebuild of [ningcodes/CommuteAIBrief](https://github.com/ningcodes/CommuteAIBrief) (MIT) on the same five parts as the stats agent.

| Step | Here |
|---|---|
| Capture | `capture.py`: 113 sources (feeds, HN queries, blog listings, release feeds, follow-builders), one frozen 48 h window, a receipt per source. Standard library only; failures are reported, never worked around |
| Ledger | `ledger.py`: dedupe, heat, interest flags, the leads the editor must decide on |
| Collector | `claude -p` session 1: diagnoses failed sources; a new feed is kept only if the program can parse it |
| Editor | `claude -p` session 2 (never the collector's): decides every required lead, shortlists, reads the originals the program fetched, writes script + evidence + notes |
| Gate | quotes must be verbatim in the original, numbers must appear in an original, every decision has a reason; one fix round |
| Voice | `tts.py`: local Qwen3-TTS (MLX) with a fixed built-in speaker, per-chunk QA, AAC via `afconvert` |
| Deliver | Telegram audio + chapters/ledger + notes |

`python3 -I agents/ai-podcast/podcast.py install` copies it to `~/Library/Application Support/ai-podcast/` and adds a launchd job (edition at 08:00). `event edition` makes one now, `status` shows its tables. The voice needs a one-time Python 3.12 venv and a 2.9 GB model; see [agents/ai-podcast/PLAN.md](agents/ai-podcast/PLAN.md).

## Singapore briefing (`agents/sg-podcast`)

The AI podcast pipeline pointed at Singapore: 15 government newsrooms, local and finance media (CNA, The Straits Times, Business Times, The Edge, Mothership, 8world and more), entertainment (8 Days, ST Life), r/singapore and big local creators' YouTube channels, in a 72-hour window. Each episode focuses on immigration, the job market and finance (2 immigration & jobs, 2 finance), plus 1 entertainment story and 1 top news story. It keeps facts apart from opinion and takes no political side. It runs at 07:30 with its own runtime and timer and shares the local voice with `ai-podcast`. Details: [agents/sg-podcast/PLAN.md](agents/sg-podcast/PLAN.md).

## Avatar video (plugin `avatar-video`)

Videos where my AI twin (HeyGen avatar + my cloned voice) explains a topic, edited in code with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4): short vertical clips (`avatar-video`; `voice-video` for my cloned voice over graphics, no face) and long 16:9 deep-dives of one article or paper (`article-explainer`).

```
/avatar-video <topic> [xhs|x] [NN s]
  video-scripter writes 2 spoken scripts → video-reviewer checks them → I pick
  → storyboard (I approve before any credits are spent) → voice in one take (I listen)
  → avatar lip-synced to that exact audio → captions, B-roll, cards in HyperFrames
  → preview (I approve) → render → hand off to /xhs-post or /x-post

/article-explainer <url or file>
  read one article or 1–3 papers → RESEARCH.md with every number's figure/table/page
  → chapter outline (I approve) → script, one item per slide (I approve)
  → voice, one take per chapter, joined → 16:9 slide deck (chapter bar, original next to a
  rebuilt Chinese diagram, source line on every slide, cover as frame 0) → render → note text → /xhs-post
```

| Path | What it is |
|---|---|
| `plugins/avatar-video/skills/avatar-video/` | The full flow, with approval gates before every paid step |
| `plugins/avatar-video/agents/video-scripter.md`, `video-reviewer.md` | Script writer and independent script check |
| `plugins/avatar-video/skills/article-explainer/` | 4–8 min 16:9 deep-dive of one article or paper (style preset H), plus `scripts/takes.py` for one take per chapter |
| `avatar-video/template-explainer/` | The 16:9 starter project for article-explainer |
| `avatar-video/brand/DESIGN.md` | Video look: colors, safe zones, captions, the 3 effects, style presets A–H |
| `avatar-video/brand/EXPLAINER-PLAYBOOK.md` | How the deep-dive format works (learned from a Xiaohongshu AI creator, 2026-11-15) |
| `avatar-video/videos.md` | Every video made (avoids repeats, notes what to improve) |
| `.claude/skills/hyperframes*`, `media-use`, `heygen-*` | Third-party skills from HeyGen, pinned in `skills-lock.json` |

Setup: Node.js 22+ (`npm install` in `avatar-video/` adds FFmpeg), a HeyGen plan, `npx hyperframes auth login`, and `/mcp` → heygen. Your `AVATAR-*.md`, recordings and renders are git-ignored.

## Diagrams (plugin `diagrams`)

`/chart-draw` draws architecture, workflow and timeline diagrams as hand-written SVG, in the style of the figures in Anthropic's [Building always-on agents](https://claude.com/resources/articles/building-always-on-agents): beige panels, white boxes, one orange path with numbered steps, and real example rows. Light mode is the default, and each diagram also gets a dark twin that GitHub shows to dark-mode readers. A checker renders each SVG with headless Chrome. It flags overlapping labels, lines crossing text and anything outside the frame, and it saves a preview at GitHub's README width with Arial.

| Path | What it is |
|---|---|
| `plugins/diagrams/skills/chart-draw/SKILL.md` | The flow: facts → pick a template → draw → check → embed |
| `plugins/diagrams/skills/chart-draw/assets/` | 10 worked examples: overview, steps + table, timeline, sequence, state machine, decision tree, swimlane, folder tree, compare, layers |
| `plugins/diagrams/skills/chart-draw/references/catalog.md` | Which type answers which question, with a recipe for each |
| `plugins/diagrams/skills/chart-draw/scripts/svgkit.py` + `examples/` | A small Python kit that draws boxes, arrows, pills and tables in the house style; 7 of the examples are built with it |
| `plugins/diagrams/skills/chart-draw/references/style.md` | Colours, type sizes, arrow and label rules |
| `plugins/diagrams/skills/chart-draw/scripts/theme.py` | Makes the dark-mode twin (`<name>-dark.svg`) of a light diagram; embed both with `<picture>`, with light as the default |
| `plugins/diagrams/skills/chart-draw/scripts/check.py` | `python3 -I check.py *.svg --github`: PNG previews + layout check: overlaps, labels on lines, text or boxes spilling over edges (exit 1 on a problem) |

Worked example: the diagrams in [agents/stats-agent/PLAN.md](agents/stats-agent/PLAN.md).

## Outlook email (plugin `outlook-email`)

Reads, searches and summarizes Outlook email through Claude in Chrome. Read-only unless I say otherwise.

## Design principles

- One agent per job; a second agent only where it adds a fresh perspective (review).
- Rules live in files, not in chat — improve the files when output is wrong.
- Nothing public happens without explicit human approval.
