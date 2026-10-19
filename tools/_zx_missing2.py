# -*- coding: utf-8 -*-
"""彻底核查：把 254 道「未补录」的臻选题截图 OCR，与核心题库线代逐题比对，找出真正缺失的题。
输出 tools/_zx_missing2.json
"""
import glob, fitz, json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QPDF = glob.glob('E:/Desktop/大观/*大观严选题/*A4紧凑*.pdf')[0]
qdoc = fitz.open(QPDF)
zx = json.load(open('tools/_zx_parsed.json', encoding='utf-8'))
core = json.load(open('pwa/data/core_bank.json', encoding='utf-8'))
rep = json.load(open('tools/_zx_insert_report.json', encoding='utf-8'))
added = {r['zx'] for r in rep['inserted']} | {103, 112, 153, 263, 344}
LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型']
coreQ = [q for s in core[0]['sections'] if s['title'] in LA for q in s['questions']]

def toks(s):
    o = set()
    for m in re.finditer(r'[\u4e00-\u9fff]{2,}', str(s or '')): o.add(m[0])
    for m in re.finditer(r'\d{2,}', str(s or '')): o.add(m[0])
    return o

# IDF（在核心题库线代上统计）
df = {}
for q in coreQ:
    for t in toks(q.get('stem', '')): df[t] = df.get(t, 0) + 1
import math
def w(t): return 1 / math.log(2 + max(0, df.get(t, 0)))
def sim(pt, ct):
    cs = set(ct)
    tw = iw = 0.0
    for t in pt:
        ww = w(t); tw += ww
        if t in cs: iw += ww
    return iw / tw if tw else 0.0

from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()

def crop(q):
    page = qdoc[q['page'] - 1]
    blocks = sorted([b for b in page.get_text('blocks') if b[4].strip()], key=lambda x: (round(x[1], 1), x[0]))
    tag = '#%03d' % q['no']
    y0 = y1 = None
    for i, b in enumerate(blocks):
        if b[4].strip().startswith(tag):
            y0 = b[3]
            for b2 in blocks[i + 1:]:
                if b2[4].strip().startswith('#'):
                    y1 = b2[1]; break
            break
    if y0 is None: return None
    clip = fitz.Rect(40, y0 + 2, page.rect.width - 40, (y1 or page.rect.height - 40) - 4)
    return page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)

todo = [q for q in zx if q['no'] not in added]
print('待核查:', len(todo), '题')
out = []
for i, q in enumerate(todo):
    pix = crop(q)
    if pix is None:
        out.append({'no': q['no'], 'cat': q['cat'], 'src': q['src'], 'ocr': '', 'best': 0, 'cand': None, 'missing': True})
        continue
    import numpy as np
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4: arr = arr[:, :, :3]
    res, _ = ocr(arr)
    txt = ' '.join(r[1] for r in res) if res else ''
    pt = toks(txt)
    best, bc = 0.0, None
    for c in coreQ:
        sc = sim(pt, toks(c.get('stem', '')))
        if sc > best: best, bc = sc, c['no']
    out.append({'no': q['no'], 'cat': q['cat'], 'src': q['src'], 'ocr': txt[:120],
                'best': round(best, 2), 'cand': bc, 'missing': best < 0.5})
    if (i + 1) % 20 == 0: print('  进度', i + 1, '/', len(todo), flush=True)

json.dump(out, open('tools/_zx_missing2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
miss = [r for r in out if r['missing']]
print('核查完成：疑似缺失', len(miss), '题 /', len(out))
for r in miss:
    print(f"  zx#{r['no']:>3}  {r['cat'].split('→')[-1].strip():<16} {r['src'][:26]:<28} best={r['best']}")
