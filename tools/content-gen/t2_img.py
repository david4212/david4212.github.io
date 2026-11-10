import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t2 import *
import msvg as S

def unit_circle_img(name, x, y, lab_x, lab_y):
    c = S.C(380, 330, 'Одиничне коло')
    cx, cy, r = 190, 180, 120
    c.line(cx - r - 28, cy, cx + r + 30, cy, col=S.AX, w=1.6, arrow=True); c.line(cx, cy + r + 24, cx, cy - r - 28, col=S.AX, w=1.6, arrow=True)
    c.text(cx + r + 30, cy + 16, 'x', size=13, italic=True); c.text(cx + 8, cy - r - 22, 'y', size=13, italic=True)
    c.circle(cx, cy, r, fill='#f8fafc', stroke=S.INK, sw=1.8)
    px, py = cx + r * float(x), cy - r * float(y)
    c.line(cx, cy, px, py, col=S.BLUE, w=2.4)
    c.line(px, py, px, cy, col='#9ca3af', w=1.2, dash='4 3'); c.line(px, py, cx, py, col='#9ca3af', w=1.2, dash='4 3')
    th = math.atan2(float(y), float(x)); th = th if th >= 0 else th + 2 * math.pi
    pts = [(cx + 26 * math.cos(-t), cy + 26 * math.sin(-t)) for t in [th * i / 40 for i in range(41)]]
    c.poly(pts, stroke=S.ORANGE, w=2, close=False)
    m = th / 2; c.text(cx + 40 * math.cos(-m) - 6, cy + 40 * math.sin(-m) + 5, 'α', size=15, col=S.ORANGE, bold=True)
    c.dot(px, py, 5, S.RED); c.dot(cx, cy, 3, S.INK)
    dx = 10 if x >= 0 else -10; dy = -10 if y >= 0 else 20
    c.text(px + dx, py + dy, f'P({lab_x}; {lab_y})', size=14, col=S.RED, bold=True, anchor='start' if x >= 0 else 'end')
    c.text(cx + 6, cy + 16, 'O', size=13)
    return c.save(name)

def f_unit_circle(T, rng, lv):
    a, b, c_ = rng.choice(TRIPLES[:5]); 
    sw = rng.random() < .5; X, Y = (F(b, c_), F(a, c_)) if not sw else (F(a, c_), F(b, c_))
    sx, sy = rng.choice([(1, 1), (-1, 1), (-1, -1), (1, -1)]) if lv >= 2 else (1, 1)
    if lv == 3: sx, sy = rng.choice([(-1, 1), (-1, -1), (1, -1), (1, 1)])
    X *= sx; Y *= sy
    img = unit_circle_img('t2_uc_' + S.tag(X, Y), X, Y, ffmt(X), ffmt(Y))
    ask = rng.choice(['sin', 'cos', 'tg', 'sin2', 'cos2', 'ctg']) if lv >= 2 else rng.choice(['sin', 'cos', 'tg'])
    if lv == 3 and ask in ('sin', 'cos'): ask = rng.choice(['sin2', 'cos2', 'tg'])
    vals = {'sin': Y, 'cos': X, 'tg': Y / X, 'ctg': X / Y, 'sin2': 2 * X * Y, 'cos2': X * X - Y * Y}
    names = {'sin': 'sin α', 'cos': 'cos α', 'tg': 'tg α', 'ctg': 'ctg α', 'sin2': 'sin 2α', 'cos2': 'cos 2α'}
    val = vals[ask]
    fmt_ = ffmt
    wr = []
    for k in vals:
        if k != ask and vals[k] != val: wr.append((vals[k], f'це значення {names[k]}, а не {names[ask]}'))
    wr.append((-val, 'знак значення не відповідає координатам точки'))
    if ask == 'tg': wr.append((X / Y, 'відношення координат перевернуто'))
    if ask == 'sin2': wr.append((Y * X, 'не подвоєно добуток координат'))
    if ask == 'cos2': wr.append((1 - 2 * X * X + 2 * Y * Y, 'формула cos 2α записана неправильно'))
    wr = [w for w in wr if w[0] != val]
    sol = {'sin': 'sin α — ордината точки P', 'cos': 'cos α — абсциса точки P', 'tg': 'tg α = sin α / cos α = y / x', 'ctg': 'ctg α = cos α / sin α = x / y',
           'sin2': 'sin 2α = 2 sin α cos α = 2xy', 'cos2': 'cos 2α = cos²α − sin²α = x² − y²'}[ask]
    wr = [(ffmt(w), r) for w, r in wr]
    return T.add(lv, f'Точка P лежить на одиничному колі (див. малюнок), α — кут між додатним напрямом осі x та променем OP. Знайдіть {names[ask]}.', ffmt(val), wr,
                 'на одиничному колі cos α — абсциса, sin α — ордината точки; tg α = y/x; sin 2α = 2xy; cos 2α = x² − y²', f'{sol}: {ffmt(val)}', img=img)

