import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mgen import *
import msvg as S
import math, itertools
from fractions import Fraction as F

T = Topic(2, 'alhebra')

def pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): r[i + j] += a * b
    return r
def padd(p, q):
    n = max(len(p), len(q)); p = [0] * (n - len(p)) + list(p); q = [0] * (n - len(q)) + list(q)
    return [a + b for a, b in zip(p, q)]
def pev(p, x):
    r = 0
    for c in p: r = r * x + c
    return r
def ppow(p, k):
    r = [1]
    for _ in range(k): r = pmul(r, p)
    return r
def lin(p, q, var='x'): return poly([p, q], var)
def fac(a, b):  # (a x + b)
    return '(' + lin(a, b) + ')'
def pt(p): return poly(p)
def rsgn(r): return f'{MINUS}{fmt(abs(r))}' if r < 0 else fmt(r)
def cs(c, name):  # коефіцієнт при змінній name
    if c == 0: return ''
    return ('' if abs(c) == 1 else fmt(abs(c))) + name

def lincomb(terms):
    """terms: [(coef, 'a'), …] → рядок"""
    out = ''
    for c, nm in terms:
        if c == 0: continue
        body = ('' if (abs(c) == 1 and nm) else fmt(abs(c))) + nm
        if not out: out = (MINUS if c < 0 else '') + body
        else: out += (' + ' if c > 0 else f' {MINUS} ') + body
    return out or '0'

# ===================== РІВЕНЬ 1 =====================
def f_square(T, rng, lv):
    p = rng.choice([1, 2, 3, 4, 5]); q = rng.choice([x for x in range(-8, 9) if x not in (0,)])
    if p == 1 and abs(q) == 1: return False
    ans = pt([p * p, 2 * p * q, q * q])
    wr = [(pt([p * p, 0, q * q]), 'пропущено подвоєний добуток 2ab'), (pt([p, 2 * p * q, q * q]) if p > 1 else pt([p * p, p * q, q * q]), 'коефіцієнт при першому доданку не піднесено до квадрата' if p > 1 else 'подвоєний добуток записано як ab'),
          (pt([p * p, -2 * p * q, q * q]), 'знак середнього доданка протилежний'), (pt([p * p, 2 * p * q, -q * q]), 'квадрат другого доданка записано зі знаком мінус'), (pt([p * p, p * q, q * q]), 'не подвоєно добуток')]
    return T.add(lv, f'Розкрийте дужки: ({lin(p, q)})².', ans, wr, '(a ± b)² = a² ± 2ab + b²: подвоєний добуток не губимо, а коефіцієнт піднесіть до квадрата',
                 f'({lin(p,q)})² = ({"x" if p==1 else str(p)+"x"})² + 2·{"x" if p==1 else str(p)+"x"}·({rsgn(q)}) + ({rsgn(q)})² = {ans}')

def f_diffsq(T, rng, lv):
    p = rng.choice([1, 2, 3, 4, 5, 6]); q = rng.randint(1, 9)
    if p == q: return False
    order = rng.choice([0, 1])
    f1, f2 = (lin(p, -q), lin(p, q)) if order else (lin(p, q), lin(p, -q))
    ans = pt([p * p, 0, -q * q])
    wr = [(pt([p * p, 0, q * q]), 'різницю квадратів прийнято за суму'), (pt([p * p, -2 * p * q, q * q]), 'застосовано формулу квадрата різниці'), (pt([p, 0, -q * q]) if p > 1 else pt([p * p, 0, -q]), 'один з доданків не піднесено до квадрата'), (pt([p * p, 0, -q * q * 2]), 'квадрат другого числа подвоєно')]
    return T.add(lv, f'Спростіть добуток: ({f1})({f2}).', ans, wr, '(a − b)(a + b) = a² − b²; середні доданки взаємно знищуються', f'({p}x)² − {q}² = {ans}')

def f_value(T, rng, lv):
    a = rng.choice([1, 2, 3, -1, -2, 4]); b = rng.choice([-5, -3, 2, 4, 6, -7]); c = rng.choice([-4, -1, 3, 5, 7]); k = rng.choice([-3, -2, -1, 2, 3, 4])
    v = a * k * k + b * k + c
    wr = [(-a * k * k + b * k + c, 'квадрат від’ємного числа знехтувано' if k < 0 else 'знак квадрата змінено'), ((a * k) ** 2 + b * k + c, 'до квадрата піднесено добуток a·k, а не k'), (a * k * k - b * k + c, 'знак другого доданка змінено'), (a * k + b * k + c, 'квадрат замінено першим степенем')]
    return T.add(lv, f'Знайдіть значення виразу {pt([a, b, c])} при x = {rsgn(k)}.', v, wr, 'підставляйте від’ємне число в дужках: (−3)² = 9, а не −9',
                 f'{rsgn(a)}·({rsgn(k)})² + ({rsgn(b)})·({rsgn(k)}) + ({rsgn(c)}) = {fmt(v)}')

def f_like(T, rng, lv):
    c1, c2, c3, c4 = [rng.choice([-6, -5, -4, -3, -2, 1, 2, 3, 4, 5, 6, 7]) for _ in range(4)]
    ans = lincomb([(c1 + c3, 'a'), (c2 + c4, 'b')])
    if c1 + c3 == 0 or c2 + c4 == 0: return False
    expr = lincomb([(c1, 'a'), (c2, 'b'), (c3, 'a'), (c4, 'b')]).replace(' + ', ' + ')
    wr = [(lincomb([(c1 + c3 + c2 + c4, 'a')]), 'змінні a і b вважали подібними доданками'), (lincomb([(c1 - c3, 'a'), (c2 + c4, 'b')]), 'коефіцієнти при a віднято замість додавання'), (lincomb([(c1 + c3, 'a'), (c2 - c4, 'b')]), 'коефіцієнти при b віднято замість додавання'), (lincomb([(c1 * c3, 'a'), (c2 * c4, 'b')]), 'коефіцієнти перемножено замість додавання')]
    return T.add(lv, f'Зведіть подібні доданки: {expr}.', ans, wr, 'додаємо лише коефіцієнти при однакових буквених частинах', f'a: {rsgn(c1)} + ({rsgn(c3)}) = {rsgn(c1+c3)}; b: {rsgn(c2)} + ({rsgn(c4)}) = {rsgn(c2+c4)}')

def f_degree(T, rng, lv):
    a1, b1 = rng.randint(1, 5), rng.randint(1, 5); a2 = rng.randint(1, 7); b2 = rng.randint(0, 2)
    c1, c2 = rng.choice([2, 3, 5, -4]), rng.choice([1, -2, 6])
    d1, d2 = a1 + b1, a2 + b2
    if d1 == d2: return False
    def mono(c, ex, ey):
        s = '' if abs(c) == 1 else str(abs(c)); 
        s += ('x' + (sup(ex) if ex > 1 else '') if ex else '') + ('y' + (sup(ey) if ey > 1 else '') if ey else '')
        return s
    expr = mono(c1, a1, b1) + (f' {"+" if c2 > 0 else MINUS} ') + mono(c2, a2, b2)
    if c1 < 0: expr = MINUS + expr
    deg = max(d1, d2)
    wr = [(max(a1, b1, a2, b2), 'взято найбільший показник однієї змінної, а не суму показників у одночлені'), (min(d1, d2), 'взято найменший степінь серед одночленів'), (d1 + d2, 'степені одночленів додано'), (a1 * b1 if d1 > d2 else a2 * b2 + 1, 'показники перемножено')]
    return T.add(lv, f'Знайдіть степінь многочлена {expr}.', deg, wr, 'степінь одночлена — сума показників усіх змінних; степінь многочлена — найбільший зі степенів його одночленів', f'степені одночленів: {d1} і {d2}; найбільший — {deg}')

def f_common(T, rng, lv):
    g = rng.choice([2, 3, 4, 5, 6]); m = rng.randint(1, 3); a = rng.choice([1, 2, 3, 4]); b = rng.choice([-5, -3, -2, 2, 3, 5, 7])
    if math.gcd(a, abs(b)) != 1: return False
    e = rng.randint(1, 2)
    expr = pt([g * a] + [0] * (e - 1) + [g * b] + [0] * m) if False else pt([g * a] + [0] * (e - 1 + 1 - 1) + [0] * 0 + [0] * (m + e - e) if False else [g * a] + [0] * e + [0] * 0)
    # g a x^(m+e) + g b x^m
    co = [g * a] + [0] * (e - 1) + [0] * m + [g * b] + [0] * m if False else None
    n1 = m + e
    co = [g * a] + [0] * (n1 - m - 1) + [g * b] + [0] * m
    expr = pt(co)
    fx = 'x' + (sup(m) if m > 1 else '')
    inner = pt([a] + [0] * (e - 1) + [b])
    ans = f'{g}{fx}({inner})'
    wr = [(f'{g}({pt([a] + [0] * (n1 - 1 - 0 + 0 - (n1 - m - 1) - 1 + (n1 - m - 1)) if False else [a] + [0] * (n1 - m - 1) + [b] + [0] * m)})', 'змінну не винесено за дужки — розклад неповний'),
          (f'{g}{fx}({pt([a] + [0] * (e - 1) + [-b])})', 'знак другого доданка в дужках змінено'),
          (f'{fx}({pt([g * a] + [0] * (e - 1) + [g * b])})', 'числовий множник не винесено — розклад неповний')]
    if m >= 2: wr.append((f'{g}{"x" + (sup(m - 1) if m > 2 else "")}({pt([a] + [0] * e + [b] + [0] * 0 if False else [a] + [0] * (e) + [0] * 0 + [0] * 0)})'.replace('()', '') if False else f'{g}{"x" + (sup(m - 1) if m > 2 else "")}({pt([a] + [0] * (e - 1) + [b] + [0]) if False else pt([a] + [0] * (e) + [b] + [0] * 0) if False else pt([a] + [0] * (e - 1) + [0]) if False else pt([a] + [0] * e + [0]) if False else "ax"})', 'змінну винесено не в найменшому степені') if False else (f'{g}x{sup(m - 1) if m > 2 else ""}({pt([a] + [0] * (e) + [b, 0] if False else [a] + [0] * e + [b] + [0])})', 'змінну винесено не в найменшому степені — розклад неповний'))
    else: wr.append((f'{g * a}{fx}({pt([1] + [0] * (e - 1) + [F(b, a)])})' if a > 1 else f'{g}{fx}({pt([a] + [0] * (e - 1) + [b + g])})', 'внутрішній коефіцієнт підібрано неточно'))
    return T.add(lv, f'Винесіть спільний множник за дужки: {expr}.', ans, wr, 'виносьте НСД коефіцієнтів і найменший степінь змінної', f'НСД коефіцієнтів {g}, змінна {fx}; {expr} = {ans}')

