===Q1===
【答案】A
【解】
**① 判型并提取公因子。** $\lim\limits_{x\to+\infty}\left[(x+a)^{1+\frac1x}-x^{1+\frac1x}\right]$ 为 $\infty-\infty$ 型，提出 $x^{1+\frac1x}$：
$$原式=\lim_{x\to+\infty}x^{1+\frac1x}\left[\left(1+\frac ax\right)^{1+\frac1x}-1\right]=\lim_{x\to+\infty}x^{\frac1x}\cdot\lim_{x\to+\infty}x\left[\left(1+\frac ax\right)^{1+\frac1x}-1\right]$$
**② 换元并用等价无穷小。** 由 $\lim\limits_{x\to+\infty}x^{\frac1x}=1$，令 $\frac1x=t\ (t\to0^+)$：
$$原式=\lim_{t\to0^+}\frac{(1+at)^{t+1}-1}{t}=\lim_{t\to0^+}\frac{e^{(t+1)\ln(1+at)}-1}{t}=\lim_{t\to0^+}\frac{(t+1)\ln(1+at)}{t}=\lim_{t\to0^+}\frac{at(t+1)}{t}=a$$
**③ 定参。** 由此得 $a=1$，A 正确。
【思路】把 $\infty-\infty$ 型极限改写为 $1^\infty$ 形式，换元后连续用 $e^u-1\sim u$、$\ln(1+at)\sim at$ 求出极限关于 $a$ 的表达式。
【易错】$x^{1+\frac1x}=x^{\frac1x}\cdot x$ 拆分后，因子 $x$ 必须与方括号配对保留；$e^{(t+1)\ln(1+at)}-1\sim(t+1)\ln(1+at)$ 的前提是指数整体趋于 $0$。

