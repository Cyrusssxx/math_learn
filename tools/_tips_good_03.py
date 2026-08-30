# -*- coding: utf-8 -*-
"""好题点睛 批次3 —— 好题13~好题22 共 52 题
四段规范：gs 公式 / yc 易错 / jq 技巧 / zy 注意（与真题 tips 同源）
"""

TIPS = {

"好题13-不等式": {
1: {
 "gs": r"构造 $f(x)=x\ln\dfrac{1+x}{1-x}+\cos x-1-\dfrac{x^2}{2}$，证 $f(x)\ge0$。法一：$f$ 偶，只需证 $[0,1)$；$f'(x)=\ln\dfrac{1+x}{1-x}+\dfrac{2x}{1-x^2}-\sin x-x>0$，故 $f(0)=0$ 为最小。法二：$f''(x)>0$ 推 $f'$ 增。法三：泰勒 $\cos x\ge1-\dfrac{x^2}{2}$ 配 $\ln\dfrac{1+x}{1-x}\ge x$。",
 "jq": r"三主流法：①构造辅助函数+单调性（最直接）；②用 $f''$ 判 $f'$ 单调；③泰勒放缩（把 $\cos x$ 放成 $1-x^2/2$，再证对数不等式）。选其一即可，法一最稳。",
 "yc": r"偶函数性质是关键桥梁——只需证 $[0,1)$、$x=0$ 即最小，避免 $[-1,0]$ 重复。法三中 $\ln\dfrac{1+x}{1-x}\ge x$ 证法同法一思路，别另起炉灶。",
 "zy": r"定义域 $(-1,1)$；奇偶化简后 $f(x)\ge f(0)=0$。三法都行，推荐法一/法二。",
},
2: {
 "gs": r"（Ⅰ）由 $f$ 单调减非负，$[k,k+1]$ 上 $f(k+1)\le f(x)\le f(k)$，积分得 $f(k+1)\le\int_k^{k+1}f\le f(k)$。（Ⅱ）取 $f(x)=1/x$，累加得 $\ln(1+n)\le1+\frac12+\cdots+\frac1n\le1+\ln n$，夹逼得 $\lim\dfrac{H_n}{\ln n}=1$。",
 "jq": r"调和级数估计标准套路：单调减函数的积分夹逼（积分测试法）把离散和包进相邻两积分。",
 "yc": r"取 $f=1/x$ 后累加方向要对齐：$1/(n+1)\le\int_n^{n+1}1/x$，上下界都要出现 $1+\frac12+\cdots+\frac1n$；夹逼上下界极限都趋于 1。",
 "zy": r"结论 $H_n\sim\ln n$，极限为 1；此结论常作工具比较 $\sum1/k$ 与 $\ln n$。",
},
3: {
 "gs": r"$I_1=\int_1^x\frac2{1+t^2}\mathrm dt$，$I_2=\int_1^x\frac{\ln t}{t-1}\mathrm dt$，$I_3=\int_1^x\frac1{\sqrt t}\mathrm dt$（$x>1$）。证 $t>1$ 时 $\frac2{1+t^2}<\frac{\ln t}{t-1}<\frac1{\sqrt t}$，由保序性 $I_1<I_2<I_3$。",
 "jq": r"变限积分大小比较 $\iff$ 被积函数大小比较（同起点 $x>1$ 单调增）。分别构造差函数 $f(t)=(1+t^2)\ln t-2(t-1)$、$g(t)=t-1-\sqrt t\ln t$ 证不等式。",
 "yc": r"起点都是 $x=1$（下限 1），比较方向一致；不能只看某点，需证整个 $(1,x)$ 上大小关系恒成立。",
 "zy": r"选 (A)。",
},
4: {
 "gs": r"（1）$f'(x)=(1-a)a^x(1+x\ln a)$，驻点 $x=-1/\ln a$（注意 $a^{-1/\ln a}=e^{-1}$），最大值 $f_{\max}=\dfrac{a-1}{e\ln a}$（$0<a<1$）。（2）固定 $y$ 对 $x$ 用（1）得 $xy^x(1-y)\le\dfrac{y-1}{e\ln y}$，由 $\ln y<y-1<0$ 得 $\dfrac{y-1}{\ln y}<1$，故 $<\dfrac1e$。",
 "jq": r"两问联动：第(2)问本质「对任意固定 $y$，先对 $x$ 取最大」，把双变量化为单变量上界再放缩。",
 "yc": r"第(1)问 $0<a<1$ 使 $\ln a<0$，故 $-1/\ln a>0$ 在定义域内；$a^{-1/\ln a}=e^{-1}$ 是指数恒等式关键。",
 "zy": r"最大值 $\dfrac{a-1}{e\ln a}$（$a-1<0,\ln a<0$ 比值为正）；第(2)结论 $<\dfrac1e$。",
},
5: {
 "gs": r"令 $f(x)=\dfrac{\arcsin x}{x}$（$0<x<1$），$f'(x)=\dfrac{x-\sqrt{1-x^2}\arcsin x}{x^2\sqrt{1-x^2}}$，再令 $g(x)=x-\sqrt{1-x^2}\arcsin x$，$g'>0\Rightarrow f'(x)>0\Rightarrow f$ 增，故 $\dfrac{\arcsin x^2}{x^2}<\dfrac{\arcsin x}{x}$。又 $\arcsin x>x\Rightarrow\dfrac{\arcsin x}{x}>1\Rightarrow\left(\dfrac{\arcsin x}{x}\right)^2>\dfrac{\arcsin x}{x}$。",
 "jq": r"先证 $f(x)=\arcsin x/x$ 在 $(0,1)$ 单调递增，利用 $0<x^2<x$ 比较前两项；再用 $\arcsin x>x$ 证比值大于 1。",
 "yc": r"$g'(x)=\dfrac{x\arcsin x}{\sqrt{1-x^2}}>0$ 关键是 $\arcsin x$ 与 $x$ 同号；$0<x^2<x$ 顺序不能反。",
 "zy": r"选 (A)。",
},
6: {
 "gs": r"（Ⅰ）$g''-g'=x-1$，特征根 $r=0,1$，特解令 $y^*=(ax+b)x$ 得 $g(x)=e^x-\frac12x^2-1$。（Ⅱ）令 $F=[f-g]'-[f-g]$，证 $F'\ge0\Rightarrow F\ge0$；再令 $G=[f-g]e^{-x}$，证 $G'\ge0\Rightarrow G\ge0\Rightarrow f\ge g$。",
 "jq": r"比较两函数大小：构造差函数，用「导数+积分因子（乘 $e^{-x}$）」法把 $[f-g]'-[f-g]\ge0$ 化成 $([f-g]e^{-x})'\ge0$。",
 "yc": r"第(Ⅰ)特解设 $(ax+b)x$（因 $r=0$ 是特征根，需乘 $x$）；第(Ⅱ)积分因子 $e^{-x}$ 来自齐次方程 $u'-u=0$。",
 "zy": r"$g(x)=e^x-\frac12x^2-1$；结论 $f(x)\ge g(x)\ (x>0)$。",
},
7: {
 "gs": r"$D:|x|+|y|\le\frac\pi2$，$I_1=\iint\sqrt{x^2+y^2}$，$I_2=\iint\sin\sqrt{x^2+y^2}$，$I_3=\iint(1-\cos\sqrt{x^2+y^2})$。令 $u=\sqrt{x^2+y^2}\in[0,\pi/2]$，由 $\sin u<u$ 得 $I_2<I_1$；由 $\sin u\ge1-\cos u$（令 $f=\sin u+\cos u-1\ge0$）得 $I_3<I_2$。",
 "jq": r"同区域二重积分比较 $\iff$ 被积函数比较。被积函数都只依赖 $r=\sqrt{x^2+y^2}$（径向对称），化为单变量函数比值。",
 "yc": r"区域 $D$ 含于半径 $\pi/2$ 圆盘，故 $u\le\pi/2$ 才能用 $(0,\pi/2)$ 上不等式；$\sin u\ge1-\cos u$ 在 $[0,\pi/2]$ 取等仅 $u=0,\pi/2$。",
 "zy": r"选 (A)：$I_3<I_2<I_1$。",
},
8: {
 "gs": r"$I_1=\int_0^\pi e^{-x^2}\sin x\,\mathrm dx+\int_\pi^{2\pi}\cdots\xlongequal{x=\pi+t}\int_0^\pi[e^{-x^2}-e^{-(\pi+x)^2}]\sin x\,\mathrm dx>0$。$I_2>\int_0^{2\pi}e^{-x^2}(1-\frac{x^2}2)\,\mathrm dx=\frac34\int_0^{2\pi}e^{-x^2}\,\mathrm dx+\frac\pi2e^{-4\pi^2}>0$。",
 "jq": r"$I_1$ 用对称换元 $x=\pi+t$ 把两段合并成被积函数恒正；$I_2$ 用 $\cos x\ge1-x^2/2$ 放缩成正项积分。",
 "yc": r"$I_1$ 不能直接说正——需半周期反对称抵消后剩「小半周期被大权重减」；$I_2$ 放缩后边界项 $\frac\pi2e^{-4\pi^2}>0$ 别漏。",
 "zy": r"选 (A)：$I_1>0,I_2>0$。",
},
9: {
 "gs": r"换元 $x=a-t$ 得 $\int_0^af=\int_0^af(a-x)$，故 $\int_0^af=\frac12\int_0^a[f(x)+f(a-x)]$。由 $f>0$ 及均值不等式 $f(x)+f(a-x)\ge2\sqrt{f(x)f(a-x)}=2a$ 得 $\int_0^af\ge a^2$；取 $f\equiv a$ 达界。",
 "jq": r"经典对称积分：$x\leftrightarrow a-x$ 换元把积分写成两式平均，再用题设乘积条件套均值不等式。",
 "yc": r"关键恒等式 $\int_0^a f(x)=\frac12\int_0^a[f(x)+f(a-x)]$；等号条件 $f(x)=f(a-x)$（取 $f\equiv a$ 满足且达 $a^2$）。",
 "zy": r"选 (D)：$[a^2,+\infty)$。",
},
10: {
 "gs": r"$I_1-I_2=\int_0^{\pi/2}f(\sin x-\cos x)\,\mathrm dx$，对 $[\pi/4,\pi/2]$ 段换元 $x\to\pi/2-x$ 合并得 $\int_0^{\pi/4}[f(\pi/2-x)-f(x)](\cos x-\sin x)\,\mathrm dx>0$（因 $\pi/2-x>x$ 且 $f$ 增）。又 $\tan x>\sin x\Rightarrow I_3>I_1$。",
 "jq": r"三角函数积分比较常用「拆分到 $[0,\pi/4]$ 与 $[\pi/4,\pi/2]$ 并作对称换元」把 $f$ 两不同点值并在同一区间比较。",
 "yc": r"$\sin x-\cos x$ 在 $[0,\pi/4]$ 负、$[\pi/4,\pi/2]$ 正，单看不行，必须对称换元合并；$f$ 增使 $f(\pi/2-x)>f(x)$（$x<\pi/4$）。",
 "zy": r"选 (D)：$I_3>I_1>I_2$。",
},
11: {
 "gs": r"$I_1-I_2=\int_0^{\pi/2}\frac{\sin x-\cos x}{1+x^2}\mathrm dx$，对称换元合并得 $\int_0^{\pi/4}(\cos x-\sin x)[1/(1+(\pi/2-x)^2)-1/(1+x^2)]\mathrm dx<0\Rightarrow I_1<I_2$。$J_1-J_2=\int_0^1e^x\frac{2-3x}{2\sqrt{1-x}}\mathrm dx$，按 $x\gtrless2/3$ 分段放缩 $e^x\le e^{2/3}$ 得 $<0\Rightarrow J_1<J_2$。",
 "jq": r"$I$ 对用对称换元；$J$ 对用「分段放缩 + 换元 $\sqrt{1-x}=t$」把含根式的差积分算成 0。",
 "yc": r"$J_1-J_2$ 通分后分子 $2-3x$ 在 $x=2/3$ 变号，分段放缩方向相反（前段 $e^x<e^{2/3}$ 但系数正，后段 $e^x>e^{2/3}$ 但系数负），故整体仍 $<0$。",
 "zy": r"选 (D)：$I_1<I_2,J_1<J_2$。",
},
12: {
 "gs": r"凹函数满足 $f(\frac{x_1+x_2}{2})\le\frac12[f(x_1)+f(x_2)]$。令 $x=u/2$ 得 $\int_0^{1/2}f(x)\,\mathrm dx=\frac12\int_0^1f(u/2)\,\mathrm du\le\frac12\int_0^1\frac12[f(u)+f(0)]\,\mathrm du=\frac14\int_0^1f$。",
 "jq": r"半区间积分估计：用凹性把 $f(x/2)$（半区间上点）夹到全区间平均；本质 Jensen 不等式的积分形式。",
 "yc": r"不能对 $f(x)$ 直接放线性（凹函数无统一上界方向）；关键变换 $x=u/2$ 把 $[0,1/2]$ 映到 $[0,1]$。",
 "zy": r"选 (A)：$4\int_0^{1/2}f\le\int_0^1f$。",
},
},

"好题14-放缩": {
1: {
 "gs": r"分部积分一次：$\int_0^1e^{-x}\sin nx\,\mathrm dx=-\frac1n\left(e^{-x}\cos nx|_0^1+\int_0^1e^{-x}\cos nx\,\mathrm dx\right)$，括号内有界（≤3），故极限为 0。",
 "jq": r"振荡积分趋于 0 标准法：分部积分使分母出现 $n$，分子有界（$\int$ 有界 + 端点值有界），整体 $O(1/n)\to0$。",
 "yc": r"法二「算出 $I_n$ 显式再取极限」也可但更繁；本题只需上界估计，分部一次足够。",
 "zy": r"填 0。",
},
2: {
 "gs": r"由 $\frac1{n+1}\le\ln(1+\frac1n)\le\frac1n$ 累加得 $1+\ln\frac{n+1}{2}\le H_n\le1+\ln n$，夹逼得 $\lim H_n/\ln n=1$。",
 "jq": r"调和和估计：用 $\ln(1+1/n)$ 夹逼每一项 $1/n$（积分放缩），再夹逼取极限。",
 "yc": r"也可直接积分测试 $\ln(n+1)\le H_n\le1+\ln n$；分子 $1+\ln\frac{n+1}{2}\to1$，上下界极限均趋于 1。",
 "zy": r"填 1。",
},
3: {
 "gs": r"上界 $n\int_n^{2n}\frac{x^2}{1+x^4}\mathrm dx<n\int_n^{2n}\frac1{x^2}\mathrm dx=\frac12$；下界 $>n\int_n^{2n}\frac1{1+x^2}\mathrm dx=n[\arctan(2n)-\arctan n]\sim\frac12$。夹逼得 1/2。",
 "jq": r"含 $x^4$ 积分难算，用 $x^2/(1+x^4)$ 上下放缩（分子 $x^2$ 近似主导）→ 一边换 $1/x^2$、一边换 $1/(1+x^2)$，两极限都 1/2。",
 "yc": r"下界放缩用 $x^2/(x^2+x^4)=1/(1+x^2)$（分子分母同除 $x^2$）；arctan 差用公式 $\arctan a-\arctan b=\arctan\frac{a-b}{1+ab}$ 取极限。",
 "zy": r"填 1/2。",
},
4: {
 "gs": r"设 $f(x)=\frac{\ln x}{x}$，$x\ge3$ 时 $f'<0$ 单调减，故 $\int_3^{n+1}\frac{\ln x}{x}\mathrm dx\le\sum_{k=3}^n\frac{\ln k}{k}\le\frac{\ln3}3+\int_3^n\frac{\ln x}{x}\mathrm dx$；积分值 $=\frac12\ln^2n-\frac12\ln^23$，夹逼得原极限 1/2。",
 "jq": r"离散和估计：单调减函数用相邻积分夹逼（左端点积分 ≤ 和 ≤ 首项 + 左移一积分）。",
 "yc": r"$\int\frac{\ln x}{x}\mathrm dx=\frac12\ln^2x+C$；上下界都除以 $\ln^2n$ 后趋于 1/2。",
 "zy": r"选 (D)。",
},
5: {
 "gs": r"上界 $\sqrt[n]{1+n\arctan x^2}\le\sqrt[n]{1+n}$，积分 $\le\frac\pi4\sqrt[n]{1+n}$；下界 $\ge1$，积分 $\ge\pi/4$。$\lim\sqrt[n]{1+n}=1$，夹逼得 $\pi/4$。",
 "jq": r"含 $n$ 次根式的极限：用「根式被 1 和下界控制、被 $\sqrt[n]{1+n}$ 控制」双向夹逼；$\sqrt[n]{1+n}\to1$ 是常用结论。",
 "yc": r"$x\in[0,1]$ 时 $\arctan x^2\le\arctan1<1$，故 $1+n\arctan x^2\le1+n$。",
 "zy": r"填 $\pi/4$。",
},
6: {
 "gs": r"两次分部积分得 $\int_0^{2\pi}e^{-x}\sin nx\,\mathrm dx=\frac{n(1-e^{-2\pi})}{1+n^2}$，故 $n\times$ 该式 $=\frac{n^2(1-e^{-2\pi})}{1+n^2}\to1-e^{-2\pi}$。",
 "jq": r"与上题不同——此处因子 $n$ 在外，必须算出显式（两次分部积分解方程），不能用有界放缩。",
 "yc": r"两次分部积分会出现「原式 = 含原式的项」，移项解代数方程；端点 $e^{-x}\sin nx|_0^{2\pi}=0$ 但 $e^{-x}\cos nx|_0^{2\pi}=1-e^{-2\pi}$。",
 "zy": r"填 $1-e^{-2\pi}$。",
},
},

"好题15-构造证明": {
1: {
 "gs": r"令 $f(x)=\sum_{k=0}^{2n+1}\frac{x^k}{k!}$，$F(x)=e^{-x}f(x)$，则 $F'(x)=e^{-x}(f'-f)=-\frac{x^{2n+1}}{(2n+1)!}e^{-x}$。$x<0$ 时 $F'>0$ 单调增，$F(-\infty)=-\infty,F(0)=1$ 有一根；$x>0$ 时 $F'<0$ 单调减，$F(+\infty)=0,F(0)=1$ 无根。",
 "jq": r"经典技巧：乘 $e^{-x}$ 后 $f'-f$ 恰好消去最高项只剩单一项，导数符号易判。",
 "yc": r"$f'-f=-\frac{x^{2n+1}}{(2n+1)!}$（$f$ 是截断指数，差分即余项）；注意偶数次截断 $\sum_{k=0}^{2n}$ 无实根（注记结论）。",
 "zy": r"有且仅有一个实根。",
},
},

"好题16-构图快速解答题": {
1: {
 "gs": r"$f$ 奇且 $x=-1$ 是 $(-\infty,0)$ 唯一零点、$f'(-1)=1>0$，由导数定义 $f$ 在 $(-1,0)$ 为正、$(-\infty,-1)$ 为负；奇性推 $(0,1)$ 负、$(1,+\infty)$ 正。$\left(\int_0^x f\right)'=f(x)>0$ 区间为 $(-1,0)$ 与 $(1,+\infty)$。",
 "jq": r"变限积分单调性 $\iff$ 被积函数 $f(x)$ 符号。先由「一点导数值>0 + 唯一零点」定出各区间 $f$ 符号，再利用奇性翻折。",
 "yc": r"单调增区间要求 $f(x)>0$（严格），不是 $f(x)\ge0$；$x=-1$ 是零点本身不入增区间内部。",
 "zy": r"选 (D)：$(-1,0)$ 与 $(1,+\infty)$。",
},
2: {
 "gs": r"被积 $f(x,y)=2-x^2-2y^2$，非负区域恰为椭圆 $x^2+2y^2\le2$ 即 $D_2$。$D_1\subset D_2$ 且 $D_2$ 上 $f\ge0\Rightarrow I_1<I_2$；$D_3,D_4$ 中超出 $D_2$ 部分 $f\le0\Rightarrow I_3,I_4\le I_2$。",
 "jq": r"同被积函数在多区域积分比较：先找被积函数非负区域，再比较各区域与该区域包含关系（超出部分贡献非正）。",
 "yc": r"关键是识别 $f\ge0\iff x^2+2y^2\le2=D_2$；不能用面积比（被积函数非均匀）。",
 "zy": r"选 (B)：$I_2$ 最大。",
},
},

"好题17-特例解题": {
1: {
 "gs": r"由 $f(x)-1=2x^2+o(x^2)$ 得 $\lim\frac{f(x)-f(0)}{x}=0\Rightarrow f'(0)=0$（②正确）。构造反例 $f(x)=1+2x^2+x^2a(x)$（$a(x)$ 为有理数取 0、无理数取 $x$），使 $x\ne0$ 时不连续 $\Rightarrow$ ①($f'(x)$ 表达式)、③($f''(0)$)、④(凹)均错。",
 "jq": r"局部展开只给 $x\to0$ 性态，不能逐项求导、不能推 $x=0$ 外性质；要否定「可导/二阶导/凹」须构造在 0 附近满足展开但别处极不规则的反例。",
 "yc": r"②可由差商极限直接得出（不需全局可导）；反例核心是让扰动 $x^2a(x)=o(x^2)$ 但破坏连续/可导。",
 "zy": r"选 (A)：仅 1 个正确（②）。",
},
},

"好题18-绝对值与根号问题": {
1: {
 "gs": r"由题意 $a\int_0^x|y|\,\mathrm dt=\int_0^x\sqrt{1+y'^2}\,\mathrm dt$，求导得 $a|y|=\sqrt{1+y'^2}$。由 $y(0)=1/a>0$ 连续及 $a|y|\ge1$ 推 $y>0$，故 $y'=\pm\sqrt{a^2y^2-1}$。积分得 $y=\frac{e^{ax}+e^{-ax}}{2a}$（双曲余弦）。",
 "jq": r"几何条件（弧长=面积倍）→ 等式两边求导化微分方程；用共轭式 $\frac{\mathrm dy}{\sqrt{a^2y^2-1}}=\frac1a\ln(ay+\sqrt{a^2y^2-1})$ 解之。",
 "yc": r"必须判定 $|y|=y$（绝对值可剥）：由 $a|y|=\sqrt{1+y'^2}\ge1$ 且 $y(0)=1/a>0$ 连续；两符号分支解相同。",
 "zy": r"$y=\frac{e^{ax}+e^{-ax}}{2a}$。",
},
2: {
 "gs": r"切线交 $x$ 轴于 $N$，由 $|OM|=|ON|$ 与 $y>0$ 得 $\frac{\mathrm dy}{\mathrm dx}=\frac{y}{x+\sqrt{x^2+y^2}}$；化为 $\frac{\mathrm dx}{\mathrm dy}=\frac{x}{y}+\sqrt{1+(x/y)^2}$，令 $u=x/y$ 得 $\frac{\mathrm du}{\sqrt{1+u^2}}=\frac{\mathrm dy}{y}$，积分 $u+\sqrt{1+u^2}=C_2y$，用 $y(0)=1$ 定 $C_2=1$，得 $y=\sqrt{1+2x}$。",
 "jq": r"几何关系转微分方程：先由相似三角形写 $y'=\frac{MP}{NP}$（$NP=NO+OP=\sqrt{x^2+y^2}+x$），再倒数换元 $u=x/y$ 解齐次型。",
 "yc": r"上凸 + $y'(x)>0$ 决定 $N$ 在 $O$ 左侧（$NP=NO+OP$）；令 $u=x/y$ 后积分 $\int\frac{\mathrm du}{\sqrt{1+u^2}}=\ln(u+\sqrt{1+u^2})$。",
 "zy": r"$y=\sqrt{1+2x}$（$x>-1/2$）。",
},
},

"好题19-一元函数积分学": {
1: {
 "gs": r"令 $F(x)=\int_0^xf+\frac1{\sqrt2}$（则 $F'=f$），原式化为 $2F'F=\frac{(x+1)e^x}{(x+2)^2}$，积分得 $F^2=\frac{e^x}{x+2}+C$，$F(0)=1/\sqrt2\Rightarrow C=0$，$F=\frac{e^{x/2}}{\sqrt{x+2}}$，$f=F'=\frac{(x+1)e^{x/2}}{2(x+2)^{3/2}}$。",
 "jq": r"含 $\int f$ 与 $f$ 的方程：令 $F=\int f$ 化「$F'F=$ 已知」→ 积分得 $F^2$。",
 "yc": r"关键拆分 $\frac{(x+1)e^x}{(x+2)^2}=\frac{e^x}{x+2}-\frac{e^x}{(x+2)^2}=(\frac{e^x}{x+2})'$；$F>0$ 取正根由连续性定。",
 "zy": r"$f(x)=\frac{(x+1)e^{x/2}}{2(x+2)^{3/2}}$。",
},
2: {
 "gs": r"原函数分段：$F(x)=\frac1{\sqrt2}\arctan(\sqrt2\tan x)-\frac{\pi}{2\sqrt2}$（$0\le x<\pi/2$）；$0$（$x=\pi/2$）；$+\frac{\pi}{2\sqrt2}$（$\pi/2<x\le\pi$）。全体原 $=F(x)+C$。",
 "jq": r"在瑕点 $x=\pi/2$（$\tan x$ 无穷）处需分段求原函数并在该点「连续拼接」——分别求 $(0,\pi/2)$、$(\pi/2,\pi)$ 的原函数，用极限值调整常数项使连续。",
 "yc": r"$\int\frac{1}{1+\sin^2x}\mathrm dx=\frac1{\sqrt2}\arctan(\sqrt2\tan x)+C$ 在 $\pi/2$ 无定义，必须拼接；拼接常数由单侧极限=0 定（使 $F(\pi/2)=0$）。",
 "zy": r"全体原函数 $=F(x)+C$，其中 $F$ 分段如上式。",
},
3: {
 "gs": r"法一令 $t=\sqrt{\frac{x-a}{b-x}}$ 得 $I=2\arctan\sqrt{\frac{x-a}{b-x}}+C$；法二 $I=2\int\frac{\mathrm d\sqrt{x-a}}{\sqrt{b-a-(x-a)}}=2\arcsin\sqrt{\frac{x-a}{b-a}}+C$。",
 "jq": r"含 $\sqrt{(x-a)(b-x)}$ 的积分：①根式代换 $t=\sqrt{\frac{x-a}{b-x}}$；②配方成 $\sqrt{r^2-u^2}$ 后用反正弦。",
 "yc": r"两法结果相差常数（均可）；注意 $a<x<b$ 保证根号内正。",
 "zy": r"$2\arctan\sqrt{\frac{x-a}{b-x}}+C$（或 $2\arcsin\sqrt{\frac{x-a}{b-a}}+C$）。",
},
4: {
 "gs": r"$\sin\frac2n\sim\frac2n$，原式 $\sim\frac1n\sum_{k=1}^n\frac1{\sqrt{1+(\frac{2k-1}{2n})^2}}\to\int_0^1\frac1{\sqrt{1+x^2}}\mathrm dx=\ln(1+\sqrt2)$。",
 "jq": r"和式极限：先等价无穷小替换 $\sin(2/n)\sim2/n$，再把和式写成黎曼和 $\frac1n\sum f(\frac{2k-1}{2n})$（中点分割）→ 定积分。",
 "yc": r"分割点 $\frac{2k-1}{2n}\in(0,1)$ 是 $[0,1]$ 的中点分割；被积 $\frac1{\sqrt{1+x^2}}$，积分 $=\ln(x+\sqrt{1+x^2})$。",
 "zy": r"填 $\ln(1+\sqrt2)$。",
},
5: {
 "gs": r"极坐标面积公式 $A=\frac12\int_0^{2\pi}r^2\mathrm d\theta=\frac12\int_0^{2\pi}\theta^2\mathrm d\theta$；$n$ 等分 $[0,2\pi]$，取右端点 $\theta_i=\frac{2\pi i}{n}$，得 $A=\lim\sum_{i=1}^n\frac12(\frac{2\pi i}{n})^2\frac{2\pi}{n}=\lim\sum\frac{4\pi^3i^2}{n^3}$。",
 "jq": r"几何量写定积分后，按「等分区间、取右端点」还原黎曼和形式。",
 "yc": r"扇形面积微元是 $\frac12r^2\mathrm d\theta$（不是 $r^2$）；第 $i$ 份取 $\theta_i=\frac{2\pi i}{n}$。",
 "zy": r"选 (A)。",
},
6: {
 "gs": r"两积分相减 $\int f(x\cos x)(\cos x-x\sin x)\,\mathrm dx=\int f(x\cos x)\,\mathrm d(x\cos x)=F(x\cos x)|_{-\pi/2}^{\pi/2}=0$（因 $x\cos x$ 两端均为 0）。故 $\int f\cdot x\sin x=\int f\cdot\cos x=m$。",
 "jq": r"由已知 $\int f(x\cos x)\cos x\,\mathrm dx=m$，构造「已知式 − 所求式」，凑微分 $\mathrm d(x\cos x)=\cos x-x\sin x$。",
 "yc": r"$x\cos x|_{x=\pm\pi/2}=0$ 使边界项为 0；不要试图直接算所求积分（无显式 $f$）。",
 "zy": r"填 $m$。",
},
7: {
 "gs": r"由 $r^2=x^2+f^2(x)$，$\theta=\arctan\frac{f(x)}x$，$\mathrm d\theta=\frac{xf'-f}{x^2+f^2}\mathrm dx$，得 $r^2\mathrm d\theta=[xf'-f]\mathrm dx$。故 $\int_\alpha^\beta r^2\mathrm d\theta=\int_a^b[xf'-f]\mathrm dx=bf(b)-af(a)-2\int_a^b f=bf(b)-af(a)$（已知 $\int_a^b f=0$）。",
 "jq": r"极坐标量转直角坐标量：写 $\theta(x)$ 与 $\mathrm d\theta/\mathrm dx$，相乘消分母 $(x^2+f^2)$ 得 $xf'-f$，再分部积分 $\int xf'=\int x\,\mathrm df$。",
 "yc": r"隐含条件 $\int_a^b f=0$ 用来消掉 $-2\int f$ 项；选项 (C) 是 $bf(b)-af(a)$。",
 "zy": r"选 (C)。",
},
8: {
 "gs": r"以 $r$ 为参，弧长 $s=\int_1^3\sqrt{1+r^2\theta'^2(r)}\,\mathrm dr$。$\theta'=\frac12(1-1/r^2)$，根号内 $=\frac14r^2+\frac12+\frac1{4r^2}=(\frac r2+\frac1{2r})^2$，积分得 $s=\int_1^3(\frac r2+\frac1{2r})\mathrm dr=2+\frac12\ln3$。",
 "jq": r"极坐标曲线弧长公式用 $r$ 作参数：$s=\int\sqrt{1+r^2\theta'^2}\,\mathrm dr$（即 $x',y'$ 合成后的简化式）。",
 "yc": r"根号内配方成完全平方式 $\to$ 去根号；积分 $\int\frac1{2r}\mathrm dr=\frac12\ln r$。",
 "zy": r"$2+\frac12\ln3$。",
},
9: {
 "gs": r"$D=[0,1]\times[0,2]$，按 $4x^2\gtrless y^2$ 分 $D_1(0\le y\le2x)$ 与 $D_2(0\le x\le y/2)$。$I=\int_0^1\mathrm dy\int_0^{2x}e^{4x^2}+\int_0^2\mathrm dy\int_0^{y/2}e^{y^2}=\frac14(e^4-1)+\frac14(e^4-1)=\frac12(e^4-1)$。",
 "jq": r"含 $\max/\min$ 的二重积分：按「谁大」用对角直线分区域，分别去掉 max 直接积分（常先对固定变量求内层）。",
 "yc": r"分层后内层积分恰与外层变量无关（如 $\int_0^{2x}e^{4x^2}\mathrm dy=2xe^{4x^2}$），才能凑微分；两区域贡献相等。",
 "zy": r"$\frac12(e^4-1)$。",
},
10: {
 "gs": r"原极限 $=\iint_D\ln\frac{1+x}{1+y}\mathrm d\sigma$，$D=\{(x,y):0\le x\le1,1-x\le y\le1+x\}$；按 $y\in[0,1]$ 与 $[1,2]$ 拆域，对应选项 (A) 的两项积分。",
 "jq": r"双重和化二重积分：令 $x=i/n,y=j/n$，由 $n-i\le j\le n+i$ 得 $1-x\le y\le1+x$ 写成区域 $D$；再按 $y$ 范围拆块匹配定积分次序。",
 "yc": r"积分域是「以 $(x,1\pm x)$ 为边界」的菱形带；$y$ 总范围 $[0,2]$，拆 $y\in[0,1]$ 时 $x\in[1-y,1]$，$y\in[1,2]$ 时 $x\in[y-1,1]$。",
 "zy": r"选 (A)。",
},
11: {
 "gs": r"$x\ne0$ 时 $f(x)=\ln(1+x^2)-2+2x\arctan\frac1x$，$f(0)=-2$，$\lim_{x\to0}f=-2$ 连续；令 $g(x)=2x\arctan\frac1x$，则 $g'_+(0)=\pi,g'_-(0)=-\pi$ 故 $f'(0)$ 不存在。",
 "jq": r"含参积分在某点性态：先分部积分化显式，再用差商定义判 $f'(0)$（左右导数不等 $\Rightarrow$ 不可导）。",
 "yc": r"连续性看极限；可导性看 $g(x)=2x\arctan(1/x)$ 左右导数（$x\to0^+$ 时 $\arctan(1/x)\to\pi/2$，$x\to0^-$ 时 $\to-\pi/2$）。",
 "zy": r"选 (B)：连续但不可导。",
},
12: {
 "gs": r"$a_n=\sum\frac{k}{2n^2+k}$ 夹逼于 $\frac14$（上下界同趋于 1/4）；$b_n=\frac1n\sum\ln(1+\frac kn)\to\int_0^1\ln(1+x)\mathrm dx=2\ln2-1$。原式 $=1/4+2\ln2-1=2\ln2-3/4$。",
 "jq": r"和式拆两项：第一项夹逼（分母 $2n^2+k$ 用 $2n^2+n$ 与 $2n^2+1$ 包）、第二项定积分定义。",
 "yc": r"$a_n$ 夹逼用 $\frac{n(n+1)}{2}$ 求和 $\sum k$；第二项 $\ln((n+k)/n)^{1/n}=\frac1n\ln(1+k/n)$。",
 "zy": r"$2\ln2-\frac34$。",
},
},

"好题20-定积分与不定积分的基本运算": {
1: {
 "gs": r"令 $t=\sqrt x$，$x=t^2$，$\int\frac{2t}{(t+1)(t^2+3)}\mathrm dt$；部分分式 $\frac{2t}{(t+1)(t^2+3)}=\frac{-1/2}{t+1}+\frac{t/2+3/2}{t^2+3}$，积分得 $-\frac12\ln(1+\sqrt x)+\frac14\ln(x+3)+\frac{\sqrt3}{2}\arctan\frac{\sqrt x}{\sqrt3}+C$。",
 "jq": r"根式积分：令 $t=\sqrt x$ 化有理函数，再部分分式分解（二次因式配 $Bt+C$）。",
 "yc": r"部分分式系数 $A+B=0,B+C=2,3A+C=0\Rightarrow A=-1/2,B=1/2,C=3/2$；最后回代 $t=\sqrt x$。",
 "zy": r"结果如上式 $+C$。",
},
2: {
 "gs": r"注意 $\mathrm d(\frac1{1-x^2})=\frac{2x}{(1-x^2)^2}\mathrm dx$，原式 $=\frac12\int\ln(x+\sqrt{1+x^2})\,\mathrm d(\frac1{1-x^2})$，分部得 $\frac{\ln(\cdots)}{2(1-x^2)}+\frac12\int\frac{\mathrm dx}{(x^2-1)\sqrt{1+x^2}}$；令 $x=\tan t$ 解后者得 $\frac1{2\sqrt2}\ln|\frac{\sqrt2x-\sqrt{1+x^2}}{\sqrt2x+\sqrt{1+x^2}}|$。",
 "jq": r"含 $(1-x^2)^2$ 分母：先识别 $\mathrm d(1/(1-x^2))$ 凑微分，分部一次降次，再用三角代换 $x=\tan t$ 处理含 $\sqrt{1+x^2}$ 的剩余积分。",
 "yc": r"剩余积分令 $x=\tan t$ 后 $\sqrt{1+x^2}=\sec t$，化为 $\int\frac{\cos t}{2\sin^2t-1}\mathrm dt=\frac1{2\sqrt2}\ln|\frac{\sqrt2\sin t-1}{\sqrt2\sin t+1}|$。",
 "zy": r"原式 $=\frac{\ln(x+\sqrt{1+x^2})}{2(1-x^2)}+\frac1{4\sqrt2}\ln|\frac{\sqrt2x-\sqrt{1+x^2}}{\sqrt2x+\sqrt{1+x^2}}|+C$。",
},
3: {
 "gs": r"作 $t=\frac\pi2-x$，区间 $[\pi/6,\pi/3]$ 对称不变，且 $\tan^2(\pi/2-x)=\cot^2x=1/\tan^2x$，故 $I=\frac12\int\frac{f(\tan^2x)+f(1/\tan^2x)}{\sin2x}=\int\csc2x$。",
 "jq": r"对称区间 + $f(x)+f(1/x)=2$：用 $x\to\pi/2-x$ 换元把被积函数变 $f(1/\cdot)$，与原式相加除以 2 用题设消去 $f$。",
 "yc": r"区间 $[\pi/6,\pi/3]$ 关于 $x=\pi/4$ 对称，换元后仍同一区间；$\sin2(\pi/2-x)=\sin2x$ 不变。",
 "zy": r"填 $\frac{\ln3}{2}$。",
},
4: {
 "gs": r"区域 $0\le x\le1,0\le y\le\sqrt x$ 即 $0\le y\le1,y^2\le x\le1$。交换后 $I=\int_0^1(1-y^2)e^{-y^2/2}\mathrm dy=\int e^{-y^2/2}+\int y\,\mathrm d(e^{-y^2/2})=\int_0^1e^{-y^2/2}+[y e^{-y^2/2}]_0^1-\int e^{-y^2/2}=e^{-1/2}$。",
 "jq": r"内层积分 $\int e^{-y^2/2}$ 算不出，必须交换积分次序把 $e^{-y^2/2}$ 提到外层；交换后配出 $\mathrm d(e^{-y^2/2})$ 抵消第一项。",
 "yc": r"$\int_0^1(1-y^2)e^{-y^2/2}\mathrm dy$ 拆两项，第二项分部使 $e^{-y^2/2}$ 积分与第一项恰好消去，只剩边界 $e^{-1/2}$。",
 "zy": r"填 $e^{-1/2}$。",
},
5: {
 "gs": r"（Ⅰ）作 $x\to-x$ 得 $\int_{-a}^a fg=\int_{-a}^a f(m-g)=m\int f-\int fg$，移项 $\int fg=\frac m2\int f$。（Ⅱ）取 $f=\frac{x\sin x}{\cos^2x+1}$（偶），$g=\frac1{e^x+1}$（$g+g_-=1$），由（Ⅰ）$I=\frac12\int_{-\pi}^\pi\frac{x\sin x}{\cos^2x+1}=\int_0^\pi\frac{x\sin x}{\cos^2x+1}\xlongequal{区间再现}\frac\pi2\int_0^\pi\frac{\sin x}{\cos^2x+1}=\frac{\pi^2}{4}$。",
 "jq": r"（Ⅰ）对称积分配偶性技巧；（Ⅱ）识别 $g(x)+g(-x)=1$ 后用（Ⅰ），再用「区间再现」$x\to\pi-x$ 把 $\int_0^\pi x\cdot h(x)=\frac\pi2\int_0^\pi h$。",
 "yc": r"区间再现公式 $\int_0^\pi xf(\sin x)\,\mathrm dx=\frac\pi2\int_0^\pi f(\sin x)$；这里 $-\int_0^\pi\frac{\mathrm d\cos x}{\cos^2x+1}=-\arctan(\cos x)|_0^\pi=\pi^2/4$。",
 "zy": r"（Ⅰ）证；（Ⅱ）$I=\frac{\pi^2}{4}$。",
},
6: {
 "gs": r"法一先求 $\int\ln(1+x^2)=x\ln(1+x^2)-2x+2\arctan x$，对原式分部，得 $\frac\pi4(\ln2-2)+\frac{\pi^2}{16}-\frac14\ln^22+\ln2$；两法结果一致（≈0.163）。",
 "jq": r"对数×反三角乘积：标准分部积分，选 $u=\arctan x$ 或 $u=\ln(1+x^2)$ 都行，关键先用不定积分备好另一函数的原函数。",
 "yc": r"法二先求 $\int\arctan x=x\arctan x-\frac12\ln(1+x^2)$；注意 $(\arctan x)^2$ 边界项与 $\frac14\ln^22$ 项；两法交叉验证防算错。",
 "zy": r"原式 $=\frac\pi4\ln2-\frac\pi2+\frac{\pi^2}{16}+\ln2-\frac14\ln^22$。",
},
7: {
 "gs": r"$D=[0,\sqrt\pi]^2$，$D_0:0\le y\le x\le\sqrt\pi$。由轮换对称 $I_1=2\iint_{D_0}\sin x^2=2\int_0^{\sqrt\pi}x\sin x^2=2$；$I_2=2\iint_{D_0}\sin y^2=2\int_0^{\sqrt\pi}(\sqrt\pi-y)\sin y^2=2\sqrt\pi\int_0^{\sqrt\pi}\sin y^2-2$。再证 $\int_0^{\sqrt\pi}\sin y^2<\frac2{\sqrt\pi}\Rightarrow I_2<2=I_1$。",
 "jq": r"含 max/min 的二重积分：用轮换对称性各化到 $x\ge y$ 三角域，去掉 max/min；$I_2$ 用变量代换 + 不等式放缩。",
 "yc": r"$I_1$ 恰好等于 2（$\int_0^{\sqrt\pi}x\sin x^2=\frac12(1-\cos\pi)=1$）；$I_2$ 比较靠 $\int_0^{\sqrt\pi}\sin y^2<\frac2{\sqrt\pi}$（经 $t=y^2$ 换元、分部、对称代换放缩）。",
 "zy": r"证得 $I_2<I_1$。",
},
8: {
 "gs": r"（Ⅱ）设 $x=nT+r$，$\int_0^xf=n\int_0^Tf+\int_0^rf$，除以 $x$ 取极限得 $\frac1T\int_0^Tf$。（Ⅲ）两被积均以 $\pi$ 为周期，先算 $\int_0^\pi\frac1{1+\cos^2t}=\frac{\sqrt2}{2}\pi$、$\int_0^\pi\frac{\sin^2t}{1+\cos^2t}=(\sqrt2-1)\pi$，再用（Ⅱ）得比值 $\frac{\sqrt2-1}{\sqrt2/2}=2-\sqrt2$。",
 "jq": r"周期函数积分平均：拆成整数个周期 + 余段，余段有界，除以 $x$ 趋 0；应用（Ⅲ）先算一个周期内积分再比值。",
 "yc": r"算 $\int_0^\pi\frac1{1+\cos^2t}$ 令 $u=\tan t$ 得 $\frac{\sqrt2}{2}\pi$；$\frac{\sin^2}{1+\cos^2}=2\cdot\frac1{1+\cos^2}-\pi$。",
 "zy": r"（Ⅱ）证；（Ⅲ）$2-\sqrt2$。",
},
9: {
 "gs": r"分子分母同除 $(x+3)^2$，注意 $\left(\frac{x^2+x}{x+3}\right)'=\frac{x^2+6x+3}{(x+3)^2}$，故原式 $=\int_0^1\frac{\mathrm d(\frac{x^2+x}{x+3})}{1+(\frac{x^2+x}{x+3})^2}=\arctan(\frac{x^2+x}{x+3})|_0^1=\arctan\frac12$。",
 "jq": r"「分式分子恰是某商的导数的分子」——同除分母平方构造 arctan 凑微分；识别 $\frac{u'}{1+u^2}$ 形式。",
 "yc": r"同除 $(x+3)^2$ 后分子需等于 $\frac{x^2+x}{x+3}$ 的导数；验证导数 $= (x^2+6x+3)/(x+3)^2$ 吻合。",
 "zy": r"填 $\arctan\frac12$。",
},
10: {
 "gs": r"$x'(t)=2e^{2t}-1,y'(t)=2e^t$，$s=\int_{\frac14\ln2}^{\frac14\ln6}\sqrt{1+4e^{4t}}\,\mathrm dt$；令 $u=\sqrt{1+4e^{4t}}$，$t=\frac14\ln2$ 时 $u=3$、$t=\frac14\ln6$ 时 $u=5$，积分得 $\frac12\int_3^5(1+\frac1{u^2-1})\mathrm du=1+\frac14\ln\frac43$。",
 "jq": r"参数方程路程 $=\int\sqrt{x'^2+y'^2}\mathrm dt$；根号内配方化简后令 $u=\sqrt{1+4e^{4t}}$ 把积分化为有理式。",
 "yc": r"根号内 $(2e^{2t}-1)^2+4e^{2t}=1+4e^{4t}$（交叉项抵消）；换元后 $u=3,5$，积分 $\frac12[u+\frac12\ln\frac{u-1}{u+1}]_3^5$。",
 "zy": r"$1+\frac14\ln\frac43$。",
},
},

"好题21-积分中值问题": {
1: {
 "gs": r"$g(x)=\int_0^x\mathrm du\int_0^{u^2}f(t,u)\,\mathrm dt$，$g'(x)=\int_0^{x^2}f(t,x)\,\mathrm dt=f(\xi,x)x^2$（$0<\xi<x^2$）。由切线条件 $f(0,0)=0,f'_y(0,0)=1$，$g'(x)\sim x^3$，$g(x)\sim\frac14x^4$。故 $a=1/4,b=4$。",
 "jq": r"含参变限积分求导后用积分中值定理；$g'(x)$ 中 $\xi=o(x)$ 使 $\xi$ 项可略，主导为 $f'_y(0,0)x^3$；再积分一次升一阶。",
 "yc": r"$f(0,0)=0$ 才使 $g'(x)\sim f'_y(0,0)x^3$；等价无穷小 $g(x)\sim\frac14x^4$（$b=4$ 比 $g'$ 的 3 高一阶）。",
 "zy": r"$a=\frac14,b=4$。",
},
},

"好题22-反常积分": {
1: {
 "gs": r"换元 $x=e^t$，拆 $I_1(t\to-\infty)$、$I_2,I_3(t\to0^\pm)$。$t\to0^\pm$ 时 $e^t/|t|^a\sim1/|t|^a$，故 $a<1$ 收敛；$t\to-\infty$ 时 $e^t\to0$ 占优，$I_1$ 恒收敛。综合 $a<1$。",
 "jq": r"瑕点 $x=1$（$\ln x=0$）把积分拆 $x<1$ 与 $x>1$ 两段，分别在 $t\to0^\mp$ 用 $p$ 积分判别；无穷限段 $I_1$ 因 $e^t$ 衰减恒收敛。",
 "yc": r"关键等价 $x\to1$ 即 $t\to0$ 时 $|\ln x|^a\sim|t|^a$，收敛条件 $a<1$；$x\to0^+$ 对应 $t\to-\infty$ 也收敛。",
 "zy": r"选 (B)：$a<1$。",
},
2: {
 "gs": r"①$\lim xf(x)=+\infty\Rightarrow f(x)\sim\frac1x$（更强）发散⇒真。②反例 $f=1/(x\ln x)$（$x>2$）使 $\lim xf=0$ 但 $\int$ 发散⇒假。③逆否：若 $\int\sqrt f$ 收敛，则 $x$ 大时 $f<1/2$，有 $f<\sqrt f$，比较得 $\int f$ 收敛⇒真。",
 "jq": r"极限审敛法 + 反例构造：①用比较判别（与 $1/x$）；②/③用反例或逆否命题（用「无穷远 $f\to0$ 故 $f<1$ 从而 $f<\sqrt f$」）。",
 "yc": r"②反例 $1/(x\ln x)$ 积分发散（$\ln\ln x$）；③不能直证原命题，转逆否更顺，且用到「$\lim f=0$ ⇒ 大 $x$ 处 $f<1$」。",
 "zy": r"选 (C)：2 个真命题（①③）。",
},
3: {
 "gs": r"①反例 $f=1/(x+1)$：$f^2$ 收敛但 $\int f$ 发散⇒假。②若 $\exists p>1$ 使 $\lim x^pf$ 存在，由极限审敛法 $\int f$ 收敛⇒真。③反例 $f=1/((x+2)\ln^2(x+2))$：$\int f$ 收敛但任意 $p>1$ 都 $\lim x^pf=+\infty$⇒假。",
 "jq": r"用极限审敛法判②（真）；用反例判①（取 $1/(x+1)$，$f^2\sim1/(x+1)^2$ 收敛而 $f$ 发散）、③（取慢收敛分母 $\ln^2$ 使 $x^pf$ 永不收敛）。",
 "yc": r"③反例关键：分母 $(x+2)\ln^2(x+2)$ 使 $\int f$ 收敛（~$1/\ln$ 积分），但 $x^pf$ 增长无界；①反例 $1/(x+1)$ 最经典。",
 "zy": r"选 (B)：1 个真命题（②）。",
},
4: {
 "gs": r"被积无定义点 $t_k=2k\pi+\pi/2$，最近两点 $\pi/2,-3\pi/2$。$t=\pi/2$ 处被积 $\sim(\pi/2-t)^{-2/3}$（$p=2/3<1$）收敛；$t=-3\pi/2$ 处 $\sim(t+3\pi/2)^{-2}$（$p=2>1$）发散；同理 $5\pi/2$ 发散。故定义域 $(-3\pi/2,5\pi/2)$。",
 "jq": r"变限积分定义域=积分路径上所有瑕点间最大连续区间。在每点用「阶判别」（比较 $(t-t_0)^\alpha$）定收敛/发散。",
 "yc": r"收敛判据：被积 $\sim(t-t_0)^{-p}$，反常积分收敛 $\iff p<1$；本题 $\pi/2$ 处 $p=2/3<1$ 可穿过，$-3\pi/2,5\pi/2$ 处 $p=2>1$ 截断。",
 "zy": r"选 (A)：$(-3\pi/2,5\pi/2)$。",
},
5: {
 "gs": r"瑕点 $x\to0^+$。令 $y=m/x$，$x=m/y$，原式 $=m^{3/2}\int_{m/n}^{+\infty}\frac{[y]}{y^{5/2}}\mathrm dy$。$[y]\le y\Rightarrow\frac{[y]}{y^{5/2}}\le\frac1{y^{3/2}}$，而 $\int_{m/n}^{+\infty}y^{-3/2}$ 收敛，由比较判别原积分恒收敛，与 $m,n$ 无关。",
 "jq": r"含取整函数 $[m/x]$ 的积分：先换元 $y=m/x$ 把取整移到分子，再用 $[y]\le y$ 放缩成 $p=3/2>1$ 的收敛 $p$ 积分。",
 "yc": r"瑕点在 $x=0^+$（$[m/x]\to\infty$）；换元后下限 $m/n$ 有限、上限无穷，关键 $[y]/y^{5/2}\le1/y^{3/2}$ 保证收敛。",
 "zy": r"选 (D)：与 $m,n$ 均无关（恒收敛）。",
},
},

}
