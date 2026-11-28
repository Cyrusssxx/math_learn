===Q1===
【答案】D
【解】
**① 把四个选项分别化为 $x^n$ 的同阶无穷小。** (A) 用余弦展开 $1-\cos x\cdot\cos 2x=1-\left(1-\dfrac{x^2}{2}+o(x^2)\right)\left(1-2x^2+o(x^2)\right)=\dfrac{5}{2}x^2+o(x^2)$，与 $x^2$ 同阶。
$$1-\cos\sqrt t\sim\frac t2,\qquad \int_0^x(1-\cos\sqrt t)\,dt\sim\frac{x^2}{4},$$
故 (B) 与 $x^2$ 同阶。
$$1-\sqrt{\cos t}\sim\frac{t^2}{4},\qquad \int_0^{\sin x}(1-\sqrt{\cos t})\,dt\sim\frac{x^3}{12},$$
故 (C) 与 $x^3$ 同阶。
**② 计算 (D) 的阶。** 内层积分与 $t$ 无关，可直接提出：
$$\int_0^x dt\int_0^x\ln(1+u^2)\,du=x\int_0^x\ln(1+u^2)\,du\sim x\cdot\frac{x^3}{3}=\frac{x^4}{3},$$
与 $x^4$ 同阶，幂次最高，故选 D。
【思路】把每个无穷小量用等价无穷小或泰勒展开写成 $x^n$ 的同阶量，比较幂次 $n$ 的大小。
【易错】阶数最高指趋于零最快，即幂次最大；累次积分中内层上限是 $x$，被积函数与 $t$ 无关时才可直接提出因子 $x$。

===Q2===
【答案】B
【解】
**① 对 $x$ 求偏导。** 方程 $xz-e^{y+z}=1$ 两边对 $x$ 求偏导：$z+x\dfrac{\partial z}{\partial x}-e^{y+z}\dfrac{\partial z}{\partial x}=0$，故
$$\frac{\partial z}{\partial x}=\frac{z}{e^{y+z}-x}.$$
**② 对 $y$ 求偏导。** 两边对 $y$ 求偏导：$x\dfrac{\partial z}{\partial y}-e^{y+z}\left(1+\dfrac{\partial z}{\partial y}\right)=0$，故
$$\frac{\partial z}{\partial y}=-\frac{e^{y+z}}{e^{y+z}-x}.$$
**③ 代入组合式验证。** 
$$x\frac{\partial z}{\partial x}+z\frac{\partial z}{\partial y}=\frac{xz-ze^{y+z}}{e^{y+z}-x}=\frac{z\left(x-e^{y+z}\right)}{e^{y+z}-x}=-z.$$
恒成立的是 (B)。
【思路】隐函数方程分别求偏导后代入四个选项，验证组合式是否恒等于右端。
【易错】对 $y$ 求偏导时链式法则产生因子 $1+\dfrac{\partial z}{\partial y}$；分母是 $e^{y+z}-x$，符号颠倒会误选 D。

===Q3===
【答案】B
【解】
**① 铅直渐近线。** $x\to0$ 时 $e^x-1\sim x\to0$，分子 $\sqrt{x^2+1}+\sin x\to1$，故 $y\to+\infty$，$x=0$ 是铅直渐近线。
**② 水平渐近线。** $x\to+\infty$ 时分母 $e^x-1$ 指数增长，故 $y\to0$，$y=0$ 是水平渐近线。
**③ 斜渐近线。** $x\to-\infty$ 时 $e^x\to0$，
$$k=\lim_{x\to-\infty}\frac{\sqrt{x^2+1}+\sin x}{x(e^x-1)}=\lim_{x\to-\infty}\frac{-x+\sin x}{-x}=1.$$
但截距
$$b=\lim_{x\to-\infty}\left[\sqrt{x^2+1}+\sin x-x\right]=-\lim_{x\to-\infty}\frac{1}{\sqrt{x^2+1}+x}-\lim_{x\to-\infty}\sin x,$$
其中 $\sin x$ 振荡无极限，故 $b$ 不存在，$x\to-\infty$ 时无斜渐近线。共 2 条，选 B。
【思路】分别考察 $x\to0$、$x\to+\infty$、$x\to-\infty$ 三个方向，检验渐近线定义中的极限是否存在。
【易错】$x\to-\infty$ 时 $\sqrt{x^2+1}\sim -x$（不是 $x$）；斜率 $k$ 存在不代表截距 $b$ 存在，必须两者都存在才有斜渐近线。

