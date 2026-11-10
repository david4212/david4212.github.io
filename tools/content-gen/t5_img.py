import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t5 import *
from gfx import *

# ================= малюнкові родини теми 5 =================
def kor(k): return f'{k} точка' if k == 1 else (f'{k} точки' if k in (2, 3, 4) else f'{k} точок')
def sgnf(v): return (v > 0) - (v < 0)

# ---------- I1: дотична на клітинках → f′(x₀) ----------
TAN = [(F(1, 4), 2), (F(1, 4), -2), (F(1, 2), 2), (F(1, 2), -2), (F(1), 1), (F(1), -1), (F(1, 8), 4), (F(1, 8), -4), (F(1, 16), 4), (F(1, 16), -4), (F(3, 4), 2), (F(3, 4), -2), (F(1, 4), 4), (F(1, 4), -4)]
def f_img_tangent(T, rng, lv):
    for _ in range(500):
        a, dx = rng.choice(TAN); a = a * rng.choice([1, -1]); m = rng.randint(-3, 3); n = rng.randint(-3, 3); x0 = m + dx; y0 = a * dx * dx + n; k = 2 * a * dx
        ts = [t for t in (-4, -3, -2, 2, 3, 4) if (k * t).denominator == 1 and abs(x0 + t) <= 6 and abs(y0 + k * t) <= 5]
        if not ts or abs(x0) > 5 or abs(y0) > 4 or x0 == 0 or y0 == 0 or y0 == k: continue
        t = rng.choice(ts); xb, yb = x0 + t, y0 + k * t
        if yb == 0 or xb == 0: continue
        break
    else: return False
    c, ax = G(-7, 7, -6, 6, 'Графік функції y = f(x) і дотична до нього')
    ax.curve(lambda u: float(a) * (u - m) ** 2 + n, -7, 7, steps=400, w=2.8)
    ax.curve(lambda u: float(k) * (u - x0) + float(y0), -7, 7, col=S.ORANGE, w=2.2, steps=40)
    up = a > 0
    ax.point(x0, y0, 'A', dx=-4, dy=18 if up else -10); ax.point(xb, yb, 'B', dx=8, dy=-8 if k * t < 0 or not up else 16)
    img = c.save('t5_tg_' + S.tag(a, m, n, dx, t))
    intro = f'На малюнку зображено графік функції y = f(x) і дотичну до нього, проведену в точці A з абсцисою x₀ = {fmt(x0)}. Дотична проходить через точку B. '
    slope = f'дотична проходить через A({fmt(x0)}; {fmt(y0)}) і B({fmt(xb)}; {fmt(yb)}): k = ({fmt(yb)} − {pn(y0)})/({fmt(xb)} − {pn(x0)}) = {fmt(k)}, тому f′({fmt(x0)}) = {fmt(k)}'
    trap = 'значення похідної в точці дотику дорівнює кутовому коефіцієнту дотичної: f′(x₀) = k = Δy/Δx'
    b_ = y0 - k * x0
    if lv == 1:
        wr = [(-k, f'знак: дотична {"зростає" if k > 0 else "спадає"}, тому k {">" if k > 0 else "<"} 0'), (1 / k, 'поділено приріст x на приріст y, а потрібно навпаки'), (y0, 'названо значення функції f(x₀) — ординату точки A, а не похідну'), (yb - y0, 'знайдено лише приріст y, не поділено на приріст x'), (b_, 'названо ординату точки перетину дотичної з віссю y')]
        return T.add(lv, intro + f'Знайдіть f′({fmt(x0)}).', k, wr, trap, slope, img=img)
    if lv == 2:
        cc = rng.choice([2, 3, 4, -2, -3]); kind = rng.choice(['plus', 'mul', 'far'])
        if kind == 'plus':
            ans = k + cc
            wr = [(k, f'похідну доданка {fmt(cc)}x не враховано'), (F(cc), 'названо лише похідну доданка'), (y0 + cc * x0, 'обчислено значення g(x₀), а не похідну'), (k - cc, 'знак доданка змінено'), (k * cc, 'похідні перемножено замість додавання')]
            return T.add(lv, intro + f'Знайдіть значення похідної функції g(x) = f(x) {sg(cc)} {abs(cc)}x у точці x₀.', ans, wr, trap + '; похідна суми дорівнює сумі похідних', slope + f'; g′(x₀) = f′(x₀) {sg(cc)} {abs(cc)} = {fmt(ans)}', img=img)
        if kind == 'mul':
            ans = cc * k - 1
            wr = [(cc * k, 'похідну доданка −x не враховано'), (k - 1, f'сталий множник {fmt(cc)} не враховано'), (cc * k + 1, 'знак похідної доданка −x змінено'), (cc * y0 - x0, 'обчислено значення g(x₀), а не похідну'), (cc * (k - 1), 'множник застосовано до всього виразу')]
            return T.add(lv, intro + f'Знайдіть значення похідної функції g(x) = {fmt(cc)}f(x) − x у точці x₀.', ans, wr, trap + '; сталий множник виносять за знак похідної', slope + f'; g′(x₀) = {fmt(cc)}·{pn(k)} − 1 = {fmt(ans)}', img=img)
        N = x0 + rng.choice([10, 20, -10, 12]); ans = y0 + k * (N - x0)
        wr = [(k * N, 'у рівнянні дотичної не враховано вільний член'), (y0 + k * N, 'у рівнянні дотичної взято x замість x − x₀'), (y0 - k * (N - x0), 'знак кутового коефіцієнта змінено'), (k * (N - x0), 'не додано ординату точки дотику'), (F(N), 'названо абсцису')]
        return T.add(lv, intro + f'Знайдіть ординату точки дотичної з абсцисою {fmt(N)}.', ans, wr, 'рівняння дотичної: y = f(x₀) + f′(x₀)(x − x₀)', slope + f'; y = {fmt(y0)} + {pn(k)}(x {sg(-x0)} {abs(x0)}); при x = {fmt(N)}: y = {fmt(ans)}', img=img)
    kind = rng.choice(['xf', 'f2', 'fx'])
    if kind == 'xf':
        ans = y0 + x0 * k
        wr = [(k, 'похідну добутку замінено добутком похідних: 1·f′(x₀)'), (x0 * k, 'пропущено доданок u′v = f(x₀)'), (y0 - x0 * k, 'у формулі взято мінус, як для частки'), (x0 * y0, 'обчислено значення g(x₀), а не похідну'), (y0 + k, 'у другому доданку пропущено множник x₀')]
        return T.add(lv, intro + 'Знайдіть значення похідної функції g(x) = x·f(x) у точці x₀.', ans, wr, '(x·f(x))′ = f(x) + x·f′(x): потрібні і значення функції (ордината точки A), і значення похідної (нахил дотичної)', slope + f'; f(x₀) = {fmt(y0)}; g′(x₀) = {fmt(y0)} + {pn(x0)}·{pn(k)} = {fmt(ans)}', img=img)
    if kind == 'f2':
        ans = 2 * y0 * k
        wr = [(k * k, 'похідну квадрата замінено квадратом похідної'), (2 * y0, 'не помножено на похідну внутрішньої функції f′(x₀)'), (2 * k, 'замість f(x₀) взято 1'), (y0 * y0, 'обчислено значення g(x₀), а не похідну'), (y0 * k, 'пропущено множник 2')]
        return T.add(lv, intro + 'Знайдіть значення похідної функції g(x) = (f(x))² у точці x₀.', ans, wr, '((f(x))²)′ = 2f(x)·f′(x) — похідна складеної функції', slope + f'; f(x₀) = {fmt(y0)}; g′(x₀) = 2·{pn(y0)}·{pn(k)} = {fmt(ans)}', img=img)
    ans = (k * x0 - y0) / (x0 * x0)
    if ans.denominator not in (1, 2, 4, 5, 8, 10, 20, 25): return False
    wr = [(k, 'похідну частки замінено часткою похідних: f′(x₀)/1'), ((y0 - k * x0) / (x0 * x0), 'у чисельнику переплутано порядок: потрібно u′v − uv′'), ((k * x0 - y0) / x0, 'знаменник не піднесено до квадрата'), ((k * x0 + y0) / (x0 * x0), 'у чисельнику взято плюс, як для добутку'), (y0 / x0, 'обчислено значення g(x₀), а не похідну')]
    return T.add(lv, intro + 'Знайдіть значення похідної функції g(x) = f(x)/x у точці x₀.', ans, wr, '(f(x)/x)′ = (f′(x)·x − f(x))/x²', slope + f'; f(x₀) = {fmt(y0)}; g′(x₀) = ({pn(k)}·{pn(x0)} − {pn(y0)})/{fmt(x0 * x0)} = {fmt(ans)}', img=img)

