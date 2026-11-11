"""Родини з малюнками: планіметрія (тема 7)."""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgen import *
from msvg import *
from fractions import Fraction as Fr
from t7 import ensure_unique

T = Topic(7, 'planimetriya')

# ===== Допоміжні =====
def rot(cx, cy, x, y, a):
    """Поворот (x,y) навколо (cx,cy) на кут a (рад)."""
    dx, dy = x - cx, y - cy
    return cx + dx*math.cos(a) - dy*math.sin(a), cy + dx*math.sin(a) + dy*math.cos(a)

def reg_poly(cx, cy, r, n, start=-math.pi/2):
    return [(cx + r*math.cos(start + 2*math.pi*i/n), cy + r*math.sin(start + 2*math.pi*i/n)) for i in range(n)]

# ===== 1. Прямокутний трикутник (Піфагор) =====
def f_img_right_tri(T, rng, lv):
    triples = [(3,4,5),(5,12,13),(6,8,10),(8,15,17),(9,12,15)]
    a, b, c = rng.choice(triples)
    k = rng.randint(1, 3) if lv >= 2 else 1
    a, b, c = a*k, b*k, c*k

    # Що шукаємо
    hide = rng.choice(['a','b','c']) if lv >= 2 else 'c'

    W, H = 360, 300
    cv = C(W, H)
    # Трикутник: прямий кут у лівому нижньому
    ox, oy = 60, 250
    s = min(220/max(a,b), 25)
    Ax, Ay = ox, oy
    Bx, By = ox + b*s, oy
    Cx, Cy = ox, oy - a*s

    cv.poly([(Ax,Ay),(Bx,By),(Cx,Cy)], fill=LIGHT[0], stroke=BLUE, w=2)
    right_angle(cv, (Ax,Ay), (Bx,By), (Cx,Cy), s=12)
    poly_label(cv, [(Ax,Ay),(Bx,By),(Cx,Cy)], ['A','B','C'], off=16, col=INK)

    cent = ((Ax+Bx+Cx)/3, (Ay+By+Cy)/3)
    if hide == 'a':
        side_label(cv, (Ax,Ay), (Cx,Cy), '?', cent, col=RED)
        side_label(cv, (Ax,Ay), (Bx,By), str(b), cent, col=BLUE)
        side_label(cv, (Bx,By), (Cx,Cy), str(c), cent, col=BLUE)
        ans = a
        text = f"Знайдіть катет AC (рис.)."
        sol = f"AC = √({c}²−{b}²) = √{c**2-b**2} = {a}"
        wrongs = ensure_unique(a, [(c-b, f"c−b = {c-b}"), (a+1, f"помилка в обчисленні"), (b, f"переплутали катети")])
    elif hide == 'b':
        side_label(cv, (Ax,Ay), (Cx,Cy), str(a), cent, col=BLUE)
        side_label(cv, (Ax,Ay), (Bx,By), '?', cent, col=RED)
        side_label(cv, (Bx,By), (Cx,Cy), str(c), cent, col=BLUE)
        ans = b
        text = f"Знайдіть катет AB (рис.)."
        sol = f"AB = √({c}²−{a}²) = √{c**2-a**2} = {b}"
        wrongs = ensure_unique(b, [(c-a, f"c−a = {c-a}"), (b+1, f"помилка"), (a, f"переплутали катети")])
    else:
        side_label(cv, (Ax,Ay), (Cx,Cy), str(a), cent, col=BLUE)
        side_label(cv, (Ax,Ay), (Bx,By), str(b), cent, col=BLUE)
        side_label(cv, (Bx,By), (Cx,Cy), '?', cent, col=RED)
        ans = c
        text = f"Знайдіть гіпотенузу BC (рис.)."
        sol = f"BC = √({a}²+{b}²) = √{a**2+b**2} = {c}"
        wrongs = ensure_unique(c, [(a+b, f"a+b = {a+b}"), (c+1, f"помилка"), (a*b, f"добуток катетів")])

    nm = f"t7_right_{tag(a,b,c,hide,lv)}"
    img = cv.save(nm)
    trap = "c² = a² + b²"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 2. Коло: вписаний кут =====
