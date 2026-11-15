#!/usr/bin/env python3
"""Always-on stats agent for Michael's Xiaohongshu notes.

Built on the five primitives from Anthropic's "Building always-on agents" (2026-11-13):
  inbox       SQLite table of events. Handlers only write rows; one worker reads them.
  timers      Separate table. A schedule (daily digest) and follow-ups (read a note's
              stats 24 h after it went live). The scheduler turns due timers into inbox events.
  memory      Files in memory/: instructions.md (copied from the repo), notes.md, reported.md.
  permissions The run is `claude -p` with an allow-list: read the note list in Chrome,
              read and edit only its own folder (stats.md + memory/). No Bash, no clicks, no publishing.
              The Telegram token never enters the run: the dispatcher reads it itself.

Everything it touches lives in ~/Library/Application Support/stats-agent/ (RUNTIME), which macOS
doesn't guard, so the launchd job needs no Full Disk Access and can't see ~/Documents. The
24-hour numbers go to RUNTIME/stats.md; /xhs-post copies them into x-assistant/posts.md.
`install` (run from the repo) copies agent.py and memory/instructions.md into RUNTIME.
  outbox      SQLite table. The run returns a message (or null to stay quiet); the
              dispatcher sends it to Telegram.

Usage (from anywhere):
  python3 -I stats-agent/agent.py install | uninstall  copy into RUNTIME and add / remove the launchd job
  python3 -I stats-agent/agent.py tick                 scheduler + worker + dispatcher (launchd runs this every 10 min)
  python3 -I stats-agent/agent.py event <kind> [json]  handler: add an event to the inbox (e.g. `event check`)
  python3 -I stats-agent/agent.py status               show inbox, timers, outbox and recent runs
"""
import datetime as dt
import fcntl
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RUNTIME = os.path.expanduser("~/Library/Application Support/stats-agent")
STATE = os.path.join(RUNTIME, "state")
MEM = os.path.join(RUNTIME, "memory")
DB = os.path.join(STATE, "agent.db")
STATS = os.path.join(RUNTIME, "stats.md")
TG_DIR = os.path.expanduser("~/.claude/channels/telegram")
CLAUDE = os.path.expanduser("~/.local/bin/claude")
MODEL = os.environ.get("STATS_AGENT_MODEL", "claude-sonnet-5-5")
DIGEST_AT = "21:15"          # daily schedule, Singapore time (the Mac's local time)
MAX_ATTEMPTS = 3
LABEL = "com.michael.stats-agent"
PLIST = os.path.expanduser("~/Library/LaunchAgents/%s.plist" % LABEL)


def now():
    return dt.datetime.now().replace(microsecond=0)


def fmt(t):
    return t.strftime("%Y-%m-%d %H:%M")


