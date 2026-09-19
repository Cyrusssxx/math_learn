# -*- coding: utf-8 -*-
"""诊断修复失败原因：打印某字段修复前后结构 + 残留错误"""
import json, io, sys
sys.path.insert(0, 'D:/ai code/math-note/tools')
from _fix_formula_v2 import fix_field, errs_of           # noqa
from _audit_formula_v2 import scan                        # noqa

BASE = 'D:/ai code/math-note/pwa/data/'
core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
qs = [q for s in core[0]['sections'] for q in s['questions']]
q = next(x for x in qs if str(x['no']) == '23')
v = q['answer']
new, hits = fix_field(v)
e0, b0 = errs_of(v)
e1, b1 = errs_of(new)
print('原错误: E=%d 裸行=%d | 修复动作: %s' % (len(e0), len(b0), hits))
print('新错误: E=%d 裸行=%d' % (len(e1), len(b1)))
for x in e1[:6]:
    print('   E残留:', x[0], 'L%s' % x[1], x[2][:70] if len(x) > 2 else '')
for x in b1[:6]:
    print('   裸行残留: L%d %s' % x)
print()
print('=== 原（问题行附近）===')
for i, L in enumerate(v.split('\n')):
    if 60 <= i <= 80:
        print('L%-3d (%d$) %s' % (i, L.count('$'), L[:110]))
print()
print('=== 修复后 ===')
for i, L in enumerate(new.split('\n')):
    if 58 <= i <= 86:
        print('L%-3d (%d$) %s' % (i, L.count('$'), L[:110]))
