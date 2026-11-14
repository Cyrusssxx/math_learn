===Q1===
【答案】A
【解】
**① 换元。** 令 $t=\dfrac1x$，则 $x\to\infty$ 时 $t\to0$，且 $ax\sin\dfrac1x=\dfrac{a\sin t}{t}$，故
$$\lim_{x\to\infty}x^2\left(2a-ax\sin\frac1x-b\cos\frac1x\right)=\lim_{t\to0}\frac{2a-\frac{a\sin t}{t}-b\cos t}{t^2}=\lim_{t\to0}\frac{2at-a\sin t-bt\cos t}{t^3}.$$
**② 泰勒展开。** 代入 $\sin t=t-\dfrac{t^3}{6}+o(t^3)$，$\cos t=1-\dfrac{t^2}{2}+o(t^2)$：
$$\frac{2at-a\left[t-\frac{t^3}{6}+o(t^3)\right]-bt\left[1-\frac{t^2}{2}+o(t^2)\right]}{t^3}=\frac{(a-b)t+\left(\frac a6+\frac b2\right)t^3+o(t^3)}{t^3}.$$
**③ 定参数。** 极限存在且为 $\dfrac12$ 当且仅当 $\begin{cases}a-b=0,\\ \dfrac a6+\dfrac b2=\dfrac12,\end{cases}$ 解得 $a=b=\dfrac34$，故选 A。
【思路】令 $t=1/x$ 化为 $\frac00$ 型，用泰勒展开按 $t$ 的幂次配平：一次项系数须为零，三次项系数即为极限值。
【易错】$ax\sin\dfrac1x$ 换元后是 $\dfrac{a\sin t}{t}$，分子分母须同乘 $t$ 才化成分母 $t^3$；$\cos t$ 的 $-\dfrac{t^2}{2}$ 项与前面的 $t$ 相乘凑出 $t^3$，系数是 $\dfrac b2$ 而非 $\dfrac b6$。
===Q2===
【答案】D
【解】
**① 求拐点。** $y'=\dfrac{x^4}{4}-x^3+x^2+C_1$，$y''=x^3-3x^2+2x=x(x-1)(x-2)$。$y''$ 在 $x=0,1,2$ 两侧均变号，故 $(0,y(0)),(1,y(1)),(2,y(2))$ 都是拐点，其中
$$y(0)=C_2,\quad y(1)=\frac{2}{15}+C_1+C_2,\quad y(2)=\frac{4}{15}+2C_1+C_2.$$
**② 判共线。** 三点共线要求
$$\frac{y(1)-y(0)}{1-0}=\frac{y(2)-y(1)}{2-1}=\frac{y(2)-y(0)}{2-0},$$
而这三个差商都等于 $\dfrac{2}{15}+C_1$，与 $C_1,C_2$ 的取值无关。
**③ 结论。** 任意 $C_1,C_2$ 下三个拐点恒共线，故选 D。
【思路】先由 $y''$ 的变号零点定出三个拐点，再验证三点之间的两个斜率与整体斜率恒相等。
【易错】三个拐点横坐标是 $0,1,2$，须逐个验证 $y''$ 变号；选项 A 对应三点落在直线 $y=0$ 上、选项 B 对应落在 $y=x+1$ 上，都只是特例，不能误认为必须成立。
===Q3===
【答案】B
【解】
**① 化简 $I_1$。** 由 $x^2-x+4=\left(x-\dfrac12\right)^2+\dfrac{15}{4}$ 知 $\dfrac{1}{\sqrt{4-x+x^2}}$ 关于 $x=\dfrac12$ 对称，故
$$\int_{\frac12}^1\frac{1}{\sqrt{4-x+x^2}}dx=\int_0^{\frac12}\frac{1}{\sqrt{4-x+x^2}}dx,\quad \int_0^1\frac{1}{\sqrt{4-x+x^2}}dx=2I_1.$$
**② 换元统一分母。** 令 $u=\sqrt x$，则
$$\int_0^1\frac{1}{\sqrt{4-x+x^2}}dx=\int_0^1\frac{2u\,du}{\sqrt{4-u^2+u^4}}=\int_0^1\frac{2x}{\sqrt{4-x^2+x^4}}dx,$$
$$I_1=\frac12\int_0^1\frac{2x}{\sqrt{4-x^2+x^4}}dx=\int_0^1\frac{x}{\sqrt{4-x^2+x^4}}dx.$$
**③ 比较 $I_1$ 与 $I_3$。** 当 $x\in(0,1)$ 时 $e^x-1>x$，故 $\dfrac{e^x-1}{\sqrt{4-x^2+x^4}}>\dfrac{x}{\sqrt{4-x^2+x^4}}$，得 $I_1<I_3$。
**④ 比较 $I_1$ 与 $I_2$。** 当 $x\in(0,1)$ 时 $x^3>x^4$，故 $4-x^2+x^3>4-x^2+x^4$，从而 $\dfrac{x}{\sqrt{4-x^2+x^3}}<\dfrac{x}{\sqrt{4-x^2+x^4}}$，得 $I_2<I_1$。
**⑤ 结论。** $I_2<I_1<I_3$，选 B。
【思路】用对称性与 $u=\sqrt x$ 把 $I_1$ 化到与 $I_2,I_3$ 同型的分母，再逐对比较被积函数。
【易错】三个被积式的分母分别是 $4-x+x^2$、$4-x^2+x^3$、$4-x^2+x^4$，须逐一对应；$I_1$ 的积分上限是 $\dfrac12$ 而非 $1$；比较只能在 $x\in(0,1)$ 上使用 $x^3>x^4$ 与 $e^x-1>x$。
===Q4===
【答案】A
【解】
**① 转化。** 记 $f(x)=a^2\sec^2x+b^2\csc^2x$，在定义域 $D=\left(0,\frac\pi2\right)\cup\left(\frac\pi2,\pi\right)\cup\left(\pi,\frac{3\pi}2\right)\cup\left(\frac{3\pi}2,2\pi\right)$ 上以 $2\pi$ 为周期；$k$ 的最大值即 $\min f(x)$。
**② 恒等变形。** 由 $\sec^2x=1+\tan^2x$、$\csc^2x=1+\cot^2x$，
$$f(x)=a^2+b^2+a^2\tan^2x+\frac{b^2}{\tan^2x}.$$
**③ 基本不等式。** 令 $u=\tan^2x>0$，由 $ab>0$ 得
$$a^2u+\frac{b^2}{u}\ge2\sqrt{a^2u\cdot\frac{b^2}{u}}=2ab,$$
等号当且仅当 $a^2u=\dfrac{b^2}{u}$ 即 $u=\dfrac ba>0$ 时取得；$D$ 上 $\tan x$ 可取遍 $\mathbb{R}\setminus\{0\}$，故 $u=\dfrac ba$ 可达。
**④ 结论。** $\min f(x)=a^2+b^2+2ab=(a+b)^2$，即 $k$ 的最大值为 $(a+b)^2$，选 A。
【思路】用 $\sec^2=1+\tan^2$、$\csc^2=1+\cot^2$ 把 $f$ 配成 $a^2u+\dfrac{b^2}{u}$，由均值不等式一次读出最小值。
【易错】$\cot^2x=\dfrac{1}{\tan^2x}$ 与 $\tan^2x$ 互为倒数；条件 $ab>0$ 同时保证 $\sqrt{a^2b^2}=ab$ 且 $u=\dfrac ba>0$ 可取；由该变形还可知 $\pi$ 也是 $f(x)$ 的一个周期；题干「对任意的 $x$」须理解为定义域 $D$ 内，$x=0,\frac\pi2,\pi,\frac{3\pi}2$ 处 $\sec x,\csc x$ 无意义。
===Q5===
【答案】C
【解】
**① 定 $f(0)$。** 令 $x=0$ 代入 $f(x+y)=f(x)f(y)$ 得 $f(0)=[f(0)]^2$，由 $f(0)\ne0$ 得 $f(0)=1$。
**② 导数定义。** 
$$f'(x)=\lim_{\Delta x\to0}\frac{f(x+\Delta x)-f(x)}{\Delta x}=\lim_{\Delta x\to0}\frac{f(x)\left[f(\Delta x)-1\right]}{\Delta x}=f(x)\lim_{\Delta x\to0}\frac{f(\Delta x)-f(0)}{\Delta x}=af(x).$$
**③ 解微分方程。** $y'=ay$ 分离变量得 $\ln|y|=ax+C_0$，由 $f(0)=1$ 定出 $f(x)=e^{ax}$。
**④ 判凹凸。** $f''(x)=a^2e^{ax}>0$ 对任意 $a\ne0$ 恒成立，故 $f(x)$ 为凹函数；而 $f'(x)=ae^{ax}$ 的符号随 $a$ 变，不恒增也不恒减，选 C。
【思路】由函数方程配合导数定义导出 $f'=af$，解出 $f=e^{ax}$，再用 $f''>0$ 判定凹凸。
【易错】$f(0)=1$ 需由 $f(0)\ne0$ 排除 $0$ 得到；$a$ 可正可负，故单调性不确定，唯一与 $a$ 符号无关的结论是 $f''=a^2e^{ax}>0$；本题沿用 $f''>0$ 称「凹函数」的约定。
===Q6===
【答案】C
【解】
**① 判连续。** 当 $(x,y)\ne(0,0)$ 时 $\ln f(x,y)=-(|x|+|y|)\ln(x^2+y^2)$，故
$$|\ln f(x,y)|\le\sqrt{2(x^2+y^2)}\,\left|\ln(x^2+y^2)\right|.$$
令 $t=\sqrt{x^2+y^2}$，右端等于 $2\sqrt2\,t\,|\ln t|$，而
$$\lim_{t\to0^+}t\ln t=\lim_{t\to0^+}\frac{\ln t}{\frac1t}\xlongequal{\text{洛必达}}\lim_{t\to0^+}\frac{\frac1t}{-\frac1{t^2}}=0,$$
由夹逼得 $\lim\limits_{(x,y)\to(0,0)}\ln f(x,y)=0$，即 $\lim\limits_{(x,y)\to(0,0)}f(x,y)=1=f(0,0)$，二重极限存在且连续。
**② 判可微。** 沿 $y=0$ 有 $f(x,0)=\left(\dfrac1{x^2}\right)^{|x|}$，
$$\left.\frac{\partial f}{\partial x}\right|_{(0,0)}=\lim_{x\to0}\frac{\left(\frac1{x^2}\right)^{|x|}-1}{x}=\lim_{x\to0}\frac{e^{-|x|\ln x^2}-1}{x}=\lim_{x\to0}\frac{-|x|\ln x^2}{x},$$
$x\to0^+$ 时该极限为 $+\infty$，$x\to0^-$ 时为 $-\infty$，故 $\left.\dfrac{\partial f}{\partial x}\right|_{(0,0)}$ 不存在。
**③ 结论。** 偏导不存在即不可微，故 $f$ 在 $(0,0)$ 处连续但不可微，选 C。
【思路】取对数把幂指函数化为乘积，用 $t\ln t\to0$ 夹逼出连续性；再用偏导定义算 $x$ 方向的极限证明不可微。
【易错】$f(x,0)=\left(\dfrac1{x^2}\right)^{|x|}$ 的指数含 $|x|$，$\dfrac{-|x|\ln x^2}{x}$ 左右极限反号发散；二重极限存在且等于 $f(0,0)=1$，故 (A)(B) 皆错。
===Q7===
【答案】D
【解】
**① 轮换对称性。** 记 $f(x,y)=(\sin^2x+\cos^2y)(x+y)$，则 $f(y,x)=(\sin^2y+\cos^2x)(y+x)$，二者相加为 $2(x+y)$。区域 $D=[0,\pi]^2$ 关于 $y=x$ 对称，故
$$\iint_Df(x,y)dxdy=\frac12\iint_D\left[f(x,y)+f(y,x)\right]dxdy=\iint_D(x+y)dxdy=2\iint_Dx\,dxdy.$$
**② 写和式极限。** 把 $[0,\pi]$ 分 $2n$ 等份，$\Delta\sigma_{ij}$ 面积为 $\dfrac{\pi^2}{4n^2}$，取点 $\left(\dfrac{i\pi}{2n},\dfrac{j\pi}{2n}\right)$：
$$\iint_Dx\,dxdy=\lim_{n\to\infty}\sum_{i=1}^{2n}\sum_{j=1}^{2n}\frac{i\pi}{2n}\cdot\frac{\pi^2}{4n^2}=\frac{\pi^3}{4}\lim_{n\to\infty}\sum_{i=1}^{2n}\frac{i}{n^2}.$$
**③ 用 $D_1$ 改写。** 记 $D_1=\{0\le y\le x\le\pi\}$，由轮换对称性 $\iint_D(x+y)dxdy=2\iint_{D_1}(x+y)dxdy$，而
$$\iint_{D_1}(x+y)dxdy=\lim_{n\to\infty}\sum_{i=1}^{2n}\sum_{j=1}^{i}\left(\frac{i\pi}{2n}+\frac{j\pi}{2n}\right)\frac{\pi^2}{4n^2}=\frac{\pi^3}{8}\lim_{n\to\infty}\sum_{i=1}^{2n}\sum_{j=1}^{i}\frac{i+j}{n^3}.$$
**④ 结论。** 
$$\iint_Df(x,y)dxdy=\frac{\pi^3}{2}\lim_{n\to\infty}\sum_{i=1}^{2n}\frac{i}{n^2}=\frac{\pi^3}{4}\lim_{n\to\infty}\sum_{i=1}^{2n}\sum_{j=1}^{i}\frac{i+j}{n^3},$$
只有 (D) 与之相符，选 D。
【思路】先用轮换对称性把被积函数降为 $x+y$，再按 $2n$ 等分直接写出二重积分的定义式与四个选项比对。
【易错】选项 (C)(D) 内层求和上限是 $i$（三角形 $y\le x$），不是 $n$；由 ② 得系数 $\dfrac{\pi^3}{2}$，而 (A) 的求和上限为 $n$、(B) 的系数为 $\pi^3$，均不符；选项 A 对应的极限值恰为 $\iint_Dx\,dxdy$，少了因子 2。
===Q8===
【答案】D
【解】
**① 一个方向的秩不等式。** 显然 $r(\alpha_1,\alpha_2,\cdots,\alpha_{t-1},\beta)\le r(\alpha_1,\alpha_2,\cdots,\alpha_t,\beta)$。
**② 反向表出。** 由 $\beta$ 可由 $\alpha_1,\alpha_2,\cdots,\alpha_t$ 线性表示，设
$$\beta=k_1\alpha_1+k_2\alpha_2+\cdots+k_t\alpha_t. \quad (1)$$
因 $\beta$ 不能由 $\alpha_1,\alpha_2,\cdots,\alpha_{t-1}$ 线性表示，故 $k_t\ne0$，于是
$$\alpha_t=\frac1{k_t}\beta-\frac{k_1}{k_t}\alpha_1-\cdots-\frac{k_{t-1}}{k_t}\alpha_{t-1},$$
即 $\alpha_t$ 可由 $\alpha_1,\cdots,\alpha_{t-1},\beta$ 表出，从而 $r(\alpha_1,\cdots,\alpha_t,\beta)\le r(\alpha_1,\cdots,\alpha_{t-1},\beta)$。
**③ 结论。** 两边夹得 $r(\alpha_1,\cdots,\alpha_t,\beta)=r(\alpha_1,\cdots,\alpha_{t-1},\beta)$，选 D。
【思路】把「$\beta$ 可由全组表出、不可由前 $t-1$ 个表出」翻译成 (1) 中末项系数 $k_t\ne0$，从而可反解出 $\alpha_t$。
【易错】取 $\alpha_1=(1,0,0)^T,\alpha_2=(2,0,0)^T,\alpha_3=(0,1,0)^T,\beta=(0,1,1)^T$，满足题设但 $r(\alpha_1,\alpha_2,\alpha_3)=2<t=3$，故 (A)(B) 错；若 $\alpha_t$ 可由前 $t-1$ 个表出，代回 (1) 会推出 $\beta$ 可由前 $t-1$ 个表出而矛盾，故 $r(\alpha_1,\cdots,\alpha_{t-1})<r(\alpha_1,\cdots,\alpha_t)$，(C) 错。
===Q9===
【答案】C
【解】
**① 由解定参数。** 由 $A(1,2,1)^T=(0,0,1)^T$ 逐行代入得
$$\begin{cases}a^2+2a+1=0,\\ b^2+2b+1=0,\\ c^2+2c+1=1,\end{cases}$$
解得 $a=b=-1$，$c=-2$ 或 $c=0$；由 $c\ne0$ 取 $c=-2$，故
$$A=\begin{pmatrix}1&-1&1\\1&-1&1\\1&-2&4\end{pmatrix}.$$
**② 定秩。** $A$ 的前两行相同，故 $|A|=0$，$r(A)\le2$；第三行与第一行线性无关，$r(A)\ge2$，故 $r(A)=2$，$Ax=0$ 的基础解系只含 $3-2=1$ 个向量，(D) 错。
**③ 判各非齐次方程。** 增广矩阵
$$\overline{A}_1=\begin{pmatrix}1&-1&1&1\\1&-1&1&0\\1&-2&4&0\end{pmatrix},\quad \overline{A}_2=\begin{pmatrix}1&-1&1&1\\1&-1&1&1\\1&-2&4&0\end{pmatrix},$$
$r(\overline{A}_1)=3\ne r(A)$，故 $Ax=(1,0,0)^T$ 无解，同理 $Ax=(0,1,0)^T$ 无解；而 $r(\overline{A}_2)=2=r(A)$，故 $Ax=(1,1,0)^T$ 有解，选 C。
【思路】把「$(1,2,1)^T$ 是 $Ax=(0,0,1)^T$ 的解」逐行代入定出 $a,b,c$，再用 $r(A)$ 与各增广矩阵的秩判别三个方程组。
【易错】解向量是 $(1,2,1)^T$，不带系数 $\dfrac12$；第三行对应 $(c+1)^2=1$ 即 $c^2+2c+1=1$，$c=0$ 须由 $c\ne0$ 舍去；$A$ 前两行相同是 $r(A)=2$ 的关键；$\overline{A}_2$ 的前两行也相同，故秩仍为 2。
===Q10===
【答案】B
【解】
**① 判相似对角化。** 记 $A=\alpha\beta^T$，由 $\alpha^T\beta=\beta^T\alpha=0$ 得
$$A^2=\alpha\beta^T\alpha\beta^T=O.$$
若 $A\xi=\lambda\xi$，则 $A^2\xi=\lambda^2\xi=0$，故 $\lambda=0$ 是三重特征值。又 $A$ 各行都是 $\beta$ 的倍数且 $\alpha,\beta\ne0$，故 $r(A)=1$，$Ax=0$ 只有 $3-1=2$ 个线性无关解，即属于 $0$ 的线性无关特征向量只有 2 个，$A$ 不能相似对角化：① 正确、② 错。
**② 找公共特征向量。** 取 $\gamma$ 为方程组 $\begin{cases}\alpha^Tx=0,\\ \beta^Tx=0\end{cases}$ 的非零解，则 $\alpha\beta^T\gamma=0$、$\beta\alpha^T\gamma=0$，从而
$$(\alpha\beta^T+\beta\alpha^T)\gamma=0+0=0,$$
即 $\gamma$ 同时是 $\alpha\beta^T$ 与 $\alpha\beta^T+\beta\alpha^T$ 的属于 $0$ 的特征向量，④ 正确、③ 错。
**③ 结论。** 正确命题为 ①④，选 B。
【思路】用 $A^2=O$ 与 $r(A)=1$ 判定不可对角化，再取同时正交于 $\alpha,\beta$ 的 $\gamma$ 构造公共特征向量。
【易错】$\alpha^T\beta=0$ 使 $A^2=O$，但 $A\ne O$（$\alpha,\beta$ 均非零），三重零特征值只有 2 个线性无关特征向量；$\gamma$ 满足 $\alpha^T\gamma=\beta^T\gamma=0$，两个矩阵作用于 $\gamma$ 都给出 $0$，故 $0$ 是公共特征值。
===Q11===
【答案】$\dfrac{\sqrt3}{6}x-\dfrac\pi3-\dfrac{\sqrt3}{3}$
【解】
**① 由相切定 $f(-2),f'(-2)$。** $f(-2)=0$，且当 $x\ne0$ 时
$$\left(\arccos\frac1x-\frac{2\pi}{3}\right)'=-\frac{1}{\sqrt{1-\frac1{x^2}}}\cdot\left(-\frac1{x^2}\right)=\frac{1}{|x|\sqrt{x^2-1}},$$
代入 $x=-2$ 得 $f'(-2)=\dfrac{1}{2\sqrt3}$。
**② 由对称关系定 $f(2),f'(2)$。** 对 $f(x)+f(-x)=-\dfrac\pi3$ 两端求导得 $f'(x)-f'(-x)=0$，即 $f'(x)=f'(-x)$，故 $f'(2)=f'(-2)=\dfrac{1}{2\sqrt3}$；又 $f(2)+f(-2)=-\dfrac\pi3$，故 $f(2)=-\dfrac\pi3$。
**③ 写切线。** $y-\left(-\dfrac\pi3\right)=\dfrac{1}{2\sqrt3}(x-2)$，整理得 $y=\dfrac{\sqrt3}{6}x-\dfrac\pi3-\dfrac{\sqrt3}{3}$。
【思路】由相切读出 $x=-2$ 处的函数值与导数值，再用 $f(x)+f(-x)$ 为常数把信息搬到 $x=2$ 处。
【易错】$\sqrt{1-\frac1{x^2}}=\dfrac{\sqrt{x^2-1}}{|x|}$，故导数含 $|x|$，$x=-2$ 时 $|x|=2$；对 $f(x)+f(-x)=-\dfrac\pi3$ 求导时复合出 $-f'(-x)$，得 $f'$ 为偶函数而非奇函数。
===Q12===
【答案】$\tan x+\sec x-1$
【解】
**① 求导解出 $f'$。** 令 $x=0$ 得 $f(0)=0$；两端对 $x$ 求导：
$$f'(x)=1+f'(x)\sin x\quad\Rightarrow\quad f'(x)=\frac{1}{1-\sin x}.$$
**② 积分还原。** 由牛顿–莱布尼茨公式
$$f(x)=f(x)-f(0)=\int_0^x\frac{dt}{1-\sin t}=\int_0^x\frac{1+\sin t}{\cos^2t}dt=\int_0^x\left(\sec^2t+\tan t\sec t\right)dt$$
$$=(\tan t+\sec t)\Big|_0^x=\tan x+\sec x-1.$$
【思路】对含变限积分的等式求导解出 $f'(x)$，再有理化 $\dfrac1{1-\sin t}$ 后积分。
【易错】$f'(x)$ 出现在积分核里，求导后是 $f'(x)=1+f'(x)\sin x$，须移项解出；$\dfrac{1+\sin t}{\cos^2t}=\sec^2t+\tan t\sec t$；勿漏由 $f(0)=0$ 定出的常数 $-1$。
===Q13===
【答案】$\dfrac{4\pi}{3}\left(e^2+\dfrac1{e^2}-e-\dfrac1e\right)$
【解】
**① 去绝对值定边界。** $|\ln x|+|\ln y|=1$ 在四种符号组合下分别化为 $xy=e$、$y=\dfrac{x}{e}$、$y=ex$、$xy=\dfrac1e$，围成曲边四边形，四顶点为 $\left(\dfrac1e,1\right),(1,e),\left(1,\dfrac1e\right),(e,1)$。
**② 分两段算体积。** 以 $x=1$ 为界：$V_1$ 由 $y=ex$ 与 $xy=\dfrac1e$ 围成，$V_2$ 由 $xy=e$ 与 $y=\dfrac{x}{e}$ 围成，
$$V_1=\pi\int_{\frac1e}^1\left(e^2x^2-\frac{1}{e^2x^2}\right)dx=\pi\left(\frac{e^2}{3}+\frac1{e^2}-\frac1{3e}-\frac1e\right),$$
$$V_2=\pi\int_1^e\left(\frac{e^2}{x^2}-\frac{x^2}{e^2}\right)dx=\pi\left(e^2+\frac1{3e^2}-e-\frac e3\right).$$
**③ 合并。** 
$$V=V_1+V_2=\frac{4\pi}{3}\left(e^2+\frac1{e^2}-e-\frac1e\right).$$
【思路】按 $\ln x,\ln y$ 的符号拆出四条边界曲线，定出四个交点后分片用圆盘法求旋转体体积。
【易错】四条边界中 $y=ex$ 与 $y=\dfrac{x}{e}$ 是过原点的直线、$xy=e$ 与 $xy=\dfrac1e$ 是双曲线，勿张冠李戴；$V_1$ 的积分限是 $\left[\dfrac1e,1\right]$、$V_2$ 是 $[1,e]$，外半径平方减内半径平方的次序不能反。
===Q14===
【答案】$(1,2)$
【解】
**① 拆积分。** 被积函数可能的瑕点为 $x=0$ 与 $x=\dfrac\pi2$，以 $\dfrac\pi4$ 拆成两段分别讨论。
**② $x\to0^+$ 端。** 此时 $(1-\sin x)^{1-p}\to1$，$\dfrac{\tan x}{(1-\sin x)^{1-p}\sin^p x}\sim\dfrac{1}{x^{p-1}}$，该段收敛要求 $p-1<1$，即 $p<2$（$p\le1$ 时 $x=0$ 不是瑕点，自动收敛）。
**③ $x\to\frac\pi2^-$ 端。** 令 $t=\dfrac\pi2-x$，则 $\sin x=\cos t$、$1-\sin x=1-\cos t\sim\dfrac{t^2}{2}$、$\cos x=\sin t\sim t$，于是
$$\frac{\tan x}{(1-\sin x)^{1-p}\sin^p x}=\frac{\sin x}{\cos x(1-\sin x)^{1-p}\sin^p x}\sim\frac{2^{1-p}}{t^{3-2p}},$$
该段收敛要求 $3-2p<1$，即 $p>1$。
**④ 结论。** 两段同时收敛得 $1<p<2$。
【思路】两个瑕点分别作等价无穷小替换，把敛散性化为 $\int_0\dfrac{dx}{x^{p-1}}$ 与 $\int_0\dfrac{dt}{t^{3-2p}}$ 的 $p$ 判别。
【易错】$x\to0^+$ 时 $\tan x\sim x$、$\sin^p x\sim x^p$，故只需 $\dfrac1{x^{p-1}}$；$x\to\dfrac\pi2^-$ 时 $1-\sin x\sim\dfrac{t^2}{2}$ 贡献 $t^{2(1-p)}$，$\cos x\sim t$ 贡献 $t^{-1}$，合起来是 $t^{3-2p}$ 而非 $t^{1-p}$。
===Q15===
【答案】$\sin 1$
【解】
**① 定 $z(0,0)$。** 在 $z^3-3xy\sin z=1$ 中令 $x=0,y=0$ 得 $z^3=1$，故 $z(0,0)=1$。
**② 一次偏导。** 方程两端对 $x$ 求偏导：
$$3z^2\frac{\partial z}{\partial x}-3y\sin z-3xy\cos z\frac{\partial z}{\partial x}=0, \quad (1)$$
代入 $x=y=0,z=1$ 得 $\left.\dfrac{\partial z}{\partial x}\right|_{(0,0)}=0$。
**③ 混合偏导。** 将 (1) 两端再对 $y$ 求偏导，代入 $x=y=0,\ z=1,\ \left.\dfrac{\partial z}{\partial x}\right|_{(0,0)}=0$，所有含 $x,y$ 或 $\dfrac{\partial z}{\partial x}$ 的项均为零，只剩
$$3\left.\frac{\partial^2z}{\partial x\partial y}\right|_{(0,0)}-3\sin1=0\quad\Rightarrow\quad\left.\frac{\partial^2z}{\partial x\partial y}\right|_{(0,0)}=\sin1.$$
【思路】先由原方程定出 $z(0,0)=1$，一次求偏导得 $z_x(0,0)=0$，再对 (1) 关于 $y$ 求偏导并代入特殊点直接解出混合偏导。
【易错】$\sin z$ 对 $x$ 求偏导要产生 $\cos z\dfrac{\partial z}{\partial x}$；在 $(0,0,1)$ 处 $\sin z=\sin1$ 而非常数 $0$，它正是混合偏导的唯一非零驱动项；混合偏导项的系数是 $3z^2=3$。
===Q16===
【答案】$-8$
【解】
**① 写矩阵、由迹定 $b$。** 二次型矩阵
$$A=\begin{pmatrix}1&-2&2\\-2&-2&a\\2&a&b\end{pmatrix},$$
正交变换下标准形的系数即 $A$ 的特征值，故特征值为 $-7,-b,-b$。由 $\operatorname{tr}(A)=b-1=-7-2b$ 得 $b=-2$；再由 $|A|=(-7)(-b)^2=-28$。
**② 算行列式定 $a$ 的候选。** 作 $c_2+2c_1,\ c_3-2c_1$ 后按第一行展开：
$$|A|=\begin{vmatrix}1&0&0\\-2&-6&a+4\\2&a+4&-6\end{vmatrix}=36-(a+4)^2=20-a^2-8a,$$
令 $-28=20-a^2-8a$ 得 $(a-4)(a+12)=0$，即 $a=4$ 或 $a=-12$。
**③ 用余子式定 $a$。** $A_{11}=\begin{vmatrix}-2&a\\a&-2\end{vmatrix}=4-a^2=-12$，得 $a=\pm4$；与 ② 取交集得 $a=4$，故 $ab=4\times(-2)=-8$。
【思路】标准形系数即特征值，用迹与行列式两条不变量锁定 $b$ 与 $|A|$，再由 $A_{11}$ 从两个候选 $a$ 中定出唯一解。
【易错】交叉项系数要折半进矩阵（$-4x_1x_2\Rightarrow a_{12}=-2$，$2ax_2x_3\Rightarrow a_{23}=a$）；$b=-2$ 后 $|A|=-7b^2=-28$、$A_{11}=4-a^2$；两组 $a$ 必须取交集，不能只用行列式结果。
===Q17===
【答案】（I）$k=-\dfrac12$；（II）$f(x)$ 在 $x=0$ 处连续
【解】
**（I）求 $k$。** $\lim\limits_{x\to1^-}f(x)=\lim\limits_{x\to1^-}(1-\cos x)^{\sin\pi x}=(1-\cos1)^0=1$。当 $1<x\le2$ 时 $0<x-1\le1$，由 $f(x)+k=\dfrac12f(x-1)$ 得
$$f(x)=\frac12\left[1-\cos(x-1)\right]^{\sin\pi(x-1)}-k.$$
令 $t=x-1\to0^+$，先算
$$\lim_{t\to0^+}\ln(1-\cos t)^{\sin\pi t}=\lim_{t\to0^+}\pi t\ln(1-\cos t)=\pi\lim_{t\to0^+}\frac{\ln(1-\cos t)}{\frac1t}\xlongequal{\text{洛必达}}-\pi\lim_{t\to0^+}\frac{t^2\sin t}{1-\cos t}=0,$$
最后一步用 $1-\cos t\sim\dfrac{t^2}{2}$，故 $\lim\limits_{t\to0^+}(1-\cos t)^{\sin\pi t}=e^0=1$，从而 $\lim\limits_{x\to1^+}f(x)=\dfrac12-k$。由 $f$ 在 $x=1$ 处连续得 $1=\dfrac12-k$，即 $k=-\dfrac12$。
**（II）判 $x=0$ 处连续性。** 由 $k=-\dfrac12$ 得 $f(x)-\dfrac12=\dfrac12f(x-1)$；令 $x\to x+1$ 得 $f(x)=2f(x+1)-1$（$-1<x\le0$）。于是
$$f(0)=2f(1)-1=1,\quad \lim_{x\to0^-}f(x)=2\lim_{x\to0^-}f(x+1)-1\xlongequal{t=x+1}2\lim_{t\to1^-}f(t)-1=1,$$
而 $\lim\limits_{x\to0^+}f(x)=\lim\limits_{x\to0^+}(1-\cos x)^{\sin\pi x}=1$。三者相等，故 $f(x)$ 在 $x=0$ 处连续。
【思路】(I) 用 $x=1$ 处左右极限相等定 $k$，关键是把 $0^0$ 型极限取对数化为 $t\ln(1-\cos t)\to0$；(II) 把递推式反解成 $f(x)=2f(x+1)-1$，将 $x=0$ 的信息搬到 $x=1$。
【易错】递推关系是 $f(x)+k=\dfrac12f(x-1)$，右端为 $f(x-1)$ 而非导数；$\lim\limits_{t\to0^+}(1-\cos t)^{\sin\pi t}$ 是 $0^0$ 型，须取对数用洛必达，不能当作「非零数的 0 次幂」；$\sin\pi(x-1)$ 在 $x\to1^+$ 时趋于 $0$ 但底数也趋于 $0$。
===Q18===
【答案】$f(x,y)=x+\dfrac{2}{15(2\sin1-\cos1)}[y]\cos y$
【解】
**① 设常数。** 记 $A=\iint_D f(x,y)dxdy$，则 $f(x,y)=x+A[y]\cos y$。
**② 定区域与 $[y]$。** 解 $\begin{cases}x=y^2\\ x=|y|\end{cases}$ 得交点 $(0,0),(1,1),(1,-1)$；$D$ 关于 $x$ 轴对称，上半 $D_1=\{y^2\le x\le y,\ 0\le y\le1\}$ 上 $[y]=0$，下半 $D_2=\{y^2\le x\le-y,\ -1\le y\le0\}$（除原点）上 $[y]=-1$。
**③ 两端积分。** 
$$A=\iint_Dx\,dxdy+A\iint_D[y]\cos y\,dxdy\xlongequal{\text{对称性}}2\iint_{D_1}x\,dxdy-A\iint_{D_2}\cos y\,dxdy,$$
其中
$$2\iint_{D_1}x\,dxdy=2\int_0^1dy\int_{y^2}^yx\,dx=\int_0^1(y^2-y^4)dy=\frac2{15},$$
$$\iint_{D_2}\cos y\,dxdy=\int_{-1}^0(-y-y^2)\cos y\,dy\xlongequal{t=-y}\int_0^1(t-t^2)\cos t\,dt=2\sin1-\cos1-1.$$
**④ 解出 $A$。** 代入得 $A=\dfrac2{15}-(2\sin1-\cos1-1)A$，故 $A(2\sin1-\cos1)=\dfrac2{15}$，即
$$A=\frac{2}{15(2\sin1-\cos1)},\quad f(x,y)=x+\frac{2}{15(2\sin1-\cos1)}[y]\cos y.$$
【思路】把含未知积分的项记为常数 $A$，对等式两端在 $D$ 上积分，得到关于 $A$ 的一次方程。
【易错】$[y]$ 在 $D_1$ 上为 $0$、在 $D_2$ 上为 $-1$（个别点不影响积分）；$\int_0^1(t-t^2)\cos t\,dt$ 需两次分部积分得 $2\sin1-\cos1-1$，该量加 $1$ 后恰与 $A$ 的分母 $2\sin1-\cos1$ 相配。
===Q19===
【答案】$\dfrac18(e^\pi+1)$
【解】
**① 解微分方程。** 特征方程 $r^2+2r-2=0$ 的根为 $r_{1,2}=-1\pm\sqrt3$，齐次通解 $C_1e^{(-1+\sqrt3)x}+C_2e^{(-1-\sqrt3)x}$。$1+i$ 不是特征根，设特解 $y^*=e^x(A\cos x+B\sin x)$，代入方程得 $e^x(4B\cos x-4A\sin x)=e^x\cos x$，故 $A=0,\ B=\dfrac14$，
$$y=C_1e^{(-1+\sqrt3)x}+C_2e^{(-1-\sqrt3)x}+\frac14e^x\sin x.$$
**② 定常数。** 由 $f(0)=0$ 得 $C_2=-C_1$；由 $f'(0)=\dfrac14$ 得 $C_1(-1+\sqrt3)+C_2(-1-\sqrt3)+\dfrac14=\dfrac14$，联立得 $2\sqrt3C_1=0$，故 $C_1=C_2=0$，$f(x)=\dfrac14e^x\sin x$。
**③ 去 $\max$ 后积分。** $[0,\pi]$ 上 $\sin x\ge0$，$[\pi,2\pi]$ 上 $\sin x\le0$，故
$$\int_0^{2\pi}\max\{f(x),0\}dx=\int_0^\pi\frac14e^x\sin x\,dx.$$
记 $I=\int_0^\pi e^x\sin x\,dx$，两次分部积分得 $I=e^\pi+1-I$，即 $I=\dfrac{e^\pi+1}{2}$，故原积分 $=\dfrac14I=\dfrac18(e^\pi+1)$。
【思路】先解二阶常系数方程并用初值把齐次部分全部消去，再按 $\sin x$ 的符号去掉 $\max$，最后用分部积分算 $\int e^x\sin x$。
【易错】特征根是 $-1\pm\sqrt3$；特解系数由 $4B=1,\ 4A=0$ 定出；$\max\{f,0\}$ 只在 $[0,\pi]$ 上取 $f$，积分上限应改为 $\pi$ 而非 $2\pi$；$\int_0^\pi e^x\sin x\,dx=\dfrac{e^\pi+1}{2}$，结果还要乘 $\dfrac14$。
===Q20===
【答案】极小值 $-e^{-\frac34}$（在 $\left(-\dfrac12,1\right)$ 处取得），无极大值
【解】
**① 求驻点。** 
$$f'_x=(y+1)(1+xy-2x^2)e^{xy-x^2},\quad f'_y=x(1+x+xy)e^{xy-x^2}.$$
因 $e^{xy-x^2}>0$，解 $\begin{cases}(y+1)(1+xy-2x^2)=0,\\ x(1+x+xy)=0\end{cases}$：$x=0$ 代入第一式得 $y=-1$；另一支 $1+x+xy=0$ 与 $1+xy-2x^2=0$ 相减得 $x(2x+1)=0$，取 $x=-\dfrac12$ 得 $y=1$。故驻点为 $(0,-1)$ 与 $\left(-\dfrac12,1\right)$。
**② 判 $(0,-1)$。** $A=f''_{xx}(0,-1)=0,\ B=f''_{xy}(0,-1)=1,\ C=f''_{yy}(0,-1)=0$，$AC-B^2=-1<0$，非极值点。
**③ 判 $\left(-\dfrac12,1\right)$。** 
$$A=6e^{-\frac34},\quad B=-e^{-\frac34},\quad C=\frac14e^{-\frac34},$$
$$AC-B^2=\frac12e^{-\frac32}>0,\quad A>0,$$
故为极小值点，极小值 $f\left(-\dfrac12,1\right)=-\dfrac12\cdot2\cdot e^{-\frac12-\frac14}=-e^{-\frac34}$。
【思路】由指数因子恒正把驻点方程降为多项式组，再用 $AC-B^2$ 的符号逐个判别两个驻点。
【易错】$f''_{xy}$ 中含 $x(y+1)+(1+x+xy)(1+xy-2x^2)$，在 $\left(-\dfrac12,1\right)$ 处第二项为 $0$ 而第一项为 $-1$；$e^{xy-x^2}$ 在该点为 $e^{-3/4}$，故 $A,B,C$ 含 $e^{-3/4}$ 而 $AC-B^2=\dfrac12e^{-3/2}$，两者指数不同；极小值 $f\left(-\dfrac12,1\right)=-e^{-3/4}$。
===Q21===
【答案】（I）$1$；（II）$\max\limits_{0\le x\le1}f(x)>6$
【解】
**（I）** 
$$\int_0^1x(1-x)f(x)dx=\int_0^1xf(x)dx-\int_0^1x^2f(x)dx=0-(-1)=1.$$
**（II）** 记 $M=\max\limits_{0\le x\le1}f(x)$，令 $g(x)=M-f(x)\ge0$。则
$$\int_0^1xg(x)dx=\frac M2-\int_0^1xf(x)dx=\frac M2,\quad \int_0^1x^2g(x)dx=\frac M3-\int_0^1x^2f(x)dx=\frac M3+1,$$
故
$$\int_0^1x(1-x)g(x)dx=\frac M2-\left(\frac M3+1\right)=\frac M6-1.$$
另一方面 $x(1-x)g(x)$ 在 $[0,1]$ 上连续非负，故该积分 $\ge0$，得 $M\ge6$。
再证 $M\ne6$：若 $M=6$，则 $\int_0^1x(1-x)g(x)dx=0$，由被积函数连续非负得 $x(1-x)g(x)\equiv0$，从而在 $(0,1)$ 内 $g(x)\equiv0$，即 $f(x)\equiv6$，于是 $\int_0^1xf(x)dx=\int_0^16x\,dx=3$，与 $\int_0^1xf(x)dx=0$ 矛盾。故 $M>6$。
【思路】(I) 把 $x(1-x)$ 拆成 $x-x^2$ 直接代入已知积分；(II) 构造非负函数 $g=M-f$，用 $\int x(1-x)g\ge0$ 得 $M\ge6$，再由等号成立时的恒等性导出矛盾排除 $M=6$。
【易错】已知条件是 $\int_0^1xf(x)dx=0$（被积含因子 $x$）与 $\int_0^1x^2f(x)dx=-1$，不是 $\int_0^1f(x)dx=0$；$M\ge6$ 只是必要条件，必须补证 $M\ne6$ 才能得到严格大于；由 $g\equiv0$ 反推 $f\equiv6$ 时要用 $\int_0^1xf(x)dx=3\ne0$ 才构成矛盾。
===Q22===
【答案】（I）$A=\begin{pmatrix}\frac12&\frac32&0\\\frac32&\frac12&0\\0&0&-1\end{pmatrix}$；（II）$P=\begin{pmatrix}\frac{\sqrt2}{4}&-\frac12&0\\\frac{\sqrt2}{4}&\frac12&0\\0&0&\frac{\sqrt2}{2}\end{pmatrix}$（$P$ 不唯一），规范形 $z_1^2-z_2^2-z_3^2$
【解】
**（I）求 $A$。** 设 $\beta$ 是 $A$ 属于 $-1$ 的特征向量，由 $A^T\alpha=2\alpha$ 得 $\alpha^TA=2\alpha^T$，于是
$$\alpha^TA\beta=2\alpha^T\beta,\quad \alpha^TA\beta=\alpha^T(-\beta)=-\alpha^T\beta\ \Rightarrow\ \alpha^T\beta=0,$$
即 $\alpha$ 与属于 $-1$ 的特征向量都正交，故 $\alpha$ 只能属于特征值 $2$。单位化 $\varepsilon_1=\dfrac1{\sqrt2}(1,1,0)^T$，把属于 $-1$ 的两个线性无关特征向量单位正交化为 $\varepsilon_2,\varepsilon_3$，令 $Q=(\varepsilon_1,\varepsilon_2,\varepsilon_3)$，则 $Q^TAQ=\operatorname{diag}(2,-1,-1)$，故 $Q^T(A+E)Q=\operatorname{diag}(3,0,0)$，
$$A+E=3\varepsilon_1\varepsilon_1^T=\frac32\begin{pmatrix}1\\1\\0\end{pmatrix}(1,1,0)=\begin{pmatrix}\frac32&\frac32&0\\\frac32&\frac32&0\\0&0&0\end{pmatrix},$$
减去 $E$ 即得 (I) 中的 $A$。
**（II）化规范形。** 由 (I) 知 $A$ 实对称，故 $A+A^T=2A$，$f(x)=2x^TAx$。正交变换 $x=Qy$ 把 $f$ 化为 $4y_1^2-2y_2^2-2y_3^2$，再令 $P_1=\operatorname{diag}\left(\dfrac12,\dfrac{\sqrt2}{2},\dfrac{\sqrt2}{2}\right)$ 即得规范形 $z_1^2-z_2^2-z_3^2$，其中 $P=QP_1$。
由 $\alpha^Tx=0$ 即 $x_1+x_2=0$ 取 $\beta_1=(-1,1,0)^T,\ \beta_2=(0,0,1)^T$，单位化得 $\varepsilon_2=\dfrac1{\sqrt2}(-1,1,0)^T,\ \varepsilon_3=(0,0,1)^T$，于是
$$Q=\begin{pmatrix}\frac{\sqrt2}{2}&-\frac{\sqrt2}{2}&0\\\frac{\sqrt2}{2}&\frac{\sqrt2}{2}&0\\0&0&1\end{pmatrix},\quad P=QP_1=\begin{pmatrix}\frac{\sqrt2}{4}&-\frac12&0\\\frac{\sqrt2}{4}&\frac12&0\\0&0&\frac{\sqrt2}{2}\end{pmatrix}.$$
亦可用配方法：$f(x)=x_1^2+x_2^2-2x_3^2+6x_1x_2=(x_1+3x_2)^2-8x_2^2-2x_3^2$，得另一可逆变换 $x=Py$ 与同一规范形，$P$ 不唯一。
【思路】(I) 由 $A^T\alpha=2\alpha$ 推出 $\alpha$ 与 $-1$ 特征向量正交，从而写出谱分解 $A+E=3\varepsilon_1\varepsilon_1^T$；(II) 借 $A$ 实对称把 $A+A^T$ 化为 $2A$，正交对角化后再缩放得规范形。
【易错】$\alpha$ 是 $A^T$ 属于 $2$ 的特征向量，只能推出 $\alpha^TA=2\alpha^T$，须借 $\alpha^T\beta=0$ 才能断定 $\alpha$ 也是 $A$ 属于 $2$ 的特征向量；$A+E$ 的特征值是 $3,0,0$，故 $A+E$ 是秩 1 阵 $3\varepsilon_1\varepsilon_1^T$；规范形系数为 $\pm1$，$P$ 不唯一。