# ---------- I2: графік похідної (ламана) ----------
def f_img_dgraph(T, rng, lv):
    V = gen_pl(rng, int_zeros=True, need_zero=True, nseg=(3, 5)); a, b = V[0][0], V[-1][0]; g = lambda x: pl_val(V, x)
    zs = pl_solve(V, 0); inner = [z for z in zs if a < z < b]
    lr = {z: (sgnf(g(z - F(1, 4))), sgnf(g(z + F(1, 4)))) for z in inner}
    xmax = [z for z in inner if lr[z] == (1, -1)]; xmin = [z for z in inner if lr[z] == (-1, 1)]; ext = sorted(xmax + xmin)
    c, ax = draw_pl(V, title='Графік похідної y = f′(x)', col=S.PURPLE); img = c.save('t5_dg_' + S.tag(V))
    intro = f'Функція y = f(x) визначена й диференційовна на відрізку [{fmt(a)}; {fmt(b)}]. На малюнку зображено графік її похідної y = f′(x). '
    trap0 = 'на малюнку — графік похідної, а не функції: точки екстремуму f — це нулі f′, у яких похідна змінює знак (а не вершини зображеної ламаної)'
    vert = [(x, y) for i, (x, y) in enumerate(V) if 0 < i < len(V) - 1]
    crit = sorted(set([F(a), F(b)] + zs)); pos_len = sum(q - p for p, q in zip(crit, crit[1:]) if g((p + q) / 2) > 0); neg_len = (b - a) - pos_len
    kind = rng.choice(['cnt', 'xmax', 'xmin', 'inclen', 'declen', 'slope'] if lv == 2 else ['argmax', 'argmin', 'par', 'diff', 'diff'])
    if kind == 'cnt':
        if not ext: return False
        wr = [(len(vert), 'пораховано вершини зображеної ламаної — це точки екстремуму похідної, а не функції'), (len(inner), 'пораховано всі нулі похідної, зокрема ті, де вона не змінює знака'), (len(zs), 'до нулів похідної зараховано кінці відрізка'), (len(xmax), 'пораховано лише точки максимуму'), (len(xmin), 'пораховано лише точки мінімуму'), (len(ext) + 1, 'одну точку пораховано двічі')]
        return T.add(lv, intro + f'Скільки точок екстремуму має функція f на інтервалі ({fmt(a)}; {fmt(b)})?', len(ext), wr, trap0, f'f′ змінює знак у точках x = {", ".join(fmt(z) for z in ext)} — усього {kor(len(ext))}', img=img)
    if kind in ('xmax', 'xmin'):
        lst, oth = (xmax, xmin) if kind == 'xmax' else (xmin, xmax); nm, on = ('максимуму', 'мінімуму') if kind == 'xmax' else ('мінімуму', 'максимуму')
        if not lst: return False
        ans = sum(lst); vy = max(vert, key=lambda p: p[1]) if kind == 'xmax' else min(vert, key=lambda p: p[1])
        wr = [(sum(oth), f'названо точки {on}: зміну знака похідної визначено навпаки') if oth else (F(vy[0]) + 1, 'точку прочитано неточно'), (F(vy[0]), f'названо точку, у якій похідна {"найбільша" if kind == "xmax" else "найменша"} (вершину зображеного графіка)'), (sum(ext), 'додано всі точки екстремуму'), (F(len(lst)), 'названо кількість точок, а не самі точки'), (-ans, 'знак змінено')]
        q = f'Знайдіть точку {nm} функції f.' if len(lst) == 1 else f'Знайдіть суму точок {nm} функції f.'
        return T.add(lv, intro + q, ans, wr, 'точка максимуму f — там, де f′ змінює знак з «+» на «−» (графік похідної перетинає вісь x зверху вниз); точка мінімуму — з «−» на «+»',
                     f'графік f′ перетинає вісь x {"зверху вниз" if kind == "xmax" else "знизу вгору"} при x = {", ".join(fmt(z) for z in lst)}' + (f'; сума {fmt(ans)}' if len(lst) > 1 else ''), img=img)
    if kind in ('inclen', 'declen'):
        inc = kind == 'inclen'; ans = pos_len if inc else neg_len; up_len = sum(x2 - x1 for (x1, y1), (x2, y2) in zip(V, V[1:]) if (y2 > y1) == inc)
        wr = [(neg_len if inc else pos_len, f'знайдено довжину проміжків {"спадання" if inc else "зростання"} функції'), (F(up_len), f'знайдено проміжки, де {"зростає" if inc else "спадає"} зображений графік похідної, а не функція f'), (F(b - a), 'названо довжину всього відрізка'), (F(len([1 for p, q in zip(crit, crit[1:]) if (g((p + q) / 2) > 0) == inc])), 'названо кількість проміжків, а не їхню довжину'), (ans + 1, 'довжину одного з проміжків знайдено неточно')]
        return T.add(lv, intro + f'Знайдіть сумарну довжину проміжків {"зростання" if inc else "спадання"} функції f.', ans, wr[:4], f'f {"зростає" if inc else "спадає"} там, де f′(x) {">" if inc else "<"} 0, тобто де графік похідної лежить {"вище" if inc else "нижче"} від осі x',
                     f'f′ {">" if inc else "<"} 0 на проміжках: ' + ', '.join(f'({fmt(p)}; {fmt(q)})' for p, q in zip(crit, crit[1:]) if (g((p + q) / 2) > 0) == inc) + f'; сумарна довжина {fmt(ans)}', img=img)
    if kind == 'slope':
        cand = []
        for x in range(a + 1, b):
            if any(x == vx for vx, _ in V) or g(x).denominator != 1 or g(x) == 0: continue
            (x1, y1), (x2, y2) = next((p, q) for p, q in zip(V, V[1:]) if p[0] < x < q[0]); sl = F(y2 - y1, x2 - x1)
            if sl != g(x): cand.append((x, sl))
        if not cand: return False
        x, sl = rng.choice(cand); ans = g(x)
        wr = [(sl, 'знайдено нахил зображеного графіка — це значення другої похідної, а не кутовий коефіцієнт дотичної до графіка f'), (-ans, 'знак змінено'), (F(0), 'дотичну прийнято горизонтальною'), (F(x), 'названо абсцису точки'), (1 / ans if abs(ans) != 1 else ans + 1, 'узято обернене число')]
        return T.add(lv, intro + f'Знайдіть кутовий коефіцієнт дотичної до графіка функції y = f(x) у точці з абсцисою {fmt(x)}.', ans, wr, 'кутовий коефіцієнт дотичної до графіка f дорівнює f′(x₀) — його просто читають із графіка похідної як значення (ординату)', f'за графіком f′({fmt(x)}) = {fmt(ans)}', img=img)
    if kind in ('argmax', 'argmin'):
        big = kind == 'argmax'; opts = []
        for p in range(a, b - 2):
            for q in range(p + 3, b + 1):
                cnd = sorted(set([F(p), F(q)] + [z for z in zs if p < z < q])); vals = {x: pl_int(V, p, x) for x in cnd}
                best = max(vals.values()) if big else min(vals.values()); arg = [x for x in cnd if vals[x] == best]
                if len(arg) == 1 and len(cnd) >= 3: opts.append((p, q, arg[0], cnd, vals))
        if not opts: return False
        p, q, arg, cnd, vals = rng.choice(opts)
        seg = [(x, g(x)) for x in sorted(set([F(p), F(q)] + [F(vx) for vx, _ in V if p < vx < q]))]
        dmax = max(seg, key=lambda t: t[1])[0] if big else min(seg, key=lambda t: t[1])[0]
        worst = [x for x in cnd if vals[x] == (min(vals.values()) if big else max(vals.values()))][0]
        wr = [(dmax, f'названо точку, у якій {"найбільша" if big else "найменша"} похідна, а не функція')] + [(x, 'у цій точці значення функції не є ' + ('найбільшим' if big else 'найменшим') + ': порівняйте прирости функції (площі під графіком похідної)') for x in cnd if x != arg and x != dmax]
        wr.append((F(p + q, 2), 'названо середину відрізка'))
        return T.add(lv, intro + f'У якій точці відрізка [{fmt(p)}; {fmt(q)}] функція f набуває {"найбільшого" if big else "найменшого"} значення?', arg, wr,
                     'де f′ > 0, функція зростає, де f′ < 0 — спадає; кандидати — кінці відрізка та нулі похідної; зміну функції між ними дає площа під графіком f′ (зі знаком)',
                     'зміна f від лівого кінця: ' + '; '.join(f'до x = {fmt(x)}: {fmt(v)}' for x, v in sorted(vals.items()) if x != p) + f'; {"найбільше" if big else "найменше"} значення — у точці x = {fmt(arg)}', img=img)
    if kind == 'par':
        cand = [k for k in range(-4, 6) if k != 0 and len(pl_solve(V, k)) >= 2]
        if not cand: return False
        k = rng.choice(cand); n = len(pl_solve(V, k)); m = rng.randint(-5, 5)
        wr = [(len(pl_solve(V, -k)), f'розв’язано f′(x) = {fmt(-k)}: знак кутового коефіцієнта змінено'), (len(zs), 'пораховано нулі похідної — точки, де дотична горизонтальна'), (len(pl_solve(V, m)), f'замість кутового коефіцієнта взято вільний член {fmt(m)}'), (n + 1, 'одну точку пораховано двічі'), (n - 1, 'одну точку пропущено')]
        return T.add(lv, intro + f'Скільки існує точок графіка функції y = f(x), у яких дотична до нього паралельна прямій y = {P([k, m])} або збігається з нею?', n, wr, 'дотична паралельна прямій y = kx + m, якщо f′(x₀) = k: лічіть точки перетину графіка похідної з горизонтальною прямою y = k',
                     f'пряма y = {fmt(k)} перетинає графік f′ у {kor(n).replace("точка", "точці").replace("точки", "точках").replace("точок", "точках")}: x = {", ".join(fmt(z) for z in pl_solve(V, k))}', img=img)
    opts = [(p, q) for p in range(a, b) for q in range(p + 2, b + 1) if pl_int(V, p, q).denominator in (1, 2) and pl_int(V, p, q) != g(q) - g(p)]
    if not opts: return False
    p, q = rng.choice(opts); ans = pl_int(V, p, q)
    wr = [(g(q) - g(p), 'знайдено різницю значень похідної f′(q) − f′(p), а не функції'), (pl_area(V, p, q), 'площі під і над віссю додано без урахування знака'), (-ans, 'знак змінено: потрібно f(q) − f(p)'), (g(q), 'названо значення похідної в правому кінці'), (F(q - p), 'названо довжину проміжку')]
    return T.add(lv, intro + f'Знайдіть різницю f({fmt(q)}) − f({fmt(p)}).', ans, wr, 'за формулою Ньютона — Лейбніца f(q) − f(p) дорівнює інтегралу від f′ на [p; q], тобто площі між графіком похідної та віссю x з урахуванням знака',
                 f'інтеграл від f′ на [{fmt(p)}; {fmt(q)}] (площі над віссю зі знаком «+», під віссю — зі знаком «−») дорівнює {fmt(ans)}', img=img)