def f_img_inscribed(T, rng, lv):
    central = rng.choice([60, 80, 100, 120, 140, 160])
    inscribed = central // 2

    W, H = 360, 340
    cv = C(W, H)
    cx, cy, r = 180, 170, 120

    cv.circle(cx, cy, r, stroke=BLUE, sw=2)
    cv.dot(cx, cy, r=3, col=GRAY)

    # Дуга: A і B на колі, C на протилежному боці
    a_angle = math.radians(-20)
    b_angle = math.radians(-20 + central)
    # вписаний кут C на протилежному боці
    c_angle = math.radians(-20 + central + 180)

    A = (cx + r*math.cos(a_angle), cy + r*math.sin(a_angle))
    B = (cx + r*math.cos(b_angle), cy + r*math.sin(b_angle))
    Cp = (cx + r*math.cos(c_angle), cy + r*math.sin(c_angle))

    # Центральний кут
    cv.line(cx, cy, A[0], A[1], col=GREEN, w=1.5)
    cv.line(cx, cy, B[0], B[1], col=GREEN, w=1.5)
    angle_arc(cv, (cx,cy), A, B, r=30, col=GREEN, label=f"{central}°")

    # Вписаний кут
    cv.line(Cp[0], Cp[1], A[0], A[1], col=RED, w=2)
    cv.line(Cp[0], Cp[1], B[0], B[1], col=RED, w=2)
    angle_arc(cv, Cp, A, B, r=28, col=RED, label="?")

    cv.dot(A[0], A[1], col=BLUE)
    cv.dot(B[0], B[1], col=BLUE)
    cv.dot(Cp[0], Cp[1], col=RED)

    poly_label(cv, [A, B, Cp], ['A','B','C'], off=18, col=INK, centre=(cx,cy))
    cv.text(cx-8, cy+16, 'O', size=12, col=GRAY)

    nm = f"t7_inscr_{tag(central,lv)}"
    img = cv.save(nm)

    text = "Знайдіть вписаний кут ACB (рис.)."
    ans = inscribed
    wrongs = ensure_unique(inscribed, [
        (central, f"це центральний кут, а не вписаний"),
        (180 - inscribed, f"180°−{inscribed}° = {180-inscribed}°"),
        (central + inscribed, f"сума замість половини"),
    ])
    trap = "вписаний = ½ центрального"
    sol = f"∠ACB = {central}°/2 = {inscribed}°"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 3. Площа трикутника з малюнком =====
def f_img_tri_area(T, rng, lv):
    base = rng.randint(4, 14)
    height = rng.randint(3, 12)
    area = Fr(base * height, 2)

    W, H = 380, 300
    cv = C(W, H)
    s = min(200/base, 180/height, 18)
    ox = 60
    oy = 260

    Ax, Ay = ox, oy
    Bx, By = ox + base*s, oy
    # верхня вершина — зсув вправо трохи
    top_off = rng.randint(int(base*s*0.2), int(base*s*0.8))
    Cx, Cy = ox + top_off, oy - height*s

    cv.poly([(Ax,Ay),(Bx,By),(Cx,Cy)], fill=LIGHT[0], stroke=BLUE, w=2)

    # висота — пунктир
    Hx, Hy = Cx, Ay  # точка під вершиною на основі
    cv.line(Cx, Cy, Hx, Hy, col=RED, w=1.5, dash="5,4")
    right_angle(cv, (Hx,Hy), (Bx,By), (Cx,Cy), s=10, col=RED)

    cent = ((Ax+Bx+Cx)/3, (Ay+By+Cy)/3)
    side_label(cv, (Ax,Ay), (Bx,By), str(base), cent, col=BLUE, off=18)
    # висота — підпис збоку
    cv.text(Hx+8, (Cy+Hy)/2, f"h={height}", size=12, col=RED, bold=True)

    poly_label(cv, [(Ax,Ay),(Bx,By),(Cx,Cy)], ['A','B','C'], off=16, col=INK)

    nm = f"t7_tarea_{tag(base,height,lv)}"
    img = cv.save(nm)

    text = "Знайдіть площу трикутника (рис.)."
    ans = area
    wrongs = ensure_unique(area, [
        (base*height, f"не поділили на 2: {base}·{height} = {base*height}"),
        (base+height, f"сума: {base}+{height} — не площа"),
        (Fr(base*height,3), f"поділили на 3 замість 2"),
    ])
    trap = "S = ½·a·h"
    sol = f"S = ½·{base}·{height} = {fmt(area)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 4. Трапеція =====
