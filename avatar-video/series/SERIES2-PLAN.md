# Series 2 plan: an enterprise-class AI agent (draft for Michael's approval; 2026-11-21)

Working title: 「从零做企业级 Agent」 (series 2 of 从零做 Agent). Status: PLAN ONLY. Nothing is built or tested yet. Ep 13 of series 1 ends by saying "I plan to do this next; details will change", so nothing in the plan below may be shown as done.

## Why this series
Series 1 built a coding agent for ONE person on ONE machine (about 1,500 lines, ep 13). A company needs different things: many people at once, who-is-who, rules nobody can switch off, a record of what happened, a cost ceiling, and an agent that can run without a person watching. The official Claude Code docs have a whole enterprise side (managed settings, sandboxing, monitoring, gateway, hosting) that series 1 did not cover. Series 2 rebuilds the smallest honest version of each piece, tests it, and compares with what the docs say Claude Code does.

## Audience and prerequisites
Someone who watched (or read) series 1, or any developer who can read Python. Same rules: no framework, plain Python, DeepSeek or Claude through environment-variable keys, every run on screen is real, Claude Code behaviour comes only from the official docs.

## Shape: five parts, 13 episodes (the same six-part video format, 8 to 9 minutes each)

### A · Who and what is allowed (ep 1 to 3)
1. **Many users, one agent service.** Goal: know who is asking. Build: a thin service in front of the engine with a user id per request, per-user working folder and session store. Docs: authentication (forced login method and organisation, credential precedence), hosting (one process per session, local disk is lost on restart). Pitfall: a leftover API key silently overriding the intended login (docs say this).
2. **Policy nobody can switch off.** Goal: rules the user cannot override. Build: managed (central) settings loaded before user and project settings, deny first then ask then allow, a managed-only lock; enforcement in the program, not in the prompt. Docs: settings (precedence: managed, command line, local, project, user), permissions ("Permission rules are enforced by Claude Code, not by the model"). Pitfall: a repository file that tries to loosen the policy (docs list what is ignored).
3. **Rules the model cannot argue with.** Goal: test the policy against an agent that is told to break it. Build: a red-team task set (reuse the ep 12 harness): prompt injection in a file, a tool description (ep 11), a command that tries to reach outside the folder. Docs: security page, permissions ("Bash permission patterns that try to constrain command arguments are fragile").

### B · Isolation (ep 4 to 6)
4. **A sandbox for commands.** Goal: limit what a command can touch, not only whether it runs. Build: run commands in a throwaway container or an OS sandbox profile with writes only in the working folder and no network except an allow-list. Docs: sandboxing (Seatbelt, bubblewrap, writes limited to the working directory, network through a proxy), secure deployment (Docker flags, gVisor, Firecracker). Honest limit: our sandbox is a teaching version.
5. **Secrets the agent never sees.** Goal: keys stay outside the boundary. Build: a small proxy that adds the API key on the way out; the agent process has no key. Docs: secure deployment (credential proxy), sandboxing (credential masking). Pitfall: tools that ignore proxy variables (docs).
6. **Many tenants in one process.** Goal: one customer cannot read another's memory or files. Build: per-tenant config dir, memory dir and working folder; a test that tries to cross. Docs: hosting (per-tenant config directory and working directory, auto memory off).

### C · See it and pay for it (ep 7 to 9)
7. **An audit log.** Goal: answer "who did what, and was it allowed" after the fact. Build: one structured event per prompt, tool call, permission decision and error, with user id and session id; content (prompts, tool output) off by default. Docs: monitoring (OpenTelemetry events such as tool_result and tool_decision; content logging off by default). Our own addition, marked as ours: a hash chain so a deleted line shows.
8. **Cost control.** Goal: a ceiling per user and per day. Build: token counting per call, budgets, a stop with a clear message. Docs: costs (seat allowance, spend limits, budgets; the cost shown is an estimate). Real test: a run that would overspend is stopped at the cap, and how far it overshoots.
9. **Evals as a gate.** Goal: no release without a passing test set. Build: the ep 12 harness run in CI on every change; pass^k as the gate; a trace saved for every failure. Docs: Anthropic "Demystifying evals for AI agents" (already read), CLI flags for headless runs.

### D · Reliability (ep 10 to 11)
10. **When things fail.** Goal: a crash or an API error does not lose the work. Build: timeouts, retries with back-off, saved session store so a run resumes after a restart. Docs: hosting (no top-level session timeout; session store), headless (retry events). Real test: kill the process mid-task, resume, finish.
11. **A person in the loop, without a terminal.** Goal: approvals when nobody is at the keyboard. Build: an approval request sent to a chat or a web page, with a timeout that denies. Docs: permissions (deny instead of prompting for unattended runs).

### E · Ship it (ep 12 to 13)
12. **Deploy it.** Goal: one container, one egress proxy, model version pinned, a gateway option. Docs: devcontainer, llm-gateway, third-party integrations (pin model versions). Pitfall: a policy file inside the image that anyone with write access can remove (the docs say so).
13. **Data and the checklist.** Goal: what is stored, for how long, who can read it. Build: retention sweep for our own logs and sessions, redaction of secrets in logs. Docs: data-usage (retention, training, zero data retention is not in the standard plan). Closing: a one-page checklist, what Claude Code has that ours does not, series ending.

## What is NOT promised
- Compliance certifications, legal advice, or a product you can sell. The series builds teaching versions and says where they stop.
- Anything the docs did not say. Where the docs are silent the video says "our version does it this way".
- The exact episode list. It may change after the first real tests (series 1 changed twice).

## Open questions for Michael (answer any; defaults in brackets)
1. Same stack as series 1: Python, no framework, DeepSeek or Claude by environment key? [yes]
2. Start from the finished ep 13 agent, as a library? [yes: one engine, new layers around it]
3. 13 episodes, or fewer (say 9: drop 3, 6, 11, 13)? [13 planned, decide after ep 1 to 3]
4. First episode: Many users (ep 1 above), or Sandbox (ep 4 above) because it is the most visual? [ep 1]
5. Posting: same channels (Xiaohongshu and YouTube), same weekly pace? [same]
6. Written articles and the public repo: a new repo for series 2 (build-your-own-enterprise-agent) or a new folder in the same repo? [new folder `series2/` in the same repo]

## Before episode 1 (the same rules as series 1)
Research first: read the pages not yet read (admin setup, server-managed settings, network config, zero data retention, the Claude apps gateway pages); write SERIES2-SYLLABUS.md in the repo; then per episode: research, real test, outline, approval, script, cards, approval, voice, rough cut, approval, post.
