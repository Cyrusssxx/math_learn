# -*- coding: utf-8 -*-
"""把 52 页扫描 PDF 渲染缩略拼版，用于判断题号与版面结构。"""
import fitz
from PIL import Image, ImageDraw
import os

SRC = r'E:/Desktop/做题/高数模拟卷/【解析】27张宇四套卷数二.pdf'
OUT = r'C:/Users/cjx/AppData/Local/Temp/zs4_pdf_contact.png'
doc = fitz.open(SRC)
thumbs = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(0.55, 0.55), colorspace=fitz.csGRAY, alpha=False)
    im = Image.frombytes('L', (pix.width, pix.height), pix.samples).convert('RGB')
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 62, 22], fill='white')
    d.text((4, 4), 'P%02d' % (i + 1), fill='red')
    thumbs.append(im)
w, h = thumbs[0].size
cols = 8
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * h), 'white')
for i, im in enumerate(thumbs):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(OUT)
print(OUT, sheet.size, 'page size', w, h)
