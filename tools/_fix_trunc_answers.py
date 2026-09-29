# -*- coding: utf-8 -*-
"""第一批：重写 18 道「解析截断 / $$ 未闭合 / 冗长」题的答案（单一方法、步骤完整、不啰嗦）"""
import json, io

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

NEW = {}

NEW[23] = """【答案】$\\frac{2}{3}$

令 $t=\\frac1x$，则 $x\\to\\infty$ 时 $t\\to0$，原式化为
$$
L=\\lim_{t\\to0}\\frac{1}{t^{2}}\\left(2-\\frac{\\sin t}{t}-\\cos t\\right)
=\\lim_{t\\to0}\\frac{2t-\\sin t-t\\cos t}{t^{3}}.
$$
用泰勒公式（展开到 $t^{3}$）：
$$
\\sin t=t-\\frac{t^{3}}{6}+o(t^{3}),\\qquad
t\\cos t=t\\left(1-\\frac{t^{2}}{2}+o(t^{2})\\right)=t-\\frac{t^{3}}{2}+o(t^{3}).
$$
代入分子：
$$
2t-\\sin t-t\\cos t=2t-\\left(t-\\frac{t^{3}}{6}\\right)-\\left(t-\\frac{t^{3}}{2}\\right)+o(t^{3})
=\\frac{2}{3}t^{3}+o(t^{3}).
$$
故
$$
L=\\lim_{t\\to0}\\frac{\\frac23t^{3}+o(t^{3})}{t^{3}}=\\frac{2}{3}.
$$"""

NEW[54] = """【答案】$0$

记 $I_n=\\displaystyle\\int_0^1 \\mathrm e^{-x}\\sin nx\\,\\mathrm dx$。先求不定积分（待定系数）：
$$
\\int \\mathrm e^{-x}\\sin nx\\,\\mathrm dx=-\\frac{\\mathrm e^{-x}(\\sin nx+n\\cos nx)}{1+n^{2}}+C.
$$
于是
$$
I_n=\\left[-\\frac{\\mathrm e^{-x}(\\sin nx+n\\cos nx)}{1+n^{2}}\\right]_0^1
=\\frac{n}{1+n^{2}}-\\frac{\\mathrm e^{-1}(\\sin n+n\\cos n)}{1+n^{2}}.
$$
当 $n\\to\\infty$ 时，$\\frac{n}{1+n^{2}}\\to0$，且 $|\\sin n+n\\cos n|\\le n+1$，故第二项的绝对值不超过 $\\frac{n+1}{\\mathrm e(1+n^{2})}\\to0$。因此
$$
\\lim_{n\\to\\infty}I_n=0.
$$"""

NEW[185] = """【答案】$y=x+2$

设斜渐近线为 $y=kx+b$。
$$
k=\\lim_{x\\to\\infty}\\frac{y}{x}=\\lim_{x\\to\\infty}\\left(1+\\arcsin\\frac{2}{x}\\right)=1,
$$
$$
b=\\lim_{x\\to\\infty}(y-kx)=\\lim_{x\\to\\infty}x\\arcsin\\frac{2}{x}
\\overset{u=\\frac2x}{=}\\lim_{u\\to0}\\frac{2\\arcsin u}{u}=2.
$$
故斜渐近线方程为 $y=x+2$。"""

NEW[397] = """【答案】$2$

由 $\\varphi(x)=x\\displaystyle\\int_0^{x^2}f(t)\\,\\mathrm dt$，求导得
$$
\\varphi'(x)=\\int_0^{x^2}f(t)\\,\\mathrm dt+x\\cdot 2x\\,f(x^{2})=\\int_0^{x^2}f(t)\\,\\mathrm dt+2x^{2}f(x^{2}).
$$
代入 $x=1$：
$$
\\varphi(1)=\\int_0^1 f(t)\\,\\mathrm dt=1,\\qquad
\\varphi'(1)=\\int_0^1 f(t)\\,\\mathrm dt+2f(1)=1+2f(1)=5.
$$
故 $f(1)=2$。"""

