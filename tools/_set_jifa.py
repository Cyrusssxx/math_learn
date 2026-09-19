# -*- coding: utf-8 -*-
"""按用户指定：把「高数1-极限」函数奇偶段的四则运算口诀块，直接用
   「全奇则奇、有偶则偶」替换（不加其它说明；顺带清理 TAB 损坏）。"""
import json, io

P = 'D:/ai code/math-note/pwa/data/notes.json'
d = json.load(io.open(P, encoding='utf-8'))
md = d[1]['md']
lines = md.split('\n')

start = end = None
for i, L in enumerate(lines):
    if start is None and '四则运算口诀' in L:
        start = i
    if start is not None and '内偶则偶，内奇同外' in L:
        end = i
        break

assert start is not None and end is not None, '未定位到块'
print('定位：L%d ~ L%d' % (start + 1, end + 1))

new_block = [
    '- **奇偶性口诀**：**全奇则奇、有偶则偶**',
    '- 复合：**内偶则偶，内奇同外**',
]
lines[start:end + 1] = new_block
d[1]['md'] = '\n'.join(lines)

with io.open(P, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

d2 = json.load(io.open(P, encoding='utf-8'))
md2 = d2[1]['md']
print('含 全奇则奇、有偶则偶:', '**全奇则奇、有偶则偶**' in md2)
print('含 复合口诀:          ', '内偶则偶，内奇同外' in md2)
print('无「次数相加」:        ', '次数相加' not in md2)
print('无「不是全奇则奇」:    ', '不是「全奇则奇」' not in md2)
print('TAB 损坏残留:          ', md2.count('\times'))
i = md2.find('奇偶性口诀')
print('--- 当前段落 ---')
print(md2[max(0, i - 30):i + 160])