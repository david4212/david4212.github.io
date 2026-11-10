import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mgen import *
import msvg as S
import math, itertools
from fractions import Fraction as F

T = Topic(4, 'funktsiyi')
M = MINUS

# ---------- допоміжне ----------
def pn(v): return f'({fmt(v)})' if F(v) < 0 else fmt(v)
def ev(co, x):
    r = F(0)
    for c in co: r = r * F(x) + c
    return r
def ys(*c): return 'y = ' + poly(list(c))
def pim(x):
    x = F(x)
    if x == 0: return '0'
    sg = M if x < 0 else ''; x = abs(x)
    if x.denominator == 1: return sg + ('π' if x == 1 else f'{x.numerator}π')
    return sg + ('π' if x.numerator == 1 else f'{x.numerator}π') + f'/{x.denominator}'
def lcmF(a, b):
    a, b = F(a), F(b)
    return F(math.lcm(a.numerator, b.numerator), math.gcd(a.denominator, b.denominator))

def setstr(parts):
    if not parts: return 'порожня множина'
    out = []
    for lo, hi, lc, rc in parts:
        if lo is not None and lo == hi: out.append('{' + fmt(lo) + '}'); continue
        ls = '(−∞' if lo is None else ('[' if lc else '(') + fmt(lo)
        rs_ = '+∞)' if hi is None else fmt(hi) + (']' if rc else ')')
        out.append(f'{ls}; {rs_}')
    return ' ∪ '.join(out)
def toggle(parts):
    return [(lo, hi, (not lc) if lo is not None else lc, (not rc) if hi is not None else rc) for lo, hi, lc, rc in parts]
def mirror(parts):
    return [(None if hi is None else -hi, None if lo is None else -lo, rc, lc) for lo, hi, lc, rc in reversed(parts)]
def complement(parts):
    parts = sorted(parts, key=lambda p: (-10**9 if p[0] is None else p[0]))
    res = []; cur_lo, cur_lc = None, False
    for lo, hi, lc, rc in parts:
        if lo is not None: res.append((cur_lo, lo, cur_lc, not lc))
        if hi is None: return res
        cur_lo, cur_lc = hi, not rc
    res.append((cur_lo, None, cur_lc, False))
    return res

def pred_set(pred, crit):
    """множина {x: pred(x)} через критичні точки; pred працює з Fraction."""
    crit = sorted(set(F(c) for c in crit))
    smp = [crit[0] - 1] + [(a + b) / 2 for a, b in zip(crit, crit[1:])] + [crit[-1] + 1]
    seq = []
    for i, s in enumerate(smp):
        seq.append(('R', i, bool(pred(s))))
        if i < len(crit): seq.append(('C', i, bool(pred(crit[i]))))
    parts = []; i = 0
    while i < len(seq):
        if not seq[i][2]: i += 1; continue
        j = i
        while j + 1 < len(seq) and seq[j + 1][2]: j += 1
        a, b = seq[i], seq[j]
        if a[0] == 'R': lo = None if a[1] == 0 else crit[a[1] - 1]; lc = False
        else: lo = crit[a[1]]; lc = True
        if b[0] == 'R': hi = None if b[1] == len(smp) - 1 else crit[b[1]]; rc = False
        else: hi = crit[b[1]]; rc = True
        parts.append((lo, hi, lc, rc)); i = j + 1
    return parts
def has_pt(parts, x):
    x = F(x)
    for lo, hi, lc, rc in parts:
        if lo is not None and (x < lo or (x == lo and not lc)): continue
        if hi is not None and (x > hi or (x == hi and not rc)): continue
        return True
    return False

def vname(i): return 'abcdefgh'[i]

# ---------- таблиця тригонометричних значень ----------
SINT = {0: '0', 30: '1/2', 45: '√2/2', 60: '√3/2', 90: '1'}
COST = {0: '1', 30: '√3/2', 45: '√2/2', 60: '1/2', 90: '0'}
TANT = {0: '0', 30: '√3/3', 45: '1', 60: '√3'}
CTGT = {30: '√3', 45: '1', 60: '√3/3', 90: '0'}
def trig_exact(fn, deg):
    t = deg % 360
    if t <= 90: ref, q = t, 1
    elif t <= 180: ref, q = 180 - t, 2
    elif t <= 270: ref, q = t - 180, 3
    else: ref, q = 360 - t, 4
    pos = {'sin': q in (1, 2), 'cos': q in (1, 4), 'tg': q in (1, 3), 'ctg': q in (1, 3)}[fn]
    tab = {'sin': SINT, 'cos': COST, 'tg': TANT, 'ctg': CTGT}[fn]
    v = tab[ref]
    return v if (pos or v == '0') else M + v, ref, q
def degs(d): return f'{d}°'
POOL = ['1/2', '√3/2', '√2/2', '1', '√3/3', '√3']

# ================= L1 =================
def expand2(r1, r2): return [1, -(r1 + r2), r1 * r2]
SUBL = {2: '₂', 3: '₃', 5: '₅', 10: '₁₀', 4: '₄'}
def sg(v): return '+' if v >= 0 else M

def f_value(T, rng, lv):
    kind = rng.choice(['quad', 'quad', 'cube', 'lin'])
    x0 = rng.choice([-4, -3, -2, -1, 2, 3, 4])
    if kind == 'quad':
        a = rng.choice([-3, -2, -1, 1, 2, 3]); b = rng.choice([v for v in range(-6, 7) if v]); c = rng.choice([v for v in range(-9, 10) if v]); co = [a, b, c]
    elif kind == 'cube':
        a = rng.choice([-2, -1, 1, 2]); b = rng.choice([-3, -1, 2, 4]); c = rng.choice([v for v in range(-5, 6) if v]); co = [a, 0, b, c]
    else:
        a = rng.choice([-5, -3, -2, 2, 3, 4]); b = rng.choice([v for v in range(-8, 9) if v]); co = [a, b]
    ans = ev(co, x0)
    wr = [(ev(co, -x0), f'підставлено x = {fmt(-x0)} замість x = {fmt(x0)}')]
    if kind == 'quad':
        if x0 < 0: wr.append((-a * x0 * x0 + b * x0 + c, f'({fmt(x0)})² обчислено як {M}{x0 * x0} (мінус не піднесено до квадрата)'))
        else: wr.append((a * x0 * x0 - b * x0 + c, f'знак доданка {fmt(b)}x змінено на протилежний'))
        wr.append((a * x0 + b * x0 + c, 'x² замінено на x'))
        wr.append((ans - c, 'вільний член не додано'))
        calc = f'{fmt(a)}·{pn(x0)}² {sg(b)} {fmt(abs(b))}·{pn(x0)} {sg(c)} {fmt(abs(c))} = {fmt(a * x0 * x0)} {sg(b * x0)} {fmt(abs(b * x0))} {sg(c)} {fmt(abs(c))}'
    elif kind == 'cube':
        wr.append((a * x0 * x0 + b * x0 + c, 'x³ замінено на x²'))
        wr.append((a * x0 ** 3 - b * x0 + c, f'знак доданка {fmt(b)}x змінено на протилежний'))
        wr.append((ans - c, 'вільний член не додано'))
        calc = f'{fmt(a)}·{pn(x0)}³ {sg(b)} {fmt(abs(b))}·{pn(x0)} {sg(c)} {fmt(abs(c))} = {fmt(a * x0 ** 3)} {sg(b * x0)} {fmt(abs(b * x0))} {sg(c)} {fmt(abs(c))}'
    else:
        wr.append((a * x0 - b, 'вільний член додано з протилежним знаком'))
        wr.append((a + x0 + b, 'добуток a·x замінено сумою'))
        wr.append((b - a * x0, 'знак добутку a·x змінено на протилежний'))
        calc = f'{fmt(a)}·{pn(x0)} {sg(b)} {fmt(abs(b))} = {fmt(a * x0)} {sg(b)} {fmt(abs(b))}'
    return T.add(lv, f'Нехай f(x) = {poly(co)}. Знайдіть f({fmt(x0)}).', ans, wr,
                 'при підстановці від’ємного числа беріть його в дужки: непарні степені зберігають мінус, парні дають плюс', f'f({fmt(x0)}) = {calc} = {fmt(ans)}')

def f_domain_basic(T, rng, lv):
    kind = rng.choice(['frac', 'frac2', 'sqrt', 'log', 'sqrt', 'log'])
    G = lambda *p: setstr(list(p))
    if kind == 'frac':
        a = rng.choice([v for v in range(-8, 9) if v]); p = rng.randint(2, 5); q = rng.choice([v for v in range(-6, 7) if v])
        txt = f'y = ({poly([p, q])})/({poly([1, -a])})'
        sol = [(None, F(a), False, False), (F(a), None, False, False)]
        z = F(-q, p)
        wr = [(G((None, F(-a), False, False), (F(-a), None, False, False)), f'нуль знаменника знайдено як x = {fmt(-a)} замість x = {fmt(a)} (знак переплутано)'),
              (G((None, z, False, False), (z, None, False, False)) if z != a else G((F(a), None, False, False)), 'виключено нуль чисельника, а не знаменника' if z != a else 'враховано лише праву частину числової осі'),
              (G((None, None, False, False)), 'вважали, що дріб визначений при всіх x'),
              (G((F(a), None, True, False)), 'враховано лише промінь праворуч від нуля знаменника, до того ж разом із самою точкою')]
        sl = f'знаменник не дорівнює нулю: {poly([1, -a])} ≠ 0, тобто x ≠ {fmt(a)}'
        trap = 'у знаменнику не може бути нуля; нуль чисельника область визначення не обмежує'
    elif kind == 'frac2':
        c = rng.randint(2, 7); p = rng.randint(1, 4)
        txt = f'y = {p}/({poly([1, 0, -c * c])})'
        sol = [(None, F(-c), False, False), (F(-c), F(c), False, False), (F(c), None, False, False)]
        wr = [(G((None, F(c), False, False), (F(c), None, False, False)), f'виключено лише x = {c}, а корінь x = {M}{c} втрачено'),
              (G((F(-c), F(c), False, False)), 'записано проміжок між коренями замість їх виключення'),
              (G((None, F(-c), False, True), (F(c), None, True, False)), f'розглянуто нерівність x² − {c * c} ≥ 0 замість умови x² − {c * c} ≠ 0'),
              (G((None, None, False, False)), 'вважали, що знаменник ніколи не дорівнює нулю')]
        sl = f'x² − {c * c} ≠ 0 ⇒ x ≠ ±{c}'
        trap = 'рівняння x² = c² має два корені, і обидва треба виключити'
    elif kind == 'sqrt':
        k = rng.choice([-4, -3, -2, 2, 3, 4, 5]); b = rng.choice([v for v in range(-12, 13) if v])
        txt = f'y = √({poly([k, b])})'
        r = F(-b, k)
        sol = [(r, None, True, False)] if k > 0 else [(None, r, False, True)]
        wr = [(G((r, None, False, False)) if k > 0 else G((None, r, False, False)), 'підкореневий вираз може дорівнювати нулю, тому кінець проміжку входить (дужка квадратна)'),
              (G((None, r, False, True)) if k > 0 else G((r, None, True, False)), 'взято промінь у протилежний бік' if k > 0 else 'при діленні на від’ємний коефіцієнт знак нерівності не змінили'),
              (G((-r, None, True, False)) if k > 0 else G((None, -r, False, True)), f'нуль виразу знайдено як {fmt(-r)} замість {fmt(r)} (знак b переплутано)'),
              (G((None, None, False, False)), 'вважали, що корінь визначений при всіх x')]
        sl = f'{poly([k, b])} ≥ 0 ⇒ x {"≥" if k > 0 else "≤"} {fmt(r)}' + ('' if k > 0 else ' (при діленні на від’ємне число знак нерівності змінюється)')
        trap = 'підкореневий вираз ≥ 0 (нуль дозволений); ділення на від’ємний коефіцієнт змінює знак нерівності'
    else:
        k = rng.choice([-3, -2, 2, 3, 4, 5]); b = rng.choice([v for v in range(-12, 13) if v]); base = rng.choice([2, 3, 5, 10])
        txt = f'y = log{SUBL[base]}({poly([k, b])})'
        r = F(-b, k)
        sol = [(r, None, False, False)] if k > 0 else [(None, r, False, False)]
        wr = [(G((r, None, True, False)) if k > 0 else G((None, r, False, True)), 'аргумент логарифма має бути строго додатним, тому кінець не входить (дужка кругла)'),
              (G((None, r, False, False)) if k > 0 else G((r, None, False, False)), 'взято промінь у протилежний бік' if k > 0 else 'при діленні на від’ємний коефіцієнт знак нерівності не змінили'),
              (G((-r, None, False, False)) if k > 0 else G((None, -r, False, False)), f'нуль аргументу знайдено як {fmt(-r)} замість {fmt(r)} (знак b переплутано)'),
              (G((None, None, False, False)), 'вважали, що логарифм визначений при всіх x')]
        sl = f'{poly([k, b])} > 0 ⇒ x {">" if k > 0 else "<"} {fmt(r)}' + ('' if k > 0 else ' (при діленні на від’ємне число знак змінюється)')
        trap = 'аргумент логарифма строго більший за нуль (нуль не дозволений)'
    return T.add(lv, f'Знайдіть область визначення функції {txt}.', setstr(sol), wr, trap, sl)

def f_zero(T, rng, lv):
    kind = rng.choice(['lin', 'quad_sum', 'quad_big', 'quad_prod', 'frac'])
    if kind == 'lin':
        k = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5]); b = rng.choice([v for v in range(-15, 16) if v and v % k])
        ans = F(-b, k)
        wr = [(F(b, k), 'не змінено знак при перенесенні вільного члена'), (F(-k, b), 'частку перевернуто (−k/b замість −b/k)'), (F(-b), 'забули поділити на k'), (F(b), 'нулем названо вільний член')]
        return T.add(lv, f'Знайдіть нуль функції {ys(k, b)}.', ans, wr, 'нуль функції — це значення x, при якому y = 0 (а не значення y при x = 0)', f'{poly([k, b])} = 0 ⇒ x = {ffmt(ans)}')
    if kind == 'frac':
        r1, r2 = rng.sample([v for v in range(-7, 8) if v], 2)
        co = expand2(r1, r2)
        txt = f'y = ({poly(co)})/({poly([1, -r2])})'
        ans = F(r1)
        wr = [(F(r2), 'підставлено нуль знаменника (при ньому функція не визначена)'), (F(r1 + r2), 'додано обидва корені чисельника'), (F(-r1), 'знак кореня переплутано')]
        return T.add(lv, f'Знайдіть нуль функції {txt}.', ans, wr, 'нуль знаменника — не нуль функції: у цій точці функція не існує', f'чисельник: {poly(co)} = 0 ⇒ x = {fmt(r1)} або x = {fmt(r2)}; x = {fmt(r2)} — нуль знаменника, тому не підходить; залишається x = {fmt(r1)}')
    r1, r2 = rng.sample([v for v in range(-8, 9) if v], 2)
    co = expand2(r1, r2); txt = ys(*co)
    if kind == 'quad_sum':
        ans = F(r1 + r2); wr = [(F(r1 * r2), 'знайдено добуток нулів, а не суму'), (F(-(r1 + r2)), 'суму нулів взято з протилежним знаком'), (F(r1), 'враховано лише один нуль'), (F(abs(r1 - r2)), 'знайдено різницю нулів')]
        return T.add(lv, f'Знайдіть суму нулів функції {txt}.', ans, wr, 'сума коренів x² + bx + c дорівнює −b', f'нулі {fmt(r1)} і {fmt(r2)}, сума {fmt(r1 + r2)}')
    if kind == 'quad_prod':
        ans = F(r1 * r2); wr = [(F(r1 + r2), 'знайдено суму нулів, а не добуток'), (F(-r1 * r2), 'знак добутку змінено'), (F(co[1] + co[2]), 'додано коефіцієнти b і c'), (F(r1 + r2 + r1 * r2), 'додано суму та добуток')]
        return T.add(lv, f'Знайдіть добуток нулів функції {txt}.', ans, wr, 'добуток коренів x² + bx + c дорівнює c', f'нулі {fmt(r1)} і {fmt(r2)}, добуток {fmt(r1 * r2)}')
    ans = F(max(r1, r2)); wr = [(F(min(r1, r2)), 'названо менший нуль замість більшого'), (F(-max(r1, r2)), 'знак кореня переплутано'), (F(r1 + r2), 'знайдено суму нулів'), (F(r1 * r2), 'знайдено добуток нулів')]
    return T.add(lv, f'Знайдіть найбільший нуль функції {txt}.', ans, wr, 'розв’язавши рівняння, виберіть саме більший із двох коренів', f'{poly(co)} = 0 ⇒ x = {fmt(r1)} або x = {fmt(r2)}; більший — {fmt(max(r1, r2))}')

def f_through_point(T, rng, lv):
    k = rng.choice([-4, -3, -2, -1, 2, 3, 4, 5]); b = rng.choice([v for v in range(-9, 10) if v])
    x0 = rng.choice([-3, -2, -1, 1, 2, 3, 4]); y0 = k * x0 + b
    if rng.random() < .5:
        ans = F(b); txt = f'Графік функції y = {poly([k, 0])} + b проходить через точку A({fmt(x0)}; {fmt(y0)}). Знайдіть b.'.replace(' + b', ' + b')
        txt = f'Графік функції y = {fmt(k) if k not in (1, -1) else ("" if k == 1 else M)}x + b проходить через точку A({fmt(x0)}; {fmt(y0)}). Знайдіть b.'
        wr = [(F(y0 + k * x0), 'добуток kx додано до y замість віднімання'), (F(y0), 'за b взято ординату точки'), (F(y0 - k), 'у добутку замість x підставлено 1'), (F(-b), 'знак b змінено на протилежний')]
        sol = f'{fmt(y0)} = {fmt(k)}·{pn(x0)} + b ⇒ b = {fmt(y0)} − {pn(k * x0)} = {fmt(b)}'
        return T.add(lv, txt, ans, wr, 'підставляйте координати точки в рівняння: x = абсциса, y = ордината', sol)
    ans = F(k)
    txt = f'Графік функції y = kx {sg(b)} {fmt(abs(b))} проходить через точку A({fmt(x0)}; {fmt(y0)}). Знайдіть k.'
    wr = [(F(y0 + b, x0) * -1 if False else F(y0 + b, x0), 'вільний член додано до y замість віднімання'), (F(y0, x0), 'не враховано вільний член'), (F(x0, y0 - b) if y0 - b else F(0), 'частку перевернуто (x/(y − b) замість (y − b)/x)'), (F(-k), 'знак k змінено на протилежний')]
    sol = f'{fmt(y0)} = k·{pn(x0)} {sg(b)} {fmt(abs(b))} ⇒ k = ({fmt(y0)} − {pn(b)})/{pn(x0)} = {fmt(k)}'
    return T.add(lv, txt, ans, wr, 'підставляйте координати точки в рівняння: x = абсциса, y = ордината', sol)

def f_vertex(T, rng, lv):
    a = rng.choice([-3, -2, -1, 1, 2, 3, 4]); m = rng.choice([v for v in range(-5, 6)]); n_ = rng.randint(-8, 8)
    b = -2 * a * m; c = a * m * m + n_; co = [a, b, c]
    if lv == 1:
        if b == 0: return False
        ans = F(m)
        wr = [(F(b, 2 * a), 'забули знак мінус у формулі x₀ = −b/(2a)'), (F(-b, a), 'забули подвоїти a у знаменнику'), (F(-b, 2 * c) if c else F(2), 'у знаменнику взято c замість a')]
        wr.append((F(c, a) if a else 1, 'абсцису вершини ототожнено з відношенням c/a'))
        return T.add(1, f'Знайдіть абсцису вершини параболи {ys(*co)}.', ans, wr, 'x₀ = −b/(2a): мінус і подвоєне a легко загубити', f'x₀ = −({fmt(b)})/(2·{pn(a)}) = {fmt(m)}')
    kind = rng.choice(['point', 'min'])
    if kind == 'point':
        ans = f'({fmt(m)}; {fmt(n_)})'
        wr = [(f'({fmt(n_)}; {fmt(m)})', 'координати вершини записано в оберненому порядку'), (f'({fmt(m)}; {fmt(c)})', 'за ординату взято вільний член c (це ордината точки перетину з Oy)'), (f'({fmt(-m)}; {fmt(n_)})', 'знак абсциси вершини переплутано'), (f'({fmt(m)}; {fmt(-n_)})', 'знак ординати вершини змінено')]
        if m == 0 or n_ == 0 or m == n_: return False
        return T.add(lv, f'Знайдіть координати вершини параболи {ys(*co)}.', ans, wr, 'ордината вершини — це y(x₀), а не c', f'x₀ = −{pn(b)}/(2·{pn(a)}) = {fmt(m)}; y₀ = {fmt(a)}·{pn(m)}² {sg(b)} {fmt(abs(b))}·{pn(m)} {sg(c)} {fmt(abs(c))} = {fmt(n_)}')
    ans = F(n_)
    wr = [(F(c), 'узято значення при x = 0'), (F(m), 'названо абсцису вершини'), (F(c - n_) if c != n_ else F(c + 1), 'від c віднімали замість обчислення значення y(x₀)'), (F(-n_), 'знак змінено')]
    word = 'найменше' if a > 0 else 'найбільше'
    return T.add(lv, f'Знайдіть {word} значення функції {ys(*co)}.', ans, wr, f'{word} значення квадратичної функції досягається у вершині; воно дорівнює y(x₀), а не x₀', f'a {">" if a>0 else "<"} 0, тому {word} значення — у вершині: x₀ = {fmt(m)}, y₀ = {fmt(n_)}')

