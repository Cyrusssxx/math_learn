# -*- coding: utf-8 -*-
"""复测页：顶栏文案压缩 + 🔁 复测按钮 + review 模式（标记题汇总、带笔记、实时同步、可筛选）"""
import io

JS = 'pwa/js/category.js'
CSS = 'pwa/css/category.css'

s = io.open(JS, encoding='utf-8').read()
orig = s

# ============ 1. 顶栏文案压缩 ============
s = s.replace("exam: { label: '📝 数二真题分类',", "exam: { label: '📝 真题',", 1)
s = s.replace("core: { label: '📘 核心题库筛选',", "core: { label: '📘 核心题库',", 1)

old = "    b.textContent = yearSortDesc ? '⬇️ 年份倒序' : '⬆️ 年份顺序';"
new = "    b.textContent = yearSortDesc ? '⬇️ 年份' : '⬆️ 年份';"
assert old in s, 'yearSort 文案'
s = s.replace(old, new, 1)

# ============ 2. 复测模式模块（插到「渲染：主区」之前） ============
anchor = "// ============ 渲染：主区 ============"
review = '''// ============ 复测页（category.html?review=1）：我的收藏 / 掌握 / 不熟 / 不会 题汇总 ============
const REVIEW_MODE = new URLSearchParams(location.search).get('review') === '1';
let rvFilter = 'all';   // all | fav | mastered | unfamiliar | unknown

/** 顶栏「🔁 复测」→ 新标签页打开复测视图 */
function openReviewPage() {
    window.open('category.html?review=1', '_blank');
}

/** 复测模式初始化：隐藏左树与分类浏览专属控件，改标题 */
function applyReviewMode() {
    if (!REVIEW_MODE) return;
    document.body.classList.add('review-mode');
    const t = document.querySelector('.exam-title');
    if (t) t.textContent = '🔁 复测';
    const sub = document.getElementById('examSub');
    if (sub) {
        sub.textContent = '我的收藏 / 掌握 / 不熟 / 不会 题汇总 · 附带原有笔记 · 与真题页和分类页实时同步';
        sub.hidden = false;
    }
    ['srcToggle', 'unmarkedFirst', 'yearSortBtn'].forEach(id => {
        const b = document.getElementById(id);
        if (b) b.style.display = 'none';
    });
    const marks = document.querySelector('.cat-marks');
    if (marks) marks.style.display = 'none';   // 复测筛选在列表顶部单独渲染
}

function setRvFilter(f) {
    rvFilter = f;
    document.querySelectorAll('.rv-filter .cat-mark').forEach(b => b.classList.toggle('on', b.dataset.rv === f));
    renderReview();
}

/** 复测列表：所有带收藏或状态标记的题（同题去重），附笔记 */
function renderReview() {
    const el = document.getElementById('catMain');
    const st = statusGet() || {}, fav = favGet() || {};
    const seen = new Set();
    const rows = [];
    for (const e of allEntries) {
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null, f = !!fav[qid];
        if (!s && !f) continue;
        if (seen.has(qid)) continue;     // 同题多来源（真题/核心题库同源）只保留一条
        seen.add(qid);
        rows.push({ paper: e.paper, secTitle: e.secTitle, q: e.q, qid, st: s, fav: f });
    }
    const counts = {
        all: rows.length,
        fav: rows.filter(r => r.fav).length,
        mastered: rows.filter(r => r.st === 'mastered').length,
        unfamiliar: rows.filter(r => r.st === 'unfamiliar').length,
        unknown: rows.filter(r => r.st === 'unknown').length,
    };
    let list = rvFilter === 'all' ? rows
        : (rvFilter === 'fav' ? rows.filter(r => r.fav) : rows.filter(r => r.st === rvFilter));
    // 排序：不会 → 不熟 → 收藏 → 掌握；同类按年份倒序
    const rank = r => r.st === 'unknown' ? 0 : r.st === 'unfamiliar' ? 1 : (r.fav ? 2 : 3);
    list = list.slice().sort((a, b) => rank(a) - rank(b) || (Number(b.paper.year || 0) - Number(a.paper.year || 0)));

    const btns = [['all', `全部 ${counts.all}`], ['fav', `📥 收藏 ${counts.fav}`], ['mastered', `🟢 掌握 ${counts.mastered}`],
                  ['unfamiliar', `🟡 不熟 ${counts.unfamiliar}`], ['unknown', `🔴 不会 ${counts.unknown}`]]
        .map(([k, label]) => `<button class="cat-mark${rvFilter === k ? ' on' : ''}" data-rv="${k}" onclick="setRvFilter('${k}')">${label}</button>`).join('');
    let html = `<div class="paper-head">
        <h1>🔁 复测 · 我的标记题</h1>
        <div class="paper-sub">共 ${counts.all} 题 · 收藏 ${counts.fav} · 掌握 ${counts.mastered} · 不熟 ${counts.unfamiliar} · 不会 ${counts.unknown}｜笔记随题附带，在真题页/分类页的标记与笔记改动会实时同步到本页</div>
        <div class="rv-filter">${btns}</div>
    </div>`;
    if (!list.length) {
        html += `<div class="empty-tip">当前筛选下没有题目。到真题页或分类页给题目点「☆ 收藏」或标「掌握 / 不熟 / 不会」，这里就会自动出现。</div>`;
        el.innerHTML = html;
        return;
    }
    list.forEach(r => { html += catCard(r.paper, r.secTitle, r.q); });
    el.innerHTML = html;
    renderMath(el);
    // 附带原有笔记：有笔记的题自动展开笔记区
    el.querySelectorAll('.q-card').forEach(card => {
        const qid = card.id.replace(/^q-/, '');
        if ((noteGet(qid) || '').trim()) {
            const nb = card.querySelector('[data-act="note"]');
            if (nb && !nb.classList.contains('on')) nb.click();
        }
    });
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

// 跨标签页实时同步：别处（真题页 / 分类页）改动收藏、标记或笔记 → 复测页自动刷新
window.addEventListener('storage', (e) => {
    const k = e.key || '';
    if (k === FAV_KEY || k === EXAM_STATUS_KEY || k.indexOf('examNote-') === 0) {
        if (REVIEW_MODE) renderReview();
        else { renderTree(); renderMain(); }
    }
});

'''
assert anchor in s
s = s.replace(anchor, review + anchor, 1)

