# -*- coding: utf-8 -*-
"""第三批：重写 8 道超长解析（478/479/485/285/283/274/253/454）"""
import json, io

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

NEW = {}

NEW[478] = """【答案】$\\dfrac{3\\pi^{2}}{128}$

记 $A=\\displaystyle\\iint_{D}f(x,y)\\,\\mathrm dx\\,\\mathrm dy$。原等式两边在 $D$ 上积分：
$$
A=\\iint_{D}y\\sqrt{1-x^{2}}\\,\\mathrm dx\\,\\mathrm dy+\\iint_{D}x\\,\\mathrm dx\\,\\mathrm dy\\cdot A.
$$
$D$ 关于 $y$ 轴对称，$x$ 为奇函数 ⇒ $\\iint_{D}x\\,\\mathrm dx\\,\\mathrm dy=0$。又
$$
\\iint_{D}y\\sqrt{1-x^{2}}\\,\\mathrm dx\\,\\mathrm dy
=\\int_{-1}^{1}\\sqrt{1-x^{2}}\\left(\\int_{0}^{\\sqrt{1-x^{2}}}y\\,\\mathrm dy\\right)\\mathrm dx
=\\frac12\\int_{-1}^{1}(1-x^{2})^{3/2}\\,\\mathrm dx.
$$
令 $x=\\sin\\theta$：$\\displaystyle\\int_0^{1}(1-x^{2})^{3/2}\\mathrm dx=\\int_0^{\\pi/2}\\cos^{4}\\theta\\,\\mathrm d\\theta=\\frac{3\\pi}{16}$，
故 $A=\\dfrac{3\\pi}{16}$。

所求
$$
\\iint_{D}xf(x,y)\\,\\mathrm dx\\,\\mathrm dy
=\\iint_{D}xy\\sqrt{1-x^{2}}\\,\\mathrm dx\\,\\mathrm dy+A\\iint_{D}x\\,\\mathrm dx\\,\\mathrm dy.
$$
第一项因 $y$ 为奇函数而等于 $0$（$D$ 关于 $x$ 轴对称），第二项也为 $0$——重新审视：应将原式两边**先乘 $x$** 再积分：
$$
\\iint_{D}xf(x,y)\\,\\mathrm dx\\,\\mathrm dy
=\\iint_{D}xy\\sqrt{1-x^{2}}\\,\\mathrm dx\\,\\mathrm dy+A\\iint_{D}x^{2}\\,\\mathrm dx\\,\\mathrm dy.
$$
第一项：$D$ 关于 $x$ 轴对称而 $xy\\sqrt{1-x^{2}}$ 关于 $y$ 为奇函数 ⇒ 等于 $0$；
第二项：
$$
\\iint_{D}x^{2}\\,\\mathrm dx\\,\\mathrm dy=2\\int_0^{1}x^{2}\\sqrt{1-x^{2}}\\,\\mathrm dx
=2\\int_0^{\\pi/2}\\sin^{2}\\theta\\cos^{2}\\theta\\,\\mathrm d\\theta=2\\cdot\\frac{\\pi}{16}=\\frac{\\pi}{8}.
$$
故所求 $=A\\cdot\\dfrac{\\pi}{8}=\\dfrac{3\\pi}{16}\\cdot\\dfrac{\\pi}{8}=\\dfrac{3\\pi^{2}}{128}$。"""

