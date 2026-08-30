# -*- coding: utf-8 -*-
# 2026 卷点睛插入——收官卷（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
import re, sys
from pathlib import Path

def insert_tips(md_path, tips):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    heads = [(i, int(re.match(r'^### (\d+)', l).group(1)))
             for i, l in enumerate(lines) if re.match(r'^### (\d+)', l)]
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

TIPS_2026 = {
1: """【公式】$\\arcsin x=x+\\dfrac{x^{3}}{6}+o(x^{3})$、$x\\ln(1+x)=x^{2}-\\dfrac{x^{3}}{2}+o(x^{3})$。
【技巧】"与 $x\\ln(1+x)$ 等价" → $ax^{2}+(b+1)x+\\dfrac{x^{3}}{6}+o(x^{3})\\sim x^{2}-\\dfrac{x^{3}}{2}$——一阶、二阶系数逐层匹配：$b+1=0$、$a=1$。
【易错】$\\arcsin$ 展开只有奇次幂；一阶项必消（$b=-1$）。
【注意】$a=1,\\ b=-1$（答案 A）。""",
2: """【公式】$f'(0)=\\lim\\limits_{x\\to0^{+}}x^{\\alpha-1}\\sin\\dfrac1x$：存在 $\\Leftrightarrow\\alpha-1>0$（$\\sin$ 有界压住）；$\\lim\\limits_{x\\to0^{+}}f'(x)$ 存在 $\\Leftrightarrow\\alpha-1\\ge1$（$x^{\\alpha-1}\\to0$ 使振幅收敛）。
【技巧】"可导但导数不连续"的双层条件：$1<\\alpha\\le2$。
【易错】$\\alpha=2$ 时 $f'$ 振幅 $x\\cos\\tfrac1x\\to0$（极限存在）但彼侧仍振荡——存在不等价于连续。
【注意】答案 C。""",
3: """【公式】$\\displaystyle\\int_0^1(1-x)f(x)\\,\\mathrm dx\\ge0$（$1-x\\ge0$、$f\\ge0$）→ $\\int f>\\int xf$；$x\\ge x^{2}$（$[0,1]$）→ $\\int xf>\\int x^{2}f$。
【技巧】层层嵌套的积分序比较：$\\int f>\\int xf>\\int x^{2}f$。
【易错】严格不等号来自 $f$ 非负连续不恒为零。
【注意】答案 B。""",
4: """【公式】分段混合偏导经典反例：$f_x(0,y)=\\lim\\limits_{x\\to0}\\dfrac{f(x,y)-f(0,y)}{x}$ 沿轴代分段表达式 → $f_x(0,y)=-y$、$f_y(x,0)=x$。
【技巧】$f_{xy}''(0,0)=\\lim\\limits_{y\\to0}\\dfrac{f_x(0,y)-f_x(0,0)}{y}=-1$；$f_{yx}''(0,0)=+1$——两个混合偏导**不相等**。
【易错】混合偏导交换次序需二阶偏导连续——本题正是反例。
【注意】答案 B。""",
5: """【公式】$I<\\dfrac{\\pi}{2}$：半圆面积 $=\\dfrac{\\pi}{2}$，被积 $<1$ 时积分 $<$ 面积。
【技巧】被积式的上界放缩 → 夹逼选答案。
【易错】$x\\ge0$ 的半圆域面积是 $\\dfrac{\\pi}{2}$。
【注意】答案 A。""",
6: """【公式】解唯一性 $\\ne$ 解恒为初值：反例 $y'=\\cos x$，$y(x_0)=y_0$ 唯一解 $y=\\sin(x-x_0)+y_0$——$y\\equiv y_0$ 不满足方程。
【技巧】"$y\\equiv y_0$ 是唯一解"需 $q\\equiv p\\,y_0$ 对所有 $x$ 成立（不只是 $x_0$ 处）。
【易错】D 的反例已足。
【注意】答案 D。""",
7: """【公式】分块对角：$\\begin{vmatrix}2A^{*}&O\\\\O&B^{-1}\\end{vmatrix}=|2A^{*}|\\cdot|B^{-1}|=8|A^{*}|\\cdot\\dfrac{1}{|B|}$。
【技巧】$|A^{*}|=|A|^{2}=4$（3 阶）→ $8\\times4\\times\\left(-\\tfrac13\\right)=-\\dfrac{32}{3}$。
【易错】$|2A^{*}|=2^{3}|A^{*}|$ 的立方；$|B^{-1}|=\\tfrac1{|B|}$。
【注意】答案 A。""",
8: """【公式】题面数据矛盾：由 $A\\alpha_1=0$ 解出参数，与该组参数下的 $\\alpha_2$ 条件冲突。
【技巧】遇到"题面数据矛盾"题：如实推导并指出矛盾，不硬凑选项。
【注意】按数据解析（题面数据矛盾，无正确选项）。""",
9: """【公式】$A^{2}=A$ → $\\lambda^{2}=\\lambda$ → $\\lambda\\in\\{0,1\\}$；$A$ 实对称 → 正交可对角化 → 幂等对称阵 = 正交投影矩阵，$r(A)=\\operatorname{tr}A$。
【技巧】幂等阵特征值只能 $0,1$；实对称保证可对角化。
【易错】$A^{2}=A$ 的一般矩阵也可对角化（最小多项式无重根）。
【注意】答案 D。""",
10: """【公式】移项：按数据解析展开为 $(A-B)(B-A)=-(A-B)^{2}$ 型。
【技巧】矩阵差的平方：$(A-B)^{2}=A^{2}-AB-BA+B^{2}$；$(A-B)^{2}=(B-A)^{2}$（负号平方）。
【易错】矩阵乘法不交换，但平方差展开的对称结构仍成立。
【注意】答案 D。""",
11: """【公式】$\\dfrac{\\arctan x}{x^{p}(x+1)}$：$x\\to0^{+}$ 端 $\\arctan x\\sim x$ → $\\sim\\dfrac{1}{x^{p-1}}$（$p<2$ 收敛）；$x\\to+\\infty$ 端 $\\arctan x\\to\\tfrac{\\pi}{2}$、$x+1\\sim x$ → $\\sim\\dfrac{1}{2x^{p+1}}$（$p>0$ 收敛）。
【技巧】双端分别判 + 取交集：$0<p<2$。
【易错】$\\arctan$ 在两端的渐近行为不同。
【注意】$0<p<2$。""",
12: """【公式】通分：$\\dfrac{\\sin x-\\ln(1+x)}{x\\sin x}$；分子 $\\sin x-\\ln(1+x)\\sim\\dfrac{x^{2}}{2}$（$\\ln$ 的二阶项 $-\\tfrac{x^{2}}2$ 无抵消）。
【技巧】展开比对：$\\sin x=x-\\tfrac{x^{3}}6+\\cdots$、$\\ln(1+x)=x-\\tfrac{x^{2}}2+\\tfrac{x^{3}}3+\\cdots$ → 分子 $\\tfrac{x^{2}}2+\\cdots$、分母 $x^{2}$ → 极限 $\\dfrac12$。
【易错】分子首项是二阶（$x$ 项被消）；$\\ln$ 的三阶 $\\tfrac{x^{3}}3$ 与 $\\sin$ 的三阶 $-\\tfrac{x^{3}}6$ 合成 $+\\tfrac{x^{3}}6$ 不影响二阶主项。
【注意】答案 $\\dfrac12$。""",
13: """【公式】隐函数曲率：$y'=-\\dfrac{2x+2\\sqrt{3}y}{2\\sqrt{3}x+2y}$，代 $(0,1)$：$y'(0)=-\\sqrt3$。
【技巧】二阶继续隐式求导后代入 $K=\\dfrac{|y''|}{(1+3)^{3/2}}$；曲率半径 $=\\dfrac1K$。
【易错】分母链式含 $y'$ 的项。
【注意】半径 4。""",
14: """【公式】链式：$g'=f_1'\\cdot\\dfrac1x+f_2'\\cdot\\pi\\cos\\pi x$，代 $x=1$：中间变量 $=\\left(\\ln1,\\sin\\pi\\right)=(0,0)$。
【技巧】$f_x(0,0)=\\pi,\\ f_y(0,0)=3$ → $g'(1)=\\pi\\cdot1+3\\cdot\\pi\\cdot(-1)=-2\\pi$。
【易错】$\\pi\\cos\\pi=-\\pi$。
【注意】$g'(1)=-2\\pi$。""",
15: """【公式】平均值 $=\\dfrac12\\displaystyle\\int_0^{2}\\ln(2+x)\\,\\mathrm dx=\\dfrac12\\left[(2+x)\\ln(2+x)-(2+x)\\right]_0^{2}$。
【技巧】代值 + $\\ln4=2\\ln2$ 化简 → $3\\ln2-1$。
【易错】系数 $\\dfrac12$；$\\ln4$ 的化简。
【注意】$3\\ln2-1$。""",
16: """【公式】规范形仅一项 → $r(AA^{\\mathrm T})=r(A)=1$（正惯性 1、负惯性 0）。
【技巧】$r(AA^{\\mathrm T})=r(A)$（$A^{\\mathrm T}Ax=0\\iff Ax=0$ 内积引理）→ $r(A)=1$ → 两行成比例。
【易错】$r(A)=1$ 的翻译（行成比例）。
【注意】$r=1$。""",
17: """【公式】极坐标：$\\theta\\in[\\tfrac\\pi4,\\tfrac{3\\pi}4]$（$|x|\\le y$）、$r\\in[0,\\sqrt2]$（圆边界 $x^{2}+y^{2}\\le2$，$r$ 上限与 $\\theta$ 无关）。
【技巧】$\\displaystyle\\iint y\\sin\\sqrt{x^{2}+y^{2}}=\\int_{\\pi/4}^{3\\pi/4}\\sin\\theta\\,\\mathrm d\\theta\\int_0^{\\sqrt2}r^{2}\\sin r\\,\\mathrm dr$——$\\theta$ 与 $r$ 完全分离；$\\int_{\\pi/4}^{3\\pi/4}\\sin\\theta=\\sqrt2$、$\\int_0^{\\sqrt2}r^{2}\\sin r\\,\\mathrm dr=2\\sqrt2\\sin\\sqrt2-2$（两次分部）。
【易错】$\\sin\\theta\\ge0$ 在区间内；$r^{2}\\sin r$ 两次分部的系数。
【注意】$I=4\\sin\\sqrt2-2\\sqrt2$。""",
18: """【公式】换元 $u=xt$：$f(x)=\\dfrac1x\\displaystyle\\int_0^{x^{3}}g(u)\\,\\mathrm du$（$x\\ne0$）→ $f'=3\\,g(x^{3})-\\dfrac{1}{x^{2}}\\displaystyle\\int_0^{x^{3}}g$。
【技巧】$f(x)=\\dfrac{G(x^{3})}{x}$（$G'=g$）→ $f'=\\dfrac{3x^{2}g(x^{3})\\cdot x-G(x^{3})}{x^{2}}$；$x\\to0$ 分支 $f(0)=\\lim\\dfrac{G(x^{3})}{x}=\\lim g(0)x^{2}=0$。
【易错】换元上下限 $u\\in[0,x^{3}]$；$\\dfrac1x$ 提因子与 $x\\to0$ 的连续补充。
【注意】$f'$ 在 $x=0$ 连续（中值定理夹逼 $\\to f'(0)$，按数据解析）。""",
19: """【公式】$f_x=\\mathrm e^{x}(2x^{2}+4x-y^{2})$、$f_y=-2y\\mathrm e^{x}$ → 驻点 $y=0$ 且 $x=0$ 或 $x=-2$。
【技巧】$A=f_{xx}=\\mathrm e^{x}(2x^{2}+8x+4-y^{2})$、$C=f_{yy}=-2\\mathrm e^{x}$、$B=f_{xy}=-2y\\mathrm e^{x}$：$(0,0)$ 处 $AC-B^{2}=-8<0$ 非极值；$(-2,0)$ 处 $AC-B^{2}=8\\mathrm e^{-4}>0$ 且 $A=-4\\mathrm e^{-2}<0$ → 极大。
【易错】$(0,0)$ 是鞍点不是极值；极大值 $\\dfrac{8}{\\mathrm e^{2}}$。
【注意】仅极大 $f(-2,0)=\\dfrac{8}{\\mathrm e^{2}}$，无极小。""",
20: """【公式】$y''=\\dfrac{6x^{2}-2}{(1+x^{2})^{3}}=0\\Rightarrow x=\\dfrac{1}{\\sqrt3}$；切线斜率 $y'\\left(\\tfrac1{\\sqrt3}\\right)=-\\dfrac{3\\sqrt3}{8}$。
【技巧】法线斜率 $=\\dfrac{8}{3\\sqrt3}$；旋转体 $V=\\pi\\displaystyle\\int_{1/\\sqrt3}^{+\\infty}\\dfrac{\\mathrm dx}{(1+x^{2})^{2}}$，用 $\\int\\dfrac{\\mathrm dx}{(1+x^{2})^{2}}=\\dfrac{x}{2(1+x^{2})}+\\tfrac12\\arctan x$。
【易错】拐点横坐标 $\\tfrac1{\\sqrt3}$；体积积分端值（$\\tfrac{\\pi}{2}$ 端）。
【注意】$V=\\dfrac{\\pi^{2}}{6}-\\dfrac{\\sqrt3}{16}\\pi$。""",
21: """【公式】缺 $y$ 且含 $(y')^{2}$：$p=y'$，$x^{2}p'-2xp-p^{2}=0$ → $p'-\\dfrac2x p=\\dfrac{p^{2}}{x^{2}}$（伯努利 $n=2$）。
【技巧】令 $z=\\dfrac1p$：可分离/线性解出 $p=\\dfrac{x^{2}}{2-x}=-x-2-\\dfrac{4}{x-2}$；积分 + $y(3)=\\tfrac12$ 定 $C_1=11$。
【易错】伯努利 $n=2$ 的倒数变换；$p$ 的有理函数拆分后积分出 $-4\\ln(x-2)$。
【注意】$y=-\\dfrac{x^{2}}{2}-2x-4\\ln(x-2)+11$。""",
22: """【公式】$A$ 行化简读 $r$ 与解空间；按数据解析的 $\\boldsymbol{\\alpha}_i$ 结构 + $D$ 的幂。
【技巧】(1) $\\boldsymbol{\\alpha}_i$ 属 $Ax=0$ 的解 → 从给定乘积条件反解；(2) $D^9=\\begin{pmatrix}1&-9\\\\0&1\\end{pmatrix}$ 型 → $A^{10}$ 由相似结构读出。
【易错】$n-r$ 的解空间维数；$D$ 幂的斜对角系数。
【注意】$A^{10}=\\begin{pmatrix}1&-8&-9&9\\\\0&-1&-1&1\\\\-1&9&10&-10\\\\-1&7&8&-8\\end{pmatrix}$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2026数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2026数二真题.md', TIPS_2026)