# -*- coding: utf-8 -*-
# 在参考题库里更宽泛地找 f(x+2)-f(x)=x 类题（不论年份）
import json, io, re, os

src = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
ref = json.load(io.open(src, encoding='utf-8'))
items = ref if isinstance(ref, list) else (ref.get('items') or ref.get('questions') or [])
print('参考库条目:', len(items))

pats = ['f(x+2)', 'f(x+2)-f(x)', 'f(x + 2)', '\\int_1^3', 'int_1^3', '_1^3']
for p in pats:
    hits = [it for it in items if p in str(it.get('stem') or it.get('content') or '')]
    print('pattern %-14r → %d' % (p, len(hits)))
    if p in ('f(x+2)', '\\int_1^3') and hits:
        for it in hits[:3]:
            print('   source=%s serial=%s' % (it.get('source'), it.get('serial') or it.get('id')))
            print('   stem: %s' % (str(it.get('stem') or it.get('content') or '')[:220]))
            print('   answer: %s' % (str(it.get('answer'))[:150]))
            print('   exp: %s' % (str(it.get('explanation') or '')[:220]))
            print()

# 列出 2023 数二 的题（看第15题在不在库里）
y23 = [it for it in items if '2023' in str(it.get('source') or '')]
print('2023 相关条目数:', len(y23))
seen = set()
for it in y23[:400]:
    s = str(it.get('source') or '')
    if '数二' in s or '数学二' in s:
        stem = str(it.get('stem') or it.get('content') or '')
        if 'f(x+2)' in stem or 'f（x+2）' in stem:
            print('FOUND:', s, stem[:200])