def f_ap_basic(T, rng, lv):
    a1 = rng.randint(-12, 15); d = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 7]); n_ = rng.randint(6, 20)
    ans = a1 + (n_ - 1) * d
    wr = [(a1 + n_ * d, f'використано a₁ + n·d замість a₁ + (n − 1)·d'), (a1 + (n_ - 2) * d, 'кількість кроків прогресії взято на 1 менше'), (a1 * d if False else n_ * d, 'за формулою взято лише n·d'), (a1 + (n_ - 1) + d, 'добуток (n − 1)·d замінено сумою')]
    return T.add(lv, f'В арифметичній прогресії a₁ = {fmt(a1)}, d = {fmt(d)}. Знайдіть a{"".join("₀₁₂₃₄₅₆₇₈₉"[int(ch)] for ch in str(n_))}.', ans, wr, 'до першого члена додають (n − 1) різниць, а не n', f'a_{n_} = a₁ + {n_ - 1}·d = {fmt(a1)} + {n_ - 1}·{pn(d)} = {fmt(ans)}')

def sub(n_): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(ch)] for ch in str(n_))

def f_ap_d(T, rng, lv):
    d = rng.choice([-6, -4, -3, -2, 2, 3, 4, 5, 7]); a1 = rng.randint(-10, 20)
    if lv == 1 or rng.random() < .5:
        p = rng.randint(1, 3); q = p + rng.randint(2, 5)
        ap, aq = a1 + (p - 1) * d, a1 + (q - 1) * d
        ans = F(d)
        wr = [(F(aq - ap), 'різницю членів не поділено на різницю їх номерів'), (F(aq - ap, q + p), 'у знаменнику додано номери замість віднімання'), (F(ap - aq, q - p), 'члени віднято в оберненому порядку'), (F(aq - ap, q - p + 1), 'у знаменнику взято на 1 більше, ніж різницю номерів')]
        return T.add(lv, f'В арифметичній прогресії a{sub(p)} = {fmt(ap)}, a{sub(q)} = {fmt(aq)}. Знайдіть різницю прогресії d.', ans, wr, 'a_q − a_p = (q − p)·d: ділити треба на різницю номерів', f'd = (a_{q} − a_{p})/({q} − {p}) = ({fmt(aq)} − {pn(ap)})/{q - p} = {fmt(d)}')
    seq = [a1 + i * d for i in range(4)]
    ans = F(d)
    wr = [(F(-d), 'різницю знайдено як a₁ − a₂'), (F(seq[1]), 'за d взято другий член'), (F(seq[3] - seq[0]), 'за d взято різницю першого й четвертого членів'), (F(seq[1] + seq[0]), 'знайдено суму двох перших членів')]
    return T.add(lv, f'Знайдіть різницю арифметичної прогресії {fmt(seq[0])}; {fmt(seq[1])}; {fmt(seq[2])}; {fmt(seq[3])}; …', ans, wr, 'різниця d = a₂ − a₁ (наступний мінус попередній)', f'd = {fmt(seq[1])} − {pn(seq[0])} = {fmt(d)}')

def f_gp_basic(T, rng, lv):
    b1 = rng.choice([1, 2, 3, 4, 5, -1, -2, -3]); q = rng.choice([2, 3, -2, -3, F(1, 2), F(-1, 2)]); n_ = rng.randint(3, 7)
    if isinstance(q, F) and b1 % 2: b1 *= 2 ** (n_ - 1)
    ans = F(b1) * F(q) ** (n_ - 1)
    qq = F(q)
    wr = [(F(b1) * qq ** n_, 'використано b₁·qⁿ замість b₁·qⁿ⁻¹'), (F(b1) * qq * (n_ - 1), 'степінь замінено множенням: b₁·q·(n − 1)'), (F(b1) + (n_ - 1) * qq, 'прогресію сплутано з арифметичною: b₁ + (n − 1)·q'), (F(b1) * qq ** (n_ - 2), 'показник степеня взято на 1 менший')]
    return T.add(lv, f'У геометричній прогресії b₁ = {fmt(b1)}, q = {ffmt(qq)}. Знайдіть b{sub(n_)}.', ans, wr, 'b_n = b₁·q^(n−1): показник на 1 менший за номер, а q підноситься до степеня, а не множиться', f'b_{n_} = {fmt(b1)}·({ffmt(qq)})^{n_ - 1} = {ffmt(ans)}')

def f_gp_q(T, rng, lv):
    q = rng.choice([2, 3, -2, -3, 4, F(1, 2), F(1, 3), -5]); b1 = rng.choice([1, 2, 3, 6, -1, -2, 5])
    if isinstance(q, F): b1 *= q.denominator ** 3
    seq = [F(b1) * F(q) ** i for i in range(4)]
    ans = F(q)
    wr = [(seq[1] - seq[0], 'знайдено різницю, а не частку (прогресію сплутано з арифметичною)'), (seq[0] / seq[1], 'частку перевернуто (b₁/b₂ замість b₂/b₁)'), (-F(q), 'знак частки змінено на протилежний'), (seq[2] / seq[0], 'знайдено b₃/b₁ = q² замість q')]
    if lv == 1: pass
    return T.add(lv, f'Знайдіть знаменник геометричної прогресії {ffmt(seq[0])}; {ffmt(seq[1])}; {ffmt(seq[2])}; {ffmt(seq[3])}; …', ans, wr, 'знаменник q = b₂ : b₁ (частка), а не різниця', f'q = {ffmt(seq[1])} : {pn_f(seq[0])} = {ffmt(q)}')
def pn_f(v): return f'({ffmt(v)})' if F(v) < 0 else ffmt(v)

def f_ap_sum(T, rng, lv):
    a1 = rng.randint(-10, 12); d = rng.choice([-4, -3, -2, 2, 3, 4, 5]); n_ = rng.choice([8, 10, 12, 15, 20, 9, 11])
    ans = n_ * (2 * a1 + (n_ - 1) * d) // 2
    an = a1 + (n_ - 1) * d
    wr = [(n_ * (a1 + an), 'суму не поділено на 2'), (n_ * (2 * a1 + n_ * d) // 2 if n_ * (2 * a1 + n_ * d) % 2 == 0 else n_ * (2 * a1 + n_ * d), 'у формулі суми взято n·d замість (n − 1)·d'), ((a1 + an) // 2 if (a1 + an) % 2 == 0 else (a1 + an), 'не помножено на кількість членів n'), (n_ * (a1 + an) // 2 + d, 'до правильної суми додано зайвий доданок d')]
    return T.add(lv, f'Знайдіть суму перших {n_} членів арифметичної прогресії, якщо a₁ = {fmt(a1)}, d = {fmt(d)}.', ans, wr, 'S_n = (a₁ + a_n)/2 · n або S_n = (2a₁ + (n − 1)d)/2 · n', f'a_{n_} = {fmt(an)}; S_{n_} = ({fmt(a1)} {sg(an)} {fmt(abs(an))})/2·{n_} = {fmt(ans)}')

def f_parity(T, rng, lv):
    FUN = [('x³ + x', lambda x: x**3 + x), ('x⁴ − x²', lambda x: x**4 - x**2), ('x² + x', lambda x: x*x + x), ('x³ − 2x', lambda x: x**3 - 2*x), ('x⁴ + 3', lambda x: x**4 + 3), ('x³ + 1', lambda x: x**3 + 1), ('|x| + x²', lambda x: abs(x) + x*x),
           ('x·|x|', lambda x: x*abs(x)), ('x⁶ − 5x²', lambda x: x**6 - 5*x*x), ('5x⁵ − x³', lambda x: 5*x**5 - x**3), ('x² − 3x', lambda x: x*x - 3*x), ('x⁴ + x³', lambda x: x**4 + x**3), ('2x − x³', lambda x: 2*x - x**3), ('x⁸ − |x|', lambda x: x**8 - abs(x))]
    kind = rng.choice(['poly', 'poly', 'trig'])
    if kind == 'trig':
        FUN = [('sin x', lambda x: math.sin(x)), ('cos x', lambda x: math.cos(x)), ('x·sin x', lambda x: x * math.sin(x)), ('x·cos x', lambda x: x * math.cos(x)), ('sin x + cos x', lambda x: math.sin(x) + math.cos(x)), ('x² + cos x', lambda x: x * x + math.cos(x)), ('tg x', lambda x: math.tan(x)),
               ('x³·sin x', lambda x: x**3 * math.sin(x)), ('sin x·cos x', lambda x: math.sin(x) * math.cos(x)), ('x + sin x', lambda x: x + math.sin(x)), ('sin 2x', lambda x: math.sin(2 * x)), ('1 + cos x', lambda x: 1 + math.cos(x)), ('x − cos x', lambda x: x - math.cos(x))]
    name, f = rng.choice(FUN)
    pts = [0.7, 1.3, 2.1, 0.45]
    ev_ = all(abs(f(x) - f(-x)) < 1e-9 for x in pts); od_ = all(abs(f(x) + f(-x)) < 1e-9 for x in pts)
    ans = 'парна' if ev_ else ('непарна' if od_ else 'ні парна, ні непарна')
    opts = {'парна': 'парна', 'непарна': 'непарна', 'ні парна, ні непарна': 'ні парна, ні непарна', 'і парна, і непарна': 'і парна, і непарна'}
    why = {'парна': ('f(−x) = −f(x): знак змінюється, а для парності потрібно f(−x) = f(x)' if od_ else 'рівність f(−x) = f(x) виконується не для всіх x'),
           'непарна': ('f(−x) = f(x): значення не змінює знак, а для непарності потрібно f(−x) = −f(x)' if ev_ else 'рівність f(−x) = −f(x) виконується не для всіх x'),
           'ні парна, ні непарна': ('функція має симетрію (f(−x) = f(x) або f(−x) = −f(x)), тому вона парна чи непарна'),
           'і парна, і непарна': 'це можливо лише для f(x) ≡ 0; тут функція не нульова'}
    wr = [(o, why[o]) for o in opts if o != ans]
    note = ''
    if kind == 'poly': note = 'підставте −x: парні степені не змінюються, непарні міняють знак'
    else: note = 'sin x і tg x — непарні, cos x — парна; добуток двох функцій однакової парності — парна, різної — непарна; сума парної й непарної (ненульових) не має парності'
    return T.add(lv, f'Яке з тверджень правильне для функції f(x) = {name}?', 'функція ' + ans, [('функція ' + w, r) for w, r in wr], note,
                 {'парна': f'f(−x) = f(x) для всіх x з області визначення, отже, функція парна', 'непарна': 'f(−x) = −f(x), отже, функція непарна', 'ні парна, ні непарна': 'ані f(−x) = f(x), ані f(−x) = −f(x) не виконується, отже, функція ні парна, ні непарна'}[ans])

def f_period(T, rng, lv):
    fn = rng.choice(['sin', 'cos', 'tg', 'ctg']); k = rng.choice([2, 3, 4, 5, 6, F(1, 2), F(1, 3), F(2, 3), F(3, 2), 8])
    base = F(2) if fn in ('sin', 'cos') else F(1)
    ans = base / F(k)
    arg = f'{ffmt(k)}x' if not isinstance(k, F) or k.denominator == 1 else (f'x/{k.denominator}' if k.numerator == 1 else f'{k.numerator}x/{k.denominator}')
    if lv >= 2 and rng.random() < .5:
        m = rng.randint(1, 6); arg2 = arg + f' {"+" if True else ""} {m}' if False else None
    wr = [(base * F(k), f'період множили на {ffmt(k)}, а треба ділити'), (base, f'коефіцієнт {ffmt(k)} при x не врахували'), ((F(1) if base == 2 else F(2)) / F(k), 'взято період іншої тригонометричної функції (π замість 2π або навпаки)'), (base / F(k) / 2, 'період зайвий раз поділено на 2'), (base * 2 / F(k), 'період подвоєно'), (F(1) / F(k) if base == 2 else F(2) / F(k), 'період іншої функції поділено на коефіцієнт')]
    wr = [(pim(v), r) for v, r in wr]
    t = f'{fn}({arg})'.replace('tg', 'tg')
    return T.add(lv, f'Знайдіть найменший додатний період функції y = {t}.', pim(ans), wr, 'T = 2π/|k| для sin і cos та π/|k| для tg і ctg: коефіцієнт стоїть у знаменнику', f'T = {"2π" if base == 2 else "π"}/{pn_f(k) if F(k).denominator == 1 else "(" + ffmt(k) + ")"} = {pim(ans)}')

def f_trig_value(T, rng, lv):
    fn = rng.choice(['sin', 'cos', 'tg', 'ctg'])
    angs = [30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330] if fn in ('sin', 'cos', 'tg', 'ctg') else []
    deg = rng.choice(angs)
    ans, ref, q = trig_exact(fn, deg)
    tab = {'sin': SINT, 'cos': COST, 'tg': TANT, 'ctg': CTGT}
    co = {'sin': 'cos', 'cos': 'sin', 'tg': 'ctg', 'ctg': 'tg'}[fn]
    wr = []
    pos = not ans.startswith(M)
    wr.append((M + ans if pos else ans[1:], f'знак у {["I","II","III","IV"][q-1]} чверті визначено неправильно'))
    cof, _, _ = trig_exact(co, deg); cofv = cof.replace(M, '')
    if cofv != ans.replace(M, ''): wr.append(((M if not pos else '') + cofv if False else (cofv if pos else M + cofv), f'використано значення {co} замість {fn} (кофункцію)'))
    for v in POOL:
        if v != ans.replace(M, '') and len(wr) < 4 and not any(v == w[0].replace(M, '') for w in wr): wr.append((v if pos else M + v, 'це табличне значення, але для іншого кута (кут приведення визначено неправильно)')); 
    fname = {'tg': 'tg', 'ctg': 'ctg'}.get(fn, fn)
    sol = f'{deg}° — {["I","II","III","IV"][q-1]} чверть, кут приведення {ref}°; {fn} {ref}° = {tab[fn][ref]}; у цій чверті {fn} {"додатний" if pos else "від’ємний"}, отже {ans}'
    return T.add(lv, f'Обчисліть {fname} {deg}°.', ans, wr, 'спочатку кут приведення й таблична величина, потім знак за чвертю (sin: + у I, II; cos: + у I, IV; tg, ctg: + у I, III)', sol)

def f_monotone_basic(T, rng, lv):
    items = [('y = −3x + 1', 'спадна'), ('y = 4x − 7', 'зростаюча'), ('y = 2ˣ', 'зростаюча'), ('y = (1/3)ˣ', 'спадна'), ('y = log₂ x', 'зростаюча'), ('y = log₀,₅ x', 'спадна'), ('y = x³', 'зростаюча'), ('y = −x³', 'спадна'), ('y = x²', 'не є монотонною'), ('y = 5 − 2x', 'спадна'), ('y = 3ˣ − 4', 'зростаюча'), ('y = (0,2)ˣ', 'спадна'),
             ('y = log₃ x', 'зростаюча'), ('y = log₁/₃ x', 'спадна'), ('y = x⁴', 'не є монотонною'), ('y = |x|', 'не є монотонною'), ('y = (2/3)ˣ', 'спадна'), ('y = (√2)ˣ', 'зростаюча'), ('y = (π/4)ˣ', 'спадна'), ('y = 1 − 3ˣ', 'спадна'), ('y = 2 − (1/2)ˣ', 'зростаюча')]
    txt, ans = rng.choice(items)
    why = {'зростаюча': {'спадна': 'напрям зміни визначено хибно: не враховано, що основа більша за 1 (або коефіцієнт додатний) — функція зростає', 'не є монотонною': 'функція зберігає напрям зміни на всій області визначення', 'стала': 'значення функції змінюються зі зміною x'},
           'спадна': {'зростаюча': 'не враховано, що основа менша за 1 (або коефіцієнт від’ємний) — функція спадає', 'не є монотонною': 'функція зберігає напрям зміни на всій області визначення', 'стала': 'значення функції змінюються зі зміною x'},
           'не є монотонною': {'зростаюча': 'функція змінює напрям: на одній частині області визначення спадає, на іншій зростає', 'спадна': 'функція змінює напрям: на одній частині області визначення спадає, на іншій зростає', 'стала': 'значення функції змінюються зі зміною x'}}[ans]
    wr = [(k, v) for k, v in why.items()]
    return T.add(lv, f'Яка з характеристик правильна для функції {txt} на її області визначення?', ans, wr, 'для a^x і log_a x: a > 1 — зростає, 0 < a < 1 — спадає; для kx + b: знак k', {'зростаюча': 'більшому x відповідає більше значення функції', 'спадна': 'більшому x відповідає менше значення функції', 'не є монотонною': 'функція не зберігає напрям: наприклад, значення при x і −x однакові'}[ans])

def f_range_basic(T, rng, lv):
    c = rng.choice([v for v in range(-7, 8) if v]); kind = rng.choice(['sq', 'nsq', 'abs', 'sqrt', 'exp', 'nexp', 'sin', 'lin'])
    cs = f' {"+" if c > 0 else M} {abs(c)}'; C = fmt(c); G = lambda *p: setstr(list(p))
    if kind == 'sq':
        txt = f'y = x²{cs}'; sol = [(F(c), None, True, False)]
        wr_ = [(G((F(c), None, False, False)), f'значення {C} досягається при x = 0, тому біля {C} дужка квадратна'), (G((None, F(c), False, True)), f'гілки параболи напрямлені вгору, значення не менші за {C}'), (G((F(-c), None, True, False)), f'число {C} взято з протилежним знаком'), (G((None, None, False, False)), 'парабола не набуває всіх дійсних значень')]
        sl = f'x² ≥ 0, тому y ≥ {C}; найменше значення {C} при x = 0'
    elif kind == 'nsq':
        txt = f'y = −x²{cs}'; sol = [(None, F(c), False, True)]
        wr_ = [(G((None, F(c), False, False)), f'значення {C} досягається при x = 0, тому біля {C} дужка квадратна'), (G((F(c), None, True, False)), f'гілки параболи напрямлені вниз, значення не більші за {C}'), (G((None, F(-c), False, True)), f'число {C} взято з протилежним знаком'), (G((None, None, False, False)), 'парабола не набуває всіх дійсних значень')]
        sl = f'−x² ≤ 0, тому y ≤ {C}; найбільше значення {C} при x = 0'
    elif kind == 'abs':
        txt = f'y = |x|{cs}'; sol = [(F(c), None, True, False)]
        wr_ = [(G((F(c), None, False, False)), f'значення {C} досягається при x = 0'), (G((F(0), None, True, False)), f'не враховано зсув на {C}: найменше значення модуля 0 стає {C}'), (G((None, F(c), False, True)), f'модуль невід’ємний, тому значення не менші за {C}'), (G((F(-c), None, True, False)), f'число {C} взято з протилежним знаком')]
        sl = f'|x| ≥ 0, тому y ≥ {C}; значення {C} досягається при x = 0'
    elif kind == 'sqrt':
        txt = f'y = √x{cs}'; sol = [(F(c), None, True, False)]
        wr_ = [(G((F(c), None, False, False)), f'значення {C} досягається при x = 0'), (G((F(0), None, True, False)), f'не враховано зсув на {C}'), (G((None, F(c), False, True)), f'√x ≥ 0, тому значення не менші за {C}'), (G((F(-c), None, True, False)), f'число {C} взято з протилежним знаком')]
        sl = f'√x ≥ 0, тому y ≥ {C}; значення {C} досягається при x = 0'
    elif kind == 'exp':
        base = rng.choice([2, 3, 5]); txt = f'y = {base}ˣ{cs}'; sol = [(F(c), None, False, False)]
        wr_ = [(G((F(c), None, True, False)), f'показникова функція ніколи не дорівнює 0, тож значення {C} не досягається (дужка кругла)'), (G((F(0), None, False, False)), f'не враховано зсув на {C}'), (G((None, None, False, False)), 'показникова функція набуває лише додатних значень, тому область значень не вся числова пряма'), (G((F(-c), None, False, False)), f'число {C} взято з протилежним знаком')]
        sl = f'{base}ˣ > 0, тому y > {C}; значення {C} не досягається'
    elif kind == 'nexp':
        base = rng.choice([2, 3, 5])
        txt = f'y = {c} − {base}ˣ' if c > 0 else f'y = {M}{base}ˣ − {abs(c)}'; sol = [(None, F(c), False, False)]
        wr_ = [(G((None, F(c), False, True)), f'aˣ > 0, тому значення {C} не досягається (дужка кругла)'), (G((F(c), None, False, False)), f'перед показниковою функцією стоїть мінус: значення менші за {C}'), (G((None, None, False, False)), 'область значень не вся числова пряма'), (G((None, F(-c), False, False)), f'число {C} взято з протилежним знаком')]
        sl = f'{base}ˣ > 0, тому −{base}ˣ < 0 і y < {C}; значення {C} не досягається'
    elif kind == 'sin':
        k = rng.choice([2, 3, 4, 5]); txt = f'y = {k}sin x{cs}'; sol = [(F(c - k), F(c + k), True, True)]
        wr_ = [(G((F(-k), F(k), True, True)), f'не враховано зсув на {C}'), (G((F(c - 1), F(c + 1), True, True)), f'не враховано множник {k} перед синусом'), (G((F(c - k), F(c + k), False, False)), 'межі значень досягаються, тому дужки квадратні'), (G((F(c), F(c + k), True, True)), 'враховано лише додатні значення синуса')]
        sl = f'−1 ≤ sin x ≤ 1 ⇒ −{k} ≤ {k}sin x ≤ {k} ⇒ {fmt(c - k)} ≤ y ≤ {fmt(c + k)}'
    else:
        k = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5]); txt = f'y = {k}x{cs}'; sol = [(None, None, False, False)]
        wr_ = [(G((F(c), None, True, False)), 'лінійна функція набуває будь-яких значень'), (G((None, F(c), False, True)), 'лінійна функція набуває будь-яких значень'), (G((F(c), F(c), True, True)), 'значення функції залежить від x'), ('(−∞; 0) ∪ (0; +∞)', 'нуль теж є значенням функції (при x = ' + ffmt(F(-c, k)) + ')')]
        sl = 'лінійна функція з k ≠ 0 набуває всіх дійсних значень'
    return T.add(lv, f'Знайдіть область значень функції {txt}.', setstr(sol), wr_, 'область значень — множина всіх y; перевірте, чи досягається межа', sl)