NEW[153] = """【答案】$\\frac{1}{\\mathrm e}$

$y=f(f(x))$，由链式法则 $\\dfrac{\\mathrm dy}{\\mathrm dx}=f'(f(x))\\cdot f'(x)$。

在 $x=\\mathrm e$ 处：$f(\\mathrm e)=\\ln\\sqrt{\\mathrm e}=\\frac12$，且因 $\\mathrm e>1$，取 $f'(x)=\\frac{1}{2x}$ 得 $f'(\\mathrm e)=\\frac{1}{2\\mathrm e}$。

又 $f(\\mathrm e)=\\frac12<1$，故外层落在 $x<1$ 分支，$f'(x)=2$，即 $f'\\!\\left(\\frac12\\right)=2$。

因此
$$
\\left.\\frac{\\mathrm dy}{\\mathrm dx}\\right|_{x=\\mathrm e}=f'\\!\\left(\\tfrac12\\right)\\cdot f'(\\mathrm e)=2\\cdot\\frac{1}{2\\mathrm e}=\\frac{1}{\\mathrm e}.
$$"""

NEW[160] = """【答案】$\\dfrac{2}{3}$

$$
\\frac{\\mathrm dx}{\\mathrm dt}=2\\mathrm e^{t}+1,\\qquad
\\frac{\\mathrm dy}{\\mathrm dt}=4\\mathrm e^{t}+4(t-1)\\mathrm e^{t}+2t=4t\\mathrm e^{t}+2t.
$$
$t=0$ 时：$\\frac{\\mathrm dx}{\\mathrm dt}=3$，$\\frac{\\mathrm dy}{\\mathrm dt}=0$，故 $\\frac{\\mathrm dy}{\\mathrm dx}=0$。

再求导：
$$
\\frac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\frac{\\mathrm d}{\\mathrm dt}\\left(\\frac{\\mathrm dy}{\\mathrm dx}\\right)\\Big/\\frac{\\mathrm dx}{\\mathrm dt},\\qquad
\\frac{\\mathrm dy}{\\mathrm dx}=\\frac{4t\\mathrm e^{t}+2t}{2\\mathrm e^{t}+1}.
$$
记 $u=4t\\mathrm e^{t}+2t,\\ v=2\\mathrm e^{t}+1$，则 $u(0)=0,\\ v(0)=3,\\ u'(0)=6$，故
$$
\\left.\\frac{\\mathrm d}{\\mathrm dt}\\left(\\frac{\\mathrm dy}{\\mathrm dx}\\right)\\right|_{t=0}=\\frac{u'(0)v(0)-u(0)v'(0)}{v^{2}(0)}=\\frac{6\\cdot3}{9}=2.
$$
于是 $\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{2}{3}$。"""

NEW[180] = """【答案】$y=3x$

点 $(0,0)$ 对应 $t=1$（此时 $x=\\int_0^0=0,\\ y=1\\cdot\\ln1=0$）。

求导：
$$
\\frac{\\mathrm dx}{\\mathrm dt}=\\mathrm e^{-(1-t)^{2}}\\cdot(-1),\\qquad
\\left.\\frac{\\mathrm dx}{\\mathrm dt}\\right|_{t=1}=-1;
$$
$$
\\frac{\\mathrm dy}{\\mathrm dt}=2t\\ln(2-t^{2})-\\frac{2t^{3}}{2-t^{2}},\\qquad
\\left.\\frac{\\mathrm dy}{\\mathrm dt}\\right|_{t=1}=-3.
$$
故切线斜率
$$
k=\\left.\\frac{\\mathrm dy}{\\mathrm dx}\\right|_{t=1}=\\frac{-3}{-1}=3,
$$
切线方程为 $y=3x$。"""

NEW[211] = """【答案】B

当 $x\\le0$ 时 $|x|=-x$，故
$$
f(x)=\\begin{cases}-x^{2},& x\\le0,\\\\ x\\ln x,& x>0,\\end{cases}\\qquad f(0)=0.
$$
**可导性**：左导数 $\\lim\\limits_{x\\to0^-}\\frac{-x^2-0}{x}=0$；右导数 $\\lim\\limits_{x\\to0^+}\\frac{x\\ln x}{x}=\\lim\\limits_{x\\to0^+}\\ln x=-\\infty$。故 $x=0$ 不可导。

**极值**：$x<0$ 时 $f(x)=-x^{2}<0$；$0<x<1$ 时 $\\ln x<0$，故 $f(x)=x\\ln x<0$。即在 $x=0$ 的某去心邻域内恒有 $f(x)<f(0)=0$，$x=0$ 为极大值点。

综上，$x=0$ 是不可导点、极值点，选 B。"""

