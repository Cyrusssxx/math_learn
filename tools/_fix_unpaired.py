# -*- coding: utf-8 -*-
"""修复 core_bank 4 个 $ 不配平字段（大观园 explanation 截断所致）：
no=353 ← exam.json 2016数二第20题完整答案
no=146 ← 手工补全（1996数三 g(x) 分段函数）
"""
import json, io, re, sys, difflib

sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import norm                                 # noqa: E402

CB = 'D:/ai code/math-note/pwa/data/core_bank.json'
EXAM = 'D:/ai code/math-note/pwa/data/exam.json'

cb = json.load(io.open(CB, encoding='utf-8'))
qs = [q for s in cb[0]['sections'] for q in s['questions']]
ex = json.load(io.open(EXAM, encoding='utf-8'))

# ---- no=353 ← 2016数二 第20题（先核验同题）----
q353 = next(q for q in qs if q['no'] == 353)
e20 = None
for vol in ex:
    if str(vol.get('year')) == '2016':
        for sec in vol.get('sections', []):
            for q in sec.get('questions', []):
                if q.get('no') == 20:
                    e20 = q
sim = difflib.SequenceMatcher(None, norm(q353['stem']), norm(e20['stem'])).ratio()
print('no=353 vs exam 2016-20 题干相似度: %.3f' % sim)
assert sim >= 0.80, '题面不匹配，中止'
q353['answer'] = e20['answer']
q353['idea'] = e20.get('idea') or ''
print('no=353 已替换为 exam 2016数二第20题答案（len=%d/%d）' % (len(q353['answer']), len(q353['idea'])))

# ---- no=146 手工补全 ----
q146 = next(q for q in qs if q['no'] == 146)
q146['idea'] = (
    '**思路**：分段点用定义，其余用求导公式；连续性的关键是比较 $\lim_{x\\to0}f\'(x)$ 与 $f\'(0)$。\n'
    '① $x\\neq0$：$f\'(x)=\\dfrac{x[g\'(x)+\\mathrm e^{-x}]-[g(x)-\\mathrm e^{-x}]}{x^{2}}'
    '=\\dfrac{xg\'(x)-g(x)+x\\mathrm e^{-x}+\\mathrm e^{-x}}{x^{2}}$。\n'
    '② $f\'(0)=\\lim\\limits_{x\\to0}\\dfrac{f(x)-f(0)}{x}'
    '=\\lim\\limits_{x\\to0}\\dfrac{g(x)-\\mathrm e^{-x}}{x^{2}}$；'
    '由 $g(0)=1,\\ g\'(0)=-1$ 泰勒展开 $g(x)-\\mathrm e^{-x}'
    '=\\dfrac{g\'\'(0)-1}{2}x^{2}+o(x^{2})$，故 $f\'(0)=\\dfrac{g\'\'(0)-1}{2}$。\n'
    '③ 连续性：$\\lim\\limits_{x\\to0}f\'(x)$ 分子按 $g\'(x)=-1+g\'\'(0)x+o(x)$、'
    '$g(x)=1-x+\\tfrac{g\'\'(0)}{2}x^{2}+o(x^{2})$、$\\mathrm e^{-x}=1-x+\\tfrac{x^{2}}{2}+o(x^{2})$ 展开，'
    '常数项与 $x$ 项相消，$x^{2}$ 项系数为 $\\dfrac{g\'\'(0)-1}{2}$，'
    '故 $\\lim\\limits_{x\\to0}f\'(x)=f\'(0)$，$f\'(x)$ 在 $x=0$ 连续。'
)
q146['answer'] = (
    '【答案】$f\'(x)=\\begin{cases}\\dfrac{xg\'(x)-g(x)+x\\mathrm e^{-x}+\\mathrm e^{-x}}{x^{2}},'
    '& x\\neq0,\\\\ \\dfrac{g\'\'(0)-1}{2}, & x=0,\\end{cases}$ 且 $f\'(x)$ 在 $(-\\infty,+\\infty)$ 连续。\n\n'
    '【解析】$x\\neq0$ 时 $f\'(x)=\\dfrac{x[g\'(x)+\\mathrm e^{-x}]-[g(x)-\\mathrm e^{-x}]}{x^{2}}'
    '=\\dfrac{xg\'(x)-g(x)+x\\mathrm e^{-x}+\\mathrm e^{-x}}{x^{2}}$；\n'
    '$f\'(0)=\\lim\\limits_{x\\to0}\\dfrac{f(x)-f(0)}{x}'
    '=\\lim\\limits_{x\\to0}\\dfrac{g(x)-\\mathrm e^{-x}}{x^{2}}'
    '=\\lim\\limits_{x\\to0}\\dfrac{\\frac{g\'\'(0)-1}{2}x^{2}+o(x^{2})}{x^{2}}'
    '=\\dfrac{g\'\'(0)-1}{2}$。\n'
    '连续性：$\\lim\\limits_{x\\to0}f\'(x)$ 中代入 $g\'(x)=-1+g\'\'(0)x+o(x)$、'
    '$g(x)=1-x+\\tfrac{g\'\'(0)}{2}x^{2}+o(x^{2})$、$\\mathrm e^{-x}=1-x+\\tfrac{x^{2}}{2}+o(x^{2})$，'
    '分子 $xg\'(x)-g(x)+x\\mathrm e^{-x}+\\mathrm e^{-x}'
    '=\\left(\\dfrac{g\'\'(0)}{2}-1\\right)x^{2}+o(x^{2})$，'
    '故 $\\lim\\limits_{x\\to0}f\'(x)=\\dfrac{g\'\'(0)-1}{2}=f\'(0)$，连续。'
)
print('no=146 已补全（answer len=%d, idea len=%d）' % (len(q146['answer']), len(q146['idea'])))

with io.open(CB, 'w', encoding='utf-8', newline='') as f:
    json.dump(cb, f, ensure_ascii=False, separators=(',', ':'))

# 复查
cb2 = json.load(io.open(CB, encoding='utf-8'))
qs2 = [q for s in cb2[0]['sections'] for q in s['questions']]
bad = [(q['no'], f) for q in qs2 for f in ('answer', 'idea')
       if (q.get(f) or '').count('$') % 2]
dd = 0
for q in qs2:
    for f in ('answer', 'idea'):
        dd += len(re.findall(r'\$\$\s*\n\s*\$\$|\$\$\$\$', q.get(f) or ''))
print('复查：$ 不配平字段 %d | 连续 $$ 空块 %d' % (len(bad), dd))
