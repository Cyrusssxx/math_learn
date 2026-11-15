# -*- coding: utf-8 -*-
"""mn27 十套卷「答案 ↔ 题目」审校修复（2026-11-15）。

两类改动：
  ROWS  按行号整行改写：清除【易错】/解析正文里的转写溯源措辞（48 行）
  TEXT  按内容精确替换：修实质数学 / 一致性错误
  BLOCK 按题块做参数记号统一

每条替换都断言命中一次（或已应用），失败即整体中止，不写盘。
用法：python tools/_fix_mn27_audit.py && python tools/_build_mn27.py
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'mn27_ans')

ROWS = [
 ('q01_ans.md', 9, '【易错】', r'【易错】第一类间断点要求左右极限都存在且有限（含可去、跳跃两类），函数在某点未定义并不自动说明它属于哪一类，要看邻近极限。另：题面分子是 $2x^{2n}-1$，其中 $-1$ 不是指数的一部分；若误读成 $2x^{2n-1}$，则 $0<|x|<1$ 时分式趋于 $0$，与三段极限结论 $-1,\dfrac12,2$ 矛盾。'),
 ('q01_ans.md', 114, '【易错】', r'【易错】$B$ 的第 2 行第 3 列为 0，该元素会改变矩阵平方与秩，务必按题中矩阵计算。另：一个向量成为特征向量必须「非零」且满足 $Ac=\lambda c$；$N^2=O$ 意味着 $N$ 的每一列被 $N$ 再次作用后变为 0，正好与本题第一个命题对应。'),
 ('q01_ans.md', 244, '【易错】', r'【易错】用交换 $x,y$ 的对称性，必须同时检查区域不变和函数变号。平方换元时在坐标轴上雅可比写成倒数会退化，但可先在内部换元再取边界极限；本题 $xy\,\mathrm{d}x\mathrm{d}y$ 组合直接变为 $\dfrac14\mathrm{d}u\mathrm{d}v$ 最清楚。另：$\sqrt[3]{x-y}$ 是实立方根（具奇性），不要当成 $3$ 倍平方根。'),
 ('q02_ans.md', 38, '【易错】', r'【易错】一侧趋于无穷就足以归为无穷间断点，不要求左右都为同一个无穷；约分后"式子在某点有值"不等于原函数已在该点定义。$x\to1$ 时约分后的式子趋于 $\dfrac12\mathrm e^{-1}$，为可去间断点；不要把 $x\to0$ 处的 $\pm\mathrm e^{-1/2}$ 误用到此处。'),
 ('q02_ans.md', 51, '【易错】', r'【易错】本题题设不相容：由 $\lim f(x)/x=0$ 得 $f(0)=f\prime(0)=0$，于是 $x\to0^+$ 时 $xf\prime\prime(x)+\mathrm e^{f(x)}\to1$ 而 $6\ln(1+x)\to0$，不等式无法成立。做题不仅要会算，也要检查条件能否同时成立；答案栏的 A 只是忽略该矛盾后的形式估计，不代表题设相容，正式使用需出题勘误。'),
 ('q02_ans.md', 96, '【易错】', r'【易错】区域内 $x+y$ 可以小于 $1$，因此"幂次越大数值越大"并非处处成立，不能直接套到积分；平移后利用奇函数项积分为 $0$ 能消掉大量项。三个积分按 $k=1,2,3$ 定义，注意 B 选项比较的是 $I_3$。'),
 ('q02_ans.md', 269, '【易错】', r'【易错】几何关系先写成积分、再对上限求导可转为微分方程；平方后开根号要依据 $f\prime$ 的符号选支，没有严格单调条件时可能出现水平段、唯一性需另查。由面积等于弧长与 $f(0)=1$ 可推出 $f\prime(0)=0$，故 $f\prime(x)>0$ 应理解为 $0<x\le1$；若把严格正号也施于 $x=0$，题设就矛盾。'),
 ('q02_stem.md', 25, '[本本注', ''),
 ('q03_ans.md', 9, '【易错】', r'【易错】用 $\mathrm{e}^u-1\sim u$ 前须确认指数 $u=\frac{\ln(1+x)}{x}-1\to0$。拆分后第一项化为 $\mathrm e\lim\frac{\ln(1+x)-x}{x^2}=-\frac{\mathrm e}{2}$，第二项为 $\mathrm e$，两者相加得 $\frac{\mathrm e}{2}$；不要把两项并列重复计算。'),
 ('q03_ans.md', 98, '【易错】', r'【易错】当 $a=-2$ 时对 $(B,A)$ 作初等行变换（竖虚线分隔 $B$ 与 $A$ 的列）'),
 ('q03_ans.md', 119, '【易错】', r'【易错】$A^{\mathrm{T}}AX=0$ 与 $AX=0$ 同解：设 $A^{\mathrm{T}}Aa=0$，则 $(Aa)^{\mathrm{T}}(Aa)=|Aa|^2=0\Rightarrow Aa=0$。由 $A_{11}\ne0$ 得 $(\alpha_2,\cdots,\alpha_n)$ 线性无关，故 $b=C_2\alpha_2+\cdots+C_n\alpha_n$ 时 $(0,C_2,\cdots,C_n)^{\mathrm{T}}$ 是 $AX=b$ 的解；注意下标从 $C_2$ 起，不要写成 $C_1$ 或重复 $C_2$。'),
 ('q03_ans.md', 246, '【易错】', r'【易错】也可用二重积分一般换元 $x-1=u,\ y-1=v$ 一次算出'),
 ('q04_ans.md', 23, '【易错】', r'【易错】分子分母须同除以 $x^6$ 才能凑出 $\left[\frac{F(x)}{x^2}\right]^3$；勿把 $f\prime(0)=6$ 直接当作 $\lim\frac{F(x)}{x^2}$（相差因子 $\frac12$）。另：作为选择题可取特殊值 $f(x)=6x$，此时'),
 ('q04_ans.md', 33, '【易错】', r'【易错】三条曲线中 $l_1$ 单调增加且恒在 $x$ 轴上方，$l_2$ 先增后减并在 $x=1$ 回到 $x$ 轴，$l_3$ 单调减少且穿过 $x$ 轴；判定 $f\prime$ 的图形时注意在极大值点 $x_0$ 左侧 $f\prime>0$、右侧 $f\prime<0$，且 $f\prime(x_0)=0$。'),
 ('q04_ans.md', 50, '**① 命题①。**', r'**① 命题①。** 由 $f\prime\prime(x)<0$ 知割线斜率 $\frac{f(t)-f(0)}{t}$ 随 $t$ 增大而不增，故对 $0\le t\le x$ 有 $\frac{f(t)-f(0)}{t-0}\ge\frac{f(x)-f(0)}{x-0}\ (t\in[0,x])$，结合 $f(0)=1$ 得 $f(t)\ge\frac{f(x)-1}{x}t+1$，命题①正确。'),
 ('q04_ans.md', 51, '**② 命题②。**', r'**② 命题②。** 由 $f\prime\prime(x)>0$ 知割线斜率随 $t$ 增大而不减，同理 $\frac{f(t)-f(0)}{t-0}\le\frac{f(x)-f(0)}{x-0}$，即 $f(t)\le\frac{f(x)-1}{x}t+1$，命题②正确。'),
 ('q04_ans.md', 58, '【易错】', r'【易错】$F\prime\prime\ge0$ 时曲线开口向上，两端点为 0 则 $F(x)\le0$；中文教材「凹/凸」术语定义不一，勿因名称混淆不等号方向。若 $f\prime\prime(x)\ge0\ (x\in[a,b])$ 且 $f(a)=f(b)=0$，则 $f(x)\le0$，此即④的依据。'),
 ('q04_ans.md', 86, '【易错】', r'【易错】题面 $f=(x+y)^n\sin\frac{1}{\sqrt{x^2+y^2}}$（不是 $(x+y)^n\cdot\frac{1}{\sin\sqrt{x^2+y^2}}$；后者在 $n=1$ 时并不趋于 $0$）。$n=2$ 时振荡项极限不存在是区分 B、C 的关键。'),
 ('q04_ans.md', 122, '【易错】', r'【易错】① 中矩阵 $A^T(B+B^T)A$ 是实对称矩阵，故①成立。实矩阵 $A$ 可正交相似于对角矩阵的充分必要条件是 $A$ 有 $n$ 个相互正交的特征向量（即 $A$ 为实对称矩阵）；④ 中反对称矩阵（非零时）不能正交相似对角化。'),
 ('q04_ans.md', 304, '【易错】', r'【易错】由 $F_n(x)$ 严格单调增加、$F_n(x_n)=0$ 及 $F_n(\frac kn-\frac{k}{n^2})<0$ 得 $\frac kn-\frac{k}{n^2}<x_n<\frac kn$（左端是减号，否则左端大于右端）。另 $(1+\frac kn-\frac{k}{n^2})^n\to e^k$ 需验证 $\left(\frac kn-\frac k{n^2}\right)n\to k$。'),
 ('q04_ans.md', 332, '【易错】', r'【易错】$\alpha\alpha^T\alpha\alpha^T=\alpha(\alpha^T\alpha)\alpha^T$，其中 $\alpha^T\alpha$ 是数可提到前面；$\lambda=-2$ 要代入 $\lambda^2-(2-k)\lambda+(1-k)=0$。（II）须由单位特征向量继续构造 $Q$ 并给出 $B$，仅写出 $\gamma_1,\gamma_2,\gamma_3$ 不算完成。'),
 ('q05_ans.md', 14, '【易错】', r'【易错】$D(x)$ 处处无极限，故 $f\prime(0)\ne0$ 时 $g\prime(0)$ 必不存在；勿由 $g$ 连续反推 $f$ 连续。原题在 $f(0)=0$ 下 (B) 也成立（见解析②），属题设瑕疵，参考答案仍按 (D)。'),
 ('q05_ans.md', 27, '【易错】', r'【易错】$f(x)=\sqrt[3]{x^2+\ln^2|x|}$ 的主阶是 $x^{2/3}$ 而非 $x$；$x\to-\infty$ 时 $g(x)\sim-x$、$h(x)\sim x^2$，必须与 $+\infty$ 分开讨论；被开方是 $x^2+\ln^2|x|$（平方），勿误作 $x^3+\ln^4|x|$。'),
 ('q05_ans.md', 50, '【易错】', r'【易错】题设只假设 $f$ 连续，未保证 $f\prime(0)$、$f\prime\prime(0)$ 存在，(A)(B) 都可能因不可导而失效；(D) 的反例是 $x^5$（不是 $x^2$ 或 $x^4$）。(B) 说的是 $f\prime(x)$ 的极小值点（带一撇），与 (A) 的 $f(x)$ 不对称，勿看漏。'),
 ('q05_ans.md', 86, '【易错】', r'【易错】三个偏导数是"相乘"得 $-1$，不是"相加"得 $-1$；③ 与 ④ 只差运算符，这是本题最主要的辨识点。'),
 ('q05_ans.md', 134, '【易错】', r'【易错】题干条件是 $\dfrac{1}{n^2}$ 的同阶（不是 $\dfrac{1}{n}$ 的同阶），因此要同时消去 $\ln(n+1)$ 与 $\dfrac{1}{n+1}$；只列 $1+a+b=0$ 会少一个方程。注意 $\dfrac{1}{n^2}$ 的上标，勿读作 $\dfrac{1}{n}$。'),
 ('q05_ans.md', 172, '【易错】', r'【易错】题干分母是 $x^2+y^2$（不是 $x^2+y^4$）；$f\prime\prime_{xy}(0,0)$ 表示"先对 $x$ 再对 $y$"求导，与部分教材 $\dfrac{\partial^2f}{\partial y\partial x}$ 的下标顺序约定不同，须按计算步骤理解；不能直接对 $f\prime\prime_{xy}(x,y)$ 取极限（该偏导在原点不连续）。'),
 ('q05_ans.md', 196, '【易错】', r'【易错】$|B-E|=4$ 为正（不是 $-4$），故 $|A|=\dfrac12$ 为正；勿把 $|B-E|$ 误算成 $-4$ 而得到 $-\dfrac12$。'),
 ('q05_ans.md', 207, '【易错】', r'【易错】题干是 $(1+x)^{\frac{2}{x}}-e^{2}\left[1-\ln(1+x)\right]$：指数为 $\dfrac{2}{x}$、常数为 $e^2$，勿误作 $(1+x)^{1/x}$ 与 $e^x$；若误读则分子不趋于 $0$，极限不存在。展开必须到 $x^2$ 阶，$x$ 一次项恰好抵消。'),
 ('q05_ans.md', 305, '【易错】', r'【易错】(I) 标准形写作 $3y_1^2-3y_3^2$ 跳过 $y_2$（零特征值排在第二位），并非漏项；(II) $x=Py$ 要求 $P$ 是"由 $y$ 到 $x$"的变换，故须对系数矩阵取逆，直接写原矩阵会错；(III) $f=0$ 是两个平面的并集，每组通解须各含两个任意常数。'),
 ('q06_ans.md', 12, '【易错】', r'【易错】题干求的是 $f^{(2n)}(1)$（$2n$ 阶导数）而非 $f^{(n)}(1)$，漏看阶数会误选 (A)；莱布尼茨展开的中间项系数应为 $C_{2n}^k\dfrac{n!}{(n-k)!}(x-1)^{n-k}g^{(2n-k)}(x)$。'),
 ('q06_ans.md', 33, '故选 (D)', r'故选 (D)（由凹函数的梯形与切线关系可证）。'),
 ('q06_ans.md', 158, '**① 换序并夹逼。**', r'**① 换序并夹逼。** 记 $M(a)=\int_0^a\mathrm{d}x\int_{\frac x2}^{x}e^{-y^2}\mathrm{d}y$（区域介于 $y=\frac x2$ 与 $y=x$ 之间）。交换积分次序，由 $x\in[y,2y]$ 得'),
 ('q06_ans.md', 164, '【易错】', r'【易错】极限是 $a\to+\infty$ 而非 $a\to0$，外层积分上限是 $a$；换序后外层对 $y$ 积分，微分是 $\mathrm{d}y$，与 $\int_0^a\mathrm{d}y\int_y^{2y}e^{-y^2}\mathrm{d}x$ 一致。'),
 ('q06_ans.md', 213, '【易错】', r'【易错】$f$ 在 $x=\frac\pi2$ 处跳跃（左极限 1、右极限 0），故 $F$ 连续但不可导，$F\prime(x)$ 的分段区间必须去掉 $x=\frac\pi2$；右导数用 $\cos t$、左导数用 $\sin t$，勿把两者对调。'),
 ('q06_ans.md', 273, '【易错】', r'【易错】（III）中的 $\left(\pm\frac{\sqrt6}{3},\pm\frac{\sqrt6}{6},\pm\frac{\sqrt6}{6}\right)^T$ 三个 $\pm$ 应理解为同号（只有 $\pm\alpha_3$ 两个点），否则会误以为有 8 个取最大值的点；另 $Q$ 的列须按特征值 $1,2,5$ 的顺序排列，才对应标准形 $y_1^2+2y_2^2+5y_3^2$。'),
 ('q07_ans.md', 20, '【易错】', r'【易错】题干积分上限为 $e^{x^2}$、分母为 $\ln(1+x^4)$，勿读作 $e^x$、$\ln(1+x^2)$；上限求导会多出因子 $2x$；常把「同阶但不等价」误选为「等价无穷小」。'),
 ('q07_ans.md', 102, '【易错】', r'【易错】「当 $a=b$ 时」的行列式左下角应为 $a$ 而非 $b$（不影响 $\lambda_{1,2}=1\pm a$）；相似与合同是两种不同等价关系，不可混用。'),
 ('q07_ans.md', 128, '【易错】', r'【易错】积分上下限是 $[n^2,n^2+n]$（勿读作 $[n,n^2]$，那样积分发散），区间长度为 $n$ 而非 $n^2-n$；本题不能先算原函数。'),
 ('q07_ans.md', 139, '【易错】', r'【易错】题目求的是 $f^{(2027)}(1)$，故通项中取 $n=2025$；$(-1)^{2025}=-1$ 决定整体符号，别漏。'),
 ('q07_ans.md', 150, '【易错】', r'【易错】括号内是 $\varphi(y-bz)$（含 $bz$，勿读作 $bx$）；条件 $a-b\varphi\prime\ne0$ 正是公分母非零的保证，$\varphi\prime$ 不能当常数处理。'),
 ('q07_ans.md', 172, '【易错】', r'【易错】积分括号内是 $f\prime(t)$ 而非 $f\prime\prime(t)$（写成 $f\prime\prime$ 会得到矛盾式）；初始条件 $f\prime(0)=0$ 需由原方程求导后令 $x=0$ 得到。'),
 ('q07_ans.md', 184, '【易错】', r'【易错】题目求的是 $x^2$ 的系数（勿读作 $x^3$）；按 $(-1,0,0)$ 行展开时前面的负号别丢，即 $-\begin{vmatrix}2x-1&1\\6x+2&x-1\end{vmatrix}$。'),
 ('q07_ans.md', 196, '【易错】', r'【易错】分母是 $\cos^{\frac52}x$（勿读作 $\cos^{\frac32}x$）；$\sec^2x=(\tan x)\prime$ 与 $\left(\frac1{\sqrt{\cos x}}\right)\prime$ 中的系数 $\frac12$ 必须对齐，最后勿漏 $+C$。'),
 ('q07_ans.md', 224, '【易错】', r'【易错】$b=3+\sqrt[3]{3}$ 而非 $3+\sqrt[3]{9}$；化简根式要用 $\sqrt[3]{81}=3\sqrt[3]{3}$，两个立方根不能合并。'),
 ('q07_ans.md', 268, '【易错】', r'【易错】$(A+E)^*$ 是 $A+E$ 的伴随矩阵（不是 $A+E$ 本身），其特征值须用 $\det(A+E)/\lambda_i\prime$；对角元顺序要与 $P$ 的列 $\beta_1,\beta_2,\beta_3$ 对应为 $1,10,10$；第 (III) 问中的对角矩阵记作 $\Lambda$，勿与矩阵 $A$ 混淆。'),
 ('q09_ans.md', 66, '【易错】', r'【易错】$\alpha\sim\beta$ 不保证 $\alpha+\gamma\sim\beta+\gamma$（和可为 0 而失去意义）；④ 中 $\gamma\ne0$ 才能约去，$\alpha=o(\beta)$ 时 $\frac{\alpha\gamma}{\beta\gamma}=\frac\alpha\beta\to0$，结论是 $\alpha\gamma=o(\beta\gamma)$。'),
 ('q10_stem.md', 46, '[本本注', ''),
]

# 内容级替换：(文件, 原文, 新文, 期望命中数)
TEXT = [
 ('q02_ans.md', '【答案】A\n【解】\n**① 由极限求 $f(0)$ 与 $f\prime(0)$。**',
  '【答案】A（原题条件矛盾，仅形式估计；见解析②勘误）\n【解】\n**① 由极限求 $f(0)$ 与 $f\prime(0)$。**', 1),
 ('q05_ans.md', '**② 排除 (B)。** 取 $f(x)\\equiv1$，则 $g(x)=D(x)$ 在 $x=0$ 处不连续，但 $f(x)$ 连续，故 (B) 错误。',
  '**② 关于 (B) 的题设瑕疵。** 题干已给 $f(0)=0$，此时 $|g(x)|=|D(x)f(x)|\\le|f(x)|$，故 $f$ 在 $0$ 连续必推出 $g$ 在 $0$ 连续，即 (B)「$g$ 不连续 $\\Rightarrow$ $f$ 不连续」也成立，与单选设定冲突。若用 $f\\equiv1$ 排除 (B)，该反例不满足 $f(0)=0$。本题按参考答案取 (D)，并把 (B) 同真这一点如实标出。', 1),
 ('q06_stem.md', 'f(x,x^2-1,f(x-1,\\ln x))=x^3', 'f(x^2-1,f(x-1,\\ln x))=x^3', 1),
 ('q06_ans.md', '不能代 $x=0$（$\\ln x$ 无定义）；内层 $f(x-1,\\ln x)$ 的导数含 $\\frac1x$ 因子。',
  '不能代 $x=0$（$\\ln x$ 无定义）；内层 $f(x-1,\\ln x)$ 的导数含 $\\frac1x$ 因子。另：第二式右端为 $x^3$ 时，代 $x=1$ 得左端 $f(0,f(0,0))=f(0,0)=0\\ne1$，原题等式在该点不自洽；下文按导数关系形式求解，结论与参考答案一致。', 1),
 ('q09_ans.md', '**④ 判 ④。** 因 $\\gamma\\ne0$，$\\dfrac{\\alpha\\gamma}{\\beta\\gamma}=\\dfrac\\alpha\\beta\\to1$，即 $\\alpha\\gamma\\sim\\beta\\gamma$，④ 正确。',
  '**④ 判 ④。** 题设 $\\alpha=o(\\beta)$ 即 $\\dfrac\\alpha\\beta\\to0$；因 $\\gamma\\ne0$ 可约去，$\\dfrac{\\alpha\\gamma}{\\beta\\gamma}=\\dfrac\\alpha\\beta\\to0$，即 $\\alpha\\gamma=o(\\beta\\gamma)$，④ 正确。', 1),
 ('q09_ans.md', '\\ln(1+u)-1}-1}{eu}=\\lim', '\\ln(1+u)-1}-1}{u}=\\lim', 1),
 ('q10_ans.md', '所以「恰有 $l$ 个」不成立，① 错。',
  '所以解向量个数至少为 $\\max(l,m)$，① 的「至多」没有保证；例如 $n=2$ 时取 $A=\\mathrm{diag}(1,0)$、$B=\\mathrm{diag}(0,1)$，则 $l=m=1$ 而 $BA=O$，$(BA)x=0$ 有 $2>1$ 个线性无关解，① 错。', 1),
 ('q10_ans.md', '当 $a=0$ 时 $x=0$，由 ④ 得 $y=\\pm\\frac{\\sqrt2}2$，驻点 $\\left(0,\\pm\\frac{\\sqrt2}2,\\mp\\frac{\\sqrt2}2\\right)$；当 $a\\ne0$ 时 $x=\\frac1{3a}$，由 $|a|<\\frac13$ 得 $|x|>1$，不满足 ④，舍去。',
  '$x=0$ 时（对任意 $a$ 都成立）由 ④ 得 $y=\\pm\\frac{\\sqrt2}2$，驻点 $\\left(0,\\pm\\frac{\\sqrt2}2,\\mp\\frac{\\sqrt2}2\\right)$；另一支 $x=\\frac1{3a}$（$a\\ne0$）由 $|a|<\\frac13$ 得 $|x|>1$，不满足 ④，舍去。', 1),
 ('q10_ans.md', '$a=0$ 得驻点 $\\left(0,\\pm\\frac{\\sqrt2}2,\\pm\\frac{\\sqrt2}2\\right)$，$a\\ne0$ 时 $x=-\\frac1{3a}$ 同样因 $|x|>1$ 舍去。',
  '$x=0$（任意 $a$）得驻点 $\\left(0,\\pm\\frac{\\sqrt2}2,\\pm\\frac{\\sqrt2}2\\right)$；另一支 $x=-\\frac1{3a}$（$a\\ne0$）同样因 $|x|>1$ 舍去。', 1),
 ('q04_ans.md', '当 $x\\in(0,x_0)$ 时 $f\\prime(x)\\ge0$，当 $x\\in(x_0,1)$ 时 $f\\prime(x_0)\\le0,\\ f\\prime(x_0)=0$，$l_3$ 满足要求',
  '当 $x\\in(0,x_0)$ 时 $f\\prime(x)>0$，当 $x\\in(x_0,1)$ 时 $f\\prime(x)<0$，且 $f\\prime(x_0)=0$，$l_3$ 满足要求', 1),
 ('q04_ans.md', '**① 排除 $l_1$。** 若 $l_1$ 是 $f(x)$ 的图形，则 $f(x)$ 在 $[0,1]$ 上单调增加且 $f(x)>0\\ (x\\in(0,1])$，故 $f\\prime(x)\\ge0,\\ \\int_0^x f(t)\\,dt>0$；但 $l_3$ 中 $x$ 轴下方有图形，故 $l_1$ 不是 $y=f(x)$ 的图形，排除 A、B。',
  '**① 排除 $l_1$。** 若 $l_1$ 是 $f(x)$ 的图形，则 $f(x)$ 在 $[0,1]$ 上单调增加且 $f(x)>0\\ (x\\in(0,1])$，故 $f\\prime(x)\\ge0$ 恒非负、$\\int_0^x f(t)\\,dt$ 单调增加且恒正；三条曲线中只有 $l_1$ 同时满足「单调增、恒正」，而 $l_2$ 在 $x=1$ 回到 $x$ 轴、$l_3$ 穿过 $x$ 轴进入负值，均不能充当 $\\int_0^x f$ 或 $f\\prime$，排除 A、B。', 1),
 ('q04_ans.md', '**③ 排除 $l_3$。** 若 $l_3$ 是 $y=f(x)$ 的图形，则 $f(x)$ 在 $[0,1]$ 上单调减少，从而 $f\\prime(x)\\le0$，故 D 不正确。',
  '**③ 排除 $l_3$。** 若 $l_3$ 是 $y=f(x)$ 的图形，则 $f(x)$ 在 $[0,1]$ 上单调减少且由正变负，从而 $f\\prime(x)\\le0$、$\\int_0^x f(t)\\,dt$ 先增后减，与 D 中 $l_1$（单调增）、$l_2$（恒非负）都不符，故 D 不正确。', 1),
 ('q04_ans.md', '**① 由 $AB=BA$ 读出 $A$ 的相似形。**', '**① 由 $AB=B\\Lambda$ 读出 $A$ 的相似形。**', 1),
 ('q04_ans.md', '=BA$$\n又 $B$ 可逆', '=B\\Lambda\\ (\\Lambda=\\mathrm{diag}(2,3,-1))$$\n又 $B$ 可逆', 1),
 ('q04_ans.md', '由 $AB=BA$ 且 $B$ 可逆得', '由 $AB=B\\Lambda$ 且 $B$ 可逆得', 1),
 ('q01_ans.md', '**① 用二阶展开计算差分极限。** 与第一套第 21 题一样，', '**① 用二阶展开计算差分极限。** ', 1),
 ('q01_ans.md', '【易错】第一套第 21 题用「弦线在上」证明上界，本题用「切线在下」证明下界。',
  '【易错】本题用「切线在下」证明下界（凸函数情形），与「弦线在上」证明上界是对偶手段。', 1),
 ('q05_ans.md', '但 $f\\prime\\prime(0)=0$，故 (D) 错', '但 $f\\prime\\prime\\prime(0)=60x^2\\big|_{x=0}=0$，故 (D) 错', 1),
 ('q02_stem.md', '$f\\prime(x)>0$，若在区间 $[0,x]$ 上', '$f\\prime(x)>0\\ (0<x\\le1)$，若在区间 $[0,x]$ 上', 1),
 ('q02_ans.md', '并给 $f\\prime>0$；按 $0<x\\le1$ 上 $f\\prime(x)>0$ 理解，$f$ 由 $1$ 递增、保持正值',
  '并给 $0<x\\le1$ 上 $f\\prime(x)>0$，$f$ 由 $1$ 递增、保持正值', 1),
 ('q06_stem.md', '知当 $x\\to0$ 时', '已知当 $x\\to0$ 时', 1),
 ('q09_ans.md', '；（II）极大值 $f(0,0)=\\dfrac43$，极小值 $f(1,1)=0$',
  '；（II）四个驻点 $(0,0)$、$(1,1)$、$\\left(\\frac{3+\\sqrt3}{4},\\frac{3-\\sqrt3}{4}\\right)$、$\\left(\\frac{3-\\sqrt3}{4},\\frac{3+\\sqrt3}{4}\\right)$，其中只有 $(0,0)$ 为极大值点（极大值 $f(0,0)=\\dfrac43$）、$(1,1)$ 为极小值点（极小值 $f(1,1)=0$），另两驻点非极值点', 1),
 ('q10_ans.md', '；（II）$\\varphi\\prime(x)$ 在 $x=0$ 处连续', '；（II）$\\varphi\\prime(0)=0$，且 $\\varphi\\prime(x)$ 在 $x=0$ 处连续', 1),
 ('q02_ans.md', '$x\\to1$ 时约分后的式子趋于有限值，为可去间断点', '$x\\to1$ 时约分后的式子趋于 $\\dfrac12\\mathrm e^{-1}$，为可去间断点', 1),
 # q04 Q22 (II) 补全：答案行 + 解答新增第 ④ 步
 ('q04_ans.md', '\\gamma_3=\\frac1{\\sqrt3}(1,1,1)^T$\n【解】',
  '\\gamma_3=\\frac1{\\sqrt3}(1,1,1)^T$；$B=\\dfrac13\\begin{pmatrix}5&-1&-1\\\\-1&5&-1\\\\-1&-1&5\\end{pmatrix}$（正定，且 $B^2=A+3E$）\n【解】', 1),
 ('q04_ans.md', '$$\\gamma_1=\\frac1{\\sqrt2}(-1,1,0)^T,\\qquad\\gamma_2=\\frac1{\\sqrt6}(1,1,-2)^T,\\qquad\\gamma_3=\\frac1{\\sqrt3}(1,1,1)^T$$\n【思路】',
  '$$\\gamma_1=\\frac1{\\sqrt2}(-1,1,0)^T,\\qquad\\gamma_2=\\frac1{\\sqrt6}(1,1,-2)^T,\\qquad\\gamma_3=\\frac1{\\sqrt3}(1,1,1)^T$$\n**④ 构造正定矩阵 $B$。** 令 $Q=(\\gamma_1,\\gamma_2,\\gamma_3)$，则 $Q$ 正交且\n$$Q^TAQ=\\mathrm{diag}(1,1,-2),\\qquad Q^T(A+3E)Q=\\mathrm{diag}(4,4,1).$$\n取\n$$B=Q\\,\\mathrm{diag}(2,2,1)Q^T=2E-\\frac13\\begin{pmatrix}1&1&1\\\\1&1&1\\\\1&1&1\\end{pmatrix}=\\frac13\\begin{pmatrix}5&-1&-1\\\\-1&5&-1\\\\-1&-1&5\\end{pmatrix},$$\n其特征值为 $2,2,1>0$，故 $B$ 正定；又 $B^2=Q\\,\\mathrm{diag}(4,4,1)Q^T=A+3E=A+kE$，满足题意。\n【思路】', 1),
]

# 参数记号统一：(文件, 题号, 处理方式)
BLOCK = [
 ('q07_ans.md', 6, 'a_to_alpha'),
 ('q09_ans.md', 11, 'a_to_alpha'),
 ('q05_ans.md', 6, 'alpha_to_a'),
]


def main():
    # 本脚本是一次性修复记录：ROWS 按行号定位，插入新解析段后行号会偏移。
    # 检测到已应用即直接返回，避免重复跑出假失败。
    done = open(os.path.join(SRC, 'q04_ans.md'), encoding='utf-8').read()
    if '**④ 构造正定矩阵 $B$。**' in done and '见解析②勘误' in open(os.path.join(SRC, 'q02_ans.md'), encoding='utf-8').read():
        print('✓ 本轮修复已应用（一次性脚本，无需重跑）')
        return

    # 源码内用 \prime 规避字符串定界冲突，写盘前还原成草稿原有的 ASCII 撇号
    def P(s):
        return s.replace(r'\prime', "'")

    cache = {}
    def load(f):
        if f not in cache:
            p = os.path.join(SRC, f)
            cache[f] = open(p, encoding='utf-8').read()
        return cache[f]
    def put(f, s):
        cache[f] = s

    # 1) 按行号整行替换（不改变行数）
    byfile = {}
    for f, ln, key, new in ROWS:
        byfile.setdefault(f, []).append((ln, key, new))
    for f, rows in byfile.items():
        lines = load(f).split('\n')
        for ln, key, new in rows:
            new = P(new)
            cur = lines[ln - 1]
            if (new and new in cur) or (not new and not cur.strip()):
                continue  # 已应用
            assert key in cur, f'{f}:{ln} 行内容不符 -> {cur[:60]!r}'
            lines[ln - 1] = new
        put(f, '\n'.join(lines))
    print(f'ROWS: {len(ROWS)} 行溯源措辞已改写')

    # 2) 内容级精确替换
    for f, old, new, want in TEXT:
        old, new = P(old), P(new)
        s = load(f)
        if s.count(old) == 0 and new in s:
            continue  # 已应用
        assert s.count(old) == want, f'{f}: 期望 {want} 次命中，实际 {s.count(old)} 次 -> {old[:70]!r}'
        put(f, s.replace(old, new, want))
    print(f'TEXT: {len(TEXT)} 处实质修复')

    # 3) 块级参数记号统一
    for f, no, mode in BLOCK:
        s = load(f)
        pat = re.compile(r'(?====Q(\d+)===)')
        m = list(pat.finditer(s))
        start = next(x.start() for x in m if int(x.group(1)) == no)
        end = next((x.start() for x in m if int(x.group(1)) == no + 1), len(s))
        blk = s[start:end]
        if mode == 'a_to_alpha':
            if '\\alpha' in blk and not re.search(r'(?<![A-Za-z\\])a(?![A-Za-z])', blk):
                continue
            nb = re.sub(r'(?<![A-Za-z\\])a(?![A-Za-z])', r'\\alpha', blk)
        else:
            nb = blk.replace('\\alpha', 'a')
        put(f, s[:start] + nb + s[end:])
    print(f'BLOCK: {len(BLOCK)} 个题块记号统一')

    for f, s in cache.items():
        with open(os.path.join(SRC, f), 'w', encoding='utf-8', newline='') as fh:
            fh.write(s)
    print('✓ 草稿修复已写盘，请运行 _build_mn27.py 重建数据')


if __name__ == '__main__':
    main()
