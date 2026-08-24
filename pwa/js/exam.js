/* 考研数学真题 - 独立页面：套卷切换 + 逐题卡片 + 收藏（localStorage） */

const FAV_KEY = 'examFav';           // { 套卷id: [题no, ...] } 或 {'qid':1}
const FAV_ONLY_KEY = 'examFavOnly';  // 是否只看收藏
const EXAM_POS_KEY = 'examLastPos';  // 刷新恢复上次位置：{paperId, no}
const REVIEW_KEY = 'examReview-';    // 试卷点评（按套卷 id 存）：examReview-{paperId}

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

// ============ 顶部栏整体折叠 ============
const TOP_COLLAPSED_KEY = 'examTopCollapsed';
function toggleTopBar(force) {
    const top = document.getElementById('examTop');
    const toggle = document.getElementById('examTopToggle');
    if (!top) return;
    const collapsed = (typeof force === 'boolean') ? force : !top.classList.contains('collapsed');
    top.classList.toggle('collapsed', collapsed);
    if (toggle) toggle.classList.toggle('collapsed', collapsed);
    localStorage.setItem(TOP_COLLAPSED_KEY, collapsed ? '1' : '0');
}
function restoreTopBar() {
    const collapsed = localStorage.getItem(TOP_COLLAPSED_KEY) === '1';
    toggleTopBar(collapsed);
}

// ============ 思路 / 笔记（2007 试水：有 idea 字段才显示思路按钮；笔记按题存 localStorage） ============
function noteGet(qid) {
    try { return localStorage.getItem('examNote-' + qid) || ''; } catch (e) { return ''; }
}
let _noteTimer = {};
function noteInput(ta) {
    const qid = ta.dataset.qid;
    const newVal = ta.value;
    const newRefs = examImgRefs(newVal);
    clearTimeout(_noteTimer[qid]);
    _noteTimer[qid] = setTimeout(() => {
        const olds = localStorage.getItem('examNote-' + qid) || '';
        const oldRefs = examImgRefs(olds);
        const orphan = oldRefs.filter(id => !newRefs.includes(id));
        if (orphan.length) examImgDel(orphan);   // 清理不再引用的图，避免存储泄漏
        try { localStorage.setItem('examNote-' + qid, newVal); } catch (e) { }
        const btn = ta.closest('.q-card') && ta.closest('.q-card').querySelector('[data-act="note"]');
        if (btn) btn.classList.toggle('has', !!newVal.trim());
    }, 500);
    // 编辑态只显示输入框；预览在「完成」时统一渲染（避免原文+预览双份显示）
}
// 笔记区 Ctrl+V 贴图：存 IndexedDB 后在光标处插入 [图:id]
function notePasteImg(e) {
    const it = [...(e.clipboardData?.items || [])].find(i => i.type.startsWith('image/'));
    if (!it) return;
    e.preventDefault();
    const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    const ta = e.target;
    examImgPut(id, it.getAsFile()).then(() => {
        const tag = `[图:${id}]`;
        const p = ta.selectionStart;
        ta.value = ta.value.slice(0, p) + tag + ta.value.slice(ta.selectionEnd);
        ta.selectionStart = ta.selectionEnd = p + tag.length;
        noteInput(ta);   // 触发保存 + 预览
    }).catch(() => alert('图片保存失败'));
}
function toggleQSec(btn, act) {
    const card = btn.closest('.q-card');
    if (!card)  return;
    const sec = card.querySelector('.q-sec.q-' + act);
    if (!sec) return;
    const open = sec.hidden;
    sec.hidden = !open;
    btn.classList.toggle('on', open);
    if (act === 'note') {
        const ta = sec.querySelector('textarea');
        if (ta) {
            if (open) {
                if (!ta.dataset.bind) {
                    ta.addEventListener('input', () => noteInput(ta));
                    ta.addEventListener('paste', notePasteImg);
                    ta.dataset.bind = '1';
                }
                ta.focus();
                noteInput(ta);
            }
        }
    }
}
// 笔记「✏️ 编辑 / 💾 完成」：编辑态只显示输入框，完成时落盘并渲染预览
function toggleNoteEdit(btn) {
    const sec = btn.closest('.q-note');
    const ta = sec.querySelector('.q-note-input');
    const pv = sec.querySelector('.q-note-preview');
    const editing = ta.style.display !== 'none';
    if (!editing) {
        // 进入编辑
        btn.textContent = '💾 完成';
        ta.style.display = '';
        if (pv) pv.hidden = true;
        if (!ta.dataset.bind) {
            ta.addEventListener('input', () => noteInput(ta));
            ta.addEventListener('paste', notePasteImg);
            ta.dataset.bind = '1';
        }
        ta.focus();
    } else {
        // 完成：清防抖定时器，立即落盘
        clearTimeout(_noteTimer[ta.dataset.qid]);
        delete _noteTimer[ta.dataset.qid];
        try { localStorage.setItem('examNote-' + ta.dataset.qid, ta.value); } catch (e) { }
        const v = ta.value.trim();
        if (v) {
            btn.textContent = '✏️ 编辑';
            ta.style.display = 'none';
            if (pv) {
                pv.innerHTML = mdBlockWithImg(ta.value);
                pv.hidden = false;
                renderMath(pv);
                if (ta.value.includes('[图:')) fillExamNoteImgs(pv);
            }
        } else {
            // 清空了内容：收起整节，重置为「空笔记」形态（下次展开直接是输入框）
            const opBtn = sec.closest('.q-card')?.querySelector('[data-act="note"]');
            sec.hidden = true;
            if (opBtn) opBtn.classList.remove('has');
            ta.style.display = '';
            btn.style.display = 'none';
        }
    }
}

