import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mgen import *
import msvg as S
import math, itertools
from fractions import Fraction as F

T = Topic(3, 'rivnyannya')
M = MINUS
OPS = {'<': '<', '<=': '≤', '>': '>', '>=': '≥'}
OPP = {'<': '>', '<=': '>=', '>': '<', '>=': '<='}
TOG = {'<': '<=', '<=': '<', '>': '>=', '>=': '>'}

# ---------- загальні допоміжні ----------
def vs(*r):
    rr = sorted(set(F(x) for x in r))
    return '; '.join(fmt(x) for x in rr) if rr else 'коренів немає'
def expand(roots, lead=1):
    p = [lead]
    for r in roots:
        q = [0] * (len(p) + 1)
        for i, a in enumerate(p): q[i] += a; q[i + 1] += -a * r
        p = q
    return p
def fac(r, m=1):
    s = f'(x {M if r > 0 else "+"} {fmt(abs(r))})'.replace(f'x {M} 0', 'x').replace('x + 0', 'x') if r != 0 else 'x'
    return s + (sup(m) if m > 1 else '')
def lc2(a, b):
    out = ('' if a == 1 else (M if a == -1 else fmt(a))) + 'x'
    out += (' + ' if b > 0 else f' {M} ') + ('' if abs(b) == 1 else fmt(abs(b))) + 'y'
    return out
def pn(v): return f'({fmt(v)})' if F(v) < 0 else fmt(v)

# ---------- множини розв'язків ----------
def setstr(parts):
    if not parts: return 'розв’язків немає'
    out = []
    for lo, hi, lc, rc in parts:
        if lo is not None and lo == hi: out.append('{' + fmt(lo) + '}'); continue
        ls = '(−∞' if lo is None else ('[' if lc else '(') + fmt(lo)
        rs_ = '+∞)' if hi is None else fmt(hi) + (']' if rc else ')')
        out.append(f'{ls}; {rs_}')
    return ' ∪ '.join(out)
def mirror(parts):
    return [(None if hi is None else -hi, None if lo is None else -lo, rc, lc) for lo, hi, lc, rc in reversed(parts)]
def ray(op, t):
    return (None, t, False, op == '<=') if op in ('<', '<=') else (t, None, op == '>=', False)
def inpart(x, p):
    lo, hi, lc, rc = p
    if lo is not None and (x < lo or (x == lo and not lc)): return False
    if hi is not None and (x > hi or (x == hi and not rc)): return False
    return True
def int_list(parts, lo=-80, hi=80):
    return [x for x in range(lo, hi + 1) if any(inpart(F(x), p) for p in parts)]

def solve_gen(num, den, lead, op):
    """lead·∏(x−r)^m / ∏(x−s)^k  op 0;  num, den — {корінь: кратність}."""
    num = dict(num); den = dict(den)
    crit = sorted(set(num) | set(den))
    want = 1 if op in ('>', '>=') else -1
    non = op in ('<=', '>=')
    def sg(x):
        s = 1 if lead > 0 else -1
        for r, m in list(num.items()) + list(den.items()):
            if x < r and m % 2: s = -s
        return s
    atoms = []; bounds = [None] + crit + [None]
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        if lo is None and hi is None: pr = F(0)
        elif lo is None: pr = hi - 1
        elif hi is None: pr = lo + 1
        else: pr = (lo + hi) / F(2)
        atoms.append(('s', lo, hi, sg(F(pr)) == want))
        if i < len(crit):
            c = crit[i]
            atoms.append(('p', c, c, (c in num) and (c not in den) and non))
    groups = []; cur = None
    for a in atoms:
        if a[3]:
            if cur is None: cur = [a, a]
            else: cur[1] = a
        elif cur: groups.append(cur); cur = None
    if cur: groups.append(cur)
    res = []
    for f, l in groups:
        lo, lc = (f[1], True) if f[0] == 'p' else (f[1], False)
        hi, rc = (l[1], True) if l[0] == 'p' else (l[2], False)
        res.append((lo, hi, lc, rc))
    return res

def set_wrongs(num, den, lead, op, fn=False):
    sol = solve_gen(num, den, lead, op)
    strict = op in ('<', '>')
    wr = [(setstr(solve_gen(num, den, lead, OPP[op])), 'розглянуто проміжки, де вираз має протилежний знак'),
          (setstr(solve_gen(num, den, lead, TOG[op])), ('нерівність строга, тому нулі функції в розв’язок не входять' if fn else 'нерівність строга, тому нулі виразу в розв’язок не входять') if strict else ('нерівність нестрога, тому нулі функції входять у розв’язок' if fn else 'нерівність нестрога, тому нулі чисельника входять у розв’язок'))]
    if den:
        n2 = dict(num); n2.update({k: 1 for k in den})
        wr.append((setstr(solve_gen(n2, {}, lead, op)), 'нуль знаменника включено до розв’язку, а на нуль ділити не можна'))
    wr.append((setstr(mirror(sol)), 'знаки коренів змінено на протилежні'))
    pts = [(F(r), F(r), True, True) for r in sorted(num)]
    wr.append((setstr(pts), 'знайдено лише нулі функції, а не розв’язок нерівності' if fn else 'знайдено лише нулі виразу, а не розв’язок нерівності'))
    return sol, wr

# ===================== РІВЕНЬ 1 =====================
def f_lin_eq(T, rng, lv):
    k = rng.choice(['two', 'brk', 'frac'])
    if k == 'two':
        a, c = rng.sample(range(2, 9), 2); x = rng.choice([v for v in range(-7, 9) if v]); b = rng.choice([v for v in range(-9, 10) if v])
        d = a * x + b - c * x
        if d == 0: return False
        wr = [(F(d + b, a - c), 'вільний член лівої частини перенесено без зміни знака'),
              (F(d - b, a + c), 'доданок із x із правої частини перенесено без зміни знака'),
              (F(b - d, a - c), 'різницю вільних членів взято у зворотному порядку'),
              (F(d - b, a), 'доданок із x із правої частини не враховано під час ділення')]
        return T.add(lv, f'Розв’яжіть рівняння: {poly([a, b])} = {poly([c, d])}.', x, wr, 'доданки з x — в одну частину, числа — в іншу; при перенесенні змінюємо знак', f'({a} − {c})x = {d} − ({b}); x = {fmt(x)}')
    if k == 'brk':
        a = rng.randint(2, 6); b = rng.choice([v for v in range(-6, 7) if v]); c = rng.choice([v for v in range(1, 6) if v != a]); x = rng.randint(-5, 7)
        d = a * (x + b) - c * x
        if d == 0: return False
        wr = [(F(d - b, a - c), f'дужку розкрито неправильно: {a} помножено лише на x'),
              (F(d + a * b, a - c), f'добуток {a}·({b}) перенесено без зміни знака'),
              (F(d - a * b, a + c), 'доданок із x із правої частини перенесено без зміни знака'),
              (F(a * b - d, a - c), 'різницю взято у зворотному порядку')]
        return T.add(lv, f'Розв’яжіть рівняння: {a}(x {"+" if b > 0 else M} {abs(b)}) = {poly([c, d])}.', x, wr, 'розкрийте дужки, помноживши a на кожен доданок', f'{a}x {"+" if a*b > 0 else M} {abs(a*b)} = {poly([c, d])}; {a - c}x = {fmt(d - a*b)}; x = {fmt(x)}')
    a = rng.randint(2, 6); b = rng.choice([v for v in range(-9, 10) if v]); m = rng.choice([v for v in range(-8, 9) if v]); r = m + b
    x0 = a * m
    wr = [(m, f'знайдено значення x/{a}, а не x'),
          (a * (r + b), f'доданок {fmt(b)} перенесено без зміни знака'),
          (a * r - b, f'на {a} помножено праву частину, але не доданок {fmt(b)}'),
          (F(m, a), f'замість множення на {a} виконано ділення')]
    return T.add(lv, f'Розв’яжіть рівняння: x/{a} {"+" if b > 0 else M} {abs(b)} = {fmt(r)}.', x0, wr, 'перенесіть число і помножте обидві частини на знаменник', f'x/{a} = {fmt(r)} − ({fmt(b)}) = {fmt(m)}; x = {a}·{pn(m)} = {fmt(x0)}')

def f_quad_roots(T, rng, lv):
    p, q = rng.sample([v for v in range(-9, 10) if v], 2)
    B, C = -(p + q), p * q; D = B * B - 4 * C; sD = math.isqrt(D)
    wr = [(vs(-p, -q), 'знак коефіцієнта b змінено (шукали корені x² − bx + c = 0)'),
          (vs(F(-B + D, 2), F(-B - D, 2)), 'корінь із дискримінанта не добуто'),
          (vs(-B + sD, -B - sD), 'у формулі коренів пропущено ділення на 2a')]
    D2 = B * B + 4 * C
    if D2 >= 0 and math.isqrt(D2) ** 2 == D2:
        s2 = math.isqrt(D2); wr.append((vs(F(-B + s2, 2), F(-B - s2, 2)), 'знак вільного члена змінено (розв’язано x² + bx − c = 0)'))
    wr.append((vs(1, C), 'корені підібрано лише за добутком, а суму не перевірено'))
    return T.add(lv, f'Розв’яжіть рівняння {poly([1, B, C])} = 0.', vs(p, q), wr, 'за теоремою Вієта: x₁ + x₂ = −b, x₁x₂ = c; або D = b² − 4c', f'D = {D}, √D = {sD}; x = ({-B} ± {sD})/2; корені {vs(p, q)}')

def f_incomplete(T, rng, lv):
    k = rng.choice(['x', 'sq', 'neg', 'sq2'])
    if k == 'x':
        a = rng.randint(1, 6); b = rng.choice([v for v in range(-12, 13) if v])
        r2 = F(-b, a)
        wr = [(vs(r2), 'обидві частини поділено на x, через що втрачено корінь x = 0'),
              (vs(0, -r2), 'знак другого кореня змінено'),
              (vs(-r2, r2), 'рівняння розв’язано як x² = c: отримано два симетричних корені'),
              (vs(0), 'розглянуто лише множник x, а другий множник не прирівняно до нуля')]
        return T.add(lv, f'Розв’яжіть рівняння {poly([a, b, 0])} = 0.', vs(0, r2), wr, 'винесіть x за дужки: x(ax + b) = 0 — добуток дорівнює нулю, коли один із множників нуль', f'x(ax + b) = 0; x = 0 або x = {fmt(r2)}')
    if k == 'sq':
        a = rng.choice([2, 3, 4, 5]); r = rng.randint(2, 9)
        wr = [(vs(r), 'від’ємний корінь втрачено'), (vs(-r * r, r * r), f'число {r*r} — це значення x², а не x'), (vs(r * r), f'рівняння x² = {r*r} розв’язано як x = {r*r}'), (vs(-a * r, a * r), f'коефіцієнт {a} не поділено, а помножено')]
        return T.add(lv, f'Розв’яжіть рівняння {a}x² = {a * r * r}.', vs(-r, r), wr, 'x² = c (c > 0) має два корені ±√c', f'x² = {r*r}; x = ±{r}')
    if k == 'neg':
        a = rng.randint(1, 9)
        wr = [(vs(-a, a), f'число {a*a} перенесено без зміни знака: отримано x² = {a*a}'), (vs(a), f'число {a*a} перенесено без зміни знака і втрачено від’ємний корінь'), (vs(0), f'доданок {a*a} відкинуто: x² = 0'), (vs(-a * a, a * a), f'число {a*a} прийнято за корінь')]
        return T.add(lv, f'Розв’яжіть рівняння x² + {a * a} = 0.', 'коренів немає', wr, 'квадрат дійсного числа невід’ємний, тому x² = від’ємне число розв’язків не має', f'x² = −{a*a} < 0')
    a = rng.randint(2, 11)
    wr = [(vs(a), 'другий корінь втрачено'), (vs(-a * a, a * a), f'число {a*a} — це значення x², а не x'), (vs(a * a), f'рівняння x² = {a*a} розв’язано як x = {a*a}'), (vs(0, a), 'різницю квадратів розкладено неправильно')]
    return T.add(lv, f'Розв’яжіть рівняння x² − {a * a} = 0.', vs(-a, a), wr, 'x² = c має два корені ±√c, якщо c > 0', f'x² = {a*a}; x = ±{a}')

def f_lin_ineq(T, rng, lv):
    a = rng.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]); b = rng.choice([v for v in range(-9, 10) if v]); c0 = rng.randint(-6, 8)
    op = rng.choice(list(OPS)); thr = F(c0 - b, a)
    op2 = OPP[op] if a < 0 else op
    sol = [ray(op2, thr)]
    strict = op in ('<', '>')
    wr = []
    if a < 0: wr.append((setstr([ray(op, thr)]), 'при діленні на від’ємне число знак нерівності не змінено'))
    else: wr.append((setstr([ray(OPP[op], thr)]), 'знак нерівності змінено, хоча ділили на додатне число'))
    wr.append((setstr([ray(TOG[op2], thr)]), 'нерівність строга, тому число в розв’язок не входить' if strict else 'нерівність нестрога, тому число входить у розв’язок'))
    wr.append((setstr([ray(op2, F(c0 + b, a))]), 'вільний член перенесено без зміни знака'))
    wr.append((setstr([ray(op2, F(c0 - b))]), 'обидві частини не поділено на коефіцієнт при x'))
    return T.add(lv, f'Розв’яжіть нерівність: {poly([a, b])} {OPS[op]} {c0}.', setstr(sol), wr, 'при множенні або діленні нерівності на від’ємне число знак змінюється на протилежний', f'{poly([a, 0])} {OPS[op]} {c0 - b}; x {OPS[op2]} {fmt(thr)}')

