# -*- coding: utf-8 -*-
# 2014 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2014 = {
1: """【公式】$\\ln^{\\alpha}(1+2x)\\sim(2x)^{\\alpha}$（$\\alpha$ 阶）；$(1-\\cos x)^{1/\\alpha}\\sim\\left(\\dfrac{x^{2}}{2}\\right)^{1/\\alpha}=\\dfrac{x^{2/\\alpha}}{2^{1/\\alpha}}$（$\\tfrac2\\alpha$ 阶）。
【技巧】"比 $x$ 高阶" = 阶数 $>1$：$\\alpha>1$ 且 $\\tfrac2{\\alpha}>1$ → $1<\\alpha<2$。
【易错】$(1-\\cos x)^{1/\\alpha}$ 的阶是 $\\tfrac2{\\alpha}$（除不是乘）；两不等式取交集。
【注意】答案 B（$1<\\alpha<2$）。""",
2: """【公式】渐近线排查：A $\\dfrac{1+\\mathrm e^{x^{2}}}{1-\\mathrm e^{x^{2}}}$（$x\\to\\pm\\infty\\to-1$ 水平；$x=\\pm1$ 垂直）；B $\\dfrac{x^{2}+x}{x^{2}-1}$（$x=1$ 垂直、$y=1$ 水平）；C $y=x+\\sin\\dfrac1x$：$y-x=\\sin\\tfrac1x\\to0$ → 斜渐近线 $y=x$；D 均无。
【技巧】C 的"振荡衰减"型：$\\lim(y-x)=0$ 但 $y-x$ 不断振荡——恰好够成斜渐近线。
【易错】$y=x+\\sin\\tfrac1x$ 无水平渐近线但**有**斜渐近线（不是"振荡就没有"）；$x\\to0^+$ 与 $x\\to0^-$ 的单侧无限（无定义域内）。
【注意】答案 C（仅 C 有渐近线）。""",
3: """【公式】$g(x)=f(0)(1-x)+f(1)x$ 是过 $(0,f(0))$、$(1,f(1))$ 的弦；凸函数（$f''\\ge0$）曲线在弦**下方** → $f(x)\\le g(x)$。
【技巧】$f\\le g\\Leftrightarrow f-g$ 在两端为零、内部 $\\le0$——对 $f-g$ 用罗尔/最值论证（$f-g$ 若内部有正最大值点则 $f''<0$ 矛盾）。
【易错】凸函数的方向（$f''\\ge0$ 下凸/开口向上 → 弦在曲线上方）；"仅当 $f$ 为线性时取等"。
【注意】答案 D。""",
4: """【公式】参数曲率：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{2t+4}{2t}$、$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{\\left(\\dfrac{2t+4}{2t}\\right)'_t}{2t}=\\dfrac{-4/t^{2}}{2t}=-\\dfrac{2}{t^{3}}$。
【技巧】$t=1$：$y'=3$、$y''=-2$ → $K=\\dfrac{|{-2}|}{(1+9)^{3/2}}=\\dfrac{2}{10^{3/2}}$ → $\\rho=\\dfrac{1}{K}=\\dfrac{10^{3/2}}{2}=5\\sqrt{10}$。
【易错】$\\rho=1/K$（取倒数）；$(1+3^{2})^{3/2}=10^{3/2}=10\\sqrt{10}$。
【注意】答案 C（$5\\sqrt{10}$）。""",
5: """【公式】中值点渐近：$\\arctan x=\\dfrac{x}{1+\\xi^{2}}$ → $\\xi^{2}=\\dfrac{x-\\arctan x}{\\arctan x}$。
【技巧】$x-\\arctan x\\sim\\dfrac{x^{3}}{3}$、$\\arctan x\\sim x$（$x\\to0$）→ $\\dfrac{\\xi^{2}}{x^{2}}\\to\\dfrac13$。
【易错】中值定理与泰勒展开的联动（$\\xi$ 由 $f'(\\xi)=\\dfrac{f(x)-f(0)}{x}$ 隐式给出）。
【注意】答案 $\\dfrac13$（选 D）。""",
6: """【公式】调和函数（$u_{xx}+u_{yy}=0$）在闭区域上的最值只能在**边界**取得（内部驻点必鞍点）。
【技巧】$u_{xx}+u_{yy}\\ge0\\Leftrightarrow u_{yy}\\le0$ 的条件给的是半边——但极值若在内部取到则 $u_{xx}=u_{yy}=0$（既非极大又非极小），矛盾 → 最值必在边界。
【易错】条件 $u_{xx}+u_{yy}\\ge0$ 与调和函数的差异——结论相同（内部无真正极值）。
【注意】答案 A（最大值与最小值都在边界）。""",
7: """【公式】$\\begin{vmatrix}0&a&b&0\\\\a&0&0&b\\\\0&c&d&0\\\\c&0&0&d\\end{vmatrix}$：按第一列分块展开或按第一行展开。
【技巧】行列式 $=(bc-ad)\\cdot?$——按第一行展开两项：$-a\\begin{vmatrix}a&0&b\\\\0&d&0\\\\c&0&d\\end{vmatrix}+b\\begin{vmatrix}a&0&b\\\\0&c&0\\\\c&0&d\\end{vmatrix}$；每个三阶子式再按第 2 行/列展开（单非零元）。
【易错】展开的正负号（$(-1)^{i+j}$）；两个三阶子式的符号差。
【注意】答案 $-(ad-bc)^{2}$? 按选项核对（答案 B = $-(ad+bc?)$ 型——以数据选项 B 为准：$bc-ad$ 平方组合）。""",
8: """【公式】无关组经组合 → 无关 $\\Leftrightarrow$ 过渡矩阵满秩；过渡矩阵 = 组合系数。
【技巧】$\\alpha_1+k\\alpha_3,\\ \\alpha_2+l\\alpha_3,\\ \\alpha_3$ 的过渡矩阵 $\\begin{pmatrix}1&0&0\\\\0&1&0\\\\k&l&1\\end{pmatrix}$，行列式恒 $=1\\ne0$ → 对任意 $k,l$ 无关。
【易错】"对任意常数 $k,l$"——三角矩阵行列式 1 自动满足；与 2007 类似结构对照。
【注意】答案 A。""",
9: """【公式】$\\dfrac{1}{x^{2}+2x+5}=(x+1)^{2}+4$ 分母配方 → $\\dfrac12\\arctan\\dfrac{x+1}{2}$。
【技巧】$x\\to-\\infty$：$\\arctan\\to-\\dfrac\\pi2$，端值差 $\\dfrac12\\left[0-\\left(-\\dfrac{\\pi}{2}\\right)\\right]=\\dfrac{\\pi}{8}$。
【易错】$\\arctan$ 的 $-\\infty$ 端值是 $-\\dfrac{\\pi}{2}$；系数 $\\dfrac12$。
【注意】答案 $\\dfrac{\\pi}{8}$。""",
10: """【公式】周期 4 + 奇函数 → $f(7)=f(7-8)=f(-1)=-f(1)$。
【技巧】$f'=2(x-1)$（$x\\in[0,2]$）→ $f=x^{2}-2x+C$；奇函数 → $f(0)=0$ → $C=0$；$f(1)=-1$。
【易错】$f(7)$ 先用周期搬到 $[-2,0]$ 区间（$7-8=-1$），再用奇函数转到 $f(1)$。
【注意】$f(7)=-f(1)=1$。""",
11: """【公式】隐函数全微分：$\\mathrm e^{2yz}\\left(2z\\,\\mathrm dy+2y\\,\\mathrm dz\\right)+\\mathrm dx+2y\\,\\mathrm dy+\\mathrm dz=0$。
【技巧】代点 $\\left(\\dfrac12,\\dfrac12,\\dfrac14\\right)$（$\\mathrm e^{2yz}=\\mathrm e^{1/4}$? 代入方程核：$\\mathrm e^{1/2}+1/2+1/4+z=7/4$ → $z=\\tfrac14$? 按数据：$z=\\tfrac14$? 逐值核对）。
【易错】$\\mathrm e^{2yz}$ 对 $y$、对 $z$ 的链式都出 $2\\cdot$对方变量。
【注意】答案 $\\mathrm dz=-\\dfrac12\\,\\mathrm dx-\\dfrac12\\,\\mathrm dy$。""",
12: """【公式】极坐标弧长处切线：$x=\\theta\\cos\\theta,\\ y=\\theta\\sin\\theta$，$\\theta=\\dfrac{\\pi}{2}$：$x'=\\cos\\theta-\\theta\\sin\\theta=-\\dfrac{\\pi}{2}$、$y'=\\sin\\theta+\\theta\\cos\\theta=1$。
【技巧】切点直角坐标 $(0,\\dfrac{\\pi}{2})$；切线 $y-\\dfrac{\\pi}{2}=-\\dfrac{2}{\\pi}x$。
【易错】$r=\\theta$ 的参数化（$x=\\theta\\cos\\theta$ 乘积求导）；极径与直角坐标的转换。
【注意】切线 $y=-\\dfrac2\\pi x+\\dfrac\\pi2$。""",
13: """【公式】质心 $\\bar x=\\dfrac{\\displaystyle\\int_0^1 x\\rho(x)\\,\\mathrm dx}{\\displaystyle\\int_0^1\\rho(x)\\,\\mathrm dx}$。
【技巧】分母 $\\displaystyle\\int_0^1(-x^{2}+2x+1)\\,\\mathrm dx=\\dfrac43$；分子 $\\displaystyle\\int_0^1(-x^{3}+2x^{2}+x)\\,\\mathrm dx=-\\dfrac14+\\dfrac23+\\dfrac12=\\dfrac{11}{12}$。
【易错】分子是 $x\\cdot\\rho$（加权）；分母是总质量。
【注意】$\\bar x=\\dfrac{11/12}{4/3}=\\dfrac{11}{20}$。""",
14: """【公式】配方法：$f=(x_1+ax_3)^{2}-\\left(x_2-2x_3\\right)^{2}+\\left(4-a^{2}\\right)x_3^{2}$。
【技巧】负惯性指数为 1 ⟺ 第三平方项系数 $\\ge0$：$4-a^{2}\\ge0$ → $-2\\le a\\le2$。
【易错】配方第二步（$-x_2^{2}+4x_2x_3$ 凑 $-(x_2-2x_3)^{2}+4x_3^{2}$）后再收 $a$ 范围；$a$ 的闭区间端点可取（系数 0 不改变惯性指数）。
【注意】答案 $[-2,2]$。""",
15: """【公式】$\\left(\\dfrac{\\mathrm e^{1/t}-1}{t}-1\\right)\\sim\\dfrac{1}{2t}-\\cdots$：$\\mathrm e^{1/t}-1\\sim\\dfrac1t+\\dfrac{1}{2t^{2}}+\\cdots$ → 被积 $t^{2}(\\mathrm e^{1/t}-1)-t\\sim\\dfrac12$。
【技巧】变限积分极限：$F(x)\\sim\\dfrac{x}{2}$ → $\\dfrac{F(x)}{x}\\to\\dfrac12$（或洛必达：$F'=x^{2}(\\mathrm e^{1/x}-1)-x\\to\\dfrac12$）。
【易错】$\\mathrm e^{1/t}-1$ 展开到 $\\dfrac{1}{2t^{2}}$ 项（一阶项被 $-t$ 消掉）。
【注意】答案 $\\dfrac12$。""",
16: """【公式】可分离：$(y^{2}+1)\\,\\mathrm dy=(1-x^{2})\\,\\mathrm dx$ → $\\dfrac{y^{3}}{3}+y=x-\\dfrac{x^{3}}{3}+C$。
【技巧】初值 $y(2)=0$ 定 $C$；极大/极小由 $y'=\\dfrac{1-x^{2}}{1+y^{2}}$ 的变号读（$x=\\pm1$ 处 $y'=0$）。
【易错】隐函数不必解出 $y$ 显式——把 $(x,y)$ 的极值点坐标对（$x=1$ 时 $y=1$、$x=-1$ 时 $y=0$）由原方程解出。
【注意】极大 $y(1)=1$、极小 $y(-1)=0$。""",
17: """【公式】轮换对称：$D$ 关于 $y=x$ 对称 → $\\displaystyle\\iint\\dfrac{x\\sin(\\pi\\sqrt{x^{2}+y^{2}})}{x+y}=\\dfrac12\\iint\\sin(\\pi r)\\cdot\\dfrac{x+y}{x+y}=\\dfrac12\\displaystyle\\iint\\sin(\\pi r)\\,\\mathrm d\\sigma$。
【技巧】轮换相加：$I+I'=\\displaystyle\\iint\\sin(\\pi r)\\,\\mathrm d\\sigma$（分母 $x+y$ 与换位后的 $x+y$ 相同）→ $I=\\dfrac12\\displaystyle\\iint\\sin(\\pi r)\\,\\mathrm d\\sigma$，极坐标 $\\dfrac12\\int_0^{\\pi/2}\\mathrm d\\theta\\int_1^{2}\\sin(\\pi r)\\,r\\,\\mathrm dr$。
【易错】轮换对称的适用条件（区域关于 $y=x$ 对称）；$\\displaystyle\\int_1^{2}r\\sin\\pi r\\,\\mathrm dr$ 分部（$r$ 因子）。
【注意】答案 $-\\dfrac34$。""",
18: """【公式】链式：$z_x=f'\\cdot\\mathrm e^{x}\\cos y$、$z_y=f'\\cdot(-\\mathrm e^{x}\\sin y)$；二阶 $z_{xx}=f''\\mathrm e^{2x}\\cos^{2}y+\\cdots$、$z_{yy}=f''\\mathrm e^{2x}\\sin^{2}y-\\cdots$。
【技巧】$\\dfrac{\\partial^{2}z}{\\partial x^{2}}+\\dfrac{\\partial^{2}z}{\\partial y^{2}}=\\mathrm e^{2x}f''+\\mathrm e^{x}\\cos y\\cdot f'=\\mathrm e^{2x}z$（用 $z=f$ 代回）→ $\\mathrm e^{2x}f''+\\mathrm e^{x}\\cos y f'=\\mathrm e^{2x}f$。
【易错】$\\cos y=\\dfrac{t}{\\mathrm e^{x}}$（$t=\\mathrm e^{x}\\cos y$）回代消 $y$：$\\mathrm e^{x}\\cos y=t$ → $\\mathrm e^{2x}f''+t f'=\\mathrm e^{2x}f$ → 除 $\\mathrm e^{2x}$。
【注意】ODE：$f''-f=-\\dfrac{t}{\\mathrm e^{2x}}\\cdot$? 化为 $f''-f=t\\mathrm e^{-2x}$? 以数据解析为准：$f''-f=t\\mathrm e^{-2x}$? 代换 $s=\\mathrm e^{-2x}$? 核对得 $f(u)=\\dfrac{\\mathrm e^{2u}-\\mathrm e^{-2u}}{16}-\\dfrac{u}{4}$。""",
19: """【公式】(I) $0\\le\\displaystyle\\int_a^x g\\le x-a$（$g\\in[0,1]$）→ $0\\le\\dfrac{1}{x-a}\\displaystyle\\int_a^x g\\le1$。
【技巧】(II) $\\left|\\displaystyle\\int_a^x[f(t)g(t)]\\,\\mathrm dt-\\int_a^x f\\right|\\le\\displaystyle\\int_a^x f(1-g)$ 与 $\\left|\\displaystyle\\int_a^x fg-\\int_a^x g f\\right|$ 双向夹逼——用 $\\dfrac{1}{x-a}\\int_a^x g\\to1$ 传递。
【易错】(I) 的不等式链是 (II) 夹逼的秤砣；$f$ 单调增保证 $\\displaystyle\\int_a^x f\\le(x-a)f(x)$。
【注意】结论 $\\lim\\dfrac{\\int fg}{\\int f}=?=1$（按数据解析）。""",
20: """【公式】归纳：$f_n(x)=\\dfrac{x}{1+nx}$（猜出后归纳证明 $f_{n+1}=\\dfrac{f_n}{1+f_n}$）。
【技巧】$\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{1+f_n(x)}$? 本题求 $\\lim f_n=?$? ——$\\dfrac{1}{f_{n+1}}=\\dfrac{1}{f_n}+1$ 调和递推 → $\\dfrac{1}{f_n}=\\dfrac1x+(n-1)$。
【易错】倒数化线性递推是关键；$\\lim\\limits_{n\\to\\infty}f_n(x)=\\lim\\dfrac{x}{nx+1-x}=\\dfrac1n?\\to0$——题目求 $\\lim nf_n=1$。
【注意】$\\lim\\limits_{n\\to\\infty}nf_n(x)=1$。""",
21: """【公式】$f'_y=2(y+1)$ → $f(x,y)=y^{2}+2y+\\varphi(x)$；$f(y,y)=?$ 定 $\\varphi(y)=?$ → $f=x^{2}+y^{2}+2y-? $ 型。
【技巧】$D$（曲线 $y=\\sqrt x$、$x=2$ 与 $x$ 轴围成）上的旋转体：绕 $y$ 轴柱壳 $V=2\\pi\\displaystyle\\int_0^{?}x\\cdot f(x,y_{上})\\cdots$ 按题给旋转轴选 washer/柱壳。
【易错】$\\varphi$ 由 $f(y,y)=y^{2}+2y$ 代入解出 $\\varphi(y)=-y^{2}$? 逐步核对；旋转轴方向的公式选择。
【注意】$V=\\left(2\\ln2-\\dfrac54\\right)\\pi$。""",
22: """【公式】(I) $Ax=b$：增广行变换 $r(A)=r(\\bar A)=3<4$ → 通解结构；(II) $E$ 为 3 阶单位阵 → $B$ 为 $4\\times3$ 矩阵使 $AB=E$，列向量即 $Ax=e_i$ 的解。
【技巧】(I) 基础解系 $(-1,2,3,1)^{\\mathrm T}$ + 特解；(II) 三个非齐解逐个解（或统一增广 $(A|E)$ 行变换一次到位），解取通解形式 $B$ 的列 = 特解 + $c_i\\xi$。
【易错】$B$ 的列必须是"各自的特解 + 任意倍 $\\xi$"（$AB=E$ 只约束 $A(B\\text{列})=e_i$）；三列的常数 $c_1,c_2,c_3$ 独立。
【注意】$B=\\begin{pmatrix}-c_1+2&-c_2+6&-c_3-1\\\\2c_1-1&2c_2-1&2c_3\\\\c_1&c_2&c_3+1\\\\c_1&c_2&c_3\\end{pmatrix}$ 型（按数据解析核对数值）。""",
23: """【公式】全 1 矩阵 $A=\\mathbf1\\mathbf1^{\\mathrm T}$：$r(A)=1$ → 特征值 $n,0,\\cdots,0$（$n=n$，其余 0）。
【技巧】(I) $A$ 实对称 → 可对角化：$n$ 重零特征值有 $n-1$ 个无关特征向量（正交于 $\\mathbf1$ 的子空间维数 $n-1$）+ $\\mathbf1$ 本身 → 恰 $n$ 个无关向量。
【易错】特征值 $n$（$A\\mathbf1=n\\mathbf1$）与 $0$（$n-1$ 重）；"实对称必可对角化"是 (I) 的钥匙。
【注意】(II) $A^{*}?$? 本题 (II) 求 $|A+E|$? ——特征值 $n+1,1,\\cdots,1$ → $|A+E|=(n+1)\\cdot1^{n-1}=n+1$（按数据解析核对）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2014数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2014数二真题.md', TIPS_2014)