def f_powers(T, rng, lv):
    k = rng.choice(['mul', 'pow', 'frac'])
    if k == 'mul':
        a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(1, 5)
        ans = f'x{sup(a + b - c)}' if a + b - c != 1 else 'x'
        wr = [(f'x{sup(a * b - c)}', 'показники при множенні перемножено'), (f'x{sup(a + b + c)}', 'показник знаменника додано'), (f'x{sup(a + b * c)}' , 'неправильний порядок дій з показниками'), (f'x{sup((a + b) // c if (a+b)%c==0 else a+b-c+2)}', 'показники поділено')]
        return T.add(lv, f'Спростіть вираз: (x{sup(a)} · x{sup(b)}) : x{sup(c)}.', ans, wr, 'при множенні степенів показники додають, при діленні — віднімають', f'{a} + {b} − {c} = {a+b-c}')
    if k == 'pow':
        c = rng.choice([2, 3, -2, 4, 5]); m = rng.randint(2, 5); n = rng.choice([2, 3])
        co = c ** n
        ans = f'{rsgn(co)}x{sup(m * n)}' if abs(co) != 1 else (f'{"−" if co<0 else ""}x{sup(m*n)}')
        wr = [(f'{rsgn(c)}x{sup(m * n)}', 'коефіцієнт не піднесено до степеня'), (f'{rsgn(co)}x{sup(m + n)}', 'показники додано замість множення'), (f'{rsgn(c * n)}x{sup(m * n)}', 'коефіцієнт помножено на показник'), (f'{rsgn(-co if c > 0 else abs(co))}x{sup(m * n)}', 'неправильний знак коефіцієнта')]
        return T.add(lv, f'Спростіть: ({rsgn(c)}x{sup(m)}){sup(n)}.', ans, wr, '(ab)ⁿ = aⁿbⁿ і (xᵐ)ⁿ = xᵐⁿ: числовий множник теж підносимо до степеня', f'({rsgn(c)}){sup(n)} = {rsgn(co)}; {m}·{n} = {m*n}')
    a, b = rng.randint(2, 4), rng.randint(2, 4)
    c = rng.randint(1, 3)
    # (x^(a+c) y^b)/(x^c y)
    ans = f'x{sup(a)}y{sup(b - 1)}' if b - 1 > 1 else (f'x{sup(a)}y' if b == 2 else f'x{sup(a)}')
    wr = [(f'x{sup(a + 2 * c)}y{sup(b - 1)}', 'показники x додано замість віднімання'), (f'x{sup(a)}y{sup(b + 1)}', 'показники y додано замість віднімання'), (f'x{sup(a - c)}y{sup(b - 1)}', 'показник x віднято двічі')]
    return T.add(lv, f'Спростіть дріб: (x{sup(a + c)}y{sup(b)}) / (x{sup(c)}y).', ans, wr, 'ділення степенів з однаковою основою — віднімання показників; кожна змінна окремо', f'x: {a + c} − {c} = {a}; y: {b} − 1 = {b - 1}')

def f_log_basic(T, rng, lv):
    b = rng.choice([2, 3, 4, 5, 10]); k = rng.choice([-3, -2, -1, 0, 1, 2, 3, 4, 5])
    if b == 10 and abs(k) > 3: return False
    if b == 5 and (k > 3 or k < -2): return False
    if b == 4 and k > 3: return False
    val = F(b) ** k
    nm = 'lg' if b == 10 else f'log{"₂₃₄₅"[b-2] if b<6 else b}'
    arg = fmt(val)
    wr = [(k + 1, 'показник степеня збільшено на 1'), (k - 1, 'показник степеня зменшено на 1'), (val, 'знайдено саме число під логарифмом, а не показник степеня'), (-k if k else 1, 'знак показника змінено'), (b * k, 'основу помножено на показник')]
    return T.add(lv, f'Обчисліть: {nm} {arg}.', k, wr, 'logₐ b — це показник степеня, до якого треба піднести a, щоб отримати b', f'{b}{sup(k)} = {arg}, отже {nm} {arg} = {k}')

TRIG = {0: ('0', '0', '0'), 30: ('1/2', '√3/2', '√3/3'), 45: ('√2/2', '√2/2', '1'), 60: ('√3/2', '1/2', '√3'), 90: ('1', '0', None), 120: ('√3/2', '−1/2', '−√3'), 135: ('√2/2', '−√2/2', '−1'), 150: ('1/2', '−√3/2', '−√3/3'),
        180: ('0', '−1', '0'), 210: ('−1/2', '−√3/2', '√3/3'), 225: ('−√2/2', '−√2/2', '1'), 240: ('−√3/2', '−1/2', '√3'), 270: ('−1', '0', None), 300: ('−√3/2', '1/2', '−√3'), 315: ('−√2/2', '√2/2', '−1'), 330: ('−1/2', '√3/2', '−√3/3')}
FN = ['sin', 'cos', 'tg']
def f_trig_table(T, rng, lv):
    ang = rng.choice([a for a in TRIG if a not in (0,)]); fi = rng.randrange(3)
    ans = TRIG[ang][fi]
    if ans is None: return False
    pool = {}
    for a2, vals in TRIG.items():
        for j in range(3):
            if vals[j] is not None and vals[j] != ans and (a2, j) != (ang, fi): pool.setdefault(vals[j], (FN[j], a2))
    cand = [v for v in pool if v not in ('0',)]
    near = [v for v in (TRIG[ang][(fi + 1) % 3], TRIG[ang][(fi + 2) % 3], ans.replace('−', '') if ans.startswith('−') else '−' + ans) if v and v != ans]
    wr = []
    for v in near + rng.sample(cand, min(6, len(cand))):
        if v in [w[0] for w in wr] or v == ans: continue
        f2, a2 = pool.get(v, (None, None))
        if v == ('−' + ans if not ans.startswith('−') else ans[1:]): why = 'знак значення визначено неправильно (перевірте чверть)'
        elif f2: why = f'це значення {f2} {a2}°, а не {FN[fi]} {ang}°'
        else: why = 'значення іншої тригонометричної функції'
        wr.append((v, why))
    return T.add(lv, f'Знайдіть значення виразу {FN[fi]} {ang}°.', ans, wr[:5], 'пригадайте таблицю значень для 30°, 45°, 60° і знак функції у відповідній чверті', f'{ang}° лежить у {["I", "II", "III", "IV"][(ang - 1) // 90]} чверті, табличне значення: {FN[fi]} {ang}° = {ans}')

def f_deg_rad(T, rng, lv):
    p, q = rng.choice([(1, 6), (1, 4), (1, 3), (1, 2), (2, 3), (3, 4), (5, 6), (7, 6), (5, 4), (4, 3), (3, 2), (5, 3), (7, 4), (11, 6), (2, 9), (5, 12)])
    deg = F(180 * p, q)
    if deg.denominator != 1: return False
    if rng.random() < 0.5:
        d = int(deg)
        wr = [(f'{d + 30}°' if d + 30 < 360 else f'{d - 30}°', 'арифметична помилка при множенні'), (f'{int(F(360 * p, q))}°' if F(360*p,q) != deg else f'{d+15}°', 'взято π = 360°'), (f'{int(F(90 * p, q))}°' if F(90*p,q).denominator == 1 else f'{d - 15}°', 'взято π = 90°'), (f'{int(F(100*p,q))}°' if F(100*p,q).denominator==1 else f'{d+45}°', 'π прийнято за 100°')]
        return T.add(lv, f'Виразіть у градусах: {p if p>1 else ""}π/{q}.'.replace('1π', 'π').replace(' π', 'π'), f'{d}°', wr, 'π радіанів = 180°, тому x π/q рад = x·180°/q', f'{p}·180°/{q} = {d}°')
    d = int(deg)
    ans = f'{p if p>1 else ""}π/{q}'
    wr = [(f'{q if q>1 else ""}π/{p}', 'чисельник і знаменник переставлено'), (f'{p + 1}π/{q}', 'неправильно скорочено дріб'), (f'{p}π/{q + 1}', 'неправильно скорочено дріб'), (f'{d}π/180', 'градуси замінено на радіани без скорочення на 180')]
    return T.add(lv, f'Виразіть у радіанах: {d}°.', ans, wr, '1° = π/180 рад: множимо кут на π/180 і скорочуємо', f'{d}·π/180 = {ans}')

