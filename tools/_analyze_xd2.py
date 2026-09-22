# -*- coding: utf-8 -*-
# 大观园线代 959 题：source 构成（数一/数二/练习册）、向量空间节点精确查找
import json, io
from collections import Counter

cats = json.load(io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/categories.json', encoding='utf-8'))
items = cats['items']
byid = {str(it['id']): it for it in items}
xd_nodes = set()
def collect(nid):
    xd_nodes.add(nid)
    for it in items:
        if str(it.get('parentId')) == str(nid):
            collect(str(it['id']))
collect('1')

q = json.load(io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json', encoding='utf-8'))['items']
xd = [it for it in q if any(str(c) in xd_nodes for c in (it.get('categoryIds') or []))]
print('线代题:', len(xd))
# source 全量统计
src = Counter(str(it.get('source') or '(无)') for it in xd)
print('\nsource 分布:')
for s, n in src.most_common(20):
    print('  %s: %d' % (s[:40], n))
# 数一标记统计
s1 = sum(1 for it in xd if '数一' in str(it.get('source') or ''))
s2 = sum(1 for it in xd if '数二' in str(it.get('source') or ''))
print('\n含"数一"来源:', s1, '| 含"数二"来源:', s2)
# 向量空间：categories 中 name 含 空间/基/维
print('\n含"空间/基/维"的节点:')
for it in items:
    nm = str(it.get('name') or '')
    if any(k in nm for k in ('空间', '基与', '维数')) and str(it.get('parentId')) in xd_nodes:
        print('  ', it['id'], nm, it.get('totalCount'))
