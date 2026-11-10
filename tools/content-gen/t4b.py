import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t4 import *

# ================= L3 =================
def sqrt_int(v):
    r = int(round(math.sqrt(v))); return r if r * r == v else None

def f_domain_hard(T, rng, lv):
    kind = rng.choice(['sqrt_frac', 'log_base', 'sqrt_cubic', 'sqrt_log', 'rat_sqrt', 'frac_log'])
    G = setstr
    if kind == 'sqrt_frac':
        r1, r2 = sorted(rng.sample(range(-6, 7), 2)); m = rng.choice([v for v in range(-7, 8) if v not in (r1, r2)])
        txt = f'y = √({poly(expand2(r1, r2))})/({poly([1, -m])})'
        conds = [(lambda x: (x - r1) * (x - r2) >= 0, f'{poly(expand2(r1, r2))} ≥ 0 (підкореневий вираз невід’ємний)'), (lambda x: x != m, f'x ≠ {fmt(m)} (знаменник не нуль)')]; crit = [r1, r2, m]
        sl = f'{poly(expand2(r1, r2))} ≥ 0 ⇒ x ≤ {fmt(r1)} або x ≥ {fmt(r2)}; x ≠ {fmt(m)}'
    elif kind == 'log_base':
        a = rng.randint(-3, 3); b = rng.randint(-6, 6)
        if a + 1 >= -b + 0 and False: return False
        txt = f'y = log_({poly([1, -a])}) ({poly([1, b])})'
        conds = [(lambda x: x - a > 0, f'{poly([1, -a])} > 0 (основа додатна)'), (lambda x: x - a != 1, f'{poly([1, -a])} ≠ 1 (основа не дорівнює 1)'), (lambda x: x + b > 0, f'{poly([1, b])} > 0 (аргумент додатний)')]; crit = [a, a + 1, -b]
        sl = f'основа: x > {fmt(a)} і x ≠ {fmt(a + 1)}; аргумент: x > {fmt(-b)}'
    elif kind == 'sqrt_cubic':
        r = sorted(rng.sample(range(-6, 7), 3)); 
        txt = f'y = √(({poly([1, -r[0]])})({poly([1, -r[1]])})({poly([1, -r[2]])}))'
        conds = [(lambda x: (x - r[0]) * (x - r[1]) * (x - r[2]) >= 0, 'добуток невід’ємний (метод інтервалів)')]; crit = r
        sl = f'метод інтервалів для ({poly([1, -r[0]])})({poly([1, -r[1]])})({poly([1, -r[2]])}) ≥ 0'
    elif kind == 'sqrt_log':
        a = rng.randint(1, 8); b = rng.randint(-6, a - 3)
        if a - (b + 1) < 1: return False
        txt = f'y = √({poly([-1, a])}) + 1/log₂({poly([1, -b])})'
        conds = [(lambda x: a - x >= 0, f'{poly([-1, a])} ≥ 0'), (lambda x: x - b > 0, f'{poly([1, -b])} > 0 (аргумент логарифма)'), (lambda x: x - b != 1, f'log₂({poly([1, -b])}) ≠ 0, тобто x ≠ {fmt(b + 1)} (знаменник не нуль)')]; crit = [a, b, b + 1]
        sl = f'x ≤ {fmt(a)}; x > {fmt(b)}; x ≠ {fmt(b + 1)}'
    elif kind == 'rat_sqrt':
        a, b = rng.sample(range(-6, 7), 2)
        txt = f'y = √(({poly([1, -a])})/({poly([1, -b])}))'
        conds = [(lambda x: x != b and (x - a) / (x - b) >= 0, f'({poly([1, -a])})/({poly([1, -b])}) ≥ 0 (знаменник не нуль)')]; crit = [a, b]
        sl = f'метод інтервалів: нуль чисельника x = {fmt(a)} (входить), нуль знаменника x = {fmt(b)} (не входить)'
    else:
        a = rng.randint(-4, 4); b = rng.randint(1, 5)
        txt = f'y = 1/√({poly([-1, a + b])}) + log₃({poly([1, -a])})'
        conds = [(lambda x: a + b - x > 0, f'{poly([-1, a + b])} > 0 (корінь у знаменнику)'), (lambda x: x - a > 0, f'{poly([1, -a])} > 0 (аргумент логарифма)')]; crit = [a, a + b]
        sl = f'x < {fmt(a + b)} і x > {fmt(a)}'
    pred = lambda x: all(c[0](x) for c in conds)
    sol = pred_set(pred, crit)
    if not sol: return False
    wr = [(G(toggle(sol)), 'кінці проміжків (дужки) визначено неправильно: строгість умов переплутано')]
    for i, (_, d) in enumerate(conds):
        pd = lambda x, i=i: all(c[0](x) for j, c in enumerate(conds) if j != i)
        s2 = pred_set(pd, crit)
        if G(s2) != G(sol): wr.append((G(s2), f'не враховано умову: {d}'))
    wr.append((G(complement(sol)), 'вказано множину, де вираз не існує'))
    return T.add(lv, f'Знайдіть область визначення функції {txt}.', G(sol), wr, 'виписуйте всі умови (корінь ≥ 0, знаменник ≠ 0, логарифм: аргумент > 0, основа > 0 і ≠ 1) і беріть їх перетин', sl)

def f_domain_param(T, rng, lv):
    m = rng.choice([1, 2, 3, 4, 5, 6]); c = m * m
    kind = rng.choice(['sqrt', 'log', 'frac'])
    if kind == 'sqrt':
        txt = f'y = √(x² + ax + {c})'; sol = [(F(-2 * m), F(2 * m), True, True)]; rule = 'підкореневий вираз має бути невід’ємним при всіх x: D ≤ 0'
        tg = 'D ≤ 0 (нестрога, бо нуль під коренем допустимий)'
        ws = [(F(-2 * m), F(2 * m), False, False), (F(-m), F(m), True, True), (None, None, False, False)]
        wr = [(setstr([ws[0]]), 'нуль під коренем допустимий, тому при D = 0 функція теж визначена (дужки квадратні)'), (setstr([ws[1]]), f'D обчислено як a² − {c} (множник 4 забули)'), (setstr(complement(sol)), 'вказано значення, при яких D > 0 (функція визначена не при всіх x)')]
    elif kind == 'log':
        txt = f'y = log₂(x² + ax + {c})'; sol = [(F(-2 * m), F(2 * m), False, False)]; rule = 'аргумент має бути додатним при всіх x: D < 0'
        tg = 'D < 0 (строга, бо аргумент логарифма не може дорівнювати нулю)'
        wr = [(setstr([(F(-2 * m), F(2 * m), True, True)]), 'при D = 0 парабола дотикається осі Ox і в одній точці аргумент дорівнює 0 — це заборонено (дужки круглі)'), (setstr([(F(-m), F(m), False, False)]), f'D обчислено як a² − {c} (множник 4 забули)'), (setstr(complement(sol)), 'вказано значення, при яких D > 0')]
    else:
        txt = f'y = 1/√(x² + ax + {c})'; sol = [(F(-2 * m), F(2 * m), False, False)]; rule = 'підкореневий вираз у знаменнику має бути додатним при всіх x: D < 0'
        tg = 'D < 0 (строга)'
        wr = [(setstr([(F(-2 * m), F(2 * m), True, True)]), 'при D = 0 у точці дотику корінь дорівнює 0, а на 0 ділити не можна (дужки круглі)'), (setstr([(F(-m), F(m), False, False)]), f'D обчислено як a² − {c} (множник 4 забули)'), (setstr(complement(sol)), 'вказано значення, при яких D > 0')]
    wr.append((setstr([(F(-4 * m), F(4 * m), sol[0][2], sol[0][3])]), 'у дискримінанті взято 16c замість 4c'))
    return T.add(lv, f'При яких значеннях параметра a область визначення функції {txt} — уся числова пряма?', setstr(sol), wr, rule, f'D = a² − {4 * c}; потрібно {tg} ⇒ a ∈ {setstr(sol)}')

