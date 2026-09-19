# -*- coding: utf-8 -*-
"""反查：题目的「知识点 catId」与「细分类 deepCats」不同树时，谁对？
   用 deepCats 反推正确知识点（大观园子树归属），统计需要修正 catId 的规模与样例。"""
import json, io
from collections import Counter, defaultdict

BASE = 'D:/ai code/math-note/pwa/data/'
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
    return out


SUB = {k: set(subtree(v)) for k, v in l2root.items()}
# 大观园节点 → 它属于哪些本库 L2（正常应唯一）
node2l2 = defaultdict(list)
for l2, st in SUB.items():
    for n in st:
        node2l2[n].append(l2)


def l2name(cid):
    v = cats.get(str(cid), {})
    p = cats.get(str(v.get('parentId')), {})
    return '%s / %s' % (p.get('display') or p.get('name') or '?', v.get('display') or v.get('name') or '?')


core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
qs = [q for s in core[0]['sections'] for q in s['questions']]

print('=== 逐题判定：catId 与大观园标签是否同树 ===')
need_fix = []
for q in qs:
    cat = str(q.get('catId'))
    dc = [str(x) for x in (q.get('deepCats') or [])]
    st = SUB.get(cat)
    if st is None or not dc:
        continue
    if any(x in st for x in dc):        # 同树 ✓
        continue
    # 不同树 → 用 deepCats 反推正确 L2
    cand = Counter()
    for x in dc:
        for l2 in node2l2.get(x, []):
            cand[l2] += 1
    if not cand:
        continue
    best, _ = cand.most_common(1)[0]
    need_fix.append((q['no'], cat, best, dc[:2], q.get('source')))

print('catId 与细分类不同树、且能反推出正确知识点的题: %d / %d' % (len(need_fix), len(qs)))
print()
print('=== 抽样（题号 | 现 catId → 应改为 | 标签 | 题源）===')
for no, cat, best, dc, src in need_fix[:12]:
    print('  题%-4s %-22s → %-22s %s | %s' % (no, l2name(cat), l2name(best), dc, src))

print()
print('=== 迁移目标分布（Top 12）===')
c = Counter(l2name(b) for _, _, b, _, _ in need_fix)
for k, v in c.most_common(12):
    print('  %-26s %d 题' % (k, v))

# 专项：题 602
print()
print('=== 专项核查 题602 ===')
for no, cat, best, dc, src in need_fix:
    if str(no) == '602':
        print('  现 catId=%s (%s)' % (cat, l2name(cat)))
        print('  deepCats=%s → 节点名=%s' % (dc, [nodes[x]['n'] for x in dc]))
        print('  应改为 %s (%s)' % (best, l2name(best)))
        print('  题源:', src)
