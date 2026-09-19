# -*- coding: utf-8 -*-
"""对比分类颗粒度：本库 exam_categories.json vs 大观园 categories.json"""
import json, io
from collections import Counter, defaultdict

OUR = 'D:/ai code/math-note/pwa/data/exam_categories.json'
DGY = ('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
       'daguanyuan-for-windows-main/assets/categories.json')

# ---- 本库 ----
our = json.load(io.open(OUR, encoding='utf-8'))
print('本库 exam_categories.json: %d 节点' % len(our))
lv = Counter(v.get('level') for v in our.values())
print('  层级分布:', dict(sorted(lv.items(), key=lambda x: (x[0] is None, x[0]))))
# 每层名字样例
bylv = defaultdict(list)
for k, v in our.items():
    bylv[v.get('level')].append(v.get('display') or v.get('name'))
for L in sorted(bylv, key=lambda x: (x is None, x)):
    n = bylv[L]
    print('  L%s (%d): %s' % (L, len(n), '、'.join(n[:12]) + ('…' if len(n) > 12 else '')))

# ---- 大观园 ----
d = json.load(io.open(DGY, encoding='utf-8'))
items = d['items']
cats = {str(x['id']): x for x in items}
print()
print('大观园 categories.json: %d 节点' % len(cats))
# 深度
def depth(cid):
    n, cur, seen = 0, str(cid), set()
    while cur in cats and cur not in seen:
        seen.add(cur)
        p = cats[cur].get('parentId')
        if p in (None, 0, '0'):
            return n
        n += 1
        cur = str(p)
    return n
dcount = Counter(depth(k) for k in cats)
print('  深度分布(根=0):', dict(sorted(dcount.items())))
# 各深度的节点样例
byд = defaultdict(list)
for k in cats:
    byд[depth(k)].append(cats[k])
for L in sorted(byд):
    n = byд[L]
    print('  d%d (%d): %s' % (L, len(n), '、'.join(x['name'] for x in n[:14]) + ('…' if len(n) > 14 else '')))
