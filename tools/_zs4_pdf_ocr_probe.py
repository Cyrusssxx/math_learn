# -*- coding: utf-8 -*-
"""探测官方答案册每页：标题、页脚、行首题号。"""
import fitz, re, json
from rapidocr_onnxruntime import RapidOCR
from PIL import Image, ImageOps
import numpy as np

SRC = r'E:/Desktop/做题/高数模拟卷/【解析】27张宇四套卷数二.pdf'
engine = RapidOCR()
doc = fitz.open(SRC)
result = {}
for pno in range(len(doc)):
    pix = doc[pno].get_pixmap(matrix=fitz.Matrix(1.8, 1.8), colorspace=fitz.csGRAY, alpha=False)
    im = Image.frombytes('L', (pix.width, pix.height), pix.samples)
    im = ImageOps.autocontrast(im, cutoff=1)
    arr = np.array(im)
    res, _ = engine(arr)
    items = []
    for box, text, score in (res or []):
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        items.append({'t': text, 'x': round(min(xs)), 'y': round(min(ys)),
                      'x1': round(max(xs)), 'y1': round(max(ys)), 's': round(score, 2)})
    result[str(pno + 1)] = items
    title = [i['t'] for i in items if '预测卷' in i['t']]
    nums = sorted({int(m.group(1)) for i in items if '答' in i['t']
                   for m in [re.match(r'\s*(\d{1,2})\s*[\.．、]?\s*答', i['t'])] if m})
    footer = [i['t'] for i in items if '第' in i['t'] and '页' in i['t']]
    print('P%02d | title=%s | qnums=%s | footer=%s' % (
        pno + 1, (title or [''])[0][:38], nums[:26], (footer or [''])[0][:40]))
json.dump(result, open(r'D:/ai code/math-note/tools/_zs4_pdf_ocr.json', 'w', encoding='utf-8'),
          ensure_ascii=False)
