===Q1===
【答案】B
【解】
**① 分离因子并套莱布尼茨公式。** 令 $g(x)=xe^x$，则 $f(x)=(x-1)^n g(x)$。由莱布尼茨公式（只写出首两项与末项）
$$f^{(2n)}(x)=C_{2n}^0(x-1)^n g^{(2n)}(x)+C_{2n}^1 n(x-1)^{n-1}g^{(2n-1)}(x)+\cdots+C_{2n}^n n!\,g^{(n)}(x),$$
除末项外各项都含因子 $(x-1)$，代入 $x=1$ 均为零，故
$$f^{(2n)}(1)=C_{2n}^n n!\,g^{(n)}(1).$$
**② 求 $g^{(n)}(1)$ 并定选项。** 对 $g(x)=x\cdot e^x$ 再用莱布尼茨公式：$g^{(n)}(x)=C_n^0xe^x+C_n^1e^x=xe^x+ne^x$，故 $g^{(n)}(1)=(n+1)e$。于是
$$f^{(2n)}(1)=C_{2n}^n n!(n+1)e=C_{2n}^n(n+1)!\,e,$$
选 (B)。
【思路】把 $(x-1)^n$ 与 $xe^x$ 分离，两次用莱布尼茨公式，只保留 $x=1$ 处的非零项。
【易错】题干求的是 $f^{(2n)}(1)$（$2n$ 阶导数）而非 $f^{(n)}(1)$，漏看阶数会误选 (A)；原册莱布尼茨展开只列首两项与末项，中间项系数应补为 $C_{2n}^k\dfrac{n!}{(n-k)!}(x-1)^{n-k}g^{(2n-k)}(x)$，属简写而非完整通项。

===Q2===
【答案】B
【解】
**① 判断命题①。** 由达布定理（导数介值定理），$f'(x)\ne0$ 时 $f'(x)$ 不能变号，故在 $(-\infty,+\infty)$ 内恒正或恒负，$f(x)$ 单调，①正确。
**② 判断命题②。** 反例：取 $x_1=1,\ x_{n+1}=\dfrac{x_n}{2}$，即 $f(x)=\dfrac x2$，$f'(x)=\dfrac12>0$，但数列 $\{x_n\}$ 严格单调减少，②错误。
**③ 判断命题③。** 反例：$f(x)=x^3$ 在 $(-\infty,+\infty)$ 内单调增加，但 $f'(0)=0$，故 $f'(x)>0$ 只是充分条件而非必要条件，③错误。
**④ 判断命题④。** 若 $f(x)=0$ 有三个根，由罗尔定理存在不同的 $\xi_1,\xi_2$ 使 $f'(\xi_1)=f'(\xi_2)=0$，与 $f'(x)$ 单调增加矛盾，故至多有两个根，④正确。
正确命题共 2 个（①④），选 (B)。
【思路】用达布定理与罗尔定理肯定①④，用两个反例否定②③。
【易错】最易把「$f'(x)>0$」当作单调增加的充要条件（③）；②中 $f'(x)>0$ 也不能保证迭代数列单调增，还依赖初值。

