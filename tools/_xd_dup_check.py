# -*- coding: utf-8 -*-
# 核实：xd_bank 中标注"数二真题"的 270 道 vs exam.json 真题的重叠情况
import json, io, re

xd = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))

xq = [q for s in xd[0]['sections'] for q in s['questions']]
s2 = [q for q in xq if re.search(r'数二', str(q.get('source') or ''))]
print('xd 里标注"数二真题"的题:', len(s2))

# exam 真题： (year, no) -> stem
ex = {}
for v in exam:
    y = str(v.get('year') or '')
    for sec in v.get('sections', []):
        for q in sec.get('questions', []):
            ex[(y, str(q['no']))] = q.get('stem') or ''


def norm(t):
    return re.sub(r'\s+', '', str(t or '')).replace('$', '')


# 按 source 提取年份 + 题号? xd 的 no 是 serial（非卷内题号），只能用 stem 比
ex_norm = set()
for k, st in ex.items():
    ns = norm(st)
    if len(ns) >= 12:
        ex_norm.add(ns)

hit = 0
hitnos = []
for q in s2:
    ns = norm(q.get('stem'))
    if len(ns) >= 12 and ns in ex_norm:
        hit += 1
        if len(hitnos) < 8:
            hitnos.append(str(q['no']))
print('其中 stem 与 exam.json 完全一致（重复）:', hit)
print('样本 serial:', hitnos)

# source 年份分布
from collections import Counter
yr = Counter()
for q in s2:
    m = re.search(r'(\d{4})', str(q.get('source') or ''))
    yr[m.group(1) if m else '?'] += 1
print('\nxd「数二真题」年份分布:')
for y, n in sorted(yr.items()):
    print('  %s: %d' % (y, n))