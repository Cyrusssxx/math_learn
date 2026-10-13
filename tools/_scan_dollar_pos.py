#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""逐字符扫描：精确定位每个字段里 `$$` 出现的位置与上下文（跳过 \\$ 转义）。
只读，用于判定修复方案。
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')


def scan(v):
    """返回 [(pos, line_no, ctx)]，ctx 为前后 26 字符"""
    out, i, n, line = [], 0, len(v), 1
    while i < n:
        ch = v[i]
        if ch == '\n':
            line += 1
            i += 1
            continue
        if ch == '\\':
            i += 2
            continue
        if ch == '$' and i + 1 < n and v[i + 1] == '$':
            out.append((i, line, v[max(0, i - 26):i].replace('\n', '⏎') + ' ⟦$$⟧ '
                        + v[i + 2:i + 26].replace('\n', '⏎')))
            i += 2
            continue
        i += 1
    return out


def main():
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    papers = ex if isinstance(ex, list) else ex.get('papers', [])
    targets = []
    for p in papers:
        for s in p['sections']:
            for q in s['questions']:
                for field in ('stem', 'answer', 'idea'):
                    v = q.get(field)
                    if v and v.count('$$') % 2 == 1:
                        targets.append((p['id'], q['no'], field, v))
    for pid, no, field, v in targets:
        hits = scan(v)
        print('=' * 92)
        print('%s Q%s [%s]  $$ 共 %d 个' % (pid, no, field, len(hits)))
        for idx, (pos, ln, ctx) in enumerate(hits):
            print('  #%-2d 字符位置=%-6d 行=%-3d %s' % (idx + 1, pos, ln, ctx))
    return 0


if __name__ == '__main__':
    sys.exit(main())
