# -*- coding: utf-8 -*-
"""审计 cat_deep.json 的 l2root 映射：找出误映射（映射到深层同名节点 / 名字不匹配 / 非 L1 直接子级）"""
import json, io

BASE = 'D:/ai code/math-note/pwa/data/'
DGY = ('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
       'daguanyuan-for-windows-main/assets/categories.json')
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes, l2root = deep['nodes'], deep['l2root']
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))
dcats = {str(x['id']): x for x in json.load(io.open(DGY, encoding='utf-8'))['items']}


def dpath(nid):
    out, cur, g = [], str(nid), 0
    while cur in dcats and g < 30:
        out.append(dcats[cur]['name'])
        p = dcats[cur].get('parentId')
        if p in (None, 0, '0'):
            break
        cur = str(p)
        g += 1
    return list(reversed(out))


def l2info(cid):
    v = cats.get(str(cid), {})
    p = cats.get(str(v.get('parentId')), {})
    return (p.get('display') or p.get('name') or '?'), (v.get('display') or v.get('name') or '?')


suspect = []
ok = 0
for l2, dg in l2root.items():
    l1name, l2name = l2info(l2)
    path = dpath(dg)
    dgname = nodes.get(str(dg), {}).get('n') or (dcats.get(str(dg), {}).get('name'))
    depth = len(path)                        # 期望 3：高等数学 / 章 / 知识点
    reasons = []
    if dgname != l2name:
        reasons.append('名字不符(%s≠%s)' % (dgname, l2name))
    if depth > 3:
        reasons.append('映射过深(深度%d: %s)' % (depth, ' / '.join(path)))
    if l1name not in path:
        reasons.append('不在同一章(%s 不在 %s)' % (l1name, ' / '.join(path)))
    if reasons:
        suspect.append((l2, l1name, l2name, dg, ' / '.join(path), reasons))
    else:
        ok += 1

print('l2root 共 %d 条：正常 %d，可疑 %d' % (len(l2root), ok, len(suspect)))
print()
for l2, l1, l2n, dg, path, reasons in suspect:
    print('L2 %s [%s / %s] → 大观园 %s' % (l2, l1, l2n, dg))
    print('   现指向: %s' % path)
    print('   问题  : %s' % '；'.join(reasons))
    # 建议：同一 L1 下的同名直接子级
    cands = [k for k, v in dcats.items()
             if v['name'] == l2n and str(v.get('parentId')) in dcats
             and dcats[str(v.get('parentId'))]['name'] == l1]
    print('   建议改为: %s' % (['%s(%s)' % (dcats[c]['name'], c) for c in cands] or '（无同章同名节点，需人工）'))
    print()
