/* 考研数学真题 - 独立页面：套卷切换 + 逐题卡片 + 收藏（localStorage） */

const FAV_KEY = 'examFav';           // { 套卷id: [题no, ...] } 或 {'qid':1}
const FAV_ONLY_KEY = 'examFavOnly';  // 是否只看收藏
const EXAM_POS_KEY = 'examLastPos';  // 刷新恢复上次位置：{paperId, no}

let papers = [];
let curPaper = null;
let favOnly = localStorage.getItem(FAV_ONLY_KEY) === '1';
let sideClosed = localStorage.getItem('examSideClosed') === '1';
let navCollapsed = localStorage.getItem('examNavCollapsed') === '1';

// ============ 收起/展开 ============
function toggleSide() {
    sideClosed = !sideClosed;
    localStorage.setItem('examSideClosed', sideClosed ? '1' : '0');
    const wrap = document.querySelector('.exam-wrap');
    const btn = document.getElementById('sideToggle');
    if (wrap) wrap.classList.toggle('side-closed', sideClosed);
    if (btn) btn.textContent = sideClosed ? '▶' : '◀';
}

function toggleFloatQ() {
    navCollapsed = !navCollapsed;
    localStorage.setItem('examNavCollapsed', navCollapsed ? '1' : '0');
    const fq = document.getElementById('floatQ');
    if (fq) fq.classList.toggle('collapsed', navCollapsed);
    // 新增：点击切换展开/收起态
    if (fq) fq.classList.toggle('expanded', !navCollapsed);
}

