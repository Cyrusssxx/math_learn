# -*- coding: utf-8 -*-
# 批次8：283/424 人工规范化重写（数学内容不变，公式独立成块、中文留外）
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

NEW_283 = """【答案】(1) $-\\cos x + \\frac{1}{3}\\cos^3 x + C$；(2) $\\frac{3}{8}x + \\frac{1}{4}\\sin 2x + \\frac{1}{32}\\sin 4x + C$；(3) $-\\cot x - \\frac{1}{3}\\cot^3 x + C$；（4）

$$
\\int \\sec^3 x \\, dx = \\frac{1}{2} \\sec x \\tan x + \\frac{1}{2} \\ln |\\sec x + \\tan x| + C
$$

这四道不定积分题涵盖了三角函数积分中非常经典的三种处理技巧：**凑微分法（奇次幂）**、**降幂法（偶次幂）**以及**分部积分法（正割/余割的奇次幂）**。

以下是详细的严谨求解过程：

---

### (1) $\\int \\sin^3 x \\, dx$
**核心技巧：奇数次幂，剥离一项凑微分。**

将 $\\sin^3 x$ 拆分为 $\\sin^2 x \\cdot \\sin x$，并利用三角恒等式 $\\sin^2 x = 1 - \\cos^2 x$。

$$
\\int \\sin^3 x \\, dx = \\int \\sin^2 x \\cdot \\sin x \\, dx
$$

$$
= \\int (1 - \\cos^2 x) (-d(\\cos x))
$$

$$
= \\int (\\cos^2 x - 1) \\, d(\\cos x)
$$

直接对 $\\cos x$ 积分：

$$
= \\frac{1}{3}\\cos^3 x - \\cos x + C
$$

---

### (2) $\\int \\cos^4 x \\, dx$
**核心技巧：偶数次幂，利用半角（倍角）公式连续降幂。**

使用降幂公式 $\\cos^2 x = \\frac{1 + \\cos 2x}{2}$：

$$
\\int \\cos^4 x \\, dx = \\int \\left( \\frac{1 + \\cos 2x}{2} \\right)^2 dx
$$

$$
= \\frac{1}{4} \\int (1 + 2\\cos 2x + \\cos^2 2x) \\, dx
$$

对其中的 $\\cos^2 2x$ 再次使用降幂公式 $\\cos^2 2x = \\frac{1 + \\cos 4x}{2}$：

$$
= \\frac{1}{4} \\int \\left( 1 + 2\\cos 2x + \\frac{1 + \\cos 4x}{2} \\right) dx
$$

$$
= \\frac{1}{4} \\int \\left( \\frac{3}{2} + 2\\cos 2x + \\frac{1}{2}\\cos 4x \\right) dx
$$

逐项积分即可得到最终结果：

$$
= \\frac{1}{4} \\left( \\frac{3}{2}x + \\sin 2x + \\frac{1}{8}\\sin 4x \\right) + C
$$

$$
= \\frac{3}{8}x + \\frac{1}{4}\\sin 2x + \\frac{1}{32}\\sin 4x + C
$$

---

### (3) $\\int \\csc^4 x \\, dx$
**核心技巧：偶数次幂，剥离二次项凑微分。**

将 $\\csc^4 x$ 拆分为 $\\csc^2 x \\cdot \\csc^2 x$，并利用公式 $\\csc^2 x = 1 + \\cot^2 x$ 以及 $d(\\cot x) = -\\csc^2 x \\, dx$。

$$
\\int \\csc^4 x \\, dx = \\int \\csc^2 x \\cdot \\csc^2 x \\, dx
$$

$$
= \\int (1 + \\cot^2 x) (-d(\\cot x))
$$

$$
= -\\int (1 + \\cot^2 x) \\, d(\\cot x)
$$

直接对 $\\cot x$ 积分：

$$
= -\\cot x - \\frac{1}{3}\\cot^3 x + C
$$

---

### (4) $\\int \\sec^3 x \\, dx$
**核心技巧：正割函数的奇数次幂，使用分部积分法（产生循环积分）。**

设 $u = \\sec x$，$dv = \\sec^2 x \\, dx$。
则 $du = \\sec x \\tan x \\, dx$，$v = \\tan x$。

应用分部积分公式 $\\int u \\, dv = uv - \\int v \\, du$：

$$
\\int \\sec^3 x \\, dx = \\sec x \\tan x - \\int \\tan x \\cdot (\\sec x \\tan x) \\, dx
$$

$$
= \\sec x \\tan x - \\int \\sec x \\tan^2 x \\, dx
$$

利用恒等式 $\\tan^2 x = \\sec^2 x - 1$：

$$
\\int \\sec^3 x \\, dx = \\sec x \\tan x - \\int \\sec x (\\sec^2 x - 1) \\, dx
$$

$$
\\int \\sec^3 x \\, dx = \\sec x \\tan x - \\int \\sec^3 x \\, dx + \\int \\sec x \\, dx
$$

将右侧的 $-\\int \\sec^3 x \\, dx$ 移项到等式左边：

$$
2 \\int \\sec^3 x \\, dx = \\sec x \\tan x + \\int \\sec x \\, dx
$$

我们已知 $\\int \\sec x \\, dx = \\ln |\\sec x + \\tan x| + C_1$，代入上式并除以 2：

$$
\\int \\sec^3 x \\, dx = \\frac{1}{2} \\sec x \\tan x + \\frac{1}{2} \\ln |\\sec x + \\tan x| + C
$$
"""

