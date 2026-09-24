# -*- coding: utf-8 -*-
# 看 xd 解析长度分布 + 最长的几道（判断是否需精简）
import json, io

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]
qs2 = sorted(qs, key=lambda q: -len(str(q.get('idea') or '')))
print('=== 最长的 5 道解析 ===')
for q in qs2[:5]:
    print('no=%s len=%d | src=%s' % (q['no'], len(str(q.get('idea') or '')), str(q.get('source'))[:30]))
    print('  ', (q.get('idea') or '')[:300].replace('\n', ' '))
    print()
# 分段统计
buckets = {'<50': 0, '50-150': 0, '150-300': 0, '300-500': 0, '>500': 0}
for q in qs:
    n = len(str(q.get('idea') or ''))
    if n < 50: buckets['<50'] += 1
    elif n < 150: buckets['50-150'] += 1
    elif n < 300: buckets['150-300'] += 1
    elif n < 500: buckets['300-500'] += 1
    else: buckets['>500'] += 1
print('解析长度分布:', buckets)
# 含"答案待补充"的
todo = [q['no'] for q in qs if '待补充' in str(q.get('idea') or '')]
print('含「待补充」:', todo)