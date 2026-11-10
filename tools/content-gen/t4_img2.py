import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t4_img import *

# ================= малюнкові родини теми 4 (частина B) =================
def bs_(a): return fmt(a) if F(a).denominator == 1 else f'({ffmt(a)})'
def tail(b): return f' {"+" if b > 0 else M} {fmt(abs(b))}' if b else ''
def exp_s(a, b): return f'y = {bs_(a)}ˣ' + tail(b)
def exps_s(a, m): return f'y = {bs_(a)}ˣ' + ('⁻' if m > 0 else '⁺') + sup(abs(m))   # y = a^(x − m)
LB = {F(2): 'log₂', F(3): 'log₃', F(1, 2): 'log₀,₅', F(1, 3): 'log₁/₃'}
def log_s(a, c, d): return f'y = {LB[F(a)]}' + (' x' if c == 0 else f'(x {M if c > 0 else "+"} {abs(c)})') + tail(d)

# ---------- I14: показникова функція ----------
def f_img_exp(T, rng, lv):
    a = F(rng.choice([2, 2, 3, F(1, 2)])); b = rng.choice([v for v in range(-4, 4) if v]); inc = a > 1
    xb = 1 if inc else -1; yb = (a if inc else 1 / a) + b; g = a if inc else 1 / a
    view = (-5, 5, min(b - 1, -1), max(b + 8, 1))
    c, ax = G(*view, 'Графік показникової функції')
    ax.seg(-5, b, 5, b, col=S.GREEN, w=1.8, dash='7 5')
    ax.curve(lambda t: float(a) ** t + b, -5, 5, steps=500, w=2.8)
    ax.point(0, 1 + b, 'A', dx=-18 if inc else 8, dy=-6); ax.point(xb, yb, 'B', dx=9 if inc else -20, dy=5)
    img = c.save('t4_ex_' + S.tag(a, b))
    intro = 'На малюнку зображено графік функції y = aˣ + b та його горизонтальну асимптоту (пунктир); позначено точки A і B графіка. '
    chk = f'асимптота y = {fmt(b)} ⇒ b = {fmt(b)}; точка B({xb}; {fmt(yb)}): a^{pn(xb)} {"+" if b > 0 else M} {abs(b)} = {fmt(yb)} ⇒ a = {ffmt(a)}'
    kind = rng.choice(['asym', 'range'] if lv == 1 else ['formula', 'val'])
    if kind == 'asym':
        wr = [(f'x = {fmt(b)}', 'асимптота горизонтальна, тому її рівняння має вигляд y = c'), (f'y = {fmt(1 + b)}', 'названо ординату точки A, у якій графік перетинає вісь y'), ('y = 0', 'це асимптота графіка y = aˣ без зсуву вздовж осі y'), (f'y = {fmt(-b)}', 'знак змінено')]
        return T.add(lv, intro + 'Укажіть рівняння асимптоти.', f'y = {fmt(b)}', wr, 'горизонтальна пряма, що проходить через точку (0; c), має рівняння y = c', f'пунктирна пряма проходить на рівні {fmt(b)} по осі y', img=img)
    if kind == 'range':
        wr = [(I(b, None), f'значення {fmt(b)} не досягається: графік лише наближається до асимптоти'), (I(None, b, False, False), 'графік лежить вище від асимптоти, а не нижче'), ('(0; +∞)', 'це множина значень функції y = aˣ без зсуву'), (I(1 + b, None, False), 'узято ординату точки A'), ('(−∞; +∞)', 'це область визначення, а не множина значень')]
        return T.add(lv, intro + 'Укажіть множину значень цієї функції.', I(b, None, False), wr, 'aˣ > 0 при всіх x, тому aˣ + b > b: графік лежить вище від асимптоти й не торкається її', f'асимптота y = {fmt(b)}, графік — вище від неї: E(f) = {I(b, None, False)}', img=img)
    if kind == 'formula':
        oth = {F(2): F(3), F(3): F(2), F(1, 2): F(1, 3)}[a]
        wr = [(exp_s(a, -b), f'знак зсуву неправильний: асимптота y = {fmt(b)}, тому b = {fmt(b)}'), (exp_s(1 / a, b), f'функція {"зростає" if inc else "спадає"}, тому основа {"більша за 1" if inc else "менша від 1"}'),
              (exps_s(a, b), 'зсув виконано вздовж осі x замість осі y: асимптотою залишилася б пряма y = 0'), (exp_s(oth, b), f'при x = {xb} значення було б {fmt((oth if inc else 1 / oth) + b)}, а в точці B воно дорівнює {fmt(yb)}')]
        return T.add(lv, 'На малюнку зображено графік функції виду y = aˣ + b та його горизонтальну асимптоту (пунктир); позначено точки A і B графіка. Укажіть формулу цієї функції.', exp_s(a, b), wr,
                     'b визначають за асимптотою y = b, основу a — за точкою з абсцисою 1 (або −1)', chk, img=img)
    k = rng.choice([4, 5, 6] if g == 2 else [3, 4]); x0 = k if inc else -k; p = g ** k; ans = p + b
    wr = [(p, 'не додано b'), (p - b, 'знак b змінено'), (g ** (k - 1) + b, 'показник степеня взято на 1 менший'), (g * k + b, 'степінь замінено множенням основи на показник'), (1 / p + b if False else F(k) + b, 'основу не враховано: до показника додано b')]
    return T.add(lv, intro + f'Знайдіть значення цієї функції при x = {fmt(x0)}.', ans, wr, 'точки з такою абсцисою на малюнку немає: спочатку знайдіть a і b', chk + f'; f({fmt(x0)}) = {bs_(a)}^{pn(x0)} {"+" if b > 0 else M} {abs(b)} = {fmt(p)} {"+" if b > 0 else M} {abs(b)} = {fmt(ans)}', img=img)

# ---------- I15: логарифмічна функція ----------
def f_img_log(T, rng, lv):
    a = F(rng.choice([2, 2, 3, F(1, 2)])); cc = rng.choice([-3, -2, -1, 1, 2, 3]); inc = a > 1
    kind = rng.choice(['domain', 'asym', 'formula'] if lv == 2 else ['formula', 'val', 'val'])
    d = 0 if lv == 2 else rng.choice([v for v in (-2, -1, 1, 2) if v != cc])
    g = a if inc else 1 / a; xb = cc + g; yb = d + (1 if inc else -1)
    view = (min(cc - 1, -1), max(cc + 9, 1), min(d - 4, -1), max(d + 4, 1))
    c, ax = G(*view, 'Графік логарифмічної функції')
    ax.seg(cc, view[2], cc, view[3], col=S.GREEN, w=1.8, dash='7 5')
    ax.curve(lambda t: math.log(t - cc) / math.log(float(a)) + d, cc + 1e-4, view[1], steps=900, w=2.8)
    ax.point(cc + 1, d, 'A', dx=8, dy=16 if inc else -8); ax.point(xb, yb, 'B', dx=-4, dy=-10 if inc else 20)
    img = c.save('t4_lg_' + S.tag(a, cc, d))
    intro = 'На малюнку зображено графік функції ' + ('y = log_a(x − c)' if d == 0 else 'y = log_a(x − c) + d') + ' та його вертикальну асимптоту (пунктир); позначено точки A і B графіка. '
    chk = f'асимптота x = {fmt(cc)} ⇒ c = {fmt(cc)}; точка A({fmt(cc + 1)}; {fmt(d)}): log_a 1 = 0' + (f' ⇒ d = {fmt(d)}' if d else '') + f'; точка B({fmt(xb)}; {fmt(yb)}): log_a {fmt(g)} = {1 if inc else M + "1"} ⇒ a = {ffmt(a)}'
    if kind == 'domain':
        wr = [(I(cc, None), f'при x = {fmt(cc)} функція не визначена (аргумент логарифма має бути додатним), тому дужка кругла'), (I(-cc, None, False), 'знак змінено'), (I(None, cc, False, False), 'графік розташований праворуч від асимптоти, а не ліворуч'), ('(0; +∞)', 'це область визначення y = log_a x без зсуву'), (I(cc + 1, None, False), 'узято абсцису точки A (нуль функції), а не асимптоту')]
        return T.add(lv, intro + 'Укажіть область визначення цієї функції.', I(cc, None, False), wr, 'область визначення — проєкція графіка на вісь x; графік наближається до асимптоти, але не перетинає її', f'графік розташований праворуч від прямої x = {fmt(cc)}: D(f) = {I(cc, None, False)}', img=img)
    if kind == 'asym':
        wr = [(f'y = {fmt(cc)}', 'асимптота вертикальна, тому її рівняння має вигляд x = c'), (f'x = {fmt(-cc)}', 'знак змінено'), ('x = 0', 'це асимптота графіка y = log_a x без зсуву'), (f'x = {fmt(cc + 1)}', 'названо абсцису точки A — нуля функції')]
        return T.add(lv, intro + 'Укажіть рівняння асимптоти.', f'x = {fmt(cc)}', wr, 'вертикальна пряма, що проходить через точку (c; 0), має рівняння x = c', f'пунктирна пряма перетинає вісь x у точці {fmt(cc)}', img=img)
    if kind == 'formula':
        oth = {F(2): F(3), F(3): F(2), F(1, 2): F(1, 3)}[a]
        wr = [(log_s(a, -cc, d), f'знак зсуву неправильний: асимптота x = {fmt(cc)}, тому під логарифмом x {M if cc > 0 else "+"} {abs(cc)}'), (log_s(1 / a, cc, d), f'функція {"зростає" if inc else "спадає"}, тому основа {"більша за 1" if inc else "менша від 1"}')]
        if d == 0: wr += [(log_s(a, 0, -cc), 'зсув виконано вздовж осі y замість осі x: асимптотою залишилася б вісь y'), (log_s(oth, cc, d), f'за точкою B: log_a {fmt(g)} = {1 if inc else M + "1"}, тому a = {ffmt(a)}')]
        else: wr += [(log_s(a, cc, -d), f'знак вертикального зсуву неправильний: f({fmt(cc + 1)}) = {fmt(d)}'), (log_s(a, d, cc), 'зсуви вздовж осей x та y переставлено місцями'), (log_s(a, cc, 0), f'не враховано вертикальний зсув: f({fmt(cc + 1)}) = {fmt(d)}, а не 0')]
        return T.add(lv, 'На малюнку зображено графік однієї з наведених функцій та його вертикальну асимптоту (пунктир); позначено точки A і B графіка. Укажіть цю функцію.', log_s(a, cc, d), wr,
                     'c визначають за асимптотою x = c; у точці з абсцисою c + 1 логарифм дорівнює 0; основу знаходять за ще однією точкою', chk, img=img)
    k = rng.choice([4, 5, 6] if g == 2 else [3, 4]); N = cc + g ** k; s = 1 if inc else -1; ans = s * k + d
    wr = [(s * k, 'не додано d'), (s * k - d, 'знак d змінено'), (-s * k + d, f'знак логарифма неправильний: основа {"більша за 1" if inc else "менша від 1"}'), (s * (k + 1) + d, 'показник степеня визначено з помилкою на 1'), (F(N), 'названо аргумент, а не значення функції')]
    return T.add(lv, intro + f'Знайдіть значення цієї функції при x = {fmt(N)}.', ans, wr, 'точки з такою абсцисою на малюнку немає: спочатку знайдіть a, c і d',
                 chk + f'; f({fmt(N)}) = {LB[a]} {fmt(g ** k)} {"+" if d > 0 else M} {abs(d)} = {fmt(s * k)} {"+" if d > 0 else M} {abs(d)} = {fmt(ans)}', img=img)

# ---------- I16: тригонометричні функції ----------
def trig_s(fn, A, k, d):
    As = {1: '', -1: M}.get(A, fmt(A)); arg = {F(1): ' x', F(2): ' 2x', F(1, 2): '(x/2)'}[F(k)]
    return f'y = {As}{fn}{arg}' + tail(d)
def halo(c, x, y, s_, size=11, col=S.GRAY, anchor='middle'):
    c.e.append(f'<text x="{S.n(x)}" y="{S.n(y)}" {S.FONT} font-size="{size}" fill="{col}" text-anchor="{anchor}" stroke="#ffffff" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round">{S.esc(s_)}</text>')
def trig_axes(title, xr, tick, ymin, ymax):
    """вісь x у частках π: від −xr·π до xr·π з кроком tick·π; повертає (c, ax, fin) — fin() малює підписи поверх кривої"""
    W = 600; w = 500; x0 = 50; h = min(46, 300 / (ymax - ymin)) * (ymax - ymin); y0 = 46
    c = S.C(W, int(h + y0 + 34), title)
    ax = S.Axes(c, x0, y0, w, h, -float(xr) * math.pi, float(xr) * math.pi, ymin, ymax, float(tick) * math.pi, 1, labels=False)
    nt = int(xr / tick)
    def fin():
        for j in range(-nt, nt + 1):
            if j == 0: continue
            X = ax.X(float(j * tick) * math.pi); c.line(X, ax.Y(0) - 3, X, ax.Y(0) + 3, col=S.AX, w=1.2)
            halo(c, X, ax.Y(0) + 17, pim(j * tick))
        for v in range(ymin, ymax + 1):
            if v == 0: continue
            c.line(ax.X(0) - 3, ax.Y(v), ax.X(0) + 3, ax.Y(v), col=S.AX, w=1.2); halo(c, ax.X(0) - 7, ax.Y(v) + 4, fmt(v), anchor='end')
        halo(c, ax.X(0) - 7, ax.Y(0) + 15, '0', anchor='end')
    return c, ax, fin