===Q3===
【答案】D
【解】
**① 由凹性列出面积不等式。** $f''(x)<0$ 表明曲线上凸（凹），曲线在弦之上、在切线之下。以 $\frac{a+b}{2}$ 分两段作梯形、并作中点处切线：
$$\left[f(a)+f\!\left(\frac{a+b}{2}\right)\right]\frac{b-a}{4}+\left[f(b)+f\!\left(\frac{a+b}{2}\right)\right]\frac{b-a}{4}<\int_a^b f(x)\,\mathrm{d}x,$$
$$\int_a^b f(x)\,\mathrm{d}x<\int_a^b\left[f\!\left(\frac{a+b}{2}\right)+f'\!\left(\frac{a+b}{2}\right)\left(x-\frac{a+b}{2}\right)\right]\mathrm{d}x.$$
**② 化简得结论。** 左端合并、右端切线积分中一次项积分为零，得
$$\frac{f(a)+f(b)+2f\!\left(\frac{a+b}{2}\right)}{4}<\frac{1}{b-a}\int_a^b f(x)\,\mathrm{d}x<f\!\left(\frac{a+b}{2}\right),$$
故选 (D)（原册标注「证明 如图 2 知」，图 2 即凹函数、梯形与切线的示意图）。
【思路】用 $f''<0$ 的凹性，把积分平均值夹在「两段梯形面积」与「中点切线下面积」之间。
【易错】记反凹向：$f''<0$ 时弦在曲线下方、切线在曲线上方，不等号方向弄反会误选 (A)(C)；题干「非负函数」条件在本证明中未用到。

===Q4===
【答案】A
【解】
**① 写成和式并夹逼。** 设
$$x_n=\sum_{k=1}^{2n}\frac{\sqrt k}{n\sqrt{n+\frac1k}},$$
由 $n\le n+\frac1k\le n+1$ 得
$$\sum_{k=1}^{2n}\frac{\sqrt k}{n\sqrt{n+1}}\le x_n\le\sum_{k=1}^{2n}\frac{\sqrt k}{n\sqrt n}.$$
**② 两端化为定积分。** 上界：
$$\lim_{n\to\infty}\sum_{k=1}^{2n}\frac{\sqrt k}{n\sqrt n}=\lim_{n\to\infty}\frac1n\sum_{k=1}^{2n}\sqrt{\frac kn}=\int_0^2\sqrt x\,\mathrm{d}x=\frac{4\sqrt2}{3};$$
下界：
$$\lim_{n\to\infty}\sum_{k=1}^{2n}\frac{\sqrt k}{n\sqrt{n+1}}=\lim_{n\to\infty}\frac{\sqrt n}{\sqrt{n+1}}\cdot\frac1n\sum_{k=1}^{2n}\sqrt{\frac kn}=\frac{4\sqrt2}{3}.$$
由夹逼定理 $\lim\limits_{n\to\infty}x_n=\dfrac{4\sqrt2}{3}$，选 (A)。
【思路】把和式写成 $\frac1n\sum\sqrt{k/n}$ 的黎曼和，积分区间是 $[0,2]$ 而非 $[0,1]$。
【易错】求和上限是 $2n$，对应 $\int_0^2\sqrt x\,\mathrm{d}x=\frac{4\sqrt2}{3}$；误按 $[0,1]$ 计算会得 $\frac23$ 而错选。

===Q5===
【答案】B
【解】
**① 求 $x\to-\infty$ 的水平渐近线。**
$$\lim_{x\to-\infty}f(x)=\lim_{x\to-\infty}\left(\sqrt{x^2+\sin^2x}+x\right)=\lim_{x\to-\infty}\frac{\sin^2x}{\sqrt{x^2+\sin^2x}-x}=0,$$
故有一条水平渐近线 $y=0$。
**② 求 $x\to+\infty$ 的斜渐近线。**
$$\lim_{x\to+\infty}\frac{f(x)}{x}=\lim_{x\to+\infty}\left(\frac{\sqrt{x^2+\sin^2x}}{x}+1\right)=\lim_{x\to+\infty}\sqrt{1+\left(\frac{\sin x}{x}\right)^2}+1=2,$$
$$\lim_{x\to+\infty}\big[f(x)-2x\big]=\lim_{x\to+\infty}\left(\sqrt{x^2+\sin^2x}-x\right)=\lim_{x\to+\infty}\frac{\sin^2x}{\sqrt{x^2+\sin^2x}+x}=0,$$
故有一条斜渐近线 $y=2x$。合计一条水平渐近线、一条斜渐近线，选 (B)。
【思路】分 $x\to+\infty$ 与 $x\to-\infty$ 两侧求渐近线，用分子有理化处理 $\sqrt{x^2+\sin^2x}\pm x$。
【易错】$\sqrt{x^2}=|x|$：$x\to-\infty$ 时给出水平渐近线 $y=0$，$x\to+\infty$ 时才给出斜率 2；漏掉负向讨论会误选 (D)。根号内是 $\sin^2x$（题干与解一致），不是 $\sin^4x$。

===Q6===
【答案】B
【解】
**① 由第一式求 $f_1'(0,0)$。** 由题设 $f(0,0)=0$。对 $f(x,x^2)=2xe^x$ 两边对 $x$ 求导：
$$f_1'(x,x^2)+2x f_2'(x,x^2)=2e^x+2xe^x,$$
令 $x=0$ 得 $f_1'(0,0)=2$。
**② 由第二式求 $f_2'(0,0)$。** 对 $f\big(x^2-1,\,f(x-1,\ln x)\big)=x^3$ 求导：
$$2x f_1'(x^2-1,f)+f_2'(x^2-1,f)\left[f_1'(x-1,\ln x)+\frac{f_2'(x-1,\ln x)}{x}\right]=3x^2,$$
令 $x=1$ 得
$$2f_1'(0,0)+f_2'(0,0)\big[f_1'(0,0)+f_2'(0,0)\big]=3,$$
代入 $f_1'(0,0)=2$ 解得 $f_2'(0,0)=-1$。
**③ 写全微分。** $\mathrm{d}f(0,0)=f_1'(0,0)\,\mathrm{d}x+f_2'(0,0)\,\mathrm{d}y=2\mathrm{d}x-\mathrm{d}y$，选 (B)。
【思路】对两个复合函数等式分别求全导数，再取特殊点 $x=0$ 与 $x=1$ 解出两个偏导。
【易错】第二式必须代入 $x=1$（使 $x^2-1=0,\ \ln x=0$），不能代 $x=0$（$\ln x$ 无定义）；内层 $f(x-1,\ln x)$ 的导数含 $\frac1x$ 因子。