def f_domain(T, rng, lv):
    a = rng.randint(1, 9); k = rng.choice(['sqrt', 'sqrt2', 'log', 'frac', 'frac2', 'sqrtfrac'])
    s = lambda t: t.replace('-', MINUS)
    if k == 'sqrt': expr, ans, w = f'√({a} − x)', f'x ≤ {a}', [(f'x ≥ {a}', 'знак нерівності змінено'), (f'x < {a}', 'підкореневий вираз може дорівнювати 0, тому нерівність нестрога'), (f'x ≠ {a}', 'умова для дробу, а не для кореня'), (f'x ≤ {MINUS}{a}', 'не враховано знак при x')]
    elif k == 'sqrt2': expr, ans, w = f'√(2x − {2*a})', f'x ≥ {a}', [(f'x > {a}', 'підкореневий вираз може дорівнювати 0'), (f'x ≥ {2 * a}', 'не поділено на коефіцієнт 2'), (f'x ≤ {a}', 'знак нерівності змінено'), (f'x ≠ {a}', 'умова для дробу, а не для кореня')]
    elif k == 'log': expr, ans, w = f'log₂({MINUS}x + {a})' if False else f'log₂(x − {a})', f'x > {a}', [(f'x ≥ {a}', 'вираз під логарифмом має бути строго додатним'), (f'x < {a}', 'знак нерівності змінено'), (f'x ≠ {a}', 'умова для дробу, а не для логарифма'), (f'x > {MINUS}{a}', 'знак числа змінено')]
    elif k == 'frac': expr, ans, w = f'x / (x² − {a*a})', f'x ≠ {MINUS}{a} і x ≠ {a}', [(f'x ≠ {a}', 'пропущено другий корінь знаменника'), (f'x ≠ {a * a}', 'знаменник прирівняно до числа a², а не розв’язано x² = a²'), (f'x > {a}', 'вираз має зміст не лише при x > a'), (f'x ≠ 0', f'нулю має дорівнювати знаменник x² − {a*a}, а не x')]
    elif k == 'frac2': expr, ans, w = f'1 / (x + {a})', f'x ≠ {MINUS}{a}', [(f'x ≠ {a}', 'знак кореня знаменника переплутано'), (f'x > {MINUS}{a}', 'на область визначення дробу немає обмеження знаку'), (f'x ≥ {MINUS}{a}', 'на область визначення дробу немає обмеження знаку'), (f'x ≠ 0', f'нулю має дорівнювати знаменник x + {a}, а не x')]
    else: expr, ans, w = f'√(x − {a}) / (x − {a + 2})', f'x ≥ {a}, x ≠ {a + 2}', [(f'x > {a}', 'підкореневий вираз може дорівнювати нулю'), (f'x ≥ {a}', 'не виключено нуль знаменника'), (f'x ≠ {a + 2}', 'не враховано умову для кореня'), (f'x > {a}, x ≠ {a + 2}', 'корінь існує і при x = a')]
    return T.add(lv, f'Знайдіть область допустимих значень виразу {expr}.', ans, w, 'ОДЗ: корінь парного степеня — підкореневий вираз ≥ 0; знаменник ≠ 0; логарифм — аргумент > 0', f'для {expr}: {ans}')

def f_cancel_num(T, rng, lv):
    a = rng.randint(2, 6); b = rng.randint(1, 4); m = rng.choice([2, 3, 4, 5, 6])
    if b % 1: return False
    if (a * m) % m: return False
    # (m a x + m b)/m = a x + b  ; (A x^2 - B x)/(c x)
    k = rng.choice([0, 1])
    if k == 0:
        num = pt([m * a, m * b]); ans = pt([a, b])
        wr = [(pt([m * a, b]), 'поділено лише перший доданок'), (pt([a, m * b]), 'поділено лише другий доданок'), (pt([a, b * m * m]), 'другий доданок помножено замість ділення'), (pt([m * a, m * b]) if False else f'{a}x + {b}' if False else pt([a, -b]), 'знак другого доданка змінено')]
        return T.add(lv, f'Скоротіть дріб ({num}) / {m}.', ans, wr, 'щоб скоротити суму, діліть на число кожен доданок', f'({m*a}x + {m*b}) : {m} = {ans}'.replace('+ -', '− '))
    c = rng.choice([2, 3, 4]); A = c * a; B = c * b
    num = pt([A, -B, 0]); ans = pt([a, -b])
    wr = [(pt([a, -B]), 'другий доданок не поділено на коефіцієнт'), (pt([A, -b]), 'перший доданок не поділено на коефіцієнт'), (pt([a, 0, -b]) if False else f'{a}x² − {b}', 'змінну поділено лише в одному доданку'), (pt([a, b]), 'знак змінено')]
    return T.add(lv, f'Скоротіть дріб ({num}) / ({c}x), x ≠ 0.', ans, wr, 'виносьте множник за дужки у чисельнику й скорочуйте з дільником', f'({num}) = {c}x({ans}), тому результат {ans}')

def f_brackets(T, rng, lv):
    a, b, c, d, e = [rng.choice([1, 2, 3, 4, 5, 6]) for _ in range(5)]
    s1 = rng.choice([-1, 1]); 
    # c0 - (a x - b) + d (x - e)  ;   a x + b
    c0 = rng.randint(1, 9)
    co_x = -a + d; const = c0 + b - d * e
    ans = pt([co_x, const])
    if co_x == 0: return False
    wr = [(pt([-a + d, c0 - b - d * e]), 'знак «мінус» перед дужкою не змінив знак другого доданка в дужці'), (pt([a + d, c0 + b - d * e]), 'знак першого доданка в дужці не змінено'), (pt([-a + d, c0 + b - e]), 'множник перед дужкою не помножено на другий доданок у дужці'), (pt([-a + d, c0 + b + d * e]), 'знак добутку d·(−e) втрачено')]
    return T.add(lv, f'Розкрийте дужки та спростіть: {c0} − ({lin(a, -b)}) + {d}({lin(1, -e)}).', ans, wr, 'мінус перед дужкою змінює знаки всіх доданків у ній; число перед дужкою множимо на кожен доданок', f'{c0} − {a}x + {b} + {d}x − {d*e} = {ans}')

# ===================== РІВЕНЬ 2 =====================
def rfac(r): return f'(x {"−" if r > 0 else "+"} {abs(r)})'
def f_factor_trinomial(T, rng, lv):
    p, q = rng.sample([x for x in range(-9, 10) if x != 0], 2)
    if p + q == 0: return False
    b, c = -(p + q), p * q
    ans = ' '.join(sorted([rfac(p), rfac(q)]))
    ans = rfac(p) + rfac(q)
    wr = [(rfac(-p) + rfac(-q), 'знаки коренів змінено: добуток c правильний, а сума — ні'), ]
    # інші розклади числа c
    divs = [d for d in range(-abs(c), abs(c) + 1) if d != 0 and c % d == 0]
    for d in divs:
        e = c // d
        if {d, e} != {p, q} and {d, e} != {-p, -q} and abs(d) <= abs(e):
            wr.append((rfac(d) + rfac(e), f'добуток {rsgn(d)}·{rsgn(e)} = {c} правильний, але сума коренів {rsgn(d + e)}, а має бути {rsgn(p + q)}'))
    wr.append((rfac(p) + rfac(-q), 'знак одного кореня змінено'))
    return T.add(lv, f'Розкладіть на множники квадратний тричлен {pt([1, b, c])}.', ans, wr[:5], 'за теоремою Вієта: x₁ + x₂ = −b, x₁ · x₂ = c; тоді x² + bx + c = (x − x₁)(x − x₂)', f'x₁ = {p}, x₂ = {q}: {pt([1,b,c])} = {ans}')

def f_factor_lead(T, rng, lv):
    for _ in range(100):
        m, n, k, l = rng.randint(1, 4), rng.choice([x for x in range(-6, 7) if x]), rng.randint(1, 3), rng.choice([x for x in range(-6, 7) if x])
        if m == 1 and k == 1: continue
        if m * l == n * k or (m, n) == (k, l): continue
        co = pmul([m, n], [k, l])
        if math.gcd(math.gcd(abs(co[0]), abs(co[1])), abs(co[2])) == 1: break
    else: return False
    ans = fac(m, n) + fac(k, l)
    wr = [(fac(m, -n) + fac(k, -l), 'знаки в дужках змінено'), (fac(m, l) + fac(k, n), 'вільні члени в дужках переставлено'), (fac(1, n) + fac(m * k, l), 'коефіцієнти розподілено неправильно'), (fac(m, n) + fac(k, -l), 'знак у другій дужці змінено')]
    return T.add(lv, f'Розкладіть на множники: {pt(co)}.', ans, wr, 'перемножте запропоновані дужки й перевірте усі три коефіцієнти', f'({lin(m,n)})({lin(k,l)}) = {pt(co)}')

def f_simplify_rat(T, rng, lv):
    p, q = rng.sample([x for x in range(-6, 7) if x != 0], 2)
    r = rng.choice([x for x in range(1, 6) if x != abs(p)])
    # (x-p)(x-q) / ((x-p)(x+... ))  → (x-q)/(x-s)
    s = rng.choice([x for x in range(-6, 7) if x not in (0, p, q)])
    num = pmul([1, -p], [1, -q]); den = pmul([1, -p], [1, -s])
    ans = f'({lin(1, -q)}) / ({lin(1, -s)})'
    wr = [(f'({lin(1, q)}) / ({lin(1, s)})', 'знаки коренів змінено'), (f'({lin(1, -s)}) / ({lin(1, -q)})', 'чисельник і знаменник переставлено'), (f'({pt(num[1:])}) / ({pt(den[1:])})', 'скорочено x² як окремий множник — так робити не можна'), (f'({lin(1, -q)}) / ({lin(1, -p)})', 'у знаменнику залишився скорочений множник')]
    return T.add(lv, f'Скоротіть дріб ({pt(num)}) / ({pt(den)}), якщо x ≠ {rsgn(p)} і x ≠ {rsgn(s)}.', ans, wr, 'розкладіть чисельник і знаменник на множники й скоротіть лише однакові множники', f'({lin(1,-p)})({lin(1,-q)}) / (({lin(1,-p)})({lin(1,-s)})) = {ans}')

