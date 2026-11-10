import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgen import *
import msvg as S
from msvg import C, INK, GRAY, BLUE, RED, ORANGE, GREEN, PURPLE

T = Topic(8, 'stereometriya')
SEC = '#fde68a'; SECS = '#b45309'; LB = '#dbeafe'

# ---------- числа ----------
def rad(a, N, d=1):
    """a·√N / d у спрощеному вигляді (рядок)"""
    k = 1; m = N; f = 2
    while f * f <= m:
        while m % (f * f) == 0: m //= f * f; k *= f
        f += 1
    a *= k
    if m == 1: return fmt(F(a, d))
    g = math.gcd(a, d); a //= g; d //= g
    s = ('' if a == 1 else str(a)) + '√' + str(m)
    return s if d == 1 else f'{s}/{d}'

def pis(c):
    c = F(c)
    if c.denominator == 1: return ('' if c == 1 else str(c.numerator)) + 'π'
    return ('' if c.numerator == 1 else str(c.numerator)) + 'π/' + str(c.denominator)

def raz(n): return f'{n} ' + ('рази' if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else 'разів')
def deg(x):
    r = round(x)
    return f'{r}°' if abs(x - r) < 1e-6 else '≈' + dec_(x) + '°'
def dec_(x): return ('%.1f' % x).replace('.', ',')

TRI = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15), (12, 16, 20), (20, 21, 29), (9, 40, 41)]
QUAD = [(1, 2, 2, 3), (2, 3, 6, 7), (2, 4, 4, 6), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (4, 8, 8, 12), (6, 6, 17, 19)]

# ---------- малювання ----------
def P(x, y, z, o, k, ax=0.5, ay=0.32): return (o[0] + k * (x + ax * y), o[1] - k * (z + ay * y))
EDGES = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A1', 'B1'), ('B1', 'C1'), ('C1', 'D1'), ('D1', 'A1'), ('A', 'A1'), ('B', 'B1'), ('C', 'C1'), ('D', 'D1')]
HID = {('D', 'A'), ('C', 'D'), ('D', 'D1')}
SUB = {'A1': 'A₁', 'B1': 'B₁', 'C1': 'C₁', 'D1': 'D₁'}

def vlab(c, V, names, centre, off=14, size=15, col=INK):
    for nme in names:
        x, y = V[nme]; dx, dy = x - centre[0], y - centre[1]; d = math.hypot(dx, dy) or 1
        c.text(x + dx / d * off, y + dy / d * off + 5, SUB.get(nme, nme), size=size, col=col, anchor='middle', bold=True)

def dimtxt(c, p, q, s, off=(0, 0), col=BLUE, size=14):
    c.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1] + 4, s, size=size, col=col, anchor='middle', bold=True)

def box(c, a, b, h, o, k, hl=None, names=True, extra=True):
    nm = {'A': (0, 0, 0), 'B': (a, 0, 0), 'C': (a, b, 0), 'D': (0, b, 0), 'A1': (0, 0, h), 'B1': (a, 0, h), 'C1': (a, b, h), 'D1': (0, b, h)}
    V = {n_: P(*p, o, k) for n_, p in nm.items()}
    if hl: c.poly([V[x] for x in hl], fill=SEC, stroke=SECS, w=2)
    for p, q in EDGES: c.line(*V[p], *V[q], col=INK, w=2, dash='5,4' if (p, q) in HID else None)
    if names:
        LOFF = {'A': (-14, 17), 'B': (13, 18), 'C': (16, 6), 'D': (-16, -7), 'A1': (-16, -6), 'B1': (-15, -13), 'C1': (15, -6), 'D1': (-6, -13)}
        for nme, (dx, dy) in LOFF.items(): c.text(V[nme][0] + dx, V[nme][1] + dy, SUB.get(nme, nme), size=15, col=INK, anchor='middle', bold=True)
    return V

def pyr(c, a, b, H, o, k, names=True, hy=True, apo=False):
    nm = {'A': (0, 0, 0), 'B': (a, 0, 0), 'C': (a, b, 0), 'D': (0, b, 0), 'S': (a / 2, b / 2, H), 'O': (a / 2, b / 2, 0), 'M': (a / 2, 0, 0)}
    V = {n_: P(*p, o, k) for n_, p in nm.items()}
    for p, q in [('A', 'B'), ('B', 'C'), ('S', 'A'), ('S', 'B'), ('S', 'C')]: c.line(*V[p], *V[q], col=INK, w=2)
    for p, q in [('D', 'A'), ('C', 'D'), ('S', 'D')]: c.line(*V[p], *V[q], col=INK, w=2, dash='5,4')
    if hy: c.line(*V['S'], *V['O'], col=RED, w=1.8, dash='4,3')
    if apo:
        c.line(*V['S'], *V['M'], col=GREEN, w=2); c.line(*V['O'], *V['M'], col=GREEN, w=1.8, dash='4,3')
    if names:
        cen = ((V['A'][0] + V['C'][0]) / 2, (V['A'][1] + V['C'][1]) / 2 - 20)
        vlab(c, V, ['A', 'B', 'C', 'D', 'S'], cen)
        c.dot(*V['O'], 3, RED); c.text(V['O'][0] + 10, V['O'][1] - 4, 'O', size=13, col=RED, bold=True)
        if apo: c.dot(*V['M'], 3, GREEN); c.text(V['M'][0] - 4, V['M'][1] + 16, 'M', size=13, col=GREEN, bold=True)
    return V

def cyl(c, cx, yb, R, h, rcol=BLUE, labR='R', labh='h', fillc='#eff6ff', axis=True):
    ry = R * 0.3; yt = yb - h
    c.path(f'M{cx-R},{yt} L{cx-R},{yb} A{R},{ry} 0 0 0 {cx+R},{yb} L{cx+R},{yt} Z', fill=fillc, stroke=INK, w=2)
    c.path(f'M{cx-R},{yb} A{R},{ry} 0 0 1 {cx+R},{yb}', stroke=INK, w=1.6, dash='5,4')
    c.ellipse(cx, yt, R, ry, fill='#dbeafe', stroke=INK, sw=2)
    if axis: c.line(cx, yt, cx, yb, col=RED, w=1.6, dash='4,3')
    if labR: c.line(cx, yb, cx + R, yb, col=rcol, w=2); c.text(cx + R / 2, yb + 15, labR, size=14, col=rcol, anchor='middle', bold=True)
    if labh: c.text(cx + R + 12, (yt + yb) / 2 + 5, labh, size=14, col=rcol, bold=True)
    return yt

def cone(c, cx, yb, R, h, labR='R', labh='h', labl='l', col=BLUE):
    ry = R * 0.3; ya = yb - h
    c.path(f'M{cx-R},{yb} L{cx},{ya} L{cx+R},{yb} A{R},{ry} 0 0 1 {cx-R},{yb} Z', fill='#eff6ff', stroke=INK, w=2)
    c.path(f'M{cx-R},{yb} A{R},{ry} 0 0 1 {cx+R},{yb}', stroke=INK, w=1.6, dash='5,4')
    c.line(cx, ya, cx, yb, col=RED, w=1.6, dash='4,3'); c.dot(cx, ya, 3, INK)
    if labR: c.line(cx, yb, cx + R, yb, col=col, w=2); c.text(cx + R / 2, yb + 16, labR, size=14, col=col, anchor='middle', bold=True)
    if labh: c.text(cx - 8, (ya + yb) / 2 + 5, labh, size=14, col=RED, anchor='end', bold=True)
    if labl: c.text(cx + R / 2 + 12, (ya + yb) / 2 - 2, labl, size=14, col=col, bold=True)

def sidel(c, V, txt, col=BLUE):
    c.text(V['A'][0] + 0.2 * (V['B'][0] - V['A'][0]), V['A'][1] + 26, txt, size=14, col=col, anchor='middle', bold=True)

def savec(c, *parts): return c.save('s8_' + S.tag(*parts))

# =====================================================================
# 1. прямокутний паралелепіпед
def f_box(T, rng, lv):
    kind = rng.choice(['V', 'S'] if lv == 1 else (['diag', 'S', 'V3', 'dsec'] if lv == 2 else ['diag3', 'c_from_d', 'ratio', 'dsec']))
    if kind in ('V', 'S', 'V3', 'dsec'):
        a, b, h = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
    else:
        q = list(rng.choice(QUAD)); dd_ = q[3]; q = q[:3]; rng.shuffle(q); a, b, h, d = q[0], q[1], q[2], dd_
        s = rng.choice([1, 2]) if lv == 3 else 1; a, b, h, d = a * s, b * s, h * s, d * s
    c = C(340, 250); V = box(c, 1.7, 1.0, 1.2, (60, 205), 100)
    dimtxt(c, V['A'], V['B'], str(a), (0, 24)); dimtxt(c, V['B'], V['C'], str(b), (22, 12)); dimtxt(c, V['A'], V['A1'], str(h), (-16, 0))
    if kind in ('V', 'S', 'V3'):
        img = savec(c, 'box', kind, a, b, h)
        if kind == 'V':
            return T.add(lv, f'На рисунку зображено прямокутний паралелепіпед ABCDA₁B₁C₁D₁ з вимірами {a}, {b} і {h}. Знайдіть його об’єм.', a * b * h,
                [(a + b + h, 'виміри додано замість множення'), (2 * (a * b + b * h + a * h), 'знайдено площу поверхні замість об’єму'), (F(a * b * h, 3), 'об’єм поділено на 3 (формула піраміди)')],
                'об’єм прямокутного паралелепіпеда — добуток трьох вимірів', f'V = {a}·{b}·{h}', img)
        if kind == 'dsec':
            c.line(*V['A'], *V['C'], col=RED, w=2); c.line(*V['A1'], *V['C1'], col=RED, w=1.6)
            img = savec(c, 'boxs', a, b, h); dg = rad(1, a * a + b * b)
            return T.add(lv, f'Основа прямокутного паралелепіпеда — прямокутник {a} × {b}, бічне ребро дорівнює {h}. Знайдіть площу діагонального перерізу AA₁C₁C (рисунок).', rad(h, a * a + b * b),
                [(a * b, 'взято площу основи'), (h * (a + b), 'діагональ основи замінено сумою сторін'), (rad(a, a * a + b * b), 'замість висоти AA₁ взято сторону AB')],
                'діагональний переріз — прямокутник: діагональ основи × висота', f'AC = {dg}, S = {dg}·{h}', img)
        if kind == 'V3':
            return T.add(lv, f'Виміри прямокутного паралелепіпеда (рисунок) дорівнюють {a}, {b} і {h}. Знайдіть суму довжин усіх його ребер.', 4 * (a + b + h),
                [(a + b + h, 'враховано лише по одному ребру кожного напрямку'), (2 * (a + b + h), 'враховано лише половину ребер'), (a * b * h, 'знайдено об’єм замість суми довжин ребер')],
                'у паралелепіпеда по 4 ребра кожного з трьох напрямків', f'4·({a} + {b} + {h})', img)
        return T.add(lv, f'Виміри прямокутного паралелепіпеда (рисунок): {a}, {b} і {h}. Знайдіть площу його повної поверхні.', 2 * (a * b + b * h + a * h),
            [(a * b * h, 'знайдено об’єм замість площі поверхні'), (a * b + b * h + a * h, 'не враховано, що кожна грань трапляється двічі'), (2 * (a + b + h), 'грані замінено сумою ребер')],
            'поверхня складається з трьох пар рівних граней', f'2·({a}·{b} + {b}·{h} + {a}·{h})', img)
    if kind == 'diag':
        c.line(*V['A'], *V['C1'], col=RED, w=2); dimtxt(c, V['A'], V['C1'], 'd?', (-14, -8), RED)
        img = savec(c, 'boxd', a, b, h)
        return T.add(lv, f'Виміри прямокутного паралелепіпеда ABCDA₁B₁C₁D₁ (рисунок): AB = {a}, BC = {b}, AA₁ = {h}. Знайдіть діагональ AC₁.', d,
            [(a + b + h, 'діагональ замінено сумою вимірів'), (rad(1, a * a + b * b), 'знайдено діагональ основи, а не просторову діагональ'),
             (rad(1, a * a + b * b + h), 'висоту не піднесено до квадрата'), (d * d, 'діагональ знайдено без добування кореня')],
            'квадрат діагоналі дорівнює сумі квадратів трьох вимірів', f'AC₁ = √({a}² + {b}² + {h}²) = √{d*d}', img)
    if kind == 'diag3':
        c.line(*V['A'], *V['C1'], col=RED, w=2)
        img = savec(c, 'boxdd', a, b, h)
        return T.add(lv, f'У прямокутному паралелепіпеді ABCDA₁B₁C₁D₁: AB = {a}, BC = {b}, AA₁ = {h}. Знайдіть синус кута між діагоналлю AC₁ та площиною основи.', ffmt(F(h, d)),
            [(ffmt(F(a, d)), 'узято ребро AB замість висоти AA₁'), (ffmt(F(d, h)), 'відношення перевернуто'), (ffmt(F(a + b, d)), 'у чисельнику сума сторін основи')],
            'у трикутнику ACC₁ катет CC₁ = AA₁ протилежний шуканому куту', f'sin∠C₁AC = CC₁ / AC₁ = {h}/{d}', img)
    if kind == 'c_from_d':
        c.line(*V['A'], *V['C1'], col=RED, w=2); dimtxt(c, V['A'], V['C1'], str(d), (-12, -10), RED)
        c.text(V['A1'][0] - 16, V['A1'][1] - 22, '', size=10)
        img = savec(c, 'boxc', a, b, h, d)
        return T.add(lv, f'Діагональ AC₁ прямокутного паралелепіпеда дорівнює {d}, AB = {a}, BC = {b}. Знайдіть бічне ребро AA₁.', h,
            [(d - a - b, 'діагональ вважали сумою трьох вимірів'), (rad(1, d * d - a * a), 'не враховано другий вимір основи BC'),
             (d * d - a * a - b * b, 'не добуто квадратний корінь'), (a + b, 'бічне ребро прирівняно до суми сторін основи')],
            'd² = a² + b² + c², звідси c² = d² − a² − b²', f'AA₁ = √({d}² − {a}² − {b}²) = √{h*h}', img)
    # ratio: відношення
    c.line(*V['A'], *V['C1'], col=RED, w=2)
    img = savec(c, 'boxr', a, b, h)
    k = rng.choice([2, 3])
    return T.add(lv, f'Виміри прямокутного паралелепіпеда (рисунок) — {a}, {b}, {h}. Кожен вимір збільшили у {raz(k)}. У скільки разів збільшилась площа його повної поверхні?', k * k,
        [(k, 'площа залежить лише від одного виміру'), (k ** 3, 'знайдено збільшення об’єму'), (3 * k, 'враховано три виміри додаванням')],
        'площа поверхні зростає у k² разів, а об’єм — у k³', f'площі пропорційні квадрату коефіцієнта подібності: {k}² = {k*k}', img)

