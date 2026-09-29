# -*- coding: utf-8 -*-
"""图片选项题挂图 + 扫描其余「图形见原书」题目的真题图可用性"""
import json, io, os

# ============ 1. 挂图（真题卷现成图，直接复用） ============
with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

ATTACH = {
    # no: (img, img2, 新选项)
    205: ('data/img/exam_fig/2001_q10.png', 'data/img/exam_fig/2001_q10_abcd.png'),
    382: ('data/img/exam_fig/2009_q06.png', 'data/img/exam_fig/2009_q06_abcd.png'),
}
IMG_OPTS = ['图 A', '图 B', '图 C', '图 D']

attached, missing_files = [], []
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            no = q.get('no')
            if no in ATTACH:
                img, img2 = ATTACH[no]
                # 校验文件存在（相对 pwa/）
                for rel in (img, img2):
                    if not os.path.exists(os.path.join('pwa', rel)):
                        missing_files.append(rel)
                q['img'] = img
                q['img2'] = img2
                q['options'] = list(IMG_OPTS)
                attached.append(no)

print(f'已挂图题号: {attached}')
print(f'缺失文件: {missing_files if missing_files else "无（全部存在）"}')

# ============ 2. 扫描其余「图形见原书/如图」题：linkedQid 是否有真题图 ============
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)
exam_img = {}
for p in exam:
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            if q.get('img'):
                exam_img[f'{p["id"]}-{q["no"]}'] = (q.get('img'), q.get('img2'))

KW = ['图形见原书', '如图', '图见原书', '原题附有', '原题配有一幅']
print('\n=== 其余依赖配图的题目（未挂图）===')
need_report = []
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            no = q.get('no')
            if no in ATTACH:
                continue
            blob = str(q.get('stem', ''))
            if any(k in blob for k in KW):
                lq = q.get('linkedQid')
                hit = exam_img.get(lq) if lq else None
                flag = '✅有真题图可挂' if hit else '❌无图源'
                print(f"no={no} | linked={lq} | {flag} | {hit[0] if hit else ''}")
                need_report.append((no, bool(hit)))

# ============ 3. 写回 core_bank.json（紧凑单行） ============
with io.open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))
print('\ncore_bank.json 已写回（紧凑单行）')

# 验证
with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    chk = json.load(f)
q205 = next(q for p in chk for s in p['sections'] for q in s['questions'] if q.get('no') == 205)
assert q205['img'].endswith('2001_q10.png') and q205['options'] == IMG_OPTS
q382 = next(q for p in chk for s in p['sections'] for q in s['questions'] if q.get('no') == 382)
assert q382['img'].endswith('2009_q06.png') and q382['options'] == IMG_OPTS
print('写回验证通过：no=205 与 no=382 已挂图、选项已改为 图A~图D')
