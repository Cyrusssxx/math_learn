# -*- coding: utf-8 -*-
# 高数0-中学公式速查：删平方差；立方和差拆开（加/减分写）
import json, io

P = 'D:/ai code/math-note/pwa/data/notes.json'
d = json.load(io.open(P, encoding='utf-8'))
n = next(x for x in d if x.get('name') == '高数0-中学公式速查')
md = n['md']

OLD1 = r'  - $(a\pm b)^2=a^2\pm2ab+b^2$；$a^2-b^2=(a-b)(a+b)$'
NEW1 = r'  - $(a\pm b)^2=a^2\pm2ab+b^2$'

OLD2 = r'  - $a^3\pm b^3=(a\pm b)(a^2\mp ab+b^2)$'
NEW2 = r'  - $a^3+b^3=(a+b)(a^2-ab+b^2)$；$a^3-b^3=(a-b)(a^2+ab+b^2)$'

changed = 0
for old, new in ((OLD1, NEW1), (OLD2, NEW2)):
    if old in md:
        md = md.replace(old, new, 1)
        changed += 1
        print('已替换: %r' % old[:40])
    else:
        print('未命中: %r' % old[:40])

n['md'] = md
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(d, fp, ensure_ascii=False, indent=2)

# 复查
d2 = json.load(io.open(P, encoding='utf-8'))
md2 = next(x for x in d2 if x.get('name') == '高数0-中学公式速查')['md']
i = md2.find('乘法公式')
print()
print('修改后:')
print(md2[i:i + 220])
print('变更数:', changed)
