# -*- coding: utf-8 -*-
# 最终修复 2003-13：raw 字符串避开转义；补块间开块后写盘
import json, io, subprocess, os

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2003数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '13')
v = q['answer']

OLD = r'x-\arcsin x}$$=\lim_{x\to 0^{-}}\frac{3ax^{2}}{1-\frac{1}{\sqrt{1-x^{2}}}}'
NEW = r'x-\arcsin x}$$\n$$\lim_{x\to 0^{-}}\frac{3ax^{2}}{1-\frac{1}{\sqrt{1-x^{2}}}}'

print('命中:', OLD in v)
if OLD in v:
    nv = v.replace(OLD, NEW, 1)
    q['answer'] = nv
    with io.open(P, 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('已写盘')
else:
    i = v.find('arcsin x')
    print('实际:', repr(v[i - 10:i + 80]))
