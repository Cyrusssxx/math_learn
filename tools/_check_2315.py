# -*- coding: utf-8 -*-
# 核对 2023 数二 第15题：我们的 exam.json vs 大观园权威题库
import json, io, re, os

exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
v = next(v for v in exam if v['id'] == '2023数二真题')
q = next(q for s in v['sections'] for q in s['questions'] if str(q['no']) == '15')
print('=== 本库 exam.json 2023数二-15 ===')
print('stem:', q.get('stem'))
print('answer:', repr(q.get('answer')))
print('idea:', (q.get('idea') or '')[:300])
print('options:', q.get('options'))

src = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
if os.path.exists(src):
    ref = json.load(io.open(src, encoding='utf-8'))
    items = ref if isinstance(ref, list) else (ref.get('items') or ref.get('questions') or [])
    print()
    print('=== 大观园题库中 2023 数二 第15题 ===')
    hits = []
    for it in items:
        s = str(it.get('source') or '')
        if '2023' in s and re.search(r'数二|数学二', s):
            st = str(it.get('stem') or it.get('content') or '')
            if 'f(x+2)-f(x)' in st or 'f(x+2)' in st:
                hits.append(it)
    print('命中:', len(hits))
    for it in hits[:3]:
        print('source:', it.get('source'), '| serial:', it.get('serial') or it.get('id'))
        print('stem:', (it.get('stem') or it.get('content') or '')[:300])
        print('answer:', repr(it.get('answer'))[:200])
        print('explanation:', (it.get('explanation') or '')[:300])
        print('---')
else:
    print('参考题库不存在:', src)