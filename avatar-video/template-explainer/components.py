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
import html as H

CSS = """
      .hid { opacity:0; }
      .dg { position:absolute; background:#fff; border:2px solid var(--line); border-radius:10px; box-shadow:0 14px 36px rgba(60,30,10,.10); overflow:hidden; }
      .dg img { position:absolute; left:0; top:0; width:100%; display:block; }
      .cmp .cl { font-size:28px; line-height:44px; }
      .cmp .cl .t { white-space:pre; }
      .chipr { display:inline-block; font-size:40px; font-weight:900; padding:14px 34px; border:3px solid var(--ink); background:#fff; white-space:nowrap; border-radius:50px; }
      .chipr.red { border-color:var(--red); color:var(--red); }
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
    def chip(self, i, key, text, phrase, left=410, top=595, red=False):
        self.beat(i, key, phrase)
        return self.hid(i, key, "chipr" + (" red" if red else ""), text,
                        "position:absolute;left:%dpx;top:%dpx;font-size:34px;padding:10px 30px" % (left, top))

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

    def stage(self):
        return "\n".join(self.SC)

    def beats(self):
        return "\n      ".join(self.BE)
