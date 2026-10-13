#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""按「no 分块」重排节归属（2026-10-13 用户要求让归属正确）。

依据（已验证）：
  · no 是按章分块的 —— 每 40 题一段里主节占比 70~97%（no 1~600 为「大观严选题」）
  · no 601~742 是补充题库（姜晓千150/660/880/900题），不在书里，无书归属 → 不动
  · no 743~1075 是线代重点题（fromX）→ 不动

做法：
  1) 对 no ∈ [1,600] 用 DP 切成 6 段（A~F），目标是「段内与某单一节一致」的题数最大
     —— 段内占多数的那一节即该段的「应属节」
  2) 段内少数派的题即为「错位题」，可改到该段应属节
  3) 先出报告（不改数据），含每段边界、应属节、错位题数与样例
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
LO_HI = 600          # 大观严选题的书内区间上限（601~742 为补充题库）
ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程']


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    secs = cb[0]['sections']
    loc, byno = {}, {}
    for s in secs:
        for q in s['questions']:
            loc[q['no']] = s['title']
            byno[q['no']] = q
    N = LO_HI

    # 前缀和：[sec][pos]
    pref = {t: [0] * (N + 2) for t in ORDER}
    for n in range(1, N + 1):
        for t in ORDER:
            pref[t][n] = pref[t][n - 1] + (1 if loc.get(n) == t else 0)

    def cnt(lo, hi, t):
        return pref[t][hi] - pref[t][lo - 1]

    def best_of(lo, hi):
        return max((cnt(lo, hi, t), t) for t in ORDER)

    INF = -10 ** 9
    DP = [[INF] * (N + 2) for _ in range(7)]
    BK = [[0] * (N + 2) for _ in range(7)]
    for k in range(1, 7):
        for hi in range(1, N + 1):
            for lo in range(1, hi + 1):
                prev = 0 if k == 1 else DP[k - 1][lo - 1]
                if k > 1 and prev == INF:
                    continue
                b, _t = best_of(lo, hi)
                v = prev + b
                if v > DP[k][hi]:
                    DP[k][hi] = v
                    BK[k][hi] = lo

    segs = []
    hi = N
    for k in range(6, 0, -1):
        lo = BK[k][hi]
        segs.append((lo, hi))
        hi = lo - 1
    segs.reverse()

    print('=== DP 最优分块（no 1~%d 切 6 段）===' % N)
    tot_same = tot_bad = 0
    plan = []
    for (lo, hi), t in zip(segs, ORDER):
        b, bt = best_of(lo, hi)
        n = hi - lo + 1
        others = collections.Counter(loc.get(x) for x in range(lo, hi + 1) if loc.get(x) != bt)
        tot_same += b
        tot_bad += n - b
        print()
        print('【%s】no %d ~ %d（%d 题）｜段内一致 %d，错位 %d' % (bt, lo, hi, n, b, n - b))
        for k, v in others.most_common(6):
            print('     错位到 %-10s %d 题' % (k, v))
        plan.append((lo, hi, bt))
    print()
    print('合计：一致 %d，错位 %d（占书内 %.0f%%）' % (
        tot_same, tot_bad, 100.0 * tot_bad / N))
    print()
    print('=== 错位样例（每段前 6 条）===')
    for lo, hi, bt in plan:
        shown = 0
        for x in range(lo, hi + 1):
            if loc.get(x) and loc[x] != bt:
                q = byno[x]
                print('   no=%-4s 现=%-10s 应=%-10s %s' % (
                    x, loc[x], bt, (q.get('stem') or '').replace('\n', ' ')[:52]))
                shown += 1
                if shown >= 6:
                    break
        print()
    out = {'segments': [[lo, hi, bt] for lo, hi, bt in plan],
           'plan': {str(x): bt for lo, hi, bt in plan for x in range(lo, hi + 1)}}
    io.open(os.path.join(ROOT, 'tools/_resec_plan.json'), 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print('方案已写 tools/_resec_plan.json（仅书内 no≤%d，601~742 与线代不动）' % N)
    return 0


if __name__ == '__main__':
    sys.exit(main())
