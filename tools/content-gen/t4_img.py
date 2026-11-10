import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t4b import *
import msvg as S

# ================= малюнкові родини теми 4 (частина A: ламані, прямі, параболи) =================
OPPS = {'>': '<', '<': '>', '>=': '<=', '<=': '>='}
TOGS = {'>': '>=', '>=': '>', '<': '<=', '<=': '<'}
SYM = {'>': '>', '<': '<', '>=': '≥', '<=': '≤'}
CMP = {'>': lambda v, t=0: v > t, '<': lambda v, t=0: v < t, '>=': lambda v, t=0: v >= t, '<=': lambda v, t=0: v <= t}
def kor(k): return f'{k} корінь' if k == 1 else (f'{k} корені' if k in (2, 3, 4) else f'{k} коренів')
def I(p, q, lc=True, rc=True): return setstr([(None if p is None else F(p), None if q is None else F(q), lc, rc)])

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
    """items: [(колір, підпис)] — рядок-легенда над графіком"""
    tot = sum(46 + 8 * len(s) for _, s in items); x = (c.w - tot) / 2 if x is None else x
    for col, s in items:
        c.line(x, y - 4, x + 26, y - 4, col=col, w=3); c.text(x + 32, y, s, size=13, col=col, bold=True); x += 46 + 8 * len(s)

# ---------- ламана ----------
def pl_val(V, x):
    x = F(x)
    for (x1, y1), (x2, y2) in zip(V, V[1:]):
        if x1 <= x <= x2: return F(y1) + F(y2 - y1) * (x - x1) / (x2 - x1)
    return None
def pl_solve(V, a):
    a = F(a); res = set()
    for (x1, y1), (x2, y2) in zip(V, V[1:]):
        if y1 == y2: continue
        if min(y1, y2) <= a <= max(y1, y2): res.add(F(x1) + (a - y1) * F(x2 - x1) / F(y2 - y1))
    return sorted(res)
def gen_pl(rng, nseg=(3, 5), int_zeros=False, need_zero=False, ylo=-4, yhi=5, xlo=-6, xhi=7, maxstep=3, x_start=None, y_start=None):
    for _ in range(4000):
        k = rng.randint(*nseg)
        x = rng.randint(xlo, xlo + 2) if x_start is None else x_start; xs = [x]
        for i in range(k): x += rng.randint(1, maxstep); xs.append(x)
        if not (xhi - 3 <= xs[-1] <= xhi): continue
        d = rng.choice([1, -1]); y = rng.randint(ylo + 1, yhi - 1) if y_start is None else y_start; ys_ = [y]; ok = True
        for i in range(k):
            y += d * rng.randint(1, 5); d = -d
            if not ylo <= y <= yhi: ok = False; break
            ys_.append(y)
        if not ok: continue
        V = list(zip(xs, ys_)); z = pl_solve(V, 0)
        if need_zero and not z: continue
        if int_zeros and any(t.denominator != 1 for t in z): continue
        return V
    raise ValueError('gen_pl: не вдалося згенерувати ламану')
def draw_pl(V, title='Графік функції y = f(x)', ends=(True, True), view=None):
    xs = [x for x, _ in V]; ys_ = [y for _, y in V]
    xmin, xmax, ymin, ymax = view or (min(min(xs) - 1, -1), max(max(xs) + 1, 1), min(min(ys_) - 1, -1), max(max(ys_) + 1, 1))
    c, ax = G(xmin, xmax, ymin, ymax, title)
    c.poly([(ax.X(x), ax.Y(y)) for x, y in V], stroke=S.BLUE, w=2.8, close=False)
    for (x, y), cl in ((V[0], ends[0]), (V[-1], ends[1])): ax.point(x, y, None, col=S.BLUE, r=4.5, hollow=not cl)
    return c, ax
def dom(V): return V[0][0], V[-1][0]
BASE = 'На малюнку зображено графік функції y = f(x), визначеної на відрізку [{a}; {b}]. '
def base(V): a, b = dom(V); return BASE.format(a=fmt(a), b=fmt(b))

# ---------- I1: значення функції за графіком ----------
def f_img_pl_value(T, rng, lv):
    V = gen_pl(rng); a, b = dom(V)
    cands = [x for x in range(a + 1, b) if x != 0 and pl_val(V, x).denominator == 1 and pl_val(V, x) != x]
    if not cands: return False
    x0 = rng.choice(cands); y0 = pl_val(V, x0)
    c, ax = draw_pl(V); img = c.save('t4_plv_' + S.tag(V))
    wr = []
    inv = [t for t in pl_solve(V, x0) if t.denominator == 1]
    if inv: wr.append((inv[0], f'знайдено x, при якому f(x) = {fmt(x0)}: переплутано аргумент і значення функції'))
    if a <= -x0 <= b: wr.append((pl_val(V, -x0), f'значення прочитано в точці x = {fmt(-x0)} (знак аргументу змінено)'))
    wr += [(-y0, 'знак значення функції змінено')] + [(pl_val(V, t), f'значення прочитано в сусідній точці x = {fmt(t)}') for t in (x0 + 1, x0 - 1) if pl_val(V, t).denominator <= 2]
    return T.add(lv, base(V) + f'Знайдіть f({fmt(x0)}).', y0, wr,
                 'f(x₀) — ордината точки графіка з абсцисою x₀: від x₀ на осі x рухайтеся вертикально до графіка, потім горизонтально до осі y',
                 f'точка графіка з абсцисою {fmt(x0)} має ординату {fmt(y0)}', img=img)

