# -*- coding: utf-8 -*-
"""全库公式格式体检：逐行状态机检查 $ / $$ 配平，找出会导致渲染裸奔的三类错误
   A. 连续 $$ 空块（$$\n$$）
   B. 孤立 $$ 行（开块未配对 → 把后续文本吞进显示块）
   C. 裸公式行（含 LaTeX 命令但无 $ 包裹）
   D. 跨行失配 $（同一行内 $ 个数为奇数）
"""
import json, io, re
from collections import Counter

FILES = {'exam.json': 'pwa/data/exam.json', 'core_bank.json': 'pwa/data/core_bank.json'}
LATEX_CMD = re.compile(r'\\(frac|dfrac|lim|left|right|begin|end|sum|int|sqrt|ln|cdot|to|infty|partial|alpha|beta|theta|Delta|sin|cos|tan|mathrm|text|quad|displaystyle|overline|vec|matrix|pmatrix|cases)\b')

def check_field(v, where, issues):
    lines = v.split('\n')
    in_disp = False
    for i, L in enumerate(lines):
        s = L.strip()
        # A. 连续 $$ 空块
        if re.search(r'\$\$\s*\n\s*\$\$', v):
            if i > 0 and lines[i - 1].strip() == '$$' and s == '$$':
                issues.append(('A 连续$$', where, i, s[:60]))
                continue
        # B. 孤立 $$ 行（切换显示块状态）
        if s == '$$':
            in_disp = not in_disp
            continue
        # 同行内完整的 $$...$$
        n_dd = L.count('$$')
        if n_dd:
            if n_dd % 2:
                issues.append(('B $$奇数', where, i, L[:90]))
            continue
        n_s = L.count('$')
        if in_disp:
            # 显示块内不应出现单个 $（KaTeX 会炸）
            if n_s:
                issues.append(('D 块内$', where, i, L[:90]))
            continue
        if n_s % 2:
            issues.append(('D 跨行失配$', where, i, L[:90]))
            continue
        # C. 裸公式行：无 $ 但有 LaTeX 命令
        if n_s == 0 and LATEX_CMD.search(L) and len(s) > 8:
            issues.append(('C 裸公式行', where, i, L[:90]))

for name, path in FILES.items():
    d = json.load(io.open(path, encoding='utf-8'))
    issues = []
    nfields = 0
    if isinstance(d, list) and d and 'sections' in d[0]:
        for vol in d:
            for sec in vol.get('sections', []):
                for q in sec.get('questions', []):
                    for f in ('stem', 'answer', 'idea'):
                        v = q.get(f) or ''
                        if v:
                            nfields += 1
                            check_field(v, '%s 第%s题.%s' % (vol.get('id'), q.get('no'), f), issues)
    else:
        for sec in d[0]['sections']:
            for q in sec['questions']:
                for f in ('stem', 'answer', 'idea'):
                    v = q.get(f) or ''
                    if v:
                        nfields += 1
                        check_field(v, 'core 第%s题.%s' % (q.get('no'), f), issues)
    print('=' * 70)
    print('%s：字段 %d 个，发现格式问题 %d 处' % (name, nfields, len(issues)))
    c = Counter(k for k, *_ in issues)
    print('  类型分布:', dict(c))
    for it in issues[:25]:
        print('   [%s] %s L%d | %s' % it)