===Q4===
【答案】C
【解】
**① 转化为拐点问题。** $f'(x)$ 的极值点就是 $f''(x)$ 变号的点，也就是 $y=f(x)$ 的拐点，故只需数拐点个数。
**② 确定 $f'$ 的零点分布。** $f(x)=(x-1)^2(x-2)^3$ 的零点为 $1$（二重）和 $2$（三重），由罗尔定理存在 $\xi\in(1,2)$ 使 $f'(\xi)=0$。又 $f'$ 是四次多项式，故可写成
$$f'(x)=(x-1)(x-2)^2g(x),$$
其零点（计重数）为 $x=1$（一重）、$x=2$（二重）与 $\xi$（单根），共四重根。
**③ 数出三个极值点。** 结合解析中 $f'(x)$ 的图像：$x=1$ 与 $x=\xi$ 是单零点，$f'$ 在这两点变号；$x=2$ 是二重零点，$f'$ 不变号且在此处取极小值；此外在 $(1,\xi)$ 与 $(\xi,2)$ 内各有一个驻点 $\eta_1,\eta_2$（分别为极小、极大）。故 $f'$ 共有 3 个极值点 $\eta_1,\eta_2,2$，即 $f$ 有 3 个拐点。选 C。
【思路】利用零点重数与罗尔定理确定 $f'$ 的全部零点，再由 $f'$ 图像数出极值点即拐点个数。
【易错】$f$ 在 $x=1$ 处是二重零点，故 $f'$ 在 $x=1$ 处只有一重零点；次数已是四次，不能再凭空增加零点。

===Q5===
【答案】D
【解】
**① 写出通解的结构类型。** 方程 $y''+py'+qy=(ax+b)e^x$ 的齐次解由特征根决定：相异实根给 $C_1e^{r_1x}+C_2e^{r_2x}$，重根给 $(C_1+C_2x)e^{r_1x}$，共轭复根给 $e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$。非齐次特解形如 $x^k(Ax+B)e^x$，其中 $k$ 是 $1$ 作为特征根的重数（共轭复根时 $k=0$）。
**② 逐项对照。** (A) $(1+x)e^x$ 可对应 $k=0$ 或 $k=1$；(C) $(x+x^2)e^x$ 对应 $1$ 是一重根；(B) $(1+\sin x)e^x$ 对应共轭复根情形，取 $\alpha=0,\ \beta=1,\ C_1=0,\ C_2=1,\ A=0,\ B=1$ 即可。
**③ 排除 (D)。** (D) 同时含 $x^2e^x$ 与 $\sin x\,e^x$：要出现 $x^2$ 因子需 $1$ 是二重实根，此时齐次解不含 $\sin x$；要出现 $\sin x$ 需共轭复根，此时 $1$ 不是特征根、$k=0$，不能产生 $x^2$ 因子。两者矛盾，故 (D) 必不是解。
【思路】按特征根与指数 $1$ 的关系分类讨论解的结构，逐项排除不可能的组合。
【易错】特解中乘 $x^k$ 的 $k$ 恰为 $1$ 作为特征根的重数；共轭复根情形下 $1$ 不可能是特征根。

===Q6===
【答案】A
【解】
**① 化为单变量比较。** 由 $x\ge0,\ y\ge0,\ x+y\le1$ 及 $(x+y)^2\ge x^2+y^2$ 得 $0<x^2+y^2\le1$。令 $t=x^2+y^2$，比较 $I_1,I_2,I_3$ 等价于比较 $t\ln t,\ t-1,\ \cos(t-1)$ 在 $(0,1]$ 上的大小。
**② 确定最大项。** 当 $0<t<1$ 时 $t\ln t<0,\ t-1<0$，而 $t-1\in(-1,0)$，故 $\cos(t-1)>0$，$I_3$ 最大。
**③ 比较 $t\ln t$ 与 $t-1$。** 令 $h(t)=t\ln t-(t-1)$，则 $h'(t)=\ln t<0$，$h$ 在 $(0,1)$ 上递减，且 $h(1)=0$，故 $0<t<1$ 时 $h(t)>h(1)=0$，即 $t\ln t>t-1$，从而 $I_1>I_2$。综上 $I_2<I_1<I_3$，选 A。
【思路】令 $t=x^2+y^2$ 把二重积分比较化为三个一元函数在 $(0,1]$ 上的比较，用单调性与符号判断。
【易错】$I_1$ 的被积函数是 $t\ln t$ 而非 $\ln t$；比较 $t\ln t$ 与 $t-1$ 要构造 $h(t)$ 并用 $h(1)=0$。

