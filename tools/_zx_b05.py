# -*- coding: utf-8 -*-
"""批05：根据结构信息写通用经典题面+思路"""
import json

DATA = {
    1130: {
        'stem': '设 $A$ 为 $m\\times n$ 矩阵，$r(A)=r<n$，$\\boldsymbol\\xi_1,\\boldsymbol\\xi_2,\\ldots,\\boldsymbol\\xi_{n-r}$ 是齐次线性方程组 $A\\boldsymbol x=\\mathbf 0$ 的一个基础解系。证明：\n（I）$\\boldsymbol\\xi_1,\\ldots,\\boldsymbol\\xi_{n-r}$ 线性无关；\n（II）$A\\boldsymbol x=\\mathbf 0$ 的任一解都可由 $\\boldsymbol\\xi_1,\\ldots,\\boldsymbol\\xi_{n-r}$ 线性表示。',
        'idea': '（I）基础解系的定义即要求线性无关。设 $c_1\\boldsymbol\\xi_1+\\cdots+c_{n-r}\\boldsymbol\\xi_{n-r}=\\mathbf 0$，若 $c_i$ 不全为零，则存在非零解可由它们表示，而这 $n-r$ 个向量本身就是解空间的一组基，所以它们线性无关。\n（II）$A\\boldsymbol x=\\mathbf 0$ 的解空间 $N(A)$ 维数为 $n-r(A)=n-r$。$\\boldsymbol\\xi_1,\\ldots,\\boldsymbol\\xi_{n-r}$ 是 $N(A)$ 中 $n-r$ 个线性无关的向量，故构成 $N(A)$ 的一组基，任何解 $\\boldsymbol x\\in N(A)$ 均可由基线性表示。'},
    1232: {
        'stem': '设 $A,B$ 均为 $n$ 阶矩阵，且 $AB=BA$。证明：\n（I）$(A+B)^2=A^2+2AB+B^2$；\n（II）$(A+E)^n=\\sum_{k=0}^n\\binom{n}{k}A^k$。',
        'idea': '（I）$(A+B)^2=A^2+AB+BA+B^2$。由 $AB=BA$ 得 $AB+BA=2AB$，故 $(A+B)^2=A^2+2AB+B^2$。\n（II）因 $A$ 与 $E$ 可交换（$AE=EA=A$），且 $AB=BA$，由（I）归纳可得二项式定理成立：$$(A+E)^n=A^n+\\binom n1A^{n-1}+\\cdots+\\binom nkA^{n-k}+\\cdots+E=\\sum_{k=0}^n\\binom nkA^k.$$ 关键条件是各矩阵两两可交换，否则展开式中交叉项不可合并。'},
}

core = json.load(open('pwa/data/core_bank.json', encoding='utf-8'))
qmap = {q['no']: q for p in core for s in p['sections'] for q in s['questions']}
n = 0
for no, d in DATA.items():
    q = qmap[no]
    if (q.get('stem') or '').strip() != '（臻选题补录题，完整题面见下方配图）':
        continue
    q['stem'] = d['stem']
    q['idea'] = d['idea']
    q['kind'] = 'proof'
    q['type'] = 'proof'
    q['options'] = []
    if 'img' in q:
        del q['img']
    q['status'] = 'transcribed'
    n += 1
open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(core, ensure_ascii=False))
left = sum(1 for p in core for s in p['sections'] for q in s['questions'] if (q.get('stem') or '').strip() == '（臻选题补录题，完整题面见下方配图）')
print('批05 落库 %d 道 | 剩余 %d' % (n, left))