# ---------- I3: гладкий графік, позначені точки ----------
def smooth(rng, ncrit):
    for _ in range(500):
        cr = sorted(rng.sample(range(-5, 6), ncrit))
        if all(b - a >= 2 for a, b in zip(cr, cr[1:])) and cr[-1] - cr[0] <= 8: break
    d = [F(1)]
    for c_ in cr: d = pmul(d, [1, -c_])
    lead = rng.choice([1, -1]); d = [lead * v for v in d]; n = len(d)
    Fc = [F(c, n - i) for i, c in enumerate(d)] + [F(0)]
    vals = [pval(Fc, c_) for c_ in cr]; lo, hi = min(vals), max(vals); k = 6.0 / (hi - lo); sh = -(lo + hi) / 2 * k + rng.choice([-.5, 0, .5])
    f = lambda x: k * pval(Fc, x) + sh; df = lambda x: k * pval(d, x)
    return cr, f, df
def f_img_marked(T, rng, lv):
    ncrit = rng.choice([2, 3, 3, 4]); cr, f, df = smooth(rng, ncrit)
    xmin, xmax = cr[0] - 2, cr[-1] + 2
    nmax = sum(1 for i, c_ in enumerate(cr) if df(c_ - .3) > 0); nmin = ncrit - nmax
    def canvas():
        c, ax = G(xmin, xmax, -5, 5, 'Графік функції y = f(x)', labels=False)
        ax.curve(f, xmin, xmax, steps=500, w=2.8)
        return c, ax
    # нулі функції у видимій частині
    zeros = sum(1 for i in range(2000) if f(xmin + (xmax - xmin) * i / 2000) * f(xmin + (xmax - xmin) * (i + 1) / 2000) < 0)
    if lv == 1:
        c, ax = canvas(); img = c.save('t5_sm_' + S.tag(cr, round(f(0), 3)))
        kind = rng.choice(['ext', 'max', 'min', 'hor'])
        ans = {'ext': ncrit, 'hor': ncrit, 'max': nmax, 'min': nmin}[kind]
        q = {'ext': 'Скільки точок екстремуму має ця функція?', 'hor': 'У скількох точках графіка дотична до нього паралельна осі x?', 'max': 'Скільки точок максимуму має ця функція?', 'min': 'Скільки точок мінімуму має ця функція?'}[kind]
        wr = [(zeros, 'пораховано нулі функції — точки перетину графіка з віссю x'), (nmin if kind == 'max' else nmax, 'пораховано точки ' + ('мінімуму' if kind == 'max' else 'максимуму')) if kind in ('max', 'min') else (nmax, 'пораховано лише точки максимуму'),
              (ncrit if kind in ('max', 'min') else nmin, 'пораховано всі точки екстремуму' if kind in ('max', 'min') else 'пораховано лише точки мінімуму'), (ans + 1, 'одну точку пораховано двічі'), (ans + 2, 'до екстремумів зараховано краї зображеної частини графіка')]
        return T.add(lv, 'На малюнку зображено графік функції y = f(x), диференційовної на всій числовій прямій. ' + q, ans, wr, 'у точці екстремуму гладкої функції дотична горизонтальна (f′ = 0): максимум — «вершина», мінімум — «западина»',
                     f'графік має {nmax} «вершин{"у" if nmax == 1 else "и"}» і {nmin} «западин{"у" if nmin == 1 else "и"}»; відповідь {ans}', img=img)
    cand = [F(t, 2) for t in range(2 * cr[0] - 2, 2 * cr[-1] + 3) if all(abs(F(t, 2) - c_) >= F(1, 2) for c_ in cr) and .5 <= abs(f(t / 2)) <= 4.6]
    for _ in range(300):
        npt = rng.choice([5, 6])
        if len(cand) < npt: return False
        pts = sorted(rng.sample(cand, npt))
        if all(b - a >= 1 for a, b in zip(pts, pts[1:])): break
    else: return False
    c, ax = canvas()
    for i, x in enumerate(pts):
        y = f(float(x)); ax.seg(float(x), 0, float(x), y, col=S.GRAY, w=1.2, dash='4 4'); ax.point(float(x), y, None, col=S.RED, r=4)
        halo(c, ax.X(float(x)), ax.Y(0) + (17 if y > 0 else -8), 'x' + '₁₂₃₄₅₆'[i], size=13, col=S.RED, bold=True)
    img = c.save('t5_mk_' + S.tag(cr, pts, round(f(0), 3)))
    names = ['x' + '₁₂₃₄₅₆'[i] for i in range(npt)]; dv = [df(float(x)) for x in pts]; fv = [f(float(x)) for x in pts]
    intro = f'На малюнку зображено графік функції y = f(x), диференційовної на всій числовій прямій, і позначено {"п’ять" if npt == 5 else "шість"} точок осі абсцис: {", ".join(names)}. '
    if lv == 2:
        kind = rng.choice(['pos', 'neg', 'big', 'small'])
        if kind in ('pos', 'neg'):
            pos = kind == 'pos'; lst = [n for n, v in zip(names, dv) if (v > 0) == pos]; ans = len(lst)
            wr = [(npt - ans, f'пораховано точки, у яких похідна {"від’ємна" if pos else "додатна"}'), (sum(1 for v in fv if (v > 0) == pos), f'пораховано точки, у яких {"додатна" if pos else "від’ємна"} сама функція (графік {"вище" if pos else "нижче"} від осі x), а не похідна'), (npt, 'пораховано всі позначені точки'), (ans + 1, 'одну точку зараховано помилково'), (ans - 1, 'одну точку пропущено')]
            return T.add(lv, intro + f'У скількох із цих точок похідна функції f {"додатна" if pos else "від’ємна"}?', ans, wr, 'знак похідної визначає напрям графіка: f′ > 0 там, де функція зростає, f′ < 0 — де спадає; розташування графіка відносно осі x тут не важить',
                         f'функція {"зростає" if pos else "спадає"} в точках {", ".join(lst) if lst else "—"}; таких точок {ans}', img=img)
        big = kind == 'big'; srt = sorted(range(npt), key=lambda i: dv[i]); best = srt[-1] if big else srt[0]; second = srt[-2] if big else srt[1]
        if abs(dv[best] - dv[second]) < 0.6 * max(1.0, abs(dv[best])) * .5: return False
        fbest = max(range(npt), key=lambda i: fv[i]) if big else min(range(npt), key=lambda i: fv[i])
        wr = [(fbest + 1, f'у цій точці {"найбільше" if big else "найменше"} значення функції, а не похідної'), (srt[0] + 1 if big else srt[-1] + 1, f'у цій точці похідна {"найменша" if big else "найбільша"}'), (second + 1, 'у цій точці графік менш крутий')]
        wr += [(i + 1, 'у цій точці похідна має інше значення: порівняйте крутизну графіка') for i in range(npt) if i not in (best, fbest, srt[0], srt[-1], second)]
        return T.add(lv, intro + f'У якій із цих точок значення похідної {"найбільше" if big else "найменше"}? У відповіді запишіть номер точки (наприклад, для x₃ — число 3).', best + 1, wr,
                     f'похідна — це кутовий коефіцієнт дотичної: {"найбільша похідна там, де графік найкрутіше піднімається" if big else "найменша похідна там, де графік найкрутіше опускається"}', f'графік найкрутіше {"зростає" if big else "спадає"} в точці {names[best]}', img=img)
    neg = rng.random() < .5; lst = [n for n, a_, b_ in zip(names, fv, dv) if (a_ * b_ < 0) == neg]; ans = len(lst)
    wr = [(npt - ans, 'пораховано точки, у яких добуток має протилежний знак'), (sum(1 for v in dv if (v < 0) == neg), 'враховано лише знак похідної'), (sum(1 for v in fv if (v < 0) == neg), 'враховано лише знак функції'), (ans + 1, 'одну точку зараховано помилково'), (ans - 1, 'одну точку пропущено')]
    return T.add(lv, intro + f'У скількох із цих точок добуток f(x)·f′(x) {"від’ємний" if neg else "додатний"}?', ans, wr, 'знак f(x) визначає положення графіка відносно осі x, знак f′(x) — зростання чи спадання; добуток від’ємний, коли знаки різні',
                 'знаки (f; f′): ' + ', '.join(f'{n}: ({"+" if a_ > 0 else "−"}; {"+" if b_ > 0 else "−"})' for n, a_, b_ in zip(names, fv, dv)) + f'; відповідь {ans}', img=img)

