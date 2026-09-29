# -*- coding: utf-8 -*-
"""第二批 A：重写 10 道超长解析（193/70/149/155/312/325/436/445/450/461）"""
import json, io

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

NEW = {}

NEW[193] = """【答案】B

**水平渐近线**：$x\\to\\pm\\infty$ 时 $\\mathrm e^{1/x^{2}}\\to1$，$\\arctan\\frac{x^{2}+x+1}{(x-1)(x+2)}\\to\\arctan1=\\frac\\pi4$，故
$$
\\lim_{x\\to\\pm\\infty}y=\\frac{\\pi}{4}\\Rightarrow y=\\frac{\\pi}{4}\\ \\text{（1 条）}.
$$

**垂直渐近线**：
- $x\\to0$：$\\mathrm e^{1/x^{2}}\\to+\\infty$，而 $\\arctan\\frac{1}{(-1)(2)}=\\arctan(-\\tfrac12)\\ne0$，故 $y\\to\\infty$，$x=0$ 是垂直渐近线；
- $x\\to1$ 或 $x\\to-2$：分母 $(x-1)(x+2)\\to0$，$\\arctan$ 内趋于 $\\pm\\infty$，故 $\\arctan\\to\\pm\\frac\\pi2$，而 $\\mathrm e^{1/x^{2}}$ 趋于有限常数，极限有界，均**不是**垂直渐近线。

**斜渐近线**：$x\\to\\pm\\infty$ 方向已存在水平渐近线，同一方向不再有斜渐近线。

综上共 **2 条**渐近线，选 B。"""

NEW[70] = """【答案】A

记 $a_n=n^{1/n}-\\frac{(-1)^{n}}{n}$，即
$$
a_n=\\begin{cases}n^{1/n}+\\dfrac1n,& n\\ \\text{为奇数},\\\\[4pt] n^{1/n}-\\dfrac1n,& n\\ \\text{为偶数}.\\end{cases}
$$

**最大值**：$a_1=1+\\frac11=2$。当 $n\\ge2$ 时 $n^{1/n}\\le\\sqrt2<1.5$，且 $\\frac1n\\le\\frac12$，故 $a_n<2$。所以最大值为 $a_1=2$。

**最小值**：奇数项 $a_n=n^{1/n}+\\frac1n>1$（$n\\ge3$）；偶数项 $a_2=\\sqrt2-\\frac12\\approx0.914$，而 $n\\ge4$ 的偶数项满足 $n^{1/n}-\\frac1n\\ge\\sqrt[4]4-\\frac14>1$。故最小值为 $a_2=\\sqrt2-\\dfrac12$。

因此数列既有最大值又有最小值，选 A。"""

NEW[149] = """【答案】C

由 $x=2t+|t|$ 得 $x=\\begin{cases}3t,&t\\ge0,\\\\ t,&t<0,\\end{cases}$ 故 $t=\\begin{cases}\\frac x3,&x\\ge0,\\\\ x,&x<0,\\end{cases}$ 于是
$$
y=f(x)=\\begin{cases}\\dfrac{x}{3}\\sin\\dfrac{x}{3},& x\\ge0,\\\\[6pt] -x\\sin x,& x<0.\\end{cases}
$$

**一阶导**：
$$
f'(x)=\\begin{cases}\\dfrac13\\sin\\dfrac x3+\\dfrac x9\\cos\\dfrac x3,& x>0,\\\\[6pt] -\\sin x-x\\cos x,& x<0,\\end{cases}
\\qquad f'(0)=\\lim_{x\\to0}\\frac{f(x)-0}{x}=0.
$$
且 $x\\to0^{\\pm}$ 时 $f'(x)\\to0$，故 $f'(x)$ 在 $x=0$ 处连续。

**二阶导**：
$$
f''_{-}(0)=\\lim_{x\\to0^-}\\frac{-\\sin x-x\\cos x}{x}=-1-1=-2,\\qquad
f''_{+}(0)=\\lim_{x\\to0^+}\\frac{\\frac13\\sin\\frac x3+\\frac x9\\cos\\frac x3}{x}=\\frac19+\\frac19=\\frac29.
$$
左右不等，故 $f''(0)$ 不存在。选 C。"""

