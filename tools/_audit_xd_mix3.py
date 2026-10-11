#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""彻底扫描：找出 core_bank 里「题干是高数内容、却挂在线代知识点下」的全部题目。

判定（保守，避免误报）：
  强高数特征（出现任一即高度可疑）：\\lim \\int \\iint \\oint 渐近线 曲率 极值
      凹凸 拐点 定积分 不定积分 二重积分 反常积分 偏导 全微分 泰勒 洛必达
      中值定理 单调 连续 无穷小 等价无穷小 数列极限 微分方程 通解 特解
  线代特征（出现任一则排除，因为线代题也会提到"方程""解"）：矩阵 行列式 向量
      特征值 特征向量 秩 可逆 转置 伴随 初等变换 分块 二次型 线性无关 线性相关
      基础解系 齐次 非齐次 正交 合同 相似 迹 方阵 单位阵 对角
"""
import io, json, os, sys

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

    def path_of(cid):
        c = catmap.get(str(cid))
        out = []
        while c and len(out) < 5:
            out.append(c.get('display') or c.get('name'))
            c = catmap.get(str(c.get('parentId')))
        return ' / '.join(reversed(out))

    hits = []
    for s in cb[0]['sections']:
        for q in s['questions']:
            cids = q.get('categoryIds') or []
            subs = [subj_of(c) for c in cids]
            if not subs or not all(x == '线性代数' for x in subs):
                continue
            t = (q.get('stem') or '')
            hiHits = [w for w in HI if w in t]
            laHits = [w for w in LA if w in t]
            if hiHits and not laHits:
                hits.append((q['no'], q.get('xdNo'), s['title'], hiHits[:5],
                             [path_of(c) for c in cids],
                             str(q.get('source'))[:24], t.replace('\n', ' ')[:78]))
    print('=== 高数题干 + 零线代特征 + 挂线代知识点 的题 ===')
    print('数量 =', len(hits))
    for t in hits:
        print('  no=%-5s(原xd-%-6s) 节[%s] 命中:%s' % (t[0], t[1], t[2], ','.join(t[3])))
        print('      挂: %s' % ' | '.join(t[4]))
        print('      src=%s  %s' % (t[5], t[6]))
    print()
    # 汇总:按 section 统计
    import collections
    c = collections.Counter(t[2] for t in hits)
    print('按 section 分布:', dict(c))
    return 0


if __name__ == '__main__':
    sys.exit(main())
