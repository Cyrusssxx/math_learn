# -*- coding: utf-8 -*-
# 2020 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2020 = {
1: """【公式】无穷小阶的运算：$\\ln(1+u)\\sim u-u^{2}/2+\\cdots$、$(1-\\cos x)^{3/2}\\sim\\left(\\tfrac{x^{2}}{2}\\right)^{3/2}=\\dfrac{x^{3}}{2^{3/2}}$。
【技巧】四项各展开成 $x$ 的幂次（$\\sqrt{1-x}\\sim$ 一阶、$\\arcsin$ 一阶、$\\mathrm e^{x^{3}}-1\\sim x^{3}$、$(1-\\cos x)^{3/2}$ 三阶）→ 阶最高即幂次最大者。
【易错】$(1-\\cos x)^{3/2}$ 是三阶（$\\tfrac32$ 次幂），远高于其余的一、二阶项。
【注意】答案 D。""",
2: """【公式】潜在间断点（$x=-1,0,1,2$）逐点求左右极限：$x=-1$ 处 $\\ln|1+x|\\to-\\infty$ → $f\\to\\infty$（第二类）；$x=0$ 处 $\\mathrm e^{1/(x-1)}\\to\\mathrm e^{-1}$、$\\ln(1+x)/x\\to1$ → 有限（第一类可去）；$x=1$ 处 $\\mathrm e^{1/(x-1)}$ 左右 $0/\\infty$ 分裂。
【技巧】$\\mathrm e^{1/(x-1)}$ 在 $x=1$ 两侧一趋 0 一趋 $\\infty$——第二类间断的典型来源。
【易错】$x=0$ 处 $\\dfrac{\\ln|1+x|}{x}\\to1$（等价代换）不是无穷。
【注意】第二类间断点 2 个（$x=-1$ 与 $x=1$，答案 C）。""",
3: """【公式】凑微分：$u=\\arcsin\\sqrt{x}$ → $\\mathrm du=\\dfrac{\\mathrm dx}{2\\sqrt{x(1-x)}}$——被积函数恰好是 $2\\,\\mathrm du$。
【技巧】$\\int_0^1 2u\\,\\mathrm du=1$；被积函数"长得像某个复合函数的导数"时先凑再算。
【易错】系数 2（分母是 $\\sqrt{x(1-x)}$，微分里是 $2\\sqrt{x(1-x)}\\,\\mathrm dx$）。
【注意】答案 1（选 A）。""",
4: """【公式】泰勒系数法：$\\ln(1-x)=-\\displaystyle\\sum_{k\\ge1}\\dfrac{x^{k}}{k}$ → $x^{2}\\ln(1-x)=\\displaystyle\\sum_{k\\ge1}\\left(-\\dfrac1k\\right)x^{k+2}$。
【技巧】$x^{n}$ 系数（$n\\ge3$）$=-\\dfrac{1}{n-2}$ → $f^{(n)}(0)=n!\\times\\left(-\\dfrac{1}{n-2}\\right)$。
【易错】负号；$n-2$ 的错位（乘 $x^{2}$ 幂次 +2）。
【注意】答案 $-\\dfrac{n!}{n-2}$（选 A）。""",
5: """【公式】分段偏导用定义：$f_x(0,0)=\\lim\\limits_{x\\to0}\\dfrac{f(x,0)-f(0,0)}{x}=\\lim\\dfrac{x-0}{x}=1$；同理 $f_y(0,0)=1$。
【技巧】分段函数在分界点的偏导/可微性一律回定义；$f(x,y)$ 在坐标轴上取 $y$ 或 $x$（单变量分支）。
【易错】可微性：$\\lim\\dfrac{f(x,y)-f(0,0)-(x+y)}{\\sqrt{x^{2}+y^{2}}}$ 沿 $y=kx$ 路径依赖 → 不可微但偏导存在。
【注意】答案 B。""",
6: """【公式】一阶线性微分不等式的积分因子：$f'-f>0\\Rightarrow\\left(\\mathrm e^{-x}f\\right)'>0$ → $\\mathrm e^{-x}f(x)$ 单调增。
【技巧】$f'-f$ 结构 → 乘 $\\mathrm e^{-x}$ 凑导数；$\\mathrm e^{-x}f(2)>\\mathrm e^{-x}f(-2)$ → $f(2)>\\mathrm e^{4}f(-2)>f(-2)$（$\\mathrm e^{4}>1$、$f>0$）。
【易错】不等式两侧同乘 $\\mathrm e^{-x}$（恒正）保号；$\\mathrm e^{2}/\\mathrm e^{-2}=\\mathrm e^{4}$ 的放大方向。
【注意】答案 B。""",
7: """【公式】$r(A)=3$（不可逆 + 有非零三阶子式）→ $r(A^{*})=1$（伴随秩三段：$n$/$1$/$0$ 对应 $r(A)$ 的 $n$/$n-1$/$\\le n-2$）。
【技巧】$A^{*}x=0$ 的解空间维数 $=4-r(A^{*})=3$，基础解系含 3 个向量——由 $AA^{*}=|A|E=O$（$|A|=0$），$A$ 的列向量组（4 个 3 维向量，含线性无关的 3 个）都是 $A^{*}x=0$ 的解。
【易错】$r(A^{*})=1$ 而非 2；基础解系个数 = 解空间维数 = 3。
【注意】答案 C。""",
8: """【公式】$P^{-1}AP=\\mathrm{diag}(1,-1,1)$ 要求 $P$ 的列依次为 $\\lambda=1,-1,1$ 的特征向量；$\\alpha_2$ 属于 $-1$ 排在第二列。
【技巧】$\\alpha_1+\\alpha_3$ 仍是 $\\lambda=1$ 的特征向量（同特征值组合保持）→ $P=(\\alpha_1+\\alpha_3,\\alpha_2,\\alpha_3)$ 型合法；含 $\\alpha_2$ 的组合不行（跨特征值）。
【易错】不同特征值的特征向量组合不再是特征向量——$P$ 的列必须逐列是特征向量。
【注意】答案 D。""",
9: """【公式】双曲函数互逆：$y=\\ln\\left(t+\\sqrt{t^{2}+1}\\right)=\\operatorname{arsinh}t\\Leftrightarrow t=\\sinh y$；$x=\\cosh y$。
【技巧】$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{1/\\sqrt{t^{2}+1}}{t/\\sqrt{t^{2}+1}}=\\dfrac1t$；$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{-1/t^{2}}{t/\\sqrt{t^{2}+1}}$，代 $t=1$。
【易错】$ x'(t)=\\dfrac{t}{\\sqrt{t^{2}+1}}$、$ y'(t)=\\dfrac{1}{\\sqrt{t^{2}+1}}$（$\\ln$ 复合求导）。
【注意】$\\left.\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}\\right|_{t=1}=-\\sqrt{2}$。""",
10: """【公式】交换次序：$D:\\ \\sqrt y\\le x\\le1\\iff 0\\le y\\le x^{2},\\ 0\\le x\\le1$ → 内层换成 $y$。
【技巧】$\\int_0^{1}\\left(\\int_0^{x^{2}}\\mathrm dy\\right)\\sqrt{x^{3}+1}\\,\\mathrm dx=\\int_0^{1}x^{2}\\sqrt{x^{3}+1}\\,\\mathrm dx$；凑 $\\mathrm d(x^{3}+1)=3x^{2}\\,\\mathrm dx$。
【易错】$\\sqrt y\\le x\\iff y\\le x^{2}$ 的不等式方向；换序后积分限从 0 到 $x^{2}$。
【注意】$\\dfrac{2}{9}\\left(2\\sqrt{2}-1\\right)$。""",
11: """【公式】复合全微分：$ z_x=\\dfrac{y+\\cos(x+y)}{1+\\left[xy+\\sin(x+y)\\right]^{2}}$、$ z_y=\\dfrac{x+\\cos(x+y)}{1+\\cdots}$。
【技巧】代 $(0,\\pi)$：$ xy+\\sin(x+y)=\\sin\\pi=0$ → 分母 1；$ z_x=\\pi-1$、$ z_y=0-1=-1$。
【易错】$\\cos(0+\\pi)=-1$；分母在原表达式为 0 处 $=1$。
【注意】$\\mathrm dz=(\\pi-1)\\,\\mathrm dx-\\mathrm dy$。""",
12: """【公式】水压力微元：$\\mathrm dP=\\rho g\\cdot$（水深 $y$）$\times$（水平条宽 $2(a-y)$）$\\,\\mathrm dy$。
【技巧】斜边在水面、直角顶点深 $a$：宽度随深度线性递减 $ 2(a-y)$ → $\\mathrm dP=2\\rho g y(a-y)\\,\\mathrm dy$，$y\\in[0,a]$。
【易错】$\\int_0^{a}2y(a-y)\\,\\mathrm dy=\\dfrac{a^{3}}{3}$（均匀分布系数）；$\\rho g$ 作为常数乘出。
【注意】$ P=\\dfrac13\\rho ga^{3}$。""",
13: """【公式】二重根 $r=-1$ → $y=(C_1+C_2x)\\mathrm e^{-x}$；初值定 $C_1=0,C_2=1$ → $ y=x\\mathrm e^{-x}$。
【技巧】$\\displaystyle\\int_0^{+\\infty}x\\mathrm e^{-x}\\,\\mathrm dx=1$（$\\Gamma(2)=1!$，分部一次）。
【易错】$ y(0)=0\\Rightarrow C_1=0$、$ y'(0)=C_2=1$；无穷端 $ x\\mathrm e^{-x}\\to0$。
【注意】$\\displaystyle\\int_0^{+\\infty}y\\,\\mathrm dx=1$。""",
14: """【公式】行变换造零：第 3 行加到第 1 行、第 4 行加到第 2 行（或类似组合）→ 出现两行相等结构 → 因式分解出 $(a^{2}-4)$。
【技巧】$ a^{2}(a^{2}-4)=a^{2}(a-2)(a+2)$——四阶行列式先做行组合降复杂度，再按展开或连加。
【易错】行加法是自由变换（值不变）；$ a$ 的偶次结构（行列式是 $ a$ 的偶函数，奇数次项全消）。
【注意】$ a^{2}(a^{2}-4)$。""",
15: """【公式】$ y=\\dfrac{x\\cdot x^{x}}{(1+x)^{x}}=x\\left(\\dfrac{x}{1+x}\\right)^{x}=x\\left(1+\\dfrac1x\\right)^{-x}$。
【技巧】$\\left(1+\\tfrac1x\\right)^{-x}\\to\\mathrm e^{-1}$ → $ a=\\lim\\dfrac yx=\\mathrm e^{-1}$；$ b=\\lim(y-\\tfrac xe)=\\lim x\\left[\\left(1+\\tfrac1x\\right)^{-x}-\\mathrm e^{-1}\\right]$，用 $\\left(1+\\tfrac1x\\right)^{x}=\\mathrm e\\left(1-\\tfrac{1}{2x}+\\cdots\\right)$ 展开到 $\\tfrac1x$ 项 → $ b=\\dfrac{1}{2\\mathrm e}$。
【易错】$\\left(1+\\tfrac1x\\right)^{-x}=\\left[\\left(1+\\tfrac1x\\right)^{x}\\right]^{-1}=\\dfrac{\\mathrm e^{-1}}{1-\\tfrac{1}{2x}+\\cdots}$ → $ =\\mathrm e^{-1}\\left(1+\\tfrac{1}{2x}+\\cdots\\right)$，乘 $x$ 后 $ b=\\dfrac{1}{2\\mathrm e}$。
【注意】$ y=\\dfrac xe+\\dfrac{1}{2\\mathrm e}$。""",
16: """【公式】变限积分含 $x$：$ g(x)=\\dfrac{1}{x}\\displaystyle\\int_0^{x}f(xt)\\,\\mathrm dt\\xlongequal{u=xt}\\dfrac{1}{x}\\displaystyle\\int_0^{x^{2}}f(u)\\,\\mathrm du$。
【技巧】$ g'=\\dfrac{2x f(x^{2})\\cdot x-\\displaystyle\\int_0^{x^{2}} f}\\cdots$? 规范：$ g(x)=\\dfrac{1}{x}G(x^{2})$（$ G'=f$）→ $ g'(x)=-\\dfrac{G(x^{2})}{x^{2}}+2f(x^{2})$；$ g'(0)=\\lim\\dfrac{g(x)-g(0)}{x}$，用 $ f(x)\\sim x$。
【易错】换元后 $x$ 从被积函数里消失（这是本题设计的🔓）；$ f(x)/x\\to1$ → $ f(0)=0$。
【注意】$ g'(0)=\\dfrac12$。""",
17: """【公式】极值联立：$ f_x=3x^{2}-y=0$、$ f_y=24y^{2}-x=0$ → $x=24y^{2}$ 代入 $ 3\\cdot576y^{4}=y$。
【技巧】$ y(1728y^{3}-1)=0$ → $ y=\\dfrac{1}{12}$、$ x=\\dfrac16$；$ AC-B^{2}$ 判别：$ f_{xx}=6x,\\ f_{yy}=48y,\\ f_{xy}=-1$ 代入 → $ AC-B^{2}=\\dfrac{6}{6}\\cdot4-1=3>0$、$ A>0$ → 极小。
【易错】$ y=0$ 的分支舍（代入 $ f_x$ 得 $ x=0$ 不满足第二式）；$ AC-B^{2}>0$ 且 $ A>0$ 才是极小。
【注意】极小值 $ f\\left(\\tfrac16,\\tfrac1{12}\\right)=-\\dfrac{1}{216}$。""",
18: """【公式】函数方程组：$ 2f(x)+x^{2}f\\left(\\tfrac1x\\right)=\\dfrac{x}{\\sqrt{1+x^{2}}}$；把 $ x$ 换成 $\\tfrac1x$ 得第二条方程，联立解 $ f(x)$。
【技巧】两条方程两个未知函数值（$ f(x)$ 与 $ f(\\tfrac1x)$）——代换法消 $ f(\\tfrac1x)$：$ f(x)=\\dfrac{x}{\\sqrt{1+x^{2}}}$。
【易错】$\\dfrac{1}{1+x^{2}}$ 的化简（$\\tfrac{1/x^{2}}{1+1/x^{2}}=\\dfrac{1}{1+x^{2}}$）；体积 $V=\\pi\\displaystyle\\int_0^{1}\\left(\\sqrt{1+x^{2}}\\right)^{2}\\cdots$ 用 $ f(x)^{2}+?$ 拆。
【注意】$ f(x)=\\dfrac{x}{\\sqrt{1+x^{2}}}$；$ V=\\dfrac{\\pi^{2}}{6}$（按数据解析）。""",
19: """【公式】极坐标：$D$ 夹在 $x=1,\\ x=2$ 间、$y\\le x$ → $\\theta\\in[0,\\tfrac\\pi4]$、$ r\\in[\\sec\\theta,2\\sec\\theta]$；被积 $\\dfrac{\\sqrt{x^{2}+y^{2}}}{x}=\\dfrac{r}{r\\cos\\theta}=\\sec\\theta$。
【技巧】$\\displaystyle\\iint\\sec\\theta\\cdot r\\,\\mathrm dr\\,\\mathrm d\\theta=\\int_0^{\\pi/4}\\sec\\theta\\cdot\\dfrac{r^{2}}{2}\\Big|_{\\sec}^{2\\sec}\\mathrm d\\theta=\\dfrac32\\int_0^{\\pi/4}\\sec^{3}\\theta\\,\\mathrm d\\theta$。
【易错】$\\int\\sec^{3}=\\dfrac12(\\sec\\tan+\\ln|\\sec+\\tan|)$；$\\sec\\tfrac{\\pi}{4}=\\sqrt2,\\ \\tan\\tfrac{\\pi}{4}=1$。
【注意】$\\dfrac34\\left(\\sqrt2+\\ln(1+\\sqrt2)\\right)$。""",
20: """【公式】(I) 罗尔：$F(x)=(x-2)f(x)$，$F(1)=0$（$f(1)=0$）、$F(2)=0$ → 存在 $\\xi\\in(1,2)$ 使 $ F'(\\xi)=0$，展开 $ (x-2)f'+f=0$。
【技巧】(II) $f''(\\xi)+\\dfrac{2?}{\\xi-2}\\cdots$ 对 $ F'$ 再用一次罗尔? 按数据解析：对 $ F'$ 在 $[1,\\xi]$ 与 $[\\xi,2]$? 上的两次罗尔/介值组合。
【易错】$ F'$ 的表达式里含 $f$ 与 $f'$；第二问的方向（构造二次使用罗尔的函数）。
【注意】(II) 按数据解析核对（涉及 $ f''$ 的结论）。""",
21: """【公式】切线 $OT$ 面积条件：切线 $ Y-f(x)=f'(x)(X-x)$，$ Y$ 轴截距 $ =f(x)-xf'(x)$；$ S_{\\triangle}=$ 截距 × 底 / 2 型 → 微分方程 $ \\dfrac12\\cdot$? $ =\\dfrac12x^{2}$。
【技巧】面积条件 → $ \\left[\\dfrac{f(x)}{x^{2}}\\right]'$? 型：$ f=xf'-\\tfrac12x^{2}$? 按数据解析化成 $ \\dfrac{f(x)}{x^{3}}$ 的导数方程 → $ y=Cx^{3}$。
【易错】$ f(0)=0$、$ f'>0$、$ C>0$ 的相容；切线在 $ x$ 轴截距的符号（$x>0$ 时 $T$ 在原点右侧）。
【注意】$ y=Cx^{3}\\ (C>0)$。""",
22: """【公式】(I) $f$ 正定 $\\Leftrightarrow$ 顺序主子式全 $>0$：$ \\Delta_1=1$、$ \\Delta_2=\\begin{vmatrix}1&a\\\\a&1\\end{vmatrix}=1-a^{2}>0$、$ \\Delta_3=|A|=-(2a+1)^{2}$? 按数据 → $ a=-\\tfrac12$ 时 $\\Delta_2=\\tfrac34>0$ 且 $\\Delta_3=0$? 按数据（半正定 + $ r=2$? 按解析核对）。
【技巧】(II) 正交变换 $x=Py$：$A$（$a=-\\tfrac12$）的特征值由 $|\\lambda E-A|=\\lambda(\\lambda-? )$ 读出 → $Q$ 列 = 单位正交特征向量。
【易错】$ a=-\\tfrac12$ 时 $A$ 的特征值 $1$（二重）与 $?$——二重根的特征向量需施密特正交化。
【注意】(I) $a=-\\tfrac12$；(II) $P=\\begin{pmatrix}2&1&2/\\sqrt3\\\\1&0&4/\\sqrt3\\\\1&0&0\\end{pmatrix}$ 型（按数据解析核对列序）。""",
23: """【公式】(I) $P$ 可逆 ⟺ $\\alpha,A\\alpha$ 线性无关。反证：若相关则 $ A\\alpha=k\\alpha$（$\\alpha$ 是特征向量）→ 与题设"$\\alpha$ 不是 $A$ 的特征向量"矛盾。
【技巧】(II) $A^{2}\\alpha=A(A\\alpha)$ 用 (I) 的 $A\\alpha$ 表达式? 按数据解析：$A^{2}\\alpha=\\alpha-?$? 由 $AP=P\\begin{pmatrix}0&-?\\\\1&?\\end{pmatrix}$ 读 $A^{2}\\alpha$。
【易错】"$\\alpha$ 不是 $A$ 的特征向量"的翻译 = $\\alpha$ 与 $ A\\alpha$ 线性无关 = $ P$ 可逆；(II) 用 $P^{-1}AP$ 的具体矩阵计算 $ A^{2}\\alpha$。
【注意】(I) $P$ 可逆；(II) 按数据解析的 $A^{2}\\alpha$ 表达式。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2020数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2020数二真题.md', TIPS_2020)
