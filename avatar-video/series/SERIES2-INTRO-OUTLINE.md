# Series 2 intro episode outline: 「从零做企业级 Agent」预告与导读 (for approval; 2026-11-24)

Format: article-explainer, landscape, about 5 to 6 min. Called "第 0 集" (series 2 intro). Same look as series 1. Say "token" and "skill" in English.
Sources: the released design docs in the public repo (PRD v1.0, TRD v1.0, prototype v1.0, tag v1.0-design, commit c453483), `SERIES2-RESEARCH.md` (Claude Code docs on managed settings, sandboxing, monitoring, costs, hosting).
**Nothing is built yet.** The intro shows the design only. No real test, no run, no number about behaviour. Every sentence about the product is future tense ("会做", "要证明"), and the screens are called a prototype with sample data.

## Beginner gate
- 企业级 enterprise-class: here it is not a certificate. It means eight requirements, and each one has a test that can fail. Ch 3.
- 沙盒 sandbox: a box around a program that limits what files and network it can touch. Ch 4.
- 凭证代理 credential proxy: a small program that holds the API key and adds it to each model call, so the agent never holds it. Ch 4.
- 审计日志 audit log: a record of who did what and whether it was allowed. Ch 4.
- 哈希链 hash chain: each log line holds the hash of the line before, so a deleted or edited line shows. Ch 4.

