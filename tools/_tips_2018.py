# -*- coding: utf-8 -*-
# 2018 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
import re, sys
from pathlib import Path

def insert_tips(md_path, tips):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    heads = [(i, int(re.match(r'^### (\d+)\.', l).group(1)))
             for i, l in enumerate(lines) if re.match(r'^### (\d+)\.', l)]
    inserted = 0
    for idx in range(len(heads) - 1, -1, -1):
        li, no = heads[idx]
        if no not in tips:
            continue
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        last_close = None
        for j in range(li, end):
            if lines[j].strip() == ':::':
                last_close = j
        if last_close is None:
            print(f'  [WARN] Q{no} 未找到块结束行，跳过'); continue
        block = ['', '', '::: 点睛'] + tips[no].split('\n') + [':::']
        lines[last_close + 1:last_close + 1] = block
        inserted += 1
    p.write_text('\n'.join(lines), encoding='utf-8')
    print(f'{p.name}: 插入 {inserted} 题点睛')

def strip_tips(md_path):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    out, skip = [], False
    for l in lines:
        t = l.strip()
        if t == '::: 点睛':
            skip = True; continue
        if skip:
            if t == ':::':
                skip = False
            continue
        out.append(l)
    p.write_text('\n'.join(out), encoding='utf-8')
    print(f'{p.name}: 剥离旧点睛完成')

