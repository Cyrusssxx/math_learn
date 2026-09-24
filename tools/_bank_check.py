# -*- coding: utf-8 -*-
# 检查：exam 模式并入的 bankItems（大观园真题）里有无数一/数三题
import json, io, re
from collections import Counter

cats = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))
XL1 = {2, 3, 4, 5, 6, 7}
xdAll = set(XL1)
for nid, n in cats.items():
    try:
        if int(n.get('parentId') or 0) in XL1:
            xdAll.add(int(nid))
    except Exception:
        pass

bank = json.load(io.open('pwa/data/bank_questions.json', encoding='utf-8'))
b = bank.get('items') or []
xd = []
for it in b:
    cids = [int(c) for c in (it.get('categoryIds') or []) if str(c).isdigit()]
    if any(c in xdAll for c in cids):
        xd.append(it)
print('大观园真题中线代题:', len(xd))
c = Counter(str(it.get('source') or '') for it in xd)
print('source 分布（前 15）:')
for s, n in c.most_common(15):
    print('  %r: %d' % (s[:40], n))
# 数一/数三 命中数
n13 = [it for it in xd if re.search(r'数一|数三', str(it.get('source') or ''))]
print('含 数一/数三:', len(n13))
for it in n13[:8]:
    print('   ', it.get('source'), '|', (it.get('stem') or '')[:44])