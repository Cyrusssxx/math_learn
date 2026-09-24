# -*- coding: utf-8 -*-
# 过滤 xd_bank：移除「数一/数三」题（93 道）与其他非数二题，保留数二真题 + 数二练习册 + 共用题
import json, io, re
from collections import Counter

P = 'pwa/data/xd_bank.json'
d = json.load(io.open(P, encoding='utf-8'))


def keep(src):
    s = str(src or '')
    # 移除：数一/数三 独有
    if re.search(r'数一|数三', s):
        return False
    return True


before = sum(len(sec['questions']) for sec in d[0]['sections'])
removed = []
for sec in d[0]['sections']:
    newq = []
    for q in sec['questions']:
        if keep(q.get('source')):
            newq.append(q)
        else:
            removed.append(str(q.get('source')))
    sec['questions'] = newq
# 删空分组
d[0]['sections'] = [sec for sec in d[0]['sections'] if sec['questions']]
after = sum(len(sec['questions']) for sec in d[0]['sections'])

print('xd_bank: %d → %d（移除 %d）' % (before, after, before - after))
print('移除的 source 样本:', Counter(removed).most_common(5))

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(d, fp, ensure_ascii=False, separators=(',', ':'))
print('已写回')

# 复查
d2 = json.load(io.open(P, encoding='utf-8'))
q2 = [q for s in d2[0]['sections'] for q in s['questions']]
c = {}
for q in q2:
    src = str(q.get('source') or '')
    if re.search(r'900|李艳芳|张宇|李永乐|模拟', src):
        c['数二练习册'] = c.get('数二练习册', 0) + 1
    elif re.search(r'\d{4}', src):
        c['数二真题(带年份)'] = c.get('数二真题(带年份)', 0) + 1
    elif '数学一二三' in src:
        c['共用'] = c.get('共用', 0) + 1
    else:
        c['其他'] = c.get('其他', 0) + 1
print('过滤后构成:', c, '| 总', len(q2))