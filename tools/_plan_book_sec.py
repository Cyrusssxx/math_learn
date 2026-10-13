#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""用「书序单调性 + 动态规划」求每道题的按书章归属（最鲁棒的做法）。

原理：
  · no 就是书序（已验证 97% 单调）→ 每道题在书里的**章**按 no 单调不减（A→B→…→F）
  · 全库只需 6 个**分段边界**（A|B、B|C、C|D、D|E、E|F 共 5 个切点）
  · 用锚点（能可靠判定章的题）做监督，DP 求「让锚点误判最少」的一组边界
    —— 把噪声摊到 5 个参数上，比逐题判定鲁棒得多

锚点来源：tools/_order_diag3.json（章级确定，47 条，最可靠）。
DP：把 no∈[1,742] 切成 6 段，段内章相同，使锚点命中数最大。
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)
DIAG3 = os.path.join(ROOT, 'tools/_order_diag3.json')

ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程']
SEC2CH = {'A. 函数极限连续': '极限', 'B. 一元微分': '一元微分', 'C. 一元积分': '一元积分',
          'D. 多元微分': '多元微分', 'E. 二重积分': '二重积分', 'F. 微分方程': '微分方程'}
MAXNO = 742          # 大观严选题区间（743+ 是并入的线代题，无书归属）


def main():
    rows = json.loads(io.open(DIAG3, encoding='utf-8').read())   # [[no, want, got], ...]
    # 锚点：want 是书章（6 章之一）→ 可信
    anchor = []
    for no, want, got in rows:
        if want in ORDER:
            anchor.append((no, ORDER.index(want)))
    anchor.sort()
    print('锚点 %d 个（章级确定）' % len(anchor))
    cnt = collections.Counter(a[1] for a in anchor)
    for i, ch in enumerate(ORDER):
        print('   %-10s %d' % (ch, cnt.get(i, 0)))
    print()

    # 预处理：每个位置 no 上各章的锚点数
    at = collections.defaultdict(lambda: [0] * 6)
    for no, ci in anchor:
        at[no][ci] += 1

    # 前缀和，便于 O(1) 求区间内某章锚点数
    pref = [[0] * 6 for _ in range(MAXNO + 2)]
    for n in range(1, MAXNO + 1):
        for c in range(6):
            pref[n][c] = pref[n - 1][c] + at[n][c]

    def cnt_in(lo, hi, c):
        return pref[hi][c] - pref[lo - 1][c]

    INF = -10 ** 9
    # DP[k][no] = 前 no 题切成 k 段（第 k 段以 no 结尾）的最大命中
    DP = [[INF] * (MAXNO + 2) for _ in range(7)]
    BK = [[0] * (MAXNO + 2) for _ in range(7)]
    for k in range(1, 7):
        c = k - 1
        for hi in range(1, MAXNO + 1):
            for lo in range(1, hi + 1):
                prev = 0 if k == 1 else DP[k - 1][lo - 1]
                if k > 1 and prev == INF:
                    continue
                v = prev + cnt_in(lo, hi, c)
                if v > DP[k][hi]:
                    DP[k][hi] = v
                    BK[k][hi] = lo

    best = DP[6][MAXNO]
    # 回溯边界
    bounds = []
    hi = MAXNO
    for k in range(6, 0, -1):
        lo = BK[k][hi]
        bounds.append((lo, hi, ORDER[k - 1]))
        hi = lo - 1
    bounds.reverse()
    print('=== DP 求出的按书分段（命中 %d / %d 个锚点）===' % (best, len(anchor)))
    for lo, hi, ch in bounds:
        print('   no %-4d ~ %-4d  %-10s  (%d 题)' % (lo, hi, ch, hi - lo + 1))
    print()

    # 逐段核对锚点命中
    print('=== 各段锚点命中情况 ===')
    for lo, hi, ch in bounds:
        c = ORDER.index(ch)
        tot = cnt_in(lo, hi, c)
        other = sum(cnt_in(lo, hi, x) for x in range(6)) - tot
        print('   %-10s 段内锚点 %2d 个（命中 %d，不符 %d）' % (ch, tot + other, tot, other))
    print()

    # 输出每题的按书归属
    sec_of = {}
    for lo, hi, ch in bounds:
        for n in range(lo, hi + 1):
            sec_of[n] = ch

    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    cur = {}
    for s in cb[0]['sections']:
        for q in s['questions']:
            cur[q['no']] = s['title']

    yan = [n for n in sec_of]
    same = [n for n in yan if cur.get(n) == sec_of[n]]
    diff = [(n, sec_of[n], cur.get(n)) for n in yan if cur.get(n) and cur[n] != sec_of[n]]
    print('=== 与现存节对比（no<=742）===')
    print('  一致 = %d（%.0f%%）' % (len(same), 100.0 * len(same) / len(yan)))
    print('  需改 = %d（%.0f%%）' % (len(diff), 100.0 * len(diff) / len(yan)))
    print()
    mx = collections.Counter((w, g) for _, w, g in diff)
    print('  迁移矩阵（按书 → 现存）：')
    for (w, g), n in mx.most_common(14):
        print('     %-10s → %-10s %d 题' % (w, g, n))
    io.open(os.path.join(ROOT, 'tools/_book_sec_plan.json'), 'w', encoding='utf-8').write(
        json.dumps({'bounds': bounds, 'secOf': {str(k): v for k, v in sec_of.items()},
                    'anchorHit': best, 'anchorTot': len(anchor)}, ensure_ascii=False))
    print()
    print('方案已写 tools/_book_sec_plan.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