# ---------- I2: найбільше / найменше значення ----------
def f_img_pl_extreme(T, rng, lv):
    V = gen_pl(rng); a, b = dom(V); ys_ = [y for _, y in V]; mx, mn = max(ys_), min(ys_)
    xmx = [x for x, y in V if y == mx]; xmn = [x for x, y in V if y == mn]
    c, ax = draw_pl(V); img = c.save('t4_ple_' + S.tag(V))
    if lv == 1:
        big = rng.random() < .5; ans = mx if big else mn; xa = xmx if big else xmn; w1, w2 = ('найбільше', 'найменше') if big else ('найменше', 'найбільше')
        wr = [(xa[0], f'названо значення x, при якому функція набуває {w1[:-1]}ого значення, а не саме значення функції'), (mn if big else mx, f'названо {w2} значення функції'),
              (V[-1][1], f'взято значення на правому кінці відрізка: f({fmt(b)})'), (V[0][1], f'взято значення на лівому кінці відрізка: f({fmt(a)})'), (mx - mn, 'знайдено різницю найбільшого й найменшого значень')]
        return T.add(lv, base(V) + f'Знайдіть {w1} значення цієї функції.', ans, wr, f'{w1} значення функції — ордината {"найвищої" if big else "найнижчої"} точки графіка (читається на осі y)',
                     f'{"найвища" if big else "найнижча"} точка графіка має координати ({fmt(xa[0])}; {fmt(ans)}), тому {w1} значення дорівнює {fmt(ans)}', img=img)
    kind = rng.choice(['diff', 'sum', 'sub', 'sub'])
    if kind == 'sub':
        opts = []
        for p in range(a, b - 2):
            for q in range(p + 3, b + 1):
                if (p, q) == (a, b): continue
                vals = [pl_val(V, p), pl_val(V, q)] + [F(y) for x, y in V if p < x < q]
                for big in (True, False):
                    v = max(vals) if big else min(vals)
                    if v != (mx if big else mn) and v.denominator == 1: opts.append((p, q, big, v, vals))
        if not opts: return False
        p, q, big, v, vals = rng.choice(opts); w1 = 'найбільше' if big else 'найменше'
        wr = [(mx if big else mn, f'знайдено {w1} значення на всій області визначення, а не на відрізку [{fmt(p)}; {fmt(q)}]'), (min(vals) if big else max(vals), f'знайдено {"найменше" if big else "найбільше"} значення на цьому відрізку'),
              (vals[0], f'взято значення на лівому кінці: f({fmt(p)})'), (vals[1], f'взято значення на правому кінці: f({fmt(q)})'), (F(q if big else p), 'названо кінець відрізка (значення x), а не значення функції')]
        return T.add(lv, base(V) + f'Знайдіть {w1} значення цієї функції на відрізку [{fmt(p)}; {fmt(q)}].', v, wr,
                     'розглядайте лише частину графіка над заданим відрізком: порівняйте значення на його кінцях і у вершинах ламаної всередині нього',
                     f'на відрізку [{fmt(p)}; {fmt(q)}] значення на кінцях {fmt(vals[0])} і {fmt(vals[1])}' + (f', у вершинах усередині: {", ".join(fmt(t) for t in vals[2:])}' if vals[2:] else '') + f'; {w1} з них {fmt(v)}', img=img)
    if kind == 'diff':
        ans = mx - mn
        wr = [(mx + mn, 'знайдено суму найбільшого й найменшого значень'), (mx, 'названо лише найбільше значення'), (b - a, 'знайдено довжину області визначення (по осі x), а не різницю значень'), (abs(xmx[0] - xmn[0]), 'знайдено відстань по осі x між точками, де досягаються найбільше й найменше значення'), (abs(mn), 'названо модуль найменшого значення')]
        return T.add(lv, base(V) + 'Знайдіть різницю між найбільшим і найменшим значеннями цієї функції.', ans, wr, 'найбільше й найменше значення читають на осі y (це ординати найвищої й найнижчої точок)',
                     f'найбільше значення {fmt(mx)}, найменше {fmt(mn)}; різниця {fmt(mx)} − {pn(mn)} = {fmt(ans)}', img=img)
    ans = mx + mn
    wr = [(mx - mn, 'знайдено різницю, а не суму'), (xmx[0] + xmn[0], 'додано абсциси точок, у яких досягаються ці значення'), (mx, 'названо лише найбільше значення'), (V[0][1] + V[-1][1], 'додано значення на кінцях області визначення'), (-(mx + mn), 'знак результату змінено')]
    return T.add(lv, base(V) + 'Знайдіть суму найбільшого й найменшого значень цієї функції.', ans, wr, 'найбільше й найменше значення — ординати найвищої й найнижчої точок графіка',
                 f'найбільше значення {fmt(mx)}, найменше {fmt(mn)}; сума {fmt(mx)} + {pn(mn)} = {fmt(ans)}', img=img)

# ---------- I3: область визначення / множина значень ----------
def f_img_pl_domain(T, rng, lv):
    V = gen_pl(rng); a, b = dom(V); ys_ = [y for _, y in V]; mx, mn = max(ys_), min(ys_)
    lc, rc = (True, True) if lv == 1 else rng.choice([(True, False), (False, True), (False, False)])
    hollow = lambda i: (i == 0 and not lc) or (i == len(V) - 1 and not rc)
    att = lambda v: any(y == v and not hollow(i) for i, (x, y) in enumerate(V))
    D = [(F(a), F(b), lc, rc)]; E = [(F(mn), F(mx), att(mn), att(mx))]
    c, ax = draw_pl(V, ends=(lc, rc)); img = c.save('t4_pld_' + S.tag(V, lc, rc))
    kind = rng.choice(['D', 'E'])
    pts = 'Зафарбована точка належить графіку, порожня — ні. ' if lv > 1 else ''
    if kind == 'D':
        ans = setstr(D)
        wr = [(setstr(E), 'названо множину значень (проміжок по осі y), а не область визначення'), (setstr(toggle(D)), 'дужки поставлено навпаки: зафарбована точка — квадратна дужка, порожня — кругла'),
              (I(a, b, True, True), 'порожню точку включено до області визначення'), (I(a, b, False, False), 'зафарбовану точку виключено з області визначення'), (I(-b, -a, rc, lc), 'знаки кінців проміжку змінено'),
              (I(min(V[0][1], V[-1][1]), max(V[0][1], V[-1][1])), 'узято ординати кінцевих точок графіка замість абсцис')]
        return T.add(lv, 'На малюнку зображено графік функції y = f(x). ' + pts + 'Укажіть область визначення цієї функції.', ans, wr,
                     'область визначення — проєкція графіка на вісь x (усі значення x, для яких є точка графіка)', f'графік розташований над проміжком осі x від {fmt(a)} до {fmt(b)}: D(f) = {ans}', img=img)
    ans = setstr(E)
    wr = [(setstr(D), 'названо область визначення (проміжок по осі x), а не множину значень'), (I(min(V[0][1], V[-1][1]), max(V[0][1], V[-1][1])), 'взято лише значення на кінцях графіка, а не найменше й найбільше значення функції'),
          (setstr(toggle(E)), 'дужки поставлено навпаки'), (I(mn, mx, True, True) if lv > 1 else I(mn, mx, False, False), 'не враховано, що значення в порожній точці функція не набуває' if lv > 1 else 'найменше й найбільше значення досягаються, тому дужки квадратні'),
          (I(-mx, -mn, E[0][3], E[0][2]), 'знаки кінців проміжку змінено')]
    return T.add(lv, 'На малюнку зображено графік функції y = f(x). ' + pts + 'Укажіть множину значень цієї функції.', ans, wr,
                 'множина значень — проєкція графіка на вісь y: від найнижчої точки до найвищої', f'найменше значення {fmt(mn)}{"" if E[0][2] else " (не досягається — точка порожня)"}, найбільше {fmt(mx)}{"" if E[0][3] else " (не досягається — точка порожня)"}: E(f) = {ans}', img=img)

