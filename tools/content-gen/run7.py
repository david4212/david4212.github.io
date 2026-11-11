import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t7_img import *
from t7 import FAMS1

def interleave(img, text):
    out = []
    for lv in (1, 2, 3):
        a = [f for f, lvs in img if lv in lvs]
        b = [f for f, lvs in text if lv in lvs]
        for i in range(max(len(a), len(b))):
            if i < len(a): out.append((a[i], [lv]))
            if i < len(b): out.append((b[i], [lv]))
    return out

FAMS = interleave(IMGF, FAMS1)

if __name__ == '__main__':
    T.strict = True
    T.run(FAMS, target=int(sys.argv[1]) if len(sys.argv) > 1 else 50)
    from t7_cards import CARDS
    T.save(cards=[{"question": q, "answer": a} for q, a in CARDS])
    from mgen import cleanup_imgs
    cleanup_imgs(T)
    ni = sum(1 for q in T.qs if q.get('image'))
    print('з малюнками:', ni, 'із', len(T.qs))
    gen = sum('неточність у проміжних обчисленнях' in q['explanation'] for q in T.qs)
    print('автодоповнених хибних варіантів:', gen)
