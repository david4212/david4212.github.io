"""Текстові родини: планіметрія (тема 7)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgen import *
from fractions import Fraction as F
import math

T = Topic(7, 'planimetriya')
FAMS = []

def isqrt(n):
    """Цілий квадратний корінь або None."""
    r = int(math.isqrt(n))
    return r if r * r == n else None

MINUS = '−'

def ensure_unique(ans, wrongs):
    """Filter wrongs to ensure all values differ from ans and each other."""
    seen = {numval(ans)}
    out = []
    for val, reason in wrongs:
        k = numval(val)
        if k is not None and k not in seen:
            seen.add(k)
            out.append((val, reason))
    # pad if needed
    delta = 2
    while len(out) < 3:
        w = ans + delta
        k = numval(w)
        if k is not None and k not in seen:
            seen.add(k)
            out.append((w, f"помилка в обчисленні"))
        delta += 1
        if delta > 100:
            break
    return out[:3]

def sqrt_fmt(n):
    """Форматує √n красиво: √4 → 2, √12 → 2√3."""
    r = isqrt(n)
    if r is not None: return fmt(r)
    # спрощуємо: n = a²·b
    a = 1
    for p in range(2, int(n**0.5) + 1):
        while n % (p * p) == 0:
            a *= p; n //= p * p
    if a == 1: return f"√{n}"
    return f"{a}√{n}"

# ===== ТРИКУТНИКИ =====

def f_pyth(T, rng, lv):
    """Теорема Піфагора"""
    triples = [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(6,8,10),(9,12,15),(9,40,41)]
    a, b, c = rng.choice(triples)
    k = rng.randint(1, 3) if lv >= 2 else 1
    a, b, c = a*k, b*k, c*k
    text = f"У прямокутному трикутнику катети дорівнюють {a} і {b}. Знайдіть гіпотенузу."
    ans = c
    wrongs = [
        (a + b, f"додали катети: {a} + {b} = {a+b}"),
        (a * b, f"добуток катетів"),
        (isqrt(a**2 + b**2 + 1) or c + 1, f"помилка в обчисленні"),
    ]
    trap = "c² = a² + b²"
    sol = f"c = √({a}² + {b}²) = √{a**2 + b**2} = {c}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_triangle_area(T, rng, lv):
    """Площа трикутника"""
    if lv == 1:
        a = rng.randint(4, 15)
        h = rng.randint(3, 12)
        text = f"Знайдіть площу трикутника з основою {a} і висотою {h}."
        ans = F(a * h, 2)
        wrongs = [
            (a * h, f"не поділили на 2: {a}·{h} = {a*h}"),
            (F(a + h, 2), f"(a+h)/2 = {F(a+h,2)} — не площа"),
            (F(a * h, 3), f"поділили на 3 замість 2"),
        ]
        trap = "S = ½·a·h"
        sol = f"S = ½ · {a} · {h} = {fmt(ans)}"
    elif lv == 2:
        # Використовуємо лише кути з простим sin: 30°→½, 90°→1
        angle = rng.choice([30, 150])
        a = rng.randint(3, 10) * 2  # парне, щоб area було цілим
        b = rng.randint(3, 10)
        # sin(30°) = sin(150°) = ½
        area = F(a * b, 4)  # ½ · a · b · ½
        text = f"Знайдіть площу трикутника, якщо дві сторони {a} і {b}, а кут між ними {angle}°."
        ans = area
        wrongs_list = [
            (F(a * b, 2), f"½·a·b = {fmt(F(a*b,2))} (забули sin)"),
            (a * b, f"a·b = {a*b} (без ½ та sin)"),
            (F(a + b, 2), f"(a+b)/2 = {fmt(F(a+b,2))} — не площа"),
        ]
        trap = f"S = ½·a·b·sin({angle}°)"
        sol = f"S = ½·{a}·{b}·sin{angle}° = ½·{a}·{b}·½ = {fmt(ans)}"
        return T.add(lv, text, ans, wrongs_list, trap, sol)
    else:
        # Герон — використовуємо відомі Геронові трійки (цілочислова площа)
        HERON = [
            (3,4,5,6),(5,5,6,12),(5,5,8,12),(5,12,13,30),(6,8,10,24),
            (7,15,20,42),(9,10,17,36),(9,12,15,54),(10,13,13,60),
            (10,17,21,84),(12,16,20,96),(13,14,15,84),(13,20,21,126),
        ]
        a, b, c, area = rng.choice(HERON)
        p = F(a+b+c, 2)
        text = f"Сторони трикутника {a}, {b}, {c}. Знайдіть його площу (за формулою Герона)."
        ans = area
        wrongs = ensure_unique(ans, [
            (F(a*b, 2), f"½·{a}·{b} = {fmt(F(a*b,2))} (без висоти)"),
            (a + b + c, f"периметр, а не площа"),
            (area * 2, f"забули √"),
        ])
        trap = f"p = {fmt(p)}, S = √(p(p−a)(p−b)(p−c))"
        sol = f"p = {fmt(p)}, S = √({fmt(p)}·{fmt(p-a)}·{fmt(p-b)}·{fmt(p-c)}) = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_triangle_perimeter(T, rng, lv):
    """Периметр трикутника"""
    a = rng.randint(3, 15)
    b = rng.randint(3, 15)
    c = rng.randint(abs(a-b)+1, a+b-1)
    text = f"Периметр трикутника зі сторонами {a}, {b}, {c}."
    ans = a + b + c
    wrongs = [
        (F(a*b, 2), f"площа, а не периметр"),
        (a + b, f"тільки дві сторони: {a}+{b}"),
        (ans + rng.choice([-1, 1, 2]), f"помилка при додаванні"),
    ]
    trap = "P = a + b + c"
    sol = f"P = {a} + {b} + {c} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_sim_triangles(T, rng, lv):
    """Подібні трикутники"""
    a1 = rng.randint(3, 8)
    k = rng.choice([2, 3, 4])
    a2 = a1 * k
    b1 = rng.randint(3, 8)
    while b1 == a1:
        b1 = rng.randint(3, 8)
    ans = b1 * k
    wrongs = ensure_unique(ans, [
        (b1 + (a2 - a1), f"додали різницю: {b1} + {a2-a1}"),
        (F(b1 * a1, a2), f"поділили замість помножили"),
        (b1, f"та сама сторона без коефіцієнта"),
    ])
    text = f"Трикутники подібні. Сторона першого {a1}, відповідна сторона другого {a2}. Знайдіть сторону другого, відповідну стороні {b1} першого."
    trap = f"коефіцієнт подібності k = {a2}/{a1} = {k}"
    sol = f"k = {k}, сторона = {b1} · {k} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_median(T, rng, lv):
    """Медіана трикутника"""
    # Відомі трійки (a,b,c) де медіана до a — ціла або проста дріб
    MED_TRIPLES = [
        (4,5,7), (6,5,5), (8,5,9), (10,7,9), (6,7,5),
        (4,3,5), (8,7,7), (10,9,9), (6,5,7), (4,7,5),
    ]
    a, b, c = rng.choice(MED_TRIPLES)
    m_sq_int = 2*b**2 + 2*c**2 - a**2
    m_half = isqrt(m_sq_int)
    if m_half is None:
        return False
    ans = F(m_half, 2)
    text = f"Сторони трикутника: a = {a}, b = {b}, c = {c}. Знайдіть медіану до сторони a."
    wrongs = ensure_unique(ans, [
        (F(a, 2), f"a/2 = {fmt(F(a,2))} — це не медіана"),
        (F(a+b+c, 3), f"(a+b+c)/3 — не формула медіани"),
        (ans + 1, f"помилка в обчисленні"),
    ])
    trap = f"mₐ = ½√(2b²+2c²−a²)"
    sol = f"mₐ = ½√(2·{b}²+2·{c}²−{a}²) = ½√{m_sq_int} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

# ===== ЧОТИРИКУТНИКИ =====

def f_rect_area(T, rng, lv):
    """Площа прямокутника / паралелограма"""
    if lv == 1:
        a, b = rng.randint(3, 15), rng.randint(3, 15)
        text = f"Знайдіть площу прямокутника зі сторонами {a} і {b}."
        ans = a * b
        wrongs = [
            (2 * (a + b), f"периметр: 2({a}+{b}) = {2*(a+b)}"),
            (F(a * b, 2), f"поділили на 2: {a}·{b}/2"),
            ((a + b)**2, f"(a+b)² — неправильна формула"),
        ]
        trap = "S = a · b"
        sol = f"S = {a} · {b} = {ans}"
    else:
        a = rng.randint(5, 15)
        h = rng.randint(3, 12)
        text = f"Знайдіть площу паралелограма зі стороною {a} і висотою {h}."
        ans = a * h
        wrongs = ensure_unique(ans, [
            (F(a * h, 2), f"½·{a}·{h} — це площа трикутника"),
            (2 * a + 2 * h, f"периметр"),
            (a**2, f"a² — квадрат сторони"),
        ])
        trap = "S = a · h"
        sol = f"S = {a} · {h} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_trap_area(T, rng, lv):
    """Площа трапеції"""
    a = rng.randint(4, 12)
    b = rng.randint(a + 2, a + 10)
    h = rng.randint(3, 10)
    text = f"Основи трапеції {a} і {b}, висота {h}. Знайдіть площу."
    ans = F((a + b) * h, 2)
    wrongs = [
        ((a + b) * h, f"не поділили на 2: ({a}+{b})·{h}"),
        (a * h, f"тільки одна основа: {a}·{h}"),
        (F(a * b * h, 2), f"½·a·b·h — неправильна формула"),
    ]
    trap = "S = ½(a+b)·h"
    sol = f"S = ½·({a}+{b})·{h} = ½·{a+b}·{h} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_rhombus(T, rng, lv):
    """Площа ромба через діагоналі"""
    d1 = rng.randint(4, 16)
    d2 = rng.randint(4, 16)
    text = f"Діагоналі ромба дорівнюють {d1} і {d2}. Знайдіть площу."
    ans = F(d1 * d2, 2)
    wrongs = [
        (d1 * d2, f"d₁·d₂ = {d1*d2} (не поділили на 2)"),
        (2 * (d1 + d2), f"периметр: 2({d1}+{d2})"),
        (F(d1 + d2, 2), f"(d₁+d₂)/2 — не площа"),
    ]
    trap = "S = ½·d₁·d₂"
    sol = f"S = ½ · {d1} · {d2} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

# ===== КОЛО =====

def f_circle_area(T, rng, lv):
    """Площа та довжина кола"""
    r = rng.randint(3, 10)
    if lv == 1:
        text = f"Довжина кола з радіусом {r} дорівнює kπ. Знайдіть k."
        ans = 2 * r
        wrongs = ensure_unique(ans, [
            (r**2, f"πr² = π·{r}² — площа, не довжина"),
            (r, f"πr — забули множник 2"),
            (2 * r**2, f"2πr² — зайвий r"),
        ])
        trap = "C = 2πr"
        sol = f"C = 2π·{r} = {2*r}π"
    else:
        text = f"Площа круга з радіусом {r} дорівнює kπ. Знайдіть k."
        ans = r**2
        wrongs = ensure_unique(ans, [
            (2 * r, f"2πr = {2*r}π — довжина, не площа"),
            (r, f"πr — без квадрату"),
            (2 * r**2, f"2πr² — зайвий множник 2"),
        ])
        trap = "S = πr²"
        sol = f"S = π·{r}² = {r**2}π"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_inscribed_angle(T, rng, lv):
    """Вписаний кут"""
    central = rng.choice([60, 80, 100, 120, 140, 160])  # без 90 та 180
    inscribed = central // 2
    text = f"Центральний кут дорівнює {central}°. Знайдіть вписаний кут, що спирається на ту ж дугу."
    ans = inscribed
    wrongs = ensure_unique(ans, [
        (central, f"{central}° — це центральний, а не вписаний"),
        (180 - inscribed, f"180° − {inscribed}° = {180-inscribed}°"),
        (central * 2, f"подвоїли замість поділити"),
    ])
    trap = "вписаний кут = ½ центрального"
    sol = f"{central}° / 2 = {inscribed}°"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_tangent(T, rng, lv):
    """Дотична до кола"""
    r = rng.randint(3, 12)
    d = rng.randint(r + 1, r + 15)
    # дотична = √(d²-r²)
    t_sq = d**2 - r**2
    rt = isqrt(t_sq)
    if rt is None:
        return False
    text = f"Відстань від точки до центра кола дорівнює {d}, радіус {r}. Знайдіть довжину дотичної."
    ans = rt
    wrongs = [
        (d - r, f"d {MINUS} r = {d-r} (не Піфагор)"),
        (d + r, f"d + r = {d+r}"),
        (isqrt(d**2 + r**2) or rt + 2, f"√(d²+r²) замість √(d²−r²)"),
    ]
    trap = "t² = d² − r² (OT ⊥ дотичній)"
    sol = f"t = √({d}² {MINUS} {r}²) = √{t_sq} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

# ===== ТРИГОНОМЕТРІЯ =====

def f_sin_cos_rule(T, rng, lv):
    """Теорема косинусів (lv2) / синусів (lv3)"""
    if lv == 2:
        # Використовуємо відомі трійки для cos60°: c²=a²+b²−ab
        # a=b → c=a (рівносторонній); (3,5,7): 9+25-15=19 ні; (3,8): 9+64-24=49=7²!
        known = [(3,8,7,60),(5,8,7,60),(7,8,13,120),(3,5,7,60),(5,3,7,60),(7,3,8,120)]
        a, b, c, angle = rng.choice(known)
        text = f"Сторони трикутника a = {a}, b = {b}, кут між ними {angle}°. Знайдіть c."
        ans = c
        wrongs = ensure_unique(ans, [
            (a + b, f"a + b = {a+b}"),
            (abs(a - b), f"|a−b| = {abs(a-b)}"),
            (a * b, f"a·b — неправильна формула"),
        ])
        trap = f"c² = a² + b² − 2ab·cos(C)"
        sol = f"c² = {a}² + {b}² − 2·{a}·{b}·cos{angle}° = {c**2}, c = {ans}"
    else:
        # Теорема синусів: sin30°=½ → R = a
        a = rng.randint(4, 12)
        ans = a
        wrongs = ensure_unique(ans, [
            (F(a, 2), f"a/2 = {fmt(F(a,2))} (забули поділити на sin)"),
            (2 * a, f"2a = {2*a} (помножили замість поділити)"),
            (a + 2, f"помилка в обчисленні"),
        ])
        text = f"У трикутнику a = {a}, ∠A = 30°. Знайдіть радіус описаного кола R."
        trap = f"a/sin(A) = 2R → R = a/(2·sin30°) = a/(2·½) = a"
        sol = f"R = {a}/(2·sin30°) = {a}/(2·0,5) = {a}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_coord_distance(T, rng, lv):
    """Відстань між точками на площині"""
    # Гарантуємо достатньо великі відстані для різних wrongs
    found = False
    for _att in range(50):
        x1, y1 = rng.randint(-5, 5), rng.randint(-5, 5)
        x2, y2 = rng.randint(-5, 5), rng.randint(-5, 5)
        dx, dy = abs(x2-x1), abs(y2-y1)
        d_sq = dx**2 + dy**2
        if d_sq < 9: continue
        rd = isqrt(d_sq)
        if rd is None: continue
        manh = dx + dy
        maxc = max(dx, dy)
        if len({rd, manh, maxc}) == 3:
            found = True
            break
    if not found:
        return False
    text = f"Знайдіть відстань між точками A({x1}; {y1}) та B({x2}; {y2})."
    ans = rd
    wrongs = ensure_unique(ans, [
        (manh, f"|Δx|+|Δy| = {manh} (манхеттенська)"),
        (maxc, f"max(|Δx|,|Δy|) = {maxc}"),
        (rd + 2, f"помилка в обчисленні"),
    ])
    trap = f"d = √((x₂−x₁)² + (y₂−y₁)²)"
    sol = f"d = √({dx}² + {dy}²) = √{d_sq} = {ans}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_midpoint(T, rng, lv):
    """Середина відрізка"""
    x1, y1 = rng.randint(-8, 8), rng.randint(-8, 8)
    x2, y2 = rng.randint(-8, 8), rng.randint(-8, 8)
    mx, my = F(x1+x2, 2), F(y1+y2, 2)
    text = f"Знайдіть координати середини відрізка A({x1}; {y1}) B({x2}; {y2}). Відповідь: сума координат."
    ans = mx + my
    wrongs = [
        (mx, f"тільки x-координата: {fmt(mx)}"),
        (my, f"тільки y-координата: {fmt(my)}"),
        (F(x1+x2+y1+y2, 4), f"поділили суму всіх на 4"),
    ]
    trap = "M = ((x₁+x₂)/2; (y₁+y₂)/2)"
    sol = f"M = ({fmt(mx)}; {fmt(my)}), сума = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_polygon_angles(T, rng, lv):
    """Сума кутів многокутника"""
    n = rng.randint(5, 9)  # від 5, щоб ans != 360
    names = {5:"п'ятикутника", 6:"шестикутника", 7:"семикутника", 8:"восьмикутника", 9:"дев'ятикутника"}
    text = f"Знайдіть суму внутрішніх кутів {names[n]}."
    ans = 180 * (n - 2)
    wrongs = ensure_unique(ans, [
        (180 * n, f"180°·{n} = {180*n}° (без −2)"),
        (360, f"360° — це сума зовнішніх"),
        (180 * (n - 1), f"180°·({n}−1) — неправильна формула"),
    ])
    trap = f"S = 180°·(n−2)"
    sol = f"S = 180°·({n}−2) = 180°·{n-2} = {ans}°"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_regular_polygon(T, rng, lv):
    """Правильний многокутник: кут"""
    n = rng.choice([3, 5, 6, 8, 10, 12])  # без 4, щоб ans != 90
    angle = F(180 * (n - 2), n)
    text = f"Знайдіть внутрішній кут правильного {n}-кутника."
    ans = angle
    wrongs = ensure_unique(ans, [
        (F(360, n), f"360°/{n} = {fmt(F(360,n))}° — зовнішній кут"),
        (180, f"180°"),
        (F(180 * n, n + 2), f"неправильна формула"),
    ])
    trap = f"кут = 180°·(n−2)/n"
    sol = f"180°·({n}−2)/{n} = {fmt(angle)}°"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_sector_area(T, rng, lv):
    """Площа сектора"""
    r = rng.randint(3, 10)
    angle = rng.choice([60, 90, 120, 270])  # без 180 — менше колізій
    coef = F(r**2 * angle, 360)
    text = f"Знайдіть площу сектора з радіусом {r} і кутом {angle}°. Відповідь у вигляді kπ; знайдіть k."
    ans = coef
    wrongs = ensure_unique(ans, [
        (F(r**2, 1), f"πr² = {r**2}π — повне коло"),
        (F(2 * r * angle, 360), f"2πr·α/360 — довжина дуги"),
        (F(r**2 * angle, 180), f"πr²·α/180 — подвоїли"),
    ])
    trap = f"S = πr²·α/360°"
    sol = f"S = π·{r}²·{angle}/360 = {fmt(coef)}π"
    return T.add(lv, text, ans, wrongs, trap, sol)

def f_trig_right(T, rng, lv):
    """Тригонометрія прямокутного трикутника"""
    triples = [(3,4,5),(5,12,13),(8,15,17),(6,8,10)]
    a, b, c = rng.choice(triples)
    what = rng.choice(['sin', 'cos', 'tg'])
    if what == 'sin':
        text = f"У прямокутному трикутнику катети {a} і {b}, гіпотенуза {c}. Знайдіть sin кута при більшому катеті."
        if a > b: a, b = b, a
        ans = F(a, c)
        wrongs = [(F(b, c), f"cos замість sin"), (F(a, b), f"tg замість sin"), (F(c, a), f"перевернутий дріб")]
    elif what == 'cos':
        text = f"У прямокутному трикутнику катети {a} і {b}, гіпотенуза {c}. Знайдіть cos кута при більшому катеті."
        if a > b: a, b = b, a
        ans = F(b, c)
        wrongs = [(F(a, c), f"sin замість cos"), (F(a, b), f"tg замість cos"), (F(c, b), f"перевернутий дріб")]
    else:
        text = f"У прямокутному трикутнику катети {a} і {b}, гіпотенуза {c}. Знайдіть tg кута при більшому катеті."
        if a > b: a, b = b, a
        ans = F(a, b)
        wrongs = [(F(b, a), f"ctg замість tg"), (F(a, c), f"sin замість tg"), (F(b, c), f"cos замість tg")]
    trap = f"{what} = протилежний/..."
    sol = f"{what} = {fmt(ans)}"
    return T.add(lv, text, ans, wrongs, trap, sol)

# === Рівні для родин ===
FAMS1 = [
    (f_pyth, [1, 2]),
    (f_triangle_area, [1, 2, 3]),
    (f_triangle_perimeter, [1]),
    (f_sim_triangles, [2, 3]),
    (f_median, [3]),
    (f_rect_area, [1, 2]),
    (f_trap_area, [1, 2]),
    (f_rhombus, [2]),
    (f_circle_area, [1, 2]),
    (f_inscribed_angle, [1, 2]),
    (f_tangent, [2, 3]),
    (f_sin_cos_rule, [2, 3]),
    (f_coord_distance, [1, 2]),
    (f_midpoint, [1, 2]),
    (f_polygon_angles, [1, 2]),
    (f_regular_polygon, [2, 3]),
    (f_sector_area, [2, 3]),
    (f_trig_right, [1, 2, 3]),
]

FAMS = FAMS1

if __name__ == '__main__':
    T.strict = True
    T.run(FAMS, target=50)
    T.save()
    print('помилок:', T.errors)
