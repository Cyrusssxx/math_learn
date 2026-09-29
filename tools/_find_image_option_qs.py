# -*- coding: utf-8 -*-
"""定位「选项为图片无法转写」的占位题目（全库扫描）"""
import json, io, re

KW = ['无法用文字准确转写', '为一幅函数图像', '图形见原书', '如上图所示', '图见原书']

files = [
    'pwa/data/exam.json',
    'pwa/data/core_bank.json',
    'pwa/data/xd_bank.json',
    'pwa/data/practice.json',
    'pwa/data/bank_questions.json',
]
for fp in files:
    try:
        with io.open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        continue
    items = []
    if fp.endswith('exam.json'):
        for p in data:
            for s in p.get('sections', []):
                for q in s.get('questions', []):
                    items.append((p.get('id'), q))
    elif fp.endswith(('xd_bank.json', 'core_bank.json')):
        for p in data:
            for s in p.get('sections', []):
                for q in s.get('questions', []):
                    items.append((p.get('id'), q))
    elif fp.endswith('bank_questions.json'):
        for idx, it in enumerate(data.get('items', [])):
            items.append(('bank', dict(it, no=idx + 1)))
    else:
        for idx, it in enumerate(data if isinstance(data, list) else []):
            items.append(('practice', dict(it, no=it.get('no', idx + 1))))

    for pid, q in items:
        blob = ' '.join(str(q.get(k, '')) for k in ('stem', 'answer', 'idea')) + ' ' + ' '.join(str(o) for o in q.get('options', []))
        hits = [k for k in KW if k in blob]
        if hits:
            print(f"--- {fp} | 归属 {pid} | no={q.get('no')} | id={q.get('id','')} | hits={hits}")
            print(f"    img={q.get('img','')} img2={q.get('img2','')}")
            print(f"    stem: {str(q.get('stem',''))[:120]}")
            print(f"    options: {q.get('options')}")
