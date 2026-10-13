#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""周洋鑫高数强化讲义例题 抽样 × math-note 核心题库 同题比对。
样本：人工视觉识别前 5 个印刷页（专题1/2/5/6）共 30 题。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
DGY = os.path.join(ROOT, 'pwa/data/dgy_items.json')

# (编号, 题干, 备注)
SAMPLE = [
    ('强化1', '设 $F(x)$ 是连续函数 $f(x)$ 的一个原函数，"$M\\\\Leftarrow N$"表示"$M$的充分必要条件是$N$"，则 $F(x)$ 是偶函数 $\\\\Leftrightarrow$ $f(x)$ 是奇函数。其中正确的结论个数为（ ）'),
    ('强化2', '设函数 $f(x)$ 在 $(-\\\\infty,+\\\\infty)$ 上有连续导数，$a$ 为任意常数，则 $\\\\int_0^x[\\\\cos(f(t))+f\'(t)]dt$ 必为奇函数'),
    ('强化3', '设函数 $f(x)=\\\\int_0^{\\\\sin x}\\\\sin^3t\\\\,dt$，$g(x)=\\\\int_0^x f(t)dt$，则（ ）'),
    ('强化4', '设 $f(x)$ 连续，则下列函数中必为偶函数的是（ ） $\\\\int_0^x\\\\frac{e^{t}-1}{e^{t}+1}\\\\cdot\\\\ln\\\\left(t+\\\\sqrt{1+t^2}\\\\right)dt$'),
    ('强化5', '当 $x\\\\to0^{+}$ 时，下列无穷小量中阶数最高的是（ ） $\\\\ln\\\\cos x-\\\\sqrt{\\\\cos x}+1$'),
    ('强化6', '当 $x\\\\to0^{+}$ 时，下列无穷小量中最高阶的是（ ） $\\\\int_0^x(e^{t^2}-1)dt$ $\\\\int_0^x\\\\ln\\\\left(1+\\\\sqrt{t^3}\\\\right)dt$ $\\\\int_0^{\\\\sin x}\\\\sin^2t\\\\,dt$ $\\\\int_0^{1-\\\\cos x}\\\\sqrt[3]{\\\\sin^3t}\\\\,dt$'),
    ('强化7', '试确定常数 $A,B,C$ 的值，使得 $e^{x}(1+Bx+Cx^{2})=1+Ax+o(x^{3})$，其中 $o(x^{3})$ 是当 $x\\\\to0$ 时比 $x^{3}$ 高阶的无穷小量。'),
    ('强化8', '设函数 $f(x)=\\\\frac{\\\\sin x}{1+x^{2}}$ 在 $x=0$ 处的3次泰勒多项式为 $ax+bx^{2}+cx^{3}$，则（ ） $a=1,b=0,c=-\\\\frac{7}{6}$'),
    ('强化17', '求极限 $\\\\lim_{x\\\\to+\\\\infty}\\\\left(x^{\\\\frac{1}{x}}-1\\\\right)^{\\\\frac{1}{\\\\ln x}}$。'),
    ('强化18', '$\\\\lim_{x\\\\to+\\\\infty}\\\\frac{x\\\\displaystyle\\\\int_1^x\\\\sin(xt)\\\\mathrm{d}t}{\\\\displaystyle\\\\int_0^x t\\\\cdot\\\\sin(x^2-t^2)\\\\mathrm{d}t}$。'),
    ('强化19', '$\\\\lim_{x\\\\to0}\\\\frac{\\\\displaystyle\\\\int_0^x\\\\left[t^2\\\\left(e^{\\\\frac1t}-1\\\\right)-t\\\\right]dt}{x^{2}\\\\ln\\\\left(1+\\\\frac1x\\\\right)}$。'),
    ('强化20', '求极限 $\\\\lim_{x\\\\to0}\\\\frac{\\\\displaystyle\\\\int_0^xdu\\\\int_0^{u^2}\\\\arctan(1+t)dt}{x(1-\\\\cos x)}$。'),
    ('强化21', '已知函数 $f(t)=\\\\int_1^xdx\\\\int_{\\\\sqrt{x}}^t\\\\frac{\\\\sin x}{y}\\\\mathrm{d}y$，则 $f\'(\\\\frac{\\\\pi}{2})=$________。'),
    ('强化22', '已知 $\\\\lim_{x\\\\to+\\\\infty}e^{\\\\left[\\\\int_0^{\\\\sqrt{x}}e^{-t^2}dt+a\\\\right]}=b$，求常数 $a,b$。'),
    ('强化23', '已知 $\\\\lim_{x\\\\to+\\\\infty}\\\\left(\\\\sqrt{x^2+x+1}-(ax+b)\\\\right)=0$，求常数 $a,b$。'),
    ('强化24', '设 $\\\\lim_{x\\\\to0}\\\\left[\\\\ln\\\\left(\\\\frac{1+e^{2/x}}{1+e^{1/x}}\\\\right)-2[x]\\\\right]$，其中 $[x]$ 为取整函数。'),
    ('强化30', '已知 $a_n=\\\\sqrt{n}-\\\\frac{(-1)^{n}}{n}$（$n=1,2,\\\\cdots$），则 $\\\\{a_n\\\\}$（ ） 有最大值，有最小值'),
    ('强化31', '设 $\\\\{x_n\\\\}$ 是数列，则"$\\\\lim_{n\\\\to\\\\infty}\\\\frac{x_{n+1}}{x_n}=1$"是"$\\\\{x_n\\\\}$ 收敛"的（ ）'),
    ('强化32', '设数列 $\\\\{x_n\\\\}$ 与 $\\\\{y_n\\\\}$ 满足 $\\\\lim_{n\\\\to\\\\infty}x_ny_n=0$，则下列断言正确的是（ ）'),
    ('强化33', '设实数列 $\\\\{a_n\\\\}$，给出以下四个命题：①若 $\\\\lim_{n\\\\to\\\\infty}a_n=a$，则 $\\\\lim\\\\sin a_n=\\\\sin a$。②若 $\\\\lim\\\\sin a_n=\\\\sin a$，则 $\\\\lim a_n=a$。③若 $\\\\lim a_n=a$，则 $\\\\lim e^{a_n}=e^{a}$。④若 $\\\\lim e^{a_n}=e^{a}$，则 $\\\\lim a_n=a$。其中真命题的个数是（ ）。'),
    ('强化34', '(2022年真题)已知数列 $\\\\{x_n\\\\}$，其中 $-\\\\frac{\\\\pi}{2}\\\\le x_n\\\\le\\\\frac{\\\\pi}{2}$，则（ ） 当 $\\\\lim\\\\cos(x_n)$ 存在时，$\\\\lim x_n$ 存在'),
    ('强化36', '求极限 $\\\\lim_{n\\\\to\\\\infty}\\\\ln^{n}\\\\left(\\\\arctan\\\\frac{a}{n}-\\\\arctan\\\\frac{a}{n+1}\\\\right)$，其中参数 $a\\\\ne0$。'),
    ('强化37', '设 $\\\\{x_n\\\\}$ 是数列，且 $\\\\lim_{n\\\\to\\\\infty}x_{3n}=\\\\lim_{n\\\\to\\\\infty}x_{3n+1}=1$，则 $\\\\{x_n\\\\}$ 收敛的充分条件为（ ）'),
    ('强化38I', '(I) 求 $\\\\lim_{n\\\\to\\\\infty}\\\\frac{1}{n}\\\\left[\\\\ln\\\\left(1+\\\\frac1n\\\\right)+\\\\ln\\\\left(1+\\\\frac2n\\\\right)+\\\\cdots+\\\\ln\\\\left(1+\\\\frac nn\\\\right)\\\\right]$。'),
    ('强化38II', '(II) 求 $\\\\lim_{n\\\\to\\\\infty}\\\\left[\\\\ln\\\\left(1+\\\\frac1n\\\\right)+\\\\ln\\\\left(1+\\\\frac2n\\\\right)+\\\\cdots+\\\\ln\\\\left(1+\\\\frac{2n}{n}\\\\right)\\\\right]$。'),
    ('强化39', '求极限 $\\\\lim\\\\left[\\\\frac{\\\\sin\\\\frac{\\\\pi}{n}+\\\\sin\\\\frac{2\\\\pi}{n}+\\\\cdots+\\\\sin\\\\frac{n\\\\pi}{n}}{n+\\\\frac{\\\\sqrt n}{2}+\\\\frac{n}{\\\\sqrt n}}\\\\right]$。'),
    ('强化40', '求极限 $\\\\lim_{n\\\\to\\\\infty}\\\\sqrt[n]{\\\\left(1+\\\\frac{1}{n^2}\\\\right)\\\\cdot\\\\left(1+\\\\frac{2^2}{n^2}\\\\right)\\\\cdots\\\\left(1+\\\\frac{n^2}{n^2}\\\\right)}$。'),
    ('强化41I', '(I) 求 $\\\\lim_{n\\\\to\\\\infty}\\\\sqrt[n]{a_1^n+a_2^n+\\\\cdots+a_m^n}$，其中 $a_i>0,i=1,2,\\\\cdots,m$。'),
    ('强化41II', '(II) 求 $\\\\lim_{n\\\\to\\\\infty}\\\\sqrt[n]{\\\\sin1+\\\\sin\\\\frac12+\\\\cdots+\\\\sin\\\\frac1n}$。'),
    ('强化42', '设周期为1的周期函数 $f(x)=x-[x]$($[x]$ 表示不超过 $x$ 的最大整数)。(I) 当 $n\\\\le x<n+1$($n$ 为正整数)时，证明：$\\\\frac n2\\\\le\\\\int_0^xf(t)dt<\\\\frac{n+1}{2}$；(II) 求 $\\\\lim_{x\\\\to+\\\\infty}\\\\frac1x\\\\int_0^xf(t)dt$。'),
]


