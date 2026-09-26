# -*- coding: utf-8 -*-
import fitz
import re, json, io

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

# 打印一些页面块，研究灰条和题目的排版
for pno in [5, 6, 7]: # 第 6, 7, 8 页
    page = doc[pno]
    blocks = page.get_text("blocks")
    print(f"=== Page {pno+1} Blocks ===")
    for b in blocks:
        # b: (x0, y0, x1, y1, text, block_no, block_type)
        txt = b[4].strip().replace('\n', ' ')
        if txt:
            print(f"  ({b[0]:.1f}, {b[1]:.1f}) -> {txt[:100]}")
