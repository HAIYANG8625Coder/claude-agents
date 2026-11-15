# AI podcast agent (`agents/ai-podcast`)

## Goal
Every morning a private **10–12 minute English episode** about AI arrives on my phone in Telegram: about 6 stories an editor agent actually read, in a fixed local voice, with chapter times and aligned English–Chinese notes. It doubles as English listening practice.

Rebuilt from [ningcodes/CommuteAIBrief](https://github.com/ningcodes/CommuteAIBrief) (日知, MIT), shown in the Xiaohongshu note "我开源了自己的AI播客：每日播报AI新闻". Same three steps (capture → select → generate), the same source pool, the same editorial rules (collector and editor are different sessions, originals are read before selection, numbers are checked against the original, a ledger records every decision), on the always-on agent setup this repo already uses.

## The five parts

| Part | Here |
|---|---|
| Inbox | SQLite `inbox` table. `podcast.py event edition [date]` or the timer adds one row per date (deduped). One worker (file lock) runs it and resumes from the last finished stage if a run dies |
| Timers | A daily timer at 08:00 (Mac local time). launchd ticks every 10 minutes; a tick with nothing due starts no model and costs nothing |
| Memory | `memory/`: `instructions.md` (editor rules), `collector.md`, `listener.md` (who I am, likes, already knows, doesn't want), `interests.json` (areas the ledger flags), `voice.json`. Learned at runtime: `seen.json` (links already used) and every past run in `runs/` (the editor reads the last 3 briefs) |
| Permissions | Two separate `claude -p` sessions, both without Bash. **Collector**: read the run, WebSearch/WebFetch to find a moved feed, write only `collector-report.json`. **Editor**: read the run and memory, write only `decisions.json` and `brief.json`; no web at all, it reads the originals the program saved. The program does every fetch, check, voice and send. The Telegram token never enters a run |
| Outbox | SQLite `outbox` table: the audio, a chapters + ledger message, and the notes (split under Telegram's 4,096 characters), or a failure notice. Sent in order by the dispatcher |

## One edition

```
capture.py      113 sources (34 feeds, 7 HN queries, 6 blog listings, 2 release feeds, 3 follow-builders feeds;
                61 X accounts listed but not captured yet) → one frozen 48 h window, a receipt per source
ledger.py       dedupe → heat (HN points/comments, X engagement, how many sources carried it) → interest flags
                → required-decisions.json (top heat + first-party news + interest matches, max 40)
collector       claude -p: diagnoses failed sources; a proposed new feed is kept only if the program can parse it
editor phase 1  claude -p: decides every required lead with a specific reason, shortlists 8–12 for the mix
                (2 hot, 1–2 big-company, 2 interest, 1 exploration)
originals       the program fetches each shortlisted original as text (HTML, GitHub README, HN thread via Algolia)
editor phase 2  same editor session: reads originals, selects ~6, writes the script, evidence quotes and notes
gate            every required id decided; selected stories have a readable original and 2+ verbatim 8-word quotes;
                every number > 10 in the script appears in a selected original; 1,300–1,700 words; chapters line up.
                One fix round with the gate's report, then stop (no audio from an unchecked script)
voice (tts.py)  local Qwen3-TTS 1.7B CustomVoice on MLX, speaker "ryan": ≤ 38-word chunks, 3 tries each,
                per-chunk QA, loudness, chapter times → episode.m4a (AAC 64 kb/s). Never sped up
deliver         Telegram: audio + chapters/ledger + notes; selected links go into seen.json
```

Files per day in `~/Library/Application Support/ai-podcast/runs/YYYY-MM-DD/`: `capture/`, `ledger/`, `collector-report.json`, `originals/`, `brief.json`, `gate.json`, `audio/`, `costs.json`, `run.log`.

## Decisions (and where this differs from the original)
- **Telegram instead of the iOS app.** The bot already exists (stats-agent); no Xcode signing that expires every 7 days, works away from home Wi-Fi.
- **The editor reads files the program fetched, not WebFetch.** WebFetch returns a model's summary, so quotes couldn't be checked word for word. Pages that need a login or JavaScript can't be selected; the editor takes the next one and says why.
- **Simpler gates.** The original has Node reading/ranking/quality gates and a hash seal. Here one Python gate checks decisions, quotes, numbers, length and chapters; the run order (gate before voice, same files) replaces the seal.
- **X accounts are not captured yet.** The original uses OpenCLI with a logged-in Chrome. Here they're listed as `not_executed` and part of their posts arrive through the public follow-builders feed. Adding them through Claude in Chrome is the next step.
- **Access rules.** An honest user agent, one request per source per day, no logins; a 403/429/login page is reported, never worked around (Latent Space and OpenAI answer 403 to scripts).
- **Duration is reported, not enforced.** The original refuses episodes outside 600–720 s; here an episode outside that band is still sent, with the real length in the notes, so a short news day still gets an episode.
- **Models:** Sonnet 5.5 for both roles (`PODCAST_EDITOR_MODEL` / `PODCAST_COLLECTOR_MODEL` to change). First real run (2026-11-15): collector $0.35, shortlist $0.34, writing $0.99.

## Use

```bash
python3 -I agents/ai-podcast/podcast.py install          # copy into Application Support, add the launchd job
python3 -I agents/ai-podcast/podcast.py event edition    # make today's episode now
python3 -I agents/ai-podcast/podcast.py status
python3 -I agents/ai-podcast/podcast.py run 2026-11-15 --from gate --to voice   # re-run some stages by hand
```

One-time voice setup (Apple Silicon): `uv python install 3.12`, a venv at `Application Support/ai-podcast/venv-tts` with `mlx==0.32.4 mlx-audio==0.6.3 numpy==2.5.4 soundfile==0.14.0 transformers==5.22.1 huggingface_hub`, and `mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit` (2.9 GB, Apache-2.0) in `Application Support/ai-podcast/models/`. The Mac must be awake at 08:00 with the network up; one edition takes about 20–25 minutes (half of it is the voice).

To steer it: edit `memory/listener.md` (likes, already knows, doesn't want) and `memory/interests.json`, add or remove sources in `sources.json`, then `install` again (it overwrites the rules, never `seen.json` or the runs).
