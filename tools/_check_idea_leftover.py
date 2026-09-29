# -*- coding: utf-8 -*-
"""定位 idea 中的残留旧解析（含 ### 标题、与被重写答案不一致）"""
import json, io

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

NOS = [23, 54, 153, 160, 185, 211, 227, 255, 316, 397, 404, 412, 416, 432, 471]
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            if q.get('no') not in NOS:
                continue
            idea = str(q.get('idea') or '')
            flag = '###' in idea or '第二步' in idea or len(idea) > 400
            if flag:
                print(f"--- no={q.get('no')} | idea长度={len(idea)} ---")
                print(idea[:400])
                print()
