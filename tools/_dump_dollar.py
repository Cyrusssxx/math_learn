#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""导出 exam.json 中所有 $$ 计数为奇数的字段全文，供逐处判断修复方案。只读。"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
OUT = os.path.join(ROOT, 'tools/_dollar_report.txt')


def main():
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    papers = ex if isinstance(ex, list) else ex.get('papers', [])
    L = []
    n = 0
    for p in papers:
        for s in p['sections']:
            for q in s['questions']:
                for field in ('stem', 'answer', 'idea'):
                    v = q.get(field)
                    if not v or v.count('$$') % 2 == 0:
                        continue
                    n += 1
                    L.append('=' * 90)
                    L.append('【%d】%s Q%s  [%s]  $$ 计数=%d' % (
                        n, p['id'], q['no'], field, v.count('$$')))
                    L.append('-' * 90)
                    L.append(v)
                    L.append('')
    io.open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
    print('共 %d 处，已写 %s' % (n, OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