def f_range_asin_bcos(T, rng, lv):
    a0, b0, r0 = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (4, 3, 5), (12, 5, 13), (8, 15, 17)])
    sa = rng.choice([1, -1]); sb = rng.choice([1, -1]); a, b = a0 * sa, b0 * sb; d = rng.randint(-5, 5)
    r = r0
    expr = f'{fmt(a) if abs(a) != 1 else ("" if a == 1 else M)}sin x {sg(b)} {abs(b)}cos x' + (f' {sg(d)} {abs(d)}' if d else '')
    ask = rng.choice(['range', 'max', 'int'])
    if ask == 'range':
        sol = [(F(d - r), F(d + r), True, True)]
        wr = [(setstr([(F(d - abs(a) - abs(b)), F(d + abs(a) + abs(b)), True, True)]), 'межі знайдено як сума модулів коефіцієнтів |a| + |b| (треба √(a² + b²))'), (setstr([(F(d - r * r), F(d + r * r), True, True)]), 'не добуто корінь: взято a² + b²'), (setstr([(F(-r), F(r), True, True)]), 'не враховано зсув ' + fmt(d)), (setstr([(F(d - max(abs(a), abs(b))), F(d + max(abs(a), abs(b))), True, True)]), 'за амплітуду взято більший з коефіцієнтів')]
        return T.add(lv, f'Знайдіть область значень функції y = {expr}.', setstr(sol), wr, 'a sin x + b cos x = √(a² + b²)·sin(x + φ), тому амплітуда √(a² + b²)', f'√({a}² + {b}²) = √{a * a + b * b} = {r}; область значень [{fmt(d - r)}; {fmt(d + r)}]') if d else T.add(lv, f'Знайдіть область значень функції y = {expr}.', setstr(sol), wr[:2] + wr[3:] + [(setstr([(F(-(abs(a) + abs(b)) // 1), F(abs(a) + abs(b)), True, True)]), 'межі знайдено як сума модулів коефіцієнтів')], 'a sin x + b cos x = √(a² + b²)·sin(x + φ), тому амплітуда √(a² + b²)', f'√({a}² + {b}²) = √{a * a + b * b} = {r}; область значень [{fmt(-r)}; {fmt(r)}]')
    if ask == 'max':
        ans = F(d + r)
        wr = [(F(d + abs(a) + abs(b)), 'амплітуду знайдено як |a| + |b|'), (F(d + r * r), 'не добуто корінь: взято a² + b²'), (F(r), 'не враховано зсув ' + fmt(d)), (F(d - r), 'знайдено найменше значення замість найбільшого')]
        if d == 0: wr[2] = (F(r + 1), 'допущено помилку в обчисленнях')
        return T.add(lv, f'Знайдіть найбільше значення функції y = {expr}.', ans, wr, 'найбільше значення = d + √(a² + b²)', f'√({a}² + {b}²) = {r}; найбільше значення {fmt(d)} + {r} = {fmt(d + r)}')
    ans = F(2 * r + 1)
    wr = [(F(2 * r), 'не враховано, що обидві межі входять'), (F(2 * r + 2), 'до кількості додано зайву межу'), (F(2 * (abs(a) + abs(b)) + 1), 'амплітуду знайдено як |a| + |b|'), (F(r + 1), 'враховано лише половину відрізка')]
    return T.add(lv, f'Скільки цілих значень набуває функція y = {expr}?', ans, wr, 'область значень — відрізок [d − r; d + r], де r = √(a² + b²)', f'r = {r}; відрізок завдовжки {2 * r}, цілих чисел {2 * r + 1}')

def f_range_quad_trig(T, rng, lv):
    kind = rng.choice(['sin2', 'cos2', 'cos2b'])
    fn = rng.choice(['sin', 'cos'])
    if kind == 'sin2':
        a = rng.choice([1, 2, -1, -2, 3]); b = rng.choice([v for v in range(-6, 7) if v]); c = rng.randint(-4, 4)
        g = lambda t: a * t * t + b * t + c
        expr = f'{fmt(a) if abs(a) != 1 else ("" if a == 1 else M)}{fn}²x {sg(b)} {abs(b) if abs(b) != 1 else ""}{fn} x' + (f' {sg(c)} {abs(c)}' if c else '')
        t0 = F(-b, 2 * a)
    elif kind == 'cos2':
        p = rng.choice([v for v in range(-6, 7) if v])
        a, b, c = -2, p, 1   # cos 2x + p sin x = 1 - 2 sin² x + p sin x
        g = lambda t: a * t * t + b * t + c
        expr = f'cos 2x {sg(p)} {abs(p) if abs(p) != 1 else ""}sin x'; fn = 'sin'; t0 = F(-b, 2 * a)
    else:
        p = rng.choice([v for v in range(-6, 7) if v])
        a, b, c = 2, p, -1   # cos 2x + p cos x = 2cos²x - 1 + p cos x
        g = lambda t: a * t * t + b * t + c
        expr = f'cos 2x {sg(p)} {abs(p) if abs(p) != 1 else ""}cos x'; fn = 'cos'; t0 = F(-b, 2 * a)
    cand = [g(F(-1)), g(F(1))] + ([g(t0)] if -1 <= t0 <= 1 else [])
    want = rng.choice(['max', 'min']); word = 'найбільше' if want == 'max' else 'найменше'
    ans = max(cand) if want == 'max' else min(cand)
    wr = []
    if -1 <= t0 <= 1: wr.append((max(g(F(-1)), g(F(1))) if want == 'max' else min(g(F(-1)), g(F(1))), 'розглянуто лише кінці відрізка t ∈ [−1; 1], вершину параболи не враховано'))
    else: wr.append((g(t0), 'взято значення у вершині параболи, але вона лежить поза відрізком t ∈ [−1; 1]'))
    wr.append((min(cand) if want == 'max' else max(cand), f'знайдено {"найменше" if want == "max" else "найбільше"} значення замість {"найбільшого" if want == "max" else "найменшого"}'))
    wr.append((g(F(0)), 'взято значення при t = 0'))
    wr.append((ans + (1 if ans + 1 not in cand else 2) if False else (g(F(1)) if ans != g(F(1)) else g(F(-1))), 'взято значення лише на одному з кінців відрізка'))
    sl = f'заміна t = {fn} x, t ∈ [−1; 1]; g(t) = {poly([a, b, c], "t")}; вершина t₀ = {ffmt(t0)} ' + ('належить' if -1 <= t0 <= 1 else 'не належить') + f' відрізку; g(−1) = {ffmt(g(F(-1)))}, g(1) = {ffmt(g(F(1)))}' + (f', g({ffmt(t0)}) = {ffmt(g(t0))}' if -1 <= t0 <= 1 else '') + f'; {word} значення {ffmt(ans)}'
    return T.add(lv, f'Знайдіть {word} значення функції y = {expr}.', ans, wr, 'зводьте до квадратичної функції від t = sin x (або cos x) з обмеженням |t| ≤ 1; перевіряйте вершину й кінці', sl)

def f_range_exp_quad(T, rng, lv):
    b = rng.choice([2, 3, 5]); p = rng.choice([v for v in range(-6, 7) if v]); c = rng.randint(-5, 8)
    t0 = F(p, 2)
    expr = f'{b * b}ˣ {sg(-p)} {abs(p) if abs(p) != 1 else ""}·{b}ˣ {sg(c)} {abs(c)}'.replace(' ·', ' ')
    expr = f'{b * b}ˣ {sg(-p)} {abs(p)}·{b}ˣ {sg(c)} {abs(c)}' if c else f'{b * b}ˣ {sg(-p)} {abs(p)}·{b}ˣ'
    g = lambda t: t * t - p * t + c
    if t0 > 0:
        lo = g(t0); sol = [(lo, None, True, False)]
        wr = [(setstr([(lo, None, False, False)]), 'вершина t₀ = ' + ffmt(t0) + ' > 0 досягається, тому значення в ній входить (дужка квадратна)'), (setstr([(F(c), None, False, False)]), 'взято значення при t → 0, а не в вершині'), (setstr([(F(c), None, True, False)]), 'взято значення g(0) = c, а не вершини'), (setstr([(F(-lo), None, True, False)]), 'знак ординати вершини змінено')]
        sl = f't = {b}ˣ > 0; g(t) = {poly([1, -p, c], "t")}; вершина t₀ = {ffmt(t0)} > 0, g(t₀) = {ffmt(lo)}; E(y) = [{ffmt(lo)}; +∞)'
    else:
        lo = F(c); sol = [(lo, None, False, False)]
        wr = [(setstr([(lo, None, True, False)]), 't = bˣ > 0, тому значення g(0) = c не досягається (дужка кругла)'), (setstr([(g(t0), None, True, False)]), 'взято значення у вершині t₀ = ' + ffmt(t0) + ', яка не належить області t > 0'), (setstr([(g(t0), None, False, False)]), 'вершина t₀ ≤ 0 не належить області t > 0'), (setstr([(F(-c), None, False, False)]), 'знак c змінено')]
        sl = f't = {b}ˣ > 0; g(t) = {poly([1, -p, c], "t")}; вершина t₀ = {ffmt(t0)} ≤ 0 лежить ліворуч від області t > 0, тому g зростає на (0; +∞): E(y) = ({c}; +∞)'
    return T.add(lv, f'Знайдіть область значень функції y = {expr}.', setstr(sol), wr, 'заміна t = aˣ > 0: вершина параболи має належати області t > 0', sl)

def f_range_misc(T, rng, lv):
    kind = rng.choice(['xk', 'abs2', 'exp', 'abs_x', 'rat', 'circ'])
    G = setstr
    if kind == 'xk':
        m = rng.choice([1, 2, 3, 4, 5]); k = m * m; pos = rng.random() < .5
        txt = f'y = x + {k}/x, x {">" if pos else "<"} 0'
        sol = [(F(2 * m), None, True, False)] if pos else [(None, F(-2 * m), False, True)]
        wr = [(G([(F(0), None, False, False)] if pos else [(None, F(0), False, False)]), 'область значень вважали всім додатним (від’ємним) променем, хоча сума має мінімум 2√k'), (G([(F(m), None, True, False)] if pos else [(None, F(-m), False, True)]), 'взято √k замість 2√k'), (G([(F(2 * k), None, True, False)] if pos else [(None, F(-2 * k), False, True)]), 'взято 2k замість 2√k'), (G([(None, F(-2 * m), False, True), (F(2 * m), None, True, False)]), 'не враховано обмеження на знак x')]
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'нерівність між середніми: x + k/x ≥ 2√k при x > 0 (рівність при x = √k)', f'x + {k}/x {"≥" if pos else "≤"} {"" if pos else M}2·√{k} = {"" if pos else M}{2 * m}')
    if kind == 'abs2':
        a, b = sorted(rng.sample(range(-8, 9), 2)); ans = b - a
        txt = f'y = |x {sg(-a)} {abs(a)}| + |x {sg(-b)} {abs(b)}|'.replace(f'|x {sg(-a)} {abs(a)}|', f'|{poly([1, -a])}|').replace(f'|x {sg(-b)} {abs(b)}|', f'|{poly([1, -b])}|')
        sol = [(F(ans), None, True, False)]
        wr = [(G([(F(0), None, True, False)]), 'вважали, що найменше значення суми модулів — 0'), (G([(F(a + b), None, True, False)]), 'найменше значення знайдено як a + b'), (G([(F(ans), None, False, False)]), 'найменше значення досягається на всьому відрізку між числами, тому дужка квадратна'), (G([(F(abs(a) + abs(b)), None, True, False)]), 'додано модулі чисел, а не знайдено відстань між ними')]
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, '|x − a| + |x − b| ≥ |a − b|; рівність — на відрізку між a і b', f'мінімум дорівнює відстані між {fmt(a)} та {fmt(b)}: {fmt(ans)}')
    if kind == 'exp':
        base = rng.choice([2, 3, 5]); txt = f'y = {base}ˣ + {base}⁻ˣ'
        sol = [(F(2), None, True, False)]
        wr = [(G([(F(0), None, False, False)]), 'сума двох додатних величин має додатну нижню межу, що не досягається? — насправді мінімум 2'), (G([(F(1), None, True, False)]), 'нижню межу взято 1'), (G([(F(2), None, False, False)]), 'мінімум 2 досягається при x = 0, тому дужка квадратна'), (G([(F(base), None, True, False)]), 'за мінімум взято основу степеня')]
        wr[0] = (G([(F(0), None, False, False)]), 'вважали, що сума може бути як завгодно близькою до 0, але вона не менша за 2 (aˣ + 1/aˣ ≥ 2)')
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 't + 1/t ≥ 2 для t > 0 (рівність при t = 1)', f'при t = {base}ˣ > 0: t + 1/t ≥ 2, мінімум 2 при x = 0; E(y) = [2; +∞)')
    if kind == 'abs_x':
        p = rng.choice([2, 4, 6, 8]); c = rng.randint(-5, 8)
        txt = f'y = x² {sg(-p)} {p}|x| {sg(c)} {abs(c)}' if c else f'y = x² − {p}|x|'
        m = p // 2; lo = c - m * m
        sol = [(F(lo), None, True, False)]
        wr = [(G([(F(c), None, True, False)]), 'взято значення при x = 0, а не мінімум при |x| = ' + str(m)), (G([(F(-lo), None, True, False)]), 'знак мінімуму змінено'), (G([(F(c - p * p), None, True, False)]), f'у вершині взято (p)² замість (p/2)²'), (G([(F(lo), None, False, False)]), 'мінімум досягається, тому дужка квадратна')]
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'заміна t = |x| ≥ 0: x² = t², вершина t₀ = p/2 > 0 досягається', f't = |x| ≥ 0; y = t² − {p}t {sg(c)} {abs(c)}; вершина t₀ = {m}, y = {fmt(lo)}')
    if kind == 'rat':
        txt = 'y = (x² − 1)/(x² + 1)'
        sol = [(F(-1), F(1), True, False)]
        wr = [(G([(F(-1), F(1), True, True)]), 'значення 1 не досягається (дріб строго менший за 1)'), (G([(F(-1), F(1), False, False)]), 'значення −1 досягається при x = 0'), (G([(F(0), F(1), True, False)]), 'не враховано, що чисельник може бути від’ємним'), (G([(None, None, False, False)]), 'значення дробу обмежені')]
        return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'виділіть ціле: (x² − 1)/(x² + 1) = 1 − 2/(x² + 1)', 'y = 1 − 2/(x² + 1); x² + 1 ≥ 1 ⇒ 0 < 2/(x² + 1) ≤ 2 ⇒ −1 ≤ y < 1')
    m = rng.choice([2, 3, 4, 5, 6])
    txt = f'y = √({m * m} − x²)'
    sol = [(F(0), F(m), True, True)]
    wr = [(G([(F(-m), F(m), True, True)]), 'значення кореня невід’ємні, тому нижня межа 0'), (G([(F(0), F(m * m), True, True)]), f'не добуто корінь з {m * m}'), (G([(F(0), F(m), True, False)]), 'значення m досягається при x = 0, тому дужка квадратна'), (G([(F(0), None, True, False)]), 'не враховано обмеження зверху: x² ≥ 0')]
    return T.add(lv, f'Знайдіть область значень функції {txt}.', G(sol), wr, 'область визначення [−m; m]; найбільше значення кореня при x = 0', f'0 ≤ x² ≤ {m * m} ⇒ 0 ≤ {m * m} − x² ≤ {m * m} ⇒ 0 ≤ y ≤ {m}')

def f_param_quad(T, rng, lv):
    kind = rng.choice(['min', 'noroot', 'one', 'vtx_line'])
    if kind == 'min':
        m = rng.randint(1, 6); c = rng.randint(1, 12); n_ = c - m * m
        a = 2 * m
        txt = f'При якому додатному значенні a найменше значення функції y = x² + ax + {c} дорівнює {fmt(n_)}?'
        ans = F(a)
        wr = [(F(m), 'з рівності c − a²/4 = n одержано a² = 4(c − n), але корінь знайдено без множника 2 (a = √(c − n) замість 2√(c − n))'), (F(a * a), 'знайдено a² замість a'), (F(4 * m), 'у формулі найменшого значення c − a²/4 взято a² замість a²/4'), (F(-a), 'за умовою a має бути додатним')]
        return T.add(lv, txt, ans, wr, 'найменше значення x² + ax + c дорівнює c − a²/4', f'c − a²/4 = {fmt(n_)} ⇒ a² = 4·({c} − {pn(n_)}) = {4 * m * m} ⇒ a = {a} (a > 0)')
    m = rng.randint(1, 7); c = m * m
    if kind == 'noroot':
        sol = [(F(-2 * m), F(2 * m), False, False)]
        wr = [(setstr([(F(-2 * m), F(2 * m), True, True)]), 'при D = 0 парабола дотикається осі Ox, тобто має спільну точку (дужки круглі)'), (setstr(complement(sol)), 'вказано значення, при яких парабола перетинає вісь Ox'), (setstr([(F(-m), F(m), False, False)]), f'D обчислено як a² − {c}'), (setstr([(F(-2 * m), F(2 * m), True, False)]), 'один із кінців додано помилково')]
        return T.add(lv, f'При яких значеннях a парабола y = x² + ax + {c} не має спільних точок з віссю Ox?', setstr(sol), wr, 'немає спільних точок ⇔ D < 0', f'D = a² − {4 * c} < 0 ⇒ a ∈ ({-2 * m}; {2 * m})'.replace('(-', '(−'))
    if kind == 'one':
        ans = F(2 * m)
        wr = [(F(m), 'D = a² − 4c прирівняно до нуля неправильно (a = √c замість a = 2√c)'), (F(4 * m), 'у дискримінанті взято 16c'), (F(c), 'знайдено c, а не додатне значення a'), (F(-2 * m), 'за умовою a має бути додатним')]
        return T.add(lv, f'При якому додатному значенні a парабола y = x² + ax + {c} має з віссю Ox рівно одну спільну точку?', ans, wr, 'одна спільна точка (дотик) ⇔ D = 0', f'D = a² − {4 * c} = 0 ⇒ a = ±{2 * m}; додатне a = {2 * m}')
    k = rng.choice([1, 2, 3]); mm = rng.randint(1, 4); s_ = rng.choice([1, -1])
    # парабола y = x² - 2a x + c, вершина (a; c - a²) лежить на прямій y = k x - ... : підставимо
    c = rng.randint(2, 12); b0 = rng.randint(-4, 4)
    # вершина (a, c - a^2), пряма y = k x + b0 :  c - a^2 = k a + b0  => a^2 + k a + b0 - c = 0
    D = k * k - 4 * (b0 - c)
    r = sqrt_int(D)
    if r is None: return False
    a1, a2 = F(-k + r, 2), F(-k - r, 2)
    if a1.denominator != 1 or a1 == a2: return False
    ans = max(a1, a2)
    wr = [(min(a1, a2), 'названо менший розв’язок замість більшого'), (a1 + a2, 'знайдено суму значень a (за Вієтом)'), (a1 * a2, 'знайдено добуток значень a'), (F(c - b0), 'знайдено вільний член квадратного рівняння')]
    return T.add(lv, f'Вершина параболи y = x² − 2ax + {c} лежить на прямій y = {poly([k, b0])}. Знайдіть більше з можливих значень a.', ans, wr, 'вершина (a; c − a²): підставте в рівняння прямої', f'вершина ({fmt(ans)}; …): {c} − a² = {k}a {sg(b0)} {abs(b0)} ⇒ a² {sg(k)} {abs(k)}a {sg(b0 - c)} {abs(b0 - c)} = 0 ⇒ a = {fmt(a1)} або a = {fmt(a2)}; більше — {fmt(ans)}')

def f_parity_param(T, rng, lv):
    kind = rng.choice(['even', 'odd', 'prod', 'sumodd'])
    k = rng.randint(1, 6)
    if kind == 'even':
        sgn = rng.choice([1, -1])
        txt = f'При якому значенні a функція f(x) = x² + (a {sg(-sgn * k)} {k})x + 5 є парною?'.replace(f'(a {sg(-sgn * k)} {k})', f'(a {"−" if sgn > 0 else "+"} {k})')
        ans = F(sgn * k)
        wr = [(F(-sgn * k), 'знак розв’язку змінено'), (F(0), 'вважали, що коефіцієнт при x має дорівнювати a, а не a ∓ k'), (F(5), 'за a узято вільний член'), (F(2 * sgn * k), 'коефіцієнт при x прирівняно до числа, що відрізняється від нуля')]
        return T.add(lv, txt, ans, wr, 'парна многочленна функція не має доданків з непарними степенями x', f'доданок з x має зникнути: a {"−" if sgn > 0 else "+"} {k} = 0 ⇒ a = {fmt(ans)}')
    if kind == 'odd':
        sgn = rng.choice([1, -1])
        txt = f'При якому значенні a функція f(x) = x³ + (a {"+" if sgn > 0 else "−"} {k})x² + x є непарною?'
        ans = F(-sgn * k)
        wr = [(F(sgn * k), 'знак розв’язку змінено'), (F(0), 'вважали, що коефіцієнт при x² має дорівнювати a, а не a ± k'), (F(1), 'за a узято коефіцієнт при x'), (F(2 * k), 'розв’язок подвоєно')]
        return T.add(lv, txt, ans, wr, 'непарна функція не має доданків з парними степенями x (крім відсутнього вільного члена)', f'доданок з x² має зникнути: a {"+" if sgn > 0 else "−"} {k} = 0 ⇒ a = {fmt(ans)}')
    if kind == 'prod':
        txt = f'Знайдіть добуток усіх значень a, при яких функція f(x) = x⁴ + (a² − {k * k})x³ + 7 є парною.'
        ans = F(-k * k)
        wr = [(F(k * k), 'знайдено суму квадратів, а не добуток коренів a = ±' + str(k)), (F(0), 'вважали, що значення a симетричні і їх сума (а не добуток) дорівнює 0'), (F(k), 'знайдено лише додатне значення a'), (F(-k), 'знайдено лише від’ємне значення a')]
        return T.add(lv, txt, ans, wr, 'доданок з x³ має зникнути: a² − k² = 0 дає два значення a', f'a² − {k * k} = 0 ⇒ a = ±{k}; добуток {k}·(−{k}) = {-k * k}')
    txt = f'Знайдіть суму всіх значень a, при яких функція f(x) = x³ + (a² − {k + 2}a + {2 * k + 1 if False else 0}) x² + x є непарною.'
    # a² − p a + q = 0, корені r1, r2 цілі
    r1, r2 = rng.sample(range(-5, 8), 2)
    txt = f'Знайдіть суму всіх значень a, при яких функція f(x) = x³ + ({poly([1, -(r1 + r2), r1 * r2], "a")})x² + x є непарною.'
    ans = F(r1 + r2)
    wr = [(F(r1 * r2), 'знайдено добуток коренів замість суми'), (F(-(r1 + r2)), 'за Вієтом сума дорівнює −b, але знак узято протилежно'), (F(0), 'вважали, що значення a симетричні'), (F(abs(r1) + abs(r2)), 'додано модулі коренів')]
    return T.add(lv, txt, ans, wr, 'коефіцієнт при x² має дорівнювати нулю; за теоремою Вієта сума коренів = −b', f'{poly([1, -(r1 + r2), r1 * r2], "a")} = 0 ⇒ a = {fmt(r1)} або a = {fmt(r2)}; сума {fmt(r1 + r2)}')

def f_period_hard(T, rng, lv):
    kind = rng.choice(['frac', 'tg_sin', 'prod', 'sqdiff', 'sum3'])
    if kind == 'frac':
        a, b = rng.sample([2, 3, 4, 5, 6], 2); f1, f2 = rng.choice(['sin', 'cos']), rng.choice(['sin', 'cos'])
        t1, t2 = F(2 * a), F(2 * b); ans = lcmF(t1, t2)
        txt = f'y = {f1}(x/{a}) + {f2}(x/{b})'
        wr = [(t1 + t2, 'періоди доданків додано'), (t1 * t2 / 2 if False else t1 * t2, 'періоди доданків перемножено'), (max(t1, t2), 'взято більший з періодів, не перевіряючи кратності'), (F(2) * lcmF(a, b) * 2 if False else F(2) * (a * b), f'взято 2π·{a}·{b} (добуток замість НСК)')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, 'T(sin(x/a)) = 2πa; період суми — НСК періодів доданків', f'T₁ = {pim(t1)}, T₂ = {pim(t2)}; НСК = {pim(ans)}')
    if kind == 'tg_sin':
        a, b = rng.sample([2, 3, 4, 5], 2)
        t1, t2 = F(1, a), F(2, b); ans = lcmF(t1, t2)
        txt = f'y = tg({a}x) + sin({b}x)'
        wr = [(t1 + t2, 'періоди доданків додано'), (min(t1, t2), 'взято менший з періодів'), (t1 * t2, 'періоди доданків перемножено'), (F(2), 'взято 2π, не враховано коефіцієнти')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, 'T(tg kx) = π/k, T(sin kx) = 2π/k; період суми — НСК', f'T₁ = π/{a} = {pim(t1)}, T₂ = 2π/{b} = {pim(t2)}; НСК = {pim(ans)}')
    if kind == 'prod':
        k = rng.choice([1, 2, 3, 4]); ans = F(1, k)
        txt = f'y = sin({k}x)·cos({k}x)' if k > 1 else 'y = sin x·cos x'
        wr = [(F(2, k), f'взято період функції sin({k}x) або cos({k}x), а добуток — це sin({2 * k}x)/2'), (F(1, 2 * k), 'період поділено ще й на 2'), (F(4, k), 'період подвоєно'), (F(1), 'коефіцієнт при x не враховано')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, 'sin t·cos t = sin(2t)/2: період зменшується вдвічі', f'sin({k}x)cos({k}x) = sin({2 * k}x)/2; T = 2π/{2 * k} = {pim(ans)}')
    if kind == 'sqdiff':
        k = rng.choice([1, 2, 3]); ans = F(1, k)
        txt = f'y = cos²({k}x) − sin²({k}x)' if k > 1 else 'y = cos²x − sin²x'
        wr = [(F(2, k), 'взято період cos(kx) без урахування формули подвійного кута'), (F(1, 2 * k), 'період поділено ще й на 2'), (F(4, k), 'період подвоєно'), (F(1), 'коефіцієнт при x не враховано')]
        wr = [(pim(v), r) for v, r in wr]
        return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, 'cos²t − sin²t = cos 2t', f'вираз = cos({2 * k}x); T = 2π/{2 * k} = {pim(ans)}')
    a, b, c = rng.sample([1, 2, 3, 4, 6], 3)
    ts = [F(2, a), F(2, b), F(2, c)]; ans = lcmF(lcmF(ts[0], ts[1]), ts[2])
    txt = f'y = sin({a}x) + cos({b}x) + sin({c}x)'.replace('(1x)', ' x').replace('sin( x)', 'sin x')
    txt = f'y = sin {"" if a == 1 else a}x + cos {"" if b == 1 else b}x + sin {"" if c == 1 else c}x'
    wr = [(sum(ts), 'періоди доданків додано'), (max(ts), 'взято найбільший період, не перевіряючи кратності'), (min(ts), 'взято найменший період'), (ts[0] * ts[1], 'перемножено два з періодів')]
    wr = [(pim(v), r) for v, r in wr]
    return T.add(lv, f'Знайдіть найменший додатний період функції {txt}.', pim(ans), wr, 'період суми кількох періодичних функцій — НСК їх періодів', f'T = {", ".join(pim(t) for t in ts)}; НСК = {pim(ans)}')

def poly_compose(f, g):
    res = [F(0)]
    for c in f:
        # res = res*g + c
        new = [F(0)] * (len(res) + len(g) - 1)
        for i, a in enumerate(res):
            for j, b in enumerate(g): new[i + j] += a * b
        new[-1] += c
        res = new
    while len(res) > 1 and res[0] == 0: res = res[1:]
    return res

def f_composite_hard(T, rng, lv):
    kind = rng.choice(['inner', 'inner', 'poly', 'ff'])
    if kind == 'inner':
        al = rng.choice([1, 2, -1]); be = rng.randint(-4, 4); ga = rng.randint(-5, 5); k = rng.choice([2, 3, -2, -1]); m = rng.randint(-3, 3)
        fco = [al, be, ga]
        h = [int(v) for v in poly_compose(fco, [k, m])]
        t0 = rng.randint(-4, 6); x0 = F(t0 - m, k)
        if x0.denominator != 1: return False
        ans = ev(fco, t0)
        wr = [(ev(h, t0), f'у вираз для f({poly([k, m])}) підставлено x = {t0}, але {poly([k, m])} = {t0} ⇒ x = {fmt(x0)}'), (ev(h, -x0), 'значення x знайдено з протилежним знаком'), (ev(h, t0 - m), 'x знайдено як t − m, а не (t − m)/k'), (ev(h, F(t0 + m, k)), 'при розв’язуванні kx + m = t знак m змінено')]
        return T.add(lv, f'Відомо, що f({poly([k, m])}) = {poly(h)}. Знайдіть f({t0}).', ev(h, x0), wr, 'f(kx + m): знайдіть x, при якому kx + m дорівнює потрібному аргументу', f'{poly([k, m])} = {t0} ⇒ x = {fmt(x0)}; f({t0}) = {fmt(ev(h, x0))}')
    if kind == 'poly':
        al = rng.choice([1, 2, -1]); be = rng.randint(-4, 4); ga = rng.randint(-5, 5); k = rng.choice([2, 3, -1, -2]); m = rng.choice([v for v in range(-4, 5) if v])
        fg = [al * k * k, 2 * al * k * m + be * k, al * m * m + be * m + ga]
        gf = [int(v) for v in poly_compose([k, m], [al, be, ga])]
        wr = [(ys(*gf), 'композицію записано у зворотному порядку: g(f(x)) замість f(g(x))'), (ys(al * k * k, be * k, al * m * m + be * m + ga), 'у квадраті суми загублено подвоєний добуток'), (ys(al * k, 2 * al * k * m + be * k, al * m * m + be * m + ga), 'множник k при x не піднесено до квадрата'), (ys(al * k * k, 2 * al * k * m + be * k, al * m * m - be * m + ga), 'у доданку β·g(x) вільний член m взято з протилежним знаком')]
        return T.add(lv, f'Нехай f(x) = {poly([al, be, ga])}, g(x) = {poly([k, m])}. Знайдіть формулу функції y = f(g(x)).', ys(*fg), wr, 'f(g(x)): підставте вираз g(x) замість x у f і розкрийте дужки (квадрат суми!)', f'f(g(x)) = {fmt(al)}·({poly([k, m])})² {sg(be)} {abs(be)}·({poly([k, m])}) {sg(ga)} {abs(ga)} = {poly(fg)}')
    k = rng.choice([2, 3, -1, -2]); b = rng.choice([v for v in range(-3, 4) if v]); x0 = rng.randint(-3, 4); n2 = rng.randint(2, 4)
    chain = [x0]
    for _ in range(n2): chain.append(k * chain[-1] + b)
    val = chain[-1]
    wr = [(k ** n2 * x0 + b, 'вільний член додано лише раз'), (k * n2 * x0 + n2 * b, 'композицію замінено множенням на n'), (k * val + b, 'виконано ще один крок композиції'), (chain[-2], 'виконано на один крок менше')]
    return T.add(lv, f'Нехай f(x) = {poly([k, b])}. Знайдіть значення, яке дає {n2}-кратне застосування функції f до числа {x0}, тобто f(f(…f({x0})…)) ({n2} разів).', val, wr, 'обчислюйте послідовно: x₁ = f(x₀), x₂ = f(x₁), …', 'ланцюжок: ' + ' → '.join(fmt(v) for v in chain))

def f_inverse_hard(T, rng, lv):
    kind = rng.choice(['mob', 'mob', 'quad'])
    if kind == 'mob':
        a, b, c, d = [rng.randint(-4, 5) for _ in range(4)]
        if a * d - b * c == 0 or c == 0 or a == 0: return False
        y0 = rng.randint(-5, 6)
        if a - c * y0 == 0: return False
        x = F(d * y0 - b, a - c * y0)
        # f(x) = (ax+b)/(cx+d); перевірка
        if c * x + d == 0: return False
        assert (a * x + b) / (c * x + d) == y0
        num = poly([a, b]); den = poly([c, d])
        ans = x
        wr = [(F(a * y0 + b, c * y0 + d) if c * y0 + d else F(1), f'обчислено f({y0}) замість розв’язування f(x) = {y0}'), (F(-d * y0 + b, a - c * y0) if True else 0, 'знаки в чисельнику d·y − b переплутано'), (F(d * y0 - b, a + c * y0) if a + c * y0 else F(2), 'знак у знаменнику a − c·y змінено'), (F(a - c * y0, d * y0 - b) if d * y0 - b else F(3), 'частку перевернуто')]
        return T.add(lv, f'Нехай f(x) = ({num})/({den}). Знайдіть f⁻¹({y0}), тобто таке x, що f(x) = {y0}.', ans, wr, 'розв’яжіть рівняння (ax + b)/(cx + d) = y відносно x: x(a − cy) = dy − b', f'({num})/({den}) = {y0} ⇒ {num} = {y0}({den}) ⇒ x = {ffmt(x)}')
    p = rng.randint(1, 5); c0 = rng.randint(-6, 4); t = rng.randint(1, 5)
    # f(x) = x² − 2p x + c0, x ≥ p ;  x = p + t  ⇒ f = (x−p)² + c0 − p² = t² + c0 − p²
    y0 = t * t + c0 - p * p
    ans = F(p + t)
    wr = [(F(p - t), 'взято корінь, що не належить області x ≥ ' + str(p)), (F(t), 'знайдено лише √(y − c + p²), не додано p'), (F(-p - t), 'знаки при розв’язуванні переплутано'), (F(p + t * t), 'корінь не добуто')]
    return T.add(lv, f'Функція f(x) = x² {sg(-2 * p)} {2 * p}x {sg(c0)} {abs(c0)} задана на проміжку [{p}; +∞). Знайдіть f⁻¹({fmt(y0)}).' if c0 else f'Функція f(x) = x² − {2 * p}x задана на проміжку [{p}; +∞). Знайдіть f⁻¹({fmt(y0)}).', ans, wr, 'обернену шукають лише на області значень; виділіть повний квадрат', f'(x − {p})² = {fmt(y0)} {sg(p * p - c0)} {abs(p * p - c0)} = {t * t} ⇒ x − {p} = {t} (x ≥ {p}) ⇒ x = {p + t}')

# ----- прогресії L3 -----
def f_ap_property(T, rng, lv):
    kind = rng.choice(['sum_idx', 'sum_idx', 'two_cond', 'three', 'smax', 'sn_eq'])
    if kind == 'sum_idx':
        n_ = rng.choice([9, 11, 13, 15, 17, 19, 21]); mid = (n_ + 1) // 2
        p = rng.randint(2, mid - 1); q = n_ + 1 - p
        X = rng.choice([v for v in range(-30, 40) if v and v % 2 == 0]) if True else 0
        ans = F(n_ * X, 2)
        wr = [(F(n_ * X), 'суму не поділено на 2'), (F(X, 2), 'не помножено на кількість членів n'), (F(X), 'за суму прийнято a_p + a_q'), (F(n_ * X, 2) + X, 'до правильної суми додано зайвий доданок')]
        return T.add(lv, f'В арифметичній прогресії a{sub(p)} + a{sub(q)} = {fmt(X)}. Знайдіть суму перших {n_} членів цієї прогресії.', ans, wr, f'якщо p + q = 1 + n, то a_p + a_q = a₁ + a_n, а S_n = (a₁ + a_n)/2·n', f'{p} + {q} = {n_ + 1} = 1 + {n_}, тому a₁ + a_{n_} = {fmt(X)}; S_{n_} = {fmt(X)}/2·{n_} = {fmt(ans)}')
    if kind == 'two_cond':
        m = rng.randint(3, 12); d = rng.choice([2, 3, 4]); Y = (m - d) * (m + d)
        ans = F(m - 2 * d)
        wr = [(F(m + 2 * d), 'при d > 0 перший член менший за третій, а тут взято a₅'), (F(m - d), 'знайдено a₂ замість a₁'), (F(m), 'за a₁ взято a₃'), (F(-(m - 2 * d)), 'знак результату змінено')]
        return T.add(lv, f'Для зростаючої арифметичної прогресії a₃ = {m}, a₂·a₄ = {Y}. Знайдіть a₁.', ans, wr, 'a₂ = a₃ − d, a₄ = a₃ + d: a₂a₄ = a₃² − d²; d > 0 для зростаючої', f'{m}² − d² = {Y} ⇒ d² = {d * d} ⇒ d = {d} (зростає); a₁ = {m} − 2·{d} = {fmt(m - 2 * d)}')
    if kind == 'three':
        x = rng.randint(2, 12); d = rng.randint(1, 4); nums = [x - d, x, x + d]
        S = 3 * x; Q = sum(v * v for v in nums)
        ans = F(x + d)
        wr = [(F(x - d), 'названо найменше число'), (F(x), 'названо середнє число'), (F(d), 'знайдено різницю прогресії'), (F(Q - S), 'знайдено різницю суми квадратів і суми')]
        return T.add(lv, f'Три числа утворюють зростаючу арифметичну прогресію. Їх сума дорівнює {S}, а сума квадратів — {Q}. Знайдіть найбільше з цих чисел.', ans, wr, 'позначте числа x − d, x, x + d: сума 3x, сума квадратів 3x² + 2d²', f'3x = {S} ⇒ x = {x}; 3·{x}² + 2d² = {Q} ⇒ d² = {d * d} ⇒ d = {d}; числа {nums[0]}, {nums[1]}, {nums[2]}; найбільше {x + d}')
    if kind == 'smax':
        d = -rng.choice([2, 3, 4, 5]); a1 = rng.randint(15, 60)
        n_best = max(n for n in range(1, 100) if a1 + (n - 1) * d > 0)
        S = lambda n: n * (2 * a1 + (n - 1) * d) // 2
        ask = rng.choice(['n', 'S'])
        if ask == 'n':
            ans = F(n_best)
            wr = [(F(n_best + 1), 'взято перший недодатний член (він зменшує суму)'), (F(n_best - 1), 'не враховано останній додатний член'), (F(-a1 // d), 'номер знайдено як частку |a₁|/|d| без урахування цілої частини та +1'), (F(a1 // abs(d) + 2), 'номер визначено з похибкою')]
            return T.add(lv, f'В арифметичній прогресії a₁ = {a1}, d = {d}. При якому n сума S_n перших n членів набуває найбільшого значення?', ans, wr, 'сума зростає, поки члени додатні; зупиняємося на останньому додатному члені', f'a_n > 0 ⇒ {a1} + (n − 1)·({d}) > 0 ⇒ n − 1 < {ffmt(F(a1, -d))} ⇒ n = {n_best}')
        ans = F(S(n_best))
        wr = [(F(S(n_best + 1)), 'враховано перший недодатний член, що не збільшує суму'), (F(S(n_best - 1)), 'не враховано останній додатний член'), (F(a1 * n_best), 'суму знайдено як a₁·n'), (F(max(S(n_best), S(n_best + 1)) + abs(d)), 'допущено помилку при обчисленні')]
        return T.add(lv, f'В арифметичній прогресії a₁ = {a1}, d = {d}. Знайдіть найбільше значення суми перших n членів.', ans, wr, 'найбільша сума — до останнього додатного члена', f'додатні члени до n = {n_best}; S_{n_best} = {fmt(ans)}')
    # sn_eq: S_n = S  =>  n
    a1 = rng.randint(-6, 8); d = rng.choice([2, 3, 4, 5]); n_ = rng.randint(6, 14)
    S = n_ * (2 * a1 + (n_ - 1) * d) // 2
    if n_ * (2 * a1 + (n_ - 1) * d) % 2: return False
    ans = F(n_)
    wr = [(F(n_ - 1), 'номер знайдено без врахування одного члена'), (F(n_ + 1), 'номер знайдено з надлишком на 1'), (F(2 * S, n_ + 0) if False else F(S, d), 'суму поділено на d'), (F(S - a1, d) if (S - a1) % d == 0 else F(n_ + 2), 'за формулою n = (S − a₁)/d (це формула для члена, а не для суми)')]
    return T.add(lv, f'В арифметичній прогресії a₁ = {fmt(a1)}, d = {d}. Скільки перших членів потрібно взяти, щоб їх сума дорівнювала {S}?', ans, wr, 'S_n = (2a₁ + (n − 1)d)·n/2 — квадратне рівняння відносно n; натуральний корінь', f'({2 * a1} + (n − 1)·{d})·n/2 = {S} ⇒ {d}n² + {2 * a1 - d}n − {2 * S} = 0 ⇒ n = {n_}'.replace('+ -', '− '))

def f_gp_hard(T, rng, lv):
    kind = rng.choice(['two', 'two', 'inf_eq', 'three', 'sn', 'compound', 'sq'])
    if kind == 'two':
        q = rng.choice([2, 3, -2, 4, -3]); b1 = rng.randint(1, 5); A = b1 * (1 + q * q); B = b1 * q * (1 + q * q)
        ask = rng.choice(['q', 'b1'])
        if ask == 'q':
            ans = F(q)
            wr = [(F(A, B), 'частку перевернуто'), (F(B - A), 'знайдено різницю сум'), (F(-q), 'знак знаменника змінено'), (F(B, A * 2), 'суму поділено на подвоєну')]
            return T.add(lv, f'У геометричній прогресії b₁ + b₃ = {A}, b₂ + b₄ = {B}. Знайдіть знаменник прогресії.', ans, wr, 'b₂ + b₄ = q(b₁ + b₃)', f'q = {B}/{A} = {q}')
        ans = F(b1)
        wr = [(F(A, 1 + q), 'у знаменнику взято 1 + q замість 1 + q²'), (F(A, 2), 'вважали, що b₃ = b₁'), (F(A - B), 'знайдено різницю сум'), (F(b1 * q), 'знайдено b₂')]
        return T.add(lv, f'У геометричній прогресії b₁ + b₃ = {A}, b₂ + b₄ = {B}. Знайдіть b₁.', ans, wr, 'q = (b₂ + b₄)/(b₁ + b₃); b₁(1 + q²) = b₁ + b₃', f'q = {B}/{A} = {q}; b₁(1 + {q * q}) = {A} ⇒ b₁ = {b1}')
    if kind == 'inf_eq':
        S = rng.choice([F(1, 2), F(1, 3), F(2, 3), F(3, 2), F(1, 4), F(2, 5), 1, 2, 3]); S = F(S)
        x = S / (1 + S)
        wr = [(S / (1 - S) if S != 1 else F(5), 'у формулі S = x/(1 − x) знак при розв’язуванні переплутано (x = S/(1 − S))'), (F(1) / (1 + S), 'знайдено 1/(1 + S) замість S/(1 + S)'), (F(S), 'за x узято саму суму'), (-x, 'знак розв’язку змінено')]
        txt = f'Розв’яжіть рівняння x + x² + x³ + … = {ffmt(S)} (ліва частина — сума нескінченної геометричної прогресії, |x| < 1).'
        return T.add(lv, txt, x, wr, 'S = b₁/(1 − q), де b₁ = x, q = x; потрібно |x| < 1', f'x/(1 − x) = {ffmt(S)} ⇒ x = {ffmt(S)}·(1 − x) ⇒ x = ({ffmt(S)})/(1 + {ffmt(S)}) = {ffmt(x)}')
    if kind == 'three':
        q = rng.choice([2, 3, 4]); m = rng.choice([4, 6, 8, 12])
        nums = [F(m, q), F(m), F(m * q)]
        if nums[0].denominator != 1: return False
        P = nums[0] * nums[1] * nums[2]; S = sum(nums)
        ans = F(m * q)
        wr = [(F(m), 'названо середнє число'), (nums[0], 'названо найменше число'), (F(S - m), 'знайдено суму крайніх чисел'), (F(P) ** F(1, 1) / m if False else F(m * m), 'знайдено добуток крайніх чисел')]
        return T.add(lv, f'Три числа утворюють зростаючу геометричну прогресію з додатними членами. Їх добуток дорівнює {fmt(P)}, а сума — {fmt(S)}. Знайдіть найбільше з цих чисел.', ans, wr, 'позначте b/q, b, bq: добуток b³; сума b(1/q + 1 + q)', f'b³ = {fmt(P)} ⇒ b = {m}; {m}(1/q + 1 + q) = {fmt(S)} ⇒ q = {q}; числа {fmt(nums[0])}, {m}, {fmt(nums[2])}; найбільше {fmt(m * q)}')
    if kind == 'sn':
        b = rng.choice([2, 3, 4]); c = rng.choice([1, 2, 3]); k = rng.randint(3, 5)
        Sn = lambda n: c * (b ** n - 1)
        bk = Sn(k) - Sn(k - 1)
        ans = F(bk)
        wr = [(F(Sn(k)), 'за член взято суму перших k членів'), (F(Sn(k + 1) - Sn(k)), 'знайдено b_(k+1) замість b_k'), (F(Sn(k - 1)), 'знайдено суму перших k − 1 членів'), (F(c * b ** k), 'до різниці сум не віднято S_(k−1)')]
        return T.add(lv, f'Сума перших n членів геометричної прогресії задається формулою S_n = {c}·{b}ⁿ − {c}. Знайдіть b{sub(k)}.', ans, wr, 'b_k = S_k − S_(k−1)', f'S_{k} = {fmt(Sn(k))}, S_{k - 1} = {fmt(Sn(k - 1))}; b_{k} = {fmt(Sn(k))} − {fmt(Sn(k - 1))} = {fmt(bk)}')
    if kind == 'compound':
        P = rng.choice([10000, 20000, 5000, 40000]); r = rng.choice([10, 20, 5]); n_ = rng.choice([2, 3]); 
        val = F(P) * (F(100 + r, 100)) ** n_
        if val.denominator != 1: return False
        wr = [(F(P) * (1 + F(r, 100) * n_), f'нараховано прості відсотки ({r}% від початкової суми щороку)'), (F(P) * (F(100 + r, 100)) ** (n_ - 1), f'враховано {n_ - 1} рік замість {n_}'), (F(P) * (F(100 + r, 100)) ** (n_ + 1), f'враховано {n_ + 1} рік замість {n_}'), (F(P) + F(P * r * n_, 100) * F(1, 2), 'відсотки враховано неправильно')]
        yrs = {2: 'роки', 3: 'роки'}[n_]
        return T.add(lv, f'Вклад {P} грн покладено в банк під {r}% річних зі складними відсотками (відсотки щороку додаються до суми вкладу). Яка сума буде на рахунку через {n_} {yrs}?', val, wr, 'складні відсотки: P·(1 + r/100)ⁿ — геометрична прогресія зі знаменником 1 + r/100', f'{P}·({100 + r}/100)^{n_} = {fmt(val)} грн')
    q = rng.choice([F(1, 2), F(1, 3), F(2, 3), F(-1, 2), F(1, 4)]); b1 = rng.choice([3, 4, 6, 8, 9, 12])
    S2 = F(b1 * b1) / (1 - q * q); S = F(b1) / (1 - q)
    wr = [(S * S, 'суму квадратів знайдено як квадрат суми'), (F(b1 * b1) / (1 - q) ** 2, 'у знаменнику взято (1 − q)² замість 1 − q²'), (F(b1 * b1) / (1 - q), 'у знаменнику взято 1 − q замість 1 − q²'), (F(b1) / (1 - q * q), 'не піднесено b₁ до квадрата')]
    return T.add(lv, f'Нескінченна геометрична прогресія має перший член b₁ = {b1} і знаменник q = {ffmt(q)}. Знайдіть суму квадратів усіх її членів.', S2, wr, 'квадрати членів теж утворюють геометричну прогресію: b₁², b₁²q², … зі знаменником q²', f'зі знаменником q² = {ffmt(q * q)}: S = {b1 * b1}/(1 − {ffmt(q * q)}) = {ffmt(S2)}')

def count_roots(fn, lo, hi, N=40000):
    cnt = 0; prev = fn(lo)
    for i in range(1, N + 1):
        x = lo + (hi - lo) * i / N; cur = fn(x)
        if prev == 0 or prev * cur < 0: cnt += 1
        prev = cur
    return cnt

def f_abs_count(T, rng, lv):
    kind = rng.choice(['abs_quad', 'abs_quad', 'abs_lin2', 'param_abs'])
    if kind == 'abs_quad':
        b = rng.choice([2, 4, 6, 8]); top = F(b * b, 4)
        k = rng.choice([F(1, 2), 1, 2, 3, 4, 5, 6, 9, 10, 12, 16, 17]); k = F(k)
        f = lambda x: abs(x * x - b * x) - float(k)
        if abs(float(k) - float(top)) < 1e-9: ans = 3
        elif k < top: ans = 4
        else: ans = 2
        # перевірка сіткою
        gc = count_roots(f, -30, 30)
        if gc != ans: 
            # рівність у вершині: корінь дотику не ловиться знакозміною
            if ans != 3 or gc not in (2,): return False
        txt = f'Скільки коренів має рівняння |x² − {b}x| = {ffmt(k)}?'
        wr = [(F(2), 'розглянуто лише рівняння x² − bx = k, а не x² − bx = ±k') if ans != 2 else (F(4), 'не враховано, що k перевищує найбільше значення −x² + bx (вершина відображеної частини)'), (F(4) if ans != 4 else F(3), 'вважали, що для будь-якого k > 0 рівняння має 4 корені'), (F(3) if ans != 3 else F(2), 'вважали, що рівно один корінь — дотичний'), (F(1), 'вважали, що графік перетинає пряму лише в одній точці'), (F(0), 'вважали, що модуль не набуває значення k')]
        wr = [w for w in wr if w[0] != F(ans)]
        return T.add(lv, txt, F(ans), wr, f'будуємо y = |x² − {b}x|: частину під віссю x відображаємо вгору; висота «горба» = {ffmt(top)}', f'висота відображеного горба {ffmt(top)}; k = {ffmt(k)} ' + ('< ' + ffmt(top) + ' — 4 перетини' if ans == 4 else ('= ' + ffmt(top) + ' — 3 перетини' if ans == 3 else '> ' + ffmt(top) + ' — 2 перетини')))
    if kind == 'abs_lin2':
        a = rng.randint(2, 6); k = rng.randint(0, a + 3)
        f = lambda x: abs(abs(x) - a) - k
        ans = 2 if k == 0 else (4 if 0 < k < a else (3 if k == a else 2))
        if k == a: pass
        elif count_roots(f, -40, 40) != ans: return False
        txt = f'Скільки коренів має рівняння ||x| − {a}| = {k}?'
        why = {0: 'k = 0: |x| = ' + str(a) + ' — 2 корені', 4: f'0 < k < {a}: |x| = {a} ± {k}, обидва значення додатні — 4 корені', 3: f'k = {a}: |x| = {2 * a} або |x| = 0 — 3 корені', 2: f'k > {a}: |x| = {a + k} (2 корені), а |x| = {a - k} < 0 — коренів немає; усього 2'}[ans if not (k == 0) else 0]
        wr = [(F(2) if ans != 2 else F(4), 'не враховано, що рівняння розпадається на дві умови, кожна з яких може дати два корені') , (F(4) if ans != 4 else F(3), 'вважали, що при будь-якому k > 0 є чотири корені'), (F(3) if ans != 3 else F(2), 'вважали, що один із випадків дає рівно один корінь'), (F(1), 'вважали, що ||x| − a| = k має єдиний корінь'), (F(0), 'вважали, що розв’язків немає')]
        return T.add(lv, txt, F(ans), [w for w in wr if w[0] != F(ans)], '||x| − a| = k ⇒ |x| = a ± k; кожне невід’ємне значення дає два корені (0 — один)', why)
    # param: при якому k рівняння |x² − bx| = k має рівно три корені
    b = rng.choice([2, 4, 6, 8, 10])
    ans = F(b * b, 4)
    wr = [(F(b * b), 'за висоту горба взято b²'), (F(b * b, 2), 'за висоту горба взято b²/2'), (F(b), 'за висоту горба взято b'), (F(b * b, 8), 'вершину знайдено неправильно (b²/8)')]
    return T.add(lv, f'При якому значенні k рівняння |x² − {b}x| = k має рівно три корені?', ans, wr, 'три корені — коли горизонтальна пряма y = k проходить через вершину відображеної частини', f'вершина x² − {b}x: x = {b // 2}, y = {-(b * b) // 4}; після відображення горб має висоту {b * b // 4}; k = {b * b // 4}')

def f_periodic_value(T, rng, lv):
    kind = rng.choice(['mod', 'mod', 'parity'])
    T_ = rng.choice([3, 4, 5, 6]); a = rng.choice([1, 2, -1]); b = rng.randint(-4, 4)
    if kind == 'mod':
        f = lambda x: a * x * x + b * x
        N = rng.choice([-1, 1]) * rng.randint(2 * T_ + 1, 8 * T_ + 2)
        r = N % T_; ans = F(f(r))
        r_wrong = N - T_ * int(N / T_)   # залишок із усіканням до нуля
        wr = [(F(f(N)), 'формулу застосовано до самого N, а не до зведеного значення'), (F(f(r_wrong)), 'залишок від ділення від’ємного числа знайдено неправильно (потрібен залишок у [0; T))') if r_wrong != r else (F(f(T_ - r)), 'взято T − r замість r'), (F(f(T_ - r)), 'взято T − r замість r'), (F(f(abs(N) % T_)), 'знак N проігноровано: взято залишок від |N|')]
        pol = poly([a, b, 0])
        return T.add(lv, f'Функція f(x) періодична з періодом {T_}, і на проміжку [0; {T_}) f(x) = {pol}. Знайдіть f({N}).', ans, wr, f'f(N) = f(N − kT): зведіть аргумент до проміжку [0; {T_}) (залишок додатний)', f'{N} = {(N - r) // T_}·{T_} {sg(r)} {r}; f({N}) = f({r}) = {fmt(ans)}')
    v1 = rng.choice([v for v in range(-8, 9) if v]); N = rng.choice([1, 3, 5, 7]) * rng.choice([1, -1])
    T2 = rng.choice([4, 6, 8])
    # f непарна, T = T2, f(1) = v1 → f(-1 - k*T2?) : f(1 - T2 * j) ... обчислимо f(−1 + T2·j)?
    j = rng.randint(2, 6)
    arg = 1 - T2 * j if rng.random() < .5 else T2 * j - 1
    # f(arg): arg ≡ 1 (mod T2) або ≡ −1 (mod T2)
    if (arg - 1) % T2 == 0: ans = F(v1); why = f'{arg} = 1 {sg(arg - 1)} {abs(arg - 1)}, період {T2}: f({arg}) = f(1) = {v1}'
    else: ans = F(-v1); why = f'{arg} = −1 {sg(arg + 1)} {abs(arg + 1)}; f({arg}) = f(−1) = −f(1) = {-v1}'
    wr = [(F(-ans), 'не враховано непарність (f(−x) = −f(x)) або використано її зайвий раз'), (F(0), 'вважали, що значення в протилежних точках взаємно знищуються'), (F(2 * ans), 'значення подвоєно'), (F(1, ans) if ans else F(1), 'взято обернену величину')]
    return T.add(lv, f'Функція f непарна та періодична з періодом {T2}. Відомо, що f(1) = {v1}. Знайдіть f({arg}).', ans, wr, 'f(x + T) = f(x) та f(−x) = −f(x): зведіть аргумент до ±1', why)

def f_monotone_param(T, rng, lv):
    kind = rng.choice(['inc', 'dec', 'base'])
    G = setstr
    if kind == 'inc':
        m = rng.choice([1, 2, 3, 4, 5]); c = m * m - 1
        txt = f'При яких значеннях a функція y = (a² − {c})ˣ є зростаючою?' if c else 'При яких значеннях a функція y = (a²)ˣ є зростаючою?'
        sol = [(None, F(-m), False, False), (F(m), None, False, False)]
        wr = [(G([(F(-m), F(m), False, False)]), 'знайдено значення a, при яких основа менша за 1 (функція не зростає)'), (G([(F(m), None, False, False)]), 'враховано лише додатні значення a (a² > ' + str(m * m) + ' дає й від’ємні)'), (G([(None, F(-m), True, True), (F(m), None, True, True)]), 'при a² − ' + str(c) + ' = 1 функція стала, тому дужки круглі'), (G([(F(-m), F(m), True, True)]), 'нерівність a² > ' + str(m * m) + ' розв’язано як a² < ' + str(m * m))]
        return T.add(lv, txt, G(sol), wr, 'показникова функція зростає, коли основа більша за 1', f'a² − {c} > 1 ⇒ a² > {m * m} ⇒ |a| > {m}')
    if kind == 'dec':
        c = rng.choice([0, 3, 8, 15, 24]); m_lo = {0: 0, 3: 3, 8: 8, 15: 15, 24: 24}[c]
        r1 = {0: '0', 3: '√3', 8: '2√2', 15: '√15', 24: '2√6'}[c]; r2 = str(int(math.isqrt(c + 1)))
        txt = f'При яких значеннях a функція y = (a² − {c})ˣ є спадною?' if c else 'При яких значеннях a функція y = (a²)ˣ є спадною?'
        if c == 0:
            ans = '(−1; 0) ∪ (0; 1)'; wr = [('(−1; 1)', 'не враховано, що при a = 0 основа дорівнює 0 (функція не визначена як показникова)'), ('(−∞; −1) ∪ (1; +∞)', 'знайдено значення a, при яких функція зростає'), ('(0; 1)', 'враховано лише додатні значення a'), ('[−1; 1]', 'при a = ±1 основа дорівнює 1, функція стала; при a = 0 основа 0')]
            return T.add(lv, txt, ans, wr, 'спадна показникова функція: 0 < основа < 1', '0 < a² < 1 ⇒ a ≠ 0 і |a| < 1')
        ans = f'({M}{r2}; {M}{r1}) ∪ ({r1}; {r2})'
        wr = [(f'({M}{r2}; {r2})', 'не виключено значення, при яких основа ≤ 0'), (f'(−∞; {M}{r2}) ∪ ({r2}; +∞)', 'знайдено значення a, при яких функція зростає'), (f'({r1}; {r2})', 'враховано лише додатні значення a'), (f'[{M}{r2}; {M}{r1}] ∪ [{r1}; {r2}]', 'на кінцях основа дорівнює 0 або 1: функція там не спадна, дужки круглі')]
        return T.add(lv, txt, ans, wr, 'спадна показникова функція: 0 < основа < 1', f'0 < a² − {c} < 1 ⇒ {c} < a² < {c + 1} ⇒ {r1} < |a| < {r2}')
    m = rng.choice([1, 2, 3, 4, 5])
    txt = f'При яких значеннях a функція y = log_(a − {m}) x є зростаючою?'
    sol = [(F(m + 1), None, False, False)]
    wr = [(G([(F(m), F(m + 1), False, False)]), 'знайдено значення a, при яких функція спадає'), (G([(F(m), None, False, False)]), f'враховано лише додатність основи a − {m} > 0, а для зростання потрібно a − {m} > 1'), (G([(None, F(m + 1), False, False)]), 'знак нерівності обрано протилежний'), (G([(F(m + 1), None, True, False)]), 'при a = ' + str(m + 1) + ' основа дорівнює 1 — функція не є логарифмічною, тому знак строгий')]
    return T.add(lv, txt, G(sol), wr, 'логарифмічна функція зростає, коли основа більша за 1', f'a − {m} > 1 ⇒ a > {m + 1}')

def f_rect_partition(T, rng, lv):
    kind = rng.choice(['part', 'tri'])
    P = rng.choice([60, 72, 96, 120, 144])
    if kind == 'part':
        # прямокутна ділянка з однією перегородкою паралельно меншій стороні: P = 2L + 3W (три «ширини»)
        ans = F(P * P, 24)
        wr = [(F(P * P, 16), 'перегородку не враховано (периметр P розподілено на 4 сторони)'), (F(P * P, 32), 'перегородку враховано двічі'), (F(P, 3) ** 2, 'за сторону квадрата взято P/3'), (F(P * P, 12), 'площу знайдено без поділу на 2')]
        return T.add(lv, f'Прямокутну ділянку потрібно огородити сіткою завдовжки {P} м і розділити на дві частини перегородкою, паралельною одній із сторін (всього три відрізки однієї довжини і два — другої). Яка найбільша площа ділянки (у м²)?', ans, wr, 'S = x·y, де 3x + 2y = P: максимум квадратичної функції', f'3x + 2y = {P} ⇒ y = ({P} − 3x)/2; S = x({P} − 3x)/2; вершина x = {ffmt(F(P, 6))}; S = {ffmt(ans)} м²')
    a_, b_ = rng.choice([(12, 16), (6, 8), (10, 24), (20, 15), (8, 14), (18, 24), (30, 40)])
    ans = F(a_ * b_, 4)
    wr = [(F(a_ * b_, 2), 'за площу прямокутника взято площу всього трикутника'), (F(a_ * b_, 8), 'сторони прямокутника взято по a/4 і b/4'), (F(a_ * b_, 3), 'сторони прямокутника взято по a/3 і b/3 (це не максимум)'), (F(a_ * b_), 'за площу взято добуток катетів')]
    return T.add(lv, f'У прямокутний трикутник із катетами {a_} і {b_} вписано прямокутник, дві сторони якого лежать на катетах. Яка найбільша площа такого прямокутника?', ans, wr, 'якщо одна сторона x, то інша b(1 − x/a); S = bx(1 − x/a) — квадратична функція з вершиною x = a/2', f'x = {fmt(F(a_, 2))}, інша сторона {fmt(F(b_, 2))}; S = {fmt(F(a_, 2))}·{fmt(F(b_, 2))} = {ffmt(ans)}')