def f_img_trap(T, rng, lv):
    a = rng.randint(4, 10)  # верхня основа
    b = rng.randint(a+3, a+10)  # нижня основа
    h = rng.randint(3, 8)
    area = Fr((a+b)*h, 2)

    W, H = 400, 300
    cv = C(W, H)
    s = min(240/b, 180/h, 20)

    ox = 80; oy = 250
    # нижня основа
    Ax, Ay = ox, oy
    Bx, By = ox + b*s, oy
    # верхня — зсунута вправо
    off_top = (b-a)*s*0.4
    Dx, Dy = ox + off_top, oy - h*s
    Cx, Cy = Dx + a*s, Dy

    cv.poly([(Ax,Ay),(Bx,By),(Cx,Cy),(Dx,Dy)], fill=LIGHT[2], stroke=GREEN, w=2)

    # висота
    Hx = Dx
    cv.line(Dx, Dy, Hx, Ay, col=RED, w=1.5, dash="5,4")
    right_angle(cv, (Hx,Ay), (Bx,By), (Dx,Dy), s=10, col=RED)

    cent = ((Ax+Bx+Cx+Dx)/4, (Ay+By+Cy+Dy)/4)
    side_label(cv, (Ax,Ay), (Bx,By), str(b), cent, off=18, col=GREEN)
    side_label(cv, (Dx,Dy), (Cx,Cy), str(a), cent, off=18, col=GREEN)
    cv.text(Hx+8, (Dy+Ay)/2, f"h={h}", size=12, col=RED, bold=True)

    poly_label(cv, [(Ax,Ay),(Bx,By),(Cx,Cy),(Dx,Dy)], ['A','B','C','D'], off=16, col=INK)

    nm = f"t7_trap_{tag(a,b,h,lv)}"
    img = cv.save(nm)

    text = "Знайдіть площу трапеції (рис.)."
    ans = area
    wrongs = [
        ((a+b)*h, f"не поділили на 2"),
        (a*h, f"тільки верхня основа: {a}·{h}"),
        (Fr(a*b*h, 2), f"½·a·b·h — неправильна формула"),
    ]
    trap = "S = ½(a+b)·h"
    sol = f"S = ½·({a}+{b})·{h} = {fmt(area)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 5. Коло: дотична =====