===Q7===
【答案】C
【解】
**① 充分性。** 由 $f(0)=f'(0)=0$ 及二阶泰勒公式，$f(t)=\dfrac{f''(\xi)}{2}t^2$，$\xi\in(0,t)$。因 $f''$ 在 $[0,1]$ 上连续，记 $|f''|\le M$，则当 $x\ge1$ 时 $\left|f\!\left(\dfrac1x\right)\right|\le \dfrac{M}{2x^2}$，与 $\dfrac1{x^2}$ 同阶或更高阶，由比较审敛法知 $\int_1^{+\infty}f\!\left(\dfrac1x\right)dx$ 收敛。
**② 必要性。** 积分收敛必有 $\lim\limits_{x\to+\infty}f\!\left(\dfrac1x\right)=0$，即 $f(0)=0$。若 $f'(0)=A\ne0$，则 $\lim\limits_{t\to0^+}\dfrac{f(t)}{t}=A$，从而 $f\!\left(\dfrac1x\right)\sim \dfrac{A}{x}$，而 $\int_1^{+\infty}\dfrac{dx}{x}$ 发散，矛盾，故 $f'(0)=0$。
**③ 结论。** 两方向都成立，是充要条件，选 C。
【思路】充分性用泰勒展开加比较审敛法；必要性用积分收敛的必要条件及 $f(t)\sim f'(0)t$ 与调和积分发散矛盾。
【易错】必要性中不能只由 $f(1/x)\to0$ 就断言 $f'(0)=0$，必须借助 $f(t)/t$ 的极限与 $\int dx/x$ 发散推出矛盾。

===Q8===
【答案】B
【解】
**① 先求 $|A|$。** 把 $A^*$ 写成 $2\times2$ 分块矩阵 $\begin{pmatrix}O&C\\D&O\end{pmatrix}$，其中 $C=\begin{pmatrix}1&-1\\3&1\end{pmatrix}$，$D=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，则
$$|A^*|=|C|\,|D|=4\times(-2)=-8,$$
而 $|A^*|=|A|^{4-1}=|A|^3=-8$，故 $|A|=-2$，$A$ 可逆。
**② 化简待求的秩。** 因 $A$ 可逆，
$$r(A^2-A)=r\big[A(A-E)\big]=r(A-E)=r\big[A^*(A-E)\big]=r(-2E-A^*)=r(2E+A^*).$$
**③ 行变换求秩。** 
$$2E+A^*=\begin{pmatrix}2&0&1&-1\\0&2&3&1\\1&1&2&0\\1&-1&0&2\end{pmatrix}\to\begin{pmatrix}1&-1&0&2\\0&2&3&1\\0&0&-1&-3\\0&0&0&-6\end{pmatrix},$$
有 3 个非零行，故 $r(A^2-A)=3$，选 B。
【思路】利用 $A^*=|A|A^{-1}$ 把秩转化为 $r(2E+A^*)$，再用初等行变换求秩。
【易错】$A$ 可逆时左乘 $A$ 不改变秩；$A^*(A-E)=|A|E-A^*=-2E-A^*$，这里 $|A|=-2$ 的符号不能弄错。

===Q9===
【答案】C
【解】
**① 证明 (C)。** 设 $\alpha$ 是 $B$ 的特征向量：$B\alpha=k\alpha$。由 $\lambda\alpha=AB\alpha\ne0$ 知 $k\ne0$。于是
$$\lambda\alpha=AB\alpha=A(k\alpha)=kA\alpha\quad\Longrightarrow\quad A\alpha=\frac{\lambda}{k}\alpha,$$
故 $\alpha$ 也是 $A$ 的特征向量。
**② 举反例排除其余。** 取 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$，$B=\begin{pmatrix}1&1\\1&1\end{pmatrix}$，$\alpha=(1,0)^T$，则 $AB\alpha=\alpha$，满足题设。此时 $B\alpha=(1,1)^T$ 不是 $\alpha$ 的倍数，(A) 错；$A\alpha=\alpha$，但 $BA\alpha=(1,1)^T$ 不是 $A\alpha$ 的倍数，(B) 错；$B\alpha=(1,1)^T$，而 $AB(B\alpha)=(2,0)^T$ 不是 $B\alpha$ 的倍数，(D) 错。
**③ 结论。** 只有 (C) 正确。
【思路】由 $AB\alpha=\lambda\alpha$ 出发，若 $\alpha$ 同时是 $B$ 的特征向量则 $k\ne0$，可解出 $A\alpha=\dfrac{\lambda}{k}\alpha$；其余选项用具体反例排除。
【易错】$\lambda\ne0$ 只能推出 $B\alpha\ne0$ 与 $A(B\alpha)=\lambda\alpha$，不能直接认定 $A\alpha$ 与 $B\alpha$ 之间的倍数关系。

