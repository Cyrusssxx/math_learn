#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""查 core_bank 里是否混入了「级数」题（G 章，数二不考）。
用宽松关键词命中后人工复核，避免正则误伤（如 \sum 出现在非级数题里）。
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')

# 用「子串」而非正则，彻底避开转义坑
KEYS = ['级数', '收敛半径', '收敛域', '幂级数', '收敛区间', '数项级数', '正项级数',
        '交错级数', '和函数', '泰勒级数', '傅里叶', '收敛于', '发散的', '绝对收敛', '条件收敛']


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    secs = cb[0]['sections']
    loc = {q['no']: s['title'] for s in secs for q in s['questions']}
    qs = [q for s in secs for q in s['questions']]

    hits = []
    for q in qs:
        blob = (q.get('stem') or '') + '\n' + (q.get('answer') or '') + '\n' + (q.get('idea') or '')
        k = next((k for k in KEYS if k in blob), None)
        if k:
            hits.append((q['no'], loc[q['no']], bool(q.get('fromX')), k, (q.get('stem') or '').replace('\n', ' ')[:64]))
    print('命中关键词的题 = %d 道' % len(hits))
    print()
    for no, t, fx, k, s in hits:
        print('  no=%-5s [%-10s] %s 「%s」 %s' % (no, t, 'fromX' if fx else '严选 ', k, s))
    print()
    # 按节统计
    import collections
    c = collections.Counter(t for _, t, _, _, _ in hits)
    print('按现存节分布：', dict(c))
    # 严选题（no<=742 且非 fromX）里的命中
    yan = [(no, t, k, s) for no, t, fx, k, s in hits if not fx]
    print()
    print('其中「严选」（非 fromX）= %d 道' % len(yan))
    for no, t, k, s in yan:
        print('   no=%-5s [%-10s] %s' % (no, t, s))
    return 0


if __name__ == '__main__':
    sys.exit(main())
