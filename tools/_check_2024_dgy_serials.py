# -*- coding: utf-8 -*-
import json, io

src = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
with io.open(src, 'r', encoding='utf-8') as f:
    dgy = json.load(f)
    items = dgy if isinstance(dgy, list) else dgy.get('items', [])

print("=== 检查 2024 年题号与真题实际题号 ===")
# 考研数二真题结构：
# 1~10: 选择题（每题5分，共50分）
# 11~16: 填空题（每题5分，共30分）
# 17~22: 解答题（共70分，17为10分，18~22为12分）

for serial in range(4957, 4979):
    it = next((x for x in items if x.get('serial') == serial), None)
    if it:
        stem = it.get('stem', '').replace('\n', ' ')[:50]
        opts = it.get('options', [])
        is_choice = len(opts) > 0
        print(f"serial: {serial} | is_choice: {is_choice} | opts_len: {len(opts)} | stem: {stem}")
