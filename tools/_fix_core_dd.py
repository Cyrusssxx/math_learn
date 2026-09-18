# -*- coding: utf-8 -*-
"""修复 core_bank.json：连续 $$ 空块折叠 + 诊断 $ 不配平字段"""
import json, io, re

P = 'D:/ai code/math-note/pwa/data/core_bank.json'
d = json.load(io.open(P, encoding='utf-8'))
pat = re.compile(r'\$\$\s*\n\s*\$\$|\$\$\$\$')


def clean_dd(s):
    while True:
        t = re.sub(r'\$\$\s*\n\s*\$\$', '$$', s)
        if t == s:
            return s
        s = t


fixed = 0
unpaired = []
for sec in d[0]['sections']:
    for q in sec.get('questions', []):
        for f in ('stem', 'answer', 'idea'):
            v = q.get(f) or ''
            if pat.search(v):
                q[f] = clean_dd(v)
                fixed += 1
            if (q[f] or '').count('$') % 2:
                unpaired.append((q.get('no'), f, (q[f] or '')[:120].replace('\n', ' ')))

with io.open(P, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, separators=(',', ':'))

print('修复连续 $$ 空块的字段: %d' % fixed)
print('修复后 $ 不配平字段: %d' % len(unpaired))
for u in unpaired:
    print('  [no=%s %s] %s' % u)