def polygraph_img(name, roots, lead, show_y0=True):
    c = S.C(500, 320, 'Графік многочлена P(x)')
    f = lambda x: lead * (x - roots[0]) * (x - roots[1]) * (x - roots[2])
    vals = [abs(f(-4.6 + 9.2 * i / 100)) for i in range(101)]
    ymax = max(vals); step = 5 if ymax <= 40 else 10 
    top = int(math.ceil(min(ymax, 60) / step) * step) + step
    ax = S.Axes(c, 55, 40, 400, 240, -5, 5, -top, top, 1, step, xlab='x', ylab='y', size=11, ylab_every=1 if top <= 30 else 2)
    ax.curve(f, -4.7, 4.7, col=S.BLUE, w=2.8, steps=300)
    for r in roots: ax.point(r, 0, None, col=S.RED, r=4.5)
    if show_y0:
        y0 = f(0); ax.point(0, y0, f'(0; {S.dec(y0, 0)})', col=S.GREEN, dx=8, dy=-6, r=4.5, size=12)
    return c.save(name)

def sgnfac(r): return f'(x {"−" if r > 0 else "+"} {abs(r)})'
def f_polygraph(T, rng, lv):
    for _ in range(100):
        roots = sorted(rng.sample(range(-4, 5), 3)); 
        if len({abs(r) for r in roots}) < 3 or min(abs(roots[1] - roots[0]), abs(roots[2] - roots[1])) < 1: continue
        if roots[0] * roots[1] * roots[2] == 0 and rng.random() < .5: continue
        lead = rng.choice([1, -1]); 
        f = lambda x: lead * (x - roots[0]) * (x - roots[1]) * (x - roots[2])
        if max(abs(f(x)) for x in range(-5, 6)) <= 60: break
    else: return False
    kind = rng.choice(['formula', 'formula', 'negcount']) if lv == 3 else 'formula'
    img = polygraph_img('t2_pg_' + S.tag(roots, lead, kind), roots, lead, show_y0=(kind == 'formula' and (roots[0] * roots[1] * roots[2] != 0)))
    pre = '' if lead == 1 else MINUS
    mk = lambda rs, ld: ('' if ld == 1 else MINUS) + ''.join(sgnfac(r) for r in rs)
    if kind == 'formula':
        ans = mk(roots, lead)
        wr = [(mk([-r for r in roots], lead), 'знаки коренів змінено: корінь x = r дає множник (x − r)'), (mk(roots, -lead), 'знак старшого коефіцієнта не відповідає поведінці графіка при x → +∞')]
        for i in range(3):
            alt = list(roots); alt[i] = -alt[i]
            if alt[i] not in roots[:i] + roots[i + 1:] and alt != roots: wr.append((mk(sorted(alt), lead), f'неправильний знак у корені {roots[i]}'))
        alt2 = [r + 1 for r in roots]; wr.append((mk(alt2, lead), 'корені зсунуто на 1: за графіком вони перетинають вісь x в інших точках'))
        return T.add(lv, 'На малюнку зображено графік многочлена третього степеня P(x) з трьома цілими коренями. Який із поданих виразів задає цей многочлен?', 'P(x) = ' + ans, [('P(x) = ' + w, r) for w, r in wr],
                     'корінь многочлена — точка перетину графіка з віссю x: корінь r дає множник (x − r); знак старшого коефіцієнта — за поведінкою на нескінченності', f'корені {", ".join(map(str, roots))}; при x → +∞ графік іде {"вгору" if lead == 1 else "вниз"}, тому старший коефіцієнт {"+" if lead == 1 else "−"}1', img=img)
    xs = list(range(-5, 6)); neg = [x for x in xs if f(x) < 0]; neg0 = [x for x in xs if f(x) <= 0]; pos = [x for x in xs if f(x) > 0]
    cnt = len(neg)
    wr = [(len(neg0), 'враховано й корені, але нерівність строга'), (len(pos), 'пораховано точки, де многочлен додатний'), (cnt + 1, 'зайве ціле число враховано'), (cnt - 1, 'одне ціле значення пропущено')]
    return T.add(lv, 'За графіком многочлена P(x) визначте, скільки цілих значень x із відрізка [−5; 5] задовольняють нерівність P(x) < 0.', cnt, wr,
                 'розв’язок P(x) < 0 — це проміжки, де графік лежить нижче осі x; корені не входять', f'корені {", ".join(map(str, roots))}; цілі x з P(x) < 0: {", ".join(map(str, neg))} — їх {cnt}', img=img)

