===Q1===
【答案】B
【解】
**① 拆项并化为 $\mathrm{e}^u-1$ 型。** 原式 $=\lim\limits_{x\to0}\dfrac{(1+x)^{\frac1x}-\mathrm{e}}{x}+\mathrm{e}\lim\limits_{x\to0}\dfrac{\ln(1+x)}{x}$，其中 $(1+x)^{\frac1x}=\mathrm{e}^{\frac1x\ln(1+x)}$，故第一项 $=\mathrm{e}\lim\limits_{x\to0}\dfrac{\mathrm{e}^{\frac1x\ln(1+x)-1}-1}{x}$。
**② 用等价无穷小与泰勒展开求第一项。** 因 $\frac{\ln(1+x)}{x}-1\to0$，由 $\mathrm{e}^u-1\sim u$ 及 $\ln(1+x)=x-\frac{x^2}{2}+o(x^2)$：
$$\mathrm{e}\lim_{x\to0}\frac{\frac{\ln(1+x)}{x}-1}{x}=\mathrm{e}\lim_{x\to0}\frac{\ln(1+x)-x}{x^2}=-\frac{\mathrm{e}}{2}.$$
**③ 合并第二项。** $\mathrm{e}\lim\limits_{x\to0}\dfrac{\ln(1+x)}{x}=\mathrm{e}$，故原式 $=-\dfrac{\mathrm{e}}{2}+\mathrm{e}=\dfrac{\mathrm{e}}{2}$，选 B。
【思路】把幂指函数写成 $\mathrm{e}^{\frac1x\ln(1+x)}$，拆分后分别用等价无穷小与 $\ln(1+x)$ 的泰勒展开求极限。
【易错】用 $\mathrm{e}^u-1\sim u$ 前须确认指数 $u=\frac{\ln(1+x)}{x}-1\to0$。原册解析第 2、3 行把 $\mathrm{e}\lim\frac{\frac1x\ln(1+x)-1}{x}$ 与 $\mathrm{e}\lim\frac{\ln(1+x)-x}{x^2}$ 并列相加，按字面计算和为 $-\frac{\mathrm e}{2}-\frac{\mathrm e}{2}+\mathrm e=0$，与最终结论 $\frac{\mathrm e}{2}$ 不自洽，疑中间项分母多印一个 $x$，属排印疑点；正确拆项见上文分步。

===Q2===
【答案】A
【解】
**① 化去分母。** 由 $\cot x=\dfrac{\cos x}{\sin x}=\dfrac{1+ax^2}{x+bx^3}+o(x^3)$ 得
$$\cos x\,(x+bx^3)=(1+ax^2)\sin x+o(x^5).$$
**② 两边作泰勒展开至 $x^5$。** 
$$(x+bx^3)\left[1-\frac{x^2}{2!}+\frac{x^4}{4!}+o(x^4)\right]=(1+ax^2)\left[x-\frac{x^3}{3!}+\frac{x^5}{5!}+o(x^5)\right]+o(x^5),$$
即 $x-\dfrac{x^3}{2}+\dfrac{x^5}{24}+bx^3-\dfrac{b}{2}x^5=x-\dfrac{x^3}{6}+\dfrac{x^5}{120}+ax^3-\dfrac{a}{6}x^5+o(x^5)$。
**③ 比较同次幂系数。** 
$$\begin{cases}-\dfrac12+b=a-\dfrac16\\[4pt] \dfrac1{24}-\dfrac b2=\dfrac1{120}-\dfrac a6\end{cases}$$
解得 $a=-\dfrac25,\ b=-\dfrac1{15}$，选 A。
【思路】把分式等式化为整式等式，两边按 $\sin x,\cos x$ 的泰勒展开比较 $x^3,x^5$ 系数。
【易错】$\cos x$ 须展开到 $x^4$、$\sin x$ 展开到 $x^5$，否则 $x^5$ 系数方程缺项；$o(x^3)$ 乘以 $x+bx^3$ 后升为 $o(x^5)$。

===Q3===
【答案】A
【解】
**① 写出通解。** $y'+y=f(x)$ 的通解为
$$y=\mathrm{e}^{-x}\int_{-\infty}^{x}\mathrm{e}^{t}f(t)\,\mathrm{d}t+C\mathrm{e}^{-x}.$$
**② 由有界性定出 $C$。** 设 $|f(x)|\le M$，则
$$\left|\mathrm{e}^{-x}\int_{-\infty}^{x}\mathrm{e}^{t}f(t)\,\mathrm{d}t\right|\le\mathrm{e}^{-x}\int_{-\infty}^{x}\mathrm{e}^{t}\cdot M\,\mathrm{d}t=M,$$
即积分项有界；而 $\mathrm{e}^{-x}$ 在 $(-\infty,+\infty)$ 内无界，故仅当 $C=0$ 时通解有界，$C\ne0$ 时无界，可排除选项 B、C、D。
**③ 验证周期性。** 设 $f$ 以 $T$ 为周期，令 $u=t-T$：
$$y(x+T)=\mathrm{e}^{-(x+T)}\int_{-\infty}^{x+T}\mathrm{e}^{t}f(t)\,\mathrm{d}t=\mathrm{e}^{-x}\int_{-\infty}^{x}\mathrm{e}^{u}f(u+T)\,\mathrm{d}u=\mathrm{e}^{-x}\int_{-\infty}^{x}\mathrm{e}^{u}f(u)\,\mathrm{d}u=y(x).$$
故该解以 $T$ 为周期，选 A。
【思路】用变上限积分写出通解，靠有界性筛去含 $C\mathrm{e}^{-x}$ 的项，再用换元验证周期。
【易错】$\mathrm{e}^{-x}$ 在 $x\to-\infty$ 时无界，是排除 $C\ne0$ 的关键；周期换元中须用 $f(u+T)=f(u)$。

