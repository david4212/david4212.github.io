import sys, importlib, traceback, random, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1])
T = mod.T
stat = collections.Counter(); err = {}
for fn, lvs in mod.FAMS:
    for lv in lvs:
        for att in range(40):
            rng = random.Random(f'test-{fn.__name__}-{lv}-{att}')
            try:
                r = fn(T, rng, lv)
                stat[(fn.__name__, lv)] += 1 if r else 0
            except ValueError as e:
                err.setdefault((fn.__name__, lv), str(e)[:150])
            except Exception as e:
                err.setdefault((fn.__name__, lv), 'EXC ' + traceback.format_exc().splitlines()[-1][:200] + ' @' + traceback.format_exc().splitlines()[-3][:120])
for k in sorted(set(list(stat) + list(err))):
    print(k, 'ok=', stat.get(k, 0), err.get(k, ''))
print(T.new)
