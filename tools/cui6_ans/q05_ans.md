===Q1===
【答案】D
【解】
**① 考察 $x=-1$。** $f(x)$ 在 $x=-1,0,1$ 处无定义。当 $x\to-1$ 时分子 $[1-\cos(x-1)]\sin x\to[1-\cos(-2)](-\sin1)\ne0$，分母含一次因子 $x+1$，故
$$\lim_{x\to-1}\frac{[1-\cos(x-1)]\sin x}{x^2(x-1)^2(x+1)}=\lim_{x\to-1}\frac{-[1-\cos2]\sin1}{4(x+1)}=\infty,$$
为无穷间断点，$f$ 在 $(-2,-1)$ 与 $(-1,0)$ 上均无界，A、B 错。
**② 考察 $x=0$。** 此时 $1-\cos(x-1)\to1-\cos1\ne0$，$\sin x\sim x$，故
$$\lim_{x\to0}f(x)=\lim_{x\to0}\frac{1-\cos1}{x}=\infty,$$
也是无穷间断点，$(0,1)$ 上无界，C 错。
**③ 考察 $x=1$。** 由 $1-\cos(x-1)\sim\dfrac{1}{2}(x-1)^2$、$\sin x\to\sin1$、$x^2(x+1)\to2$，
$$\lim_{x\to1}f(x)=\lim_{x\to1}\frac{[1-\cos(x-1)]\sin1}{2(x-1)^2}=\frac{\sin1}{4},$$
是可去间断点，补定义后在 $x=1$ 附近有界，故 $f$ 在 $(1,2)$ 上有界，D 正确。
【思路】逐个检查无定义点 $x=-1,0,1$ 处的极限类型，用 $1-\cos u\sim u^2/2$、$\sin x\sim x$ 判断是否无穷间断。
【易错】$1-\cos(x-1)$ 的等价无穷小是关于 $x-1$ 的；在 $x=-1$ 与 $x=0$ 处它趋于非零常数，误用 $u^2/2$ 会得出错误结论。
===Q2===
【答案】C
【解】
**① 建立相邻项比值不等式。** 由 $x_{n+1}=x_n^2$、$y_{n+1}=1-\cos y_n$ 及严格不等式 $1-\cos u<\dfrac{1}{2}u^2\ (u\ne0)$，得
$$\frac{y_n}{x_n}=\frac{1-\cos y_{n-1}}{x_{n-1}^2}<\frac{1}{2}\left(\frac{y_{n-1}}{x_{n-1}}\right)^2.$$
**② 迭代出指数衰减上界。** 反复使用上式，并利用 $y_1/x_1=1$，归纳得
$$0<\frac{y_n}{x_n}<\frac{1}{2}\cdot\left(\frac{1}{2}\right)^2\cdots\left(\frac{1}{2}\right)^{2^{n-2}}=\left(\frac{1}{2}\right)^{2^{n-1}-1}.$$
**③ 夹逼定阶。** 因 $2^{n-1}-1\to\infty$，右端趋于 $0$，故 $\lim\limits_{n\to\infty}\dfrac{y_n}{x_n}=0$，即 $y_n$ 是 $x_n$ 的高阶无穷小，选 C。
【思路】用 $1-\cos u<u^2/2$ 把 $y_n/x_n$ 与前一项平方比较，迭代得到指数型上界后夹逼。
【易错】$1-\cos u\sim u^2/2$ 只在 $u\to0$ 时成立，本题必须用严格不等式 $1-\cos u<u^2/2$（可由函数 $u^2/2-(1-\cos u)$ 单调递增证明）才能层层递推。
===Q3===
【答案】B
【解】
**① 分解乘积。** 记 $g_1(x)=|\sin x|$，$g_2(x)=x^2-1$，则 $f=g_1g_2$。在 $(-2,2)$ 内 $g_1$ 只在 $x=0$ 不可导，$g_2$ 处处可导且零点为 $x=\pm1$。
**② 判定 $x=\pm1$。** 在这两点 $g_2(a)=0$，直接写差商：
$$\frac{f(x)-f(a)}{x-a}=\frac{(x^2-1)|\sin x|}{x-a}=(x+a)|\sin x|\xrightarrow{x\to a}2a|\sin a|,$$
极限存在，故 $f$ 在 $x=\pm1$ 处可导；$g_2$ 的零点恰好补偿了因子的不可导性。
**③ 判定 $x=0$。** 此时 $g_2(0)=-1\ne0$，而 $|\sin x|$ 在 $0$ 处左、右导数分别为 $-1$、$1$，不可导，乘积 $f$ 在 $0$ 处也不可导。故只有一个不可导点，选 B。
【思路】用差商直接验证：因子 $x^2-1$ 在 $\pm1$ 为零使乘积恢复可导，而在 $x=0$ 处 $|\sin x|$ 的不可导性被保留。
【易错】在 $(-2,2)$ 内 $|\sin x|$ 的不可导点只有 $x=0$（$\pm\pi$ 不在区间内）；不能因为 $x^2-1$ 有零点就误判 $f$ 在 $\pm1$ 不可导。
===Q4===
【答案】C
【解】
**① 判断 $f$ 的奇偶性。** 记 $h(t)=t(1+\cos t)$，显见 $h$ 为奇函数。由换元 $t=-s$，
$$f(-x)=\int_0^{-\sin x}h(t)dt=\int_0^{\sin x}h(-s)(-ds)=\int_0^{\sin x}h(s)ds=f(x),$$
故 $f$ 为偶函数，A 错。
**② 判断 $g$ 的奇偶性。** $g(x)=\int_0^x f(t)dt$ 且 $f$ 为偶函数，则 $g(-x)=\int_0^{-x}f(t)dt=-\int_0^xf(-s)ds=-g(x)$，故 $g$ 为奇函数，D 错。
**③ 判拐点。** 由微积分基本定理与链式法则，
$$g''(x)=f'(x)=h(\sin x)\cos x=\sin x\,[1+\cos(\sin x)]\cos x.$$
在 $x=0$ 的充分小邻域内 $1+\cos(\sin x)>0$、$\cos x>0$，故 $g''(x)$ 与 $x$ 同号：$x<0$ 时为负、$x>0$ 时为正，凹凸性改变，$(0,0)$ 是曲线 $y=g(x)$ 的拐点，选 C。
【思路】先由被积函数与上限的奇偶性得出 $f$ 偶、$g$ 奇，再求 $g''=f'$ 考察其在 $0$ 两侧的符号变化。
【易错】变上限积分 $\int_0^{\varphi(x)}h(t)dt$ 的奇偶性由 $\varphi$ 与 $h$ 共同决定：本题 $\varphi=\sin x$ 为奇、$h$ 为奇，结果才是偶函数；不要把「奇函数的变上限积分必为偶函数」当通用结论。
===Q5===
【答案】A
【解】
**① 转化为特征根条件。** 特征方程为 $r^2+ar+b=0$。微分方程的任意解都趋于 $0$，等价于全部特征根的实部均严格小于 $0$（含重根情形）。
**② 实根情形。** 若 $a^2-4b\ge0$，两根均为实数且均负，由韦达定理需两根之和 $-a<0$、之积 $b>0$，即 $a>0,\ b>0$。
**③ 复根情形。** 若 $a^2-4b<0$，共轭复根为 $-\dfrac a2\pm i\beta$，实部 $-\dfrac a2<0$ 要求 $a>0$；此时判别式条件给出 $b>\dfrac{a^2}{4}>0$。两种情形合并，充要条件为 $a>0,\ b>0$，选 A。
【思路】把「任意解趋于零」翻译为特征根实部全负，再分实根（韦达定理）与共轭复根（实部表达式）两种情形讨论。
【易错】复根情形不能只写 $a>0$ 就结束，还须由判别式小于零得到 $b>a^2/4$，合并后才得到 $a>0,\ b>0$。
===Q6===
【答案】D
【解】
**① 还原二重积分。** 当 $0\le x\le\pi$ 时 $\sin\dfrac{x}{2}\ge-\sin x$，故原累次积分的上下限是颠倒的，原式等于 $-\iint\limits_D f(x,y)dxdy$，其中
$$D=\left\{(x,y)\,\middle|\,0\le x\le\pi,\ -\sin x\le y\le\sin\frac{x}{2}\right\}.$$
**② 固定 $y\in[-1,0]$。** 下边界曲线 $y=-\sin x$ 在 $[0,\frac{\pi}{2}]$ 上给 $x=-\arcsin y$，在 $[\frac{\pi}{2},\pi]$ 上给 $x=\pi+\arcsin y$（注意 $y<0$ 时 $\arcsin y<0$），故 $x$ 从 $-\arcsin y$ 到 $\pi+\arcsin y$。
**③ 固定 $y\in[0,1]$。** 上边界 $y=\sin\dfrac{x}{2}$ 给 $x=2\arcsin y$，区域内 $x$ 从 $2\arcsin y$ 到 $\pi$。
**④ 写出结果。** 加上颠倒限带来的负号：
$$I=-\int_{-1}^{0}dy\int_{-\arcsin y}^{\pi+\arcsin y}f(x,y)\,dx-\int_0^1dy\int_{2\arcsin y}^{\pi}f(x,y)\,dx,$$
选 D。
【思路】先把上下限颠倒的累次积分还原为带负号的二重积分，画出 $y=\sin\frac{x}{2}$ 与 $y=-\sin x$ 围成的区域，再按 $y$ 分两段反解 $x$。
【易错】原式上限 $-\sin x$ 小于下限 $\sin\frac{x}{2}$，必须先提出负号；$y<0$ 时 $\arcsin y<0$，右边界是 $\pi+\arcsin y$ 而不是 $\pi-\arcsin y$。
===Q7===
【答案】C
【解】
**① 命题①错误。** 取 $f(x)=e^{-x}$，$g(x)=-1$，在 $[0,+\infty)$ 上 $f(x)>g(x)$，且 $\int_0^{+\infty}e^{-x}dx=1$ 收敛，但 $\int_0^{+\infty}(-1)dx$ 发散。大小关系不能直接决定反常积分的敛散性。
**② 命题②正确。** 由 $(f+g)^2\le2(f^2+g^2)$，
$$\int_0^{+\infty}[f(x)+g(x)]^2dx\le2\int_0^{+\infty}f^2(x)dx+2\int_0^{+\infty}g^2(x)dx<+\infty,$$
由比较判别法知该积分收敛。
**③ 命题③错误。** 取 $f(x)=\dfrac{1}{\sqrt{x+2}\ln(x+2)}$，在 $[0,+\infty)$ 上非负连续，且
$$\int_0^{+\infty}f^2(x)dx=\int_0^{+\infty}\frac{dx}{(x+2)\ln^2(x+2)}$$
收敛；但当 $x\to+\infty$ 时 $\dfrac{f(x)}{\sqrt{1+x}}\sim\dfrac{1}{x\ln x}$，而 $\displaystyle\int^{+\infty}\frac{dx}{x\ln x}$ 发散。故只有命题②正确，共 1 个，选 C。
【思路】①②用比较判别法与不等式放缩，③用反例 $f(x)=1/(\sqrt{x+2}\ln(x+2))$ 否定，关键是 $\int dx/(x\ln x)$ 发散。
【易错】$\int^{+\infty}\dfrac{dx}{x\ln x}$ 发散而 $\int^{+\infty}\dfrac{dx}{x\ln^2x}$ 收敛，只差一个对数幂次；构造反例时还要注意 $f\ge0$ 且连续。
===Q8===
【答案】D
【解】
**① 把等价转化为秩相等。** 向量组等价的充要条件是 $r(\beta_1,\beta_2,\beta_3)=r(\alpha_1,\alpha_2,\alpha_3)=r(\beta_1,\beta_2,\beta_3,\alpha_1,\alpha_2,\alpha_3)$。对增广矩阵作初等行变换：
$$\begin{pmatrix}1&3&3&0&1&2\\2&0&2&1&3&n\\-3&-3&-5&-1&m&1\end{pmatrix}\to\begin{pmatrix}1&3&3&0&1&2\\0&-6&-4&1&1&n-4\\0&6&4&-1&m+3&7\end{pmatrix}\to\begin{pmatrix}1&3&3&0&1&2\\0&-6&-4&1&1&n-4\\0&0&0&0&m+4&n+3\end{pmatrix}.$$
**② 定出 $m,n$。** 要使后三组向量不增加秩，最后一行必须为零，即 $m+4=0$、$n+3=0$，故 $m=-4$，$n=-3$。此时前两行线性无关，两个向量组的秩均为 2，确等价，选 D。
【思路】把向量组等价写成合并矩阵秩不变，行变换后最后一行给出 $m+4=0$、$n+3=0$。
【易错】等价要求两个向量组互相能线性表示，只检查 $r(\alpha)=r(\beta)$ 不够，必须检验合并矩阵不增秩；题中 $\alpha_2=(1,3,m)^T$ 的 $m$ 出现在第三行第五列，不要与 $\beta$ 的分量混淆。
===Q9===
【答案】A
【解】
**① 由 $AA^T\beta=0$ 推出 $A^T\beta=0$。** 两边左乘 $\beta^T$：
$$\beta^TAA^T\beta=(A^T\beta)^T(A^T\beta)=\|A^T\beta\|^2=0,$$
因 $A^T\beta$ 为实向量，故 $A^T\beta=0$。
**② 反证 $AX=\beta$ 无解。** 若存在 $X_0$ 使 $AX_0=\beta$，两边左乘 $\beta^T$ 得
$$\beta^T\beta=\beta^TAX_0=(A^T\beta)^TX_0=0,$$
于是 $\beta=0$，与 $\beta$ 为非零列向量矛盾。故 $AX=\beta$ 必无解。
**③ 排除其余选项。** $A^TAX=A^T\beta=0$ 恒有零解；其解唯一还是无穷多取决于 $r(A^TA)=r(A)$ 是否等于 $n$，题设未给定 $r(A)$ 与 $n$ 的关系，故 C、D 都不必然成立。选 A。
【思路】把 $AA^T\beta=0$ 左乘 $\beta^T$ 得到 $A^T\beta=0$，再用 $\beta^TAX_0=0$ 与 $\beta\ne0$ 矛盾证明方程组无解。
【易错】由 $AA^T\beta=0$ 到 $A^T\beta=0$ 必须借助 $\beta^TAA^T\beta=\|A^T\beta\|^2$ 的正定性，不能两边直接「约去」$A$；$A^TAX=0$ 解唯一需要 $r(A)=n$，题中没有这个条件。
===Q10===
【答案】B
【解】
**① 写成两个线性形式之积。** 因 $\alpha\beta^T$ 是秩一矩阵，
$$f=X^T(\alpha\beta^T)X=(\alpha^TX)(\beta^TX).$$
令 $y_1=\alpha^TX$，$y_2=\beta^TX$，$y_3=x_3$。由 $\alpha,\beta$ 线性无关知此变换可逆。
**② 求标准形对应矩阵的特征值。** 在新变量下 $f=y_1y_2$，其对称矩阵为
$$\begin{pmatrix}0&\frac{1}{2}&0\\\frac{1}{2}&0&0\\0&0&0\end{pmatrix},$$
特征值为 $\dfrac{1}{2},-\dfrac{1}{2},0$。
**③ 读出惯性指数。** 正特征值、负特征值各 1 个，故正、负惯性指数分别为 $1,1$，选 B。
【思路】把 $X^T(\alpha\beta^T)X$ 化为 $(\alpha^TX)(\beta^TX)$，取对应对称阵求特征值定惯性指数。
【易错】$\alpha\beta^T$ 非对称，不能直接拿它求惯性指数；二次型对应的对称阵是 $\dfrac{\alpha\beta^T+\beta\alpha^T}{2}$，其特征值为 $\pm\dfrac{1}{2},0$。
===Q11===
【答案】$\dfrac{1}{3}$
【解】
**① 两边作泰勒展开。** 由 $e^{x^2}=1+x^2+o(x^2)$，
$$f(\xi)=e^{\xi^2}=1+\xi^2+o(\xi^2),\qquad \frac{\tan x}{x}=\frac{x+\frac{1}{3}x^3+o(x^3)}{x}=1+\frac{1}{3}x^2+o(x^2).$$
**② 取对数比较系数。** 由 $e^{\xi^2}=\dfrac{\tan x}{x}$ 得 $\xi^2=\ln\left(1+\dfrac{1}{3}x^2+o(x^2)\right)=\dfrac{1}{3}x^2+o(x^2)$。
**③ 求极限。** $\lim\limits_{x\to0}\dfrac{\xi^2}{x^2}=\dfrac{1}{3}$。
【思路】对等式两边作二阶展开，或取对数后用 $\ln(1+u)\sim u$，比较 $x^2$ 的系数得到 $\xi^2\sim\frac{1}{3}x^2$。
【易错】$\xi$ 依赖于 $x$ 且随 $x\to0$ 而趋于 $0$，须先取对数把指数拉下来；若误把 $\xi$ 当作与 $x$ 同阶的独立变量直接代入会得到错误系数。
===Q12===
【答案】$-\dfrac{e}{2}$
【解】
**① 确定 $x=0$ 对应的 $t,y$。** 由 $x=\int_1^t e^{-u^2}du$ 知 $x=0$ 时 $t=1$；代入 $te^y+y-1=0$ 得 $e^y+y-1=0$。左端关于 $y$ 严格递增且 $y=0$ 满足，故 $y(0)=0$。
**② 对参变量 $t$ 求导。** $\dfrac{dx}{dt}=e^{-t^2}$；对 $te^y+y-1=0$ 求导得
$$e^y+(te^y+1)\frac{dy}{dt}=0,\qquad \frac{dy}{dx}=\frac{dy/dt}{dx/dt}=-\frac{e^{t^2+y}}{te^y+1}.$$
**③ 代入。** 取 $t=1,\ y=0$，得 $y'(0)=-\dfrac{e^{1+0}}{1\cdot1+1}=-\dfrac e2$。
【思路】把 $x,y$ 都看作 $t$ 的函数，分别求导后用参数方程求导公式 $\frac{dy}{dx}=\frac{dy/dt}{dx/dt}$，在 $x=0$ 对应 $t=1,y=0$ 处代入。
【易错】$\frac{dx}{dt}=e^{-t^2}$ 而非 $e^{t^2}$，做商后指数变为 $e^{t^2+y}$；不要忘记先由 $x=0$ 定出 $t=1$ 再由隐式方程定出 $y=0$。
===Q13===
【答案】$1$
【解】
**① 拆成两项。** 
$$\sum_{i=1}^{2n}\frac{1+i}{n^2}\sin^2\frac{(i-1)\pi}{n}=\sum_{i=1}^{2n}\frac{1}{n^2}\sin^2\frac{(i-1)\pi}{n}+\sum_{i=1}^{2n}\frac{i}{n^2}\sin^2\frac{(i-1)\pi}{n}.$$
第一项绝对值不超过 $\dfrac{2n}{n^2}\to0$。
**② 第二项凑黎曼和。** 取 $x_i=\dfrac in$，步长 $\dfrac{1}{n}$，$i=1,\dots,2n$ 对应区间 $(0,2]$：
$$\sum_{i=1}^{2n}\frac{i}{n^2}\sin^2\frac{(i-1)\pi}{n}=\frac{1}{n}\sum_{i=1}^{2n}\frac in\sin^2\left(\pi\cdot\frac{i-1}{n}\right)\longrightarrow\int_0^2 x\sin^2(\pi x)\,dx.$$
**③ 计算定积分。** 令 $u=\pi x$，则
$$\int_0^2x\sin^2(\pi x)dx=\frac1{\pi^2}\int_0^{2\pi}u\sin^2u\,du=\frac1{\pi^2}\cdot\pi^2=1.$$
【思路】把求和拆为可忽略的 $1/n^2$ 项与黎曼和，积分区间是 $[0,2]$，再换元 $u=\pi x$ 求值。
【易错】上限是 $2n$ 而非 $n$，积分区间是 $[0,2]$；第一项虽趋于 0 但仍须单独说明，不能直接丢弃。
===Q14===
【答案】$\dfrac{GM}{a}\ln2$
【解】
**① 求细杆对质点的引力。** 设质点 $C$ 到细杆近端的距离为 $x$，线密度 $\rho=\dfrac Ma$。取杆上距近端 $t$ 的微元 $dm=\dfrac Ma\,dt$，由万有引力定律
$$F(x)=\int_0^a\frac{G\cdot1\cdot dm}{(x+t)^2}=\frac{GM}{a}\int_0^a\frac{dt}{(x+t)^2}=\frac{GM}{a}\left(\frac{1}{x}-\frac1{x+a}\right)=\frac{GM}{x(x+a)}.$$
**② 计算引力做功。** 质点从无穷远沿延长线移到距近端 $a$ 处，位移与引力同向：
$$W=\int_a^{+\infty}F(x)dx=\frac{GM}{a}\int_a^{+\infty}\left(\frac{1}{x}-\frac1{x+a}\right)dx=\frac{GM}{a}\left[\ln\frac{x}{x+a}\right]_a^{+\infty}=\frac{GM}{a}\ln2.$$
【思路】先积分求均匀细杆对延长线上单位质点的引力 $F(x)=GM/[x(x+a)]$，再对位移从 $a$ 到 $+\infty$ 积分得功。
【易错】积分下限是终点到近端的距离 $a$；$\ln\dfrac{x}{x+a}$ 在无穷远处趋于 $0$、在 $x=a$ 处为 $\ln\dfrac{1}{2}$，相减得 $\ln2$，符号不能弄反。
===Q15===
【答案】$7$
【解】
**① 提取一阶偏导。** 由 $\lim\limits_{\substack{x\to0\\y\to0}}\dfrac{f(x,y)-2x+y}{x^2+y^2}=1$ 知 $f(x,y)=2x-y+O(x^2+y^2)$，从而
$$f(0,0)=0,\qquad f_x(0,0)=2,\qquad f_y(0,0)=-1.$$
**② 拆分所求极限。**
$$\lim_{t\to0}\frac{f(2t,0)-f(0,\sin t)+2f(t,t)}{t}=2\lim_{t\to0}\frac{f(2t,0)-f(0,0)}{2t}-\lim_{t\to0}\frac{f(0,\sin t)-f(0,0)}{\sin t}\cdot\frac{\sin t}{t}+2\lim_{t\to0}\frac{f(t,t)-f(0,0)}{t}.$$
第一项为 $2f_x(0,0)=4$；第二项为 $-f_y(0,0)=1$；第三项中 $f(t,t)-f(0,0)=(f_x+f_y)t+o(t)=t+o(t)$，故为 $2$。
**③ 求和。** 原极限为 $4+1+2=7$。
【思路】由一阶展开 $f(x,y)=2x-y+O(x^2+y^2)$ 把三个差商化为两个偏导数的线性组合，代入 $f_x(0,0)=2$、$f_y(0,0)=-1$，注意沿路径 $x=y=t$ 的差商极限是 $f_x+f_y$。
【易错】$f(0,\sin t)$ 需乘上 $\frac{\sin t}{t}\to1$ 才能凑成对 $y$ 的差商；沿路径 $(t,t)$ 的差商极限是 $f_x+f_y$，不能只写 $f_x$。
===Q16===
【答案】$3$
【解】
**① 由不可逆得 $a=b$。** 
$$A-aE=\begin{pmatrix}1&b&1\\1&0&-1\\2&a&0\end{pmatrix},\qquad |A-aE|=1\cdot a-b(0+2)+1\cdot a=2(a-b)=0,$$
故 $a=b$；结合 $b>0$ 知 $a>0$。
**② 计算第三行代数余子式。**
$$A_{31}=(-1)^{3+1}\begin{vmatrix}b&1\\a&-1\end{vmatrix}=-a-b,\qquad A_{32}=(-1)^{3+2}\begin{vmatrix}a+1&1\\1&-1\end{vmatrix}=a+2,$$
$$A_{33}=(-1)^{3+3}\begin{vmatrix}a+1&b\\1&a\end{vmatrix}=a^2+a-b.$$
**③ 代入条件。** $A_{31}+A_{32}+A_{33}=a^2+a+2-2b=8$，代入 $a=b$ 得 $a^2-a-6=0$，解得 $a=3$ 或 $a=-2$；由 $a>0$ 取 $a=3$。
【思路】由 $|A-aE|=0$ 得 $a=b$，再逐项计算第三行的代数余子式并代入和式解二次方程。
【易错】$A_{31}$ 的余子式是删去第 3 行第 1 列后剩下的 $\begin{pmatrix}b&1\\a&-1\end{pmatrix}$，其中右下角元素是 $A$ 的 $(2,2)$ 元 $a$；符号 $(-1)^{i+j}$ 须逐项确认。
===Q17===
【答案】$\dfrac{\pi}{4}+\dfrac{1}{4}+\dfrac{1}{4}\ln\dfrac{5}{2}-\arctan 2$
【解】
**① 化为极坐标。** 令 $x=r\cos\theta,\ y=r\sin\theta$。条件 $1\le x^2+y^2\le2x$ 与 $y\ge0$ 给出 $0\le\theta\le\dfrac{\pi}{3}$、$1\le r\le2\cos\theta$，故
$$I=\int_0^{\pi/3}d\theta\int_1^{2\cos\theta}\frac{r\sin\theta}{1+r^2}\,r\,dr=\int_0^{\pi/3}d\theta\int_1^{2\cos\theta}\left(1-\frac1{1+r^2}\right)\sin\theta\,dr.$$
**② 先对 $r$ 积分。** 内层原函数为 $r-\arctan r$，于是
$$I=\int_0^{\pi/3}\left[2\sin\theta\cos\theta-\arctan(2\cos\theta)\sin\theta-\sin\theta+\frac{\pi}{4}\sin\theta\right]d\theta.$$
**③ 计算可直接积分的部分。**
$$\int_0^{\pi/3}\left[2\sin\theta\cos\theta+\left(\frac{\pi}{4}-1\right)\sin\theta\right]d\theta=\left[-\frac{1}{2}\cos2\theta-\left(\frac{\pi}{4}-1\right)\cos\theta\right]_0^{\pi/3}=\frac{\pi}{8}+\frac{1}{4}.$$
**④ 处理反正切项。** 令 $t=2\cos\theta$，
$$\int_0^{\pi/3}\arctan(2\cos\theta)\,d\cos\theta=\frac{1}{2}\int_1^2\arctan t\,dt=\frac{1}{2}\left[t\arctan t-\frac{1}{2}\ln(1+t^2)\right]_1^2=\frac{\pi}{8}-\arctan2+\frac{1}{4}\ln\frac{5}{2}.$$
合并得 $I=\dfrac{\pi}{8}+\dfrac{1}{4}+\dfrac{\pi}{8}-\arctan2+\dfrac{1}{4}\ln\dfrac{5}{2}=\dfrac{\pi}{4}+\dfrac{1}{4}+\dfrac{1}{4}\ln\dfrac{5}{2}-\arctan2$。
【思路】用极坐标把区域化为 $0\le\theta\le\frac{\pi}{3}$、$1\le r\le2\cos\theta$，对 $r$ 积出 $r-\arctan r$，再对 $\theta$ 作换元 $t=2\cos\theta$ 处理反正切积分。
【易错】$\int\arctan t\,dt=t\arctan t-\frac{1}{2}\ln(1+t^2)$；代入上下限后出现 $\arctan1=\frac{\pi}{4}$ 与 $\ln\frac{5}{2}$，符号容易弄反；极坐标中角度上限是 $\frac{\pi}{3}$（由 $2\cos\theta\ge1$ 定出）。
===Q18===
【答案】(1) $f(x,y)=e^{-x}(y-1)^2+\sin x$；(2) $V=\dfrac{\pi}{2}\left(e^{2\pi}+e^{\pi}\right)$
【解】
**(1) 求 $f(x,y)$。**
**① 先对 $x$ 积分。** 由二阶偏导连续有 $f''_{xy}=f''_{yx}=2e^{-x}(1-y)$，对 $x$ 积分：
$$f'_y(x,y)=\int 2e^{-x}(1-y)\,dx=2e^{-x}(y-1)+C_1(y).$$
由 $f'_y(0,y)=2(y-1)$ 得 $C_1(y)=0$。
**② 再对 $y$ 积分。** $f(x,y)=\int 2e^{-x}(y-1)dy=e^{-x}(y-1)^2+C_2(x)$，由 $f(x,1)=\sin x$ 得 $C_2(x)=\sin x$，故 $f(x,y)=e^{-x}(y-1)^2+\sin x$。
**(2) 求旋转体体积。**
**① 确定曲线范围。** $f(x,y)=0$ 即 $(y-1)^2=-e^x\sin x$。由 $0\le x\le2\pi$ 且右端非负知 $\pi\le x\le2\pi$。
**② 列圆盘法积分。** 绕直线 $y=1$ 旋转，半径为 $|y-1|$，故
$$V=\pi\int_\pi^{2\pi}(y-1)^2dx=\pi\int_\pi^{2\pi}\left(-e^x\sin x\right)dx.$$
**③ 分部积分求值。** 由 $\int e^x\sin x\,dx=\dfrac{e^x(\sin x-\cos x)}2$，
$$\int_\pi^{2\pi}\left(-e^x\sin x\right)dx=\left[\frac{e^x(\cos x-\sin x)}2\right]_\pi^{2\pi}=\frac{e^{2\pi}+e^\pi}{2},$$
故 $V=\dfrac{\pi}{2}\left(e^{2\pi}+e^\pi\right)$。
【思路】由混合偏导连续依次对 $x$、对 $y$ 积分并用两个边值定出积分常数；再把曲线写成 $(y-1)^2=-e^x\sin x$，用圆盘法求绕 $y=1$ 的体积。
【易错】先对 $x$ 积分时出现的「常数」是 $y$ 的函数，必须由 $f'_y(0,y)$ 确定；旋转体面积是 $\pi(y-1)^2$，其中半径的平方已消去绝对值，但不能漏乘 $\pi$。
===Q19===
【答案】在 $(1,1)$ 处取得极大值 $e$；$(0,0)$ 不是极值点
【解】
**① 隐函数求一阶偏导。** 令 $F=2x^3-6xy+3y^2+\dfrac{1}{e} z\ln z=0$，则 $F_x=6x^2-6y$，$F_y=-6x+6y$，$F_z=\dfrac{1}{e}(\ln z+1)$。由隐函数求导，
$$6x^2-6y+\frac{1}{e}(\ln z+1)z'_x=0,\qquad -6x+6y+\frac{1}{e}(\ln z+1)z'_y=0.$$
令 $z'_x=z'_y=0$ 得 $y=x^2$ 与 $y=x$，故驻点为 $(0,0)$、$(1,1)$；代入原方程得 $z(0,0)=1$、$z(1,1)=e$。
**② 求二阶偏导方程。** 对上面两式再求偏导，在驻点处 $z'_x=z'_y=0$，得
$$12x+\frac{1}{e}(\ln z+1)z''_{xx}=0,\qquad 6+\frac{1}{e}(\ln z+1)z''_{yy}=0,\qquad -6+\frac{1}{e}(\ln z+1)z''_{xy}=0.$$
**③ 判别 $(0,0)$。** 此时 $z=1$，$\ln z+1=1$，$x=0$，故 $A=z''_{xx}=0$，$B=z''_{xy}=6e$，$C=z''_{yy}=-6e$。因 $AC-B^2=-36e^2<0$，该点不是极值点。
**④ 判别 $(1,1)$。** 此时 $z=e$，$\ln z+1=2$，$x=1$，故 $A=-6e$，$B=3e$，$C=-3e$。因 $AC-B^2=9e^2>0$ 且 $A<0$，函数在 $(1,1)$ 处取极大值 $z(1,1)=e$。
【思路】隐函数求一阶偏导定驻点，再对一阶关系求导得到二阶偏导满足的方程，用 $AC-B^2$ 判别两个驻点。
【易错】驻点处虽 $z'_x=z'_y=0$，但 $\dfrac{1}{e}(\ln z+1)$ 随点变化：$(0,0)$ 处为 $1$、$(1,1)$ 处为 $2$，代入时不能用同一个系数；$z''_{yy}$ 方程中的常数是 $+6$，故 $C$ 为负。
===Q20===
【答案】$y=\dfrac{(\sqrt2+1)e^x+(\sqrt2-1)e^{-x}}{2}$
【解】
**① 由法线写出线段 $PQ$ 的长度。** 设 $P(x_0,y_0)$，$y_0>0$，法线方程为 $y-y_0=-\dfrac1{y'(x_0)}(x-x_0)$。令 $y=0$ 得 $Q\big(x_0+y_0y'(x_0),\,0\big)$，故
$$|PQ|=\sqrt{[y_0y'(x_0)]^2+y_0^2}=y_0\sqrt{1+[y'(x_0)]^2}.$$
**② 用曲率半径列微分方程。** 曲率半径 $R=\dfrac{\{1+[y'(x_0)]^2\}^{\frac{3}{2}}}{y''(x_0)}$。由 $R=|PQ|$ 得 $yy''=1+(y')^2$。
**③ 降阶求解。** 令 $p=y'$，$y''=p\dfrac{dp}{dy}$，则 $\dfrac{p\,dp}{1+p^2}=\dfrac{dy}{y}$，积分得
$$\frac{1}{2}\ln(1+p^2)=\ln y+C_1.$$
由 $y(0)=\sqrt2$、$p(0)=1$ 得 $C_1=0$，故 $1+p^2=y^2$，取正根 $p=\sqrt{y^2-1}$（因 $y'(0)=1>0$）。
**④ 再积分一次。** $\displaystyle\int\frac{dy}{\sqrt{y^2-1}}=\int dx$ 给出 $\ln\left(y+\sqrt{y^2-1}\right)=x+C_2$，由 $y(0)=\sqrt2$ 得 $C_2=\ln(\sqrt2+1)$，即
$$y+\sqrt{y^2-1}=(\sqrt2+1)e^x,\qquad y-\sqrt{y^2-1}=(\sqrt2-1)e^{-x}.$$
两式相加得 $y=\dfrac{(\sqrt2+1)e^x+(\sqrt2-1)e^{-x}}{2}$。
【思路】由法线与 $x$ 轴交点写出 $|PQ|$，与曲率半径相等得到 $yy''=1+(y')^2$，用 $p=y'$ 降阶两次积分，最后利用倒数关系解出 $y$。
【易错】曲率半径公式中分母是 $y''$ 而非 $|y''|$（本题凹函数 $y''>0$），法线斜率是 $-\frac1{y'}$；降阶后取 $p=\sqrt{y^2-1}$ 的正根要由 $y'(0)=1$ 确定。
===Q21===
【答案】(1) $f'(x)\ge2x(1-x)$；(2) $\dfrac{1}{3}\le\int_0^1f(x)dx\le\dfrac{2}{3}$，两问均成立
【解】
**(1) 证明 $f'(x)\ge2x(1-x)$。**
**① 在任意点 $x_0\in(0,1)$ 作泰勒展开。** 分别在 $x_0$ 处展开到 $x=0$ 与 $x=1$：
$$f(0)=f(x_0)-x_0f'(x_0)+\frac{x_0^2}{2}f''(\xi_1)=0,\quad \xi_1\in(0,x_0),$$
$$f(1)=f(x_0)+(1-x_0)f'(x_0)+\frac{(1-x_0)^2}{2}f''(\xi_2)=1,\quad \xi_2\in(x_0,1).$$
**② 相减并用 $|f''|\le2$。** 第二式减第一式得
$$f'(x_0)=1+\frac{x_0^2}{2}f''(\xi_1)-\frac{(1-x_0)^2}{2}f''(\xi_2)\ge1-x_0^2-(1-x_0)^2=2x_0(1-x_0).$$
由 $x_0$ 任意，结论成立。
**(2) 证明积分不等式。**
**① 消去 $f'(x_0)$。** 将第一式乘 $(1-x_0)$、第二式乘 $x_0$ 后相加：
$$x_0=f(x_0)+\frac{x_0^2(1-x_0)}{2}f''(\xi_1)+\frac{x_0(1-x_0)^2}{2}f''(\xi_2).$$
**② 估计 $f(x_0)$。** 由 $|f''|\le2$ 得 $|f(x_0)-x_0|\le x_0^2(1-x_0)+x_0(1-x_0)^2=x_0(1-x_0)$，故
$$x_0^2\le f(x_0)\le2x_0-x_0^2.$$
**③ 积分。** 在 $[0,1]$ 上积分得 $\dfrac{1}{3}\le\int_0^1f(x)dx\le\dfrac{2}{3}$。
【思路】在任意内点作泰勒展开到两个端点，相减消去 $f(x_0)$ 得导数下界；按权重 $(1-x_0)$、$x_0$ 相加消去 $f'(x_0)$，得 $f$ 的夹逼后积分。
【易错】两个泰勒余项中的 $\xi_1,\xi_2$ 一般不同，不能合并；消去 $f'(x_0)$ 的权重是 $(1-x_0)$ 与 $x_0$，不是随便取的数。
===Q22===
【答案】(1) $a=2,\ b=2$；(2) $P=\begin{pmatrix}2&5&4\\1&3&3\\0&0&1\end{pmatrix}$；(3) 解法一：$Q_1=\begin{pmatrix}2&4&6\\1&2&3\\0&0&0\end{pmatrix},\ Q_2=\begin{pmatrix}3&-5&3\\-1&2&-2\\0&0&1\end{pmatrix}$；解法二：$Q_1=\begin{pmatrix}2&5&4\\1&3&3\\0&0&1\end{pmatrix},\ Q_2=\begin{pmatrix}1&-1&2\\0&0&0\\0&0&0\end{pmatrix}$
【解】
**(1) 求 $a,b$。**
**① 用相似不变量。** 由 $A\sim B$ 得 $\operatorname{tr}(A)=\operatorname{tr}(B)$：$a-1=1$，故 $a=2$。
**② 用秩条件定 $b$。** $B$ 的特征值为 $1,0,0$，且 $3-r(B)=2$ 说明 $B$ 可对角化，故 $A$ 也可对角化，从而 $r(A-0\cdot E)=1$。此时
$$A=\begin{pmatrix}2&-2&4\\1&-1&b\\0&0&0\end{pmatrix},\qquad r(A)=1$$
要求各行成比例，故 $b=2$。
**(2) 求可逆矩阵 $P$。**
**① 求两组特征向量。** 对特征值 $1$，由 $(A-E)x=0$ 得 $\alpha_1=(2,1,0)^T$；对特征值 $0$，得 $\alpha_2=(1,1,0)^T$、$\alpha_3=(-2,0,1)^T$。对 $B$，特征值 $1$ 的向量 $\beta_1=(1,0,0)^T$，特征值 $0$ 的向量 $\beta_2=(-2,1,0)^T$、$\beta_3=(-3,0,1)^T$。
**② 拼成变换矩阵。** 令 $P_1=(\alpha_1,\alpha_2,\alpha_3)$、$P_2=(\beta_1,\beta_2,\beta_3)$，则 $P_1^{-1}AP_1=P_2^{-1}BP_2=\operatorname{diag}(1,0,0)$，故 $P=P_1P_2^{-1}$：
$$P=\begin{pmatrix}2&1&-2\\1&1&0\\0&0&1\end{pmatrix}\begin{pmatrix}1&-2&-3\\0&1&0\\0&0&1\end{pmatrix}=\begin{pmatrix}2&5&4\\1&3&3\\0&0&1\end{pmatrix}.$$
**(3) 求 $Q_1,Q_2$。**
**① 解法一。** 由 $P^{-1}AP=B$ 得 $A=PBP^{-1}$。取 $Q_1=PB$、$Q_2=P^{-1}$，则 $Q_1Q_2=PBP^{-1}=A$、$Q_2Q_1=P^{-1}PB=B$：
$$Q_1=\begin{pmatrix}2&4&6\\1&2&3\\0&0&0\end{pmatrix},\qquad Q_2=\begin{pmatrix}3&-5&3\\-1&2&-2\\0&0&1\end{pmatrix}.$$
**② 解法二。** 直接取 $Q_1=P$、$Q_2=P^{-1}A$，同样有 $Q_1Q_2=A$、$Q_2Q_1=P^{-1}AP=B$：
$$Q_1=\begin{pmatrix}2&5&4\\1&3&3\\0&0&1\end{pmatrix},\qquad Q_2=\begin{pmatrix}1&-1&2\\0&0&0\\0&0&0\end{pmatrix}.$$
【思路】由相似不变量（迹、秩）定 $a,b$，分别求 $A,B$ 的同组特征值特征向量拼成 $P_1,P_2$，得 $P=P_1P_2^{-1}$；再由 $A=PBP^{-1}$ 两种分组方式给出 $Q_1,Q_2$。
【易错】$P$ 的列必须与 $B$ 的特征向量列按相同特征值顺序对应，直接用 $P_1$ 而不乘 $P_2^{-1}$ 一般得不到 $B$；$Q_1,Q_2$ 不唯一，给出一种满足 $A=Q_1Q_2$、$B=Q_2Q_1$ 的分解即可。
