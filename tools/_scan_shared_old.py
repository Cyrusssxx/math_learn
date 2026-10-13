#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""扫描「linkedQidOld / linkFix.from 被多道题共享」—— 这是笔记串号的根因。

category.js 的 migrateLinkFixKeys() 对每道题：
    old = linkFix.from || linkedQidOld
    newKey = qidOf('core', q.no)
    if (fav[old] && !fav[newKey]) ...   // 收藏/状态/笔记 复制到 newKey
一道题的 old 唯一时无害；但若 N 道题共享同一个 old（历史遗留的错误关联被批量
清除时留下的），**同一份笔记会被复制到 N 道无关的题上** → 笔记串号。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    key_of = lambda q: q['linkedQid'] if q.get('linkedQid') else 'core-%s' % q['no']

    groups = collections.defaultdict(list)
    for q in qs:
        old = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if old:
            groups[old].append(q)

    shared = {k: v for k, v in groups.items() if len(v) > 1}
    print('有迁移线索的题 = %d 道，涉及旧键 %d 个' % (
        sum(len(v) for v in groups.values()), len(groups)))
    print('其中【被多题共享】的旧键 = %d 个，牵涉 %d 道题' % (
        len(shared), sum(len(v) for v in shared.values())))
    print()

    if not shared:
        print('✅ 无共享，迁移不会串号')
        return 0

    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    e = ann['exam']
    fav = json.loads(e['favs']); st = json.loads(e['status'])
    note_keys = set(k.replace('examNote-', '') for k in e['notes'])
    print('=== 共享组明细（只列旧键上有用户标记的）===')
    n_user = 0
    for old, lst in sorted(shared.items(), key=lambda x: -len(x[1])):
        has = []
        if old in fav: has.append('收藏')
        if old in st: has.append('状态:' + st[old])
        if old in note_keys: has.append('笔记')
        mark = '+'.join(has) or '—'
        if has:
            n_user += 1
        print('  旧键 %-20s 被 %2d 道题共享   该键上的用户数据: %s' % (old, len(lst), mark))
        for q in lst[:6]:
            print('      no=%-5s key=%-16s %s' % (q['no'], key_of(q),
                                                  (q.get('stem') or '').replace('\n', ' ')[:56]))
        if len(lst) > 6:
            print('      …另 %d 道' % (len(lst) - 6))
    print()
    print('>>> 其中【旧键上确有用户标记】的组 = %d 个 —— 这些组会真实串号' % n_user)
    return 0


if __name__ == '__main__':
    sys.exit(main())