def f_inverse_val(T, rng, lv):
    k = rng.choice([-4, -3, -2, 2, 3, 4, 5]); b = rng.choice([v for v in range(-9, 10) if v]); x0 = rng.choice([v for v in range(-4, 6) if v])
    y0 = k * x0 + b
    ans = F(x0)
    wr = [(F(k * y0 + b), f'обчислено f({fmt(y0)}) замість розв’язування рівняння f(x) = {fmt(y0)}'), (F(y0 + b, k), 'вільний член додано замість віднімання'), (F(k, y0 - b) if y0 != b else F(k), 'частку перевернуто'), (F(-x0), 'знак результату змінено')]
    return T.add(lv, f'Нехай f(x) = {poly([k, b])}. Знайдіть f⁻¹({fmt(y0)}), де f⁻¹ — функція, обернена до f.', ans, wr, 'f⁻¹(a) — це такий x, що f(x) = a (а не f(a))', f'{poly([k, b])} = {fmt(y0)} ⇒ x = ({fmt(y0)} − {pn(b)})/{pn(k)} = {fmt(x0)}')

def f_transform_text(T, rng, lv):
    p = rng.randint(1, 6); q = rng.randint(1, 6)
    sx = rng.choice([1, -1]); sy = rng.choice([1, -1])
    inner = f'x {"−" if sx > 0 else "+"} {p}'
    ex = f'y = f({inner})' + (f' {"+" if sy > 0 else "−"} {q}')
    def txt(hx, vy):
        return f'паралельне перенесення на {p} {"вправо" if hx > 0 else "вліво"} і на {q} {"вгору" if vy > 0 else "вниз"}'
    ans = txt(sx, sy)
    wr = [(txt(-sx, sy), 'напрям горизонтального зсуву визначено навпаки (f(x − p) зсуває вправо, f(x + p) — вліво)'), (txt(sx, -sy), 'напрям вертикального зсуву визначено навпаки (+q — вгору, −q — вниз)'), (txt(-sx, -sy), 'обидва напрями зсуву визначено навпаки')]
    return T.add(lv, f'Як із графіка функції y = f(x) отримати графік функції {ex}?', ans, wr, 'зсув за x «працює навпаки»: x − p — вправо, x + p — вліво; зсув за y — «як є»', f'x {"−" if sx > 0 else "+"} {p} — {"вправо" if sx > 0 else "вліво"} на {p}; {"+" if sy > 0 else "−"}{q} — {"вгору" if sy > 0 else "вниз"} на {q}')

def f_hyperbola(T, rng, lv):
    k = rng.choice([-9, -6, -4, -3, -2, 2, 3, 4, 5, 8, 12]); form = rng.choice(['k/x', 'k/x', 'sh'])
    q1 = 'у I і III координатних чвертях'; q2 = 'у II і IV координатних чвертях'
    ans = q1 if k > 0 else q2
    wr = [(q2 if k > 0 else q1, 'знак k у гіперболи y = k/x переплутано: при k > 0 гілки в I і III чвертях' if k > 0 else 'знак k переплутано: при k < 0 гілки у II і IV чвертях'), ('у I і II координатних чвертях', 'гілки гіперболи розташовані в протилежних чвертях (кутах), а не в сусідніх'), ('у III і IV координатних чвертях', 'гілки гіперболи розташовані в протилежних чвертях (кутах), а не в сусідніх')]
    wr.append(('в усіх чвертях' if False else 'лише в I чверті', 'гіперболу сплутано з однією гілкою (наприклад, з y = √x)'))
    return T.add(lv, f'У яких координатних чвертях розташований графік функції y = {fmt(k)}/x?', ans, wr, 'знак k визначає чверті: k > 0 — I і III, k < 0 — II і IV', f'k = {fmt(k)} {">" if k > 0 else "<"} 0, тому гіпербола розташована {ans}')

def f_slope(T, rng, lv):
    x1 = rng.randint(-4, 3); x2 = x1 + rng.randint(1, 5); k = rng.choice([-3, -2, -1, 2, 3, F(1, 2), F(-1, 2), F(3, 2)])
    dx = x2 - x1
    if isinstance(k, F) and dx % k.denominator: x2 = x1 + k.denominator * rng.randint(1, 2); dx = x2 - x1
    y1 = rng.randint(-6, 6); y2 = y1 + F(k) * dx
    ans = F(k)
    dy = y2 - y1
    wr = [(F(dx) / dy if dy else F(0), 'відношення змін координат перевернуто (Δx/Δy замість Δy/Δx)'), (-F(k), 'різниці координат узято з різним порядком (знак змінено)'), ((y2 + y1) / (x2 + x1) if x2 + x1 else F(5), 'координати додано замість віднімання'), (dy, 'різницю ординат не поділено на різницю абсцис')]
    return T.add(lv, f'Знайдіть кутовий коефіцієнт прямої, що проходить через точки A({fmt(x1)}; {fmt(y1)}) та B({fmt(x2)}; {fmt(y2)}).', ans, wr, 'k = (y₂ − y₁)/(x₂ − x₁): різниці беруть в одному порядку', f'k = ({fmt(y2)} − {pn(y1)})/({fmt(x2)} − {pn(x1)}) = {ffmt(dy)}/{dx}' + ('' if F(dy, dx) == F(dy) / dx and ffmt(dy) + '/' + str(dx) == ffmt(ans) else f' = {ffmt(ans)}'))

def f_parallel_perp(T, rng, lv):
    k = rng.choice([-4, -3, -2, 2, 3, 4, 5, F(1, 2), F(-1, 2), F(2, 3), F(-3, 4)]); b = rng.choice([v for v in range(-8, 9) if v])
    kind = rng.choice(['par', 'perp'])
    kk = F(k)
    expr = f'y = {ffmt(kk) if abs(kk) != 1 else ""}x {sg(b)} {abs(b)}' if kk.denominator == 1 else f'y = {"−" if kk < 0 else ""}{abs(kk.numerator)}x/{kk.denominator} {sg(b)} {abs(b)}'
    if kind == 'par':
        ans = kk
        wr = [(-1 / kk, 'це кутовий коефіцієнт перпендикулярної прямої'), (-kk, 'знак кутового коефіцієнта змінено'), (F(b), 'за кутовий коефіцієнт взято вільний член')]
        return T.add(lv, f'Пряма паралельна прямій {expr}. Який кутовий коефіцієнт має ця пряма?', ans, wr, 'паралельні прямі мають однакові кутові коефіцієнти', f'паралельні прямі мають рівні кутові коефіцієнти: k = {ffmt(kk)}')
    ans = -1 / kk
    wr = [(kk, 'це кутовий коефіцієнт паралельної прямої'), (-kk, 'змінено лише знак (треба й перевернути)'), (1 / kk, 'перевернуто, але знак не змінено')]
    return T.add(lv, f'Пряма перпендикулярна до прямої {expr}. Який кутовий коефіцієнт має ця пряма?', ans, wr, 'для перпендикулярних прямих k₁·k₂ = −1: потрібно і змінити знак, і перевернути', f'k₁·k₂ = −1 ⇒ k₂ = −1/({ffmt(kk)}) = {ffmt(ans)}')

def f_axes_int(T, rng, lv):
    k = rng.choice([-4, -3, -2, 2, 3, 4, 5]); b = rng.choice([v for v in range(-12, 13) if v and v % k == 0])
    xi = F(-b, k)
    kind = rng.choice(['ox', 'oy', 'sum'])
    if kind == 'ox':
        ans = xi; wr = [(F(b, k), 'не змінено знак при перенесенні вільного члена'), (F(b), 'за абсцису взято вільний член'), (F(-b), 'забули поділити на k'), (F(-k, b), 'частку перевернуто')]
        return T.add(lv, f'Знайдіть абсцису точки перетину графіка функції {ys(k, b)} з віссю Ox.', ans, wr, 'на осі Ox y = 0', f'{poly([k, b])} = 0 ⇒ x = {fmt(xi)}')
    if kind == 'oy':
        ans = F(b); wr = [(xi, 'знайдено перетин з віссю Ox (там y = 0)'), (F(k), 'за ординату взято кутовий коефіцієнт'), (F(-b), 'знак змінено'), (F(k + b), 'додано k і b')]
        return T.add(lv, f'Знайдіть ординату точки перетину графіка функції {ys(k, b)} з віссю Oy.', ans, wr, 'на осі Oy x = 0, тому y = b', f'x = 0 ⇒ y = {fmt(b)}')
    ans = xi + b; wr = [(xi - b, 'ординату точки перетину з Oy взято з протилежним знаком'), (xi * b, 'знайдено добуток замість суми'), (F(b), 'враховано лише точку на осі Oy'), (xi, 'враховано лише точку на осі Ox')]
    return T.add(lv, f'Графік функції {ys(k, b)} перетинає осі координат у точках A (на осі Ox) і B (на осі Oy). Знайдіть суму абсциси точки A та ординати точки B.', ans, wr, 'A(−b/k; 0), B(0; b): складають абсцису A і ординату B', f'A({fmt(xi)}; 0), B(0; {fmt(b)}); {fmt(xi)} {sg(b)} {fmt(abs(b))} = {fmt(ans)}')

def f_compare_simple(T, rng, lv):
    kind = rng.choice(['pow', 'pow', 'log'])
    if kind == 'pow':
        base = rng.choice([2, 3, 5, F(1, 2), F(1, 3), F(2, 3), F(3, 2), F(1, 5)]); p, q = rng.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
        up = base > 1; hi = p > q
        gt = (hi == up)
        sym = '>' if gt else '<'
        txt = f'Порівняйте числа ({ffmt(base)})^{p} і ({ffmt(base)})^{q}. Укажіть правильну відповідь: ({ffmt(base)})^{p} … ({ffmt(base)})^{q}.'.replace('^-', '^−')
        ans = sym; other = '<' if gt else '>'
        wr = [(other, 'не враховано, що показникова функція ' + ('зростає' if up else 'спадає') + f' (основа {ffmt(base)} ' + ('більша' if up else 'менша') + ' за 1)'), ('=', 'показники різні, а показникова функція монотонна — значення різні'), ('порівняти неможливо', 'порівняти можна, адже основа однакова й функція монотонна')]
        sl = f'основа {ffmt(base)} {">" if up else "<"} 1, функція {"зростає" if up else "спадає"}; {p} {">" if hi else "<"} {q}, тому ({ffmt(base)})^{p} {sym} ({ffmt(base)})^{q}'.replace('^-', '^−')
        return T.add(lv, txt, ans, wr, 'при a > 1 більшому показнику відповідає більше значення, при 0 < a < 1 — менше', sl)
    base = rng.choice([2, 3, 5, F(1, 2), F(1, 3), F(1, 5), 10]); p, q = rng.sample([2, 3, 5, 6, 7, 9, 11, 13], 2)
    up = base > 1; hi = p > q; gt = (hi == up)
    sym = '>' if gt else '<'
    bs = ffmt(base)
    txt = f'Порівняйте числа log{SUBL.get(base, "_" + bs) if not isinstance(base, F) else "_(" + bs + ")"} {p} і log{SUBL.get(base, "_" + bs) if not isinstance(base, F) else "_(" + bs + ")"} {q}. Укажіть правильну відповідь.'
    ans = f'перше число {"більше" if gt else "менше"} за друге'
    wr = [(f'перше число {"менше" if gt else "більше"} за друге', 'не враховано, що логарифмічна функція ' + ('зростає' if up else 'спадає') + f' (основа {bs} ' + ('більша' if up else 'менша') + ' за 1)'), ('числа рівні', 'аргументи різні, а логарифмічна функція монотонна — значення різні'), ('порівняти неможливо', 'порівняти можна, адже основа однакова й функція монотонна')]
    return T.add(lv, txt, ans, wr, 'при a > 1 логарифмічна функція зростає, при 0 < a < 1 — спадає', f'основа {bs} {">" if up else "<"} 1, функція {"зростає" if up else "спадає"}; {p} {">" if hi else "<"} {q}, тому перше число {"більше" if gt else "менше"} за друге')

# ================= L2 =================
def f_domain_comb(T, rng, lv):
    kind = rng.choice(['sq_quad', 'inv_sqrt', 'sqrt_frac', 'log_quad', 'two_sqrt', 'log_sqrt', 'frac_quad', 'sqrt_sqrt'])
    G = setstr
    if kind == 'sq_quad':
        c = rng.randint(2, 9)
        txt = f'y = √({poly([1, 0, -c * c])})'; pred = lambda x: x * x - c * c >= 0; crit = [-c, c]
        sl = f'x² − {c * c} ≥ 0 ⇒ (x − {c})(x + {c}) ≥ 0 ⇒ x ≤ {M}{c} або x ≥ {c}'
        trap = 'нерівність x² ≥ c² розв’язують методом інтервалів: це «зовнішні» промені, а не відрізок між коренями'
    elif kind == 'inv_sqrt':
        a, b = rng.sample(range(-8, 9), 2); a, b = min(a, b), max(a, b)
        if b - a < 2: return False
        txt = f'y = 1/√(({poly([1, -a])})({poly([1, -b])}))'; pred = lambda x: (x - a) * (x - b) > 0; crit = [a, b]
        sl = f'підкореневий вираз у знаменнику має бути строго додатним: ({poly([1, -a])})({poly([1, -b])}) > 0 ⇒ x < {fmt(a)} або x > {fmt(b)}'
        trap = 'корінь стоїть у знаменнику, тому підкореневий вираз строго більший за 0 (рівність нулю неприпустима)'
    elif kind == 'sqrt_frac':
        a = rng.randint(-6, 3); m = a + rng.randint(2, 7)
        txt = f'y = √({poly([1, -a])})/({poly([1, -m])})'; pred = lambda x: x - a >= 0 and x != m; crit = [a, m]
        sl = f'{poly([1, -a])} ≥ 0 ⇒ x ≥ {fmt(a)}; знаменник: x ≠ {fmt(m)}'
        trap = 'крім умови для кореня, треба виключити нуль знаменника'
    elif kind == 'log_quad':
        a, b = rng.sample(range(-7, 8), 2); a, b = min(a, b), max(a, b)
        if b - a < 2: return False
        base = rng.choice([2, 3, 5])
        txt = f'y = log{SUBL[base]}(({poly([1, -a])})({poly([1, -b])}))'; pred = lambda x: (x - a) * (x - b) > 0; crit = [a, b]
        sl = f'({poly([1, -a])})({poly([1, -b])}) > 0 ⇒ x < {fmt(a)} або x > {fmt(b)}'
        trap = 'добуток додатний, коли множники мають однаковий знак — ззовні від коренів, а не між ними'
    elif kind == 'two_sqrt':
        a = rng.randint(-8, 2); b = a + rng.randint(3, 9)
        txt = f'y = √({poly([1, -a])}) + √({poly([-1, b])})'; pred = lambda x: x - a >= 0 and b - x >= 0; crit = [a, b]
        sl = f'{poly([1, -a])} ≥ 0 і {poly([-1, b])} ≥ 0 ⇒ {fmt(a)} ≤ x ≤ {fmt(b)}'
        trap = 'обидва підкореневі вирази мають бути невід’ємними одночасно (перетин умов)'
    elif kind == 'log_sqrt':
        a = rng.randint(-6, 3); b = a + rng.randint(3, 9)
        txt = f'y = log₂({poly([1, -a])}) + √({poly([-1, b])})'; pred = lambda x: x - a > 0 and b - x >= 0; crit = [a, b]
        sl = f'{poly([1, -a])} > 0 і {poly([-1, b])} ≥ 0 ⇒ {fmt(a)} < x ≤ {fmt(b)}'
        trap = 'під логарифмом — строга нерівність, під коренем — нестрога: кінці проміжку різні'
    elif kind == 'frac_quad':
        r1, r2 = rng.sample(range(-7, 8), 2); r1, r2 = min(r1, r2), max(r1, r2)
        txt = f'y = 1/({poly(expand2(r1, r2))})'; pred = lambda x: (x - r1) * (x - r2) != 0; crit = [r1, r2]
        sl = f'{poly(expand2(r1, r2))} ≠ 0 ⇒ x ≠ {fmt(r1)} і x ≠ {fmt(r2)}'
        trap = 'виключаються обидва корені квадратного тричлена'
    else:
        a = rng.randint(-5, 2); m = rng.randint(1, 6)
        txt = f'y = √({poly([1, -a])})/√({poly([-1, a + m])})'; pred = lambda x: x - a >= 0 and a + m - x > 0; crit = [a, a + m]
        sl = f'{poly([1, -a])} ≥ 0 ⇒ x ≥ {fmt(a)}; {poly([-1, a + m])} > 0 ⇒ x < {fmt(a + m)}'
        trap = 'корінь у знаменнику вимагає строгої нерівності, корінь у чисельнику — нестрогої'
    sol = pred_set(pred, crit)
    wr = [(G(toggle(sol)), 'кінці проміжків (дужки) визначено неправильно: строгість/нестрогість умов переплутано'), (G(complement(sol)), 'вказано множину, де вираз не існує (доповнення до області визначення)')]
    wr.append((G(mirror(sol)), 'знаки меж змінено на протилежні'))
    if len(sol) >= 2: wr.append((G(sol[:1]), 'враховано лише один із проміжків'))
    else:
        lo, hi, lc, rc = sol[0]
        if lo is not None and hi is not None: wr.append((G([(lo, hi, not lc, not rc)]) if (lc == rc) else G([(lo, hi, lc, lc)]), 'кінці проміжку визначено неправильно'))
        wr.append((G([(None, None, False, False)]), 'умови не враховано: область визначення — уся числова пряма'))
    return T.add(lv, f'Знайдіть область визначення функції {txt}.', G(sol), wr, trap, sl)

def f_domain_int_count(T, rng, lv):
    kind = rng.choice(['seg', 'seg', 'open', 'quad_out', 'sum'])
    if kind == 'seg':
        a = rng.randint(-9, 2); b = a + rng.randint(4, 11); k = b - a + 1
        txt = f'y = √({poly([1, -a])}) + √({poly([-1, b])})'
        ans = F(k); wr = [(F(k - 1), 'враховано не всі кінці: різницю b − a не збільшено на 1'), (F(k - 2), 'виключено обидва кінці, хоча корінь допускає 0'), (F(b + a), 'додано кінці проміжку'), (F(k + 1), 'до кількості цілих додано зайвий 1')]
        return T.add(lv, f'Скільки цілих чисел містить область визначення функції {txt}?', ans, wr, 'для відрізка [a; b] кількість цілих чисел дорівнює b − a + 1', f'область визначення [{fmt(a)}; {fmt(b)}]; цілих чисел {fmt(b)} − {pn(a)} + 1 = {k}')
    if kind == 'open':
        a = rng.randint(-9, 2); b = a + rng.randint(5, 12); k = b - a - 1
        txt = f'y = log₂(({poly([1, -a])})({poly([-1, b])}))'
        ans = F(k); wr = [(F(k + 1), 'різницю b − a взято без віднімання 1 (кінці включено)'), (F(k + 2), 'до кількості додано обидва кінці'), (F(k - 1), 'забрано зайве: виключено ще одне число'), (F(b - a - 2) if b - a - 2 != k else F(b + a), 'неправильно підраховано число цілих у проміжку')]
        return T.add(lv, f'Скільки цілих чисел належить області визначення функції {txt}?', ans, wr, 'нерівність строга: кінці (a; b) не входять; цілих b − a − 1', f'({poly([1, -a])})({poly([-1, b])}) > 0 ⇒ x ∈ ({fmt(a)}; {fmt(b)}); цілих чисел {fmt(b)} − {pn(a)} − 1 = {k}')
    if kind == 'quad_out':
        c = rng.randint(3, 8); lo_, hi_ = -(c - 1), c - 1
        txt = f'y = √({c * c} − x²)'
        ans = F(2 * c - 1); wr = [(F(2 * c - 3), 'кінці −c і c відкинуто, хоча корінь допускає 0'), (F(2 * c), 'забули про x = 0 або порахували зайве'), (F(c), 'враховано лише додатні числа й нуль'), (F(2 * c + 1), 'додано зайві числа за межами області')]
        return T.add(lv, f'Скільки цілих чисел містить область визначення функції {txt}?', ans, wr, 'нерівність нестрога: кінці [−c; c] входять', f'{c * c} − x² ≥ 0 ⇒ |x| ≤ {c} ⇒ [{M}{c}; {c}]; цілих чисел {2 * c + 1}'.replace(f'{2*c+1}', str(2 * c + 1)))
    if kind == 'sum':
        a = rng.randint(-5, 0); b = a + rng.randint(4, 8)
        txt = f'y = √({poly([1, -a])})/√({poly([-1, b])})'
        cnt = b - a; ints = list(range(a, b)); ans = F(sum(ints))
        wr = [(F(sum(range(a, b + 1))), 'включено правий кінець b, хоча під коренем у знаменнику строга нерівність'), (F(sum(range(a + 1, b))), 'виключено лівий кінець a, хоча під коренем у чисельнику нерівність нестрога'), (F(a + b - 1), 'за суму взято суму крайніх значень'), (F(len(ints)), 'знайдено кількість цілих чисел, а не їх суму')]
        return T.add(lv, f'Знайдіть суму всіх цілих чисел, що належать області визначення функції {txt}.', ans, wr, 'лівий кінець входить (корінь у чисельнику), правий — ні (корінь у знаменнику)', f'x ∈ [{fmt(a)}; {fmt(b)}); цілі: {", ".join(fmt(v) for v in ints)}; сума {fmt(ans)}')
    return False

