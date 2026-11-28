===Q1===
【答案】C
【解】
**① 定位无定义点。** $f(x)=\dfrac{\ln|x^2-1|\sin(x+1)}{x^2}\cdot\mathrm{e}^{-\frac{1}{|x|}}$ 在 $x=0$（分母含 $x^2$ 且指数 $-\dfrac1{|x|}$）与 $x=\pm1$（$\ln|x^2-1|$）处无定义，故只有 $0,\pm1$ 可能是间断点。
**② 求 $x\to-1$ 与 $x\to0$ 的极限。** 令 $h=x+1\to0$，则 $|x^2-1|=|(x-1)(x+1)|\sim2|h|$，$\ln|x^2-1|\sim\ln(2|h|)$ 而 $\sin(x+1)\sim h$，由 $h\ln|h|\to0$ 得分子趋于 $0$，分母趋于 1、$\mathrm{e}^{-\frac1{|x|}}\to\mathrm{e}^{-1}$，故 $\lim\limits_{x\to-1}f(x)=0$。当 $x\to0$，$\ln|x^2-1|=\ln(1-x^2)\sim-x^2$，故 $\dfrac{\ln|x^2-1|}{x^2}\to-1$，但 $\mathrm{e}^{-\frac1{|x|}}\to0$，故 $\lim\limits_{x\to0}f(x)=0$。
**③ 求 $x\to1$ 的极限。** 此时 $\ln|x^2-1|\to-\infty$，$\sin(x+1)\to\sin2\ne0$，$\mathrm{e}^{-\frac1{|x|}}\to\mathrm{e}^{-1}$，分母趋于 1，故 $\lim\limits_{x\to1}f(x)=\infty$，为无穷间断点。
**④ 计数。** $x=0$ 与 $x=-1$ 处极限存在且有限，均为可去间断点，共 2 个，选 C。
【思路】先由定义域锁定三个间断点，再用 $h\ln|h|\to0$、$\ln(1-x^2)\sim-x^2$ 与 $\mathrm{e}^{-1/|x|}\to0$ 分别求极限，按可去间断定义计数。
【易错】$x=0$ 处 $\dfrac{\ln(1-x^2)}{x^2}\to-1$ 本身有限，起决定作用的是 $\mathrm{e}^{-\frac1{|x|}}\to0$；$x=\pm1$ 处 $\sin(x+1)$ 的极限分别是 $\sin2\ne0$ 与 $0$，二者结论完全不同。

===Q2===
【答案】A
【解】
**① 由连续性定 $c$。** $f(0^-)=c$，$f(0^+)=\ln1=0$，故 $c=0$。
**② 由一阶导数连续定 $b$。** $f'_-(0)=\lim\limits_{x\to0^-}\dfrac{ax^2+b\sin x}{x}=b$，$f'_+(0)=\lim\limits_{x\to0^+}\dfrac{\ln(1+x)}{x}=1$，故 $b=1$。
**③ 写出 $f'(x)$ 并求二阶导数的左右极限。** 由①②，
$$f'(x)=\begin{cases}2ax+\cos x,&x<0,\\[2pt]1,&x=0,\\[2pt]\dfrac1{1+x},&x>0.\end{cases}$$
于是 $f''(0^-)=\lim\limits_{x\to0^-}\dfrac{2ax+\cos x-1}{x}=2a$，$f''(0^+)=\lim\limits_{x\to0^+}\dfrac{\frac1{1+x}-1}{x}=\lim\limits_{x\to0^+}\dfrac{-x}{x(1+x)}=-1$。
**④ 二阶导数不存在的条件。** 需 $2a\ne-1$，即 $a\ne-\dfrac12$。结合 $b=1,c=0$，选 A。
【思路】先在 $x=0$ 用连续与一阶导连续定出 $c,b$，再写出导函数的分段表达式，用差商求 $f''$ 的左右极限并令其不等。
【易错】二阶导数存在的含义是导函数在该点可导，须用 $f'(x)$ 在 0 处的差商，不能把 $x<0$ 的二阶导公式 $2a-\cos x$ 直接代入 $x=0$；选项 B 的 $a\ne\frac12$（正号）与正确条件 $a\ne-\frac12$ 只差一个符号。

===Q3===
【答案】D
【解】
**① 由 $f''>0$ 判定无极值点。** $f''>0$ 说明 $f'$ 严格递增，当 $x\in(0,1)$ 时 $f'(x)>f'(0)=1>0$，故 $f$ 在 $(0,1)$ 严格递增，导数不变号，没有极值点。
**② 用拉格朗日中值定理判定有零点。** $f$ 在 $[0,1]$ 连续、在 $(0,1)$ 可导，存在 $\xi\in(0,1)$ 使
$$f(1)-f(0)=f'(\xi)(1-0)=f'(\xi)>0.$$
故 $f(1)>f(0)=-1$，且 $f(1)=f(0)+f'(\xi)=-1+f'(\xi)>0$。因 $f(0)=-1<0$、$f(1)>0$，由零点定理 $f$ 在 $(0,1)$ 内至少有一个零点。选 D。
【思路】$f''>0\Rightarrow f'$ 递增，结合 $f'(0)=1$ 得 $f'>0$ 排除极值；再用拉格朗日中值定理估计 $f(1)>0$，配合 $f(0)<0$ 用零点定理确认零点。
【易错】导数恒正只说明单调，不能推出有极值；也不能仅凭 $f(0)<0$ 就断言有零点，必须确认另一端函数值为正。

