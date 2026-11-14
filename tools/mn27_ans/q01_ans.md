===Q1===
【答案】C
【解】
**① 按 $|x|$ 与 1 的大小求点态极限。** 先固定 $x$ 令 $n\to\infty$：$f(x)=\lim\limits_{n\to\infty}\dfrac{2x^{2n}-1}{x^{2n}+1}\sin\dfrac1x$。当 $0<|x|<1$ 时 $x^{2n}\to0$，分式趋于 $-1$；当 $|x|>1$ 时分子分母同除以 $x^{2n}$，分式趋于 $2$；当 $|x|=1$ 时 $x^{2n}=1$，分式恒为 $\dfrac12$。故
$$f(x)=\begin{cases}-\sin\dfrac1x,&0<|x|<1,\\[3pt]\dfrac12\sin\dfrac1x,&|x|=1,\\[3pt]2\sin\dfrac1x,&|x|>1.\end{cases}$$
**② 判断 $x=1$ 与 $x=-1$。** 在 $x=1$ 处左极限为 $-\sin1$、右极限为 $2\sin1$，均有限但不等，是跳跃间断点；在 $x=-1$ 处左极限为 $-2\sin1$、右极限为 $\sin1$，同样为跳跃间断点。二者都属于第一类。
**③ 检查 $x=0$ 及其他点。** 在 0 附近 $f(x)=-\sin\dfrac1x$，取 $x_k=\dfrac{1}{\pi/2+2k\pi}$、$z_k=\dfrac{1}{3\pi/2+2k\pi}$ 均趋于 $0^+$，但函数值分别为 $-1$、$1$，右极限不存在，属振荡型间断点，不是第一类；其余点落在某个连续分段内部，无新间断点。故第一类间断点共 2 个，选 C。
【思路】先固定 $x$ 求点态极限得到分段函数，再逐个考察分段点处的左右极限判定间断类型。
【易错】第一类间断点要求左右极限都存在且有限（含可去、跳跃两类），函数在某点未定义并不自动说明它属于哪一类，要看邻近极限。另：题面分子是 $2x^{2n}-1$，其中 $-1$ 不是指数的一部分；若误读成 $2x^{2n-1}$，则 $0<|x|<1$ 时分式趋于 $0$，与原册三段极限结论 $-1,\dfrac12,2$ 矛盾。

===Q2===
【答案】A
【解】
**① 把趋于 0 的量单独记成函数并乘积分因子。** 令 $g(x)=f(x)+f'(x)$，则 $g(x)\to0$，且 $f'(x)+f(x)=g(x)$。两边乘积分因子 $\mathrm{e}^x$，左边变为 $[\mathrm{e}^x f(x)]'$，故
$$\mathrm{e}^x f(x)-f(0)=\int_0^x \mathrm{e}^t g(t)\,\mathrm{d}t,\qquad f(x)=\mathrm{e}^{-x}f(0)+\mathrm{e}^{-x}\int_0^x \mathrm{e}^t g(t)\,\mathrm{d}t.$$
**② 把积分分成固定段与尾段。** 任取 $\varepsilon>0$，由 $g(t)\to0$ 存在 $M$ 使 $t\ge M$ 时 $|g(t)|<\varepsilon$；对 $x\ge M$，
$$f(x)=\mathrm{e}^{-x}\left[f(0)+\int_0^M \mathrm{e}^t g(t)\,\mathrm{d}t\right]+\mathrm{e}^{-x}\int_M^x \mathrm{e}^t g(t)\,\mathrm{d}t.$$
方括号内为固定常数，第一项趋于 0；第二项满足
$$\left|\mathrm{e}^{-x}\int_M^x \mathrm{e}^t g(t)\,\mathrm{d}t\right|\le\varepsilon\,\mathrm{e}^{-x}\int_M^x \mathrm{e}^t\,\mathrm{d}t=\varepsilon\left(1-\mathrm{e}^{M-x}\right)\le\varepsilon.$$
**③ 得出极限与渐近线。** 故当 $x$ 充分大时 $|f(x)|$ 被一个趋于 0 的量与任意小的 $\varepsilon$ 控制，即 $f(x)\to0$。按水平渐近线定义 $y=0$ 成立，选 A。
【思路】用积分因子把微分关系写成积分表达式，再按固定段与尾段分离估计，证明 $f(x)\to0$。
【易错】不能由 $f+f'\to0$ 直接断言 $f\to0$ 与 $f'\to0$：两个量之和趋于 0，两个量未必分别趋于 0；本题要借助二者之间的微分关系和积分因子才能得结论。

