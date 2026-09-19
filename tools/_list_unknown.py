# -*- coding: utf-8 -*-
"""列出「无法判定」的题（deepCats 反推不出 L2）：题号 / 现归属 / 标签 / 题干摘要"""
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


def dpath(nid):
    out, cur, g = [], str(nid), 0
    while cur in nodes and g < 30:
        out.append(nodes[cur]['n'])
        cur = nodes[cur]['p']
        g += 1
    return ' / '.join(reversed(out))


core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
qs = [q for s in core[0]['sections'] for q in s['questions']]
print('=== core_bank 无法判定 ===')
n = 0
for q in qs:
    dc = [str(x) for x in (q.get('deepCats') or [])]
    cand = set()
    for x in dc:
        cand |= set(node2l2.get(x, []))
    if cand:
        continue
    n += 1
    print('%d) 题%s [%s] 现:%s' % (n, q['no'], q.get('source'), l2name(q['catId'])))
    print('   标签: %s' % ([dpath(x) for x in dc] if dc else '（无）'))
    print('   题干: %s' % (q.get('stem') or '')[:170].replace('\n', ' '))
    print()

exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
print('=== exam 无法判定 ===')
n = 0
for vol in exam:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            dc = [str(x) for x in (q.get('deepCats') or [])]
            cand = set()
            for x in dc:
                cand |= set(node2l2.get(x, []))
            if cand:
                continue
            n += 1
            print('%d) %s 第%s题 现:%s' % (n, vol.get('id'), q['no'], [l2name(c) for c in (q.get('categoryIds') or [])]))
            print('   标签: %s' % ([dpath(x) for x in dc] if dc else '（无）'))
            print('   题干: %s' % (q.get('stem') or '')[:170].replace('\n', ' '))
            print()