// ============ 收藏存储（按题唯一 id：套卷id-题号） ============
function favGet() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || {}; } catch (e) { return {}; }
}
function favSave(obj) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(obj)); }
    catch (e) { console.error('收藏保存失败（可能超出存储配额）:', e); alert('收藏存储空间不足，保存失败。请清理部分收藏后重试。'); }
}
function qidOf(paperId, no) { return paperId + '-' + no; }
function isFav(qid) { return !!favGet()[qid]; }
function toggleFav(qid, btn) {
    const f = favGet();
    if (f[qid]) delete f[qid]; else f[qid] = 1;
    favSave(f);
    if (btn) {
        btn.classList.toggle('on', !!f[qid]);
        btn.textContent = f[qid] ? '⭐' : '☆';   // 同步切换实心/空心星（之前只切 class 导致 UI 不更新）
        btn.title = f[qid] ? '取消收藏' : '收藏此题';
    }
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

/** 多行块：逐行处理，公式/文本混合；支持跨行 $$...$$ 块 */
/** 防御：单个未闭合的 $$ 会让 KaTeX 误吞后续内容、拖垮整张卡片。
 *  这里保证 $$ 成对：奇数时在末尾补一个闭合 $$，把影响限制在本公式内。 */
function balanceDollars(s) {
    const n = (s.match(/\$\$/g) || []).length;
    return n % 2 === 0 ? s : s + '$$';
}
function mdBlock(s) {
    s = balanceDollars(s);
    const lines = s.split('\n');
    const out = [];
    let mathBuf = null;   // 累积跨行 $$ 块

    for (const raw of lines) {
        const l = raw.trim();
        if (!l) { if (mathBuf) { mathBuf += '\n'; } continue; }

        // 检测 $$ 开/闭（不在行内 $ 内的独立 $$）
        if (mathBuf === null && l.startsWith('$$') && !l.endsWith('$$')) {
            // $$ 块开始
            mathBuf = l;
            continue;
        }
        if (mathBuf !== null) {
            mathBuf += '\n' + l;
            if (l.endsWith('$$')) {
                // $$ 块结束
                out.push('<p>' + mdInline(mathBuf) + '</p>');
                mathBuf = null;
            }
            continue;
        }
        out.push('<p>' + mdInline(l) + '</p>');
    }
    // 未闭合的 $$ 当普通行
    if (mathBuf) out.push('<p>' + mdInline(mathBuf) + '</p>');
    return out.join('');
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
    return `<div class="q-card" id="q-${qid}" data-qno="${q.no}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
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
    renderNav();
}

/** 右侧题号导航：显示当前套卷全部题号，点击跳转；滚动高亮当前题 */
function renderNav() {
    const el = document.getElementById('floatQNo');
    if (!el) return;
    const list = document.getElementById('floatQList');
    if (!curPaper) { el.textContent = '—'; if (list) list.innerHTML = ''; return; }
    const all = [];
    curPaper.sections.forEach((sec, si) => {
        sec.questions.forEach(q => all.push({ no: q.no, tag: secTag(si) }));
    });
    const favOnlyOn = favOnly;
    el.textContent = curPaper.year + '年';
    if (list) list.innerHTML = all.map(({ no, tag }) =>
        `<button class="nav-q${favOnlyOn && !isFav(qidOf(curPaper.id, no)) ? ' hidden' : ''}"
            data-navq="${no}" title="${tag}${no} 题" onclick="jumpToQ(${no})">${no}</button>`
    ).join('');
    highlightNav();
}

/** 滚动时高亮视口内当前题 */
function highlightNav() {
    const cards = Array.from(document.querySelectorAll('.q-card'));
    const btns = document.querySelectorAll('.nav-q');
    if (!cards.length || !btns.length) return;
    const half = window.innerHeight * 0.45;
    let cur = null;
    for (const c of cards) {
        const r = c.getBoundingClientRect();
        if (r.top <= half) cur = c; else break;
    }
    const curNo = cur ? cur.getAttribute('data-qno') : null;
    btns.forEach(b => b.classList.toggle('on', b.getAttribute('data-navq') === curNo));
}

/** 记录当前套卷 + 视口内题号（节流 + 退出时保存） */
function saveExamPos() {
    if (!curPaper) return;
    let no = null;
    const half = window.innerHeight * 0.45;
    for (const c of document.querySelectorAll('.q-card')) {
        if (c.getBoundingClientRect().top <= half) no = c.getAttribute('data-qno');
        else break;
    }
    try { localStorage.setItem(EXAM_POS_KEY, JSON.stringify({ paperId: curPaper.id, no })); }
    catch (e) { /* 忽略 */ }
}

function jumpToQ(no) {
    const qid = qidOf(curPaper.id, no);
    const el = document.getElementById('q-' + qid);
    console.log('Jump to:', no, qid, 'Element:', el);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        console.error('Element not found for:', qid);
    }
}

let _qPosTimer = null;
document.addEventListener('scroll', () => {
    highlightNav();
    if (!_qPosTimer) _qPosTimer = setTimeout(() => { _qPosTimer = null; saveExamPos(); }, 600);
}, { passive: true });
window.addEventListener('resize', () => { highlightNav(); });
window.addEventListener('beforeunload', saveExamPos);
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') saveExamPos(); });

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
    // 悬浮导航初始状态
    const fq = document.getElementById('floatQ');
    if (fq) {
        fq.classList.toggle('collapsed', navCollapsed);
        fq.classList.toggle('expanded', !navCollapsed);
    }
    // 恢复上次浏览位置：套卷 + 题号
    let startPaper = papers[0] || null;
    let startNo = null;
    try {
        const pos = JSON.parse(localStorage.getItem(EXAM_POS_KEY));
        if (pos && pos.paperId) {
            const p = papers.find(x => x.id === pos.paperId);
            if (p) { startPaper = p; startNo = pos.no ? parseInt(pos.no, 10) : null; }
        }
    } catch (e) { }
    curPaper = startPaper;
    renderPaperList();
    renderCurrent();
    const sub = document.getElementById('examSub');
    if (sub && curPaper) sub.textContent = curPaper.title;
    // 滚动到上次题号（收藏过滤下该题可能被隐藏，找不到则留在顶部）
    if (startNo) {
        const q = document.getElementById('q-' + qidOf(curPaper.id, startNo));
        if (q) q.scrollIntoView({ block: 'start' });
    }
}

init();