===Q3===
【答案】C
【解】
**① 按 $t$ 的正负去绝对值。** $x=2t-|t|$，$y=t|\mathrm{e}^t-1|$。当 $t\ge0$ 时 $x=t$、$\mathrm{e}^t-1\ge0$，故 $y=t(\mathrm{e}^t-1)$；当 $t<0$ 时 $x=3t$、$\mathrm{e}^t-1<0$，故 $y=t(1-\mathrm{e}^t)$。因此
$$f(x)=\begin{cases}x(\mathrm{e}^x-1),&x\ge0,\\[3pt]\dfrac{x}{3}\left(1-\mathrm{e}^{x/3}\right),&x<0.\end{cases}$$
**② 按定义求 $f'(0)$。** $f(0)=0$，右侧差商为 $\mathrm{e}^x-1\to0$，左侧差商为 $\dfrac{1-\mathrm{e}^{x/3}}{3}\to0$，所以 $f'(0)=0$。
**③ 求两侧的 $f'(x)$ 并检查连续性。** 在 $x\ne0$ 时，
$$f'(x)=\begin{cases}\mathrm{e}^x-1+x\mathrm{e}^x,&x>0,\\[3pt]\dfrac13\left(1-\mathrm{e}^{x/3}\right)-\dfrac{x}{9}\mathrm{e}^{x/3},&x<0.\end{cases}$$
令 $x\to0^\pm$，两边均趋于 0 即 $f'(0)$，故 $f'$ 连续。
**④ 检查 $f'$ 在 0 处能否再求导。** 右侧 $f'(x)=2x+O(x^2)$；左侧用 $\mathrm{e}^{x/3}=1+\dfrac{x}{3}+O(x^2)$，得 $f'(x)=-\dfrac{x}{9}-\dfrac{x}{9}+O(x^2)=-\dfrac{2}{9}x+O(x^2)$。因此 $\lim\limits_{x\to0^+}\dfrac{f'(x)}{x}=2$、$\lim\limits_{x\to0^-}\dfrac{f'(x)}{x}=-\dfrac29$ 不相等，$f''(0)$ 不存在。选 C。
【思路】按 $t\ge0$、$t<0$ 去绝对值写出分段 $f(x)$，用差商求 $f'(0)$ 并验证 $f'$ 连续，再比较 $f'(x)/x$ 的左右极限判定可导性。
【易错】「$f$ 可导」「$f'$ 连续」「$f'$ 可导」是三个不同层次。分段点处不能只把 $x=0$ 代入某一侧导数公式，必须先比较左右差商。

===Q4===
【答案】C
【解】
**① 从给定极限得到低阶导数。** 因 $f'(x)=x^2(1+o(1))\to0$，由连续性得 $f'(0)=0$；再由
$$f''(0)=\lim_{x\to0}\frac{f'(x)-f'(0)}{x}=\lim_{x\to0}\frac{x\,f'(x)}{x^2}=0.$$
**② 确定三阶导数。** 对 $f'$ 在 0 展开到二阶：$f'(x)=f'(0)+f''(0)x+\dfrac12 f'''(0)x^2+o(x^2)$。代入前两项均为 0 并除以 $x^2$，题给极限 1 意味着 $\dfrac{f'''(0)}{2}=1$，故 $f'''(0)=2$。
**③ 用二阶导数的变号判断拐点。** 由 $f'''(0)=2$，$f''(x)=f''(0)+f'''(0)x+o(x)=2x+o(x)$。在充分小的左邻域 $f''<0$、右邻域 $f''>0$，凹凸性改变，故 $(0,f(0))$ 为拐点。
**④ 排除极值。** 因 $f'(x)/x^2\to1>0$，在 0 的充分小去心邻域里左右两侧都有 $f'(x)>0$，函数经过 0 仍递增，没有由增变减或由减变增，故 $f(0)$ 不是极值。选 C。
【思路】由 $f'(x)/x^2\to1$ 结合泰勒展开定出 $f'(0)=f''(0)=0$、$f'''(0)=2$，再用 $f''$ 变号判拐点、由 $f'>0$ 排除极值。
【易错】驻点只表示 $f'=0$：典型情形 $x^3$ 在 0 导数为 0 却无极值而有拐点。本题 $f'$ 呈 $x^2$ 型、$f''$ 呈 $x$ 型，是同一种局部结构。

===Q5===
【答案】D
【解】
**① 把无穷上限换成有限数 $R$。** 0 处无奇点，只需考察
$$I(R)=\int_0^R\left(\frac{ax}{1+x^2}-\frac{1}{1+2x}\right)\mathrm{d}x.$$
第一项令 $u=1+x^2$、第二项令 $v=1+2x$，得 $I(R)=\dfrac{a}{2}\ln(1+R^2)-\dfrac12\ln(1+2R)$。
**② 分离会发散的 $\ln R$ 项。** 对 $R>0$，$\ln(1+R^2)=2\ln R+\ln(1+R^{-2})$，$\ln(1+2R)=\ln R+\ln(2+R^{-1})$，所以
$$I(R)=\left(a-\frac12\right)\ln R+\frac a2\ln(1+R^{-2})-\frac12\ln(2+R^{-1}).$$
后两项有有限极限，要使整体收敛必须 $a-\dfrac12=0$，即 $a=\dfrac12$。
**③ 代入并取极限。** 代 $a=\dfrac12$ 后第一项消失，余下两项分别趋于 $0$ 与 $-\dfrac12\ln2$，故 $I=-\dfrac12\ln2$，选 D。
【思路】以共同截断上限 $R$ 保留两个发散积分，分离出 $\ln R$ 项，令其系数为 0 定出 $a$，再取极限求值。
【易错】两个分别发散的积分不能拆开相减成「$\infty-\infty$」。应保留共同截断上限 $R$，先合并或抵消再取极限。

===Q6===
【答案】B
【解】
**① 分别算四个偏导。** 记 $w=\mathrm{e}^{\alpha x+\beta y}$，有 $w_x=\alpha w$、$w_y=\beta w$。乘积法则给出
$$u_x=w(v_x+\alpha v),\quad u_y=w(v_y+\beta v),\quad u_{xx}=w(v_{xx}+2\alpha v_x+\alpha^2 v),\quad u_{yy}=w(v_{yy}+2\beta v_y+\beta^2 v).$$
二阶偏导中的 $2\alpha v_x$ 来自对两个乘积项分别求导后相加，不能漏掉系数 2。
**② 代回并按 $v$ 的导数分类。** 约去恒非零的 $w$，得
$$0=v_{xx}-v_{yy}+(2\alpha+a)v_x+(-2\beta+a)v_y+\left[\alpha^2-\beta^2+a(\alpha+\beta)\right]v.$$
**③ 让不需要的一阶项系数为 0。** 要求 $2\alpha+a=0$、$-2\beta+a=0$，故 $\alpha=-\dfrac a2$、$\beta=\dfrac a2$。
**④ 核查零阶项是否也消失。** 代入得 $\alpha^2-\beta^2=0$、$\alpha+\beta=0$，所以 $v$ 的系数也为 0，剩下的方程恰为 $v_{xx}-v_{yy}=0$。选 B。
【思路】用乘积法则完整展开 $u=vw$ 的各阶偏导，按 $v_{xx},v_{yy},v_x,v_y,v$ 分类，令多余项系数全为 0 定出 $\alpha,\beta$。
【易错】换元题不能只比较两个一阶导数系数就停止，还要检查零阶项。这里 $-u_{yy}$ 前的负号决定了 $v_y$ 系数是 $-2\beta+a$，并非 $2\beta+a$。

===Q7===
【答案】A
【解】
**① 把原来的积分限写成区域不等式。** 由 $I=\int_0^{\pi/2}\mathrm{d}\theta\int_0^{\sqrt{\sin2\theta}}f(\theta,r)r\,\mathrm{d}r$ 得 $0\le\theta\le\dfrac\pi2$、$0\le r$、$r^2\le\sin2\theta$。因 $\sin2\theta$ 最大值为 1，半径的整体范围是 $0\le r\le1$。
**② 固定 $r$，求允许的 $\theta$。** 令 $\phi=2\theta\in[0,\pi]$，对固定 $r$，$\sin\phi\ge r^2\iff\arcsin r^2\le\phi\le\pi-\arcsin r^2$。两边除以 2 得
$$\frac12\arcsin r^2\le\theta\le\frac\pi2-\frac12\arcsin r^2.$$
**③ 按新顺序写积分。** 外层 $r$ 从 0 到 1，内层 $\theta$ 按上面的区间变化，被积函数仍是 $f(\theta,r)\,r$，由此得
$$I=\int_0^1\mathrm{d}r\int_{\frac12\arcsin r^2}^{\frac\pi2-\frac12\arcsin r^2}f(\theta,r)\,r\,\mathrm{d}\theta.$$
选 A。
【思路】把原积分限转成区域不等式，固定 $r$ 后从 $r^2\le\sin2\theta$ 反解出 $\theta$ 的双侧边界，再交换积分次序。
【易错】在 $[0,\pi]$ 上解 $\sin\phi\ge c$ 有左右两个边界，不能只保留 $\phi\ge\arcsin c$。这里只是交换已有变量的积分次序、没有再次做坐标变换，所以不要额外再乘一个 $r$。

===Q8===
【答案】B
【解】
**① 把线性表示写成方程组。** 设 $\beta=c_1\alpha_1+c_2\alpha_2+c_3\alpha_3$，其中 $\beta=(a,1,1)^{\mathrm{T}}$、$\alpha_1=(b,0,1)^{\mathrm{T}}$、$\alpha_2=(1,b-1,1)^{\mathrm{T}}$、$\alpha_3=(1,0,b)^{\mathrm{T}}$，即
$$\begin{cases}b c_1+c_2+c_3=a,\\[2pt](b-1)c_2=1,\\[2pt]c_1+c_2+b c_3=1.\end{cases}$$
「不唯一」意味着系数矩阵不可逆，因而
$$\begin{vmatrix}b&1&1\\0&b-1&0\\1&1&b\end{vmatrix}=(b-1)(b^2-1)=0,$$
所以 $b=1$ 或 $b=-1$。
**② 用有解条件排除 $b=1$。** 若 $b=1$，方程组第二行变为 $0=1$，无解。故只能 $b=-1$，第二行给 $c_2=-\dfrac12$。
**③ 求 $a$ 并验证不唯一。** 将第一行和第三行相加，$c_1,c_3$ 消去，得 $2c_2=a+1$，代入 $c_2=-\dfrac12$ 得 $a=-2$。在 $a=-2,b=-1$ 下方程要求 $c_3=c_1-\dfrac32$，令 $c_1=s$ 则
$$(c_1,c_2,c_3)=\left(s,-\frac12,s-\frac32\right),\quad s\in\mathbb{R},$$
存在自由参数，确有无穷多种表示。选 B。
【思路】「表示不唯一」要求方程组有解且系数矩阵不可逆；由行列式为 0 得 $b$ 的候选，再用相容性排除 $b=1$，最后定 $a$ 并写出通解。
【易错】行列式为 0 只说明「不可能唯一」，还可能根本无解。本题必须继续利用 $\beta$ 的分量检查相容性，不能一算出 $b=\pm1$ 就结束。

===Q9===
【答案】D
【解】
**① 先研究最简单的相似代表。** 设 $A=SBS^{-1}$，$S$ 可逆。其中
$$B=\begin{pmatrix}\lambda_0&1&0\\0&\lambda_0&0\\0&0&\lambda_0\end{pmatrix},\qquad N=A-\lambda_0 E,\quad N_0=B-\lambda_0 E=\begin{pmatrix}0&1&0\\0&0&0\\0&0&0\end{pmatrix},$$
则 $N=SN_0S^{-1}$。观察 $N_0$ 只有一个非零列，故 $r(N_0)=1$；直接相乘得 $N_0^2=O$，从而 $N_0^3=O$。
**② 把秩与幂的结论转移到 $N$。** 左右乘可逆矩阵不改变秩，所以 $r(N)=1$；又
$$N^2=SN_0S^{-1}SN_0S^{-1}=SN_0^2S^{-1}=O,$$
同理 $N^3=O$。因此命题②③④正确。
**③ 检查非零列是否为特征向量。** 设 $c$ 是 $N$ 的第 $j$ 个非零列，即 $c=N e_j$（$e_j$ 为第 $j$ 个标准单位向量），则
$$(A-\lambda_0 E)c=Nc=N^2 e_j=0,$$
所以 $Ac=\lambda_0 c$。由于已要求 $c\ne0$，它确实是特征向量，命题①也正确。四个命题全部成立，选 D。
【思路】把 $A$ 相似到最简代表 $B$，研究 $N_0=B-\lambda_0E$ 的秩与幂零性，再借可逆相似变换把结论转移到 $N=A-\lambda_0E$。
【易错】采用已确认勘误：$B$ 的第 2 行第 3 列为 0，重排稿误写的 1 已纠正；该元素会改变矩阵平方与秩，不能沿用错误矩阵的推导（本解已按第 2 行第 3 列为 0 转写）。另：一个向量成为特征向量必须「非零」且满足 $Ac=\lambda c$；$N^2=O$ 意味着 $N$ 的每一列被 $N$ 再次作用后变为 0，正好与本题第一个命题对应。

===Q10===
【答案】D
【解】
**① 把文字条件写成式子。** 「$\alpha$ 不是 $A^2X=0$ 的解」表示 $A^2\alpha\ne0$；「$A\alpha$ 是解」表示 $A^2(A\alpha)=A^3\alpha=0$。同时 $A\alpha\ne0$，否则再次乘 $A$ 会使 $A^2\alpha=0$，矛盾。
**② 用线性无关的定义。** 设 $c_1A\alpha+c_2A^2\alpha=0$，两边左乘 $A$ 得 $c_1A^2\alpha+c_2A^3\alpha=0$。第二项为 0，而 $A^2\alpha\ne0$，故 $c_1=0$。
**③ 回代求另一个系数。** 代回原线性组合得 $c_2A^2\alpha=0$，所以 $c_2=0$。只有全零系数组合才为 0，故 $A\alpha$ 与 $A^2\alpha$ 线性无关，选 D。
【思路】把「是不是解」翻译成 $A^m\alpha=0$ 的幂零链，设线性组合后左乘 $A$ 逐层消去系数。
【易错】遇到 $A^m\alpha=0$ 但 $A^{m-1}\alpha\ne0$，可反复左乘 $A$ 从最高次处逐层消去系数。这里不能把 $A^2\alpha\ne0$ 误写成 $A^2\ne0$ 后就忘记它对特定向量的作用。

===Q11===
【答案】$2(\mathrm{e}-1)$
【解】
**① 令 $x=0$ 求 $f(0)$。** 由题给关系 $\int_1^{x+f(x)}\mathrm{e}^{-t^2}\,\mathrm{d}t=x+\int_0^x x\sin t^2\,\mathrm{d}t$，右边在 $x=0$ 时为 0，故 $\int_1^{f(0)}\mathrm{e}^{-t^2}\,\mathrm{d}t=0$。被积函数始终为正，只有上下限相同时积分为 0，所以 $f(0)=1$。
**② 求 $f'(0)$。** 记 $J(x)=\int_0^x\sin t^2\,\mathrm{d}t$，右边为 $x+xJ(x)$。两边求导得
$$\mathrm{e}^{-(x+f(x))^2}\left[1+f'(x)\right]=1+J(x)+x\sin x^2.$$
代 $x=0$，$J(0)=0$ 且 $f(0)=1$，所以 $\mathrm{e}^{-1}[1+f'(0)]=1$，解得 $f'(0)=\mathrm{e}-1$。
**③ 凑导数差商。** 因 $2/n\to0$，
$$n\left[f\!\left(\frac2n\right)-1\right]=2\cdot\frac{f(2/n)-f(0)}{2/n}\longrightarrow 2f'(0)=2(\mathrm{e}-1).$$
【思路】用导数定义把 $n[f(2/n)-1]$ 凑成 $2f'(0)$，而 $f'(0)$ 由隐式变上限积分关系两边求导得到。
【易错】数列极限 $n[f(c/n)-f(0)]$ 常等于 $cf'(0)$，但必须先确认常数项正是 $f(0)$。变上限为 $x+f(x)$ 时，链式法则带来 $1+f'(x)$，不能只写 $f'(x)$。

===Q12===
【答案】$\dfrac{2\mathrm{e}^{\pi/2}}{\pi}$
【解】
**① 写平均值公式。** $f(x)=\dfrac{\mathrm{e}^x(1+\sin x)}{1+\cos x}$，区间长度为 $\dfrac\pi2$，所以
$$\bar f=\frac{2}{\pi}\int_0^{\pi/2}\frac{\mathrm{e}^x(1+\sin x)}{1+\cos x}\,\mathrm{d}x.$$
**② 用半角恒等式寻找乘积导数。** 有 $\tan\dfrac x2=\dfrac{\sin x}{1+\cos x}$，且 $\left(\tan\dfrac x2\right)'=\dfrac12\sec^2\dfrac x2=\dfrac{1}{1+\cos x}$。乘积法则给出
$$\left(\mathrm{e}^x\tan\frac x2\right)'=\mathrm{e}^x\frac{\sin x}{1+\cos x}+\mathrm{e}^x\frac{1}{1+\cos x}=f(x).$$
**③ 代入上下限。** $\tan0=0$、$\tan\dfrac\pi4=1$，故原积分为 $\mathrm{e}^{\pi/2}$，平均值为 $\dfrac{2\mathrm{e}^{\pi/2}}{\pi}$。
【思路】由半角公式识别 $\dfrac{1+\sin x}{1+\cos x}=\tan\dfrac x2+\left(\tan\dfrac x2\right)'$，凑出原函数 $\mathrm{e}^x\tan\dfrac x2$ 后除以区间长度。
【易错】平均值不是函数在区间中点的值，也不只是定积分值。看到 $1+\cos x$ 可联想半角公式；若又有 $\mathrm{e}^x$，尝试寻找 $(\mathrm{e}^x g)'=\mathrm{e}^x(g+g')$ 的结构。

===Q13===
【答案】$y=x+2-x\mathrm{e}^x$
【解】
**① 恢复 $a,b$。** 齐次方程 $y''+ay'+by=0$ 通解为 $(C_1+C_2x)\mathrm{e}^x$，说明特征根 1 为二重根，特征多项式 $(r-1)^2=r^2-2r+1$，所以 $a=-2$、$b=1$，方程为 $y''-2y'+y=x$。
**② 为非齐次项 $x$ 设多项式特解。** 设 $y_p=ux+v$，则 $y_p'=u$、$y_p''=0$，代入得 $ux+(v-2u)=x$。比较系数得 $u=1$、$v=2$，取 $y_p=x+2$。
**③ 写完整通解并求常数。** $y=(C_1+C_2x)\mathrm{e}^x+x+2$，$y'=(C_1+C_2+C_2x)\mathrm{e}^x+1$。令 $x=0$，由 $y(0)=2$ 得 $C_1=0$；再由 $y'(0)=0$ 得 $C_1+C_2+1=0$，故 $C_2=-1$。代回得 $y=x+2-x\mathrm{e}^x$。
【思路】由齐次通解反推特征方程与系数 $a,b$，设一次多项式特解，再用两个初值定出 $C_1,C_2$。
【易错】非齐次方程的解是「齐次通解＋一个非齐次特解」。右端为一次多项式可先设一次多项式；若 0 恰为齐次特征根，才需要再乘 $x$ 调整，本题 0 不是特征根，所以不需调整。

===Q14===
【答案】$0$
【解】
**① 写变限积分求导公式。** 对 $F(x)=\int_{a(x)}^{b(x)}h(x,t)\,\mathrm{d}t$，$F'(x)=h(x,b(x))b'(x)-h(x,a(x))a'(x)+\int_{a(x)}^{b(x)}h_x(x,t)\,\mathrm{d}t$。此处 $f(x,y)=\int_{x/y}^{xy}(x-yt)\varphi(t)\,\mathrm{d}t$，把 $y$ 视为常数，上限导数为 $y$、下限导数为 $1/y$，被积函数对 $x$ 的偏导为 $\varphi(t)$。
**② 求 $f_x$。** 在上限 $t=xy$ 处 $x-yt=x(1-y^2)$；在下限 $t=x/y$ 处它等于 0，边界项自动消失。因此
$$f_x(x,y)=xy(1-y^2)\varphi(xy)+\int_{x/y}^{xy}\varphi(t)\,\mathrm{d}t.$$
**③ 再对 $y$ 求导。** 第一项用乘积与链式法则，积分项再次用变限公式，得到
$$f_{xy}(x,y)=x(1-3y^2)\varphi(xy)+x^2y(1-y^2)\varphi'(xy)+x\varphi(xy)+\frac{x}{y^2}\varphi\!\left(\frac{x}{y}\right).$$
最后一项是正号，因为下限导数 $\partial(x/y)/\partial y=-x/y^2$ 又与公式中的负号相乘。
**④ 代入 $y=1$。** 此时第二项因 $1-y^2=0$ 消失，其余三项为 $-2x\varphi(x)+x\varphi(x)+x\varphi(x)=0$，故 $f''_{xy}(2,1)=0$。
【思路】先对 $x$ 求偏导（下限边界项自动为零），再对 $y$ 求偏导，最后代 $y=1$ 让各项相消。
【易错】不能先看到 $f(x,1)=0$ 就直接断言 $f_{xy}(x,1)=0$：沿一条线恒为 0 并不控制法向变化，应先按要求求偏导再代入，也避免未经检查就交换混合偏导顺序。

===Q15===
【答案】$\dfrac{\mathrm{e}-1}{2}$
【解】
**① 确定区域。** $I=\int_0^1\mathrm{d}x\int_0^{1-x}\mathrm{e}^{(x+y)^2}\,\mathrm{d}y$，积分域为 $x\ge0,\ y\ge0,\ x+y\le1$，是第一象限的直角三角形。
**② 换元使被积函数只含一个变量。** 令 $u=x+y,\ v=x$，则 $x=v,\ y=u-v$，区域变为 $0\le u\le1,\ 0\le v\le u$。雅可比为
$$\left|\frac{\partial(x,y)}{\partial(u,v)}\right|=\begin{vmatrix}0&1\\1&-1\end{vmatrix}=|-1|=1,$$
因此 $I=\int_0^1\mathrm{d}u\int_0^u \mathrm{e}^{u^2}\,\mathrm{d}v$。
**③ 先积掉 $v$。** 对固定 $u$，$\mathrm{e}^{u^2}$ 为常数，内层积分为 $u\mathrm{e}^{u^2}$。再令 $w=u^2$、$\mathrm{d}w=2u\,\mathrm{d}u$，
$$I=\int_0^1 u\mathrm{e}^{u^2}\,\mathrm{d}u=\frac12\int_0^1 \mathrm{e}^w\,\mathrm{d}w=\frac{\mathrm{e}-1}{2}.$$
【思路】用 $u=x+y$ 换元把被积函数化为单变量，等值线长度随 $u$ 变化恰好产生因子 $u$，再凑微分求值。
【易错】直接对 $y$ 积 $\mathrm{e}^{(x+y)^2}$ 没有常见初等原函数，但这不意味着二重积分难算；变量 $x+y$ 的等值线在三角域内长度随 $u$ 变化，积掉另一个变量后恰好产生因子 $u$。

===Q16===
【答案】$a\ne1$
【解】
**① 理解平方和的零点。** $f=(2x_2+3x_3)^2+(x_1+3x_2+ax_3)^2+(x_1+ax_2-2x_3)^2$ 每项都是平方，故 $f\ge0$ 自动成立。正定还要求：只要 $X\ne0$ 就有 $f(X)>0$，等价地三个括号同时为 0 时只允许 $X=0$。
**② 写出线性变换矩阵。**
$$M=\begin{pmatrix}0&2&3\\1&3&a\\1&a&-2\end{pmatrix},\qquad f(X)=\|MX\|^2,$$
只有零解等价于 $M$ 可逆，即 $|M|\ne0$。
**③ 展开行列式。** 按第一行展开，
$$|M|=-2\begin{vmatrix}1&a\\1&-2\end{vmatrix}+3\begin{vmatrix}1&3\\1&a\end{vmatrix}=-2(-2-a)+3(a-3)=5a-5=5(a-1).$$
所以 $a\ne1$；当 $a=1$ 时 $M$ 奇异，有非零 $X$ 使 $MX=0$，从而 $f(X)=0$，不正定。
【思路】把平方和写成 $\|MX\|^2$，正定等价于齐次方程 $MX=0$ 只有零解，即检验 $M$ 是否可逆。
【易错】平方和一定半正定，但未必正定。把各平方中的线性式按行放成矩阵 $M$，只需检验 $M$ 是否可逆；通常不必先展开成对称矩阵 $M^{\mathrm{T}}M$ 再算顺序主子式。

===Q17===
【答案】$2$
【解】
**① 从已知条件获得 $f$ 在 1 附近的形式。** 分母 $x-1\to0$ 且商趋于 2，由连续性得 $f(1)=0$；将自变量写成 $1+h$，得 $f(1+h)=2h+o(h)\ (h\to0)$。
**② 为分子作换元。** 所求极限为 $\lim\limits_{x\to0}\dfrac{\int_0^{x^2}\mathrm{e}^u f(\mathrm{e}^u-\mathrm{e}^{x^2}+1)\,\mathrm{d}u}{x^2\ln(\cos x)}$。令 $\delta=\mathrm{e}^{x^2}-1$，则 $\delta\ge0$ 且 $\delta\sim x^2$；再令 $v=\mathrm{e}^u-\mathrm{e}^{x^2}+1$、$\mathrm{d}v=\mathrm{e}^u\mathrm{d}u$。当 $u=0$ 时 $v=2-\mathrm{e}^{x^2}=1-\delta$；当 $u=x^2$ 时 $v=1$。因此分子等于
$$\int_{1-\delta}^{1}f(v)\,\mathrm{d}v=\int_{-\delta}^{0}f(1+h)\,\mathrm{d}h.$$
**③ 算出分子的主项。** 代 $f(1+h)=2h+o(h)$，
$$\int_{-\delta}^{0}[2h+o(h)]\,\mathrm{d}h=\left[h^2\right]_{-\delta}^{0}+o(\delta^2)=-\delta^2+o(\delta^2).$$
积分从负的 $h$ 到 0，主项为负；由 $\delta\sim x^2$，分子 $=-x^4+o(x^4)$。
**④ 求分母主项。** 由 $\cos x=1-\dfrac{x^2}{2}+o(x^2)$ 及 $\ln(1+z)=z+o(z)$，$\ln(\cos x)=-\dfrac12 x^2+o(x^2)$，$x^2\ln(\cos x)=-\dfrac12 x^4+o(x^4)$。故所求极限为 $(-1)/(-1/2)=2$。
【思路】用换元 $v=\mathrm{e}^u-\mathrm{e}^{x^2}+1$ 去掉分子里的指数权重，分别求分子分母关于 $x^4$ 的主项再相除。
【易错】换元不仅要改被积函数和微分，还要立即改上下限，本题 $\mathrm{e}^u\mathrm{d}u$ 正好是内层 $\mathrm{e}^u-\mathrm{e}^{x^2}+1$ 的微分。检查分子分母的正负，可防止把答案错写成 $-2$。

===Q18===
【答案】（I）$-\dfrac{2}{\mathrm{e}}$，在 $x=\mathrm{e}^{-2}$ 处取得；（II）$F'$ 在 0 处连续，$F'(0)=0$
【解】
**（I）求 $f$ 在 $(0,\infty)$ 的最小值。**
**① 求解微分方程。** $2xf'-f=2\sqrt x,\ f(1)=0$ 两边除以 $2x$ 得 $f'-\dfrac{1}{2x}f=x^{-1/2}$。积分因子为 $\exp\!\left(\int-\dfrac{1}{2x}\mathrm{d}x\right)=x^{-1/2}$，乘上后得 $\left[f(x)/\sqrt x\right]'=1/x$，积分得 $f(x)/\sqrt x=\ln x+C$。由 $f(1)=0$ 得 $C=0$，所以 $f(x)=\sqrt x\ln x$。
**② 求导并列出符号。** $f'(x)=\dfrac{\ln x}{2\sqrt x}+\dfrac{1}{\sqrt x}=\dfrac{\ln x+2}{2\sqrt x}$。分母为正，导数在 $x=\mathrm{e}^{-2}$ 处为 0，左侧负、右侧正，故该点是全区间的最小值点，$f(\mathrm{e}^{-2})=\mathrm{e}^{-1}\cdot(-2)=-\dfrac{2}{\mathrm{e}}$。
**（II）讨论 $F(x)=\int_{-1}^x f(|t|)\,\mathrm{d}t$ 的 $F'$ 在 0 处是否连续。**
**① 先处理 $f(|t|)$ 在 $t=0$ 的含义。** 当 $x\to0^+$，令 $s=1/\sqrt x\to\infty$，则 $\sqrt x\ln x=-\dfrac{2\ln s}{s}\to0$。因此定义
$$g(t)=\begin{cases}\sqrt{|t|}\ln|t|,&t\ne0,\\[3pt]0,&t=0,\end{cases}$$
使 $g$ 在 0 连续；改单点取值不改变积分，原 $F$ 可写成 $\int_{-1}^x g(t)\,\mathrm{d}t$。
**② 直接验证 $F'(0)$。** $\dfrac{F(h)-F(0)}{h}=\dfrac1h\int_0^h g(t)\,\mathrm{d}t$，由于 $g(t)\to0$，其绝对值不超过 $\sup_{|t|\le|h|}|g(t)|\to0$，故 $F'(0)=0$。在 $x\ne0$ 附近，微积分基本定理给 $F'(x)=g(x)$，从而 $\lim\limits_{x\to0}F'(x)=\lim\limits_{x\to0}g(x)=0=F'(0)$，即 $F'$ 在 0 处连续。
【思路】（I）解一阶线性方程求 $f$ 并看导数符号定最小值；（II）先求极限、作连续延拓，再用积分基本定理验证 $F'(0)=\lim F'(x)=0$。
【易错】题面中的 $\ln|t|$ 在 0 未定义，不能无说明地直接代 0，正确步骤是先求极限作连续延拓再用积分基本定理。这里 $f'$ 在 $0^+$ 可能无界，不影响 $F'$ 连续，因为 $F'$ 等于 $f(|x|)$，不是 $f'(|x|)$。

===Q19===
【答案】最大值为 $1$，在 $(0,1)$ 和 $(0,-1)$ 处取得
【解】
**① 把各因子记成新变量。** 对 $f(x,y)=\mathrm{e}^x y^2\left(3-\mathrm{e}^x-y^2\right)$、$D=\{\mathrm{e}^x+y^2\le3\}$，令 $u=\mathrm{e}^x>0$、$v=y^2\ge0$、$w=3-\mathrm{e}^x-y^2\ge0$。区域条件保证 $w$ 非负，且 $u+v+w=3$，原函数恰为 $uvw$。
**② 用算术—几何平均不等式。** 对三个非负数，
$$\sqrt[3]{uvw}\le\frac{u+v+w}{3}=1,$$
所以 $uvw\le1$；等号要求 $u=v=w$，又和为 3，故必须 $u=v=w=1$。
**③ 将等号条件还原为原变量。** $\mathrm{e}^x=1$ 给 $x=0$；$y^2=1$ 给 $y=\pm1$；此时 $w=3-1-1=1$，两点均在区域内，原函数值都是 1，上界可达，最大值为 1。
【思路】把函数化为三个非负数之积 $uvw$ 且 $u+v+w=3$ 为定值，用均值不等式求上界并验证等号可达。
【易错】用均值不等式前必须检查每个因子非负，本题区域的作用正是保证第三个因子非负。求二元最值不一定要解偏导方程；「非负乘积＋固定和」的结构应优先识别。

===Q20===
【答案】$\dfrac{\mathrm{e}+\mathrm{e}^{-1}-2}{8}$
【解】
**① 严格说明第一项为什么为 0。** 被积函数为 $\sqrt[3]{x-y}+xy\mathrm{e}^{x^2-y^2}$，$D=\{x,y\ge0:x^2+y^2\le1\}$。记 $J=\iint_D\sqrt[3]{x-y}\,\mathrm{d}x\mathrm{d}y$，区域在交换 $x,y$ 后不变、面积元也不变，所以
$$J=\iint_D\sqrt[3]{y-x}\,\mathrm{d}x\mathrm{d}y=-\iint_D\sqrt[3]{x-y}\,\mathrm{d}x\mathrm{d}y=-J,$$
因此 $J=0$，这里用的是实立方根的奇性。
**② 把剩下的积分换成平方变量。** 令 $u=x^2,\ v=y^2$，因 $x,y\ge0$ 可取 $x=\sqrt u,\ y=\sqrt v$，区域变成 $u\ge0,\ v\ge0,\ u+v\le1$，且 $\mathrm{d}u=2x\mathrm{d}x$、$\mathrm{d}v=2y\mathrm{d}y$、$xy\,\mathrm{d}x\mathrm{d}y=\dfrac14\mathrm{d}u\mathrm{d}v$。于是
$$I=\frac14\int_0^1\mathrm{d}u\int_0^{1-u}\mathrm{e}^{u-v}\,\mathrm{d}v.$$
**③ 先积 $v$ 再积 $u$ 并整理。** 把 $\mathrm{e}^u$ 当常数，$\int_0^{1-u}\mathrm{e}^{u-v}\,\mathrm{d}v=\mathrm{e}^u\left[-\mathrm{e}^{-v}\right]_0^{1-u}=\mathrm{e}^u-\mathrm{e}^{2u-1}$，故
$$I=\frac14\left[\int_0^1\mathrm{e}^u\,\mathrm{d}u-\mathrm{e}^{-1}\int_0^1\mathrm{e}^{2u}\,\mathrm{d}u\right]=\frac14\left[(\mathrm{e}-1)-\frac{\mathrm{e}^{-1}}{2}(\mathrm{e}^2-1)\right]=\frac{\mathrm{e}+\mathrm{e}^{-1}-2}{8}.$$
【思路】先用交换 $x,y$ 的对称性与立方根奇性消去第一项，再用 $u=x^2,v=y^2$ 化简余下积分，两次单积分求值。
【易错】用交换 $x,y$ 的对称性，必须同时检查区域不变和函数变号。平方换元时在坐标轴上雅可比写成倒数会退化，但可先在内部换元再取边界极限；本题 $xy\,\mathrm{d}x\mathrm{d}y$ 组合直接变为 $\dfrac14\mathrm{d}u\mathrm{d}v$ 最清楚。另：原册印刷的 $3\sqrt{x-y}$ 应读作实立方根 $\sqrt[3]{x-y}$（小易注「实立方根的奇性」可佐证），不要当成 $3$ 倍平方根。

===Q21===
【答案】（I）$f''(x)\ge0$；（II）对任意正整数 $n$，$\int_0^1 f(x^n)\,\mathrm{d}x\ge f\!\left(\frac{1}{n+1}\right)$，两问均成立
【解】
**（I）证明 $f''\ge0$。**
**① 用二阶展开计算差分极限。** 与第一套第 21 题一样，
$$f(x\pm h)=f(x)\pm f'(x)h+\frac12 f''(x)h^2+o(h^2).$$
两式相加并减 $2f(x)$，得到 $f''(x)h^2+o(h^2)\ge0$。除以 $h^2>0$、令 $h\to0$，得 $f''(x)\ge0$。
**（II）证明积分不等式。**
**① 证明切线是下界。** 设 $a$ 为固定点，因 $f''\ge0$ 知 $f'$ 不减。当 $z>a$ 时 $f(z)-f(a)=\int_a^z f'(t)\,\mathrm{d}t\ge f'(a)(z-a)$；当 $z<a$ 时 $f'(t)\le f'(a)$ 在 $[z,a]$ 上成立，积分后同样得到 $f(z)-f(a)\ge f'(a)(z-a)$。因此对所有 $z$，
$$f(z)\ge f(a)+f'(a)(z-a).$$
**② 选使一次项积分消失的 $a$。** 由于 $\int_0^1 x^n\,\mathrm{d}x=\dfrac{1}{n+1}$，令 $a=\dfrac{1}{n+1}$，把上式中的 $z$ 换为 $x^n$ 并积分：
$$\int_0^1 f(x^n)\,\mathrm{d}x\ge\int_0^1\left[f(a)+f'(a)(x^n-a)\right]\mathrm{d}x=f(a)+f'(a)\left(\frac{1}{n+1}-a\right)=f(a).$$
代回 $a$ 即证。
【思路】（I）用二阶泰勒展开把差分条件转为 $f''\ge0$；（II）由 $f''\ge0$ 得切线下界，取切点为 $x^n$ 在 $[0,1]$ 上的平均值使一次项积分恰为 0。
【易错】第一套第 21 题用「弦线在上」证明上界，本题用「切线在下」证明下界。切点不是随便选，而取 $x^n$ 在 $[0,1]$ 上的平均值，使多余的一次项积分恰好为 0。

===Q22===
【答案】（I）$a=2,\ b=-2,\ \lambda=4$；（II）可化为 $3y_1^2-3y_2^2-3y_3^2$
【解】
**（I）求 $a,b,\lambda$。**
**① 把伴随矩阵特征关系转为 $A$ 的特征关系。** $r(A)=3$ 说明 $A$ 可逆，$A^*=|A|A^{-1}$ 也可逆，故其特征值 $\lambda\ne0$。在 $A^*\alpha=\lambda\alpha$ 左乘 $A$，$|A|\alpha=\lambda A\alpha$，所以 $A\alpha=\mu\alpha$，其中 $\mu=|A|/\lambda$。
**② 逐行写出方程。** 对 $A=\begin{pmatrix}2&1&1\\1&2&1\\1&1&a\end{pmatrix}$、$\alpha=(1,b,1)^{\mathrm{T}}$，
$$A\alpha=\begin{pmatrix}3+b\\2+2b\\1+b+a\end{pmatrix}=\begin{pmatrix}\mu\\\mu b\\\mu\end{pmatrix}.$$
前两行给 $\mu=3+b$ 与 $2+2b=b(3+b)$，移项因式分解得 $b^2+b-2=(b-1)(b+2)=0$。因 $b\ne1$，得 $b=-2$、$\mu=1$；第三行给 $1-2+a=1$，所以 $a=2$。
**③ 计算行列式求 $\lambda$。** 此时
$$|A|=\begin{vmatrix}2&1&1\\1&2&1\\1&1&2\end{vmatrix}=2(4-1)-(2-1)+(1-2)=4.$$
由 $\mu=|A|/\lambda=1$，得 $\lambda=4$。
**（II）将 $X^{\mathrm{T}}(A-A^*)X$ 正交化为标准形。**
**① 写出 $A-A^*$ 的简单结构。** 设 $J$ 为 3 阶全 1 矩阵，则 $A=E+J$ 且 $J^2=3J$。验证
$$(E+J)\left(E-\frac J4\right)=E+\frac34 J-\frac14 J^2=E,$$
故 $A^{-1}=E-\dfrac J4$、$A^*=4E-J$，于是 $A-A^*=-3E+2J$。
**② 找正交单位特征向量。** 对 $v_1=(1,1,1)^{\mathrm{T}}$，$Jv_1=3v_1$，故 $(-3E+2J)v_1=3v_1$；对任意分量和为 0 的向量 $v$ 有 $Jv=0$，对应特征值为 $-3$。可选
$$q_1=\frac1{\sqrt3}(1,1,1)^{\mathrm{T}},\quad q_2=\frac1{\sqrt2}(1,-1,0)^{\mathrm{T}},\quad q_3=\frac1{\sqrt6}(1,1,-2)^{\mathrm{T}},$$
三向量两两点积为 0、长度为 1。
**③ 写变换与标准形。** 令 $Q=(q_1,q_2,q_3)$，则 $Q^{\mathrm{T}}Q=E$，$Q^{\mathrm{T}}(A-A^*)Q=\operatorname{diag}(3,-3,-3)$。在正交变换 $X=QY$ 下，
$$X^{\mathrm{T}}(A-A^*)X=Y^{\mathrm{T}}\operatorname{diag}(3,-3,-3)Y=3y_1^2-3y_2^2-3y_3^2.$$
【思路】（I）借 $A^*=|A|A^{-1}$ 把伴随矩阵特征向量转成 $A$ 的特征向量，逐行比对定 $a,b$ 再算 $|A|$ 定 $\lambda$；（II）用 $A=E+J,\ J^2=3J$ 化简 $A-A^*$，取正交单位特征向量作 $Q$ 化标准形。
【易错】可逆矩阵 $A$ 与 $A^*$ 拥有同一组特征向量，对应特征值乘积为 $|A|$。正交变换化二次型使用的是 $Q^{\mathrm{T}}MQ$；因为 $Q$ 正交才有 $Q^{-1}=Q^{\mathrm{T}}$，不能对任意可逆矩阵混用这两个符号。
