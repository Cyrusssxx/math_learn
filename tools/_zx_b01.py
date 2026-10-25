# -*- coding: utf-8 -*-
"""批01：确定题落库 + 存疑题标记跳过"""
import json
import sympy as sp

# ---- sympy 验证 ----
# Q1205: 方程组 x1+2x2+x3=3; 2x1+(k+4)x2-5x3=6; -x1-2x2+kx3=-3 有无穷多解
k, x1, x2, x3 = sp.symbols('k x1 x2 x3')
M = sp.Matrix([[1, 2, 1], [2, k+4, -5], [-1, -2, k]])
Aug = sp.Matrix([[1, 2, 1, 3], [2, k+4, -5, 6], [-1, -2, k, -3]])
# 无穷多解: r(A)=r(Aug)<3
for kv in range(0, 10):
    rv = M.subs(k, kv).rank()
    ra = Aug.subs(k, kv).rank()
    if rv == ra and rv < 3:
        print('Q1205 k=%d r=%d (无穷多解)' % (kv, rv))

# Q1215: (a-b)I + bJ 的特征值/基础解系
# A = [[a,b,...],[b,a,...],...], 特征值 a+(n-1)b (1重), a-b (n-1重)
# a=b 时 A 全 b 矩阵, r=1, 基础解系 n-1 个
# a≠b 时: a=b? 分情况: a+(n-1)b=0 或 a-b=0
print('Q1215 分类讨论: a=b(全b), a≠b 且 a+(n-1)b=0, a≠b 且 a+(n-1)b≠0')

# Q1117: ABA=A 广义逆构造, 验证 A=diag(1,...,1,0,...,0) 时 B=A
A_test = sp.diag(1, 1, 0)
B_test = sp.diag(1, 1, 0)
print('Q1117 对角形验证 ABA=A:', A_test * B_test * A_test == A_test)

