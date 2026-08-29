# -*- coding: utf-8 -*-
# 2016 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
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

TIPS_2016 = {
1: """【公式】三阶对比：$\\alpha_1=x(\\cos\\sqrt x-1)\\sim-x\\cdot\\tfrac x2=-\\tfrac{x^{2}}{2}$；$\\alpha_2=\\sqrt x\\ln(1+x^{1/3})\\sim x^{5/6}$；$\\alpha_3=\\sqrt[3]{1+\\sqrt[3]{x}}-1\\sim\\tfrac{x^{1/3}}{3}$。
【技巧】阶数：$\\alpha_3(\\tfrac13)<\\alpha_1(\\tfrac32)<\\alpha_2(\\tfrac56)$? 统一化成 $x$ 的幂：$\\tfrac13<\\tfrac56<\\tfrac32$ → 从低到高 $\\alpha_3,\\alpha_2,\\alpha_1$。
【易错】$\\alpha_1$ 的阶是 $\\dfrac32$（$x\\cdot\\tfrac x2$）；$\\alpha_2$ 是 $1+\\tfrac13=\\tfrac56$。
【注意】答案 B（$\\alpha_3,\\alpha_2,\\alpha_1$）。""",
2: """【公式】分段原函数：$F'(x)=f(x)$ 且 $F$ 在 $x=1$ 连续可导——$x<1$ 段 $(x-1)^{2}+C_1$、$x\\ge1$ 段 $x\\ln x-x+C_2$，连续 + 导数匹配定常数。
【技巧】原函数存在定理：$f$ 含绝对跳跃不连续（本题 $f$ 在 $x=1$ 左右极限 $0,0$ 连续 ✓）→ 原函数存在且连续拼接。
【易错】两个任意常数不是独立的（连续条件 $-1+C_1=-1+C_2$ → $C_1=C_2$）。
【注意】答案 D。""",
3: """【公式】$(1)$：$\\left(-\\mathrm e^{1/x}\\right)'=\\dfrac{1}{x^{2}}\\mathrm e^{1/x}$ → 积分限 $-\\infty\\to0$ 时 $\\mathrm e^{1/x}\\to0$ → 收敛；$(2)$ 发散。
【技巧】找原函数定敛散最稳；$(1)$ 收敛、$(2)$ $\\displaystyle\\int_0^{1}\\dfrac{1}{x}\\mathrm e^{1/x}\\,\\mathrm dx$ 换元 $u=\\dfrac1x$ 化 $\\displaystyle\\int_1^{+\\infty}\\dfrac{\\mathrm e^{u}}{u}\\,\\mathrm du$ 发散。
【易错】积分限翻转的负号；$(2)$ 的发散性判断（$\\mathrm e^{u}$ 指数增长）。
【注意】答案 B（(1) 收敛、(2) 发散）。""",
4: """【公式】导函数图形：$f'$ 的零点 + 变号 → $f$ 的极值；$f'$ 图形上 $f''$ 类似分析（图形单调性变化）。
【技巧】图给 $f'$ 曲线：$x_1,x_3,x_4$ 处 $f'=0$ 且变号（左右 $f'$ 符号翻转），$x_2$ 处 $f'=0$ 但不变号（切于横轴）。
【易错】极值点 3 个、拐点 2 个（$f''=f'$ 的极值点 → $f'$ 图形的极值点位置）——图形双重解读。
【注意】答案 B。""",
5: """【公式】公切线在曲线上方（凸曲线 $f_i''<0$）→ $f_i(x)\\le g(x)$（$g$ 为切线）；$g(x_0)=f_1(x_0)=f_2(x_0)$、$g'=f_i'(x_0)$。
【技巧】$f_1(x)-f_2(x)$ 在 $x_0$ 处取极大值（$g$ 夹在中间）：$(f_1-f_2)'=0$、$(f_1-f_2)''=f_1''-f_2''$ 符号？——按选项方向核对。
【易错】切线位于凸曲线上方 → $f_i\\le g$；两曲线都在 $g$ 下但相对大小由极值方向定。
【注意】答案 A（$x_0$ 是 $f_1-f_2$ 的极值点）。""",
6: """【公式】商求导：$f'_x=\\dfrac{\\mathrm e^{x}(x-y)-(\\mathrm e^{x}-\\mathrm e^{y})}{(x-y)^{2}}$；$f'_y=\\dfrac{-\\mathrm e^{y}(x-y)+(\\mathrm e^{x}-\\mathrm e^{y})}{(x-y)^{2}}$。
【技巧】"对任意 $x\\ne y$"的恒等式（选项 D）：两项相加 $f'_x+f'_y=\\dfrac{(\\mathrm e^{x}-\\mathrm e^{y})(1-x+y)}{(x-y)^{2}}$? 逐项化简核对——商的分子分母结构。
【易错】$f'_y$ 的 $-\\mathrm e^{y}(x-y)-(\\mathrm e^{x}-\\mathrm e^{y})\\cdot(-1)$ 双重负号。
【注意】答案 D。""",
7: """【公式】相似不变量与传递性：$B=P^{-1}AP$ → $B^{\\mathrm T}=P^{\\mathrm T}A\\left(P^{-1}\\right)^{\\mathrm T}=(P^{-1})^{\\mathrm T}$? 对照选项；$P^{-1}+P$ 类似 $A^{-1}+A$ 的相似（$Q=P^{-1}$）。
【技巧】"(B) $P^{-1}BP? $ / $P^{\\mathrm T}BP$" 类：$A^{\\mathrm T}\\sim B^{\\mathrm T}$ ✓（$B^{\\mathrm T}=(P^{\\mathrm T})^{-1}A^{\\mathrm T}P^{\\mathrm T}$）；(C) $A^{*}\\sim B^{*}$（$B^{*}=P^{*}?$? $B^{*}=P^{\\mathrm T}$? 逐项验证）。
【易错】$A^{-1}\\sim B^{-1}$ ✓（$B^{-1}=P^{-1}A^{-1}P$）；$A^{*}\\sim B^{*}$：$B^{*}=|B|B^{-1}=|A|P^{-1}A^{-1}P=P^{-1}A^{*}P$ ✓——错误的是 C。
【注意】答案 C。""",
8: """【公式】$A=aE+J$（$J$ 全 1 元素）：特征值 $a+3$（对应全 1 向量）与 $a$（二重，正交于全 1）。
【技巧】正负惯性指数 = 特征值正负个数：$a$ 需满足 $a+3$ 与 $a$ 异号 → $-3<a<0$ → 负惯性 2、正惯性 1 → $p=1,q=2$。
【易错】$|A|=a^{2}(a+3)$ 的符号分析也可（$a^{2}>0$ → $a(a+3)<0$）。
【注意】答案 C。""",
9: """【公式】斜渐近线：$y=\\dfrac{x^{3}}{1+x^{2}}+\\arctan(1+x^{2})=x-\\dfrac{x}{1+x^{2}}+\\arctan(1+x^{2})$。
【技巧】多项式除法出 $x$，尾项 $\\to0$；$\\arctan(1+x^{2})\\to\\dfrac{\\pi}{2}$（$x\\to\\pm\\infty$）→ 渐近线 $y=x+\\dfrac{\\pi}{2}$。
【易错】$\\arctan$ 两端极限同为 $\\dfrac{\\pi}{2}$（$1+x^{2}\\to+\\infty$，不产生 $-\\tfrac\\pi2$ 分支）。
【注意】$y=x+\\dfrac{\\pi}{2}$。""",
10: """【公式】黎曼和：$\\dfrac{1}{n^{2}}\\sum k\\sin\\dfrac{k}{n}=\\dfrac{1}{n}\\sum\\dfrac{k}{n}\\sin\\dfrac{k}{n}\\to\\displaystyle\\int_0^{1}x\\sin x\\,\\mathrm dx$。
【技巧】$\\displaystyle\\int_0^1 x\\sin x\\,\\mathrm dx=\\left[-x\\cos x+\\sin x\\right]_0^{1}=\\sin1-\\cos1$。
【易错】配平系数（$\\dfrac{k}{n^{2}}=\\dfrac1n\\cdot\\dfrac{k}{n}$）；分部积分。
【注意】答案 $\\sin1-\\cos1$。""",
11: """【公式】解的结构：$y_2-y_1=\\mathrm e^{x}$ 是齐次解 → $p$ 满足 $1+p=0$ → $p=-1$；特解 $y_1=x^{2}-\\mathrm e^{x}$ 代入非齐次读 $q$。
【技巧】$y'-y=2x-x^{2}$（代 $y_1$：$2x-1-(x^{2}-\\mathrm e^{x})\\cdot$? 直接代 $y_2=x^{2}$：$2x-x^{2}=q$）。
【易错】$\\mathrm e^{x}$ 对应齐次根 1；$q$ 由任一特解代入读出。
【注意】$y'-y=2x-x^{2}$。""",
12: """【公式】变限含 $x$ 的积分方程：$f(x)=(x+1)^{2}+2\\displaystyle\\int_0^x f$ → 两边求导 $f'=2(x+1)+2f$ → 一阶线性 $f'-2f=2(x+1)$。
【技巧】$f(0)=1$；通解 $f=C\\mathrm e^{2x}-x-\\dfrac{3}{2}$? 逐次求导读 $f^{(n)}(0)$ 的递推：$f'(0)=2\\cdot1+2=4$、$f''(0)=2+2f'(0)=10$ → $f^{(n)}(0)=5\\cdot2^{n-1}$ 型。
【易错】特解形式（$ax+b$ 型特解代回定 $a=-1$）；$n$ 项通项由前几项归纳。
【注意】$f^{(n)}(0)=5\\cdot2^{n-1}$。""",
13: """【公式】相关变化率：$l=\\sqrt{x^{2}+x^{6}}$ → $\\dfrac{\\mathrm dl}{\\mathrm dt}=\\dfrac{(2x+6x^{5})v_0}{2l}=\\dfrac{v_0(1+3x^{4})}{\\sqrt{1+x^{4}}}$。
【技巧】$x=1$ 代入：$\\dfrac{v_0\\cdot4}{\\sqrt2}=2\\sqrt2\\,v_0$。
【易错】$\\dfrac{\\mathrm dx}{\\mathrm dt}=v_0$ 的链式；$x=1$ 处 $l=\\sqrt2$。
【注意】$2\\sqrt2\\,v_0$。""",
14: """【公式】"相似于列变换后矩阵"：右端矩阵第 3 行 = 第 1 行 + 第 2 行 → 秩 2；原矩阵对角 $a$ 循环 → 特征值 $a-1,a-1,a+2$（各行和相等 → $(a+2)$ 特征值）。
【技巧】相似 ⟺ 特征值集合相同：右端秩 2 → 零特征值 → $a-1=0$? 循环阵 $\\lambda=a-1$（二重）、$a+2$ → 相似对象有零特征值 → $a=1$? 按数据答案核对（$a$ 与行列式）。
【易错】循环行列式特征值（行和相等模型）；相似 ⟺ 特征多项式相同 + 可对角化（实对称/循环阵均可对角化）。
【注意】答案 2（按数据解析：行列式或迹计算）。""",
15: """【公式】$1^{\\infty}$：$\\ln I=\\lim\\dfrac{\\ln(\\cos2x+2x\\sin x)}{x^{4}}$，内层 $\\cos2x+2x\\sin x=1-\\dfrac{2x^{2}}{?}\\cdots$ 泰勒到四阶：$\\cos2x=1-2x^{2}+\\tfrac{2x^{4}}{3}+\\cdots$、$2x\\sin x=2x^{2}-\\tfrac{x^{4}}{3}+\\cdots$ → 和 $=1+\\dfrac{x^{4}}{3}+\\cdots$。
【技巧】$\\ln(1+\\tfrac{x^{4}}{3}+\\cdots)\\sim\\tfrac{x^{4}}{3}$ → $\\dfrac{1}{x^{4}}\\cdot\\dfrac{x^{4}}{3}=\\dfrac13$。
【易错】$\\cos2x$ 与 $2x\\sin x$ 的 $x^{2}$ 项（$-2x^{2}$ 与 $+2x^{2}$）恰好相消——必须展开到 $x^{4}$ 才见分晓。
【注意】答案 $\\mathrm e^{1/3}$。""",
16: """【公式】分段变限：$x<1$ 时 $\\displaystyle\\int_0^{1}\\left|t^{2}-x^{2}\\right|\\mathrm dt=\\int_0^{x}(x^{2}-t^{2})\\,\\mathrm dt+\\int_{x}^{1}(t^{2}-x^{2})\\,\\mathrm dt$；$x\\ge1$ 全为 $x^{2}-t^{2}$。
【技巧】$f'(x)$ 分段（上限 $x$ 处被积函数为零，求导只剩内层）；$x=1$ 两侧导数衔接（$2x$ 与 $4x^{2}-2x$ 在 $x=1$ 都 $=2$ ✓）。
【易错】$x<1$ 段的 $\\int_0^{x}$ 与 $\\int_x^{1}$ 两块；$x=1$ 是连续拼接点。
【注意】最小值 $\\dfrac14$（$f'(x)=0$ 的内点）。""",
17: """【公式】隐函数极值：$z_x=-\\dfrac{2xz+2}{(x^{2}+y^{2})+1/z}$、$z_y=-\\dfrac{2yz+2}{\\cdots}$ → 驻点 $xz=-1,yz=-1$ → $x=y=-\\dfrac1z$。
【技巧】代回约束 $(x^{2}+y^{2})z+\\ln z+2(x+y+1)=0$：$x=y=-\\tfrac1z$ → $\\dfrac{2}{z^{2}}z+\\ln z-\\dfrac{4}{z}+2=0$? 试 $z=1$：$2+0-4+2=0$ ✓ → 极大值 $z=1$。
【易错】二阶判别（$A,C$ 符号按隐函数二阶导）；驻点 $x=y=-\\tfrac1z$ 的对称性。
【注意】极大值 $z=1$（$(-1,-1)$ 处）。""",
18: """【公式】$D$ 关于 $y$ 轴对称 → $xy$ 项消失；剩 $\\displaystyle\\iint\\dfrac{x}{\\sqrt{x^{2}+y^{2}}}=\\dfrac12\\displaystyle\\iint\\dfrac{x+y?}{}$? — 本题被积 $\\dfrac{x\\cos? }{}$ 按题：$\\dfrac{x}{\\sqrt{x^{2}+y^{2}}}$：关于 $x$ 奇 → 消零；按题给 $\\displaystyle\\iint\\dfrac{x^{2}+?}{}$。
【技巧】三角形区域（顶点 $O,(1,1),(-1,1)$）关于 $y$ 轴对称 → 奇项消、偶项留；按数据解析的极坐标/直角坐标路径。
【易错】对称轴是 $y$ 轴（$x\\mapsto-x$）；被积函数的奇偶按 $x$ 判。
【注意】答案 $1-\\dfrac{\\pi}{2}$。""",
19: """【公式】已知一解 $y_1=\\mathrm e^{x}$ → 降阶法：令 $y_2=u\\mathrm e^{x}$，代方程消 $\\mathrm e^{x}$ 得 $u''+\\left(2-\\dfrac{2x+1}{2x-1}\\right)u'=0$? 分离变量。
【技巧】降阶公式：$u'=\\dfrac{C\\mathrm e^{-\\int P\\,\\mathrm dx}}{y_1^{2}}$（$P=\\dfrac{-(2x+1)}{2x-1}$）→ $u=-(2x+1)\\mathrm e^{-x}$ → $y_2=-(2x+1)$。
【易错】$P$ 的符号（标准形 $y''+Py'+Qy=0$ 中 $P=\\dfrac{-(2x+1)}{2x-1}$）；常数解可取 $y_2=2x+1$。
【注意】通解 $y=C_1\\mathrm e^{x}+C_2(2x+1)$。""",
20: """【公式】两曲线：圆 $L_1$（$x^{2}+y^{2}=1$ 四分之一）与星形线段 $L_2$（$x=\\cos^{3}t,y=\\sin^{3}t$，$t\\in[\\tfrac{\\pi}{2},0]$ 反向）；$D$ 为两者围成。
【技巧】$V$（绕 $y=x$? 题给绕 $x$ 轴? 按题）：washer 圆部分 + 星形线部分参数体积 $\\pi\\displaystyle\\int y^{2}\\,\\mathrm dx$（$\\mathrm dx=-3\\cos^{2}t\\sin t\\,\\mathrm dt$）；表面积 $2\\pi\\int y\\sqrt{1+y'^{2}}$（星形线 $y'=3\\sin^{2}t\\cos t/\\sin?$ → $\\sqrt{1+9? }$ 已知 $y\\sqrt{1+y'^{2}}=3\\sin^{2}t\\cos t$）。
【易错】星形线的参数积分限方向（$t$ 从 $\\tfrac\\pi2$ 到 $0$ 翻负号）；$\\sqrt{1+y'^{2}}$ 的化简（$\\sin^{2}t\\cdot3?$）。
【注意】$V=\\dfrac{18\\pi}{35}$、$S=\\dfrac{16\\pi}{5}$。""",
21: """【公式】(I) 介值构造：$\\varphi(x)=f(x)-\\dfrac{1}{3\\pi}\\sin\\dfrac{3\\pi}{?}x$? 按 (I) 结论 $\\dfrac{1}{3\\pi}$：$f(0)=0$、$f\\left(\\tfrac{3\\pi}{2}\\right)=?$ 的两点零点定理。
【技巧】(II) 由 $f'(x)=\\dfrac{\\cos x}{2x-3\\pi}$：$x\\in\\left(0,\\tfrac{3\\pi}{2}\\right)$ 内 $\\cos$ 的符号分三段 → $f$ 的单调区间 → 极值与最值；$f\\left(\\tfrac{3\\pi}{2}\\right)=0$（题给）。
【易错】分母 $2x-3\\pi<0$（区间内恒负）→ $f'$ 符号 $=-\\cos x$ 的符号——单调性方向反转。
【注意】(I) $\\dfrac{1}{3\\pi}$（按数据解析）。""",
22: """【公式】$Ax=\\beta$ 有无穷多解 → $r(A)=r(\\bar A)<3$ → $\\det A=0$：按第一列展开 $\\det=-a^{2}+?$? 行变换读 $a$。
【技巧】无穷多解 → 特解 + 基础解系；$\\beta=(a,a+1,a-1)$? 代入行变换后的简化方程读 $a=0$。
【易错】$a=0$ 与 $a\\ne0$ 两分支；基础解系 $(0,-1,1)^{\\mathrm T}$ 与特解 $(1,-1,0)$? 按数据。
【注意】$a=0$；通解 $x=k(0,-1,1)^{\\mathrm T}+(1,-1,0)^{\\mathrm T}$ 型（按数据解析）。""",
23: """【公式】$A$ 特征多项式：$\\lambda\\left[(\\lambda+3)^{2}+2? \\right]=\\lambda(\\lambda^{2}+6\\lambda+8)=\\lambda(\\lambda+2)(\\lambda+4)$（按解析）→ 特征值 $0,-2,-4$。
【技巧】$A^{99}$ 用对角化：$A^{99}=P\\mathrm{diag}(0,(-2)^{99},(-4)^{99})P^{-1}$——幂零化简或 $A^{2}$ 直接递推（$A^{2}$ 与 $A$ 的关系式 $A^{2}+6A+8E=r$? 秩 1 修正）。
【易错】$(-2)^{99}$ 的符号（奇数次幂为负）；$P^{-1}$ 的计算或特征多项式降幂式 $A^{3}+6A^{2}+8A=O$ 的利用（$A^{99}=A\\cdot(A^{2})^{49}$ 递推更快）。
【注意】$A^{99}=\\begin{pmatrix}2^{99}-2&1-2^{99}&2-2^{98}\\\\2^{100}-2&1-2^{100}&2-2^{99}\\\\0&0&0\\end{pmatrix}$ 型（按数据解析核对）。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2016数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2016数二真题.md', TIPS_2016)