# 2. куб
def f_cube(T, rng, lv):
    c = C(300, 240); V = box(c, 1.3, 1.3, 1.3, (60, 195), 100)
    kind = rng.choice(['diag', 'fd'] if lv == 1 else (['diag_v', 'V_from_S'] if lv == 2 else ['d_to_V', 'fd_to_S', 'AC1_len']))
    if kind == 'diag':
        a = rng.randint(2, 12); c.line(*V['A'], *V['C1'], col=RED, w=2); dimtxt(c, V['A'], V['B'], str(a), (0, 24))
        return T.add(lv, f'Ребро куба ABCDA₁B₁C₁D₁ дорівнює {a} (рисунок). Знайдіть діагональ куба AC₁.', rad(a, 3),
            [(rad(a, 2), 'знайдено діагональ грані'), (3 * a, 'діагональ замінено сумою трьох ребер'), (str(a * a) + '√3', 'ребро піднесено до квадрата')],
            'діагональ куба d = a√3', f'AC₁ = {a}·√3', savec(c, 'cd', a))
    if kind == 'fd':
        a = rng.randint(2, 12); c.line(*V['A'], *V['C'], col=RED, w=2); dimtxt(c, V['A'], V['B'], str(a), (0, 24))
        return T.add(lv, f'Ребро куба дорівнює {a} (рисунок). Знайдіть діагональ його грані AC.', rad(a, 2),
            [(rad(a, 3), 'взято просторову діагональ'), (2 * a, 'діагональ вважали сумою двох сторін'), (a, 'діагональ грані прирівняно до ребра')],
            'діагональ квадрата зі стороною a дорівнює a√2', f'AC = {a}√2', savec(c, 'cf', a))
    if kind == 'diag_v':
        m = rng.randint(2, 9)
        c.line(*V['A'], *V['C1'], col=RED, w=2); dimtxt(c, V['A'], V['C1'], rad(m, 3), (-18, -8), RED)
        return T.add(lv, f'Діагональ куба дорівнює {rad(m,3)} (рисунок). Знайдіть об’єм куба.', m ** 3,
            [(3 * m ** 3, 'діагональ вважали ребром'), (m * m, 'піднесено до квадрата замість куба'), (6 * m * m, 'знайдено площу поверхні')],
            'діагональ куба — a√3, тому a = d/√3', f'a = {rad(m,3)}/√3 = {m}, V = {m}³', savec(c, 'cdv', m))
    if kind == 'V_from_S':
        m = rng.randint(2, 9)
        return T.add(lv, f'Площа повної поверхні куба (рисунок) дорівнює {6*m*m}. Знайдіть його об’єм.', m ** 3,
            [(m * m, 'знайдено площу однієї грані'), (6 * m ** 3, 'об’єм помножено на кількість граней'), (m ** 3 * 3, 'взято діагональ куба як ребро')],
            'S = 6a², звідси a = √(S/6)', f'a² = {m*m}, a = {m}, V = {m}³', savec(c, 'cvs', m))
    if kind == 'd_to_V':
        m = rng.randint(2, 6)
        c.line(*V['A'], *V['C1'], col=RED, w=2)
        return T.add(lv, f'Діагональ куба дорівнює {rad(m,3)}. Знайдіть площу повної поверхні куба.', 6 * m * m,
            [(m ** 3, 'знайдено об’єм'), (6 * 3 * m * m, 'діагональ вважали ребром'), (6 * m, 'ребро помножено на 6 замість квадрата')],
            'з d = a√3 знаходимо ребро, потім S = 6a²', f'a = {m}, S = 6·{m}² = {6*m*m}', savec(c, 'dS', m))
    if kind == 'fd_to_S':
        m = rng.randint(2, 9)
        c.line(*V['A'], *V['C'], col=RED, w=2); dimtxt(c, V['A'], V['C'], rad(m, 2), (-18, -2), RED)
        return T.add(lv, f'Діагональ грані куба дорівнює {rad(m,2)} (рисунок). Знайдіть площу повної поверхні куба.', 6 * m * m,
            [(m ** 3, 'знайдено об’єм замість площі'), (12 * m * m, 'діагональ грані вважали ребром'), (3 * m * m, 'враховано три грані')],
            'діагональ грані d = a√2', f'a = {m}, S = 6a² = {6*m*m}', savec(c, 'fS', m))
    # довжина діагоналі, якщо відомий об'єм
    m = rng.randint(2, 7)
    c.line(*V['A'], *V['C1'], col=RED, w=2)
    return T.add(lv, f'Об’єм куба дорівнює {m**3}. Знайдіть діагональ куба.', rad(m, 3),
        [(rad(m, 2), 'знайдено діагональ грані'), (m ** 3 * 1, 'діагональ вважали рівною об’єму'), (3 * m, 'діагональ замінено сумою трьох ребер')],
        'спочатку ребро a = ∛V, потім d = a√3', f'a = {m}, d = {m}√3', savec(c, 'dV', m))

# 3. пряма трикутна призма
def prism_tri(c, p, q, h, o, k):
    nm = {'A': (0, 0, 0), 'B': (p, 0, 0), 'C': (0, q, 0), 'A1': (0, 0, h), 'B1': (p, 0, h), 'C1': (0, q, h)}
    V = {n_: P(*pt, o, k) for n_, pt in nm.items()}
    for a_, b_ in [('A', 'B'), ('A', 'A1'), ('B', 'B1'), ('A1', 'B1'), ('B1', 'C1'), ('A1', 'C1')]: c.line(*V[a_], *V[b_], col=INK, w=2)
    for a_, b_ in [('A', 'C'), ('B', 'C'), ('C', 'C1')]: c.line(*V[a_], *V[b_], col=INK, w=2, dash='5,4')
    return V
def f_prism(T, rng, lv):
    p, q, hy = rng.choice(TRI);
    if rng.random() < 0.5: p, q = q, p
    h = rng.randint(3, 10) if lv == 1 else rng.randint(5, 15)
    c = C(330, 240); V = prism_tri(c, 1.6, 1.2, 1.3, (60, 205), 100)
    S.right_angle(c, V['A'], V['B'], V['C'], 12); S.right_angle(c, V['A1'], V['B1'], V['C1'], 12)
    vlab(c, V, list(V), ((V['A'][0] + V['C1'][0]) / 2, (V['A'][1] + V['C1'][1]) / 2))
    dimtxt(c, V['A'], V['B'], str(p), (0, 24)); dimtxt(c, V['A'], V['C'], str(q), (-17, -10)); dimtxt(c, V['B'], V['B1'], str(h), (14, 0))
    kind = rng.choice(['V', 'S_b'] if lv == 1 else (['S_b', 'S_full', 'V_h'] if lv == 2 else ['S_full', 'V_h', 'h_from_S']))
    base = F(p * q, 2)
    if kind == 'V':
        return T.add(lv, f'Основа прямої призми — прямокутний трикутник із катетами {p} і {q} (рисунок), висота призми {h}. Знайдіть об’єм призми.', base * h,
            [(p * q * h, 'не враховано множник ½ у площі трикутника'), (base * h / 3, 'об’єм поділено на 3 (формула піраміди)'), ((p + q) * h, 'площу основи замінено сумою катетів')],
            'V = S основи · h', f'S основи = ½·{p}·{q} = {fmt(base)}, V = {fmt(base)}·{h}', savec(c, 'pV', p, q, h))
    if kind == 'S_b':
        return T.add(lv, f'Основа прямої призми — прямокутний трикутник із катетами {p} і {q} (рисунок), висота {h}. Знайдіть площу бічної поверхні.', (p + q + hy) * h,
            [((p + q) * h, 'не враховано бічну грань на гіпотенузі'), (base * h, 'знайдено об’єм'), ((p + q + hy) * h * 2, 'площу бічної поверхні подвоєно')],
            'S бічна = Pоснови · h; гіпотенуза з теореми Піфагора', f'гіпотенуза {hy}; S = ({p} + {q} + {hy})·{h}', savec(c, 'pSb', p, q, h))
    if kind == 'S_full':
        return T.add(lv, f'Основа прямої призми — прямокутний трикутник із катетами {p} і {q} (рисунок), висота {h}. Знайдіть площу повної поверхні.', (p + q + hy) * h + p * q,
            [((p + q + hy) * h + base, 'додано площу лише однієї основи'), ((p + q + hy) * h, 'не додано площі основ'), ((p + q) * h + p * q, 'не враховано грань на гіпотенузі')],
            'S повна = S бічна + 2·S основи', f'S = {(p+q+hy)*h} + 2·{fmt(base)}', savec(c, 'pSf', p, q, h))
    if kind == 'V_h':
        V_ = base * h
        return T.add(lv, f'Основа прямої призми — прямокутний трикутник із катетами {p} і {q}. Об’єм призми дорівнює {fmt(V_)}. Знайдіть висоту призми.', h,
            [(F(V_, p * q), 'не враховано, що площа основи — половина добутку катетів'), (V_ - base, 'площу основи відняли від об’єму'), (F(V_ * 3, base), 'застосовано формулу піраміди')],
            'h = V / S основи', f'h = {fmt(V_)}/{fmt(base)}', savec(c, 'pVh', p, q, h))
    # h_from_S
    Sb = (p + q + hy) * h
    return T.add(lv, f'Основа прямої призми — прямокутний трикутник із катетами {p} і {q}. Площа бічної поверхні дорівнює {Sb}. Знайдіть висоту призми.', h,
        [(F(Sb, p + q), 'не враховано гіпотенузу в периметрі'), (F(Sb, p * q), 'периметр замінено добутком катетів'), (F(Sb, 2 * (p + q + hy)), 'периметр основи подвоєно')],
        'висота = S бічна / P основи', f'P = {p} + {q} + {hy} = {p+q+hy}, h = {Sb}/{p+q+hy}', savec(c, 'phS', p, q, h))

