===Q1===
【答案】C
【解】
**① 导数极限的局部性只覆盖去心邻域。** $\lim\limits_{x\to0}f'(x)=a$ 存在，只能说明 $f$ 在 $x=0$ 的左、右邻域内可导，无法反映 $x=0$ 处的可导性，故 (A) 错。例如 $f(x)=\begin{cases}x+1,&x\le0,\\x-1,&x>0,\end{cases}$ 满足 $\lim\limits_{x\to0}f'(x)=1$，但 $x=0$ 处左极限为 $1$、右极限为 $-1$，极限不存在，故 (B) 错。
**② 在连续性假设下用中值定理补上 $x=0$ 处。** 若 $f$ 在 $x=0$ 连续，对 $x>0$ 用拉格朗日中值定理，存在 $\xi\in(0,x)$ 使
$$f'_+(0)=\lim_{x\to0^+}\frac{f(x)-f(0)}{x}=\lim_{x\to0^+}f'(\xi)=\lim_{x\to0^+}f'(x)=a.$$
同理 $f'_-(0)=a$，故 $f'(0)$ 存在且等于 $a$，(C) 正确。
**③ 反例排除 (D)。** 取 $f(x)=\begin{cases}2x,&x\ne0,\\1,&x=0,\end{cases}$ 则 $\lim\limits_{x\to0}f'(x)=2$ 存在，而在 $x=0$ 的充分小去心邻域内 $f(x)=2x$ 可任意小，故 $f(0)=1$ 为极大值，(D) 错。
【思路】区分「导函数的极限」与「该点导数」，前者只管去心邻域；补上连续性后用拉格朗日中值定理把差商换成 $f'(\xi)$ 取极限。
【易错】$\lim f'(x)$ 存在并不能推出 $f$ 在该点连续或可导；必须另加连续性条件，才能由中值定理得到 $f'(0)=\lim f'(x)$。

===Q2===
【答案】D
【解】
**① 用反例逐一排除。** 对 (A) 取 $x_n=(-1)^n$，则 $x_n^2=1$ 收敛，但 $x_{n+1}-x_n$ 在 $\pm2$ 间振荡，极限不存在；对 (B) 仍取 $x_n=(-1)^n$，则 $x_n-\dfrac1{x_n}=(-1)^n-(-1)^n=0$ 收敛，而 $x_{n+1}-x_n$ 极限不存在；对 (C) 取 $x_n=n$，则 $\arctan x_n\to\dfrac\pi2$ 收敛，但 $x_{n+1}-x_n=1$。故 (A)(B)(C) 都不是充分条件。
**② 论证 (D) 充分。** 令 $h(x)=x+\sin x$，则 $h'(x)=1+\cos x\ge0$ 且只在孤立点取零，故 $h$ 在 $\mathbb R$ 上严格单调递增、连续，且值域为 $\mathbb R$，其反函数连续。若 $\{h(x_n)\}$ 收敛，则 $\{x_n\}=\{h^{-1}(h(x_n))\}$ 收敛，设极限为 $A$，于是 $x_{n+1}-x_n\to A-A=0$。
【思路】前三项用 $(-1)^n$ 与 $n$ 两组反例排除；对 (D) 考察 $h(x)=x+\sin x$ 严格单调且连续，由反函数连续性把 $\{h(x_n)\}$ 的收敛传递到 $\{x_n\}$。
【易错】$h'(x)\ge0$ 且零点孤立才能保证严格单调；仅有 $\arctan$ 连续还不够——$\arctan x_n$ 收敛时 $x_n$ 可以像 $n$ 一样发散，因为 $\arctan$ 有界且其反函数只在有界区间内定义。

===Q3===
【答案】B
【解】
**① 数驻点看 $f'$ 的零点。** 从图像数出 $f'(x)=0$ 的位置共 4 个：左侧 U 形曲线与 $x$ 轴的两个穿越点、右侧下降段的一个穿越点、右侧小凸起与 $x$ 轴的一个相切点，故 $a=4$。
**② 数极值点看 $f'$ 是否变号。** 左侧两个穿越点处 $f'$ 由正变负、由负变正；右侧下降段由正变负；右侧小凸起处 $f'$ 在零点两侧同号（只相切不穿越），不产生极值。故极值点 $b=3$。
**③ 数拐点看 $f'$ 的单调性是否改变。** $f'$ 的单调性在四个位置改变：左侧谷底、右侧谷底、右侧小凸起，以及 $x=0$（图像在 $y$ 轴两侧不相接，左侧 $f'$ 递增、右侧 $f'$ 递减），故 $c=4$。
【思路】驻点数 $f'$ 的零点，极值点数 $f'$ 的变号零点，拐点数 $f'$ 单调性的改变点；注意相切零点不产生极值、间断点也可能是拐点。
【易错】极值点只可能出现在驻点或不可导点，但驻点未必是极值点；拐点对应 $f'$ 的单调性变化，即使 $f'$ 在该点不连续也需计入。