# ============ 3. renderMain 路由到复测视图 ============
old = """function renderMain() {
    const el = document.getElementById('catMain');
    if (catSearchKw) { renderSearchResults(); return; }   // 搜索模式：跨分类列表"""
new = """function renderMain() {
    const el = document.getElementById('catMain');
    if (REVIEW_MODE) { renderReview(); return; }           // 复测模式：标记题汇总
    if (catSearchKw) { renderSearchResults(); return; }   // 搜索模式：跨分类列表"""
assert old in s, 'renderMain 路由'
s = s.replace(old, new, 1)

# ============ 4. init 中启用复测模式 ============
old = "    applySrcMode(false);   // 先应用上次数据源（exam / core）→ 决定 papers，再建索引"
new = """    applySrcMode(false);   // 先应用上次数据源（exam / core）→ 决定 papers，再建索引
    applyReviewMode();     // 复测模式（?review=1）：隐藏分类树、改标题"""
assert old in s, 'init 调用'
s = s.replace(old, new, 1)

io.open(JS, 'w', encoding='utf-8', newline='').write(s)
print('category.js 复测模块已写入，字节变化:', len(s) - len(orig))

# ============ 5. CSS：顶栏压缩到一行 + 复测页样式 ============
css = io.open(CSS, encoding='utf-8').read()
add = '''
/* ============ 顶栏压缩：让所有按钮在同一行（小屏仍允许换行） ============ */
.exam-topbtns { gap: 6px; row-gap: 6px; flex-wrap: nowrap; }
.exam-topbtns .exam-btn { padding: 4px 9px; font-size: 12.5px; }
.exam-topbtns .cat-mark { padding: 3px 8px; font-size: 12.5px; }
.exam-topbtns .cat-search { width: 158px; font-size: 12.5px; }
.exam-topbtns .cat-search:focus { width: 200px; }
@media (max-width: 1400px) { .exam-topbtns { flex-wrap: wrap; } }

/* ============ 复测页（category.html?review=1） ============ */
body.review-mode .exam-wrap { grid-template-columns: 1fr; }
body.review-mode #catSide { display: none; }
body.review-mode #catMain { max-width: 1080px; }
.rv-filter { display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0 2px; }
.rv-filter .cat-mark { padding: 4px 10px; font-size: 12.5px; }
body.review-mode .q-card { margin-bottom: 14px; }
'''
io.open(CSS, 'w', encoding='utf-8', newline='').write(css + add)
print('category.css 已追加顶栏压缩与复测页样式')
