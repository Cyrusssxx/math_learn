# -*- coding: utf-8 -*-
"""量化：题目的 deepCats 有多少落在「其 catId 对应的大观园子树」之外（导致浮层覆盖不全）"""
import json, io
from collections import Counter

BASE = 'D:/ai code/math-note/pwa/data/'
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes, l2root = deep['nodes'], deep['l2root']

kids = {}
for cid, v in nodes.items():
    if v['p']:
        kids.setdefault(v['p'], []).append(cid)


def subtree(root):
    out, stack = [], [str(root)]
    while stack:
        x = stack.pop()
        if x in out:
            continue
        out.append(x)
        stack += kids.get(x, [])
    return set(out)


SUB = {k: subtree(v) for k, v in l2root.items()}      # 本库 L2 id → 大观园子树集合

for name, path, getq in (
    ('core_bank', BASE + 'core_bank.json', lambda d: [q for s in d[0]['sections'] for q in s['questions']]),
    ('exam', BASE + 'exam.json', lambda d: [q for v in d for s in v.get('sections', []) for q in s.get('questions', [])]),
):
    d = json.load(io.open(path, encoding='utf-8'))
    qs = getq(d)
    inside = outside = noroot = 0
    miss_examples = []
    l2_cnt = Counter()
    for q in qs:
        dc = [str(x) for x in (q.get('deepCats') or [])]
        cids = [str(x) for x in (q.get('categoryIds') or [])] or ([str(q['catId'])] if q.get('catId') else [])
        st = None
        for c in cids:
            if c in SUB:
                st = SUB[c]
                break
        if st is None:
            noroot += 1
            continue
        if any(x in st for x in dc):
            inside += 1
        else:
            outside += 1
            if len(miss_examples) < 5:
                miss_examples.append((q.get('no'), cids[0], dc[:3]))
        l2_cnt[cids[0]] += 1
    print('=' * 66)
    print('%s：共 %d 题' % (name, len(qs)))
    print('  deepCats 落在本知识点子树内 : %d' % inside)
    print('  deepCats 落在子树外（浮层看不到）: %d' % outside)
    print('  该知识点无细分类映射（无子树） : %d' % noroot)
    print('  样例（题号, 本库L2, deepCats前三）:', miss_examples[:3])
    print('  知识点覆盖数 %d' % len(l2_cnt))
