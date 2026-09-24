# -*- coding: utf-8 -*-
# 查大观园原始数据：线代节点的 totalCount vs 实际挂题数、按 source 分类（对齐截图 327）
import json, io, re, os
from collections import Counter

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))

# categories.json 结构
items = cats.get('items') if isinstance(cats, dict) else cats
print('categories 顶层键:', list(cats.keys()) if isinstance(cats, dict) else 'list')
print('节点数:', len(items) if isinstance(items, (list, dict)) else '?')

# 打印所有含「线」「行列式」「矩阵」「向量」「特征」「二次型」的节点
names = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型', '线性代数']
it = items.values() if isinstance(items, dict) else items
found = []
for n in it:
    nm = str(n.get('name') or n.get('title') or '')
    if nm in names:
        found.append((n.get('id'), nm, n.get('totalCount'), n.get('parentId')))
print()
print('线代相关节点:')
for f in sorted(found, key=lambda x: str(x[0])):
    print('  id=%s name=%s totalCount=%s parentId=%s' % f)

# 统计 questions.json 里挂这些节点（含后代）的题数
xl = [f for f in found if f[1] != '线性代数']
xl_ids = set(str(f[0]) for f in xl)
def in_xl(q):
    return any(str(c) in xl_ids for c in (q.get('categoryIds') or []))

xq = [q for q in qs if in_xl(q)]
print()
print('大观园挂线代 L2 节点的题数:', len(xq))
print('按 name 分别（一个题可能多节点）:')
for fid, nm, tc, pid in sorted(xl, key=lambda x: str(x[0])):
    c = sum(1 for q in xq if str(fid) in [str(x) for x in (q.get('categoryIds') or [])])
    print('  %-14s 实际挂题=%3d  totalCount=%s' % (nm, c, tc))

# source 分类
def kind(src):
    s = str(src or '')
    if '数学一二三' in s:
        return 'B_共用'
    if re.search(r'数一|数三', s):
        return 'C_数一数三'
    if re.search(r'数二', s):
        if re.search(r'900|李艳芳|张宇|李永乐|模拟|套', s):
            return 'A2_数二练习册'
        return 'A1_数二真题'
    if re.search(r'19\d\d|20\d\d', s):
        return 'D_其他年份真题'
    return 'E_无标注'

c = Counter(kind(q.get('source')) for q in xq)
print()
print('线代题 source 构成:')
for k in sorted(c):
    print('  %-14s %d' % (k, c[k]))