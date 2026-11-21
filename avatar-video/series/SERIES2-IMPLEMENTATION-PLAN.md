# Implementation plan: how to build an enterprise-class agent (draft for approval, 2026-11-21)

This plan says **what we build, in what order, how each piece is tested, and where it can go wrong**. It sits under `SERIES2-PLAN.md` (the 13-episode story) and `SERIES2-RESEARCH.md` (what the official docs say). Nothing here is built yet.

## 1. What "enterprise-class" means here (the 8 requirements)

We do not claim a certification. We mean an agent service that meets eight concrete requirements. Each one has a test that can fail.

| # | Requirement | Plain meaning | Done when |
|---|---|---|---|
| R1 | Identity | Every request has a known user | a request without a valid token is refused, and every event carries a user id |
| R2 | Policy | Rules the user cannot switch off | a managed deny rule beats a user allow rule, in a test |
| R3 | Isolation | A command or a tenant cannot touch what it should not | a sandboxed command cannot write outside its folder or reach a blocked host; tenant A cannot read tenant B |
| R4 | Secrets | The agent process never holds the model key | the key is not in the agent's environment or files; a test greps for it |
| R5 | Audit | Afterwards we can say who did what, and whether it was allowed | one event per prompt, tool call and decision; a deleted line is detected |
| R6 | Cost | A ceiling per user and per day | a run that would overspend is stopped; we measure how far it overshoots |
| R7 | Reliability | A crash or an API error does not lose the work | kill the process mid-task, resume, finish |
| R8 | Release gate | No change ships without passing tests | CI runs the no-key checks on every change and the real evals on a schedule |

## 2. Architecture (one picture in words)

```
client (curl / small CLI)
   │  HTTPS-style request + token
   ▼
┌──────────────── service (stdlib http.server + sqlite3) ───────────────┐
│ identity ─► policy ─► budget check ─► session runner ─► audit log     │
└───────────────────────────────┬───────────────────────────────────────┘
                                │ one subprocess per session, per-tenant folders and env
                                ▼
                    agent engine (series 1, ep13 agent.py, unchanged where possible)
                       │ tool calls                         │ model calls
                       ▼                                    ▼
                 sandbox (run_bash)                 credential proxy (loopback)
                 no net / allow-list                 adds the key, counts tokens
                                                            ▼
                                                      model API (Claude or DeepSeek)
```

Principles:
- **Reuse the engine.** The ep13 `agent.py` stays the core. New code wraps it and adds hooks. We change the engine only where a requirement needs it (permissions precedence, a model-call function that goes through the proxy, usage reporting).
- **Standard library only.** `http.server`, `sqlite3`, `subprocess`, `hashlib`, `hmac`, `json`. This keeps the series' "no framework" rule, and the machine has Python 3.9 (so no `match`, no `X | Y` type hints).
- **One folder per episode, copy-forward**, like series 1, so any step can be checked out and run.
- **Every component has a no-key test** (a scripted fake model and fake clock), plus real runs on DeepSeek for the behaviour that needs a model.

## 3. Technical decisions (with my recommendation)

| Decision | Options | Recommendation and why |
|---|---|---|
| Service | stdlib `http.server` vs FastAPI | stdlib: keeps the rule, fewer moving parts. Note it is single-threaded by default; use `ThreadingHTTPServer`. |
| State | JSON files vs SQLite | SQLite: users, budgets, approvals, sessions need queries and transactions. |
| Sandbox on this Mac | Docker vs macOS `sandbox-exec` | `sandbox-exec` (present at `/usr/bin/sandbox-exec`; Docker is not installed here). The docs say Claude Code uses Seatbelt on macOS. Ship a Dockerfile as the deployable variant, marked "not run on this machine" until we can test it. |
| Network allow-list | OS rules vs a small proxy | A small allow-list proxy we write (HTTP CONNECT), like the docs' proxy design. |
| Secrets | env var in the agent vs credential proxy | Credential proxy on loopback: the engine's base URL points to it; the proxy adds the key. |
| Audit integrity | plain log vs hash chain | Hash chain (each line holds the hash of the previous one). Our own addition, labelled as ours. |
| Approvals channel | terminal vs web vs chat | A small HTTP approve/deny endpoint first; a chat webhook as a second step. |
| CI | GitHub Actions vs local | GitHub Actions in the public repo: no-key checks on every push, real evals on a schedule with a repository secret. |

