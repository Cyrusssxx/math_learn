# -*- coding: utf-8 -*-
"""打印 5 个真异常字段的完整结构（含上下文行），确定修复方案"""
import json, io

exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
targets = [
    ('2022数二真题', '19', 'answer'),
    ('2020数二真题', '5', 'stem'),
    ('2020数二真题', '14', 'stem'),
    ('2020数二真题', '14', 'answer'),
    ('2000数二真题', '12', 'answer'),
]
for t, no, f in targets:
    vol = next(v for v in exam if v['id'] == t)
    q = next(x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no)
    v = q.get(f) or ''
    lines = v.split('\n')
    print('=' * 72)
    print('%s 第%s题.%s  len=%d 行数=%d' % (t, no, f, len(v), len(lines)))
    for i, L in enumerate(lines):
        if not L.strip():
            continue
        print('L%-3d (%d$) %s' % (i, L.count('$'), L[:140]))
