# -*- coding: utf-8 -*-
"""批00：9 道自转录题落库（题干 LaTeX 我写 + 思路我写 + sympy 复验）"""
import json
import sympy as sp
import random

# ---- 落库前 sympy 复验 ----
random.seed(11)
# Q1109: 反对称 + β 的秩，n=2,3,4 各随机验证
def rankB(n):
    A = sp.zeros(n)
    for i in range(n):
        for j in range(i + 1, n):
            v = random.randint(-3, 3)
            A[i, j] = v
            A[j, i] = -v
    beta = sp.Matrix(n, 1, lambda i, j: random.randint(1, 3))
    B = sp.zeros(n + 1)
    B[:n, :n] = A
    B[:n, n] = beta
    B[n, :n] = beta.T
    return B.rank()
print('Q1109 n=2 rank:', [rankB(2) for _ in range(3)], '| n=3:', [rankB(3) for _ in range(3)],
      '| n=4:', [rankB(4) for _ in range(3)])
# 期望: n=2 → 2 (n), n=3 → 4 (n+1), n=4 → 4 (n) → 答案 C

B0 = sp.Matrix([[0, 0, 0], [1, 0, 3], [0, 1, -2]])
assert (B0 + sp.eye(3)).det() == -4
A2 = sp.diag(1, -1)
X = (2 * A2).inv() - 2 * A2.adjugate()   # (2A)* = 2^{n-1}A* = 2A*
Bb = sp.zeros(4)
Bb[:2, :2] = X
Bb[2:, 2:] = A2
assert (2 * Bb).det() == 100
print('Q1300/Q1084 复验通过')

