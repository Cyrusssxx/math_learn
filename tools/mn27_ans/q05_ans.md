===Q1===
【答案】D
【解】
**① 排除 (A)(C)。** 取
$$f(x)=\begin{cases}x^2,&x\text{为有理数},\\1,&x\text{为无理数},\end{cases}$$
则 $f(x)$ 在 $x=0$ 处不连续、不可导；此时
$$g(x)=\begin{cases}x^2,&x\text{为有理数},\\0,&x\text{为无理数},\end{cases}$$
在 $x=0$ 的某去心邻域内 $\left|\dfrac{g(x)-g(0)}{x}\right|\leqslant|x|$，故 $\lim\limits_{x\to0}\dfrac{g(x)-g(0)}{x}=0$，即 $g(x)$ 在 $x=0$ 处连续、可导，故 (A)(C) 错误。
**② 排除 (B)。** 取 $f(x)\equiv1$，则 $g(x)=D(x)$ 在 $x=0$ 处不连续，但 $f(x)$ 连续，故 (B) 错误。
**③ 验证 (D)。** 若 $g(x)$ 在 $x=0$ 处可导，则
$$g'(0)=\lim_{x\to0}\frac{g(x)}{x}=\lim_{x\to0}\frac{f(x)-f(0)}{x}D(x)=f'(0)\lim_{x\to0}D(x)$$
应存在，但 $\lim\limits_{x\to0}D(x)$ 不存在，与 $f'(0)\ne0$ 矛盾，故 (D) 正确。
【思路】用狄利克雷函数构造反例逐项排除，再以反证法确认 (D)。
【易错】$D(x)$ 处处无极限，故 $f'(0)\ne0$ 时 $g'(0)$ 必不存在；勿由 $g$ 连续反推 $f$ 连续。另：本册 8 页页眉交替印作「全国硕士研究生入学考试数学模拟试卷参考答案」与「超越"5+5"套试卷(数学二)参考答案」，同一答案册出现两套书名，属排印不一致。

===Q2===
【答案】A
【解】
**① $x\to+\infty$ 的主阶。** 
$$\lim_{x\to+\infty}\frac{f(x)}{x^{2/3}}=\lim_{x\to+\infty}\frac{\sqrt[3]{x^2+\ln^2|x|}}{x^{2/3}}=\lim_{x\to+\infty}\sqrt[3]{1+\frac{\ln^2|x|}{x^2}}=1,$$
由洛必达法则
$$\lim_{x\to+\infty}\frac{g(x)}{x}=\lim_{x\to+\infty}\frac{2x+e^x-e^{-x}}{x^2+e^x+e^{-x}}=1,\qquad \lim_{x\to+\infty}\frac{h(x)}{e^x}=\lim_{x\to+\infty}\frac{e^x+x^2}{e^x}=1+\lim_{x\to+\infty}\frac{x^2}{e^x}=1.$$
**② $x\to-\infty$ 的主阶。** 
$$\lim_{x\to-\infty}\frac{g(x)}{-x}=\lim_{x\to-\infty}\frac{\ln(x^2+e^x+e^{-x})}{-x}=-\lim_{x\to-\infty}\frac{2x+e^x-e^{-x}}{x^2+e^x+e^{-x}}=1,\qquad \lim_{x\to-\infty}\frac{h(x)}{x^2}=\lim_{x\to-\infty}\frac{e^x+x^2}{x^2}=1.$$
**③ 比较。** 由 $\lim\limits_{x\to+\infty}\dfrac{e^x}{x}=+\infty$，$\lim\limits_{x\to+\infty}\dfrac{x}{\sqrt[3]{x^2}}=+\infty$，知 $|x|$ 充分大时 $h(x)>g(x)>f(x)$，选 (A)。
【思路】用提主阶与洛必达定出三函数在 $\pm\infty$ 的增长阶，再比较大小。
【易错】$f(x)=\sqrt[3]{x^2+\ln^2|x|}$ 的主阶是 $x^{2/3}$ 而非 $x$；$x\to-\infty$ 时 $g(x)\sim-x$、$h(x)\sim x^2$，必须与 $+\infty$ 分开讨论；原册 $f$ 中被开方是 $x^2+\ln^2|x|$（平方），扫描件极易误读成 $x^3+\ln^4|x|$。

===Q3===
【答案】A
【解】
**① 平移化对称区间。** 令 $x=\dfrac{\pi}{2}+t$，则 $x^2-\pi x+\pi^2=t^2+\dfrac{3}{4}\pi^2$，$\pi+\cos x=\pi-\sin t$，于是
$$\text{原式}=\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\frac{\pi-\sin t}{t^2+\frac{3}{4}\pi^2}\,dt=\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\frac{\pi}{t^2+\frac{3}{4}\pi^2}\,dt,$$
其中 $\dfrac{\sin t}{t^2+\frac{3}{4}\pi^2}$ 为奇函数，在对称区间上积分为 $0$。
**② 用偶性与反正切求值。** 
$$=\frac{4}{\sqrt3}\arctan\frac{2t}{\sqrt3\pi}\Bigg|_{0}^{\frac{\pi}{2}}=\frac{4}{\sqrt3}\cdot\frac{\pi}{6}=\frac{2\sqrt3}{9}\pi.$$
【思路】配方并平移，把分母化为 $t^2+a^2$，由奇偶性消去正弦项后套用反正切原函数。
【易错】别忘了 $\cos\left(\dfrac{\pi}{2}+t\right)=-\sin t$ 产生奇函数项；$\arctan\dfrac{1}{\sqrt3}=\dfrac{\pi}{6}$，系数 $\dfrac{4}{\sqrt3}$ 含偶性折半，勿误写成 $\dfrac{2}{\sqrt3}$。

