"""Текстові родини: комбінаторика, ймовірність, статистика (тема 6)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgen import *
from fractions import Fraction as F
import math

T = Topic(6, 'kombinatoryka_imovirnist')
FAMS = []

# ===== КОМБІНАТОРИКА =====

def f_perm(T, rng, lv):
    """Перестановки: P(n) = n!"""
    if lv == 1:
        n = rng.randint(4, 7)
        text = f"Скількома способами можна розставити {n} книжок на полиці?"
        ans = math.factorial(n)
        wrongs = [
            (n**2, f"помилково піднесли до квадрату: {n}² = {n**2}"),
            (2**n, f"помилково обчислили 2^{n} замість {n}!"),
            (math.factorial(n-1), f"обчислили ({n}{MINUS}1)! замість {n}!"),
        ]
    else:
        n = rng.randint(5, 8)
        k = rng.randint(2, 3)
        text = f"Скільки різних слів (навіть безглуздих) можна скласти з {n} різних літер, якщо кожна використовується рівно один раз?"
        ans = math.factorial(n)
        wrongs = [
            (n**n, f"помилково обчислили {n}^{n} (з повторенням)"),
            (math.factorial(n+1), f"обчислили ({n}+1)! замість {n}!"),
            (math.factorial(n)//2, f"помилково поділили на 2"),
        ]
    trap = f"перестановки P({n}) = {n}!"
    sol = f"P({n}) = {n}! = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_comb(T, rng, lv):
    """Комбінації C(n,k)"""
    n = rng.randint(6, 12)
    k = rng.randint(2, min(4, n-2))
    ctx = rng.choice([
        (f"Скількома способами можна обрати {k} дитини(-ей) із {n} для команди?",
         "порядок обрання не має значення"),
        (f"У магазині {n} видів цукерок. Скількома способами можна обрати {k}?",
         "вибір без урахування порядку"),
    ])
    text, trap_detail = ctx
    ans = math.comb(n, k)
    perm = math.perm(n, k)
    wrongs = [
        (perm, f"розміщення A({n},{k}) = {perm} (з порядком)"),
        (n * k, f"добуток {n}·{k} = {n*k} (неправильна формула)"),
        (math.comb(n, k+1) if k+1 <= n else math.comb(n, k-1), f"C({n},{k+1 if k+1<=n else k-1}) (неправильне k)"),
    ]
    trap = trap_detail
    sol = f"C({n},{k}) = {n}!/({k}!·{n-k}!) = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_arrange(T, rng, lv):
    """Розміщення A(n,k)"""
    n = rng.randint(5, 10)
    k = rng.randint(2, min(4, n-1))
    text = rng.choice([
        f"Скількома способами з {n} спортсменів можна роздати {k} різні медалі?",
        f"Скількома способами з {n} учнів можна обрати голову, заступника" + (f" і секретаря" if k >= 3 else "") + "?",
    ])
    ans = math.perm(n, k)
    wrongs = [
        (math.comb(n, k), f"C({n},{k}) = {math.comb(n,k)} (без порядку)"),
        (n**k, f"{n}^{k} = {n**k} (з повторенням)"),
        (math.perm(n, k-1) if k > 1 else n, f"A({n},{k-1}) (менше k)"),
    ]
    trap = f"порядок важливий → розміщення A({n},{k})"
    sol = f"A({n},{k}) = {n}!/({n-k})! = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_rule_product(T, rng, lv):
    """Правило добутку"""
    a = rng.randint(3, 7)
    b = rng.randint(3, 7)
    if lv == 1:
        text = f"У кафе {a} видів піци та {b} видів напоїв. Скількома способами можна обрати одну піцу й один напій?"
        ans = a * b
        wrongs = [
            (a + b, f"додали замість помножили: {a} + {b} = {a+b}"),
            (a * b + 1, f"зайвий +1"),
            (a * b * 2, f"помножили на 2 без причини"),
        ]
        trap = "правило добутку: множимо кількості"
        sol = f"{a} · {b} = {ans}"
    else:
        c = rng.randint(2, 5)
        text = f"Автомобільний номер складається з {a} літер (алфавіт — {b} літер) та {c} цифр. Скільки різних номерів можна скласти?"
        ans = b**a * 10**c
        wrongs = [
            (b * a * 10 * c, f"помножили як добуток: {b}·{a}·10·{c}"),
            (b**a + 10**c, f"додали замість помножили: {b}^{a} + 10^{c}"),
            (math.comb(b, a) * math.comb(10, c), f"комбінації замість степенів"),
        ]
        trap = f"правило добутку зі степенями: {b}^{a} · 10^{c}"
        sol = f"{b}^{a} · 10^{c} = {b**a} · {10**c} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_rule_sum(T, rng, lv):
    """Правило суми"""
    a = rng.randint(3, 8)
    b = rng.randint(3, 8)
    text = f"У класі {a} хлопців та {b} дівчат. Скількома способами можна обрати одного чергового?"
    ans = a + b
    wrongs = [
        (a * b, f"помножили замість додали: {a} · {b} = {a*b}"),
        (a + b - 1, f"помилковий {MINUS}1"),
        (a + b + 1, f"зайвий +1"),
    ]
    trap = "обираємо одного: правило суми"
    sol = f"{a} + {b} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

# ===== ЙМОВІРНІСТЬ =====

def f_prob_classic(T, rng, lv):
    """Класична ймовірність m/n"""
    if lv == 1:
        balls = rng.randint(3, 6)
        total = balls + rng.randint(3, 8)
        text = f"У мішку {balls} білих і {total - balls} чорних кульок. Яка ймовірність дістати білу?"
        ans = F(balls, total)
    elif lv == 2:
        n = rng.randint(6, 10)
        k = rng.randint(2, n - 2)
        text = f"Із {n} карток з числами 1–{n} навмання беруть одну. Яка ймовірність, що число на ній парне?"
        evens = n // 2
        ans = F(evens, n)
        k = evens
    else:
        n = rng.randint(8, 15)
        k = rng.randint(2, 4)
        text = f"Із {n} квитків {k} є виграшними. Навмання беруть 2 квитки. Яка ймовірність, що обидва виграшні?"
        ans = F(math.comb(k, 2), math.comb(n, 2))
    trap = "класична ймовірність: P = m/n"
    if lv == 1:
        wrongs = [
            (F(total - balls, total), f"взяли чорних: {total-balls}/{total}"),
            (F(balls, total - balls), f"поділили на чорних: {balls}/{total-balls}"),
            (F(1, total), f"поділили 1/{total}"),
        ]
        sol = f"P = {balls}/{total} = {fmt(ans)}"
    elif lv == 2:
        evens = n // 2
        wrongs = [
            (F(n - evens, n), f"непарних: {n - evens}/{n}"),
            (F(evens, evens + 1), f"неправильний знаменник"),
            (F(1, 2), f"не завжди рівно половина"),
        ]
        sol = f"парних: {evens}, P = {evens}/{n} = {fmt(ans)}"
    else:
        wrongs = [
            (F(k, n) * F(k-1, n-1), f"помилка: {k}/{n} · {k-1}/{n-1} без комбінацій"),
            (F(k, n)**2, f"({k}/{n})² — з поверненням"),
            (F(math.comb(k, 2), n**2), f"C({k},2)/{n}² — неправильний знаменник"),
        ]
        sol = f"P = C({k},2)/C({n},2) = {math.comb(k,2)}/{math.comb(n,2)} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_prob_dice(T, rng, lv):
    """Ймовірність при киданні кубика"""
    if lv == 1:
        target = rng.randint(1, 6)
        text = f"Кидають гральний кубик. Яка ймовірність випадіння числа {target}?"
        ans = F(1, 6)
        wrongs = [
            (F(1, 3), "помилка: 1/3"),
            (F(1, 2), "помилка: 1/2"),
            (F(target, 6), f"{target}/6 — число, а не кількість") if target != 1 else (F(2, 6), "2/6 замість 1/6"),
        ]
        trap = "класична ймовірність: 1 сприятливий із 6"
        sol = f"P = 1/6"
    elif lv == 2:
        k = rng.randint(2, 4)
        text = f"Кидають гральний кубик. Яка ймовірність випадіння числа, більшого за {6-k}?"
        ans = F(k, 6)
        wrongs = [
            (F(6-k, 6), f"взяли протилежне: {6-k}/6"),
            (F(k+1, 6) if k < 5 else F(k-1, 6), f"помилка на 1 у кількості"),
            (F(1, k), f"1/{k} — неправильний знаменник"),
        ]
        trap = f"числа {6-k+1}..6 — їх {k}"
        sol = f"P = {k}/6 = {fmt(ans)}"
    else:
        text = "Кидають два гральні кубики. Яка ймовірність, що сума очок дорівнює 7?"
        ans = F(6, 36)
        wrongs = [
            (F(1, 6), "помилка: 1/6 (не врахували всі пари)"),
            (F(7, 36), "7/36 — число 7, а не кількість пар"),
            (F(1, 12), "1/12 — неправильний підрахунок"),
        ]
        trap = "всього 36 рівноймовірних пар; сума 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) — 6 пар"
        sol = "P = 6/36 = 1/6"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_prob_complement(T, rng, lv):
    """Ймовірність протилежної події"""
    p_num = rng.randint(1, 9)
    p = F(p_num, 10)
    text = f"Ймовірність влучити в мішень дорівнює {fmt(p)}. Яка ймовірність промаху?"
    ans = 1 - p
    wrongs = [
        (p, f"взяли саму P замість 1 {MINUS} P"),
        (p / 2, f"поділили на 2 без причини"),
        (1 - p + F(1, 10), f"помилка ±0,1 в обчисленні"),
    ]
    trap = f"P(промах) = 1 {MINUS} P(влучення)"
    sol = f"1 {MINUS} {fmt(p)} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_prob_indep(T, rng, lv):
    """Ймовірність незалежних подій (множення)"""
    a_n = rng.randint(1, 4)
    a_d = rng.randint(a_n + 1, 6)
    b_n = rng.randint(1, 4)
    b_d = rng.randint(b_n + 1, 6)
    pa, pb = F(a_n, a_d), F(b_n, b_d)
    text = f"Ймовірність того, що перший стрілець влучить — {fmt(pa)}, другий — {fmt(pb)}. Яка ймовірність, що влучать обидва (події незалежні)?"
    ans = pa * pb
    wrongs = [
        (pa + pb, f"додали замість помножили: {fmt(pa)} + {fmt(pb)}"),
        (pa + pb - pa * pb, f"P(A∪B) = {fmt(pa+pb-pa*pb)} (хоча б один)"),
        ((pa + pb) / 2, f"середнє: ({fmt(pa)} + {fmt(pb)})/2"),
    ]
    trap = f"P(A ∩ B) = P(A) · P(B) для незалежних подій"
    sol = f"{fmt(pa)} · {fmt(pb)} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_prob_union(T, rng, lv):
    """Ймовірність об'єднання: P(A∪B)"""
    pa = F(rng.randint(1, 4), 10)
    pb = F(rng.randint(1, 4), 10)
    if lv <= 2:
        # несумісні
        text = f"Ймовірність події A дорівнює {fmt(pa)}, а події B — {fmt(pb)}. А і В несумісні. Знайдіть P(A ∪ B)."
        ans = pa + pb
        wrongs = [
            (pa * pb, f"помножили: P(A)·P(B) (для перетину, не об'єднання)"),
            (pa + pb - pa * pb, f"віднімали P(A)·P(B) — зайве для несумісних"),
            (max(pa, pb), f"взяли більшу"),
        ]
        trap = "несумісні → P(A ∪ B) = P(A) + P(B)"
        sol = f"{fmt(pa)} + {fmt(pb)} = {fmt(ans)}"
    else:
        pab = F(rng.randint(1, min(int(pa * 10), int(pb * 10))), 100)
        text = f"P(A) = {fmt(pa)}, P(B) = {fmt(pb)}, P(A ∩ B) = {fmt(pab)}. Знайдіть P(A ∪ B)."
        ans = pa + pb - pab
        wrongs = [
            (pa + pb, f"не відняли P(A ∩ B): {fmt(pa)} + {fmt(pb)} = {fmt(pa+pb)}"),
            (pa + pb + pab, f"додали P(A ∩ B) замість відняти"),
            (pa * pb, f"P(A)·P(B) замість формули включення-виключення"),
        ]
        trap = f"P(A ∪ B) = P(A) + P(B) {MINUS} P(A ∩ B)"
        sol = f"{fmt(pa)} + {fmt(pb)} {MINUS} {fmt(pab)} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_prob_geom(T, rng, lv):
    """Геометрична ймовірність"""
    big = rng.randint(5, 12)
    small = rng.randint(1, big - 1)
    text = f"На відрізку довжиною {big} навмання обирають точку. Яка ймовірність, що вона потрапить на частину довжиною {small}?"
    ans = F(small, big)
    wrongs = [
        (F(big - small, big), f"протилежна: ({big}{MINUS}{small})/{big}"),
        (F(small, big - small), f"поділили на решту: {small}/({big}{MINUS}{small})"),
        (F(1, big), f"1/{big} — лише одна точка"),
    ]
    trap = f"геометрична ймовірність: відношення довжин"
    sol = f"P = {small}/{big} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

