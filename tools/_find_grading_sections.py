# -*- coding: utf-8 -*-
"""定位残留「阅卷/评分」段的题目"""
import json, io

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

for p in core:
    for s in p['sections']:
        for q in s['questions']:
            a = str(q.get('answer') or '')
            for kw in ('阅卷', '评分'):
                i = a.find(kw)
                if i >= 0:
                    print(f"no={q.get('no')} [{kw}]: ...{a[max(0, i - 30):i + 40]}...")
                    break
