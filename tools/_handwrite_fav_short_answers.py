# -*- coding: utf-8 -*-
"""手写「收藏∩不会/不熟∩未抽」池子里真正答案简略/跳步严重的题。

筛选口径：26 道候选中，多数答案已含完整推导（200+ 字），强行重写只会改坏。
只重写以下 7 类典型简略题：
  DG900JXB-333  特征多项式一句带过，行列式展开全缺
  DG900JXB-1370 球形抽水：idea 直接复制 answer，积分计算未展开
  DG900JXB-1115 变量代换微分方程：换元求导过程（本题考点）全缺
  DG900JXB-1371 半球抽水：idea=answer，积分未展开
  core-269      反常积分：分部积分与后续积分全跳
  DG900JXB-1362 三角板水压力：idea=answer，变化率推导跳步
  core-288      不定积分：法二万能代换无展开、法一未落到结果

多副本题（core+dgy）两副本写同样的详细答案；idea=answer 的题同时重写 idea 为步骤概括。
只覆盖 answer / idea，绝不改 stem/options/kind。
写回格式：core_bank.json=indent=1 无尾换行；dgy_items.json=单行紧凑无尾换行。
"""
import json, io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')


def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)


def save(fn, obj, indent=None):
    txt = json.dumps(obj, ensure_ascii=False, indent=indent)
    with io.open(os.path.join(DATA, fn), 'w', encoding='utf-8', newline='') as f:
        f.write(txt)


def index_papers(obj):
    idx = {}
    papers = obj if isinstance(obj, list) else obj.get('papers', [])
    for p in papers:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                idx[(p.get('id'), str(q.get('no')))] = q
    return idx


# ===== 详细答案正文（raw string 保留 LaTeX 单反斜杠）=====
A333 = r'''特征多项式直接算：
$$
|\lambda E-A|=\begin{vmatrix}\lambda-1&-4&7\\-2&\lambda-8&12\\-3&-12&\lambda+17\end{vmatrix}.
$$
按第一行展开：三个余子式依次为 $(\lambda-8)(\lambda+17)+144=\lambda^2+9\lambda+8$、$(-2)(\lambda+17)+36=-2\lambda+2$、$24+3(\lambda-8)=3\lambda$，故
$$
|\lambda E-A|=(\lambda-1)(\lambda^2+9\lambda+8)+4(-2\lambda+2)+7\cdot3\lambda
=\lambda^3+8\lambda^2+12\lambda=\lambda(\lambda+2)(\lambda+6).
$$
解 $|\lambda E-A|=0$ 得特征值 $0,-2,-6$，其中最小的是 $-6$。'''

A1370 = r'''以球心为原点、竖直向上为 $y$ 轴，则水面（顶部）在 $y=R$，球体范围为 $-R\le y\le R$。在高度 $y$ 处取厚度为 $\mathrm{d}y$ 的水平薄层：此处截面半径 $\sqrt{R^2-y^2}$，截面积 $S(y)=\pi(R^2-y^2)$，薄层重量 $\rho g\pi(R^2-y^2)\mathrm{d}y$；把这层水抽到顶部需提升 $R-y$，故功元 $\mathrm{d}W=\rho g(R-y)\pi(R^2-y^2)\mathrm{d}y$，总功
$$
W=\rho g\int_{-R}^{R}(R-y)\pi(R^2-y^2)\,\mathrm{d}y.
$$
展开 $(R-y)(R^2-y^2)=R^3-R^2y-Ry^2+y^3$。对称区间 $[-R,R]$ 上奇函数项 $-R^2y,\,y^3$ 的积分为零，故
$$
W=\rho g\pi\int_{-R}^{R}(R^3-Ry^2)\,\mathrm{d}y
=\rho g\pi\left(2R^4-\frac{2R^4}{3}\right)
=\frac{4}{3}\pi\rho gR^4.
$$'''

