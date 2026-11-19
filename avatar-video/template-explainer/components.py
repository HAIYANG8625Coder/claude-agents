"""Shared slide components for article-explainer episodes (extracted from series ep 6 v2, 2026-11-19).

Use it from an episode's build.py instead of copying helper functions:

    import sys, os; sys.path.insert(0, os.path.join(D, "../../template-explainer"))
    from components import Deck, CSS
    deck = Deck()
    deck.scene(1, "01 问题", deck.cards(0, [("a", "❓", "它们是什么", "子标题", "它们是什么")], tight=True), "解释：本片整理 · 示意")
    ...
    STAGE = deck.stage(); BEATS = deck.beats()      # then fill the template as ep 6 v2's build.py does

SAFE AREA (stage = the 1920x1080 frame, slide content goes inside it; learned the hard way on ep 6):
  - slide content: top 90 .. about 680 px in scene coordinates (a 1400-wide diagram at top 90 ends at ~700);
  - the .src source line sits at about 830 px and the caption band starts at about 870 px, so nothing of yours goes below ~740;
  - a chip UNDER a diagram: make the diagram 1100 wide (left 410) and put the chip at top 595, font 34 (CHIP below does it);
  - code windows side by side: left 80 and left 980, width 860, font 28 / line 44 (.cmp).
"""
import html as H, re

CSS = """
      .hid { opacity:0; }
      .dg { position:absolute; background:#fff; border:2px solid var(--line); border-radius:10px; box-shadow:0 14px 36px rgba(60,30,10,.10); overflow:hidden; }
      .dg img { position:absolute; left:0; top:0; width:100%; display:block; }
      .cmp .cl { font-size:28px; line-height:44px; }
      .cmp .cl .t { white-space:pre; }
      .chipr { display:inline-block; font-size:40px; font-weight:900; padding:14px 34px; border:3px solid var(--ink); background:#fff; white-space:nowrap; border-radius:50px; }
      .chipr.red { border-color:var(--red); color:var(--red); }
      .cwin { position:absolute; left:80px; top:96px; width:980px; background:#fffdf9; border:2px solid var(--line); border-radius:10px; box-shadow:0 14px 36px rgba(60,30,10,.10); overflow:hidden; }
      .cwin .wbar { height:48px; background:#efe3d6; display:flex; align-items:center; gap:10px; padding:0 20px; font-family:var(--mono); font-size:24px; color:var(--ink-2); }
      .cwin .wbar i { width:14px; height:14px; border-radius:50%; display:block; }
      .cwin .body { padding:14px 0; }
      .cl { display:flex; font-family:var(--mono); font-size:28px; line-height:37px; border-left:8px solid transparent; }
      .cl b { width:66px; text-align:right; padding-right:22px; color:#b3a495; font-weight:400; flex:none; }
      .cl .t { white-space:pre; }
      .cl.on { background:rgba(155,27,63,.12); border-left-color:var(--red); }
      .ck { color:#7a3fbf; } .cs { color:#1f7a4d; } .cn { color:#b4690e; }
      .cwin.m .cl { font-size:24px; line-height:36px; }
      .term .cl b { display:none; }
      .term .body { padding:18px 26px; }
      .term .t { white-space:pre-wrap; word-break:break-all; }
      .term .pr { color:var(--mint); font-weight:900; }
      .rc { position:absolute; left:1110px; width:730px; }
      .rcard { padding:22px 30px; margin-bottom:18px; font-size:38px; font-weight:900; line-height:1.35; }
      .rcard code { font-family:var(--mono); color:var(--red); font-size:34px; }
      .mc { padding:18px 26px; margin-bottom:16px; border-left:12px solid var(--blue); background:#fff; border-radius:8px; border:1.5px solid var(--line); border-left-width:12px; }
      .mc.asst { border-left-color:#d9822b; } .mc.tool { border-left-color:var(--mint); }
      .mc .role { font-family:var(--mono); font-size:26px; font-weight:700; color:var(--ink-2); }
      .mc .txt { font-family:var(--mono); font-size:30px; line-height:1.4; white-space:pre-wrap; word-break:break-all; }
"""
SAFE = {"content_top": 90, "content_bottom": 680, "never_below": 740, "chip_top_under_diagram": 595, "diagram_w_with_chip": 1100, "diagram_left_with_chip": 410}


