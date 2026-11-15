#!/usr/bin/env python3
"""Always-on Singapore briefing: a private 10–12 minute English episode on Singapore every morning, sent to Telegram.

The ai-podcast agent (itself a rebuild of ningcodes/CommuteAIBrief, MIT) pointed at Singapore: government
newsrooms, local media, r/singapore and big local creators. Same five parts from "Building always-on agents":
  inbox       SQLite table of events (`edition` for a date). Handlers only write rows; one worker reads them.
  timers      A daily timer (EDITION_AT, local time) that drops an `edition` event into the inbox.
  memory      memory/: instructions.md (editor rules), collector.md, listener.md, interests.json,
              seen.json (links used before) and every past run in runs/ (the last three briefs are read).
  permissions Two separate `claude -p` sessions with allow-lists, both without Bash:
                collector  reads the capture, may WebSearch/WebFetch to find a moved feed, writes one report;
                editor     reads the ledger and the originals, writes decisions.json and brief.json only.
              The program itself does every fetch, the checks, the voice and the sending.
              The Telegram token never enters a run.
  outbox      SQLite table. The episode (audio + notes) or a failure notice; the dispatcher sends it.

The pipeline for one date (each stage writes its files into runs/<date>/ and can be re-run):
  capture → ledger → collector → editor phase 1 (decide + shortlist) → fetch originals →
  editor phase 2 (read, select, write) → gate (+ one fix round) → voice (local Qwen3-TTS) → outbox

Everything lives in ~/Library/Application Support/sg-podcast/ (RUNTIME), outside ~/Documents. The voice
(Python venv + Qwen3-TTS model) is shared, read-only, with ai-podcast so the 2.9 GB model exists once.

Usage:
  python3 -I agents/sg-podcast/podcast.py install | uninstall   copy into RUNTIME, add / remove the launchd job
  python3 -I podcast.py tick                                    scheduler + worker + dispatcher (launchd, every 10 min)
  python3 -I podcast.py event edition [YYYY-MM-DD]              queue an edition now
  python3 -I podcast.py run [YYYY-MM-DD] [--from STAGE] [--to STAGE]   run stages in the foreground (testing)
  python3 -I podcast.py status                                  inbox, timers, outbox, recent runs
"""
import datetime as dt
import fcntl
import html
import html.parser
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import urllib.parse
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
RUNTIME = os.path.expanduser("~/Library/Application Support/sg-podcast")
VOICE_RUNTIME = os.path.expanduser("~/Library/Application Support/ai-podcast")   # shared venv + model
STATE = os.path.join(RUNTIME, "state")
MEM = os.path.join(RUNTIME, "memory")
RUNS = os.path.join(RUNTIME, "runs")
DB = os.path.join(STATE, "agent.db")
VENV_PY = os.path.join(VOICE_RUNTIME, "venv-tts", "bin", "python")
TG_DIR = os.path.expanduser("~/.claude/channels/telegram")
CLAUDE = os.path.expanduser("~/.local/bin/claude")
EDITOR_MODEL = os.environ.get("PODCAST_EDITOR_MODEL", "claude-sonnet-5-5")
COLLECTOR_MODEL = os.environ.get("PODCAST_COLLECTOR_MODEL", "claude-sonnet-5-5")
EDITION_AT = "07:30"         # local time (the Mac's clock, Singapore); before ai-podcast at 08:00 so the two voices never overlap
WINDOW_HOURS = 72            # ministries publish on weekdays, so a weekend-proof window
LABEL = "com.michael.sg-podcast"
PLIST = os.path.expanduser("~/Library/LaunchAgents/%s.plist" % LABEL)
STAGES = ["capture", "ledger", "collector", "shortlist", "originals", "write", "gate", "voice", "deliver"]
WORDS = (1300, 1700)         # 10–12 minutes at the voice's ~137 words a minute; the measured audio is what counts
MAX_ATTEMPTS = 2

sys.path.insert(0, HERE)
import capture  # noqa: E402  (same folder; copied next to this file by install)


def now():
    return dt.datetime.now().replace(microsecond=0)


def fmt(t):
    return t.strftime("%Y-%m-%d %H:%M")


def rd(date, *p):
    return os.path.join(RUNS, date, *p)


