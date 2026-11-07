# -*- coding: utf-8 -*-
"""2016 数二第 23 题（矩阵高次幂 + 分块列组合）：补齐关键步骤、修公式排版与串题 tips。
双份数据同步：exam.json 的 2016数二真题-23 与 core_bank.json 的 no.819（linkedQid 指向前者）。

格式铁律（按文件实测，勿改）：
  exam.json      -> json.dumps(d, ensure_ascii=False)            单行、无尾换行
  core_bank.json -> json.dumps(d, indent=1, ensure_ascii=False)  逐字段一行、无尾换行
"""
import json

EXAM = 'pwa/data/exam.json'
CORE = 'pwa/data/core_bank.json'

HEAD = r"""【答案】（I）$A^{99}=\begin{pmatrix}2^{99}-2&1-2^{99}&2-2^{98}\\2^{100}-2&1-2^{100}&2-2^{99}\\0&0&0\end{pmatrix}$；
（II）$\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2$，$\beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2$，$\beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2$。
"""

BODY = r"""
**（I）第一步：求特征值与特征向量**

按 $\lambda E-A$ 的第 3 行展开（该行只有最后一个元素 $\lambda$）：
$$
|\lambda E-A|=\begin{vmatrix}\lambda&1&-1\\-2&\lambda+3&0\\0&0&\lambda\end{vmatrix}
=\lambda\begin{vmatrix}\lambda&1\\-2&\lambda+3\end{vmatrix}
=\lambda\bigl[\lambda(\lambda+3)+2\bigr]=\lambda(\lambda^2+3\lambda+2)=\lambda(\lambda+1)(\lambda+2).
$$
特征值为 $\lambda_1=-2,\ \lambda_2=-1,\ \lambda_3=0$，三者互异，故 $A$ 可对角化。

解 $(\lambda E-A)x=0$ 得特征向量：
$\lambda_1=-2$：由 $A+2E=\begin{pmatrix}2&-1&1\\2&-1&0\\0&0&2\end{pmatrix}$ 得 $x_3=0$、$2x_1-x_2=0$，取 $\xi_1=(1,2,0)^{\mathrm T}$；
$\lambda_2=-1$：由 $A+E=\begin{pmatrix}1&-1&1\\2&-2&0\\0&0&1\end{pmatrix}$ 得 $x_3=0$、$x_1=x_2$，取 $\xi_2=(1,1,0)^{\mathrm T}$；
$\lambda_3=0$：由 $Ax=0$ 得 $-x_2+x_3=0$、$2x_1-3x_2=0$，取 $x_2=2$ 得 $\xi_3=(3,2,2)^{\mathrm T}$。

**第二步：构造 $P$ 并求 $P^{-1}$**

以 $\xi_1,\xi_2,\xi_3$ 为列（顺序与对角元 $-2,-1,0$ 一一对应）：
$$
P=\begin{pmatrix}1&1&3\\2&1&2\\0&0&2\end{pmatrix},\qquad P^{-1}AP=\Lambda=\mathrm{diag}(-2,-1,0).
$$
$|P|=-2\ne0$，对 $(P\mid E)$ 作初等行变换（或由 $P^{-1}=\frac{1}{|P|}P^{*}$）得
$$
P^{-1}=\begin{pmatrix}-1&1&\frac12\\2&-1&-2\\0&0&\frac12\end{pmatrix}.
$$

**第三步：算 $A^{99}=P\Lambda^{99}P^{-1}$**

$99$ 为奇数，$\Lambda^{99}=\mathrm{diag}\bigl((-2)^{99},(-1)^{99},0\bigr)=\mathrm{diag}(-2^{99},-1,0)$。先算
$$
P\Lambda^{99}=\begin{pmatrix}-2^{99}&-1&0\\-2^{100}&-1&0\\0&0&0\end{pmatrix},
$$
再右乘 $P^{-1}$（逐列相乘，例如第 1 列 $=(-2^{99})(-1)+(-1)\cdot2=2^{99}-2$）：
$$
A^{99}=(P\Lambda^{99})P^{-1}=\begin{pmatrix}2^{99}-2&1-2^{99}&2-2^{98}\\2^{100}-2&1-2^{100}&2-2^{99}\\0&0&0\end{pmatrix}.
$$

**（II）第一步：归纳证明 $B^{n}=BA^{n-1}\ (n\ge2)$**

基例 $n=2$ 即题设 $B^2=BA$。若 $B^k=BA^{k-1}$ 成立，则
$$
B^{k+1}=B\cdot B^k=B\bigl(BA^{k-1}\bigr)=B^2A^{k-1}=(BA)A^{k-1}=BA^{k}.
$$
故对一切 $n\ge2$ 成立；取 $n=100$ 得 $B^{100}=BA^{99}$。全过程只用 $B^2=BA$ 与结合律，**不需要** $A,B$ 可交换。

**第二步：按列分块读出 $\beta_j$**

记 $A^{99}=(c_1,c_2,c_3)$。由矩阵乘法的列分块规则
$$
B^{100}=BA^{99}=B(c_1,c_2,c_3)=(Bc_1,\ Bc_2,\ Bc_3),
$$
而 $B=(\alpha_1,\alpha_2,\alpha_3)$，故 $\beta_j=Bc_j$，即 $\beta_j$ 是 $\alpha_1,\alpha_2,\alpha_3$ 以 $c_j$ 的分量为系数的线性组合（**注意** $\beta_j$ 是 $B^{100}$ 的第 $j$ 列，不是 $B^{100}\alpha_j$）。
$$
c_1=\begin{pmatrix}2^{99}-2\\2^{100}-2\\0\end{pmatrix},\quad
c_2=\begin{pmatrix}1-2^{99}\\1-2^{100}\\0\end{pmatrix},\quad
c_3=\begin{pmatrix}2-2^{98}\\2-2^{99}\\0\end{pmatrix}.
$$
代入得
$$
\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,\quad
\beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2,\quad
\beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2.
$$
$A^{99}$ 第 3 行全为 $0$，所以三个组合里都不含 $\alpha_3$。

**易错点**：① 特征向量与 $\Lambda$ 对角元必须同序；② $(-2)^{99}=-2^{99}$、$(-1)^{99}=-1$（奇数次幂为负）；③ 归纳时不能擅自交换 $A,B$；④ $\beta_j$ 的系数取自 $A^{99}$ 的**第 $j$ 列**，不是第 $j$ 行。
"""