===Q4===
【答案】B
【解】
**① 把积分拆成两段。** 被积函数在 $x=0$ 处可能出现瑕点，故
$$\int_0^{+\infty}=\int_0^1+\int_1^{+\infty},$$
原积分收敛当且仅当两段同时收敛。
**② $x\to0^+$ 端。** 由 $\ln^n(x+1)\sim x^n$、$\sqrt{1+x^m}\to1$，被积函数 $\sim x^{k+n}$；$\int_0^1x^{k+n}dx$ 收敛要求 $k+n>-1$，即 $k>-n-1$。要对一切正整数 $n$ 成立，最紧的是 $n=1$，得 $k>-2$。
**③ $x\to+\infty$ 端。** 由 $\ln^n(x+1)\sim\ln^nx$、$\sqrt{1+x^m}\sim x^{m/2}$，被积函数 $\sim x^{k-\frac m2}\ln^nx$；收敛要求 $k-\dfrac m2<-1$，即 $k<\dfrac m2-1$。要对一切正整数 $m$ 成立，最紧的是 $m=1$，得 $k<-\dfrac12$。
**④ 取交集。** $k\in\left(-2,-\dfrac12\right)$，选 B。
【思路】在 0 与 $\infty$ 两端分别用比较判别法的极限形式，把"对任意正整数 $m,n$ 收敛"化为对最不利情形 $n=1$、$m=1$ 的约束，再取交集。
【易错】"对任意正整数 $m,n$ 均收敛"必须取所有 $m,n$ 的交集，不能只验证某一个固定取值；$\ln^n(x+1)$ 在 0 附近提供的是 $x^n$ 因子，不应误当成 $x$。

===Q5===
【答案】A
【解】
**① 换元并整理方程。** 由 $y=z^m$ 得 $\dfrac{dy}{dx}=mz^{m-1}\dfrac{dz}{dx}$，代入 $y'=ax^\alpha+by^\beta$：
$$mz^{m-1}\frac{dz}{dx}=ax^\alpha+bz^{m\beta}\quad\Longrightarrow\quad \frac{dz}{dx}=\frac a m x^\alpha z^{1-m}+\frac b m z^{m\beta-m+1}.$$
**② 齐次方程的两个条件。** 要写成 $\dfrac{dz}{dx}=f\!\left(\dfrac zx\right)$：第一项 $x^\alpha z^{1-m}=\left(\dfrac xz\right)^{m-1}$ 只依赖于 $\dfrac zx$，需 $\alpha=m-1$；第二项必须不含 $x,z$ 的单独幂次，需 $m\beta-m+1=0$。
**③ 消去 $m$。** 由第二式 $m=\dfrac1{1-\beta}$，代入第一式得 $\alpha=\dfrac1{1-\beta}-1=\dfrac{\beta}{1-\beta}$，于是 $\dfrac1\alpha=\dfrac{1-\beta}{\beta}=\dfrac1\beta-1$，即 $\dfrac1\beta-\dfrac1\alpha=1$。选 A。
【思路】换元后把方程整理为 $z'$ 的表达式，令两项分别成为 $\frac zx$ 的函数与常数，消去辅助指数 $m$ 得到 $\alpha,\beta$ 的关系。
【易错】$m$ 是引入的中间指数，最后必须消去；齐次条件要求 $z'$ 右端只能通过 $\frac zx$ 依赖变量，不能残留 $x^\alpha$ 与 $z$ 的独立幂次。

===Q6===
【答案】C
【解】
**① 充分性。** 若 $g(0,0)=0$，则 $f(0,0)=0$，且
$$\left|\frac{f(x,0)-f(0,0)}{x}\right|=\left|\frac{g(x,0)|x|}{x}\right|=|g(x,0)|\to|g(0,0)|=0\quad(x\to0),$$
故 $f'_x(0,0)=0$；同理 $\left|\dfrac{f(0,y)-f(0,0)}{y}\right|=|g(0,y)|\to0$，故 $f'_y(0,0)=0$，偏导存在。
**② 必要性。** 若 $f'_x(0,0),f'_y(0,0)$ 存在，则 $\lim\limits_{x\to0^+}g(x,0)\dfrac{|x|}{x}=\lim\limits_{x\to0^+}g(x,0)=g(0,0)$ 存在；而在 $y$ 方向
$$\lim_{y\to0^+}g(0,y)\frac{|y|}{y}=g(0,0),\qquad \lim_{y\to0^-}g(0,y)\frac{|y|}{y}=-g(0,0).$$
两者必须相等，故 $g(0,0)=-g(0,0)$，即 $g(0,0)=0$。
**③ 结论。** 条件既是充分又是必要的，选 C。
【思路】沿 $x$ 轴与 $y$ 轴写差商，注意 $|x|/x$ 在两侧的符号；充分性用夹逼，必要性用左右差商必须一致。
【易错】$|y|/y$ 在 $y\to0^-$ 时为 $-1$，正因为这一符号差异才逼出 $g(0,0)=0$；只检查 $x\to0^+$ 一个方向不足以得到必要性。

