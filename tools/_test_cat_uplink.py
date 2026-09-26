# -*- coding: utf-8 -*-
import json, io, os

with io.open('pwa/data/exam_categories.json', 'r', encoding='utf-8') as f:
    ecats = json.load(f)

with io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/categories.json', 'r', encoding='utf-8') as f:
    dcats = json.load(f).get('items', [])

dnode = {n['id']: n for n in dcats}

def map_to_exam_cat(d_cids):
    # d_cids 是大观园的 categoryIds
    res = []
    for cid in d_cids:
        curr = cid
        # 如果已经在 exam_categories 中
        while curr:
            if str(curr) in ecats:
                res.append(curr)
                break
            curr = dnode.get(curr, {}).get('parentId')
    return list(set(res))

# 测试几个
from _verify_all_346_final2 import final_matches

print("=== 测试大观园 categoryIds 向上归并到 exam_categories ===")
missing_cat = []
for m in final_matches:
    cids = m['item'].get('categoryIds', [])
    mc = map_to_exam_cat(cids)
    if not mc:
        missing_cat.append((m['pdf_num'], m['chapter'], m['topic'], cids))
        
print(f"346 题中无法映射考点的题目数: {len(missing_cat)}")
if missing_cat:
    for mc in missing_cat[:5]:
        print(f"  #{mc[0]} | {mc[1]} | {mc[2]} | cids: {mc[3]}")
else:
    print("全部 346 题均可完美自动上溯到已有的 45 个二级线代知识点！")
