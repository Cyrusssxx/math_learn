# -*- coding: utf-8 -*-
"""抽查切图：拼版查看题号是否完整、有无页脚残留。"""
import json, os
from PIL import Image, ImageDraw

ROOT = r'D:/ai code/math-note'
d = json.load(open(os.path.join(ROOT, 'pwa/data/mn27_zs4_papers.json'), encoding='utf-8'))
sel = [(1, 1), (1, 9), (1, 17), (1, 21), (2, 11), (2, 22), (3, 20), (4, 14), (4, 22)]
tiles = []
for vol, no in sel:
    q = [q for s in d[vol - 1]['sections'] for q in s['questions'] if q['no'] == no][0]
    paths = [p for p in q['ansImg'] if 'mn27zs4pdf-' in p]
    ims = []
    for p in paths:
        im = Image.open(os.path.join(ROOT, 'pwa', p)).convert('RGB')
        im.thumbnail((430, 620))
        ims.append(im)
    w = max(i.width for i in ims)
    h = sum(i.height for i in ims) + 26 * len(ims)
    tile = Image.new('RGB', (w + 8, h), 'white')
    dr = ImageDraw.Draw(tile)
    y = 0
    for im in ims:
        dr.text((4, y + 4), 'V%d Q%d %s' % (vol, no, os.path.basename(paths[len(ims) - len(ims) + 0])[:4]), fill='red')
        y += 22
        tile.paste(im, (4, y))
        y += im.height + 4
    tiles.append(tile)

cols = 3
maxw = max(t.width for t in tiles)
rows = (len(tiles) + cols - 1) // cols
maxh = max(t.height for t in tiles)
sheet = Image.new('RGB', (cols * maxw, rows * maxh), '#ddd')
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * maxw, (i // cols) * maxh))
out = r'C:/Users/cjx/AppData/Local/Temp/zs4_cuts_check.png'
sheet.save(out)
print(out, sheet.size)