NEW[155] = """【答案】$\\left.\\dfrac{\\mathrm dz}{\\mathrm dx}\\right|_{x=0}=0$，$\\left.\\dfrac{\\mathrm d^{2}z}{\\mathrm dx^{2}}\\right|_{x=0}=1$

**第一步：求 $y(0),y'(0),y''(0)$**。方程 $y-x\\mathrm e^{y-1}=1$ 中令 $x=0$ 得 $y(0)=1$。
两边对 $x$ 求导：
$$
y'-\\mathrm e^{y-1}-x\\mathrm e^{y-1}y'=0\\Rightarrow y'(0)=1.
$$
再求导：
$$
y''-\\mathrm e^{y-1}y'-\\mathrm e^{y-1}y'-x\\mathrm e^{y-1}(y')^{2}-x\\mathrm e^{y-1}y''=0
\\Rightarrow y''(0)=2\\mathrm e^{0}y'(0)=2.
$$

**第二步：求 $u=\\ln y-\\sin x$ 在 $x=0$ 处的导数**。
$$
u(0)=0,\\qquad u'=y'/y-\\cos x\\Rightarrow u'(0)=1-1=0,
$$
$$
u''=\\frac{y''y-(y')^{2}}{y^{2}}+\\sin x\\Rightarrow u''(0)=\\frac{2\\cdot1-1}{1}=1.
$$

**第三步：复合求导**。$z=f(u)$，故
$$
\\frac{\\mathrm dz}{\\mathrm dx}=f'(u)u'\\Rightarrow\\left.\\frac{\\mathrm dz}{\\mathrm dx}\\right|_{0}=f'(0)\\cdot0=0;
$$
$$
\\frac{\\mathrm d^{2}z}{\\mathrm dx^{2}}=f''(u)(u')^{2}+f'(u)u''\\Rightarrow\\left.\\frac{\\mathrm d^{2}z}{\\mathrm dx^{2}}\\right|_{0}=f''(0)\\cdot0+f'(0)\\cdot1=1.
$$"""

NEW[312] = """【答案】$\\dfrac{37}{12}$

**求交点**：$y=-x^{3}+x^{2}+2x=-x(x-2)(x+1)=0$，得 $x=-1,\\,0,\\,2$。
在区间 $(-1,0)$ 上 $y<0$，在 $(0,2)$ 上 $y>0$，故
$$
A=\\int_{-1}^{0}(-y)\\,\\mathrm dx+\\int_{0}^{2}y\\,\\mathrm dx.
$$
**第一段**：
$$
\\int_{-1}^{0}(x^{3}-x^{2}-2x)\\,\\mathrm dx=\\left[\\frac{x^{4}}{4}-\\frac{x^{3}}{3}-x^{2}\\right]_{-1}^{0}=-\\left(\\frac14+\\frac13-1\\right)=\\frac{5}{12}.
$$
**第二段**：
$$
\\int_{0}^{2}(-x^{3}+x^{2}+2x)\\,\\mathrm dx=\\left[-\\frac{x^{4}}{4}+\\frac{x^{3}}{3}+x^{2}\\right]_{0}^{2}=-4+\\frac83+4=\\frac83.
$$
**合计**：$A=\\dfrac{5}{12}+\\dfrac83=\\dfrac{5+32}{12}=\\dfrac{37}{12}$。"""

NEW[325] = """【答案】（I）$\\ln(1+\\sqrt2)$；（II）$V_x=\\pi\\left(1-\\dfrac{\\pi}{4}\\right)$

**(I) 面积**：
$$
A=\\int_1^{+\\infty}\\frac{\\mathrm dx}{x\\sqrt{1+x^{2}}}.
$$
令 $x=\\dfrac1t$（$t:1\\to0$），则
$$
A=\\int_0^1\\frac{\\mathrm dt}{\\sqrt{1+t^{2}}}=\\Big[\\ln\\left(t+\\sqrt{1+t^{2}}\\right)\\Big]_0^1=\\ln(1+\\sqrt2).
$$

**(II) 旋转体体积**（绕 $x$ 轴）：
$$
V_x=\\pi\\int_1^{+\\infty}y^{2}\\,\\mathrm dx=\\pi\\int_1^{+\\infty}\\frac{\\mathrm dx}{x^{2}(1+x^{2})}
=\\pi\\int_1^{+\\infty}\\left(\\frac{1}{x^{2}}-\\frac{1}{1+x^{2}}\\right)\\mathrm dx
$$
$$
=\\pi\\left[-\\frac1x-\\arctan x\\right]_1^{+\\infty}=\\pi\\left[0-\\left(-1-\\frac\\pi4\\right)\\right]=\\pi\\left(1-\\frac\\pi4\\right).
$$"""

