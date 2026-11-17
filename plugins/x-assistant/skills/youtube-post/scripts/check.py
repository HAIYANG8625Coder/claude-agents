#!/usr/bin/env python3
"""Check a YouTube post file against YouTube Studio's limits.

Usage: python3 -I check.py <yt-post.md>
  The file has "# Title", "# Description" and "# Tags" sections.
  Checks: title <= 100 characters, description <= 5000, no < or > in either,
  tags <= 500 characters (commas included), and the chapter list
  (first at 00:00, at least 3, increasing, each >= 10 s apart) if there is one.
Exit code 1 if anything fails.
"""
import re
import sys


def section(text, name):
    m = re.search(r"^#\s*" + name + r"\s*\n(.*?)(?=^#\s+[A-Z]|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def secs(stamp):
    n = 0
    for part in stamp.split(":"):
        n = n * 60 + int(part)
    return n


text = open(sys.argv[1], encoding="utf-8").read()
title = section(text, "Title")
desc = section(text, "Description")
tags = section(text, "Tags")
bad = False


def line(label, ok, detail):
    global bad
    bad = bad or not ok
    print("%-12s %-30s %s" % (label, detail, "OK" if ok else "FIX"))


line("title", 0 < len(title) <= 100, "%d / 100" % len(title))
line("description", 0 < len(desc) <= 5000, "%d / 5000" % len(desc))
angles = [c for c in title + desc if c in "<>"]
line("< >", not angles, "%d found" % len(angles))
tag_list = [t.strip() for t in tags.split(",") if t.strip()]
tag_len = len(",".join(tag_list))
line("tags", tag_len <= 500, "%d / 500 (%d tags)" % (tag_len, len(tag_list)))

stamps = re.findall(r"^\s*((?:\d+:)?\d{1,2}:\d{2})\s+\S", desc, re.M)
if stamps:
    times = [secs(s) for s in stamps]
    ok = times[0] == 0 and len(times) >= 3 and all(b - a >= 10 for a, b in zip(times, times[1:]))
    line("chapters", ok, "%d, first %s" % (len(times), stamps[0]))
else:
    print("%-12s %-30s %s" % ("chapters", "none", "-"))

sys.exit(1 if bad else 0)
