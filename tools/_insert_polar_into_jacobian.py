# -*- coding: utf-8 -*-
"""把「极坐标换元策略判断法则」插到高数6「换元法：雅可比行列式」章顶部。
不新增 ## 章 → chapters 不变；批注锚点 #0/#24/#34 均在插入点(块58)之前，不受影响。
"""
import io, json, sys

P = 'pwa/data/notes.json'
raw = io.open(P, encoding='utf-8').read()
data = json.loads(raw)
note = next(n for n in data if n['id'] == '高数6-二重积分')
md0 = note['md']

MARK = '## 换元法：雅可比行列式 <!-- 源:p3 -->'
assert md0.count(MARK) == 1, '换元法章标题不唯一: %d' % md0.count(MARK)
assert '极坐标换元策略判断法则' not in md0, '已插入过，避免重复'

INSERT = r'''### 极坐标换元策略判断法则：展开后看常数项 <!-- 源:777高数必背 p4 -->

遇到「积分区域是圆（或圆的一部分）」的二重积分，先不要急着问要不要换元，而是把圆的方程**展开**，看常数项是否为零——这一步直接决定极坐标好不好用：

| 圆的类型 | 直角坐标方程特征 | 展开化简后的核心 | 代入极坐标后的极径 $r$ | 推荐做法 |
| --- | --- | --- | --- | --- |
| 标准圆（圆心在原点） | $x^2+y^2\le R^2$ | 无一次项 | $r\le R$ | 直接极坐标 |
| 过原点的圆 | $(x-a)^2+y^2\le a^2$；一般地 $(x-a)^2+(y-b)^2\le R^2$ 且 $a^2+b^2=R^2$ | 常数项抵消：$x^2+y^2\le 2ax+2by$ | $r\le 2(a\cos\theta+b\sin\theta)$，极径**一次式直接解出** | 直接极坐标（**不要换元**） |
| 不过原点的圆 | $(x-a)^2+(y-b)^2\le R^2,\ a^2+b^2\neq R^2$ | 常数项不消：$x^2+y^2\le 2ax+2by+C\ (C\neq0)$ | $r^2-2r(a\cos\theta+b\sin\theta)-C\le0$，解 $r$ 要**二次求根加判别式** | 平移换元 或 展开利用对称性 |

**判定口诀**：**过原点 ⇒ 无常数项 ⇒ 能约掉公因式 $r$ ⇒ 直接极坐标；不过原点 ⇒ 有常数项 ⇒ $r$ 变成二次不等式 ⇒ 先平移换元。** 过原点的圆是极坐标换元的「天选之子」。

> 为什么过原点就能直接解？代入 $x=r\cos\theta,\ y=r\sin\theta$，方程变成 $r^2-2r(a\cos\theta+b\sin\theta)\le0$，**公因式 $r$ 可以约掉**（$r=0$ 只是原点一个点），于是 $r$ 的一次不等式立刻解出。不过原点时常数项 $C\neq0$，$r^2$ 与常数项无法同时约去，只能解二次不等式。

### 例一：过原点的圆直接极坐标（不要换元） <!-- 源:777高数必背 p4 -->

$D:x^2+y^2\le2x$（即 $(x-1)^2+y^2\le1$，圆心 $(1,0)$、半径 1，**过原点**），求 $I=\displaystyle\iint_D\sqrt{x^2+y^2}\,d\sigma$。

- **换元前（直角坐标）**：$x$ 从 $0$ 到 $2$，$y$ 从 $-\sqrt{2x-x^2}$ 到 $\sqrt{2x-x^2}$，被积 $\sqrt{x^2+y^2}$，被积函数与积分限都带根号，几乎积不动。
- **判断**：展开 $x^2+y^2-2x\le0$，常数项为零 ⇒ 过原点 ⇒ 直接极坐标，**不做平移**。
- **换元后（极坐标）**：$r^2\le2r\cos\theta\Rightarrow 0\le r\le2\cos\theta,\ -\dfrac\pi2\le\theta\le\dfrac\pi2$，且 $\sqrt{x^2+y^2}=r,\ d\sigma=r\,drd\theta$：
$$
I=\int_{-\pi/2}^{\pi/2}d\theta\int_0^{2\cos\theta}r\cdot r\,dr
=\frac83\int_{-\pi/2}^{\pi/2}\cos^3\theta\,d\theta
=\frac83\cdot\frac43=\frac{32}{9}.
$$
（其中 $\displaystyle\int_{-\pi/2}^{\pi/2}\cos^3\theta\,d\theta=2\cdot\frac23=\frac43$，用点火公式。）

**反面提醒**：此题若画蛇添足令 $u=x-1$，区域变成 $u^2+y^2\le1$，但被积变成 $\sqrt{(u+1)^2+y^2}$，反而更难——**过原点的圆不要平移换元**。

### 例二：不过原点的圆先平移换元 <!-- 源:真题点睛 2009·19 -->

$D:(x-1)^2+(y-1)^2\le1$（圆心 $(1,1)$、半径 1，$1^2+1^2=2\neq1$，**不过原点**），求 $I=\displaystyle\iint_D(x-y)\,d\sigma$。

- **换元前（硬套极坐标）**：展开得 $x^2+y^2\le2x+2y-1$，即 $C=-1\neq0$；代入极坐标：
$$
r^2-2r(\cos\theta+\sin\theta)+1\le0
\Rightarrow r\le(\cos\theta+\sin\theta)+\sqrt{(\cos\theta+\sin\theta)^2-1},
$$
还要讨论判别式 $(\cos\theta+\sin\theta)^2\ge1$ 来定 $\theta$ 范围——**极苦，这就是不过原点别硬上极坐标的原因**。
- **判断**：常数项 $C\neq0$ ⇒ 不过原点 ⇒ 先把圆心搬到原点。
- **换元后（平移）**：令 $u=x-1,\ v=y-1$，则 $J=1$，$D':u^2+v^2\le1$，被积 $x-y=u-v$。$D'$ 关于 $u=v$ 对称，而 $u-v$ 在交换 $u\leftrightarrow v$ 下变号（轮换对称的奇函数）：
$$
I=\iint_{D'}(u-v)\,dudv=0.
$$
**三行结束**。这就是真题点睛里 2009·19 的套路：圆域不过原点时，先平移到原点，剩下的交给对称性。

### 易错提醒与口诀 <!-- 源:777高数必背 p4 -->

- **别凭「看着像圆」就换元**：先展开看常数项——过原点才有约掉 $r$ 的便宜。
- **过原点却去平移**：被积函数被平移搞复杂（例一的反面）。
- **不过原点却硬套极坐标**：$r$ 变成二次不等式，判别式加根号，计算量暴涨（例二）。
- **「展开利用对称性」是不不过原点的另一条路**：若被积函数展开后能写成关于某条直线（如 $x=1$）的奇函数，直接偶倍奇零，连平移都不用写——见前面「补充：关于平移对称轴的奇偶对称」。

'''

new_md = md0.replace(MARK, MARK + '\n' + INSERT, 1)
note['md'] = new_md
# chapters 不变（未加 ## 章）
out = json.dumps(data, ensure_ascii=False, indent=2)
io.open(P, 'w', encoding='utf-8', newline='').write(out)

# 验证：去掉插入段后严格等于原 md
assert new_md.replace('\n' + INSERT, '', 1) == md0, '原文被破坏（非纯插入）'
assert note['chapters'] == next(n for n in json.loads(raw) if n['id'] == '高数6-二重积分')['chapters'], 'chapters 被改'
print('插入完成 | 新增 %d 字 | chapters 数 %d 不变' % (len(new_md) - len(md0), len(note['chapters'])))
print('插入点：换元法章标题正下方，原文完整保留')