===Q4===
【答案】C
【解】
**① 构造 $g$ 得上界。** 令 $g(x)=f(x)-f'(0)x$，则 $g'(x)=f'(x)-f'(0)<0$（$f'$ 严格单调减少），又 $g(0)=0$，故 $x\in(0,1)$ 时 $g(x)<0$，即 $\dfrac{f(x)}{x}<f'(0)$。
**② 构造 $h$ 并求导。** 令 $h(x)=\dfrac{f(x)}{x}$，由 $f(0)=0$ 与拉格朗日中值定理：
$$h'(x)=\frac{f'(x)x-f(x)}{x^2}=\frac{f'(x)x-[f(x)-f(0)]}{x^2}=\frac{f'(x)-f'(\xi)}{x}\quad(0<\xi<x).$$
因 $f'$ 严格单调减少且 $\xi<x$，故 $h'(x)<0$，$h$ 单调减少。
**③ 得结论。** 由 $x<1$ 得 $h(x)>h(1)$，即 $\dfrac{f(x)}{x}>\dfrac{f(1)}{1}$，亦即 $f(1)<\dfrac{f(x)}{x}$，选 C。
【思路】两次构造函数（$g$ 与 $h=f/x$），用单调性与拉格朗日中值定理夹出 $\frac{f(x)}{x}$ 的范围。
【易错】$h'(x)$ 中 $\xi$ 介于 $0$ 与 $x$ 之间，须用 $f'(\xi)>f'(x)$ 才能判 $h'<0$；勿漏 $f(0)=0$ 条件。

===Q5===
【答案】A
【解】
**① 求引力函数 $F(x)$。** 质点位于 $x\in[0,L]$，细棒线密度 $\rho=\dfrac{M}{L}$，取 $[t,t+\mathrm{d}t]\subset[2L,3L]$，则 $\mathrm{d}m=\rho\,\mathrm{d}t=\dfrac{M}{L}\mathrm{d}t$，
$$\mathrm{d}F=\frac{GM_0\,\mathrm{d}m}{(t-x)^2},\qquad F(x)=\int_{2L}^{3L}\frac{GM_0M}{L(t-x)^2}\,\mathrm{d}t=\frac{GM_0M}{L}\left(\frac{1}{2L-x}-\frac{1}{3L-x}\right).$$
**② 对位移积分求功。** 取 $[x,x+\mathrm{d}x]\subset[0,L]$，$\mathrm{d}W=F(x)\mathrm{d}x$，
$$W=\frac{GM_0M}{L}\int_0^L\left(\frac{1}{2L-x}-\frac{1}{3L-x}\right)\mathrm{d}x=\left.\frac{GM_0M}{L}\ln\frac{3L-x}{2L-x}\right|_0^L=\frac{GM_0M}{L}\ln\frac43.$$
选 A。
【思路】先对细棒积分得引力 $F(x)$，再对质点位移积分得功。
【易错】细棒在 $[2L,3L]$、质点在 $[0,L]$，两次积分的变量与积分限分别为 $t$ 与 $x$；$\ln\frac{3L-x}{2L-x}$ 代入 $x=L$ 与 $x=0$ 得 $\ln2-\ln\frac32=\ln\frac43$。

===Q6===
【答案】C
【解】
设 $D:x^2+y^2\le1$，逐个判断四个二重积分是否为零。
**① 选项 ①。** $I=\iint_D\sqrt{x^2+y^2}\,(\mathrm{e}^{ax}-\mathrm{e}^{-ay})\,\mathrm{d}x\mathrm{d}y$。由 $D$ 关于 $y=x$ 对称，$\iint_D\sqrt{x^2+y^2}\,\mathrm{e}^{-ay}\,\mathrm{d}x\mathrm{d}y=\iint_D\sqrt{x^2+y^2}\,\mathrm{e}^{-ax}\,\mathrm{d}x\mathrm{d}y$，故 $I=\iint_D\sqrt{x^2+y^2}\,(\mathrm{e}^{ax}-\mathrm{e}^{-ax})\,\mathrm{d}x\mathrm{d}y$；被积函数关于 $x$ 为奇函数且 $D$ 关于 $y$ 轴对称，故 $I=0$。
**② 选项 ②。** $I=\iint_D\sqrt{x^2+y^2}\,(\mathrm{e}^{ax}-\mathrm{e}^{ay})\,\mathrm{d}x\mathrm{d}y$，由轮换对称性
$$I=\frac12\iint_D\sqrt{x^2+y^2}\,\left(\mathrm{e}^{ax}-\mathrm{e}^{ay}+\mathrm{e}^{ay}-\mathrm{e}^{ax}\right)\mathrm{d}x\mathrm{d}y=0.$$
**③ 选项 ③。** $I=\iint_D\sqrt{x^2+y^2}\,(\mathrm{e}^{ax}+\mathrm{e}^{ay})\,\mathrm{d}x\mathrm{d}y$，被积函数 $\ge0$ 且不恒为零，故 $I>0$。
**④ 选项 ④。** 不妨设 $a>0$，$D=\{(x,y)\mid -a\le x\le a,\ x^2\le y\le x^2+1\}$ 关于 $y$ 轴对称，而 $\int_{x^2}^{x^2+1}xf(y)\,\mathrm{d}y=x\int_{x^2}^{x^2+1}f(y)\,\mathrm{d}y$ 关于 $x$ 是奇函数，故 $\int_{-a}^{a}\mathrm{d}x\int_{x^2}^{x^2+1}xf(y)\,\mathrm{d}y=0$。
综上，值为零的是 ①②④ 共 3 个，选 C。
【思路】利用积分区域的对称性、被积函数的奇偶性与轮换对称性逐个判零。
【易错】① 中 $\mathrm{e}^{ax}-\mathrm{e}^{-ax}$ 关于 $x$ 是奇函数；③ 的被积函数恒非负，勿误判为零。

===Q7===
【答案】C
【解】
**① 必要性（$f''\ge0\Rightarrow$ 不等式）。** 不妨设 $h>0$，由微积分基本定理与积分中值定理：
$$f(a+h)+f(a-h)-2f(a)=\int_a^{a+h}f'(x)\,\mathrm{d}x+\int_a^{a-h}f'(x)\,\mathrm{d}x=h\,[f'(\xi_2)-f'(\xi_1)],$$
其中 $a-h<\xi_1<a<\xi_2<a+h$。由 $f''(x)\ge0$ 知 $f'$ 单调增加，$f'(\xi_2)\ge f'(\xi_1)$，故上式 $\ge0$；$h<0$ 同理，$h=0$ 时等号成立。
**② 充分性（不等式 $\Rightarrow f''\ge0$）。** 对 $\forall a\in\mathbb{R}$ 用泰勒公式：
$$f(a+h)=f(a)+f'(a)h+\frac12f''(a)h^2+o(h^2),\quad f(a-h)=f(a)-f'(a)h+\frac12f''(a)h^2+o(h^2),$$
两式相加得 $f(a+h)+f(a-h)-2f(a)=f''(a)h^2+o(h^2)\ge0$，即 $f''(a)+\dfrac{o(h^2)}{h^2}\ge0$。令 $h\to0$ 得 $f''(a)\ge0$，即 $f''(x)\ge0$。
故选 C（二者等价）。
【思路】分必要性与充分性双向证明，分别用积分中值定理与带佩亚诺余项的泰勒公式。
【易错】充分性须对任意 $a$ 成立并令 $h\to0$，才能由一点推到整个区间；$h<0$ 可复用 $h>0$ 的对称性结论。

===Q8===
【答案】A
【解】
**① 由 $AX=0$ 有非零解定 $a$。** $|A|=0$，而
$$|A|=\begin{vmatrix}1&-2&-2\\1&a&a\\a&4&a\end{vmatrix}=(a+2)(a-4)=0,$$
得 $a=-2$ 或 $a=4$。
**② 由 $BX=A$ 无解再定 $a$。** 无解说明 $A$ 的列向量组不能由 $B$ 的列向量组线性表示，故 $B$ 的列向量组线性相关（否则 $B$ 列满秩时任意同维列向量都可由其表示，矛盾），即 $|B|=0$：
$$|B|=\begin{vmatrix}1&1&a\\1&a&1\\a&1&1\end{vmatrix}=-(a-1)^2(a+2)=0,$$
得 $a=1$ 或 $a=-2$。
**③ 取交集。** 公共解为 $a=-2$，选 A。
【思路】分别由齐次方程有非零解、矩阵方程无解得到 $a$ 的候选集合，取交集。
【易错】原册【注】：当 $a=-2$ 时对 $(B,A)$ 作初等行变换（竖虚线分隔 $B$ 与 $A$ 的列）
$$(B,A)=\begin{pmatrix}1&1&-2&\vdots&1&-2&-2\\1&-2&1&\vdots&1&-2&-2\\-2&1&1&\vdots&-2&4&-2\end{pmatrix}\to\begin{pmatrix}1&0&-1&\vdots&1&-2&0\\0&1&-1&\vdots&0&0&0\\0&0&0&\vdots&0&0&1\end{pmatrix},$$
末行出现 $0=1$，故 $(0,0,1)^{\mathrm{T}}$ 不能由 $B$ 的列向量组线性表示，验证 $BX=A$ 无解；$a=4$ 不满足 $|B|=0$ 须舍去。

===Q9===
【答案】D
【解】
**① 化简判据。** 由 $\alpha_1,\alpha_2,\alpha_3,\beta$ 线性无关知 $\alpha_1,\alpha_2,\alpha_3$ 线性无关，故两组四个向量线性相关与否，只取决于 $k\beta+\gamma$ 与 $\beta+k\gamma$ 能否由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示。
**② 讨论 $k$。** 已知 $\beta$ 不能、$\gamma$ 能由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示，故 $k\beta+\gamma$ 当 $k=0$ 时可表示、当 $k\ne0$ 时不可表示——随 $k$ 而变，因此选项 A、B 不能选。
**③ 判定 C、D。** $\beta+k\gamma$ 因含 $\beta$ 而总是不可由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示，故含 $\beta+k\gamma$ 的那组恒线性无关，选项 C 不正确；综上只有 D 正确。
【思路】把「四个向量相关」化为「新向量能否由 $\alpha_1,\alpha_2,\alpha_3$ 线性表示」，再按 $k$ 讨论。
【易错】$k$ 是未定参数，$k\beta+\gamma$ 的相关性随 $k$ 变化，不能一概而论；$\beta+k\gamma$ 恒不可表示。

===Q10===
【答案】B
【解】
**① 由同解得秩条件。** 若 $A^{\mathrm{T}}X=0$ 的解均是 $b^{\mathrm{T}}X=0$ 的解，则 $A^{\mathrm{T}}X=0$ 与 $\begin{cases}A^{\mathrm{T}}X=0\\b^{\mathrm{T}}X=0\end{cases}$ 同解，故 $r(A^{\mathrm{T}})=r\begin{pmatrix}A^{\mathrm{T}}\\b^{\mathrm{T}}\end{pmatrix}$，即 $r(A)=r(A,b)$，从而 $AX=b$ 有解，但无法确定是否有无穷多解，故选项 B 的说法错误，应选 B。
**② 排除 A。** 若 $AX=b$ 有唯一解，则 $AX=0$ 只有零解，$|A|\ne0$，$|A^{\mathrm{T}}A|=|A^{\mathrm{T}}|\cdot|A|=|A|^2\ne0$，A 成立。
**③ 排除 C。** 若 $AX=b$ 有无穷多解，则 $|A|=0$，$A^{*}b=A^{*}AX=|A|EX=0$，即 $b$ 是 $A^{*}X=0$ 的解，C 成立。
**④ 排除 D。** 由 $A^{*}b=0\ (b\ne0)$ 知 $A^{*}X=0$ 有非零解，$r(A^{*})<n$；由 $A_{11}\ne0$ 得 $r(A^{*})=1$，故 $r(A)=n-1$。由 $A^{*}A=|A|E=0$ 知 $A$ 的第 $2,3,\cdots,n$ 列是 $A^{*}X=0$ 的基础解系，故 $b=C_2\alpha_2+C_3\alpha_3+\cdots+C_n\alpha_n$，$(0,C_2,C_3,\cdots,C_n)^{\mathrm{T}}$ 是 $AX=b$ 的解，且 $r(A)=n-1$ 故有无穷多解，D 成立。
【思路】把「解集包含」转成秩条件 $r(A)=r(A,b)$，再逐个检验四个选项。
【易错】原册【注】：结论「$A$ 为 $n$ 阶实矩阵时 $A^{\mathrm{T}}AX=0$ 与 $AX=0$ 同解」，证法是设 $A^{\mathrm{T}}Aa=0$ 则 $(Aa)^{\mathrm{T}}(Aa)=|Aa|^2=0\Rightarrow Aa=0$；并由 $A_{11}=(-1)^{1+1}\begin{vmatrix}a_{22}&\cdots&a_{2n}\\\vdots&&\vdots\\a_{n2}&\cdots&a_{nn}\end{vmatrix}\ne0$ 得删去首行首列后的列向量组线性无关、增加分量后仍无关，故 $(\alpha_2,\cdots,\alpha_n)$ 线性无关，$(0,C_2,\cdots,C_n)^{\mathrm{T}}$ 为 $AX=b$ 的解。另：原册 p35 该两处下标印作 $b=C_2\alpha_2+C_1\alpha_1+\cdots$ 与 $(0,C_2,C_2,\cdots,C_n)^{\mathrm{T}}$，与 p36 注不一致，疑下标排印衍误，以后者 $b=C_2\alpha_2+\cdots+C_n\alpha_n$、$(0,C_2,\cdots,C_n)^{\mathrm{T}}$ 为准。

===Q11===
【答案】$\dfrac{2\sqrt2}{3}$
【解】
**① 参数化并求一阶导。** 视 $\theta$ 为参数，$\begin{cases}x=r\cos\theta=(1+\cos\theta)\cos\theta\\y=r\sin\theta=(1+\cos\theta)\sin\theta\end{cases}$，
$$\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{\cos\theta+\cos2\theta}{-\sin\theta-\sin2\theta}=-\frac{2\cos\frac{3\theta}{2}\cos\frac{\theta}{2}}{2\sin\frac{3\theta}{2}\cos\frac{\theta}{2}}=-\cot\frac{3\theta}{2}.$$
**② 求二阶导。** 
$$\frac{\mathrm{d}^2y}{\mathrm{d}x^2}=\frac{\mathrm{d}}{\mathrm{d}\theta}\left(-\cot\frac{3\theta}{2}\right)\frac{\mathrm{d}\theta}{\mathrm{d}x}=-\frac32\cdot\frac{1}{\sin^2\frac{3\theta}{2}}\cdot\frac{1}{2\sin\frac{3\theta}{2}\cos\frac{\theta}{2}}=-\frac34\frac{1}{\sin^3\frac{3\theta}{2}\cos\frac{\theta}{2}}.$$
**③ 代入求曲率半径。** 当 $\theta=\dfrac\pi2$ 时 $\dfrac{\mathrm{d}y}{\mathrm{d}x}=1$、$\dfrac{\mathrm{d}^2y}{\mathrm{d}x^2}=-3$，故
$$R=\frac{(1+y'^2)^{\frac32}}{|y''|}=\frac{2\sqrt2}{3}.$$
【思路】把极坐标曲线写成参数方程，用参数求导算到二阶导，再套曲率半径公式。
【易错】$\frac{\mathrm d^2y}{\mathrm dx^2}=\frac{\mathrm d}{\mathrm d\theta}\!\left(\frac{\mathrm dy}{\mathrm dx}\right)\cdot\frac{\mathrm d\theta}{\mathrm dx}$，切勿漏乘 $\frac{\mathrm d\theta}{\mathrm dx}$；和差化积后 $\cos\frac\theta2$ 可约去。

===Q12===
【答案】$\pi$
【解】
**① 判敛。** $x=1,\ x=3$ 是反常积分的瑕点，
$$\lim_{x\to1^+}(x-1)^{\frac12}\cdot\frac{1}{\sqrt{(x-1)(3-x)}}=\frac1{\sqrt2},\qquad \lim_{x\to3^-}(3-x)^{\frac12}\cdot\frac{1}{\sqrt{(x-1)(3-x)}}=\frac1{\sqrt2},$$
幂次 $\frac12<1$，故原积分收敛。
**② 配方换元求值。** 
$$I=\int_1^3\frac{\mathrm{d}(x-2)}{\sqrt{1-(x-2)^2}}\xlongequal{x-2=u}\int_{-1}^{1}\frac{\mathrm{d}u}{\sqrt{1-u^2}}=2\int_0^1\frac{\mathrm{d}u}{\sqrt{1-u^2}}=\left.2\arcsin u\right|_0^1=\pi.$$
【思路】先用瑕点判别法确认收敛，再配方换元化为 $\arcsin$ 的标准积分。
【易错】$\sqrt{(x-1)(3-x)}=\sqrt{1-(x-2)^2}$ 须配方；两端都是瑕点，须分别判别敛散。

===Q13===
【答案】$2$
【解】
**① 算 $1^\infty$ 型极限。** 
$$\lim_{x\to\infty}\left(\cos\frac ax\right)^{x^2}=\lim_{x\to\infty}\left[1-\left(\sin\frac ax\right)^2\right]^{\frac{x^2}{2}}=\mathrm{e}^{\lim\limits_{x\to\infty}\frac{x^2}{2}\ln\left[1-\left(\sin\frac ax\right)^2\right]}=\mathrm{e}^{-\lim\limits_{x\to\infty}\frac{x^2}{2}\left(\sin\frac ax\right)^2}=\mathrm{e}^{-\frac{a^2}{2}}.$$
**② 算积分的极限。** 由积分中值定理 $\int_x^{x+1}f(t)\,\mathrm{d}t=f(\xi),\ \xi\in(x,x+1)$，
$$\lim_{x\to\infty}\int_x^{x+1}f(t)\,\mathrm{d}t=\lim_{\xi\to\infty}f(\xi)=\mathrm{e}^{-2}.$$
**③ 比较指数定 $a$。** 由 $\mathrm{e}^{-\frac{a^2}{2}}=\mathrm{e}^{-2}$ 得 $a^2=4$，解得 $a=2$。
【思路】两端分别化为 $\mathrm{e}^{-\frac{a^2}{2}}$ 与 $\mathrm{e}^{-2}$，比较指数定出 $a$。
【易错】$\cos\frac ax=\left(1-\sin^2\frac ax\right)^{1/2}$，故外层指数是 $\frac{x^2}{2}$；$\sin\frac ax\sim\frac ax$ 得 $-\frac{a^2}{2}$，勿漏平方。

===Q14===
【答案】$2(x-1)\mathrm{e}^x+x+2$
【解】
**① 由齐次通解反推方程。** 通解 $y=(C_1+C_2x)\mathrm{e}^x$ 说明特征根 $\lambda_1=\lambda_2=1$，故 $a=-(\lambda_1+\lambda_2)=-2,\ b=\lambda_1\lambda_2=1$；方程为 $y''-2y'+y=x$，可求得特解 $y^{*}=x+2$，全解
$$y(x)=(C_1+C_2x)\mathrm{e}^x+x+2.$$
**② 由等价无穷小定 $C_1,C_2$。** 由 $y(x)\sim x\ (x\to0)$ 有
$$\lim_{x\to0}\frac{(C_1+C_2x)\mathrm{e}^x+x+2}{x}=1\Rightarrow\lim_{x\to0}\bigl[(C_1+C_2x)\mathrm{e}^x+2\bigr]=0\Rightarrow C_1=-2.$$
再用洛必达法则 $\lim\limits_{x\to0}\dfrac{(-2+C_2x)\mathrm{e}^x+2}{x}=\lim\limits_{x\to0}\dfrac{\mathrm{e}^x(C_2-2+C_2x)}{1}=0$，得 $C_2=2$。
**③ 写出结果。** $y(x)=2(x-1)\mathrm{e}^x+x+2$。
【思路】由齐次通解反推特征方程与系数，设出含 $C_1,C_2$ 的全解，用 $y(x)\sim x$ 两次取极限定常数。
【易错】$y(x)\to0$ 只是 $y\sim x$ 的必要条件，先得 $C_1=-2$；必须再用一次极限（洛必达）才得 $C_2$。

===Q15===
【答案】$\dfrac\pi4\ln2$
【解】
**① 列出体积积分。** 
$$V=\int_1^{+\infty}\pi\left(\frac{\sqrt{x\ln x}}{1+x^2}\right)^2\mathrm{d}x=\pi\int_1^{+\infty}\frac{x\ln x}{(1+x^2)^2}\,\mathrm{d}x.$$
**② 凑微分分部积分。** 由 $\mathrm{d}\left(\frac{1}{1+x^2}\right)=-\frac{2x}{(1+x^2)^2}\mathrm{d}x$：
$$V=-\frac\pi2\int_1^{+\infty}\ln x\,\mathrm{d}\!\left(\frac{1}{1+x^2}\right)=-\left.\frac\pi2\frac{\ln x}{1+x^2}\right|_1^{+\infty}+\frac\pi2\int_1^{+\infty}\frac{\mathrm{d}x}{x(1+x^2)}.$$
**③ 裂项求值。** $\dfrac{1}{x(1+x^2)}=\dfrac1x-\dfrac{x}{1+x^2}$，故
$$V=\frac\pi2\int_1^{+\infty}\left(\frac1x-\frac{x}{1+x^2}\right)\mathrm{d}x=\left.\frac\pi2\ln\frac{x}{\sqrt{1+x^2}}\right|_1^{+\infty}=\frac\pi4\ln2.$$
【思路】旋转体体积化为反常积分，凑 $\frac{1}{(1+x^2)^2}$ 分部积分后裂项。
【易错】$x\to+\infty$ 时 $\frac{\ln x}{1+x^2}\to0$ 使边界项为零；$\ln\frac{x}{\sqrt{1+x^2}}$ 在上限取极限为 $0$、下限为 $-\frac12\ln2$。

===Q16===
【答案】$-3$
【解】
**① 判定三特征值相等。** 不同特征值的特征向量之和不是特征向量，故要使 $\alpha_1+\alpha_2$ 是 $A$ 的特征向量须 $\lambda_1=\lambda_2$；同理 $\alpha_1+\alpha_2+\alpha_3$ 为特征向量须 $\lambda_1=\lambda_3$，故 $\lambda_1=\lambda_2=\lambda_3$。
**② 求公共特征值。** 由 $|A|=\lambda_1\lambda_2\lambda_3=\lambda_1^3=-1$，得 $\lambda_1=\lambda_2=\lambda_3=-1$。
**③ 求迹。** $\operatorname{tr}A=\lambda_1+\lambda_2+\lambda_3=-3$。
【思路】用「特征向量之和仍为特征向量 ⇒ 对应特征值相同」把三特征值合一，再由行列式求值。
【易错】$\lambda_1^3=-1$ 在实数范围内只有 $-1$ 一解；迹等于全部特征值之和（含重数）。

===Q17===
【答案】$n=3,\ a=\dfrac1{12}$
【解】
**① 换元化简积分。** 令 $u=x-t$，
$$\int_0^x tf(x-t)\,\mathrm{d}t=\int_0^x(x-u)f(u)\,\mathrm{d}u=x\int_0^x f(u)\,\mathrm{d}u-\int_0^x uf(u)\,\mathrm{d}u.$$
**② 洛必达降阶。** 
$$\lim_{x\to0}\frac{\int_0^x tf(x-t)\,\mathrm{d}t-\frac12x^2}{ax^n}=\lim_{x\to0}\frac{x\int_0^x f(u)\,\mathrm{d}u-\int_0^x uf(u)\,\mathrm{d}u-\frac12x^2}{ax^n}=\lim_{x\to0}\frac{\int_0^x f(u)\,\mathrm{d}u-x}{nax^{n-1}}=\lim_{x\to0}\frac{f(x)-1}{n(n-1)ax^{n-2}}=1.$$
**③ 求 $\lim\frac{f(x)-1}{x}$。** 由题设 $\lim\limits_{x\to0}\dfrac{xf(x)-\ln(1+x)}{x^2}=1$，
$$\lim_{x\to0}\frac{f(x)-1}{x}=\lim_{x\to0}\frac{xf(x)-\ln(1+x)+\ln(1+x)-x}{x^2}=1+\lim_{x\to0}\frac{\frac{1}{1+x}-1}{2x}=1-\frac12=\frac12.$$
**④ 定 $n,a$。** $\lim\limits_{x\to0}\dfrac{f(x)-1}{n(n-1)ax^{n-2}}=\lim\limits_{x\to0}\dfrac{f(x)-1}{x}\cdot\dfrac{1}{n(n-1)ax^{n-3}}=\dfrac12\lim\limits_{x\to0}\dfrac{1}{n(n-1)ax^{n-3}}=1$，故 $n-3=0$ 且 $\dfrac12\cdot\dfrac{1}{n(n-1)a}=1$，得 $n=3,\ a=\dfrac1{12}$。
【思路】换元把卷积型积分化为变上限积分，两次洛必达后用已知极限先求 $\lim\frac{f(x)-1}{x}$，再定 $n$ 与 $a$。
【易错】$\left(\int_0^x f(u)\mathrm{d}u-x\right)'=f(x)-1$；极限为 $1$ 要求 $x^{n-3}$ 的指数为 $0$，否则为 $0$ 或发散。

===Q18===
【答案】（I）$f(x)=n^2\mathrm{e}^{\frac xn}-(n+1)x$；（II）驻点 $x_n=n\ln\left(1+\frac1n\right)$（极小值点），$\lim\limits_{n\to\infty}x_n^n=\mathrm{e}^{-\frac12}$
【解】
**（I）解一阶线性微分方程。**
**① 套通解公式。** 方程 $f'(x)-\dfrac1n f(x)=\left(1+\dfrac1n\right)x-1-n$ 的通解为
$$f(x)=\mathrm{e}^{\int\frac1n\mathrm{d}x}\left\{\int\left[\left(1+\frac1n\right)x-1-n\right]\mathrm{e}^{-\int\frac1n\mathrm{d}x}\mathrm{d}x+C\right\}=\mathrm{e}^{\frac xn}\left\{\int\left[\left(1+\frac1n\right)x-(1+n)\right]\mathrm{e}^{-\frac xn}\mathrm{d}x+C\right\}=-(n+1)x+C\mathrm{e}^{\frac xn}.$$
**② 由初值定常数。** $f(0)=n^2$ 得 $C=n^2$，故 $f(x)=n^2\mathrm{e}^{\frac xn}-(n+1)x$。
**（II）求极值点与数列极限。**
**① 求驻点并判型。** $f'(x)=n\mathrm{e}^{\frac xn}-(1+n)=0$ 得驻点 $x=x_n=n\ln\left(1+\frac1n\right)$；又 $f''(x)=\mathrm{e}^{\frac xn}>0$，故 $x_n$ 为极小值点。
**② 化为指数型极限。** 由 $x_n=\dfrac{\ln(1+\frac1n)}{\frac1n}$，
$$\lim_{n\to\infty}x_n^n=\lim_{n\to\infty}\left[\frac{\ln\left(1+\frac1n\right)}{\frac1n}\right]^n=\mathrm{e}^{\lim\limits_{n\to\infty}n\ln\left[n\ln\left(1+\frac1n\right)\right]}.$$
**③ 用泰勒展开算指数上的极限。** 由 $\ln(1+u)\sim u$ 及 $\ln\left(1+\frac1n\right)-\frac1n=-\frac{1}{2n^2}+o\left(\frac1{n^2}\right)$：
$$\lim_{n\to\infty}n\ln\left[n\ln\left(1+\frac1n\right)\right]=\lim_{n\to\infty}n\left[\frac{\ln\left(1+\frac1n\right)}{\frac1n}-1\right]=\lim_{n\to\infty}\frac{\ln\left(1+\frac1n\right)-\frac1n}{\frac1{n^2}}=-\frac12,$$
故 $\lim\limits_{n\to\infty}x_n^n=\mathrm{e}^{-\frac12}$。
【思路】（I）解一阶线性方程并用初值定常数；（II）先求驻点，再把 $1^\infty$ 型极限取对数化为 $\frac00$ 型用泰勒展开。
【易错】$n\to\infty$ 时 $x_n\to1$，属 $1^\infty$ 型，须取对数；$\ln(1+\frac1n)$ 须展开到 $\frac1{n^2}$ 项才得 $-\frac12$。

===Q19===
【答案】极大值 $z=1$（在 $(1,1,1)$ 处），极小值 $z=-1$（在 $(-1,-1,-1)$ 处）
【解】
**① 由全微分还原 $f$。** 
$$\mathrm{d}f(x,y,z)=(2x-2y)\mathrm{d}x+(4y-2x-2z)\mathrm{d}y+(6z-2y)\mathrm{d}z=\mathrm{d}\left(x^2+2y^2+3z^2-2xy-2yz+C\right),$$
即 $f(x,y,z)=x^2+2y^2+3z^2-2xy-2yz+C$。由 $f(1,1,1)=0$ 得 $C=-2$，故曲面方程为
$$x^2+2y^2+3z^2-2xy-2yz-2=0.$$
**② 隐函数求偏导定驻点。** 视 $z=z(x,y)$，两边分别对 $x,y$ 求偏导：
$$\begin{cases}2x+6z\cdot z'_x-2y-2yz'_x=0\\4y+6z\cdot z'_y-2x-2z-2yz'_y=0\end{cases}$$
令 $z'_x=0,\ z'_y=0$ 得 $x=y,\ 2y-x-z=0$，即 $x=y=z$；代入原方程得 $x=\pm1$，故有两个驻点 $(1,1,1)$ 与 $(-1,-1,-1)$。
**③ 再求一次偏导并判别。** 对上两式再求偏导得
$$\begin{cases}1+3(z'_x)^2+(3z-y)z''_{xx}=0\\3z'_x\cdot z'_y-1-z'_x+(3z-y)z''_{xy}=0\\2+3(z'_y)^2-2z'_y+(3z-y)z''_{yy}=0\end{cases}$$
在 $(1,1,1)$ 处：$A=z''_{xx}=-\dfrac12,\ B=z''_{xy}=\dfrac12,\ C=z''_{yy}=-1$，$AC-B^2=\dfrac14>0,\ A<0$，故为极大值点，极大值 $z=1$；在 $(-1,-1,-1)$ 处：$A=\dfrac12,\ B=-\dfrac12,\ C=1$，$AC-B^2=\dfrac14>0,\ A>0$，故为极小值点，极小值 $z=-1$。
【思路】由全微分还原隐函数方程，隐函数求导找驻点，再用 $AC-B^2$ 判别极值。
【易错】再求偏导时 $z$ 是 $x,y$ 的函数，$(3z-y)z''$ 项不可漏；须 $AC-B^2>0$ 且看 $A$ 的符号定极大或极小。

===Q20===
【答案】$I=-\dfrac{3\pi}{2}$
【解】
**① 用对称性化简被积函数。** $D$ 关于直线 $y=x$ 对称，故 $\iint_D x\,\mathrm{d}x\mathrm{d}y=\iint_D y\,\mathrm{d}x\mathrm{d}y$，
$$I=\iint_D(x^2+y^2-4x)\,\mathrm{d}x\mathrm{d}y=\iint_D(x^2+y^2-2x-2y)\,\mathrm{d}x\mathrm{d}y=\iint_D\left[(x-1)^2+(y-1)^2-2\right]\mathrm{d}x\mathrm{d}y.$$
$D$ 是圆 $(x-1)^2+(y-1)^2\le1$，面积为 $\pi$，故 $I=\iint_D(x-1)^2\mathrm{d}x\mathrm{d}y+\iint_D(y-1)^2\mathrm{d}x\mathrm{d}y-2\pi$。
**② 计算 $\iint_D(x-1)^2\mathrm{d}x\mathrm{d}y$。** 
$$\iint_D(x-1)^2\,\mathrm{d}x\mathrm{d}y=\int_0^2\mathrm{d}x\int_{1-\sqrt{1-(x-1)^2}}^{1+\sqrt{1-(x-1)^2}}(x-1)^2\,\mathrm{d}y=2\int_0^2(x-1)^2\sqrt{1-(x-1)^2}\,\mathrm{d}x$$
$$\xlongequal{x-1=\sin t}2\int_{-\frac\pi2}^{\frac\pi2}\sin^2t\cos^2t\,\mathrm{d}t=4\int_0^{\frac\pi2}\sin^2t\,(1-\sin^2t)\,\mathrm{d}t=4\left(\frac12\times\frac\pi2-\frac34\times\frac12\times\frac\pi2\right)=\frac\pi4.$$
**③ 合并结果。** 同理可得 $\iint_D(y-1)^2\,\mathrm{d}x\mathrm{d}y=\dfrac\pi4$，故
$$I=\frac\pi4+\frac\pi4-2\pi=-\frac{3\pi}{2}.$$
【思路】用轮换对称性把 $-4x$ 配成 $-2x-2y$，平移后化为圆盘上的标准积分。
【易错】原册【注】：也可用二重积分一般换元 $x-1=u,\ y-1=v$ 一次算出
$$\iint_D\left[(x-1)^2+(y-1)^2\right]\mathrm{d}x\mathrm{d}y=\iint_{u^2+v^2<1}(u^2+v^2)\,\mathrm{d}u\mathrm{d}v=\int_0^{2\pi}\mathrm{d}\theta\int_0^1 r^2\cdot r\,\mathrm{d}r=2\pi\cdot\frac14=\frac\pi2,$$
故 $I=\dfrac\pi2-2\pi=-\dfrac{3\pi}{2}$；勿忘减去 $2\iint_D\mathrm{d}x\mathrm{d}y=2\pi$。

===Q21===
【答案】（I）$4\int_0^a xf(x)\,\mathrm{d}x>3a\int_0^a f(x)\,\mathrm{d}x$；（II）$\dfrac h2\left[f'(h)+f'(0)\right]>f(h)-f(0)\ (\forall h\in(0,a))$
【解】
**（I）构造函数逐次求导。**
**① 构造 $F$ 并求三阶导。** 令 $F(a)=\int_0^a xf(x)\,\mathrm{d}x-\dfrac34a\int_0^a f(x)\,\mathrm{d}x$，则
$$F'(a)=\frac14af(a)-\frac34\int_0^a f(x)\,\mathrm{d}x,\qquad F''(a)=-\frac12f(a)+\frac14af'(a),$$
$$F'''(a)=-\frac14\left[f'(a)-f'(0)\right]+\frac14af''(a)=-\frac14af''(\xi)+\frac14af''(a)=\frac14a\left[f''(a)-f''(\xi)\right]\quad(0<\xi<a).$$
**② 逐层判号。** 由 $f''(x)$ 严格单调增加知 $F'''(a)>0\Rightarrow F''(a)$ 单调增加；又 $F''(0)=0$ 故 $F''(a)>0\Rightarrow F'(a)$ 单调增加；又 $F'(0)=0$ 故 $F'(a)>0\Rightarrow F(a)$ 单调增加；而 $F(0)=0$ 故 $F(a)>0$，即 $4\int_0^a xf(x)\,\mathrm{d}x>3a\int_0^a f(x)\,\mathrm{d}x$。
**（II）另作辅助函数。**
**① 构造并求导。** 将 $h$ 改为 $x$，作辅助函数 $F(x)=\dfrac x2\left[f'(x)+f'(0)\right]-\left[f(x)-f(0)\right]$，$F(0)=0$，则
$$F'(x)=\frac12\left[f'(x)+f'(0)\right]+\frac x2f''(x)-f'(x)=\frac x2f''(x)-\left[\frac12f'(x)-\frac12f'(0)\right]=\frac x2\left[f''(x)-f''(\xi)\right]\quad(0<\xi<x).$$
**② 判号得结论。** 由 $f''(x)$ 严格单调增加知 $F'(x)>0$，从而 $F(x)>F(0)=0,\ x\in(0,a)$。故对 $\forall h\in(0,a)$ 有
$$\frac h2\left[f'(h)+f'(0)\right]>f(h)-f(0).$$
【思路】两问都用「构造辅助函数＋逐次求导＋拉格朗日中值定理＋$f''$ 严格单调增加」把导数符号逐层推回函数符号。
【易错】$f'(a)-f'(0)=af''(\xi)$、$\frac12[f'(x)-f'(0)]=\frac x2f''(\xi)$ 均用中值定理；$F(0)=F'(0)=F''(0)=0$ 是逐层判号的起点。

===Q22===
【答案】（I）$a=-1,\ b=-2$，$X=\begin{pmatrix}k_1+\frac32&k_2-\frac32\\-\frac12&\frac12\\k_1&k_2\end{pmatrix}$（$k_1,k_2$ 为任意常数）；（II）$GB^{\mathrm{T}}$ 的行向量组与 $B^{\mathrm{T}}$ 的行向量组等价
【解】
**（I）由同解定参数并解矩阵方程。**
**① 化为秩条件。** 由 $A^{\mathrm{T}}X=0$ 的解均是 $B^{\mathrm{T}}X=0$ 的解，知 $A^{\mathrm{T}}X=0$ 与 $\begin{cases}A^{\mathrm{T}}X=0\\B^{\mathrm{T}}X=0\end{cases}$ 同解，故 $r(A^{\mathrm{T}})=r\begin{pmatrix}A^{\mathrm{T}}\\B^{\mathrm{T}}\end{pmatrix}$，即 $r(A)=r(A,B)$。
**② 初等行变换。** 
$$(A,B)=\begin{pmatrix}a&1&1&\vdots&b&2\\0&a-1&0&\vdots&1&-1\\1&1&a&\vdots&1&-1\end{pmatrix}\to\begin{pmatrix}1&1&a&\vdots&1&-1\\0&a-1&0&\vdots&1&-1\\a&1&1&\vdots&b&2\end{pmatrix}\to\begin{pmatrix}1&1&a&\vdots&1&-1\\0&a-1&0&\vdots&1&-1\\0&1-a&1-a^2&\vdots&b-a&a+2\end{pmatrix}\to\begin{pmatrix}1&1&a&\vdots&1&-1\\0&a-1&0&\vdots&1&-1\\0&0&1-a^2&\vdots&b-a+1&a+1\end{pmatrix}.$$
由 $1-a^2=0$ 得 $a=\pm1$；$a=1$ 时 $r(A)=1$ 而 $r(A,B)\ne1$，舍去；$a=-1$ 时
$$(A,B)\to\begin{pmatrix}1&1&-1&\vdots&1&-1\\0&-2&0&\vdots&1&-1\\0&0&0&\vdots&b+2&0\end{pmatrix},$$
当 $b=-2$ 时才有 $r(A)=r(A,B)=2$。故 $a=-1,\ b=-2$。
**③ 解 $AX=B$。** 此时
$$(A,B)\to\begin{pmatrix}1&1&-1&\vdots&1&-1\\0&-2&0&\vdots&1&-1\\0&0&0&\vdots&0&0\end{pmatrix}\Rightarrow X=\begin{pmatrix}k_1+\frac32&k_2-\frac32\\-\frac12&\frac12\\k_1&k_2\end{pmatrix}\quad(k_1,k_2\ \text{为任意常数}).$$
**（II）证明行向量组等价。**
**① 取极大线性无关组。** 由（I）$(A,B)$ 列向量的一个极大线性无关组构成矩阵
$$G=\begin{pmatrix}-1&1\\0&-2\\1&1\end{pmatrix},\qquad B^{\mathrm{T}}=\begin{pmatrix}-2&1&1\\2&-1&-1\end{pmatrix}.$$
**② 证两齐次方程组同解。** 显然 $B^{\mathrm{T}}X=0$ 的解是 $GB^{\mathrm{T}}X=0$ 的解；反之设 $\alpha$ 是 $GB^{\mathrm{T}}X=0$ 的解，即 $GB^{\mathrm{T}}\alpha=0$，故 $B^{\mathrm{T}}\alpha$ 是 $GX=0$ 的解。由 $r(G_{3\times2})=2$（$G$ 列满秩）知 $GX=0$ 只有零解，故 $B^{\mathrm{T}}\alpha=0$。于是 $GB^{\mathrm{T}}X=0$ 与 $B^{\mathrm{T}}X=0$ 同解，即 $GB^{\mathrm{T}}$ 的行向量组与 $B^{\mathrm{T}}$ 的行向量组等价。
【思路】（I）把解集包含转成秩相等，用行变换定参数并解矩阵方程；（II）借 $G$ 列满秩证两个齐次方程组同解，从而行向量组等价。
【易错】$a=1$ 使 $r(A)<r(A,B)$，必须舍去；$G$ 是 $3\times2$ 列满秩矩阵，$GX=0$ 只有零解是（II）的关键。