def f_img_tangent(T, rng, lv):
    # Відомі (r, d) з цілою дотичною: r²+t²=d²
    TANG_TRIPLES = [
        (3,5,4),(4,5,3),(5,13,12),(6,10,8),(8,10,6),
        (8,17,15),(9,15,12),(5,10,None),(3,4,None),
    ]
    from t7 import isqrt
    r_val = rng.randint(3, 10)
    found = False
    for _ in range(30):
        d = rng.randint(r_val+2, r_val+15)
        t_sq = d**2 - r_val**2
        rt = isqrt(t_sq)
        if rt is not None:
            found = True
            break
    if not found:
        return False

    W, H = 400, 320
    cv = C(W, H)

    cx, cy = 160, 160
    sc = min(100/d, 12)
    R = r_val * sc
    D = d * sc
    T_len = rt * sc

    # Точка P правіше
    Px, Py = cx + D, cy

    # Точка дотику T — на колі
    angle_t = math.acos(R/D)
    Tx = cx + R*math.cos(angle_t)
    Ty = cy - R*math.sin(angle_t)

    cv.circle(cx, cy, R, stroke=BLUE, sw=2)
    cv.dot(cx, cy, r=3, col=GRAY)
    cv.text(cx-14, cy+4, 'O', size=13, col=GRAY, bold=True)

    # Радіус до T
    cv.line(cx, cy, Tx, Ty, col=GREEN, w=1.5)
    # PT — дотична
    cv.line(Px, Py, Tx, Ty, col=RED, w=2)
    # OP
    cv.line(cx, cy, Px, Py, col=INK, w=1.5, dash="4,3")

    right_angle(cv, (Tx,Ty), (cx,cy), (Px,Py), s=10, col=RED)

    cv.dot(Px, Py, col=RED)
    cv.dot(Tx, Ty, col=GREEN)

    cv.text(Px+8, Py+4, 'P', size=13, col=RED, bold=True)
    cv.text(Tx-14, Ty-8, 'T', size=13, col=GREEN, bold=True)

    # Підписи довжин
    mx1, my1 = (cx+Px)/2, cy+18
    cv.text(mx1, my1, f"OP = {d}", size=12, col=INK, anchor='middle')
    mx2, my2 = (cx+Tx)/2-12, (cy+Ty)/2-4
    cv.text(mx2, my2, f"r = {r_val}", size=12, col=GREEN, anchor='middle')

    nm = f"t7_tang_{tag(r_val,d,lv)}"
    img = cv.save(nm)

    text = "Знайдіть довжину дотичної PT (рис.)."
    ans = rt
    wrongs = [
        (d - r_val, f"d−r = {d-r_val}"),
        (d + r_val, f"d+r = {d+r_val}"),
        (rt + 1, f"помилка в обчисленні"),
    ]
    trap_hint = "PT² = OP² − r²"
    sol = f"PT = √({d}²−{r_val}²) = √{t_sq} = {rt}"
    return T.add(lv, text, ans, wrongs, trap_hint, sol, img=img)

# ===== 6. Паралелограм =====
def f_img_parallelogram(T, rng, lv):
    a = rng.randint(5, 12)
    h = rng.randint(3, 10)
    area = a * h

    W, H = 400, 300
    cv = C(W, H)
    s = min(200/a, 160/h, 18)

    ox, oy = 60, 250
    shift = rng.randint(int(2*s), int(4*s))  # зсув верхньої сторони

    Ax, Ay = ox, oy
    Bx, By = ox + a*s, oy
    Cx, Cy = Bx + shift, oy - h*s
    Dx, Dy = Ax + shift, oy - h*s

    cv.poly([(Ax,Ay),(Bx,By),(Cx,Cy),(Dx,Dy)], fill=LIGHT[3], stroke=PURPLE, w=2)

    # висота
    cv.line(Dx, Dy, Dx, Ay, col=RED, w=1.5, dash="5,4")
    right_angle(cv, (Dx,Ay), (Bx,By), (Dx,Dy), s=10, col=RED)

    cent = ((Ax+Bx+Cx+Dx)/4, (Ay+By+Cy+Dy)/4)
    side_label(cv, (Ax,Ay), (Bx,By), str(a), cent, off=18, col=PURPLE)
    cv.text(Dx+8, (Dy+Ay)/2, f"h={h}", size=12, col=RED, bold=True)

    poly_label(cv, [(Ax,Ay),(Bx,By),(Cx,Cy),(Dx,Dy)], ['A','B','C','D'], off=16, col=INK)

    nm = f"t7_para_{tag(a,h,lv)}"
    img = cv.save(nm)

    text = "Знайдіть площу паралелограма (рис.)."
    ans = area
    wrongs = [
        (Fr(a*h,2), f"½·{a}·{h} — площа трикутника"),
        (2*(a+h), f"периметр"),
        (a**2, f"квадрат сторони"),
    ]
    trap = "S = a · h"
    sol = f"S = {a} · {h} = {area}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 7. Ромб: діагоналі =====
