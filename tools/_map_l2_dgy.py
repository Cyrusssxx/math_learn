# -*- coding: utf-8 -*-
"""建立「本库 L2 知识点 ↔ 大观园节点」映射：按 name 在 d2/d3 层匹配 + 父链校验，报告命中率"""
import json, io
from collections import Counter

OUR = 'D:/ai code/math-note/pwa/data/exam_categories.json'
DGY = ('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
       'daguanyuan-for-windows-main/assets/categories.json')

our = json.load(io.open(OUR, encoding='utf-8'))
cats = {str(x['id']): x for x in json.load(io.open(DGY, encoding='utf-8'))['items']}
kids = {}
for k, v in cats.items():
    kids.setdefault(str(v.get('parentId')), []).append(k)


def path_of(cid):
    parts, cur, seen = [], str(cid), set()
    while cur in cats and cur not in seen:
        seen.add(cur)
        parts.append(cats[cur]['name'])
        p = cats[cur].get('parentId')
        if p in (None, 0, '0'):
            break
        cur = str(p)
    return list(reversed(parts))


# 本库 L1/L2
our_l1 = {k: v for k, v in our.items() if v.get('level') == 1}
our_l2 = {k: v for k, v in our.items() if v.get('level') == 2}
print('本库 L1=%d  L2=%d' % (len(our_l1), len(our_l2)))

# 大观园所有节点按 name 建索引
by_name = {}
for k, v in cats.items():
    by_name.setdefault(v['name'], []).append(k)

# 数二子树（高数 223 + 线代 1）
def subtree(root):
    out, stack = [], [str(root)]
    while stack:
        x = stack.pop()
        out.append(x)
        stack += kids.get(x, [])
    return set(out)


SHU2 = subtree(223) | subtree(1)

matched, miss = {}, []
for cid, v in our_l2.items():
    name = (v.get('display') or v.get('name') or '').strip()
    pname = cats.get(str(v.get('parentId')), {}).get('name') if str(v.get('parentId')) in cats else None
    # 本库父节点（L1）名
    our_parent = our.get(str(v.get('parentId')), {})
    l1name = our_parent.get('display') or our_parent.get('name')
    cands = [c for c in by_name.get(name, []) if c in SHU2]
    # 优先父链里含本库 L1 名的
    best = None
    for c in cands:
        p = path_of(c)
        if l1name and l1name in p:
            best = c
            break
    if best is None and cands:
        best = cands[0]
    if best:
        matched[cid] = best
    else:
        miss.append((name, l1name))

print('L2 命中大观园节点: %d / %d' % (len(matched), len(our_l2)))
print()
if miss:
    print('未命中 %d 个（需人工映射）:' % len(miss))
    for n, l1 in miss:
        print('   [%s] %s' % (l1, n))
print()
# 命中样例
print('命中样例（本库 L2 → 大观园节点）：')
for i, (cid, dg) in enumerate(list(matched.items())[:10]):
    print('   %s  →  %s (id=%s)  path=%s' % (our[cid]['display'], cats[dg]['name'], dg, ' / '.join(path_of(dg))))

json.dump(matched, io.open('D:/ai code/math-note/tools/_l2_map.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print()
print('已写 tools/_l2_map.json')
