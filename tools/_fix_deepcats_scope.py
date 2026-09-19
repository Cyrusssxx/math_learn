# -*- coding: utf-8 -*-
"""修复 deepCats 越界：把每题的大观园细分类标签约束到「其知识点对应子树」内。
   - 保留落在子树内的标签（可能多个）
   - 越界的全部丢弃；若一个都不剩 → 回落到该知识点的细分类根（l2root[catId]）
   产出：tools/_deepcats_core.json / tools/_deepcats_exam.json 的修正版
"""
import json, io
from collections import Counter

BASE = 'D:/ai code/math-note/pwa/data/'
TOOLS = 'D:/ai code/math-note/tools/'
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes, l2root = deep['nodes'], deep['l2root']
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))

kids = {}
for cid, v in nodes.items():
    if v['p']:
        kids.setdefault(v['p'], []).append(cid)


def subtree(root):
    out, stack, seen = [], [str(root)], set()
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
        stack += kids.get(x, [])
    return set(out)


SUB = {k: subtree(v) for k, v in l2root.items()}

# ---------- core_bank ----------
core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
qs = [q for s in core[0]['sections'] for q in s['questions']]
core_deep = json.load(io.open(TOOLS + '_deepcats_core.json', encoding='utf-8'))
stat = Counter()
new_core = {}
for q in qs:
    qid = q['id']
    cat = str(q.get('catId'))
    old = [str(x) for x in (core_deep.get(qid) or [])]
    st = SUB.get(cat)
    if st is None:
        new_core[qid] = old
        stat['无子树'] += 1
        continue
    kept = [x for x in old if x in st]
    if kept:
        new_core[qid] = kept
        stat['保留子树内'] += 1
    else:
        new_core[qid] = [l2root[cat]]
        stat['越界→回落根'] += 1
json.dump(new_core, io.open(TOOLS + '_deepcats_core.json', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'), sort_keys=True)
print('core_bank: %s' % dict(stat))

# ---------- exam ----------
exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
exam_deep = json.load(io.open(TOOLS + '_deepcats_exam.json', encoding='utf-8'))
stat2 = Counter()
new_exam = {}
for vol in exam:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            key = '%s-%s' % (vol.get('id'), q.get('no'))
            old = [str(x) for x in (exam_deep.get(key) or [])]
            cids = [str(x) for x in (q.get('categoryIds') or [])]
            st = None
            for c in cids:
                if c in SUB:
                    st = SUB[c]
                    cat = c
                    break
            if st is None:
                new_exam[key] = old
                stat2['无子树'] += 1
                continue
            kept = [x for x in old if x in st]
            if kept:
                new_exam[key] = kept
                stat2['保留子树内'] += 1
            else:
                new_exam[key] = [l2root[cat]]
                stat2['越界→回落根'] += 1
json.dump(new_exam, io.open(TOOLS + '_deepcats_exam.json', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'), sort_keys=True)
print('exam:      %s' % dict(stat2))

# ---------- 效果预估：函数知识点覆盖 ----------
fn = next((k for k, v in cats.items() if v.get('level') == 2 and (v.get('display') or v.get('name')) == '函数'
           and cats[str(v.get('parentId'))].get('display') == '极限'), None)
print()
print('「函数」知识点 id=%s，共 %d 题' % (fn, sum(1 for q in qs if str(q.get('catId')) == str(fn))))
st = SUB[str(fn)]
cov = sum(1 for q in qs if str(q.get('catId')) == str(fn) and any(x in st for x in new_core[q['id']]))
print('  修复后覆盖（能在浮层被找到）: %d' % cov)
dist = Counter()
for q in qs:
    if str(q.get('catId')) == str(fn):
        for x in new_core[q['id']]:
            dist[nodes[x]['n']] += 1
print('  细分类分布:', dict(dist))