===Q4===
【答案】C
【解】
**① 排除 (A)。** 取
$$f(x)=\begin{cases}-x^2,&x\leqslant0,\\-\sqrt{x},&x>0,\end{cases}$$
满足 $f$ 在 $[-1,1]$ 连续、$(-1,0)$ 内 $f''<0$、$(0,1)$ 内 $f''>0$，但 $f(0)=0$ 为极大值，故 (A) 错。
**② 排除 (B)。** 反例同上，$f$ 在 $x=0$ 不可导，$f'(x)$ 在 $x=0$ 无定义，谈不上极小值点，故 (B) 错。
**③ 验证 (C)。** $f''$ 在 $x=0$ 两侧变号，$x=0$ 为拐点；由拐点的必要条件，若 $f''(0)$ 存在则 $f''(0)=0$，故 (C) 正确。
**④ 排除 (D)。** 取 $f(x)=x^5$，$f''(x)=20x^3$ 在 $(-1,0)$ 内为负、$(0,1)$ 内为正，但 $f''(0)=0$，故 (D) 错。
【思路】凹凸性变号给出拐点，用拐点必要条件配合分段反例筛选四个选项。
【易错】题设只假设 $f$ 连续，未保证 $f'(0)$、$f''(0)$ 存在，(A)(B) 都可能因不可导而失效；(D) 的反例是 $x^5$（不是 $x^2$ 或 $x^4$）。另：(B) 原文作「$f'(x)$ 的极小值点」（带一撇），与 (A) 的 $f(x)$ 不对称，扫描件易看漏该撇，属需留意的排印细节。

===Q5===
【答案】C
【解】
**① $x\to0^+$ 给出上界。** 由
$$\lim_{x\to0^+}\frac{\ln(1+x^p)}{x^\lambda\sqrt{1+x^q}}\cdot x^{\lambda-p}=1,$$
$\int_0^1\dfrac{1}{x^{\lambda-p}}\,dx$ 对任意 $p>0$ 收敛，得 $\lambda-p<1$，故 $\lambda\leqslant1$。
**② $x\to+\infty$ 给出下界。** 此时 $\sqrt{1+x^q}\sim x^{q/2}$，$\int_1^{+\infty}\dfrac{\ln(1+x^p)}{x^{\lambda+q/2}}\,dx$ 对任意 $p,q>0$ 收敛，得 $\lambda+\dfrac{q}{2}>1$，故 $\lambda\geqslant1$。
**③ 合并。** 综上 $\lambda=1$。
【思路】把反常积分拆成 $0$ 与 $+\infty$ 两处，用等价无穷小（大）定出 $\lambda$ 两个方向的不等式。
【易错】"$p,q$ 为任意正实数"是关键：令 $p\to0^+$ 得 $\lambda\leqslant1$，令 $q\to0^+$ 得 $\lambda\geqslant1$；忽略"任意"会误选 (A) 或 (B)。

===Q6===
【答案】A
【解】
**① 偏导数是否存在依赖 $\alpha,\beta$。** 
$$\lim_{x\to0}\frac{f(x,0)-f(0,0)}{x-0}=\lim_{x\to0}\frac{x^2+\alpha|x|}{x}=\alpha\lim_{x\to0}\frac{|x|}{x},$$
故当且仅当 $\alpha=0$ 时 $f'_x(0,0)$ 存在且为 $0$；同理当且仅当 $\beta=0$ 时 $f'_y(0,0)$ 存在且为 $0$。
**② 可微性也依赖 $\alpha,\beta$。** 若偏导数存在，则 $\alpha=\beta=0$ 且 $f'_x(0,0)=f'_y(0,0)=0$，此时
$$\lim_{\substack{x\to0\\y\to0}}\frac{f(x,y)-f(0,0)-xf'_x(0,0)-yf'_y(0,0)}{\sqrt{x^2+y^2}}=\lim_{\substack{x\to0\\y\to0}}\frac{(x-y)^2}{\sqrt{x^2+y^2}}=0,$$
即 $f$ 在 $(0,0)$ 可微；若 $\alpha,\beta$ 不全为零则偏导数不存在，必不可微。故两者都与 $\alpha,\beta$ 有关。
【思路】用定义判定偏导数存在性（归结为 $\lim\frac{|x|}{x}$），再用可微定义验证差商极限为 $0$。
【易错】$\alpha|x|$、$\beta|y|$ 在原点不可导是核心；可微的前提是偏导数存在，不能只验证 $\dfrac{(x-y)^2}{\sqrt{x^2+y^2}}\to0$ 就断言"任意 $\alpha,\beta$ 都可微"。