===Q10===
【答案】A
【解】
**① 求 $A$ 的特征值。** $(\alpha,\beta,\gamma)$ 为正交矩阵，故三向量单位正交。于是
$$A\alpha=\alpha\alpha^T\alpha-2\beta\beta^T\alpha=\alpha,\quad A\beta=-2\beta,\quad A\gamma=0,$$
特征值为 $1,-2,0$。
**② 求 $(A+E)^*$ 的特征值。** $A+E$ 的特征值为 $2,-1,1$，行列式 $|A+E|=-2$。由 $M^*=|M|M^{-1}$ 得 $(A+E)^*$ 的特征值为 $-1,2,-2$，对应特征向量依次为 $\alpha,\beta,\gamma$。
**③ 写标准形求条件最大值。** $A+E$ 对称，故 $(A+E)^*$ 对称，正交变换下
$$f=x^T(A+E)^*x=-y_1^2+2y_2^2-2y_3^2=2(y_1^2+y_2^2+y_3^2)-3y_1^2-4y_3^2.$$
由 $x^Tx=y_1^2+y_2^2+y_3^2=5$ 得 $f=10-3y_1^2-4y_3^2\le10$，当 $y_1=y_3=0$ 时取到最大值 10，选 A。
【思路】用正交基直接求 $A$ 的特征值，再借 $M^*$ 的特征值为 $|M|/\lambda_i$ 得伴随矩阵标准形，最后在球面约束下求最大值。
【易错】伴随矩阵的特征值是 $|M|/\lambda_i$ 而非 $\lambda_i$；正交变换保持 $x^Tx$ 不变，约束才化为 $y_1^2+y_2^2+y_3^2=5$。

===Q11===
【答案】$3-\ln 2$
【解】
**① 由参数方程求 $f'(1)$。** 
$$\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{2+1/t}{1+4t}=\frac{3+\ln t}{1+4t}.$$
由 $x=1$ 得 $t+2t^2=1$，解得 $t=\dfrac12$（负根舍去）。故
$$f'(1)=\left.\frac{dy}{dx}\right|_{t=1/2}=\frac{3-\ln2}{3}=1-\frac13\ln2.$$
**② 凑导数定义。** 令 $u=\dfrac1x\to0^+$，则
$$x\left[f\!\left(1+\frac2x\right)-f\!\left(1-\frac1x\right)\right]=\frac{f(1+2u)-f(1-u)}{u}=\frac{f(1+2u)-f(1)}{u}+\frac{f(1)-f(1-u)}{u}\to 3f'(1)=3-\ln2.$$
【思路】参数方程求导得 $f'(1)$，再用导数定义把极限化为 $2f'(1)+f'(1)$。
【易错】$y=2t+t\ln t$ 的导数是 $3+\ln t$ 而非 $2+\ln t$；由 $x=1$ 解 $t$ 时要舍去负根。

===Q12===
【答案】$-4\pi$
【解】
**① 把 $f$ 写乘积形式并展开三阶导。** 令 $g(x)=\ln(2+\cos x)$，则 $f(x)=x^2g(x)$，由乘积求导
$$f^{(3)}(x)=x^2g^{(3)}(x)+6xg''(x)+6g'(x).$$
**② 用周期性化简。** $g$ 是以 $2\pi$ 为周期的偶函数，各阶导数也是 $2\pi$ 周期函数，且奇阶导数在零点为 0，故 $g'(2\pi)=g'(0)=0$，$g^{(3)}(2\pi)=g^{(3)}(0)=0$。于是 $f^{(3)}(2\pi)=12\pi g''(2\pi)=12\pi g''(0)$。
**③ 求 $g''(0)$。** $g'(x)=-\dfrac{\sin x}{2+\cos x}$，故
$$g''(x)=-\frac{2\cos x+1}{(2+\cos x)^2},\qquad g''(0)=-\frac{3}{9}=-\frac13.$$
因此 $f^{(3)}(2\pi)=12\pi\cdot\left(-\dfrac13\right)=-4\pi$。
【思路】三阶乘积求导后利用 $g$ 的周期性与奇偶性消去奇阶导数项，只需算 $g''(0)$。
【易错】三阶乘积求导的系数是 $1,6,6$，不能漏掉 $6xg''$ 项；$g''$ 的分子是 $2\cos x+1$。

===Q13===
【答案】$\ln(1+e)-\ln 2$
【解】
**① 由积分与 $a$ 无关求 $f$。** 对 $\int_a^{ab}f(x)dx$ 关于 $a$ 求导并令其为零：
$$\frac{d}{da}\int_a^{ab}f(x)dx=bf(ab)-f(a)=0.$$
令 $a=1$ 得 $bf(b)=f(1)=1$，故 $f(x)=\dfrac1x$。
**② 计算积分。** 
$$\int_0^1 f(e^{-x}+1)\,dx=\int_0^1\frac{dx}{e^{-x}+1}=\int_0^1\frac{e^x}{1+e^x}\,dx=\Big[\ln(1+e^x)\Big]_0^1=\ln(1+e)-\ln2.$$
【思路】变上限积分对参数求导得到函数方程，定出 $f(x)=1/x$ 后凑微分 $\dfrac{e^x}{1+e^x}dx=d\ln(1+e^x)$ 积分。
【易错】上限是 $ab$，求导得 $bf(ab)$，不要漏乘 $b$；"$f(e^{-x}+1)$"是把 $e^{-x}+1$ 作为自变量代入 $f$。