def db():
    os.makedirs(STATE, exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.executescript("""
    CREATE TABLE IF NOT EXISTS inbox (id TEXT PRIMARY KEY, kind TEXT, payload TEXT, status TEXT DEFAULT 'pending',
        attempts INTEGER DEFAULT 0, created TEXT, done TEXT, error TEXT);
    CREATE TABLE IF NOT EXISTS timers (id TEXT PRIMARY KEY, kind TEXT, due TEXT, daily_at TEXT, payload TEXT,
        status TEXT DEFAULT 'active');
    CREATE TABLE IF NOT EXISTS outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, status TEXT DEFAULT 'pending',
        created TEXT, sent TEXT, error TEXT);
    CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, started TEXT, ended TEXT, events TEXT,
        status TEXT, cost REAL, summary TEXT);
    """)
    # the one schedule: a daily digest
    c.execute("INSERT OR IGNORE INTO timers (id, kind, due, daily_at, payload) VALUES (?,?,?,?,?)",
              ("schedule:daily-digest", "schedule", next_daily(DIGEST_AT), DIGEST_AT, "{}"))
    c.commit()
    return c


def next_daily(hhmm, after=None):
    after = after or now()
    h, m = map(int, hhmm.split(":"))
    t = after.replace(hour=h, minute=m, second=0)
    return fmt(t if t > after else t + dt.timedelta(days=1))


# ---- handler: write the event and return at once (deeper checks belong in the run)
def add_event(c, eid, kind, payload):
    cur = c.execute("INSERT OR IGNORE INTO inbox (id, kind, payload, created) VALUES (?,?,?,?)",
                    (eid, kind, json.dumps(payload, ensure_ascii=False), fmt(now())))
    c.commit()
    return cur.rowcount == 1   # 0 = duplicate, deduped by id


# ---- scheduler: due timers become inbox events; timers never start runs themselves
def schedule(c):
    for t in c.execute("SELECT * FROM timers WHERE status='active' AND due <= ?", (fmt(now()),)).fetchall():
        payload = json.loads(t["payload"] or "{}")
        add_event(c, "%s@%s" % (t["id"], t["due"]), t["kind"], dict(payload, timer=t["id"], due=t["due"]))
        if t["kind"] == "schedule":
            c.execute("UPDATE timers SET due=? WHERE id=?", (next_daily(t["daily_at"]), t["id"]))
        else:
            c.execute("UPDATE timers SET status='done' WHERE id=?", (t["id"],))
    c.commit()


def read(path, tail=None):
    if not os.path.exists(path):
        return ""
    text = open(path, encoding="utf-8").read()
    return text[-tail:] if tail else text


def prompt_for(events):
    ev = "\n".join("- %s (%s) %s" % (e["id"], e["kind"], e["payload"]) for e in events)
    return """You are Michael's always-on stats agent. You woke up for a run; when it ends you go back to sleep.
Current time (Singapore): {now}

Follow memory/instructions.md exactly. Your memory, loaded for this run:

### memory/instructions.md
{ins}

### memory/notes.md (what you learned before)
{notes}

### memory/reported.md (the last messages already sent to Michael; don't repeat them)
{rep}

### Events in this run (batched; handle them all in this one run)
{ev}

Paths: your stats file is {stats} ; your memory folder is {mem}
End your run with ONE fenced ```json block and nothing after it:
{{"message": "<Telegram text in Chinese, or null to stay quiet>", "follow_ups": [{{"title": "<note title>", "due": "YYYY-MM-DD HH:MM"}}], "summary": "<one line: what you did>"}}
""".format(now=fmt(now()), ins=read(os.path.join(MEM, "instructions.md")),
           notes=read(os.path.join(MEM, "notes.md")) or "(empty)",
           rep=read(os.path.join(MEM, "reported.md"), tail=3000) or "(nothing sent yet)",
           ev=ev, stats=STATS, mem=MEM)


def claude_cmd():
    allowed = [
        "mcp__claude-in-chrome__tabs_context_mcp", "mcp__claude-in-chrome__tabs_create_mcp",
        "mcp__claude-in-chrome__navigate", "mcp__claude-in-chrome__get_page_text",
        "mcp__claude-in-chrome__tabs_close_mcp",
        "Read(/%s/**)" % RUNTIME,
        "Edit(/%s)" % STATS, "Write(/%s)" % STATS, "Edit(/%s/**)" % MEM, "Write(/%s/**)" % MEM,
    ]
    denied = ["Bash", "WebFetch", "WebSearch", "Agent", "NotebookEdit",
              "mcp__claude-in-chrome__computer", "mcp__claude-in-chrome__javascript_tool",
              "mcp__claude-in-chrome__form_input", "mcp__claude-in-chrome__file_upload",
              "mcp__claude-in-chrome__browser_batch"]
    return [CLAUDE, "-p", "--chrome", "--model", MODEL, "--max-turns", "30", "--output-format", "json",
            "--permission-mode", "dontAsk",
            "--allowedTools", ",".join(allowed), "--disallowedTools", ",".join(denied),
            # a nested session must never load the Telegram plugin (it would steal the bot from the live session)
            "--settings", '{"enabledPlugins":{"telegram@claude-plugins-official":false}}']


def parse_result(out):
    data = json.loads(out)
    text = data.get("result") or ""
    m = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.S)
    if not m:
        raise ValueError("run ended without a json block: " + text[-300:])
    return json.loads(m[-1]), data.get("total_cost_usd")