===Q2===
【答案】B
【解】
**① 求 $f(0)$ 与 $f'(0)$。** 由 $f(x)$ 有连续导数及 $\lim\limits_{x\to0}\frac{f(x)}{x}=6$，得 $f(0)=0$，$f'(0)=\lim\limits_{x\to0}\frac{f(x)-f(0)}{x-0}=6$。
**② 洛必达求核心极限。** 令 $F(x)=\int_0^x f(t)\,dt$，则 $F(0)=0,\ F'(0)=f(0)=0,\ F''(0)=f'(0)=6$，故
$$\lim_{x\to0}\frac{F(x)}{x^2}=\lim_{x\to0}\frac{F'(x)}{2x}=\frac12\lim_{x\to0}F''(x)=\frac12\lim_{x\to0}f'(x)=\frac12 f'(0)=3$$
**③ 复合自变量。** 令 $u=x^3$，则 $\lim\limits_{x\to0}\frac{F(x^3)}{x^6}=\lim\limits_{u\to0}\frac{F(u)}{u^2}=3$。
**④ 组合得结果。**
$$\lim_{x\to0}\frac{\int_0^{x^3}f(t)\,dt}{\left[\int_0^x f(t)\,dt\right]^3}=\lim_{x\to0}\frac{\frac{F(x^3)}{x^6}}{\left[\frac{F(x)}{x^2}\right]^3}=\frac{3}{3^3}=\frac19$$
B 正确。
【思路】用变限积分 $F(x)$ 把原式改写成 $\frac{F(x^3)}{x^6}\big/\left[\frac{F(x)}{x^2}\right]^3$，核心是洛必达求出 $\lim\frac{F(x)}{x^2}=3$。
【易错】分子分母须同除以 $x^6$ 才能凑出 $\left[\frac{F(x)}{x^2}\right]^3$；勿把 $f'(0)=6$ 直接当作 $\lim\frac{F(x)}{x^2}$（相差因子 $\frac12$）。原册小注：作为选择题可取特殊值 $f(x)=6x$，此时
$$\lim_{x\to0}\frac{\int_0^{x^3}f(t)\,dt}{\left[\int_0^x f(t)\,dt\right]^3}=\lim_{x\to0}\frac{3x^6}{(3x^2)^3}=\frac19$$

===Q3===
【答案】C
【解】
**① 排除 $l_1$。** 若 $l_1$ 是 $f(x)$ 的图形，则 $f(x)$ 在 $[0,1]$ 上单调增加且 $f(x)>0\ (x\in(0,1])$，故 $f'(x)\ge0,\ \int_0^x f(t)\,dt>0$；但 $l_3$ 中 $x$ 轴下方有图形，故 $l_1$ 不是 $y=f(x)$ 的图形，排除 A、B。
**② 判定 $l_2$。** 若 $l_2$ 是 $y=f(x)$ 的图形，则 $f(x)$ 有唯一最大值点 $x_0\in(0,1)$，在 $[0,x_0]$ 上单调增加、在 $[x_0,1]$ 上单调减少，且 $f(x)>0\ (x\in(0,1))$，从而 $\int_0^x f(t)\,dt>0$ 且单调增加，$l_1$ 满足要求；当 $x\in(0,x_0)$ 时 $f'(x)\ge0$，当 $x\in(x_0,1)$ 时 $f'(x_0)\le0,\ f'(x_0)=0$，$l_3$ 满足要求，故 C 正确。
**③ 排除 $l_3$。** 若 $l_3$ 是 $y=f(x)$ 的图形，则 $f(x)$ 在 $[0,1]$ 上单调减少，从而 $f'(x)\le0$，故 D 不正确。
【思路】利用 $f>0$ 时 $\int_0^x f$ 恒正且单调增加，以及 $f$ 的升降与 $f'$ 符号的对应关系，逐一排除三条候选曲线。
【易错】原册此解析中 $l_1$ 与 $l_3$ 编号多处混用（先写「$l_1$ 满足要求」，紧接又写「$l_3$ 满足要求」），且「当 $x\in(x_0,1)$ 时 $f'(x_0)\le0$」疑应为「$f'(x)\le0$」，属明显排印疑点，以上按原册照录。

===Q4===
【答案】A
【解】
**① 拆分积分区间。**
$$I=\int_0^1\frac{dx}{x^{p-1}(1-x)^{p+q}}+\int_1^{+\infty}\frac{dx}{x^{p-1}(x-1)^{p+q}}$$
记两项为 $I_1+I_2$。
**② $I_1$ 的收敛条件。** 当 $x\to0^+$ 时 $\frac{1}{x^{p-1}(1-x)^{p+q}}\sim\frac{1}{x^{p-1}}$；当 $x\to1^-$ 时 $\sim\frac{1}{(1-x)^{p+q}}$。故 $I_1$ 收敛要求 $p-1<1$ 且 $p+q<1$。
**③ $I_2$ 的收敛条件。** 当 $x\to1^+$ 时 $\frac{1}{x^{p-1}(x-1)^{p+q}}\sim\frac{1}{(x-1)^{p+q}}$；当 $x\to+\infty$ 时 $\sim\frac{1}{x^{2p+q-1}}$。故 $I_2$ 收敛要求 $p+q<1$ 且 $2p+q-1>1$。
**④ 合并。** 由 $p-1<1$ 得 $p<2$，由 $p+q<1$ 得 $q<1-p$，由 $2p+q-1>1$ 得 $q>2(1-p)$，故 $I$ 收敛时 $p<2$ 且 $2(1-p)<q<1-p$，A 正确。
【思路】按奇点 $x=1$ 把广义积分拆成两段，分别在 $0^+,\ 1^\pm,\ +\infty$ 处用 $p$-积分敛散判别（$0$ 附近幂次 $<1$ 收敛，无穷远处幂次 $>1$ 收敛）。
【易错】无穷远处的等价无穷小是 $\frac1{x^{2p+q-1}}$ 而非 $\frac1{x^{p-1}}$，指数须把两个因子合并；$0$ 与 $1$ 两处的条件要同时满足，不能只查一个奇点。

===Q5===
【答案】D
【解】
**① 命题①。** 由图(a)，弦 $\overline{AB}$ 的斜率不小于弦 $\overline{AC}$ 的斜率：$\frac{f(t)-f(0)}{t-0}\ge\frac{f(x)-f(0)}{x-0}\ (t\in[0,x])$，结合 $f(0)=1$ 得 $f(t)\ge\frac{f(x)-1}{x}t+1$，命题①正确。
**② 命题②。** 由图(b)同理 $\frac{f(t)-f(0)}{t-0}\le\frac{f(x)-f(0)}{x-0}$，即 $f(t)\le\frac{f(x)-1}{x}t+1$，命题②正确。
**③ 命题③。** 若 $f(x)\le0$ 不成立，则存在 $x_0\in(0,1)$ 使 $f(x_0)>0$；由 $f(0)=f(1)=0$ 知 $f$ 在 $(0,1)$ 内必有正的极大值，设极大值点 $\xi\in(0,1)$，则 $f(\xi)>0,\ f''(\xi)\le0$，从而 $\left.[f''(x)-f(x)]\right|_{x=\xi}<0$，与已知条件矛盾，故命题③正确。
**④ 命题④。** 由已知
$$\left[e^{-2x}f(x)\right]''=\left[f''(x)-4f'(x)+4f(x)\right]e^{-2x}\ge0$$
记 $F(x)=e^{-2x}f(x)$，则 $F$ 在 $(0,1)$ 内是凹函数，故 $F(x)\le\max\{F(0),F(1)\}=0$，从而 $f(x)\le0$，命题④正确。
**⑤ 结论。** 四个命题全都正确，正确的个数是 $4$，D 正确。
【思路】①②用割线斜率比较凹凸性，③用反证加极大值点处 $f''\le0$，④构造 $e^{-2x}f(x)$ 用二阶导数符号判定。
【易错】原册称 $F''\ge0$ 时 $F$ 为「凹函数」并按「端点为零则 $F\le0$」使用，中文教材凹凸术语定义不一，勿因名称混淆不等号方向。原册小注：若 $f''(x)\ge0\ (x\in[a,b])$ 且 $f(a)=f(b)=0$，则 $f(x)\le0$（图像为开口向上、位于 $x$ 轴下方的曲线），此即④的依据。

===Q6===
【答案】C
【解】
**① 化为方程根的问题。** 取对数，并令 $f(x)=bx^2-2\ln x-\ln a$。
**② 端点趋势。** $\lim\limits_{x\to0^+}f(x)=+\infty,\ \lim\limits_{x\to+\infty}f(x)=+\infty$，要使 $f(x)=0$ 有两个正实根，$f(x)$ 在 $(0,+\infty)$ 内需有负的最小值。
**③ 求最小值。** 由 $f'(x)=2bx-\frac2x=0$ 得唯一驻点 $x_0=\frac1{\sqrt b}$，且 $f''(x_0)=2b+\frac{2}{x_0^2}>0$，故 $x_0$ 是极小值点也是最小值点，
$$f\left(\frac1{\sqrt b}\right)=1+\ln b-\ln a=\ln\frac{be}{a}$$
**④ 定条件。** 令 $\ln\frac{be}{a}<0$ 得 $\frac{be}{a}<1$，即 $\frac ab>e$，C 正确。
【思路】取对数把「有两个正实根」转化为 $f(x)=bx^2-2\ln x-\ln a$ 的最小值小于零。
【易错】最小值是 $\ln\frac{be}{a}$，其中常数 $1$ 来自 $b\cdot\frac1b$，不要漏掉 $-\ln a$；驻点 $\frac1{\sqrt b}$ 存在隐含 $b>0$。

===Q7===
【答案】B
【解】
**① 连续性。** 由 $f(x,y)=(x+y)^n\sin\frac{1}{\sqrt{x^2+y^2}}$ 且 $\lim\limits_{(x,y)\to(0,0)}f(x,y)=0=f(0,0)$，知对任何正整数 $n$，$f(x,y)$ 在 $(0,0)$ 处都连续，选项 D 正确，故排除。
**② 偏导数存在性。**
$$f'_x(0,0)=\lim_{x\to0}\frac{f(x,0)-f(0,0)}{x}=\lim_{x\to0}\frac{x^n\sin\frac1{|x|}}{x}=\lim_{x\to0}x^{n-1}\sin\frac1{|x|}$$
当 $n>1$ 时 $f'_x(0,0)=0$；同理 $f'_y(0,0)=0$，即 $n\ge2$ 时两个偏导数均存在，选项 A 正确，故排除。
**③ 求偏导函数并讨论连续性。**
$$f'_x(x,y)=\begin{cases}n(x+y)^{n-1}\sin\frac{1}{\sqrt{x^2+y^2}}-(x+y)^n\cos\frac{1}{\sqrt{x^2+y^2}}\cdot\frac{x}{\sqrt{(x^2+y^2)^3}},&x^2+y^2\ne0\\0,&x^2+y^2=0\end{cases}$$
$n>1$ 时 $\lim\limits_{(x,y)\to(0,0)}n(x+y)^{n-1}\sin\frac{1}{\sqrt{x^2+y^2}}=0$；$n=2$ 时 $\lim\limits_{(x,y)\to(0,0)}\frac{x(x+y)^n}{(x^2+y^2)^{\frac32}}\cos\frac{1}{\sqrt{x^2+y^2}}$ 不存在。
当 $n\ge3$ 时
$$\left|\frac{x(x+y)^n\cos\frac{1}{\sqrt{x^2+y^2}}}{(x^2+y^2)^{\frac32}}\right|\le\left|\frac{(x+y)^n}{x^2+y^2}\right|\le\frac{\left(2\sqrt{\frac{x^2+y^2}{2}}\right)^n}{x^2+y^2}=2^{\frac n2}(x^2+y^2)^{\frac n2-1}$$
而 $\lim\limits_{(x,y)\to(0,0)}2^{\frac n2}(x^2+y^2)^{\frac n2-1}=0$，故该极限存在且为 $0$，即 $n\ge3$ 时 $f'_x(x,y)$ 在 $(0,0)$ 处连续；同理 $f'_y(x,y)$ 也连续，选项 C 正确，故排除。
**④ 结论。** 综上所述，应选 B。
【思路】先用定义求 $(0,0)$ 处偏导存在的条件（$n\ge2$），再写出偏导函数，用夹逼定理讨论其在 $(0,0)$ 的连续性（$n\ge3$ 连续、$n=2$ 不连续）。
【易错】原册首行把 $f$ 误排为 $(x+y)^n\cdot\frac{1}{\sin\sqrt{x^2+y^2}}$（该式在 $n=1$ 时并不趋于 $0$，与「对任何正整数 $n$ 都连续」矛盾），由后文导数式可知应为 $(x+y)^n\sin\frac{1}{\sqrt{x^2+y^2}}$，属明显排印错误，此处按正确形式转写。$n=2$ 时振荡项极限不存在是区分 B、C 的关键。

===Q8===
【答案】A
【解】
**① 由条件推出 $A,B$ 的关系。** 由 $A+B=AB$ 得 $AB-A-B+E=E$，即 $(A-E)(B-E)=E$，故 $A-E,\ B-E$ 均可逆，且 $B=(A-E)^{-1}A$。
**② 三秩相等证同解。** 这说明 $B$ 可通过对 $A$ 施行初等行变换得到，故 $r(A)=r(B)$，且
$$r\begin{pmatrix}A\\B\end{pmatrix}=r\begin{pmatrix}A\\(A-E)^{-1}A\end{pmatrix}=r\begin{pmatrix}A\\O\end{pmatrix}=r(A)$$
三秩相等，故 $AX=0$ 与 $BX=0$ 同解，应选 A。
**③ 举反例排除 B、C、D。** 对 B，若 $B$ 可逆则 $BAX=0$ 与 $AX=0$ 同解，故取 $B$ 不可逆：取 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix},\ B=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$，则 $A+B=O,\ AB=O,\ BA=O$，满足题设，但 $AX=0$ 与 $BAX=0$ 系数矩阵的秩不相等，因此不同解。对 C，用 B 的反例可直接排除。对 D，取 $A=B=2E$，则 $A+B=4E,\ AB=4E$ 满足题设，但 $A-B=O$，$AX=0$ 与 $(A-B)X=0$ 系数矩阵的秩不相等，因此不同解。综上应选 A。
【思路】由 $(A-E)(B-E)=E$ 得 $B=(A-E)^{-1}A$，用「三秩相等」判定 $AX=0$ 与 $BX=0$ 同解，其余选项逐一构造反例。
【易错】$(A-E)(B-E)=E$ 的展开是 $AB-A-B+E=E$，不要漏掉 $+E$；判断两齐次方程组同解看系数矩阵的秩是否相等，而非 $A,B$ 是否相似或相抵。

===Q9===
【答案】B
【解】
**① 命题②。** 由 $r(A)<r(B)=n$ 知 $\alpha_1,\alpha_2,\cdots,\alpha_n$ 线性相关，从而 $\alpha_1,\alpha_2,\cdots,\alpha_n,\beta_1,\beta_2,\cdots,\beta_n$ 线性相关，命题②正确。
**② 命题④。** 由
$$(A+B,A-B)=(A,B)\begin{pmatrix}E&E\\E&-E\end{pmatrix},\qquad\begin{vmatrix}E&E\\E&-E\end{vmatrix}=(-2)^n\ne0$$
（$E$ 为 $n$ 阶单位矩阵）知该分块矩阵可逆，故 $r(A,B)=r(A+B,A-B)$；由上知 $(A,B)$ 的列向量组线性相关，从而 $(A+B,A-B)$ 的列向量组线性相关，命题④正确。
**③ 命题①。** 取 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix},\ B=\begin{pmatrix}1&0\\0&1\end{pmatrix}$，满足 $r(A)<r(B)=2$，但 $\begin{pmatrix}1\\0\end{pmatrix},\begin{pmatrix}0\\0\end{pmatrix},\begin{pmatrix}1\\0\end{pmatrix},\begin{pmatrix}0\\1\end{pmatrix}$ 线性相关，故命题①不正确。
**④ 命题③。** 取同样的 $A,B$，则
$$(A+B,A-B)=\left(\begin{pmatrix}2&0\\0&1\end{pmatrix},\begin{pmatrix}0&0\\0&-1\end{pmatrix}\right)$$
其列向量组线性相关，故命题③不正确。B 正确。
【思路】用秩判断向量组的相关性，关键是把 $(A+B,A-B)$ 写成 $(A,B)$ 右乘可逆矩阵从而秩不变。
【易错】$\begin{vmatrix}E&E\\E&-E\end{vmatrix}=(-2)^n$ 而非 $(-2)^{2n}$；举反例时 $A,B$ 必须满足 $r(A)<r(B)=n$ 这一前提。