===Q7===
【答案】B
【解】
**① 化为直角坐标累次积分。** 极坐标下 $r^3\sin^2\theta\,\mathrm{d}r\,\mathrm{d}\theta=y^2\cdot r\,\mathrm{d}r\,\mathrm{d}\theta$，即被积函数为 $y^2$；两段上限 $\frac{1}{\sin\theta+2\cos\theta}$ 与 $\frac{1}{\sin\theta-\cos\theta}$ 分别对应直线 $2x+y=1$ 与 $y-x=1$，合起来区域为 $0\le y\le1,\ y-1\le x\le\frac{1-y}{2}$。
**② 计算。**
$$I=\int_0^1\mathrm{d}y\int_{y-1}^{\frac{1-y}{2}}y^2\,\mathrm{d}x=\frac32\int_0^1(y^2-y^3)\,\mathrm{d}y=\frac18,$$
选 (B)。
【思路】把 $r^3\sin^2\theta$ 认作 $y^2\,\mathrm{d}\sigma$，将两条极坐标边界还原成直线后交换积分次序。
【易错】勿把被积函数误看成 $r^3\sin\theta$；第二段上限是 $\frac{1}{\sin\theta-\cos\theta}$（对应 $x\ge y-1$），若误读成 $\frac{1}{\sin\theta-2\cos\theta}$ 会算成 $\frac1{12}$ 而错选 (A)。

===Q8===
【答案】A
【解】
**① 命题①。** 若 $A^3x=0$ 与 $A^4x=0$ 有不同解，则存在三维非零列向量 $\alpha$ 使 $A^3\alpha\ne0,\ A^4\alpha=0$；此时 $\alpha,A\alpha,A^2\alpha,A^3\alpha$ 既线性无关、又是 4 个三维向量（必线性相关），矛盾，故 $r(A^3)=r(A^4)$，①正确。
**② 命题②。** 由 $r(AB)=r(BA)+1$ 得 $r(BA)\le1$，故
$$r(ABA)+r(BAB)\le r(BA)+r(BA)\le2,$$
②正确。
**③ 命题③。** 由 $r(A+E)+r(-A)\ge r(E)=3$ 及 $r(A)=1$ 得 $r(A+E)\ge2$，③正确。
**④ 命题④。** 一方面 $r(ABB^T)\le r(AB)$；另一方面 $r(ABB^T)\ge r(ABB^TA^T)=r\big(AB(AB)^T\big)=r(AB)$，故两者相等，④正确。
四个命题全正确，选 (A)。
【思路】依次用「幂次矩阵零空间稳定」、秩不等式、Sylvester 不等式（取 $A+E$ 与 $-A$）、以及 $r(MM^T)=r(M)$ 判定。
【易错】④ 的关键是 $r(MM^T)=r(M)$；③ 中 Sylvester 不等式常写成 $r(X+Y)\ge r(X)+r(Y)-n$，此处 $n=3$。

===Q9===
【答案】B
【解】
**① 由基础解系读出秩与关系。** $Ax=0$ 的基础解系为 $(2,0,2,7)^T$，故 $r(A)=4-1=3$，且 $2\alpha_1+2\alpha_3+7\alpha_4=\boldsymbol 0$。
**② 逐项判断。** $\alpha_2$ 与 $\alpha_1,\alpha_3,\alpha_4$ 中任取两不同向量都构成 $\alpha_1,\alpha_2,\alpha_3,\alpha_4$ 的极大无关组，故 (A) 正确；若 $\alpha_2$ 可由 $\alpha_1,\alpha_3,\alpha_4$ 线性表示，则 $r(A)\le2$，与 $r(A)=3$ 矛盾，故 (B) 错误；由正定定义验证 $AA^T$ 正定，(C) 正确；$r(A)=3$ 等于行数，对任意三维列向量 $\boldsymbol b$ 有 $r(A,\boldsymbol b)=3$，故 $Ax=\boldsymbol b$ 必有解，(D) 正确。
说法错误的是 (B)，选 (B)。
【思路】由基础解系含 1 个向量得 $r(A)=3$，再用列向量组的秩逐项排除。
【易错】$A$ 是 $3\times4$，$r(A)=3$ 是行满秩（对任意三维 $\boldsymbol b$，$Ax=\boldsymbol b$ 有解），但列向量组必线性相关；易把「行满秩」误当「列满秩」而错判 (D)。

