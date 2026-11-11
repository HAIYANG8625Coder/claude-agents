#!/usr/bin/env python3
"""Count a Xiaohongshu note the way the editor does.

Usage: python3 -I count.py <post.md> [#topic ...]
  post.md has "# 标题" and "# 正文" sections. Topics already written in the
  body are counted once; pass any others as extra arguments. Prints the title length, body length and body+topics total,
  counting emoji and other non-BMP characters as 2 (the editor counts UTF-16).
"""
import re
import sys


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def section(text, name):
    m = re.search(r"^#\s*" + name + r"\s*\n(.*?)(?=^#\s|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


text = open(sys.argv[1], encoding="utf-8").read()
title = section(text, "标题")
body = section(text, "正文")
extra = [t for t in " ".join(sys.argv[2:]).split() if t not in body]  # skip topics already in the body
topics = " ".join(extra)
total = u16(body) + (u16(topics) + 1 if topics else 0)

ok = lambda good: "OK" if good else "TOO LONG"
print("title  %3d / 20    %s" % (u16(title), ok(u16(title) <= 20)))
print("body   %4d" % u16(body))
print("body+topics %4d / 1000  %s" % (total, ok(total <= 1000)))
