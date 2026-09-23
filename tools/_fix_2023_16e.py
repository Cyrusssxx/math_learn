# -*- coding: utf-8 -*-
# 2023-16：`：$$\nD=1` → `：\n$$\nD=1`（$$ 独立成行才被 mdBlock 识别为显示块）
import json, io, re, subprocess, os, tempfile

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2023数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '16')
a = q['answer']
n = a.count('：$$\nD=1')
nv = a.replace('：$$\nD=1', '：\n$$\nD=1')
q['answer'] = nv
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('替换处数:', n)

# 渲染验证（页面级：移除 .katex 后无 \ 残留）