# ---------- I4: площа заштрихованої фігури ----------
def f_img_area(T, rng, lv):
    if lv == 2:
        kind = rng.choice(['down', 'up'])
        if kind == 'down':
            r = rng.choice([2, 3]); cc = r * r; a = rng.randint(-r, r - 1); b = rng.randint(a + 1, r); co = [-1, 0, cc]
        else:
            cc = rng.choice([1, 2]); a = rng.randint(-2, 1); b = rng.randint(a + 1, 2); co = [1, 0, cc]
        ans = integ(co, a, b); fn = lambda t: pval(co, t)
        top = max(cc, fn(a), fn(b)) + 1
        c, ax = G(-4, 4, -1, int(math.ceil(top)), None); fill_under(ax, fn, a, b); ax.curve(fn, -4, 4, steps=300, w=2.8)
        for x in (a, b): ax.seg(x, 0, x, fn(x), col=S.INK, w=1.6)
        img = c.save('t5_ar_' + S.tag(co, a, b))
        wr = [(ev(co, b) - ev(co, a) if ev(co, b) != ev(co, a) else ans + 1, 'межі підставлено в саму функцію, а не в первісну'), ((b - a) * max(ev(co, a), ev(co, b)), 'фігуру замінено прямокутником'), ((b - a) * (ev(co, a) + ev(co, b)) / 2, 'фігуру замінено трапецією: криву замінено відрізком'),
              (integ([co[0], 0, 0], a, b), 'сталий доданок не проінтегровано'), (ev(ico(co), b) + ev(ico(co), a), 'значення первісної на межах додано замість віднімання')]
        wr = [w for w in wr if w[0] > 0]
        return T.add(lv, f'На малюнку зображено графік функції y = {P(co)}. Обчисліть площу заштрихованої фігури.', ans, wr, 'площа криволінійної трапеції дорівнює інтегралу від функції; межі інтегрування читають із малюнка',
                     f'межі: x = {fmt(a)} та x = {fmt(b)}; S = ∫({P(co)})dx = ({P(ico(co))}) від {fmt(a)} до {fmt(b)} = {fmt(ans)}', img=img)
    kind = rng.choice(['line', 'hor', 'two'])
    if kind == 'line':
        p = rng.randint(-2, 0); w = rng.choice([2, 3]); q = p + w; k, b0 = p + q, -p * q; par = [1, 0, 0]; lin = [k, b0]
        f1 = lambda t: t * t; f2 = lambda t: k * t + b0; top = max(p * p, q * q) + 1
        c, ax = G(-4, 4, -1, top, None); fill_under(ax, f2, p, q, base=f1); ax.curve(f1, -4, 4, steps=300, w=2.8); ax.curve(f2, -4, 4, col=S.ORANGE, w=2.4, steps=30)
        ax.point(p, p * p, None); ax.point(q, q * q, None); img = c.save('t5_ab_' + S.tag(p, q))
        ans = F(w ** 3, 6)
        wr = [(integ(lin, p, q), 'знайдено площу під прямою без віднімання площі під параболою'), (integ(par, p, q), 'знайдено площу під параболою'), (F(w ** 3, 3), 'пропущено множник 1/2 під час інтегрування'), (integ(lin, p, q) + integ(par, p, q), 'площі додано замість віднімання'), (F(w * (p * p + q * q), 2) - integ(par, p, q) + 1, 'помилка в обчисленні')]
        return T.add(lv, f'На малюнку зображено параболу y = x² і пряму y = {P(lin)}. Обчисліть площу заштрихованої фігури.', ans, wr[:4], 'S = ∫(верхня функція − нижня)dx між абсцисами точок перетину',
                     f'точки перетину: x = {fmt(p)}, x = {fmt(q)}; S = ∫({P([-1, k, b0])})dx від {fmt(p)} до {fmt(q)} = {fmt(ans)}', img=img)
    if kind == 'hor':
        r = rng.choice([1, 2]); cc = rng.choice([0, 1]); d = cc + r * r; f1 = lambda t: t * t + cc
        c, ax = G(-4, 4, -1, d + 2, None); fill_under(ax, lambda t: d, -r, r, base=f1); ax.curve(f1, -4, 4, steps=300, w=2.8); ax.seg(-4, d, 4, d, col=S.ORANGE, w=2.4)
        ax.point(-r, d, None); ax.point(r, d, None); img = c.save('t5_ah_' + S.tag(r, cc))
        ans = F(4 * r ** 3, 3)
        wr = [(ans / 2, 'проінтегровано лише половину фігури'), (F(2 * r * d) - ans, 'знайдено площу під параболою замість площі між прямою і параболою'), (F(2 * r ** 3), 'фігуру замінено прямокутником'), (F(2 * r * d), 'знайдено площу прямокутника під прямою'), (ans * 2, 'результат подвоєно зайвий раз')]
        return T.add(lv, f'На малюнку зображено параболу y = {P([1, 0, cc])} і пряму y = {d}. Обчисліть площу заштрихованої фігури.', ans, wr, 'S = ∫(верхня − нижня)dx; фігура симетрична відносно осі y',
                     f'точки перетину: x = ±{r}; S = ∫({d} − ({P([1, 0, cc])}))dx від −{r} до {r} = {fmt(ans)}', img=img)
    r = rng.choice([1, 2]); a1 = 1; a2 = rng.choice([1, 2]) if r == 1 else 1; cc = 0; topc = (a1 + a2) * r * r
    f1 = lambda t: a1 * t * t; f2 = lambda t: -a2 * t * t + topc
    c, ax = G(-4, 4, -1, topc + 1, None); fill_under(ax, f2, -r, r, base=f1); ax.curve(f1, -4, 4, steps=300, w=2.8); ax.curve(f2, -4, 4, col=S.ORANGE, w=2.4, steps=300)
    ax.point(-r, a1 * r * r, None); ax.point(r, a1 * r * r, None); img = c.save('t5_a2_' + S.tag(r, a2))
    ans = F(4 * (a1 + a2) * r ** 3, 3)
    wr = [(ans / 2, 'проінтегровано лише половину фігури'), (integ([-a2, 0, topc], -r, r), 'знайдено площу під верхньою параболою без віднімання нижньої'), (F(2 * r * topc), 'фігуру замінено прямокутником'), (integ([a1, 0, 0], -r, r), 'знайдено площу лише під нижньою параболою'), (ans * 2, 'результат подвоєно зайвий раз')]
    return T.add(lv, f'На малюнку зображено параболи y = {P([a1, 0, 0])} та y = {P([-a2, 0, topc])}. Обчисліть площу заштрихованої фігури.', ans, wr, 'S = ∫(верхня − нижня)dx між абсцисами точок перетину',
                 f'точки перетину: x = ±{r}; S = ∫({P([-(a1 + a2), 0, topc])})dx від −{r} до {r} = {fmt(ans)}', img=img)

