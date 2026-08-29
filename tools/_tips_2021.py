# -*- coding: utf-8 -*-
# 2021 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2021 = {
1: """【公式】$\\mathrm e^{t^{3}}-1\\sim t^{3}$ → $\\displaystyle\\int_0^{x^{2}}\\left(\\mathrm e^{t^{3}}-1\\right)\\mathrm dt\\sim\\displaystyle\\int_0^{x^{2}}t^{3}\\,\\mathrm dt=\\dfrac{x^{8}}{4}$。
【技巧】被积无穷小 → 积分升阶（上端 $x^{2}$ 代入 $t^{3}$ 变 $x^{8}$）。
【易错】$\\dfrac{x^{8}}{4}$ 与 $x^{7}$ 比较：$\\dfrac{\\tfrac{x^{8}}4}{x^{7}}=\\dfrac x4\\to0$ → 是 $x^{7}$ 的**高阶**无穷小。
【注意】答案 C（高阶）。""",
2: """【公式】$f(0)=1$、$\\lim\\dfrac{\\mathrm e^{x}-1}{x}=1$ → 连续；导数定义 $\\lim\\dfrac{f(x)-f(0)}{x}=\\lim\\dfrac{\\tfrac{\\mathrm e^{x}-1}{x}-1}{x}=\\lim\\dfrac{\\mathrm e^{x}-1-x}{x^{2}}=\\dfrac12$。
【技巧】$\\mathrm e^{x}-1-x\\sim\\tfrac{x^{2}}2$（泰勒展开差项）。
【易错】"连续但不可导"与"可导"的选项区分——本题导数存在（$=\\tfrac12$），既连续又可导。
【注意】答案 D。""",
3: """【公式】$ V=\\pi r^{2}h$ → $ \\dfrac{\\mathrm dV}{\\mathrm dt}=\\pi\\left(2rh'\\cdot? \\right)$：$ \\dfrac{\\mathrm dV}{\\mathrm dt}=\\pi\\left(2r\\dfrac{\\mathrm dr}{\\mathrm dt}h+r^{2}\\dfrac{\\mathrm dh}{\\mathrm dt}\\right)$。
【技巧】代 $r=10,h=5$? 按题给高：$ \\dfrac{\\mathrm dV}{\\mathrm dt}=\\pi(2\\cdot10\\cdot2\\cdot h+100\\cdot(-3))$——$h$ 用题给值（$h=5\\,\\mathrm{cm}$? 按题面）。
【易错】$ h'=-3$ 的负号（高在减小）；乘积法则两项。
【注意】按数据解析（$\\pi$ 系数的选项 C）。""",
4: """【公式】$ f'=a-\\dfrac bx$，驻点 $ x=\\dfrac ba$；$ f''=\\dfrac b{x^{2}}$ 符号看 $b$。
【技巧】两个零点 ⟺ 极大值 $>0$ 且极小值 $<0$；$ f\\to\\pm\\infty$ 端点行为（$x\\to0^{+}$ 由 $-b\\ln x$ 控制、$ x\\to\\infty$ 由 $ax$ 控制）。
【易错】$ b$ 的符号决定极值是极大还是极小；两个零点需要极大极大或极大极小的组合（画 $ y=ax$ 与 $ y=b\\ln x$ 的相对位置）。
【注意】答案 A。""",
5: """【公式】$\\sec x=1+\\dfrac{x^{2}}{2}+o(x^{2})$（由 $\\cos x=1-\\dfrac{x^{2}}{2}+\\cdots$ 取倒数）→ $ a=0,\\ b=\\dfrac12$。
【技巧】$\\dfrac{1}{1-u}=1+u+\\cdots$，$ u=\\dfrac{x^{2}}{2}$；一阶项为 0（偶函数）。
【易错】$ f''(0)=1$（$\\tfrac{x^{2}}{2}$ 系数 ×2）；$ b=\\dfrac{f''(0)}{2}$。
【注意】答案 D。""",
6: """【公式】两条曲线条件都对 $ f$ 求导（链式）：$ f_1'(x+1,\\mathrm e^{x})+\\mathrm e^{x}f_2'(x+1,\\mathrm e^{x})=(x+1)(3x+1)$；$ f_1'(x,x^{2})\\cdot1+f_2'(x,x^{2})\\cdot2x=4x\\ln x+2x$。
【技巧】代 $ x=1$：第一条给 $ f_1'(2,\\mathrm e)+\\mathrm e f_2'(2,\\mathrm e)=4$；第二条给 $ f_1'(1,1)+2f_2'(1,1)=2$；再代 $ x=0$（第一条）：$ f_1'(1,1)+f_2'(1,1)=0$——两方程解 $ f_1'(1,1),f_2'(1,1)$。
【易错】$\\mathrm e^{x}$ 在 $ x=0$ 处 $=1$、$ x+1=1$ → 点恰为 $(1,1)$；第二条曲线在 $ x=1$ 时点也是 $(1,1)$（$ x=x^{2}=1$）——两个条件在同一个点交汇是本题设计。
【注意】$\\mathrm df(1,1)=f_1'(1,1)\\,\\mathrm dx+f_2'(1,1)\\,\\mathrm dy$，答案 C。""",
7: """【公式】黎曼和：$\\displaystyle\\int_0^1 f=\\lim\\limits_{n\\to\\infty}\\dfrac1n\\displaystyle\\sum_{k=1}^{n}f\\left(\\tfrac kn\\right)$——题给和式需配平成此形式。
【技巧】$ f(x)=\\dfrac{1}{1+?}$? 按和式的结构识别（分母含 $ k/n$ 的有理式 → $\\dfrac{1}{1+x}$ 或其变体）；端点效应不影响极限。
【易错】和式的下标起点（$k=1$ vs $k=0$）与 $f(0)$ 的取值。
【注意】答案 B。""",
8: """【公式】先展开合并同类项：$ f=2x_1x_2+2x_2x_3+2x_1x_3$（三个平方项全部消掉！）→ 矩阵 $ A=\\begin{pmatrix}0&1&1\\\\1&0&1\\\\1&1&0\\end{pmatrix}$。
【技巧】$ A$ 特征值 $2,-1,-1$（各行和 2 → $(1,1,1)$ 特征向量；迹 0 → 另两根和 $-2$）→ 正惯性 1、负惯性 2。
【易错】"平方项全消"意味着标准形是 $ 2y_1^{2}-y_2^{2}-y_3^{2}$（不能配成三个平方）。
【注意】答案 B（正 1、负 2）。""",
9: """【公式】$ A=BC$（$ C$ 为过渡阵）⟺ $ r(A)=r(B)$（$ B$ 可逆时双向）。
【技巧】$\\alpha$ 组可由 $\\beta$ 组表示且 $\\beta$ 组可由 $\\alpha$ 组表示 ⟺ 秩相等 → 存在可逆 $C$ 使 $ A=BC$（$r(A)=r(B)=3$ 时 $C=A B^{-1}$? 反向也行）。
【易错】$r(A)=r(B)=3$（3 维满秩）→ 两向量组都线性无关、都等价 → $C$ 可逆。
【注意】答案 D。""",
10: """【公式】下三角可逆 $P$ 左乘 = 行变换（只用"下三角行的倍加"）；上三角 $Q$ 右乘 = 列变换（上三角型倍加）→ $ PAQ$ 化对角 = 高斯消元不用交换行。
【技巧】消元顺序：$ a_{21}$ 用 $ a_{11}$ 消（行 2 减 2×行 1）、$ a_{31}$ 用行 1 消——但 $ a_{21}=2\\ne0$ 且主对角全可作主元（$1,1,-5$? 核对消元过程是否需要行交换）。
【易错】消元中途出现 0 主元 → 需行交换 → 下三角 $P$ 做不到 → 选项排除的关键。
【注意】答案 C（消元可行且 $P,Q$ 保持三角）。""",
11: """【公式】$\\displaystyle\\int_0^{+\\infty}\\mathrm e^{-ax^{2}}\\,\\mathrm dx=\\dfrac12\\sqrt{\\dfrac{\\pi}{a}}$（高斯积分）；$ 3^{-x^{2}}=\\mathrm e^{-x^{2}\\ln3}$ → $ a=\\ln3$。
【技巧】偶函数对称加倍：$\\int_{-\\infty}^{+\\infty}|x|\\mathrm e^{-x^{2}\\ln3}\\,\\mathrm dx=2\\displaystyle\\int_0^{+\\infty}x\\mathrm e^{-(\\ln3)x^{2}}\\,\\mathrm dx$，凑 $\\mathrm d(x^{2})$：$ =\\dfrac{1}{\\ln3}$。
【易错】$ 3^{-x^{2}}=\\mathrm e^{-(\\ln3)x^{2}}$（底换指数）；$|x|$ 奇偶加倍。
【注意】答案 $\\dfrac{1}{\\ln3}$。""",
12: """【公式】参数二阶导：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{4t\\mathrm e^{t}}{2\\mathrm e^{t}+1}$，$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{\\left(\\dfrac{\\mathrm dy}{\\mathrm dx}\\right)'_t}{2\\mathrm e^{t}+1}$。
【技巧】$\\dfrac{\\mathrm dy}{\\mathrm dt}=4\\mathrm e^{t}+4(t-1)\\mathrm e^{t}+2t=4t\\mathrm e^{t}+2t$——代 $t=0$：$ \\dfrac{\\mathrm dy}{\\mathrm dx}=0$、$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{?}{2}$。
【易错】$(t-1)\\mathrm e^{t}$ 乘积求导出 $ \\mathrm e^{t}+(t-1)\\mathrm e^{t}=t\\mathrm e^{t}$。
【注意】答案 $\\dfrac23$。""",
13: """【公式】隐函数在 $(0,2)$：$ z+2\\ln z=1$ → $ z=1$；$ z_x=-\\dfrac{F_x}{F_z}$，$ F_x=z-\\dfrac{2y}{1+4x^{2}y^{2}}$。
【技巧】代点：$ F_x=1-\\dfrac{4}{1+4\\cdot4}=1-\\dfrac{4}{17}$? 按 $\\arctan(2xy)$ 求导 $\\dfrac{2y}{1+4x^{2}y^{2}}$，$(0,2)$ 处 $=2$ → $ F_x=1-2=-1$。
【易错】$ F_z=\\dfrac{1}{z}+\\dfrac{2y}{1+4x^{2}y^{2}}=1+2=3$；$(y\\ln z)'_y=\\ln z$。
【注意】$ z_x(0,2)=\\dfrac13$。""",
14: """【公式】先交换内层次序：$\\displaystyle\\int_1^{t^{2}}\\mathrm dx\\int_{\\sqrt{x}}^{t}\\sin\\dfrac xy\\,\\mathrm dy$ 的区域由 $ x\\in[1,t^{2}],\\ \\sqrt x\\le y\\le t$ 确定 → 换成 $ y\\in[1,t],\\ y^{2}\\le x\\le t^{2}$。
【技巧】内层 $\\displaystyle\\int_{y^{2}}^{t^{2}}\\sin\\dfrac xy\\,\\mathrm dx=\\left[-y\\cos\\dfrac xy\\right]=y\\left(\\cos y-\\cos t\\right)$? （$\\sin(x/y)$ 对 $x$ 积分出 $-y\\cos(x/y)$）→ 再对 $y$ 积分。
【易错】交换后限的对应（$ y$ 从 1 到 $ t$，$t>1$）；$\\sin\\dfrac xy$ 对 $x$ 积分的原函数 $-y\\cos\\dfrac xy$。
【注意】$ f'(t)=\\dfrac{\\pi}{2}\\cos\\dfrac{2}{\\pi}$（变限求导后的结果，按数据解析）。""",
15: """【公式】三阶特征方程 $ \\lambda^{3}-1=0$ → 根 $ 1,\\ -\\tfrac12\\pm\\dfrac{\\sqrt3}{2}\\mathrm i$。
【技巧】实根给 $ \\mathrm e^{x}$；共轭复根 $ \\alpha\\pm\\beta\\mathrm i$ 给 $ \\mathrm e^{\\alpha x}(C\\cos\\beta x+C\\sin\\beta x)$，$ \\alpha=-\\tfrac12,\\ \\beta=\\tfrac{\\sqrt3}2$。
【易错】$ \\lambda^{3}-1=(\\lambda-1)(\\lambda^{2}+\\lambda+1)$ 的二次因式；复根的实部为 $-\\tfrac12$。
【注意】通解 $ y=C_1\\mathrm e^{x}+\\mathrm e^{-x/2}\\left(C_2\\cos\\dfrac{\\sqrt3}{2}x+C_3\\sin\\dfrac{\\sqrt3}{2}x\\right)$。""",
16: """【公式】四阶行列式中 $ x$ 的最高次：$ x^{4}$（主对角全 $ x$）与 $ x^{3}$ 的来源——按列展开或选非零元素乘积。
【技巧】$ x^{3}$ 项由"三个 $ x$ + 一个常数"的排列贡献：枚举反对称排列的符号（$-4x^{3}$ 与 $-x^{3}$ 两类）。
【易错】排列 $\\sigma$ 的逆序数符号；漏掉"对角全 x"之外的三个 x 组合。
【注意】$ x^{3}$ 系数 $=-5$。""",
17: """【公式】$ \\dfrac{\\int_0^x \\mathrm e^{t^{2}}\\,\\mathrm dt}{\\mathrm e^{x}-1}\\to1$（洛必达一次：$\\dfrac{\\mathrm e^{x^{2}}}{\\mathrm e^{x}}\\to1$）。
【技巧】整体差式通分后洛必达到二阶：分子 $ \\mathrm e^{x^{2}}(1?)\\cdots$；或 $ \\mathrm e^{x}-1-x\\sim\\tfrac{x^{2}}{2}$ 与 $ \\int_0^x\\mathrm e^{t^{2}}-x\\sim\\tfrac{x^{3}}{3}?$ 阶数配平。
【易错】两次洛必达的条件验证；$\\int_0^x(\\mathrm e^{t^{2}}-1)\\,\\mathrm dt\\sim\\dfrac{x^{3}}{3}$。
【注意】答案 $\\dfrac12$。""",
18: """【公式】$f(x)=\\dfrac{x|x|}{1+x}$：$x\\ge0$ 时 $ \\dfrac{x^{2}}{1+x}$、$ x<0$ 时 $ \\dfrac{-x^{2}}{1+x}$。
【技巧】$ f''=\\dfrac{2}{(1+x)^{3}}$（两段统一）恒正 → 全域凹向上？——但 $ x=-1$ 是无穷间断，左右两支分开看：各支内 $f''>0$（凹）；凸区间按数据给的口径（$(-1,0)$ 凸? 以解析符号计算为准——$ x<0$ 段 $f''=\\dfrac{2}{(1+x)^{3}}>0$ 若 $ x>-1$）。
【易错】$ x<-1$ 与 $ -1<x<0$ 的分母符号变化（$(1+x)^{3}$ 变号！）→ $ f''$ 在 $x<-1$ 时为**负**（凸）、$-1<x$ 时为正（凹）。
【注意】凹 $(-1,0),(0,\\infty)$? 按数据解析：凹 $(-\\infty,-1),(0,+\\infty)$、凸 $(-1,0)$（以 $f''$ 符号为准核对）。""",
19: """【公式】两次求导还原：$ \\dfrac{f(x)}{\\sqrt x}=\\dfrac13x^{2}-x+? +C$? ——$ \\left(\\dfrac{x^{2}}{6}-\\dfrac{x^{2}}{2}\\right)$? 逐次：先乘 $ \\sqrt x$ 再求导读 $ f(x)=\\sqrt x\\left(\\dfrac{x^{2}}{3}-x+C\\right)$? 按数据解析路径。
【技巧】弧长 $s=\\displaystyle\\int_0^{?}\\sqrt{1+f'^{2}}\\,\\mathrm dx$；$ f'(x)=\\dfrac{?}{2\\sqrt x}$ 的平方恰好配成完全平方 → 弧长被积函数线性化。
【易错】常数 $C$ 由 $ f(0)=?$（原方程代 $x=0$）定；完全平方式的识别。
【注意】$ s=\\dfrac{22}{3}$、$ A=\\dfrac{425\\pi}{9}$（旋转体，按数据解析）。""",
20: """【公式】一阶线性 $ y'-\\dfrac6x y=-\\dfrac6x$，积分因子 $ x^{-6}$：$ \\left(yx^{-6}\\right)'=-6x^{-7}$ → $ y=1+Cx^{6}$。
【技巧】(2) $ I_y=\\pi\\displaystyle\\int_0^{x?}y^{4}\\cdots$? 按题给旋转轴：$ y^{2}$ 作为半径 → $ I_y=\\dfrac{\\pi}{2}\\displaystyle\\int y^{4}\\,\\mathrm dx$? 对 $P(x, y)$ 使 $ I_y$ 最小 → $ y=1+\\dfrac{x^{6}}{3}$ 代入求驻点 $ x=1$。
【易错】$ y(\\sqrt3)=10$ 定 $ C=9$（$ 9\\cdot27=243,\\ 243/3=81+1=82?$ 按数据核 $C$）。
【注意】$ y=1+\\dfrac{x^{6}}{3}$；$ P=\\left(1,\\dfrac43\\right)$（最小 $ I_y=\\dfrac{64\\pi}{81}\\cdot?$ 按数据）。""",
21: """【公式】双纽线：$ (x^{2}+y^{2})^{2}=x^{2}-y^{2}$ 极坐标 $ r^{2}=\\cos2\\theta$；第一象限 $ \\theta\\in[0,\\tfrac\\pi4]$。
【技巧】$\\displaystyle\\iint x\\,\\mathrm d\\sigma=\\int_0^{\\pi/4}\\mathrm d\\theta\\int_0^{\\sqrt{\\cos2\\theta}}r^{2}\\cos\\theta\\,\\mathrm dr=\\dfrac13\\int_0^{\\pi/4}\\cos^{?}\\theta\\cdots=\\dfrac13\\int\\cos^{5/2}2\\theta\\cos\\theta$? 规范路径：$ \\displaystyle\\int\\cos^{3/2}2\\theta\\cos\\theta\\,\\mathrm d\\theta$ 按数据解析（可能用 $\\cos2\\theta=2\\cos^{2}\\theta-1$ 与对称化简）。
【易错】$ r^{2}=\\cos2\\theta$ 的开方（第一象限取正）；被积 $ x=r\\cos\\theta$ 乘雅可比 $r$ → $ r^{2}\\cos\\theta$。
【注意】答案 $\\dfrac{1}{48}$。""",
22: """【公式】仅有两个不同特征值 ⟺ 特征多项式的根分布为"一单根 + 一二重根"；$|\\lambda E-A|=(\\lambda-(2-b?))\\cdots$ 按第一行展开。
【技巧】$ \\alpha=(1,1,1)?$? 是特征向量? 由 $ A\\alpha=\\lambda\\alpha$ 逐分量读方程 → 解 $(a,b)$ 组合（数据给出 $(1,1)$ 与 $(-1,3)$ 两组）。
【易错】"仅有两个不同特征值"还要求二重根处可对角化与否的隐含讨论（本题只问参数值）。
【注意】$(a,b)=(1,1)$ 或 $(-1,3)$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2021数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2021数二真题.md', TIPS_2021)
