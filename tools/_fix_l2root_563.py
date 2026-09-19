# -*- coding: utf-8 -*-
"""修正 l2root 误映射：本库 L2「二重积分/其他」(563) 应指向大观园真节点「二重积分/其他」(563)，
   而不是深层的「二重积分/计算/极坐标/其他」(585)。"""
import json, io

P = 'D:/ai code/math-note/pwa/data/cat_deep.json'
d = json.load(io.open(P, encoding='utf-8'))
old = d['l2root'].get('563')
d['l2root']['563'] = '563'
json.dump(d, io.open(P, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), sort_keys=True)

d2 = json.load(io.open(P, encoding='utf-8'))
print('563 映射: %s → %s' % (old, d2['l2root']['563']))
print('l2root 条数:', len(d2['l2root']))
print('格式单行:', io.open(P, encoding='utf-8').read().count('\n') == 0)