DOM = {'ge': ('x ≥ a', 'y = √(x − a)'), 'gt': ('x > a', 'y = log₂(x − a)'), 'le': ('x ≤ a', 'y = √(a − x)'), 'lt': ('x < a', 'y = log₂(a − x)'), 'ne': ('x ≠ a', 'y = 1/(x − a)'), 'seg': ('−a ≤ x ≤ a', 'y = √(a² − x²)'), 'ne2': ('x ≠ ±a', 'y = 1/(x² − a²)')}
def domain_img(name, kind, a):
    c = S.C(520, 120, 'Область визначення функції')
    x0, x1, y = 30, 490, 70; lo, hi = -7, 7
    px = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo)
    c.line(x0 - 10, y, x1 + 14, y, col=S.AX, w=1.8, arrow=True)
    for t in range(lo, hi + 1):
        X = px(t); c.line(X, y - 5, X, y + 5, col=S.AX, w=1.2)
        if t % 1 == 0 and (t % 1 == 0): c.text(X, y + 22, S.dec(t, 0), size=11, anchor='middle', col=S.GRAY)
    def seg(l, r, col=S.BLUE): c.line(px(l), y, px(r), y, col=col, w=6)
    def dotp(v, filled): c.circle(px(v), y, 5.5, fill=(S.BLUE if filled else '#fff'), stroke=S.BLUE, sw=2.2)
    if kind == 'ge': seg(a, hi + .3); dotp(a, True)
    elif kind == 'gt': seg(a, hi + .3); dotp(a, False)
    elif kind == 'le': seg(lo - .3, a); dotp(a, True)
    elif kind == 'lt': seg(lo - .3, a); dotp(a, False)
    elif kind == 'ne': seg(lo - .3, hi + .3); dotp(a, False)
    elif kind == 'seg': seg(-a, a); dotp(-a, True); dotp(a, True)
    elif kind == 'ne2': seg(lo - .3, hi + .3); dotp(-a, False); dotp(a, False)
    return c.save(name)

def f_domain_line(T, rng, lv):
    a = rng.randint(1, 5)
    kinds = list(DOM); kind = rng.choice(kinds)
    if kind in ('seg', 'ne2') and a < 1: return False
    img = domain_img('t2_dm_' + S.tag(kind, a), kind, a)
    fill = lambda s: s.replace('a²', str(a * a)).replace('±a', f'±{a}').replace('−a', f'−{a}').replace(' a', f' {a}').replace('(a', f'({a}').replace('a)', f'{a})').replace('= a', f'= {a}')
    def fill2(s):
        s = s.replace('a²', str(a * a))
        s = s.replace('−a', f'−{a}').replace('±a', f'±{a}')
        s = s.replace('x − a', f'x − {a}').replace('a − x', f'{a} − x').replace('≥ a', f'≥ {a}').replace('> a', f'> {a}').replace('≤ a', f'≤ {a}').replace('< a', f'< {a}').replace('≠ a', f'≠ {a}')
        return s
    ans = fill2(DOM[kind][1])
    others = [k for k in kinds if k != kind]
    wr = [(fill2(DOM[k][1]), f'область визначення цієї функції — {fill2(DOM[k][0])}') for k in rng.sample(others, 5)]
    ret = T.add(lv, 'На числовій прямій зображено область визначення деякої функції (порожні кружки — виколоті точки). Яка з поданих функцій має саме таку область визначення?', ans, wr,
                'корінь парного степеня — підкореневий вираз ≥ 0; логарифм — аргумент > 0; дріб — знаменник ≠ 0', f'множина {fill2(DOM[kind][0])} збігається з областю визначення {ans}', img=img)
    return ret

