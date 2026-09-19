# -*- coding: utf-8 -*-
"""公式格式修复器 v2（迭代式）：按优先级反复修复 → 复检 → 不过则回滚。
规则：
  R1 折叠相邻的独立 $$ 行（避免产生「连续 $$ 空块」）
  R2 裸公式行段（display 外的公式行）→ 用 $$ 包裹
  R3 未闭合 $$：开块后紧跟正文 → 删该开块；开块后是公式 → 段末补闭合
  R4 E1 display 内出现单 $ → 删掉多余的那个 $
  R5 E2 inline 内出现 $$ → 降级为 $
dry-run：只统计，不写盘。
"""
import json, io, sys, re
sys.path.insert(0, 'D:/ai code/math-note/tools')
from _audit_formula_v2 import scan, LATEX_CMD        # noqa

BASE = 'D:/ai code/math-note/pwa/data/'
HAN = re.compile(r'[\u4e00-\u9fff]')
FORM = re.compile(LATEX_CMD.pattern)


def is_formula(L):
    s = L.strip()
    return bool(s) and '$' not in s and bool(FORM.search(s))


def errs_of(text):
    e, b = scan(text)
    return [x for x in e if x[0][:2] in ('E1', 'E2', 'E3')], b


# ---------- 规则实现（每轮只应用一条，返回是否改动） ----------
def R1_merge_dd(lines):
    """折叠相邻独立 $$ 行（中间仅空行）"""
    changed = False
    out, i = [], 0
    while i < len(lines):
        if lines[i].strip() == '$$':
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip() == '$$':
                out.append(lines[i])
                i = j + 1                      # 吞掉第二个及其间空行
                changed = True
                continue
        out.append(lines[i])
        i += 1
    return out, changed


def R2_wrap_bare(lines):
    """裸公式行段包裹 $$（需知道该行是否已在 display 内）"""
    # 用状态机求每行进入状态
    text = '\n'.join(lines)
    errs, b = scan(text)
    bare = {ln - 1 for ln, _ in b}             # 1-based 行号 → 0-based
    if not bare:
        return lines, False
    out, i, changed = [], 0, False
    while i < len(lines):
        if i in bare:
            j = i
            while j < len(lines) and (j in bare or (not lines[j].strip() and (j + 1) in bare)):
                j += 1
            out.append('$$')
            out.extend(lines[i:j])
            out.append('$$')
            changed = True
            i = j
        else:
            out.append(lines[i])
            i += 1
    return out, changed


def R3_fix_unclosed(lines):
    """未闭合 $$：开块后紧跟正文 → 删开块；否则在其后公式段末补闭合"""
    text = '\n'.join(lines)
    errs, _ = scan(text)
    e3 = [x for x in errs if x[0] == 'E3 未闭合$$']
    if not e3:
        return lines, False
    # 找最后一个独立 $$ 行（未配对的那个开块）
    dd = [i for i, L in enumerate(lines) if L.strip() == '$$']
    if not dd:
        # 行首 $$ 开块（同行有公式）→ 在末尾补 $$
        if re.match(r'^\s*\$\$', text):
            return lines + ['$$'], True
        return lines, False
    oi = dd[-1] if len(dd) % 2 == 1 else None
    if oi is None:
        return lines, False
    nxt = next((lines[j] for j in range(oi + 1, len(lines)) if lines[j].strip()), '')
    if nxt and not is_formula(nxt) and '$' not in nxt:
        return [L for k, L in enumerate(lines) if k != oi], True      # 删多余开块
    j = oi + 1
    while j < len(lines) and (is_formula(lines[j]) or not lines[j].strip()):
        j += 1
    return lines[:j] + ['$$'] + lines[j:], True


def R4_fix_e1(lines):
    """display 内出现单 $ → 删除该 $（逐行状态机定位）"""
    state = None
    changed = False
    for idx, L in enumerate(lines):
        newL, i = L, 0
        while i < len(newL):
            if newL.startswith('$$', i):
                state = None if state == 'display' else ('display' if state is None else state)
                i += 2
                continue
            if newL[i] == '$':
                if state == 'display':
                    newL = newL[:i] + newL[i + 1:]
                    changed = True
                    continue
                state = None if state == 'inline' else ('inline' if state is None else state)
            i += 1
        lines[idx] = newL
    return lines, changed


def R5_fix_e2(lines):
    """inline 内出现 $$ → 降级为单 $"""
    state = None
    changed = False
    for idx, L in enumerate(lines):
        newL, i = L, 0
        while i < len(newL):
            if newL.startswith('$$', i):
                if state == 'inline':
                    newL = newL[:i] + '$' + newL[i + 2:]
                    changed = True
                    state = None
                    i += 1
                    continue
                state = None if state == 'display' else ('display' if state is None else state)
                i += 2
                continue
            if newL[i] == '$':
                state = None if state == 'inline' else ('inline' if state is None else state)
            i += 1
        lines[idx] = newL
    return lines, changed


def fix_field(text):
    orig = text
    lines = text.split('\n')
    hits = []
    for rnd in range(6):
        e, b = errs_of('\n'.join(lines))
        if not e and not b:
            break
        for name, fn in (('R1', R1_merge_dd), ('R2', R2_wrap_bare), ('R3', R3_fix_unclosed),
                         ('R4', R4_fix_e1), ('R5', R5_fix_e2)):
            lines2, ch = fn(lines)
            if ch:
                lines = lines2
                hits.append('%s(第%d轮)' % (name, rnd + 1))
                break
        else:
            break
    new = '\n'.join(lines)
    e, b = errs_of(new)
    if e or b:
        return orig, ['!! 复检未过，回滚（剩 %d err + %d 裸行）' % (len(e), len(b))]
    return new, hits


if __name__ == '__main__':
    from collections import Counter
    stats = Counter()
    samples = []
    for tag, path, iterate in (('core', BASE + 'core_bank.json', lambda d: [(q, q) for s in d[0]['sections'] for q in s['questions']]),
                               ('exam', BASE + 'exam.json', lambda d: [(q, q) for v in d for s in v.get('sections', []) for q in s.get('questions', [])])):
        d = json.load(io.open(path, encoding='utf-8'))
        for _, q in iterate(d):
            for f in ('stem', 'answer', 'idea'):
                v = q.get(f) or ''
                if not v:
                    continue
                e, b = errs_of(v)
                if not e and not b:
                    continue
                new, hits = fix_field(v)
                if new != v and not any(h.startswith('!!') for h in hits):
                    stats[tag + ' 修好'] += 1
                    if len(samples) < 5:
                        samples.append((tag, q.get('no'), f, hits))
                else:
                    stats[tag + ' 未修好'] += 1
    print('=== dry-run 结果 ===')
    for k, v in sorted(stats.items()):
        print('  %-14s %d' % (k, v))
    print()
    for s in samples:
        print('  样例 %s 第%s题.%s → %s' % s)
