# Series 2: what was checked on 2026-11-24 (results of the unconfirmed-items audit)

All tests were run on this Mac (macOS 27.2.1, Python 3.9.6, Docker server 29.5.2 on Colima). Scratch files: the session scratchpad `sbx/`. Re-run them in Phase 0 from a plain terminal and keep them in the repo.

## Confirmed by running it
| Item | Result |
|---|---|
| `sandbox-exec` works | Yes. The earlier exit 137 came from a bad test (`-n no-network` names a profile that is not there). A profile file works. |
| Seatbelt engine profile for Python 3.9 | Python starts under `(deny default)` with reads limited to `/usr`, `/System`, `/Library`, `/private/var/db`, `/private/etc`, `/dev`, `/var/db`, `/private/var/folders`, the tenant folder and `(literal "/")`. Without `(literal "/")` it aborts (exit 134). |
| What that profile blocks | read of a file outside the tenant folder, listing `~/.ssh`, write outside the tenant folder (`../x`), write to `$HOME`, read through a symlink that points outside, connect to loopback port 8700. All raised PermissionError. |
| What it allows | read and write inside the tenant folder; connect to loopback port 8701 only (`(allow network-outbound (remote ip "localhost:8701"))`). So TRD open question 2 is answered: one loopback port can be allowed while others are blocked. |
| Command profile (no network rule) | connect to 8701 blocked. |
| Docker works, Colima runs | `docker run` works; `colima list` says Running (4 CPU, 6 GiB, 60 GiB). `colima status` itself hangs: cosmetic, use `colima list`. |
| Hardened container flags | `--cap-drop ALL --read-only --user 1000:1000 --security-opt no-new-privileges --tmpfs /tmp --network none`: write to `/` refused, `/tmp` works, no network. |
| `--internal` Docker network | A container on it reaches a peer container by name, cannot reach the internet and cannot resolve `host.docker.internal`. This is the network for engine containers. |
| DeepSeek usage fields | `deepseek-flash` through the Anthropic-shaped endpoint returns `usage.input_tokens` and `usage.output_tokens` in a plain call (37 / 50), a streamed call (37 / 50, via `get_final_message`) and a tool call (284 / 37, stop `tool_use`). R6 can price from them. Cache fields not checked. |

## New finding (changes the design)
On a **default** Docker network under Colima, a container reached host services bound to `127.0.0.1` through `host.docker.internal` and `host.lima.internal` (tested with a loopback-only listener). So the TRD's earlier worry ("the container cannot reach the host loopback") was the wrong way round: **it can**, which would let a container reach `agentd` on 8700. Rule for the design: engine and command containers run only on an `--internal` network, never on the default bridge; `keyproxy` runs as a container on that network. Test this in Phase 0 for every container the runner starts.

## Confirmed from the docs read on 2026-11-24 (six pages; one subagent fetch, so check quotes on the page before they go on screen)
- admin-setup: delivery order server-managed (highest), plist/registry, file-based, Windows HKCU (lowest, "treat as a convenience default rather than an enforcement channel"). Arrays such as `permissions.allow` and `permissions.deny` merge, so developers can extend managed lists but not remove entries. Lockdown keys: `allowManagedPermissionRulesOnly`, `permissions.disableBypassPermissionsMode`, `sandbox.enabled`, `sandbox.network.allowedDomains`. **Naming:** our PRD lock `allow_managed_rules_only` is our own spelling of `allowManagedPermissionRulesOnly`; say so on screen.
- server-managed-settings: set at claude.ai (Teams or Enterprise, Owner role); fetched at startup and polled hourly; `forceRemoteSettingsRefresh: true` makes the CLI exit if the fetch fails (fail closed); cache expires 24 h after the last good fetch. Security approval dialogs for hooks, `apiKeyHelper` and proxy settings. The last part of the page (summary only, unverified) says it is a client-side control, not a security boundary.
- managed-mcp: `managed-mcp.json` gives exclusive control; denylists merge from every scope and nothing overrides a deny match; a `serverName` entry "is not a security control".
- network-config: `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`; no SOCKS support; mTLS variables; API streaming timeouts `API_TIMEOUT_MS`, `CLAUDE_STREAM_IDLE_TIMEOUT_MS` (useful for episode 10).
- zero-data-retention: only for qualified Claude for Enterprise accounts, enabled by Anthropic, not from admin settings, direct Anthropic platform only (not Bedrock, Vertex, Foundry); cloud sessions, `/feedback`, `/share` and Remote Control are off under ZDR.
- hipaa-setup: needs Claude Enterprise, a BAA and direct Claude API sign-in; a gateway or custom `ANTHROPIC_BASE_URL` is NOT eligible. Relevant to us: our service is a gateway-like design, so it can never claim to be a HIPAA setup of Claude Code. Say so in episode 13.

## Still unconfirmed
- The Claude apps gateway pages and plugins/org were not read.
- The last part of server-managed-settings and of the permissions page came from a model summary.
- Seatbelt profile: tested with a Python probe only. The real engine (anthropic SDK, httpx, TLS certs, the engine's own file use) is untested until Phase 0.
- Docker flags were tested on Alpine, not on our engine image.
- Whether the Docker `--internal` result holds on Linux in CI is untested (Docker on Linux differs from Colima).
- All *proposed* numbers in the TRD are still targets.
