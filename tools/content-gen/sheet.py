"""Контактні аркуші малюнків згенерованого файла: python3 sheet.py <NN_slug_gen.json> [крок] → /tmp/sheet_K.png + список питань"""
import json, sys, os, subprocess, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
d = json.load(open(f'{ROOT}/content/math/{sys.argv[1]}')); step = int(sys.argv[2]) if len(sys.argv) > 2 else 1; off = int(sys.argv[3]) if len(sys.argv) > 3 else 0
qs = [q for q in d['questions'] if q.get('image')][off::step]
pngs = []
for i, q in enumerate(qs):
    p = f'/tmp/sh_{i}.png'; subprocess.run(['rsvg-convert', '-w', '520', ROOT + '/public' + q['image'], '-o', p]); pngs.append(p)
    print(f'#{i + 1} L{q["testLevel"]} {os.path.basename(q["image"])}: {q["text"]}\n     {q["options"]} → {q["options"][q["correctIndex"]]}')
for k in range(0, len(pngs), 9):
    args = ['montage']
    for j, p in enumerate(pngs[k:k + 9]): args += ['-label', f'#{k + j + 1}', p]
    subprocess.run(args + ['-tile', '3x3', '-geometry', '520x400+4+4', '-pointsize', '16', f'/tmp/sheet_{k // 9}.png']); print('→', f'/tmp/sheet_{k // 9}.png')
