# -*- coding: utf-8 -*-
"""第二轮补录：裁题面图 + 定位答案图（87 题）→ tools/_zx_add2_list.json"""
import glob, fitz, json, re, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QPDF = glob.glob('E:/Desktop/大观/*大观严选题/*A4紧凑*.pdf')[0]
APDF = glob.glob('E:/Desktop/大观/*大观严选题/*通用答案*.pdf')[0]
qdoc = fitz.open(QPDF)
adoc = fitz.open(APDF)

def strip_pfx(t):
    return re.sub(r'\s+', '', re.sub(r'^\s*\(?[a-z0-9ivx]+\)?\)\s*', '', str(t or '').replace('>>', '').strip(), flags=re.I)).replace('版', '').lower()

zx = json.load(open('tools/_zx_parsed.json', encoding='utf-8'))
by_no = {q['no']: q for q in zx}
targets = json.load(open('tools/_zx_add_round2.json', encoding='utf-8'))
nos = [t['no'] for t in targets]

# 行级页眉
H = json.load(open('tools/_ans_headers2.json', encoding='utf-8'))
all_srcs = {strip_pfx(q['src']) for q in zx}
headers = sorted([(h['page'] - 1, h['y'], h['text']) for h in H if strip_pfx(h['text']) in all_srcs], key=lambda x: (x[0], x[1]))

from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()

def toks(s):
    o = set()
    for m in re.finditer(r'[\u4e00-\u9fff]{2,}', str(s or '')): o.add(m[0])
    for m in re.finditer(r'\d{2,}', str(s or '')): o.add(m[0])
    return o

out = []
for k, no in enumerate(nos):
    q = by_no[no]
    # 1) 题面截图
    page = qdoc[q['page'] - 1]
    blocks = sorted([b for b in page.get_text('blocks') if b[4].strip()], key=lambda x: (round(x[1], 1), x[0]))
    y0 = y1 = None
    tag = '#%03d' % no
    for i, b in enumerate(blocks):
        if b[4].strip().startswith(tag):
            y0 = b[3]
            for b2 in blocks[i + 1:]:
                if b2[4].strip().startswith('#'):
                    y1 = b2[1]; break
            break
    qimg = None
    if y0 is not None:
        clip = fitz.Rect(40, y0 + 2, page.rect.width - 40, (y1 or page.rect.height - 40) - 4)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=clip)
        qimg = f'pwa/data/img/zx_q/zx{no:03d}.png'
        pix.save(qimg)
    # 题 OCR（用于答案首图判别）
    qocr = ''
    if qimg:
        import numpy as np
        pix2 = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
        arr = np.frombuffer(pix2.samples, dtype=np.uint8).reshape(pix2.height, pix2.width, pix2.n)
        if pix2.n == 4: arr = arr[:, :, :3]
        res, _ = ocr(arr)
        qocr = ' '.join(r[1] for r in res) if res else ''
    # 2) 答案定位
    hdr = q.get('_hdr')
    aimgs = []
    if hdr and y0 is not None:
        pi0, yy = hdr['page'] - 1, hdr['y']
        nxt = None
        for ht in headers:
            if (ht[0], ht[1]) > (pi0, yy): nxt = (ht[0], ht[1]); break
        pages = [pi0] if (nxt is None or nxt[0] == pi0) else list(range(pi0, nxt[0] + 1))
        rects = []
        for pj in pages:
            p = adoc[pj]
            for img in p.get_images(full=True):
                for rr in p.get_image_rects(img[0]):
                    if rr.width < 40 or rr.height < 14: continue
                    if pj == pi0 and rr.y0 <= yy + 2: continue
                    if nxt and pj == nxt[0] and rr.y0 >= nxt[1] - 2: continue
                    rects.append((pj, rr))
        rects.sort(key=lambda x: (x[0], x[1].y0, x[1].x0))
        qtoks = toks(qocr)
        for k2, (pj, rr) in enumerate(rects):
            p = adoc[pj]
            clip2 = fitz.Rect(rr.x0 - 2, rr.y0 - 2, rr.x1 + 2, rr.y1 + 2)
            pix3 = p.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip2)
            import numpy as np
            arr = np.frombuffer(pix3.samples, dtype=np.uint8).reshape(pix3.height, pix3.width, pix3.n)[:, :, :3]
            jpg = f'pwa/data/img/zx_a/zx{no:03d}_{len(aimgs)}.jpg'
            Image.fromarray(arr).convert('L').save(jpg, 'JPEG', quality=82, optimize=True)
            # OCR 判别：只有当这是第 0 张且后面还有图时才允许按题面跳过
            skip = False
            if k2 == 0 and len(rects) > 1:
                import numpy as np
                arr = np.frombuffer(pix3.samples, dtype=np.uint8).reshape(pix3.height, pix3.width, pix3.n)
                if pix3.n == 4: arr = arr[:, :, :3]
                res, _ = ocr(arr)
                t = ' '.join(r[1] for r in res) if res else ''
                tk = toks(t)
                inter = len(qtoks & tk)
                if qtoks and tk and inter / max(1, min(len(qtoks), len(tk))) >= 0.5:
                    skip = True
                    os.remove(jpg)
            if not skip:
                aimgs.append(jpg)
            if len(aimgs) >= 4: break
    out.append({'no': no, 'cat': q['cat'], 'src': q['src'], 'page': q['page'],
                'qimg': qimg, 'aimgs': aimgs, 'hdr': (q.get('_hdr') or {}).get('text', '')})
    print(f"#{no:03d} 题面{'✓' if qimg else '✗'} 答案图{len(aimgs)}")

json.dump(out, open('tools/_zx_add2_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ok = sum(1 for r in out if r['qimg'] and r['aimgs'])
print(f'\n完成：完整 {ok} / {len(out)}')
