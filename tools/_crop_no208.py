# -*- coding: utf-8 -*-
"""裁剪 nynu 第2页第10题（03年导函数图形题）的配图 → no208"""
import pymupdf as fitz
import shutil, os

# no220 重命名规范化
src = 'pwa/data/img/core_fig/no220_raw.png'
if os.path.exists(src):
    shutil.move(src, 'pwa/data/img/core_fig/no220.png')
    print('no220.png 已规范化')

doc = fitz.open('tools/_web_imgs/nynu_daoyanshou.pdf')
page = doc[1]
# 图在第(D)选项下方（PDF pt 坐标，按整页渲染推算），先裁一个窗口，Read 验证
clip = fitz.Rect(90, 410, 360, 560)
pm = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip)
pm.save('pwa/data/img/core_fig/no208.png')
print(f'no208.png 裁剪完成 ({pm.width}x{pm.height})，待 Read 验证')
doc.close()