===Q14===
【答案】$\dfrac{a}{5}$
【解】
**① 求面积关于横坐标的函数。** 设 $P(X,Y)$，$Y=\dfrac{X^2}{4}$。直线 $AP$ 的斜率为 $\dfrac{Y-1}{X}=\dfrac X4-\dfrac1X$，方程 $y=\left(\dfrac X4-\dfrac1X\right)x+1$。面积
$$S(X)=\int_0^X\left[\left(\frac X4-\frac1X\right)x+1-\frac{x^2}{4}\right]dx=\frac{X^3}{24}+\frac X2.$$
**② 由变化率反解横坐标速度。** 
$$\frac{dS}{dt}=\frac{dS}{dX}\cdot\frac{dX}{dt}=\left(\frac{X^2}{8}+\frac12\right)\frac{dX}{dt}=a\quad\Longrightarrow\quad \frac{dX}{dt}=\frac{8a}{X^2+4}.$$
**③ 代入 $X=6$。** $\left.\dfrac{dX}{dt}\right|_{X=6}=\dfrac{8a}{40}=\dfrac a5$。
【思路】写出直线 $AP$ 方程并积分得面积 $S(X)$，再用链式法则由已知面积变化率反解横坐标变化率。
【易错】抛物线 $x=2\sqrt y$ 即 $y=x^2/4$；面积是直线减抛物线在 $[0,X]$ 上的积分，不要漏掉线段 $OA$ 对应的部分。

===Q15===
【答案】$3dx+2dy$
【解】
**① 换元求 $f$ 的显式表达。** 令 $u=\dfrac yx,\ v=2x-y$，则 $x=\dfrac{v}{2-u},\ y=\dfrac{uv}{2-u}$。代入 $f\!\left(\dfrac yx,2x-y\right)=x+y$：
$$f(u,v)=\frac{v}{2-u}+\frac{uv}{2-u}=\frac{v(1+u)}{2-u}\quad\Longrightarrow\quad f(x,y)=\frac{y(1+x)}{2-x}.$$
**② 求偏导并代入。** $f'_x(x,y)=\dfrac{3y}{(2-x)^2}$，$f'_y(x,y)=\dfrac{x+1}{2-x}$，故 $f'_x(1,1)=3,\ f'_y(1,1)=2$。
**③ 写出全微分。** $df(x,y)\big|_{(1,1)}=3dx+2dy$。
【思路】作变量代换 $u=y/x,\ v=2x-y$ 反解出 $x,y$ 得到 $f$ 的表达式，再求偏导代入 $(1,1)$。
【易错】换元后须把 $(u,v)$ 重新记为 $(x,y)$ 才是 $f$ 的表达式；也可直接对原式两边微分，解关于 $f'_1,f'_2$ 的线性方程组。

===Q16===
【答案】$-\dfrac{5}{4}$
【解】
**① 化为方程组有无穷多解。** 条件即方程组
$$\begin{pmatrix}1&1&-2\\-1&2&-1\\a&2&b\end{pmatrix}\begin{pmatrix}c_1\\c_2\\c_3\end{pmatrix}=\begin{pmatrix}3\\2\\0\end{pmatrix}$$
有无穷多解，故系数矩阵与增广矩阵的秩都小于 3。
**② 系数矩阵奇异。** 行变换
$$\begin{pmatrix}1&1&-2&3\\-1&2&-1&2\\a&2&b&0\end{pmatrix}\to\begin{pmatrix}1&1&-2&3\\0&3&-3&5\\0&2-a&b+2a&-3a\end{pmatrix}.$$
系数矩阵奇异要求 $3(b+2a)+3(2-a)=3(a+b+2)=0$，即 $a+b=-2$。
**③ 增广矩阵也降秩。** 增广矩阵任意三阶子式为 0，取其中一个得 $-2+4b=0$，故 $b=\dfrac12$，进而 $a=-\dfrac52$，所以 $ab=-\dfrac54$。
【思路】"表示不唯一"等价于方程组有无穷多解，即系数矩阵与增广矩阵秩都小于 3，分别列条件求 $a,b$。
【易错】系数矩阵奇异只是必要条件，还须保证相容性（增广矩阵秩也降低），不能只算一个行列式就结束。

