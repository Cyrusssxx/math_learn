# -*- coding: utf-8 -*-
# 2009 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2009 = {
1: """【公式】可去间断点 $\\Leftrightarrow$ 极限存在；$\\dfrac{1-x}{\\sin\\pi x}\\xrightarrow{x\\to1}-\\dfrac1\\pi$（洛必达）。
【技巧】分子 $x-x^{3}=x(1-x)(1+x)$ 与 $\\sin\\pi x$ 的零点都在整数处——分子也为零的整数点（$0,\\pm1$）才可能可去，其余整数全为 $\\infty$（第二类）。
【易错】$x\\to1$ 时把 $1-x$ 与 $\\sin\\pi x$ 都看成无穷小：$\\dfrac{1-x}{\\sin\\pi x}=\\dfrac{1-x}{\\sin(\\pi-\\pi x)}\\to\\dfrac1\\pi$（换元更顺）。
【注意】可去间断点共 3 个：$x=0,\\pm1$（答案 C）。""",
2: """【公式】$\\sin ax=ax-\\dfrac{a^{3}x^{3}}{6}+o(x^{3})$ → $x-\\sin ax=(1-a)x+\\dfrac{a^{3}x^{3}}{6}+o(x^{3})$；$x^{2}\\ln(1-bx)\\sim-bx^{3}$。
【技巧】与 $x^{2}$ 阶（三阶式子）匹配 → 一阶项必须消失：$1-a=0$，剩 $\\dfrac{x^{3}}{6}=-bx^{3}$。
【易错】不消一阶项直接比三阶系数；$-b$ 的负号（$\\ln(1-bx)\\sim-bx$）。
【注意】$a=1,\\ b=-\\dfrac16$（答案 A）。""",
3: """【公式】全微分还原：$\\mathrm z=x\\,\\mathrm dx+y\\,\\mathrm dy\\Rightarrow z=\\dfrac{x^{2}}{2}+\\dfrac{y^{2}}{2}+C$。
【技巧】椭圆抛物面在原点取极小——$z_x=z_y=0$、二阶正定，一眼定结论。
【易错】D 选项说"是极大值点"——开口向上的抛物面是**极小**。
【注意】答案 D（极小值点，非极大）。""",
4: """【公式】交换次序先画区域：两块积分 $D_1:\\ 1\\le x\\le y\\le2$ 与 $D_2:\\ 1\\le y\\le2,\\ \\sin\\dfrac{\\pi y}{2}\\le x\\le1$ 拼成一个区域。
【技巧】边界反解：$y=\\sin\\dfrac{\\pi x}2$ 在 $[1,2]$（$x\\in[1,2]$ 即角在 $[\\tfrac\\pi2,\\pi]$）上递减，反解 $x=\\dfrac{2}{\\pi}\\arcsin?$——按数据的选项路径：合并后先 $y$ 后 $x$ 或先 $x$ 后 $y$ 二选一。
【易错】$\\sin\\dfrac{\\pi x}{2}$ 在 $[1,2]$ 单调减，反解时 arcsin 的象限与系数。
【注意】答案 C。""",
5: """【公式】曲率圆信息：$\\rho=1$、圆心 $(0,0)$ → 曲线在 $(1,1)$ 处 $y'=-1$、$|y''|(1+y'^{2})^{3/2}=1$ → $y''(1)=-\\dfrac{1}{(1+1)^{3/2}}<0$。
【技巧】$f''$ 不变号（凸性固定）→ 曲线始终在曲率圆与切线的"夹层"内：$x\\in(1,2)$ 上 $f(x)<$ 切线值 $f(1)+f'(1)(x-1)=1-1\\cdot1=0$，也 $<$ 圆弧值 0。
【易错】$y'(1)=-1$ 是从圆的切线（垂直于半径）读出的；凸方向与圆内侧一致才可夹。
【注意】$f(2)<0$（答案 B）。""",
6: """【公式】$F'=f$：$f>0$ 段 $F$ 增、$f<0$ 段 $F$ 减；$F$ 的值 = $f$ 与 $x$ 轴围成的代数面积。
【技巧】$x<0$ 段用 $F(x)=-\\displaystyle\\int_x^0 f$：面积在 $x$ 轴下方取负——$F$ 在 $x<0$ 为负值且变化由 $f$ 的符号控制。
【易错】左半区间的 $F$ 值符号（对 $x<0$ 是负的）；$f$ 过零点才是 $F$ 的极值点。
【注意】答案 D。""",
7: """【公式】分块伴随：$M=\\begin{pmatrix}O&A\\\\B&O\\end{pmatrix}\\Rightarrow M^{*}=\\begin{pmatrix}O&|A|B^{-1}\\\\|B|A^{-1}&O\\end{pmatrix}$，再代 $A^{-1}=\\dfrac{A^{*}}{|A|}$。
【技巧】$|M|=|A||B|=6$；$B^{-1}=\\dfrac{B^{*}}{3}$、$A^{-1}=\\dfrac{A^{*}}{2}$ → 右上块 $=\\dfrac{2}{3}B^{*}$、左下块 $=\\dfrac{3}{2}A^{*}$。
【易错】分块求逆的子块**交换位置**（右上↔左下）；系数 $\\dfrac{2}{3}$ 与 $\\dfrac{3}{2}$ 别放反。
【注意】答案 B。""",
8: """【公式】列组合 = 右乘过渡阵：$Q=PC$（$C=\\begin{pmatrix}1&0&0\\\\1&1&0\\\\0&0&1\\end{pmatrix}$）→ $Q^{\\mathrm T}AQ=C^{\\mathrm T}\\Lambda C$。
【技巧】$P^{\\mathrm T}AP=\\mathrm{diag}(1,1,3)$ + 列的线性组合 → 只需算 $C^{\\mathrm T}\\Lambda C$（$3\\times3$ 小矩阵乘法）。
【易错】$C$ 的列是新列的表示系数（$\\alpha_1+\\alpha_2$ 是第一列 → $C$ 第一列 $(1,1,0)^{\\mathrm T}$）。
【注意】答案 A：$\\begin{pmatrix}2&1&0\\\\1&1&0\\\\0&0&3\\end{pmatrix}$。""",
9: """【公式】参数求导：$\\dfrac{\\mathrm dx}{\\mathrm dt}=-\\mathrm e^{-(1-t)^{2}}$（变限积分下限求导带负号）、$\\dfrac{\\mathrm dy}{\\mathrm dt}=3t^{2}\\ln(2-t^{3})-\\dfrac{3t^{4}}{2-t^{3}}$。
【技巧】$t=1$ 代入：$\\ln(2-1)=0$ 消掉第一项，$\\dfrac{\\mathrm dy}{\\mathrm dt}=-3$、$\\dfrac{\\mathrm dx}{\\mathrm dt}=-1$ → 斜率 3。
【易错】变限积分下限求导的负号；$t=1$ 时 $(0,0)$（$x=\\displaystyle\\int_0^0=0$）。
【注意】切线 $y=3x$。""",
10: """【公式】收敛性：$|k|\\ge0$ 时 $\\mathrm e^{|k|x}$ 当 $k\\ge0$ 不衰减发散 → 必须 $k<0$；$\\displaystyle\\int_0^{+\\infty}\\mathrm e^{kx}\\,\\mathrm dx=-\\dfrac{1}{k}$。
【技巧】偶函数对称：$1=2\\displaystyle\\int_0^{+\\infty}\\mathrm e^{kx}\\,\\mathrm dx=\\dfrac{-2}{k}$ → $k=-2$。
【易错】$|k|$ 与 $k$ 的区分（指数上 $|k||x|$，$k<0$ 时 $=|k|x=-kx$）；结果取负。
【注意】$k=-2$。""",
11: """【公式】振荡积分分部两次解封闭式：$I_n=\\displaystyle\\int_0^1\\mathrm e^{-x}\\sin nx\\,\\mathrm dx=\\dfrac{1-\\mathrm e^{-1}(\\sin n-n\\cos n)}{1+n^{2}}$ 型。
【技巧】放缩：$|I_n|\\le\\dfrac{1+\\mathrm e^{-1}(1+n)}{1+n^{2}}\\to0$（$n^{2}$ 吃掉 $n$）。
【易错】分部两次的符号配平；不要试图对 $\\sin nx$ 单独取极限（积分与极限不能随意交换）。
【注意】答案 0。""",
12: """【公式】隐函数一阶 $y'=\\dfrac{1-y}{x+\\mathrm e^{y}}$；二阶继续求导：$y''=-\\dfrac{2y'+xy''+\\mathrm e^{y}y''+y'^{2}\\mathrm e^{y}}{(x+\\mathrm e^{y})^{2}}$? 逐项规范求。
【技巧】代 $(0,0)$：$y'(0)=1$；二阶式代值后解出 $y''(0)=-3$。
【易错】$x=0$ 时 $y(0)=0$（不是 1：$0+\\mathrm e^{0}=0+1$ ✓）；$\\mathrm e^{y}\\cdot y'$ 的乘积求导。
【注意】$y''(0)=-3$。""",
13: """【公式】幂指函数：$y'=x^{2x}\\cdot2(\\ln x+1)$，驻点 $x=\\mathrm e^{-1}$。
【技巧】端点比较：$y(1)=1$ vs $y(\\mathrm e^{-1})=\\mathrm e^{-2/\\mathrm e}\\approx0.48$——驻点值才是最小。
【易错】$x\\to0^{+}$ 时 $x^{2x}=\\mathrm e^{2x\\ln x}\\to\\mathrm e^{0}=1$（不是 0）；$(0,1]$ 不含 $x=0$ 但极限 1 仍高于驻点值。
【注意】最小值 $\\mathrm e^{-2/\\mathrm e}$。""",
14: """【公式】相似不变量：迹。$\\operatorname{tr}(\\alpha\\beta^{\\mathrm T})=\\beta^{\\mathrm T}\\alpha$（内积是数）。
【技巧】$\\alpha\\beta^{\\mathrm T}\\sim\\mathrm{diag}(2,0,0)$ → 迹 $=2$ → $\\beta^{\\mathrm T}\\alpha=2$。
【易错】$\\operatorname{tr}(\\alpha\\beta^{\\mathrm T})=\\operatorname{tr}(\\beta^{\\mathrm T}\\alpha)$（循环移位）；$\\beta^{\\mathrm T}\\alpha=\\alpha^{\\mathrm T}\\beta$。
【注意】答案 2。""",
15: """【公式】$1-\\cos x\\sim\\dfrac{x^{2}}{2}$、$\\sin^{4}x\\sim x^{4}$；$\\ln(1+\\tan x)=\\tan x-\\dfrac{\\tan^{2}x}{2}+\\cdots$ → $x-\\ln(1+\\tan x)=x-\\tan x+\\dfrac{\\tan^{2}x}{2}+\\cdots$，其中 $x-\\tan x\\sim-\\dfrac{x^{3}}{3}$（三阶）。
【技巧】剥层：分子第一因子给 $x^{2}/2$，中括号的主项是 $\\dfrac{\\tan^{2}x}{2}\\sim\\dfrac{x^{2}}{2}$ → 比值 $\\dfrac{\\tfrac{x^{2}}2\\cdot\\tfrac{x^{2}}2}{x^{4}}=\\dfrac14$。
【易错】$x-\\tan x$ 是三阶项、不参与二阶主项；$\\tan^{2}x\\sim x^{2}$ 的系数 1。
【注意】答案 $\\dfrac14$。""",
16: """【公式】根式反解：$t=\\sqrt{\\dfrac{1+x}{x}}\\Rightarrow x=\\dfrac{1}{t^{2}-1}$，$\\mathrm dx=\\dfrac{-2t}{(t^{2}-1)^{2}}\\,\\mathrm dt$。
【技巧】换元后 $\\ln(1+t)$ 保留、$\\dfrac{1}{\\mathrm e^{?}}$ 之类消失——分部一次把 $\\ln t$ 的导数 $\\dfrac1t$ 与 $\\dfrac{2t}{(t^{2}-1)^{2}}$ 相乘出有理分式。
【易错】$x\\to+\\infty$ 对应 $t\\to1^{+}$（下限）、$x\\to0^{+}$ 对应 $t\\to+\\infty$（上限）——方向翻转。
【注意】结果含 $\\ln t-\\dfrac{1}{2(t^{2}-1)}\\cdots$ 按数据解析回代 $t=\\sqrt{\\dfrac{1+x}{x}}$。""",
17: """【公式】链式：$z_x=f'_1+f'_2+yf'_3$、$z_y=f'_1-f'_2+xf'_3$；二阶逐项展开后按 $f''_{ij}$ 归并（$f'_{ij}=f'_{ji}$ 对称）。
【技巧】$\\dfrac{\\partial^{2}z}{\\partial x\\partial y}$：对 $z_x$ 的每一项再对 $y$ 求导——$f'_1,f'_2,f'_3$ 各自链式回三个中间变量，共 9 项后合并。
【易错】中间变量 $x+y,x-y,xy$ 的导数（$1,1,y$ 与 $1,-1,x$）；$f''_{33}$ 的 $xy$ 交叉项。
【注意】按 $f''_{11},f''_{22},f''_{33},f''_{12},f''_{13},f''_{23}$ 归类写全。""",
18: """【公式】可降阶：$p=y'$，$xp'-p=-2$（齐次线性）→ $\\dfrac{p}{x}$ 型：$\\left(\\dfrac px\\right)'=\\dfrac{2}{x^{2}}$ → $p=2+C_1x$。
【技巧】$y=C_1+2x+\\dfrac{C_2}{2}x^{2}$ 用"过原点"→ $C_1=0$；"切线斜率/所围条件"定 $C_2$。
【易错】$p=2$ 常数解与 $p=2+C_1x$ 通解的关系；初值条件对应哪个常数。
【注意】按数据解析：$y=2x+C_2x^{2}$ 代入面积条件定 $C_2$。""",
19: """【公式】平移+极坐标：$x=1+r\\cos\\theta,\\ y=1+r\\sin\\theta$，边界 $r\\le2(\\sin\\theta+\\cos\\theta)$；被积 $x-y=r(\\cos\\theta-\\sin\\theta)$。
【技巧】**平移对称秒杀**：令 $u=x-1,v=y-1$，圆域关于 $u,v$ 交换对称 → $\\displaystyle\\iint(u-v)=\\displaystyle\\iint(v-u)=-\\displaystyle\\iint(u-v)\\Rightarrow I=0$。
【易错】极坐标硬算也可（$w=\\theta-\\tfrac\\pi4$ 后被积函数为奇），但平移对称三行结束；别在极坐标里苦算。
【注意】答案 0。""",
20: """【公式】左段（$-\\pi<x<0$）：$y=-\\dfrac{x}{y'}\\Rightarrow yy'=-x\\Rightarrow\\dfrac{\\mathrm d(y^{2})}{\\mathrm dx}=-2x$ → $y^{2}=-x^{2}+C$，初值定 $C=\\pi^{2}$。
【技巧】右段曲率半径条件 → $y''+y+x=0$（$x\\ge0$）——曲率信息翻译成二阶线性非齐次方程；通解 $C_1\\cos x+C_2\\sin x-x$。
【易错】两段在 $x=0$ 处光滑连接（$y$ 值 $\\pi$、$y'$ 值连续）定右段常数 $C_1=\\pi$。
【注意】$y'(0)$ 由左段 $y'=-\\dfrac{x}{y}$ 在连接点算出。""",
21: """【公式】(I) 罗尔定理证明拉格朗日：构造 $\\varphi(x)=f(x)-f(a)-\\dfrac{f(b)-f(a)}{b-a}(x-a)$，$\\varphi(a)=\\varphi(b)=0$ → 存在 $\\xi$ 使 $\\varphi'(\\xi)=0$。
【技巧】(II) 用 (I)：对 $f(t)=\\displaystyle\\int_0^{t}?$ 型逐项用中值/介值，配合极限条件 $\\lim\\limits_{\\lambda\\to0}?$ 取 $\\lambda\\to0$ 传递。
【易错】辅助函数的构造来源（把要证的等式移项、对 $x$ 看成未知曲线的"差曲线"）；罗尔三条件（连续、可导、端点值相等）写全。
【注意】(I)(II) 的结论链：先中值定理、再用题给极限条件。""",
22: """【公式】递推非齐次 $A\\xi_{2}=\\xi_{1}$：增广 $(A,\\xi_1)$ 行变换，$r=2$ → 通解 = 特解 + $k\\cdot$基础解系。
【技巧】三问递推解 $A\\xi_2=\\xi_1$、$A\\xi_3=\\xi_2$、$A\\xi_4=\\xi_3$? 每层先核 $r(A)=r(A,\\xi_i)$ 存在性；自由常数并入特解写成统一形式。
【易错】$A$ 的秩（各行和为 0 → $(1,1,1)$ 是 $Ax=0$ 解 → ①基础解系 $(1,1,1)^{\\mathrm T}$）；下一层解的存在性要重新验证。
【注意】(II) 的解统一为 $\\xi_2=\\left(-\\dfrac12,-\\dfrac12,1\\right)^{\\mathrm T}+k_1(1,-1,? )$ 按数据解析核对。""",
23: """【公式】规范形 $y_2^{2}+y_3^{2}$（无 $y_1^{2}$ 项）→ $\\lambda=0$ 是 $A$ 的特征值 → $|0\\cdot E-A|=|{-A}|=0$ → 解出 $a$。
【技巧】$|{-A}|=(-1)^{3}|A|$，$|A|=$ 按第一行展开含 $a$ 的多项式 → 因式分解定 $a$（$a=0$ 与 $a=2$ 候选，再由惯性指数筛）。
【易错】规范形还规定正惯性指数 $=2$——两个候选都要数正特征值个数（$a=0$ 时 $2,-1,0$? 逐个核）。
【注意】$a=0$ 时 $A\\to$ 特征值 $0,1,2?$? 按数据解析：$a=0$ 时正惯性 2、$\\lambda=0$ 一个，规范形吻合。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2009数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2009数二真题.md', TIPS_2009)
