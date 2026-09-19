# -*- coding: utf-8 -*-
"""cat_deep.json 结构升级：{ nodes, l2root }。
   nodes  = 大观园数二相关 826 节点 {id:{n,p}}
   l2root = 本库 L2 知识点 id → 大观园细分类根 id（57 精确命中 + 2 个模糊兜底）
"""
import json, io, difflib

BASE = 'D:/ai code/math-note/pwa/data/'
ROOT = 'D:/ai code/math-note/tools/'

nodes = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
# 兼容旧结构（纯 nodes）
if 'nodes' in nodes:
    nodes = nodes['nodes']
m = json.load(io.open(ROOT + '_l2_map.json', encoding='utf-8'))
our = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))

# 大观园节点名索引（仅数二相关）
byname = {}
for k, v in nodes.items():
    byname.setdefault(v['n'], []).append(k)

# 2 个精确未命中的知识点 → 模糊匹配到同章下最相近的节点
FUZZY = {
    '多项式以行列式形式给出': '行列式',
    '求可逆矩阵，使得': '二次型',
}
our_l2 = {k: v for k, v in our.items() if v.get('level') == 2}
l1name = {}
for k, v in our_l2.items():
    p = our.get(str(v.get('parentId')), {})
    l1name[k] = p.get('display') or p.get('name')

added = []
for cid, (qname, l1) in [(k, (v.get('display') or v.get('name'), l1name[k])) for k, v in our_l2.items()]:
    if cid in m or l1 in ('数二',):
        continue
    # 全库按名字相似度取最佳（这两个知识点在同章下无同名节点，模糊匹配到最相近的算法节点）
    best, bid = 0.0, None
    for k, v in nodes.items():
        s = difflib.SequenceMatcher(None, qname, v['n']).ratio()
        if s > best:
            best, bid = s, k
    if bid and best >= 0.6:
        m[cid] = bid
        added.append((qname, nodes[bid]['n'], round(best, 2)))

out = {'nodes': nodes, 'l2root': m}
json.dump(out, io.open(BASE + 'cat_deep.json', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'), sort_keys=True)

print('cat_deep.json: nodes=%d, l2root=%d' % (len(nodes), len(m)))
print('模糊补入 %d 个：%s' % (len(added), added))
# 覆盖率：本库知识点（排除年份类）
kn = [k for k, v in our_l2.items() if l1name[k] != '数二']
print('知识点覆盖: %d / %d' % (sum(1 for k in kn if k in m), len(kn)))
