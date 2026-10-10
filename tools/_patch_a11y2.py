#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""给 index.html 的搜索框补 aria-label + 快捷键提示。
⚠️ 不硬编码行尾：用「定位 placeholder 子串 → 在其后插入」的方式，避免 CRLF/LF 假设出错。
"""
import io, sys, re

p = 'D:/ai code/math-note/pwa/index.html'
s = io.open(p, encoding='utf-8', newline='').read()
orig = s

if 'aria-label="搜索笔记' in s:
    print('已存在，跳过')
    sys.exit(0)

# 找到 searchInput 的 <input ...> 标签整体（跨行），在其中插 aria-label 并改 placeholder
m = re.search(r'<input type="search" id="searchInput"[^>]*>', s, re.S)
if not m:
    print('⚠️ 未找到 searchInput 标签')
    sys.exit(1)
tag = m.group(0)
new_tag = tag.replace('placeholder="搜索..."', 'placeholder="搜索…（/ 或 Ctrl+K）"')
if new_tag == tag:
    new_tag = tag.replace('placeholder="搜索', 'placeholder="搜索…（/ 或 Ctrl+K）\u200b"', 1)
# 在 id 后插入 aria-label（保持属性顺序可读）
new_tag = new_tag.replace('id="searchInput"', 'id="searchInput" aria-label="搜索笔记（快捷键 / 或 Ctrl+K）"', 1)

s = s[:m.start()] + new_tag + s[m.end():]
if s == orig:
    print('⚠️ 无实际改动')
    sys.exit(1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('已写入搜索框 aria-label + 快捷键提示')