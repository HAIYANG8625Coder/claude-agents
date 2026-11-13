#!/usr/bin/env python3
"""Build every step card from one JSON file, instead of copying step.html by hand.

Usage: python3 -I make_steps.py steps.json <out-dir>
Then render each file with x-image/render.sh (or all of them in a loop).

steps.json:
{
  "slug": "tg",                 # files are named xhs-<slug>-step<N>.html
  "kicker": "STEP",             # optional, e.g. "第" / "LESSON"; shown as "STEP 1 / 6"
  "alternate": true,            # optional, terminal style only: even steps use the light theme
  "style": "terminal",          # optional: terminal (default) | notebook | bigtype (see templates/styles.css)
  "steps": [
    {"title": "建机器人，拿 token", "sub": "在 Telegram 里操作", "roomy": false,
     "items": [
       {"do": "搜索 @BotFather，打开对话"},
       {"cmd": "/newbot"},
       {"note": "⚠️ 坑：token 等于机器人的钥匙", "detail": "别发到群里、截图或公开的地方"}
     ]}
  ]
}
Text is inserted as HTML, so you may use <span class="hl">, &nbsp; and <wbr>.
"roomy": true gives a card with little content bigger text (see step.html).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "templates", "step.html")
BRAND = os.path.abspath(os.path.join(HERE, "..", "..", "x-image", "templates", "brand.css"))
STYLES = os.path.abspath(os.path.join(HERE, "..", "templates", "styles.css"))
STYLE = None  # set below from the spec

spec = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
tpl = open(TEMPLATE, encoding="utf-8").read()
# Relative links from the output folder, so the cards render there and no home-folder path lands in git.
tpl = re.sub(r'href="[^"]*brand\.css"', lambda m: 'href="%s"' % os.path.relpath(BRAND, out), tpl)
tpl = re.sub(r'href="[^"]*styles\.css"', lambda m: 'href="%s"' % os.path.relpath(STYLES, out), tpl)
STYLE = spec.get("style", "terminal")
if STYLE not in ("terminal", "notebook", "bigtype"):
    raise SystemExit("unknown style: %r" % STYLE)
steps = spec["steps"]
n = len(steps)


def item(it):
    if "do" in it:
        return '<div class="do">%s</div>' % it["do"]
    if "cmd" in it:
        return '<div class="cmd">%s</div>' % it["cmd"]
    if "note" in it:
        return '<div class="pit"><div class="t">%s</div><div class="d">%s</div></div>' % (
            it["note"], it.get("detail", ""))
    raise SystemExit("unknown item: %r" % it)


for i, st in enumerate(steps, 1):
    prog = "".join('<i class="%s"></i>' % ("on" if k <= i else "") for k in range(1, n + 1))
    top = '<div class="top"><div class="kicker">%s %d / %d</div><div class="prog">%s</div></div>' % (
        spec.get("kicker", "STEP"), i, n, prog)
    head = "<h2>%s</h2>" % st["title"] + ('<div class="sub">%s</div>' % st["sub"] if st.get("sub") else "")
    body = '<div class="body">%s</div>' % "".join(item(it) for it in st["items"])
    html = re.sub(r'<div class="top">.*?(?=<div class="foot">)', lambda m: top + "\n" + head + "\n" + body + "\n",
                  tpl, flags=re.S)
    classes = []
    if STYLE == "terminal" and spec.get("alternate") and i % 2 == 0:
        classes.append("light")
    elif STYLE == "notebook":
        classes.append("s-notebook")
    elif STYLE == "bigtype":
        # cover = bt-0, overview = bt-1, so step i gets the next colour along
        classes += ["s-bigtype", "bt-%d" % ((i + 1) % 6)]
    if st.get("roomy"):
        classes.append("roomy")
    if classes:
        html = re.sub(r"<body>(?=<div)", lambda m: "<body class=\"%s\">" % " ".join(classes), html, count=1)
    path = os.path.join(out, "xhs-%s-step%d.html" % (spec["slug"], i))
    open(path, "w", encoding="utf-8").write(html)
    print(path)
