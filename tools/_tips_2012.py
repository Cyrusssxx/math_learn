# -*- coding: utf-8 -*-
# 2012 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2012 = {
1: """【公式】$y=\\dfrac{x^{2}+x}{x^{2}-1}=\\dfrac{x}{x-1}$（约去 $x+1$）：垂直 $x=1$、水平 $y=1$（$x\\to\\infty$ 时 $\\dfrac x{x-1}\\to1$）。
【技巧】约分后再数渐近线——被约掉的 $x=-1$ 是可去间断点，不产生垂直渐近线。
【易错】垂直渐近线只有 $x=1$（$x=-1$ 约掉了）；斜渐近线与水平渐近线不并存（同侧只算一条）。
【注意】共 2 条（答案 C）。""",
2: """【公式】单因式求导：$f'(0)=(\\mathrm e^{0}-1)'$ 所在因子取导、其余因子取值——$f'(0)=\\left[(\\mathrm e^{x}-1)\\right]'_{x=0}\\cdot(1-2)\\cdots(1-n)$。
【技巧】$f(0)=0$（$\\mathrm e^{0}-1=0$ 的因子）→ 只需求导"那个为零的因子"：$f'(0)=1\\cdot(-1)(-2)\\cdots(1-n)=(-1)^{n-1}(n-1)!$。
【易错】逐因子全展开乘积法则会累死；连乘 $(1-2)(1-3)\\cdots(1-n)=(-1)^{n-1}(n-1)!$。
【注意】答案 A（$(-1)^{n-1}(n-1)!$）。""",
3: """【公式】单向链条：$\\{S_n\\}$ 有界（+单调增）→ $S_n$ 收敛 → $a_n=S_n-S_{n-1}\\to0$；反之 $a_n\\to0$ 推不出有界（调和级数反例）。
【技巧】正项级数部分和单调增是"有界 ⟺ 收敛"的桥。
【易错】$a_n\\to0$ 只是必要条件——$\\sum\\tfrac1n$ 是灵魂反例。
【注意】答案 B（有界是收敛的充要 → 是 $a_n\\to0$ 的充要）。""",
4: """【公式】分段比较：$I_2-I_1=\\displaystyle\\int_\\pi^{2\\pi}\\mathrm e^{x^{2}}\\sin x\\,\\mathrm dx<0$（$\\sin<0$ 且 $\\mathrm e^{x^{2}}$ 更大）；$I_3-I_2=\\displaystyle\\int_{2\\pi}^{3\\pi}>0$。
【技巧】周期平移比较：$I_3-I_2$ 段的 $\\mathrm e^{x^{2}}$ 大于 $I_2-I_1$ 段对应点 → $|I_3-I_2|>|I_2-I_1|$ → $I_3>I_1$。
【易错】被积函数非周期（$\\mathrm e^{x^{2}}$ 增长）——同符号区间比较要"对应点代换"（$x\\to x-\\pi$）。
【注意】答案 D（$I_2<I_1<I_3$）。""",
5: """【公式】偏导符号 = 单调方向：$f'_x>0$ → $f$ 关于 $x$ 严格增；固定另一变量的累次极限比较 $f(x_1,y)-f(x_2,y)$。
【技巧】$x_1<x_2,y_1<y_2$ 时沿路径比较：先沿 $x$ 增、再沿 $y$ 减——$f(x_1,y_1)<f(x_2,y_1)$ 且 $f(x_2,y_1)<f(x_2,y_2)$ 链出结果。
【易错】可微/偏导正只保证各变量单调，不给"联合"结构——别引入泰勒余项乱估计。
【注意】答案 D（$f(x_1,y_2)<f(x_2,y_1)$ 的具体组合按选项核对：$x_1<x_2,y_1<y_2$ 时 $f(x_1,y_1)$ 与 $f(x_2,y_2)$ 的大小不定，但 $f(x_1,y_2)$ 与 $f(x_2,y_1)$ 有定序）。""",
6: """【公式】对称性：$D$ 关于 $x=0$（$y$ 轴）对称？——$D$ 由 $y=\\sin x$（奇）、$x=\\pm\\tfrac\\pi2$、$y=1$ 围成 → 关于 $y$ 轴对称。
【技巧】$x^{5}y$ 关于 $x$ 是奇 → 该项积分为 0；剩下 $-\\displaystyle\\iint 1\\,\\mathrm d\\sigma=-$（区域面积）。
【易错】区域面积 = $\\displaystyle\\int_{-\\pi/2}^{\\pi/2}(1-\\sin x)\\,\\mathrm dx=\\pi-2$（$\\sin$ 奇函数积分为 0）。
【注意】答案 $2-\\pi$（选 D）。""",
7: """【公式】$\\alpha_1=\\begin{pmatrix}0\\\\0\\\\c_1\\end{pmatrix}$ 与 $\\alpha_2,\\alpha_3,\\alpha_4$ 的线性组合 → 齐次方程组 $(0,0,c_1)$ 型判断。
【技巧】$\\alpha_1,\\alpha_3,\\alpha_4$ 的行列式按第一列只有 $c_1$ 展开；无关 $\\Leftrightarrow c_1\\ne0$ 且对应 2×2 子式 $\\ne0$。
【易错】四个选项分别是"不同子向量组"的相关/无关判断——用"部分组无关、加向量后相关"的结构逐个核。
【注意】答案 C。""",
8: """【公式】$Q=(\\alpha_1+\\alpha_2,\\alpha_2,\\alpha_3)=P\\underbrace{\\begin{pmatrix}1&0&0\\\\1&1&0\\\\0&0&1\\end{pmatrix}}_{C}$ → $Q^{\\mathrm T}AQ=C^{\\mathrm T}(P^{\\mathrm T}AP)C$。
【技巧】$P^{-1}AP=\\mathrm{diag}(1,1,2)$ → $Q^{\\mathrm T}AQ=C^{\\mathrm T}\\Lambda C$（$3\\times3$ 小乘法）。
【易错】$C$ 的列 = 新列的表示系数；算完 $\\begin{pmatrix}2&1&0\\\\1&1&0\\\\0&0&2\\end{pmatrix}$ 型。
【注意】答案 B。""",
9: """【公式】隐函数：$x=0$ 时 $1-y=\\mathrm e^{y}$ → $y=0$；一阶 $2x-y'=\\mathrm e^{y}y'$ → $y'(0)=0$。
【技巧】二阶对 $2x-y'=\\mathrm e^{y}y'$ 再求导：$2-y''=\\mathrm e^{y}(y'^{2}+y'')$，代 $(0,0)$ 得 $2-y''=y''$。
【易错】$\\mathrm e^{y}y'$ 乘积求导；$y'(0)=0$ 让 $\\mathrm e^{0}\\cdot y'^{2}$ 项消失。
【注意】$y''(0)=1$。""",
10: """【公式】黎曼和：$n\\displaystyle\\sum_{i=1}^{n}\\frac{1}{i^{2}+n^{2}}=\\frac1n\\sum_{i=1}^{n}\\frac{1}{1+(i/n)^{2}}\\to\\int_0^{1}\\frac{\\mathrm dx}{1+x^{2}}$。
【技巧】$\\dfrac{n^{2}}{i^{2}+n^{2}}=\\dfrac{1}{1+(i/n)^{2}}$ 的因式配平。
【易错】$\\arctan x\\Big|_0^1=\\dfrac\\pi4$。
【注意】答案 $\\dfrac\\pi4$。""",
11: """【公式】$z=f(u)$，$u=\\ln x+\\dfrac1y$：$z_x=\\dfrac1x f'$、$z_y=-\\dfrac1{y^{2}}f'$。
【技巧】$x\\dfrac{\\partial z}{\\partial x}+\\dfrac{y^{2}}{?}\\dfrac{\\partial z}{\\partial y}$? 按题给组合代入系数：$x\\cdot\\dfrac1x+? $ 与 $y^{2}\\cdot(-\\dfrac1{y^{2}})$ 相消 → 0。
【易错】单中间变量 $f'$ 只有一个——组合系数凑成 $1-1=0$。
【注意】答案 0。""",
12: """【公式】把 $x$ 看作 $y$ 的函数：$\\dfrac{\\mathrm dx}{\\mathrm dy}+\\dfrac{x}{y}=3y$（一阶线性，积分因子 $y$）→ $(xy)'=3y^{2}$。
【技巧】"对 $y$ 解"的识别：$x$ 的次数低、$y^{2}$ 在另一项——反转自变量是标准动作。
【易错】$(xy)'=3y^{2}$ 积分 $xy=y^{3}+C$；初值 $(1,1)$ 定 $C=0$。
【注意】$y^{2}=x$ 即 $y=\\sqrt x$。""",
13: """【公式】曲率 $K=\\dfrac{|y''|}{(1+y'^{2})^{3/2}}=\\dfrac{2}{\\left[1+(2x+1)^{2}\\right]^{3/2}}=\\dfrac{\\sqrt2}{2}$。
【技巧】$\\left[1+(2x+1)^{2}\\right]^{3/2}=2^{3/2}$ → $1+(2x+1)^{2}=2$ → $2x+1=\\pm1$ → $x=0$（舍，$x<0$）或 $x=-1$。
【易错】$x<0$ 的定义域筛掉 $x=0$；$\\left(\\dfrac{\\sqrt2}{2}\\right)^{-2/3}=2$ 的反解。
【注意】点 $(-1,0)$。""",
14: """【公式】$|B|=-|A|$（行交换）；$|A^{*}|=|A|^{n-1}=9$。
【技巧】$|BA^{*}|=|B|\\cdot|A^{*}|=-3\\cdot9=-27$。
【易错】$|A^{*}|=|A|^{2}$（3 阶 $n-1=2$）；行交换行列式变号。
【注意】答案 $-27$。""",
15: """【公式】(I) $a=\\lim\\dfrac{x(1+x)-\\sin x}{x\\sin x}\\sim\\lim\\dfrac{x+\\tfrac{x^{3}}{6}?}{}\\cdots$：$\\sin x=x-\\tfrac{x^{3}}{6}+\\cdots$ → 分子 $x^{2}+\\dfrac{x^{3}}{6}$，分母 $\\sim x^{2}$ → $a=1$。
【技巧】(II) $f(x)-a$ 与 $x^{k}$ 同阶：分子 $\\dfrac{1+x}{\\sin x}-\\dfrac1x-1$ 通分后泰勒展开到三阶（$x^{3}$ 项系数非零 → $k=1$）。
【易错】$\\sin x=x-\\tfrac{x^{3}}{6}+\\cdots$ 的三阶项在分子里起作用；$k$ 由最低非零项次数定。
【注意】$a=1,\\ k=1$。""",
16: """【公式】$f_x=(1-x^{2})\\mathrm e^{-\\frac{x^{2}+y^{2}}{2}}$、$f_y=-xy\\,\\mathrm e^{-\\cdots}$。
【技巧】驻点：$f_x=0\\Rightarrow x=\\pm1$；$f_y=0\\Rightarrow x=0$ 或 $y=0$ → 驻点 $(1,0),(-1,0),(0,\\pm?)$——$(1,0)$ 与 $(-1,0)$ 两点；$A,C$ 判别（$AC-B^{2}>0$ 且 $A$ 号）。
【易错】$f_y=0$ 的两支：$x=0$（此时 $f_x=1\\ne0$ 舍）或 $y=0$；$f_{yy}$ 的符号。
【注意】极大 $\\mathrm e^{-1/2}$（$(1,0)$）、极小 $-\\mathrm e^{-1/2}$（$(-1,0)$）。""",
17: """【公式】切线：$y=\\dfrac1{x_0}x+\\ln x_0-1$ 过 $(0,1)$ → $\\ln x_0=2$ → $x_0=\\mathrm e^{2}$、切点 $A(\\mathrm e^{2},2)$；$B$ 为 $L$ 与 $x$ 轴交点（$x=1$）。
【技巧】面积 = 切线与 $L$、$x=1$ 之间的三角形/曲边差；旋转体绕 $x$ 轴 washer 或绕 $y$ 轴（按题）。
【易错】切线截距 $\\ln x_0-1=1$ 与过 $(0,1)$ 的匹配；区域 $D$ 的边界识别。
【注意】面积 $\\mathrm e^{2}-1$；体积 $\\dfrac{2\\pi}{3}(\\mathrm e^{2}+3)$。""",
18: """【公式】心形线右瓣 $r=1+\\cos\\theta$（$0\\le\\theta\\le\\pi$）：$\\displaystyle\\iint xy\\,\\mathrm d\\sigma=\\int_0^{\\pi}\\mathrm d\\theta\\int_0^{1+\\cos\\theta}r^{3}\\cos\\theta\\sin\\theta\\,\\mathrm dr$。
【技巧】内层 $=\\dfrac{(1+\\cos\\theta)^{4}}{4}\\cos\\theta\\sin\\theta$；换元 $u=\\cos\\theta$（$\\mathrm du=-\\sin\\theta\\,\\mathrm d\\theta$）：$\\dfrac14\\displaystyle\\int_0^{1}(1+u)^{4}u\\,\\mathrm du$。
【易错】$\\sin\\theta\\ge0$ 消绝对值；$u$ 换元后 $u\\in[1,0]$ 翻转限。
【注意】答案 $\\dfrac{16}{15}$。""",
19: """【公式】联立两方程：$f''+f'-2f=0$ 与 $f''+f=2\\mathrm e^{x}$ 相减 → $f'-3f=-2\\mathrm e^{x}$（一阶线性！不用解二阶）。
【技巧】$f=C\\mathrm e^{-3x}+\\dfrac23\\mathrm e^{x}$ 代回第二方程定 $C=\\dfrac13$? 验证得 $f=\\mathrm e^{x}$（$C=0$ 由 $f''+f'=3\\mathrm e^{x}-2\\mathrm e^{x}=\\mathrm e^{x}$ 一致）。
【易错】两方程相减是本题的钥匙（消去 $f''$）；通解常数由相容性定。
【注意】(I) $f=\\mathrm e^{x}$；(II) $y=f(x^{2})$ 拐点：$\\left[f(x^{2})\\right]''$ 在 $x=0$ 处变号 → 拐点 $(0,0)$。""",
20: """【公式】奇偶延拓：$f(-x)=f(x)$（$x\\ln\\dfrac{1+x}{1-x}$ 奇 + $\\cos x-1-\\tfrac{x^{2}}2$ 偶 → 整体偶）→ 只需证 $x\\ge0$。
【技巧】$f'(x)=\\ln\\dfrac{1+x}{1-x}+x\\cdot\\dfrac2{1-x^{2}}-\\sin x-x$：$\\ln\\dfrac{1+x}{1-x}=2\\left(x+\\dfrac{x^{3}}{3}+\\cdots\\right)$ 逐步验证 $f'\\ge0$ → $f(0)=0$ 为最小。
【易错】$f'$ 的两个正项来源（$\\ln$ 展开与 $\\dfrac{2x}{1-x^{2}}$）；偶函数免一半工作量。
【注意】最小值 $f(0)=0$ 即不等式。""",
21: """【公式】(I) 零点定理：$f_n(\\tfrac12)=\\tfrac12+\\cdots+(\\tfrac12)^{n-1}<1$ → $f_n(\\tfrac12)<0$；$f_n(1)=n-1>0$ → $(\\tfrac12,1)$ 内有根；$f_n'(x)=\\left(1-x^{n}\\right)/(1-x)>0$? 正项和递增 → 唯一根。
【技巧】(II) $x_n\\in(\\tfrac12,1)$ 且 $x_{n}^{n}\\to0$：方程两边取 $n$ 次幂相关的极限——$x_n^{n-1}(1+x_n)=\\cdots$ 用 $x_n^{n}\\to0$ 传递 → $\\lim x_n=\\dfrac12$。
【易错】唯一性用 $f_n$ 严格增；$\\lim x_n\\ge\\tfrac12$ 与 $x_n^{n}\\to0$ 的联动。
【注意】$\\lim x_n=\\dfrac12$。""",
22: """【公式】(I) 按第一行展开：$|A|=1\\cdot(1-a^{?})-a\\cdot(a-a^{3})?\\cdots=1-a^{4}$（四项循环结构）。
【技巧】(II) 无穷多解 → $|A|=0$ → $a=\\pm1$：$a=1$ 时 $r(A)=1\\ne r(\\bar A)$ 无解；$a=-1$ 时 $r(A)=r(\\bar A)=3<4$ → 通解 $x=(0,-1,0,0)^{\\mathrm T}+k(1,1,1,1)^{\\mathrm T}$。
【易错】$a=1$ 分支是无解（不是无穷多解）；特解 $(-1?)$ 按数据 $(-1,0,0)$ 型核对。
【注意】$a=-1$；通解如上。""",
23: """【公式】(I) $A^{\\mathrm T}A$ 正定 ⟺ $r(A^{\\mathrm T}A)=r(A)$? 标准结论：$A^{\\mathrm T}A$ 正定 $\\Leftrightarrow r(A)=n$（列满秩）。$r(A)=2\\ne3$ → 不正定。
【技巧】$r(A^{\\mathrm T}A)=r(A)$（$A^{\\mathrm T}Ax=0$ 与 $Ax=0$ 同解）→ 二次型 $f=x^{\\mathrm T}A^{\\mathrm T}Ax=|Ax|^{2}$ 的零空间即 $Ax=0$ 的解空间。
【易错】(II) $A^{\\mathrm T}A$ 的正惯性指数 = $r(A)=2$ → 标准形 $2y_2^{2}+6y_3^{2}$（特征值 $0,2,6$）。
【注意】(I) 不正定；(II) $Q=(\\alpha_1,\\alpha_2,\\alpha_3)$，$f=2y_2^{2}+6y_3^{2}$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2012数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2012数二真题.md', TIPS_2012)
