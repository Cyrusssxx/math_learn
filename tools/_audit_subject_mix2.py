#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全量排查「学科混入」：以 linkedQid 为锚，找出同一道真题在 core_bank 里
被挂了与真题侧不同学科知识点的题 —— 这是「线代分类里混入高数」的精确信号。

原理：题目的 linkedQid 指向真题侧的同题，真题侧的知识点归属是可信基准。
      若 core 侧挂的学科与真题侧不一致，说明 core 侧的 categoryIds 错了。

同时输出三类清单：
  A. 跨库学科矛盾（强信号，可直接判错）
  B. 题干学科 vs 挂载学科矛盾（弱信号，需人工复核）
  C. section 与挂载学科矛盾
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
CATS = os.path.join(ROOT, 'pwa/data/exam_categories.json')

HI_WORDS = ['\\int', '\\iint', '\\lim', '积分', '导数', '极限', '连续', '微分', '偏导',
            '级数', '二重积分', '曲线', '定积分', '不定积分', '泰勒', '洛必达', '中值定理',
            '渐近线', '曲率', '单调', '凹凸', '一阶线性', '通解', '特解']
LA_WORDS = ['矩阵', '行列式', '向量', '特征值', '特征向量', '秩', '可逆', '线性无关',
            '线性相关', '二次型', '方程组', '相似', '合同', '转置', '伴随', '初等变换',
            '分块', '迹', '基础解系', '齐次', '非齐次']


def make_catmap():
    cats = json.loads(io.open(CATS, encoding='utf-8').read())
    m = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    if not all(isinstance(v, dict) for v in list(m.values())[:3]):
        m = {str(c['id']): c for c in m.get('categories', [])}
    return m


def subject_of(cid, catmap):
    c = catmap.get(str(cid))
    n = 0
    while c and c.get('level', 0) > 0 and n < 6:
        c = catmap.get(str(c.get('parentId')))
        n += 1
    return c.get('name') if c else None


def path_of(cid, catmap):
    c = catmap.get(str(cid))
    out = []
    while c and len(out) < 5:
        out.append(c.get('display') or c.get('name'))
        c = catmap.get(str(c.get('parentId')))
    return ' / '.join(reversed(out))


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    catmap = make_catmap()

    # 真题侧索引：qid → 题目
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q

    cqs = [q for s in cb[0]['sections'] for q in s['questions']]

    def subs_of(q):
        return [subject_of(c, catmap) for c in (q.get('categoryIds') or [])]

    print('=== A. 跨库学科矛盾（linkedQid 指向的真题挂另一学科）===')
    A = []
    for q in cqs:
        lq = q.get('linkedQid')
        if not lq:
            continue
        z = zp.get(lq)
        if not z:
            continue
        core_subs = set(x for x in subs_of(q) if x in ('高等数学', '线性代数'))
        zhen_subs = set(x for x in subs_of(z) if x in ('高等数学', '线性代数'))
        if core_subs and zhen_subs and core_subs != zhen_subs:
            A.append((q['no'], q.get('fromX'), lq, sorted(core_subs), sorted(zhen_subs),
                      [path_of(c, catmap) for c in (q.get('categoryIds') or [])],
                      [path_of(c, catmap) for c in (z.get('categoryIds') or [])],
                      str(q.get('source'))[:24], (q.get('stem') or '').replace('\n', ' ')[:70]))
    print('数量 =', len(A))
    for t in A:
        print('  no=%-5s fromX=%-5s ← %s' % (t[0], t[1], t[2]))
        print('      core挂: %s' % ' | '.join(t[5]))
        print('      真题挂: %s' % ' | '.join(t[6]))
        print('      src=%s  %s' % (t[7], t[8]))

    print()
    print('=== B. 题干学科 vs 挂载学科矛盾（弱信号）===')
    B = []
    for q in cqs:
        subs = [x for x in subs_of(q) if x in ('高等数学', '线性代数')]
        if not subs:
            continue
        t = (q.get('stem') or '')
        hi = sum(t.count(w) for w in HI_WORDS)
        la = sum(t.count(w) for w in LA_WORDS)
        all_la = all(x == '线性代数' for x in subs)
        all_hi = all(x == '高等数学' for x in subs)
        if all_la and hi > la and hi >= 2:
            B.append(('线代挂载/题干像高数', q['no'], q.get('fromX'), hi, la, str(q.get('source'))[:22], t.replace('\n', ' ')[:70]))
        elif all_hi and la > hi and la >= 3:
            B.append(('高数挂载/题干像线代', q['no'], q.get('fromX'), hi, la, str(q.get('source'))[:22], t.replace('\n', ' ')[:70]))
    print('数量 =', len(B))
    for t in B:
        print('  [%s] no=%-5s fromX=%-5s 高数词%d/线代词%d src=%s' % (t[0], t[1], t[2], t[3], t[4], t[5]))
        print('        %s' % t[6])

    print()
    print('=== C. section 与挂载学科矛盾 ===')
    LA_SEC = {'行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'}
    C = []
    for s in cb[0]['sections']:
        for q in s['questions']:
            subs = [x for x in subs_of(q) if x in ('高等数学', '线性代数')]
            if not subs:
                continue
            sec_la = s['title'] in LA_SEC
            if all(x == '线性代数' for x in subs) != sec_la:
                C.append((s['title'], q['no'], q.get('fromX'), subs, str(q.get('source'))[:22], (q.get('stem') or '').replace('\n', ' ')[:60]))
    print('数量 =', len(C))
    for t in C[:20]:
        print('  [%s] no=%s fromX=%s 挂=%s src=%s' % (t[0], t[1], t[2], t[3], t[4]))
        print('        %s' % t[5])
    return 0


if __name__ == '__main__':
    sys.exit(main())
