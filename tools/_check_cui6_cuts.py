# -*- coding: utf-8 -*-
"""崔6切图抽检拼版。"""
import fitz, json, os
from PIL import Image, ImageDraw

DATA = r'D:/ai code/math-note/pwa/data/mn27_cui6_papers.json'
OUT = r'C:/Users/cjx/AppData/Local/Temp/cui6_cuts_check.png'
d = json.load(open(DATA, encoding='utf-8'))
checks = [(1, 3), (1, 21), (2, 22), (4, 14), (5, 8), (5, 10), (5, 22)]
tiles = []
for vol, no in checks:
    q = [q for s in d[vol-1]['sections'] for q in s['questions'] if q['no'] == no][0]
    ims = [Image.open(os.path.join(r'D:/ai code/math-note/pwa', p)).convert('RGB')
           for p in q['ansImg']]
    # 缩小到统一宽 380
    thumbs = []
    for im in ims:
        w = 380
        h = max(30, int(im.height * w / im.width))
        thumbs.append(im.resize((w, min(h, 520))))
    tile = Image.new('RGB', (390, sum(t.height for t in thumbs) + 30), '#ffffff')
    dr = ImageDraw.Draw(tile)
    dr.text((5, 4), f'V{vol} Q{no} ({len(ims)} seg)', fill='#cc0000')
    y = 22
    for t in thumbs:
        tile.paste(t, (5, y)); y += t.height + 2
    tiles.append(tile)

W = 390 * len(tiles)
H = max(t.height for t in tiles)
canvas = Image.new('RGB', (W, H), '#dddddd')
for i, t in enumerate(tiles):
    canvas.paste(t, (i * 390, 0))
canvas.save(OUT)
print('saved', OUT, canvas.size)