def squares_img(name, a, b, labA, labB, labR, labS):
    c = S.C(360, 300, 'Квадрат зі стороною a + b')
    u = 150 / (a + b); x0, y0 = 40, 50
    A, B = a * u, b * u
    c.rect(x0, y0, A, A, fill='#dbeafe', stroke=S.INK); c.rect(x0 + A, y0, B, A, fill='#dcfce7', stroke=S.INK)
    c.rect(x0, y0 + A, A, B, fill='#dcfce7', stroke=S.INK); c.rect(x0 + A, y0 + A, B, B, fill='#ffedd5', stroke=S.INK)
    c.text(x0 + A / 2, y0 + A / 2 + 5, labA, size=14, anchor='middle', bold=True); c.text(x0 + A + B / 2, y0 + A / 2 + 5, labR, size=14, anchor='middle', bold=True)
    c.text(x0 + A / 2, y0 + A + B / 2 + 5, labR, size=14, anchor='middle', bold=True); c.text(x0 + A + B / 2, y0 + A + B / 2 + 5, labB, size=14, anchor='middle', bold=True)
    c.text(x0 + A / 2, y0 - 8, 'a', size=15, anchor='middle', italic=True, col=S.BLUE); c.text(x0 + A + B / 2, y0 - 8, 'b', size=15, anchor='middle', italic=True, col=S.ORANGE)
    c.text(x0 - 10, y0 + A / 2 + 5, 'a', size=15, anchor='end', italic=True, col=S.BLUE); c.text(x0 - 10, y0 + A + B / 2 + 5, 'b', size=15, anchor='end', italic=True, col=S.ORANGE)
    c.text(x0 + (A + B) / 2, y0 + A + B + 30, labS, size=14, anchor='middle', bold=True, col=S.RED)
    return c.save(name)

def f_squares(T, rng, lv):
    a, b = rng.sample(range(2, 9), 2)
    kind = rng.choice(['sumsq', 'big'])
    if kind == 'sumsq':
        S_, p = (a + b) ** 2, a * b
        img = squares_img('t2_sq_' + S.tag(a, b, kind), max(a, b), min(a, b), 'a²', 'b²', f'ab = {p}', f'Площа всього квадрата = {S_}')
        ans = S_ - 2 * p
        wr = [(S_ - p, 'площу лише одного прямокутника віднято від загальної'), (S_ + 2 * p, 'площі прямокутників додано, а не віднято'), (S_, 'площу прямокутників не віднято'), (S_ - 4 * p, 'віднято чотири площі прямокутників замість двох')]
        return T.add(lv, f'Квадрат зі стороною a + b розрізано на два квадрати та два однакові прямокутники (див. малюнок). Площа великого квадрата дорівнює {S_}, а площа кожного прямокутника — {p}. Знайдіть a² + b².', ans, wr,
                     '(a + b)² = a² + 2ab + b²: площа великого квадрата — це сума площ двох квадратів і двох прямокутників', f'{S_} − 2·{p} = {ans}', img=img)
    A_, B_ = a * a, b * b; p = a * b
    img = squares_img('t2_sq_' + S.tag(a, b, kind), max(a, b), min(a, b), f'{max(A_, B_)}', f'{min(A_, B_)}', 'ab', 'Площа всього квадрата = ?')
    S_ = (a + b) ** 2
    wr = [(A_ + B_, 'площі лише двох квадратів додано'), (2 * (A_ + B_), 'площі двох квадратів подвоєно'), (A_ + B_ + p, 'враховано лише один прямокутник'), (A_ * B_, 'площі перемножено')]
    return T.add(lv, f'Квадрат розрізано на два квадрати з площами {max(A_, B_)} і {min(A_, B_)} та два однакові прямокутники (див. малюнок). Яка площа всього квадрата?', S_, wr,
                 'сторони малих квадратів — √площі; велика сторона = їх сума; площа = (сума)²', f'сторони {max(a,b)} і {min(a,b)}; ({max(a,b)} + {min(a,b)})² = {S_}', img=img)

