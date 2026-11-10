import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t2_img import *
import random
T.run(FAMS, target=68)
try:
    from t2_cards import CARDS
except Exception: CARDS = []
T.save(cards=[{"question": q, "answer": a} for q, a in CARDS])
cleanup_imgs(T)
