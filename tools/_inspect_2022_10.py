# -*- coding: utf-8 -*-
import json, io, os

# 1. 检查 exam.json 中 2022 年第 10 题
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

for paper in exam_data:
    if '2022' in paper.get('id', '') or '2022' in paper.get('title', ''):
        for sec in paper.get('sections', []):
            for q in sec.get('questions', []):
                if str(q.get('no')) == '10':
                    print("=== 2022 题 10 当前在库内容 ===")
                    print("stem:", repr(q.get('stem')))
                    print("options:", repr(q.get('options')))
                    print("answer:", repr(q.get('answer')))
                    print("idea:", repr(q.get('idea'))[:200])

# 2. 检查大观园参考题库中的 2022-10 题原样
src = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
if os.path.exists(src):
    with io.open(src, 'r', encoding='utf-8') as f:
        dgy = json.load(f)
        items = dgy if isinstance(dgy, list) else dgy.get('items', [])
        print("\n=== 大观园题库中 2022 数二第 10 题 ===")
        for it in items:
            src_str = str(it.get('source', ''))
            if '2022' in src_str and ('数二' in src_str or '数学二' in src_str):
                # 检查是否包含 alpha 或 等价
                stem = str(it.get('stem', ''))
                if 'alpha_1' in stem or '\\alpha_1' in stem or '等价' in stem:
                    print("serial:", it.get('serial'), "source:", src_str)
                    print("stem:", repr(stem))
                    print("options:", repr(it.get('options')))
                    print("answer:", repr(it.get('answer')))
                    print("exp:", repr(it.get('explanation', ''))[:200])
