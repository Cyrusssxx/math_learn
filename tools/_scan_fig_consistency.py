# -*- coding: utf-8 -*-
"""题图一致性双向检查：
1) exam_fig/*.png 文件未被任何 q.img/q.img2 引用（孤儿文件）
2) 题干含 如图/下图/如右图/图中曲线/图所示 等字样但 q.img/q.img2 为空（缺图题）
用法: python -X utf8 tools/_scan_fig_consistency.py
"""
import json, re, os, glob

EXAM = 'pwa/data/exam.json'
FIGDIR = 'pwa/data/img/exam_fig'

d = json.load(open(EXAM, encoding='utf-8'))

# 收集所有被引用图文件
used = set()
imgless_q = []
PAT = re.compile(r'如图|下图|如右图|如左图|图所示|如图所示|图中曲线|由图中')
for e in d:
    for s in e.get('sections', []):
        for q in s.get('questions', []):
            for k in ('img', 'img2'):
                v = q.get(k)
                if v:
                    used.add(os.path.basename(v))
            stem = q.get('stem') or ''
            if PAT.search(stem) and not (q.get('img') or q.get('img2')):
                imgless_q.append((str(e.get('year')), q.get('no'), stem.split('\n')[0][:60]))

# 1) 孤儿文件
orphans = []
for f in sorted(glob.glob(os.path.join(FIGDIR, '*.png'))):
    b = os.path.basename(f)
    if b not in used:
        orphans.append(b)

print('=== 1) exam_fig 未被引用文件(孤儿) ===')
for o in orphans:
    print('  -', o)
if not orphans:
    print('  (无)')

print('\n=== 2) 题干含图字样但无配图的题 ===')
for y, no, st in imgless_q:
    print(f'  - {y} Q{no}: {st}')
if not imgless_q:
    print('  (无)')