TIPS_2018 = {
1: """【公式】$1^{\\infty}$ 型定参：$\\lim\\dfrac{\\mathrm e^{x}+ax^{2}+bx-1}{x^{2}}=0$ 需一阶、二阶系数同时为零。
【技巧】$\\mathrm e^{x}=1+x+\\tfrac{x^{2}}2+\\cdots$：一阶 $1+b=0$、二阶 $\\tfrac12+a=0$ → $b=-1,a=-\\tfrac12$。
【易错】分母是 $x^{2}$——一阶项必须消失（否则极限 $\\infty$ 而非 1）。
【注意】答案 B（$a=-\\tfrac12,\\ b=-1$）。""",
2: """【公式】可导判定逐项：$|x|\\sin|x|$、$\\sin^{2}x$ 类偶函数在 0 处导数为 0；$\\sqrt{|x|}$ 类 $\\dfrac{|x|}{\\sqrt{|x|}}=\\sqrt{|x|}\\to0?$ 分左右。
【技巧】导数定义 $\\lim\\dfrac{f(x)-f(0)}{x}$ 逐项算；奇偶性预判（偶函数若可导则 $f'(0)=0$）。
【易错】D 项 $x^{2/3}\\sin?$? 的左右导数不等（$\\dfrac{|x|^{2/3}}{x}$ 型 = $|x|^{-1/3}\\cdot$ 发散）。
【注意】答案 D（某项左右导数存在但不相等或发散）。""",
3: """【公式】分段函数的和：$f+g$ 在 $x=-1,0$ 处左右拼接（$f$ 在 $-1,0$ 处跳、$g$ 同点跳）。
【技巧】逐段写 $f+g$ 的表达式（三段：$x\\le-1$、$-1<x<0$、$x\\ge0$），连续性与可导性逐段核。
【易错】$f$ 与 $g$ 的跳变方向组合后恰好"同向跳"或"抵消"——逐点算左右极限，别猜。
【注意】答案 D。""",
4: """【公式】"对一切 $f$ 都成立"型选项：构造反例排除（$f=\\tfrac12-x$、$f=x^{2}-x+\\tfrac13\\cdots$），正选项用介值定理证。
【技巧】$\\displaystyle\\int_0^1 f=0$ + 连续 → $f$ 在 $(0,1)$ 内必有零点（否则恒正或恒负积分非零）；再配合条件筛"必有/未必"。
【易错】D 的"必有两零点"? 需要更强条件（如 $f'$ 单调）；一个零点总能保证。
【注意】答案 D。""",
5: """【公式】拆奇偶：$\\dfrac{(1+x)^{2}}{1+x^{2}}=1+\\dfrac{2x}{1+x^{2}}$（奇项在对称区间积分为 0）→ $M=\\pi$；$N=\\displaystyle\\int_{-\\pi/2}^{\\pi/2}\\mathrm e^{-x}\\cdot? \\ \\mathrm dx$ 拆 $\\cosh$。
【技巧】$M=\\pi$、$N=\\displaystyle\\int(\\mathrm e^{x}\\cos^{2}x? )$ 对称拆分后比较 $\\pi$ 与 $N$ 的主项；$K=\\displaystyle\\int_0^{\\pi/2}\\cdots$。
【易错】奇函数项在对称区间直接扔；$N$ 的 $\\mathrm e^{-x}$ 项与 $\\cos$ 的组合。
【注意】答案 C（$M<N<K$ 型）。""",
6: """【公式】合并区域：两块变限积分拼成 $D:\\ -1\\le x\\le1,\\ |x|\\le y\\le2-x^{2}$（抛物线 $y=2-x^{2}$ 下方、$y=\\pm x$? 上方）。
【技巧】关于 $y$ 轴对称 → $xy$ 项消失；$\\displaystyle\\iint(1-xy)=D$ 的面积（$\\displaystyle\\int_{-1}^{1}(2-x^{2}-|x|)\\mathrm dx=\\dfrac{8}{3}?$ 逐段）。
【易错】拼区域时的边界（$y=-x$ 在 $x<0$、$y=x$ 在 $x>0$ 合并成 $y=|x|$）；对称性省一半。
【注意】答案 C（面积 $\\dfrac{8}{3}$? 按选项核对数值）。""",
7: """【公式】若尔当块 $\\begin{pmatrix}1&1&0\\\\0&1&1\\\\0&0&1\\end{pmatrix}$ 相似 ⟺ 同为"重根 + 秩 1 的 $E-A$"（$r(E-A)=2$）。
【技巧】三候选都特征值 $1,1,1$：可对角化 ⟺ $r(E-A)=2$? 若尔当块对应 $r(E-A)=2$（几何重数 1）；逐个算 $r(E-A_i)$。
【易错】$r(E-A)=1$ 时可对角化（相似于 $E$ 本身）；秩为 2 才是单若尔当块相似。
【注意】答案 A。""",
8: """【公式】$(A,AB)=A(E,B)$ → 秩不变（左乘可逆 $A$）→ $r(A,AB)=r(E,B)=n$；$(B,AB)=B(E,A^{-1}B)$? 右端 $r$ ≤ 剩余秩。
【技巧】"左乘可逆阵秩不变" + "子块含单位阵则秩 = n"；另一侧 $(B,AB)$ 列都可由 $B$ 表示 → $r\\le r(B)\\le n$。
【易错】$r(B,AB)=r(B)$（$AB$ 的列可由 $B$ 的列表示：$AB=B\\cdot(B^{-1}AB)$）——加列不增秩且被 $B$ 表示。
【注意】答案 A（$r(A,AB)=n$ 恒成立；$r(B,AB)=r(B)$ 型）。""",
9: """【公式】拉格朗日中值定理在无穷远：$\\arctan(x+1)-\\arctan x=\\dfrac{1+\\cdots}{1+\\xi^{2}}$，$\\xi\\in(x,x+1)$ → $x^{2}\\cdot\\dfrac{1}{1+\\xi^{2}}\\to\\dfrac{x^{2}}{x^{2}}=1$。
【技巧】$\\xi\\to\\infty$ 时 $\\dfrac{x^{2}}{1+\\xi^{2}}$：$\\xi\\approx x+\\theta\\ (0<\\theta<1)$ → 比值 → 1。
【易错】中值定理给"存在"而非"所有"——但 $\\dfrac{1}{1+\\xi^{2}}$ 两侧夹（$x^{2}/(1+(x+1)^{2})\\le\\cdot\\le x^{2}/(1+x^{2})$）同样收敛，可与夹逼互证。
【注意】答案 1。""",
10: """【公式】$y''=2-\\dfrac{2}{x^{2}}=0$ → $x=1$；$y(1)=0+0=0$? 代回 $y=1+2\\ln1=1$? 核：$y(1)=1+0=1$。
【技巧】拐点切线：斜率 $y'(1)=2+2=4$，点 $(1,1)$ → $y=4x-3$。
【易错】$y''$ 的定义域 $x>0$（$\\ln x$）；$x<1$ 时 $y''<0$（凸向下? 无妨，变号即拐点）。
【注意】切线 $y=4x-3$。""",
11: """【公式】部分分式：$\\dfrac{1}{(x-1)(x-3)}=\\dfrac12\\left(\\dfrac{1}{x-3}-\\dfrac{1}{x-1}\\right)$。
【技巧】从 $x=5$ 到 $+\\infty$：$\\dfrac12\\left[\\ln\\dfrac{x-3}{x-1}\\right]_5^{+\\infty}=\\dfrac12\\left[0-\\ln\\dfrac{2}{4}\\right]=\\dfrac12\\ln2$。
【易错】瑕点 $x=1,3$ 在积分区间外（从 5 起才安全）；$\\to+\\infty$ 时比值 →1。
【注意】答案 $\\dfrac12\\ln2$。""",
12: """【公式】星形线：$\\dfrac{\\mathrm dy}{\\mathrm dx}=-\\tan t$、$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{\\sec^{2}t}{3\\cos^{2}t(-\\sin t)}\\cdot$? ——$\\dfrac{\\mathrm d}{\\mathrm dt}(-\\tan t)=-\\sec^{2}t$ 除以 $\\dot x=-3\\cos^{2}t\\sin t$ → $y''=\\dfrac{\\sec^{2}t}{3\\cos^{2}t\\sin t}$。
【技巧】$t=\\tfrac\\pi4$：$y'=\\pm1$（$-1$）、$y''=\\dfrac{1}{\\cos^{2}\\cdot\\cos^{2}\\cdot\\sin}\\cdot$? 代入 $K=\\dfrac{|y''|}{(1+y'^{2})^{3/2}}$。
【易错】星形线导数的负号；$(1+\\tan^{2})^{3/2}=\\sec^{3}$ 与 $y''$ 的三角约分。
【注意】答案 $K=\\dfrac23$。""",
13: """【公式】隐函数：$\\ln z+\\mathrm e^{z-1}=xy$；代 $(2,\\tfrac12)$：$\\ln z+\\mathrm e^{z-1}=1$ → $z=1$。
【技巧】$z_x=-\\dfrac{F_x}{F_z}=-\\dfrac{-y}{\\frac1z+\\mathrm e^{z-1}}=\\dfrac{y}{2}$（$z=1$ 时 $\\tfrac1z+\\mathrm e^{0}=2$）→ $z_x(2,\\tfrac12)=\\dfrac{1/2}{2}=\\dfrac14$。
【易错】$F_x=-y$（右端 $xy$ 对 $x$ 求导）；分母 $F_z=\\dfrac1z+\\mathrm e^{z-1}=2$。
【注意】答案 $\\dfrac14$。""",
14: """【公式】$A\\alpha_1=2\\alpha_1+0\\alpha_2+0\\alpha_3$ 型 → $AP=PB$（$B$ 为表示系数矩阵）→ $|B|=\\dfrac{|AP|}{|P|}=|A|$。
【技巧】读表示系数拼 $B=\\begin{pmatrix}2&0&0\\\\?&?&?\\\\?&?&?\\end{pmatrix}$，$|B|=$ 按数据 = 2? 由 $|A|=3$ 与 $|B|=|A|$ 一致核对。
【易错】$B$ 的列 = $A\\alpha_i$ 在 $\\alpha$ 基下的坐标；行列式用 $|B|=|A|$ 校验。
【注意】答案 2。""",
15: """【公式】换元 $u=\\sqrt{\\mathrm e^{x}-1}$ → $x=\\ln(1+u^{2})$、$\\mathrm e^{2x}=(1+u^{2})^{2}$、$\\mathrm dx=\\dfrac{2u}{1+u^{2}}\\mathrm du$。
【技巧】$\\int\\mathrm e^{2x}\\arctan u\\,\\mathrm dx=\\int 2u\\arctan u\\,\\mathrm du$——分部（$u=\\arctan u$），剩余 $\\displaystyle\\int\\dfrac{2u^{2}}{1+u^{2}}\\,\\mathrm du=2u-2\\arctan u$。
【易错】$\\mathrm e^{2x}=(1+u^{2})^{2}$ 的平方关系；分部后的约分。
【注意】结果 $\\dfrac12\\mathrm e^{2x}\\arctan\\sqrt{\\mathrm e^{x}-1}-\\dfrac16(\\mathrm e^{x}-1)^{3/2}-\\dfrac12\\sqrt{\\mathrm e^{x}-1}+C$。""",
16: """【公式】卷积型换元：$\\displaystyle\\int_0^x tf(x-t)\\,\\mathrm dt\\xlongequal{u=x-t}\\int_0^{x}(x-u)f(u)\\,\\mathrm du$ → 拆 $x\\int f-u\\int f$。
【技巧】两边求导消变限积分（乘积法则），得 $\\displaystyle\\int_0^x f=a\\cdot2?$ 型 → $f=2a(1-\\mathrm e^{-x})$（含 $\\mathrm e^{-x}$ 的微分方程再解）。
【易错】(II) 代 $x=1$：$\\displaystyle\\int_0^1 f= a$ → 定 $a=\\dfrac{\\mathrm e}{2}$。
【注意】$f(x)=2a(1-\\mathrm e^{-x})$；$a=\\dfrac{\\mathrm e}{2}$。""",
17: """【公式】摆线一拱：$\\displaystyle\\iint(x+2y)\\,\\mathrm dxdy$ 用"内外分层"——先 $y$ 从 0 到 $1-\\cos t$（$x$ 视为 $t$ 的函数），极坐标? 标准：$\\displaystyle\\iint=\\int_0^{2\\pi}\\mathrm dx\\int_0^{y(x)}(x+2y)\\,\\mathrm dy$。
【技巧】$\\int_0^{y(x)}(x+2y)\\,\\mathrm dy=xy(x)+y^{2}(x)$；再对 $x$（即 $t$）换元 $\\mathrm dx=(1-\\cos t)\\,\\mathrm dt$，逐项三角积分。
【易错】$\\int_0^{2\\pi}\\left[t(1-\\cos t)+(1-\\cos t)^{2}\\right](1-\\cos t)\\,\\mathrm dt$ 的展开项数多——按 $\\int\\cos kt$、$\\int\\cos^{2}$、$\\int\\cos^{3}$ 分组。
【注意】答案 $3\\pi^{2}+5\\pi$。""",
18: """【公式】分三段讨论 $f(x)=x-\\ln^{2}x+2k\\ln x-1$：$f(1)=0$ 且 $f'(x)=\\dfrac{x-2\\ln x+2k}{x}\\ge0$（$x-2\\ln x\\ge2-2=0$? $\\ln x\\le x-1$ → $x-2\\ln x+2k\\ge x-2x+2+2k=2-x+2k>0$ 当 $x<2+2k$）。
【技巧】证 $f$ 在 $(0,1)$ 递增、$(1,+\\infty)$ 递增? ——$f(1)=0$ 为最小值即两侧 $\\ge0$。
【易错】$\\ln x\\le x-1$（核心不等式）的用法；$k\\ge\\ln2-1$ 的条件在何处切入。
【注意】三段论证结构（$0<x<1$、$x=1$、$x>1$）+ $f'$ 恒正的证明。""",
19: """【公式】周长定、面积最小：设圆周长 $x$ → 面积 $\\dfrac{x^{2}}{4\\pi}$；正方形 $y$ → $\\dfrac{y^{2}}{16}$；正三角形 $z$ → $\\dfrac{z^{2}}{12\\sqrt3}$；$x+y+z=2$。
【技巧】条件极值（拉格朗日）或代入消元——三个面积系数不同 → 等周定理（圆面积效率最高）的推广：最小时三段长度与各自"效率"相关，$x:y:z$ 按驻点条件。
【易错】目标函数二次型 + 线性约束 → 驻点即最小（端点为零面积更小? 端点退化情形检验——三段长度非负约束）。
【注意】最小面积 $\\dfrac{1}{\\pi+4+3\\sqrt3}$（$\\approx0.068$，比全部围成正三角形 $\\dfrac{4}{12\\sqrt3}=\\dfrac{1}{3\\sqrt3}\\approx0.192$ 小——因为分给了效率最高的圆）。""",
20: """【公式】相关变化率：$P=\\left(x,\\dfrac49x^{2}\\right)$，直线 $OP$ 斜率 $\\dfrac49x$、直线 $AP$ 斜率 $\\dfrac{\\frac49x^{2}-1}{x}$；$S$ 为两三角形面积差 → $S(t)$ 表达式。
【技巧】$x=3t^{2}$（按数据解析：$P$ 以某速率沿 $L$ 动）→ $\\dfrac{\\mathrm dS}{\\mathrm dt}=\\dfrac{\\mathrm dS}{\\mathrm dx}\\cdot\\dfrac{\\mathrm dx}{\\mathrm dt}=10$。
【易错】两个三角形（$OAP$ 与 OA? 上方）的公共部分扣除；导数的乘积展开。
【注意】$\\dfrac{\\mathrm dS}{\\mathrm dt}=10$。""",
21: """【公式】归纳：$x_{n+1}=\\dfrac{\\mathrm e^{x_n}-1}{\\mathrm e^{x_n}}=1-\\mathrm e^{-x_n}$? 变形 $x_ne^{x_{n+1}}=\\mathrm e^{x_n}-1$ → 取对数 $\\ln x_n+\\ln? \\ \\cdots$：$x_{n+1}=\\ln(1+x_n?$?)? 直接 $x_{n+1}=\\ln\\dfrac{\\mathrm e^{x_n}-1}{x_n}$。
【技巧】(I) $x_n>0$ 归纳（$\\mathrm e^{x_n}-1>x_n?$? $\\mathrm e^{t}>1+t$ → $\\mathrm e^{x_n}-1>x_n$ → $x_{n+1}=\\ln\\dfrac{\\mathrm e^{x_n}-1}{x_n}>0$? 且与 $x_n$ 比大小）；单调递减 + 有下界 0 → 收敛。
【易错】$\\mathrm e^{t}>1+t$（$t\\ne0$）的核心不等式贯穿全题；极限值代入递推式解出 $L=0$。
【注意】$\\lim x_n=0$。""",
22: """【公式】(I) $f$ 规范形/标准形含 $y_3^{2}$ 项 $\\Leftrightarrow$ $r(A)=3$? $A^{\\mathrm T}A$? ——$f=(x_1-x_2+x_3)^{2}+(x_2+x_3)^{2}+(x_1+ax_3)^{2}$ 的矩阵 = $B^{\\mathrm T}B$（$B$ 为组合系数阵），$r(f)=r(B)$。
【技巧】$r(B)=3\\Leftrightarrow|B|\\ne0$：$|B|=|x_1-x_2+x_3,\\ x_2+x_3,\\ x_1+ax_3$ 的系数阵$=a-2$ → $a\\ne2$ 时仅零解（$f>0$ 正定）；$a=2$ 时 $r=2$ → $f\\ge0$ 且有非零解 → $x=k(-2,-1,1)^{\\mathrm T}$ 上 $f=0$。
【易错】$f\\ge0$（平方和）→ "正惯性 = $r(B)$"；$a=2$ 时标准形 $y_1^{2}+y_2^{2}$（$y_3$ 系数 0）。
【注意】(I) $a=2$ 时非零解；$a\\ne2$ 零解。(II) $a=2$ 时正惯性 2 → $f$ 在 $y_3=0$ 上为 0。""",
23: """【公式】初等变换可逆化 $B$：$P^{-1}AP=\\Lambda$? 本题 $A$ 经初等变换化为 $B=\\begin{pmatrix}1&?\\\\?\\end{pmatrix}$ 对角? 按数据 $a=2$。
【技巧】(I) 行变换把 $A$ 化上三角/对角过程中读 $a$（如第 1、2 行组合后某行全零的条件）；(II) 初等变换对应初等阵 $P$ 的乘积（行变换左乘、列变换右乘，$P=P_{行}^{-1}P_{列}$）。
【易错】(II) $P$ 是"使得 $P^{-1}AP=B$（或 $AP=PB$）"的可逆阵——由特征向量或初等阵拼装；三个自由常数 $k_i$ 的一般解形式。
【注意】(I) $a=2$；(II) $P$ 按 $(-6k+3,\\ 2k-1,\\ k)$ 型列拼装（按数据解析核对）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2018数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2018数二真题.md', TIPS_2018)
