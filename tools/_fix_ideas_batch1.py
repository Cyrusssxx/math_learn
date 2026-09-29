# -*- coding: utf-8 -*-
"""为第一批 15 题重写简洁「思路」，并去掉 no=432 中的 \\tag（避免非 display 模式渲染报错）"""
import json, io

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

IDEA = {
    23: '**思路**：$x\\to\\infty$ 型根式/三角混合 → 变量代换 + 泰勒。\n'
        '① 令 $t=\\frac1x$，化为 $\\frac{2t-\\sin t-t\\cos t}{t^{3}}$。\n'
        '② $\\sin t=t-\\frac{t^{3}}{6}+o(t^{3})$，$t\\cos t=t-\\frac{t^{3}}{2}+o(t^{3})$。\n'
        '③ 分子 $=\\frac23t^{3}+o(t^{3})$ ⇒ 极限 $\\frac23$。',
    54: '**思路**：先算含 $n$ 的积分，再取极限。\n'
        '① 待定系数求 $\\int e^{-x}\\sin nx\\,dx=-\\frac{e^{-x}(\\sin nx+n\\cos nx)}{1+n^{2}}$。\n'
        '② 代入 $0,1$ 得 $I_n=\\frac{n}{1+n^{2}}-\\frac{e^{-1}(\\sin n+n\\cos n)}{1+n^{2}}$。\n'
        '③ 两项均 $\\to0$（有界量除以 $n$）⇒ 极限 $0$。',
    153: '**思路**：分段函数复合求导，关键是"由内向外定位区间"。\n'
         '① 内层：$f(e)=\\frac12$，$f\'(e)=\\frac{1}{2e}$（$e>1$ 分支）。\n'
         '② 外层自变量 $=\\frac12<1$，故 $f\'(\\frac12)=2$（另一分支）。\n'
         '③ 链式法则：$2\\cdot\\frac{1}{2e}=\\frac1e$。',
    160: '**思路**：参数方程二阶导 = 一阶导对 $t$ 求导再除以 $\\frac{dx}{dt}$。\n'
         '① $x\'=2e^{t}+1$，$y\'=4te^{t}+2t$；$t=0$ 时 $\\frac{dy}{dx}=0$。\n'
         '② $\\frac{d}{dt}\\left(\\frac{y\'}{x\'}\\right)_{t=0}=\\frac{u\'(0)}{v(0)}=2$。\n'
         '③ 除以 $x\'(0)=3$ ⇒ $\\frac23$。',
    185: '**思路**：斜渐近线 $y=kx+b$。\n'
         '① $k=\\lim\\frac yx=1+\\lim\\arcsin\\frac2x=1$。\n'
         '② $b=\\lim(y-x)=\\lim x\\arcsin\\frac2x=2$（等价无穷小）。\n'
         '③ 得 $y=x+2$。',
    211: '**思路**：分段去绝对值后，分别判可导性与极值。\n'
         '① $f(x)=-x^{2}(x\\le0)$、$x\\ln x(x>0)$，$f(0)=0$。\n'
         '② 左导 $=0$，右导 $=\\lim\\ln x=-\\infty$ ⇒ 不可导。\n'
         '③ 两侧邻域 $f(x)<f(0)$ ⇒ $x=0$ 为极大值点 ⇒ B。',
    227: '**思路**：参数方程下用 $\\frac{dy}{dx}$ 定极值、$\\frac{d^{2}y}{dx^{2}}$ 定凹凸。\n'
         '① $\\frac{dy}{dx}=\\frac{t^{2}-1}{t^{2}+1}$，驻点 $t=\\pm1$（$t=-1$ 极大、$t=1$ 极小）。\n'
         '② $\\frac{d^{2}y}{dx^{2}}=\\frac{4t}{(t^{2}+1)^{3}}$：正为凹、负为凸。\n'
         '③ $t=0$ 处二阶导变号 ⇒ 拐点 $(\\frac13,\\frac13)$。',
    255: '**思路**：二次根式 → 配方 → 套基本公式。\n'
         '① 配方：$x(4-x)=2^{2}-(x-2)^{2}$。\n'
         '② 套 $\\int\\frac{du}{\\sqrt{a^{2}-u^{2}}}=\\arcsin\\frac ua+C$。\n'
         '③ 得 $\\arcsin\\frac{x-2}{2}+C$。',
    316: '**思路**：一拱面积等比递减，求和即可。\n'
         '① 第 $k$ 拱（代换 $x=k\\pi+u$）：$a_k=e^{-k\\pi}\\int_0^{\\pi}e^{-u}\\sin u\\,du$。\n'
         '② $\\int_0^{\\pi}e^{-u}\\sin u\\,du=\\frac{1+e^{-\\pi}}{2}$。\n'
         '③ 等比级数（公比 $e^{-\\pi}$）求和 ⇒ $\\frac{e^{\\pi}+1}{2(e^{\\pi}-1)}$。',
    397: '**思路**：变限积分求导，注意复合上限 $x^{2}$。\n'
         '① $\\varphi\'(x)=\\int_0^{x^{2}}f(t)dt+2x^{2}f(x^{2})$。\n'
         '② $\\varphi(1)=\\int_0^1 f=1$，$\\varphi\'(1)=1+2f(1)=5$。\n'
         '③ 得 $f(1)=2$。',
    404: '**思路**：连续性看重极限，偏导数按定义。\n'
         '① 沿 $y=kx$ 极限 $=\\frac{k}{1+k^{2}}$ 随 $k$ 变 ⇒ 不连续。\n'
         '② $f\'_x(0,0)=f\'_y(0,0)=0$（定义式分子恒为 0）⇒ 偏导存在。\n'
         '③ 选 C。',
    412: '**思路**：先由复合关系解出 $f(u,v)$ 的表达式。\n'
         '① 令 $u=x+y,\\,v=\\frac yx$，解出 $x=\\frac{u}{1+v},\\,y=\\frac{uv}{1+v}$。\n'
         '② $f(u,v)=x^{2}-y^{2}=\\frac{u^{2}(1-v)}{1+v}$。\n'
         '③ 求偏导代入 $u=v=1$ 得 $0$ 与 $-\\frac12$ ⇒ D。',
    416: '**思路**：复合求导后相消。\n'
         '① $z_x=f\'(u)(-\\cos x)+y$，$z_y=f\'(u)\\cos y+x$（$u=\\sin y-\\sin x$）。\n'
         '② 分别除以 $\\cos x,\\cos y$ 相加，$f\'(u)$ 项抵消。\n'
         '③ 剩 $\\frac{y}{\\cos x}+\\frac{x}{\\cos y}$。',
    432: '**思路**：两个方程各求一次全导数，再消去 $\\frac{dy}{dx}$。\n'
         '① $z=xf(x+y)$ ⇒ $\\frac{dz}{dx}=(f+xf\')+xf\'\\frac{dy}{dx}$。\n'
         '② $F(x,y,z)=0$ ⇒ $F\'_x+F\'_y\\frac{dy}{dx}+F\'_z\\frac{dz}{dx}=0$。\n'
         '③ 联立消去 $\\frac{dy}{dx}$ 即得。',
    471: '**思路**：先对 $y$ 积分（分子正好是 $y$），再对 $x$ 积分。\n'
         '① $\\int_0^1\\frac{y\\,dy}{(1+x^{2}+y^{2})^{3/2}}=\\frac{1}{\\sqrt{1+x^{2}}}-\\frac{1}{\\sqrt{2+x^{2}}}$。\n'
         '② 用 $\\int\\frac{dx}{\\sqrt{x^{2}+c}}=\\ln(x+\\sqrt{x^{2}+c})$。\n'
         '③ 代入 $0,1$ 化简得 $\\ln(1+\\sqrt2)-\\ln\\frac{1+\\sqrt3}{\\sqrt2}$。',
}

changed = []
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            no = q.get('no')
            if no in IDEA:
                q['idea'] = IDEA[no]
                changed.append(no)
            if no == 432 and '\\tag' in str(q.get('answer', '')):
                a = q['answer']
                a = a.replace('\\tag{1}', '').replace('\\tag{2}', '')
                a = a.replace('（$y$ 视为常数', '（$y$ 视为常数')
                q['answer'] = a
                changed.append('432-去tag')

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

print(f'已重写思路 {len(changed)} 项: {sorted(set(changed))}')