===Q17===
【答案】$e^{2/\pi}$
【解】
**（1）证明存在唯一实根。**
**① 用导数划分单调区间。** 
$$f'_n(x)=1-\frac{n+1}{1+x^2}=\frac{x^2-n}{1+x^2}.$$
当 $0<x<\sqrt n$ 时 $f'_n(x)<0$，$f_n$ 递减且 $f_n(x)<f_n(0)=0$，无实根，且 $f_n(\sqrt n)<0$。当 $x>\sqrt n$ 时 $f'_n(x)>0$，$f_n$ 递增且 $\lim\limits_{x\to+\infty}f_n(x)=+\infty$，由保号性存在 $X>\sqrt n$ 使 $f_n(X)>0$。
**② 零点定理与唯一性。** $f_n(\sqrt n)\cdot f_n(X)<0$，由零点定理存在 $x_n\in(\sqrt n,X)$ 使 $f_n(x_n)=0$；又在 $(\sqrt n,+\infty)$ 上严格递增，故根唯一。
**（2）计算极限。**
**① 用根的条件化简底数。** 由 $x_n=(n+1)\arctan x_n$ 得
$$\frac{2x_n}{\pi(n+1)}=\frac{2\arctan x_n}{\pi},$$
故所求为 $\lim\limits_{n\to\infty}\left[\dfrac{2\arctan x_n}{\pi}\right]^{-x_n}$。
**② 取对数后用洛必达。** 
$$-x_n\ln\frac{2\arctan x_n}{\pi}=-x_n\ln\left(1+\frac{2\arctan x_n-\pi}{\pi}\right)\sim -\frac{x_n}{\pi}\left(2\arctan x_n-\pi\right).$$
由洛必达法则
$$\lim_{x\to+\infty}\frac{2\arctan x-\pi}{1/x}=\lim_{x\to+\infty}\frac{2/(1+x^2)}{-1/x^2}=-2,$$
且 $x_n\to+\infty$，故指数极限为 $-\dfrac1\pi\cdot(-2)=\dfrac2\pi$，原极限为 $e^{2/\pi}$。
【思路】（1）用导数符号分区间讨论单调性，结合零点定理证存在唯一；（2）由根的条件把底数化为 $2\arctan x_n/\pi$，取对数后用洛必达处理 $1^\infty$ 型。
【易错】单调区间的分界是 $\sqrt n$ 而非 $n$；$1^\infty$ 型极限须取对数，不能直接用底数极限代替。

