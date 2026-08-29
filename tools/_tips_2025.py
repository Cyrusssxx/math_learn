# -*- coding: utf-8 -*-
# 2025 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2025 = {
1: """【公式】隐函数偏导：$\\left(1+\\dfrac1z\\right)z_x-\\mathrm e^{-x^{2}}=0$ → $ z_x=\\dfrac{z\\,\\mathrm e^{-x^{2}}}{1+z}$。
【技巧】对 $y$ 同理：$ z_y=-\\dfrac{z\\,\\mathrm e^{-y^{2}}}{1+z}$ → 组合 $\\dfrac{\\partial z}{\\partial x}-\\dfrac{\\partial z}{\\partial y}\\cdot$? 按选项系数配平。
【易错】$\\displaystyle\\int_y^x\\mathrm e^{-t^{2}}\\,\\mathrm dt$ 上下限都要求导（$\\mathrm e^{-x^{2}}$ 与 $-\\mathrm e^{-y^{2}}$）。
【注意】答案 A。""",
2: """【公式】$ f'=\\mathrm e^{x^{2}}\\sin x$：$ f'(0)=0$、$ f''(0)=\\mathrm e^{0}\\cos0=1\\ne0$ → $f$ 在 0 取极小。
【技巧】$ g(x)=\\left(\\displaystyle\\int_0^x\\mathrm e^{t^{2}}\\,\\mathrm dt\\right)^{2}$：$ g'=2\\mathrm e^{x^{2}}\\cdot\\displaystyle\\int_0^x\\mathrm e^{t^{2}}\\mathrm dt\\sim2x\\cdot x^{3}$? $\\int_0^x\\mathrm e^{t^{2}}\\sim x$ → $ g\\sim x^{2}$，$ g(0)=g'(0)=0$、$ g''(0)=2$。
【易错】$\\dfrac{f}{g}$ 型比较或 $\\lim\\dfrac{f}{g}=\\dfrac{\\sin x\\text{ 主项}}{}$? 按数据选项 B 的结构核。
【注意】答案 B。""",
3: """【公式】任意解的 $\\displaystyle\\int_0^{+\\infty}$ 收敛 ⟺ 特征根实部全 $<0$（指数衰减型通解；单零根给常数、复纯虚给振荡，均使积分发散或条件不普适）。
【技巧】$ r^{2}-2ar+(a+2)=0$ 的根实部 $=a<0$? 韦达：两根和 $=2a<0$ 且积 $=a+2>0$ → $-2<a<0$；再核复根条件（$\\Delta<0$ 时实部 $=a$）。
【易错】$ a=0$ 时根 $\\pm\\sqrt2\\mathrm i$ 纯虚 → 通解振荡不衰减 → 积分发散（排除端点）；$\\Delta\\ge0$ 分支的根符号。
【注意】答案 C。""",
4: """【公式】$ f=o(g)$ 的高阶传递：$ f+g\\sim g$、$ f\\cdot g$ 的阶 = 阶和、$ f^{2}=o(g^{2})$? 与 $\\sqrt{|g|}$ 型的相对阶。
【技巧】逐项算阶：$\\dfrac{f\\cdot g}{?}\\cdots$ 选项里"$f$ 与 $f\\cdot g$ 谁高阶"——$ f\\cdot g$ 的阶 = 阶和 > $f$ 的阶 → $ f\\cdot g$ 是 $ f$ 的高阶 → 选对应 C。
【易错】$ f+g\\sim g$（低阶吸收高阶）的方向；$ f^{2}$ 与 $ g$ 的阶比较需知道具体阶数。
【注意】答案 C。""",
5: """【公式】换序：$ D:\\ 4-x^{2}\\le y\\le4$（$x\\in[-2,2]$）⟺ $ 0\\le y\\le4,\\ -\\sqrt{4-y}\\le x\\le\\sqrt{4-y}$。
【技巧】$ y=4-x^{2}\\iff x^{2}=4-y$ → 换序后 $\\int_0^{4}\\left[\\displaystyle\\int_{-\\sqrt{4-y}}^{\\sqrt{4-y}}f\\right]\\mathrm dy$。
【易错】抛物线开口向下的区域（$y$ 从 $4-x^{2}$ 到 4）；$\\sqrt{4-y}$ 的符号（取正负两支）。
【注意】答案 A。""",
6: """【公式】引力分量：$\\overrightarrow{QP}=(x,-1)$、$ r=\\sqrt{x^{2}+1}$ → $ P$ 对 $ Q$ 的引力沿 $\\overrightarrow{QP}$ 单位化 × $\\dfrac{G}{r^{2}}$。
【技巧】$ F_x=\\dfrac{G\\cdot x}{(x^{2}+1)^{3/2}}$、$ F_y=\\dfrac{-G}{(x^{2}+1)^{3/2}}$（按数据 B 的积分表达）——$\\displaystyle\\int_0^{+\\infty}\\dfrac{x\\,\\mathrm dx}{(x^{2}+1)^{3/2}}=1$、$\\displaystyle\\int_0^{+\\infty}\\dfrac{\\mathrm dx}{(x^{2}+1)^{3/2}}=1$（$\\dfrac{u}{\\sqrt{1+u^{2}}}$ 端值）。
【易错】引力的方向向量与距离三次方的组合；积分的物理意义（$ x\\to\\infty$ 时分量趋于有限）。
【注意】答案 B。""",
7: """【公式】① $\\lim\\dfrac{|f|-f(0)}{x}$ 存在 ⇒ $|f(0)|=f(0)$ 即 $ f(0)\\ge0$；② $\\lim\\dfrac{f(x)-f(0)}{|x|}$ 存在 ⇒ $ f(0)=0$ 且左右导数互为相反数。
【技巧】③④关于 $\\lim\\dfrac{|f(x)|-|f(0)|}{x}$ 与 $\\lim\\dfrac{f(x)-f(0)}{|x|}$——用 $ f(0)>0$、$=0$、$<0$ 三种情形分类讨论可导性。
【易错】$ f(0)=0$ 时 $\\lim\\dfrac{|f(x)|}{x}$：$f(x)>0$ 侧与 <0 侧符号随 $|x|$ 变——左右导数差一个负号 → 不存在（若 $f$ 过零且两侧异号）。
【注意】答案 D。""",
8: """【公式】分块对角特征：$|\\lambda E-A|=(b-\\lambda)\\left[(1-\\lambda)(a-\\lambda)-4\\right]$ → 特征值 $ b$ 与 $\\dfrac{1+a\\pm\\sqrt{(a-1)^{2}+16}}{2}$。
【技巧】一个正 + 两个负：$ b>0$ 且 $ a+1<0$（$(1+a)/2<0$，即二重分支全负：$(1+a)^{2}-16>0$ 且和为 $1+a<0$）→ 按数据 D 的组合。
【易错】$(a-1)^{2}+16>0$ 恒真 → 二重分支的实部条件由韦达读：两根之和 $1+a<0$ 且两根之积 $a-3<0$? 按解析配平。
【注意】答案 D。""",
9: """【公式】行变换可逆（保行空间）→ "能行变换得到" ⟺ 两矩阵行等价 ⟺ 行最简形相同 → 答案矩阵的行空间 = 候选矩阵的行空间。
【技巧】算候选矩阵的行最简形（或秩 + 行空间一致）：秩 2 且首两行张成 $\\langle(1,1,0,1),(0,0,1,2)\\rangle$。
【易错】秩相同不充分（行空间须一致）；行变换不可逆方向——"得到"是双向行等价。
【注意】答案 B。""",
10: """【公式】$ r(AB)=r(BA)+1$：三阶矩阵的秩组合——$ r(BA)\\ge1$、$ r(AB)\\le3$。
【技巧】构造反例（$ A=\\mathrm{diag}(1,1,0)$ 型）核选项；$ r(AB)=r(BA)+1$ 意味着两乘积秩不同 → 排除"恒有 $r(AB)=r(BA)$"的选项。
【易错】秩不等式 $ r(AB)\\ge r(A)+r(B)-n$ 的使用；构造 $ A,B$ 的具体形态。
【注意】答案 D。""",
11: """【公式】部分分式：$ \\dfrac{a}{x(2x+a)}=\\dfrac{1}{x}-\\dfrac{2}{2x+a}$（验证：$ 2x+a-2x=a$ ✓）。
【技巧】$ \\displaystyle\\int_1^{+\\infty}\\left(\\dfrac1x-\\dfrac{2}{2x+a}\\right)\\mathrm dx=\\left[\\ln\\dfrac{x}{2x+a}\\right]_1^{\\infty}=\\ln\\dfrac{1}{2}-\\ln\\dfrac{1}{2+a}=\\ln\\dfrac{2+a}{2}=\\ln2$ → $ a=2$。
【易错】$\\dfrac{2}{2x+a}$ 的系数 2（分子凑 $\\mathrm d(2x+a)$）；$\\to\\infty$ 端比值 →1。
【注意】$a=2$。""",
12: """【公式】立方根曲线：$\\dfrac yx=\\left(1-\\dfrac3x+\\dfrac{1}{x^{2}}\\right)^{1/3}\\sim1-\\dfrac{1}{x}+\\cdots$ → 斜渐近线 $ y=x-1$。
【技巧】$\\dfrac{x^{3}-3x^{2}+1}{}$ 立方展开：$(x-1)^{3}=x^{3}-3x^{2}+3x-1$ → $ x^{3}-3x^{2}+1=(x-1)^{3}-3x+2$ → $ y=\\sqrt[3]{(x-1)^{3}-3x+2}\\approx x-1$（尾项 →0）。
【易错】$\\sqrt[3]{(x-1)^{3}}=x-1$ 的主项；尾项 $-3x+2$ 的三阶小量处理。
【注意】$y=x-1$。""",
13: """【公式】黎曼和：$ \\dfrac{1}{n^{2}}\\sum k\\ln\\dfrac kn=\\dfrac1n\\sum\\dfrac kn\\ln\\dfrac kn\\to\\displaystyle\\int_0^{1}x\\ln x\\,\\mathrm dx=-\\dfrac14$。
【技巧】$\\displaystyle\\int_0^{1}x\\ln x\\,\\mathrm dx=\\left[\\dfrac{x^{2}}{2}\\ln x-\\dfrac{x^{2}}{4}\\right]_0^{1}=-\\dfrac14$（$x\\ln x\\to0$）。
【易错】上限是 $\\tfrac{n-1}{n}$ 与 $\\tfrac kn$ 的端点差（末项 $ k=n$ 时 $\\ln\\tfrac nn=0$，计入不计入不影响）。
【注意】答案 $-\\dfrac14$。""",
14: """【公式】第二个方程变限积分上限含 $ y+t^{2}$ → 对 $ t$ 求导：$2-\\mathrm e^{-(y+t^{2})^{2}}\\cdot\\left(y'+2t\\right)=0$。
【技巧】$ x=\\ln(1+2t)$ → $x=0$ 时 $ t=0$；代第二个方程 $ y(0)+0$? 定 $ y(0)=1$? 由 $2\\cdot0-\\displaystyle\\int_1^{y}??$ 核对——按数据解析：$ y(0)=?$ 且 $t=0$ 时 $ y'=\\mathrm e$。
【易错】$ y+t^{2}$ 在 $t=0$ 处 $=y(0)$；$\\mathrm e^{-(y+t^{2})^{2}}$ 的链式。
【注意】$\\left.\\dfrac{\\mathrm dy}{\\mathrm dx}\\right|=\\dfrac{y'+2t}{\\dfrac{1}{1+2t}}$? 链式除 $ x'_t=\\dfrac{2}{1+2t}$ → 答案 $\\mathrm e$。""",
15: """【公式】全微分判定：$\\dfrac{\\partial}{\\partial y}(2y-3x)=2$、$\\dfrac{\\partial}{\\partial x}(2x-5y)=2$ 相等 → 恰当微分方程。
【技巧】存在 $ U(x,y)$ 使 $ U_x=2y-3x,\\ U_y=2x-5y$：积 $ U=2xy-\\tfrac{3x^{2}}{2}+\\varphi(y)$，对 $y$ 定 $\\varphi'=-5y$ → $ U=2xy-\\tfrac32x^{2}-\\tfrac52y^{2}=C$。
【易错】恰当性验证是第一步；初值 $ y(1)=1$ → $ U(1,1)=2-\\tfrac32-\\tfrac52=4$? 按数据 $=4$ 核对。
【注意】$5y^{2}-4xy+3x^{2}=4$。""",
16: """【公式】$\\alpha_1,\\alpha_2,\\alpha_3$ 无关 + $\\alpha_4=?$ 表示 → $ r(A)=3$；$ Ax=\\beta$? 基础解系 1 个。
【技巧】$\\alpha_4=\\alpha_1+?\\alpha_2+?\\alpha_3$ 读表示系数 → 特解；$\\alpha_1-\\alpha_2+\\alpha_3-\\alpha_4=0$? 的系数组合 → 基础解系 $(1,1,-1,-1)^{\\mathrm T}$。
【易错】表示系数的符号；特解与基础解系的来源（列关系直读，不用解方程组）。
【注意】$ x=k(1,1,-1,-1)^{\\mathrm T}+(1,0,0,4)^{\\mathrm T}$。""",
17: """【公式】部分分式：$ \\dfrac{1}{(1+x)(x^{2}-2x+2)}=\\dfrac{A}{1+x}+\\dfrac{Bx+D}{x^{2}-2x+2}$；$ x^{2}-2x+2=(x-1)^{2}+1$ → $\\arctan(x-1)$ 型。
【技巧】$ A=\\dfrac{1}{1+1-2+2}=\\dfrac12$? 代 $ x=-1$：$ A=\\dfrac{1}{1+3}=\\dfrac14$? 按 $\\dfrac{3}{10}\\ln2$ 反推 $ A$ 的分母——按数据解析定 $ A,B,D$。
【易错】$\\arctan(x-1)\\Big|_0^{1}=0-\\left(-\\tfrac{\\pi}{4}\\right)=\\tfrac{\\pi}{4}$；$\\ln$ 项在两端的值。
【注意】$ \\dfrac{3}{10}\\ln2+\\dfrac{\\pi}{10}$。""",
18: """【公式】分母 $\\ln(1+x)+\\ln(1-x)=\\ln(1-x^{2})\\sim-x^{2}$：分子 $ x f(x)-\\mathrm e^{2\\sin x}+1$ 中 $\\mathrm e^{2\\sin x}-1\\sim2\\sin x\\sim2x$。
【技巧】极限存在 + 分母 $\\sim-x^{2}$ → 分子 $ xf(x)-2x\\to0$? 逐阶：$\\dfrac{xf(x)-2x}{-x^{2}}=-\\dfrac{2}{5}?$? 按数据解析的系数读 $ f(0)$ 与 $ f'(0)$。
【易错】$\\mathrm e^{2\\sin x}=1+2\\sin x+2\\sin^{2}x+\\cdots$ 展开到 $ x^{2}$；$f$ 连续 → $ f(0)=2$。
【注意】$ f'(0)=5$。""",
19: """【公式】全微分恰当性：$ \\dfrac{\\partial}{\\partial y}(-2x\\mathrm e^{-y})=2x\\mathrm e^{-y}=\\dfrac{\\partial}{\\partial x}\\left(\\mathrm e^{-y}(x^{2}-y-1)\\right)$? ——$\\partial_x=2x\\mathrm e^{-y}$ ✓ 恰当。
【技巧】$ f=\\displaystyle\\int(-2x\\mathrm e^{-y})\\mathrm dx=-x^{2}\\mathrm e^{-y}+\\varphi(y)$，对 $y$ 求导配 $ \\mathrm e^{-y}(x^{2}-y-1)$ → $\\varphi(y)=(y+2)\\mathrm e^{-y}-? \\cdots$；$f(0,0)=2$ 定常数。
【易错】$\\varphi(y)$ 的方程（$ \\mathrm e^{-y}(-y-1)+\\varphi'=\\mathrm e^{-y}(x^{2}-y-1)$ 中 $ x^{2}$ 项已由第一块吸收）。
【注意】$ f=-x^{2}\\mathrm e^{-y}+(y+2)\\mathrm e^{-y}$? 核 $f(0,0)=2$ ✓；$ f(0,-1)=\\mathrm e$ 极大（$y$ 方向二阶判别）。""",
20: """【公式】双圆域交集：$ x^{2}+y^{2}\\le4x$（圆心 $(2,0)$）与 $ \\le4y$（圆心 $(0,2)$）→ 交叠叶形，极坐标：$ r\\le4\\cos\\theta$ 与 $ r\\le4\\sin\\theta$ → $\\theta\\in[0,\\tfrac\\pi4]$ 取 $ r\\le4\\sin\\theta$（小者）、$\\theta\\in[\\tfrac\\pi4,\\tfrac\\pi2]$ 取 $ r\\le4\\cos\\theta$。
【技巧】$ x-y=r(\\cos\\theta-\\sin\\theta)$：分两段极坐标积分，$\\cos-\\sin$ 与 $\\sin-\\cos$ 互为相反 → 合并系数倍增；$\\int(\\sin\\theta)^{?}\\cdots$ 三角积分。
【易错】两圆的交点在 $\\theta=\\tfrac\\pi4$（$ r=2\\sqrt2$）；分段后 $(\\cos-\\sin)$ 的符号（第一段正、第二段负 → 用绝对值或交换限）。
【注意】$12\\pi-\\dfrac{112}{3}$。""",
21: """【公式】严格凸的弦不等式：$ f'$ 严格增 $\\Leftrightarrow$ 对任意 $ x_1<x<x_2$（$ x_1,x_2\\in(a,b)$），$\\dfrac{f(x_2)-f(x)}{x_2-x}>\\dfrac{f(x)-f(x_1)}{x-x_1}$ 型三点不等式（按数据的两段结构）。
【技巧】必要性：拉格朗日于 $[x_1,x]$、$[x,x_2]$ → $ f'(\\xi_1)<f'(\\xi_2)$（$\\xi_1<\\xi_2$ 严格增）→ 斜率严格增 → 不等式。
【易错】充分性：任取 $ u<v<w\\in(a,b)$ 用三点条件 + 连续性传递到 $ f'$ 严格增（二分/介值论证）。
【注意】三点条件的两种写法（数据解析的形式）与中值定理的对接。""",
22: """【公式】相似：$\\operatorname{tr}A=5+a? =\\operatorname{tr}B$ 与 $|A|=|B|$ 联立 → $ a=4$；$\\lambda$ 由 $B$ 读。
【技巧】(2) 正交变换：$|A|=\\prod\\lambda=k>0$ + 二重特征值的秩条件 → $ k=3$、$Q$ 由单位正交特征向量拼成。
【易错】$a=4$ 的联立（迹 + 行列式）；正交阵的列规范（$\\dfrac{1}{\\sqrt2},\\dfrac{1}{\\sqrt6}$ 型系数）。
【注意】(I) $a=4,\\ k>0$；(II) $k=3$，$Q=\\begin{pmatrix}-\\frac1{\\sqrt2}&-\\frac1{\\sqrt6}&\\cdots\\end{pmatrix}$（按数据解析列序）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2025数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2025数二真题.md', TIPS_2025)
