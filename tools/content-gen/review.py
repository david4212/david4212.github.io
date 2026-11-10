import sys, importlib, random
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1]); T = mod.T
lo, hi = int(sys.argv[2]), int(sys.argv[3])
for fn, lvs in mod.FAMS[lo:hi]:
    lv = lvs[-1]
    for att in range(30):
        rng = random.Random(f'rev-{fn.__name__}-{att}')
        n0 = len(T.qs)
        try: fn(T, rng, lv)
        except ValueError: continue
        if len(T.qs) > n0:
            q = T.qs[-1]; print(f'[{fn.__name__} L{lv}]', q['text']); print('  ', q['options'], '→', q['options'][q['correctIndex']]); print('  ', q['explanation'].replace('\n', '\n   ')); print(); break