DATA = {
    1205: {
        'stem': '设线性方程组 $$\\begin{cases}x_1+2x_2+x_3=3,\\\\2x_1+(k+4)x_2-\\phantom{-}5x_3=6,\\\\-x_1-2x_2+kx_3=-3\\end{cases}$$ 有无穷多解，求 $k$ 的值并求通解。',
        'idea': '增广矩阵 $$\\bar A=\\begin{pmatrix}1&2&1&3\\\\2&k+4&-5&6\\\\-1&-2&k&-3\\end{pmatrix}\\xrightarrow{\\text{行变换}}\\begin{pmatrix}1&2&1&3\\\\0&k&-7&0\\\\0&0&k+1&0\\end{pmatrix}.$$ 有无穷多解要求 $r(A)=r(\\bar A)<3$，故 $k=0$（$k\\ne0$ 时 $r=3$ 唯一解）。$k=0$ 时 $\\bar A\\to\\begin{pmatrix}1&2&1&3\\\\0&0&-7&0\\\\0&0&1&0\\end{pmatrix}\\to\\begin{pmatrix}1&2&0&3\\\\0&0&1&0\\end{pmatrix}$，通解 $$\\boldsymbol x=(3,0,0)^{\\mathrm T}+t(-2,1,0)^{\\mathrm T},\\quad t\\in\\mathbb R.$$'},
    1117: {
        'stem': '设 $A$ 为 $n$ 阶实对称矩阵，且 $r(A)=r<n$。证明：存在 $n$ 阶实矩阵 $B$，使得 $$ABA=A.$$',
        'idea': '实对称矩阵可正交对角化：存在正交矩阵 $Q$ 使 $$A=Q\\begin{pmatrix}\\lambda_1&&&\\\\&\\ddots&&\\\\&&\\lambda_r&\\\\&&&0\\\\&&&&\\ddots\\\\&&&&&0\\end{pmatrix}Q^{\\mathrm T}$$ 其中 $\\lambda_i\\ne0$（$i\\le r$）。取 $$B=Q\\begin{pmatrix}\\lambda_1^{-1}&&&\\\\&\\ddots&&\\\\&&\\lambda_r^{-1}&\\\\&&&0\\\\&&&&\\ddots\\\\&&&&&0\\end{pmatrix}Q^{\\mathrm T}$$ 则 $ABA=Q\\Lambda Q^{\\mathrm T}\\cdot Q\\Lambda^{+}Q^{\\mathrm T}\\cdot Q\\Lambda Q^{\\mathrm T}=Q\\Lambda\\Lambda^{+}\\Lambda Q^{\\mathrm T}=Q\\Lambda Q^{\\mathrm T}=A$（$\\Lambda\\Lambda^+\\Lambda=\\Lambda$，因对角只需逐元素验证 $\\lambda\\cdot\\lambda^{-1}\\cdot\\lambda=\\lambda$，零行自然为零）。'},
    1215: {
        'stem': '设 $n$ 元齐次线性方程组 $$\\begin{cases}ax_1+bx_2+bx_3+\\cdots+bx_n=0,\\\\bx_1+ax_2+bx_3+\\cdots+bx_n=0,\\\\\\quad\\vdots\\\\bx_1+bx_2+\\cdots+bx_{n-1}+ax_n=0\\end{cases}$$ 求它的基础解系。',
        'idea': '系数矩阵 $A=(a-b)E+bJ$（$J$ 为全 $1$ 矩阵），特征值为 $a+(n-1)b$（$1$ 重，特征向量 $(1,\\ldots,1)^{\\mathrm T}$）与 $a-b$（$n-1$ 重）。\n① $a\\ne b$ 且 $a\\ne-(n-1)b$：$|A|\\ne0$，只有零解。\n② $a=b$（$A=bJ$，$r=1$）：基础解系为 $\\boldsymbol\\xi_1=(1,-1,0,\\ldots,0)^{\\mathrm T},\\ldots,\\boldsymbol\\xi_{n-1}=(1,0,\\ldots,0,-1)^{\\mathrm T}$（$n-1$ 个）。\n③ $a\\ne b$ 且 $a=-(n-1)b$：$r(A)=n-1$，基础解系仅 $\\boldsymbol\\xi=(1,1,\\ldots,1)^{\\mathrm T}$。'},
    1212: {
        'stem': '设 $\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\ldots,\\boldsymbol\\alpha_m\\ (m\\le n)$ 为 $n$ 维列向量组，记 $A=(\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\ldots,\\boldsymbol\\alpha_m)$。证明：$\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\ldots,\\boldsymbol\\alpha_m$ 线性无关的充分必要条件是齐次线性方程组 $A\\boldsymbol x=\\mathbf 0$ 只有零解。',
        'idea': '同 core#1202（书内重复收录）。按定义，$\\alpha_1,\\ldots,\\alpha_m$ 线性相关 $\\iff$ 存在不全为零的系数使 $x_1\\alpha_1+\\cdots+x_m\\alpha_m=\\mathbf 0$，而 $A\\boldsymbol x$ 正是这个线性组合。故「$A\\boldsymbol x=\\mathbf 0$ 有非零解」$\\iff$「线性相关」，取逆否即得结论。等价说法：$r(A)=m$。'},
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
    q['kind'] = 'calc'
    q['type'] = 'calc'
    q['options'] = []
    if 'img' in q:
        del q['img']
    q['status'] = 'transcribed'
    n += 1
open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(core, ensure_ascii=False))
left = sum(1 for p in core for s in p['sections'] for q in s['questions'] if (q.get('stem') or '').strip() == '（臻选题补录题，完整题面见下方配图）')
print('批01 落库 %d 道 | 剩余图片题 %d' % (n, left))
print('跳过(转录不完整): 1174(命题组合), 1113(命题组合), 1312(矩阵待定), 1121(选项不全), 1217(Jordan块结构待定), 1210(实对称条件未确认)')
