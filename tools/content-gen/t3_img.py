import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t3 import *
import msvg as S

# ---------- допоміжне ----------
def complement(parts):
    parts = sorted(parts, key=lambda p: (-10**9 if p[0] is None else p[0]))
    res = []; cur_lo, cur_lc = None, False
    for lo, hi, lc, rc in parts:
        if lo is not None: res.append((cur_lo, lo, cur_lc, not lc))
        if hi is None: return res
        cur_lo, cur_lc = hi, not rc
    res.append((cur_lo, None, cur_lc, False))
    return res
def flip_ends(parts):
    return [(lo, hi, (not lc) if lo is not None else lc, (not rc) if hi is not None else rc) for lo, hi, lc, rc in parts]
def pic_wrongs(sol):
    wr = [(setstr(flip_ends(sol)), 'зафарбовані й порожні точки на малюнку прочитано навпаки (дужки переплутано)'),
          (setstr(complement(sol)), 'вибрано проміжки, які на малюнку не заштриховані'),
          (setstr(mirror(sol)), 'знаки значень на кінцях проміжків змінено на протилежні')]
    if len(sol) >= 2: wr.append((setstr(sol[:1]), 'враховано лише один із заштрихованих проміжків'))
    else:
        lo, hi, lc, rc = sol[0]
        if lo is not None and hi is not None: wr.append((setstr([(lo, hi, lc, not rc if False else rc)][:0] or [(lo, hi, False, rc)]), 'лівий кінець проміжку не враховано, хоча точка на малюнку зафарбована') if lc else (setstr([(lo, hi, True, rc)]), 'лівий кінець проміжку включено, хоча точка на малюнку порожня'))
    return wr

def numline(c, y, xmin, xmax, parts, x0=40, x1=None, color=S.BLUE, step=1):
    x1 = c.w - 40 if x1 is None else x1
    X = lambda v: x0 + (float(v) - xmin) / (xmax - xmin) * (x1 - x0)
    c.line(x0 - 14, y, x1 + 16, y, col=S.AX, w=1.8, arrow=True)
    k = math.ceil(xmin / step - 1e-9)
    while k * step <= xmax + 1e-9:
        v = k * step; c.line(X(v), y - 4, X(v), y + 4, col=S.AX, w=1.4); c.text(X(v), y + 20, fmt(v) if v != 0 else '0', size=12, anchor='middle', col=S.GRAY); k += 1
    c.text(x1 + 18, y + 20, 'x', size=13, italic=True)
    for lo, hi, lc, rc in parts:
        if lo is not None and lo == hi:
            c.dot(X(lo), y, 5.5, color); c.text(X(lo), y - 14, fmt(lo), size=13, anchor='middle', bold=True, col=color); continue
        xa = X(lo) if lo is not None else x0 - 14; xb = X(hi) if hi is not None else x1 + 16
        c.line(xa, y, xb, y, col=color, w=5)
        t = xa + 4
        while t < xb - 3:
            c.line(t, y - 2, t + 6, y - 14, col=color, w=1.2); t += 8
        for v, cl in ((lo, lc), (hi, rc)):
            if v is None: continue
            if cl: c.dot(X(v), y, 5.5, color)
            else: c.circle(X(v), y, 5.5, fill='#fff', stroke=color, sw=2.2)
            c.text(X(v), y - 22, fmt(v), size=13, anchor='middle', bold=True, col=color)

def span_for(parts, pad=2):
    vs_ = [float(v) for p in parts for v in p[:2] if v is not None]
    lo = math.floor(min(vs_)) - pad; hi = math.ceil(max(vs_)) + pad
    return lo, hi

# ---------- I1: числова пряма → проміжок ----------
def f_img_numline(T, rng, lv):
    p, q = sorted(rng.sample(range(-7, 8), 2)); kind = rng.choice(['seg', 'out', 'ray', 'ray']); lcl, rcl = rng.random() < .5, rng.random() < .5
    if kind == 'seg': sol = [(F(p), F(q), lcl, rcl)]
    elif kind == 'out': sol = [(None, F(p), False, lcl), (F(q), None, rcl, False)]
    else:
        if rng.random() < .5: sol = [(None, F(p), False, lcl)]
        else: sol = [(F(q), None, rcl, False)]
    lo, hi = span_for(sol)
    c = S.C(560, 120, 'Множина розв’язків нерівності')
    numline(c, 78, lo, hi, sol, step=1 if hi - lo <= 16 else 2)
    img = c.save('t3_nl_' + S.tag(p, q, kind, lcl, rcl, sol[0][1] is None))
    return T.add(lv, 'На числовій прямій зображено множину розв’язків деякої нерівності (заштрихована частина). Запишіть цю множину у вигляді проміжків.', setstr(sol), pic_wrongs(sol),
                 'порожня точка (о) — кінець не належить множині, дужка «(» або «)»; зафарбована (●) — належить, дужка «[» або «]»', f'за малюнком: {setstr(sol)}', img=img)

