# -*- coding: utf-8 -*-
"""提取 no220（xdf PDF 位图）+ 渲染 nynu 第2页供定位 no208 矢量图"""
import pymupdf as fitz
import os

os.makedirs('pwa/data/img/core_fig', exist_ok=True)
os.makedirs('tools/_web_imgs', exist_ok=True)

# 1. no220：xdf 第2页 xref=34（207x162，位于题干下方）
doc = fitz.open('tools/_web_imgs/xdf_2016shu2.pdf')
pix = fitz.Pixmap(doc, 34)
if pix.alpha:
    pix = fitz.Pixmap(fitz.csRGB, pix)
pix.save('pwa/data/img/core_fig/no220_raw.png')
print(f'no220: 已提取 xref=34 → {pix.width}x{pix.height}')
doc.close()

# 2. no208：nynu 第2页整页渲染（矢量图，需页面裁剪）
doc2 = fitz.open('tools/_web_imgs/nynu_daoyanshou.pdf')
page = doc2[1]
# 找第 10 题题干位置定位裁剪窗口
for kw in ['10.', '导函数的图形', '则 f', '极小值点']:
    for r in page.search_for(kw):
        print(f'nynu p2 文字"{kw}" @ ({r.x0:.0f},{r.y0:.0f},{r.x1:.0f},{r.y1:.0f})')
mat = fitz.Matrix(3, 3)  # 3x 渲染
pm = page.get_pixmap(matrix=mat)
pm.save('tools/_web_imgs/nynu_p2_full.png')
print(f'nynu 第2页整页渲染 → tools/_web_imgs/nynu_p2_full.png ({pm.width}x{pm.height})')
doc2.close()
