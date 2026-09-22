# -*- coding: utf-8 -*-
# 修复 2023-16：行内 $ 跨行包矩阵环境（$\n\begin{...}...\end{...}$ → 显示块）
import json, io, re

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2023数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '16')
v = q['answer']

# 模式：`：$\n\begin{cases}...`（行内 $ 开 + 换行矩阵）→ 显示块 `$$\n\begin{cases}...\end{cases}$$`
# 具体：`$：$\n\begin{cases}` 且结尾 `\end{cases}$`
nv = v.replace('：$\n\\begin{cases}', '：$$\n\\begin{cases}')
nv = nv.replace('\\end{cases}$', '\\end{cases}$$')
nv = nv.replace('$a=2,b=-4$：$$\nD=', '$a=2,b=-4$：$$\nD=')

print('修改前 $ 计数:', v.count('$'), '修改后:', nv.count('$'))
q['answer'] = nv
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('已写盘')
