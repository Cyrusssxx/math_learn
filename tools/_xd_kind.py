# -*- coding: utf-8 -*-
# 统计 xd_bank 的 source 类型分布（决定剔除范围）
import json, io, re
from collections import Counter

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]
print('xd_bank 总题:', len(qs))


def kind(src):
    s = str(src or '')
    if re.search(r'数二', s):
        return 'A_数二真题'
    if '数学一二三' in s:
        return 'B_数学一二三共用'
    if re.search(r'数一|数三', s):
        return 'C_数一数三'
    if re.search(r'19\d\d|20\d\d', s):
        return 'D_其他年份真题'
    return 'E_例题模拟'


c = Counter(kind(q.get('source')) for q in qs)
for k in sorted(c):
    print('  %s: %d' % (k, c[k]))

print()
print('E_例题模拟 source 样本:')
seen = set()
for q in qs:
    if kind(q.get('source')) == 'E_例题模拟':
        s = str(q.get('source') or '')
        if s not in seen:
            seen.add(s)
            print('   %r' % s)
        if len(seen) >= 12:
            break