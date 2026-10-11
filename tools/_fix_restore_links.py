#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ③（用户报告：数二真题的标记/笔记在 core 模式下丢失）：

根因：修复①删掉的 15 道「与 core 既有题重复」的题，恰恰是**承担真题标记同步**的
     那份（它们有 linkedQid）；保留的"重复对象"（no=189/382/…）全部没有 linkedQid，
     从未与真题同步。删掉后用户在真题页做的标记/笔记，core 模式自然看不到了。

修法：给 12 道「重复对象」补 linkedQid（= 被删题的真题键，经核对为同题）。
     · 补齐后 core 侧与真题侧**双向同步**（收藏/标记/笔记），比 linkFix 单向复制更正确。
     · 特例 no=221：已有 linkedQid='2008数二真题-12'（另一道相似题），不覆盖；
       改用 linkFix 单向复制 2019数二真题-2 上的标记（当前无标记，防将来）。
     · 补前核对：目标 linkedQid 当前未被多题占用（避免重建一对多冲突）。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')

# 被删题号 → 其真题键；重复对象号
PAIRS = [
    (766, 189, '2016数二真题-9'),
    (825, 382, '2009数二真题-6'),
    (849, 320, '2003数二真题-4'),
    (865, 221, '2019数二真题-2'),
    (869, 373, '2010数二真题-4'),
    (892, 43, '2024数二真题-2'),
    (917, 389, '2011数二真题-6'),
    (962, 92, '2015数二真题-2'),
    (998, 159, '2020数二真题-9'),
    (1002, 375, '2022数二真题-5'),
    (1042, 466, '2002数二真题-4'),
    (1043, 40, '2011数二真题-2'),
]


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    by_no = {q['no']: q for q in qs}

    # 当前 linkedQid 占用（补齐后不得出现一对多）
    occ = collections.Counter(q['linkedQid'] for q in qs if q.get('linkedQid'))

    patched, skipped = [], []
    for del_no, keep_no, lq in PAIRS:
        kq = by_no.get(keep_no)
        if not kq:
            skipped.append((keep_no, '题不存在')); continue
        if kq.get('linkedQid'):
            # 已有别的关联（如 no=221 → 2008数二真题-12）：不覆盖，用 linkFix 单向复制
            kq['linkFix'] = {'from': lq}
            patched.append((keep_no, lq, 'linkFix（已有其他关联 %s）' % kq['linkedQid']))
            continue
        if occ.get(lq, 0) > 0:
            skipped.append((keep_no, 'linkedQid 已被 %d 道占用' % occ[lq])); continue
        kq['linkedQid'] = lq
        occ[lq] = 1
        patched.append((keep_no, lq, 'linkedQid（双向同步）'))

    print('=== 补齐真题关联 ===')
    for n, lq, how in patched:
        print('  no=%-5s ← %-20s  %s' % (n, lq, how))
    for n, why in skipped:
        print('  no=%-5s 跳过：%s' % (n, why))

    # 自检：不得出现一对多（「题干全部相同」的真同题组除外 —— 那是合法的同题多份）
    occ2 = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            occ2[q['linkedQid']].append(q)
    bad = {}
    def _norm(s):
        s = s or ''
        s = re.sub(r'\\[a-zA-Z]+', ' ', s)
        s = re.sub(r'[{}$\s\\]+', '', s)
        return s
    for k, v in occ2.items():
        if len(v) > 1:
            norms = {_norm(q.get('stem')) for q in v}
            if len(norms) > 1:
                bad[k] = len(v)
    if bad:
        print('❌ 自检失败（重建了一对多）:', bad)
        return 1
    print('✅ 自检通过（真同题组除外，无一对多冲突）')
    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
