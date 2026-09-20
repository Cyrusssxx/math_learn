# -*- coding: utf-8 -*-
# 批次9：268/274 整体重排为规范块结构（内容不变，中文行独立、公式块独立）
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = 'pwa/data/core_bank.json'

def load():
    with open(SRC, encoding='utf-8') as f:
        return json.load(f)

def find_q(data, no):
    for s in data[0]['sections']:
        for q in s['questions']:
            if str(q['no']) == str(no):
                return q
    return None

NEW_268 = """【答案】
$$
\\int\\frac{xe^x}{\\sqrt{e^x-1}} dx = 2(x - 2)\\sqrt{e^x - 1} + 4\\arctan(\\sqrt{e^x - 1}) + C
$$

这是一道非常经典的微积分题目，综合考察了无理代换和分部积分。整体思路是先通过换元去掉根号，再利用分部积分法处理多项式与对数函数的乘积。

以下是详细的求解步骤：

### **第一步：根式换元**

为了消除分母中的根号，我们令 $t = \\sqrt{e^x - 1}$。

由此可以推导出：
* 两边平方：$t^2 = e^x - 1$
* 解出 $e^x$：$e^x = t^2 + 1$
* 解出 $x$：$x = \\ln(t^2 + 1)$
* 对 $e^x = t^2 + 1$ 两边求微分，得到：$e^x dx = 2t dt$

将这些式子代入原积分中：
$$
\\int\\frac{x}{\\sqrt{e^x-1}} (e^x dx) = \\int \\frac{\\ln(t^2 + 1)}{t} (2t dt)
$$

化简后，积分转化为：
$$
2 \\int \\ln(t^2 + 1) dt
$$

---

### **第二步：分部积分**

现在我们需要求解 $\\int \\ln(t^2 + 1) dt$。由于被积函数是对数函数，通常将被积函数看作 $1 \\cdot \\ln(t^2 + 1)$，并使用分部积分法 ($\\int u dv = uv - \\int v du$)。

令：
* $u = \\ln(t^2 + 1)$，则 $du = \\frac{2t}{t^2 + 1} dt$
* $dv = dt$，则 $v = t$

应用分部积分公式：
$$
2 \\int \\ln(t^2 + 1) dt = 2 \\left[ t \\ln(t^2 + 1) - \\int t \\cdot \\frac{2t}{t^2 + 1} dt \\right]
$$

$$
= 2t \\ln(t^2 + 1) - 4 \\int \\frac{t^2}{t^2 + 1} dt
$$

对于右侧的积分，我们可以通过“加一减一”的技巧将被积函数化为真分式：
$$
\\int \\frac{t^2}{t^2 + 1} dt = \\int \\frac{(t^2 + 1) - 1}{t^2 + 1} dt = \\int \\left( 1 - \\frac{1}{t^2 + 1} \\right) dt
$$

$$
= t - \\arctan(t)
$$

将这个结果代回原式：
$$
2 \\int \\ln(t^2 + 1) dt = 2t \\ln(t^2 + 1) - 4(t - \\arctan(t)) + C
$$

$$
= 2t \\ln(t^2 + 1) - 4t + 4\\arctan(t) + C
$$

---

### **第三步：回代变量**

最后，将 $t = \\sqrt{e^x - 1}$ 以及 $\\ln(t^2 + 1) = x$ 代回上式中：
$$
= 2\\sqrt{e^x - 1} \\cdot x - 4\\sqrt{e^x - 1} + 4\\arctan(\\sqrt{e^x - 1}) + C
$$

提取公因式稍作整理，最终结果为：
$$
\\int\\frac{xe^x}{\\sqrt{e^x-1}} dx = 2(x - 2)\\sqrt{e^x - 1} + 4\\arctan(\\sqrt{e^x - 1}) + C
$$

*(其中 $C$ 为积分常数)*
"""