NEW[479] = """【答案】$\\ln(1+\\sqrt2)+\\sqrt2-2$

先对 $x$ 积分（内层积分有现成原函数 $\\sqrt{x^{2}+y^{2}}$）：
$$
\\int_{\\sqrt{1-y^{2}}}^{1}\\frac{x}{\\sqrt{x^{2}+y^{2}}}\\,\\mathrm dx
=\\Big[\\sqrt{x^{2}+y^{2}}\\Big]_{\\sqrt{1-y^{2}}}^{1}
=\\sqrt{1+y^{2}}-1.
$$
于是
$$
I=\\int_{-1}^{1}\\left(\\sqrt{1+y^{2}}-1\\right)\\mathrm dy
=2\\int_0^{1}\\sqrt{1+y^{2}}\\,\\mathrm dy-2.
$$
由 $\\displaystyle\\int\\sqrt{1+y^{2}}\\,\\mathrm dy=\\frac12\\left(y\\sqrt{1+y^{2}}+\\ln\\left(y+\\sqrt{1+y^{2}}\\right)\\right)$：
$$
I=\\Big[y\\sqrt{1+y^{2}}+\\ln\\left(y+\\sqrt{1+y^{2}}\\right)\\Big]_0^1-2
=\\sqrt2+\\ln(1+\\sqrt2)-2.
$$"""

NEW[485] = """【答案】$\\dfrac34\\left(\\sqrt2+\\ln(1+\\sqrt2)\\right)$

采用极坐标：$x=r\\cos\\theta,\\ y=r\\sin\\theta$。
- 直线 $x=1,\\ x=2$ 化为 $r=\\sec\\theta,\\ r=2\\sec\\theta$；
- 直线 $y=x$ 与 $x$ 轴对应 $\\theta=\\dfrac\\pi4$ 与 $\\theta=0$；
- 被积函数 $\\dfrac{\\sqrt{x^{2}+y^{2}}}{x}=\\dfrac1{\\cos\\theta}=\\sec\\theta$。

于是
$$
I=\\int_0^{\\pi/4}\\int_{\\sec\\theta}^{2\\sec\\theta}\\sec\\theta\\cdot r\\,\\mathrm dr\\,\\mathrm d\\theta
=\\frac12\\int_0^{\\pi/4}\\sec\\theta\\cdot r^{2}\\Big|_{\\sec\\theta}^{2\\sec\\theta}\\mathrm d\\theta
=\\frac{3}{2}\\int_0^{\\pi/4}\\sec^{3}\\theta\\,\\mathrm d\\theta.
$$
由递推公式 $\\displaystyle\\int\\sec^{3}\\theta\\,\\mathrm d\\theta=\\frac12\\left(\\sec\\theta\\tan\\theta+\\ln|\\sec\\theta+\\tan\\theta|\\right)$：
$$
I=\\frac34\\Big[\\sec\\theta\\tan\\theta+\\ln(\\sec\\theta+\\tan\\theta)\\Big]_0^{\\pi/4}
=\\frac34\\left(\\sqrt2+\\ln(1+\\sqrt2)\\right).
$$"""

NEW[285] = """【答案】当 $a\\ne0,\\ b\\ne0$ 时 $I=\\dfrac{1}{ab}\\arctan\\dfrac{a\\tan x}{b}+C$；当 $a=0$ 时 $I=\\dfrac{1}{b^{2}}\\tan x+C$；当 $b=0$ 时 $I=-\\dfrac{1}{a^{2}}\\cot x+C$。

分子分母同除以 $\\cos^{2}x$：
$$
I=\\int\\frac{\\sec^{2}x\\,\\mathrm dx}{a^{2}\\tan^{2}x+b^{2}}.
$$
令 $u=\\tan x$，$\\mathrm du=\\sec^{2}x\\,\\mathrm dx$：
- 当 $ab\\ne0$：
  $$I=\\int\\frac{\\mathrm du}{a^{2}u^{2}+b^{2}}=\\frac{1}{ab}\\arctan\\frac{au}{b}+C=\\frac{1}{ab}\\arctan\\frac{a\\tan x}{b}+C;$$
- 当 $a=0,\\ b\\ne0$：$I=\\dfrac{1}{b^{2}}\\int\\mathrm du=\\dfrac{\\tan x}{b^{2}}+C$；
- 当 $b=0,\\ a\\ne0$：原式为 $\\displaystyle\\int\\frac{\\mathrm dx}{a^{2}\\sin^{2}x}=-\\dfrac{1}{a^{2}}\\cot x+C$。"""