def f_add_frac(T, rng, lv):
    a = rng.randint(1, 6); p, q = rng.sample([1, 2, 3, 4, -1, -2, -3], 2)
    num = [p + q, a * (p - q)]
    den = [1, 0, -a * a]
    ans = f'({pt(num)}) / ({pt(den)})' if num[1] != 0 else f'{pt(num[:1] + [0])[:-0] if False else pt(num[:1] + [0]).rstrip("0")} / ({pt(den)})'
    if num[0] == 0 or num[1] == 0: return False
    alt = lambda n_: f'({pt(n_)}) / ({pt(den)})'
    wr = [(f'{p + q} / ({lin(2, 0)})', 'чисельники й знаменники дробів складено окремо'), (alt([p + q, -a * (p - q)]), 'знак вільного члена в чисельнику змінено'), (f'{p + q} / ({pt(den)})', 'у чисельнику загублено змінну'), (alt([p - q, a * (p + q)]), 'коефіцієнти в чисельнику розставлено неправильно')]
    return T.add(lv, f'Спростіть: {fmt(p) if p != 1 else ""}/({lin(1, -a)}) + {fmt(q) if q != 1 else ""}/({lin(1, a)}), якщо x ≠ ±{a}.'.replace('(1)', '1').replace('/(', '/(').replace(': /', ': 1/').replace('+ /', '+ 1/'), ans, wr,
                 'зведіть до спільного знаменника (x − a)(x + a) = x² − a²', f'{p}(x + {a}) + {q}(x − {a}) = {pt(num)}, знаменник {pt(den)}')

def f_sym_value(T, rng, lv):
    s = rng.randint(3, 12); p_ = rng.randint(-8, 14)
    if s * s - 4 * p_ < 0: return False
    kind = rng.choice(['sq', 'diff', 'cube'])
    if kind == 'sq':
        ans = s * s - 2 * p_
        wr = [(s * s, 'пропущено член −2ab'), (s * s + 2 * p_, 'знак подвоєного добутку змінено'), (s * s - p_, 'добуток не подвоєно'), (s + p_, 'суму та добуток складено')]
        return T.add(lv, f'Відомо, що a + b = {s} і ab = {fmt(p_)}. Знайдіть a² + b².', ans, wr, 'a² + b² = (a + b)² − 2ab', f'{s}² − 2·({fmt(p_)}) = {fmt(ans)}')
    if kind == 'diff':
        ans = s * s - 4 * p_
        wr = [(s * s - 2 * p_, 'у формулі (a − b)² взято 2ab замість 4ab'), (s * s + 4 * p_, 'знак добутку змінено'), (s * s, 'не враховано добуток ab'), (s - 2 * p_, 'суму не піднесено до квадрата')]
        return T.add(lv, f'Відомо, що a + b = {s} і ab = {fmt(p_)}. Знайдіть (a − b)².', ans, wr, '(a − b)² = (a + b)² − 4ab', f'{s}² − 4·({fmt(p_)}) = {fmt(ans)}')
    ans = s ** 3 - 3 * p_ * s
    wr = [(s ** 3, 'не враховано доданок −3ab(a + b)'), (s ** 3 + 3 * p_ * s, 'знак доданка −3ab(a + b) змінено'), (s ** 3 - 3 * p_, 'не помножено на (a + b)'), (s * s * s - p_ * s, 'коефіцієнт 3 втрачено')]
    return T.add(lv, f'Відомо, що a + b = {s} і ab = {fmt(p_)}. Знайдіть a³ + b³.', ans, wr, 'a³ + b³ = (a + b)³ − 3ab(a + b)', f'{s}³ − 3·({fmt(p_)})·{s} = {fmt(ans)}')

def f_remainder(T, rng, lv):
    deg = rng.choice([3, 3, 4]); co = [rng.choice([1, 2, -1, 3, -2]) ] + [rng.choice([-4, -3, -2, -1, 0, 1, 2, 3, 5]) for _ in range(deg)]
    a = rng.choice([1, 2, 3, -1, -2])
    v = pev(co, a)
    wr = [(pev(co, -a), 'підставлено −a замість a'), (sum(co), 'знайдено значення многочлена при x = 1'), (co[-1], 'взято вільний член'), (v + a, 'до значення додано a')]
    return T.add(lv, f'Знайдіть остачу від ділення многочлена {pt(co)} на двочлен x {"−" if a > 0 else "+"} {abs(a)}.', v, wr, 'теорема Безу: остача від ділення P(x) на (x − a) дорівнює P(a)', f'P({rsgn(a)}) = {fmt(v)}')

def f_cubes(T, rng, lv):
    k = rng.choice([1, 2, 3]); d = rng.choice([1, 2, 3, 4, 5]); sgn_ = rng.choice([1, -1])
    A = k; B = d
    expr = pt([k ** 3, 0, 0, sgn_ * d ** 3])
    s = '+' if sgn_ > 0 else '−'
    f1 = lin(k, sgn_ * d)
    f2 = pt([k * k, -sgn_ * k * d, d * d])
    ans = f'({f1})({f2})'
    wr = [(f'({f1}){sup(3)}', 'куб суми (різниці) замість суми (різниці) кубів'), (f'({f1})({pt([k * k, sgn_ * k * d, d * d])})', 'знак у середньому доданку неповного квадрата не змінено'), (f'({f1})({pt([k * k, -sgn_ * 2 * k * d, d * d])})', 'середній член подвоєно, як у повному квадраті'), (f'({lin(k, -sgn_ * d)})({f2})', 'знак у першому множнику протилежний')]
    return T.add(lv, f'Розкладіть на множники: {expr}.', ans, wr, 'a³ ± b³ = (a ± b)(a² ∓ ab + b²)', f'{expr} = ({"x" if k==1 else str(k)+"x"})³ {s} {d}³ = {ans}')

SUBL = '₂₃₄₅'
def f_logs(T, rng, lv):
    b = rng.choice([2, 3, 5]); k = rng.randint(1, 3); m = b ** k
    for _ in range(80):
        C = rng.choice([2, 3, 4, 5, 6, 8, 9]); B = rng.choice([2, 3, 4, 6, 8, 12, 9]); 
        if (m * C) % B: continue
        A = m * C // B
        if A not in (1, m) and A != B and A < 400: break
    else: return False
    nm = f'log{SUBL[b-2]}'
    wr = [(k + 1, 'помилка в обчисленні степеня'), (k - 1, 'помилка в обчисленні степеня'), (m, 'знайдено число під логарифмом, а не показник'), (A + B - C, 'логарифми «складено» як числа')]
    return T.add(lv, f'Обчисліть: {nm} {A} + {nm} {B} − {nm} {C}.', k, wr, 'logₐx + logₐy = logₐ(xy); logₐx − logₐy = logₐ(x/y)', f'{nm} ({A}·{B}/{C}) = {nm} {m} = {k}')

def rtxt(k, b): return f'√{b}' if k == 1 else f'{k}√{b}'
def f_radicals(T, rng, lv):
    k = rng.choice(['sq', 'diff', 'rat', 'conj'])
    if k == 'sq':
        p = rng.choice([2, 3, 5, 6, 7]); q = rng.choice([2, 3, 4]); b = p * q * q
        ans = p + b + 2 * p * q
        wr = [(p + b, 'пропущено подвоєний добуток коренів'), (p + b + p * q, 'добуток коренів не подвоєно'), (p + b - 2 * p * q, 'знак подвоєного добутку змінено'), (F(p * b), 'квадрат суми замінено добутком підкореневих чисел')]
        return T.add(lv, f'Обчисліть: (√{p} + √{b})².', ans, wr, '(a + b)² = a² + 2ab + b²; √p · √(pq²) = pq', f'{p} + {b} + 2·√{p*b} = {p} + {b} + {2*p*q} = {ans}')
    if k == 'diff':
        p = rng.choice([2, 3, 5, 7, 11]); q = rng.randint(1, 4)
        ans = p - q * q
        if p == q * q: return False
        wr = [(p + q * q, 'різницю квадратів прийнято за суму'), (p - q, 'число q не піднесено до квадрата'), (p * p - q * q, 'корінь піднесено до квадрата невірно'), (-(p + q * q) if False else q * q - p, 'порядок віднімання змінено')]
        return T.add(lv, f'Обчисліть: (√{p} + {q})(√{p} − {q}).', ans, wr, '(a + b)(a − b) = a² − b²', f'{p} − {q*q} = {ans}')
    if k == 'rat':
        c = rng.choice([2, 4, 6, 8, 10, 12, 15]); m = rng.choice([2, 3, 5, 6, 7])
        g = F(c, m)
        ans = f'{fmt(g)}√{m}' if g != 1 else f'√{m}'
        if g.denominator != 1 and False: return False
        ansv = (g.numerator, m) if g.denominator == 1 else None
        if g.denominator != 1: ans = f'{c}√{m}/{m}'
        wr = [(f'{c}√{m}', 'знаменник не враховано — множник √m не скорочено'), (f'{c}/{m}', 'корінь у чисельнику загублено'), (f'{c * m}√{m}', 'чисельник помножено на m замість ділення'), (f'{c}√{m}/{m * m}' if False else f'√{c * m}', 'множник m внесено під корінь без ділення')]
        return T.add(lv, f'Звільніться від ірраціональності в знаменнику: {c}/√{m}.', ans, wr, 'множимо чисельник і знаменник на √m: c/√m = c√m/m', f'{c}/√{m} = {c}√{m}/{m}' + (f' = {fmt(g)}√{m}' if g.denominator == 1 else ''))
    m, n_ = rng.choice([(5, 4), (7, 3), (10, 6), (6, 2), (11, 7), (8, 6), (13, 9), (7, 5)]); dm = m - n_
    c = dm * rng.choice([1, 2, 3])
    q = c // dm
    ans = (f'{q}(√{m} + √{n_})' if q > 1 else f'√{m} + √{n_}')
    wr = [(f'{q}(√{m} − √{n_})' if q > 1 else f'√{m} − √{n_}', 'знак між коренями в спряженому виразі не змінено'), (f'{c}(√{m} + √{n_})', 'не враховано, що знаменник дорівнює m − n'), (f'{c}(√{m} + √{n_}) / {m + n_}', 'у знаменнику суму замість різниці'), (f'√{m * n_}' if False else f'{q}√{m + n_}', 'корені «складено» під одним знаком')]
    return T.add(lv, f'Звільніться від ірраціональності в знаменнику: {c}/(√{m} − √{n_}).', ans, wr, 'множимо чисельник і знаменник на спряжений вираз: (√a − √b)(√a + √b) = a − b', f'{c}(√{m}+√{n_})/({m} − {n_}) = {ans}')

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]
def f_trig_ident(T, rng, lv):
    a, b, c = rng.choice(TRIPLES); quad = rng.choice([1, 1, 2, 3, 4]) if lv >= 2 else 1
    sin_s, cos_s = (1, 1) if quad == 1 else (1, -1) if quad == 2 else (-1, -1) if quad == 3 else (-1, 1)
    ask = rng.choice(['sin', 'cos', 'tg'])
    sw = rng.random() < .5
    sv, cv = (F(a, c), F(b, c)) if not sw else (F(b, c), F(a, c))
    sv *= sin_s; cv *= cos_s
    qname = {1: 'першої', 2: 'другої', 3: 'третьої', 4: 'четвертої'}[quad]
    given = rng.choice(['sin', 'cos'])
    if given == 'sin': g_txt = f'sin α = {fmt(sv)}'; need = [('cos', cv), ('tg', sv / cv)]
    else: g_txt = f'cos α = {fmt(cv)}'; need = [('sin', sv), ('tg', sv / cv)]
    nm, val = rng.choice(need)
    gv = sv if given == 'sin' else cv
    ur = {'cos': cv, 'sin': sv, 'tg': sv / cv}
    wr = [(-val, 'знак значення не відповідає чверті'), (1 / val if val != 0 else 1, 'знайдено обернену величину'), (F(1) - gv * gv if nm != 'tg' else gv, 'знайдено квадрат другої функції, не взято корінь')]
    w2 = [(x, r) for x, r in wr if x != val]
    # додаткові: решта з тригонометричних значень
    for nm2, v2 in ur.items():
        if nm2 != nm and v2 != val: w2.append((v2, f'знайдено значення {nm2} α, а не {nm} α'))
    return T.add(lv, f'Відомо, що {g_txt} і α — кут {qname} чверті. Знайдіть {nm} α.', val, w2, 'sin²α + cos²α = 1; знак функції визначається чвертю: sin > 0 в I–II, cos > 0 в I і IV', f'модуль {nm} α знаходимо з sin²α + cos²α = 1; у {qname} чверті {nm} α {"додатний" if val > 0 else "від’ємний"}, тому {nm} α = {fmt(val)}')

