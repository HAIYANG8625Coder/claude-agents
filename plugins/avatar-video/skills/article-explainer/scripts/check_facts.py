#!/usr/bin/env python3
"""List every number in an episode's texts that is NOT in its facts.json.

Usage: python3 -I check_facts.py <video folder> <text file> [<text file> ...]
  <video folder>/facts.json   {"facts": [{"v": "59", "what": "fixed, plain setup, of 60", "src": "ep06/demo/work-plain-*.json"}, ...]}
  text files: script.json (the spoken script), post texts (xhs-*-post.md, yt-*-post.md), index.html captions, ...

Numbers are read as digits ("59", "12.5") and as Chinese numerals ("五十九", "十二"). Every one must be a fact's "v"
(digits) or listed in "also": ["第", ...] is not needed: plain ordinals like 第6集 are skipped (a number right after 第).
It is a review aid, not a proof: a number that is in facts.json can still be used for the wrong thing, so read each line.
Exit code 1 when a text has a number that facts.json doesn't list.
"""
import json, os, re, sys

DIG = {"零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
CN = re.compile(r"[零〇一二两三四五六七八九十百]+")

def cn_to_int(s):
    if "百" in s:
        a, b = s.split("百", 1)
        return (DIG.get(a, 1) if a else 1) * 100 + (cn_to_int(b) if b else 0)
    if "十" in s:
        a, b = s.split("十", 1)
        return (DIG[a] if a else 1) * 10 + (DIG[b] if b else 0)
    n = 0
    for ch in s:
        n = n * 10 + DIG[ch]
    return n

def text_of(path):
    raw = open(path, encoding="utf-8").read()
    if path.endswith(".json"):
        try:
            data = json.loads(raw)
            return "\n".join(x.get("say", "") if isinstance(x, dict) else str(x) for x in data)
        except Exception:
            pass
    return raw

def numbers(text):
    out = []
    text = re.sub(r"\d+:\d\d", " ", text)            # chapter times 02:25
    for m in re.finditer(r"(?<![A-Za-z_\-])\d+(?:\.\d+)?", text):
        before = text[max(0, m.start() - 1):m.start()]
        if before == "第":                            # 第6集, 第12步: ordinals are not facts
            continue
        out.append((m.group(0), text[max(0, m.start() - 12):m.end() + 12].replace("\n", " ")))
    for m in CN.finditer(text):
        s = m.group(0)
        if s in ("一", "二", "三", "四", "十") and len(s) == 1:
            ctx = text[max(0, m.start() - 1):m.end() + 1]
            if re.search(r"[一二三四五六七八九十]个?[，,：:、]", ctx) and m.end() < len(text) and text[m.end()] in "，,：:、":
                continue                               # list markers: 一，计划模式 / 二，清单
        if m.start() > 0 and text[m.start() - 1] == "第":
            continue
        if s in ("零", "〇"):                         # 从零做 / 零基础: a word, not a number
            continue
        try:
            out.append((str(cn_to_int(s)), text[max(0, m.start() - 12):m.end() + 12].replace("\n", " ")))
        except Exception:
            pass
    return out

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    folder, files = sys.argv[1], sys.argv[2:]
    facts = json.load(open(os.path.join(folder, "facts.json"), encoding="utf-8"))["facts"]
    ok = {str(f["v"]) for f in facts}
    bad = 0
    for p in files:
        seen = {}
        for n, ctx in numbers(text_of(p)):
            if n not in ok:
                seen.setdefault(n, ctx)
        print("%s: %s" % (os.path.basename(p), "all numbers are in facts.json" if not seen else "%d number(s) NOT in facts.json" % len(seen)))
        for n, ctx in seen.items():
            print("   %s   ...%s..." % (n, ctx)); bad += 1
    sys.exit(1 if bad else 0)

main()
