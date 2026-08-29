# -*- coding: utf-8 -*-
# 2004 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2004 = {
1: """【公式】含参极限定函数：$x\\ne0$ 时 $f(x)=\\dfrac{(1-1/n)x}{x^{2}+1/n}\\to\\dfrac{1}{x}$；$x=0$ 时 $f(0)=0$。
【技巧】按 $x$ 取值分情况求极限（$x=0$ 直接代；$x\\ne0$ 约去 $n$ 的干扰项）。
【易错】$x\\ne0$ 时别把 $f(x)$ 算成常数——是 $\\dfrac1x$；$f(0)$ 是 0 不是 $\\infty$。
【注意】$x=0$ 处 $\\lim f=\\infty\\ne f(0)$，为无穷间断点（第二类）。""",
2: """【公式】参数二阶导：$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{y''(t)}{x'(t)^{3}}$；上凸 $\\Leftrightarrow$ 二阶导 $<0$。
【技巧】$x'=3t^{2}+3>0$ 恒正 → $t$ 与 $x$ 同增，$t<0$ 直接翻译成 $x$ 的范围；$y''=6t$。
【易错】凸性看二阶导**符号**，不是凹凸函数定义死抠；$x=t^{3}+3t+1$ 严格增保证区间不反。
【注意】答案 $(-\\infty,1]$（$t\\le0\\iff x\\le1$）。""",
3: """【公式】$x=\\sec t$：$\\sqrt{x^{2}-1}=\\tan t$，$\\mathrm dx=\\sec t\\tan t\\,\\mathrm dt$；或倒代换 $x=\\dfrac1t$。
【技巧】见 $\\sqrt{x^{2}-1}$ 就想 $\\sec$；积分限 $x:1\\to+\\infty$ 映射 $t:0\\to\\dfrac{\\pi}{2}$。
【易错】被积函数约分后剩 $\\mathrm dt$（分子分母的 $\\tan t$ 恰好消掉）。
【注意】答案 $\\dfrac{\\pi}{2}$。""",
4: """【公式】隐函数偏导（$z$ 在指数上）：$\\dfrac{\\partial z}{\\partial x}=\\dfrac{2\\mathrm e^{2x-3z}}{1+3\\mathrm e^{2x-3z}}$，$\\dfrac{\\partial z}{\\partial y}=\\dfrac{\\mathrm e^{2x-3z}}{1+3\\mathrm e^{2x-3z}}$。
【技巧】组合 $3z_x+z_y$ 先通分再代回 $\\mathrm e^{2x-3z}=z-2y$（原方程）化简——代回是本题点睛之笔。
【易错】$-3z$ 对 $x$、对 $y$ 求导都出 $-3z'$ 链式项，分母 $1+3\\mathrm e^{2x-3z}$ 别漏。
【注意】答案 2。""",
5: """【公式】整理成 $y'-\\dfrac{y}{2x}=\\dfrac{x^{2}}{2}$，积分因子 $x^{-1/2}$：$\\left(yx^{-1/2}\\right)'=\\dfrac12x^{3/2}$。
【技巧】一阶线性标准流程：标准化 → 积分因子 → 通解 → 初值定 $C$。
【易错】$\\dfrac{y}{2x}$ 移项变负号；$y(1)=\\dfrac65$ 代入求 $C=\\dfrac15$。
【注意】特解 $y=\\dfrac{x^{3}}{5}+\\sqrt{x}$。""",
6: """【公式】$A^{*}A=|A|E$；方程右乘 $A$ 化简后 $|A|\\,(A-2E)B=A$，取行列式 $|B|=\\dfrac{|A|}{|A|^{3}}\\cdot\\dfrac{|A|}{|A-2E|}$ 型。
【技巧】见 $A^{*}$ 先右乘 $A$（或左乘）转化为 $|A|E$；求 $|B|$ 走行列式方程，不硬解 $B$。
【易错】$|A^{*}|=|A|^{n-1}=|A|^{2}$；$|A|=3$（分块对角 $\\begin{vmatrix}2&1\\\\1&2\\end{vmatrix}\\cdot1=3$）、$|A-2E|=1$。
【注意】答案 $|B|=\\dfrac19$。""",
7: """【公式】变限无穷小比阶：直接对上限求导（洛必达）——$\\beta'=\\tan(x^{2})\\cdot2x\\sim2x^{3}\\Rightarrow\\beta\\sim\\tfrac{2}{3}x^{3}$；$\\gamma'=\\dfrac{\\sin x^{3/2}}{2\\sqrt x}\\sim\\dfrac{x}{2}$。
【技巧】$\\alpha'=\\cos x^{2}\\to1\\Rightarrow\\alpha\\sim x$；三个都化成 $x$ 的幂次排序（$\\alpha<\\gamma<\\beta$）。
【易错】上限是 $x^{2}$、$\\sqrt x$ 的链式因子（$2x$、$\\dfrac{1}{2\\sqrt x}$）别丢；$\\tan\\sqrt t\\sim\\sqrt t$、$\\sin t^{3}\\sim t^{3}$ 先等价再积。
【注意】"从低阶到高阶"排 $\\alpha,\\gamma,\\beta$（答案 B）。""",
8: """【公式】绝对值函数：$f=|x(1-x)|$ 在 $(0,1)$ 内 $=x(1-x)$、两侧 $=-(x(1-x))$；符号切换点 $x=0,1$。
【技巧】$x=0$ 附近左、右二阶导为 $+2$、$-2$ 变号 → 既是极小值点又是拐点；画 $y=x(1-x)$ 翻折图一眼看穿。
【易错】$x=1$ 同样是极小+拐点；别以为零点是极值就一定不是拐点——绝对值翻折处二阶导必变号。
【注意】答案 C。""",
9: """【公式】$\\ln\\sqrt[n]{\\prod_{k=1}^{n}(1+k/n)^{2}}=\\dfrac{2}{n}\\sum\\ln(1+k/n)\\to2\\displaystyle\\int_0^{1}\\ln(1+x)\\,\\mathrm dx$。
【技巧】连乘开 $n$ 次方根 = 对数化成黎曼和；$\\displaystyle\\int\\ln(1+x)\\,\\mathrm dx=(1+x)\\ln(1+x)-(1+x)+C$。
【易错】系数是 $\\dfrac{2}{n}$（平方给的）；$\\dfrac1n\\to\\mathrm dx$ 换元 $x=\\dfrac{k}{n}$。
【注意】$2(2\\ln2-1)=4\\ln2-2$（答案 B）。""",
10: """【公式】导数定义单侧解读：$f'(0)=\\lim\\limits_{x\\to0^{+}}\\dfrac{f(x)-f(0)}{x}>0\\Rightarrow$ 存在 $\\delta$，$x\\in(0,\\delta)$ 时 $f(x)>f(0)$。
【技巧】"一点导数为正" ≠ 邻域单调——单点信息只保证"局部偏高"，C 是唯一站得住的。
【易错】A/B 的"邻域单调"需要 $f'$ 在区间上为正（题给只是一点）；D 的左侧 $x<0$ 除法变号 → $f(x)<f(0)$。
【注意】反例模型：$f(x)=x+2x^{2}\\sin(1/x)$ 在 $0$ 处导数为正但任意邻域内不单调。""",
11: """【公式】特征根 $\\pm\\mathrm i$；右端 $x^{2}+1$ 设 $ax^{2}+bx+c$，右端 $\\sin x$ 因 $\\pm\\mathrm i$ 是特征根必须乘 $x$：$x(A\\sin x+B\\cos x)$。
【技巧】叠加原理分两类右端各设各的；共振项（$\\pm\\mathrm i$ 对应 $\\sin/\\cos$）务必乘 $x$ 且 $\\sin,\\cos$ 成对。
【易错】只设 $Cx\\sin x$ 不带 $\\cos$ 项是典型错误——方程对 $\\cos x$ 的作用同样共振。
【注意】答案 A。""",
12: """【公式】$D:\\ x^{2}+y^{2}\\le2y$ 即 $r\\le2\\sin\\theta$（圆心 $(0,1)$、半径 1 的圆在极坐标下的表达）；面积元 $r\\,\\mathrm dr\\,\\mathrm d\\theta$，$\\theta\\in[0,\\pi]$。
【技巧】圆在 $y$ 正半轴 → $\\sin\\theta$（在 $x$ 正半轴才是 $\\cos\\theta$）；平移圆心 $y_0=c$ → $r=2c\\sin\\theta$。
【易错】四个选项的差异就在 $r$ 上限与被积表达——$x=r\\cos\\theta,y=r\\sin\\theta$ 逐项对号，别混用。
【注意】答案 D。""",
13: """【公式】列变换 = 右乘初等阵：交换 1、2 列 → $E_{12}$；第 2 列加到第 3 列 → $\\begin{pmatrix}1&0&0\\\\0&1&1\\\\0&0&1\\end{pmatrix}$；$C=AE_{12}E_{23}$，$Q=E_{12}E_{23}$。
【技巧】"行左列右"口诀：行变换左乘、列变换右乘；Q 就是两个初等阵按操作顺序相乘。
【易错】列加法初等阵的非零元位置（$E$ 的第 2 行第 3 列为 1）；两阵相乘的顺序（先做的在左）。
【注意】答案 D。""",
14: """【公式】$AB=O\\Rightarrow r(A)+r(B)\\le n$（$n$ 为 $A$ 的列数 = $B$ 的行数）；$B\\ne O\\Rightarrow Ax=0$ 有非零解 $\\Rightarrow r(A)<n$。
【技巧】双向推理一次配齐：$B$ 非零列给出 $A$ 列相关；$A$ 非零给出 $r(A)\\ge1$ → $r(B)\\le n-1$ → $B$ 行相关。
【易错】B、C 选项偷换"方阵"特例——题设是"任意两个非零矩阵"（不必方阵），用特殊例推翻不了普遍结论。
【注意】答案 A（A 列相关 + B 行相关）。""",
15: """【公式】$1^{\\infty}$ 型：$\\left(\\dfrac{2+\\cos x}{3}\\right)^{x}=\\mathrm e^{x\\ln\\frac{2+\\cos x}{3}}$，$\\ln\\dfrac{2+\\cos x}{3}=\\ln\\left(1+\\dfrac{\\cos x-1}{3}\\right)\\sim\\dfrac{\\cos x-1}{3}\\sim-\\dfrac{x^{2}}{6}$。
【技巧】指数部分 $x\\cdot(-\\dfrac{x^{2}}{6})=-\\dfrac{x^{3}}{6}$，再 $\\dfrac{\\mathrm e^{-x^{3}/6}-1}{x^{3}}\\sim-\\dfrac16$——两次等价连环。
【易错】$\\cos x-1\\sim-\\dfrac{x^{2}}{2}$ 除以 3 后是 $-\\dfrac{x^{2}}{6}$；"指数差 −1 → 除以 $x^{3}$"的等价 $\\mathrm e^{u}-1\\sim u$。
【注意】答案 $-\\dfrac16$。""",
16: """【公式】关系式延拓：$-2\\le x<0$ 时 $x+2\\in[0,2)$ → $f(x)=k(x+2)((x+2)^{2}-4)=k(x+2)x(x+4)$。
【技巧】(2) 图形与 $x$ 轴围面积：分三段（$[-2,0]$、$[0,2]$、$[2,k+2]$）逐段积分，$x=2$ 与 $x=k+2$ 处函数值为 0 是分段依据。
【易错】$k<0$（$k=-2$ 时抛物线开口翻转）影响第三段的积分方向——绝对值处理。
【注意】$\\left(x^{2}+4x\\right)$ 的因式分解让零点位置一目了然（$x=0,-2,-4$）。""",
17: """【公式】周期性：$f(x+\\pi)=\\displaystyle\\int_{x+\\pi}^{x+3\\pi/2}|\\sin t|\\,\\mathrm dt\\xlongequal{t=u+\\pi}f(x)$（$|\\sin(u+\\pi)|=|\\sin u|$）。
【技巧】值域只看 $[0,\\pi]$：$f(x)=\\cos x+\\sin x=\\sqrt2\\sin\\left(x+\\tfrac\\pi4\\right)$（分段去绝对值后），$f'(x)=0$ 找内部极值，端点 $f(0)=f(\\pi)=1$。
【易错】绝对值分段积分时 $[x,\\tfrac\\pi2]$、$[\\tfrac\\pi2,x+\\tfrac\\pi2]$ 两段的符号；周期函数最值在一个周期内找。
【注意】值域 $[2-\\sqrt2,\\sqrt2]$。""",
18: """【公式】旋成体侧面积：$S=2\\pi\\displaystyle\\int_0^{t}y\\sqrt{1+y'^{2}}\\,\\mathrm dx=\\pi\\int_0^{t}(\\mathrm e^{x}+\\mathrm e^{-x})\\,\\mathrm dx=2\\pi\\sinh t$（$y=\\cosh x$ 时 $y\\sqrt{1+y'^{2}}=y^{2}$）。
【技巧】$y=\\cosh x$、$y'=\\sinh x$、$1+\\sinh^{2}=\\cosh^{2}$——双曲函数恒等式让侧面积被积函数自动开干净。
【易错】$V=\\pi\\int y^{2}\\,\\mathrm dx$ 与侧面积公式别混；$\\cosh^{2}-\\sinh^{2}=1$。
【注意】$V:S=\\dfrac{\\pi(\\sinh t\\cosh t+ t)}{2\\pi\\sinh t}$，$t\\to\\infty$ 比值 → $\\dfrac12$。""",
19: """【公式】拉格朗日：$\\dfrac{\\ln^{2}b-\\ln^{2}a}{b-a}=\\dfrac{2\\ln\\xi}{\\xi}$，$e<a<\\xi<b<\\mathrm e^{2}$。
【技巧】$g(x)=\\dfrac{\\ln x}{x}$ 在 $(\\mathrm e,\\mathrm e^{2})$ 单调递减（$g'=\\dfrac{1-\\ln x}{x^{2}}<0$）→ $\\dfrac{2\\ln\\xi}{\\xi}>g(\\mathrm e^{2})=\\dfrac{4}{\\mathrm e^{2}}$，下界取在右端点。
【易错】单调递减函数的下界在右端点（不是左端点）；严格不等号来自 $\\xi<\\mathrm e^{2}$。
【注意】备选法：构造 $\\varphi(x)=\\ln^{2}x-\\dfrac{4}{\\mathrm e^{2}}x$ 求导看单调。""",
20: """【公式】牛顿第二定律：$m\\dfrac{\\mathrm dv}{\\mathrm dt}=-kv^{2}$；链式 $\\dfrac{\\mathrm dv}{\\mathrm dt}=v\\dfrac{\\mathrm dv}{\\mathrm dx}$ 直接得位移—速度关系 $\\dfrac{m\\,\\mathrm dv}{v}=-k\\,\\mathrm dx$。
【技巧】求"最长滑行距离" = $t\\to\\infty$ 的 $x$ 极限 $=\\dfrac{mv_0}{k}$——不必解出 $x(t)$ 再极限，对 $v$ 积分一次到位。
【易错】单位换算 $700\\,\\mathrm{km/h}=\\dfrac{175}{0.9}\\,\\mathrm{m/s}$；$k$ 由"前 60 秒滑行 $d$"的条件定。
【注意】答案 1.05 km。""",
21: """【公式】链式法则：$z_x=2x f_1'+y\\mathrm e^{xy}f_2'$，$z_y=-2y f_1'+x\\mathrm e^{xy}f_2'$；二阶混合偏导 $f_{12}'=f_{21}'$。
【技巧】每个二阶项逐因子展开（$f_1'$ 对 $x$ 又链式回两个中间变量），项数多但机械——按 $f_{11},f_{12},f_{22}$ 分组不易漏。
【易错】$\\mathrm e^{xy}$ 对 $x$ 求导出 $y\\mathrm e^{xy}$、对 $y$ 出 $x\\mathrm e^{xy}$；二阶乘积求导用莱布尼茨。
【注意】最终按 $f_{11},f_{12},f_{22}$ 三类合并同类项。""",
22: """【公式】含参齐次方程组分类：$a=0$ 时 $r(A)=2$ → 基础解系 2 个向量；$a\\ne0$ 且 $a\\ne-4$ 时 $r(A)=n$ 仅零解；$a=-4$ 时 $r(A)=n-1$。
【技巧】系数矩阵行变换时把首列 $a$ 的行除出去之前先提公因子；基础解系向量有"和向量"特征 $(1,2,\\cdots,n)^{\\mathrm T}$。
【易错】$a=-4$ 与 $a=0$ 是两个不同临界，各自的基础解系形态不同；漏掉任一分类即扣分。
【注意】$a=-4$ 时通解 $x=k(1,2,3,4)^{\\mathrm T}$。""",
23: """【公式】特征方程有二重根：$|\\lambda E-A|=0$ 的重根 λ₀ 额外要求 $r(\\lambda_0E-A)=n-\\text{重数}$ 才可对角化。
【技巧】特征多项式对 $a$ 分两种：$\\lambda=2$ 为二重根（定 $a=-2$，此时三个特征向量齐 → 可对角化）与 $\\lambda=4$ 为二重根（定 $a=-\\tfrac23$，$r(4E-A)=2\\ne1$ → 不可对角化）。
【易错】两种二重根情形都要讨论（漏一种就是一半分）；"不可对角化"的依据是秩条件而非直接断言。
【注意】结论：$a=-2$ 可对角化；$a=-\\tfrac23$ 不可对角化。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2004数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2004数二真题.md', TIPS_2004)
