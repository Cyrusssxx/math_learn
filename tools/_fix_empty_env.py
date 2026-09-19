# -*- coding: utf-8 -*-
"""修复「行内空环境 + 块外内容」的错乱结构：
   把 \begin{cases}\end{cases} / \begin{vmatrix}\end{vmatrix}（行内成对空环境）拆成
   正确的 \begin{env}（内容紧随其后，行尾已有 \end{env} 闭合）。
   涉及：2020数二5.stem、2020数二14.stem/answer、2000数二12.answer"""
import json, io

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))

FIX = {
    ('2020数二真题', '5', 'stem', r'f(x,y)=\begin{cases}\end{cases}', r'f(x,y)=\begin{cases}'),
    ('2020数二真题', '14', 'stem', r'\begin{vmatrix}\end{vmatrix}', r'\begin{vmatrix}'),
    ('2020数二真题', '14', 'answer', r'\begin{vmatrix}\end{vmatrix}', r'\begin{vmatrix}'),
    ('2000数二真题', '12', 'answer', r'\begin{cases}\end{cases}', r'\begin{cases}'),
}

applied = 0
for t, no, f, old, new in FIX:
    vol = next(v for v in exam if v['id'] == t)
    q = next(x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no)
    v = q.get(f) or ''
    assert old in v, '未找到: %s 第%s题.%s 的 %r' % (t, no, f, old)
    q[f] = v.replace(old, new, 1)
    applied += 1
    print('已修: %s 第%s题.%s' % (t, no, f))

assert applied == len(FIX), '未全部应用'
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))

# 复查
d2 = json.load(io.open(P, encoding='utf-8'))
for t, no, f, old, new in FIX:
    vol = next(v for v in d2 if v['id'] == t)
    q = next(x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no)
    assert old not in (q.get(f) or ''), '仍残留: %s' % t
print('复查通过：4 处空环境错乱已修复，格式单行 =', io.open(P, encoding='utf-8').read().count('\n') == 0)