#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复上一步被写坏的 searchInput 标签：去掉零宽字符与多余引号，写成干净的属性列表。"""
import io, re, sys

p = 'D:/ai code/math-note/pwa/index.html'
s = io.open(p, encoding='utf-8', newline='').read()
orig = s

m = re.search(r'<input type="search" id="searchInput"[^>]*?>', s, re.S)
if not m:
    print('未找到 searchInput'); sys.exit(1)

old = m.group(0)
# 取原有的事件属性，重新拼一个干净标签（保留 ind）不用猜缩进：整段重写
new = ('<input type="search" id="searchInput" aria-label="搜索笔记（快捷键 / 或 Ctrl+K）" '
       'placeholder="搜索… /  Ctrl+K"\r\n'
       '                   autocomplete="off" oninput="onSearchDebounced(this.value)" '
       'onfocus="onSearchFocus(this.value)">')

s = s[:m.start()] + new + s[m.end():]
# 保险：清掉任何残留的零宽字符
s = s.replace('\u200b', '')

if s == orig:
    print('无改动'); sys.exit(0)
io.open(p, 'w', encoding='utf-8', newline='').write(s)

chk = io.open(p, encoding='utf-8', newline='').read()
mm = re.search(r'<input type="search" id="searchInput"[^>]*?>', chk, re.S)
print('修复后：')
print(repr(mm.group(0)))
print('零宽字符残留 =', chk.count('\u200b'))