# -*- coding: utf-8 -*-
"""补裁 24 道漏补的甄选题（题面图 + 答案图）。"""
import fitz, json, glob, re, os, io
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

QPDF = glob.glob('E:/Desktop/大观/*大观严选题/*A4紧凑*.pdf')[0]
APDF = glob.glob('E:/Desktop/大观/*大观严选题/*通用答案*.pdf')[0]
qdoc, adoc = fitz.open(QPDF), fitz.open(APDF)
ocr = RapidOCR()

zx = json.load(io.open('tools/_zx_parsed.json', encoding='utf-8'))
by_no = {q['no']: q for q in zx}
nos = json.load(io.open('tools/_zx_missing_img.json', encoding='utf-8'))

def strip_pfx(t):
    return re.sub(r'^[a-z]\)\s*', '', str(t or '').strip())

H = json.load(io.open('tools/_ans_headers2.json', encoding='utf-8'))
all_srcs = {strip_pfx(q['src']) for q in zx}
headers = sorted([(h['page'] - 1, h['y'], h['text']) for h in H if strip_pfx(h['text']) in all_srcs],
                 key=lambda x: (x[0], x[1]))

def toks(s):
    o = set()
    for m in re.finditer(r'[\u4e00-\u9fff]{2,}', str(s or '')): o.add(m[0])
    for m in re.finditer(r'\d{2,}', str(s or '')): o.add(m[0])
    return o

out = []
for no in nos:
    q = by_no[no]
    # 1) 题面图
    page = qdoc[q['page'] - 1]
    blocks = sorted([b for b in page.get_text('blocks') if b[4].strip()], key=lambda x: (round(x[1], 1), x[0]))
    y0 = y1 = None
    tag = '#%03d' % no
    for i, b in enumerate(blocks):
        if b[4].strip().startswith(tag):
            y0 = b[3]
            for b2 in blocks[i + 1:]:
                if b2[4].strip().startswith('#'): y1 = b2[1]; break
            break
    qimg = None
    if y0 is not None:
        clip = fitz.Rect(40, y0 + 2, page.rect.width - 40, (y1 or page.rect.height - 40) - 4)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=clip)
        qimg = 'pwa/data/img/zx_q/zx%03d.png' % no
        pix.save(qimg)
    qocr = ''
    if qimg:
        pix2 = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
        arr = np.frombuffer(pix2.samples, dtype=np.uint8).reshape(pix2.height, pix2.width, pix2.n)
        if pix2.n == 4: arr = arr[:, :, :3]
        res, _ = ocr(arr)
        qocr = ' '.join(r[1] for r in res) if res else ''
    # 2) 答案图
    hdr = q.get('_hdr'); aimgs = []
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
            a = np.frombuffer(pix3.samples, dtype=np.uint8).reshape(pix3.height, pix3.width, pix3.n)[:, :, :3]
            jpg = 'pwa/data/img/zx_a/zx%03d_%d.jpg' % (no, len(aimgs))
            Image.fromarray(a).convert('L').save(jpg, 'JPEG', quality=82, optimize=True)
            skip = False
            if k2 == 0 and len(rects) > 1:
                arr = np.frombuffer(pix3.samples, dtype=np.uint8).reshape(pix3.height, pix3.width, pix3.n)
                if pix3.n == 4: arr = arr[:, :, :3]
                res, _ = ocr(arr)
                t = ' '.join(r[1] for r in res) if res else ''
                tk = toks(t)
                if qtoks and tk and len(qtoks & tk) / max(1, min(len(qtoks), len(tk))) >= 0.5:
                    skip = True; os.remove(jpg)
            if not skip: aimgs.append(jpg)
            if len(aimgs) >= 4: break
    out.append({'no': no, 'cat': q['cat'], 'src': q['src'], 'page': q['page'],
                'qimg': qimg, 'aimgs': aimgs, 'hdr': (hdr or {}).get('text', '')})
    print('#%03d 题面%s 答案图%d' % (no, '✓' if qimg else '✗', len(aimgs)))

json.dump(out, io.open('tools/_zx_missing_cropped.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n完成', sum(1 for r in out if r['qimg'] and r['aimgs']), '/', len(nos))
