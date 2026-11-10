import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t1 import *
import msvg as S

CATS = ['Житло', 'Їжа', 'Транспорт', 'Освіта', 'Одяг', 'Розваги', 'Заощадження', 'Комунальні']

def pie_img(name, title, cats, pcts, unknown=None):
    c = S.C(520, 250, title)
    S.pie(c, 130, 140, 88, pcts, colors=S.LIGHT, labels=[('?' if i == unknown else f'{p}%') for i, p in enumerate(pcts)], size=14)
    for i, cat in enumerate(cats):
        y = 70 + i * 28
        c.rect(270, y - 12, 18, 18, fill=S.LIGHT[i], stroke=S.INK, sw=1)
        c.text(296, y + 2, cat, size=14)
    return c.save(name)

def f_pie(T, rng, lv):
    k = rng.choice([4, 5]); cats = rng.sample(CATS, k)
    while True:
        pcts = [5 * rng.randint(1, 8) for _ in range(k - 1)]
        last = 100 - sum(pcts)
        if 5 <= last <= 40 and len(set(pcts + [last])) == k: pcts.append(last); break
    D = rng.choice([8000, 12000, 15000, 20000, 24000, 30000, 36000, 40000])
    ttl = rng.choice(['Витрати сім’ї за місяць', 'Структура місячного бюджету'])
    mode = rng.choice(['cat', 'diff', 'sum', 'hidden']) if lv >= 2 else 'cat'
    if lv == 3: mode = rng.choice(['hidden', 'diff', 'sum'])
    i, j = rng.sample(range(k), 2)
    amt = lambda p: D * p // 100
    if mode == 'hidden':
        h = rng.randrange(k); name = 'p' + S.tag(cats, pcts, h)
        img = pie_img(f't1_pie_{name}', ttl, cats, pcts, unknown=h)
        known = sum(p for t, p in enumerate(pcts) if t != h)
        p = pcts[h]
        wr = [(amt(known), 'знайдено суму відомих секторів, а не пропущеного'), (D * p, 'не поділено на 100'), (amt(100 - p), 'знайдено решту бюджету, а не потрібну категорію'), (p, 'у відповідь записано відсоток замість суми в гривнях')]
        return T.add(lv, f'На діаграмі показано, як сім’я розподіляє місячний дохід {D} грн. Для категорії «{cats[h]}» відсоток не зазначено. Скільки гривень витрачають на «{cats[h]}»?', amt(p), wr,
                     'сума всіх секторів кругової діаграми — 100%; невідомий сектор = 100% − відомі', f'{100} − {known} = {p}%; {D} · {p} : 100 = {amt(p)} грн', img=img)
    img = pie_img('t1_pie_' + S.tag(cats, pcts, mode, 'x'), ttl, cats, pcts)
    if mode == 'cat':
        p = pcts[i]
        wr = [(D * p, 'не поділено на 100'), (amt(100 - p), 'знайдено решту бюджету'), (p, 'у відповідь записано відсоток, а не гривні'), (F(D, p), 'суму поділено на відсоток')]
        return T.add(lv, f'За діаграмою визначте, скільки гривень становлять витрати на «{cats[i]}», якщо місячний дохід сім’ї — {D} грн.', amt(p), wr, 'частина = загальна сума · відсоток : 100', f'{D} · {p} : 100 = {amt(p)} грн', img=img)
    if mode == 'diff':
        a, b = pcts[i], pcts[j]
        if a == b: return False
        hi, lo = (i, j) if a > b else (j, i)
        wr = [(abs(a - b), 'різницю відсотків записано як гривні'), (amt(a + b), 'витрати додано, а не віднято'), (D * abs(a - b), 'не поділено на 100'), (amt(max(a, b)), 'знайдено лише більшу категорію')]
        return T.add(lv, f'Місячний дохід сім’ї — {D} грн. На скільки гривень витрати на «{cats[hi]}» більші за витрати на «{cats[lo]}» (за діаграмою)?', amt(abs(a - b)), wr, 'різниця часток × загальна сума', f'({pcts[hi]}% − {pcts[lo]}%) · {D} = {abs(a-b)}% · {D} = {amt(abs(a-b))} грн', img=img)
    a, b = pcts[i], pcts[j]
    wr = [(a + b, 'відсотки додано, але потрібні гривні'), (amt(a) * amt(b), 'суми в гривнях помножено'), (amt(a + b) * 2, 'суму подвоєно'), (amt(100 - a - b), 'знайдено решту бюджету')]
    return T.add(lv, f'Місячний дохід сім’ї — {D} грн. Скільки гривень становлять разом витрати на «{cats[i]}» та «{cats[j]}» (за діаграмою)?', amt(a + b), wr, 'складіть відсотки двох секторів і знайдіть їх від загальної суми', f'({a}% + {b}%) · {D} = {a+b}% · {D} = {amt(a+b)} грн', img=img)

