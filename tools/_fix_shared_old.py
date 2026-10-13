#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ⑧：共享旧键导致的「笔记串号」（2026-10-13 用户报 413/414）。

根因：category.js 的 migrateLinkFixKeys() 对每道题都执行
      old = linkFix.from || linkedQidOld → 把 old 键的收藏/状态/笔记复制到该题主键。
     历史遗留让 **22 个旧键被 132 道题共享**（当年批量清除错误 linkedQid 时，
     同一批题都留下了同一个 old），于是同一份笔记被复制到 N 道无关的题上。
     实测：`2007数二真题-13`（y=1/(2x+3)）的笔记「n! 别忘了」被复制给了
     no=413/414（偏导数题）、93、294、434 —— 用户看到的就是这个。

处置：
  · 每组只保留「真同题」那一道的迁移线索，其余写成 linkedQidDead（仅留痕、不迁移）
  · 真同题归属 = tools/_shared_old_plan2.json（全库 sim>=0.90 反查）
                + MANUAL（人工判定：变量名/写法差异压低相似度的 3 组）
  · 非共享的 37 个旧键（一对一）保持原样，无害
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
PLAN2 = os.path.join(ROOT, 'tools/_shared_old_plan2.json')

# 人工判定：被变量名/写法差异压低相似度，但确为同题
MANUAL = {
    '2005数二真题-1':  163,   # y=(1+sin x)^x 求 dy|_{x=π}（真题侧写作 y'|_{x=π}，数学等价）
    '2007数二真题-13': 167,   # y=1/(2x+3) 求 y^(n)(0)（core 侧变量名写成 f(x)）
    '2012数二真题-10': 56,    # 黎曼和 lim n[1/(1²+n²)+…]（core 侧把 1² 简写成 1）
}


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    by_no = {q['no']: q for q in qs}
    plan = json.loads(io.open(PLAN2, encoding='utf-8').read())

    groups = collections.defaultdict(list)
    for q in qs:
        old = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if old:
            groups[old].append(q)

    shared = {k: v for k, v in groups.items() if len(v) > 1}
    single = {k: v for k, v in groups.items() if len(v) == 1}
    print('共享组 %d 个（%d 道题）｜独占键 %d 个（保持原样）' % (
        len(shared), sum(len(v) for v in shared.values()), len(single)))
    print()

    # 目标：old -> 允许迁移的 core no（None = 不迁移）
    target = {}
    for old in shared:
        if old in MANUAL:
            target[old] = MANUAL[old]
        else:
            t = plan.get(old) or []
            target[old] = t[0] if t else None

    n_keep = n_drop = 0
    for old, lst in shared.items():
        keep = target[old]
        for q in lst:
            cur = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
            if cur != old:
                continue
            if keep is not None and q['no'] == keep:
                # 保留迁移
                q['linkFix'] = {'from': old, 'reason': 'shared-old-keep'}
                q.pop('linkedQidOld', None)
                n_keep += 1
            else:
                # 改为不迁移（留痕）
                q['linkedQidDead'] = old
                q.pop('linkedQidOld', None)
                q.pop('linkFix', None)
                n_drop += 1

    # MANUAL 里指定的题，若当前线索指向别处，纠正过来
    for old, no in MANUAL.items():
        q = by_no.get(no)
        if not q:
            print('⚠️ MANUAL 指定的 no=%s 不存在' % no)
            continue
        cur = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if cur != old:
            print('纠正 no=%-5s 的迁移源：%s → %s' % (no, cur, old))
            if cur and cur in shared:
                # 原来是共享键的持有者，现在改指别处 → 旧的改成 dead
                q['linkedQidDead'] = cur
            q['linkFix'] = {'from': old, 'reason': 'manual-same-question'}
            q.pop('linkedQidOld', None)

    print('保留迁移 %d 道｜改判不迁移 %d 道' % (n_keep, n_drop))
    print()

    # 清理冗余：linkedQidOld 与 linkedQidDead 指向同一个死键时，删掉 linkedQidOld。
    # （_fix_bad_links2.py 的 PROMOTE 分支既写了 Dead 又留着早期的 Old，
    #   虽然 linkFix.from 优先级更高、实际不会迁移，但字段语义混乱。）
    n_clean = 0
    for q in qs:
        if q.get('linkedQidOld') and q.get('linkedQidOld') == q.get('linkedQidDead'):
            q.pop('linkedQidOld', None)
            n_clean += 1
    if n_clean:
        print('清理冗余 linkedQidOld（与 Dead 同值）= %d 道' % n_clean)
        print()

    # ---- 自检 ----
    g2 = collections.defaultdict(list)
    for q in qs:
        old = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if old:
            g2[old].append(q['no'])
    bad = {k: v for k, v in g2.items() if len(v) > 1}
    if bad:
        print('❌ 自检失败：仍有共享的迁移源', bad)
        return 1
    print('✅ 自检 1：每个迁移源都唯一（不会再串号）')
    # 死键不得同时是迁移源
    dupe = [q['no'] for q in qs if q.get('linkedQidDead')
            and ((q.get('linkFix') or {}).get('from') == q['linkedQidDead']
                 or q.get('linkedQidOld') == q['linkedQidDead'])]
    if dupe:
        print('❌ 自检失败：死键被当成迁移源', dupe)
        return 1
    print('✅ 自检 2：死键（linkedQidDead）不会被迁移')
    print('   现有迁移源 %d 个（全部唯一）｜死键 %d 个' % (
        len(g2), sum(1 for q in qs if q.get('linkedQidDead'))))

    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
