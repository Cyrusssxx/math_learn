# -*- coding: utf-8 -*-
import fitz # PyMuPDF
import json, io, os, sys

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

print(f"总页数: {len(doc)}")
for i in range(min(5, len(doc))):
    page = doc[i]
    text = page.get_text()
    print(f"--- Page {i+1} ---")
    print(text[:300].strip())
    print("\n")
