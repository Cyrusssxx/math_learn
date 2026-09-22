# -*- coding: utf-8 -*-
# 精选 xd_bank：数二真题全留（264）+ 数一数三按知识点均衡补充（~90）→ ~354 题
import json, io, re
from collections import defaultdict

bank = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = []
for s in bank[0]['sections']:
    for q in s['questions']:
        qs.append({'q': q, 'sec': s['title']})

def tier(src):
    s = src or ''
    if re.search(r'数二', s):
        return 'A'
    if re.search(r'数一|数三', s):
        return 'B'
    if re.search(r'19\d\d|20\d\d', s):
        return 'B'
    return 'C'

for it in qs:
    it['tier'] = tier(it['q'].get('source') or '')

# 按知识点分组（保持知识点内顺序）
bycat = defaultdict(list)
for it in qs:
    c0 = str((it['q'].get('categoryIds') or [None])[0])
    bycat[c0].append(it)

# A 全留；B 按知识点轮转补足（每轮每知识点取 1 题，直到目标）
picked = []
picked_ids = set()
for it in qs:
    if it['tier'] == 'A':
        picked.append(it)
        picked_ids.add(id(it['q']))

target_B = 90
# 知识点轮转：按知识点当前 A 数量从少到多排，每轮各取 1 个 B
cats_sorted = sorted(bycat.keys(), key=lambda c: -len(bycat[c]))
rounds = 0
while len([p for p in picked if p['tier'] == 'B']) < target_B and rounds < 60:
    rounds += 1
    for c in cats_sorted:
        for it in bycat[c]:
            if it['tier'] == 'B' and id(it['q']) not in picked_ids:
                picked.append(it)
                picked_ids.add(id(it['q']))
                break
        if len([p for p in picked if p['tier'] == 'B']) >= target_B:
            break

nA = len([p for p in picked if p['tier'] == 'A'])
nB = len([p for p in picked if p['tier'] == 'B'])
print('精选: 总 %d = A %d + B %d' % (len(picked), nA, nB))

# 重建题库（保持知识点分组 + 原顺序）
sec_map = defaultdict(list)
order = {}
for it in picked:
    c0 = it['sec']
    sec_map[c0].append(it['q'])
bank[0]['sections'] = [{'title': c, 'questions': sec_map[c]} for c in sorted(sec_map, key=int)]
with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as fp:
    json.dump(bank, fp, ensure_ascii=False, separators=(',', ':'))

# 分布报告
from collections import Counter
tc = Counter(p['tier'] for p in picked)
print('分层:', dict(tc))
cnt = Counter(it['sec'] for it in picked)
print('知识点覆盖:', len(cnt), '个；Top:', cnt.most_common(5))