def jload(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def jsave(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def log(date, msg):
    line = "%s %s" % (fmt(now()), msg)
    print(line, flush=True)
    with open(rd(date, "run.log"), "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------- inbox, timers, outbox
def db():
    os.makedirs(STATE, exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.executescript("""
    CREATE TABLE IF NOT EXISTS inbox  (id TEXT PRIMARY KEY, kind TEXT, payload TEXT, status TEXT DEFAULT 'pending',
                                       attempts INTEGER DEFAULT 0, created TEXT, done TEXT, error TEXT);
    CREATE TABLE IF NOT EXISTS timers (id TEXT PRIMARY KEY, kind TEXT, due TEXT, payload TEXT, status TEXT DEFAULT 'waiting');
    CREATE TABLE IF NOT EXISTS outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, payload TEXT,
                                       status TEXT DEFAULT 'pending', created TEXT, sent TEXT, error TEXT);
    CREATE TABLE IF NOT EXISTS runs   (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, started TEXT, ended TEXT,
                                       status TEXT, cost REAL, summary TEXT);
    """)
    return c


def next_daily(hhmm, after):
    h, m = map(int, hhmm.split(":"))
    t = after.replace(hour=h, minute=m, second=0)
    return t if t > after else t + dt.timedelta(days=1)


def add_event(c, eid, kind, payload):
    cur = c.execute("INSERT OR IGNORE INTO inbox (id, kind, payload, created) VALUES (?,?,?,?)",
                    (eid, kind, json.dumps(payload), fmt(now())))
    c.commit()
    return cur.rowcount == 1


def schedule(c):
    t = c.execute("SELECT * FROM timers WHERE id='daily'").fetchone()
    if not t:
        c.execute("INSERT INTO timers (id, kind, due, payload) VALUES ('daily','edition',?, '{}')",
                  (fmt(next_daily(EDITION_AT, now())),))
        c.commit()
        return
    if t["due"] <= fmt(now()):
        date = t["due"][:10]
        add_event(c, "edition:" + date, "edition", {"date": date})   # dedup: one edition per date
        c.execute("UPDATE timers SET due=? WHERE id='daily'", (fmt(next_daily(EDITION_AT, now())),))
        c.commit()


def outbox(c, kind, payload):
    c.execute("INSERT INTO outbox (kind, payload, created) VALUES (?,?,?)", (kind, json.dumps(payload, ensure_ascii=False), fmt(now())))
    c.commit()


# ---------------------------------------------------------------- claude runs
def claude(prompt, allowed, model, session=None, resume=False, max_turns=60, timeout=1800):
    denied = ["Bash", "Agent", "NotebookEdit", "mcp__claude-in-chrome__*"]
    if "WebFetch" not in allowed:
        denied += ["WebFetch", "WebSearch"]
    cmd = [CLAUDE, "-p", "--model", model, "--max-turns", str(max_turns), "--output-format", "json",
           "--permission-mode", "dontAsk", "--allowedTools", ",".join(allowed), "--disallowedTools", ",".join(denied),
           # a nested session must never load the Telegram plugin (it would steal the bot from the live session)
           "--settings", '{"enabledPlugins":{"telegram@claude-plugins-official":false}}']
    cmd += ["--resume", session] if resume else ["--session-id", session]
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=RUNTIME, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError("claude run failed: " + (p.stderr or p.stdout)[-400:])
    out = json.loads(p.stdout)
    if out.get("is_error"):
        raise RuntimeError("claude run error: " + str(out.get("result"))[-400:])
    return out.get("total_cost_usd") or 0.0


def perm(path, *verbs):
    return ["%s(/%s)" % (v, path) for v in verbs]


def cost_add(date, stage, usd):
    costs = jload(rd(date, "costs.json"), {})
    costs[stage] = round(costs.get(stage, 0) + usd, 4)
    jsave(rd(date, "costs.json"), costs)


# ---------------------------------------------------------------- stages
def last_capture(date):
    days = sorted(d for d in os.listdir(RUNS) if d < date and os.path.exists(os.path.join(RUNS, d, "capture", "results.json")))
    return os.path.join(RUNS, days[-1], "capture") if days else None


def sources_for_today(date):
    """sources.json with the routes the collector has repaired (route-overrides.json) applied."""
    src = jload(os.path.join(RUNTIME, "sources.json"))
    over = jload(os.path.join(STATE, "route-overrides.json"), {})
    for s in src["sources"]:
        if s["id"] in over:
            s["configured_url"], s["url"] = s.get("url"), over[s["id"]]["url"]
    path = rd(date, "sources.json")
    jsave(path, src)
    return path


def st_capture(date):
    args = [sys.executable, "-I", os.path.join(HERE, "capture.py"), rd(date, "capture"), "--sources", sources_for_today(date),
            "--hours", str(WINDOW_HOURS)]
    prev = last_capture(date)
    if prev:
        args += ["--prev", prev]
    p = subprocess.run(args, capture_output=True, text=True, timeout=900)
    if p.returncode not in (0, 2):     # 2 = some sources failed: reported, not fatal
        raise RuntimeError("capture crashed: " + p.stderr[-400:])
    log(date, "capture " + p.stdout.strip())


def st_ledger(date):
    p = subprocess.run([sys.executable, "-I", os.path.join(HERE, "ledger.py"), rd(date),
                        "--interests", os.path.join(MEM, "interests.json"), "--seen", os.path.join(MEM, "seen.json")],
                       capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError("ledger crashed: " + p.stderr[-400:])
    log(date, "ledger " + p.stdout.strip())


def st_collector(date):
    report = rd(date, "collector-report.json")
    prompt = ("Read %s first and follow it. Today's run folder is %s (relative paths in the rules are inside it). "
              "Write the report to %s. Then reply with one line: done." % (os.path.join(MEM, "collector.md"), rd(date), report))
    sid = str(uuid.uuid4())
    usd = claude(prompt, ["Read(/%s/**)" % RUNTIME, "WebFetch", "WebSearch"] + perm(report, "Write", "Edit"),
                 COLLECTOR_MODEL, session=sid, max_turns=40)
    cost_add(date, "collector", usd)
    rep = jload(report)
    if not rep:
        raise RuntimeError("collector wrote no report")
    rep["_session"] = sid
    # try every proposed route ourselves; keep it only if it really parses
    src = {s["id"]: s for s in jload(rd(date, "sources.json"))["sources"]}
    results = jload(rd(date, "capture", "results.json"))
    over = jload(os.path.join(STATE, "route-overrides.json"), {})
    window = results["summary"]["window"]
    start, end = (dt.datetime.fromisoformat(window[k]) for k in ("start", "end"))
    added = 0
    for s in rep.get("sources", []):
        url, sid_ = s.get("proposed_url"), s.get("id")
        if s.get("diagnosis") != "route_broken" or not url or sid_ not in src:
            continue
        trial = dict(src[sid_], url=url)
        r, items = capture.run_source(trial, rd(date, "capture"), start, end, {})
        s["trial"] = r["status"]
        if r["status"] in ("success", "empty"):
            over[sid_] = {"url": url, "since": date, "was": src[sid_].get("url")}
            results["receipts"] = [r if x["id"] == sid_ else x for x in results["receipts"]]
            with open(rd(date, "capture", "items.jsonl"), "a", encoding="utf-8") as f:
                for i in items:
                    f.write(json.dumps(i, ensure_ascii=False) + "\n")
            added += 1
    if added:
        st = {}
        for r in results["receipts"]:
            st[r["status"]] = st.get(r["status"], 0) + 1
        results["summary"]["status"] = st
        jsave(rd(date, "capture", "results.json"), results)
        jsave(os.path.join(STATE, "route-overrides.json"), over)
        st_ledger(date)
    jsave(report, rep)
    log(date, "collector ok, %d route(s) repaired, $%.2f" % (added, usd))


def editor_session(date):
    meta = jload(rd(date, "editor.json"), {})
    if "session" not in meta:
        meta["session"] = str(uuid.uuid4())
        jsave(rd(date, "editor.json"), meta)
    return meta


def editor_perms(date):
    return (["Read(/%s/**)" % RUNTIME] + perm(rd(date, "ledger", "decisions.json"), "Write", "Edit")
            + perm(rd(date, "brief.json"), "Write", "Edit"))


def st_shortlist(date):
    meta = editor_session(date)
    collector = (jload(rd(date, "collector-report.json")) or {}).get("_session")
    if collector and collector == meta["session"]:
        raise RuntimeError("editor and collector must be different sessions")
    past = sorted(d for d in os.listdir(RUNS) if d < date and os.path.exists(os.path.join(RUNS, d, "brief.json")))[-3:]
    prompt = """Read {mem}/instructions.md and {mem}/listener.md first and follow them. You are the editor for {date}.
Today's run folder is {run}. Do PHASE 1 only: decide every required id and write {run}/ledger/decisions.json with the shortlist.
Other inputs: {mem}/seen.json, earlier briefs: {past}.
Reply with one line: done.""".format(mem=MEM, date=date, run=rd(date),
                                     past=", ".join(os.path.join(RUNS, d, "brief.json") for d in past) or "none yet")
    started = meta.get("started")
    usd = claude(prompt, editor_perms(date), EDITOR_MODEL, session=meta["session"], resume=bool(started))
    meta["started"] = True
    jsave(rd(date, "editor.json"), meta)
    cost_add(date, "shortlist", usd)
    d = jload(rd(date, "ledger", "decisions.json"))
    if not d or not d.get("shortlist"):
        raise RuntimeError("editor wrote no shortlist")
    log(date, "shortlist %d candidates, $%.2f" % (len(d["shortlist"]), usd))


class Text(html.parser.HTMLParser):
    SKIP = {"script", "style", "nav", "header", "footer", "svg", "noscript", "form", "button", "aside"}
    BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "pre", "blockquote", "tr", "br", "div", "section", "article", "td", "figcaption"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def text(self):
        t = re.sub(r"[ \t\r\f\v]+", " ", "".join(self.out))
        return re.sub(r"\n\s*\n+", "\n\n", t).strip()


def read_original(url):
    """Fetch one original as plain text. Returns (ok, text, note)."""
    u = urllib.parse.urlsplit(url)
    host = u.netloc.lower().replace("www.", "")
    if host in ("x.com", "twitter.com"):
        return False, "", "x.com needs a login; read the article or repo it points to instead"
    m = re.match(r"/([^/]+)/([^/]+)/?$", u.path)
    if host == "github.com" and m:
        code, data, _ = capture.fetch("https://api.github.com/repos/%s/%s/readme" % m.groups(),
                                      headers={"Accept": "application/vnd.github.raw"})
        return True, data.decode("utf-8", "replace"), "GitHub README"
    if host == "news.ycombinator.com" and "id=" in u.query:
        return read_hn(urllib.parse.parse_qs(u.query)["id"][0])
    code, data, final = capture.fetch(url, limit=8 << 20)
    head = data[:300].lstrip().lower()
    if head.startswith(b"%pdf"):
        return False, "", "PDF (not extracted)"
    p = Text()
    p.feed(data.decode("utf-8", "replace"))
    t = p.text()
    if len(t) < 1200 or re.search(r"(?i)(sign in to continue|enable javascript|log in to read|subscribe to read)", t[:2000]):
        return False, t[:2000], "too little text: a login wall or a JavaScript-only page"
    return True, t, "HTML %s" % final


def read_hn(item_id, max_comments=60):
    code, data, _ = capture.fetch("https://hn.algolia.com/api/v1/items/%s" % item_id)
    root = json.loads(data)
    lines = ["HN: %s (%s points)" % (root.get("title"), root.get("points"))]
    if root.get("text"):
        lines.append(_plain(root["text"]))
    n = 0

    def walk(node, depth):
        nonlocal n
        for ch in node.get("children") or []:
            if n >= max_comments:
                return
            if ch.get("text"):
                lines.append("%s- %s: %s" % ("  " * depth, ch.get("author"), _plain(ch["text"])))
                n += 1
            if depth < 2:
                walk(ch, depth + 1)
    walk(root, 0)
    return True, "\n\n".join(lines), "HN thread via Algolia, %d comments" % n


def _plain(s):
    p = Text()
    p.feed(s)
    return p.text()


def st_originals(date):
    d = jload(rd(date, "ledger", "decisions.json"))
    leads = {l["id"]: l for l in jload(rd(date, "ledger", "leads.json"))}
    os.makedirs(rd(date, "originals"), exist_ok=True)
    got = 0
    for s in d["shortlist"]:
        lid = s["id"]
        url = s.get("url") or leads.get(lid, {}).get("url")
        try:
            ok, text, note = read_original(url)
        except Exception as e:
            ok, text, note = False, "", "%s: %s" % (type(e).__name__, str(e)[:200])
        with open(rd(date, "originals", lid + ".txt"), "w", encoding="utf-8") as f:
            f.write("URL: %s | fetched: %s | %s | %d chars\n\n%s" % (url, "ok" if ok else "FAILED", note, len(text), text[:120000]))
        got += ok
        disc = leads.get(lid, {}).get("discussion")
        if ok and disc and disc != url:
            try:
                _, t, note = read_hn(urllib.parse.parse_qs(urllib.parse.urlsplit(disc).query)["id"][0], 30)
                with open(rd(date, "originals", lid + "-hn.txt"), "w", encoding="utf-8") as f:
                    f.write("URL: %s | fetched: ok | %s\n\n%s" % (disc, note, t))
            except Exception:
                pass
    log(date, "originals %d/%d readable" % (got, len(d["shortlist"])))


def st_write(date, feedback=None):
    meta = editor_session(date)
    if feedback:
        prompt = ("The checker rejected {run}/brief.json. Fix exactly these problems by editing brief.json, change nothing else, "
                  "then reply with one line: done.\n\n{fb}").format(run=rd(date), fb=feedback)
    else:
        prompt = ("Now PHASE 2 for {date}: read the originals in {run}/originals/, select the stories, and write {run}/brief.json "
                  "exactly as the rules say. Reply with one line: done.").format(date=date, run=rd(date))
    usd = claude(prompt, editor_perms(date), EDITOR_MODEL, session=meta["session"], resume=True, max_turns=80)
    cost_add(date, "write", usd)
    if not jload(rd(date, "brief.json")):
        raise RuntimeError("editor wrote no brief.json")
    log(date, "write%s $%.2f" % (" (fix)" if feedback else "", usd))


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2014", "-").replace("\u2013", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def numbers(s):
    out = set()
    for m in re.finditer(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)", s):
        n = m.group(1).replace(",", "").rstrip(".")
        try:
            if float(n) > 10 and not re.fullmatch(r"20[2-3]\d", n):
                out.add(n)
        except ValueError:
            pass
    return out


def gate(date):
    """Structure and provenance checks. They can't prove understanding; they stop invented quotes and numbers."""
    b = jload(rd(date, "brief.json"))
    if not b:
        return ["brief.json is missing or not valid JSON"]
    probs = []
    d = jload(rd(date, "ledger", "decisions.json"), {})
    req = {r["id"] for r in jload(rd(date, "ledger", "required-decisions.json"), [])}
    decided = {x["id"]: x for x in d.get("decisions", [])}
    for x in b.get("decisions", []):
        decided[x["id"]] = x
    for i in sorted(req - set(decided)):
        probs.append("no decision for required id %s" % i)
    for x in decided.values():
        if len((x.get("reason") or "").split()) < 3 or re.fullmatch(r"(?i)\s*not selected\.?\s*", x.get("reason") or ""):
            probs.append("decision %s needs a specific reason" % x["id"])
    shortlist = {s["id"] for s in d.get("shortlist", [])}
    stories = b.get("stories") or []
    if not 3 <= len(stories) <= 7:
        probs.append("%d stories; aim for about 6 (3–7 allowed)" % len(stories))
    texts = {}
    for s in stories:
        sid = s.get("id")
        if sid not in shortlist:
            probs.append("story %s was not on the shortlist" % sid)
            continue
        files = [f for f in os.listdir(rd(date, "originals")) if f.startswith(sid)]
        raw = "".join(open(rd(date, "originals", f), encoding="utf-8").read() for f in files)
        if "fetched: ok" not in raw:
            probs.append("story %s: its original could not be read, so it can't be selected" % sid)
            continue
        texts[sid] = raw
        nraw = norm(raw)
        ev = [e for e in s.get("evidence", []) if len((e.get("quote") or "").split()) >= 8]
        if len(ev) < 2:
            probs.append("story %s: needs at least 2 quotes of 8+ words" % sid)
        for e in ev:
            if norm(e["quote"]) not in nraw:
                probs.append("story %s: quote not found verbatim in the original: \"%s\"" % (sid, e["quote"][:90]))
    script = b.get("script") or ""
    words = len(script.split())
    if not WORDS[0] <= words <= WORDS[1]:
        probs.append("script is %d words; plan for %d–%d (10–12 minutes)" % (words, WORDS[0], WORDS[1]))
    known = set().union(*[numbers(t) for t in texts.values()]) if texts else set()
    known |= numbers(date)
    missing = sorted(numbers(script) - known, key=float)
    if missing:
        probs.append("numbers in the script that appear in no selected original: %s" % ", ".join(missing))
    paras = [p.strip() for p in re.split(r"\n\s*\n", script) if p.strip()]
    chapter_ids = set()
    for c in b.get("chapters") or []:
        chapter_ids.add(c.get("id"))
        if not any(p.startswith((c.get("start_text") or "\0").strip()) for p in paras):
            probs.append("chapter %s: start_text doesn't begin any paragraph" % c.get("id"))
    if len(chapter_ids) < len(texts):
        probs.append("fewer chapters (%d) than stories (%d)" % (len(chapter_ids), len(texts)))
    for n in b.get("notes") or []:
        if not (n.get("en") and n.get("zh") and n.get("terms")):
            probs.append("note for %s needs en, zh and terms" % n.get("chapter_id"))
        if n.get("chapter_id") not in chapter_ids:
            probs.append("note points at unknown chapter %s" % n.get("chapter_id"))
    if re.search(r"https?://", script):
        probs.append("the script contains a URL; keep links in notes")
    return probs


def st_gate(date):
    for attempt in range(2):
        probs = gate(date)
        jsave(rd(date, "gate.json"), {"checked": fmt(now()), "attempt": attempt + 1, "problems": probs})
        if not probs:
            log(date, "gate passed")
            return
        log(date, "gate: %d problem(s)" % len(probs))
        if attempt == 0:
            st_write(date, feedback="\n".join("- " + p for p in probs))
    raise RuntimeError("gate failed after one fix round: " + "; ".join(probs[:5]))


def st_voice(date):
    if not os.path.exists(VENV_PY):
        raise RuntimeError("local TTS isn't set up (run `podcast.py setup-tts`)")
    env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    p = subprocess.run([VENV_PY, "-I", os.path.join(HERE, "tts.py"), rd(date, "brief.json"), rd(date, "audio"),
                        "--voice", os.path.join(MEM, "voice.json")], capture_output=True, text=True, env=env, timeout=3600)
    if p.returncode != 0:
        raise RuntimeError("voice failed: " + (p.stderr or p.stdout)[-500:])
    info = json.loads(p.stdout.strip().splitlines()[-1])
    log(date, "voice %.0f s (%.1f min) in %.0f s" % (info["seconds"], info["seconds"] / 60, info["took"]))


def st_deliver(date, c=None):
    b = jload(rd(date, "brief.json"))
    audio = jload(rd(date, "audio", "episode.json"))
    funnel = jload(rd(date, "ledger", "funnel.json"), {})
    d = jload(rd(date, "ledger", "decisions.json"), {})
    costs = jload(rd(date, "costs.json"), {})
    mins = audio["seconds"] / 60
    flag = "" if 600 <= audio["seconds"] <= 720 else "（时长 %.1f 分钟，不在 10–12 分钟内）" % mins
    caption = "🎧 %s · %s\n%s" % (date, b["title"], b.get("summary_zh", ""))
    chapters = []
    for ch in b.get("chapters", []):
        t = (audio.get("chapters") or {}).get(ch["id"])
        chapters.append("%s %s" % ("%d:%02d" % divmod(int(t), 60) if t is not None else "–", ch["title"]))
    notes = ["📝 笔记 / Notes · %s%s" % (date, flag), ""]
    for n in b.get("notes", []):
        notes += ["▍%s" % n["title"], n["zh"], "", n["en"], "", "词汇: " + "；".join(n.get("terms", []))]
        notes += ["🔗 " + u for u in n.get("source_urls", [])] + [""]
    st = funnel.get("sources", {})
    ledger = ("📊 账本: %d 个来源执行 %d 个 (成功 %d / 空 %d / 失败 %d, 未接入 %d) · 抓回 %d 条 → 去重 %d → 必审 %d → 候选 %d → 入选 %d · 花费 $%.2f"
              % (sum(st.values()), sum(v for k, v in st.items() if k != "not_executed"), st.get("success", 0), st.get("empty", 0),
                 st.get("failed", 0), st.get("not_executed", 0), funnel.get("captured", 0), funnel.get("unique", 0),
                 funnel.get("required_decisions", 0), len(d.get("shortlist", [])), len(b.get("stories", [])), sum(costs.values())))
    msgs = [{"kind": "audio", "path": rd(date, "audio", "episode.m4a"), "title": b["title"], "caption": caption[:1000],
             "duration": int(audio["seconds"])},
            {"kind": "text", "text": "\n".join(["⏱ 章节 Chapters"] + chapters + ["", ledger])}]
    body = "\n".join(notes)
    while body:   # Telegram messages are capped at 4096 characters
        cut = body.rfind("\n\n", 0, 3800) if len(body) > 3800 else len(body)
        cut = cut if cut > 0 else 3800
        msgs.append({"kind": "text", "text": body[:cut]})
        body = body[cut:].lstrip()
    own = c is None
    c = c or db()
    for m in msgs:
        outbox(c, m.pop("kind"), m)
    # memory: what has been used, so tomorrow's editor doesn't repeat it as new
    seen = jload(os.path.join(MEM, "seen.json"), [])
    seen += [{"url": s["url"], "title": s["title"], "date": date} for s in b.get("stories", [])]
    jsave(os.path.join(MEM, "seen.json"), seen[-500:])
    if own:
        dispatch(c)
    log(date, "deliver queued %d message(s)" % len(msgs))


STAGE_FN = {"capture": st_capture, "ledger": st_ledger, "collector": st_collector, "shortlist": st_shortlist,
            "originals": st_originals, "write": st_write, "gate": st_gate, "voice": st_voice, "deliver": st_deliver}


def edition(date, start="capture", stop="deliver", c=None):
    os.makedirs(rd(date), exist_ok=True)
    for name in STAGES[STAGES.index(start):STAGES.index(stop) + 1]:
        log(date, "== " + name)
        if name == "deliver":
            st_deliver(date, c)
        else:
            STAGE_FN[name](date)
        done = jload(rd(date, "stages.json"), {})
        done[name] = fmt(now())
        jsave(rd(date, "stages.json"), done)


def resume_point(date):
    done = jload(rd(date, "stages.json"), {})
    for s in STAGES:
        if s not in done:
            return s
    return None


# ---------------------------------------------------------------- worker + dispatcher
def work(c):
    lock = open(os.path.join(STATE, "worker.lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return
    for e in c.execute("SELECT * FROM inbox WHERE status='pending' ORDER BY created").fetchall():
        date = json.loads(e["payload"]).get("date") or e["created"][:10]
        c.execute("UPDATE inbox SET attempts=attempts+1 WHERE id=?", (e["id"],))
        run = c.execute("INSERT INTO runs (date, started, status) VALUES (?,?, 'running')", (date, fmt(now()))).lastrowid
        c.commit()
        try:
            start = resume_point(date) if os.path.exists(rd(date)) else "capture"
            if start:
                edition(date, start, "deliver", c)
            c.execute("UPDATE inbox SET status='done', done=?, error=NULL WHERE id=?", (fmt(now()), e["id"]))
            c.execute("UPDATE runs SET ended=?, status='ok', cost=?, summary=? WHERE id=?",
                      (fmt(now()), sum(jload(rd(date, "costs.json"), {}).values()), (jload(rd(date, "brief.json")) or {}).get("title"), run))
        except Exception as ex:
            err = str(ex)[:500]
            os.makedirs(rd(date), exist_ok=True)
            log(date, "FAILED: " + err)
            c.execute("UPDATE runs SET ended=?, status='failed', summary=? WHERE id=?", (fmt(now()), err, run))
            c.execute("UPDATE inbox SET error=? WHERE id=?", (err, e["id"]))
            if e["attempts"] + 1 >= MAX_ATTEMPTS:
                c.execute("UPDATE inbox SET status='failed' WHERE id=?", (e["id"],))
                outbox(c, "text", {"text": "⚠️ 今天（%s）的新加坡播报没做出来，停在「%s」：%s\n昨天的那期还在。" % (date, resume_point(date), err[:300])})
        c.commit()


def tg():
    env = dict(l.strip().split("=", 1) for l in open(os.path.join(TG_DIR, ".env")) if "=" in l)
    token = env["TELEGRAM_BOT_TOKEN"].strip().strip('"')
    chat = json.load(open(os.path.join(TG_DIR, "access.json")))["allowFrom"][0]
    return token, chat


def tg_call(method, fields, files=None):
    token, chat = tg()
    fields = dict(fields, chat_id=chat)
    if files:
        boundary = uuid.uuid4().hex
        parts = []
        for k, v in fields.items():
            parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, k, v)).encode())
        for k, (name, data, ctype) in files.items():
            parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n'
                          % (boundary, k, name, ctype)).encode() + data + b"\r\n")
        body = b"".join(parts) + ("--%s--\r\n" % boundary).encode()
        req = urllib.request.Request("https://api.telegram.org/bot%s/%s" % (token, method), data=body,
                                     headers={"Content-Type": "multipart/form-data; boundary=" + boundary})
    else:
        req = urllib.request.Request("https://api.telegram.org/bot%s/%s" % (token, method),
                                     data=urllib.parse.urlencode(fields).encode())
    with urllib.request.urlopen(req, timeout=120) as r:
        if not json.load(r).get("ok"):
            raise RuntimeError("telegram said not ok")


def dispatch(c):
    for m in c.execute("SELECT * FROM outbox WHERE status='pending' ORDER BY id").fetchall():
        p = json.loads(m["payload"])
        try:
            if m["kind"] == "audio":
                with open(p["path"], "rb") as f:
                    data = f.read()
                tg_call("sendAudio", {"title": p["title"], "performer": "Singapore Daily", "caption": p["caption"],
                                      "duration": p["duration"]},
                        {"audio": (os.path.basename(p["path"]), data, "audio/mp4")})
            else:
                tg_call("sendMessage", {"text": p["text"], "disable_web_page_preview": "true"})
            c.execute("UPDATE outbox SET status='sent', sent=? WHERE id=?", (fmt(now()), m["id"]))
        except Exception as e:
            c.execute("UPDATE outbox SET error=? WHERE id=?", (str(e)[:300].replace(TG_DIR, "~"), m["id"]))
            c.commit()
            break   # keep the order: audio before its notes
        c.commit()


def status(c):
    for name, q in [("inbox", "SELECT id, status, attempts, created, substr(error,1,80) FROM inbox ORDER BY created DESC LIMIT 7"),
                    ("timers", "SELECT id, kind, due, status FROM timers"),
                    ("outbox", "SELECT id, kind, status, created, sent, substr(error,1,60) FROM outbox ORDER BY id DESC LIMIT 6"),
                    ("runs", "SELECT id, date, started, ended, status, cost, substr(summary,1,80) FROM runs ORDER BY id DESC LIMIT 7")]:
        print("== " + name)
        for r in c.execute(q):
            print("  " + " | ".join("" if v is None else str(v) for v in r))


# ---------------------------------------------------------------- install
def install():
    for d in (MEM, STATE, RUNS):
        os.makedirs(d, exist_ok=True)
    # code, sources and rules are overwritten; learned state (seen.json, route-overrides.json, runs/) never is
    for f in ("podcast.py", "capture.py", "ledger.py", "tts.py", "sources.json"):
        shutil.copy2(os.path.join(HERE, f), os.path.join(RUNTIME, f))
    for f in os.listdir(os.path.join(HERE, "memory")):   # rules are overwritten; learned files (seen.json) are not in the repo
        shutil.copy2(os.path.join(HERE, "memory", f), os.path.join(MEM, f))
    logf = os.path.join(STATE, "launchd.log")
    path = "%s:/usr/bin:/bin:/usr/sbin:/sbin" % os.path.dirname(CLAUDE)
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
""".format(py=os.path.realpath(sys.executable), label=LABEL, script=os.path.join(RUNTIME, "podcast.py"), path=path, log=logf)
    with open(PLIST, "w") as f:
        f.write(plist)
    subprocess.run(["launchctl", "unload", PLIST], capture_output=True)
    subprocess.run(["launchctl", "load", PLIST], check=True)
    print("installed: %s (ticks every 10 min while the Mac is awake; edition at %s)" % (PLIST, EDITION_AT))


def uninstall():
    subprocess.run(["launchctl", "unload", PLIST], capture_output=True)
    if os.path.exists(PLIST):
        os.remove(PLIST)
    print("removed " + PLIST)


def main():
    args = sys.argv[1:] or ["tick"]
    cmd = args[0]
    if cmd in ("install", "uninstall"):
        return install() if cmd == "install" else uninstall()
    c = db()
    os.makedirs(RUNS, exist_ok=True)
    if cmd == "tick":
        schedule(c)
        work(c)
        dispatch(c)
    elif cmd == "event":
        date = args[2] if len(args) > 2 else now().strftime("%Y-%m-%d")
        print("queued" if add_event(c, "edition:%s:%s" % (date, fmt(now())), "edition", {"date": date}) else "duplicate")
    elif cmd == "run":
        date = next((a for a in args[1:] if re.fullmatch(r"\d{4}-\d\d-\d\d", a)), now().strftime("%Y-%m-%d"))
        opt = dict(zip(args[1::1], args[2::1]))
        edition(date, opt.get("--from", "capture"), opt.get("--to", "deliver"), c)
        dispatch(c)
    elif cmd == "status":
        status(c)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