===Q7===
【答案】D
【解】
**① 验证 ①。** 对 $F(x,y,z)=0$ 两边求微分，得 $F'_x\,dx+F'_y\,dy+F'_z\,dz=0$，① 正确。
**② 验证 ②。** 把 $z=z(x,y)$ 代入后两边对 $x$ 求偏导，得 $F'_x+z'_xF'_z=0$，② 正确。
**③ 验证 ③④。** 由隐函数求导公式
$$z'_x=-\frac{F'_x}{F'_z},\qquad x'_y=-\frac{F'_y}{F'_x},\qquad y'_z=-\frac{F'_z}{F'_y},$$
故
$$z'_x\cdot x'_y\cdot y'_z=\left(-\frac{F'_x}{F'_z}\right)\cdot\left(-\frac{F'_y}{F'_x}\right)\cdot\left(-\frac{F'_z}{F'_y}\right)=-1,$$
即 ④ 正确、③（三者相加为 $-1$）错误，故选 (D)。
【思路】用全微分与隐函数求导公式逐个检验四个结论，选出 ①②④。
【易错】三个偏导数是"相乘"得 $-1$，不是"相加"得 $-1$；③ 与 ④ 只差运算符，扫描版极易看错，这是本题最主要的辨识点。

===Q8===
【答案】C
【解】
**① 由基础解系定秩。** $A^*x=0$ 的基础解系含 $2$ 个线性无关向量，即 $3-r(A^*)=2$，故 $r(A^*)=1$，从而 $r(A)=2$。
**② 行变换。** 
$$A=\begin{pmatrix}1&-1&1\\2a&1-a&2a\\a&-a&a^2-2\end{pmatrix}\longrightarrow\begin{pmatrix}1&-1&1\\0&a+1&0\\0&0&(a-2)(a+1)\end{pmatrix}.$$
**③ 定 $a$。** 当 $a=-1$ 时 $r(A)=1$，不满足题意；当 $a=2$ 时 $r(A)=2$，满足题意，故选 (C)。
【思路】用伴随矩阵秩的性质把条件化为 $r(A)=2$，再对 $A$ 作初等行变换讨论参数。
【易错】$r(A^*)=1\iff r(A)=n-1=2$（若 $r(A)\leqslant n-2$ 则 $A^*=O$），勿误判为 $r(A)=1$；$a=-1$ 使秩降为 $1$ 必须排除。

===Q9===
【答案】A
【解】
**① 必要性。** $AB$ 为 $n$ 阶可逆阵，$r(AB)=n$；由 $n=r(AB)\leqslant r(A)\leqslant n$ 与 $n=r(AB)\leqslant r(B)\leqslant n$，得 $r(A)=r(B)=n$，故 (A) 是必要条件。
**② (A) 不充分。** 取
$$A=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix},\qquad B=\begin{pmatrix}0&0\\1&0\\0&1\end{pmatrix},\qquad AB=\begin{pmatrix}0&0\\1&0\end{pmatrix},$$
$AB$ 不可逆，故 (A) 非充分，答案选 (A)。
**③ 辨析 (B)。** 由 Sylvester 不等式 $r(AB)\geqslant r(A)+r(B)-m$，若 $r(A)+r(B)\geqslant m+n$ 则 $r(AB)\geqslant n$，又 $r(AB)\leqslant n$，故 $r(AB)=n$，(B) 充分；但取 $A=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$，$B=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$ 时 $AB=E$ 可逆而 $r(A)+r(B)=4<m+n=5$，故 (B) 不必要。
【思路】用 $r(AB)\leqslant\min\{r(A),r(B)\}$ 证必要性、用 $r(AB)\geqslant r(A)+r(B)-m$ 辨析 (B)，并各配反例。
【易错】题干要"必要非充分"；(B) 恰是"充分非必要"，方向最易选反。注意 $A$ 为 $n\times m$、$B$ 为 $m\times n$，判据里出现的是 $m+n$ 而不是 $2n$。

===Q10===
【答案】D
【解】
**① 求 $A$ 的特征值。** 
$$A=\begin{pmatrix}1&a&1\\a&b&a\\1&a&1\end{pmatrix}$$
为对称阵，第 $1,3$ 行相同故 $|A|=0$；$\lambda=2$ 为二重特征值，由 $\operatorname{tr}A=2+b=4$ 得 $b=2$，再由 $r(A-2E)=1$ 得 $a=0$。故 $A$ 的特征值为 $2,2,0$，且 $A$ 可对角化。
**② 排除 (A)(B)。** 二者特征值均为 $2,2,1$，与 $A$ 不同，不可能相似。
**③ 排除 (C)。** (C) 特征值为 $2,2,0$，但
$$r(C-2E)=r\begin{pmatrix}0&1&1\\0&0&1\\0&0&-2\end{pmatrix}=2\ne3-2,$$
故 (C) 不可对角化，与可对角化的 $A$ 不相似。
**④ 验证 (D)。** (D) 特征值为 $2,2,0$，且
$$r(D-2E)=r\begin{pmatrix}0&0&2\\0&0&1\\0&0&-2\end{pmatrix}=1=3-2,$$
故 (D) 可对角化，与 $A$ 相似。
【思路】实对称阵必可对角化；同特征值只是相似的必要条件，还须核对二重特征值 $\lambda=2$ 的几何重数 $3-r(2E-M)$。
【易错】四个选项里 (C)(D) 特征值都与 $A$ 相同，区别只在是否可对角化；判据是 $r(\lambda E-M)=n-$重数$=1$，不是 $r(M)=2$。

