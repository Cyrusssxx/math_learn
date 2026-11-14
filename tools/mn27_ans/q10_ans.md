===Q1===
【答案】D
【解】
**① 选项 (A)。** 由积分中值定理，$\int_x^{\sin x}\frac{\sin t}{1+t^2}dt=\frac{\sin\xi}{1+\xi^2}(\sin x-x)$，其中 $\xi$ 介于 $x$ 与 $\sin x$ 之间。$x\to0$ 时 $\xi\to0$，故 $\frac{\sin\xi}{1+\xi^2}\sim\xi$；又 $\sin x\sim x$ 得 $\xi\sim x$，且 $\sin x-x\sim-\frac{x^3}{6}$，于是
$$\int_x^{\sin x}\frac{\sin t}{1+t^2}dt\sim x\cdot\left(-\frac{x^3}{6}\right)=-\frac{x^4}{6},$$
为 $x$ 的 4 阶无穷小。
**② 选项 (B)。** $1-\sqrt{\cos 2t}=1-(1+\cos2t-1)^{\frac12}\sim-\frac12(\cos2t-1)\sim-\frac12\left(-\frac12\right)(2t)^2=t^2$，故
$$\int_{x^2}^{x^{\frac43}}(1-\sqrt{\cos2t})dt\sim\int_{x^2}^{x^{\frac43}}t^2dt=\frac13t^3\Big|_{x^2}^{x^{\frac43}}=\frac13(x^4-x^6)\sim\frac13x^4,$$
亦为 4 阶。
**③ 选项 (C)。** 由泰勒公式 $f(t)=f(0)+f'(0)t+o(t)\sim t$，故
$$\int_0^xtf(x-t)dt\sim\int_0^xt(x-t)dt=\frac{x^3}{6},$$
为 3 阶。
**④ 选项 (D)。** $(1+x^2)^{\tan x^3}-1=e^{\tan x^3\ln(1+x^2)}-1\sim\tan x^3\ln(1+x^2)\sim x^5$，为 5 阶。
**⑤ 结论。** 四者中阶数最高的是 $x^5$，故选 (D)。
【思路】用积分中值定理、等价无穷小与泰勒公式分别定出四个无穷小的阶，比较得最高阶为 (D)。
【易错】(B) 的积分上限是 $x^{\frac43}$（印得形似 $\frac{x^4}{3}$），下限 $x^2$ 代入 $\frac13t^3$ 得 $\frac13x^6$，故结果为 $\frac13x^4$ 而非 $\frac13x^3$；(D) 的指数是 $\tan x^3$，由 $e^u-1\sim u$ 得 $\tan x^3\ln(1+x^2)\sim x^5$，与 $\sin x^3$ 同阶。
===Q2===
【答案】A
【解】
**① 读出 $f(0)$ 与 $f'(0)$。** 由
$$\lim_{x\to0}\frac{f(x)+e^x-1}{\sin x}=\lim_{x\to0}\frac{f(x)}x+\lim_{x\to0}\frac{e^x-1}x=-1,$$
得 $f(0)=0,\ f'(0)=-2$。
**② 用泰勒公式作估计。** $f(x)=f(0)+f'(0)x+\frac12f''(\xi)x^2\ (x\in(-1,1),\ \xi$ 介于 $0$ 与 $x$ 之间$)$；由 $f''(x)<0$ 得 $f(x)\le f'(0)x=-2x$，对任意 $x\in(-1,1)$ 成立，故选 (A)。
【思路】由极限等于 $-1$ 拆出 $f'(0)=-2$，再用带拉格朗日余项的泰勒公式与 $f''<0$ 得到线性上界。
【易错】$\frac{f(x)+e^x-1}{\sin x}$ 要拆成 $\frac{f(x)}x+\frac{e^x-1}x$ 两项，第二项极限为 $1$，故 $\lim\frac{f(x)}x=-2$ 而不是 $-1$；余项 $\frac12f''(\xi)x^2\le0$ 是不等号方向的关键。
===Q3===
【答案】B
【解】
**① 求 $f'(x)$。** 由 $f(x)=\int_0^{1-x}e^{t(2-t)}dt$，变上限求导得
$$f'(x)=-e^{(1-x)[2-(1-x)]}=-e^{(1-x)(1+x)}=-e^{1-x^2}.$$
**② 分部积分。** 注意 $f(1)=0$，故
$$\int_0^1f(x)dx=\left.xf(x)\right|_0^1-\int_0^1xf'(x)dx=\int_0^1xe^{1-x^2}dx=-\frac12\int_0^1e^{1-x^2}d(1-x^2).$$
**③ 定值。** $-\frac12e^{1-x^2}\big|_0^1=\frac12(e-1)$，故选 (B)。
【思路】先对变上限积分求导得 $f'(x)=-e^{1-x^2}$，再用分部积分把 $\int_0^1f$ 化成可积的 $\int_0^1xe^{1-x^2}dx$。
【易错】上限是 $1-x$、被积指数是 $t(2-t)$，代入 $t=1-x$ 才得 $(1-x)(1+x)=1-x^2$；$f(1)=0$ 保证分部积分边界项 $\left.xf(x)\right|_0^1$ 为零，不能凭空丢掉。
===Q4===
【答案】D
【解】
**① 定 $y(0)$ 与 $y'(0)$。** 将 $x=0$ 代入题干方程得 $\arctan y=0$，故 $y(0)=0$；两边对 $x$ 求导：
$$\frac{y'}{1+y^2}+e^{(xy)^2}\cdot(y+xy')=1,$$
代入 $x=0,\ y(0)=0$ 得 $y'(0)=1$。
**② 再求导得 $y''(0)$。** 继续对 $x$ 求导：
$$\frac{y''(1+y^2)-2y(y')^2}{(1+y^2)^2}+e^{(xy)^2}\cdot2xy(y+xy')^2+e^{(xy)^2}\cdot(2y'+xy'')=0,$$
代入 $x=0,\ y(0)=0,\ y'(0)=1$ 得 $y''(0)=-2$。
**③ 结论。** $\left.d[y'(x)]\right|_{x=0}=y''(0)dx=-2dx$，故选 (D)。若改为对 $y$ 求导，则
$$\left.\frac{d[y'(x)]}{d[y(x)]}\right|_{x=0}=\frac{y''(0)dx}{y'(0)dx}=\frac{y''(0)}{y'(0)}=-2.$$
【思路】对隐函数方程连续求两次导，依次定出 $y(0),\ y'(0),\ y''(0)$，再写出所求微分。
【易错】指数因子是 $e^{(xy)^2}$，求导时多出 $2xy(y+xy')$，在 $x=0$ 处该项为 $0$；$y'(0)=1$ 使 $\frac{y''(0)}{y'(0)}$ 与 $y''(0)$ 数值相同，但两个导数含义不同。
===Q5===
【答案】D
【解】
**① 判 (A)。** $\lim\limits_{x\to0}f(x)=\lim\limits_{x\to0}\frac{e^x-1}x=1$，$f$ 在 $[-1,2]$ 上有界且只有有限个间断点，故可积。当 $\lim f(x)=f(0)$ 即 $a=1$ 时 $f$ 连续、存在原函数；当 $a\ne1$ 时 $x=0$ 为可去间断点，$f$ 在 $[-1,2]$ 上不存在原函数，故 (A) 错。
**② 判 (B)。** $\lim\limits_{x\to0^-}f(x)=\lim\limits_{x\to0^-}\frac{\sin x-x}{x^2}=\lim\limits_{x\to0^-}\frac{-\frac16x^3}{x^2}=0$，$\lim\limits_{x\to0^+}f(x)=\lim\limits_{x\to0^+}\frac{\ln(1+2x)}x=2$；左右极限不等，故 $F(x)=\int_0^xf(t)dt$ 在 $x=0$ 处不可导，(B) 错。
**③ 判 (C)。** $f(t^2)$ 为偶函数，$\int_0^xf(t^2)dt$ 为奇函数，于是 $F(x)=\dfrac{\int_0^xf(t^2)dt}{x}$ 为偶函数，(C) 错。
**④ 判 (D)。** $f(t)-f(-t)$ 为奇函数且以 $T$ 为周期，故
$$\int_0^T[f(t)-f(-t)]dt=\int_{-\frac T2}^{\frac T2}[f(t)-f(-t)]dt=0,$$
从而 $F(x)=\int_0^x[f(t)-f(-t)]dt$ 也是周期为 $T$ 的周期函数，(D) 正确。
【思路】用「可去间断点无原函数」「跳跃间断点使变限积分不可导」「奇偶函数的变限积分」及「一周期积分为零」逐项排除。
【易错】(A) 与 (B) 分别对应不同的 $f$（$\frac{e^x-1}x$ 与 $\frac{\sin x-x}{x^2},\frac{\ln(1+2x)}x$），不可混用；奇函数在对称区间上一周期积分为 $0$ 是 (D) 仍为周期函数的关键。
===Q6===
【答案】B
【解】
**① 连续性。** $f(x,y)=x^2+y^2-\dfrac{6x^2y^2}{x^2+y^2}$，因 $\dfrac{x^2}{x^2+y^2}$ 有界、$y^2\to0$，故 $\lim\limits_{\substack{x\to0\\y\to0}}f(x,y)=0=f(0,0)$，$f$ 在 $(0,0)$ 连续。
**② 偏导数与驻点。** $f'_x(0,0)=\lim\limits_{x\to0}\frac{f(x,0)-f(0,0)}x=\lim\limits_{x\to0}\frac{x^2}x=0$，同理 $f'_y(0,0)=0$，故 $(0,0)$ 是驻点。
**③ 非极值点。** 沿 $y=\pm x$ 有 $f(x,\pm x)=-x^2<0=f(0,0)$；沿 $y=0$ 有 $f(x,0)=x^2>0=f(0,0)$。或令 $x=r\cos\theta,\ y=r\sin\theta$：
$$f(x,y)=r^2-6r^2\cos^2\theta\sin^2\theta=r^2\left[1-\frac32(\sin2\theta)^2\right]=\frac14r^2(1+3\cos4\theta),$$
在 $\theta\in[0,2\pi)$ 上可正可负，故 $(0,0)$ 不是极值点。
**④ 可微性。** 
$$\lim_{\substack{x\to0\\y\to0}}\frac{f(x,y)-f(0,0)-f'_x(0,0)x-f'_y(0,0)y}{\sqrt{x^2+y^2}}=\lim_{\substack{x\to0\\y\to0}}\left(\sqrt{x^2+y^2}-\frac{6x^2y^2}{(x^2+y^2)^{\frac32}}\right)=0,$$
因 $\frac{6x^2y^2}{(x^2+y^2)^{3/2}}=6\cdot\frac{x^2}{x^2+y^2}\cdot\frac{y}{\sqrt{x^2+y^2}}\cdot y\to0$，故 $f$ 在 $(0,0)$ 可微。
**⑤ 混合偏导。** 当 $(x,y)\ne(0,0)$ 时 $f'_x(x,y)=2x-\dfrac{12xy^4}{(x^2+y^2)^2}$，于是
$$f''_{xy}(0,0)=\lim_{y\to0}\frac{f'_x(0,y)-f'_x(0,0)}y=\lim_{y\to0}\frac{0-0}y=0.$$
综上选 (B)。
【思路】按连续、偏导、极值、可微、混合偏导五个层次逐一验证，用两条路径或极坐标判非极值。
【易错】$\frac{x^2y^2}{(x^2+y^2)^{3/2}}$ 是「有界量乘无穷小」而非发散，可微性由此成立；$f'_x(0,y)=0$ 使 $f''_{xy}(0,0)=0$，不必对一般点表达式再取极限。
===Q7===
【答案】A
【解】
**① 由极限读 $f'(0)$。** $\lim\limits_{x\to0}\frac{f(x)}x=1$ 给出 $f(0)=0,\ f'(0)=1$。
**② 分子化极坐标。** 设 $D:x^2+y^2\le t^2$，
$$\iint_Df(x^2+y^2)dxdy=\int_0^{2\pi}d\theta\int_0^tf(r^2)rdr=2\pi\int_0^tf(r^2)rdr.$$
**③ 分母交换积分次序。**
$$\int_0^{t^2}dx\int_x^{t^2}e^{(x-y)^2}dy=\int_0^{t^2}dy\int_0^{y}e^{(x-y)^2}dx\xlongequal{x-y=u}\int_0^{t^2}dy\int_{-y}^{0}e^{u^2}du.$$
**④ 洛必达。**
$$\lim_{t\to0^+}\frac{2\pi\int_0^tf(r^2)rdr}{\int_0^{t^2}\left(\int_{-y}^{0}e^{u^2}du\right)dy}=\lim_{t\to0^+}\frac{2\pi f(t^2)\cdot t}{2t\cdot\int_{-t^2}^{0}e^{u^2}du}=\pi\lim_{t\to0^+}\frac{f(t^2)}{\int_{-t^2}^{0}e^{u^2}du}.$$
**⑤ 积分中值。** $\int_{-t^2}^{0}e^{u^2}du=t^2e^{\xi^2}\ (\xi$ 介于 $0$ 与 $-t^2$ 之间$)$，故
$$\pi\lim_{t\to0^+}\frac{f(t^2)}{t^2e^{\xi^2}}=\pi\frac{f'(0)}1=\pi,$$
故选 (A)。
【思路】分子用极坐标化为变上限积分，分母交换次序后凑成 $\int e^{u^2}du$，再洛必达配合积分中值定理把极限化为 $\pi f'(0)$。
【易错】分子积分域半径为 $t$、分母外层上限为 $t^2$，求导后因子分别为 $2\pi f(t^2)t$ 与 $2t\int_{-t^2}^0e^{u^2}du$；$\frac{f(t^2)}{t^2}\to f'(0)=1$、$e^{\xi^2}\to1$，结果是 $\pi$ 而非 $2\pi$。
===Q8===
【答案】C
【解】
**① 判 ①。** 由题意 $r(A)=n-l,\ r(B)=n-m$。因 $r(BA)\le\min\{r(A),r(B)\}=\min(n-l,n-m)$，故 $(BA)x=0$ 的基础解系含向量个数
$$n-r(BA)\ge n-\min(n-l,n-m)=\max(l,m),$$
所以「恰有 $l$ 个」不成立，① 错。
**② 判 ②。** 由 $l+m>n$ 得
$$r(A\pm B)\le r(A)+r(B)=2n-(l+m)<n,$$
即 $r(A-B)<n$，故 $(A-B)x=0$ 必有非零解，② 正确。
**③ 判 ③。** 由 $Ax=0$ 与 $Bx=0$ 无非零公共解，即 $\begin{pmatrix}A\\B\end{pmatrix}x=0$ 仅有零解，故 $r\begin{pmatrix}A\\B\end{pmatrix}=n$，③ 正确。
**④ 结论。** 正确的有 2 个，故选 (C)。
【思路】用 $r(BA)\le\min\{r(A),r(B)\}$、$r(A\pm B)\le r(A)+r(B)$ 与堆叠矩阵满秩三个工具逐一判断。
【易错】$r(BA)$ 只能给上界，故基础解系向量个数是「至少 $\max(l,m)$」而不是等于；堆叠矩阵 $\begin{pmatrix}A\\B\end{pmatrix}$ 满秩等价于两方程组无非零公共解。
===Q9===
【答案】D
【解】
**① 定 $r(B)$。** 由 $AB=O$ 得 $r(A)+r(B)\le3$；$A$ 含非零二阶子式 $\begin{vmatrix}1&3\\-4&0\end{vmatrix}$，故 $r(A)\ge2$，从而 $r(B)\le1$。又 $B\ne O$ 得 $r(B)=1$，即 $B$ 各行（列）成比例。
**② 写出 $B$ 的形式。** 由 $B$ 每行元素之和为 $3$ 有 $B\begin{pmatrix}1\\1\\1\end{pmatrix}=3\begin{pmatrix}1\\1\\1\end{pmatrix}$，即 $3$ 是 $B$ 的特征值、$\begin{pmatrix}1\\1\\1\end{pmatrix}$ 为对应特征向量。设
$$B=\begin{pmatrix}k\\k\\k\end{pmatrix}(a_1,a_2,a_3)=\begin{pmatrix}ka_1&ka_2&ka_3\\ka_1&ka_2&ka_3\\ka_1&ka_2&ka_3\end{pmatrix},\quad k(a_1+a_2+a_3)=3.$$
**③ 用实对称性定出 $B$。** $B$ 实对称得 $a_1=a_2=a_3$，结合 $k(a_1+a_2+a_3)=3$ 得 $ka_1=1$，故
$$B=\begin{pmatrix}1&1&1\\1&1&1\\1&1&1\end{pmatrix}=\begin{pmatrix}1\\1\\1\end{pmatrix}(1,1,1).$$
**④ 计算二次型。** 当 $x=(1,-1,2)^T$ 时，
$$x^TBx=(1,-1,2)\begin{pmatrix}1\\1\\1\end{pmatrix}(1,1,1)\begin{pmatrix}1\\-1\\2\end{pmatrix}=2\times2=4,$$
故选 (D)。
【思路】由 $AB=O$ 与 $A$ 的二阶子式锁定 $r(B)=1$，再用「行和为 3」与实对称性把 $B$ 写成秩 1 矩阵 $\mathbf{1}\mathbf{1}^T$。
【易错】$B$ 的每行和为 $3$ 给出的是特征值 $3$ 与特征向量 $(1,1,1)^T$，不是 $B=3E$；$x^TBx=(\mathbf{1}^Tx)^2$，其中 $\mathbf{1}^Tx=1-1+2=2$，故为 $4$。
===Q10===
【答案】A
【解】
**① 由 $AB=2B$ 定秩。** $(A-2E)B=O$ 给出 $r(A-2E)+r(B)\le3$；由 $B^*\ne O$ 得 $r(B^*)\ge1$，即 $r(B)\ge2$，故 $r(A-2E)\le1$。
**② 排除 $A=2E$。** 若 $r(A-2E)=0$ 则 $A=2E$，此时 $|A|=8\ne4$，舍去；故 $r(A-2E)=1$。
**③ 定 $A$ 的特征值。** $(A-2E)x=0$ 的基础解系含 2 个线性无关解，故 $\lambda=2$ 至少是 $A$ 的二重特征值；由 $|A|=4$ 得第三个特征值 $\lambda_3=\frac{4}{2\times2}=1$。
**④ 算行列式。** $A^{-1}$ 的特征值为 $\frac12,\frac12,1$，$A^{-1}+2E$ 的特征值为 $\frac52,\frac52,3$，故
$$|A^{-1}+2E|=\frac52\cdot\frac52\cdot3=\frac{75}{4},$$
故选 (A)。
【思路】把矩阵方程转成秩不等式定出 $\lambda=2$ 的重数，再由行列式补出第三个特征值，最后用特征值的平移与取倒数算行列式。
【易错】$B^*\ne O$ 只保证 $r(B)\ge n-1=2$，故只能得 $r(A-2E)\le1$；必须回代 $|A|=4$ 排除 $A=2E$，否则 $\lambda_3$ 无从确定。
===Q11===
【答案】$\frac{1}{24}$
【解】
**① 建面积函数。** 设 $A(x_0,\sin x_0)$，直线 $OA:y=\frac{\sin x_0}{x_0}x$，所围面积
$$S=\int_0^{x_0}\left(\sin x-\frac{\sin x_0}{x_0}x\right)dx=1-\cos x_0-\frac12x_0\sin x_0,$$
记 $S(x)=1-\cos x-\frac12x\sin x$。
**② 泰勒展开。** $1-\cos x=\frac12x^2-\frac1{24}x^4+o(x^4)$，$\frac12x\sin x=\frac12x\left(x-\frac16x^3+o(x^3)\right)=\frac12x^2-\frac1{12}x^4+o(x^4)$。
**③ 求极限。**
$$\lim_{x\to0^+}\frac{S(x)}{x^4}=\lim_{x\to0^+}\frac{\left(\frac12x^2-\frac1{24}x^4\right)-\left(\frac12x^2-\frac1{12}x^4\right)+o(x^4)}{x^4}=\frac1{24}.$$
【思路】先把面积写成 $x_0$ 的函数，再用 $\sin x,\cos x$ 的四阶泰勒展开消去 $x^2$ 项，读出 $x^4$ 系数。
【易错】$\cos x$ 与 $x\sin x$ 都必须展到 $x^4$（只到 $x^2$ 会得到 $0$）；$\frac1{12}-\frac1{24}=\frac1{24}$，符号别反。
===Q12===
【答案】$\dfrac{y(u-2v)-6x}{u+v}$
【解】
**① 建立目标。** 由 $z=u+2v$ 得 $\frac{\partial z}{\partial x}=\frac{\partial u}{\partial x}+2\frac{\partial v}{\partial x}$。
**② 方程组对 $x$ 求偏导。** 对 $\begin{cases}xy-u+v=0,\\x^2+3y+uv=1\end{cases}$ 求偏导：
$$\begin{cases}y-\dfrac{\partial u}{\partial x}+\dfrac{\partial v}{\partial x}=0,\\[4pt]2x+v\dfrac{\partial u}{\partial x}+u\dfrac{\partial v}{\partial x}=0.\end{cases}$$
**③ 解线性方程组。** 由第一式 $\frac{\partial v}{\partial x}=\frac{\partial u}{\partial x}-y$ 代入第二式，解得
$$\frac{\partial u}{\partial x}=\frac{yu-2x}{u+v},\qquad\frac{\partial v}{\partial x}=-\frac{2x+yv}{u+v}.$$
**④ 合并。**
$$\frac{\partial z}{\partial x}=\frac{yu-2x}{u+v}-2\cdot\frac{2x+yv}{u+v}=\frac{y(u-2v)-6x}{u+v}.$$
【思路】把 $u,v$ 视为 $x,y$ 的隐函数，对方程组求偏导解出两个偏导，再按 $z=u+2v$ 线性组合。
【易错】$y$ 为自变量、求偏导时视为常数，第一式是 $y-\frac{\partial u}{\partial x}+\frac{\partial v}{\partial x}=0$；分母 $u+v\ne0$ 是方程组可解的条件。
===Q13===
【答案】$y=x+3$
【解】
**① 求 $k$。**
$$k=\lim_{x\to+\infty}\frac{f(x)}x=\lim_{x\to+\infty}\frac{(x^2+3x+1)\ln x}{x^2\ln(x+1)}=\lim_{x\to+\infty}\frac{x^2+3x+1}{x^2}\cdot\lim_{x\to+\infty}\frac{\ln x}{\ln(x+1)}=1.$$
**② 求 $b$。**
$$b=\lim_{x\to+\infty}[f(x)-kx]=\lim_{x\to+\infty}\frac{(x^2+3x+1)\ln x-x^2\ln(x+1)}{x\ln(x+1)}$$
$$=\lim_{x\to+\infty}\frac{x^2\ln\frac{x}{x+1}+(3x+1)\ln x}{x\ln(x+1)}=\lim_{x\to+\infty}\frac{x\ln\frac{x}{x+1}}{\ln(x+1)}+\lim_{x\to+\infty}\frac{3x+1}{x}\cdot\lim_{x\to+\infty}\frac{\ln x}{\ln(x+1)}.$$
**③ 定值。** $\ln\frac{x}{x+1}\sim-\frac1{x+1}$ 使第一项分子 $\to-1$、分母 $\to+\infty$，故第一项为 $0$；第二项 $=3\times1=3$，得 $b=3$。
**④ 结论。** 斜渐近线为 $y=x+3$。
【思路】按 $k=\lim\frac{f(x)}x,\ b=\lim[f(x)-kx]$ 两步求斜渐近线，分子拆成 $x^2\ln\frac{x}{x+1}$ 与 $(3x+1)\ln x$ 两部分。
【易错】$\frac{x\ln\frac{x}{x+1}}{\ln(x+1)}\to0$（分子有界、分母发散），不能把 $\ln\frac{x}{x+1}\sim-\frac1{x+1}$ 代入后误算成 $-1$ 与 $3$ 相加得 $2$。
===Q14===
【答案】$f(x)=x^2$
【解】
**① 由已知极限读出 $f(0),f'(0),f''(0)$。** 因 $x-\tan x\sim-\frac{x^3}3$，
$$0=\lim_{x\to0}\frac{xf(x)-\ln(1+x^3)}{x-\tan x}=-3\lim_{x\to0}\frac{xf(x)-\ln(1+x^3)}{x^3}=-3\lim_{x\to0}\frac{f(x)}{x^2}+3,$$
故 $\lim\limits_{x\to0}\frac{f(x)}{x^2}=1$。由泰勒公式 $f(x)=f(0)+f'(0)x+\frac12f''(0)x^2+o(x^2)$ 得 $f(0)=f'(0)=0,\ f''(0)=2$。
**② 用题干条件求导。** 由 $f(x+y)=f(x)+f(y)+\frac12yf'(x)+\frac12xf'(y)$ 得
$$f'(x)=\lim_{y\to0}\frac{f(x+y)-f(x)}y=\lim_{y\to0}\frac{f(y)+\frac12yf'(x)+\frac12xf'(y)}y=f'(0)+\frac12f'(x)+\frac12xf''(0).$$
**③ 解出 $f$。** 代入 $f'(0)=0,\ f''(0)=2$ 得 $f'(x)=\frac12f'(x)+x$，即 $f'(x)=2x$，$f(x)=x^2+C$；由 $f(0)=0$ 得 $C=0$，故 $f(x)=x^2$。
【思路】先用等价无穷小与泰勒展开从极限读出 $f(0),f'(0),f''(0)$，再把函数方程对 $y$ 取极限凑出 $f'(x)$ 的代数方程。
【易错】$x-\tan x\sim-\frac{x^3}3$ 与 $\ln(1+x^3)\sim x^3$ 配套，若分母误作 $x^3$ 会把 $\lim\frac{f}{x^2}$ 算成 $0$；$\frac{f'(y)-f'(0)}y\to f''(0)=2$ 是得到 $f'(x)=2x$ 的关键。
===Q15===
【答案】$\frac83\pi$
【解】
**① 取微元。** 任取 $y\in[0,2]$，薄层体积 $dV=\pi x^2dy=2\pi ydy$（容器由 $y=\frac{x^2}2$ 旋转而成），取 $\rho g=1$ 得 $dG=2\pi ydy$。
**② 微元功。** 把该薄层从顶部 $y=2$ 抽出需提升 $2-y$，故
$$dW=(2-y)dG=2\pi y(2-y)dy.$$
**③ 积分。**
$$W=\int_0^22\pi y(2-y)dy=2\pi\left[y^2-\frac{y^3}3\right]_0^2=\frac83\pi.$$
【思路】用柱壳微元写出体积与重力，乘提升高度 $2-y$ 后对 $y$ 从 $0$ 到 $2$ 积分。
【易错】提升距离是 $2-y$（容器高为 $2$）而不是 $y$；$x^2=2y$ 使 $dV=\pi x^2dy=2\pi ydy$，别漏 $\pi$。
===Q16===
【答案】$\begin{pmatrix}1&0&0\\0&1&0\\0&0&-\frac23\end{pmatrix}$
【解】
**① 化简题干方程。** 两边右乘 $A$ 得 $BA-2A=2|A|E-B$；由 $|A|=\frac12$ 得 $BA-2A=E-B$，恒等变形为
$$(2E-B)(A+E)=E.$$
由可逆阵定义还有 $(A+E)(2E-B)=E$，故 $BA=AB$，且 $2E-B=(A+E)^{-1}$。
**② 表达待求矩阵。** 待求矩阵 $=2BA-BA-2A=BA-2A=(B-2E)A=-(2E-B)A=-(A+E)^{-1}A$。
**③ 代入对角阵。** 由 $(A+E)^{-1}=\begin{pmatrix}\frac12&0&0\\0&\frac12&0\\0&0&3\end{pmatrix}^{-1}=\begin{pmatrix}2&0&0\\0&2&0\\0&0&\frac13\end{pmatrix}$，且 $A=(A+E)-E=\begin{pmatrix}-\frac12&0&0\\0&-\frac12&0\\0&0&2\end{pmatrix}$，得
$$-(A+E)^{-1}A=-\begin{pmatrix}2&0&0\\0&2&0\\0&0&\frac13\end{pmatrix}\begin{pmatrix}-\frac12&0&0\\0&-\frac12&0\\0&0&2\end{pmatrix}=\begin{pmatrix}1&0&0\\0&1&0\\0&0&-\frac23\end{pmatrix}.$$
【思路】先把矩阵方程凑成 $(2E-B)(A+E)=E$ 得到 $2E-B=(A+E)^{-1}$，再利用对角阵直接相乘。
【易错】$-(A+E)^{-1}A=(A+E)^{-1}-E$，若把减号后的 $A$ 误作 $E$ 之外的量会算错对角元；$A$ 的第三个对角元是 $2$，与 $(A+E)^{-1}$ 的 $\frac13$ 相乘才得 $-\frac23$。
===Q17===
【答案】（I）$a=2$；（II）$\varphi'(x)$ 在 $x=0$ 处连续
【解】
**（I）由可导定 $a$。** $f$ 在 $x=0$ 可导必连续，$f(0)=\lim\limits_{x\to0^-}a\ln(1-ax)=0$，且
$$\lim_{x\to0^+}f(x)=\lim_{x\to0^+}(a-6)\sin x+\lim_{x\to0^+}x^a\cos\frac1x,$$
当 $a>0$ 时后项 $\to0$，故 $f$ 在 $x=0$ 连续。由左右导数：
$$f'_-(0)=\lim_{x\to0^-}\frac{a\ln(1-ax)}x=-a^2,$$
$$f'_+(0)=\lim_{x\to0^+}\frac{(a-6)\sin x}x+\lim_{x\to0^+}\frac{x^a\cos\frac1x}x=a-6+\lim_{x\to0^+}x^{a-1}\cos\frac1x,$$
当 $a-1>0$ 时末项 $\to0$，得 $f'_+(0)=a-6$。令 $-a^2=a-6$ 解得 $a=2$（$a=-3$ 不满足 $a>1$，舍去）。
**（II）证 $\varphi'$ 在 $0$ 连续。** $\varphi(x)=f(x)(e^x-1)$，$\varphi(0)=0$，由导数定义
$$\varphi'(0)=\lim_{x\to0}\frac{f(x)(e^x-1)}x=\lim_{x\to0}f(x)=f(0)=0.$$
当 $x\ne0$ 时 $\varphi'(x)=f'(x)(e^x-1)+f(x)e^x$。取 $a=2$：$x>0$ 时 $f(x)=-4\sin x+x^2\cos\frac1x$，$f'(x)=-4\cos x+2x\cos\frac1x+\sin\frac1x$ 有界，故
$$\lim_{x\to0^+}\varphi'(x)=\lim_{x\to0^+}f'(x)(e^x-1)+f(0)=0;$$
$x<0$ 时 $f(x)=2\ln(1-2x),\ f'(x)=\frac{-4}{1-2x}\to-4$，
$$\lim_{x\to0^-}\varphi'(x)=\lim_{x\to0^-}\left[\frac{-4}{1-2x}(e^x-1)+2\ln(1-2x)e^x\right]=0.$$
左右极限均等于 $\varphi'(0)=0$，故 $\varphi'$ 在 $x=0$ 处连续。
【思路】(I) 用连续性与左右导数相等解出 $a$；(II) 先由导数定义算 $\varphi'(0)$，再用 $f'$ 有界与 $e^x-1\sim x$ 证 $\lim\varphi'=\varphi'(0)$。
【易错】$f'_+(0)$ 存在需要 $a>1$（使 $x^{a-1}\cos\frac1x\to0$），这正是舍去 $a=-3$ 的理由；$\varphi'(0)$ 必须单独用定义求，不能把 $\varphi'(x)$ 的表达式直接代入 $x=0$。
===Q18===
【答案】（I）$f(x)=e^{-2x}+(x-1)e^{-x}$；（II）$V=(\sqrt2-1)\pi^{\frac32}$
【解】
**（I）化积分方程为微分方程。** 令 $x-t=u$：
$$\int_0^x[3f'(x-t)+2f(x-t)]dt=x\int_0^x[3f'(u)+2f(u)]du-\int_0^xu[3f'(u)+2f(u)]du.$$
题干方程两边对 $x$ 求导得 $f'(x)=-e^{-x}-\int_0^x[3f'(u)+2f(u)]du$，再求导得
$$f''(x)=e^{-x}-[3f'(x)+2f(x)],\quad\text{即}\quad f''+3f'+2f=e^{-x}.$$
特征方程 $r^2+3r+2=0$ 有根 $-2,-1$，齐次通解 $C_1e^{-2x}+C_2e^{-x}$；因 $-1$ 是单根设特解 $Axe^{-x}$，代入得 $A=1$，故
$$f(x)=C_1e^{-2x}+C_2e^{-x}+xe^{-x}.$$
由 $\lim\limits_{x\to0}\frac{f(x)}x=0$ 展开 $f(x)=C_1(1-2x)+C_2(1-x)+x(1-x)+o(x)$，得
$$\begin{cases}C_1+C_2=0,\\1-2C_1-C_2=0,\end{cases}\Rightarrow\begin{cases}C_1=1,\\C_2=-1,\end{cases}$$
即 $f(x)=e^{-2x}+(x-1)e^{-x}$。
**（II）算旋转体体积。** $f(x)=e^{-x}(e^{-x}+x-1)$，由 $e^{-x}>1-x\ (x>0)$ 得 $f(x)>0$，故
$$V=\int_0^{+\infty}2\pi x\cdot\frac{f(x)}{x^{\frac32}}dx=2\pi\int_0^{+\infty}\frac{e^{-2x}+(x-1)e^{-x}}{\sqrt x}dx.$$
其中
$$\int_0^{+\infty}\frac{e^{-2x}}{\sqrt x}dx\xlongequal{2x=t}\frac1{\sqrt2}\int_0^{+\infty}\frac{e^{-t}}{\sqrt t}dt=\frac1{\sqrt2}\Gamma\left(\frac12\right)=\sqrt{\frac\pi2},$$
$$\int_0^{+\infty}\sqrt x e^{-x}dx=\Gamma\left(\frac32\right)=\frac12\Gamma\left(\frac12\right)=\frac{\sqrt\pi}2,\qquad\int_0^{+\infty}\frac{e^{-x}}{\sqrt x}dx=\Gamma\left(\frac12\right)=\sqrt\pi.$$
故
$$V=2\pi\left(\sqrt{\frac\pi2}+\frac{\sqrt\pi}2-\sqrt\pi\right)=(\sqrt2-1)\pi^{\frac32}.$$
【思路】(I) 把含 $x-t$ 的积分方程两次求导化为二阶常系数方程，用特征根法与 $\lim\frac{f(x)}x=0$ 定常数；(II) 用柱壳法列出反常积分，拆成三个 $\Gamma$ 函数值。
【易错】$-1$ 是特征单根，特解须设 $Axe^{-x}$ 而非 $Ae^{-x}$；$\Gamma(\frac12)=\sqrt\pi,\ \Gamma(\frac32)=\frac{\sqrt\pi}2$，合并 $\sqrt{\frac\pi2}+\frac{\sqrt\pi}2-\sqrt\pi$ 时整体因子 $2\pi$ 别漏。
===Q19===
【答案】最大值为 $\frac12$，最小值为 $-\frac12$
【解】
**① 拉格朗日函数与驻点方程。** 设 $L=ax^3-yz+\lambda(x^2+y^2+z^2-1)$，
$$\begin{cases}L'_x=3ax^2+2\lambda x=0 & ①\\L'_y=-z+2\lambda y=0 & ②\\L'_z=-y+2\lambda z=0 & ③\\L'_\lambda=x^2+y^2+z^2-1=0 & ④\end{cases}$$
由 ②$-$③ 得 $(y-z)(1+2\lambda)=0$，故 $z=y$ 或 $\lambda=-\frac12$。
**② 分支 $\lambda=-\frac12$。** 代入 ② 得 $z=-y$，代入 ① 得 $x(3ax-1)=0$。当 $a=0$ 时 $x=0$，由 ④ 得 $y=\pm\frac{\sqrt2}2$，驻点 $\left(0,\pm\frac{\sqrt2}2,\mp\frac{\sqrt2}2\right)$；当 $a\ne0$ 时 $x=\frac1{3a}$，由 $|a|<\frac13$ 得 $|x|>1$，不满足 ④，舍去。
**③ 分支 $z=y$。** 代入 ③ 得 $z=0$ 或 $\lambda=\frac12$。$z=y=0$ 时由 ④ 得 $x=\pm1$，驻点 $(\pm1,0,0)$；$\lambda=\frac12$ 时 ① 给出 $x(3ax+1)=0$，$a=0$ 得驻点 $\left(0,\pm\frac{\sqrt2}2,\pm\frac{\sqrt2}2\right)$，$a\ne0$ 时 $x=-\frac1{3a}$ 同样因 $|x|>1$ 舍去。
**④ 比较函数值。**
$$u\left(0,\pm\frac{\sqrt2}2,\mp\frac{\sqrt2}2\right)=\frac12,\quad u(1,0,0)=a,\quad u(-1,0,0)=-a,\quad u\left(0,\pm\frac{\sqrt2}2,\pm\frac{\sqrt2}2\right)=-\frac12.$$
由 $|a|<\frac13$ 知 $\pm a\in\left(-\frac13,\frac13\right)$，故最大值为 $\frac12$，最小值为 $-\frac12$。
【思路】用拉格朗日乘数法按 $z=y$ 与 $\lambda=-\frac12$ 分支列出全部驻点，逐一算 $u=ax^3-yz$ 比较。
【易错】两组驻点 $\left(0,\pm\frac{\sqrt2}2,\mp\frac{\sqrt2}2\right)$ 与 $\left(0,\pm\frac{\sqrt2}2,\pm\frac{\sqrt2}2\right)$ 的第三分量符号相反，分别对应 $u=\frac12$ 与 $u=-\frac12$；$|a|<\frac13$ 保证 $u=\pm a$ 不是最值。
===Q20===
【答案】$I=7\sqrt2\pi+32\pi+2\sqrt2\ln(1+\sqrt2)-76$
【解】
**① 分域写出被积函数。** 曲线 $C_1:2x^2-4x=y^2$，$C_2:x=4-\sqrt{16-y^2}$；$D_1$ 为 $C_1$ 与 $x=4$ 所围区域，$D_2$ 为 $C_1,C_2$ 所围区域，$D=D_1+D_2$，
$$f(x,y)=\begin{cases}\dfrac{x}{\sqrt{4x-x^2}}, & (x,y)\in D_1,\\[6pt] x(y+1), & (x,y)\in D_2.\end{cases}$$
**② 算 $D_1$ 上的积分。**
$$\iint_{D_1}\frac{x}{\sqrt{4x-x^2}}dxdy=2\int_2^4dx\int_0^{\sqrt{2x^2-4x}}\frac{x}{\sqrt{4x-x^2}}dy=2\sqrt2\int_2^4x\sqrt{\frac{x-2}{4-x}}dx.$$
令 $u=x-2$、再令 $u=2-v^2$、最后 $v=\sqrt2\sin\theta$，得
$$2\sqrt2\int_0^2(u+2)\sqrt{\frac{u}{2-u}}du=4\sqrt2\int_0^{\sqrt2}(4-v^2)\sqrt{2-v^2}dv=16\sqrt2\int_0^{\frac\pi2}(1+\cos^2\theta)\cos^2\theta\,d\theta=7\sqrt2\pi.$$
**③ 算 $D_2$ 上的积分。** 由对称性 $\iint_{D_2}x(y+1)dxdy=\iint_{D_2}x\,dxdy$，且
$$\iint_{D_2}x\,dxdy=2\left(\int_0^4dx\int_0^{\sqrt{8x-x^2}}xdy-\int_2^4dx\int_0^{\sqrt{2x^2-4x}}xdy\right).$$
其中 $\int_0^4x\sqrt{8x-x^2}dx\xlongequal{x-4=u}\int_{-4}^0(u+4)\sqrt{16-u^2}du=16\pi-\frac{64}{3}$；$\int_2^4x\sqrt{2x^2-4x}dx=\sqrt2\int_2^4x\sqrt{(x-1)^2-1}dx=\frac{50}{3}-\sqrt2\ln(1+\sqrt2)$。
故该部分 $=32\pi-76+2\sqrt2\ln(1+\sqrt2)$。
**④ 合并。** $I=7\sqrt2\pi+32\pi+2\sqrt2\ln(1+\sqrt2)-76$。
【思路】按 $D_1,D_2$ 拆分被积函数，$D_1$ 用三角换元算无理积分，$D_2$ 用奇偶对称消去 $y$ 后化为两个二次积分之差。
【易错】$D_1$ 的 $y$ 上限是 $\sqrt{2x^2-4x}$（$C_1$），$D_2$ 中圆弧对应上限是 $\sqrt{8x-x^2}$（$C_2$），两者不可互换；$\int_0^{\frac\pi2}(1+\cos^2\theta)\cos^2\theta d\theta=\frac{7\pi}{16}$，别漏 $\cos^4\theta$ 的 $\frac{3\pi}{16}$。
===Q21===
【答案】（I）存在唯一 $c\in(0,a)$ 使 $\int_0^c\frac{1}{g(x)}dx=\int_c^ag(x)dx$；（II）$\lim\limits_{n\to\infty}x_n=c$
【解】
**（I）构造 $G$ 用零点定理与单调性。** 设 $g(x)<0$（由题设）。令 $G(x)=\int_0^x\frac1{g(t)}dt-\int_x^ag(t)dt$，则 $G$ 在 $[0,a]$ 可导，且
$$G(0)=-\int_0^ag(t)dt>0,\qquad G(a)=\int_0^a\frac1{g(t)}dt<0.$$
由零点定理存在 $c\in(0,a)$ 使 $G(c)=0$；又 $G'(x)=\frac1{g(x)}+g(x)<0$，$G$ 严格单调递减，故零点唯一，即 $\int_0^c\frac1{g(x)}dx=\int_c^ag(x)dx$。
**（II）证数列收敛于 $c$。** 记 $H_n(x)=\int_{\frac1n}^x\frac1{g(t)}dt-\int_x^ag(t)dt$，$x_n$ 为其零点。因
$$H_n\left(\frac1n\right)=-\int_{\frac1n}^ag(t)dt>0,\quad H_n(a)=\int_{\frac1n}^a\frac1{g(t)}dt<0,\quad H'_n(x)=\frac1{g(x)}+g(x)<0,$$
故 $H_n$ 在 $\left(\frac1n,a\right)$ 内恰有一个零点，即 $0<\frac1n<x_n<a$，$\{x_n\}$ 有界。又
$$H_n(x)-H_{n+1}(x)=\int_{\frac1n}^{\frac1{n+1}}\frac1{g(t)}dt>0\Rightarrow H_{n+1}(x_n)<H_n(x_n)=0=H_{n+1}(x_{n+1}),$$
由 $H_{n+1}$ 单调递减得 $x_{n+1}<x_n$，故 $\{x_n\}$ 单调递减有下界，从而收敛。设 $\lim x_n=b$，对 $H_n(x_n)=0$ 两边取极限：
$$\lim_{n\to\infty}\int_{\frac1n}^{x_n}\frac1{g(t)}dt=\lim_{n\to\infty}\int_{x_n}^ag(t)dt\Rightarrow\int_0^b\frac1{g(t)}dt=\int_b^ag(t)dt,$$
即 $G(b)=0$；由 (I) 零点唯一得 $b=c$，故 $\lim\limits_{n\to\infty}x_n=c$。
【思路】(I) 用零点定理加严格单调性证存在唯一 $c$；(II) 用 $H_n$ 的零点给出 $x_n$ 的有界与单调，再对积分等式取极限并借唯一性定出极限为 $c$。
【易错】$g<0$ 时 $\frac1g+g<0$ 是单调性的来源，且 $\int_{1/n}^{1/(n+1)}\frac1g\,dt>0$（负函数、上限小于下限）；取极限须同时让下限 $\frac1n\to0$ 与 $x_n\to b$，二者不可分开处理。
===Q22===
【答案】（I）二次型矩阵为 $A^*=\begin{pmatrix}A_{11}&A_{21}&A_{31}\\A_{12}&A_{22}&A_{32}\\A_{13}&A_{23}&A_{33}\end{pmatrix}$；（II）$P=\begin{pmatrix}\frac1{\sqrt2}&\frac1{\sqrt6}&\frac1{\sqrt3}\\0&-\frac2{\sqrt6}&\frac1{\sqrt3}\\-\frac1{\sqrt2}&\frac1{\sqrt6}&\frac1{\sqrt3}\end{pmatrix}$，$\Lambda=\begin{pmatrix}-3&0&0\\0&-3&0\\0&0&-\frac{24}{5}\end{pmatrix}$
【解】
**（I）按第一行展开并写成二次型。**
$$f(x_1,x_2,x_3)=x_1\begin{vmatrix}x_1&a_{12}&a_{13}\\x_2&a_{22}&a_{23}\\x_3&a_{32}&a_{33}\end{vmatrix}-x_2\begin{vmatrix}x_1&a_{11}&a_{13}\\x_2&a_{21}&a_{23}\\x_3&a_{31}&a_{33}\end{vmatrix}+x_3\begin{vmatrix}x_1&a_{11}&a_{12}\\x_2&a_{21}&a_{22}\\x_3&a_{31}&a_{32}\end{vmatrix}$$
$$=x_1(x_1A_{11}+x_2A_{21}+x_3A_{31})+x_2(x_1A_{12}+x_2A_{22}+x_3A_{32})+x_3(x_1A_{13}+x_2A_{23}+x_3A_{33})$$
$$=(x_1,x_2,x_3)\begin{pmatrix}A_{11}&A_{21}&A_{31}\\A_{12}&A_{22}&A_{32}\\A_{13}&A_{23}&A_{33}\end{pmatrix}\begin{pmatrix}x_1\\x_2\\x_3\end{pmatrix}=x^TA^*x,$$
故二次型矩阵为 $A^*$（即 $A$ 的伴随矩阵）。
**（II）求 $A,B$ 的特征值与正交矩阵。** 由 $A^*$ 的特征值 $1,1,4$ 及 $|A^*|=|A|^2=4,\ |A|>0$ 得 $|A|=2$，$A$ 的特征值 $\lambda_1=\lambda_2=2,\ \lambda_3=\frac12$。由 $A$ 各行元素之和为 $a<1$ 得 $A\begin{pmatrix}1\\1\\1\end{pmatrix}=a\begin{pmatrix}1\\1\\1\end{pmatrix}$，故 $a=\lambda_3=\frac12$，对应特征向量 $\gamma=\begin{pmatrix}1\\1\\1\end{pmatrix}$。
由 $\left[\left(\frac12A\right)^*\right]^{-1}=\frac{\frac12A}{\left|\frac12A\right|}=2A$，题干方程化为 $ABA=3AB+6E$，解得
$$B=6A^{-1}(A-3E)^{-1}=6(A^2-3A)^{-1},$$
故 $B$ 的特征值 $\mu=\frac{6}{\lambda^2-3\lambda}$：$\mu_1=\mu_2=-3,\ \mu_3=-\frac{24}{5}$。
$\lambda=2$ 的特征向量满足 $x_1+x_2+x_3=0$，取已正交的 $\gamma_1=\begin{pmatrix}1\\0\\-1\end{pmatrix},\ \gamma_2=\begin{pmatrix}1\\-2\\1\end{pmatrix}$；单位化得
$$\beta_1=\frac1{\sqrt2}\begin{pmatrix}1\\0\\-1\end{pmatrix},\quad\beta_2=\frac1{\sqrt6}\begin{pmatrix}1\\-2\\1\end{pmatrix},\quad\beta_3=\frac1{\sqrt3}\begin{pmatrix}1\\1\\1\end{pmatrix}.$$
令 $P=(\beta_1,\beta_2,\beta_3)$，则 $P$ 为正交矩阵且 $P^TBP=\Lambda=\mathrm{diag}\left(-3,-3,-\frac{24}{5}\right)$。
【思路】(I) 用代数余子式把行列式写成 $x^TA^*x$；(II) 由伴随矩阵与特征值关系定出 $A$ 的谱，借 $\left[(kA)^*\right]^{-1}$ 化简方程求 $B$ 的谱，最后把特征向量正交单位化。
【易错】$A^*$ 的元素是 $(A^*)_{ij}=A_{ji}$（代数余子式转置），二次型矩阵别写成余子式矩阵本身；$B$ 的特征值须用 $\frac{6}{\lambda^2-3\lambda}$ 逐一代入，$P$ 的列顺序须与 $\Lambda$ 的 $-3,-3,-\frac{24}{5}$ 对应。
