# -*- coding: utf-8 -*-
"""给「高数3.1-一元积分-计算」追加《变限积分》一章。

纪律：
- notes.json 格式 = json.dumps(indent=2, ensure_ascii=False)，无尾换行（已验 round-trip 完全一致）
- 只能追加到 md 末尾：annotate.js 的 sid = 笔记id#文档顺序，中间插入会让后面所有批注错位
- chapters 必须与正文 ## 逐个镜像
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'pwa', 'data', 'notes.json')
NID = '高数3.1-一元积分-计算'
CH = '变限积分'

APPEND = r"""
## 变限积分 <!-- 源:补充 -->

> 🎯 **本章定位**：前面「三大积分法 + 换元」解决「求得出原函数」的积分；本章解决**原函数求不出来（或不必求）**时怎么求导、求极限。存在性条件见「积分存在性 · ③ 变上限函数的连续 / 可导」，本节只讲**怎么算**。

### 1️⃣ 变上限积分函数

- **定义**：$F(x)=\int_a^x f(t)dt$（$a$ 为**常数**，$x$ 为**自变量**，$t$ 为**积分变量**）
  - 三个身份不能混：$x$ 是**求导变量**；$t$ 是**哑变量**（写成 $u$、$s$ 结果不变）；$a$ 是常数下限
  - ⚠️ $\int_0^x f(x)dt=xf(x)$，而 $\int_0^x f(t)dt\neq xf(x)$——前者被积函数与 $t$ 无关，后者的 $t$ 才是变量
- **三条基本结论**（$f$ 在讨论区间上）：
  - $f$ **可积** ⇒ $F(x)$ **连续**
  - $f$ **连续** ⇒ $F(x)$ **可导**，且 $F'(x)=f(x)$（**原函数存在定理**）
  - 因此变上限积分就是一个**具体的原函数**：$\int f(x)dx=\int_a^x f(t)dt+C$

### 2️⃣ ⭐⭐ 变限积分求导公式

- **一般式**（上下限都是函数，$f$ 连续）：
  $$\frac{d}{dx}\int_{\varphi(x)}^{\psi(x)}f(t)dt=f\left(\psi(x)\right)\psi'(x)-f\left(\varphi(x)\right)\varphi'(x)$$
  - 🧠 口诀：**上限代入乘上限导 − 下限代入乘下限导**
  - 本质是「复合函数求导 + 牛顿-莱布尼茨」两步合一

| 形式 | 求导结果 | 说明 |
| :--- | :--- | :--- |
| $\int_a^b f(t)dt$ | $0$ | 上下限都是常数，整体是常数 |
| $\int_a^x f(t)dt$ | $f(x)$ | 最基本形式，变量直接替换 |
| $\int_a^{\psi(x)}f(t)dt$ | $f\left(\psi(x)\right)\psi'(x)$ | 上限是复合函数，**别忘链式** |
| $\int_{\varphi(x)}^{\psi(x)}f(t)dt$ | $f\left(\psi\right)\psi'-f\left(\varphi\right)\varphi'$ | 上下限都动，注意减号 |

- ⚠️ 最高频失分：上限是 $x^2$ 忘乘 $2x$、上限是 $\sin x$ 忘乘 $\cos x$、下限是变量时**漏掉负号**

### 3️⃣ ⭐⭐⭐ 被积函数含 $x$：先分离，再求导

- **核心结论**：求导变量 $x$ 与积分变量 $t$ **必须先分离**，否则不能直接套上面的公式
- **两条路**：
  - **能提出就提**：$x$ 只以**乘积因子**形式出现 ⇒ 提到积分号外，再用乘积法则
  - **提不动就换元**：$x$ 藏在 $f(\cdot)$ **内部** ⇒ 换元把 $x$ 从被积函数里赶出去
  - 🧠 口诀：**含 $x$ 先分离，能提则提，提不动就换元**

**情形 A｜$x$ 是可提出的因子**

- $\int_0^x xf(t)dt=x\int_0^x f(t)dt$，求导要用**乘积法则**：
  $$\frac{d}{dx}\left[x\int_0^x f(t)dt\right]=\int_0^x f(t)dt+xf(x)$$