def f_sys_lin(T, rng, lv):
    x, y = rng.randint(-5, 7), rng.randint(-5, 7)
    if x == y or x == 0 or y == 0: return False
    a, b, c, d = rng.choice([(1, 1, 1, -1), (2, 1, 1, -1), (1, 2, 1, -1), (3, 1, 1, 1), (2, -1, 1, 1), (1, 1, 2, -1), (1, -1, 3, 2), (2, 3, 1, -1), (1, 3, 1, -1), (3, -1, 1, 1)])
    e, f = a * x + b * y, c * x + d * y
    ask = rng.choice(['xy', 'y', 'x', 'sum', 'diff'])
    vals = {'xy': (x * y, 'добуток x · y'), 'y': (y, 'значення y'), 'x': (x, 'значення x'), 'sum': (x + y, 'суму x + y'), 'diff': (x - y, 'різницю x − y')}
    ans, nm = vals[ask]
    short = {'xy': 'добуток xy', 'y': 'y', 'x': 'x', 'sum': 'суму x + y', 'diff': 'різницю x − y'}
    wr = [(v, f'знайдено {short[kk]}, а не {short[ask]}') for kk, (v, _) in vals.items() if kk != ask]
    rng.shuffle(wr)
    return T.add(lv, f'Розв’яжіть систему рівнянь {{ {lc2(a, b)} = {e}, {lc2(c, d)} = {f} }} і знайдіть {nm}.', ans, wr, 'додавання або підстановка: виразіть одну змінну або зрівняйте коефіцієнти', f'x = {fmt(x)}, y = {fmt(y)}; {short[ask]} = {fmt(ans)}')

def f_exp_eq(T, rng, lv):
    b = rng.choice([2, 3, 5, 10, F(1, 2), F(1, 3)]); k = rng.choice([-3, -2, -1, 2, 3, 4])
    N = F(b) ** k
    if abs(N) > 2000: return False
    bs = fmt(b) if not isinstance(b, F) else f'({fmt(b)})'
    wr = [(-k, 'знак показника переплутано'), (N, 'відповіддю назвали число, а не показник'), (k + 1, 'степінь пораховано з похибкою на одиницю'), (F(N) / F(b), 'число поділено на основу, а показник не шукали')]
    return T.add(lv, f'Розв’яжіть рівняння {bs}^x = {fmt(N)}.', k, wr, 'зведіть обидві частини до однієї основи й прирівняйте показники', f'{fmt(N)} = {bs}^({k}), отже x = {k}')

def f_log_eq(T, rng, lv):
    kind = rng.choice(['x', 'base', 'lg'])
    if kind == 'x':
        b = rng.choice([2, 3, 5, 4]); k = rng.choice([-2, -1, 2, 3, 4]); N = F(b) ** k
        if abs(N) > 700: return False
        sb = {2: '₂', 3: '₃', 4: '₄', 5: '₅'}[b]
        wr = [(b * k, f'замість степеня {b}^({k}) знайдено добуток {b}·({k})'), (k, 'відповіддю назвали значення логарифма, а не x'), (F(b) ** (-k), 'знак показника степеня переплутано'), (b + k, 'основу і значення логарифма додано')]
        return T.add(lv, f'Розв’яжіть рівняння log{sb} x = {fmt(k)}.', N, wr, 'logₐ x = k ⇔ x = aᵏ', f'x = {b}^({k}) = {fmt(N)}')
    if kind == 'base':
        N, k = rng.choice([(16, 2), (27, 3), (64, 3), (81, 4), (125, 3), (32, 5), (100, 2), (49, 2), (64, 6), (243, 5)]); r = round(N ** (1 / k))
        wr = [(F(N, k), 'аргумент поділено на показник'), (k, 'відповіддю назвали значення логарифма'), (N, 'відповіддю назвали аргумент логарифма'), (N - k, 'від аргументу віднято значення логарифма')]
        return T.add(lv, f'Розв’яжіть рівняння log_x {N} = {k} (x > 0, x ≠ 1).', r, wr, 'log_x a = k ⇔ xᵏ = a', f'x^{k} = {N}; x = {r}')
    k = rng.choice([-3, -2, -1, 1, 2, 3, 4]); N = F(10) ** k
    wr = [(k, 'відповіддю назвали значення логарифма, а не x'), (10 * k, 'показник помножено на основу 10'), (F(10) ** (-k), 'знак показника степеня переплутано'), (10 + k, 'основу і значення логарифма додано')]
    return T.add(lv, f'Розв’яжіть рівняння lg x = {fmt(k)}.', N, wr, 'lg x = log₁₀ x; lg x = k ⇔ x = 10ᵏ', f'x = 10^({k}) = {fmt(N)}')

def f_sqrt_eq(T, rng, lv):
    a = rng.randint(2, 9); b = rng.randint(1, 8); xv = a * a - b
    wr = [(a - b, 'праву частину не піднесено до квадрата'), (a * a + b, f'число {b} перенесено без зміни знака'), (a * a, f'число {b} під коренем втрачено'), (a * a - b * b, f'число {b} піднесено до квадрата')]
    return T.add(lv, f'Розв’яжіть рівняння √(x + {b}) = {a}.', xv, wr, 'піднесіть обидві частини до квадрата й виконайте перевірку', f'x + {b} = {a*a}; x = {xv}; перевірка: √{a*a} = {a}')

def f_frac_eq(T, rng, lv):
    x = rng.choice([v for v in range(-6, 9) if v]); k = rng.randint(2, 5); c = rng.choice([v for v in range(-5, 6) if v and v != x])
    a = (k - 1) * x - k * c
    if a == 0: return False
    wr = [(F(a - k * c, k - 1), f'добуток {k}·({fmt(c)}) перенесено без зміни знака'),
          (F(a + k * c, k + 1), 'доданок x перенесено без зміни знака'),
          (F(a + c, k - 1), f'число {k} помножено лише на x, а не на {fmt(-c)}'),
          (F(-(a + k * c), k - 1), 'різницю взято у зворотному порядку')]
    den = f'(x {M if c > 0 else "+"} {abs(c)})'
    return T.add(lv, f'Розв’яжіть рівняння (x {"+" if a > 0 else M} {abs(a)}) / {den} = {k}.', x, wr, 'домножте обидві частини на знаменник (x ≠ ' + fmt(c) + ') і розв’яжіть лінійне рівняння', f'x {"+" if a > 0 else M} {abs(a)} = {k}{den}; {k - 1}x = {fmt(a + k*c)}; x = {fmt(x)}')

def f_discr_count(T, rng, lv):
    cnt = rng.choice([0, 1, 2, 2])
    if cnt == 1:
        s, t = rng.randint(1, 3), rng.randint(1, 5); sg_ = rng.choice([1, -1]); A, B, C = s * s, 2 * s * t * sg_, t * t
    else:
        while True:
            A = rng.randint(1, 4); B = rng.randint(-8, 8); C = rng.randint(-6, 9)
            D_ = B * B - 4 * A * C
            if (cnt == 2 and D_ > 0) or (cnt == 0 and D_ < 0): break
    D = B * B - 4 * A * C
    names = {0: 'жодного', 1: 'один', 2: 'два'}
    rel = {0: '< 0', 1: '= 0', 2: '> 0'}
    what = {0: 'коренів немає лише при D < 0', 1: 'один корінь буває лише при D = 0', 2: 'два корені бувають лише при D > 0'}
    wr = [(names[w], f'{what[w]}, а тут D = {D} {rel[cnt]}') for w in (0, 1, 2) if w != cnt]
    wr.append(('три', 'квадратне рівняння має не більше двох коренів'))
    return T.add(lv, f'Скільки коренів має рівняння {poly([A, B, C])} = 0?', names[cnt], wr, 'кількість коренів визначає дискримінант: D > 0 — два, D = 0 — один, D < 0 — жодного', f'D = {B}² − 4·{A}·({C}) = {D} {rel[cnt]}')

def f_vieta(T, rng, lv):
    p, q = rng.sample([v for v in range(-8, 9)], 2)
    B, C = -(p + q), p * q; S_, P_ = p + q, p * q
    kind = rng.choice(['prod', 'sum', 'sqs'])
    if kind == 'prod':
        nm = 'добуток'; ans = C
        wr = [(-C, 'знак добутку змінено'), (S_, 'знайдено суму коренів'), (B, 'взято коефіцієнт b'), (C * C, 'вільний член піднесено до квадрата')]
    elif kind == 'sum':
        nm = 'суму'; ans = S_
        wr = [(B, 'суму коренів взято зі знаком коефіцієнта b, а має бути −b'), (P_, 'знайдено добуток коренів'), (-P_, 'знайдено добуток коренів із протилежним знаком'), (S_ * P_, 'суму помножено на добуток')]
    else:
        nm = None; ans = p * p + q * q
        wr = [(S_ * S_, 'не віднято подвоєний добуток коренів'), (S_ * S_ + 2 * P_, 'знак подвоєного добутку змінено'), (S_ * S_ - P_, 'добуток коренів не подвоєно'), (S_ - 2 * P_, 'суму коренів не піднесено до квадрата')]
    txt = f'Не розв’язуючи рівняння {poly([1, B, C])} = 0, знайдіть ' + (f'{nm} його коренів.' if nm else 'x₁² + x₂².')
    return T.add(lv, txt, ans, wr, 'формули Вієта: x₁ + x₂ = −b, x₁x₂ = c; x₁² + x₂² = (x₁ + x₂)² − 2x₁x₂', f'x₁ + x₂ = {S_}, x₁x₂ = {P_}; відповідь {ans}')

def f_abs_eq(T, rng, lv):
    a = rng.choice([v for v in range(-6, 7) if v]); b = rng.randint(1, 8)
    wr = [(vs(a + b), 'розглянуто лише випадок, коли вираз під модулем додатний'), (vs(a - b), 'розглянуто лише випадок, коли вираз під модулем від’ємний'), (vs(-b, b), 'зсув під модулем не враховано: розв’язано |x| = ' + str(b)), (vs(b - a, -a - b), 'знак числа під модулем змінено')]
    txt = f'|x {M if a > 0 else "+"} {abs(a)}| = {b}'
    return T.add(lv, f'Розв’яжіть рівняння {txt}.', vs(a - b, a + b), wr, '|u| = b (b > 0) ⇔ u = b або u = −b', f'x {M if a > 0 else "+"} {abs(a)} = ±{b}; x = {fmt(a - b)} або x = {fmt(a + b)}')

def f_number_word(T, rng, lv):
    k = rng.choice(['diff', 'consec', 'ratio'])
    if k == 'diff':
        s, d = rng.randint(30, 90), rng.randint(2, 12)
        if (s + d) % 2: return False
        big, small = (s + d) // 2, (s - d) // 2
        wr = [(big, 'знайдено більше число, а не менше'), (F(s, 2), 'суму поділено навпіл, ніби числа однакові'), (s - d, 'від суми віднято різницю, але не поділено навпіл'), (s + d, 'до суми додано різницю й не поділено навпіл')]
        return T.add(lv, f'Сума двох чисел дорівнює {s}, а їх різниця — {d}. Знайдіть менше з цих чисел.', small, wr, 'нехай менше число x, більше — x + d; тоді 2x + d = s', f'2x + {d} = {s}; x = {small}')
    if k == 'consec':
        n_ = rng.randint(5, 25); prod = n_ * (n_ + 1)
        wr = [(n_ + 1, 'знайдено більше число, а не менше'), (n_ - 1, 'взято попереднє число: (n−1)·n ≠ добутку'), (2 * n_ + 1, 'знайдено суму двох чисел'), (n_ + 2, 'взято число через одне')]
        return T.add(lv, f'Добуток двох послідовних натуральних чисел дорівнює {prod}. Знайдіть менше з них.', n_, wr, 'x(x + 1) = p — квадратне рівняння; від’ємний корінь відкиньте', f'x² + x − {prod} = 0; x = {n_}')
    a, b = rng.choice([(2, 3), (3, 4), (1, 4), (2, 5), (3, 5), (1, 3)]); k2 = rng.randint(3, 9); tot = (a + b) * k2
    wr = [(a * k2, 'знайдено менше число, а не більше'), (F(tot, b), 'суму поділено лише на другу частину відношення'), (tot - b, 'від суми віднято частину відношення'), (F(tot, a), 'суму поділено лише на першу частину відношення')]
    return T.add(lv, f'Два числа відносяться як {a} : {b}, а їх сума дорівнює {tot}. Знайдіть більше число.', b * k2, wr, 'числа ak і bk; (a + b)k = сума', f'k = {tot} : {a + b} = {k2}; більше число {b}·{k2} = {b*k2}')

