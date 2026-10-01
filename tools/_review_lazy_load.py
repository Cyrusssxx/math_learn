# -*- coding: utf-8 -*-
"""复测页改为分批渲染：首批 20 题，滚到底部自动加载更多（保留按钮兜底），避免一次性渲染全部题卡"""
import io

JS = 'pwa/js/category.js'
CSS = 'pwa/css/category.css'

s = io.open(JS, encoding='utf-8').read()

OLD = """function renderReview() {
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
}"""

NEW = """// 复测列表分批渲染：首批 RV_PAGE 题，滚到底部自动追加（并保留「加载更多」按钮兜底）
const RV_PAGE = 20;
let rvShown = RV_PAGE, rvList = [], rvIO = null;

function rvCardHtml(r) { return catCard(r.paper, r.secTitle, r.q); }

/** 只对新增批次做收尾：KaTeX、笔记自动展开、贴图回填（避免整页重算） */
function rvAfterRender(batch) {
    renderMath(batch);
    batch.querySelectorAll('.q-card').forEach(card => {
        const qid = card.id.replace(/^q-/, '');
        if ((noteGet(qid) || '').trim()) {
            const nb = card.querySelector('[data-act="note"]');
            if (nb && !nb.classList.contains('on')) nb.click();
        }
    });
    batch.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

function rvUpdateMore() {
    const btn = document.getElementById('rvMoreBtn');
    const tip = document.getElementById('rvMoreTip');
    const rest = rvList.length - rvShown;
    if (btn) {
        btn.style.display = rest > 0 ? '' : 'none';
        btn.textContent = '⬇️ 加载更多（还剩 ' + rest + ' 题）';
    }
    if (tip) tip.textContent = rest > 0 ? ('已显示 ' + rvShown + ' / ' + rvList.length + ' 题') : ('已全部加载 ' + rvList.length + ' 题');
}

/** 追加下一批（按钮点击 / 滚动到底自动触发） */
function rvAppendMore() {
    const wrap = document.getElementById('rvList');
    if (!wrap) return;
    const rest = rvList.slice(rvShown, rvShown + RV_PAGE);
    if (!rest.length) { rvUpdateMore(); return; }
    const batch = document.createElement('div');
    batch.className = 'rv-batch';
    batch.innerHTML = rest.map(rvCardHtml).join('');
    wrap.appendChild(batch);
    rvShown += rest.length;
    rvAfterRender(batch);
    rvUpdateMore();
}

/** 滚到底部附近自动加载下一批（浏览器不支持 IntersectionObserver 时按钮仍可用） */
function rvSetupAutoMore() {
    if (rvIO) { rvIO.disconnect(); rvIO = null; }
    const target = document.getElementById('rvBottom');
    if (!target || typeof IntersectionObserver === 'undefined') return;
    rvIO = new IntersectionObserver(es => { if (es.some(x => x.isIntersecting)) rvAppendMore(); }, { rootMargin: '600px' });
    rvIO.observe(target);
}

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
    rvList = list;
    rvShown = Math.min(RV_PAGE, list.length);

    const btns = [['all', `全部 ${counts.all}`], ['fav', `📥 收藏 ${counts.fav}`], ['mastered', `🟢 掌握 ${counts.mastered}`],
                  ['unfamiliar', `🟡 不熟 ${counts.unfamiliar}`], ['unknown', `🔴 不会 ${counts.unknown}`]]
        .map(([k, label]) => `<button class="cat-mark${rvFilter === k ? ' on' : ''}" data-rv="${k}" onclick="setRvFilter('${k}')">${label}</button>`).join('');
    let html = `<div class="paper-head">
        <h1>🔁 复测 · 我的标记题</h1>
        <div class="paper-sub">共 ${counts.all} 题 · 收藏 ${counts.fav} · 掌握 ${counts.mastered} · 不熟 ${counts.unfamiliar} · 不会 ${counts.unknown}｜分批加载（每批 ${RV_PAGE} 题，滚到底自动加载）｜笔记随题附带，标记与笔记改动实时同步</div>
        <div class="rv-filter">${btns}</div>
    </div>`;
    if (!list.length) {
        html += `<div class="empty-tip">当前筛选下没有题目。到真题页或分类页给题目点「☆ 收藏」或标「掌握 / 不熟 / 不会」，这里就会自动出现。</div>`;
        el.innerHTML = html;
        return;
    }
    html += `<div id="rvList"></div>
      <div class="rv-bottom" id="rvBottom">
        <button class="exam-btn" id="rvMoreBtn" onclick="rvAppendMore()">⬇️ 加载更多</button>
        <span class="rv-more-tip" id="rvMoreTip"></span>
      </div>`;
    el.innerHTML = html;
    const wrap = document.getElementById('rvList');
    const batch = document.createElement('div');
    batch.className = 'rv-batch';
    batch.innerHTML = rvList.slice(0, rvShown).map(rvCardHtml).join('');
    wrap.appendChild(batch);
    rvAfterRender(batch);
    rvUpdateMore();
    rvSetupAutoMore();
}"""

assert OLD in s, '未匹配到 renderReview 原实现'
s = s.replace(OLD, NEW, 1)
io.open(JS, 'w', encoding='utf-8', newline='').write(s)
print('category.js 已改为分批渲染')

css = io.open(CSS, encoding='utf-8').read()
css += '''
/* 复测页分批加载：底部提示与按钮 */
.rv-bottom { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 16px 0 44px; }
.rv-more-tip { font-size: 12.5px; color: var(--text-faint); }
'''
io.open(CSS, 'w', encoding='utf-8', newline='').write(css)
print('category.css 已追加分批加载样式')