REDF = [('sin(π − α)', 1, 0), ('cos(π − α)', 0, -1), ('sin(π/2 + α)', 0, 1), ('cos(π/2 + α)', -1, 0), ('sin(π + α)', -1, 0), ('cos(π + α)', 0, -1), ('sin(2π − α)', -1, 0), ('cos(−α)', 0, 1), ('sin(−α)', -1, 0), ('cos(π/2 − α)', 1, 0), ('sin(π/2 − α)', 0, 1), ('cos(2π − α)', 0, 1)]
def f_reduction(T, rng, lv):
    (t1, s1, c1), (t2, s2, c2) = rng.sample(REDF, 2)
    op = rng.choice([1, -1])
    S_, C_ = s1 + op * s2, c1 + op * c2
    if (S_, C_) == (0, 0) and rng.random() < .7: return False
    def ex(S_, C_): return lincomb([(S_, 'sin α'), (C_, 'cos α')])
    ans = ex(S_, C_)
    wr = [(ex(-S_, -C_), 'всі знаки змінено навпаки'), (ex(s1 - op * s2, c1 - op * c2), 'знак другого доданка змінено на протилежний'), (ex(S_ + C_ if False else C_, S_), 'sin і cos переплутано (кофункція)'), (ex(S_ * 2, C_ * 2) if (S_, C_) != (0, 0) else ex(2, 0), 'результат подвоєно')]
    return T.add(lv, f'Спростіть вираз: {t1} {"+" if op > 0 else "−"} {t2}.', ans, wr, 'формули зведення: перед функцією ставимо знак початкової функції у відповідній чверті; для π/2 ± α функція змінюється на кофункцію', f'{t1} = {ex(s1, c1)}; {t2} = {ex(s2, c2)}; результат {ans}')

def rsym(q): return {2: '√', 3: '∛', 4: '∜'}.get(q, sup(q) + '√')
def f_rat_exp(T, rng, lv):
    r, q = rng.choice([(2, 3), (3, 3), (4, 2), (2, 4), (3, 2), (5, 2), (2, 5), (10, 3), (3, 4)]); p = rng.choice([1, 2, 3, -1, -2, -3, 5, -4])
    if math.gcd(abs(p), q) != 1: return False
    base = r ** q
    if base > 1000 or (q == 3 and abs(p) > 2) or abs(p) > 3 and q > 2: return False
    val = F(r) ** p
    wr = [(F(base) ** p, 'корінь не добуто: основу піднесено до всього показника'), (F(r) ** (-p), 'знак показника змінено'), (F(r) * p, 'основу помножено на показник'), (F(r) ** (p + 1), 'показник степеня збільшено на 1'), (F(r) ** (p - 1), 'показник степеня зменшено на 1')]
    return T.add(lv, f'Обчисліть: {base}^({rsgn(p)}/{q}).', val, wr, 'a^(p/q) = (ᵠ√a)ᵖ: спершу корінь q-го степеня, потім степінь p; від’ємний показник — обернене число', f'{rsym(q)}{base} = {r}; {r}^({rsgn(p)}) = {fmt(val)}')

def f_coef_sum(T, rng, lv):
    a, b = rng.choice([1, 2, 3]), rng.choice([-1, -2, 1, 2, -3]); n_ = rng.choice([2, 3, 4]); c, d = rng.choice([1, 2, -1]), rng.choice([2, 3, -2, 1])
    P = pmul(ppow([a, b], n_), [c, d])
    kind = rng.choice(['sum', 'free', 'alt'])
    if kind == 'sum':
        v = pev(P, 1)
        wr = [(pev(P, -1), 'знайдено значення при x = −1'), (pev(P, 0), 'знайдено вільний член'), (P[0], 'взято старший коефіцієнт'), (v + 1, 'до відповіді додано зайву одиницю')]
        return T.add(lv, f'Знайдіть суму всіх коефіцієнтів многочлена P(x) = ({lin(a, b)}){sup(n_)}({lin(c, d)}) після розкриття дужок.', v, wr, 'сума коефіцієнтів многочлена дорівнює P(1)', f'P(1) = ({a + b}){sup(n_)}·({c + d}) = {fmt(v)}')
    if kind == 'free':
        v = P[-1]
        wr = [(pev(P, 1), 'знайдено суму коефіцієнтів'), (P[0], 'взято старший коефіцієнт'), (pev(P, -1), 'знайдено значення при x = −1'), (v * -1 if v else 1, 'знак вільного члена змінено')]
        return T.add(lv, f'Знайдіть вільний член многочлена P(x) = ({lin(a, b)}){sup(n_)}({lin(c, d)}) після розкриття дужок.', v, wr, 'вільний член многочлена дорівнює P(0)', f'P(0) = ({b}){sup(n_)}·({d}) = {fmt(v)}')
    v = pev(P, 1) - 2 * 0
    alt = pev(P, -1)
    wr = [(pev(P, 1), 'знайдено суму всіх коефіцієнтів'), (pev(P, 0), 'знайдено вільний член'), (-alt, 'знак значення змінено'), (P[0], 'взято старший коефіцієнт')]
    return T.add(lv, f'Знайдіть значення P(−1) для многочлена P(x) = ({lin(a, b)}){sup(n_)}({lin(c, d)}), не розкриваючи дужок.', alt, wr, 'значення многочлена в точці знаходять підстановкою в добуток', f'P(−1) = ({rsgn(-a + b)}){sup(n_)}·({rsgn(-c + d)}) = {fmt(alt)}')

def f_poly_deg(T, rng, lv):
    a, b, c = rng.randint(1, 4), rng.randint(2, 4), rng.randint(2, 4)
    n1, n2 = rng.randint(2, 5), rng.randint(1, 4)
    deg = a * n1 + b * n2
    expr = f'(x{sup(n1)} + 1){sup(a)}(x{sup(n2)} − 2x){sup(b)}'
    if n2 == 1: expr = f'(x{sup(n1)} + 1){sup(a)}(x − 2){sup(b)}'
    wr = [(a + b + n1 + n2, 'показники всіх степенів додано'), (a * n1 + n2, 'не враховано показник другого множника'), (max(a * n1, b * n2), 'взято найбільший із степенів множників, а не їх суму'), (a * n1 * b * n2, 'степені перемножено')]
    return T.add(lv, f'Знайдіть степінь многочлена {expr}.', deg, wr, 'степінь добутку многочленів дорівнює сумі степенів; степінь (Pᵏ) — k · deg P', f'{a}·{n1} + {b}·{n2 if n2>1 else 1} = {deg}')