===Q7===
【答案】D
【解】
**① 用原函数处理奇偶性。** 设 $F'(t)=f(t)$；当 $f$ 为奇函数时，可取 $F$ 为偶函数，此时 $F(0)=0$。
**② 验证选项 D。** 记 $H(x)=\displaystyle\int_0^xdy\int_y^xf(t)\,dt$，则
$$H(x)=\int_0^x[F(x)-F(y)]\,dy=xF(x)-\int_0^xF(y)\,dy.$$
$x$ 是奇函数、$F$ 是偶函数，故 $xF(x)$ 为奇函数；$F$ 为偶函数时 $\int_0^xF(y)dy$ 为奇函数；两者之差仍为奇函数，故 (D) 正确。
**③ 排除其余选项。** 取 $f(t)=t$（奇），(B) 给出 $\displaystyle\int_a^x\frac{y^2}{2}dy=\frac{x^3}{6}-\frac{a^3}{6}$，$a\ne0$ 时非奇非偶；取 $f(t)=1$（偶），(A) 给出 $\displaystyle\int_0^x(y-a)dy=\frac{x^2}{2}-ax$，非奇函数；(C) 中 $\int_0^yf(t)dt$ 在 $f$ 偶时为奇函数，再对 $y$ 从 0 积分得偶函数，也不是奇函数。选 D。
【思路】把二重积分化为 $xF(x)-\int_0^xF(y)dy$，利用"奇×偶=奇"与"偶函数从 0 积分得奇函数"判定；其余选项用具体函数举例排除。
【易错】连续奇函数的原函数是偶函数（差一个常数），此处取 $F(0)=0$ 最方便；累积积分 $\int_0^xF(y)dy$ 的奇偶性与 $F$ 相反，不要混淆。

===Q8===
【答案】C
【解】
**① 作线性变换。** 令
$$y_1=x_1+kx_2,\quad y_2=x_1+x_3,\quad y_3=x_1-2x_2+(k+2)x_3,$$
即 $y=Px$，其中 $P=\begin{pmatrix}1&k&0\\1&0&1\\1&-2&k+2\end{pmatrix}$。
**② $P$ 可逆时不合要求。** $|P|=-(k+2)(k-1)$。若 $|P|\ne0$，则 $f=y_1^2+y_2^2-y_3^2$，负惯性指数为 1，不满足题设。
**③ $P$ 不可逆时逐个检验。** 故 $k=1$ 或 $k=-2$。当 $k=1$ 时 $f=(x_1+x_2)^2+(x_1+x_3)^2-(x_1-2x_2+3x_3)^2$，取 $(x_1,x_2,x_3)=(0,0,1)$ 得 $f=-8<0$，负惯性指数至少为 1，不合；当 $k=-2$ 时 $f=(x_1+x_3)^2\ge0$，负惯性指数为 0，符合要求。选 C。
【思路】把三个平方项作为新变量写成 $y=Px$，先由 $|P|=0$ 缩小 $k$ 的范围，再回到原二次型检验半正定性。
【易错】$P$ 不可逆时不能直接由 $y_1^2+y_2^2-y_3^2$ 下结论，必须验证原二次型；负惯性指数为 0 等价于二次型半正定，可找一个使函数值为负的点来排除。

===Q9===
【答案】C
【解】
**① 翻译条件。** 方程组 $Ax=0$ 与 $Bx=0$ 有非零公共解，意味着存在 $x\ne0$ 使 $Ax=Bx=0$，从而 $r(A)<n,\ r(B)<n$。
**② A、B 成立。** (A) 中两方程组分别等价于 $A^TAv=0,\ A^Tu+v=0$ 与 $A^Tu+v=0,\ Av=0$；因 $r(A)<n$，可取 $v=0$ 及 $u\ne0$ 满足 $A^Tu=0$，得到非零公共解。(B) 中两方程组分别为 $Eu+Av=0,\ ABv=0$ 与 $Eu+ABv=0,\ Bv=0$；取题设公共解 $w\ne0$（$Aw=Bw=0$），令 $u=0,v=w$，则四个方程全部成立，故 (B) 也有非零公共解。
**③ D 成立。** 用行变换 $R_1\leftarrow R_1-AB\,R_2$ 把 $\begin{pmatrix}A&AB\\O&E\end{pmatrix}$ 化为 $\begin{pmatrix}A&O\\O&E\end{pmatrix}$；用行变换 $R_2\leftarrow R_2-BA\,R_1$ 把 $\begin{pmatrix}O&E\\A&BA\end{pmatrix}$ 化为 $\begin{pmatrix}O&E\\A&O\end{pmatrix}$。二者均为行等价变换，秩都是 $r(A)+n$ 且解集相同，故 (D) 正确。
**④ C 不成立。** (C) 中两个矩阵的秩都等于 $2r(A)$，但秩相同不代表解集相同。取 $n=2,\ A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$：第一组要求 $u_2=-v_1,\ v_2=0$（$u_1,v_1$ 自由），第二组要求 $u_2=0,\ v_1=0$（$u_1,v_2$ 自由），解集不同，故"同解"错误。选 C。
【思路】把"非零公共解"转化为分块矩阵秩小于 $2n$，对 A、B、D 用分块行列变换验证；对 C 用反例说明秩相同但解集不同。
【易错】"同解"指两个方程组的解集合完全相同，仅维数（秩）相同不够；分块矩阵作行变换时要保证变换可逆，才能保持解集不变。