# ---------- I2: числова пряма → нерівність ----------
def f_img_numline_ineq(T, rng, lv):
    m = rng.choice([v for v in range(-4, 5) if v]); r = rng.randint(1, 5)
    kind = rng.choice(['le', 'ge', 'lt', 'gt'])
    op = {'le': '<=', 'ge': '>=', 'lt': '<', 'gt': '>'}[kind]
    a, b = F(m - r), F(m + r)
    if op in ('<=', '<'): sol = [(a, b, op == '<=', op == '<=')]
    else: sol = [(None, a, False, op == '>='), (b, None, op == '>=', False)]
    lo, hi = span_for(sol)
    c = S.C(560, 120, 'Множина розв’язків нерівності')
    numline(c, 78, lo, hi, sol, step=1 if hi - lo <= 16 else 2)
    img = c.save('t3_nli_' + S.tag(m, r, kind))
    sh = f'x {"−" if m > 0 else "+"} {abs(m)}'
    opt = lambda o, s_: f'|{s_}| {OPS[o]} {r}'
    ans = opt(op, sh)
    other = {'<=': '>=', '>=': '<=', '<': '>', '>': '<'}
    wr = [(opt(other[op], sh), 'вибрано протилежний знак нерівності: множина була б доповненням'),
          (opt(TOG[op], sh), 'на малюнку точки ' + ('зафарбовані' if op in ('<=', '>=') else 'порожні') + ', тому нерівність ' + ('нестрога' if op in ('<=', '>=') else 'строга')),
          (opt(op, f'x {"+" if m > 0 else "−"} {abs(m)}'), 'центр симетрії проміжку взято з протилежним знаком'),
          (opt(op, 'x'), 'центр проміжку (середина між кінцями) не враховано')]
    return T.add(lv, 'На числовій прямій зображено множину розв’язків (заштрихована частина). Яка з нерівностей має саме такі розв’язки?', ans, wr,
                 '|x − m| ≤ r задає відрізок з центром у точці m і радіусом r; |x − m| ≥ r — дві промені назовні', f'центр — середина кінців = {m}, радіус = {r}; відповідь {ans}', img=img)

# ---------- I3: парабола-графік → нерівність ----------
def graph_axes(c, xmin, xmax, ymin, ymax, w=440, h=270, x0=55, y0=36, xs=1, ys=1, **kw):
    return S.Axes(c, x0, y0, w, h, xmin, xmax, ymin, ymax, xs, ys, **kw)

def f_img_parab_ineq(T, rng, lv):
    p, q = sorted(rng.sample(range(-5, 6), 2)); a = rng.choice([1, -1]); op = rng.choice(list(OPS))
    f = lambda x: a * (x - p) * (x - q)
    vy = abs(a * (p - q) ** 2 / 4); top = max(2, math.ceil(vy) + 1)
    xmin, xmax = min(p, q) - 2, max(p, q) + 2
    c = S.C(560, 340, 'Графік функції y = f(x)')
    ax = graph_axes(c, xmin, xmax, -top if a > 0 else -top, top, xs=1, ys=1 if top <= 10 else 2, ylab_every=1 if top <= 8 else 2, lab_every=1 if xmax - xmin <= 14 else 2)
    ax.curve(f, xmin + .05, xmax - .05, col=S.BLUE, w=2.8, steps=240)
    for r in (p, q): ax.point(r, 0, None, col=S.RED, r=5)
    img = c.save('t3_pb_' + S.tag(p, q, a))
    sol, wr = set_wrongs({F(p): 1, F(q): 1}, {}, a, op, fn=True)
    return T.add(lv, f'На малюнку зображено графік квадратичної функції y = f(x); відмічено точки перетину з віссю x. Розв’яжіть нерівність f(x) {OPS[op]} 0.', setstr(sol), wr,
                 'f(x) > 0 там, де графік лежить вище осі x; f(x) < 0 — нижче; нулі функції — точки перетину з віссю', f'нулі функції {p} та {q}; гілки {"вгору" if a > 0 else "вниз"}; відповідь {setstr(sol)}', img=img)

