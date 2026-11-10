import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t4_img2 import *
import random
L1 = [f_value, f_domain_basic, f_zero, f_through_point, f_vertex, f_ap_basic, f_ap_d, f_gp_basic, f_gp_q, f_ap_sum, f_parity, f_period, f_trig_value, f_monotone_basic, f_range_basic, f_inverse_val, f_transform_text, f_hyperbola, f_slope, f_parallel_perp, f_axes_int, f_compare_simple]
L2 = [f_domain_comb, f_range_trig, f_reduction, f_ap_find_n, f_gp_sum, f_trig_identity, f_composite, f_extrema_segment, f_parity2, f_period2, f_gp_inf, f_trig_addition, f_inverse_formula, f_quad_word, f_ap_sum_formula, f_compare_order, f_exp_point, f_trig_amplitude, f_line_param, f_piecewise,
      f_recurrent, f_seq_formula, f_gp_mean, f_ap_mean, f_domain_int_count, f_range_other, f_shift_value, f_line_two_points, f_quad_a, f_quad_signs, f_symmetry, f_ap_sign, f_ap_sum_range, f_ap_insert, f_gp_find_n, f_gp_q_terms, f_parity_value, f_line_area]
L3 = [f_domain_hard, f_domain_param, f_range_asin_bcos, f_range_quad_trig, f_range_exp_quad, f_range_misc, f_param_quad, f_parity_param, f_period_hard, f_composite_hard, f_inverse_hard, f_ap_property, f_gp_hard, f_abs_count, f_periodic_value, f_monotone_param, f_rect_partition]
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
    T.run(FAMS, target=int(sys.argv[1]) if len(sys.argv) > 1 else 72)
    from t4_cards import CARDS
    T.save(cards=[{"question": q, "answer": a} for q, a in CARDS])
    cleanup_imgs(T)
    ni = sum(1 for q in T.qs if q.get('image')); print('з малюнками:', ni, 'із', len(T.qs))
    gen = sum('неточність у проміжних обчисленнях' in q['explanation'] for q in T.qs); print('автодоповнених хибних варіантів:', gen)