===Q10===
【答案】C
【解】
**① 判定 (B)(D)。** 由 $\alpha^TA\alpha>0,\ \beta^TA\beta<0$ 知二次型 $x^TAx$ 既取正值又取负值，$A$ 的特征值有正有负，规范形为 $y_1^2-y_2^2$，故 $A$ 与 $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ 合同，且存在非零列向量 $\gamma$ 使 $\gamma^TA\gamma=0$，(B)(D) 正确。
**② 判定 (A)。** 条件已保证 $\alpha,\beta$ 皆非零；若线性相关则 $\alpha=k\beta\ (k\ne0)$，于是 $\alpha^TA\alpha=k^2\beta^TA\beta<0$，与 $\alpha^TA\alpha>0$ 矛盾，故 $\alpha,\beta$ 线性无关，(A) 正确。
**③ 判定 (C)。** 规范形只说明惯性指数为 $(1,1)$，并不要求 $\alpha,\beta$ 正交，(C) 错误。选 (C)。
【思路】由二次型取正、负值判定 $A$ 不定，再逐项验证线性无关、合同、正交与存在零值向量。
【易错】「$\alpha^TA\alpha>0,\ \beta^TA\beta<0$」只能推出 $\alpha,\beta$ 线性无关，推不出 $\alpha^T\beta=0$；把「不定」误当成「$\alpha\perp\beta$」是最大陷阱。

===Q11===
【答案】$\left(\dfrac53,-\dfrac23\right)$
【解】
**① 把条件写成极限并拆项。** 由 $(a+b\cos x)\arctan x=x+o(x^3)$ 得
$$\lim_{x\to0}\frac{(a+b\cos x)\arctan x-x}{x^3}=0,$$
即
$$\lim_{x\to0}\left(\frac{a+b\cos x-1}{x^2}\cdot\frac{\arctan x}{x}+\frac{\arctan x-x}{x^3}\right)=0.$$
**② 求标准极限。** 由洛必达法则
$$\lim_{x\to0}\frac{\arctan x-x}{x^3}=\lim_{x\to0}\frac{\frac1{1+x^2}-1}{3x^2}=-\frac13,$$
故 $\lim\limits_{x\to0}\dfrac{a+b\cos x-1}{x^2}=\dfrac13$；由极限有限还须 $a+b=1$。
**③ 解出 $a,b$。**
$$\frac13=\lim_{x\to0}\frac{b\cos x-b}{x^2}=-b\lim_{x\to0}\frac{1-\cos x}{x^2}=-\frac12 b,$$
得 $b=-\dfrac23,\ a=\dfrac53$。
【思路】把 $o(x^3)$ 条件拆成两个标准极限，先定 $a+b$，再用 $\arctan x-x\sim-\frac{x^3}{3}$ 定 $b$。
【易错】拆项时须保证 $\frac{a+b\cos x-1}{x^2}$ 极限存在，故必有 $a+b=1$；以及 $\arctan x-x\sim-\frac13x^3$ 的系数符号。

===Q12===
【答案】$\dfrac{3}{16}\pi^2$
【解】
**① 用对称性转化。** $y=g(x)$ 是 $y=\sin^2x,\ x\in\left[\frac\pi2,\pi\right]$ 的反函数；由对称性，曲线 $y=g(x)$ 与 $y$ 轴、直线 $y=\frac\pi2$ 围成图形绕 $y$ 轴旋转的体积，等于 $y=\sin^2x$ 与 $x$ 轴、直线 $x=\frac\pi2$ 围成图形绕 $x$ 轴旋转的体积。
**② 用 Wallis 公式计算。**
$$V=\int_{\frac\pi2}^{\pi}\pi\sin^4x\,\mathrm{d}x=\pi\int_0^{\frac\pi2}\sin^4x\,\mathrm{d}x=\pi\cdot\frac34\cdot\frac12\cdot\frac\pi2=\frac{3}{16}\pi^2.$$
【思路】利用反函数与原函数关于 $y=x$ 的对称性，把绕 $y$ 轴的体积换成绕 $x$ 轴的 $\pi\int y^2\,\mathrm{d}x$。
【易错】被积函数是 $\pi y^2=\pi\sin^4x$（因原函数是 $y=\sin^2x$），不是 $\pi\sin^2x$；Wallis 结果 $\int_0^{\pi/2}\sin^4x\,\mathrm{d}x=\frac{3\pi}{16}$。

===Q13===
【答案】$e^y$
【解】
**① 求偏导并代入方程。** 由 $z=f(x+g(y))$ 得 $\frac{\partial z}{\partial x}=f'$，$\frac{\partial z}{\partial y}=f'\cdot g'$，代入 $g(y)\frac{\partial z}{\partial x}-\frac{\partial z}{\partial y}=0$ 得
$$g\cdot f'-f'\cdot g'=0.$$
**② 解微分方程。** 因 $f'>0$ 可约去 $f'$，得 $g'-g=0$，通解 $g(y)=Ce^y$；由 $g(0)=1$ 得 $C=1$，故 $g(y)=e^y$。
【思路】链式法则求偏导后，方程化为关于 $g$ 的一阶线性微分方程。
【易错】必须借助 $f'(x)>0$ 才能约去 $f'$；漏用 $g(0)=1$ 会保留任意常数 $C$。

