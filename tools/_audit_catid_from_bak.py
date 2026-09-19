# -*- coding: utf-8 -*-
"""用「备份中的原始 deepCats」反查 catId 错配：判定每题正确的本库知识点，统计规模与样例。"""
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
node2l2 = defaultdict(list)
for l2, st in SUB.items():
    for n in st:
        node2l2[n].append(l2)

# 大观园节点 → 其到根的路径（用于展示）
def dpath(nid):
    out, cur, g = [], str(nid), 0
    while cur in nodes and g < 30:
        out.append(nodes[cur]['n'])
        cur = nodes[cur]['p']
        g += 1
    return ' / '.join(reversed(out))

def l2name(cid):
    v = cats.get(str(cid), {})
    p = cats.get(str(v.get('parentId')), {})
    return '%s / %s' % (p.get('display') or p.get('name') or '?', v.get('display') or v.get('name') or '?')

bak = json.load(io.open('D:/ai code/math-note/_bak_core.json', encoding='utf-8'))
qs = [q for s in bak[0]['sections'] for q in s['questions']]

fix, same, unknown = [], 0, 0
for q in qs:
    cat = str(q.get('catId'))
    dc = [str(x) for x in (q.get('deepCats') or [])]
    if not dc:
        unknown += 1
        continue
    cand = Counter()
    for x in dc:
        for l2 in node2l2.get(x, []):
            cand[l2] += 1
    if not cand:
        unknown += 1
        continue
    best, _ = cand.most_common(1)[0]
    if best == cat:
        same += 1
    else:
        fix.append((str(q['no']), cat, best, dc[:2], q.get('source'), q.get('stem') or ''))

print('=== 反查结果（core_bank 606 题）===')
print('  知识点一致      : %d' % same)
print('  知识点错（应改）: %d' % len(fix))
print('  无法判定        : %d' % unknown)
print()
print('=== 迁移去向 Top 15（现 → 应改为）===')
c = Counter('%s → %s' % (l2name(f[1]), l2name(f[2])) for f in fix)
for k, v in c.most_common(15):
    print('  %-46s %d 题' % (k, v))
print()
print('=== 抽样 12 条 ===')
for no, cat, best, dc, src, stem in fix[:12]:
    print('  题%-4s [%s] %s → %s' % (no, src, l2name(cat), l2name(best)))
    print('        标签 %s: %s' % (dc, dpath(dc[0])))
print()
print('=== 专项：题602 ===')
for no, cat, best, dc, src, stem in fix:
    if no == '602':
        print('  现 %s → 应 %s' % (l2name(cat), l2name(best)))
        print('  大观园标签路径:', dpath(dc[0]))
        print('  题干:', stem[:80])
