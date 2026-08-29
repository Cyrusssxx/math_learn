# -*- coding: utf-8 -*-
# 2013 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2013 = {
1: """【公式】$\\cos x-1\\sim-\\dfrac{x^{2}}{2}$ → $x\\sin\\alpha(x)\\sim x^{2}$ → $\\sin\\alpha(x)\\sim x$ → $\\alpha(x)\\to0$。
【技巧】等价链逐环传递；$\\alpha(x)$ 是"被 $\\sin$ 压住的角"，$\\sin\\alpha\\to0$ 时 $\\alpha\\to0$（$|\\alpha|<\\tfrac\\pi2$ 内单射）。
【易错】同阶无穷小的区分（C 说"同阶但不等价"——$\\alpha(x)\\sim x$ 确实等价，别被选项绕晕）。
【注意】答案 C（等价无穷小）。""",
2: """【公式】导数定义伪装：$n\\left[f\\left(\\dfrac2n\\right)-f(0)\\right]=2\\cdot\\dfrac{f(2/n)-f(0)}{2/n}\\to2f'(0)$。
【技巧】隐函数 $\\cos(xy)+\\ln y-x=1$ 代 $(0,1)$ ✓；求导 $-y\\sin(xy)+\\dfrac{y'}{y}-1=0$ → $y'(0)=1$。
【易错】系数 2（$\\tfrac2n$）；分母是 $y$ 不是 $x$。
【注意】$2f'(0)=2$（答案 A）。""",
3: """【公式】$F(x)=\\displaystyle\\int_1^x f(t)\\,\\mathrm dt$：分段积（$\\sin$ 段与常数 2 段）。
【技巧】$F(2\\pi)=F(\\pi)+\\displaystyle\\int_\\pi^{2\\pi}2\\,\\mathrm dt=2+2\\pi$；$F(\\pi)=\\displaystyle\\int_0^{\\pi}\\sin=2$。
【易错】$F$ 在 $[\\pi,2\\pi]$ 段的斜率为 2（$f=2$）；$F(3\\pi)=2+2\\pi+\\displaystyle\\int_{2\\pi}^{3\\pi}\\sin t\\,\\mathrm dt$（第三段又积 $\\sin$）。
【注意】答案 C。""",
4: """【公式】比较判别法（对数压不过幂）：$x=1$ 处 $\\dfrac{1}{(x-1)^{\\alpha-1}}$ 与 $\\dfrac{1}{x\\ln^{\\alpha}x}$ 在 $x\\to1$ 时 $\\ln^{\\alpha}x\\sim(x-1)^{\\alpha}$ → 两段同阶拼接。
【技巧】统一判据：$\\alpha-1<1\\iff\\alpha<2$ 时收敛、$\\alpha\\ge2$ 时发散。
【易错】$x\\to\\mathrm e^{+}$ 无穷远端：$\\dfrac{1}{x\\ln^{\\alpha}x}$ 对任意 $\\alpha>1$ 收敛（对数积分判别）。
【注意】答案 D（$\\alpha$ 分界是 2）。""",
5: """【公式】链式：$z_x=-\\dfrac{y}{x^{2}}f(xy)+\\dfrac{y^{2}}{x}f'$、$z_y=\\dfrac1x f(xy)+y f'$。
【技巧】目标式 $\\dfrac xy z_x-\\dfrac1y z_y$? 代入后按 $f$ 与 $f'$ 归并——$f(xy)$ 项系数：$-\\dfrac{y}{x^{2}}\\cdot\\dfrac xy-\\dfrac{y}{x}\\cdot\\dfrac1x$ 合并。
【易错】$f(xy)$ 与 $f'(xy)$ 是两个独立"未知数"分别归并；商的链式符号。
【注意】答案 A。""",
6: """【公式】象限替换对称：$I_k=\\displaystyle\\iint_{D_k}(y-x)\\,\\mathrm dx\\,\\mathrm dy$；$D_2$ 与 $D_4$ 关于 $y=x$ 对称。
【技巧】$D_2\\leftrightarrow D_4$ 互换时 $y-x$ 变号 → $I_2=-I_4$，$I_1=I_3$（各自对称）；$|I_3|$ 最大（第一象限 $y-x$ 与 $r$ 无关、$\\mathrm e^{r^{2}}$? 被积含 $\\mathrm e$ 权重）。
【易错】$D_1,D_3$ 的被积不含 $\\mathrm e$——四个积分的被积函数是 $(y-x)\\mathrm e^{(x+y)^{2}}$? 按题面代入核。
【注意】答案 B。""",
7: """【公式】$C=AB$：$C$ 的列 $\\subset$ $A$ 的列空间 → $r(C)\\le r(A)$；$B$ 可逆 → $A=CB^{-1}$ → $r(A)\\le r(C)$。
【技巧】双向夹出 $r(A)=r(C)$；"表示性"叙述 = 秩相等 + 列空间相同。
【易错】"等价"选项（列向量组等价 $\\Leftrightarrow$ 列空间相同）——本题 $B$ 可逆恰好保证列空间相同 → 列向量组等价。
【注意】答案 B。""",
8: """【公式】实对称必可对角化；$A\\sim\\Lambda$（$\\Lambda$ 对角）→ 同特征值：$\\operatorname{tr}A=b+2$、$\\det A=?$ 与 $\\Lambda=\\mathrm{diag}(2,b,0)$? 按选项核对特征值集合。
【技巧】$a$ 由重根条件定：$A$ 的特征多项式有二重根 $2$ → $r(2E-A)=1$? 逐选项验证秩条件。
【易错】实对称"必可对角化"是钥匙（排除不可对角化分支）；$a$ 与 $b$ 联立。
【注意】答案 B。""",
9: """【公式】$1^{\\infty}$ 型：$\\left(2-\\dfrac{\\ln(1+x)}{x}\\right)^{1/x}=\\mathrm e^{\\frac1x\\ln\\left(1+\\left[1-\\frac{\\ln(1+x)}{x}\\right]\\right)}$，内层 $1-\\dfrac{\\ln(1+x)}{x}\\sim\\dfrac{x}{2}$。
【技巧】指数 $\\dfrac1x\\cdot\\dfrac x2=\\dfrac12$ → $\\mathrm e^{1/2}$。
【易错】$\\ln(1+x)=x-\\dfrac{x^{2}}{2}+\\cdots$ 的二阶项是主项来源。
【注意】答案 $\\mathrm e^{1/2}$。""",
10: """【公式】反函数导数：$\\dfrac{\\mathrm dx}{\\mathrm dy}=\\dfrac{1}{f'(x)}=\\dfrac{1}{\\sqrt{1-\\mathrm e^{x}}}$。
【技巧】$x=-1$ → $f'(-1)=\\sqrt{1-\\mathrm e^{-1}}$ → $\\left(f^{-1}\\right)'(f(-1))=\\dfrac{1}{\\sqrt{1-\\mathrm e^{-1}}}$。
【易错】反函数求导公式的自变量对应（$y_0=f(-1)$ 处）；$\\mathrm e^{x}\\le1$（$x\\le0$）。
【注意】答案 $\\dfrac{1}{\\sqrt{1-\\mathrm e^{-1}}}$。""",
11: """【公式】极坐标扇形面积：$S=\\dfrac12\\displaystyle\\int r^{2}\\,\\mathrm d\\theta=\\dfrac12\\int_{-\\pi/6}^{\\pi/6}\\cos^{2}3\\theta\\,\\mathrm d\\theta$。
【技巧】$\\cos^{2}3\\theta=\\dfrac{1+\\cos6\\theta}{2}$，对称区间减半工作量。
【易错】$\\cos6\\theta$ 在 $\\left[-\\tfrac\\pi6,\\tfrac\\pi6\\right]$ 上恰好积出一个整周期 → 贡献 0。
【注意】$S=\\dfrac12\\cdot\\dfrac12\\cdot\\dfrac{\\pi}{3}=\\dfrac{\\pi}{12}$。""",
12: """【公式】参数求导：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{t/(1+t^{2})}{1/(1+t^{2})}=t$，$t=1$ → 斜率 1。
【技巧】$y=\\ln\\sqrt{1+t^{2}}=\\tfrac12\\ln(1+t^{2})$ 先化简再求导；法线斜率 $-1$。
【易错】切点 $\\left(\\dfrac{\\pi}{4},\\ln\\sqrt2\\right)$（$\\arctan1=\\tfrac{\\pi}{4}$）。
【注意】法线 $y+x-\\dfrac{\\pi}{4}-\\ln\\sqrt2=0$。""",
13: """【公式】解的结构：$y_1-y_3=\\mathrm e^{3x}$、$y_2-y_3=\\mathrm e^{x}$ 是齐次解 → 特征根 1、3；$y_3=-x\\mathrm e^{2x}$ 是非齐特解 → 右端共振 $\\sim x\\mathrm e^{2x}$（$\\lambda=2$ 单特征根）。
【技巧】通解 = $y_3+$ 齐次通解 = $-x\\mathrm e^{2x}+C_1\\mathrm e^{3x}+C_2\\mathrm e^{x}$。
【易错】"三个解"的差分技巧（两两相减得齐次解）；特征根由差分结果反推。
【注意】通解 $-x\\mathrm e^{2x}+C_1\\mathrm e^{3x}+C_2\\mathrm e^{x}$。""",
14: """【公式】$a_{ij}+A_{ij}=0$ → $A^{\\mathrm T}=-A^{*}$；两边右乘/左乘 $A$：$AA^{\\mathrm T}=-AA^{*}=-|A|E$。
【技巧】取行列式：$|A^{\\mathrm T}|=(-|A|)^{3}|E|$ → $|A|=-|A|^{3}$ → $|A|=\\pm1$；再由 $AA^{\\mathrm T}=-|A|E\\succeq0$（半正定）筛 $|A|<0$ → $|A|=-1$。
【易错】$AA^{\\mathrm T}$ 半正定 → $-|A|\\ge0$ → $|A|\\le0$，结合 $|A|=\\pm1$ 定 $-1$；非零矩阵排除 $|A|=0$ 分支。
【注意】答案 $-1$。""",
15: """【公式】裂项：$1-\\cos x\\cos2x\\cos3x=(1-\\cos x)+\\cos x(1-\\cos2x)+\\cos x\\cos2x(1-\\cos3x)$。
【技巧】每个括号是 $1-\\cos\\bullet\\sim\\dfrac{\\bullet^{2}}{2}$，逐段：$\\dfrac{x^{2}}{2}+\\cos x\\cdot\\dfrac{4x^{2}}{2}+\\cos x\\cos2x\\cdot\\dfrac{9x^{2}}{2}$ → 系数和 $\\dfrac{1+4+9}{2}=7$。
【易错】三个 $\\cos$ 因子在取极限时 $\\to1$（不影响系数）；拆项的"递推式"写法（每段多乘一个 cos）。
【注意】$n=2,\\ a=7$。""",
16: """【公式】$V_x=\\pi\\displaystyle\\int_0^{a}x^{2/3}\\,\\mathrm dx=\\dfrac{3\\pi}{5}a^{5/3}$；$V_y=\\dfrac{\\pi}{?}a^{?}$? ——绕 $y$ 轴用柱壳：$V_y=2\\pi\\displaystyle\\int_0^{a}x\\cdot x^{1/3}\\,\\mathrm dx=\\dfrac{6\\pi}{7}a^{7/3}$。
【技巧】$V_x=V_y$ → $\\dfrac{3a^{5/3}}{5}=\\dfrac{6a^{7/3}}{7}$ → $a^{2/3}=\\dfrac{7}{10}\\cdot\\dfrac{7}{?}$ 代数解 $a=7\\sqrt7$。
【易错】柱壳法（外壳体积 $2\\pi x\\cdot$ 高 $\\cdot\\mathrm dx$）绕 $y$ 轴免去反解；$\\sqrt[3]{x}$ 与 $x$ 的指数运算。
【注意】$a=7^{3/2}=7\\sqrt7$。""",
17: """【公式】三直线围成三角形（顶点 $(0,0),(6,2),(2,6)$）；$\\displaystyle\\iint x^{2}\\,\\mathrm d\\sigma$ 按 $x$ 分三段或用对称。
【技巧】$D$ 关于 $y=x$ 对称 + 被积 $x^{2}$：$\\displaystyle\\iint x^{2}=\\dfrac12\\iint(x^{2}+y^{2})\\cdots$ 或按数据解析的 $y$ 型分块（$y\\in[0,2]$ 段 $x\\in[\\tfrac y3,3y]$、$y\\in[2,6]$ 段 $x\\in[\\tfrac y3,8-y]$）。
【易错】上下边界分段（$y=3x$ 与 $x+y=8$ 的切换点 $(2,6)$）；内层积分的上下限方向。
【注意】答案 $\\dfrac{416}{3}$。""",
18: """【公式】(I) 奇函数 → $f(0)=0$；$F(x)=f(x)-x$：$F(0)=0$、$F(1)=0$ → 罗尔给 $\\xi\\in(0,1)$ 使 $f'(\\xi)=1$。
【技巧】(II) $\\eta$ 的存在性用 $F'$ 的两零点再罗尔：$F'(0)=f'(0)-1$? 由 $f$ 奇 → $f'$ 偶 → $f'(0)$? 结论 $f'(\\eta)=1$ 与 $f''(\\eta)=0$ 的两级罗尔链。
【易错】$f(0)=0$（奇函数在原点连续必有）；$F$ 的两个端点零点（$x=0,1$）与内零点（$\\xi$）配合两次罗尔。
【注意】(II) 存在 $\\eta\\in(-1,1)$ 使 $f''(\\eta)=0$（按解析：$\\xi\\in(0,1)$ 与 $-\\xi\\in(-1,0)$ 关于原点对称夹出）。""",
19: """【公式】隐函数约束最值：$g=x^{3}-xy+y^{3}-1=0$（$x,y\\ge0$），$d=x^{2}+y^{2}$。
【技巧】拉格朗日：$2x=\\lambda(3x^{2}-y)$、$2y=\\lambda(3y^{2}-x)$；代入约束解得 $d_{\\min}=1$（点 $(1,0)$）与 $d_{\\max}=\\sqrt2$（点 $\\left(\\dfrac{\\sqrt[3]{2}}{}?\\right)$ 按解析）。
【易错】边界情形（$x=0$ 或 $y=0$）单独验证——$y=0$：$x^{3}=1$ → $(1,0)$ 距离 1；拉格朗日内点解出另一点。
【注意】最长 $\\sqrt2$、最短 $1$（按数据解析）。""",
20: """【公式】(I) $f'=\\dfrac1x-\\dfrac1{x^{2}}=\\dfrac{x-1}{x^{2}}$ → $x=1$ 唯一极小点，$f(1)=1$。
【技巧】(II) $\\ln x_n+\\dfrac{1}{x_{n+1}}<1$ 与 $\\ln x_n+\\dfrac{1}{x_n}\\ge1$（(I) 结论 $f\\ge1$）联立 → $\\dfrac{1}{x_{n+1}}<\\dfrac{1}{x_n}$ → $x_{n+1}>x_n$ 递增有上界 1。
【易错】"单调递增有上界 → 收敛"；极限方程传递：$\\lim\\left(\\ln x_n+\\dfrac{1}{x_{n+1}}\\right)=1$ 与 $\\ln\\lim x_n\\ge1$ 夹出 $\\lim x_n=1$。
【注意】$\\lim x_n=1$。""",
21: """【公式】(I) 弧长 $s=\\displaystyle\\int_1^{\\mathrm e}\\sqrt{1+\\left(\\dfrac{x}{2}-\\dfrac{1}{2x}\\right)^{2}}\\,\\mathrm dx=\\dfrac12\\int_1^{\\mathrm e}\\left(x+\\dfrac1x\\right)\\mathrm dx$（完全平方式 $\\left(\\tfrac{x}{2}-\\tfrac{1}{2x}\\right)^{2}+1=\\left(\\tfrac{x}{2}+\\tfrac{1}{2x}\\right)^{2}$）。
【技巧】(II) $D$ 面积 $=\\displaystyle\\int_1^{\\mathrm e}\\left(\\dfrac{x^{2}}{4}-\\dfrac12\\ln x\\right)\\mathrm dx$；形心 $\\bar x=\\dfrac{\\iint x}{\\text{面积}}$（$\\iint x\\,\\mathrm d\\sigma=\\displaystyle\\int x\\cdot y\\,\\mathrm dx$ 柱壳）。
【易错】完全平方式的识别是本题命门；形心公式 $\\bar x=\\dfrac{\\int xy\\,\\mathrm dx}{\\int y\\,\\mathrm dx}$。
【注意】$s=\\dfrac{\\mathrm e^{2}+1}{4}$；$\\bar x=\\dfrac{3(\\mathrm e^{4}-2\\mathrm e^{2}-3)}{4(\\mathrm e^{3}-7)}$。""",
22: """【公式】迹条件：$\\operatorname{tr}(AC-CA)=0\\Rightarrow b=\\operatorname{tr}(B)=0$（一秒排除一个参数）。
【技巧】设 $C=\\begin{pmatrix}x_1&x_2\\\\x_3&x_4\\end{pmatrix}$ 展开比较对应元素得 4 方程：$ax_3-x_2=0$、$x_2+ax_4-ax_1=1$、$x_1-x_3-x_4=1$、$x_2-ax_3=b$——第 3 式解出 $x_1$ 代入第 2 式得 $-a=1$。
【易错】展开 $AC-CA$ 时 $A$ 的元素位置（$a$ 在右上、1 在左下）别错；先取迹再解方程能省一半讨论。
【注意】$a=-1,\\ b=0$；通解 $C=\\begin{pmatrix}k_1+k_2+1&-k_1\\\\k_1&k_2\\end{pmatrix}$。""",
23: """【公式】$f=2(\\alpha^{\\mathrm T}x)^{2}+(\\beta^{\\mathrm T}x)^{2}=2x^{\\mathrm T}\\alpha\\alpha^{\\mathrm T}x+x^{\\mathrm T}\\beta\\beta^{\\mathrm T}x$ → 矩阵 $2\\alpha\\alpha^{\\mathrm T}+\\beta\\beta^{\\mathrm T}$。
【技巧】(I) 二次型转矩阵的标准动作（标量平方 = 行列外积）；(II) $\\alpha\\perp\\beta$ 且均单位 → $r(2\\alpha\\alpha^{\\mathrm T}+\\beta\\beta^{\\mathrm T})=2$ → 特征值 $2,1,0$，正交变换下标准形 $2y_1^{2}+y_2^{2}$。
【易错】$\\alpha\\alpha^{\\mathrm T}$ 的特征值 $|\\alpha|^{2},0,0$（秩 1）；$2\\alpha\\alpha^{\\mathrm T}+\\beta\\beta^{\\mathrm T}$ 的特征值 = 2、1、0（正交基下对角化，因为 $\\alpha\\perp\\beta$）。
【注意】(I) 矩阵 $2\\alpha\\alpha^{\\mathrm T}+\\beta\\beta^{\\mathrm T}$；(II) 标准形 $2y_1^{2}+y_2^{2}$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2013数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2013数二真题.md', TIPS_2013)