# ===================== РІВЕНЬ 3 =====================
def f_x_inv(T, rng, lv):
    k = rng.randint(3, 9); kind = rng.choice(['sq', 'cube', 'sqm'])
    if kind == 'sq':
        ans = k * k - 2
        wr = [(k * k, 'не віднято подвоєний добуток 2'), (k * k + 2, 'знак подвоєного добутку змінено'), (k * k - 1, 'подвоєний добуток записано як 1'), (2 * k, 'суму просто подвоєно')]
        return T.add(lv, f'Відомо, що x + 1/x = {k}. Знайдіть x² + 1/x².', ans, wr, '(x + 1/x)² = x² + 2 + 1/x²', f'{k}² − 2 = {ans}')
    if kind == 'cube':
        ans = k ** 3 - 3 * k
        wr = [(k ** 3, 'не враховано доданок 3(x + 1/x)'), (k ** 3 + 3 * k, 'знак змінено'), (k ** 3 - 3, 'не помножено 3 на (x + 1/x)'), (k * (k * k - 2), 'використано формулу для x² + 1/x² і помножено на k')]
        return T.add(lv, f'Відомо, що x + 1/x = {k}. Знайдіть x³ + 1/x³.', ans, wr, '(x + 1/x)³ = x³ + 3(x + 1/x) + 1/x³', f'{k}³ − 3·{k} = {ans}')
    d = rng.randint(1, 5)
    ans = d * d + 2
    wr = [(d * d, 'не додано 2'), (d * d - 2, 'знак подвоєного добутку змінено'), (2 * d, 'різницю подвоєно'), (d * d + 1, 'подвоєний добуток записано як 1')]
    return T.add(lv, f'Відомо, що x − 1/x = {d}. Знайдіть x² + 1/x².', ans, wr, '(x − 1/x)² = x² − 2 + 1/x²', f'{d}² + 2 = {ans}')

