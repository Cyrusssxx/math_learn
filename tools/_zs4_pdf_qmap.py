# -*- coding: utf-8 -*-
"""从 OCR 结果提取每卷每题的题号锚点（页 + y）。"""
import json, re
D = json.load(open(r'D:/ai code/math-note/tools/_zs4_pdf_ocr.json', encoding='utf-8'))
VOL_PAGES = {1: range(3, 15), 2: range(15, 28), 3: range(28, 41), 4: range(41, 53)}
PAT = re.compile(r'^\s*(\d{1,2})\s*[.．、]\s*(答|解|证|应填|填)')

out = {}
for vol, pages in VOL_PAGES.items():
    hits = {}
    for p in pages:
        for it in D[str(p)]:
            m = PAT.match(it['t'])
            if m and it['x'] < 165:
                no = int(m.group(1))
                hits.setdefault(no, []).append((p, it['y'], it['t'][:48]))
    out[vol] = hits
    print('=== 卷%d ===' % vol)
    for no in range(1, 23):
        h = hits.get(no, [])
        print('  Q%-2d %s' % (no, ' | '.join('P%d@%d %s' % (p, y, t) for p, y, t in h) or 'MISSING'))
json.dump({str(k): {str(n): v for n, v in h.items()} for k, h in out.items()},
          open(r'D:/ai code/math-note/tools/_zs4_pdf_qmap.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
