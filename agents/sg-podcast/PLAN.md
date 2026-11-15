# Singapore briefing agent (`agents/sg-podcast`)

## Goal
Every morning at 07:30 a private **10–12 minute English episode on Singapore** arrives in Telegram, focused on **immigration** (work passes, PR, visas: what changes, for whom, from when, how much), **the job market** and **finance** (markets, rates, property, CPF), with one light **entertainment** story and the day's top news. With chapter times and English–Chinese notes.

It is a copy of [`ai-podcast`](../ai-podcast/PLAN.md) pointed at Singapore. The AI agent is untouched: separate folder, runtime, database, timer and launchd job. They share only the Telegram bot and, read-only, the local voice (the venv and the 2.9 GB Qwen3-TTS model in `Application Support/ai-podcast/`).

## What's different from ai-podcast

| | ai-podcast | sg-podcast |
|---|---|---|
| Sources | 113 AI sources | 48: 15 government newsrooms (PMO, gov.sg, MOM, MAS, MOE, MOH, CPF, LTA, IRAS, MTI, MOF, ICA, URA, MND, MSF), gov.sg and PMO YouTube, local news (CNA, ST, BT, Mothership, 8world, Independent, RICE), finance (ST Business, CNA Business, BT markets / property / wealth, The Edge Singapore, Dollars and Sense, Seedly), entertainment (8 Days, ST Life, TheSmartLocal, Seth Lui), r/singapore and r/askSingapore, 9 big local creators' YouTube channels, HN "singapore" |
| Window | 48 h | 72 h (ministries publish on weekdays) |
| Must-decide leads | top heat, first-party AI labs, interests | top heat, **every official government lead**, interests (immigration, jobs, finance and markets, personal money, property, entertainment) |
| Episode mix | 2 hot, 1–2 big-company, 2 interest, 1 exploration | 2 **immigration & jobs** (rules read from the MOM / ICA release), 2 **finance**, 1 **entertainment**, 1 **top news** |
| Editor rules | mechanisms and numbers with scope | what changes / for whom / from when / how much; attribute every claim; facts apart from opinion; no political side; courts and crime worded exactly as the original |
| Time | 08:00 | 07:30, so the two voices never run at once |

`capture.py` here also reads day-first dates ("14 November 2026", the government sites' format) and repairs WordPress feeds with a stray `&` (Mothership).

## Honest limits
- Facebook, Instagram, TikTok and X need a login, so politicians' and influencers' posts there aren't read; creators are followed through their public YouTube channels.
- TODAY, HDB, ELD and MTI answer 403 to scripts and are reported, not worked around. MAS's news page needs a browser. Some newsroom pages (MOE, MSF, CPF, MND) list menu links rather than releases; the collector reports them and proposes a better official route when it finds one.
- Paywalled Straits Times articles can't be read in full; the editor then picks CNA or the official release.

## Use

```bash
python3 -I agents/sg-podcast/podcast.py install          # copy into Application Support/sg-podcast, add the launchd job (07:30)
python3 -I agents/sg-podcast/podcast.py event edition    # make today's episode now
python3 -I agents/sg-podcast/podcast.py status
```

Steer it with `memory/listener.md`, `memory/interests.json` and `sources.json`, then `install` again (it never touches `seen.json` or past runs). The pipeline, gate, voice and outbox work exactly as in [ai-podcast/PLAN.md](../ai-podcast/PLAN.md).