===Q11===
【答案】$(a,b)=(-2,1)$
【解】
**① 统一凑出 $\ln(n+1)$。** 令 $u_n=\ln\left[(n+1)(n+2)^a(n+3)^b\right]$，则
$$u_n=\ln(n+1)+a\ln(n+1)+a\ln\left(1+\frac{1}{n+1}\right)+b\ln(n+1)+b\ln\left(1+\frac{2}{n+1}\right).$$
**② 泰勒展开。** 用 $\ln(1+t)=t-\dfrac{t^2}{2}+o(t^2)$ 得
$$u_n=(1+a+b)\ln(n+1)+\frac{a+2b}{n+1}-\left(\frac{a}{2}+2b\right)\frac{1}{(n+1)^2}+o\left(\frac{1}{n^2}\right).$$
**③ 由阶数列方程。** $u_n$ 是 $\dfrac{1}{n^2}$ 的同阶无穷小，须消去 $\ln(n+1)$ 项与 $\dfrac{1}{n+1}$ 项，故 $1+a+b=0$，$a+2b=0$，解得 $a=-2$，$b=1$。
【思路】把 $\ln(n+2)$、$\ln(n+3)$ 都写成 $\ln(n+1)$ 加小量，展开后按目标阶数令前两项系数为零。
【易错】题干条件是 $\dfrac{1}{n^2}$ 的同阶（不是 $\dfrac{1}{n}$ 的同阶），因此要同时消去 $\ln(n+1)$ 与 $\dfrac{1}{n+1}$；只列 $1+a+b=0$ 会少一个方程。扫描件中 $\dfrac{1}{n^2}$ 的上标较小，极易误读为 $\dfrac{1}{n}$，属识读疑点。

===Q12===
【答案】$1$
【解】
**① 交换积分次序。** 原积分区域为 $0\leqslant x\leqslant u,\ x\leqslant y\leqslant u$，即 $0\leqslant x\leqslant y\leqslant u$，故
$$F(u)=\int_0^u dy\int_0^y\sin^4(x-y)\,dx.$$
**② 求导并换元。** 
$$F'(u)=\int_0^u\sin^4(x-u)\,dx=\int_{-u}^{0}\sin^4t\,dt=\int_0^u\sin^4t\,dt,\qquad F''(u)=\sin^4u,$$
其中用到换元 $t=x-u$ 与 $\sin^4t$ 为偶函数。
**③ 用华里士公式与反函数求导。** 
$$F'\left(\frac{\pi}{2}\right)=\int_0^{\frac{\pi}{2}}\sin^4t\,dt=\frac{3}{4}\cdot\frac{1}{2}\cdot\frac{\pi}{2}=\frac{3}{16}\pi,\qquad F''\left(\frac{\pi}{2}\right)=1,$$
因 $G$ 是 $F'$ 的反函数，故
$$G'\left(\frac{3}{16}\pi\right)=\frac{1}{F''\left(\frac{\pi}{2}\right)}=1.$$
【思路】交换累次积分次序把 $u$ 只留在上限，求导得 $F'(u)$，再用反函数求导公式 $G'=\dfrac{1}{F''}$。
【易错】原积分内层是 $\int_x^u$，交换后为 $\int_0^y\sin^4(x-y)\,dx$，勿把区域写反；$G$ 是 $F'$ 的反函数，自变量 $\dfrac{3\pi}{16}$ 对应 $u=\dfrac{\pi}{2}$（因 $F'(\frac{\pi}{2})=\frac{3\pi}{16}$），分母是 $F''$ 而非 $F'$。

===Q13===
【答案】$\pi-2$
【解】
**① 利用对称性去绝对值。** 设 $D_1=\left\{(x,y)\mid 0\leqslant x\leqslant\dfrac{\pi}{2},\ 0\leqslant y\leqslant\dfrac{\pi}{2},\ x\geqslant y\right\}$，由 $x,y$ 对称得
$$\text{原式}=2\iint_{D_1}\sin|x-y|\,d\sigma=2\iint_{D_1}\sin(x-y)\,d\sigma=2\int_0^{\frac{\pi}{2}}dx\int_0^x\sin(x-y)\,dy.$$
**② 积分求值。** 
$$=2\int_0^{\frac{\pi}{2}}(1-\cos x)\,dx=2\left(\frac{\pi}{2}-1\right)=\pi-2.$$
【思路】按 $x\geqslant y$ 分半区域去掉绝对值，再化为累次积分。
【易错】$\sin|x-y|$ 关于 $x=y$ 对称，可折半乘 $2$；在 $D_1$ 上 $|x-y|=x-y$，内层对 $y$ 积分得 $1-\cos x$，别把内层限写成 $y$ 到 $\dfrac{\pi}{2}$。

