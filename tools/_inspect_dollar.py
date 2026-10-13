#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查 exam.json 中 answer 字段 $$ 不平衡的具体位置，打印上下文供人工判断。
只读，不写。
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')


def main():
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    papers = ex if isinstance(ex, list) else ex.get('papers', [])
    bad = []
    for p in papers:
        for s in p['sections']:
            for q in s['questions']:
                for field in ('stem', 'answer', 'idea'):
                    v = q.get(field)
                    if not v:
                        continue
                    n = v.count('$$')
                    if n % 2 == 1:
                        bad.append((p['id'], q['no'], field, n, v))
    print('$$ 计数为奇数的字段 = %d 处' % len(bad))
    print()
    for pid, no, field, n, v in bad:
        print('=' * 78)
        print('%s Q%s [%s]  $$ 计数=%d' % (pid, no, field, n))
        # 逐行找 $$ 位置
        lines = v.split('\n')
        for i, ln in enumerate(lines):
            if '$$' in ln:
                c = ln.count('$$')
                print('   L%-3d (%d个$$): %s' % (i, c, ln[:100]))
        print('   ---- 前后各 3 行 ----')
        for i, ln in enumerate(lines[:14]):
            print('   %2d│ %s' % (i, ln[:96]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