DATA = {
    1300: {
        'stem': '设 $A$ 为 $3$ 阶矩阵，$\\boldsymbol{x}$ 为 $3$ 维列向量，向量组 $\\boldsymbol{x}, A\\boldsymbol{x}, A^2\\boldsymbol{x}$ 线性无关，且 $$A^3\\boldsymbol{x}=3A\\boldsymbol{x}-2A^2\\boldsymbol{x}.$$\n（I）记 $P=(\\boldsymbol{x},A\\boldsymbol{x},A^2\\boldsymbol{x})$，求 $3$ 阶矩阵 $B$，使 $AP=PB$；\n（II）求 $|A+E|$。',
        'idea': '由 $AP=PB$，$B$ 的第 $j$ 列就是 $A\\cdot(P\\text{ 的第}j\\text{列})$ 在基 $\\boldsymbol{x},A\\boldsymbol{x},A^2\\boldsymbol{x}$ 下的坐标：$A\\boldsymbol{x}=A\\boldsymbol{x}$、$A(A\\boldsymbol{x})=A^2\\boldsymbol{x}$、$A(A^2\\boldsymbol{x})=A^3\\boldsymbol{x}=3A\\boldsymbol{x}-2A^2\\boldsymbol{x}$，坐标分别为 $(0,1,0)^{\\mathrm T},(0,0,1)^{\\mathrm T},(0,3,-2)^{\\mathrm T}$，故 $$B=\\begin{pmatrix}0&0&0\\\\1&0&3\\\\0&1&-2\\end{pmatrix}.$$ 由 $AP=PB$ 且 $P$ 可逆得 $A=PBP^{-1}$，即 $A\\sim B$，从而 $$|A+E|=|B+E|=\\begin{vmatrix}1&0&0\\\\1&1&3\\\\0&1&-1\\end{vmatrix}=-4.$$'},
    1078: {
        'stem': '设 $n$ 阶实对称矩阵 $A$ 满足 $A^2+A=O$，$n$ 阶矩阵 $B$ 满足 $B^2+B=E$，且 $r(AB)=2$，求 $|A+2E|$。',
        'idea': '实对称矩阵可对角化。设 $\\lambda$ 为 $A$ 的特征值，由 $A^2+A=O$ 得 $\\lambda^2+\\lambda=0$，故 $\\lambda\\in\\{0,-1\\}$。设 $\\mu$ 为 $B$ 的特征值，$\\mu^2+\\mu-1=0$，$\\mu=\\dfrac{-1\\pm\\sqrt5}{2}\\ne0$，故 $B$ 可逆，于是 $$r(A)=r(AB)=2,$$ 即 $A$ 的特征值 $-1$ 恰有 $2$ 个、$0$ 恰有 $n-2$ 个。故 $A+2E$ 的特征值为 $1$（$2$ 重）与 $2$（$n-2$ 重）， $$|A+2E|=2^{\\,n-2}.$$'},
    1081: {
        'stem': '设 $\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\ldots,\\boldsymbol\\alpha_k\\ (k>1)$ 是 $n$ 维正交单位实列向量组，记 $$A=\\boldsymbol\\alpha_1\\boldsymbol\\alpha_1^{\\mathrm T}+\\boldsymbol\\alpha_2\\boldsymbol\\alpha_2^{\\mathrm T}+\\cdots+\\boldsymbol\\alpha_k\\boldsymbol\\alpha_k^{\\mathrm T},$$ 求 $|(A+E)^*|$。',
        'idea': '由 $\\boldsymbol\\alpha_i^{\\mathrm T}\\boldsymbol\\alpha_j=\\delta_{ij}$ 得 $(\\boldsymbol\\alpha_i\\boldsymbol\\alpha_i^{\\mathrm T})^2=\\boldsymbol\\alpha_i(\\boldsymbol\\alpha_i^{\\mathrm T}\\boldsymbol\\alpha_i)\\boldsymbol\\alpha_i^{\\mathrm T}=\\boldsymbol\\alpha_i\\boldsymbol\\alpha_i^{\\mathrm T}$，且不同下标的交叉项为 $O$，故 $A^2=A$（投影矩阵），其特征值为 $1$（$k$ 重）与 $0$（$n-k$ 重）。于是 $A+E$ 的特征值为 $2$（$k$ 重）与 $1$（$n-k$ 重），$|A+E|=2^k$， $$|(A+E)^*|=|A+E|^{\\,n-1}=2^{\\,k(n-1)}.$$'},
    1083: {
        'stem': '设 $A$ 为 $m$ 阶方阵且 $|A|=a$，$B$ 为 $n$ 阶方阵且 $|B|=b$，$C$ 为 $l$ 阶方阵且 $|C|=c$，求 $$\\begin{vmatrix}O&O&A\\\\O&B&O\\\\C&O&O\\end{vmatrix}.$$',
        'idea': '这是块反对角型行列式（非零块位于 $(1,3),(2,2),(3,1)$ 位置）。一般结论：块阶为 $s_1,s_2,\\ldots,s_k$ 的块反对角阵，其行列式 $=(-1)^{\\sum_{i<j}s_is_j}\\prod_i|A_i|$。两块时即熟悉的 $\\begin{vmatrix}O&A\\\\B&O\\end{vmatrix}=(-1)^{mn}|A||B|$。本题符号为 $(-1)^{mn+nl+lm}$，故 $$|D|=(-1)^{mn+nl+lm}\\,abc.$$（可用 $m,n,l$ 取小值随机数值验证该符号规律。）'},
    1084: {
        'stem': '设 $A$ 为 $2$ 阶矩阵且 $|A|=-1$，$$B=2\\begin{pmatrix}(2A)^{-1}-(2A)^*&O\\\\O&A\\end{pmatrix},$$ 求 $|B|$。',
        'idea': '对 $2$ 阶矩阵：$(2A)^{-1}=\\dfrac12A^{-1}=\\dfrac{A^*}{2|A|}=-\\dfrac{A^*}{2}$；$(2A)^*=2^{n-1}A^*=2A^*$。记 $X=(2A)^{-1}-(2A)^*=-\\dfrac52A^*$，则 $$|X|=\\Big(\\frac52\\Big)^2|A^*|=\\frac{25}{4}|A|^{n-1}=\\frac{25}{4}|A|=-\\frac{25}{4}.$$ $B$ 为 $4$ 阶矩阵，整体提出 $2$ 时每行提一个 $2$： $$|B|=2^4\\,|X|\\cdot|A|=16\\cdot\\Big(-\\frac{25}{4}\\Big)\\cdot(-1)=100.$$'},
    1188: {
        'stem': '设 $A=(a_{ij})$ 为 $3$ 阶矩阵，且 $a_{ij}=A_{ij}$（$A_{ij}$ 为 $a_{ij}$ 的代数余子式），$a_{33}\\ne0$。记 $\\boldsymbol b=(a_{13},a_{23},a_{33})^{\\mathrm T}$，求方程组 $A\\boldsymbol x=\\boldsymbol b$ 的解。',
        'idea': '$a_{ij}=A_{ij}$ 等价于 $A^{\\mathrm T}=A^*$，于是 $$AA^{\\mathrm T}=AA^*=|A|E.$$ 按第 $3$ 行展开：$|A|=a_{31}A_{31}+a_{32}A_{32}+a_{33}A_{33}=a_{31}^2+a_{32}^2+a_{33}^2>0$。又 $|AA^{\\mathrm T}|=|A|^3$（$3$ 阶）$=|A|^2\\cdot|A|$，结合 $AA^{\\mathrm T}=|A|E$ 得 $|A|^2=|A|^3$，故 $|A|=1$。于是 $A$ 为正交矩阵，$A^{\\mathrm T}=A^{-1}=A^*$。由 $\\boldsymbol b=A^{\\mathrm T}\\boldsymbol e_3$ 得 $$\\boldsymbol x=A^{-1}\\boldsymbol b=A^{\\mathrm T}\\boldsymbol b=A^*\\boldsymbol b,$$ 且 $A(A^{\\mathrm T}\\boldsymbol b)=|A|\\boldsymbol b=\\boldsymbol b$ 验证成立。'},
    1096: {
        'stem': '设 $A$ 为 $3$ 阶非零矩阵，$A^*$ 为 $A$ 的伴随矩阵，且 $A^*=-2A$，则 $A^2=$（ ）.',
        'options': ['$-4E$', '$4E$', '$-\\dfrac14E$', '$\\dfrac14E$'],
        'idea': '由 $A^*=-2A$ 两边左乘 $A$：$AA^*=|A|E=-2A^2$，故 $A^2=-\\dfrac{|A|}{2}E$。取行列式：$|A^*|=|-2A|$，即 $|A|^{n-1}=(-2)^n|A|$，$n=3$ 时 $|A|^2=-8|A|$，$|A|=0$ 或 $|A|=-8$。若 $|A|=0$，则 $A^2=O$，于是 $r(A)\\le1$，$3$ 阶矩阵 $r(A)\\le1$ 时 $r(A^*)=0$ 即 $A^*=O$，与 $A$ 非零且 $A^*=-2A$ 矛盾。故 $|A|=-8$， $$A^2=-\\frac{-8}{2}E=4E.$$ 答案选 B。'},
    1109: {
        'stem': '设 $A=(a_{ij})$ 为 $n$ 阶实反对称矩阵（$a_{ij}=-a_{ji}$），$\\boldsymbol\\beta$ 为 $n$ 维非零列向量，$$B=\\begin{pmatrix}A&\\boldsymbol\\beta\\\\\\boldsymbol\\beta^{\\mathrm T}&0\\end{pmatrix},$$ 则（ ）.',
        'options': ['$r(B)$ 恒等于 $n$', '$r(B)$ 恒等于 $n+1$', '$r(B)$ 可以等于 $n$，也可以等于 $n+1$', '$r(B)$ 与 $n$ 无关'],
        'idea': '考察 $B\\binom{\\boldsymbol y}{t}=\\mathbf 0$，即 $A\\boldsymbol y+t\\boldsymbol\\beta=\\mathbf 0$ 且 $\\boldsymbol\\beta^{\\mathrm T}\\boldsymbol y=0$。\n当 $n$ 为偶数时，可取 $A$ 可逆（反对称矩阵阶为偶数时可逆），则 $\\boldsymbol y=-tA^{-1}\\boldsymbol\\beta$；由 $A^{-1}$ 仍反对称知 $\\boldsymbol\\beta^{\\mathrm T}A^{-1}\\boldsymbol\\beta=0$，第二个方程自动满足，$t$ 可取 $1$，得非零解，此时 $r(B)=n$。\n当 $n$ 为奇数时，$|A|=0$ 且一般 $r(A)=n-1$，$\\ker A=\\mathrm{span}\\{\\boldsymbol u\\}$ 且 $\\operatorname{im}A$ 的正交补为 $\\ker A^{\\mathrm T}=\\ker A$；取 $\\boldsymbol\\beta\\notin\\operatorname{im}A$，则第一个方程强制 $t=0$，进而 $\\boldsymbol y\\in\\ker A$ 且 $\\boldsymbol\\beta^{\\mathrm T}\\boldsymbol y=0$ 强制 $\\boldsymbol y=\\mathbf 0$，只有零解，$r(B)=n+1$。\n故 $r(B)$ 既可以是 $n$ 也可以是 $n+1$（随机数值验证：$n=2$ 得 $2$，$n=3$ 得 $4$）。答案选 C。'},
    1202: {
        'stem': '设 $\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\ldots,\\boldsymbol\\alpha_m\\ (m\\le n)$ 为 $n$ 维列向量组，记 $A=(\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\ldots,\\boldsymbol\\alpha_m)$。证明：$\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\ldots,\\boldsymbol\\alpha_m$ 线性无关的充分必要条件是线性方程组 $A\\boldsymbol x=\\mathbf 0$ 只有零解。',
        'idea': '按定义，$\\boldsymbol\\alpha_1,\\ldots,\\boldsymbol\\alpha_m$ 线性相关 $\\iff$ 存在不全为零的 $x_1,\\ldots,x_m$ 使 $x_1\\boldsymbol\\alpha_1+\\cdots+x_m\\boldsymbol\\alpha_m=\\mathbf 0$。而 $$A\\boldsymbol x=x_1\\boldsymbol\\alpha_1+x_2\\boldsymbol\\alpha_2+\\cdots+x_m\\boldsymbol\\alpha_m,$$ 故「$A\\boldsymbol x=\\mathbf 0$ 有非零解」与「向量组线性相关」是同一件事，取逆否即得：线性无关 $\\iff$ $A\\boldsymbol x=\\mathbf 0$ 只有零解。等价说法：$r(A)=m$（列满秩）。'},
}

core = json.load(open('pwa/data/core_bank.json', encoding='utf-8'))
qmap = {q['no']: q for p in core for s in p['sections'] for q in s['questions']}
n = 0
for no, d in DATA.items():
    q = qmap[no]
    assert (q.get('stem') or '').strip() == '（臻选题补录题，完整题面见下方配图）', no
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
print('批00 落库 %d 道 | 剩余图片题 %d' % (n, left))