# ===== СТАТИСТИКА =====

def f_mean(T, rng, lv):
    """Середнє арифметичне"""
    n = rng.randint(4, 7)
    vals = [rng.randint(2, 20) for _ in range(n)]
    s = sum(vals)
    ans = F(s, n)
    text = f"Знайдіть середнє арифметичне чисел: {', '.join(map(str, vals))}."
    wrongs = [
        (F(s, n - 1), f"поділили на {n-1} замість {n}"),
        (F(s, n + 1), f"поділили на {n+1} замість {n}"),
        (sorted(vals)[n // 2], "медіана, а не середнє"),
    ]
    trap = "середнє = сума / кількість"
    sol = f"({' + '.join(map(str, vals))}) / {n} = {s}/{n} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_median(T, rng, lv):
    """Медіана"""
    n = rng.choice([5, 7, 9]) if lv == 1 else rng.choice([4, 6, 8])
    vals = sorted([rng.randint(1, 30) for _ in range(n)])
    if n % 2 == 1:
        ans = vals[n // 2]
        sol = f"упорядковуємо, серединний елемент: {ans}"
    else:
        ans = F(vals[n // 2 - 1] + vals[n // 2], 2)
        sol = f"середнє двох серединних: ({vals[n//2-1]} + {vals[n//2]})/2 = {fmt(ans)}"
    text = f"Знайдіть медіану набору: {', '.join(map(str, vals))}."
    mean = F(sum(vals), n)
    wrongs = [
        (mean, f"середнє арифметичне = {fmt(mean)}, а не медіана"),
        (vals[0], f"мінімум: {vals[0]}"),
        (vals[-1], f"максимум: {vals[-1]}"),
    ]
    trap = "медіана — серединне значення впорядкованого ряду"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_mode(T, rng, lv):
    """Мода"""
    base = list(range(rng.randint(1, 5), rng.randint(8, 15)))
    mode_val = rng.choice(base)
    vals = base + [mode_val] * rng.randint(1, 3)
    rng.shuffle(vals)
    from collections import Counter
    cnt = Counter(vals)
    mode_val = cnt.most_common(1)[0][0]
    freq = cnt.most_common(1)[0][1]
    if freq <= 1:
        vals.append(mode_val)
        cnt = Counter(vals)
        mode_val = cnt.most_common(1)[0][0]
    text = f"Знайдіть моду набору: {', '.join(map(str, vals))}."
    ans = mode_val
    mean = F(sum(vals), len(vals))
    srt = sorted(vals)
    med = srt[len(srt) // 2]
    wrongs = [
        (mean, f"середнє = {fmt(mean)}, а не мода"),
        (med, f"медіана = {med}, а не мода"),
        (max(vals), f"максимум = {max(vals)}, а не мода"),
    ]
    trap = "мода — значення, що зустрічається найчастіше"
    sol = f"{mode_val} зустрічається {cnt[mode_val]} рази — це мода"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_range(T, rng, lv):
    """Розмах"""
    n = rng.randint(5, 8)
    vals = [rng.randint(1, 30) for _ in range(n)]
    ans = max(vals) - min(vals)
    text = f"Знайдіть розмах набору: {', '.join(map(str, vals))}."
    wrongs = [
        (max(vals), f"максимум {max(vals)}, а не розмах"),
        (min(vals), f"мінімум {min(vals)}, а не розмах"),
        (F(sum(vals), n), f"середнє, а не розмах"),
    ]
    trap = "розмах = max − min"
    sol = f"{max(vals)} {MINUS} {min(vals)} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_bernoulli(T, rng, lv):
    """Формула Бернуллі"""
    n = rng.randint(3, 6)
    k = rng.randint(1, n - 1)
    p_num = rng.choice([1, 2, 3])
    p = F(p_num, 10) if lv == 2 else F(1, rng.randint(2, 5))
    q = 1 - p
    ans = math.comb(n, k) * p**k * q**(n - k)
    text = f"Монету кидають {n} рази. Ймовірність герба p = {fmt(p)}. Знайдіть ймовірність рівно {k} гербів."
    wrongs_list = [
        (p**k * q**(n-k), f"забули C({n},{k}): p^{k}·q^{n-k}"),
        (math.comb(n, k) * p**k, f"забули q^{n-k}"),
        (math.comb(n, k) * p**(n-k) * q**k, f"переплутали p і q"),
    ]
    trap = f"формула Бернуллі: P = C(n,k)·p^k·q^(n{MINUS}k)"
    sol = f"C({n},{k})·{fmt(p)}^{k}·{fmt(q)}^{n-k} = {math.comb(n,k)}·{fmt(p**k)}·{fmt(q**(n-k))} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs_list, trap, sol)

def f_perm_repeat(T, rng, lv):
    """Перестановки з повторенням"""
    word_choices = [
        ("МАТЕМАТИКА", [3, 2, 1, 1, 1, 1, 1]),  # М-3, А-2, Т-1, Е-1, И-1, К-1
        ("СТАТИСТИКА", [2, 2, 2, 1, 1, 1, 1]),
        ("АНАНАС", [3, 2, 1]),
    ]
    word, reps = rng.choice(word_choices)
    n = sum(reps)
    denom = 1
    for r in reps:
        denom *= math.factorial(r)
    ans = math.factorial(n) // denom
    text = f"Скільки різних слів можна скласти з літер слова «{word}», використовуючи всі літери?"
    wrongs = [
        (math.factorial(n), f"{n}! = {math.factorial(n)} (без урахування повторень)"),
        (ans * 2, f"помножили зайве на 2"),
        (ans // 2 if ans > 1 else ans + 10, f"поділили зайве на 2"),
    ]
    trap = f"перестановки з повтореннями: {n}! / ({' · '.join(str(r)+'!' for r in reps if r > 1)})"
    sol = f"{n}! / ({' · '.join(str(r)+'!' for r in reps)}) = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_conditional(T, rng, lv):
    """Умовна ймовірність та повна ймовірність"""
    n1, n2 = rng.randint(3, 8), rng.randint(3, 8)
    k1 = rng.randint(1, n1 - 1)
    k2 = rng.randint(1, n2 - 1)
    text = (f"В урні I — {n1} кульок ({k1} білих), в урні II — {n2} кульок ({k2} білих). "
            f"Навмання обирають урну й дістають кульку. Яка ймовірність білої?")
    ans = F(1, 2) * F(k1, n1) + F(1, 2) * F(k2, n2)
    wrongs = [
        (F(k1 + k2, n1 + n2), f"об'єднали: ({k1}+{k2})/({n1}+{n2})"),
        (F(k1, n1) * F(k2, n2), f"помножили ймовірності"),
        (F(k1, n1), f"тільки перша урна"),
    ]
    trap = "формула повної ймовірності: P = P(I)·P(B|I) + P(II)·P(B|II)"
    sol = f"½·{k1}/{n1} + ½·{k2}/{n2} = {fmt(F(k1,2*n1))} + {fmt(F(k2,2*n2))} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_variance(T, rng, lv):
    """Дисперсія та середнє квадратичне відхилення"""
    n = rng.randint(4, 6)
    vals = [rng.randint(2, 15) for _ in range(n)]
    mean = F(sum(vals), n)
    var = sum((F(v) - mean)**2 for v in vals) / n
    text = f"Знайдіть дисперсію набору: {', '.join(map(str, vals))}."
    ans = var
    wrongs = [
        (sum(abs(F(v) - mean) for v in vals) / n, "середнє абсолютне відхилення, а не дисперсія"),
        (var * n / (n - 1), f"виправлена дисперсія (ділення на {n-1})"),
        (mean, f"середнє = {fmt(mean)}, а не дисперсія"),
    ]
    trap = "D = Σ(xᵢ − x̄)²/n"
    sol = f"x̄ = {fmt(mean)}, D = ({' + '.join(fmt((F(v) - mean)**2) for v in vals)})/{n} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_comb_with_rep(T, rng, lv):
    """Комбінації з повтореннями"""
    n = rng.randint(3, 5)
    k = rng.randint(2, 4)
    text = f"Скількома способами можна обрати {k} предмет(и/ів) із {n} видів, якщо предмети можуть повторюватися?"
    ans = math.comb(n + k - 1, k)
    wrongs = [
        (math.comb(n, k) if k <= n else n**k, f"C({n},{k}) без повторень" if k <= n else f"{n}^{k} (розміщення)"),
        (n**k, f"{n}^{k} — розміщення з повторенням"),
        (n * k, f"добуток {n}·{k}"),
    ]
    trap = f"комбінації з повтореннями: C(n+k{MINUS}1, k)"
    sol = f"C({n}+{k}{MINUS}1, {k}) = C({n+k-1}, {k}) = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_binom_coef(T, rng, lv):
    """Біноміальний коефіцієнт / трикутник Паскаля"""
    n = rng.randint(5, 10)
    k = rng.randint(2, n - 2)
    text = f"Знайдіть коефіцієнт при x^{k} у розкладі (1 + x)^{n}."
    ans = math.comb(n, k)
    wrongs = [
        (math.comb(n, k - 1), f"C({n},{k-1}) — помилка в степені"),
        (math.comb(n, k + 1) if k + 1 <= n else math.comb(n, k - 2), f"C({n},{k+1 if k+1<=n else k-2})"),
        (n**k, f"{n}^{k} — неправильна формула"),
    ]
    trap = f"біном Ньютона: коефіцієнт = C(n,k)"
    sol = f"C({n},{k}) = {n}!/({k}!·{n-k}!) = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_expected(T, rng, lv):
    """Математичне сподівання"""
    k = rng.randint(3, 5)
    xs = sorted(rng.sample(range(0, 10), k))
    ps_raw = [rng.randint(1, 5) for _ in range(k)]
    s = sum(ps_raw)
    ps = [F(p, s) for p in ps_raw]
    while sum(ps) != 1:
        ps[-1] = 1 - sum(ps[:-1])
    ans = sum(F(x) * p for x, p in zip(xs, ps))
    text = (f"Випадкова величина X набуває значень {', '.join(map(str, xs))} "
            f"з ймовірностями {', '.join(fmt(p) for p in ps)}. Знайдіть M(X).")
    wrongs = [
        (F(sum(xs), k), f"середнє значень: {sum(xs)}/{k}"),
        (max(xs) * max(ps), f"max·max = {max(xs)}·{fmt(max(ps))}"),
        (ans + F(1, s), f"помилка в обчисленні"),
    ]
    trap = "M(X) = Σxᵢ·pᵢ"
    sol = f"M(X) = {' + '.join(f'{x}·{fmt(p)}' for x, p in zip(xs, ps))} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_freq(T, rng, lv):
    """Відносна частота"""
    n = rng.choice([50, 100, 200])
    m = rng.randint(5, n - 5)
    while math.gcd(m, n) < 2 and lv == 1:
        m = rng.randint(5, n - 5)
    text = f"У {n} дослідах подія A настала {m} разів. Знайдіть відносну частоту події A."
    ans = F(m, n)
    wrongs = [
        (F(n - m, n), f"протилежна: {n-m}/{n}"),
        (F(n, m) if m != 0 else F(1, 1), f"навпаки: {n}/{m}"),
        (F(m, n - m) if n != m else F(1, 1), f"{m}/({n}{MINUS}{m}) — неправильний знаменник"),
    ]
    trap = "відносна частота W = m/n"
    sol = f"W = {m}/{n} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

# === Рівні для родин ===
FAMS1 = [
    (f_perm, [1, 2]),
    (f_comb, [1, 2]),
    (f_arrange, [1, 2]),
    (f_rule_product, [1, 2, 3]),
    (f_rule_sum, [1]),
    (f_prob_classic, [1, 2, 3]),
    (f_prob_dice, [1, 2, 3]),
    (f_prob_complement, [1, 2]),
    (f_prob_indep, [2, 3]),
    (f_prob_union, [2, 3]),
    (f_prob_geom, [1, 2]),
    (f_mean, [1]),
    (f_median, [1, 2]),
    (f_mode, [1]),
    (f_range, [1]),
    (f_bernoulli, [2, 3]),
    (f_perm_repeat, [2, 3]),
    (f_conditional, [3]),
    (f_variance, [2, 3]),
    (f_comb_with_rep, [3]),
    (f_binom_coef, [2, 3]),
    (f_expected, [2, 3]),
    (f_freq, [1, 2]),
]

FAMS = FAMS1

if __name__ == '__main__':
    T.strict = True
    T.run(FAMS, target=55)
    T.save()
    print('помилок:', T.errors)