===Q14===
【答案】$\dfrac12$
【解】
**① 换序并夹逼。** 记 $M(a)=\int_0^a\mathrm{d}x\int_{\frac x2}^{x}e^{-y^2}\mathrm{d}y$（图 3 中区域介于 $y=\frac x2$ 与 $y=x$ 之间）。交换积分次序，由 $x\in[y,2y]$ 得
$$\int_0^{\frac a2}\mathrm{d}y\int_y^{2y}e^{-y^2}\mathrm{d}x\le M(a)\le\int_0^{a}\mathrm{d}y\int_y^{2y}e^{-y^2}\mathrm{d}x.$$
**② 计算两端。** 下界 $=\int_0^{a/2}ye^{-y^2}\mathrm{d}y=\frac12\left(1-e^{-a^2/4}\right)\to\frac12$；上界 $=\int_0^{a}ye^{-y^2}\mathrm{d}y=\frac12\left(1-e^{-a^2}\right)\to\frac12$（$a\to+\infty$）。
**③ 夹逼得结论。** 由夹逼定理
$$\lim_{a\to+\infty}\int_0^a\mathrm{d}x\int_{\frac x2}^{x}e^{-y^2}\mathrm{d}y=\frac12.$$
【思路】把无法初等积分的 $e^{-y^2}$ 累次积分换序，用夹逼定理求 $a\to+\infty$ 的极限。
【易错】极限是 $a\to+\infty$ 而非 $a\to0$，外层积分上限是 $a$。原册第 89 页首行把上界累次积分的外层微分误印成 $\mathrm{d}x$（应为 $\mathrm{d}y$），与第 87 页不等式链中的 $\int_0^a\mathrm{d}y\int_y^{2y}e^{-y^2}\mathrm{d}x$ 不一致，属排印笔误，按 $\mathrm{d}y$ 理解即可。