SCORE = r"""
📋 **评分参考（满分 11 分）｜按考研数学阅卷通用规则估算**

**（I）** ① 求特征值 $0,-1,-2$ 与特征向量，$P^{-1}AP=\mathrm{diag}(-2,-1,0)$ — **3 分**（结构分）
② $A^{99}=P\Lambda^{99}P^{-1}$，计算得 $A^{99}$ — **4 分**（关键推导）
**（II）** ③ 归纳证 $B^n=BA^{n-1}$，$B^{100}=BA^{99}$ — **2 分**
④ 由 $B^{100}=(\alpha_1,\alpha_2,\alpha_3)A^{99}$ 写出 $\beta_1,\beta_2,\beta_3$ 线性组合 — **2 分**
"""

IDEA = r"""**思路**：(I) 三个特征值互异 ⟹ $A=P\Lambda P^{-1}$，于是 $A^{99}=P\Lambda^{99}P^{-1}$；(II) 由 $B^2=BA$ 归纳出 $B^n=BA^{n-1}$，再用列分块把 $B^{100}=BA^{99}$ 的每一列写成 $\alpha_1,\alpha_2,\alpha_3$ 的线性组合。
① $|\lambda E-A|=\lambda(\lambda+1)(\lambda+2)$，特征向量按 $-2,-1,0$ 的顺序排成 $P$；
② $\Lambda^{99}=\mathrm{diag}(-2^{99},-1,0)$，算出 $A^{99}$ 的三列；
③ $A^{99}$ 第 3 行全为 $0$，故 $\beta_1,\beta_2,\beta_3$ 都不含 $\alpha_3$。"""

TIPS = {
    "gs": r"$|\lambda E-A|=\lambda(\lambda+1)(\lambda+2)$，特征值 $0,-1,-2$；$A^{99}=P\,\mathrm{diag}(-2^{99},-1,0)P^{-1}$。",
    "jq": r"三特征值互异可对角化；先算 $P\Lambda^{99}$ 再右乘 $P^{-1}$，比三矩阵连乘少一半运算；$B^{100}=BA^{99}$ 用列分块 $(Bc_1,Bc_2,Bc_3)$ 读系数。",
    "yc": r"特征向量与对角元必须同序；$(-2)^{99}=-2^{99}$ 的符号；归纳只能用 $B^2=BA$，不能交换 $A,B$；$\beta_j$ 取的是 $A^{99}$ 的第 $j$ 列而非第 $j$ 行。",
    "zy": r"$A^{99}$ 第 3 行为 $0$，所以三个 $\beta_j$ 都不含 $\alpha_3$；$\beta_j$ 是 $B^{100}$ 的第 $j$ 列，不是 $B^{100}\alpha_j$。",
}

# ---------- exam.json ----------
raw = open(EXAM, encoding='utf-8').read()
d = json.loads(raw)
assert json.dumps(d, ensure_ascii=False) == raw, 'exam.json 格式与预期不符，停止'
n = 0
for p in d:
    if p.get('id') != '2016数二真题':
        continue
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            if q.get('no') == 23:
                old = q['answer']
                assert ('评分参考' in old) or old.startswith('【答案】（I）$A^{99}'), 'exam 23 内容已变'
                q['answer'] = HEAD + BODY + SCORE
                q['idea'] = IDEA
                q['tips'] = TIPS
                n += 1
assert n == 1, 'exam 命中 %d 题' % n
open(EXAM, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False))

# ---------- core_bank.json ----------
raw = open(CORE, encoding='utf-8').read()
c = json.loads(raw)
assert json.dumps(c, indent=1, ensure_ascii=False) == raw, 'core_bank.json 格式与预期不符，停止'
n = 0
for p in c:
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            if q.get('no') == 819 and q.get('linkedQid') == '2016数二真题-23':
                old = q['answer']
                assert ('由矩阵 $A$ 的特征值' in old) or old.startswith('【答案】（I）$A^{99}'), 'core 819 内容已变'
                q['answer'] = HEAD + BODY
                q['idea'] = IDEA
                q['tips'] = TIPS
                n += 1
assert n == 1, 'core 命中 %d 题' % n
open(CORE, 'w', encoding='utf-8', newline='\n').write(json.dumps(c, indent=1, ensure_ascii=False))

print('已同步：exam.json 2016数二真题-23 与 core_bank.json no.819')
print('answer(含评分参考) %d 字 / 无评分参考 %d 字, idea %d 字, tips 4 段' %
      (len(HEAD + BODY + SCORE), len(HEAD + BODY), len(IDEA)))