===Q10===
【答案】C
【解】
**① 命题①。** $A^T(B+B^T)A=O$（由 $B^T=-B$ 得 $B+B^T=O$），故 ① 中矩阵是实对称矩阵。
**② 命题②。** $(BAB)^T=B^TA^TB^T=BAB$，故 ② 中矩阵是实对称矩阵。
**③ 命题③。** $(AB-BA)^T=(AB)^T-(BA)^T=B^TA^T-A^TB^T=AB-BA$，故 ③ 中矩阵为实对称矩阵。
**④ 命题④。** $(ABA)^T=A^TB^TA^T=-ABA$，④ 中矩阵是反对称矩阵，故 $ABA$ 不能正交相似于对角矩阵。
**⑤ 结论。** 矩阵中可以正交相似于对角矩阵的个数为 $3$，C 正确。
【思路】实矩阵可正交相似对角化当且仅当它是实对称矩阵，逐个取转置判断四个矩阵是否对称。
【易错】原册 ① 行作「$A^T(B+B^T)A=O$，故 $A^T(B+B^T)A$，故 ① 中矩阵是实对称矩阵」，「故」后文字疑有重复脱漏，按原意照录。原册小注：实矩阵 $A$ 可正交相似于对角矩阵的充分必要条件是 $A$ 有 $n$ 个相互正交的特征向量（即 $A$ 为实对称矩阵）。④ 中反对称矩阵（非零时）不能正交相似对角化。

