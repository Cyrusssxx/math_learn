# -*- coding: utf-8 -*-
# 2008 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2008 = {
1: """【公式】罗尔定理：$f(0)=f(1)=f(2)=0$ → $f'$ 在 $(0,1)$、$(1,2)$ 内各有一零点。
【技巧】$x^{2}$ 因子让 $f'(0)=0$——多项式因式的重数直接给出导数零点；三种来源合计。
【易错】只数罗尔内点（2 个）漏掉 $x=0$；罗尔给"至少"，还要用 $f'$ 是二次多项式（至多 2 个非零零点+0）封顶。
【注意】$f'=4x^{3}-9x^{2}+4x$ 恰 3 个零点，答案 D。""",
2: """【公式】分部积分：$\\displaystyle\\int_0^{a}xf'(x)\\,\\mathrm dx=\\left[xf(x)\\right]_0^{a}-\\int_0^{a}f(x)\\,\\mathrm dx$。
【技巧】题目只给 $f$ 的图形不给表达式——$\\displaystyle\\int_0^{a}f$ 就是图形下的面积（从图上读），这是本题的标志性动作。
【易错】$xf(x)$ 在 $x=0$ 端的值：$0\\cdot f(0)=0$；图形端点值 $(a,f(a))=(2,0)$? 读图要准。
【注意】代入后化简出选项值（答案 C）。""",
3: """【公式】通解反推方程：$\\mathrm e^{x}$ → 根 1；$\\cos2x,\\sin2x$ → 共轭复根 $\\pm2\\mathrm i$；特征方程 $(\\lambda-1)(\\lambda^{2}+4)=\\lambda^{3}-\\lambda^{2}+4\\lambda-4$。
【技巧】实数通解里的 $\\cos\\omega x,\\sin\\omega x$ 成对出现 = 共轭复根 $\\pm\\omega\\mathrm i$；复根因子 $\\lambda^{2}+\\omega^{2}$。
【易错】展开 $(\\lambda-1)(\\lambda^{2}+4)$ 的 $-4\\lambda$ 与 $-4$ 常数项符号。
【注意】答案 D：$y'''+y''-? $——按展开式逐项对照选项。""",
4: """【公式】$\\lim\\limits_{x\\to0}x\\ln|x|=0$（幂函数压倒对数）→ $x=0$ 可去；$x\\to1$ 时 $\\ln|x|\\to\\pm\\infty$ 且 $|x-1|\\to0^{+}$ → 发散。
【技巧】两个间断点分开定性：$x=0$ 可去（补值即可连续）；$x=1$ 处左右都发散（无穷型第二类）。
【易错】$\\dfrac{\\sin x}{|x-1|}$ 在 $x\\to1$ 时 $\\to\\sin1\\ne0$；$\\ln|x|$ 左右同趋于 $-\\infty$（$\\ln|1\\mp h|$ 都 $\\to-\\infty$）。
【注意】答案 A（1 个可去 + 1 个无穷型）。""",
5: """【公式】复合收敛性辨析：$\\{x_n\\}$ 单调 + $f$ 同向单调 ⇒ $\\{f(x_n)\\}$ 单调，再配 $f$ 有界 → 单调有界定理给收敛。
【技巧】B 的链条完整（单调+有界），A 的断点：$f$ 不连续时 $\\lim f(x_n)\\ne f(\\lim x_n)$ 甚至极限不存在。
【易错】"单调有界"是 $\\{f(x_n)\\}$ 收敛的充分条件；$\\{x_n\\}$ 收敛推不出 $\\{f(x_n)\\}$ 收敛（$f$ 未必连续）。
【注意】答案 B。""",
6: """【公式】极坐标：$\\dfrac{f(\\sqrt{x^{2}+y^{2}})}{\\sqrt{x^{2}+y^{2}}}\\,\\mathrm dx\\,\\mathrm dy\\to f(r)\\,\\mathrm dr\\,\\mathrm d\\theta$（分母的 $r$ 与雅可比 $r$ 相消）。
【技巧】先积 $r$ 再积 $\\theta$：$F(u,v)=v\\displaystyle\\int_1^{u}f(r)\\,\\mathrm dr$（分离变量型）→ $\\dfrac{\\partial^{2}F}{\\partial u\\partial v}=f(u)$。
【易错】区域 $D_{uv}$ 的极坐标描述（$1\\le r\\le u$、$0\\le\\theta\\le v$）；求偏导的顺序不影响结果。
【注意】答案 A。""",
7: """【公式】幂零阵：$A^{3}=O\\Rightarrow(E-A)(E+A+A^{2})=E-A^{3}=E$、$(E+A)(E-A+A^{2})=E+A^{3}=E$——$E\\pm A$ 都可逆。
【技巧】$1-a^{3}=(1-a)(1+a+a^{2})$、$1+a^{3}=(1+a)(1-a+a^{2})$ 两个代数恒等式的矩阵版一起用。
【易错】只验证一个方向的逆；"$A$ 非零"排除 $A=O$ 的平凡情形（此时 $A^{3}=O$ 平凡）。
【注意】答案 C。""",
8: """【公式】实对称矩阵合同 $\\Leftrightarrow$ 正、负惯性指数相同；实对称 + 相同特征多项式 → 既相似又合同。
【技巧】$A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}$ 特征值 $3,-1$（正负惯性各 1）→ 找特征值同为 $3,-1$ 的选项（$D=\\begin{pmatrix}1&-2\\\\-2&1\\end{pmatrix}$）。
【易错】合同不必相似（$P^{\\mathrm T}AP=D$ 的 $P$ 非正交时特征值可变）；只比正负惯性个数。
【注意】答案 D。""",
9: """【公式】无穷小链：$1-\\cos u\\sim\\dfrac{u^{2}}{2}$、$\\mathrm e^{x^{2}}-1\\sim x^{2}$ → 原式 $\\sim\\dfrac{x^{2}f^{2}(x)/2}{x^{2}f(x)}=\\dfrac{f(x)}{2}\\to\\dfrac{f(0)}{2}=1$。
【技巧】$f$ 连续 → 极限处的 $f(x)$ 直接写 $f(0)$。
【易错】系数 $\\dfrac12$ 别丢；$\\cos[xf(x)]$ 的 $u=xf(x)\\to0$ 需要说明（$f$ 连续有界）。
【注意】$f(0)=2$。""",
10: """【公式】一阶线性 $y'-\\dfrac yx=x\\mathrm e^{-x}$，积分因子 $\\dfrac1x$：$\\left(\\dfrac yx\\right)'=\\mathrm e^{-x}$。
【技巧】$\\left(\\dfrac yx\\right)'=\\dfrac{y'x-y}{x^{2}}$ 的识别（方程左边恰好是这个）；$\\displaystyle\\int\\mathrm e^{-x}\\,\\mathrm dx=-\\mathrm e^{-x}$ 的负号是本题唯一陷阱。
【易错】$\\int\\mathrm e^{-x}\\,\\mathrm dx$ 写成 $+\\mathrm e^{-x}$ 就整体变号——正确通解 $y=x\\left(C-\\mathrm e^{-x}\\right)$。
【注意】通解 $y=x\\left(C-\\mathrm e^{-x}\\right)$（$C$ 任意；已代回验证）。""",
11: """【公式】隐函数：$F_x=y\\cos(xy)+\\dfrac{-1}{y-x}-1$，$F_y=x\\cos(xy)+\\dfrac{1}{y-x}$，$y'=-\\dfrac{F_x}{F_y}$。
【技巧】代 $(0,1)$：$F_x=1\\cdot1-1-1=-1$、$F_y=0+1=1$ → $y'=1$。
【易错】$\\ln(y-x)$ 对 $x$ 求导 $\\dfrac{-1}{y-x}$（链式负号）；对 $y$ 求导 $\\dfrac{1}{y-x}$。
【注意】切线 $y=x+1$。""",
12: """【公式】$y=x^{5/3}-5x^{2/3}$：$y''=\\dfrac{10}{9}x^{-4/3}(x+1)$——分母 $x^{4/3}>0$ 恒正，变号只看 $(x+1)$。
【技巧】$x=0$ 处 $y''$ 不存在但两侧同正 → 不是拐点；$x=-1$ 处变号 → 拐点 $(-1,-6)$。
【易错】实数分数幂 $(-1)^{1/3}=-1$、$(-1)^{2/3}=1$（按 $\\sqrt[3]{x}$ 理解）；$y''$ 不存在的点也要检验是否变号。
【注意】拐点 $(-1,-6)$。""",
13: """【公式】对数化：$\\ln z=\\dfrac xy\\ln\\dfrac yx$，$z_x=z\\cdot\\dfrac1y\\left(\\ln\\dfrac yx-1\\right)$。
【技巧】代点 $(1,2)$：$z=2^{1/2}=\\sqrt2$、$\\ln\\dfrac yx=\\ln2$ → $z_x=\\sqrt2\\cdot\\dfrac12(\\ln2-1)$。
【易错】$\\dfrac{\\partial}{\\partial x}\\left(\\dfrac xy\\ln\\dfrac yx\\right)=\\dfrac1y\\ln\\dfrac yx+\\dfrac xy\\cdot\\left(-\\dfrac1x\\right)$ 的第二项。
【注意】答案 $\\dfrac{\\sqrt2}{2}(\\ln2-1)$。""",
14: """【公式】$|kA|=k^{n}|A|$（$n$ 阶）；特征值之积 $=|A|$。
【技巧】接力：$|2A|=8|A|=-48\\Rightarrow|A|=-6$ → $2\\cdot3\\cdot\\lambda=-6$ → $\\lambda=-1$。
【易错】$2^{3}=8$（3 阶矩阵）；$\\lambda$ 的符号（负数）。
【注意】$\\lambda=-1$。""",
15: """【公式】$u-\\sin u\\sim\\dfrac{u^{3}}{6}$（$u\\to0$）——把 $u=\\sin x$ 整体代入：$\\sin x-\\sin(\\sin x)\\sim\\dfrac{\\sin^{3}x}{6}$。
【技巧】嵌套三角别反复泰勒，"整体代入"一步到位；整体 $\\sim\\dfrac{\\sin^{4}x}{6x^{4}}\\to\\dfrac16$。
【易错】方向：分子是 $\\sin x-\\sin(\\sin x)$（大减小）；分母 $x^{4}$ 与 $\\sin x\\sim x$ 配平。
【注意】答案 $\\dfrac16$。""",
16: """【公式】先解 $x(t)$：$\\mathrm e^{x}\\,\\mathrm dx=2t\\,\\mathrm dt\\Rightarrow\\mathrm e^{x}=t^{2}+1$，即 $x=\\ln(1+t^{2})$。
【技巧】$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{2t\\ln(1+t^{2})}{2t/(1+t^{2})}=\\dfrac{\\mathrm dy/\\mathrm dt}{\\mathrm dx/\\mathrm dt}$——先由变限积分得 $y'_t=2t\\ln(1+t^{2})$，$x'_t=\\dfrac{2t}{1+t^{2}}$。
【易错】$x'_t$ 是复合 $\\ln(1+t^{2})$ 的导数 $\\dfrac{2t}{1+t^{2}}$（不是 $2t$）。
【注意】题目所求 $\\dfrac{\\mathrm dy}{\\mathrm dx}=\\ln(1+t^{2})$（恰好干净）。""",
17: """【公式】$x=\\sin t$：$\\displaystyle\\int_0^{\\pi/2}t\\sin^{2}t\\,\\mathrm dt=\\dfrac12\\int_0^{\\pi/2}t(1-\\cos2t)\\,\\mathrm dt$。
【技巧】$\\displaystyle\\int t\\cos2t\\,\\mathrm dt$ 分部一次：$=\\left[\\dfrac{t\\sin2t}{2}\\right]_0^{\\pi/2}-\\displaystyle\\int\\dfrac{\\sin2t}{2}\\,\\mathrm dt$（边界项为 0，剩 $+\\dfrac14\\cos2t\\Big|_0^{\\pi/2}$ 的负贡献）。
【易错】分部符号与 $\\cos2t$ 在两端点的值（$-1,1$）；反常性由 $x\\to1$ 的分母处理（换元后自动消失）。
【注意】结果 $\\dfrac{\\pi^{2}}{16}+\\dfrac14$。""",
18: """【公式】分块：曲线 $xy=1$ 把 $D=[0,\\tfrac12]\\times[0,2]$ 分成 $xy\\le1$（$\\max=1$）与 $xy>1$（$\\max=xy$）。
【技巧】"借整体算补块"：$\\max$ 的积分 = 1×整块面积（大块）+ 分离出的 $\\displaystyle\\iint_{xy>1}(xy-1)\\,\\mathrm dx\\,\\mathrm dy$ 修正项。
【易错】$xy=1$ 与边界的交点（$x=\\tfrac12, y=2$）；小三角区域的积分限（$\\tfrac1y\\le x\\le\\tfrac12$）。
【注意】按数据解析的分块结果核对（$19/4+\\ln2$ 型）。""",
19: """【公式】题设 $S(t)=tf^{2}(t)$ 与公式 $S=2\\pi\\displaystyle\\int_0^t f\\sqrt{1+f'^{2}}\\,\\mathrm dx$、$V=\\pi\\displaystyle\\int_0^t f^{2}\\,\\mathrm dx$ 两边对 $t$ 求导后相除消元。
【技巧】$2\\pi f\\sqrt{1+f'^{2}}=f^{2}+2tf f'\\cdot$? 逐项求导后约 $f$，整理成 $\\dfrac{f'}{f}$ 的可分离方程 → $f=\\dfrac{1}{\\pi x+1}$（用 $f(0)=1$）。
【易错】求导时的乘积法则（右端 $tf^{2}$ 是乘积）；$\\sqrt{1+f'^{2}}$ 的平方去根号。
【注意】结果 $f(x)=\\dfrac{1}{\\pi x+1}$。""",
20: """【公式】(I) 标准介值路线：$m\\le f\\le M$ → $m(b-a)\\le\\displaystyle\\int_a^b f\\le M(b-a)$ → $m\\le\\dfrac1{b-a}\\int_a^b f\\le M$ → 连续函数介值定理取 $\\eta$。
【技巧】替代路线：$F(x)=\\displaystyle\\int_a^x f$ 用拉格朗日中值定理（$F$ 可导且 $F'=f$ 连续），$\\eta=F'(\\xi)=\\dfrac{F(b)-F(a)}{b-a}$。
【易错】(I) 是 (II) 的工具：把 (II) 的变限积分套 (I)，$\\eta$ 依赖于 $x$ 后再取极限。
【注意】介值定理与罗尔两条路线都要会。""",
21: """【公式】双约束拉格朗日，或消元：$z=x^{2}+y^{2}$ 且 $x+y+z=4$ → $(x+\\tfrac12)^{2}+(y+\\tfrac12)^{2}=\\dfrac92$（圆）。
【技巧】目标 $u=x^{2}+y^{2}+z^{2}=z^{2}+z$（用约束 1）——只差一个 $z$：由 $x+y=4-z$、$x^{2}+y^{2}=z$ 得 $(x-y)^{2}=10z-z^{2}-16\\ge0$ → $z\\in[2,8]$ → $u\\in[6,72]$。
【易错】判别式 $\\ge0$ 给出 $z$ 的范围（这一步是本题巧劲）；$u=z^{2}+z$ 在 $z\\ge2$ 单调增。
【注意】最小 6（$z=2$），最大 72（$z=8$）。""",
22: """【公式】三对角行列式递推：$D_n=(2a)D_{n-1}-a^{2}D_{n-2}$，$D_1=2a,D_2=3a^{2}$ → $D_n=(n+1)a^{n}$。
【技巧】(II) $a=1$ 时行变换：$r(A)=r(\\bar A)=n-1$ → 无穷多解；通解 = 特解 + $k\\times(1,-2,1,0,\\cdots)^{\\mathrm T}$ 型。
【易错】递推归纳要两步初值；$a\\ne0$ 且 $a\\ne1$ 时唯一解（零解）；$a=0$ 时……分类全覆盖。
【注意】按数据解析的参数分支写全（$a=1$ 时自由变量 1 个）。""",
23: """【公式】特征向量的像逐项作用：$A\\alpha_1=-\\alpha_1$（$\\lambda=-1$）、$A\\alpha_2=\\alpha_2$（$\\lambda=1$）、$A\\alpha_3=A(\\alpha_1+\\alpha_2)=-\\alpha_1+\\alpha_2$。
【技巧】$A\\beta=A(\\alpha_1+\\alpha_2+\\alpha_3)=-2\\alpha_1+2\\alpha_2$——全部翻译回 $\\alpha_1,\\alpha_2$ 表示。
【易错】$\\alpha_3$ 不是特征向量（它是两不同特征值特征向量之和）；$\\alpha_1,\\alpha_2$ 无关保证表示唯一。
【注意】$A\\beta=-2\\alpha_1+2\\alpha_2$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2008数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2008数二真题.md', TIPS_2008)
