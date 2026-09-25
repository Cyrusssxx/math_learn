# -*- coding: utf-8 -*-
import json, io, os, re

src = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
with io.open(src, 'r', encoding='utf-8') as f:
    dgy = json.load(f)
    items = dgy if isinstance(dgy, list) else dgy.get('items', [])

print("=== 搜索大观园题库中包含 2022 / 2024 的数二题目 ===")
dgy_2022 = {}
dgy_2024 = {}

for it in items:
    s = str(it.get('source', ''))
    # 查找数二真题
    if ('2022' in s or '2024' in s) and ('数二' in s or '数学二' in s):
        # 看看是真题还是模拟/练习册
        # 打印出来看看
        stem = it.get('stem', '')
        print("source:", s, "serial:", it.get('serial'), "stem[:40]:", stem[:40].replace('\n', ' '))