// ============ 试卷点评（按套卷 id 存 localStorage，纯文本，popover 自动保存） ============
function reviewGet(pid) {
    try { return localStorage.getItem(REVIEW_KEY + pid) || ''; } catch (e) { return ''; }
}
function reviewSave(pid, v) {
    try { localStorage.setItem(REVIEW_KEY + pid, v); } catch (e) { }
}
function reviewHas(pid) { return !!reviewGet(pid).trim(); }

// ============ 笔记图片（IndexedDB，独立于收藏/点评；复用 [图:id] 占位符） ============
// 与笔记站 annotate.js 同机制：图片存 IndexedDB，文本里用 [图:id] 占位，渲染时回填
let _examImgDB = null;
function examImgDB() {
    if (!_examImgDB) {
        _examImgDB = new Promise((res, rej) => {
            const rq = indexedDB.open('examNoteImg', 1);
            rq.onupgradeneeded = () => rq.result.createObjectStore('imgs');
            rq.onsuccess = () => res(rq.result);
            rq.onerror = () => rej(rq.error);
        });
    }
    return _examImgDB;
}
function examImgPut(id, blob) {
    return examImgDB().then(d => new Promise((res, rej) => {
        const tx = d.transaction('imgs', 'readwrite');
        tx.objectStore('imgs').put(blob, id);
        tx.oncomplete = res; tx.onerror = () => rej(tx.error);
    }));
}
function examImgGet(id) {
    return examImgDB().then(d => new Promise(res => {
        const rq = d.transaction('imgs').objectStore('imgs').get(id);
        rq.onsuccess = () => res(rq.result || null);
        rq.onerror = () => res(null);
    }));
}
function examImgDel(ids) {
    if (!ids || !ids.length) return Promise.resolve();
    return examImgDB().then(d => new Promise(res => {
        const tx = d.transaction('imgs', 'readwrite');
        ids.forEach(id => tx.objectStore('imgs').delete(id));
        tx.oncomplete = res; tx.onerror = res;
    }));
}
function examImgRefs(t) {
    return [...(t || '').matchAll(/\[图:([a-z0-9]+)\]/g)].map(m => m[1]);
}
// 渲染笔记文本时，把 [图:id] 换成占位 img（后续 fillExamNoteImgs 回填 blob）
function mdBlockWithImg(s) {
    return mdBlock(s)
        .replace(/\[图:([a-z0-9]+)\]/g,
            (_, id) => `<img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)">`);
}
async function fillExamNoteImgs(root) {
    if (!root) return;
    const imgs = root.querySelectorAll('img.exam-note-img[data-img]');
    for (const img of imgs) {
        const blob = await examImgGet(img.dataset.img);
        if (blob) img.src = URL.createObjectURL(blob);
        else img.replaceWith(document.createTextNode('[图片已丢失]'));
    }
}

