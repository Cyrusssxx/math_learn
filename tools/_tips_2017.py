# -*- coding: utf-8 -*-
# 2017 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2017 = {
1: """【公式】等价无穷小分阶：$1-\\cos\\sqrt{x}\\sim\\dfrac{x}{2}$ → 右极限 $=\\dfrac1a$。
【技巧】可导必先连续——两步筛：连续定 $b=\\dfrac1a$；可导要求左导（常数段）$=0=$ 右导 → 无解 → 只有"连续不可导"分支。
【易错】左导数（$x\\le0$ 常数 $b$）恒为 0；右极限 $\\dfrac1a$ 若非 0 则不可导。
【注意】答案 A。""",
2: """【公式】凸函数（$f''>0$）在 $[-1,1]$ 上：曲线位于两端连线 $y=1$ 的下方；$f'(x)$ 严格递增 → $f'(-1)<f'(0)<f'(1)$。
【技巧】$f(0)=-1$ 与 $f(\\pm1)=1$ 的落差判 $f'(0)$ 型选项（凸函数的导数序关系）。
【易错】"凹的图像位于两端连线下方"的方向别反；$f'(0)$ 与端点导数的大小序。
【注意】答案 B。""",
3: """【公式】数列收敛 + $f$ 连续 → $f(x_n)$ 收敛；$\\sin x_n$ 之类复合需 $f$ 连续才行——本题只设"数列收敛"本身。
【技巧】反例定位：$x_n=2n\\pi$ 收敛但 $\\sin x_n\\equiv0$；逐选项配反例。
【易错】$\\sin x_n$、$[x_n]$、$x_n+\\tfrac1n$ 各自需要不同的反例结构。
【注意】答案 D（反例组合）。""",
4: """【公式】特征根 $2\\pm2\\mathrm i$；右端 $\\mathrm e^{2x}$（$\\lambda=2$ 非根 → $y_1^{*}=a\\mathrm e^{2x}$）与 $\\mathrm e^{2x}\\cos2x$（$2+2\\mathrm i$ 是根 → 乘 $x$：$y_2^{*}=x\\mathrm e^{2x}(a\\cos2x+b\\sin2x)$）。
【技巧】叠加原理两项分别设；共振判断逐项独立（$\\lambda=2$ 与 $2\\pm2\\mathrm i$ 是不同的 $\\lambda$）。
【易错】复根共振的 $x$ 因子；虚部实部成对。
【注意】答案 C。""",
5: """【公式】偏导符号 = 单调方向（同 2012 Q5 模型）。
【技巧】累次极限链：沿 $x$ 增沿 $y$ 减，四点两路径夹出定序——$f(x_1,y_1)$ 与 $f(x_2,y_2)$ 的大小不可定（两变量同向变化无序），但交叉组合可定。
【易错】别用中值定理过度推断；偏导正只给各变量严格单调。
【注意】答案 D（与 2012 Q5 同型）。""",
6: """【公式】路程 = 速度曲线下面积：乙追上甲 $\\Leftrightarrow\\displaystyle\\int_0^{t_0}(v_2-v_1)\\,\\mathrm dt=10$（弥补 10 米差）。
【技巧】图形面积替代积分值（$v_2-v_1$ 与横轴围的面积从图上读）；$t_0$ 是速度曲线首次达到"面积=10"的时刻。
【易错】10 米是初始领先量（甲在前）——方程 $S_1-S_2=10$ 的符号方向；速度曲线交点前后的正负抵消。
【注意】答案 C（按数据选项）。""",
7: """【公式】$A\\alpha_i=\\lambda_i\\alpha_i$（$\\lambda=0,1,2$ 对应 $\\alpha_1,\\alpha_2,\\alpha_3$）→ $A(\\alpha_1+\\alpha_2+\\alpha_3)=\\alpha_2+2\\alpha_3$。
【技巧】组合向量的像逐项作用后再合并（$0\\cdot\\alpha_1+1\\cdot\\alpha_2+2\\cdot\\alpha_3$）。
【易错】二次型 $x^{\\mathrm T}A x$ 在 $(1,1,1)$ 的值 = $\\alpha_i$ 的像加权内积。
【注意】答案 B。""",
8: """【公式】上三角阵特征值 = 对角元：$A,B,C$ 特征值同为 $1,2,2$；可对角化 $\\Leftrightarrow r(2E-A)=3-2=1$。
【技巧】$r(2E-A)$ 逐个算：$A$ 的 $2E-A$ 秩 2 → 不可对角化；$B$ 的秩 1 → 可对角化（$C$ 是对角阵本身）。
【易错】"相似于对角阵 C"逐个验证秩条件，不是上三角就自动可对角化。
【注意】答案 B（仅 $B$ 可相似于 $C$）。""",
9: """【公式】斜渐近线：$k=\\lim\\left(1+\\arcsin\\dfrac2x\\right)=1$，$b=\\lim x\\arcsin\\dfrac2x=\\lim x\\cdot\\dfrac2x=2$。
【技巧】$\\arcsin\\dfrac2x\\sim\\dfrac2x$（$x\\to\\infty$）——等价代换读 $b$。
【易错】$\\arcsin$ 的等价（主值分支奇函数）；$x\\to\\pm\\infty$ 两侧同为 2。
【注意】$y=x+2$。""",
10: """【公式】参数二阶导：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{\\cos t}{1+\\mathrm e^{t}}$；$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{\\left(\\dfrac{\\cos t}{1+\\mathrm e^{t}}\\right)_t'}{1+\\mathrm e^{t}}$。
【技巧】分子在 $t=0$：$\\dfrac{-\\sin0(1+1)-1\\cdot\\cos0}{(1+1)^{2}}=-\\dfrac12$ → 二阶 $=-\\dfrac{1/2}{2}=-\\dfrac18$。
【易错】二阶导分母合并为 $(1+\\mathrm e^{t})^{3}$，代 $t=0$ 后是 $8$ 而非 $4$——合并前后要一致。
【注意】答案 $-\\dfrac18$。""",
11: """【公式】分部 + 收敛端：$\\displaystyle\\int_1^{+\\infty}\\dfrac{\\ln u}{u^{2}}\\,\\mathrm du=\\left[-\\dfrac{\\ln u}{u}\\right]_1^{+\\infty}+\\int_1^{+\\infty}\\dfrac{\\mathrm du}{u^{2}}=0+1=1$。
【技巧】换元 $u=1+x$ 统一；$\\dfrac{\\ln u}{u}\\to0$（$u\\to\\infty$，指数压对数）。
【易错】$\\ln u$ 在 $u=1$ 处为 0；分部的 $v=-\\dfrac1u$。
【注意】答案 1。""",
12: """【公式】全微分还原：$f_x=y\\mathrm e^{y}$（对 $x$ 是常数）→ $f=xy\\mathrm e^{y}+\\varphi(y)$。
【技巧】$f_y=x\\mathrm e^{y}(y+1)+\\varphi'(y)$ 与题给 $x(1+y)\\mathrm e^{y}$ 对照 → $\\varphi'=0$ → 常数；$f(0,0)=0$ 定为 0。
【易错】对 $x$ 积分的"常数"是 $y$ 的函数 $\\varphi(y)$；$y\\mathrm e^{y}$ 对 $x$ 求导为 0。
【注意】$f=xy\\mathrm e^{y}$。""",
13: """【公式】交换次序：内层 $\\displaystyle\\int_y^{1}\\dfrac{\\tan x}{x}\\,\\mathrm dx$ 积不出 → 换次序后 $\\int_0^{1}\\dfrac{\\tan x}{x}\\cdot x\\,\\mathrm dx=\\int_0^{1}\\tan x\\,\\mathrm dx$。
【技巧】"内层积不出原函数"是换序的信号；换后内层 $\\int_0^x\\mathrm dy=x$ 消掉分母。
【易错】$\\int_0^1\\tan x\\,\\mathrm dx=-\\left[\\ln|\\cos x|\\right]_0^1=\\ln\\dfrac{1}{\\cos1}$。
【注意】答案 $-\\ln\\cos1$。""",
14: """【公式】特征向量条件：$A(1,1,2)^{\\mathrm T}=\\lambda(1,1,2)^{\\mathrm T}$ → 三分量方程解 $a,\\lambda$。
【技巧】分量：$4+1-4=\\lambda$ → $\\lambda=1$；$1+2+2a=1\\Rightarrow a=-1$；第三分量 $3+1-2=2=\\lambda\\cdot2$ ✓ 自洽校验。
【易错】第三个方程是校验不是多余；特征值由任一分量读。
【注意】$a=-1$。""",
15: """【公式】换元消根号：$u=x-t$ → $\\displaystyle\\int_0^x \\mathrm e^{t}\\sqrt{x-t}\\,\\mathrm dt=\\int_0^{x}\\mathrm e^{x-u}\\sqrt{u}\\,\\mathrm du=\\mathrm e^{x}\\int_0^{x}\\mathrm e^{-u}\\sqrt u\\,\\mathrm du$。
【技巧】分母 $\\sqrt{\\sin x}\\sim\\sqrt x$：分子主项 $\\displaystyle\\int_0^{x}\\sqrt u\\,\\mathrm du=\\dfrac23x^{3/2}$（$\\mathrm e^{x}\\to1$）→ 极限 $\\dfrac{\\tfrac23x^{3/2}}{\\sqrt{x}}\\to\\dfrac23$。
【易错】$\\sqrt{\\sin x}\\sim\\sqrt x$（$x\\to0^{+}$）；$\\mathrm e^{x}\\to1$。
【注意】答案 $\\dfrac23$。""",
16: """【公式】全参数链式：$y=f(\\mathrm e^{x},\\cos x)$ → $y'=\\mathrm e^{x}f_1'-\\sin x\\, f_2'$；$y''=\\mathrm e^{2x}f_{11}''-2\\mathrm e^{x}\\sin x\\, f_{12}''+\\sin^{2}x\\, f_{22}''-\\mathrm e^{x}f_1'-\\cos x\\, f_2'$。
【技巧】$x=0$ 代入：$\\mathrm e^{0}=\\cos0=1$ → $y'(0)=f_1'(1,1)$；二阶交叉项 $-2\\sin0=0$ 消失、$\\sin^{2}0=0$ → $y''(0)=f_{11}''(1,1)+f_{22}''(1,1)-f_1'(1,1)-f_2'(1,1)$。
【易错】乘积法则（$\\mathrm e^{x}f_1'$ 求导出两项）；$(-\\sin x)^{2}=\\sin^{2}x$。
【注意】$y'(0)=f_1'(1,1)$；$y''(0)=f_{11}''(1,1)+f_{22}''(1,1)-f_1'(1,1)-f_2'(1,1)$。""",
17: """【公式】黎曼和：$\\displaystyle\\sum\\frac{k}{n^{2}}\\ln\\left(1+\\frac{k}{n}\\right)=\\frac1n\\sum\\frac kn\\ln\\left(1+\\frac kn\\right)\\to\\int_0^{1}x\\ln(1+x)\\,\\mathrm dx$。
【技巧】分部：$\\int x\\ln(1+x)\\,\\mathrm dx=\\dfrac12\\left[(x^{2}-1)\\ln(1+x)\\right]-\\dfrac14x^{2}+\\dfrac12x$（取 $x^{2}-1$ 让边界项在 $x=1$ 处为零）。
【易错】$\\dfrac kn\\to x$ 的配平（$\\dfrac{k}{n^{2}}=\\dfrac1n\\cdot\\dfrac kn$）；分部取 $(x^{2}-1)$ 因子而非 $x^{2}$ 可直接消边界项。
【注意】$\\displaystyle\\int_0^{1}x\\ln(1+x)\\,\\mathrm dx=\\dfrac12\\ln2-\\dfrac12\\left(\\ln2-\\dfrac12\\right)=\\dfrac14$。""",
18: """【公式】隐函数极值：$3x^{2}+3y^{2}y'-3+3y'=0$ → $y'=\\dfrac{1-x^{2}}{1+y^{2}}$，驻点 $x=\\pm1$。
【技巧】$x=1$：曲线方程 $1+y^{3}-3+3y-2=0$ → $y=1$ ✓（极大）；$x=-1$：$-1+y^{3}+3+3y-2=0$ → $y=0$（极小）。
【易错】驻点 $x=\\pm1$ 对应的 $y$ 值由隐式方程分别解；极大/极小由 $y'$ 两侧符号或二阶导判。
【注意】极小 $y(-1)=0$、极大 $y(1)=1$。""",
19: """【公式】(I) $\\lim\\limits_{x\\to0^{+}}\\dfrac{f(x)}{x}=1$ 且分母 $\\to0^{+}$ → $f(x)\\sim x>0$（$x\\to0^{+}$）；且 $f(0)=0$（极限存在 = 分子趋零）。
【技巧】(II) 拐点 = $f''$ 变号：构造 $\\varphi(x)=f(x)-x$：$\\varphi(0)=0$、$\\varphi(1)=f(1)-1>0$、$\\varphi'(0)=0$ → $\\varphi$ 内部有正极值点 → $f'-1$ 变号 → $f''$ 变号。
【易错】$\\varphi$ 的三零点（$0,\\xi_0,1$）→ $\\varphi'$ 两零点 → $\\varphi''$ 零点——两级罗尔链。
【注意】(II) 存在 $\\eta\\in(0,1)$ 使 $f''(\\eta)=0$（按解析）。""",
20: """【公式】极坐标：$D$ 圆 $r=2\\sin\\theta$（$0\\le\\theta\\le\\pi$）；分母 $x+1=1+r\\cos\\theta$。
【技巧】$\\displaystyle\\int_0^{\\pi}\\mathrm d\\theta\\int_0^{2\\sin\\theta}\\dfrac{r\\sin\\theta}{1+r\\cos\\theta}r\\,\\mathrm dr$——先 $r$ 积分（分母线性 → 对数原函数）。
【易错】内层 $\\displaystyle\\int\\dfrac{r^{2}\\sin\\theta}{1+r\\cos\\theta}\\,\\mathrm dr$ 拆项按数据解析路径。
【注意】答案 $\\dfrac{5\\pi}{4}$。""",
21: """【公式】切线斜率 = $-\\dfrac xy$（从数据解析读：切线与两轴交点中点条件）→ $y\\,\\mathrm dy=-x\\,\\mathrm dx$ → $x^{2}+y^{2}=C$。
【技巧】"线段被某轴平分/切线过定点" → 中点或定点条件 → 微分方程；初值 $y(1)=0$ 定 $C=1$。
【易错】斜率表达式由题设几何条件翻译；$\\arctan\\dfrac yx$ 的微分 $=\\dfrac{x\\,\\mathrm dy-y\\,\\mathrm dx}{x^{2}+y^{2}}$。
【注意】解 $\\arctan\\dfrac yx+\\dfrac12\\ln(x^{2}+y^{2})=0$（对数与反正切的组合原函数）。""",
22: """【公式】(I) $\\alpha_3=\\alpha_1+2\\alpha_2$ → $r(A)=2$（$\\alpha_1,\\alpha_2$ 无关 + 第三列表示）→ $\\det A=0$；$\\beta=\\alpha_1+\\alpha_2+\\alpha_3=2\\alpha_1+3\\alpha_2$ → $Ax=\\beta$ 有解。
【技巧】(II) $Ax=\\beta$ 的特解读表示系数：$\\beta=2\\alpha_1+3\\alpha_2+0\\cdot\\alpha_3$ → $x_0=(2,3,0)^{\\mathrm T}$；基础解系由 $Ax=0$（$\\alpha_1+2\\alpha_2-\\alpha_3=0$ 从列关系读）得 $(1,2,-1)^{\\mathrm T}$。
【易错】特解系数直接来自 $\\beta$ 的表示（不用解方程组）；基础解系从列关系读系数。
【注意】通解 $x=(1,1,1)^{\\mathrm T}+k(1,2,-1)^{\\mathrm T}$（数据解析形式；特解不同形式等价）。""",
23: """【公式】(I) 从数据答案 $\\alpha=2$ 与 $Q$ 列读：标准形含 $2y_1^{2}$ → 特征值由秩与迹定。
【技巧】条件"$f$ 在某方向恒 0"翻译成 $\\lambda=0$ 特征向量 → 特征多项式解 $\\alpha$；$Q$ 列 = 单位正交特征向量。
【易错】正交变换保持 $\\lambda$ 集合；$\\alpha$ 由特征多项式的重根条件定（数据 $\\alpha=2$）。
【注意】$\\alpha=2$；$Q=\\begin{pmatrix}\\frac1{\\sqrt3}&-\\frac1{\\sqrt2}&\\frac1{\\sqrt6}\\\\\\cdots\\end{pmatrix}$（按数据解析）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2017数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2017数二真题.md', TIPS_2017)