===Q10===
【答案】C
【解】
**① 命题①错误。** 实对称矩阵合同的充要条件是正负惯性指数相同。$A,B$ 可逆只保证都不含零特征值，但惯性指数可以不同（如 $A=E,\ B=-E$），故不一定存在 $P$ 使 $P^TAP=B$。
**② 命题②正确。** $A$ 可逆且实对称，则 $A^2$ 正定，存在正交矩阵 $Q$ 使 $Q^TA^2Q=E$，即 $A^2=(Q^{-1})^T(Q^{-1})$；取 $P=Q^{-1}$ 即得 $A^2=P^TP$。
**③ 命题③正确。** 同理 $B^2$ 也正定，故 $A^2$ 与 $B^2$ 合同，存在可逆 $P$ 使 $P^TA^2P=B^2$。
**④ 命题④正确。** 取 $P=A$，则 $P^{-1}ABP=A^{-1}ABA=BA$，恒成立。
四个命题中成立 3 个，选 C。
【思路】逐条辨析：合同看惯性指数，正定矩阵可合同于单位阵，相似变换取 $P=A$ 即可交换 $AB$ 与 $BA$。
【易错】$A^2$ 正定的原因是对任意 $x\ne0$，$x^TA^2x=(Ax)^T(Ax)>0$（$A$ 可逆）；勿把"可逆"与"正定"混为一谈。

===Q11===
【答案】$\mathrm{e}^{\frac12}$
【解】
**① 取对数化为乘积极限。** 设所求极限为 $L$，则
$$\ln L=\lim_{x\to+\infty}\frac{x}{\ln x}\ln\left(\frac{x^{\frac1x}+1}{2}\right)=\lim_{x\to+\infty}\frac{x}{\ln x}\ln\left(1+\frac{x^{\frac1x}-1}{2}\right).$$
**② 用等价无穷小。** $x^{\frac1x}=\mathrm{e}^{\frac{\ln x}{x}}=1+\dfrac{\ln x}{x}+o\!\left(\dfrac{\ln x}{x}\right)$，故 $x^{\frac1x}-1\sim\dfrac{\ln x}{x}$，进而 $\ln\left(1+\dfrac{x^{1/x}-1}{2}\right)\sim\dfrac{\ln x}{2x}$。
**③ 求极限并还原。** $\ln L=\lim\limits_{x\to+\infty}\dfrac{x}{\ln x}\cdot\dfrac{\ln x}{2x}=\dfrac12$，故 $L=\mathrm{e}^{1/2}$。
【思路】$1^\infty$ 型取对数，把底数写成 $1+u$ 后用 $\ln(1+u)\sim u$，其中 $x^{1/x}-1\sim\frac{\ln x}{x}$。
【易错】指数是 $\dfrac{x}{\ln x}$ 而不是 $\dfrac1{\ln x}$；若在换元 $t=\ln x$ 后忘记 $x=\mathrm{e}^t$，会使主项相消关系出错。

===Q12===
【答案】$-1$
【解】
**① 先求 $y(0)$。** 令 $x=0$，方程变为 $0+0+1=0+\mathrm{e}^{y(0)}$，故 $y(0)=0$。
**② 两边对 $x$ 求导。** 记 $u=xy$，则
$$y+xy'+\mathrm{e}^{u^2}(y+xy')=1+\mathrm{e}^y y'.$$
**③ 代入 $x=0,y=0$。** 此时 $u=0$，得 $0+0+1\cdot(0+0)=1+\mathrm{e}^0y'(0)$，故 $y'(0)=-1$。
【思路】先用 $x=0$ 定出隐函数初值，再对方程两边求导并代值，注意变上限积分的导数要乘上限的导数。
【易错】$\left(\int_0^{xy}\mathrm{e}^{t^2}dt\right)'=\mathrm{e}^{x^2y^2}(y+xy')$，不能只写 $\mathrm{e}^{x^2y^2}$；$x=0$ 时积分上限为 0，边界项中的 $\mathrm{e}^{u^2}=1$。