def f_extrema_segment(T, rng, lv):
    a = rng.choice([-3, -2, -1, 1, 2, 3]); m = rng.randint(-4, 4); n_ = rng.randint(-8, 8)
    b = -2 * a * m; c = a * m * m + n_; co = [a, b, c]
    f = lambda x: ev(co, x)
    inside = rng.random() < .55
    if inside: lo = m - rng.randint(1, 4); hi = m + rng.randint(1, 4)
    else:
        side = rng.choice([-1, 1]); lo = m + side * rng.randint(1, 3); hi = lo + side * rng.randint(2, 4)
        if side < 0: lo, hi = hi, lo
    if lo >= hi: return False
    want = rng.choice(['max', 'min'])
    vals = [f(lo), f(hi)] + ([f(m)] if lo <= m <= hi else [])
    ans = max(vals) if want == 'max' else min(vals)
    word = 'найбільше' if want == 'max' else 'найменше'
    wr = []
    if lo <= m <= hi: wr.append((max(f(lo), f(hi)) if want == 'max' else min(f(lo), f(hi)), 'розглянуто лише значення на кінцях відрізка, вершину не враховано'))
    else: wr.append((f(m), 'взято значення у вершині, яка не належить відрізку'))
    wr.append((f(lo) if ans != f(lo) else f(hi), 'взято значення лише на одному кінці'))
    wr.append((min(vals) if want == 'max' else max(vals), f'знайдено {"найменше" if want == "max" else "найбільше"} значення замість {word}'))
    wr.append((F(m), 'названо абсцису вершини, а не значення функції'))
    wr.append((f(lo) + f(hi), 'додано значення на кінцях'))
    pos = 'належить відрізку' if lo <= m <= hi else 'не належить відрізку'
    sl = f'вершина x₀ = {fmt(m)} {pos}; ' + (f'f({fmt(lo)}) = {fmt(f(lo))}, f({fmt(hi)}) = {fmt(f(hi))}' + (f', f({fmt(m)}) = {fmt(f(m))}' if lo <= m <= hi else '')) + f'; {word} значення {fmt(ans)}'
    return T.add(lv, f'Знайдіть {word} значення функції {ys(*co)} на відрізку [{fmt(lo)}; {fmt(hi)}].', ans, wr, 'на відрізку екстремум може бути у вершині (якщо вона на відрізку) або на кінцях; перевіряйте всі точки', sl)

def f_range_trig(T, rng, lv):
    kind = rng.choice(['asin', 'acos', 'neg', 'cnt'])
    a = rng.choice([2, 3, 4, 5, 6]); b = rng.randint(-6, 6); k = rng.choice([1, 2, 3])
    arg = 'x' if k == 1 else f'{k}x'
    fn = rng.choice(['sin', 'cos'])
    sgn = rng.choice([1, -1]) if kind == 'neg' else 1
    aa = a * sgn
    lo, hi = b - a, b + a
    if kind == 'cnt':
        ans = F(2 * a + 1)
        txt = f'Скільки цілих значень набуває функція y = {fmt(aa) if abs(aa) != 1 else ""}{fn} {arg}{" " + sg(b) + " " + str(abs(b)) if b else ""}?'
        wr = [(F(2 * a), 'не враховано, що обидві межі входять до області значень'), (F(2 * a + 2), 'до кількості додано зайву межу'), (F(a + 1), 'враховано лише додатні значення синуса/косинуса'), (F(a), 'враховано лише половину значень')]
        return T.add(lv, txt, ans, wr, 'область значень — відрізок [b − a; b + a]; цілих чисел у ньому (b + a) − (b − a) + 1', f'область значень [{fmt(lo)}; {fmt(hi)}], довжина 2·{a}; цілих чисел {2 * a + 1}')
    txt = f'y = {"−" if sgn < 0 else ""}{a}{fn} {arg}{" " + sg(b) + " " + str(abs(b)) if b else ""}'
    sol = [(F(lo), F(hi), True, True)]
    wr = [(setstr([(F(-a), F(a), True, True)]), 'не враховано зсув на ' + fmt(b) if b else 'не враховано множник перед тригонометричною функцією'), (setstr([(F(lo), F(hi), False, False)]), 'межі досягаються, тому дужки квадратні'), (setstr([(F(b - 1), F(b + 1), True, True)]), f'не враховано множник {a} перед функцією'), (setstr([(F(b), F(b + a), True, True)]), 'враховано лише додатні значення функції sin/cos'), (setstr([(F(-hi), F(-lo), True, True)]), 'знаки меж змінено на протилежні')]
    if b == 0: wr[0] = (setstr([(F(-1), F(1), True, True)]), 'не враховано множник перед тригонометричною функцією')
    return T.add(lv, f'Знайдіть область значень функції {txt}.', setstr(sol), wr, 'множник k у аргументі (kx) область значень не змінює; змінюють її множник перед функцією та зсув', f'−1 ≤ {fn} {arg} ≤ 1; множимо на {a}{" (знак нерівностей не змінюється; при мінусі межі міняються місцями — відрізок той самий)" if sgn < 0 else ""} і додаємо {fmt(b)}: [{fmt(lo)}; {fmt(hi)}]')

def f_range_other(T, rng, lv):
    kind = rng.choice(['sqrt', 'hyp', 'hyp2', 'absq', 'quad_neg'])
    G = setstr
    if kind == 'sqrt':
        a = rng.randint(-6, 6); b = rng.choice([v for v in range(-7, 8) if v]); k = rng.choice([1, 2, 3, -1, -2])
        txt = f'y = {"−" if k < 0 else ""}{abs(k) if abs(k) > 1 else ""}√({poly([1, -a])}) {sg(b)} {abs(b)}'
        sol = [(F(b), None, True, False)] if k > 0 else [(None, F(b), False, True)]
        wr = [(G([(F(b), None, False, False)] if k > 0 else [(None, F(b), False, False)]), f'значення {fmt(b)} досягається при x = {fmt(a)}, тому дужка квадратна'), (G([(None, F(b), False, True)] if k > 0 else [(F(b), None, True, False)]), 'неправильно визначено, куди напрямлена функція (знак перед коренем)'), (G([(F(a + b), None, True, False)] if k > 0 else [(None, F(a + b), False, True)]), 'число під коренем змішано зі зсувом: область значень залежить лише від зсуву b'), (G([(F(0), None, True, False)]), 'не враховано зсув на ' + fmt(b))]
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'зсув під коренем область значень не змінює; змінює лише доданок поза коренем', f'√({poly([1, -a])}) ≥ 0, тож y {"≥" if k > 0 else "≤"} {fmt(b)}; значення {fmt(b)} досягається при x = {fmt(a)}')
    if kind == 'hyp':
        a = rng.randint(-5, 5); b = rng.choice([v for v in range(-6, 7) if v]); k = rng.choice([1, 2, 3, 4, -1, -2, -3])
        txt = f'y = {k}/({poly([1, -a])}) {sg(b)} {abs(b)}'
        sol = [(None, F(b), False, False), (F(b), None, False, False)]
        wr = [(G([(None, F(a), False, False), (F(a), None, False, False)]), f'виключено число {fmt(a)} (воно виключається з області визначення, а не значень)'), (G([(None, None, False, False)]), 'дріб k/(x − a) ніколи не дорівнює 0, тому y ≠ ' + fmt(b)), (G([(None, F(0), False, False), (F(0), None, False, False)]), 'не враховано зсув на ' + fmt(b)), (G([(None, F(-b), False, False), (F(-b), None, False, False)]), f'число {fmt(b)} взято з протилежним знаком')]
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'гіпербола k/(x − a) + b ніколи не набуває значення b (горизонтальна асимптота y = b)', f'дріб {k}/({poly([1, -a])}) ≠ 0, тому y ≠ {fmt(b)}')
    if kind == 'hyp2':
        b = rng.choice([v for v in range(-6, 7) if v]); k = rng.choice([1, 2, 3, 4, -1, -2, -3])
        txt = f'y = {k}/x {sg(b)} {abs(b)}'
        sol = [(None, F(b), False, False), (F(b), None, False, False)]
        wr = [(G([(None, F(0), False, False), (F(0), None, False, False)]), f'виключено нуль: x ≠ 0 стосується області визначення, а не значень'), (G([(None, None, False, False)]), f'число {fmt(b)} не буде значенням функції'), (G([(None, F(-b), False, False), (F(-b), None, False, False)]), f'число {fmt(b)} взято з протилежним знаком')]
        wr.append((G([(F(b), None, False, False)]), 'враховано лише частину значень (дріб може бути і від’ємним)'))
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'k/x ≠ 0 для будь-якого x, тому y ≠ b', f'{k}/x ≠ 0, отже y ≠ {fmt(b)}')
    if kind == 'absq':
        a = rng.choice([v for v in range(-5, 6) if v]); c = rng.randint(1, 7)
        txt = f'y = |{poly([1, -a])}| {sg(-c)} {c}' if False else f'y = |{poly([1, -a])}| − {c}'
        sol = [(F(-c), None, True, False)]
        wr = [(G([(F(c), None, True, False)]), f'число {c} взято з протилежним знаком'), (G([(F(-c), None, False, False)]), f'значення {fmt(-c)} досягається при x = {fmt(a)}'), (G([(F(0), None, True, False)]), f'не враховано зсув на −{c}'), (G([(F(a - c), None, True, False)]), 'абсцису вершини змішано з зсувом за y')]
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'зсув усередині модуля (за x) область значень не змінює', f'|{poly([1, -a])}| ≥ 0, тож y ≥ {fmt(-c)}; значення {fmt(-c)} досягається при x = {fmt(a)}')
    a = rng.choice([1, 2, 3]); m = rng.randint(-3, 3); n_ = rng.randint(-5, 5)
    b = -2 * (-a) * m
    co = [-a, b, -a * m * m + n_]
    txt = ys(*co)
    sol = [(None, F(n_), False, True)]
    wr = [(G([(F(n_), None, True, False)]), 'гілки параболи напрямлені вниз (a < 0), значення не більші за ординату вершини'), (G([(None, F(m), False, True)]), 'за найбільше значення взято абсцису вершини'), (G([(None, F(co[2]), False, True)]), 'за найбільше значення взято вільний член c'), (G([(None, F(n_), False, False)]), 'вершина належить графіку, тому дужка квадратна')]
    return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'область значень параболи визначає ордината вершини y₀, а не c чи x₀', f'x₀ = {fmt(m)}, y₀ = {fmt(n_)}; a < 0 ⇒ y ≤ {fmt(n_)}')

def f_parity2(T, rng, lv):
    FUN = [('x²·sin x', lambda x: x * x * math.sin(x)), ('x³·cos x', lambda x: x**3 * math.cos(x)), ('x·sin x', lambda x: x * math.sin(x)), ('(x² + 1)/x', lambda x: (x * x + 1) / x), ('x/(x² + 1)', lambda x: x / (x * x + 1)), ('x⁴ − cos x', lambda x: x**4 - math.cos(x)), ('x⁴ + 2x²', lambda x: x**4 + 2 * x * x),
           ('x² + x', lambda x: x * x + x), ('(x³ + x)·cos x', lambda x: (x**3 + x) * math.cos(x)), ('|x|·x³', lambda x: abs(x) * x**3), ('x + 1/x', lambda x: x + 1 / x), ('sin x + x²', lambda x: math.sin(x) + x * x), ('x³·|x|', lambda x: x**3 * abs(x)), ('x·|x|·sin x', lambda x: x * abs(x) * math.sin(x)),
           ('cos x/x', lambda x: math.cos(x) / x), ('x² − |x|', lambda x: x * x - abs(x)), ('x⁵ − 3x³', lambda x: x**5 - 3 * x**3), ('(x² − 1)/(x² + 1)', lambda x: (x * x - 1) / (x * x + 1)), ('(x + 1)²', lambda x: (x + 1)**2), ('x·cos x + x³', lambda x: x * math.cos(x) + x**3),
           ('2ˣ + 2⁻ˣ', lambda x: 2**x + 2**(-x)), ('2ˣ − 2⁻ˣ', lambda x: 2**x - 2**(-x)), ('3ˣ + 1', lambda x: 3**x + 1), ('x² + tg x', lambda x: x * x + math.tan(x)), ('tg x·sin x', lambda x: math.tan(x) * math.sin(x)), ('x⁶ − sin x', lambda x: x**6 - math.sin(x))]
    name, f = rng.choice(FUN)
    pts = [0.7, 1.3, 0.45, 0.9]
    ev_ = all(abs(f(x) - f(-x)) < 1e-9 for x in pts); od_ = all(abs(f(x) + f(-x)) < 1e-9 for x in pts)
    ans = 'парна' if ev_ else ('непарна' if od_ else 'ні парна, ні непарна')
    why = {'парна': ('f(−x) = −f(x): знак змінюється, а для парності потрібно f(−x) = f(x)' if od_ else 'рівність f(−x) = f(x) виконується не для всіх x'),
           'непарна': ('f(−x) = f(x): значення не змінює знак, а для непарності потрібно f(−x) = −f(x)' if ev_ else 'рівність f(−x) = −f(x) виконується не для всіх x'),
           'ні парна, ні непарна': 'функція має симетрію (f(−x) = f(x) або f(−x) = −f(x)), тому вона парна чи непарна',
           'і парна, і непарна': 'це можливо лише для f(x) ≡ 0; тут функція не нульова'}
    wr = [('функція ' + o, why[o]) for o in why if o != ans]
    sol = {'парна': 'f(−x) = f(x): функція парна', 'непарна': 'f(−x) = −f(x): функція непарна', 'ні парна, ні непарна': 'f(−x) не збігається ні з f(x), ні з −f(x): функція ні парна, ні непарна'}[ans]
    return T.add(lv, f'Яке з тверджень правильне для функції f(x) = {name}?', 'функція ' + ans, wr, 'добуток двох функцій однакової парності — парна, різної — непарна; сума парної й непарної (ненульових) парності не має', sol)

def f_period2(T, rng, lv):
    kind = rng.choice(['sum', 'sum', 'sq', 'abs'])
    if kind == 'sum':
        a, b = rng.sample([1, 2, 3, 4, 5, 6], 2); f1 = rng.choice(['sin', 'cos']); f2 = rng.choice(['sin', 'cos']); 
        t1, t2 = F(2, a), F(2, b); ans = lcmF(t1, t2)
        txt = f'y = {f1}({a}x) + {f2}({b}x)' if a > 1 and b > 1 else f'y = {f1} {("" if a == 1 else str(a))}x + {f2} {("" if b == 1 else str(b))}x'
        wr = [(t1 + t2, 'періоди доданків додано'), (min(t1, t2), 'взято менший з періодів'), (t1 * t2, 'періоди доданків перемножено'), (max(t1, t2), 'взято більший з періодів, не перевіряючи, чи є він кратним іншому'), (F(2), 'взято 2π, не врахувавши коефіцієнти при x')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, 'період суми — найменше спільне кратне періодів доданків', f'T₁ = {pim(t1)}, T₂ = {pim(t2)}; НСК = {pim(ans)}')
    if kind == 'sq':
        f1 = rng.choice(['sin', 'cos']); k = rng.choice([1, 2, 3]); ans = F(1, k)
        txt = f'y = {f1}²({k if k > 1 else ""}x)' if k > 1 else f'y = {f1}² x'
        wr = [(F(2, k), f'взято період самої функції {f1}'), (F(1, 2 * k), 'період поділено ще й на 2'), (F(4, k), 'період подвоєно'), (F(1), 'коефіцієнт при x не враховано')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, f'{f1}² α = (1 ∓ cos 2α)/2: період зменшується вдвічі', f'{f1}² t = (1 {"−" if f1 == "sin" else "+"} cos 2t)/2, де t = {k if k > 1 else ""}x; період {pim(F(1, k))}')
    if kind == 'abs':
        f1 = rng.choice(['sin', 'cos']); k = rng.choice([1, 2, 3, 4]); ans = F(1, k)
        txt = f'y = |{f1}({k}x)|' if k > 1 else f'y = |{f1} x|'
        wr = [(F(2, k), f'взято період функції {f1}({k}x), а модуль зменшує його вдвічі'), (F(1, 2 * k), 'період поділено ще й на 2'), (F(1), 'коефіцієнт при x не враховано'), (F(4, k), 'період подвоєно')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, 'модуль відображає від’ємні піввихилі вгору, тому період sin/cos зменшується вдвічі', f'період {f1}({k}x) дорівнює {pim(F(2, k))}, а |{f1}({k}x)| — вдвічі менший: {pim(ans)}')
    a, b = rng.sample([1, 2, 3, 4], 2)
    txt = f'y = sin({a}x)·cos({b}x)' if a > 1 and b > 1 else f'y = sin {("" if a == 1 else str(a))}x·cos {("" if b == 1 else str(b))}x'
    t1, t2 = F(2, a), F(2, b); ans = lcmF(t1, t2)
    wr = [(pim(t1 * t2), 'періоди множників перемножено'), (pim(t1 + t2), 'періоди множників додано'), (pim(min(t1, t2)), 'взято менший з періодів'), (pim(F(2)), 'взято 2π, не врахувавши коефіцієнти при x')]
    return T.add(lv, f'Знайдіть період функції {txt} (один із періодів, що не обов’язково найменший, але спільний для обох множників).', pim(ans), wr, 'спільний період добутку — НСК періодів множників', f'T₁ = {pim(t1)}, T₂ = {pim(t2)}; НСК = {pim(ans)}') if False else False

def f_composite(T, rng, lv):
    kind = rng.choice(['val', 'val', 'expr', 'self'])
    a = rng.choice([-3, -2, -1, 1, 2, 3]); b = rng.randint(-5, 5); c = rng.randint(-5, 5); d = rng.choice([-3, -2, 2, 3, 4]); e = rng.randint(-6, 6)
    f = lambda x: a * x * x + b * x + c
    g = lambda x: d * x + e
    x0 = rng.choice([-2, -1, 0, 1, 2, 3])
    fx = poly([a, b, c]); gx = poly([d, e])
    if kind == 'val':
        ans = f(g(x0)); 
        wr = [(g(f(x0)), 'функції підставлено у зворотному порядку: g(f(x)) замість f(g(x))'), (f(x0) * g(x0), 'знайдено добуток f(x₀)·g(x₀)'), (f(x0) + g(x0), 'знайдено суму f(x₀) + g(x₀)'), (f(g(x0) + 0) if False else f(x0) , 'знайдено f(x₀) замість f(g(x₀))')]
        return T.add(lv, f'Нехай f(x) = {fx}, g(x) = {gx}. Знайдіть f(g({fmt(x0)})).', ans, wr, 'спочатку обчислюють внутрішню функцію g, потім підставляють результат у f', f'g({fmt(x0)}) = {fmt(g(x0))}; f({fmt(g(x0))}) = {fmt(ans)}')
    if kind == 'self':
        ans = f(f(x0))
        wr = [(f(x0) * f(x0), 'значення функції піднесено до квадрата замість підстановки в f'), (2 * f(x0), 'значення f(x₀) подвоєно'), (f(x0), 'підставлення виконано лише один раз'), (f(x0 * x0), 'у f підставлено x₀² замість f(x₀)')]
        return T.add(lv, f'Нехай f(x) = {fx}. Знайдіть f(f({fmt(x0)})).', ans, wr, 'f(f(x₀)): спочатку f(x₀), потім це число знову підставляють у f', f'f({fmt(x0)}) = {fmt(f(x0))}; f({fmt(f(x0))}) = {fmt(ans)}')
    # вираз f(g(x)) для лінійних f, g
    p, q = rng.choice([2, 3, -2, -3, 4]), rng.choice([v for v in range(-5, 6) if v]); r, s_ = rng.choice([2, 3, -2, 4, -1]), rng.choice([v for v in range(-6, 7) if v])
    if (p, q) == (r, s_): return False
    F1 = lambda x: p * x + q; G1 = lambda x: r * x + s_
    comp = [p * r, p * s_ + q]; comp2 = [r * p, r * q + s_]
    ans = ys(*comp)
    wr = [(ys(*comp2), 'композицію записано у зворотному порядку: g(f(x))'), (ys(p * r, p * s_ - q) if q else ys(p * r, p * s_ + 1), 'вільний член f додано з протилежним знаком'), (ys(p + r, q + s_), 'функції додано замість підстановки'), (ys(p * r, q * s_), 'вільні члени перемножено')]
    return T.add(lv, f'Нехай f(x) = {poly([p, q])}, g(x) = {poly([r, s_])}. Знайдіть формулу функції y = f(g(x)).', ans, wr, 'f(g(x)): замість x у f підставляють весь вираз g(x)', f'f(g(x)) = {fmt(p)}·({poly([r, s_])}) {sg(q)} {abs(q)} = {poly(comp)}')