===Q14===
【答案】$1$
【解】
**① 先求 $f'_x(0,0)$。** 
$$f'_x(0,0)=\lim_{x\to0}\frac{f(x,0)-f(0,0)}{x}=\lim_{x\to0}\frac{0-0}{x}=0.$$
**② 求 $(x,y)\ne(0,0)$ 时的 $f'_x$。** 
$$f'_x(x,y)=\frac{y^3\cos(xy^3)(x^2+y^2)-2x\sin(xy^3)}{(x^2+y^2)^2},$$
故 $f'_x(0,y)=\dfrac{y^3\cdot y^2}{y^4}=y$。
**③ 用定义求混合偏导。** 
$$f''_{xy}(0,0)=\lim_{y\to0}\frac{f'_x(0,y)-f'_x(0,0)}{y}=\lim_{y\to0}\frac{y-0}{y}=1.$$
【思路】分段点处的混合偏导必须用定义：先求 $f'_x(0,y)$，再对 $y$ 取差商极限。
【易错】题干分母是 $x^2+y^2$（不是 $x^2+y^4$），扫描件易看错；原册用 $f''_{xy}(0,0)$ 表示"先对 $x$ 再对 $y$"求导，与部分教材 $\dfrac{\partial^2f}{\partial y\partial x}$ 的下标顺序约定不同，须按计算步骤理解；不能直接对 $f''_{xy}(x,y)$ 取极限（该偏导在原点不连续）。

===Q15===
【答案】$\dfrac{3}{\sqrt e-1}e^{\frac{x^2}{2}}-2$
【解】
**① 把积分记为常数。** 设 $a=\displaystyle\int_0^1 t\,y(t)\,dt$，则方程化为 $y'(x)=xy(x)+ax$。
**② 解一阶线性方程。** 
$$y(x)=e^{\int x\,dx}\left(\int ax\,e^{-\int x\,dx}\,dx+C\right)=e^{\frac{x^2}{2}}\left(\int ax\,e^{-\frac{x^2}{2}}\,dx+C\right)=-a+Ce^{\frac{x^2}{2}}.$$
**③ 定 $C$ 与 $a$。** 由 $y(1)-y(0)=3$ 得 $(\sqrt e-1)C=3$，即 $C=\dfrac{3}{\sqrt e-1}$；又
$$a=\int_0^1 x\,y(x)\,dx=\int_0^1\left(-ax+Cx\,e^{\frac{x^2}{2}}\right)dx=-\frac{a}{2}+(\sqrt e-1)C=-\frac{a}{2}+3,$$
得 $a=2$。故 $y(x)=\dfrac{3}{\sqrt e-1}e^{\frac{x^2}{2}}-2$。
【思路】把方程中的定积分 $\int_0^1 t\,y(t)\,dt$ 视为常数 $a$，解线性方程后再自洽定出 $a$ 与 $C$。
【易错】$a=\int_0^1 t\,y(t)\,dt=\int_0^1 x\,y(x)\,dx$ 是同一个常数，必须把求出的 $y(x)$ 代回该积分得到自洽方程才能定出 $a=2$；漏掉这一步会少一个条件。

===Q16===
【答案】$\dfrac12$
【解】
**① 由条件解出 $A$。** 由 $(A-E)^{-1}=B-E$ 得 $A-E=(B-E)^{-1}$，于是
$$A=(B-E)^{-1}+E=(B-E)^{-1}\left[E+(B-E)\right]=(B-E)^{-1}B.$$
**② 取行列式。** 其中
$$B=\begin{pmatrix}0&1&0\\0&3&1\\2&0&0\end{pmatrix},\qquad |B|=2,\qquad |B-E|=4,$$
故
$$|A|=\frac{|B|}{|B-E|}=\frac{2}{4}=\frac{1}{2}.$$
【思路】由逆矩阵关系把 $A$ 表成 $(B-E)^{-1}B$，再对乘积取行列式。
【易错】$|B-E|=4$ 为正（不是 $-4$），故 $|A|=\dfrac12$ 为正；原册答案行与解一致，若把 $|B-E|$ 误算成 $-4$ 会得到 $-\dfrac12$。

