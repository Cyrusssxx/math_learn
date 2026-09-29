# -*- coding: utf-8 -*-
"""no=478 答案清理：去掉「重新审视」啰嗦段，按正确顺序直述"""
import json, io

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

ans = (
    '【答案】$\\dfrac{3\\pi^{2}}{128}$\n'
    '\n'
    '记 $A=\\displaystyle\\iint_{D}f(x,y)\\,\\mathrm dx\\,\\mathrm dy$。\n'
    '\n'
    '**第一步：求 $A$**。原等式两边在 $D$ 上积分：\n'
    '$$\n'
    'A=\\iint_{D}y\\sqrt{1-x^{2}}\\,\\mathrm dx\\,\\mathrm dy+\\left(\\iint_{D}x\\,\\mathrm dx\\,\\mathrm dy\\right)\\!\\cdot A.\n'
    '$$\n'
    '$D$ 关于 $y$ 轴对称且 $x$ 为奇函数，故 $\\iint_{D}x\\,\\mathrm dx\\,\\mathrm dy=0$。又\n'
    '$$\n'
    '\\iint_{D}y\\sqrt{1-x^{2}}\\,\\mathrm dx\\,\\mathrm dy\n'
    '=\\int_{-1}^{1}\\sqrt{1-x^{2}}\\left(\\int_{0}^{\\sqrt{1-x^{2}}}y\\,\\mathrm dy\\right)\\mathrm dx\n'
    '=\\frac12\\int_{-1}^{1}(1-x^{2})^{3/2}\\,\\mathrm dx.\n'
    '$$\n'
    '令 $x=\\sin\\theta$，则 $\\displaystyle\\int_0^{1}(1-x^{2})^{3/2}\\,\\mathrm dx=\\int_0^{\\pi/2}\\cos^{4}\\theta\\,\\mathrm d\\theta=\\frac{3\\pi}{16}$，\n'
    '故 $A=\\dfrac{3\\pi}{16}$。\n'
    '\n'
    '**第二步：求 $\\iint_{D}xf(x,y)\\,\\mathrm dx\\,\\mathrm dy$**。原等式两边乘 $x$ 后再积分：\n'
    '$$\n'
    '\\iint_{D}xf(x,y)\\,\\mathrm dx\\,\\mathrm dy\n'
    '=\\iint_{D}xy\\sqrt{1-x^{2}}\\,\\mathrm dx\\,\\mathrm dy+\\left(\\iint_{D}x^{2}\\,\\mathrm dx\\,\\mathrm dy\\right)\\!\\cdot A.\n'
    '$$\n'
    '第一项：$D$ 关于 $x$ 轴对称，被积函数关于 $y$ 为奇函数，故为 $0$；第二项：\n'
    '$$\n'
    '\\iint_{D}x^{2}\\,\\mathrm dx\\,\\mathrm dy=2\\int_0^{1}x^{2}\\sqrt{1-x^{2}}\\,\\mathrm dx\n'
    '=2\\int_0^{\\pi/2}\\sin^{2}\\theta\\cos^{2}\\theta\\,\\mathrm d\\theta=2\\cdot\\frac{\\pi}{16}=\\frac{\\pi}{8}.\n'
    '$$\n'
    '故所求 $=A\\cdot\\dfrac{\\pi}{8}=\\dfrac{3\\pi}{16}\\cdot\\dfrac{\\pi}{8}=\\dfrac{3\\pi^{2}}{128}$。'
)

idea = (
    '**思路**：等式两边乘 $x$ 再积分，利用对称性消项。\n'
    '① 先积分原等式：$\\iint_D x=0$（对称），$\\iint_D y\\sqrt{1-x^2}=\\frac{3\\pi}{16}$ ⇒ $A=\\frac{3\\pi}{16}$；\n'
    '② 两边乘 $x$ 积分：$xy\\sqrt{1-x^2}$ 关于 $y$ 奇 ⇒ 0，$\\iint_D x^2=\\frac{\\pi}{8}$；\n'
    '③ 所求 $=\\frac{3\\pi}{16}\\cdot\\frac{\\pi}{8}=\\frac{3\\pi^2}{128}$。'
)

for p in core:
    for s in p['sections']:
        for q in s['questions']:
            if q.get('no') == 478:
                q['answer'] = ans
                q['idea'] = idea

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))
print('no=478 已清理为直述版')
