# -*- coding: utf-8 -*-
# 查「21记5-导数应用」的极值/拐点充分条件三段落全文
import json, io

d = json.load(io.open('pwa/data/notes.json', encoding='utf-8'))
n5 = next(n for n in d if n.get('name') == '21记5-导数应用')
md = n5['md']
for key in ('第一充分条件', '第二充分', '第三充分', '拐点'):
    i = md.find(key)
    if i >= 0:
        print('=== [%s] ===' % key)
        print(md[max(0, i - 100):i + 420])
        print()