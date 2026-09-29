# -*- coding: utf-8 -*-
"""通用：从真题 PDF 中定位某题的文字与绘图块，裁剪配图
用法: python tools/_extract_fig_generic.py <pdf> "<关键词>" <输出png> [页号(0起)]
"""
import pymupdf as fitz
import sys, os

pdf = sys.argv[1]
kw = sys.argv[2]
out = sys.argv[3]
page_no = int(sys.argv[4]) if len(sys.argv) > 4 else None


def analyze(page, pno):
    """返回 (文字命中坐标, 绘图块列表) 均在默认(显示)坐标系"""
    hits = []
    for k in kw.split('|'):
        for r in page.search_for(k):
            hits.append((k, r))
    log = page.get_bboxlog()
    paths = []
    for typ, rect in log:
        if 'text' in typ:
            continue
        r = rect if isinstance(rect, fitz.Rect) else fitz.Rect(rect)
        if r.width > 3 or r.height > 3:
            paths.append(r)
    return hits, paths


doc = fitz.open(pdf)
pages = range(len(doc)) if page_no is None else [page_no]
found = False
for pno in pages:
    page = doc[pno]
    hits, paths = analyze(page, pno)
    if not hits:
        continue
    found = True
    print(f'--- 第{pno+1}页 | 文字命中 {len(hits)} | 绘图块 {len(paths)} ---')
    for k, r in hits[:6]:
        print(f'   文字"{k}" @ ({r.x0:.0f},{r.y0:.0f},{r.x1:.0f},{r.y1:.0f})')
    if not paths:
        print('   ⚠️ 本页无矢量绘图块（可能是位图或图在别页）')
        for xref, *_ in page.get_images(full=True)[:5]:
            for rr in page.get_image_rects(xref):
                print(f'   位图 xref={xref} @ ({rr.x0:.0f},{rr.y0:.0f},{rr.x1:.0f},{rr.y1:.0f})')
        continue
    for r in paths:
        print(f'   绘图块: ({r.x0:.0f},{r.y0:.0f},{r.x1:.0f},{r.y1:.0f}) {r.width:.0f}x{r.height:.0f}')
    # 合并所有绘图块 → 裁剪（外扩 8pt）
    ub = paths[0]
    for r in paths[1:]:
        ub = ub | r
    clip = fitz.Rect(ub.x0 - 8, ub.y0 - 8, ub.x1 + 8, ub.y1 + 8)
    pm = page.get_pixmap(matrix=fitz.Matrix(5, 5), clip=clip)
    pm.save(out)
    print(f'   ✅ 已裁剪绘图块并集 ({clip.x0:.0f},{clip.y0:.0f},{clip.x1:.0f},{clip.y1:.0f}) → {out} ({pm.width}x{pm.height})')
    break
if not found:
    print('未命中关键词')