def f_shift_value(T, rng, lv):
    kind = rng.choice(['x1', 'x2', 'half'])
    a = rng.choice([1, 2, 3]); b = rng.randint(-6, 6); c = rng.randint(-8, 8)
    base = [a, b, c]
    if kind in ('x1', 'x2'):
        s_ = 1 if kind == 'x1' else rng.choice([2, 3, -1, -2])
        g = lambda x: ev(base, x)  # f(x + s) = g(x)
        t = rng.randint(2, 6) + s_ if s_ > 0 else rng.randint(1, 5)
        x0 = t - s_
        ans = g(x0)
        wr = [(g(t), f'у вираз підставлено x = {t}, але його треба брати x = {t} − ({fmt(s_)}) = {x0}'), (g(t + s_), f'аргумент змінено в протилежний бік (x = {fmt(t + s_)})'), (g(-x0), 'аргумент взято з протилежним знаком'), (ev(base, t) + s_, 'зсув додано до значення, а не до аргументу')]
        return T.add(lv, f'Відомо, що f(x {"+" if s_ > 0 else "−"} {abs(s_)}) = {poly(base)}. Знайдіть f({t}).', ans, wr, f'f({t}) = f(x {"+" if s_>0 else "−"} {abs(s_)}) при x = {t} {"−" if s_>0 else "+"} {abs(s_)}', f'x {"+" if s_ > 0 else "−"} {abs(s_)} = {t} ⇒ x = {x0}; f({t}) = {fmt(ans)}')
    k = rng.choice([2, 3, 4]); m = rng.randint(-3, 3)
    g = lambda x: ev(base, x)  # f(kx) = g(x)
    x0 = rng.choice([-3, -2, -1, 1, 2, 3]); t = k * x0
    ans = g(x0)
    wr = [(g(t), f'у вираз підставлено x = {t}, але kx = {t} ⇒ x = {x0}'), (g(x0 * k * k), 'аргумент помножено двічі'), (g(F(t, 1) / (k * k)) if False else g(t + k), 'неправильно знайдено x'), (ev(base, k) * x0 if False else ev(base, -x0), 'аргумент взято з протилежним знаком')]
    return T.add(lv, f'Відомо, що f({k}x) = {poly(base)}. Знайдіть f({t}).', ans, wr, f'f({t}) = f({k}·{pn(x0)}): спочатку знайдіть x із {k}x = {t}', f'{k}x = {t} ⇒ x = {x0}; f({t}) = {fmt(ans)}')

def f_inverse_formula(T, rng, lv):
    kind = rng.choice(['lin', 'lin', 'cube', 'sqrt', 'exp', 'log', 'frac'])
    if kind == 'lin':
        k = rng.choice([-4, -3, -2, 2, 3, 4, 5]); b = rng.choice([v for v in range(-9, 10) if v])
        bs = '−' if b > 0 else '+'; ob = '+' if b > 0 else '−'
        def invs(kv, sign): return f'y = (x {sign} {abs(b)})/{kv}' if kv > 0 else f'y = −(x {sign} {abs(b)})/{abs(kv)}'
        ans = invs(k, bs)
        w3 = (invs(abs(k), bs), 'знак коефіцієнта k при діленні втрачено') if k < 0 else (f'y = x/{k} {bs} {abs(b)}', 'вільний член не поділено на k')
        wr = [(invs(k, ob), 'вільний член додано/віднято з неправильним знаком (треба виконати зворотну дію)'), (ys(k, -b), 'змінено лише знак вільного члена, а коефіцієнт k не перенесено в знаменник'), w3, (f'y = {k}/(x {bs} {abs(b)})', 'дріб записано перевернутим')]
        return T.add(lv, f'Знайдіть функцію, обернену до функції {ys(k, b)}.', ans, wr, 'щоб знайти обернену, виразіть x через y, потім поміняйте місцями x та y', f'y = {poly([k, b])} ⇒ x = (y {bs} {abs(b)})/{pn(k)}; міняємо x і y: {ans}')
    if kind == 'cube':
        c = rng.choice([v for v in range(-8, 9) if v]); ans = f'y = ∛(x {"−" if c > 0 else "+"} {abs(c)})'
        wr = [(f'y = ∛(x {"+" if c > 0 else "−"} {abs(c)})', 'константу перенесено зі знаком, що не відповідає зворотній дії'), (f'y = ∛x {"−" if c > 0 else "+"} {abs(c)}', 'число, що додавали до x³, віднято вже після добування кореня'), (f'y = (x {"−" if c > 0 else "+"} {abs(c)})³', 'замість кубічного кореня піднесено до куба'), (f'y = √(x {"−" if c > 0 else "+"} {abs(c)})', 'взято квадратний корінь замість кубічного')]
        return T.add(lv, f'Знайдіть функцію, обернену до функції y = x³ {sg(c)} {abs(c)}.', ans, wr, 'обернена до x³ + c: x = ∛(y − c)', f'y = x³ {sg(c)} {abs(c)} ⇒ x³ = y {"−" if c > 0 else "+"} {abs(c)} ⇒ x = ∛(y {"−" if c > 0 else "+"} {abs(c)}); міняємо x і y: {ans}')
    if kind == 'sqrt':
        c = rng.choice([v for v in range(-6, 7) if v]); ans = f'y = (x {"−" if c > 0 else "+"} {abs(c)})², x ≥ {fmt(c)}'
        wr = [(f'y = (x {"+" if c > 0 else "−"} {abs(c)})², x ≥ {fmt(c)}', 'константу перенесено зі знаком, що не відповідає зворотній дії'), (f'y = x² {"−" if c > 0 else "+"} {abs(c)}, x ≥ {fmt(c)}', 'число віднімають до піднесення в квадрат, а не після'), (f'y = (x {"−" if c > 0 else "+"} {abs(c)})², x ≥ 0', 'область визначення оберненої — область значень початкової: x ≥ ' + fmt(c)), (f'y = √(x {"−" if c > 0 else "+"} {abs(c)}), x ≥ {fmt(c)}', 'взято корінь замість піднесення до квадрата')]
        return T.add(lv, f'Знайдіть функцію, обернену до функції y = √x {sg(c)} {abs(c)}.', ans, wr, 'область значень початкової функції стає областю визначення оберненої', f'y = √x {sg(c)} {abs(c)} ⇒ √x = y {"−" if c > 0 else "+"} {abs(c)} ⇒ x = (y {"−" if c > 0 else "+"} {abs(c)})², y ≥ {fmt(c)}; міняємо x і y: {ans}')
    if kind == 'exp':
        a = rng.choice([2, 3, 5]); c = rng.choice([v for v in range(-4, 5) if v])
        ans = f'y = log{SUBL[a]}(x {"−" if c > 0 else "+"} {abs(c)})'
        wr = [(f'y = log{SUBL[a]}(x {"+" if c > 0 else "−"} {abs(c)})', 'константу перенесено зі знаком, що не відповідає зворотній дії'), (f'y = log{SUBL[a]} x {"−" if c > 0 else "+"} {abs(c)}', 'число, що додавали до aˣ, віднято вже після логарифмування'), (f'y = {a}^(x {"−" if c > 0 else "+"} {abs(c)})', 'замість логарифма записано показникову функцію'), (f'y = log_x({a}) {"−" if c > 0 else "+"} {abs(c)}', 'основу й аргумент логарифма переплутано')]
        return T.add(lv, f'Знайдіть функцію, обернену до функції y = {a}ˣ {sg(c)} {abs(c)}.', ans, wr, 'логарифм береться від виразу (x − c), а не від x', f'y = {a}ˣ {sg(c)} {abs(c)} ⇒ {a}ˣ = y {"−" if c > 0 else "+"} {abs(c)} ⇒ x = log{SUBL[a]}(y {"−" if c > 0 else "+"} {abs(c)}); міняємо x і y: {ans}')
    if kind == 'log':
        a = rng.choice([2, 3, 5]); c = rng.choice([v for v in range(-4, 5) if v])
        ans = f'y = {a}^(x {"−" if c > 0 else "+"} {abs(c)})'
        wr = [(f'y = {a}^(x {"+" if c > 0 else "−"} {abs(c)})', 'константу перенесено зі знаком, що не відповідає зворотній дії'), (f'y = {a}^x {"−" if c > 0 else "+"} {abs(c)}', 'число, що додавали до логарифма, віднято вже поза степенем'), (f'y = log{SUBL[a]}(x {"−" if c > 0 else "+"} {abs(c)})', 'замість показникової функції записано логарифм'), (f'y = x^{a} {"−" if c > 0 else "+"} {abs(c)}', 'показникову функцію сплутано зі степеневою')]
        return T.add(lv, f'Знайдіть функцію, обернену до функції y = log{SUBL[a]} x {sg(c)} {abs(c)}.', ans, wr, 'з рівності log_a x = y − c маємо x = a^(y − c)', f'y = log{SUBL[a]} x {sg(c)} {abs(c)} ⇒ log{SUBL[a]} x = y {"−" if c > 0 else "+"} {abs(c)} ⇒ x = {a}^(y {"−" if c > 0 else "+"} {abs(c)}); міняємо x і y: {ans}')
    k = rng.choice([2, 3, 4, 5]); c = rng.choice([v for v in range(-6, 7) if v])
    ans = f'y = {k}/(x {"−" if c > 0 else "+"} {abs(c)})' if False else None
    # y = k/x + c  →  y = k/(x − c)
    ans = f'y = {k}/(x {"−" if c > 0 else "+"} {abs(c)})'
    wr = [(f'y = {k}/(x {"+" if c > 0 else "−"} {abs(c)})', 'константу перенесено зі знаком, що не відповідає зворотній дії'), (f'y = {k}/x {"−" if c > 0 else "+"} {abs(c)}', 'число віднято вже після ділення, а не в знаменнику'), (f'y = (x {"−" if c > 0 else "+"} {abs(c)})/{k}', 'дріб записано перевернутим'), (f'y = {k}x {"−" if c > 0 else "+"} {abs(c)}', 'дріб k/x замінено добутком kx')]
    return T.add(lv, f'Знайдіть функцію, обернену до функції y = {k}/x {sg(c)} {abs(c)}.', ans, wr, 'із y = k/x + c: k/x = y − c ⇒ x = k/(y − c)', f'y = {k}/x {sg(c)} {abs(c)} ⇒ {k}/x = y {"−" if c > 0 else "+"} {abs(c)} ⇒ x = {k}/(y {"−" if c > 0 else "+"} {abs(c)}); міняємо x і y: {ans}')

def f_line_two_points(T, rng, lv):
    k = rng.choice([-4, -3, -2, 2, 3, 4, 5, F(1, 2), F(-1, 2), F(3, 2), F(-3, 2)]); b = rng.choice([v for v in range(-8, 9) if v])
    kk = F(k)
    step = kk.denominator
    x1 = rng.randint(-3, 2) * step; x2 = x1 + step * rng.randint(1, 3)
    y1 = kk * x1 + b; y2 = kk * x2 + b
    kind = rng.choice(['kb', 'sum', 'eq'])
    if kind == 'eq':
        def rend(kv, bv):
            kv = F(kv)
            ks = '' if kv == 1 else (M if kv == -1 else ffmt(kv) if kv.denominator == 1 else f'{ffmt(kv)}·')
            ks = ('' if kv == 1 else M if kv == -1 else (fmt(kv) if kv.denominator == 1 else f'({ffmt(kv)})'))
            return f'y = {ks}x {sg(bv)} {fmt(abs(bv))}'
        ans = rend(kk, b)
        wr = [(rend(kk, -b), 'вільний член b знайдено з протилежним знаком'), (rend(-kk, b), 'кутовий коефіцієнт знайдено зі знаком мінус (різниці взято в різному порядку)'), (rend(1 / kk, b), 'кутовий коефіцієнт перевернуто (Δx/Δy)'), (rend(kk, y1), 'за вільний член узято ординату першої точки')]
        return T.add(lv, f'Пряма проходить через точки A({fmt(x1)}; {ffmt(y1)}) та B({fmt(x2)}; {ffmt(y2)}). Запишіть рівняння цієї прямої.', ans, wr, 'спочатку k = Δy/Δx, потім b із підстановки однієї точки', f'k = ({ffmt(y2)} − {pn_f(y1)})/({fmt(x2)} − {pn(x1)}) = {ffmt(kk)}; b = {ffmt(y1)} − ({ffmt(kk)})·{pn(x1)} = {fmt(b)}; {ans}')
    if kind == 'kb':
        ans = kk * 0 + F(b)
        wr = [(F(-b), 'знак b змінено'), (kk, 'знайдено кутовий коефіцієнт, а не вільний член'), (F(y1), 'за b узято ординату першої точки'), (y1 + kk * x1, 'добуток kx додано до y замість віднімання'), (F(y2), 'за b узято ординату другої точки')]
        return T.add(lv, f'Графік функції y = kx + b проходить через точки A({fmt(x1)}; {ffmt(y1)}) та B({fmt(x2)}; {ffmt(y2)}). Знайдіть b.', ans, wr, 'спочатку знайдіть k, потім підставте координати однієї точки', f'k = {ffmt(kk)}; b = y₁ − k·x₁ = {ffmt(y1)} − ({ffmt(kk)})·{pn(x1)} = {fmt(b)}')
    ans = kk + b
    wr = [(kk * b, 'знайдено добуток k·b замість суми'), (kk - b, 'вільний член віднято замість додавання'), (F(b), 'знайдено лише b'), (kk, 'знайдено лише k')]
    return T.add(lv, f'Графік функції y = kx + b проходить через точки A({fmt(x1)}; {ffmt(y1)}) та B({fmt(x2)}; {ffmt(y2)}). Знайдіть k + b.', ans, wr, 'спочатку знайдіть k і b окремо, лише потім додайте', f'k = {ffmt(kk)}, b = {fmt(b)}; k + b = {ffmt(ans)}')

def f_line_param(T, rng, lv):
    kind = rng.choice(['par', 'perp', 'inter', 'pt'])
    if kind in ('par', 'perp'):
        k1 = rng.choice([2, 3, 4, -2, -3, 5]); aa = rng.choice([2, 3, 4, 5])
        # прямі y = k1 x + 1 та y = (a·m) x + 3, шукаємо m... простіше: y = (a + c)x
        c = rng.randint(-4, 4)
        if kind == 'par':
            a = k1 - c
            txt = f'При якому значенні a прямі y = {poly([k1, 3])} та y = (a {sg(c)} {abs(c)})x − 2 паралельні?'.replace(' + 0', '')
            wr = [(F(-k1 - c), 'прирівняно кутовий коефіцієнт до протилежного числа'), (F(k1 + c), 'вільний член c додано замість віднімання'), (F(-1, k1) - c, 'застосовано умову перпендикулярності'), (F(k1), 'не враховано доданок c у коефіцієнті')]
            return T.add(lv, txt, F(a), wr, 'паралельні прямі мають рівні кутові коефіцієнти (вільні члени різні)', f'k₁ = k₂: {fmt(k1)} = a {sg(c)} {abs(c)} ⇒ a = {fmt(a)}') if c else False
        # perp
        k1 = rng.choice([2, 4, -2, -4, 5, -5, 1, -1]); 
        k2 = F(-1, k1); a = k2 - c
        txt = f'При якому значенні a прямі y = {poly([k1, 3])} та y = (a {sg(c)} {abs(c)})x − 2 перпендикулярні?'
        wr = [(F(k1) - c, 'застосовано умову паралельності'), (F(1, k1) - c, 'знак у k₁·k₂ = −1 не враховано'), (F(-k1) - c, 'взято протилежне число, але не обернене'), (k2 + c, 'вільний член c додано замість віднімання')]
        return T.add(lv, txt, a, wr, 'k₁·k₂ = −1: кутові коефіцієнти перпендикулярних прямих обернені за модулем і протилежні за знаком', f'{fmt(k1)}·(a {sg(c)} {abs(c)}) = −1 ⇒ a {sg(c)} {abs(c)} = {ffmt(k2)} ⇒ a = {ffmt(a)}') if c else False
    if kind == 'inter':
        x0 = rng.randint(-4, 4); y0 = rng.randint(-6, 6)
        k1, k2 = rng.sample([-3, -2, -1, 1, 2, 3, 4], 2)
        b1 = y0 - k1 * x0; b2 = y0 - k2 * x0
        ans = f'({fmt(x0)}; {fmt(y0)})'
        wr = [(f'({fmt(y0)}; {fmt(x0)})', 'координати точки записано в оберненому порядку'), (f'({fmt(-x0)}; {fmt(y0)})', 'знак абсциси переплутано (при розв’язуванні k₁x + b₁ = k₂x + b₂ вільні члени перенесено без зміни знаку)'), (f'({fmt(x0)}; {fmt(b1)})', 'за ординату взято вільний член першої прямої')]
        if x0 == 0 or y0 == 0 or x0 == y0 or x0 == -y0: return False
        wr.append((f'({fmt(x0)}; {fmt(b2)})', 'за ординату взято вільний член другої прямої'))
        return T.add(lv, f'Знайдіть координати точки перетину прямих {ys(k1, b1)} та {ys(k2, b2)}.', ans, wr, 'прирівняйте праві частини, знайдіть x, потім підставте його в одне з рівнянь', f'{poly([k1, b1])} = {poly([k2, b2])} ⇒ x = {fmt(x0)}; y = {fmt(k1)}·{pn(x0)} {sg(b1)} {fmt(abs(b1))} = {fmt(y0)}')
    # pt: пряма проходить через точку — знайти параметр
    k = rng.choice([2, 3, -2, -3, 4]); x0 = rng.choice([-3, -2, -1, 1, 2, 3]); y0 = rng.randint(-8, 8)
    a = F(y0 - 3 * 1, x0) if False else None
    m = rng.choice([v for v in range(-4, 5) if v]); a = rng.randint(-5, 5)
    # y = (a−m)·... : y = a x + m·x? просто: пряма y = (a + k)x − 1 проходить через (x0, y0)
    y0 = (a + k) * x0 - 1
    ans = F(a)
    wr = [(F(y0 - 1, x0) - k, 'вільний член −1 перенесено без зміни знака'), (F(y0 + 1, x0), 'не враховано доданок k у коефіцієнті'), (F(y0 + 1, x0) + k, 'коефіцієнт (a + k) знайдено, але k додано замість віднімання'), (F(y0, x0) - k, 'не враховано вільний член −1')]
    return T.add(lv, f'При якому значенні a пряма y = (a {sg(k)} {abs(k)})x − 1 проходить через точку M({fmt(x0)}; {fmt(y0)})?', ans, wr, 'підставте координати точки, потім розв’яжіть отримане рівняння відносно a', f'{fmt(y0)} = (a {sg(k)} {abs(k)})·{pn(x0)} − 1 ⇒ a {sg(k)} {abs(k)} = {ffmt(F(y0 + 1, x0))} ⇒ a = {fmt(a)}')

def f_line_area(T, rng, lv):
    k = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4, 6]); b = rng.choice([v for v in range(-12, 13) if v and v % k == 0])
    xi = F(-b, k)
    ans = F(abs(b) * abs(xi), 2)
    wr = [(F(abs(b) * abs(xi)), 'площу прямокутника взято замість трикутника (не поділено на 2)'), (F(abs(b) + abs(xi), 2), 'катети додано замість множення'), (F(abs(b) + abs(xi)), 'знайдено суму катетів'), (F(abs(b) * abs(xi), 4), 'площу поділено на 4')]
    return T.add(lv, f'Пряма {ys(k, b)} разом з осями координат утворює трикутник. Знайдіть його площу.', ans, wr, 'катети — відрізки осей від початку координат до точок перетину: |b| та |b/k|', f'вісь Oy: (0; {fmt(b)}), вісь Ox: ({fmt(xi)}; 0); S = ½·{fmt(abs(b))}·{fmt(abs(xi))} = {ffmt(ans)}')

def fac(r): return 'x' if r == 0 else f'(x {"−" if r > 0 else "+"} {abs(r)})'

