# -*- coding: utf-8 -*-
# 批次插入器：把 {题号: 点睛文本} 插入真题源 md（每题最后一个块之后、下一题 ### 之前）
# 用法: python _tips_2000.py
import re, sys
from pathlib import Path

def insert_tips(md_path, tips):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    # 找到每题的行号区间
    heads = [(i, int(re.match(r'^### (\d+)\.', l).group(1)))
             for i, l in enumerate(lines) if re.match(r'^### (\d+)\.', l)]
    inserted = 0
    # 从后往前插：前面的行号不受插入影响
    for idx in range(len(heads) - 1, -1, -1):
        li, no = heads[idx]
        if no not in tips:
            continue
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        # 题目区间内最后一个 ':::'（块结束行）
        last_close = None
        for j in range(li, end):
            if lines[j].strip() == ':::':
                last_close = j
        if last_close is None:
            print(f'  [WARN] {p.name} Q{no} 未找到块结束行，跳过')
            continue
        block = ['', '', '::: 点睛'] + tips[no].split('\n') + [':::']
        lines[last_close + 1:last_close + 1] = block
        inserted += 1
    p.write_text('\n'.join(lines), encoding='utf-8')
    print(f'{p.name}: 插入 {inserted} 题点睛')

TIPS_2000 = {
1: """【公式】$\\arctan x=x-\\dfrac{x^{3}}{3}+o(x^{3})$；$\\ln(1+u)\\sim u$（$u\\to0$）。
【易错】不能代入 $\\arctan x\\sim x$——分子是减法，一换代入就成 0；减法型必须展开到"相消阶"（本题 $x^{3}$）。
【技巧】把 $x-\\arctan x\\sim\\dfrac{x^{3}}{3}$ 当结论背下来；分母 $\\ln(1+2x^{3})\\sim2x^{3}$ 整体系数 2 别丢。
【注意】比阶时分子分母要同阶才能直接相除；$o(x^{3})$ 不影响比值。""",
2: """【公式】隐函数求导：$2^{y}\\ln2\\cdot y'=1+y'$；$\\mathrm{d}y=y'\\,\\mathrm{d}x$。
【技巧】先代 $x=0$ 定 $y(0)$：$2^{y}=y$，试 $y=1$ 恰好成立。
【易错】没求 $y(0)$ 就对导数式代 $x=0$；$2^{1}\\ln2=2\\ln2=\\ln4$，两个写法等价别当错。
【注意】求微分别只算 $y'$ 就停，答案要写成 $\\mathrm{d}y=\\dfrac{\\mathrm{d}x}{\\ln4-1}$。""",
3: """【公式】$\\displaystyle\\int\\frac{\\mathrm{d}t}{t^{2}+a^{2}}=\\frac1a\\arctan\\frac ta+C$。
【技巧】见 $\\sqrt{x-2}$ 整体换元 $t=\\sqrt{x-2}$：$x=t^{2}+2$，$\\mathrm{d}x=2t\\,\\mathrm{d}t$，根号消掉成有理积分。
【易错】换元后积分限跟着变：$x=2\\to t=0$，$+\\infty\\to+\\infty$；$x+7=t^{2}+9$ 别写成 $t^{2}-9$。
【注意】$\\arctan\\dfrac t3\\Big|_0^{+\\infty}=\\dfrac{\\pi}{2}$——无穷限收敛到 $\\dfrac\\pi2$，不是发散。""",
4: """【公式】斜渐近线：$k=\\lim\\limits_{x\\to\\infty}\\dfrac yx$，$b=\\lim\\limits_{x\\to\\infty}(y-kx)$。
【技巧】$b$ 的极限里拆 $\\mathrm e^{1/x}=1+\\dfrac1x+o(\\dfrac1x)$，或用 $\\mathrm e^{1/x}-1\\sim\\dfrac1x$。
【易错】$b=\\lim[(2x-1)\\mathrm e^{1/x}-2x]$ 直接代会 $\\infty-\\infty$；必须先写 $2x\\mathrm e^{1/x}=2x(\\mathrm e^{1/x}-1)+2x$ 拆项。
【注意】严格说要 $x\\to+\\infty$ 与 $x\\to-\\infty$ 都验证；本题两侧极限相同，渐近线 $y=2x+1$。""",
5: """【公式】核心恒等式：由 $B=(E+A)^{-1}(E-A)$ 左乘 $(E+A)$ 移项得 $(A+E)(B+E)=2E$。
【技巧】目标是 $(E+B)^{-1}$——不要真的去求逆！配凑出 $(E+B)\\cdot\\dfrac12(E+A)=E$ 即可，答案就是 $\\dfrac12(E+A)$。
【易错】硬算 4 阶矩阵的逆是大坑；移项时 $AB+B=E-A$ 添 $A$ 凑 $(A+E)B+(A+E)=2E$ 这一步容易卡住。
【注意】系数 2 的来源：$E-A$ 与 $E+A$ 之和为 $2E$。""",
6: """【技巧】连续性：$\\mathrm e^{bx}>0$ 恒成立，故 $a\\ge0$ 时分母 $a+\\mathrm e^{bx}>0$ 恒正；极限：$x\\to-\\infty$ 时 $\\mathrm e^{bx}$ 按 $b$ 分三段讨论（$b>0\\to0$，$b=0\\to1$，$b<0\\to+\\infty$）。
【易错】$a=0$ 允许吗？允许——$b<0$ 时 $f=\\dfrac{x}{\\mathrm e^{bx}}\\to0$ 且分母恒正，所以是 $a\\ge0$ 不是 $a>0$，这正是 D 与 B 的区别。
【注意】两个条件各筛掉一批选项：连续性保 $a\\ge0$，极限保 $b<0$。""",
7: """【公式】拐点判定：$f''(x_0)=0$ 且 $f''$ 在 $x_0$ 两侧变号（充分条件：$f'''(x_0)\\ne0$）。
【技巧】抽象函数关系式可以两边求导递推：原式求导得 $f'''+2f'f''=1$，代 $x=0$ 得 $f'''(0)=1\\ne0$。
【易错】看到 $f'(0)=0$、$f''(0)=0$ 就想判极值——$f''(0)=0$ 时极值判别法失效，本题极值根本无法确定。
【注意】"拐点"是曲线上的点 $(0,f(0))$，不是横坐标。""",
8: """【公式】$\\left(\\dfrac fg\\right)'=\\dfrac{f'g-fg'}{g^{2}}$。
【技巧】见 $f'g-fg'$ 立刻凑商的导数（分母 $g^2>0$ 保号）；单调性不等式对 $\\dfrac fg$ 用，再交叉相乘。
【易错】交叉相乘的方向：$\\dfrac{f(x)}{g(x)}>\\dfrac{f(b)}{g(b)}$ 且 $g>0$，乘过去得 $f(x)g(b)>f(b)g(x)$，别把不等号写反。
【注意】与 $a$ 比较的是 $x<a$ 的不等式（本题只有与 $b$ 比较的成立），逐个选项验证。""",
9: """【公式】$\\sin6x=6x-\\dfrac{(6x)^3}{6}+o(x^3)=6x-36x^3+o(x^3)$。
【技巧】"已知一个极限求另一个"：把已知函数泰勒展开代入已知式，整体除 $x^3$ 后移项读出目标极限。
【易错】用 $\\sin6x\\sim6x$ 精度不够——分母是 $x^3$，必须展到 $x^3$ 项。
【注意】极限为 0 说明分子是 $x^3$ 的高阶无穷小：$\\dfrac{6+f(x)}{x^2}-36\\to0$。""",
10: """【公式】特解 $\\mathrm e^{\\lambda x}$ ↔ 特征根 $\\lambda$；$x\\,\\mathrm e^{\\lambda x}$ ↔ $\\lambda$ 为二重根。
【技巧】$y_2=2x\\mathrm e^{-x}$ 里的系数 2 无关紧要，关键是 $x$ 因子 → $r=-1$ 二重根；$y_3=\\mathrm e^{x}$ → $r=1$。
【易错】三个特解只给了两个根——别漏"二重根计两次"；阶数 3 = 重根数之和。
【注意】特征方程 $(r+1)^2(r-1)=r^3+r^2-r-1$，符号别展开错（选 B）。""",
11: """【公式】$\\displaystyle\\int\\frac{\\mathrm{d}x}{1+\\mathrm e^{x}}=x-\\ln(1+\\mathrm e^{x})+C$。
【技巧】$f(\\ln x)$ 型：令 $t=\\ln x$ 反解 $x=\\mathrm e^{t}$，还原 $f$ 的表达式再积分。
【易错】分部积分取 $u=\\ln(1+\\mathrm e^{x})$、$\\mathrm dv=\\mathrm e^{-x}\\mathrm dx$；尾项 $\\int\\dfrac{\\mathrm dx}{1+\\mathrm e^x}$ 别硬算——分子凑 $(1+\\mathrm e^x)-\\mathrm e^x$ 两秒出结果。
【注意】不定积分结果记得 $+C$。""",
12: """【技巧】直线截正方形：$t$ 按 $0\\le t\\le1$、$1<t\\le2$、$t>2$ 三段画图定形，别凭空写。
【公式】第一段直角三角形 $S=\\dfrac12t^2$；第二段补形 $S=1-\\dfrac12(2-t)^2$；第三段满铺 $S=1$。
【易错】第二段是"整个正方形减右上角三角形"，直接写成 $\\dfrac12(2-t)^2$ 是最常见错误。
【注意】对 $t$ 积分后自变量换成 $x$，分段点与 $S(t)$ 对齐（$x=1,2$）。""",
13: """【公式】$f^{(n)}(0)=n!\\cdot[x^n]\\,f(x)$（泰勒系数法）；$\\ln(1+x)=\\sum_{k\\ge1}\\dfrac{(-1)^{k-1}}{k}x^{k}$。
【技巧】乘 $x^2$ 只把每项幂次 +2——$x^n$ 系数即展开式中 $k=n-2$ 项系数，比莱布尼茨公式快得多。
【易错】符号 $(-1)^{n-3}=(-1)^{n-1}$（差 2 次方不变号）；只对 $n\\ge3$ 成立（$n=1,2$ 时系数为 0）。
【注意】本题结论 $f^{(n)}(0)=\\dfrac{(-1)^{n-1}n!}{n-2}$ 可当模型记：$x^{m}\\ln(1+x)$ 同理。""",
14: """【公式】$|\\cos t|$ 周期为 $\\pi$，$\\displaystyle\\int_0^{\\pi}|\\cos t|\\,\\mathrm dt=2$。
【技巧】周期函数积分 = 整周期 × 每周期积分值 + 余段；极限用夹逼。
【易错】余段 $\\displaystyle\\int_{n\\pi}^{x}$ 的范围是 $[0,2)$（上开下闭），写闭区间就错了；放缩 $\\dfrac{S(x)}x$ 时 $x\\ge n\\pi$、$x<(n+1)\\pi$ 的分母方向要一致。
【注意】$n\\to\\infty$ 时左右两端都趋于 $\\dfrac2\\pi$，夹逼收口。""",
15: """【公式】微元法：$\\dfrac{\\mathrm dm}{\\mathrm dt}=$（排入浓度×排入速率）$-$（湖内浓度×流出速率）；一阶线性 $\\dfrac{\\mathrm dm}{\\mathrm dt}+\\dfrac m3=\\dfrac{m_0}{6}$。
【技巧】浓度均匀 → 流出带走量 $=\\dfrac mV\\cdot\\dfrac V3=\\dfrac m3$，$V$ 直接消掉；排入 $A$ 量 $=\\dfrac{m_0}{V}\\cdot\\dfrac V6=\\dfrac{m_0}6$。
【易错】初始条件 $m(0)=5m_0$（1999 年底）；"降至 $m_0$ 以内"解 $m(t)=m_0$ 的临界时刻。
【注意】答案 $t=3\\ln9=6\\ln3\\approx6.6$ 年；通解 $m=\\dfrac{m_0}2+Ce^{-t/3}$ 的稳态是 $\\dfrac{m_0}2$（永远降不到 0）。""",
16: """【技巧】见 $\\displaystyle\\int_0^\\pi f\\,\\mathrm dx=0$ 与 $\\int_0^\\pi f\\cos x\\,\\mathrm dx=0$ 成对出现 → 构造 $F(x)=\\int_0^x f$，把条件变成 $F(0)=F(\\pi)=0$ 与 $\\int_0^\\pi F\\sin x\\,\\mathrm dx=0$。
【公式】分部积分转移导数：$\\int f\\cos x\\,\\mathrm dx=\\int\\cos x\\,\\mathrm dF=[F\\cos x]_0^\\pi+\\int F\\sin x\\,\\mathrm dx$。
【易错】分部积分的符号（$\\cos$ 求导出 $-\\sin$，负负得正）；中值定理只能保证 $F(\\eta)\\sin\\eta=0$，$\\sin\\eta=0$（即 $\\eta=\\tfrac\\pi2$）的情形要单独讨论。
【注意】两个零点 = 找两段罗尔区间 $[0,\\eta]$、$[\\eta,\\pi]$。""",
17: """【公式】导数定义 $f'(1)=\\lim\\limits_{x\\to0}\\dfrac{f(1+\\sin x)-f(1)}{\\sin x}$；周期 5 → $f(x+5)=f(x)$ 且 $f'(x+5)=f'(x)$。
【技巧】$\\alpha(x)=o(x)$：式子除以 $x$ 再取极限，高阶项自动消失；$f(1)$ 先令 $x\\to0$ 对原式取极限求出（$f(1)=0$）。
【易错】第二个极限 $\\dfrac{f(1-\\sin x)-f(1)}{-\\sin x}\\cdot\\dfrac{\\sin x}{x}$ 里的负号——拆项后是 $+3f'(1)$，符号丢就选错。
【注意】切点 $(6,f(6))=(6,0)$，斜率 $f'(6)=f'(1)=2$，切线 $y=2x-12$。""",
18: """【公式】绕 $x$ 轴旋转（washer）：$V=\\pi\\int_a^b\\bigl[\\text{外}^2-\\text{内}^2\\bigr]\\,\\mathrm dx$。
【技巧】体积是 $a$ 的一元函数 $V(a)$：交点 $x_A=\\dfrac1{\\sqrt{a+1}}$ 作上限，对 $a$ 求导找驻点。
【易错】被积函数是（直线 $OA$）$^{2}-$（抛物线）$^{2}$，$0\\le x\\le x_A$ 上直线在抛物线上方，别减反；对 $\\dfrac{a^2}{(a+1)^{5/2}}$ 求导用对数求导法更快。
【注意】$a\\to0^+$、$a\\to+\\infty$ 时 $V\\to0$，驻点 $a=4$ 即最大；$V_{\\max}=\\dfrac{32\\pi}{375\\sqrt5}$。""",
19: """【技巧】含 $\\displaystyle\\int_0^x f$ 的积分方程：先乘 $(x+1)$ 整理再两边求导消去积分号。
【公式】得 $(x+1)f''+(x+2)f'=0$；令 $g=f'$ 分离变量 $\\dfrac{g'}g=-1-\\dfrac1{x+1}$ → $g=\\dfrac{C\\mathrm e^{-x}}{x+1}$。
【易错】定 $C$ 用 $f'(0)$：原式代 $x=0$，积分项 $\\int_0^0=0$，得 $f'(0)+f(0)=0$，即 $f'(0)=-1$。
【注意】(2) 双侧估计：$f'= -\\dfrac{\\mathrm e^{-x}}{x+1}<0$ 且 $\\dfrac1{x+1}\\le1$ → $f(x)=1-\\int_0^x\\dfrac{\\mathrm e^{-t}}{t+1}\\mathrm dt \\ge 1-\\int_0^x\\mathrm e^{-t}\\,\\mathrm dt=\\mathrm e^{-x}$，上界 $f(0)=1$ 由单调减给出。""",
20: """【公式】外积型 $A=\\alpha\\beta^{\\mathrm T}$：$A^2=\\alpha(\\beta^{\\mathrm T}\\alpha)\\beta^{\\mathrm T}=(\\beta^{\\mathrm T}\\alpha)A$——幂次塌缩为"数 × A"。
【技巧】先算内积 $B=\\beta^{\\mathrm T}\\alpha=2$（一个数！），则 $A^2=2A$、$A^4=8A$、$B^2=4$、$B^4=16$，方程瞬间降为线性方程组。
【易错】$B^2A^2$ 里 $B^2=4$ 是数、$A^2=2A$ 是矩阵，数乘与矩阵乘别混；$r(A)=1$，$A$ 的幂不用硬乘。
【注意】化简后合并同类项（$A$ 的系数与常数项分开），解普通线性方程组即得 $x$。""",
21: """【公式】$\\beta_3$ 可由 $\\alpha_1,\\alpha_2,\\alpha_3$ 线性表示 $\\Leftrightarrow r(\\alpha_1,\\alpha_2,\\alpha_3)=r(\\alpha_1,\\alpha_2,\\alpha_3,\\beta_3)$。
【技巧】三步走：① 行阶梯化求 $r(\\alpha)=2$；② $r(\\beta)=2$ ⟹ $\\det[\\beta_1,\\beta_2,\\beta_3]=3b-a=0$；③ 表示条件 ⟹ $\\det[\\alpha_1,\\alpha_2,\\beta_3]=2b-10=0$。两条方程解出 $a=15,b=5$。
【易错】$\\det[\\beta]=0$ 只是"秩 ≤ 2"的必要条件，秩也可能更低——需确认 $\\beta$ 组确有二阶非零子式。
【注意】"相同的秩"给的是方程一，"可线性表示"给的是方程二，两个条件缺一不可。""",
}

if __name__ == '__main__':
    insert_tips(r'D:\ai code\数学二真题\2000数二真题.md', TIPS_2000)
