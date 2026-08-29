# -*- coding: utf-8 -*-
# 2001 卷点睛插入（写作规范见 _tips_2000.py 头注释）
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
            print(f'  [WARN] Q{no} 未找到块结束行，跳过')
            continue
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

TIPS_2001 = {
1: """【公式】分子有理化：$\\sqrt A-\\sqrt B=\\dfrac{A-B}{\\sqrt A+\\sqrt B}$（$A-B$ 必出公因子）。
【技巧】$\\dfrac00$ 型三连动作固定：分母因式分解 → 分子乘共轭 → 约去公因子后代值。
【易错】共轭在 $x=1$ 处的值 $\\sqrt2+\\sqrt2=2\\sqrt2$ 直接口算，别展开算错；$x^{2}+x-2=(x-1)(x+2)$ 的因式分解。
【注意】答案 $-\\dfrac{\\sqrt2}{6}=-\\dfrac{2}{3\\cdot2\\sqrt2}$，两种写法等价。""",
2: """【公式】隐函数偏导公式 $y'=-\\dfrac{F_x}{F_y}$；法线斜率 $=-\\dfrac{1}{\\text{切线斜率}}$。
【技巧】公式法（分别求 $F_x$、$F_y$）比两边直接求导稳——$\\cos(xy)$ 的链式（内层 $xy$ 求导出 $y$ 和 $x$ 两项）藏在偏导里不易漏。
【易错】"法线"不是切线：$y'=-2$ 是切线斜率，答案要的是负倒数 $\\dfrac12$；先代点验证在曲线上。
【注意】$\\mathrm e^{2x+y}$ 在 $(0,1)$ 处 $=\\mathrm e$。""",
3: """【公式】对称区间：奇函数积分为 0；$\\displaystyle\\int\\sin^{2}x\\cos x\\,\\mathrm dx=\\dfrac{\\sin^{3}x}{3}+C$。
【技巧】对称区间先扫一遍奇偶性——能砍掉一半就不硬算。
【易错】$\\sin^{2}x\\cos x$ 是偶函数（偶×偶），不能扔；凑微分方向 $\\cos x\\,\\mathrm dx=\\mathrm d(\\sin x)$。
【注意】奇偶判定：$x^{3}$ 奇 × $\\cos x$ 偶 = 奇。""",
4: """【公式】$\\left(y\\arcsin x\\right)'=y'\\arcsin x+\\dfrac{y}{\\sqrt{1-x^{2}}}$；$\\left(\\arcsin x\\right)'=\\dfrac{1}{\\sqrt{1-x^{2}}}$。
【技巧】一阶方程动手前先扫一眼：左边恰好是某乘积的导数 → 凑微分直接积分，比套一阶线性公式快一个量级。
【易错】初始点 $(\\tfrac12,0)$：$0\\cdot\\arcsin\\tfrac12=\\tfrac12+C$ 定 $C$，别把 $y=0$ 当成无信息。
【注意】$\\arcsin\\tfrac12=\\dfrac{\\pi}{6}$ 本题其实用不到（乘的是 $y=0$）。""",
5: """【公式】"各行元素之和相等"型行列式：全 1 列加到一列提公因子，$\\left|\\begin{smallmatrix}a&1&1\\\\1&a&1\\\\1&1&a\\end{smallmatrix}\\right|=(a+2)(a-1)^{2}$。
【技巧】$|A|=0$ 只给候选值（$a=-2,1$），无穷多解必须逐个回代验证 $r(A)=r(\\bar A)<n$。
【易错】$a=1$ 时 $r(A)=1\\ne r(\\bar A)=2$ 是无解不是无穷多解——只解 $|A|=0$ 不回代是本题最大陷阱。
【注意】含参方程组题的完整闭环：行列式 → 候选 → 秩验证 → 结论。""",
6: """【公式】分段函数复合的"值域视角"：先算内层值域，再看落在外层哪一段。
【技巧】$f$ 的值域是 $\\{0,1\\}$，全部落在 $|u|\\le1$（取值 1 的段）→ 第二层起恒为 1，与 $x$ 无关。
【易错】别把三层嵌套想复杂——第二层已经塌缩成常数 1，$f(1)=1$。
【注意】$f(1)=1$ 用的是 $|1|\\le1$ 的边界含等号。""",
7: """【公式】$1-\\cos x\\sim\\dfrac{x^{2}}2$、$\\ln(1+u)\\sim u$、$\\mathrm e^{u}-1\\sim u$、$\\sin u\\sim u$——全部换算成 $x$ 的幂次再比阶。
【技巧】"A 是 B 的高阶无穷小" = $A$ 的阶数 **严格大于** $B$ 的阶数；链式条件翻译成 $2<n+1<4$。
【易错】不等号方向写反（"A 比 B 高阶"说成 A 阶数小）；幂次相乘时指数相加（$x\\cdot x^{n}=x^{n+1}$）。
【注意】$n$ 为正整数且不等式取不到端点 → $n=2$ 唯一。""",
8: """【公式】$y''=0$ 的点 ≠ 拐点——须验证变号（充分条件：该点处 $y'''\\ne0$，即 $y''$ 的单重零点）。
【技巧】$y''$ 是二次式 → 拐点至多 2 个；两根处 $y'''=24x-48\\ne0$ 立刻确认。
【易错】数出 $y''$ 的零点个数就当拐点个数——多重零点（切于横轴）不变号就不是拐点。
【注意】结构对称性：曲线关于 $x=2$ 对称，两个拐点也关于 $x=2$ 对称，可作检验。""",
9: """【公式】构造比较：$g(x)=f(x)-x$，则 $g(1)=0$、$g'(1)=f'(1)-1=0$、$g''=f''<0$ → $g$ 在 $x=1$ 取极大值。
【技巧】"$f$ 与 $x$ 比大小"条件反射作差；"二阶导 < 0"的信息链：$g''<0\\Rightarrow g'$ 递减 $\\Rightarrow$ 以 $g'(1)=0$ 为界左右定 $g'$ 符号。
【易错】$f'(1)=1$ 是隐藏锚点（$g'(1)=0$），丢掉它整个判定断链。
【注意】极大值 $g(1)=0$ → 两侧 $g<0$，即两侧**均** $f(x)<x$——选"均"的选项，别选两侧不同。""",
10: """【公式】图形语言互译：增区间 $\\leftrightarrow f'>0$、减区间 $\\leftrightarrow f'<0$、极值点 $\\leftrightarrow f'=0$ 且变号（可导时）。
【技巧】只抓 $f'$ 的**符号变化序列**（本题"正→负→正"两个零点），不描具体形状。
【易错】下降段对应 $f'<0$，别顺着 $f$ 的下降方向把 $f'$ 也画成下降。
【注意】图形选择题用符号序列排除，比逐段分析快。""",
11: """【公式】$\\sqrt{x^{2}+1}$ 换元模板：$x=\\tan t$ → $\\sqrt{x^{2}+1}=\\sec t$；$\\displaystyle\\int\\frac{\\mathrm du}{1+u^{2}}=\\arctan u+C$。
【技巧】连续两次换元（$x=\\tan t$ 后 $u=\\sin t$）比硬凑更顺；回代用辅助直角三角形：$\\sin t=\\dfrac{x}{\\sqrt{x^{2}+1}}$。
【易错】$2\\tan^{2}t+1=\\dfrac{1+\\sin^{2}t}{\\cos^{2}t}$ 的整理——分子分母同乘 $\\cos t$ 时 $\\mathrm dx=\\sec^{2}t\\,\\mathrm dt$ 只剩一个 $\\cos t$。
【注意】答案 $\\arctan\\dfrac{x}{\\sqrt{x^{2}+1}}+C$。""",
12: """【公式】$1^{\\infty}$ 型：$\\ln L=\\lim(\\text{底数}-1)\\times$指数；本题 $\\ln L=\\lim\\limits_{t\\to x}\\dfrac{\\ln\\sin t-\\ln\\sin x}{x-\\sin x}$。
【技巧】洛必达时**对 $t$ 求导**（$x$ 是常数）——这正是"对数差商 = 对 $t$ 求导"的结构，$\\dfrac{\\cot t}{-\\cos t}$。
【易错】$x=k\\pi$ 与 $x=\\dfrac{k\\pi}{2}$（$k$ 奇）两类间断点要分开验证极限行为；$\\to0$ 与 $\\to+\\infty$ 都属第二类。
【注意】间断点分类题先写全 $\\sin2x=0$ 的解，再按左右极限归类，别漏 $k$ 的奇偶。""",
13: """【公式】曲率半径 $\\rho=\\dfrac{(1+y'^{2})^{3/2}}{|y''|}$；弧长 $\\dfrac{\\mathrm ds}{\\mathrm dx}=\\sqrt{1+y'^{2}}$；链式换元 $\\dfrac{\\mathrm d\\rho}{\\mathrm ds}=\\dfrac{\\mathrm d\\rho/\\mathrm dx}{\\mathrm ds/\\mathrm dx}$。
【技巧】$\\rho(s)$ 对 $s$ 的导数全部转成对 $x$ 的导数之商——参数链式是这类题的唯一主线。
【易错】$y''<0$ 时取 $|y''|$；$\\left(\\tfrac12(4x+1)^{3/2}\\right)'=3\\sqrt{4x+1}$ 的系数（$\\tfrac32\\cdot2$）。
【注意】最终答案是常数 9——若算出带 $x$ 的式子，多半是 $\\dfrac{\\mathrm ds}{\\mathrm dx}$ 或链式错了。""",
14: """【公式】反函数三件套：$g(f(x))=x$、$f(g(x))=x$、$\\left(f^{-1}\\right)'(x)=\\dfrac{1}{f'(f^{-1}(x))}$；变限积分方程第一步两边求导。
【技巧】求出 $g(x)=\\mathrm e^{x}(x^{2}+2x)$ 后**不必反解** $f$ 的显式——$g(f(x))=x$ 隐式定位即可：$\\mathrm e^{f}[f^{2}+2f]=x$。
【易错】$\\dfrac{\\mathrm d}{\\mathrm dx}\\left[x^{2}\\mathrm e^{x}\\right]=\\mathrm e^{x}(x^{2}+2x)$ 的乘积求导；隐式解再求导时 $\\dfrac{\\mathrm d}{\\mathrm du}\\bigl[(u^{2}+2u)\\mathrm e^{u}\\bigr]=\\mathrm e^{u}(u^{2}+4u+2)$。
【注意】本题 $f$ 无初等显式——答案写隐式方程 $\\mathrm e^{f}[f^{2}+2f]=x$（$f\\ge0$）就是完整答案。""",
15: """【公式】$f'=g,\\ g'=2\\mathrm e^{x}-f$ 消元：$f''+f=2\\mathrm e^{x}$；特解 $\\mathrm e^{x}$（$\\lambda=1$ 非特征根），通解 $C_{1}\\sin x+C_{2}\\cos x+\\mathrm e^{x}$。
【技巧】被积式 $\\dfrac{g}{1+x}-\\dfrac{f}{(1+x)^{2}}$ 凑商导数：分母差一次幂 → $\\left[\\dfrac{f}{1+x}\\right]'$（用 $f'=g$ 替换后恰好吻合）。
【易错】两个初值 $f(0)=0$、$f'(0)=g(0)=2$ 缺一不可；凑商导数时先把 $f'=g$ 代进分子。
【注意】积分即原函数代端点：$\\left[\\dfrac{f(x)}{1+x}\\right]_0^{\\pi}=\\dfrac{\\mathrm e^{\\pi}-1}{1+\\pi}$。""",
16: """【公式】切线 $y$ 截距（$X=0$）：$Y=y-xy'$；齐次方程识别：$\\sqrt{x^{2}+y^{2}}=y-xy'$ 各项都齐次 → 令 $y=ux$。
【技巧】几何条件翻译成微分方程后，$\\dfrac{\\mathrm du}{\\sqrt{1+u^{2}}}=-\\dfrac{\\mathrm dx}{x}$ 的积分结果是 $\\operatorname{arsinh}u=-\\ln x+C$（对 $\\mathrm e$ 化简）。
【易错】$y$ 截距 = 曲线减去 $xy'$，不是 $y+xy'$；$\\sqrt{x^{2}+y^{2}}=y-xy'$ 隐含右式非负，开方去绝对值时方向别反。
【注意】隐式解 $y+\\sqrt{x^{2}+y^{2}}=\\tfrac12$ 两边平方可化为抛物线 $y=\\tfrac14-x^{2}$，第二问就变成标准切线围面积最值。""",
17: """【公式】半球 $V=\\dfrac23\\pi r^{3}$、$S=2\\pi r^{2}$（贴地无底面，不加 $\\pi r^{2}$）；链式 $\\dfrac{\\mathrm dV}{\\mathrm dt}=2\\pi r^{2}\\dfrac{\\mathrm dr}{\\mathrm dt}$。
【技巧】"速率 ∝ 表面积" + 立体公式 → $\\dfrac{\\mathrm dr}{\\mathrm dt}=-K$ 常数：半径**匀速**减小，是这类题的核心结论。
【易错】融化是减少，$-K$ 的负号；"剩 $\\dfrac18$ 体积" = 半径剩 $\\dfrac12$（开立方，不是体积开方）。
【注意】3 小时半径减半 → 再 3 小时融完剩下的一半 → 总共 6 小时，可口的 sanity check。""",
18: """【公式】一阶麦克劳林（带拉格朗日余项）：$f(x)=f(0)+f'(0)x+\\dfrac{f''(\\xi)}{2}x^{2}$；$\\displaystyle\\int_{-a}^{a}x\\,\\mathrm dx=0$、$\\int_{-a}^{a}x^{2}\\,\\mathrm dx=\\dfrac{2a^{3}}{3}$。
【技巧】证"存在 $\\eta$ 使 $f''(\\eta)\\times$常数 $=\\int f$"：展开式逐项积分（奇次项归零）+ 积分中值定理（$f''$ 连续、$x^{2}\\ge0$ 保号）。
【易错】$\\xi$ 是随 $x$ 变的，不能直接把 $f''(\\xi)$ 提出积分号——靠 $x^{2}\\ge0$ 的保号性 + 连续函数介值把 $\\eta$ 找出来，这一步要写明。
【注意】$f(0)=0$ 已给，展开从 $f'(0)x$ 起步；常数 $\\dfrac{a^{3}}{3}$ 由 $\\dfrac12\\cdot\\dfrac{2a^{3}}{3}$ 而来。""",
19: """【公式】矩阵方程提取公因子：$AXA-AXB-BXA+BXB=(A-B)X(A-B)$（左提 $A-B$、右提 $A-B$）。
【技巧】矩阵方程先做"左合并 + 右合并"，配成 $MXN=E$ 型 → $X=M^{-1}N^{-1}$。
【易错】四项交叉项的符号（减 $AXB$、减 $BXA$）提错一个就配不成完全平方结构；$(A-B)$ 是单位上三角，求逆可逐列解方程。
【注意】$X=[(A-B)^{-1}]^{2}$，$A-B$ 对角元全 1 必可逆，答案 $\\begin{pmatrix}1&2&5\\\\0&1&2\\\\0&0&1\\end{pmatrix}$。""",
20: """【公式】基础解系两条件：① 都是 $Ax=0$ 的解（$\\beta$ 是 $\\alpha$ 的线性组合，自动满足）；② 线性无关。个数 $n-r(A)$ 由 $\\alpha$ 组继承。
【技巧】按 $\\alpha_i$ 归并组合系数得循环方程组，线性无关 $\\Leftrightarrow$ 系数行列式 $\\ne0$：$\\begin{vmatrix}1&0&0&t\\\\t&1&0&0\\\\0&t&1&0\\\\0&0&t&1\\end{vmatrix}=1-t^{4}$。
【易错】$t^{4}\\ne1$ 在**实数范围**内即 $t\\ne\\pm1$（实数只有这两个四次方根）；$t=\\pm1$ 时要指出相关（存在非零组合）。
【注意】答"当 $t\\ne\\pm1$ 时 $\\beta_{1},\\dots,\\beta_{4}$ 也是基础解系"，两半缺一不可：既是解、又无关。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2001数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2001数二真题.md', TIPS_2001)