# ---------- I4: проміжки монотонності ----------
def f_img_pl_mono(T, rng, lv):
    V = gen_pl(rng, nseg=(3, 5)); a, b = dom(V); segs = list(zip(V, V[1:]))
    up = [s for s in segs if s[1][1] > s[0][1]]; dn = [s for s in segs if s[1][1] < s[0][1]]
    inc = rng.random() < .5; good, bad = (up, dn) if inc else (dn, up); w1, w2 = ('зростає', 'спадає') if inc else ('спадає', 'зростає')
    c, ax = draw_pl(V); img = c.save('t4_plm_' + S.tag(V))
    kind = 'int' if lv == 1 else rng.choice(['int', 'len', 'ext'])
    if kind == 'int':
        s = rng.choice(good); i = segs.index(s); ans = I(s[0][0], s[1][0])
        inside = lambda p, q: any(g[0][0] <= p and q <= g[1][0] for g in good)
        wr = [(I(t[0][0], t[1][0]), f'на цьому проміжку функція {w2}') for t in shuffled(rng, bad)[:2]]
        if i + 1 < len(segs): wr.append((I(s[0][0], segs[i + 1][1][0]), f'на цьому проміжку функція спочатку {w1}, а потім {w2}: усередині є точка екстремуму'))
        if i > 0: wr.append((I(segs[i - 1][0][0], s[1][0]), f'на цьому проміжку функція спочатку {w2}, а потім {w1}: усередині є точка екстремуму'))
        ylo, yhi = sorted((s[0][1], s[1][1]))
        if not inside(ylo, yhi): wr.insert(1, (I(ylo, yhi), 'названо проміжок значень функції (по осі y), а не проміжок значень аргументу'))
        wr = [w for w in wr if not inside(*[F(t.replace(M, '-').replace(',', '.')) for t in w[0].strip('[]').split('; ')])]
        return T.add(lv, base(V) + f'Укажіть проміжок, на якому функція {w1}.', ans, wr, f'функція {w1}, якщо при русі зліва направо графік іде {"вгору" if inc else "вниз"}; проміжки монотонності записують значеннями x',
                     f'на відрізку {ans} графік іде {"вгору" if inc else "вниз"}: від точки ({fmt(s[0][0])}; {fmt(s[0][1])}) до точки ({fmt(s[1][0])}; {fmt(s[1][1])})', img=img)
    if kind == 'len':
        ans = sum(s[1][0] - s[0][0] for s in good)
        wr = [(sum(s[1][0] - s[0][0] for s in bad), f'знайдено сумарну довжину проміжків, на яких функція {w2}'), (b - a, 'знайдено довжину всієї області визначення'), (len(good), f'знайдено кількість проміжків, на яких функція {w1}, а не їхню довжину'),
              (sum(abs(s[1][1] - s[0][1]) for s in good), 'додано зміни значень функції (по осі y), а не довжини проміжків по осі x'), (max(s[1][0] - s[0][0] for s in good), 'знайдено довжину лише найдовшого з таких проміжків')]
        return T.add(lv, base(V) + f'Знайдіть сумарну довжину проміжків, на яких ця функція {w1}.', ans, wr, 'довжину проміжку монотонності вимірюють уздовж осі x',
                     f'функція {w1} на проміжках: {", ".join(I(s[0][0], s[1][0]) for s in good)}; сумарна довжина {" + ".join(fmt(s[1][0] - s[0][0]) for s in good)} = {fmt(ans)}', img=img)
    ext = V[1:-1]; nmax = sum(1 for i in range(1, len(V) - 1) if V[i][1] > V[i - 1][1]); nmin = len(ext) - nmax
    what = rng.choice(['max', 'min']); ans = sum(x for i, (x, y) in enumerate(V) if 0 < i < len(V) - 1 and ((y > V[i - 1][1]) == (what == 'max')))
    oth = sum(x for i, (x, y) in enumerate(V) if 0 < i < len(V) - 1 and ((y > V[i - 1][1]) != (what == 'max')))
    yv = sum(y for i, (x, y) in enumerate(V) if 0 < i < len(V) - 1 and ((y > V[i - 1][1]) == (what == 'max')))
    wr = [(oth, f'додано точки {"мінімуму" if what == "max" else "максимуму"} замість точок {"максимуму" if what == "max" else "мінімуму"}'), (yv, 'додано значення функції в цих точках (ординати), а не самі точки (абсциси)'),
          (ans + oth, 'додано всі точки екстремуму — і максимуму, і мінімуму'), (nmax if what == 'max' else nmin, 'знайдено кількість таких точок, а не їхню суму'), (ans + (b if (V[-1][1] > V[-2][1]) == (what == 'max') else a), 'до точок екстремуму зараховано кінець відрізка')]
    names = [fmt(x) for i, (x, y) in enumerate(V) if 0 < i < len(V) - 1 and ((y > V[i - 1][1]) == (what == 'max'))]
    if len(names) < 2: return False
    return T.add(lv, base(V) + f'Знайдіть суму всіх точок {"максимуму" if what == "max" else "мінімуму"} цієї функції на інтервалі ({fmt(a)}; {fmt(b)}).', ans, wr,
                 'точка максимуму (мінімуму) — це значення x, у якому зростання змінюється спаданням (спадання — зростанням); кінці відрізка точками екстремуму не є',
                 f'точки {"максимуму" if what == "max" else "мінімуму"}: x = {", ".join(names)}; сума дорівнює {fmt(ans)}', img=img)

# ---------- I5: знак функції ----------
def f_img_pl_sign(T, rng, lv):
    V = gen_pl(rng, int_zeros=True, need_zero=True); a, b = dom(V); op = rng.choice(list(OPPS))
    z = pl_solve(V, 0); crit = [a, b] + z
    def Sx(o): return pred_set(lambda x: a <= x <= b and CMP[o](pl_val(V, x)), crit)
    sol = Sx(op)
    if not sol: return False
    c, ax = draw_pl(V); img = c.save('t4_pls_' + S.tag(V))
    unb = [(None if lo == a else lo, None if hi == b else hi, lc and lo != a, rc and hi != b) for lo, hi, lc, rc in sol]
    wr = [(setstr(Sx(OPPS[op])), f'вибрано проміжки, де графік лежить {"нижче" if op in (">", ">=") else "вище"} від осі x'),
          (setstr(Sx(TOGS[op])), ('нерівність строга: нулі функції не входять до розв’язку' if op in ('>', '<') else 'нерівність нестрога: нулі функції входять до розв’язку')),
          (setstr(unb), f'не враховано, що функція визначена лише на відрізку [{fmt(a)}; {fmt(b)}]')]
    if len(sol) >= 2: wr.append((setstr(sol[:1]), 'враховано лише один із проміжків')); wr.append((setstr(sol[-1:]), 'враховано лише один із проміжків'))
    wr.append((setstr(mirror(sol)), 'знаки кінців проміжків змінено на протилежні'))
    return T.add(lv, base(V) + f'Розв’яжіть нерівність f(x) {SYM[op]} 0.', setstr(sol), wr,
                 'f(x) > 0 там, де графік лежить вище від осі x; f(x) < 0 — нижче; у нулях функції f(x) = 0',
                 f'нулі функції: x = {", ".join(fmt(t) for t in z)}; графік {"вище" if op in (">", ">=") else "нижче"} від осі x{" або на ній" if op in (">=", "<=") else ""} при x ∈ {setstr(sol)}', img=img)