===Q17===
【答案】$\dfrac{2}{3}e^2$
【解】
**① 提出常数 $e^2$。** 分子 $(1+x)^{\frac{2}{x}}-e^2+e^2\ln(1+x)=e^2\left[e^{\frac{2\ln(1+x)}{x}-2}-1+\ln(1+x)\right]$，故
$$\text{原式}=e^2\lim_{x\to0}\frac{e^{\frac{2\ln(1+x)}{x}-2}-1+\ln(1+x)}{x^2}.$$
**② 泰勒展开。** 由 $\dfrac{2\ln(1+x)}{x}-2=-x+\dfrac{2}{3}x^2+o(x^2)$，$\ln(1+x)=x-\dfrac12x^2+o(x^2)$，以及 $e^u=1+u+\dfrac12u^2+o(u^2)$，方括号内为
$$\left(-x+\frac{2}{3}x^2\right)+\frac{1}{2}x^2+\left(x-\frac12x^2\right)+o(x^2)=\frac{2}{3}x^2+o(x^2).$$
**③ 得极限。** 原式 $=e^2\lim\limits_{x\to0}\dfrac{\frac{2}{3}x^2+o(x^2)}{x^2}=\dfrac{2}{3}e^2$。
【思路】把 $(1+x)^{2/x}$ 写成 $e^2e^{\frac{2\ln(1+x)}{x}-2}$，指数与对数都展开到 $x^2$ 阶后合并。
【易错】题干是 $(1+x)^{\frac{2}{x}}-e^{2}\left[1-\ln(1+x)\right]$：指数为 $\dfrac{2}{x}$、常数为 $e^2$，扫描件中这两个 "$2$" 很小，极易误读为 $(1+x)^{1/x}$ 与 $e^x$；若误读则分子不趋于 $0$，极限不存在。展开必须到 $x^2$ 阶，$x$ 一次项恰好抵消。

===Q18===
【答案】$f(x)=\dfrac{1}{27}(x+1)^3$
【解】
**① 由相切条件定初值。** 曲线 $y=\varphi(x)$ 与 $y=\int_{-1}^{x}\left(t+\sqrt{1-t^2}\right)^2dt$ 在 $x=1$ 处相切，且 $\varphi$ 是 $f$ 的反函数，故
$$\varphi(1)=\int_{-1}^{1}\left(t+\sqrt{1-t^2}\right)^2dt=\int_{-1}^{1}\left(1+2t\sqrt{1-t^2}\right)dt=2,$$
$$\varphi'(1)=\left.\left(\int_{-1}^{x}\left(t+\sqrt{1-t^2}\right)^2dt\right)'\right|_{x=1}=\left.\left(x+\sqrt{1-x^2}\right)^2\right|_{x=1}=1,$$
从而 $f(2)=1$，$f'(2)=1$。
**② 把方程化为 $f$ 的 ODE。** 由 $\dfrac{dx}{dy}=\dfrac{1}{f'(x)}$，$\dfrac{d^2x}{dy^2}=-\dfrac{f''(x)}{[f'(x)]^3}$，代入
$$\left(\frac{dy}{dx}\right)^2\frac{d^2x}{dy^2}=-\frac{1}{x+1}-\frac{x+1}{9}\cdot\frac{dx}{dy}$$
得
$$-\frac{f''(x)}{f'(x)}=-\frac{1}{x+1}-\frac{x+1}{9}\cdot\frac{1}{f'(x)},$$
即 $f''(x)-\dfrac{1}{x+1}f'(x)=\dfrac{x+1}{9}$。
**③ 解出 $f$。** 令 $p=f'(x)$，则 $\dfrac{dp}{dx}-\dfrac{1}{x+1}p=\dfrac{x+1}{9}$，解得
$$p=e^{\int\frac{dx}{x+1}}\left(\int\frac{x+1}{9}e^{-\int\frac{dx}{x+1}}dx+C_1\right)=(x+1)\left(\frac{x}{9}+C_1\right).$$
代入 $f'(2)=1$ 得 $C_1=\dfrac{1}{9}$，故 $f'(x)=\dfrac{1}{9}(x+1)^2$，$f(x)=\dfrac{1}{27}(x+1)^3+C_2$；由 $f(2)=1$ 得 $C_2=0$。
【思路】先由相切与反函数关系得到 $f(2)=1,\ f'(2)=1$，再用反函数二阶导公式把方程化为关于 $f'(x)$ 的一阶线性方程。
【易错】$\varphi(1)=2$ 意味着 $f(2)=1$（反函数自变量互换），$\varphi'(1)=1$ 意味着 $f'(2)=\dfrac{1}{\varphi'(1)}=1$；$\dfrac{d^2x}{dy^2}=-\dfrac{f''}{[f']^3}$ 的负号勿丢；曲线被积函数是 $\left(t+\sqrt{1-t^2}\right)^2$（平方，非三次方）。

===Q19===
【答案】（I）$f'(x_0)=0$；（II）存在 $\xi\in(a,b)$ 使 $f'(\xi)=0$
【解】
**（I）由最大值点证 $f'(x_0)=0$。**
**① 单侧导数的符号。** 因 $f(x_0)$ 为 $(a,b)$ 内最大值，
$$f'_+(x_0)=\lim_{x\to x_0^+}\frac{f(x)-f(x_0)}{x-x_0}\leqslant0,\qquad f'_-(x_0)=\lim_{x\to x_0^-}\frac{f(x)-f(x_0)}{x-x_0}\geqslant0.$$
**② 夹出结论。** $f$ 在 $x_0$ 可导，$f'_+(x_0)=f'_-(x_0)=f'(x_0)$，故二者同为 $0$，即 $f'(x_0)=0$。