## 4. Phases and work breakdown

Each phase ends with something you can run. Effort is in "sessions" (a session = one working block like the ones we did for episodes 11 to 13).

### Phase 0 · Foundation (1 session)
- Write the threat model on one page: assets (the model key, tenant files, the host), actors (a user, a prompt-injected file, a malicious tool description, another tenant), and what we do not defend against.
- Skeleton of the repo `ep01/` … with the ep13 engine copied in, a fake model for tests, a fake clock.
- Read the docs pages not yet read (admin setup, server-managed settings, network config, zero data retention, the gateway pages).
- **Exit:** requirements table agreed, skeleton runs the ep13 checks.

### Phase A · Who and what is allowed (3 sessions: ep 1 to 3)
- **ep 1 identity and service.** `POST /sessions`, `POST /sessions/<id>/messages`, per-user tokens (hashed in SQLite), per-user folders, a session store. Tests: no token → 401, a token reads only its own sessions.
- **ep 2 policy.** `policy.json` (managed) loaded before user and project rules; precedence managed > project > user; lock flags (`allow_managed_rules_only`, `disable_bypass`). Extend the ep4 `Permissions` class. Tests: a managed deny beats a user allow; a project file that tries to loosen policy is ignored.
- **ep 3 policy under attack.** A red-team set built on the ep12 harness: injection in a file, in a tool description, a path escape, a `curl` to a blocked host. Real runs, 5 per case, with and without the policy.
- **Exit:** R1 and R2 pass their tests.

### Phase B · Isolation (3 sessions: ep 4 to 6)
- **ep 4 sandbox.** `run_bash` runs under a `sandbox-exec` profile: write only inside the tenant's folder, no network by default, allow-list through our proxy. A Dockerfile variant. Tests: `touch ../x` fails; `curl blocked.example` fails; reading `~/.ssh` is denied.
- **ep 5 secrets.** The credential proxy and a test that the engine process has no key in its environment or any file it can read. Pitfall to show: a tool that ignores proxy variables.
- **ep 6 tenancy.** Per-tenant config dir, memory dir, working dir, empty setting sources. A test that tries to cross from tenant A to tenant B by path, by symlink and by memory file.
- **Exit:** R3 and R4 pass.

### Phase C · See it and pay for it (3 sessions: ep 7 to 9)
- **ep 7 audit.** Event schema (id, time, user, session, type, tool, decision, hash). Content (prompts, tool output) off by default. `verify_audit.py` detects a removed or edited line.
- **ep 8 cost.** Read `usage` from each model call, price table, per-user daily budget in SQLite, a stop with a clear message. Measure the overshoot on a run that crosses the cap.
- **ep 9 release gate.** The ep12 harness in CI, pass^k as the gate, a trace saved per failure.
- **Exit:** R5, R6, R8 pass.

### Phase D · Reliability (2 sessions: ep 10 to 11)
- **ep 10 failure handling.** Timeouts at three levels (model call, turn, session), retry with back-off on 429/5xx, resume from the saved session. Real test: kill the process mid-task, resume, finish.
- **ep 11 approvals without a terminal.** An approval queue, an HTTP endpoint, a webhook; a timeout that denies. Test with a fake clock.
- **Exit:** R7 passes.

