# -*- coding: utf-8 -*-
"""公式格式修复器（安全版）：修复 → 内置复检 → 不过则以原文回滚。
   规则A 未闭合 $$ 且开块后紧跟正文行 → 删除该多余开块
   规则B 未闭合 $$ 且开块后紧跟公式行 → 在该公式行段末尾补闭合 $$
   规则C display 外的裸公式行段 → 用 $$ 包裹
   dry-run：只统计，不写盘。
"""
import json, io, re, sys
from collections import Counter

LATEX_CMD = re.compile(r'\\(?:frac|dfrac|tfrac|lim|left|right|begin|end|sum|int|iint|sqrt|ln|cdot|to|infty|partial|alpha|beta|gamma|theta|lambda|Delta|sigma|sin|cos|tan|cot|sec|csc|arctan|mathrm|text|quad|qquad|displaystyle|overline|vec|boldsymbol|matrix|pmatrix|cases|Bigl|Bigr|Big|big|log|max|min|exp)')
HAN = re.compile(r'[\u4e00-\u9fff]')


def is_formula_line(L):
    s = L.strip()
    return bool(s) and '$' not in s and LATEX_CMD.search(s)


def is_prose_line(L):
    s = L.strip()
    return bool(s) and not LATEX_CMD.search(s)


def scan_state(text):
    """返回 (errors, states, spans)。errors: 列表; states[i]=进入第 i 行时的状态; spans=已被 $ 覆盖的区间"""
    errs, spans, states = [], [], []
    state, open_pos = None, None
    pos = 0
    for i, L in enumerate(text.split('\n')):
        states.append(state)
        for m in re.finditer(r'\$\$|\$', L):
            tok = m.group(0)
            gpos = pos + m.start()
            if state is None:
                state, open_pos = ('display' if tok == '$$' else 'inline'), gpos
            elif state == 'display' and tok == '$$':
                spans.append((open_pos, gpos + len(tok))); state = None
            elif state == 'inline' and tok == '$':
                spans.append((open_pos, gpos + len(tok))); state = None
            else:
                errs.append(('E%d 嵌套错' % (1 if state == 'display' else 2), i + 1))
                spans.append((open_pos, gpos + len(tok))); state = None
        pos += len(L) + 1
    if state is not None:
        errs.append(('E3 未闭合' + ('$$' if state == 'display' else '$'), (text[:open_pos].count('\n') + 1)))
    return errs, states, spans


def bare_lines(text, spans):
    out, pos = [], 0
    for i, L in enumerate(text.split('\n')):
        if is_formula_line(L) and len(L.strip()) > 8:
            if not any(a <= p < b for a, b in spans for p in (pos, pos + max(0, len(L) - 1))):
                out.append(i)
        pos += len(L) + 1
    return out


def fix_field(text):
    """返回 (新文本, 日志列表)；修复后复检不过 → 返回原文 + 标记需人工"""
    orig = text
    lines = text.split('\n')
    logs = []

    # ---- 规则A/B：处理未闭合 $$ ----
    errs, states, spans = scan_state(text)
    if any(e[0].startswith('E3 未闭合$$') for e in errs):
        dd = [i for i, L in enumerate(lines) if L.strip() == '$$']
        # 逐个"开块"（奇数索引位）检查其后首行
        for k in range(0, len(dd), 2):
            oi = dd[k]
            if oi >= len(lines):
                break
            nxt = next((lines[j] for j in range(oi + 1, len(lines)) if lines[j].strip()), '')
            has_close = (k + 1) < len(dd)
            if not has_close:
                # 未闭合的开块
                if nxt and is_prose_line(nxt) and not is_formula_line(nxt) and '$' not in nxt:
                    lines = [L for idx, L in enumerate(lines) if idx != oi]   # 规则A：多余开块
                    logs.append('A 删多余开块@L%d' % (oi + 1))
                else:
                    # 规则B：找其后连续公式行段末尾补闭合
                    j = oi + 1
                    seg_start = j
                    while j < len(lines) and (is_formula_line(lines[j]) or not lines[j].strip()):
                        j += 1
                    if j > seg_start:
                        lines.insert(j, '$$')
                        logs.append('B 补闭合@L%d' % (j + 1))
                    else:
                        lines = [L for idx, L in enumerate(lines) if idx != oi]
                        logs.append('A 删无用开块@L%d' % (oi + 1))
                break
    text2 = '\n'.join(lines)

    # ---- 规则C：包裹 display 外的裸公式行段 ----
    errs2, states2, spans2 = scan_state(text2)
    if spans2 or True:
        bl = set(bare_lines(text2, spans2))
        if bl:
            src = text2.split('\n')
            out, i, n = [], 0, len(src)
            cnt = 0
            while i < n:
                if i in bl:
                    j = i
                    while j < n and (j in bl or (not src[j].strip() and (j + 1) < n and (j + 1) in bl)):
                        j += 1
                    out.append('$$'); out.extend(src[i:j]); out.append('$$')
                    cnt += 1
                    i = j
                else:
                    out.append(src[i]); i += 1
            text2 = '\n'.join(out)
            if cnt:
                logs.append('C 包裹裸公式段 x%d' % cnt)

    # ---- 复检 ----
    e3, _, _ = scan_state(text2)
    _, _, sp = scan_state(text2)
    bad = [x for x in e3 if x[0].startswith('E3') or x[0].startswith('E1') or x[0].startswith('E2')]
    if bad or bare_lines(text2, sp):
        return orig, ['!! 复检未过，回滚（剩余 %d 处）' % (len(bad) + len(bare_lines(text2, sp)))]
    return text2, logs


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'D:/ai code/math-note/pwa/data/exam.json'
    tag = 'core' if 'core' in target else 'exam'
    d = json.load(io.open(target, encoding='utf-8'))
    stat = Counter()
    samples = []
    def handle(q, label):
        for f in ('stem', 'answer', 'idea'):
            v = q.get(f) or ''
            if not v:
                continue
            e, _, sp = scan_state(v)
            bl = bare_lines(v, sp)
            if not (e or bl):
                continue
            new, logs = fix_field(v)
            if new != v and not any(x.startswith('!!') for x in logs):
                stat['可修复字段'] += 1
                q[f] = new
                if len(samples) < 6:
                    samples.append((label + '.' + f, logs))
            else:
                stat['需人工字段'] += 1
                if len(samples) < 6:
                    samples.append((label + '.' + f, logs + ['（原文保持不变）']))
    if isinstance(d, list) and d and 'sections' in d[0]:
        for vol in d:
            for sec in vol.get('sections', []):
                for q in sec.get('questions', []):
                    handle(q, '%s 第%s题' % (vol.get('id'), q.get('no')))
    else:
        for sec in d[0]['sections']:
            for q in sec['questions']:
                handle(q, 'core 第%s题' % q.get('no'))
    print('=' * 70)
    print('%s 修复统计: %s' % (tag, dict(stat)))
    for w, logs in samples:
        print('  %s → %s' % (w, ' ; '.join(logs)))
