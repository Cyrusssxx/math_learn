# -*- coding: utf-8 -*-
"""定位题602（core_bank no=602，2025数一）的 answer，打印行级 $ 结构"""
import json, io
import sys
sys.path.insert(0, 'D:/ai code/math-note/tools')
from _audit_formula_v2 import scan                       # noqa

BASE = 'D:/ai code/math-note/pwa/data/'
core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
qs = [q for s in core[0]['sections'] for q in s['questions']]
q = next(x for x in qs if str(x['no']) == '602')
print('source:', q.get('source'), '| catId:', q.get('catId'), '| deepCats:', q.get('deepCats'))
v = q['answer']
e, b = scan(v)
print('scan: E=%s 裸行=%s' % (e, b))
print('len=%d  $数=%d' % (len(v), v.count('$')))
print()
for i, L in enumerate(v.split('\n')):
    print('L%-3d (%d$) %s' % (i, L.count('$'), L[:120]))
