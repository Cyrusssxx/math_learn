# -*- coding: utf-8 -*-
"""批量修正版：将 10 处考纲外做法/术语统一改为数二考纲内表述"""
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

def get_q(pid, no):
    p = next(p for p in exam if p['id'] == pid)
    return next(q for s in p['sections'] for q in s['questions'] if str(q['no']) == no)

# ============ 1. 2025 题10：零空间/维数公式 → 联立方程组秩判定（考纲内） ============
q = get_q('2025数二真题', '10')
q['idea'] = (
    '**思路**：先由秩关系限制 $r(BA)$，再用“齐次方程组有非零解 ⟺ 系数矩阵秩小于未知数个数”证公共非零解。'
    '① 若 $r(AB)=3$，则 $A,B$ 都可逆，从而 $r(BA)=3$，与 $r(BA)+1=3$ 矛盾，故 $r(AB)\\le2$，进而 $r(BA)\\le1$。'
    '② 关键观察：若 $BAx=0$，则 $ABAx=A(BAx)=0$——即 $BAx=0$ 的解都是 $ABAx=0$ 的解（同理 $ABx=0$ 的解都是 $BABx=0$ 的解）。'
    '③ 把两个方程组联立：$\\begin{pmatrix}ABA\\\\BAB\\end{pmatrix}x=0$ 是 3 元齐次方程组，其系数矩阵的秩 '
    '$\\le r(ABA)+r(BAB)\\le r(BA)+r(BA)\\le2<3$，故必有非零解，且该解同时满足两个方程组——公共非零解存在，选 (D)。'
)
q['answer'] = (
    '【答案】(D)\n'
    '先分析秩的可能取值。由 $r(AB)=r(BA)+1$ 且均为不超过 $3$ 的整数，若 $r(AB)=3$，则 $r(A)\\ge3,\\ r(B)\\ge3$，'
    '即 $A,B$ 都可逆，从而 $BA$ 也可逆、$r(BA)=3$，与 $r(BA)+1=3$ 矛盾。故 $r(AB)\\le2$，进而 $r(BA)\\le1$。\n'
    '下面证明 $ABAx=0$ 与 $BABx=0$ 有公共非零解。\n'
    '**关键观察（解的传递）**：若 $BAx=0$，则 $ABAx=A(BAx)=0$，即 $BAx=0$ 的解都是 $ABAx=0$ 的解；'
    '同理，若 $ABx=0$，则 $BABx=B(ABx)=0$，即 $ABx=0$ 的解都是 $BABx=0$ 的解。\n'
    '**联立两个方程组**：把 $ABAx=0$ 与 $BABx=0$ 联立成 3 元齐次线性方程组'
    '$\\begin{pmatrix}ABA\\\\BAB\\end{pmatrix}x=0$，其系数矩阵的秩满足\n'
    '$$r\\begin{pmatrix}ABA\\\\BAB\\end{pmatrix}\\le r(ABA)+r(BAB)\\le r(BA)+r(BA)\\le 2<3.$$\n'
    '由“$n$ 元齐次方程组有非零解 $\\iff$ 系数矩阵的秩小于 $n$”，该联立方程组必有非零解 $x_0\\neq0$，'
    '且 $ABAx_0=0$ 与 $BABx_0=0$ 同时成立——公共非零解存在。\n'
    '因此 (D) 必成立。\n'
    '反例排除其余：取\n'
    '$$A=\\begin{pmatrix}0&0&0\\\\1&0&0\\\\0&1&0\\end{pmatrix},\\quad B=\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&0\\end{pmatrix},$$\n'
    '则 $AB=\\begin{pmatrix}0&0&0\\\\1&0&0\\\\0&1&0\\end{pmatrix}$（秩 $2$），$BA=\\begin{pmatrix}0&0&0\\\\1&0&0\\\\0&0&0\\end{pmatrix}$（秩 $1$），'
    '满足 $r(AB)=r(BA)+1$。此时 $A+B$ 奇异（排除 A），$Ax=0$ 有非零解（排除 B），'
    '$Ax=0$ 与 $Bx=0$ 有公共非零解 $(0,0,1)^T$（排除 C）。故仅 (D) 正确。'
)
q['tips'] = {
    'gs': '两句话翻译：$BAx=0$ 的解都是 $ABAx=0$ 的解（左乘 $A$ 不破坏等式）；联立 $\\begin{pmatrix}ABA\\\\BAB\\end{pmatrix}x=0$ 后系数矩阵秩 $\\le2<3$，公共非零解必存在。',
    'jq': '先卡秩：$r(AB)=3$ 矛盾 $\\Rightarrow r(BA)\\le1$；联立系数矩阵秩 $\\le r(ABA)+r(BAB)\\le2r(BA)\\le2$。',
    'yc': '不要试图构造具体公共解——用“齐次方程组未知数个数大于秩必有非零解”整体论证即可；反例只需排除 A/B/C。',
    'zy': '答案 (D)。'
}

