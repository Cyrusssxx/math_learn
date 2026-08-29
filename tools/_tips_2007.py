# -*- coding: utf-8 -*-
# 2007 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2007 = {
1: """【公式】等价无穷小分阶：$\\mathrm e^{x^{2}}-1\\sim x^{2}$（二阶）、$\\arcsin x\\sim x$（一阶）、幂指型 $(1+\\tan x)^{\\arcsin x}=\\mathrm e^{\\arcsin x\\ln(1+\\tan x)}$ 的指数 $\\sim x^{2}$。
【技巧】与 $\\sqrt{x}$ 等价 = 阶数为 $\\tfrac12$——四个候选先各算阶数再对号。
【易错】幂指型取对数后的阶数是乘积 $\\arcsin x\\cdot\\tan x\\sim x^{2}$，不是一阶。
【注意】答案 B。""",
2: """【技巧】不连续点 $x=0,1$：$x=0$ 处左右极限都存在但不相等（第一类）；$x=1$ 处 $\\mathrm e^{1/x}-\\mathrm e\\to0$ 使分母趋零、$f\\to\\infty$（第二类）。
【易错】$x=0$ 的左右：$\\mathrm e^{1/x}$ 两侧天壤之别，但 $\\tan x\\sim x$ 使两侧极限都有限且不等。
【注意】答案 A。""",
3: """【公式】变限积分奇偶性：$f$ 奇 → $F(x)=\\displaystyle\\int_0^x f$ 偶。
【技巧】半圆面积直接用几何公式：直径 1 → 半径 $\\tfrac12$ → 半圆面积 $\\dfrac{\\pi}{8}$；对称点函数值用奇偶搬移。
【易错】半圆面积是 $\\dfrac12\\pi r^{2}=\\dfrac{\\pi}{8}$，别把直径当半径。
【注意】答案 C。""",
4: """【公式】导数定义变形：$\\lim\\limits_{x\\to0}\\dfrac{f(x)-f(-x)}{2x}=f'(0)$（$f$ 连续时成立）；$\\lim\\limits_{x\\to0}\\dfrac{f(x^{2})-f(0)}{x^{2}}$ 只是右导数类信息。
【技巧】四命题逐个用定义验证：A、B、C 都能成立，只剩 D。
【易错】D 的漏洞：$\\lim\\dfrac{f(x^{2})-f(0)}{x^{2}}$ 存在推不出 $f'(0)$ 存在（缺左侧）。
【注意】答案 D（错误命题）。""",
5: """【公式】渐近线三查：垂直（$x=0$，$\\dfrac1x\\to\\infty$）、水平（$x\\to-\\infty$：$\\ln(1+\\mathrm e^{x})\\to0$、$\\dfrac1x\\to0$ → $y=0$）、斜（$x\\to+\\infty$：$\\ln(1+\\mathrm e^{x})\\approx x$）。
【技巧】$\\ln(1+\\mathrm e^{x})=x+\\ln(1+\\mathrm e^{-x})$ 恒等变形（$x\\to+\\infty$ 时尾项 →0）一步得斜渐近线 $y=x$。
【易错】两侧行为可以不同：$-\\infty$ 侧水平 $y=0$、$+\\infty$ 侧斜 $y=x$，各算各的。
【注意】共 3 条（答案 D）。""",
6: """【公式】$f''>0$ 双性质：拉格朗日给 $u_{n+1}-u_n=f'(\\xi_n)>0$（单调增）；下凸给弦比弧高 $f(n)>\\dfrac{f(n-1)+f(n+1)}{2}$ 型。
【技巧】选项逐条翻译：单调类用中值定理、加权比较类用凸性中点不等式。
【易错】$u_n<f(n+1)$ 类比较要用凸性中点不等式（$f(n)<\\dfrac{f(n-1)+f(n+1)}2$ 移项），不是单调性直接推。
【注意】答案 D。""",
7: """【公式】可微充分条件：某邻域内偏导存在且**连续** ⇒ 可微；偏导存在本身不充分。
【技巧】A、B 只给偏导存在（经典反例 $\\dfrac{xy}{x^{2}+y^{2}}$）；D 只给沿两坐标轴方向。
【注意】答案 C。""",
8: """【公式】交换次序先画域：$D:\\ \\dfrac\\pi2\\le x\\le\\pi,\\ \\sin x\\le y\\le1$；$y=\\sin x$ 在 $[\\tfrac\\pi2,\\pi]$ 递减。
【技巧】改先 $y$ 后 $x$：$y\\in[0,1]$，左边界反解 $x=\\pi-\\arcsin y$（第二象限解）、右边界 $x=\\pi$。
【易错】$\\sin x=y$ 在 $[\\tfrac\\pi2,\\pi]$ 的反解是 $\\pi-\\arcsin y$，直接写 $\\arcsin y$ 就错。
【注意】答案 B。""",
9: """【公式】无关组经线性变换 → 无关 $\\Leftrightarrow$ 过渡矩阵行列式 $\\ne0$。
【技巧】三个选项各算系数行列式（加减型常为 $\\pm1$、含"全加列"的常为 0）。
【易错】初等组合的行列式（$\\begin{vmatrix}1&0&1\\\\1&1&0\\\\0&1&1\\end{vmatrix}=2\\ne0$）口算即可。
【注意】答案 A。""",
10: """【公式】各行和为 0 的对称阵：$(1,1,1)^{\\mathrm T}$ 是 $\\lambda=0$ 的特征向量；实对称不同特征值的特征向量自动正交。
【技巧】另两个特征向量取与 $(1,1,1)$ 正交的 $(1,0,-1)^{\\mathrm T},(0,1,-1)^{\\mathrm T}$（同属 $\\lambda=1$），正交规范化拼 $P$。
【易错】$A\\alpha=0\\alpha$ = "特征值 0"的翻译钥匙；$\\lambda=1$ 的两个向量还要施密特正交化。
【注意】答案 B。""",
11: """【公式】$\\arctan x=x-\\dfrac{x^{3}}{3}+o(x^{3})$、$\\sin x=x-\\dfrac{x^{3}}{6}+o(x^{3})$——相减 $-\\dfrac{x^{3}}{6}$。
【技巧】减法型展开到相消阶（$x^{3}$）直接做差。
【易错】$\\arctan$ 的三次项系数是 $-\\tfrac13$ 不是 $-\\tfrac16$。
【注意】答案 $-\\dfrac16$。""",
12: """【公式】参数求导：$\\dot x=-\\sin t(1+2\\cos t)$、$\\dot y=\\cos t$，$t=\\tfrac\\pi4$ 代入得切线斜率 $-\\dfrac{1}{1+\\sqrt2}$。
【技巧】法线斜率 = 切线斜率负倒数 = $1+\\sqrt2$。
【易错】"法线"方程不是切线方程；$1+2\\cos t=1+\\sqrt2$ 的分母整理。
【注意】法线斜率 $1+\\sqrt2$。""",
13: """【公式】模型：$\\left(\\dfrac{1}{ax+b}\\right)^{(n)}=\\dfrac{(-1)^{n}a^{n}n!}{(ax+b)^{n+1}}$。
【技巧】从一阶 $-2(2x+3)^{-2}$、二阶 $8(2x+3)^{-3}$ 找规律（$2^{n}$、$3^{n+1}$、$(-1)^{n}$ 各归各位）。
【易错】$n$ 从 0 开始与从 1 开始的错位；负号交替。
【注意】$y^{(n)}(0)=\\dfrac{(-1)^{n}2^{n}n!}{3^{n+1}}$。""",
14: """【公式】特征根 1、3 → 齐次 $C_1\\mathrm e^{x}+C_2\\mathrm e^{3x}$；右端 $2\\mathrm e^{2x}$：$\\lambda=2$ 非特征根 → 特解 $A\\mathrm e^{2x}$，代回 $-A=2$。
【技巧】代回速算 $(2^{2}-4\\cdot2+3)A=-A=2$。
【易错】$A=-2$；$\\lambda=2$ 不是特征根（特征根是 1、3），不乘 $x$。
【注意】通解 $C_1\\mathrm e^{x}+C_2\\mathrm e^{3x}-2\\mathrm e^{2x}$。""",
15: """【公式】链式：$z_x=-\\dfrac{y}{x^{2}}f'_1+\\dfrac1y f'_2$，$z_y=\\dfrac1x f'_1-\\dfrac{x}{y^{2}}f'_2$。
【技巧】$x z_x-y z_y$ 代入后按 $f'_1,f'_2$ 归并：$f'_1$ 系数 $-\\tfrac yx-\\tfrac yx=-\\tfrac{2y}x$，$f'_2$ 系数 $\\tfrac xy+\\tfrac xy=\\tfrac{2x}y$。
【易错】$\\dfrac y{x^{2}}$、$\\dfrac x{y^{2}}$ 的求导符号与平方项。
【注意】答案 $2\\left(-\\dfrac{y}{x}f'_1+\\dfrac{x}{y}f'_2\\right)$。""",
16: """【公式】$A$ 为 4 阶移位幂零阵：$A^{2}$ 右上移一位、$A^{3}$ 再移、$A^{4}=E$ → $A^{-1}=A^{3}$。
【技巧】$A^{*}=|A|A^{-1}$（$|A|=1$）→ $A^{*}=A^{3}$；矩阵方程移项后右乘 $A$ 解 $B$。
【易错】$A^{2}$ 的非零带在右上第二超对角线；别把 $A^{4}=E$ 漏验。
【注意】$|B|=1$。""",
17: """【公式】变限积分含 $f^{-1}$：代换 $t=f(u)$（$\\mathrm dt=f'(u)\\,\\mathrm du$）→ $\\displaystyle\\int_0^{f(x)}f^{-1}(t)\\,\\mathrm dt=\\int_0^x u f'(u)\\,\\mathrm du$（条件代 $x=0$ 得 $f(0)=0$ 定限）。
【技巧】分部：$\\int_0^x u\\,\\mathrm df(u)=[uf(u)]_0^x-\\displaystyle\\int_0^x f(u)\\,\\mathrm du$，两边对 $x$ 求导解微分方程。
【易错】反解上下限时要说明 $f(0)=0$（把 $x=0$ 代入原积分式）。
【注意】解得 $f(x)=\\ln|\\sin x+\\cos x|$，在 $\\left[0,\\tfrac\\pi4\\right]$ 上即 $\\ln(\\sin x+\\cos x)$。""",
18: """【公式】旋成体体积：$V(a)=\\pi\\displaystyle\\int_0^{+\\infty}y^{2}\\,\\mathrm dx=\\pi\\int_0^{+\\infty}x\\,a^{x/a}\\,\\mathrm dx$；模型 $\\displaystyle\\int_0^{+\\infty}xq^{x}\\,\\mathrm dx=\\dfrac{1}{(\\ln q)^{2}}$（$0<q<1$）。
【技巧】换元 $q=a^{1/a}$：$V(a)=\\dfrac{\\pi a}{\\ln^{2}a}$；求导得驻点由 $\\ln a=1$ 给出，即 $a=\\mathrm e$。
【易错】$\\dfrac{\\mathrm dV}{\\mathrm da}=\\pi\\dfrac{\\ln a(\\ln a-2)}{\\ln^{4}a}$：分子是 $\\ln a(\\ln a-2)$，驻点别写成别的。
【注意】(II) $1<a<\\mathrm e$ 时 $V$ 递减、$a>\\mathrm e$ 递增，最小体积 $V(\\mathrm e)=\\pi\\mathrm e^{2}$。""",
19: """【公式】缺 $y$ 降阶 + 反解型：令 $p=y'$，$p'(x+p^{2})=p$ → 反解 $\\dfrac{\\mathrm dx}{\\mathrm dp}-\\dfrac{x}{p}=p$（一阶线性）。
【技巧】公式解 $x=p(p+C)$；初值 $p(1)=1$ ⇒ $C=0$、$p^{2}=x$，取 $p=\\sqrt{x}$ 积分，$y(1)=1$ 定 $C_1=\\tfrac13$。
【注意】特解 $y=\\dfrac23x^{3/2}+\\dfrac13$（已验证）。""",
20: """【公式】隐函数初值与逐层求导：$y-x\\mathrm e^{y-1}=1$ 代 $x=0$ 得 $y(0)=1$；一阶求导 $y'=\\dfrac{\\mathrm e^{y-1}}{1-x\\mathrm e^{y-1}}$，$y'(0)=1$（与 $f'(0)=1$ 一致）。
【技巧】(2) 继续隐式求二阶导，在 $(0,1)$ 处代值（$\\mathrm e^{y-1}=1$）逐层结算。
【易错】$x=0$ 时 $\\mathrm e^{y-1}=1$（不是 $\\mathrm e$）；每层求导都含 $y'$、$y''$ 链式项。
【注意】二阶结果为 1。""",
21: """【公式】双最大值 + 端点等值：$f(a)=g(a)$、$f(b)=g(b)$、$f,g$ 在 $(a,b)$ 内各有最大值且相等 → 构造 $\\varphi=f-g$：两端为零、内部两零点。
【技巧】设 $f$ 最大点 $x_1$、$g$ 最大点 $x_2$：$\\varphi(x_1)\\ge0$、$\\varphi(x_2)\\le0$，零点定理夹出 $\\varphi$ 的内零点 → 罗尔 → $\\varphi'$ 零点 → 再罗尔 → $\\varphi''=f''-g''$ 零点。
【易错】$\\varphi(x_1)$、$\\varphi(x_2)$ 的符号（各自在对方的最大点处取不到自己的最大值）；两零点可能重合时的退化情形要排除。
【注意】结论 $f''(\\xi)=g''(\\xi)$ 即 $\\varphi''(\\xi)=0$。""",
22: """【公式】绝对值分区：$|x|+|y|\\le1$（正方形内 $f=x^{2}$）与 $1<|x|+|y|\\le2$（环带 $f=\\dfrac{1}{\\sqrt{x^{2}+y^{2}}}$）。
【技巧】环带用对称性 4 倍化简后逐块算；正方形内 $\\displaystyle\\iint x^{2}\\,\\mathrm d\\sigma=\\dfrac13$（对 $x$ 积分按 $|y|\\le1-|x|$）。
【易错】菱形边界的四条线（$x\\pm y=\\pm1$）；对称性提 4 倍前先确认被积函数的对称性。
【注意】合计 $\\dfrac13+2\\sqrt2\\ln(3+2\\sqrt2)$。""",
23: """【公式】公共解 = 联立方程组的解；或"①的通解代入②"。
【技巧】① 的通解 $\\mu(0,1,-1)^{\\mathrm T}$ 代入 ② 得 $2\\mu-\\mu=1$ → $\\mu=1$ → $a=2$ 时公共解 $(0,1,-1)^{\\mathrm T}$。
【易错】$a\\ne2$ 时联立只有零解（零向量不算"非零公共解"）；自由变量选 $x_2$。
【注意】公共非零解 $\\Leftrightarrow a=2$。""",
24: """【公式】$A\\alpha_1=\\alpha_1$ → $A^{k}\\alpha_1=\\alpha_1$；实对称 → 不同特征值的特征向量自动正交。
【技巧】由 $\\alpha_1=(1,-1,1)^{\\mathrm T}$（$\\lambda=1$）构造与它正交的 $\\lambda=2,-2$ 特征向量（解两个正交条件方程），正交规范化拼 $Q$。
【易错】$A^{k}\\alpha_1=\\lambda_1^{k}\\alpha_1=\\alpha_1$（$1^{k}=1$）；正交条件的方程组求解。
【注意】(II) $A=\\begin{pmatrix}0&1&-1\\\\1&0&1\\\\-1&1&0\\end{pmatrix}$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2007数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2007数二真题.md', TIPS_2007)