- ⚠️ 只有 $f(x)\cdot f(t)$ 这类**变量可分离**的形式能提；$f(x-t)$、$f(x+t)$、$f(xt)$ **提不出来**

**情形 B｜$x$ 在 $f(\cdot)$ 内部，必须换元**

| 原式 | 换元 | 换元后 |
| :--- | :--- | :--- |
| $\int_0^x f(x-t)dt$ | $u=x-t$，$dt=-du$ | $\int_0^x f(u)du$ |
| $\int_0^x f(x+t)dt$ | $u=x+t$，$dt=du$ | $\int_x^{2x}f(u)du$ |
| $\int_0^x f(xt)dt$ | $u=xt$，$dt=\frac{du}{x}$ | $\frac{1}{x}\int_0^{x^2}f(u)du$ |
| $\int_0^x tf(x-t)dt$ | $u=x-t$，$t=x-u$ | $x\int_0^x f(u)du-\int_0^x uf(u)du$ |

- ⚠️ 换元必须**三件套同步改**：被积函数、微分 $dt$、**上下限**（漏改上限最常见）
- 🔍 一眼判断新上限：$x-t$、$x+t$ 型**区间长度不变**（上限仍是 $x$ 或变为 $2x$）；$xt$、$x^2-t^2$ 型**区间被缩放**（上限变成 $x^2$）
- 例（平方上限）：$\int_0^x f(x^2-t^2)t\,dt$，令 $u=x^2-t^2$、$t\,dt=-\frac{du}{2}$ ⟹ $\frac12\int_0^{x^2}f(u)du$，求导得 $\frac12 f(x^2)\cdot 2x=xf(x^2)$

**情形 C｜上下限与被积函数同时含 $x$**

- 顺序不能颠倒：**先换元把 $x$ 从被积函数清掉 → 再套第 2 节的求导公式**
- 例：$\frac{d}{dx}\int_x^{2x}f(x-t)dt$，先令 $u=x-t$ ⟹ $\int_{-x}^{0}f(u)du$，再求导 $=0-f(-x)\cdot(-1)=f(-x)$

### 4️⃣ 高频构件：$\Phi(x)=\int_0^x(x-t)f(t)dt$

- **先展开再求导**（$x-t$ 可拆成两项乘积，不必换元）：
  $$\Phi(x)=x\int_0^x f(t)dt-\int_0^x tf(t)dt$$
  $$\Phi'(x)=\int_0^x f(t)dt+xf(x)-xf(x)=\int_0^x f(t)dt$$
  $$\Phi''(x)=f(x)$$