# ===================== РІВЕНЬ 2 =====================
def f_quad_lead(T, rng, lv):
    for _ in range(200):
        u_, w_ = rng.randint(1, 4), rng.randint(1, 4)
        v_, z_ = rng.choice([v for v in range(-8, 9) if v]), rng.choice([v for v in range(-8, 9) if v])
        if u_ == 1 and w_ == 1: continue
        A, B, C = u_ * w_, u_ * z_ + v_ * w_, v_ * z_
        if math.gcd(math.gcd(A, abs(B)), abs(C)) != 1: continue
        p, q = F(-v_, u_), F(-z_, w_)
        if p == q: continue
        break
    else: return False
    D = B * B - 4 * A * C; sD = math.isqrt(D)
    wr = [(vs(-p, -q), 'знак −b у формулі коренів втрачено'),
          (vs(A * p, A * q), 'у знаменнику формули коренів взято 2 замість 2a'),
          (vs(2 * p, 2 * q), 'у знаменнику формули коренів взято a замість 2a')]
    D2 = B * B + 4 * A * C
    if D2 >= 0 and math.isqrt(D2) ** 2 == D2:
        s2 = math.isqrt(D2); wr.append((vs(F(-B + s2, 2 * A), F(-B - s2, 2 * A)), 'у дискримінанті знак добутку 4ac змінено'))
    wr.append((vs(p, -q), 'знак одного з коренів змінено'))
    return T.add(lv, f'Розв’яжіть рівняння {poly([A, B, C])} = 0.', vs(p, q), wr, 'x = (−b ± √D)/(2a), D = b² − 4ac', f'D = {B}² − 4·{A}·({C}) = {D}, √D = {sD}; x = ({-B} ± {sD})/{2*A}; корені {vs(p, q)}')

def f_biquad(T, rng, lv):
    kind = rng.choice(['cnt', 'cnt', 'prod', 'sum', 'max'])
    if kind == 'cnt':
        case = rng.choice(['pp', 'pn', 'nn', 'p0'])
        if case == 'pp': t1, t2 = rng.sample([1, 4, 9, 16, 25], 2); cnt = 4
        elif case == 'pn': t1 = rng.choice([1, 4, 9, 16]); t2 = -rng.choice([1, 2, 3, 4, 5, 9]); cnt = 2
        elif case == 'nn': t1, t2 = rng.sample([-1, -2, -3, -4, -5, -6, -8, -9], 2); cnt = 0
        else: t1 = 0; t2 = rng.choice([1, 4, 9, 16, 25]); cnt = 3
        B, C = -(t1 + t2), t1 * t2; ts = [t1, t2]
        wr = [(len(ts), 'підраховано корені допоміжного рівняння відносно t = x², а не відносно x'),
              (sum(1 for t in ts if t > 0), 'кожне додатне t = x² дає два значення x = ±√t, а враховано лише одне'),
              (2 * len(ts), 'кожному t приписано по два значення x, хоча від’ємне t коренів не дає, а t = 0 дає один'),
              (3 if cnt != 3 else 5, 'вважали, що один із коренів t дає лише одне значення x')]
        desc = ', '.join(f't = {t}' + (' (t < 0 — не підходить)' if t < 0 else ' (x = 0)' if t == 0 else f' (x = ±{math.isqrt(t)})') for t in ts)
        return T.add(lv, f'Скільки дійсних коренів має рівняння {poly([1, 0, B, 0, C])} = 0?', cnt, wr, 'підстановка t = x² (t ≥ 0): кожне додатне t дає два значення x, t = 0 — одне, від’ємне t — жодного', f'{desc}; разом коренів: {cnt}')
    p, q = sorted(rng.sample([1, 2, 3, 4, 5], 2)); t1, t2 = p * p, q * q
    B, C = -(t1 + t2), t1 * t2
    eq = poly([1, 0, B, 0, C])
    if kind == 'prod':
        wr = [(p * q, 'добуток лише додатних коренів'), (-C, 'знак добутку змінено'), (0, 'вважали, що корені взаємно скорочуються, як у сумі'), (-B, 'знайдено суму значень t = x², а не добуток коренів x')]
        return T.add(lv, f'Знайдіть добуток усіх дійсних коренів рівняння {eq} = 0.', C, wr, 'корені ±p, ±q: (−p)(p)(−q)(q) = p²q²', f't = {t1} або {t2}; корені ±{p}, ±{q}; добуток {C}')
    if kind == 'sum':
        wr = [(2 * (p + q), 'додано модулі коренів'), (p + q, 'враховано лише додатні корені'), (-B, 'знайдено суму значень t = x²'), (-(p + q), 'враховано лише від’ємні корені')]
        return T.add(lv, f'Знайдіть суму всіх дійсних коренів рівняння {eq} = 0.', 0, wr, 'корені розташовані парами ±: їх сума дорівнює нулю', f'корені ±{p}, ±{q}; сума 0')
    wr = [(t2, 'назвали найбільше значення t = x², а не x'), (p, 'взято менший додатний корінь'), (p + q, 'знайдено суму додатних коренів'), (-q, 'взято від’ємний корінь')]
    return T.add(lv, f'Знайдіть найбільший корінь рівняння {eq} = 0.', q, wr, 'підстановка t = x² (t ≥ 0), потім x = ±√t', f't = {t1} або {t2}; найбільший корінь √{t2} = {q}')

def f_quad_ineq(T, rng, lv):
    p, q = sorted(rng.sample(range(-8, 9), 2)); lead = rng.choice([1, 1, 2, -1, -2, 3]); op = rng.choice(list(OPS))
    co = expand([p, q], lead)
    sol, wr = set_wrongs({F(p): 1, F(q): 1}, {}, lead, op)
    return T.add(lv, f'Розв’яжіть нерівність {poly(co)} {OPS[op]} 0.', setstr(sol), wr, 'знайдіть корені, позначте їх на осі й визначте знак виразу на кожному проміжку (гілки параболи вгору при a > 0, вниз при a < 0)', f'корені {p} та {q}; старший коефіцієнт {"додатний" if lead > 0 else "від’ємний"}; відповідь {setstr(sol)}')

def f_rat_ineq(T, rng, lv):
    nr = rng.sample(range(-7, 8), rng.choice([1, 2]))
    dr = rng.choice([x for x in range(-7, 8) if x not in nr])
    op = rng.choice(list(OPS))
    sol, wr = set_wrongs({F(r): 1 for r in nr}, {F(dr): 1}, 1, op)
    num = ''.join(fac(r) for r in sorted(nr))
    return T.add(lv, f'Розв’яжіть нерівність {num} / {fac(dr)} {OPS[op]} 0.', setstr(sol), wr, 'метод інтервалів: нулі чисельника при нестрогій нерівності входять у розв’язок, нулі знаменника — ніколи', f'критичні точки: {", ".join(fmt(c) for c in sorted(set(nr) | {dr}))}; відповідь {setstr(sol)}')

def f_sys_lin2(T, rng, lv):
    x, y = rng.randint(-5, 6), rng.randint(-5, 6)
    if x == y or x == 0 or y == 0: return False
    for _ in range(80):
        a, b, c, d = [rng.choice([1, 2, 3, 4, -1, -2, -3, 5]) for _ in range(4)]
        if a * d - b * c != 0 and abs(a * d - b * c) <= 7 and a * d + b * c != 0: break
    else: return False
    e, f = a * x + b * y, c * x + d * y
    det2 = a * d + b * c; x2, y2 = F(e * d + b * f, det2), F(a * f - c * e, det2)
    pr = lambda u, v: f'({fmt(u)}; {fmt(v)})'
    wr = [(pr(y, x), 'координати розв’язку переставлено місцями'), (pr(x, -y), 'знак y змінено'), (pr(-x, y), 'знак x змінено'),
          (pr(x2, y2), 'під час складання рівнянь знак коефіцієнта при y у першому рівнянні втрачено')]
    return T.add(lv, f'Розв’яжіть систему рівнянь {{ {lc2(a, b)} = {e}, {lc2(c, d)} = {f} }}.', pr(x, y), wr, 'зрівняйте коефіцієнти при одній змінній і додайте (відніміть) рівняння; перевірте підстановкою', f'x = {fmt(x)}, y = {fmt(y)}; перевірка: {a}·{pn(x)} + ({b})·{pn(y)} = {e}')

def f_sys_sym(T, rng, lv):
    p, q = rng.sample(range(-6, 9), 2); s, P_ = p + q, p * q
    kind = rng.choice(['x2y2', 'x3y3', 'dif2', 'inv'])
    if kind == 'inv' and P_ == 0: return False
    head = f'Числа x і y задовольняють умови x + y = {s} і xy = {P_}. '
    if kind == 'x2y2':
        ans = s * s - 2 * P_
        wr = [(s * s, 'не віднято подвоєний добуток 2xy'), (s * s + 2 * P_, 'знак 2xy змінено'), (s * s - P_, 'добуток не подвоєно'), (s - 2 * P_, 'суму не піднесено до квадрата')]
        return T.add(lv, head + 'Знайдіть x² + y².', ans, wr, 'x² + y² = (x + y)² − 2xy', f'{s}² − 2·({P_}) = {ans}')
    if kind == 'x3y3':
        ans = s ** 3 - 3 * P_ * s
        wr = [(s ** 3, 'не віднято 3xy(x + y)'), (s ** 3 - 3 * P_, 'у формулі втрачено множник (x + y)'), (s ** 3 + 3 * P_ * s, 'знак 3xy(x + y) змінено'), (s * s * s - P_ * s, 'замість 3xy(x + y) віднято xy(x + y)')]
        return T.add(lv, head + 'Знайдіть x³ + y³.', ans, wr, 'x³ + y³ = (x + y)³ − 3xy(x + y)', f'{s}³ − 3·({P_})·{s} = {ans}')
    if kind == 'dif2':
        ans = s * s - 4 * P_
        wr = [(s * s - 2 * P_, 'знайдено x² + y²'), (s * s, 'не віднято 4xy'), (s * s + 4 * P_, 'знак 4xy змінено'), (s * s - P_, 'добуток xy не збільшено у чотири рази')]
        return T.add(lv, head + 'Знайдіть (x − y)².', ans, wr, '(x − y)² = (x + y)² − 4xy', f'{s}² − 4·({P_}) = {ans}')
    ans = F(s, P_)
    wr = [(F(P_, s) if s else 0, 'дріб перевернуто: знайдено xy/(x + y)'), (s * P_, 'суму помножено на добуток'), (s - P_, 'від суми віднято добуток'), (F(-s, P_), 'знак суми змінено')]
    return T.add(lv, head + 'Знайдіть 1/x + 1/y.', ans, wr, '1/x + 1/y = (x + y)/(xy)', f'{s}/({P_}) = {fmt(ans)}')

def f_exp_eq2(T, rng, lv):
    b = rng.choice([2, 3, 5]); kind = rng.choice(['sum', 'quad', 'shift'])
    if kind == 'sum':
        k = rng.randint(1, 4); m = rng.randint(1, 3); N = b ** (k + m) + b ** k
        if N > 4000: return False
        lhs = lambda w: F(b) ** (w + m) + F(b) ** w
        wr = [(w, f'підстановка x = {w} дає {fmt(lhs(w))}, а не {N}') for w in (k + 1, k - 1, k + m, m) if w != k]
        wr.append((N, 'відповіддю назвали праву частину'))
        return T.add(lv, f'Розв’яжіть рівняння {b}^(x + {m}) + {b}^x = {N}.', k, wr, 'винесіть bˣ за дужки: bˣ(b^m + 1) = N, тоді bˣ = N / (b^m + 1)', f'{b}^x·({b}^{m} + 1) = {N}; {b}^x = {b**k}; x = {k}')
    if kind == 'quad':
        t1, t2 = rng.sample([0, 1, 2, 3], 2); A, B = b ** t1, b ** t2
        ask = rng.choice(['sum', 'prod'])
        ans = t1 + t2 if ask == 'sum' else t1 * t2
        wr = [(t1 * t2 if ask == 'sum' else t1 + t2, 'знайдено ' + ('добуток' if ask == 'sum' else 'суму') + ' коренів замість ' + ('суми' if ask == 'sum' else 'добутку')),
              (A + B, 'знайдено суму значень t = bˣ, а не коренів x'), (A * B, 'знайдено добуток значень t = bˣ'), (b ** ans if b ** ans != ans else ans + 1, 'результат прийнято за показник степеня')]
        return T.add(lv, f'Знайдіть {"суму" if ask == "sum" else "добуток"} коренів рівняння {b}^(2x) − {A + B}·{b}^x + {A * B} = 0.', ans, wr, 'підстановка t = bˣ > 0 дає квадратне рівняння; потім x = log_b t', f't² − {A + B}t + {A * B} = 0; t = {A} або t = {B}; x = {t1} та x = {t2}')
    s = rng.choice([2, 3]); x = rng.choice([v for v in range(-4, 6) if v]); m = x * (s - 1)
    wr = [(F(m, s + 1), 'доданок x перенесено без зміни знака'), (-x, 'знак числа m змінено'), (F(m, s), 'доданок x із правої частини не враховано'), (m * (s - 1), 'замість ділення на s − 1 виконано множення')]
    return T.add(lv, f'Розв’яжіть рівняння {b ** s}^x = {b}^(x {"+" if m > 0 else M} {abs(m)}).', x, wr, 'зведіть обидві частини до основи b: (bˢ)ˣ = b^(sx)', f'{b}^({s}x) = {b}^(x {"+" if m > 0 else M} {abs(m)}); {s}x = x {"+" if m > 0 else M} {abs(m)}; x = {x}')