# ---------- I4: графіки двох прямих → система ----------
def f_img_lines(T, rng, lv):
    x, y = rng.randint(-4, 4), rng.randint(-4, 4)
    while True:
        k1, k2 = rng.choice([-3, -2, -1, 1, 2, 3, F(1, 2), F(-1, 2)]), rng.choice([-3, -2, -1, 1, 2, 3, F(1, 2), F(-1, 2)])
        if k1 != k2: break
    b1, b2 = y - k1 * x, y - k2 * x
    if abs(b1) > 6 or abs(b2) > 6 or F(b1).denominator != 1 or F(b2).denominator != 1: return False
    c = S.C(520, 360, 'Графіки двох рівнянь')
    ax = graph_axes(c, -7, 7, -7, 7, w=380, h=290, x0=60, y0=38, xs=1, ys=1)
    ax.curve(lambda t: float(k1 * t + b1), -7, 7, col=S.BLUE, w=2.6, steps=40); ax.curve(lambda t: float(k2 * t + b2), -7, 7, col=S.ORANGE, w=2.6, steps=40)
    used = []
    for (kk, bb, nm, colr, cands) in ((k1, b1, '(1)', S.BLUE, (5.5, -5.5, 4, -4, 3, -3)), (k2, b2, '(2)', S.ORANGE, (-5.5, 5.5, -4, 4, -3, 3))):
        for xl in cands:
            yl = float(kk * xl + bb)
            if abs(yl) <= 6 and abs(xl - x) >= 1.5 and all(abs(xl - ux) >= 1.5 or abs(yl - uy) >= 1.2 for ux, uy in used):
                ax.label(xl + 0.2, yl + 0.5, nm, col=colr, bold=True, size=14); used.append((xl, yl)); break
    img = c.save('t3_ln_' + S.tag(x, y, k1, k2))
    ask = rng.choice(['pair', 'pair', 'sum', 'x'])
    pr = lambda u, v: f'({fmt(u)}; {fmt(v)})'
    if ask == 'pair':
        ans = pr(x, y); wr = [(pr(y, x), 'координати точки перетину переставлено'), (pr(x, -y), 'знак y змінено'), (pr(-x, y), 'знак x змінено'), (pr(x + 1, y), 'координату x знято з малюнка з похибкою на одиницю')]
        q = 'Знайдіть розв’язок системи (x; y).'
    elif ask == 'sum':
        ans = x + y; wr = [(x - y, 'знайдено різницю x − y'), (x * y, 'знайдено добуток x · y'), (-(x + y), 'знак суми змінено'), (x + y + 1, 'координату знято з малюнка з похибкою на одиницю')]
        q = 'Знайдіть значення суми x + y для розв’язку системи.'
    else:
        ans = x; wr = [(y, 'знайдено ординату y замість абсциси x'), (-x, 'знак x змінено'), (x + 1, 'абсцису знято з малюнка з похибкою'), (x - 1, 'абсцису знято з малюнка з похибкою')]
        q = 'Знайдіть x — першу координату розв’язку системи.'
    return T.add(lv, 'На малюнку зображено графіки двох лінійних рівнянь (1) і (2) системи. ' + q, ans, wr,
                 'розв’язок системи — координати точки перетину графіків обох рівнянь', f'графіки перетинаються в точці ({fmt(x)}; {fmt(y)})', img=img)

# ---------- I5: парабола і горизонталь ----------
def f_img_parab_k(T, rng, lv):
    a = rng.choice([1, -1]); h = rng.randint(-3, 3); v = rng.randint(-4, 4)
    f = lambda t: a * (t - h) ** 2 + v
    lim = 6
    c = S.C(560, 340, 'Графік функції y = f(x)')
    ax = graph_axes(c, -6, 6, -lim, lim, xs=1, ys=1, lab_every=1, ylab_every=1)
    ax.curve(f, -5.9, 5.9, col=S.BLUE, w=2.8, steps=300)
    ax.point(h, v, None, col=S.RED, r=5)
    if lv == 2:
        k = rng.choice([x for x in range(-5, 6) if True])
        ax.seg(-6, k, 6, k, col=S.GREEN, w=1.8, dash='6 4'); ax.label(5.1, k + 0.4, f'y = {fmt(k)}', col=S.GREEN, bold=True, size=12)
        img = c.save('t3_pk_' + S.tag(a, h, v, k))
        d = a * (k - v)
        cnt = 2 if d > 0 else 1 if d == 0 else 0
        names = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'}
        why = {0: 'пряма y = k не перетинає графік', 1: 'пряма y = k лише дотикається до графіка у вершині', 2: 'пряма y = k перетинає графік у двох точках'}
        wr = [(names[w], why[w] + ', а на малюнку ' + ('двох точок перетину немає' if w == 2 else 'такого не видно' if w else 'точки перетину є')) for w in (0, 1, 2) if w != cnt]
        wr = [(names[0], 'вважали, що розв’язків немає, хоча пряма перетинає графік') if cnt > 0 and w[0] == '0' else w for w in wr]
        wr.append(('3', 'парабола не може перетнути пряму y = k більше ніж у двох точках'))
        return T.add(lv, f'На малюнку зображено графік функції y = f(x) (вершину позначено точкою) і пряму y = {fmt(k)}. Скільки коренів має рівняння f(x) = {fmt(k)}?', names[cnt], wr,
                     'корені рівняння f(x) = k — абсциси точок перетину графіка з горизонтальною прямою y = k', f'вершина ({h}; {v}); пряма y = {fmt(k)} має з графіком {cnt} спільн' + ('их точок' if cnt != 1 else 'у точку'), img=img)
    img = c.save('t3_pkp_' + S.tag(a, h, v))
    op = '>' if a > 0 else '<'
    ok = [(F(v), None, False, False)] if a > 0 else [(None, F(v), False, False)]
    wr = [(setstr([(F(v), None, True, False)] if a > 0 else [(None, F(v), False, True)]), 'при a = ' + str(v) + ' рівняння має лише один корінь (дотик у вершині)'),
          (setstr([(None, F(v), False, False)] if a > 0 else [(F(v), None, False, False)]), 'пряма y = a не перетинає графік в таких точках: взято протилежний бік від вершини'),
          (setstr([(F(h), None, False, False)] if a > 0 else [(None, F(h), False, False)]), 'замість ординати вершини взято її абсцису'),
          (setstr([(F(-v), None, False, False)] if a > 0 else [(None, F(-v), False, False)]), 'знак ординати вершини змінено')]
    return T.add(lv, 'На малюнку зображено графік функції y = f(x); вершину параболи позначено точкою. При яких значеннях a рівняння f(x) = a має два різні корені?', setstr(ok), wr,
                 'два корені — коли горизонтальна пряма y = a перетинає графік у двох точках', f'вершина ({h}; {v}); гілки {"вгору" if a > 0 else "вниз"}; два корені при a {">" if a > 0 else "<"} {v}', img=img)

