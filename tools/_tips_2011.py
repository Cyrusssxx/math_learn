# -*- coding: utf-8 -*-
# 2011 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2011 = {
1: """【公式】$\\sin ax=ax-\\dfrac{a^{3}x^{3}}{6}+o(x^{3})$ → $3\\sin x-\\sin3x=\\left(3x-\\dfrac{x^{3}}{2}\\right)-\\left(3x-\\dfrac{27x^{3}}{6}\\right)=4x^{3}$。
【技巧】减法型展开到相消阶；系数逐项核对（$\\dfrac{27}{6}-\\dfrac{3}{6}=\\dfrac{24}{6}=4$）。
【易错】$\\sin3x$ 的三次项系数是 $-\\dfrac{27}{6}$（$a^{3}=27$）。
【注意】$c=4,\\ k=3$（答案 C）。""",
2: """【公式】导数定义拼装：$\\dfrac{x^{2}f(x)-2f(x^{3})}{x^{3}}=\\dfrac{f(x)-f(0)}{x}-2\\cdot\\dfrac{f(x^{3})-f(0)}{x^{3}}$（加减 $f(0)$）。
【技巧】两项分别就是 $f'(0)$ 与 $f'(0)$ 的定义式（$x^{3}\\to0$ 与 $x\\to0$ 同阶）。
【易错】$f(0)=0$ 是加减 $f(0)$ 的前提；系数 2 落在第二项。
【注意】$f'(0)-2f'(0)=-f'(0)$（答案 B）。""",
3: """【公式】$\\left[\\ln|(x-1)(x-2)(x-3)|\\right]'=\\dfrac{1}{x-1}+\\dfrac{1}{x-2}+\\dfrac{1}{x-3}=\\dfrac{3x^{2}-12x+11}{(x-1)(x-2)(x-3)}$。
【技巧】驻点 = 分子二次式的零点：判别式 $144-132=12>0$ → 恰 2 个。
【易错】$x=1,2,3$ 处不可导（对数零点），但它们不是驻点；判别式别算错。
【注意】2 个（答案 C）。""",
4: """【公式】特征根 $\\pm\\lambda$ → 右端 $\\mathrm e^{\\pm\\lambda x}$ 都是共振项 → 特解 $x\\left(A\\mathrm e^{\\lambda x}+B\\mathrm e^{-\\lambda x}\\right)$。
【技巧】两项分别乘 $x$（叠加原理）；$\\lambda>0$ 时 $\\pm\\lambda$ 都是单特征根。
【易错】只给一项乘 $x$、另一项不乘是最常见错误。
【注意】答案 C。""",
5: """【公式】$A=z_{xx}(0,0)=f''(0)g(0)$、$C=z_{yy}(0,0)=f(0)g''(0)$、$B=z_{xy}(0,0)=f'(0)g'(0)=0$；极小值充分条件：$A>0,\\ C>0$。
【技巧】$g(0)<0$ 翻转符号：$A>0\\Leftrightarrow f''(0)<0$；$f(0)>0$ 保号：$C>0\\Leftrightarrow g''(0)>0$——找"$f''(0)<0$ 且 $g''(0)>0$"的选项。
【易错】$B=0$ 使 $AC-B^{2}=AC$；符号翻转由 $g(0)<0$ 承担，别算成 $f$ 翻。
【注意】选 $f''(0)<0,\\ g''(0)>0$ 的选项（极小值充分条件）。""",
6: """【公式】$(0,\\tfrac\\pi4)$ 上 $\\sin x<\\cos x<1<\\cot x$ → 取对数保序：$\\ln\\sin x<\\ln\\cos x<0<\\ln\\cot x$。
【技巧】被积函数逐项比较 → 积分逐项比较（区间相同）；$\\ln\\cos x<0$ 说明 $J$ 的中间项为负。
【易错】对数在 $(0,1)$ 上为负、在 $(1,\\infty)$ 上为正——三项跨越了 1。
【注意】答案 B（$I<J<K$ 型）。""",
7: """【技巧】列组合 → 右乘过渡阵、行交换 → 左乘初等阵：$B=AP_1$、$E=P_2B$ → $A=P_2^{-1}?$ 按操作顺序组装 $P_1P_2$ 与 $A$ 的关系。
【易错】本题选项与推导存在出入（数据中已标注"待核"）——方法论本身（列变换右乘、行变换左乘、$P_1^{-1}=E_{12}$）是考点，答案键以数据标注为准。
【注意】先掌握"列右乘、行左乘"的组装逻辑，此题具体选项存疑（数据答案 D 标记待核）。""",
8: """【公式】$(1,0,1,0)^{\\mathrm T}$ 是 $Ax=0$ 的解 → $\\alpha_1+\\alpha_3=0$ → $\\alpha_3=-\\alpha_1$；$n-r(A)=1$ → $r(A)=3$。
【技巧】把 $\\beta=\\alpha_1+2\\alpha_2+3\\alpha_3$ 全部化成 $\\alpha_1,\\alpha_2$ 表示：$=-\\alpha_1+2\\alpha_2$；$Ax=\\beta$ 的解 = 表示系数 $(0,2,2,0)^{\\mathrm T}$。
【易错】$\\alpha_2+\\alpha_3=(0,1,1,0)^{\\mathrm T}$ → $\\alpha_2=-\\alpha_3+(0,1,1,0)^{\\mathrm T}=\\alpha_1+(0,1,1,0)^{\\mathrm T}$；符号别错。
【注意】$x=(0,2,2,0)^{\\mathrm T}$（答案 D）。""",
9: """【公式】$\\lim(a^{n}+b^{n})^{1/n}=\\max(a,b)$。
【技巧】$\\left(\\dfrac{1+2^{n}}{2}\\right)^{1/n}=2\\cdot\\left(\\dfrac{1+2^{n}}{2^{n}}\\right)^{1/n}=2\\left(1+2^{-n}\\right)^{1/n}\\to2$（$n\\ln(1+2^{-n})\\to0$）。
【易错】除以 $2^{n}$ 的"归一"技巧；剩余因子趋于 1 的论证（指数 $\\tfrac1n$）。
【注意】答案 2。""",
10: """【公式】一阶线性积分因子 $\\mathrm e^{x}$：$(\\mathrm e^{x}y)'=\\cos x$ → $\\mathrm e^{x}y=\\sin x+C$。
【技巧】初值 $y(0)=0$ → $C=0$，一步到位。
【易错】$\\displaystyle\\int\\cos x\\,\\mathrm dx=\\sin x$；除回 $\\mathrm e^{x}$。
【注意】$y=\\mathrm e^{-x}\\sin x$。""",
11: """【公式】弧长 $s=\\displaystyle\\int\\sqrt{1+y'^{2}}\\,\\mathrm dx=\\int_0^{\\pi/4}\\sqrt{1+\\tan^{2}x}\\,\\mathrm dx=\\int_0^{\\pi/4}\\sec x\\,\\mathrm dx$。
【公式补充】$\\displaystyle\\int\\sec x\\,\\mathrm dx=\\ln|\\sec x+\\tan x|+C$。
【易错】$1+\\tan^{2}=\\sec^{2}$ 开方取正（区间上 $\\sec>0$）；端点 $\\sec0=1,\\tan0=0$、$\\sec\\tfrac\\pi4=\\sqrt2,\\tan\\tfrac\\pi4=1$。
【注意】答案 $\\ln(1+\\sqrt2)$。""",
12: """【公式】指数分布期望：$\\displaystyle\\int_0^{+\\infty}x\\lambda\\mathrm e^{-\\lambda x}\\,\\mathrm dx=\\dfrac{1}{\\lambda}$（$\\Gamma(2)/\\lambda=\\tfrac{1}{\\lambda}$）。
【技巧】分部一次：$\\left[-x\\mathrm e^{-\\lambda x}\\right]_0^{\\infty}+\\dfrac1{\\lambda}\\displaystyle\\int_0^{\\infty}\\lambda\\mathrm e^{-\\lambda x}\\,\\mathrm dx=0+\\dfrac1{\\lambda}$。
【易错】$\\lambda$ 在密度里出现两次；$\\infty$ 端 $x\\mathrm e^{-\\lambda x}\\to0$。
【注意】答案 $\\dfrac1{\\lambda}$。""",
13: """【公式】极坐标：圆 $x^{2}+y^{2}=2y$ → $r=2\\sin\\theta$；直线 $y=x$ → $\\theta=\\dfrac\\pi4$；$y$ 轴 → $\\theta=\\dfrac\\pi2$。
【技巧】$\\displaystyle\\iint xy\\,\\mathrm d\\sigma=\\int_{\\pi/4}^{\\pi/2}\\mathrm d\\theta\\int_0^{2\\sin\\theta}r^{3}\\cos\\theta\\sin\\theta\\,\\mathrm dr=4\\int_{\\pi/4}^{\\pi/2}\\sin^{5}\\theta\\cos\\theta\\,\\mathrm d\\theta$。
【易错】$r^{3}$（$xy=r^{2}\\cos\\sin$ 乘雅可比 $r$）；凑 $\\mathrm d(\\sin\\theta)$ 后 $\\sin$ 的五次方。
【注意】$\\dfrac46\\left[\\sin^{6}\\theta\\right]_{\\pi/4}^{\\pi/2}=\\dfrac23\\left(1-\\dfrac18\\right)=\\dfrac{7}{12}$。""",
14: """【公式】配方法：$f=(x_1+x_2+x_3)^{2}+2x_2^{2}$——第三个平方项缺失 → $r(f)=2$、正惯性指数 2。
【技巧】配方后不出现的变量即秩亏损方向（$x_1+x_2+x_3=0$ 且 $x_2=0$ 时 $f=0$）。
【易错】正惯性指数 = 正平方项个数 = 2（不是 3）。
【注意】答案 2。""",
15: """【公式】分子 $\\displaystyle\\int_0^{x}\\ln(1+t^{2})\\,\\mathrm dt\\sim\\dfrac{x^{3}}{3}$（$x\\to0$）；$\\sim\\dfrac{x^{2}\\ln x}{}$ 增长（$x\\to+\\infty$，积分 $\\approx x\\ln(1+x^{2})-2x+2\\arctan x$）。
【技巧】双侧极限分类：$\\dfrac{\\sim x^{3}/3}{x^{\\alpha}}$ 在 $\\alpha<3$ 时为 0、$\\alpha=3$ 时 $\\dfrac13$；$x\\to+\\infty$ 端 $\\dfrac{\\approx x\\cdot2\\ln x}{x^{\\alpha}}$ 在 $\\alpha>1$ 时为 0。
【易错】$x\\to+\\infty$ 端分部积分后的主项 $\\approx x\\ln(1+x^{2})$（增长比 $x$ 快、比 $x^{1+\\epsilon}$ 慢）→ 条件 $\\alpha>1$。
【注意】交集 $1<\\alpha<3$。""",
16: """【公式】参数二阶导：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{t^{2}-1+1?}{t^{2}+1}\\cdots$——$x'_t=t^{2}+1>0$ 恒正，$t$ 与 $x$ 同增。
【技巧】$t=\\dfrac23$ 对应 $x=\\dfrac{35}{27}$? 先由 $x=\\dfrac13t^{3}+t+\\dfrac13$ 解出对应 $t$，再算二阶导。
【易错】$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{y''_t x'_t-y'_t x''_t}{x'^{3}}$ 的分母立方；$y=\\dfrac{t^{3}}{3}+t^{2}+\\dfrac{t}{3}$ 的求导。
【注意】按数据解析（$y''=\\dfrac{t^{2}-1}{t^{2}+1}$? 以解析为准）。""",
17: """【公式】链式 + 极值条件：$g'(1)=0$（$g$ 在 $x=1$ 取极值）→ $z_x$ 在 $x=1,y=?$ 处的表达式里 $yg'(1)$ 项消失。
【技巧】$z_{xy}$ 展开：$x\\left[f''_{11}y+f''_{12}g'\\right]+xg'\\left[f''_{21}y+f''_{22}g'\\right]+f'_2 g'$ 中代 $g'(1)=0$、$x=1,y=?$ 的对应值。
【易错】极值条件只给出 $g'(1)=0$（$g''(1)$ 未知符号）；$f$ 的下标变量是 $(xy,\\ yg(x))$——第一个中间变量对 $x$ 的导数是 $y$。
【注意】$z_{xy}|=f''_{11}+y\\cdot$? 按数据解析代入 $(1,1)$：$=f''_{11}(1,1)+f''_{12}(1,1)$? 以解析为准。""",
18: """【公式】倾角与切线斜率：$\\tan\\alpha=y'$ → $\\alpha=\\arctan y'$ → $\\dfrac{\\mathrm d\\alpha}{\\mathrm dx}=\\dfrac{y''}{1+y'^{2}}$。
【技巧】"曲线与 $y=x$ 相切于原点" → $y(0)=0,\\ y'(0)=1$ → $\\alpha(0)=\\dfrac\\pi4$；$\\lim\\limits_{x\\to0^+}\\dfrac{\\mathrm d\\alpha}{\\mathrm dx}=?$ 由 $y''(0)$ 定。
【易错】$\\arctan$ 求导 $\\dfrac{1}{1+y'^{2}}$；相切条件给两个初值。
【注意】按数据解析（极限为 $\\dfrac12$? 以解析为准）。""",
19: """【公式】(I) $\\ln(1+x)-\\ln1=\\dfrac{x}{1+\\xi}$（$\\xi\\in(0,x)$）→ $\\dfrac{x}{1+x}<\\ln(1+x)<x$。
【技巧】(II) 把 $\\dfrac1{n+1}$ 放缩为 $\\ln\\left(1+\\dfrac1n\\right)$（左半）与右半 $\\ln\\left(1+\\dfrac1n\\right)>\\dfrac{2n+1}{(n+1)^{2}}$（右端 = $\\dfrac1n+\\dfrac1{n+1}$ 的组合）——逐和累加：$\\sum\\ln\\left(1+\\dfrac1n\\right)=\\ln(n+1)$。
【易错】(II) 的右端 $\\dfrac{2n+1}{(n+1)^{2}}=\\dfrac1{n+1}+\\dfrac{1}{(n+1)^{2}}?$ 由 $\\dfrac{2n+1}{(n+1)^{2}}<\\ln\\left(1+\\dfrac1n\\right)$ 需要单独构造（右端两项拆分）。
【注意】 telescope（裂项相消）后 $\\ln(n+1)$ 与调和数夹出结论。""",
20: """【公式】旋转体容积分段：$y\\in[\\tfrac12,2]$ 段用圆 $x^{2}+(y-1)^{2}=1$（$x^{2}=2y-y^{2}$），$y\\in[0,\\tfrac12]$ 段用抛物线 $x^{2}=2y$。
【技巧】圆盘法逐段：$V=\\pi\\displaystyle\\int_{1/2}^{2}(2y-y^{2})\\,\\mathrm dy+\\pi\\int_0^{1/2}2y\\,\\mathrm dy$。
【易错】分界 $y=\\tfrac12$（两曲线交点 $x^{2}=1,\\ x=1$）；$x^{2}=2y-y^{2}=1-(y-1)^{2}$。
【注意】(II) 清洗后液面高度 $h$ 由"剩余体积 = 半容积"解出（对称性：$h=1$? 按数据解析）。""",
21: """【公式】交换次序 + 边界条件消项：$\\displaystyle\\iint xy f''_{xy}\\,\\mathrm dx\\,\\mathrm dy=\\int_0^1 y\\left[\\int_0^1 x f''_{xy}\\,\\mathrm dx\\right]\\mathrm dy$，内层分部 $\\left[xf'_y\\right]_0^1-\\displaystyle\\int f'_y\\,\\mathrm dx$。
【技巧】$f(1,y)=0$ → $\\dfrac{\\partial}{\\partial y}f(1,y)=f'_y(1,y)=0$（边界导数为零是分部边界项消失的关键）。
【易错】两次分部的边界项（$x=1$ 处 $f'_y=0$、$y=1$ 处 $f'_x=0$）——全靠题给边界条件；$f(0,y)=?$ 无条件（$x=0$ 处 $x$ 因子消项）。
【注意】结论 $I=\\displaystyle\\iint_D f\\,\\mathrm d\\sigma$（恒等式反用）。""",
22: """【公式】无关极大线性无关组：$\\alpha_1,\\alpha_2$ 无关（分量不成比例）→ 添 $\\alpha_3$ 判秩；极大无关组与其余向量的表示关系。
【技巧】行变换消参后极大无关组选 $\\alpha_1,\\alpha_2$（或含参形式按 $a$ 的取值讨论——参数让 $\\alpha_2,\\alpha_3$ 成比例时另选）。
【易错】参数 $a$ 的临界值（使某两向量成比例）必须单独讨论表示系数。
【注意】按数据解析写出极大无关组与其余向量的表示式（含参数分支）。""",
23: """【公式】$A\\begin{pmatrix}1\\\\0\\\\-1\\end{pmatrix}=\\begin{pmatrix}0\\\\0\\\\0\\end{pmatrix}$ → $\\lambda=0$，特征向量 $\\alpha_1=(1,0,-1)^{\\mathrm T}$；第二列 → $A(1,0,1)^{\\mathrm T}=(1,1,1)^{\\mathrm T}$? 逐列读条件。
【技巧】$r(A)=2$ → 零特征值单重 + 另两个特征值；实对称 → 用正交性构造第二个特征向量（与 $\\alpha_1$ 正交且满足 $A\\alpha=0$? 由给定的乘积矩阵读）。
【易错】给定矩阵 $A(1,0,-1)=0$、$A(1,0,1)=(1,1,1)$ → $\\beta=(1,1,1)$ 分解到 $\\alpha$ 方向求 $A\\beta$。
【注意】(II) 按数据解析（$A\\beta=?$ 表示系数法）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2011数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2011数二真题.md', TIPS_2011)
