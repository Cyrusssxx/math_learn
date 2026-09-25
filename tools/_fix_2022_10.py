# -*- coding: utf-8 -*-
import json, io, os

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

# 找到 2022 数二真题
p2022 = next(p for p in exam_data if p['id'] == '2022数二真题')
q10 = next(q for s in p2022['sections'] for q in s['questions'] if str(q['no']) == '10')

print("原 stem:", repr(q10['stem']))
print("原 options:", q10['options'])

# 修复 stem 中的矩阵换行 \\
# 设 $\alpha_1=\begin{pmatrix}\lambda\\1\\1\end{pmatrix}$，$\alpha_2=\begin{pmatrix}1\\\lambda\\1\end{pmatrix}$，$\alpha_3=\begin{pmatrix}1\\1\\\lambda\end{pmatrix}$，$\alpha_4=\begin{pmatrix}1\\\lambda\\\lambda^2\end{pmatrix}$，若 $\alpha_1,\alpha_2,\alpha_3$ 与 $\alpha_1,\alpha_2,\alpha_4$ 等价，则 $\lambda\in$（　）
fixed_stem = (
    '设 $\\alpha_1=\\begin{pmatrix}\\lambda\\\\1\\\\1\\end{pmatrix}$，'
    '$\\alpha_2=\\begin{pmatrix}1\\\\\\lambda\\\\1\\end{pmatrix}$，'
    '$\\alpha_3=\\begin{pmatrix}1\\\\1\\\\\\lambda\\end{pmatrix}$，'
    '$\\alpha_4=\\begin{pmatrix}1\\\\\\lambda\\\\\\lambda^2\\end{pmatrix}$，'
    '若 $\\alpha_1,\\alpha_2,\\alpha_3$ 与 $\\alpha_1,\\alpha_2,\\alpha_4$ 等价，则 $\\lambda\\in$（　）'
)

# 规范化 options
fixed_options = [
    '(A) $\\{\\lambda\\mid\\lambda\\in\\mathbb R\\}$',
    '(B) $\\{\\lambda\\mid\\lambda\\in\\mathbb R,\\lambda\\ne-1\\}$',
    '(C) $\\{\\lambda\\mid\\lambda\\in\\mathbb R,\\lambda\\ne-1,\\lambda\\ne-2\\}$',
    '(D) $\\{\\lambda\\mid\\lambda\\in\\mathbb R,\\lambda\\ne-2\\}$'
]

q10['stem'] = fixed_stem
q10['options'] = fixed_options

# 保存回 exam.json（注意单行紧凑 JSON 规则！）
with io.open('pwa/data/exam.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(exam_data, f, ensure_ascii=False, separators=(',', ':'))

print("\n已成功写回 exam.json！")

# 再次读取验证
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    verify_data = json.load(f)
vq10 = next(q for p in verify_data if p['id'] == '2022数二真题' for s in p['sections'] for q in s['questions'] if str(q['no']) == '10')
print("验证写回后的 stem:", repr(vq10['stem']))
print("验证写回后的 options:", vq10['options'])