===Q4===
【答案】A
【解】
**① 判断奇偶性。** $\sin^3t$ 为奇函数，其变上限积分 $f(x)=\int_0^x\sin^3t\,dt$ 为偶函数；$\cos^4t$ 为偶函数，$g(x)=\int_0^x\cos^4t\,dt$ 为奇函数。命题①正确。
**② 判断单调性。** $f'(x)=\sin^3x$ 可变正可负，$f$ 非单调；$g'(x)=\cos^4x\ge0$ 且不在任何区间恒为零，故 $g$ 单调递增。命题②「均不是单调函数」错误。
**③ 判断有界性。** $g'\ge0$ 且 $\lim\limits_{x\to+\infty}g'(x)\ne0$，$g$ 单调递增且无界；而 $f$ 有界，$0\le f(x)\le\int_0^{\pi}\sin^3t\,dt=\dfrac43$。命题③「均有界」错误。
**④ 判断周期性。** 因 $\sin^3t$ 以 $2\pi$ 为周期且 $\int_x^{x+2\pi}\sin^3t\,dt=0$，有 $f(x+2\pi)=f(x)$，$f$ 是周期函数；$g$ 单调递增，必不是周期函数。命题④「均不是周期函数」错误。
仅①正确，正确个数为 1。
【思路】利用变上限积分的被积函数奇偶性定 $f,g$ 的奇偶性，由 $f',g'$ 的符号定单调性，由周期函数在一个周期上积分为零判断 $f$ 的周期性。
【易错】变上限积分的奇偶性由被积函数奇偶性决定：奇函数的变上限积分是偶函数，偶函数的变上限积分是奇函数；正的周期函数累积后是单调递增而非周期函数。

===Q5===
【答案】C
【解】
**① 特例法快速定位。** 取 $f(x)=x+\dfrac13x^2$，满足 $\lim\limits_{x\to0}\dfrac{f(x)}x=1$ 且 $f''=\dfrac23\in(0,1)$，此时
$$\int_0^1f(x)\,dx=\int_0^1\left(x+\frac13x^2\right)dx=\frac12+\frac19=\frac{11}{18}\in\left(\frac12,1\right),$$
只有 (C) 符合。
**② 严格证明下界。** 由 $\lim\limits_{x\to0}f(x)/x=1$ 及 $f$ 连续得 $f(0)=0$、$f'(0)=1$；由 $0<f''<1$ 知 $f'$ 严格递增且 $f'(1)-f'(0)<1$，故 $1\le f'(x)\le f'(1)<2$。令 $F_1(x)=f(x)-x$，有 $F_1(0)=0$、$F_1'(x)=f'(x)-1>0$，故 $f(x)>x$。
**③ 严格证明上界。** 令 $F_2(x)=f(x)-2x$，有 $F_2(0)=0$、$F_2'(x)=f'(x)-2<0$，故 $f(x)<2x$。于是
$$\int_0^1x\,dx<\int_0^1f(x)\,dx<\int_0^12x\,dx,$$
即 $\dfrac12<\int_0^1f(x)\,dx<1$，选 (C)。
【思路】先取满足条件的二次函数估算出答案区间，再借 $0<f''<1$ 得 $1\le f'<2$，用 $f(x)-x$ 与 $f(x)-2x$ 的单调性夹逼 $f$。
【易错】$\lim f(x)/x=1$ 同时给出 $f(0)=0$ 与 $f'(0)=1$；由 $f''>0$ 只能得 $f'(x)>f'(0)=1$（$x>0$），不能直接写出 $f$ 的表达式，需用辅助函数比较。

===Q6===
【答案】B
【解】
**① 去根号换元。** 令 $t=\sqrt{e^x-1}$，则 $e^x=t^2+1$，即 $x=\ln(t^2+1)$，从而 $\mathrm{d}x=\dfrac{2t}{t^2+1}\mathrm{d}t$；当 $x:0\to+\infty$ 时 $t:0\to+\infty$。
**② 化为有理函数积分。** 代入得
$$\int_0^{+\infty}\frac{\mathrm{d}x}{\sqrt{e^x-1}}=\int_0^{+\infty}\frac1t\cdot\frac{2t}{t^2+1}\,\mathrm{d}t=2\int_0^{+\infty}\frac{\mathrm{d}t}{t^2+1}=2\arctan t\Big|_0^{+\infty}=\pi.$$
选 (B)。
【思路】用 $t=\sqrt{e^x-1}$ 把指数型反常积分化为 $\int\frac{\mathrm{d}t}{1+t^2}$ 的标准反正切积分。
【易错】换元后必须同步改写微分与上下限：$x=0$ 对应 $t=0$，$x\to+\infty$ 对应 $t\to+\infty$；$\dfrac{2t}{t^2+1}$ 中的因子 $t$ 与分母的根号相消，不能漏掉。

