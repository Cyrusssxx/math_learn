# -*- coding: utf-8 -*-
"""阶段2：为 101 道缺失题裁答案图（页眉→下一题页眉之间的扫描图），OCR 质检。
题面图（OCR 与题干吻合的首图）不计入答案图。"""
import glob, fitz, json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APDF = glob.glob('E:/Desktop/大观/*大观严选题/*通用答案*.pdf')[0]

def strip_pfx(t):
    return re.sub(r'\s+', '', re.sub(r'^\s*\(?[a-z0-9ivx]+\)?\)\s*', '', str(t or '').replace('>>', '').strip(), flags=re.I)).replace('版', '').lower()

def toks(s):
    out = set()
    for m in re.finditer(r'[\u4e00-\u9fff]{2,}', str(s or '')): out.add(m[0])
    for m in re.finditer(r'\d{2,}', str(s or '')): out.add(m[0])
    return out

zx = json.load(open('tools/_zx_parsed.json', encoding='utf-8'))
add = json.load(open('tools/_zx_add_list.json', encoding='utf-8'))
by_no = {q['no']: q for q in zx}

# 全部题目页眉（行级坐标 + 前缀剥离）
adoc = fitz.open(APDF)
headers = []
all_srcs = {strip_pfx(q['src']) for q in zx}
for h in json.load(open('tools/_ans_headers2.json', encoding='utf-8')):
    if strip_pfx(h['text']) in all_srcs:
        headers.append((h['page'] - 1, h['y'], h['text']))
headers.sort(key=lambda x: (x[0], x[1]))
print('题目页眉总数:', len(headers))
# 模糊补齐：无精确页眉的题，用「来源片段互含」找页眉
def fuzzy_hdr(q):
    s = strip_pfx(q['src'])
    cands = [h for h in json.load(open('tools/_ans_headers2.json', encoding='utf-8'))
             if s and (s in strip_pfx(h['text']) or strip_pfx(h['text']) in s)]
    return cands

from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()

results = []
for item in add:
    no = item['no']
    q = by_no[no]
    hdr = q.get('_hdr')
    if not hdr:
        cands = fuzzy_hdr(q)
        if cands:
            hdr = {'page': cands[0]['page'], 'y': cands[0]['y'], 'text': cands[0]['text']}
            item['fuzzy'] = True
    if not hdr:
        item['aimgs'] = []
        item['flag'] = '无页眉'
        results.append(item); continue
    pi0, y0 = hdr['page'] - 1, hdr['y']
    # 下一题页眉
    nxt = None
    for htuple in headers:
        pj, yj = htuple[0], htuple[1]
        if (pj, yj) > (pi0, y0): nxt = (pj, yj); break
    pages = [pi0] if (nxt is None or nxt[0] == pi0) else list(range(pi0, nxt[0] + 1))
    # 收集区域内的扫描图
    rects = []
    for pj in pages:
        p = adoc[pj]
        for img in p.get_images(full=True):
            for r in p.get_image_rects(img[0]):
                if r.width < 40 or r.height < 14: continue
                if pj == pi0 and r.y0 <= y0 + 2: continue
                if nxt and pj == nxt[0] and r.y0 >= nxt[1] - 2: continue
                rects.append((pj, r))
    rects.sort(key=lambda x: (x[0], x[1].y0, x[1].x0))
    # OCR 识别：跳过题面首图（与题干 OCR 吻合者）
    qtoks = toks(item.get('qocr', ''))
    aimgs, flags = [], []
    qt = qtoks
    for k, (pj, r) in enumerate(rects):
        p = adoc[pj]
        clip = fitz.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2)
        pix = p.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
        fp = f'pwa/data/img/zx_a/zx{no:03d}_{len(aimgs)}.png'
        pix.save(fp)
        res, _ = ocr(fp)
        t = ' '.join(x[1] for x in res) if res else ''
        tk = toks(t)
        if tk:
            inter = len(qtoks & tk)
            is_stem = len(qtoks) > 0 and inter / max(1, min(len(qtoks), len(tk))) >= 0.5
        else:
            is_stem = (r.height < 60)   # 无文字的矮图视为题面
        if k == 0 and is_stem:
            continue                     # 首图=题面，跳过
        aimgs.append(fp)
        if len(aimgs) >= 4: break        # 最多 4 张
    item['aimgs'] = aimgs
    item['flag'] = 'OK' if aimgs else '无答案图'
    if not aimgs: flags and None
    results.append(item)
    print(f"#{no:03d} {item['flag']} 答案图{len(aimgs)}张")

json.dump(results, open('tools/_zx_add_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ok = sum(1 for r in results if r['flag'] == 'OK')
print(f'\n完成：OK {ok} / {len(results)}')