NEW[436] = """【答案】$-\\mathrm dx$

**定函数值**：代入 $x=0,\\ y=1$ 得 $\\mathrm e^{z}+0+0+\\cos0=2$，即 $\\mathrm e^{z}=1$，故 $z=0$。

**对 $x$ 求偏导**：
$$
\\mathrm e^{z}z_x+yz+xy z_x+1-\\sin x=0.
$$
代入 $(0,1),\\ z=0$：$z_x+0+0+1-0=0$，故 $z_x=-1$。

**对 $y$ 求偏导**：
$$
\\mathrm e^{z}z_y+xz+xy z_y=0.
$$
代入 $(0,1),\\ z=0$：$z_y+0+0=0$，故 $z_y=0$。

因此
$$
\\mathrm dz\\big|_{(0,1)}=z_x\\,\\mathrm dx+z_y\\,\\mathrm dy=-\\mathrm dx.
$$"""

NEW[445] = """【答案】在 $\\left(1,-\\dfrac43\\right)$ 处取得极小值 $-\\mathrm e^{-1/3}$

$$
f_x=\\left(x^{2}+y+\\frac{x^{3}}{3}\\right)\\mathrm e^{x+y},\\qquad
f_y=\\left(1+y+\\frac{x^{3}}{3}\\right)\\mathrm e^{x+y}.
$$
令 $f_x=f_y=0$（$\\mathrm e^{x+y}>0$）：
$$
x^{2}+y+\\frac{x^{3}}{3}=0,\\qquad 1+y+\\frac{x^{3}}{3}=0\\Rightarrow x^{2}-1=0\\Rightarrow x=\\pm1.
$$
- $x=1$：$y=-\\dfrac43$；
- $x=-1$：$y=-\\dfrac23$。

**二阶判别**（驻点处 $B=f_{xy}$ 计算略，直接代入 $A=f_{xx},\\ C=f_{yy}$）：
在 $\\left(1,-\\frac43\\right)$ 处 $AC-B^{2}>0$ 且 $A>0$，为极小值点，
$$
f\\left(1,-\\tfrac43\\right)=\\left(-\\tfrac43+\\tfrac13\\right)\\mathrm e^{1-\\frac43}=-\\mathrm e^{-1/3};
$$
在 $\\left(-1,-\\frac23\\right)$ 处 $AC-B^{2}<0$，不是极值点。

故 $f$ 仅在 $\\left(1,-\\frac43\\right)$ 处取极小值 $-\\mathrm e^{-1/3}$。"""

NEW[450] = """【答案】在 $(-\\mathrm e,\\,2k\\pi)\\ (k\\in\\mathbb Z)$ 处取得极小值 $-\\dfrac{\\mathrm e^{2}}{2}$

$$
f_x=\\mathrm e^{\\cos y}+x,\\qquad f_y=-x\\sin y\\,\\mathrm e^{\\cos y}.
$$
令 $f_y=0$：$x=0$ 或 $\\sin y=0$。若 $x=0$，则 $f_x=\\mathrm e^{\\cos y}>0$，矛盾；故 $\\sin y=0$，即 $y=k\\pi$。
- $y=2k\\pi$（$\\cos y=1$）：$f_x=\\mathrm e+x=0\\Rightarrow x=-\\mathrm e$；
- $y=(2k+1)\\pi$（$\\cos y=-1$）：$f_x=\\mathrm e^{-1}+x=0\\Rightarrow x=-\\mathrm e^{-1}$。

**二阶判别**：$A=f_{xx}=1$，$B=f_{xy}=-\\sin y\\,\\mathrm e^{\\cos y}=0$（驻点处），
$C=f_{yy}=-x\\cos y\\,\\mathrm e^{\\cos y}$（驻点处 $\\sin y=0$）。
- $(-\\mathrm e,\\,2k\\pi)$：$C=\\mathrm e\\cdot1\\cdot\\mathrm e=\\mathrm e^{2}>0$，$AC-B^{2}=\\mathrm e^{2}>0$ 且 $A>0$ ⇒ 极小值，
  $$f(-\\mathrm e,\\,2k\\pi)=-\\mathrm e\\cdot\\mathrm e+\\frac{\\mathrm e^{2}}{2}=-\\frac{\\mathrm e^{2}}{2};$$
- $(-\\mathrm e^{-1},\\,(2k+1)\\pi)$：$C=-\\mathrm e^{-2}<0$，$AC-B^{2}<0$ ⇒ 不是极值点。

故极小值为 $-\\dfrac{\\mathrm e^{2}}{2}$。"""

NEW[461] = """【答案】最大值为 $3$，最小值为 $-2$

由 $\\mathrm dz=2x\\,\\mathrm dx-2y\\,\\mathrm dy$ 得 $f_x=2x,\\ f_y=-2y$，积分得
$$
f(x,y)=x^{2}-y^{2}+C.
$$
由 $f(1,1)=2$ 得 $1-1+C=2$，故 $C=2$，即 $f(x,y)=x^{2}-y^{2}+2$。

**内部**：驻点 $(0,0)$（在椭圆域内），$f(0,0)=2$。

**边界** $x^{2}+\\dfrac{y^{2}}{4}=1$：取参数 $x=\\cos t,\\ y=2\\sin t$，则
$$
f=\\cos^{2}t-4\\sin^{2}t+2=3-5\\sin^{2}t,
$$
其最大值为 $3$（$\\sin t=0$，即 $(\\pm1,0)$），最小值为 $-2$（$\\sin^{2}t=1$，即 $(0,\\pm2)$）。

比较内部值 $2$，故最大值为 $3$，最小值为 $-2$。"""

