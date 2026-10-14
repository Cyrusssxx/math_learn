#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""仅提取 PDF 书签（目录大纲），输出层级、标题、页码。"""
import io, json, os, sys

PDF = r'E:/Desktop/大观/【合集】大观答案/【合集】大观答案.pdf'

try:
    import fitz
except ImportError:
    print('PyMuPDF 未安装')
    sys.exit(1)

doc = fitz.open(PDF)
print('页数:', doc.page_count)
toc = doc.get_toc(simple=True)   # [[level, title, page], ...]
print('书签条数:', len(toc))
print()
if not toc:
    print('（此书签为空）')
    sys.exit(0)

# 按 level 缩进打印
for lv, title, page in toc:
    pad = '  ' * (lv - 1)
    print(f'{pad}[L{lv}] {title}  →  p{page}')

# 统计
from collections import Counter
cnt = Counter(lv for lv, _, _ in toc)
print()
print('层级分布:', dict(sorted(cnt.items())))
doc.close()
