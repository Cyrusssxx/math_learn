# -*- coding: utf-8 -*-
import fitz
import re, json, io

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

# 分析 346 题的章节分布
from _verify_all_346_final2 import final_matches

chap_counts = {}
for m in final_matches:
    ch = m['chapter']
    chap_counts[ch] = chap_counts.get(ch, 0) + 1

print("346 题的章节分布:")
for ch, cnt in chap_counts.items():
    print(f"  {ch}: {cnt} 题")

total = sum(chap_counts.values())
print(f"总计: {total} 题")

# 检查各大章节对应的题目范围
chap_ranges = {}
for m in final_matches:
    ch = m['chapter']
    if ch not in chap_ranges:
        chap_ranges[ch] = [m['pdf_num'], m['pdf_num']]
    else:
        chap_ranges[ch][0] = min(chap_ranges[ch][0], m['pdf_num'])
        chap_ranges[ch][1] = max(chap_ranges[ch][1], m['pdf_num'])

print("\n章节题号区间:")
for ch, r in chap_ranges.items():
    print(f"  {ch}: #{r[0]:03d} ~ #{r[1]:03d} (共 {r[1]-r[0]+1} 题)")
