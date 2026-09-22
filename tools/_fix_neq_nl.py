# -*- coding: utf-8 -*-
# 修复 2024 卷：\neq 被拆成「真实换行 + eq」→ 合并回 \neq
import json, io, re

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))


def fix(s):
    # 换行紧跟 eq（eq 后非字母）→ \neq
    s2 = re.sub(r'\neq(?![a-zA-Z])', '\\neq', s)
    return s2


fixed = 0
for v in exam:
    if v['id'] != '2024数二真题':
        continue
    for sec in v.get('sections', []):
        for q in sec.get('questions', []):
            for f in ('stem', 'answer', 'idea', 'tips'):
                t = q.get(f) or ''
                if isinstance(t, dict):
                    nv = {}
                    for k, val in t.items():
                        ns = fix(str(val))
                        nv[k] = ns
                        if ns != val:
                            fixed += 1
                    q[f] = nv
                else:
                    ns = fix(t)
                    if ns != t:
                        q[f] = ns
                        fixed += 1

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('修复处数:', fixed)
