# -*- coding: utf-8 -*-
# 最终收尾：2003-13 第二处块间开块；2003-22 方程组 $$ 独立行
import json, io

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))


def getq(rid, no):
    return next(x for v in exam if v['id'] == rid for s in v['sections'] for x in s['questions'] if str(x['no']) == no)


q13 = getq('2003数二真题', '13')
v = q13['answer']
OLD13 = r'\text{极限的四则运算})$$=\lim_{x\to 0^{-}}\frac{3ax^{2}}{\sqrt{1-x^{2}}-1}'
NEW13 = r'\text{极限的四则运算})$$\n$$\lim_{x\to 0^{-}}\frac{3ax^{2}}{\sqrt{1-x^{2}}-1}'
if OLD13 in v:
    q13['answer'] = v.replace(OLD13, NEW13, 1)
    print('OK 2003-13 第二处')
else:
    print('W 2003-13 未命中:', repr(v[v.find('四则运算') - 10:v.find('四则运算') + 60]))

q22 = getq('2003数二真题', '22')
v = q22['answer']
OLD22 = '方程组$$\\begin{cases}ax+2by=-3c'
NEW22 = '方程组\n$$\n\\begin{cases}ax+2by=-3c'
if OLD22 in v:
    q22['answer'] = v.replace(OLD22, NEW22, 1)
    print('OK 2003-22 方程组独立行')
else:
    i = v.find('方程组')
    print('W 2003-22 未命中:', repr(v[i:i + 50]))

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
