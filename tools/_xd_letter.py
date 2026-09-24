# -*- coding: utf-8 -*-
# 精确统计：answer 仅为选项字母 的题（真正的问题）, 并看其解析长度
import json, io, re

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]

only_letter = []
for q in qs:
    a = str(q.get('answer') or '').strip()
    # 纯字母（可能带 $ 或括号/句点）
    if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', a) and re.search(r'[A-Da-d]', a):
        only_letter.append(q)

print('答案仅为选项字母的题:', len(only_letter), '/', len(qs))
print()
# 它们的解析长度分布
lens = sorted(len(str(q.get('idea') or '')) for q in only_letter)
print('其解析长度: 最短 %d, 中位 %d, 最长 %d' % (lens[0], lens[len(lens)//2], lens[-1]))
b = {'<50': 0, '50-100': 0, '100-200': 0, '>200': 0}
for q in only_letter:
    n = len(str(q.get('idea') or ''))
    if n < 50: b['<50'] += 1
    elif n < 100: b['50-100'] += 1
    elif n < 200: b['100-200'] += 1
    else: b['>200'] += 1
print('解析长度分布:', b)
print()
print('=== 样本 5 道（题面 + 现有答案/解析）===')
for q in only_letter[:5]:
    print('--- no=%s | src=%s' % (q['no'], str(q.get('source'))[:30]))
    print('  stem:', (q.get('stem') or '')[:90].replace('\n', ' '))
    opts = q.get('options') or []
    if opts:
        print('  opts:', ' | '.join(str(o)[:34] for o in opts[:4]))
    print('  answer:', repr(q.get('answer')))
    print('  idea:', (q.get('idea') or '')[:130].replace('\n', ' '))
    print()
# 解析低于 100 字的（真正需要补全的）
weak = [q for q in only_letter if len(str(q.get('idea') or '')) < 100]
print('其中解析<100字的:', len(weak), '→ 这些是需重写的重点')
print('题号:', [q['no'] for q in weak][:30])