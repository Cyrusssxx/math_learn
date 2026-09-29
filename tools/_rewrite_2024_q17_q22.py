# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

p24 = next(p for p in exam if p['id'] == '2024数二真题')

# ============ 题 17：考纲内解法（对称性 + 直角坐标） ============
q17 = next(q for s in p24['sections'] for q in s['questions'] if str(q['no']) == '17')

q17['idea'] = (
    '**思路**：先审题——四条边界全是 $xy=c$ 型双曲线与 $y=kx$ 型过原点直线，每条边界方程在 $x,y$ 互换后不变'
    '（$y=3x$ 与 $y=\\frac x3$ 互为反函数），故 $D$ 关于直线 $y=x$ 对称。'
    '① 对称性消项：在对称区域上 $x$ 与 $y$ 地位对等，$\\iint_D x\\,d\\sigma=\\iint_D y\\,d\\sigma$，'
    '故 $\\iint_D(x-y)\\,d\\sigma=0$——被积函数中的 $x-y$ 项不用算！'
    '② 于是 $I=\\iint_D 1\\,d\\sigma=S_D$（面积），全程只用考纲内的直角坐标方法。'
    '③ 算面积：四个交点以 $x=1$ 为界分两段（先 $y$ 后 $x$），分别对 $\\left(3x-\\frac1{3x}\\right)$ 与 $\\left(\\frac3x-\\frac x3\\right)$ 积分，'
    '对数项合并恰好得 $\\frac83\\ln3$。'
)

q17['answer'] = (
    '【答案】$\\dfrac83\\ln 3$。\n'
    '**第一步：利用对称性，消去 $x-y$ 项（本题关键观察）。**\n'
    '区域 $D$ 的四条边界：双曲线 $xy=\\dfrac13$、$xy=3$ 的方程在 $x,y$ 互换后不变；直线 $y=3x$ 与 $y=\\dfrac x3$ 互为反函数，'
    '其图像关于直线 $y=x$ 对称。故区域 $D$ 关于直线 $y=x$ 对称：若 $(x,y)\\in D$，则 $(y,x)\\in D$。\n'
    '于是在对称区域上 $x$ 与 $y$ 的地位完全对等：\n'
    '$$\\iint_D x\\,d\\sigma=\\iint_D y\\,d\\sigma\\quad\\Longrightarrow\\quad \\iint_D(x-y)\\,d\\sigma=0.$$\n'
    '（等价说法：令 $\\sigma$ 为关于 $y=x$ 的反射变换，则 $\\sigma(D)=D$，而 $x-y$ 在 $\\sigma$ 下变号，故其积分为零。）\n'
    '因此\n'
    '$$I=\\iint_D(1+x-y)\\,d\\sigma=\\iint_D 1\\,d\\sigma=S_D.$$\n'
    '**第二步：直角坐标计算面积 $S_D$（分块定限）。**\n'
    '四条边界两两相交，交点分别为：\n'
    '$y=3x$ 与 $xy=\\dfrac13$ 交于 $\\left(\\dfrac13,1\\right)$；$y=3x$ 与 $xy=3$ 交于 $(1,3)$；\n'
    '$y=\\dfrac x3$ 与 $xy=\\dfrac13$ 交于 $\\left(1,\\dfrac13\\right)$；$y=\\dfrac x3$ 与 $xy=3$ 交于 $(3,1)$。\n'
    '以 $x=1$ 为界把 $D$ 分成左右两块：\n'
    '- 当 $\\dfrac13\\le x\\le1$ 时，$y$ 从下边界双曲线 $y=\\dfrac{1}{3x}$ 积到上边界直线 $y=3x$；\n'
    '- 当 $1\\le x\\le3$ 时，$y$ 从下边界直线 $y=\\dfrac x3$ 积到上边界双曲线 $y=\\dfrac3x$。\n'
    '故\n'
    '$$S_D=\\int_{1/3}^{1}\\left(3x-\\frac{1}{3x}\\right)dx+\\int_{1}^{3}\\left(\\frac{3}{x}-\\frac{x}{3}\\right)dx.$$\n'
    '分别计算：\n'
    '$$\\int_{1/3}^{1}\\left(3x-\\frac{1}{3x}\\right)dx=\\left[\\frac{3x^2}{2}-\\frac{\\ln x}{3}\\right]_{1/3}^{1}'
    '=\\frac32-\\frac16-\\frac{\\ln 3}{3}=\\frac43-\\frac{\\ln 3}{3},$$\n'
    '$$\\int_{1}^{3}\\left(\\frac{3}{x}-\\frac{x}{3}\\right)dx=\\left[3\\ln x-\\frac{x^2}{6}\\right]_{1}^{3}'
    '=3\\ln 3-\\frac96+\\frac16=3\\ln 3-\\frac43.$$\n'
    '相加，常数项 $\\dfrac43-\\dfrac43$ 恰好抵消，得\n'
    '$$S_D=3\\ln 3-\\frac{\\ln 3}{3}=\\dfrac{8\\ln 3}{3}.$$\n'
    '**结论**：$I=\\iint_D(1+x-y)\\,dx\\,dy=S_D=\\dfrac{8\\ln 3}{3}$。'
)

