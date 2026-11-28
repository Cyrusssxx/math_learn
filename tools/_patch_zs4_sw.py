# -*- coding: utf-8 -*-
"""把 127 张张宇四套 PDF 答案图加入 sw.js PRECACHE（幂等）。"""
import json, os

ROOT = r'D:/ai code/math-note'
SW = os.path.join(ROOT, 'pwa/sw.js')
d = json.load(open(os.path.join(ROOT, 'pwa/data/mn27_zs4_papers.json'), encoding='utf-8'))
paths = sorted({p for pp in d for s in pp['sections'] for q in s['questions']
                for p in (q.get('ansImg') or []) if 'mn27zs4pdf-' in p})
s = open(SW, encoding='utf-8').read()
anchor = "    'data/img/zx_site/mn27-zs4-3-20_1.png',\n"
assert anchor in s
assert "'data/img/zx_site/mn27zs4pdf-" not in s, 'already patched'
block = anchor + '    // 27 张宇四套：官方答案册 PDF 逐题切图（88 题 %d 张）\n' % len(paths)
block += ''.join("    '%s',\n" % p for p in paths)
s = s.replace(anchor, block, 1)
open(SW, 'w', encoding='utf-8').write(s)
print('SW PRECACHE 新增 %d 张' % len(paths))
