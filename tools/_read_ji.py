# -*- coding: utf-8 -*-
# 读「高数2-一元微分」极值充分/拐点段落 + 全库排查其他「条件1/2/3」式条目
import json, io, re

d = json.load(io.open('pwa/data/notes.json', encoding='utf-8'))
n2 = next(n for n in d if n.get('name') == '高数2-一元微分')
md = n2['md']

for key in ('极值充分', '拐点', '凹凸充分'):
    i = md.find(key)
    if i >= 0:
        print('=== [%s] 上下文 ===' % key)
        print(md[i:i + 500])
        print()

print('====== 全库排查其他「条件一/二/三」「第一/二/三充分」式条目 ======')
pat = re.compile(r'(条件[一二三123]|第[一二三123]充分|充分条件[一二三123])')
for n in d:
    md2 = n.get('md') or ''
    for m in pat.finditer(md2):
        s = max(0, m.start() - 40)
        frag = md2[s:m.start() + 80].replace('\n', ' ')
        print('[%s] ...%s...' % (n.get('name'), frag))
        break  # 每篇笔记只报一次位置样本