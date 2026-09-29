# -*- coding: utf-8 -*-
"""Dump 两个网上 PDF 的全部内嵌图片清单 + 每页文字首行（帮助定位题）"""
import pymupdf as fitz
import os

for pdf_path in ['tools/_web_imgs/xdf_2016shu2.pdf', 'tools/_web_imgs/nynu_daoyanshou.pdf']:
    if not os.path.exists(pdf_path):
        print(f'缺失: {pdf_path}')
        continue
    doc = fitz.open(pdf_path)
    print(f'\n===== {pdf_path} | {len(doc)} 页 =====')
    for pno in range(len(doc)):
        page = doc[pno]
        imgs = page.get_images(full=True)
        # 文字：找题号标记
        txt = page.get_text()
        marks = []
        for key in ['(4)', '(2)', '10.', '导函数', '拐点', '曲线段']:
            if key in txt:
                marks.append(key)
        if not imgs and not marks:
            continue
        print(f'  第{pno+1}页: 内嵌图 {len(imgs)} 张 | 关键词 {marks}')
        # 找含关键词的行位置
        for kw in ['导函数的图形', '曲线段的方程', '拐点个数']:
            for r in page.search_for(kw):
                print(f'    文字"{kw}" @ ({r.x0:.0f},{r.y0:.0f},{r.x1:.0f},{r.y1:.0f})')
        for im in imgs:
            xref = im[0]
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                rects = []
            w = im[2]
            h = im[3]
            for rr in rects:
                print(f'    图 xref={xref} 像素={w}x{h} 页面位置=({rr.x0:.0f},{rr.y0:.0f})-({rr.x1:.0f},{rr.y1:.0f})')
            if not rects:
                print(f'    图 xref={xref} 像素={w}x{h} (页面未引用)')
    doc.close()