// ============ 配图 / 笔记贴图 单击放大（复用 exam.css 的 .zoom-overlay 遮罩） ============
function zoomAnsImg(img) {
    let ov = document.getElementById('zoomOverlay');
    if (!ov) {
        ov = document.createElement('div');
        ov.id = 'zoomOverlay';
        ov.className = 'zoom-overlay';
        ov.onclick = function () { ov.classList.remove('show'); };
        ov.innerHTML = '<img id="zoomImg" alt="放大图片">';
        const big = ov.querySelector('#zoomImg');
        // 点放大图本身不关闭，点遮罩其余处关闭
        big.onclick = function (e) { e.stopPropagation(); };
        document.body.appendChild(ov);
        // Esc 关闭
        document.addEventListener('keydown', function onEsc(e) {
            if (e.key === 'Escape') {
                ov.classList.remove('show');
                document.removeEventListener('keydown', onEsc);
            }
        });
    }
    const big = document.getElementById('zoomImg');
    big.src = img.currentSrc || img.src;
    ov.classList.add('show');
}

// 全局唯一 popover 节点（懒创建，挂载到 body）
let _reviewPop = null;
let _reviewPid = null;
let _reviewTimer = null;
function reviewPop() {
    if (_reviewPop) return _reviewPop;
    const ov = document.createElement('div');
    ov.className = 'review-pop';
    ov.innerHTML =
        '<div class="review-pop-head"><span class="review-pop-title">试卷点评</span>' +
        '<button class="review-pop-x" title="关闭">×</button></div>' +
        '<textarea class="review-pop-ta" placeholder="写下对这套卷的整体点评：难度、易错点、时间分配、复习建议…（自动保存）"></textarea>' +
        '<div class="review-pop-tip">自动保存到本机浏览器 · 仅自己可见</div>';
    document.body.appendChild(ov);
    // 关闭按钮
    ov.querySelector('.review-pop-x').addEventListener('click', closeReviewPop);
    // 输入防抖保存
    const ta = ov.querySelector('.review-pop-ta');
    ta.addEventListener('input', () => {
        clearTimeout(_reviewTimer);
        _reviewTimer = setTimeout(() => {
            const v = ta.value;
            reviewSave(_reviewPid, v);
            syncReviewMarkers();   // 实时更新方块/列表标记填充态
        }, 500);
    });
    // 点击 popover 内部不冒泡到 document（避免触发外部关闭）
    ov.addEventListener('click', (e) => e.stopPropagation());
    _reviewPop = ov;
    return ov;
}
function openReviewPop(pid, anchor) {
    const ov = reviewPop();
    const ta = ov.querySelector('.review-pop-ta');
    _reviewPid = pid;
    ta.value = reviewGet(pid);
    // 定位：锚定在小方块右侧/下方
    ov.style.display = 'block';
    const r = anchor.getBoundingClientRect();
    const pw = 320, ph = ov.offsetHeight || 220;
    let left = r.right + 8;
    let top = r.top;
    if (left + pw > window.innerWidth - 8) left = Math.max(8, r.left - pw - 8);
    if (top + ph > window.innerHeight - 8) top = Math.max(8, window.innerHeight - ph - 8);
    ov.style.left = left + 'px';
    ov.style.top = top + 'px';
    setTimeout(() => ta.focus(), 0);
    // 绑定一次性外部点击 / Esc 关闭
    setTimeout(() => {
        document.addEventListener('click', _reviewOutside);
        document.addEventListener('keydown', _reviewEsc);
    }, 0);
}
function closeReviewPop() {
    if (_reviewPop) _reviewPop.style.display = 'none';
    _reviewPid = null;
    document.removeEventListener('click', _reviewOutside);
    document.removeEventListener('keydown', _reviewEsc);
}
function _reviewOutside(e) {
    if (_reviewPop && !_reviewPop.contains(e.target) && !e.target.closest('.review-btn')) {
        closeReviewPop();
    }
}
function _reviewEsc(e) { if (e.key === 'Escape') closeReviewPop(); }

// 同步所有点评标记（小方块 + 左侧列表项）的填充态，依据当前数据
function syncReviewMarkers() {
    document.querySelectorAll('.review-btn').forEach(b => {
        b.classList.toggle('has', reviewHas(b.dataset.pid));
    });
    document.querySelectorAll('.paper-item').forEach(b => {
        const pid = b.dataset.pid || (b.getAttribute('onclick') ? b.getAttribute('onclick').match(/'([^']+)'/g) : null);
        const id = b.dataset.pid || '';
        b.classList.toggle('has-review', reviewHas(id));
    });
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
        `<button class="paper-item${curPaper && curPaper.id === p.id ? ' on' : ''}" data-pid="${p.id}" onclick="openPaper('${p.id}')">
            <span class="paper-year">${p.year}</span>
            <span class="paper-name">${p.title.replace('年数学（二）真题', '年数二')}</span>
            <span class="review-dot${reviewHas(p.id) ? ' on' : ''}" title="有试卷点评"></span>
        </button>`
    ).join('');
}

