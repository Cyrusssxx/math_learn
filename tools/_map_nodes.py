# -*- coding: utf-8 -*-
# 建立「大观园线代节点 → 我们 exam_categories 节点」映射表（供导入用）
import json, io, re

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
dy_cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))['items']
dy_node = {int(n['id']): n for n in dy_cats}

our = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))
our_node = {int(k): v for k, v in our.items()}

# 我们的线代节点（L1=1 及其后代）
def our_anc(nid):
    out, cur, g = [], nid, 0
    while cur is not None and g < 10:
        out.append(cur)
        p = our_node.get(cur, {}).get('parentId')
        cur = int(p) if p is not None and str(p).isdigit() else None
        g += 1
    return out

our_xl = {nid: our_node[nid] for nid in our_node if 1 in our_anc(nid)}
print('我们线代节点数:', len(our_xl))
print('我们线代节点清单（id/name/parent）:')
for nid in sorted(our_xl):
    n = our_xl[nid]
    print('  %-5s %-26s parent=%s' % (nid, str(n.get('name'))[:26], n.get('parentId')))

print()
print('大观园线代节点（深层，含 path）:')
dy_xl = {int(n['id']): n for n in dy_cats if int(n.get('id') or 0) == 1 or (n.get('parentId') is not None and 1 in [int(x) for x in [n.get('parentId')]] )}
# 只取 L2 层（parent=1）及其子
def dy_anc(nid):
    out, cur, g = [], nid, 0
    while cur is not None and g < 10:
        out.append(cur)
        p = dy_node.get(cur, {}).get('parentId')
        cur = int(p) if p is not None else None
        g += 1
    return out
dy_xl = {nid: dy_node[nid] for nid in dy_node if 1 in dy_anc(nid)}
print('大观园线代节点数:', len(dy_xl))
for nid in sorted(dy_xl)[:60]:
    n = dy_xl[nid]
    print('  %-5s %-24s parent=%s | %s' % (nid, str(n.get('name'))[:24], n.get('parentId'), n.get('path')))