===Q13===
【答案】$-\dfrac{\pi}{3}$
【解】
**① 分部积分。** 取 $u=2\pi-x,\ dv=y''(x)dx$，则
$$\int_0^{2\pi}(2\pi-x)y''(x)dx=\Big[(2\pi-x)y'(x)\Big]_0^{2\pi}+\int_0^{2\pi}y'(x)dx=-2\pi y'(0)+y(2\pi)-y(0).$$
**② 确定 $x$ 与 $t$ 的对应。** $\dfrac{dx}{dt}=2+\cos t>0$，故 $x(t)$ 严格递增；$x=0$ 对应 $t=0$，$x=2\pi$ 对应 $t=\pi$。
**③ 求函数值。** $y(2\pi)=\ln(\sin\pi+\mathrm{e}^\pi)=\pi$，$y(0)=\ln(0+1)=0$。
**④ 求 $y'(0)$。** $\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}=\dfrac{\cos t+\mathrm{e}^t}{\sin t+\mathrm{e}^t}\cdot\dfrac1{2+\cos t}$，令 $t=0$ 得 $y'(0)=\dfrac{2}{1}\cdot\dfrac13=\dfrac23$。
**⑤ 代入得结果。** 原式 $=-2\pi\cdot\dfrac23+\pi-0=-\dfrac{\pi}{3}$。
【思路】分部积分把 $y''$ 降为 $y'$ 与 $y$，再由参数方程确定 $x=0,2\pi$ 对应的参数值，最后用链式法则求 $y'(0)$。
【易错】$x=2t+\sin t$ 在 $t=2\pi$ 时等于 $4\pi$ 而非 $2\pi$，故积分上限 $2\pi$ 对应的是 $t=\pi$；参数方程求导必须写 $\frac{dy/dt}{dx/dt}$。

===Q14===
【答案】$\dfrac{5\pi}{4}-2$
【解】
**① 求交点。** 由 $1+\cos\theta=1$ 得 $\cos\theta=0$，即 $\theta=\dfrac\pi2,\ \dfrac{3\pi}2$。
**② 写出公共部分面积。** 当 $\cos\theta\ge0$ 即 $|\theta|\le\dfrac\pi2$ 时 $1+\cos\theta\ge1$，公共部分由圆 $r=1$ 界定；其余角度由心形线 $r=1+\cos\theta$ 界定。故
$$S=\frac12\int_{-\frac\pi2}^{\frac\pi2}1^2\,d\theta+\frac12\int_{\frac\pi2}^{\frac{3\pi}2}(1+\cos\theta)^2\,d\theta.$$
**③ 计算两段。** 第一段为 $\dfrac\pi2$。第二段展开 $(1+\cos\theta)^2=1+2\cos\theta+\cos^2\theta$，积分得
$$\frac12\left[\pi+2\left(\sin\frac{3\pi}{2}-\sin\frac\pi2\right)+\frac\pi2\right]=\frac12\left(\pi-4+\frac\pi2\right)=\frac{3\pi}{4}-2.$$
**④ 合并。** $S=\dfrac\pi2+\dfrac{3\pi}4-2=\dfrac{5\pi}4-2$。
【思路】先求两曲线交点确定分段角度，再按"取较小 $r$"的原则分两段用极坐标面积公式 $\frac12\int r^2d\theta$。
【易错】公共部分在 $|\theta|\le\frac\pi2$ 取的是圆 $r=1$，不是心形线；$\int_{\pi/2}^{3\pi/2}2\cos\theta\,d\theta=-4$，不要漏掉负号。

===Q15===
【答案】$(-\infty,-2]$
【解】
**① 转为求二元函数最小值。** 不等式恒成立等价于 $A\le\min\limits_{a,b\in\mathbb R}\left[a^4+b^4-(a+b)^2\right]$。记 $f(a,b)=a^4+b^4-(a+b)^2$。
**② 求驻点。** $\dfrac{\partial f}{\partial a}=4a^3-2(a+b)=0$，$\dfrac{\partial f}{\partial b}=4b^3-2(a+b)=0$。两式相减得 $a^3=b^3\Rightarrow a=b$，代回得 $4a^3-4a=0$，故 $a=0,\pm1$，驻点为 $(0,0),(1,1),(-1,-1)$。
**③ 判别极值。** $f_{aa}=12a^2-2,\ f_{ab}=-2,\ f_{bb}=12b^2-2$。在 $(1,1),(-1,-1)$ 处 $AC-B^2=(10)(10)-4=96>0$ 且 $A=10>0$，为极小值点，$f(1,1)=f(-1,-1)=1+1-4=-2$。
**④ 确认全局最小。** 当 $|a|\to\infty$ 或 $|b|\to\infty$ 时 $f\to+\infty$，故 $-2$ 为全局最小值，从而 $A\le-2$，即 $A\in(-\infty,-2]$。
【思路】把恒成立问题化为求 $f(a,b)$ 的最小值，用偏导为零找驻点，再用二阶判别与无穷远处的趋势确认全局最小值。
【易错】$(0,0)$ 处 $AC-B^2=4-4=0$，判别法失效，需另作判断：沿 $b=a$ 取充分小的 $a\ne0$ 时 $f=2a^4-4a^2<0$，故原点不是最小值点；不要把 $f(0,0)=0$ 当成最小值。

===Q16===
【答案】$2$
【解】
**① 由 $A$ 不可逆得到特征值 0。** $A$ 为奇异矩阵，故 $\lambda=0$ 是 $A$ 的特征值。
**② 由 $(A+E)B=O$ 得到特征值 $-1$。** 因 $r(B)=2>0$，$B$ 至少有两个线性无关的列向量 $\alpha_1,\alpha_2$，它们满足 $(A+E)\alpha_i=0$，即 $A\alpha_i=-\alpha_i$。故 $-1$ 是特征值且至少有两个线性无关的特征向量，代数重数至少为 2。
**③ 确定 $A$ 的全部特征值。** $A$ 是三阶矩阵，已有 0 与至少二重的 $-1$，故 $\lambda(A)=0,-1,-1$。
**④ 求行列式。** $A+2E$ 的特征值为 $2,1,1$，故 $|A+2E|=2\times1\times1=2$。
【思路】把矩阵方程 $(A+E)B=O$ 与 $r(B)=2$ 转化为 $-1$ 的几何重数至少为 2，从而确定 $A$ 的全部特征值，再由特征值求行列式。
【易错】$B\ne O$ 仅能保证 $-1$ 是特征值；正是 $r(B)=2$ 才保证 $-1$ 的重数至少为 2，否则无法确定第三个特征值。

===Q17===
【答案】$\dfrac{\sqrt2\pi}{24}-\dfrac{\sqrt2}{9}$
【解】
**① 用直线 $y=x$ 分割区域。** $D$ 是单位圆内满足 $x+y\ge0$ 的半圆。用 $y=x$ 分为 $D_1:\{y\le x\}$ 与 $D_2:\{y\ge x\}$。$D_2$ 关于 $y$ 轴对称，而被积函数 $\dfrac{xy^2}{1+x^2+y^2}$ 关于 $x$ 为奇函数，故 $\iint_{D_2}\dfrac{xy^2}{1+x^2+y^2}dxdy=0$。
**② 在 $D_1$ 上用极坐标。** $D_1$ 对应 $-\dfrac\pi4\le\theta\le\dfrac\pi4,\ 0\le r\le1$，于是
$$I=2\int_0^{\frac\pi4}\cos\theta\sin^2\theta\,d\theta\int_0^1\frac{r^4}{1+r^2}\,dr.$$
**③ 分别计算两个单积分。** $\int_0^{\pi/4}\cos\theta\sin^2\theta\,d\theta=\left[\dfrac{\sin^3\theta}{3}\right]_0^{\pi/4}=\dfrac{\sqrt2}{12}$；又 $\dfrac{r^4}{1+r^2}=r^2-1+\dfrac1{1+r^2}$，故 $\int_0^1\dfrac{r^4}{1+r^2}dr=\dfrac13-1+\dfrac\pi4=\dfrac\pi4-\dfrac23$。
**④ 合并。** $I=2\cdot\dfrac{\sqrt2}{12}\left(\dfrac\pi4-\dfrac23\right)=\dfrac{\sqrt2\pi}{24}-\dfrac{\sqrt2}{9}$。
【思路】利用对称性与被积函数关于 $x$ 的奇性消去一半区域，再用极坐标分离变量，化为两个单积分的乘积。
【易错】$D_2$ 关于 $y$ 轴对称的前提是它同时落在 $x+y\ge0$ 的半圆内；$\int_0^1\frac{r^4}{1+r^2}dr$ 要先做多项式除法，不能误用 $\ln(1+r^2)$。

===Q18===
【答案】切线方程为 $y=2x+2$
【解】
**① 由连续性求 $f(0)$ 与 $f(1)$。** $f$ 是连续的奇函数，故 $f(0)=0$。对题给等式两边取 $x\to0$：左边 $\to\lim\limits_{x\to0}[2f(x)+f(-x)]=3f(0)=0$，故右边分式极限为 1，从而分子 $\sqrt{1+2f(\mathrm{e}^x)}-\sqrt{1-f(1-\tan x)}\to0$，即 $\sqrt{1+2f(1)}=\sqrt{1-f(1)}$，解得 $f(1)=0$。
**② 有理化并求 $f'(1)$。** 此时分母根号和趋于 $\sqrt{1+2f(1)}+\sqrt{1-f(1)}=2$，故
$$1=\lim_{x\to0}\frac{2f(\mathrm{e}^x)+f(1-\tan x)}{2x}.$$
利用 $f(1)=0$ 拆项：
$$\frac{2f(\mathrm{e}^x)+f(1-\tan x)}{2x}=\frac{f(\mathrm{e}^x)-f(1)}{\mathrm{e}^x-1}\cdot\frac{\mathrm{e}^x-1}{x}+\frac{f(1-\tan x)-f(1)}{-\tan x}\cdot\frac{-\tan x}{2x}.$$
令 $x\to0$，两项分别趋于 $f'(1)$ 与 $-\dfrac12f'(1)$，故 $\dfrac12f'(1)=1$，即 $f'(1)=2$。
**③ 转到 $x=-1$。** 奇函数的导函数为偶函数，故 $f(-1)=-f(1)=0$，$f'(-1)=f'(1)=2$。
**④ 写切线方程。** $y-0=2(x+1)$，即 $y=2x+2$。
【思路】先由奇函数连续性与等式极限定出 $f(0)=f(1)=0$，再有理化并用导数定义凑出 $f'(1)$，最后利用奇函数导数为偶函数得到 $x=-1$ 处的数据。
【易错】题目只保证 $f$ 在 $x=1$ 处可导，不能对原极限使用洛必达法则，必须先有理化再用导数定义；分子有理化后分母的极限是 2 而不是 1。

===Q19===
【答案】(I) $\dfrac{\partial^2f}{\partial u\partial v}=\mathrm{e}^{u+v}$；(II) $z(x,y)=\mathrm{e}^{3x-y}+5x^2+5y^2+1$
【解】
**（I）求 $\dfrac{\partial^2f}{\partial u\partial v}$。**
**① 用链式法则求二阶偏导。** 由 $u=2x+y,\ v=x-2y$ 得
$$z_x=2f_u+f_v,\qquad z_y=f_u-2f_v,$$
$$z_{xx}=4f_{uu}+4f_{uv}+f_{vv},\quad z_{xy}=2f_{uu}-3f_{uv}-2f_{vv},\quad z_{yy}=f_{uu}-4f_{uv}+4f_{vv}.$$
**② 代入方程。** $2z_{xx}-3z_{xy}-2z_{yy}=25f_{uv}$，而 $u+v=3x-y$，故 $25f_{uv}=25\mathrm{e}^{3x-y}=25\mathrm{e}^{u+v}$，得 $f_{uv}=\mathrm{e}^{u+v}$。
**（II）求 $z(x,y)$ 的表达式。**
**① 对 $v$ 积分求 $f_u$。** 由 $f_{uv}=\mathrm{e}^{u+v}$ 得 $f_u=\mathrm{e}^{u+v}+C(u)$。令 $v=0$，由 $f_u(u,0)=\mathrm{e}^u+C(u)=\mathrm{e}^u+2u$ 得 $C(u)=2u$，故 $f_u=\mathrm{e}^{u+v}+2u$。
**② 对 $u$ 积分求 $f$。** $f=\mathrm{e}^{u+v}+u^2+C(v)$。令 $u=0$，由 $f(0,v)=\mathrm{e}^v+C(v)=\mathrm{e}^v+v^2+1$ 得 $C(v)=v^2+1$，故 $f(u,v)=\mathrm{e}^{u+v}+u^2+v^2+1$。
**③ 回代原变量。** $u=2x+y,\ v=x-2y$，故
$$z=\mathrm{e}^{3x-y}+(2x+y)^2+(x-2y)^2+1=\mathrm{e}^{3x-y}+5x^2+5y^2+1.$$
【思路】用链式法则把原方程化为关于 $f$ 的混合偏导方程，再对 $v$、$u$ 依次积分并利用两个边界条件定出积分"常数"。
【易错】积分"常数"是另一变量的函数，必须由给定边界条件确定；$u+v=(2x+y)+(x-2y)=3x-y$，不是 $3x-2y$。

===Q20===
【答案】(I) $f(x)=\mathrm{e}^{x/2}+\mathrm{e}^{-x/2}$；(II) $\left(\dfrac{4}{\mathrm{e}+1},\ \dfrac{\mathrm{e}}2+\dfrac1{2\mathrm{e}}+\dfrac{2\mathrm{e}}{\mathrm{e}^2-1}\right)$
【解】
**（I）求 $f(x)$。**
**① 建立微分方程。** 由 $f'=\dfrac12g$ 得 $f''=\dfrac12g'=\dfrac14f$，即 $f''-\dfrac14f=0$，通解 $f=C_1\mathrm{e}^{x/2}+C_2\mathrm{e}^{-x/2}$。
**② 代入初值。** $f(0)=C_1+C_2=2$，$f'(0)=\dfrac{C_1-C_2}{2}=0$，故 $C_1=C_2=1$，得 $f(x)=\mathrm{e}^{x/2}+\mathrm{e}^{-x/2}$。
**（II）求形心坐标。**
**① 写弧长微元。** $f'=\dfrac12\mathrm{e}^{x/2}-\dfrac12\mathrm{e}^{-x/2}$，故
$$ds=\sqrt{1+(f')^2}\,dx=\left(\frac12\mathrm{e}^{x/2}+\frac12\mathrm{e}^{-x/2}\right)dx.$$
**② 求弧长。** $L=\int_0^2ds=\left[\mathrm{e}^{x/2}-\mathrm{e}^{-x/2}\right]_0^2=\mathrm{e}-\dfrac1{\mathrm{e}}$。
**③ 求横坐标。** $\int_0^2x\,ds=\int_0^2x\left(\frac12\mathrm{e}^{x/2}+\frac12\mathrm{e}^{-x/2}\right)dx=2\left(\mathrm{e}-\frac1{\mathrm{e}}\right)-2\left(\mathrm{e}+\frac1{\mathrm{e}}\right)+4=4-\dfrac4{\mathrm{e}}$，故 $\bar x=\dfrac{4-4/\mathrm{e}}{\mathrm{e}-1/\mathrm{e}}=\dfrac4{\mathrm{e}+1}$。
**④ 求纵坐标。** $\int_0^2y\,ds=\int_0^2\left(\mathrm{e}^{x/2}+\mathrm{e}^{-x/2}\right)\left(\frac12\mathrm{e}^{x/2}+\frac12\mathrm{e}^{-x/2}\right)dx=\int_0^2\left(\frac12\mathrm{e}^x+\frac12\mathrm{e}^{-x}+1\right)dx=\dfrac{\mathrm{e}^2}{2}-\dfrac1{2\mathrm{e}^2}+2$。
于是 $\bar y=\dfrac{\frac{\mathrm{e}^2}{2}-\frac1{2\mathrm{e}^2}+2}{\mathrm{e}-\frac1{\mathrm{e}}}=\dfrac{\mathrm{e}}2+\dfrac1{2\mathrm{e}}+\dfrac{2\mathrm{e}}{\mathrm{e}^2-1}$。
【思路】由微分关系消去 $g$ 得二阶常系数方程求 $f$，再用弧长微元 $ds=\sqrt{1+(f')^2}\,dx$ 把形心坐标写成定积分 $\bar x=\frac{\int x\,ds}{\int ds},\ \bar y=\frac{\int y\,ds}{\int ds}$ 计算。
【易错】$\sqrt{1+(f')^2}$ 化简为 $\frac12\mathrm{e}^{x/2}+\frac12\mathrm{e}^{-x/2}$，不能直接写成 $\sqrt{1+(f')^2}=f'(x)$；形心公式的分母是弧长 $L=\mathrm{e}-\frac1{\mathrm{e}}$，不是区间长度 2。

===Q21===
【答案】(I) 对任意正整数 $n$ 均有 $x_n>1$；(II) 数列单调递减且有下界，故收敛，$\lim\limits_{n\to\infty}x_n=1$
【解】
**（I）证明 $x_n>1$。**
**① 构造辅助函数。** 设 $f(x)=x^2-1-\ln x\ (x\ge1)$，则 $f'(x)=2x-\dfrac1x>0$，$f(1)=0$，故 $x>1$ 时 $f(x)>0$，即 $x^2-1>\ln x$，从而 $\dfrac{x^2}{1+\ln x}>1$。
**② 归纳。** $x_1=a>1$，若 $x_n>1$ 则 $\dfrac{x_n^2}{1+\ln x_n}>1$，故 $x_{n+1}=1+\ln\left(\dfrac{x_n^2}{1+\ln x_n}\right)>1$。由数学归纳法，一切 $x_n>1$。
**（II）证明收敛并求极限。**
**① 化为差分。** 当 $x>1$，
$$x_{n+1}-x_n=1+2\ln x_n-\ln(1+\ln x_n)-x_n=:g(x_n).$$
**② 判断 $g$ 的符号。** 记 $\varphi(x)=1+2\ln x-x-x\ln x$，则
$$g'(x)=\frac2x-\frac1{x(1+\ln x)}-1=\frac{\varphi(x)}{x(1+\ln x)},\qquad \varphi'(x)=\frac2x-2-\ln x<0\quad(x>1).$$
因 $\varphi(1)=0$ 且 $\varphi$ 递减，故 $x>1$ 时 $\varphi(x)<0$，从而 $g'(x)<0$、$g(x)<g(1)=0$，即 $x_{n+1}<x_n$。
**③ 收敛性与极限。** $\{x_n\}$ 单调递减且以 1 为下界，故收敛。设 $\lim\limits_{n\to\infty}x_n=A\ge1$，对递推式取极限得 $A=1+\ln\left(\dfrac{A^2}{1+\ln A}\right)$，即 $g(A)=0$；由 $g$ 在 $(1,+\infty)$ 严格为负知唯一解为 $A=1$。故 $\lim\limits_{n\to\infty}x_n=1$。
【思路】用 $x^2-1>\ln x$ 做归纳证明下界，再构造函数 $g(x)$ 研究差分符号得单调性，最后取极限解不动点方程。
【易错】$\varphi'(x)=\frac2x-2-\ln x$ 在 $x>1$ 恒负，需 $x(1+\ln x)>0$ 才能得 $g'<0$；取极限时不能直接断言 $A>1$，否则 $g(A)<0$ 与 $g(A)=0$ 矛盾，正是这一点说明 $A=1$。

===Q22===
【答案】(I) $a=1$ 或 $a=9$；(II) $a=9$ 时不存在可逆矩阵 $P$；$a=1$ 时存在，$P=\begin{pmatrix}k_1&2k_1+k_2&0\\k_1&k_2&0\\0&0&k_3\end{pmatrix}$，其中 $k_1\ne0,\ k_3\ne0$
【解】
**（I）求 $a$。**
**① 求特征多项式。** $|A-\lambda E|=(2-\lambda)\left[\lambda^2-(a+7)\lambda+6a+10\right]$。
**② 排除 $\lambda=2$ 为三重根。** 若 $\lambda=2$ 是三重根，需 $a+7=4$ 且 $6a+10=4$，无解。
**③ 排除 $\lambda=2$ 为二重根。** 若 $\lambda=2$ 是二次因式的根，则 $4-2(a+7)+6a+10=0\Rightarrow a=0$。此时 $A-2E=\begin{pmatrix}3&0&0\\1&0&0\\0&0&0\end{pmatrix}$，$r(A-2E)=1$，$\lambda=2$ 对应两个线性无关特征向量，$A$ 可对角化，舍去。
**④ 二次因式有重根。** $\Delta=(a+7)^2-4(6a+10)=a^2-10a+9=(a-1)(a-9)=0$，故 $a=1$ 或 $a=9$。当 $a=1$ 时 $\lambda=4$ 为二重根，$A-4E=\begin{pmatrix}1&-1&0\\1&-1&0\\0&0&-2\end{pmatrix}$，$r(A-4E)=2$，只有一个线性无关特征向量，不可对角化；当 $a=9$ 时 $\lambda=8$ 为二重根，$A-8E=\begin{pmatrix}-3&-9&0\\1&3&0\\0&0&-6\end{pmatrix}$，$r(A-8E)=2$，同样不可对角化。故 $a=1$ 或 $a=9$。
**（II）判断并求 $P$。**
**① $a=9$ 时不存在。** 此时 $B=\begin{pmatrix}20&2&0\\0&20&0\\0&0&2\end{pmatrix}$，特征值为 $20,20,2$，与 $A$ 的特征值 $8,8,2$ 不同，故 $A$ 与 $B$ 不相似，不存在这样的 $P$。
**② $a=1$ 时构造 $P$。** 此时 $B=\begin{pmatrix}4&2&0\\0&4&0\\0&0&2\end{pmatrix}$，设 $P=(\alpha_1,\alpha_2,\alpha_3)$，条件 $P^{-1}AP=B$ 等价于 $A\alpha_1=4\alpha_1,\ A\alpha_2=2\alpha_1+4\alpha_2,\ A\alpha_3=2\alpha_3$。
由 $(A-4E)\alpha_1=0$ 解得 $\alpha_1=(k_1,k_1,0)^T$；由 $(A-4E)\alpha_2=2\alpha_1$ 解得 $\alpha_2=(2k_1+k_2,k_2,0)^T$；由 $(A-2E)\alpha_3=0$ 解得 $\alpha_3=(0,0,k_3)^T$。
**③ 可逆条件。** $P=\begin{pmatrix}k_1&2k_1+k_2&0\\k_1&k_2&0\\0&0&k_3\end{pmatrix}$，$|P|=-2k_1^2k_3\ne0$，取 $k_1\ne0,\ k_3\ne0$ 即可。
【思路】先由特征多项式与"不可对角化"条件定 $a$，再用特征值比较排除 $a=9$；对 $a=1$ 按 $AP=PB$ 逐列解出特征向量与广义特征向量，并验证 $P$ 可逆。
【易错】$a=0$ 时 $\lambda=2$ 虽为二重根但 $r(A-2E)=1$，此时 $A$ 可对角化，必须舍去；相似矩阵特征值必须相同，这是排除 $a=9$ 的最快方法；$P$ 的列顺序要与 $B$ 的若尔当块结构对应，不能随意交换。
