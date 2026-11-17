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
]

# 章节标题（数据里的 section.title；只用于展示与题型分组，与分类树无关）
CHAPTERS = [
    (50001, '一、函数极限与连续'),
    (50002, '二、一元函数微分学'),
    (50003, '三、一元函数积分学'),
    (50004, '四、矩阵及行列式'),
    (50005, '五、向量与线性方程组'),
    (50006, '六、二次型'),
]