### Phase E · Ship it (2 sessions: ep 12 to 13)
- **ep 12 deploy.** Dockerfile, a compose file with the service, the proxy and the egress allow-list, a pinned model name, config through environment. Honest note on what we could not run locally.
- **ep 13 data and the checklist.** A retention sweep, secret redaction in logs, a data inventory, a one-page checklist, "what Claude Code has that ours does not", the series ending.
- **Exit:** a fresh clone passes `./check.sh` and a scripted end-to-end demo.

## 5. How each piece is tested (the same method as series 1)

1. A **no-key test** with a fake model and a fake clock. It must fail first (so we know it can fail), then pass.
2. A **real run** on DeepSeek for anything that depends on the model: 5 trials per setup, saved traces, graders that look at outcomes (files, state, the audit log), not at wording.
3. **Read at least one failed trace** per episode before writing the script.
4. **Report null results.** If the test shows nothing, the episode says so.
5. **Facts file.** Every number in a script is computed from the raw run files by code.

## 6. Risks and what we do about them

| Risk | What we do |
|---|---|
| No Docker on this machine | Use `sandbox-exec` for the tested path; the Dockerfile is labelled untested until we can run it |
| `sandbox-exec` is deprecated by Apple | Say so on screen; the docs say Claude Code uses Seatbelt, but we are not copying its code |
| Our sandbox gives a false sense of safety | Show the escapes we know (symlinks, an allowed domain used for exfiltration: the docs warn about it) and list what it does not stop |
| A hash chain is not tamper-proof against someone who rewrites the whole file | Say so; the chain only detects a partial edit; real systems ship logs to a separate store |
| Model behaviour varies | 5 trials, report ranges, never one run |
| Scope creep | Each episode has one exit test; anything else goes to a "not built" list |
| Docs we have not read | Read them in Phase 0; mark anything unconfirmed |
| Cost of real runs | DeepSeek flash, small tasks; budget a rough number per episode before running |

## 7. Repo layout (new public repo, built episode by episode)

```
build-an-enterprise-class-agent/
  README.md  SYLLABUS.md  THREAT-MODEL.md  LICENSE
  articles/        one written article per episode
  ep01/ … ep13/    cumulative code per episode: service/, policy/, sandbox/, proxy/, audit/, tests/, demo/
  .github/workflows/   checks.yml (every push), evals.yml (scheduled)
```

## 8. Order I recommend, and why

1. Phase 0 first: the threat model decides what the tests must prove.
2. Then build **a thin vertical slice before filming anything**: identity + policy + audit around the engine with a fake model (about 1.5 sessions). If the architecture is wrong, we find out before episode 1 is scripted.
3. Then episodes in the order of the plan. Sandbox (ep 4) is the most visual, but it needs the service and policy from ep 1 and 2 to be meaningful.

## 9. Decisions I need from you (my default in brackets)

1. Stay with plain Python and the standard library only? [yes]
2. Start from the finished ep13 agent as the engine? [yes]
3. 13 episodes, or 9 (drop ep 3, 6, 11 and 13 as separate episodes)? [13, decide after Phase A]
4. Sandbox with `sandbox-exec` on this Mac and a Dockerfile as an untested variant? [yes; or install Docker/Colima first so we can test both]
5. First episode: many users (ep 1), or sandbox (ep 4) because it is the most visual? [ep 1, after the vertical slice]
6. Same channels and weekly pace? [same]
7. New public repo `build-an-enterprise-class-agent`: start committing real code there right after Phase 0? [yes]
8. Should real-model runs use Claude (needs a key and costs more) or stay on DeepSeek flash like series 1? [DeepSeek flash]

## 10. What happens after you approve

1. I do Phase 0 (threat model, skeleton, the unread docs) and send you the one-page threat model and the checklist.
2. I build the vertical slice and show you a real run (a request with a token → policy decision → audit line → hash-chain check).
3. Then episode 1 follows the usual flow: research, test, outline, your OK, script, slides, your OK, voice, rough cut, your OK, post.