def norm(s):
    s = (s or '')
    for _ in range(3):
        s = re.sub(r'^\s*[（(]?\s*本题满分[^）)]*分\s*[）)]?\s*', '', s)
        s = re.sub(r'^\s*【[^】]{1,24}】\s*', '', s)
        s = re.sub(r'^\s*[（(]\s*(?:19|20)\d\d[^）)]{0,20}[）)]\s*', '', s)
        s = re.sub(r'^\s*\d{1,2}\s*[.、]\s*', '', s)
    s = re.sub(r'\\(?:mathrm|mathbb|mathbf|operatorname)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\(?:left|right|displaystyle|limits|,|;|!|:|\s)+', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = re.sub(r'[{}\\$\s]', '', s)
    s = re.sub(r'[，。、；：,.;:（）()]', '', s)
    return s


def bg(s):
    s = norm(s)
    return set(s[i:i + 2] for i in range(len(s) - 1))


def sim(a, b):
    A, B = bg(a), bg(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    dgy = json.loads(io.open(DGY, encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q.get('stem') or ''
    for p in (dgy if isinstance(dgy, list) else dgy.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q.get('stem') or ''

    key_of = lambda q: q['linkedQid'] if q.get('linkedQid') else 'core-%s' % q['no']
    # 比对池：core_bank 全部 + 真题全部（含已关联的，避免漏判）
    pool = [(q['no'], key_of(q), q.get('stem') or '') for q in qs]
    pool += [(None, k, v) for k, v in zp.items()]

    print('抽样 %d 题 × 比对池 %d 题' % (len(SAMPLE), len(pool)))
    print()
    rows = []
    for tag, stem in SAMPLE:
        best = sorted(((sim(stem, s), no, key, s) for no, key, s in pool), key=lambda x: -x[0])[:2]
        rows.append((tag, stem, best))

    n_same = n_sim = n_diff = 0
    for tag, stem, best in rows:
        s0, no0, k0, txt0 = best[0]
        if s0 >= 0.75:
            n_same += 1
            verdict = '同题'
        elif s0 >= 0.55:
            n_sim += 1
            verdict = '疑似'
        else:
            n_diff += 1
            verdict = '不同'
        print('%-8s sim=%.3f  %-6s -> core no=%s %s' % (tag, s0, verdict, no0, k0))
        if s0 < 0.75:
            print('         样本: %s' % stem.replace('\n', ' ')[:70])
            print('         题库: %s' % (txt0 or '').replace('\n', ' ')[:70])
    print()
    print('=== 抽样结论 ===')
    print('  同题（sim>=0.75） = %d / %d = %.0f%%' % (n_same, len(SAMPLE), 100.0 * n_same / len(SAMPLE)))
    print('  疑似（0.55~0.75） = %d' % n_sim)
    print('  不同（<0.55）      = %d' % n_diff)
    print('  合计「已在题库中」  = %d / %d = %.0f%%' % (
        n_same + n_sim, len(SAMPLE), 100.0 * (n_same + n_sim) / len(SAMPLE)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
