import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from t8 import *
T.run(FAMS, target=62)
try:
    from t8_cards import CARDS
except Exception: CARDS = []
T.save(cards=[{"question": q, "answer": a} for q, a in CARDS])
cleanup_imgs(T)