A1115 = r'''令 $x=\sin t\ \left(-\frac{\pi}{2}\lt t\lt\frac{\pi}{2}\right)$，记 $Y(t)=y(\sin t)$，则 $t=\arcsin x$，且 $\dfrac{\mathrm{d}t}{\mathrm{d}x}=\dfrac{1}{\cos t}$。由链式法则
$$
y'=\frac{\mathrm{d}Y}{\mathrm{d}t}\cdot\frac{\mathrm{d}t}{\mathrm{d}x}=\frac{Y'}{\cos t},
$$
$$
y''=\frac{\mathrm{d}}{\mathrm{d}x}\Big(\frac{Y'}{\cos t}\Big)
=\frac{\mathrm{d}}{\mathrm{d}t}\Big(\frac{Y'}{\cos t}\Big)\frac{\mathrm{d}t}{\mathrm{d}x}
=\frac{Y''\cos t+Y'\sin t}{\cos^2t}\cdot\frac{1}{\cos t}
=\frac{Y''\cos t+Y'\sin t}{\cos^3t}.
$$
代入 $(1-x^2)y''-xy'-4y=0$，并用 $1-x^2=\cos^2t,\ x=\sin t$：
$$
\cos^2t\cdot\frac{Y''\cos t+Y'\sin t}{\cos^3t}-\sin t\cdot\frac{Y'}{\cos t}-4Y
=\frac{Y''\cos t+Y'\sin t}{\cos t}-\frac{Y'\sin t}{\cos t}-4Y
=Y''-4Y=0.
$$
故方程化为 $Y''-4Y=0$，通解 $Y=A\mathrm{e}^{2t}+B\mathrm{e}^{-2t}$，即
$$
y=A\mathrm{e}^{2\arcsin x}+B\mathrm{e}^{-2\arcsin x}.
$$
$x=0$ 对应 $t=0$：由 $y(0)=Y(0)=A+B=1$；又 $y'(0)=\dfrac{Y'(0)}{\cos0}=Y'(0)=2A-2B=6$，即 $A-B=3$。联立得 $A=2,\ B=-1$，所求特解
$$
y=2\mathrm{e}^{2\arcsin x}-\mathrm{e}^{-2\arcsin x}.
$$'''

A1371 = r'''以 $y$ 记水面以下的深度（$0\le y\le4$）。半球半径为 $4$、球心在原水面处，故深度 $y$ 处水平截面半径 $r$ 满足 $r^2+y^2=16$，截面积 $S(y)=\pi(16-y^2)$，薄层体积 $\pi(16-y^2)\mathrm{d}y$、重量 $\rho g\pi(16-y^2)\mathrm{d}y$。该层位于水面下 $y$ 米，要抽到水面上方 $6$ 米，提升距离为 $6+y$，故
$$
W=\rho g\int_0^4(16-y^2)(6+y)\,\mathrm{d}y
=1000\times9.8\times3.14\int_0^4(16-y^2)(6+y)\,\mathrm{d}y.
$$
展开 $(16-y^2)(6+y)=96+16y-6y^2-y^3$，逐项积分：
$$
\int_0^4(96+16y-6y^2-y^3)\,\mathrm{d}y
=\left[96y+8y^2-2y^3-\frac{y^4}{4}\right]_0^4
=384+128-128-64=320.
$$
于是 $W=1000\times9.8\times3.14\times320=9847040\ \mathrm{J}$。'''

A269 = r'''先把被积函数化简：分子分母同乘 $\mathrm{e}^{2x}$，
$$
\frac{\mathrm{e}^{-x}}{(1+\mathrm{e}^{-x})^2}=\frac{\mathrm{e}^{x}}{(1+\mathrm{e}^{x})^2},
$$
故 $I=\displaystyle\int_0^{+\infty}\frac{x\,\mathrm{e}^{x}}{(1+\mathrm{e}^{x})^2}\,\mathrm{d}x$。注意到
$$
\left(\frac{1}{1+\mathrm{e}^{x}}\right)'=-\frac{\mathrm{e}^{x}}{(1+\mathrm{e}^{x})^2},
$$
分部积分（取 $u=x$，$\mathrm{d}v=\dfrac{\mathrm{e}^{x}}{(1+\mathrm{e}^{x})^2}\mathrm{d}x=-\mathrm{d}\big(\frac{1}{1+\mathrm{e}^{x}}\big)$）：
$$
I=-\left[\frac{x}{1+\mathrm{e}^{x}}\right]_0^{+\infty}+\int_0^{+\infty}\frac{\mathrm{d}x}{1+\mathrm{e}^{x}}.
$$
边界项：$x\to+\infty$ 时 $\dfrac{x}{1+\mathrm{e}^{x}}\to0$，$x=0$ 时为 $0$，故为零。对余下积分令 $t=\mathrm{e}^{-x}$，则 $\mathrm{d}x=-\dfrac{\mathrm{d}t}{t}$，$\dfrac{1}{1+\mathrm{e}^{x}}=\dfrac{t}{1+t}$，
$$
\int_0^{+\infty}\frac{\mathrm{d}x}{1+\mathrm{e}^{x}}=\int_1^{0}\frac{t}{1+t}\left(-\frac{\mathrm{d}t}{t}\right)=\int_0^1\frac{\mathrm{d}t}{1+t}=\big[\ln(1+t)\big]_0^1=\ln2.
$$
故 $I=\ln2$。'''

