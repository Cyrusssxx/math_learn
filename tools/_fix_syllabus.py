# -*- coding: utf-8 -*-
"""剔除 mn27 十套卷 / exam.json 真题答案中的数一·数三专属内容，替换为数二大纲内的等价表述。

设计约束：
- exam.json 是单行紧凑 JSON，必须 json.loads -> 改 dict -> json.dumps(ensure_ascii=False) 写回；
  该序列化格式与文件原始字节完全一致（已验证）。
- 每条替换显式断言命中次数为 1；重复执行时若 old 已消失且 new 已在，则跳过（幂等）。
- 不改动题目（stem/options）与最终结论，只替换答案/思路/点睛里的超纲名称、解法与元话语。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM = os.path.join(ROOT, 'pwa', 'data', 'exam.json')
DRAFT = os.path.join(ROOT, 'tools', 'mn27_ans', 'q07_ans.md')

# (卷 id, 题号, 字段路径, 原文, 新文)
PATCH = [
    # ---------- 2026 数二 Q21：伯努利方程（数一专属）→ 倒数换元 ----------
    ('2026数二真题', 21, 'answer',
     r'''这是 $n=2$ 的伯努利方程，令 $z=\dfrac1p$，则 $z'=-\dfrac{p'}{p^2}$，代入得一阶线性方程''',
     r'''对含 $p^2$ 的方程作倒数换元 $z=\dfrac1p$，则 $z'=-\dfrac{p'}{p^2}$，代入得一阶线性方程'''),
    ('2026数二真题', 21, 'answer',
     r'''积分因子为 $x^2$，于是 $(x^2z)'=-1$，解得''',
     r'''两边同乘 $x^2$，得 $(x^2z)'=-1$，解得'''),
    ('2026数二真题', 21, 'idea',
     r'''① 令 $p=y'$，得伯努利方程 $p'-\dfrac2xp=\dfrac{p^2}{x^2}$。② 令 $z=\dfrac1p$ 化一阶线性''',
     r'''① 令 $p=y'$，得 $p'-\dfrac2xp=\dfrac{p^2}{x^2}$；② 再令 $z=\dfrac1p$ 化一阶线性'''),
    ('2026数二真题', 21, 'tips.gs',
     r'''不显含 $y$ 的二阶方程令 $p=y'$；伯努利方程 $p'-\dfrac2xp=\dfrac{p^2}{x^2}$ 取 $z=\dfrac1p$ 化为一阶线性。''',
     r'''不显含 $y$ 的二阶方程令 $p=y'$；对 $p'-\dfrac2xp=\dfrac{p^2}{x^2}$ 取倒数换元 $z=\dfrac1p$ 化为一阶线性。'''),
    ('2026数二真题', 21, 'tips.yc',
     r'''伯努利倒数变换后符号易错；''',
     r'''倒数换元后符号易错；'''),

    # ---------- 2025 数二 Q15：全微分方程/势函数（数一专属）→ 凑全微分 ----------
    ('2025数二真题', 15, 'answer',
     r'''方程为全微分方程，存在势函数 $U(x,y)$ 使 $dU=P\,dx+Q\,dy=0$。''',
     r'''故左端是某个二元函数 $U(x,y)$ 的全微分，即 $dU=P\,dx+Q\,dy=0$。'''),
    ('2025数二真题', 15, 'idea',
     r'''**思路**：验证全微分，构造势函数 $U(x,y)=C$，再代入初值。① $P=2y-3x,\ Q=2x-5y$，$P_y=Q_x=2$，是全微分方程。''',
     r'''**思路**：验证左端为全微分，构造二元函数 $U(x,y)=C$，再代入初值。① $P=2y-3x,\ Q=2x-5y$，$P_y=Q_x=2$，故可直接凑全微分。'''),
    ('2025数二真题', 15, 'tips.gs',
     r'''恰当微分方程判定：$\dfrac{\partial}{\partial y}(2y-3x)=2=\dfrac{\partial}{\partial x}(2x-5y)$，故为全微分方程。''',
     r'''由 $\dfrac{\partial}{\partial y}(2y-3x)=2=\dfrac{\partial}{\partial x}(2x-5y)$，左端可凑成二元函数 $U$ 的全微分 $dU=P\,dx+Q\,dy$。'''),
    ('2025数二真题', 15, 'tips.jq',
     r'''求势函数 $U$ 使''',
     r'''求二元函数 $U$ 使'''),

    # ---------- 2024 数二 Q18：欧拉方程（数一专属名称）→ 按题设提示换元 ----------
    ('2024数二真题', 18, 'answer',
     r'''（1）这是欧拉方程。令 $x=\mathrm e^t$''',
     r'''（1）按题设提示令 $x=\mathrm e^t$'''),
    ('2024数二真题', 18, 'idea',
     r'''**思路**：欧拉方程用 $x=\mathrm e^t$ 化为常系数方程。''',
     r'''**思路**：按题设提示用 $x=\mathrm e^t$ 化为常系数方程。'''),
    ('2024数二真题', 18, 'tips.gs',
     r'''欧拉方程换元 $x=\mathrm e^t$：''',
     r'''换元 $x=\mathrm e^t$：'''),

    # ---------- 2024 数二 Q17：考纲元话语 ----------
    ('2024数二真题', 17, 'idea',
     r'''（面积），全程只用考纲内的直角坐标方法。③ 算面积：''',
     r'''（面积）。③ 用直角坐标分两段算面积：'''),

    # ---------- 2023 数二 Q5：数一共用题溯源注 ----------
    ('2023数二真题', 5, 'tips.zy',
     r'''本题即 2023 数二第 5 题（= 2023 数一第 3 题）。''',
     ''),

    # ---------- 2020 数二 Q4：无穷级数展开（数一/数三专属）→ 带佩亚诺余项的麦克劳林公式 ----------
    ('2020数二真题', 4, 'answer',
     r'''【答案】(A)
$\ln(1-x)=-\sum\limits_{k=1}^{\infty}\frac{x^k}{k}$，故 $f(x)=x^2\ln(1-x)$ 中 $x^n$ 的系数为 $-\frac{1}{n-2}$。
又 $f^{(n)}(0)=n!\times(\text{\text{第}}x^n\text{\text{项的系数}})$，故 $f^{(n)}(0)=-\dfrac{n!}{n-2}$，选(A)。''',
     r'''【答案】(A)
由带佩亚诺余项的麦克劳林公式，取到 $n$ 阶（$n\ge3$）：
$$\ln(1-x)=-\sum_{k=1}^{n}\frac{x^k}{k}+o(x^n)\quad(x\to0).$$
两边乘 $x^2$ 得
$$f(x)=x^2\ln(1-x)=-\sum_{k=1}^{n}\frac{x^{k+2}}{k}+o(x^{n+2}),$$
其中 $x^n$ 项对应 $k=n-2$，系数为 $-\dfrac1{n-2}$。
又由泰勒公式系数与导数的关系 $f(x)=\dfrac{f^{(n)}(0)}{n!}x^n+o(x^n)$，得
$$f^{(n)}(0)=n!\times\left(-\frac1{n-2}\right)=-\frac{n!}{n-2},$$
选 (A)。'''),
    ('2020数二真题', 4, 'idea',
     r'''**思路**：$n$ 阶导数在 $0$ 的值由幂级数 $x^n$ 项系数决定。
① $\ln(1-x)=-\sum_{k\ge1}\tfrac{x^k}{k}$。
② $f(x)=x^2\ln(1-x)$ 中 $x^n$ 的系数为 $-\tfrac1{n-2}$。
③ $f^{(n)}(0)=n!\times(\text{\text{系数}})=-\tfrac{n!}{n-2}$，选 A。''',
     r'''**思路**：用带佩亚诺余项的麦克劳林公式取到 $n$ 阶，再由 $x^n$ 项系数读出 $f^{(n)}(0)$。
① $\ln(1-x)=-\sum_{k=1}^{n}\frac{x^k}{k}+o(x^n)$。
② $f(x)=x^2\ln(1-x)$ 中 $x^n$ 项（$k=n-2$）系数为 $-\tfrac1{n-2}$。
③ 由泰勒系数关系 $f^{(n)}(0)=n!\times$（$x^n$ 项系数）$=-\tfrac{n!}{n-2}$，选 A。'''),
    ('2020数二真题', 4, 'tips.gs',
     r'''泰勒系数法：$\ln(1-x)=-\displaystyle\sum_{k\ge1}\dfrac{x^{k}}{k}$ → $x^{2}\ln(1-x)=\displaystyle\sum_{k\ge1}\left(-\dfrac1k\right)x^{k+2}$。''',
     r'''麦克劳林公式（带佩亚诺余项）：$\ln(1-x)=-\sum_{k=1}^{n}\dfrac{x^{k}}{k}+o(x^n)$ → $x^{2}\ln(1-x)=-\sum_{k=1}^{n}\dfrac{x^{k+2}}{k}+o(x^{n+2})$。'''),
    ('2020数二真题', 4, 'tips.jq',
     r'''$x^{n}$ 系数（$n\ge3$）$=-\dfrac{1}{n-2}$ → $f^{(n)}(0)=n!\times\left(-\dfrac{1}{n-2}\right)$。''',
     r'''$x^{n}$ 项对应 $k=n-2$，系数为 $-\dfrac{1}{n-2}$ → $f^{(n)}(0)=n!\times\left(-\dfrac{1}{n-2}\right)$。'''),
    ('2020数二真题', 4, 'tips.yc',
     r'''负号；$n-2$ 的错位（乘 $x^{2}$ 幂次 +2）。''',
     r'''负号；$n-2$ 的错位（乘 $x^{2}$ 幂次 +2）；展开必须写成有限阶并带 $o(x^n)$，不要用无穷级数。'''),

    # ---------- 同类排查：2000 数二 Q13（与 2020 Q4 同题型的幂级数解法）----------
    ('2000数二真题', 13, 'answer',
     r'''【解析】利用莱布尼茨公式和 $\ln(1+x)$ 的麦克劳林展开。
$$\ln(1+x)=\sum_{k=1}^{\infty}\frac{(-1)^{k-1}}{k}x^{k},\quad |x|<1.f(x)=x^{2}\sum_{k=1}^{\infty}\frac{(-1)^{k-1}}{k}x^{k}
=\sum_{k=1}^{\infty}\frac{(-1)^{k-1}}{k}x^{k+2}
=\sum_{m=3}^{\infty}\frac{(-1)^{m-3}}{m-2}x^{m}$$
比较 $x^{n}$ 的系数：$f^{(n)}(0)/n! = \dfrac{(-1)^{n-3}}{n-2}=\dfrac{(-1)^{n-1}}{n-2}$。
故
$$f^{(n)}(0)=\frac{(-1)^{n-1}n!}{n-2},\quad n\geqslant 3$$
.''',
     r'''【解析】用带佩亚诺余项的麦克劳林公式（取到 $n$ 阶，$n\ge3$）：
$$\ln(1+x)=\sum_{k=1}^{n}\frac{(-1)^{k-1}}{k}x^{k}+o(x^n)\quad(x\to0).$$
两边乘 $x^{2}$ 得
$$f(x)=x^{2}\ln(1+x)=\sum_{k=1}^{n}\frac{(-1)^{k-1}}{k}x^{k+2}+o(x^{n+2}),$$
其中 $x^{n}$ 项对应 $k=n-2$，系数为 $\dfrac{(-1)^{n-3}}{n-2}=\dfrac{(-1)^{n-1}}{n-2}$。
由泰勒公式系数与导数的关系 $f(x)=\dfrac{f^{(n)}(0)}{n!}x^{n}+o(x^{n})$，得
$$f^{(n)}(0)=\frac{(-1)^{n-1}n!}{n-2},\quad n\ge3.$$'''),
    ('2000数二真题', 13, 'idea',
     r'''**思路**：用麦克劳林展开比较 $x^n$ 系数。
① $\ln(1+x)=\sum_{k=1}^\infty\tfrac{(-1)^{k-1}}kx^k$，$|x|<1$。
② $f(x)=x^2\ln(1+x)$，展开后 $x^n$ 项系数为 $\tfrac{(-1)^{n-1}}{n-2}$。
③ $f^{(n)}(0)/n!=$ 该系数。''',
     r'''**思路**：用带佩亚诺余项的麦克劳林公式取到 $n$ 阶，比较 $x^n$ 项系数。
① $\ln(1+x)=\sum_{k=1}^{n}\tfrac{(-1)^{k-1}}kx^{k}+o(x^{n})$。
② $f(x)=x^{2}\ln(1+x)$ 中 $x^{n}$ 项（$k=n-2$）系数为 $\tfrac{(-1)^{n-1}}{n-2}$。
③ 由泰勒系数关系 $f^{(n)}(0)=n!\times$（$x^{n}$ 项系数）$=\tfrac{(-1)^{n-1}n!}{n-2}$。'''),
    ('2000数二真题', 13, 'tips.gs',
     r'''泰勒系数法：$f^{(n)}(0)=n!\cdot[x^{n}]f(x)$——高阶导数问题优先想展开，不用莱布尼茨。''',
     r'''麦克劳林公式（带佩亚诺余项）取到 $n$ 阶，$f^{(n)}(0)=n!\times$（$x^{n}$ 项系数）。'''),

    # ---------- 同类排查：2010 数二 Q11 tips ----------
    ('2010数二真题', 11, 'tips.gs',
     r'''$\ln(1-2x)=-\displaystyle\sum_{n\ge1}\dfrac{(2x)^{n}}{n}$ → $x^{n}$ 系数 $-\dfrac{2^{n}}{n}$ → $y^{(n)}(0)=n!\times$系数 $=-2^{n}(n-1)!$。''',
     r'''麦克劳林公式（带佩亚诺余项）取到 $n$ 阶：$\ln(1-2x)=-\sum_{k=1}^{n}\dfrac{(2x)^{k}}{k}+o(x^{n})$ → $x^{n}$ 项系数 $-\dfrac{2^{n}}{n}$ → $y^{(n)}(0)=n!\times$系数 $=-2^{n}(n-1)!$。'''),
    ('2010数二真题', 11, 'tips.jq',
     r'''展开比逐次求导快一个量级；$y^{(n)}(0)=n!\cdot[x^{n}]y$。''',
     r'''用有限阶展开比逐次求导快；$y^{(n)}(0)=n!\times$（$x^{n}$ 项系数）。'''),

    # ---------- 同类排查：2014 数二 Q20 tips 混入另一题的级数内容 ----------
    ('2014数二真题', 20, 'tips.jq',
     r'''$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{1+f_n(x)}$ 本题求 $\lim f_n=?$ ——$\dfrac{1}{f_{n+1}}=\dfrac{1}{f_n}+1$ 调和递推 → $\dfrac{1}{f_n}=\dfrac1x+(n-1)$。''',
     r'''由 $\dfrac1{f_{n+1}}=\dfrac1{f_n}+1$ 归纳得 $f_n(x)=\dfrac{x}{1+nx}$；再算 $S_n=\int_0^1\dfrac{x}{1+nx}\,\mathrm dx=\dfrac1n\left[1-\dfrac{\ln(1+n)}{n}\right]$。'''),
    ('2014数二真题', 20, 'tips.yc',
     r'''倒数化线性递推是关键；$\lim\limits_{n\to\infty}f_n(x)=\lim\dfrac{x}{nx+1-x}=\dfrac1n?\to0$——题目求 $\lim nf_n=1$。''',
     r'''倒数化线性递推是关键；$nS_n=1-\dfrac{\ln(1+n)}{n}$，由 $\dfrac{\ln n}{n}\to0$ 得 $\lim\limits_{n\to\infty}nS_n=1$。'''),
    ('2014数二真题', 20, 'tips.zy',
     r'''$\lim\limits_{n\to\infty}nf_n(x)=1$。''',
     r'''$\lim\limits_{n\to\infty}nS_n=1$。'''),

    # ---------- 同类排查：2024 数二 Q7 反例改用等比部分和（有限和 + 单调有界）----------
    ('2024数二真题', 7, 'answer',
     r'''构造反例：令 $f(x)$ 在第 $n$ 个区间 $[n,n+\frac1{n^3}]$ 上取常值 $n$，其余为 $0$。则
$$\int_0^{+\infty}f(x)\mathrm dx=\sum_{n=1}^\infty n\cdot\frac1{n^3}=\sum_{n=1}^\infty\frac1{n^2}<+\infty$$
收敛，但在尖峰处 $x^pf(x)=n^p\cdot n=n^{p+1}\to+\infty$，不可能有极限（有限），故不存在这样的 $p$。命题③为假。''',
     r'''构造反例：令 $f(x)$ 在 $[2^{n},\,2^{n}+4^{-n}]$ 上取常值 $2^{n}$、其余为 $0$（把阶梯磨成窄的连续尖峰即可满足连续性，面积数量级不变）。对任意 $N$，
$$\int_0^{2^{N}+4^{-N}}f(x)\,\mathrm dx=\sum_{n=1}^{N}2^{n}\cdot4^{-n}=\sum_{n=1}^{N}\frac1{2^{n}}<1,$$
由 $f\ge0$ 且部分积分一致有界知 $\int_0^{+\infty}f(x)\,\mathrm dx$ 收敛；但在尖峰处 $x^pf(x)\ge(2^{n})^{p}\cdot2^{n}=2^{n(p+1)}\to+\infty$，不可能有有限极限，故不存在这样的 $p$。命题③为假。'''),
    ('2024数二真题', 7, 'idea',
     r'''③ 命题③（若 $\int f$ 收敛则存在 $p>1$ 使 $\lim x^pf(x)$ 存在）：构造 $f$ 在 $[n,n+\frac1{n^3}]$ 上取值 $n$、其余为 $0$，则 $\int f=\sum\frac1{n^2}$ 收敛，但 $x^pf(x)$ 在尖峰处为 $n^{p+1}\to\infty$，不存在这样的 $p$，故③假。''',
     r'''③ 命题③（若 $\int f$ 收敛则存在 $p>1$ 使 $\lim x^pf(x)$ 存在）：令 $f$ 在 $[2^{n},\,2^{n}+4^{-n}]$ 上取值 $2^{n}$、其余为 $0$（磨成连续尖峰不改结论），则部分积分 $\int_0^{2^{N}+4^{-N}}f=\sum_{n=1}^{N}2^{-n}<1$ 一致有界，故 $\int f$ 收敛；但尖峰处 $x^pf(x)\ge2^{n(p+1)}\to\infty$，不存在这样的 $p$，故③假。'''),
]

# 草稿 q07_ans.md：第一类曲线积分 → 弧长微元 + 参数定积分
DRAFT_PATCH = [
    (r'''**① 质心公式。** 摆线 $\begin{cases} x=t-\sin t,\\ y=1-\cos t, \end{cases}\ (0\le t\le2\pi)$ 的质心纵坐标 $\bar y=\dfrac{\int_L y\,ds}{\int_L ds}$。''',
     r'''**① 质心公式（化为参数 $t$ 的定积分）。** 摆线 $\begin{cases} x=t-\sin t,\\ y=1-\cos t, \end{cases}\ (0\le t\le2\pi)$ 的弧长微元为 $\mathrm ds=\sqrt{x'^2(t)+y'^2(t)}\,\mathrm dt$，线密度为 $1$ 时质心纵坐标为
$$\bar y=\frac{\int_0^{2\pi}y(t)\sqrt{x'^2(t)+y'^2(t)}\,\mathrm dt}{\int_0^{2\pi}\sqrt{x'^2(t)+y'^2(t)}\,\mathrm dt}.$$'''),
    (r'''$$\int_L ds=\int_0^{2\pi}\sqrt{x'^2(t)+y'^2(t)}\,dt''',
     r'''$$\int_0^{2\pi}\sqrt{x'^2(t)+y'^2(t)}\,\mathrm dt'''),
    (r'''$$\int_L y\,ds=\int_0^{2\pi}(1-\cos t)\cdot2\left|\sin\frac t2\right|dt''',
     r'''$$\int_0^{2\pi}y(t)\sqrt{x'^2(t)+y'^2(t)}\,\mathrm dt=\int_0^{2\pi}(1-\cos t)\cdot2\left|\sin\frac t2\right|dt'''),
    (r'''【思路】摆线一拱的质心用第一类曲线积分 $\bar y=\int_L y\,ds\big/\int_L ds$ 计算。''',
     r'''【思路】摆线一拱的质心用弧长微元 $\mathrm ds=\sqrt{x'^2+y'^2}\,\mathrm dt$ 化为参数 $t$ 的定积分计算。'''),
]


def get_field(q, path):
    cur = q
    for key in path.split('.'):
        cur = cur[key]
    return cur


def set_field(q, path, val):
    keys = path.split('.')
    cur = q
    for key in keys[:-1]:
        cur = cur[key]
    cur[keys[-1]] = val


# 历史缺陷：2021 数二卷 tips 中 \frac 被 JSON 解析成换页符 U+000C + "rac"
CTRL_CHAR = '\x0c'
CTRL_FIX = '\\f'


def fix_control_chars(node):
    """就地还原被 JSON 转义吃掉的反斜杠；返回还原数量。"""
    n = 0
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if isinstance(v, str):
                if CTRL_CHAR in v:
                    node[k] = v.replace(CTRL_CHAR, CTRL_FIX)
                    n += v.count(CTRL_CHAR)
            else:
                n += fix_control_chars(v)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, str):
                if CTRL_CHAR in v:
                    node[i] = v.replace(CTRL_CHAR, CTRL_FIX)
                    n += v.count(CTRL_CHAR)
            else:
                n += fix_control_chars(v)
    return n


def apply_exam():
    raw = open(EXAM, 'rb').read().decode('utf-8')
    d = json.loads(raw)
    idx = {p['id']: {q['no']: q
                     for s in p['sections'] for q in s['questions']}
           for p in d}
    applied = skipped = 0
    for pid, no, path, old, new in PATCH:
        q = idx[pid][no]
        cur = get_field(q, path)
        assert isinstance(cur, str), (pid, no, path, type(cur))
        if old in cur:
            assert cur.count(old) == 1, f'{pid} Q{no} {path}: old 出现 {cur.count(old)} 次'
            set_field(q, path, cur.replace(old, new, 1))
            applied += 1
        else:
            if new == '':
                assert '数一第' not in cur, f'{pid} Q{no} {path}: 溯源注未清除'
            else:
                assert (cur == new) or (new in cur), f'{pid} Q{no} {path}: old 未命中且 new 不在'
            skipped += 1
    ctrl = fix_control_chars(d)
    out = json.dumps(d, ensure_ascii=False)
    if out != raw:
        with open(EXAM, 'w', encoding='utf-8', newline='') as f:
            f.write(out)
    print(f'[exam.json] 应用 {applied} 条，已应用跳过 {skipped} 条，控制字符还原 {ctrl} 处；'
          f'写回格式与原文一致：{len(out.encode("utf-8"))} 字节')
    return applied + ctrl


def apply_draft():
    s = open(DRAFT, encoding='utf-8').read()
    applied = skipped = 0
    for old, new in DRAFT_PATCH:
        if old in s:
            assert s.count(old) == 1, f'草稿替换命中 {s.count(old)} 次: {old[:50]}'
            s = s.replace(old, new, 1)
            applied += 1
        else:
            assert new in s, f'草稿 old 未命中且 new 不在: {old[:50]}'
            skipped += 1
    open(DRAFT, 'w', encoding='utf-8', newline='').write(s)
    print(f'[q07_ans.md] 应用 {applied} 条，已应用跳过 {skipped} 条')
    return applied


def main():
    a = apply_exam()
    b = apply_draft()
    print(f'合计 {a + b} 条替换；幂等重跑应输出「应用 0 条」')
    return 0


if __name__ == '__main__':
    sys.exit(main())