# 4. правильна чотирикутна піраміда
APO = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (6, 8, 10), (4, 3, 5), (12, 5, 13)]
LE = [(4, 1, 3), (8, 2, 6), (8, 7, 9), (12, 3, 9), (12, 7, 11)]
def f_pyramid(T, rng, lv):
    kind = rng.choice(['V', 'Sb_apo'] if lv == 1 else (['Sb', 'Sfull', 'edge', 'H_from_V'] if lv == 2 else ['edge_Sb', 'apo_from', 'H_from_edge']))
    c = C(330, 260)
    if kind in ('V', 'Sb_apo', 'Sb', 'Sfull', 'apo_from', 'H_from_V'):
        t, H, l = rng.choice(APO); a = 2 * t
        if kind == 'H_from_V': H = rng.choice([3, 6, 9]); t = rng.choice([2, 3, 4, 5]); a = 2 * t; l = None
        V = pyr(c, 1.8, 1.2, 1.5, (60, 215), 90, apo=True)
        sidel(c, V, str(a)); dimtxt(c, V['S'], V['O'], str(H), (14, -4), RED)
        if kind == 'V':
            return T.add(lv, f'У правильній чотирикутній піраміді SABCD сторона основи дорівнює {a}, а висота SO — {H} (рисунок). Знайдіть об’єм піраміди.', F(a * a * H, 3),
                [(a * a * H, 'не враховано множник ⅓'), (F(a * H, 3), 'площу основи замінено стороною'), (F(a * a * H, 2), 'замість ⅓ узято ½')],
                'V = ⅓·Sосн·H', f'V = ⅓·{a}²·{H}', savec(c, 'yV', a, H))
        if kind == 'H_from_V':
            Vv = F(a * a * H, 3)
            return T.add(lv, f'Об’єм правильної чотирикутної піраміди дорівнює {fmt(Vv)}, сторона основи — {a}. Знайдіть висоту піраміди.', H,
                [(F(Vv, a * a), 'не враховано множник ⅓ у формулі об’єму'), (F(3 * Vv, a), 'площу основи замінено стороною'), (F(2 * Vv, a * a), 'замість ⅓ узято ½')],
                'H = 3V / Sосн', f'H = 3·{fmt(Vv)}/{a*a}', savec(c, 'yH', a, H))
        c.text(V['M'][0] + 24, V['M'][1] - 22, '', size=10)
        dimtxt(c, V['S'], V['M'], 'l', (-13, 0), GREEN)
        if kind == 'Sb_apo':
            return T.add(lv, f'У правильній чотирикутній піраміді сторона основи дорівнює {a}, апофема SM = {l} (рисунок). Знайдіть площу бічної поверхні.', 2 * a * l,
                [(a * l, 'враховано лише дві бічні грані'), (F(a * l, 2), 'знайдено площу лише однієї бічної грані'), (a * a + 2 * a * l, 'додано площу основи — це повна поверхня')],
                'Sбічна = ½·P основи·l = 2a·l', f'Sб = ½·4·{a}·{l}', savec(c, 'ySa', a, l))
        if kind == 'Sb':
            return T.add(lv, f'У правильній чотирикутній піраміді сторона основи дорівнює {a}, висота {H}. Знайдіть площу бічної поверхні.', 2 * a * l,
                [(2 * a * H, 'замість апофеми взято висоту'), (a * l, 'враховано лише дві бічні грані'), (2 * a * t, 'замість апофеми взято половину сторони основи')],
                'апофема l = √(H² + (a/2)²), Sб = 2a·l', f'l = √({H}² + {t}²) = {l}', savec(c, 'ySb', a, H))
        if kind == 'Sfull':
            return T.add(lv, f'У правильній чотирикутній піраміді сторона основи дорівнює {a}, висота {H}. Знайдіть площу повної поверхні.', a * a + 2 * a * l,
                [(2 * a * l, 'не додано площу основи'), (a * a + 2 * a * H, 'замість апофеми взято висоту'), (a * a + a * l, 'бічну поверхню враховано лише наполовину')],
                'Sповна = Sосн + Sбічна; апофема l = √(H² + (a/2)²)', f'l = {l}, S = {a*a} + 2·{a}·{l}', savec(c, 'ySf', a, H))
        # apo_from: апофема з бічної поверхні
        Sb = 2 * a * l
        return T.add(lv, f'Площа бічної поверхні правильної чотирикутної піраміди дорівнює {Sb}, сторона основи — {a}. Знайдіть апофему.', l,
            [(F(Sb, a), 'не враховано, що бічних граней чотири'), (F(Sb, 4 * a), 'площу чотирьох граней поділено на чотири сторони'), (F(Sb, a * a), 'поділено на площу основи')],
            'Sб = 2a·l, звідси l = Sб/(2a)', f'l = {Sb}/(2·{a})', savec(c, 'yl', a, l))
    a, H, b = rng.choice(LE); V = pyr(c, 1.8, 1.2, 1.5, (60, 215), 90)
    sidel(c, V, str(a)); dimtxt(c, V['S'], V['O'], str(H), (14, -4), RED)
    if kind == 'edge':
        return T.add(lv, f'У правильній чотирикутній піраміді сторона основи дорівнює {a}, висота {H} (рисунок). Знайдіть бічне ребро.', b,
            [(rad(1, H * H + (a // 2) ** 2), 'замість половини діагоналі основи взято половину сторони'), (rad(1, H * H + a * a), 'замість половини діагоналі взято сторону основи'), (H + a // 2, 'бічне ребро замінено сумою катетів')],
            'бічне ребро — гіпотенуза з катетами H і AO = a√2/2', f'AO² = {a*a//2}, SA = √({H}² + {a*a//2}) = {b}', savec(c, 'ye', a, H))
    if kind == 'edge_Sb':
        l2 = H * H + (a // 2) ** 2
        return T.add(lv, f'У правильній чотирикутній піраміді сторона основи дорівнює {a}, висота {H}. Знайдіть апофему бічної грані.', rad(1, l2),
            [(b, 'взято бічне ребро замість апофеми'), (H, 'апофему вважали висотою'), (rad(1, H * H + a * a), 'замість половини сторони основи взято всю сторону')],
            'апофема — гіпотенуза трикутника з катетами H і a/2', f'l = √({H}² + {a//2}²) = √{l2}', savec(c, 'yl2', a, H))
    # H_from_edge
    return T.add(lv, f'У правильній чотирикутній піраміді сторона основи дорівнює {a}, бічне ребро — {b}. Знайдіть висоту піраміди.', H,
        [(rad(1, b * b - (a // 2) ** 2), 'замість половини діагоналі основи віднято половину сторони'), (rad(1, b * b - a * a // 2 + 1) if False else (b * b - a * a // 2), 'не добуто квадратний корінь'), (b - a // 2, 'катет знайдено як різницю гіпотенузи й катета')] + ([(rad(1, b * b - a * a), 'замість половини діагоналі основи віднято сторону')] if b * b > a * a else []),
        'H² = b² − (a√2/2)²', f'H² = {b}² − {a*a//2} = {H*H}', savec(c, 'yHe', a, H))

# 4b. кут нахилу грані до основи
def f_pyr_angle(T, rng, lv):
    a = rng.choice(range(4, 31, 2))
    phi = rng.choice([30, 45, 60])
    c = C(330, 260); V = pyr(c, 1.8, 1.2, 1.5, (60, 215), 90, apo=True)
    S.angle_arc(c, V['M'], V['S'], V['O'], 26, ORANGE, 'φ'); sidel(c, V, str(a))
    Hs = {30: rad(a, 3, 6), 45: fmt(F(a, 2)), 60: rad(a, 3, 2)}
    ws = {30: [(fmt(F(a, 2)), 'взято tg 45°, а не tg 30°'), (rad(a, 3, 2), 'взято tg 60°, а не tg 30°'), (rad(a, 3, 3), 'у tg 30° = 1/√3 половину сторони замінено стороною')],
          45: [(rad(a, 3, 6), 'взято tg 30°'), (rad(a, 3, 2), 'взято tg 60°'), (fmt(a), 'половину сторони замінено стороною основи')],
          60: [(fmt(F(a, 2)), 'взято tg 45°'), (rad(a, 3, 6), 'взято tg 30°'), (rad(a, 3), 'половину сторони замінено стороною основи')]}
    return T.add(lv, f'У правильній чотирикутній піраміді сторона основи дорівнює {a}. Бічна грань нахилена до площини основи під кутом {phi}° (рисунок). Знайдіть висоту піраміди.', Hs[phi], ws[phi],
        'кут нахилу грані вимірюють між апофемою та її проєкцією OM = a/2', f'H = OM·tg {phi}° = {fmt(F(a,2))}·tg {phi}°', savec(c, 'ya', a, phi))

# 5. циліндр
def f_cylinder(T, rng, lv):
    d2, h, dg = rng.choice([(6, 8, 10), (8, 6, 10), (10, 24, 26), (12, 5, 13), (6, 8, 10), (8, 6, 10), (24, 10, 26), (12, 16, 20), (16, 12, 20)])
    R = d2 // 2; R_ = R
    c = C(300, 250); cyl(c, 140, 195, 70, 110, labR=str(R), labh=str(h))
    kind = rng.choice(['V', 'Sb'] if lv == 1 else (['St', 'diag', 'sq'] if lv == 2 else ['sect_area', 'h_from_V', 'diag_R']))
    if kind == 'V':
        return T.add(lv, f'Радіус основи циліндра дорівнює {R}, висота — {h} (рисунок). Знайдіть об’єм циліндра.', pis(R * R * h),
            [(pis(F(R * R * h, 3)), 'застосовано формулу конуса'), (pis(2 * R * h), 'знайдено площу бічної поверхні'), (pis(d2 * d2 * h), 'діаметр підставлено замість радіуса'), (pis(R * h * h), 'радіус і висоту переплутано в формулі')],
            'V = πR²h', f'V = π·{R}²·{h}', savec(c, 'cV', R, h))
    if kind == 'Sb':
        return T.add(lv, f'Радіус основи циліндра дорівнює {R}, висота — {h} (рисунок). Знайдіть площу бічної поверхні.', pis(2 * R * h),
            [(pis(R * R * h), 'знайдено об’єм'), (pis(R * h), 'не враховано множник 2'), (pis(2 * R * (R + h)), 'знайдено площу повної поверхні'), (pis(2 * R * R), 'висоту прирівняно до радіуса')],
            'Sбічна = 2πRh', f'Sб = 2π·{R}·{h}', savec(c, 'cSb', R, h))
    if kind == 'St':
        return T.add(lv, f'Радіус основи циліндра дорівнює {R}, висота — {h}. Знайдіть площу повної поверхні циліндра.', pis(2 * R * (R + h)),
            [(pis(2 * R * h), 'не додано площі основ'), (pis(2 * R * h + R * R), 'додано площу лише однієї основи'), (pis(2 * R * h + 4 * R), 'до бічної поверхні додано довжини кіл замість площ основ')],
            'Sповна = 2πR(R + h)', f'S = 2π·{R}·({R} + {h})', savec(c, 'cSt', R, h))
    if kind == 'diag':
        c.line(140 - 70, 195 - 110, 140 + 70, 195, col=RED, w=1.6, dash='3,3')
        return T.add(lv, f'Осьовим перерізом циліндра є прямокутник із діагоналлю {dg}. Радіус основи дорівнює {R}. Знайдіть висоту циліндра.', h,
            [(dg - R, 'від діагоналі віднято радіус'), (rad(1, dg * dg - R * R), 'замість діаметра у перерізі взято радіус'), (dg - d2, 'від діагоналі віднято діаметр')],
            'у перерізі діагональ — гіпотенуза з катетами 2R та h', f'h = √({dg}² − {d2}²) = {h}', savec(c, 'cdg', R, h))
    if kind == 'sq':
        return T.add(lv, f'Осьовий переріз циліндра — квадрат зі стороною {d2}. Знайдіть об’єм циліндра.', pis(R * R * d2),
            [(pis(R * R * R), 'висоту прирівняно до радіуса'), (pis(d2 * d2 * d2), 'діаметр підставлено замість радіуса'), (pis(2 * R * d2), 'знайдено площу бічної поверхні')],
            'у квадраті висота дорівнює діаметру основи', f'R = {R}, h = {d2}, V = π·{R}²·{d2}', savec(c, 'cq', R))
    if kind == 'sect_area':
        return T.add(lv, f'Радіус основи циліндра дорівнює {R}, висота — {h}. Знайдіть площу осьового перерізу.', d2 * h,
            [(R * h, 'замість діаметра взято радіус'), (pis(R * R), 'знайдено площу основи'), (pis(d2 * h), 'додано зайвий множник π')],
            'осьовий переріз — прямокутник 2R × h', f'S = {d2}·{h}', savec(c, 'cA', R, h))
    if kind == 'h_from_V':
        return T.add(lv, f'Об’єм циліндра дорівнює {pis(R*R*h)}, радіус основи — {R}. Знайдіть висоту.', h,
            [(F(R * R * h, R), 'у знаменник підставлено радіус, а не R²'), (F(R * R * h, 3 * R * R), 'застосовано формулу конуса'), (h * R, 'висоту знайдено множенням на радіус')],
            'h = V/(πR²)', f'h = {R*R*h}/{R*R}', savec(c, 'chV', R, h))
    # diag_R: радіус з діагоналі й висоти
    return T.add(lv, f'Діагональ осьового перерізу циліндра дорівнює {dg}, висота — {h}. Знайдіть радіус основи.', R,
        [(d2, 'знайдено діаметр, а не радіус'), (dg - h, 'від діагоналі віднято висоту'), (dg * dg - h * h, 'не добуто корінь')],
        'діаметр = √(d² − h²), радіус — його половина', f'2R = √({dg}² − {h}²) = {d2}', savec(c, 'cR', R, h))

# 6. конус
def f_cone(T, rng, lv):
    R, h, l = rng.choice(TRI + [(12, 5, 13), (8, 6, 10), (15, 8, 17), (24, 7, 25), (4, 3, 5), (12, 9, 15)])
    c = C(300, 250); cone(c, 150, 200, 80, 125, labR=str(R), labh=str(h), labl=str(l))
    kind = rng.choice(['V', 'Sb'] if lv == 1 else (['St', 'sect', 'l_from'] if lv == 2 else ['sector', 'R_from_Sb', 'V_from_l']))
    if kind == 'V':
        return T.add(lv, f'Радіус основи конуса дорівнює {R}, висота — {h} (рисунок). Знайдіть об’єм конуса.', pis(F(R * R * h, 3)),
            [(pis(R * R * h), 'не враховано множник ⅓'), (pis(F(R * R * l, 3)), 'замість висоти взято твірну'), (pis(F(R * h, 3)), 'замість R² взято R'), (pis(F(2 * R * R * h, 3)), 'замість ⅓ узято ⅔')],
            'V = ⅓πR²h', f'V = ⅓π·{R}²·{h}', savec(c, 'nV', R, h))
    if kind == 'Sb':
        return T.add(lv, f'Радіус основи конуса дорівнює {R}, твірна — {l} (рисунок). Знайдіть площу бічної поверхні.', pis(R * l),
            [(pis(2 * R * l), 'використано довжину кола замість половини'), (pis(R * h), 'замість твірної взято висоту'), (pis(R * (R + l)), 'знайдено площу повної поверхні')],
            'Sбічна = πRl', f'Sб = π·{R}·{l}', savec(c, 'nSb', R, l))
    if kind == 'St':
        return T.add(lv, f'Радіус основи конуса дорівнює {R}, висота — {h}. Знайдіть площу повної поверхні конуса.', pis(R * (R + l)),
            [(pis(R * l), 'не додано площу основи'), (pis(R * (R + h)), 'замість твірної взято висоту'), (pis(2 * R * l + R * R), 'бічну поверхню подвоєно')],
            'твірна l = √(R² + h²), Sповна = πR(R + l)', f'l = {l}, S = π·{R}·({R} + {l})', savec(c, 'nSt', R, h))
    if kind == 'sect':
        return T.add(lv, f'Радіус основи конуса дорівнює {R}, висота — {h}. Знайдіть площу осьового перерізу.', R * h,
            [(F(R * h, 2), 'не враховано, що основа трикутника — діаметр'), (R * l, 'замість висоти взято твірну'), (pis(R * l), 'знайдено бічну поверхню')],
            'осьовий переріз — рівнобедрений трикутник з основою 2R і висотою h', f'S = ½·{2*R}·{h}', savec(c, 'nA', R, h))
    if kind == 'l_from':
        return T.add(lv, f'Висота конуса дорівнює {h}, радіус основи — {R}. Знайдіть твірну.', l,
            [(h + R, 'твірну знайдено як суму висоти й радіуса'), (rad(1, abs(h * h - R * R)), 'квадрати катетів віднімали замість додавання'), (R * R + h * h, 'не добуто корінь')],
            'l² = R² + h²', f'l = √({R}² + {h}²) = {l}', savec(c, 'nl', R, h))
    if kind == 'sector':
        ang = F(360 * R, l)
        if ang.denominator != 1: return False
        return T.add(lv, f'Розгорткою бічної поверхні конуса є круговий сектор. Радіус основи конуса — {R}, твірна — {l}. Знайдіть центральний кут сектора (у градусах).', ang,
            [(F(180 * R, l), 'взято половину кута: довжину основи прийнято за довжину півкола'), (F(360 * (l - R), l), 'замість радіуса основи взято різницю l − R'), (F(360 * h, l), 'замість радіуса взято висоту')],
            'довжина дуги сектора дорівнює довжині кола основи: φ = 360°·R/l', f'φ = 360°·{R}/{l}', savec(c, 'nsec', R, l))
    if kind == 'R_from_Sb':
        return T.add(lv, f'Площа бічної поверхні конуса дорівнює {pis(R*l)}, твірна — {l}. Знайдіть радіус основи.', R,
            [(F(R, 2), 'використано формулу бічної поверхні 2πRl'), (l, 'радіус прирівняно до твірної'), (h, 'замість радіуса взято висоту')],
            'R = Sб/(πl)', f'R = {R*l}/{l}', savec(c, 'nR', R, l))
    return T.add(lv, f'Твірна конуса дорівнює {l}, радіус основи — {R}. Знайдіть об’єм конуса.', pis(F(R * R * h, 3)),
        [(pis(F(R * R * l, 3)), 'замість висоти взято твірну'), (pis(R * R * h), 'не враховано множник ⅓'), (pis(F(R * R * (l - R), 3)), 'висоту знайдено як різницю твірної та радіуса')],
        'спочатку висота h = √(l² − R²)', f'h = {h}, V = ⅓π·{R}²·{h}', savec(c, 'nVl', R, l))

# 7. куля
def sphere(c, cx, cy, R, d=None, r=None, labR=True):
    c.circle(cx, cy, R, fill='#eff6ff', stroke=INK, sw=2)
    c.path(f'M{cx-R},{cy} A{R},{R*0.3} 0 0 0 {cx+R},{cy}', stroke=INK, w=1.4)
    c.path(f'M{cx-R},{cy} A{R},{R*0.3} 0 0 1 {cx+R},{cy}', stroke=INK, w=1.2, dash='4,3')
    c.dot(cx, cy, 3.5, RED); c.text(cx - 14, cy + 4, 'O', size=13, col=RED, bold=True, anchor='middle')
    if labR:
        c.line(cx, cy, cx + R * 0.7, cy - R * 0.7, col=BLUE, w=2); c.text(cx + R * 0.35 + 8, cy - R * 0.35 - 10, 'R', size=14, col=BLUE, bold=True)
def f_sphere(T, rng, lv):
    kind = rng.choice(['V', 'S'] if lv == 1 else (['sec_area', 'R_from'] if lv == 2 else ['d_from', 'sec_R', 'ratio']))
    c = C(300, 250)
    if kind in ('V', 'S'):
        R = rng.choice([3, 6, 9, 12, 2, 4, 5, 7, 10]); sphere(c, 150, 130, 85)
        c.text(150, 235, f'R = {R}', size=14, anchor='middle', bold=True, col=BLUE)
        if kind == 'V':
            return T.add(lv, f'Радіус кулі дорівнює {R} (рисунок). Знайдіть об’єм кулі.', pis(F(4 * R ** 3, 3)),
                [(pis(4 * R * R), 'знайдено площу поверхні'), (pis(F(R ** 3, 3)), 'пропущено множник 4'), (pis(F(4 * R * R * 2, 3)) if R != 2 else pis(F(2 * R ** 3, 3)), 'степінь радіуса знижено до другого' if R != 2 else 'знайдено об’єм півкулі'), (pis(F(2 * R ** 3, 3)), 'знайдено об’єм півкулі')],
                'V = ⁴⁄₃πR³', f'V = 4π·{R}³/3', savec(c, 'sV', R))
        return T.add(lv, f'Радіус кулі дорівнює {R} (рисунок). Знайдіть площу поверхні кулі.', pis(4 * R * R),
            [(pis(F(4 * R ** 3, 3)), 'знайдено об’єм'), (pis(R * R), 'пропущено множник 4'), (pis(2 * R * R), 'взято 2πR² (півсфера без основи)')],
            'S = 4πR²', f'S = 4π·{R}²', savec(c, 'sS', R))
    Rr, d, r = rng.choice([(5, 3, 4), (13, 5, 12), (10, 6, 8), (17, 8, 15), (25, 7, 24), (25, 15, 20), (15, 9, 12), (26, 10, 24)])
    sphere(c, 150, 120, 85, labR=False)
    ry = 85 * 0.3 * r / Rr; yc = 120 - 85 * d / Rr; rx = 85 * r / Rr
    c.ellipse(150, yc, rx, ry * 1.0 if ry > 3 else 3, fill='#fde68a', stroke=SECS, sw=2)
    c.line(150, 120, 150, yc, col=RED, w=1.8, dash='4,3'); c.dot(150, yc, 3, SECS)
    c.line(150, yc, 150 + rx, yc, col=SECS, w=2)
    c.line(150, 120, 150 + rx, yc, col=BLUE, w=2)
    c.text(156, (120 + yc) / 2 + 10, 'd', size=14, col=RED, bold=True); c.text(150 + rx / 2, yc + 14, 'r', size=14, col=SECS, bold=True, anchor='middle'); c.text(150 + rx / 2 + 14, (120 + yc) / 2 + 4, 'R', size=14, col=BLUE, bold=True)
    if kind == 'sec_area':
        return T.add(lv, f'Кулю радіуса {Rr} перетято площиною на відстані {d} від центра (рисунок). Знайдіть площу перерізу.', pis(r * r),
            [(pis(Rr * Rr), 'взято площу великого круга'), (pis(d * d), 'радіус перерізу прирівняно до відстані'), (pis((Rr - d) ** 2), 'радіус перерізу знайдено як різницю R і d')],
            'r² = R² − d²', f'r² = {Rr}² − {d}² = {r*r}', savec(c, 'sA', Rr, d))
    if kind == 'R_from':
        return T.add(lv, f'Площина перетинає кулю на відстані {d} від центра. Радіус кола перерізу дорівнює {r}. Знайдіть радіус кулі.', Rr,
            [(r + d, 'радіус кулі знайдено як суму r і d'), (rad(1, abs(r * r - d * d)) if r != d else r, 'квадрати віднімали замість додавання'), (r * r + d * d, 'не добуто корінь')],
            'R² = r² + d²', f'R = √({r}² + {d}²) = {Rr}', savec(c, 'sR', Rr, d))
    if kind == 'd_from':
        return T.add(lv, f'Радіус кулі дорівнює {Rr}, радіус кола перерізу — {r}. Знайдіть відстань від центра кулі до площини перерізу.', d,
            [(Rr - r, 'відстань знайдено як різницю радіусів'), (rad(1, Rr * Rr + r * r), 'квадрати додавали замість віднімання'), (Rr * Rr - r * r, 'не добуто корінь')],
            'd² = R² − r²', f'd = √({Rr}² − {r}²) = {d}', savec(c, 'sd', Rr, r))
    if kind == 'sec_R':
        return T.add(lv, f'Радіус кулі дорівнює {Rr}. Площа перерізу кулі площиною дорівнює {pis(r*r)}. Знайдіть відстань від центра кулі до площини.', d,
            [(rad(1, Rr * Rr + r * r), 'квадрати додавали замість віднімання'), (Rr - r, 'радіуси відняли без квадратів'), (r, 'відстань прирівняно до радіуса перерізу')],
            'r = √(площа/π), d² = R² − r²', f'r = {r}, d = √({Rr*Rr} − {r*r}) = {d}', savec(c, 'sd2', Rr, r))
    k = rng.choice([2, 3])
    sphere(c, 150, 120, 70)
    return T.add(lv, f'Радіус кулі збільшили у {raz(k)}. У скільки разів збільшився її об’єм?', k ** 3,
        [(k * k, 'знайдено збільшення площі поверхні'), (k, 'об’єм вважали пропорційним радіусу'), (k ** 3 * 4, 'до відношення додано коефіцієнт формули')],
        'V ∝ R³', f'V₂/V₁ = {k}³', savec(c, 'sk', k))

# 8. розгортки куба
def cube_fold(cells):
    cells = set(cells); start = min(cells)
    die = {'top': 0, 'bottom': 1, 'north': 2, 'south': 3, 'east': 4, 'west': 5}
    faces = {start: die['bottom']}; st = {start: die}; q = [start]; seen = {start}
    while q:
        cur = q.pop(0); s = st[cur]
        for dr, dc, mv in ((0, 1, 'e'), (0, -1, 'w'), (-1, 0, 'n'), (1, 0, 's')):
            nx = (cur[0] + dr, cur[1] + dc)
            if nx in cells and nx not in seen:
                seen.add(nx); ns = dict(s)
                if mv == 'e': ns['top'], ns['east'], ns['bottom'], ns['west'] = s['west'], s['top'], s['east'], s['bottom']
                if mv == 'w': ns['top'], ns['west'], ns['bottom'], ns['east'] = s['east'], s['top'], s['west'], s['bottom']
                if mv == 'n': ns['top'], ns['north'], ns['bottom'], ns['south'] = s['south'], s['top'], s['north'], s['bottom']
                if mv == 's': ns['top'], ns['south'], ns['bottom'], ns['north'] = s['north'], s['top'], s['south'], s['bottom']
                st[nx] = ns; faces[nx] = ns['bottom']; q.append(nx)
    return faces
def net_valid(cells): return len(set(cube_fold(cells).values())) == 6
def norm_net(cells):
    best = None
    pts = list(cells)
    for _ in range(2):
        for _r in range(4):
            pts = [(c_, -r_) for r_, c_ in pts]
            mr = min(p[0] for p in pts); mc = min(p[1] for p in pts)
            sh = tuple(sorted((r_ - mr, c_ - mc) for r_, c_ in pts))
            if best is None or sh < best: best = sh
        pts = [(r_, -c_) for r_, c_ in pts]
    return best
def rand_net(rng, w=4, hh=4):
    cells = {(rng.randint(0, hh - 1), rng.randint(0, w - 1))}
    while len(cells) < 6:
        r_, c_ = rng.choice(sorted(cells)); dr, dc = rng.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        nx = (r_ + dr, c_ + dc)
        if 0 <= nx[0] < hh and 0 <= nx[1] < w: cells.add(nx)
    mr = min(p[0] for p in cells); mc = min(p[1] for p in cells)
    return tuple(sorted((r_ - mr, c_ - mc) for r_, c_ in cells))
def draw_nets(c, nets, labels='АБВГ', cols=2, pw=190, ph=145, cs=26, x0=14, y0=20):
    for i, cells in enumerate(nets):
        px = x0 + (i % cols) * pw; py = y0 + (i // cols) * ph
        c.text(px + 4, py + 14, labels[i] + ')', size=15, bold=True, col=PURPLE)
        for r_, c_ in cells: c.rect(px + 22 + c_ * cs, py + 22 + r_ * cs, cs, cs, fill='#dbeafe', stroke=INK, sw=1.6)
def f_net(T, rng, lv):
    want_valid = rng.random() < 0.6
    valid, invalid = [], []
    tries = 0
    while (len(valid) < (1 if want_valid else 3) or len(invalid) < (3 if want_valid else 1)) and tries < 3000:
        tries += 1; n_ = rand_net(rng, 4 if lv < 3 else 4, 4)
        k_ = norm_net(n_)
        if any(norm_net(x) == k_ for x in valid + invalid): continue
        (valid if net_valid(n_) else invalid).append(n_)
    if len(valid) < (1 if want_valid else 3) or len(invalid) < (3 if want_valid else 1): return False
    if want_valid: ans = valid[0]; others = invalid[:3]; q = 'Яка з фігур є розгорткою куба?'
    else: ans = invalid[0]; others = valid[:3]; q = 'Яка з фігур НЕ є розгорткою куба?'
    nets = [ans] + list(others); idx = list(range(4)); rng.shuffle(idx)
    order = [nets[i] for i in idx]; pos = idx.index(0)
    c = C(400, 300); draw_nets(c, order)
    L = 'АБВГ'
    def desc(n_):
        rows = {}
        for r_, c_ in n_: rows[r_] = rows.get(r_, 0) + 1
        return '-'.join(str(rows[r_]) for r_ in sorted(rows))
    def why_bad(n_):
        f = cube_fold(n_); cnt = {}
        for cell, fc in f.items(): cnt.setdefault(fc, []).append(cell)
        dup = [v for v in cnt.values() if len(v) > 1]
        return f'під час згортання {len(dup[0])} клітинки накладаються на одну грань, а якась грань куба залишається порожньою'
    wr = []
    for i, n_ in enumerate(order):
        if i == pos: continue
        wr.append((f'{L[i]} (рядки {desc(n_)})', why_bad(n_) if want_valid else 'ця фігура згортається в куб без накладань: шість різних граней'))
    sol = 'усі шість клітинок потрапляють на різні грані куба' if want_valid else why_bad(ans)
    return T.add(lv, q + ' (рисунок; у дужках — кількість клітинок у рядках зверху вниз)', f'{L[pos]} (рядки {desc(ans)})', wr, 'перевіряй згортання: жоден ряд не має більше 4 клітинок, і грані не повинні накладатися', sol, savec(c, 'net', *[str(sorted(x)) for x in order]))

# 9. Ейлер / многогранники
def nprism(c, n_, cx, cy, R, h, pyramid=False):
    pts_b = []
    for i in range(n_):
        t = 2 * math.pi * i / n_ + math.pi / 2 * 0 + 0.3
        pts_b.append((cx + R * math.cos(t), cy - 0.3 * R * math.sin(t), math.sin(t)))
    top = [(x, y - h) for x, y, d in pts_b]
    def hid_edge(i, j): return (pts_b[i][2] + pts_b[j][2]) / 2 > 0.3
    for i in range(n_):
        j = (i + 1) % n_
        c.line(pts_b[i][0], pts_b[i][1], pts_b[j][0], pts_b[j][1], col=INK, w=2, dash='5,4' if hid_edge(i, j) else None)
    if not pyramid:
        c.poly(top, stroke=INK, w=2, fill='none')
        for i in range(n_): c.line(pts_b[i][0], pts_b[i][1], top[i][0], top[i][1], col=INK, w=2, dash='5,4' if pts_b[i][2] > 0.3 else None)
    else:
        ap = (cx, cy - h)
        for i in range(n_): c.line(pts_b[i][0], pts_b[i][1], ap[0], ap[1], col=INK, w=2, dash='5,4' if pts_b[i][2] > 0.3 else None)
NAMES = {3: 'трикутна', 4: 'чотирикутна', 5: 'п’ятикутна', 6: 'шестикутна', 7: 'семикутна', 8: 'восьмикутна'}
def f_count(T, rng, lv):
    n_ = rng.randint(3, 6 if lv == 1 else 8); pyramid = rng.random() < 0.5
    c = C(280, 230); nprism(c, n_, 140, 170 if not pyramid else 185, 78, 110, pyramid)
    nm = 'піраміда' if pyramid else 'призма'; Vn, En, Fn = ((n_ + 1, 2 * n_, n_ + 1) if pyramid else (2 * n_, 3 * n_, n_ + 2))
    kind = rng.choice(['E', 'V', 'F'])
    img = savec(c, 'cnt', n_, pyramid)
    title = f'{NAMES[n_].capitalize()} {nm}' if pyramid else f'{NAMES[n_].capitalize()} призма'
    if kind == 'E':
        ans = En; wr = [(n_ if pyramid else 2 * n_, 'враховано лише ребра основи' if pyramid else 'враховано лише ребра двох основ'), (Vn + Fn, 'вершини й грані додано без віднімання 2'), (Vn + Fn - 1, 'у формулі Ейлера віднято 1 замість 2'), (En + n_, 'бічні ребра пораховано двічі'), (Vn + Fn + 2, 'до суми вершин і граней додано 2')]
        sol = f'ребер: {En}'
    elif kind == 'V':
        ans = Vn; wr = [(Fn, 'пораховано грані'), (En, 'пораховано ребра'), (n_, 'не враховано вершини ' + ('вершини піраміди' if pyramid else 'другої основи')), (Vn + 1, 'пораховано зайву вершину'), (Vn + 2, 'до числа вершин додано 2')]
        sol = f'вершин: {Vn}'
    else:
        ans = Fn; wr = [(n_, 'враховано лише бічні грані'), (n_ + 2 if pyramid else n_ + 1, 'пораховано ' + ('дві основи, як у призмі' if pyramid else 'лише одну основу')), (Vn, 'пораховано вершини'), (En, 'пораховано ребра'), (n_ + 3, 'пораховано три зайві грані')]
        sol = f'граней: {Fn}'
    qt = {'E': 'ребер', 'V': 'вершин', 'F': 'граней'}[kind]
    if lv == 3 and rng.random() < 0.5:
        # зворотне завдання: за кількістю ребер
        return T.add(lv, f'Многогранник — {nm}, в основі якої лежить n-кутник. Усього в неї {En} ребер. Скільки в неї граней (включно з основами)?', Fn,
            [(En // (2 if pyramid else 3), 'знайдено кількість сторін основи, а не граней'), (Vn, 'пораховано вершини'), (En - n_, 'від ребер відняли сторони основи')],
            ('E = 2n для піраміди' if pyramid else 'E = 3n для призми') + ', грані: ' + ('n + 1' if pyramid else 'n + 2'), f'n = {n_}, граней {Fn}', img)
    return T.add(lv, f'Скільки {qt} має {title.lower()} (рисунок)?', ans, wr, 'ребра, вершини й грані підраховуй окремо; перевір за формулою Ейлера B − P + Г = 2', sol + f'; перевірка: {Vn} − {En} + {Fn} = 2', img)

# 10. пофарбований куб
def grid_cube(c, n_, o, k):
    a = n_
    # три видимі грані: front (y=0), top (z=n), right (x=n)
    for i in range(n_ + 1):
        c.line(*P(i, 0, 0, o, k), *P(i, 0, a, o, k), col=GRAY, w=1)
        c.line(*P(0, 0, i, o, k), *P(a, 0, i, o, k), col=GRAY, w=1)
        c.line(*P(i, 0, a, o, k), *P(i, a, a, o, k), col=GRAY, w=1)
        c.line(*P(0, i, a, o, k), *P(a, i, a, o, k), col=GRAY, w=1)
        c.line(*P(a, i, 0, o, k), *P(a, i, a, o, k), col=GRAY, w=1)
        c.line(*P(a, 0, i, o, k), *P(a, a, i, o, k), col=GRAY, w=1)
    for p_, q_ in [((0, 0, 0), (a, 0, 0)), ((a, 0, 0), (a, a, 0)), ((0, 0, 0), (0, 0, a)), ((a, 0, 0), (a, 0, a)), ((a, a, 0), (a, a, a)), ((0, 0, a), (a, 0, a)), ((a, 0, a), (a, a, a)), ((0, 0, a), (0, a, a)), ((0, a, a), (a, a, a))]:
        c.line(*P(*p_, o, k), *P(*q_, o, k), col=INK, w=2.2)
def f_paint(T, rng, lv):
    n_ = rng.randint(3, 5 if lv == 1 else 9)
    c = C(300, 250); grid_cube(c, n_, (60, 205), 130 / n_)
    kind = rng.choice(['3', '0', '2', '1', 'any', 'area']) if lv > 1 else rng.choice(['3', '0', 'area'])
    cnt = {'any': n_ ** 3 - (n_ - 2) ** 3, 'area': 6 * n_ * n_, '3': 8, '2': 12 * (n_ - 2), '1': 6 * (n_ - 2) ** 2, '0': (n_ - 2) ** 3}
    txt = {'any': 'хоча б одну зафарбовану грань', 'area': 'зафарбованих квадратів (одиничних граней) отримано загалом', '3': 'три грані', '2': 'дві грані', '1': 'одну грань', '0': 'жодної грані'}
    pre = f'Куб із ребром {n_} зафарбували зовні та розрізали на {n_**3} кубиків з ребром 1 (рисунок). '
    ans = cnt[kind]
    allv = [8, 12 * (n_ - 2), 6 * (n_ - 2) ** 2, (n_ - 2) ** 3, 6 * n_ * n_, 12 * n_ - 16]
    reasons = {8: 'враховано лише кубики-вершини', 12 * (n_ - 2): 'враховано лише кубики на ребрах (без кутових)', 6 * (n_ - 2) ** 2: 'враховано лише кубики в центрі граней', (n_ - 2) ** 3: 'враховано лише внутрішні кубики',
               6 * n_ * n_: 'пораховано всі квадрати на гранях великого куба, а не кубики', 12 * n_ - 16: 'сума кубиків із двома та трьома зафарбованими гранями'}
    reasons[n_ ** 3 - (n_ - 2) ** 3] = 'кубики без фарби враховано як зафарбовані'; reasons[n_ ** 3] = 'взято всі кубики'
    allv += [n_ ** 3 - (n_ - 2) ** 3, n_ ** 3, 6 * (n_ - 2) ** 2 + 12 * (n_ - 2)]; reasons[6 * (n_ - 2) ** 2 + 12 * (n_ - 2)] = 'враховано лише кубики на ребрах і гранях без кутових'
    wr = [(v, reasons[v]) for v in dict.fromkeys(allv) if v != ans]
    q_ = {'3': 'Скільки кубиків мають зафарбованими три грані?', '2': 'Скільки кубиків мають зафарбованими дві грані?', '1': 'Скільки кубиків мають зафарбованою одну грань?', '0': 'Скільки кубиків не мають жодної зафарбованої грані?', 'any': 'Скільки кубиків мають хоча б одну зафарбовану грань?', 'area': 'Скільки одиничних квадратів на гранях цих кубиків зафарбовано (разом з усіх кубиків)?'}[kind]
    return T.add(lv, pre + q_, ans, wr, 'кубики поділяються за положенням: вершини, ребра, грані, внутрішні',
        {'any': f'усі кубики, крім внутрішнього куба ({n_}−2)³: {n_**3} − {(n_-2)**3}', 'area': f'зафарбовано 6 граней великого куба по {n_}² квадратів: 6·{n_*n_}', '3': 'кубики з трьома зафарбованими гранями — кутові, їх 8', '2': f'на кожному з 12 ребер {n_-2} кубиків без кутових: 12·{n_-2}', '1': f'на кожній із 6 граней ({n_}−2)² кубиків: 6·{(n_-2)**2}', '0': f'внутрішній куб із ребром {n_}−2: ({n_}−2)³'}[kind], savec(c, 'pt', n_, kind))

# 11. перерізи куба
def f_section(T, rng, lv):
    a = rng.randint(2, 9)
    kind = rng.choice(['tri_area', 'tri_perim'] if lv <= 2 else ['tri_area', 'rect', 'dist'])
    c = C(300, 240);
    if kind in ('tri_area', 'tri_perim'):
        V = box(c, 1.3, 1.3, 1.3, (60, 195), 100, hl=['A', 'B1', 'D1'])
        if kind == 'tri_area':
            return T.add(lv, f'Через вершини A, B₁ і D₁ куба ABCDA₁B₁C₁D₁ з ребром {a} проведено переріз (рисунок). Знайдіть його площу.', rad(a * a, 3, 2),
                [(F(a * a, 2), 'трикутник вважали прямокутним рівнобедреним з катетами a'), (rad(a * a, 3, 4), 'сторону трикутника взято рівною a, а не a√2'), (rad(a * a, 2), 'взято площу діагонального перерізу')],
                'сторони трикутника — діагоналі граней a√2, трикутник рівносторонній', f'S = (a√2)²·√3/4 = {a*a}·2·√3/4', savec(c, 'sec1', a))
        return T.add(lv, f'Через вершини A, B₁ і D₁ куба з ребром {a} проведено переріз (рисунок). Знайдіть його периметр.', rad(3 * a, 2),
            [(3 * a, 'сторони перерізу вважали рівними ребру'), (rad(3 * a, 3), 'сторони вважали рівними діагоналі куба'), (rad(2 * a, 2), 'враховано лише дві сторони')],
            'AB₁ = B₁D₁ = AD₁ = a√2 — діагоналі граней', f'P = 3a√2 = 3·{a}√2', savec(c, 'sec2', a))
    if kind == 'rect':
        V = box(c, 1.3, 1.3, 1.3, (60, 195), 100, hl=['A', 'C', 'C1', 'A1'])
        return T.add(lv, f'Куб ABCDA₁B₁C₁D₁ має ребро {a}. Знайдіть площу діагонального перерізу AA₁C₁C (рисунок).', rad(a * a, 2),
            [(a * a, 'взято площу грані'), (rad(a * a, 3), 'взято діагональ куба замість діагоналі грані'), (rad(a * a, 2, 2), 'площу прямокутника обчислено як для трикутника')],
            'переріз — прямокутник зі сторонами AC = a√2 і AA₁ = a', f'S = a√2·a = {a*a}√2', savec(c, 'sec3', a))
    V = box(c, 1.3, 1.3, 1.3, (60, 195), 100, hl=['A1', 'B', 'D'])
    return T.add(lv, f'Ребро куба ABCDA₁B₁C₁D₁ дорівнює {a}. Знайдіть відстань від вершини A₁ до прямої BD (рисунок).', rad(a, 6, 2),
        [(rad(a, 2), 'взято довжину A₁B, а не висоту трикутника'), (rad(a, 3, 2), 'висоту рівностороннього трикутника обчислено зі стороною a'), (fmt(a), 'відстань прирівняно до ребра')],
        'трикутник A₁BD рівносторонній зі стороною a√2; відстань — його висота', f'h = a√2·√3/2 = {a}√6/2', savec(c, 'sec4', a))

# 12. тетраедр із перпендикуляром (теорема про три перпендикуляри)
def tetra(c, A_, B_, H, o, k):
    nm = {'A': (0, 0, 0), 'B': (A_, 0, 0), 'C': (A_, B_, 0), 'S': (0, 0, H)}
    V = {n_: P(*p, o, k) for n_, p in nm.items()}
    for a_, b_ in [('A', 'B'), ('B', 'C'), ('S', 'A'), ('S', 'B'), ('S', 'C')]: c.line(*V[a_], *V[b_], col=INK, w=2)
    c.line(*V['A'], *V['C'], col=INK, w=2, dash='5,4')
    S.right_angle(c, V['A'], V['S'], V['B'], 12); S.right_angle(c, V['B'], V['A'], V['C'], 12)
    vlab(c, V, ['A', 'B', 'C', 'S'], ((V['A'][0] + V['C'][0]) / 2, (V['S'][1] + V['A'][1]) / 2))
    return V
def f_tetra(T, rng, lv):
    p, q, hy = rng.choice(TRI);
    if rng.random() < .5: p, q = q, p
    h = rng.randint(3, 12)
    c = C(320, 240); V = tetra(c, 1.7, 1.2, 1.5, (60, 205), 95)
    dimtxt(c, V['A'], V['B'], str(p), (0, 22)); dimtxt(c, V['B'], V['C'], str(q), (18, 10)); dimtxt(c, V['S'], V['A'], str(h), (-14, 0), RED)
    kind = rng.choice(['SB', 'SC'] if lv <= 2 else ['SC', 'BC_perp', 'angle'])
    sb2 = h * h + p * p
    if kind == 'SB':
        return T.add(lv, f'SA ⊥ (ABC), ∠ABC = 90°, AB = {p}, SA = {h} (рисунок). Знайдіть SB.', rad(1, sb2),
            [(p + h, 'гіпотенузу знайдено як суму катетів'), (rad(1, abs(h * h - p * p)) if h != p else h, 'квадрати віднімали замість додавання'), (sb2, 'не добуто корінь')],
            'трикутник SAB прямокутний (SA ⊥ AB)', f'SB² = {h}² + {p}² = {sb2}', savec(c, 'tSB', p, h))
    if kind == 'SC':
        sc2 = h * h + p * p + q * q
        return T.add(lv, f'SA ⊥ (ABC), ∠ABC = 90°, AB = {p}, BC = {q}, SA = {h} (рисунок). Знайдіть SC.', rad(1, sc2),
            [(rad(1, h * h + q * q), 'катет AB пропущено'), (rad(1, p * p + q * q), 'враховано лише основу'), (h + p + q, 'довжину знайдено як суму трьох катетів')],
            'SC² = SA² + AB² + BC² (теорема про три перпендикуляри: SB ⊥ BC)', f'SC² = {h}² + {p}² + {q}² = {sc2}', savec(c, 'tSC', p, q, h))
    if kind == 'BC_perp':
        sb2 = h * h + p * p
        return T.add(lv, f'SA ⊥ (ABC), ∠ABC = 90°, AB = {p}, BC = {q}, SA = {h}. Знайдіть площу трикутника SBC.', rad(q, sb2, 2),
            [(F(q * h, 2), 'взято SA замість SB'), (F(p * q, 2), 'знайдено площу трикутника ABC'), (rad(q, sb2), 'не враховано множник ½')],
            'SB ⊥ BC за теоремою про три перпендикуляри, тому S = ½·BC·SB', f'SB = √({h}² + {p}²), S = ½·{q}·SB', savec(c, 'tS', p, q, h))
    # angle: кут між SB і площиною основи: tg = h/p
    return T.add(lv, f'SA ⊥ (ABC), ∠ABC = 90°, AB = {p}, SA = {h}. Знайдіть тангенс кута між прямою SB та площиною основи ABC.', ffmt(F(h, p)),
        [(ffmt(F(p, h)), 'відношення катетів перевернуто'), (ffmt(F(h, hy if False else p + h)), 'у знаменнику сума катетів'), (rad(1, h * h + p * p) if False else ffmt(F(h * h, p * p)), 'тангенс піднесено до квадрата')],
        'кут між SB та площиною — це ∠SBA, бо AB — проєкція SB', f'tg∠SBA = SA/AB = {h}/{p}', savec(c, 'tA', p, h))

# 13. кут між діагоналлю й площиною основи
def f_boxangle(T, rng, lv):
    m = rng.randint(2, 14); phi = rng.choice([30, 45, 60])
    a = m; d2 = m * m * 2
    cc = {45: ('√2', m * m * 2), 30: None, 60: None}
    if phi == 45: hh = (m, 2); ch = rad(m, 2)
    elif phi == 60: hh = (m, 6); ch = rad(m, 6)
    else: hh = (m, 6); ch = rad(m, 6, 3)
    c = C(340, 250); V = box(c, 1.7, 1.0, 1.2, (60, 205), 100)
    c.line(*V['A'], *V['C1'], col=RED, w=2); c.line(*V['A'], *V['C'], col=RED, w=1.6, dash='4,3'); S.angle_arc(c, V['A'], V['C1'], V['C'], 30, ORANGE, 'φ')
    dimtxt(c, V['A'], V['B'], str(m), (0, 24)); dimtxt(c, V['B'], V['C'], str(m), (22, 12)); dimtxt(c, V['A'], V['A1'], ch, (-24, 0))
    cv = {45: m * 2 ** .5, 30: m * 6 ** .5 / 3, 60: m * 6 ** .5}[phi]; dv = m * 2 ** .5
    cands = [(math.degrees(math.atan(cv / m)), 'у тангенсі до висоти взято сторону AB, а не діагональ основи AC'), (math.degrees(math.atan(dv / cv)), 'відношення катетів перевернуто'), (math.degrees(math.atan(cv / (dv / 2))), 'взято половину діагоналі основи'), (math.degrees(math.atan(m / cv)), 'сторону основи поділено на висоту')]
    ws = [(deg(v), r) for v, r in cands if abs(v - phi) > 0.01]
    return T.add(lv, f'У прямокутному паралелепіпеді ABCDA₁B₁C₁D₁ основа ABCD — квадрат зі стороною {m}, бічне ребро AA₁ = {ch} (рисунок). Знайдіть кут φ між діагоналлю AC₁ та площиною основи.', f'{phi}°', ws[:4],
        'кут між прямою та площиною — кут між прямою та її проєкцією (AC)', f'AC = {m}√2, tg φ = CC₁/AC = {ch}/{m}√2 → φ = {phi}°', savec(c, 'ba', m, phi))

# 14. комбінації тіл
def f_inscr(T, rng, lv):
    a = rng.choice([2, 4, 6, 8, 10, 12]); c = C(300, 258)
    kind = rng.choice(['sph_in_cube', 'cyl_in_cube'] if lv <= 2 else ['cube_in_sph', 'sph_in_cyl', 'cyl_in_cube_S', 'sph_in_cube_ratio'])
    if kind == 'sph_in_cube':
        c.rect(70, 40, 160, 160, fill='#eff6ff'); c.circle(150, 120, 80, fill='#dbeafe', stroke=BLUE, sw=2.2); c.text(150, 246, f'ребро куба {a}', size=14, anchor='middle', bold=True, col=BLUE)
        return T.add(lv, f'У куб із ребром {a} вписано кулю (на рисунку — осьовий переріз). Знайдіть об’єм кулі.', pis(F(a ** 3, 6)),
            [(pis(F(4 * a ** 3, 3)), 'радіус вважали рівним ребру'), (pis(F(a ** 3, 24)), 'радіус вважали рівним a/4'), (pis(F(a ** 3, 8)), 'не враховано множник 4/3 у формулі кулі')],
            'радіус вписаної кулі R = a/2', f'R = {fmt(F(a,2))}, V = ⁴⁄₃π·({fmt(F(a,2))})³', savec(c, 'in1', a))
    if kind == 'cyl_in_cube':
        c.rect(70, 40, 160, 160, fill='#eff6ff'); c.rect(70, 40, 160, 160, stroke=INK, sw=2); c.text(150, 246, f'ребро куба {a}', size=14, anchor='middle', bold=True, col=BLUE)
        c.path('M70,200 A80,24 0 0 0 230,200', stroke=BLUE, w=2); c.path('M70,200 A80,24 0 0 1 230,200', stroke=BLUE, w=1.6, dash='5,4'); c.ellipse(150, 40, 80, 24, fill='#dbeafe', stroke=BLUE, sw=2)
        return T.add(lv, f'У куб із ребром {a} вписано циліндр, висота якого дорівнює ребру куба (рисунок). Знайдіть об’єм циліндра.', pis(F(a ** 3, 4)),
            [(pis(a ** 3), 'радіус основи вважали рівним ребру'), (pis(F(a ** 3, 2)), 'радіус взято як a/√2'), (pis(F(a ** 3, 3)), 'застосовано формулу конуса')],
            'радіус основи циліндра R = a/2', f'V = π·({fmt(F(a,2))})²·{a}', savec(c, 'in2', a))
    if kind == 'cube_in_sph':
        c.circle(150, 120, 90, fill='#eff6ff', stroke=BLUE, sw=2.2)
        c.poly([(150 - 52, 120 - 52), (150 + 52, 120 - 52), (150 + 52, 120 + 52), (150 - 52, 120 + 52)], stroke=INK, w=2, fill='#dbeafe'); c.line(98, 68, 202, 172, col=RED, w=1.6, dash='4,3')
        c.text(150, 246, f'ребро куба {a}', size=14, anchor='middle', bold=True, col=BLUE)
        return T.add(lv, f'У кулю вписано куб із ребром {a} (рисунок). Знайдіть радіус кулі.', rad(a, 3, 2),
            [(fmt(F(a, 2)), 'радіус прирівняно до половини ребра (вписана куля)'), (rad(a, 2, 2), 'взято половину діагоналі грані'), (rad(a, 3), 'взято діагональ куба, а не її половину')],
            'діагональ куба — діаметр кулі: 2R = a√3', f'R = {a}√3/2', savec(c, 'in3', a))
    if kind == 'sph_in_cyl':
        cyl(c, 150, 200, 70, 140, labR=None, labh=None, axis=False)
        c.circle(150, 130, 70, fill='#dbeafe', stroke=BLUE, sw=2)
        c.text(150, 226, f'радіус кулі {a}', size=14, anchor='middle', bold=True, col=BLUE)
        return T.add(lv, f'Кулю радіуса {a} вписано в циліндр (рисунок). Знайдіть площу бічної поверхні циліндра.', pis(4 * a * a),
            [(pis(2 * a * a), 'висоту циліндра вважали рівною радіусу'), (pis(8 * a * a), 'висоту циліндра взято як 4R'), (pis(F(4 * a ** 3, 3)), 'знайдено об’єм кулі')],
            'вписана куля торкається основ: h = 2R, радіус циліндра R', f'Sб = 2π·{a}·{2*a}', savec(c, 'in4', a))
    if kind == 'cyl_in_cube_S':
        c.rect(70, 40, 160, 160, stroke=INK, sw=2, fill='#eff6ff'); c.path('M70,200 A80,24 0 0 0 230,200', stroke=BLUE, w=2); c.path('M70,200 A80,24 0 0 1 230,200', stroke=BLUE, w=1.6, dash='5,4'); c.ellipse(150, 40, 80, 24, fill='#dbeafe', stroke=BLUE, sw=2)
        c.text(150, 246, f'ребро куба {a}', size=14, anchor='middle', bold=True, col=BLUE)
        return T.add(lv, f'Циліндр вписано в куб з ребром {a} (рисунок). Знайдіть площу повної поверхні циліндра.', pis(F(3 * a * a, 2)),
            [(pis(a * a), 'враховано лише бічну поверхню'), (pis(4 * a * a), 'радіус вважали рівним ребру'), (pis(3 * a * a), 'площі основ обчислено з радіусом a замість a/2')],
            'R = a/2, h = a: Sповна = 2πR(R + h)', f'S = 2π·{fmt(F(a,2))}·({fmt(F(a,2))} + {a})', savec(c, 'in5', a))
    c.rect(70, 40, 160, 160, fill='#eff6ff'); c.circle(150, 120, 80, fill='#dbeafe', stroke=BLUE, sw=2.2); c.text(150, 246, f'ребро куба {a}', size=14, anchor='middle', bold=True, col=BLUE)
    return T.add(lv, f'У куб вписано кулю (рисунок). Знайдіть, у скільки разів об’єм куба більший за об’єм кулі.', f'6/π',
        [('π/6', 'відношення об’ємів перевернуто'), ('3/(4π)', 'радіус кулі взято рівним ребру'), ('8/π', 'не враховано множник 4/3 у формулі кулі')],
        'V куба = a³, V кулі = πa³/6', 'a³ : (πa³/6) = 6/π', savec(c, 'in6', a))

# 15. переливання води
def f_water(T, rng, lv):
    R1, R2 = rng.choice([(6, 3), (4, 2), (10, 5), (9, 3), (8, 4), (6, 2), (12, 4), (10, 2)]); h1 = rng.choice([4, 6, 8, 9, 12, 16, 3, 5]);
    h2 = F(R1 * R1 * h1, R2 * R2)
    c = C(380, 270)
    for cx, R_, lvl, lab, col in ((100, R1 * 7, 0.55, f'R₁ = {R1}', BLUE), (290, R2 * 7, 0.7, f'R₂ = {R2}', BLUE)):
        ry = R_ * 0.3; yb = 200; yt = yb - 130
        wy = yb - 130 * lvl
        c.path(f'M{cx-R_},{wy} L{cx-R_},{yb} A{R_},{ry} 0 0 0 {cx+R_},{yb} L{cx+R_},{wy} A{R_},{ry} 0 0 1 {cx-R_},{wy} Z', fill='#bfdbfe', stroke='none')
        c.ellipse(cx, wy, R_, ry, fill='#93c5fd', stroke='#2563eb', sw=1.2)
        cyl(c, cx, yb, R_, 130, labR=None, labh=None, axis=False, fillc='none')
        c.text(cx, yb + 34, lab, size=14, anchor='middle', bold=True, col=col)
    c.text(100, 258, f'рівень води h₁ = {h1}', size=14, anchor='middle', bold=True, col=BLUE); c.text(290, 258, 'рівень води h₂ = ?', size=14, anchor='middle', bold=True, col=RED)
    return T.add(lv, f'Воду з циліндричної посудини з радіусом основи {R1} і рівнем води {h1} перелили у другу циліндричну посудину з радіусом основи {R2} (рисунок). Яким буде рівень води в другій посудині?', h2,
        [(F(R1 * h1, R2), 'у співвідношенні взято радіуси без квадратів'), (F(R2 * R2 * h1, R1 * R1), 'відношення площ основ перевернуто'), (h1, 'рівень вважали незмінним')],
        'об’єм води не змінюється: R₁²h₁ = R₂²h₂', f'h₂ = {R1}²·{h1}/{R2}² = {fmt(h2)}', savec(c, 'w', R1, R2, h1))

# 16. обертання плоских фігур
def f_rot(T, rng, lv):
    p, q, hy = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (4, 3, 5), (8, 6, 10), (12, 5, 13)])
    c = C(340, 220); kind = rng.choice(['rect', 'tri_leg', 'tri_leg2'] if lv <= 2 else ['tri_leg', 'tri_leg2', 'rect_side'])
    if kind in ('rect', 'rect_side'):
        a, b = rng.choice([(x_, y_) for x_ in range(2, 10) for y_ in range(3, 13) if x_ != y_])
        c.rect(120, 60, 100, 100, fill='#dbeafe', stroke=INK, sw=2); c.line(120, 40, 120, 180, col=RED, w=1.6, dash='6,4')
        c.text(112, 112, str(a), size=15, anchor='end', bold=True, col=BLUE); c.text(170, 180, str(b), size=15, anchor='middle', bold=True, col=BLUE)
        c.text(250, 112, 'вісь обертання — сторона a', size=12, col=RED)
        return T.add(lv, f'Прямокутник зі сторонами {a} і {b} обертається навколо сторони {a} (рисунок). Знайдіть об’єм тіла обертання.', pis(b * b * a),
            [(pis(a * a * b), 'радіус і висоту переплутано'), (pis(F(b * b * a, 3)), 'застосовано формулу конуса'), (pis(2 * b * a), 'знайдено площу бічної поверхні'), (pis(2 * b * (a + b)), 'знайдено площу повної поверхні')],
            'тіло обертання — циліндр з радіусом b і висотою a', f'V = π·{b}²·{a}', savec(c, 'rr', a, b))
    c.poly([(120, 160), (120, 60), (230, 160)], fill='#dbeafe', stroke=INK, w=2); c.line(120, 40, 120, 180, col=RED, w=1.6, dash='6,4')
    S.right_angle(c, (120, 160), (120, 60), (230, 160), 12)
    ax, other = (p, q) if kind == 'tri_leg' else (q, p)
    c.text(112, 112, str(ax), size=15, anchor='end', bold=True, col=BLUE); c.text(175, 180, str(other), size=15, anchor='middle', bold=True, col=BLUE)
    c.text(250, 112, 'вісь — катет ' + str(ax), size=12, col=RED)
    return T.add(lv, f'Прямокутний трикутник із катетами {p} і {q} обертається навколо катета {ax} (рисунок). Знайдіть об’єм тіла обертання.', pis(F(other * other * ax, 3)),
        [(pis(F(ax * ax * other, 3)), 'вісь і радіус переплутано'), (pis(other * other * ax), 'не враховано множник ⅓'), (pis(F(hy * hy * ax, 3)), 'замість радіуса взято гіпотенузу')],
        'тіло обертання — конус: R — другий катет, h — вісь', f'V = ⅓π·{other}²·{ax}', savec(c, 'rt', p, q, ax))

# 17. подібність і масштаб
def f_scale(T, rng, lv):
    k = rng.choice([2, 3, 4, 5]); c = C(280, 190)
    c.rect(30, 90, 60, 60, fill='#dbeafe'); c.rect(130, 150 - 60 * 1.9, 60 * 1.9, 60 * 1.9, fill='#fde68a', stroke=SECS)
    c.text(60, 175, 'a', size=14, anchor='middle', bold=True); c.text(190, 175, f'{k}a', size=14, anchor='middle', bold=True)
    kind = rng.choice(['V', 'S', 'melt'] if lv <= 2 else ['melt', 'V_back', 'S_to_V'])
    if kind == 'V':
        return T.add(lv, f'Ребро одного куба у {raz(k)} більше за ребро другого (рисунок). У скільки разів об’єм першого куба більший за об’єм другого?', k ** 3,
            [(k * k, 'знайдено відношення площ'), (k, 'об’єм вважали пропорційним ребру'), (6 * k, 'враховано кількість граней')], 'об’єми подібних тіл відносяться як куби коефіцієнта подібності', f'{k}³ = {k**3}', savec(c, 'scV', k))
    if kind == 'S':
        return T.add(lv, f'Ребро одного куба у {raz(k)} більше за ребро другого (рисунок). У скільки разів площа поверхні першого куба більша за площу поверхні другого?', k * k,
            [(k ** 3, 'знайдено відношення об’ємів'), (k, 'площу вважали пропорційною ребру'), (6 * k * k, 'враховано кількість граней')], 'площі подібних тіл відносяться як квадрати коефіцієнта подібності', f'{k}² = {k*k}', savec(c, 'scS', k))
    if kind == 'melt':
        a = rng.choice([2, 3, 4]); n_ = rng.choice([8, 27, 64]) ; b = round(n_ ** (1 / 3))
        return T.add(lv, f'Металевий куб із ребром {a * b} переплавили в кубики з ребром {a} (рисунок). Скільки кубиків отримали?', b ** 3,
            [(b, 'враховано лише відношення ребер'), (b * b, 'враховано відношення площ'), (6 * b * b, 'пораховано квадрати на гранях')], 'кількість кубиків = відношення об’ємів = (відношення ребер)³', f'({a*b}/{a})³ = {b}³', savec(c, 'scm', a, b))
    if kind == 'V_back':
        return T.add(lv, f'Об’єм одного куба у {raz(k**3)} більший за об’єм другого (рисунок). У скільки разів ребро першого куба більше за ребро другого?', k,
            [(k * k, 'знайдено відношення площ'), (k ** 3, 'об’єм прийнято за відношення ребер'), (F(k ** 3, 3), 'відношення об’ємів поділено на 3')], 'відношення ребер — кубічний корінь з відношення об’ємів', f'∛{k**3} = {k}', savec(c, 'scb', k))
    return T.add(lv, f'Площа поверхні одного куба у {raz(k*k)} більша за площу поверхні другого (рисунок). У скільки разів об’єм першого куба більший за об’єм другого?', k ** 3,
        [(k * k, 'відношення об’ємів прирівняно до відношення площ'), (k, 'знайдено відношення ребер'), (k ** 4, 'відношення ребер піднесено до четвертого степеня')], 'коефіцієнт подібності = √(відношення площ), V ∝ k³', f'k = √{k*k} = {k}, V ∝ {k}³', savec(c, 'scx', k))

# ---------- логічні твердження ----------
TRUE = [('Через будь-які три точки, що не лежать на одній прямій, проходить єдина площина.', 'аксіома стереометрії'),
        ('Якщо дві різні площини мають спільну точку, то вони перетинаються по прямій.', 'аксіома перетину площин'),
        ('Пряма, перпендикулярна до двох прямих площини, що перетинаються, перпендикулярна до цієї площини.', 'ознака перпендикулярності прямої та площини'),
        ('Через пряму та точку поза нею проходить площина, і до того ж єдина.', 'наслідок з аксіом'),
        ('Через дві прямі, що перетинаються, проходить єдина площина.', 'наслідок з аксіом'),
        ('Діагоналі куба рівні й перетинаються в одній точці.', 'властивість куба'),
        ('Якщо пряма, що не лежить у площині, паралельна якійсь прямій цієї площини, то вона паралельна площині.', 'ознака паралельності прямої та площини'),
        ('Два перпендикуляри до однієї площини паралельні між собою.', 'теорема про перпендикуляри до площини'),
        ('Осьовим перерізом циліндра є прямокутник.', 'властивість циліндра'),
        ('Осьовим перерізом конуса є рівнобедрений трикутник.', 'властивість конуса'),
        ('Будь-який переріз кулі площиною є кругом.', 'властивість кулі'),
        ('Кількість ребер призми, в основі якої n-кутник, дорівнює 3n.', 'формула кількості ребер призми'),
        ('Усі бічні грані правильної піраміди — рівні рівнобедрені трикутники.', 'властивість правильної піраміди'),
        ('Діагональ прямокутного паралелепіпеда виражається через три виміри за формулою d² = a² + b² + c².', 'теорема про діагональ паралелепіпеда')]
FALSE = [('Через дві мимобіжні прямі можна провести площину.', 'мимобіжні прямі не лежать в одній площині'),
         ('Дві прямі, що не мають спільних точок, завжди паралельні.', 'у просторі такі прямі можуть бути мимобіжними'),
         ('Якщо пряма перпендикулярна до однієї прямої площини, то вона перпендикулярна до площини.', 'потрібна перпендикулярність до двох прямих, що перетинаються'),
         ('Через три точки завжди проходить єдина площина.', 'якщо точки лежать на одній прямій, площин безліч'),
         ('Два різні перпендикуляри до однієї прямої завжди паралельні.', 'у просторі вони можуть перетинатися або бути мимобіжними'),
         ('Осьовим перерізом конуса є прямокутник.', 'осьовий переріз конуса — рівнобедрений трикутник'),
         ('Об’єм піраміди дорівнює добутку площі основи на висоту.', 'правильна формула V = ⅓·S·H'),
         ('Діагональ куба з ребром a дорівнює a√2.', 'діагональ куба — a√3, а a√2 — діагональ грані'),
         ('У призми з n-кутною основою 2n граней.', 'граней n + 2, а вершин 2n'),
         ('Якщо дві площини паралельні, то будь-яка пряма однієї паралельна будь-якій прямій другої.', 'прямі можуть бути мимобіжними'),
         ('Площа бічної поверхні циліндра дорівнює πRh.', 'правильна формула 2πRh'),
         ('Об’єм кулі дорівнює 4πR².', '4πR² — площа поверхні; об’єм — ⁴⁄₃πR³'),
         ('Бічна поверхня конуса дорівнює 2πRl.', 'правильна формула πRl'),
         ('Якщо пряма паралельна площині, то вона паралельна всім прямим цієї площини.', 'вона паралельна лише тим, що лежать з нею в одній площині, інші — мимобіжні')]
def f_logic(T, rng, lv):
    neg = rng.random() < 0.5
    if not neg:
        t = rng.choice(TRUE); fs = rng.sample(FALSE, 3)
        return T.add(lv, 'Яке з тверджень є правильним?', t[0], [(f[0], f'хибне: {f[1]}') for f in fs], 'у стереометрії планіметричні твердження можуть бути хибними', f'правильне: {t[1]}')
    f = rng.choice(FALSE); ts = rng.sample(TRUE, 3)
    return T.add(lv, 'Яке з тверджень є хибним?', f[0], [(t[0], f'правильне: {t[1]}') for t in ts], 'шукай твердження, у якому порушено умову', f'хибне: {f[1]}')
def f_euler(T, rng, lv):
    Vn = rng.randint(5, 14); Fn = rng.randint(5, 12); En = Vn + Fn - 2
    kind = rng.choice(['E', 'F', 'V'])
    if kind == 'E':
        return T.add(lv, f'Опуклий многогранник має {Vn} вершин і {Fn} граней. Скільки в нього ребер?', En,
            [(Vn + Fn, 'вершини й грані додано без віднімання 2'), (Vn + Fn + 2, 'до суми вершин і граней додано 2'), (Vn * Fn // 2 if Vn * Fn // 2 != En else Vn * Fn // 2 + 1, 'вершини помножено на грані')],
            'формула Ейлера: B − P + Г = 2', f'P = {Vn} + {Fn} − 2', None)
    if kind == 'F':
        return T.add(lv, f'Опуклий многогранник має {Vn} вершин і {En} ребер. Скільки в нього граней?', Fn,
            [(En - Vn, 'від ребер відняли вершини, забувши додати 2'), (En - Vn - 2, 'у формулі Ейлера знак при 2 взято від’ємним'), (En + Vn, 'ребра й вершини додано')],
            'формула Ейлера: B − P + Г = 2', f'Г = 2 − {Vn} + {En}', None)
    return T.add(lv, f'Опуклий многогранник має {Fn} граней і {En} ребер. Скільки в нього вершин?', Vn,
        [(En - Fn, 'від ребер відняли грані, забувши додати 2'), (En - Fn - 2, 'у формулі Ейлера знак при 2 взято від’ємним'), (En + Fn, 'ребра й грані додано')],
        'формула Ейлера: B − P + Г = 2', f'В = 2 + {En} − {Fn}', None)

FAMS = [(f_box, [1, 2, 3]), (f_cube, [1, 2, 3]), (f_prism, [1, 2, 3]), (f_pyramid, [1, 2, 3]), (f_pyr_angle, [2, 3]), (f_cylinder, [1, 2, 3]), (f_cone, [1, 2, 3]), (f_sphere, [1, 2, 3]),
        (f_net, [1, 2, 3]), (f_count, [1, 2, 3]), (f_paint, [1, 2, 3]), (f_section, [2, 3]), (f_tetra, [2, 3]), (f_boxangle, [2, 3]), (f_inscr, [2, 3]), (f_water, [2, 3]), (f_rot, [2, 3]), (f_scale, [1, 2, 3]),
        (f_logic, [1, 2, 3]), (f_euler, [2, 3])]
