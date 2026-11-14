# -*- coding: utf-8 -*-
"""mn27 草稿审计：题干 / 答案两份 md 的结构与 LaTeX 配对检查。"""
import re, os, sys, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mn27_ans')
SEP = re.compile(r'(?====Q(\d+)===)')
TAGS = ('03', '04', '05', '06', '07')
errs = []


def blocks(path):
    s = open(path, encoding='utf-8').read()
    parts = SEP.split(s)
    # parts = ['', no1, body1, no2, body2, ...]
    out = []
    for i in range(1, len(parts) - 1, 2):
        out.append((int(parts[i]), parts[i + 1]))
    return s, out


def latex_check(s, tag, kind, no):
    """逐行检查 $ 配对；$$ 独占行；\\begin/\\end 配对。"""
    if s.count('$') % 2:
        errs.append(f'{tag} {kind} Q{no}: $ 总数为奇数')
    for ln in s.split('\n'):
        t = ln.strip()
        if not t:
            continue
        if t.startswith('$$'):
            if not t.endswith('$$') or len(t) < 5:
                errs.append(f'{tag} {kind} Q{no}: $$ 块未独占行 -> {t[:50]}')
            continue
        c = t.count('$') - 2 * t.count('$$')
        if c % 2:
            errs.append(f'{tag} {kind} Q{no}: 行内 $ 未配对 -> {t[:60]}')
    b = len(re.findall(r'\\begin\{', s))
    e = len(re.findall(r'\\end\{', s))
    if b != e:
        errs.append(f'{tag} {kind} Q{no}: begin/end = {b}/{e}')
    for env in re.findall(r'\\begin\{(\w+\*?)\}', s):
        if s.count('\\begin{' + env + '}') != s.count('\\end{' + env + '}'):
            errs.append(f'{tag} {kind} Q{no}: 环境 {env} 未配对')
    for ln in s.split('\n'):
        if re.match(r'^\s*(?:-\s|\d+\.\s)', ln):
            errs.append(f'{tag} {kind} Q{no}: 出现列表前缀 -> {ln.strip()[:50]}')


def check_stem(tag):
    s, bs = blocks(os.path.join(ROOT, f'q{tag}_stem.md'))
    nos = [n for n, _ in bs]
    if nos != list(range(1, 23)):
        errs.append(f'{tag} stem: 题号不连续 {nos}')
    for n, b in bs:
        k = re.search(r'【题型】(\w+)', b)
        if not k:
            errs.append(f'{tag} stem Q{n}: 缺【题型】')
            continue
        kind = k.group(1)
        want = 'choice' if n <= 10 else ('blank' if n <= 16 else 'calc')
        if kind != want:
            errs.append(f'{tag} stem Q{n}: 题型 {kind} != {want}')
        if '【题干】' not in b:
            errs.append(f'{tag} stem Q{n}: 缺【题干】')
        for c in 'ABCD':
            has = ('【' + c + '】') in b
            if (n <= 10) != has:
                errs.append(f'{tag} stem Q{n}: 选项 {c} {"缺" if n <= 10 else "多余"}')
        if '【答案】' in b or '【解】' in b:
            errs.append(f'{tag} stem Q{n}: 混入答案/解析')
        if n >= 17 and '满分' not in b:
            errs.append(f'{tag} stem Q{n}: 解答题缺分值')
        latex_check(b, tag, 'stem', n)
    return nos


def check_ans(tag):
    s, bs = blocks(os.path.join(ROOT, f'q{tag}_ans.md'))
    nos = [n for n, _ in bs]
    if nos != list(range(1, 23)):
        errs.append(f'{tag} ans: 题号不连续 {nos}')
    for n, b in bs:
        for key in ('【答案】', '【解】', '【思路】'):
            if key not in b:
                errs.append(f'{tag} ans Q{n}: 缺 {key}')
        latex_check(b, tag, 'ans', n)
    return nos


for t in TAGS:
    a = check_stem(t)
    b = check_ans(t)
    print(f'q{t}: stem {len(a)} 题 / ans {len(b)} 题 / 对应 {"OK" if a == b == list(range(1, 23)) else "FAIL"}')

print()
if errs:
    print(f'发现 {len(errs)} 个问题：')
    for e in errs[:80]:
        print(' -', e)
    sys.exit(1)
print('✓ mn27 草稿审计通过（5 套 × 22 题，题干与答案题号一一对应）')
