# -*- coding: utf-8 -*-
"""修复：复测页标签标题仍是「真题分类」+ 复测入口改为原生链接（避免弹窗拦截/复用标签导致误以为跳回分类）
   - 复测模式设置 document.title
   - 复测入口由 window.open 改为 <a target="_blank" rel="noopener">
   - 复测页新增「🗂 分类」返回入口；复测页内隐藏复测入口本身
"""
import io

HTML = 'pwa/category.html'
JS = 'pwa/js/category.js'
CSS = 'pwa/css/category.css'

# ---------- HTML ----------
h = io.open(HTML, encoding='utf-8').read()
old = '<button class="exam-btn" onmousedown="event.preventDefault()" onclick="openReviewPage()" title="复测：新标签页打开「我的标记题」汇总（收藏/掌握/不熟/不会，附带笔记，实时同步）">🔁 复测</button>'
new = ('<a class="exam-btn rv-entry" href="category.html?review=1" target="_blank" rel="noopener" '
       'title="复测：新标签页打开「我的标记题」汇总（收藏/掌握/不熟/不会，附带笔记，实时同步）">🔁 复测</a>\n'
       '            <a class="exam-btn rv-back" href="category.html" title="返回分类页">🗂 分类</a>')
assert old in h, '复测按钮'
h = h.replace(old, new, 1)
io.open(HTML, 'w', encoding='utf-8', newline='').write(h)
print('category.html：复测入口改为原生链接 + 新增返回分类入口')

# ---------- JS ----------
s = io.open(JS, encoding='utf-8').read()
old = """    const sub = document.getElementById('examSub');
    if (sub) {
        sub.textContent = '我的收藏 / 掌握 / 不熟 / 不会 题汇总 · 附带原有笔记 · 与真题页和分类页实时同步';
        sub.hidden = false;
    }"""
new = """    document.title = '🔁 复测 · 我的标记题';   // 标签页标题（否则仍是「真题分类」，易误以为跳回了分类）
    const sub = document.getElementById('examSub');
    if (sub) {
        sub.textContent = '我的收藏 / 掌握 / 不熟 / 不会 题汇总 · 附带原有笔记 · 与真题页和分类页实时同步';
        sub.hidden = false;
    }"""
assert old in s, 'applyReviewMode 标题'
s = s.replace(old, new, 1)

old = """function openReviewPage() {
    window.open('category.html?review=1', '_blank');
}"""
new = """function openReviewPage() {
    // 顶栏入口已改为原生 <a target="_blank">（避免弹窗拦截）；此处保留兼容调用
    window.open('category.html?review=1', '_blank', 'noopener');
}"""
assert old in s, 'openReviewPage'
s = s.replace(old, new, 1)
io.open(JS, 'w', encoding='utf-8', newline='').write(s)
print('category.js：复测模式设置 document.title')

# ---------- CSS ----------
c = io.open(CSS, encoding='utf-8').read()
c += '''
/* 复测入口 / 返回分类入口：仅在对应视图显示 */
.rv-back { display: none; }
body.review-mode .rv-back { display: inline-flex; }
body.review-mode .rv-entry { display: none; }   /* 已在复测页，隐藏入口避免重复打开 */
'''
io.open(CSS, 'w', encoding='utf-8', newline='').write(c)
print('category.css：复测入口/返回入口显隐样式')
