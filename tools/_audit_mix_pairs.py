#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""逐题人工核对：20 道混入题 vs core 既有高数题的最佳匹配（完整题干并排）。"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
CATS = os.path.join(ROOT, 'pwa/data/exam_categories.json')

HI = ['\\lim', '\\int', '\\iint', '\\oint', '渐近线', '曲率', '极值', '凹凸', '拐点',
      '定积分', '不定积分', '二重积分', '反常积分', '偏导', '全微分', '泰勒', '洛必达',
      '中值定理', '单调', '无穷小', '数列极限', '微分方程', '通解', '特解', '导数',
      '\\dfrac{d', '面积', '体积', '弧长', '旋转体']
LA = ['矩阵', '行列式', '向量', '特征值', '特征向量', '秩', '可逆', '转置', '伴随',
      '初等变换', '分块', '二次型', '线性无关', '线性相关', '基础解系', '齐次', '非齐次',
      '正交', '合同', '相似', '迹', '方阵', '单位阵', '对角', '方程组', '解向量',
      '线性表示', '极大无关组', 'E$', '|A|', 'A^', 'A^{-1}', '\\alpha_', '\\beta_']


def norm(s):
    s = s or ''
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    s = re.sub(r'（\s*）|\(\s*\)|_{2,}', '', s)
    return s


def bigrams(s):
    return set(s[i:i + 2] for i in range(len(s) - 1)) if len(s) > 1 else {s}


def jac(a, b):
    A, B = bigrams(a), bigrams(b)
    return len(A & B) / len(A | B) if (A and B) else 0.0


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    cats = json.loads(io.open(CATS, encoding='utf-8').read())
    catmap = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    if not all(isinstance(v, dict) for v in list(catmap.values())[:3]):
        catmap = {str(c['id']): c for c in catmap.get('categories', [])}

    def subj_of(cid):
        c = catmap.get(str(cid)); n = 0
        while c and c.get('level', 0) > 0 and n < 6:
            c = catmap.get(str(c.get('parentId'))); n += 1
        return c.get('name') if c else None

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    mix = []
    for s in cb[0]['sections']:
        for q in s['questions']:
            subs = [subj_of(c) for c in (q.get('categoryIds') or [])]
            if not subs or not all(x == '线性代数' for x in subs):
                continue
            t = q.get('stem') or ''
            if [w for w in HI if w in t] and not [w for w in LA if w in t]:
                mix.append((s['title'], q))
    pool = [q for q in qs if not q.get('fromX')]

    for i, (sec, q) in enumerate(mix, 1):
        nq = norm(q.get('stem'))
        scored = sorted(((jac(nq, norm(p.get('stem'))), p) for p in pool), key=lambda x: -x[0])[:2]
        print('=' * 100)
        print('[%2d/20] no=%s(原xd-%s) 所属节[%s] src=%s' % (i, q['no'], q.get('xdNo'), sec, str(q.get('source'))[:30]))
        print('  ★ 新题全文: %s' % (q.get('stem') or '').replace('\n', ' '))
        for sc, p in scored:
            print('  · 相似 %.2f ← no=%s src=%s' % (sc, p['no'], str(p.get('source'))[:30]))
            print('      全文: %s' % (p.get('stem') or '').replace('\n', ' '))
    return 0


if __name__ == '__main__':
    sys.exit(main())
