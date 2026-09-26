# -*- coding: utf-8 -*-
import json, io, os

with io.open('pwa/data/exam_categories.json', 'r', encoding='utf-8') as f:
    ecats = json.load(f)

print(f"exam_categories.json 节点数: {len(ecats)}")
for cid, cinfo in sorted(ecats.items(), key=lambda x: int(x[0])):
    if [2, 3, 4, 5, 6, 7].count(cinfo.get('parentId')) or cid in ['1', '2', '3', '4', '5', '6', '7']:
        print(f"  id {cid:<4} | parent: {str(cinfo.get('parentId')):<4} | name: {cinfo.get('name')}")
