"""svgkit: tiny helpers that draw in the chart-draw house style.

You still place everything yourself (x, y, w, h); the kit only makes every box, arrow,
label and table look the same, so a new diagram type takes minutes, not an hour.

    import sys; sys.path.insert(0, "<skill>/scripts")
    from svgkit import Diagram
    d = Diagram(1200, 600)
    d.panel(40, 40, 400, 300, "What starts a run")
    d.box(80, 100, 200, 90, "Timers", "21:15 digest", kind="accent")
    d.arrow([(180, 192), (180, 260)], label="Fires when due")
    d.save("docs/overview.svg")

Box kinds: plain (thin grey border, orange title), main (thick black border, black title),
accent (orange fill + halo: the 1-2 things the diagram is about), faded (dropped / not used),
dashed (optional / later), dark (filled ink, white text: a person or an outside system).
Arrow colors: ink (black, 2 px), accent (orange, 2.5 px; the main path), grey (quiet).
Every text argument can hold "\\n" for a second line.
Themes: draw in the light palette (the default); save() also writes <name>-dark.svg
through theme.py, so the dark version never drifts from the light one.
"""
from xml.sax.saxutils import escape

INK, ACCENT, GREY, MUTED, QUIET, FADED = "#1f1f1f", "#d4600b", "#6b6b6b", "#8a8a8a", "#9a968e", "#a8a49c"
PANEL, BORDER, ACCENT_FILL, HALO, WHITE = "#f0ede6", "#d8d4cc", "#fcefe5", "#e9c9ae", "#ffffff"
FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
LINE = 1.3  # line height as a multiple of font size


def _t(s):
    return escape(str(s))


