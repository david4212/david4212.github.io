import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t1_img import *
import random
T.run(FAMS, target=68)
from t1_cards import CARDS
T.save(cards=[{"question": q, "answer": a} for q, a in CARDS])
cleanup_imgs(T)
if len(sys.argv) > 1:
    rnd = random.Random(int(sys.argv[1]))
    for q in rnd.sample(T.qs, 14):
        print('Lv', q['testLevel'], '|', q['text']); print('  ', q['options'], 'ans=', q['options'][q['correctIndex']]); print('  ', q['explanation'].replace('\n', '\n   ')); print()
