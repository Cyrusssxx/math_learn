# -*- coding: utf-8 -*-
# 批次插入器：把 {题号: 点睛文本} 插入真题源 md（每题最后一个块之后、下一题 ### 之前）
# 用法: python _tips_2000.py
# 写作原则（与思路分工，防重合）：
#   思路 = 本题怎么解（具体步骤、中间展开）；点睛 = 可迁移的知识资产。
#   公式段只写泛化模型/可背结论，不复述思路里已有的具体展开（无泛化价值则整段省略）；
#   技巧段写通用套路与最优路径；易错/注意写思路里没有的坑与边界。
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

def strip_tips(md_path):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    out, skip = [], 0
    for l in lines:
        t = l.strip()
        if t == '::: 点睛':
            skip = 1; continue
        if skip:
            if t == ':::':
                skip = 0
            continue
        out.append(l)
    p.write_text('\n'.join(out), encoding='utf-8')
    print(f'{p.name}: 剥离旧点睛完成')

TIPS_2000 = {
1: """【公式】减法型结论串（可背）：$x-\\arctan x\\sim\\dfrac{x^{3}}{3}$，$x-\\sin x\\sim\\dfrac{x^{3}}{6}$，$x-\\tan x\\sim\\dfrac{x^{3}}{3}$，$x-\\ln(1+x)\\sim\\dfrac{x^{2}}{2}$。
【易错】减法型不能直接等价代换——一代入就变 0；必须泰勒展开到"相消阶"。
【技巧】抽象函数配 $x^{k}$ 分母：把已知函数展到 $x^{k}$ 阶，余项全部并入 $o(x^{k})$，$f(x)$ 的阶自动显形。
【注意】比阶时分子分母要同阶才能直接相除；$o(x^{3})$ 不影响比值。""",
2: """【公式】$\\mathrm dy=y'\\,\\mathrm dx$；指数求导 $\\left(a^{y}\\right)'=a^{y}\\ln a\\cdot y'$。
【技巧】隐函数求 $\\mathrm dy$ 三步顺序固定：代 $x=x_0$ 定 $y_0$ → 两边求导代值 → 写 $\\mathrm dy$。
【易错】跳过"先定 $y_0$"直接代 $x=0$ 是最常见断点；$2^{1}\\ln2=\\ln4$。
【注意】题目问微分就答到 $\\mathrm dy=\\cdots\\,\\mathrm dx$，只写 $y'$ 不完整。""",
3: """【公式】$\\displaystyle\\int\\frac{\\mathrm{d}t}{t^{2}+a^{2}}=\\frac1a\\arctan\\frac ta+C$。
【技巧】$\\sqrt{\\text{一次式}}$ 的标准动作：$t=\\sqrt{x-2}$，$\mathrm dx=2t\\,\\mathrm dt$，分子分母的 $t$ 约干净。
【易错】换元必换限：$x=2\\to t=0$，$+\\infty\\to+\\infty$；$x+7=t^{2}+9$ 的符号。
【注意】无穷处 $\\arctan\\dfrac t3\\to\\dfrac{\\pi}{2}$，收敛值有限，不是发散。""",
4: """【技巧】斜渐近线的 $b=\\lim(y-kx)$ 是 $\\infty-\\infty$ 型：把含 $\\mathrm e$ 的项按 $\\mathrm e^{1/x}=1+\\dfrac1x+o(\\dfrac1x)$ 拆开再合并。
【易错】$(2x-1)\\mathrm e^{1/x}$ 整体直接代展开会漏项；规范做法是 $2x\\,\\mathrm e^{1/x}=2x(\\mathrm e^{1/x}-1)+2x$ 拆成"已知等价 + 常数"。
【注意】两侧极限都要验证一致才是一条渐近线；本题 $x\\to\\pm\\infty$ 相同。""",
5: """【公式】模型：$B=(E+A)^{-1}(E-A)$ 型恒有 $(A+E)(B+E)=2E$，即 $(E+B)^{-1}=\\dfrac12(E+A)$——凡"$A$ 的两个线性组合互为逆桥"都这样配。
【技巧】目标含逆 → 不求逆，改证"乘起来等于 $E$"。
【易错】移项卡点：$AB+B=E-A$ 两边添 $A$，左侧才配得出 $(A+E)B+(A+E)$。
【注意】系数 2 来自 $(E-A)+(E+A)=2E$。""",
6: """【技巧】$\\mathrm e^{bx}$ 在 $x\\to-\\infty$ 按 $b$ 三段讨论（$>0\\to0$、$=0\\to1$、$<0\\to+\\infty$）；分母恒正性只看 $a$ 与 $\\mathrm e^{bx}>0$。
【易错】$a=0$ 边界：$b<0$ 时 $f=\\dfrac{x}{\\mathrm e^{bx}}\\to0$ 且分母恒正——$a=0$ 合法，这正是 D 选项 $a\\ge0$ 的含义，选 $a>0$ 就错。
【注意】两个条件各卡一半选项：连续保 $a\\ge0$，极限保 $b<0$。""",
7: """【公式】拐点判定：$f''(x_0)=0$ 且 $f''$ 两侧变号（充分条件 $f'''(x_0)\\ne0$）；$f'$ 极值点 ↔ $f$ 拐点。
【技巧】抽象关系式 = 高阶导数的递推公式：两边求导就能一层层往下推（本题推到 $f'''$）。
【易错】$f'(0)=0$ 且 $f''(0)=0$ 时极值判别法全部失效，极值无法判定——别硬选极值项。
【注意】"拐点"指曲线上的点 $(0,f(0))$，不是横坐标 $0$。""",
8: """【公式】见 $f'g-fg'$ → $\\left(\\dfrac fg\\right)'$ 的分子；对照 $f'g+fg'\\to(fg)'$。正函数相除保序：$\\dfrac{f(x)}{g(x)}>\\dfrac{f(b)}{g(b)}\\iff f(x)g(b)>f(b)g(x)$（$g>0$）。
【技巧】导数条件给的不等式 → 还原成"某构造函数单调"，再写单调不等式比对选项。
【易错】单调减写出的是 $\\dfrac{f(x)}{g(x)}>\\dfrac{f(b)}{g(b)}$（$x<b$），乘过去方向别反。
【注意】四个选项分别与 $a$、$b$、端点值比较，逐一对照单调不等式，别凭感觉。""",
9: """【公式】$\\sin ax=ax-\\dfrac{a^{3}}{6}x^{3}+o(x^{3})$（$a=6$ 时三次项系数 $-36$）。
【技巧】"已知极限反求另一极限"：已知函数泰勒展开代入，整体除 $x^{3}$，目标式作为整体被"读出"。
【易错】代 $\\sin6x\\sim6x$ 精度不够（分母 $x^{3}$），必须展到三次项。
【注意】"极限为 0" 翻译成 $\\dfrac{6+f(x)}{x^{2}}\\to36$ 这种整体读出法，比解 $f(x)$ 快得多。""",
10: """【公式】特解 ↔ 特征根映射：$\\mathrm e^{\\lambda x}$ ↔ 单根 $\\lambda$；$x\\,\\mathrm e^{\\lambda x}$ ↔ 二重根；$(r-\\lambda_1)\\cdots$ 展开即方程系数。
【技巧】$x\\,\\mathrm e^{-x}$ 的 $x$ 因子 = 二重根信号；特解前面的系数（2、3）无信息量。
【易错】三个特解只给出两个根——重根计两次才凑满三阶；漏了就选成单根组合。
【注意】$(r+1)^{2}(r-1)=r^{3}+r^{2}-r-1$，展开符号核对一遍再选。""",
11: """【公式】$\\displaystyle\\int\\frac{\\mathrm{d}x}{1+\\mathrm e^{x}}=x-\\ln(1+\\mathrm e^{x})+C$（分子加减 $\\mathrm e^{x}$ 拆两项）。
【技巧】$f(\\varphi(x))$ 给复合式求 $f$ 的积分：令 $t=\\varphi(x)$ 反解再代入，先还原 $f$ 本体。
【易错】分部取 $u=\\ln(1+\\mathrm e^{x})$、$\\mathrm dv=\\mathrm e^{-x}\\mathrm dx$，取反了越积越复杂；尾项别硬算，凑分子。
【注意】$\\int f\\,\\mathrm dx$ 是不定积分，$+C$ 不能丢。""",
12: """【技巧】几何面积型分段函数：先画直线与区域的相对位置，交点即分段点（本题 $t=1,2$）。
【公式】第一段直角三角形 $\\dfrac12t^{2}$；第二段补形 $1-\\dfrac12(2-t)^{2}$；满铺为常数。
【易错】第二段是"正方形 − 右上角三角形"，直接写 $\\dfrac12(2-t)^{2}$ 是高频错误。
【注意】积分结果的自变量 $x$ 的分段点与 $S(t)$ 的分段点一致（$x=1,2$），逐段积分。""",
13: """【公式】泰勒系数法：$f^{(n)}(0)=n!\\cdot[x^{n}]f(x)$——高阶导数问题优先想展开，不用莱布尼茨。
【技巧】乘 $x^{2}$ = 全部幂次 +2：$x^{n}$ 系数就是 $\\ln(1+x)$ 展开中 $k=n-2$ 项的系数。
【易错】$(-1)^{n-3}=(-1)^{n-1}$（差偶数次幂）；结论只对 $n\\ge3$ 成立，$n=1,2$ 系数为 0。
【注意】模型可迁移：$x^{m}\\ln(1+x)$ 求 $f^{(n)}(0)$ 全是这一招。""",
14: """【技巧】周期函数长区间积分：拆"整周期 × 单周期值 + 余段"；余段用 $0\\le\\text{余段}<\\text{单周期值}$ 放缩，极限用夹逼。
【易错】余段的界是 $[0,2)$（下闭上开），写成闭区间就丢了严谨性分；放缩 $\\dfrac{S(x)}x$ 时 $x\\ge n\\pi$、$x<(n+1)\\pi$ 两个界配合使用。
【注意】$n\\to\\infty$ 时左右界同时收口到 $\\dfrac2\\pi$，别只放缩一边。""",
15: """【公式】微元法建模：$\\dfrac{\\mathrm dm}{\\mathrm dt}=$（注入浓度×注入速率）$-$（湖内浓度×流出速率）；一阶线性标准式 $\\dfrac{\\mathrm dm}{\\mathrm dt}+\\dfrac m3=\\dfrac{m_0}6$。
【技巧】"浓度均匀"意味着流出带走量 $=\\dfrac mV\\cdot\\dfrac V3=\\dfrac m3$——$V$ 一定消掉，见到 $V$ 别留着。
【易错】注入的 $A$ 量用"限定浓度" $\\dfrac{m_0}{V}$ 而非当前湖内浓度；初始值 $m(0)=5m_0$ 对应 1999 年底。
【注意】"至多多少年"求临界 $m(t)=m_0$：$t=6\\ln3$；稳态 $\\dfrac{m_0}2$ 说明永远降不到 0。""",
16: """【技巧】$\\displaystyle\\int_0^{\\pi}f\\,\\mathrm dx=0$ 与 $\\int_0^{\\pi}f\\cos x\\,\\mathrm dx=0$ 成对出现 → 造 $F(x)=\\int_0^x f$：第一条件变 $F$ 的端点值，第二条件分部后变成无 $f$ 的积分条件。
【公式】分部转移导数：$\\displaystyle\\int f\\cos x\\,\\mathrm dx=[F\\cos x]_0^{\\pi}+\\int F\\sin x\\,\\mathrm dx$——把"被积函数带 $\\cos$"化成"带 $\\sin$"。
【易错】中值定理得 $F(\\eta)\\sin\\eta=0$ 后，$\\sin\\eta=0$（$\\eta=\\tfrac\\pi2$）的情形必须单独讨论，直接断言 $F(\\eta)=0$ 会漏。
【注意】两个零点 = 找到两段都满足罗尔条件的区间 $[0,\\eta]$、$[\\eta,\\pi]$。""",
17: """【公式】导数定义的变形识别：$\\lim\\limits_{x\\to0}\\dfrac{f(1+\\sin x)-f(1)}{\\sin x}=f'(1)$；周期函数 $f'(x+T)=f'(x)$（导函数同周期）。
【技巧】$\\alpha(x)=o(x)$ 的处理：等式两边除以 $x$ 取极限，高阶项自动归零；$f(1)$ 先令 $x\\to0$ 取极限求出。
【易错】$f(1-\\sin x)$ 那项拆导数定义时，$\\dfrac{\\sin x}{x}\\to1$ 而内部分母是 $-\\sin x$——负号落在 $f'(1)$ 前面，配 $-3f(1-\\sin x)$ 后是 $+3f'(1)$。
【注意】切点 $(6,f(6))$ 靠周期平移得到，别把 $f(6)$ 算错。""",
18: """【公式】washer：$V=\\pi\\int\\bigl[\\text{外}^{2}-\\text{内}^{2}\\bigr]\\,\\mathrm dx$；直线绕轴是锥、抛物线绕轴是抛物面体。
【技巧】几何量含参数 → 统一表成 $V(a)$ 一元函数，求导找驻点；交点横坐标 $\\dfrac1{\\sqrt{a+1}}$ 作积分上限。
【易错】$x\\in[0,x_A]$ 上直线在抛物线上方，$\\text{外}^2-\\text{内}^2$ 别减反；对 $\\dfrac{a^{2}}{(a+1)^{5/2}}$ 求导先取对数更稳。
【注意】$a\\to0^+$、$a\\to\\infty$ 时 $V\\to0$，唯一驻点 $a=4$ 即最大，$V_{\\max}=\\dfrac{32\\pi}{375\\sqrt5}$。""",
19: """【公式】变限积分方程标配动作：整理成 $\\text{某式}=\\displaystyle\\int_0^x f$ 后两边求导；一次消不干净就再求一次（本题得可降阶二阶方程）。
【技巧】$f'$ 满足的可分离方程：$\\dfrac{g'}g=-1-\\dfrac1{x+1}$ 直接积出 $g=\\dfrac{C\\mathrm e^{-x}}{x+1}$，不必套一阶线性公式。
【易错】定 $C$ 的 $f'(0)$ 从原式取 $x=0$ 得到（$\\int_0^0=0$ 消失），$f'(0)+f(0)=0$；忘掉这步就卡死。
【注意】双侧不等式两条腿：单调减给上界 $f\\le1$；N-L 积分 $+\\dfrac1{t+1}\\le1$ 放缩给下界 $f\\ge\\mathrm e^{-x}$。""",
20: """【公式】秩 1 矩阵模型：$A=\\alpha\\beta^{\\mathrm T}\\Rightarrow A^{k}=(\\beta^{\\mathrm T}\\alpha)^{k-1}A$——一切幂的问题先算内积（一个数）。
【技巧】$B=\\beta^{\\mathrm T}\\alpha=2$ 是数，$B^{2}A^{2}=4\\cdot2A=8A$；矩阵方程瞬间化为一元线性方程组。
【易错】数与矩阵身份别混：$B^{2}=4$、$B^{4}=16$ 直接算，$A$ 的幂走塌缩公式，$r(A)=1$ 不用硬乘。
【注意】合并同类项后解普通方程组；这类"形式复杂、算完极简"的题先别被 $A^{4}x$ 吓住。""",
21: """【公式】线性表示的秩语言：$\\beta$ 可由 $\\alpha_1,\\alpha_2,\\alpha_3$ 表示 $\\Leftrightarrow r(\\alpha_1,\\alpha_2,\\alpha_3)=r(\\alpha_1,\\alpha_2,\\alpha_3,\\beta)$。
【技巧】双条件双方程：① 秩相等给 $r(\\beta)=2$ → $\\det[\\beta]=3b-a=0$；② 可表示给 $\\det[\\alpha_1,\\alpha_2,\\beta_3]=2b-10=0$。联立即得 $a=15,b=5$。
【易错】$\\det[\\beta]=0$ 只保证秩 $\\le2$，须确认确有二阶非零子式（秩恰为 2），否则单条件可能多解。
【注意】选两列构造行列式时挑已线性无关的那组（$\\alpha_1,\\alpha_2$），比硬算三阶带参行列式快。""",
}

if __name__ == '__main__':
    import sys
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2000数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2000数二真题.md', TIPS_2000)