===Q7===
【答案】C
【解】
**① 写出积分区域。** 由 $0\le x\le2$、$x^2\le y\le x$ 知：当 $0\le x\le1$ 时区域夹在抛物线 $y=x^2$ 与直线 $y=x$ 之间；当 $1<x\le2$ 时 $x^2>x$，原积分的上下限次序颠倒，需加负号，几何上对应同一条抛物线与直线之间那块带方向的区域。
**② 化为极坐标边界。** 抛物线 $y=x^2$ 即 $r\sin\theta=r^2\cos^2\theta$，得 $r=\tan\theta\sec\theta$；直线 $y=x$ 对应 $\theta=\dfrac\pi4$；直线 $x=2$ 对应 $r=2\sec\theta$；交点 $(2,4)$ 对应 $\theta=\arctan2$。
**③ 按角度分段写出。** 当 $0\le\theta\le\dfrac\pi4$ 时，$r$ 从 $0$ 到抛物线 $\tan\theta\sec\theta$；当 $\dfrac\pi4\le\theta\le\arctan2$ 时，因 $y$ 的积分方向反转，$r$ 应从 $2\sec\theta$ 积到 $\tan\theta\sec\theta$。故
$$I=\int_0^{\frac\pi4}\mathrm{d}\theta\int_0^{\tan\theta\sec\theta}f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r+\int_{\frac\pi4}^{\arctan2}\mathrm{d}\theta\int_{2\sec\theta}^{\tan\theta\sec\theta}f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r,$$
选 (C)。
【思路】先识别 $y=x^2$、$y=x$、$x=2$ 三条边界，写出极坐标方程，再按 $\theta=\pi/4$ 分段，注意 $x\in(1,2)$ 时内层积分方向反转要用交换上下限体现负号。
【易错】本题在 $x\in(1,2)$ 内层积分是「从大到小」，必须加负号；(C) 把负号吸收进交换后的上下限，(D) 的第二个积分上下限顺序相反且无负号，故错。

===Q8===
【答案】B
【解】
**① 验证 (A)(C)(D)。** 偶置换矩阵由偶数次交换两行得到，故 $|A|=1$ 且 $A$ 正交，即 $A^{-1}=A^T$，(A) 成立；由 $A^*=|A|A^{-1}=A^{-1}$ 得 (D) 成立；偶置换矩阵的逆仍是偶置换矩阵，故 $A^*$ 为偶置换矩阵，(C) 成立。
**② 举反例否定 (B)。** 取
$$A=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix},$$
它可由三阶单位矩阵经两次交换行得到，是偶置换矩阵。此时 $A^*=A^{-1}=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$，且 $(A^*)^T=(A^T)^*=A\ne A^*$，故 (B) 不一定成立。
【思路】先用 $|A|=1$、$A^{-1}=A^T$、$A^*=|A|A^{-1}$ 确认三项必然成立，再找一个三阶偶置换矩阵的具体反例检验伴随与转置可交换性。
【易错】矩阵取伴随与取转置一般不可交换，即 $(A^T)^*\ne(A^*)^*$ 常成立；验证「不一定成立」只需一个反例，无需一般证明。

===Q9===
【答案】C
【解】
**① 求 $A^*$ 与 $A$ 的特征值。** 令 $B=\begin{pmatrix}2&1&0\\-1&0&0\\0&0&4\end{pmatrix}$，由 $|\lambda E-B|=(\lambda-1)^2(\lambda-4)=0$ 得 $A^*$ 的特征值为 $1,1,4$，故 $|A^*|=4$。又 $|A^*|=|A|^2$ 且 $|A|>0$，得 $|A|=2$，于是 $A$ 的特征值为 $\dfrac2{1},\dfrac2{1},\dfrac24$，即 $2,2,\dfrac12$。
**② 求 $r(A-2E)$。** $A^*-E\sim\begin{pmatrix}1&1&0\\-1&-1&0\\0&0&3\end{pmatrix}$，故 $r(A^*-E)=2$，即 $A^*$ 对应二重特征值 $1$ 只有一个线性无关特征向量。因 $A$ 可逆，$A^*$ 与 $A$ 的特征向量相同，故 $A$ 对应二重特征值 $2$ 也只有一个线性无关特征向量，即 $(A-2E)x=0$ 只有一个线性无关解，从而 $r(A-2E)=2$。
**③ 求 $r(2A-E)$。** 同理 $A^*-4E\sim\begin{pmatrix}-2&1&0\\-1&-4&0\\0&0&0\end{pmatrix}$，$r(A^*-4E)=2$，故 $A$ 对应特征值 $\dfrac12$ 只有一个线性无关特征向量，$r\!\left(A-\dfrac12E\right)=2$。由 $2A-E=2\!\left(A-\dfrac12E\right)$ 得 $r(2A-E)=2$。
综上 $r(A-2E)+r(2A-E)=4$，选 (C)。
【思路】由相似矩阵特征值相同定出 $A^*$ 的谱，用 $|A^*|=|A|^{n-1}$ 与 $|A|>0$ 反推 $A$ 的谱，再由 $A^*$ 与 $A$ 特征向量相同，把几何重数转移过来求秩。
【易错】$r(A-\lambda E)=n-\dim\ker(A-\lambda E)$，二重特征值未必给出两个线性无关特征向量；必须由 Jordan 块结构（即 $r(A^*-\lambda E)$）判断几何重数。

