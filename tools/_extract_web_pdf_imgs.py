# -*- coding: utf-8 -*-
"""从网上下载的 PDF 中定位目标题干并提取其内嵌图片"""
import pymupdf as fitz
import json, io, os

OUT_DIR = 'pwa/data/img/core_fig'
os.makedirs(OUT_DIR, exist_ok=True)

JOBS = [
    # (pdf路径, 题干搜索串, 题号标签)
    ('tools/_web_imgs/xdf_2016shu2.pdf', '其导函数的图形如图所示', 'no220'),
    ('tools/_web_imgs/nynu_daoyanshou.pdf', '导函数的图形如图所示', 'no208'),
]

for pdf_path, keyword, tag in JOBS:
    if not os.path.exists(pdf_path):
        print(f'跳过（文件不存在）: {pdf_path}')
        continue
    doc = fitz.open(pdf_path)
    print(f'\n=== {pdf_path} | 页数 {len(doc)} | 关键词 "{keyword}" ===')
    # 1. 定位题干文字位置
    anchor_rects = []
    for pno in range(len(doc)):
        for r in doc[pno].search_for(keyword):
            anchor_rects.append((pno, r))
    print(f'  题干命中 {len(anchor_rects)} 处: {[(p, tuple(round(v) for v in r)) for p, r in anchor_rects]}')
    # 2. 列出候选页的内嵌图片（位置+尺寸）
    for pno, r in anchor_rects:
        page = doc[pno]
        print(f'  -- 第 {pno + 1} 页的内嵌图片 --')
        for xref in [im[0] for im in page.get_images(full=True)]:
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                continue
            for rr in rects:
                # 距离题干文字块的距离（垂直方向优先）
                dy = rr.y0 - r.y1 if rr.y0 >= r.y1 else r.y0 - rr.y1
                print(f'    xref={xref} rect=({rr.x0:.0f},{rr.y0:.0f},{rr.x1:.0f},{rr.y1:.0f}) size={rr.width:.0f}x{rr.height:.0f} 与题干dy={dy:.0f}')
        # 3. 取该页中在题干下方 400pt 内、宽>80pt 的第一张图 → 提取像素保存
        best = None
        for xref in [im[0] for im in page.get_images(full=True)]:
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                continue
            for rr in rects:
                if rr.y0 >= r.y1 - 10 and rr.width > 80 and rr.height > 60:
                    gap = rr.y0 - r.y1
                    if gap < 500 and (best is None or gap < best[0]):
                        best = (gap, xref, rr)
        if best:
            _, xref, rr = best
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.alpha:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                out = os.path.join(OUT_DIR, f'{tag}_raw.png')
                pix.save(out)
                print(f'  ✅ 已提取 → {out} (xref={xref}, {pix.width}x{pix.height})')
            except Exception as e:
                print(f'  ❌ 像素提取失败 xref={xref}: {e}')
        else:
            print('  ❌ 未找到题干下方的合适图片')
    doc.close()
