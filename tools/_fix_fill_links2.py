#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ⑤：补第二批「实为真题同题却缺关联」的 core 题 linkedQid（12 道）。

来源：tools/_cmp_marks_sync2.py 的「A 类 top1 相似度复查」+ 人工逐对核对题干。
上一批（_fix_fill_links.py，157 道）用的是「从 core 无关联题出发找真题 top1」，
阈值 0.60；本批改为**从用户有标记的真题键出发反查 core 全库**，因此能捞出
「那道 core 题不是任何真题的 top1」的漏网之鱼（例如 2019-23 的 core 版把
（Ⅰ）（Ⅱ）写成 (I)(II)，被 norm 差异稀释到 0.691）。

12 对全部人工核对过题干，确认同题；2017数二真题-11 ↔ core-277 经核对为
**假阳性**（∫ln(1+x)/(1+x)^2 与 ∫ln(x+1)/x^2 被积函数不同），已排除。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')

# (真题键, core no) —— 全部人工核对为同题
PAIRS = [
    ('2017数二真题-20', 493),
    ('2016数二真题-18', 494),
    ('2015数二真题-18', 468),
    ('2024数二真题-4', 69),
    ('2008数二真题-5', 66),
    ('2019数二真题-23', 994),
    ('2019数二真题-12', 344),
    ('2007数二真题-4', 134),
    ('2022数二真题-3', 207),
    ('2009数二真题-7', 831),
    ('2018数二真题-8', 833),
    ('2024数二真题-18', 558),
    # 第二批（2026-10-11）：剥掉 core 版的【例3.47】/【14】/(1) 等排版前缀后浮现，
    # 全部人工核对题干为同题。
    ('2023数二真题-19', 325),   # core 版标「【例3.47】（2023，数二、三）」
    ('2006数二真题-18', 75),    # core 版带【14】前缀：0<x_1<π, x_{n+1}=sin x_n
    ('2014数二真题-23', 996),   # 证明 n 阶全 1 矩阵
    ('2016数二真题-4', 220),    # 导函数图形题（真题带图，core 注「图形见原书 P40」）
    ('2026数二真题-4', 359),    # 细杆对质点的万有引力
]


def norm(s):
    s = s or ''
    s = re.sub(r'（本题满分[^）]*分）', '', s)
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    return s


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    by_no = {q['no']: q for q in qs}

    # 占用表：某真题键已被多少道 core 题当作 linkedQid
    occ = collections.Counter(q['linkedQid'] for q in qs if q.get('linkedQid'))

    patched, skip = [], []
    for k, no in PAIRS:
        if k not in zp:
            skip.append((k, no, '真题里没有这个键'))
            continue
        if no not in by_no:
            skip.append((k, no, 'core 里没有这个 no'))
            continue
        q = by_no[no]
        if q.get('linkedQid'):
            skip.append((k, no, 'core 题已有 linkedQid=%s' % q['linkedQid']))
            continue
        if occ.get(k, 0) > 0:
            skip.append((k, no, '真题键已被 %d 道 core 题占用' % occ[k]))
            continue
        q['linkedQid'] = k
        q['linkScan'] = 'human-2'      # 人工核对留痕（区别于自动匹配的数值分）
        occ[k] += 1
        patched.append((no, k))

    print('计划 %d 对 → 实际补 %d 对' % (len(PAIRS), len(patched)))
    for no, k in patched:
        print('   core no=%-5s → %s' % (no, k))
    for k, no, why in skip:
        print('   ⚠️ 跳过 %-18s (core no=%s)：%s' % (k, no, why))

    # 自检：不得出现「题干不全同」的一对多
    g = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            g[q['linkedQid']].append(q)
    bad = {k: len(v) for k, v in g.items() if len(v) > 1 and len({norm(q.get('stem')) for q in v}) > 1}
    if bad:
        print('❌ 自检失败（一对多回潮）:', bad)
        return 1
    print('✅ 自检通过：无一对多回潮')

    # 自检：题数与 no 唯一性
    nos = [q['no'] for q in qs]
    assert len(nos) == len(set(nos)), 'no 重复'
    print('✅ 题数 =', len(qs))

    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
