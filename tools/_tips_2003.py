# -*- coding: utf-8 -*-
# 2003 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2003 = {
1: """【公式】$(1+u)^{\\alpha}-1\\sim\\alpha u$（$u\\to0$）→ $(1-ax^{2})^{\\frac14}-1\\sim-\\dfrac{ax^{2}}4$；$x\\sin x\\sim x^{2}$。
【技巧】等价定参数 = 两边同阶后比系数。
【易错】$\\alpha=\\tfrac14$ 且 $u=-ax^{2}$ 带符号——$-\\dfrac{a}4$ 别丢负号。
【注意】$-\\dfrac a4=1\\Rightarrow a=-4$。""",
2: """【公式】隐函数两边求导：$y+xy'+\\dfrac2x=4y^{3}y'$。
【技巧】先验证点 $(1,1)$ 在曲线上（$1+0=1$ ✓）再代值求 $y'$。
【易错】$(xy)'=y+xy'$ 乘积法则；$2\\ln x$ 的导数是 $\\dfrac2x$。
【注意】$y'(1)=1$，切线 $y=x$。""",
3: """【公式】$2^{x}=\\mathrm e^{x\\ln2}=\\displaystyle\\sum_{n\\ge0}\\frac{(x\\ln2)^{n}}{n!}$——指数型幂函数直接"落指数"。
【技巧】$x^{n}$ 项系数 = $\\dfrac{f^{(n)}(0)}{n!}$，两问一个来源。
【易错】系数是 $\\dfrac{(\\ln2)^{n}}{n!}$，$f^{(n)}(0)=(\\ln2)^{n}$ 是导数值——题目问的是"系数"。
【注意】麦克劳林在 $\\mathbb R$ 上处处收敛。""",
4: """【公式】极坐标面积 $S=\\dfrac12\\displaystyle\\int_{\\alpha}^{\\beta}\\rho^{2}\\,\\mathrm d\\theta=\\dfrac12\\int_0^{2\\pi}\\mathrm e^{2a\\theta}\\,\\mathrm d\\theta$。
【技巧】$\\rho^{2}=\\mathrm e^{2a\\theta}$（平方=指数翻倍），一整圈一段积完。
【易错】$\\mathrm e^{2a\\theta}$ 的原函数 $\\dfrac{1}{2a}\\mathrm e^{2a\\theta}$；上下限代入后 $\\mathrm e^{4\\pi a}-1$ 再除 $4a$。
【注意】答案 $\\dfrac{\\mathrm e^{4\\pi a}-1}{4a}$。""",
5: """【公式】$\\alpha\\alpha^{\\mathrm T}$ 秩 1 = 列 × 行；$\\alpha^{\\mathrm T}\\alpha=\\operatorname{tr}(\\alpha\\alpha^{\\mathrm T})$=对角元之和。
【技巧】由第一行 $(1,-1,1)$ 读出 $\\alpha^{\\mathrm T}=(1,-1,1)$，$\\alpha^{\\mathrm T}\\alpha=1+1+1=3$。
【易错】拆分时行向量取任意非零行（符号要一致）；$\\alpha^{\\mathrm T}\\alpha$ 是数不是矩阵。
【注意】答案 3。""",
6: """【公式】$A^{2}B-A-B=E\\Rightarrow(A^{2}-E)B=A+E\\Rightarrow(A-E)(A+E)B=A+E\\Rightarrow B=(A-E)^{-1}$。
【技巧】求 $|B|$ 不必算出 $B$：$|B|=\\dfrac{|A+E|}{|A-E||A+E|}=\\dfrac{1}{|A-E|}$（约去 $|A+E|$）。
【易错】约去 $A+E$ 需 $|A+E|\\ne0$（本题主对角 $1,3,1$ 显然非零）；$A^{2}-E=(A-E)(A+E)$ 因 $E$ 可交换恒成立。
【注意】$|A-E|=\\begin{vmatrix}0&0&1\\\\0&1&0\\\\-2&0&0\\end{vmatrix}=2$，$|B|=\\dfrac12$。""",
7: """【公式】极限四则的除法规则要求分母极限非零——反证：若 $\\lim b_{n}c_{n}=A\\ne0$，则 $c_{n}=\\dfrac{b_{n}c_{n}}{b_{n}}\\to A$ 有限，与 $c_n\\to\\infty$ 矛盾。
【技巧】$b_n\\to1$ 是"可除"的关键（极限非零才保除法合法）；非负数列保证不出现 $\\infty-\\infty$ 型抵消。
【易错】$A=0$ 的情形不被反证排除——$b_nc_n$ 可以趋于 0，所以"极限必为 0"这类过强结论要小心。
【注意】逐一验证选项中哪些结论对**一切**满足条件的数列成立（答案 D）。""",
8: """【公式】凑微分：$x^{n-1}\\,\\mathrm dx=\\dfrac{1}{n}\\mathrm d(1+x^{n})$；重要极限 $\\left(1-\\dfrac{1}{n+1}\\right)^{n}=\\left(\\dfrac{n}{n+1}\\right)^{n}\\to\\mathrm e^{-1}$。
【技巧】先积出 $a_n=\\dfrac1n\\left[\\left(1+\\left(\\tfrac{n}{n+1}\\right)^{n}\\right)^{3/2}-1\\right]$，再乘 $n$ 取极限。
【易错】$\\left(\\dfrac{n}{n+1}\\right)^{n}=\\left(1-\\dfrac1{n+1}\\right)^{n}\\to\\mathrm e^{-1}$（指数是 $n$ 不是 $n+1$）。
【注意】$na_n\\to\\left(1+\\mathrm e^{-1}\\right)^{3/2}-1$，选 B。""",
9: """【公式】反求参数函数：把解 $y=\\dfrac{x}{\\ln x}$ 及其导数 $y'=\\dfrac{\\ln x-1}{\\ln^{2}x}$ 代入方程，解出 $\\varphi$。
【技巧】$\\dfrac yx=\\dfrac{1}{\\ln x}\\Rightarrow\\dfrac xy=\\ln x$、$\\dfrac yx\\cdot\\dfrac xy=1$ 这类代换关系先列出来。
【易错】$\\varphi$ 的自变量是 $\\dfrac xy$，最后要把表达式化成 $\\dfrac xy$ 的函数（答案 $-\\dfrac{y^{2}}{x^{2}}$ 的形式）。
【注意】验证法：选项代回检验比硬推快。""",
10: """【公式】极值点两类来源：$f'=0$ 且两侧变号；$f'$ 不存在但两侧变号。
【技巧】导函数图上数：与 $x$ 轴的交点（$f'=0$）+ 图形断点（$f'$ 不存在处），逐个看左右符号。
【易错】$x=0$ 处 $f'$ 不存在也可为极值点——只数零点会漏；"变号"才计，不变号的驻点不算。
【注意】本题两个极小值点、一个极大值点（答案 C）。""",
11: """【公式】$x\\in(0,\\tfrac\\pi4)$：$\\tan x>x\\Rightarrow\\dfrac{\\tan x}{x}>1$、$\\dfrac{x}{\\tan x}<1$。
【技巧】除比较 $I_1,I_2$ 外还必须与 1 比：$\\tan x\\le\\sec x\\Rightarrow\\dfrac{\\tan x}{x}\\le\\dfrac1{x\\cos x}$，$\\displaystyle\\int_0^{\\pi/4}\\sec x\\,\\mathrm dx=\\ln(1+\\sqrt2)<1$ 掐住 $I_1$。
【易错】只得出 $I_1>I_2$ 排除两个选项后，另两个都在"$1$ 的位置"上见分晓——$\\dfrac{\\pi}{4}<1$ 是关键常识。
【注意】结论 $I_1>1>I_2$。""",
12: """【公式】表示性秩定理：组 I 可由组 II 表示 $\\Rightarrow r(\\mathrm I)\\le r(\\mathrm{II})$；等价 $\\Leftrightarrow$ 秩相等（互为表示）。
【技巧】"可由"只是单向不等式；等价必须补"秩相等"条件。
【易错】由可表示推不出两组合并后秩不减、也推不出可互相表示——单向与双向要分清。
【注意】答案 D：$r(\\mathrm I)=r(\\mathrm{II})\\Leftrightarrow$ 两向量组等价。""",
13: """【公式】左右极限：$\\ln(1+ax^{3})\\sim ax^{3}$；$x-\\arcsin x\\sim-\\dfrac{x^{3}}{6}$；$\\mathrm e^{ax}-1-ax\\sim\\dfrac{a^{2}x^{2}}{2}$；$\\sin\\dfrac x4\\sim\\dfrac x4$。
【技巧】左极限 $=\\dfrac{ax^{3}}{-x^{3}/6}=-6a=6\\Rightarrow a=-1$；右极限 $=\\dfrac{a^{2}x^{2}/2+x^{2}}{x^{2}/4}=2a^{2}+4=6\\Rightarrow a=\\pm1$——交集即答案。
【易错】$x-\\arcsin x$ 是负的三阶无穷小（$\\arcsin x=x+\\tfrac{x^3}6+\\cdots$）；右段分子二次项 $x^{2}$ 与 $\\tfrac{a^{2}x^{2}}2$ 要相加。
【注意】$a=-1$ 同时满足左右（右段只要求 $a=\\pm1$）。""",
14: """【公式】参数二阶导：$y''=\\dfrac{1}{\\varphi'(t)}\\dfrac{\\mathrm d}{\\mathrm dt}\\left(\\dfrac{\\psi'(t)}{\\varphi'(t)}\\right)$；变限积分求导上下限都带导数。
【技巧】$\\psi'(t)=\\dfrac{2\\mathrm e\\cdot t^{2}}{t}-\\dfrac{\\mathrm e^{t}}{t}=\\dfrac{2\\mathrm e t^{2}-\\mathrm e^{t}}{t}$（$\\mathrm e^{1+2\\ln t}=\\mathrm e t^{2}$ 对数落地）；$x=9\\Rightarrow t=2$。
【易错】$\\mathrm e^{1+2\\ln t}=\\mathrm e\\cdot t^{2}$（$t>0$）；链式除以 $\\varphi'(t)=4t$ 两次。
【注意】答案 $-\\dfrac{\\mathrm e}{16(1+2\\ln2)^{2}}$。""",
15: """【公式】换元模板：$x=\\tan t$ → $\\sqrt{1+x^{2}}=\\sec t$、$(1+x^{2})^{3/2}=\\sec^{3}t$、$\\mathrm dx=\\sec^{2}t\\,\\mathrm dt$；$\\displaystyle\\int\\mathrm e^{t}\\sin t\\,\\mathrm dt=\\dfrac{\\mathrm e^{t}(\\sin t-\\cos t)}{2}+C$。
【技巧】换元后 $\\int\\mathrm e^{t}\\sin t\\,\\mathrm dt$ 是经典"两次分部回头式"，一次背熟终身受益。
【易错】回代：$\\tan t=x\\Rightarrow\\sin t=\\dfrac{x}{\\sqrt{1+x^{2}}}$、$\\cos t=\\dfrac{1}{\\sqrt{1+x^{2}}}$（辅助三角形）。
【注意】结果 $\\dfrac{\\mathrm e^{\\arctan x}(x-1)}{2\\sqrt{1+x^{2}}}+C$。""",
16: """【公式】反函数二阶导：$\\dfrac{\\mathrm dx}{\\mathrm dy}=\\dfrac1{y'}$，$\\dfrac{\\mathrm d^{2}x}{\\mathrm dy^{2}}=-\\dfrac{y''}{y'^{3}}$。
【技巧】把 $x''_{y}=-\\dfrac{y''}{y'^{3}}$ 代入原方程，乘 $y'^{3}$ 整理，即得关于 $y=y(x)$ 的可降阶方程。
【易错】负号与立方（不是平方）；$y'\\ne0$ 的题设保证反函数求导合法。
【注意】(2) 解出 $y=\\ln\\left(x+\\sqrt{x^{2}+1}\\right)$ 型双曲函数解。""",
17: """【公式】交点个数 $\\Leftrightarrow$ 方程 $\\varphi(x)=\\ln^{4}x-4\\ln x+4x-k$ 在 $(0,+\\infty)$ 的根个数；$\\varphi'(x)=\\dfrac{4(\\ln^{3}x-\\ln x+x)}{x}$。
【技巧】证 $\\varphi'$ 恰有一个零点（分子在 $(0,1)$ 负、$x\\ge1$ 正——$\\ln^{3}x-\\ln x\\ge-\\dfrac{2}{3\\sqrt3}>-\\dfrac12<x$ 的正项兜底），得唯一极小值 $m=\\varphi(x_0)$。
【易错】$k$ 与极小值 $m$ 的三种关系各对应 0、1（相切）、2 个交点——只讨论 $k=m$ 一种不完整。
【注意】$x\\to0^+$ 与 $x\\to+\\infty$ 时 $\\varphi\\to+\\infty$，两端上翘夹住唯一谷底。""",
18: """【公式】法线 $y$ 截距 $=y+\\dfrac{x}{y'}$；"线段 $PQ$ 被 $x$ 轴平分" $\\Rightarrow Q_y=-y$（中点纵坐标 0）。
【技巧】几何条件一步化微分方程：$y+\\dfrac{x}{y'}=-y\\Rightarrow2y\\,\\mathrm dy=-x\\,\\mathrm dx\\Rightarrow y^{2}=C-\\dfrac{x^{2}}{4}$——直接积，不用套类型。
【易错】法线斜率是 $-\\dfrac1{y'}$（不是 $-y'$）；中点条件是"纵坐标之和为 0"。
【注意】过 $\\left(\\tfrac{\\sqrt2}2,\\tfrac12\\right)$ 定 $C=\\dfrac12$，第一象限取 $y=\\dfrac12\\sqrt{2-x^{2}}$（椭圆弧）。""",
19: """【公式】体积-面积链：$\\dfrac{\\mathrm dV}{\\mathrm dt}=\\pi\\varphi^{2}(y)\\cdot\\dfrac{\\mathrm dy}{\\mathrm dt}=3$；液面面积 $A=\\pi\\varphi^{2}(y)$，$\\dfrac{\\mathrm dA}{\\mathrm dt}=\\pi$。
【技巧】两条件相除消去时间：$\\dfrac{\\mathrm dV/\\mathrm dt}{\\mathrm dA/\\mathrm dt}=\\dfrac{\\mathrm dy}{\\mathrm dA}\\cdot A\\cdots$ 直白路径——$\\dfrac{\\mathrm dV}{\\mathrm dA}=3$，配合 $\\mathrm dV=A\\,\\mathrm dy=\\pi\\varphi^{2}\\,\\mathrm dy$ 解出 $\\varphi^{2}(y)=2y+4$。
【易错】$A=\\pi\\varphi^{2}$ 是圆面积公式（半径 $\\varphi$）；$\\mathrm dV=A\\,\\mathrm dy$ 的薄层体积元。
【注意】(2) 由 $\\varphi^{2}=2y+4$ 得 $y=\\dfrac{\\varphi^{2}-4}{2}$ 代入体积式解 $t$。""",
20: """【公式】极限存在 + 分母 $\\to0$ ⇒ 分子 $\\to0$：$\\lim\\limits_{x\\to a^{+}}f(2x-a)=f(a)=0$（用连续性）。
【技巧】(1) 的 $f(a)=0$ 配 $f'>0$ 单调增 → $x>a$ 时 $f(x)>0$——是 (2) 中构造函数不恒为零的台阶。
【易错】(2) 双中值题常用"把区间一分两段、两次拉格朗日"或"作辅助函数 + 罗尔"；$\\lim\\dfrac{f(2x-a)}{x-a}=2f'(a)$ 这个解读在后续问里常被忽略。
【注意】$f(2x-a)\\to f(a)=0$ 同时说明 $f$ 在左端点"从零起步"。""",
21: """【公式】二重根可对角化条件：$\\lambda$ 为 $k$ 重根时 $r(\\lambda E-A)=n-k$。
【技巧】$|\\lambda E-A|=(\\lambda-6)(\\lambda^{2}-4\\lambda-12)=(\\lambda-6)^{2}(\\lambda+2)$：二重根 $6$ → 令 $r(6E-A)=1$，行倍数关系 $-$8 行 = $-2\\times$ 首行读出 $a=0$。
【易错】特征值 $6,-2$（不是 $6,2$）；$P$ 的第三列对应 $\\lambda=-2$ 的特征向量（分量含自由变量）。
【注意】$P^{-1}AP=\\mathrm{diag}(6,6,-2)$，$P$ 列序与对角元对应。""",
22: """【公式】三直线交于一点 $\\Leftrightarrow$ 方程组唯一解 $\\Leftrightarrow r(A)=r(\\bar A)=2$；系数行列式 $\\det=a^{3}+b^{3}+c^{3}-3abc=(a+b+c)(a^{2}+b^{2}+c^{2}-ab-bc-ca)$。
【技巧】必要性巧证：三式相加得 $(a+b+c)(x+2y+3)=0$；若 $a+b+c\\ne0$ 则 $x+2y+3=0$，与 $l_1$ 对比系数矛盾（三条直线互不相同）→ 必有 $a+b+c=0$。
【易错】充分性要分两步：$a+b+c=0$ 时先看 $\\det=0$（三行相关），再证 $r(A)=r(\\bar A)=2$（用前两行不成比例）。
【注意】$a^{2}+b^{2}+c^{2}-ab-bc-ca>0$（非全等实数），是分解式非零因子的依据。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2003数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2003数二真题.md', TIPS_2003)