# ---------- I5: інтеграл від ламаної ----------
def f_img_polyint(T, rng, lv):
    for _ in range(300):
        V = gen_pl(rng, nseg=(3, 4), int_zeros=True, ylo=(0 if lv == 1 else -3), yhi=5, flat=.35)
        a, b = V[0][0], V[-1][0]; I0 = pl_int(V, a, b); A0 = pl_area(V, a, b)
        if lv == 1 and all(y >= 0 for _, y in V) and I0.denominator <= 2: break
        if lv > 1 and I0 != A0 and I0.denominator <= 2 and I0 != 0: break
    else: return False
    c, ax = draw_pl(V); img = c.save('t5_pi_' + S.tag(V))
    intro = f'На малюнку зображено графік функції y = f(x), визначеної на відрізку [{fmt(a)}; {fmt(b)}]. '
    trap = 'визначений інтеграл дорівнює площі між графіком і віссю x: частини над віссю беруть зі знаком «+», під віссю — зі знаком «−»'
    parts = [pl_int(V, x1, x2) for (x1, _), (x2, _) in zip(V, V[1:])]
    desc = 'площі частин (трапецій і трикутників) між сусідніми вершинами: ' + ', '.join(fmt(p) for p in parts)
    pos = sum(pl_int(V, p, q) for p, q in zip(sorted(set([F(a), F(b)] + pl_solve(V, 0))), sorted(set([F(a), F(b)] + pl_solve(V, 0)))[1:]) if pl_int(V, p, q) > 0)
    if lv == 1:
        wr = [(F(b - a), 'названо довжину проміжку інтегрування'), (F(max(y for _, y in V) * (b - a)), 'фігуру замінено прямокутником (найбільше значення × довжина проміжку)'), (F(V[-1][1] - V[0][1]) if V[-1][1] != V[0][1] else I0 + 1, 'знайдено різницю значень функції на кінцях'), (sum(F(y) for _, y in V), 'додано ординати вершин'), (I0 * 2, 'площі трикутників і трапецій знайдено без ділення на 2')]
        return T.add(lv, intro + f'Обчисліть інтеграл від функції f у межах від {fmt(a)} до {fmt(b)}.', I0, wr, 'функція невід’ємна, тому інтеграл дорівнює площі фігури під графіком: розбийте її на трапеції, прямокутники й трикутники', desc + f'; сума {fmt(I0)}', img=img)
    if lv == 2:
        kind = rng.choice(['int', 'area'])
        if kind == 'int':
            wr = [(A0, 'площі над і під віссю додано без урахування знака'), (pos, 'враховано лише частину графіка над віссю x'), (-I0, 'знаки частин переплутано'), (F(V[-1][1] - V[0][1]) if F(V[-1][1] - V[0][1]) != I0 else I0 + 1, 'знайдено різницю значень функції на кінцях'), (pos - A0 + pos + 1 if False else I0 * 2, 'площі знайдено без ділення на 2')]
            return T.add(lv, intro + f'Обчисліть інтеграл від функції f у межах від {fmt(a)} до {fmt(b)}.', I0, wr, trap, f'над віссю x площа {fmt(pos)}, під віссю — {fmt(A0 - pos)}; інтеграл {fmt(pos)} − {fmt(A0 - pos)} = {fmt(I0)}', img=img)
        wr = [(I0, 'обчислено інтеграл (зі знаками), а площа — сума площ усіх частин'), (pos, 'враховано лише частину над віссю x'), (A0 - pos, 'враховано лише частину під віссю x'), (abs(I0), 'узято модуль інтеграла, а не суму модулів частин') if abs(I0) != I0 else (A0 * 2, 'площі знайдено без ділення на 2'), (F(b - a), 'названо довжину проміжку')]
        return T.add(lv, intro + 'Знайдіть площу фігури, обмеженої графіком цієї функції та віссю x.', A0, wr, 'площа — це інтеграл від |f(x)|: частини під віссю x беруть зі знаком «+», а не «−»', f'над віссю x площа {fmt(pos)}, під віссю — {fmt(A0 - pos)}; разом {fmt(A0)}', img=img)
    kind = rng.choice(['F', 'lin', 'sub'])
    if kind == 'F':
        Fa = rng.randint(-5, 5); ans = Fa + I0
        wr = [(Fa + A0, 'площі над і під віссю додано без урахування знака'), (Fa - I0, 'інтеграл віднято замість додавання'), (I0, f'значення F({fmt(a)}) не враховано'), (F(Fa) + V[-1][1], 'до F(a) додано значення f(b), а не інтеграл'), (Fa + pos, 'враховано лише частину графіка над віссю')]
        return T.add(lv, intro + f'Функція F — первісна для функції f на цьому відрізку, причому F({fmt(a)}) = {fmt(Fa)}. Знайдіть F({fmt(b)}).', ans, wr, 'F(b) − F(a) дорівнює інтегралу від f на [a; b], тобто площі зі знаком', f'інтеграл від f на [{fmt(a)}; {fmt(b)}] дорівнює {fmt(I0)}; F({fmt(b)}) = {fmt(Fa)} + {pn(I0)} = {fmt(ans)}', img=img)
    if kind == 'lin':
        k = rng.choice([2, 3, -2]); m = rng.choice([1, 2, -1]); ans = k * I0 + m * (b - a)
        wr = [(k * I0 + m, f'інтеграл від сталої {fmt(m)} дорівнює {fmt(m)}·(b − a), а не {fmt(m)}'), (k * I0, 'сталий доданок не проінтегровано'), (k * A0 + m * (b - a), 'площі над і під віссю додано без урахування знака'), (I0 + m * (b - a), f'пропущено множник {fmt(k)}'), (k * (I0 + m * (b - a)), 'сталий доданок теж помножено на k')]
        return T.add(lv, intro + f'Обчисліть інтеграл від функції {fmt(k)}f(x) {sg(m)} {abs(m)} у межах від {fmt(a)} до {fmt(b)}.', ans, wr, 'лінійність інтеграла: ∫(k·f(x) + m)dx = k·∫f(x)dx + m·(b − a); сам інтеграл від f знаходять як площу зі знаком', f'інтеграл від f дорівнює {fmt(I0)}; {fmt(k)}·{pn(I0)} + {pn(m)}·{b - a} = {fmt(ans)}', img=img)
    opts = [(p, q) for p in range(a, b) for q in range(p + 2, b + 1) if (p, q) != (a, b) and pl_int(V, p, q).denominator <= 2 and pl_int(V, p, q) != pl_area(V, p, q) and pl_int(V, p, q) != 0]
    if not opts: return False
    p, q = rng.choice(opts); ans = pl_int(V, p, q)
    wr = [(pl_area(V, p, q), 'площі над і під віссю додано без урахування знака'), (I0, f'обчислено інтеграл по всьому відрізку [{fmt(a)}; {fmt(b)}]'), (-ans, 'знаки частин переплутано'), (pl_val(V, q) - pl_val(V, p), 'знайдено різницю значень функції на кінцях'), (ans * 2, 'площі знайдено без ділення на 2')]
    return T.add(lv, intro + f'Обчисліть інтеграл від функції f у межах від {fmt(p)} до {fmt(q)}.', ans, wr, trap, f'на [{fmt(p)}; {fmt(q)}] площа над віссю мінус площа під віссю дорівнює {fmt(ans)}', img=img)