NEW[227] = """【答案】极小值点 $\\left(\\frac53,\\frac13\\right)$（极小值 $\\frac13$），极大值点 $\\left(-\\frac13,\\frac53\\right)$（极大值 $\\frac53$）；拐点 $\\left(\\frac13,\\frac13\\right)$；$t>0$ 时曲线凹，$t<0$ 时凸。

$$
\\frac{\\mathrm dx}{\\mathrm dt}=t^{2}+1,\\qquad \\frac{\\mathrm dy}{\\mathrm dt}=t^{2}-1,\\qquad
\\frac{\\mathrm dy}{\\mathrm dx}=\\frac{t^{2}-1}{t^{2}+1}.
$$
**极值**：令 $\\frac{\\mathrm dy}{\\mathrm dx}=0$ 得 $t=\\pm1$。
$t=1$ 时 $x=\\frac53,\\ y=\\frac13$；$t=-1$ 时 $x=-\\frac13,\\ y=\\frac53$。
因 $t^{2}+1>0$，$\\frac{\\mathrm dy}{\\mathrm dx}$ 的符号由 $t^{2}-1$ 决定：$t<-1$ 为正、$-1<t<1$ 为负、$t>1$ 为正，故 $t=-1$ 处取极大、$t=1$ 处取极小。

**凹凸与拐点**：
$$
\\frac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\frac{\\mathrm d}{\\mathrm dt}\\left(\\frac{t^{2}-1}{t^{2}+1}\\right)\\Big/(t^{2}+1)=\\frac{4t}{(t^{2}+1)^{3}}.
$$
分母恒正，故 $t>0$ 时二阶导为正（凹），$t<0$ 时为负（凸）；$t=0$ 时二阶导为 $0$ 且变号，对应 $(x,y)=\\left(\\frac13,\\frac13\\right)$ 为拐点。"""

NEW[255] = """【答案】$\\arcsin\\dfrac{x-2}{2}+C$

配方：
$$
x(4-x)=4-(x-2)^{2}=2^{2}-(x-2)^{2}.
$$
于是
$$
\\int\\frac{\\mathrm dx}{\\sqrt{x(4-x)}}=\\int\\frac{\\mathrm dx}{\\sqrt{2^{2}-(x-2)^{2}}}
=\\arcsin\\frac{x-2}{2}+C.
$$"""

NEW[316] = """【答案】$\\dfrac{\\mathrm e^{\\pi}+1}{2(\\mathrm e^{\\pi}-1)}$

曲线在 $x=k\\pi\\ (k=0,1,2,\\dots)$ 处与 $x$ 轴相交，相邻交点之间为一拱，第 $k$ 拱的面积为
$$
a_k=\\int_{k\\pi}^{(k+1)\\pi}\\mathrm e^{-x}|\\sin x|\\,\\mathrm dx.
$$
作代换 $x=k\\pi+u$（$u\\in[0,\\pi]$，此时 $\\sin x=(-1)^{k}\\sin u$，取绝对值后为 $\\sin u$）：
$$
a_k=\\mathrm e^{-k\\pi}\\int_0^{\\pi}\\mathrm e^{-u}\\sin u\\,\\mathrm du.
$$
由 $\\displaystyle\\int \\mathrm e^{-x}\\sin x\\,\\mathrm dx=-\\frac{\\mathrm e^{-x}(\\sin x+\\cos x)}{2}+C$ 得
$$
\\int_0^{\\pi}\\mathrm e^{-u}\\sin u\\,\\mathrm du=\\left[-\\frac{\\mathrm e^{-u}(\\sin u+\\cos u)}{2}\\right]_0^{\\pi}=\\frac{1+\\mathrm e^{-\\pi}}{2}.
$$
故 $a_k=\\dfrac{1+\\mathrm e^{-\\pi}}{2}\\,\\mathrm e^{-k\\pi}$。总面积为等比级数（公比 $q=\\mathrm e^{-\\pi}$）：
$$
S=\\sum_{k=0}^{\\infty}a_k=\\frac{1+\\mathrm e^{-\\pi}}{2}\\cdot\\frac{1}{1-\\mathrm e^{-\\pi}}
=\\frac{\\mathrm e^{\\pi}+1}{2(\\mathrm e^{\\pi}-1)}.
$$"""

NEW[404] = """【答案】C

**连续性**：取路径 $y=kx$（$x\\to0$），
$$
\\lim_{x\\to0}f(x,kx)=\\lim_{x\\to0}\\frac{kx^{2}}{x^{2}+k^{2}x^{2}}=\\frac{k}{1+k^{2}},
$$
随 $k$ 变化而不同（如 $k=0$ 时为 $0$，$k=1$ 时为 $\\frac12$），故重极限不存在，$f$ 在 $(0,0)$ 不连续。

**偏导数**：按定义，
$$
f'_x(0,0)=\\lim_{x\\to0}\\frac{f(x,0)-f(0,0)}{x}=\\lim_{x\\to0}\\frac{0-0}{x}=0,
$$
同理 $f'_y(0,0)=0$。故两个偏导数都存在。

因此选 C（不连续，偏导数存在）。"""

