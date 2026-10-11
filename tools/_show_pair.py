#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""打印若干 (真题键, core no) 对的完整题干，供人工核对是否同题。"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')

PAIRS = [
    ('2017数二真题-20', 493),
    ('2016数二真题-18', 494),
    ('2015数二真题-18', 468),
    ('2024数二真题-4', 69),
    ('2008数二真题-5', 66),
    ('2019数二真题-23', 994),
    ('2019数二真题-12', 344),
    ('2007数二真题-4', 134),
    ('2022数二真题-3', 207),
    ('2009数二真题-7', 831),
    ('2018数二真题-8', 833),
    ('2024数二真题-18', 558),
    ('2007数二真题-24', 1016),
]


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q
    cq = {q['no']: q for s in cb[0]['sections'] for q in s['questions']}

    for k, no in PAIRS:
        a, b = zp.get(k), cq.get(no)
        print('=' * 78)
        print('真题 %s   ⟨⟨⟨   core no=%s  (当前 key=%s)' % (
            k, no, b.get('linkedQid') or ('core-%s' % no)))
        print('--- 真题 ---')
        print((a.get('stem') or '').strip()[:420])
        print('--- core ---')
        print((b.get('stem') or '').strip()[:420])
    return 0


if __name__ == '__main__':
    sys.exit(main())
