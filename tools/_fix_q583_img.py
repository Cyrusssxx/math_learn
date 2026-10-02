# -*- coding: utf-8 -*-
"""题 583（2020 数一）：答案替换为用户提供的原书解析截图；
   同步 PRECACHE；并扫描全库类似问题（答案重复标记 / 解析引用原书图）"""
import json, io, os, shutil, re
import pymupdf as fitz

SRC_IMG = 'C:/Users/cjx/.workbuddy/clipboard-images/clipboard-2026-10-02T05-28-55-474Z-c1f7b873.png'
DST_IMG = 'pwa/data/img/core_fig/no583.png'
CORE = 'pwa/data/core_bank.json'
SW = 'pwa/sw.js'

# ---------- 1. 图片落地（检查尺寸，必要时压缩到合适宽度） ----------
os.makedirs('pwa/data/img/core_fig', exist_ok=True)
pix = fitz.Pixmap(SRC_IMG)
print(f'原图: {pix.width}x{pix.height}, {os.path.getsize(SRC_IMG) / 1024:.0f} KB')
if pix.width > 1400:                      # 过宽则等比缩小，控制体积
    scale = 1400 / pix.width
    pix = fitz.Pixmap(pix, 0)
    pix.shrink(round(1 / scale) if scale < 0.5 else 1)
pix.save(DST_IMG)
print(f'已保存: {DST_IMG} ({os.path.getsize(DST_IMG) / 1024:.0f} KB)')

# ---------- 2. 修改 core_bank：挂图 + 答案替换 ----------
with io.open(CORE, encoding='utf-8') as f:
    core = json.load(f)

hit = None
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            if q.get('no') == 583:
                hit = q
if hit is None:
    raise SystemExit('未找到题 583')
hit['img'] = 'data/img/core_fig/no583.png'
hit['answer'] = ('【答案】$am+n$\n'
                 '（完整解析见下方图片：特征方程判别式分三种情况讨论，'
                 '并由 $f(x)=-f\'\'(x)-af\'(x)$ 积分得 $\\int_0^{+\\infty}f(x)\\,\\mathrm dx=f\'(0)+af(0)=n+am$）')
print('题 583 已挂图并精简答案')
print('  新答案:', hit['answer'][:60].replace('\n', ' '))

with io.open(CORE, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

# ---------- 3. SW PRECACHE ----------
s = io.open(SW, encoding='utf-8').read()
if "'data/img/core_fig/no583.png'" not in s:
    anchor = "    'data/img/core_fig/no515.png',\n"
    assert anchor in s, 'PRECACHE 锚点缺失'
    s = s.replace(anchor, anchor + "    'data/img/core_fig/no583.png',\n", 1)
    io.open(SW, 'w', encoding='utf-8', newline='').write(s)
    print('sw.js PRECACHE 已加入 no583.png')
else:
    print('sw.js 已包含 no583.png')

# ---------- 4. 扫描类似问题 ----------
print('\n=== 全库扫描：答案重复标记 / 解析指向图片 ===')
for fp in (CORE, 'pwa/data/xd_bank.json', 'pwa/data/exam.json'):
    if not os.path.exists(fp):
        continue
    with io.open(fp, encoding='utf-8') as f:
        data = json.load(f)
    dup, imgref = [], []
    for p in data:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                a = str(q.get('answer') or '')
                if '【答案】【答案】' in a:
                    dup.append(q.get('no'))
                if re.search(r'见原书|见下图|见解析图|见上方图|（图见|\(图见', a):
                    imgref.append((q.get('no'), a[:50].replace('\n', ' ')))
    print(f'{fp}: 答案头重复 {len(dup)} 处 {dup[:10]} | 解析引用图片 {len(imgref)} 处')
    for no, txt in imgref[:8]:
        print(f'   no={no}: {txt}')