# ---------- I6: кількість коренів f(x) = a ----------
def f_img_pl_roots(T, rng, lv):
    V = gen_pl(rng, nseg=(4, 5)); a, b = dom(V); ys_ = sorted(set(y for _, y in V)); mn, mx = ys_[0], ys_[-1]
    cnt = lambda t: len(pl_solve(V, t))
    c, ax = draw_pl(V); img = c.save('t4_plr_' + S.tag(V))
    if lv == 2:
        cand = [t for t in range(mn, mx + 1) if cnt(t) >= 2 and t != 0]
        if not cand: return False
        t = rng.choice(cand); k = cnt(t)
        wr = [(cnt(t + 1), f'пряму проведено на одиницю вище: y = {fmt(t + 1)}'), (cnt(t - 1), f'пряму проведено на одиницю нижче: y = {fmt(t - 1)}'), (cnt(0), 'знайдено кількість нулів функції, тобто коренів рівняння f(x) = 0'),
              (len(pl_solve(V, -t)), f'пряму проведено на рівні y = {fmt(-t)} (знак змінено)'), (k + 1, 'одну з точок перетину пораховано двічі'), (k - 1, 'одну з точок перетину пропущено')]
        return T.add(lv, base(V) + f'Скільки коренів має рівняння f(x) = {fmt(t)}?', k, wr, f'кількість коренів рівняння f(x) = a дорівнює кількості спільних точок графіка з горизонтальною прямою y = a',
                     f'пряма y = {fmt(t)} має з графіком {k} спільн{"у точку" if k == 1 else ("і точки" if k < 5 else "их точок")}: x = {", ".join(fmt(x) for x in pl_solve(V, t))}', img=img)
    ks = {k: pred_set(lambda t, k=k: cnt(t) == k, ys_) for k in range(0, 6)}
    cand = [k for k in range(2, 6) if ks[k]] or [1]
    k = rng.choice(cand); ans = setstr(ks[k])
    wr = [(setstr(ks[j]), f'при таких a рівняння має {kor(j)}, а не {k}') for j in sorted(range(1, 6), key=lambda j: abs(j - k)) if j != k and ks[j]]
    wr.insert(1, (setstr(toggle(ks[k])), 'кінці проміжків перевірено неправильно: підставте a, що дорівнює ординаті вершини ламаної, і перелічіть корені'))
    wr.append((setstr(ks[0]), 'при таких a пряма y = a не має спільних точок із графіком — коренів немає'))
    return T.add(lv, base(V) + f'Знайдіть усі значення a, при яких рівняння f(x) = a має рівно {kor(k)}.', ans, wr,
                 'рухайте горизонтальну пряму y = a знизу вгору й лічіть спільні точки з графіком; окремо перевіряйте рівні, на яких лежать вершини ламаної та її кінці',
                 f'вершини й кінці ламаної лежать на рівнях y = {", ".join(fmt(t) for t in ys_)}; рівно {kor(k)} рівняння має при a ∈ {ans}', img=img)

# ---------- I7: цілі розв’язки нерівності f(x) ? t ----------
def f_img_pl_intcount(T, rng, lv):
    V = gen_pl(rng, nseg=(4, 5)); a, b = dom(V); ys_ = [y for _, y in V]; mn, mx = min(ys_), max(ys_)
    t = rng.choice(range(mn + 1, mx)); op = rng.choice(list(OPPS)); kind = rng.choice(['cnt', 'sum'])
    xs_ = lambda o: [x for x in range(a, b + 1) if CMP[o](pl_val(V, x), t)]
    X = xs_(op)
    if len(X) < 2 or len(X) == b - a + 1: return False
    c, ax = draw_pl(V); img = c.save('t4_pli_' + S.tag(V))
    tg = 'не враховано цілі точки, у яких f(x) = ' + fmt(t) if op in ('>=', '<=') else 'зараховано також точки, у яких f(x) = ' + fmt(t) + ', хоча нерівність строга'
    if kind == 'cnt':
        ans = len(X)
        wr = [(len(xs_(TOGS[op])), tg), (len(xs_(OPPS[op])), 'пораховано цілі x, для яких виконується протилежна нерівність'), (b - a + 1, 'пораховано всі цілі числа з області визначення'), (len(pl_solve(V, t)), f'знайдено кількість коренів рівняння f(x) = {fmt(t)}'), (ans + 1, 'одне зайве число зараховано'), (ans - 1, 'одне число пропущено')]
        return T.add(lv, base(V) + f'Скільки цілих чисел x задовольняють нерівність f(x) {SYM[op]} {fmt(t)}?', ans, wr, f'проведіть пряму y = {fmt(t)} і перевірте кожне ціле x з області визначення; зверніть увагу, чи нерівність строга',
                     f'нерівність виконується для x = {", ".join(fmt(x) for x in X)} — усього {ans} чисел', img=img)
    ans = sum(X)
    wr = [(sum(xs_(TOGS[op])), tg), (sum(xs_(OPPS[op])), 'додано цілі x, для яких виконується протилежна нерівність'), (len(X), 'знайдено кількість цілих розв’язків, а не їхню суму'), (sum(range(a, b + 1)), 'додано всі цілі числа з області визначення'), (ans - X[-1], 'найбільший із цілих розв’язків пропущено'), (-ans, 'знак суми змінено')]
    return T.add(lv, base(V) + f'Знайдіть суму всіх цілих чисел x, що задовольняють нерівність f(x) {SYM[op]} {fmt(t)}.', ans, wr, f'проведіть пряму y = {fmt(t)} і перевірте кожне ціле x з області визначення; зверніть увагу, чи нерівність строга',
                 f'нерівність виконується для x = {", ".join(fmt(x) for x in X)}; сума дорівнює {fmt(ans)}', img=img)

# ---------- I8: f(f(x)) за графіком ----------
def f_img_pl_comp(T, rng, lv):
    V = gen_pl(rng); a, b = dom(V); cnt = lambda t: len(pl_solve(V, t))
    if lv == 2:
        cands = []
        for x in range(a, b + 1):
            y = pl_val(V, x)
            if y.denominator == 1 and a <= y <= b and y != x:
                z = pl_val(V, y)
                if z.denominator == 1 and z != y: cands.append((x, y, z))
        if not cands: return False
        x, y, z = rng.choice(cands)
        c, ax = draw_pl(V); img = c.save('t4_plc_' + S.tag(V))
        wr = [(y, f'знайдено лише f({fmt(x)}) — внутрішнє значення'), (y * y, f'f(f(x)) сплутано з квадратом (f(x))²'), (2 * y, 'f(f(x)) сплутано з 2·f(x)'), (pl_val(V, x) * x, 'значення функції помножено на аргумент'), (-z, 'знак результату змінено')]
        return T.add(lv, base(V) + f'Знайдіть f(f({fmt(x)})).', z, wr, 'спочатку знайдіть внутрішнє значення f(x₀), а потім значення функції в цій новій точці',
                     f'f({fmt(x)}) = {fmt(y)}; f({fmt(y)}) = {fmt(z)}', img=img)
    cands = []
    for t in range(-4, 6):
        inner = pl_solve(V, t); tot = sum(cnt(u) for u in inner)
        if inner and 2 <= tot <= 8 and tot != len(inner): cands.append((t, inner, tot))
    if not cands: return False
    t, inner, tot = rng.choice(cands)
    c, ax = draw_pl(V); img = c.save('t4_plc_' + S.tag(V))
    wr = [(len(inner), f'розв’язано лише рівняння f(t) = {fmt(t)}, а до змінної x не повернулися'), (len(inner) ** 2, 'кількість коренів зовнішнього рівняння піднесено до квадрата'), (2 * len(inner), 'кількість коренів зовнішнього рівняння подвоєно'), (tot + 1, 'один із коренів пораховано двічі'), (tot - 1, 'один із коренів пропущено')]
    return T.add(lv, base(V) + f'Скільки коренів має рівняння f(f(x)) = {fmt(t)}?', tot, wr,
                 'позначте t = f(x): спочатку розв’яжіть f(t) = c за графіком, а потім для кожного знайденого t порахуйте корені рівняння f(x) = t',
                 f'f(t) = {fmt(t)} при t = {", ".join(ffmt(u) for u in inner)}; рівняння f(x) = t мають відповідно {", ".join(str(cnt(u)) for u in inner)} коренів; разом {tot}', img=img)