===Q11===
【答案】$y=2x+\frac14+\frac2e$
【解】
**① 求斜率。**
$$\lim_{x\to+\infty}\frac yx=\lim_{x\to+\infty}\frac{\sqrt{4x^2+x}\ln\left(e+\frac1x\right)}{x}=\lim_{x\to+\infty}\sqrt{4+\frac1x}\ln\left(e+\frac1x\right)=2\ln e=2$$
**② 求截距。**
$$\lim_{x\to+\infty}(y-2x)=\lim_{x\to+\infty}\left\{\left(\sqrt{4x^2+x}-2x\right)\ln\left(e+\frac1x\right)+\left[2x\ln\left(e+\frac1x\right)-2x\right]\right\}$$
$$=\lim_{x\to+\infty}\frac{x}{\sqrt{4x^2+x}+2x}\ln\left(e+\frac1x\right)+\lim_{x\to+\infty}2x\ln\left(1+\frac{1}{ex}\right)=\frac14+\lim_{x\to+\infty}2x\cdot\frac{1}{ex}=\frac14+\frac2e$$
**③ 写出方程。** 所求斜渐近线方程为 $y=2x+\frac14+\frac2e$。
【思路】设斜渐近线 $y=kx+b$，$k=\lim\frac yx$，$b=\lim(y-kx)$；计算中把 $\sqrt{4x^2+x}-2x$ 有理化，并用 $\ln\left(e+\frac1x\right)-1=\ln\left(1+\frac{1}{ex}\right)$。
【易错】$\ln\left(e+\frac1x\right)\to1$ 而非 $0$，拆项时必须减去 $2x$；$\sqrt{4x^2+x}-2x=\frac{x}{\sqrt{4x^2+x}+2x}\to\frac14$，不能当作 $0$ 丢掉。

===Q12===
【答案】$-2$
【解】
**① 化简已知极限。** 当 $x\to1$ 时 $\sqrt{x}-1=\sqrt{1+(x-1)}-1\sim\frac12(x-1)$，故
$$\lim_{x\to1}\frac{f(x)+x^x-1}{\frac12(x-1)}=-2\ \Longrightarrow\ \lim_{x\to1}\frac{f(x)+x^x-1}{x-1}=-1$$
从而 $\lim\limits_{x\to1}[f(x)+x^x-1]=0$，得 $\lim\limits_{x\to1}f(x)=f(1)=0$；记 $\frac{f(x)+x^x-1}{x-1}=-1+\alpha(x)$，其中 $\alpha(x)\to0\ (x\to1)$。
**② 写出 $f(x)$。** 当 $x\to1$ 时 $\alpha(x)\to0$，故
$$f(x)=1-x^x+(x-1)[\alpha(x)-1]$$
**③ 由定义求 $f'(1)$。**
$$f'(1)=\lim_{x\to1}\frac{f(x)-f(1)}{x-1}=\lim_{x\to1}\frac{1-x^x+(x-1)[\alpha(x)-1]}{x-1}=\lim_{x\to1}\left(\frac{1-x^x}{x-1}+[\alpha(x)-1]\right)$$
$$=-1-\lim_{x\to1}\frac{e^{x\ln x}-1}{x-1}=-1-\lim_{x\to1}\frac{x\ln x}{x-1}=-1-\lim_{x\to1}(\ln x+1)=-1-1=-2$$
【思路】把已知极限改写成 $f(x)+x^x-1$ 的一阶等价关系，得出 $f(1)=0$ 与 $f(x)$ 的表达式，再用导数定义配合 $\frac{x\ln x}{x-1}\to1$。
【易错】$f(x)$ 表达式中的 $[\alpha(x)-1]$ 项贡献 $-1$，不能漏；$e^{x\ln x}-1\sim x\ln x$，且 $\lim\frac{x\ln x}{x-1}=1$（洛必达得 $\ln x+1$）。

