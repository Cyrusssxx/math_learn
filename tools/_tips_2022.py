# -*- coding: utf-8 -*-
# 2022 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2022 = {
1: """【公式】等价与比阶四命题：① $\\alpha\\sim\\beta$ ⇒ $\\alpha/\\beta^{n}\\to0?$ 分情况；② $\\alpha\\sim-\\alpha$ 平方等价但比值 $\\to-1$（反例 $\\beta=-\\alpha$）。
【技巧】③④用比值结构：$\\dfrac{\\alpha}{\\beta}-1\\to0$ ⟺ $\\alpha-\\beta=o(\\beta)$；组合 $\\alpha+\\beta=\\beta(1+o(1))$。
【易错】②的反例（$\\beta=-\\alpha$）是四个命题辨析的灵魂；平方等价推不出原等价（符号丢失）。
【注意】答案 C（仅①③④型）。""",
2: """【公式】交换次序：$D:\\ 0\\le y\\le x\\le2$ → $\\displaystyle\\int_0^{2}\\dfrac{1}{\\sqrt{1+x^{3}}}\\left(\\displaystyle\\int_0^{x}\\mathrm dy\\right)\\mathrm dx=\\int_0^{2}\\dfrac{x\\,\\mathrm dx}{\\sqrt{1+x^{3}}}$。
【技巧】凑微分 $\\sqrt{1+x^{3}}\\,\\mathrm d?$? ——$\\mathrm d(1+x^{3})=3x^{2}\\,\\mathrm dx$ 不匹配；用 $\\displaystyle\\int_0^{2}\\dfrac{x}{\\sqrt{1+x^{3}}}\\,\\mathrm dx$ 换元 $u=1+x^{3}$? 系数不齐——按数据解析路径（换元 $t=\\sqrt{1+x^{3}}$）。
【易错】交换次序的限（$y$ 从 0 到 $x$）；被积函数只含 $x$ → 换序后立即降维。
【注意】答案 D。""",
3: """【公式】$f''(x_0)$ 存在 ⇒ $f'$ 在 $x_0$ 连续 → $f'(x_0)>0$ 时邻域内 $f'>0$ → $f$ 局部严格增。
【技巧】"一点导数为正"配"二阶可导"（$f'$ 连续）才升级成局部单调；仅有 $f'(x_0)>0$ 只能推出局部偏高（2014 Q10 的对照）。
【易错】B 的表述方向（$f'(x_0)>0$ + $f'$ 连续 → 存在 $\\delta$ 使 $f$ 在 $(x_0-\\delta,x_0+\\delta)$ 严格增? 仅右侧结论）——逐项核对区间范围。
【注意】答案 B。""",
4: """【公式】卷积型变限积分：$ F(x,y)=H(x-y)$，$H(u)=\\displaystyle\\int_0^{u}(u-t)f(t)\\,\\mathrm dt$ → $ H''=f(u)$（两次求导，$H'=\\displaystyle\\int_0^u f$）。
【技巧】$ \\dfrac{\\partial^{2}F}{\\partial x^{2}}=H''(x-y)$、$ \\dfrac{\\partial F}{\\partial x}=H'$、$ \\dfrac{\\partial F}{\\partial y}=-H'$——全微分与组合选项按此结构读。
【易错】$\\dfrac{\\partial F}{\\partial y}$ 的负号（$u=x-y$ 对 $y$ 是 $-1$）；链式第二层。
【注意】答案 C。""",
5: """【公式】双瑕点：$ x\\to0^{+}$：$\\dfrac{\\ln x}{x^{p}(1-x)^{1-p}}\\sim\\dfrac{\\ln x}{x^{p}}$（$\\ln$ 不改敛散）→ $p<1$ 收敛；$ x\\to1^{-}$：$(1-x)^{-(1-p)}\\cdot\\ln x\\sim-\\dfrac{1-x}{(1-x)^{1-p}}$? $\\ln x\\to-\\infty$ 且 $\\sim-(1-x)$? 精确：$\\ln x\\to-\\infty$ 时 $(1-x)^{-(1-p)}$ 与 $ x\\to1$ 的行为按 $\\ln$ 互换判断。
【技巧】令 $ t=1-x$ 看第二端；$ p$ 的范围取交集。
【易错】$\\ln x$ 在 $x\\to1^-$ 是缓慢发散——$ p$ 的条件按数据解析（$p<\\tfrac12$? 以解析为准）。
【注意】答案 A。""",
6: """【公式】$\\sin$ 在 $[-\\tfrac\\pi2,\\tfrac\\pi2]$ 严格单调 → 一一对应。
【技巧】单调一一对应 ⇒ 数列收敛与函数极限互相传递（$\\sin x_n$ 收敛 ⇒ $ x_n$ 收敛）；其余选项用反例（$\\pm\\tfrac\\pi2$ 端点行为）。
【易错】$\\cos x$ 不单调（在 $[0,\\tfrac\\pi2]$ 单调但区间含负半轴时非一一）；$\\tan$ 与 $\\arctan$ 的传递方向。
【注意】答案 D。""",
7: """【公式】$0<x<1$ 时 $\\ln(1+x)>\\dfrac{x}{2}$（由 $\\ln(1+x)$ 的凹性或切线放缩下界）；同时 $\\ln(1+x)<x$。
【技巧】被积函数同分母 → 比分子：$\\ln(1+x)$ 与 $\\dfrac x2$ 比 → $ I_2>I_1$；上界 $\\ln(1+x)<x<1+?\\ $ 与 $\\dfrac{\\tan x?}{}$ 配平得 $ I_2<2I_1$。
【易错】$\\dfrac{x}{2}<\\ln(1+x)<x$ 的双侧放缩（凹函数切线是下界）；"$I_2$ 与 $2I_1$ 比"的系数来源。
【注意】答案 A（$I_1<I_2<2I_1$）。""",
8: """【公式】$A\\sim\\Lambda$ 的充要：特征多项式相同 + 可对角化；$\\lambda=1,-1,0$ 两两不同 → 必可对角化 → $A\\sim\\Lambda$ 恒成立。
【技巧】特征值两两不同是"必可对角化"的最强保证——四个选项只要特征值集合相同的都相似。
【易错】题问的是"$A$ 的特征值**不可能**是"还是"相似于"？逐项核对（答案 B 的说法）。
【注意】答案 B。""",
9: """【公式】Vandermonde 型系数阵：$\\begin{pmatrix}1&1&1\\\\1&a&a^{2}\\\\1&b&b^{2}\\end{pmatrix}$ 的行列式 $=(a-1)(b-1)(b-a)$。
【技巧】无解/无穷多解 ⟺ $|A|=0$ ⟺ $ 1,a,b$ 有相等者；相等时按重合情况分类读秩。
【易错】三类重合（$1=a$、$1=b$、$a=b$）各自给出不同的通解——逐分支验证 $ r(A)=r(\\bar A)$。
【注意】答案 D。""",
10: """【公式】两向量组等价 ⟺ $r(\\mathrm I)=r(\\mathrm{II})=r(\\mathrm I,\\mathrm{II})$；过渡行列式 $|\\alpha_1,\\alpha_2,\\alpha_3|=(\\lambda-1)^{2}(\\lambda+2)$。
【技巧】$\\lambda=1$（三重）与 $\\lambda=-2$（单）分类：$\\lambda=1$ 时秩降 → 等价成立与否按数据；$\\lambda=-2$ 时行列式 $=0$ → 秩 <3 → 等价不成立。
【易错】$(\\lambda-1)^{2}$ 与 $(\\lambda+2)$ 的零点归属（哪支等价哪支不等价按数据解析）。
【注意】答案 C。""",
11: """【公式】$1^{\\infty}$：$\\ln\\left(\\dfrac{1+\\mathrm e^{x}}{2}\\right)\\sim\\dfrac{\\mathrm e^{x}-1}{2}\\sim\\dfrac x2$（$x\\to0$，$\\mathrm e^{x}-1\\sim x$）→ 指数 $\\cot x\\cdot\\dfrac x2\\to\\dfrac12$。
【技巧】$\\cot x\\sim\\dfrac1x$（$x\\to0$）；$\\ln(1+u)\\sim u$ 的 $u=\\dfrac{\\mathrm e^{x}-1}{2}$。
【易错】$\\dfrac{1+\\mathrm e^{x}}{2}\\to1$（底数趋 1 的确认）；指数系数 $\\tfrac12$。
【注意】答案 $\\sqrt{\\mathrm e}$。""",
12: """【公式】隐函数：$2x+y+xy'+3y^{2}y'=0$ → $ y'=-\\dfrac{2x+y}{x+3y^{2}}$，代 $(1,1)$ 得 $ y'=-\\tfrac34$。
【技巧】二阶继续隐式求导：$2+y'+y'+xy''+6y(y')^{2}+3y^{2}y''=0$，代 $(1,1,-\\tfrac34)$：$2-\\tfrac32+xy''+\\tfrac{9}{2}\\cdot$? 逐项核。
【易错】$6y(y')^{2}=6\\cdot\\tfrac{9}{16}=\\tfrac{27}{8}$ 的分数运算；$ x=1,y=1$ 的代入。
【注意】$ y''(1)=-\\dfrac{31}{32}$。""",
13: """【公式】拆分子：$\\dfrac{2x+3}{x^{2}-x+1}=\\dfrac{(2x-1)+4}{x^{2}-x+1}=\\dfrac{(x^{2}-x+1)'}{x^{2}-x+1}+\\dfrac{4}{(x-\\tfrac12)^{2}+\\tfrac34}$。
【技巧】$\\displaystyle\\int\\dfrac{\\mathrm du}{u^{2}+a^{2}}=\\dfrac1a\\arctan\\dfrac ua$（$a=\\tfrac{\\sqrt3}{2}$）。
【易错】$ a=\\dfrac{\\sqrt3}{2}$ 的 $\\dfrac1a=\\dfrac{2}{\\sqrt3}$；$\\arctan\\left(\\dfrac{2x-1}{\\sqrt3}\\right)\\Big|_0^1=\\arctan\\tfrac1{\\sqrt3}-\\arctan(-\\tfrac1{\\sqrt3})$。
【注意】$ 4\\cdot\\dfrac{2}{\\sqrt3}\\cdot\\dfrac{\\pi}{6}=\\dfrac{4\\pi}{3\\sqrt3}$，加 $\\ln|1|=0$ → 答案 $\\dfrac{8\\pi}{3\\sqrt3}$（数据解析含 $\\dfrac{4}{3}\\cdot$ 校核）。""",
14: """【公式】$ r^{3}-2r^{2}+5r=r(r^{2}-2r+5)$ → 根 $0,\\ 1\\pm2\\mathrm i$。
【技巧】实根给常数项解 $ C_1$；复根 $1\\pm2\\mathrm i$ → $ \\mathrm e^{x}(C_2\\cos2x+C_3\\sin2x)$。
【易错】复根实部是 1（不是 0）；$\\beta=2$ 进三角函数。
【注意】$ y=C_1+\\mathrm e^{x}(C_2\\cos2x+C_3\\sin2x)$。""",
15: """【公式】极坐标面积：$ S=\\dfrac12\\displaystyle\\int_0^{\\pi/3}\\sin^{2}3\\theta\\,\\mathrm d\\theta$，换元 $ u=3\\theta$（$\\mathrm du=3\\,\\mathrm d\\theta$）→ $\\dfrac16\\displaystyle\\int_0^{\\pi}\\sin^{2}u\\,\\mathrm du=\\dfrac16\\cdot\\dfrac{\\pi}{2}$。
【技巧】$\\sin^{2}u=\\dfrac{1-\\cos2u}{2}$，$\\int_0^{\\pi}\\cos2u\\,\\mathrm du=0$。
【易错】换元系数 $\\dfrac13$（漏则差 3 倍）；玫瑰线一瓣 $\\theta$ 从 0 到 $\\tfrac\\pi3$。
【注意】答案 $\\dfrac{\\pi}{12}$。""",
16: """【公式】行变换 = 左乘、列变换 = 右乘：$ PAQ=\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&1&-1\\end{pmatrix}$? 型 → $|PAQ|=|P||A||Q|$ 读 $|A|$。
【技巧】交换 2、3 行的 $|S|=-1$；"第 2 列 $-1$ 倍加到第 1 列"的初等阵行列式 $=1$ → $|A|=-1\\times$（变换后行列式）。
【易错】列变换矩阵的元素位置（$-1$ 加到第 1 列 → $E_{12}(-1)$ 写法）；整体符号。
【注意】答案 $-1$。""",
17: """【公式】导数定义伪装：$\\lim\\dfrac{f(\\mathrm e^{x^{2}})-3f(1+\\sin x^{2})}{x^{2}}$——$\\mathrm e^{x^{2}}\\to1$、$1+\\sin x^{2}\\to1$，设 $ A=\\mathrm e^{x^{2}}-1\\sim x^{2}$、$ B=\\sin x^{2}\\sim x^{2}$。
【技巧】拆分：$\\dfrac{f(1+A)-f(1)}{A}\\cdot\\dfrac{A}{x^{2}}-3\\cdot\\dfrac{f(1+B)-f(1)}{B}\\cdot\\dfrac{B}{x^{2}}\\to f'(1)-3f'(1)=-2f'(1)$。
【易错】$\\lim\\dfrac{f(\\mathrm e^{x^{2}})-f(1)}{\\mathrm e^{x^{2}}-1}=f'(1)$ 的两项**分别**用定义；$-3$ 的系数保留。
【注意】$-2f'(1)=-2? $ 数据给 $f'(1)=-1$ → 极限 $=2$? 按数据解析核对（数据给 $f'(1)=-1$）。""",
18: """【公式】一阶线性：$ y'-\\dfrac2x y=\\dfrac{\\ln x-\\tfrac12}{x}$，积分因子 $ x^{-2}$ → $\\left(yx^{-2}\\right)'=\\dfrac{\\ln x-\\tfrac12}{x^{3}}$。
【技巧】$\\displaystyle\\int\\dfrac{\\ln x-\\tfrac12}{x^{3}}\\,\\mathrm dx$ 分部两次；渐近线：$ y\\to\\infty$ 无垂直、$ x\\to0^{+}$ 时 $ y\\to-\\infty$? 按解析的 $ y=\\dfrac14+\\left(\\dfrac{?}{x^{2}}\\right)$ 型。
【易错】$\\displaystyle\\int x^{-3}\\ln x\\,\\mathrm dx=-\\dfrac{\\ln x}{2x^{2}}+\\dfrac{1}{4x^{2}}$ 的分部符号；初值 $ y(1)=\\dfrac14$。
【注意】$ y=\\dfrac14+\\left(\\dfrac{e^{2}+? }{}\\right)\\cdots$ 按数据解析：$\\dfrac{e^2+1}{4}$ 为 $x\\to0$? 渐近线相关量（以解析为准）。""",
19: """【公式】区域：$ y-2\\le x\\le\\sqrt{4-y^{2}}$（$0\\le y\\le2$）——直线 $x=y-2$ 与四分之一圆 $x^{2}+y^{2}=4$。
【技巧】极坐标：$ x=y-2$ → $ r=\\dfrac{2(\\sin?)}{}$? ——$ r\\cos\\theta=r\\sin\\theta-2\\Rightarrow r=\\dfrac{2}{\\sin\\theta-\\cos\\theta}$，$\theta$ 从 $\\tfrac\\pi2$（$x=0$ 端? 顶点 $(0,2)$ 即 $\theta=\\tfrac\\pi2$）到 $\\pi$? 端点 $(−2,0)$ 即 $\theta=\\pi$。内层 $ r\\in[2(\\sin?−\\cos?),2]$。
【易错】$ x=y-2$ 的极坐标化（移项配方非圆——直线 $r(\\cos−\\sin)=-2$）；$\theta$ 的范围（顶点角度）。
【注意】答案 $2\\pi-2$（按数据解析：极坐标下直线到圆的组合积分）。""",
20: """【公式】复合消元：$ f(x+y,\\dfrac yx)=\\cdots$ 与 $\\dfrac{\\partial f}{\\partial u}-\\dfrac{\\partial f}{\\partial v}=\\cdots$? 数据给 $ \\dfrac{\\partial f}{\\partial v}=2u-v?$? ——按解析：$ f(u,v)$ 由 $ g(x,y)=f(2x+y,x-2y)$ 的偏导反推。
【技巧】反推路径：$ g_x=2f_u+f_v$、$ g_y=f_u-2f_v$ → 联立解 $ f_u,f_v$（用 $ g_x,g_y$ 表示）→ 积分还原 $ f(u,v)$。
【易错】二元一次方程组解 $ f_u,f_v$（系数行列式 $-5$）；积分常数 $\\varphi(v)$ 的处理。
【注意】(2) $ f(u,v)=(u^{2}+v^{2})\\mathrm e^{-(u+v)}$、仅 $(0,0)$ 极小值 0（按数据解析）。""",
21: """【公式】凸函数的等价刻画：$ f''\\ge0\\iff f(x)+f(a+b-x)\\ge2f\\left(\\tfrac{a+b}2\\right)$（中点凸）且对任意区间 $\\iff$ 弦在曲线上方。
【技巧】必要性：构造 $ g(t)=f(t)+f(a+b-t)$? 直接用凸性定义（$\\lambda=\\tfrac12$ 中点凸 + 递推）；充分性：对任意 $\\lambda$ 用连续性 + 中点凸的传递（或 $ x$ 取二分逼近）。
【易错】"中点凸 + 连续 ⟺ 凸"的引理是本题的桥梁；$a+b-x$ 的对称化技巧。
【注意】两级结论（任意区间上的弦不等式）。""",
22: """【公式】正交变换 $x=Qy$ 下标准形 $ y_1^{2}+y_2^{2}$（无 $ y_3^{2}$ 项）→ $\\lambda=0$ 是特征值且 $f$ 半正定？ 数据：$|E-A|=?$ 读 $a$。
【技巧】$A$ 特征值 $1,1,0$（正交变换下标准形系数）→ $|E-A|=0$ 展开解 $a$；(2) $|A+2E|=?$ 用特征值 $3,3,2$。
【易错】$\\lambda=1$ 二重 → $r(E-A)=1$ 定 $a$ 的行倍数关系；$|A+2E|=\\prod(\\lambda_i+2)=3\\cdot3\\cdot2=18$。
【注意】(1) $Q=\\begin{pmatrix}\\frac1{\\sqrt2}&0&\\frac1{\\sqrt2}\\\\0&1&0\\\\-\\frac1{\\sqrt2}&0&\\frac1{\\sqrt2}\\end{pmatrix}$ 型；(2) $|A+2E|=18$（按数据解析核对）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2022数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2022数二真题.md', TIPS_2022)
