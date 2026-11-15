#!/usr/bin/env python3
"""Capture: one 48-hour discovery pass over sources.json (titles, links, dates, receipts).

Discovery only. Nothing here reads an article; the editor reads originals later.
Every source ends as success, empty, failed or not_executed, with a receipt in results.json.

  python3 -I capture.py <out_dir> [--sources sources.json] [--prev <last capture dir>] [--hours 48]

Writes <out_dir>/results.json (one receipt per source), items.jsonl (one lead per line) and raw/.
Standard library only (macOS system Python 3.9 works).
Access rules (from the original project): an honest user agent, one request per source per day, no logins,
and a 403 / 429 / login page is reported as failed, never retried or worked around.
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import email.utils
import gzip
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "sg-podcast-capture/0.1 (personal feed reader; one request per source per day)"
UTC = dt.timezone.utc
MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
DATE_TXT = re.compile(r"\b((?:%s)[a-z]*\.? \d{1,2},? 20\d\d|\d{1,2} (?:%s)[a-z]* 20\d\d)\b" % (MONTHS, MONTHS))
DATE_ISO = re.compile(r"\b(20\d\d-\d\d-\d\d)(?:T\d\d:\d\d(?::\d\d)?(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d)?)?\b")


class Redirect308(urllib.request.HTTPRedirectHandler):
    """Python 3.9's urllib doesn't follow 308 Permanent Redirect (claude.com uses it)."""
    def http_error_308(self, req, fp, code, msg, headers):
        return self.http_error_302(req, fp, 302, msg, headers)

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return urllib.request.Request(newurl, headers=dict(req.header_items()))


OPENER = urllib.request.build_opener(Redirect308)


def fetch(url, limit=32 << 20, headers=None):
    h = {"User-Agent": UA, "Accept-Encoding": "gzip", "Accept": "*/*"}
    h.update(headers or {})
    with OPENER.open(urllib.request.Request(url, headers=h), timeout=40) as r:
        data = r.read(limit + 1)
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return r.status, data[:limit], r.geturl()


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(s)
        return d if d.tzinfo else d.replace(tzinfo=UTC)
    except Exception:
        pass
    m = DATE_ISO.search(s)
    if m:
        try:
            d = dt.datetime.fromisoformat(m.group(0).replace("Z", "+00:00"))
            return d if d.tzinfo else d.replace(tzinfo=UTC)
        except ValueError:
            return dt.datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=UTC)
    m = DATE_TXT.search(s)
    if m:
        t = re.sub(r"[.,]", "", m.group(1))
        for f in ("%b %d %Y", "%B %d %Y", "%d %b %Y", "%d %B %Y"):
            try:
                return dt.datetime.strptime(t, f).replace(tzinfo=UTC)
            except ValueError:
                pass
    return None


def text(el):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", el or ""))).strip()


def local(tag):
    return tag.rsplit("}", 1)[-1]


# ---- one parser per kind; each returns (items, extra receipt fields)
def parse_feed(src, data, **_):
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        # some WordPress feeds (Mothership) carry a bare "&" or a control character; repair just those and retry
        fixed = re.sub(rb"&(?!(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);)", b"&amp;", data)
        root = ET.fromstring(re.sub(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b"", fixed))
    items, audio = [], 0
    title = ""
    for el in root.iter():
        name = local(el.tag)
        if name == "title" and not title:
            title = (el.text or "").strip()
        if name not in ("item", "entry"):
            continue
        f = {local(c.tag): c for c in el}
        link = ""
        if "link" in f:
            link = (f["link"].text or "").strip() or f["link"].get("href", "")
            for c in el:
                if local(c.tag) == "link" and c.get("rel", "alternate") == "alternate" and c.get("href"):
                    link = c.get("href")
        has_audio = any(local(c.tag) == "enclosure" and "audio" in (c.get("type") or "") for c in el)
        audio += has_audio
        date = None
        for k in ("pubDate", "published", "updated", "date"):
            if k in f:
                date = parse_date(f[k].text)
                if date:
                    break
        summary = ""
        for k in ("description", "summary", "content", "encoded"):
            if k in f and f[k].text:
                summary = text(f[k].text)[:400]
                break
        items.append({"title": text(f["title"].text if "title" in f else ""), "url": link,
                      "published": date.isoformat() if date else None, "summary": summary,
                      "audio": has_audio})
    extra = {"feed_title": title}
    if src.get("require_audio") and not audio:
        raise ValueError("feed has no audio enclosures (wrong show or route?)")
    return items, extra


def parse_hn(src, data, **_):
    items = []
    for h in json.loads(data)["hits"]:
        items.append({"title": h.get("title") or "", "url": h.get("url") or "https://news.ycombinator.com/item?id=%s" % h["objectID"],
                      "discussion": "https://news.ycombinator.com/item?id=%s" % h["objectID"],
                      "published": dt.datetime.fromtimestamp(h["created_at_i"], UTC).isoformat(),
                      "points": h.get("points") or 0, "comments": h.get("num_comments") or 0})
    return items, {}


def parse_releases(src, data, **_):
    return [{"title": "%s %s" % (src["name"].split(" releases")[0], r.get("name") or r.get("tag_name")),
             "url": r["html_url"], "published": r.get("published_at"), "summary": text(r.get("body") or "")[:400]}
            for r in json.loads(data)], {}


def parse_follow_builders(src, data, **_):
    d, items = json.loads(data), []
    for b in d.get("x") or []:
        for t in b.get("tweets") or []:
            items.append({"title": "@%s: %s" % (b.get("handle"), text(t.get("text"))[:200]), "url": t.get("url"),
                          "published": t.get("createdAt"), "likes": t.get("likes") or 0,
                          "retweets": t.get("retweets") or 0, "replies": t.get("replies") or 0, "via_handle": b.get("handle")})
    for p in (d.get("blogs") or []) + (d.get("podcasts") or []):
        items.append({"title": text(p.get("title")), "url": p.get("url"), "published": p.get("publishedAt"),
                      "summary": text(p.get("description") or p.get("transcript") or "")[:400], "via": p.get("name")})
    return items, {"feed_generated": d.get("generatedAt")}


def card_date(page, a, b):
    """The date printed on the same card as a link: inside its <article> or <li> if that is small,
    else the nearest date within 500 characters on either side."""
    for tag in ("article", "li"):
        s, e = page.rfind("<" + tag, 0, a), page.find("</%s>" % tag, b)
        if s != -1 and e != -1 and e - s < 6000 and page.find("</%s>" % tag, s, a) == -1:
            d = parse_date(text(page[s:e]))
            if d:
                return d
    best = None
    for m in list(DATE_TXT.finditer(page, max(0, a - 500), a)) + list(DATE_TXT.finditer(page, b, b + 500)):
        dist = a - m.end() if m.end() <= a else m.start() - b
        if best is None or dist < best[0]:
            best = (dist, m.group(1))
    return parse_date(best[1]) if best else None


def parse_listing(src, data, prev_urls=(), **_):
    page = data.decode("utf-8", "replace")
    base = src["url"]
    host = urllib.parse.urlsplit(base).netloc.replace("www.", "")
    items, seen = [], set()
    for m in re.finditer(r'<a\b[^>]*href="([^"#]+)"[^>]*>(.*?)</a>', page, re.S):
        url = urllib.parse.urljoin(base, html.unescape(m.group(1))).split("?")[0]
        title = text(m.group(2))
        u = urllib.parse.urlsplit(url)
        if url in seen or len(title) < 15 or u.netloc.replace("www.", "") != host:
            continue
        if u.path.rstrip("/").count("/") < 2 or url.rstrip("/") == base.rstrip("/"):
            continue  # skip nav links: an article lives at least two levels deep (/news/<slug>)
        seen.add(url)
        date = parse_date(title) or card_date(page, m.start(), m.end())
        how = "listing-text" if date else ("new-since-last-run" if prev_urls and url not in prev_urls else "unknown")
        items.append({"title": DATE_TXT.sub("", title).strip(" ·|-")[:200], "url": url,
                      "published": date.isoformat() if date else None, "date_source": how})
    if not items:
        raise ValueError("no article links found (layout changed or page needs a browser)")
    return items, {}


PARSERS = {"feed": parse_feed, "hn": parse_hn, "github_releases": parse_releases,
           "follow_builders": parse_follow_builders, "html_listing": parse_listing}


def run_source(src, out, start, end, prev_urls):
    r = {"id": src["id"], "name": src["name"], "kind": src["kind"], "url": src.get("url")}
    if not src.get("daily", True) or src["kind"] not in PARSERS:
        r.update(status="not_executed", reason=src.get("note", "no daily route"))
        return r, []
    url = src.get("url")
    if src["kind"] == "hn":
        url = "https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode(
            {"tags": "story", "hitsPerPage": 50, "query": src["query"],
             "numericFilters": "created_at_i>%d" % int(start.timestamp())})
        r["url"] = url
    try:
        code, data, final = fetch(url)
        ext = "json" if src["kind"] in ("hn", "github_releases", "follow_builders") else "html" if src["kind"] == "html_listing" else "xml"
        raw = os.path.join(out, "raw", "%s.%s" % (src["id"], ext))
        with open(raw, "wb") as f:
            f.write(data)
        r.update(http=code, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), raw=os.path.relpath(raw, out))
        if final != url:
            r["final_url"] = final
        items, extra = PARSERS[src["kind"]](src, data, prev_urls=prev_urls.get(src["id"], set()))
        r.update(extra)
    except Exception as e:
        r.update(status="failed", error=("%s: %s" % (type(e).__name__, e))[:300])
        return r, []
    kept = []
    for it in items:
        d = parse_date(it.get("published")) if it.get("published") else None
        if d and not (start <= d <= end + dt.timedelta(hours=1)):
            continue
        if not d and it.get("date_source") == "unknown":
            continue  # undated and not new since the last run (or no last run): can't place it in the window
        it.update(source_id=src["id"], source_name=src["name"])
        kept.append(it)
    r.update(status="success" if kept else "empty", items_total=len(items), items_in_window=len(kept),
             undated=sum(1 for i in kept if not i.get("published")))
    return r, kept


def load_prev(prev):
    urls = {}
    if prev and os.path.exists(os.path.join(prev, "listing-urls.json")):
        urls = {k: set(v) for k, v in json.load(open(os.path.join(prev, "listing-urls.json"))).items()}
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--sources", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources.json"))
    ap.add_argument("--prev", help="last capture dir, to date blog listings by diff")
    ap.add_argument("--hours", type=int, default=48)
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "raw"), exist_ok=True)
    sources = json.load(open(a.sources))["sources"]
    end = dt.datetime.now(UTC).replace(microsecond=0)
    start = end - dt.timedelta(hours=a.hours)
    prev = load_prev(a.prev)
    with cf.ThreadPoolExecutor(8) as ex:
        done = list(ex.map(lambda s: run_source(s, a.out, start, end, prev), sources))
    receipts = [r for r, _ in done]
    items = [i for _, its in done for i in its]
    # remember every listing URL (in window or not) so tomorrow's run can tell new from old
    listing = {}
    for s in sources:
        if s["kind"] == "html_listing":
            raw = os.path.join(a.out, "raw", s["id"] + ".html")
            if os.path.exists(raw):
                try:
                    its, _ = parse_listing(s, open(raw, "rb").read())
                    listing[s["id"]] = sorted({i["url"] for i in its} | prev.get(s["id"], set()))
                except ValueError:
                    pass
    json.dump(listing, open(os.path.join(a.out, "listing-urls.json"), "w"), indent=0)
    with open(os.path.join(a.out, "items.jsonl"), "w", encoding="utf-8") as f:
        for i in items:
            f.write(json.dumps(i, ensure_ascii=False) + "\n")
    count = {}
    for r in receipts:
        count[r["status"]] = count.get(r["status"], 0) + 1
    summary = {"window": {"start": start.isoformat(), "end": end.isoformat(), "hours": a.hours},
               "sources": len(receipts), "status": count, "items": len(items), "first_run": not prev}
    json.dump({"summary": summary, "receipts": receipts}, open(os.path.join(a.out, "results.json"), "w"),
              indent=1, ensure_ascii=False)
    print(json.dumps(summary))
    executed = [r for r in receipts if r["status"] != "not_executed"]
    sys.exit(2 if any(r["status"] == "failed" for r in executed) else 0)


if __name__ == "__main__":
    main()