## Chapters
0 开场: hook. Series 1 made an agent that works for one person on one machine, about 1,500 lines. Hand it to a company and five things go wrong. This series makes it safe for many people. Today: what we will build, how, and how you will know it works. Nothing is built yet, and I say so.
1 第一季回顾 (30 s): the series 1 agent in one line: loop, tools, permissions, plan mode, skills, MCP, memory, eval harness. It trusts its user completely.
2 公司不能直接用，五个问题 [D1]: no identity (anyone is the user); rules live with the user (they can edit them); no isolation (full rights, key in the environment); no ceiling (a loop can spend the month); needs a person at the keyboard (a crash loses the run). Source: PRD section 1.
3 什么叫"企业级"：八条要求 [D2, table]: R1 identity, R2 policy, R3 isolation, R4 secrets, R5 audit, R6 cost, R7 reliability, R8 release gate. Each has an acceptance test that fails first, then passes. What we do NOT claim: no SOC 2, ISO or HIPAA, no legal advice, no product to sell. Source: PRD sections 2 and 5.
4 架构一张图 [D3, 3 slides]: a small service wraps the unchanged ep13 engine. Whatever enforces a rule sits outside the sandbox, so a compromised engine cannot switch it off. Three processes: agentd (identity, policy, audit, approvals), keyproxy (holds the key, counts cost), egress (allow-list for network). One engine process per session. Commands run one level deeper and cannot even reach the proxy. Sources: PRD section 7, TRD section 2.
5 四个界面（原型）[4 screenshots from the prototype]: developer session (every tool call shows the rule that allowed or blocked it); approvals on the phone (an unanswered request is denied); admin console (company rules only, per-member spend vs daily cap); audit log (the chain check points at the edited line). Say: sample data, clickable prototype is live on GitHub Pages.
6 怎么做、怎么证明 [D4]: 13 episodes in 5 parts (who and what is allowed, isolation, see it and pay for it, reliability, ship it), about 8 to 9 min each. Same method as series 1: a no-key test with a fake model first, then real runs on DeepSeek flash, 5 trials, read a failed trace, report null results, every number computed from raw files. Plus a red-team set: prompt injection in a file, a hidden instruction in a tool description, a path escape, a repo file that tries to loosen the policy, a loop that overspends. What "pass" looks like: 8 of 8 requirement tests, 0 escapes out of the red-team set with controls on, overshoot at most one model call. Source: PRD sections 4, 9.
7 我们会做错的地方，和怎么补（诚实）: four limits, each paired with the fix Michael approved on 2026-11-24. Source: PRD section 11 (updated to v1.1).
   - Sandbox is a teaching version and can give false confidence → **Docker is the main sandbox** (read-only root, no network, dropped capabilities, CPU and memory caps); `sandbox-exec` is the second option because Apple marks it DEPRECATED (its own man page says so). Each escape (symlink, `..`, path to the db, data sent to an allowed host) is **run on screen** with the control on and with it off; the chapter is "what the tests prove and what they don't".
   - Hash chain only detects partial edits → **anchor**: the service writes the newest chain hash to a place the engine cannot reach (a separate file outside the sandbox, or a Docker volume mounted read-only into the engine's side), so a whole-file rewrite no longer goes unseen. Still not protection against someone who owns the host; said on screen.
   - Engine events are self-reported → **cross-check**: the proxy sees every model call, the service sees every approval and decision; a check compares them with what the engine reports and flags a mismatch as its own audit line.
   - Docs pages not read are marked "unconfirmed", never claimed. Listed on screen: server-managed settings, zero data retention, HIPAA setup, the Claude apps gateway, admin setup, managed MCP, network config, plugins/org.
8 路线与怎么跟 : the 7 phases, about 16 working sessions, no episode filmed before a thin end-to-end slice works. Where to follow: repo `HAIYANG8625Coder/build-an-enterprise-class-agent` (PRD, TRD, prototype now; code from Phase 0), series 1 repo for the engine. Weekly pace on Xiaohongshu and YouTube.
9 结尾: one-line takeaway (an enterprise agent is the same loop plus boundaries that live outside the model), then the comment question: "如果你的公司要用 Agent，你最担心的是哪一件：密钥、花费、还是它乱改文件？"

## Notes and open points for Michael
- Title idea: 「从零做企业级 Agent｜预告：13 集要做什么」. Cover: 「Agent 给公司用，要补哪八件事」 / 「第二季预告」.
- Length: 5 to 6 min, about 30 slides. Shorter than a normal episode because there is no real test.
- No screen recording of running code (nothing runs yet). The prototype screens are used instead; they are labelled "原型，示例数据".
- Facts file: the counts (8 requirements, 13 episodes, 5 parts, 4 screens, 16 sessions, 7 phases, 1,500 lines) are read from the PRD by code before the script.
- Decision for you: keep the 13-episode number in the video? The PRD says "13 planned; revisit after Phase A", so I would say "planned 13, may change".
- Not claimed: anything about Claude Code beyond what the docs say; the docs facts used are only the general ones in SERIES2-RESEARCH.md.

## Unconfirmed items found on 2026-11-24 (audit of PRD v1.0, TRD v1.0, research notes and this outline)
Checked on this Mac today: Docker server 29.5.2 answers; Python 3.9.6; macOS 27.2.1; `man sandbox-exec` says DEPRECATED (confirmed).
Not confirmed, so the intro must not state them as facts:
1. Docs pages never read: admin-setup, server-managed-settings, managed-mcp, network-config, zero-data-retention, hipaa-setup, the Claude apps gateway pages, plugins/org (SERIES2-RESEARCH.md).
2. The last 13,853 characters of the permissions page were reproduced by a model, so quotes from that tail are less reliable; check on the page before any quote goes on screen.
3. The fetch tool passes pages through a small model: every exact docs quote must be checked on the page.
4. Seatbelt profile (TRD section 7) is a sketch. Not tested that Python starts under `(deny default)`, nor that one loopback port can be allowed while others are blocked (TRD open questions 1 and 2).
5. A `sandbox-exec -n no-network /usr/bin/true` test run from this session was killed (exit 137) rather than finishing. Cause unknown: it may be this session's own sandbox. Treat "sandbox-exec works on this Mac" as UNCONFIRMED until Phase 0 runs it from a plain terminal.
6. `colima status` did not return within 120 s from this session, although `docker version` answered. Treat "Colima is healthy" as unconfirmed too.
7. DeepSeek flash: whether every response carries input and output token counts in the Anthropic shape is unchecked (TRD open question 3). R6 depends on it.
8. Docker design gap: services listen on `127.0.0.1` on the Mac, but a container under Colima cannot reach the host's loopback that way. The TRD's "engine container reaches only keyproxy" needs a different network path (for example keyproxy in a container on an internal network). Not tested.
9. "The engine never gets the Docker socket; the runner starts command containers" is a design, not a tested fact.
10. Every number marked *proposed* (4 sessions, 50 ms, 1,500 new lines, 120 s, 4 retries, 5 min, 8 h, 60 s cache) is a target, not a result. The 1 GiB / 5 GiB / 1 CPU figure is the docs' starting point for hosting (read in full).
11. The pass^k = 5 gate for real evals could flake with a real model; unmeasured.
12. GitHub Actions: Docker sandbox tests in CI on Linux are planned; no workflow exists yet.
13. The cost of the new anchor and cross-check (about 20 lines for the anchor) is my estimate, not measured.
