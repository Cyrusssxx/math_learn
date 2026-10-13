#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""查清 core_bank 的 no 到底是什么顺序。
方法：按 no 分段统计各节占比，看 no 是否「按节分块连续」。
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    secs = cb[0]['sections']
    loc = {}
    for s in secs:
        for q in s['questions']:
            loc[q['no']] = s['title']
    nos = sorted(loc)
    print('no 范围 %d~%d，共 %d 题' % (nos[0], nos[-1], len(nos)))
    print()
    # 每 40 个 no 一段，统计节分布
    print('=== 按 no 分段（每 40）的节构成 ===')
    print('%-12s %s' % ('no 段', '节分布（前3）'))
    lo = nos[0]
    for start in range(1, 1081, 40):
        seg = [n for n in nos if start <= n < start + 40]
        if not seg:
            continue
        c = collections.Counter(loc[n] for n in seg)
        top = ', '.join('%s×%d' % (k, v) for k, v in c.most_common(3))
        print('%-12s %d 题  %s' % ('%d~%d' % (start, start + 39), len(seg), top))
    print()
    # 找「节切换点」：相邻 no 属不同节的位置
    sw = [n for a, n in zip(nos, nos[1:]) if loc[a] != loc[n]]
    print('=== 节切换点 %d 处（相邻 no 换节）===' % len(sw))
    print('  前 30 个切换点:', sw[:30])
    print()
    # 主要连续块
    print('=== 连续同节块（>=5 题，前 25 块）===')
    blocks = []
    cur_sec, cur_lo, prev = loc[nos[0]], nos[0], nos[0]
    for n in nos[1:]:
        if loc[n] != cur_sec:
            if prev - cur_lo + 1 >= 5:
                blocks.append((cur_lo, prev, cur_sec, prev - cur_lo + 1))
            cur_sec, cur_lo = loc[n], n
        prev = n
    if prev - cur_lo + 1 >= 5:
        blocks.append((cur_lo, prev, cur_sec, prev - cur_lo + 1))
    for a, b, s, n in blocks[:25]:
        print('   no %-4d ~ %-4d  %-10s %d 题' % (a, b, s, n))
    print('   …共 %d 块' % len(blocks))
    return 0


if __name__ == '__main__':
    sys.exit(main())
