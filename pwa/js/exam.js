/* 考研数学真题 - 独立页面：套卷切换 + 逐题卡片 + 收藏（localStorage） */

const FAV_KEY = 'examFav';           // { 套卷id: [题no, ...] } 或 {'qid':1}
const FAV_ONLY_KEY = 'examFavOnly';  // 是否只看收藏

let papers = [];
let curPaper = null;
let favOnly = localStorage.getItem(FAV_ONLY_KEY) === '1';

// ============ 收藏存储（按题唯一 id：套卷id-题号） ============
function favGet() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || {}; } catch (e) { return {}; }
}
function favSave(obj) { localStorage.setItem(FAV_KEY, JSON.stringify(obj)); }
function qidOf(paperId, no) { return paperId + '-' + no; }
function isFav(qid) { return !!favGet()[qid]; }
function toggleFav(qid, btn) {
    const f = favGet();
    if (f[qid]) delete f[qid]; else f[qid] = 1;
    favSave(f);
    if (btn) btn.classList.toggle('on', !!f[qid]);
    if (favOnly) renderCurrent();
}

function toggleFavOnly() {
    favOnly = !favOnly;
    localStorage.setItem(FAV_ONLY_KEY, favOnly ? '1' : '0');
    const btn = document.getElementById('favOnly');
    if (btn) btn.classList.toggle('on', favOnly);
    renderCurrent();
}

// ============ 渲染 ============
function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** 轻量 Markdown→HTML：KaTeX 原样保留；**加粗**；整行公式$$ $$；换行 → <br> */
function mdInline(s) {
    return esc(s)
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}

function mdBlock(s) {
    // 多行块：逐行处理，公式/文本混合
    return s.split('\n').map(line => {
        const l = line.trim();
        if (!l) return '';
        return '<p>' + mdInline(l) + '</p>';
    }).join('');
}

function renderPaperList() {
    const el = document.getElementById('paperList');
    el.innerHTML = papers.map(p =>
        `<button class="paper-item${curPaper && curPaper.id === p.id ? ' on' : ''}" onclick="openPaper('${p.id}')">
            <span class="paper-year">${p.year}</span>
            <span class="paper-name">${p.title.replace('年数学（二）真题', '年数二')}</span>
        </button>`
    ).join('');
}

function qCard(p, sec, q, secIdx) {
    const qid = qidOf(p.id, q.no);
    const fav = isFav(qid);
    const kindTag = q.kind === 'choice' ? '选择' : (q.no >= 11 && q.no <= 16 ? '填空' : '解答');
    const stem = mdBlock(q.stem);
    const options = q.options && q.options.length
        ? `<div class="q-options">${q.options.map(o => `<div class="q-opt">${mdInline(o)}</div>`).join('')}</div>`
        : '';
    return `<div class="q-card" id="q-${qid}">
        <div class="q-head">
            <span class="q-no">${secTag(secIdx)}-${q.no}</span>
            <span class="q-kind">${kindTag}</span>
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="收藏此题">${fav ? '⭐' : '☆'}</button>
        </div>
        <div class="q-body">${stem}${options}</div>
        <details class="q-answer">
            <summary>查看答案与解析</summary>
            <div class="q-answer-body">${mdBlock(q.answer)}</div>
        </details>
    </div>`;
}

function secTag(secIdx) {
    return ['一', '二', '三', '四', '五'][secIdx] || (secIdx + 1);
}

function renderCurrent() {
    const el = document.getElementById('examMain');
    if (!curPaper) { el.innerHTML = '<div class="loading">请选择一套卷</div>'; return; }
    let html = `<div class="paper-head">
        <h1>${curPaper.title}</h1>
        <div class="paper-meta">共 ${curPaper.sections.reduce((a, s) => a + s.questions.length, 0)} 题 · 满分 150 分</div>
    </div>`;
    let shown = 0, total = 0;
    curPaper.sections.forEach((sec, si) => {
        const secQs = sec.questions.filter(q => !favOnly || isFav(qidOf(curPaper.id, q.no)));
        total += sec.questions.length;
        shown += secQs.length;
        if (!secQs.length) return;
        html += `<div class="q-section">
            <div class="q-section-title">${sec.title}</div>`;
        secQs.forEach(q => { html += qCard(curPaper, sec, q, si); });
        html += '</div>';
    });
    if (favOnly && shown === 0) {
        html += '<div class="empty-tip">还没有收藏的题目，点击题目右上角 ☆ 收藏。</div>';
    }
    el.innerHTML = html + (favOnly ? `<div class="fav-count">收藏 ${shown}/${total} 题</div>` : '');
    renderMath(el);
}

function renderMath(root) {
    if (!window.katex || !root) return;
    try {
        renderMathInElement(root, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '\\[', right: '\\]', display: true },
                { left: '$', right: '$', display: false },
            ],
            throwOnError: false,
        });
    } catch (e) { /* ignore */ }
}

function openPaper(id) {
    curPaper = papers.find(p => p.id === id);
    renderPaperList();
    renderCurrent();
    const sub = document.getElementById('examSub');
    if (sub && curPaper) sub.textContent = curPaper.title;
    const q = document.querySelector('.q-card');
    if (q) q.scrollIntoView();
}

async function init() {
    const resp = await fetch('data/exam.json');
    if (!resp.ok) throw new Error('加载真题失败: ' + resp.status);
    papers = await resp.json();
    const favBtn = document.getElementById('favOnly');
    if (favBtn) favBtn.classList.toggle('on', favOnly);
    // 默认打开最新套卷
    const saved = papers.find(p => p.year === new Date().getFullYear());
    curPaper = papers[0] || null;
    renderPaperList();
    renderCurrent();
    const sub = document.getElementById('examSub');
    if (sub && curPaper) sub.textContent = curPaper.title;
}

init();
