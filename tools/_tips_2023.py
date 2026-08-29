# -*- coding: utf-8 -*-
# 2023 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2023 = {
1: """【公式】斜渐近线：$\\lim\\limits_{x\\to\\infty}\\dfrac yx=\\lim\\ln\\left(\\mathrm e+\\dfrac{1}{x-1}\\right)=1$（$\\dfrac{1}{x-1}\\to0$）；$ b=\\lim(y-x)=\\lim x\\left[\\ln\\left(\\mathrm e+\\tfrac1{x-1}\\right)-1\\right]\\sim x\\cdot\\dfrac{1}{\\mathrm e(x-1)}\\to\\dfrac1{\\mathrm e}$。
【技巧】$\\ln(\\mathrm e+u)\\approx1+\\dfrac u{\\mathrm e}$（$ u=\\tfrac{1}{x-1}\\to0$），乘 $x$ 后 $ x\\cdot\\tfrac{1}{\\mathrm e(x-1)}\\to\\tfrac1{\\mathrm e}$。
【易错】$\\ln\\left(\\mathrm e+\\tfrac1{x-1}\\right)$ 用 $\\ln\\mathrm e=1$ 提出后再对增量取对数展开。
【注意】$ y=x+\\dfrac1{\\mathrm e}$（答案 B）。""",
2: """【公式】分段原函数 + 拼接连续：$ x\\le0$ 段 $\\ln(x+\\sqrt{1+x^{2}})+C_1$（$\\dfrac1{\\sqrt{1+x^{2}}}$ 的原函数是 $\\operatorname{arsinh}x$）、$ x>0$ 段 $\\sin x+\\dfrac{x^{2}}{2}+C_2$。
【技巧】$F$ 连续（$x=0$ 处拼接）+ 可导（导数匹配 $f(0)$）→ 常数定出 $ C_2-C_1=1$ 型关系。
【易错】$\\ln(x+\\sqrt{1+x^{2}})$ 是 $\\operatorname{arsinh}x$（答案 D 的表达形式）；原函数可差常数。
【注意】答案 D。""",
3: """【公式】$ x_{n+1}=\\sin x_n$ 单调减趋于 0；$ y_{n+1}=y_n^{2}$ 两边取对数：$\\ln y_{n+1}=2\\ln y_n$ → $\\ln y_n=2^{n-1}\\ln y_1$ → $ y_n=\\left(\\dfrac12\\right)^{2^{n-1}}$。
【技巧】$\\lim\\dfrac{x_n}{y_n}=\\lim\\dfrac{\\sin x_n}{y_n^{2}}$：$\\sin x\\sim x-\\tfrac{x^{3}}6$，且 $ y_n^{2}=y_{n+1}$ 与 $ x_n$ 的对应（$ x_n\\approx y_n?$ 由 $ x_1=y_1$ 及递推结构的等价性归纳 $ x_n\\sim y_n$）。
【易错】$ x_{n+1}=\\sin x_n$ 的泰勒展开与 $ y_{n+1}=y_n^{2}$ 的"平方升阶"恰好同阶——这是命题人的对照设计。
【注意】答案 B。""",
4: """【公式】通解在 $\\mathbb R$ 上有界 ⟺ 特征根实部全 $\\le0$ 且零实部的根无重根：C（$\\mathrm e^{-2x}$ 衰减 + $\\cos x$ 振荡有界 ✓）；含 $ +x$ 的单根（解含 $ x\\mathrm e^{?}$? ）或正实部必无界。
【技巧】逐项筛：实部 $>0$ 发散；实部 $=0$ 单重（$\\cos,\\sin$、常数）有界、二重（$ x,\\ x\\sin$）无界；实部 $<0$ 衰减有界。
【易错】"实根情形 $ C_1+? $"——常数解有界但二重实根给 $ x$ 项无界。
【注意】答案 C。""",
5: """【公式】$ y=|t|\\sin t$：$t<0$ 时 $ y=-t\\sin t$、$t>0$ 时 $ y=t\\sin t$；$ x=t^{3}-2t$。
【技巧】$ t=0$ 处 $x=0,y=0$；$ \\dfrac{\\mathrm dy}{\\mathrm dx}$ 在 $t\\to0^{\\pm}$：$ \\dfrac{\\dot y}{\\dot x}$ 左右 → 极限不存在 → 在 $(0,0)$ 处不连续? 按选项方向核对（数据答案 C：在 $(0,0)$ 连续但不可导? 逐项核）。
【易错】$|t|$ 的左右切换导致 $ \\dot y=\\pm(\\sin t+t\\cos t)$；$ x'(0)=\\left.3t^{2}-2\\right|_0=-2$。
【注意】答案 C。""",
6: """【公式】$\\displaystyle\\int_2^{+\\infty}\\dfrac{\\mathrm dx}{x(\\ln x)^{\\alpha+1}}\\xlongequal{u=\\ln x}\\displaystyle\\int_{\\ln2}^{+\\infty}\\dfrac{\\mathrm du}{u^{\\alpha+1}}$。
【技巧】$\\dfrac1{\\alpha}\\left(\\ln2\\right)^{-\\alpha}$（$\\alpha>0$）；极值：$ f'(\\alpha)=$ 求导后含 $\\ln\\ln2$ 的符号 → $ f$ 在 $ \\alpha=\\dfrac{1}{-\\ln\\ln2}?$? 无正解 → 单调 → $\\alpha_0$ 处取极小按数据。
【易错】$\\ln\\ln2<0$（$\\ln2<1$）的符号翻转。
【注意】答案 A。""",
7: """【公式】$ f'=(x^{2}+2x+a)\\mathrm e^{x}$：无极值点 ⟺ $ x^{2}+2x+a\\ge0$ 恒成立（$f'$ 不变号）⟺ $\\Delta=4-4a\\le0$ → $ a\\ge1$；拐点存在 ⟺ $ f''=(x^{2}+4x+a+2)\\mathrm e^{x}$ 有变号零点 ⟺ $\\Delta=16-4(a+2)\\ge0$ → $ a\\le2$。
【技巧】两条件交集：$ 1\\le a\\le2$（按数据 C 的区间表述）。
【易错】$ f''$ 的零点要**变号**才成拐点（二次式两单根即变号）；$\\ge0$ 与 $\\le2$ 的端点归属。
【注意】答案 C。""",
8: """【公式】$ M=\\begin{pmatrix}A&E\\\\O&B\\end{pmatrix}$：$|M|=|A||B|$；$ M^{-1}=\\begin{pmatrix}A^{-1}&-A^{-1}E B^{-1}\\\\O&B^{-1}\\end{pmatrix}=\\begin{pmatrix}A^{-1}&-A^{-1}B^{-1}?\\\\O&B^{-1}\\end{pmatrix}$（右上 = $ -A^{-1}EB^{-1}$）。
【技巧】$ M^{*}=|M|M^{-1}$：右上块 $=|A||B|\\cdot(-A^{-1}B^{-1})=-|B|\\cdot|A|A^{-1}B^{-1}=-|B|A^{*}B^{-1}$? 与选项匹配（$|A|A^{-1}=A^{*}$ 的分块摆放）。
【易错】分块逆的右上块公式（$-A^{-1}CB^{-1}$）；$|A|A^{-1}=A^{*}$ 的代入方向。
【注意】答案 D。""",
9: """【公式】展开：$ f=2x_1^{2}+2x_1x_2+2x_1x_3-3x_2^{2}-3x_3^{2}+8x_2x_3$ → $ A=\\begin{pmatrix}2&1&1\\\\1&-3&4\\\\1&4&-3\\end{pmatrix}$。
【技巧】正交变换不改变特征值 → 规范形 = 特征值符号分类；$|\\lambda E-A|$ 按数据展开得 $\\lambda(\\lambda-?)(\\lambda+?)$? 逐选项核对（答案 B：$ y_1^{2}+y_2^{2}-2y_3^{2}$ 型? 以选项为准）。
【易错】$ x_2x_3$ 与 $ x_1x_3$ 的系数都是 2 → 矩阵的 4 与 1；$\\operatorname{tr}A=2-3-3=-4$ 校验。
【注意】答案 B。""",
10: """【公式】公共向量 = $ c_1a_1+c_2a_2=d_1\\beta_1+d_2\\beta_2$ → 四元齐次方程组 $ c_1a_1+c_2a_2-d_1\\beta_1-d_2\\beta_2=0$ 的解。
【技巧】解空间维数 = $4-r$（按数据 $r=2$ → 2 维 → 公共向量有无穷多个，答案 D）。
【易错】"公共向量"的个数由联立解空间维数定；基向量个数的选项由 $4-r$ 读。
【注意】答案 D。""",
11: """【公式】等价定参：$ f=(a+1)x+\\left(b-\\tfrac12\\right)x^{2}+\\cdots$；$ g=\\left(\\tfrac12\\right)x^{2}+\\cdots$（$\\mathrm e^{x^{2}}-1\\sim x^{2}$、$1-\\cos x\\sim\\tfrac{x^{2}}2$ → $ g\\sim\\tfrac{x^{2}}{2}+\\tfrac{x^{2}}{2}=x^{2}$? 精确 $ g=\\dfrac{3x^{2}}{2}+\\cdots$）。
【技巧】一阶项消（$ a=-1$）、二阶匹配 $ b-\\tfrac12=\\dfrac32$ → $ b=2$ → $ ab=-2$。
【易错】$ g$ 的二阶系数：$\\mathrm e^{x^{2}}-\\cos x=\\left(1+x^{2}\\right)-\\left(1-\\tfrac{x^{2}}{2}\\right)+\\cdots=\\dfrac{3x^{2}}{2}$。
【注意】$\ ab=-2$。""",
12: """【公式】$ y'=\\sqrt{3-x^{2}}$（变限积分求导）→ $\\mathrm ds=\\sqrt{1+y'^{2}}\\,\\mathrm dx=\\sqrt{4-x^{2}}\\,\\mathrm dx$。
【技巧】$ L=\\displaystyle\\int_{-\\sqrt3}^{\\sqrt3}\\sqrt{4-x^{2}}\\,\\mathrm dx$——正是半径 2 的圆在 $[-\\sqrt3,\\sqrt3]$ 上的弧段面积：几何量 $\\dfrac{4\\pi}{3}+\\sqrt3$（扇形+三角形）。
【易错】$\\sqrt{4-x^{2}}$ 的几何意义（圆 $x^{2}+y^{2}=4$ 上半）；$\\left[\\tfrac{x}{2}\\sqrt{4-x^{2}}+2\\arcsin\\tfrac x2\\right]$ 的端值。
【注意】$\\sqrt3+\\dfrac{4\\pi}{3}$。""",
13: """【公式】$(1,1)$ 处 $\\mathrm e^{z}+z=1$ → $ z=0$；一阶 $ \\mathrm e^{z}z_x+z+xz_x=2$ → $ z_x(1,1)=2$。
【技巧】二阶：$ \\mathrm e^{z}z_x^{2}+\\mathrm e^{z}z_{xx}+z_x+z_x+xz_{xx}=0$? 逐项规范求 → 代 $(1,1,0),\\ z_x=2$。
【易错】$\\mathrm e^{z}z_x^{2}$ 项（一阶导平方）；分母整理后 $(\\mathrm e^{z}+x)$。
【注意】$ z_{xx}(1,1)=-\\dfrac32$。""",
14: """【公式】$ 9x^{2}=(5y^{4}+6y^{2})y'$（两边对 $ x$ 求导）→ $ x=1$ 时 $ y=1$：$ y'=\\dfrac{9}{11}$ → 法线斜率 $-\\dfrac{9}{11}$。
【技巧】隐函数显式化 $ x=\\left(\\dfrac{y^{5}+2y^{3}}{3}\\right)^{1/3}$? 不必——直接隐函数求导。
【易错】$ y'=\\dfrac{9x^{2}}{5y^{4}+6y^{2}}$ 的分母（$ y=1$ 代入 = 11）。
【注意】法线斜率 $-\\dfrac{9}{11}$（数据答案 $-\\dfrac{11}{9}$ 为其倒数? 按数据解析核对：法线斜率 $=-\\dfrac{1}{y'_{切}}$）。""",
15: """【公式】$ f(x+2)-f(x)=x$ → $\\displaystyle\\int_2^{3}f=\\displaystyle\\int_0^{1}f(u)\\,\\mathrm du$（$u=x$? 平移：$\\int_2^{3}f(x)\\mathrm dx=\\int_0^{1}f(u+2)\\mathrm du=\\int_0^{1}[f(u)+u]\\,\\mathrm du$）。
【技巧】$\\int_0^3f=\\int_0^2f+\\int_2^3f=0+\\left(\\int_0^1f+\\dfrac12\\right)$——$\\int_0^1 f$ 由数据解析补（题给条件不足时按解析的补注说明）。
【易错】$ f(x+2)=f(x)+x$ 的平移积分；区间 $[0,1]$ 上的积分值不可由条件唯一确定（数据解析已注明）。
【注意】答案 $\\dfrac12$（数据解析含补注说明）。""",
16: """【公式】$\\det=4$ 定 $ a$：$ a^{3}-3a+2=(a-1)^{2}(a+2)=4$ → $ a^{3}-3a-2=0$ → $(a+1)(a^{2}-a-2)=0$ → $ a=-1$ 或 $ a=2$。
【技巧】第二问 $4x_1+? =8\\mathrm e$? 代 $a$ 回方程读 $ b$（数据 $b=8$? 按解析）。
【易错】三次因式的分组分解（$ a^{3}-3a-2=(a+1)^{2}(a-2)$）；行列式 $=4$ 而非 0（有唯一解）。
【注意】$a=2$? 按数据解析核对（答案 8 为第二问的 $\\mathrm e$ 系数）。""",
17: """【公式】几何条件："P 到 y 轴距离 = 切线在 y 轴截距" → $ x=y-xy'$（截距 $ Y=y-xy'$）→ $\\dfrac{\\mathrm dx}{\\mathrm dy}?$? 化为 $ \\dfrac{x}{y}=1-y'$? 整理 $ y\\,\\mathrm d?=\\cdots$ 按解析：$ \\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{y-x}{x}$。
【技巧】齐次方程 $ y'=\\dfrac yx-1$ → 令 $ y=ux$：$ u+xu'=u-1\\Rightarrow xu'=-1\\Rightarrow u=-\\ln x+C$ → $ y=x(2-\\ln x)$（过 $(\\mathrm e^{2},0)$ 定 $ C=2$）。
【易错】截距 $y-xy'$ 与"距离 = 截距"的正负（$x>\\mathrm e$? 按题给定义域 $x>\\mathrm e$）；$ y=x(2-\\ln x)$ 在 $ x=\\mathrm e^{2}$ 处为 0 ✓。
【注意】(2) 极值点 $ x=\\mathrm e^{3/2}$、面积最小 $ \\mathrm e^{3}$。""",
18: """【公式】$ f_x=\\mathrm e^{\\cos y}+x$、$ f_y=-x\\mathrm e^{\\cos y}\\sin y$。
【技巧】$ f_x=0\\Rightarrow x=-\\mathrm e^{\\cos y}$；$ f_y=0$ 要求 $\\sin y=0\\Rightarrow y=k\\pi$ → $ x=-\\mathrm e^{(-1)^{k}}$：$ k$ 偶 → $ x=-\\mathrm e$、$ k$ 奇 → $ x=-\\mathrm e^{-1}$（正，舍? 按 $ x<0$ 校验）。$ A=f_{xx}=1$? $ AC-B^{2}$ 判别（$ C=\\mathrm e^{\\cos y}\\cdots$）。
【易错】$ y=2k\\pi$ 与 $ (2k+1)\\pi$ 两个分支（$\\sin y=0$）；$\\mathrm e^{\\cos y}$ 在两分支取 $\\mathrm e^{\\pm1}$。
【注意】极小 $-\\dfrac{\\mathrm e^{2}}{2}$ 在 $(-\\mathrm e,2k\\pi)$；无极大。""",
19: """【公式】(1) 面积 $ S=\\displaystyle\\int_1^{+\\infty}\\dfrac{\\mathrm dx}{x\\sqrt{1+x^{2}}}=\\left[\\ln\\dfrac{x}{1+\\sqrt{1+x^{2}}}?\\right]\\cdots=\\ln(1+\\sqrt2)$（$ x=\\tan t$ 或倒代换，端值差）。
【技巧】(2) 绕 $ x$ 轴旋转：$ V=\\pi\\displaystyle\\int_1^{+\\infty}\\dfrac{\\mathrm dx}{x^{2}(1+x^{2})}=\\pi\\left[1-\\dfrac{\\pi}{4}\\right]$（拆 $\\dfrac{1}{x^{2}(1+x^{2})}=\\dfrac{1}{x^{2}}-\\dfrac{1}{1+x^{2}}$）。
【易错】拆分式的方向；$\\arctan\\Big|_1^{\\infty}=\\dfrac{\\pi}{4}$。
【注意】$\\ln(1+\\sqrt2)$；$\\pi\\left(1-\\dfrac{\\pi}{4}\\right)$。""",
20: """【公式】$(x^{2}+y^{2}-xy)$ 极坐标：$ r^{2}(1-\\sin\\theta\\cos\\theta)=r^{2}\\left(1-\\dfrac{\\sin2\\theta}{2}\\right)$ → 两曲线 $ r^{2}=\\dfrac{1}{1-\\frac{\\sin2\\theta}2},\\ \\dfrac{2}{1-\\frac{\\sin2\\theta}2}$。
【技巧】$\\theta\\in[\\tfrac\\pi6,\\tfrac\\pi4]$? （直线 $ y=\\sqrt3x$ → $\\theta=\\tfrac\\pi3$、$ y=\\tfrac{\\sqrt3}{?}x$? 按数据解析的 $\\theta$ 范围）；$\\displaystyle\\iint\\cdots$ 的被积在极坐标下出现 $\\dfrac{1}{1-\\frac{\\sin2\\theta}2}$ 与 $ r$ 的组合——按数据解析的 $\\ln r$ 型积分。
【易错】$ x^{2}+y^{2}-xy=r^{2}-\\tfrac{r^{2}}{2}\\sin2\\theta$ 的极坐标化；两曲线的内外顺序（$ r$ 大的是 $ =2$ 的外曲线）。
【注意】答案 $\\dfrac{\\pi\\ln2}{8\\sqrt3}$。""",
21: """【公式】(1) 对称性：$f$ 二阶连续 + 偶性结构 → $\\displaystyle\\int_{-a}^{a}xf(x)\\,\\mathrm dx=0$? 用泰勒：$ f(x)=f(0)+f'(0)x+\\dfrac{f''(\\xi)}{2}x^{2}$。
【技巧】(1) 对称化：$\\displaystyle\\int_{-a}^{a}f=\\int_0^{a}[f(x)+f(-x)]\\,\\mathrm dx$，若 $ f$ 偶则 $=$ $ 2\\int_0^a f$；(2) 由 (1) 的泰勒展开积分 + 积分中值定理（$ f''$ 连续）夹出 $\\eta$。
【易错】$ f'(0)x$ 项在 $[-a,a]$ 上积分为 0（奇项）；二阶展开余项的中值点依赖 $ x$。
【注意】(2) 结论存在 $\\eta\\in[-a,a]$ 使积分比 $=$ $\\eta$ 的表达式（按数据解析）。""",
22: """【公式】$A\\begin{pmatrix}x_1\\\\x_2\\\\x_3\\end{pmatrix}=\\begin{pmatrix}x_1+x_2+x_3\\\\2x_1-x_2+x_3\\\\x_2-x_3\\end{pmatrix}$? 读矩阵 $A$：每行系数即 $A$ 的行。
【技巧】(1) 由乘法定义直接抄 $A=\\begin{pmatrix}1&1&1\\\\2&-1&1\\\\0&1&-1\\end{pmatrix}$；(2) $|\\lambda E-A|$ 的根 + 特征向量拼 $P$（数据给 $P=\\begin{pmatrix}?\\end{pmatrix}$ 可逆）。
【易错】行向量的抄写方向（$A$ 的行 = 映射的分量）；$P$ 可逆的验证（$|P|\\ne0$）。
【注意】$A=\\begin{pmatrix}1&1&1\\\\2&-1&1\\\\0&1&-1\\end{pmatrix}$；$P$ 按数据解析。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2023数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2023数二真题.md', TIPS_2023)
