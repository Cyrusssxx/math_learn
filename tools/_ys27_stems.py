# -*- coding: utf-8 -*-
"""27 模拟卷精选题（亚瑟爱数学 2026.11）—— 题干转写表。

来源：E:/Desktop/做题/27模拟卷精选题/【紧凑版题本】…pdf（11 页，第 3 页起是题目）
答案：同目录【答案册】…pdf（45 页），由 _build_ys27.py 合并。

字段：
  no      —— 本库内部序号 1..37（= qid `ys27-<no>`，必须唯一）
  origin  —— 原卷题号（题本上的编号，跨卷重复，只作展示）
  source  —— 题本上的出处标签，如「李艳芳数二卷一-5·凹凸性」
  kind    —— 'choice' | 'blank' | 'calc'
  catId   —— 三级分类叶子 id（见 YS27_CATS）
  stem    —— 题干（mdBlock 语法：$$ 独占行、$ 行内、不支持 - 列表）
  options —— 选择题选项；填空/解答为空数组
"""

STEMS = [
    dict(
        no=1, origin='6', kind='choice', source='ep 数二卷一-6·等价无穷小', catId=50011,
        stem=r"""设当 $x\to 0$ 时，$\alpha(x),\beta(x)$ 为非零无穷小，则下列选项中正确个数为

① 若 $\alpha(x)\sim\beta(x)$，则 $\alpha(x)-\beta(x)=o(\alpha(x))$；

② 若 $\alpha(x)\sim\beta(x)$，则 $\alpha^2(x)-\beta^2(x)=o(\alpha(x))$；

③ 若 $\gamma(x)$ 是 $x\to 0$ 时的无穷小量，则 $\alpha(x)+\gamma(x)\sim\beta(x)+\gamma(x)$；

④ 若 $\alpha(x)=o(\beta(x))$，则对任意的 $x\to 0$ 时的非零无穷小量 $\gamma(x)$，都有 $\alpha(x)\gamma(x)=o(\beta(x)\gamma(x))$。""",
        options=['A. 1.', 'B. 2.', 'C. 3.', 'D. 4.'],
    ),
    dict(
        no=2, origin='5', kind='choice', source='李艳芳数二卷一-5·凹凸性', catId=50021,
        stem=r"""设函数 $f(x)$ 在 $(-\infty,+\infty)$ 内有定义，且对于任意的 $x,y$，都有 $f(x+y)=f(x)f(y)$，已知 $f(0)\neq 0$，$f'(0)=a\neq 0$，则""",
        options=[
            'A. $f(x)$ 单调增加.',
            'B. $f(x)$ 单调减少.',
            'C. $f(x)$ 为凹函数.',
            'D. $f(x)$ 为凸函数.',
        ],
    ),
    dict(
        no=3, origin='6', kind='choice', source='张八数二卷三-6·可导概念判断', catId=50022,
        stem=r"""下列三个命题：

① 设 $f(x)$ 在 $x=x_0$ 处连续，在 $x=x_0$ 的某去心邻域内可导，若 $\lim\limits_{x\to x_0}f'(x)$ 存在，则 $f(x)$ 在 $x=x_0$ 处可导且 $f'(x_0)=\lim\limits_{x\to x_0}f'(x)$；

② 设 $f(x)$ 在 $x=x_0$ 处连续，在 $x=x_0$ 的某去心邻域内可导，若 $\lim\limits_{x\to x_0^+}f'(x)$ 与 $\lim\limits_{x\to x_0^-}f'(x)$ 均存在但不相等，则 $f'(x_0)$ 不存在；

③ 设 $f(x)$ 在 $x=x_0$ 的某邻域内可导，若 $\lim\limits_{x\to x_0^+}f'(x)$ 与 $\lim\limits_{x\to x_0^-}f'(x)$ 均存在，则必有 $\lim\limits_{x\to x_0}f'(x)$ 存在.

所有真命题的序号为""",
        options=['A. ①②.', 'B. ②③.', 'C. ①③.', 'D. ①②③.'],
    ),
    dict(
        no=4, origin='2', kind='choice', source='张八数二卷七-2·微分概念判断', catId=50023,
        stem=r"""若二元函数 $f(x,y)$ 与 $g(x,y)$ 在点 $P_0(x_0,y_0)$ 的某邻域内有定义，$f(x,y)$ 在点 $P_0$ 处可微且 $f(x_0,y_0)=0$，$g(x,y)$ 在点 $P_0$ 处连续但不可微，则对于下列 $4$ 个函数：

$$F_1(x,y)=f(x,y)|f(x,y)|,\quad F_2(x,y)=f(x,y)g(x,y),$$

$$F_3(x,y)=f(x,y)|g(x,y)|,\quad F_4(x,y)=|f(x,y)|g(x,y).$$

说法正确的是""",
        options=[
            'A. 只有 $F_1(x,y)$ 在点 $P_0$ 处可微.',
            'B. 只有 $F_1(x,y)$，$F_2(x,y)$ 在点 $P_0$ 处可微.',
            'C. 只有 $F_1(x,y)$，$F_2(x,y)$，$F_3(x,y)$ 在点 $P_0$ 处可微.',
            'D. $4$ 个函数均在点 $P_0$ 处可微.',
        ],
    ),
    dict(
        no=5, origin='3', kind='choice', source='张八数二卷七-3·凹凸性概念', catId=50024,
        stem=r"""反常积分 ① $\displaystyle\int_0^{+\infty}\frac{|\sin x|}{\sqrt{x^3}}\,\mathrm{d}x$，② $\displaystyle\int_0^{+\infty}\frac{1}{1+\sqrt{x|\sin x|}}\,\mathrm{d}x$ 的敛散性为""",
        options=[
            'A. ①收敛，②收敛.',
            'B. ①收敛，②发散.',
            'C. ①发散，②收敛.',
            'D. ①发散，②发散.',
        ],
    ),
    dict(
        no=6, origin='4', kind='choice', source='ep 数二卷一-4·有界性与导数', catId=50025,
        stem=r"""设函数 $f(x)$ 在区间 $(0,1)$ 上可导，则下列说法中正确的是""",
        options=[
            r'A. 若存在常数 $M>0$，使得 $|f^{\prime}(x)|<\frac{M}{\sqrt{x}}$，则 $f(x)$ 在 $(0,1)$ 上有界.',
            r'B. 若 $f(x)+f^{\prime}(x)$ 在 $(0,1)$ 上无界，则 $f(x)f^{\prime}(x)$ 也在 $(0,1)$ 上无界.',
            r'C. 若 $f(x)$ 在 $(0,1)$ 上有界，则存在常数 $M>0$，使得 $|f^{\prime}(x)|<\frac{M}{\sqrt{x}}$.',
            r'D. 若 $f^{\prime}(x)$ 在 $(0,1)$ 上无界，则 $f(x)$ 也在 $(0,1)$ 上无界.',
        ],
    ),
    dict(
        no=7, origin='3', kind='choice', source='ep 数二卷三-3·微分与增量', catId=50023,
        stem=r"""设函数 $y=f(x)$ 具有二阶导数，$f^{\prime}(x)\le 0$，$f^{\prime\prime}(x)\le 0$，$\Delta x$ 为自变量 $x$ 在 $x_0$ 处的增量，$\Delta y$ 与 $\mathrm{d}y$ 分别是 $f(x)$ 在点 $x_0$ 处的增量与微分，若 $\Delta x<0$，则""",
        options=[
            r'A. $0\le \mathrm{d}y\le \Delta y$.',
            r'B. $0\le \Delta y\le \mathrm{d}y$.',
            r'C. $\Delta y\le \mathrm{d}y\le 0$.',
            r'D. $\mathrm{d}y\le \Delta y\le 0$.',
        ],
    ),
    dict(
        no=8, origin='5', kind='choice', source='ep 数二卷三-5·凹凸性', catId=50021,
        stem=r"""设函数 $f(x)$ 在 $[0,+\infty)$ 上二阶可导，且 $f(0)=0$. 下列命题中，正确的个数为

① 若在 $(0,+\infty)$ 上恒有 $f^{\prime\prime}(x)<0$，则 $\frac{f(x)}{x}$ 在 $(0,+\infty)$ 上单调减少；

② 若 $\frac{f(x)}{x}$ 在 $(0,1]$ 上单调减少，则在 $(0,1]$ 上恒有 $f^{\prime\prime}(x)\le 0$；

③ 若 $\lim\limits_{x\to+\infty}\frac{f(x)}{x}$ 存在，则 $\lim\limits_{x\to+\infty}f^{\prime}(x)$ 存在；

④ 若在 $(0,+\infty)$ 上恒有 $f^{\prime\prime}(x)<0$，且 $\lim\limits_{x\to+\infty}\frac{f(x)}{x}$ 存在，则 $\lim\limits_{x\to+\infty}f^{\prime}(x)$ 存在.""",
        options=['A. 1.', 'B. 2.', 'C. 3.', 'D. 4.'],
    ),
    dict(
        no=9, origin='6', kind='choice', source='小侯七数二卷三-6·导数概念', catId=50022,
        stem=r"""已知 $f(x)$ 在 $x=0$ 的某邻域内有定义，在 $x=0$ 的去心邻域内可导，极限 $\lim\limits_{x\to 0}f^{\prime}(x)$ 存在，下列说法正确的为""",
        options=[
            r'A. 若极限 $\lim\limits_{x\to 0}\frac{f^{\prime}(x)+f(x)}{x}$ 存在，则 $f(x)$ 在 $x=0$ 处可导.',
            r'B. 若 $\int_0^x f(t)\,\mathrm{d}t$ 在 $x=0$ 处可导，则 $f(x)$ 在 $x=0$ 处可导.',
            r'C. 若 $f^{\prime}(0)$ 存在，则 $f^{\prime}(0)$ 不一定等于 $\lim\limits_{x\to 0}f^{\prime}(x)$.',
            r'D. 若 $f^{\prime}(0)$ 存在，则极限 $\lim\limits_{x\to 0}\frac{f(x)-f(0)}{x^{1/3}}=0$.',
        ],
    ),
    dict(
        no=10, origin='4', kind='choice', source='李艳芳数二卷二-4·积分物理应用（仅数二）', catId=50032,
        stem=r"""设动点 $P$ 从原点出发以匀速 $v_0$ 沿 $x$ 轴正向运动，点 $A$ 为 $y$ 轴正半轴上的定点，坐标为 $(0,a)$，记 $\angle APO=\alpha$，$AP$ 的长为 $l$，则 $\alpha$ 关于时间的变化率为（　　）""",
        options=[
            r'A. $\frac{av_0}{l}$',
            r'B. $\frac{l}{av_0}$',
            r'C. $\frac{av_0}{l^2}$',
            r'D. $\frac{l^2}{av_0}$',
        ],
    ),
    dict(
        no=11, origin='3', kind='choice', source='李林数二卷五-3·反函数积分', catId=50031,
        stem=r"""设可导函数 $y=f(x)$ 在 $[a,b]$ 上严格单调递增，$g(y)$ 是 $f(x)$ 的反函数，则

$$\int_a^b f(x)\,\mathrm{d}x+\int_{f(a)}^{f(b)}g(y)\,\mathrm{d}y=(\quad)$$""",
        options=[
            r'A. $f(b)-f(a)$',
            r'B. $bf(b)-af(a)$',
            r'C. $af(b)-bf(a)$',
            r'D. $af(a)-bf(b)$',
        ],
    ),
    dict(
        no=12, origin='10', kind='choice', source='李艳芳数二卷一-10·相似对角化', catId=50041,
        stem=r"""设 $\alpha,\beta$ 为相互正交的 $3$ 维非零列向量，则下列命题中，正确的是（　　）

① $\alpha\beta^{\mathrm{T}}$ 不能相似对角化.

② $\alpha\beta^{\mathrm{T}}$ 能相似对角化.

③ $\alpha\beta^{\mathrm{T}}$ 与 $\alpha\beta^{\mathrm{T}}+\beta\alpha^{\mathrm{T}}$ 没有公共的特征向量.

④ $\alpha\beta^{\mathrm{T}}$ 与 $\alpha\beta^{\mathrm{T}}+\beta\alpha^{\mathrm{T}}$ 有公共的特征向量.""",
        options=['A. ①③.', 'B. ①④.', 'C. ②③.', 'D. ②④.'],
    ),
    dict(
        no=13, origin='10', kind='choice', source='ep 数二卷二-10·矩阵秩的关系', catId=50042,
        stem=r"""设 $A,B,C$ 是三个 $n$ 阶方阵，且 $BA=O$，$A+CB=E$，则下列结论正确的是

① $r(A)+r(B)=n$；　② $r(A)+r(A-E)=n$；　③ $r(B)+r(B-E)=n$；　④ $r\begin{pmatrix}A\\B\end{pmatrix}=n$.""",
        options=['A. ①②④.', 'B. ②③④.', 'C. ①②③.', 'D. ①②③④.'],
    ),
    dict(
        no=14, origin='9', kind='choice', source='小侯七数二卷一-9·矩阵概念', catId=50043,
        stem=r"""已知三阶矩阵 $A,B$ 满足 $AB=O$，其中矩阵 $A=\begin{pmatrix}1&3&-4\\3&a&0\\-4&0&c\end{pmatrix}$，实对称矩阵 $B$ 每行元素之和均为 $3$，则当列向量 $x=(1,-1,2)^{\mathrm{T}}$ 时，二次型 $x^{\mathrm{T}}Bx=$""",
        options=['A. 1', 'B. 2', 'C. 3', 'D. 4'],
    ),
    dict(
        no=15, origin='8', kind='choice', source='小侯七数二卷三-8·矩阵关系与对称性', catId=50042,
        stem=r"""下列说法中，

① 已知矩阵 $E-BA$ 可逆，其中 $A,B$ 均为 $n$ 阶矩阵，则 $E+A(E-BA)^{-1}B$ 的逆矩阵为 $E-AB$；

② 已知 $A$ 为 $n$ 阶反对称矩阵，$B$ 为 $n$ 阶实对称矩阵，且 $A,B$ 乘积可交换，$B+A$ 可逆，则矩阵 $(B-A)(B+A)^{-1}$ 为正交矩阵；

③ 已知 $A,B$ 为 $n$ 阶实对称矩阵，其中矩阵 $A$ 和 $E+AB$ 均可逆，则 $(E+AB)^{-1}A$ 为实对称矩阵；

④ $n$ 阶矩阵 $A,B$ 满足 $AB+A+B=O$，其中可逆矩阵 $A$ 为实对称矩阵，则 $B^{-1}A^2B^{\mathrm{T}}=A^2$.

正确的个数为""",
        options=['A. 1 个.', 'B. 2 个.', 'C. 3 个.', 'D. 4 个.'],
    ),
    dict(
        no=16, origin='8', kind='choice', source='李永乐数二卷三-8·向量组线性相关与无关', catId=50051,
        stem=r"""设 $A$ 是 $n$ 阶可逆矩阵，$\alpha_1,\alpha_2,\cdots,\alpha_s\,(2\le s\le n)$ 都是 $n$ 维非零列向量，则 $\alpha_i^{\mathrm{T}}A^{\mathrm{T}}A\alpha_j=0\ (i,j=1,2,\cdots,s,\ i\neq j)$ 是向量组 $\alpha_1,\alpha_2,\cdots,\alpha_s$ 线性无关的""",
        options=[
            'A. 充要条件.',
            'B. 必要非充分条件.',
            'C. 充分非必要条件.',
            'D. 既不充分也不必要条件.',
        ],
    ),
    dict(
        no=17, origin='8', kind='choice', source='小侯七数二卷四-8·方程组同解与公共解', catId=50052,
        stem=r"""下列说法

① 已知 $n$ 阶方阵 $A,B,C$ 满足 $BC=O$，且 $r(A)<r(C)$，则存在 $n$ 维非零列向量 $\alpha$，使得 $A\alpha=B\alpha$.

② 已知矩阵方程 $AXB=C$ 有解，其中 $A,B,C$ 分别为 $m\times n,\ l\times s,\ m\times s$ 阶矩阵，$X$ 为 $n\times l$ 阶矩阵，若 $r(A)=r(A,C)=n$，$r(B)=r\begin{pmatrix}B\\C\end{pmatrix}=l$，则方程组 $AXB=C$ 有唯一解.

③ 非齐次方程组 $\begin{pmatrix}A&O\\O&B\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}0\\\beta\end{pmatrix}$ 有解的充要条件是 $r(B)>0$，$r(A)=r(A,\beta)$.

④ 非齐次方程组 $Ax=\beta$ 有解的充要条件是向量 $\beta$ 与齐次方程组 $A^{\mathrm{T}}x=0$ 的所有解向量正交.

正确的个数为""",
        options=['A. 0.', 'B. 1.', 'C. 2.', 'D. 3.'],
    ),
    dict(
        no=18, origin='10', kind='choice', source='李永乐数二卷五-10·二次型定义', catId=50061,
        stem=r"""设 $A=(a_{ij})=\begin{pmatrix}1&1\\1&1\\0&a\end{pmatrix}$，定义二次型 $f(x_1,x_2)=\sum\limits_{i=1}^{3}\left(\sum\limits_{j=1}^{2}a_{ij}x_j\right)^2$，若 $f$ 为正定二次型，则实数 $a$ 应满足""",
        options=['A. $a=0$.', 'B. $a\neq 0$.', 'C. $a>0$.', 'D. $a<0$.'],
    ),
    dict(
        no=19, origin='22', kind='calc', source='ep 数二卷一-22·二次型与正交变换', catId=50062,
        stem=r"""（本题满分 $12$ 分）已知数列 $\{x_n\},\{y_n\}$ 满足 $x_0=y_0=1$，且对任意正整数 $n$，有

$$\begin{cases}x_n=y_{n-1}+\lambda^{\,n-1},\\ y_n=-2x_{n-1}+3y_{n-1}+2\lambda^{\,n-1},\end{cases}$$

记 $\alpha_n=\begin{pmatrix}x_n\\y_n\\\lambda^{\,n}\end{pmatrix}$.

(1) 写出满足 $\alpha_n=A\alpha_{n-1}$ 的矩阵 $A$；

(2) 若 $A$ 仅有两个不同的特征值且可相似对角化，求 $\lambda$ 的值；

(3) 在 (2) 的条件下，求 $x_n,y_n$ 的通项公式.""",
        options=[],
    ),
    dict(
        no=20, origin='4', kind='choice', source='李艳芳数一第三套第4题（原书列在「级数」章）', catId=50071,
        stem=r"""设封闭曲线 $L$ 的方程为 $\frac{x^2}{4}+y^2=1$，函数 $f(x,y)$ 满足 $\oint_L\frac{\partial f}{\partial n}\,\mathrm{d}s$ 等于由 $L$ 所围成区域 $D$ 的面积，其中 $n$ 是曲线 $L$ 的单位外法线向量，则 $f(x,y)$ 可以是下列函数中的（　　）""",
        options=[
            r'A. $e^x\sin y+\frac{y^2}{2}$.',
            r'B. $e^x\sin y+y^2$.',
            r'C. $\frac{x^2}{4}+y^2$.',
            r'D. $\frac{x^2}{2}+\frac{y^2}{4}$.',
        ],
    ),
    dict(
        no=21, origin='22', kind='calc', source='小侯七数一第一套第22题', catId=50082,
        stem=r"""已知 $X_1,X_2,\cdots,X_n\,(n\ge 2)$ 为来自正态总体 $N(\mu,\sigma^2)$ 的简单随机样本，参数 $\mu$ 与 $\sigma^2$ 未知.

(1) 已知 $\int_{-\infty}^{A}f(x,\mu,\sigma^2)\,\mathrm{d}x=0.975$，求参数 $A$ 的最大似然估计量，其中 $f(x,\mu,\sigma^2)$ 为总体随机变量 $X$ 的概率密度；($\Phi(1.96)=0.975$)

(2) 若 $\hat\mu$ 与 $\hat\sigma^2$ 分别为 $\mu$ 与 $\sigma^2$ 的最大似然估计量，计算期望 $E\left[(\hat\mu-\mu)^4\hat\sigma^4\right]$.""",
        options=[],
    ),
    dict(
        no=22, origin='22', kind='calc', source='小侯七数一第三套第22题', catId=50082,
        stem=r"""已知 $X_1,X_2,\cdots,X_{50}$ 为来自正态总体 $N(\mu,\sigma^2)$ 的简单随机样本，参数 $\mu$ 与 $\sigma^2$ 未知.

(1) 求参数 $\mu$ 与 $\sigma^2$ 的最大似然估计量；

(2) 若样本均值 $\bar x=14.75$，样本方差 $S^2=\frac{1}{49}\sum\limits_{i=1}^{50}(X_i-\bar X)^2=66.90$，求参数 $\mu$ 的置信度为 $0.95$ 的置信区间，其中 $\sqrt{S^2}\approx 8.18$，$t_{0.025}(49)=2.010$；

(3) 以 (2) 中样本数据考虑零假设 $H_0:\mu=12$ 与备择假设 $H_1:\mu\neq 12$，则在显著性水平 $\alpha=5\%$ 时，判断是否拒绝 $H_0$.""",
        options=[],
    ),
    dict(
        no=23, origin='9', kind='choice', source='李艳芳数一第二套第9题', catId=50081,
        stem=r"""设随机变量 $X$ 的分布函数为 $F(x)$，概率密度为 $f(x)$，则下列说法中，错误的是（　　）""",
        options=[
            r'A. $\frac{1}{2}[f(x)+f(-x)]$ 必为某随机变量的概率密度.',
            r'B. $f(x)f(-x)$ 必为某随机变量的概率密度.',
            r'C. $2f(x)F(x)$ 必为某随机变量的概率密度.',
            r'D. $2f(x)[1-F(x)]$ 必为某随机变量的概率密度.',
        ],
    ),
    dict(
        no=24, origin='10', kind='choice', source='李艳芳数一第二套第10题', catId=50082,
        stem=r"""设总体 $X$ 服从均匀分布 $U(\theta_1,\theta_2)$。$X_1,X_2,\cdots,X_{96}$ 为来自总体 $X$ 的一个简单随机样本。利用样本的一阶原点矩和二阶中心矩估计 $\theta_1,\theta_2$，矩估计值分别为 $\hat\theta_1,\hat\theta_2$。已知样本方差 $S^2=\frac{1}{10}$，则 $\hat\theta_2-\hat\theta_1=$（　　）""",
        options=[
            r'A. $\frac{\sqrt{19}}{5}$.',
            r'B. $\frac{\sqrt{19}}{4}$.',
            r'C. $\frac{\sqrt{30}}{5}$.',
            r'D. $\frac{\sqrt{30}}{4}$.',
        ],
    ),
    dict(
        no=25, origin='22', kind='calc', source='李艳芳数一第三套第22题', catId=50081,
        stem=r"""设随机变量 $X$ 服从 $(0,2)$ 上的均匀分布，当 $0<X\le 1$ 时，在 $X=x$ 的条件下，随机变量 $Y\sim N(x,1)$；当 $1<X<2$ 时，在 $X=x$ 的条件下，随机变量 $Y$ 服从 $(0,x)$ 上的均匀分布。令 $Z=\min\{X,Y\}$.

(Ⅰ) 求 $(X,Y)$ 的联合概率密度 $f(x,y)$；

(Ⅱ) 求 $Z$ 的概率密度 $f_Z(z)$，结果用标准正态分布的分布函数 $\Phi(z)$ 表示.""",
        options=[],
    ),
    dict(
        no=26, origin='9', kind='choice', source='张八数一第一套第9题', catId=50081,
        stem=r"""设 $X$ 与 $Y$ 为具有二阶矩的随机变量，且 $DX\neq 0$，若记 $G(a,b)=E\left\{[Y-(a+bX)]^2\right\}$，则 $G(a,b)$ 在驻点处的值为""",
        options=[
            r'A. $(1-\rho_{XY}^2)DY$.',
            r'B. $(1+\rho_{XY}^2)DY$.',
            r'C. $(1-\rho_{XY}^2)\mathrm{Cov}(X,Y)$.',
            r'D. $(1+\rho_{XY}^2)\mathrm{Cov}(X,Y)$.',
        ],
    ),
    dict(
        no=27, origin='10', kind='choice', source='张八数一第三套第10题', catId=50083,
        stem=r"""设两组数据分别来自两个方差相同且相互独立的正态总体 $X\sim N(\mu_1,\sigma^2)$ 与 $Y\sim N(\mu_2,\sigma^2)$。现检验两组数据的均值有无显著差异，且犯第一类错误的概率为 $\alpha$，则应""",
        options=[
            r'A. 在置信度为 $1-\alpha$ 下，检验 $H_0:\mu_1\neq\mu_2$；$H_1:\mu_1=\mu_2$.',
            r'B. 在置信度为 $1-\frac{\alpha}{2}$ 下，检验 $H_0:\mu_1\neq\mu_2$；$H_1:\mu_1=\mu_2$.',
            r'C. 在置信度为 $1-\alpha$ 下，检验 $H_0:\mu_1=\mu_2$；$H_1:\mu_1\neq\mu_2$.',
            r'D. 在置信度为 $1-\frac{\alpha}{2}$ 下，检验 $H_0:\mu_1=\mu_2$；$H_1:\mu_1\neq\mu_2$.',
        ],
    ),
    dict(
        no=28, origin='16', kind='blank', source='张八数一第三套第16题', catId=50081,
        stem=r"""设随机变量 $X$ 服从 $[-1,a]$ 上的均匀分布，如果由切比雪夫不等式得 $P\{|X-1|<\varepsilon\}\ge\frac{2}{3}$，则 $(a,\varepsilon)=$ ______.""",
        options=[],
    ),
    dict(
        no=29, origin='22', kind='calc', source='张八数一第三套第22题', catId=50081,
        stem=r"""快递驿站有 $2$ 个打包台，同时来了 $3$ 位寄件人：$A$ 和 $B$ 先在两个打包台打包快递，$C$ 需要等其中一个打包台空闲后，再开始打包。已知每个人的打包时间相互独立，且都服从参数为 $\lambda\,(\lambda>0)$ 的指数分布。求寄件人 $C$ 从进入驿站到打包完成离开的总时间 $T$ 的概率密度.""",
        options=[],
    ),
    dict(
        no=30, origin='22', kind='calc', source='张八数一第六套第22题', catId=50081,
        stem=r"""设商场某日的顾客总数 $N$ 服从泊松分布 $P(\lambda)$，单个顾客每次的消费额为 $1$（单位：元），令 $X_j$ 表示第 $j$ 个顾客 $n$ 次试验消费的次数，$X_j$ 与 $N$ 独立且服从二项分布 $B(n,p)$.

(1) 已知 $N=m\,(m>0)$ 的条件下，求全天营业额 $S$ 的概率分布；

(2) 计算 $E(S\mid N)$；

(3) 计算 $ES$.""",
        options=[],
    ),
    dict(
        no=31, origin='22', kind='calc', source='李六数一第六套第22题', catId=50082,
        stem=r"""设总体 $X\sim U[0,\theta]$，$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的简单随机样本。

(Ⅰ) 求 $\theta$ 的最大似然估计量 $\hat\theta$，并说明 $\hat\theta$ 是否为 $\theta$ 的无偏估计量；

(Ⅱ) 记 $X_{(n)}=\max(X_1,X_2,\cdots,X_n)$，若选取 $T=\frac{X_{(n)}}{\theta}$ 为统计量，判断 $\theta$ 的 $1-\alpha\,(0<\alpha<1)$ 的置信区间是否为

$$\left(\frac{X_{(n)}}{\sqrt[n]{1-\alpha/2}},\ \frac{X_{(n)}}{\sqrt[n]{\alpha/2}}\right).$$""",
        options=[],
    ),
    dict(
        no=32, origin='19', kind='calc', source='李艳芳数一第一套第19题', catId=50091,
        stem=r"""计算曲面积分

$$I=\iint_\Sigma\left[x\left(1+\frac{1}{|x|+|y|}\right)\mathrm{d}y\mathrm{d}z+y\left(1+\frac{1}{|x|+|y|}\right)\mathrm{d}z\mathrm{d}x+z\left(1+\frac{|x|}{|x|+|y|}\right)\mathrm{d}x\mathrm{d}y\right]$$

其中 $\Sigma$ 是圆柱面 $x^2+y^2=1$ 与平面 $z=1,\ z=-1$ 所围立体表面的外侧.""",
        options=[],
    ),
    dict(
        no=33, origin='4', kind='choice', source='李艳芳数一第二套第4题', catId=50092,
        stem=r"""设 $b_n\neq 0\,(n=0,1,\cdots)$，幂级数 $\sum\limits_{n=0}^{\infty}a_nx^n$ 与 $\sum\limits_{n=0}^{\infty}b_nx^n$ 的收敛半径分别为 $R$ 与 $2R$，$0<R<+\infty$。记幂级数 $\sum\limits_{n=0}^{\infty}(a_n-b_n)x^n$ 的收敛半径为 $r_1$，$\sum\limits_{n=0}^{\infty}\frac{a_n}{b_n}x^n$ 的收敛半径为 $r_2$，则（　　）""",
        options=[
            r'A. $r_1\le R,\ r_2=\frac{1}{2}$.',
            r'B. $r_1\le R,\ r_2\le\frac{1}{2}$.',
            r'C. $r_1=R,\ r_2=\frac{1}{2}$.',
            r'D. $r_1=R,\ r_2\le\frac{1}{2}$.',
        ],
    ),
    dict(
        no=34, origin='14', kind='blank', source='李艳芳数一第二套第14题', catId=50092,
        stem=r"""设 $f(x)$ 是周期为 $2\pi$ 的函数，且当 $x\in(-\pi,\pi)$ 时，$f(x)=|x\cos x|$。若 $f(x)=\frac{a_0}{2}+\sum\limits_{n=1}^{\infty}a_n\cos(nx)$，则 $\sum\limits_{n=1}^{\infty}a_{2n}=$ ______.""",
        options=[],
    ),
    dict(
        no=35, origin='19', kind='calc', source='李艳芳数一第二套第19题', catId=50093,
        stem=r"""设直线 $L$ 过点 $A(1,0,0)$、点 $B(1,1,1)$，将 $L$ 绕 $z$ 轴旋转一周得到曲面 $S$，$S$ 与平面 $x=2z$ 的交线为 $\Gamma$，从 $z$ 轴正向看去，$\Gamma$ 沿逆时针方向.

(Ⅰ) 求 $S$ 的曲面方程，并判断其形状；

(Ⅱ) 求曲线积分 $I=\int_\Gamma \sin(xy)\,\mathrm{d}x+(x^3+xz-z^2)\,\mathrm{d}y+(y+x^2z)\,\mathrm{d}z$.""",
        options=[],
    ),
    dict(
        no=36, origin='7', kind='choice', source='张八数一第五套第7题', catId=50093,
        stem=r"""线性方程组 $\begin{cases}x_1+x_2+ax_3=4,\\ x_1-x_2+2x_3=-4,\\ -x_1+ax_2+x_3=a^2\end{cases}$ 所代表的三个平面不可能的位置关系为（　　）

![四个选项均为三平面位置关系示意图](data/img/ys27/ys27_q36.png)""",
        options=[],
    ),
    dict(
        no=37, origin='14', kind='blank', source='张八数一第八套第14题', catId=50092,
        stem=r"""设 $S(x)=\sum\limits_{n=1}^{\infty}b_n\sin\frac{n\pi x}{2}$，其中 $b_n=\int_0^1 x^2\sin\frac{n\pi x}{2}\,\mathrm{d}x+\int_1^2 e^x\sin\frac{n\pi x}{2}\,\mathrm{d}x$，$n\in\mathbb{N}_+$，则 $S(-9)=$ ______.""",
        options=[],
    ),
]

