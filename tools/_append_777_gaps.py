# -*- coding: utf-8 -*-
"""把 777 必背资料比对出的 5 条真实缺漏，按「各归其位」追加到对应笔记末尾。

铁律：
  - 原 md 必须是新 md 的严格前缀（批注按 笔记id#块序号 定位，绝不改已有内容）
  - 新增 ## 章必须同步追加 chapters 数组项（chapters[i] ↔ 正文第 i 个 ## 镜像）
  - 章标题不得含 $...$（目录取 textContent，KaTeX 会双副本）
  - notes.json 写回 indent=2、无尾换行
"""
import json, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'pwa', 'data', 'notes.json')
raw_old = io.open(P, encoding='utf-8').read()
data = json.loads(raw_old)
before = {n['id']: dict(md=n['md'], chapters=list(n['chapters'])) for n in data}

# 5 条缺漏：(笔记id, 新章标题(纯文字), 正文markdown)
APPENDS = [
    ('线代2-矩阵', '补充：元素等于代数余子式相反数的对偶结论', r'''### 元素为代数余子式相反数的对偶结论 <!-- 源:777线代必背 p1 -->
与「$a_{ij}=A_{ij}\Rightarrow|A|=1$」成对记忆：设 $A$ 为 $3$ 阶非零矩阵，则
$$
a_{ij}=-A_{ij}\ (i,j=1,2,3)\ \Longleftrightarrow\ A^*=-A^{T}\ \Longleftrightarrow\ A^{T}A=E\ (A\text{ 正交})\ \Longrightarrow\ |A|=-1.
$$
- 推导：$a_{ij}=-A_{ij}$ 即 $A$ 等于代数余子式矩阵的相反数，故 $A^*=(A_{ij})^T=-A^T$；代入 $AA^*=|A|E$ 得 $-AA^T=|A|E$，即 $AA^T=-|A|E$。两边取行列式：$|A|^2=(-|A|)^3=-|A|^3$，即 $|A|^2(1+|A|)=0$；由 $A\neq O$（否则 $AA^T=O$ 逼出 $A=O$）排除 $|A|=0$，故 $|A|=-1$，代回得 $AA^T=E$，$A$ 正交。
- ⚠️ 对比：正号支 $a_{ij}=A_{ij}\Rightarrow|A|=1$，负号支 $a_{ij}=-A_{ij}\Rightarrow|A|=-1$，二者行列式符号相反，不能互推。'''),

    ('高数1-极限', '补充：函数图像的轴对称与中心对称判定', r'''### 一般轴对称与中心对称判定 <!-- 源:777高数必背 p3 -->
把奇偶性 $f(-x)=\pm f(x)$（即 $a=b=0$ 的特例）推广到任意对称轴 / 对称中心：
$$
\begin{aligned}
&\text{轴对称：}\ f(a+x)=f(b-x)\ \Longleftrightarrow\ f(x)\ \text{的对称轴为}\ x=\frac{a+b}{2},\\
&\text{中心对称：}\ f(a+x)+f(b-x)=c\ \Longleftrightarrow\ f(x)\ \text{的对称中心为}\ \Big(\frac{a+b}{2},\,\frac{c}{2}\Big).
\end{aligned}
$$
- 口诀：轴对称「自定和，函数等，相加除二对称轴」；中心对称「自定和，函相等，对称中心对半求」。
- 验证：令 $u=a+x$，则 $b-x=a+b-u$，轴对称式变 $f(u)=f(a+b-u)$，即关于 $x=\frac{a+b}{2}$ 对称；中心对称式变 $f(u)+f(a+b-u)=c$，即关于 $\big(\frac{a+b}{2},\frac c2\big)$ 中心对称。
- 用法：抽象函数给 $f(a+x)=f(b-x)$ 的条件，直接读出对称轴，再结合周期性可推更多对称轴；中心对称常与「$f(x)+f(2a-x)=2b$ 求积分」配合。'''),

    ('高数0-中学公式速查', '补充：三元完全平方与完全立方', r'''### 三元完全平方 / 完全立方 <!-- 源:777高数必背 p2 -->
二元 $(a\pm b)^2,(a\pm b)^3$ 的三元推广（配方、因式分解常用）：
$$
(a+b+c)^2=a^2+b^2+c^2+2ab+2ac+2bc,
$$
$$
(a-b+c)^2=a^2+b^2+c^2-2ab+2ac-2bc,
$$
$$
(a+b+c)^3=a^3+b^3+c^3+3a^2(b+c)+3b^2(a+c)+3c^2(a+b)+6abc.
$$
- 特例：$a+b+c=0$ 时 $(a+b+c)^3=0$ 给出 $a^3+b^3+c^3=3abc$（与线代真题点睛里的因式分解 $a^3+b^3+c^3-3abc=(a+b+c)(a^2+b^2+c^2-ab-bc-ca)$ 呼应）。
- 用途：三元二次型配方、$a^3+b^3+c^3-3abc$ 型因式分解的展开依据。'''),

    ('高数3.1-一元积分-计算', '补充：双参数点火公式（华里士推广）', r'''### 双参数点火公式华里士推广 <!-- 源:777高数必背 p9 -->
单参数 Wallis 公式的双参数推广（$a,b$ 为非负整数，$x\in[0,\frac\pi2]$）：
$$
\int_0^{\frac{\pi}{2}}\sin^{a}x\,\cos^{b}x\,\mathrm{d}x=
\begin{cases}
\dfrac{(a-1)!!\,(b-1)!!}{(a+b)!!}\cdot\dfrac{\pi}{2}, & a,b\ \text{全为偶数},\\[6pt]
\dfrac{(a-1)!!\,(b-1)!!}{(a+b)!!}, & a,b\ \text{不全为偶数}.
\end{cases}
$$
- 关键：**只有 $a,b$ 同为偶数时才乘 $\frac\pi2$**，只要有一个是奇数就不乘。
- 记号约定：$(-1)!!=0!!=1$。
- 退化：取 $b=0$（偶数）即回单参数 Wallis——$a$ 偶得 $\frac{(a-1)!!}{a!!}\cdot\frac\pi2$，$a$ 奇得 $\frac{(a-1)!!}{a!!}$；取 $a=b=1$ 得 $\int_0^{\pi/2}\sin x\cos x\,dx=\frac{0!!\,0!!}{2!!}=\frac12$。
- 注意：$b$ 为奇时也可用 $\int_0^{2\pi}\sin^a x\cos^b x\,dx=0$（$b$ 奇）等周期性结论，见「几何意义与高次幂处理」。'''),

    ('高数6-二重积分', '补充：关于平移对称轴的奇偶对称', r'''### 关于平移对称轴的奇偶对称 <!-- 源:777高数必背 p18 -->
把「关于坐标轴（$x=0,y=0$）对称看 $x,y$ 奇偶」推广到平移后的对称轴：若区域 $D$ 关于直线 $x=1$ 对称，则改看被积函数中 $x-1$ 的奇偶性：
$$
\iint_D f(x,y)\,d\sigma=
\begin{cases}
2\displaystyle\iint_{D_{x\ge 1}} f(x,y)\,d\sigma, & f(1+t,y)=f(1-t,y)\ (x-1\ \text{为偶}),\\[4pt]
0, & f(1+t,y)=-f(1-t,y)\ (x-1\ \text{为奇}).
\end{cases}
$$
关于 $y=1$ 对称同理，改看 $y-1$ 的奇偶性。
- 做法：把对称轴平移到新原点（令 $u=x-1$），再套用坐标轴对称的「偶倍奇零」。
- 与「轮换对称」区别：这里是**沿一条直线翻折**的偶倍奇零，轮换对称是 $x,y$ 互换后值不变，两者机理不同。'''),
]

