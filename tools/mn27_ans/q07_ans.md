===Q1===
【答案】D
【解】
**① 判断 (A)。** 由 $a_n>0$ 且 $\lim\limits_{n\to\infty}a_n=A$ 只能推出 $A\ge0$（如 $a_n=\frac1n\to0$），故 (A) 错。
**② 判断 (B)。** 取 $a_n=\begin{cases} n, & n\text{ 为奇数},\\ 0, & n\text{ 为偶数}, \end{cases}$ 则子列 $a_{2k-1}\to\infty$，但 $\lim\limits_{n\to\infty}a_n$ 不存在，故 (B) 错。
**③ 判断 (C)。** 取 $a_n=n$，有 $\lim\limits_{n\to\infty}\frac{a_{n+1}}{a_n}=\lim\limits_{n\to\infty}\frac{n+1}{n}=1$，但 $\lim\limits_{n\to\infty}a_n=\infty$，故 (C) 错。
**④ 判断 (D)。** $f$ 在 $x=A$ 处连续且 $\lim\limits_{n\to\infty}a_n=A$，由海涅定理（函数极限与数列极限的等价性）得 $\lim\limits_{n\to\infty}f(a_n)=f(A)$，故 (D) 正确。
【思路】用三个反例逐一排除 (A)(B)(C)，由海涅定理确认 (D)。
【易错】把「$a_n>0$」误推成「极限 $A>0$」；或误以为 $\lim\frac{a_{n+1}}{a_n}=1$ 能保证 $a_n$ 收敛。
===Q2===
【答案】D
【解】
**① 求 $f'(1)$。** 由题设 $\frac{\Delta y}{\Delta x}=1+\frac{o(\Delta x)}{\Delta x}$，令 $\Delta x\to0$ 得 $f'(1)=1$；又 $f(1)=0$。
**② 洛必达化简。** 对 $\frac{0}{0}$ 型极限求导（上限 $e^{x^2}$ 给出因子 $2x$）：
$$\lim_{x\to0}\frac{\int_1^{e^{x^2}}f(t)\,dt}{\ln(1+x^4)}=\lim_{x\to0}\frac{2xe^{x^2}f(e^{x^2})}{4x^3}=\frac12\lim_{x\to0}\frac{f(e^{x^2})}{x^2}.$$
**③ 凑导数定义。** 因 $e^{x^2}-1\sim x^2$ 且 $f(1)=0$，
$$\frac12\lim_{x\to0}\frac{f(1+e^{x^2}-1)-f(1)}{e^{x^2}-1}=\frac12f'(1)=\frac12.$$
比值为非零非 1 的常数 $\frac12$，故两无穷小同阶而非等价，选 (D)。
【思路】由增量关系读出 $f'(1)=1$，再用洛必达与导数定义算出比值 $\frac12$，判定同阶非等价。
【易错】题干积分上限为 $e^{x^2}$、分母为 $\ln(1+x^4)$（低清扫描极易误读为 $e^x$、$\ln(1+x^2)$），上限求导会多出因子 $2x$；常把「同阶但不等价」误选为「等价无穷小」。
===Q3===
【答案】D
【解】
**① 铅直渐近线。** 曲线 $y=\frac{x^3+1}{x^2-1}+e^{\frac1x}\arctan x$。
$$\lim_{x\to1}\left(\frac{x^3+1}{x^2-1}+e^{\frac1x}\arctan x\right)=\infty,$$
故 $x=1$ 为一条铅直渐近线；
$$\lim_{x\to-1}\left(\frac{x^3+1}{x^2-1}+e^{\frac1x}\arctan x\right)=\lim_{x\to-1}\left(\frac{x^2-x+1}{x-1}+e^{\frac1x}\arctan x\right)=-\frac32-\frac{\pi}{4e},$$
故 $x=-1$ 不是铅直渐近线；又 $\lim\limits_{x\to0^+}\frac{x^3+1}{x^2-1}=-1$，且
$$\lim_{x\to0^+}e^{\frac1x}\arctan x=\lim_{x\to0^+}\frac{e^{\frac1x}}{\frac1x}=+\infty,$$
所以 $\lim\limits_{x\to0^+}y=+\infty$，故 $x=0$ 为一条铅直渐近线。
**② 水平渐近线。** $\lim\limits_{x\to-\infty}e^{\frac1x}\arctan x=-\frac\pi2$，$\lim\limits_{x\to+\infty}e^{\frac1x}\arctan x=\frac\pi2$，而 $\frac{x^3+1}{x^2-1}\to\mp\infty$，两端 $y\to\mp\infty$，故无水平渐近线。
**③ 斜渐近线。** 用 $\frac{x^3+1}{x^2-1}-x=\frac1{x-1}$：
$$k_1=\lim_{x\to+\infty}\frac yx=\lim_{x\to+\infty}\left(\frac{x^3+1}{x(x^2-1)}+\frac1x e^{\frac1x}\arctan x\right)=1,\quad b_1=\lim_{x\to+\infty}(y-x)=\lim_{x\to+\infty}\left(\frac1{x-1}+e^{\frac1x}\arctan x\right)=\frac\pi2,$$
得 $y=x+\frac\pi2$；同理 $k_2=1,\ b_2=-\frac\pi2$，得 $y=x-\frac\pi2$。
**④ 结论。** 共 2 条铅直、2 条斜渐近线，合计 4 条，选 (D)。
【思路】按铅直、水平、斜三类逐一用极限排查，特别注意 $x\to0^+$ 时 $e^{1/x}\arctan x$ 发散。
【易错】$x=-1$ 处分子分母含公因子 $(x+1)$ 可约分，不能判为渐近线；$\arctan x$ 在 $\pm\infty$ 分别趋于 $\pm\frac\pi2$，导致两条不同的斜渐近线。
===Q4===
【答案】D
【解】
**① 构造函数并判单调。** 令 $f(x)=\frac{x}{\ln(1+x)}\ (0<x<1)$，则
$$f'(x)=\frac{\ln(1+x)-\frac{x}{1+x}}{\ln^2(1+x)}>0$$
（因 $0<x<1$ 时 $\ln(1+x)>\frac{x}{1+x}$），故 $f$ 单调递增。
**② 比较 $I_1$ 与 $I_3$。** 由 $0<x<1$ 时 $x>x^2$ 及 $f$ 递增得 $f(x)>f(x^2)$，即
$$\frac{x}{\ln(1+x)}>\frac{x^2}{\ln(1+x^2)}.$$
**③ 比较 $I_2$ 与 $I_1$。** 由 $\ln(1+x)<x$ 得 $\frac{x}{\ln(1+x)}>1$，从而 $\frac{x^2}{\ln^2(1+x)}>\frac{x}{\ln(1+x)}$。
**④ 结论。** 在 $(0,1)$ 上
$$\frac{x^2}{\ln^2(1+x)}>\frac{x}{\ln(1+x)}>\frac{x^2}{\ln(1+x^2)},$$
由定积分保序性得 $I_3<I_1<I_2$，选 (D)。（其中 $I_1=\int_0^1\frac{x}{\ln(1+x)}dx,\ I_2=\int_0^1\frac{x^2}{\ln^2(1+x)}dx,\ I_3=\int_0^1\frac{x^2}{\ln(1+x^2)}dx$。）
【思路】把三个被积函数统一为 $f(x)=\frac{x}{\ln(1+x)}$ 在 $x$ 与 $x^2$ 处的取值，用单调性一次比较。
【易错】$I_3$ 的分母是 $\ln(1+x^2)$ 而非 $\ln^2(1+x)$；比较必须限制 $0<x<1$ 才有 $x>x^2$。
===Q5===
【答案】C
【解】
**① 质心公式。** 摆线 $\begin{cases} x=t-\sin t,\\ y=1-\cos t, \end{cases}\ (0\le t\le2\pi)$ 的质心纵坐标 $\bar y=\dfrac{\int_L y\,ds}{\int_L ds}$。
**② 算弧长。**
$$\int_L ds=\int_0^{2\pi}\sqrt{x'^2(t)+y'^2(t)}\,dt=\int_0^{2\pi}\sqrt{(1-\cos t)^2+\sin^2t}\,dt=\int_0^{2\pi}\sqrt{2-2\cos t}\,dt=2\int_0^{2\pi}\left|\sin\frac t2\right|dt=8.$$
**③ 算分子。**
$$\int_L y\,ds=\int_0^{2\pi}(1-\cos t)\cdot2\left|\sin\frac t2\right|dt=4\int_0^{2\pi}\sin^3\frac t2\,dt=8\int_0^{\pi}\sin^3x\,dx=16\int_0^{\frac\pi2}\sin^3x\,dx=\frac{32}{3}.$$
**④ 结果。** $\bar y=\dfrac{32/3}{8}=\dfrac43$，选 (C)。
【思路】摆线一拱的质心用第一类曲线积分 $\bar y=\int_L y\,ds\big/\int_L ds$ 计算。
【易错】$\sqrt{2-2\cos t}=2\left|\sin\frac t2\right|$ 在 $[0,2\pi]$ 上非负可直接去绝对值；点火公式 $\int_0^{\pi/2}\sin^3x\,dx=\frac23$ 不要记错。
===Q6===
【答案】B
【解】
**① 写出主部。** 由 $\lim\limits_{\substack{x\to0\\y\to0}}\frac{f(x,y)}{(x^2+y^2)^a}=1$ 得 $f(0,0)=0$ 且
$$f(x,y)=(x^2+y^2)^a+o\!\left((x^2+y^2)^a\right).$$
**② 由 $f'_x(0,0)$ 存在定范围。** 取 $y=0$ 得 $f(x,0)=|x|^{2a}+o(|x|^{2a})$，于是
$$f'_x(0,0)=\lim_{x\to0}\frac{f(x,0)-f(0,0)}x=\lim_{x\to0}\frac{|x|^{2a}+o(|x|^{2a})}{x}$$
存在必须 $2a>1$，即 $a>\frac12$。
**③ 对 $y$ 同理。** $f'_y(0,0)$ 存在同样要求 $2a>1$，即 $a>\frac12$，故选 (B)。
【思路】把偏导数存在转化为 $\frac{|x|^{2a}}{x}$ 在 $x\to0$ 极限存在，从而要求 $2a>1$。
【易错】$a=\frac12$ 时 $\frac{|x|}{x}$ 左右极限为 $\pm1$ 不存在，必须取严格不等号；$|x|^{2a}$ 的绝对值不能丢。
===Q7===
【答案】D
【解】
**① 化为二重积分。**
$$\lim_{n\to\infty}\sum_{i=1}^{2n}\sum_{j=1}^{2n-i}\frac{|i-j|}{n^3}=\lim_{n\to\infty}\sum_{i=1}^{2n}\sum_{j=1}^{2n-i}\left|\frac in-\frac jn\right|\cdot\frac1{n^2}=\int_0^2dx\int_0^{2-x}|x-y|\,dy.$$
**② 定区域。** 令 $\frac in=x,\ \frac jn=y$；由 $1\le i\le2n,\ 1\le j\le2n-i$ 得 $\frac1n\le x\le2,\ \frac1n\le y\le2-\frac in=2-x$，取 $n\to\infty$ 得 $0\le x\le2,\ 0\le y\le2-x$（由 $x=0,\ y=0,\ y=2-x$ 围成的三角形）。
**③ 用轮换对称性去绝对值。** 以 $y=x$ 分域，取 $x\ge y$ 的一半再乘 2：
$$I=2\int_0^1dy\int_y^{2-y}(x-y)\,dx=4\int_0^1(1-y)^2dy=\frac43,$$
选 (D)。
【思路】先把双重和式写成二重积分，再用区域关于 $y=x$ 的对称性把 $|x-y|$ 化为 $(x-y)$ 的两倍。
【易错】求和上限是 $j\le2n-i$（三角形区域），不是 $j\le n$；被积函数含绝对值，必须按 $y=x$ 拆分区域。
===Q8===
【答案】A
【解】
**① 由解的包含关系得秩。** $Ax=0$ 的解都是 $Bx=0$ 的解，即 $N(A)\subseteq N(B)$，故 $r(A)=r\begin{pmatrix}A\\B\end{pmatrix}$。
**② 加条件。** 若 $A$ 的行向量可由 $B$ 的行向量表示，则 $r(B)=r\begin{pmatrix}A\\B\end{pmatrix}$。
**③ 结论。** 于是 $r(A)=r(B)=r\begin{pmatrix}A\\B\end{pmatrix}$，两方程组解空间维数相同且已有包含关系，故 $Ax=0$ 与 $Bx=0$ 同解，选 (A)。
【思路】用解空间包含关系与堆叠矩阵的秩 $r\begin{pmatrix}A\\B\end{pmatrix}$ 搭桥，行向量可表出时推出 $r(A)=r(B)$。
【易错】「行向量」与「列向量」可表出对应的秩结论不同；四个选项中只有 (A) 能保证 $r(A)=r(B)$。
===Q9===
【答案】C
【解】
**① 特征多项式。** 对 $A=\begin{pmatrix}1&a\\b&1\end{pmatrix},\ B=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$，
$$|A-\lambda E|=\begin{vmatrix}1-\lambda&a\\b&1-\lambda\end{vmatrix}=\lambda^2-2\lambda+1-ab,\quad \Delta=4-4(1-ab)=4ab.$$
**② 判相似对角化。** 若 $ab>0$ 则 $\Delta>0$，$A$ 有两个不同特征值，故相似于对角阵，命题 ② 正确；$ab<0$ 时 $\Delta<0$ 无实特征值，① 错。
**③ 判合同。** 当 $a=b$ 时 $|A-\lambda E|=\lambda^2-2\lambda+1-a^2$，$\lambda_{1,2}=1\pm a$；当 $a=b>1$ 时 $A$ 与 $B$ 的特征值均为一正一负，且都是实对称阵，正负惯性指数相同，故 $A$ 与 $B$ 合同，命题 ③ 正确。
**④ 结论。** ②③ 正确，选 (C)。
【思路】相似对角化看判别式 $\Delta=4ab$，合同看实对称阵的正负惯性指数（特征值符号）。
【易错】原册「当 $a=b$ 时」的行列式左下角仍印作 $b$，应改为 $a$（排印疏漏，不影响 $\lambda_{1,2}=1\pm a$）；相似与合同是两种不同等价关系，不可混用。
===Q10===
【答案】D
【解】
**① 翻译条件。** $\alpha$ 组不能由 $\beta$ 组表出、而 $\beta$ 组可由 $\alpha$ 组表出，等价于
$$r(\alpha_1,\alpha_2,\alpha_3\mid\beta_1,\beta_2,\beta_3)=r(\alpha_1,\alpha_2,\alpha_3)\ne r(\beta_1,\beta_2,\beta_3).$$
**② 行变换。** 对增广矩阵作 $r_2-2r_1,\ r_3+r_1,\ r_4-3r_1$，再作 $\frac12r_4,\ r_4-r_2$，得末行
$$\begin{pmatrix}0&0&0&\mid&4-a&4-a&0\end{pmatrix},$$
故由 $r(\alpha_1,\alpha_2,\alpha_3\mid\beta_1,\beta_2,\beta_3)=r(\alpha_1,\alpha_2,\alpha_3)$ 知 $4-a=0$，即 $a=4$。
**③ 验证。** 当 $a=4$ 时该矩阵经 $r_3-6r_2$ 化为
$$\begin{pmatrix}1&2&-1&\mid&1&3&0\\0&1&2&\mid&2&1&1\\0&0&-10&\mid&0&0&0\\0&0&0&\mid&0&0&0\end{pmatrix},$$
有 $r(\alpha_1,\alpha_2,\alpha_3\mid\beta_1,\beta_2,\beta_3)=r(\alpha_1,\alpha_2,\alpha_3)=3$，$r(\beta_1,\beta_2,\beta_3)=2$，满足题意，故选 (D)。
【思路】把「可／不可线性表出」翻译成秩的等式与不等式，再用初等行变换定出参数 $a$。
【易错】必须回代 $a=4$ 验证 $\beta$ 组秩确实更小（否则只是必要条件）；三个向量组均为 4 维列向量，增广矩阵是 4 行 6 列。
===Q11===
【答案】$\frac{\pi}{2}$
【解】
**① 积分中值定理。**
$$\lim_{n\to\infty}\int_{n^2}^{n^2+n}\frac{\arctan x}{\sqrt x}\,dx=\lim_{n\to\infty}\frac{\arctan\xi}{\sqrt\xi}\cdot n=\lim_{n\to\infty}\arctan\xi\cdot\lim_{n\to\infty}\frac n{\sqrt\xi}=\frac\pi2\lim_{n\to\infty}\frac n{\sqrt\xi},$$
其中 $n^2\le\xi\le n^2+n$，区间长度为 $n$，且 $\xi\to+\infty$ 故 $\arctan\xi\to\frac\pi2$。
**② 夹逼。**
$$\frac n{\sqrt{n^2+n}}\le\frac n{\sqrt\xi}\le\frac n{\sqrt{n^2}},\quad \lim_{n\to\infty}\frac n{\sqrt{n^2+n}}=\lim_{n\to\infty}\frac n{\sqrt{n^2}}=1,$$
故 $\lim\limits_{n\to\infty}\frac n{\sqrt\xi}=1$。
**③ 结论。**
$$\lim_{n\to\infty}\int_{n^2}^{n^2+n}\frac{\arctan x}{\sqrt x}\,dx=\frac\pi2.$$
【思路】用积分中值定理把变限积分写成 $\frac{\arctan\xi}{\sqrt\xi}\cdot n$，再夹逼得 $\frac n{\sqrt\xi}\to1$。
【易错】积分上下限是 $[n^2,n^2+n]$（低清扫描极易误读为 $[n,n^2]$，那样积分发散），区间长度为 $n$ 而非 $n^2-n$；本题不能先算原函数。
===Q12===
【答案】$\left(\dfrac{1}{2^{2026}}-2\right)\cdot2025!$
【解】
**① 换元后求导。** $f(x)=\int_1^x\ln(t+x)\,dt\xlongequal{u=t+x}\int_{1+x}^{2x}\ln u\,du$，故
$$f'(x)=2\ln(2x)-\ln(1+x)=2\ln2+2\ln x-\ln(1+x),\quad f''(x)=\frac2x-\frac1{1+x}.$$
**② 高阶导通项。**
$$f^{(n+2)}(x)=\left[f''(x)\right]^{(n)}=\left(\frac2x-\frac1{1+x}\right)^{(n)}=(-1)^n n!\left[\frac2{x^{n+1}}-\frac1{(1+x)^{n+1}}\right].$$
**③ 代入 $n=2025,\ x=1$。**
$$f^{(2027)}(1)=(-1)^{2025}2025!\left[2-\frac1{2^{2026}}\right]=\left(\frac1{2^{2026}}-2\right)\cdot2025!.$$
【思路】先换元把 $f$ 写成可求导的形式，求两次导后套 $\left(\frac1x\right)^{(n)}$ 公式得高阶导通项。
【易错】题目求的是 $f^{(2027)}(1)$（扫描小字易误看作 2025 阶），故通项中取 $n=2025$；$(-1)^{2025}=-1$ 决定整体符号，别漏。
===Q13===
【答案】$1$
【解】
**① 对 $x$ 求偏导。** 隐函数方程为 $x-az=\varphi(y-bz)$，其中 $\varphi$ 可导且 $a-b\varphi'\ne0$。两边对 $x$ 求偏导：
$$1-a\frac{\partial z}{\partial x}=\varphi'\cdot\left(-b\frac{\partial z}{\partial x}\right)\Rightarrow\frac{\partial z}{\partial x}=\frac1{a-b\varphi'}.$$
**② 对 $y$ 求偏导。**
$$-a\frac{\partial z}{\partial y}=\varphi'\cdot\left(1-b\frac{\partial z}{\partial y}\right)\Rightarrow\frac{\partial z}{\partial y}=-\frac{\varphi'}{a-b\varphi'}.$$
**③ 线性组合。**
$$a\frac{\partial z}{\partial x}+b\frac{\partial z}{\partial y}=\frac{a-b\varphi'}{a-b\varphi'}=1.$$
【思路】方程两边分别对 $x,y$ 求偏导解出两个偏导，再按待求式组合。
【易错】括号内是 $\varphi(y-bz)$（含 $bz$，扫描易误读为 $bx$）；条件 $a-b\varphi'\ne0$ 正是公分母非零的保证，$\varphi'$ 不能当常数处理。
===Q14===
【答案】$\dfrac12\left(\dfrac\pi2-1\right)$
【解】
**① 交换积分次序。** 区域为 $0\le y\le\sqrt{\left(\frac\pi2\right)^3}$，$\sqrt[3]{y}\le x\le\sqrt{\frac\pi2}$，等价于 $0\le x\le\sqrt{\frac\pi2},\ 0\le y\le x^3$：
$$\int_0^{\sqrt{\left(\frac\pi2\right)^3}}dy\int_{\sqrt[3]{y}}^{\sqrt{\frac\pi2}}\cos x^2\,dx=\int_0^{\sqrt{\frac\pi2}}\cos x^2\,dx\int_0^{x^3}dy=\int_0^{\sqrt{\frac\pi2}}x^3\cos x^2\,dx.$$
**② 换元 $t=x^2$。**
$$\int_0^{\sqrt{\frac\pi2}}x^3\cos x^2\,dx=\frac12\int_0^{\frac\pi2}t\cos t\,dt=\frac12\left(\frac\pi2-1\right).$$
【思路】先交换积分次序消去 $dy$ 得到 $x^3\cos x^2$，再用 $t=x^2$ 把 $\cos x^2$ 化为 $\cos t$。
【易错】内层下限是 $\sqrt[3]{y}$，交换后为 $y\le x^3$；外层上限 $\sqrt{(\pi/2)^3}$ 保证换元 $t=x^2$ 后上限恰为 $\frac\pi2$。
===Q15===
【答案】$f(x)=2e^{-x}+\dfrac34e^{2x}-\dfrac12x^2+\dfrac12x-\dfrac34$
【解】
**① 拆积分并两次求导。** 题设 $f(x)=2+\int_0^x(x-t)\left[f'(t)+2f(t)+t^2\right]dt$，改写为
$$f(x)=2+x\int_0^x\left[f'(t)+2f(t)+t^2\right]dt-\int_0^xt\left[f'(t)+2f(t)+t^2\right]dt,$$
两边对 $x$ 求导得 $f'(x)=\int_0^x\left[f'(t)+2f(t)+t^2\right]dt$，再求导得
$$f''(x)-f'(x)-2f(x)=x^2.$$
**② 齐次通解。** 特征方程 $r^2-r-2=0$，根 $r_1=-1,\ r_2=2$，齐次通解为 $C_1e^{-x}+C_2e^{2x}$。
**③ 特解与通解。** 设特解 $y^*=ax^2+bx+c$ 代入得 $a=-\frac12,\ b=\frac12,\ c=-\frac34$，故
$$f(x)=C_1e^{-x}+C_2e^{2x}-\frac12x^2+\frac12x-\frac34.$$
**④ 定常数。** 由 $f(0)=2,\ f'(0)=0$ 得 $C_1=2,\ C_2=\frac34$，即得答案式。
【思路】把含 $(x-t)$ 的积分方程两次求导化为二阶常系数非齐次微分方程，用特征根法加初始条件定解。
【易错】积分括号内是 $f'(t)$ 而非 $f''(t)$（低清扫描易混，若写成 $f''$ 会得到矛盾式）；初始条件 $f'(0)=0$ 需由原方程求导后令 $x=0$ 得到。
===Q16===
【答案】$-2$
【解】
**① 行列式降次。** 对
$$f(x)=\begin{vmatrix}x+1&x-1&x+2&x-2\\x&2x&3x+2&4x-1\\x-1&2x+1&3x-1&4x+2\\x&2x+1&3x&4x+1\end{vmatrix}$$
作 $r_3-r_2,\ r_4-r_2$，再作 $c_2-c_1,\ c_3-c_1,\ c_4-c_1$，得
$$f(x)=\begin{vmatrix}x+1&-2&1&-3\\x&x&2x+2&3x-1\\-1&2&-2&4\\0&1&-2&2\end{vmatrix}.$$
**② 化为二阶。** 再作 $c_3+2c_2,\ c_4-2c_2$ 后按第 4 行展开为三阶式，并作 $c_2+2c_1$：
$$f(x)=\begin{vmatrix}x+1&2x-1&1\\x&6x+2&x-1\\-1&0&0\end{vmatrix}=-\begin{vmatrix}2x-1&1\\6x+2&x-1\end{vmatrix}=-2x^2+9x+1.$$
**③ 取系数。** $x^2$ 的系数为 $-2$。
【思路】用行、列初等变换把四阶行列式降到二阶，展开成多项式后读出 $x^2$ 系数。
【易错】题目求的是 $x^2$ 的系数（低清扫描易误读为 $x^3$）；按 $(-1,0,0)$ 行展开时前面的负号别丢，即 $-\begin{vmatrix}2x-1&1\\6x+2&x-1\end{vmatrix}$。
===Q17===
【答案】$\dfrac{\tan x}{\sqrt{\cos x}}+C$
【解】
**① 拆项。**
$$\int\frac{1+\frac12\sin^2x}{\cos^{\frac52}x}\,dx=\int\left(\frac1{\cos^2x}\cdot\frac1{\sqrt{\cos x}}+\frac{\sin^2x}{2\cos^2x\sqrt{\cos x}}\right)dx.$$
**② 关键导数。**
$$\left(\frac1{\sqrt{\cos x}}\right)'=\frac{\sin x}{2\cos x\sqrt{\cos x}}.$$
**③ 凑乘积求导。**
$$\text{原式}=\int\left[\sec^2x\cdot\frac1{\sqrt{\cos x}}+\frac{\sin x}{\cos x}\left(\frac1{\sqrt{\cos x}}\right)'\right]dx=\int\left[(\tan x)'\cdot\frac1{\sqrt{\cos x}}+\tan x\left(\frac1{\sqrt{\cos x}}\right)'\right]dx$$
$$=\int\left(\frac{\tan x}{\sqrt{\cos x}}\right)'dx=\frac{\tan x}{\sqrt{\cos x}}+C.$$
【思路】把被积函数凑成 $(\tan x)'\cdot\frac1{\sqrt{\cos x}}+\tan x\cdot\left(\frac1{\sqrt{\cos x}}\right)'$，即乘积的导数。
【易错】分母是 $\cos^{\frac52}x$（扫描易误读为 $\cos^{\frac32}x$）；$\sec^2x=(\tan x)'$ 与 $\left(\frac1{\sqrt{\cos x}}\right)'$ 中的系数 $\frac12$ 必须对齐，最后勿漏 $+C$。
===Q18===
【答案】（I）$y''\left[y^2-x^2(y')^2\right]=0$；（II）$f(x)=\dfrac{k}{x}\ (k>0\text{ 为常数},\ x>0)$
【解】
**（I）由面积条件导出微分方程。** 设 $x>0$ 时 $f(x)$ 二阶可导，$f(x)>0,\ f'(x)<0$，曲线 $y=f(x)$ 在 $(x,y)$ 处切线为 $Y-y=y'(X-x)$，与两坐标轴交点为 $\left(x-\frac{y}{y'},0\right)$、$(0,y-xy')$，故
$$\frac12\left|x-\frac{y}{y'}\right|\cdot|y-xy'|=m\quad(m\text{ 为常数}),$$
即 $2xy-x^2y'-\dfrac{y^2}{y'}=\pm2m$。两边对 $x$ 求导：
$$2y+2xy'-2xy'-x^2y''-\frac1{(y')^2}\left[2y(y')^2-y^2y''\right]=0,$$
整理得 $\dfrac{y''}{(y')^2}\left[y^2-x^2(y')^2\right]=0$，即 $y''\left[y^2-x^2(y')^2\right]=0$。
**（II）解出 $f(x)$。** 由 $y''=f''(x)\ne0$ 得 $y^2-x^2(y')^2=0$，即 $(y-xy')(y+xy')=0$。因 $y=f(x)>0,\ x>0,\ y'=f'(x)<0$，故 $y-xy'>0$，只能 $y+xy'=0$，即
$$\frac{dy}{y}=-\frac{dx}{x}.$$
两边积分得 $\ln|y|=-\ln|x|+C$；由 $x>0,\ y>0$ 有 $|y|=y,\ |x|=x$，故 $xy=k$，即 $y=\frac{k}{x}$，其中 $k=e^C>0$，于是
$$f(x)=\frac{k}{x}\quad(k>0\text{ 为常数},\ x>0).$$
【思路】(I) 把「切线与坐标轴围成面积为常数」写成方程并对 $x$ 求导化简；(II) 由 $f''\ne0$ 舍去一支，解可分离变量方程。
【易错】面积式含绝对值，去掉后右端是 $\pm2m$，求导后常数消失；判断符号须用 $y>0,\ x>0,\ y'<0$ 排除 $y-xy'=0$ 这一支，否则会错得 $y=Cx$。
===Q19===
【答案】$d_{\min}=\sqrt{10+3\sqrt[3]{9}+9\sqrt[3]{3}}$（此时 $a=1+\sqrt[3]{9},\ b=3+\sqrt[3]{3}$）
【解】
**① 求切线与约束。** 曲线 $C:\frac{x^2}{a^2}+\frac{y^2}{b^2}=2$ 在 $P(a,b)$ 处的斜率
$$\left.\frac{dy}{dx}\right|_P=-\frac{b^2x}{a^2y}\bigg|_{(a,b)}=-\frac ba,$$
切线 $Y-b=-\frac ba(X-a)$，即 $\frac1aX+\frac1bY=2$。代入 $(2,6)$ 得 $\frac1a+\frac3b=1$。所求为 $d=|OP|=\sqrt{a^2+b^2}$ 在该条件下的最小值。
**② 拉格朗日乘数法。** 构造
$$L(a,b,\lambda)=a^2+b^2+\lambda\left(\frac1a+\frac3b-1\right),$$
$$\begin{cases}L'_a=2a-\dfrac{\lambda}{a^2}=0,\\[4pt]L'_b=2b-\dfrac{3\lambda}{b^2}=0,\\[4pt]\dfrac1a+\dfrac3b-1=0.\end{cases}$$
由前两式消去 $\lambda$ 得 $b^3=3a^3$，结合 $a>0,b>0$ 解得 $a=1+\sqrt[3]{9},\ b=3+\sqrt[3]{3}$；驻点唯一，故为最小值点。
**③ 结果。**
$$d=\sqrt{\left(1+\sqrt[3]{9}\right)^2+\left(3+\sqrt[3]{3}\right)^2}=\sqrt{10+3\sqrt[3]{9}+9\sqrt[3]{3}}.$$
【思路】由切线过定点得约束 $\frac1a+\frac3b=1$，再用拉格朗日乘数法求 $\sqrt{a^2+b^2}$ 的条件极值。
【易错】$b=3+\sqrt[3]{3}$ 而非 $3+\sqrt[3]{9}$（扫描小字易混）；化简根式要用 $\sqrt[3]{81}=3\sqrt[3]{3}$，两个立方根不能合并。
===Q20===
【答案】$I=1-\dfrac\pi2+\ln2$
【解】
**① 用对称性化简。** 设 $D$ 为 $x^2+y^2=x$ 所围区域，$D_1$ 为其中 $y>0$ 的部分。$D$ 关于 $x$ 轴对称，$\frac{2xy}{1+x^2+y^2}$ 关于 $y$ 为奇函数，故
$$\iint_D\frac{2xy}{1+x^2+y^2}\,d\sigma=0,\qquad \iint_D\frac{|y|}{1+x^2+y^2}\,d\sigma=2\iint_{D_1}\frac{y}{1+x^2+y^2}\,d\sigma.$$
**② 化极坐标。** 边界 $r=\cos\theta$，上半部分 $0\le\theta\le\frac\pi2,\ 0\le r\le\cos\theta$：
$$I=2\int_0^{\frac\pi2}d\theta\int_0^{\cos\theta}\frac{r\sin\theta}{1+r^2}\,r\,dr=2\int_0^{\frac\pi2}\sin\theta\left(\cos\theta-\arctan(\cos\theta)\right)d\theta.$$
**③ 分别积分。**
$$\int_0^{\frac\pi2}\sin\theta\cos\theta\,d\theta=\left.\frac12\sin^2\theta\right|_0^{\frac\pi2}=\frac12,$$
$$\int_0^{\frac\pi2}\sin\theta\arctan(\cos\theta)\,d\theta=-\int_0^{\frac\pi2}\arctan(\cos\theta)\,d(\cos\theta)\xlongequal{\cos\theta=t}\int_0^1\arctan t\,dt$$
$$=\left.t\arctan t\right|_0^1-\int_0^1\frac{t}{1+t^2}\,dt=\frac\pi4-\frac12\ln2.$$
**④ 合并。** $I=2\left[\frac12-\left(\frac\pi4-\frac12\ln2\right)\right]=1-\frac\pi2+\ln2$。
【思路】对称性先消去奇函数项，极坐标化为一重积分，最后分部积分处理 $\arctan t$。
【易错】$\int_0^{\cos\theta}\frac{r^2}{1+r^2}dr=\cos\theta-\arctan(\cos\theta)$，别漏 $\arctan$ 项；$\int_0^1\arctan t\,dt=\frac\pi4-\frac12\ln2$，整体还要乘 2 并与 $\frac12$ 相减。
===Q21===
【答案】（I）存在 $x_1,x_2\in(0,1),\ x_1\ne x_2$ 使 $\frac1{f(x_1)}+\frac1{f(x_2)}=2$；（II）存在 $\xi\in(0,1)$ 使 $2\int_0^\xi f(x)\,dx=f(\xi)+2\xi-1$
【解】
**（I）介值定理 + 拉格朗日中值定理。** 设 $f$ 在 $[0,1]$ 连续，$f(0)=0,\ \int_0^1f(x)dx=1$；令 $F(x)=\int_0^xf(t)\,dt$，则 $F(0)=0,\ F(1)=1,\ F'(x)=f(x)$。由连续函数介值定理，存在 $\eta\in(0,1)$ 使 $F(\eta)=\frac12$。在 $[0,\eta]$、$[\eta,1]$ 上分别用拉格朗日中值定理：
$$F'(x_1)=f(x_1)=\frac{F(\eta)-F(0)}{\eta-0}=\frac{1/2}{\eta},\quad x_1\in(0,\eta),$$
$$F'(x_2)=f(x_2)=\frac{F(1)-F(\eta)}{1-\eta}=\frac{1/2}{1-\eta},\quad x_2\in(\eta,1).$$
于是
$$\frac1{f(x_1)}+\frac1{f(x_2)}=\frac{\eta}{1/2}+\frac{1-\eta}{1/2}=2.$$
**（II）构造辅助函数用罗尔定理。** 令 $\varphi(x)=e^{-2x}\left[F(x)-x\right]$，则
$$\varphi'(x)=e^{-2x}\left[-2F(x)+2x+F'(x)-1\right].$$
又 $\varphi(0)=0$，且
$$\varphi(1)=e^{-2}\left[F(1)-1\right]=e^{-2}\left[\int_0^1f(t)\,dt-1\right]=0,$$
由罗尔定理存在 $\xi\in(0,1)$ 使 $\varphi'(\xi)=0$。因 $e^{-2\xi}\ne0$，得 $-2F(\xi)+2\xi+F'(\xi)-1=0$；代入 $F'(\xi)=f(\xi)$ 即
$$2\int_0^\xi f(x)\,dx=f(\xi)+2\xi-1.$$
【思路】(I) 用 $F(\eta)=\frac12$ 把区间二分、各用一次中值定理；(II) 按待证等式配出 $e^{-2x}[F(x)-x]$ 再用罗尔定理。
【易错】辅助函数的指数因子 $e^{-2x}$ 来自把 $-2F+2x+F'-1=0$ 凑成 $\varphi'=0$；$F(1)=\int_0^1f(x)dx=1$ 是 $\varphi(1)=0$ 的关键，不能漏用 $\int_0^1f=1$。
===Q22===
【答案】（I）$A=k\alpha\alpha^T$（$\alpha\ne0,\ k\ne0$）；（II）$A=\begin{pmatrix}1&2&2\\2&4&4\\2&4&4\end{pmatrix}$；（III）$P=\begin{pmatrix}1&-2&-2\\2&1&0\\2&0&1\end{pmatrix}$，$P^{-1}(A+E)^*P=\begin{pmatrix}1&0&0\\0&10&0\\0&0&10\end{pmatrix}$
【解】
**（I）谱分解。** $A$ 为三阶实对称阵且 $r(A)=1$，故可对角化且特征值为 $\lambda_1\ne0,\ \lambda_2=\lambda_3=0$。取对应的两两正交单位特征向量 $\xi_1,\xi_2,\xi_3$，令 $Q=(\xi_1,\xi_2,\xi_3)$ 为正交阵，则
$$A=Q\begin{pmatrix}\lambda_1&0&0\\0&0&0\\0&0&0\end{pmatrix}Q^T=(\xi_1,\xi_2,\xi_3)\begin{pmatrix}\lambda_1&0&0\\0&0&0\\0&0&0\end{pmatrix}\begin{pmatrix}\xi_1^T\\\xi_2^T\\\xi_3^T\end{pmatrix}=\lambda_1\xi_1\xi_1^T.$$
取 $k=\lambda_1,\ \alpha=\xi_1$，即得 $A=k\alpha\alpha^T$。
**（II）求 $A$。** $\lambda=9$ 对应特征向量 $\beta_1=(1,2,2)^T$，单位化得 $\xi_1=\frac1{\|\beta_1\|}\beta_1=\frac13(1,2,2)^T$，由 (I)
$$A=9\cdot\frac13\begin{pmatrix}1\\2\\2\end{pmatrix}\cdot\frac13(1,2,2)=\begin{pmatrix}1&2&2\\2&4&4\\2&4&4\end{pmatrix}.$$
**（III）求 $P$ 与对角阵。** 设 $\beta=(x_1,x_2,x_3)^T$ 为 $\lambda_2=\lambda_3=0$ 对应的特征向量，由实对称阵不同特征值的特征向量正交得 $x_1+2x_2+2x_3=0$，取基础解系
$$\beta_2=(-2,1,0)^T,\quad\beta_3=(-2,0,1)^T,\quad P=(\beta_1,\beta_2,\beta_3)=\begin{pmatrix}1&-2&-2\\2&1&0\\2&0&1\end{pmatrix}.$$
$A+E$ 的特征值为 $\lambda_1'=10,\ \lambda_2'=\lambda_3'=1$，故伴随矩阵 $(A+E)^*$ 的特征值为 $\frac{\det(A+E)}{\lambda_i'}=1,10,10$，于是
$$P^{-1}(A+E)^*P=\begin{pmatrix}1&0&0\\0&10&0\\0&0&10\end{pmatrix}.$$
【思路】用秩 1 实对称阵的谱分解写出 $A=k\alpha\alpha^T$，借特征向量正交性构造 $P$，最后由伴随矩阵特征值 $\det(A+E)/\lambda_i'$ 得对角阵。
【易错】$(A+E)^*$ 是 $A+E$ 的伴随矩阵（不是 $A+E$ 本身），其特征值须用 $\det(A+E)/\lambda_i'$；对角元顺序要与 $P$ 的列 $\beta_1,\beta_2,\beta_3$ 对应为 $1,10,10$；原册第 (III) 问中的对角矩阵记作 $\Lambda$，勿与矩阵 $A$ 混淆。