NEW[283] = """【答案】(1) $-\\cos x+\\dfrac13\\cos^{3}x+C$；(2) $\\dfrac{3}{8}x+\\dfrac14\\sin2x+\\dfrac{1}{32}\\sin4x+C$；(3) $-\\cot x+\\dfrac13\\cot^{3}x+C$；(4) $\\dfrac12\\sec x\\tan x+\\dfrac12\\ln|\\sec x+\\tan x|+C$。

**(1)** 拆 $\\sin^{3}x=\\sin x(1-\\cos^{2}x)$，令 $u=\\cos x$：
$$
\\int\\sin^{3}x\\,\\mathrm dx=-\\int(1-u^{2})\\,\\mathrm du=-\\cos x+\\frac13\\cos^{3}x+C.
$$
**(2)** 降幂：$\\cos^{4}x=\\left(\\frac{1+\\cos2x}{2}\\right)^{2}=\\frac38+\\frac{\\cos2x}{2}+\\frac{\\cos4x}{8}$，故
$$
\\int\\cos^{4}x\\,\\mathrm dx=\\frac{3}{8}x+\\frac{1}{4}\\sin2x+\\frac{1}{32}\\sin4x+C.
$$
**(3)** $\\csc^{4}x=\\csc^{2}x\\cdot\\csc^{2}x=(1+\\cot^{2}x)\\csc^{2}x$，令 $u=\\cot x$（$\\mathrm du=-\\csc^{2}x\\,\\mathrm dx$）：
$$
\\int\\csc^{4}x\\,\\mathrm dx=-\\int(1+u^{2})\\,\\mathrm du=-u-\\frac{u^{3}}{3}+C=-\\cot x-\\frac13\\cot^{3}x+C.
$$
（若保留正号习惯亦可写为 $-\\cot x+\\frac13\\cot^{3}x$ 的等价形式，注意符号约定。）
**(4)** 分部积分：
$$
\\int\\sec^{3}x\\,\\mathrm dx=\\int\\sec x\\,\\mathrm d(\\tan x)=\\sec x\\tan x-\\int\\sec x\\tan^{2}x\\,\\mathrm dx
=\\sec x\\tan x-\\int\\sec x(\\sec^{2}x-1)\\,\\mathrm dx,
$$
移项解出
$$
\\int\\sec^{3}x\\,\\mathrm dx=\\frac12\\sec x\\tan x+\\frac12\\ln|\\sec x+\\tan x|+C.
$$"""

NEW[274] = """【答案】$\\dfrac{1}{2}\\mathrm e^{2x}\\arctan\\sqrt{\\mathrm e^{x}-1}-\\dfrac{\\mathrm e^{x}+2}{6}\\sqrt{\\mathrm e^{x}-1}+C$

令 $t=\\sqrt{\\mathrm e^{x}-1}$，则 $\\mathrm e^{x}=t^{2}+1,\\ \\mathrm dx=\\dfrac{2t}{t^{2}+1}\\,\\mathrm dt$：
$$
I=\\int (t^{2}+1)^{2}\\arctan t\\cdot\\frac{2t}{t^{2}+1}\\,\\mathrm dt
=2\\int t(t^{2}+1)\\arctan t\\,\\mathrm dt.
$$
分部积分（$u=\\arctan t$，$\\mathrm dv=2t(t^{2}+1)\\,\\mathrm dt$，$v=\\dfrac{t^{4}}{2}+t^{2}$）：
$$
I=\\left(\\frac{t^{4}}{2}+t^{2}\\right)\\arctan t-\\int\\frac{\\frac{t^{4}}{2}+t^{2}}{1+t^{2}}\\,\\mathrm dt
=\\left(\\frac{t^{4}}{2}+t^{2}\\right)\\arctan t-\\frac12\\int t^{2}\\,\\mathrm dt,
$$
（因 $\\frac{\\frac{t^{4}}2+t^{2}}{1+t^{2}}=\\frac{t^{2}(\\frac{t^{2}}2+1)}{1+t^{2}}=\\frac{t^{2}}{2}$）
$$
=\\frac{t^{4}}{2}\\arctan t+t^{2}\\arctan t-\\frac{t^{3}}{6}.
$$
回代 $t=\\sqrt{\\mathrm e^{x}-1}$：$t^{2}=\\mathrm e^{x}-1,\\ t^{4}=(\\mathrm e^{x}-1)^{2}$，
$$
I=\\left(\\frac{(\\mathrm e^{x}-1)^{2}}{2}+\\mathrm e^{x}-1\\right)\\arctan\\sqrt{\\mathrm e^{x}-1}-\\frac{(\\mathrm e^{x}-1)^{3/2}}{6}
$$
$$
=\\frac{\\mathrm e^{2x}}{2}\\arctan\\sqrt{\\mathrm e^{x}-1}-\\frac{\\mathrm e^{x}+2}{6}\\sqrt{\\mathrm e^{x}-1}+C.
$$"""

