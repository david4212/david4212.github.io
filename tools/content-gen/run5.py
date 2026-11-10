import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t5_img import *
import random

# Text families from t5.py
L1 = [f_d_poly, f_d_point, f_d_table, f_anti_poly, f_int_poly, f_motion, f_tangent_slope, f_crit, f_int_basic, f_second]
L2 = [f_d_product, f_d_quot, f_d_chain, f_tangent_eq, f_tangent_par, f_extr_seg, f_anti_point, f_area_parab, f_area_between, f_NL, f_from_deriv, f_kin_int]
L3 = [f_param_mono, f_deriv_factored, f_int_prop]
TEXT = [(f, [1]) for f in L1] + [(f, [2]) for f in L2] + [(f, [3]) for f in L3]

def interleave(img, text):
    """чергує малюнкові й текстові родини окремо для кожного рівня"""
    out = []
    for lv in (1, 2, 3):
        a = [f for f, lvs in img if lv in lvs]; b = [f for f, lvs in text if lv in lvs]
        for i in range(max(len(a), len(b))):
            if i < len(a): out.append((a[i], [lv]))
            if i < len(b): out.append((b[i], [lv]))
    return out

FAMS = interleave(IMGF, TEXT)

if __name__ == '__main__':
    T.strict = True
    T.run(FAMS, target=int(sys.argv[1]) if len(sys.argv) > 1 else 55)
    from t5_cards import CARDS
    T.save(cards=[{"question": q, "answer": a} for q, a in CARDS])
    cleanup_imgs(T)
    ni = sum(1 for q in T.qs if q.get('image')); print('з малюнками:', ni, 'із', len(T.qs))
    gen = sum('неточність у проміжних обчисленнях' in q['explanation'] for q in T.qs); print('автодоповнених хибних варіантів:', gen)