NEW_274 = """【答案】
$$
\\int e^{2x}\\arctan\\sqrt{e^x-1}dx = \\frac{1}{2}e^{2x}\\arctan\\sqrt{e^x-1} - \\frac{e^x+2}{6}\\sqrt{e^x-1} + C
$$

这个问题可以通过**换元法**和**分部积分法**来解决。关键在于先通过换元消去复杂的指数根式，再利用分部积分处理反三角函数。

以下是详细步骤：

### 第一步：换元法

观察到根式 $\\sqrt{e^x-1}$，令：
$$
t = \\sqrt{e^x-1} \\implies t^2 = e^x - 1 \\implies e^x = t^2 + 1
$$

对 $e^x = t^2 + 1$ 两边求导：
$$
e^x dx = 2t dt \\implies dx = \\frac{2t}{e^x} dt = \\frac{2t}{t^2 + 1} dt
$$

同时，注意被积函数中的 $e^{2x} = (e^x)^2 = (t^2+1)^2$。将这些代入原积分：
$$
I = \\int (t^2 + 1)^2 \\cdot \\arctan t \\cdot \\frac{2t}{t^2+1} dt
$$

简化得：
$$
I = \\int 2t(t^2 + 1) \\arctan t \\, dt = \\int (2t^3 + 2t) \\arctan t \\, dt
$$

---

### 第二步：分部积分法

设 $u = \\arctan t$，$dv = (2t^3 + 2t) dt$。
则：
$$
du = \\frac{1}{1+t^2} dt
$$

$$
v = \\int (2t^3 + 2t) dt = \\frac{1}{2}t^4 + t^2 = \\frac{1}{2}(t^4 + 2t^2)
$$

> **技巧提示：** 为了后面计算方便，我们可以给 $v$ 凑一个常数项。注意到 $du$ 的分母是 $1+t^2$，如果 $v$ 能包含 $(1+t^2)$ 的幂次会更简单。
> 观察到 $\\frac{d}{dt} \\left[ \\frac{1}{2}(t^2+1)^2 \\right] = \\frac{1}{2} \\cdot 2(t^2+1) \\cdot 2t = 2t^3 + 2t$。
> 所以我们取 $v = \\frac{1}{2}(t^2+1)^2$。

根据分部积分公式 $\\int u\\,dv = uv - \\int v\\,du$：
$$
I = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\int \\frac{1}{2}(t^2+1)^2 \\cdot \\frac{1}{1+t^2} dt
$$

$$
I = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\frac{1}{2} \\int (t^2+1) dt
$$

---

### 第三步：计算剩余积分并回代

1.  **计算积分：**
    $$
    \\frac{1}{2} \\int (t^2+1) dt = \\frac{1}{2} \\left( \\frac{1}{3}t^3 + t \\right) = \\frac{1}{6}t^3 + \\frac{1}{2}t
    $$

2.  **代回 $t = \\sqrt{e^x-1}$ 和 $t^2+1 = e^x$：**
    $$
    I = \\frac{1}{2}(e^x)^2 \\arctan\\sqrt{e^x-1} - \\left( \\frac{1}{6}(\\sqrt{e^x-1})^3 + \\frac{1}{2}\\sqrt{e^x-1} \\right) + C
    $$

3.  **化简结果：**

    提取 $\\sqrt{e^x-1}$ 项：
    $$
    \\frac{1}{6}(e^x-1)\\sqrt{e^x-1} + \\frac{1}{2}\\sqrt{e^x-1} = \\sqrt{e^x-1} \\left( \\frac{e^x-1+3}{6} \\right) = \\frac{e^x+2}{6}\\sqrt{e^x-1}
    $$

---

### 最终结果：

$$
\\int e^{2x}\\arctan\\sqrt{e^x-1}dx = \\frac{1}{2}e^{2x}\\arctan\\sqrt{e^x-1} - \\frac{e^x+2}{6}\\sqrt{e^x-1} + C
$$
"""

if __name__ == '__main__':
    data = load()
    for no, new in [('268', NEW_268), ('274', NEW_274)]:
        q = find_q(data, no)
        old = q['answer']
        print(no, 'len', len(old), '->', len(new))
        q['answer'] = new
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('written.')