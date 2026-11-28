# -*- coding: utf-8 -*-
"""把崔6切图加入 sw.js PRECACHE（幂等）。"""
import json, os, re

ROOT = r'D:/ai code/math-note'
SW = os.path.join(ROOT, 'pwa', 'sw.js')
DATA = os.path.join(ROOT, 'pwa', 'data', 'mn27_cui6_papers.json')
PREFIX = 'mn27cui6pdf-'

d = json.load(open(DATA, encoding='utf-8'))
imgs = sorted({p for s0 in d for s in s0['sections'] for q in s['questions']
               for p in (q.get('ansImg') or []) if PREFIX in p})
s = open(SW, encoding='utf-8').read()

# 先移除旧的崔6图片条目
lines = [l for l in s.split('\n') if PREFIX not in l]
s = '\n'.join(lines)

anchor = "    'data/mn27_cui6_papers.json',\n"
assert anchor in s
fig = 'data/img/mn27/mn27_qcui01_03.png'
paths = [fig] + imgs
block = anchor + '\n'.join(f"    '{p}'," for p in paths) + '\n'
s = s.replace(anchor, block, 1)
with open(SW, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('写入', len(imgs), '张崔6预缓存')
