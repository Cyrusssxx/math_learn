# -*- coding: utf-8 -*-
"""裁掉臻选题面图底部的大片空白（页内最后一题会一路裁到页底）。
只裁底部、不动顶部和左右；保留 12px 呼吸边距；>25% 空白才处理。"""
import os, io, json
import numpy as np
from PIL import Image

DATA = 'pwa/data/core_bank.json'
cb = json.load(io.open(DATA, encoding='utf-8'))
LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型']
PAD = 12
TH = 0.25

report = []
for s in cb[0]['sections']:
    if s['title'] not in LA: continue
    for q in s['questions']:
        img = q.get('img')
        if not img: continue
        p = 'pwa/' + img
        if not os.path.exists(p): continue
        im = Image.open(p)
        if im.mode != 'L': im = im.convert('L')
        a = np.array(im)
        if a.size == 0: continue
        ink = (a < 245).sum(axis=1)
        nz = np.nonzero(ink)[0]
        if len(nz) == 0: continue
        last = int(nz[-1])
        H = a.shape[0]
        tail = H - 1 - last
        if tail / H <= TH: continue
        newH = min(H, last + 1 + PAD)
        if newH >= H: continue
        box = (0, 0, a.shape[1], newH)
        im2 = im.crop(box)
        im2.save(p, 'PNG', optimize=True)
        report.append({'no': q['no'], 'zx': q.get('srcOrder'), 'sec': s['title'],
                       'before': [a.shape[1], H], 'after': [a.shape[1], newH],
                       'savedPx': H - newH, 'kbBefore': os.path.getsize(p)})

print('裁剪题面图', len(report), '张')
print('%-7s | %-6s | %-16s | %-14s | %-10s | %s' % ('题号','臻选#','章','原 宽x高','裁掉px','节省'))
tot = 0
for r in report:
    tot += r['savedPx']
    print('%-7d | #%-5d | %-16s | %dx%d | %-10d | %.0f%%' % (
        r['no'], r['zx'] or 0, r['sec'], r['before'][0], r['before'][1], r['savedPx'],
        r['savedPx'] / r['before'][1] * 100))
print('\n合计裁掉 %d px 高度' % tot)
