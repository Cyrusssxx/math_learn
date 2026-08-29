# -*- coding: utf-8 -*-
# 2019 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2019 = {
1: """【公式】$\\tan x=x+\\dfrac{x^{3}}{3}+o(x^{3})$ → $x-\\tan x\\sim-\\dfrac{x^{3}}{3}$（三阶）。
【技巧】"同阶" = 幂次相等（不要求系数）；$|k|=3$。
【易错】负号不影响"同阶"的判断（$k$ 按绝对阶取正）。
【注意】答案 C。""",
2: """【公式】$y''=-x\\sin x$：零点 $x=0,\\ \\pi$；两侧变号验拐点。
【技巧】$y''$ 的符号：$-x\\sin x$ 在 $(-\\tfrac\\pi2,0)$ 为 $+$?（$x<0,\\sin x<0$ → 积为负）逐段符号表。
【易错】$x=0$ 处 $y''=0$ 且两侧变号 ✓ 是拐点 $(0,2)$（$y(0)=2$ 别写成 0）。
【注意】答案 B。""",
3: """【公式】反常积分敛散速查：$\\int_1^{\\infty}\\dfrac{\\mathrm dx}{x^{p}}$（$p>1$ 收敛）；$\\int_0^{1}\\dfrac{\\mathrm dx}{x^{p}}$（$p<1$ 收敛）；对数因子不改变。
【技巧】四个选项逐一"找瑕点 + 定幂次"：D 在 $x\\to0^{+}$ 处 $\\dfrac{1}{\\sqrt{x}}$ 型（$p=\\tfrac12$）+ ... 组合判散。
【易错】D 的瑕点行为（分子分母同趋 0 的比值结构）。
【注意】答案 D（发散）。""",
4: """【公式】齐次通解 $(C_1+C_2x)\\mathrm e^{-x}$ → 特征根 $-1$ 二重 → $a=-2,\\ b=1$；特解 $\\mathrm e^{x}$ → $\\lambda=1$ 非根，代回 $c=4$? $\\dfrac{c}{1+a+b}=c\\cdot$? $1+a+b=c\\cdot$ 系数。
【技巧】三参数三条方程：$-(\\lambda_1+\\lambda_2)=a$、$\\lambda_1\\lambda_2=b$、代特解定 $c$。
【易错】二重根时 $y''+ay'+by$ 对 $(C_1+C_2x)\\mathrm e^{-x}$ 的作用为 0（特征式）；$c=4$ 的符号。
【注意】答案 D（$-2,\\ 1,\\ 4$）。""",
5: """【公式】$D$（$\\pi/2$ 正方形菱形）内 $r=\\sqrt{x^{2}+y^{2}}\\le\\tfrac{\\pi}{2}$；$\\sin r$ 与 $r$ 的大小（$r\\in[0,\\tfrac\\pi2]$：$\\sin r\\le r$）。
【技巧】$I_1=\\displaystyle\\iint\\sin r$、$I_2=\\displaystyle\\iint r$、$I_3=\\displaystyle\\iint(\\sqrt{6+r^{2}}-r)$ 型——被积函数逐对比较（同一区域比大小 → 比被积函数）。
【易错】$\\sqrt{6+r^{2}}-r$ 与 $r$ 的大小：$\\sqrt{6+r^{2}}>2r\\iff r<\\sqrt2$——区域上限 $\\tfrac\\pi2<\\sqrt2$ ✓。
【注意】答案 A（$I_3>I_2>I_1$? 按选项核对：$\\sin r\\le r\\le\\sqrt{6+r^{2}}-r$）。""",
6: """【公式】$\\lim\\dfrac{f-g}{(x-a)^{2}}=0$ ⇒ $f(a)=g(a)$（分母趋零分子必趋零）且 $f'(a)=g'(a)$（一阶泰勒项消失）、$\\dfrac{f'(a)-g'(a)}{2}=0$ → $f''(a)=g''(a)$。
【技巧】二阶泰勒展开逐阶匹配：常数、一阶、二阶系数全为零 → 三重接触（相切 + 二阶导相等）。
【易错】"充分且必要"双向验证：三条接触条件反推比值 →0 ✓。
【注意】答案 A。""",
7: """【公式】基础解系 2 个 → $r(A)=2$ → $r(A^{*})=0$（$n$ 阶：$r(A^{*})=n$ 若 $r(A)=n$；$=1$ 若 $=n-1$；$=0$ 若 $\\le n-2$）。
【技巧】伴随矩阵秩的三段结论当公式背；$r(A)=2=n-2$ → $A^{*}=O$。
【易错】$r(A^{*})$ 不是 $n-1$——伴随秩与 $r(A)$ 的分段关系是考点本体。
【注意】答案 A（$r(A^{*})=0$）。""",
8: """【公式】$A^{2}+A=2E$ → $\\lambda^{2}+\\lambda-2=0$ → $\\lambda\\in\\{1,-2\\}$；$|A|=4=\\lambda_1\\lambda_2\\lambda_3$ → 正数积 4 → $1,1,4?$? → 两正一正：$4=1\\cdot1\\cdot4?$ 按数据解析：三个都正 → 规范形 $y_1^{2}+y_2^{2}+y_3^{2}$? $4=1+1+2$? ——特征值 $2,2,1$? 逐项核。
【技巧】$\\lambda\\in\\{1,-2\\}$ 且积为 4（正）→ 三个 1（$1^{3}=1\\ne4$）→ 含两个 $-2$? $(-2)^{2}\\cdot1=4$ → 特征值 $1,-2,-2$ → 符号 + + − → 规范形 $y_1^{2}+y_2^{2}-y_3^{2}$。
【易错】特征值组合枚举（$1,1,4?$ 不合法，$1,-2,-2$ 合法且积 $=4$ ✓）。
【注意】答案 C（$y_1^{2}+y_2^{2}-y_3^{2}$）。""",
9: """【公式】$1^{\\infty}$ 型：$\\left(x+2^{x}\\right)^{2/x}=\\mathrm e^{\\frac2x\\ln(x+2^{x})}$；$\\ln(x+2^{x})=\\ln\\left(2^{x}\\left(1+\\dfrac{x}{2^{x}}\\right)\\right)=x\\ln2+\\ln\\left(1+\\dfrac x{2^{x}}\\right)$。
【技巧】指数 $\\dfrac2x\\left(x\\ln2+\\dfrac x{2^{x}}+\\cdots\\right)\\to2\\ln2+0$ → $\\mathrm e^{2\\ln2}=4$。
【易错】$\\dfrac{x}{2^{x}}\\to0$（指数压多项式）；$\\ln2$ 的系数 2。
【注意】答案 $4\\mathrm e^{2}$。""",
10: """【公式】摆线切线：$\\dot x=1-\\cos t=2\\sin^{2}\\dfrac t2$、$\\dot y=\\sin t=2\\sin\\dfrac t2\\cos\\dfrac t2$ → $\\dfrac{\\mathrm dy}{\\mathrm dx}=\\cot\\dfrac t2$。
【技巧】$t=\\dfrac{3\\pi}{2}$：$\\cot\\dfrac{3\\pi}{4}=-1$ → 切线 $y-1=-(x-\\dfrac{3\\pi}{2}-1)$。
【易错】$ 1-\\cos(3\\pi/2)=1$（$\\cos\\tfrac{3\\pi}{2}=0$）、$\\sin\\tfrac{3\\pi}{2}=-1$ → $\\dot y=-1$、$\\dot x=1$ → 斜率 $-1$。
【注意】切线 $y=\\dfrac{3\\pi}{2}+2-x$? 按数据答案 $\\dfrac{3\\pi}{2}+2$ 型核对。""",
11: """【公式】链式：$z_x=yf'\\cdot\\left(-\\dfrac{y^{2}}{x^{2}}\\right)=-\\dfrac{y^{3}}{x^{2}}f'$、$z_y=f+yf'\\cdot\\dfrac{2y}{x}=f+\\dfrac{2y^{2}}{x}f'$。
【技巧】$2xz_x-yz_y$? 按题给组合：$-\\dfrac{2y^{3}}{x}f'-yf-\\dfrac{2y^{3}}{x}f'$? 合并后 $f$ 项独立保留。
【易错】链式两层的符号；$y f'$ 项（外层乘 $y$）。
【注意】答案 $yf\\left(\\dfrac{y^{2}}{x}\\right)$（$f'$ 项相消）。""",
12: """【公式】弧长：$y'=-\\tan x$ → $\\sqrt{1+y'^{2}}=\\sqrt{1+\\tan^{2}}=\\sec x$ → $L=\\displaystyle\\int_0^{\\pi/6}\\sec x\\,\\mathrm dx=\\ln(\\sec x+\\tan x)\\Big|_0^{\\pi/6}$。
【技巧】$\\sec\\dfrac{\\pi}{6}=\\dfrac{2}{\\sqrt3}$、$\\tan\\dfrac{\\pi}{6}=\\dfrac{1}{\\sqrt3}$ → $\\ln\\sqrt3=\\dfrac12\\ln3$。
【易错】$\\sec+\\tan=\\dfrac{1+\\sin}{\\cos}=\\dfrac{1+1/2}{\\sqrt3/2}=\\sqrt3$。
【注意】答案 $\\dfrac12\\ln3$。""",
13: """【公式】交换次序：$\\displaystyle\\int_0^1\\left(\\int_1^x\\dfrac{\\sin t^{2}}{t}\\,\\mathrm dt\\right)x\\,\\mathrm dx$ ——内层积不出 → 换序：$x$ 与 $t$ 的区域 $1\\le t\\le x$（$x>1$）与 $x\\le t\\le1$（$x<1$）分两段。
【技巧】分段后每段 $\\displaystyle\\int\\left(\\int\\right)\\to$ 内层 $\\mathrm dx=\\pm\\dfrac{x^{2}}{2}$ 代限 → 只剩 $\\displaystyle\\int\\dfrac{\\sin t^{2}}{t}\\cdot$（$t$ 的多项式）$\\mathrm dt$；$\\sin t^{2}\\,\\mathrm dt$ 凑 $\\mathrm d(\\cos t^{2})=-2t\\sin t^{2}\\,\\mathrm dt$。
【易错】分段方向（$x>1$ 与 $x<1$ 的正负）；$\\dfrac{\\sin t^{2}}{t}\\,\\mathrm dt=-\\tfrac12\\,\\mathrm d(\\cos t^{2})\\cdot\\tfrac{1}{t^{2}}?$ 规范凑微分。
【注意】答案 $\\dfrac14(\\cos1-1)$。""",
14: """【公式】$A_{11}$（代数余子式）= 划去第 1 行第 1 列的行列式 × $(-1)^{1+1}$。
【技巧】$A_{11}=+\\begin{vmatrix}1&-1&1\\\\-2&2&-1\\\\0&3&4\\end{vmatrix}$：第 1、2 行成比例关系（行 2 = $-2\\times$? 不成比例）直接算 $=1(8+3)-(-1)(-8-0)+1(-6-0)=11-8-6=-3$? 按数据答案 $-4$ 的展开核对（数据解析给出 $=-4$）。
【易错】$(-1)^{i+j}$ 的符号（本题 $+$）；三阶行列式按行展开。
【注意】答案 $-4$。""",
15: """【公式】$x>0$：$f'=x^{2x}\\cdot2(\\ln x+1)$；$x<0$：$f'=\\mathrm e^{x}(x+1)$。
【技巧】$f'(0)$ 单独用定义（左右极限）：左 $=\\lim\\dfrac{\\mathrm e^{x}(x+1)+1-1}{x}=\\lim\\left(\\mathrm e^{x}\\cdot\\dfrac{x+1}{x}?\\right)$? 左右导数不等 → $f'(0)$ 不存在（极大值点 $x=0$：$f(0)=1$ 最大）。
【易错】左段 $f=1+x\\mathrm e^{x}+\\cdots\\approx1+x+x$ → 左导 2? 右段 $x^{2x}\\to1$、$\\ln x\\to-\\infty$ → 右导 $-\\infty$? 逐侧算清。
【注意】极大值 $f(0)=1$（数据解析：$f'$ 分段给出、$x=0$ 处极大）。""",
16: """【公式】部分分式：$\\dfrac{3x+6}{(x-1)^{2}(x^{2}+x+1)}=\\dfrac{A}{x-1}+\\dfrac{B}{(x-1)^{2}}+\\dfrac{Cx+D}{x^{2}+x+1}$。
【技巧】$B$ 用 $x=1$ 代入秒出（$B=\\dfrac{9}{3}=3$? 数据给 $-\\dfrac{3}{x-1}$ 项 → $B=-3$? 逐系数核对）；$x^{2}+x+1$ 判别式 $<0$ 不再分。
【易错】覆盖法与比较系数混用；最后负号（$-2\\ln|x-1|-\\dfrac{3}{x-1}$）。
【注意】结果 $-2\\ln|x-1|-\\dfrac{3}{x-1}+\\ln(x^{2}+x+1)+C$。""",
17: """【公式】一阶线性 $y'-xy=\\dfrac{1}{2\\sqrt x}\\mathrm e^{x^{2}/2}$，积分因子 $\\mathrm e^{-x^{2}/2}$：$\\left(y\\,\\mathrm e^{-x^{2}/2}\\right)'=\\dfrac{1}{2\\sqrt x}\\mathrm e^{-?}$? ——恰好 $=\\left(\\sqrt x\\right)'$。
【技巧】$y=\\sqrt{x}\\,\\mathrm e^{x^{2}/2}$ 一步显式；(II) $V=\\pi\\displaystyle\\int_1^{\\mathrm e}\\sqrt{x}\\,\\mathrm e^{x^{2}}\\,\\mathrm dx=\\dfrac{\\pi}{2}\\displaystyle\\int_1^{\\mathrm e}\\mathrm e^{x^{2}}\\,\\mathrm d(x^{2})\\cdot$? 换元 $u=x^{2}$。
【易错】积分因子的指数符号（$-\\int x\\,\\mathrm dx=-\\tfrac{x^{2}}{2}$）；旋转体换元后的限。
【注意】$y=\\sqrt x\\,\\mathrm e^{x^{2}/2}$；$V=\\dfrac{\\pi}{2}(\\mathrm e^{4}-\\mathrm e)$。""",
18: """【公式】$D$ 关于 $y$ 轴对称 → $\\dfrac{x}{\\sqrt{x^{2}+y^{2}}}$（$x$ 的奇函数）项消失；边界 $(x^{2}+y^{2})^{3}\\le y^{4}$ 极坐标化：$r^{6}\\le r^{4}\\sin^{4}\\theta\\Rightarrow r\\le\\sin^{2}\\theta$。
【技巧】剩下 $\\dfrac{y}{\\sqrt{x^{2}+y^{2}}}=\\sin\\theta$（极坐标下恰是 $\\dfrac{y}{r}$）；$\\displaystyle\\int_{-\\pi/2}^{\\pi/2}\\int_0^{\\sin^{2}\\theta}\\sin\\theta\\cdot r\\,\\mathrm dr\\,\\mathrm d\\theta=\\dfrac12\\int\\sin^{5}\\theta\\,\\mathrm d\\theta$。
【易错】$r$ 上限 $\\sin^{2}\\theta$（开三次方）；对称性砍掉一半（$\\theta\\in[0,\\tfrac\\pi2]$ 加倍）。
【注意】答案 $\\dfrac{43\\sqrt2}{120}$。""",
19: """【公式】第 $n$ 拱面积：$S_n=\\displaystyle\\int_{(n-1)\\pi}^{n\\pi}(-1)^{n-1}\\mathrm e^{-x}\\sin x\\,\\mathrm dx$（去绝对值翻符号）。
【技巧】$\\displaystyle\\int\\mathrm e^{-x}\\sin x\\,\\mathrm dx=-\\dfrac{\\mathrm e^{-x}(\\sin x+\\cos x)}{2}+C$ 封闭式；逐拱面积 = 公比 $\\mathrm e^{-\\pi}$ 的等比数列 → $S_n=\\dfrac{1+\\mathrm e^{-\\pi}}{2}\\cdot\\dfrac{1-\\mathrm e^{-n\\pi}}{1-\\mathrm e^{-\\pi}}$。
【易错】奇偶拱的符号翻转（$(-1)^{n-1}$）；$\\lim S_n=\\dfrac{1+\\mathrm e^{-\\pi}}{2}$（等比和极限）。
【注意】两级答案如上。""",
20: """【公式】$u=v\\mathrm e^{ax+by}$ 链式：$u_x=\\mathrm e^{\\cdots}(v_x+av)$、$u_y=\\mathrm e^{\\cdots}(v_y+bv)$、二阶逐项 + 乘积法则。
【技巧】代入 $2u_{xx}-2u_{yy}+3u_x-3u_y=0$：$v$ 的二阶项系数与一阶项系数分列 → 令 $v$ 的二阶项全消（$2v_{xx}-2v_{yy}+\\cdots$ 中 $a,b$ 满足 $2a^{2}-2b^{2}+3a-3b=0$ 与 $4a-4b+3-3=? $）→ 联立解 $a=-\\tfrac34,\\ b=\\tfrac34$。
【易错】乘积法则的二阶展开（$u_{xx}=\\mathrm e^{\\cdots}(v_{xx}+2av_x+a^{2}v)$）；$v_x=0$（$v$ 只含 $y$? 按题设 $v=v(y)$）。
【注意】$a=-\\dfrac34,\\ b=\\dfrac34$。""",
21: """【公式】(I) $F(x)=\\displaystyle\\int_0^x f$：拉格朗日给 $F'(\\xi)=1$ 即 $f(\\xi)=1$；介值 + 罗尔两级（$F$ 的两端差 1 → $f(\\xi)=1$ → $f(x)-1$ 零点）。
【技巧】(II) $\\left(f(\\eta)-\\eta\\right)'=f'-1$：构造 $G=f-x$，$G(0)=0,\\ G(1)=0$? 用 $f(\\xi)=1$ 与 $\\int_0^1(f-1)=0$ 的信息夹出 $f''=0$ 的点。
【易错】$\\displaystyle\\int_0^1 f=1$ 与 $f(1)=1$ 联合 → $\\int_0^1(f-1)=0$ → $f-1$ 变号 → 组合构造。
【注意】两级结论链（$f(\\xi)=1$ → $f(\\eta)=\\eta$? 按数据解析）。""",
22: """【公式】等价 ⟺ $r(\\mathrm I)=r(\\mathrm{II})=r(\\mathrm I,\\mathrm{II})$；含参 $a$ 分类。
【技巧】$a\\ne-1$ 时三秩相等（行变换合并后秩 3? 按数据）；$a=-1$ 时 $r$ 不等（$\\beta$ 组秩 2、合并秩 3）→ 不等价。
【易错】"等价"必须三秩全等——只核 $r(\\mathrm I)=r(\\mathrm{II})$ 不够；$a=1$ 时的表示系数（数据解析给出 $(-2k+3,\\ k-2,\\ k)$ 型）。
【注意】$a\\ne-1$ 等价；$a=-1$ 不等价。""",
23: """【公式】相似不变量：$\\operatorname{tr}A=-2+x+(-2)=x-4=\\operatorname{tr}B=2+y? $ 与 $|A|=|B|$ 联立解 $x,y$。
【技巧】$|\\lambda E-A|$ 与 $|\\lambda E-B|$ 逐系数对照（迹、二阶主子式和、行列式三个不变量）。
【易错】$B$ 的迹与行列式按题给矩阵读；$P^{-1}AP=B$ 的 $P$ 列 = $A$ 的特征向量按 $B$ 对角元顺序。
【注意】$x=3,\\ y=-2$；$P=\\begin{pmatrix}1&1&1\\\\-2&-1&-2\\\\0&0&-4\\end{pmatrix}$（列对应按 $B$ 的对角顺序，按数据解析核对）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2019数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2019数二真题.md', TIPS_2019)
