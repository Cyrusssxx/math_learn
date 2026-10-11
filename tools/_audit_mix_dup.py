#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""问题①的重复性验证：20 道「混入线代的高数题」是否与 core 既有高数题重复。

判定：题干归一化后做 bigram Jaccard 相似度（项目既有去重方法，见分类页 normStem 思路）。
  ≥0.90 → 判定重复（可在 core 里看到两遍）
  0.60~0.90 → 高度相似，需人工复核（可能是同题改写）
  <0.60 → 视为不重复
"""
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
    """归一化：去 LaTeX 命令、空白、花括号，保留数字与字母（避免把不同题归一化到一起）"""
    s = s or ''
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)      # \lim \int \frac …
    s = re.sub(r'[{}$\s\\]+', '', s)        # 花括号/美元/空白/反斜杠
    s = re.sub(r'（\s*）|\(\s*\)|_{2,}', '', s)
    return s


def bigrams(s):
    return set(s[i:i + 2] for i in range(len(s) - 1)) if len(s) > 1 else {s}


def jac(a, b):
    A, B = bigrams(a), bigrams(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    cats = json.loads(io.open(CATS, encoding='utf-8').read())
    catmap = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    if not all(isinstance(v, dict) for v in list(catmap.values())[:3]):
        catmap = {str(c['id']): c for c in catmap.get('categories', [])}

    def subj_of(cid):
        c = catmap.get(str(cid))
        n = 0
        while c and c.get('level', 0) > 0 and n < 6:
            c = catmap.get(str(c.get('parentId')))
            n += 1
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
    # 比对池：全部非 fromX 题（core 原有 741）+ 其余 fromX 题（避免误判为"与线代题重复"）
    pool = [q for q in qs if not q.get('fromX')]
    print('混入题 = %d 道；比对池 = core 原有 %d 道' % (len(mix), len(pool)))

    dup, near, clean = [], [], []
    for sec, q in mix:
        nq = norm(q.get('stem'))
        best = (0.0, None)
        for p in pool:
            s = jac(nq, norm(p.get('stem')))
            if s > best[0]:
                best = (s, p)
        tag = 'dup' if best[0] >= 0.90 else ('near' if best[0] >= 0.60 else 'clean')
        rec = (sec, q, best[0], best[1])
        (dup if tag == 'dup' else near if tag == 'near' else clean).append(rec)

    def show(tag, rows, limit=20):
        print()
        print('--- %s：%d 道 ---' % (tag, len(rows)))
        for sec, q, sc, p in rows[:limit]:
            print('  no=%-5s(原xd-%-6s) 节[%-10s] 相似度=%.2f' % (q['no'], q.get('xdNo'), sec, sc))
            print('     新: %s' % (q.get('stem') or '').replace('\n', ' ')[:74])
            if p:
                print('     旧: no=%s  %s' % (p['no'], (p.get('stem') or '').replace('\n', ' ')[:64]))
                print('         src=%s' % str(p.get('source'))[:40])

    show('① 判定重复（≥0.90）', dup)
    show('② 高度相似需复核（0.60~0.90）', near)
    show('③ 无重复（<0.60）', clean)
    print()
    print('汇总：重复 %d / 需复核 %d / 无重复 %d' % (len(dup), len(near), len(clean)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
