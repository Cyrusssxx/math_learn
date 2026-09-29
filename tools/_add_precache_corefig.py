# -*- coding: utf-8 -*-
"""把新增的 core_fig 配图加入 sw.js 的 PRECACHE（离线可用）"""
import io, os, re

SW = 'pwa/sw.js'
IMGS = [
    'data/img/core_fig/no208.png',
    'data/img/core_fig/no219.png',
    'data/img/core_fig/no220.png',
    'data/img/core_fig/no357.png',
    'data/img/core_fig/no362.png',
    'data/img/core_fig/no380.png',
    'data/img/core_fig/no515.png',
]

s = io.open(SW, encoding='utf-8').read()
missing_files = [p for p in IMGS if not os.path.exists(os.path.join('pwa', p))]
if missing_files:
    raise SystemExit(f'图片不存在：{missing_files}')

add = [p for p in IMGS if f"'{p}'" not in s]
if not add:
    print('PRECACHE 已包含全部 core_fig 图片，无需修改')
else:
    # 锚点：'data/img/bank/2017race.jpg', 之后插入
    anchor = "    'data/img/bank/2017race.jpg',\n"
    if anchor not in s:
        raise SystemExit('未找到插入锚点')
    block = ''.join(f"    '{p}',\n" for p in add)
    s = s.replace(anchor, anchor + block, 1)
    io.open(SW, 'w', encoding='utf-8', newline='').write(s)
    print(f'已向 PRECACHE 插入 {len(add)} 条：{add}')
