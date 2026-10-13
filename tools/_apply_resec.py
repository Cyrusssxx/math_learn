#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""按书归属重排节归属 —— DRY-RUN 预演（默认不改数据，--apply 才写）。

范围与不动项（关键）：
  · 只处理 no ∈ [1,600]（大观严选题书内区间）
  · no 601~742（补充题库：姜晓千150/660/880/900题）**不动** —— 不在书里，无书归属
  · no 743~1075（线代重点题 fromX）**不动**
  · **不改 no / catId / linkedQid / linkAlias / 任何标记字段** —— 只把题挪到别的 section

安全性（已在 category.js 核实）：
  · 收藏/笔记主键 = linkedQid 或 'core-<no>'，**与所属 section 无关**
  · advice.js 统计用 categoryIds（catId），**不看 section**
  · section 只影响 core 模式的题卡来源标签与分组展示
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
PLAN = os.path.join(ROOT, 'tools/_resec_plan.json')
ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程']


def main():
    apply = '--apply' in sys.argv
    strict = '--all' not in sys.argv        # 默认只改相邻章（更保守）
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    plan = json.loads(io.open(PLAN, encoding='utf-8').read())
    sec_of = {int(k): v for k, v in plan['plan'].items()}      # no -> 应属节（仅 1~600）

    secs = cb[0]['sections']
    bytitle = {s['title']: s for s in secs}
    before = {s['title']: len(s['questions']) for s in secs}

    # 逐题判定新归属
    moves = []
    skipped = []
    newq = {t: [] for t in bytitle}
    for s in secs:
        for q in s['questions']:
            tgt = sec_of.get(q['no'], s['title'])       # 不在方案内的保持原节
            if tgt != s['title']:
                # ⚠️ DP 只保证「段的主节」正确，段内个别题可能是**真跨章题**
                #    （书里 A 章末尾放道多元最值题做综合，很正常）。
                #    跨 2 章以上的改动极可能是 DP 误判 → 默认跳过（--all 可强制全改）。
                gap = abs(ORDER.index(tgt) - ORDER.index(s['title']))
                if strict and gap > 1 and s['title'] in ORDER:
                    skipped.append((q['no'], s['title'], tgt,
                                    (q.get('stem') or '').replace('\n', ' ')[:52]))
                    newq[s['title']].append(q)
                    continue
                moves.append((q['no'], s['title'], tgt, (q.get('stem') or '').replace('\n', ' ')[:52]))
            newq[tgt].append(q)

    # 各节内按 no 升序（与现状一致）
    for t in newq:
        newq[t].sort(key=lambda q: q['no'])

    print('=== 预演：待改题 %d 道（占书内 %.0f%%）｜跳过（跨≥2章，疑 DP 误判）%d 道 ===' % (
        len(moves), 100.0 * len(moves) / 600, len(skipped)))
    print()
    print('%-12s %8s %8s %8s' % ('节', '原题数', '新题数', '增减'))
    for t in [s['title'] for s in secs]:
        b, a = before[t], len(newq[t])
        d = a - b
        print('%-12s %8d %8d %+8d' % (t, b, a, d))
    print('%-12s %8d %8d' % ('合计', sum(before.values()), sum(len(v) for v in newq.values())))
    print()
    print('=== 迁移矩阵（原节 → 新节）===')
    mx = collections.Counter((f, t) for _, f, t, _ in moves)
    for (f, t), n in mx.most_common():
        print('   %-10s → %-10s %d 题' % (f, t, n))
    print()
    print('=== 待改题样例（前 24）===')
    for no, f, t, st in sorted(moves)[:24]:
        print('   no=%-4s %-10s→%-10s %s' % (no, f, t, st))
    if skipped:
        print()
        print('=== 跳过（保留原节，跨≥2章疑误判，前 12）===')
        for no, f, t, st in sorted(skipped)[:12]:
            print('   no=%-4s 保持 %-10s（DP 想改到 %-10s） %s' % (no, f, t, st))

    # ---- 自检 ----
    allno = sorted(q['no'] for v in newq.values() for q in v)
    assert len(allno) == len(set(allno)), 'no 重复'
    assert len(allno) == sum(before.values()), '题数不守恒'
    print()
    print('✅ 自检：题数守恒 %d，no 无重复' % len(allno))
    # 只有 6 个高数节被改，线代节应零变动
    lin = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型']
    bad = [t for t in lin if before[t] != len(newq[t])]
    print('✅ 自检：线代 6 节零变动' if not bad else '❌ 线代节被动过: %s' % bad)

    if not apply:
        print()
        print('（DRY-RUN，未写文件。确认后加 --apply 执行）')
        return 0

    for s in secs:
        s['questions'] = newq[s['title']]
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print()
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