# ---------- I9: пряма ----------
KS = [1, -1, 2, -2, 3, -3, F(1, 2), F(-1, 2), F(3, 2), F(-3, 2)]
def lin_s(k, b): return 'y = ' + poly([F(k), F(b)])
def draw_lines(lines, pts=(), view=(-7, 7, -6, 6), title=None, fill=None):
    c, ax = G(*view, title)
    if fill: c.poly([(ax.X(x), ax.Y(y)) for x, y in fill], fill='#dbeafe', stroke='none', w=0)
    for (k, b), col in zip(lines, (S.BLUE, S.ORANGE)): ax.curve(lambda t, k=k, b=b: float(k * t + b), view[0], view[1], col=col, w=2.6, steps=60)
    for x, y, nm, dx, dy in pts: ax.point(x, y, nm, col=S.RED, dx=dx, dy=dy)
    return c, ax
def f_img_line(T, rng, lv):
    for _ in range(300):
        k = F(rng.choice(KS)); b = rng.choice([v for v in range(-4, 5) if v]); st = k.denominator
        xs = [x for x in range(-6, 7) if x % st == 0 and x != 0 and abs(k * x + b) <= 5 and k * x + b != 0]
        if len(xs) >= 2 and xs[-1] - xs[0] >= 2: break
    else: return False
    x1, x2 = sorted(rng.sample(xs, 2)); y1, y2 = k * x1 + b, k * x2 + b
    c, ax = draw_lines([(k, b)], [(x1, y1, 'A', -16 if k > 0 else 8, -8), (x2, y2, 'B', -16 if k > 0 else 8, -8)], title='Графік лінійної функції')
    img = c.save('t4_ln_' + S.tag(k, b, x1, x2))
    intro = 'На малюнку зображено графік лінійної функції y = kx + b, що проходить через точки A і B. '
    slope = f'k = (y_B − y_A)/(x_B − x_A) = ({fmt(y2)} − {pn(y1)})/({fmt(x2)} − {pn(x1)}) = {fmt(k)}'
    kind = rng.choice(['k', 'b', 'k'] if lv == 1 else ['formula', 'zero', 'far'])
    if kind == 'k':
        wr = [(-k, f'не враховано напрям: функція {"зростає" if k > 0 else "спадає"}, тому k {">" if k > 0 else "<"} 0'), (1 / k, 'поділено приріст x на приріст y, а потрібно навпаки'), (F(b), 'названо b — ординату точки перетину з віссю y'), (y2 - y1, 'знайдено лише приріст y, не поділено на приріст x'), (F(x2 - x1), 'знайдено приріст x')]
        return T.add(lv, intro + 'Знайдіть k.', k, wr, 'кутовий коефіцієнт k = Δy/Δx — на скільки змінюється y, коли x зростає на 1', slope, img=img)
    if kind == 'b':
        wr = [(-b / k, 'названо абсцису точки перетину з віссю x (нуль функції)'), (F(-b), 'знак змінено'), (k, 'названо кутовий коефіцієнт k'), (y1, 'названо ординату точки A'), (y2, 'названо ординату точки B')]
        return T.add(lv, intro + 'Знайдіть b.', F(b), wr, 'b = f(0) — ордината точки перетину графіка з віссю y', f'графік перетинає вісь y у точці (0; {fmt(b)}), тому b = {fmt(b)}', img=img)
    if kind == 'formula':
        wr = [(lin_s(-k, b), f'знак k неправильний: функція {"зростає" if k > 0 else "спадає"}'), (lin_s(k, -b), f'знак b неправильний: графік перетинає вісь y у точці (0; {fmt(b)})'), (lin_s(-k, -b), 'обидва знаки змінено')]
        if k not in (1, -1): wr.insert(1, (lin_s(1 / k, b), 'k знайдено як Δx/Δy замість Δy/Δx'))
        if b != k: wr.append((lin_s(b, k), 'k і b переставлено місцями'))
        return T.add(lv, 'На малюнку зображено графік лінійної функції, що проходить через точки A і B. Укажіть формулу, якою задано цю функцію.', lin_s(k, b), wr, 'k = Δy/Δx, b — ордината точки перетину з віссю y', slope + f'; b = {fmt(b)}', img=img)
    if kind == 'zero':
        z = -b / k
        wr = [(b / k, 'знак змінено: з kx + b = 0 маємо x = −b/k'), (-k / b, 'дріб перевернуто'), (F(b), 'названо ординату перетину з віссю y, а не нуль функції'), (F(-b), 'не поділено на k'), (k, 'названо кутовий коефіцієнт')]
        if z.denominator == 1 and abs(z) <= 6: return False
        return T.add(lv, intro + 'Знайдіть нуль цієї функції.', z, wr, 'нуль функції — значення x, при якому y = 0; якщо точка перетину з віссю x не у вузлі сітки, знайдіть формулу і розв’яжіть рівняння', slope + f'; b = {fmt(b)}; {poly([k, F(b)])} = 0 ⇒ x = {ffmt(z)}', img=img)
    N = rng.choice([10, 12, 20, 30, 40, 50]) * rng.choice([1, -1]); ans = k * N + b
    wr = [(k * N - b, 'знак b змінено'), (k * N, 'не додано b'), (k * (N + b), 'b додано до аргументу, а не до добутку'), (-k * N + b, 'знак k змінено'), (N + b, 'не враховано коефіцієнт k')]
    return T.add(lv, intro + f'Знайдіть значення цієї функції при x = {fmt(N)}.', ans, wr, 'точки з такою абсцисою на малюнку немає: спочатку знайдіть формулу функції', slope + f'; b = {fmt(b)}; f({fmt(N)}) = {fmt(k)}·{pn(N)} + {pn(b)} = {fmt(ans)}', img=img)