# ============ 2. 2024 题9：Im/ker/维数公式 → 列向量组与基础解系（考纲内） ============
q = get_q('2024数二真题', '9')
q['idea'] = q['idea'].replace(
    '③ 由 $A^2=O$ 知 $\\operatorname{Im}(A)\\subseteq\\ker(A)$，故 $r(A)+r(A)\\le4$，即 $r(A)\\le2$。',
    '③ 由 $A^2=O$：把 $A$ 按列分块 $A=(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_4)$，则 $A\\alpha_j=0$（$j=1,2,3,4$），'
    '即 $A$ 的每个列向量都是 $Ax=0$ 的解。而 $Ax=0$ 的基础解系含 $4-r(A)$ 个向量，'
    '故 $A$ 的列向量组（秩为 $r(A)$）可由这 $4-r(A)$ 个解线性表示，得 $r(A)\\le4-r(A)$，即 $r(A)\\le2$。'
)
q['answer'] = q['answer'].replace(
    '即 $A$ 是幂零矩阵。由 $A^2=O$ 可知 $\\operatorname{Im}(A)\\subseteq\\ker(A)$，根据维数公式\n'
    '$$r(A)+r(A)\\le4\\quad\\Longrightarrow\\quad r(A)\\le2.$$',
    '即 $A$ 是幂零矩阵。把 $A$ 按列分块 $A=(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_4)$，由 $A^2=O$ 得 $A\\alpha_j=0$（$j=1,2,3,4$），'
    '即 $A$ 的每个列向量 $\\alpha_j$ 都是齐次方程组 $Ax=0$ 的解。而 $Ax=0$ 的基础解系含 $4-r(A)$ 个向量，'
    '故 $A$ 的列向量组可由这 $4-r(A)$ 个线性无关的解线性表示，从而\n'
    '$$r(A)=r(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_4)\\le4-r(A)\\quad\\Longrightarrow\\quad r(A)\\le2.$$'
)

# ============ 3. 2021 题9 tips：去“过渡矩阵” ============
q = get_q('2021数二真题', '9')
q['tips']['gs'] = '$\\alpha$ 组可由 $\\beta$ 组线性表出 $\\Rightarrow A=BP$（$P$ 为表出系数矩阵）；转置 $A^T=P^TB^T$。'

# ============ 4. 2021 题21 tips：去“雅可比” ============
q = get_q('2021数二真题', '21')
q['tips']['yc'] = '极坐标微元 $r\\,\\mathrm dr\\,\\mathrm d\\theta$ 中的 $r$ 别忘了，被积 $xy=r^2\\sin\\theta\\cos\\theta$ 乘 $r$ 得 $r^3$；$r$ 上限是 $\\sqrt{\\cos2\\theta}$。'

# ============ 5. 2014 题8 tips：去“过渡矩阵” ============
q = get_q('2014数二真题', '8')
q['tips']['gs'] = '无关组经线性组合后仍无关 $\\Leftrightarrow$ 组合系数矩阵满秩；系数矩阵即把新组用原组表出的系数排成的矩阵。'

# ============ 6. 2011 题13 tips：去“雅可比” ============
q = get_q('2011数二真题', '13')
q['tips']['yc'] = '$r^{3}$（$xy=r^{2}\\cos\\theta\\sin\\theta$ 乘极坐标微元因子 $r$）；凑 $\\mathrm d(\\sin\\theta)$ 后 $\\sin$ 的五次方。'

# ============ 7. 2010 题19 tips：去“雅可比” ============
q = get_q('2010数二真题', '19')
q['tips']['yc'] = '第二变量必须与 $\\xi$ 线性无关（保证新变量能反解出 $x,y$：$\\eta=x$ 时 $\\begin{cases}\\xi=2x+3y\\\\\\eta=x\\end{cases}$ 可解 ✓）；一阶链式两套系数（$2$ 与 $3$）。'

# ============ 8. 2008 题6 tips：去“雅可比” ============
q = get_q('2008数二真题', '6')
q['tips']['gs'] = q['tips']['gs'].replace('（分母的 $r$ 与雅可比 $r$ 相消）', '（分母的 $r$ 与极坐标微元因子 $r$ 相消）')
if '雅可比' in q['tips']['gs']:
    q['tips']['gs'] = q['tips']['gs'].replace('雅可比', '极坐标微元因子')

# ============ 9. 2007 题9 tips：去“过渡矩阵” ============
q = get_q('2007数二真题', '9')
q['tips']['gs'] = '无关组经线性变换后仍无关 $\\Leftrightarrow$ 组合系数矩阵的行列式 $\\ne0$。'

# ============ 10. 2007 题24 idea：去“正交补” ============
q = get_q('2007数二真题', '24')
q['idea'] = q['idea'].replace('多项式特征值 + 正交补 + 反求矩阵', '多项式特征值 + 利用实对称矩阵正交性求其余特征向量 + 反求矩阵')

# ============ 写回（紧凑单行） ============
with io.open('pwa/data/exam.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(exam, f, ensure_ascii=False, separators=(',', ':'))

# ============ 复检 ============
kw = ['雅可比', 'Jacobian', '向量空间', '过渡矩阵', '基变换', '正交补', '不变子空间', '\\ker', '\\operatorname{Im}', '\\dim N', '维数公式']
hits = 0
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam2 = json.load(f)
for p in exam2:
    for s in p['sections']:
        for qq in s['questions']:
            text = (qq.get('idea') or '') + '||' + (qq.get('answer') or '') + '||' + json.dumps(qq.get('tips', {}), ensure_ascii=False)
            found = [k for k in kw if k in text]
            if found:
                hits += 1
                print(f"{p['id']} 题{qq['no']}: {found}")
print(f"复检完成，剩余命中 {hits} 处")
