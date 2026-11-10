"""Малюнкові родини: комбінаторика, ймовірність, статистика (тема 6)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgen import *
from fractions import Fraction as F
import math
import msvg as S
from msvg import C, Axes, tag, bars, pie

T = Topic(6, 'kombinatoryka_imovirnist')

# I1: Стовпчикова діаграма — середнє / медіана / мода
def f_img_bar_stats(T, rng, lv):
    n = rng.randint(4, 6)
    labels = [rng.choice(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]) for _ in range(n)]
    while len(set(labels)) < n:
        labels = rng.sample(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"], n)
    vals = [rng.randint(2, 15) for _ in range(n)]

    c = C(480, 300, "Кількість відвідувачів за днями")
    ymax = max(vals) + 3
    ax = Axes(c, 60, 50, 360, 200, 0, n + 1, 0, ymax, 1, max(1, ymax // 5), grid=True, labels=True)
    bars(c, ax, vals, labels, col=S.BLUE)
    nm = f"t6_bar_{tag(vals, labels)}"
    img = c.save(nm)

    if lv == 1:
        # Середнє
        ans = F(sum(vals), n)
        text = f"За стовпчиковою діаграмою визначте середнє арифметичне кількості відвідувачів."
        wrongs = [
            (max(vals), f"максимум {max(vals)}, а не середнє"),
            (sorted(vals)[n // 2], f"медіана, а не середнє"),
            (F(sum(vals), n + 1), f"поділили на {n+1} замість {n}"),
        ]
        trap = "середнє = сума / кількість"
        sol = f"({' + '.join(map(str, vals))}) / {n} = {fmt(ans)}"
    elif lv == 2:
        # Розмах
        ans = max(vals) - min(vals)
        text = f"За стовпчиковою діаграмою визначте розмах даних."
        wrongs = [
            (max(vals), f"максимум, а не розмах"),
            (min(vals), f"мінімум, а не розмах"),
            (F(sum(vals), n), f"середнє, а не розмах"),
        ]
        trap = "розмах = max − min"
        sol = f"{max(vals)} {MINUS} {min(vals)} = {ans}"
    else:
        # Медіана
        srt = sorted(vals)
        if n % 2 == 1:
            ans = srt[n // 2]
        else:
            ans = F(srt[n // 2 - 1] + srt[n // 2], 2)
        text = f"За стовпчиковою діаграмою визначте медіану кількості відвідувачів."
        wrongs = [
            (F(sum(vals), n), f"середнє = {fmt(F(sum(vals), n))}, а не медіана"),
            (max(vals), f"максимум, а не медіана"),
            (min(vals), f"мінімум, а не медіана"),
        ]
        trap = "впорядкуйте значення та знайдіть серединне"
        sol = f"впорядковано: {', '.join(map(str, srt))}, медіана = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# I2: Кругова діаграма — частка / ймовірність
def f_img_pie(T, rng, lv):
    k = rng.randint(3, 5)
    names = rng.sample(["футбол", "баскетбол", "волейбол", "теніс", "плавання", "біг"], k)
    raw = [rng.randint(5, 30) for _ in range(k)]
    total = sum(raw)

    c = C(420, 350, "Улюблені види спорту учнів")
    pie(c, 210, 190, 110, raw, labels=[f"{names[i]}\n{raw[i]}" for i in range(k)], size=11)
    nm = f"t6_pie_{tag(raw, names)}"
    img = c.save(nm)

    target_idx = rng.randint(0, k - 1)
    target_name = names[target_idx]
    target_val = raw[target_idx]

    if lv == 1:
        text = f"За круговою діаграмою визначте, яку частку становлять учні, що обрали {target_name}."
        ans = F(target_val, total)
        wrongs = [
            (F(target_val, total - target_val), f"{target_val}/({total}{MINUS}{target_val}) — неправильний знаменник"),
            (F(1, k), f"1/{k} — не всі рівні"),
            (F(total - target_val, total), f"решта, а не {target_name}"),
        ]
        trap = "частка = кількість обраних / загальна кількість"
        sol = f"{target_val}/{total} = {fmt(ans)}"
    else:
        text = f"За діаграмою: яка ймовірність, що навмання обраний учень вподобав {target_name}?"
        ans = F(target_val, total)
        wrongs = [
            (F(target_val, total - target_val), f"поділили на решту"),
            (F(max(raw), total), f"взяли найбільшу групу"),
            (F(1, k), f"1/{k} — не всі рівні"),
        ]
        trap = "P = сприятливих / всього"
        sol = f"P = {target_val}/{total} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# I3: Таблиця частот на малюнку → мода
def f_img_freq_table(T, rng, lv):
    vals = sorted(rng.sample(range(1, 20), rng.randint(4, 6)))
    freqs = [rng.randint(1, 8) for _ in vals]
    # Ensure unique mode
    max_f = max(freqs)
    while freqs.count(max_f) > 1:
        idx = rng.randint(0, len(freqs) - 1)
        if freqs[idx] == max_f:
            freqs[idx] -= 1
    max_f = max(freqs)
    mode_idx = freqs.index(max_f)
    mode_val = vals[mode_idx]
    n_total = sum(freqs)

    c = C(460, 140, "Таблиця частот")
    # Draw table
    cw = 50
    x0 = (460 - cw * (len(vals) + 1)) / 2
    y0 = 50
    for i in range(len(vals) + 2):
        c.line(x0 + i * cw, y0, x0 + i * cw, y0 + 60, col=S.AX, w=1)
    for j in range(3):
        c.line(x0, y0 + j * 30, x0 + (len(vals) + 1) * cw, y0 + j * 30, col=S.AX, w=1)
    c.text(x0 + cw / 2, y0 + 20, "xᵢ", size=12, anchor='middle', bold=True)
    c.text(x0 + cw / 2, y0 + 50, "nᵢ", size=12, anchor='middle', bold=True)
    for i, (v, f) in enumerate(zip(vals, freqs)):
        c.text(x0 + (i + 1.5) * cw, y0 + 20, str(v), size=12, anchor='middle')
        c.text(x0 + (i + 1.5) * cw, y0 + 50, str(f), size=12, anchor='middle')

    nm = f"t6_freq_{tag(vals, freqs)}"
    img = c.save(nm)

    if lv == 1:
        text = "За таблицею частот визначте моду вибірки."
        ans = mode_val
        mean = F(sum(v * f for v, f in zip(vals, freqs)), n_total)
        wrongs = [
            (mean, f"середнє = {fmt(mean)}, а не мода"),
            (max_f, f"частота {max_f} — це кількість, а не значення"),
            (vals[-1], f"максимальне значення, а не мода"),
        ]
        trap = "мода — значення з найбільшою частотою"
        sol = f"найбільша частота {max_f} у значення {mode_val} — це мода"
    else:
        text = "За таблицею частот знайдіть середнє зважене вибірки."
        ans = F(sum(v * f for v, f in zip(vals, freqs)), n_total)
        wrongs = [
            (F(sum(vals), len(vals)), f"середнє без ваг: {sum(vals)}/{len(vals)}"),
            (mode_val, f"мода, а не середнє"),
            (F(sum(v * f for v, f in zip(vals, freqs)), n_total + 1), f"поділили на {n_total+1}"),
        ]
        trap = "середнє зважене = Σxᵢ·nᵢ / Σnᵢ"
        sol = f"Σxᵢ·nᵢ = {sum(v*f for v,f in zip(vals, freqs))}, N = {n_total}, x̄ = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# I4: Дерево ймовірностей (2 рівні)
def f_img_tree(T, rng, lv):
    # Two urns
    n1, n2 = rng.randint(4, 8), rng.randint(4, 8)
    w1, w2 = rng.randint(1, n1 - 1), rng.randint(1, n2 - 1)
    b1, b2 = n1 - w1, n2 - w2

    c = C(500, 280, "Дерево ймовірностей")
    # Draw tree
    cx, cy = 80, 140
    # Branch to urns
    c.line(cx, cy, 200, 60, col=S.BLUE, w=2)
    c.line(cx, cy, 200, 220, col=S.BLUE, w=2)
    c.text(130, 80, "½", size=12, col=S.BLUE, bold=True)
    c.text(130, 200, "½", size=12, col=S.BLUE, bold=True)
    # Urna I
    c.text(210, 50, f"I: {w1}б, {b1}ч", size=11, bold=True)
    c.line(230, 60, 380, 30, col=S.GREEN, w=1.5)
    c.line(230, 60, 380, 90, col=S.RED, w=1.5)
    c.text(300, 30, f"{w1}/{n1}", size=11, col=S.GREEN, bold=True)
    c.text(300, 80, f"{b1}/{n1}", size=11, col=S.RED, bold=True)
    c.text(390, 25, "біла", size=10, col=S.GREEN)
    c.text(390, 85, "чорна", size=10, col=S.RED)
    # Urna II
    c.text(210, 215, f"II: {w2}б, {b2}ч", size=11, bold=True)
    c.line(230, 220, 380, 190, col=S.GREEN, w=1.5)
    c.line(230, 220, 380, 250, col=S.RED, w=1.5)
    c.text(300, 190, f"{w2}/{n2}", size=11, col=S.GREEN, bold=True)
    c.text(300, 240, f"{b2}/{n2}", size=11, col=S.RED, bold=True)
    c.text(390, 185, "біла", size=10, col=S.GREEN)
    c.text(390, 245, "чорна", size=10, col=S.RED)

    nm = f"t6_tree_{tag(n1, n2, w1, w2)}"
    img = c.save(nm)

    ans = F(1, 2) * F(w1, n1) + F(1, 2) * F(w2, n2)
    text = "За деревом ймовірностей знайдіть P(біла кулька)."
    wrongs = [
        (F(w1 + w2, n1 + n2), f"об'єднали: ({w1}+{w2})/({n1}+{n2})"),
        (F(w1, n1) * F(w2, n2), f"помножили P(б|I)·P(б|II)"),
        (F(w1, n1), f"тільки перша урна"),
    ]
    trap = "формула повної ймовірності"
    sol = f"½·{w1}/{n1} + ½·{w2}/{n2} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# I5: Гістограма частот
def f_img_histogram(T, rng, lv):
    # intervals
    start = rng.choice([0, 10, 20])
    step = rng.choice([5, 10])
    k = rng.randint(4, 6)
    bins = [(start + i * step, start + (i + 1) * step) for i in range(k)]
    freqs = [rng.randint(2, 15) for _ in range(k)]
    total = sum(freqs)

    c = C(500, 300, "Гістограма частот")
    ymax = max(freqs) + 3
    ax = Axes(c, 60, 50, 380, 200, start, start + k * step, 0, ymax, step, max(1, ymax // 4))
    for i, ((a, b), f) in enumerate(zip(bins, freqs)):
        X1, X2 = ax.X(a), ax.X(b)
        Y0, Yf = ax.Y(0), ax.Y(f)
        c.rect(X1, Yf, X2 - X1, Y0 - Yf, fill=S.LIGHT[i % len(S.LIGHT)], stroke=S.BLUE, sw=1.5)
        c.text((X1 + X2) / 2, Yf - 5, str(f), size=11, anchor='middle', bold=True)

    nm = f"t6_hist_{tag(bins, freqs)}"
    img = c.save(nm)

    if lv == 1:
        target_bin = rng.randint(0, k - 1)
        a, b = bins[target_bin]
        text = f"За гістограмою визначте відносну частоту інтервалу [{a}; {b})."
        ans = F(freqs[target_bin], total)
        wrongs = [
            (F(freqs[target_bin], total - freqs[target_bin]), f"поділили на решту"),
            (F(1, k), f"1/{k}"),
            (F(total - freqs[target_bin], total), f"решта інтервалів"),
        ]
        trap = "відносна частота = nᵢ / N"
        sol = f"{freqs[target_bin]}/{total} = {fmt(ans)}"
    else:
        text = "За гістограмою знайдіть вибіркове середнє (за серединами інтервалів)."
        mids = [(a + b) / 2 for a, b in bins]
        ans = F(sum(F(m) * f for m, f in zip(mids, freqs)), total)
        wrongs = [
            (F(sum(int(m) for m in mids), k), f"середнє середин: {sum(int(m) for m in mids)}/{k}"),
            (F(sum(freqs[i] * bins[i][0] for i in range(k)), total), "лівий край замість середини"),
            (max(mids), f"середина найбільшого — не середнє"),
        ]
        trap = "x̄ = Σmᵢ·nᵢ / N, де mᵢ — середина інтервалу"
        sol = f"x̄ = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# I6: Таблиця розподілу → M(X)
def f_img_dist_table(T, rng, lv):
    k = rng.randint(3, 5)
    xs = sorted(rng.sample(range(0, 8), k))
    ps_raw = [rng.randint(1, 5) for _ in range(k)]
    denom = sum(ps_raw)
    ps = [F(p, denom) for p in ps_raw]
    ps[-1] = 1 - sum(ps[:-1])

    c = C(460, 130)
    cw = 70
    x0 = (460 - cw * (k + 1)) / 2
    y0 = 20
    for i in range(k + 2):
        c.line(x0 + i * cw, y0, x0 + i * cw, y0 + 60, col=S.AX, w=1)
    for j in range(3):
        c.line(x0, y0 + j * 30, x0 + (k + 1) * cw, y0 + j * 30, col=S.AX, w=1)
    c.text(x0 + cw / 2, y0 + 20, "X", size=13, anchor='middle', bold=True)
    c.text(x0 + cw / 2, y0 + 50, "P", size=13, anchor='middle', bold=True)
    for i in range(k):
        c.text(x0 + (i + 1.5) * cw, y0 + 20, str(xs[i]), size=12, anchor='middle')
        c.text(x0 + (i + 1.5) * cw, y0 + 50, fmt(ps[i]), size=11, anchor='middle')

    nm = f"t6_dist_{tag(xs, ps_raw)}"
    img = c.save(nm)

    if lv <= 2:
        ans = sum(F(x) * p for x, p in zip(xs, ps))
        text = "За таблицею розподілу знайдіть математичне сподівання M(X)."
        wrongs = [
            (F(sum(xs), k), f"середнє значень: {sum(xs)}/{k}"),
            (max(xs), f"максимум, а не M(X)"),
            (ans + F(1, denom), f"помилка в обчисленні"),
        ]
        trap = "M(X) = Σxᵢ·pᵢ"
        sol = f"M(X) = {' + '.join(f'{x}·{fmt(p)}' for x, p in zip(xs, ps))} = {fmt(ans)}"
    else:
        mx = sum(F(x) * p for x, p in zip(xs, ps))
        ans = sum(F(x)**2 * p for x, p in zip(xs, ps)) - mx**2
        text = "За таблицею розподілу знайдіть дисперсію D(X)."
        wrongs = [
            (mx, f"M(X) = {fmt(mx)}, а не D(X)"),
            (sum(F(x)**2 * p for x, p in zip(xs, ps)), f"M(X²) без віднімання M(X)²"),
            (ans + F(1, denom), f"помилка в обчисленні"),
        ]
        trap = "D(X) = M(X²) − [M(X)]²"
        sol = f"M(X) = {fmt(mx)}, M(X²) = {fmt(sum(F(x)**2 * p for x,p in zip(xs, ps)))}, D = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# I7: Діаграма Ейлера-Венна
def f_img_venn(T, rng, lv):
    n_total = rng.randint(30, 60)
    a_only = rng.randint(5, 15)
    b_only = rng.randint(5, 15)
    ab = rng.randint(2, 8)
    rest = n_total - a_only - b_only - ab
    if rest < 0:
        return False

    c = C(420, 300, f"Опитування {n_total} учнів")
    # Draw circles
    c.circle(155, 165, 80, fill='#dbeafe80', stroke=S.BLUE, sw=2)
    c.circle(265, 165, 80, fill='#dcfce780', stroke=S.GREEN, sw=2)
    c.text(120, 170, str(a_only), size=16, anchor='middle', bold=True, col=S.BLUE)
    c.text(210, 170, str(ab), size=16, anchor='middle', bold=True, col=S.PURPLE)
    c.text(300, 170, str(b_only), size=16, anchor='middle', bold=True, col=S.GREEN)
    c.text(380, 270, str(rest), size=14, anchor='middle', col=S.GRAY)
    c.rect(40, 70, 340, 220, stroke=S.GRAY, sw=1, fill='none')
    c.text(155, 85, "Футбол", size=12, anchor='middle', col=S.BLUE, bold=True)
    c.text(265, 85, "Баскетбол", size=12, anchor='middle', col=S.GREEN, bold=True)

    nm = f"t6_venn_{tag(a_only, b_only, ab, rest)}"
    img = c.save(nm)

    if lv == 1:
        ans = a_only + ab
        text = "За діаграмою Венна визначте, скільки учнів грають у футбол."
        wrongs = [
            (a_only, f"тільки «тільки футбол»: {a_only} (без перетину)"),
            (ab, f"тільки перетин: {ab}"),
            (a_only + b_only + ab, f"усі, хто грає хоч щось"),
        ]
        trap = "футбол = «тільки футбол» + «обидва»"
        sol = f"{a_only} + {ab} = {ans}"
    else:
        text = "Яка ймовірність, що навмання обраний учень грає хоча б в один вид спорту?"
        ans = F(a_only + b_only + ab, n_total)
        wrongs = [
            (F(rest, n_total), f"обрали тих, хто не грає"),
            (F(a_only + b_only, n_total), f"без перетину: ({a_only}+{b_only})/{n_total}"),
            (F(ab, n_total), f"тільки перетин"),
        ]
        trap = "хоча б один = A ∪ B"
        sol = f"P = ({a_only}+{b_only}+{ab})/{n_total} = {a_only+b_only+ab}/{n_total} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# I8: Box-plot (ящик з вусами) → медіана / квартилі
def f_img_boxplot(T, rng, lv):
    mn = rng.randint(5, 15)
    q1 = mn + rng.randint(3, 8)
    med = q1 + rng.randint(2, 6)
    q3 = med + rng.randint(2, 6)
    mx = q3 + rng.randint(3, 8)

    c = C(460, 160, "Ящик з вусами")
    # Scale
    lo, hi = mn - 2, mx + 2
    x0, xw = 60, 340
    y0, bh = 70, 50
    def sx(v):
        return x0 + (v - lo) / (hi - lo) * xw
    # Whiskers
    c.line(sx(mn), y0 + bh / 2, sx(q1), y0 + bh / 2, col=S.INK, w=2)
    c.line(sx(q3), y0 + bh / 2, sx(mx), y0 + bh / 2, col=S.INK, w=2)
    c.line(sx(mn), y0 + 10, sx(mn), y0 + bh - 10, col=S.INK, w=2)
    c.line(sx(mx), y0 + 10, sx(mx), y0 + bh - 10, col=S.INK, w=2)
    # Box
    c.rect(sx(q1), y0, sx(q3) - sx(q1), bh, fill='#dbeafe', stroke=S.BLUE, sw=2)
    c.line(sx(med), y0, sx(med), y0 + bh, col=S.RED, w=2.5)
    # Labels
    for v, lab in [(mn, str(mn)), (q1, 'Q₁'), (med, 'Me'), (q3, 'Q₃'), (mx, str(mx))]:
        c.text(sx(v), y0 + bh + 18, lab, size=11, anchor='middle', bold=True)

    nm = f"t6_box_{tag(mn, q1, med, q3, mx)}"
    img = c.save(nm)

    if lv == 1:
        text = "За ящиком з вусами визначте медіану."
        ans = med
        wrongs = [
            (q1, f"Q₁ = {q1}, а не медіана"),
            (q3, f"Q₃ = {q3}, а не медіана"),
            (F(mn + mx, 2), f"середнє min і max: ({mn}+{mx})/2"),
        ]
        trap = "медіана — вертикальна лінія всередині ящика"
        sol = f"Me = {med}"
    else:
        ans = q3 - q1
        text = "За ящиком з вусами визначте міжквартильний розмах (IQR)."
        wrongs = [
            (mx - mn, f"повний розмах: {mx} {MINUS} {mn}"),
            (med - q1, f"Me {MINUS} Q₁ = {med - q1}"),
            (q3 - med, f"Q₃ {MINUS} Me = {q3 - med}"),
        ]
        trap = "IQR = Q₃ − Q₁"
        sol = f"IQR = {q3} {MINUS} {q1} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)


IMGF = [
    (f_img_bar_stats, [1, 2, 3]),
    (f_img_pie, [1, 2]),
    (f_img_freq_table, [1, 2]),
    (f_img_tree, [2, 3]),
    (f_img_histogram, [1, 2]),
    (f_img_dist_table, [2, 3]),
    (f_img_venn, [1, 2]),
    (f_img_boxplot, [1, 2]),
]

FAMS = IMGF