class Deck:
    def __init__(self):
        self.SC, self.BE = [], []

    # ---- basics
    def scene(self, ch, sec, inner, src):
        i = len(self.SC)
        self.SC.append('        <div class="scene" id="sc%d" data-ch="%d">\n%s%s\n          <div class="src">%s</div>\n        </div>' % (
            i, ch, ('          <div class="sec">%s</div>\n' % sec) if sec else "", inner, src))
        return i

    def beat(self, i, k, phrase, extra=""):
        self.BE.append('pop("#s%d%s", at("%s")%s);' % (i, k, phrase, extra))

    def raw_beat(self, js):
        self.BE.append(js)

    @staticmethod
    def hid(i, k, cls, inner, style="", tag="div"):
        return '<%s class="hid %s" id="s%d%s"%s>%s</%s>' % (tag, cls, i, k, (' style="%s"' % style) if style else "", inner, tag)

    @staticmethod
    def c3(e, t, small=None, color=None):
        return '<span class="e">%s</span><div%s>%s%s</div>' % (e, (' style="color:%s"' % color) if color else "", t, ("<small>%s</small>" % small) if small else "")

    def next_id(self):
        return len(self.SC)

    # ---- card rows: items = (key, emoji, title, small or None, phrase that makes it pop)
    def cards(self, i, items, top=70, tight=False, reds=()):
        out = '<div class="row3%s" style="top:%dpx">' % (" tight" if tight else "", top)
        for k, (key, e, t, sm, ph) in enumerate(items):
            out += self.hid(i, key, "card", self.c3(e, t, sm), "border:3px solid var(--red)" if k in reds else "")
            self.beat(i, key, ph)
        return out + "</div>"

    # ---- a chip under a diagram (see SAFE)
    def chip(self, i, key, text, phrase, left=410, top=595, red=False, fs=34):
        self.beat(i, key, phrase)
        return self.hid(i, key, "chipr" + (" red" if red else ""), text,
                        "position:absolute;left:%dpx;top:%dpx;font-size:%dpx;padding:10px 30px" % (left, top, fs))

    # ---- staged SVG diagram: stages = [1, 2, ...] files assets/diagrams/<name>-s<k>.svg; phrases = what makes each stage fade in
    def diagram(self, i, name, stages, phrases, left=250, top=90, width=1400, view_h=520):
        scale = width / 1200.0
        out = '<div class="dg hid" id="s%dD" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (i, left, top, width, int(view_h * scale))
        for k in stages:
            out += '<img class="hid" id="s%dG%d" src="assets/diagrams/%s-s%d.svg"/>' % (i, k, name, k)
        out += "</div>"
        self.BE.append('pop("#s%dD", at("%s"));' % (i, phrases[0]))
        for k, ph in zip(stages, phrases):
            self.BE.append('fadeIn("#s%dG%d", at("%s"));' % (i, k, ph))
        return out

    # ---- before / after code windows side by side. lon/ron = line numbers to highlight
    def codecmp(self, i, ltitle, llines, rtitle, rlines, lphrase, rphrase, lon=(), ron=()):
        def win(tag, left, title, lines, on, color):
            rows = "".join('<div class="cl%s"><span class="t">%s</span></div>' % (" on" if k in on else "", H.escape(l)) for k, l in enumerate(lines))
            return ('<div class="cwin card term cmp hid" id="s%d%s" style="top:150px;left:%dpx;width:860px"><div class="wbar" style="color:%s">'
                    '<i style="background:#e0646f"></i><i style="background:#e8b64c"></i><i style="background:#5fbf9f"></i>%s</div><div class="body">%s</div></div>') % (i, tag, left, color, title, rows)
        self.beat(i, "W1", lphrase); self.beat(i, "W2", rphrase)
        return win("W1", 80, ltitle, llines, lon, "#b3261e") + win("W2", 980, rtitle, rlines, ron, "#1f7a4d")

    # ---- recap rows: rows = (key, label, text)
    def recap(self, i, rows, top=140):
        return '<div class="recap" style="top:%dpx">' % top + "".join(
            '<div class="rr hid" id="s%d%s"><div class="h"><b>%s</b></div><div class="d">%s</div></div>' % (i, k, n, d) for k, n, d in rows) + "</div>"

    # ---- real code from a file (added from ep 7, 2026-11-19). code = list of the file's lines; picks = line numbers or None for a "..." row;
    #      marks = (substring of the line, phrase that lights it). Comments after two spaces + "#" are cut.
    @staticmethod
    def hi(line):
        e = H.escape(line)
        e = re.sub(r'(&quot;.*?&quot;|&#x27;.*?&#x27;)', lambda m: '<span class="cs">%s</span>' % m.group(1), e)
        e = re.sub(r'\b(def|return|for|in|if|try|except|import|not|as)\b(?![^<]*</span>)', r'<span class="ck">\1</span>', e)
        e = re.sub(r'\b(\d+)\b(?![^<]*</span>)', r'<span class="cn">\1</span>', e)
        return e

    @staticmethod
    def lineno(code, sub):
        """1-based number of the first line containing sub (fails loudly if the code changed)"""
        return next(k + 1 for k, l in enumerate(code) if sub in l)

    def codeex(self, i, code, picks, marks, top=96, title="agent.py"):
        rows = ""
        for ln in picks:
            if ln is None:
                rows += '<div class="cl"><b></b><span class="t">    ...</span></div>'
            else:
                rows += '<div class="cl" id="s%dL%d"><b>%d</b><span class="t">%s</span></div>' % (i, ln, ln, self.hi(re.split(r"\s{2,}#", code[ln - 1])[0]))
        for sub, phrase in marks:
            ln = next(p for p in picks if p and sub in code[p - 1])
            self.BE.append('lit("#s%dL%d", at("%s"));' % (i, ln, phrase))
        return ('<div class="cwin m card" style="top:%dpx"><div class="wbar"><i style="background:#e0646f"></i><i style="background:#e8b64c"></i>'
                '<i style="background:#5fbf9f"></i>%s</div><div class="body">%s</div></div>') % (top, title, rows)

    # ---- side cards next to a code window: items = [(cls, html)], pop them with raw_beat
    @staticmethod
    def rcards(i, items, top=110):
        out = '<div class="rc" style="top:%dpx">' % top
        for k, (cls, txt) in enumerate(items):
            out += '<div class="rcard card hid" id="s%dR%d">%s</div>' % (i, k, txt)
        return out + "</div>"

    # ---- a chat message card (kind = "", "asst" or "tool")
    @staticmethod
    def msgcard(i, k, role, kind, text, style=""):
        return '<div class="mc %s hid" id="s%d%s"%s><div class="role">%s</div><div class="txt">%s</div></div>' % (kind, i, k, (' style="%s"' % style) if style else "", role, H.escape(text))

    # ---- a long staged chart that grows row by row (one SVG per stage: <name>-s<k>.svg); base = stage already on screen at scene start
    def seqscene(self, i, name, base, rows_phr, top=90, left=330, width=1260, view_h=570):
        out = '<div class="dg hid" id="s%dD" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (i, left, top, width, int(view_h * width / 1200.0))
        for k in ([base] if base else []) + [k for k, _ in rows_phr]:
            out += '<img class="hid" id="s%dG%d" src="assets/diagrams/%s-s%d.svg"/>' % (i, k, name, k)
        out += "</div>"
        first = rows_phr[0][1]
        self.BE.append('pop("#s%dD", at("%s"));' % (i, first))
        if base: self.BE.append('fadeIn("#s%dG%d", at("%s"));' % (i, base, first))
        for k, ph in rows_phr: self.BE.append('fadeIn("#s%dG%d", at("%s"));' % (i, k, ph))
        return out

    def stage(self):
        return "\n".join(self.SC)

    def beats(self):
        return "\n      ".join(self.BE)
