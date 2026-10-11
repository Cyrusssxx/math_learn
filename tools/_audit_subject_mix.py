#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全量检查：core_bank 里「题干的学科」与「所挂知识点的学科」是否一致。
用于排查「线代分类里混入高数题」。

判定方式：强特征词计数（不依赖分词）。
  高数强特征：\\int \\lim 积分 导数 极限 连续 微分 偏导 级数 二重积分 曲线 定积分 不定积分
  线代强特征：矩阵 行列式 向量 特征值 特征向量 秩 可逆 线性无关 线性相关 二次型 方程组
            相似 合同 转置 伴随 初等变换 分块
统计题干（去掉 LaTeX 环境名干扰）里两类词的命中数，取多者判为「疑似」；
只报「疑似与所属分类矛盾」的题，供人工复核。
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
CATS = os.path.join(ROOT, 'pwa/data/exam_categories.json')

LA_SEC = {'行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'}
HI_WORDS = ['\\int', '\\lim', '\\iint', '积分', '导数', '极限', '连续', '微分', '偏导',
            '级数', '二重积分', '曲线', '定积分', '不定积分', '泰勒', '洛必达', '中值定理',
            '单调', '凹凸', '渐近线', '曲率', '一阶线性', '通解', '特解']
LA_WORDS = ['矩阵', '行列式', '向量', '特征值', '特征向量', '秩', '可逆', '线性无关',
            '线性相关', '二次型', '方程组', '相似', '合同', '转置', '伴随', '初等变换',
            '分块', '迹', '基础解系', '齐次', '非齐次']


def subject_of(cid, catmap):
    c = catmap.get(str(cid))
    if not c:
        return None
    # 沿父链上溯到 level 0
    seen = 0
    while c and c.get('level', 0) > 0 and seen < 5:
        c = catmap.get(str(c.get('parentId')))
        seen += 1
    return c.get('name') if c else None


def score(text):
    t = text or ''
    hi = sum(t.count(w) for w in HI_WORDS)
    la = sum(t.count(w) for w in LA_WORDS)
    return hi, la


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    cats = json.loads(io.open(CATS, encoding='utf-8').read())
    catmap = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    if not all(isinstance(v, dict) for v in list(catmap.values())[:3]):
        catmap = {str(c['id']): c for c in catmap.get('categories', [])}

    bad = []
    for s in cb[0]['sections']:
        sec_la = s['title'] in LA_SEC
        for q in s['questions']:
            for cid in (q.get('categoryIds') or []):
                subj = subject_of(cid, catmap)
                if subj not in ('高等数学', '线性代数'):
                    continue
                c_la = (subj == '线性代数')
                if c_la == sec_la:
                    continue          # section 与知识点学科一致 → 跳过
                bad.append((s['title'], subj, q['no'], q.get('fromX'), cid,
                            str(q.get('source'))[:26], q.get('stem') or ''))

    print('=== A. section 学科 ≠ 知识点学科 的挂载 ===')
    print('数量 =', len(bad))
    for t in bad[:12]:
        print('  [%s/%s] no=%s fromX=%s cid=%s src=%s' % (t[0], t[1], t[2], t[3], t[4], t[5]))

    # B. 逐题按题干判定，找出「挂线代知识点但题干像高数」的题
    print()
    print('=== B. 挂线代知识点、但题干更像高数 的题 ===')
    hits = []
    for s in cb[0]['sections']:
        for q in s['questions']:
            cids = q.get('categoryIds') or []
            subs = [subject_of(c, catmap) for c in cids]
            if not subs or not all(x == '线性代数' for x in subs):
                continue
            hi, la = score(q.get('stem'))
            if hi > la and hi >= 2:
                hits.append((q['no'], q.get('fromX'), s['title'], hi, la,
                             str(q.get('source'))[:26], (q.get('stem') or '').replace('\n', ' ')[:90]))
    print('数量 =', len(hits))
    for t in hits[:15]:
        print('  no=%s fromX=%s sec=%s 高数词%d/线代词%d src=%s' % (t[0], t[1], t[2], t[3], t[4], t[5]))
        print('       %s' % t[6])

    # C. 反向：挂高数知识点但题干像线代
    print()
    print('=== C. 挂高数知识点、但题干更像线代 的题 ===')
    hits2 = []
    for s in cb[0]['sections']:
        for q in s['questions']:
            subs = [subject_of(c, catmap) for c in (q.get('categoryIds') or [])]
            if not subs or not all(x == '高等数学' for x in subs):
                continue
            hi, la = score(q.get('stem'))
            if la > hi and la >= 2:
                hits2.append((q['no'], q.get('fromX'), s['title'], hi, la,
                              str(q.get('source'))[:26], (q.get('stem') or '').replace('\n', ' ')[:90]))
    print('数量 =', len(hits2))
    for t in hits2[:15]:
        print('  no=%s fromX=%s sec=%s 高数词%d/线代词%d src=%s' % (t[0], t[1], t[2], t[3], t[4], t[5]))
        print('       %s' % t[6])
    return 0


if __name__ == '__main__':
    sys.exit(main())