# ---------- I6: схема знаків ----------
def f_img_signs(T, rng, lv):
    pat = rng.choice(['nn', 'nd', 'ndd', 'sq', 'nnd'])
    rts = sorted(rng.sample(range(-6, 7), 3))
    r0, r1, r2 = rts
    if pat == 'nn': num = {F(r0): 1, F(r1): 1}; den = {}
    elif pat == 'nd': num = {F(r0): 1}; den = {F(r1): 1}
    elif pat == 'ndd': num = {F(r0): 1}; den = {F(r1): 1, F(r2): 1}
    elif pat == 'sq': num = {F(r0): 2, F(r1): 1}; den = {}
    else: num = {F(r0): 1, F(r2): 1}; den = {F(r1): 1}
    lead = rng.choice([1, -1]) if lv >= 3 else 1
    op = rng.choice(list(OPS))
    crit = sorted(set(num) | set(den))
    def sg(x):
        s = 1 if lead > 0 else -1
        for r, m in list(num.items()) + list(den.items()):
            if x < r and m % 2: s = -s
        return s
    lo, hi = int(crit[0]) - 2, int(crit[-1]) + 2
    c = S.C(560, 150, 'Знаки функції f на проміжках')
    x0, x1, y = 40, 520, 90
    X = lambda v: x0 + (float(v) - lo) / (hi - lo) * (x1 - x0)
    c.line(x0 - 14, y, x1 + 16, y, col=S.AX, w=1.8, arrow=True)
    bnds = [lo - 0.5] + [float(v) for v in crit] + [hi + 0.5]
    for i in range(len(bnds) - 1):
        mid_ = (bnds[i] + bnds[i + 1]) / 2; s = sg(F(mid_).limit_denominator(1000))
        c.text(X(mid_), y - 34, '+' if s > 0 else '−', size=26, anchor='middle', bold=True, col=S.GREEN if s > 0 else S.RED)
    for r in crit:
        if r in den: c.circle(X(r), y, 6, fill='#fff', stroke=S.INK, sw=2.2)
        else: c.dot(X(r), y, 6, S.INK)
        c.text(X(r), y + 24, fmt(r), size=13, anchor='middle', bold=True)
    c.text(x1 + 18, y + 20, 'x', size=13, italic=True)
    c.text(40, 138, '● — нуль функції f;   ○ — точка, де f не існує', size=12, col=S.GRAY)
    img = c.save('t3_sg_' + S.tag(sorted(num.items()), sorted(den.items()), lead))
    sol = solve_gen(num, den, lead, op)
    strict = op in ('<', '>')
    wr = [(setstr(solve_gen(num, den, lead, OPP[op])), 'взято проміжки з протилежним знаком'),
          (setstr(solve_gen(num, den, lead, TOG[op])), 'нерівність строга, тому нулі функції не входять' if strict else 'нерівність нестрога, тому нулі функції входять у розв’язок')]
    if den:
        n2 = dict(num); n2.update(den)
        wr.append((setstr(solve_gen(n2, {}, lead, op)), 'точки, де функція не існує (○), включено до розв’язку'))
    wr.append((setstr(mirror(sol)), 'знаки значень у відповіді змінено на протилежні'))
    if any(m == 2 for m in num.values()): 
        n3 = {k: 1 for k in num}
        wr.append((setstr(solve_gen(n3, den, lead, op)), f'нуль {fmt([k for k, m in num.items() if m == 2][0])} прийнято за простий: через нього знак нібито змінюється, а на малюнку він не змінюється'))
    return T.add(lv, f'На малюнку показано знаки функції f на кожному з проміжків. Розв’яжіть нерівність f(x) {OPS[op]} 0.', setstr(sol), wr,
                 'нерівність f(x) > 0 — проміжки зі знаком «+», f(x) < 0 — зі знаком «−»; при нестрогій нерівності додайте нулі функції (●), але ніколи — точки розриву (○)', f'критичні точки: {", ".join(fmt(r) for r in crit)}; відповідь {setstr(sol)}', img=img)

