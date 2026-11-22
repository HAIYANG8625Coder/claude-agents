# Implementation plan: how to build an enterprise-class agent (draft for approval, 2026-11-21; revised the same day after review)

This plan says **what we build, in what order, how each piece is tested, and where it can go wrong**. It sits under `SERIES2-PLAN.md` (the 13-episode story) and `SERIES2-RESEARCH.md` (what the official docs say). Nothing here is built yet.

## 1. What "enterprise-class" means here (the 8 requirements)

We do not claim a certification. We mean an agent service that meets eight concrete requirements. Each one has a test that can fail.

| # | Requirement | Plain meaning | Done when |
|---|---|---|---|
| R1 | Identity | Every request has a known user | a request without a valid token is refused, and every event carries a user id |
| R2 | Policy | Rules the user cannot switch off | a managed deny rule beats a user allow rule, in a test |
| R3 | Isolation | A command or a tenant cannot touch what it should not | a sandboxed command cannot write outside its folder or reach a blocked host; the engine process cannot read the SQLite db, the audit log or the key file; tenant A cannot read tenant B |
| R4 | Secrets | The agent process never holds the model key | the key is not in the engine's environment or any file it can read; a command cannot reach the credential proxy; a test greps and tries |
| R5 | Audit | Afterwards we can say who did what, and whether it was allowed | one event per prompt, model call, tool call and decision, each marked with who wrote it (service, proxy or engine); a deleted line is detected |
| R6 | Cost | A ceiling per user and per day | the proxy refuses the model call that would cross the daily cap; the overshoot is at most one call |
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
   ┌──── sandbox profile around the WHOLE engine process ────┐
   │  agent engine (series 1, ep13 agent.py)                 │
   │  can write: its tenant folder only                      │
   │  cannot read: SQLite db, audit log, key file, ~/.ssh    │
   │  network: only the proxy port, with a per-session token │
   │     │ tool calls (run_bash: no network at all,          │
   │     │ the proxy port included)                          │
   └─────┼───────────────────────────────┬───────────────────┘
         ▼                               │ model calls + session token
   commands in the tenant folder         ▼
                              credential proxy (loopback, outside the sandbox)
                              checks the session token, adds the key,
                              counts tokens, refuses the call that would cross
                              the budget, writes audit events for model calls
                                         ▼
                              model API (Claude or DeepSeek)
