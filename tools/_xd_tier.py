# -*- coding: utf-8 -*-
# 精选前分析：xd_bank 分层（数二真题/数一数三真题/例题）+ 质量过滤统计
import json, io, re
from collections import Counter

bank = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = []
for s in bank[0]['sections']:
    for q in s['questions']:
        qs.append(q)
print('总题数:', len(qs))

def tier(src):
    s = src or ''
    if re.search(r'数二', s):
        return 'A_数二真题'
    if re.search(r'数一|数三', s):
        return 'B_数一数三'
    if re.search(r'真题同源|姜晓千|强化|基础|例题|模拟|六套|套卷|900|880|李永乐', s):
        return 'C_例题模拟'
    if re.search(r'19\d\d|20\d\d', s):
        return 'B_数一数三'   # 有年份无科目标记（多为真题）
    return 'D_其他'

t = Counter(tier(q.get('source') or '') for q in qs)
print('分层:')
for k, n in t.most_common():
    print('  %s: %d' % (k, n))

# 质量过滤：stem/answer/idea 非空 + 选项完整（若 options 非空则应 4 项）
def quality(q):
    if not (q.get('stem') or '').strip():
        return False
    if not (q.get('answer') or '').strip():
        return False
    if not (q.get('idea') or '').strip():
        return False
    opts = q.get('options') or []
    if opts and len(opts) < 3:
        return False
    return True

bad = [q for q in qs if not quality(q)]
print('\n质量不合格:', len(bad))
# 按知识点统计可用题
from collections import defaultdict
bycat = defaultdict(list)
for q in qs:
    if quality(q):
        c0 = str((q.get('categoryIds') or [None])[0])
        bycat[c0].append(q)
print('可用题按知识点（前 10）:')
for c, lst in sorted(bycat.items(), key=lambda x: -len(x[1]))[:10]:
    print('  %s: %d' % (c, len(lst)))