def f_img_trig(T, rng, lv):
    fn = rng.choice(['sin', 'cos']); k = F(rng.choice([1, 1, 2, F(1, 2)])); d = rng.choice([-1, 0, 0, 1, 2])
    A = rng.choice([1, 2, 3]) if lv < 3 else rng.choice([1, 2, 3, -1, -2])
    kind = rng.choice(['max', 'min', 'range'] if lv == 1 else (['period', 'period', 'A', 'd'] if lv == 2 else ['formula']))
    if kind in ('A', 'd') and d == 0: d = rng.choice([-1, 1, 2])
    if kind == 'period' and k == 1: k = F(rng.choice([2, F(1, 2)]))
    tf = {'sin': math.sin, 'cos': math.cos}
    f = lambda t, fn=fn, A=A, k=k, d=d: A * tf[fn](float(k) * t) + d
    xr, tick = {F(1): (2, F(1, 2)), F(2): (1, F(1, 4)), F(1, 2): (4, F(1))}[k]
    hi, lo = d + abs(A), d - abs(A)
    c, ax, fin = trig_axes('Графік функції y = f(x)', xr, tick, min(lo - 1, -1), max(hi + 1, 1))
    ax.curve(f, steps=600, w=2.8); fin()
    img = c.save('t4_tr_' + S.tag(fn, A, k, d))
    Tp = 2 / k   # період у частках π
    if kind in ('max', 'min'):
        big = kind == 'max'; ans = hi if big else lo
        wr = [(lo if big else hi, f'названо {"найменше" if big else "найбільше"} значення'), (F(abs(A)), 'названо амплітуду — половину розмаху коливань'), (F(d), 'названо рівень середньої лінії графіка'), (F(1) if big else F(-1), f'названо {"найбільше" if big else "найменше"} значення функції y = {fn} x без перетворень'), (F(hi - lo), 'названо розмах — різницю найбільшого й найменшого значень')]
        return T.add(lv, f'На малюнку зображено графік функції y = f(x), визначеної на всій числовій прямій. Знайдіть {"найбільше" if big else "найменше"} значення цієї функції.', ans, wr,
                     'найбільше й найменше значення читають на осі y: це рівні «гребенів» і «западин» графіка', f'{"гребені" if big else "западини"} графіка лежать на рівні y = {fmt(ans)}', img=img)
    if kind == 'range':
        ans = I(lo, hi)
        wr = [(I(-abs(A), abs(A)), 'не враховано зсув графіка вздовж осі y'), ('[−1; 1]', f'це множина значень функції y = {fn} x без перетворень'), (I(lo, hi, False, False), 'найбільше й найменше значення досягаються, тому дужки квадратні'), ('(−∞; +∞)', 'це область визначення, а не множина значень'), (I(-hi, -lo), 'знаки кінців проміжку змінено'), (I(0, hi) if lo < 0 else I(lo - 1, hi), 'нижню межу прочитано неправильно')]
        return T.add(lv, 'На малюнку зображено графік функції y = f(x), визначеної на всій числовій прямій. Укажіть множину значень цієї функції.', ans, wr,
                     'множина значень — проміжок на осі y від найнижчих точок графіка до найвищих', f'найменше значення {fmt(lo)}, найбільше {fmt(hi)}: E(f) = {ans}', img=img)
    if kind == 'period':
        ans = pim(Tp)
        wr = [(pim(Tp / 2), 'узято відстань між сусідніми найвищою та найнижчою точками — це половина періоду'), (pim(Tp * 2), 'узято відстань, що вміщує два повні коливання'), (pim(Tp / 4), 'узято відстань від точки на середній лінії до найближчого екстремуму — чверть періоду'), ('2π', f'це період функції y = {fn} x; тут графік {"стиснуто" if k > 1 else "розтягнуто"} вздовж осі x')]
        pk = [j * Tp + (Tp / 4 if fn == 'sin' else 0) for j in (0, 1)]
        return T.add(lv, 'На малюнку зображено графік періодичної функції y = f(x). Укажіть її найменший додатний період.', ans, wr,
                     'період — відстань уздовж осі x між сусідніми найвищими точками графіка (або довжина одного повного коливання)', f'сусідні найвищі точки мають абсциси {pim(pk[0])} та {pim(pk[1])}; T = {ans}', img=img)
    form = f'y = A {fn} kx + d (A > 0)'
    if kind == 'A':
        wr = [(F(hi), 'названо найбільше значення функції'), (F(hi - lo), 'названо розмах; амплітуда — його половина'), (F(d), 'названо d — рівень середньої лінії'), (F(lo), 'названо найменше значення функції'), (F(abs(A)) + 1, 'амплітуду прочитано неточно')]
        return T.add(lv, f'На малюнку зображено графік функції {form}. Знайдіть A.', F(A), wr, 'A = (y_max − y_min)/2 — половина різниці найбільшого й найменшого значень', f'y_max = {fmt(hi)}, y_min = {fmt(lo)}; A = ({fmt(hi)} − {pn(lo)})/2 = {fmt(A)}', img=img)
    if kind == 'd':
        wr = [(F(A), 'названо амплітуду A'), (F(hi), 'названо найбільше значення функції'), (F(lo), 'названо найменше значення функції'), (F(-d), 'знак змінено'), (F(hi - lo), 'названо розмах коливань')]
        return T.add(lv, f'На малюнку зображено графік функції {form}. Знайдіть d.', F(d), wr, 'd = (y_max + y_min)/2 — рівень середньої лінії, навколо якої коливається графік', f'y_max = {fmt(hi)}, y_min = {fmt(lo)}; d = ({fmt(hi)} + {pn(lo)})/2 = {fmt(d)}', img=img)
    ofn = 'cos' if fn == 'sin' else 'sin'; k2 = 1 / k if k != 1 else F(2)
    cands = [(trig_s(ofn, A, k, d), lambda t: A * tf[ofn](float(k) * t) + d, f'f(0) = {fmt(F(round(f(0))))}: для синуса було б {fmt(d)}, для косинуса {fmt(A + d)}'),
             (trig_s(fn, -A, k, d), lambda t: -A * tf[fn](float(k) * t) + d, f'знак коефіцієнта перед {fn} неправильний: графік було б відображено відносно середньої лінії'),
             (trig_s(fn, A, k2, d), lambda t: A * tf[fn](float(k2) * t) + d, f'період графіка дорівнює {pim(Tp)}, тому k = 2π/T = {ffmt(k)}')]
    if d != 0 and d != A: cands.append((trig_s(fn, d, k, A), lambda t: d * tf[fn](float(k) * t) + A, 'амплітуду й вертикальний зсув переставлено місцями'))
    if d != 0: cands.append((trig_s(fn, A, k, -d), lambda t: A * tf[fn](float(k) * t) - d, f'знак вертикального зсуву неправильний: середня лінія y = {fmt(d)}'))
    if abs(A) != 1: cands.append((trig_s(fn, A // abs(A), k, d), lambda t: (A // abs(A)) * tf[fn](float(k) * t) + d, f'амплітуда дорівнює {abs(A)}, а не 1'))
    smp = [i * .37 - 6 for i in range(34)]
    wr = [(s_, r_) for s_, g_, r_ in cands if any(abs(g_(t) - f(t)) > 1e-6 for t in smp)]
    return T.add(lv, 'На малюнку зображено графік однієї з наведених функцій. Укажіть цю функцію.', trig_s(fn, A, k, d), wr,
                 'середня лінія дає вертикальний зсув, розмах — амплітуду, період T — коефіцієнт k = 2π/T; значення в нулі показує, синус це чи косинус',
                 f'y_max = {fmt(hi)}, y_min = {fmt(lo)} ⇒ амплітуда {abs(A)}, середня лінія y = {fmt(d)}; період {pim(Tp)} ⇒ k = {ffmt(k)}; f(0) = {fmt(F(round(f(0))))}', img=img)

# ---------- I17: гіпербола ----------
def hyp_s(k, a, b): return f'y = {fmt(k)}/' + ('x' if a == 0 else f'(x {M if a > 0 else "+"} {abs(a)})') + tail(b)
def draw_hyp(ax, k, a, b, lo=-6, hi=6, col=S.BLUE, w=2.8, asym=True):
    if asym:
        if a != 0 or True: ax.seg(a, ax.ymin, a, ax.ymax, col=S.GREEN, w=1.6, dash='7 5')
        ax.seg(ax.xmin, b, ax.xmax, b, col=S.GREEN, w=1.6, dash='7 5')
    f = lambda t: k / (t - a) + b
    ax.curve(f, lo, a - .01, steps=400, w=w, col=col); ax.curve(f, a + .01, hi, steps=400, w=w, col=col)
def f_img_hyp(T, rng, lv):
    k = rng.choice([1, 2, 3, 4, -1, -2, -3, -4]); a = rng.choice([-2, -1, 1, 2]); b = rng.choice([v for v in (-2, -1, 1, 2) if v != a])
    c, ax = G(-6, 6, -6, 6, 'Графік функції y = f(x)')
    draw_hyp(ax, k, a, b)
    px, py = a + 1, b + k
    ax.point(px, py, 'A', dx=8, dy=-6 if k > 0 else 16)
    img = c.save('t4_hy_' + S.tag(k, a, b))
    intro = 'На малюнку зображено графік функції y = f(x) (гіперболу) та його асимптоти (пунктир). '
    kind = rng.choice(['asym', 'domain', 'range'] if lv == 2 else ['formula', 'formula', 'val'])
    two = lambda v: f'(−∞; {fmt(v)}) ∪ ({fmt(v)}; +∞)'
    if kind == 'asym':
        st = lambda u, v: f'x = {fmt(u)}, y = {fmt(v)}'
        wr = [(st(b, a), 'асимптоти переплутано: вертикальна пряма має рівняння x = c, горизонтальна — y = c'), (st(-a, b), 'знак у рівнянні вертикальної асимптоти змінено'), (st(a, -b), 'знак у рівнянні горизонтальної асимптоти змінено'), (st(-a, -b), 'обидва знаки змінено')]
        return T.add(lv, intro + 'Укажіть рівняння асимптот.', st(a, b), wr, 'вертикальна пряма має рівняння x = c (перетинає вісь x у точці c), горизонтальна — y = c', f'вертикальна асимптота перетинає вісь x у точці {fmt(a)}, горизонтальна — вісь y у точці {fmt(b)}', img=img)
    if kind == 'domain':
        wr = [(two(b), 'узято горизонтальну асимптоту: вона обмежує множину значень, а не область визначення'), (two(-a), 'знак змінено'), ('(−∞; +∞)', f'при x = {fmt(a)} функція не визначена — там проходить вертикальна асимптота'), (I(a, None, False), 'враховано лише праву гілку гіперболи'), (two(0), 'це область визначення y = k/x без зсуву')]
        return T.add(lv, intro + 'Укажіть область визначення цієї функції.', two(a), wr, 'область визначення — проєкція графіка на вісь x: гіпербола не має точки з абсцисою, що відповідає вертикальній асимптоті', f'вертикальна асимптота x = {fmt(a)}: D(f) = {two(a)}', img=img)
    if kind == 'range':
        wr = [(two(a), 'узято вертикальну асимптоту: вона обмежує область визначення, а не множину значень'), (two(-b), 'знак змінено'), ('(−∞; +∞)', f'значення {fmt(b)} функція не набуває — там проходить горизонтальна асимптота'), (I(b, None, False), 'враховано лише одну гілку гіперболи'), (two(0), 'це множина значень y = k/x без зсуву')]
        return T.add(lv, intro + 'Укажіть множину значень цієї функції.', two(b), wr, 'множина значень — проєкція графіка на вісь y: гіпербола не перетинає горизонтальну асимптоту', f'горизонтальна асимптота y = {fmt(b)}: E(f) = {two(b)}', img=img)
    chk = f'асимптоти x = {fmt(a)} та y = {fmt(b)} ⇒ y = k/(x {M if a > 0 else "+"} {abs(a)}) {"+" if b > 0 else M} {abs(b)}; точка A({fmt(px)}; {fmt(py)}): k/1 {"+" if b > 0 else M} {abs(b)} = {fmt(py)} ⇒ k = {fmt(k)}'
    if kind == 'formula':
        wr = [(hyp_s(k, -a, b), f'знак у знаменнику неправильний: вертикальна асимптота x = {fmt(a)}, тому знаменник x {M if a > 0 else "+"} {abs(a)}'), (hyp_s(k, a, -b), f'знак вільного доданка неправильний: горизонтальна асимптота y = {fmt(b)}'),
              (hyp_s(-k, a, b), f'знак k неправильний: праворуч від вертикальної асимптоти графік лежить {"вище" if k > 0 else "нижче"} від горизонтальної'), (hyp_s(k, b, a), 'зсуви вздовж осей переставлено місцями')]
        if abs(k) != 1: wr.insert(3, (hyp_s(k // abs(k), a, b), f'не враховано k: у точці A значення відрізняється від {fmt(b)} на {abs(k)}, а не на 1'))
        return T.add(lv, 'На малюнку зображено графік однієї з наведених функцій та його асимптоти (пунктир); позначено точку A графіка. Укажіть цю функцію.', hyp_s(k, a, b), wr,
                     'y = k/(x − a) + b: вертикальна асимптота x = a, горизонтальна y = b; k знаходять за точкою графіка', chk, img=img)
    m = rng.choice([4, 5, 8, 10]); N = a + abs(k) * m; s = 1 if k > 0 else -1; ans = b + F(s, m)
    wr = [(b - F(s, m), 'знак дробу змінено'), (F(s, m), 'не додано b'), (F(b) + s * m, 'дріб перевернуто'), (F(b), 'названо лише горизонтальну асимптоту')]
    return T.add(lv, 'На малюнку зображено графік функції y = k/(x − a) + b та його асимптоти (пунктир); позначено точку A графіка. ' + f'Знайдіть значення цієї функції при x = {fmt(N)}.', ans, wr,
                 'точки з такою абсцисою на малюнку немає: спочатку знайдіть k, a і b', chk + f'; f({fmt(N)}) = {fmt(k)}/{fmt(N - a)} {"+" if b > 0 else M} {abs(b)} = {fmt(ans)}', img=img)

# ---------- I18: перетворення графіків ----------
def tr_lab(sy, sx, p, q):
    inner = (M if sx < 0 else '') + 'x' + (f' {M if p > 0 else "+"} {abs(p)}' if p else '')
    return 'g(x) = ' + (M if sy < 0 else '') + f'f({inner})' + tail(q)
def tr_map(V, sy, sx, p, q): return sorted((sx * (x + p), sy * y + q) for x, y in V)
SHAPES = [[(0, 0), (1, 2), (3, 1), (4, 3)], [(0, 2), (2, 0), (3, 2), (4, 1)], [(0, 0), (2, 3), (3, 1), (5, 2)], [(0, 1), (1, 3), (3, 0), (4, 1)], [(0, 3), (1, 0), (3, 2), (4, 1)], [(0, 0), (1, 3), (2, 1), (4, 2)], [(0, 1), (2, 2), (3, 0), (4, 3)]]
def draw_two(Vf, Vg, view=(-7, 7, -6, 6), names=('y = f(x)', 'y = g(x)'), ends=True):
    c, ax = G(view[0], view[1], view[2], view[3], ' ')
    legend(c, [(S.BLUE, names[0]), (S.ORANGE, names[1])], y=22)
    for V, col in ((Vf, S.BLUE), (Vg, S.ORANGE)):
        c.poly([(ax.X(x), ax.Y(y)) for x, y in V], stroke=col, w=2.8, close=False)
        if ends:
            for x, y in (V[0], V[-1]): ax.point(x, y, None, col=col, r=4)
    return c, ax
def inview(V, view=(-7, 7, -6, 6)): return all(view[0] < x < view[1] and view[2] < y < view[3] for x, y in V)
def f_img_transform(T, rng, lv):
    kind = 'shift' if lv == 2 else rng.choice(['rx', 'ry', 'rxs', 'cs', 'sc', 'sc'])
    if kind == 'sc':
        sk = rng.choice(['2f', 'hf', 'f2', 'fh'])
        for _ in range(500):
            xs = sorted(rng.sample({'2f': range(-5, 6), 'hf': range(-5, 6), 'f2': range(-6, 7, 2), 'fh': range(-3, 4)}[sk], 4))
            ys_ = [rng.choice({'2f': range(-2, 3), 'hf': range(-4, 5, 2), 'f2': range(-4, 5), 'fh': range(-4, 5)}[sk]) for _ in xs]
            if xs[-1] - xs[0] < (4 if sk != 'fh' else 3) or any(u == v for u, v in zip(ys_, ys_[1:])) or all(y == 0 for y in ys_) or len(set(ys_)) < 3: continue
            if sk in ('f2', 'fh') and all(x == 0 for x in xs): continue
            break
        Vf = list(zip(xs, ys_))
        mp = {'2f': lambda V: [(x, 2 * y) for x, y in V], 'hf': lambda V: [(x, F(y, 2)) for x, y in V], 'f2': lambda V: [(F(x, 2), y) for x, y in V], 'fh': lambda V: [(2 * x, y) for x, y in V], 'p2': lambda V: [(x, y + 2) for x, y in V], 's2': lambda V: [(x + 2, y) for x, y in V]}
        lab = {'2f': 'g(x) = 2f(x)', 'hf': 'g(x) = 0,5f(x)', 'f2': 'g(x) = f(2x)', 'fh': 'g(x) = f(0,5x)', 'p2': 'g(x) = f(x) + 2', 's2': 'g(x) = f(x − 2)'}
        why = {'2f': 'це розтяг графіка вдвічі від осі x (уздовж осі y)', 'hf': 'це стиск графіка вдвічі до осі x (уздовж осі y)', 'f2': 'це стиск графіка вдвічі до осі y (уздовж осі x)', 'fh': 'це розтяг графіка вдвічі від осі y (уздовж осі x)', 'p2': 'це паралельне перенесення на 2 одиниці вгору', 's2': 'це паралельне перенесення на 2 одиниці вправо'}
        Vg = mp[sk](Vf)
        if not inview(Vg) or sorted(Vg) == sorted(Vf): return False
        wr = [(lab[j], why[j] + ', а на малюнку ' + why[sk][3:]) for j in ('2f', 'hf', 'f2', 'fh', 'p2') if j != sk and sorted(mp[j](Vf)) != sorted(Vg)]
        c, ax = draw_two(Vf, Vg); img = c.save('t4_tf_' + S.tag(Vf, sk))
        i0 = max(range(4), key=lambda i: abs(Vf[i][0]) + abs(Vf[i][1]))
        return T.add(lv, 'На малюнку зображено графіки функцій y = f(x) та y = g(x), визначених на відрізках. Графік g отримано з графіка f одним перетворенням. Укажіть правильну рівність.', lab[sk], wr,
                     'множник перед f змінює ординати точок (розтяг/стиск уздовж осі y), множник біля x змінює абсциси — «навпаки»: f(2x) стискає, f(0,5x) розтягує',
                     f'точка ({fmt(Vf[i0][0])}; {fmt(Vf[i0][1])}) графіка f перейшла в точку ({fmt(Vg[i0][0])}; {fmt(Vg[i0][1])}) графіка g: {why[sk]}', img=img)
    sh = [list(p) for p in rng.choice(SHAPES)]
    for _ in range(500):
        ox, oy = rng.randint(-6, 2), rng.randint(-5, 2); Vf = [(x + ox, y + oy) for x, y in sh]
        p, q = rng.choice([v for v in range(-6, 7) if v]), rng.choice([v for v in range(-5, 6) if v])
        if kind == 'shift': prm = (1, 1, p, q)
        elif kind == 'rx': prm = (-1, 1, 0, q)
        elif kind == 'ry': prm = (1, -1, 0, q)
        elif kind == 'rxs': prm = (-1, 1, p, 0)
        else: prm = (-1, -1, 0, rng.choice([0, 0, q]))
        Vg = tr_map(Vf, *prm)
        if not inview(Vf) or not inview(Vg): continue
        if kind == 'shift' and (abs(p) < 3 and abs(q) < 3 or p == q): continue
        bbf = (min(x for x, _ in Vf), max(x for x, _ in Vf), min(y for _, y in Vf), max(y for _, y in Vf)); bbg = (min(x for x, _ in Vg), max(x for x, _ in Vg), min(y for _, y in Vg), max(y for _, y in Vg))
        if not (bbf[1] < bbg[0] or bbg[1] < bbf[0] or bbf[3] < bbg[2] or bbg[3] < bbf[2]) and kind != 'shift': continue
        break
    else: return False
    sy, sx, p, q = prm
    RX = '−f(x) — симетрія відносно осі x, f(−x) — симетрія відносно осі y'
    if kind == 'shift':
        cs = [((1, 1, -p, q), f'напрям горизонтального зсуву визначено навпаки: f(x − a) зсуває графік на a одиниць {"вправо" if True else ""}'), ((1, 1, p, -q), 'напрям вертикального зсуву визначено навпаки: f(x) + b зсуває графік на b одиниць вгору'), ((1, 1, -p, -q), 'обидва напрями зсуву визначено навпаки'), ((1, 1, q, p), 'величини зсувів уздовж осей x та y переставлено місцями')]
        trap = 'g(x) = f(x − a) + b: зсув на a вправо (при a > 0) і на b вгору (при b > 0); знак біля x «працює навпаки»'
        sol = f'графік зсунуто на {abs(p)} {"вправо" if p > 0 else "вліво"} і на {abs(q)} {"вгору" if q > 0 else "вниз"}'
    elif kind == 'rx':
        cs = [((1, -1, 0, q), 'переплутано симетрії: ' + RX), ((-1, 1, 0, -q), 'напрям вертикального зсуву визначено навпаки'), ((-1, -1, 0, q), 'зайва симетрія відносно осі y: абсциси точок не змінилися'), ((1, 1, 0, q), 'графік не лише зсунуто, а й відображено відносно осі x'), ((-1, 1, q, 0), 'зсув виконано вздовж осі x замість осі y')]
        trap = RX; sol = 'абсциси точок не змінилися, графік «перевернуто» (симетрія відносно осі x)' + (f' і зсунуто на {abs(q)} {"вгору" if q > 0 else "вниз"}' if q else '')
    elif kind == 'ry':
        cs = [((-1, 1, 0, q), 'переплутано симетрії: ' + RX), ((1, -1, 0, -q), 'напрям вертикального зсуву визначено навпаки'), ((-1, -1, 0, q), 'зайва симетрія відносно осі x'), ((1, 1, 0, q), 'графік не лише зсунуто, а й відображено відносно осі y'), ((1, -1, q, 0), 'зсув виконано вздовж осі x замість осі y')]
        trap = RX; sol = 'графік відображено відносно осі y (абсциси змінили знак)' + (f' і зсунуто на {abs(q)} {"вгору" if q > 0 else "вниз"}' if q else '')
    elif kind == 'rxs':
        cs = [((-1, 1, -p, 0), 'напрям горизонтального зсуву визначено навпаки'), ((1, -1, p, 0), 'переплутано симетрії: ' + RX), ((-1, 1, 0, p), 'зсув виконано вздовж осі y замість осі x'), ((1, 1, p, 0), 'графік не лише зсунуто, а й відображено відносно осі x'), ((-1, -1, p, 0), 'зайва симетрія відносно осі y')]
        trap = RX + '; f(x − a) — зсув на a вправо'; sol = f'графік відображено відносно осі x і зсунуто на {abs(p)} {"вправо" if p > 0 else "вліво"}'
    else:
        cs = [((-1, 1, 0, q), 'виконано лише симетрію відносно осі x, а абсциси точок теж змінили знак'), ((1, -1, 0, q), 'виконано лише симетрію відносно осі y, а ординати теж змінили знак'), ((1, 1, 0, q), 'графік відображено симетрично відносно початку координат, а не залишено на місці'), ((-1, -1, 0, -q if q else 2), 'вертикальний зсув визначено неправильно'), ((-1, -1, 2, q), 'зайвий горизонтальний зсув')]
        trap = '−f(−x) — симетрія відносно початку координат: обидві координати кожної точки змінюють знак'; sol = 'кожна точка (x; y) графіка f перейшла в точку (−x; −y)' + (f', після чого графік зсунуто на {abs(q)} {"вгору" if q > 0 else "вниз"}' if q else '')
    wr = [(tr_lab(*cp), r) for cp, r in cs if tr_map(Vf, *cp) != Vg and cp != prm]
    c, ax = draw_two(Vf, Vg); img = c.save('t4_tf_' + S.tag(Vf, prm))
    return T.add(lv, 'На малюнку зображено графіки функцій y = f(x) та y = g(x), визначених на відрізках. Графік g отримано з графіка f за допомогою перетворень. Укажіть правильну рівність.', tr_lab(*prm), wr, trap, sol, img=img)

# ---------- I19: арифметична прогресія (точковий графік) ----------
def seq_plot(vals, title, ylab, lab=False, ystep=1):
    n = len(vals); ymin = min(min(vals), 0) - ystep; ymax = max(max(vals), 0) + ystep
    if ystep == 1:
        c, ax = G(0, n + 1, int(ymin), int(ymax), title, maxcell=40, xlab='n', ylab=ylab)
    else:
        h = 300; w = 54 * (n + 1); c = S.C(560, h + 80, title); ax = S.Axes(c, (560 - w) / 2, 46, w, h, 0, n + 1, int(ymin) if min(vals) < 0 else 0, int(ymax), 1, ystep, xlab='n', ylab=ylab)
    for i, v in enumerate(vals):
        ax.seg(i + 1, 0, i + 1, float(v), col=S.GRAY, w=1.2, dash='3 4')
        ax.point(i + 1, float(v), fmt(v) if lab else None, col=S.RED, r=5, dx=8, dy=-8)
    return c, ax
def f_img_ap(T, rng, lv):
    for _ in range(300):
        d = rng.choice([-3, -2, -1, 1, 2, 3]); n = 5 if abs(d) == 3 else 6; a1 = rng.randint(-6, 8); vals = [a1 + i * d for i in range(n)]
        if min(vals) >= -7 and max(vals) <= 9 and 0 not in vals[:1]: break
    c, ax = seq_plot(vals, 'Члени арифметичної прогресії', 'aₙ'); img = c.save('t4_ap_' + S.tag(a1, d))
    intro = f'На малюнку точками зображено перші {"п’ять" if n == 5 else "шість"} членів арифметичної прогресії (aₙ): по горизонталі — номер n, по вертикалі — значення aₙ. '
    read = f'a₁ = {fmt(a1)}, a₂ = {fmt(vals[1])}, тому d = {fmt(vals[1])} − {pn(a1)} = {fmt(d)}'
    an = lambda k: a1 + (k - 1) * d; Sn = lambda k: F(k * (2 * a1 + (k - 1) * d), 2)
    kind = rng.choice(['d', 'next'] if lv == 1 else (['far', 'formula', 'S'] if lv == 2 else ['Sfar', 'first', 'Sneg']))
    if kind == 'd':
        wr = [(-d, 'різницю знайдено як a₁ − a₂; потрібно від наступного члена відняти попередній'), (a1, 'названо перший член'), (vals[-1] - vals[0], 'знайдено різницю останнього й першого із зображених членів'), (vals[1], 'названо другий член'), (F(vals[1], a1) if a1 else d + 1, 'знайдено відношення a₂ : a₁, як для геометричної прогресії')]
        return T.add(lv, intro + 'Знайдіть різницю d цієї прогресії.', d, wr, 'різниця арифметичної прогресії d = aₙ₊₁ − aₙ', read, img=img)
    if kind == 'next':
        k = n + rng.choice([2, 3, 4]); ans = an(k)
        wr = [(a1 + k * d, 'використано a₁ + n·d замість a₁ + (n − 1)·d'), (an(k - 1), 'знайдено попередній член'), (vals[-1] + d, f'знайдено лише наступний після зображених член a{sub(n + 1)}'), (a1 - (k - 1) * d, 'знак різниці d змінено'), (vals[-1], 'названо останній із зображених членів')]
        return T.add(lv, intro + f'Знайдіть a{sub(k)}.', ans, wr, 'aₙ = a₁ + (n − 1)·d', read + f'; a{sub(k)} = {fmt(a1)} + {k - 1}·{pn(d)} = {fmt(ans)}', img=img)
    if kind == 'far':
        k = rng.choice([15, 20, 21, 25, 30, 31, 40, 50]); ans = an(k)
        wr = [(a1 + k * d, 'використано a₁ + n·d замість a₁ + (n − 1)·d'), (a1 - (k - 1) * d, 'знак різниці d змінено'), (k * d, 'не додано a₁'), ((k - 1) * d, 'не додано a₁'), (Sn(k), 'знайдено суму перших членів, а не член прогресії')]
        return T.add(lv, intro + f'Знайдіть a{sub(k)}.', ans, wr, 'aₙ = a₁ + (n − 1)·d: до першого члена додають (n − 1) різниць', read + f'; a{sub(k)} = {fmt(a1)} + {k - 1}·{pn(d)} = {fmt(ans)}', img=img)
    if kind == 'formula':
        fs = lambda u, v: 'aₙ = ' + poly([u, v], 'n')
        wr = [(fs(d, a1), 'записано a₁ + dn замість a₁ + d(n − 1)'), (fs(-d, a1 + d), 'знак різниці d змінено'), (fs(a1, d), 'a₁ і d переставлено місцями'), (fs(d, -(a1 - d)), 'знак вільного члена змінено'), (fs(d, a1 + d), 'записано a₁ + d(n + 1) замість a₁ + d(n − 1)')]
        return T.add(lv, intro + 'Укажіть формулу n-го члена цієї прогресії.', fs(d, a1 - d), wr, 'aₙ = a₁ + d(n − 1) = dn + (a₁ − d); перевіряйте формулу підстановкою n = 1 і n = 2', read + f'; aₙ = {fmt(a1)} + {pn(d)}(n − 1) = {poly([d, a1 - d], "n")}', img=img)
    if kind in ('S', 'Sfar'):
        k = rng.choice([10, 12, 15] if kind == 'S' else [20, 25, 30, 40]); ans = Sn(k)
        wr = [(F(an(k)), f'знайдено член a{sub(k)}, а не суму'), (F(k * (a1 + an(k))), 'суму першого й останнього членів помножено на n без ділення на 2'), (F(k * (2 * a1 + k * d), 2), 'у формулі взято n·d замість (n − 1)·d'), (Sn(k - 1), 'додано на один член менше'), (F(k * (2 * a1 - (k - 1) * d), 2), 'знак різниці d змінено')]
        return T.add(lv, intro + f'Знайдіть суму перших {k} членів цієї прогресії.', ans, wr, 'Sₙ = (2a₁ + (n − 1)d)·n/2 = (a₁ + aₙ)·n/2', read + f'; S{sub(k)} = (2·{pn(a1)} + {k - 1}·{pn(d)})·{k}/2 = {fmt(ans)}', img=img)
    if kind == 'first':
        Cv = rng.choice([50, 75, 100, 120, 150, 200]) * (1 if d > 0 else -1)
        k = next(j for j in range(1, 500) if (an(j) > Cv if d > 0 else an(j) < Cv))
        wr = [(k - 1, f'член із цим номером ще не {"більший" if d > 0 else "менший"} за {fmt(Cv)}: a{sub(k - 1)} = {fmt(an(k - 1))}'), (k + 1, 'номер знайдено з помилкою на 1: уже попередній член задовольняє умову'), (abs(Cv) // abs(d), 'число поділено на різницю без урахування a₁'), (F(an(k)), 'названо сам член, а не його номер'), (k - 2, f'a{sub(max(k - 2, 1))} ще не задовольняє умову')]
        return T.add(lv, intro + f'Знайдіть номер першого члена цієї прогресії, який {"більший" if d > 0 else "менший"} за {fmt(Cv)}.', k, wr, 'складіть нерівність a₁ + (n − 1)d > C (або < C) і знайдіть найменше натуральне n',
                     read + f'; {fmt(a1)} + {pn(d)}(n − 1) {">" if d > 0 else "<"} {fmt(Cv)}; a{sub(k - 1)} = {fmt(an(k - 1))}, a{sub(k)} = {fmt(an(k))}, тому n = {k}', img=img)
    # сума всіх від’ємних / додатних членів серед перших N
    Nn = rng.choice([20, 25, 30]); neg = d > 0
    part = [an(j) for j in range(1, Nn + 1) if (an(j) < 0 if neg else an(j) > 0)]
    if len(part) < 2 or len(part) > Nn - 2:
        part = [an(j) for j in range(n + 1, Nn + 1)]; ans = sum(part)
        wr = [(Sn(Nn), f'знайдено суму всіх {Nn} членів, а не лише членів із номерами від {n + 1}'), (ans + vals[-1], f'до суми зараховано також член a{sub(n)}'), (ans - an(n + 1), f'член a{sub(n + 1)} пропущено'), (Sn(Nn) + Sn(n), 'суму зображених членів додано замість віднімання'), (F(an(Nn)), 'названо останній член')]
        return T.add(lv, intro + f'Знайдіть суму членів цієї прогресії з номерами від {n + 1} до {Nn} включно.', ans, wr, f'шукана сума дорівнює S{sub(Nn)} − S{sub(n)}', read + f'; S{sub(Nn)} = {fmt(Sn(Nn))}, S{sub(n)} = {fmt(Sn(n))}; різниця {fmt(ans)}', img=img)
    ans = sum(part); m = len(part)
    wr = [(Sn(Nn), f'знайдено суму всіх перших {Nn} членів'), (-ans, 'знак суми змінено'), (ans - part[-1] if neg else ans - part[-1], 'один із потрібних членів пропущено'), (F(m), 'знайдено кількість таких членів, а не суму'), (Sn(Nn) - ans, f'знайдено суму {"невід’ємних" if neg else "недодатних"} членів')]
    return T.add(lv, intro + f'Знайдіть суму всіх {"від’ємних" if neg else "додатних"} членів цієї прогресії.' if (neg and d > 0 and a1 < 0) or (not neg and a1 > 0) else intro + f'Знайдіть суму всіх {"від’ємних" if neg else "додатних"} членів серед перших {Nn} членів цієї прогресії.', ans, wr,
                 'з’ясуйте, скільки членів мають потрібний знак (нерівність для aₙ), і додайте їх за формулою суми', read + f'; потрібний знак мають {m} членів: від {fmt(part[0])} до {fmt(part[-1])}; сума ({fmt(part[0])} + {pn(part[-1])})·{m}/2 = {fmt(ans)}', img=img)

# ---------- I20: геометрична прогресія (точковий графік) ----------
GPS = [([1, 2, 4, 8, 16], 2), ([2, 4, 8, 16], 2), ([16, 8, 4, 2, 1], 2), ([3, 6, 12, 24], 3), ([24, 12, 6, 3], 3), ([1, 3, 9, 27], 3), ([27, 9, 3, 1], 3), ([32, 16, 8, 4, 2], 4), ([18, 6, 2], 2), ([2, 6, 18], 2), ([5, 10, 20], 2), ([20, 10, 5], 2)]
def f_img_gp(T, rng, lv):
    vals, ystep = rng.choice(GPS); b1 = F(vals[0]); q = F(vals[1], vals[0]); n = len(vals)
    c, ax = seq_plot(vals, 'Члени геометричної прогресії', 'bₙ', lab=True, ystep=ystep); img = c.save('t4_gp_' + S.tag(vals))
    cnt = {3: 'три', 4: 'чотири', 5: 'п’ять'}[n]
    intro = f'На малюнку точками зображено перші {cnt} член{"и" if n < 5 else "ів"} геометричної прогресії (bₙ): по горизонталі — номер n, по вертикалі — значення bₙ (підписані біля точок). '
    read = f'b₁ = {fmt(b1)}, b₂ = {fmt(vals[1])}, тому q = {fmt(vals[1])} : {fmt(b1)} = {ffmt(q)}'
    bn = lambda k: b1 * q ** (k - 1)
    kind = rng.choice(['q', 'term'] if lv == 2 else (['S', 'term2'] if q > 1 else ['Sinf', 'term2']))
    if kind == 'q':
        wr = [(1 / q, 'поділено попередній член на наступний'), (F(vals[1] - vals[0]), 'знайдено різницю b₂ − b₁, як для арифметичної прогресії'), (b1, 'названо перший член'), (F(vals[-1], vals[0]), 'останній із зображених членів поділено на перший'), (F(vals[1]), 'названо другий член')]
        return T.add(lv, intro + 'Знайдіть знаменник q цієї прогресії.', q, wr, 'знаменник геометричної прогресії q = bₙ₊₁ : bₙ', read, img=img)
    if kind in ('term', 'term2'):
        k = n + (rng.choice([2, 3]) if kind == 'term' else rng.choice([3, 4, 5])); ans = bn(k)
        wr = [(b1 * q ** k, 'використано b₁·qⁿ замість b₁·qⁿ⁻¹'), (bn(k - 1), 'знайдено попередній член'), (b1 * q * (k - 1), 'степінь замінено множенням'), (b1 + (k - 1) * (F(vals[1]) - b1), 'прогресію сплутано з арифметичною'), (F(vals[-1]) * q, f'знайдено лише b{sub(n + 1)}')]
        return T.add(lv, intro + f'Знайдіть b{sub(k)}.', ans, wr, 'bₙ = b₁·qⁿ⁻¹', read + f'; b{sub(k)} = {fmt(b1)}·({ffmt(q)}){sup(k - 1)} = {ffmt(ans)}', img=img)
    if kind == 'S':
        k = n + rng.choice([2, 3, 4]); ans = b1 * (q ** k - 1) / (q - 1)
        wr = [(bn(k), f'знайдено член b{sub(k)}, а не суму'), (b1 * (q ** k - 1), 'не поділено на q − 1' if q != 2 else 'результат прочитано неправильно'), (b1 * (q ** (k - 1) - 1) / (q - 1), 'додано на один член менше'), (b1 * q ** k / (q - 1), 'у чисельнику не віднято 1'), (b1 * (q ** (k + 1) - 1) / (q - 1), 'додано на один член більше')]
        return T.add(lv, intro + f'Знайдіть суму перших {k} членів цієї прогресії.', ans, wr, 'Sₙ = b₁(qⁿ − 1)/(q − 1)', read + f'; S{sub(k)} = {fmt(b1)}·({fmt(q)}{sup(k)} − 1)/({fmt(q)} − 1) = {ffmt(ans)}', img=img)
    ans = b1 / (1 - q)
    wr = [(b1 / (1 + q), 'у знаменнику взято 1 + q'), (F(sum(vals)), 'додано лише зображені члени'), (b1 / q, 'перший член поділено на q'), (b1 * (1 - q), 'перший член помножено на (1 − q) замість ділення'), (b1 * q / (1 - q), 'у чисельнику взято b₂ замість b₁')]
    return T.add(lv, intro + 'Прогресія нескінченна. Знайдіть суму всіх її членів.', ans, wr, 'сума нескінченної геометричної прогресії з |q| < 1: S = b₁/(1 − q)', read + f'; S = {fmt(b1)}/(1 − {ffmt(q)}) = {ffmt(ans)}', img=img)

# ---------- I21: два графіки — композиція, порівняння ----------
def gen_sl(rng, x0=-5, x1=5, ylim=5):
    for _ in range(3000):
        br = sorted(rng.sample(range(x0 + 2, x1 - 1), rng.choice([1, 2])))
        if any(b - a < 2 for a, b in zip(br, br[1:])): continue
        xs = [x0] + br + [x1]; y = rng.randint(-ylim + 1, ylim - 1); V = [(x0, y)]; prev = 0; ok = True
        for xa, xb in zip(xs, xs[1:]):
            sl = rng.choice([s_ for s_ in (-2, -1, 1, 2) if s_ * prev <= 0 and s_ != prev])
            y += sl * (xb - xa); prev = sl
            if abs(y) > ylim: ok = False; break
            V.append((xb, y))
        if ok: return V
    raise ValueError('gen_sl')
def f_img_two(T, rng, lv):
    for _ in range(300):
        Vf, Vg = gen_sl(rng), gen_sl(rng)
        same = [t for t in range(-10, 11) if pl_val(Vf, F(t, 2)) == pl_val(Vg, F(t, 2))]
        if len(same) <= 2 and all(b - a > 1 for a, b in zip(same, same[1:])): break
    else: return False
    f = lambda x: pl_val(Vf, x); g = lambda x: pl_val(Vg, x); ind = lambda v: -5 <= v <= 5
    c, ax = draw_two(Vf, Vg, view=(-6, 6, -6, 6)); img = c.save('t4_tw_' + S.tag(Vf, Vg))
    intro = 'На малюнку зображено графіки функцій y = f(x) та y = g(x), визначених на відрізку [−5; 5]. '
    kind = 'comp' if lv == 2 else rng.choice(['cnt', 'combo', 'eq'])
    if kind == 'comp':
        cand = [x for x in range(-5, 6) if ind(g(x)) and ind(f(x)) and f(g(x)) != g(f(x)) and g(x) != x]
        if not cand: return False
        x = rng.choice(cand); ans = f(g(x))
        wr = [(g(f(x)), 'порядок дій переплутано: знайдено g(f(x)), а потрібно спочатку обчислити внутрішню функцію g'), (g(x), 'знайдено лише внутрішнє значення g(x)'), (f(x) * g(x), 'композицію сплутано з добутком f(x)·g(x)'), (f(x) + g(x), 'композицію сплутано із сумою f(x) + g(x)'), (f(x), 'знайдено f(x) замість f(g(x))')]
        return T.add(lv, intro + f'Знайдіть f(g({fmt(x)})).', ans, wr, 'спочатку за графіком g знайдіть внутрішнє значення, потім підставте його як аргумент у f', f'g({fmt(x)}) = {fmt(g(x))}; f({fmt(g(x))}) = {fmt(ans)}', img=img)
    if kind == 'combo':
        cand = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a != b and ind(g(a)) and ind(f(b)) and ind(f(a)) and ind(g(b)) and g(a) != a and f(b) != b]
        if not cand: return False
        a, b = rng.choice(cand); ans = f(g(a)) + g(f(b))
        wr = [(g(f(a)) + f(g(b)), 'в обох доданках порядок функцій переплутано'), (f(g(a)) - g(f(b)), 'другий доданок віднято замість додавання'), (g(a) + f(b), 'знайдено лише внутрішні значення'), (f(g(a)), 'обчислено лише перший доданок'), (f(a) * g(a) + g(b) * f(b), 'композиції сплутано з добутками')]
        return T.add(lv, intro + f'Знайдіть значення виразу f(g({fmt(a)})) + g(f({fmt(b)})).', ans, wr, 'у записі f(g(x)) спочатку обчислюють внутрішню функцію g, у записі g(f(x)) — внутрішню f',
                     f'g({fmt(a)}) = {fmt(g(a))}, f({fmt(g(a))}) = {fmt(f(g(a)))}; f({fmt(b)}) = {fmt(f(b))}, g({fmt(f(b))}) = {fmt(g(f(b)))}; сума {fmt(ans)}', img=img)
    if kind == 'cnt':
        op = rng.choice(list(OPPS)); xs_ = lambda o: [x for x in range(-5, 6) if CMP[o](f(x), g(x))]
        X = xs_(op)
        if not 2 <= len(X) <= 9: return False
        wr = [(len(xs_(TOGS[op])), ('не враховано цілі точки, у яких f(x) = g(x)' if op in ('>=', '<=') else 'зараховано точки, у яких f(x) = g(x), хоча нерівність строга')), (len(xs_(OPPS[op])), 'графіки переплутано: пораховано точки, де виконується протилежна нерівність'), (11, 'пораховано всі цілі числа відрізка [−5; 5]'), (len(X) + 1, 'одне зайве число зараховано'), (len(X) - 1, 'одне число пропущено')]
        return T.add(lv, intro + f'Скільки цілих чисел x задовольняють нерівність f(x) {SYM[op]} g(x)?', len(X), wr, 'f(x) > g(x) там, де графік f лежить вище від графіка g; перевіряйте кожне ціле x від −5 до 5',
                     f'нерівність виконується для x = {", ".join(fmt(x) for x in X)} — усього {len(X)} чисел', img=img)
    brk = sorted(set(x for x, _ in Vf) | set(x for x, _ in Vg)); roots = set()
    for xa, xb in zip(brk, brk[1:]):
        da, db = f(xa) - g(xa), f(xb) - g(xb)
        if da == 0: roots.add(F(xa))
        if db == 0: roots.add(F(xb))
        if da * db < 0: roots.add(F(xa) + (xb - xa) * da / (da - db))
    if not roots: return False
    ask = rng.choice(['n', 'sum']) if all(r.denominator in (1, 2) for r in roots) and len(roots) >= 2 else 'n'
    zf, zg = len(pl_solve(Vf, 0)), len(pl_solve(Vg, 0))
    if ask == 'n':
        k = len(roots)
        wr = [(zf, 'знайдено кількість нулів функції f'), (zg, 'знайдено кількість нулів функції g'), (zf + zg, 'додано кількості нулів обох функцій'), (k + 1, 'одну точку перетину пораховано двічі'), (k - 1, 'одну точку перетину пропущено')]
        return T.add(lv, intro + 'Скільки коренів має рівняння f(x) = g(x)?', k, wr, 'корені рівняння f(x) = g(x) — абсциси точок перетину графіків f і g (а не точок перетину з віссю x)', f'графіки перетинаються в {k} точ{"ці" if k == 1 else "ках"}: x = {", ".join(ffmt(r) for r in sorted(roots))}', img=img)
    ans = sum(roots)
    wr = [(sum(f(r) for r in roots), 'додано ординати точок перетину, а не абсциси'), (F(len(roots)), 'знайдено кількість коренів, а не їхню суму'), (-ans, 'знак змінено'), (sum(pl_solve(Vf, 0)), 'додано нулі функції f'), (ans - max(roots), 'один із коренів пропущено')]
    return T.add(lv, intro + 'Знайдіть суму всіх коренів рівняння f(x) = g(x).', ans, wr, 'корені рівняння f(x) = g(x) — абсциси точок перетину графіків', f'графіки перетинаються при x = {", ".join(fmt(r) for r in sorted(roots))}; сума {fmt(ans)}', img=img)

# ---------- I22: обернена функція ----------
def f_img_inverse(T, rng, lv):
    for _ in range(300):
        k = rng.choice([4, 5]); xs = sorted(rng.sample(range(-6, 7), k)); ys_ = sorted(rng.sample(range(-5, 6), k))
        if xs[0] > -3 or xs[-1] < 3: continue
        if rng.random() < .5: ys_ = ys_[::-1]
        V = list(zip(xs, ys_))
        if any(abs(F(y2 - y1, x2 - x1)) > 3 for (x1, y1), (x2, y2) in zip(V, V[1:])): continue
        break
    a, b = dom(V); ylo, yhi = min(ys_), max(ys_); f = lambda x: pl_val(V, x)
    gi = lambda cv: pl_solve(V, cv)[0]
    c, ax = draw_pl(V); img = c.save('t4_inv_' + S.tag(V))
    intro = base(V) + 'Функція g є оберненою до функції f. '
    cand = [t for t in range(ylo, yhi + 1) if t != 0 and gi(t).denominator == 1 and a <= t <= b and gi(t) != t and f(t).denominator <= 2 and f(t) != gi(t)]
    if not cand: return False
    if lv == 2:
        t = rng.choice(cand); ans = gi(t)
        wr = [(f(t), f'знайдено f({fmt(t)}), а не значення оберненої функції'), (-ans, 'знак змінено'), (-F(t), 'обернену функцію сплутано з протилежним числом'), (F(1, t) if t else F(1), 'обернену функцію сплутано з оберненим числом 1/c')]
        for dt in (1, -1):
            if ylo <= t + dt <= yhi and gi(t + dt).denominator == 1: wr.append((gi(t + dt), f'знайдено g({fmt(t + dt)})'))
        return T.add(lv, intro + f'Знайдіть g({fmt(t)}).', ans, wr, 'g(c) — це таке x, що f(x) = c: проведіть пряму y = c і знайдіть абсцису точки перетину з графіком f', f'f({fmt(ans)}) = {fmt(t)}, тому g({fmt(t)}) = {fmt(ans)}', img=img)
    kind = rng.choice(['sum', 'eq', 'fg'])
    if kind == 'sum' and len(cand) >= 2:
        t1, t2 = rng.sample(cand, 2); ans = gi(t1) + gi(t2)
        wr = [(f(t1) + f(t2), 'додано значення самої функції f, а не оберненої'), (gi(t1) - gi(t2), 'знайдено різницю'), (gi(t1) + f(t2), 'для другого доданка знайдено f замість g'), (f(t1) + gi(t2), 'для першого доданка знайдено f замість g'), (F(t1 + t2), 'додано аргументи')]
        return T.add(lv, intro + f'Знайдіть g({fmt(t1)}) + g({fmt(t2)}).', ans, wr, 'g(c) — це таке x, що f(x) = c', f'f({fmt(gi(t1))}) = {fmt(t1)} ⇒ g({fmt(t1)}) = {fmt(gi(t1))}; f({fmt(gi(t2))}) = {fmt(t2)} ⇒ g({fmt(t2)}) = {fmt(gi(t2))}; сума {fmt(ans)}', img=img)
    if kind == 'eq':
        cand2 = [x for x in range(a, b + 1) if x != 0 and f(x).denominator == 1 and f(x) != x and ylo <= x <= yhi and gi(x) != f(x) and gi(x).denominator <= 2]
        if not cand2: return False
        x = rng.choice(cand2); ans = f(x)
        wr = [(gi(x), f'знайдено g({fmt(x)}), тобто розв’язано рівняння f(t) = {fmt(x)}, а потрібно навпаки'), (-ans, 'знак змінено'), (F(x), 'за корінь узято праву частину рівняння'), (-F(x), 'узято число, протилежне до правої частини')]
        return T.add(lv, intro + f'Розв’яжіть рівняння g(x) = {fmt(x)}.', ans, wr, 'якщо g(x) = c, то x = f(c): обернена функція «міняє місцями» аргумент і значення', f'g(x) = {fmt(x)} ⇔ x = f({fmt(x)}) = {fmt(ans)}', img=img)
    t = rng.choice(cand); ans = f(t) + gi(t)
    wr = [(2 * f(t), 'обидва доданки обчислено як f'), (2 * gi(t), 'обидва доданки обчислено як g'), (f(t) - gi(t), 'знайдено різницю'), (gi(t), 'знайдено лише g'), (f(t), 'знайдено лише f')]
    return T.add(lv, intro + f'Знайдіть f({fmt(t)}) + g({fmt(t)}).', ans, wr, 'f(c) читають за абсцисою c, а g(c) — за ординатою c (це x, для якого f(x) = c)', f'f({fmt(t)}) = {fmt(f(t))}; g({fmt(t)}) = {fmt(gi(t))}, бо f({fmt(gi(t))}) = {fmt(t)}; сума {fmt(ans)}', img=img)

# ---------- I23: парна / непарна функція за половиною графіка ----------
def f_img_parity_half(T, rng, lv):
    even = rng.random() < .5; s = 1 if even else -1
    V = gen_pl(rng, nseg=(2, 4), x_start=0, y_start=None if even else 0, ylo=-4, yhi=4, xhi=7, int_zeros=(lv == 3))
    b = V[-1][0]; f = lambda x: pl_val(V, x); Y = max(abs(y) for _, y in V)
    c, ax = draw_pl(V, title=f'Графік функції y = f(x) при x ≥ 0', view=(-b - 1, b + 1, -Y - 1, Y + 1)); img = c.save('t4_ph_' + S.tag(V, even))
    name = 'парною' if even else 'непарною'
    intro = f'Функція y = f(x) визначена на відрізку [−{b}; {b}] і є {name}. На малюнку зображено її графік на відрізку [0; {b}]. '
    rule = 'для парної функції f(−x) = f(x): графік симетричний відносно осі y' if even else 'для непарної функції f(−x) = −f(x): графік симетричний відносно початку координат'
    full = lambda x: f(x) if x >= 0 else s * f(-x)
    ints = [x for x in range(1, b + 1) if f(x).denominator == 1 and f(x) != 0]
    if lv == 1:
        if not ints: return False
        x = rng.choice(ints); ans = s * f(x)
        wr = [(-ans, 'для парної функції знак значення не змінюється' if even else 'для непарної функції знак значення змінюється на протилежний'), (F(-x), 'названо аргумент, а не значення функції')]
        wr += [(s * f(t), f'значення прочитано для x = {t}') for t in (x + 1, x - 1) if 0 <= t <= b and f(t).denominator <= 2]
        wr.append((F(x), 'названо модуль аргументу'))
        return T.add(lv, intro + f'Знайдіть f(−{x}).', ans, wr, rule, f'f({x}) = {fmt(f(x))}, тому f(−{x}) = {fmt(ans)}', img=img)
    if lv == 2:
        if len(ints) < 2: return False
        p, q = rng.sample(ints, 2); form = rng.choice(['a', 'b'])
        if form == 'a':
            ans = s * f(p) + f(q)
            wr = [(-s * f(p) + f(q), 'властивість застосовано неправильно: ' + rule), (s * f(p) - f(q), 'другий доданок віднято'), (-ans, 'знак результату змінено'), (f(p) * f(q) * s, 'значення перемножено, а не додано'), (f(q), 'обчислено лише другий доданок')]
            return T.add(lv, intro + f'Знайдіть значення виразу f(−{p}) + f({q}).', ans, wr, rule, f'f(−{p}) = {fmt(s * f(p))}, f({q}) = {fmt(f(q))}; сума {fmt(ans)}', img=img)
        ans = 2 * s * f(p) - s * f(q)
        wr = [(-ans, 'властивість застосовано неправильно: ' + rule), (2 * s * f(p) + s * f(q), 'другий доданок додано замість віднімання'), (s * f(p) - s * f(q), 'пропущено множник 2'), (2 * f(p) * s - f(q) * (-s), 'для другого значення знак визначено неправильно'), (2 * s * f(p), 'обчислено лише перший доданок')]
        return T.add(lv, intro + f'Знайдіть значення виразу 2f(−{p}) − f(−{q}).', ans, wr, rule, f'f(−{p}) = {fmt(s * f(p))}, f(−{q}) = {fmt(s * f(q))}; 2·{pn(s * f(p))} − {pn(s * f(q))} = {fmt(ans)}', img=img)
    kind = rng.choice(['zeros', 'ineq', 'ineq', 'sum'])
    zr = pl_solve(V, 0); zpos = [z for z in zr if z > 0]
    if kind == 'sum' and all(f(x).denominator == 1 for x in range(0, b + 1)):
        ans = sum(full(x) for x in range(-b, b + 1)); half = sum(f(x) for x in range(0, b + 1))
        wr = [(half, 'додано лише значення на зображеній частині графіка'), (2 * half, 'значення f(0) пораховано двічі' if even else 'суму зображених значень подвоєно: для непарної функції значення в симетричних точках протилежні'), (F(0) if even else 2 * half - f(0), 'використано властивість непарної функції' if even else 'використано властивість парної функції'), (ans + 1, 'помилка в одному з доданків'), (ans - f(b) * s, 'значення на лівому кінці не враховано')]
        return T.add(lv, intro + f'Знайдіть суму значень функції в усіх цілих точках відрізка [−{b}; {b}]: f(−{b}) + f(−{b - 1}) + … + f({b}).', ans, wr, rule,
                     ('значення в точках x і −x однакові, тому сума дорівнює 2·(' + ' + '.join(pn(f(x)) for x in range(1, b + 1)) + f') + f(0) = {fmt(ans)}') if even else 'значення в точках x і −x протилежні, а f(0) = 0, тому всі доданки взаємно знищуються: сума дорівнює 0', img=img)
    if kind == 'zeros' or not zpos:
        tot = 2 * len(zpos) + (1 if f(0) == 0 else 0)
        if tot < 2: return False
        wr = [(len(zr), 'пораховано нулі лише на зображеній частині графіка'), (2 * len(zr), 'нуль x = 0 пораховано двічі') if f(0) == 0 else (2 * len(zr) + 1, 'зараховано x = 0, хоча f(0) ≠ 0'), (tot + 1, 'один нуль пораховано двічі'), (tot - 1, 'один нуль пропущено'), (len(zpos), 'пораховано лише додатні нулі')]
        return T.add(lv, intro + f'Скільки нулів має ця функція на відрізку [−{b}; {b}]?', tot, wr, 'графік симетричний, тому кожному додатному нулю відповідає від’ємний; нуль x = 0 (якщо він є) рахують один раз',
                     f'додатні нулі: {", ".join(fmt(z) for z in zpos)}; симетричні їм: {", ".join(fmt(-z) for z in zpos)}' + ('; також x = 0' if f(0) == 0 else '') + f'; разом {tot}', img=img)
    op = rng.choice(['>', '<']); crit = sorted(set([-b, b, 0] + zr + [-z for z in zr]))
    def Sx(o, sg=s, right=False): return pred_set(lambda x: (0 if right else -b) <= x <= b and CMP[o](f(x) if x >= 0 else sg * f(-x)), crit)
    sol = Sx(op)
    if not sol: return False
    wr = [(setstr(Sx(op, right=True)), 'розглянуто лише зображену частину графіка (x ≥ 0)'), (setstr(Sx(op, sg=-s)), 'графік добудовано як для ' + ('непарної' if even else 'парної') + ' функції'), (setstr(Sx(OPPS[op])), 'знак нерівності переплутано'), (setstr(Sx(TOGS[op])), 'нерівність строга: нулі функції не входять'), (setstr(mirror(Sx(op, right=True))), 'узято лише добудовану ліву частину')]
    return T.add(lv, intro + f'Розв’яжіть нерівність f(x) {SYM[op]} 0.', setstr(sol), wr, rule + '; добудуйте ліву половину графіка й розгляньте весь відрізок',
                 f'на [0; {b}] нерівність виконується при x ∈ {setstr(Sx(op, right=True)) if Sx(op, right=True) else "∅"}; ' + ('ліва частина симетрична відносно осі y' if even else 'ліворуч знаки значень протилежні') + f'; відповідь {setstr(sol)}', img=img)

# ---------- I24: чотири графіки — вибрати потрібний ----------
def panel_canvas(drawers, title=None, rng_=(-5, 5)):
    c = S.C(600, 610 if not title else 630, title); oy = 20 if title else 0
    for i, dr in enumerate(drawers):
        x0 = 40 + (i % 2) * 290; y0 = 44 + (i // 2) * 290 + oy; w = h = 230
        ax = S.Axes(c, x0, y0, w, h, rng_[0], rng_[1], rng_[0], rng_[1], 1, 1, labels=False, size=10)
        dr(ax)
        halo(c, ax.X(1), ax.Y(0) + 14, '1', size=10); halo(c, ax.X(0) - 6, ax.Y(1) + 4, '1', size=10, anchor='end'); halo(c, ax.X(0) - 6, ax.Y(0) + 13, '0', size=10, anchor='end')
        c.circle(x0 + 14, y0 + 14, 12, fill='#1f2937', stroke='#1f2937'); c.text(x0 + 14, y0 + 19, str(i + 1), size=14, col='#ffffff', anchor='middle', bold=True)
    return c
def cv(fn, a=-5, b=5): return lambda ax: ax.curve(fn, a, b, col=S.BLUE, w=2.4, steps=400)
def cvh(k, a, b): return lambda ax: draw_hyp(ax, k, a, b, lo=-5, hi=5, w=2.4)
def sq_(t): return math.sqrt(t)
def panel_sets(rng, lv):
    m, n = rng.choice([1, 2, 3]), rng.choice([1, 2, 3]); sg_ = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    kind = rng.choice(['lin', 'par', 'abs', 'explog'] if lv == 1 else ['par2', 'sqrt', 'cub', 'hyp', 'expshift', 'trig', 'log', 'abs2'])
    if kind == 'lin':
        k = rng.choice([1, 2, F(1, 2)]); return [(lin_s(a * k, b * n), cv(lambda t, a=a, b=b: float(a * k) * t + b * n)) for a, b in sg_], 'знак k показує, зростає чи спадає функція; b — ордината точки перетину з віссю y'
    if kind == 'par': return [(par_s(1, a * m, b * n), cv(lambda t, a=a, b=b: (t - a * m) ** 2 + b * n)) for a, b in sg_], 'вершина параболи y = (x − m)² + n розташована в точці (m; n)'
    if kind == 'par2': return [(par_s(a, b * m, -a * n), cv(lambda t, a=a, b=b: a * (t - b * m) ** 2 - a * n)) for a, b in sg_], 'знак перед дужкою задає напрям гілок; вершина параболи y = a(x − m)² + n — точка (m; n)'
    ab = lambda a, b: f'y = |x {M if a > 0 else "+"} {m}| {"+" if b > 0 else M} {n}'
    if kind == 'abs': return [(ab(a, b), cv(lambda t, a=a, b=b: abs(t - a * m) + b * n)) for a, b in sg_], 'графік y = |x − m| + n — «кут» із вершиною в точці (m; n)'
    if kind == 'abs2': return [(f'y = {M if a < 0 else ""}|x {M if b > 0 else "+"} {m}|' + tail(a * n), cv(lambda t, a=a, b=b: a * abs(t - b * m) + a * n)) for a, b in sg_], 'знак «−» перед модулем перевертає «кут» гілками вниз; вершина — у точці (m; n)'
    if kind == 'sqrt':
        return [(f'y = √(x {M if a > 0 else "+"} {m}) {"+" if b > 0 else M} {n}', cv(lambda t, a=a, b=b: sq_(t - a * m) + b * n)) for a, b in sg_], 'графік y = √(x − m) + n починається в точці (m; n) і йде вправо-вгору'
    if kind == 'cub':
        m, n = rng.choice([1, 2]), rng.choice([1, 2, 3])
        return [(f'y = (x {M if a > 0 else "+"} {m})³ {"+" if b > 0 else M} {n}', cv(lambda t, a=a, b=b: (t - a * m) ** 3 + b * n)) for a, b in sg_], 'центр симетрії графіка y = (x − m)³ + n — точка (m; n)'
    if kind == 'hyp':
        k = rng.choice([1, 2, -1, -2]); return [(hyp_s(k, m, 0), cvh(k, m, 0)), (hyp_s(k, -m, 0), cvh(k, -m, 0)), (hyp_s(k, 0, m), cvh(k, 0, m)), (hyp_s(k, 0, -m), cvh(k, 0, -m))], 'y = k/(x − a) + b: вертикальна асимптота x = a, горизонтальна y = b'
    if kind == 'explog':
        a = rng.choice([2, 3]); lg = {2: ('log₂', 'log₀,₅'), 3: ('log₃', 'log₁/₃')}[a]
        return [(f'y = {a}ˣ', cv(lambda t: a ** t)), (f'y = (1/{a})ˣ', cv(lambda t: a ** (-t))), (f'y = {lg[0]} x', cv(lambda t: math.log(t) / math.log(a), 1e-4, 5)), (f'y = {lg[1]} x', cv(lambda t: -math.log(t) / math.log(a), 1e-4, 5))], 'показникова функція визначена при всіх x і проходить через (0; 1); логарифмічна визначена при x > 0 і проходить через (1; 0); основа, більша за 1, — зростання'
    if kind == 'expshift':
        a = rng.choice([2, 3]); m = rng.choice([1, 2, 3])
        return [(exp_s(a, m), cv(lambda t: a ** t + m)), (exp_s(a, -m), cv(lambda t: a ** t - m)), (exps_s(a, m), cv(lambda t: a ** (t - m))), (exps_s(a, -m), cv(lambda t: a ** (t + m)))], 'доданок після степеня зсуває графік уздовж осі y (змінює асимптоту), доданок у показнику — уздовж осі x'
    if kind == 'log':
        a = rng.choice([2, 3]); lg = {2: 'log₂', 3: 'log₃'}[a]; L = lambda t: math.log(t) / math.log(a)
        return [(log_s(a, m, 0), cv(lambda t: L(t - m), m + 1e-4, 5)), (log_s(a, -m, 0), cv(lambda t: L(t + m), -m + 1e-4, 5)), (log_s(a, 0, m), cv(lambda t: L(t) + m, 1e-4, 5)), (log_s(a, 0, -m), cv(lambda t: L(t) - m, 1e-4, 5))], 'y = log_a(x − c) має вертикальну асимптоту x = c; доданок після логарифма зсуває графік уздовж осі y'
    v = rng.choice(['sign', 'shift', 'ak'])
    if v == 'sign': return [('y = sin x', cv(math.sin)), ('y = cos x', cv(math.cos)), ('y = −sin x', cv(lambda t: -math.sin(t))), ('y = −cos x', cv(lambda t: -math.cos(t)))], 'sin 0 = 0, cos 0 = 1; знак «−» відображає графік відносно осі x'
    if v == 'shift': return [('y = sin x + 1', cv(lambda t: math.sin(t) + 1)), ('y = sin x − 1', cv(lambda t: math.sin(t) - 1)), ('y = cos x + 1', cv(lambda t: math.cos(t) + 1)), ('y = cos x − 1', cv(lambda t: math.cos(t) - 1))], 'значення в нулі: sin 0 = 0, cos 0 = 1; доданок зсуває графік уздовж осі y'
    return [('y = 2sin x', cv(lambda t: 2 * math.sin(t))), ('y = sin 2x', cv(lambda t: math.sin(2 * t))), ('y = 2cos x', cv(lambda t: 2 * math.cos(t))), ('y = cos 2x', cv(lambda t: math.cos(2 * t)))], 'множник перед функцією змінює амплітуду, множник біля x — період'
def f_img_panels(T, rng, lv):
    items, trap = panel_sets(rng, lv)
    order = shuffled(rng, range(4)); items = [items[i] for i in order]; pick = rng.randrange(4)
    c = panel_canvas([d for _, d in items]); img = c.save('t4_pn_' + S.tag([s_ for s_, _ in items], pick))
    wr = [(i + 1, f'на малюнку {i + 1} зображено графік функції {items[i][0]}') for i in range(4) if i != pick]
    return T.add(lv, f'На якому з малюнків 1–4 зображено графік функції {items[pick][0]}? У відповіді вкажіть номер малюнка.', pick + 1, wr, trap, f'графік функції {items[pick][0]} зображено на малюнку {pick + 1}', img=img)

# ---------- I25: чотири графіки — парність, монотонність ----------
EVEN = [('y = x² − 2', cv(lambda t: t * t - 2)), ('y = |x| − 1', cv(lambda t: abs(t) - 1)), ('y = 3 − x²', cv(lambda t: 3 - t * t)), ('y = 2cos x', cv(lambda t: 2 * math.cos(t))), ('y = 4 − |x|', cv(lambda t: 4 - abs(t)))]
ODD = [('y = x³/4', cv(lambda t: t ** 3 / 4)), ('y = 2/x', cvh(2, 0, 0)), ('y = −x', cv(lambda t: -t)), ('y = 2sin x', cv(lambda t: 2 * math.sin(t))), ('y = x/2', cv(lambda t: t / 2))]
NEITHER = [('y = (x − 1)² − 2', cv(lambda t: (t - 1) ** 2 - 2)), ('y = x + 2', cv(lambda t: t + 2)), ('y = 2ˣ − 2', cv(lambda t: 2 ** t - 2)), ('y = √(x + 3) − 1', cv(lambda t: sq_(t + 3) - 1)), ('y = |x − 2| − 1', cv(lambda t: abs(t - 2) - 1)), ('y = (x + 2)²', cv(lambda t: (t + 2) ** 2))]
INC = [('y = 2ˣ − 2', cv(lambda t: 2 ** t - 2)), ('y = x³/4', cv(lambda t: t ** 3 / 4)), ('y = x/2 + 1', cv(lambda t: t / 2 + 1)), ('y = √(x + 4) − 1', cv(lambda t: sq_(t + 4) - 1)), ('y = log₂(x + 4)', cv(lambda t: math.log2(t + 4), -4 + 1e-4, 5))]
DEC = [('y = (1/2)ˣ − 2', cv(lambda t: .5 ** t - 2)), ('y = −x³/4', cv(lambda t: -t ** 3 / 4)), ('y = 1 − x/2', cv(lambda t: 1 - t / 2)), ('y = 2 − √(x + 4)', cv(lambda t: 2 - sq_(t + 4)))]
NONM = [('y = x² − 2', cv(lambda t: t * t - 2)), ('y = |x| − 1', cv(lambda t: abs(t) - 1)), ('y = 2sin x', cv(lambda t: 2 * math.sin(t))), ('y = 3 − x²', cv(lambda t: 3 - t * t)), ('y = |x − 2| − 1', cv(lambda t: abs(t - 2) - 1))]
def f_img_parity_panels(T, rng, lv):
    kind = rng.choice(['even', 'even2', 'inc'] if lv == 1 else ['odd', 'odd2', 'dec'])
    if kind in ('even', 'even2', 'odd', 'odd2'):
        ev = kind.startswith('even'); e, o = rng.choice(EVEN), rng.choice(ODD); nn = rng.sample(NEITHER, 2)
        items = [(e, 'E'), (o, 'O'), (nn[0], 'N'), (nn[1], 'N')]; rng.shuffle(items); pick = [t for _, t in items].index('E' if ev else 'O')
        why = {'E': 'графік симетричний відносно осі y — функція парна', 'O': 'графік симетричний відносно початку координат — функція непарна', 'N': 'графік не симетричний ні відносно осі y, ні відносно початку координат — функція ні парна, ні непарна'}
        q = {'even': 'На якому з малюнків 1–4 зображено графік парної функції?', 'even2': 'Графік якої з функцій, зображених на малюнках 1–4, симетричний відносно осі y?', 'odd': 'На якому з малюнків 1–4 зображено графік непарної функції?', 'odd2': 'Графік якої з функцій, зображених на малюнках 1–4, симетричний відносно початку координат?'}[kind]
        trap = 'графік парної функції симетричний відносно осі y, непарної — відносно початку координат'
    else:
        inc = kind == 'inc'; a_, d_ = rng.choice(INC), rng.choice(DEC); nn = rng.sample(NONM, 2)
        items = [(a_, 'I'), (d_, 'D'), (nn[0], 'N'), (nn[1], 'N')]; rng.shuffle(items); pick = [t for _, t in items].index('I' if inc else 'D')
        why = {'I': 'при русі зліва направо графік увесь час іде вгору — функція зростає', 'D': 'при русі зліва направо графік увесь час іде вниз — функція спадає', 'N': 'на одних проміжках функція зростає, на інших — спадає'}
        q = f'На якому з малюнків 1–4 зображено графік функції, що {"зростає" if inc else "спадає"} на всій своїй області визначення?'
        trap = 'функція зростає, якщо більшому значенню x відповідає більше значення y: графік іде вгору при русі зліва направо' if inc else 'функція спадає, якщо більшому значенню x відповідає менше значення y: графік іде вниз при русі зліва направо'
    c = panel_canvas([it[0][1] for it in items]); img = c.save('t4_pp4_' + S.tag([it[0][0] for it in items], kind))
    wr = [(i + 1, f'на малюнку {i + 1}: {why[items[i][1]]}') for i in range(4) if i != pick]
    return T.add(lv, q + ' У відповіді вкажіть номер малюнка.', pick + 1, wr, trap, f'малюнок {pick + 1}: {why[items[pick][1]]}', img=img)

# ---------- I26: періодична ламана ----------
def f_img_periodic(T, rng, lv):
    for _ in range(500):
        Tp = rng.choice([3, 4, 4, 5, 6]); pat = [rng.randint(-2, 4) for _ in range(Tp)]
        if any(pat[i] == pat[(i + 1) % Tp] for i in range(Tp)) or len(set(pat)) < 3: continue
        if any(Tp % d == 0 and all(pat[i] == pat[i % d] for i in range(Tp)) for d in range(1, Tp)): continue
        break
    p = lambda x: pat[x % Tp]
    xmin, xmax = -3, 11
    c, ax = G(xmin, xmax, min(pat + [-1]) - 1, max(pat + [1]) + 1, 'Фрагмент графіка періодичної функції y = f(x)')
    c.poly([(ax.X(x), ax.Y(p(x))) for x in range(xmin, xmax + 1)], stroke=S.BLUE, w=2.8, close=False)
    img = c.save('t4_per_' + S.tag(pat))
    if lv == 2:
        N = rng.randint(25, 120) * rng.choice([1, 1, -1]); ans = p(N)
        wr = [(p(N + 1), 'остачу від ділення на період знайдено з помилкою на 1'), (p(N - 1), 'остачу від ділення на період знайдено з помилкою на 1'), (F(N % Tp), 'названо остачу від ділення на період, а не значення функції'), (p(0), 'f(N) замінено на f(0) без урахування остачі'), (p(abs(N) % Tp) if N < 0 else p(-N), 'знак аргументу не враховано')]
        return T.add(lv, f'Функція y = f(x) визначена на всій числовій прямій і є періодичною з найменшим додатним періодом T = {Tp}. На малюнку зображено фрагмент її графіка. Знайдіть f({fmt(N)}).', ans, wr,
                     'f(x + T) = f(x): від аргументу можна відняти (або до нього додати) будь-яку кількість періодів', f'{fmt(N)} = {Tp}·{pn((N - N % Tp) // Tp)} + {N % Tp}, тому f({fmt(N)}) = f({N % Tp}) = {fmt(ans)}', img=img)
    kind = rng.choice(['sum', 'one', 'cnt'])
    intro = 'Функція y = f(x) визначена на всій числовій прямій і є періодичною. На малюнку зображено фрагмент її графіка, що містить кілька періодів. '
    if kind == 'one':
        N = rng.randint(200, 2030); ans = p(N)
        wr = [(p(N + 1), 'остачу від ділення на період знайдено з помилкою на 1'), (p(N - 1), 'остачу від ділення на період знайдено з помилкою на 1'), (F(N % Tp), 'названо остачу від ділення на період, а не значення функції'), (p(0), 'f(N) замінено на f(0) без урахування остачі'), (p(N % (Tp + 1)), f'період визначено неправильно: {Tp + 1} замість {Tp}')]
        return T.add(lv, intro + f'Знайдіть f({N}).', ans, wr, 'спочатку за малюнком визначте період (відстань між сусідніми однаковими «фрагментами»), потім замініть аргумент остачею від ділення на період',
                     f'період T = {Tp}; {N} = {Tp}·{N // Tp} + {N % Tp}, тому f({N}) = f({N % Tp}) = {fmt(ans)}', img=img)
    if kind == 'sum':
        N1 = rng.randint(100, 999); N2 = rng.randint(100, 999); ans = p(N1) + p(-N2)
        wr = [(p(N1) + p(N2), 'для від’ємного аргументу остачу знайдено так само, як для додатного'), (p(N1) - p(-N2), 'значення віднято, а не додано'), (p(N1 + 1) + p(-N2), 'остачу для першого аргументу знайдено з помилкою на 1'), (2 * p(0), 'обидва значення замінено на f(0)'), (p(N1), 'обчислено лише перший доданок')]
        return T.add(lv, intro + f'Знайдіть f({N1}) + f(−{N2}).', ans, wr, 'визначте період за малюнком; для від’ємного аргументу додавайте періоди, доки не потрапите на зображений фрагмент',
                     f'період T = {Tp}; f({N1}) = f({N1 % Tp}) = {fmt(p(N1))}; −{N2} = {Tp}·({fmt(-((N2 + Tp - 1) // Tp))}) + {(-N2) % Tp}, тому f(−{N2}) = f({(-N2) % Tp}) = {fmt(p(-N2))}; сума {fmt(ans)}', img=img)
    L = Tp * rng.choice([10, 20, 25, 50]); v = rng.choice(sorted(set(pat))); per = sum(1 for x in range(Tp) if pat[x] == v)
    # кількість розв’язків f(x) = v на [0; L): на кожному періоді однакова; рахуємо точно через ламану одного періоду
    Vp = [(x, p(x)) for x in range(0, Tp + 1)]; sols = [t for t in pl_solve(Vp, v) if t < Tp]; ans = len(sols) * (L // Tp)
    wr = [(len(sols), 'пораховано корені лише на одному періоді'), (per * (L // Tp), 'враховано лише цілі корені') if per != len(sols) else (ans + 1, 'кінець проміжку зараховано, хоча він не входить'), (len(sols) * L, 'кількість коренів на періоді помножено на довжину проміжку, а не на кількість періодів'), (L // Tp, 'знайдено лише кількість періодів'), (ans - 1, 'один корінь пропущено')]
    return T.add(lv, intro + f'Скільки коренів має рівняння f(x) = {fmt(v)} на проміжку [0; {L})?', ans, wr, 'порахуйте корені на одному періоді й помножте на кількість періодів, що вміщуються в проміжок',
                 f'період T = {Tp}; на проміжку [0; {Tp}) рівняння має {kor(len(sols))}; періодів {L // Tp}; разом {len(sols)}·{L // Tp} = {ans}', img=img)

# ---------- I27: кусково-лінійна функція з розривом ----------
def f_img_piece(T, rng, lv):
    for _ in range(500):
        x0 = rng.randint(-6, -3); s = rng.randint(-1, 2); x2 = rng.randint(4, 6); y0, u, v, y2 = [rng.randint(-4, 5) for _ in range(4)]
        if abs(u - v) < 2 or y0 == u or v == y2: continue
        if lv == 3 and (max(min(y0, u), min(v, y2)) >= min(max(y0, u), max(v, y2))): continue   # потрібне перекриття значень
        break
    lcl = rng.random() < .5   # (s; u) зафарбована, (s; v) порожня — або навпаки
    xmin, xmax = x0 - 1, x2 + 1; ys_ = [y0, u, v, y2]
    c, ax = G(xmin, xmax, min(ys_ + [-1]) - 1, max(ys_ + [1]) + 1, 'Графік функції y = f(x)')
    ax.seg(x0, y0, s, u, col=S.BLUE, w=2.8); ax.seg(s, v, x2, y2, col=S.BLUE, w=2.8)
    ax.point(x0, y0, None, col=S.BLUE, r=4.5); ax.point(x2, y2, None, col=S.BLUE, r=4.5)
    ax.point(s, u, None, col=S.BLUE, r=5, hollow=not lcl); ax.point(s, v, None, col=S.BLUE, r=5, hollow=lcl)
    img = c.save('t4_pc_' + S.tag(x0, s, x2, y0, u, v, y2, lcl))
    intro = f'На малюнку зображено графік функції y = f(x), визначеної на відрізку [{fmt(x0)}; {fmt(x2)}]. Зафарбована точка належить графіку, порожня — ні. '
    fs = u if lcl else v; hol = v if lcl else u
    in1 = lambda t, cl=None: min(y0, u) <= t <= max(y0, u) and (t != u or (lcl if cl is None else cl))
    in2 = lambda t, cl=None: min(v, y2) <= t <= max(v, y2) and (t != v or ((not lcl) if cl is None else cl))
    crit = sorted(set(ys_))
    if lv == 1:
        V1 = [(x0, y0), (s, u)]; V2 = [(s, v), (x2, y2)]
        wr = [(hol, 'узято ординату порожньої точки, а вона не належить графіку'), (F(u + v, 2), 'узято середнє значення між двома точками'), (F(s), 'названо абсцису, а не значення функції')]
        wr += [(pl_val(V1, s - 1), f'значення прочитано в точці x = {fmt(s - 1)}'), (pl_val(V2, s + 1), f'значення прочитано в точці x = {fmt(s + 1)}')]
        wr = [w for w in wr if F(w[0]).denominator <= 2]
        return T.add(lv, intro + f'Знайдіть f({fmt(s)}).', fs, wr, 'над точкою x розташовані дві позначки: значення функції дає зафарбована точка', f'при x = {fmt(s)} зафарбована точка має ординату {fmt(fs)}, тому f({fmt(s)}) = {fmt(fs)}', img=img)
    rng_set = pred_set(lambda t: in1(t) or in2(t), crit)
    if lv == 2:
        ans = setstr(rng_set)
        wr = [(setstr(pred_set(lambda t: in1(t, True) or in2(t, True), crit)), 'ординату порожньої точки зараховано до множини значень'), (I(min(ys_), max(ys_)), 'не враховано розрив: узято весь проміжок від найменшого до найбільшого значення'),
              (I(x0, x2), 'названо область визначення (проміжок по осі x)'), (setstr(pred_set(lambda t: in1(t, False) or in2(t, False), crit)), 'ординату зафарбованої точки розриву виключено'), (setstr(toggle(rng_set)), 'дужки поставлено навпаки')]
        return T.add(lv, intro + 'Укажіть множину значень цієї функції.', ans, wr, 'спроєктуйте на вісь y кожну з двох частин графіка окремо й об’єднайте проєкції; ордината порожньої точки входить лише тоді, коли її набуває інша частина',
                     f'ліва частина дає значення від {fmt(min(y0, u))} до {fmt(max(y0, u))}, права — від {fmt(min(v, y2))} до {fmt(max(v, y2))}; з урахуванням порожньої точки E(f) = {ans}', img=img)
    k = 2; two = pred_set(lambda t: in1(t) + in2(t) == 2, crit); one = pred_set(lambda t: in1(t) + in2(t) == 1, crit)
    if not two: return False
    ans = setstr(two)
    wr = [(setstr(one), 'при таких a рівняння має рівно один корінь'), (setstr(pred_set(lambda t: in1(t, True) + in2(t, True) == 2, crit)), 'ординату порожньої точки зараховано: при цьому a один із «коренів» відповідає порожній точці'),
          (setstr(rng_set), 'названо всю множину значень функції — при таких a рівняння має хоча б один корінь'), (setstr(toggle(two)), 'кінці проміжку перевірено неправильно'), (setstr(pred_set(lambda t: in1(t, False) + in2(t, False) == 2, crit)), 'ординату зафарбованої точки розриву безпідставно виключено')]
    return T.add(lv, intro + 'Знайдіть усі значення a, при яких рівняння f(x) = a має рівно два корені.', ans, wr, 'пряма y = a має перетинати обидві частини графіка; порожня точка коренем не є, тому рівень порожньої точки перевіряйте окремо',
                 f'ліва частина набуває значень від {fmt(min(y0, u))} до {fmt(max(y0, u))}, права — від {fmt(min(v, y2))} до {fmt(max(v, y2))}; обидві частини перетинає пряма y = a при a ∈ {ans}', img=img)

# ---------- I28: графік руху ----------
def f_img_motion(T, rng, lv):
    who = rng.choice([('Велосипедист', 'виїхав', 'велосипедист', 'їхав'), ('Турист', 'вийшов', 'турист', 'йшов'), ('Автомобіль', 'виїхав', 'автомобіль', 'їхав')])
    vs = {'Велосипедист': [10, 15, 20], 'Турист': [4, 5, 6], 'Автомобіль': [40, 60, 80]}[who[0]]; unit = vs[0] // 2 if who[0] != 'Турист' else 2
    for _ in range(500):
        v1, v2 = rng.choice(vs), rng.choice(vs); t1, ts, t2 = rng.choice([1, 2]), rng.choice([1, 2]), rng.choice([1, 2]); back = lv == 2 and rng.random() < .6
        s1 = v1 * t1; s2 = s1 + v2 * t2; P = [(0, 0), (t1, s1), (t1 + ts, s1), (t1 + ts + t2, s2)]
        if back:
            tb = rng.choice([1, 2, 3]); P += [(P[-1][0] + 1, s2), (P[-1][0] + 1 + tb, 0)]
            if s2 % tb: continue
        if v1 == v2 or P[-1][0] > 8: continue
        break
    tmax = P[-1][0] + 1; ystep = {'Велосипедист': 10, 'Турист': 2, 'Автомобіль': 40}[who[0]]; smax = (s2 // ystep + 2) * ystep
    w = 440; h = min(300, 34 * smax / ystep); c = S.C(600, int(h + 86), 'Графік руху')
    ax = S.Axes(c, 80, 48, w, h, 0, tmax, 0, smax, 1, ystep, xlab='t, год', ylab='s, км')
    c.poly([(ax.X(t), ax.Y(s_)) for t, s_ in P], stroke=S.BLUE, w=2.8, close=False)
    for t, s_ in P: ax.point(t, s_, None, col=S.BLUE, r=3.5)
    img = c.save('t4_mv_' + S.tag(P))
    intro = f'{who[0]} {who[1]} з дому. На малюнку зображено графік залежності відстані s (у км) від дому від часу t (у годинах). '
    T_all = P[-1][0]
    kind = rng.choice(['stop', 'sat', 'v1'] if lv == 1 else (['avg', 'path', 'vret', 'v2'] if back else ['avg', 'v2', 'vcmp']))
    if kind == 'stop':
        stops = ts + (1 if back else 0)
        wr = [(t1, 'названо час руху до зупинки'), (t1 + ts, 'названо момент часу, коли зупинка закінчилася, а не її тривалість'), (T_all, 'названо загальний час'), (T_all - ts, 'названо час руху без зупинки'), (s1, 'названо відстань, на якій була зупинка')]
        return T.add(lv, intro + 'Скільки годин тривала зупинка?', ts, wr, 'під час зупинки відстань не змінюється — на графіку це горизонтальний відрізок; тривалість читають на осі t', f'горизонтальний відрізок графіка — від t = {t1} до t = {t1 + ts}; зупинка тривала {ts} год', img=img)
    if kind == 'sat':
        tq = T_all; ans = s2
        wr = [(s1, 'названо відстань до місця зупинки'), (s2 - s1, 'названо шлях лише після зупинки'), (T_all, 'названо час, а не відстань'), (s2 + s1, 'відстань до зупинки додано двічі'), (v2, 'названо швидкість на останній ділянці')]
        return T.add(lv, intro + f'На якій відстані (у км) від дому був {who[2]} через {tq} год після початку руху?', ans, wr, 'відстань у момент часу t — ордината точки графіка з абсцисою t', f'при t = {tq} ордината точки графіка дорівнює {s2}', img=img)
    if kind == 'v1':
        wr = [(F(s1), 'названо пройдений шлях, а не швидкість') if t1 > 1 else (F(s1) * 2, 'шлях помножено на 2'), (F(s1, t1 + ts), 'шлях поділено на час разом із зупинкою'), (F(v2), 'знайдено швидкість після зупинки'), (F(s2, T_all), 'знайдено середню швидкість за весь час'), (F(s1 * t1), 'шлях помножено на час, а не поділено'), (F(s2), 'названо відстань від дому наприкінці руху'), (F(v1 + v2), 'додано швидкості на двох ділянках руху'), (F(s2 - s1), 'названо шлях після зупинки')]
        return T.add(lv, intro + f'З якою швидкістю (у км/год) {who[2]} рухався до зупинки?', F(v1), wr, 'швидкість = шлях : час; на графіку — нахил відрізка', f'за {t1} год пройдено {s1} км: v = {s1}/{t1} = {v1} км/год', img=img)
    if kind == 'v2':
        ta = t1 + ts
        wr = [(F(s2, t2), 'поділено всю відстань від дому на час останньої ділянки'), (F(v1), 'знайдено швидкість до зупинки'), (F(s2 - s1), 'названо шлях на цій ділянці, а не швидкість') if t2 > 1 else (F(s2), 'названо відстань від дому'), (F(s2, ta + t2), 'знайдено середню швидкість від початку руху'), (F(s2 - s1, ta + t2), 'шлях ділянки поділено на весь час від початку руху')]
        return T.add(lv, intro + f'З якою швидкістю (у км/год) {who[2]} рухався після першої зупинки, віддаляючись від дому?', F(v2), wr, 'швидкість на ділянці = зміна відстані : тривалість ділянки', f'від t = {ta} до t = {ta + t2} відстань зросла з {s1} до {s2} км: v = {s2 - s1}/{t2} = {v2} км/год', img=img)
    if kind == 'vcmp':
        ans = abs(v1 - v2)
        wr = [(F(v1 + v2), 'швидкості додано'), (F(max(v1, v2)), 'названо більшу швидкість'), (F(min(v1, v2)), 'названо меншу швидкість'), (F(abs(s2 - 2 * s1)), 'порівняно шляхи, а не швидкості'), (F(max(v1, v2), min(v1, v2)), 'знайдено, у скільки разів, а не на скільки')]
        return T.add(lv, intro + f'На скільки км/год відрізняються швидкості руху до зупинки й після неї?', ans, wr, 'швидкість на ділянці = зміна відстані : тривалість ділянки; час зупинки до ділянок руху не входить',
                     f'до зупинки: {s1}/{t1} = {v1} км/год; після: {s2 - s1}/{t2} = {v2} км/год; різниця {ans} км/год', img=img)
    if kind == 'path':
        ans = 2 * s2
        wr = [(F(s2), 'враховано лише шлях від дому, без повернення'), (F(0), 'названо відстань від дому наприкінці, а не пройдений шлях'), (F(s2 + s1), 'до найбільшої відстані додано відстань до першої зупинки'), (F(2 * s2 + s1), 'відстань до зупинки додано зайвий раз'), (F(s2 * T_all), 'відстань помножено на час')]
        return T.add(lv, intro + f'Який шлях (у км) подолав {who[2]} за весь час?', ans, wr, 'графік показує відстань від дому, а не пройдений шлях: шлях туди й назад додають', f'найбільша відстань від дому {s2} км; шлях туди й назад: {s2} + {s2} = {ans} км', img=img)
    if kind == 'vret':
        ans = F(s2, tb)
        wr = [(F(s2, T_all), 'відстань поділено на весь час'), (F(v2), 'знайдено швидкість на ділянці перед поворотом'), (F(s2), 'названо відстань') if tb > 1 else (F(v1), 'знайдено швидкість на першій ділянці'), (F(2 * s2, T_all), 'знайдено середню швидкість за весь час'), (F(s2, tb + 1), 'до часу повернення додано час зупинки')]
        return T.add(lv, intro + f'З якою швидкістю (у км/год) {who[2]} повертався додому?', ans, wr, 'повернення — ділянка, на якій відстань від дому зменшується до нуля', f'відстань зменшилася з {s2} км до 0 за {tb} год: v = {s2}/{tb} = {fmt(ans)} км/год', img=img)
    if back:
        ans = F(2 * s2, T_all)
        if ans.denominator not in (1, 2, 4, 5): return False
        wr = [(F(s2, T_all), 'враховано шлях лише в один бік'), (F(2 * s2, T_all - ts - 1), 'час зупинок не враховано, а середню швидкість обчислюють за весь час'), (F(v1 + v2, 2), 'знайдено середнє арифметичне швидкостей'), (F(0), 'переміщення (0 км) поділено на час'), (F(2 * s2), 'названо шлях')]
        return T.add(lv, intro + f'Знайдіть середню швидкість (у км/год) на всьому шляху з урахуванням зупинок.', ans, wr, 'середня швидкість = увесь шлях : увесь час (разом із зупинками); це не середнє арифметичне швидкостей', f'шлях {2 * s2} км, час {T_all} год: {2 * s2}/{T_all} = {fmt(ans)} км/год', img=img)
    ans = F(s2, T_all)
    if ans.denominator not in (1, 2, 4, 5): return False
    wr = [(F(v1 + v2, 2), 'знайдено середнє арифметичне швидкостей на двох ділянках'), (F(s2, T_all - ts), 'час зупинки не враховано'), (F(s2), 'названо шлях'), (F(v1), 'названо швидкість на першій ділянці'), (F(v2), 'названо швидкість на останній ділянці')]
    return T.add(lv, intro + f'Знайдіть середню швидкість (у км/год) за весь час від початку руху, ураховуючи зупинку.', ans, wr, 'середня швидкість = увесь шлях : увесь час (разом із зупинкою); це не середнє арифметичне швидкостей', f'шлях {s2} км, час {T_all} год: {s2}/{T_all} = {fmt(ans)} км/год', img=img)

IMG_B2 = [(f_img_two, [2, 3]), (f_img_inverse, [2, 3]), (f_img_parity_half, [1, 2, 3]), (f_img_panels, [1, 2]), (f_img_parity_panels, [1, 2]), (f_img_periodic, [2, 3]), (f_img_piece, [1, 2, 3]), (f_img_motion, [1, 2])]
IMG_B1 = [(f_img_exp, [1, 2]), (f_img_log, [2, 3]), (f_img_trig, [1, 2, 3]), (f_img_hyp, [2, 3]), (f_img_transform, [2, 3]), (f_img_ap, [1, 2, 3]), (f_img_gp, [2, 3])]
FAMS = IMG_B1 + IMG_B2
IMGF = IMG_A + IMG_B1 + IMG_B2
