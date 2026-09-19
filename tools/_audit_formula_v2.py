# -*- coding: utf-8 -*-
"""公式格式体检 v2：token 流状态机（$$ / $），精确判定配平与嵌套错误
   状态：none / display($$) / inline($)
   真错误类型：
     E1 display 内出现单 $（KaTeX 必炸 → 逐字裸奔）
     E2 inline 内出现 $$
     E3 未闭合（$$ 或 $ 开到底）—— 会把后续正文吞进公式
     E4 裸公式行（含 LaTeX 命令但该行不在任何 $ 区间内 → 原文显示）
"""
import json, io, re
from collections import Counter

FILES = {'exam.json': 'pwa/data/exam.json', 'core_bank.json': 'pwa/data/core_bank.json'}
LATEX_CMD = re.compile(r'\\(?:frac|dfrac|tfrac|lim|left|right|begin|end|sum|int|iint|sqrt|ln|cdot|to|infty|partial|alpha|beta|gamma|theta|lambda|Delta|sigma|sin|cos|tan|cot|sec|csc|arctan|mathrm|text|quad|qquad|displaystyle|overline|vec|boldsymbol|matrix|pmatrix|cases|Bigl|Bigr|Big|big|log|max|min|exp|e\^)')


def scan(text):
    """返回 (errs, bare_lines)。errs: [(type, line_no, snippet)]"""
    errs = []
    spans = []          # 已被 $ 覆盖的 [start,end) 区间（用于裸行判定）
    state = None        # None | 'display' | 'inline'
    open_at = None
    for m in re.finditer(r'\$\$|\$', text):
        ln = text.count('\n', 0, m.start()) + 1
        tok = m.group(0)
        if state is None:
            state = 'display' if tok == '$$' else 'inline'
            open_at = (m.start(), ln)
        elif state == 'display':
            if tok == '$$':
                spans.append((open_at[0], m.end()))
                state, open_at = None, None
            else:
                errs.append(('E1 display内单$', ln, text[max(0, m.start() - 40):m.start() + 40].replace('\n', '⏎')))
                # 容错：按内层 $ 处理，避免后续全部误报
                spans.append((open_at[0], m.end()))
                state, open_at = None, None
        else:  # inline
            if tok == '$':
                spans.append((open_at[0], m.end()))
                state, open_at = None, None
            else:
                errs.append(('E2 inline内$$', ln, text[max(0, m.start() - 40):m.start() + 40].replace('\n', '⏎')))
                spans.append((open_at[0], m.end()))
                state, open_at = None, None
    if state is not None:
        errs.append(('E3 未闭合' + ('$$' if state == 'display' else '$'), open_at[1],
                     text[open_at[0]:open_at[0] + 60].replace('\n', '⏎')))

    # E4 裸公式行：含 LaTeX 命令、不在任何 $ 区间内、长度足够
    def covered(pos):
        return any(a <= pos < b for a, b in spans)

    bare = []
    pos = 0
    for i, L in enumerate(text.split('\n')):
        if LATEX_CMD.search(L) and len(L.strip()) > 8 and not any(covered(p) for p in range(pos, pos + len(L))):
            bare.append((i + 1, L.strip()[:80]))
        pos += len(L) + 1
    return errs, bare


def walk(path, tag):
    d = json.load(io.open(path, encoding='utf-8'))
    out = []
    if isinstance(d, list) and d and 'sections' in d[0]:
        for vol in d:
            for sec in vol.get('sections', []):
                for q in sec.get('questions', []):
                    for f in ('stem', 'answer', 'idea'):
                        v = q.get(f) or ''
                        if v:
                            e, b = scan(v)
                            for it in e:
                                out.append((it[0], '%s 第%s题.%s' % (vol.get('id'), q.get('no'), f), it[1], it[2]))
                            for ln, s in b:
                                out.append(('E4 裸公式行', 'core 第%s题.%s' % (q.get('no'), f), ln, s))
    else:
        for sec in d[0]['sections']:
            for q in sec['questions']:
                for f in ('stem', 'answer', 'idea'):
                    v = q.get(f) or ''
                    if v:
                        e, b = scan(v)
                        for it in e:
                            out.append((it[0], '%s 第%s题.%s' % (tag, q.get('no'), f), it[1], it[2]))
                        for ln, s in b:
                            out.append(('E4 裸公式行', '%s 第%s题.%s' % (tag, q.get('no'), f), ln, s))
    return out


def main():
    for name, path in FILES.items():
        issues = walk(path, 'core')
        c = Counter(k for k, *_ in issues)
        print('=' * 72)
        print('%s：真问题 %d 处' % (name, len(issues)))
        print('  分布:', dict(c))
        # 按字段聚合
        by = Counter(w for _, w, _, _ in issues)
        print('  受影响字段 %d 个，Top8:' % len(by))
        for w, n in by.most_common(8):
            print('    %-28s %d 处' % (w, n))
        for it in issues[:10]:
            print('   [%s] %s L%s | %s' % it)


if __name__ == '__main__':
    main()
