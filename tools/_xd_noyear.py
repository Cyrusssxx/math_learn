# -*- coding: utf-8 -*-
# 看 xd 里「数二」类中无年份的 204 道 source 真实形态
import json, io, re
from collections import Counter

xd = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
xq = [q for s in xd[0]['sections'] for q in s['questions']]
s2 = [q for q in xq if re.search(r'数二', str(q.get('source') or ''))]
noyear = [q for q in s2 if not re.search(r'\d{4}', str(q.get('source') or ''))]
print('「数二」类无年份:', len(noyear))
c = Counter(str(q.get('source') or '') for q in noyear)
print('\nsource 分布:')
for s, n in c.most_common(20):
    print('  %r: %d' % (s[:60], n))
print('\n样本（source + stem）:')
for q in noyear[:6]:
    print('  no=%s src=%r' % (q['no'], str(q.get('source') or '')[:40]))
    print('     stem=%s' % (q.get('stem') or '')[:70])
