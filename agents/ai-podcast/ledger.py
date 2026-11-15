#!/usr/bin/env python3
"""Ledger: turn a capture into what the editor must look at, and keep the funnel honest.

  python3 -I ledger.py <run_dir> [--interests memory/interests.json] [--seen seen.json]

Reads <run_dir>/capture/{results.json,items.jsonl}. Writes <run_dir>/ledger/:
  leads.json              every unique lead with a stable id, heat, interest flags, who carried it
  candidates.md           the same as a compact table for the editor (sorted by heat)
  required-decisions.json leads the editor must decide on (top heat + interest matches + first-party news)
  sources.md              per-source status, so failures are visible, not hidden
  funnel.json             captured → unique → required → (shortlist → selected, filled in later)
Standard library only.
"""
import argparse
import hashlib
import json
import os
import re
import urllib.parse

FIRST_PARTY = ("blog-anthropic", "blog-claude", "blog-openai", "blog-deepmind", "blog-google", "release-")
REQUIRED_MAX = 40


def norm_url(u):
    if not u:
        return ""
    p = urllib.parse.urlsplit(u.strip())
    q = "&".join(x for x in p.query.split("&") if x and not x.startswith(("utm_", "ref=", "s=", "t=")))
    host = p.netloc.lower().replace("www.", "").replace("mobile.twitter.com", "x.com").replace("twitter.com", "x.com")
    return urllib.parse.urlunsplit(("https", host, p.path.rstrip("/"), q, ""))


def lead_id(url):
    return hashlib.sha1(url.encode()).hexdigest()[:8]


def heat(group):
    """Community signal only: HN points/comments, X engagement, and how many sources carried it."""
    h = 0
    for i in group:
        h += i.get("points", 0) + 2 * i.get("comments", 0)
        h += (i.get("likes", 0) + 3 * i.get("retweets", 0) + 2 * i.get("replies", 0)) / 10.0
    h += 40 * (len({i["source_id"] for i in group}) - 1)
    return round(h, 1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--interests", default=os.path.join(here, "memory", "interests.json"))
    ap.add_argument("--seen", help="seen.json: links already used in earlier episodes")
    a = ap.parse_args()
    cap, out = os.path.join(a.run, "capture"), os.path.join(a.run, "ledger")
    os.makedirs(out, exist_ok=True)
    results = json.load(open(os.path.join(cap, "results.json")))
    items = [json.loads(l) for l in open(os.path.join(cap, "items.jsonl"), encoding="utf-8") if l.strip()]
    areas = {k: re.compile(v) for k, v in json.load(open(a.interests))["areas"].items()}
    seen = {}
    if a.seen and os.path.exists(a.seen):
        seen = {norm_url(s["url"]): s for s in json.load(open(a.seen))}

    groups = {}
    for i in items:
        key = norm_url(i.get("url"))
        if key:
            groups.setdefault(key, []).append(i)
    leads = []
    for url, g in groups.items():
        best = max(g, key=lambda i: len(i.get("title") or ""))
        blob = " ".join((i.get("title") or "") + " " + (i.get("summary") or "") for i in g)
        dates = sorted(i["published"] for i in g if i.get("published"))
        lead = {"id": lead_id(url), "url": best.get("url"), "title": best.get("title"),
                "published": dates[0] if dates else None, "sources": sorted({i["source_id"] for i in g}),
                "heat": heat(g), "interests": [k for k, r in areas.items() if r.search(blob)],
                "summary": (best.get("summary") or "")[:300]}
        disc = [i["discussion"] for i in g if i.get("discussion")]
        if disc:
            lead["discussion"] = disc[0]
        if url in seen:
            lead["seen_before"] = seen[url].get("date")
        leads.append(lead)
    leads.sort(key=lambda l: (-l["heat"], l["title"] or ""))

    required, why = [], {}
    def need(l, reason):
        if l["id"] not in why and len(required) < REQUIRED_MAX:
            required.append(l)
            why[l["id"]] = reason
    for l in leads[:15]:
        if l["heat"] > 0:
            need(l, "top heat")
    for l in leads:
        if any(s.startswith(FIRST_PARTY) for s in l["sources"]):
            need(l, "first-party news")
    for l in leads:
        if l["interests"]:
            need(l, "interest: " + ", ".join(l["interests"]))
    req = [{"id": l["id"], "title": l["title"], "url": l["url"], "why_required": why[l["id"]]} for l in required]

    json.dump(leads, open(os.path.join(out, "leads.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(req, open(os.path.join(out, "required-decisions.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(out, "candidates.md"), "w", encoding="utf-8") as f:
        f.write("# Leads (%d unique, sorted by heat)\n\nid | published | heat | sources | interests | title | url\n---|---|---|---|---|---|---\n" % len(leads))
        for l in leads:
            f.write("%s | %s | %s | %s | %s | %s | %s%s\n" % (
                l["id"], (l["published"] or "?")[:16], l["heat"], ",".join(l["sources"]), ",".join(l["interests"]),
                (l["title"] or "").replace("|", "/")[:150], l["url"],
                " (seen %s)" % l["seen_before"] if l.get("seen_before") else ""))
    with open(os.path.join(out, "sources.md"), "w", encoding="utf-8") as f:
        f.write("# Sources %s\n\n" % json.dumps(results["summary"]["status"]))
        for r in results["receipts"]:
            f.write("- %s `%s` %s %s\n" % (r["status"], r["id"], r.get("items_in_window", ""),
                                          r.get("error") or r.get("reason") or ""))
    funnel = {"window": results["summary"]["window"], "sources": results["summary"]["status"],
              "captured": len(items), "unique": len(leads), "required_decisions": len(req)}
    json.dump(funnel, open(os.path.join(out, "funnel.json"), "w"), indent=1)
    print(json.dumps(funnel))


if __name__ == "__main__":
    main()
