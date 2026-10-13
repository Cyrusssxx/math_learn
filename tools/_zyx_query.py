#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""关键词直查核心题库：确认周洋鑫样本里的若干题在 core_bank 里有没有同题。
用子串匹配（避开正则转义坑），题干做了 LaTeX 结构归一。"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')


def bare(s):
    """剥 LaTeX 结构符号，只留公式内容与文字，用于子串比对。"""
    s = s or ''
    s = re.sub(r'\\(?:mathrm|mathbb|mathbf|operatorname)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\(?:left|right|displaystyle|limits|,|;|!|:|\s)+', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = re.sub(r'[{}\\$\s]', '', s)
    return s


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    key_of = lambda q: q['linkedQid'] if q.get('linkedQid') else 'core-%s' % q['no']

    QUERIES = [
        ('ln(1+k/n) 求和', ['ln(1+', 'ln1+']),
        ('a_n = ⁿ√n - (-1)ⁿ/n', ['n-', 'n']) if False else ('a_n 型', ['a_n']),
        ('√(x²+x+1)-(ax+b)', ['x2+x+1', 'x^2+x+1']),
        ('arctan(a/n)', ['arctan']),
        ('e^{2/x}', ['e2x']),
        ('x^{1/x}', ['x1x']),
        ('lim e^{∫√x e^{-t²}}', ['et2']),
        ('周期函数 f(x)=x-[x]', ['x[x]', 'x-[x]']),
        ('∫₀ˣ sin(xt)dt / ∫ t·sin(x²-t²)', ['sin(xt)', 'sinxt']),
        ('x∫₁ˣsin(xt)', ['sin(xt)']),
        ('√[n]{a₁ⁿ+...+aₘⁿ}', ['a1n', 'a_1^n']),
        ('cos(sin xₙ)', ['cossin', 'cossinx']),
        ('x₃ₙ=x₃ₙ₊₁', ['x3n', 'x_{3n}']),
        ('lim xₙyₙ=0', ['xny_n', 'x_ny_n']),
        ('ln((1+e^{2/x})/(1+e^{1/x}))', ['1+e2x', '1+e^{2/x}']),
    ]
    for label, keys in QUERIES:
        print('=== %s ===' % label)
        hit = 0
        for q in qs:
            b = bare(q.get('stem') or '')
            if any(k in b for k in keys if k):
                hit += 1
                if hit <= 4:
                    print('  no=%-5s %-18s %s' % (q['no'], key_of(q),
                                                  (q.get('stem') or '').replace('\n', ' ')[:80]))
        if not hit:
            print('  （core_bank 无匹配）')
        elif hit > 4:
            print('  …另 %d 道' % (hit - 4))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
