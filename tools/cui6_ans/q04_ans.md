===Q1===
【答案】B
【解】
**① 用拉格朗日中值定理处理 $\alpha$。** 把 $\cos$ 在 $\ln(1+x)$ 与 $x$ 之间用中值定理：
$$\alpha=\cos\ln(1+x)-\cos x=[x-\ln(1+x)]\sin\xi,\qquad \ln(1+x)<\xi<x\ (x>0).$$
**② 求 $\alpha$ 的主项。** 由 $\dfrac{\ln(1+x)}{x}<\dfrac{\xi}{x}<1$ 及夹逼定理得 $\xi/x\to1$；又 $x-\ln(1+x)\sim\dfrac{x^2}{2}$，所以
$$\lim_{x\to0^+}\frac{\alpha}{x^3}=\lim_{x\to0^+}\frac{\sin\xi}{\xi}\cdot\frac{\xi}{x}\cdot\frac{x-\ln(1+x)}{x^2}=1\cdot1\cdot\frac12=\frac12,$$
即 $\alpha\sim\dfrac12x^3$。
**③ 求 $\beta$ 的主项。** 上限 $1-\cos x\to0$，用洛必达法则，注意 $\arctan u\sim u$、$1-\cos x\sim\dfrac{x^2}{2}$：
$$\lim_{x\to0^+}\frac{\beta}{x^3}=\frac13\lim_{x\to0^+}\frac{\arctan(1-\cos x)\sin x}{x^2\sqrt{1-\cos x}}=\frac13\lim_{x\to0^+}\frac{\sqrt{1-\cos x}}{x}=\frac{1}{3\sqrt2},$$
即 $\beta\sim\dfrac{1}{3\sqrt2}x^3$。
**④ 比较阶。** $\alpha,\beta$ 都是 $x^3$ 的同阶无穷小，但 $\alpha/\beta\to\dfrac{3\sqrt2}{2}\ne1$，不等价，选 B。
【思路】对 $\alpha$ 用拉格朗日中值定理、对 $\beta$ 用变上限积分求导加洛必达法则，分别求出 $x^3$ 的系数再比较比值是否为 1。
【易错】同阶只要求比值趋于非零常数，等价还要求比值恰为 1。$\beta$ 的被积函数 $\arctan t/\sqrt t\sim\sqrt t$，积分主项是 $\frac23u^{3/2}$，不能漏掉平方根带来的 $3/2$ 次幂。
===Q2===
【答案】D
【解】
**① 讨论 $b\le0$。** $f'(x)=ae^x-b$，当 $b\le0$ 时 $f'(x)\ge a>0$，$f$ 严格递增至多一个零点，不合题意。
**② 求唯一极值点。** 当 $b>0$ 时由 $f'(x)=0$ 得 $x=\ln\dfrac{b}{a}$；又 $f''(x)=ae^x>0$，故该点是唯一极小值点也是最小值点。因 $x\to\pm\infty$ 时 $f(x)\to+\infty$，恰有两个零点等价于最小值小于 0。
**③ 解不等式。** 
$$f\!\left(\ln\frac ba\right)=ae^{\ln(b/a)}-b\ln\frac ba=b\left(1-\ln\frac ba\right)<0\iff \ln\frac ba>1\iff \frac ba>e.$$
故选 D。
【思路】先按 $b$ 的符号分类，再找唯一极小值点，用「最小值小于 0」配合两端趋于 $+\infty$ 得到两个零点的充要条件。
【易错】$a>0$ 保证 $f''>0$，极小值点是全局最小值点；但必须同时验证 $x\to-\infty$ 时 $f\to+\infty$（因 $-bx\to+\infty$），否则两个零点无从谈起。
===Q3===
【答案】C
【解】
**① 由相似关系化简几何量。** 设液面半径 $r$、水深 $h$、体积 $V$、面积 $S$。容器高 $8$、口半径 $4$，故 $h=2r$，即 $r=\dfrac h2$；于是
$$V=\frac13\pi r^2h=\frac{\pi}{12}h^3,\qquad S=\pi r^2=\frac{\pi}{4}h^2.$$
**② 由注水速度求 $dh/dt$。** $\dfrac{dV}{dt}=\dfrac{\pi}{4}h^2\dfrac{dh}{dt}=5$。当 $h=2$ 时 $\dfrac{\pi}{4}\cdot4\cdot\dfrac{dh}{dt}=5$，故 $\dfrac{dh}{dt}=\dfrac{5}{\pi}\text{cm/s}$。
**③ 求面积增长率。** 由 $r=\dfrac h2$ 得 $\dfrac{dr}{dt}=\dfrac12\dfrac{dh}{dt}=\dfrac{5}{2\pi}$；$h=2$ 时 $r=1$，故
$$\frac{dS}{dt}=2\pi r\frac{dr}{dt}=2\pi\cdot1\cdot\frac{5}{2\pi}=5\text{cm}^2/\text{s}.$$
选 C。
【思路】用圆锥相似关系把 $V,S$ 都写成水深 $h$ 的单变量函数，先由 $dV/dt$ 反解 $dh/dt$，再链式求导得 $dS/dt$。
【易错】倒置圆锥尖端在下，相似关系是 $h=2r$ 而非 $r=2h$；液面面积变化率须对 $S=\pi r^2$ 求导，不能直接拿体积变化率代入。
===Q4===
【答案】C
【解】
**① 排除 (A)。** $f(x)=x^3$ 在 $x=0$ 的邻域严格递增，但 $f'(0)=0$，故 (A) 错。
**② 排除 (B)。** $f(x)=|x|^{3/2}$ 在 $x\ne0$ 处 $f''(x)=\dfrac{3}{4\sqrt{|x|}}>0$，在 $0$ 附近为凹函数，但 $f''(0)$ 不存在，故 (B) 错。
**③ 排除 (D)。** 取 $x_0=1$，$f(x)=(x-1)^2$ 在 $x_0^3=1$ 处 $f''(1)=2>0$（凹）；而 $h(x)=f(x^3)=(x^3-1)^2$ 有 $h''(1)=-6<0$，凹凸性改变，故 (D) 错。
**④ 验证 (C)。** $x\mapsto x^3$ 在 $\mathbb{R}$ 上严格递增：若 $f$ 在 $x_0^3$ 的邻域单调递增，则 $x_1<x_2$ 时 $x_1^3<x_2^3$，从而 $f(x_1^3)<f(x_2^3)$，即 $f(x^3)$ 在 $x_0$ 的邻域单调递增。选 C。
【思路】用 $x^3$、$|x|^{3/2}$、$(x-1)^2$ 三个反例逐个排除，再利用 $x^3$ 严格保序说明复合函数保持单调性。
【易错】严格单调递增不保证 $f'(x_0)>0$（导数可为 0）；凹凸性在复合 $f(x^3)$ 后未必保持，因为内层在 $x_0\ne0$ 处二阶导数不为 0，会改变二阶导符号。
===Q5===
【答案】A
【解】
**① 比较 $I$ 与 $J$。** 三个积分同在 $[0,1]$ 上，只需比较被积函数。当 $x>0$ 时 $e^x-1>x>\ln(1+x)$，所以
$$\int_0^1\frac{e^x-1}{x}\,dx>\int_0^1\frac{\ln(1+x)}{x}\,dx,\qquad I>J.$$
**② 比较 $J$ 与 $K$。** 令 $g(x)=(1+x)\ln(1+x)-x$，则
$$g'(x)=\ln(1+x)+1-\frac{1}{1+x}=\ln(1+x)+\frac{x}{1+x}>0\quad(x>0),$$
且 $g(0)=0$，故 $g(x)>0$，即 $\dfrac{\ln(1+x)}{x}>\dfrac{1}{1+x}$（$x\in(0,1]$）。积分得 $J>K$。
**③ 结论。** $I>J>K$，选 A。
【思路】把三个积分化到同一区间上比较被积函数：$e^x-1>x>\ln(1+x)$ 给出 $I>J$，辅助函数 $(1+x)\ln(1+x)-x$ 单调递增给出 $J>K$。
【易错】端点 $x=0$ 处两个分式都是 $0/0$ 型，比较应在 $(0,1]$ 上进行；比较 $J,K$ 不能直接交叉相乘后默认不等号方向，需验证 $1+x>0$。
===Q6===
【答案】D
【解】
**① 连续性。** $(x,y)\to(0,0)$ 时 $|x+y|\le\sqrt2\sqrt{x^2+y^2}$，而 $\arctan$ 有界，故 $|f(x,y)|\le\sqrt2\sqrt{x^2+y^2}\to0=f(0,0)$，连续。
**② 偏导数。** 由定义
$$f_x(0,0)=\lim_{x\to0}\arctan\frac{1}{|x|}=\frac{\pi}{2},\qquad f_y(0,0)=\lim_{y\to0}\arctan\frac{1}{|y|}=\frac{\pi}{2}.$$
**③ 可微性。** 需验证
$$\lim_{(x,y)\to(0,0)}\frac{f(x,y)-f_x(0,0)x-f_y(0,0)y}{\sqrt{x^2+y^2}}=\lim_{(x,y)\to(0,0)}\frac{x+y}{\sqrt{x^2+y^2}}\left(\arctan\frac{1}{\sqrt{x^2+y^2}}-\frac{\pi}{2}\right)=0.$$
其中 $\dfrac{x+y}{\sqrt{x^2+y^2}}$ 有界（绝对值 $\le\sqrt2$），括号趋于 0，乘积趋于 0，故可微。
**④ 偏导数连续。** $(x,y)\ne(0,0)$ 时
$$f_x(x,y)=\arctan\frac{1}{\sqrt{x^2+y^2}}-\frac{x(x+y)}{\sqrt{x^2+y^2}\,(1+x^2+y^2)}.$$
当 $(x,y)\to(0,0)$，第一项趋于 $\dfrac\pi2$，第二项绝对值 $\le\dfrac{|x||x+y|}{\sqrt{x^2+y^2}}\le\sqrt2|x|\to0$，故 $f_x\to\dfrac\pi2=f_x(0,0)$；同理 $f_y$ 连续。选 D。
【思路】按「连续→偏导存在→可微→偏导连续」四步逐层验证，可微性用有界量乘无穷小量处理。
【易错】$\dfrac{x+y}{\sqrt{x^2+y^2}}$ 的极限不存在但有界，不能说它发散就断定不可微；必须把整项乘上趋于 0 的因子一并判断。
===Q7===
【答案】D
【解】
**① 把和式写成二重和。** 原极限为
$$\lim_{n\to\infty}\frac{1}{n^2}\sum_{i=1}^{2n}\sum_{j=i}^{2n}\frac{j}{n}\sin\frac{i\pi}{2n}.$$
**② 确定步长与区域。** 令 $x=\dfrac jn\in(0,2]$、$y=\dfrac{i}{2n}\in(0,1]$，则 $\Delta x=\dfrac1n$、$\Delta y=\dfrac{1}{2n}$，于是 $\dfrac{1}{n^2}=2\Delta x\Delta y$；条件 $j\ge i$ 等价于 $x=\dfrac jn\ge\dfrac{i}{n}=2y$。
**③ 化为二重积分。** 当 $n\to\infty$，二重和收敛到
$$\int_0^1dy\int_{2y}^22x\sin(\pi y)\,dx,$$
对应选项 D。
【思路】识别二重黎曼和：先固定 $i$ 把内层写成对 $j$ 的求和，再按 $x=j/n,\ y=i/(2n)$ 定网格步长、按 $j\ge i$ 定积分区域 $x\ge2y$。
【易错】$\sin\dfrac{i\pi}{2n}=\sin(\pi y)$，不要误写成 $\sin\dfrac{\pi y}{2}$；内层求和从 $j=i$ 开始，因此下限是 $x=2y$ 而不是 $y$。
===Q8===
【答案】C
【解】
**① 命题①。** 设 $B=(b_{ij})$，则 $C_1=AB=(\alpha_1,\ldots,\alpha_n)B$，其第 $j$ 列为 $\sum_{i=1}^n b_{ij}\alpha_i$，故 $C_1$ 的列向量都可由 $\alpha_1,\ldots,\alpha_n$ 线性表示，①正确。②声称可由 $\beta_i$ 表示，一般不成立：取 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$、$B=\begin{pmatrix}0&0\\1&0\end{pmatrix}$，则 $C_1=AB=\begin{pmatrix}1&0\\0&0\end{pmatrix}$，其列 $(1,0)^T$ 不能由 $\beta_1=(0,0)^T$、$\beta_2=(0,1)^T$ 表示，②错误。
**② 命题③。** $C_2=A+B=(\alpha_1+\beta_1,\ldots,\alpha_n+\beta_n)$，每个列向量都是 $C_3=(A,B)$ 的列向量之和，故③正确。
**③ 命题④。** 由秩的基本不等式，
$$r(C_2)=r(A+B)\le r(A,B)=r(C_3)\le r(A)+r(B),$$
故④正确。正确命题为①③④，选 C。
【思路】把矩阵按列分块，用「乘积的列是左因子的列的线性组合」判断①②，用列空间包含关系判断③，用秩的不等式判断④。
【易错】$C_1=AB$ 的列落在 $A$ 的列空间而非 $B$ 的列空间；$r(A,B)\le r(A)+r(B)$ 是上界而不是等式，不能随意加强。
===Q9===
【答案】A
【解】
**① 翻译条件。** $Ax=0$ 的解都是 $Bx=0$ 的解，等价于 $B$ 的每个行向量都可由 $A$ 的行向量线性表示，即 $r(A)=r\begin{pmatrix}A\\B\end{pmatrix}$；两方程组不同解，等价于行空间不相同，即 $r(A)>r(B)$。记 $A$ 的三行为 $r_1,r_2,r_3$。
**② 表示 $B$ 的行。** 注意 $B$ 的第一行就是 $r_2=(2,1,1,2)$。设 $B$ 的第二行 $s_2=(0,-2,1,1)=c_1r_1+c_2r_2+c_3r_3$，比较第 1、3、4 分量得 $c_1+c_2+c_3=0$、$2c_1+c_2=1$，再比较第 2 分量得 $(a+1)c_1=0$；同理第三行 $s_3=(4,4,1,3)=r_2+r_3$ 无条件成立。
**③ 讨论 $a$。** 当 $a\ne-1$ 时 $c_1=0$，可取 $c_2=1,c_3=-1$ 表示 $s_2$，此时 $r(A)=3>r(B)=2$，两解集不同，符合要求。当 $a=-1$ 时 $r_1=2r_2-r_3$，$r(A)=2=r(B)$，两方程组同解，不合要求。故 $a\ne-1$，选 A。
【思路】把解集包含关系转成行空间的包含关系，直接设系数把 $B$ 的行用 $A$ 的行表示，从相容性条件中分离出 $a+1$ 这个因子。
【易错】「解都是解」只给出行空间包含，还要用「不同解」排除行空间相等的情形；$a=-1$ 时 $A$ 的三行线性相关，恰是同解的临界情形。
===Q10===
【答案】B
【解】
**① 同矩阵多项式可同时对角化。** (A) 中 $B=A-E$，(D) 中 $B=-A+2E$，二者与 $A$ 有相同的特征向量，可用同一个可逆矩阵对角化。
**② 伴随矩阵情形。** (C) 中记 $A_0$、$B_0$ 为选项矩阵，直接相乘得 $A_0B_0=-3E=|A_0|E$，即 $B_0=A_0^*=|A_0|A_0^{-1}$。可逆矩阵与其伴随矩阵有相同的特征向量，故也可同时对角化。
**③ 排除 (B)。** (B) 中第二个矩阵恰是第一个的转置 $A^T$，而该 $A$ 不是对称矩阵，$A$ 与 $A^T$ 的特征向量一般不同，不存在同一个可逆矩阵把它们同时对角化。选 B。
【思路】利用「$f(A)$、$A^{-1}$、$A^*$ 与 $A$ 同特征向量」逐一验证，只剩转置情形不能保证同特征向量。
【易错】$A$ 与 $A^T$ 相似（特征值相同）但特征向量不同，相似≠能由同一个可逆矩阵同时对角化；(C) 中要通过计算发现 $B$ 是 $A$ 的伴随而不是凭对角元素猜测。
===Q11===
【答案】$y=x-1$
【解】
**① 求 $f$ 的斜渐近线。** 因 $x\ge0$ 时 $e^{-x}\to0$，
$$\lim_{x\to+\infty}\frac{f(x)}{x}=\lim_{x\to+\infty}\frac{x+1}{x(1+e^{-x})}=1,$$
$$\lim_{x\to+\infty}[f(x)-x]=\lim_{x\to+\infty}\frac{x+1-x(1+e^{-x})}{1+e^{-x}}=\lim_{x\to+\infty}\frac{1-xe^{-x}}{1+e^{-x}}=1,$$
故 $y=f(x)$ 的斜渐近线为 $y=x+1$。
**② 利用反函数的对称性。** $y=g(x)$ 与 $y=f(x)$ 的图像关于直线 $y=x$ 对称，把 $y=x+1$ 中的 $x,y$ 互换得 $x=y+1$，即 $y=x-1$。
【思路】先求原函数的斜渐近线 $y=kx+b$，再由反函数图像关于 $y=x$ 对称，把渐近线方程中的 $x,y$ 对调。
【易错】不能把 $y=x+1$ 直接当作反函数的渐近线；对称操作是交换 $x,y$，故截距由 $+1$ 变为 $-1$。
===Q12===
【答案】$\dfrac{5\sqrt5}{3}$
【解】
**① 求一阶导数。** $t=0$ 时 $x=0,y=0$。由
$$\frac{dx}{dt}=1+\frac{1}{1+t}=\frac{t+2}{1+t},\qquad \frac{dy}{dt}=e^t,$$
得
$$\frac{dy}{dx}=\frac{e^t(1+t)}{t+2},\qquad \left.\frac{dy}{dx}\right|_{t=0}=\frac12.$$
**② 求二阶导数。** 
$$\frac{d^2y}{dx^2}=\frac{\dfrac{d}{dt}\!\left(\dfrac{e^t(1+t)}{t+2}\right)}{\dfrac{dx}{dt}}=\frac{\dfrac{e^t(t^2+3t+3)}{(t+2)^2}}{\dfrac{t+2}{1+t}}=\frac{e^t(1+t)(t^2+3t+3)}{(t+2)^3},$$
代入 $t=0$ 得 $\left.\dfrac{d^2y}{dx^2}\right|_{t=0}=\dfrac38$。
**③ 代入曲率半径公式。**
$$R=\frac{\left[1+\left(y'\right)^2\right]^{3/2}}{|y''|}=\frac{\left[1+\left(\frac12\right)^2\right]^{3/2}}{\frac38}=\frac{\left(\frac54\right)^{3/2}}{\frac38}=\frac{5\sqrt5}{3}.$$
【思路】参数方程求导公式 $y'=\dfrac{y_t'}{x_t'}$、$y''_{xx}=\dfrac{(y'_x)'_t}{x'_t}$，再代入曲率半径公式。
【易错】二阶导数必须再除以 $dx/dt$，不能只对 $dy/dx$ 关于 $t$ 求导；$t=0$ 对应点 $(0,0)$ 要先验证。
===Q13===
【答案】$\ln|x|-\dfrac{1}{2}\ln(x^2+2x+2)-\arctan(x+1)+C$
【解】
**① 待定系数分解。** 设
$$\frac{2}{x(x^2+2x+2)}=\frac{A}{x}+\frac{Bx+C}{x^2+2x+2},$$
通分比较系数得 $2=A(x^2+2x+2)+x(Bx+C)=(A+B)x^2+(2A+C)x+2A$，故 $A=1,B=-1,C=-2$。
**② 拆分并积分。** 
$$\frac{2}{x(x^2+2x+2)}=\frac1x-\frac{x+2}{x^2+2x+2}=\frac1x-\frac12\frac{2x+2}{x^2+2x+2}-\frac{1}{(x+1)^2+1}.$$
于是
$$I=\ln|x|-\frac12\ln(x^2+2x+2)-\arctan(x+1)+C.$$
【思路】用有理函数部分分式分解，把二次因子拆出导数 $\frac{2x+2}{x^2+2x+2}$ 与剩余常数，分别凑对数与反正切。
【易错】$x^2+2x+2=(x+1)^2+1$ 恒正，其对数无需绝对值；常数项 $C=-2$ 来自比较 $x$ 的一次项系数。
===Q14===
【答案】$x^2y''-3xy'+3y=(x^2-3x+3)e^x$
【解】
**① 由解之差得到齐次解。** $y_2-y_1=-x$ 与 $y_3-y_1=x^3$ 是对应齐次方程的解。设齐次方程为 $y''+p(x)y'+q(x)y=0$。
**② 求 $p(x),q(x)$。** 代入 $y=-x$ 得 $-p-xq=0$；代入 $y=x^3$ 得 $6x+3x^2p+x^3q=0$。联立解得
$$q(x)=\frac{3}{x^2},\qquad p(x)=-\frac{3}{x}.$$
**③ 求非齐次项。** 代入 $y_1=e^x$：
$$f(x)=e^x-\frac3x e^x+\frac{3}{x^2}e^x=\frac{x^2-3x+3}{x^2}e^x.$$
乘以 $x^2$ 化为整式形式，得 $x^2y''-3xy'+3y=(x^2-3x+3)e^x$。
【思路】利用非齐次方程任意两个特解之差是齐次解，由两个齐次解反解出 $p,q$，再代回一个特解确定右端项。
【易错】三个特解互差给出两个齐次解，但 $x$ 与 $x^3$ 在 $x=0$ 处不构成通常意义的基础解系，方程应写成不显含奇点的整式形式；不能直接把 $y_1=e^x$ 当作齐次解。
===Q15===
【答案】$\dfrac{15\pi}{4}\times10^4\text{J}$
【解】
**① 建立坐标系与分层。** 取竖直坐标 $y$，容器顶部为 $y=0$。外壁 $x^2+z^2+y^2=4$（$-2\le y\le0$），内壁 $x^2+z^2+y^2=1$（$-1\le y\le0$）。水的比重 $\rho g=1000\times10=10^4$。把水分为两层：$-2\le y\le-1$ 的实心层与 $-1\le y\le0$ 的空心层。
**② 外层水做功。** $-2\le y\le-1$ 处截面是半径 $\sqrt{4-y^2}$ 的圆盘，提升距离为 $-y$：
$$W_1=\int_{-2}^{-1}10^4\pi(4-y^2)(-y)\,dy=10^4\pi\left[\frac{y^4}{4}-2y^2\right]_{-2}^{-1}=\frac94\pi\times10^4\text{J}.$$
**③ 内层水做功。** $-1\le y\le0$ 处截面是外圆减内圆的圆环，面积 $\pi[(4-y^2)-(1-y^2)]=3\pi$：
$$W_2=\int_{-1}^{0}10^4\cdot3\pi(-y)\,dy=\frac32\pi\times10^4\text{J}.$$
**④ 求和。** $W=W_1+W_2=\left(\dfrac94+\dfrac32\right)\pi\times10^4=\dfrac{15\pi}{4}\times10^4\text{J}$。
【思路】按高度分层作微元，用 $dW=\rho g\cdot(\text{截面积})dy\cdot(\text{提升距离}-y)$，并对实心段与圆环段分别积分。
【易错】$-1\le y\le0$ 段是圆环而非整圆盘，必须减去内壁截面；内外壁之间「距离相等」只说明两半球同心，不能把壁厚当作竖直厚度。
===Q16===
【答案】$35$
【解】
**① 求 $A^*$ 的特征值。** $A$ 为实对称矩阵，$|A|=1\times2\times3=6$，且 $A^*=|A|A^{-1}$。由 $A\alpha_1=\alpha_1$、$A\alpha_2=2\alpha_2$ 得
$$A^*\alpha_1=\frac{|A|}{1}\alpha_1=6\alpha_1,\qquad A^*\alpha_2=\frac{|A|}{2}\alpha_2=3\alpha_2.$$
**② 计算 $Q^T(A+A^*)Q$。** 于是
$$(A+A^*)Q=(A+A^*)(\alpha_1,\alpha_2)=(7\alpha_1,5\alpha_2).$$
不同特征值的单位特征向量正交，故 $\alpha_1^T\alpha_1=\alpha_2^T\alpha_2=1$、$\alpha_1^T\alpha_2=0$，从而
$$Q^T(A+A^*)Q=\begin{pmatrix}\alpha_1^T\\\alpha_2^T\end{pmatrix}(7\alpha_1,5\alpha_2)=\begin{pmatrix}7&0\\0&5\end{pmatrix}.$$
**③ 取行列式。** 所求为 $7\times5=35$。
【思路】利用 $A^*=|A|A^{-1}$ 与 $A$ 同特征向量、特征值为 $|A|/\lambda$，把 $(A+A^*)\alpha_i$ 写成 $(7\alpha_1,5\alpha_2)$，再借单位正交性化为对角阵。
【易错】$A^*$ 是伴随矩阵而非转置矩阵，其特征值是 $|A|/\lambda$ 即 $6,3,2$，所以 $(A+A^*)\alpha_1=7\alpha_1$、$(A+A^*)\alpha_2=5\alpha_2$；若误当成转置会得到 $2\alpha_1,4\alpha_2$，结果错为 $8$。
===Q17===
【答案】(1) $\dfrac{d^2y}{dt^2}+2\dfrac{dy}{dt}+y=0$；(2) $2$
【解】
**① 用链式法则换元。** $t=\tan x$，故 $\dfrac{dt}{dx}=\sec^2x$，
$$\frac{dy}{dx}=\sec^2x\frac{dy}{dt},\qquad \frac{d^2y}{dx^2}=\frac{d}{dt}\!\left(\sec^2x\frac{dy}{dt}\right)\frac{dt}{dx}=2\sec^2x\tan x\frac{dy}{dt}+\sec^4x\frac{d^2y}{dt^2}.$$
**② 代入原方程。** 利用 $\cos^4x\sec^4x=1$、$\cos^4x\cdot2\sec^2x\tan x=2\sin x\cos x=\sin2x$、$2\cos^2x\sec^2x\left(1-\dfrac12\sin2x\right)=2-\sin2x$，原方程化为
$$\frac{d^2y}{dt^2}+\sin2x\frac{dy}{dt}+(2-\sin2x)\frac{dy}{dt}+y=0,$$
即 $\dfrac{d^2y}{dt^2}+2\dfrac{dy}{dt}+y=0$。
**③ 由切线条件定常数。** 特征方程 $r^2+2r+1=0$ 有重根 $r=-1$，通解 $y=(C_1+C_2t)e^{-t}$。$x=0$ 对应 $t=0$，切线 $y=1$ 给出 $y(0)=1$、$y'(0)=0$，即 $C_1=1$、$-C_1+C_2=0$，故 $C_2=1$，$y(t)=(1+t)e^{-t}$。
**④ 计算广义积分。**
$$\int_0^{+\infty}(1+t)e^{-t}\,dt=\left[-(t+2)e^{-t}\right]_0^{+\infty}=2.$$
【思路】用 $dt/dx=\sec^2x$ 逐阶换导，把变系数方程化为常系数方程；切线条件在 $t=0$ 处给出两个初值，最后用指数衰减的广义积分收尾。
【易错】二阶导换元时必须同时对 $\sec^2x$ 求导，产生 $2\sec^2x\tan x\cdot dy/dt$ 项；切线条件 $y'(0)=0$ 是对 $x$ 的导数，因 $t'(0)=1$，恰好也等于 $dy/dt|_{t=0}$。
===Q18===
【答案】最大值为 $2$，在 $\left(\sqrt{\dfrac35},\,2\sqrt{\dfrac35}\right)$ 处取得；最小值为 $-1$，在 $\left(-2\sqrt{\dfrac35},\,\sqrt{\dfrac35}\right)$ 处取得
【解】
**① 求隐函数的偏导。** 对 $z^3+2z=y(4x+3y)$ 两边分别求偏导：
$$(3z^2+2)z_x=4y,\qquad (3z^2+2)z_y=4x+6y,$$
$$z_x=\frac{4y}{3z^2+2},\qquad z_y=\frac{4x+6y}{3z^2+2}.$$
**② 拉格朗日乘数法。** 约束 $y=\sqrt{3-x^2}$ 即 $x^2+y^2=3,\ y>0$。设 $L=z(x,y)-\lambda(x^2+y^2-3)$，令偏导为零：
$$\frac{4y}{3z^2+2}=2\lambda x,\quad \frac{4x+6y}{3z^2+2}=2\lambda y,\quad x^2+y^2=3.$$
前两式分别乘 $y$、$x$ 并消去 $\lambda$，得 $4y^2=4x^2+6xy$，即 $2x^2+3xy-2y^2=0$，因式分解 $(2x-y)(x+2y)=0$，故 $x=\dfrac y2$ 或 $x=-2y$。
**③ 求候选点及函数值。** 结合 $x^2+y^2=3,\ y>0$ 得
$$P_1=\left(\sqrt{\frac35},\,2\sqrt{\frac35}\right),\qquad P_2=\left(-2\sqrt{\frac35},\,\sqrt{\frac35}\right).$$
在 $P_1$ 处 $z^3+2z=2a(4a+6a)=20a^2=12$（$a=\sqrt{3/5}$），得 $z=2$；在 $P_2$ 处 $z^3+2z=-3$，得 $z=-1$。
**④ 检查端点。** 约束是上半圆弧，端点 $(\pm\sqrt3,0)$ 处 $z^3+2z=0$ 得 $z=0$。比较三个候选值，最大值为 $2$、最小值为 $-1$。
【思路】用隐函数求导得 $z_x,z_y$，再用拉格朗日乘数法把两个一阶条件交叉相乘消去 $\lambda$，最后与端点值比较。
【易错】约束是圆弧而非整圆，必须补查端点 $(\pm\sqrt3,0)$；由 $z^3+2z=c$ 求 $z$ 时注意该三次函数严格递增，根唯一。
===Q19===
【答案】$\dfrac{3\pi}{4}$
【解】
**① 展开并利用对称性。** $(x+y+1)(x+2y-1)=x^2+3xy+2y^2+y-1$。区域 $D$ 满足 $xy\ge0$ 且关于原点中心对称、关于 $y=x$ 对称，故 $\iint_D y\,dxdy=0$、$\iint_D x^2dxdy=\iint_D y^2dxdy$。于是记 $D_1$ 为 $D$ 在第一象限的部分，
$$I=2\iint_{D_1}\left[\frac32(x^2+y^2)+3xy-1\right]dxdy.$$
**② 化为极坐标。** $(x^2+y^2)^2\le4xy$ 在极坐标下为 $r^4\le2r^2\sin2\theta$，即 $0\le r\le\sqrt{2\sin2\theta}$，$\theta\in\left[0,\dfrac\pi2\right]\cup\left[\pi,\dfrac{3\pi}{2}\right]$。在第一象限：
$$I=2\int_0^{\pi/2}d\theta\int_0^{\sqrt{2\sin2\theta}}\left[\frac32r^2(1+\sin2\theta)-1\right]r\,dr.$$
**③ 先积 $r$ 再换元。** 内层积分结果为 $\dfrac32(1+\sin2\theta)\sin^22\theta-\sin2\theta$。令 $u=2\theta$，
$$I=\frac12\int_0^\pi\left(3\sin^2u+3\sin^3u-2\sin u\right)du=3\cdot\frac12\cdot\frac\pi2+3\cdot\frac23-2=\frac{3\pi}{4}.$$
这里用到 $\int_0^\pi\sin^2u\,du=\dfrac\pi2$、$\int_0^\pi\sin^3u\,du=\dfrac43$、$\int_0^\pi\sin u\,du=2$。
【思路】先展开被积函数，利用 $D$ 的对称性和 $x,y$ 可交换性化简，再在极坐标下用 $r^2\le2\sin2\theta$ 定限，最后令 $u=2\theta$ 求三角积分。
【易错】$D$ 只在第一、三象限，不是整个平面；对称消去的是一次项 $y$，不能把 $3xy$ 也消掉；极坐标中 $r$ 的上限是 $\sqrt{2\sin2\theta}$ 而非 $2\sin2\theta$。
===Q20===
【答案】(1) $f(x)$ 在 $(0,+\infty)$ 上可导；(2) $A=\dfrac{2-2\ln2}{4-\pi}$
【解】
**① 证明可导。** 当 $x\ne k$ 时两表达式均可导，只需检查整数点 $x=k$。左侧 $k-1\le x<k$ 时由递推式
$$f(x)=\left(-\frac{\pi}{4}\right)^{k-1}f(x-k+1)=\left(-\frac{\pi}{4}\right)^{k-1}(k-x)\arctan(x-k+1),$$
且 $f(k)=0$。记 $h=x-k<0$，则 $x-k+1=1+h$、$k-x=-h$，故
$$f'_-(k)=\lim_{h\to0^-}\frac{\left(-\frac{\pi}{4}\right)^{k-1}(-h)\arctan(1+h)}{h}=-\left(-\frac{\pi}{4}\right)^{k-1}\arctan1=\left(-\frac\pi4\right)^k.$$
右侧 $k\le x<k+1$ 时 $f(x)=\left(-\dfrac\pi4\right)^k f(x-k)$，取 $h=x-k>0$：
$$f'_+(k)=\lim_{h\to0^+}\frac{\left(-\frac\pi4\right)^k f(h)}{h}=\left(-\frac\pi4\right)^k f'(0)=\left(-\frac\pi4\right)^k,$$
其中 $f(0)=0$、$f'(0)=-\arctan0+1\cdot\dfrac{1}{1+0}=1$。左右导数相等，故在 $(0,+\infty)$ 上处处可导。
**② 把总面积写成各段面积之和。** 在 $[0,1]$ 上 $f(x)=(1-x)\arctan x\ge0$，且 $\int_k^{k+1}f(x)dx=\left(-\dfrac\pi4\right)^k\int_0^1 f(t)dt$，故前 $N+1$ 段面积为等比数列前 $N+1$ 项和，令 $N\to\infty$ 取极限：
$$A=\lim_{N\to\infty}\sum_{k=0}^{N}\left(\frac\pi4\right)^k\int_0^1(1-t)\arctan t\,dt=\frac{4}{4-\pi}\int_0^1(1-t)\arctan t\,dt.$$
**③ 计算基段积分。** 分部积分：
$$\int_0^1\arctan t\,dt=\left[t\arctan t-\frac12\ln(1+t^2)\right]_0^1=\frac\pi4-\frac12\ln2,$$
$$\int_0^1 t\arctan t\,dt=\left[\frac{t^2}{2}\arctan t\right]_0^1-\frac12\int_0^1\frac{t^2}{1+t^2}dt=\frac\pi8-\frac12+\frac\pi8=\frac\pi4-\frac12.$$
相减得 $\int_0^1(1-t)\arctan t\,dt=\dfrac12-\dfrac12\ln2$。
**④ 求和。** $A=\dfrac{4}{4-\pi}\cdot\dfrac{1-\ln2}{2}=\dfrac{2-2\ln2}{4-\pi}$。
【思路】先按整数段写出 $f$ 的分段表达式并用左右导数验证可导性，再把面积化为等比数列前 $N$ 项和取极限乘基段积分，最后分部积分求出基段值。
【易错】递推因子是 $\left(-\dfrac\pi4\right)^k$，求面积时取绝对值得到公比 $\dfrac\pi4<1$；$f'(0)=1$ 要由 $[(1-x)\arctan x]'$ 在 $0$ 处取值确认，不能想当然。
===Q21===
【答案】(1) $\max\limits_{x\in[0,a]}\{f^2(x)\}\le a\int_0^a[f'(t)]^2dt$；(2) $\int_0^a f^2(x)dx\le\dfrac{a^2}{2}\int_0^a[f'(x)]^2dx$，两问均成立
【解】
**① 构造辅助函数。** 由 $f(0)=0$ 知 $f(x)=\int_0^x f'(t)dt$。令
$$F(x)=x\int_0^x[f'(t)]^2dt-f^2(x)=x\int_0^x[g(t)]^2dt-\left(\int_0^x g(t)dt\right)^2,\quad g=f'.$$
**② 求导并配方。** 
$$F'(x)=\int_0^x g^2(t)dt+xg^2(x)-2g(x)\int_0^x g(t)dt=\int_0^x[g(t)-g(x)]^2dt\ge0.$$
又 $F(0)=0$，故 $F(x)\ge0$，即 $f^2(x)\le x\int_0^x[g(t)]^2dt$。
**③ 证明 (1)。** 因 $x\le a$ 且积分区间可扩大，
$$f^2(x)\le x\int_0^x[g(t)]^2dt\le a\int_0^a[f'(t)]^2dt,$$
两边对 $x$ 取最大值即得 (1)。
**④ 证明 (2)。** 对上式在 $[0,a]$ 上积分，并注意 $\int_0^x g^2(t)dt\le\int_0^a g^2(t)dt$，
$$\int_0^a f^2(x)dx\le\int_0^a x\,dx\int_0^a[g(t)]^2dt=\frac{a^2}{2}\int_0^a[f'(x)]^2dx.$$
【思路】构造 $F(x)=x\int_0^x[f']^2-f^2$，求导后配成 $\int_0^x[f'(t)-f'(x)]^2dt\ge0$，得到逐点估计后再积分。
【易错】$F'(x)$ 中 $xg^2(x)$ 与新引入的 $-2g(x)\int_0^x g$ 必须同时保留才能配方；$f'$ 连续保证上述积分与求导合法，题设 $f(0)=0$ 是 $f=\int f'$ 的关键。
===Q22===
【答案】(1) $x=k(1,1,1)^T,\ k\in\mathbb{R}$；(2) $x=Py$，其中 $P=\begin{pmatrix}\frac12+\frac1{\sqrt6}&\frac1{\sqrt6}&-\frac12+\frac1{\sqrt6}\\[3pt]\frac1{\sqrt6}&-\frac2{\sqrt6}&\frac1{\sqrt6}\\[3pt]-\frac12+\frac1{\sqrt6}&\frac1{\sqrt6}&\frac12+\frac1{\sqrt6}\end{pmatrix}$
【解】
**① 确定合同标准矩阵。** $g=\dfrac12y_1^2+y_2^2+\dfrac12y_3^2-y_1y_3$ 的矩阵为
$$B=\begin{pmatrix}\frac12&0&-\frac12\\0&1&0\\-\frac12&0&\frac12\end{pmatrix},\qquad |B-\lambda E|=(1-\lambda)(\lambda^2-\lambda)=-\lambda(\lambda-1)^2,$$
故 $\lambda(B)=1,1,0$。由 $A^2=A$ 知 $\lambda(A)\in\{0,1\}$，又 $A$ 与 $B$ 合同且秩相同，故 $\lambda(A)=1,1,0$。
**② 求 $A$ 的特征向量并正交化。** $\alpha_1+\alpha_2+\alpha_3=0$ 说明 $e_1=(1,1,1)^T$ 满足 $Ae_1=0$，是 $\lambda=0$ 的特征向量。对 $\lambda=1$，特征向量 $(a,b,c)^T$ 满足 $a+b+c=0$，取
$$e_2=(1,0,-1)^T,\qquad e_3=(1,-2,1)^T,$$
二者正交。单位化后取
$$Q=(q_1,q_2,q_3)=\begin{pmatrix}\frac1{\sqrt2}&\frac1{\sqrt6}&\frac1{\sqrt3}\\0&-\frac2{\sqrt6}&\frac1{\sqrt3}\\-\frac1{\sqrt2}&\frac1{\sqrt6}&\frac1{\sqrt3}\end{pmatrix},$$
则 $x=Qz$ 使 $f=x^TAx=z_1^2+z_2^2$。
**③ 第 (1) 问。** $f=0$ 等价于 $z_1=z_2=0$，故 $z=(0,0,k)^T$，
$$x=Qz=k(1,1,1)^T,\qquad k\in\mathbb{R}.$$
**④ 第 (2) 问。** 对 $B$，由 $(B-E)y=0$ 得 $\lambda=1$ 的特征向量 $\gamma_1=(1,0,-1)^T$、$\gamma_2=(0,1,0)^T$；由 $By=0$ 得 $\lambda=0$ 的特征向量 $\gamma_3=(1,0,1)^T$。单位化并取
$$R=\begin{pmatrix}\frac1{\sqrt2}&0&\frac1{\sqrt2}\\0&1&0\\-\frac1{\sqrt2}&0&\frac1{\sqrt2}\end{pmatrix},\qquad y=Rz\ \text{使}\ g=z_1^2+z_2^2.$$
由 $Q^TAQ=R^TBR$，得 $(QR^T)^TA(QR^T)=B$，故 $P=QR^T$ 为正交矩阵，逐元素相乘即得所求矩阵。
【思路】先由二次型矩阵 $B$ 的特征值确定 $A$ 的谱，用 $\alpha_1+\alpha_2+\alpha_3=0$ 找到零特征值向量并单位化得 $Q$，化 $f$ 为 $z_1^2+z_2^2$；再对 $B$ 取相似的单位特征向量矩阵 $R$，用 $P=QR^T$ 拼出所需正交变换。
【易错】$Q$ 来自 $A$，$R$ 来自 $B$，两者对应同一标准形 $z_1^2+z_2^2$，故组合方式是 $P=QR^T$ 而不是 $Q^TR$；$\lambda=1$ 的特征子空间是二维的，$\gamma_1,\gamma_2$ 的选取只要正交单位即可，不唯一。