def f_quad_a(T, rng, lv):
    kind = rng.choice(['vp', 'vp', 'bc', 'zeros'])
    A_ = lambda a: '' if a == 1 else (M if a == -1 else fmt(a))
    if kind == 'vp':
        a = rng.choice([-3, -2, -1, 2, 3, 4]); m = rng.choice([v for v in range(-4, 5) if v]); n_ = rng.choice([v for v in range(-6, 7) if v])
        p = m + rng.choice([-3, -2, -1, 1, 2, 3]); q = a * (p - m) ** 2 + n_
        ans = F(a)
        wr = [(F(q - n_), 'не поділено на (p − m)²'), (F(q + n_, (p - m) ** 2), 'ординату вершини додано замість віднімання'), (F(q - n_, abs(p - m)), 'різницю абсцис не піднесено до квадрата'), (-F(a), 'знак a змінено')]
        return T.add(lv, f'Парабола y = a{fac(m)}² {sg(n_)} {abs(n_)} проходить через точку ({fmt(p)}; {fmt(q)}). Знайдіть a.', ans, wr, 'підставте координати точки: a = (y − y₀)/(x − x₀)²', f'{fmt(q)} = a·({fmt(p)} {"−" if m > 0 else "+"} {abs(m)})² {sg(n_)} {abs(n_)} ⇒ a = {fmt(q - n_)}/{(p - m) ** 2} = {fmt(a)}')
    if kind == 'bc':
        a = rng.choice([-2, -1, 1, 2, 3]); m = rng.choice([v for v in range(-4, 5) if v]); n_ = rng.choice([v for v in range(-6, 7) if v])
        b = -2 * a * m; c = a * m * m + n_
        ask = rng.choice(['b', 'c', 'sum']); vtxt = f'({fmt(m)}; {fmt(n_)})'
        head = f'Парабола y = {A_(a)}x² + bx + c має вершину в точці {vtxt}.'
        if ask == 'b':
            ans = F(b); wr = [(F(-b), 'знак b змінено (x₀ = −b/(2a))'), (F(b, 2 * a), 'за b взято абсцису вершини зі знаком, протилежним до потрібного: b = −2a·x₀'), (F(b * 2), 'коефіцієнт b подвоєно'), (F(c), 'названо вільний член')]
            return T.add(lv, head + ' Знайдіть b.', ans, wr, 'x₀ = −b/(2a) ⇒ b = −2a·x₀', f'b = −2·{pn(a)}·{pn(m)} = {fmt(b)}')
        if ask == 'c':
            ans = F(c); wr = [(F(n_), 'вільний член прийнято за ординату вершини'), (F(c - 2 * n_), 'ординату вершини віднято замість додавання'), (F(-c), 'знак c змінено'), (F(a * m * m), 'не додано ординату вершини')]
            return T.add(lv, head + ' Знайдіть c.', ans, wr, 'c = y(0) = a·x₀² + y₀', f'c = {pn(a)}·{pn(m)}² {sg(n_)} {abs(n_)} = {fmt(c)}')
        ans = F(b + c); wr = [(F(c - b), 'коефіцієнт b взято з протилежним знаком'), (F(b), 'знайдено лише b'), (F(c), 'знайдено лише c'), (F(b * c), 'знайдено добуток b·c')]
        return T.add(lv, head + ' Знайдіть b + c.', ans, wr, 'b = −2a·x₀, c = a·x₀² + y₀', f'b = {fmt(b)}, c = {fmt(c)}; b + c = {fmt(b + c)}')
    r1, r2 = rng.sample(range(-5, 6), 2); a = rng.choice([-2, -1, 2, 3])
    px = rng.choice([v for v in range(-6, 7) if v not in (r1, r2)])
    py = a * (px - r1) * (px - r2)
    ans = F(a)
    wr = [(F(py), 'не поділено на добуток (p − x₁)(p − x₂)'), (F(py, (px + r1) * (px + r2)) if (px + r1) * (px + r2) else F(7), 'нулі взято з протилежним знаком'), (F(py, abs((px - r1) * (px - r2))), 'знак добутку не враховано'), (F(-a), 'знак a змінено')]
    return T.add(lv, f'Парабола y = a{fac(r1)}{fac(r2)} проходить через точку ({fmt(px)}; {fmt(py)}). Знайдіть a.', ans, wr, 'підставте координати точки у форму a(x − x₁)(x − x₂)', f'{fmt(py)} = a·({fmt(px)} − {pn(r1)})({fmt(px)} − {pn(r2)}) ⇒ a = {fmt(py)}/{fmt((px - r1) * (px - r2))} = {fmt(a)}')

def f_quad_signs(T, rng, lv):
    a = rng.choice([-1, 1]); b = rng.choice([-1, 0, 1]); c = rng.choice([-1, 1])
    desc = []
    desc.append('гілки параболи напрямлені ' + ('вгору' if a > 0 else 'вниз'))
    desc.append('парабола перетинає вісь Oy ' + ('вище' if c > 0 else 'нижче') + ' від початку координат')
    if b == 0: desc.append('вершина параболи лежить на осі Oy')
    else:
        pos = (-b / a) > 0 
        desc.append('вершина параболи розташована ' + ('праворуч' if pos else 'ліворуч') + ' від осі Oy')
    def s3(a_, b_, c_):
        sym = lambda v: '> 0' if v > 0 else ('< 0' if v < 0 else '= 0')
        return f'a {sym(a_)}, b {sym(b_)}, c {sym(c_)}'
    ans = s3(a, b, c)
    wr = [(s3(-a, b if b == 0 else -b, c), 'знаки a і b змінено (a вгору/вниз і положення вершини переплутано)'), (s3(a, b if b == 0 else -b, c), 'знак b визначено навпаки: він залежить від a і положення вершини (x₀ = −b/(2a))'), (s3(a, b, -c), 'знак c визначено навпаки: c — ордината точки перетину з Oy'), (s3(-a, -b if b else 0, -c), 'усі знаки визначено навпаки')]
    if b == 0: wr[0] = (s3(-a, 0, c), 'напрям гілок параболи визначено навпаки'); wr[1] = (s3(a, 1, c), 'вершина на осі Oy означає x₀ = 0, тобто b = 0'); wr[3] = (s3(-a, 0, -c), 'напрям гілок і знак c визначено навпаки')
    sl = f'a {"> 0" if a > 0 else "< 0"} (гілки {"вгору" if a > 0 else "вниз"}); c = y(0) {"> 0" if c > 0 else "< 0"}; x₀ = −b/(2a) ' + ('= 0 ⇒ b = 0' if b == 0 else f'{"> 0" if -b / a > 0 else "< 0"}, а оскільки a {"> 0" if a > 0 else "< 0"}, b {"< 0" if b < 0 else "> 0"}')
    return T.add(lv, f'Графік функції y = ax² + bx + c має такі властивості: {desc[0]}; {desc[1]}; {desc[2]}. Які знаки мають коефіцієнти a, b, c?', ans, wr, 'a — напрям гілок, c — ордината перетину з Oy, b — з положення вершини: x₀ = −b/(2a)', sl)

def f_quad_word(T, rng, lv):
    kind = rng.choice(['proj', 'proj_t', 'fence', 'wall', 'profit'])
    if kind in ('proj', 'proj_t'):
        v = rng.choice([10, 15, 20, 25, 30, 40]); h0 = rng.choice([0, 0, 5, 10, 15, 20])
        # h(t) = -5t^2 + v t + h0
        t_top = F(v, 10); hmax = F(-5) * t_top * t_top + v * t_top + h0
        if kind == 'proj':
            ans = hmax
            wr = [(F(h0) + v * t_top, 'у h(t₀) не враховано доданок −5t²'), (F(-5) * (F(v, 5)) ** 2 + v * F(v, 5) + h0, 'підставлено t = v/5 (подвоєний час підйому) замість t = v/10'), (t_top, 'знайдено час досягнення найбільшої висоти, а не саму висоту'), (hmax - h0 if h0 else hmax + 5, 'не враховано початкову висоту' if h0 else 'допущено арифметичну помилку при обчисленні h(t₀)')]
            txt = f'Тіло кинули вертикально вгору з висоти {h0} м із початковою швидкістю {v} м/с. Висота (у метрах) над землею змінюється за формулою h(t) = {h0} + {v}t − 5t² (t — час у секундах).' if h0 else f'Тіло кинули вертикально вгору з початковою швидкістю {v} м/с. Висота (у метрах) над землею змінюється за формулою h(t) = {v}t − 5t² (t — час у секундах).'
            return T.add(lv, txt + ' Знайдіть найбільшу висоту, на яку підніметься тіло (у метрах).', ans, wr, 'найбільше значення квадратичної функції — в її вершині t₀ = −b/(2a)', f't₀ = {v}/10 = {ffmt(t_top)} с; h(t₀) = {ffmt(hmax)} м')
        ans = t_top
        wr = [(F(v, 5), 'знайдено час польоту до повернення на початкову висоту (подвоєний час підйому)'), (F(v, 20), 'у знаменнику взято 20 замість 10'), (F(v), 'за час узято коефіцієнт при t'), (hmax, 'знайдено найбільшу висоту, а не час її досягнення')]
        txt = f'Висота тіла (у метрах), кинутого вгору, змінюється за формулою h(t) = {h0 + 0 if h0 else ""}{" + " if h0 else ""}{v}t − 5t². Через скільки секунд тіло досягне найбільшої висоти?'.replace('h(t) = ' + ('' if not h0 else ''), 'h(t) = ')
        return T.add(lv, txt, ans, wr, 'найбільша висота — у вершині параболи: t₀ = −b/(2a)', f't₀ = −{v}/(2·(−5)) = {ffmt(t_top)} с')
    if kind == 'fence':
        P = rng.choice([40, 48, 60, 80, 100, 120]); side = F(P, 4); ans = side * side
        wr = [(F(P, 2) ** 2, 'за сторону взято півпериметр P/2'), (F(P, 2) * side, 'взято прямокутник зі сторонами P/2 і P/4'), (side, 'знайдено сторону квадрата, а не площу'), (ans * 2, 'площу квадрата подвоєно')]
        return T.add(lv, f'Із сітки завдовжки {P} м потрібно огородити прямокутну ділянку якомога більшої площі (з усіх чотирьох сторін). Яка найбільша площа (у м²)?', ans, wr, 'серед прямокутників з даним периметром найбільшу площу має квадрат', f'сторона квадрата {P}/4 = {ffmt(side)} м; S = {ffmt(side)}² = {ffmt(ans)} м²')
    if kind == 'wall':
        P = rng.choice([40, 60, 80, 100, 120, 160]); ans = F(P * P, 8)
        wr = [(F(P * P, 16), 'ділянку взято квадратною (сторона P/4), а стіна дозволяє довшу сторону'), (F(P, 4), 'знайдено меншу сторону ділянки'), (F(P, 2), 'знайдено довжину сторони вздовж стіни, а не площу'), (F(P, 2) ** 2, 'обидві сторони взято по P/2')]
        return T.add(lv, f'Ділянку прямокутної форми потрібно огородити сіткою завдовжки {P} м із трьох сторін, а четвертою стороною буде стіна. Яка найбільша площа ділянки (у м²)?', ans, wr, 'S = x(P − 2x), де x — сторона, перпендикулярна стіні; максимум при x = P/4', f'x({P} − 2x) має найбільше значення при x = {ffmt(F(P, 4))}: S = {ffmt(F(P, 4))}·{ffmt(F(P, 2))} = {ffmt(ans)} м²')
    # profit
    p0 = rng.choice([20, 30, 40, 50]); k = rng.choice([2, 4, 5]); c = rng.choice([4, 5, 8, 10])
    # прибуток (ціна x, продано p0·k − k·x ... ) спрощено: P(x) = (x − c)(A − k x)
    A = rng.choice([100, 120, 150, 200]); 
    # q = A − k x ; x ціна ; витрати c на штуку
    f = lambda x: (x - c) * (A - k * x)
    xv = F(A + k * c, 2 * k)
    if xv.denominator != 1: return False
    ans = f(xv)
    wr = [(f(F(A, 2 * k)), 'знайдено прибуток при ціні найбільшої виручки, без урахування собівартості'), (F(A * A, 4 * k), 'знайдено найбільшу виручку замість прибутку'), ((xv + c) * (A - k * xv), 'собівартість додано до ціни замість віднімання'), (xv, 'названо оптимальну ціну, а не прибуток')]
    return T.add(lv, f'Магазин продає товар за ціною x грн, собівартість одиниці — {c} грн, а кількість проданих за день одиниць дорівнює {A} − {k}x. Знайдіть найбільший можливий денний прибуток (у грн).', ans, wr, 'прибуток = (ціна − собівартість)·кількість; це парабола з гілками вниз, максимум у вершині', f'P(x) = (x − {c})({A} − {k}x); вершина x₀ = ({A} + {k * c})/(2·{k}) = {fmt(xv)}; P(x₀) = {fmt(ans)} грн')

def f_symmetry(T, rng, lv):
    items = [('відносно осі Ox', '−f(x)', 'y = −f(x)'), ('відносно осі Oy', 'f(−x)', 'y = f(−x)'), ('відносно початку координат', '−f(−x)', 'y = −f(−x)')]
    ft = rng.choice([('y = 2ˣ', {'Ox': 'y = −2ˣ', 'Oy': 'y = 2⁻ˣ', 'O': 'y = −2⁻ˣ'}), ('y = log₂ x', {'Ox': 'y = −log₂ x', 'Oy': 'y = log₂(−x)', 'O': 'y = −log₂(−x)'}), ('y = √x', {'Ox': 'y = −√x', 'Oy': 'y = √(−x)', 'O': 'y = −√(−x)'}), ('y = x² + x', {'Ox': 'y = −x² − x', 'Oy': 'y = x² − x', 'O': 'y = −x² + x'}), ('y = x² − 2x', {'Ox': 'y = −x² + 2x', 'Oy': 'y = x² + 2x', 'O': 'y = −x² − 2x'}), ('y = 3ˣ', {'Ox': 'y = −3ˣ', 'Oy': 'y = 3⁻ˣ', 'O': 'y = −3⁻ˣ'}), ('y = x³ − 3x²', {'Ox': 'y = −x³ + 3x²', 'Oy': 'y = −x³ − 3x²', 'O': 'y = x³ + 3x²'}), ('y = √(x + 2)', {'Ox': 'y = −√(x + 2)', 'Oy': 'y = √(2 − x)', 'O': 'y = −√(2 − x)'})])
    name, res = ft
    ax = rng.choice(['Ox', 'Oy', 'O'])
    word = {'Ox': 'відносно осі Ox', 'Oy': 'відносно осі Oy', 'O': 'відносно початку координат'}[ax]
    ans = res[ax]
    cand = [res['Ox'], res['Oy'], res['O']]
    wr = []
    for other, rsn in (('Ox', 'це графік, симетричний відносно осі Ox (змінюється знак функції)'), ('Oy', 'це графік, симетричний відносно осі Oy (змінюється знак аргументу)'), ('O', 'це графік, симетричний відносно початку координат (змінюються обидва знаки)')):
        if other != ax: wr.append((res[other], rsn))
    # додаткова хибна: початкова функція
    wr.append((name, 'це сама початкова функція: графік не змінено'))
    wr.append((name + ' + 1' if False else name.replace('y = ', 'y = 1/('), 'взято обернену величину'))
    wr = [(v, r) for v, r in wr if v != ans and not v.startswith('y = 1/(')]
    rule = {'Ox': 'відносно Ox: y → −y, тобто y = −f(x)', 'Oy': 'відносно Oy: x → −x, тобто y = f(−x)', 'O': 'відносно початку: y = −f(−x)'}[ax]
    return T.add(lv, f'Графік функції {name} симетрично відобразили {word}. Яка формула задає отриманий графік?', ans, wr, 'Ox → мінус перед функцією; Oy → мінус перед x; початок координат → обидва мінуси', rule + f'; отримуємо {ans}')

# ----- прогресії L2 -----
def f_ap_find_n(T, rng, lv):
    a1 = rng.randint(-20, 20); d = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 7]); n_ = rng.randint(8, 30)
    an = a1 + (n_ - 1) * d
    ans = F(n_)
    wr = [(F(n_ - 1), 'різницю (an − a₁)/d взято без додавання 1 (номер на 1 менший)'), (F(n_ + 1), 'до (an − a₁)/d додано 2 замість 1'), (F(an - a1, d) * 2 if (an - a1) % d == 0 else F(n_ + 2), 'номер знайдено як подвоєну кількість кроків'), (F(an - a1), 'різницю an − a₁ не поділено на d')]
    return T.add(lv, f'В арифметичній прогресії a₁ = {fmt(a1)}, d = {fmt(d)}. Який номер має член, що дорівнює {fmt(an)}?', ans, wr, 'a_n = a₁ + (n − 1)d ⇒ n = (a_n − a₁)/d + 1', f'{fmt(an)} = {fmt(a1)} + (n − 1)·{pn(d)} ⇒ n − 1 = {fmt((n_ - 1))} ⇒ n = {n_}')

