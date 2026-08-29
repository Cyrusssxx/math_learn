# -*- coding: utf-8 -*-
# 2006 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2006 = {
1: """【公式】水平渐近线：$\\lim\\limits_{x\\to\\infty}\\dfrac{x+4\\sin x}{5x-2\\cos x}=\\lim\\dfrac{1+4\\frac{\\sin x}{x}}{5-2\\frac{\\cos x}{x}}$。
【技巧】"无穷小 × 有界 = 无穷小"：$\\dfrac{\\sin x}{x}\\to0$、$\\dfrac{\\cos x}{x}\\to0$，振荡项自动熄灭。
【易错】$\\sin x$、$\\cos x$ 在 $\\infty$ 处无极限，但不能约掉 $x$ 后忘了它们有界——恰恰因为有界才趋于 0。
【注意】水平渐近线 $y=\\dfrac15$。""",
2: """【公式】连续补值：$f(0)=\\lim\\limits_{x\\to0}f(x)$；洛必达 + 变限积分求导 $\\left(\\displaystyle\\int_0^x\\sin t^{2}\\,\\mathrm dt\\right)'=\\sin x^{2}$。
【技巧】$\\dfrac{\\sin x^{2}}{x^{3}}\\sim\\dfrac{x^{2}}{x^{3}}=\\dfrac1x\\to\\infty$？——不，等价代换前先核对：实际 $\\sim\\dfrac{x^{2}}{x^{3}}$ 发散，用洛必达核对到底。
【易错】等价代换的精度：分母 $x^3$，分子 $\\sin t^{2}\\sim t^{2}$ 积出来是 $\\dfrac{x^{3}}{3}$，极限 $\\dfrac13$——不是 $\\infty$。
【注意】补值 $f(0)=\\dfrac13$。""",
3: """【公式】$\\displaystyle\\int\\frac{x\\,\\mathrm dx}{(1+x^{2})^{2}}$：凑 $\\mathrm d(1+x^{2})=2x\\,\\mathrm dx$，$\\displaystyle\\int\\frac{\\mathrm du}{u^{2}}=-\\dfrac1u$。
【技巧】偶函数被积、$x\\,\\mathrm dx$ 配 $1+x^{2}$——换元 $u=1+x^{2}$ 从 1 到 $+\\infty$。
【易错】$u\\to+\\infty$ 时 $-\\dfrac1u\\to0$（收敛），下限给出 $-(-1)=1$，乘 $\\tfrac12$。
【注意】答案 $\\dfrac12$。""",
4: """【公式】可分离：$\\dfrac{\\mathrm dy}{y}=\\dfrac{1-x}{x}\\,\\mathrm dx=\\left(\\dfrac1x-1\\right)\\mathrm dx$ → $\\ln|y|=\\ln|x|-x+C$。
【技巧】通解 $y=Cx\\mathrm e^{-x}$（写成正的 $C$ 即可，常数吸收符号与绝对值）。
【易错】$\\dfrac{1-x}{x}$ 拆成 $\\dfrac1x-1$ 两项分别积。
【注意】$y=Cx\\mathrm e^{-x}$。""",
5: """【公式】隐函数：$y=1-x\\mathrm e^{y}$ 两边对 $x$ 求导 $y'=\\dfrac{\\mathrm e^{y}}{1+x\\mathrm e^{y}}$? 更稳：$y'-\\mathrm e^{y}-x\\mathrm e^{y}y'=0$。
【技巧】先代 $x=0$ 定 $y(0)=1$，再代 $(0,1)$：$y'(0)-\\mathrm e=0$。
【易错】$x\\mathrm e^{y}$ 乘积求导（$x$ 与 $\\mathrm e^y$ 各导一次）；把 $\\left.\\dfrac{\\mathrm dy}{\\mathrm dx}\\right|_{x=0}$ 误当 $y$ 值。
【注意】答案 $-\\mathrm e$。""",
6: """【公式】$BA=B+2E\\Rightarrow B(A-E)=2E\\Rightarrow|B|\\cdot|A-E|=4$。
【技巧】$|A-E|=\\left|\\begin{smallmatrix}1&1\\\\-1&0\\end{smallmatrix}\\right|=1$ → $|B|=4$？核对：$A-E=\\begin{pmatrix}1&1\\\\-1&1\\end{pmatrix}$，$|A-E|=2$ → $|B|=2$。
【易错】$A-E$ 的元素（$A$ 减 $E$ 是对角减 1）；行列式 2×2 别算错。
【注意】答案 $|B|=2$。""",
7: """【公式】微分与增量的大小比较：$\\Delta y=\\mathrm dy+o(\\Delta x)$，凹函数（$f''>0$）时 $\\Delta y>\\mathrm dy$。
【技巧】几何直观：下凸曲线上，割线增量（$\\Delta y$，从曲线上走）高于切线增量（$\\mathrm dy$，沿切线走）。
【易错】$f'>0$ 与本题无关（单调性），别混入；凹凸性由 $f''>0$ 决定。
【注意】答案 A：$0<\\mathrm dy<\\Delta y$（$\\Delta x>0$）。""",
8: """【公式】奇函数在 $x=0$ 处若有定义且连续则 $f(0)=0$；第一类间断点 → $f(0^{\\pm})$ 存在但不等 → $f(0^+)=-f(0^-)\\ne0$。
【技巧】赋值法：取 $f(x)=\\begin{cases}1&x>0\\\\-1&x<0\\end{cases}$ 直接算 $\\displaystyle\\int_0^x f$ 的奇偶与可导性。
【易错】$\\displaystyle\\int_0^x f$ 在 $x=0$ 处：左导 = $f(0^-)=-1$、右导 = $f(0^+)=1$ → 不可导，但仍连续且是奇函数。
【注意】答案 B（连续的奇函数但不可导）。""",
9: """【公式】复合求导：$h'=\\mathrm e^{1+g}g'$ → $1=\\mathrm e^{1+g(1)}\\cdot2$ → $\\mathrm e^{1+g(1)}=\\dfrac12$。
【技巧】$\\ln$ 两边解出 $g(1)=\\ln\\dfrac12-1=-\\ln2-1$。
【易错】别把 $h'(1)=1$ 当成 $\\mathrm e^{1+g}=1$（丢了 $g'$ 的除法）。
【注意】答案 C。""",
10: """【公式】解 → 方程反推：$C_1\\mathrm e^{x}+C_2\\mathrm e^{-2x}$ → 特征根 $1,-2$ → $y''+y'-2y=0$；$x\\mathrm e^{x}$ 是右端 $\\sim$ 共振项（$1$ 为单根，乘 $x$）。
【技巧】非齐次项形如 $P\\mathrm e^{x}$：原方程右端 $=3\\mathrm e^{x}$ 型——把 $x\\mathrm e^x$ 代入 $(\\lambda+... )$ 验证。
【易错】特征多项式 $(\\lambda-1)(\\lambda+2)=\\lambda^{2}+\\lambda-2$ 的符号；共振乘 $x$ 的结构对应右端指数。
【注意】答案 B。""",
11: """【公式】极坐标 $\\theta\\in[0,\\tfrac\\pi4]$、$r\\in[0,1]$ 是圆心角 $45°$ 的扇形；直角坐标 $x\\ge0,y\\ge0,y\\le x$。
【技巧】交换积分次序 = 画扇形边界：$y$ 从 0 到 $\\dfrac{\\sqrt2}{2}x$ 与 $y$ 从 $\\dfrac{\\sqrt2}{2}x$ 到 $\\sqrt{1-x^{2}}$ 两段。
【易错】直线 $\\theta=\\tfrac\\pi4$ 即 $y=x$；圆弧 $r=1$ 即 $y=\\sqrt{1-x^{2}}$。
【注意】答案 C（分两段的直角坐标积分）。""",
12: """【公式】条件极值必要条件：$\\dfrac{f'_x}{f'_y}=\\dfrac{\\varphi'_x}{\\varphi'_y}$（$\\varphi'_y\\ne0$ 时由隐函数求导 $\\dfrac{\\mathrm dy}{\\mathrm dx}=-\\dfrac{\\varphi'_x}{\\varphi'_y}$ 代入一元极值）。
【技巧】不引入 $\\lambda$ 也能表达：$f'_x-\\dfrac{\\varphi'_x}{\\varphi'_y}f'_y=0$。
【易错】选项的差异在分母与符号——紧扣 $\\varphi'_y\\ne0$ 的题设条件写。
【注意】答案 D。""",
13: """【公式】部分组无关 → 整组无关的升维判别：延长分量（添 0 分量）保持无关；反之缩短不保。
【技巧】低维无关 ⇒ 高维（添分量）无关；整组 $s$ 个向量无关的"必要条件"类选项用维数与个数比判断。
【易错】"无关 ⇒ 任何部分组无关"是对的；反过来"部分无关 ⇒ 整组无关"只在升维场景成立。
【注意】答案 A。""",
14: """【公式】行/列变换 → 初等阵左/右乘：行加（第 2 行加到第 1 行）= 左乘 $P$；列变换（第 1 列 $-1$ 倍加到第 2 列）= 右乘 $Q$。
【技巧】$C=PAQ$ → $C^{-1}=A^{-1}$? 不，$P,Q$ 可逆 → $A=P^{-1}CQ^{-1}$，$A^{*}=C^{*}\\cdot$... 按选项组织：$BA=C$ 则 $B=CA^{-1}$ 型。
【易错】列变换对应的初等阵写在**右**边；$P^{-1}$ 与 $Q^{-1}$ 的位置。
【注意】答案 B。""",
15: """【公式】泰勒定参数：$\\mathrm e^{x}=1+x+\\dfrac{x^{2}}{2}+\\dfrac{x^{3}}{6}+o(x^{3})$ 代入后逐次方比较系数。
【技巧】"等式对任意 $x$ 成立" → 同次幂系数相等：$x$ 项 $A=1+B$，$x^{2}$ 项 $0=\\dfrac12+C$，$x^{3}$ 项 $0=\\dfrac16+\\dfrac B6$。
【易错】$o(x^{3})$ 不参与系数比较；三个未知数三个方程恰好定出 $A=\\dfrac13,B=-\\dfrac23,C=-\\dfrac12$。
【注意】洛必达逐次法作为方法 2 等价。""",
16: """【公式】$\\arcsin\\mathrm e^{x}$ 的换元：令 $t=\\arcsin\\mathrm e^{x}$（$x\\le0$），$\\mathrm e^{x}=\\sin t$；分部积分取 $\\mathrm dv=\\mathrm e^{-x}\\mathrm dx$。
【技巧】$\\dfrac{\\mathrm dx}{\\mathrm e^{x}}=-\\mathrm d(\\mathrm e^{-x})$，分部后剩 $\\displaystyle\\int\\mathrm e^{-x}\\cdot\\dfrac{\\mathrm e^{x}}{\\sqrt{1-\\mathrm e^{2x}}}\\,\\mathrm dx=\\displaystyle\\int\\dfrac{\\mathrm dx}{\\sqrt{1-\\mathrm e^{2x}}}$。
【易错】定义域 $x\\le0$；第二段再换元 $u=\\mathrm e^{-x}$：$\\displaystyle\\int-\\dfrac{\\mathrm du}{\\sqrt{u^{2}-1}}=-\\ln\\left(u+\\sqrt{u^{2}-1}\\right)$。
【注意】结果 $-\\mathrm e^{-x}\\arcsin\\mathrm e^{x}+\\ln\\left(\\mathrm e^{-x}+\\sqrt{\\mathrm e^{-2x}-1}\\right)+C$。""",
17: """【公式】区域关于 $x$ 轴对称 + 被积函数关于 $y$ 为奇 → 该部分积分为 0，只剩 $\\dfrac{x^{2}}{1+x^{2}+y^{2}}$ 项。
【技巧】对称性砍掉奇项后，$D$（右半单位圆）上用极坐标：$\\displaystyle\\int_{-\\pi/2}^{\\pi/2}\\mathrm d\\theta\\int_0^1\\dfrac{r^{3}}{1+r^{2}}\\,\\mathrm dr$。
【易错】$\\dfrac{xy}{1+x^{2}+y^{2}}$ 关于 $y$ 是奇（$x$ 固定时 $y\\mapsto-y$ 变号）——对称轴是 $x$ 轴不是 $y$ 轴。
【注意】结果 $\\dfrac{\\pi}{2}\\left(1-\\ln2\\right)$（$\\displaystyle\\int_0^1\\dfrac{r^{3}}{1+r^{2}}\\mathrm dr=\\dfrac12-r^{2}\\to\\dfrac12(1-\\ln2)$）。""",
18: """【公式】$0<x<\\pi$ 时 $0<\\sin x<x$ → 数列单调递减有下界 0 → 收敛；$x_{n+1}=\\sin x_n\\to0$（夹逼：$\\sin x\\sim x$ 但只需单调有界）。
【技巧】(II) 经典极限 $\\lim\\dfrac{x_{n+1}}{x_n^{3}}$：泰勒 $\\sin x=x-\\dfrac{x^{3}}{6}+o(x^{3})$ → $x_{n+1}=x_n-\\dfrac{x_n^{3}}{6}+\\cdots$，即 $\\lim\\left(\\dfrac{1}{x_{n+1}^{2}}-\\dfrac{1}{x_n^{2}}\\right)=\\dfrac13$（斯特森型）。
【易错】(II) 不能直接说 $\\dfrac{\\sin x-x}{x^{3}}\\to-\\dfrac16$ 就完——需要把倒数差配凑成该极限的累加和。
【注意】$\\lim\\left(\\dfrac1{x_{n+1}^{2}}-\\dfrac1{x_n^{2}}\\right)=\\dfrac13$。""",
19: """【公式】"对 $a<b$ 证 $g(b)>g(a)$" → 构造 $f(x)=x\\sin x+2\\cos x+\\pi x$ 证单调增：$f'(x)=\\sin x+x\\cos x-2\\sin x+\\pi=x\\cos x+\\pi-\\sin x$。
【技巧】$f'(x)>0$ 的证明：$\\pi-\\sin x>0$ 兜底，$x\\cos x$ 在 $(0,\\pi)$ 可负但 $x\\cos x\\ge-x>-\pi$? 精确：$\\cos x\\ge-1$ → $x\\cos x\\ge-x>-\\pi$，与 $\\pi-\\sin x\\ge\\pi-1$ 相加 $>0$。
【易错】别拆成两半各自粗放估计——合并写 $f'(x)=\\pi-\\sin x+x\\cos x>\\pi-1-x\\ge0$ 的推理要严谨（$x\\le\\pi$）。
【注意】单调增 + $a<b$ 直接得结论。""",
20: """【公式】径向函数链式：$z_x=f'\\cdot\\dfrac{x}{\\sqrt{x^{2}+y^{2}}}$、$z_y=f'\\cdot\\dfrac{y}{\\sqrt{x^{2}+y^{2}}}$，二阶再乘一次链式（注意 $\\left(\\dfrac{x}{r}\\right)'_x=\\dfrac{y^{2}}{r^{3}}$）。
【技巧】代入 $\\dfrac{\\partial^{2}z}{\\partial x^{2}}+\\dfrac{\\partial^{2}z}{\\partial y^{2}}$ 后 $\\dfrac{y^{2}+x^{2}}{r^{3}}=\\dfrac1r$ 自动归并 → 得 $f''-\\dfrac{f'}{r}=f$。
【易错】二阶项里 $\\left(\\dfrac{x}{r}\\right)'_x=\\dfrac{r^{2}-x^{2}}{r^{3}}=\\dfrac{y^{2}}{r^{3}}$（不是 $\\dfrac1r$ 的全导）。
【注意】方程化为 $f''-\\dfrac1r f'=f$，初值由 $f(1)=0$ 类条件定。""",
21: """【公式】参数曲线：$x'=2t$、$y'=4-2t$；$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{-2}{4t}=-\\dfrac1{2t}$。
【技巧】曲率、凸性、切线三问都用 $t$ 的符号分段（$t>0\\iff x>1$）；切点 $t=1$（对应 $x=2,y=3$? 由方程解）。
【易错】$t\\ge0$ 的定义域让 $x\\ge1$；二阶导分母 $x'=2t$ 在 $t=0$ 处退化点单独说明。
【注意】按 (I)(II)(III) 逐问套参数求导结论。""",
22: """【公式】含参非齐次方程组：无穷多解 $\\Leftrightarrow r(A)=r(\\bar A)<4$；行变换后按参数 $a,b$ 分类。
【技巧】从行阶梯形读秩：$a=2,b=1$? 按答案给的参数组合（两行成比例的情形）分类验证唯一解/无穷解。
【易错】分类讨论别漏"唯一解"分支；自由变量选择影响基础解系写法（答案不唯一）。
【注意】写出通解 = 特解 + $k\\times$基础解系（按各参数分支）。""",
23: """【公式】对称矩阵 + 行和均 3 → $\\xi=(1,1,1)^{\\mathrm T}$ 是 $A$ 的特征向量（特征值 3）；$A\\alpha_1=0\\Rightarrow\\lambda_1=0$（$\\alpha_1=(-1,2,-1)$）。
【技巧】实对称矩阵不同特征值的特征向量自动正交 → 由 $\\lambda=0,3$ 的向量**构造** $\\lambda=2$ 的特征向量（与 $\\alpha_1$ 正交，如 $(1,0,-1)^{\\mathrm T}$），再正交规范化。
【易错】"各行元素之和均为 3" $\\Leftrightarrow A(1,1,1)^{\\mathrm T}=3(1,1,1)^{\\mathrm T}$——这条翻译是全题钥匙；$A\\alpha=0$ 翻译成 $\\lambda=0$。
【注意】(2) $A^{100}\\xi=3^{100}\\xi$：对称阵正交相似于对角阵，$A^{100}=Q\\mathrm{diag}(0,3,3^{100})Q^{\\mathrm T}$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2006数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2006数二真题.md', TIPS_2006)