# ---------- I7: тригонометричний графік і горизонталь ----------
def f_img_trig(T, rng, lv):
    fn = rng.choice(['sin', 'cos']); L = rng.choice([2, 2, 4]) if lv >= 3 else 2
    a = rng.choice([F(1), F(-1), F(0), F(1, 2), F(-1, 2), F(3, 2), F(-3, 2)] if lv >= 3 else [F(1), F(-1), F(0), F(1, 2), F(-1, 2)])
    fs = lambda v: ('−' if v < 0 else '') + (str(abs(v.numerator)) if v.denominator == 1 else f'{abs(v.numerator)}/{v.denominator}')
    base = math.sin if fn == 'sin' else math.cos
    w_, h_ = 600, 300
    c = S.C(w_, h_, f'Графік функції y = {fn} x')
    x0, y0, pw, ph = 60, 40, 470, 210
    ymin, ymax = -1.6, 1.6
    X = lambda t: x0 + t / (L * math.pi) * pw
    Y = lambda v: y0 + ph - (v - ymin) / (ymax - ymin) * ph
    ya = Y(0)
    for k in range(0, 2 * L + 1):
        t = k * math.pi / 2; c.line(X(t), y0, X(t), y0 + ph, col=S.GRID, w=1)
    for v in (-1, -0.5, 0.5, 1): c.line(x0, Y(v), x0 + pw, Y(v), col=S.GRID, w=1)
    c.line(x0 - 6, ya, x0 + pw + 14, ya, col=S.AX, w=1.6, arrow=True); c.line(x0, y0 + ph + 4, x0, y0 - 10, col=S.AX, w=1.6, arrow=True)
    c.text(x0 + pw + 14, ya + 16, 'x', size=13, italic=True); c.text(x0 + 8, y0 - 6, 'y', size=13, italic=True)
    labs = {1: 'π/2', 2: 'π', 3: '3π/2', 4: '2π', 5: '5π/2', 6: '3π', 7: '7π/2', 8: '4π'}
    for k in range(1, 2 * L + 1): c.text(X(k * math.pi / 2), ya + 16, labs[k], size=11, anchor='middle', col=S.GRAY)
    for v, s_ in ((1, '1'), (0.5, '1/2'), (-0.5, '−1/2'), (-1, '−1')): c.text(x0 - 7, Y(v) + 4, s_, size=11, anchor='end', col=S.GRAY)
    pts = [(X(t), Y(base(t))) for t in [L * math.pi * i / 400 for i in range(401)]]
    c.poly(pts, stroke=S.BLUE, w=2.8, close=False)
    c.line(x0, Y(float(a)), x0 + pw, Y(float(a)), col=S.GREEN, w=1.8, dash='6 4')
    c.text(x0 + 8, Y(float(a)) + (-6 if a >= 0 else 16), f'y = {fs(a)}', size=12, col=S.GREEN, bold=True, anchor='start')
    # точки перетину
    sols = set()
    av = float(a)
    if abs(av) <= 1 + 1e-12:
        if fn == 'sin':
            b0 = math.asin(av); cand = [b0 + 2 * math.pi * k for k in range(-3, 6)] + [math.pi - b0 + 2 * math.pi * k for k in range(-3, 6)]
        else:
            b0 = math.acos(av); cand = [b0 + 2 * math.pi * k for k in range(-3, 6)] + [-b0 + 2 * math.pi * k for k in range(-3, 6)]
        for t in cand:
            if -1e-9 <= t <= L * math.pi + 1e-9: sols.add(round(max(t, 0), 7))
    for t in sols: c.dot(X(t), Y(av), 4.5, S.RED)
    cnt = len(sols)
    img = c.save('t3_tr_' + S.tag(fn, L, a))
    names = {k: str(k) for k in range(0, 9)}
    pool = [k for k in (0, 1, 2, 3, 4, 5, 6) if k != cnt]
    near = sorted(pool, key=lambda k: abs(k - cnt))[:4]
    def why(k):
        if k < cnt: return 'частину точок перетину, зокрема на межах проміжку, пропущено'
        return 'враховано зайві точки перетину, яких на малюнку немає'
    wr = [(names[k], why(k)) for k in near]
    return T.add(lv, f'На малюнку зображено графік функції y = {fn} x на проміжку [0; {L}π] і пряму y = {fs(a)}. Скільки коренів на цьому проміжку має рівняння {fn} x = {fs(a)}?', names[cnt], wr,
                 'корені — абсциси спільних точок графіка й горизонтальної прямої; не забудьте про кінці проміжку', f'на [0; {L}π] маємо {cnt} ' + ('спільну точку' if cnt == 1 else 'спільні точки' if 2 <= cnt <= 4 else 'спільних точок') + ' — стільки ж коренів', img=img)