IDEA = {
    193: '**思路**：三类渐近线分别找。\n① 水平：$x\\to\\pm\\infty$ 得 $y=\\frac\\pi4$；\n② 垂直：只有 $x=0$（其余可疑点极限有界）；\n③ 斜：同向已有水平渐近线则无斜渐近线 ⇒ 共 2 条。',
    70: '**思路**：分奇偶项讨论，注意 $n^{1/n}$ 在 $n\\ge2$ 时不超过 $\\sqrt2$。\n① 奇数项 $a_n=n^{1/n}+\\frac1n>1$，偶数项 $a_n=n^{1/n}-\\frac1n$；\n② $a_1=2$ 为最大（其余项 $<2$）；\n③ $a_2=\\sqrt2-\\frac12$ 为最小（其余项 $>1$）⇒ A。',
    149: '**思路**：由 $x=2t+|t|$ 分段反解 $t$，写出 $f(x)$ 的分段式再判导数。\n① $f(x)=\\frac x3\\sin\\frac x3(x\\ge0)$、$-x\\sin x(x<0)$；\n② $f\'(0)=0$ 且 $f\'$ 连续；\n③ $f\'\'_{-}(0)=-2\\ne f\'\'_{+}(0)=\\frac29$ ⇒ $f\'\'(0)$ 不存在 ⇒ C。',
    155: '**思路**：先由隐函数求 $y(0),y\'(0),y\'\'(0)$，再复合求导。\n① $y(0)=1,\\ y\'(0)=1,\\ y\'\'(0)=2$；\n② $u=\\ln y-\\sin x$：$u(0)=0,\\ u\'(0)=0,\\ u\'\'(0)=1$；\n③ $z\'=f\'u\'=0$，$z\'\'=f\'\'(u\')^2+f\'u\'\'=1$。',
    312: '**思路**：先求交点定区间，再按符号分段积分。\n① 交点 $x=-1,0,2$；\n② $(-1,0)$ 上 $y<0$ 取 $-y$，$(0,2)$ 上 $y>0$；\n③ 两段分别为 $\\frac5{12}$ 与 $\\frac83$，合计 $\\frac{37}{12}$。',
    325: '**思路**：反常积分用倒代换 $x=\\frac1t$。\n① 面积 $=\\int_0^1\\frac{dt}{\\sqrt{1+t^2}}=\\ln(1+\\sqrt2)$；\n② 体积 $=\\pi\\int_1^\\infty(\\frac1{x^2}-\\frac1{1+x^2})dx=\\pi(1-\\frac\\pi4)$。',
    436: '**思路**：先定 $z$ 值，再分别求 $z_x,z_y$。\n① 代入 $(0,1)$ 得 $z=0$；\n② 对 $x$ 求导得 $z_x=-1$，对 $y$ 求导得 $z_y=0$；\n③ $dz=-dx$。',
    445: '**思路**：求驻点后用 $AC-B^2$ 判别。\n① $f_x=f_y=0$ ⇒ $x=\\pm1$，对应 $y=-\\frac43$ 与 $-\\frac23$；\n② $(1,-\\frac43)$：$AC-B^2>0,A>0$ ⇒ 极小 $-e^{-1/3}$；\n③ $(-1,-\\frac23)$：$AC-B^2<0$ ⇒ 非极值。',
    450: '**思路**：由 $f_y=0$ 先定 $y=k\\pi$，再由 $f_x=0$ 定 $x$。\n① 驻点 $(-\\mathrm e,2k\\pi)$ 与 $(-\\mathrm e^{-1},(2k+1)\\pi)$；\n② 前者 $AC-B^2>0,A>0$ ⇒ 极小 $-\\frac{e^2}2$；\n③ 后者 $AC-B^2<0$ ⇒ 非极值。',
    461: '**思路**：由全微分积分出 $f$，再比较内部驻点与边界。\n① $f=x^2-y^2+2$（由 $f(1,1)=2$ 定常数）；\n② 内部驻点 $(0,0)$：$f=2$；\n③ 边界参数化后 $f=3-5\\sin^2t$ ⇒ 最大 3、最小 $-2$。',
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

print('已重写第二批 A：' + str(sorted(set(changed))))
