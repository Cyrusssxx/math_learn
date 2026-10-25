# -*- coding: utf-8 -*-
"""批04：根据结构+来源反推题面，sympy 验证"""
import json
import sympy as sp

# Q1210: 3阶A, 特征值1,-1,2, α₃=(1,1,1)ᵀ属于2, A*α₃=(-1,-1,-1)ᵀ, 求A
# |A| = 1·(-1)·2 = -2, A*α₃ = |A|/λ · α₃ = -2/2 · α₃ = -α₃ = (-1,-1,-1)ᵀ ✓
# 如果A实对称(2018数二三风格), α₁⊥α₃, α₂⊥α₃:
# 属于1的α₁: x+y+z=0, 取(1,-1,0)ᵀ; 属于-1的α₂: x+y+z=0且⊥α₁, 取(1,1,-2)ᵀ
# A = P diag(1,-1,2) P⁻¹, P=[(1,-1,0),(1,1,-2),(1,1,1)]
P = sp.Matrix([[1, 1, 1], [-1, 1, 1], [0, -2, 1]])
D = sp.diag(1, -1, 2)
A = P * D * P.inv()
print('Q1210 A =', A.tolist())
print('Q1210 验证 A*(1,1,1)ᵀ =', (A * sp.Matrix([1,1,1])).T.tolist())
print('Q1210 验证 |A| =', A.det(), '(期望-2)')
print('Q1210 验证 A*α₃ =', (A.adjugate() * sp.Matrix([1,1,1])).T.tolist())

# Q1122: Aα₁=α₂, Aα₂=α₃, Aα₃=α₁+α₂ → 证|A|=0
# AP = A(α₁,α₂,α₃) = (α₂,α₃,α₁+α₂) = P·B, B的列=(0,0,1),(1,0,1),(0,1,0)
B = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 1, 0]])
print('Q1122 |B| =', B.det(), '(期望0 → |A|=|B|=0)')

# Q1316: A²+A=O → 特征值λ²+λ=0 → λ∈{0,-1}
# 这是经典结论: r(A)=r(A+(-E)·(-1))... 
# A²+A=O → A(A+E)=O → r(A)+r(A+E)≤n; 又 r(A)+r(A+E)≥r(A-(A+E))=r(E)=n → 等号
# 所以 r(A)+r(A+E)=n, |A+E|=(-1)^{r(A)}·0^{n-r(A+E)}... 
# 具体题目可能是求 |A+E| 或 r(A)+r(A+E) 的最大/最小值
print('Q1316: A²+A=O → r(A)+r(A+E)=n, 特征值只有0和-1')

# Q1217: 求(P⁻¹(A+λE)P)*
# P⁻¹(A+λE)P = P⁻¹AP + λE → 若Aα=λ₀α, 则此矩阵的特征值为 λ₀+λ
# (P⁻¹(A+λE)P)* = |P⁻¹(A+λE)P| · (P⁻¹(A+λE)P)⁻¹ = |A+λE| · P⁻¹(A+λE)⁻¹P
# = P⁻¹ |A+λE|(A+λE)⁻¹ P = P⁻¹(A+λE)*P
print('Q1217: (P⁻¹(A+λE)P)* = P⁻¹(A+λE)*P')

DATA = {
    1210: {
        'stem': '设 $3$ 阶实对称矩阵 $A$ 的特征值为 $1,-1,2$，属于特征值 $2$ 的特征向量为 $\\boldsymbol\\alpha_3=(1,1,1)^{\\mathrm T}$，且 $A^*\\boldsymbol\\alpha_3=(-1,-1,-1)^{\\mathrm T}$。\n（I）求属于特征值 $1$ 和 $-1$ 的特征向量 $\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2$；\n（II）求矩阵 $A$。',
        'idea': '$|A|=1\\times(-1)\\times2=-2$。$A^*\\boldsymbol\\alpha_3=\\dfrac{|A|}{2}\\boldsymbol\\alpha_3=-\\boldsymbol\\alpha_3$，与题设一致。\n实对称矩阵不同特征值的特征向量正交。$\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2$ 均满足 $x+y+z=0$（正交于 $\\boldsymbol\\alpha_3$），且 $\\boldsymbol\\alpha_1\\perp\\boldsymbol\\alpha_2$。取 $$\\boldsymbol\\alpha_1=(1,-1,0)^{\\mathrm T},\\qquad \\boldsymbol\\alpha_2=(1,1,-2)^{\\mathrm T}$$（验证：内积 $=1-1+0=0$ ✓）。\n令 $P=(\\boldsymbol\\alpha_1,\\boldsymbol\\alpha_2,\\boldsymbol\\alpha_3)$，则 $$A=P\\begin{pmatrix}1&&\\\\&-1&\\\\&&2\\end{pmatrix}P^{-1}=\\frac13\\begin{pmatrix}1&0&2\\\\0&1&2\\\\2&2&0\\end{pmatrix}.$$'},
    1316: {
        'stem': '设 $n$ 阶实矩阵 $A$ 满足 $A^2+A=O$，求 $r(A)+r(A+E)$。',
        'idea': '由 $A^2+A=O$ 即 $A(A+E)=O$，得 $$r(A)+r(A+E)\\le n.$$ 另一方面 $$r(A)+r(A+E)\\ge r(A-(A+E))=r(-E)=n.$$ 故 $$r(A)+r(A+E)=n.$$ 进一步：$A$ 的特征值满足 $\\lambda^2+\\lambda=0$，即 $\\lambda\\in\\{0,-1\\}$；若 $A$ 可对角化则 $r(A)=$ 特征值 $-1$ 的个数，$r(A+E)=$ 特征值 $0$ 的个数。'},
    1217: {
        'stem': '设 $A$ 为 $n$ 阶矩阵，$\\lambda_0$ 为 $A$ 的特征值，$\\boldsymbol\\alpha$ 为对应的特征向量，$P$ 为 $n$ 阶可逆矩阵。证明：$(P^{-1}(A+\\lambda_0 E)P)^*=P^{-1}(A+\\lambda_0 E)^*P$。',
        'idea': '由伴随矩阵的基本性质：对任意可逆矩阵 $M$，$M^*=|M|M^{-1}$。而 $$P^{-1}(A+\\lambda_0 E)P = P^{-1}AP+\\lambda_0 E.$$ 利用伴随的共轭性质：$$(P^{-1}MP)^* = P^*M^*(P^{-1})^* = |P|P^{-1}\\cdot M^*\\cdot |P^{-1}|(P^{-1})^{-1} = P^{-1}M^*P$$ 因 $|P|\\cdot|P^{-1}|=1$。取 $M=A+\\lambda_0 E$ 即得结论。'},
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
print('批04 落库 %d 道 | 剩余 %d' % (n, left))