NEW_424 = """【解析】由复合函数链式法则得

$$
\\frac{\\partial u}{\\partial x}=\\frac{\\partial u}{\\partial\\xi}\\cdot\\frac{\\partial\\xi}{\\partial x}+\\frac{\\partial u}{\\partial\\eta}\\cdot\\frac{\\partial\\eta}{\\partial x}=\\frac{\\partial u}{\\partial\\xi}+\\frac{\\partial u}{\\partial\\eta},
$$

$$
\\frac{\\partial u}{\\partial y}=\\frac{\\partial u}{\\partial\\xi}\\cdot\\frac{\\partial\\xi}{\\partial y}+\\frac{\\partial u}{\\partial\\eta}\\cdot\\frac{\\partial\\eta}{\\partial y}=a\\cdot\\frac{\\partial u}{\\partial\\xi}+b\\cdot\\frac{\\partial u}{\\partial\\eta},
$$

$$
\\frac{\\partial^{2}u}{\\partial x^{2}}=\\frac{\\partial}{\\partial x}\\!\\left(\\frac{\\partial u}{\\partial\\xi}+\\frac{\\partial u}{\\partial\\eta}\\right)=\\frac{\\partial^{2}u}{\\partial\\xi^{2}}+\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta}+\\frac{\\partial^{2}u}{\\partial\\eta\\partial\\xi}+\\frac{\\partial^{2}u}{\\partial\\eta^{2}}
$$

$$
=\\frac{\\partial^{2}u}{\\partial\\xi^{2}}+2\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta},
$$

$$
\\frac{\\partial^{2}u}{\\partial x\\partial y}=\\frac{\\partial}{\\partial y}\\!\\left(\\frac{\\partial u}{\\partial\\xi}+\\frac{\\partial u}{\\partial\\eta}\\right)=\\frac{\\partial^{2}u}{\\partial\\xi^{2}}\\cdot\\frac{\\partial\\xi}{\\partial y}+\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta}\\cdot\\frac{\\partial\\eta}{\\partial y}+\\frac{\\partial^{2}u}{\\partial\\eta\\partial\\xi}\\cdot\\frac{\\partial\\xi}{\\partial y}+\\frac{\\partial^{2}u}{\\partial\\eta^{2}}\\cdot\\frac{\\partial\\eta}{\\partial y}
$$

$$
=a\\frac{\\partial^{2}u}{\\partial\\xi^{2}}+(a+b)\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta}+b\\frac{\\partial^{2}u}{\\partial\\eta^{2}},
$$

$$
\\frac{\\partial^{2}u}{\\partial y^{2}}=\\frac{\\partial}{\\partial y}\\!\\left(a\\frac{\\partial u}{\\partial\\xi}+b\\frac{\\partial u}{\\partial\\eta}\\right)=a\\Bigl(a\\frac{\\partial^{2}u}{\\partial\\xi^{2}}+b\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta}\\Bigr)+b\\Bigl(a\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta}+b\\frac{\\partial^{2}u}{\\partial\\eta^{2}}\\Bigr)
$$

$$
=a^{2}\\frac{\\partial^{2}u}{\\partial\\xi^{2}}+b^{2}\\frac{\\partial^{2}u}{\\partial\\eta^{2}}+2ab\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta},
$$

故

$$
4\\dfrac{\\partial^{2}u}{\\partial x^{2}}+12\\dfrac{\\partial^{2}u}{\\partial x\\partial y}+5\\dfrac{\\partial^{2}u}{\\partial y^{2}}=(5a^{2}+12a+4)\\frac{\\partial^{2}u}{\\partial\\xi^{2}}+(5b^{2}+12b+4)\\frac{\\partial^{2}u}{\\partial\\eta^{2}}+[12(a+b)+10ab+8]\\frac{\\partial^{2}u}{\\partial\\xi\\partial\\eta}=0,
$$

所以 $\\begin{cases}5a^{2}+12a+4=0\\\\5b^{2}+12b+4=0\\\\12(a+b)+10ab+8\\neq 0\\end{cases}$

则 $a=-\\dfrac{2}{5}$ 或 $-2$，$b=-\\dfrac{2}{5}$ 或 $-2$。又因为当 $(a,b)$ 为 $(-2,-2),(-\\dfrac{2}{5},-\\dfrac{2}{5})$ 时方程 (3) 不满足，

所以当 $(a,b)$ 为 $(-\\dfrac{2}{5},-2),(-2,-\\dfrac{2}{5})$ 满足题意。
"""

if __name__ == '__main__':
    data = load()
    for no, new in [('283', NEW_283), ('424', NEW_424)]:
        q = find_q(data, no)
        old = q['answer']
        print(no, 'len', len(old), '->', len(new))
        q['answer'] = new
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('written.')