===Q10===
【答案】B
【解】
**① 由 $A\alpha=\alpha$ 定出矩阵。** 平方项系数均为 0，故
$$A=\begin{pmatrix}0&a_{12}&a_{13}\\a_{12}&0&a_{23}\\a_{13}&a_{23}&0\end{pmatrix}.$$
由 $A\alpha=\alpha$、$\alpha=(1,2,-1)^T$ 得
$$\begin{cases}2a_{12}-a_{13}=1,\\a_{12}-a_{23}=2,\\a_{13}+2a_{23}=-1,\end{cases}\quad\text{解得}\quad a_{12}=1,\ a_{13}=1,\ a_{23}=-1,$$
即 $A=\begin{pmatrix}0&1&1\\1&0&-1\\1&-1&0\end{pmatrix}$。
**② 求特征值定惯性指数。** 计算特征多项式
$$|\lambda E-A|=\begin{vmatrix}\lambda&-1&-1\\-1&\lambda&1\\-1&1&\lambda\end{vmatrix}=(\lambda-1)^2(\lambda+2)=0,$$
特征值为 $1,1,-2$。正特征值两个、负特征值一个，故正、负惯性指数分别为 $2,1$，选 (B)。
【思路】「平方项系数为 0」确定 $A$ 的零对角结构，由特征方程 $A\alpha=\alpha$ 解出三个非对角元，再求特征值符号得到惯性指数。
【易错】二次型矩阵的对角元是平方项系数、非对角元是交叉项系数的一半；本题交叉项系数若为 $2x_1x_2$ 形式才对应非对角元 $1$，需按 $A\alpha=\alpha$ 的分量方程整体核对。

===Q11===
【答案】$\dfrac13$
【解】
**① 处理分母。** 由 $\ln(1+x)=x-\dfrac{x^2}{2}+o(x^2)$ 得 $x-\ln(1+x)=\dfrac{x^2}{2}+o(x^2)$，故分母 $x[x-\ln(1+x)]\sim\dfrac{x^3}{2}$。
**② 把分子写成两角差。** 注意 $\arctan x=x-\dfrac{x^3}{3}+o(x^3)$ 与 $\sin x$ 同阶于 $x$，故可将分子写为 $\tan(\sin x)-\tan(\arctan x)$。由拉格朗日中值定理，存在 $\xi$ 介于 $\sin x$ 与 $\arctan x$ 之间（$\xi\to0$），使
$$\tan(\sin x)-\tan(\arctan x)=\sec^2\xi\,(\sin x-\arctan x)\sim\sin x-\arctan x.$$
**③ 算主项并相除。** 由 $\sin x=x-\dfrac{x^3}{6}+o(x^3)$、$\arctan x=x-\dfrac{x^3}{3}+o(x^3)$ 得
$$\sin x-\arctan x=\frac{x^3}{6}+o(x^3),$$
所以原极限 $=\dfrac{1/6}{1/2}=\dfrac13$。
【思路】分母用 $\ln(1+x)$ 展开定出 $x^3/2$，分子把 $x$ 换成 $\arctan x$ 后用中值定理化为 $\sin x-\arctan x$，再用泰勒展开求主项。
【易错】$\tan(\sin x)-x$ 与 $x^3$ 同阶但不能分别把 $\tan(\sin x)$、$x$ 各自替换成低阶近似后相减；用中值定理或拆成 $[\tan(\sin x)-\sin x]+[\sin x-x]$ 更稳妥。

