# -*- coding: utf-8 -*-
# 统一修复：①行内 $...$ 内真实换行 → 合并（6 卷）；②2023-16 的 =8$。 → =8$$
import json, io, re

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
VOLS = {'2021数二真题', '2022数二真题', '2023数二真题', '2024数二真题', '2025数二真题', '2026数二真题'}

INLINE_CROSS = re.compile(r'(?<!\$)\$([^$\n]*)\n([^$\n]*)\$(?!\$)')
n1 = n2 = 0
for v in exam:
    if v['id'] not in VOLS:
        continue
    for sec in v.get('sections', []):
        for q in sec.get('questions', []):
            for f in ('stem', 'answer', 'idea', 'tips'):
                t = q.get(f) or ''
                if isinstance(t, dict):
                    nv = {}
                    for k, val in t.items():
                        s = str(val)
                        s2 = INLINE_CROSS.sub(lambda m: '$' + m.group(1) + m.group(2) + '$', s)
                        nv[k] = s2
                        if s2 != s:
                            n1 += 1
                    q[f] = nv
                else:
                    s2 = INLINE_CROSS.sub(lambda m: '$' + m.group(1) + m.group(2) + '$', t)
                    if s2 != t:
                        q[f] = s2
                        n1 += 1
            # 2023-16 特例：=8$。 → =8$$
            if v['id'] == '2023数二真题' and str(q.get('no')) == '16':
                a = q.get('answer') or ''
                if '=8$。' in a:
                    q['answer'] = a.replace('=8$。', '=8$$')
                    n2 += 1

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('行内$跨行合并处:', n1, '；2023-16 =8$$ 补:', n2)
