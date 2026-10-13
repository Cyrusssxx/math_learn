#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""导出 core_bank「catId × 节」交叉表 + 每个 catId 的名字，用于判断节归属是否错乱。
另按 no（= 书序）列出每节的 no 分布，看同一节是否横跨全书。
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)


def main():
    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    cats = json.loads(io.open(P('exam_categories.json'), encoding='utf-8').read())
    cm = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    nm = lambda i: (cm.get(str(i)) or {}).get('name', '?')

    secs = cb[0]['sections']
    # catId -> 出现在哪些节
    owner = collections.defaultdict(list)
    for sec in secs:
        c = collections.Counter(q.get('catId') for q in sec['questions'])
        for cid, n in c.items():
            owner[cid].append((sec['title'], n))

    print('=== catId → 所属节 交叉表（按 catId 排序）===')
    print('%-7s %-20s %s' % ('catId', 'name', '出现在哪些节(题数)'))
    multi = []
    for cid in sorted(owner, key=lambda x: (len(owner[x]) > 1, x)):
        parts = ' | '.join('%s(%d)' % (t, n) for t, n in owner[cid])
        flag = '  ⚠️跨节' if len(owner[cid]) > 1 else ''
        print('%-7s %-20s %s%s' % (cid, nm(cid)[:20], parts, flag))
        if len(owner[cid]) > 1:
            multi.append(cid)
    print()
    print('跨节的 catId = %d 个：%s' % (len(multi), multi))
    print()
    print('=== 每节的 no（书序）分布 ===')
    for sec in secs:
        nos = sorted(q['no'] for q in sec['questions'])
        # 连续段
        segs = []
        s = prev = nos[0]
        for n in nos[1:]:
            if n == prev + 1:
                prev = n
                continue
            segs.append((s, prev))
            s = prev = n
        segs.append((s, prev))
        segs = [x for x in segs if x[1] - x[0] >= 0]
        txt = ','.join('%d-%d' % (a, b) if a != b else str(a) for a, b in segs[:14])
        print('  %-14s %3d 题  no: %s%s' % (
            sec['title'], len(nos), txt, ' …' if len(segs) > 14 else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
