#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修正 notes.json 的目录(chapters)与正文 ## 的匹配度 + 列表缩进规范化

原则：**chapters 必须与正文 ## 逐项镜像**（reader.js 用下标 chapters[i] ↔ ch-i）。
差异时一律以**正文##文字**为准 —— 改 chapters 只动标签（目录/导航树/搜索路径），
改 ## 会动正文文本，可能让已有的划词批注/荧光高亮锚点失效。
"""
import io, json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'pwa', 'data', 'notes.json')
raw = io.open(P, encoding='utf-8').read()
notes = json.loads(raw)

DRY = '--apply' not in sys.argv


def dump(o):
    return json.dumps(o, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else '')


# 0) 自检：无改动时能否字节还原
assert dump(notes) == raw, '⚠️ 序列化不能字节还原，放弃写入（避免整文件 diff）'
print('[自检] json 往返字节一致 ✓')

changes = []

for n in notes:
    nid = n['id']
    md0 = n['md']
    md = md0

    # ---- 1) 列表缩进规范化：5→4、7→6（级别 floor(n/2) 不变，渲染完全等价） ----
    lines = md.split('\n')
    fixed = 0
    for i, l in enumerate(lines):
        m = re.match(r'^( +)- ', l)
        if m and len(m.group(1)) % 2:
            w = len(m.group(1))
            nw = w - 1                      # 5→4 / 7→6，floor(w/2) 不变
            lines[i] = ' ' * nw + l[w:]
            fixed += 1
    if fixed:
        md = '\n'.join(lines)
        changes.append(f'{nid}: 列表缩进规范化 {fixed} 行')

    # ---- 2) 连续 3+ 空行 → 2 个换行 ----
    md2, k = re.subn(r'\n{3,}', '\n\n', md)
    if k:
        md = md2
        changes.append(f'{nid}: 收敛连续空行 {k} 处')

    # ---- 3) 目录镜像正文 ## ----
    h2 = [re.sub(r'<!--.*?-->', '', l).rstrip()[3:].strip()
          for l in md.split('\n') if l.startswith('## ')]
    if h2 != n['chapters']:
        changes.append(f'{nid}: chapters {len(n["chapters"])} → {len(h2)} 项')
        for i in range(max(len(h2), len(n['chapters']))):
            a = h2[i] if i < len(h2) else '<无>'
            b = n['chapters'][i] if i < len(n['chapters']) else '<无>'
            if a != b:
                changes.append(f'    [{i}] 「{b}」 → 「{a}」')
        n['chapters'] = h2

    n['md'] = md

print('\n=== 变更清单 ===')
for c in changes:
    print('  ' + c)
if not changes:
    print('  （无变更）')

if DRY:
    print('\n[DRY-RUN] 未写入。加 --apply 执行。')
else:
    io.open(P, 'w', encoding='utf-8', newline='').write(dump(notes))
    print('\n[已写入] ' + P)