def f_log_eq2(T, rng, lv):
    cands = [(bb, kk, d1, (bb ** kk) // d1) for bb in (2, 3, 5) for kk in range(2, 6) for d1 in range(1, 30) if (bb ** kk) % d1 == 0 and d1 < (bb ** kk) // d1 and bb ** kk <= 700]
    bb, kk, d1, d2 = rng.choice(cands); m = d2 - d1; N = bb ** kk
    sb = {2: '₂', 3: '₃', 5: '₅'}[bb]
    wr = [(vs(d1, -d2), 'сторонній корінь не відкинуто: за ОДЗ x > 0'), (-d2, 'вибрано лише сторонній корінь'), (d2, 'знайдено значення x + ' + str(m) + ', а не x'), (N, 'відповіддю назвали праву частину')]
    return T.add(lv, f'Розв’яжіть рівняння log{sb} x + log{sb}(x + {m}) = {kk}.', d1, wr, 'logₐu + logₐv = logₐ(uv); ОДЗ: усі аргументи логарифмів додатні; сторонні корені відкидають', f'x(x + {m}) = {N}; x² + {m}x − {N} = 0; x = {d1} або x = {-d2}; за ОДЗ підходить x = {d1}')

def f_irrat_eq(T, rng, lv):
    if rng.random() < 0.5:
        r = rng.randint(3, 8); s = 2 - r; c = r * (r - 2)
        txt = f'√(2x + {c}) = x'; cond = 'x ≥ 0'; sol = f'2x + {c} = x²; x² − 2x − {c} = 0; x = {r} або x = {s}; x = {s} < 0 — сторонній корінь'
        S2 = s; ext = f'x = {s} не задовольняє умову x ≥ 0'
    else:
        d = rng.randint(1, 3); r = rng.randint(d + 2, d + 6); s = 2 * d + 1 - r; c = d * d - r * s
        txt = f'√(x + {c}) = x − {d}'; sol = f'x + {c} = (x − {d})²; x² − {2*d + 1}x + {d*d - c} = 0; x = {r} або x = {s}; при x = {s} права частина {s - d} < 0 — сторонній корінь'
    wr = [(vs(r, s), 'сторонній корінь не відкинуто: права частина має бути невід’ємною'), (s, 'підійшов лише сторонній корінь'), (r + s, 'знайдено суму коренів квадратного рівняння'), (r * s, 'знайдено добуток коренів квадратного рівняння')]
    return T.add(lv, f'Розв’яжіть рівняння {txt}.', r, wr, 'піднесіть обидві частини до квадрата, а потім перевірте: права частина √ є невід’ємною', sol)

TRIG = [
 ('sin x = 1/2', '(−1)ⁿ·π/6 + πn, n ∈ ℤ', [('π/6 + 2πn, n ∈ ℤ', 'втрачено другу серію x = 5π/6 + 2πn'), ('±π/6 + 2πn, n ∈ ℤ', 'застосовано формулу для косинуса'), ('(−1)ⁿ·π/3 + πn, n ∈ ℤ', 'arcsin(1/2) = π/6, а не π/3'), ('(−1)ⁿ·π/6 + 2πn, n ∈ ℤ', 'період загальної формули — π, а не 2π')]),
 ('cos x = 1/2', '±π/3 + 2πn, n ∈ ℤ', [('π/3 + 2πn, n ∈ ℤ', 'втрачено серію x = −π/3 + 2πn'), ('±π/6 + 2πn, n ∈ ℤ', 'arccos(1/2) = π/3, а не π/6'), ('(−1)ⁿ·π/3 + πn, n ∈ ℤ', 'застосовано формулу для синуса'), ('±π/3 + πn, n ∈ ℤ', 'період косинуса — 2π, а не π')]),
 ('tg x = 1', 'π/4 + πn, n ∈ ℤ', [('π/4 + 2πn, n ∈ ℤ', 'період тангенса — π, а не 2π'), ('±π/4 + πn, n ∈ ℤ', 'застосовано формулу для косинуса'), ('π/3 + πn, n ∈ ℤ', 'arctg 1 = π/4, а не π/3'), ('(−1)ⁿ·π/4 + πn, n ∈ ℤ', 'застосовано формулу для синуса')]),
 ('sin x = −1', '−π/2 + 2πn, n ∈ ℤ', [('π/2 + 2πn, n ∈ ℤ', 'sin(π/2) = 1, а не −1'), ('−π/2 + πn, n ∈ ℤ', 'період — 2π: при непарних n sin = 1'), ('π + 2πn, n ∈ ℤ', 'sin π = 0'), ('3π/2 + πn, n ∈ ℤ', 'при парних n маємо x = 3π/2, але при непарних sin = 1')]),
 ('cos x = 0', 'π/2 + πn, n ∈ ℤ', [('πn, n ∈ ℤ', 'cos πn = ±1, а не 0'), ('π/2 + 2πn, n ∈ ℤ', 'втрачено серію x = −π/2 + 2πn'), ('π + 2πn, n ∈ ℤ', 'cos π = −1'), ('2πn, n ∈ ℤ', 'cos 0 = 1')]),
 ('sin x = √3/2', '(−1)ⁿ·π/3 + πn, n ∈ ℤ', [('(−1)ⁿ·π/6 + πn, n ∈ ℤ', 'arcsin(√3/2) = π/3, а не π/6'), ('±π/3 + 2πn, n ∈ ℤ', 'застосовано формулу для косинуса'), ('π/3 + 2πn, n ∈ ℤ', 'втрачено серію x = 2π/3 + 2πn'), ('(−1)ⁿ·2π/3 + πn, n ∈ ℤ', 'arcsin(√3/2) = π/3, а не 2π/3')]),
 ('cos x = −1/2', '±2π/3 + 2πn, n ∈ ℤ', [('±π/3 + 2πn, n ∈ ℤ', 'arccos(−1/2) = π − π/3 = 2π/3, а не π/3'), ('2π/3 + 2πn, n ∈ ℤ', 'втрачено серію x = −2π/3 + 2πn'), ('±2π/3 + πn, n ∈ ℤ', 'період косинуса — 2π, а не π'), ('±π/6 + 2πn, n ∈ ℤ', 'cos(π/6) = √3/2, а не 1/2')]),
 ('tg x = −√3', '−π/3 + πn, n ∈ ℤ', [('π/3 + πn, n ∈ ℤ', 'arctg(−a) = −arctg a: знак втрачено'), ('−π/6 + πn, n ∈ ℤ', 'tg(π/6) = √3/3, а не √3'), ('−π/3 + 2πn, n ∈ ℤ', 'період тангенса — π, а не 2π'), ('±π/3 + πn, n ∈ ℤ', 'застосовано формулу для косинуса')]),
 ('sin x = 0', 'πn, n ∈ ℤ', [('2πn, n ∈ ℤ', 'втрачено серію x = π + 2πn'), ('π/2 + πn, n ∈ ℤ', 'це розв’язки рівняння cos x = 0'), ('π + 2πn, n ∈ ℤ', 'втрачено серію x = 2πn'), ('(−1)ⁿ·π/2 + πn, n ∈ ℤ', 'arcsin 0 = 0, а не π/2')]),
 ('cos x = 1', '2πn, n ∈ ℤ', [('πn, n ∈ ℤ', 'при непарних n cos = −1'), ('π + 2πn, n ∈ ℤ', 'cos π = −1'), ('π/2 + 2πn, n ∈ ℤ', 'cos(π/2) = 0'), ('±2πn, n ∈ ℤ', 'зайвий знак ±: серія та сама, формула для ± тут не потрібна')]),
 ('sin x = 1', 'π/2 + 2πn, n ∈ ℤ', [('−π/2 + 2πn, n ∈ ℤ', 'sin(−π/2) = −1'), ('π/2 + πn, n ∈ ℤ', 'при непарних n sin = −1'), ('π + 2πn, n ∈ ℤ', 'sin π = 0'), ('2πn, n ∈ ℤ', 'sin 0 = 0')]),
 ('cos x = −1', 'π + 2πn, n ∈ ℤ', [('2πn, n ∈ ℤ', 'cos 0 = 1'), ('π/2 + 2πn, n ∈ ℤ', 'cos(π/2) = 0'), ('πn, n ∈ ℤ', 'при парних n cos = 1'), ('−π + πn, n ∈ ℤ', 'при парних n cos = 1')]),
 ('tg x = 0', 'πn, n ∈ ℤ', [('π/2 + πn, n ∈ ℤ', 'tg(π/2) не існує'), ('2πn, n ∈ ℤ', 'втрачено серію x = π + 2πn'), ('π + 2πn, n ∈ ℤ', 'втрачено серію x = 2πn'), ('πn/2, n ∈ ℤ', 'зайві розв’язки x = π/2 + πn, де тангенс не існує')]),
 ('tg x = √3/3', 'π/6 + πn, n ∈ ℤ', [('π/3 + πn, n ∈ ℤ', 'tg(π/3) = √3, а не √3/3'), ('π/6 + 2πn, n ∈ ℤ', 'період тангенса — π, а не 2π'), ('±π/6 + πn, n ∈ ℤ', 'застосовано формулу для косинуса'), ('π/4 + πn, n ∈ ℤ', 'tg(π/4) = 1, а не √3/3')]),
 ('sin x = −1/2', '(−1)ⁿ⁺¹·π/6 + πn, n ∈ ℤ', [('(−1)ⁿ·π/6 + πn, n ∈ ℤ', 'arcsin(−a) = −arcsin a: знак втрачено'), ('−π/6 + 2πn, n ∈ ℤ', 'втрачено серію x = 7π/6 + 2πn'), ('±π/6 + 2πn, n ∈ ℤ', 'застосовано формулу для косинуса'), ('(−1)ⁿ⁺¹·π/3 + πn, n ∈ ℤ', 'arcsin(1/2) = π/6, а не π/3')]),
 ('cos x = √2/2', '±π/4 + 2πn, n ∈ ℤ', [('π/4 + 2πn, n ∈ ℤ', 'втрачено серію x = −π/4 + 2πn'), ('±π/4 + πn, n ∈ ℤ', 'період косинуса — 2π, а не π'), ('±π/3 + 2πn, n ∈ ℤ', 'cos(π/3) = 1/2, а не √2/2'), ('(−1)ⁿ·π/4 + πn, n ∈ ℤ', 'застосовано формулу для синуса')]),
 ('cos x = √3/2', '±π/6 + 2πn, n ∈ ℤ', [('±π/3 + 2πn, n ∈ ℤ', 'cos(π/3) = 1/2, а не √3/2'), ('π/6 + 2πn, n ∈ ℤ', 'втрачено серію x = −π/6 + 2πn'), ('±π/6 + πn, n ∈ ℤ', 'період косинуса — 2π, а не π'), ('(−1)ⁿ·π/6 + πn, n ∈ ℤ', 'застосовано формулу для синуса')]),
 ('sin x = √2/2', '(−1)ⁿ·π/4 + πn, n ∈ ℤ', [('±π/4 + 2πn, n ∈ ℤ', 'застосовано формулу для косинуса'), ('π/4 + 2πn, n ∈ ℤ', 'втрачено серію x = 3π/4 + 2πn'), ('(−1)ⁿ·π/3 + πn, n ∈ ℤ', 'sin(π/3) = √3/2, а не √2/2'), ('(−1)ⁿ·π/4 + 2πn, n ∈ ℤ', 'період загальної формули — π, а не 2π')]),
]
def f_trig_eq(T, rng, lv):
    eq, ans, wr = rng.choice(TRIG)
    return T.add(lv, f'Розв’яжіть рівняння {eq}.', ans, wr, 'запам’ятайте загальні формули: sin x = a → x = (−1)ⁿ arcsin a + πn; cos x = a → x = ± arccos a + 2πn; tg x = a → x = arctg a + πn', f'{eq}: x = {ans.replace(", n ∈ ℤ", "")}, n ∈ ℤ')

def f_expo_ineq(T, rng, lv):
    b = rng.choice([2, 3, 5, F(1, 2), F(1, 3), F(2, 3)]); k = rng.choice([-2, -1, 1, 2, 3, 4]); op = rng.choice(list(OPS))
    N = F(b) ** k
    if abs(N) > 500 or (N != 0 and abs(N) < F(1, 500)): return False
    bs = fmt(b) if not isinstance(b, F) else f'({fmt(b)})'
    inc = F(b) > 1; opx = op if inc else OPP[op]
    sol = [ray(opx, F(k))]
    strict = op in ('<', '>')
    wr = [(setstr([ray(OPP[opx], F(k))]), 'основа більша за 1: знак нерівності для показників зберігається, а його змінено' if inc else 'основа менша за 1: знак нерівності для показників слід змінити на протилежний'),
          (setstr([ray(TOG[opx], F(k))]), 'нерівність строга, тому число k у розв’язок не входить' if strict else 'нерівність нестрога, тому число k входить у розв’язок'),
          (setstr([ray(opx, N)]), 'розв’язком названо число, з яким порівнювали, а не показник'),
          (setstr([ray(opx, F(-k))]), 'знак показника переплутано')]
    return T.add(lv, f'Розв’яжіть нерівність {bs}^x {OPS[op]} {fmt(N)}.', setstr(sol), wr, 'зведіть до однієї основи; при основі > 1 знак зберігається, при 0 < a < 1 — змінюється на протилежний', f'{fmt(N)} = {bs}^({k}); x {OPS[opx]} {k}')

def f_log_ineq(T, rng, lv):
    b = rng.choice([2, 3, 5, F(1, 2), F(1, 3)]); k = rng.randint(1, 3); op = rng.choice(list(OPS))
    N = F(b) ** k; inc = F(b) > 1; ox = op if inc else OPP[op]
    sb = {2: '₂', 3: '₃', 5: '₅'}.get(b) if not isinstance(b, F) else f'_({b.numerator}/{b.denominator})'
    odz = lambda o, t: (F(0), t, False, o == '<=') if o in ('<', '<=') else (t, None, o == '>=', False)
    sol = [odz(ox, N)]; strict = op in ('<', '>')
    wr = [(setstr([odz(OPP[ox], N)]), 'основа більша за 1: знак нерівності зберігається, а його змінено' if inc else 'основа менша за 1: знак нерівності слід змінити на протилежний'),
          (setstr([(None, N, False, ox == '<=')]) if ox in ('<', '<=') else setstr([(None, N, False, OPP[ox] == '<=')]), 'не враховано ОДЗ: аргумент логарифма має бути додатним' if ox in ('<', '<=') else 'знак змінено, а ОДЗ x > 0 не враховано'),
          (setstr([odz(TOG[ox], N)]), 'нерівність строга, тому кінець у розв’язок не входить' if strict else 'нерівність нестрога, тому кінець входить у розв’язок'),
          (setstr([odz(ox, F(k))]), 'аргумент порівняно з показником k, а не з b^k')]
    return T.add(lv, f'Розв’яжіть нерівність log{sb} x {OPS[op]} {k}.', setstr(sol), wr, 'враховуйте ОДЗ x > 0; при основі > 1 знак зберігається, при 0 < a < 1 — змінюється', f'x {OPS[ox]} {fmt(N)} за правилом основи; з ОДЗ x > 0: {setstr(sol)}')

def f_int_count(T, rng, lv):
    p, q = sorted(rng.sample(range(-8, 9), 2)); op = rng.choice(['<=', '<'])
    if q - p < 3: return False
    co = expand([p, q]); cnt = q - p + 1 if op == '<=' else q - p - 1
    if op == '<=': wr = [(q - p - 1, 'кінці p і q виключено, хоча нерівність нестрога'), (q - p, 'кількість знайдено як різницю кінців'), (q - p + 2, 'до кінців додано ще одну зайву точку'), (q - p + 3, 'враховано точки за межами відрізка')]
    else: wr = [(q - p + 1, 'кінці p і q включено, хоча нерівність строга'), (q - p, 'кількість знайдено як різницю кінців'), (q - p - 2, 'виключено ще одне ціле число всередині проміжку'), (q - p + 2, 'враховано точки за межами проміжку')]
    return T.add(lv, f'Скільки цілих розв’язків має нерівність {poly(co)} {OPS[op]} 0?', cnt, wr, 'розв’яжіть нерівність і підрахуйте цілі числа в одержаному проміжку', f'розв’язок: {"[" if op == "<=" else "("}{p}; {q}{"]" if op == "<=" else ")"}; цілих чисел: {cnt}')

def f_param_one(T, rng, lv):
    b = rng.choice([2, 4, 6, 8, 10, 12, -2, -4, -6, -8, -10]); k = F(b * b, 4)
    wr = [(b * b, 'взято k = b² замість b²/4'), (-k, 'знак значення змінено'), (F(b * b, 2), 'у рівнянні D = 0 коефіцієнт 4 замінено на 2: b² = 2k'), (F(b, 2), 'квадрат у виразі b²/4 не піднесено')]
    return T.add(lv, f'При якому значенні k рівняння x² {"+" if b > 0 else M} {abs(b)}x + k = 0 має рівно один корінь?', k, wr, 'один корінь — дискримінант D = 0: b² − 4k = 0', f'D = {b*b} − 4k = 0; k = {fmt(k)}')

def f_param_two(T, rng, lv):
    b = rng.choice([2, 4, 6, 8, -2, -4, -6, -8, 10]); thr = F(b * b, 4); case = rng.choice(['two', 'none', 'any'])
    op = {'two': '<', 'none': '>', 'any': '<='}[case]
    sol = [ray(op, thr)]
    what = {'two': 'має два різні корені', 'none': 'не має коренів', 'any': 'має хоча б один корінь'}[case]
    cond = {'two': 'D > 0', 'none': 'D < 0', 'any': 'D ≥ 0'}[case]
    wr = [(setstr([ray(OPP[op], thr)]), 'нерівність для k записано в протилежний бік (знак при діленні на −4 не змінено)'),
          (setstr([ray(TOG[op], thr)]), 'межу k = ' + fmt(thr) + (' включено, але тоді D = 0 і корінь один' if case == 'two' else ' виключено, але тоді D = 0 і корінь один (він теж потрібен)' if case == 'any' else ' включено, але тоді D = 0 і корінь є')),
          (setstr([ray(op, F(b * b, 2))]), 'дискримінант записано як b² − 2k замість b² − 4k'),
          (setstr([ray(op, F(b * b))]), 'дискримінант записано як b² − k замість b² − 4k')]
    return T.add(lv, f'При яких значеннях k рівняння x² {"+" if b > 0 else M} {abs(b)}x + k = 0 {what}?', setstr(sol), wr, f'{cond}, де D = b² − 4k', f'D = {b*b} − 4k; {cond} ⇒ k {OPS[op]} {fmt(thr)}')

def f_system_ineq(T, rng, lv):
    a1 = rng.randint(2, 4); b1 = rng.randint(1, 9); c1 = rng.randint(-4, 3); x1 = F(c1 + b1, a1)
    d = rng.randint(1, 6); e = rng.randint(6, 14); x2 = F(e - d)
    if x1 >= x2 - 1: return False
    o1 = rng.choice(['>', '>=']); o2 = rng.choice(['<', '<='])
    sol = [(x1, x2, o1 == '>=', o2 == '<=')]
    wr = [(setstr([(None, None, False, False)]), 'знайдено об’єднання розв’язків замість перетину'), (setstr([ray(o1, x1)]), 'враховано лише першу нерівність'), (setstr([ray(o2, x2)]), 'враховано лише другу нерівність'), (setstr([(x1, x2, o1 != '>=', o2 != '<=')]), 'строгість нерівностей враховано навпаки')]
    return T.add(lv, f'Розв’яжіть систему нерівностей {{ {a1}x − {b1} {OPS[o1]} {fmt(c1)}, x + {d} {OPS[o2]} {e} }}.', setstr(sol), wr, 'розв’яжіть кожну нерівність і знайдіть перетин множин розв’язків', f'x {OPS[o1]} {fmt(x1)}; x {OPS[o2]} {fmt(x2)}; перетин {setstr(sol)}')

def f_rect_word(T, rng, lv):
    a, b = rng.sample(range(2, 16), 2); a, b = max(a, b), min(a, b)
    P_, A_ = 2 * (a + b), a * b
    wr = [(b, 'знайдено меншу сторону'), (P_ // 2, 'знайдено півпериметр'), (F(P_, 4), 'периметр поділено на 4, як для квадрата'), (a - b, 'знайдено різницю сторін')]
    return T.add(lv, f'Периметр прямокутника дорівнює {P_} см, а його площа — {A_} см². Знайдіть довжину більшої сторони (см).', a, wr, 'півпериметр a + b = P/2 і добуток ab = S — це формули Вієта для коренів t² − (P/2)t + S = 0', f't² − {P_//2}t + {A_} = 0; t = {a} або {b}; більша сторона {a} см')

def f_lin_ineq2(T, rng, lv):
    a, c = rng.sample([v for v in range(-6, 7) if v], 2); b, d = rng.sample([v for v in range(-9, 10) if v], 2)
    op = rng.choice(list(OPS)); k = a - c; thr = F(d - b, k); op2 = OPP[op] if k < 0 else op; strict = op in ('<', '>')
    wr = [(setstr([ray(op if k < 0 else OPP[op], thr)]), 'при діленні на від’ємне число знак нерівності не змінено' if k < 0 else 'знак нерівності змінено, хоча ділили на додатне число'),
          (setstr([ray(TOG[op2], thr)]), 'нерівність строга, тому число в розв’язок не входить' if strict else 'нерівність нестрога, тому число входить у розв’язок'),
          (setstr([ray(op2, -thr)]), 'різницю вільних членів взято у зворотному порядку'),
          (setstr([ray(op2, F(d + b, k))]), 'вільний член перенесено без зміни знака')]
    return T.add(lv, f'Розв’яжіть нерівність: {poly([a, b])} {OPS[op]} {poly([c, d])}.', setstr([ray(op2, thr)]), wr, 'зберіть доданки з x в одній частині; при діленні на від’ємне число змінюйте знак', f'({a} − ({c}))x {OPS[op]} {d} − ({b}); {k}x {OPS[op]} {d - b}; x {OPS[op2]} {fmt(thr)}')

def f_abs_ineq(T, rng, lv):
    p = 1 if lv == 2 else rng.choice([2, 3, -2, -3]); q = rng.choice([v for v in range(-9, 10) if v]); r = rng.randint(1, 8)
    op = rng.choice(list(OPS))
    x1, x2 = F(r - q, p), F(-r - q, p)
    nd = {x1: 1, x2: 1}
    sol = solve_gen(nd, {}, 1, op)
    strict = op in ('<', '>')
    wr = [(setstr(solve_gen(nd, {}, 1, OPP[op])), 'взято протилежний тип нерівності: |u| < r замість |u| > r (або навпаки)'),
          (setstr(solve_gen(nd, {}, 1, TOG[op])), 'нерівність строга, тому кінці в розв’язок не входять' if strict else 'нерівність нестрога, тому кінці входять у розв’язок'),
          (setstr(solve_gen({F(r, p): 1, F(-r, p): 1}, {}, 1, op)), 'зсув q під модулем не враховано'),
          (setstr(solve_gen({F(r - q): 1, F(-r - q): 1}, {}, 1, op)), 'обидві частини не поділено на коефіцієнт при x'),
          (setstr([ray(op if p > 0 else OPP[op], x1)]), 'розглянуто лише одну з двох нерівностей, на які розпадається модуль')]
    return T.add(lv, f'Розв’яжіть нерівність |{poly([p, q])}| {OPS[op]} {r}.', setstr(sol), wr, '|u| < r ⇔ −r < u < r; |u| > r ⇔ u < −r або u > r', f'{poly([p, q])} = ±{r} при x = {fmt(x2)} та x = {fmt(x1)}; відповідь {setstr(sol)}')

FAMS_L12 = [(f_lin_eq, [1]), (f_quad_roots, [1]), (f_incomplete, [1]), (f_lin_ineq, [1]), (f_sys_lin, [1]), (f_exp_eq, [1]), (f_log_eq, [1]), (f_sqrt_eq, [1]), (f_frac_eq, [1]), (f_discr_count, [1]), (f_vieta, [1, 2]), (f_abs_eq, [1]), (f_number_word, [1]),
            (f_quad_lead, [2]), (f_biquad, [2]), (f_quad_ineq, [2]), (f_rat_ineq, [2]), (f_sys_lin2, [2]), (f_sys_sym, [2]), (f_exp_eq2, [2]), (f_log_eq2, [2]), (f_irrat_eq, [2]), (f_trig_eq, [2]), (f_expo_ineq, [2]), (f_log_ineq, [2]), (f_int_count, [2]), (f_param_one, [2]), (f_param_two, [2]), (f_system_ineq, [2]), (f_rect_word, [2]), (f_lin_ineq2, [2]), (f_abs_ineq, [2])]
FAMS = FAMS_L12

# ===================== РІВЕНЬ 3 =====================
SB = {2: '₂', 3: '₃', 5: '₅', 10: '₁₀'}
def lin_term(c, name, first=False):
    """c·name зі знаком для запису виразу"""
    if c == 0: return ''
    body = (name if abs(c) == 1 else f'{fmt(abs(c))}·{name}')
    if first: return (M if c < 0 else '') + body
    return (' + ' if c > 0 else f' {M} ') + body
def const_term(c):
    if c == 0: return ''
    return (' + ' if c > 0 else f' {M} ') + fmt(abs(c))

def f_rat_eq_ext(T, rng, lv):
    p = rng.randint(2, 5); A = rng.choice([v for v in range(-9, 10) if v and v not in (-p, -3 * p)])
    r2 = -2 * p - A
    if r2 in (p, -p): return False
    txt = f'x/(x − {p}) {"+" if A > 0 else M} {abs(A)}/(x + {p}) = {2*p*p}/(x² − {p*p})'
    wr = [(vs(p, r2), f'сторонній корінь x = {p} не відкинуто: він перетворює знаменник на нуль'), (p, 'знайдено лише нуль знаменника'), (-r2, 'знак кореня змінено'), (p + A, 'взято коефіцієнт при x у квадратному рівнянні')]
    return T.add(lv, f'Розв’яжіть рівняння {txt}.', r2, wr, 'ОДЗ: x ≠ ±' + str(p) + '; зведіть до спільного знаменника й перевірте корені на ОДЗ',
                 f'x(x + {p}) {"+" if A > 0 else M} {abs(A)}(x − {p}) = {2*p*p}; (x − {p})(x {"+" if 2*p + A > 0 else M} {abs(2*p + A)}) = 0; x = {p} не входить в ОДЗ; x = {r2}')

def f_two_radicals(T, rng, lv):
    u_, v_ = rng.choice([(5, 3), (4, 2), (5, 4), (6, 4), (7, 5), (6, 2), (5, 1), (4, 3), (6, 5), (7, 3), (8, 6), (7, 1)])
    k = u_ - v_; tot = u_ * u_ - v_ * v_
    a = rng.randint(1, min(12, tot - 1)); b = tot - a
    x = u_ * u_ - a
    wr = [(x + a, 'знайдено значення підкореневого виразу x + ' + str(a) + ', а не x'), (v_ * v_, f'знайдено значення виразу x − {b}, а не x'), (u_ * u_ + a, f'число {a} додано замість віднімання'), (u_ * u_ - b, f'віднято {b} замість {a}')]
    return T.add(lv, f'Розв’яжіть рівняння √(x + {a}) − √(x − {b}) = {k}.', x, wr, 'помножте і поділіть на спряжений вираз: √A − √B = k ⇒ √A + √B = (A − B)/k', f'(x + {a}) − (x − {b}) = {tot}; √(x+{a}) + √(x−{b}) = {tot}/{k} = {u_ + v_}; √(x+{a}) = {u_}; x = {u_*u_} − {a} = {x}')

def f_exp_quad2(T, rng, lv):
    b = rng.choice([2, 3, 5]); t1, t2 = sorted(rng.sample([1, 2, 3], 2)); A, B_ = b ** t1, b ** t2
    q = (A + B_) // b; n = A * B_
    ask = rng.choice(['sum', 'prod'])
    ans = t1 + t2 if ask == 'sum' else t1 * t2
    alt = (t1 + 1) + (t2 + 1) if ask == 'sum' else (t1 + 1) * (t2 + 1)
    wr = [(alt, 'знайдено корені відносно x + 1, а не x'), (A + B_, 'знайдено суму значень t = bˣ, а не суму коренів x'), (n, 'знайдено добуток значень t = bˣ'), (t1 * t2 if ask == 'sum' else t1 + t2, 'знайдено ' + ('добуток' if ask == 'sum' else 'суму') + ' коренів замість ' + ('суми' if ask == 'sum' else 'добутку'))]
    return T.add(lv, f'Знайдіть {"суму" if ask == "sum" else "добуток"} коренів рівняння {b}^(2x) − {q}·{b}^(x + 1) + {n} = 0.', ans, wr, 'bˣ⁺¹ = b·bˣ; підстановка t = bˣ > 0 зводить рівняння до квадратного', f't² − {q*b}t + {n} = 0; t = {A} або t = {B_}; x = {t1} та x = {t2}')

def f_log_quad(T, rng, lv):
    b = rng.choice([2, 3, 5]); u1, u2 = rng.sample([-2, -1, 0, 1, 2, 3, 4], 2); sb = SB[b]
    S_, P_ = u1 + u2, u1 * u2
    eq = f'(log{sb} x)²' + lin_term(-S_, f'log{sb} x') + const_term(P_) + ' = 0'
    ask = rng.choice(['sum', 'prod'])
    xs = (F(b) ** u1, F(b) ** u2)
    ans = xs[0] + xs[1] if ask == 'sum' else xs[0] * xs[1]
    wr = [(S_, 'знайдено суму значень логарифма, а не коренів x'), (F(b) ** P_, 'показники перемножено замість додавання'), (xs[0] * xs[1] if ask == 'sum' else xs[0] + xs[1], 'знайдено ' + ('добуток' if ask == 'sum' else 'суму') + ' коренів замість ' + ('суми' if ask == 'sum' else 'добутку')), (b * S_, 'основу помножено на суму значень логарифма')]
    return T.add(lv, f'Знайдіть {"суму" if ask == "sum" else "добуток"} коренів рівняння {eq}.', ans, wr, 'підстановка t = logₐ x дає квадратне рівняння; x = aᵗ', f'{poly([1, -S_, P_], "t")} = 0; t = {u1} та t = {u2}; x = {fmt(xs[0])} та x = {fmt(xs[1])}')

def f_abs_two(T, rng, lv):
    nz = [v for v in range(-7, 8) if v]
    a, b = rng.sample(nz, 2); d = abs(a - b)
    ta = f'|x {M if a > 0 else "+"} {abs(a)}|'; tb = f'|x {M if b > 0 else "+"} {abs(b)}|'
    if rng.random() < 0.5:
        c = d + rng.randint(1, 6); ans = a + b
        wr = [(F(a + b, 2), 'знайдено середину відрізка між числами під модулями, а не суму коренів'), (c, 'відповіддю назвали праву частину'), (a + b + c, 'до суми коренів додано праву частину'), (abs(a - b), 'знайдено відстань між числами під модулями'), (a * b, 'знайдено добуток чисел під модулями'), (c + d, 'додано довжину відрізка до правої частини')]
        return T.add(lv, f'Знайдіть суму всіх коренів рівняння {ta} + {tb} = {c}.', ans, wr, 'корені симетричні відносно середини відрізка між нулями модулів: x = (a + b ± c)/2', f'c = {c} > |a − b| = {d}: коренів два: x = {fmt(F(a + b - c, 2))} і x = {fmt(F(a + b + c, 2))}; сума {a + b}')
    case = rng.choice(['two', 'inf', 'zero'])
    if case == 'zero':
        if d < 2: return False
        c = rng.randint(1, d - 1)
    elif case == 'inf': c = d
    else: c = d + rng.randint(1, 6)
    names = {0: '0', 1: '1', 2: '2', 'inf': 'нескінченно багато', 3: '3', 4: '4'}
    cnt = {'two': 2, 'inf': 'inf', 'zero': 0}[case]
    reasons = {
        ('two', 1): 'розглянуто лише один із випадків розкриття модулів', ('two', 'inf'): 'рівність виконується на всьому відрізку лише при c = |a − b|',
        ('two', 0): 'вважали, що сума відстаней не може дорівнювати c', ('two', 4): 'кожен із модулів дає два випадки, але випадки поза умовами розкриття коренів не дають',
        ('inf', 2): 'не враховано, що між числами сума відстаней стала й дорівнює |a − b|', ('inf', 1): 'розглянуто лише один із випадків розкриття модулів',
        ('inf', 0): 'вважали, що розв’язків немає', ('inf', 3): 'підраховано окремі точки, а розв’язком є весь відрізок',
        ('zero', 2): 'мінімальне значення суми |x − a| + |x − b| дорівнює |a − b| > c, тому розв’язків немає', ('zero', 1): 'вважали, що розв’язок єдиний — у середині відрізка',
        ('zero', 'inf'): 'сума відстаней дорівнює c на всьому відрізку лише при c = |a − b|', ('zero', 4): 'підраховано всі випадки розкриття модулів без перевірки умов'}
    opts = [k for k in (0, 1, 2, 'inf', 3, 4) if k != cnt and (case, k) in reasons]
    wr = [(names[k], reasons[(case, k)]) for k in opts]
    sol = {'two': f'c = {c} > |a − b| = {d}: два корені', 'inf': f'c = |a − b| = {d}: розв’язком є весь відрізок [{min(a,b)}; {max(a,b)}]', 'zero': f'c = {c} < |a − b| = {d}: розв’язків немає'}[case]
    return T.add(lv, f'Скільки розв’язків має рівняння {ta} + {tb} = {c}?', names[cnt], wr, 'сума відстаней від x до двох точок не менша за відстань між ними', sol)

TRIGI = [
 ('sin x = 1/2', '[0; 2π]', 2, [(1, 'втрачено корінь x = 5π/6'), (3, 'враховано зайвий корінь'), (4, 'враховано корені рівнянь sin x = 1/2 і sin x = −1/2')]),
 ('2cos²x − 3cos x + 1 = 0', '[0; 2π]', 4, [(2, 'не враховано корені cos x = 1: x = 0 і x = 2π'), (3, 'кінці проміжку 0 і 2π враховано лише один раз'), (5, 'для cos x = 1/2 враховано зайвий корінь'), (6, 'кожному значенню cos x приписано по три корені')]),
 ('sin²x = 1/4', '[0; 2π]', 4, [(2, 'розглянуто лише sin x = 1/2'), (3, 'один корінь пропущено'), (8, 'кожен із чотирьох коренів порахований двічі')]),
 ('cos 2x = 0', '[0; π]', 2, [(1, 'розв’язано cos x = 0 замість cos 2x = 0'), (3, 'враховано корінь, що виходить за межі проміжку'), (4, 'враховано корені на проміжку [0; 2π]')]),
 ('sin x · cos x = 0', '[0; π]', 3, [(2, 'кінці проміжку 0 і π враховано лише один раз'), (1, 'розглянуто лише cos x = 0'), (4, 'враховано зайвий корінь x = 3π/2')]),
 ('tg x = 1', '[0; 2π]', 2, [(1, 'втрачено корінь x = 5π/4'), (3, 'враховано зайвий корінь'), (4, 'враховано корені рівнянь tg x = 1 і tg x = −1')]),
 ('cos x = −1', '[0; 4π]', 2, [(1, 'втрачено корінь x = 3π'), (3, 'враховано зайвий корінь x = 5π'), (4, 'кожний корінь порахований двічі')]),
 ('|sin x| = 1/2', '[0; 2π]', 4, [(2, 'розглянуто лише sin x = 1/2'), (3, 'один корінь пропущено'), (6, 'враховано зайві корені')]),
 ('sin x = cos x', '[0; 2π]', 2, [(1, 'втрачено корінь x = 5π/4'), (3, 'враховано зайвий корінь'), (4, 'розв’язано sin x = ± cos x')]),
 ('sin 2x = 1', '[0; 2π]', 2, [(1, 'розв’язано sin x = 1 замість sin 2x = 1'), (3, 'враховано зайвий корінь'), (4, 'враховано корені рівнянь sin 2x = 1 і sin 2x = −1')]),
 ('cos x = 0', '[0; 3π]', 3, [(2, 'втрачено корінь x = 5π/2'), (4, 'враховано корінь x = 7π/2, що виходить за межі проміжку'), (6, 'кожний корінь порахований двічі')]),
 ('2sin²x + sin x − 1 = 0', '[0; 2π]', 3, [(2, 'не враховано корінь x = 3π/2 (sin x = −1)'), (4, 'для sin x = −1 враховано зайвий корінь'), (6, 'кожному значенню sin x приписано по три корені')]),
 ('sin x = 1', '[0; 5π]', 3, [(2, 'втрачено корінь x = 9π/2'), (4, 'враховано корінь x = 13π/2, що виходить за межі проміжку'), (6, 'кожний корінь порахований двічі')]),
 ('cos x = 1/2', '[−π; π]', 2, [(1, 'втрачено корінь x = −π/3'), (3, 'враховано зайвий корінь'), (4, 'враховано корені cos x = ±1/2')]),
 ('tg x = 0', '[−π; π]', 3, [(1, 'враховано лише корінь x = 0'), (2, 'кінці проміжку −π та π враховано не обидва'), (5, 'враховано точки, де тангенс не існує')]),
 ('2sin²x − sin x − 1 = 0', '[0; 2π]', 3, [(2, 'не враховано корінь x = π/2 (sin x = 1)'), (4, 'для sin x = 1 враховано зайвий корінь'), (6, 'кожному значенню sin x приписано по три корені')]),
]
TRIG_SOL = {"'sin x = 1/2', '[0; 2π]'": 'x = π/6 та x = 5π/6', "'2cos²x − 3cos x + 1 = 0', '[0; 2π]'": 'cos x = 1 → x = 0, 2π; cos x = 1/2 → x = π/3, 5π/3', "'sin²x = 1/4', '[0; 2π]'": 'sin x = ±1/2 → x = π/6, 5π/6, 7π/6, 11π/6', "'cos 2x = 0', '[0; π]'": '2x = π/2 + πn → x = π/4 + πn/2 → x = π/4, 3π/4', "'sin x · cos x = 0', '[0; π]'": 'sin x = 0 → x = 0, π; cos x = 0 → x = π/2', "'tg x = 1', '[0; 2π]'": 'x = π/4 + πn → x = π/4, 5π/4', "'cos x = −1', '[0; 4π]'": 'x = π + 2πn → x = π, 3π', "'|sin x| = 1/2', '[0; 2π]'": 'sin x = ±1/2 → x = π/6, 5π/6, 7π/6, 11π/6', "'sin x = cos x', '[0; 2π]'": 'tg x = 1 → x = π/4, 5π/4', "'sin 2x = 1', '[0; 2π]'": '2x = π/2 + 2πn → x = π/4 + πn → x = π/4, 5π/4', "'cos x = 0', '[0; 3π]'": 'x = π/2 + πn → x = π/2, 3π/2, 5π/2', "'2sin²x + sin x − 1 = 0', '[0; 2π]'": 'sin x = 1/2 → x = π/6, 5π/6; sin x = −1 → x = 3π/2', "'sin x = 1', '[0; 5π]'": 'x = π/2 + 2πn → x = π/2, 5π/2, 9π/2', "'cos x = 1/2', '[−π; π]'": 'x = ±π/3 + 2πn → x = −π/3, π/3', "'tg x = 0', '[−π; π]'": 'x = πn → x = −π, 0, π', "'2sin²x − sin x − 1 = 0', '[0; 2π]'": 'sin x = 1 → x = π/2; sin x = −1/2 → x = 7π/6, 11π/6'}
def f_trig_interval(T, rng, lv):
    eq, iv, cnt, wr = rng.choice(TRIGI)
    sol = [v for k, v in TRIG_SOL.items() if k.startswith(repr(eq) + ', ' + repr(iv))][0]
    extra = [(cnt + 1, 'враховано зайвий корінь'), (cnt - 1 if cnt > 1 else cnt + 3, 'один корінь пропущено')]
    return T.add(lv, f'Скільки коренів має рівняння {eq} на проміжку {iv}?', cnt, wr + extra, 'розв’яжіть рівняння в загальному вигляді, а потім відберіть корені, що належать проміжку (з урахуванням кінців)', f'{sol}; на проміжку {iv} коренів: {cnt}')

def f_motion(T, rng, lv):
    for _ in range(300):
        v = rng.randint(8, 20); c = rng.randint(2, 5); k1, k2 = rng.randint(1, 4), rng.randint(1, 4)
        if v - c < 3: continue
        d1, d2 = k1 * (v + c), k2 * (v - c); t = k1 + k2
        a2, b2, c2 = t, -(d1 + d2), c * (d1 - d2) - t * c * c
        D = b2 * b2 - 4 * a2 * c2
        if c2 == 0 or D <= 0 or math.isqrt(D) ** 2 != D: continue
        v2 = F(-b2 - math.isqrt(D), 2 * a2) if F(-b2 + math.isqrt(D), 2 * a2) == v else F(-b2 + math.isqrt(D), 2 * a2)
        if F(-b2 + math.isqrt(D), 2 * a2) != v and F(-b2 - math.isqrt(D), 2 * a2) != v: continue
        if v2 > c: continue
        break
    else: return False
    wr = [(v + c, 'знайдено швидкість катера за течією'), (v - c, 'знайдено швидкість катера проти течії'), (F(d1 + d2, t), 'знайдено середню швидкість на всьому шляху (відстань : час)'), (v + 2 * c, 'швидкість течії додано двічі')]
    return T.add(lv, f'Катер пройшов {d1} км за течією річки та {d2} км проти течії, витративши на весь шлях {t} год. Швидкість течії дорівнює {c} км/год. Знайдіть власну швидкість катера (км/год).', v, wr, 'час = відстань / швидкість; швидкість за течією v + c, проти течії v − c', f'{d1}/(v + {c}) + {d2}/(v − {c}) = {t}; {poly([a2, b2, c2], "v")} = 0; v = {v} (другий корінь {fmt(v2)} ≤ {c} не підходить)')

def f_work(T, rng, lv):
    cands = []
    for x in range(2, 31):
        for d in range(1, 13):
            t = F(x * (x + d), 2 * x + d)
            if (t * 10).denominator == 1 and t >= 2: cands.append((x, d, t))
    x, d, t = rng.choice(cands)
    x2 = F(-t * d, x)
    wr = [(x + d, 'знайдено час, за який завдання виконав би другий робітник'), (2 * t, 'вважали, що робітники працюють однаково швидко'), (t + d, 'до спільного часу додано різницю часів'), (x2, 'вибрано від’ємний корінь, який за змістом задачі не підходить')]
    return T.add(lv, f'Двоє робітників, працюючи разом, виконують завдання за {fmt(t)} год. Перший, працюючи сам, виконав би його на {d} год швидше за другого. За скільки годин виконає завдання самостійно перший робітник?', x, wr, 'продуктивності додаються: 1/x + 1/(x + d) = 1/t', f'1/x + 1/(x + {d}) = 1/{fmt(t)}; x² + ({d} − {fmt(2*t)})x − {fmt(t*d)} = 0; x = {x} (другий корінь {fmt(x2)} < 0 не підходить)')

def f_vieta_adv(T, rng, lv):
    kind = rng.choice(['inv', 'cube', 'abs', 'rel', 'diff'])
    if kind in ('inv', 'cube', 'abs'):
        p, q = rng.sample([v for v in range(-7, 8) if v], 2); B, C = -(p + q), p * q; S_, P_ = p + q, p * q
        eq = poly([1, B, C])
        if kind == 'inv':
            ans = F(S_, P_)
            wr = [(F(P_, S_) if S_ else 0, 'дріб перевернуто: знайдено x₁x₂/(x₁ + x₂)'), (S_ * P_, 'суму помножено на добуток'), (F(-S_, P_), 'знак суми змінено'), (S_ - P_, 'від суми віднято добуток')]
            return T.add(lv, f'Не розв’язуючи рівняння {eq} = 0, знайдіть 1/x₁ + 1/x₂.', ans, wr, '1/x₁ + 1/x₂ = (x₁ + x₂)/(x₁x₂)', f'x₁ + x₂ = {S_}, x₁x₂ = {P_}; {fmt(S_)}/{pn(P_)} = {fmt(ans)}')
        if kind == 'cube':
            ans = S_ ** 3 - 3 * P_ * S_
            wr = [(S_ ** 3, 'не віднято 3x₁x₂(x₁ + x₂)'), (S_ ** 3 - 3 * P_, 'у формулі втрачено множник (x₁ + x₂)'), (S_ ** 3 + 3 * P_ * S_, 'знак 3x₁x₂(x₁ + x₂) змінено'), (S_ * (S_ * S_ - P_), 'замість 3x₁x₂ віднято x₁x₂')]
            return T.add(lv, f'Не розв’язуючи рівняння {eq} = 0, знайдіть x₁³ + x₂³.', ans, wr, 'x₁³ + x₂³ = (x₁ + x₂)³ − 3x₁x₂(x₁ + x₂)', f'x₁ + x₂ = {S_}, x₁x₂ = {P_}; {S_}³ − 3·({P_})·({S_}) = {ans}')
        ans = abs(p - q); D = (p - q) ** 2
        wr = [(D, 'корінь із (x₁ − x₂)² не добуто'), (abs(S_), 'знайдено модуль суми коренів'), (S_ * S_ - 2 * P_, 'знайдено x₁² + x₂²'), (abs(P_), 'знайдено модуль добутку коренів')]
        return T.add(lv, f'Не розв’язуючи рівняння {eq} = 0, знайдіть |x₁ − x₂|.', ans, wr, '(x₁ − x₂)² = (x₁ + x₂)² − 4x₁x₂', f'(x₁ − x₂)² = {S_}² − 4·({P_}) = {D}; |x₁ − x₂| = {ans}')
    if kind == 'rel':
        k = rng.choice([2, 3, 4]); r = rng.randint(1, 6); S_ = (k + 1) * r; ans = k * r * r
        wr = [(r * r, f'добуток обчислено як r·r без множника {k}'), (k * r, 'знайдено більший корінь, а не добуток'), (r, 'знайдено менший корінь, а не добуток'), (S_, 'взято суму коренів')]
        return T.add(lv, f'Один із коренів рівняння x² − {S_}x + c = 0 у {k} рази більший за інший. Знайдіть c.', ans, wr, 'нехай корені r і kr: за теоремою Вієта (k + 1)r = сума, c = k·r²', f'{k+1}r = {S_}; r = {r}; c = {k}·{r}² = {ans}')
    S_ = rng.randint(3, 14); d = rng.choice([x for x in range(1, S_) if (S_ - x) % 2 == 0])
    ans = F(S_ * S_ - d * d, 4)
    wr = [(F(S_ * S_ - d * d, 2), 'діленням на 2 замість 4'), (S_ * S_ - d * d, 'різницю квадратів не поділено на 4'), (F(S_ * S_ + d * d, 4), 'знак d² змінено'), (F(S_ - d, 2), 'знайдено менший корінь, а не добуток')]
    return T.add(lv, f'Різниця коренів рівняння x² − {S_}x + c = 0 дорівнює {d}. Знайдіть c.', ans, wr, 'корені (S + d)/2 і (S − d)/2; c = їх добуток = (S² − d²)/4', f'x₁ = {fmt(F(S_ + d, 2))}, x₂ = {fmt(F(S_ - d, 2))}; c = {fmt(ans)}')

def f_param_all(T, rng, lv):
    s = rng.randint(1, 6); kind = rng.choice(['gt', 'ge', 'two', 'none'])
    nd = {F(-2 * s): 1, F(2 * s): 1}
    if kind in ('gt', 'none'):
        what = 'виконується для всіх дійсних x' if kind == 'gt' else 'не має дійсних коренів'
        eq = f'x² − ax + {s*s} > 0' if kind == 'gt' else f'x² − ax + {s*s} = 0'
        sol = solve_gen(nd, {}, 1, '<'); cond = 'D < 0'
        wr = [(setstr(solve_gen(nd, {}, 1, '>')), 'знайдено значення, при яких D > 0'), (setstr(solve_gen(nd, {}, 1, '<=')), 'при D = 0 парабола дотикається до осі: нерівність > 0 не виконується (або корінь існує)'), (setstr(solve_gen({F(-s): 1, F(s): 1}, {}, 1, '<')), 'у дискримінанті a² − 4·' + str(s*s) + ' втрачено множник 4'), (setstr([ray('<', F(2 * s))]), 'враховано лише одну з умов −' + str(2*s) + ' < a < ' + str(2*s))]
        txt = f'При яких значеннях a нерівність {eq[:-2] if False else eq} {what}?' if kind == 'gt' else f'При яких значеннях a рівняння {eq} {what}?'
        if kind == 'gt': txt = f'При яких значеннях a нерівність {eq} виконується для всіх дійсних x?'
    elif kind == 'ge':
        eq = f'x² − ax + {s*s} ≥ 0'
        sol = solve_gen(nd, {}, 1, '<='); cond = 'D ≤ 0'
        wr = [(setstr(solve_gen(nd, {}, 1, '>=')), 'знайдено значення, при яких D ≥ 0'), (setstr(solve_gen(nd, {}, 1, '<')), 'при D = 0 парабола дотикається до осі, і нерівність ≥ 0 виконується: межі треба включити'), (setstr(solve_gen({F(-s): 1, F(s): 1}, {}, 1, '<=')), 'у дискримінанті a² − 4·' + str(s*s) + ' втрачено множник 4'), (setstr([ray('<=', F(2 * s))]), 'враховано лише одну з умов')]
        txt = f'При яких значеннях a нерівність {eq} виконується для всіх дійсних x?'
    else:
        eq = f'x² + ax + {s*s} = 0'
        sol = solve_gen(nd, {}, 1, '>'); cond = 'D > 0'
        wr = [(setstr(solve_gen(nd, {}, 1, '<')), 'знайдено значення, при яких D < 0'), (setstr(solve_gen(nd, {}, 1, '>=')), 'при D = 0 корінь один: межі в розв’язок не входять'), (setstr(solve_gen({F(-s): 1, F(s): 1}, {}, 1, '>')), 'у дискримінанті a² − 4·' + str(s*s) + ' втрачено множник 4'), (setstr([ray('>', F(2 * s))]), 'враховано лише одну з двох умов (a < −' + str(2*s) + ' або a > ' + str(2*s) + ')')]
        txt = f'При яких значеннях a рівняння {eq} має два різні корені?'
    return T.add(lv, txt, setstr(sol), wr, f'умова на дискримінант: {cond}, де D = a² − 4·{s*s}', f'D = a² − {4*s*s}; {cond}; відповідь {setstr(sol)}')

def f_int_sum_rat(T, rng, lv):
    p, q = rng.sample(range(-8, 9), 2)
    if abs(p - q) < 3: return False
    op = rng.choice(['<', '<='])
    sol = solve_gen({F(p): 1}, {F(q): 1}, 1, op)
    ints = int_list(sol); ans = sum(ints)
    lo_v, hi_v = min(p, q), max(p, q)
    role = {p: 'чисельника', q: 'знаменника'}
    strict = op == '<'
    def sum_with(lc_, rc_): return sum(x for x in range(lo_v, hi_v + 1) if (x > lo_v or lc_) and (x < hi_v or rc_))
    cor = {lo_v: (not strict) if role[lo_v] == 'чисельника' else False, hi_v: (not strict) if role[hi_v] == 'чисельника' else False}
    wr = []
    for end, nm in ((lo_v, 'lo'), (hi_v, 'hi')):
        flip = {lo_v: cor[lo_v], hi_v: cor[hi_v]}; flip[end] = not flip[end]
        if role[end] == 'чисельника':
            why = f'нуль чисельника x = {end} виключено, хоча нерівність нестрога' if cor[end] else f'нуль чисельника x = {end} включено, хоча нерівність строга'
        else:
            why = f'нуль знаменника x = {end} включено, а на нуль ділити не можна'
        wr.append((sum_with(flip[lo_v], flip[hi_v]), why))
    wr.append((sum_with(True, True) if not (cor[lo_v] and cor[hi_v]) else sum_with(False, False), 'обидва кінці оброблено неправильно'))
    wr.append((p + q, 'додано лише нулі чисельника і знаменника'))
    return T.add(lv, f'Знайдіть суму всіх цілих розв’язків нерівності (x {M if p > 0 else "+"} {abs(p)}) / (x {M if q > 0 else "+"} {abs(q)}) {OPS[op]} 0.', ans, wr, 'метод інтервалів: нуль знаменника завжди виключається; нуль чисельника входить лише при нестрогій нерівності', f'розв’язок {setstr(sol)}; цілі: {", ".join(str(i) for i in ints)}; сума {ans}')

def f_poly_ineq_count(T, rng, lv):
    a, b, c = rng.sample(range(-7, 8), 3)
    b, c = min(b, c), max(b, c)
    if c - b < 4: return False
    op = rng.choice(['<', '<='])
    sol = solve_gen({F(a): 2, F(b): 1, F(c): 1}, {}, 1, op)
    cnt = len(int_list(sol))
    cc = (op == '<=')
    def cnt_of(closed, a_in):
        base = set(range(b if closed else b + 1, (c + 1) if closed else c))
        if a_in: base.add(a)
        else: base.discard(a)
        return len(base)
    wr = []
    for closed, a_in in ((not cc, cc), (cc, not cc), (not cc, not cc)):
        why = []
        if closed != cc: why.append(f'кінці {b} і {c} ' + ('включено, хоча нерівність строга' if closed else 'не включено, хоча нерівність нестрога'))
        if a_in != cc: why.append(f'точку x = {a} ' + ('включено, хоча в ній вираз дорівнює нулю, а нерівність строга' if a_in else 'виключено, хоча в ній вираз дорівнює нулю, а нерівність нестрога'))
        wr.append((cnt_of(closed, a_in), '; '.join(why)))
    wr.append((len(set(range(b, c + 1)) | {a}), 'усі нулі виразу прийнято за розв’язки'))
    return T.add(lv, f'Скільки цілих розв’язків має нерівність {fac(a, 2)}{fac(b)}{fac(c)} {OPS[op]} 0?', cnt, wr, 'множник у парному степені не змінює знака, але дає нуль у точці x = ' + fmt(a), f'нулі: {fmt(a)} (кратність 2), {b}, {c}; розв’язок {setstr(sol)}; цілих: {cnt}')

def f_rat_ineq3(T, rng, lv):
    pat = rng.choice(['nn_d', 'n_dd', 'nn_dd', 'sq_d'])
    rts = rng.sample(range(-8, 9), 4)
    if pat == 'nn_d': num = {rts[0]: 1, rts[1]: 1}; den = {rts[2]: 1}
    elif pat == 'n_dd': num = {rts[0]: 1}; den = {rts[1]: 1, rts[2]: 1}
    elif pat == 'nn_dd': num = {rts[0]: 1, rts[1]: 1}; den = {rts[2]: 1, rts[3]: 1}
    else: num = {rts[0]: 2, rts[1]: 1}; den = {rts[2]: 1}
    op = rng.choice(list(OPS))
    numF = {F(k): v for k, v in num.items()}; denF = {F(k): v for k, v in den.items()}
    sol, wr = set_wrongs(numF, denF, 1, op)
    ntxt = ''.join(fac(r, m) for r, m in sorted(num.items())); dtxt = ''.join(fac(r, m) for r, m in sorted(den.items()))
    if pat == 'sq_d':
        sq = [r for r, m in num.items() if m == 2][0]
        wr.append((setstr(solve_gen({k: 1 for k in numF}, denF, 1, op)), f'множник ({fac(sq)[1:-1]})² прийнято за звичайний: знак при переході через x = {sq} не змінюється'))
    return T.add(lv, f'Розв’яжіть нерівність {ntxt} / {"(" + dtxt + ")" if len(den) > 1 else dtxt} {OPS[op]} 0.', setstr(sol), wr, 'метод інтервалів: корені парної кратності не змінюють знака; нулі знаменника не входять у розв’язок', f'критичні точки {", ".join(fmt(c) for c in sorted(set(num) | set(den)))}; відповідь {setstr(sol)}')

def f_irrat_ineq(T, rng, lv):
    a = rng.randint(1, 9); b = rng.choice([-3, -2, -1, 0, 1, 2, 3, 4, 5]); op = rng.choice(list(OPS))
    lo = F(-a); t = F(b * b - a); strict = op in ('<', '>'); less = op in ('<', '<=')
    if b < 0:
        sol = [] if less else [(lo, None, True, False)]
        how = (f'корінь невід’ємний, а {b} < 0, тому розв’язків немає' if less else f'корінь невід’ємний і завжди більший за {b}, тому розв’язок збігається з ОДЗ')
        alts = ([(setstr([(lo, t, True, False)]), 'піднесено до квадрата від’ємне число, не врахувавши його знак'), (setstr([(lo, None, True, False)]), 'вважали, що нерівність виконується в усій ОДЗ'), (setstr([(None, t, False, False)]), 'не враховано ОДЗ та знак правої частини'), (setstr([(t, None, False, False)]), 'піднесено до квадрата від’ємне число')]
                if less else
                [('розв’язків немає', 'вважали, що корінь не може бути більшим за від’ємне число'), (setstr([(t, None, False, False)]), 'піднесено до квадрата від’ємне число, що змінило розв’язок'), (setstr([(None, t, False, False)]), 'піднесено до квадрата від’ємне число і змінено знак'), (setstr([(lo, t, True, False)]), 'нерівність розв’язано як 0 ≤ A < b²')])
    else:
        if less:
            sol = [(lo, t, True, op == '<=')]
            how = f'0 ≤ x + {a} {OPS[op]} {b*b}; −{a} ≤ x {OPS[op]} {fmt(t)}'
            alts = [(setstr([(None, t, False, op == '<=')]), 'не враховано ОДЗ: підкореневий вираз має бути невід’ємним'), (setstr([(t, None, op == '<=', False)]), 'знак нерівності змінено після піднесення до квадрата'),
                    (setstr([(lo, t, True, op != '<=')]), f'нерівність строга, тому кінець {fmt(t)} не входить' if strict else f'нерівність нестрога, тому кінець {fmt(t)} входить'), (setstr([(lo, F(b), True, op == '<=')]), 'праву частину не піднесено до квадрата')]
        else:
            sol = [(t, None, op == '>=', False)]
            how = f'x + {a} {OPS[op]} {b*b}; x {OPS[op]} {fmt(t)}; ОДЗ x ≥ −{a} виконується автоматично'
            alts = [(setstr([(lo, t, True, False)]), 'розв’язано в протилежному напрямку'), (setstr([(lo, None, True, False)]), f'враховано лише ОДЗ x ≥ −{a}'), (setstr([(t, None, op != '>=', False)]), f'нерівність строга, тому кінець {fmt(t)} не входить' if strict else f'нерівність нестрога, тому кінець {fmt(t)} входить'), (setstr([(F(b), None, op == '>=', False)]), 'праву частину не піднесено до квадрата')]
    ans = setstr(sol)
    return T.add(lv, f'Розв’яжіть нерівність √(x + {a}) {OPS[op]} {fmt(b)}.', ans, alts, f'враховуйте ОДЗ (x + {a} ≥ 0) і те, що значення кореня невід’ємне', f'ОДЗ: x ≥ −{a}; {how}; відповідь {ans}')

def f_circle_sys(T, rng, lv):
    x, y = rng.sample([v for v in range(-7, 8) if v], 2); a = x * x + y * y; d = x - y
    kind = rng.choice(['xy', 'cnt'])
    if kind == 'xy':
        ans = x * y
        wr = [(a - d * d, 'не поділено на 2: 2xy = a − (x − y)²'), (F(a + d * d, 2), 'знак (x − y)² змінено'), (F(d * d, 2), 'взято лише (x − y)²/2'), (a * d, 'розв’язки перемножено без обчислень')]
        return T.add(lv, f'Нехай (x; y) — розв’язок системи {{ x² + y² = {a}, x − y = {d} }}. Знайдіть xy.', ans, wr, 'x² + y² = (x − y)² + 2xy', f'{a} = {d}² + 2xy; 2xy = {a - d*d}; xy = {fmt(ans)}')
    a2 = rng.randint(2, 30); d2 = rng.randint(1, 8); D4 = 2 * a2 - d2 * d2
    cnt = 2 if D4 > 0 else 1 if D4 == 0 else 0
    names = {0: 'жодного', 1: 'один', 2: 'два', 4: 'чотири'}
    why = {0: 'розв’язків немає лише коли 2a < d²', 1: 'один розв’язок — лише при 2a = d²', 2: 'два розв’язки — при 2a > d²', 4: 'кожному значенню x відповідає лише один y = x − d'}
    wr = [(names[k], why[k] + f', а тут 2·{a2} {"<" if D4 < 0 else "=" if D4 == 0 else ">"} {d2*d2}') for k in (0, 1, 2) if k != cnt]
    wr.append(('чотири', why[4]))
    return T.add(lv, f'Скільки розв’язків (x; y) має система {{ x² + y² = {a2}, x − y = {d2} }}?', names[cnt], wr, 'підставте y = x − d у перше рівняння й дослідіть дискримінант', f'x² + (x − {d2})² = {a2}; 2x² − {2*d2}x + {d2*d2 - a2} = 0; D = {4 * D4} {">" if D4 > 0 else "=" if D4 == 0 else "<"} 0; розв’язків: {names[cnt]}')

def f_exp_system(T, rng, lv):
    b = rng.choice([2, 3, 5]); s = rng.randint(3, 8); d = rng.choice([v for v in range(1, s) if (s + v) % 2 == 0])
    x, y = (s + d) // 2, (s - d) // 2
    wr = [(y, 'знайдено y, а не x'), (s, 'знайдено суму x + y'), (d, 'знайдено різницю x − y'), (x * y, 'знайдено добуток xy')]
    return T.add(lv, f'Розв’яжіть систему {{ {b}^x · {b}^y = {b ** s}, x − y = {d} }}. Чому дорівнює x?', x, wr, 'bˣ·bʸ = bˣ⁺ʸ, тому x + y = ' + str(s), f'x + y = {s}, x − y = {d}; x = {x}, y = {y}')

def f_log_sys(T, rng, lv):
    cands = [(b, k, d1, (b ** k) // d1) for b in (2, 3) for k in range(2, 6) for d1 in range(1, 40) if (b ** k) % d1 == 0 and d1 < (b ** k) // d1 and b ** k <= 400]
    b, k, d1, d2 = rng.choice(cands); sb = SB[b]
    wr = [(d1, 'знайдено менше число, а не більше'), (d1 + d2, 'знайдено суму чисел'), (b ** k, 'знайдено добуток чисел'), (d2 - d1, 'знайдено різницю чисел'), (k, 'відповіддю назвали праву частину першого рівняння')]
    return T.add(lv, f'Розв’яжіть систему {{ log{sb} x + log{sb} y = {k}, x + y = {d1 + d2} }}. Знайдіть більше з чисел x, y.', d2, wr, 'logₐx + logₐy = logₐ(xy), тому xy = a^k; x, y — корені t² − St + P = 0', f'xy = {b**k}, x + y = {d1 + d2}; t² − {d1+d2}t + {b**k} = 0; корені {d1} і {d2}')

def f_log_ineq_quad(T, rng, lv):
    b = rng.choice([2, 3]); k = rng.randint(2, 4 if b == 2 else 3); N = b ** k
    pairs = [(u_, N // u_) for u_ in range(1, N + 1) if N % u_ == 0 and u_ != N // u_]
    u_, w_ = rng.choice(pairs); s = u_ - w_   # x² − s x ≤ N  ⇔  (x − u)(x + w) ≤ 0
    if s == 0: return False
    sb = SB[b]
    lo_b, hi_b = -w_, u_
    odz = lambda x: x * (x - s) > 0
    bound = lambda x, strict: (lo_b < x < hi_b) if strict else (lo_b <= x <= hi_b)
    ok = [x for x in range(lo_b - 2, hi_b + 3) if bound(x, False) and odz(x)]
    cnt = len(ok)
    wr = [(len([x for x in range(lo_b, hi_b + 1)]), 'ОДЗ (' + poly([1, -s, 0]) + ' > 0) не враховано'), (len([x for x in range(lo_b - 2, hi_b + 3) if bound(x, True) and odz(x)]), 'нерівність log ≤ k розв’язано як строгу: кінці відрізка відкинуто'),
          (len([x for x in range(lo_b - 2, hi_b + 3) if bound(x, False)]) - len([x for x in range(lo_b - 2, hi_b + 3) if bound(x, False) and not odz(x)]) + 1, 'враховано зайву точку, де аргумент логарифма дорівнює нулю'),
          (hi_b - lo_b, 'кількість цілих знайдено як різницю кінців')]
    return T.add(lv, f'Скільки цілих розв’язків має нерівність log{sb}({poly([1, -s, 0])}) ≤ {k}?', cnt, wr, 'log_b f(x) ≤ k ⇔ 0 < f(x) ≤ b^k (при b > 1)', f'0 < {poly([1, -s, 0])} ≤ {N}; перша: x ∉ [{min(0, s)}; {max(0, s)}]; друга: {lo_b} ≤ x ≤ {hi_b}; цілі розв’язки: {", ".join(str(i) for i in ok)}; усього {cnt}')

def f_log_def(T, rng, lv):
    b, N = rng.choice([(2, 5), (2, 7), (3, 5), (3, 7), (2, 3), (5, 2), (5, 3), (3, 2), (2, 9), (5, 7), (7, 3), (7, 5)])
    ans = f'log{SB.get(b, "_" + str(b))} {N}'
    sbN = lambda bb, nn: f'log{SB.get(bb, "_" + str(bb))} {nn}'
    wr = [(sbN(N, b), 'основу й аргумент логарифма переплутано'), (f'{N}/{b}', 'число поділено на основу'), (f'{N} − {b}', 'від числа віднято основу'), (f'√{N}' if N != b else '1', 'показник знайдено як корінь із числа')]
    return T.add(lv, f'Розв’яжіть рівняння {b}^x = {N}.', ans, wr, 'a^x = N ⇔ x = logₐ N, якщо N — не степінь числа a', f'x = log{SB.get(b, "_" + str(b))} {N}')

FAMS = [(f_lin_eq, [1]), (f_quad_roots, [1]), (f_incomplete, [1]), (f_lin_ineq, [1]), (f_sys_lin, [1]), (f_exp_eq, [1]), (f_log_eq, [1]), (f_sqrt_eq, [1]), (f_frac_eq, [1]), (f_discr_count, [1]), (f_vieta, [1, 2]), (f_abs_eq, [1]), (f_number_word, [1]),
        (f_quad_lead, [2]), (f_biquad, [2]), (f_quad_ineq, [2]), (f_rat_ineq, [2]), (f_sys_lin2, [2]), (f_sys_sym, [2]), (f_exp_eq2, [2]), (f_log_eq2, [2]), (f_irrat_eq, [2]), (f_trig_eq, [2]), (f_expo_ineq, [2]), (f_log_ineq, [2]), (f_int_count, [2]), (f_param_one, [2]), (f_param_two, [2]), (f_system_ineq, [2]), (f_rect_word, [2]), (f_lin_ineq2, [2]), (f_abs_ineq, [2, 3]), (f_log_def, [2]),
        (f_rat_eq_ext, [3]), (f_two_radicals, [3]), (f_exp_quad2, [3]), (f_log_quad, [3]), (f_abs_two, [3]), (f_trig_interval, [3]), (f_motion, [3]), (f_work, [3]), (f_vieta_adv, [3]), (f_param_all, [3]), (f_int_sum_rat, [3]), (f_poly_ineq_count, [3]), (f_rat_ineq3, [3]), (f_irrat_ineq, [3]), (f_circle_sys, [3]), (f_exp_system, [3]), (f_log_sys, [3]), (f_log_ineq_quad, [3])]
