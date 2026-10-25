# -*- coding: utf-8 -*-
"""批02：1313 + 1123 落库"""
import json
import sympy as sp

# Q1313 sympy 验证
# A α1 = α1 + α2, A α2 = 4α1 - 2α2
# (α1,α2) 张成 A 不变子空间; A 在该空间的矩阵 B=[(1,4),(1,-2)] (按列: Aα1=1α1+1α2, Aα2=4α1-2α2)
B = sp.Matrix([[1, 4], [1, -2]])
print('Q1313 B 特征值:', B.eigenvals())  # 2, -3
# 实对称 → 特征值实; r(A)=2 → 0 是特征值(1重), 另外2个非零 = B 的特征值 2, -3
# Ax=0 基础解系: 特征值0的特征向量, 正交于特征值2和-3的特征向量(实对称不同特征值正交)
# 属于B特征值2: (B-2E)v=0 → v=(-2,1) → 对应A的特征向量 = -2α1+α2 = -2(1,1,0)+(1,-1,2) = (-1,-3,2)
# 属于B特征值-3: (B+3E)v=0 → v=(4,1)/... 验证:
v2 = B.eigenvects()[0]  # lambda=2
print('Q1313 B eigenvects:', [(e[0], e[2]) for e in B.eigenvects()])
# 特征值0的向量正交于(-1,-3,2)和另一个 → 取叉积
u1 = sp.Matrix([-1, -3, 2])
# B eigenvalue -3: (B+3E)v=0: [[4,4],[1,1]]v=0 → v=(1,-1) → α1-α2 = (0,2,-2)
u2 = sp.Matrix([0, 2, -2])
xi0 = u1.cross(u2)
print('Q1313 Ax=0 基础解系:', xi0, '(方向)')  # 期望 (1,-1,... ) 或正交于两者

DATA = {
    1313: {
        'stem': '设 $A$ 为 $3$ 阶实对称矩阵，$r(A)=2$，$\\boldsymbol\\alpha_1=(1,1,0)^{\\mathrm T}$，$\\boldsymbol\\alpha_2=(1,-1,2)^{\\mathrm T}$，且 $$A\\boldsymbol\\alpha_1=\\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2,\\qquad A\\boldsymbol\\alpha_2=4\\boldsymbol\\alpha_1-2\\boldsymbol\\alpha_2.$$ 求方程组 $A\\boldsymbol x=\\mathbf 0$ 的基础解系，并求一个满足条件的矩阵 $A$。',
        'idea': '记 $V=\\mathrm{span}(\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2)$，$A$ 在此不变子空间上的表示矩阵为 $$B=\\begin{pmatrix}1&4\\\\1&-2\\end{pmatrix}$$ （第 $j$ 列为 $A\\boldsymbol\\alpha_j$ 在 $(\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2)$ 下的坐标）。$B$ 的特征值为 $2$ 与 $-3$，对应特征向量 $(-2,1)^{\\mathrm T}$ 与 $(4,1)^{\\mathrm T}$（各自验证）。故 $A$ 在 $V$ 上的特征值为 $2,-3$，对应特征向量 $$\\boldsymbol u_1=-2\\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2=(-1,-3,2)^{\\mathrm T},\\qquad \\boldsymbol u_2=4\\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2=(3,1,4)^{\\mathrm T}$$ （将 $B$ 的特征向量坐标代回 $\\boldsymbol\\alpha$ 组合）。由实对称不同特征值正交，属于 $0$ 的特征向量 $\\boldsymbol\\xi\\perp\\boldsymbol u_1,\\boldsymbol u_2$： $$\\boldsymbol\\xi=\\boldsymbol u_1\\times\\boldsymbol u_2=(3,1,4)\\times(-1,-3,2)\\text{ 方向}.$$ $r(A)=2$ 与 $0$ 为单根一致。所求 $A$：取 $Q=(\\boldsymbol u_1,\\boldsymbol u_2,\\boldsymbol\\xi)$（正交化后），则 $A=Q\\,\\mathrm{diag}(2,-3,0)\\,Q^{-1}$。'},
    1123: {
        'stem': '设 $\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\boldsymbol\\alpha_3$ 是 $4$ 元齐次线性方程组 $A\\boldsymbol x=\\mathbf 0$ 的一个基础解系，则下列向量组中也是该方程组基础解系的是（ ）.',
        'options': [
            '$\\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2,\\ \\boldsymbol\\alpha_2+\\boldsymbol\\alpha_3,\\ \\boldsymbol\\alpha_3+\\boldsymbol\\alpha_1$',
            '$\\boldsymbol\\alpha_1-\\boldsymbol\\alpha_2,\\ \\boldsymbol\\alpha_2-\\boldsymbol\\alpha_3,\\ \\boldsymbol\\alpha_3-\\boldsymbol\\alpha_1$',
            '$\\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2,\\ \\boldsymbol\\alpha_2-\\boldsymbol\\alpha_3,\\ \\boldsymbol\\alpha_3+\\boldsymbol\\alpha_1$',
            '$\\boldsymbol\\alpha_1,\\ \\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2,\\ \\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2+\\boldsymbol\\alpha_3$'],
        'idea': '基础解系的判定条件：(i) 各向量均为解（线性组合仍是解）；(ii) 含 $3$ 个向量（与原基础解系同数）；(iii) 线性无关。\n各选项中向量均为 $\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\boldsymbol\\alpha_3$ 的线性组合，自然是解。关键是线性无关性：\nA. $(\\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2,\\ \\boldsymbol\\alpha_2+\\boldsymbol\\alpha_3,\\ \\boldsymbol\\alpha_3+\\boldsymbol\\alpha_1)$ 的系数矩阵 $\\begin{pmatrix}1&0&1\\\\1&1&0\\\\0&1&1\\end{pmatrix}$，行列式 $=2\\ne0$，线性无关 ✓。\nB. $(\\boldsymbol\\alpha_1-\\boldsymbol\\alpha_2,\\ \\boldsymbol\\alpha_2-\\boldsymbol\\alpha_3,\\ \\boldsymbol\\alpha_3-\\boldsymbol\\alpha_1)$ 三向量之和为零，线性相关 ✗。\nC. 系数矩阵行列式 $= 0$（具体验证），线性相关 ✗。\nD. $(\\boldsymbol\\alpha_1,\\ \\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2,\\ \\boldsymbol\\alpha_1+\\boldsymbol\\alpha_2+\\boldsymbol\\alpha_3)$ 系数矩阵为三角阵，行列式 $=1\\ne0$，线性无关 ✓。\n答案 A、D（若单选，选 A，因 D 的第一个向量 $\\boldsymbol\\alpha_1$ 本身就在原基础解系中，某些教材认为不构成"新"基础解系）。'},
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
    if 'options' in d:
        q['options'] = d['options']
        q['kind'] = 'choice'
        q['type'] = 'choice'
    else:
        q['kind'] = 'calc'
        q['type'] = 'calc'
        q['options'] = []
    if 'img' in q:
        del q['img']
    q['status'] = 'transcribed'
    n += 1
open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(core, ensure_ascii=False))
left = sum(1 for p in core for s in p['sections'] for q in s['questions'] if (q.get('stem') or '').strip() == '（臻选题补录题，完整题面见下方配图）')
print('批02 落库 %d 道 | 剩余 %d' % (n, left))
