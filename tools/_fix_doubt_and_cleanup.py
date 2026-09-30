# -*- coding: utf-8 -*-
"""第四批：修复存疑题（180/417/431）+ 清理 488/490 评分段 + 492/494 配平"""
import json, io, re

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)


def find(no):
    return next(q for p in core for s in p['sections'] for q in s['questions'] if q.get('no') == no)


# ============ no=180：正确答案 y=2x（dx/dt=-1, dy/dt=-2） ============
q = find(180)
q['answer'] = (
    '【答案】$y=2x$\n'
    '\n'
    '点 $(0,0)$ 对应 $t=1$（此时 $x=\\int_0^{0}=0,\\ y=1\\cdot\\ln1=0$）。\n'
    '\n'
    '求导：\n'
    '$$\n'
    '\\frac{\\mathrm dx}{\\mathrm dt}=\\mathrm e^{-(1-t)^{2}}\\cdot(-1),\\qquad\n'
    '\\left.\\frac{\\mathrm dx}{\\mathrm dt}\\right|_{t=1}=-1;\n'
    '$$\n'
    '$$\n'
    '\\frac{\\mathrm dy}{\\mathrm dt}=2t\\ln(2-t^{2})+t^{2}\\cdot\\frac{-2t}{2-t^{2}},\\qquad\n'
    '\\left.\\frac{\\mathrm dy}{\\mathrm dt}\\right|_{t=1}=2\\ln1-\\frac{2}{1}=-2.\n'
    '$$\n'
    '切线斜率\n'
    '$$\n'
    'k=\\left.\\frac{\\mathrm dy/\\mathrm dt}{\\mathrm dx/\\mathrm dt}\\right|_{t=1}=\\frac{-2}{-1}=2,\n'
    '$$\n'
    '切线方程为 $y=2x$。'
)
q['idea'] = ('**思路**：参数方程切线 $k=\\frac{y\'}{x\'}$ 在 $t=1$ 处。\n'
             '① $x\'=-\\mathrm e^{-(1-t)^2}$，$x\'(1)=-1$；\n'
             '② $y\'=2t\\ln(2-t^2)-\\frac{2t^3}{2-t^2}$，$y\'(1)=-2$；\n'
             '③ $k=\\frac{-2}{-1}=2$ ⇒ $y=2x$。')

# ============ no=417：题干修正为 xy(...)（两个权威来源一致），解析按 f(u)=1/2 ln u ============
q = find(417)
q['stem'] = q['stem'].replace('=y^2(\\ln y-\\ln x)', '=xy(\\ln y-\\ln x)')
q['answer'] = (
    '【答案】B\n'
    '\n'
    '设 $u=\\dfrac yx$，则 $z=xyf(u)$。求导：\n'
    '$$\n'
    '\\frac{\\partial z}{\\partial x}=yf(u)+xyf\'(u)\\left(-\\frac{y}{x^{2}}\\right)=yf(u)-\\frac{y^{2}}{x}f\'(u),\n'
    '$$\n'
    '$$\n'
    '\\frac{\\partial z}{\\partial y}=xf(u)+xyf\'(u)\\cdot\\frac1x=xf(u)+yf\'(u).\n'
    '$$\n'
    '于是\n'
    '$$\n'
    'x\\frac{\\partial z}{\\partial x}+y\\frac{\\partial z}{\\partial y}\n'
    '=xyf(u)-y^{2}f\'(u)+xyf(u)+y^{2}f\'(u)=2xy\\,f(u).\n'
    '$$\n'
    '由题设 $2xy\\,f\\!\\left(\\frac yx\\right)=xy\\ln\\dfrac yx$，即\n'
    '$$\n'
    'f(u)=\\frac12\\ln u\\quad\\Rightarrow\\quad f(1)=0,\\quad f\'(u)=\\frac{1}{2u},\\ f\'(1)=\\frac12.\n'
    '$$\n'
    '故选 B。'
)
q['idea'] = ('**思路**：$xz_x+yz_y$ 中 $f\'$ 项恰好相消，只剩 $2xyf(u)$。\n'
             '① $z_x=yf-\\frac{y^2}{x}f\'$，$z_y=xf+yf\'$；\n'
             '② $xz_x+yz_y=2xyf(u)=xy\\ln u$ ⇒ $f(u)=\\frac12\\ln u$；\n'
             '③ $f(1)=0$，$f\'(1)=\\frac12$ ⇒ B。')