===Q12===
【答案】$-\dfrac{16}{27}$
【解】
**① 求对应的 $y$。** 将 $x=2$ 代入 $x^3+y^3-3x+6y=2$ 得 $8+y^3-6+6y=2$，即 $y^3+6y=0$，因 $y^2+6>0$ 得 $y=0$。
**② 把 $x$ 视为 $y$ 的函数求一阶导。** 两边对 $y$ 求导（记 $x'=dx/dy$）得
$$3x^2x'+3y^2-3x'+6=0.$$
代入 $x=2,y=0$：$12x'-3x'+6=0$，得 $x'=-\dfrac23$。
**③ 再求导并代入。** 继续对 $y$ 求导得
$$6x(x')^2+3x^2x''+6y-3x''=0.$$
代入 $x=2,\ y=0,\ x'=-\dfrac23$：
$$12\cdot\frac49+9x''=0\ \Longrightarrow\ x''=-\frac{16}{27}.$$
【思路】隐函数求导时明确 $x=x(y)$，两次对 $y$ 求导，先由原方程定出 $y$，再依次代入一阶、二阶导方程。
【易错】题目求的是 $d^2x/dy^2$ 而非 $d^2y/dx^2$，求导变量不能搞反；符号上 $x'=-2/3$ 为负，二次求导后 $x''$ 仍为负，答案带负号。

===Q13===
【答案】$\dfrac13\pi e^3+\pi e-\dfrac43\pi$
【解】
**① 写旋转曲面面积公式。** $y'=\dfrac{x}{2}-\dfrac{1}{2x}$，绕 $y$ 轴旋转的侧面积为
$$S=2\pi\int_1^e x\sqrt{1+(y')^2}\,\mathrm{d}x.$$
**② 化简根式。** 因
$$1+\left(\frac{x}{2}-\frac{1}{2x}\right)^2=\left(\frac{x}{2}+\frac{1}{2x}\right)^2,$$
且 $x\in[1,e]$ 上 $\dfrac{x}{2}+\dfrac{1}{2x}>0$，故
$$S=2\pi\int_1^e x\left(\frac{x}{2}+\frac{1}{2x}\right)\mathrm{d}x=2\pi\int_1^e\left(\frac{x^2}{2}+\frac12\right)\mathrm{d}x.$$
**③ 计算定积分。** 
$$S=2\pi\left[\frac{x^3}{6}+\frac{x}{2}\right]_1^e=\frac{\pi}{3}(e^3-1)+\pi(e-1)=\frac13\pi e^3+\pi e-\frac43\pi.$$
【思路】利用 $\sqrt{1+(y')^2}=\frac{x}{2}+\frac{1}{2x}$ 的完全平方结构去掉根号，再套用绕 $y$ 轴旋转的侧面积公式积分。
【易错】绕 $y$ 轴旋转的面积公式是 $2\pi\int x\sqrt{1+(y')^2}\,dx$，半径是 $x$ 不是 $y$；根式化简时 $\sqrt{(\frac x2+\frac1{2x})^2}$ 要取正值，区间内该式为正。

===Q14===
【答案】$(-\infty,0)$
【解】
**① 写特征方程。** $y''+y'+ay=0$ 的特征方程为 $\lambda^2+\lambda+a=0$，判别式 $\Delta=1-4a$。
**② 讨论 $\Delta>0$。** 当 $a<\dfrac14$ 时，$\lambda_{1,2}=\dfrac{-1\pm\sqrt{1-4a}}{2}$，通解为 $y=C_1e^{\lambda_1x}+C_2e^{\lambda_2x}$。存在无界解当且仅当较大根 $\lambda_1=\dfrac{-1+\sqrt{1-4a}}{2}>0$，即 $\sqrt{1-4a}>1$，解得 $a<0$。
**③ 讨论 $\Delta\le0$。** 当 $a=\dfrac14$ 时，$\lambda_1=\lambda_2=-\dfrac12$，通解 $y=(C_1+C_2x)e^{-x/2}$ 在 $(0,+\infty)$ 上有界；当 $a>\dfrac14$ 时，$\lambda_{1,2}=-\dfrac12\pm\dfrac{\sqrt{4a-1}}{2}i$，通解为衰减的指数乘正余弦，也有界。
综上，仅当 $a<0$ 时存在无界解，即 $a\in(-\infty,0)$。
【思路】按特征方程判别式分三种情形，判断通解中是否含有指数增长项 $e^{\lambda x}$（$\lambda>0$）或有界性被多项式破坏的情形。
【易错】「存在无界解」只需一个特解无界，即较大特征根为正即可；重根 $-1/2$ 情形虽有因子 $x$，但被 $e^{-x/2}$ 压制仍有界。

===Q15===
【答案】$x-y$
【解】
**① 记中间变量。** 令 $z=\dfrac{x+y}{xy}=\dfrac1x+\dfrac1y$，则 $u=xyf(z)$，且 $z_x=-\dfrac1{x^2}$、$z_y=-\dfrac1{y^2}$。
**② 求两个偏导。** 由乘积与链式法则，
$$u_x=yf(z)+xyf'(z)\left(-\frac1{x^2}\right)=yf(z)-\frac{y}{x}f'(z),$$
$$u_y=xf(z)+xyf'(z)\left(-\frac1{y^2}\right)=xf(z)-\frac{x}{y}f'(z).$$
**③ 代入组合式。** 于是
$$x^2u_x-y^2u_y=\left[x^2yf(z)-xyf'(z)\right]-\left[xy^2f(z)-xyf'(z)\right]=xy(x-y)f(z)=(x-y)u,$$
其中含 $f'(z)$ 的两项恰好抵消。故 $g(x,y)=x-y$。
【思路】把 $u$ 看作 $xyf(z)$ 求偏导，含 $f'$ 的项在组合 $x^2u_x-y^2u_y$ 中相消，剩下 $(x-y)u$。
【易错】$z=\frac{x+y}{xy}$ 应拆成 $\frac1x+\frac1y$ 再求导更简单；不要误把 $f'$ 的项保留下来，也不要漏掉乘积法则中 $y f(z)$ 与 $x f(z)$ 两项。

===Q16===
【答案】$x=\begin{pmatrix}1\\1\\0\end{pmatrix}+k\begin{pmatrix}-1\\2\\1\end{pmatrix}\ (k\in\mathbb R)$
【解】
**① 把 $A$ 写成 $P$ 乘常数矩阵。** 令 $P=(\alpha_1,\alpha_2,\alpha_3)$，由 $\alpha_1,\alpha_2,\alpha_3$ 线性无关知 $P$ 可逆。按列写出
$$A=PB,\quad B=\begin{pmatrix}1&0&1\\1&1&-1\\0&1&-2\end{pmatrix},\qquad \alpha_4=P\beta,\quad \beta=\begin{pmatrix}1\\2\\1\end{pmatrix}.$$
**② 化简方程。** $Ax=\alpha_4\iff PBx=P\beta\iff Bx=\beta$（左乘 $P^{-1}$）。
**③ 解线性方程组。** 对增广矩阵作初等行变换：
$$(B,\beta)=\begin{pmatrix}1&0&1&1\\1&1&-1&2\\0&1&-2&1\end{pmatrix}\longrightarrow\begin{pmatrix}1&0&1&1\\0&1&-2&1\\0&0&0&0\end{pmatrix}.$$
得 $x_1=1-x_3$、$x_2=1+2x_3$。令 $x_3=k$，通解为
$$x=\begin{pmatrix}1\\1\\0\end{pmatrix}+k\begin{pmatrix}-1\\2\\1\end{pmatrix}\quad(k\in\mathbb R).$$
【思路】用线性无关的 $\alpha_1,\alpha_2,\alpha_3$ 作基，把向量方程化为坐标方程组 $Bx=\beta$，再高斯消元写出通解。
【易错】矩阵 $A$ 的三列依次是 $\alpha_1+\alpha_2$、$\alpha_2+\alpha_3$、$\alpha_1-\alpha_2-2\alpha_3$，写成 $PB$ 时 $B$ 的各列要与之对应；$\alpha_4$ 的坐标是 $(1,2,1)^T$ 而不是 $(1,1,1)^T$。

===Q17===
【答案】$a=-2$；$x=-1$ 是 $f'(x)$ 的第二类（无穷）间断点
【解】
**① 求左导数。** $f(0)=0$。当 $x\to0^-$ 时，
$$f'_-(0)=\lim_{x\to0^-}\frac{f(x)-f(0)}{x}=\lim_{x\to0^-}\frac{\ln\left|\frac{1+x}{1-x}\right|+ax}{x}=a+\lim_{x\to0^-}\frac{\ln(1+x)-\ln(1-x)}{x}=a+1+1=a+2.$$
**② 求右导数并定 $a$。** 当 $x\to0^+$ 时，令 $t=1/x\to+\infty$，
$$f'_+(0)=\lim_{x\to0^+}\frac{e^{-\frac1x}}{x}=\lim_{t\to+\infty}\frac{t}{e^{t}}=0.$$
由可导要求 $f'_-(0)=f'_+(0)$，得 $a+2=0$，即 $a=-2$，且 $f'(0)=0$。
**③ 写出 $f'$ 并找间断点。** 分段求导得
$$f'(x)=\begin{cases}\dfrac{1}{1+x}+\dfrac{1}{1-x}-2,&x\le0\text{ 且 }x\ne-1,\\[4pt]\dfrac{1}{x^2}e^{-\frac1x},&x>0.\end{cases}$$
$f'$ 的定义域为 $\{x\in(-\infty,+\infty)\mid x\ne-1\}$，故唯一间断点是 $x=-1$。
**④ 判别类型。** 因 $\lim\limits_{x\to-1}f'(x)=\lim\limits_{x\to-1}\left(\dfrac1{1+x}+\dfrac1{1-x}-2\right)=\infty$（左、右分别趋于 $-\infty$、$+\infty$），极限不存在且为无穷，故 $x=-1$ 是 $f'(x)$ 的第二类（无穷）间断点。
【思路】用导数定义分别求 $x=0$ 处左右导数定出 $a$，再分段求导写出 $f'$，由定义域找出间断点并用极限判别类型。
【易错】右支是 $e^{-1/x}$，其差商极限为 $0$；$\ln\left|\frac{1+x}{1-x}\right|$ 在 $x=0$ 附近的绝对值可去掉，但 $x=-1$ 是本题真正的奇点；$x=0$ 处虽分段但左右导数相等，$f'$ 在 $0$ 连续。

===Q18===
【答案】(I) $f(x)=\sqrt{1+x^2}$；(II) $y=\dfrac{1}{\sqrt2}x+\dfrac{1}{\sqrt2}$
【解】
**（I）求 $f(x)$。**
**① 作变量替换构造方程组。** 令 $t=\dfrac1x$，原方程化为
$$2f\!\left(\frac1t\right)+t f(t)=\frac{3\sqrt{1+t^2}}{t},$$
即对任意 $x>0$ 有
$$\begin{cases}2f(x)+x f\!\left(\frac1x\right)=3\sqrt{1+x^2},\\[3pt]2f\!\left(\frac1x\right)+\dfrac1x f(x)=\dfrac{3\sqrt{1+x^2}}{x}.\end{cases}$$
**② 消去 $f(1/x)$。** 第二式乘 $x$ 得 $2x f(1/x)+f(x)=3\sqrt{1+x^2}$，与第一式乘 $2$ 相消，解得 $f(x)=\sqrt{1+x^2}$。
**（II）求面积最小的切线。**
**① 写出切线方程。** 设切点为 $\left(t,\sqrt{1+t^2}\right)$，由 $f'(x)=\dfrac{x}{\sqrt{1+x^2}}$ 得切线
$$y-\sqrt{1+t^2}=\frac{t}{\sqrt{1+t^2}}(x-t),\quad\text{即}\quad y=\frac{t}{\sqrt{1+t^2}}x+\frac{1}{\sqrt{1+t^2}}.$$
**② 写出面积函数。** 曲线在切线上方，故
$$S(t)=\int_0^2\!\left[\sqrt{1+x^2}-\frac{t}{\sqrt{1+t^2}}x-\frac{1}{\sqrt{1+t^2}}\right]\mathrm{d}x=\int_0^2\sqrt{1+x^2}\,\mathrm{d}x-\frac{2t+2}{\sqrt{1+t^2}}.$$
**③ 求最小值。** 求导得 $S'(t)=\dfrac{2t-2}{(1+t^2)^{3/2}}$，唯一驻点 $t=1$；$0<t<1$ 时 $S'<0$、$t>1$ 时 $S'>0$，故 $t=1$ 处取最小值。此时切线为 $y=\dfrac{1}{\sqrt2}x+\dfrac{1}{\sqrt2}$。
【思路】(I) 用 $x\leftrightarrow1/x$ 联立方程组消元；(II) 设切点写出切线，把围成面积写成切点参数的函数，求导找最小点。
【易错】换元后第二式右端是 $\frac{3\sqrt{1+t^2}}{t}$ 而非 $3\sqrt{1+t^2}$，需先把 $t$ 换回 $1/x$ 再整理；面积积分中的常数项 $\int_0^2\sqrt{1+x^2}dx$ 与切点无关，求导时可整体看作常数。

===Q19===
【答案】极大值 $f(4,-4)=64$，$(0,0)$ 不是极值点
【解】
**① 由混合偏导求 $f_x$。** 由 $\dfrac{\partial^2f}{\partial x\partial y}=-6$ 对 $y$ 积分得 $f_x=-6y+C_1(x)$；代入 $\left.f_x\right|_{(x,0)}=6x-3x^2$ 得 $C_1(x)=6x-3x^2$，故
$$f_x=-6y+6x-3x^2.$$
**② 积分求 $f$。** 对 $x$ 积分得 $f=-6xy+3x^2-x^3+C_2(y)$；代入 $f(0,y)=y^3+3y^2$ 得 $C_2(y)=y^3+3y^2$，故
$$f(x,y)=3x^2+3y^2-x^3+y^3-6xy.$$
**③ 求驻点。** 令
$$f_x=6(x-y)-3x^2=0,\qquad f_y=6(y-x)+3y^2=0,$$
两式相加得 $3(y^2-x^2)=0$，解得 $(4,-4)$ 与 $(0,0)$。
**④ 判别驻点。** $f_{xx}=6-6x$、$f_{xy}=-6$、$f_{yy}=6+6y$。在 $(4,-4)$ 处 $A=-18,\ B=-6,\ C=-18$，$AC-B^2=288>0$ 且 $A<0$，故为极大值点，$f(4,-4)=64$。在 $(0,0)$ 处 $A=6,B=-6,C=6$，$AC-B^2=0$，判别法失效。沿曲线 $y=x+kx^2$，
$$f(x,x+kx^2)=3(k^2+k)x^4+o(x^4),$$
取 $k=1$ 时为正、取 $k=-\dfrac12$ 时为负，故 $(0,0)$ 非极值点。
【思路】由混合偏导条件逐次积分并用边界条件定出 $f$，解驻点方程后用二阶判别法；判别失效时沿曲线 $y=x+kx^2$ 比较函数值符号。
【易错】$AC-B^2=0$ 时不能断定是极值点，必须进一步分析；本题沿不同 $k$ 值的抛物线方向函数值异号，恰好说明不是极值。

===Q20===
【答案】$\dfrac14(e-1)$
【解】
**① 用轮换对称性化简。** 区域 $D=\{x\ge0,\ y\ge0,\ x+y\le1\}$ 关于 $y=x$ 对称，故
$$I=\frac12\iint_D\frac{(x+y)e^{(x+y)^2}}{x+y}\,dxdy=\frac12\iint_D e^{(x+y)^2}\,dxdy.$$
**② 用极坐标计算。** $x+y=r(\cos\theta+\sin\theta)$，边界 $x+y=1$ 对应 $r=\dfrac1{\cos\theta+\sin\theta}$，于是
$$I=\frac12\int_0^{\frac\pi2}\mathrm{d}\theta\int_0^{\frac1{\cos\theta+\sin\theta}}e^{r^2(\cos\theta+\sin\theta)^2}\,r\,\mathrm{d}r=\frac14(e-1)\int_0^{\frac\pi2}\frac{\mathrm{d}\theta}{(\cos\theta+\sin\theta)^2}.$$
**③ 完成单积分。** 由 $(\cos\theta+\sin\theta)^2=2\sin^2\!\left(\theta+\dfrac\pi4\right)$，
$$\int_0^{\frac\pi2}\frac{\mathrm{d}\theta}{(\cos\theta+\sin\theta)^2}=\frac12\left[-\cot\!\left(\theta+\frac\pi4\right)\right]_0^{\frac\pi2}=\frac12\left[-\cot\frac{3\pi}{4}+\cot\frac\pi4\right]=1,$$
故 $I=\dfrac14(e-1)$。
【思路】先利用轮换对称性把非对称的 $x$ 换成 $\frac{x+y}{2}$ 消去分母，再用极坐标把指数化为 $r$ 的函数先积 $r$ 后积 $\theta$。
【易错】轮换对称性要求区域关于 $y=x$ 对称，本题三角域满足；$\frac{x}{x+y}$ 与 $\frac{y}{x+y}$ 在对称区域上积分相等，二者之和为 $1$，故各占一半。

===Q21===
【答案】(I) 存在 $\xi\in(0,x)$ 使 $[f'(\xi)]^2\le\dfrac1{x^2}$；(II) $[f'(0)]^2\le2$
【解】
**（I）证明存在 $\xi$。**
**① 用拉格朗日中值定理。** 对固定的 $x\in(0,1)$，存在 $\xi\in(0,x)$ 使
$$f'(\xi)=\frac{f(x)-f(0)}{x}=\frac{f(x)-1}{x}.$$
**② 用条件夹住 $f'(\xi)$。** 由 $f(x)\ge0$ 得 $\dfrac{f(x)-1}{x}\ge-\dfrac1x$；由 $f'(x)\le0$ 知 $f$ 递减，故 $f(x)\le f(0)=1$，即 $\dfrac{f(x)-1}{x}\le0$。于是 $-\dfrac1x\le f'(\xi)\le0$，平方得 $[f'(\xi)]^2\le\dfrac1{x^2}$。
**（II）证明 $[f'(0)]^2\le2$。**
**① 构造辅助函数。** 令 $F(x)=[f'(x)]^2-[f(x)]^2$，则
$$F'(x)=2f'(x)f''(x)-2f(x)f'(x)=2f'(x)\left[f''(x)-f(x)\right]\ge0,$$
因为 $f'(x)\le0$ 且 $f''(x)-f(x)\le0$。故 $F$ 在 $[0,1]$ 上单调递增，$F(\xi)\ge F(0)$。
**② 代入估计。** 由 $F(\xi)\ge F(0)$ 得
$$[f'(\xi)]^2-[f(\xi)]^2\ge[f'(0)]^2-[f(0)]^2=[f'(0)]^2-1,$$
即
$$[f'(0)]^2\le[f'(\xi)]^2-[f(\xi)]^2+1\le\frac1{x^2}+1.$$
取 $x=1$ 即得 $[f'(0)]^2\le2$。
【思路】(I) 拉格朗日中值定理把 $f'(\xi)$ 写成差商，用 $0\le f\le1$ 夹逼；(II) 构造 $F=(f')^2-f^2$，由 $F'\ge0$ 得单调性，把 $F(\xi)\ge F(0)$ 与 (I) 的估计结合后取 $x=1$。
【易错】$F'$ 的因子 $2f'(x)\le0$ 与 $f''-f\le0$ 相乘为非负，单调方向不能弄反；最后取 $x=1$ 是因为 $\frac1{x^2}+1$ 随 $x$ 增大而减小，最大值在最小的 $x=1$ 处取得。

===Q22===
【答案】(I) 正定；(II) $P=\begin{pmatrix}\dfrac1{\sqrt2}&\dfrac1{\sqrt6}&\dfrac1{2\sqrt3}\\0&\dfrac2{\sqrt6}&\dfrac1{\sqrt3}\\0&0&\dfrac{\sqrt3}{2}\end{pmatrix}$，规范型 $f=z_1^2+z_2^2+z_3^2$
【解】
**（I）证明正定。**
**① 写顺序主子式递推。** 二次型矩阵 $A$ 的主对角元为 $2$，相邻非对角元为 $-1$，记 $D_k$ 为 $k$ 阶顺序主子式，则
$$D_n=2D_{n-1}-D_{n-2},\qquad D_1=2,\ D_2=3,\ D_3=4.$$
**② 解递推。** 由 $D_n-D_{n-1}=D_{n-1}-D_{n-2}=\cdots=D_2-D_1=1$，得 $D_n=D_1+(n-1)=n+1>0$。各阶顺序主子式全为正，由西尔维斯特判别法知 $f$ 正定。
**（II）$n=3$ 时化为规范型。**
**① 配方。** 此时 $f=2x_1^2+2x_2^2+2x_3^2-2x_1x_2-2x_2x_3$，逐次配方得
$$f=2\!\left(x_1-\frac12x_2\right)^2+\frac32x_2^2+2x_3^2-2x_2x_3=2\!\left(x_1-\frac12x_2\right)^2+\frac32\!\left(x_2-\frac23x_3\right)^2+\frac43x_3^2.$$
**② 写出可逆变换。** 令
$$z_1=\sqrt2\!\left(x_1-\frac12x_2\right),\quad z_2=\sqrt{\frac32}\!\left(x_2-\frac23x_3\right),\quad z_3=\frac2{\sqrt3}x_3,$$
反解得 $x=Pz$，其中
$$P=\begin{pmatrix}\dfrac1{\sqrt2}&\dfrac1{\sqrt6}&\dfrac1{2\sqrt3}\\[3pt]0&\dfrac2{\sqrt6}&\dfrac1{\sqrt3}\\[3pt]0&0&\dfrac{\sqrt3}{2}\end{pmatrix},$$
$P$ 为上三角且对角元均非零，故可逆。在此变换下 $f=z_1^2+z_2^2+z_3^2$ 为规范型。
【思路】(I) 建立三对角行列式递推 $D_n=2D_{n-1}-D_{n-2}$ 得 $D_n=n+1>0$；(II) 用拉格朗日配方法逐次消去交叉项，取平方根定义新变量得到可逆变换与规范型。
【易错】三对角行列式递推的初值是 $D_1=2,D_2=3$（不是 $D_0=1$ 直接套用会差一项）；规范型要求系数只为 $1$ 或 $-1$，故需把配方系数开方并入新变量，而不能停在 $2z_1^2+\frac32z_2^2+\frac43z_3^2$。
