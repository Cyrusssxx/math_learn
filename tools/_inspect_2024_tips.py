# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

p24 = next(p for p in exam if p['id'] == '2024数二真题')

# 查看 tips 字段结构
for no in ['17', '22']:
    q = next(q for s in p24['sections'] for q in s['questions'] if str(q['no']) == no)
    tips = q.get('tips', {})
    print(f"===== 2024 题 {no} tips =====")
    for k, v in tips.items():
        print(f"  [{k}]: {v}")
