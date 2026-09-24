# -*- coding: utf-8 -*-
# 大观园线代题全量分析：节点分布 / source 类型 / 与 we库覆盖对比（对齐截图 327）
import json, io, re, os
from collections import Counter

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))['items']
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))['items']

XL2 = {'2': '行列式', '3': '矩阵', '4': '向量', '5': '线性方程组', '6': '特征值与特征向量', '7': '二次型'}
XL2_IDS = set(XL2.keys())

def xl_nodes(q):
    return [str(c) for c in (q.get('categoryIds') or []) if str(c) in XL2_IDS]

xq = [q for q in qs if xl_nodes(q)]
print('大观园挂线代 L2 的题:', len(xq), '/ 总', len(qs))

# 各节点计数（一题可多节点）
print()
print('各章挂题数（大观园原始，全科目）:')
for cid, nm in XL2.items():
    c = sum(1 for q in xq if cid in [str(x) for x in (q.get('categoryIds') or [])])
    print('  %-12s %d' % (nm, c))

# source 分类
def kind(src):
    s = str(src or '')
    if '数学一二三' in s:
        return 'B_数一二三共用'
    if re.search(r'数一|数三', s):
        return 'C_数一或数三'
    if re.search(r'数二', s):
        if re.search(r'900|李艳芳|张宇|李永乐|模拟|套|题源|强化|基础', s):
            return 'A2_数二练习册/模拟'
        return 'A1_数二真题'
    if re.search(r'19\d\d|20\d\d', s):
        return 'D_其他真题'
    return 'E_无标注(自编/其他)'

c = Counter(kind(q.get('source')) for q in xq)
print()
print('线代题 source 构成（大观园全量）:')
tot = 0
for k in sorted(c):
    print('  %-16s %d' % (k, c[k]))
    tot += c[k]

# 数二范围（去掉数一/数三独有）
er = [q for q in xq if kind(q.get('source')) != 'C_数一或数三']
print()
print('去掉「数一/数三」后（≈数二范围）:', len(er))
c2 = Counter(kind(q.get('source')) for q in er)
for k in sorted(c2):
    print('  %-16s %d' % (k, c2[k]))

# 我们库的覆盖
OUR_XD = 'pwa/data/xd_bank.json'
our = json.load(io.open(OUR_XD, encoding='utf-8'))
oq = [q for s in our[0]['sections'] for q in s['questions']]
print()
print('我们 xd_bank:', len(oq))
exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
eq = [q for v in exam for s in v.get('sections', []) for q in s.get('questions')
      if any(str(x) in XL2_IDS for x in (q.get('categoryIds') or []))]
print('我们 exam.json 线代真题:', len(eq))

# 覆盖：用 stem 规范化比对大观园数二范围线代题 vs 我们（xd_bank + exam.json）
def norm(t):
    s = re.sub(r'\s+', '', str(t or '')).replace('$', '')
    s = re.sub(r'\\dfrac|\\tfrac', r'\\frac', s)
    return s

our_set = set()
for q in oq + eq:
    n = norm(q.get('stem'))
    if len(n) >= 12:
        our_set.add(n)
our_pref = set(list(our_set)[i][:40] for i in range(len(our_set)))

missing = []
for q in er:
    n = norm(q.get('stem'))
    if len(n) < 12:
        continue
    if n in our_set or n[:40] in our_pref:
        continue
    missing.append(q)
print()
print('大观园数二范围线代 %d 题中，我们库缺失（stem 未匹配）: %d' % (len(er), len(missing)))
cm = Counter(kind(q.get('source')) for q in missing)
print('缺失构成:')
for k in sorted(cm):
    print('  %-16s %d' % (k, cm[k]))
print()
print('缺失样本 10:')
for q in missing[:10]:
    print('  serial=%s src=%-28s stem=%s' % (q.get('serial'), str(q.get('source'))[:28], norm(q.get('stem'))[:60]))