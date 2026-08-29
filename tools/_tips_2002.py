# -*- coding: utf-8 -*-
# 2002 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2002 = {
1: """【公式】连续 $\\Leftrightarrow\\lim\\limits_{x\\to0^+}f=f(0)$；$1-\\mathrm e^{u}\\sim-u$；$\\arcsin u\\sim u$。
【技巧】右极限 $\\dfrac{1-\\mathrm e^{ax^{2}}}{\\arcsin\\frac x2}\\sim\\dfrac{-ax^{2}}{x/2}=-2ax\\to0$——极限是 0，与 $a$ 无关，$a$ 只从左值 $f(0)=a$ 进入方程。
【易错】把右极限当成 $-2a$（忘了 $x\\to0$）然后解 $-2a=a$——分母是 $x/2$ 不是常数，比值趋于 0。
【注意】$a=0$ 时 $f\\equiv0$，两段自然连续。""",
2: """【公式】反常积分面积：$S=\\displaystyle\\int_{0}^{+\\infty}x\\mathrm e^{-x}\\,\\mathrm dx=\\Gamma(2)=1!$。
【技巧】分部积分 $\\displaystyle\\int x\\mathrm e^{-x}\\,\\mathrm dx=-(x+1)\\mathrm e^{-x}+C$，端点值：$x\\to+\\infty$ 时 $\\dfrac{x+1}{\\mathrm e^{x}}\\to0$（指数吃掉多项式）。
【易错】"曲线下方、$x$ 轴上方"的图形语言 → 翻译成 $\\displaystyle\\int_0^{+\\infty}y\\,\\mathrm dx$；$y=0$ 线别写成别的。
【注意】反常积分先判收敛（$\\mathrm e^{-x}$ 衰减）再算值。""",
3: """【公式】观察型：$(yy')'=y'^{2}+yy''=0\\Rightarrow yy'=C$——比标准降阶快一步。
【技巧】"不显含 $x$"用 $y''=p\\dfrac{\\mathrm dp}{\\mathrm dy}$ 是通用降阶；但见到 $yy''+y'^{2}$ 先试试整体导数。
【易错】$p=0$（常函数）分支不满足 $y'(0)=\\tfrac12$，舍弃时要说一句。
【注意】初值：$yy'=C$ 代 $y=1,y'=\\tfrac12$ 得 $C=\\tfrac12$；再积 $y\\,\\mathrm dy=\\tfrac12\\mathrm dx$ → $y^{2}=x+1$，取正根。""",
4: """【公式】黎曼和：$\\lim\\limits_{n\\to\\infty}\\dfrac1n\\displaystyle\\sum_{k=1}^{n}f\\!\\left(\\tfrac{k\\pi}{n}\\right)=\\dfrac{1}{\\pi}\\displaystyle\\int_0^{\\pi}f(t)\\,\\mathrm dt$。
【技巧】$\\sqrt{1+\\cos t}=\\sqrt2\\left|\\cos\\tfrac t2\\right|$（半角公式），$t\\in(0,\\pi)$ 内取 $\\sqrt2\\cos\\tfrac t2$。
【易错】$\\dfrac1n$ 要配成 $\\dfrac{\\pi}{n}\\cdot\\dfrac{1}{\\pi}$——系数 $\\dfrac1\\pi$ 别丢。
【注意】$\\displaystyle\\int_0^{\\pi}\\cos\\tfrac t2\\,\\mathrm dt=2$，答案 $\\dfrac{2\\sqrt2}{\\pi}$。""",
5: """【公式】特征值三条校验：$\\sum\\lambda_i=\\operatorname{tr}A$、$\\prod\\lambda_i=\\det A$、$\\text{二阶主子式之和}=$ 一次项系数。
【技巧】填空题先算 $\\operatorname{tr}A=4$、$\\det A=0$ 预判"一个非零 + 两个零"，再展开 $|\\lambda E-A|$ 确认。
【易错】矩阵元素抄错一个符号（$A_{33}$ 是 $2$）全盘皆输；展开 $2\\times2$ 子式时的负号。
【注意】$|\\lambda E-A|=\\lambda^{2}(\\lambda-4)$：零特征值是二重根。""",
6: """【公式】"线性主部" = 微分：$\\mathrm dy=f'(x^{2})\\cdot2x\\,\\mathrm dx$。
【技巧】两个负号（$x=-1$ 使 $2x=-2$、$\\Delta x=-0.1$）相乘为正，$0.1=f'(1)\\cdot0.2$。
【易错】链式 $\\dfrac{\\mathrm dy}{\\mathrm dx}=f'(x^{2})\\cdot2x$ 的 $2x$ 因子最容易丢；$f'$ 的自变量是 $x^{2}=1$。
【注意】答案 $f'(1)=0.5$，选 D。""",
7: """【公式】变限积分奇偶性：被积函数 $g(t)$ 奇 → $F(x)=\\displaystyle\\int_0^x g$ 偶；$g$ 偶 → $F$ 奇。
【技巧】逐项判内层：$f(t^{2})$ 偶 → A 的 $F$ 奇；$f(t)\\cdot[f(t)+f(-t)]$ 中括号内恒偶 → 整体奇 → D 的 $F$ 必偶。
【易错】"必为偶"要求对**任意**连续 $f$ 成立——含 $f(-t)$ 的对称结构才保偶，含 $f(t)$ 单独项的不能保证。
【注意】B、C 的被积函数一般既非奇又非偶，不选。""",
8: """【公式】初值代方程：$y''(0)+py'(0)+qy(0)=\\mathrm e^{0}=1\\Rightarrow y''(0)=1$；泰勒 $y=\\tfrac{y''(0)}{2}x^{2}+o(x^{2})$。
【技巧】不必解出 $p,q$、不必解方程——$\\dfrac{\\ln(1+x^{2})}{y(x)}\\sim\\dfrac{x^{2}}{x^{2}/2}=2$。
【易错】$\\mathrm e^{3x}$ 在 $x=0$ 取值是 $1$ 不是 $3$；$y(0)=y'(0)=0$ 使一阶项消失。
【注意】"特解"只是条件，极限用局部泰勒即够。""",
9: """【公式】反证：若 $\\lim\\limits_{x\\to+\\infty}f'=l>0$，则充分远处 $f'>\\tfrac l2\\Rightarrow f\\to+\\infty$ 与有界矛盾（$l<0$ 同理）。
【技巧】"必有"型选项逐个找反例排除：$f=\\dfrac{\\sin x^{2}}{x}$ 有界可导但 $f'$ 不趋于 0（振幅 2 的振盪），可打掉多个选项。
【易错】"有界 + 可导"推不出 $f'\\to0$——振盪反例是本题灵魂。
【注意】B 的正路：极限存在时只能 $l=0$。""",
10: """【公式】表示性的秩语言：$\\beta_2$ 不可由 $\\alpha$ 组表示 $\\Leftrightarrow r(\\alpha_1,\\alpha_2,\\alpha_3,\\beta_2)=4$（升维）；$\\beta_1$ 可表示 = 无新维度。
【技巧】含 $\\beta_2$ 的组合向量（$\\beta_2+k\\beta_1$）：加上可表示的 $k\\beta_1$ 不改变秩 → 对任意 $k$ 线性无关；含 $\\beta_1$ 的组合（$\\beta_1+k\\beta_2$）凑不出新维度 → 4 向量必相关。
【易错】$k=0$ 特例也涵盖在"任意常数"里——结论须对 $k=0$ 同样成立。
【注意】选"含 $\\beta_2$ 组合线性无关"的那个选项。""",
11: """【公式】极坐标 → 参数方程：$x=r\\cos\\theta,y=r\\sin\\theta$，$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{\\mathrm dy/\\mathrm d\\theta}{\\mathrm dx/\\mathrm d\\theta}$。
【技巧】本题两个导数在 $\\theta=\\tfrac\\pi6$ 处恰好相等（都是 $\\dfrac{\\sqrt3-1}2$）→ 斜率恰为 1，属"设计好的巧合"，算出 1 先自查再自信。
【易错】$\\dfrac{\\mathrm dy}{\\mathrm d\\theta}=\\sin^{2}\\theta+(1-\\cos\\theta)\\cos\\theta$ 展开成 $1+\\cos\\theta-2\\cos^{2}\\theta$；切点坐标分母是 4。
【注意】切线 $y=x+\\dfrac{5-3\\sqrt3}{4}$，法线 $y=-x+\\dfrac{\\sqrt3-1}{4}$（斜率 $\\pm1$）。""",
12: """【公式】跨段变限积分：$F(x)=\\displaystyle\\int_{-1}^{0}(2t+\\tfrac32t^{2})\\,\\mathrm dt+\\int_0^{x}\\dfrac{t\\mathrm e^{t}}{(\\mathrm e^{t}+1)^{2}}\\,\\mathrm dt$（$0\\le x<1$）。
【技巧】第二段被积函数认出 $\\dfrac{t\\mathrm e^{t}}{(\\mathrm e^{t}+1)^{2}}=-t\\,\\mathrm d\\!\\left(\\dfrac{1}{\\mathrm e^{t}+1}\\right)$ → 分部积分。
【易错】$x<0$ 与 $x\\ge0$ 的表达式都写全；$x=0$ 处两段拼接连续（分段函数的变限积分天然连续）。
【注意】$\\displaystyle\\int_0^{x}\\dfrac{t\\mathrm e^{t}}{(\\mathrm e^{t}+1)^{2}}\\mathrm dt=\\dfrac{x}{\\mathrm e^{x}+1}-\\ln\\dfrac{2}{\\mathrm e^{x}+1}-\\dfrac{0}{2}+\\ln2\\cdots$ 按部就班算。""",
13: """【公式】对数差商识别：$\\lim\\limits_{h\\to0}\\dfrac1h\\ln\\dfrac{f(x+hx)}{f(x)}=\\dfrac{f'(x)}{f(x)}$（$\\ln$ 差 $\\div h\\to$ 导数除函数）。
【技巧】得 $\\dfrac{f'}{f}=\\dfrac{1}{x^{2}}$？不对——右端是 $\\dfrac{1}{x^{2}}$ 的负值？逐题代入题给右端再分离变量 $\\ln f=C-\\dfrac1x$。
【易错】定常数 $C$ 用 $\\lim\\limits_{x\\to+\\infty}f=1\\Rightarrow C=0$；别忘 $x>0$。
【注意】答案 $f=\\mathrm e^{-1/x}$。""",
14: """【公式】一阶线性 $y'-\\dfrac2x y=-1$，积分因子 $x^{-2}$：$\\left(\\dfrac{y}{x^{2}}\\right)'=-\\dfrac{1}{x^{2}}$ → $y=x+Cx^{2}$。
【技巧】通解含参数 $C$ → 体积 $V(C)=\\pi\\displaystyle\\int_1^{2}(x+Cx^{2})^{2}\\,\\mathrm dx$ 是 $C$ 的二次函数，$\\dfrac{\\mathrm dV}{\\mathrm dC}=0$ 得 $C=-\\dfrac{75}{124}$。
【易错】旋转体被积的是 $y^{2}$ 不是 $y$；$\\displaystyle\\int_1^{2}x^{4}\\,\\mathrm dx=\\dfrac{31}{5}$ 别算成 $\\dfrac{32}{5}$。
【注意】最优解 $y=x-\\dfrac{75}{124}x^{2}$。""",
15: """【公式】静水压力微元 $\\mathrm dP=\\rho g\\cdot$（水深）$\\times$（水平条面积）；水平条面积 = $2x\\,\\mathrm dy$（用对称轴）。
【技巧】坐标系建在抛物线顶点，$x^{2}=2py$ 的开口方向与 $p$ 的符号按图定；压力比 5:4 列成两个积分之比约分。
【易错】水深是从水面（闸门上端）往下量，坐标 $y$ 与深度的换算差一个 $h$；抛物线段与矩形段的面积微元分开列。
【注意】解出 $h=2\\,\\mathrm m$（$y^{2}=2px$ 的参数 $p$ 由"顶点在下端"几何关系定）。""",
16: """【公式】均值不等式造上界：$x_{n+1}=\\sqrt{x_{n}(3-x_{n})}\\le\\dfrac{x_{n}+(3-x_{n})}{2}=\\dfrac32$。
【技巧】单调性看 $x_{n+1}^{2}-x_{n}^{2}=x_{n}(3-2x_{n})$——在 $x_n\\ge\\tfrac32$ 上减、$\\le\\tfrac32$ 上增，配合"首个元素起就 $<\\tfrac32$"得整体递增。
【易错】上界是 $\\dfrac32$ 不是 3；归纳要两个方向（有界 + 单调）都写。
【注意】极限方程 $x=\\sqrt{x(3-x)}$ → $x^{2}=3x-x^{2}$ → $x=\\dfrac32$。""",
17: """【公式】左边：中值 $\\dfrac{\\ln b-\\ln a}{b-a}=\\dfrac1\\xi$（$a<\\xi<b$），$\\dfrac1\\xi>\\dfrac1b$，再证 $\\dfrac1b>\\dfrac{2a}{a^{2}+b^{2}}\\iff(b-a)^{2}>0$。
【技巧】右边 "$\\sqrt{ab}$" 处理：比值代换 $u=\\dfrac ba>1$，化成单变量 $\\ln u<\\sqrt u-\\dfrac1{\\sqrt u}$，构造 $h(u)$ 求导 $h'(u)=\\dfrac{(\\sqrt u-1)^{2}}{2u^{3/2}}>0$。
【易错】$\\xi$ 与 $\\sqrt{ab}$ 的大小关系不能凭中值定理直接断言——右半必须构造函数，不能放缩糊弄。
【注意】左半是"中值 + 一步代数"，右半是"代换 + 构造"，两种手法一次卷齐。""",
18: """【公式】泰勒：$f(kh)=f(0)+khf'(0)+\\dfrac{k^{2}h^{2}}{2}f''(0)+o(h^{2})$；$o(h^{2})$ 的代数：$\\lambda_1f(h)+\\lambda_2f(2h)+\\lambda_3f(3h)-f(0)=o(h^{2})$ 逐阶匹配。
【技巧】三阶匹配 = 三个线性方程：$\\sum\\lambda_k=1$、$\\sum k\\lambda_k=0$、$\\sum k^{2}\\lambda_k=0$（$f(0)\\ne0,f'(0)\\ne0,f''(0)\\ne0$ 保证右端非零、方程非退化）。
【易错】唯一性靠系数行列式 $\\ne0$（范德蒙型 $(2-1)(3-1)(3-2)=2$）——只证存在不证唯一要扣分。
【注意】消元解出 $\\lambda_1=3,\\lambda_2=-3,\\lambda_3=1$。""",
19: """【公式】可逆性证明套路：凑 $X\\cdot Y=kE$。本题 $2B=AB-4A\\Rightarrow(A-2E)B=4A$，再添 $(B-4E)$：$(A-2E)(B-4E)=8E$。
【技巧】第一问逆用：$\\dfrac{B-4E}8=(A-2E)^{-1}$；第二问直接 $X=(A-2E)^{-1}B=\\dfrac{(B-4E)B}{8}=\\dfrac{B^{2}-4B}{8}$。
【易错】$(A-2E)B=4A$ 右端含 $A$，此时还**不能**断言可逆——必须再凑出 $=8E$ 的右端。
【注意】$B$ 对称 → $B^{2}-4B$ 对称 → $X$ 对称，可作检验。""",
20: """【公式】解的结构：$Ax=\\beta$ 通解 = 特解 + $k\\cdot$（$Ax=0$ 的基础解系）；$r(A)=3$（4 元）→ 一个自由变量。
【技巧】系数翻译直接读解：$\\alpha_1=2\\alpha_2-\\alpha_3\\Rightarrow(1,-2,1,0)^{\\mathrm T}$ 是 $Ax=0$ 的解；$\\beta=3\\alpha_2+\\alpha_4\\Rightarrow(0,3,0,1)^{\\mathrm T}$ 是特解。
【易错】$\\alpha_1=2\\alpha_2-\\alpha_3$ 的系数带符号（$\\alpha_3$ 系数是 $-1$）；$\\beta$ 的和式里没有 $\\alpha_1$、$\\alpha_3$。
【注意】通解 $x=k(1,-2,1,0)^{\\mathrm T}+(0,3,0,1)^{\\mathrm T}$（$k$ 任意）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2002数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2002数二真题.md', TIPS_2002)