q17['tips'] = {
    'gs': '边界 $xy=c$ 与 $y=kx$ 均关于 $y=x$ 对称（$y=3x$ 与 $y=\\frac x3$ 互为反函数）⟹ $D$ 对称 ⟹ $\\iint_D(x-y)d\\sigma=0$，只剩面积。',
    'jq': '交点 $\\left(\\frac13,1\\right),(1,3),\\left(1,\\frac13\\right),(3,1)$；以 $x=1$ 分两段：$\\left[\\frac13,1\\right]$ 上 $y:\\frac1{3x}\\to3x$，$[1,3]$ 上 $y:\\frac x3\\to\\frac3x$。',
    'yc': '对称性消项是省时关键：若直接硬算 $\\iint_D x\\,d\\sigma$ 与 $\\iint_D y\\,d\\sigma$ 会做大量无用功；面积分两段时下/上边界要按 $x$ 与 $1$ 的大小关系切换。',
    'zy': '答案 $\\frac83\\ln3$。'
}

# ============ 题 22：去向量空间术语，改为秩与基础解系的审题推理链 ============
q22 = next(q for s in p24['sections'] for q in s['questions'] if str(q['no']) == '22')

q22['idea'] = (
    '**思路**：把两个文字条件逐句“翻译”成秩的信息，参数自然解出。'
    '① “$Ax=0$ 的解都是 $B^Tx=0$ 的解”：把 $Ax=0$ 的通解代进 $B^Tx=0$ 应当恒成立；'
    '② “但两个方程组不同解”：$B^Tx=0$ 还有一批 $Ax=0$ 之外的解 ⟹ 后者的解更多；'
    '③ 数解的“多少”用秩：$n$ 元齐次方程组基础解系含 $n-r$ 个向量。$A$ 是 $2\\times3$ 且前两列无关 ⟹ $r(A)=2$（与 $a$ 无关），'
    '$Ax=0$ 的基础解系含 $3-2=1$ 个向量；于是 $B^Tx=0$ 的基础解系必须含多于 1 个向量 ⟹ $r(B^T)=r(B)<2$，即 $r(B)=1$；'
    '④ $r(B)=1$ ⟺ $B$ 的两列成比例：$(1,1,b)^T\\parallel(1,1,2)^T$ ⟹ $b=2$；'
    '⑤ 求 $a$：把 $Ax=0$ 的那个非零解具体解出来，代进 $B^Tx=0$ 即可；'
    '⑥ (2) 问算 $BA$ 时发现每行成比例、矩阵对称，可写成一个列向量乘自身的转置 $ww^T$，'
    '二次型即 $f=(w^Tx)^2$；秩 1 对称矩阵的特征值就是“迹”与一串 $0$，正交单位化即得 $Q$。'
)

