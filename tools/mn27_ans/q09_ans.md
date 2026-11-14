===Q1===
【答案】D
【解】
**① 求 $f'(0)$。** 记 $g(t)=\dfrac{\ln(1+t^2)}{1+\int_0^te^{-s^2}ds}$，它在 $t=0$ 处连续，故 $f(x)=\int_0^xg(t)dt$ 在 $x=0$ 处可导，且
$$f'(0)=\left.\frac{\ln(1+x^2)}{1+\int_0^xe^{-s^2}ds}\right|_{x=0}=0,$$
由此排除 (A)、(B)。
**② 判 $f'(x)$ 的符号。** 当 $x\in(0,\delta)$ 或 $x\in(-\delta,0)$ 时分子 $\ln(1+x^2)>0$、分母 $1+\int_0^xe^{-s^2}ds>0$，故 $f'(x)=\dfrac{\ln(1+x^2)}{1+\int_0^xe^{-s^2}ds}>0$，即 $f$ 在 $0$ 两侧均单调递增。
**③ 结论。** 于是 $x\in(0,\delta)$ 时 $f(x)>0=f(0)$，$x\in(-\delta,0)$ 时 $f(x)<0=f(0)$，故 $x=0$ 不是 $f(x)$ 的极值点，选 (D)。
【思路】用变限积分求导得 $f'(0)=0$ 排除 (A)(B)，再由两侧 $f'>0$ 判定 $x=0$ 非极值点。
【易错】$f'(0)=0$ 只说明是驻点，极值要看两侧 $f(x)$ 与 $f(0)$ 的大小；$f'(x)>0$ 在 $x=0$ 两侧同时成立时函数单调递增穿过零点，不是极值。
===Q2===
【答案】B
【解】
**① 求原点处偏导数。** 由 $f(x,0)=f(0,y)=0$，按定义
$$f'_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=0,\qquad f'_y(0,0)=0,$$
故命题 ② 正确。
**② 验证可微性。** 
$$\lim_{\substack{x\to0\\y\to0}}\frac{f(x,y)-f'_x(0,0)x-f'_y(0,0)y-f(0,0)}{\sqrt{x^2+y^2}}=\lim_{\substack{x\to0\\y\to0}}\frac{(x^2+y^2)\sin\frac1{xy}}{\sqrt{x^2+y^2}}=\lim_{\substack{x\to0\\y\to0}}\sqrt{x^2+y^2}\sin\frac1{xy}=0,$$
故 $f$ 在 $(0,0)$ 可微，命题 ① 正确。
**③ 排除 ③。** 当 $xy\ne0$ 时 $f'_x(x,y)=2x\sin\dfrac1{xy}-\dfrac{x^2+y^2}{x^2y}\cos\dfrac1{xy}$；在 $x=0,\ y\ne0$ 处按定义的差商 $\dfrac{f(h,y)-f(0,y)}h=\dfrac{h^2+y^2}{h}\sin\dfrac1{hy}$，取 $h=\dfrac1{2k\pi y}$ 时为 0，取 $h=\dfrac{1}{\left(2k\pi+\frac\pi2\right)y}$ 时绝对值趋于无穷大，故 $f'_x(0,y)$ 不存在，③ 错。
**④ 排除 ④。** 沿 $y=x\ne0$ 有 $f'_x(x,x)=2x\sin\dfrac1{x^2}-\dfrac2x\cos\dfrac1{x^2}$；取 $x_k=(2k\pi)^{-\frac12}$，则 $(x_k,x_k)\to(0,0)$ 而 $f'_x(x_k,x_k)=-2\sqrt{2k\pi}\to-\infty$，故 $f'_x$ 在原点不连续，④ 错。
**⑤ 结论。** 正确的只有 ①②，选 (B)。
【思路】按定义算偏导、用可微定义验证 ①，再分别构造差商与路径反例否定 ③、④。
【易错】$f(x,y)=(x^2+y^2)\sin\frac1{xy}$ 在坐标轴上补定义为 0，可微但偏导数并非处处存在；振荡因子 $\sin\frac1{xy}$ 使 $f'_x$ 在原点附近无界、不连续。
===Q3===
【答案】C
【解】
**① 特征根与通解。** 对应齐次方程特征方程 $(r+1)(r+a-1)=0$，根 $r_1=-1,\ r_2=1-a$。当 $a\ne1,2$ 时设特解 $y_p=Ax+B$，代入 $y''+ay'+(a-1)y=x$ 得 $aA+(a-1)(Ax+B)=x$，比较系数得 $(a-1)A=1,\ aA+(a-1)B=0$，即 $A=\dfrac1{a-1},\ B=-\dfrac{a}{(a-1)^2}$，故
$$y=C_1e^{-x}+C_2e^{(1-a)x}+\frac{x}{a-1}-\frac{a}{(a-1)^2}.$$
**② 由斜渐近线定范围。** $x\to+\infty$ 时 $e^{-x}\to0$；要使任一解都有斜渐近线还须 $e^{(1-a)x}\to0$，即 $a>1$。此时渐近线 $y=\dfrac{x}{a-1}-\dfrac{a}{(a-1)^2}$，斜率 $k=\dfrac1{a-1}$，由 $0<k<1$ 得 $a>2$。
**③ 讨论退化情形 $a=1,2$。** $a=1$ 时方程为 $y''+y'=x$，令 $u=y'$ 得 $(e^xu)'=xe^x$，积分两次得 $y=\dfrac12x^2-x+C_1e^{-x}+C_2$，无斜渐近线；$a=2$ 时特征方程有二重根 $-1$，通解 $y=(C_1+C_2x)e^{-x}+x-2$，渐近线 $y=x-2$ 斜率等于 1，也不合题意。
**④ 排除法验证。** 取 $a=1$ 时 $y=\dfrac12x^2-x$ 满足 $y''+y'=1+(x-1)=x$ 是解但无斜渐近线，排除 (A)；取 $a=2$ 时 $y=x-2$ 满足 $y''+2y'+y=0+2+(x-2)=x$ 是解但斜率为 1，排除 (B)、(D)。综上 $a\in(2,+\infty)$，选 (C)。
【思路】按特征根是否与 $-1$ 重合分类求通解，用 $x\to+\infty$ 的渐近线斜率 $0<k<1$ 定出 $a>2$。
【易错】$a=1,2$ 时特解形式退化，必须单独讨论；「任一解都有斜渐近线」要求齐次部分 $e^{(1-a)x}\to0$，不能只看一个特解。
===Q4===
【答案】A
【解】
**① 用柯西中值定理证 (A)。** 固定 $x_0\in(0,1)$，为利用 $|f'(x)|<\dfrac M{\sqrt x}$，对 $f(t)$ 与 $\sqrt t$ 在 $x$ 与 $x_0$ 之间用柯西中值定理：
$$\left|\frac{f(x)-f(x_0)}{\sqrt x-\sqrt{x_0}}\right|=\left|2\sqrt\xi\,f'(\xi)\right|<2M,$$
其中 $\xi$ 介于 $x$ 与 $x_0$ 之间。于是 $|f(x)-f(x_0)|\le2M\left|\sqrt x-\sqrt{x_0}\right|\le2M$（$x=x_0$ 时亦成立），由三角不等式 $|f(x)|\le|f(x_0)|+2M$ 对一切 $x\in(0,1)$ 成立，故 $f$ 有界，(A) 正确。
**② 取 $f(x)=\sqrt x$ 排除 (B)。** 此时 $f(x)+f'(x)=\sqrt x+\dfrac1{2\sqrt x}$ 在 $(0,1)$ 上无界，而 $f(x)f'(x)=\dfrac12$ 有界。
**③ 取 $f(x)=x^{\frac13}$ 排除 (C)、(D)。** 此时 $f'(x)=\dfrac13x^{-\frac23}$，$f$ 在 $(0,1)$ 有界而 $f'$ 无界，故 (D) 错；又 $|f'(x)|\sqrt x=\dfrac13x^{-\frac16}\to+\infty\ (x\to0^+)$，不可能存在常数 $M>0$ 使 $|f'(x)|<\dfrac M{\sqrt x}$ 恒成立，故 (C) 错。选 (A)。
【思路】柯西中值定理把 $|f'|$ 的界转化为 $f$ 的界，再用两个幂函数反例排除其余命题。
【易错】柯西中值定理给出 $\dfrac{f(x)-f(x_0)}{\sqrt x-\sqrt{x_0}}=2\sqrt\xi f'(\xi)$，因子 $2\sqrt\xi$ 恰好抵消 $\dfrac1{\sqrt\xi}$；$x=x_0$ 时差商为 0 需单独补上。
===Q5===
【答案】C
【解】
**① 写压力微元。** 椭圆 $\dfrac{x^2}{4}+y^2=1$ 在深度 $x$ 处的水平弦宽为 $2\sqrt{1-\dfrac{x^2}{4}}$，压强 $p=\rho gx$，故
$$dF=p\,dS=\rho gx\cdot2\sqrt{1-\frac{x^2}{4}}\,dx=2\rho gx\sqrt{1-\frac{x^2}{4}}\,dx.$$
**② 三角换元。** 令 $\dfrac x2=\sin\theta\ (0\le\theta\le\dfrac\pi2)$，则 $x=2\sin\theta,\ dx=2\cos\theta d\theta$：
$$F=\int_0^22\rho gx\sqrt{1-\frac{x^2}{4}}dx=\int_0^{\frac\pi2}8\rho g\sin\theta\cos^2\theta\,d\theta=-8\rho g\int_0^{\frac\pi2}\cos^2\theta\,d\cos\theta.$$
**③ 结果。** $F=-8\rho g\cdot\dfrac13\left.\cos^3\theta\right|_0^{\frac\pi2}=\dfrac83\rho g$，选 (C)。
【思路】用微元法把静水总压力写成定积分，再以 $\frac x2=\sin\theta$ 换元化为三角积分。
【易错】水平弦宽是 $2\sqrt{1-\frac{x^2}{4}}$（整条弦），不是 $\sqrt{1-\frac{x^2}{4}}$；换元后 $x=2\sin\theta$ 与 $dx=2\cos\theta d\theta$ 使系数成为 $8\rho g$。
===Q6===
【答案】C
【解】
**① 判 ①。** 由 $x\to0$ 时 $\alpha\sim\beta$ 知 $\dfrac\beta\alpha\to1$，故 $\dfrac{\alpha-\beta}\alpha=1-\dfrac\beta\alpha\to0$，① 正确。
**② 判 ②。** 由 $\dfrac\beta\alpha\to1$ 及 $\alpha+\beta\to0$：
$$\frac{\alpha^2-\beta^2}\alpha=\frac{(\alpha-\beta)(\alpha+\beta)}\alpha=\left(1-\frac\beta\alpha\right)(\alpha+\beta)\to0,$$
② 正确。
**③ 判 ③。** 取 $\alpha=x,\ \beta=x+x^2,\ \gamma=-x$，三者均为无穷小且 $\dfrac\alpha\beta\to1$；但 $\alpha+\gamma=0,\ \beta+\gamma=x^2$，两者之比为 0 不趋于 1，③ 错。
**④ 判 ④。** 因 $\gamma\ne0$，$\dfrac{\alpha\gamma}{\beta\gamma}=\dfrac\alpha\beta\to1$，即 $\alpha\gamma\sim\beta\gamma$，④ 正确。
**⑤ 结论。** 正确的有 ①②④，共 3 个，选 (C)。
【思路】把 $\alpha\sim\beta$ 即 $\frac\beta\alpha\to1$ 代入各命题，用反例 $\alpha+\gamma\equiv0$ 否定 ③。
【易错】$\alpha\sim\beta$ 不保证 $\alpha+\gamma\sim\beta+\gamma$（和可为 0 而失去意义）；原册 ④ 行把 $\dfrac{\alpha\gamma}{\beta\gamma}=\dfrac\alpha\beta$ 的极限印成 $0$，与 $\alpha\sim\beta$ 矛盾，应为 $1$。
===Q7===
【答案】A
【解】
**① 定积分区域。** 区域由 $y=0,\ x=y$ 及圆 $(x-1)^2+y^2=1$ 在第一象限内的圆弧围成。取极坐标 $x=r\cos\theta,\ y=r\sin\theta$，直线 $x=y$ 对应 $\theta=\dfrac\pi4$，圆化为 $r=2\cos\theta$，故
$$0\le\theta\le\frac\pi4,\qquad 0\le r\le2\cos\theta.$$
**② 化被积函数。** $\dfrac{x}{\sqrt{x^2+y^2}}=\cos\theta$，面积微元 $d\sigma=r\,dr\,d\theta$，故
$$I=\int_0^{\frac\pi4}d\theta\int_0^{2\cos\theta}r\cos\theta\,dr=2\int_0^{\frac\pi4}\cos^3\theta\,d\theta.$$
**③ 计算。** 
$$2\int_0^{\frac\pi4}(1-\sin^2\theta)\,d\sin\theta=2\left(\sin\theta-\frac13\sin^3\theta\right)\Big|_0^{\frac\pi4}=2\left(\frac{\sqrt2}{2}-\frac13\cdot\frac12\cdot\frac{\sqrt2}{2}\right)=\frac{5\sqrt2}{6},$$
选 (A)。
【思路】极坐标下用 $r=2\cos\theta$ 定限，把二重积分化为 $\int\cos^3\theta\,d\theta$。
【易错】圆 $(x-1)^2+y^2=1$ 的极坐标方程是 $r=2\cos\theta$（不是 $r=1$）；面积元中的因子 $r$ 不能漏，积 $r$ 后得 $\cos^3\theta$ 而非 $\cos^2\theta$。
===Q8===
【答案】B
【解】
**① 特征多项式。** 二次型矩阵 $A=\begin{pmatrix}1&2&0\\2&a&0\\0&0&b\end{pmatrix}$，
$$|\lambda E-A|=(\lambda-b)\left[(\lambda-1)(\lambda-a)-4\right]=(\lambda-b)\left[\lambda^2-(a+1)\lambda+a-4\right].$$
故 $\lambda_1=b$，另两根满足 $\lambda_2+\lambda_3=a+1,\ \lambda_2\lambda_3=a-4$。
**② 由惯性指数得必要条件。** 正惯性指数为 1、负惯性指数为 2 说明三个特征值一正两负，故 $|A|=\lambda_1\lambda_2\lambda_3=b(a-4)>0$，只有 $a>4,\ b>0$ 或 $a<4,\ b<0$ 两种可能。
**③ 排除一种并定结论。** 若 $a>4,\ b>0$，则 $\lambda_2+\lambda_3>0$ 且 $\lambda_2\lambda_3>0$，$\lambda_2,\lambda_3$ 均为正，加上 $\lambda_1=b>0$ 与正惯性指数 1 矛盾；若 $a<4,\ b<0$，则 $\lambda_1<0$ 而 $\lambda_2\lambda_3<0$，另两根一正一负，恰合题意。故 $a<4,\ b<0$，选 (B)。
【思路】由特征多项式读出 $\lambda_2+\lambda_3$ 与 $\lambda_2\lambda_3$，用「一正两负」的惯性指数定出 $a<4,\ b<0$。
【易错】正惯性指数是正特征值个数，须结合 $|A|=b(a-4)>0$ 与 $\lambda_2\lambda_3=a-4$ 的符号；$a>4,b>0$ 会使三个特征值全为正，与题设矛盾。
===Q9===
【答案】D
【解】
**① 把条件翻译为秩。** I 可由 II 线性表示而 II 不能由 I 线性表示，等价于 $r(\mathrm{I})<r(\mathrm{II})$。
**② 求两组的秩。** 对 I 作列变换 $\alpha_2-2\alpha_1=(0,0,a-4)^T$，故 $a=4$ 时 $r(\mathrm{I})=1$，$a\ne4$ 时 $r(\mathrm{I})=2$；对 II 组成的矩阵作行变换：
$$(\beta_1,\beta_2,\beta_3)=\begin{pmatrix}1&0&1\\0&1&1\\b&c&1\end{pmatrix}\to\begin{pmatrix}1&0&1\\0&1&1\\0&0&1-b-c\end{pmatrix},$$
故 $b+c=1$ 时 $r(\mathrm{II})=2$，$b+c\ne1$ 时 $r(\mathrm{II})=3$。
**③ 检查 I 能否由 II 表示。** 对 $(\beta_1,\beta_2,\beta_3,\alpha_1,\alpha_2)$ 作同样行变换：
$$\begin{pmatrix}1&0&1&\vdots&1&2\\0&1&1&\vdots&1&2\\b&c&1&\vdots&2&a\end{pmatrix}\to\begin{pmatrix}1&0&1&\vdots&1&2\\0&1&1&\vdots&1&2\\0&0&1-b-c&\vdots&2-b-c&a-2b-2c\end{pmatrix}.$$
若 $b+c=1$，表示 $\alpha_1$ 的方程组末行成为 $0=1$ 无解，与题意矛盾，故 $b+c\ne1$。
**④ 结论。** 此时 $r(\mathrm{II})=3$，可表示任意三维向量，故对任意 $a\in\mathbb R$ 都有 II 可表示 I；而 $r(\mathrm{I})\le2$，I 不能表示 II。因此 $a\in\mathbb R,\ b+c\ne1$，选 (D)。选项 (C) 只给出 $a=4$ 时的特例，未包含全部可能取值，故不正确。
【思路】把「可／不可线性表出」翻译成秩的不等式，用初等变换求秩并回代增广矩阵验证。
【易错】必须回代 $b+c\ne1$ 验证 $\alpha_1$ 可解，否则只得到必要条件；$b+c=1$ 时末行 $0=1$ 才是矛盾根源，而 $a$ 可取任意实数。
===Q10===
【答案】D
【解】
**① 伴随矩阵的秩关系。** $r(A)=n$ 时 $r(A^*)=n$；$r(A)=n-1$ 时 $r(A^*)=1$；$r(A)\le n-2$ 时 $A^*=O$。
**② 证必要性。** 若 $r(A)=n$，则 $A^T$ 可逆，$A^Tx=0$ 只有零解，不可能有非零公共解。若 $r(A)=n-1$，则 $r(A^*)=1$，可写 $A^*=\alpha\beta^T$（$\alpha,\beta\ne0$）；由 $A^*A=O$ 得 $A\alpha=0,\ A^T\beta=0$，而 $r(A^T)=n-1$ 故 $A^Tx=0$ 的基础解系可取为 $\beta$。设 $x=\lambda\beta\ (\lambda\ne0)$ 为非零公共解，则
$$A^*Bx=\alpha\beta^TB(\lambda\beta)=\lambda(\beta^TB\beta)\alpha\ne0$$
（$B$ 正定给 $\beta^TB\beta>0$，且 $\lambda\ne0,\ \alpha\ne0$），与 $A^*Bx=0$ 矛盾，故 $r(A)\le n-2$。
**③ 证充分性。** 若 $r(A)\le n-2$，则 $A^*=O$，$A^*Bx=0$ 对任意 $x$ 成立；又 $r(A^T)=r(A)<n$，$A^Tx=0$ 有非零解，取其中任一非零解即为非零公共解。故充要条件为 $r(A)\le n-2$。
**④ 排除其余选项。** 取 $A=O$ 有非零公共解而 $r(A)=0$，故 (A) 不是必要条件；$r(A)=n-1$ 时虽有 $r(A)+r(A^*)=n$ 却不存在非零公共解，故 (B) 不充分；$r(A)\le n$ 对任意 $n$ 阶矩阵恒成立，而 $A$ 可逆时无非零公共解，故 (C) 不充分。选 (D)。
【思路】按 $A^*$ 的秩分三种情形讨论，再用 $B$ 正定与 $A^*=\alpha\beta^T$ 排除 $r(A)=n-1$。
【易错】$r(A)=n-1$ 时由 $A^*=\alpha\beta^T$ 与 $A^*A=O$ 可得 $A^T\beta=0$，这是把公共解写成 $\lambda\beta$ 的关键；正定性只用于 $\beta^TB\beta>0$。
===Q11===
【答案】$1<a<3$
【解】
**① 考查 0 端。** $x\to0^+$ 时 $\arctan x\sim x,\ \ln(x+2)\to\ln2$，
$$\frac{\arctan^2x}{x^a\ln(x+2)}\sim\frac1{\ln2}\cdot\frac1{x^{a-2}},$$
由幂函数反常积分的敛散性，收敛当且仅当 $a-2<1$，即 $a<3$。
**② 考查 $+\infty$ 端。** $x\to+\infty$ 时 $\arctan x\to\dfrac\pi2,\ \ln(x+2)\sim\ln x$，被积函数与 $\dfrac{\pi^2}{4x^a\ln x}$ 等价，只需考查 $\int_2^{+\infty}\dfrac{dx}{x^a\ln x}$。若 $a>1$，$\dfrac1{x^a\ln x}\le\dfrac1{x^a}$ 收敛；若 $a=1$，$\int\dfrac{dx}{x\ln x}=\ln\ln x+C$ 发散；若 $a<1$，对充分大的 $x$ 有 $\ln x\le x^{\frac{1-a}2}$，从而 $\dfrac1{x^a\ln x}\ge\dfrac1{x^{\frac{a+1}2}}$，而 $\dfrac{a+1}2<1$ 仍发散。故无穷端收敛等价于 $a>1$。
**③ 合并两端。** $a>1$ 且 $a<3$，即 $1<a<3$。
【思路】分别在 0 与 $+\infty$ 两端取等价量，化为 $p$-积分与 $\int\frac{dx}{x^a\ln x}$ 的敛散性。
【易错】0 端等价于 $\dfrac1{x^{a-2}}$，条件是 $a-2<1$ 即 $a<3$；$a=1$ 时 $\int\frac{dx}{x\ln x}$ 发散，不能因分母多一个 $\ln x$ 就认为收敛。
===Q12===
【答案】$y=x+\dfrac12$
【解】
**① 求斜率。** 定义域 $x>0$，只需求 $x\to+\infty$ 时的斜渐近线：
$$k=\lim_{x\to+\infty}\frac yx=\lim_{x\to+\infty}\left[\frac1e\left(1+\frac1x\right)^{x+1}+\frac1x\ln\left(1+\frac1x\right)\right]=1.$$
**② 求截距。** 因 $\ln\left(1+\frac1x\right)\to0$，
$$b=\lim_{x\to+\infty}(y-x)=\lim_{x\to+\infty}\left[\frac{(x+1)^{x+1}}{x^xe}-x\right]=\lim_{x\to+\infty}\frac xe\left[\left(1+\frac1x\right)^{x+1}-e\right].$$
令 $\dfrac1x=u\to0^+$，用 $e^t-1\sim t$ 及 $\ln(1+u)=u-\dfrac12u^2+o(u^2)$：
$$b=\lim_{u\to0^+}\frac{e^{\left(1+\frac1u\right)\ln(1+u)-1}-1}{eu}=\lim_{u\to0^+}\frac{(u+1)\ln(u+1)-u}{u^2}=\lim_{u\to0^+}\frac{\frac12u^2+o(u^2)}{u^2}=\frac12.$$
**③ 结论。** 斜渐近线方程为 $y=x+\dfrac12$。
【思路】先由 $\frac yx$ 得 $k=1$，再令 $u=\frac1x$ 并用泰勒展开算 $b=\lim(y-x)$。
【易错】$\left(1+\frac1x\right)^{x+1}\to e$ 但须展开到 $u^2$ 阶才得出 $\frac12$；$\ln\left(1+\frac1x\right)$ 项极限为 0，不影响 $b$。
===Q13===
【答案】$\dfrac\pi4$
【解】
**① 凑成定积分定义。** 把根号中的 $n^2$ 提出：
$$\frac1{n(n+1)}\sum_{k=1}^n\sqrt{n^2-k^2}=\frac n{n+1}\cdot\frac1n\sum_{k=1}^n\sqrt{1-\left(\frac kn\right)^2}.$$
**② 取极限。** 因 $\sqrt{1-t^2}$ 在 $[0,1]$ 上连续且 $\dfrac n{n+1}\to1$，所求极限为
$$\int_0^1\sqrt{1-t^2}\,dt=\frac\pi4$$
（单位圆在第一象限内的面积）。
【思路】把和式写成 $\frac1n\sum f\left(\frac kn\right)$ 的黎曼和，极限即 $\int_0^1\sqrt{1-t^2}dt$。
【易错】系数 $\dfrac n{n+1}\to1$ 不可漏掉；$\int_0^1\sqrt{1-t^2}dt$ 是四分之一单位圆面积 $\dfrac\pi4$，不是 $\dfrac\pi2$。
===Q14===
【答案】$\dfrac12e^6-\dfrac14e^3$
【解】
**① 参数方程的二阶导公式。** 
$$\frac{d^2y}{dx^2}=\frac1{x'}\frac d{dt}\left(\frac{y'}{x'}\right)=\frac{y''x'-y'x''}{(x')^3}.$$
**② 求 $x',x''$ 与 $y'(0)$。** 由 $x=t^2+2t+3$ 得 $x'(0)=2,\ x''(0)=2$；$t=0$ 时 $y=3$。对 $e^y\sin t-y+3=0$ 两边关于 $t$ 求导得 $e^y(y'\sin t+\cos t)-y'=0$，代入 $t=0,\ y=3$ 得 $y'(0)=e^3$。
**③ 求 $y''(0)$。** 再求导一次并整理得
$$e^y\left[\left((y')^2+y''-1\right)\sin t+2y'\cos t\right]-y''=0,$$
代入 $t=0,\ y=3,\ y'(0)=e^3$ 得 $2e^3\cdot e^3-y''(0)=0$，即 $y''(0)=2e^6$。
**④ 代入公式。** 
$$\left.\frac{d^2y}{dx^2}\right|_{t=0}=\frac{2e^6\cdot2-e^3\cdot2}{2^3}=\frac12e^6-\frac14e^3.$$
【思路】$y$ 由隐式方程确定、$x$ 由参数方程给出，用 $\frac{y''x'-y'x''}{(x')^3}$ 把二阶导化为对 $t$ 的导数。
【易错】求 $y''$ 时指数因子是 $e^y$（在 $y=3$ 处取值 $e^3$）且要用乘积求导；$x'=2t+2$ 在 $t=0$ 为 2，$(x')^3=8$ 勿误写成 $x^3$。
===Q15===
【答案】$2\cos4-\dfrac14\sin4$
【解】
**① 求 $g$ 与 $f$。** 由 $\sin x^2$ 是 $g(x)$ 的一个原函数得 $g(x)=(\sin x^2)'=2x\cos x^2$。当 $x\ne0$ 时把极限凑成导数定义：
$$f(x)=\lim_{t\to\infty}\frac{\ln\left(1+\frac xt\right)}{\frac xt}\cdot x\cdot\frac{g\left(2x+\frac1t\right)-g(2x)}{\frac1t}=xg'(2x),$$
其中第一个因子趋于 1、最后一个因子趋于 $g'(2x)$；$x=0$ 时原式直接给出 $f(0)=0$，故上式对一切 $x$ 成立。
**② 换元并分部积分。** 令 $u=2x$：
$$\int_0^1f(x)dx=\int_0^1xg'(2x)dx=\frac14\int_0^2ug'(u)du=\left.\frac14ug(u)\right|_0^2-\frac14\int_0^2g(u)du.$$
**③ 结果。** 由 $g(2)=4\cos4$ 及 $\int_0^2g(u)du=\left.\sin u^2\right|_0^2=\sin4$ 得
$$\int_0^1f(x)dx=\frac12\cdot4\cos4-\frac14(\sin4-\sin0)=2\cos4-\frac14\sin4.$$
【思路】先把极限识别为 $xg'(2x)$，再令 $u=2x$ 分部积分，利用 $\int g=\sin x^2$ 收尾。
【易错】$\dfrac{\ln(1+x/t)}{x/t}\to1$ 与差商 $\to g'(2x)$ 都要求 $t\to\infty$；换元 $u=2x$ 带来系数 $\dfrac14$，分部积分后 $\int_0^2g(u)du=\sin4$。
===Q16===
【答案】$x=2\alpha_1+\alpha_2+k(-2\alpha_1+\alpha_2+\alpha_3),\ k\in\mathbb R$
【解】
**① 写出 $AP$ 定秩。** 令 $P=(\alpha_1,\alpha_2,\alpha_3)$，三向量线性无关故 $P$ 可逆。按题设逐列写出
$$AP=(\alpha_2,\alpha_3,2\alpha_2-\alpha_3)=P\begin{pmatrix}0&0&0\\1&0&2\\0&1&-1\end{pmatrix}=PB,$$
故 $A$ 与 $B$ 相似，$r(A)=r(B)=2$，齐次方程组 $Ax=0$ 的基础解系含一个向量。
**② 求基础解系。** 设 $x=c_1\alpha_1+c_2\alpha_2+c_3\alpha_3$，则 $Ax=(c_1+2c_3)\alpha_2+(c_2-c_3)\alpha_3$。由 $\alpha_2,\alpha_3$ 线性无关，$Ax=0$ 等价于 $c_1+2c_3=0,\ c_2-c_3=0$；令 $c_3=k$ 得齐次通解 $x=k(-2\alpha_1+\alpha_2+\alpha_3)$。
**③ 求特解并合成。** 由 $A\alpha_1=\alpha_2,\ A\alpha_2=\alpha_3$ 得 $A(2\alpha_1+\alpha_2)=2\alpha_2+\alpha_3$，故原方程的一个特解为 $2\alpha_1+\alpha_2$；全部解
$$x=2\alpha_1+\alpha_2+k(-2\alpha_1+\alpha_2+\alpha_3),\qquad k\in\mathbb R.$$
【思路】用 $P$ 把 $A$ 相似到具体矩阵 $B$ 定秩，再解 $Ax=0$ 并配一个特解。
【易错】$B$ 由 $\alpha_1,\alpha_2,\alpha_3$ 的像逐列拼出，第三列是 $2\alpha_2-\alpha_3$；$r(A)=2$ 时基础解系只有 1 个向量，勿漏任意常数 $k$。
===Q17===
【答案】$-\dfrac{x}{x^2+x+1}+C$
【解】
**① 换元法（$x\ne0$）。** 分子分母同除以 $x^2$：
$$I=\int\frac{x^2-1}{(x^2+x+1)^2}dx=\int\frac{1-\frac1{x^2}}{\left(x+\frac1x+1\right)^2}dx.$$
令 $u=x+\dfrac1x$，则 $du=\left(1-\dfrac1{x^2}\right)dx$，故
$$I=\int\frac{du}{(u+1)^2}=-\frac1{u+1}+C=-\frac{x}{x^2+x+1}+C.$$
**② 补 $x=0$ 并验算。** 因 $x^2+x+1=\left(x+\dfrac12\right)^2+\dfrac34>0$，所得函数在 $\mathbb R$ 上可导，且 $\left(-\dfrac{x}{x^2+x+1}\right)'=\dfrac{x^2-1}{(x^2+x+1)^2}$，故结果对 $x=0$ 也成立。
**③ 分部积分另解。** 由 $I=\int\dfrac1{x^2+x+1}dx-\int\dfrac{x+2}{(x^2+x+1)^2}dx$，而
$$\int\frac1{x^2+x+1}dx=\frac{x}{x^2+x+1}+\int\frac{2x^2+x}{(x^2+x+1)^2}dx,$$
代回得 $I=\dfrac{x}{x^2+x+1}+\int\dfrac{2(x^2-1)}{(x^2+x+1)^2}dx=\dfrac{x}{x^2+x+1}+2I$，解得 $I=\dfrac{-x}{x^2+x+1}+C$。
【思路】把被积函数凑成 $u=x+\frac1x$ 的微分，或分部积分得到 $I=\frac{x}{x^2+x+1}+2I$ 反解。
【易错】换元 $u=x+\frac1x$ 要求 $x\ne0$，必须补证 $x^2+x+1>0$ 使原函数在全体实数可导；分部积分法解出的 $I$ 要移项除以 2 并补 $+C$。
===Q18===
【答案】（I）$f(x,y)=\dfrac43(x^3+y^3)-\dfrac52(x^2+y^2)+xy+\dfrac43$；（II）极大值 $f(0,0)=\dfrac43$，极小值 $f(1,1)=0$
【解】
**（I）由 $f'_x$ 积分还原 $f$。** 将 $f'_x=4x^2-5x+y$ 对 $x$ 积分得 $f(x,y)=\dfrac43x^3-\dfrac52x^2+xy+\varphi(y)$；再对 $y$ 求偏导与 $f'_y=4y^2-5y+x$ 比较得 $\varphi'(y)=4y^2-5y$，从而 $\varphi(y)=\dfrac43y^3-\dfrac52y^2+C$。由 $f(1,1)=0$ 得 $\dfrac83-5+1+C=0$，即 $C=\dfrac43$，所以
$$f(x,y)=\frac43(x^3+y^3)-\frac52(x^2+y^2)+xy+\frac43.$$
**（II）求驻点并判别极值。** 驻点满足 $4x^2-5x+y=0$ 与 $4y^2-5y+x=0$，两式相减得 $(x-y)(4x+4y-6)=0$，故 $x=y$ 或 $x+y=\dfrac32$。当 $x=y$ 时代入得 $4x^2-4x=0$，驻点为 $(0,0),(1,1)$；当 $x+y=\dfrac32$ 时令 $y=\dfrac32-x$ 得 $8x^2-12x+3=0$，另两驻点为
$$\left(\frac{3+\sqrt3}{4},\frac{3-\sqrt3}{4}\right),\qquad\left(\frac{3-\sqrt3}{4},\frac{3+\sqrt3}{4}\right).$$
由 $f''_{xx}=8x-5,\ f''_{yy}=8y-5,\ f''_{xy}=1$，判别式 $D=f''_{xx}f''_{yy}-(f''_{xy})^2=(8x-5)(8y-5)-1$。在 $(0,0)$ 处 $D=24>0$ 且 $f''_{xx}=-5<0$，为极大值点，极大值 $f(0,0)=\dfrac43$；在 $(1,1)$ 处 $D=8>0$ 且 $f''_{xx}=3>0$，为极小值点，极小值 $f(1,1)=0$。对另两驻点有 $x+y=\dfrac32,\ xy=\dfrac38$，故 $D=64xy-40(x+y)+24=64\cdot\dfrac38-40\cdot\dfrac32+24=-12<0$，均不是极值点。
【思路】先由偏导积分还原 $f$，再解驻点方程组并用二阶判别式 $D$ 分类。
【易错】两驻点方程相减须因式分解为 $(x-y)(4x+4y-6)=0$，否则会漏掉 $x+y=\frac32$ 这一支；最后两驻点可整体代入 $xy=\frac38,\ x+y=\frac32$ 算 $D$，无需硬代坐标。
===Q19===
【答案】$I=\dfrac\pi4+\dfrac{23}{24}-\dfrac{\sqrt2}{3}$
【解】
**① 化简取整并定区域。** 极坐标下 $\sqrt{x^2+y^2}=r$；当 $0\le r<1$ 时被积函数为 0，当 $1\le r<2$ 时 $[r]=1$。边界取值不影响积分，只需算 $r\ge1$ 的部分；由圆 $r=2\cos\theta$ 与 $1\le2\cos\theta$ 得 $0\le\theta\le\dfrac\pi3$。
**② 按 $y=x$ 分区。** 区域 A 对应 $\dfrac\pi4\le\theta\le\dfrac\pi3$，此时 $\max\{x,y\}=y=r\sin\theta$；区域 B 对应 $0\le\theta\le\dfrac\pi4$，此时 $\max\{x,y\}=x=r\cos\theta$；两区均有 $1\le r\le2\cos\theta$，故 $I=I_A+I_B$。
**③ 算 $I_A$。** 
$$I_A=\int_{\frac\pi4}^{\frac\pi3}d\theta\int_1^{2\cos\theta}r^2\sin\theta\,dr=\frac13\int_{\frac\pi4}^{\frac\pi3}\sin\theta(8\cos^3\theta-1)d\theta=\left(-\frac23\cos^4\theta+\frac13\cos\theta\right)\Big|_{\frac\pi4}^{\frac\pi3}=\frac7{24}-\frac{\sqrt2}{6}.$$
**④ 算 $I_B$。** 
$$I_B=\int_0^{\frac\pi4}d\theta\int_1^{2\cos\theta}r^2\cos\theta\,dr=\frac83\int_0^{\frac\pi4}\cos^4\theta\,d\theta-\frac13\int_0^{\frac\pi4}\cos\theta\,d\theta,$$
由降幂公式 $\cos^4\theta=\dfrac{3+4\cos2\theta+\cos4\theta}{8}$ 得 $\int_0^{\frac\pi4}\cos^4\theta\,d\theta=\dfrac{3\pi}{32}+\dfrac14$，又 $\int_0^{\frac\pi4}\cos\theta\,d\theta=\dfrac{\sqrt2}{2}$，故 $I_B=\dfrac\pi4+\dfrac23-\dfrac{\sqrt2}{6}$。
**⑤ 结论。** $I=I_A+I_B=\dfrac\pi4+\dfrac{23}{24}-\dfrac{\sqrt2}{3}$。
【思路】用 $[r]$ 把积分限制在 $r\ge1$，再按 $y=x$ 拆分 $\max\{x,y\}$，极坐标化为两区累次积分。
【易错】$I_A$ 的原函数是 $-\dfrac23\cos^4\theta+\dfrac13\cos\theta$（四次幂）；$I_B$ 中 $-\dfrac13\int\cos\theta=-\dfrac{\sqrt2}{6}$ 不能漏，两块相加时 $\dfrac{\sqrt2}{6}$ 合并为 $\dfrac{\sqrt2}{3}$。
===Q20===
【答案】（I）$V=\dfrac{16}{105}\pi a^3$；（II）$S=\dfrac{16}{5}\pi a^2$
【解】
**（I）旋转体体积。** 曲线为星形线 $x=a\cos^3t,\ y=a\sin^3t$。区域 $D_1$ 绕 $y$ 轴旋转时垂直于 $y$ 轴的截面为半径 $x$ 的圆，由 $y=a\sin^3t$ 得 $dy=3a\sin^2t\cos t\,dt$，故
$$V=\pi\int_0^{\frac\pi2}x^2(t)y'(t)\,dt=3\pi a^3\int_0^{\frac\pi2}(\cos^7t-\cos^9t)\,dt=3\pi a^3\left(\frac{16}{35}-\frac{128}{315}\right)=\frac{16}{105}\pi a^3.$$
**（II）旋转体表面积。** 边界由 L 与 $\Gamma$ 分别旋转所得的内、外两部分曲面组成，两曲线端点重合，无须另加端面面积。由 $x'=-3a\cos^2t\sin t,\ y'=3a\sin^2t\cos t$ 得 $\sqrt{(x')^2+(y')^2}=3a\sin t\cos t$，故
$$S_L=2\pi\int_0^{\frac\pi2}y(t)\sqrt{(x')^2+(y')^2}\,dt=6\pi a^2\int_0^{\frac\pi2}\sin^4t\cos t\,dt=\frac65\pi a^2.$$
对 $\Gamma$：在 $0<x<a$ 时 $y'=-\dfrac{x}{\sqrt{a^2-x^2}}$，故 $y\sqrt{1+(y')^2}=\sqrt{a^2-x^2}\sqrt{1+\dfrac{x^2}{a^2-x^2}}=a$，于是 $S_\Gamma=2\pi\int_0^a a\,dx=2\pi a^2$。总表面积
$$S=S_L+S_\Gamma=\frac65\pi a^2+2\pi a^2=\frac{16}{5}\pi a^2.$$
【思路】体积用圆盘法 $V=\pi\int x^2dy$，表面积分 L（弧长旋转）与 $\Gamma$（球面带）两部分相加。
【易错】$V$ 中 $y'=3a\sin^2t\cos t$ 使被积为 $3\pi a^3(\cos^7t-\cos^9t)$，由点火公式得 $\dfrac{16}{35}-\dfrac{128}{315}$；$\Gamma$ 旋转时 $y\sqrt{1+(y')^2}=a$ 为常数，故 $S_\Gamma=2\pi a^2$。
===Q21===
【答案】（I）$\lim\limits_{n\to\infty}x_n=2$；（II）$\lim\limits_{n\to\infty}\dfrac{S_n}{2^n}=-2$
【解】
**（I）单调有界收敛。** 由 $x_1=3>2$ 且
$$x_{n+1}-2=\frac{x_n^2+2}{2x_n-1}-2=\frac{(x_n-2)^2}{2x_n-1},$$
若 $x_n>2$ 则分子、分母皆正，故 $x_{n+1}>2$，归纳得 $x_n>2\ (n\ge1)$。又
$$x_n-x_{n+1}=x_n-\frac{x_n^2+2}{2x_n-1}=\frac{(x_n-2)(x_n+1)}{2x_n-1}>0,$$
故 $\{x_n\}$ 单调递减且有下界，由单调有界准则知其收敛。设 $\lim\limits_{n\to\infty}x_n=A\ge2$，在递推式两边取极限得 $A=\dfrac{A^2+2}{2A-1}$，即 $(A-2)(A+1)=0$，结合 $A\ge2$ 得 $\lim\limits_{n\to\infty}x_n=2$。
**（II）求 $\lim\frac{S_n}{2^n}$。** 由 $x_{n+1}+1=\dfrac{(x_n+1)^2}{2x_n-1}$ 与 (I) 中的差式相除：
$$a_{n+1}=\frac{x_{n+1}-2}{x_{n+1}+1}=\left(\frac{x_n-2}{x_n+1}\right)^2=a_n^2.$$
由 $a_1=\dfrac14$ 得 $a_n=a_1^{2^{n-1}}=2^{-2^n}>0$，故 $\log_2a_n=-2^n$；由等比求和
$$S_n=\sum_{k=1}^n\log_2a_k=-\sum_{k=1}^n2^k=-2^{n+1}+2,$$
于是 $\lim\limits_{n\to\infty}\dfrac{S_n}{2^n}=\lim\limits_{n\to\infty}\left(-2+\dfrac2{2^n}\right)=-2$。
【思路】(I) 用单调有界准则求极限；(II) 把 $a_n$ 化为迭代 $a_{n+1}=a_n^2$，取对数后等比求和。
【易错】$x_n>2$ 保证 $2x_n-1>0$，否则差商符号无法判定；$a_n=2^{-2^n}$ 才使 $\log_2a_n=-2^n$，求和 $-\sum2^k$ 后除以 $2^n$ 得 $-2$，不是直接消去 $2^{n+1}$。
===Q22===
【答案】（I）$A=\begin{pmatrix}0&1&1\\-2&3&2\\0&0&\lambda\end{pmatrix}$；（II）$\lambda=1$；（III）$x_n=2^n,\ y_n=2^{n+1}-1\ (n=0,1,\cdots)$
【解】
**（I）写出递推矩阵。** 由题设递推关系
$$\begin{pmatrix}x_n\\y_n\\\lambda^n\end{pmatrix}=\begin{pmatrix}0&1&1\\-2&3&2\\0&0&\lambda\end{pmatrix}\begin{pmatrix}x_{n-1}\\y_{n-1}\\\lambda^{n-1}\end{pmatrix},\qquad A=\begin{pmatrix}0&1&1\\-2&3&2\\0&0&\lambda\end{pmatrix}.$$
**（II）由相似对角化定 $\lambda$。** 
$$|\mu E-A|=(\mu-\lambda)\left[\mu(\mu-3)+2\right]=(\mu-\lambda)(\mu-1)(\mu-2),$$
特征值为 $1,2,\lambda$；由 $A$ 只有两个不同的特征值知 $\lambda=1$ 或 $\lambda=2$。当 $\lambda=1$ 时 $A-E=\begin{pmatrix}-1&1&1\\-2&2&2\\0&0&0\end{pmatrix}$ 的秩为 1，二重特征值 1 有 $3-1=2$ 个线性无关的特征向量，加上特征值 2 的一个特征向量，$A$ 可相似对角化；当 $\lambda=2$ 时 $A-2E=\begin{pmatrix}-2&1&1\\-2&1&2\\0&0&0\end{pmatrix}$ 的秩为 2，二重特征值 2 只有 $3-2=1$ 个线性无关的特征向量，不能相似对角化。故 $\lambda=1$。
**（III）求 $x_n,y_n$。** 取 $\lambda=1$。由 $(A-E)v=0$ 得 $-v_1+v_2+v_3=0$，可取 $v_1=(1,1,0)^T,\ v_2=(1,0,1)^T$；由 $(A-2E)v=0$ 两式相减得 $v_3=0$、再得 $v_2=2v_1$，可取 $v_3=(1,2,0)^T$。将 $\alpha_0=(1,1,1)^T$ 写成 $c_1v_1+c_2v_2+c_3v_3$，比较分量得 $c_1+c_2+c_3=1,\ c_1+2c_3=1,\ c_2=1$，解得 $c_1=-1,\ c_2=c_3=1$。由 $\alpha_n=A^n\alpha_0$ 及 $Av_1=v_1,\ Av_2=v_2,\ Av_3=2v_3$ 得
$$\alpha_n=-v_1+v_2+2^nv_3=\begin{pmatrix}2^n\\2^{n+1}-1\\1\end{pmatrix},$$
比较分量得 $x_n=2^n,\ y_n=2^{n+1}-1,\ n=0,1,\cdots$。
【思路】把递推写成 $\alpha_n=A\alpha_{n-1}$，用相似对角化条件定 $\lambda$，再把初值按特征向量展开求 $A^n\alpha_0$。
【易错】递推向量第三分量是 $\lambda^n$（不是 $z_n$），故 $A$ 的右下角为 $\lambda$；$\lambda=2$ 时二重特征值只有 1 个无关特征向量，不可对角化；$A^n\alpha_0$ 中 $v_1,v_2$ 对应特征值 1、$v_3$ 对应 2，系数依次为 $-1,1,2^n$。