===Q13===
【答案】$\frac12$
【解】
**① 一阶求导。** $e^y+xy+x^2=1$ 两边对 $x$ 求导得
$$e^y\cdot y'+y+xy'+2x=0$$
记为式 ①；将 $x=0,\ y=0$ 代入式 ①，得 $y'(0)=0$。
**② 二阶求导。** 式 ① 两边再对 $x$ 求导得
$$e^y(y')^2+e^y y''+2y'+xy''+2=0$$
记为式 ②；将 $x=0,\ y=0,\ y'(0)=0$ 代入式 ②，得 $y''(0)=-2$。
**③ 曲率半径。**
$$R=\frac{(1+y'^2)^{\frac32}}{|y''|}=\frac12$$
【思路】隐函数逐次求导得 $y'(0),\ y''(0)$，再代入曲率半径公式 $R=\frac{(1+y'^2)^{3/2}}{|y''|}$。
【易错】式 ① 再求导时 $y+xy'$ 产生 $y'+y'+xy''=2y'+xy''$，易漏一项；曲率半径分子是 $(1+y'^2)^{3/2}$ 而非 $(1+y')^{3/2}$。

===Q14===
【答案】$\frac{y^2}{4}+\frac{3}{4y^2}=x$
【解】
**① 化为关于 $x$ 的一阶线性方程。** 已知方程 $(y^2-2x)\,dy-y\,dx=0$，视 $y$ 为自变量，可化为
$$\frac{dx}{dy}+\frac{2x}{y}=y$$
**② 求通解。** 解一阶线性微分方程：
$$x=e^{-\int\frac2y dy}\left(\int y\,e^{\int\frac2y dy}dy+C\right)=y^{-2}\left(\int y^3\,dy+C\right)=\frac{y^2}{4}+\frac{C}{y^2}$$
**③ 定常数。** 由 $y(1)=1$ 得 $C=\frac34$，所求特解为 $\frac{y^2}{4}+\frac{3}{4y^2}=x$。
【思路】把 $y$ 作自变量，将方程化为 $\frac{dx}{dy}+\frac2y x=y$，套一阶线性方程通解公式。
【易错】积分因子 $e^{\int\frac2y dy}=y^2$（取 $y>0$），非齐次项 $y$ 乘 $y^2$ 得 $y^3$；由 $y(1)=1$ 定 $C$ 时是代入 $x=1,\ y=1$。

===Q15===
【答案】$\frac12\pi^3$
【解】
**① 写出 $V_n$。**
$$V_n=2\pi\int_0^{n\pi}x\cos^2x\,dx=\pi\int_0^{n\pi}x(1+\cos2x)\,dx=\pi\left[\int_0^{n\pi}x\,dx+\frac12\int_0^{n\pi}x\,d(\sin2x)\right]$$
**② 分部积分。**
$$V_n=\frac12n^2\pi^3+\frac\pi2\left[\left.x\sin2x\right|_0^{n\pi}-\int_0^{n\pi}\sin2x\,dx\right]=\frac12n^2\pi^3$$
因 $\sin2n\pi=0$ 且 $\int_0^{n\pi}\sin2x\,dx=0$。
**③ 取极限。**
$$\lim_{n\to\infty}\frac{V_n}{(n+1)^2}=\frac12\pi^3$$
【思路】用 $\cos^2x=\frac{1+\cos2x}{2}$ 化简体积积分，分部积分后振荡项为零，只剩 $\frac12n^2\pi^3$。
【易错】$\pi\int_0^{n\pi}x\,dx=\frac12 n^2\pi^3$，上限 $n\pi$ 带来的 $\pi$ 因子不要漏；分母 $(n+1)^2\sim n^2$。

===Q16===
【答案】$-5$
【解】
**① 由 $AB=BA$ 读出 $A$ 的相似形。** 由已知，有
$$AB=\begin{pmatrix}2b_{11}&3b_{12}&-b_{13}\\2b_{21}&3b_{22}&-b_{23}\\2b_{31}&3b_{32}&-b_{33}\end{pmatrix}=\begin{pmatrix}b_{11}&b_{12}&b_{13}\\b_{21}&b_{22}&b_{23}\\b_{31}&b_{32}&b_{33}\end{pmatrix}\begin{pmatrix}2&0&0\\0&3&0\\0&0&-1\end{pmatrix}=BA$$
又 $B$ 可逆，故
$$B^{-1}AB=\begin{pmatrix}2&0&0\\0&3&0\\0&0&-1\end{pmatrix}$$
即 $A$ 相似于该对角阵，且 $|A|=-6$。
**② 求 $A^*$ 的特征值。** $A^*$ 的特征值为 $\frac{|A|}{\lambda}$，即 $-3,\ -2,\ 6$。
**③ 计算 $|A+A^*|$。**
$$B^{-1}(A+A^*)B=B^{-1}AB+B^{-1}A^*B=\begin{pmatrix}2&0&0\\0&3&0\\0&0&-1\end{pmatrix}+\begin{pmatrix}-3&0&0\\0&-2&0\\0&0&6\end{pmatrix}=\begin{pmatrix}-1&0&0\\0&1&0\\0&0&5\end{pmatrix}$$
$$|A+A^*|=(-1)\times1\times5=-5$$
【思路】由 $AB=BA$ 且 $B$ 可逆得 $A\sim\mathrm{diag}(2,3,-1)$，再用 $A^*$ 的特征值 $\frac{|A|}{\lambda}$ 将 $A+A^*$ 相似对角化求行列式。
【易错】$A^*$ 的特征值是 $\frac{|A|}{\lambda}$ 而非 $\lambda$；$A+A^*$ 与 $B^{-1}(A+A^*)B$ 有相同特征值，行列式等于特征值之积。

===Q17===
【答案】$a=b=1$
【解】
**① 构造拉格朗日函数。** 应用拉格朗日乘数法，令
$$L=3x^2+2xy+3y^2+\lambda\left(1-\frac{x^2}{a^2}-\frac{y^2}{b^2}\right)$$
则
$$\begin{cases}L'_x=2\left[\left(3-\frac{\lambda}{a^2}\right)x+y\right]=0\\L'_y=2\left[x+\left(3-\frac{\lambda}{b^2}\right)y\right]=0\\L'_\lambda=1-\frac{x^2}{a^2}-\frac{y^2}{b^2}=0\end{cases}$$
依次记为式 ①、②、③。
**② 求 $\lambda$。** 式 ①$\times\frac x2+$ 式 ②$\times\frac y2$ 得
$$3x^2+2xy+3y^2-\lambda\left(\frac{x^2}{a^2}+\frac{y^2}{b^2}\right)=0$$
由约束（式 ③）$\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ 知 $\lambda=3x^2+2xy+3y^2$；将 $x=\frac{\sqrt2}{2},\ y=-\frac{\sqrt2}{2}$ 代入得
$$\lambda=3\left(\frac{\sqrt2}{2}\right)^2+2\times\frac{\sqrt2}{2}\times\left(-\frac{\sqrt2}{2}\right)+3\left(-\frac{\sqrt2}{2}\right)^2=2$$
**③ 解 $a,b$。** 将 $\lambda=2,\ x=\frac{\sqrt2}{2},\ y=-\frac{\sqrt2}{2}$ 代入式 ①、式 ②，得
$$\begin{cases}\left(3-\frac{2}{a^2}\right)\frac{\sqrt2}{2}-\frac{\sqrt2}{2}=0\\\frac{\sqrt2}{2}+\left(3-\frac{2}{b^2}\right)\left(-\frac{\sqrt2}{2}\right)=0\end{cases}$$
解上方程组，得 $a=b=1$。
【思路】用拉格朗日乘数法，先把 ①、② 分别乘 $\frac x2,\frac y2$ 相加消去 $\lambda$ 的约束项，定出 $\lambda=2$ 后回代求 $a,b$。
【易错】$\lambda=3x^2+2xy+3y^2$ 依赖约束式 ③，不能省略该步；代入点时 $y$ 为负，符号要仔细。

===Q18===
【答案】$\frac\pi7$（其中 $f(t)=e^{-\frac2\pi t^2}$）
【解】
**① 求 $f(t)$。**
$$f(t)=\lim_{x\to+\infty}\left(\frac2\pi\arctan\frac{x}{t^2}\right)^x=e^{\lim\limits_{x\to+\infty}x\ln\left(\frac2\pi\arctan\frac{x}{t^2}\right)}$$
当 $t\ne0$ 时，有
$$\lim_{x\to+\infty}x\ln\left[1+\left(\frac2\pi\arctan\frac{x}{t^2}-1\right)\right]=\lim_{x\to+\infty}\frac{\frac2\pi\arctan\frac{x}{t^2}-1}{\frac1x}=-\frac2\pi t^2$$
故 $f(t)=e^{-\frac2\pi t^2}$。
**② 交换积分次序。** 记 $D=\{(s,y)\mid s^2\le y\le t,\ 0\le s\le\sqrt t\}$，交换积分次序得
$$\int_0^{\sqrt t}ds\int_{s^2}^t\sin y^2\,dy=\int_0^t dy\int_0^{\sqrt y}\sin y^2\,ds=\int_0^t\sqrt y\sin y^2\,dy$$
**③ 等价无穷小与洛必达。** 由 $[1-f(t)]\,t^{\frac32}=(1-e^{-\frac2\pi t^2})\,t^{\frac32}\sim\frac2\pi t^{\frac72}\ (t\to0^+)$，故
$$\lim_{t\to0^+}\frac{\int_0^{\sqrt t}ds\int_{s^2}^t\sin y^2\,dy}{[1-f(t)]\,t^{\frac32}}=\lim_{t\to0^+}\frac{\int_0^t\sqrt y\sin y^2\,dy}{\frac2\pi t^{\frac72}}=\lim_{t\to0^+}\frac{\sqrt t\sin t^2}{\frac2\pi\cdot\frac72 t^{\frac52}}=\frac\pi7$$
【思路】先取对数用 $1^\infty$ 型极限求出 $f(t)$，再交换累次积分次序化为变限积分，最后用等价无穷小加洛必达法则。
【易错】$\frac2\pi\arctan\frac{x}{t^2}-1\sim-\frac{2t^2}{\pi x}$，故指数极限为 $-\frac2\pi t^2$；交换次序后上限是 $t$、被积是 $\sqrt y\sin y^2$；洛必达后分子 $\sqrt t\sin t^2\sim t^{\frac52}$ 与分母同阶，得 $\frac\pi7$。

===Q19===
【答案】（I）$f(x)=e^{x-1}+e^{-(x-1)}-2$；（II）$V=\pi(5e^{-1}+e-4)$
【解】
**（I）**
**① 换元化简积分方程。** 令 $u=x-t$，则
$$\int_0^{x-1}t f(x-t)\,dt=\int_1^x(x-u)f(u)\,du$$
故有
$$f(x)=(x-1)^2+x\int_1^x f(u)\,du-\int_1^x uf(u)\,du$$
记为式 ①。
**② 两次求导化微分方程。** 式 ① 两边对 $x$ 求导得
$$f'(x)=2(x-1)+\int_1^x f(u)\,du$$
记为式 ②；式 ② 两边再对 $x$ 求导得
$$f''(x)-f(x)=2$$
记为式 ③。
**③ 定初始条件并求解。** 式 ① 中令 $x=1$ 得 $f(1)=0$；式 ② 中令 $x=1$ 得 $f'(1)=0$。解微分方程 ③ 得 $y=C_1e^x+C_2e^{-x}-2$，又由
$$\begin{cases}f(1)=C_1e+C_2e^{-1}-2=0\\f'(1)=C_1e-C_2e^{-1}=0\end{cases}$$
解得 $C_1=e^{-1},\ C_2=e$，故 $y=f(x)=e^{x-1}+e^{-(x-1)}-2$。
**（II）**
**① 写体积。** 由（I）知区域 $D$，绕 $x=1$ 旋转一周所得旋转体体积为
$$V=\pi\cdot1^2(e^{-1}+e-2)-2\pi\int_0^1(1-x)f(x)\,dx$$
**② 算积分。** 令 $t=x-1$，则
$$\int_0^1(1-x)\left[e^{x-1}+e^{-(x-1)}-2\right]dx=-\int_{-1}^0 t\left(e^t+e^{-t}-2\right)dt=-2e^{-1}+1$$
**③ 得结果。**
$$V=\pi(e^{-1}+e-2)-2\pi(-2e^{-1}+1)=\pi(5e^{-1}+e-4)$$
【思路】（I）换元后两次求导把积分方程化为 $f''-f=2$，并由原式取初值求解；（II）写出绕 $x=1$ 的旋转体体积，换元算积分。
【易错】（I）中 $\frac{d}{dx}\left[x\int_1^x f-\int_1^x uf\right]=\int_1^x f$，链式求导时勿漏项；初值 $f(1),f'(1)$ 必须从式 ①、② 在 $x=1$ 处取得。（II）换元 $t=x-1$ 时 $1-x=-t$，上限变 $0$、下限变 $-1$。

===Q20===
【答案】$\frac{4\sqrt3\pi}{27}$
【解】
**① 利用对称性。** $D$ 关于直线 $y=x$ 对称，被积函数 $x+y$ 也关于 $y=x$ 对称，$D_1$ 为阴影部分（$0\le\theta\le\frac\pi4$），故
$$I=\iint_D(x+y)\,dx\,dy=2\iint_{D_1}(x+y)\,dx\,dy$$
**② 化为极坐标。** 边界为 $x^3+y^3=1$，即 $r^3(\cos^3\theta+\sin^3\theta)=1$，故
$$I=2\int_0^{\frac\pi4}d\theta\int_0^{\sqrt[3]{\frac{1}{\cos^3\theta+\sin^3\theta}}}(\cos\theta+\sin\theta)\,r^2\,dr$$
$$=2\int_0^{\frac\pi4}(\cos\theta+\sin\theta)\cdot\left.\frac13 r^3\right|_0^{\sqrt[3]{\frac{1}{\cos^3\theta+\sin^3\theta}}}d\theta=\frac23\int_0^{\frac\pi4}\frac{\cos\theta+\sin\theta}{\cos^3\theta+\sin^3\theta}\,d\theta$$
**③ 三角化简。** 由 $\cos^3\theta+\sin^3\theta=(\cos\theta+\sin\theta)(1-\cos\theta\sin\theta)$，
$$I=\frac23\int_0^{\frac\pi4}\frac{d\theta}{\cos^2\theta-\cos\theta\sin\theta+\sin^2\theta}=\frac23\int_0^{\frac\pi4}\frac{d\theta}{1-\cos\theta\sin\theta}$$
分子分母同除以 $\cos^2\theta$ 并令 $t=\tan\theta$，得
$$I=\frac23\int_0^1\frac{dt}{1+t^2-t}$$
**④ 配方积分。**
$$I=\frac23\int_0^1\frac{d\left(t-\frac12\right)}{\left(t-\frac12\right)^2+\left(\frac{\sqrt3}{2}\right)^2}=\left.\frac23\cdot\frac2{\sqrt3}\arctan\frac{2\left(t-\frac12\right)}{\sqrt3}\right|_0^1$$
$$=\frac{4}{3\sqrt3}\left[\arctan\frac1{\sqrt3}-\arctan\left(-\frac1{\sqrt3}\right)\right]=\frac{4\sqrt3\pi}{27}$$
【思路】先由对称性取一半区域，再用极坐标把边界 $x^3+y^3=1$ 化为 $r^3(\cos^3\theta+\sin^3\theta)=1$，最后 $\tan\theta$ 换元并配方成反正切积分。
【易错】边界是 $x^3+y^3=1$，故 $r$ 上限为三次根 $\sqrt[3]{\frac{1}{\cos^3\theta+\sin^3\theta}}$；$\cos^3\theta+\sin^3\theta$ 分解后的 $\cos\theta+\sin\theta$ 要与分子约分；$\arctan\frac1{\sqrt3}=\frac\pi6$。

===Q21===
【答案】（I）$f_n(x)=x^n+nx$；（II）$\lim\limits_{n\to\infty}(1+x_n)^n=e^k$
【解】
**（I）**
**① 化为一阶线性方程。** $xf_n'(x)-f_n(x)=(n-1)x^n$ 变形为
$$f_n'(x)-\frac1x f_n(x)=(n-1)x^{n-1}$$
**② 求通解。** 这是一阶线性微分方程，其通解为
$$f_n(x)=e^{\int\frac1x dx}\left[\int(n-1)x^{n-1}e^{-\int\frac1x dx}dx+C\right]=x\left[\int(n-1)x^{n-2}dx+C\right]=x(x^{n-1}+C)=x^n+Cx$$
**③ 定常数。** 由 $f_n(1)=1+n$ 得 $C=n$，故 $f_n(x)=x^n+nx$。
**（II）**
**① 存在唯一实根。** 令 $F_n(x)=f_n(x)-k=x^n+nx-k$，则
$$F_n(0)=-k<0,\qquad F_n\left(\frac kn\right)=\left(\frac kn\right)^n>0$$
由零点定理知存在 $x_n\in\left(0,\frac kn\right)$ 使 $F_n(x_n)=f_n(x_n)-k=0$；又 $F_n'(x)=nx^{n-1}+n>0$，$F_n(x)$ 严格单调增加，故 $x_n$ 是方程 $f_n(x)=k$ 的唯一实根。
**② 缩小范围。** 由已知 $n>k$，当 $n>1$ 时有 $\frac kn<1,\ \frac{k}{n^2}<\frac kn$，且
$$F_n\left(\frac kn-\frac{k}{n^2}\right)=\left(\frac kn-\frac{k}{n^2}\right)^n-\frac kn<\left(\frac kn-\frac{k}{n^2}\right)-\frac kn=-\frac{k}{n^2}<0$$
由 $F_n(x)$ 严格单调增加且 $F_n(x_n)=0$，知
$$\frac kn-\frac{k}{n^2}<x_n<\frac kn$$
**③ 夹逼。** 于是
$$\left(1+\frac kn-\frac{k}{n^2}\right)^n<(1+x_n)^n<\left(1+\frac kn\right)^n$$
又 $\lim\limits_{n\to\infty}\left(1+\frac kn\right)^n=e^k$，且
$$\lim_{n\to\infty}\left(1+\frac kn-\frac{k}{n^2}\right)^n=\lim_{n\to\infty}\left(1+\frac kn-\frac{k}{n^2}\right)^{\frac{1}{\frac kn-\frac k{n^2}}\cdot\left(\frac kn-\frac k{n^2}\right)n}=e^k$$
故由夹逼准则，得 $\lim\limits_{n\to\infty}(1+x_n)^n=e^k$。
【思路】（I）解一阶线性微分方程；（II）用零点定理定位唯一根 $x_n\in\left(\frac kn-\frac{k}{n^2},\frac kn\right)$，再由 $(1+\frac kn)^n\to e^k$ 夹逼。
【易错】原册在「由 $F_n(x)$ 严格单调增加，$F_n(x_n)=0$，知」之后一行印作 $\frac kn+\frac{k}{n^2}<x_n<\frac kn$，加号应为减号（否则左端大于右端，且与上一行 $F_n(\frac kn-\frac{k}{n^2})<0$ 矛盾），属明显排印错误，此处按正确形式转写。另 $(1+\frac kn-\frac{k}{n^2})^n\to e^k$ 需验证 $\left(\frac kn-\frac k{n^2}\right)n\to k$。

===Q22===
【答案】（I）$k=3$，且 $A^2+A=2E$；（II）$\alpha=(3,3,3)^T$，$A=\begin{pmatrix}0&-1&-1\\-1&0&-1\\-1&-1&0\end{pmatrix}$，特征值 $\lambda_1=\lambda_2=1,\lambda_3=-2$，单位特征向量 $\gamma_1=\frac1{\sqrt2}(-1,1,0)^T,\gamma_2=\frac1{\sqrt6}(1,1,-2)^T,\gamma_3=\frac1{\sqrt3}(1,1,1)^T$
【解】
**（I）**
**① 展开 $A^2$。**
$$A^2=\left(E-\frac{k}{\alpha^T\alpha}\alpha\alpha^T\right)\left(E-\frac{k}{\alpha^T\alpha}\alpha\alpha^T\right)=E-\frac{2k}{\alpha^T\alpha}\alpha\alpha^T+\frac{k^2}{(\alpha^T\alpha)^2}\left(\alpha\alpha^T\alpha\alpha^T\right)$$
$$=E-\frac{2k}{\alpha^T\alpha}\alpha\alpha^T+\frac{k^2}{\alpha^T\alpha}\alpha\alpha^T$$
**② 代入已知化简。** 由已知 $\frac{k}{\alpha^T\alpha}\alpha\alpha^T=E-A$，代入上式得
$$A^2=E-2(E-A)+k(E-A)=(k-1)E+(2-k)A$$
即 $A^2-(2-k)A+(1-k)E=O$。
**③ 由特征值定 $k$。** 设 $\lambda$ 为 $A$ 的任一特征值，$\xi$ 为其对应的特征向量，则
$$\left[A^2-(2-k)A+(1-k)E\right]\xi=0$$
得 $\lambda^2-(2-k)\lambda+(1-k)=0$。由 $\lambda=-2$ 是 $A$ 的特征值，有
$$(-2)^2-(2-k)(-2)+1-k=0$$
解得 $k=3$，且 $A^2+A=2E$。
**（II）**
**① 求 $A$。** 由（I）知 $\alpha=(k,k,k)^T=(3,3,3)^T$，则
$$\alpha^T\alpha=(3,3,3)\begin{pmatrix}3\\3\\3\end{pmatrix}=27,\qquad\alpha\alpha^T=\begin{pmatrix}3\\3\\3\end{pmatrix}(3,3,3)=9\begin{pmatrix}1&1&1\\1&1&1\\1&1&1\end{pmatrix}$$
故
$$A=E-\frac{k}{\alpha^T\alpha}\alpha\alpha^T=E-\frac{3}{27}\cdot9\begin{pmatrix}1&1&1\\1&1&1\\1&1&1\end{pmatrix}=\begin{pmatrix}0&-1&-1\\-1&0&-1\\-1&-1&0\end{pmatrix}$$
**② 求特征值与特征向量。**
$$|\lambda E-A|=\begin{vmatrix}\lambda&1&1\\1&\lambda&1\\1&1&\lambda\end{vmatrix}=(\lambda-1)^2(\lambda+2)=0$$
知 $A$ 的特征值为 $\lambda_1=\lambda_2=1,\ \lambda_3=-2$。由 $(E-A)X=0$ 得 $A$ 的特征向量为 $\alpha_1=(-1,1,0)^T,\ \alpha_2=(1,1,-2)^T$（已正交）；由 $(-2E-A)X=0$ 得 $A$ 的特征向量为 $\alpha_3=(1,1,1)^T$。
**③ 单位化。** 将 $\alpha_1,\alpha_2,\alpha_3$ 单位化，得
$$\gamma_1=\frac1{\sqrt2}(-1,1,0)^T,\qquad\gamma_2=\frac1{\sqrt6}(1,1,-2)^T,\qquad\gamma_3=\frac1{\sqrt3}(1,1,1)^T$$
【思路】（I）利用 $\alpha^T\alpha$ 是数量把 $(\alpha\alpha^T)^2$ 化简，结合 $\frac{k}{\alpha^T\alpha}\alpha\alpha^T=E-A$ 得矩阵方程，再把已知特征值代入定出 $k$；（II）定量算出 $A$ 后求特征值、特征向量并单位化。
【易错】$\alpha\alpha^T\alpha\alpha^T=\alpha(\alpha^T\alpha)\alpha^T$，其中 $\alpha^T\alpha$ 是数可提到前面；$\lambda=-2$ 要代入 $\lambda^2-(2-k)\lambda+(1-k)=0$。本页（第 54 页）为所给扫描的末页，（II）在写出 $\gamma_1,\gamma_2,\gamma_3$ 后即止，通常应有的「令 $Q=(\gamma_1,\gamma_2,\gamma_3)$，则 $Q^TAQ=\mathrm{diag}(1,1,-2)$」未见后续页，疑原册后续内容缺失。