- 🧠 结论一句话：**被积函数里 $(x-t)$ 的次数 = 求导后要「多求几阶」**——每消掉一层就多求一次导
  - 0 次：$\frac{d}{dx}\int_0^x f(t)dt=f(x)$
  - 1 次：$\Phi'(x)=\int_0^x f(t)dt$，$\Phi''(x)=f(x)$
  - 2 次：$\Phi(x)=\int_0^x(x-t)^2f(t)dt$ ⟹ $\Phi'''(x)=2f(x)$
- **用途**：$\Phi'(0)=0$ 且 $\Phi''(0)=f(0)$ ⇒ 直接用极值**第二充分条件**；$f>0$ ⇒ $\Phi''>0$ ⇒ $\Phi$ 是凹函数

### 5️⃣ 变限积分的极限（洛必达 + 等价无穷小）

- **标准套路**：验 $\frac{0}{0}$ 型 → 洛必达（分子用求导公式）→ 化简 → 必要时再上等价无穷小
  - 例：$\lim\limits_{x\to0}\frac{\int_0^x\ln(1+t^2)dt}{x^3}=\lim\limits_{x\to0}\frac{\ln(1+x^2)}{3x^2}=\lim\limits_{x\to0}\frac{x^2}{3x^2}=\frac13$
- **等价无穷小直达式**（$f$ 连续）：
  - $f(0)\neq0$ ⇒ $\int_0^x f(t)dt\sim f(0)\,x$
  - 复合上限推广：$\varphi(x)\to0$ 时 $\int_0^{\varphi(x)}f(t)dt\sim f(0)\varphi(x)$
  - $f(0)=0$ 时降一阶：$\int_0^x f(t)dt\sim\frac{f'(0)}{2}x^2$
- **通用手法**：被积函数先等价替换再积分。$f(t)\sim g(t)\ (t\to0)$ 且 $g$ 不变号 ⟹ $\int_0^x f(t)dt\sim\int_0^x g(t)dt$
  - 例：$\int_0^x\ln(1+t)dt\sim\int_0^x t\,dt=\frac{x^2}{2}$
- ⚠️ 洛必达前必须验型；求导后若仍含变限积分可再洛一次
- ⚠️ 不可把 $f(t)$ 直接换成 $f(0)$ 当常数再积分（仅 $f(0)\neq0$ 且只求首项时才等价）

### 6️⃣ 变限积分的奇偶性

- **结论**（下限必须为 $0$）：
  - $f$ **偶** ⇒ $F(x)=\int_0^x f(t)dt$ 是**奇函数**
  - $f$ **奇** ⇒ $F(x)=\int_0^x f(t)dt$ 是**偶函数**
- 🧠 记忆：**求导与积分都让奇偶性「翻转一档」**，偶 ↔ 奇
- ⚠️ 下限不是 $0$ 时不成立：$f$ 偶时 $\int_1^x f(t)dt$ 是「奇函数 + 常数」，既非奇也非偶

### 7️⃣ 易错点总表

- ⚠️ **忘乘上限导数**：$\psi(x)=x^2$、$\sin x$、$e^x$ 都要乘各自的导数
- ⚠️ **被积函数含 $x$ 直接套公式**：$f(x-t)$、$f(xt)$ 必须先换元或拆项
- ⚠️ **换元漏改上下限**，尤其上限从 $x$ 变成 $x^2$、$2x$
- ⚠️ **下限项写成加号**：公式是 $f(\psi)\psi'-f(\varphi)\varphi'$
- ⚠️ **$x$ 与 $t$ 混用**：$\int_0^x f(x)dt=xf(x)$ 是「$x$ 乘常数」，不是变限函数
- ⚠️ **前提条件缺失**：被积函数在 $[a,x]$ 上连续才可直接用公式；有间断点要分段或按定义求导
- ⚠️ **洛必达未验型**，或求导时漏掉分母的导数

### 8️⃣ 进阶：含参变限积分的求导

::: fold 莱布尼茨公式（数二不直接考，理解「三项来源」用）
- 当被积函数也含 $x$（$f=f(x,t)$）时：
  $$\frac{d}{dx}\int_{\varphi(x)}^{\psi(x)}f(x,t)dt=f\left(x,\psi(x)\right)\psi'(x)-f\left(x,\varphi(x)\right)\varphi'(x)+\int_{\varphi(x)}^{\psi(x)}\frac{\partial f}{\partial x}(x,t)dt$$
- 三项来源：**上限项 − 下限项 + 内部偏导项**；$f$ 不含 $x$ 时第三项为 $0$，退化为第 2 节的一般式
- 这也是「被积函数含 $x$ 先换元」的**理论兜底**：换元后 $x$ 不再出现在被积函数内部，第三项自然消失
:::

- 🔗 相关：反常积分的收敛判别见「反常积分」篇；变限积分构成的等式证明常在「真题点睛」出现（构造 $\Phi(x)=\int_0^x f(t)dt$ 后用单调性/介值）
"""


def main():
    raw = io.open(P, encoding='utf-8').read()
    data = json.loads(raw)
    assert json.dumps(data, indent=2, ensure_ascii=False) == raw, 'round-trip 不一致，禁止写入'

    note = None
    for it in data:
        if it['id'] == NID:
            note = it
            break
    assert note is not None, '找不到笔记 ' + NID

    md = note['md']
    assert CH not in note['chapters'], '章节已存在，勿重复追加'
    assert '\n## ' + CH not in md, '正文已有该章，勿重复追加'

    note['md'] = md + APPEND
    note['chapters'].append(CH)

    out = json.dumps(data, indent=2, ensure_ascii=False)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(out)
    print('已追加：%s' % CH)
    print('chapters %d -> %d，md %d -> %d 字符' % (
        len(note['chapters']) - 1, len(note['chapters']), len(md), len(note['md'])))


if __name__ == '__main__':
    main()