q22['answer'] = (
    '【答案】（1）$a=1,\\ b=2$；（2）标准形为 $6y_1^2$，其中\n'
    '$$Q=\\begin{pmatrix}\\frac1{\\sqrt6}&\\frac1{\\sqrt2}&\\frac1{\\sqrt3}\\\\[4pt]'
    '\\frac1{\\sqrt6}&-\\frac1{\\sqrt2}&\\frac1{\\sqrt3}\\\\[4pt]'
    '\\frac2{\\sqrt6}&0&-\\frac1{\\sqrt3}\\end{pmatrix}.$$\n'
    '**（1）第一步：由“解的多少”定 $r(B)=1$，从而 $b=2$。**\n'
    '$A=\\begin{pmatrix}0&1&a\\\\1&0&1\\end{pmatrix}$ 的前两列 $\\begin{pmatrix}0\\\\1\\end{pmatrix},\\begin{pmatrix}1\\\\0\\end{pmatrix}$ 线性无关，'
    '故 $r(A)=2$（与 $a$ 无关），$Ax=0$ 的基础解系含 $3-2=1$ 个向量。\n'
    '“$Ax=0$ 的解都是 $B^Tx=0$ 的解，但两个方程组不同解”说明：$B^Tx=0$ 的解比 $Ax=0$ 的解多，'
    '即 $B^Tx=0$ 的基础解系所含向量个数 $3-r(B^T)>3-r(A)=1$，故 $r(B^T)=r(B)<2$，即 $r(B)=1$。\n'
    '$B$ 的两列为 $(1,1,b)^T$ 与 $(1,1,2)^T$，两列成比例当且仅当 $b=2$（此时 $r(B)=1$）。故 $b=2$。\n'
    '**第二步：把 $Ax=0$ 的解代入 $B^Tx=0$，求 $a$。**\n'
    '解 $Ax=0$：$\\begin{cases}x_2+ax_3=0\\\\x_1+x_3=0\\end{cases}$，取 $x_3=1$ 得基础解系 $\\xi=(-1,-a,1)^T$。\n'
    '由“$Ax=0$ 的解都是 $B^Tx=0$ 的解”，$\\xi$ 必须满足 $B^T\\xi=0$。$b=2$ 时\n'
    '$$B^T=\\begin{pmatrix}1&1&2\\\\1&1&2\\end{pmatrix},\\qquad B^T\\xi=0\\iff \\xi_1+\\xi_2+2\\xi_3=0,$$\n'
    '代入 $\\xi=(-1,-a,1)^T$：$-1-a+2=0$，解得 $a=1$。\n'
    '检验“不同解”：$r(B^T)=r(B)=1$，$B^Tx=0$ 的基础解系含 $3-1=2$ 个向量，确有 $B^Tx=0$ 的解不是 $Ax=0$ 的解，条件吻合。\n'
    '所以 $a=1,\\ b=2$。\n'
    '**（2）第一步：写出二次型矩阵并观察结构。**\n'
    '代入 $a=1,\\ b=2$：\n'
    '$$BA=\\begin{pmatrix}1&1\\\\1&1\\\\2&2\\end{pmatrix}\\begin{pmatrix}0&1&1\\\\1&0&1\\end{pmatrix}'
    '=\\begin{pmatrix}1&1&2\\\\1&1&2\\\\2&2&4\\end{pmatrix}.$$\n'
    '它本身是对称矩阵，故 $f=x^TBAx$ 的矩阵就是 $M=BA$。注意到三行成比例：\n'
    '$$M=\\begin{pmatrix}1\\\\1\\\\2\\end{pmatrix}(1,1,2)=ww^T,\\qquad w=(1,1,2)^T,$$\n'
    '为秩 $1$ 对称矩阵，于是\n'
    '$$f=x^Tww^Tx=(w^Tx)^2=(x_1+x_2+2x_3)^2.$$\n'
    '**第二步：求特征值与正交单位特征向量。**\n'
    '秩 1 对称矩阵的特征值：一个非零特征值等于迹，其余为 $0$，即\n'
    '$$\\lambda_1=\\operatorname{tr}(M)=1+1+4=6,\\qquad \\lambda_2=\\lambda_3=0.$$\n'
    '- $\\lambda_1=6$：由 $M=ww^T$ 知 $Mw=ww^Tw=\\|w\\|^2w=6w$，即 $w$ 就是属于 $6$ 的特征向量，'
    '单位化 $\\eta_1=\\dfrac{1}{\\sqrt6}(1,1,2)^T$；\n'
    '- $\\lambda_2=\\lambda_3=0$：解 $Mx=0$，等价于 $x_1+x_2+2x_3=0$，取两个正交的单位解\n'
    '  $$\\eta_2=\\dfrac{1}{\\sqrt2}(1,-1,0)^T,\\qquad \\eta_3=\\dfrac{1}{\\sqrt3}(1,1,-1)^T$$\n'
    '  （$\\eta_3$ 是把 $(1,1,-1)^T$ 与 $\\eta_2$ 正交化后的结果，且满足 $1+1-2=0$）。\n'
    '**第三步：写出正交变换与标准形。**\n'
    '令 $Q=(\\eta_1,\\eta_2,\\eta_3)$，则 $Q$ 为正交矩阵，且\n'
    '$$Q^TMQ=\\operatorname{diag}(6,0,0).$$\n'
    '故正交变换 $x=Qy$ 下\n'
    '$$f=6y_1^2.$$\n'
    '**复盘（从题目能判断出什么）**：见到“一个方程组的解全是另一个方程组的解”就往“把前者的通解代入后者”与“秩的大小关系”两条路走；'
    '见到 $f=x^TBAx$ 且 $BA$ 恰为对称的秩 1 矩阵，立刻按 $ww^T$ 拆开，标准形与特征向量一步到位。'
)