def f_img_rhombus(T, rng, lv):
    d1 = rng.randint(4, 14)
    d2 = rng.randint(4, 14)
    area = Fr(d1*d2, 2)

    W, H = 360, 340
    cv = C(W, H)

    cx, cy = 180, 170
    s = min(120/max(d1,d2), 15)
    hw, hh = d1*s/2, d2*s/2

    A = (cx, cy - hh)  # верх
    B = (cx + hw, cy)   # право
    Cp = (cx, cy + hh)  # низ
    D = (cx - hw, cy)   # ліво

    cv.poly([A, B, Cp, D], fill=LIGHT[5], stroke='#0891b2', w=2)

    # діагоналі
    cv.line(A[0], A[1], Cp[0], Cp[1], col=RED, w=1.5, dash="5,4")
    cv.line(B[0], B[1], D[0], D[1], col=GREEN, w=1.5, dash="5,4")
    right_angle(cv, (cx,cy), B, A, s=10, col=GRAY)

    cv.text(cx+6, cy-hh/2-4, f"d₂={d2}", size=12, col=RED, bold=True)
    cv.text(cx+hw/2+4, cy+14, f"d₁={d1}", size=12, col=GREEN, bold=True)

    poly_label(cv, [A, B, Cp, D], ['A','B','C','D'], off=16, col=INK, centre=(cx,cy))

    nm = f"t7_rhomb_{tag(d1,d2,lv)}"
    img = cv.save(nm)

    text = "Знайдіть площу ромба (рис.)."
    ans = area
    wrongs = [
        (d1*d2, f"d₁·d₂ = {d1*d2} (без /2)"),
        (2*(d1+d2), f"2(d₁+d₂) = {2*(d1+d2)} — периметр"),
        (Fr(d1+d2,2), f"(d₁+d₂)/2 — не площа"),
    ]
    trap = "S = ½·d₁·d₂"
    sol = f"S = ½·{d1}·{d2} = {fmt(area)}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 8. Коло та сектор =====
def f_img_sector(T, rng, lv):
    r_val = rng.randint(3, 10)
    angle = rng.choice([60, 90, 120, 270])
    coef = Fr(r_val**2 * angle, 360)

    W, H = 360, 340
    cv = C(W, H)

    cx, cy = 180, 180
    R = min(120, r_val * 14)

    a1 = math.radians(-angle/2)
    a2 = math.radians(angle/2)

    x1, y1 = cx + R*math.cos(a1), cy + R*math.sin(a1)
    x2, y2 = cx + R*math.cos(a2), cy + R*math.sin(a2)
    large = 1 if angle > 180 else 0

    cv.path(f'M{n(cx)},{n(cy)} L{n(x1)},{n(y1)} A{R},{R} 0 {large} 1 {n(x2)},{n(y2)} Z',
            fill=LIGHT[0], stroke=BLUE, w=2)

    cv.dot(cx, cy, r=3, col=GRAY)

    angle_arc(cv, (cx,cy), (x1,y1), (x2,y2), r=30, col=ORANGE, label=f"{angle}°")

    mx = cx + R*0.5*math.cos(0)
    cv.text(mx, cy-10, f"r = {r_val}", size=13, col=BLUE, bold=True, anchor='middle')

    nm = f"t7_sect_{tag(r_val,angle,lv)}"
    img = cv.save(nm)

    text = f"Площа сектора = kπ. Знайдіть k (рис.)."
    ans = coef
    wrongs = ensure_unique(coef, [
        (Fr(r_val**2, 1), f"πr² = {r_val**2}π — повне коло"),
        (Fr(2*r_val*angle,360), f"довжина дуги, не площа"),
        (Fr(r_val**2*angle,180), f"подвоїли"),
    ])
    trap = "S = πr²·α/360°"
    sol = f"S = π·{r_val}²·{angle}/360 = {fmt(coef)}π"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 9. Координатна площина: відстань =====
