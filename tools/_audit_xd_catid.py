#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""定位 xd 并入题的 categoryIds 错误模式：
   xd 原 section（PDF 章节「一、行列式」等） vs categoryIds 上溯到的章（level 1）vs 学科。
   若「原节 ∉ 挂载知识点所属章」，说明映射错位而非个别笔误。
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
CATS = os.path.join(ROOT, 'pwa/data/exam_categories.json')

SEC2KEY = {'行列式': '行列式', '矩阵': '矩阵', '向量': '向量',
           '线性方程组': '线性方程组', '特征值与特征向量': '特征值与特征向量', '二次型': '二次型'}


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    cats = json.loads(io.open(CATS, encoding='utf-8').read())
    catmap = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    if not all(isinstance(v, dict) for v in list(catmap.values())[:3]):
        catmap = {str(c['id']): c for c in catmap.get('categories', [])}

    def chap_of(cid):
        """上溯到 level 1（章）"""
        c = catmap.get(str(cid))
        n = 0
        while c and c.get('level', 0) > 1 and n < 6:
            c = catmap.get(str(c.get('parentId')))
            n += 1
        return c

    def subj_of(cid):
        c = chap_of(cid)
        if not c:
            return None
        g = catmap.get(str(c.get('parentId')))
        return g.get('name') if g else None

    print('=== xd 并入题：所在 section × 挂载知识点所属章 ===')
    x = collections.Counter()
    mism = []
    for s in cb[0]['sections']:
        for q in s['questions']:
            if not q.get('fromX'):
                continue
            chaps = []
            for cid in (q.get('categoryIds') or []):
                ch = chap_of(cid)
                chaps.append(ch.get('name') if ch else '?')
            for ch in set(chaps):
                x[(s['title'], ch)] += 1
            if any(c != s['title'] for c in chaps):
                mism.append((q['no'], q.get('xdNo'), s['title'], chaps,
                             str(q.get('source'))[:22], (q.get('stem') or '').replace('\n', ' ')[:64]))
    print('  交叉计数（行=section，列=挂载知识点的章）:')
    for (sec, ch), n in sorted(x.items()):
        flag = '' if sec == ch else '   <== 不一致'
        print('    %-14s × %-14s %4d%s' % (sec, ch, n, flag))
    print()
    print('=== 不一致的题：共 %d 道 ===' % len(mism))
    for t in mism[:40]:
        print('  no=%-5s(原xd-%s) 节[%s] 挂[%s]' % (t[0], t[1], t[2], ','.join(t[3])))
        print('      src=%s  %s' % (t[4], t[5]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
