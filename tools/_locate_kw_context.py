# -*- coding: utf-8 -*-
import json, io, re

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

targets = [
    ('2025数二真题', '10', ['\\dim', 'N(']),
    ('2024数二真题', '9', ['\\ker', '\\operatorname{Im}', '维数公式']),
    ('2021数二真题', '9', ['过渡矩阵']),
    ('2021数二真题', '21', ['雅可比']),
    ('2014数二真题', '8', ['过渡矩阵']),
    ('2011数二真题', '13', ['雅可比']),
    ('2010数二真题', '19', ['雅可比']),
    ('2008数二真题', '6', ['雅可比']),
    ('2007数二真题', '9', ['过渡矩阵']),
    ('2007数二真题', '24', ['正交补']),
]

for pid, no, kws in targets:
    p = next(p for p in exam if p['id'] == pid)
    q = next(q for s in p['sections'] for q in s['questions'] if str(q['no']) == no)
    print(f"########## {pid} 题 {no} ##########")
    for field in ['idea', 'answer']:
        text = q.get(field) or ''
        for kw in kws:
            for m in re.finditer(re.escape(kw), text):
                s0 = max(0, m.start() - 60)
                s1 = min(len(text), m.end() + 80)
                print(f"  [{field}] 命中 '{kw}': ...{text[s0:s1]}...")
    tips = q.get('tips', {})
    tips_str = json.dumps(tips, ensure_ascii=False)
    for kw in kws:
        if kw in tips_str:
            idx = tips_str.find(kw)
            print(f"  [tips] 命中 '{kw}': ...{tips_str[max(0,idx-60):idx+80]}...")
    print()
