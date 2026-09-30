# -*- coding: utf-8 -*-
"""按指定题号导出 core_bank 题目信息到 UTF-8 文件
用法: python tools/_dump_custom.py 488,490,492
"""
import json, io, sys

NOS = [int(x) for x in sys.argv[1].split(',')]
OUT = sys.argv[2] if len(sys.argv) > 2 else 'tools/_dump_custom.txt'

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
            lines.append('答案开头: ' + ans[:150].replace('\n', ' '))
            if len(ans) > 500:
                lines.append('答案末尾: …' + ans[-250:].replace('\n', ' '))
            lines.append('idea: ' + str(q.get('idea') or '')[:150].replace('\n', ' '))
            lines.append('')

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'已写入 {OUT}')