**（II）由端点导数符号把最大值逼入开区间。**
**① 端点附近的保号性。** 由 $f'_+(a)=\lim\limits_{x\to a^+}\dfrac{f(x)-f(a)}{x-a}>0$，存在 $\delta_1>0$，当 $x\in(a,a+\delta_1)\subset(a,b)$ 时 $\dfrac{f(x)-f(a)}{x-a}>0$，故 $f(x)>f(a)$；由 $f'_-(b)=\lim\limits_{x\to b^-}\dfrac{f(x)-f(b)}{x-b}<0$，存在 $\delta_2>0$，当 $x\in(b-\delta_2,b)\subset(a,b)$ 时 $\dfrac{f(x)-f(b)}{x-b}<0$，结合 $x-b<0$ 得 $f(x)>f(b)$。
**② 用 (I) 收尾。** $f$ 在 $[a,b]$ 上可导故连续，最大值存在；因 $f(a),f(b)$ 都不是最大值，最大值在 $(a,b)$ 内某点 $\xi$ 取得，由 (I) 得 $f'(\xi)=0$。
【思路】(I) 用左右导数不等式夹出 $f'(x_0)=0$；(II) 用保号性把最大值逼进开区间，再套 (I)。
【易错】(I) 中 $x\to x_0^+$ 时分子 $\leqslant0$、分母 $>0$，故右导数 $\leqslant0$；左导数因分母 $<0$ 而 $\geqslant0$，两者不等号方向相反，勿写反。(II) 在 $b$ 附近 $x-b<0$，由比值 $<0$ 应推出 $f(x)>f(b)$，才能说明端点不是最大值。