def triangle_img(name, a, b, c_, lab_a, lab_b, lab_c, angle='A'):
    cvs = S.C(380, 290, 'Прямокутний трикутник ABC (∠C = 90°)')
    sc = 180 / max(a, b)
    C = (60, 245); A = (60 + b * sc, 245); B = (60, 245 - a * sc)
    cvs.poly([C, A, B], fill='#f0f9ff', stroke=S.INK, w=2)
    S.right_angle(cvs, C, A, B, s=13)
    S.poly_label(cvs, [C, A, B], ['C', 'A', 'B'], off=15, centre=((C[0] + A[0] + B[0]) / 3, (C[1] + A[1] + B[1]) / 3))
    cen = ((C[0] + A[0] + B[0]) / 3, (C[1] + A[1] + B[1]) / 3)
    S.side_label(cvs, B, C, lab_a, cen, off=18, col=S.BLUE); S.side_label(cvs, C, A, lab_b, cen, off=16, col=S.BLUE); S.side_label(cvs, A, B, lab_c, cen, off=16, col=S.BLUE)
    if angle == 'A': S.angle_arc(cvs, A, C, B, r=30, col=S.ORANGE)
    else: S.angle_arc(cvs, B, A, C, r=30, col=S.ORANGE)
    return cvs.save(name)

def f_right_triangle(T, rng, lv):
    a0, b0, c0 = rng.choice(TRIPLES[:5]); k = rng.choice([1, 1, 2, 3]) if c0 < 20 else 1
    a, b, c_ = a0 * k, b0 * k, c0 * k
    if rng.random() < .5: a, b = b, a
    angle = rng.choice(['A', 'B']); fn = rng.choice(['sin', 'cos', 'tg'])
    hide = rng.choice(['none', 'c', 'a', 'b']) if lv >= 2 else 'none'
    la, lb, lc = str(a), str(b), str(c_)
    if hide == 'c': lc = '?'
    elif hide == 'a': la = '?'
    elif hide == 'b': lb = '?'
    img = triangle_img('t2_tr_' + S.tag(a, b, c_, hide, angle), a, b, c_, la, lb, lc, angle)
    opp, adj = (a, b) if angle == 'A' else (b, a)
    val = {'sin': F(opp, c_), 'cos': F(adj, c_), 'tg': F(opp, adj)}[fn]
    wr = []
    other = {'sin': F(adj, c_), 'cos': F(opp, c_), 'tg': F(adj, opp)}
    wr.append((other[fn], 'катети або сторони переплутано (це функція кута з іншої вершини)'))
    if fn != 'tg': wr.append((F(opp, adj) if fn == 'sin' else F(adj, opp), 'катет поділено на катет — це тангенс чи котангенс'))
    else: wr.append((F(opp, c_), 'катет поділено на гіпотенузу — це синус'))
    wr.append((F(c_, adj if fn == 'cos' else opp), 'відношення перевернуто'))
    wr.append((F(opp + adj, c_) if fn != 'tg' else F(opp * adj, c_), 'сторони додано/перемножено замість ділення'))
    wr = [(ffmt(w[0]), w[1]) for w in wr if w[0] != val]
    vertex = angle
    nm = {'sin': 'sin', 'cos': 'cos', 'tg': 'tg'}[fn]
    pre = {'none': '', 'c': 'гіпотенузу знайдіть за теоремою Піфагора', 'a': 'катет a знайдіть за теоремою Піфагора', 'b': 'катет b знайдіть за теоремою Піфагора'}[hide]
    return T.add(lv, f'У прямокутному трикутнику ABC (∠C = 90°) сторони подано на малюнку (знаком «?» позначено невідому сторону). Знайдіть {nm} ∠{vertex}.', ffmt(val), wr,
                 'sin — протилежний катет / гіпотенуза; cos — прилеглий катет / гіпотенуза; tg — протилежний / прилеглий' + ('; невідому сторону шукайте за теоремою Піфагора' if hide != 'none' else ''),
                 f'BC = {a}, AC = {b}, AB = {c_}; для ∠{vertex}: протилежний катет {opp}, прилеглий {adj}; {nm} {vertex} = {ffmt(val)}', img=img)

FAMS += [(f_unit_circle, [1, 2, 3]), (f_polygraph, [2, 3]), (f_domain_line, [1, 2]), (f_squares, [2]), (f_right_triangle, [1, 2])]
IMGF = FAMS[-5:]
FAMS += IMGF + IMGF