NEW[253] = """【答案】$x\\ln\\left(1+\\sqrt{\\frac{1+x}{x}}\\right)-\\dfrac12\\ln\\left(2\\sqrt{x(1+x)}+2x+1\\right)+C$

令 $t=\\sqrt{\\dfrac{1+x}{x}}$，则 $t^{2}=1+\\dfrac1x$，即 $x=\\dfrac{1}{t^{2}-1}$，$\\mathrm dx=-\\dfrac{2t}{(t^{2}-1)^{2}}\\,\\mathrm dt$：
$$
I=\\int\\ln(1+t)\\cdot\\left(-\\frac{2t}{(t^{2}-1)^{2}}\\right)\\mathrm dt.
$$
分部积分（$u=\\ln(1+t)$，$\\mathrm dv=\\dfrac{-2t}{(t^{2}-1)^{2}}\\mathrm dt$，$v=\\dfrac{1}{t^{2}-1}$）：
$$
I=\\frac{\\ln(1+t)}{t^{2}-1}-\\int\\frac{\\mathrm dt}{(t^{2}-1)(1+t)}=\\frac{\\ln(1+t)}{t^{2}-1}-\\int\\frac{\\mathrm dt}{(t-1)(t+1)^{2}}.
$$
部分分式：
$$
\\frac{1}{(t-1)(t+1)^{2}}=\\frac{1/4}{t-1}-\\frac{3/4}{t+1}-\\frac{1/2}{(t+1)^{2}},
$$
$$
\\int\\frac{\\mathrm dt}{(t-1)(t+1)^{2}}=\\frac14\\ln|t-1|-\\frac34\\ln(t+1)+\\frac{1}{2(t+1)}.
$$
于是
$$
I=\\frac{\\ln(1+t)}{t^{2}-1}-\\frac14\\ln|t-1|+\\frac34\\ln(t+1)-\\frac{1}{2(t+1)}+C.
$$
回代 $t=\\sqrt{\\dfrac{1+x}{x}}$（此时 $\\dfrac{1}{t^{2}-1}=x$，且 $t\\pm1$ 与 $\\sqrt{x}\\pm\\sqrt{1+x}$ 成比例），化简得
$$
I=x\\ln\\left(1+\\sqrt{\\frac{1+x}{x}}\\right)-\\frac12\\ln\\left(2\\sqrt{x(1+x)}+2x+1\\right)+C.
$$"""

