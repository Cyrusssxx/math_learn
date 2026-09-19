# -*- coding: utf-8 -*-
"""列出「无法判定」的题（原始 deepCats 反推不出本库 L2），供逐题人工分析。
   core 与 exam 各输出一份清单（题号 / 现归属 / 原始标签路径 / 题干）。"""
import json, io
from collections import defaultdict

BASE = 'D:/ai code/math-note/pwa/data/'
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes, l2root = deep['nodes'], deep['l2root']
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))

kids = {}
for cid, v in nodes.items():
    if v['p']:
        kids.setdefault(v['p'], []).append(cid)


def subtree(root):
    out, st, seen = [], [str(root)], set()
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
        st += kids.get(x, [])
    return set(out)


SUB = {k: subtree(v) for k, v in l2root.items()}
node2l2 = defaultdict(list)
for l2, s in SUB.items():
    for n in s:
        node2l2[n].append(l2)


def l2name(cid):
    v = cats.get(str(cid), {})
    p = cats.get(str(v.get('parentId')), {})
    return '%s / %s' % (p.get('display') or p.get('name') or '?', v.get('display') or v.get('name') or '?')


# 大观园完整树（含数二之外），用于展示标签路径
raw = json.load(io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
                        'daguanyuan-for-windows-main/assets/categories.json', encoding='utf-8'))
dcats = {str(x['id']): x for x in raw['items']}


def dpath(nid):
    out, cur, g = [], str(nid), 0
    while cur in dcats and g < 30:
        out.append(dcats[cur]['name'])
        p = dcats[cur].get('parentId')
        if p in (None, 0, '0'):
            break
        cur = str(p)
        g += 1
    return ' / '.join(reversed(out))


def show(title, items):
    print('=' * 74)
    print(title)
    print('=' * 74)
    for i, (no, catname, dc, src, stem) in enumerate(items, 1):
        print('%d) 题%s [%s]  现归属: %s' % (i, no, src, catname))
        print('   标签: %s' % ([dpath(x) for x in dc] if dc else '（无标签）'))
        print('   题干: %s' % (stem or '')[:190].replace('\n', ' '))
        print()


# ---- core ----
orig = json.load(io.open('D:/ai code/math-note/_orig_core.json', encoding='utf-8'))
core_qs = [q for s in orig[0]['sections'] for q in s['questions']]
core_items = []
for q in core_qs:
    dc = [str(x) for x in (q.get('deepCats') or [])]
    if any(node2l2.get(x) for x in dc):
        continue
    core_items.append((q['no'], l2name(q.get('catId')), dc, q.get('source'), q.get('stem')))
show('【core_bank】无法判定 %d 题' % len(core_items), core_items)

# ---- exam ----
orig2 = json.load(io.open('D:/ai code/math-note/_orig_exam.json', encoding='utf-8'))
exam_items = []
for vol in orig2:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            dc = [str(x) for x in (q.get('deepCats') or [])]
            if any(node2l2.get(x) for x in dc):
                continue
            cids = q.get('categoryIds') or []
            exam_items.append(('%s-%s' % (vol.get('id'), q['no']),
                               ' / '.join(l2name(c) for c in cids), dc, '', q.get('stem')))
show('【exam】无法判定 %d 题' % len(exam_items), exam_items)