# ---------- I10: площа трикутника / перетин прямих ----------
def f_img_line_area(T, rng, lv):
    if lv == 2:
        kind = rng.choice(['axes', 'two'])
        if kind == 'axes':
            p = rng.choice([v for v in range(-6, 7) if abs(v) >= 2]); q = rng.choice([v for v in range(-5, 6) if abs(v) >= 2]); k = F(-q, p)
            c, ax = draw_lines([(k, q)], [(p, 0, 'A', -4, -10 if q < 0 else 20), (0, q, 'B', 8, 4)], fill=[(0, 0), (p, 0), (0, q)]); ax.label(-.45, -.55, 'O', bold=True, size=13)
            img = c.save('t4_la_' + S.tag(p, q)); ans = F(abs(p * q), 2)
            wr = [(F(abs(p * q)), 'добуток катетів не поділено на 2'), (F(abs(p) + abs(q)), 'катети додано, а не перемножено'), (F(p * p + q * q), 'знайдено квадрат гіпотенузи AB'), (F(abs(p) + abs(q), 2), 'знайдено півсуму катетів'), (F(abs(p * q), 4), 'добуток катетів поділено на 4')]
            return T.add(lv, 'Пряма, зображена на малюнку, перетинає осі координат у точках A і B. Знайдіть площу трикутника AOB, де O — початок координат.', ans, wr,
                         'трикутник AOB прямокутний: його катети лежать на осях і дорівнюють |x_A| та |y_B|', f'OA = {abs(p)}, OB = {abs(q)}; S = {abs(p)}·{abs(q)}/2 = {fmt(ans)}', img=img)
        for _ in range(300):
            x0, y0 = rng.randint(-3, 3), rng.choice([-5, -4, -3, 3, 4, 5]); xa, xb = sorted(rng.sample(range(-6, 7), 2))
            if xa >= x0 or xb <= x0 or xb - xa < 3: continue
            k1, k2 = F(y0, x0 - xa), F(y0, x0 - xb); b1, b2 = -k1 * xa, -k2 * xb
            if b1.denominator == 1 and b2.denominator == 1 and b1 != b2 and x0 != 0: break
        else: return False
        c, ax = draw_lines([(k1, b1), (k2, b2)], [(xa, 0, 'A', -16, -8 if y0 < 0 else 18), (xb, 0, 'B', 8, -8 if y0 < 0 else 18), (x0, y0, 'C', 8, -8 if y0 > 0 else 18)], fill=[(xa, 0), (xb, 0), (x0, y0)])
        img = c.save('t4_la2_' + S.tag(x0, y0, xa, xb)); ans = F((xb - xa) * abs(y0), 2)
        wr = [(F((xb - xa) * abs(y0)), 'добуток основи на висоту не поділено на 2'), (F(abs(b1 - b2) * abs(x0), 2), 'знайдено площу трикутника, обмеженого цими прямими та віссю y'), (F(xb - xa + abs(y0)), 'основу й висоту додано'), (F((xb - xa) * abs(y0), 4), 'добуток поділено на 4'), (F((xb - xa + abs(y0)), 2), 'знайдено півсуму основи й висоти')]
        return T.add(lv, 'На малюнку зображено дві прямі, які перетинаються в точці C і перетинають вісь x у точках A і B. Знайдіть площу трикутника ABC.', ans, wr,
                     'за основу візьміть сторону AB на осі x; висота, проведена з вершини C, дорівнює |y_C|', f'AB = {fmt(xb)} − {pn(xa)} = {xb - xa}, висота |y_C| = {abs(y0)}; S = {xb - xa}·{abs(y0)}/2 = {fmt(ans)}', img=img)
    for _ in range(500):
        k1, k2 = rng.sample([-3, -2, -1, 1, 2, 3], 2); b1, b2 = rng.randint(-4, 4), rng.randint(-4, 4)
        if b1 == b2: continue
        xs = F(b2 - b1, k1 - k2); ys_ = k1 * xs + b1
        if xs.denominator == 1 or abs(xs) > 5 or abs(ys_) > 5 or abs(b1 + k1) > 5 or abs(b2 + k2) > 5: continue
        break
    else: return False
    c, ax = draw_lines([(k1, b1), (k2, b2)], [(0, b1, 'A', 8, -6), (1, b1 + k1, 'B', 8, -6), (0, b2, 'C', -18, 14), (1, b2 + k2, 'D', 8, 14)])
    img = c.save('t4_lx_' + S.tag(k1, b1, k2, b2)); kind = rng.choice(['x', 'y', 'sum'])
    eq = f'пряма AB: {lin_s(k1, b1)}; пряма CD: {lin_s(k2, b2)}; {poly([F(k1), F(b1)])} = {poly([F(k2), F(b2)])} ⇒ x = {ffmt(xs)}, y = {ffmt(ys_)}'
    trap = 'точка перетину не лежить у вузлі сітки, тому її координати треба обчислити: складіть рівняння обох прямих і прирівняйте праві частини'
    if kind == 'x':
        wr = [(-xs, 'знак змінено під час перенесення доданків'), (ys_, 'названо ординату точки перетину'), (F(round(xs)) if round(xs) != xs else xs + 1, 'координату прочитано з малюнка наближено, без обчислень'), (F(b2 - b1, k1 + k2) if k1 + k2 else F(b1 + b2, k1 - k2), 'коефіцієнти при x додано, а не віднято')]
        return T.add(lv, 'На малюнку зображено прямі AB і CD. Знайдіть абсцису точки їх перетину.', xs, wr, trap, eq, img=img)
    if kind == 'y':
        wr = [(-ys_, 'знак змінено'), (xs, 'названо абсцису точки перетину'), (F(round(ys_)) if round(ys_) != ys_ else ys_ + 1, 'координату прочитано з малюнка наближено, без обчислень'), (k2 * xs + b1, 'абсцису підставлено в рівняння з переплутаними коефіцієнтами')]
        return T.add(lv, 'На малюнку зображено прямі AB і CD. Знайдіть ординату точки їх перетину.', ys_, wr, trap, eq, img=img)
    ans = xs + ys_
    wr = [(xs - ys_, 'знайдено різницю координат'), (xs, 'названо лише абсцису'), (ys_, 'названо лише ординату'), (-ans, 'знак змінено'), (F(round(xs) + round(ys_)) if F(round(xs) + round(ys_)) != ans else ans + 1, 'координати прочитано з малюнка наближено')]
    return T.add(lv, 'На малюнку зображено прямі AB і CD, що перетинаються в точці (x₀; y₀). Знайдіть x₀ + y₀.', ans, wr, trap, eq + f'; x₀ + y₀ = {ffmt(ans)}', img=img)

# ---------- I11: парабола — формула ----------
def par_s(a, m, n):
    A = {1: '', -1: M}.get(a, fmt(a)); core = 'x²' if m == 0 else f'(x {M if m > 0 else "+"} {abs(m)})²'
    return 'y = ' + A + core + (f' {"+" if n > 0 else M} {abs(n)}' if n else '')
def draw_par(a, m, n, pts=(), title='Графік квадратичної функції', view=None):
    if view is None:
        xmin, xmax = min(m - 4, -1), max(m + 4, 1)
        ymin, ymax = (min(n - 1, -1), max(n + 8, 1)) if a > 0 else (min(n - 8, -1), max(n + 1, 1))
        view = (xmin, xmax, ymin, ymax)
    c, ax = G(*view, title)
    ax.curve(lambda t: float(a) * (t - m) ** 2 + n, view[0], view[1], col=S.BLUE, w=2.8, steps=400)
    for x, y, nm, dx, dy in pts: ax.point(x, y, nm, col=S.RED, dx=dx, dy=dy)
    return c, ax