# ---------- I8: графік многочлена → нерівність ----------
def f_img_poly(T, rng, lv):
    kind = rng.choice(['3', '3', 'sq'])
    if kind == '3':
        r = sorted(rng.sample(range(-5, 6), 3)); num = {F(x): 1 for x in r}
    else:
        r = rng.sample(range(-5, 6), 2); num = {F(r[0]): 2, F(r[1]): 1}
    lead = rng.choice([1, -1]); op = rng.choice(list(OPS))
    f = lambda t: lead * math.prod((t - float(k)) ** m for k, m in num.items())
    xmin, xmax = min(r) - 2, max(r) + 2
    ys = [abs(f(min(r) - 0.6 + (max(r) - min(r) + 1.2) * i / 200)) for i in range(201)]
    ymaxv = max(ys)
    for st in (1, 2, 5, 10, 20, 50):
        if ymaxv / st <= 5: break
    top = int(math.ceil(ymaxv / st) + 1) * st
    c = S.C(560, 340, 'Графік многочлена y = P(x)')
    ax = graph_axes(c, xmin, xmax, -top, top, xs=1, ys=st, lab_every=1 if xmax - xmin <= 14 else 2, ylab_every=2 if top / st > 6 else 1)
    ax.curve(f, xmin + .05, xmax - .05, col=S.BLUE, w=2.8, steps=300)
    for k in num: ax.point(float(k), 0, None, col=S.RED, r=5)
    img = c.save('t3_pl_' + S.tag(sorted(num.items()), lead))
    sol, wr = set_wrongs(num, {}, lead, op, fn=True)
    if kind == 'sq':
        sq = [k for k, m in num.items() if m == 2][0]
        wr.insert(0, (setstr(solve_gen({k: 1 for k in num}, {}, lead, op)), f'нуль {fmt(sq)} прийнято за простий: знак при переході через нього нібито змінюється, а на малюнку графік лише дотикається до осі'))
    return T.add(lv, f'На малюнку зображено графік многочлена y = P(x); усі точки його перетину або дотику з віссю x позначено. Розв’яжіть нерівність P(x) {OPS[op]} 0.', setstr(sol), wr,
                 'дотик графіка до осі x не змінює знака P(x), але в цій точці P(x) = 0: при нестрогій нерівності вона входить у розв’язок (навіть як ізольована)', f'нулі: {", ".join(fmt(k) for k in sorted(num))}; відповідь {setstr(sol)}', img=img)

