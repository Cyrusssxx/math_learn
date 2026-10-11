#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""逐键明细对比：用户标注（真题侧键） vs core_bank 实际能读到的键。
输出「没同步」的每一处，并归类原因。

同步规则（qidOf）：
  core 题主键 = linkedQid（若有）否则 'core-<no>'
  ⇒ 用户标注键 K 能在 core 显示  ⟺  存在某 core 题，其主键 == K
未同步 = 用户标注键中，没有任何 core 题的主键等于它。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
CATS = os.path.join(ROOT, 'pwa/data/exam_categories.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    cats = json.loads(io.open(CATS, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    catmap = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    if not all(isinstance(v, dict) for v in list(catmap.values())[:3]):
        catmap = {str(c['id']): c for c in catmap.get('categories', [])}
    e = ann['exam']
    fav = json.loads(e['favs'])
    st = json.loads(e['status'])
    notes = e['notes']
    note_keys = set(k.replace('examNote-', '') for k in notes)

    # 真题侧全量（用于判断「core 里根本没这道题」）
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    core_keys = set()
    for q in qs:
        core_keys.add(q['linkedQid'] if q.get('linkedQid') else 'core-%s' % q['no'])

    def kinds(k):
        out = []
        if k in fav: out.append('收藏')
        if k in st: out.append('状态:' + st[k])
        if k in note_keys: out.append('笔记')
        return out

    allmark = (set(fav) | set(st) | note_keys)
    unsynced = sorted(k for k in allmark if k not in core_keys)
    synced = [k for k in allmark if k in core_keys]

    print('用户标注键总数 =', len(allmark))
    print('  ✓ 能在 core 模式显示（core 有同题）=', len(synced))
    print('  ✗ 不能在 core 显示 =', len(unsynced))
    print()

    # 归类
    in_exam = []      # 真题键，但 core 未收录该题
    dg = []           # DG 大观园键
    other = []        # 其他（xd/xd-号 等）
    for k in unsynced:
        if k in zp:
            in_exam.append(k)
        elif k.startswith('DG'):
            dg.append(k)
        else:
            other.append(k)

    print('=== 类别 1：真题里有、但 core_bank 未收录该题（%d 个）===' % len(in_exam))
    print('    ⇒ 属正常：core 题库没这道题，无法显示（可在真题页看）')
    # 按卷统计
    bypaper = collections.Counter(k.rsplit('-', 1)[0] for k in in_exam)
    for p, n in bypaper.most_common(12):
        print('     %-22s %d 个' % (p, n))
    print()
    print('   明细（前 25）：')
    for k in in_exam[:25]:
        q = zp.get(k)
        print('     %-20s %-14s %s' % (k, '+'.join(kinds(k)), (q.get('stem') or '').replace('\n', ' ')[:56]))
    print()

    print('=== 类别 2：DG 大观园键（%d 个）===' % len(dg))
    print('    ⇒ 大观园题库题，core 若未收录则不同步')
    for k in dg[:15]:
        print('     %-20s %s' % (k, '+'.join(kinds(k))))
    print()

    print('=== 类别 3：其他键（%d 个）===' % len(other))
    for k in other[:20]:
        print('     %-20s %s' % (k, '+'.join(kinds(k))))
    print()

    # 反向：core 题有主键但真题侧无对应（core 独有的题）
    zhen_keys = set(zp)
    core_only = [k for k in core_keys if k.startswith('core-')]
    print('（参考）core 侧独立键（无关联）数 =', len(core_only))
    return 0


if __name__ == '__main__':
    sys.exit(main())