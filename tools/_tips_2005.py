# -*- coding: utf-8 -*-
# 2005 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2005 = {
1: """【公式】幂指函数求导：$y=u^{v}=\\mathrm e^{v\\ln u}\\Rightarrow y'=u^{v}\\left(v'\\ln u+v\\dfrac{u'}{u}\\right)$。
【技巧】$x=\\pi$ 处 $\\sin\\pi=0$：$y=1$，$\\ln(1+\\sin x)=0$，只剩 $x\\cdot\\dfrac{\\cos x}{1+\\sin x}=\\pi\\cdot(-1)$ 一项。
【易错】$\\cos\\pi=-1$ 的符号；对数求导两项（$v'\\ln u$ 与 $v\\dfrac{u'}{u}$）都别丢。
【注意】答案 $-\\pi$。""",
2: """【公式】斜渐近线：$y=\\dfrac{(1+x)^{3/2}}{\\sqrt x}=x^{3/2}\\left(1+\\dfrac1x\\right)^{3/2}\\cdot\\dfrac1{\\sqrt x}$，用 $(1+\\tfrac1x)^{3/2}=1+\\dfrac{3}{2x}+o(\\tfrac1x)$。
【技巧】"提出 $x$ 的主导幂次 + 泰勒一阶展开"一步读出 $y=x+\\dfrac32$，比分别算 $k$、$b$ 快。
【易错】$x\\to+\\infty$ 单侧（$\\sqrt x$ 定义域）；展开只到一阶项，二次项并入误差。
【注意】渐近线 $y=x+\\dfrac32$。""",
3: """【公式】$x=\\sin t$：$\\sqrt{1-x^{2}}=\\cos t$；$\\displaystyle\\int\\frac{\\mathrm du}{1+u^{2}}=\\arctan u+C$。
【技巧】换元后分子 $\\sin t\\cos t\\,\\mathrm dt$ 与分母的 $\\cos t$ 约掉，剩 $\\dfrac{\\sin t}{1+\\cos^{2}t}\\,\\mathrm dt=-\\mathrm d(\\arctan\\cos t)$。
【易错】换元限 $0\\to\\dfrac\\pi2$；$\\mathrm d(\\cos t)=-\\sin t\\,\\mathrm dt$ 的负号。
【注意】答案 $\\arctan 1-\\arctan 0=\\dfrac{\\pi}{4}$。""",
4: """【公式】一阶线性 $y'+\\dfrac2x y=\\ln x$，积分因子 $x^{2}$：$\\left(x^{2}y\\right)'=x^{2}\\ln x$。
【技巧】$\\displaystyle\\int x^{2}\\ln x\\,\\mathrm dx=\\dfrac{x^{3}}{3}\\ln x-\\dfrac{x^{3}}{9}+C$（分部一次）。
【易错】通解 $y=\\dfrac{x\\ln x}{3}-\\dfrac{x}{9}+\\dfrac{C}{x^{2}}$ 的 $x^{-2}$ 因子；初值 $y(1)=-\\dfrac19$ 恰好消掉 $\\dfrac{x}{9}$ 项、定 $C=0$。
【注意】特解 $y=\\dfrac{x\\ln x}{3}-\\dfrac{x}{9}$。""",
5: """【公式】$\\sqrt{A}-\\sqrt{B}=\\dfrac{A-B}{\\sqrt A+\\sqrt B}$；$1-\\cos x\\sim\\dfrac{x^{2}}{2}$；$\\arcsin x\\sim x$。
【技巧】$\\sqrt{1+x\\arcsin x}-\\sqrt{\\cos x}\\to0$ 是 $\\tfrac00$：有理化后分子 $1+x\\arcsin x-\\cos x\\sim\\dfrac32x^{2}$，分母 $\\sqrt A+\\sqrt B\\to2$，故 $\\beta\\sim\\dfrac34x^{2}$。
【易错】$-\\cos x$ 展开成 $-1+\\dfrac{x^{2}}{2}$（负号保留）；分母趋 2 不是趋 1。
【注意】$k=\\dfrac34$。""",
6: """【公式】列组合 → 矩阵乘法：$B=A\\,C$（$C$ 为组合系数矩阵），$|B|=|A|\\cdot|C|$。
【技巧】把每个新列写成 $\\alpha_1,\\alpha_2,\\alpha_3$ 的系数作为 $C$ 的列，$|C|$ 用行列式性质（列和相等型 = $\\dfrac{\\text{公因子}}{}$）快速算。
【易错】系数矩阵别转置错方向（新列的系数放 $C$ 的**列**）。
【注意】$|C|=2$，$|B|=2|A|$（答案 2）。""",
7: """【公式】夹逼：$|x|<1$ 时 $1\\le\\sqrt[n]{1+|x|^{3n}}<\\sqrt[n]{2}\\to1$；$|x|>1$ 时 $\\sqrt[n]{|x|^{3n}}<\\cdot<|x|^{3}\\sqrt[n]{2}\\to|x|^{3}$。
【技巧】"最大项压倒"模型：$\\lim\\sqrt[n]{a^{n}+b^{n}}=\\max(a,b)$，本题 $\\max(1,|x|^{3})$。
【易错】$|x|=1$ 时极限是 1（$\\sqrt[n]{2}\\to1$），不是 2——分段点两侧衔接才保证连续。
【注意】处处连续、$\\pm1$ 处不可导（答案 C）。""",
8: """【公式】原函数奇偶性定理：$f$ 奇 $\\Leftrightarrow$ $f$ 的**任一**原函数都偶（$F(x)=\\int_0^x f+C$ 中 $C$ 不破坏偶性）；$f$ 偶 $\\Leftrightarrow$ 恰有一个原函数奇（$C=0$ 那个）。
【技巧】用 $F(x)=\\int_0^x f+ C$ 统一表达"任一原函数"，换元核对 $F(-x)$ 与 $F(x)$。
【易错】偶函数的原函数不一定奇——差常数项，选项里"任一/存在"的措辞就是考点。
【注意】答案 A。""",
9: """【公式】参数导数：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{1/(1+t)}{2t+2}=\\dfrac{1}{2(t+1)^{2}}$。
【技巧】$x=3$ 解出 $t=1$ 与 $t=-3$，但 $y=\\ln(1+t)$ 要求 $t>-1$ → 舍 $t=-3$（定义域筛根）。
【易错】法线斜率是切线斜率的负倒数：$\\dfrac18\\to-8$；$y$ 值 $\\ln2$ 别丢。
【注意】法线 $y-\\ln2=-8(x-3)$。""",
10: """【公式】区域关于 $y=x$ 对称 → $\\displaystyle\\iint_D f(x,y)\\,\\mathrm d\\sigma=\\iint_D f(y,x)\\,\\mathrm d\\sigma$。
【技巧】原积分 $I$ 与互换 $x,y$ 后的积分 $I'$ 相加：$I+I'$ 里 $a\\sqrt f$ 与 $b/\\sqrt f$ 配平，得 $I=\\dfrac{a+b}{2}\\displaystyle\\iint_D\\left(\\sqrt f+\\dfrac1{\\sqrt f}\\right)\\mathrm d\\sigma$ 型常数。
【易错】对称性只适用于**关于 $y=x$ 对称的区域**（本题 $x\\ge0,y\\ge0$ 圆域满足）。
【注意】答案 D（常数 $(a+b)$ 的一半型）。""",
11: """【公式】变限积分上下限求导：$\\dfrac{\\partial}{\\partial x}\\displaystyle\\int_{x-y}^{x+y}\\psi=\\psi(x+y)-\\psi(x-y)$（上限导 +、下限导 −）。
【技巧】$u_{xx}-u_{yy}$ 逐项算：$\\varphi(x\\pm y)$ 的二阶链式系数相同相消，剩 $\\psi$ 项——对照选项直接判。
【易错】$\\varphi'(x-y)$ 对 $y$ 求导出负号；二阶展开整理时的正负号配平。
【注意】答案 B。""",
12: """【公式】$\\dfrac{x}{x-1}\\to\\mp\\infty$（$x\\to1^{\\mp}$）→ $\\mathrm e^{\\frac{x}{x-1}}\\to0/+\\infty$；$x\\to0$ 时 $\\dfrac{x}{x-1}\\to0$ → 分母 $\\mathrm e^{0}-1=0$。
【技巧】逐点求左右极限归类：$x=1$ 处左右都使 $f\\to0$？分母 $\\to\\pm\\infty$、$f\\to0$（第一类可去趋势）；$x=0$ 处分母 $\\to0$、$f\\to\\infty$（第二类）。
【易错】$\\mathrm e^{+\\infty}$ 与 $\\mathrm e^{-\\infty}$ 天壤之别——$\\dfrac{x}{x-1}$ 在 $1$ 两侧一个 $+\\infty$ 一个 $-\\infty$。
【注意】答案 D。""",
13: """【公式】$A(\\alpha_1+\\alpha_2)=\\lambda_1\\alpha_1+\\lambda_2\\alpha_2\\ne\\lambda(\\alpha_1+\\alpha_2)$（$\\lambda_1\\ne\\lambda_2$）。
【技巧】特征向量的非零线性组合仍是特征向量 $\\Leftrightarrow$ 组合的向量**属于同一特征值**；不同特征值的和向量必不是。
【易错】$\\alpha_1+\\alpha_2$ 不是特征向量，但 $\\alpha_1$、$\\alpha_2$ 各自是；$k_1k_2\\ne0$ 的条件就是排除"只取一个"。
【注意】答案 B。""",
14: """【公式】行交换：$B=E_{12}A$；伴随转置关系 $B^{*}=A^{*}E_{12}^{*}$，$E_{12}^{*}=|E_{12}|E_{12}^{-1}=-E_{12}$ → $B^{*}=-A^{*}E_{12}$。
【技巧】伴随矩阵乘法配合 $A^{*}A=|A|E$：$B^{*}A=-A^{*}E_{12}A=-A^{*}B$ 一行出答案。
【易错】行变换左乘、$E_{12}^{-1}=E_{12}$、$|E_{12}|=-1$ 三个小点凑齐才不错。
【注意】答案 C。""",
15: """【公式】被积函数含 $x-t$：换元 $u=x-t$ → $\\displaystyle\\int_0^{x}uf(u)\\,\\mathrm du$（限随 $x$ 变，积分变量与 $x$ 解耦）。
【技巧】之后三次洛必达（分子是 $x$ 的三阶变限积分），或直接用 $\\left(\\displaystyle\\int_0^x uf(u)\\mathrm du\\right)'=xf(x)$。
【易错】换元后上下限（$u:x\\to0$，翻负号）；洛必达时 $x$ 是常量、只对上限变量求导。
【注意】答案 $\\dfrac12$。""",
16: """【公式】"面积相等" → 变限积分方程：$C_3$ 左侧面积（对 $y$ 积分更方便）$\\displaystyle\\int_1^{\\varphi(y)}(C_2-C_1)\\,\\mathrm dx$ 型。
【技巧】把 $y=\\varphi(x)$ 反写成 $x=\\varphi(y)$：两曲线 $\\mathrm e^{y}-1$ 与 $\\tfrac12(\\mathrm e^{y}+1)$ 之差对 $y$ 积分，$=\\dfrac{\\mathrm e^{y}-1}{2}-y$。
【易错】积分区间从 $y=1$（过点 $(0,1)$）起；对 $y$ 积分时两条曲线的左右关系。
【注意】$x=\\varphi(y)=\\ln y-\\dfrac{y-1}{2y}$。""",
17: """【公式】拐点 $(3,2)$ → $f''(3)=0$；切线斜率读导数：$l_1$ 过 $(0,0)$、$(2,4)$ → $f'(0)=2$；$l_2$ 过 $(2,4)$、$(3,2)$ → $f'(3)=\\dfrac{4-2}{2-3}=-2$。
【技巧】$\\displaystyle\\int_0^3(x^{2}+x)f'''\\,\\mathrm dx$ 逐次分部积分（$f'''=\\mathrm df''$）：每层把导数往 $f$ 挪一层，边界项 $\\left[(x^{2}+x)f''\\right]$、$\\left[(2x+1)f'\\right]$ 用已知值结算，最后 $2\\int_0^3 f'=2[f(3)-f(0)]=4$。
【易错】$l_2$ 的斜率用"交点 − 切点"算（$\\dfrac{4-2}{2-3}=-2$），方向别反；边界项在 $x=0$ 处系数 $(x^{2}+x)=0$ 自动消失。
【注意】三段结算 $=7\\times2+1\\times2+2\\times2=20$。""",
18: """【公式】变量替换的二阶导：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{\\dot y}{\\dot x}=-\\dfrac{\\dot y}{\\sin t}$，$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{\\ddot y\\,\\dot x-\\dot y\\,\\ddot x}{\\dot x^{3}}$（$\\dot x=-\\sin t,\\ddot x=-\\cos t$）。
【技巧】$(1-x^{2})=\\sin^{2}t$、$-xy'$ 项代入后整式相消 → 方程化成 $y''_{t}+y=0$（欧拉型转常系数的典范）。
【易错】$\\dot x=-\\sin t$ 的负号进二阶公式；$x=0\\Leftrightarrow t=\\dfrac\\pi2$ 定初值 $y|_{t=\\pi/2}=1,\\ y'|_{t=\\pi/2}=-2$。
【注意】解 $y=C_1\\cos t+C_2\\sin t$，回代 $y=2x+\\sqrt{1-x^{2}}$（$-1<x<1$）。""",
19: """【公式】零点定理：$F(x)=f(x)+x-1$，$F(0)=-1<0$、$F(1)=1>0$ → 存在 $\\xi\\in(0,1)$ 使 $f(\\xi)+\\xi-1=0$。
【技巧】(Ⅱ) 用 $f$ 递增 + $f(\\xi)=1-\\xi$ 把 $[0,1]$ 拆成 $[0,\\xi]$ 与 $[\\xi,1]$ 两段分别用拉格朗日中值定理，相加配出 $f(b)-f(a)$ 的夹逼。
【易错】$F(0)$、$F(1)$ 的符号别代错（$f(0)=0$、$f(1)=1$）；(Ⅱ) 两段中值后还要用 $f'>-1$? 题给 $f$ 单调增的条件筛选。
【注意】这类"存在 ξ + 再证不等式"的双问结构：(Ⅰ) 的结论是 (Ⅱ) 的分段点。""",
20: """【公式】全微分还原：$f=\\displaystyle\\int 2x\\,\\mathrm dx=x^{2}+g(y)$，对 $y$ 偏导 $g'(y)=-2y$ → $f=x^{2}-y^{2}+C$；$f(1,1)=2\\Rightarrow C=2$。
【技巧】椭圆边界 $x^{2}+\\dfrac{y^{2}}{2}=1$ 上求 $f$ 最值：参数化 $x=\\cos t,y=\\sqrt2\\sin t$ → $f=\\cos^{2}t-2\\sin^{2}t+2$，余弦二次型直接读最值。
【易错】$y^{2}=2\\sin^{2}t$ 的系数 2；内部驻点 $(0,0)$：$f=2$（不是最值）。
【注意】最大 3（$x=\\pm1$），最小 $-2$（$y=\\pm\\sqrt2$）。""",
21: """【公式】绝对值分区：$x^{2}+y^{2}\\le1$ 内取 $1-(x^{2}+y^{2})$、外取 $-$；极坐标 $\\mathrm d\\sigma=r\\,\\mathrm dr\\,\\mathrm d\\theta$。
【技巧】第一象限单位圆 $D$：圆内 $\\displaystyle\\int_0^{\\pi/2}\\!\\!\\int_0^{1}(1-r^{2})r\\,\\mathrm dr\\,\\mathrm d\\theta$、圆环外同理；或"整圆 − 补块"。
【易错】绝对值零线 $r=1$ 恰好是 $D$ 的边界 → 圆内部分只有"内圆"，外侧部分被 $D$ 裁成扇形块。
【注意】答案 $\\dfrac{\\pi}{4}-\\dfrac{1}{3}$。""",
22: """【公式】线性相关 $\\Leftrightarrow|A|=0$：$\\left|\\begin{smallmatrix}1&1&a\\\\1&a&1\\\\a&1&1\\end{smallmatrix}\\right|=(a+2)(a-1)^{2}$ → 候选 $a=1,-2$。
【技巧】双条件题：相关（行列式为 0）+ "某向量不能由其余表示"（秩恰好 $2$）——$a=1$ 时 $\\alpha_1=\\alpha_2$ 秩 2 ✓；$a=-2$ 时秩 2 但 $\\alpha_3$ 可由 $\\alpha_1,\\alpha_2$ 表示 → 排除。
【易错】两个候选只验证相关、不验证第二条件就下结论——$a=-2$ 是陷阱选项。
【注意】$a=1$。""",
23: """【公式】$AB=O\\Rightarrow$ ① $B$ 的每列都是 $Ax=0$ 的解；② $r(A)+r(B)\\le3$。
【技巧】$B$ 的秩由 $k$ 决定：$k=9$ 时第 2、3 行都是第 1 行的 3 倍 → $r(B)=1$；$k\\ne9$ → $r(B)=2$ → 按 $r(A)=3-r(B)$ 分层讨论基础解系个数。
【易错】$r(B)$ 的判断（行成比例与否）；基础解系向量个数 = $n-r(A)$。
【注意】(2) 分 $r(A)=1$、$r(A)=2$ 两种情形分别写通解。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2005数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2005数二真题.md', TIPS_2005)
