# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

p2024 = next(p for p in exam_data if p.get('id') == '2024数二真题')
print("=== 本库 2024数二真题 题目结构 ===")
for sec in p2024.get('sections', []):
    print(f"Section: {sec.get('title')}")
    for q in sec.get('questions', []):
        no = q.get('no')
        opts = q.get('options', [])
        stem = q.get('stem', '').replace('\n', ' ')[:45]
        print(f"  No: {no} | opts_len: {len(opts)} | stem: {stem}")
