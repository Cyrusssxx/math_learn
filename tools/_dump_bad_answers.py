# -*- coding: utf-8 -*-
"""导出待整治题目信息到 UTF-8 文件（避免终端编码问题）
每题：题号/来源/题干/选项/答案长度/答案开头(含正确答案)/答案末尾(判断截断)
"""
import json, io, sys

PART = sys.argv[1] if len(sys.argv) > 1 else 'trunc'

TRUNC_NOS = [23, 54, 185, 397, 153, 160, 180, 211, 227, 255, 316, 404, 412, 416, 417, 431, 432, 471]
LONG_NOS = [193, 70, 149, 155, 282, 454, 253, 274, 283, 285, 311, 312, 325, 424, 436, 445, 450, 461, 478, 479, 485]

NOS = TRUNC_NOS if PART == 'trunc' else LONG_NOS

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

lines = []
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            if q.get('no') not in NOS:
                continue
            ans = str(q.get('answer') or '')
            opts = q.get('options') or []
            lines.append('=' * 70)
            lines.append(f"no={q.get('no')} | src={q.get('source')} | 长度={len(ans)}")
            lines.append(f"题干: {q.get('stem', '')}")
            if opts:
                lines.append('选项: ' + ' || '.join(str(o) for o in opts))
            lines.append('答案开头: ' + ans[:120].replace('\n', ' '))
            if len(ans) > 400:
                lines.append('答案末尾: …' + ans[-200:].replace('\n', ' '))
            lines.append('')

out = f'tools/_dump_{PART}.txt'
with io.open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'已写入 {out}（{len(NOS)} 题）')
