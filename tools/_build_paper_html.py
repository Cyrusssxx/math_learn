# 从 category.html 生成独立拼卷页 paper.html
# 骨架写死拼卷样式，强刷第一帧就是拼卷，不再闪分类页
import re
from pathlib import Path

PWA = Path(__file__).resolve().parent.parent / 'pwa'
src = (PWA / 'category.html').read_text(encoding='utf-8')
h = src

# 1) 页面标题
h = h.replace('<title>分类题库</title>', '<title>🎲 拼卷 · 随机收藏题</title>', 1)

# 2) 顶栏品牌：标题 + 副标题（副标题直接写小块，data-tip 完整规则，与 ppApplyMode 一致）
h = h.replace(
    '<div class="exam-title">分类题库</div>\n                <div class="exam-sub" id="examSub">按大观园三级分类（学科 / 章节 / 知识点）· 点击知识点查看跨年真题</div>',
    '<div class="exam-title">🎲 拼卷</div>\n                <div class="exam-sub pp-tip" id="examSub" data-tip="从收藏的题里拼一份卷（22 题起，可加量）· 不会 / 不熟抽完才抽仅收藏 · 同一状态内最久没做的先抽 · 抽过的题不再重复">ⓘ 抽题规则</div>',
    1)

# 3) 左栏标题 + 树容器直接换成历史拼卷列表容器（ppSide 往里面填）
h = h.replace('<div class="exam-side-title">知识点分类</div>', '<div class="exam-side-title">历史拼卷</div>', 1)
h = h.replace('<div id="catTree"></div>', '<div id="catTree"><div id="paperList"></div></div>', 1)

# 4) 隐藏分类页专属控件（静态 hidden，避免 JS 加载前闪出）
for btn_id in ('srcToggle', 'unmarkedFirst', 'yearSortBtn'):
    h = h.replace(f'<button class="exam-btn" id="{btn_id}"', f'<button class="exam-btn" id="{btn_id}" hidden', 1)
h = h.replace('<div class="cat-marks">', '<div class="cat-marks" hidden>', 1)

# 5) 顶栏「拼卷」入口在本页改为非当前页提示：本页就是拼卷，去掉指向自己的 🎲 拼卷链接
h = re.sub(r'\s*<a class="exam-btn rv-entry" href="category\.html\?paper=1"[^>]*>🎲 拼卷</a>', '', h, count=1)

# 6) 「🗂 分类题库」返回按钮：本页不是 paper-mode 切换文案，直接显示分类题库（去掉 rv-back-paper span，
#    保留 rv-back-label 并去掉 hidden 依赖，避免 CSS 依赖 body.paper-mode）
h = h.replace(
    '<a class="exam-btn rv-back hf-back" href="category.html" title="返回分类页"><span class="rv-back-label">🗂 分类</span><span class="rv-back-paper">🗂 分类题库</span></a>',
    '<a class="exam-btn" href="category.html" title="返回分类题库">🗂 分类题库</a>',
    1)

# 7) 背景面板 PAGE_ID：category → paper，并把 paper 加入应用范围列表
h = h.replace("const PAGE_ID = 'category';   // 本页标识（index / exam / category 三页各不相同）",
              "const PAGE_ID = 'paper';   // 本页标识（index / exam / category / paper 各不相同）", 1)
h = h.replace("{ id: 'category', label: '分类页' },",
              "{ id: 'category', label: '分类页' },\n        { id: 'paper', label: '拼卷页' },", 1)

# 8) 主区首屏占位：分类页「加载中」改为拼卷提示（数据未到前不误导）
h = h.replace('<div class="loading">加载中…</div>',
              '<div class="loading">🎲 正在准备拼卷…</div>', 1)

# 校验：改动点都命中
checks = {
    'title': '<title>🎲 拼卷 · 随机收藏题</title>' in h,
    'brand': '<div class="exam-title">🎲 拼卷</div>' in h,
    'sub': 'id="examSub" data-tip=' in h and 'ⓘ 抽题规则</div>' in h,
    'side': '<div class="exam-side-title">历史拼卷</div>' in h,
    'paperList': '<div id="paperList"></div>' in h,
    'srcHidden': 'id="srcToggle" hidden' in h and 'id="unmarkedFirst" hidden' in h and 'id="yearSortBtn" hidden' in h,
    'marksHidden': '<div class="cat-marks" hidden>' in h,
    'noSelfLink': 'href="category.html?paper=1"' not in h,
    'back': '>🗂 分类题库</a>' in h,
    'pageId': "const PAGE_ID = 'paper'" in h,
    'scope': "{ id: 'paper', label: '拼卷页' }," in h,
    'loading': '🎲 正在准备拼卷…' in h,
    'noOldBrand': '<div class="exam-title">分类题库</div>' not in h,
    'noOldSide': '<div class="exam-side-title">知识点分类</div>' not in h,
}
bad = [k for k, v in checks.items() if not v]
if bad:
    raise SystemExit('替换校验失败: ' + ', '.join(bad))

(PWA / 'paper.html').write_text(h, encoding='utf-8', newline='')
print('OK paper.html bytes=', len(h.encode('utf-8')))
print('checks=', len(checks))
