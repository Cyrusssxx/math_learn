# -*- coding: utf-8 -*-
# 补全 no=216 的解析（答案 a=-6,b=2 已用 sympy 验证：det A=a+6, det B=7(b-2)）
import json, io

P = 'pwa/data/xd_bank.json'
d = json.load(io.open(P, encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]
q = next(x for x in qs if str(x['no']) == '216')

q['idea'] = (
    '设 $A=(\\alpha_1,\\alpha_2,\\alpha_3)$，$B=(\\beta_1,\\beta_2,\\beta_3)$。'
    '计算 $|A|=a+6$，$|B|=7(b-2)$。'
    '因 $A\\mathbf{x}=\\beta_1$ 无解，$\\beta_1$ 不能由 $\\alpha_1,\\alpha_2,\\alpha_3$ 线性表示，'
    '故 $r(A)<3$（否则三向量可作为基表示任意向量），即 $a=-6$，此时 $r(A)=2$。'
    '又 $r(B)=r(A)=2$，则 $|B|=7(b-2)=0$，得 $b=2$（且此时 $r(B)=2$，与 $r(A)$ 相等）。'
    '综上 $a=-6,\\ b=2$。'
)
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(d, fp, ensure_ascii=False, separators=(',', ':'))
print('no=216 解析已补全:', q['idea'][:80])

# 复查全库
d2 = json.load(io.open(P, encoding='utf-8'))
q2 = [q for s in d2[0]['sections'] for q in s['questions']]
todo = [x['no'] for x in q2 if '待补充' in str(x.get('idea') or '')]
print('全库仍含「待补充」:', todo or '无')
print('总题数:', len(q2))