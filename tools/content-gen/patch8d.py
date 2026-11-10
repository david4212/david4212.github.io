s=open('t8.py',encoding='utf-8').read()
def rp(a,b,cnt=None):
    global s
    assert a in s, a[:80]
    s=s.replace(a,b)
# vertex label offsets for box
rp("""    cen = ((V['A'][0] + V['C1'][0]) / 2, (V['A'][1] + V['C1'][1]) / 2)
    if names: vlab(c, V, list(V), cen)
    return V""","""    if names:
        LOFF = {'A': (-14, 17), 'B': (13, 18), 'C': (16, 6), 'D': (-16, -7), 'A1': (-16, -6), 'B1': (-15, -13), 'C1': (15, -6), 'D1': (-6, -13)}
        for nme, (dx, dy) in LOFF.items(): c.text(V[nme][0] + dx, V[nme][1] + dy, SUB.get(nme, nme), size=15, col=INK, anchor='middle', bold=True)
    return V""")
rp("def savec(c, *parts)","""def sidel(c, V, txt, col=BLUE):
    c.text(V['A'][0] + 0.2 * (V['B'][0] - V['A'][0]), V['A'][1] + 26, txt, size=14, col=col, anchor='middle', bold=True)

def savec(c, *parts)""")
rp("dimtxt(c, V['A'], V['B'], str(a), (0, 24)); dimtxt(c, V['S'], V['O'], str(H), (-14, 0), RED)","sidel(c, V, str(a)); dimtxt(c, V['S'], V['O'], str(H), (14, -4), RED)")
rp("S.angle_arc(c, V['M'], V['S'], V['O'], 26, ORANGE, 'φ'); dimtxt(c, V['A'], V['B'], str(a), (0, 24))","S.angle_arc(c, V['M'], V['S'], V['O'], 26, ORANGE, 'φ'); sidel(c, V, str(a))")
rp("dimtxt(c, V['S'], V['M'], 'l', (12, -2), GREEN)","dimtxt(c, V['S'], V['M'], 'l', (-13, 0), GREEN)")
rp("dimtxt(c, V['A'], V['C'], str(q), (-22, 6))","dimtxt(c, V['A'], V['C'], str(q), (-17, -10))")
# nets canvas
rp("c = C(400, 270); draw_nets(c, order)","c = C(400, 300); draw_nets(c, order)")
rp("def draw_nets(c, nets, labels='АБВГ', cols=2, pw=190, ph=125,","def draw_nets(c, nets, labels='АБВГ', cols=2, pw=190, ph=145,")
rp("def hid_edge(i, j): return (pts_b[i][2] + pts_b[j][2]) / 2 > 0.05","def hid_edge(i, j): return (pts_b[i][2] + pts_b[j][2]) / 2 > 0.3")
rp("dash='5,4' if pts_b[i][2] > 0.05 else None)\n    else:","dash='5,4' if pts_b[i][2] > 0.3 else None)\n    else:")
rp("c.line(pts_b[i][0], pts_b[i][1], ap[0], ap[1], col=INK, w=2, dash='5,4' if pts_b[i][2] > 0.05 else None)","c.line(pts_b[i][0], pts_b[i][1], ap[0], ap[1], col=INK, w=2, dash='5,4' if pts_b[i][2] > 0.3 else None)")
# cyl in cube bottom arcs
rp("""c.rect(70, 40, 160, 160, fill='#eff6ff'); c.rect(70, 40, 160, 160, stroke=BLUE, sw=2.2); c.text(150, 222, f'ребро куба {a}', size=14, anchor='middle', bold=True, col=BLUE)
        c.ellipse(150, 40, 80, 24, fill='#dbeafe', stroke=BLUE, sw=2)""","""c.rect(70, 40, 160, 160, fill='#eff6ff'); c.rect(70, 40, 160, 160, stroke=INK, sw=2); c.text(150, 222, f'ребро куба {a}', size=14, anchor='middle', bold=True, col=BLUE)
        c.path('M70,200 A80,24 0 0 0 230,200', stroke=BLUE, w=2); c.path('M70,200 A80,24 0 0 1 230,200', stroke=BLUE, w=1.6, dash='5,4'); c.ellipse(150, 40, 80, 24, fill='#dbeafe', stroke=BLUE, sw=2)""")
rp("""c.rect(70, 40, 160, 160, stroke=BLUE, sw=2.2, fill='#eff6ff'); c.ellipse(150, 40, 80, 24, fill='#dbeafe', stroke=BLUE, sw=2)""","""c.rect(70, 40, 160, 160, stroke=INK, sw=2, fill='#eff6ff'); c.path('M70,200 A80,24 0 0 0 230,200', stroke=BLUE, w=2); c.path('M70,200 A80,24 0 0 1 230,200', stroke=BLUE, w=1.6, dash='5,4'); c.ellipse(150, 40, 80, 24, fill='#dbeafe', stroke=BLUE, sw=2)""")
# water
i=s.index("    c = C(380, 250); cyl(c, 100, 200, R1 * 7")
j=s.index("    return T.add(lv, f'Воду з циліндричної")
s=s[:i]+"""    c = C(380, 260)
    for cx, R_, lvl, lab, col in ((100, R1 * 7, 0.55, f'R₁ = {R1}', BLUE), (290, R2 * 7, 0.7, f'R₂ = {R2}', BLUE)):
        ry = R_ * 0.3; yb = 200; yt = yb - 130
        wy = yb - 130 * lvl
        c.path(f'M{cx-R_},{wy} L{cx-R_},{yb} A{R_},{ry} 0 0 0 {cx+R_},{yb} L{cx+R_},{wy} A{R_},{ry} 0 0 1 {cx-R_},{wy} Z', fill='#bfdbfe', stroke='none')
        c.ellipse(cx, wy, R_, ry, fill='#93c5fd', stroke='#2563eb', sw=1.2)
        cyl(c, cx, yb, R_, 130, labR=None, labh=None, axis=False, fillc='none')
        c.text(cx, yb + 40, lab, size=14, anchor='middle', bold=True, col=col)
    c.text(100, 245, f'рівень води h₁ = {h1}', size=14, anchor='middle', bold=True, col=BLUE); c.text(290, 245, 'рівень води h₂ = ?', size=14, anchor='middle', bold=True, col=RED)
"""+s[j:]
open('t8.py','w',encoding='utf-8').write(s)
