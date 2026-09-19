# -*- coding: utf-8 -*-
"""原地约束 deepCats：把每题的大观园细分类标签限制在「其知识点对应子树」内。
   - 落在子树内的保留（可多个）
   - 越界的丢弃；若一个都不剩 → 回落到该知识点的细分类根（l2root[catId]）
   作用于 pwa/data/core_bank.json 与 pwa/data/exam.json（保持原格式）。
"""
import json, io
from collections import Counter

BASE = 'D:/ai code/math-note/pwa/data/'
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes, l2root = deep['nodes'], deep['l2root']

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

# 节点深度（越深越具体），用于一题多标签时取最具体的那个
def depth_of(nid):
    d, cur, guard = 0, str(nid), 0
    while cur in nodes and nodes[cur]['p'] and guard < 30:
        cur = nodes[cur]['p']
        d += 1
        guard += 1
    return d


def constrain(q, cat_ids):
    """返回 (新 deepCats, 状态)。每题**只保留一个最具体**的细分类标签，
    保证「本级 + 各子分支」计数之和严格等于该知识点题数（避免多标签重复计数）。"""
    old = [str(x) for x in (q.get('deepCats') or [])]
    st = None
    cat = None
    for c in cat_ids:
        if str(c) in SUB:
            st, cat = SUB[str(c)], str(c)
            break
    if st is None:
        return old, '无子树'
    kept = [x for x in old if x in st]
    if kept:
        pick = max(kept, key=depth_of)          # 取最深（最具体）
        return [pick], '保留(单标签)' if len(kept) == 1 else '收敛为最具体'
    return [l2root[cat]], '回落根'


summary = {}
# ---------- core_bank ----------
P = BASE + 'core_bank.json'
d = json.load(io.open(P, encoding='utf-8'))
st1 = Counter()
for s in d[0]['sections']:
    for q in s['questions']:
        q['deepCats'], tag = constrain(q, [q.get('catId')])
        st1[tag] += 1
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
summary['core_bank'] = dict(st1)
print('core_bank:', dict(st1))

# ---------- exam ----------
P2 = BASE + 'exam.json'
e = json.load(io.open(P2, encoding='utf-8'))
st2 = Counter()
for vol in e:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            q['deepCats'], tag = constrain(q, q.get('categoryIds') or [])
            st2[tag] += 1
with io.open(P2, 'w', encoding='utf-8', newline='') as f:
    json.dump(e, f, ensure_ascii=False, separators=(',', ':'))
summary['exam'] = dict(st2)
print('exam:     ', dict(st2))

# ---------- 复检 ----------
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))
fn = next(k for k, v in cats.items() if v.get('level') == 2 and (v.get('display') or v.get('name')) == '函数'
          and cats[str(v.get('parentId'))].get('display') == '极限')
d2 = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
qs = [q for s in d2[0]['sections'] for q in s['questions']]
mine = [q for q in qs if str(q.get('catId')) == str(fn)]
st = SUB[str(fn)]
cov = sum(1 for q in mine if any(x in st for x in (q.get('deepCats') or [])))
print()
print('复检「函数」知识点：共 %d 题，约束后覆盖 %d 题（浮层可见）' % (len(mine), cov))
dist = Counter()
for q in mine:
    for x in q['deepCats']:
        dist[nodes[x]['n']] += 1
print('  细分类分布:', dict(dist))
