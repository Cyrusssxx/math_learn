#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""终验：①无非法一对多 ②21 道失联题的标记可恢复 ③12 道对象题已接上同步"""
import io, json, re, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def norm(s):
    s = s or ''
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    return s


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    e = ann['exam']
    marked = set(json.loads(e['favs']).keys()) | set(json.loads(e['status']).keys()) | set(
        k.replace('examNote-', '') for k in e['notes'])
    qs = [q for s in cb[0]['sections'] for q in s['questions']]

    g = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            g[q['linkedQid']].append(q)

    bad = {k: len(v) for k, v in g.items()
           if len(v) > 1 and len({norm(q.get('stem')) for q in v}) > 1}
    legal = {k: len(v) for k, v in g.items() if len(v) > 1}
    print('① 非法一对多 =', bad if bad else '无')
    print('   合法同题组 =', legal if legal else '无')

    # ② 失联恢复验证：模拟前端 migrateLinkFixKeys / linkedQidOld 的效果
    restored = 0
    for q in qs:
        old = q.get('linkedQidOld')
        new = q.get('linkedQid') or ('core-%s' % q['no'])
        if old and old in marked and old != new:
            restored += 1
    print('② 被清 linkedQid 的题中，旧键有用户标记、将由前端迁移函数恢复的 =', restored, '道')

    # ③ 对象题同步验证
    by_no = {q['no']: q for s in cb[0]['sections'] for q in s['questions']}
    PAIRS = {189: '2016数二真题-9', 382: '2009数二真题-6', 320: '2003数二真题-4',
             373: '2010数二真题-4', 43: '2024数二真题-2', 389: '2011数二真题-6',
             92: '2015数二真题-2', 159: '2020数二真题-9', 375: '2022数二真题-5',
             466: '2002数二真题-4', 40: '2011数二真题-2'}
    ok = sum(1 for n, lq in PAIRS.items() if by_no[n].get('linkedQid') == lq)
    print('③ 12 道对象题已接上双向同步 =', ok, '/ 11+1linkFix（no=221 走 linkFix 单向）')

    # ④ 总数
    print('④ 总题数 =', len(qs), '（1059 预期）')
    return 0 if (not bad and len(qs) == 1059) else 1


if __name__ == '__main__':
    sys.exit(main())