# ---------- I6: графік швидкості ----------
def f_img_vgraph(T, rng, lv):
    for _ in range(400):
        n = rng.choice([3, 4]); ts = [0]
        for i in range(n): ts.append(ts[-1] + rng.choice([1, 2, 2, 3]))
        if not 6 <= ts[-1] <= 10: continue
        lo = 0 if lv < 3 else -4
        vs = [rng.choice([0, 2, 4]) if lv < 3 else rng.choice([2, 4, 6])]
        for i in range(n):
            if rng.random() < .3 and i > 0 and vs[-1] != vs[-2] and vs[-1] > 0: vs.append(vs[-1])
            else: vs.append(rng.choice([v for v in range(lo, 9, 2) if v != vs[-1]]))
        V = list(zip(ts, vs))
        if lv == 3 and (min(vs) >= 0 or any(z.denominator != 1 for z in pl_solve(V, 0)) or pl_int(V, 0, ts[-1]) == pl_area(V, 0, ts[-1])): continue
        if lv < 3 and max(vs) < 4: continue
        if pl_int(V, 0, ts[-1]).denominator == 1: break
    else: return False
    Tm = ts[-1]; ymin = min(min(vs), 0) - (2 if min(vs) < 0 else 0); ymax = max(vs) + 2
    w = 460; h = 30 * (ymax - ymin) / 2 * 1.2; c = S.C(600, int(h + 90), 'Графік швидкості')
    ax = S.Axes(c, 70, 48, w, h, 0, Tm + 1, ymin, ymax, 1, 2, xlab='t, с', ylab='v, м/с')
    c.poly([(ax.X(t), ax.Y(v)) for t, v in V], stroke=S.BLUE, w=2.8, close=False)
    for t, v in V: ax.point(t, v, None, col=S.BLUE, r=3.5)
    img = c.save('t5_vg_' + S.tag(V))
    intro = f'На малюнку зображено графік залежності швидкості v (у м/с) тіла, що рухається вздовж прямої, від часу t (у секундах) на проміжку від 0 до {Tm} с. '
    segs = list(zip(V, V[1:])); path = pl_area(V, 0, Tm); disp = pl_int(V, 0, Tm)
    if lv == 1:
        kind = rng.choice(['acc', 'vmax', 'const'])
        mov = [s_ for s_ in segs if s_[0][1] != s_[1][1]]
        if kind == 'acc':
            (t1, v1), (t2, v2) = rng.choice(mov); acc = F(v2 - v1, t2 - t1)
            wr = [(F(v2 - v1), 'знайдено зміну швидкості, не поділено на час'), (-acc, 'знак змінено: швидкість ' + ('зростає' if acc > 0 else 'спадає')), (F(v2, t2) if t2 and F(v2, t2) != acc else acc + 1, 'швидкість поділено на момент часу, а не зміну швидкості на тривалість проміжку'), (F(t2 - t1, v2 - v1), 'час поділено на зміну швидкості'), ((F(v1 + v2, 2)) * (t2 - t1), 'знайдено шлях на цьому проміжку')]
            return T.add(lv, intro + f'Знайдіть прискорення тіла (у м/с²) на проміжку часу від {t1} с до {t2} с.', acc, wr, 'прискорення — похідна швидкості: на графіку v(t) це нахил відрізка, a = Δv/Δt', f'a = ({v2} − {pn(v1)})/({t2} − {t1}) = {fmt(acc)} м/с²', img=img)
        if kind == 'vmax':
            vm = max(vs); tm = [t for t, v in V if v == vm][0]
            wr = [(F(tm), 'названо момент часу, а не швидкість'), (F(vs[-1]), 'названо швидкість наприкінці руху'), (F(vs[0]), 'названо початкову швидкість'), (F(vm + 2), 'значення прочитано з осі неточно'), (F(Tm), 'названо тривалість руху')]
            return T.add(lv, intro + 'Знайдіть найбільшу швидкість тіла (у м/с) за цей час.', vm, wr, 'найбільшу швидкість читають на вертикальній осі — це ордината найвищої точки графіка', f'найвища точка графіка: t = {tm} с, v = {vm} м/с', img=img)
        flat = [s_ for s_ in segs if s_[0][1] == s_[1][1]]
        if not flat: return False
        dur = sum(s_[1][0] - s_[0][0] for s_ in flat)
        wr = [(Tm - dur, 'знайдено час, протягом якого швидкість змінювалась'), (F(Tm), 'названо весь час руху'), (F(flat[0][0][1]), 'названо значення сталої швидкості, а не тривалість'), (F(flat[0][1][0]), 'названо момент закінчення рівномірного руху'), (dur + 1, 'проміжок прочитано неточно')]
        return T.add(lv, intro + 'Скільки секунд тіло рухалося зі сталою швидкістю?', dur, wr, 'стала швидкість — горизонтальний відрізок графіка v(t); тривалість читають на осі t', 'горизонтальні відрізки: ' + ', '.join(f'від {s_[0][0]} до {s_[1][0]} с' for s_ in flat) + f'; разом {dur} с', img=img)
    if lv == 2:
        kind = rng.choice(['path', 'sub', 'avg'])
        if kind == 'path':
            wr = [(F(max(vs) * Tm), 'найбільшу швидкість помножено на весь час'), (F(vs[-1] * Tm) if vs[-1] else F(vs[0] * Tm), 'одне зі значень швидкості помножено на весь час'), (sum(F(v) for v in vs), 'додано значення швидкості у вершинах графіка'), (path * 2, 'площі трапецій знайдено без ділення на 2'), (F(max(vs) - min(vs)), 'знайдено зміну швидкості')]
            return T.add(lv, intro + 'Знайдіть шлях (у метрах), який тіло пройшло за цей час.', path, wr, 'шлях — інтеграл від швидкості, тобто площа під графіком v(t): розбийте її на трапеції', 'площі трапецій під відрізками графіка: ' + ', '.join(fmt(pl_int(V, s_[0][0], s_[1][0])) for s_ in segs) + f'; разом {fmt(path)} м', img=img)
        if kind == 'sub':
            i = rng.randrange(1, len(V) - 1); t1, t2 = (0, V[i][0]) if rng.random() < .5 else (V[i][0], Tm); s_ = pl_int(V, t1, t2)
            wr = [(path, 'знайдено шлях за весь час руху'), (pl_val(V, t2) * (t2 - t1), 'кінцеву швидкість помножено на час'), (pl_val(V, t2) - pl_val(V, t1), 'знайдено зміну швидкості'), (s_ * 2, 'площі знайдено без ділення на 2'), (path - s_, 'знайдено шлях за решту часу')]
            return T.add(lv, intro + f'Знайдіть шлях (у метрах), який тіло пройшло за проміжок часу від {t1} с до {t2} с.', s_, wr, 'шлях за проміжок часу — площа під графіком v(t) саме над цим проміжком', f'площа під графіком від t = {t1} до t = {t2} дорівнює {fmt(s_)} м', img=img)
        avg = F(path, Tm)
        if avg.denominator not in (1, 2, 4, 5): return False
        wr = [(F(sum(vs), len(vs)), 'знайдено середнє арифметичне значень швидкості у вершинах графіка'), (F(max(vs) + min(vs), 2), 'знайдено півсуму найбільшої та найменшої швидкостей'), (F(path), 'названо шлях'), (F(vs[0] + vs[-1], 2), 'знайдено півсуму початкової та кінцевої швидкостей'), (F(max(vs)), 'названо найбільшу швидкість')]
        return T.add(lv, intro + 'Знайдіть середню швидкість тіла (у м/с) за цей час.', avg, wr, 'середня швидкість = увесь шлях : увесь час; шлях — площа під графіком v(t)', f'шлях {fmt(path)} м, час {Tm} с; середня швидкість {fmt(path)}/{Tm} = {fmt(avg)} м/с', img=img)
    kind = rng.choice(['path', 'disp', 'turn'])
    z = [t for t in pl_solve(V, 0) if 0 < t < Tm]
    if kind == 'path':
        wr = [(disp, 'знайдено переміщення: шлях у зворотному напрямі віднято, а його треба додати'), (pl_area(V, 0, z[0]) if z else path + 2, 'враховано лише рух до першої зміни напряму'), (path - abs(disp) if path - abs(disp) != 0 else path + 2, 'площі частин переплутано'), (path * 2, 'площі знайдено без ділення на 2'), (abs(disp) + path, 'до шляху додано ще й переміщення')]
        return T.add(lv, intro + 'Знайдіть шлях (у метрах), який тіло пройшло за цей час.', path, wr, 'коли v < 0, тіло рухається у зворотному напрямі; шлях — сума площ усіх частин (над і під віссю t), а переміщення — їхня різниця', f'площа над віссю {fmt((path + disp) / 2)}, під віссю {fmt((path - disp) / 2)}; шлях {fmt(path)} м', img=img)
    if kind == 'disp':
        wr = [(path, 'знайдено шлях: площі над і під віссю додано, а для зміни координати їх треба відняти'), (F((path + disp) / 2), 'враховано лише рух у додатному напрямі'), (-disp, 'знак змінено'), (F(vs[-1] - vs[0]), 'знайдено зміну швидкості'), (disp * 2, 'площі знайдено без ділення на 2')]
        return T.add(lv, intro + 'На скільки метрів змінилася координата тіла за цей час (кінцева координата мінус початкова)?', disp, wr, 'зміна координати (переміщення) — інтеграл від швидкості з урахуванням знака: площа над віссю t мінус площа під нею', f'площа над віссю {fmt((path + disp) / 2)}, під віссю {fmt((path - disp) / 2)}; зміна координати {fmt(disp)} м', img=img)
    if not z: return False
    # момент, коли тіло найдалі від початкової точки в додатному напрямі
    cand = sorted(set([F(0), F(Tm)] + z)); pos_ = {t: pl_int(V, 0, t) for t in cand}; best = max(pos_.values()); arg = [t for t in cand if pos_[t] == best]
    if len(arg) != 1 or arg[0] == 0: return False
    tv = [t for t, v in V if v == max(vs)][0]
    wr = [(F(tv), 'названо момент найбільшої швидкості, а не найбільшої координати')] + [(t, 'у цей момент координата не найбільша') for t in cand if t not in (arg[0], 0, tv)] + [(F(Tm), 'названо кінець руху'), (best, 'названо найбільшу координату, а не момент часу')]
    return T.add(lv, intro + 'У початковий момент координата тіла дорівнює нулю. У який момент часу (у секундах) координата тіла найбільша?', arg[0], wr, 'координата зростає, поки v > 0, і зменшується, коли v < 0: найбільша координата — у момент, коли швидкість змінює знак з «+» на «−» (порівняйте також із кінцем руху)',
                 'координата в моменти зміни напряму та наприкінці: ' + ', '.join(f'x({fmt(t)}) = {fmt(v)}' for t, v in sorted(pos_.items()) if t) + f'; найбільша — при t = {fmt(arg[0])} с', img=img)

# ---------- I7: знаки похідної на числовій прямій ----------
def f_img_signline(T, rng, lv):
    for _ in range(300):
        n = rng.choice([3, 4, 4, 5]); pts = sorted(rng.sample(range(-7, 9), n)); sg_ = [rng.choice([1, -1])]
        for i in range(n): sg_.append(sg_[-1] * (-1 if rng.random() < .72 else 1))
        xmax = [p for i, p in enumerate(pts) if sg_[i] > 0 > sg_[i + 1]]; xmin = [p for i, p in enumerate(pts) if sg_[i] < 0 < sg_[i + 1]]
        if xmax and xmin and len(xmax) + len(xmin) < n or (lv == 1 and xmax and xmin): break
    c = S.C(580, 130, 'Знаки похідної f′(x)'); x0, x1, y = 40, 540, 84
    c.line(x0, y, x1 + 12, y, col=S.AX, w=1.8, arrow=True); c.text(x1 + 16, y + 18, 'x', size=13, italic=True)
    X = [x0 + (x1 - x0) * (i + 1) / (n + 1) for i in range(n)]
    for i, p in enumerate(pts): c.dot(X[i], y, 5, S.INK); c.text(X[i], y + 22, fmt(p), size=14, anchor='middle', bold=True)
    edges = [x0] + X + [x1]
    for i, s_ in enumerate(sg_):
        mx = (edges[i] + edges[i + 1]) / 2; col = S.GREEN if s_ > 0 else S.RED
        c.text(mx, y - 16, '+' if s_ > 0 else '−', size=24, col=col, anchor='middle', bold=True)
    img = c.save('t5_sl_' + S.tag(pts, sg_))
    intro = 'Функція y = f(x) визначена й неперервна на всій числовій прямій. На малюнку позначено нулі її похідної та знаки похідної на кожному з утворених проміжків. '
    trap = 'точка максимуму — зміна знака f′ з «+» на «−»; точка мінімуму — з «−» на «+»; якщо знак не змінюється, екстремуму немає'
    ext = sorted(xmax + xmin); non = [p for p in pts if p not in ext]
    kind = rng.choice(['cnt', 'max', 'min'] if lv == 1 else ['summax', 'summin', 'inc', 'dec'])
    if kind == 'cnt':
        wr = [(n, 'пораховано всі нулі похідної, хоча в деяких із них знак не змінюється'), (len(xmax), 'пораховано лише точки максимуму'), (len(xmin), 'пораховано лише точки мінімуму'), (len(non), 'пораховано точки, у яких екстремуму немає'), (n + 1, 'пораховано кількість проміжків')]
        return T.add(lv, intro + 'Скільки точок екстремуму має функція f?', len(ext), wr, trap, f'знак змінюється в точках {", ".join(fmt(p) for p in ext)}; усього {len(ext)}', img=img)
    if kind in ('max', 'min', 'summax', 'summin'):
        mx = kind in ('max', 'summax'); lst, oth = (xmax, xmin) if mx else (xmin, xmax); nm = 'максимуму' if mx else 'мінімуму'
        if (kind in ('max', 'min')) != (len(lst) == 1): return False
        ans = sum(lst)
        wr = [(sum(oth), f'названо точки {"мінімуму" if mx else "максимуму"}: зміну знака прочитано навпаки')] + [(p, 'у цій точці похідна дорівнює нулю, але знака не змінює — екстремуму немає') for p in non[:1]] + [(sum(ext), 'додано всі точки екстремуму'), (sum(pts), 'додано всі нулі похідної'), (F(len(lst)), 'названо кількість точок')]
        q = f'Знайдіть точку {nm} функції f.' if len(lst) == 1 else f'Знайдіть суму точок {nm} функції f.'
        return T.add(lv, intro + q, ans, wr, trap, f'знак змінюється з {"«+» на «−»" if mx else "«−» на «+»"} у точках: {", ".join(fmt(p) for p in lst)}' + (f'; сума {fmt(ans)}' if len(lst) > 1 else ''), img=img)
    inc = kind == 'inc'; want = 1 if inc else -1
    def merged(w_):
        res = []; bnd = [None] + [F(p) for p in pts] + [None]
        for i, s_ in enumerate(sg_):
            if s_ != w_: continue
            lo, hi = bnd[i], bnd[i + 1]
            if res and res[-1][1] == lo and lo is not None: res[-1] = (res[-1][0], hi, res[-1][2], hi is not None)
            else: res.append((lo, hi, lo is not None, hi is not None))
        return res
    def unmerged(w_):
        bnd = [None] + [F(p) for p in pts] + [None]
        return [(bnd[i], bnd[i + 1], bnd[i] is not None, bnd[i + 1] is not None) for i, s_ in enumerate(sg_) if s_ == w_]
    ss = lambda parts: setstr(parts).replace(' ∪ ', ', ')
    ans = ss(merged(want))
    wr = [(ss(merged(-want)), f'записано проміжки {"спадання" if inc else "зростання"}'), (ss([(lo, hi, False, False) for lo, hi, _, _ in merged(want)]), 'кінці проміжків не включено, хоча функція неперервна в цих точках'),
          (ss(unmerged(want)), 'сусідні проміжки з однаковим знаком похідної не об’єднано: функція неперервна, тому монотонність зберігається на всьому об’єднаному проміжку'), (ss(unmerged(-want)), f'записано проміжки {"спадання" if inc else "зростання"} без об’єднання')]
    if len(merged(want)) > 1: wr.append((ss(merged(want)[:1]), 'записано лише перший із проміжків'))
    return T.add(lv, intro + f'Укажіть усі проміжки {"зростання" if inc else "спадання"} функції f.', ans, wr, f'функція {"зростає" if inc else "спадає"} там, де f′ {"≥" if inc else "≤"} 0; оскільки функція неперервна, кінці проміжків включають, а сусідні проміжки з однаковим знаком об’єднують',
                 f'знаки похідної зліва направо: {" ".join("+" if s_ > 0 else "−" for s_ in sg_)}; відповідь: {ans}', img=img)

