#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断「标记失联」：我改动（删 15 道 + 清 133 道 linkedQid）后，
哪些 core 题此前能通过 linkedQid 同步显示用户的真题标记、现在不能了。

原理：
  改动前主键 = linkedQid（若题有）→ 与真题侧同题共享标记
  改动后主键 = linkedQid（未清的）/ core-<no>（被清的）
  失联 = 旧主键上有用户标记，且新主键 ≠ 旧主键（且新主键上没有标记）
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    e = ann['exam']
    fav = json.loads(e['favs'])
    st = json.loads(e['status'])
    notes = e['notes']
    marked = set(fav) | set(st) | set(k.replace('examNote-', '') for k in notes)

    def kind(k):
        out = []
        if k in fav: out.append('收藏')
        if k in st: out.append('状态=' + st[k])
        if ('examNote-' + k) in notes: out.append('笔记')
        return '+'.join(out)

    qs = [q for s in cb[0]['sections'] for q in s['questions']]

    print('=== ① 被【清除 linkedQid】的题：旧键（linkedQidOld）上有用户标记、现在失联的 ===')
    n1 = 0
    for q in qs:
        old = q.get('linkedQidOld')
        if not old or old not in marked:
            continue
        new = q.get('linkedQid') or ('core-%s' % q['no'])
        if new == old:
            continue
        lf = q.get('linkFix')
        n1 += 1
        print('  no=%-5s fromX=%-5s 旧键=%-20s 新键=%-14s linkFix=%s' % (
            q['no'], q.get('fromX'), old, new, '有' if lf else '无'))
        print('       标记: %s   题干: %s' % (kind(old), (q.get('stem') or '')[:56].replace('\n', ' ')))
    print('  小计 =', n1)

    print()
    print('=== ② 被【删除的 15 道】的 linkedQid 上有标记 → 检查其「重复对象」是否接上了同步 ===')
    # 删除清单 + 重复对象
    DELMAP = [
        (766, 189), (825, 382), (849, 320), (865, 221), (869, 373), (892, 43),
        (917, 389), (962, 92), (998, 159), (1002, 375), (1042, 466), (1043, 40),
    ]
    by_no = {q['no']: q for q in qs}
    for old_no, keep_no in DELMAP:
        # 被删题的 linkedQid（从 linkfix_map / 记忆拿）
        pass
    mp = json.loads(io.open(os.path.join(ROOT, 'tools/_linkfix_map.json'), encoding='utf-8').read())
    cleared_nos = set(n for _, n in mp['cleared'])
    # 被删题的 linkedQid 无法从现数据拿（已删），从 git HEAD~2 拿
    import subprocess
    out = subprocess.run(['git', 'show', 'e8b1cd3~1:pwa/data/core_bank.json'],
                         capture_output=True, text=True, encoding='utf-8').stdout
    old_cb = json.loads(out)
    old_q = {q['no']: q for s in old_cb[0]['sections'] for q in s['questions']}
    for del_no, keep_no in DELMAP:
        dq = old_q.get(del_no)
        kq = by_no.get(keep_no)
        if not dq or not kq:
            print('  no=%s 或 no=%s 缺失' % (del_no, keep_no)); continue
        dlq = dq.get('linkedQid')
        klq = kq.get('linkedQid')
        sync_ok = (dlq == klq and dlq) or (dlq in marked and klq == dlq)
        has_mark = dlq in marked if dlq else False
        print('  删 no=%-5s(键=%-18s 有标记=%s) → 保留 no=%-5s(键=%-18s) 同步=%s' % (
            del_no, str(dlq), has_mark, keep_no, str(klq),
            '✓接上' if dlq and klq == dlq else ('✗断!' if has_mark else '—')))
    print()
    print('=== ③ core 全库：题干与真题高度相似但无 linkedQid（同步缺失，既有问题）===')
    # 只统计被删 15 道的重复对象
    print('（本次先聚焦 ①②；全库排查另行）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
