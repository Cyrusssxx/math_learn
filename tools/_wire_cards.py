# -*- coding: utf-8 -*-
"""记忆卡上线：index 入口改为「记忆卡」；精选选填入口并入好题刷题页；SW 预缓存登记"""
import io, os

# ---------- 1. index.html：精选选填入口 → 记忆卡 ----------
IDX = 'pwa/index.html'
h = io.open(IDX, encoding='utf-8').read()
old = '<a class="exam-link selected-link" href="selected.html" target="_blank" title="打开精选选填（新标签页）">✨ 精选选填</a>'
new = ('<a class="exam-link selected-link" href="cards.html" target="_blank" '
       'title="打开记忆卡（新标签页）：把笔记做成挖空卡片，按间隔重复复习">🧠 记忆卡</a>')
assert old in h, 'index 精选选填入口'
h = h.replace(old, new, 1)
io.open(IDX, 'w', encoding='utf-8', newline='').write(h)
print('index.html：入口改为 🧠 记忆卡 → cards.html')

# ---------- 2. good.html：并入「精选选填」入口 ----------
GD = 'pwa/good.html'
g = io.open(GD, encoding='utf-8').read()
anchor = '<button class="good-btn" id="favOnly" onclick="toggleFavOnly()" title="只看已收藏的题目">⭐ 收藏夹</button>'
add = ('\n            <a class="good-btn" href="selected.html" target="_blank" '
       'title="打开精选选填（新标签页）">✨ 精选选填</a>')
if 'href="selected.html"' in g:
    print('good.html：已存在精选选填入口，跳过')
elif anchor in g:
    g = g.replace(anchor, anchor + add, 1)
    io.open(GD, 'w', encoding='utf-8', newline='').write(g)
    print('good.html：顶栏已并入 ✨ 精选选填 入口')
else:
    raise SystemExit('good.html 未找到锚点')

# ---------- 3. sw.js：预缓存登记 ----------
SW = 'pwa/sw.js'
s = io.open(SW, encoding='utf-8').read()
added = []
for path, anchor2 in [('cards.html', "    'category.html',\n"),
                      ('css/cards.css', "    'css/category.css',\n"),
                      ('js/cards.js', "    'js/category.js',\n")]:
    if f"'{path}'" in s:
        continue
    if anchor2 in s:
        s = s.replace(anchor2, anchor2 + f"    '{path}',\n", 1)
        added.append(path)
if added:
    io.open(SW, 'w', encoding='utf-8', newline='').write(s)
print('sw.js PRECACHE 新增:', added if added else '无（已存在）')

# ---------- 4. 校验文件存在 ----------
for f in ('pwa/cards.html', 'pwa/css/cards.css', 'pwa/js/cards.js'):
    print(('OK  ' if os.path.exists(f) else '缺失 ') + f)