MONTHS = ['Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер']
def bar_img(name, title, labels, vals, ymax, ystep):
    c = S.C(460, 280, title)
    ax = S.Axes(c, 60, 45, 370, 190, 0.4, len(vals) + 0.6, 0, ymax, 1, ystep, grid=True, labels=False, xlab='', ylab='')
    for k in range(0, ymax + 1, ystep):
        if k: c.text(ax.X(0.4) - 6, ax.Y(k) + 4, str(k), size=11, anchor='end', col=S.GRAY)
    S.bars(c, ax, vals, labels, col='#93c5fd')
    return c.save(name)

def f_bar(T, rng, lv):
    n = rng.choice([4, 5, 6]); labels = MONTHS[:n]
    while True:
        base = rng.choice([20, 25, 40, 50, 60, 80])
        vals = [base * rng.choice([1, 1.25, 1.5, 2, 0.5, 0.75, 1.2]) for _ in range(n)]
        if all(v == int(v) for v in vals) and len({int(v) for v in vals}) >= n - 1: break
    vals = [int(v) for v in vals]
    ymax = max(vals) + (10 - max(vals) % 10); ystep = 10 if ymax <= 100 else 20
    ttl = rng.choice(['Продаж за місяць, тис. грн', 'Кількість відвідувачів, сотні', 'Продано книг, десятки'])
    mode = rng.choice(['pct_up', 'times', 'share']) if lv == 2 else rng.choice(['share', 'pct_two'])
    i, j = sorted(rng.sample(range(n), 2))
    img_name = 't1_bar_' + S.tag(vals, ttl, mode, i, j)
    img = bar_img(img_name, ttl, labels, vals, ymax, ystep)
    tot = sum(vals)
    if mode == 'pct_up':
        a, b = vals[i], vals[j]
        if a == b or (abs(b - a) * 100) % a: return False
        pct = F(abs(b - a) * 100, a); word = 'збільшився' if b > a else 'зменшився'
        wr = [(F(abs(b - a) * 100, b), 'різницю поділено на кінцеве значення, а не на початкове'), (abs(b - a), 'різницю значень записано як відсотки'), (F(b * 100, a), 'знайдено, скільки відсотків становить кінцеве значення від початкового'), (pct + 10, 'відсоток підібрано неточно')]
        return T.add(lv, f'За діаграмою визначте, на скільки відсотків показник у місяці «{labels[j]}» {word} порівняно з місяцем «{labels[i]}» ({ttl.lower()}).', pc(pct), [(pc(w), r) for w, r in wr],
                     'відсоткова зміна = (нове − старе) : старе · 100%', f'|{b} − {a}| : {a} · 100% = {fmt(pct)}%', img=img)
    if mode == 'times':
        a, b = vals[i], vals[j]
        if a == b: return False
        hi, lo = max(a, b), min(a, b)
        wr = [(hi - lo, 'знайдено різницю, а не відношення'), (F(lo, hi), 'відношення взято навпаки'), (hi + lo, 'значення додано'), (F(hi, lo) + 1, 'до відношення додано одиницю')]
        return T.add(lv, f'У скільки разів найбільше з двох значень на діаграмі (місяці «{labels[i]}» та «{labels[j]}») більше за менше? ({ttl})', F(hi, lo), wr, 'відношення більшого до меншого', f'{hi} : {lo} = {fmt(F(hi, lo))}', img=img)
    if mode == 'share':
        m = max(range(n), key=lambda t: vals[t])
        if sorted(vals)[-1] == sorted(vals)[-2]: return False
        sh = F(vals[m] * 100, tot)
        wr = [(F(vals[m] * 100, max(vals) + min(vals)), 'у знаменнику взято не всю суму, а лише два значення'), (F(vals[m] * 100, vals[0]), 'взято відношення до першого стовпчика'), (F(vals[m]), 'значення прийнято за відсоток'), (F(vals[m] * 100, tot - vals[m]), 'у знаменнику взято суму без цього місяця')]
        return T.add(lv, f'Скільки відсотків від загального обсягу за всі {n} місяці на діаграмі становить найбільший місяць? ({ttl})', pc(sh), [(pc(w), r) for w, r in wr], 'частка = частина : ціле · 100%, де ціле — сума всіх стовпчиків', f'сума {tot}; {vals[m]} : {tot} · 100% = {fmt(sh) if sh.denominator==1 else dc(float(sh),1)}%', img=img)
    # pct_two: два послідовних порівняння
    a, b = vals[i], vals[j]; avg = F(sum(vals), n)
    if a == b: return False
    wr = [(F(a + b, 2), 'взято середнє лише двох значень'), (F(sum(vals) - a - b, n - 2) if n > 2 else 0, 'середнє тільки решти місяців'), (F(max(vals) + min(vals), 2), 'середнє найбільшого та найменшого'), (avg + 5, 'арифметична помилка')]
    return T.add(lv, f'Знайдіть середнє арифметичне значень за всі {n} місяці на діаграмі ({ttl}).', avg, wr, 'середнє = сума всіх значень : кількість значень', f'({" + ".join(map(str, vals))}) : {n} = {fmt(avg)}', img=img)

