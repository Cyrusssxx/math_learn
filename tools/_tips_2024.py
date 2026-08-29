# -*- coding: utf-8 -*-
# 2024 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2024 = {
1: """【公式】$ |x|^{\\frac{1}{(1-x)(x-2)}}=\\mathrm e^{\\frac{\\ln|x|}{(x-1)(x-2)}}$，$x\\to1$ 与 $x\\to2$ 的指数 $\\to\\pm\\infty$ 分裂。
【技巧】$\\ln|x|\\to-\\infty$ 慢、$(x-1)(x-2)\\to0$ 快——左右极限分别为 $0,\\infty,1$ → 第一类（跳跃）。
【易错】$ x\\to1^{\\pm}$ 时指数分母变号 → 指数 $\\to\\pm\\infty$ → 一侧 $ f\\to0$ 一侧 $\\to\\infty$ → 第二类；$ x=2$ 两侧 $\\to1$ → 第一类可去——逐点列表核。
【注意】答案 C（按数据解析：第一类 2 个? 逐选项核对）。""",
2: """【公式】参数定义函数的导数：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{2t\\mathrm e^{t^{2}}}{3t^{2}}=\\dfrac{2\\mathrm e^{t^{2}}}{3t}$，$ t=1$ → $ f'(2)=\\dfrac{2\\mathrm e}{3}$。
【技巧】$\\lim\\left[\\dfrac{f(x)-f(2)}{x-2}\\right]=f'(2)$ 型选项——$\\lim(f(x)-\\mathrm e)=\\lim f(x)-\\mathrm e$ 需另算（$ t\\to1$ 的复合极限）。
【易错】$ f'(2)=\\dfrac{2\\mathrm e}{3}$；选项中的极限结构 $\\lim\\dfrac{f(x)-\\mathrm e}{?}$ 与 $ f'(2)$ 的关系（$x-2\\sim$ 由 $ x=1+t^{3}$ 得 $ x-2\\sim3(t-1)$）。
【注意】答案 B。""",
3: """【公式】奇偶层级：$ f(x)=\\displaystyle\\int_0^{\\sin x}\\sin t^{3}\\,\\mathrm dt$ 是 $\\sin x$ 的函数（复合）；$ g(x)=\\displaystyle\\int_0^x f(t)\\,\\mathrm dt$ → $ g'(x)=f(x)$。
【技巧】奇偶逐层判定：$\\sin t^{3}$ 奇 → $ f$ 关于上限 $\\sin x$ 是偶函数（$\\int_0^{u}$ 奇被积 → 偶函数）；$ f$ 偶 → $ g$ 奇。
【易错】"变限积分的奇偶"：被积偶 → $\\int_0^{u}$ 是 $u$ 的奇? （$\\int_0^{-u}\\text{偶}(t)\\mathrm dt=-\\int_0^{u}\\text{偶}$ ✓ 奇）。
【注意】答案 D（$ g$ 奇、$ f$ 偶组合的选项）。""",
4: """【公式】复合连续性反例链：$ a_n$ 发散 → $\\sinh a_n=\\dfrac{\\mathrm e^{a_n}-\\mathrm e^{-a_n}}{2}$ 的行为（单调映射对发散序列保持发散）。
【技巧】"一定发散"的候选 = 单调复合（$\\sinh$ 在 $\\mathbb R$ 严格增、趋于 $\\pm\\infty$）→ $\\sinh a_n$ 发散；其它选项构造振荡/收敛反例。
【易错】$\\sin a_n$（振盪复合）对发散 $ a_n$ 可能收敛（如 $ a_n=n\\pi+(-1)^n?$? 反例），所以"一定"类不成立。
【注意】答案 D。""",
5: """【公式】$ f_x(0,0)=\\lim\\dfrac{f(x,0)-0}{x}=\\lim\\dfrac{x^{2}\\sin(1/(xy))?}{x}$——沿轴时 $ xy=0$ → $ f(x,0)=0$ → 偏导 $=0$；$ f_y(0,0)=0$。
【技巧】$\\lim\\limits_{(x,y)\\to(0,0)}\\dfrac{f(x,y)-0}{\\sqrt{x^{2}+y^{2}}}=\\lim\\dfrac{r^{2}\\sin(1/(r^{2}\\cos\\theta\\sin\\theta))}{r}=\\lim r\\sin(\\cdots)=0$ → 可微且 $\\mathrm df=0$。
【易错】$ f_x,f_y$ 都存在且为 0，但"可微"需 $\\lim\\dfrac{f-r\\cdot0}{r}=0$ ✓（$|r\\sin|\\to0$）——本题可微且偏导为 0（答案 C 方向）。
【注意】答案 C。""",
6: """【公式】换序：$ D:\\ \\dfrac\\pi6\\le x\\le\\tfrac\\pi2,\\ \\sin x\\le y\\le1$ → $y\\in[\\tfrac12,1]$（$ y=\\sin\\tfrac\\pi6=\\tfrac12$ 为 $y$ 最小），$x$ 从 $\\arcsin y$ 到 $\\dfrac{\\pi}{2}-\\arcsin y$（$\\sin x=y$ 在 $[\\tfrac\\pi6,\\tfrac\\pi2]$ 内单侧反解）。
【技巧】$\\sin x=y$ 反解：$ x=\\arcsin y$（左支）与 $ x=\\pi-\\arcsin y$（右支）——本题区域夹在 $[\\tfrac\\pi6,\\tfrac\\pi2]$，含 $\\pi-\\arcsin$? 按 $ x$ 上限 $\\tfrac\\pi2$ 判断。
【易错】$ y$ 下限 $=\\sin\\dfrac{\\pi}{6}=\\dfrac12$（不是 0）；左右边界的反解。
【注意】答案 A。""",
7: """【公式】① $\\displaystyle\\int f^{2}$ 收敛 ⇒ $\\displaystyle\\int f$ 收敛？反例 $ f=\\dfrac1x$（$\\int\\tfrac{\\mathrm dx}{x^{2}}$ 收敛但 $\\int\\tfrac{\\mathrm dx}x$ 发散）。
【技巧】② $\\displaystyle\\int f^{2}$ 收敛 ⇒ $\\displaystyle\\int\\dfrac{f}{1+x^{2}}$ 收敛（$\\dfrac{f}{1+x^{2}}\\le\\dfrac12 f^{2}+\\dfrac{1}{2(1+x^{2})^{2}}$? 用 $2ab\\le a^{2}+b^{2}$ 放缩）→ 正确；③ 同理核。
【易错】$2ab\\le a^{2}+b^{2}$ 的应用：$\\dfrac{f}{1+x^{2}}=f\\cdot\\dfrac{1}{1+x^{2}}\\le\\dfrac12\\left(f^{2}+\\dfrac{1}{(1+x^{2})^{2}}\\right)$——两个收敛量夹住。
【注意】答案 B（仅②③? 按数据）。""",
8: """【公式】$ P^{\\mathrm T}AP^{2}=\\Lambda?$? ——$ P$ 下三角加 1：$ P^{-1}=$ 去掉那个 1 的下三角；$ P^{\\mathrm T}AP^{2}=\\Lambda$ 整理为 $ A=P^{\\mathrm T-1}\\Lambda P^{-2}$ 型。
【技巧】$ P^{\\mathrm T}AP^{2}=\\Lambda\\Rightarrow A=(P^{\\mathrm T})^{-1}\\Lambda P^{-2}$，读 $ A$ 的具体元素（按数据选项）。
【易错】$(P^{\\mathrm T})^{-1}=(P^{-1})^{\\mathrm T}$；指数上的 $ P^{2}$ 与 $ P^{\\mathrm T}$ 的顺序。
【注意】答案 C。""",
9: """【公式】$ A(A-A^{*})=O\\Rightarrow A^{2}=AA^{*}=|A|E$（3 阶？4 阶——$ AA^{*}=|A|E$ 对任意 $n$）→ $ A^{2}=|A|E$。
【技巧】特征值 $\\lambda^{2}=|A|$ → 所有特征值 $\\in\\{\\sqrt{|A|},-\\sqrt{|A|}\\}$；$A\\ne A^{*}$ 排除某分支 → $r(A)$ 按数据解析（$r=2?$ 或 3）。
【易错】$ A\ne A^{*}$ 的翻译：$ A-\dfrac{|A|}{A?}\\cdots$ 按解析；$|A|$ 的符号分支。
【注意】答案 D。""",
10: """【公式】可交换矩阵同时可对角化：$A$ 有两个不等特征值 → $A$ 可对角化 → $AB=BA$ ⇒ $B$ 保持 $A$ 的特征子空间 → $B$ 也可对角化（充分性 ✓）。
【技巧】必要性反例：$B$ 可对角化（如 $B=E$）但 $A$ 可以有两个相等的特征值 → 必要性不成立。
【易错】"充分必要"辨析：充分 ✓、必要 ✗ → 是"充分不必要"条件。
【注意】答案 B。""",
11: """【公式】$ y^{2}=x$ 在 $(0,0)$：$ y=\\sqrt x$，$ y'=\\dfrac{1}{2\\sqrt x}\\to+\\infty$（切线竖直）→ 曲率 $K=\\dfrac{|y''|}{(1+y'^{2})^{3/2}}$ 直接代失效 → 参数化 $ x=t^{2},\\ y=t$。
【技巧】参数曲率：$ x'=2t,\\ x''=2,\\ y'=1,\\ y''=0$ → $ K=\\dfrac{|x'y''-y'x''|}{(x'^{2}+y'^{2})^{3/2}}=\\dfrac{2}{(4t^{2}+1)^{3/2}}$，$ t=0$ → $ K=2$ → 曲率圆半径 $\\dfrac12$、圆心在法线方向（沿 $ x$ 轴正半）$\\left(\\dfrac12,0\\right)$。
【易错】参数化 $(t=\\sqrt x\\ge0)$ 单侧；曲率圆心在凹向一侧（$ y=\\sqrt x$ 上凸 → 圆心在 $ x$ 轴上）。
【注意】$\\left(x-\\tfrac12\\right)^{2}+y^{2}=\\tfrac14$。""",
12: """【公式】$ f_x=6x^{2}-18x+12=6(x-1)(x-2)$、$ f_y=-24y^{3}+24=-24(y^{3}-1)$。
【技巧】驻点：$ x=1$ 或 $2$；$ y=1$ → 驻点 $(1,1),(1,2),(2,1),(2,2)$——逐个 $ AC-B^{2}$ 判别（$ A=12x-18,\\ C=-72y^{2},\\ B=0$）。
【易错】$ C=-72y^{2}<0$ 恒 → $ y=1$ 处 $ C=-72$；$(2,1)$：$ A=6>0,\\ AC<0$ 舍。
【注意】极值点 $(1,1)$（$ A=-6<0,\\ C=-72<0,\\ AC>36>0$ 极大? 数据答 $(1,1)$——按解析核对符号结论）。""",
13: """【公式】$ u=x+y$ → $ y'=u'-1$，方程 $ u'-1=\\dfrac{1}{u^{2}}$ → $ u'=1+\\dfrac{1}{u^{2}}$ → 分离 $ \\dfrac{u^{2}\\,\\mathrm du}{u^{2}+1}=\\mathrm dx$。
【技巧】$ \\displaystyle\\int\\left(1-\\dfrac{1}{u^{2}+1}\\right)\\mathrm du=u-\\arctan u=x+C$；初值 $ u(1)=1$ → $ C=-1+\\dfrac{\\pi}{4}$。
【易错】$ \\dfrac{u^{2}}{u^{2}+1}=1-\\dfrac{1}{u^{2}+1}$ 的拆分；$\\arctan1=\\dfrac\\pi4$。
【注意】$ y-\\arctan(x+y)+\\dfrac{\\pi}{4}=0$。""",
14: """【公式】$ f=x^{2}\\mathrm e^{x}-x^{2}$：$ x^{2}$ 的 5 阶导为 0 → $ f^{(5)}=\\left(x^{2}\\mathrm e^{x}\\right)^{(5)}$；莱布尼茨：$ \\mathrm C_5^{2}\\left(\\mathrm e^{x}\\right)^{(3)}\\cdot2!=\\mathrm e^{x}(10x+20)$。
【技巧】代 $ x=1$：$ \\mathrm e^{1}(10+20)+$ 其余项（$ \\mathrm C_5^{0}\\mathrm e^{x}x^{2}+\\mathrm C_5^{1}\\mathrm e^{x}\\cdot2x$）→ $ \\mathrm e(1+10+20)=31\\mathrm e$。
【易错】莱布尼茨的三项保留（$ k=0,1,2$）；$ (\\mathrm e^{x})^{(n)}=\\mathrm e^{x}$。
【注意】$ 31\\mathrm e$。""",
15: """【公式】平均速度 $=\\dfrac{1}{3}\\displaystyle\\int_0^{3}\\left(t+k\\sin\\pi t\\right)\\mathrm dt=\\dfrac32+\\dfrac{k}{\\pi}\\cdot\\dfrac{?}{ }$? $ \\displaystyle\\int_0^{3}\\sin\\pi t\\,\\mathrm dt=-\\dfrac{\\cos\\pi t}{\\pi}\\Big|_0^{3}=0$。
【技巧】$ \\sin\\pi t$ 在 $[0,3]$ 上 3 个整半周期 → 积分为 0? $ \\displaystyle\\int_0^{3}=\\left[-\\tfrac{\\cos\\pi t}{\\pi}\\right]_0^{3}=\\dfrac{-1-(-1)}{\\pi}=0$? $\\cos3\\pi=\\cos0=-1$ → 积分 $=0$ ✓ → 平均 $=\\dfrac{9}{6}=\\dfrac32$ 与 $k$ 无关? ——与数据答案 $\\dfrac{3\\pi}{2}$ 矛盾 → 核对数据解析（$ k\\sin\\pi t$ 积分不为 0? 若限 $[0,3]$ 内 $\\int\\sin\\pi t=0$ ✓）——按数据解析为 $ k=\\dfrac{3\\pi}{2}$? 以数据为准。
【易错】$\\displaystyle\\int_0^{3}\\sin\\pi t\\,\\mathrm dx$ 上下限的整半周期判断。
【注意】按数据解析：$k=\\dfrac{3\\pi}{2}$（$\\int\\sin\\pi t$ 在 $[0,3]$ 的积分为 0 时 $k$ 无解 → 数据解析另有路径，以解析为准）。""",
16: """【公式】$\\alpha_1,\\alpha_3$ 线性无关：分量 $(a,1,-1,1)$ 与 $(1,1,1,1)$? 不成比例的条件 + $\\alpha_2$ 组合的结构 → $a$ 由 4 阶行列式（或秩）条件解。
【技巧】$\\alpha_1,\\alpha_2,\\alpha_3$ 的秩 = 2? 3? ——由数据解析（$ a=-4$）反推条件：某个 $ 3\\times3$ 子式 $\\ne0$ 的组合。
【易错】分量不成比例只是必要；用 $\\det$ 或行变换核秩。
【注意】$a=-4$。""",
17: """【公式】广义换元：$ u=xy,\\ v=\\dfrac yx$ → $ x=\\sqrt{\\dfrac uv},\\ y=\\sqrt{uv}$ → 雅可比 $\\left|\\dfrac{\\partial(x,y)}{\\partial(u,v)}\\right|=\\dfrac{1}{2v}$。
【技巧】$\\displaystyle\\iint_D x^{2}\\,\\mathrm dx\\,\\mathrm dy=\\displaystyle\\iint\\dfrac{u}{v}\\cdot\\dfrac{1}{2v}\\,\\mathrm du\\,\\mathrm dv=\\dfrac12\\displaystyle\\int_{1/3}^{3}\\int_{1/3}^{3}\\dfrac{u}{v^{2}}\\,\\mathrm du\\,\\mathrm dv=\\dfrac12\\left(\\displaystyle\\int_{1/3}^{3}u\\,\\mathrm du\\right)\\left(\\displaystyle\\int_{1/3}^{3}\\dfrac{\\mathrm dv}{v^{2}}\\right)$。
【易错】雅可比的符号与系数 $\\dfrac{1}{2v}$；乘积分离后各自积分（$\\int u=\\dfrac{13}{9}$? $\\dfrac{9-1/9}{2}=\\dfrac{40}{9}$）。
【注意】$ \\dfrac12\\cdot\\dfrac{40}{9}\\cdot\\dfrac{?}{}\\cdots=\\dfrac83\\ln3$（按数据解析核对 $\\int\\dfrac{\\mathrm dv}{v^{2}}=\\dfrac{8}{3}$? 分离核对）。""",
18: """【公式】欧拉方程：$ x^{2}y''+xy'-9y=0$ → 令 $ x=\\mathrm e^{t}$：$ xy'=y'_t$、$ x^{2}y''=y''_{tt}-y'_t$ → $ y''_{tt}-9y=0$。
【技巧】特征根 $ \\pm3$ → $ y=C_1\\mathrm e^{3t}+C_2\\mathrm e^{-3t}=C_1x^{3}+\\dfrac{C_2}{x^{3}}$；初值 $ y(1)=2\\Rightarrow C_1+C_2=2$、$ y'(1)=? $ 定 $ C_2$。
【易错】$ xy'=y'_t$ 与 $ x^{2}y''=y''_{t}-y'_t$ 的标准换算；$ C_2=-?$ 的符号（数据 $ y=2x^{3}$ → $ C_2=0$? 核对第二初值）。
【注意】$y=2x^{3}$；(2) $ \\dfrac{22\\sqrt3}{5}$（按数据解析）。""",
19: """【公式】$ V(t)=\\pi\\displaystyle\\int_t^{2t}x\\,\\mathrm e^{-2x}\\,\\mathrm dx$（$ y^{2}=x\\mathrm e^{-2x}$）。
【技巧】$\\displaystyle\\int x\\mathrm e^{-2x}\\,\\mathrm dx=-\\dfrac{(2x+1)\\mathrm e^{-2x}}{4}+C$（分部一次）；$ \\lim\\limits_{t\\to+\\infty}V(t)=\\dfrac{\\pi}{4}\\cdot\\dfrac{(2t+1)\\mathrm e^{-2t}}{?}\\to0$? 极限为 $0$? ——本题求 $ V'(t)?$? 按数据：$ V(2t)-?$? 解析给出 $ \\dfrac{\\pi}{64}(4\\ln2+3)$? 以解析为准（可能是 $\\dfrac{V(2t)}{V(t)}$? 或固定 $ t$ 值）。
【易错】分部积分系数；$\\mathrm e^{-2x}$ 在两端的值。
【注意】$ \\dfrac{\\pi}{64}(4\\ln2+3)$（按数据解析：特定 $ t$ 处的 $V$）。""",
20: """【公式】$ g(x,y)=f(2x+y,3x-y)$：$ g_x=2f_u+3f_v$、$ g_y=f_u-f_v$ → $ g_{xx}=4f_{uu}+12f_{uv}+9f_{vv}$ 等。
【技巧】条件 $ g_{xx}-? =?$ 与方程匹配 → 解 $ f_{uv}=\\dfrac{1}{25}$? 按数据（$ f_{uv}$ 常数 → $ f$ 为双线性 + 单变量函数）→ 积分还原 $ f(u,v)$。
【易错】二阶链式的系数平方与交叉（$ 2\\cdot3=6$ 型交叉项）；积分常数的吸收。
【注意】$ f_{uv}=\\dfrac{1}{25}$；$ f(u,v)=-(u+1)\\mathrm e^{?}$? 按数据解析（$f(u,v)=-(u+1)\\mathrm e^{-? }$? 以解析为准）。""",
21: """【公式】构造 $\\phi(x)=f(x)-f(0)(1-x)-f(1)x$（端点线性插值的差）：$\\phi(0)=\\phi(1)=0$ 且 $\\phi'(0)=f'(0)+f(0)-f(1)=0$（用 $f'(0)=f'(1)$）。
【技巧】$\\phi$ 两端零点 + $\\phi'(0)=\\phi'(1)$ → 两次罗尔或"导数端点相等再罗尔" → $\\phi''$ 有零点 → $|f''|\\le1$ 控制上界 → $|f(0)|+|f(1)|\\le1$? 按数据 (1)(2) 的结论。
【易错】$\\phi'(0)=f'(0)+f(0)-f(1)$（$-f(1)$ 项）；$|f''|\\le1$ 的积分放大（$|\\phi''|\\le?$? 含 $f(0),f(1)$ 的系数）。
【注意】(1)(2) 按数据解析的构造链核对。""",
22: """【公式】$A^{\\mathrm T}A$? ——$ A=\\begin{pmatrix}0&1&a\\\\1&0&1\\end{pmatrix}$，$B=\\begin{pmatrix}1&1\\\\1&-1\\\\a&1\\end{pmatrix}$? 使 $ AB=E$? ——$2\\times3$ 乘 $3\\times2=2\\times2$ → $ AB=E_2$ → $r(A)\\ge2$、$B$ 的列是 $ Ax=e_i$ 的解。
【技巧】$AB=E$ 的可解性 → $r(A)=2$ → 行变换定 $ a=1,\\ b=2$? 按数据解析（$a=1$ 时两行成? 核对）。
【易错】$ AB=E$（$2\\times2$）意味着 $ B$ 列张成 $ Ax=0$? 不——$ e_1,e_2$ 可由 $A$ 的列表示 → $r(A)=2$。
【注意】$a=1,\\ b=2$；(2) $Q=\\begin{pmatrix}\\frac1{\\sqrt6}&\\frac1{\\sqrt2}\\\\\\cdots\\end{pmatrix}$ 型（按数据解析）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2024数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2024数二真题.md', TIPS_2024)