===Q20===
【答案】（I）$z''_{xx}-2z''_{xy}+z''_{yy}=(x-y)^2f''_{11}-2f'_1$；（II）$-6$
【解】
**（I）逐项求二阶偏导。**
**① 一阶偏导。** 对 $z=f(xy,\ g(x+y))$ 用链式法则得 $z'_x=f'_1\cdot y+f'_2\cdot g'$，$z'_y=f'_1\cdot x+f'_2\cdot g'$。
**② 二阶偏导。** 
$$z''_{xx}=y\left(f''_{11}y+f''_{12}g'\right)+\left(f''_{21}y+f''_{22}g'\right)g'+f'_2g''=y^2f''_{11}+2yf''_{12}g'+f''_{22}g'^2+f'_2g'',$$
$$z''_{xy}=f'_1+y\left(f''_{11}x+f''_{12}g'\right)+\left(f''_{21}x+f''_{22}g'\right)g'+f'_2g''=f'_1+xyf''_{11}+(x+y)f''_{12}g'+f''_{22}g'^2+f'_2g'',$$
$$z''_{yy}=x\left(f''_{11}x+f''_{12}g'\right)+\left(f''_{21}x+f''_{22}g'\right)g'+f'_2g''=x^2f''_{11}+2xf''_{12}g'+f''_{22}g'^2+f'_2g''.$$
**③ 合并。** 代入得
$$z''_{xx}-2z''_{xy}+z''_{yy}=(x-y)^2f''_{11}-2f'_1.$$

**（II）代入具体 $f$。**
**① 求偏导。** $f(u,v)=u^2+3v$ 时 $f'_1=2u$，$f''_{11}=2$。
**② 代入 $x=1,y=2$。** 此时 $u=xy=2$，
$$z''_{xx}-2z''_{xy}+z''_{yy}=f''_{11}(2,g(3))-2f'_1(2,g(3))=2-4\times2=-6.$$
【思路】链式法则求出三个二阶偏导，利用 $f''_{12}=f''_{21}$ 合并消去含 $g'$、$g''$ 的项，再代入具体 $f$ 求值。
【易错】$f$ 具有二阶连续偏导数才保证 $f''_{12}=f''_{21}$，合并后含 $g'$、$g''$ 的项全部抵消，只剩 $-2f'_1$；(II) 中 $u=xy=2$ 使 $f'_1=4$，勿误用 $f'_1=2$ 而得到 $-2$ 或 $-4$。

===Q21===
【答案】最大值 $e$（在 $(1,0),(0,1)$ 取得），最小值 $1$（在 $(0,0)$ 取得）
【解】
**① 把二重积分记为常数 $A$。** 设 $A=\iint\limits_D xyf(x,y)\,d\sigma$，则 $f(x,y)=e^{x^2+y^2}-Axy$，于是
$$A=\iint_D xy\left(e^{x^2+y^2}-Axy\right)d\sigma=\iint_D xy\,e^{x^2+y^2}d\sigma-A\iint_D x^2y^2\,d\sigma.$$
**② 极坐标算两个积分。** 
$$=\int_0^{\frac{\pi}{2}}d\theta\int_0^1 r\cos\theta\cdot r\sin\theta\cdot e^{r^2}\cdot r\,dr-A\int_0^{\frac{\pi}{2}}d\theta\int_0^1 r^2\cos^2\theta\cdot r^2\sin^2\theta\cdot r\,dr$$
$$=\frac12\cdot\frac12\int_0^1 t e^t\,dt-A\int_0^{\frac{\pi}{2}}\left(\sin^2\theta-\sin^4\theta\right)d\theta\cdot\frac16=\frac14-\frac{\pi}{96}A\qquad(t=r^2).$$
故 $A=\dfrac{24}{96+\pi}$，即 $f(x,y)=e^{x^2+y^2}-\dfrac{24}{96+\pi}xy$。
**③ 讨论 $D$ 上的最值。** 内部由 $f'_x=2xe^{x^2+y^2}-\dfrac{24y}{96+\pi}=0$、$f'_y=2ye^{x^2+y^2}-\dfrac{24x}{96+\pi}=0$ 得驻点 $(0,0)$ 不在 $D$ 内，舍去；边界 $y=0\ (0\leqslant x\leqslant1)$ 与 $x=0\ (0\leqslant y\leqslant1)$ 上 $f=e^{x^2}$、$f=e^{y^2}$ 单调增，候选点 $(1,0),(0,1),(0,0)$；边界 $x^2+y^2=1\ (x>0,y>0)$ 上令
$$L(x,y,\lambda)=e-\frac{24}{96+\pi}xy+\lambda\left(x^2+y^2-1\right),$$
由
$$L'_x=-\frac{24}{96+\pi}y+2\lambda x=0,\qquad L'_y=-\frac{24}{96+\pi}x+2\lambda y=0,\qquad L'_\lambda=x^2+y^2-1=0$$
解得 $(x,y)=\left(\dfrac{\sqrt2}{2},\dfrac{\sqrt2}{2}\right)$。
**④ 比较。** 由 $f(1,0)=f(0,1)=e$，$f(0,0)=1$，$f\left(\dfrac{\sqrt2}{2},\dfrac{\sqrt2}{2}\right)=e-\dfrac{12}{96+\pi}$，得最大值为 $e$，最小值为 $1$。
【思路】积分方程中的 $\iint_D xyf\,d\sigma$ 是常数，设 $A$ 后自洽求出，再按"内部驻点 + 两条坐标轴边界 + 圆弧上拉格朗日乘子"求最值。
【易错】$A$ 必须自洽求解（$A=\frac14-\frac{\pi}{96}A$），别把 $A$ 当作 $0$；$D$ 是第一象限的四分之一圆，极坐标 $\theta\in\left[0,\frac{\pi}{2}\right]$；$f\left(\frac{\sqrt2}{2},\frac{\sqrt2}{2}\right)=e-\frac{12}{96+\pi}$ 介于 $1$ 与 $e$ 之间，不是最值。

===Q22===
【答案】（I）$3y_1^2-3y_3^2$；（II）$P=\begin{pmatrix}1&0&-2\\0&1&2\\0&0&1\end{pmatrix}$；（III）见解中两组通解
【解】
**（I）定 $a$ 与特征值。**
**① 矩阵与 $a$。** 二次型矩阵
$$A=\begin{pmatrix}1&0&a\\0&-1&2\\a&2&0\end{pmatrix}.$$
正负惯性指数均为 $1$，故 $A$ 的特征值一正一负一零，$|A|=a^2-4=\lambda_1\lambda_2\lambda_3=0$，由 $a>0$ 得 $a=2$。
**② 特征多项式与标准形。** 
$$|\lambda E-A|=\lambda^3-9\lambda=\lambda(\lambda-3)(\lambda+3),$$
故正交变换下的标准形为 $3y_1^2-3y_3^2$。

**（II）配方法求 $P$。**
**① 配方与变换。** 
$$f(x_1,x_2,x_3)=(x_1+2x_3)^2-(x_2-2x_3)^2,$$
令 $y_1=x_1+2x_3$，$y_2=x_2-2x_3$，$y_3=x_3$，则规范形为 $f=y_1^2-y_2^2$。
**② 求 $P$。** 由 $x=Py$，
$$P=\begin{pmatrix}1&0&2\\0&1&-2\\0&0&1\end{pmatrix}^{-1}=\begin{pmatrix}1&0&-2\\0&1&2\\0&0&1\end{pmatrix}.$$

**（III）解 $f=0$。**
**① 因式分解。** 
$$f=(x_1+2x_3)^2-(x_2-2x_3)^2=(x_1+x_2)(x_1-x_2+4x_3)=0,$$
等价于 $x_1+x_2=0$ 或 $x_1-x_2+4x_3=0$。
**② 两组通解。** 
$$x_1+x_2=0:\quad x=k_1\begin{pmatrix}-1\\1\\0\end{pmatrix}+k_2\begin{pmatrix}0\\0\\1\end{pmatrix},$$
$$x_1-x_2+4x_3=0:\quad x=k_3\begin{pmatrix}1\\1\\0\end{pmatrix}+k_4\begin{pmatrix}-4\\0\\1\end{pmatrix},$$
$k_1,k_2,k_3,k_4$ 为任意实数。
【思路】(I) 由惯性指数知 $|A|=0$ 定 $a$，再求特征值；(II) 配方后用 $x=Py$ 取逆得 $P$；(III) 平方差分解后分别求两个齐次方程的基础解系。
【易错】(I) 标准形写作 $3y_1^2-3y_3^2$ 跳过 $y_2$（零特征值排在第二位），并非漏项，属原册的编号方式；(II) $x=Py$ 要求 $P$ 是"由 $y$ 到 $x$"的变换，故须对系数矩阵取逆，直接写原矩阵会错；(III) $f=0$ 是两个平面的并集，每组通解须各含两个任意常数。
