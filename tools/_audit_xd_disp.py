#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""对「混入线代的 20 道高数题」做处置判定 + 全文查重。
  1. 是否会与 core 既有的高数题重复（linkedQid 是否已被非 fromX 题引用 / 题干相同）
  2. xd 并入题内部的重复（题干完全相同）
  3. 用户是否在这 20 道上有标记（有则不能简单删）
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
CATS = os.path.join(ROOT, 'pwa/data/exam_categories.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'

HI = ['\\lim', '\\int', '\\iint', '\\oint', '渐近线', '曲率', '极值', '凹凸', '拐点',
      '定积分', '不定积分', '二重积分', '反常积分', '偏导', '全微分', '泰勒', '洛必达',
      '中值定理', '单调', '无穷小', '数列极限', '微分方程', '通解', '特解', '导数',
      '\\dfrac{d', '面积', '体积', '弧长', '旋转体']
LA = ['矩阵', '行列式', '向量', '特征值', '特征向量', '秩', '可逆', '转置', '伴随',
      '初等变换', '分块', '二次型', '线性无关', '线性相关', '基础解系', '齐次', '非齐次',
      '正交', '合同', '相似', '迹', '方阵', '单位阵', '对角', '方程组', '解向量',
      '线性表示', '极大无关组', 'E$', '|A|', 'A^', 'A^{-1}', '\\alpha_', '\\beta_']


def norm_stem(s):
    s = re.sub(r'\s+', '', s or '')
    s = re.sub(r'\\underline\{?\\?h?space\{[^}]*\}?\}?', '', s)
    return s


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    cats = json.loads(io.open(CATS, encoding='utf-8').read())
    catmap = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    if not all(isinstance(v, dict) for v in list(catmap.values())[:3]):
        catmap = {str(c['id']): c for c in catmap.get('categories', [])}
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    ex = ann['exam']
    marked = set(json.loads(ex['favs']).keys()) | set(json.loads(ex['status']).keys()) | set(
        k.replace('examNote-', '') for k in ex['notes'])

    def subj_of(cid):
        c = catmap.get(str(cid))
        n = 0
        while c and c.get('level', 0) > 0 and n < 6:
            c = catmap.get(str(c.get('parentId')))
            n += 1
        return c.get('name') if c else None

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    # 1) 混入题清单
    mix = []
    for s in cb[0]['sections']:
        for q in s['questions']:
            subs = [subj_of(c) for c in (q.get('categoryIds') or [])]
            if not subs or not all(x == '线性代数' for x in subs):
                continue
            t = q.get('stem') or ''
            if [w for w in HI if w in t] and not [w for w in LA if w in t]:
                mix.append((s['title'], q))
    print('=== 混入题 %d 道 · 处置判定 ===' % len(mix))

    # linkedQid 被非 fromX 题引用 → 说明 core 里已有同题（在正确位置）
    link_owner = {}
    for q in qs:
        if q.get('linkedQid') and not q.get('fromX'):
            link_owner.setdefault(q['linkedQid'], []).append(q['no'])
    # 题干重复索引
    by_norm = collections.defaultdict(list)
    for q in qs:
        by_norm[norm_stem(q.get('stem'))].append(q)

    dup_with_core, dup_inside, solo = [], [], []
    for sec, q in mix:
        lq = q.get('linkedQid')
        same = [x for x in by_norm[norm_stem(q.get('stem'))] if x['no'] != q['no']]
        owner = link_owner.get(lq, []) if lq else []
        if owner:
            dup_with_core.append((sec, q, lq, owner))
        elif same:
            dup_inside.append((sec, q, [x['no'] for x in same]))
        else:
            solo.append((sec, q))

    print()
    print('--- ① 与 core 已有题重复（linkedQid 已被非 fromX 题占用）: %d 道 ---' % len(dup_with_core))
    for sec, q, lq, owner in dup_with_core:
        print('  no=%-5s(原xd-%-6s) 节[%s] linkedQid=%s → core 已有 no=%s' % (q['no'], q.get('xdNo'), sec, lq, owner))
    print()
    print('--- ② xd 内部重复（题干与其它并入题相同）: %d 道 ---' % len(dup_inside))
    for sec, q, same in dup_inside:
        print('  no=%-5s(原xd-%-6s) 节[%s] 与 no=%s 题干相同' % (q['no'], q.get('xdNo'), sec, same))
    print()
    print('--- ③ 独立新增（core 无同题）: %d 道 ---' % len(solo))
    for sec, q in solo:
        m = '有标记' if ('core-%s' % q['no']) in marked else (
            '有标记(旧键)' if ('xd-%s' % q.get('xdNo')) in marked else '')
        print('  no=%-5s(原xd-%-6s) 节[%-10s] src=%-22s %s' % (
            q['no'], q.get('xdNo'), sec, str(q.get('source'))[:22], m))
        print('        %s' % (q.get('stem') or '').replace('\n', ' ')[:76])

    # 3) xd 内部全体重复检查（不限混入题）
    print()
    print('=== xd 并入题内部题干重复（全体 333 道）===')
    dupn = 0
    for norm, group in by_norm.items():
        fx = [q for q in group if q.get('fromX')]
        if len(fx) > 1 and norm:
            dupn += 1
            print('  题干相同的组: %s' % [('%s(xd-%s)' % (q['no'], q.get('xdNo'))) for q in fx])
    print('  重复组数 =', dupn)
    return 0


if __name__ == '__main__':
    sys.exit(main())
