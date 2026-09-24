# -*- coding: utf-8 -*-
# 核实：数二真题（exam.json + bankItems 大观园）中线代题的真实总数，逐卷列出
import json, io, re

exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
cats = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))
bank = json.load(io.open('pwa/data/bank_questions.json', encoding='utf-8'))

# 线代 L1/L2 节点
XL1 = {2, 3, 4, 5, 6, 7}
xdL2, xdAll = set(), set(XL1)
for nid, n in cats.items():
    try:
        pid = int(n.get('parentId') or 0)
    except Exception:
        continue
    if pid in XL1:
        xdL2.add(int(nid))
        xdAll.add(int(nid))

print('=== exam.json（27 套数二真题）线代题 ===')
tot = 0
per_year = {}
for v in exam:
    n = 0
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            cids = [int(c) for c in (q.get('categoryIds') or []) if str(c).isdigit()]
            if any(c in xdAll for c in cids):
                n += 1
    if n:
        per_year[v['id']] = n
        tot += n
print('总:', tot, '| 逐卷:', per_year)

print()
print('=== bank_questions.json（大观园数二真题）线代题 ===')
b = bank.get('items') or []
bn = 0
for it in b:
    cids = [int(c) for c in (it.get('categoryIds') or []) if str(c).isdigit()]
    if any(c in xdAll for c in cids):
        bn += 1
print('大观园数二真题线代:', bn)

print()
print('=== 合计（数二真题线代）:', tot + bn, '===')

# 对照：xd_bank 里各类
xd = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
xq = [q for s in xd[0]['sections'] for q in s['questions']]
print()
print('xd_bank（补充题库）总:', len(xq))
c = {}
for q in xq:
    src = str(q.get('source') or '')
    if re.search(r'数一|数三', src):
        c['数一/数三'] = c.get('数一/数三', 0) + 1
    elif '数学一二三' in src:
        c['共用'] = c.get('共用', 0) + 1
    elif re.search(r'900|李艳芳|张宇|李永乐|模拟|套', src):
        c['数二练习册'] = c.get('数二练习册', 0) + 1
    elif re.search(r'\d{4}', src):
        c['数二真题(带年份)'] = c.get('数二真题(带年份)', 0) + 1
    else:
        c['其他'] = c.get('其他', 0) + 1
print('构成:', c)