class Diagram:
    def __init__(self, width=1200, height=700, font=FONT):
        self.w, self.h, self.font, self.parts = width, height, font, []

    # ---- text
    def text(self, x, y, s, size=14, color=GREY, weight=400, anchor="start"):
        """Text with its first baseline at y. '\\n' starts a new line below."""
        for i, line in enumerate(str(s).split("\n")):
            self.parts.append('<text x="%g" y="%g" font-size="%g" font-weight="%d" fill="%s"%s>%s</text>' % (
                x, y + i * size * LINE, size, weight, color,
                "" if anchor == "start" else ' text-anchor="%s"' % anchor, _t(line)))

    def title(self, x, y, s, size=21):
        self.text(x, y, s, size, INK, 700)

    def step(self, x, y, s, size=20, anchor="start"):
        """A numbered step label on the main path: '1. Write the event'."""
        self.text(x, y, s, size, ACCENT, 700, anchor)

    def note(self, x, y, s, size=13.5, anchor="start"):
        self.text(x, y, s, size, MUTED, 400, anchor)

    # ---- shapes
    def panel(self, x, y, w, h, heading=None, rx=14, heading_size=17):
        self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"/>' % (x, y, w, h, rx, PANEL))
        if heading:
            self.text(x + w / 2, y + 38, heading, heading_size, INK, 700, "middle")

    def box(self, x, y, w, h, title, sub=None, kind="plain", title_size=None, sub_size=14, rx=None):
        styles = {
            "plain":  (WHITE, BORDER, 1.5, ACCENT, None),
            "main":   (WHITE, INK, 2.5, INK, None),
            "accent": (ACCENT_FILL, ACCENT, 2.5, ACCENT, None),
            "faded":  (WHITE, "#e3dfd7", 1.5, QUIET, None),
            "dashed": (WHITE, FADED, 2, GREY, "8 6"),
            "dark":   (INK, INK, 0, WHITE, None),
        }
        fill, stroke, sw, tcolor, dash = styles[kind]
        rx = rx if rx is not None else (10 if kind == "main" else 9)
        if kind == "accent":
            self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"/>' % (x - 6, y - 6, w + 12, h + 12, rx + 3, HALO))
        self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g"%s/>' % (
            x, y, w, h, rx, fill, stroke, sw, ' stroke-dasharray="%s"' % dash if dash else ""))
        ts = title_size or (24 if kind == "main" else 19)
        tl = str(title).split("\n")
        sl = str(sub).split("\n") if sub else []
        block = len(tl) * ts * LINE + (len(sl) * sub_size * LINE + 4 if sl else 0)
        top = y + (h - block) / 2 + ts * 0.95
        self.text(x + w / 2, top, title, ts, tcolor, 700, "middle")
        if sl:
            scol = "#d9d6cf" if kind == "dark" else (QUIET if kind == "faded" else GREY)
            self.text(x + w / 2, top + len(tl) * ts * LINE + 4, sub, sub_size, scol, 400, "middle")

    def pill(self, x, y, s, kind="accent", size=14):
        """A small rounded tag: a status, a state name, a version. (x, y) is its left/top."""
        w = len(str(s)) * size * 0.62 + 24
        fill, col = {"accent": (ACCENT_FILL, ACCENT), "plain": (WHITE, GREY), "dark": (INK, WHITE), "ok": ("#e6f4ea", "#1e7a3c")}[kind]
        self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="1.2"/>' % (
            x, y, w, size + 14, (size + 14) / 2, fill, col))
        self.text(x + w / 2, y + size + 3, s, size, col, 700, "middle")
        return w

    def person(self, cx, cy, name=None, r=15):
        """A person icon centred at (cx, cy) (head centre), name below."""
        self.parts.append('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (cx, cy, r, INK))
        self.parts.append('<path d="M%g,%g Q%g,%g %g,%g Q%g,%g %g,%g Z" fill="%s"/>' % (
            cx - 1.9 * r, cy + 3.2 * r, cx - 1.9 * r, cy + 1.3 * r, cx, cy + 1.3 * r, cx + 1.9 * r, cy + 1.3 * r, cx + 1.9 * r, cy + 3.2 * r, INK))
        if name:
            self.text(cx, cy + 3.2 * r + 22, name, 16, INK, 700, "middle")

    def dot(self, cx, cy, r=8, color=INK):
        self.parts.append('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (cx, cy, r, color))

    def bar(self, x, y, w, h, color=ACCENT):
        self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="4" fill="%s"/>' % (x, y, w, h, color))

    def line(self, x1, y1, x2, y2, color=BORDER, width=1.5, dash=None):
        self.parts.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"%s/>' % (
            x1, y1, x2, y2, color, width, ' stroke-dasharray="%s"' % dash if dash else ""))

    # ---- arrows
    def arrow(self, pts, color="ink", width=None, dashed=False, both=False, head=True,
              label=None, label_at=None, label_side="right", label_size=14):
        """A straight or elbowed arrow through pts [(x, y), ...]; corners are rounded.
        label goes beside the first segment (right of a vertical one, above a horizontal one)
        unless label_at=(x, y) is given."""
        col = {"ink": INK, "accent": ACCENT, "grey": FADED}[color]
        width = width or (2.5 if color == "accent" else 2)
        mid = "a" + color
        d, r = "M%g,%g" % pts[0], 12
        for i in range(1, len(pts)):
            if i < len(pts) - 1:
                (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
                def toward(ax, ay, bx, by, k):
                    dx, dy = bx - ax, by - ay
                    n = max(abs(dx), abs(dy)) or 1
                    return ax + dx / n * k, ay + dy / n * k
                ax_, ay_ = toward(x1, y1, x0, y0, r)
                bx_, by_ = toward(x1, y1, x2, y2, r)
                d += " L%g,%g Q%g,%g %g,%g" % (ax_, ay_, x1, y1, bx_, by_)
            else:
                d += " L%g,%g" % pts[i]
        self.parts.append('<path d="%s" fill="none" stroke="%s" stroke-width="%g"%s%s%s/>' % (
            d, col, width, ' stroke-dasharray="10 7"' if dashed else "",
            ' marker-end="url(#%s)"' % mid if head else "", ' marker-start="url(#%s)"' % mid if both else ""))
        if label:
            if label_at:
                lx, ly, anchor = label_at[0], label_at[1], "start"
            else:
                (x0, y0), (x1, y1) = pts[0], pts[1]
                if abs(x1 - x0) < abs(y1 - y0):   # vertical: beside it
                    lx = x0 + 12 if label_side == "right" else x0 - 12
                    ly, anchor = (y0 + y1) / 2 - (label.count("\n") * label_size * LINE) / 2 + 5, ("start" if label_side == "right" else "end")
                else:                              # horizontal: above it, centred
                    lx, anchor = (x0 + x1) / 2, "middle"
                    ly = y0 - 12 - label.count("\n") * label_size * LINE
            self.text(lx, ly, label, label_size, ACCENT if color == "accent" and label[:1].isdigit() else GREY,
                      700 if color == "accent" and label[:1].isdigit() else 400, anchor)

    # ---- tables (the article's "database table" look)
    def table(self, x, y, w, name, kind, columns, rows, row_h=50, highlight=(), dropped=(), name_size=24):
        """columns: [(header, x_offset, anchor)], rows: [[cell, ...]]. highlight / dropped: row indexes.
        Highlighted rows are grouped in one orange frame; their last cell turns orange and bold."""
        top = y + 66
        h = 66 + 34 + len(rows) * (row_h + 10) + 12
        self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="18" fill="%s"/>' % (x, y, w, h, PANEL))
        self.text(x + 26, y + 44, name, name_size, ACCENT, 700)
        if kind:
            self.text(x + 34 + len(name) * name_size * 0.58, y + 44, kind, 17, GREY)
        for head, off, anchor in columns:
            self.text(x + off, top + 22, head, 15, GREY, 700, anchor)
        ry = top + 36
        hl = sorted(highlight)
        if hl:
            g0 = ry + hl[0] * (row_h + 10)
            gh = len(hl) * row_h + (len(hl) - 1) * 10
            self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="%s" stroke="%s" stroke-width="2.5"/>' % (
                x + 18, g0, w - 36, gh, WHITE, ACCENT))
        for i, row in enumerate(rows):
            yy = ry + i * (row_h + 10)
            if i in dropped:
                self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="9 7"/>' % (
                    x + 18, yy, w - 36, row_h, FADED))
            elif i not in highlight:
                self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="%s" stroke="#dedad2" stroke-width="1.5"/>' % (
                    x + 18, yy, w - 36, row_h, WHITE))
            for j, (cell, (head, off, anchor)) in enumerate(zip(row, columns)):
                last = j == len(columns) - 1
                col = QUIET if i in dropped else (ACCENT if (last and i in highlight) else (MUTED if last else (INK if j else GREY)))
                self.text(x + off, yy + row_h / 2 + 6, cell, 16, col, 700 if (last and i in highlight) else 400, anchor)
        return h

    # ---- output
    def svg(self):
        defs = "".join(
            '<marker id="a%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (n, c)
            for n, c in (("ink", INK), ("accent", ACCENT), ("grey", FADED)))
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="%s">\n'
                '  <defs>%s</defs>\n  <rect width="%d" height="%d" fill="#ffffff"/>\n  %s\n</svg>\n') % (
            self.w, self.h, self.w, self.h, self.font.replace('"', "'"), defs, self.w, self.h, "\n  ".join(self.parts))

    def save(self, path, dark=True):
        """Write the light diagram to path (the default theme) and, unless dark=False,
        its dark-mode twin to <name>-dark.svg next to it."""
        text = self.svg()
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        if dark:
            from theme import to_dark, dark_path
            with open(dark_path(path), "w", encoding="utf-8") as f:
                f.write(to_dark(text)[0])
        return path