NEW[412] = """【答案】(D)

令 $u=x+y,\\ v=\\dfrac yx$，解得
$$
x=\\frac{u}{1+v},\\qquad y=\\frac{uv}{1+v}.
$$
代入 $f\\left(x+y,\\frac yx\\right)=x^{2}-y^{2}$：
$$
f(u,v)=\\left(\\frac{u}{1+v}\\right)^{2}-\\left(\\frac{uv}{1+v}\\right)^{2}
=\\frac{u^{2}(1-v^{2})}{(1+v)^{2}}=\\frac{u^{2}(1-v)}{1+v}.
$$
求偏导并代入 $u=1,\\ v=1$：
$$
\\frac{\\partial f}{\\partial u}=\\frac{2u(1-v)}{1+v}\\Rightarrow\\left.\\frac{\\partial f}{\\partial u}\\right|_{(1,1)}=0,
\\qquad
\\frac{\\partial f}{\\partial v}=u^{2}\\cdot\\frac{-(1+v)-(1-v)}{(1+v)^{2}}=\\frac{-2u^{2}}{(1+v)^{2}}\\Rightarrow\\left.\\frac{\\partial f}{\\partial v}\\right|_{(1,1)}=-\\frac{1}{2}.
$$
依次是 $0$ 与 $-\\dfrac12$，选 D。"""

NEW[416] = """【答案】$\\dfrac{y}{\\cos x}+\\dfrac{x}{\\cos y}$

设 $u=\\sin y-\\sin x$，则 $z=f(u)+xy$。由复合求导：
$$
\\frac{\\partial z}{\partial x}=f'(u)(-\\cos x)+y,\\qquad
\\frac{\\partial z}{\partial y}=f'(u)\\cos y+x.
$$
代入所求式：
$$
\\frac{1}{\\cos x}\\cdot\\frac{\\partial z}{\\partial x}+\\frac{1}{\\cos y}\\cdot\\frac{\\partial z}{\\partial y}
=\\frac{-f'(u)\\cos x+y}{\\cos x}+\\frac{f'(u)\\cos y+x}{\\cos y}
=-f'(u)+\\frac{y}{\\cos x}+f'(u)+\\frac{x}{\\cos y}
=\\frac{y}{\\cos x}+\\frac{x}{\\cos y}.
$$"""

NEW[417] = """【答案】B

设 $u=\\dfrac yx$，则 $z=xyf(u)$。求导：
$$
\\frac{\\partial z}{\\partial x}=yf(u)+xyf'(u)\\left(-\\frac{y}{x^{2}}\\right)=yf(u)-\\frac{y^{2}}{x}f'(u),
$$
$$
\\frac{\\partial z}{\\partial y}=xf(u)+xyf'(u)\\cdot\\frac1x=xf(u)+yf'(u).
$$
于是
$$
x\\frac{\\partial z}{\\partial x}+y\\frac{\\partial z}{\\partial y}=2xy\\,f(u).
$$
由题设 $2xy\\,f\\!\\left(\\frac yx\\right)=y^{2}\\ln\\frac yx$，即
$$
f(u)=\\frac{y}{2x}\\ln\\frac yx=\\frac{u}{2}\\ln u.
$$
故 $f(1)=0$，$f'(u)=\\frac12(\\ln u+1)$，$f'(1)=\\frac12$，对应选项 B（$f(1)=0$）。"""

NEW[431] = """【答案】$\\dfrac{1}{8\\mathrm e^{2}}$

先定 $(1,1)$ 处的函数值：代入 $x=1,\\ y=1$，$\\int_1^1=0$，得
$$
z+\\ln z=1\\Rightarrow z=1.
$$
方程两边对 $x$ 求导（$y$ 视为常数，$z=z(x,y)$）：
$$
\\frac{\\partial z}{\\partial x}+\\frac{1}{z}\\frac{\\partial z}{\\partial x}-\\mathrm e^{-x^{2}}=0
\\Rightarrow\\left(1+\\frac1z\\right)z_x=\\mathrm e^{-x^{2}}.
$$
代入 $(1,1)$（此时 $z=1$）：$2z_x=\\mathrm e^{-1}$，故 $z_x=\\dfrac{1}{2\\mathrm e}$。

再对 $x$ 求导一次：
$$
\\left(1+\\frac1z\\right)z_{xx}-\\frac{1}{z^{2}}(z_x)^{2}=-2x\\mathrm e^{-x^{2}}.
$$
代入 $x=1,\\ z=1,\\ z_x=\\frac{1}{2\\mathrm e}$：
$$
2z_{xx}-\\frac{1}{4\\mathrm e^{2}}=-2\\mathrm e^{-1}\\cdot 1\\cdot(-1)\\Big|_{x=1}\\Rightarrow
2z_{xx}=\\frac{1}{4\\mathrm e^{2}}.
$$
故 $\\dfrac{\\partial^{2}z}{\\partial x^{2}}\\Big|_{(1,1)}=\\dfrac{1}{8\\mathrm e^{2}}$。"""

