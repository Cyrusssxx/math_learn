# -*- coding: utf-8 -*-
"""可靠检查：exam.json / core_bank.json 的连续 $$ 空块、$ 配平（用 .py 文件，绕开 bash 转义）"""
import json, io, re

pat = re.compile(r'\$\$\s*\n\s*\$\$|\$\$\$\$')

for path in ('D:/ai code/math-note/pwa/data/exam.json',
             'D:/ai code/math-note/pwa/data/core_bank.json'):
    d = json.load(io.open(path, encoding='utf-8'))
    qs = []
    if isinstance(d, list) and d and 'sections' in d[0]:
        for vol in d:
            for s in vol.get('sections', []):
                qs += s.get('questions', [])
    else:
        qs = [q for s in d[0]['sections'] for q in s['questions']]
    n = bad_dollar = 0
    samples = []
    for q in qs:
        for f in ('stem', 'answer', 'idea'):
            v = q.get(f) or ''
            m = pat.findall(v)
            if m:
                n += len(m)
                if len(samples) < 5:
                    samples.append((str(q.get('no')), f, len(m)))
            if v.count('$') % 2:
                bad_dollar += 1
    print(path.split('/')[-1])
    print('  连续 $$ 空块: %d | $ 不配平字段: %d' % (n, bad_dollar))
    for s in samples:
        print('    样本:', s)
    print()
