# -*- coding: utf-8 -*-
# 分析大观园线代题：收集线代子树节点（parent 链到 线性代数=1）、向量空间节点、实际题量
import json, io

cats = json.load(io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/categories.json', encoding='utf-8'))
items = cats['items']
byid = {str(it['id']): it for it in items}

# 线性代数=1 的子树（含自己）
xd_nodes = set()
def collect(nid):
    xd_nodes.add(nid)
    for it in items:
        if str(it.get('parentId')) == str(nid):
            collect(str(it['id']))
collect('1')
print('线代子树节点数:', len(xd_nodes))

# 向量空间相关节点（name 含 向量空间/基/维数/坐标）
vs_nodes = set()
for it in items:
    nm = str(it.get('name') or '')
    if any(k in nm for k in ('向量空间', '基与维数', '坐标', '过渡矩阵', '维数')):
        vs_nodes.add(str(it['id']))
        print('  向量空间节点:', it['id'], nm, 'totalCount=', it.get('totalCount'))
print('向量空间节点数:', len(vs_nodes))

# 统计 items 中线代题量（categoryIds 含线代节点）
q = json.load(io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json', encoding='utf-8'))
items_q = q['items']
xd_cnt = vs_cnt = 0
xd_only = []
for it in items_q:
    cids = [str(c) for c in (it.get('categoryIds') or [])]
    if any(c in xd_nodes for c in cids):
        xd_cnt += 1
        if any(c in vs_nodes for c in cids):
            vs_cnt += 1
        else:
            xd_only.append(it)
print()
print('线代题总数:', xd_cnt, '| 其中向量空间:', vs_cnt, '| 排除后:', len(xd_only))
print('(约数二线代补充量)', len(xd_only))
# source 字段分布（真题/练习）
from collections import Counter
src = Counter()
for it in xd_only[:200]:
    s = str(it.get('source') or '')
    src[s[:6]] += 1
print('source 前 5 类:', src.most_common(5))