seen = set()
for nid, title, body in APPENDS:
    note = next((n for n in data if n['id'] == nid), None)
    assert note is not None, '笔记不存在: ' + nid
    assert nid not in seen, '重复追加: ' + nid
    seen.add(nid)
    old_md = note['md']
    assert '$' not in title, '章标题不得含公式: ' + title
    assert title not in note['chapters'], '章标题重复: ' + nid
    # 严格前缀：只在末尾追加，绝不改已有字节
    sep = '' if old_md.endswith('\n\n') else ('\n' if old_md.endswith('\n') else '\n\n')
    block = sep + '## ' + title + '\n\n' + body.strip() + '\n'
    note['md'] = old_md + block
    note['chapters'].append(title)
    print('追加 %-22s 新章「%s」 md %d->%d chapters %d' % (
        nid, title, len(old_md), len(note['md']), len(note['chapters'])))

# 全局校验：只有 5 篇的 md/chapters 变了，且原内容是新内容严格前缀；其余字段与篇目一字未动
assert len(seen) == 5
others_untouched = 0
for n in data:
    nid = n['id']
    if nid not in seen:
        assert n['md'] == before[nid]['md'] and n['chapters'] == before[nid]['chapters'], '越界改动: ' + nid
        others_untouched += 1
    else:
        assert n['md'].startswith(before[nid]['md']), '原 md 非严格前缀: ' + nid
        assert n['chapters'][:-1] == before[nid]['chapters'], '原 chapters 被改: ' + nid
        for fld in ('id','subject','order','name','title'):
            assert n[fld] == next(x for x in data if x['id']==nid)[fld]
print('未触及笔记数', others_untouched, '| 追加篇数', len(seen))

# chapters ↔ ## 镜像：新增 5 篇必须通过；其余不得引入新的不符
# 注：线代4-线性方程组在 HEAD 既有 chapters(10)≠## (11) 的历史不符，与本次无关，仅放行此项。
import re
KNOWN_MISMATCH = {'线代4-线性方程组'}
unexpected = []
for n in data:
    h2 = [l[3:].split('<!--')[0].strip() for l in n['md'].split('\n') if l.startswith('## ')]
    if h2 == n['chapters']:
        continue
    if n['id'] in seen:
        raise AssertionError('本次追加的笔记镜像不符: %s' % n['id'])
    if n['id'] not in KNOWN_MISMATCH:
        unexpected.append(n['id'])
assert not unexpected, '引入新的镜像不符: %s' % unexpected
print('镜像校验通过：新增5篇全符合；仅放行 HEAD 既有的 线代4 历史不符')

# 写回：indent=2，无尾换行
out = json.dumps(data, ensure_ascii=False, indent=2)
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('写回完成，字节', len(out.encode('utf-8')))
