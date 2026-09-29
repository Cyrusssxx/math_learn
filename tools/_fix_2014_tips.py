# -*- coding: utf-8 -*-
"""修复 2014 题8 tips.jq 被 inline python -c 转义破坏的问题（\a 响铃、\b 退格等）"""
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

p = next(p for p in exam if p['id'] == '2014数二真题')
q = next(q for s in p['sections'] for q in s['questions'] if str(q['no']) == '8')

# 正确内容：单反斜杠 LaTeX（json.dump 会自动转义存储）
q['tips']['jq'] = (
    '$\\alpha_1+k\\alpha_3,\\ \\alpha_2+l\\alpha_3,\\ \\alpha_3$ 用原组表出的系数矩阵 '
    '$\\begin{pmatrix}1&0&0\\\\0&1&0\\\\k&l&1\\end{pmatrix}$，'
    '行列式恒 $=1\\ne0$ → 对任意 $k,l$ 都线性无关。'
)

with io.open('pwa/data/exam.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(exam, f, ensure_ascii=False, separators=(',', ':'))

# 读回验证
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam2 = json.load(f)
q2 = next(q for p in exam2 if p['id'] == '2014数二真题' for s in p['sections'] for q in s['questions'] if str(q['no']) == '8')
print('修复后 tips.jq:', q2['tips']['jq'])
assert '\\alpha_1' in q2['tips']['jq'], 'alpha 仍缺失反斜杠！'
assert 'pmatrix' in q2['tips']['jq'], 'pmatrix 缺失！'
print('✅ 修复验证通过')