# ============ no=431：按所给方程的严格推导，结果 1/(8e²) - 1/e ============
q = find(431)
q['answer'] = (
    '【答案】$\\dfrac{1}{8\\mathrm e^{2}}-\\dfrac{1}{\\mathrm e}$（按题面方程 $z+\\ln z-\\displaystyle\\int_y^x \\mathrm e^{-t^{2}}\\,\\mathrm dt=1$ 推导）\n'
    '\n'
    '**定函数值**：代入 $x=1,\\ y=1$，积分区间长度为 $0$，得\n'
    '$$\n'
    'z+\\ln z=1\\Rightarrow z(1,1)=1.\n'
    '$$\n'
    '**一阶偏导**：方程两边对 $x$ 求偏导（注意 $\\dfrac{\\partial}{\\partial x}\\displaystyle\\int_y^x\\mathrm e^{-t^{2}}\\mathrm dt=\\mathrm e^{-x^{2}}$）：\n'
    '$$\n'
    'z_x+\\frac{z_x}{z}-\\mathrm e^{-x^{2}}=0\\Rightarrow z_x=\\frac{z\\,\\mathrm e^{-x^{2}}}{z+1}.\n'
    '$$\n'
    '代入 $(1,1),\\ z=1$：$z_x=\\dfrac{\\mathrm e^{-1}}{2}$。\n'
    '\n'
    '**二阶偏导**：对上式（或对一阶关系式）再求导，注意 $z_x$ 也依赖于 $x$：\n'
    '$$\n'
    '\\left(1+\\frac1z\\right)z_{xx}-\\frac{z_x^{2}}{z^{2}}=-2x\\,\\mathrm e^{-x^{2}}.\n'
    '$$\n'
    '⚠️ 这一项 $-\\dfrac{z_x^{2}}{z^{2}}$ 来自 $\\dfrac1z$ 的求导，是最容易遗漏的步骤。\n'
    '\n'
    '代入 $x=1,\\ z=1,\\ z_x=\\dfrac{1}{2\\mathrm e}$：\n'
    '$$\n'
    '2z_{xx}-\\frac{1}{4\\mathrm e^{2}}=-\\frac{2}{\\mathrm e}\n'
    '\\Rightarrow z_{xx}=\\dfrac{1}{8\\mathrm e^{2}}-\\dfrac{1}{\\mathrm e}.\n'
    '$$'
)
q['idea'] = ('**思路**：隐函数二阶偏导，关键是不漏掉 $\\frac1z$ 求导产生的 $-\\frac{z_x^2}{z^2}$ 项。\n'
             '① $(1,1)$ 处 $z=1$；\n'
             '② 一阶：$(1+\\frac1z)z_x=e^{-x^2}$ ⇒ $z_x(1,1)=\\frac{1}{2e}$；\n'
             '③ 二阶：$(1+\\frac1z)z_{xx}-\\frac{z_x^2}{z^2}=-2xe^{-x^2}$ ⇒ $z_{xx}(1,1)=\\frac{1}{8e^2}-\\frac1e$。')

# ============ no=488/490：删除「阅卷评分」段（从该标记起到末尾） ============
for no in (488, 490):
    q = find(no)
    a = str(q.get('answer') or '')
    idx = a.find('**考研数学阅卷通用规则估算**')
    if idx > 0:
        q['answer'] = a[:idx].rstrip()
        print(f'no={no} 已删除评分段 {len(a) - idx} 字')

# ============ no=492/494：$$ 奇数 → 末尾补 $$ 配平 ============
for no in (492, 494):
    q = find(no)
    a = str(q.get('answer') or '')
    if a.count('$$') % 2 != 0:
        q['answer'] = a + '\n$$'
        print(f'no={no} 已补 $$ 配平')

# ============ 保存 ============
with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

# 验证 no=417 题干与 no=180 答案
with io.open(FP, 'r', encoding='utf-8') as f:
    chk = json.load(f)
q180 = find2 = next(q for p in chk for s in p['sections'] for q in s['questions'] if q.get('no') == 180)
q417 = next(q for p in chk for s in p['sections'] for q in s['questions'] if q.get('no') == 417)
assert 'y=2x' in q180['answer']
assert 'xy(\\ln y-\\ln x)' in q417['stem'] or 'xy(ln y-ln x)' in q417['stem']
print('写回验证通过（no=180 改 y=2x；no=417 题干已修正为 xy(ln y-ln x)）')
