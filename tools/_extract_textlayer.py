# -*- coding: utf-8 -*-
"""抽取【A4紧凑】数二大观严选题做题本.pdf 的文字层（该 PDF 非扫描件，含文本）。

产出：
  tools/_yancai_textlayer.json  {page: 原始文本}
  tools/_yancai_textlayer.txt   人类可读版
"""
import json, io, re
import pymupdf

PDF = r'D:/ai code/【A4紧凑】数二大观严选题做题本.pdf'
OUT_JSON = 'D:/ai code/math-note/tools/_yancai_textlayer.json'
OUT_TXT = 'D:/ai code/math-note/tools/_yancai_textlayer.txt'

doc = pymupdf.open(PDF)
data = {}
lines = []
for i in range(doc.page_count):
    t = doc[i].get_text()
    data[str(i + 1)] = t
    lines.append('\n\n########## PAGE %d ##########\n' % (i + 1))
    lines.append(t.rstrip())

with io.open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
with io.open(OUT_TXT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

tot = sum(len(v) for v in data.values())
print('总页数 %d | 文字层总字符 %d' % (doc.page_count, tot))
empty = [p for p, v in data.items() if len(v.strip()) < 50]
print('文字层几乎为空的页:', empty)
print('已写', OUT_JSON)
print('已写', OUT_TXT)