# 三级分类：27 模拟卷精选题（L0）→ 九章（L1）→ 知识点（L2）
YS27_CATS = [
    dict(id=50000, name='27模拟卷精选题', parentId=None, level=0, ord=60000,
         path='27模拟卷精选题'),
    dict(id=50001, name='函数极限与连续', parentId=50000, level=1, ord=1),
    dict(id=50002, name='一元函数微分学', parentId=50000, level=1, ord=2),
    dict(id=50003, name='一元函数积分学', parentId=50000, level=1, ord=3),
    dict(id=50004, name='矩阵及行列式', parentId=50000, level=1, ord=4),
    dict(id=50005, name='向量与线性方程组', parentId=50000, level=1, ord=5),
    dict(id=50006, name='二次型', parentId=50000, level=1, ord=6),
    dict(id=50007, name='级数与曲线积分', parentId=50000, level=1, ord=7),
    dict(id=50008, name='概率论（数一/数三）', parentId=50000, level=1, ord=8),
    dict(id=50009, name='数一专项（数一）', parentId=50000, level=1, ord=9),

    dict(id=50011, name='等价无穷小与阶', parentId=50001, level=2, ord=1),
    dict(id=50021, name='抽象函数与凹凸性', parentId=50002, level=2, ord=1),
    dict(id=50022, name='可导性概念', parentId=50002, level=2, ord=2),
    dict(id=50023, name='微分概念与增量', parentId=50002, level=2, ord=3),
    dict(id=50024, name='反常积分敛散性', parentId=50002, level=2, ord=4),
    dict(id=50025, name='有界性与导数', parentId=50002, level=2, ord=5),
    dict(id=50031, name='积分计算与反函数', parentId=50003, level=2, ord=1),
    dict(id=50032, name='积分物理应用', parentId=50003, level=2, ord=2),
    dict(id=50041, name='相似对角化', parentId=50004, level=2, ord=1),
    dict(id=50042, name='秩与矩阵关系', parentId=50004, level=2, ord=2),
    dict(id=50043, name='矩阵运算与概念', parentId=50004, level=2, ord=3),
    dict(id=50051, name='向量组线性相关性', parentId=50005, level=2, ord=1),
    dict(id=50052, name='方程组解的结构', parentId=50005, level=2, ord=2),
    dict(id=50061, name='正定与标准形', parentId=50006, level=2, ord=1),
    dict(id=50062, name='二次型与对角化', parentId=50006, level=2, ord=2),
    dict(id=50071, name='曲线积分与格林公式', parentId=50007, level=2, ord=1),
    dict(id=50081, name='分布与数字特征', parentId=50008, level=2, ord=1),
    dict(id=50082, name='参数估计', parentId=50008, level=2, ord=2),
    dict(id=50083, name='假设检验', parentId=50008, level=2, ord=3),
    dict(id=50091, name='曲面积分', parentId=50009, level=2, ord=1),
    dict(id=50092, name='幂级数与傅里叶', parentId=50009, level=2, ord=2),
    dict(id=50093, name='空间解析几何与曲线积分', parentId=50009, level=2, ord=3),
]

# 章节标题（数据里的 section.title；只用于展示与题型分组，与分类树无关）
CHAPTERS = [
    (50001, '一、函数极限与连续'),
    (50002, '二、一元函数微分学'),
    (50003, '三、一元函数积分学'),
    (50004, '四、矩阵及行列式'),
    (50005, '五、向量与线性方程组'),
    (50006, '六、二次型'),
    (50007, '七、级数与曲线积分'),
    (50008, '八、概率论'),
    (50009, '九、数一专项'),
]
