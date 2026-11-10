"""Генератор математичних питань НМТ: параметричні родини, відповіді рахуються кодом."""
import random, hashlib, json, os, glob, math, re
from fractions import Fraction as F
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
LET = 'АБВГД'
MINUS = '−'

def fmt(x):
    if isinstance(x, str): return x.replace('-', MINUS)
    if isinstance(x, float): x = F(str(round(x, 8))).limit_denominator(10**6)
    if isinstance(x, int): s = str(x)
    else:
        x = F(x)
        if x.denominator == 1: s = str(x.numerator)
        else:
            d = x.denominator
            while d % 2 == 0: d //= 2
            while d % 5 == 0: d //= 5
            if d == 1: s = ('%.6f' % float(x)).rstrip('0').rstrip('.').replace('.', ',')
            else: s = f'{x.numerator}/{x.denominator}'
    return s.replace('-', MINUS)

def numval(x):
    if isinstance(x, (int, F)): return F(x)
    if isinstance(x, float): return F(str(round(x, 8))).limit_denominator(10**6)
    return None

def sgn(n, first=False):
    """знак для запису многочлена: +3 → ' + 3', −3 → ' − 3'"""
    if first: return fmt(n)
    return (' + ' if n >= 0 else f' {MINUS} ') + fmt(abs(n))

def poly(coefs, var='x'):
    """coefs від старшого до молодшого: [1,-5,6] → x² − 5x + 6"""
    n = len(coefs) - 1
    sup = {0: '', 1: '', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶'}
    out = ''
    for i, c in enumerate(coefs):
        p = n - i
        if c == 0: continue
        a = abs(c)
        body = ('' if (a == 1 and p > 0) else fmt(a)) + (var + sup[p] if p >= 1 else '')
        if not out: out = (MINUS if c < 0 else '') + body
        else: out += (' + ' if c > 0 else f' {MINUS} ') + body
    return out or '0'

class Topic:
    def __init__(self, idx, out_slug):
        self.idx = idx
        files = [f for f in sorted(glob.glob(f'{ROOT}/content/math/{idx:02d}_*.json')) if '_gen' not in f]
        self.title = None; self.seen = set(); self.exist = {1: 0, 2: 0, 3: 0}
        for f in files:
            d = json.load(open(f, encoding='utf-8'))
            self.title = d['topic']
            for q in d['questions']:
                self.seen.add(q['text'].strip() + '\x01' + '|'.join(sorted(q['options'])))
                self.exist[q['testLevel']] += 1
        self.out = f'{ROOT}/content/math/{idx:02d}_{out_slug}_gen.json'
        self.qs = []; self.new = {1: 0, 2: 0, 3: 0}; self.cards = []
        self.errors = 0

    def add(self, lv, text, ans, wrongs, trap, sol, img=None):
        text = re.sub(r'(?<![\w)])-(?=\d)', MINUS, text.strip())
        fa = fmt(ans)
        opts = [(ans, None)]
        names = {fa}
        for w in wrongs:
            v, r = w
            fv = fmt(v)
            if fv in names: continue
            names.add(fv); opts.append((v, r))
        if len(opts) < 4 and numval(ans) is not None and len(opts) >= 3:
            for dlt in (1, -1, 2, -2, 10, -10):
                v = numval(ans) + dlt
                if fmt(v) not in names and len(opts) < 4:
                    names.add(fmt(v)); opts.append((v, 'результат відрізняється від правильного через неточність у проміжних обчисленнях'))
        if len(opts) < 4:
            self.errors += 1
            raise ValueError(f'мало хибних варіантів: {text[:60]} {[fmt(o[0]) for o in opts]}')
        nopt = 5 if (lv >= 2 and len(opts) >= 5) else 4
        opts = opts[:nopt]
        vals = [numval(o[0]) for o in opts]
        idxs = list(range(len(opts)))
        if all(v is not None for v in vals): idxs.sort(key=lambda i: vals[i])
        else:
            rnd = random.Random(int(hashlib.md5(text.encode()).hexdigest()[:12], 16)); rnd.shuffle(idxs)
        ci = idxs.index(0)
        options = [fmt(opts[i][0]) for i in idxs]
        wr = [f'{LET[p]}) {fmt(opts[i][0])} — {opts[i][1]}' for p, i in enumerate(idxs) if i != 0]
        sol = re.sub(r'(?<![\w)])-(?=\d)', MINUS, sol); trap = re.sub(r'(?<![\w)])-(?=\d)', MINUS, trap)
        ex = f"💡 Пастка: {trap.rstrip('.')}.\n❌ Хибні: {'; '.join(w.rstrip('. ') for w in wr)}.\n✅ {LET[ci]}) {fa} — {sol.rstrip('.')}."
        key = text + '\x01' + '|'.join(sorted(options))
        if key in self.seen: return False
        ex = re.sub(r'(?<![\w)])-(?=\d)', MINUS, ex)
        q = {'text': text, 'options': options, 'correctIndex': ci, 'explanation': ex, 'testLevel': lv}
        if img: q['image'] = img
        self.qs.append(q); self.seen.add(key); self.new[lv] += 1
        return True

    def need(self, lv, target=55):
        return max(0, target - self.exist[lv] - self.new[lv])

    def run(self, fams, target=55, rounds=60):
        """fams: список (fn, [рівні]); fn(T, rng, lv) має викликати T.add."""
        for r in range(rounds):
            progressed = False
            for fi, (fn, lvs) in enumerate(fams):
                for lv in lvs:
                    if self.need(lv, target) <= 0: continue
                    for att in range(6):
                        rng = random.Random(f'{self.idx}-{fi}-{lv}-{r}-{att}')
                        try:
                            if fn(self, rng, lv): progressed = True; break
                        except ValueError as e:
                            print('!!', fn.__name__, e); break
            if all(self.need(l, target) <= 0 for l in (1, 2, 3)) or not progressed: break

    def save(self, cards=None):
        d = {'subject': 'MATH', 'topic': self.title, 'questions': self.qs, 'cards': cards or []}
        json.dump(d, open(self.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(os.path.basename(self.out), 'нових', len(self.qs), self.new, 'було', self.exist,
              'разом', {l: self.exist[l] + self.new[l] for l in (1, 2, 3)})

def pick(rng, lo, hi, excl=()):
    while True:
        v = rng.randint(lo, hi)
        if v not in excl: return v

def shuffled(rng, lst):
    l = list(lst); rng.shuffle(l); return l

def u(v, unit): return f'{fmt(v)} {unit}'
def pc(x):
    x = F(x)
    if x.denominator == 1: return fmt(x) + '%'
    return '≈' + fmt(round(float(x), 1)) + '%'
def dc(x, nd=2):
    """десяткове число з комою"""
    return ('%.*f' % (nd, float(x))).rstrip('0').rstrip('.').replace('.', ',').replace('-', MINUS)
SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
def sup(k): return str(k).translate(SUP)
def cleanup_imgs(T):
    """видаляє SVG цієї теми (tN_*), на які немає посилань"""
    import re
    used = {q['image'] for q in T.qs if q.get('image')}
    for f in glob.glob(f'{ROOT}/public/img/math/t{T.idx}_*.svg'):
        p = '/img/math/' + os.path.basename(f)
        if p not in used: os.remove(f)

def ffmt(x):
    """дріб a/b (без десяткових), мінус — U+2212"""
    x = F(x)
    return fmt(x) if x.denominator == 1 else f"{MINUS if x < 0 else ''}{abs(x.numerator)}/{x.denominator}"