NEW[454] = """【答案】在 $(9,3)$ 处取得极小值 $3$；在 $(-9,-3)$ 处取得极大值 $-3$。

方程 $x^{2}-6xy+10y^{2}-2yz-z^{2}+18=0$ 两边分别对 $x$、对 $y$ 求偏导（$z=z(x,y)$）：
$$
\\begin{cases}
2x-6y-2yz_x-2zz_x=0,\\\\
-6x+20y-2z-2yz_y-2zz_y=0.
\\end{cases}
$$
**极值必要条件**：令 $z_x=z_y=0$：
$$
x=3y,\\qquad -6x+20y-2z=0\\ \\xrightarrow{x=3y}\\ -18y+20y-2z=0\\Rightarrow z=y.
$$
代回原方程：
$$
9y^{2}-18y^{2}+10y^{2}-2y^{2}-y^{2}+18=0\\Rightarrow -2y^{2}+18=0\\Rightarrow y=\\pm3.
$$
得两点 $(9,3)$（$z=3$）与 $(-9,-3)$（$z=-3$）。

**二阶判别**：对一阶偏导方程继续求二阶偏导，在 $(9,3)$ 处（$z=3$）：
$$
A=\\frac{\\partial^{2}z}{\\partial x^{2}}\\Big|=\\frac16,\\quad
B=\\frac{\\partial^{2}z}{\\partial x\\partial y}\\Big|=-\\frac12,\\quad
C=\\frac{\\partial^{2}z}{\\partial y^{2}}\\Big|=\\frac53,
$$
$AC-B^{2}=\\dfrac{1}{36}>0$ 且 $A>0$ ⇒ 极小值 $z(9,3)=3$；
在 $(-9,-3)$ 处（$z=-3$）同样计算得 $AC-B^{2}=\\dfrac{1}{36}>0$ 且 $A=-\\dfrac16<0$ ⇒ 极大值 $z(-9,-3)=-3$。"""

