# -*- coding: utf-8 -*-
import fitz

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

for pno in range(5, 12):
    page = doc[pno]
    text = page.get_text()
    print(f"=== Page {pno+1} ===")
    print(text.strip())
    print("\n" + "="*50 + "\n")