```

Principles:
- **Sandbox the engine, not only its commands.** The engine runs as the same OS user as the service. If only `run_bash` were sandboxed, the engine's own file tools and Python code could read the SQLite database, the audit log and the proxy's key file. R3, R4 and R5 would then rest on path checks inside the engine. So one `sandbox-exec` profile wraps the whole engine subprocess. `run_bash` gets a stricter profile inside it.
- **Whoever enforces a rule sits outside the sandbox.** Budget checks, the key and the audit log live in the service and the proxy, never in the engine.
- **Reuse the engine.** The ep13 `agent.py` stays the core. New code wraps it and adds hooks. We change the engine only where a requirement needs it (permissions precedence, a model-call function that goes through the proxy, usage reporting). Known change: `make_client()` in ep13 has the DeepSeek URL written in and reads a real key from the environment. It must take the proxy URL and a per-session token instead.
- **Say where a fact comes from.** The service and the proxy write audit events from what they see themselves (requests, model calls, tokens, budget stops). Tool calls and permission decisions happen inside the engine, so the engine reports them. Those events are marked `source: engine` and labelled on screen as self-reported.
- **Standard library only.** `http.server`, `sqlite3`, `subprocess`, `hashlib`, `hmac`, `json`. This keeps the series' "no framework" rule, and the machine has Python 3.9 (so no `match`, no `X | Y` type hints).
- **One folder per episode, copy-forward**, like series 1, so any step can be checked out and run.
- **Every component has a no-key test** (a scripted fake model and fake clock), plus real runs on DeepSeek for the behaviour that needs a model.

## 3. Technical decisions (with my recommendation)

| Decision | Options | Recommendation and why |
|---|---|---|
| Service | stdlib `http.server` vs FastAPI | stdlib: keeps the rule, fewer moving parts. Use `ThreadingHTTPServer`, since the plain server handles one request at a time. The Python docs say `http.server` is not meant for production, so the video says so. No TLS: the service listens on loopback only. |
| State | JSON files vs SQLite | SQLite: users, budgets, approvals, sessions need queries and transactions. With threads: one connection per thread, WAL mode, a `busy_timeout`. |
| Sandbox on this Mac | Docker vs macOS `sandbox-exec` | Both, and both are tested on this Mac. `sandbox-exec` (at `/usr/bin/sandbox-exec`) wraps the whole engine process (see section 2); the docs say Claude Code uses Seatbelt on macOS. Docker runs here through Colima (installed 2026-11-22: docker 29.10, Colima 0.10.3, compose 5.8; a 2026-11-22 test container with `--network none --cap-drop ALL --read-only` and a non-root user could not reach the network or write to `/`). CI on Linux runs the Docker variant too. |
| Network allow-list | OS rules vs a small proxy | A small allow-list proxy we write (HTTP CONNECT), like the docs' proxy design. `run_bash` gets no network at all, the loopback ports of our own proxies included, so a command cannot spend the key with `curl localhost:<port>`. |
| Secrets | env var in the agent vs credential proxy | Credential proxy on loopback: the engine's base URL points to it. The engine gets a per-session token, never the key; the proxy checks the token (so it knows the tenant) and adds the key. The key file is readable by the proxy only. |
| Budget | check before each message vs check on every model call | On every model call, in the proxy: it refuses the call that would cross the limit. The overshoot is then at most one call, a clean number to show. A check before each message would let one long turn make many calls past the limit. |
| Audit integrity | plain log vs hash chain | Hash chain (each line holds the hash of the previous one), written by the service and the proxy, outside the sandbox. Our own addition, labelled as ours. |
| Admin | file edited by hand vs admin role | Two roles: `user` and `admin`. Only an admin token can change the managed policy (`PUT /policy`), and the change is an audit event. |
| Approvals channel | terminal vs web vs chat | A small HTTP approve/deny endpoint first; a chat webhook as a second step. |
| CI | GitHub Actions vs local | GitHub Actions in the public repo: no-key checks on every push, real evals on a schedule with a repository secret (forks never get it). The Linux runners have no `sandbox-exec` but do have Docker, so CI tests the Docker sandbox, and the Mac runs both the `sandbox-exec` and the Docker tests. Each sandbox test names the variant it covers. |

## 4. Phases and work breakdown

Each phase ends with something you can run. Effort is in "sessions" (a session = one working block like the ones we did for episodes 11 to 13).

### Phase 0 · Foundation (1 session)
- Write the threat model on one page: assets (the model key, tenant files, the host), actors (a user, a prompt-injected file, a malicious tool description, another tenant), and what we do not defend against.
- Skeleton of the repo `ep01/` … with the ep13 engine copied in, a fake model for tests, a fake clock.
- Read the docs pages not yet read (admin setup, server-managed settings, network config, zero data retention, the gateway pages).
- **Exit:** requirements table agreed, skeleton runs the ep13 checks.

### Phase A · Who and what is allowed (3 sessions: ep 1 to 3)
- **ep 1 identity and service.** `POST /sessions`, `POST /sessions/<id>/messages`, per-user tokens (hashed in SQLite) with a role (`user` or `admin`), per-user folders, a session store. Tests: no token → 401, a token reads only its own sessions, a user token cannot change the policy.
- **ep 2 policy.** `policy.json` (managed) loaded before user and project rules; precedence managed > project > user; lock flags (`allow_managed_rules_only`, `disable_bypass`). Extend the ep4 `Permissions` class. Tests: a managed deny beats a user allow; a project file that tries to loosen policy is ignored.
- **ep 3 policy under attack.** A red-team set built on the ep12 harness: injection in a file, in a tool description, a path escape, a `curl` to a blocked host. Real runs, 5 per case, with and without the policy.
- **Exit:** R1 and R2 pass their tests.

### Phase B · Isolation (3 sessions: ep 4 to 6)
- **ep 4 sandbox.** Two layers. The whole engine process runs under a `sandbox-exec` profile: writes only inside the tenant's folder, no reads of the service's db, audit log or key file, network only to the proxy port. `run_bash` runs under a stricter profile inside it, with no network at all (loopback included) unless the policy allows a host through the allow-list proxy. A Dockerfile variant, tested on the Mac (Colima) and in CI. Tests: `touch ../x` fails; `curl blocked.example` fails; reading `~/.ssh` is denied; the engine's `read_file` on the SQLite db fails; `curl localhost:<proxy port>` from a command fails.
- **ep 5 secrets.** The credential proxy with a per-session token, and tests that the engine process has no key in its environment or any file it can read, and that a wrong or expired session token is refused. Engine change: `make_client()` takes the proxy URL and the session token. Pitfall to show: a tool that ignores proxy variables.
- **ep 6 tenancy.** Per-tenant config dir, memory dir, working dir, empty setting sources. A test that tries to cross from tenant A to tenant B by path, by symlink and by memory file.
- **Exit:** R3 and R4 pass.

### Phase C · See it and pay for it (3 sessions: ep 7 to 9)
- **ep 7 audit.** Event schema (id, time, user, session, type, tool, decision, source, hash). The service and the proxy write the log; the engine sends its tool and decision events to the service, which marks them `source: engine` (self-reported). Content (prompts, tool output) off by default. `verify_audit.py` detects a removed or edited line. Test: the engine cannot open the log file.
- **ep 8 cost.** The proxy reads `usage` from each model call, prices it, and keeps the per-user daily total in SQLite. Before each call it estimates the cost and refuses the call that would cross the cap, with a clear message. Measure the overshoot on a run that crosses the cap (the target is at most one call).
- **ep 9 release gate.** The ep12 harness in CI, pass^k as the gate, a trace saved per failure. CI on Linux runs the Docker sandbox tests; the Mac runs both variants, and the report says which variant ran where.
- **Exit:** R5, R6, R8 pass.

### Phase D · Reliability (2 sessions: ep 10 to 11)
- **ep 10 failure handling.** Timeouts at three levels (model call, turn, session), retry with back-off on 429/5xx, resume from the saved session. Real test: kill the process mid-task, resume, finish.
- **ep 11 approvals without a terminal.** An approval queue, an HTTP endpoint, a webhook; a timeout that denies. Test with a fake clock.
- **Exit:** R7 passes.

### Phase E · Ship it (2 sessions: ep 12 to 13)
- **ep 12 deploy.** Dockerfile, a compose file with the service, the proxy and the egress allow-list, a pinned model name, config through environment. The whole compose setup runs on this Mac through Colima; note anything that differs on a real Linux server (Colima runs Linux in a VM).
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
| Docker on this Mac runs inside a Colima VM, not on a Linux host | Run the Docker tests in CI on Linux as well, and say on screen that the Mac runs Linux in a VM |
| A command spends the key through the local proxy | `run_bash` has no network, loopback included; the proxy also requires a per-session token |
| The engine reads or edits what it should not (db, log, key) | The whole engine process is sandboxed, and a test tries each file |
| Self-reported audit events can lie | Mark them `source: engine` and say so on screen; only service and proxy events are observed facts |
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
2. Then build **a thin vertical slice before filming anything**: identity + policy + audit around the engine with a fake model, with the engine process already inside a minimal `sandbox-exec` profile and its model calls going through a stub proxy (about 2 sessions). The sandbox-around-the-engine design is the riskiest part, so it goes into the slice. If the architecture is wrong, we find out before episode 1 is scripted.
3. Then episodes in the order of the plan. Sandbox (ep 4) is the most visual, but it needs the service and policy from ep 1 and 2 to be meaningful.

## 9. Decisions I need from you (my default in brackets)

This list replaces the open questions in `SERIES2-PLAN.md`. The repo question there is settled: series 2 has its own public repo.

1. Stay with plain Python and the standard library only? [yes]
2. Start from the finished ep13 agent as the engine? [yes]
3. 13 episodes, or 9 (drop ep 3, 6, 11 and 13 as separate episodes)? [13, decide after Phase A]
4. ~~Sandbox with `sandbox-exec` only, Dockerfile untested?~~ Settled 2026-11-22: Docker is installed through Colima, so both variants are tested on this Mac.
5. First episode: many users (ep 1), or sandbox (ep 4) because it is the most visual? [ep 1, after the vertical slice]
6. Same channels and weekly pace? [same]
7. New public repo `build-an-enterprise-class-agent`: start committing real code there right after Phase 0? [yes]
8. Should real-model runs use Claude (needs a key and costs more) or stay on DeepSeek flash like series 1? [DeepSeek flash]

## 10. What happens after you approve

1. I do Phase 0 (threat model, skeleton, the unread docs) and send you the one-page threat model and the checklist.
2. I build the vertical slice and show you a real run (a request with a token → policy decision → sandboxed engine → model call through the proxy → audit line → hash-chain check).
3. Then episode 1 follows the usual flow: research, test, outline, your OK, script, slides, your OK, voice, rough cut, your OK, post.