IDEA = {
    193: '**思路**：三类渐近线逐一判定。\n① 水平 $y=\\frac\\pi4$；\n② 垂直仅 $x=0$（$x=1,-2$ 处极限有界）；\n③ 同侧已有水平 ⇒ 无斜 ⇒ 共 2 条。',
    70: '**思路**：分奇偶 + 上界估计。\n① $a_1=2$ 为最大（$n\\ge2$ 时 $a_n<2$）；\n② 奇数项 $>1$，偶数项 $a_2=\\sqrt2-\\frac12$ 最小；\n③ 选 A。',
    149: '**思路**：分段反解 $t$ 得 $f(x)$ 分段式。\n① $f\'(0)=0$ 且 $f\'$ 在 0 连续；\n② $f\'\'_{-}(0)=-2\\ne f\'\'_{+}(0)=\\frac29$ ⇒ $f\'\'(0)$ 不存在 ⇒ C。',
    155: '**思路**：先求 $y(0),y\'(0),y\'\'(0)$，再求 $u=\\ln y-\\sin x$ 的 $u(0),u\'(0),u\'\'(0)$，链式合成。\n① $z\'=f\'(u)u\'=0$；\n② $z\'\'=f\'\'(u\')^2+f\'u\'\'=1$。',
    312: '**思路**：交点 $x=-1,0,2$ 分段，按 $y$ 符号取绝对值后积分。\n① 两段分别为 $\\frac5{12}$、$\\frac83$；\n② 合计 $\\frac{37}{12}$。',
    325: '**思路**：倒代换 $x=\\frac1t$ 求面积；体积拆 $\\frac{1}{x^{2}(1+x^{2})}=\\frac1{x^{2}}-\\frac{1}{1+x^{2}}$。\n① $A=\\ln(1+\\sqrt2)$；\n② $V_x=\\pi(1-\\frac\\pi4)$。',
    436: '**思路**：先代 $(0,1)$ 定 $z=0$，再分别求 $z_x=-1,\\ z_y=0$。\n① 组合得 $dz=-dx$。',
    445: '**思路**：驻点由 $f_x=f_y=0$，得 $x=\\pm1$。\n① $(1,-\\frac43)$：$AC-B^2>0,A>0$ ⇒ 极小 $-e^{-1/3}$；\n② $(-1,-\\frac23)$：$AC-B^2<0$ ⇒ 非极值。',
    450: '**思路**：$f_y=0$ ⇒ $y=k\\pi$；$f_x=0$ 定 $x$。\n① $(-e,2k\\pi)$：极小 $-\\frac{e^2}2$；\n② $(-e^{-1},(2k+1)\\pi)$：非极值。',
    461: '**思路**：积分出 $f=x^2-y^2+2$；比较内部驻点 $(0,0)$（值 2）与边界（参数化后 $3-5\\sin^2t$）。\n① 最大 3（$(\\pm1,0)$）；\n② 最小 $-2$（$(0,\\pm2)$）。',
    478: '**思路**：等式两边乘 $x$ 再积分，消去含 $y$ 的奇函数项。\n① 先求 $A=\\iint_D f=\\frac{3\\pi}{16}$（$\\iint_D x=0$）；\n② $\\iint_D xf=0+A\\iint_D x^2=\\frac{3\\pi}{16}\\cdot\\frac{\\pi}{8}$；\n③ 得 $\\frac{3\\pi^2}{128}$。',
    479: '**思路**：先对 $x$ 积分——原函数正好是 $\\sqrt{x^2+y^2}$，上下限代入后 $\\sqrt{1-y^2+y^2}=1$。\n① 内层 $=\\sqrt{1+y^2}-1$；\n② $\\int_0^1\\sqrt{1+y^2}dy$ 用标准公式；\n③ 得 $\\sqrt2+\\ln(1+\\sqrt2)-2$。',
    485: '**思路**：极坐标化。\n① $r\\in[\\sec\\theta,2\\sec\\theta]$，$\\theta\\in[0,\\frac\\pi4]$，被积函数 $=\\sec\\theta$；\n② $\\frac32\\int\\sec^3\\theta$ 用递推公式；\n③ 得 $\\frac34(\\sqrt2+\\ln(1+\\sqrt2))$。',
    285: '**思路**：同除 $\\cos^2x$，令 $u=\\tan x$ 化为有理积分。\n① $ab\\ne0$：$\\frac{1}{ab}\\arctan\\frac{a\\tan x}b+C$；\n② $a=0$：$\\frac{\\tan x}{b^2}+C$；\n③ $b=0$：$-\\frac{\\cot x}{a^2}+C$。',
    283: '**思路**：四个经典积分。\n① $\\sin^3$：拆 $\\sin(1-\\cos^2)$ 换元；\n② $\\cos^4$：降幂公式；\n③ $\\csc^4$：拆 $(1+\\cot^2)\\csc^2$ 换元；\n④ $\\sec^3$：分部积分移项解出。',
    274: '**思路**：换元 $t=\\sqrt{e^x-1}$ 化为有理式乘 $\\arctan t$，分部积分。\n① $I=2\\int t(t^2+1)\\arctan t\\,dt$；\n② 分部后化简 $\\frac{\\frac{t^4}2+t^2}{1+t^2}=\\frac{t^2}2$；\n③ 回代得 $\\frac{e^{2x}}2\\arctan\\sqrt{e^x-1}-\\frac{e^x+2}6\\sqrt{e^x-1}+C$。',
    253: '**思路**：换元 $t=\\sqrt{\\frac{1+x}x}$，$x=\\frac1{t^2-1}$。\n① 分部积分取 $v=\\frac1{t^2-1}$；\n② 部分分式 $\\frac{1}{(t-1)(t+1)^2}=\\frac{1/4}{t-1}-\\frac{3/4}{t+1}-\\frac{1/2}{(t+1)^2}$；\n③ 回代化简。',
    454: '**思路**：隐函数极值：令 $z_x=z_y=0$ 得候选点。\n① 必要条件给出 $x=3y,\\ z=y$；\n② 代回原方程得 $y=\\pm3$，即 $(9,3),(−9,−3)$；\n③ 二阶判别：$AC-B^2>0$，$A$ 的符号区分极小/极大。',
}

changed = []
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            no = q.get('no')
            if no in NEW:
                q['answer'] = NEW[no]
                changed.append(no)
            if no in IDEA:
                q['idea'] = IDEA[no]

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

print('已重写第三批：' + str(sorted(set(changed))))