def f_img_parab_formula(T, rng, lv):
    a = F(rng.choice([1, -1, 2, -2, F(1, 2), F(-1, 2)])); m = rng.choice([-3, -2, -1, 1, 2, 3]); n = rng.choice([v for v in range(-4, 5) if v and v != m])
    dx = 2 if a.denominator == 2 else 1; px, py = m + dx, n + a * dx * dx
    c, ax = draw_par(a, m, n, [(m, n, 'A', 8, 16 if a > 0 else -8), (px, py, 'B', 8, 4)]); img = c.save('t4_pf_' + S.tag(a, m, n))
    b, cc = -2 * a * m, a * m * m + n
    chk = f'вершина A({fmt(m)}; {fmt(n)}) ⇒ y = a(x {M if m > 0 else "+"} {abs(m)})² {"+" if n > 0 else M} {abs(n)}; точка B({fmt(px)}; {fmt(py)}): a·{dx * dx} {"+" if n > 0 else M} {abs(n)} = {fmt(py)} ⇒ a = {fmt(a)}'
    if lv == 2:
        wr = [(par_s(a, -m, n), f'знак у дужках неправильний: вершина має абсцису {fmt(m)}, тому в дужках x {M if m > 0 else "+"} {abs(m)}'), (par_s(a, m, -n), f'знак вільного доданка неправильний: ордината вершини {fmt(n)}'),
              (par_s(-a, m, n), f'гілки параболи напрямлені {"вгору" if a > 0 else "вниз"}, тому a {">" if a > 0 else "<"} 0'), (par_s(a, n, m), 'координати вершини переставлено місцями')]
        if abs(a) != 1: wr.insert(2, (par_s(a / abs(a), m, n), f'не враховано розтяг: на відстані {dx} від осі симетрії значення відрізняється від ординати вершини на {fmt(abs(a) * dx * dx)}, а не на {dx * dx}'))
        return T.add(lv, 'На малюнку зображено параболу з вершиною в точці A, що проходить через точку B. Укажіть формулу, якою задано цю функцію.', par_s(a, m, n), wr,
                     'парабола з вершиною (m; n) має рівняння y = a(x − m)² + n; коефіцієнт a знаходять за ще однією точкою', chk, img=img)
    kind = rng.choice(['b', 'c', 'D', 'far'])
    intro = 'На малюнку зображено графік функції y = ax² + bx + c; позначено вершину параболи A та ще одну точку графіка B. '
    full = chk + f'; y = {poly([a, b, cc])}'
    if kind == 'b':
        wr = [(-b, 'знак: абсциса вершини x₀ = −b/(2a), тому b = −2a·x₀'), (F(m), 'названо абсцису вершини'), (F(-2 * m), 'не враховано коефіцієнт a'), (cc, 'знайдено коефіцієнт c'), (-a * m, 'у формулі x₀ = −b/(2a) пропущено множник 2')]
        return T.add(lv, intro + 'Знайдіть b.', b, wr, 'абсциса вершини x₀ = −b/(2a); спочатку за точками A і B знайдіть a', full + f'; b = {fmt(b)}', img=img)
    if kind == 'c':
        wr = [(F(n), 'названо ординату вершини, а не ординату точки перетину з віссю y'), (a * m * m - n, 'знак ординати вершини змінено'), (F(m * m + n), 'не враховано коефіцієнт a'), (-cc, 'знак змінено'), (b, 'знайдено коефіцієнт b')]
        return T.add(lv, intro + 'Знайдіть c.', cc, wr, 'c = f(0); якщо точки перетину з віссю y на малюнку не видно або її важко прочитати, знайдіть формулу функції', full + f'; c = f(0) = {fmt(cc)}', img=img)
    if kind == 'D':
        D = b * b - 4 * a * cc
        wr = [(-D, 'знак змінено'), (b * b + 4 * a * cc, 'у формулі D = b² − 4ac узято знак «плюс»'), (b * b - a * cc, 'пропущено множник 4'), (b * b, 'обчислено лише b²'), (F(n), 'названо ординату вершини')]
        return T.add(lv, intro + 'Знайдіть дискримінант квадратного тричлена ax² + bx + c.', D, wr, 'спочатку відновіть формулу за вершиною та ще однією точкою, потім D = b² − 4ac', full + f'; D = {pn(b)}² − 4·{pn(a)}·{pn(cc)} = {fmt(D)}', img=img)
    t = rng.choice([8, 10, 12, 20]) * rng.choice([1, -1]); ans = a * t * t + n
    wr = [(F(t * t + n), 'не враховано коефіцієнт a'), (a * abs(t) + n, 'відстань до осі симетрії не піднесено до квадрата'), (a * (m + t) ** 2 + n, 'не враховано зсув вершини: у дужках має бути x − x₀'), (a * t * t - n, 'знак ординати вершини змінено'), (a * t * t, 'не додано ординату вершини')]
    if abs(a) == 1: wr = wr[1:]
    return T.add(lv, intro + f'Знайдіть значення цієї функції при x = {fmt(m + t)}.', ans, wr, 'точки з такою абсцисою на малюнку немає: відновіть формулу y = a(x − x₀)² + y₀', chk + f'; f({fmt(m + t)}) = {fmt(a)}·{pn(t)}² {"+" if n > 0 else M} {abs(n)} = {fmt(ans)}', img=img)

# ---------- I12: знаки коефіцієнтів параболи ----------
def f_img_parab_signs(T, rng, lv):
    for _ in range(300):
        a = F(rng.choice([1, -1, F(1, 2), F(-1, 2)])); m = rng.choice([-3, -2, -1, 1, 2, 3]); n = rng.choice([v for v in range(-4, 5) if v])
        b, cc = -2 * a * m, a * m * m + n; D = b * b - 4 * a * cc
        if cc != 0 and abs(cc) <= 5 and D != 0: break
    else: return False
    c, ax = draw_par(a, m, n, view=(-7, 7, -6, 6)); img = c.save('t4_ps_' + S.tag(a, m, n))
    names = ['a', 'b', 'c'] if lv == 2 else rng.choice([['b', 'c', 'D'], ['a', 'c', 'D'], ['a', 'b', 'D']])
    val = {'a': a, 'b': b, 'c': cc, 'D': D}
    why = {'a': f'гілки параболи напрямлені {"вгору" if a > 0 else "вниз"}, тому a {">" if a > 0 else "<"} 0',
           'b': f'вершина лежить {"праворуч" if m > 0 else "ліворуч"} від осі y: x₀ = −b/(2a) {">" if m > 0 else "<"} 0, тому a і b мають {"різні" if m > 0 else "однакові"} знаки і b {">" if b > 0 else "<"} 0',
           'c': f'c = f(0): графік перетинає вісь y {"вище" if cc > 0 else "нижче"} від початку координат, тому c {">" if cc > 0 else "<"} 0',
           'D': f'парабола {"перетинає вісь x у двох точках" if D > 0 else "не має спільних точок з віссю x"}, тому D {">" if D > 0 else "<"} 0'}
    st = lambda flip: ', '.join(f'{nm} {">" if (val[nm] > 0) != (nm in flip) else "<"} 0' for nm in names)
    wr = [(st([nm]), why[nm]) for nm in names] + [(st(names[1:]), why[names[1]] + '; ' + why[names[2]]), (st(names[:2]), why[names[0]] + '; ' + why[names[1]])]
    rng.shuffle(wr)
    return T.add(lv, f'На малюнку зображено графік функції y = ax² + bx + c{" (D — дискримінант тричлена ax² + bx + c)" if "D" in names else ""}. Укажіть правильне твердження.', st([]), wr,
                 'a — напрям гілок; c = f(0) — точка перетину з віссю y; знак b визначають за положенням вершини x₀ = −b/(2a); знак D — за кількістю точок перетину з віссю x', '; '.join(why[nm] for nm in names), img=img)