function qCard(p, sec, q, secIdx) {
    const qid = qidOf(p.id, q.no);
    const fav = isFav(qid);
    const kindTag = q.kind === 'choice' ? '选择' : (q.no >= 11 && q.no <= 16 ? '填空' : '解答');
    const stem = mdBlock(q.stem);
    const figHtml = q.img ? `<img class="q-fig-img" src="${q.img}" alt="题${q.no}配图" loading="lazy" onclick="zoomAnsImg(this)">${(q.img2?`<img class="q-fig-img" src="${q.img2}" alt="题${q.no}配图2" loading="lazy" onclick="zoomAnsImg(this)">`:'')}` : '';
    const options = q.options && q.options.length
        ? `<div class="q-options">${q.options.map(o => `<div class="q-opt">${mdInline(o)}</div>`).join('')}</div>`
        : '';
    const note = noteGet(qid);
    const hasNote = !!note.trim();
    const noteHtml = hasNote
        ? `<div class="q-sec q-note">
            <div class="q-note-preview">${mdBlockWithImg(note)}</div>
            <textarea class="q-note-input" data-qid="${qid}" style="display:none" placeholder="记下你的思路、易错点、类比题…（Ctrl+V 可贴图；用 $...$ 写公式会自动渲染）">${esc(note)}</textarea>
            <button class="q-note-editbtn" onclick="toggleNoteEdit(this)" title="编辑笔记">✏️ 编辑</button>
        </div>`
        : `<div class="q-sec q-note" hidden>
            <textarea class="q-note-input" data-qid="${qid}" placeholder="记下你的思路、易错点、类比题…（Ctrl+V 可贴图；用 $...$ 写公式会自动渲染）"></textarea>
            <div class="q-note-preview" hidden></div>
        </div>`;
    const ideaBtn = q.idea ? `<button class="q-op" data-act="idea" onclick="toggleQSec(this,'idea')">思路</button>` : '';
    const ideaHtml = q.idea ? `<div class="q-sec q-idea" hidden>${mdBlock(q.idea)}</div>` : '';
    return `<div class="q-card" id="q-${qid}" data-qno="${q.no}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindTag}</span>
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="收藏此题">${fav ? '⭐' : '☆'}</button>
        </div>
        <div class="q-body">${stem}${figHtml}${options}</div>
        <div class="q-ops">
            <button class="q-op" data-act="answer" onclick="toggleQSec(this,'answer')">查看答案</button>
            ${ideaBtn}
            <button class="q-op${hasNote ? ' has' : ''}" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>
        </div>
        ${ideaHtml}
        ${noteHtml}
        <div class="q-sec q-answer" hidden><div class="q-answer-body">${mdBlock(q.answer)}</div></div>
    </div>`;
}

function secTag(secIdx) {
    return ['一', '二', '三', '四', '五'][secIdx] || (secIdx + 1);
}

function renderCurrent() {
    const el = document.getElementById('examMain');
    if (!curPaper) { el.innerHTML = '<div class="loading">请选择一套卷</div>'; return; }
    const review = reviewGet(curPaper.id);
    const reviewFirst = review.trim().split('\n')[0].trim();
    let html = `<div class="paper-head">
        <div class="paper-head-top">
            <h1>${curPaper.title}</h1>
            <button class="review-btn${review.trim() ? ' has' : ''}" data-pid="${curPaper.id}" title="写试卷点评" onclick="openReviewPop('${curPaper.id}', this)">▦</button>
        </div>
        <div class="paper-meta">共 ${curPaper.sections.reduce((a, s) => a + s.questions.length, 0)} 题 · 满分 150 分</div>
        ${reviewFirst ? `<div class="paper-review-line">💬 ${esc(reviewFirst)}</div>` : ''}
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
    // 默认展开的笔记预览回填 [图:id] 贴图
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
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
    // 顶部栏整体折叠（恢复上次状态）
    restoreTopBar();
}

init();
