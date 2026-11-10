"""Мінімальна SVG-бібліотека для математичних малюнків (графіки, фігури, діаграми)."""
import math, os, hashlib
IMG = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public', 'img', 'math'))
os.makedirs(IMG, exist_ok=True)
FONT = "font-family=\"Arial, Helvetica, sans-serif\""
INK = '#1f2937'; GRID = '#e5e7eb'; AX = '#374151'; BLUE = '#2563eb'; RED = '#dc2626'; GREEN = '#16a34a'; ORANGE = '#ea580c'; PURPLE = '#7c3aed'; GRAY = '#6b7280'
PAL = ['#2563eb', '#ea580c', '#16a34a', '#7c3aed', '#dc2626', '#0891b2', '#ca8a04', '#db2777']
LIGHT = ['#dbeafe', '#ffedd5', '#dcfce7', '#ede9fe', '#fee2e2', '#cffafe', '#fef9c3', '#fce7f3']

def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def n(x): return ('%.2f' % x).rstrip('0').rstrip('.')

class C:
    def __init__(self, w, h, title=None):
        self.w, self.h = w, h; self.e = []
        self.e.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>')
        if title: self.text(w / 2, 22, title, size=15, bold=True, anchor='middle')
    def line(self, x1, y1, x2, y2, col=INK, w=1.5, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.e.append(f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{col}" stroke-width="{w}"{d} stroke-linecap="round"/>')
        if arrow:
            a = math.atan2(y2 - y1, x2 - x1); L = 9
            p = [(x2, y2), (x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4)), (x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))]
            self.poly(p, fill=col, stroke=col, w=1)
    def rect(self, x, y, w, h, fill='none', stroke=INK, sw=1.5, rx=0):
        self.e.append(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def circle(self, x, y, r, fill='none', stroke=INK, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.e.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def dot(self, x, y, r=3.5, col=INK): self.circle(x, y, r, fill=col, stroke=col, sw=1)
    def ellipse(self, x, y, rx, ry, fill='none', stroke=INK, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.e.append(f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(rx)}" ry="{n(ry)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def poly(self, pts, fill='none', stroke=INK, w=1.5, close=True, dash=None):
        tag = 'polygon' if close else 'polyline'
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.e.append(f'<{tag} points="{" ".join(n(x) + "," + n(y) for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"{d}/>')
    def path(self, d, fill='none', stroke=INK, w=1.5, dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ''
        self.e.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"{dd}/>')
    def text(self, x, y, s, size=13, col=INK, anchor='start', bold=False, italic=False, rot=None):
        t = f' transform="rotate({rot} {n(x)} {n(y)})"' if rot else ''
        st = (' font-weight="bold"' if bold else '') + (' font-style="italic"' if italic else '')
        self.e.append(f'<text x="{n(x)}" y="{n(y)}" {FONT} font-size="{size}" fill="{col}" text-anchor="{anchor}"{st}{t}>{esc(s)}</text>')
    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
                + ''.join(self.e) + '</svg>')
    def save(self, name):
        p = f'{IMG}/{name}.svg'
        open(p, 'w', encoding='utf-8').write(self.svg())
        return f'/img/math/{name}.svg'

def tag(*parts):
    return hashlib.md5('|'.join(str(p) for p in parts).encode()).hexdigest()[:8]

def dec(x, nd=1):
    s = ('%.' + str(nd) + 'f') % x
    return s.rstrip('0').rstrip('.').replace('.', ',').replace('-', '−') if '.' in s else s.replace('-', '−')

class Axes:
    """Декартова система з сіткою; mx/my — перетворення з математичних координат у піксельні."""
    def __init__(self, c, x0, y0, w, h, xmin, xmax, ymin, ymax, xstep=1, ystep=1, grid=True, labels=True, xlab='x', ylab='y', lab_every=1, ylab_every=1, size=11):
        self.c, self.x0, self.y0, self.w, self.h = c, x0, y0, w, h
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        sx = w / (xmax - xmin); sy = h / (ymax - ymin); self.sx, self.sy = sx, sy
        if grid:
            k = math.ceil(xmin / xstep - 1e-9)
            while k * xstep <= xmax + 1e-9:
                X = self.X(k * xstep); c.line(X, y0, X, y0 + h, col=GRID, w=1); k += 1
            k = math.ceil(ymin / ystep - 1e-9)
            while k * ystep <= ymax + 1e-9:
                Y = self.Y(k * ystep); c.line(x0, Y, x0 + w, Y, col=GRID, w=1); k += 1
        ax_y = self.Y(0) if ymin <= 0 <= ymax else y0 + h
        ax_x = self.X(0) if xmin <= 0 <= xmax else x0
        c.line(x0 - 4, ax_y, x0 + w + 12, ax_y, col=AX, w=1.6, arrow=True)
        c.line(ax_x, y0 + h + 4, ax_x, y0 - 12, col=AX, w=1.6, arrow=True)
        c.text(x0 + w + 12, ax_y + 15, xlab, size=size + 1, italic=True)
        c.text(ax_x + 8, y0 - 6, ylab, size=size + 1, italic=True)
        if labels:
            k = math.ceil(xmin / xstep - 1e-9); i = 0
            while k * xstep <= xmax + 1e-9:
                v = k * xstep
                if abs(v) > 1e-9 and i % lab_every == 0:
                    X = self.X(v); c.line(X, ax_y - 3, X, ax_y + 3, col=AX, w=1.2)
                    c.text(X, ax_y + 16, dec(v, 2), size=size, anchor='middle', col=GRAY)
                k += 1; i += 1
            k = math.ceil(ymin / ystep - 1e-9); i = 0
            while k * ystep <= ymax + 1e-9:
                v = k * ystep
                if abs(v) > 1e-9 and i % ylab_every == 0:
                    Y = self.Y(v); c.line(ax_x - 3, Y, ax_x + 3, Y, col=AX, w=1.2)
                    c.text(ax_x - 7, Y + 4, dec(v, 2), size=size, anchor='end', col=GRAY)
                k += 1; i += 1
            c.text(ax_x - 7, ax_y + 15, '0', size=size, anchor='end', col=GRAY)
    def X(self, x): return self.x0 + (x - self.xmin) * self.sx
    def Y(self, y): return self.y0 + self.h - (y - self.ymin) * self.sy
    def curve(self, fn, a=None, b=None, col=BLUE, w=2.4, steps=200, dash=None):
        a = self.xmin if a is None else a; b = self.xmax if b is None else b
        pts = []
        for i in range(steps + 1):
            x = a + (b - a) * i / steps
            try: y = fn(x)
            except Exception: y = None
            pts.append((x, y))
        lo, hi = self.ymin, self.ymax
        segs = []; cur = []
        for (xa_, ya_), (xb_, yb_) in zip(pts, pts[1:]):
            if ya_ is None or yb_ is None or (ya_ < lo and yb_ < lo) or (ya_ > hi and yb_ > hi):
                if len(cur) > 1: segs.append(cur)
                cur = []; continue
            dy = yb_ - ya_; t0, t1 = 0.0, 1.0
            if dy != 0:
                ta, tb = (lo - ya_) / dy, (hi - ya_) / dy
                t0 = max(t0, min(ta, tb)); t1 = min(t1, max(ta, tb))
            if t0 > t1: 
                if len(cur) > 1: segs.append(cur)
                cur = []; continue
            p0 = (self.X(xa_ + (xb_ - xa_) * t0), self.Y(ya_ + dy * t0)); p1 = (self.X(xa_ + (xb_ - xa_) * t1), self.Y(ya_ + dy * t1))
            if t0 > 1e-9 or not cur:
                if len(cur) > 1: segs.append(cur)
                cur = [p0]
            cur.append(p1)
            if t1 < 1 - 1e-9: segs.append(cur); cur = []
        if len(cur) > 1: segs.append(cur)
        for sg in segs: self.c.poly(sg, stroke=col, w=w, close=False, dash=dash)
    def point(self, x, y, label=None, col=RED, dx=6, dy=-8, r=4, hollow=False, size=13):
        X, Y = self.X(x), self.Y(y)
        if hollow: self.c.circle(X, Y, r, fill='#fff', stroke=col, sw=2)
        else: self.c.dot(X, Y, r, col)
        if label: self.c.text(X + dx, Y + dy, label, size=size, col=col, bold=True)
    def seg(self, x1, y1, x2, y2, col=INK, w=2, dash=None):
        self.c.line(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), col=col, w=w, dash=dash)
    def label(self, x, y, s, col=INK, size=12, anchor='start', bold=False): self.c.text(self.X(x), self.Y(y), s, size=size, col=col, anchor=anchor, bold=bold)

def pie(c, cx, cy, r, parts, colors=None, labels=None, start=-90, inner_text=True, size=13):
    """parts — частки (сума довільна); labels — підписи (рядки) всередині/зовні."""
    tot = sum(parts); a = start; colors = colors or LIGHT
    for i, p in enumerate(parts):
        a2 = a + 360 * p / tot
        x1, y1 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
        large = 1 if a2 - a > 180 else 0
        if len(parts) == 1: c.circle(cx, cy, r, fill=colors[0], stroke=INK)
        else: c.path(f'M{n(cx)},{n(cy)} L{n(x1)},{n(y1)} A{r},{r} 0 {large} 1 {n(x2)},{n(y2)} Z', fill=colors[i % len(colors)], stroke='#fff', w=2)
        if labels:
            m = math.radians((a + a2) / 2); rr = r * 0.62 if inner_text else r + 22
            c.text(cx + rr * math.cos(m), cy + rr * math.sin(m) + 5, labels[i], size=size, anchor='middle', bold=True)
        a = a2

def bars(c, ax, vals, labels, col=BLUE, bw=0.55, show=True, cols=None, size=12):
    """Стовпчикова діаграма на вже побудованих Axes (x = 1..n)."""
    for i, v in enumerate(vals):
        x = i + 1
        X1, X2 = ax.X(x - bw / 2), ax.X(x + bw / 2)
        c.rect(X1, ax.Y(v), X2 - X1, ax.Y(0) - ax.Y(v), fill=(cols[i] if cols else col), stroke='#1e3a8a', sw=1)
        if show: c.text((X1 + X2) / 2, ax.Y(v) - 5, dec(v, 1), size=size, anchor='middle', bold=True)
        c.text((X1 + X2) / 2, ax.Y(0) + 17, labels[i], size=size, anchor='middle')

def poly_label(c, pts, names, off=14, size=15, col=INK, centre=None):
    """Підписи вершин назовні від центру багатокутника."""
    cx = sum(p[0] for p in pts) / len(pts) if centre is None else centre[0]
    cy = sum(p[1] for p in pts) / len(pts) if centre is None else centre[1]
    for (x, y), s in zip(pts, names):
        dx, dy = x - cx, y - cy; d = math.hypot(dx, dy) or 1
        c.text(x + dx / d * off, y + dy / d * off + 5, s, size=size, col=col, anchor='middle', bold=True)

def mid(p, q): return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)

def side_label(c, p, q, s, centre, off=14, size=13, col=BLUE):
    mx, my = mid(p, q); dx, dy = mx - centre[0], my - centre[1]; d = math.hypot(dx, dy) or 1
    c.text(mx + dx / d * off, my + dy / d * off + 4, s, size=size, col=col, anchor='middle', bold=True)

def right_angle(c, v, p, q, s=11, col=INK):
    """Позначка прямого кута у вершині v між променями на p та q."""
    def unit(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy); return dx / d, dy / d
    u, w = unit(v, p), unit(v, q)
    a = (v[0] + u[0] * s, v[1] + u[1] * s); b = (v[0] + (u[0] + w[0]) * s, v[1] + (u[1] + w[1]) * s); d2 = (v[0] + w[0] * s, v[1] + w[1] * s)
    c.poly([a, b, d2], stroke=col, w=1.3, close=False)

def angle_arc(c, v, p, q, r=24, col=ORANGE, label=None, size=12):
    a1 = math.atan2(p[1] - v[1], p[0] - v[0]); a2 = math.atan2(q[1] - v[1], q[0] - v[0])
    d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    x1, y1 = v[0] + r * math.cos(a1), v[1] + r * math.sin(a1); x2, y2 = v[0] + r * math.cos(a1 + d), v[1] + r * math.sin(a1 + d)
    c.path(f'M{n(x1)},{n(y1)} A{r},{r} 0 0 {1 if d > 0 else 0} {n(x2)},{n(y2)}', stroke=col, w=1.8)
    if label:
        m = a1 + d / 2
        c.text(v[0] + (r + 14) * math.cos(m), v[1] + (r + 14) * math.sin(m) + 4, label, size=size, col=col, anchor='middle', bold=True)