===Q15===
【答案】$\ln\left|\sec\dfrac yx+\tan\dfrac yx\right|=x-1$
【解】
**① 化为齐次方程并换元。** 原方程等价于
$$\frac{xy'-y}{x^2}=\cos\frac yx,\quad\text{即}\quad\left(\frac yx\right)'=\cos\frac yx.$$
令 $z=\dfrac yx$，得 $\dfrac{\mathrm{d}z}{\mathrm{d}x}=\cos z$，即 $\sec z\,\mathrm{d}z=\mathrm{d}x$。
**② 积分并定常数。** 通解为 $\ln|\sec z+\tan z|=x+C$，即 $\ln\left|\sec\frac yx+\tan\frac yx\right|=x+C$；代入 $y(1)=0$（即 $z=0$）得 $C=-1$，故特解为 $\ln\left|\sec\frac yx+\tan\frac yx\right|=x-1$。
【思路】识别为齐次方程，用 $z=y/x$ 化为可分离变量方程。
【易错】$\int\sec z\,\mathrm{d}z=\ln|\sec z+\tan z|$ 的绝对值与形式；特解是隐式表达式，勿漏绝对值与常数 $C=-1$。

===Q16===
【答案】$a=2$
【解】
**① 由条件锁定重特征值。** 「线性无关特征向量个数小于 3」即 $A$ 不可对角化，故必有重特征值。由
$$A=\begin{pmatrix}4&a&1\\0&a+3&0\\a-3&-a&a\end{pmatrix},\qquad |\lambda E-A|=(\lambda-a-3)(\lambda-3)(\lambda-a-1),$$
全体特征值为 $a+3,\ 3,\ a+1$；重根只能是 $a=0$（$a+3=3$）或 $a=2$（$a+1=3$）。
**② 用几何重数筛选。** $a=0$ 时 $r(A-3E)=1$，特征值 3 有两个线性无关特征向量，$A$ 可对角化，不合题意；$a=2$ 时 $r(A-3E)=2$，几何重数为 1，不可对角化，满足题意。故 $a=2$。
【思路】先由不可对角化锁定重根，再用 $r(A-3E)$ 判断几何重数是否小于代数重数。
【易错】只解出 $a=0$ 或 $2$ 不够，必须用 $r(A-3E)$ 排除 $a=0$；由第二行 $[0,a+3,0]$ 可直接看出 $a+3$ 是一个特征值。

===Q17===
【答案】$e-2$
【解】
**① 凑微分并换元。**
$$\int_0^{\frac\pi2}\frac{e^{\sin x}\sin2x}{(1+\sin x)^2}\mathrm{d}x=2\int_0^{\frac\pi2}\frac{e^{\sin x}\sin x\cos x}{(1+\sin x)^2}\mathrm{d}x=2\int_0^{\frac\pi2}\frac{e^{\sin x}\sin x}{(1+\sin x)^2}\mathrm{d}(\sin x),$$
令 $t=\sin x$，得
$$2\int_0^1\frac{te^t}{(1+t)^2}\mathrm{d}t=-2\int_0^1te^t\,\mathrm{d}\!\left(\frac1{1+t}\right).$$
**② 分部积分求值。**
$$-\frac{2te^t}{1+t}\Big|_0^1+2\int_0^1 e^t\,\mathrm{d}t=-e+2(e-1)=e-2.$$
【思路】把 $\sin2x\,\mathrm{d}x$ 凑成 $2\sin x\,\mathrm{d}(\sin x)$，换元后对 $\frac{1}{(1+t)^2}$ 凑微分作分部积分。
【易错】$\sin2x=2\sin x\cos x$，其中 $\cos x\,\mathrm{d}x=\mathrm{d}(\sin x)$；分部积分项 $-\frac{2te^t}{1+t}\big|_0^1$ 易漏负号。

===Q18===
【答案】（I）$F'(x)=\begin{cases}\sin x,&0\le x<\frac\pi2\\\cos x,&\frac\pi2<x\le\pi\end{cases}$，且 $F(x)$ 在 $x=\frac\pi2$ 处不可导；（II）$g(x)$ 在 $(a,b)$ 内一定没有第一类间断点（证明见解）。
【解】
**（I）** $f(x)=\begin{cases}\sin x,&0\le x\le\frac\pi2\\\cos x,&\frac\pi2<x\le\pi\end{cases}$，$F(x)=\int_0^x f(t)\mathrm{d}t$。
**① 求分段点处右导数。**
$$F_+'\left(\frac\pi2\right)=\lim_{\Delta x\to0^+}\frac{\int_0^{\frac\pi2+\Delta x}f(t)\mathrm{d}t-\int_0^{\frac\pi2}f(t)\mathrm{d}t}{\Delta x}=\lim_{\Delta x\to0^+}\frac{\int_{\frac\pi2}^{\frac\pi2+\Delta x}\cos t\,\mathrm{d}t}{\Delta x}=\lim_{\Delta x\to0^+}\frac{\cos\left(\frac\pi2+\Delta x\right)}{1}=0.$$
**② 求分段点处左导数。**
$$F_-'\left(\frac\pi2\right)=\lim_{\Delta x\to0^-}\frac{\int_{\frac\pi2}^{\frac\pi2+\Delta x}\sin t\,\mathrm{d}t}{\Delta x}=\lim_{\Delta x\to0^-}\frac{\sin\left(\frac\pi2+\Delta x\right)}{1}=1.$$
左右导数不等，故 $F$ 在 $x=\frac\pi2$ 处不可导；其余点 $F'(x)=f(x)$，得 $F'(x)=\begin{cases}\sin x,&0\le x<\frac\pi2\\\cos x,&\frac\pi2<x\le\pi\end{cases}$。
**（II）** 反设 $g(x)$ 在 $(a,b)$ 内有第一类间断点 $x_0$，记 $\lim\limits_{x\to x_0^-}g(x)=A,\ \lim\limits_{x\to x_0^+}g(x)=B$。
**① 用拉格朗日中值定理求单侧导数。**
$$G_-'(x_0)=\lim_{x\to x_0^-}\frac{G(x)-G(x_0)}{x-x_0}=\lim_{x\to x_0^-}\frac{g(\xi)}{1}=A,\qquad G_+'(x_0)=\lim_{x\to x_0^+}\frac{G(x)-G(x_0)}{x-x_0}=\lim_{x\to x_0^+}\frac{g(\eta)}{1}=B$$
（$\xi,\eta$ 介于 $x$ 与 $x_0$ 之间）。
**② 由可导性推出矛盾。** 因 $G'(x_0)=g(x_0)$ 存在，故 $A=B=g(x_0)$，即 $\lim\limits_{x\to x_0}g(x)=g(x_0)$，$x_0$ 是连续点，与「第一类间断点」矛盾。故 $g(x)$ 在 $(a,b)$ 内没有第一类间断点。
【思路】（I）积分上限函数在分段点求左右导数；（II）导函数若有第一类间断点会与导数存在性（拉格朗日中值定理）矛盾。
【易错】$f$ 在 $x=\frac\pi2$ 处跳跃（左极限 1、右极限 0），故 $F$ 连续但不可导，$F'(x)$ 的分段区间必须去掉 $x=\frac\pi2$；原册右导数用 $\cos t$、左导数用 $\sin t$，与 $f$ 的定义自洽，勿把两者对调。

===Q19===
【答案】极大值 $z=1$（在 $\left(-\frac52,\frac12\right)$ 处），极小值 $z=-1$（在 $\left(\frac52,-\frac12\right)$ 处）。
【解】
**① 求一阶偏导与驻点。** 设 $F(x,y,z)=x^2+5y^2+7z^2+2xy+4xz-2$，则
$$\frac{\partial z}{\partial x}=-\frac{x+y+2z}{7z+2x},\qquad \frac{\partial z}{\partial y}=-\frac{5y+x}{7z+2x}.$$
令二者为 0，解得 $x=-5y,\ z=2y$，代回原方程得驻点 $\left(-\frac52,\frac12\right),\ \left(\frac52,-\frac12\right)$。
**② 求二阶偏导。** 记 $A=z_{xx},B=z_{xy},C=z_{yy}$，对隐函数再求导：
$$\frac{\partial^2z}{\partial x^2}=-\frac{(1+2z_x')(7z+2x)-(x+y+2z)\frac{\partial(7z+2x)}{\partial x}}{(7z+2x)^2},$$
$$\frac{\partial^2z}{\partial y^2}=-\frac{5(7z+2x)-(5y+x)\frac{\partial(7z+2x)}{\partial y}}{(7z+2x)^2},$$
$$\frac{\partial^2z}{\partial x\partial y}=-\frac{(1+2z_y')(7z+2x)-(x+y+2z)\frac{\partial(7z+2x)}{\partial y}}{(7z+2x)^2}.$$
**③ 判别极值。** 代入 $\left(-\frac52,\frac12\right)$ 得 $z=1,\ A=-\frac12,\ B=-\frac12,\ C=-\frac52$，$B^2-AC<0$ 且 $A<0$，取极大值 $z=1$；代入 $\left(\frac52,-\frac12\right)$ 得 $z=-1,\ A=\frac12,\ B=\frac12,\ C=\frac52$，$B^2-AC<0$ 且 $A>0$，取极小值 $z=-1$。
【思路】隐函数求一、二阶偏导，解出驻点后用 $B^2-AC$ 的符号判定极值。
【易错】原方程交叉项是 $2xy$（不是 $2xyz$），故 $F_x=2x+2y+4z$、$F_y=10y+2x$、$F_z=14z+4x$；判别式用 $B^2-AC<0$（等价于 $AC-B^2>0$）。

===Q20===
【答案】（I）$I(a)=\dfrac\pi{12}\left[8-8(1-a^2)^{3/2}-3a^4\right]$；（II）最大值为 $\dfrac{7-4\sqrt2}{3}\pi$（在 $a=\sqrt{2\sqrt2-2}$ 处取得）。
【解】
**（I）** 区域 $D=\{(x,y)\mid x^2+y^2\le a^2\},\ 0\le a\le1$。
**① 极坐标计算根式部分。**
$$\iint_D\sqrt{1-x^2-y^2}\,\mathrm{d}\sigma=\int_0^{2\pi}\mathrm{d}\theta\int_0^a r\sqrt{1-r^2}\,\mathrm{d}r=\pi\left[-\frac23(1-r^2)^{3/2}\right]_0^a=\frac23\pi\left[1-(1-a^2)^{3/2}\right].$$
**② 轮换对称性计算 $x^2$ 部分。**
$$\iint_D x^2\,\mathrm{d}\sigma=\iint_D\frac{x^2+y^2}{2}\,\mathrm{d}\sigma=\int_0^{2\pi}\mathrm{d}\theta\int_0^a\frac{r^2}{2}r\,\mathrm{d}r=\frac\pi4a^4.$$
**③ 合并。** $I(a)=\dfrac\pi{12}\left[8-8(1-a^2)^{3/2}-3a^4\right]$。
**（II）** $I(a)$ 定义域为 $[0,1]$，
$$I'(a)=\pi a\left[2\sqrt{1-a^2}-a^2\right].$$
令 $I'(a)=0$ 得 $a=0$ 或 $4-4a^2=a^4$，解得区间内驻点 $a=\sqrt{2\sqrt2-2}$；比较
$$I(0)=0,\quad I(1)=\frac5{12}\pi,\quad I\!\left(\sqrt{2\sqrt2-2}\right)=\frac{7-4\sqrt2}{3}\pi,$$
因 $\frac{7-4\sqrt2}{3}\pi>\frac5{12}\pi$，故 $I(a)$ 的最大值为 $\dfrac{7-4\sqrt2}{3}\pi$。
【思路】圆域上用极坐标加轮换对称性求出 $I(a)$ 的显式，再在 $[0,1]$ 上求一元函数最值。
【易错】$\int r\sqrt{1-r^2}\,\mathrm{d}r=-\frac13(1-r^2)^{3/2}$，勿漏 $\frac23$ 系数；比较端点 $a=1$ 与驻点值时 $\frac{7-4\sqrt2}{3}\approx0.448>\frac5{12}\approx0.417$，勿把 $I(1)$ 误当最大。

===Q21===
【答案】（I）$f(x)=0$ 在 $(0,1)$ 内至少有两个不同的实根；（II）存在 $\eta\in(0,1)$ 使 $\eta\big[f''(\eta)-f'(\eta)\big]=f''(\eta)-3f'(\eta)+2f(\eta)$。
【解】
**（I）** 令 $F(x)=\int_0^x f(t)\mathrm{d}t$，则 $F(0)=F(1)=0$。
**① 分部积分转化第二个条件。**
$$\int_0^1 f(x)g(x)\mathrm{d}x=\int_0^1 g(x)\,\mathrm{d}\big(F(x)\big)=F(x)g(x)\Big|_0^1-\int_0^1 F(x)g'(x)\mathrm{d}x=-\int_0^1 F(x)g'(x)\mathrm{d}x=0.$$
**② 中值定理加罗尔定理。** 由积分中值定理存在 $c\in(0,1)$ 使 $F(c)g'(c)=0$，又 $g'(c)\ne0$ 故 $F(c)=0$；在 $[0,c]$、$[c,1]$ 上分别用罗尔定理，存在 $x_1\in(0,c),\ x_2\in(c,1)$ 使 $F'(x_1)=F'(x_2)=0$，即 $f(x_1)=f(x_2)=0$。
**（II）**
**① 构造 $H$ 用罗尔定理。** 令 $H(x)=f(x)e^{-x}$，由（I）知 $H(x_1)=H(x_2)=0$，故存在 $\xi\in(x_1,x_2)$ 使 $H'(\xi)=0$，即 $f'(\xi)-f(\xi)=0$。
**② 构造 $G$ 再用罗尔定理。** 令 $G(x)=(x-1)^2\big[f'(x)-f(x)\big]$，有 $G(\xi)=G(1)=0$，故存在 $\eta\in(\xi,1)\subset(0,1)$ 使 $G'(\eta)=0$，展开即
$$\eta\big[f''(\eta)-f'(\eta)\big]=f''(\eta)-3f'(\eta)+2f(\eta).$$
【思路】（I）分部积分把 $\int fg=0$ 化为 $\int Fg'=0$，再用积分中值定理与罗尔定理；（II）连续两次构造辅助函数 $f(x)e^{-x}$ 与 $(x-1)^2(f'-f)$ 用罗尔定理。
【易错】$G(x)$ 的幂次是 $(x-1)^2$（不是 3 次），否则导出的系数会变成 $-4f'+3f$；$g'(x)\ne0$ 是从 $F(c)g'(c)=0$ 推出 $F(c)=0$ 的关键。

===Q22===
【答案】（I）$A$ 为实对称阵，$a=b=1$；（II）$Q=(\alpha_1,\alpha_2,\alpha_3)$，标准形 $y_1^2+2y_2^2+5y_3^2$；（III）最大值 $5$，在 $x=\pm\left(\frac{\sqrt6}{3},\frac{\sqrt6}{6},\frac{\sqrt6}{6}\right)^T$ 处取得。
【解】
**（I）** 由 $(A-A^T)(A^T-A)=O$ 即 $(A-A^T)(A-A^T)^T=O$，故 $A-A^T=O$，$A$ 为实对称阵；由
$$A=\begin{pmatrix}4&a&1\\1&2&1\\1&b&2\end{pmatrix}$$
对称得 $a=b=1$。
**（II）**
**① 求特征值。** $|\lambda E-A|=(\lambda-1)(\lambda-2)(\lambda-5)$，特征值为 $1,2,5$。
**② 求单位特征向量。** 分别对 $\lambda=1,2,5$ 解 $(\lambda E-A)x=0$，得
$$\alpha_1=\left(0,-\frac{\sqrt2}{2},\frac{\sqrt2}{2}\right)^T,\quad \alpha_2=\left(-\frac{\sqrt3}{3},\frac{\sqrt3}{3},\frac{\sqrt3}{3}\right)^T,\quad \alpha_3=\left(\frac{\sqrt6}{3},\frac{\sqrt6}{6},\frac{\sqrt6}{6}\right)^T.$$
**③ 写正交变换与标准形。** 取 $Q=(\alpha_1,\alpha_2,\alpha_3)$，则 $x=Qy$ 化标准形为 $y_1^2+2y_2^2+5y_3^2$。
**（III）** 因 $Q$ 为正交阵，$\|x\|=1$ 当且仅当 $\|y\|=1$；此时 $y_1^2+2y_2^2+5y_3^2$ 在 $y=(0,0,\pm1)^T$ 处取最大值 $5$，对应 $x=\pm\alpha_3=\pm\left(\frac{\sqrt6}{3},\frac{\sqrt6}{6},\frac{\sqrt6}{6}\right)^T$。
【思路】（I）用 $MM^T=O\Rightarrow M=O$ 证对称；（II）求特征值与单位特征向量得正交矩阵；（III）正交变换保范数，二次型最大值即最大特征值。
【易错】原册（III）把 $x$ 写成 $\left(\pm\frac{\sqrt6}{3},\pm\frac{\sqrt6}{6},\pm\frac{\sqrt6}{6}\right)^T$，三个 $\pm$ 应理解为同号（只有 $\pm\alpha_3$ 两个点），否则会误以为有 8 个取最大值的点；另 $Q$ 的列须按特征值 $1,2,5$ 的顺序排列，才对应标准形 $y_1^2+2y_2^2+5y_3^2$。
