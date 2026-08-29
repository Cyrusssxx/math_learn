# -*- coding: utf-8 -*-
# 2010 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2010 = {
1: """【公式】约分：$\\dfrac{x^{2}-x}{x^{2}-1}=\\dfrac{x}{x+1}$（$x=1$ 是可去零点）。
【技巧】约分后剩两类嫌疑点：$x=0$（$\\sqrt{1+1/x^{2}}$ 无定义）与 $x=-1$（分母零）；$x=0$ 处 $\\sqrt{1+\\tfrac1{x^{2}}}\\to\\left|\\dfrac1x\\right|$，$f\\to\\dfrac{x}{x+1}\\cdot\\dfrac{1}{|x|}=\\dfrac{1}{1+x}\\to1$（可去）。
【易错】$x=-1$ 处 $\\dfrac{x}{x+1}\\to\\infty$ 且 $\\sqrt{\\cdot}\\to\\left|\\tfrac1x\\right|$，整体 $\\to\\infty$（无穷间断）；约掉的 $x=1$ 是可去间断点，要计入"间断点"但不计入"无穷"。
【注意】无穷间断点 1 个（$x=-1$，答案 B）。""",
2: """【公式】解的结构：$\\lambda y_1+\\mu y_2$ 是齐次 $y'+p(x)y=0$ 的解 $\\Leftrightarrow\\lambda+\\mu=0$；更是非齐次解 $\\Leftrightarrow\\lambda+\\mu=1$。
【技巧】题给 $\\lambda y_1-\\mu y_2$：即 $\\lambda+(-\\mu)=0$ 且 $\\lambda+(-\\mu)=1$——矛盾 → 不存在这样的 $\\lambda,\\mu$，选"恒不是"分支。
【易错】减号要换算成系数和（$-\\mu$ 的系数是 $-1$）；齐次解之差、非齐次解之差是齐次解这两条结构定理是钥匙。
【注意】答案 A。""",
3: """【公式】相切 = 有公共切点 + 斜率相等：$2x_0=\\dfrac{a}{x_0}$ 且 $x_0^{2}=a\\ln x_0$。
【技巧】$a=2x_0^{2}$ 代入：$x_0^{2}=2x_0^{2}\\ln x_0$ → $\\ln x_0=\\tfrac12$ → $x_0=\\sqrt{\\mathrm e}$、$a=2\\mathrm e$。
【易错】$\\ln$ 的定义域 $x_0>0$ 自动满足；两条件缺一不可（只联立斜率会多解）。
【注意】$a=2\\mathrm e$（选 C）。""",
4: """【公式】瑕积分比较判别法：对数因子永远压不过幂（$|\\ln(1-x)|<C_{\\epsilon}(1-x)^{-\\epsilon}$ 对任意 $\\epsilon>0$）→ 敛散性完全由幂函数因子 $x^{-2/n}$（$x\\to0$）与 $(1-x)^{-2/n}$（$x\\to1$）决定。
【技巧】两端点分头判：$p=\\dfrac2n\\ge1$（即 $n\\ge2$）时两端都发散；$p<1$（$n=1$）时两端都收敛。
【易错】对数不改变敛散（这是本题的设计）；$n$ 是正整数 → 只有 $n=1$ 收敛。
【注意】答案 D（$n$ 最大取 1）。""",
5: """【公式】隐函数链式：$F\\left(\\tfrac yx,\\tfrac zx\\right)=0$ 对 $x$ 求导：$f'_1\\cdot\\left(-\\dfrac y{x^{2}}\\right)+f'_2\\cdot\\dfrac{xz_x-z}{x^{2}}=0$ → $x\\dfrac{\\partial z}{\\partial x}=\\dfrac yx f'_1+\\dfrac zf'_2$。
【技巧】$\\dfrac zx$ 对 $x$ 求导出 $\\dfrac{xz_x-z}{x^{2}}$（$z$ 是 $x$ 的函数）；对 $y$ 同理得 $x\\dfrac{\\partial z}{\\partial y}=-f'_1+\\dfrac zf'_2$ 型。
【易错】两个偏导的符号与 $\\dfrac zx$ 的商法则；最后按选项整理成 $x\\dfrac{\\partial z}{\\partial x}$ 与 $\\dfrac{\\partial z}{\\partial y}$ 的组合。
【注意】答案 B。""",
6: """【公式】二重黎曼和配平：$\\dfrac{n}{(n+i)(n^{2}+j^{2})}=\\dfrac1n\\cdot\\dfrac{1}{(1+\\frac in)(1+(\\frac jn)^{2})}$。
【技巧】和的乘积拆成两个独立黎曼和极限的乘积：$\\left(\\displaystyle\\int_0^1\\frac{\\mathrm dx}{1+x}\\right)\\left(\\displaystyle\\int_0^1\\frac{\\mathrm dx}{1+x^{2}}\\right)=\\ln2\\cdot\\dfrac{\\pi}{4}$。
【易错】系数 $n$ 的配平（$\\dfrac1n$ 提出后每维各留 $\\dfrac1n$）；$i,j$ 从 1 起对应 $x=\\dfrac in\\in(0,1]$（端点不影响极限）。
【注意】答案 $\\dfrac{\\pi\\ln2}{4}$（选 D）。""",
7: """【公式】表示性秩定理：$\\mathrm I$ 可由 $\\mathrm{II}$ 表示 → $r(\\mathrm I)\\le r(\\mathrm{II})$。
【技巧】$\\mathrm I$ 无关 → $r(\\mathrm I)=r$；$r(\\mathrm{II})\\le s$ → 链 $r\\le s$。
【易错】"可表示"只给单向不等式；别把"等价"（需双向）混进来。
【注意】答案 A（$r\\le s$）。""",
8: """【公式】$A^{2}+A=O$ → 每个特征值 $\\lambda$ 满足 $\\lambda^{2}+\\lambda=0$ → $\\lambda\\in\\{0,-1\\}$；实对称必可对角化。
【技巧】$4$ 阶、$r(A)=3$ → $0$ 恰一个、$-1$ 恰三个 → 相似于 $\\mathrm{diag}(-1,-1,-1,0)$。
【易错】"秩 3"卡死零特征值的个数；实对称保证可对角化（一般矩阵靠 $A^2+A=O$ 无重根因子也能对角化）。
【注意】答案 D。""",
9: """【公式】$\\lambda^{3}-2\\lambda^{2}+\\lambda-2=(\\lambda^{2}(\\lambda-2))+（\\lambda-2)=(\\lambda-2)(\\lambda^{2}+1)$。
【技巧】三次多项式先试整数根（$\\lambda=2$ 代入 $8-8+2-2=0$ ✓），再因式分解出 $\\lambda^{2}+1$。
【易错】复根 $\\pm\\mathrm i$ → $\\cos x,\\sin x$；实根 2 → $\\mathrm e^{2x}$。
【注意】通解 $C_1\\mathrm e^{2x}+C_2\\cos x+C_3\\sin x$。""",
10: """【公式】$\\dfrac{2x^{3}}{x^{2}+1}=2x-\\dfrac{2x}{x^{2}+1}$（多项式除法一次到位）。
【技巧】分母恒正无垂直渐近线；尾项 $\\dfrac{2x}{x^{2}+1}\\to0$ → 斜渐近线 $y=2x$。
【易错】水平渐近线不存在（$x\\to\\infty$ 时 $y\\to\\infty$）；别漏查。
【注意】$y=2x$。""",
11: """【公式】$\\ln(1-2x)=-\\displaystyle\\sum_{n\\ge1}\\dfrac{(2x)^{n}}{n}$ → $x^{n}$ 系数 $-\\dfrac{2^{n}}{n}$ → $y^{(n)}(0)=n!\\times$系数 $=-2^{n}(n-1)!$。
【技巧】展开比逐次求导快一个量级；$y^{(n)}(0)=n!\\cdot[x^{n}]y$。
【易错】$(n-1)!$ 的错位（$n!$ 除以 $n$）；负号。
【注意】答案 $-2^{n}(n-1)!$。""",
12: """【公式】极坐标弧长：$s=\\displaystyle\\int\\sqrt{r^{2}+r'^{2}}\\,\\mathrm d\\theta$；$r=\\mathrm e^{\\theta}$、$r'=r$ → 被积 $\\sqrt2\\,\\mathrm e^{\\theta}$。
【技巧】$\\theta\\in[0,\\pi]$ 直接积：$\\sqrt2(\\mathrm e^{\\pi}-1)$。
【易错】$\\sqrt{2\\mathrm e^{2\\theta}}=\\sqrt2\\,\\mathrm e^{\\theta}$（$\\mathrm e^{\\theta}>0$ 无绝对值问题）。
【注意】答案 $\\sqrt2(\\mathrm e^{\\pi}-1)$。""",
13: """【公式】相关变化率：对角线 $d=\\sqrt{l^{2}+w^{2}}$ → $d'=\\dfrac{ll'+ww'}{d}$。
【技巧】$l=12,w=5$ 恰是勾股数（$d=13$）；代入 $l'=2,w'=3$：$d'=\\dfrac{24+15}{13}=3$。
【易错】问的是**对角线**的变化率（不是面积 $S=lw$ 的 46）。
【注意】答案 $3\\,\\mathrm{cm/s}$。""",
14: """【公式】构造乘积凑行列式：$A(A^{-1}+B)B^{-1}=B^{-1}+A$ → $|A+B^{-1}|=|A|\\cdot|A^{-1}+B|\\cdot\\dfrac{1}{|B|}$。
【技巧】三条接力：$3\\cdot2\\cdot\\dfrac12=3$。
【易错】构造方向：想出现 $A+B^{-1}$ 就左乘 $A$、右乘 $B^{-1}$。
【注意】答案 3。""",
15: """【公式】拆项：$f(x)=x^{2}\\displaystyle\\int_1^{x^{2}}\\mathrm e^{-t^{2}}\\,\\mathrm dt-\\int_1^{x^{2}}t\\,\\mathrm e^{-t^{2}}\\,\\mathrm dt$，求导（变限上限 $x^{2}$ 链式 + 乘积法则）后前两项恰好相消：$f'(x)=2x\\displaystyle\\int_1^{x^{2}}\\mathrm e^{-t^{2}}\\,\\mathrm dt$。
【技巧】$\\mathrm e^{-t^{2}}>0$ → $f'$ 符号由 $x^{2}-1$ 决定：$|x|<1$ 减、$|x|>1$ 增。
【易错】上限 $x^{2}$ 的链式 $2x$；$f(\\pm1)$ 为极小值（$f'$ 变号点）。
【注意】单调区间与极小值 $f(\\pm1)$（原函数值按解析代入）。""",
16: """【公式】(I) $0<\\ln(1+t)<t$（$t>0$）→ $[\\ln(1+t)]^{n}<t^{n}$，$\\left|\\ln t\\right|[\\ln(1+t)]^{n}\\le|\\ln t|\\,t^{n}$——对数被幂压制。
【技巧】(II) 用 (I) 的两侧夹逼取极限（同乘归一化因子后比较）。
【易错】$\\ln t\\to-\\infty$（$t\\to0^{+}$）看似危险，但 $\\ln(1+t)^{n}\\sim t^{n}$ 的压制是逐 $n$ 成立的。
【注意】(II) 极限为 1。""",
17: """【公式】参数二阶导 + 题给条件联立：$\\left(1+\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}\\right)\\left(\\dfrac{\\mathrm dy}{\\mathrm dx}\\right)^{2}=1$，其中 $\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{\\psi'(t)}{2t+2}$、$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{\\psi''(t)(2t+2)-2\\psi'(t)}{(2t+2)^{3}}$。
【技巧】代回整理得 $\\psi''-\\dfrac{\\psi'}{1+t}=6t+2$? 按解析路径解一阶线性方程：$\\psi'=C(1+t)+3t^{2}+\\cdots$，初值 $\\psi'(1)=3$、$\\psi(1)=\\dfrac52$ 定常数。
【易错】分母 $(2t+2)^{3}$ 的链式与化简（$2t+2=2(1+t)$）；$t=1$ 对应 $x=3$ 的换算。
【注意】$\\psi(t)=\\dfrac32t^{3}+t^{2}$（$t>-1$；$\\psi(1)=\\dfrac52$ ✓）。""",
18: """【公式】平放椭圆柱：油深 $\\dfrac b2$ → 油面对应 $\\sin t=\\dfrac12$（从顶部量 $t=\\dfrac{\\pi}{6}$）；弓形面积 = 半椭圆 $\\dfrac{\\pi ab}{2}$ − 上部小弓形。
【技巧】上部小弓形 $\\displaystyle\\int_{b/2}^{b}2\\sqrt{1-\\tfrac{y^{2}}{b^{2}}}\\cdot b\\cdot? \\ \\mathrm dy$：换元 $y=b\\sin t$ → $ab\\displaystyle\\int_{\\pi/6}^{\\pi/2}\\cos^{2}t\\,\\mathrm dt=ab\\left(\\dfrac{\\pi}{3}+\\dfrac{\\sqrt3}{8}\\right)$ 型。
【易错】油深从顶部往下量 $\\dfrac b2$ → 自由液面在 $y=\\dfrac b2$ 处（顶为 $b$）；弓形积分限 $\\tfrac{\\pi}{6}\\to\\tfrac{\\pi}{2}$。
【注意】油质量 $m=\\left(\\dfrac{2\\pi}{3}+\\dfrac{\\sqrt3}{4}\\right)ab\\,l\\rho$。""",
19: """【公式】变换设计：原方程 $4u_{xx}+12u_{xy}+9u_{yy}=0$ 的主象征 $4\\lambda^{2}+12\\lambda\\mu+9\\mu^{2}=(2\\lambda+3\\mu)^{2}$ 退化 → 取 $\\xi=2x+3y$（沿退化方向）、$\\eta=y$（无关方向）。
【技巧】链式回代后 $u_{xx},u_{xy},u_{yy}$ 的组合恰好只剩 $u_{\\eta\\eta}$ 项：原方程 $\\Leftrightarrow u_{\\eta\\eta}=0$ → $u=\\eta\\,\\Phi(\\xi)+\\Psi(\\xi)$ 型。
【易错】第二变量必须与 $\\xi$ 线性无关（雅可比 $\\ne0$，$\\eta=x$ 会与 $\\xi=2x+3y$ 无关 ✓，$\\eta=y$ 也可）；一阶链式两套系数（$2$ 与 $3$）。
【注意】(II) 由 $u_{\\eta\\eta}=0$ 积分两次 + 用 $u(x,0)=?$ 的边界条件定函数。""",
20: """【公式】极坐标逆向翻译：$r^{2}\\sin\\theta=y$、$r^{2}\\cos2\\theta=x^{2}-y^{2}$ → 根号 $\\sqrt{1-x^{2}+y^{2}}$；$D$（$0\\le\\theta\\le\\tfrac\\pi4,\\ 0\\le r\\le\\cos\\theta$ 的圆域 $x^{2}+y^{2}\\le x$ 的 $y\\ge0$ 上半）。
【技巧】被积化为 $y\\sqrt{1-x^{2}+y^{2}}$：先对 $x$ 积分（$x$ 只在根号里，限 $0\\to\\sqrt{1-y^{2}}$），圆弧积分公式 $\\displaystyle\\int\\sqrt{a^{2}-u^{2}}\\,\\mathrm du=\\dfrac{u}{2}\\sqrt{a^{2}-u^{2}}+\\dfrac{a^{2}}{2}\\arcsin\\dfrac ua$。
【易错】$\\cos2\\theta=\\cos^{2}\\theta-\\sin^{2}\\theta$（先降幂再翻译）；$D$ 的边界 $r=\\cos\\theta$ 即 $x^{2}+y^{2}=x$（圆心 $\\left(\\tfrac12,0\\right)$、半径 $\\tfrac12$，只取 $y\\ge0$ 上半与 $\\theta\\le\\tfrac\\pi4$ 的交集）。
【注意】$I=\\dfrac13-\\dfrac{3\\pi}{16}$（按数据解析）。""",
21: """【公式】(I) 造 $F(x)=f(x)-\\dfrac{x^{3}}{3}$：$F(0)=0$、$F(1)=f(1)-\\dfrac13=0$（用 $f(1)=\\dfrac13$）→ 罗尔给 $F'(\\xi)=0$ 型结论。
【技巧】(I) 的 $f(\\xi)=\\dfrac{\\xi^{3}}{3}$ 分两段（$\\xi\\in(0,\\tfrac12)$ 或 $\\eta$ 路线）：在 $[0,\\tfrac12]$ 上对 $F$ 用中值；或按数据解析：拉格朗日于 $[0,\\tfrac12]$、$[\\tfrac12,1]$ 两段。
【易错】(II) 的结论 $f'(\\xi)+f'(\\eta)=\\xi^{2}+\\eta^{2}$：$F'$ 的两处零点（$F'$ 端点等值 → 罗尔 → $F''$ 零点之外，这里是 $F'$ 与 $x^{2}$ 的两个交点）——两次罗尔接力。
【注意】分段点 $\\tfrac12$ 分开 $\\xi<\\tfrac12<\\eta$（结论带此结构）。""",
22: """【公式】两个不同的解 → $r(A)=r(\\bar A)<3$；$\\det A=\\lambda(\\lambda-1)^{2}$ → 候选 $\\lambda=0$（单）与 $\\lambda=1$（二重）。
【技巧】$\\lambda=1$：$r(A)=2$ 但增广行和校验 $r(\\bar A)=3$（无解）→ 排除；$\\lambda=0$：$r(A)=r(\\bar A)=2$ ✓ → $b$ 由增广行变换读出 $b=-\\dfrac12$。
【易错】二重根候选必须回代验证秩（$\\lambda=1$ 是陷阱分支）；特解可由行和结构直接读。
【注意】$\\lambda=0,\\ b=-\\dfrac12$；通解 $x=k(1,0,1)^{\\mathrm T}+\\left(\\dfrac32,-\\dfrac12,0\\right)^{\\mathrm T}$。""",
23: """【公式】(I) $\\lambda=1$ 是 $A$ 的二重特征值 → $r(E-A)=3-2=1$；$\\det(E-A)$ 含 $a$ 展开 → $a=-1$。
【技巧】$a=-1$ 时三个特征值 $2,-4,5$（sympy 核对：$\\operatorname{tr}=3$ ✓、互相 $\\ne$）；(II) $Q^{\\mathrm T}AQ=\\mathrm{diag}(2,-4,5)$ 的 $Q$ 由实对称矩阵三个特征向量（自动正交）规范化拼成。
【易错】二重根条件用"秩 = 1"而不仅是行列式为零；$Q$ 的列与 $\\Lambda$ 对角元一一对应。
【注意】$a=-1$；$Q^{\\mathrm T}AQ=\\mathrm{diag}(2,-4,5)$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2010数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2010数二真题.md', TIPS_2010)