q22['tips'] = {
    'gs': '审题翻译：解集包含+不同解 ⟹ 解的个数不同 ⟹ $3-r(B)>3-r(A)=1$ ⟹ $r(B)=1$ ⟹ 两列成比例 $b=2$；再把 $Ax=0$ 的解 $\\xi=(-1,-a,1)^T$ 代入 $B^Tx=0$ 得 $a=1$。',
    'jq': '$BA=\\begin{pmatrix}1&1&2\\\\1&1&2\\\\2&2&4\\end{pmatrix}=ww^T,\\ w=(1,1,2)^T$，秩 1 对称：特征值 $=\\operatorname{tr}=6$ 与 $0,0$；$\\lambda=6$ 的特征向量就是 $w$ 本身。',
    'yc': '不能用“$B^T$ 的行可由 $A$ 的行表示”之外跳步；“不同解”保证 $r(B)=1$ 而非 $2$。$\\eta_2,\\eta_3$ 必须正交：先取 $(1,-1,0)^T$，再用与两向量都正交的 $(1,1,-1)^T$。',
    'zy': '答案（1）$a=1,b=2$；（2）标准形 $6y_1^2$。'
}

# ============ 紧凑单行写回 ============
with io.open('pwa/data/exam.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(exam, f, ensure_ascii=False, separators=(',', ':'))

# 验证写回后仍可解析
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    check = json.load(f)
q17c = next(q for p in check if p['id'] == '2024数二真题' for s in p['sections'] for q in s['questions'] if str(q['no']) == '17')
q22c = next(q for p in check if p['id'] == '2024数二真题' for s in p['sections'] for q in s['questions'] if str(q['no']) == '22')
assert '雅可比' not in q17c['idea'] and '雅可比' not in q17c['answer'] and '雅可比' not in str(q17c['tips'])
assert 'ker' not in q22c['idea'] and 'ker' not in q22c['answer'] and 'ker' not in str(q22c['tips'])
print('题 17 与题 22 解析重写完成，写回并校验通过（idea/answer/tips 均无雅可比/ker 术语）')
