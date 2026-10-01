# -*- coding: utf-8 -*-
"""复测页：每批加载 40 题 + 底部加底线（分隔线）与「加载更多题」按钮"""
import io

JS = 'pwa/js/category.js'
CSS = 'pwa/css/category.css'

s = io.open(JS, encoding='utf-8').read()

# 1. 每批 40 题
old = "const RV_PAGE = 20;"
new = "const RV_PAGE = 40;"
assert old in s, 'RV_PAGE'
s = s.replace(old, new, 1)

# 2. 按钮文案加「题」
old = "        btn.textContent = '⬇️ 加载更多（还剩 ' + rest + ' 题）';"
new = "        btn.textContent = '⬇️ 加载更多题（还剩 ' + rest + ' 题）';"
assert old in s, 'btn 文案'
s = s.replace(old, new, 1)

old = '<button class="exam-btn" id="rvMoreBtn" onclick="rvAppendMore()">⬇️ 加载更多</button>'
new = '<button class="exam-btn" id="rvMoreBtn" onclick="rvAppendMore()">⬇️ 加载更多题</button>'
assert old in s, 'bottom 按钮'
s = s.replace(old, new, 1)

io.open(JS, 'w', encoding='utf-8', newline='').write(s)
print('category.js：每批 40 题 + 文案「加载更多题」')

# 3. CSS：底部加底线（分隔线）+ 上间距
css = io.open(CSS, encoding='utf-8').read()
old = """.rv-bottom { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 16px 0 44px; }"""
new = """.rv-bottom {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    margin-top: 18px;                      /* 与上一批题目拉开距离 */
    padding: 18px 0 44px;
    border-top: 1px solid var(--border);   /* 底线：标记为列表分隔 */
}
.rv-bottom .exam-btn { padding: 6px 16px; font-size: 13px; }"""
assert old in css, 'rv-bottom css'
css = css.replace(old, new, 1)
io.open(CSS, 'w', encoding='utf-8', newline='').write(css)
print('category.css：底部底线与按钮样式已更新')