NEW[432] = """【答案】$\\dfrac{\\mathrm dz}{\\mathrm dx}=\\dfrac{(f+xf')F'_y-xf'F'_x}{F'_y+xf'F'_z}$

由 $z=xf(x+y)$，对 $x$ 求导：
$$
\\frac{\\mathrm dz}{\\mathrm dx}=f(x+y)+xf'(x+y)\\left(1+\\frac{\\mathrm dy}{\\mathrm dx}\\right).
\\tag{1}
$$
由 $F(x,y,z)=0$，全导数：
$$
F'_x+F'_y\\frac{\\mathrm dy}{\\mathrm dx}+F'_z\\frac{\\mathrm dz}{\\mathrm dx}=0.
\\tag{2}
$$
记 $f=f(x+y),\\ f'=f'(x+y)$。由 (1) 得
$$
\\frac{\\mathrm dz}{\\mathrm dx}=(f+xf')+xf'\\frac{\\mathrm dy}{\\mathrm dx}.
\\tag{1'}
$$
将 $(1')$ 代入 (2)：
$$
F'_x+F'_y\\frac{\\mathrm dy}{\\mathrm dx}+F'_z\\left[(f+xf')+xf'\\frac{\\mathrm dy}{\\mathrm dx}\\right]=0,
$$
解出 $\\dfrac{\\mathrm dy}{\\mathrm dx}=-\\dfrac{F'_x+(f+xf')F'_z}{F'_y+xf'F'_z}$，代回 $(1')$ 整理得
$$
\\frac{\\mathrm dz}{\\mathrm dx}=\\frac{(f+xf')F'_y-xf'F'_x}{F'_y+xf'F'_z}.
$$"""

NEW[471] = """【答案】$\\ln(1+\\sqrt2)-\\ln\\dfrac{1+\\sqrt3}{\\sqrt2}$

先对 $y$ 积分（视 $x$ 为常数，令 $a^{2}=1+x^{2}$）：
$$
\\int_0^1\\frac{y\\,\\mathrm dy}{(1+x^{2}+y^{2})^{3/2}}
=\\left[-\\frac{1}{\\sqrt{1+x^{2}+y^{2}}}\\right]_{y=0}^{1}
=\\frac{1}{\\sqrt{1+x^{2}}}-\\frac{1}{\\sqrt{2+x^{2}}}.
$$
再对 $x$ 积分（用 $\\int\\frac{\\mathrm dx}{\\sqrt{x^{2}+c}}=\\ln\\left(x+\\sqrt{x^{2}+c}\\right)$）：
$$
\\begin{aligned}
I&=\\int_0^1\\frac{\\mathrm dx}{\\sqrt{1+x^{2}}}-\\int_0^1\\frac{\\mathrm dx}{\\sqrt{2+x^{2}}}\\\\
&=\\Big[\\ln\\left(x+\\sqrt{1+x^{2}}\\right)\\Big]_0^1-\\Big[\\ln\\left(x+\\sqrt{2+x^{2}}\\right)\\Big]_0^1\\\\
&=\\ln(1+\\sqrt2)-\\ln\\sqrt2-\\ln(1+\\sqrt3)+\\ln\\sqrt2\\\\
&=\\ln(1+\\sqrt2)-\\ln\\frac{1+\\sqrt3}{\\sqrt2}.
\\end{aligned}
$$"""

# 存疑题（推导结果与既有答案/选项不一致，需人工核对）：本轮只做格式提示，不重写内容
SKIP = {180, 417, 431}

changed = []
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            no = q.get('no')
            if no in NEW and no not in SKIP:
                q['answer'] = NEW[no]
                changed.append(no)

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

print(f'已重写 {len(changed)} 题解析: {sorted(changed)}')
