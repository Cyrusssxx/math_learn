# -*- coding: utf-8 -*-
# 复现大观园「880 专项·数二」页的线代分类数（对齐截图 30/78/45/75/59/40）
import json, io, re
from collections import Counter

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))['items']
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))['items']

node = {int(n['id']): n for n in cats}

def anc(nid):
    out, cur, g = [], nid, 0
    while cur is not None and g < 20:
        out.append(cur)
        p = node.get(cur, {}).get('parentId')
        cur = int(p) if p is not None else None
        g += 1
    return out

def desc(root):
    return {nid for nid in node if root in anc(nid)}

XL1 = 1
XL2 = {int(n['id']): n['name'] for n in cats if int(n.get('parentId') or 0) == XL1}
desc_xl2 = {cid: desc(cid) for cid in XL2}

def match_math_two(src):
    s = str(src or '')
    if '数二' in s:
        return True
    return ('数一' not in s) and ('数三' not in s)

# 880 专项：source 含 '880'
q880 = [q for q in qs if '880' in str(q.get('source') or '')]
print('source 含 880 的题:', len(q880))
q880_2 = [q for q in q880 if match_math_two(q.get('source'))]
print('其中数二口径:', len(q880_2))

# 剔除数二不考章节（1064 级数 / 601 概率 / 8 线性代数-数学一专项）
excluded = set()
for r in (1064, 601, 8):
    excluded |= desc(r)
print('剔除章节节点数:', len(excluded))

def in_xl(q):
    return any(int(c) in desc_xl2_sum for c in (q.get('categoryIds') or []) if str(c).isdigit())
desc_xl2_sum = set()
for cid in XL2:
    if cid == 8:
        continue
    desc_xl2_sum |= desc_xl2[cid]

q880_2x = [q for q in q880_2 if not any(int(c) in excluded for c in (q.get('categoryIds') or []) if str(c).isdigit())]
print('剔除不考章节后:', len(q880_2x))

xl_880 = [q for q in q880_2x if in_xl(q)]
c = Counter()
for q in xl_880:
    for cid in XL2:
        if cid == 8:
            continue
        if any(int(x) in desc_xl2[cid] for x in (q.get('categoryIds') or []) if str(x).isdigit()):
            c[cid] += 1
print()
print('880·数二 线代分类:')
print('  总=%d' % len(xl_880))
for cid in sorted(XL2):
    if cid == 8:
        continue
    print('  %-12s %d' % (XL2[cid], c.get(cid, 0)))
print()
print('截图目标:      总=327 | 行列式=30 矩阵=78 向量=45 线方=75 特征值=59 二次型=40')