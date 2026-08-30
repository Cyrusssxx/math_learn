# -*- coding: utf-8 -*-
"""好题点睛 批次2 —— 好题9~好题12 共 32 题
四段规范：gs 公式 / yc 易错 / jq 技巧 / zy 注意（与真题 tips 同源）
"""

TIPS = {

"好题9-微分概念问题": {
1: {
 "gs": r"$f$ 在 $x_0$ 二阶可导 $\Rightarrow f'(x)$ 在 $x_0$ 连续，故 $\lim\limits_{x\to x_0}f'(x)=f'(x_0)>0\Rightarrow$ 存在 $\delta>0$ 使 $x\in(x_0-\delta,x_0+\delta)$ 时 $f'(x)>0$。",
 "jq": r"判「一点导数值 $\to$ 邻域性质」：单调性只需 $f'(x)$ 连续（二阶可导已保证）；凹凸性需 $f''(x)$ 连续，题干只给 $f''(x_0)$ 存在，不够。",
 "yc": r"A 反例 $f(x)=x^3$（单调增但 $f'(0)=0$）；C 反例 $f(x)=x^4$（凹但 $f''(0)=0$）；D 错在 $f''(x_0)>0$ 只说明该点为正，推不出邻域保凹。",
 "zy": r"选 (B)。D 反例 $f(x)=x^4\sin\dfrac1x+\dfrac{x^2}{4}$，$f''(0)=\dfrac12>0$ 但 $f''(x)$ 在 0 附近振荡变号，邻域不保凹。",
},
},

"好题10-导数的应用": {
1: {
 "gs": r"曲率 $K=\dfrac{|y''|}{\left[1+(y')^2\right]^{3/2}}$；曲率圆与曲线在该点同切线、同曲率、同凹凸性，故 $y''(1)=-2<0$。",
 "jq": r"由 $f''$ 不变号 $+y''(1)<0$ 推出 $(1,2)$ 上 $f''<0\Rightarrow f'$ 递减，又 $f'(1)=-1<0\Rightarrow f'<0\Rightarrow f$ 单调减（无极值）；再用拉氏中值 $f(2)\le f(1)-1=0$ 判零点。",
 "yc": r"切线斜率由曲率圆法线方向推：$x^2+y^2=2$ 在 $(1,1)$ 法线斜率 1，故切线斜率 $-1$，不是直接读导数。",
 "zy": r"选 (B)：无极值点，有零点。",
},
2: {
 "gs": r"$f(x)=\ln|x-1|+\ln|x-2|+\ln|x-3|$，$f'(x)=\dfrac{3x^2-12x+11}{(x-1)(x-2)(x-3)}$，驻点即分子二次式零点。",
 "jq": r"法二更巧：令 $g=(x-1)(x-2)(x-3)$，则 $f'=\dfrac{g'}{g}$，$f'=0\Leftrightarrow g'=0$；罗尔定理知 $g'$ 在 $(1,2),(2,3)$ 各一零点，且 $g'$ 为二次式至多两零点。",
 "yc": r"驻点定义在函数定义域内（即 $x\neq1,2,3$），只看分子根不数分母零点；判别式 $\Delta>0$ 得两实根。",
 "zy": r"选 (C)：2 个驻点。",
},
3: {
 "gs": r"$x>2$ 时 $\left[\dfrac2x\right]=0\Rightarrow\lim\limits_{x\to+\infty}f(x)=0$（水平渐近线）；$x<-2$ 时 $\left[\dfrac2x\right]=-1\Rightarrow k=-1,b=0$（斜渐近线 $y=-x$）。",
 "jq": r"取整函数分段处理：按 $\left|\dfrac2x\right|$ 与 1、0 的比较切区间；$x\to0$ 时 $\lim\limits_{x\to0}x\left[\dfrac2x\right]=2$（极限存在，不产生渐近线）。",
 "yc": r"「极限存在」不产生铅直渐近线：$\lim\limits_{x\to0}f(x)=2$ 只是普通极限，不是无穷。",
 "zy": r"选 (B)：共 2 条渐近线。",
},
4: {
 "gs": r"$f''(x)>0\Rightarrow f$ 凹（下凸），弦在曲线上方：$f(x)\le(1-a)x+a$，$a=f(0)$；积分得 $0<\int_0^1f<\dfrac12(1+a)\Rightarrow a>-1$。",
 "jq": r"用「弦函数」（线性插值）从上方控制凹函数，再积分推出 $f(0)$ 下界。",
 "yc": r"结论只保证 $f(0)>-1$ 严格不等；反例 $f=5(x-\frac12)^2-\frac14$ 使 $f(\frac12)<0$，故 (C)(D) 错。",
 "zy": r"选 (B)。",
},
5: {
 "gs": r"$f'(x)=a+2x\sin\dfrac1x-\cos\dfrac1x$，$2x\sin\dfrac1x\to0$（无穷小×有界量），主导项 $a-\cos\dfrac1x$。",
 "jq": r"分 $a\ge1$ 与 $0<a<1$ 讨论：$a\ge1$ 时 $f'>0$ 单调增；$0<a<1$ 时取 $x=\dfrac1{2n\pi}$ 与 $x=\dfrac1{2n\pi+\pi/2}$ 使 $f'$ 异号，不单调。",
 "yc": r"「$a>0$」未给大小，必须分类——是否单调与 $a$ 有关，不能一眼判定。",
 "zy": r"选 (D)。",
},
6: {
 "gs": r"按 $u$ 与 $x^3$ 大小拆积分；求导后变限项相消得 $f'(x)=3x^2\!\left(\int_{-x^3}^{x^3}e^{u^2}\,\mathrm du\right)$（$u=-t$ 对称化）。",
 "jq": r"绝对值积分求导标准动作：先去掉绝对值分段，再对两段分别求导，交叉项恰好抵消；单调性由被积函数恒正定。",
 "yc": r"换元 $u=-t$ 把 $\int_{-1}^{x^3}e^{u^2}\mathrm du$ 变成 $\int_{-x^3}^{1}e^{t^2}\mathrm dt$，抵消后只剩 $[-x^3,x^3]$ 一段。",
 "zy": r"最小值 $f(0)=\int_{-1}^1|u|e^{u^2}\,\mathrm du=e-1$。",
},
7: {
 "gs": r"$x_0\neq0$ 时 $f''(x_0)=\dfrac{e^{x_0}-x_0-1}{x_0^2}>0$（极小）；$x_0=0$ 时取极限 $f''(0)-3f''(0)=\lim\limits_{x\to0}\dfrac{e^x-x-1}{x^2}=\dfrac12\Rightarrow f''(0)=-\dfrac14<0$（极大）。",
 "jq": r"驻点 $x_0$ 分是否为零讨论：$x_0=0$ 不能代原方程，需对 $\dfrac{f''-3f'/x}{}$ 两边取极限用导数定义。",
 "yc": r"$e^x-x-1>0\ (x\neq0)$ 是常用不等式，分子恒正；$x_0=0$ 时第二充分条件的公式失效需代极限。",
 "zy": r"选 (C)：可能极大也可能极小。",
},
8: {
 "gs": r"先求 $y=f(x)$ 斜渐近线：$a=\lim\limits_{x\to+\infty}\dfrac{f(x)}{x}=1$，$b=\lim\limits_{x\to+\infty}(f(x)-x)=-2\Rightarrow y=x-2$；反函数关于 $y=x$ 对称，故 $x=y-2$ 即 $y=x+2$。",
 "jq": r"反函数渐近线对称法：先求原曲线 $y=x-2$，反函数渐近线为 $x=y-2$ 改写；避免直接求反函数（通常求不出显式）。",
 "yc": r"$\ln(e^{x^2}+1)=\ln e^{x^2}+o(1)=x^2+o(1)$，别把 $+1$ 当主项；斜渐近线两条互相关 $y=x\pm2$。",
 "zy": r"$y=x+2$。",
},
9: {
 "gs": r"换元 $u=x-t$：$F(x)=x\int_0^x\cos^3u\,\mathrm du-\int_0^xu\cos^3u\,\mathrm du$；$F'(x)=\int_0^x\cos^3u\,\mathrm du=\sin x-\dfrac13\sin^3x$，$F''(x)=\cos^3x$。",
 "jq": r"卷积型变限积分先换元拆成普通积分；分段（$0\le x\le\pi$ 与 $x>\pi$）后分段求导，再判极值/拐点。",
 "yc": r"$x>\pi$ 时 $\int_0^\pi\cos^3u\,\mathrm du=0\Rightarrow F'(x)\equiv0$（无极值）；拐点看 $F''$ 在 $x=\pi/2$ 两侧变号。",
 "zy": r"选 (B)：无极值点，有拐点。",
},
10: {
 "gs": r"配方 $f(x)=\begin{cases}x-1+\dfrac1{x+1},&x\ge0,\\ 1-x-\dfrac1{x+1},&x<0.\end{cases}$；$f''(x)=\begin{cases}2(x+1)^{-3},&x\ge0,\\ -2(x+1)^{-3},&x<0.\end{cases}$",
 "jq": r"含 $|x|$ 先化成分段，再多项式除法化简求导最高效；渐近线分别算 $x\to-1$（铅直）、$x\to\pm\infty$（两条斜）。",
 "yc": r"斜渐近线左右极限不同：$x\to+\infty$ 得 $y=x-1$，$x\to-\infty$ 得 $y=-x+1$，共 3 条；凹区间 $(-\infty,-1)\cup(0,+\infty)$，凸区间 $(-1,0)$。",
 "zy": r"3 条渐近线：$x=-1$、$y=x-1$、$y=-x+1$。",
},
11: {
 "gs": r"泰勒：$e^{x/2}\ln(1+x)=x+\dfrac{5x^3}{24}+o(x^3)$；故 $f(0)=1$ 连续，$f'(0)=0$（由极限 $\dfrac{5x^3/24+o(x^3)}{x^2}\to0$），$f(x)=1+\dfrac{5x^2}{24}+o(x^2)$ 取极小。",
 "jq": r"三步法：先连续性（排除 A）→ 导数定义求 $f'(0)$（排除 D）→ 用泰勒展开 $f(x)$ 读 $x^2$ 项系数判极值（排除 B）。",
 "yc": r"$f'(0)=0$ 是关键中间结论；判极值用 $f(x)-f(0)$ 的二阶展开而非二阶导公式（因含 $|x|$ 不可用公式）。",
 "zy": r"选 (C)：取极小值。",
},
12: {
 "gs": r"$f'(x)=(x^2-3x+a)e^x$ 无零点 $\Rightarrow\Delta=9-4a\le0\Rightarrow a\ge\dfrac94$；$f''(x)=(x^2-x+a-3)e^x$ 有零点 $\Rightarrow\Delta=1-4(a-3)>0\Rightarrow a<\dfrac{13}{4}$。",
 "jq": r"无极值点 $\iff f'(x)$ 不变号 $\iff$ 二次式判别式 $\le0$；有拐点 $\iff f''(x)$ 变号 $\iff$ 二次式判别式 $>0$。",
 "yc": r"极值要求 $f'(x)=0$ 且变号；这里「无极值点」是恒非负/非正，故判别式取 $\le0$ 而非 $>0$；拐点要求 $f''$ 严格变号故 $>0$。",
 "zy": r"$a\in\left[\dfrac94,\dfrac{13}{4}\right)$。",
},
},

"好题11-微分证明": {
1: {
 "gs": r"（Ⅰ）辅助函数 $\varphi(x)=f(x)-f(a)-\dfrac{f(b)-f(a)}{b-a}(x-a)$，罗尔定理得 $\varphi'(\xi)=0\Rightarrow$ 拉格朗日中值定理。（Ⅱ）$f'_+(0)=\lim\limits_{x\to0^+}\dfrac{f(x)-f(0)}{x}\xlongequal{\text{拉/洛}}A$。",
 "jq": r"（Ⅱ）两法：拉氏中值 $f(x)-f(0)=f'(\xi_x)x$ 取极限；或洛必达 $\lim\dfrac{f(x)-f(0)}{x}=\lim f'(x)=A$。",
 "yc": r"几何意义：$\varphi(x)$ 是曲线与弦 $AB$ 的纵坐标差；单侧导数存在须左右极限相等，这里只用右极限配合 $\lim f'(x)=A$。",
 "zy": r"（Ⅰ）经典构造；（Ⅱ）结论 $f'_+(0)=A$（导数极限定理的半侧版本）。",
},
2: {
 "gs": r"证 $f(x)$ 在 $(0,+\infty)$ 内取正最大值：取 $x_1>0$ 使 $f(x_1)>0$，由 $\lim\limits_{x\to+\infty}f(x)=0$ 取 $M>x_1$ 使 $x>M$ 时 $|f(x)|<f(x_1)$，则 $[0,M]$ 上最大值点 $\xi$ 为内点且 $f'(\xi)=0$。",
 "jq": r"「无穷远趋于 0 + 某点为正」 $\Rightarrow$ 必在有限区间内部取正最大值，直接套费马/罗尔。",
 "yc": r"须说明 $f(x)\not\equiv0$ 且 $\xi$ 是内点（因 $f(\xi)\ge f(0)=0$，且 $f(\xi)\ge f(x_1)>0=f(0)$ 挡住端点）。",
 "zy": r"本题是罗尔定理在无穷区间的推广。",
},
3: {
 "gs": r"令 $x=\lambda x_1+(1-\lambda)x_2$，对 $[x_1,x]$、$[x,x_2]$ 分别用拉氏中值定理，两式相减配出 $\lambda f(x_1)+(1-\lambda)f(x_2)-f(x)=\lambda(1-\lambda)(x_2-x_1)\bigl[f'(\xi_1)-f'(\xi_2)\bigr]$。",
 "jq": r"严格凸的等价刻画：$f'$ 严格增 $\Rightarrow$ 严格凸；用两次拉氏中值构造 $\lambda f(x_1)+(1-\lambda)f(x_2)-f(x)$ 并配出 $f'(\xi_1)-f'(\xi_2)$。",
 "yc": r"关键是 $\xi_1<\xi_2$ 与 $f'$ 严格单调增，使右端 $<0$；这就是 Jensen 不等式的微分证明。",
 "zy": r"结论即 $f(\lambda x_1+(1-\lambda)x_2)<\lambda f(x_1)+(1-\lambda)f(x_2)$（严格凸）。",
},
4: {
 "gs": r"（Ⅰ）$f(x+y)=f(x)+f'(x)y+\dfrac{f''(x)}{2}y^2+\dfrac{f'''(\xi)}{6}y^3$。（Ⅱ）两式相减得 $|f'(x)|\le\dfrac1y+\dfrac{y^2}{6}$。（Ⅲ）$g(y)=\dfrac1y+\dfrac{y^2}{6}$ 在 $y=\sqrt[3]3$ 取最小，值 $\dfrac{\sqrt[3]9}{2}$。",
 "jq": r"（Ⅱ）用 $x+y$ 与 $x-y$ 两式相减消去 $f,f''$，解出 $f'(x)$ 并放缩。（Ⅲ）法二更简：三项均值不等式 $g=\dfrac1{2y}+\dfrac1{2y}+\dfrac{y^2}{6}\ge3\sqrt[3]{\dfrac1{24}}=\dfrac{\sqrt[3]9}{2}$。",
 "yc": r"放缩用到 $|f|\le1,|f'''|\le1$；使 $|f'(x)|$ 任意小的关键是 $y$ 可任取，再对 $y$ 优化上界。",
 "zy": r"$|f'(x)|\le\dfrac{\sqrt[3]9}{2}$。",
},
5: {
 "gs": r"（Ⅰ）令 $F(u)=\int_0^xf(t)\,\mathrm dt-uxf(x)-(1-u)xf(0)$，由 $F(0)=xf(\xi)-xf(0)>0$、$F(1)=xf(\xi)-xf(x)<0$ 零点定理得 $\theta$。（Ⅱ）$\lim\limits_{x\to0^+}\theta=\dfrac12$。",
 "jq": r"（Ⅱ）把 $\theta$ 表达式化为 $\dfrac{\int_0^xf-xf(0)}{x(f(x)-f(0))}=\dfrac{\int_0^xf-xf(0)}{x^2}\cdot\dfrac{x}{f(x)-f(0)}$ 再用洛必达/等价。",
 "yc": r"$f'(\xi)>0$ 且 $0<\xi<x$ 推 $F(0)>0,F(1)<0$；极限拆两项，第一项洛必达得 $\dfrac1{2f'(0)}$，乘 $\dfrac1{f'(0)}$ 得 $\dfrac12$。",
 "zy": r"（Ⅰ）加权积分中值；（Ⅱ）$\theta\to\dfrac12$（退化到中点差商）。",
},
6: {
 "gs": r"（Ⅰ）法一令 $F(x)=\int_0^xf$，拉氏中值得 $f(c)=1$，由 $f(c)=f(1)$ 罗尔得 $f'(\xi)=0$。（Ⅱ）法一令 $G=f+x^2$，$G''=f''+2$，对 $[0,c],[c,1]$ 用拉氏中值再对 $G'$ 用一次得 $f''(\eta)<-2$。",
 "jq": r"（Ⅱ）法二构造二次函数 $g(x)=-3x^2+4x$ 满足三点条件，令 $G=f-g$ 用罗尔链（三次）得 $G''=0\Rightarrow f''=-6<-2$。",
 "yc": r"法二关键：由 $g(0)=0,g(1)=1,\int_0^1g=1$ 解出 $a=-3,b=4$；罗尔链需 $G(0)=G(k)=G(1)=0$ 三个零点。",
 "zy": r"（Ⅰ）存在 $\xi$ 使 $f'(\xi)=0$；（Ⅱ）存在 $\eta$ 使 $f''(\eta)<-2$。",
},
7: {
 "gs": r"（Ⅰ）令 $g(x)=(x-2)f(x)$，则 $g(1)=g(2)=0$，罗尔得 $f(\xi)=(2-\xi)e^{\xi^2}$。（Ⅱ）对 $(f,g)=(\int_1^xe^{t^2}, \ln x)$ 用柯西中值定理。",
 "jq": r"（Ⅰ）构造乘积 $(x-2)f(x)$ 造出两个零点触发罗尔；（Ⅱ）柯西中值把 $f(2)$ 与 $\eta e^{\eta^2}$ 用 $\ln2$ 挂钩。",
 "yc": r"柯西中值公式 $\dfrac{f(2)-f(1)}{g(2)-g(1)}=\dfrac{f'(\eta)}{g'(\eta)}$，其中 $f(1)=0,g(1)=0,g(2)=\ln2$；注意 $f'(\eta)=e^{\eta^2}$。",
 "zy": r"（Ⅰ）罗尔；（Ⅱ）柯西中值，得 $f(2)=\ln2\cdot\eta e^{\eta^2}$。",
},
8: {
 "gs": r"必要性：在 $\dfrac{a+b}{2}$ 处一阶泰勒展开，$f''\ge0$ 保证积分项 $\ge0$。充分性：反证（局部 $f''<0$ 推出矛盾）或洛必达（对 $a=x_0-\delta,b=x_0+\delta$ 取极限）。",
 "jq": r"充要性经典的「中点积分平均 $\ge$ 中点函数值」等价于凸；证明双向都要写，泰勒展开法与构造 $F(x)$ 法任选。",
 "yc": r"充分性法二用 $\lim\limits_{\delta\to0^+}\dfrac{\int_{x_0-\delta}^{x_0+\delta}f-2\delta f(x_0)}{(4/3)\delta^3}\xlongequal{\text{洛}}\dfrac{f''(x_0)}{4}\ge0$；不要对 $f''$ 不连续时用高阶洛必达。",
 "zy": r"$f''(x)\ge0\iff f\left(\dfrac{a+b}{2}\right)\le\dfrac1{b-a}\int_a^bf(x)\,\mathrm dx$。",
},
9: {
 "gs": r"令 $F(u)=\int_0^uf$，在 $0$ 处泰勒：$F(a)=f(0)a+\dfrac{f'(0)}2a^2+\dfrac{f''(\xi_1)}6a^3$，$f(-a)=f(0)-f'(0)a+\dfrac{f''(\xi_2)}2a^2$；两式相加整理得 $\int_0^af=\dfrac a2[3f(0)-f(-a)]+\dfrac{a^3}{12}[2f''(\xi_1)+3f''(\xi_2)]$。",
 "jq": r"用连续函数介值（达布性质）：存在 $\xi$ 使 $2f''(\xi_1)+3f''(\xi_2)=5f''(\xi)$，从而系数 $\dfrac5{12}$。",
 "yc": r"不能直接写 $f''(\xi_1)=f''(\xi_2)=f''(\xi)$（不是同一点），必须用有界性 + 介值定理合并成一个 $\xi$。",
 "zy": r"$\int_0^a f(x)\,\mathrm dx=\dfrac a2[3f(0)-f(-a)]+\dfrac5{12}f''(\xi)a^3$。",
},
10: {
 "gs": r"（Ⅰ）在两端点处一阶泰勒：$f(x)=f(0)(1-x)+f(1)x+\dfrac12[f''(\xi_2)x(x-1)^2-f''(\xi_1)x^2(x-1)]$，放缩得 $\le\dfrac{x(1-x)}2$。（Ⅱ）对 (Ⅰ) 积分：$\int_0^1\dfrac{x(1-x)}2\,\mathrm dx=\dfrac1{12}$。",
 "jq": r"（Ⅰ）法二构造 $F=f-f(0)(1-x)-f(1)x-\dfrac{x(1-x)}2$、$G=+\dfrac{x(1-x)}2$，由 $F''\ge0,G''\le0$ 判上下界。（Ⅱ）积分后三角不等式。",
 "yc": r"（Ⅰ）放缩关键 $(1-x)+x=1$ 配合 $|f''|\le1$ 合并成 $\dfrac{x(1-x)}2$。（Ⅱ）$\left|\int f-\dfrac{f(0)+f(1)}2\right|\le\int|f-f(0)(1-x)-f(1)x|$。",
 "zy": r"（Ⅰ）$\le\dfrac{x(1-x)}2$；（Ⅱ）$\le\dfrac1{12}$。",
},
11: {
 "gs": r"令 $F(t)=\left(\int_0^tf\right)^{3/2}-\dfrac32\int_0^tf^2$，$F'(t)=\dfrac32f(t)\left[\left(\int_0^tf\right)^{1/2}-f(t)\right]$；再令 $g(t)=\int_0^tf-f^2(t)$，$g'(t)=2f(t)(\frac12-f'(t))\ge0$。",
 "jq": r"双辅助函数：外层 $F$ 管不等式，内层 $g$ 证 $\int_0^tf\ge f^2(t)$（即 $\sqrt{\int_0^tf}\ge f(t)$）；由 $0<f'<\frac12$ 保证 $g'\ge0$。",
 "yc": r"由 $0<f'(x)<\frac12$ 得 $f\ge0$，故 $g'\ge0$；$g\ge0\Rightarrow\sqrt{\int_0^tf}\ge f(t)\Rightarrow F'\ge0$。",
 "zy": r"$\left(\int_0^a f\right)^{3/2}\ge\dfrac32\int_0^a f^2$。",
},
12: {
 "gs": r"令 $F(x)=xf'(x)+f(x)-\int_0^xf(t)\,\mathrm dt$，则 $F(0)=0$，$F'(x)=xf''(x)+2f'(x)-f(x)$。设最大值点 $c$ 使 $f(c)=M>0$。",
 "jq": r"分 $c\in(0,1)$ 与 $c=1$ 两情形：由 $F(c)>0$（或 $F(1)>0$）对 $[0,c]$（或 $[0,1]$）用拉氏中值得 $F'(\xi)>0$。",
 "yc": r"$c\in(0,1)$ 时 $f'(c)=0$，$F(c)=f(c)-\int_0^cf>f(c)-cf(c)>0$（因 $\int_0^cf<cf(c)$ 且 $c<1$）；$c=1$ 时 $f'(1)\ge0$ 保证 $F(1)>0$。",
 "zy": r"存在 $\xi\in(0,1)$ 使 $\xi f''(\xi)+2f'(\xi)>f(\xi)$。",
},
13: {
 "gs": r"（Ⅰ）令 $F(x)=f(x)-f(a)x$，由 $\int_0^a[f(x)-f(a)x]=0$ 介值得 $F(c)=0$，再用 $F(0)=F(c)=0$ 罗尔得 $f'(\xi)=f(a)$。（Ⅱ）令 $G=(f'-\lambda f(a))e^{-\lambda x}$，对 $G(\xi)=G(x_0)=0$ 罗尔。",
 "jq": r"奇函数条件：由 $f$ 奇 $\Rightarrow F$ 奇 $\Rightarrow F(-c)=-F(c)$，从而多一个零点触发第二次罗尔；或法二用 $F(t)=\int_0^tf-\frac12t^2f(a)$ 偶 + 三次罗尔。",
 "yc": r"（Ⅱ）要同时用过 $f'(\xi)=f(a)$ 与 $f'(-c)=f'(\xi)$（偶导）；$G$ 的指数因子使求导后恰好出现 $-\lambda f'$ 项。",
 "zy": r"（Ⅰ）$f'(\xi)=f(a)$；（Ⅱ）$f''(\eta)-\lambda f'(\eta)+\lambda f(a)=0$。",
},
14: {
 "gs": r"（Ⅰ）必要性由 $f(x\pm h)$ 一阶泰勒相加得 $f(x+h)+f(x-h)-2f(x)=\dfrac{h^2}{2}[f''(\xi_1)+f''(\xi_2)]\ge0$。充分性取极限 $\lim\limits_{h\to0}\dfrac{f(x+h)-2f(x)+f(x-h)}{h^2}=f''(x)$。（Ⅱ）拐点 $x_0$ 两侧 $f''$ 异号 $\Rightarrow f'$ 在 $x_0$ 取极大 $\Rightarrow f''(x_0)=0$。",
 "jq": r"（Ⅰ）充要性：必要性泰勒，充分性用洛必达（只一次，因 $f''$ 未必连续，再拆成两个差商）保号得 $f''\ge0$。（Ⅱ）由拐点定义 + （Ⅰ）。",
 "yc": r"充分性中 $f$ 仅二阶可导，$f''$ 未必连续，洛必达只用一次，第二步拆成 $\dfrac{f'(x+h)-f'(x)}{2h}-\dfrac{f'(x-h)-f'(x)}{2h}$。",
 "zy": r"（Ⅰ）$f''\ge0\iff f(x+h)-2f(x)+f(x-h)\ge0$；（Ⅱ）拐点处 $f''(x_0)=0$。",
},
15: {
 "gs": r"（Ⅰ）令 $F=\int_0^tf^3$，$G=\left(\int_0^tf\right)^2$，两次柯西中值：$\dfrac{\int_0^1f^3}{(\int_0^1f)^2}=\dfrac{f^3(\eta)}{2f(\eta)\int_0^\eta f}=\dfrac{f^2(\eta)-f^2(0)}{2\int_0^\eta f}=f'(\xi)$。（Ⅱ）令 $H=\int_0^txf$，泰勒 $H(1)=\dfrac16(\eta f''(\eta)+2f'(\eta))$。",
 "jq": r"（Ⅰ）柯西中值连用的标准套路：分子分母各取变限积分，再对结果式再用一次柯西中值引入 $\xi$。（Ⅱ）构造三阶可导的 $H$ 用三阶泰勒直接读出目标组合。",
 "yc": r"（Ⅰ）两次柯西中值：$\eta\in(0,1)$ 由第一次得，$\xi\in(0,\eta)$ 由第二次得；（Ⅱ）$H(0)=H'(0)=H''(0)=0$ 使泰勒只剩三阶项。",
 "zy": r"（Ⅰ）$\int_0^1f^3=f'(\xi)(\int_0^1f)^2$；（Ⅱ）$\eta f''(\eta)+2f'(\eta)=6\int_0^1xf$。",
},
},

"好题12-泰勒的运用": {
1: {
 "gs": r"消参：$t\ge0\Rightarrow x=3t,y=\dfrac{x}{3}\tan\dfrac{x}{3}$；$t<0\Rightarrow x=t,y=-x\tan x$。$f'(x)$ 左右极限均为 0（连续），$f''_+(0)=\dfrac29$，$f''_-(0)=-2$（不等）。",
 "jq": r"含 $|t|$ 先按 $t\gtrless0$ 消参化成分段显函数；再算左右一、二阶导数极限判连续性与二阶导存在性。",
 "yc": r"$f'(0)$ 存在且连续（选 C 的前半）；但 $f''_+(0)\neq f''_-(0)$ 故 $f''(0)$ 不存在，选 (C) 而非 (D)。",
 "zy": r"选 (C)：$f'(x)$ 连续，$f''(0)$ 不存在。",
},
2: {
 "gs": r"$\cos|x|=\cos x$（任意阶可导）；$g(x)=x^2|x|=\begin{cases}x^3,&x\ge0\\-x^3,&x<0\end{cases}$，$g'(x)=3x|x|$，$g''(x)=6|x|$，但 $g'''_\pm(0)=\pm6$ 不等。",
 "jq": r"「偶函数 + $|x|$ 幂次项」问题：$|x|^n$ 决定最高可导阶——$|x|^3$ 恰好二阶可导、三阶左右导数异号。",
 "yc": r"逐阶用导数定义算单侧极限，不能直接套 $|x|$ 求导公式；$\cos|x|$ 全程光滑，拖累来自 $x^2|x|$。",
 "zy": r"最高阶数为 2。",
},
3: {
 "gs": r"法二最巧：$f(x)=\dfrac{1+x}{\sqrt{1-x^2}}=\dfrac1{\sqrt{1-x^2}}+\dfrac{x}{\sqrt{1-x^2}}=1+\dfrac12x^2+\cdots+x+\cdots=1+x+\dfrac12x^2+o(x^2)$。",
 "jq": r"求二次泰勒系数：比较系数法或化成 $\dfrac1{\sqrt{1-x^2}}$（$=1+\frac12x^2+\cdots$）展开；避免直接对根式连求导。",
 "yc": r"法一系数比较：$b-\frac12=\frac12\Rightarrow b=1$，$c-\frac b2-\frac18=-\frac18\Rightarrow c=\frac12$；别把 $a$ 错写成 0。",
 "zy": r"选 (B)：$a=1,b=1,c=\dfrac12$。",
},
4: {
 "gs": r"代 $x=0$ 得 $y(0)=0$；求导 $2-e^{-y^2}y'=y+xy'$，得 $y'(0)=2$；再求导 $-e^{-y^2}y''+2ye^{-y^2}(y')^2=2y'+xy''$，得 $y''(0)=-4$。",
 "jq": r"隐函数求二阶泰勒：逐次对方程求导并代入已知 $y(0),y'(0)$，解出 $y''(0)$；由 $y=\lambda_1x+\lambda_2x^2+o(x^2)$ 得 $(\lambda_1,\lambda_2)=(y'(0),\frac{y''(0)}2)$。",
 "yc": r"第二次求导时 $-\dfrac{\mathrm d}{\mathrm dx}e^{-y^2}=e^{-y^2}\cdot2y\cdot y'$（链式法则别漏 $2y$）；$\lambda_2=\dfrac{y''(0)}2=-2$ 不是 $-4$。",
 "zy": r"选 (B)：$(\lambda_1,\lambda_2)=(2,-2)$。",
},
},

}
