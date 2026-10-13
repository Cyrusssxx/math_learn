#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""内容裁决：对「DP 想改、当前未改」的题，用**题干/答案的内容特征**判断它到底属于哪一节，
   与 DP 的 want 比对：一致 → 改；不一致 → 保持（DP 误判）。

特征优先级（从强到弱，命中最高优先级者为准）：
  二重积分  : \iint / 二重积分
  多元微分  : \partial / f(x,y) 定义 / z=z(x,y) / 全微分
  微分方程  : 微分方程 / 通解 / 特解 / (y'' 且 y')
  一元积分  : \int（无 \iint）
  极限      : \lim
  一元微分  : 导数/可导/极值/拐点/渐近线/中值定理/泰勒
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
PLAN = os.path.join(ROOT, 'tools/_resec_plan.json')
ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程']


def classify(q):
    """返回内容特征判定的节名（None = 判不出）。
    ⚠️ 只按**题干**计数，不用答案——答案里的分步计算会含多个 \\int，会误判。
    ⚠️ 累次积分（\\int_0^1 dy\\int_y^1 ...）有**两个** \\int，属二重积分，必须先判。"""
    stem = q.get('stem') or ''
    blob = stem + '\n' + (q.get('answer') or '')[:400]
    has = lambda *ks: any(k in blob for k in ks)
    if has(r'\iint', '二重积分') or stem.count(r'\int') >= 2:
        return '二重积分'
    if has(r'\partial', '全微分', r'z=z(x,y)', r'z = z(x, y)', r'f(x,y)', r'f(x, y)', r'u(x,y)'):
        return '多元微分'
    if has('微分方程', '通解', '特解', '满足方程', r'y^{\prime\prime}', "y''", r'\mathrm{d}y'):
        return '微分方程'
    if has(r'\int', '不定积分', '定积分', '反常积分', '原函数', '积分上限'):
        return '一元积分'
    if has(r'\lim', '极限'):
        return '极限'
    if has('导数', '可导', '极值', '拐点', '渐近线', '中值定理', '泰勒', '单调'):
        return '一元微分'
    return None


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    plan = json.loads(io.open(PLAN, encoding='utf-8').read())
    sec_of = {int(k): v for k, v in plan['plan'].items()}
    secs = cb[0]['sections']
    loc, byno = {}, {}
    for s in secs:
        for q in s['questions']:
            loc[q['no']] = s['title']
            byno[q['no']] = q

    pend = [(n, loc[n], sec_of[n]) for n in sorted(sec_of)
            if n in loc and loc[n] != sec_of[n]]
    print('待内容裁决 = %d 道' % len(pend))
    print()
    conf, doubt = [], []
    for n, got, want in pend:
        q = byno[n]
        feat = classify(q)
        if feat == want:
            conf.append((n, got, want, feat, q))
        else:
            doubt.append((n, got, want, feat, q))

    print('=== 内容支持 DP（应改）= %d 道 ===' % len(conf))
    byg = collections.Counter()
    for n, got, want, feat, q in conf:
        byg[(got, want)] += 1
    for (g, w), c in byg.most_common():
        print('   %-10s → %-10s  %d 道' % (g, w, c))
    print()
    for n, got, want, feat, q in conf[:14]:
        print('   no=%-4s %-10s→%-10s [特征=%s] %s' % (
            n, got, want, feat, (q.get('stem') or '').replace('\n', ' ')[:44]))
    print()
    print('=== 内容不支持（保持不动）= %d 道 ===' % len(doubt))
    for n, got, want, feat, q in doubt[:14]:
        print('   no=%-4s 保持 %-10s (DP想 %-10s) [特征=%s] %s' % (
            n, got, want, feat, (q.get('stem') or '').replace('\n', ' ')[:40]))

    if not apply:
        print()
        print('（DRY-RUN，加 --apply 执行）')
        return 0

    # 执行：把 conf 里的题挪到目标节
    moved = 0
    for s in secs:
        keep = []
        for q in s['questions']:
            n = q['no']
            if n in {c[0] for c in conf}:
                tgt = sec_of[n]
                if tgt != s['title']:
                    for s2 in secs:
                        if s2['title'] == tgt:
                            s2['questions'].append(q)
                            break
                    moved += 1
                    continue
            keep.append(q)
        s['questions'] = keep
    for s in secs:
        s['questions'].sort(key=lambda q: q['no'])
    allno = sorted(q['no'] for s in secs for q in s['questions'])
    assert len(allno) == len(set(allno)), 'no 重复'
    assert len(allno) == 1059, '题数不守恒: %d' % len(allno)
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print()
    print('已移动 %d 道，题数守恒 1059 ✅，已写回 core_bank.json' % moved)
    return 0


if __name__ == '__main__':
    sys.exit(main())
