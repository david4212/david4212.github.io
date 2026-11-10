"""Огляд малюнкових родин: python3 revimg.py <модуль> [lo hi] [seed] → друкує по зразку на (родина, рівень) і складає /tmp/rev_<модуль>_K.png"""
import sys, importlib, random, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1]); T = mod.T
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0; hi = int(sys.argv[3]) if len(sys.argv) > 3 else 999; seed = sys.argv[4] if len(sys.argv) > 4 else 'r'
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
pngs = []; k = 0
for fn, lvs in mod.FAMS[lo:hi]:
    for lv in lvs:
        for att in range(30):
            rng = random.Random(f'{seed}-{fn.__name__}-{lv}-{att}'); n0 = len(T.qs)
            try: fn(T, rng, lv)
            except ValueError: continue
            if len(T.qs) > n0:
                q = T.qs[-1]; k += 1
                print(f'#{k} [{fn.__name__} L{lv}]', q['text']); print('  ', q['options'], '→', q['options'][q['correctIndex']]); print('  ', q['explanation'].replace('\n', '\n   ')); print()
                if q.get('image'):
                    p = f'/tmp/rv_{k}.png'; subprocess.run(['rsvg-convert', '-w', '560', ROOT + '/public' + q['image'], '-o', p]); pngs.append((k, p))
                break
for i in range(0, len(pngs), 6):
    args = ['montage']
    for kk, p in pngs[i:i + 6]: args += ['-label', f'#{kk}', p]
    out = f'/tmp/rev_{sys.argv[1]}_{i // 6}.png'
    subprocess.run(args + ['-tile', '3x2', '-geometry', '560x440+6+6', '-pointsize', '18', out]); print('→', out)