# ---------- I13: властивості параболи ----------
def f_img_parab_props(T, rng, lv):
    a = F(rng.choice([1, -1, 2, -2, F(1, 2), F(-1, 2)])); m = rng.choice([-3, -2, -1, 1, 2, 3]); n = rng.choice([v for v in range(-4, 5) if v and v != m and v != -m])
    c, ax = draw_par(a, m, n, [(m, n, None, 0, 0)]); img = c.save('t4_pp_' + S.tag(a, m, n))
    up = a > 0; intro = 'На малюнку зображено графік квадратичної функції y = f(x); позначено вершину параболи. '
    kind = rng.choice(['range', 'axis', 'vertex'] if lv == 1 else ['inc', 'dec', 'two', 'none'])
    if kind == 'range':
        ans = I(n, None) if up else I(None, n, False, True)
        wr = [(I(None, n, False, True) if up else I(n, None), f'гілки напрямлені {"вгору" if up else "вниз"}, тому ордината вершини — {"найменше" if up else "найбільше"} значення'), (I(m, None) if up else I(None, m, False, True), 'узято абсцису вершини замість ординати'),
              (I(n, None, False) if up else I(None, n, False, False), 'значення у вершині досягається, тому дужка квадратна'), ('(−∞; +∞)', 'це область визначення; множина значень обмежена ординатою вершини'), (I(-n, None) if up else I(None, -n, False, True), 'знак ординати вершини змінено')]
        return T.add(lv, intro + 'Укажіть множину значень цієї функції.', ans, wr, 'множину значень читають на осі y: для параболи вона обмежена ординатою вершини', f'вершина ({fmt(m)}; {fmt(n)}), гілки {"вгору" if up else "вниз"}: E(f) = {ans}', img=img)
    if kind == 'axis':
        ans = f'x = {fmt(m)}'
        wr = [(f'x = {fmt(n)}', 'узято ординату вершини замість абсциси'), (f'y = {fmt(n)}', 'це горизонтальна пряма через вершину; вісь симетрії параболи вертикальна'), (f'x = {fmt(-m)}', 'знак абсциси вершини змінено'), (f'y = {fmt(m)}', 'вісь симетрії вертикальна, її рівняння має вигляд x = x₀')]
        return T.add(lv, intro + 'Укажіть рівняння осі симетрії параболи.', ans, wr, 'вісь симетрії параболи — вертикальна пряма x = x₀, що проходить через вершину', f'абсциса вершини x₀ = {fmt(m)}, тому вісь симетрії x = {fmt(m)}', img=img)
    if kind == 'vertex':
        pr = lambda u, v: f'({fmt(u)}; {fmt(v)})'
        wr = [(pr(n, m), 'координати переставлено: спочатку записують абсцису, потім ординату'), (pr(-m, n), 'знак абсциси змінено'), (pr(m, -n), 'знак ординати змінено'), (pr(-m, -n), 'обидва знаки змінено')]
        return T.add(lv, intro + 'Укажіть координати вершини.', pr(m, n), wr, 'координати точки записують у порядку (x; y)', f'вершина розташована в точці з абсцисою {fmt(m)} та ординатою {fmt(n)}', img=img)
    if kind in ('inc', 'dec'):
        right = (kind == 'inc') == up
        ans = I(m, None) if right else I(None, m, False, True)
        sub_ = lambda v: (v >= m) if right else (v <= m)   # чи є промінь із кінцем v частиною правильного проміжку
        wr = [(I(None, m, False, True) if right else I(m, None), f'на цьому проміжку функція {"спадає" if kind == "inc" else "зростає"}')]
        if not sub_(n): wr.append((I(n, None) if right else I(None, n, False, True), 'узято ординату вершини; проміжки монотонності записують значеннями x'))
        wr.append((I(None, n, False, True) if right else I(n, None), 'узято ординату вершини та ще й протилежний напрям'))
        if not sub_(-m): wr.append((I(-m, None) if right else I(None, -m, False, True), 'знак абсциси вершини змінено'))
        wr.append(('(−∞; +∞)', 'квадратична функція не є монотонною на всій числовій прямій'))
        wr.append((I(None, -m, False, True) if right else I(-m, None), 'знак абсциси вершини змінено й напрям обрано протилежний'))
        return T.add(lv, intro + f'Укажіть проміжок {"зростання" if kind == "inc" else "спадання"} цієї функції.', ans, wr, 'монотонність змінюється у вершині; проміжки записують значеннями x (абсциса вершини)',
                     f'гілки {"вгору" if up else "вниз"}, вершина при x = {fmt(m)}: функція {"зростає" if kind == "inc" else "спадає"} на {ans}', img=img)
    two = kind == 'two'
    S2 = I(n, None, False) if up else I(None, n, False, False); S0 = I(None, n, False, False) if up else I(n, None, False)
    ans = S2 if two else S0
    wr = [(S0 if two else S2, f'при таких t рівняння {"не має коренів" if two else "має два корені"}'), (I(n, None) if (up == two) else I(None, n, False, True), f'при t = {fmt(n)} рівняння має рівно один корінь (вершина), тому дужка кругла'),
          ('{' + fmt(n) + '}', 'при такому t корінь рівно один'), (I(None, m, False, False) if (up == two) else I(m, None, False), 'узято абсцису вершини замість ординати й протилежний напрям')]
    rgt = up == two
    if not ((m >= n) if rgt else (m <= n)): wr.insert(2, (I(m, None, False) if rgt else I(None, m, False, False), 'узято абсцису вершини замість ординати'))
    if not ((-n >= n) if rgt else (-n <= n)): wr.append((I(-n, None, False) if rgt else I(None, -n, False, False), 'знак ординати вершини змінено'))
    return T.add(lv, intro + f'При яких значеннях t рівняння f(x) = t {"має два різні корені" if two else "не має коренів"}?', ans, wr, 'корені рівняння f(x) = t — спільні точки параболи з горизонтальною прямою y = t',
                 f'пряма y = t {"перетинає параболу у двох точках" if two else "не має спільних точок із параболою"}, коли вона проходить {"вище" if (up == two) else "нижче"} від вершини: t {">" if (up == two) else "<"} {fmt(n)}', img=img)

IMG_A = [(f_img_pl_value, [1]), (f_img_pl_extreme, [1, 2]), (f_img_pl_domain, [1, 2]), (f_img_pl_mono, [1, 2]), (f_img_pl_sign, [2]), (f_img_pl_roots, [2, 3]), (f_img_pl_intcount, [3]), (f_img_pl_comp, [2, 3]),
         (f_img_line, [1, 2]), (f_img_line_area, [2, 3]), (f_img_parab_formula, [2, 3]), (f_img_parab_signs, [2, 3]), (f_img_parab_props, [1, 2])]
FAMS = IMG_A
