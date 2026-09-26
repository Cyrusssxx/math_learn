# -*- coding: utf-8 -*-
import fitz
import re, json, io

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

# 打印 Page 5 的目录文本
p5_text = doc[4].get_text()
print("=== Page 5 考点地图 ===")
print(p5_text[:1500])

# 看看 Page 5 后面有没有
p4_text = doc[3].get_text()
print("=== Page 4 35天打卡表 ===")
print(p4_text[:1500])