def f_ap_sign(T, rng, lv):
    kind = rng.choice(['neg', 'first_pos'])
    d = rng.choice([2, 3, 4, 5, 6, 7]); 
    if kind == 'neg':
        a1 = -rng.randint(10, 60)
        while a1 % d == 0: a1 = -rng.randint(10, 60)
        # a_n < 0 ⇔ a1 + (n-1)d < 0 ⇔ n < (d - a1)/d
        cnt = (-a1 - 1) // d + 1 
        # перевірка прямим підрахунком
        cnt = sum(1 for n in range(1, 200) if a1 + (n - 1) * d < 0)
        ans = F(cnt)
        wr = [(F(cnt + 1), 'враховано також перший невід’ємний член'), (F(cnt - 1), 'не враховано останній від’ємний член'), (F(-a1 // d), 'знайдено цілу частину частки |a₁|/d без урахування, що номер членів починається з 1'), (F(cnt + 2), 'кількість визначено з похибкою на 2')]
        return T.add(lv, f'В арифметичній прогресії a₁ = {fmt(a1)}, d = {fmt(d)}. Скільки від’ємних членів має ця прогресія?', ans, wr, 'розв’яжіть нерівність a₁ + (n − 1)d < 0 і візьміть натуральні n (строга нерівність)', f'{fmt(a1)} + (n − 1)·{d} < 0 ⇒ n − 1 < {ffmt(F(-a1, d))} ⇒ n ≤ {cnt}')
    a1 = -rng.randint(10, 60)
    first = next(n for n in range(1, 200) if a1 + (n - 1) * d > 0)
    ans = F(first)
    wr = [(F(first - 1), 'за перший додатний узято останній недодатний член'), (F(first + 1), 'додано зайвий крок'), (F(-a1 // d), 'знайдено цілу частину частки |a₁|/d без урахування, що номер членів починається з 1'), (F(first + 2), 'номер визначено з похибкою')]
    return T.add(lv, f'В арифметичній прогресії a₁ = {fmt(a1)}, d = {fmt(d)}. Який номер має перший додатний член цієї прогресії?', ans, wr, 'розв’яжіть нерівність a₁ + (n − 1)d > 0 і візьміть найменше натуральне n', f'{fmt(a1)} + (n − 1)·{d} > 0 ⇒ n − 1 > {ffmt(F(-a1, d))} ⇒ n = {first}')

def f_ap_sum_formula(T, rng, lv):
    p = rng.choice([1, 2, 3]); q = rng.choice([v for v in range(-6, 8) if v]); k = rng.randint(4, 9)
    Sn = lambda n: p * n * n + q * n
    ak = Sn(k) - Sn(k - 1)
    ans = F(ak)
    wr = [(F(Sn(k)), 'за член взято суму перших k членів'), (F(Sn(k) - Sn(k + 1)), 'різницю сум взято в оберненому порядку (S_k − S_{k+1})'), (F(Sn(k - 1)), 'знайдено суму перших k − 1 членів'), (F(Sn(k) - Sn(k - 2)), 'з S_k віднято S_{k−2} (це сума двох членів)')]
    return T.add(lv, f'Сума перших n членів арифметичної прогресії задається формулою S_n = {poly([p, q, 0], "n")}. Знайдіть a{sub(k)}.', ans, wr, 'a_k = S_k − S_(k−1)', f'S_{k} = {fmt(Sn(k))}, S_{k - 1} = {fmt(Sn(k - 1))}; a_{k} = {fmt(Sn(k))} − {pn(Sn(k - 1))} = {fmt(ak)}')

def f_ap_sum_range(T, rng, lv):
    a1 = rng.randint(-8, 10); d = rng.choice([2, 3, 4, -2, -3, 5]); p = rng.randint(2, 5); q = p + rng.randint(3, 6)
    terms = [a1 + (i - 1) * d for i in range(p, q + 1)]
    ans = F(sum(terms)); cnt = q - p + 1
    Sq = q * (2 * a1 + (q - 1) * d) // 2; Sp = (p - 1) * (2 * a1 + (p - 2) * d) // 2; Sp2 = p * (2 * a1 + (p - 1) * d) // 2
    wr = [(F(Sq - Sp2), f'від S_{q} віднято S_{p} (член a_{p} не потрапив до суми)'), (F(Sq), f'знайдено суму перших {q} членів'), (F(Sq - Sp + terms[0]), f'до правильної суми додано зайвий член a_{p}'), (F(cnt * (terms[0] + terms[-1])), 'суму не поділено на 2')]
    return T.add(lv, f'В арифметичній прогресії a₁ = {fmt(a1)}, d = {fmt(d)}. Знайдіть суму членів від a{sub(p)} до a{sub(q)} включно.', ans, wr, f'сума від a_p до a_q дорівнює S_q − S_(p−1)', f'членів {cnt}: перший {fmt(terms[0])}, останній {fmt(terms[-1])}; сума = ({fmt(terms[0])} {sg(terms[-1])} {fmt(abs(terms[-1]))})/2·{cnt} = {fmt(ans)}')

def cx(c): return 'x' if c == 1 else (M + 'x' if c == -1 else fmt(c) + 'x')

def f_ap_mean(T, rng, lv):
    kind = rng.choice(['mean', 'mean', 'quad'])
    d = rng.choice([-4, -3, -2, 2, 3, 5]); m = rng.randint(-6, 8)
    if kind == 'mean':
        a, c = m - d, m + d
        ans = F(m)
        wr = [(F(a * c), 'знайдено добуток крайніх чисел'), (F(c - a), 'знайдено різницю крайніх чисел'), (F(a + c), 'не поділено суму крайніх на 2'), (F(m + d), 'за середній член узято наступний член прогресії')]
        return T.add(lv, f'Числа {fmt(a)}, x, {fmt(c)} (у цьому порядку) утворюють арифметичну прогресію. Знайдіть x.', ans, wr, 'середній член арифметичної прогресії — середнє арифметичне сусідніх', f'x = ({fmt(a)} {sg(c)} {fmt(abs(c))})/2 = {fmt(m)}')
    # x+a, 2x+b, ... : рівність 2(2x+b) = (x+a) + (3x + c)
    x0 = rng.randint(-5, 7); a_ = rng.randint(-4, 4); k2, k3 = rng.choice([(2, 3), (3, 5), (2, 4)]); 
    # терми: x + a_, k2*x + b_, k3*x + c_ ; потрібна рівність 2(k2 x + b_) = (x + a_) + (k3 x + c_)  => (2k2 - 1 - k3) x = a_ + c_ - 2 b_
    coef = 2 * k2 - 1 - k3
    if coef == 0: return False
    b_ = rng.randint(-4, 4); c_ = 2 * b_ - a_ + coef * x0
    t1, t2, t3 = f'x {sg(a_)} {abs(a_)}' if a_ else 'x', f'{k2}x {sg(b_)} {abs(b_)}' if b_ else f'{k2}x', f'{k3}x {sg(c_)} {abs(c_)}' if c_ else f'{k3}x'
    ans = F(x0)
    wr = [(F(-x0), 'знак розв’язку змінено'), (F(a_ + c_ - 2 * b_, coef + 1) if coef + 1 else F(1), 'коефіцієнти при x зведено неправильно'), (F(a_ + c_ + 2 * b_, coef) , 'знаки вільних членів у рівності 2a₂ = a₁ + a₃ переплутано'), (F(x0 + 1), 'допущено арифметичну помилку при розв’язанні лінійного рівняння')]
    return T.add(lv, f'Числа {t1}; {t2}; {t3} (у цьому порядку) утворюють арифметичну прогресію. Знайдіть x.', ans, wr, 'умова: 2·a₂ = a₁ + a₃', f'2({t2}) = ({t1}) + ({t3}) ⇒ {cx(coef)} = {fmt(a_ + c_ - 2 * b_)} ⇒ x = {fmt(x0)}')

def chs(m): return 'числа' if m in (2, 3, 4) else 'чисел'

def f_ap_insert(T, rng, lv):
    d = rng.choice([-4, -3, -2, 2, 3, 4, 5]); a1 = rng.randint(-10, 10); m = rng.randint(2, 6)
    last = a1 + (m + 1) * d
    kind = rng.choice(['d', 'sum'])
    if kind == 'd':
        ans = F(d)
        wr = [(F(last - a1, m), f'різницю поділено на {m} (кількість вставлених), а треба на {m + 1}'), (F(last - a1, m + 2), f'різницю поділено на {m + 2}'), (F(a1 - last, m + 1), 'крайні числа віднято в оберненому порядку'), (F(last - a1), 'різницю крайніх чисел не поділено на кількість кроків')]
        return T.add(lv, f'Між числами {fmt(a1)} та {fmt(last)} вставили {m} {chs(m)} так, що всі числа утворили арифметичну прогресію. Знайдіть різницю цієї прогресії.', ans, wr, f'з {m} вставленими числами всього {m + 2} членів і {m + 1} кроків', f'{fmt(last)} = {fmt(a1)} + {m + 1}·d ⇒ d = {fmt(d)}')
    ins = [a1 + i * d for i in range(1, m + 1)]; ans = F(sum(ins))
    wr = [(F(sum(ins) + a1 + last), 'до суми вставлених додано крайні числа'), (F(m * (a1 + last)), 'суму не поділено на 2'), (F((a1 + last) * (m + 2), 2), 'знайдено суму всіх членів, включно з крайніми'), (F(sum(ins) - ins[0]), 'до суми не включено перше вставлене число')]
    return T.add(lv, f'Між числами {fmt(a1)} та {fmt(last)} вставили {m} {chs(m)} так, що всі числа утворили арифметичну прогресію. Знайдіть суму вставлених чисел.', ans, wr, 'сума вставлених = сума всіх членів мінус крайні (або (a₁ + a_n)/2 · m)', f'вставлені числа: {", ".join(fmt(v) for v in ins)}; сума {fmt(ans)}')

def f_gp_sum(T, rng, lv):
    q = rng.choice([2, 3, -2, F(1, 2), F(-1, 2), 4]); b1 = rng.choice([1, 2, 3, 5, -2]); n_ = rng.randint(3, 6)
    if isinstance(q, F): b1 *= 2 ** n_
    qq = F(q)
    S = F(b1) * (qq ** n_ - 1) / (qq - 1)
    bn = F(b1) * qq ** (n_ - 1)
    wr = [(F(b1) * (qq ** n_ + 1) / (qq + 1) if qq != -1 else F(0), 'у формулі суми взято (qⁿ + 1)/(q + 1) замість (qⁿ − 1)/(q − 1)'), (F(b1) * (qq ** (n_ - 1) - 1) / (qq - 1), 'у формулі показник взято n − 1 замість n'), (F(b1) * (1 - qq ** n_) / (qq - 1), 'у чисельнику формули порядок членів переплутано (1 − qⁿ замість qⁿ − 1)'), (bn, 'знайдено n-й член прогресії, а не суму')]
    return T.add(lv, f'Знайдіть суму перших {n_} членів геометричної прогресії, якщо b₁ = {fmt(b1)}, q = {ffmt(qq)}.', S, wr, 'S_n = b₁(qⁿ − 1)/(q − 1)', f'S_{n_} = {fmt(b1)}·(({ffmt(qq)})^{n_} − 1)/({ffmt(qq)} − 1) = {ffmt(S)}')

def f_gp_inf(T, rng, lv):
    kind = rng.choice(['sum', 'q', 'dec'])
    if kind == 'sum':
        q = rng.choice([F(1, 2), F(1, 3), F(-1, 2), F(2, 3), F(1, 4), F(-1, 3), F(3, 4), F(1, 5)]); b1 = rng.choice([3, 4, 6, 8, 9, 12, 15])
        S = F(b1) / (1 - q)
        wr = [(F(b1) / (1 + q), 'у знаменнику взято 1 + q замість 1 − q'), (F(b1) / q, 'у знаменнику взято q замість 1 − q'), (F(b1) * (1 - q), 'замість ділення на (1 − q) помножено на нього'), (F(b1), 'за суму взято перший член')]
        return T.add(lv, f'Знайдіть суму нескінченної спадної геометричної прогресії, якщо b₁ = {fmt(b1)}, q = {ffmt(q)}.', S, wr, 'S = b₁/(1 − q), коли |q| < 1', f'S = {fmt(b1)}/(1 − {pn_f(q)}) = {ffmt(S)}')
    if kind == 'q':
        q = rng.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(-1, 2)]); b1 = rng.choice([6, 8, 12, 18, 24]); S = F(b1) / (1 - q)
        wr = [(1 - F(S, b1), 'з формули S = b₁/(1 − q) помилково отримано q = 1 − S/b₁'), (F(b1) / S, 'знайдено відношення b₁/S, а це 1 − q'), (1 - q, 'знайдено 1 − q замість q'), (-q, 'знак q змінено')]
        return T.add(lv, f'Сума нескінченної спадної геометричної прогресії дорівнює {ffmt(S)}, а перший член — {fmt(b1)}. Знайдіть знаменник прогресії.', q, wr, 'S = b₁/(1 − q) ⇒ 1 − q = b₁/S ⇒ q = 1 − b₁/S', f'1 − q = {fmt(b1)}/{ffmt(S)} = {ffmt(1 - q)} ⇒ q = {ffmt(q)}')
    # періодичний дріб
    nd = rng.choice([1, 2]); digs = rng.randint(1, 9) if nd == 1 else rng.choice([12, 27, 36, 45, 18, 54, 63, 81, 15])
    val = F(digs, 10 ** nd - 1)
    txt = f'0,({digs:0{nd}d})'
    wr = [(F(digs, 10 ** nd), 'період поділено на 10ⁿ замість 10ⁿ − 1'), (F(digs, 10 ** nd + 1), 'у знаменнику взято 10ⁿ + 1'), (F(digs, 10 ** nd - 1) * 10, 'результат помножено на 10'), (F(digs, 10 ** nd - 2), 'у знаменнику взято 10ⁿ − 2')]
    return T.add(lv, f'Запишіть нескінченний періодичний десятковий дріб {txt} у вигляді звичайного дробу (скоротіть його, якщо можливо; відповідь запишіть як a/b).', val, wr, 'це сума нескінченно спадної геометричної прогресії зі знаменником 10⁻ⁿ', f'{txt} = {digs}/{10 ** nd - 1} = {ffmt(val)}')

def f_gp_mean(T, rng, lv):
    q = rng.choice([2, 3, -2, 4, F(1, 2), 5]); b = rng.choice([1, 2, 3, 4, 5, 6])
    if isinstance(q, F): b *= 2
    a_ = F(b) / q; c = F(b) * q
    kind = rng.choice(['pos', 'abs'])
    ans = F(b)
    pr = a_ * c  # = b^2
    wr = [(F(a_ + c, 2), 'знайдено середнє арифметичне замість середнього геометричного'), (-F(b), 'знак результату змінено'), (pr, 'знайдено добуток крайніх чисел (це b²)'), (F(c - a_), 'знайдено різницю крайніх чисел')]
    if q < 0: 
        return T.add(lv, f'Числа {ffmt(a_)}, x, {ffmt(c)} (у цьому порядку) утворюють геометричну прогресію. Знайдіть x.', ans, wr + [(-ans, 'вибрано від’ємний корінь, хоча він не відповідає знаку прогресії')], 'x² = a·c, але знак x визначається чергуванням знаків прогресії (з q < 0 знаки чергуються)', f'x² = {ffmt(a_)}·({ffmt(c)}) = {ffmt(pr)}·(−1)... ') if False else False
    return T.add(lv, f'Числа {ffmt(a_)}, x, {ffmt(c)} утворюють геометричну прогресію з додатними членами. Знайдіть x.', ans, wr, 'b₂² = b₁·b₃, а при додатних членах x = √(b₁·b₃)', f'x² = {ffmt(a_)}·{ffmt(c)} = {ffmt(pr)} ⇒ x = {fmt(b)}')

def f_gp_find_n(T, rng, lv):
    q = rng.choice([2, 3, F(1, 2), 4, 5]); b1 = rng.choice([1, 2, 3, 5]); n_ = rng.randint(4, 9)
    if isinstance(q, F): b1 *= 2 ** n_
    qq = F(q); bn = F(b1) * qq ** (n_ - 1)
    ans = F(n_)
    wr = [(F(n_ - 1), 'показник n − 1 прийнято за номер n'), (F(n_ + 1), 'до номера додано 2 замість 1'), (F(n_ * 2), 'номер подвоєно'), (F(n_ - 2), 'номер взято на 2 менше')]
    return T.add(lv, f'У геометричній прогресії b₁ = {fmt(b1)}, q = {ffmt(qq)}. Який номер має член, що дорівнює {ffmt(bn)}?', ans, wr, 'b_n = b₁·q^(n−1): знайдіть показник n − 1, потім n', f'{ffmt(bn)} = {fmt(b1)}·({ffmt(qq)})^(n−1) ⇒ ({ffmt(qq)})^(n−1) = {ffmt(bn / b1)} ⇒ n − 1 = {n_ - 1} ⇒ n = {n_}')

def f_gp_q_terms(T, rng, lv):
    q = rng.choice([2, 3, F(1, 2), 4, F(1, 3), F(2, 3)]); p = rng.randint(1, 3); k = rng.choice([2, 3]); qq = F(q)
    b1 = rng.choice([1, 2, 3, 5]) * (q.denominator ** (p + k) if isinstance(q, F) else 1)
    bp = F(b1) * qq ** (p - 1); bq = F(b1) * qq ** (p - 1 + k)
    ans = qq
    ratio = bq / bp
    wr = [(ratio, f'із частки не добуто кореня степеня {k}'), (bq - bp, 'знайдено різницю, а не частку'), (bp / bq, 'частку перевернуто'), (ratio ** F(1, 1) / k if False else ratio / k, f'частку поділено на {k} замість добування кореня')]
    return T.add(lv, f'У геометричній прогресії з додатними членами b{sub(p)} = {ffmt(bp)}, b{sub(p + k)} = {ffmt(bq)}. Знайдіть знаменник прогресії.', ans, wr, f'b_(p+k)/b_p = q^k: знаменник — корінь степеня {k} із частки', f'q^{k} = {ffmt(bq)}/{ffmt(bp)} = {ffmt(ratio)} ⇒ q = {ffmt(qq)} (члени додатні)')

# ----- показникова / логарифмічна функції L2 -----
def f_exp_point(T, rng, lv):
    kind = rng.choice(['base', 'val', 'asym', 'mono'])
    if kind == 'base':
        a = rng.choice([2, 3, 4, 5, F(1, 2), F(1, 3), F(2, 3)]); p = rng.choice([2, 3, 4, -1, -2])
        a = F(a); q = a ** p
        ans = a
        wr = [(1 / a, 'основу знайдено оберненою: помилково враховано знак показника'), (q ** F(1, 1) / p if False else q / p, 'значення функції поділено на показник замість добування кореня'), (F(q), 'основою названо саме значення функції'), (q - p, 'від значення функції віднято показник')]
        pt = f'({p}; {ffmt(q)})'
        return T.add(lv, f'Графік показникової функції y = aˣ проходить через точку {pt}. Знайдіть a.', ans, wr, 'підставте координати: q = a^p, звідки a = q^(1/p)', f'a^{p} = {ffmt(q)} ⇒ a = {ffmt(a)}'.replace('^-', '^−'))
    if kind == 'val':
        a = rng.choice([2, 3, 5]); p = rng.randint(2, 4); q = a ** p
        ans = F(1, q)
        wr = [(F(-q), 'знак показника сприйнято як знак значення'), (F(q), 'f(−p) прийнято рівним f(p)'), (F(1, a * p), 'степінь замінено множенням'), (F(-p * a), 'показник від’ємного аргументу перемножено з основою')]
        return T.add(lv, f'Графік функції y = aˣ проходить через точку ({p}; {q}). Знайдіть значення функції при x = −{p}.', ans, wr, 'a^(−p) = 1/a^p', f'a^{p} = {q} ⇒ a = {a}; f(−{p}) = {a}^(−{p}) = 1/{q}')
    if kind == 'asym':
        a = rng.choice([2, 3, 5]); c = rng.choice([v for v in range(-6, 7) if v])
        ans = f'y = {fmt(c)}'
        wr = [(f'y = {fmt(-c)}', 'знак числа c переплутано'), ('y = 0', 'не враховано вертикальний зсув на ' + fmt(c)), (f'x = {fmt(c)}', 'асимптоту показникової функції названо вертикальною прямою'), (f'y = {a}', 'за асимптоту взято основу степеня')]
        return T.add(lv, f'Яка пряма є горизонтальною асимптотою графіка функції y = {a}ˣ {sg(c)} {abs(c)}?', ans, wr, 'aˣ → 0 при x → −∞ (a > 1), тому графік прямує до y = c', f'при x → −∞ значення {a}ˣ → 0, тому y → {fmt(c)}')
    kind2 = rng.choice(['exp', 'log'])
    a = rng.choice([2, 3, 5])
    if kind2 == 'exp':
        ans = f'a > 3'; k = rng.choice([1, 2, 3, 4])
        # y = (a - k)^x зростає ⇔ a - k > 1 ⇔ a > k+1
        ans = setstr([(F(k + 1), None, False, False)])
        wr = [(setstr([(F(k), None, False, False)]), f'враховано лише додатність основи (a − {k} > 0), а для зростання потрібно a − {k} > 1'), (setstr([(F(k), F(k + 1), False, False)]), 'знайдено значення a, при яких функція спадає'), (setstr([(None, F(k + 1), False, False)]), 'знак нерівності обрано протилежний (основа більша за 1 — функція зростає)'), (setstr([(F(k + 1), None, True, False)]), f'при a − {k} = 1 функція стала (y = 1), тому знак строгий')]
        return T.add(lv, f'При яких значеннях a функція y = (a − {k})ˣ є зростаючою?', ans, wr, 'показникова функція зростає, коли основа більша за 1', f'a − {k} > 1 ⇒ a > {k + 1}')
    k = rng.choice([1, 2, 3, 4])
    ans = setstr([(F(k), F(k + 1), False, False)])
    wr = [(setstr([(None, F(k + 1), False, False)]), f'враховано лише умову a − {k} < 1, а умову a − {k} > 0 (основа додатна) не враховано'), (setstr([(F(k + 1), None, False, False)]), 'знайдено значення a, при яких функція зростає'), (setstr([(F(0), F(1), False, False)]), 'за основу взято a, а не вираз a − ' + str(k)), (setstr([(F(k), F(k + 1), True, True)]), f'при a = {k} основа дорівнює 0, а при a = {k + 1} — дорівнює 1: такі значення a не підходять, тому дужки круглі')]
    return T.add(lv, f'При яких значеннях a функція y = log_(a − {k}) x є спадною?', ans, wr, 'логарифмічна функція спадає, коли основа між 0 і 1', f'0 < a − {k} < 1 ⇒ {k} < a < {k + 1}')

def pw(b, e):
    b = F(b); e = F(e)
    bs = fmt(b) if b.denominator == 1 else f'({ffmt(b)})'
    return f'{bs}{sup(e.numerator)}' if e.denominator == 1 else f'{bs}^({ffmt(e)})'

def f_compare_order(T, rng, lv):
    pool = []
    for base in (2, 3, 5): pool.append((f'{base}^({rng.choice(["0,5", "1,5", "−1", "2", "−2", "0,3"])})', None))
    items = []
    spec = rng.choice(['pow', 'log', 'mix'])
    def val_pow(b, e): return float(b) ** float(e)
    cand = []
    if spec in ('pow', 'mix'):
        for b in (2, 3, F(1, 2), F(1, 3), F(2, 3), 5, F(3, 2), 10):
            for e in (F(1, 2), F(3, 2), -1, 2, -2, F(1, 3), F(-1, 2), 3):
                cand.append((pw(b, e), float(b) ** float(e)))
    if spec in ('log', 'mix'):
        for b in (2, 3, 5, F(1, 2), F(1, 3), 10):
            for x in (2, 3, 4, 5, 8, F(1, 2), F(1, 4), 9, 7):
                cand.append((f'log{SUBL.get(b, "_(" + ffmt(b) + ")")} {ffmt(x)}', math.log(float(x)) / math.log(float(b))))
    pick = rng.sample(cand, 3)
    def binof(v): return 0 if v < 0 else (1 if v < 1 else (2 if v < 2 else 3))
    BIN = ['менше за 0', 'між 0 і 1', 'між 1 і 2', 'більше за 2']
    if len(set(binof(v) for _, v in pick)) < 3 or any(abs(v - round(v)) < 0.05 for _, v in pick): return False
    names = [n for n, _ in pick]
    order = sorted(pick, key=lambda t: t[1])
    ans = ' < '.join(n for n, _ in order)
    wr = [(' < '.join(n for n, _ in reversed(order)), 'порядок обернено (за спаданням замість зростання)'), (' < '.join([order[1][0], order[0][0], order[2][0]]), f'помилково поставлено {order[1][0]} перед {order[0][0]}'), (' < '.join([order[0][0], order[2][0], order[1][0]]), f'помилково поставлено {order[2][0]} перед {order[1][0]}'), (' < '.join([order[2][0], order[0][0], order[1][0]]), f'найбільше число {order[2][0]} помилково поставлено на перше місце')]
    approx = '; '.join(f'{n} — {BIN[binof(v)]}' for n, v in order)
    return T.add(lv, f'Розташуйте числа {names[0]}, {names[1]}, {names[2]} у порядку зростання.', ans, wr, 'для a > 1 більшому показнику відповідає більше значення, для 0 < a < 1 — менше; для логарифмів — аналогічно за основою', f'оцінимо кожне число відносно 0, 1, 2: {approx}')

# ----- тригонометрія L2 -----
def f_trig_amplitude(T, rng, lv):
    A = rng.choice([2, 3, 4, 5, -2, -3, -4]); k = rng.choice([1, 2, 3, 4, F(1, 2), F(1, 3)]); d = rng.choice([-3, -2, -1, 0, 1, 2, 3, 4]); fn = rng.choice(['sin', 'cos'])
    kk = F(k)
    arg = 'x' if kk == 1 else (f'{kk.numerator}x' if kk.denominator == 1 else f'x/{kk.denominator}')
    expr = f'{"−" if A < 0 else ""}{abs(A)}{fn}({arg})' if kk != 1 else f'{"−" if A < 0 else ""}{abs(A)}{fn} x'
    if d: expr += f' {sg(d)} {abs(d)}'
    what = rng.choice(['max', 'min', 'per', 'amp'])
    if what == 'max':
        ans = F(abs(A) + d)
        wr = [(F(A + d), 'найбільше значення прийнято за A + d, хоча A < 0 (потрібно взяти |A| + d)') if A < 0 else (F(abs(A)), 'не враховано вертикальний зсув d'), (F(d - abs(A)), 'знайдено найменше значення замість найбільшого'), (F(abs(A) * (1 + d)), 'зсув d помножено на амплітуду'), (F(abs(A) + abs(d)), 'зсув додано за модулем')]
        if A > 0 and d == 0: return False
        return T.add(lv, f'Знайдіть найбільше значення функції y = {expr}.', ans, wr, 'найбільше значення: |A| + d (sin і cos набувають значень від −1 до 1)', f'−1 ≤ {fn}(…) ≤ 1, тому найбільше значення дорівнює {abs(A)} {sg(d)} {abs(d)} = {fmt(ans)}')
    if what == 'min':
        ans = F(d - abs(A))
        wr = [(F(d + abs(A)), 'знайдено найбільше значення замість найменшого'), (F(-abs(A)), 'не враховано вертикальний зсув d'), (F(d + A), 'знак множника A прийнято за знак найменшого значення без перевірки'), (F(-(abs(A) + d)), 'знак результату змінено')]
        if d == 0: return False
        return T.add(lv, f'Знайдіть найменше значення функції y = {expr}.', ans, wr, 'найменше значення: d − |A|', f'найменше значення дорівнює {fmt(d)} − {abs(A)} = {fmt(ans)}')
    if what == 'per':
        base = F(2) / kk; ans = base
        wr = [(base * kk * kk, f'період множили на k'), (F(2), 'коефіцієнт при x не враховано'), (base / 2, 'період зайвий раз поділено на 2'), (F(1) / kk, 'взято період π/k (як у tg)'), (base * 2, 'період подвоєно')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції y = {expr}.', pim(ans), wr, 'період функції A·sin(kx) + d дорівнює 2π/|k| (A і d його не змінюють)', f'T = 2π/{ffmt(kk)} = {pim(ans)}')
    ans = F(abs(A))
    wr = [(F(abs(A) + d), 'до амплітуди додано зсув d'), (F(2 * abs(A)), 'взято розмах (різницю найбільшого та найменшого), а не амплітуду'), (F(d), 'за амплітуду взято вертикальний зсув'), (F(A), 'амплітуда не може бути від’ємною: це |A|')]
    if A > 0: wr[3] = (F(abs(A) * kk), 'амплітуду помножено на коефіцієнт k при x')
    return T.add(lv, f'Знайдіть амплітуду коливання, заданого функцією y = {expr}.', ans, wr, 'амплітуда дорівнює |A|', f'амплітуда {abs(A)}')

def f_reduction(T, rng, lv):
    fn = rng.choice(['sin', 'cos', 'tg', 'ctg']); shift = rng.choice([90, 180, 270, 360]); sgn = rng.choice([1, -1])
    if shift == 360 and sgn == 1: shift = 180
    th = 0.37
    def num(f, x):
        return {'sin': math.sin(x), 'cos': math.cos(x), 'tg': math.tan(x), 'ctg': 1 / math.tan(x)}[f]
    val = num(fn, math.radians(shift) + sgn * th)
    cands = [(sg_, f2) for f2 in ('sin', 'cos', 'tg', 'ctg') for sg_ in (1, -1)]
    right = [c for c in cands if abs(sg_val(c, th, num) - val) < 1e-9]
    if len(right) != 1: return False
    rs, rf = right[0]
    def nm(c): return ('−' if c[0] < 0 else '') + c[1] + ' α'
    shift_txt = {90: 'π/2', 180: 'π', 270: '3π/2', 360: '2π'}[shift]
    use_deg = rng.random() < .4
    shift_s = f'{shift}°' if use_deg else shift_txt
    arg = f'{shift_s} {"+" if sgn > 0 else "−"} α'
    co = {'sin': 'cos', 'cos': 'sin', 'tg': 'ctg', 'ctg': 'tg'}
    wr = []
    wr.append(((-rs, rf), 'знак у цій чверті визначено неправильно'))
    wr.append(((rs, co[rf]), 'неправильно визначено, чи змінюється назва функції (π/2 і 3π/2 — змінюється, π і 2π — ні)'))
    wr.append(((-rs, co[rf]), 'і назву функції, і знак визначено неправильно'))
    wr.append(((rs, rf) if False else (1 if rs > 0 else -1, {'sin': 'tg', 'cos': 'ctg', 'tg': 'sin', 'ctg': 'cos'}[rf]), 'взято зовсім іншу функцію'))
    changes = rf != fn
    q = {90: 'II' if sgn > 0 else 'I', 180: 'III' if sgn > 0 else 'II', 270: 'IV' if sgn > 0 else 'III', 360: 'I' if sgn > 0 else 'IV'}[shift]
    sl = f'{shift_s} {"+" if sgn > 0 else "−"} α при малому α лежить у {q} чверті, де {fn} {"додатний" if (num(fn, math.radians(shift) + sgn * th) > 0) else "від’ємний"}; ' + ('назва функції змінюється' if changes else 'назва функції не змінюється') + f'; отже {fn}({arg}) = {nm(right[0])}'
    return T.add(lv, f'Спростіть вираз {fn}({arg}), α — гострий кут.', nm(right[0]), [(nm(w), r) for w, r in wr], 'кут π/2 і 3π/2 змінюють назву функції на кофункцію; π і 2π — ні; знак визначає чверть вихідної функції', sl)
def sg_val(c, th, num): return c[0] * num(c[1], th)

def f_trig_identity(T, rng, lv):
    s_, c_, h = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 35, 37)])
    quad = rng.choice([1, 2, 3, 4]); known = rng.choice(['sin', 'cos']); ask = rng.choice(['cos' if False else 'other', 'tg', 'sin2', 'cos2'])
    S = F(s_, h) * (1 if quad in (1, 2) else -1); C = F(c_, h) * (1 if quad in (1, 4) else -1)
    if known == 'cos' and False: pass
    qn = {1: '(0; π/2)', 2: '(π/2; π)', 3: '(π; 3π/2)', 4: '(3π/2; 2π)'}[quad]
    qn_name = {1: 'першій', 2: 'другій', 3: 'третій', 4: 'четвертій'}[quad]
    if known == 'sin': given = f'sin α = {ffmt(S)}'; kv, ov, on = S, C, 'cos α'; known_s = 'sin α'
    else: given = f'cos α = {ffmt(C)}'; kv, ov, on = C, S, 'sin α'; known_s = 'cos α'
    head = f'Відомо, що {given}, α ∈ {qn} ({qn_name} чверті).'
    pos = lambda v: v > 0
    if ask == 'other':
        ans = ov
        wr = [(-ov, f'знак {on} у {qn_name} чверті визначено неправильно'), (1 - abs(kv), f'замість √(1 − {known_s}²) обчислено 1 − |{known_s}|'), (1 - kv * kv, f'замість √(1 − {known_s}²) обчислено 1 − {known_s}² (корінь не добуто)'), (abs(ov) * F(h, c_ if known == "sin" else s_) * 1 if False else abs(kv) ** 2 , f'знайдено {known_s}² замість {on}')]
        return T.add(lv, head + f' Знайдіть {on}.', ans, wr, f'з основної тотожності {on}² = 1 − {known_s}², знак визначає чверть', f'{on}² = 1 − ({ffmt(kv)})² = {ffmt(ov * ov)} ⇒ {on} = ±{ffmt(abs(ov))}; у {qn_name} чверті {on} {"додатний" if ov > 0 else "від’ємний"}: {ffmt(ov)}')
    if ask == 'tg':
        ans = S / C
        wr = [(-S / C, 'знак tg α визначено неправильно'), (C / S, 'знайдено ctg α замість tg α'), (S * C, 'tg α знайдено як добуток sin α·cos α'), (-C / S, 'знайдено ctg α з протилежним знаком')]
        return T.add(lv, head + ' Знайдіть tg α.', ans, wr, 'tg α = sin α/cos α; знак — за чвертю', f'sin α = {ffmt(S)}, cos α = {ffmt(C)}; tg α = {ffmt(S)} : ({ffmt(C)}) = {ffmt(ans)}')
    if ask == 'sin2':
        ans = 2 * S * C
        wr = [(-2 * S * C, 'знак sin 2α визначено неправильно (добуток sin α·cos α має знак за чвертю)'), (S * C, 'у формулі sin 2α = 2 sin α cos α пропущено множник 2'), (2 * S, 'sin 2α прийнято за 2 sin α'), (C * C - S * S, 'застосовано формулу cos 2α замість sin 2α')]
        return T.add(lv, head + ' Знайдіть sin 2α.', ans, wr, 'sin 2α = 2 sin α cos α', f'sin α = {ffmt(S)}, cos α = {ffmt(C)}; sin 2α = 2·({ffmt(S)})·({ffmt(C)}) = {ffmt(ans)}')
    ans = C * C - S * S
    wr = [(-(C * C - S * S), 'знак cos 2α змінено'), (2 * S * C, 'застосовано формулу sin 2α замість cos 2α'), (C - S, 'cos 2α прийнято за cos α − sin α'), (C * C + S * S if False else 1 - 2 * C * C, 'застосовано формулу 1 − 2cos²α, але вона для cos 2α має вигляд 2cos²α − 1')]
    return T.add(lv, head + ' Знайдіть cos 2α.', ans, wr, 'cos 2α = cos²α − sin²α = 1 − 2sin²α', f'cos 2α = ({ffmt(C)})² − ({ffmt(S)})² = {ffmt(ans)}')

def f_trig_addition(T, rng, lv):
    U_ = [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300]
    pairs = [((u + v) // 2, (u - v) // 2) for u in U_ for v in U_ if v < u and (u + v) % 2 == 0 and (u - v) // 2 >= 5 and (u + v) // 2 < 180]
    A, B = rng.choice(pairs)
    ok = lambda d: d % 30 == 0 or d % 45 == 0
    if not (ok(A + B) and ok(A - B)): return False
    kind = rng.choice(['sin+', 'sin-', 'cos+', 'cos-'])
    names = {'sin+': (f'sin {A}°·cos {B}° + cos {A}°·sin {B}°', 'sin', A + B), 'sin-': (f'sin {A}°·cos {B}° − cos {A}°·sin {B}°', 'sin', A - B), 'cos+': (f'cos {A}°·cos {B}° − sin {A}°·sin {B}°', 'cos', A + B), 'cos-': (f'cos {A}°·cos {B}° + sin {A}°·sin {B}°', 'cos', A - B)}
    expr, fn, ang = names[kind]
    ans, _, _ = trig_exact(fn, ang)
    wr = []
    for k2, (e2, f2, a2) in names.items():
        if k2 == kind: continue
        v, _, _ = trig_exact(f2, a2)
        wr.append((v, f'застосовано формулу {f2}({A}° {"+" if k2.endswith("+") else "−"} {B}°) = {f2} {a2}° (знаки у формулі переплутано)'))
    wr = [(v, r) for v, r in wr if v != ans]
    name = {'sin+': f'sin({A}° + {B}°)', 'sin-': f'sin({A}° − {B}°)', 'cos+': f'cos({A}° + {B}°)', 'cos-': f'cos({A}° − {B}°)'}[kind]
    return T.add(lv, f'Обчисліть: {expr}.', ans, wr, 'впізнайте формулу додавання: sin(a ± b) = sin a cos b ± cos a sin b; cos(a ± b) = cos a cos b ∓ sin a sin b', f'вираз дорівнює {name} = {fn} {ang}° = {ans}')

def f_piecewise(T, rng, lv):
    a = rng.choice([-3, -2, -1, 0, 1, 2]); k1 = rng.choice([2, 3, -1, -2, 1]); b1 = rng.randint(-4, 4); c2 = rng.choice([1, 2, -1, -2]); b2 = rng.randint(-5, 5)
    f1 = lambda x: k1 * x + b1; f2 = lambda x: c2 * x * x + b2
    f = lambda x: f1(x) if x < a else f2(x)
    xs = [a - rng.randint(1, 3), a + rng.randint(0, 3)]
    if xs[0] == xs[1]: return False
    r1, r2 = f(xs[0]), f(xs[1])
    txt = f'f(x) = {{ {poly([k1, b1])}, якщо x < {fmt(a)}; {poly([c2, 0, b2])}, якщо x ≥ {fmt(a)} }}'
    if lv == 1:
        x0 = xs[0] if rng.random() < .5 else xs[1]; r0 = f(x0)
        wh0 = 'x < ' + fmt(a) if x0 < a else 'x ≥ ' + fmt(a)
        other = f2(x0) if x0 < a else f1(x0)
        wr = [(other, 'застосовано не ту формулу (умову на x проігноровано)'), (-r0, 'знак результату змінено'), (r0 + (1 if r0 + 1 != other else 2), 'допущено арифметичну помилку при обчисленні')]
        wr.append((f1(x0) + f2(x0), 'додано значення за обома формулами'))
        return T.add(lv, f'Функцію задано формулою {txt}. Знайдіть f({fmt(x0)}).', r0, wr, 'спочатку з’ясуйте, до якого проміжку належить x, потім використайте відповідну формулу', f'{fmt(x0)} задовольняє умову {wh0}, тому f({fmt(x0)}) = {fmt(r0)}')
    ans = F(r1 + r2)
    wr = [(f1(xs[0]) + f1(xs[1]), 'обидва значення знайдено за першою формулою'), (f2(xs[0]) + f2(xs[1]), 'обидва значення знайдено за другою формулою'), (f2(xs[0]) + f1(xs[1]), 'формули застосовано навпаки (умови проігноровано)'), (r1 - r2, 'значення віднято замість додавання')]
    wh = lambda x: 'x < ' + fmt(a) if x < a else 'x ≥ ' + fmt(a)
    return T.add(lv, f'Функцію задано формулою {txt}. Знайдіть f({fmt(xs[0])}) + f({fmt(xs[1])}).', ans, wr, 'спочатку з’ясуйте, до якого проміжку належить значення x, потім використайте відповідну формулу', f'{fmt(xs[0])} ({wh(xs[0])}): f = {fmt(r1)}; {fmt(xs[1])} ({wh(xs[1])}): f = {fmt(r2)}; сума {fmt(ans)}')

def f_parity_value(T, rng, lv):
    kind = rng.choice(['even', 'odd', 'sum'])
    a = rng.choice([2, 3, 4, 5, 6, 7]); v = rng.choice([v for v in range(-9, 10) if v])
    if kind == 'even':
        ans = F(v); wr = [(F(-v), 'функцію вважали непарною: f(−a) = −f(a), хоча вона парна'), (F(0), 'вважали, що значення в протилежних точках взаємно знищуються'), (F(2 * v), 'значення в точках a та −a додано'), (F(1, v), 'взято обернену величину')]
        return T.add(lv, f'Функція y = f(x) парна, f(−{a}) = {fmt(v)}. Знайдіть f({a}).', ans, wr, 'парна функція: f(−x) = f(x)', f'f({a}) = f(−{a}) = {fmt(v)}')
    if kind == 'odd':
        ans = F(-v); wr = [(F(v), 'функцію вважали парною: f(−a) = f(a), хоча вона непарна'), (F(0), 'вважали, що значення в протилежних точках взаємно знищуються'), (F(2 * v), 'значення в точках a та −a додано'), (F(1, v), 'взято обернену величину')]
        return T.add(lv, f'Функція y = f(x) непарна, f(−{a}) = {fmt(v)}. Знайдіть f({a}).', ans, wr, 'непарна функція: f(−x) = −f(x)', f'f({a}) = −f(−{a}) = {fmt(-v)}')
    b = rng.choice([v2 for v2 in range(-9, 10) if v2 and v2 != v]); a2 = rng.choice([x for x in (2, 3, 4, 5) if x != a])
    # f парна, g непарна: f(a)=v, g(a)=b → f(−a) + g(−a)
    ans = F(v - b)
    wr = [(F(v + b), 'обидві функції вважали парними'), (F(-v - b), 'обидві функції вважали непарними'), (F(-v + b), 'парність функцій переплутано (f — непарна, g — парна)'), (F(0), 'вважали, що значення при −a та a взаємно знищуються')]
    return T.add(lv, f'Функція f парна, а функція g непарна. Відомо, що f({a}) = {fmt(v)}, g({a}) = {fmt(b)}. Знайдіть f(−{a}) + g(−{a}).', ans, wr, 'f(−a) = f(a) (парна), g(−a) = −g(a) (непарна)', f'f(−{a}) = {fmt(v)}, g(−{a}) = {fmt(-b)}; сума {fmt(v)} {sg(-b)} {fmt(abs(b))} = {fmt(ans)}')

def f_recurrent(T, rng, lv):
    kind = rng.choice(['lin', 'mul', 'mix'])
    n_ = rng.randint(4, 7); a1 = rng.randint(-5, 6)
    if kind == 'lin':
        d = rng.choice([-4, -3, -2, 2, 3, 5]); seq = [a1]
        for _ in range(n_ - 1): seq.append(seq[-1] + d)
        ans = F(seq[-1])
        wr = [(F(seq[-1] + d), 'зроблено на один крок більше'), (F(seq[-2]), 'зроблено на один крок менше'), (F(a1 + n_ * d), 'використано a₁ + n·d замість (n − 1)·d'), (F(a1 * d if False else a1 + d * (n_ - 1) * 2), 'різницю додано двічі за кожен крок')]
        return T.add(lv, f'Послідовність задано рекурентно: a₁ = {fmt(a1)}, a_(n+1) = a_n {sg(d)} {abs(d)}. Знайдіть a{sub(n_)}.', ans, wr, 'це арифметична прогресія з різницею d: a_n = a₁ + (n − 1)d', f'a_n = {fmt(a1)} + {n_ - 1}·{pn(d)} = {fmt(seq[-1])}')
    if kind == 'mul':
        q = rng.choice([2, 3, -2]); a1 = rng.choice([1, 2, 3, -1]); seq = [a1]
        for _ in range(n_ - 1): seq.append(seq[-1] * q)
        ans = F(seq[-1])
        wr = [(F(seq[-1] * q), 'зроблено на один крок більше'), (F(seq[-2]), 'зроблено на один крок менше'), (F(a1 * q * (n_ - 1)), 'степінь замінено множенням'), (F(a1 + q * (n_ - 1)), 'прогресію сплутано з арифметичною')]
        return T.add(lv, f'Послідовність задано рекурентно: a₁ = {fmt(a1)}, a_(n+1) = {fmt(q)}·a_n. Знайдіть a{sub(n_)}.', ans, wr, 'це геометрична прогресія: a_n = a₁·q^(n−1)', f'a_n = {fmt(a1)}·({fmt(q)})^{n_ - 1} = {fmt(seq[-1])}')
    p, c = rng.choice([2, 3]), rng.choice([-3, -2, -1, 1, 2, 3]); n_ = rng.randint(4, 5); seq = [a1]
    for _ in range(n_ - 1): seq.append(p * seq[-1] + c)
    ans = F(seq[-1])
    wr = [(F(seq[-1] * p + c), 'зроблено на один крок більше'), (F(seq[-2]), 'зроблено на один крок менше'), (F(p * seq[-2] - c), 'вільний член c додано з протилежним знаком'), (F(p * a1 + c) if n_ > 2 else F(seq[0]), 'виконано лише один крок рекурентності')]
    return T.add(lv, f'Послідовність задано рекурентно: a₁ = {fmt(a1)}, a_(n+1) = {p}a_n {sg(c)} {abs(c)}. Знайдіть a{sub(n_)}.', ans, wr, 'обчислюйте член за членом: a₂, a₃, …', f'послідовність: {", ".join(fmt(v) for v in seq)}; a_{n_} = {fmt(seq[-1])}')

def f_seq_formula(T, rng, lv):
    kind = rng.choice(['neg', 'term', 'min'])
    r1 = rng.randint(2, 6); r2 = r1 + rng.randint(3, 9)
    # a_n = (n - r1)(n - r2) = n² - (r1+r2) n + r1 r2
    co = [1, -(r1 + r2), r1 * r2]
    if kind == 'neg':
        cnt = sum(1 for n in range(1, 60) if (n - r1) * (n - r2) < 0); ans = F(cnt)
        wr = [(F(cnt + 2), 'враховано також члени, що дорівнюють нулю (кінці проміжку)'), (F(cnt + 1), 'не враховано, що при n = ' + str(r1) + ' та n = ' + str(r2) + ' члени дорівнюють нулю'), (F(r2 - r1), 'кількість знайдено як різницю коренів (не враховано, що кінці не входять)'), (F(cnt - 1), 'виключено ще один член')]
        return T.add(lv, f'Послідовність задано формулою a_n = {poly(co, "n")}. Скільки її членів від’ємні?', ans, wr, 'від’ємні члени — ті, що між коренями (n натуральне, строга нерівність)', f'a_n = (n − {r1})(n − {r2}) < 0 ⇒ {r1} < n < {r2}; натуральних n: {cnt}')
    if kind == 'term':
        n_ = rng.randint(5, 15); an = (n_ - r1) * (n_ - r2); ans = F(an)
        wr = [(F((n_ + 1 - r1) * (n_ + 1 - r2)), f'підставлено n = {n_ + 1}'), (F((n_ - 1 - r1) * (n_ - 1 - r2)), f'підставлено n = {n_ - 1}'), (F(n_ * n_ - (r1 + r2) * n_ - r1 * r2), 'знак вільного члена змінено'), (F(n_ * n_ + (r1 + r2) * n_ + r1 * r2), 'знак доданка з n змінено')]
        return T.add(lv, f'Послідовність задано формулою a_n = {poly(co, "n")}. Знайдіть a{sub(n_)}.', ans, wr, 'підставляйте номер n у формулу', f'a_{n_} = {n_}² {sg(co[1])} {abs(co[1])}·{n_} {sg(co[2])} {co[2]} = {fmt(an)}')
    # найменший член
    vals = {n: (n - r1) * (n - r2) for n in range(1, 40)}
    nmin = min(vals, key=lambda n: vals[n]); ans = F(vals[nmin])
    wr = [(F(vals[1]), 'за найменший взято перший член'), (F(-F((r2 - r1) ** 2, 4)) if (r2 - r1) % 2 else F(vals[nmin] - 1), 'значення в вершині параболи взято без урахування, що n — натуральне' if (r2 - r1) % 2 else 'знайдено значення при сусідньому номері, а не найменше'), (F(nmin), 'названо номер найменшого члена, а не сам член'), (F(vals[nmin + 2]), f'взято член з номером n = {nmin + 2}')]
    return T.add(lv, f'Послідовність задано формулою a_n = {poly(co, "n")}. Знайдіть найменший член цієї послідовності.', ans, wr, 'вершина параболи n₀ = −b/(2a); n має бути натуральним — перевірте найближчі натуральні значення', f'n₀ = {ffmt(F(r1 + r2, 2))}; найменший член — при n = {nmin}: a_{nmin} = {fmt(ans)}')