===Q18===
【答案】（I）$y=2x-x^2\ (0<x<2)$；（II）$P\left(\dfrac43,\dfrac89\right)$，最小面积 $\dfrac{64}{27}$
【解】
**（I）求曲线方程。**
**① 由中点条件建立微分方程。** 设 $P(x,y)$，切线为 $Y-y=y'(X-x)$，令 $X=0$ 得 $A(0,y-xy')$。线段 $AP$ 的中点为 $M\left(\dfrac x2,\dfrac{2y-xy'}{2}\right)$，它在直线 $y=2x$ 上，故
$$\frac{2y-xy'}{2}=2\cdot\frac x2=x\quad\Longrightarrow\quad xy'-2y=-2x.$$
**② 解一阶线性方程。** 两边除以 $x^3$ 得 $\left(\dfrac{y}{x^2}\right)'=-\dfrac{2}{x^2}$，积分得 $y=2x+Cx^2$。由 $y(1)=1$ 得 $C=-1$，又曲线在第一象限，故 $0<x<2$，即 $L:y=2x-x^2\ (0<x<2)$。
**（II）求最小面积。**
**① 写切线截距与面积函数。** $P(x,2x-x^2)$，$y'=2-2x$，切线为 $Y=(2-2x)X+x^2$。与两正半轴相交要求 $1<x<2$；$y$ 轴截距 $OA=x^2$，$x$ 轴截距 $OB=\dfrac{x^2}{2(x-1)}$，故
$$S(x)=\frac12\cdot x^2\cdot\frac{x^2}{2(x-1)}=\frac{x^4}{4(x-1)}.$$
**② 求导定最小值。** $S'(x)=\dfrac{x^3(3x-4)}{4(x-1)^2}$。当 $1<x<\dfrac43$ 时 $S'<0$，当 $\dfrac43<x<2$ 时 $S'>0$，故 $x=\dfrac43$ 处取最小值，此时 $y=\dfrac89$，
$$S_{\min}=\frac{(4/3)^4}{4(4/3-1)}=\frac{64}{27}.$$
【思路】（I）由切线 $y$ 轴截距写中点坐标，化为可降阶的一阶线性方程；（II）写出切线在两轴上的截距得面积函数，求导找最小。
【易错】中点纵坐标是 $\dfrac{y+(y-xy')}{2}$，不能漏掉 $P$ 自身的 $y$；第一象限要求 $0<x<2$，与正半轴围成三角形又要求 $x>1$。

===Q19===
【答案】$f(x,y)=\dfrac{x^3}{3}-x+xe^{\cos y}$；极小值 $-\dfrac23(1-e^{-1})^{3/2}$ 在 $\left(\sqrt{1-e^{-1}},(2k+1)\pi\right)$ 取得，极大值 $\dfrac23(1-e^{-1})^{3/2}$ 在 $\left(-\sqrt{1-e^{-1}},(2k+1)\pi\right)$ 取得，$k\in\mathbb{Z}$
【解】
**① 由全微分还原 $f$。** $f_x=x^2-1+e^{\cos y}$，对 $x$ 积分得 $f=\dfrac{x^3}{3}-x+xe^{\cos y}+C(y)$。再对 $y$ 求偏导得 $f_y=-xe^{\cos y}\sin y+C'(y)$，与已知比较得 $C'(y)=0$。由 $f(0,0)=0$ 得 $C=0$，故
$$f(x,y)=\frac{x^3}{3}-x+xe^{\cos y}.$$
**② 求驻点。** 令 $f_x=x^2-1+e^{\cos y}=0$、$f_y=-xe^{\cos y}\sin y=0$。若 $x=0$，则 $e^{\cos y}=1$，即 $\cos y=0$，$y=\dfrac\pi2+k\pi$；若 $\sin y=0$，则 $y=k\pi$，$y=2k\pi$ 时 $x^2=1-e<0$ 无实数解，$y=(2k+1)\pi$ 时 $x^2=1-e^{-1}$。驻点为 $\left(0,\dfrac\pi2+k\pi\right)$ 与 $\left(\pm\sqrt{1-e^{-1}},(2k+1)\pi\right)$。
**③ 二阶判别。** 记 $A=f_{xx}=2x$，$B=f_{xy}=-e^{\cos y}\sin y$，$C_0=f_{yy}=xe^{\cos y}(\sin^2y-\cos y)$。在 $\left(0,\dfrac\pi2+k\pi\right)$ 处 $A=C_0=0,\ B=\pm1$，$AC_0-B^2=-1<0$，不是极值点。在 $\left(\sqrt{1-e^{-1}},(2k+1)\pi\right)$ 处 $A>0,\ AC_0-B^2=2(1-e^{-1})e^{-1}>0$，为极小值点，极小值 $-\dfrac23(1-e^{-1})^{3/2}$；在 $\left(-\sqrt{1-e^{-1}},(2k+1)\pi\right)$ 处 $A<0,\ AC_0-B^2>0$，为极大值点，极大值 $\dfrac23(1-e^{-1})^{3/2}$。
【思路】对 $f_x$ 积分并对 $y$ 比较定出 $C(y)$，解 $f_x=f_y=0$ 得驻点，再用二阶判别法 $AC_0-B^2$ 分类。
【易错】由 $e^{\cos y}=1$ 应推出 $\cos y=0$ 而非 $\cos y=1$；驻点 $\left(0,\dfrac\pi2+k\pi\right)$ 是鞍点，不是极值点。

===Q20===
【答案】$\dfrac29+\dfrac{\pi}{24}$
【解】
**① 按 $x$ 与 $y$ 的大小拆分。** 在第一象限
$$|\sqrt{xy-y^2}|=\begin{cases}\sqrt{y^2-xy},&x<y,\\[3pt]\sqrt{xy-y^2},&x\ge y.\end{cases}$$
用直线 $y=x$ 把 $D$ 分为 $D_1\ (x<y)$ 与 $D_2\ (x\ge y)$。
**② 计算 $D_1$ 上的积分。** 先对 $x$ 积分：
$$\iint_{D_1}\sqrt{y^2-xy}\,dxdy=\int_0^1dy\int_0^y\sqrt{y^2-xy}\,dx=\int_0^1\frac23 y^2\,dy=\frac29.$$
**③ 计算 $D_2$ 上的积分。** 先对 $x$ 积分再作换元 $y=\sin^2 t$：
$$\iint_{D_2}\sqrt{xy-y^2}\,dxdy=\int_0^1dy\int_y^1\sqrt{xy-y^2}\,dx=\frac43\int_0^{\pi/2}\sin^2t\cos^2t\,dt=\frac{\pi}{24}.$$
两部分相加得 $I=\dfrac29+\dfrac{\pi}{24}$。
【思路】先用绝对值把被积函数拆成分段形式，对 $x$ 积分后分别用幂函数积分与三角换元求单积分。
【易错】$D_1$ 与 $D_2$ 的被积函数根号内符号相反，不能在整块 $D$ 上直接用 $\sqrt{xy-y^2}$；$D_2$ 的结果是 $\pi/24$ 而非 $2/9$。

===Q21===
【答案】充要条件成立：若 $f'(x)$ 单调不减则不等式成立；若不等式对任意 $a<b$ 成立则 $f'(x)$ 单调不减
【解】
**（I）充分性。**
**① 构造辅助函数。** 固定 $a$，令
$$F(t)=\int_a^t xf'(x)\,dx-\frac{a+t}{2}\big[f(t)-f(a)\big],\qquad t\ge a,$$
则 $F(a)=0$，且
$$F'(t)=tf'(t)-\frac12\big[f(t)-f(a)\big]-\frac{a+t}{2}f'(t)=\frac{t-a}{2}f'(t)-\frac12\big[f(t)-f(a)\big],$$
进而 $F''(t)=\dfrac{t-a}{2}f''(t)$。
**② 由 $f''\ge0$ 得结论。** 若 $f'$ 单调不减，由 $f''$ 连续得 $f''(x)\ge0$，故 $t>a$ 时 $F''(t)\ge0$。结合 $F'(a)=0$ 得 $F'(t)\ge0$，从而 $F(t)\ge0$。取 $t=b$ 即
$$\int_a^b xf'(x)\,dx\ge\frac{a+b}{2}\big[f(b)-f(a)\big].$$
**（II）必要性（逆否命题）。**
**① 反设 $f'$ 不单调不减。** 则存在 $x_1<x_2$ 使 $f'(x_1)>f'(x_2)$。对 $f'$ 用拉格朗日中值定理，存在 $x_0\in(x_1,x_2)$ 使
$$f''(x_0)=\frac{f'(x_2)-f'(x_1)}{x_2-x_1}<0.$$
由 $f''$ 连续，存在 $\delta>0$，在 $(x_0-\delta,x_0+\delta)$ 内恒有 $f''(x)<0$。
**② 构造反例。** 在该区间内取 $a<b$，仍令上述 $F(t)$。此时对 $t\in(a,b)$ 有 $F''(t)=\dfrac{t-a}{2}f''(t)<0$，又 $F'(a)=0$，故 $F'(t)<0$，$F(t)<0$，取 $t=b$ 得
$$\int_a^b xf'(x)\,dx<\frac{a+b}{2}\big[f(b)-f(a)\big],$$
与题设矛盾。故逆否命题成立，必要性得证。
【思路】构造差值函数 $F(t)$ 并二次求导得 $\dfrac{t-a}{2}f''(t)$；充分性用 $f''\ge0$，必要性用逆否命题与 $f''<0$ 的局部区间。
【易错】$F''$ 含因子 $(t-a)$，只在 $t\ge a$ 时符号才由 $f''$ 决定；必要性宜用逆否命题，不能直接由积分不等式推出 $f''$ 点点非负。

===Q22===
【答案】（I）$A=\begin{pmatrix}c_1-c_2&2c_1-c_2&c_1&c_2\\ c_3-c_4&2c_3-c_4&c_3&c_4\end{pmatrix}$，其中 $\begin{vmatrix}c_1&c_2\\ c_3&c_4\end{vmatrix}\ne0$；（II）$a=3,\ b=2,\ c=1,\ d=1$
【解】
**（I）求所有矩阵 $A$。**
**① 转置为齐次方程。** 由 $A(\alpha_1,\alpha_2)=O$ 得 $(\alpha_1,\alpha_2)^T A^T=O$，即 $A^T$ 的每个列向量都是齐次方程组 $(\alpha_1,\alpha_2)^T x=0$ 的解。
**② 求基础解系。** 
$$(\alpha_1,\alpha_2)^T=\begin{pmatrix}1&-2&3&-1\\0&1&-2&1\end{pmatrix}\to\begin{pmatrix}1&0&-1&1\\0&1&-2&1\end{pmatrix},$$
基础解系为 $\xi_1=(1,2,1,0)^T,\ \xi_2=(-1,-1,0,1)^T$。
**③ 写出 $A$ 的一般形式。** 设 $A^T$ 的两列分别为 $c_1\xi_1+c_2\xi_2$ 与 $c_3\xi_1+c_4\xi_2$，转置回去得
$$A=\begin{pmatrix}c_1-c_2&2c_1-c_2&c_1&c_2\\ c_3-c_4&2c_3-c_4&c_3&c_4\end{pmatrix}.$$
因 $Ax=0$ 的基础解系含 2 个向量，解空间维数为 2，故 $r(A)=2$，需 $\begin{vmatrix}c_1&c_2\\ c_3&c_4\end{vmatrix}\ne0$。
**（II）由同解求参数。**
**① 列出方程。** $Ax=0$ 与 $Bx=0$ 同解等价于 $\alpha_1,\alpha_2$ 也是 $Bx=0$ 的解，即
$$B(\alpha_1,\alpha_2)=\begin{pmatrix}1-2a+3b-c&a-2b+c\\ d-8+3a-b&4-2a+b\end{pmatrix}=O.$$
**② 求解并验证。** 由四个方程
$$1-2a+3b-c=0,\quad a-2b+c=0,\quad d-8+3a-b=0,\quad 4-2a+b=0$$
解得 $a=3,\ b=2,\ c=1,\ d=1$，代回检验满足要求。
【思路】（I）把 $A(\alpha_1,\alpha_2)=O$ 转置为关于 $A^T$ 行向量的齐次方程；（II）同解等价于 $B$ 也以 $\alpha_1,\alpha_2$ 为解，列方程组求参。
【易错】$A$ 是 $2\times4$ 矩阵，$r(A)=2$ 要求两行线性无关，即 $\begin{vmatrix}c_1&c_2\\ c_3&c_4\end{vmatrix}\ne0$；同解只需 $B\alpha_i=0$，不必要求 $B$ 与 $A$ 行等价。