def numline_img(name, k, lo, hi, parts):
    c = S.C(520, 120)
    x0, x1, y = 40, 480, 70
    c.line(x0 - 10, y, x1 + 14, y, col=S.AX, w=1.8, arrow=True)
    span = hi - lo; px = lambda v: x0 + (v - lo) * (x1 - x0) / span
    for t in range(lo * parts, hi * parts + 1):
        X = px(F(t, parts)); big = t % parts == 0
        c.line(X, y - (9 if big else 5), X, y + (9 if big else 5), col=S.AX, w=1.6 if big else 1)
        if big: c.text(X, y + 26, S.dec(t // parts, 0), size=14, anchor='middle')
    X = px(F(k, parts)); c.dot(X, y, 5.5, S.RED); c.text(X, y - 16, 'P', size=16, col=S.RED, anchor='middle', bold=True)
    return c.save(name)

def f_numline(T, rng, lv):
    lo = rng.choice([-3, -2, -1, 0, 1]); hi = lo + rng.choice([3, 4])
    parts = rng.choice([4, 5, 10]) if lv == 1 else rng.choice([4, 5, 8])
    t = rng.randint(lo * parts + 1, hi * parts - 1)
    if t % parts == 0: return False
    img = numline_img('t1_nl_' + S.tag(lo, hi, parts, t), t, lo, hi, parts)
    val = F(t, parts)
    ip = math.floor(val); frac_ticks = t - ip * parts
    wr = [(F(ip) + F(frac_ticks, 10), f'проміжок розбито на {parts} частин, тому одна поділка дорівнює 1/{parts}, а не 0,1'), (F(t), 'кількість поділок від нуля прийнято за значення числа'),
          (F(ip) + F(frac_ticks, parts) + (1 if ip >= 0 else -1), 'зсув на одну одиницю від правильного'), (F(ip + 1) - F(frac_ticks, parts) if frac_ticks else val, 'відлік поділок ведеться від більшого числа')]
    return T.add(lv, f'Яке число зображено на числовій прямій точкою P? (Між сусідніми цілими числами — {parts} однакових проміжків.)', val, wr,
                 'ціна поділки = довжина одиничного відрізка : кількість проміжків', f'один проміжок = 1/{parts}; від нуля до P — {t} поділок, тому {t}/{parts} = {fmt(val)}', img=img)

def dt_img(name, segs, tmax, smax, tstep, sstep, marks=()):
    """segs — вершини ламаної [(t,s)...]"""
    c = S.C(520, 290, 'Графік руху велосипедиста')
    ax = S.Axes(c, 60, 45, 380, 190, 0, tmax, 0, smax, tstep, sstep, xlab='t, год', ylab='s, км', size=12)
    ax.c.poly([(ax.X(t), ax.Y(s)) for t, s in segs], stroke=S.BLUE, w=3, close=False)
    for t, s in segs:
        ax.point(t, s, None, col=S.BLUE, r=4)
    for t, s in marks:
        ax.seg(t, 0, t, s, col=S.GRAY, dash='4 3', w=1.2); ax.seg(0, s, t, s, col=S.GRAY, dash='4 3', w=1.2)
        ax.point(t, s, None, col=S.RED, r=4.5)
        ax.c.text(ax.X(t), ax.Y(s) - 9, f'({S.dec(t, 1)}; {S.dec(s, 1)})', size=12, col=S.RED, anchor='middle', bold=True)
    return c.save(name)

def f_disttime(T, rng, lv):
    v1 = rng.choice([10, 12, 15, 20]); t1 = rng.choice([1, 1.5, 2]); rest = rng.choice([0.5, 1, 1.5]); v2 = rng.choice([8, 12, 16, 24, 20]); t3 = rng.choice([1, 1.5, 2])
    if v1 == v2: return False
    s1 = v1 * t1; s2 = s1 + v2 * t3
    if s1 != int(s1) or s2 != int(s2): return False
    T2 = t1 + rest + t3
    segs = [(0, 0), (t1, s1), (t1 + rest, s1), (T2, s2)]
    sstep = 10 if s2 <= 60 else 20
    smax = (int(s2) // sstep + 1) * sstep
    tmax = math.ceil(T2) + (0.5 if math.ceil(T2) - T2 < 0.5 else 0)
    tmax = max(tmax, T2 + 0.5)
    tstep = 0.5
    tmax = math.ceil(tmax * 2) / 2
    kind = rng.choice(['rest', 'v2', 'avg', 'v1']) if lv == 2 else rng.choice(['avg', 'avgmove', 'back'])
    if kind in ('rest', 'v1', 'v2', 'back'): marks = ()
    img = dt_img('t1_dt_' + S.tag(segs, kind), segs, tmax, smax, tstep, sstep, marks=[(t1, s1), (t1 + rest, s1), (T2, s2)])
    if kind == 'rest':
        m = int(rest * 60)
        return T.add(lv, 'За графіком руху велосипедиста визначте, скільки хвилин він стояв (відрізок, де відстань не змінюється).', m, [(F(rest), 'час залишено в годинах'), (int(t1 * 60), 'взято тривалість першого відрізка'), (int(rest * 100), 'години перераховано у хвилини множенням на 100'), (int(T2 * 60), 'взято весь час руху')],
                     'на графіку шляху горизонтальний відрізок означає зупинку', f'зупинка тривала {fmt(F(str(rest)))} год = {m} хв', img=img)
    if kind == 'v2':
        return T.add(lv, 'За графіком визначте швидкість велосипедиста після зупинки (км/год).', v2, [(v1, 'взято швидкість на першому відрізку'), (F(s2) / F(str(T2)), 'взято середню швидкість за весь час'), (F(s2), 'взято весь пройдений шлях'), (v2 + v1, 'швидкості двох ділянок додано')],
                     'швидкість = пройдений шлях : час на цьому відрізку', f'({fmt(F(str(s2)))} − {fmt(F(str(s1)))}) : {fmt(F(str(t3)))} = {v2} км/год', img=img)
    if kind == 'v1':
        return T.add(lv, 'За графіком визначте швидкість велосипедиста на першому відрізку шляху (км/год).', v1, [(v2, 'взято швидкість на останньому відрізку'), (F(s2) / F(str(T2)), 'взято середню швидкість за весь час'), (F(s1), 'взято шлях замість швидкості'), (F(str(t1)), 'взято час замість швидкості')],
                     'швидкість = пройдений шлях : час', f'{fmt(F(str(s1)))} : {fmt(F(str(t1)))} = {v1} км/год', img=img)
    if kind == 'avg':
        av = F(str(s2)) / F(str(T2))
        wr = [(F(v1 + v2, 2), 'середня швидкість — не середнє арифметичне швидкостей на ділянках'), (F(str(s2)) / (F(str(t1)) + F(str(t3))), 'час зупинки не враховано'), (F(str(s2)), 'взято весь шлях'), (F(str(s2)) / F(str(rest)) , 'шлях поділено на час зупинки')]
        return T.add(lv, 'Знайдіть середню швидкість велосипедиста на всьому шляху (разом із зупинкою), км/год, за графіком.', av, wr, 'середня швидкість = весь шлях : весь час (зупинка входить у час)',
                     f'{fmt(F(str(s2)))} : {fmt(F(str(T2)))} = {fmt(av)} км/год', img=img)
    if kind == 'avgmove':
        av = F(str(s2)) / (F(str(t1)) + F(str(t3)))
        wr = [(F(str(s2)) / F(str(T2)), 'у час руху включено зупинку'), (F(v1 + v2, 2), 'середня швидкість — не середнє арифметичне швидкостей'), (F(str(s2)), 'взято весь шлях'), (F(str(s2)) / F(str(t3)), 'час першого відрізка не враховано')]
        return T.add(lv, 'Знайдіть середню швидкість велосипедиста лише під час руху (без урахування зупинки), км/год, за графіком.', av, wr, 'середня швидкість руху = весь шлях : час руху без зупинки',
                     f'{fmt(F(str(s2)))} : ({fmt(F(str(t1)))} + {fmt(F(str(t3)))}) = {fmt(av)} км/год', img=img)
    return False

FAMS += [(f_pie, [2, 3]), (f_bar, [2, 3]), (f_numline, [1, 2]), (f_disttime, [2, 3])]

ITEMS = [('Хліб', [18, 22, 25]), ('Молоко', [32, 36, 40]), ('Сир', [120, 150, 180]), ('Яблука, кг', [30, 40, 45]), ('Олія', [60, 75, 90]), ('Чай', [50, 70, 80]), ('Цукор, кг', [25, 30, 35]), ('Кава', [100, 120, 150]), ('Печиво', [20, 30, 40]), ('Сік', [35, 45, 55])]
def receipt_img(name, rows, hide=None):
    h = 70 + 30 * (len(rows) + 1)
    c = S.C(460, h, 'Касовий чек')
    cols = [20, 190, 270, 360]
    c.rect(10, 38, 440, 28, fill='#eef2ff', stroke=S.GRAY, sw=1)
    for x, t in zip(cols, ['Товар', 'К-сть', 'Ціна, грн', 'Сума, грн']): c.text(x, 57, t, size=13, bold=True)
    for r, (nm, q, p) in enumerate(rows):
        y = 66 + 30 * r
        c.rect(10, y, 440, 30, fill='#fff', stroke=S.GRAY, sw=1)
        c.text(cols[0], y + 20, nm, size=13); c.text(cols[1], y + 20, str(q), size=13); c.text(cols[2], y + 20, str(p), size=13)
        c.text(cols[3], y + 20, '?' if hide == r else str(q * p), size=13, bold=(hide == r), col=(S.RED if hide == r else S.INK))
    return c.save(name)

def f_receipt(T, rng, lv):
    k = rng.choice([3, 4]); its = rng.sample(ITEMS, k)
    rows = [(nm, rng.randint(1, 5), rng.choice(prs)) for nm, prs in its]
    tot = sum(q * p for _, q, p in rows)
    mode = rng.choice(['total', 'hidden', 'disc', 'change'])
    if lv == 1: mode = rng.choice(['total', 'change'])
    h = rng.randrange(k) if mode == 'hidden' else None
    img = receipt_img('t1_rc_' + S.tag(rows, mode), rows, hide=h)
    if mode == 'total':
        q0, p0 = rows[0][1], rows[0][2]
        wr = [(sum(p for _, _, p in rows), 'додано лише ціни, кількість не враховано'), (sum(q for _, q, _ in rows), 'додано кількості замість сум'), (tot - rows[0][1] * rows[0][2], 'не враховано один товар'), (tot + rows[-1][2], 'зайву одиницю останнього товару враховано')]
        return T.add(lv, 'За касовим чеком (на малюнку) знайдіть, скільки гривень потрібно заплатити за всі товари.', tot, wr, 'вартість = кількість · ціна; далі додайте суми всіх рядків', ' + '.join(str(q * p) for _, q, p in rows) + f' = {tot} грн', img=img)
    if mode == 'hidden':
        T_ = tot; known = sum(q * p for t, (_, q, p) in enumerate(rows) if t != h)
        # у чеку невідома лише сума в рядку h; питання — яка вона
        q, p = rows[h][1], rows[h][2]
        wr = [(q + p, 'кількість і ціну додано замість множення'), (p, 'взято ціну одиниці'), (q * p + p, 'додано зайву одиницю товару'), (F(p, q), 'ціну поділено на кількість')]
        return T.add(lv, f'У касовому чеку (на малюнку) сума в рядку «{rows[h][0]}» стерлась. Яким числом її треба замінити?', q * p, wr, 'сума в рядку = кількість · ціна', f'{q} · {p} = {q*p}', img=img)
    if mode == 'disc':
        d = rng.choice([10, 20, 25, 5, 15]);
        if (tot * d) % 100: return False
        fin = tot - tot * d // 100
        wr = [(tot * d // 100, 'знайдено розмір знижки, а не ціну зі знижкою'), (tot - d, 'відсоток відняли як гривні'), (tot + tot * d // 100, 'знижку додано до суми'), (F(tot * (100 - d), 10), 'зсув коми на розряд')]
        return T.add(lv, f'За чеком (на малюнку) покупець має знижку {d}% на всю покупку. Скільки гривень він заплатить?', fin, wr, 'ціна зі знижкою = сума · (100 − знижка)%', f'сума {tot} грн; {tot} · {100-d} : 100 = {fin} грн', img=img)
    pay = ((tot // 100) + 1) * 100 + rng.choice([0, 100])
    wr = [(pay + tot, 'суму чека додано до внесеної суми'), (tot, 'взято суму чека замість здачі'), (pay - tot + 10, 'арифметична помилка у відніманні'), (pay - rows[0][1] * rows[0][2], 'від внесеної суми віднято вартість лише першого товару')]
    return T.add(lv, f'Покупець розрахувався банкнотами на {pay} грн за покупку з чека (на малюнку). Скільки гривень здачі він має отримати?', pay - tot, wr, 'здача = внесена сума − сума чека', f'{pay} − {tot} = {pay - tot} грн', img=img)

FAMS += [(f_receipt, [1, 2, 3])]
IMGF = [f for f in FAMS if f[0].__name__ in ('f_pie', 'f_bar', 'f_numline', 'f_disttime', 'f_receipt')]
FAMS += IMGF + IMGF   # більша частка питань із малюнками