# ---------- I9: геометричні рівняння ----------
def f_img_geom(T, rng, lv):
    kind = rng.choice(['rect', 'tri', 'ring'])
    if kind == 'rect':
        x = rng.randint(2, 9); d = rng.randint(1, 7); area = x * (x + d)
        c = S.C(420, 250, 'Прямокутник')
        c.rect(70, 60, 240, 130, fill='#dbeafe', stroke=S.INK, sw=2)
        c.text(190, 52, f'x + {d}', size=15, anchor='middle', bold=True, col=S.BLUE); c.text(60, 130, 'x', size=15, anchor='end', bold=True, col=S.BLUE)
        c.text(190, 132, f'S = {area}', size=18, anchor='middle', bold=True)
        img = c.save('t3_gr_' + S.tag(x, d))
        wr = [(x + d, 'знайдено більшу сторону замість меншої'), (F(area, d), 'площу поділено на різницю сторін'), (-x - d, 'обрано від’ємний корінь рівняння, а довжина не може бути від’ємною'), (area - d, 'від площі віднято різницю сторін')]
        return T.add(lv, f'Сторони прямокутника дорівнюють x та x + {d}, його площа — {area} (див. малюнок). Знайдіть x.', x, wr, 'S = a·b: складіть рівняння x(x + d) = S; від’ємний корінь відкиньте', f'x² + {d}x − {area} = 0; x = {x}', img=img)
    if kind == 'tri':
        a, b = rng.choice([(3, 4), (5, 12), (8, 15), (6, 8), (7, 24), (9, 12), (12, 16), (20, 21)]); h = math.isqrt(a * a + b * b)
        d = b - a
        c = S.C(420, 260, 'Прямокутний трикутник')
        P0, P1, P2 = (70, 200), (70 + 20 * b * 0.9 if b < 12 else 300, 200), (70, 200 - (20 * a * 0.9 if b < 12 else 150 * a / b))
        P1 = (300, 200) if b >= 12 else (70 + 22 * b, 200); P2 = (70, 200 - (150 * a / b if b >= 12 else 22 * a))
        c.poly([P0, P1, P2], fill='#dbeafe', stroke=S.INK, w=2)
        S.right_angle(c, P0, P1, P2)
        c.text(60, (P0[1] + P2[1]) / 2 + 4, 'x', size=15, anchor='end', bold=True, col=S.BLUE)
        c.text((P0[0] + P1[0]) / 2, 224, f'x + {d}', size=15, anchor='middle', bold=True, col=S.BLUE)
        c.text((P1[0] + P2[0]) / 2 + 18, (P1[1] + P2[1]) / 2 - 6, f'{h}', size=15, anchor='start', bold=True, col=S.RED)
        img = c.save('t3_gt_' + S.tag(a, b))
        wr = [(b, 'знайдено більший катет'), (-b, 'обрано від’ємний корінь рівняння'), (h, 'відповіддю назвали гіпотенузу'), (F(h, 2), 'гіпотенузу поділено навпіл')]
        return T.add(lv, f'У прямокутного трикутника катети дорівнюють x та x + {d}, а гіпотенуза — {h} (див. малюнок). Знайдіть менший катет x.', a, wr, 'теорема Піфагора: x² + (x + d)² = c²', f'x² + (x + {d})² = {h*h}; {poly([2, 2*d, d*d - h*h])} = 0; x = {a}', img=img)
    s = rng.randint(4, 9); t = rng.randint(1, s - 2) if s > 3 else 1; area = s * s - t * t
    c = S.C(420, 280, 'Квадрат із квадратним вирізом')
    c.rect(60, 50, 190, 190, fill='#dbeafe', stroke=S.INK, sw=2); c.rect(105, 95, 100, 100, fill='#ffffff', stroke=S.INK, sw=2)
    c.text(155, 42, f'{s}', size=15, anchor='middle', bold=True, col=S.BLUE); c.text(155, 150, 'x', size=22, anchor='middle', bold=True, col=S.RED)
    c.text(275, 150, f'площа зафарбованої', size=13, anchor='start'); c.text(275, 168, f'частини {area}', size=13, anchor='start', bold=True)
    img = c.save('t3_gq_' + S.tag(s, t))
    wr = [(s - t, 'знайдено ширину рамки'), (F(area, s), 'площу поділено на сторону квадрата'), (s * s - area, 'знайдено площу вирізу, а не сторону'), (-t, 'обрано від’ємний корінь рівняння')]
    return T.add(lv, f'Із квадрата зі стороною {s} вирізали квадрат зі стороною x (див. малюнок). Площа частини, що залишилася, дорівнює {area}. Знайдіть x.', t, wr, f'{s}² − x² = {area}', f'{s*s} − x² = {area}; x² = {t*t}; x = {t}', img=img)

# ---------- I10: графік |x − a| + |x − b| ----------
def f_img_abs(T, rng, lv):
    a, b = sorted(rng.sample(range(-5, 6), 2)); d = b - a
    c_ = rng.choice([d - 1, d, d + 1, d + 2, d + 3])
    if c_ < 1: return False
    op = rng.choice(['<', '<=', '>', '>='])
    f = lambda t: abs(t - a) + abs(t - b)
    xmin, xmax = a - 4, b + 4
    top = max(c_, d) + 4
    c = S.C(560, 340, 'Графік функції y = f(x)')
    ax = graph_axes(c, xmin, xmax, 0, top, xs=1, ys=1, lab_every=1 if xmax - xmin <= 14 else 2, ylab_every=1 if top <= 10 else 2)
    ax.curve(f, xmin + .02, xmax - .02, col=S.BLUE, w=2.8, steps=300)
    ax.seg(xmin, c_, xmax, c_, col=S.GREEN, w=1.8, dash='6 4'); ax.label(xmin + .3, c_ + .35, f'y = {c_}', col=S.GREEN, bold=True, size=12)
    img = c.save('t3_ab_' + S.tag(a, b, c_))
    txa = f'|x {M if a > 0 else "+"} {abs(a)}|' if a else '|x|'; txb = f'|x {M if b > 0 else "+"} {abs(b)}|' if b else '|x|'
    cx = F(a + b, 2)
    if c_ > d: eq_set = [(cx - F(c_, 2), cx + F(c_, 2), op in ('<=',), op in ('<=',))]
    elif c_ == d: eq_set = [(F(a), F(b), True, True)]
    else: eq_set = []
    # f(x) op c
    full = {'<': eq_set, '<=': eq_set}
    if c_ > d:
        lo_, hi_ = cx - F(c_, 2), cx + F(c_, 2)
        if op == '<': sol = [(lo_, hi_, False, False)]
        elif op == '<=': sol = [(lo_, hi_, True, True)]
        elif op == '>': sol = [(None, lo_, False, False), (hi_, None, False, False)]
        else: sol = [(None, lo_, False, True), (hi_, None, True, False)]
    elif c_ == d:
        if op == '<': sol = []
        elif op == '<=': sol = [(F(a), F(b), True, True)]
        elif op == '>': sol = [(None, F(a), False, False), (F(b), None, False, False)]
        else: sol = [(None, F(a), False, True), (F(b), None, True, False)]
    else:
        if op in ('<', '<='): sol = []
        else: sol = [(None, None, False, False)]
    if not sol and c_ >= d: pass
    if len(sol) == 0 and False: return False
    ans = setstr(sol)
    wr = []
    if sol and not (len(sol) == 1 and sol[0][0] is None and sol[0][1] is None):
        wr.append((setstr(flip_ends(sol)), 'нерівність ' + ('строга' if op in ('<', '>') else 'нестрога') + ': дужки переплутано'))
        wr.append((setstr(complement(sol)), 'взято ту частину осі, де графік розташований з протилежного боку від прямої'))
        wr.append((setstr(mirror(sol)), 'знаки кінців змінено'))
    else:
        wr.append(('розв’язків немає' if sol else '(−∞; +∞)', 'не враховано положення прямої відносно графіка'))
    if (F(a), F(b), True, True) not in sol: wr.append((setstr([(F(a), F(b), True, True)]), 'проміжок між числами під модулями прийнято за розв’язок'))
    if len(wr) < 4: wr.append((setstr([(F(a), None, True, False)]), 'розглянуто лише один із модулів'))
    if len(wr) < 4: wr.append((setstr([(None, F(b), False, True)]), 'розглянуто лише один із модулів'))
    return T.add(lv, f'На малюнку зображено графік функції f(x) = {txa} + {txb} і пряму y = {c_}. Розв’яжіть нерівність f(x) {OPS[op]} {c_}.', ans, wr,
                 'розв’язок нерівності f(x) ≤ c — ті x, при яких графік лежить не вище прямої y = c', f'графік і пряма перетинаються в точках x = {fmt(F(a+b-c_,2))} та x = {fmt(F(a+b+c_,2))}' if c_ > d else (f'пряма дотикається до горизонтального дна графіка на [{a}; {b}]' if c_ == d else 'пряма проходить нижче графіка'), img=img)