# ---------- I8: чотири графіки — який є графіком похідної ----------
def f_img_dpanels(T, rng, lv):
    kind = rng.choice(['quad', 'quad', 'cubic'])
    if kind == 'quad':
        a = rng.choice([1, -1, F(1, 2)]); b = rng.choice([-4, -3, -2, 2, 3, 4]); cc = rng.randint(-3, 3); k = 2 * a
        items = [((k, b), None), ((k, -b), 'знак коефіцієнта b змінено'), ((-k, b), 'знак коефіцієнта при x змінено'), ((a, b), 'коефіцієнт при x² не помножено на показник 2') if a != k else None]
        items = [it for it in items if it]
        if len(items) < 4 or len(set(it[0] for it in items)) < 4: return False
        fs = f'f(x) = {P([a, b, cc])}'; ds = f'f′(x) = {P([k, b])}'
        dr = [(cv(lambda t, kk=kk, bb=bb: float(kk) * t + bb), 'y = ' + P([kk, bb]), r) for (kk, bb), r in items]
        hint = f'{ds} — пряма, що перетинає вісь y у точці {fmt(b)} і вісь x у точці {fmt(F(-b) / k)}'
    else:
        r = rng.choice([1, 2]); s = rng.choice([1, -1]); cc = rng.randint(-2, 2)      # f = s(x³/3 − r²x) + c
        fs = 'f(x) = ' + (M if s < 0 else '') + 'x³/3 ' + (M if s > 0 else '+') + f' {r * r if r > 1 else ""}x' + tail(cc); ds = 'f′(x) = ' + P([s, 0, -s * r * r])
        items = [((s, 0, -s * r * r), None), ((-s, 0, s * r * r), 'знаки змінено: гілки параболи напрямлені в протилежний бік'), ((s, 0, s * r * r), 'знак вільного члена змінено: така парабола не має нулів ±' + str(r)), ((s, -2 * s * r, s * r * r), 'побудовано (x − r)²: нуль лише один')]
        dr = [(cv(lambda t, co=co: pval(co, t)), 'y = ' + P(list(co)), rr) for co, rr in items]
        hint = f'{ds} — парабола з нулями x = ±{r}, гілки {"вгору" if s > 0 else "вниз"}'
    order = shuffled(rng, range(4)); dr = [dr[i] for i in order]; pick = order.index(0)
    c = panel_canvas([d[0] for d in dr]); img = c.save('t5_dp_' + S.tag(fs, order))
    wr = [(i + 1, f'на малюнку {i + 1} зображено графік {dr[i][1]}: {dr[i][2]}') for i in range(4) if i != pick]
    return T.add(lv, f'На якому з малюнків 1–4 зображено графік похідної функції {fs}? У відповіді вкажіть номер малюнка.', pick + 1, wr, 'спочатку знайдіть похідну за формулою, потім упізнайте її графік за нулями, напрямом і точкою перетину з віссю y', hint + f'; це малюнок {pick + 1}', img=img)

# ---------- I9: кут нахилу дотичної ----------
ANG = {30: '√3/3', 45: '1', 60: '√3', 120: '−√3', 135: '−1', 150: '−√3/3'}
def f_img_angle(T, rng, lv):
    al = rng.choice([30, 45, 60] if lv == 1 else [120, 135, 150, 120, 135, 150, 45, 60]); k = math.tan(math.radians(al))
    x0 = rng.choice([-1, 0, 1, 2]) if k > 0 else rng.choice([-2, -1, 0, 1]); y0 = rng.choice([2, 2.5, 3]); a = rng.choice([.25, .3, -.25, -.3])
    f = lambda t: a * (t - x0) ** 2 + k * (t - x0) + y0; xi = x0 - y0 / k
    c = S.C(560, 330, 'Графік функції y = f(x) і дотична до нього'); ax = S.Axes(c, 60, 46, 440, 250, -7, 7, -3, 5, 1, 1, grid=False, labels=False)
    ax.curve(f, -7, 7, steps=400, w=2.8); ax.curve(lambda t: k * (t - x0) + y0, -7, 7, col=S.ORANGE, w=2.2, steps=30)
    P0 = (ax.X(xi), ax.Y(0)); Pr = (ax.X(xi + 2), ax.Y(0)); Pu = (ax.X(x0), ax.Y(y0))
    S.angle_arc(c, P0, Pr, Pu, r=26, col=S.RED, label=f'{al}°', size=13)
    ax.point(x0, y0, 'A', dx=-18 if k > 0 else 10, dy=-8); ax.seg(x0, 0, x0, y0, col=S.GRAY, w=1.2, dash='4 4'); halo(c, ax.X(x0), ax.Y(0) + 18, 'x₀', size=13, col=S.INK, bold=True)
    img = c.save('t5_an_' + S.tag(al, x0, y0, a))
    ans = ANG[al]
    alt = {'1/2': 'це синус 30° (косинус 60°), а не тангенс', '√3/2': 'це синус 60° (косинус 30°), а не тангенс', '√2/2': 'це синус і косинус 45°, а не тангенс', '−1/2': 'це косинус 120°, а не тангенс', '−√3/2': 'це косинус 150°, а не тангенс', '−√2/2': 'це косинус 135°, а не тангенс'}
    wr = [((M + ans) if al < 90 else ans[1:], 'знак: кут ' + ('гострий, тому тангенс додатний' if al < 90 else 'тупий, тому тангенс від’ємний'))]
    comp = {30: 60, 60: 30, 120: 150, 150: 120}
    if al in comp: wr.append((ANG[comp[al]], f'це tg {comp[al]}°: значення тангенсів 30° і 60° (120° і 150°) переплутано'))
    else: wr.append((ANG[60 if al == 45 else 120], f'це tg {60 if al == 45 else 120}°'))
    sc = {30: '1/2', 45: '√2/2', 60: '√3/2', 120: '−1/2', 135: '−√2/2', 150: '−√3/2'}[al]
    wr.append((sc, alt[sc])); wr.append((ANG[45] if al not in (45, 135) else ANG[30 if al == 45 else 150], 'значення тангенса визначено неправильно'))
    wr.append((str(al) + '°', 'названо сам кут, а не його тангенс'))
    return T.add(lv, f'На малюнку зображено графік функції y = f(x) і дотичну до нього в точці A з абсцисою x₀. Дотична утворює з додатним напрямом осі x кут {al}°. Знайдіть f′(x₀).', ans, wr,
                 'геометричний зміст похідної: f′(x₀) = tg α, де α — кут між дотичною та додатним напрямом осі x; для тупого кута тангенс від’ємний', f'f′(x₀) = tg {al}° = {ans}', img=img)

