"""Генератор питань з української мови для НМТ: дані + правила, відповіді рахуються кодом."""
import random, hashlib, json, os, glob, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
LET = 'АБВГД'
IMGDIR = f'{ROOT}/public/img/ukrainian'
os.makedirs(IMGDIR, exist_ok=True)

class Topic:
    def __init__(self, idx, out_slug):
        self.idx = idx
        files = [f for f in sorted(glob.glob(f'{ROOT}/content/ukrainian_language/{idx:02d}_*.json')) if '_gen' not in f]
        self.seen = set(); self.exist = {1: 0, 2: 0, 3: 0}
        for f in files:
            d = json.load(open(f, encoding='utf-8'))
            self.title = d['topic']
            self.excards = {c['question'] for c in d['cards']}
            for q in d['questions']:
                self.seen.add(q['text'].strip() + '\x01' + '|'.join(sorted(q['options'])))
                self.exist[q['testLevel']] += 1
        self.out = f'{ROOT}/content/ukrainian_language/{idx:02d}_{out_slug}_gen.json'
        self.qs = []; self.new = {1: 0, 2: 0, 3: 0}
        self.cnt = {}

    def add(self, lv, text, ans, wrongs, trap, sol, img=None, n5=True):
        opts = [(ans, None)]; names = {ans}
        for v, r in wrongs:
            if v in names: continue
            names.add(v); opts.append((v, r))
        if len(opts) < 4:
            raise ValueError(f'мало хибних варіантів: {text[:50]}')
        nopt = 5 if (n5 and lv >= 3 and len(opts) >= 5) else 4
        opts = opts[:nopt]
        idxs = list(range(len(opts)))
        rnd = random.Random(int(hashlib.md5((text + ans).encode()).hexdigest()[:12], 16)); rnd.shuffle(idxs)
        ci = idxs.index(0)
        options = [opts[i][0] for i in idxs]
        wr = [f'{LET[p]}) {opts[i][0]} — {opts[i][1]}' for p, i in enumerate(idxs) if i != 0]
        for p in (f'«{ans}» — ', f'«{ans}» = ', f'{ans} — ', f'{ans} = ', f'{ans}: '):
            if sol.startswith(p) and len(sol) > len(p): sol = sol[len(p):]; break
        ex = f"💡 Пастка: {trap.rstrip('.')}.\n❌ Хибні: {'; '.join(w.rstrip('. ') for w in wr)}.\n✅ {LET[ci]}) {ans} — {sol.rstrip('.')}."
        key = text.strip() + '\x01' + '|'.join(sorted(options))
        if key in self.seen: return False
        q = {'text': text.strip(), 'options': options, 'correctIndex': ci, 'explanation': ex, 'testLevel': lv}
        if img: q['image'] = img
        self.qs.append(q); self.seen.add(key); self.new[lv] += 1
        return True

    def need(self, lv, target=52):
        return max(0, target - self.exist[lv] - self.new[lv])

    def run(self, fams, target=52, rounds=80):
        for r in range(rounds):
            progressed = False
            for fi, (fn, lvs) in enumerate(fams):
                for lv in lvs:
                    if self.need(lv, target) <= 0: continue
                    for att in range(8):
                        rng = random.Random(f'u{self.idx}-{fi}-{lv}-{r}-{att}')
                        try:
                            if fn(self, rng, lv): progressed = True; break
                        except ValueError as e:
                            continue
            if all(self.need(l, target) <= 0 for l in (1, 2, 3)) or not progressed: break

    def save(self, cards=None):
        cards = [c for c in (cards or []) if c['question'] not in self.excards]
        d = {'subject': 'UKRAINIAN', 'topic': self.title, 'questions': self.qs, 'cards': cards}
        json.dump(d, open(self.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(os.path.basename(self.out), 'нових', len(self.qs), self.new, 'було', self.exist,
              'разом', {l: self.exist[l] + self.new[l] for l in (1, 2, 3)}, 'карток', len(cards))

def sample(rng, lst, k): return rng.sample(list(lst), k)
VOW = set('аеєиіїоуюя')
