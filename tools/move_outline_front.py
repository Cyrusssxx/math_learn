# -*- coding: utf-8 -*-
"""move_outline_front.py — 把各导图 md 末尾的「考试大纲要点/考点提示」章移到第一章之前
（常考重点前置）。用法：python -X utf8 move_outline_front.py
"""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent.parent / 'math' / '导图'
PAT = re.compile(r'^## (考试大纲要点|考点提示)')

for path in sorted(SRC.glob('*.md')):
    lines = path.read_text(encoding='utf-8').splitlines()
    # 找目标章的起止
    start = next((i for i, l in enumerate(lines) if PAT.match(l)), None)
    if start is None:
        print(f'跳过（无要点章）: {path.name}')
        continue
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
    first_h2 = next((i for i, l in enumerate(lines) if l.startswith('## ')), None)
    if first_h2 == start:
        print(f'已在最前: {path.name}')
        continue
    block = [l for l in lines[start:end] if l.strip()] + ['']
    rest = lines[:start] + lines[end:]
    # 在第一章前插入
    first_h2 = next(i for i, l in enumerate(rest) if l.startswith('## '))
    out = rest[:first_h2] + block + rest[first_h2:]
    path.write_text('\n'.join(out).rstrip() + '\n', encoding='utf-8')
    print(f'前置完成: {path.name}（{lines[start][3:].strip()}）')
