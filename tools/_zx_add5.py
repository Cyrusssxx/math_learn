# -*- coding: utf-8 -*-
"""补录剩余 5 题：#103 #112 #153 #263 #344
#103 答案图被「首图=题面」误判剔除；其余 4 题答案册用 🐙 代指张宇/经典题写法不同。
输出 pwa/data/img/zx_a/*.jpg + tools/_zx_add5.json
"""
import glob, fitz, json, re, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APDF = glob.glob('E:/Desktop/大观/*大观严选题/*通用答案*.pdf')[0]
adoc = fitz.open(APDF)
H = json.load(open('tools/_ans_headers2.json', encoding='utf-8'))

# 手工指定的答案页眉（page 1-based, y）
TARGET = {
    103: {'page': 85,  'y': 455.7},
    112: {'page': 91,  'y': 750.6},
    153: {'page': 126, 'y': 283.3},
    263: {'page': 229, 'y': 408.1},
    344: {'page': 316, 'y': 517.3},
}
# 全部页眉位置（行级），用于截断到下一题
hpos = sorted({(h['page'], h['y']) for h in H})

out = {}
for no, t in TARGET.items():
    pi0 = t['page'] - 1
    y0 = t['y']
    nxt = None
    for (pj, yj) in hpos:
        if (pj, yj) > (t['page'], y0):
            nxt = (pj - 1, yj); break
    pages = [pi0] if (nxt is None or nxt[0] == pi0) else list(range(pi0, nxt[0] + 1))
    rects = []
    for pj in pages:
        p = adoc[pj]
        for img in p.get_images(full=True):
            for r in p.get_image_rects(img[0]):
                if r.width < 40 or r.height < 14: continue
                if pj == pi0 and r.y0 <= y0 + 2: continue
                if nxt and pj == nxt[0] and r.y0 >= nxt[1] - 2: continue
                rects.append((pj, r))
    rects.sort(key=lambda x: (x[0], x[1].y0))
    files = []
    for k, (pj, r) in enumerate(rects):
        p = adoc[pj]
        clip = fitz.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2)
        pix = p.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
        png = f'pwa/data/img/zx_a/zx{no:03d}_{k}.png'
        pix.save(png)
        jpg = png[:-4] + '.jpg'
        Image.open(png).convert('L').save(jpg, 'JPEG', quality=82, optimize=True)
        os.remove(png)
        files.append(jpg)
    out[no] = files
    print(f'#{no}: {len(files)} 张 → {[os.path.basename(f) for f in files]}')

json.dump(out, open('tools/_zx_add5.json', 'w', encoding='utf-8'), ensure_ascii=False)