A1362 = r'''边长为 $2$ 的等边三角形高 $h=\sqrt3$。以 $y$ 记从水面向下的深度（$0\le y\le\sqrt3$），深度 $y$ 处板的水平宽度 $w(y)=2\left(1-\dfrac{y}{\sqrt3}\right)$（顶部为 $2$、底部顶点为 $0$）。

$(1)$ 深度 $y$ 处压强 $\rho gy$，压力元 $\mathrm{d}P=\rho gy\,w(y)\mathrm{d}y$，故板一侧所受水压力
$$
P=\rho g\int_0^{\sqrt3}y\cdot2\left(1-\frac{y}{\sqrt3}\right)\mathrm{d}y
=2\rho g\left[\frac{y^2}{2}-\frac{y^3}{3\sqrt3}\right]_0^{\sqrt3}
=2\rho g\left(\frac{3}{2}-1\right)=\rho g.
$$

$(2)$ 设水面上升了 $s$（$\dfrac{\mathrm{d}s}{\mathrm{d}t}=0.1$）。板固定不动，板上距顶部为 $y$ 处的深度由 $y$ 变为 $y+s$，于是
$$
P(s)=\rho g\int_0^{\sqrt3}(y+s)\,w(y)\,\mathrm{d}y
=\rho g\int_0^{\sqrt3}y\,w(y)\mathrm{d}y+\rho g\,s\int_0^{\sqrt3}w(y)\mathrm{d}y.
$$
第一项即 $(1)$ 中的 $\rho g$；第二项中 $\displaystyle\int_0^{\sqrt3}w(y)\mathrm{d}y$ 正是三角板面积 $\dfrac{1}{2}\times2\times\sqrt3=\sqrt3$。故
$$
P(s)=\rho g+\sqrt3\,\rho g\,s,\qquad
\frac{\mathrm{d}P}{\mathrm{d}t}=\frac{\mathrm{d}P}{\mathrm{d}s}\cdot\frac{\mathrm{d}s}{\mathrm{d}t}=\sqrt3\,\rho g\times0.1=0.1\sqrt3\,\rho g.
$$'''

A288 = r'''法一（共轭化）：分子分母同乘 $1-\sin x$，
$$
\int\frac{\mathrm{d}x}{1+\sin x}=\int\frac{1-\sin x}{1-\sin^2x}\mathrm{d}x
=\int\frac{1-\sin x}{\cos^2x}\mathrm{d}x
=\int(\sec^2x-\sec x\tan x)\,\mathrm{d}x
=\tan x-\sec x+C.
$$

法二（万能代换）：令 $t=\tan\dfrac{x}{2}$，则 $\sin x=\dfrac{2t}{1+t^2}$，$\mathrm{d}x=\dfrac{2}{1+t^2}\mathrm{d}t$，且
$$
1+\sin x=1+\frac{2t}{1+t^2}=\frac{(1+t)^2}{1+t^2},
$$
故
$$
\int\frac{\mathrm{d}x}{1+\sin x}=\int\frac{2/(1+t^2)}{(1+t)^2/(1+t^2)}\mathrm{d}t
=\int\frac{2\,\mathrm{d}t}{(1+t)^2}=-\frac{2}{1+t}+C=-\frac{2}{1+\tan\frac{x}{2}}+C.
$$
两结果等价：$\tan\left(\dfrac{x}{2}-\dfrac{\pi}{4}\right)=\dfrac{t-1}{t+1}=1-\dfrac{2}{1+t}$，故 $-\dfrac{2}{1+t}$ 与 $\tan\left(\dfrac{x}{2}-\dfrac{\pi}{4}\right)$ 只差常数；三者同为原函数。'''

# ===== idea=answer 的题，重写为步骤概括 =====
I1370 = r'''① 以球心为原点建 $y$ 轴，高度 $y$ 处截面积 $\pi(R^2-y^2)$、提升距离 $R-y$；② 按功元 $\rho g(R-y)\pi(R^2-y^2)\mathrm{d}y$ 从 $-R$ 积到 $R$；③ 展开被积式，借奇偶性去掉奇函数项，积出 $\frac{4}{3}\pi\rho gR^4$。'''

I1115 = r'''① 令 $x=\sin t$，用链式法则得 $y'=\frac{Y'}{\cos t}$、$y''=\frac{Y''\cos t+Y'\sin t}{\cos^3t}$；② 借 $1-x^2=\cos^2t$ 代入原方程，含 $Y'\sin t$ 的两项抵消，化为 $Y''-4Y=0$；③ 写通解，由 $y(0)=1,\ y'(0)=6$（$x=0\Leftrightarrow t=0$）定出 $A=2,B=-1$。'''

