import sys, importlib
sys.path.insert(0, '.')
from ukgen import *
n = int(sys.argv[1]); slug = sys.argv[2]; target = int(sys.argv[3]) if len(sys.argv) > 3 else 52
m = importlib.import_module(f'u{n}')
T = Topic(n, slug)
for a in m.H: T.add(*a)
T.run(m.FAMS, target=target)
cards = getattr(m, 'CARDS', [])
T.save(cards)
