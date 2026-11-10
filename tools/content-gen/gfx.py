"""Спільні графічні помічники для малюнкових родин (теми 5+): сітка, ламані, панелі, підписи."""
import math
from fractions import Fraction as F
import msvg as S
from mgen import fmt, MINUS

def G(xmin, xmax, ymin, ymax, title=None, W=560, maxcell=36, maxw=460, maxh=330, **kw):
    """полотно з квадратною сіткою 1×1"""
    nx, ny = xmax - xmin, ymax - ymin
    cell = min(maxcell, maxw / nx, maxh / ny)
    w, h = cell * nx, cell * ny
    x0 = (W - w) / 2; y0 = 46 if title else 24
    c = S.C(W, int(h + y0 + 32), title)
    ax = S.Axes(c, x0, y0, w, h, xmin, xmax, ymin, ymax, 1, 1, **kw)
    return c, ax
def legend(c, items, y=18, x=None):
    tot = sum(46 + 8 * len(s) for _, s in items); x = (c.w - tot) / 2 if x is None else x
    for col, s in items:
        c.line(x, y - 4, x + 26, y - 4, col=col, w=3); c.text(x + 32, y, s, size=13, col=col, bold=True); x += 46 + 8 * len(s)
def halo(c, x, y, s_, size=11, col=S.GRAY, anchor='middle', bold=False):
    c.e.append(f'<text x="{S.n(x)}" y="{S.n(y)}" {S.FONT} font-size="{size}" fill="{col}" text-anchor="{anchor}"{" font-weight=\"bold\"" if bold else ""} stroke="#ffffff" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round">{S.esc(s_)}</text>')
def pim(x):
    x = F(x)
    if x == 0: return '0'
    sg = MINUS if x < 0 else ''; x = abs(x)
    if x.denominator == 1: return sg + ('π' if x == 1 else f'{x.numerator}π')
    return sg + ('π' if x.numerator == 1 else f'{x.numerator}π') + f'/{x.denominator}'

# ---------- ламана ----------
def pl_val(V, x):
    x = F(x)
    for (x1, y1), (x2, y2) in zip(V, V[1:]):
        if x1 <= x <= x2: return F(y1) + F(y2 - y1) * (x - x1) / (x2 - x1)
    return None
def pl_solve(V, a):
    a = F(a); res = set()
    for (x1, y1), (x2, y2) in zip(V, V[1:]):
        if y1 == y2:
            continue
        if min(y1, y2) <= a <= max(y1, y2): res.add(F(x1) + (a - y1) * F(x2 - x1) / F(y2 - y1))
    return sorted(res)
def pl_int(V, a, b):
    """точний інтеграл ламаної на [a; b]"""
    a, b = F(a), F(b); tot = F(0)
    for (x1, y1), (x2, y2) in zip(V, V[1:]):
        lo, hi = max(a, F(x1)), min(b, F(x2))
        if lo < hi: tot += (pl_val(V, lo) + pl_val(V, hi)) / 2 * (hi - lo)
    return tot
def pl_area(V, a, b):
    """площа між ламаною та віссю x (без знака)"""
    pts = sorted(set([F(a), F(b)] + [z for z in pl_solve(V, 0) if a < z < b] + [F(x) for x, _ in V if a < x < b]))
    return sum(abs(pl_int(V, p, q)) for p, q in zip(pts, pts[1:]))
def gen_pl(rng, nseg=(3, 5), int_zeros=False, need_zero=False, ylo=-4, yhi=5, xlo=-6, xhi=7, maxstep=3, x_start=None, y_start=None, flat=0.0):
    for _ in range(6000):
        k = rng.randint(*nseg)
        x = rng.randint(xlo, xlo + 2) if x_start is None else x_start; xs = [x]
        for i in range(k): x += rng.randint(1, maxstep); xs.append(x)
        if not (xhi - 3 <= xs[-1] <= xhi): continue
        d = rng.choice([1, -1]); y = rng.randint(ylo + 1, yhi - 1) if y_start is None else y_start; ys_ = [y]; ok = True
        for i in range(k):
            if flat and rng.random() < flat and i > 0 and ys_[-1] != ys_[-2]: ys_.append(y); continue
            y += d * rng.randint(1, 5); d = -d
            if not ylo <= y <= yhi: ok = False; break
            ys_.append(y)
        if not ok: continue
        V = list(zip(xs, ys_)); z = pl_solve(V, 0)
        if need_zero and not z: continue
        if int_zeros and any(t.denominator != 1 for t in z): continue
        return V
    raise ValueError('gen_pl: не вдалося згенерувати ламану')
def draw_pl(V, title='Графік функції y = f(x)', ends=(True, True), view=None, col=S.BLUE, **kw):
    xs = [x for x, _ in V]; ys_ = [y for _, y in V]
    xmin, xmax, ymin, ymax = view or (min(min(xs) - 1, -1), max(max(xs) + 1, 1), min(min(ys_) - 1, -1), max(max(ys_) + 1, 1))
    c, ax = G(xmin, xmax, ymin, ymax, title, **kw)
    c.poly([(ax.X(x), ax.Y(y)) for x, y in V], stroke=col, w=2.8, close=False)
    for (x, y), cl in ((V[0], ends[0]), (V[-1], ends[1])): ax.point(x, y, None, col=col, r=4.5, hollow=not cl)
    return c, ax

# ---------- панелі 2×2 ----------
def panel_canvas(drawers, title=None, rng_=(-5, 5), nums=True):
    c = S.C(600, 610 if not title else 630, title); oy = 20 if title else 0
    for i, dr in enumerate(drawers):
        x0 = 40 + (i % 2) * 290; y0 = 44 + (i // 2) * 290 + oy; w = h = 230
        ax = S.Axes(c, x0, y0, w, h, rng_[0], rng_[1], rng_[0], rng_[1], 1, 1, labels=False, size=10)
        dr(ax)
        halo(c, ax.X(1), ax.Y(0) + 14, '1', size=10); halo(c, ax.X(0) - 6, ax.Y(1) + 4, '1', size=10, anchor='end'); halo(c, ax.X(0) - 6, ax.Y(0) + 13, '0', size=10, anchor='end')
        if nums: c.circle(x0 + 14, y0 + 14, 12, fill='#1f2937', stroke='#1f2937'); c.text(x0 + 14, y0 + 19, str(i + 1), size=14, col='#ffffff', anchor='middle', bold=True)
    return c
def cv(fn, a=-5, b=5, col=S.BLUE): return lambda ax: ax.curve(fn, a, b, col=col, w=2.4, steps=400)

def fill_under(ax, fn, a, b, base=lambda t: 0.0, fill='#bfdbfe', steps=80, stroke='none'):
    """зафарбовує область між y = fn(x) та y = base(x) на [a; b]"""
    up = [(ax.X(a + (b - a) * i / steps), ax.Y(fn(a + (b - a) * i / steps))) for i in range(steps + 1)]
    dn = [(ax.X(a + (b - a) * i / steps), ax.Y(base(a + (b - a) * i / steps))) for i in range(steps, -1, -1)]
    ax.c.poly(up + dn, fill=fill, stroke=stroke, w=0)

def pmul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): r[i + j] += F(a) * b
    return r
def pval(co, x):
    r = 0.0
    for c in co: r = r * x + float(c)
    return r