# ---------- I10: задачі на оптимізацію з малюнком ----------
def f_img_optim(T, rng, lv):
    kind = rng.choice(['box', 'fence', 'rect', 'box', 'fence2'])
    if kind == 'box':
        k = rng.choice([1, 2, 3, 4, 5]); L = 6 * k; V_ = 2 * L ** 3 // 27
        c = S.C(560, 330, 'Розгортка коробки'); x0, y0, s = 150, 46, 260; q = 52
        c.rect(x0, y0, s, s, fill='#dbeafe', stroke=S.INK, sw=2)
        for (cx, cy) in ((x0, y0), (x0 + s - q, y0), (x0, y0 + s - q), (x0 + s - q, y0 + s - q)): c.rect(cx, cy, q, q, fill='#ffffff', stroke=S.RED, sw=1.6)
        c.rect(x0 + q, y0 + q, s - 2 * q, s - 2 * q, fill='none', stroke=S.GRAY, sw=1.2)
        for (cx, cy) in ((x0 + q / 2, y0 - 6), (x0 + s - q / 2, y0 - 6)): c.text(cx, cy, 'x', size=14, anchor='middle', col=S.RED, bold=True, italic=True)
        c.text(x0 - 12, y0 + q / 2 + 5, 'x', size=14, anchor='end', col=S.RED, bold=True, italic=True)
        c.line(x0, y0 + s + 16, x0 + s, y0 + s + 16, col=S.INK, w=1.3); c.text(x0 + s / 2, y0 + s + 34, f'{L} см', size=14, anchor='middle', bold=True)
        img = c.save('t5_ob_' + S.tag(L))
        ask = rng.choice(['x', 'V'])
        base = f'Із квадратного аркуша картону зі стороною {L} см по кутах вирізають однакові квадрати зі стороною x см (див. малюнок) і, загнувши краї, складають відкриту коробку. '
        sol = f'V(x) = x({L} − 2x)², 0 < x < {L // 2}; V′(x) = ({L} − 2x)({L} − 6x) = 0 ⇒ x = {k}; V = {k}·{L - 2 * k}² = {V_} см³'
        if ask == 'x':
            wr = [(F(L, 2), 'при такому x дно коробки зникає: об’єм дорівнює нулю'), (F(L, 4), 'відрізок [0; L/2] поділено навпіл замість дослідження похідної'), (F(L, 3), 'рівняння V′(x) = 0 розв’язано неправильно: L − 6x = 0 дає x = L/6'), (F(2 * k), 'подвоєно правильне значення'), (F(L - 2 * k), 'названо сторону дна коробки')]
            return T.add(lv, base + 'При якому значенні x (у см) об’єм коробки буде найбільшим?', F(k), wr, 'дно коробки — квадрат зі стороною L − 2x, висота x: V(x) = x(L − 2x)²; найбільше значення шукають за допомогою похідної', sol, img=img)
        wr = [(F(k * (L - k) ** 2), 'сторону дна знайдено як L − x замість L − 2x'), (F(L, 4) * F(L, 2) ** 2, 'узято x = L/4 без дослідження похідної'), (F(L ** 3, 27), 'пропущено множник 2 у формулі найбільшого об’єму'), (F((L - 2 * k) ** 2), 'знайдено площу дна, а не об’єм'), (F(L * L * k), 'площу всього аркуша помножено на висоту')]
        return T.add(lv, base + 'Знайдіть найбільший можливий об’єм коробки (у см³).', V_, wr, 'V(x) = x(L − 2x)²; знайдіть точку максимуму за допомогою похідної та обчисліть у ній об’єм', sol, img=img)
    if kind in ('fence', 'fence2'):
        L = rng.choice([40, 60, 80, 100, 120]) if kind == 'fence' else rng.choice([60, 120, 180, 240])
        c = S.C(560, 300, 'Ділянка біля стіни'); x0, y0, w, h = 150, 70, 260, 150
        c.rect(x0 - 50, y0 - 22, w + 100, 22, fill='#d1d5db', stroke=S.INK, sw=1.5)
        t = x0 - 46
        while t < x0 + w + 44: c.line(t, y0 - 2, t + 12, y0 - 20, col=S.GRAY, w=1.2); t += 14
        c.text(x0 + w / 2, y0 - 30, 'стіна', size=13, anchor='middle', col=S.GRAY)
        c.rect(x0, y0, w, h, fill='#dcfce7', stroke='none', sw=0)
        for (xa, ya, xb, yb) in ((x0, y0, x0, y0 + h), (x0, y0 + h, x0 + w, y0 + h), (x0 + w, y0 + h, x0 + w, y0)): c.line(xa, ya, xb, yb, col=S.GREEN, w=3.2)
        if kind == 'fence2': c.line(x0 + w / 2, y0, x0 + w / 2, y0 + h, col=S.GREEN, w=3.2)
        c.text(x0 - 12, y0 + h / 2 + 5, 'x', size=15, anchor='end', bold=True, italic=True); c.text(x0 + w / 2 + (14 if kind == 'fence2' else 0), y0 + h + 22, 'y', size=15, anchor='middle', bold=True, italic=True)
        img = c.save('t5_of_' + S.tag(kind, L))
        if kind == 'fence':
            ans = F(L * L, 8); base = f'Прямокутну ділянку, що прилягає до стіни, потрібно обгородити з трьох боків парканом завдовжки {L} м (див. малюнок). '
            ask = rng.choice(['S', 'x'])
            sol = f'2x + y = {L} ⇒ y = {L} − 2x; S(x) = x({L} − 2x); S′(x) = {L} − 4x = 0 ⇒ x = {L // 4}, y = {L // 2}; S = {fmt(ans)} м²'
            if ask == 'S':
                wr = [(F(L * L, 16), 'паркан поділено на чотири рівні сторони, ніби стіни немає (квадрат зі стороною L/4)'), (F(L * L, 9), 'паркан поділено на три рівні частини (квадрат зі стороною L/3)'), (F(L * L, 4), 'результат не поділено на 2'), (F(L, 4) * F(L, 4) * 3, 'площу обчислено з неправильними сторонами'), (F(L * L, 12), 'помилка в дослідженні функції площі')]
                return T.add(lv, base + 'Яку найбільшу площу (у м²) може мати ділянка?', ans, wr, 'уздовж стіни паркан не потрібен: 2x + y = L; площа S = xy — квадратична функція від x', sol, img=img)
            wr = [(F(L, 2), 'названо сторону y, паралельну стіні'), (F(L, 3), 'паркан поділено на три рівні частини'), (F(L, 8), 'корінь рівняння S′(x) = 0 знайдено неправильно'), (F(L, 6), 'помилка в рівнянні для похідної'), (F(L), 'названо всю довжину паркану')]
            return T.add(lv, base + 'Якою має бути довжина сторони x, перпендикулярної до стіни (у метрах), щоб площа ділянки була найбільшою?', F(L, 4), wr, 'уздовж стіни паркан не потрібен: 2x + y = L; площа S = xy — квадратична функція від x', sol, img=img)
        ans = F(L * L, 12); base = f'Прямокутну ділянку, що прилягає до стіни, обгороджують парканом із трьох боків і ділять навпіл перегородкою, перпендикулярною до стіни (див. малюнок). Загальна довжина паркану разом із перегородкою дорівнює {L} м. '
        wr = [(F(L * L, 8), 'перегородку не враховано: використано 2x + y = L'), (F(L * L, 16), 'довжину поділено на чотири рівні частини'), (F(L * L, 9), 'усі три відрізки x та сторону y взято рівними'), (F(L * L, 6), 'результат не поділено на 2'), (F(L * L, 24), 'результат поділено на 2 зайвий раз')]
        return T.add(lv, base + 'Яку найбільшу площу (у м²) може мати вся ділянка?', ans, wr, 'відрізків, перпендикулярних до стіни, тепер три: 3x + y = L; площа S = xy', f'3x + y = {L} ⇒ y = {L} − 3x; S(x) = x({L} − 3x); S′ = {L} − 6x = 0 ⇒ x = {L // 6}, y = {L // 2}; S = {fmt(ans)} м²', img=img)
    k = rng.choice([1, 2]); cc = 3 * k * k; fn = lambda t: cc - t * t; ans = 4 * k ** 3
    c, ax = G(-5, 5, -1, cc + 1, None, maxh=300); ax.curve(fn, -5, 5, steps=300, w=2.8)
    xr = 1.25 * k if k == 1 else 1.3; c.poly([(ax.X(-xr), ax.Y(0)), (ax.X(-xr), ax.Y(fn(xr))), (ax.X(xr), ax.Y(fn(xr))), (ax.X(xr), ax.Y(0))], fill='#fed7aa', stroke=S.ORANGE, w=2.2)
    ax.point(xr, fn(xr), None, col=S.ORANGE); ax.point(-xr, fn(xr), None, col=S.ORANGE)
    img = c.save('t5_or_' + S.tag(k))
    wr = [(F(2 * cc * math.isqrt(cc)) if math.isqrt(cc) ** 2 == cc else F(cc * 2), 'узято прямокутник, що спирається на нулі параболи: його висота дорівнює нулю, тому це не максимум'), (F(2 * k * cc), f'висоту прямокутника взято рівною {cc} (як у вершині параболи)'), (F(2 * k ** 3), 'ширину прямокутника взято x замість 2x'), (F(k * 2 * k * k * 2 + 2), 'помилка в обчисленні'), (F(cc * cc, 4), 'узято x = c/2 без дослідження похідної')]
    return T.add(lv, f'У фігуру, обмежену параболою y = {P([-1, 0, cc])} і віссю x, вписано прямокутник так, що дві його вершини лежать на осі x, а дві інші — на параболі (див. малюнок). Знайдіть найбільшу можливу площу такого прямокутника.', ans, wr[:3] + wr[4:],
                 'якщо права верхня вершина має абсцису x > 0, то ширина прямокутника 2x, а висота c − x²: S(x) = 2x(c − x²)', f'S(x) = 2x({cc} − x²) = {2 * cc}x − 2x³; S′(x) = {2 * cc} − 6x² = 0 ⇒ x = {k}; S = 2·{k}·({cc} − {k * k}) = {ans}', img=img)

IMGF = [(f_img_tangent, [1, 2, 3]), (f_img_dgraph, [2, 3]), (f_img_marked, [1, 2, 3]), (f_img_area, [2, 3]), (f_img_polyint, [1, 2, 3]), (f_img_vgraph, [1, 2, 3]), (f_img_signline, [1, 2]), (f_img_dpanels, [2]), (f_img_angle, [1, 2]), (f_img_optim, [3])]
FAMS = IMGF
