# Series 2 episode 1 research: many users, one agent service (official sources only; read 2026-11-25)

Sources, downloaded as the pages' Markdown (code.claude.com/docs/en/): agent-sdk/hosting (24,497 bytes, read in full), authentication (37,977; read the sections on team setup, restricting login, credential management, precedence and profiles), agent-sdk/sessions (the "Resume across hosts" part), agent-sdk/session-storage (the opening). Check any quote on the page before it goes on screen.

## One session, one process (agent-sdk/hosting)
- The Agent SDK starts a `claude` CLI subprocess that owns a shell, a working directory and the session files. "One agent session maps to one subprocess." N sessions need N processes.
- Sessions inherit the application's working directory unless each gets its own `cwd`.
- A starting size: 1 GiB RAM, 5 GiB disk, 1 CPU per agent (a floor).
- No top-level session timeout; bound it with max turns.

## Who checks identity (agent-sdk/hosting, "Auth and secrets")
- Inbound: "put authentication at a gateway in front of the agent container." The agent should receive pre-authenticated requests and should not be the part that validates user tokens. **Our design matches: the service checks the token; the engine never sees it.**
- Model key: the subprocess reads it from its environment, or a proxy outside the container adds it (episode 5).

## State on local disk (agent-sdk/hosting, sessions, session-storage)
- Session transcripts (`~/.claude/projects/`), `CLAUDE.md` files and working-folder files are on local disk. None survive a restart, a scale-down or a move to another node.
- A `SessionStore` adapter mirrors transcripts to a database or object store. Transcripts only; writes are best-effort (a failed batch is dropped and a `mirror_error` message is sent).
- Resuming on another host: use a session store, move the file, or do not rely on resume and pass the needed results into a new session.

## Several tenants in one container (agent-sdk/hosting) (mainly episode 6)
- Skip filesystem settings (`setting_sources=[]`), disable auto memory, a config folder per tenant, a working folder per tenant, egress rules per tenant.

## Credentials (authentication)
- Claude Code's order when several are present: cloud provider variables; `ANTHROPIC_AUTH_TOKEN` (sent as `Authorization: Bearer`); `ANTHROPIC_API_KEY` (sent as `X-Api-Key`); `apiKeyHelper`; `CLAUDE_CODE_OAUTH_TOKEN`; profiles and federation; the `/login` subscription. A signed-in Claude apps gateway outranks the list.
- The page's own warning: with a subscription and `ANTHROPIC_API_KEY` set, Claude Code uses the key once approved, which can fail if the key belongs to a disabled or expired organization. `/status` shows which is in use.
- Admins: `forceLoginMethod` and `forceLoginOrgUUID` in managed settings; under them, environment credentials are blocked at startup. A saved Console credential's organization is **not** checked at startup.

## Measured by us, not from the docs (anthropic Python SDK 0.125.0, a stub server)
This is the SDK our engine uses. It is not Claude Code, and these results say nothing about Claude Code.
- Key given in code, `ANTHROPIC_BASE_URL` left over: the call and the key went to the old address. `ANTHROPIC_CUSTOM_HEADERS` was applied too.
- Key from `ANTHROPIC_API_KEY`, token left over: both headers were sent.
- Key given in code, token left over: the token was **not** sent. (We expected it would be; our first test was wrong.)

## What this means for our version (done and tested, `ep01/`)
- Token → user → folder → session in a small service; one engine process per message with an environment built from nothing; the conversation saved per session.
- Open: no policy, no sandbox, the engine holds the key. Read-only mode until episode 2.