# ---------- I11: показникова/логарифмічна функція ----------
def f_img_exp(T, rng, lv):
    b = rng.choice([2, 2, 3, F(1, 2)]); k = rng.choice([1, 2, 3] if b != 3 else [1, 2]); op = rng.choice(list(OPS))
    f = lambda t: float(b) ** t
    N = F(b) ** k
    c = S.C(560, 340, f'Графік функції y = {fmt(b) if not isinstance(b, F) else "(1/2)"}ˣ')
    if isinstance(b, F): xmin, xmax = -4, 3
    else: xmin, xmax = -3, 4
    ymax = 9 if b == 3 else 9 if isinstance(b, F) else 9
    ax = graph_axes(c, xmin, xmax, 0, 9, xs=1, ys=1, lab_every=1, ylab_every=1)
    ax.curve(f, xmin + .02, xmax - .02, col=S.BLUE, w=2.8, steps=300)
    ax.seg(xmin, float(N), xmax, float(N), col=S.GREEN, w=1.8, dash='6 4'); ax.label(xmin + .2, float(N) + .35, f'y = {fmt(N)}', col=S.GREEN, bold=True, size=12)
    xk = -k if isinstance(b, F) else k
    ax.point(xk, float(N), None, col=S.RED, r=5)
    img = c.save('t3_ex_' + S.tag(b, k))
    inc = F(b) > 1; ox = op if inc else OPP[op]
    sol = [ray(ox, F(xk))]; strict = op in ('<', '>')
    wr = [(setstr([ray(OPP[ox], F(xk))]), 'взято частину осі x, де графік розташований з протилежного боку від прямої'),
          (setstr([ray(TOG[ox], F(xk))]), 'нерівність строга, тому точка перетину не входить' if strict else 'нерівність нестрога, тому точка перетину входить'),
          (setstr([ray(op, N)]), 'розв’язком названо ординату точки перетину замість абсциси'),
          (setstr([ray(ox, F(-xk))]), 'знак абсциси точки перетину змінено')]
    bs = fmt(b) if not isinstance(b, F) else '(1/2)'
    return T.add(lv, f'На малюнку зображено графік функції y = {bs}^x і пряму y = {fmt(N)}; точку перетину позначено. Розв’яжіть нерівність {bs}^x {OPS[op]} {fmt(N)}.', setstr(sol), wr,
                 'розв’язок — ті x, при яких графік лежить вище (нижче) прямої; для основи a > 1 функція зростає, для 0 < a < 1 — спадає', f'точка перетину при x = {xk}; {"зростає" if inc else "спадає"}; відповідь {setstr(sol)}', img=img)

IMGF = [(f_img_numline, [1, 2]), (f_img_numline_ineq, [2, 3]), (f_img_parab_ineq, [2]), (f_img_lines, [1, 2]), (f_img_parab_k, [2, 3]), (f_img_signs, [2, 3]), (f_img_trig, [2, 3]), (f_img_poly, [3]), (f_img_geom, [2]), (f_img_abs, [3]), (f_img_exp, [2])]
FAMS = FAMS + IMGF + IMGF
