# -*- coding: utf-8 -*-
"""批03: Q1108 落库"""
import json
import sympy as sp

# Q1108 验证: A 为 m×n, r(A)=m (行满秩)
# A. PA=A, P m阶 → P=E? 反例: m=1,n=2, A=[1,0], P=[2] → PA=[2,0]≠A 不行; P=[1] → PA=A ✓ 但 P 不必为 E?
#    实际: PA=A 意味着 (P-E)A=O, 即 P-E 的每行 ⊥ A 的行空间. A 行满秩 → A 的行空间 = R^m → P-E=O → P=E ✓
#    等等, (P-E)A=O 表示 P-E 的行向量与 A 的所有列正交. A m×n 行满秩 → A 的列空间 ⊆ R^m 满维?
#    A 的列空间 ⊆ R^m, dim = r = m → 列空间 = R^m → P-E=O → A ✓
# B. AP=A, P n阶 → (A)(P-E)=O, 即 A 的行 × (P-E) 的列 = 0. 这要求 P-E 的列 ⊥ A 的行空间.
#    A 的行空间 ⊆ R^n, dim = m < n (行满秩但列不满). P-E 的列可以取在 A 的零空间中 → P-E ≠ O 可能 → B ✗
# C. 行变换化 (E_m, O) ✓ (行满秩的标准形)
# D. 列变换化 (E_m, O)? 列变换改变列空间. r(A)=m → 存在可逆 Q (n阶) 使 AQ = [B, O] 其中 B m×m 可逆.
#    再配合行变换... 但只做列变换? A=[1,0] (m=1,n=2): 列变换只能调换/缩放列 → [λ, 0] ≠ [1, 0] 除非...
#    列变换: A=C₁C₂...A 的列可重新组合. A=[1,0], 列变换(右乘可逆2阶阵Q): [1,0]Q = Q的第一行.
#    取 Q = [[1,0],[0,2]] → [1,0] ✓ 已经是 (E₁,O). 但取 A=[1,1]: [1,1]Q = (Q的第1行加第2行)... 
#    取 Q 使 [1,1]Q=[1,0]: Q=[[1,0],[-1,1]]? [1,1]×[[1,0],[-1,1]] = [1-1, 0+1]=[0,1] 不行
#    Q=[[1,0],[0,0]]不可逆. 试试 Q=[[1,0],[-1,1]]: [1·1+1·(-1), 1·0+1·1]=[0,1] ≠ [1,0]
#    Q=[[1,0],[0,t]]: [1,t] ≠ [1,0] 除非 t=0 但不可逆
#    所以 [1,1] 不能仅通过列变换化为 [1,0]? 但 [1,1] 可以通过列变换(列2减列1)化为... 列变换是右乘: [1,1]Q
#    Q 的作用是组合列: 新列 = 旧列的线性组合. [1,1]Q = (q₁₁+q₂₁, q₁₂+q₂₂) = Q的行和
#    要 = [1,0]: 需 Q 第一列行和=1, 第二列行和=0, |Q|≠0. Q=[[1,0],[0,1]]: [1,1]≠[1,0] ✗
#    Q=[[1,-1],[0,1]]: 行和=[1,0] ✓ |Q|=1 ✓! 所以 [1,1]Q = [1,0] ✓ 可以!
#    一般: r(A)=m, A 可经列变换使前 m 列化为可逆 B, 剩余列 → 调整使得非零列吸收? 
#    实际结论: 任何 r(A)=r 的矩阵可经列变换化为 (B_r, O) 其中 B_r 是 m×r 列满秩.
#    若 m=r: B 可逆 m×m → 再取 B⁻¹... 不对, 列变换是右乘, A Q = [B, O] (m×n), B 是 m×m 可逆
#    要化成 (E_m, O): 需再右乘 diag(B⁻¹, E) → [E_m, O] ✓ 所以 D ✓
# 结论: A ✓, B ✗, C ✓, D ✓ → 答案 A、C、D（如果单选，答案可能是 ACD 或按题目要求选不正确的 → B）
# 常见出法: "则下列结论正确的是" 单选 → 可能只考一个最佳答案
print('Q1108 逻辑验证: A✓(列满秩消去) B✗(零空间非零) C✓(标准形) D✓(列变换化标准形)')

DATA = {
    1108: {
        'stem': '设 $A$ 为 $m\\times n$ 矩阵，$r(A)=m$，则下列结论正确的是（ ）.',
        'options': [
            '若 $P$ 为 $m$ 阶矩阵且 $PA=A$，则 $P=E$',
            '若 $P$ 为 $n$ 阶矩阵且 $AP=A$，则 $P=E$',
            '$A$ 可经过初等行变换化为 $(E_m,\\ O)$',
            '$A$ 可经过初等列变换化为 $(E_m,\\ O)$'],
        'idea': '$r(A)=m$ 即行满秩（隐含 $m\\le n$），列空间 $=\\mathbb R^m$。\n**A ✓**：$PA=A\\iff(P-E)A=O$，即 $P-E$ 的每一行与 $A$ 的所有列正交；$A$ 列满维（$\\dim=m$）故 $P-E=O$。\n**B ✗**：$AP=A\\iff A(P-E)=O$，$P-E$ 的列可取自 $A$ 的零空间 $N(A)$（$\\dim=n-m\\ge1$，因 $m<n$ 或 $m=n$ 时为零空间无选取；若 $m<n$ 则 $N(A)\\ne\\{\\mathbf 0\\}$，存在 $P\\ne E$ 使 $AP=A$）。\n**C ✓**：行满秩矩阵经初等行变换必可化为简化行阶梯形 $(E_m,\\ O)$（标准形定理）。\n**D ✓**：$r(A)=m$ 时存在可逆 $Q$（$n$ 阶）使 $AQ=(B,\\ O)$，$B$ 为 $m$ 阶可逆；再右乘 $\\begin{pmatrix}B^{-1}&O\\\\O&E\\end{pmatrix}$ 得 $(E_m,\\ O)$，两次均为初等列变换的复合。\n综上 **A、C、D 正确**；若单选选不正确的，则选 **B**。'},
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
print('批03 落库 %d 道 | 剩余 %d' % (n, left))
