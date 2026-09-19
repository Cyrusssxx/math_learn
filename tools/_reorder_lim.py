# -*- coding: utf-8 -*-
"""在「高数1-极限」这一章内重排小节：把常用计算/公式小节移到目录最前。
   同时同步 chapters 数组（与 ## 标题一一对应），保证 toc / 章节 hash 不错位。"""
import json, io

P = 'D:/ai code/math-note/pwa/data/notes.json'
d = json.load(io.open(P, encoding='utf-8'))
n = d[1]
md = n['md']
lines = md.split('\n')

# 切块：头部（# 标题等，到第一个 ## 之前）+ 各 ## 小节块
head, blocks, cur = [], [], None
for L in lines:
    if L.startswith('## '):
        cur = [L]
        blocks.append(cur)
    elif cur is not None:
        cur.append(L)
    else:
        head.append(L)

# 各块标题
titles = [b[0][3:] for b in blocks]
print('原顺序 %d 节:' % len(titles))
for i, t in enumerate(titles):
    print('   %2d  %s' % (i + 1, t))

# 常用置顶清单（按此顺序放最前）
PIN = ['泰勒公式', '极限计算：七类未定式', '极限计算：三大思路', '微积分工具']

def idx(t):
    try:
        return PIN.index(t.split(' ')[0] if not t.startswith('极限') else t)
    except ValueError:
        return None

# 把 PIN 中的节抽出置顶（保持 PIN 顺序），其余按原序
pin_blocks, rest = [], []
for b in blocks:
    t = b[0][3:]
    in_pin = next((p for p in PIN if t.startswith(p)), None)
    if in_pin:
        pin_blocks.append(b)
    else:
        rest.append(b)

# 按 PIN 顺序排列置顶块（处理同名前缀：顺序按在 PIN 中的出现）
order = {t: i for i, t in enumerate(PIN)}
pin_blocks.sort(key=lambda b: order[next(p for p in PIN if b[0][3:].startswith(p))])
new_blocks = pin_blocks + rest

out = '\n'.join(head) + '\n' + '\n'.join('\n'.join(b) for b in new_blocks)
n['md'] = out

# 同步 chapters（重排后 md 的 ## 标题顺序）
new_chapters = [b[0][3:].split('<!--')[0].strip() for b in new_blocks]
n['chapters'] = new_chapters

with io.open(P, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# 验证
d2 = json.load(io.open(P, encoding='utf-8'))
md2 = d2[1]['md']
hs = [L[3:].split('<!--')[0].strip() for L in md2.split('\n') if L.startswith('## ')]
print()
print('重排后 %d 节:' % len(hs))
for i, t in enumerate(hs):
    print('   %2d  %s' % (i + 1, t))
print()
print('chapters 与 ## 顺序一致:', hs == d2[1]['chapters'])
print('前 4 节为常用:', hs[:4] == ['泰勒公式', '极限计算：七类未定式', '极限计算：三大思路', '微积分工具'])