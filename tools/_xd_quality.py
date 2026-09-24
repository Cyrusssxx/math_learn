# -*- coding: utf-8 -*-
# 检测 xd_bank 全部题的 answer / idea(解析) 质量：缺失、过短、含异常
import json, io, re
from collections import Counter

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]
print('xd_bank 总题:', len(qs))

stat = Counter()
short_ans, short_idea, empty_ans, empty_idea = [], [], [], []
for q in qs:
    a = str(q.get('answer') or '').strip()
    e = str(q.get('idea') or '').strip()
    na, ne = len(a), len(e)
    if not a:
        empty_ans.append(q['no'])
    elif na < 8:
        short_ans.append((q['no'], a))
    if not e:
        empty_idea.append(q['no'])
    elif ne < 30:
        short_idea.append((q['no'], e[:40]))
    stat['ans<8'] += 1 if (a and na < 8) else 0
    stat['idea<30'] += 1 if (e and ne < 30) else 0

print('answer 缺失:', len(empty_ans), '| 极短(<8字):', len(short_ans))
print('idea(解析) 缺失:', len(empty_idea), '| 极短(<30字):', len(short_idea))
print()
print('=== 极短 answer 样本 10 ===')
for no, a in short_ans[:10]:
    print('  no=%s: %r' % (no, a))
print()
print('=== 极短 idea 样本 10 ===')
for no, e in short_idea[:10]:
    print('  no=%s: %r' % (no, e))
print()
# 长度分布
lens_a = [len(str(q.get('answer') or '')) for q in qs]
lens_e = [len(str(q.get('idea') or '')) for q in qs]
import statistics as st
print('answer 长度: 中位 %d, 均值 %d, 最短 %d, 最长 %d' % (st.median(lens_a), sum(lens_a)/len(lens_a), min(lens_a), max(lens_a)))
print('idea  长度: 中位 %d, 均值 %d, 最短 %d, 最长 %d' % (st.median(lens_e), sum(lens_e)/len(lens_e), min(lens_e), max(lens_e)))
# 样例
print()
print('=== 随机 2 题完整样例 ===')
for q in qs[100:102]:
    print('no=%s | src=%s' % (q['no'], q.get('source')))
    print('  stem:', (q.get('stem') or '')[:70])
    print('  answer:', (q.get('answer') or '')[:120])
    print('  idea:', (q.get('idea') or '')[:160])