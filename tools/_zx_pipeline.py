# -*- coding: utf-8 -*-
"""
线代臻选题补题流水线（第一阶段：对齐 + 截图 + OCR 质检）
输入: tools/_zx_parsed.json(355题) tools/_zx_final_miss.json(117候选)
输出: tools/_zx_add_list.json(确认缺失+截图+答案图) pwa/data/img/zx_q|zx_a/*.png
用法: D:/python/python.exe tools/_zx_pipeline.py [--limit N]
"""
import glob, fitz, json, re, os, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QPDF = glob.glob('E:/Desktop/大观/*大观严选题/*A4紧凑*.pdf')[0]
APDF = glob.glob('E:/Desktop/大观/*大观严选题/*通用答案*.pdf')[0]

def nrm(s):
    return re.sub(r'\s+', '', str(s or '')).replace('版', '').lower()

def toks(s):
    out = []
    for m in re.finditer(r'[\u4e00-\u9fff]{2,}', str(s or '')): out.append(m[0])
    for m in re.finditer(r'\d{2,}', str(s or '')): out.append(m[0])
    return set(out)

# ---------- 1. 载入 ----------
zx = json.load(open('tools/_zx_parsed.json', encoding='utf-8'))
cand = json.load(open('tools/_zx_final_miss.json', encoding='utf-8'))
cand_nos = {q['no'] for q in cand if not (q.get('_best', 0) >= 0.45 and q.get('_dist', 0) >= 2)}
targets = [q for q in zx if q['no'] in cand_nos]
print(f'确认缺失 {len(targets)} 题（候选 {len(cand_nos)}）')

# ---------- 2. 答案册页眉 → 题目页眉序列 ----------
adoc = fitz.open(APDF)
headers = []   # (page_idx, y, text)
for pi in range(12, len(adoc)):
    for b in adoc[pi].get_text('blocks'):
        for line in b[4].split('\n'):
            line = line.strip()
            if line.endswith('>>') and len(line) > 3:
                headers.append((pi, b[1], line))
# 只保留「与某题 source 精确相等」的页眉（排除章/节/考点上下文页眉）
src_set = {}
for q in zx:
    src_set.setdefault(nrm(q['src']), []).append(q)
qheaders = []  # (page_idx, y, text, src_norm)
for (pi, y, t) in headers:
    s = nrm(re.sub(r'^[a-z]\)\s*', '', t).rstrip('>').strip())
    if s in src_set:
        qheaders.append((pi, y, t, s))
print(f'题目页眉 {len(qheaders)} 个 / 题目 {len(zx)} 题')

# ---------- 3. 组内顺序对齐 ----------
# 每个来源组：第 k 题 ↔ 该来源第 k 个页眉
hdr_by_src = {}
for h in qheaders:
    hdr_by_src.setdefault(h[3], []).append(h)
q_by_src = {}
for q in zx:
    q_by_src.setdefault(nrm(q['src']), []).append(q)
align = {}   # question no -> header
warn = []
for s, qs in q_by_src.items():
    hs = hdr_by_src.get(s, [])
    if len(hs) < len(qs):
        warn.append(f'来源[{s[:20]}] 题{len(qs)} > 页眉{len(hs)}')
    for i, q in enumerate(qs):
        if i < len(hs):
            align[q['no']] = hs[i]
        else:
            align[q['no']] = hs[-1] if hs else None   # 多题共用最后一页眉
print(f'对齐完成；警告 {len(warn)} 条')
for w in warn[:8]: print('  ⚠', w)

# 每题答案区域 = 从其页眉起，到下一个「题目页眉」止的所有扫描图
hdr_pos = sorted([(h[0], h[1]) for h in qheaders])
def answer_images(no):
    h = align.get(no)
    if not h: return []
    pi, y, _, _ = h
    # 下一个题目页眉位置
    nxt = None
    for (pj, yj) in hdr_pos:
        if (pj, yj) > (pi, y):
            nxt = (pj, yj); break
    imgs = []
    pages = [pi] if (nxt is None or nxt[0] == pi) else list(range(pi, nxt[0] + 1))
    for pj in pages:
        p = adoc[pj]
        for img in p.get_images(full=True):
            for r in p.get_image_rects(img[0]):
                if r.width < 30 or r.height < 12: continue
                if pj == pi and r.y0 <= y: continue          # 页眉之前的不算
                if nxt and pj == nxt[0] and r.y0 >= nxt[1]: continue  # 到下一题页眉为止
                imgs.append((pj, r))
    return imgs

# ---------- 4. 题面截图 ----------
qdoc = fitz.open(QPDF)
os.makedirs('pwa/data/img/zx_q', exist_ok=True)
os.makedirs('pwa/data/img/zx_a', exist_ok=True)

def crop_question(q):
    page = qdoc[q['page'] - 1]
    blocks = sorted([b for b in page.get_text('blocks') if b[4].strip()], key=lambda x: (round(x[1], 1), x[0]))
    y0 = y1 = None
    tag = '#%03d' % q['no']
    for i, b in enumerate(blocks):
        if b[4].strip().startswith(tag):
            y0 = b[3]
            for b2 in blocks[i + 1:]:
                if b2[4].strip().startswith('#'):
                    y1 = b2[1]; break
            break
    if y0 is None: return None
    clip = fitz.Rect(40, y0 + 2, page.rect.width - 40, (y1 or page.rect.height - 40) - 4)
    pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=clip)
    fp = f'pwa/data/img/zx_q/zx{q["no"]:03d}.png'
    pix.save(fp)
    return fp

# ---------- 5. 执行（仅 targets） ----------
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
out = []
for q in targets:
    no = q['no']
    qimg = crop_question(q)
    # 题 OCR（用于答案首图是否为题面的比对 & 质检）
    qocr = ''
    if qimg:
        res, _ = ocr(qimg)
        qocr = ' '.join(r[1] for r in res) if res else ''
    # 答案图
    afiles = []
    imgs = answer_images(no)
    for k, (pj, r) in enumerate(imgs):
        p = adoc[pj]
        clip = fitz.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2)
        pix = p.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
        fp = f'pwa/data/img/zx_a/zx{no:03d}_{k}.png'
        pix.save(fp)
        afiles.append(fp)
    out.append({'no': no, 'cat': q['cat'], 'src': q['src'], 'page': q['page'],
                'qimg': qimg, 'qocr': qocr[:300], 'aimgs': afiles,
                'hdr': (align.get(no) or (None, None, '', ''))[2]})
json.dump(out, open('tools/_zx_add_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'完成 {len(out)} 题；输出 tools/_zx_add_list.json')
