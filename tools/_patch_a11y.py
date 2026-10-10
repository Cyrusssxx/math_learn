#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""给 index.html 的搜索框与移动端菜单按钮补 aria-label / 快捷键提示。
保持原行尾(CRLF),只做定点替换。"""
import io, sys

p = 'D:/ai code/math-note/pwa/index.html'
s = io.open(p, encoding='utf-8', newline='').read()
orig = s
rep = []

# 1) 搜索框：补 aria-label + 快捷键提示（placeholder 里带出来，用户才知道有这个键）
old1 = '<input type="search" id="searchInput" placeholder="搜索..."'
new1 = '<input type="search" id="searchInput" placeholder="搜索...（/ 或 Ctrl+K）"\r\n                   aria-label="搜索笔记（快捷键 / 或 Ctrl+K）"'
if old1 in s:
    s = s.replace(old1, new1, 1)
    rep.append('搜索框 aria-label + 快捷键提示')

# 2) 移动端 ☰ 按钮：补 aria-label
old2 = '<button class="menu-btn" onclick="document.getElementById(\'sidebar\').classList.toggle(\'show\')">☰</button>'
new2 = '<button class="menu-btn" aria-label="展开笔记目录" title="展开目录" onclick="document.getElementById(\'sidebar\').classList.toggle(\'show\')">☰</button>'
if old2 in s:
    s = s.replace(old2, new2, 1)
    rep.append('☰ 按钮 aria-label')

if s == orig:
    print('⚠️ 没有任何替换命中，未写入')
    sys.exit(1)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('已写入，改动：')
for r in rep:
    print('  · ' + r)