def f_img_coord_dist(T, rng, lv):
    from t7 import isqrt
    found = False
    for _att in range(50):
        x1, y1 = rng.randint(-4, 4), rng.randint(-4, 4)
        x2, y2 = rng.randint(-4, 4), rng.randint(-4, 4)
        d_sq = (x2-x1)**2 + (y2-y1)**2
        if d_sq >= 9:
            rd = isqrt(d_sq)
            if rd is not None:
                found = True
                break
    if not found:
        return False

    W, H = 380, 380
    cv = C(W, H)
    lo = min(x1,x2,y1,y2) - 1
    hi = max(x1,x2,y1,y2) + 1
    ax = Axes(cv, 40, 20, 320, 320, lo, hi, lo, hi)

    ax.seg(x1, y1, x2, y2, col=BLUE, w=2.5)
    ax.point(x1, y1, f"A({x1};{y1})", col=RED, dy=-12)
    ax.point(x2, y2, f"B({x2};{y2})", col=GREEN, dy=14)

    nm = f"t7_coord_{tag(x1,y1,x2,y2,lv)}"
    img = cv.save(nm)

    text = "Знайдіть довжину відрізка AB (рис.)."
    ans = rd
    wrongs = ensure_unique(rd, [
        (abs(x2-x1)+abs(y2-y1), f"|Δx|+|Δy| = {abs(x2-x1)+abs(y2-y1)}"),
        (rd+1, f"помилка"),
        (max(abs(x2-x1), abs(y2-y1)), f"max(|Δx|,|Δy|)"),
    ])
    trap = "d = √((x₂−x₁)²+(y₂−y₁)²)"
    sol = f"d = √(({x2}−{x1})²+({y2}−{y1})²) = √{d_sq} = {rd}"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# ===== 10. Правильний многокутник у колі =====
def f_img_reg_poly(T, rng, lv):
    nn = rng.choice([3,5,6,8])
    angle = Fr(180*(nn-2), nn)

    W, H = 360, 340
    cv = C(W, H)
    cx, cy = 180, 175
    R = 110

    cv.circle(cx, cy, R, stroke=GRAY, sw=1, dash="4,3")
    pts = reg_poly(cx, cy, R, nn)
    cv.poly(pts, fill=LIGHT[1], stroke=ORANGE, w=2)

    names = {3:['A','B','C'], 4:['A','B','C','D'], 5:['A','B','C','D','E'],
             6:['A','B','C','D','E','F'], 8:['A','B','C','D','E','F','G','H']}
    poly_label(cv, pts, names[nn], off=18, col=INK, centre=(cx,cy))

    # Показуємо кут у першій вершині
    angle_arc(cv, pts[0], pts[-1], pts[1], r=22, col=RED, label="?")

    nm = f"t7_regp_{tag(nn,lv)}"
    img = cv.save(nm)

    nnames = {3:"трикутника",4:"чотирикутника",5:"п'ятикутника",6:"шестикутника",8:"восьмикутника"}
    text = f"Знайдіть внутрішній кут правильного {nnames[nn]} (рис.)."
    ans = angle
    wrongs = ensure_unique(angle, [
        (Fr(360,nn), f"360°/{nn} = {fmt(Fr(360,nn))}° — зовнішній"),
        (180, f"180° — тільки для трикутника"),
        (Fr(180*nn, nn+1), f"неправильна формула"),
    ])
    trap = "кут = 180°·(n−2)/n"
    sol = f"180°·({nn}−2)/{nn} = {fmt(angle)}°"
    return T.add(lv, text, ans, wrongs, trap, sol, img=img)

# === Рівні ===
IMGF = [
    (f_img_right_tri, [1, 2, 3]),
    (f_img_inscribed, [1, 2]),
    (f_img_tri_area, [1, 2]),
    (f_img_trap, [1, 2, 3]),
    (f_img_tangent, [2, 3]),
    (f_img_parallelogram, [1, 2]),
    (f_img_rhombus, [2, 3]),
    (f_img_sector, [2, 3]),
    (f_img_coord_dist, [1, 2, 3]),
    (f_img_reg_poly, [1, 2]),
]