def f_sym3(T, rng, lv):
    kind = rng.choice(['ab_from_sq', 'cube', 'prod'])
    s = rng.randint(3, 9); q = rng.randint(5, 30)
    if kind == 'ab_from_sq':
        if (s * s - q) % 2 or 2 * q < s * s or s * s == q: return False
        ans = (s * s - q) // 2
        wr = [(s * s - q, 'не поділено на 2'), ((s * s + q) // 2 if (s*s+q)%2==0 else F(s*s+q,2), 'знак перед q змінено'), (q - s, 'суму й суму квадратів просто відняли'), ((q - s * s) // 2 if (q - s*s)%2==0 else F(q-s*s,2), 'порядок віднімання змінено')]
        return T.add(lv, f'Відомо, що a + b = {s} і a² + b² = {q}. Знайдіть ab.', ans, wr, '2ab = (a + b)² − (a² + b²)', f'({s}² − {q}) : 2 = {ans}')
    if kind == 'cube':
        ab = rng.randint(-5, 8)
        ans = s * (q * 0 + (s * s - 3 * ab))
        wr = [(s ** 3, 'не враховано доданок −3ab(a + b)'), (s ** 3 + 3 * ab * s, 'знак змінено'), (s * (s * s - ab), 'у формулі суми кубів не подвоєно/потроєно ab'), (s * s - 3 * ab, 'не помножено на (a + b)')]
        return T.add(lv, f'Відомо, що a + b = {s} і ab = {fmt(ab)}. Знайдіть a³ + b³.', ans, wr, 'a³ + b³ = (a + b)(a² − ab + b²) = (a + b)((a + b)² − 3ab)', f'{s}·({s}² − 3·({ab})) = {ans}')
    ab = rng.randint(2, 9)
    ans = ab * s
    wr = [(ab + s, 'суму й добуток додано'), (s * s, 'взято квадрат суми'), (ab * ab * s if False else ab * (s - 1), 'один із множників зменшено'), (ab * s * s, 'множник (a + b) піднесено до квадрата')]
    return T.add(lv, f'Відомо, що a + b = {s} і ab = {ab}. Знайдіть a²b + ab².', ans, wr, 'a²b + ab² = ab(a + b)', f'{ab} · {s} = {ans}')

def f_rem_system(T, rng, lv):
    a, b = rng.sample([1, 2, 3, -1, -2, 0], 2)
    A, B = rng.randint(-6, 8), rng.randint(-6, 8)
    if A == B: return False
    u = F(B - A, b - a); v = A - u * a
    def lt(u, v): return pt([u, v]) if True else ''
    ans = lt(u, v)
    wr = [(lt(-u, v), 'знак коефіцієнта при x змінено'), (lt(u, A + B - v if False else -v), 'знак вільного члена змінено'), (lt(v, u), 'коефіцієнти переставлено місцями'), (lt(F(A + B, 2), 0) if (A+B)%2==0 else lt(A + B, 0), 'невірно складено систему')]
    return T.add(lv, f'При діленні многочлена P(x) на (x {"−" if a>0 else "+"} {abs(a)}) остача дорівнює {fmt(A)}, а при діленні на (x {"−" if b>0 else "+"} {abs(b)}) остача дорівнює {fmt(B)}. Яка остача від ділення P(x) на добуток цих двочленів?'.replace('x + 0', 'x').replace('x − 0', 'x'), ans, wr,
                 'остача має вигляд ux + v; за теоремою Безу P(a) = ua + v, P(b) = ub + v', f'u·({rsgn(a)}) + v = {fmt(A)}, u·({rsgn(b)}) + v = {fmt(B)}; u = {fmt(u)}, v = {fmt(v)}')

def f_param_div(T, rng, lv):
    r = rng.choice([1, 2, 3, -1, -2]); a = rng.randint(-5, 5); b = rng.randint(-6, 6)
    c = -(r ** 3 + a * r * r + b * r)
    P = lambda aa: pev([1, aa, b, c], r)
    wr = []
    t = -((-r) ** 3 + b * (-r) + c)
    if (r * r) and t % (r * r) == 0: wr.append((t // (r * r), 'розв’язано умову для (x + r) замість (x − r)'))
    wr += [(-a, 'знак параметра змінено'), (a + r, 'арифметична похибка при підстановці'), (F(c + r ** 3 + b * r, r), 'не піднесено r до квадрата'), (a * r, 'параметр помножено на r')]
    return T.add(lv, f'При якому значенні a многочлен {pt([1, 0, b, c]).replace("x³", "x³" )} + a x² ділиться без остачі на (x {"−" if r > 0 else "+"} {abs(r)})?'.replace(' + a x²', f' + ax²') if False else
                 f'При якому значенні a многочлен x³ + ax²{sgn(b)}x{sgn(c)} ділиться без остачі на (x {"−" if r > 0 else "+"} {abs(r)})?'.replace('+ 1x', '+ x').replace('− 1x', '− x'), a, wr,
                 'P(x) ділиться на (x − r) тоді й лише тоді, коли P(r) = 0', f'P({rsgn(r)}) = {rsgn(r**3)} + a·{r*r} + ({rsgn(b)})·({rsgn(r)}) + ({rsgn(c)}) = 0, звідки a = {rsgn(a)}')

def f_log_conv(T, rng, lv):
    LI = [('log₃ 8', '3/a', [('3a', 'відношення логарифмів перевернуто'), ('a/3', 'відношення логарифмів перевернуто'), ('a + 3', 'логарифм частки замінено сумою'), ('8/a', '8 лишилось як число')], 'log₃ 8 = 3 · log₃ 2 = 3 / log₂ 3'),
          ('log₂ 12', 'a + 2', [('2a', 'добуток замінено на добуток логарифмів'), ('a + 3', 'невірно розкладено 12 на множники'), ('3a', '12 розглянуто як 3 · 4 без логарифма'), ('a − 2', 'знак перед 2 змінено')], 'log₂ 12 = log₂ 3 + log₂ 4 = a + 2'),
          ('log₂ 18', '2a + 1', [('a + 2', 'множники 2 і 9 переплутано'), ('3a', 'добуток замінено множенням логарифмів'), ('2a + 2', 'log₂ 2 прийнято за 2'), ('a² + 1', 'квадрат поставлено не туди')], 'log₂ 18 = log₂ 2 + 2 log₂ 3 = 1 + 2a'),
          ('log₄ 3', 'a/2', [('2a', 'основу 4 записано як 2 без урахування степеня'), ('a + 2', 'частку логарифмів замінено їх сумою'), ('1/(2a)', 'відношення логарифмів перевернуто'), ('a − 2', 'частку логарифмів замінено їх різницею')], 'log₄ 3 = log₂ 3 / log₂ 4 = a/2'),
          ('log₂ 0,75', 'a − 2', [('2 − a', 'знак результату змінено'), ('a + 2', 'ділення замінено множенням'), ('a/4', 'log₂ 3 поділено на 4 замість віднімання log₂ 4'), ('−a', 'не враховано log₂ 4')], 'log₂ 0,75 = log₂ 3 − log₂ 4 = a − 2'),
          ('log₃ 16', '4/a', [('4a', 'відношення логарифмів перевернуто'), ('a/4', 'відношення логарифмів перевернуто'), ('a + 4', 'логарифм степеня замінено сумою'), ('16/a', '16 лишилось як число')], 'log₃ 16 = 4 · log₃ 2 = 4/a'),
          ('log₂ 72', '2a + 3', [('3a + 2', 'множники 8 і 9 переплутано'), ('5a', 'добуток замінено множенням логарифмів'), ('a + 6', 'множник 9 розглянуто як 3 + 6'), ('2a + 4', 'log₂ 8 прийнято за 4')], 'log₂ 72 = log₂ 8 + log₂ 9 = 3 + 2a')]
    t, ans, w, sol = rng.choice(LI)
    return T.add(lv, f'Відомо, що log₂ 3 = a. Виразіть {t} через a.', ans, w, 'розкладайте аргумент на множники 2 і 3 та користуйтеся logₐ(xy) = logₐx + logₐy, logₐxᵏ = k logₐx і формулою переходу до іншої основи', sol)

def f_log_power(T, rng, lv):
    c = rng.choice([2, 3, 5]); m = rng.choice([2, 3]); x = rng.choice([2, 3, 4, 5, 7])
    kind = rng.choice(['power', 'shift'])
    if kind == 'power':
        base = c ** m; ans = x ** m
        sb = SUBL[c - 2]
        wr = [(x, 'вважали, що a^(logₐ x) = x для будь-якої основи, але основа тут c^m'), (x * m, 'показник m помножено на аргумент'), (x + m, 'показник m додано до аргументу'), (c * x, 'основу помножено на аргумент')]
        return T.add(lv, f'Обчисліть: {base}^(log{sb} {x}).', ans, wr, '(cᵐ)^(log_c x) = (c^(log_c x))ᵐ = xᵐ, бо c^(log_c x) = x', f'({c}{sup(m)})^(log{sb} {x}) = ({c}^(log{sb} {x})){sup(m)} = {x}{sup(m)} = {ans}')
    k = rng.randint(1, 3); ans = c ** k * x; sb = SUBL[c - 2]
    wr = [(c * k * x if False else k + x, 'показники й числа додано замість множення'), (c ** k + x, 'степінь додано до аргументу'), (c ** k * k * x if False else c * k * x, 'основу помножено на показник'), (x ** k * c, 'показник k поставлено біля аргументу')]
    return T.add(lv, f'Обчисліть: {c}^({k} + log{sb} {x}).', ans, wr, 'a^(m + n) = aᵐ · aⁿ та a^(logₐ x) = x', f'{c}{sup(k)} · {c}^(log{sb} {x}) = {c**k} · {x} = {ans}')

def f_log_chain(T, rng, lv):
    a = rng.choice([2, 3]); k = rng.randint(2, 4); chain = rng.sample([2, 3, 5, 7], 3)
    while a in chain: chain = rng.sample([2, 3, 5, 7], 3)
    b1, b2 = chain[0], chain[1]
    ans = k
    sb = lambda x: ''.join('₀₁₂₃₄₅₆₇₈₉'[int(d)] for d in str(x))
    expr = f'log{sb(a)} {b1} · log{sb(b1)} {b2} · log{sb(b2)} {a ** k}'
    wr = [(a ** k, 'знайдено число, а не показник степеня'), (k + 1, 'показник збільшено на 1'), (k * b1, 'показник помножено на основу проміжного логарифма'), (F(1, k), 'відношення логарифмів перевернуто')]
    return T.add(lv, f'Обчисліть: {expr}.', ans, wr, 'logₐb · log_b c = logₐc (ланцюжок логарифмів «скорочується»)', f'= log{sb(a)} {a**k} = {k}')

def f_telescope(T, rng, lv):
    mode = rng.choice(['step1', 'step2'])
    if mode == 'step1':
        n = rng.choice([4, 9, 16, 25, 36, 49, 64, 100]); r = int(math.isqrt(n))
        ans = r - 1
        wr = [(n - 1, 'під знаком кореня залишилось n замість √n'), (r, 'першу одиницю не віднято'), (r + 1, 'знак першого доданка змінено'), (F(r - 1, 2), 'поділено на 2 без підстав')]
        return T.add(lv, f'Обчисліть суму: 1/(√1 + √2) + 1/(√2 + √3) + … + 1/(√{n-1} + √{n}).', ans, wr, 'кожен доданок звільніть від ірраціональності: 1/(√(k+1) + √k) = √(k+1) − √k — сума «телескопічна»', f'сума = √{n} − √1 = {r} − 1 = {ans}')
    n = rng.choice([9, 25, 49, 81, 121]); r = int(math.isqrt(n)); ans = F(r - 1, 2)
    wr = [(r - 1, 'не враховано, що кожен доданок дорівнює (√(k+2) − √k)/2'), (F(r, 2), 'першу одиницю не віднято'), (F(n - 1, 2), 'під знаком кореня залишилось n'), (F(r + 1, 2), 'знак першого доданка змінено')]
    return T.add(lv, f'Обчисліть суму: 1/(1 + √3) + 1/(√3 + √5) + … + 1/(√{n-2} + √{n}).', ans, wr, '1/(√(k) + √(k+2)) = (√(k+2) − √k)/2 — доданки взаємно скорочуються', f'сума = (√{n} − 1)/2 = ({r} − 1)/2 = {fmt(ans)}')

def f_trig_sumcos(T, rng, lv):
    k = rng.choice([F(1, 2), F(7, 5), F(1, 3), F(3, 4), F(4, 3) if False else F(5, 4), F(6, 5), F(1, 5)])
    ans = (k * k - 1) / 2
    wr = [(k * k / 2, 'не віднято 1 перед діленням на 2'), (k * k - 1, 'не поділено на 2'), ((k - 1) / 2, 'суму не піднесено до квадрата'), ((k * k + 1) / 2, 'знак перед 1 змінено')]
    return T.add(lv, f'Відомо, що sin α + cos α = {fmt(k)}. Знайдіть sin α · cos α.', ans, wr, '(sin α + cos α)² = 1 + 2 sin α cos α', f'({fmt(k)})² = 1 + 2sinαcosα ⇒ sinαcosα = {fmt(ans)}')

def f_trig_tg(T, rng, lv):
    t = rng.choice([2, 3, 4, 5, -2, -3, F(1, 2), F(1, 3), 5]); kind = rng.choice(['ratio', 'prod', 'lin'])
    t = F(t)
    if kind == 'ratio':
        ans = (t + 1) / (t - 1)
        wr = [((t - 1) / (t + 1), 'чисельник і знаменник переставлено'), (t, 'значення tg α прийнято за відповідь'), ((t + 1) / (t + 1) if False else (t + 1) * (t - 1), 'ділення замінено множенням'), (-ans, 'знак результату змінено')]
        return T.add(lv, f'Відомо, що tg α = {fmt(t)}. Знайдіть (sin α + cos α) / (sin α − cos α).', ans, wr, 'поділіть чисельник і знаменник на cos α (cos α ≠ 0): sin α / cos α = tg α', f'({fmt(t)} + 1) / ({fmt(t)} − 1) = {fmt(ans)}')
    if kind == 'prod':
        ans = t / (1 + t * t)
        wr = [(t * t / (1 + t * t), 'знайдено sin²α'), (1 / (1 + t * t), 'знайдено cos²α'), (t / (1 - t * t) if t * t != 1 else t, 'у знаменнику взято 1 − tg²α замість 1 + tg²α'), (2 * t / (1 + t * t), 'знайдено sin 2α, а не sin α cos α')]
        return T.add(lv, f'Відомо, що tg α = {fmt(t)}. Знайдіть sin α · cos α.', ans, wr, 'sin α cos α = tg α / (1 + tg²α) (поділіть на sin²α + cos²α = 1)', f'{fmt(t)} / (1 + {fmt(t*t)}) = {fmt(ans)}')
    a, b, c, d = rng.choice([(2, -1, 1, 3), (3, 1, 1, -2), (1, 2, 2, 1), (4, -1, 1, 1), (2, 3, 1, -1)])
    den = c * t + d
    if den == 0: return False
    ans = (a * t + b) / den
    wr = [((a * t - b) / den, 'знак у чисельнику змінено'), ((a * t + b) / (c * t - d), 'знак у знаменнику змінено'), (den / (a * t + b) if a * t + b != 0 else 1, 'дріб перевернуто'), (F(a + b, c + d) if c + d else 1, 'замість tg α підставлено 1')]
    ex = lambda x, y, s: f'{cs(x, s)}{" + " if y > 0 else " − "}{abs(y)}'
    return T.add(lv, f'Відомо, що tg α = {fmt(t)}. Знайдіть ({a if a>1 else ""} sin α {"+" if b>0 else "−"} {abs(b) if abs(b)>1 else ""} cos α) / ({c if c>1 else ""} sin α {"+" if d>0 else "−"} {abs(d) if abs(d)>1 else ""} cos α).'.replace('( sin', '(sin').replace('  ', ' '), ans, wr,
                 'поділіть чисельник і знаменник на cos α, щоб отримати вираз із tg α', f'({a}·{fmt(t)} {"+" if b>0 else "−"} {abs(b)}) / ({c}·{fmt(t)} {"+" if d>0 else "−"} {abs(d)}) = {fmt(ans)}')

def f_trig_double(T, rng, lv):
    a, b, c = rng.choice(TRIPLES); quad = rng.choice([1, 2])
    sv = F(a, c); cv = F(b, c) * (1 if quad == 1 else -1)
    kind = rng.choice(['cos2', 'sin2'])
    qn = 'першої' if quad == 1 else 'другої'
    if kind == 'cos2':
        ans = 1 - 2 * sv * sv
        wr = [(2 * sv * sv - 1, 'знак формули cos 2α змінено'), (1 - sv * sv, 'не подвоєно sin²α'), (2 * sv * cv, 'знайдено sin 2α, а не cos 2α'), (-ans if ans != 0 else 1, 'знак результату змінено')]
        return T.add(lv, f'Відомо, що sin α = {fmt(sv)} і α — кут {qn} чверті. Знайдіть cos 2α.', ans, wr, 'cos 2α = 1 − 2 sin²α (знак чверті тут не впливає)', f'1 − 2·({fmt(sv)})² = {fmt(ans)}')
    ans = 2 * sv * cv
    wr = [(-ans, 'знак cos α не відповідає чверті'), (2 * sv, 'cos α не враховано'), (sv * cv, 'не подвоєно добуток'), (1 - 2 * sv * sv, 'знайдено cos 2α, а не sin 2α')]
    return T.add(lv, f'Відомо, що sin α = {fmt(sv)} і α — кут {qn} чверті. Знайдіть sin 2α.', ans, wr, 'sin 2α = 2 sin α cos α; знак cos α залежить від чверті', f'cos α = {fmt(cv)}; sin 2α = 2·{fmt(sv)}·({fmt(cv)}) = {fmt(ans)}')

def f_abs_interval(T, rng, lv):
    a = rng.randint(-5, 2); b = a + rng.randint(3, 8); kind = rng.choice(['sum', 'diff'])
    if kind == 'sum':
        ans = str(b - a)
        wr = [(f'2x − {b + a}'.replace('− -', '+ '), 'розкрито модулі так, ніби x поза проміжком'), (str(b + a if b + a > 0 else a - b), 'числа a і b додано'), (f'{b - a} − 2x'.replace('− -', '+ '), 'знак модуля розкрито неправильно'), (f'x', 'змінні не скорочено')]
        wr = [(w, r) for w, r in wr]
        return T.add(lv, f'Спростіть вираз |x {"−" if a>0 else "+"} {abs(a)}| + |x − {b}|, якщо {fmt(a)} < x < {b}.'.replace('x + 0', 'x').replace('x − 0', 'x'), ans, wr, 'визначте знак кожного виразу під модулем на заданому проміжку', f'x − {a} > 0 і x − {b} < 0 ⇒ (x − {a}) + ({b} − x) = {b - a}'.replace('− -', '+ '))
    s = -(a + b)
    ans = f'2x {"−" if a + b > 0 else "+"} {abs(a + b)}' if a + b != 0 else '2x'
    wr = [(str(b - a), 'модулі підібрано так, ніби змінна скоротилась'), (f'{b - a} − 2x'.replace('− -', '+ '), 'знак при x змінено'), (f'2x {"+" if a + b > 0 else "−"} {abs(a + b)}' if a + b != 0 else '−2x', 'знак вільного члена змінено'), (f'{a + b} − 2x'.replace('− -', '+ '), 'модулі розкрито у протилежний бік')]
    return T.add(lv, f'Спростіть вираз |x {"−" if a>0 else "+"} {abs(a)}| − |x − {b}|, якщо {fmt(a)} < x < {b}.'.replace('x + 0', 'x').replace('x − 0', 'x'), ans, wr, 'на проміжку (a; b): |x − a| = x − a, |x − b| = b − x', f'(x − {a}) − ({b} − x) = {ans}'.replace('− -', '+ '))

def f_domain_count(T, rng, lv):
    a = rng.randint(2, 7); b = rng.randint(2, 8)
    ex = rng.sample(range(-a + 1, b), rng.choice([1, 2]))
    exs = sorted(ex)
    cnt = sum(1 for x in range(-a, b + 1) if x not in exs)
    den = ' · '.join(f'(x {"−" if e > 0 else "+"} {abs(e)})' for e in exs if e != 0) if all(e != 0 for e in exs) else None
    den_parts = []
    for e in exs:
        den_parts.append('x' if e == 0 else f'(x {"−" if e > 0 else "+"} {abs(e)})')
    den = ''.join(den_parts) if len(den_parts) == 1 else ' · '.join(den_parts)
    expr = f'√(x + {a}) · √({b} − x) / ({den})'
    wr = [(cnt + len(exs), 'не виключено цілі точки, де знаменник дорівнює нулю'), (cnt + 1 if False else b + a - 1 - len(exs), 'крайні цілі точки відрізка не враховано'), (b + a + 1, 'вказано кількість цілих точок відрізка без виключення'), (cnt - 1, 'виключено зайву точку')]
    return T.add(lv, f'Скільки цілих значень x належить області допустимих значень виразу {expr}?', cnt, wr, 'корені — нестрогі нерівності (відрізок), знаменник ≠ 0 — виколюємо точки', f'відрізок [{-a}; {b}] містить {a + b + 1} цілих чисел; виколюємо {len(exs)}: {cnt}')

def f_exp_sym(T, rng, lv):
    k = rng.randint(3, 8); kind = rng.choice(['4x', '8x'])
    if kind == '4x':
        ans = k * k - 2
        wr = [(k * k, 'не віднято подвоєний добуток 2'), (k * k + 2, 'знак подвоєного добутку змінено'), (2 * k, 'суму подвоєно'), (k * k - 1, 'подвоєний добуток записано як 1')]
        return T.add(lv, f'Відомо, що 2ˣ + 2⁻ˣ = {k}. Знайдіть 4ˣ + 4⁻ˣ.', ans, wr, '(2ˣ + 2⁻ˣ)² = 4ˣ + 2 + 4⁻ˣ, бо 2ˣ · 2⁻ˣ = 1', f'{k}² − 2 = {ans}')
    ans = k ** 3 - 3 * k
    wr = [(k ** 3, 'не враховано доданок 3(a + 1/a)'), (k ** 3 + 3 * k, 'знак змінено'), (k * k * k - 3, 'не помножено на k'), (k * (k * k - 2), 'використано формулу для квадрата й помножено на k')]
    return T.add(lv, f'Відомо, що 2ˣ + 2⁻ˣ = {k}. Знайдіть 8ˣ + 8⁻ˣ.', ans, wr, '(a + 1/a)³ = a³ + 3(a + 1/a) + 1/a³ при a = 2ˣ', f'{k}³ − 3·{k} = {ans}')

def f_pow_expr(T, rng, lv):
    a = rng.choice([2, 3, 5]); p, q, r = rng.randint(2, 4), rng.randint(0, 1), rng.randint(0, 1)
    if q == r: return False
    sg = rng.choice([1, -1])
    num = F(a) ** p + sg * F(a) ** q
    ans = F(a) ** (p - r) + sg * F(a) ** (q - r)
    wr = [(F(a) ** (p - r) + sg * F(a) ** (q - r) * 2, 'другий доданок враховано двічі'), (F(a) ** (p - r) - sg * F(a) ** (q - r), 'знак між доданками змінено'), (F(a) ** (p + q - r), 'доданки об’єднано як множники'), (F(a) ** (p - r), 'другий доданок втрачено')]
    n_ = 'n'
    t = f'(2^(n + {p})'.replace('2', str(a)) if False else None
    sa = str(a)
    sh = lambda s_: ('n' + (f' + {s_}' if s_ > 0 else '')) if s_ else 'n'
    txt = f'({sa}^({sh(p)}) {"+" if sg > 0 else "−"} {sa}^({sh(q)})) / {sa}^({sh(r)})' if True else ''
    return T.add(lv, f'Обчисліть значення виразу {txt}.', ans, wr, 'виносьте найменший степінь за дужки або діліть кожен доданок: aᵐ⁺ⁿ / aⁿ = aᵐ', f'{sa}^{p - r} {"+" if sg > 0 else "−"} {sa}^{q - r} = {fmt(ans)}')

def f_big(T, rng, lv):
    N = rng.choice([1001, 2023, 5003, 10001, 3001, 4007, 999]); d = rng.randint(2, 4)
    kind = rng.choice(['sq', 'sq2'])
    if kind == 'sq':
        ans = d * d
        wr = [(0, 'вважали, що різниця дорівнює нулю'), (d, 'число d не піднесено до квадрата'), (2 * d * d, 'квадрат подвоєно'), (d * d + 1, 'до результату додано 1')]
        return T.add(lv, f'Обчисліть, не користуючись калькулятором: {N}² − {N - d} · {N + d}.', ans, wr, '(a − d)(a + d) = a² − d², тому різниця дорівнює d²', f'{N}² − ({N}² − {d}²) = {d}² = {ans}')
    ans = 4 * N * d
    wr = [(2 * N * d, 'не помножено на 4'), (N * d, 'використано лише добуток'), (4 * d * d, 'знайдено добуток замість різниці'), (4 * N * d + 4 * d * d, 'додано квадрати')]
    return T.add(lv, f'Обчисліть: ({N + d})² − ({N - d})².', ans, wr, 'a² − b² = (a − b)(a + b)', f'({N}+{d} − {N}+{d})({N}+{d}+{N}−{d}) = {2*d}·{2*N} = {ans}')

def f_log_eq_val(T, rng, lv):
    b = rng.choice([2, 3, 5]); m = rng.randint(2, 4); n_ = rng.randint(1, 3)
    # log_b(x)=m, log_b(y)=n -> log_b(x^2/y)  = 2m-n
    ans = 2 * m - n_
    sb = SUBL[b - 2]
    wr = [(2 * m + n_, 'логарифм частки замінено сумою'), (m * 2 - n_ * 2, 'показник застосовано до обох змінних'), (m - n_, 'не враховано квадрат x'), (2 * m * n_ if False else m * n_, 'логарифми перемножено')]
    return T.add(lv, f'Відомо, що log{sb} x = {m} і log{sb} y = {n_}. Знайдіть log{sb} (x² / y).', ans, wr, 'logₐ(x²/y) = 2 logₐ x − logₐ y', f'2·{m} − {n_} = {ans}')

FAMS = [(f_square, [1]), (f_diffsq, [1]), (f_value, [1]), (f_like, [1]), (f_degree, [1]), (f_common, [1]), (f_powers, [1]), (f_log_basic, [1, 2]), (f_trig_table, [1, 2]), (f_deg_rad, [1]), (f_domain, [1, 2]), (f_cancel_num, [1]), (f_brackets, [1]),
        (f_factor_trinomial, [2]), (f_factor_lead, [2]), (f_simplify_rat, [2]), (f_add_frac, [2]), (f_sym_value, [2]), (f_remainder, [2]), (f_cubes, [2]), (f_logs, [2]), (f_radicals, [2]), (f_trig_ident, [2, 3]), (f_reduction, [2]),
        (f_rat_exp, [2]), (f_coef_sum, [2]), (f_poly_deg, [2]),
        (f_x_inv, [3]), (f_sym3, [3]), (f_rem_system, [3]), (f_param_div, [3]), (f_log_conv, [3]), (f_log_power, [3]), (f_log_chain, [3]), (f_telescope, [3]), (f_trig_sumcos, [3]), (f_trig_tg, [3]), (f_trig_double, [3]),
        (f_abs_interval, [3]), (f_domain_count, [3]), (f_exp_sym, [3]), (f_pow_expr, [3]), (f_big, [3]), (f_log_eq_val, [3])]