I1371 = r'''① 以深度 $y$ 为变量，由 $r^2+y^2=16$ 得截面积 $\pi(16-y^2)$，提升距离 $6+y$；② 列功的积分 $W=\rho g\int_0^4(16-y^2)(6+y)\mathrm{d}y$；③ 展开被积式逐项积分得 $320$，代入 $\rho=1000,g=9.8,\pi=3.14$ 算出 $9847040\ \mathrm{J}$。'''

I1362 = r'''① 边长 $2$ 的等边三角形高 $\sqrt3$，深度 $y$ 处板宽 $w(y)=2(1-y/\sqrt3)$；② 由压强 $\rho gy$ 写压力元并积分得 (1) $P=\rho g$；③ 水面上升 $s$ 后各点深度加 $s$，$P(s)=\rho g+\rho g s S$，$S=\sqrt3$ 为板面积，故 $\frac{\mathrm{d}P}{\mathrm{d}t}=\sqrt3\rho g\cdot0.1$。'''

# 各源答案前缀风格：core 库这些题原答案无【答案】头，dgy 库原题有
H = '【答案】'
#  PLAN: (file, (paperId, no), new_answer, new_idea 或 None)
PLAN = [
    ('dgy',  ('DG900JXB', '333'),  H + '$-6$\n\n' + A333,   None),
    ('core', ('core', '736'),      '$-6$\n\n' + A333,       None),
    ('dgy',  ('DG900JXB', '1370'), H + '$\\dfrac{4}{3}\\pi\\rho gR^4$\n\n' + A1370, I1370),
    ('core', ('core', '1361'),     '$\\dfrac{4}{3}\\pi\\rho gR^4$\n\n' + A1370, I1370),
    ('dgy',  ('DG900JXB', '1115'), H + '化为 $Y\'\'-4Y=0$；特解为 $y=2\\mathrm{e}^{2\\arcsin x}-\\mathrm{e}^{-2\\arcsin x}$。\n\n' + A1115, I1115),
    ('core', ('core', '1362'),     H + '$9847040\\ \\mathrm{J}$\n\n' + A1371, I1371),
    ('dgy',  ('DG900JXB', '1371'), H + '$9847040\\ \\mathrm{J}$\n\n' + A1371, I1371),
    ('core', ('core', '269'),      '$\\ln2$\n\n' + A269,    None),
    ('core', ('core', '1353'),     H + '$(1)\\ \\rho g$；$(2)\\ 0.1\\sqrt3\\,\\rho g$。\n\n' + A1362, I1362),
    ('dgy',  ('DG900JXB', '1362'), H + '$(1)\\ \\rho g$；$(2)\\ 0.1\\sqrt3\\,\\rho g$。\n\n' + A1362, I1362),
    ('core', ('core', '288'),      '$\\tan x-\\sec x+C$\n\n' + A288, None),
]

core = load('core_bank.json')
dgy = load('dgy_items.json')
core_bak = load('core_bank.json.bak_20261120_hwans')
dgy_bak = load('dgy_items.json.bak_20261120_hwans')
idx = {'core': index_papers(core), 'dgy': index_papers(dgy)}
ibak = {'core': index_papers(core_bak), 'dgy': index_papers(dgy_bak)}

seen = set()
for fname, key, new_ans, new_idea in PLAN:
    q = idx[fname][key]
    old = ibak[fname][key]
    # 题干/选项/类型绝不能被改
    for fld in ('stem', 'options', 'kind', 'no'):
        assert q.get(fld) == old.get(fld), '%s %s 字段 %s 与备份不符' % (fname, key, fld)
    assert len(new_ans) > len(str(old.get('answer') or '')), '新答案反而更短 %s %s' % (fname, key)
    q['answer'] = new_ans
    if new_idea is not None:
        q['idea'] = new_idea
    seen.add((fname, key))
    print('%-5s %-22s ans %4d->%4d idea %s' % (
        fname, str(key), len(str(old.get('answer') or '')), len(new_ans),
        ('%4d->%4d' % (len(str(old.get('idea') or '')), len(new_idea))) if new_idea else 'keep'))

# 全局：除 PLAN 里的题外，任何题都不许变
for fname, cur, bak in [('core', core, core_bak), ('dgy', dgy, dgy_bak)]:
    ci, bi = index_papers(cur), index_papers(bak)
    assert ci.keys() == bi.keys(), fname + ' 题目数量变化'
    changed = [k for k in ci if ci[k] != bi[k]]
    unexpected = [k for k in changed if (fname, k) not in seen]
    assert not unexpected, '%s 出现越界改动: %s' % (fname, unexpected)
    print('%s 实际改动题数=%d 全部在计划内' % (fname, len(changed)))

save('core_bank.json', core, indent=1)
save('dgy_items.json', dgy, indent=None)
print('写回完成，计划题对=%d（含多副本）' % len(seen))
