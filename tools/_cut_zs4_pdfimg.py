# -*- coding: utf-8 -*-
"""从官方《【解析】27张宇四套卷数二.pdf》按题号切答案原图，追加到 mn27_zs4_papers.json 的 ansImg。

锚点来自 tools/_zs4_pdf_qmap.json（RapidOCR），3 个漏检题号人工补齐。
只追加 ansImg，不改动题干/答案/思路等任何已有字段。
"""
import fitz, json, os
from PIL import Image

ROOT = r'D:/ai code/math-note'
SRC = r'E:/Desktop/做题/高数模拟卷/【解析】27张宇四套卷数二.pdf'
OUT_DIR = os.path.join(ROOT, 'pwa/data/img/zx_site')
DATA = os.path.join(ROOT, 'pwa/data/mn27_zs4_papers.json')
QMAP = json.load(open(os.path.join(ROOT, 'tools/_zs4_pdf_qmap.json'), encoding='utf-8'))

# 人工补 OCR 漏检：(页, y)
FIX = {1: {21: (12, 1118)}, 2: {22: (27, 397)}, 4: {14: (45, 1103)}}

# OCR 在 1.8x 坐标系；输出用 2.2x 渲染，坐标按此比例放大
OCR_SCALE = 1.8
RENDER_SCALE = 2.2
F = RENDER_SCALE / OCR_SCALE
X0, X1 = 55, 865          # 1.8x 坐标：正文左右边界
Y_TOP, Y_BOT = 100, 1218  # 1.8x 坐标：页眉/页脚之内

VOL_PAGES = {1: range(3, 15), 2: range(15, 28), 3: range(28, 41), 4: range(41, 53)}

def anchors(vol):
    src = QMAP[str(vol)]
    a = {}
    for no in range(1, 23):
        hits = src.get(str(no)) or []
        if hits:
            a[no] = (int(hits[0][0]), int(hits[0][1]))
    for no, pos in FIX.get(vol, {}).items():
        a[no] = pos
    missing = [n for n in range(1, 23) if n not in a]
    assert not missing, ('vol %d missing anchors' % vol, missing)
    return a

def segments(a, no):
    """返回 [(page, y0, y1)]，y 均为 1.8x 坐标。"""
    p0, y0 = a[no]
    if no < 22:
        p1, y1 = a[no + 1]
    else:
        p1, y1 = p0, Y_BOT
    segs = []
    if p0 == p1:
        segs.append((p0, max(Y_TOP, y0 - 12), min(Y_BOT, y1 - 8)))
    else:
        segs.append((p0, max(Y_TOP, y0 - 12), Y_BOT))
        for p in range(p0 + 1, p1):
            segs.append((p, Y_TOP, Y_BOT))
        segs.append((p1, Y_TOP, min(Y_BOT, y1 - 8)))
    return [(p, y0, y1) for p, y0, y1 in segs if y1 - y0 > 12]

doc = fitz.open(SRC)
d = json.load(open(DATA, encoding='utf-8'))
# 幂等：重跑时先剥掉本脚本生成的 PDF 图引用，保留站点原图（mn27-zs4-*）
for _pp in d:
    for _s in _pp['sections']:
        for _q in _s['questions']:
            _q['ansImg'] = [p for p in (_q.get('ansImg') or []) if 'mn27zs4pdf-' not in p]
report = []
total_new = 0
for vol in (1, 2, 3, 4):
    a = anchors(vol)
    pp = d[vol - 1]
    assert pp['id'] == 'mn27-zs4-%d' % vol, pp['id']
    cache = {}
    for s in pp['sections']:
        for q in s['questions']:
            no = q['no']
            q.setdefault('ansImg', [])
            before = list(q['ansImg'])  # 站点原图，必须在 PDF 图之前
            for k, (p, ya, yb) in enumerate(segments(a, no)):
                if p not in cache:
                    pix = doc[p - 1].get_pixmap(matrix=fitz.Matrix(RENDER_SCALE, RENDER_SCALE),
                                                colorspace=fitz.csGRAY, alpha=False)
                    cache[p] = Image.frombytes('L', (pix.width, pix.height), pix.samples)
                im = cache[p].crop((int(X0 * F), int(ya * F), int(X1 * F), int(yb * F)))
                name = 'mn27zs4pdf-%d-%d_%d.png' % (vol, no, k)
                path = os.path.join(OUT_DIR, name)
                im.save(path, optimize=True)
                rel = 'data/img/zx_site/' + name
                assert rel not in q['ansImg'], rel
                q['ansImg'].append(rel)
                total_new += 1
            report.append((vol, no, len(q['ansImg']) - len(before), before, q['ansImg']))

json.dump(d, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False)
print('切图完成：新增 %d 张，合计 %d 题' % (total_new, len(report)))
for vol in (1, 2, 3, 4):
    rows = [r for r in report if r[0] == vol]
    print('卷%d: %d 题 / %d 张 / 每题目数 %s' %
          (vol, len(rows), sum(r[2] for r in rows), [r[2] for r in rows]))
print('已有站点原图保留：', [(v, n, b) for v, n, c, b, af in report if b])