# ---- worker: one per inbox (file lock), batches every pending event into one run
def work(c):
    lock = open(os.path.join(STATE, "worker.lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return   # another worker is mid-run; it (or the next tick) picks these up
    events = c.execute("SELECT * FROM inbox WHERE status='pending' ORDER BY created").fetchall()
    if not events:
        return
    ids = [e["id"] for e in events]
    c.execute("UPDATE inbox SET attempts=attempts+1 WHERE id IN (%s)" % ",".join("?" * len(ids)), ids)
    run = c.execute("INSERT INTO runs (started, events, status) VALUES (?,?,?)",
                    (fmt(now()), json.dumps(ids, ensure_ascii=False), "running")).lastrowid
    c.commit()
    try:
        p = subprocess.run(claude_cmd(), input=prompt_for(events), capture_output=True, text=True,
                           cwd=RUNTIME, timeout=900)
        if p.returncode != 0:
            raise RuntimeError((p.stderr or p.stdout)[-500:])
        res, cost = parse_result(p.stdout)
    except Exception as e:  # leave events pending for a retry; give up after MAX_ATTEMPTS
        err = str(e)[:500]
        c.execute("UPDATE runs SET ended=?, status='failed', summary=? WHERE id=?", (fmt(now()), err, run))
        c.execute("UPDATE inbox SET error=? WHERE id IN (%s)" % ",".join("?" * len(ids)), [err] + ids)
        dead = c.execute("SELECT id FROM inbox WHERE status='pending' AND attempts>=? AND id IN (%s)"
                         % ",".join("?" * len(ids)), [MAX_ATTEMPTS] + ids).fetchall()
        if dead:
            c.execute("UPDATE inbox SET status='failed' WHERE id IN (%s)" % ",".join("?" * len(dead)), [d[0] for d in dead])
            c.execute("INSERT INTO outbox (text, created) VALUES (?,?)",
                      ("⚠️ 数据助手连续 %d 次没读到笔记数据（%s）。Chrome 开着吗？Claude in Chrome 连上了吗？" % (MAX_ATTEMPTS, err[:120]), fmt(now())))
        c.commit()
        return
    for f in res.get("follow_ups") or []:
        title, due = f.get("title"), f.get("due")
        if title and due and re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d$", due):
            c.execute("INSERT OR IGNORE INTO timers (id, kind, due, payload) VALUES (?,?,?,?)",
                      ("follow_up:" + title, "follow_up", due, json.dumps({"title": title}, ensure_ascii=False)))
    if res.get("message"):
        c.execute("INSERT INTO outbox (text, created) VALUES (?,?)", (res["message"], fmt(now())))
    c.execute("UPDATE inbox SET status='done', done=?, error=NULL WHERE id IN (%s)" % ",".join("?" * len(ids)),
              [fmt(now())] + ids)
    c.execute("UPDATE runs SET ended=?, status='ok', cost=?, summary=? WHERE id=?",
              (fmt(now()), cost, res.get("summary"), run))
    c.commit()


# ---- dispatcher: the only place that holds the Telegram token
def telegram_send(text):
    env = dict(l.strip().split("=", 1) for l in open(os.path.join(TG_DIR, ".env")) if "=" in l)
    token = env["TELEGRAM_BOT_TOKEN"].strip().strip('"')
    chat = json.load(open(os.path.join(TG_DIR, "access.json")))["allowFrom"][0]
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    with urllib.request.urlopen("https://api.telegram.org/bot%s/sendMessage" % token, data=data, timeout=20) as r:
        if not json.load(r).get("ok"):
            raise RuntimeError("telegram said not ok")


def dispatch(c):
    for m in c.execute("SELECT * FROM outbox WHERE status='pending' ORDER BY id").fetchall():
        try:
            telegram_send(m["text"])
            c.execute("UPDATE outbox SET status='sent', sent=? WHERE id=?", (fmt(now()), m["id"]))
            with open(os.path.join(MEM, "reported.md"), "a", encoding="utf-8") as f:   # past-messages memory
                f.write("\n## %s\n%s\n" % (fmt(now()), m["text"]))
        except Exception as e:
            c.execute("UPDATE outbox SET error=? WHERE id=?", (str(e)[:300].replace(TG_DIR, "~"), m["id"]))
        c.commit()


def status(c):
    for name, q in [("inbox", "SELECT id, kind, status, attempts, created, error FROM inbox ORDER BY created DESC LIMIT 10"),
                    ("timers", "SELECT id, kind, due, status FROM timers ORDER BY due"),
                    ("outbox", "SELECT id, status, created, sent, substr(text,1,40) AS text FROM outbox ORDER BY id DESC LIMIT 5"),
                    ("runs", "SELECT id, started, ended, status, cost, substr(summary,1,90) AS summary FROM runs ORDER BY id DESC LIMIT 5")]:
        print("== " + name)
        for r in c.execute(q):
            print("  " + " | ".join("" if v is None else str(v) for v in r))


def install():
    import shutil
    os.makedirs(MEM, exist_ok=True)
    os.makedirs(STATE, exist_ok=True)
    shutil.copy2(os.path.abspath(__file__), os.path.join(RUNTIME, "agent.py"))
    shutil.copy2(os.path.join(HERE, "memory", "instructions.md"), os.path.join(MEM, "instructions.md"))
    log = os.path.join(STATE, "launchd.log")
    path = "%s:%s:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin" % (os.path.dirname(CLAUDE), os.path.expanduser("~/.local/node/bin"))
    plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>{label}</string>
  <key>ProgramArguments</key><array><string>{py}</string><string>-I</string><string>{script}</string><string>tick</string></array>
  <key>StartInterval</key><integer>600</integer>
  <key>RunAtLoad</key><true/>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>{path}</string></dict>
  <key>StandardOutPath</key><string>{log}</string>
  <key>StandardErrorPath</key><string>{log}</string>
</dict></plist>
""".format(py=os.path.realpath(sys.executable), label=LABEL, script=os.path.join(RUNTIME, "agent.py"), path=path, log=log)
    open(PLIST, "w").write(plist)
    subprocess.run(["launchctl", "unload", PLIST], capture_output=True)
    subprocess.run(["launchctl", "load", PLIST], check=True)
    print("installed: %s (every 10 min while the Mac is awake)" % PLIST)


def uninstall():
    subprocess.run(["launchctl", "unload", PLIST], capture_output=True)
    if os.path.exists(PLIST):
        os.remove(PLIST)
    print("removed " + PLIST)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "tick"
    if cmd in ("install", "uninstall"):
        return install() if cmd == "install" else uninstall()
    c = db()
    if cmd == "tick":
        schedule(c)
        work(c)
        dispatch(c)
    elif cmd == "event":
        kind = sys.argv[2] if len(sys.argv) > 2 else "check"
        payload = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        added = add_event(c, "manual:%s@%s" % (kind, fmt(now())), kind, payload)
        print("queued" if added else "duplicate, ignored")
    elif cmd == "status":
        status(c)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
