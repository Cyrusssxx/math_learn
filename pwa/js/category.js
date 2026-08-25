/* 真题分类浏览页：左=二级分类树（学科/章节，可折叠、含题数），右=选中章节的跨年真题
 * 分类口径：大观园「知识点/章节」体系（exam_categories.json 的 12 个二级章节）。
 * 复用 exam.js 的渲染 / 收藏辅助函数（独立副本，避免改动 exam.js 既有行为）。 */

const FAV_KEY = 'examFav';            // { qid: 1 }，qid = 套卷id-题no
const FAV_ONLY_KEY = 'examFavOnly';   // 是否只看收藏

// ============ 收藏存储 ============
function qidOf(paperId, no) { return paperId + '-' + no; }
function favGet() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || {}; } catch (e) { return {}; }
}
function favSave(obj) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(obj)); }
    catch (e) { console.error('收藏保存失败:', e); alert('收藏存储空间不足，保存失败。'); }
}
function isFav(qid) { return !!favGet()[qid]; }
function toggleFav(qid, btn) {
    const f = favGet();
    if (f[qid]) delete f[qid]; else f[qid] = 1;
    favSave(f);
    if (btn) {
        btn.classList.toggle('on', !!f[qid]);
        btn.textContent = f[qid] ? '⭐' : '☆';
        btn.title = f[qid] ? '取消收藏' : '收藏此题';
    }
    // 收藏过滤开启时，实时刷新分类树与题目列表
    if (favOnly) { renderTree(); renderMain(); }
}

let favOnly = localStorage.getItem(FAV_ONLY_KEY) === '1';
function toggleFavOnly() {
    favOnly = !favOnly;
    localStorage.setItem(FAV_ONLY_KEY, favOnly ? '1' : '0');
    const btn = document.getElementById('favOnly');
    if (btn) btn.classList.toggle('on', favOnly);
    renderTree();
    renderMain();
}

// ============ Markdown / KaTeX 渲染（与 exam.js 同源） ============
function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function mdInline(s) {
    return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}
function balanceDollars(s) {
    const n = (s.match(/\$\$/g) || []).length;
    return n % 2 === 0 ? s : s + '$$';
}
function mdBlock(s) {
    s = balanceDollars(s);
    const lines = s.split('\n');
    const out = [];
    let buf = null;
    for (const raw of lines) {
        const l = raw.trim();
        if (!l) { if (buf) buf += '\n'; continue; }
        if (buf === null && l.startsWith('$$') && !l.endsWith('$$')) { buf = l; continue; }
        if (buf !== null) {
            buf += '\n' + l;
            if (l.endsWith('$$')) { out.push('<p>' + mdInline(buf) + '</p>'); buf = null; }
            continue;
        }
        out.push('<p>' + mdInline(l) + '</p>');
    }
    if (buf) out.push('<p>' + mdInline(buf) + '</p>');
    return out.join('');
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

// ============ 配图单击放大（复用 exam.css 的 .zoom-overlay 遮罩） ============
function zoomAnsImg(img) {
    let ov = document.getElementById('zoomOverlay');
    if (!ov) {
        ov = document.createElement('div');
        ov.id = 'zoomOverlay';
        ov.className = 'zoom-overlay';
        ov.onclick = function () { ov.classList.remove('show'); };
        ov.innerHTML = '<img id="zoomImg" alt="放大图片">';
        const big = ov.querySelector('#zoomImg');
        big.onclick = function (e) { e.stopPropagation(); };
        document.body.appendChild(ov);
        document.addEventListener('keydown', function onEsc(e) {
            if (e.key === 'Escape') { ov.classList.remove('show'); document.removeEventListener('keydown', onEsc); }
        });
    }
    const big = document.getElementById('zoomImg');
    big.src = img.currentSrc || img.src;
    ov.classList.add('show');
}

// ============ 笔记（仅预览，复用 [图:id] 占位符；编辑在真题页进行） ============
function noteGet(qid) {
    try { return localStorage.getItem('examNote-' + qid) || ''; } catch (e) { return ''; }
}
function mdBlockWithImg(s) {
    return mdBlock(s).replace(/\[图:([a-z0-9]+)\]/g,
        (_, id) => `<img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)">`);
}
async function fillExamNoteImgs(root) {
    if (!root) return;
    const imgs = root.querySelectorAll('img.exam-note-img[data-img]');
    for (const img of imgs) {
        const id = img.dataset.img;
        const blob = await examImgGet(id);
        if (blob) img.src = URL.createObjectURL(blob);
        else img.replaceWith(document.createTextNode('[图片已丢失]'));
    }
}
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
function examImgGet(id) {
    return examImgDB().then(d => new Promise(res => {
        const rq = d.transaction('imgs').objectStore('imgs').get(id);
        rq.onsuccess = () => res(rq.result || null);
        rq.onerror = () => res(null);
    }));
}

// ============ 折叠段落（答案/思路/笔记） ============
function toggleQSec(btn, act) {
    const card = btn.closest('.q-card');
    if (!card) return;
    const sec = card.querySelector('.q-sec.q-' + act);
    if (!sec) return;
    const open = sec.hidden;
    sec.hidden = !open;
    btn.classList.toggle('on', open);
}

// ============ 数据 ============
let papers = [];
let cats = {};          // { id: {id,name,path,parent} }
let allEntries = [];    // { paper, secTitle, q, catId }
let curCat = null;      // 选中的章节 id
const collapsedSubjects = new Set();

// 由 section 标题判定题型（比 exam.js 的 no 区间启发式更稳：老卷填空/选择编号不固定）
function secKindLabel(t) {
    if (t.includes('选择题')) return '选择';
    if (t.includes('填空题')) return '填空';
    return '解答';
}

function buildEntries() {
    allEntries = [];
    for (const p of papers) {
        for (const sec of p.sections) {
            for (const q of sec.questions) {
                const cids = q.categoryIds || [];
                for (const cid of cids) {
                    allEntries.push({ paper: p, secTitle: sec.title, q, catId: cid });
                }
            }
        }
    }
}

function activeEntries() {
    if (!favOnly) return allEntries;
    return allEntries.filter(e => isFav(qidOf(e.paper.id, e.q.no)));
}

// 按「学科 → 章节」聚合，章节只保留有题数的；学科按 高数/线代/概率 固定顺序
function buildTree(entries) {
    const byCat = {};
    for (const e of entries) byCat[e.catId] = (byCat[e.catId] || 0) + 1;
    const subjMap = {};
    for (const id in cats) {
        const c = cats[id];
        const subj = (c.path || '').split(' / ')[0] || '其他';
        if (!subjMap[subj]) subjMap[subj] = [];
        subjMap[subj].push({ id: parseInt(id, 10), name: c.name, count: byCat[id] || 0 });
    }
    // 章节按题数降序（最常考的排前面），便于复习 prioritized
    for (const subj in subjMap) subjMap[subj].sort((a, b) => b.count - a.count);
    const order = ['高等数学', '线性代数', '概率统计'];
    return Object.keys(subjMap)
        .filter(subj => subjMap[subj].some(c => c.count > 0))   // 隐藏空章节的学科
        .map(subj => ({
            subject: subj,
            chapters: subjMap[subj].filter(c => c.count > 0)
        }))
        .sort((a, b) => {
            const ia = order.indexOf(a.subject), ib = order.indexOf(b.subject);
            return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
        });
}

// ============ 渲染：分类树 ============
function renderTree() {
    const entries = activeEntries();
    const el = document.getElementById('catTree');
    if (!entries.length) {
        el.innerHTML = `<div class="empty-tip">${favOnly
            ? '还没有收藏的题目。到真题页点卡片右上角 ☆ 收藏后，这里会按章节汇总。'
            : '暂无分类数据。'}</div>`;
        return;
    }
    const tree = buildTree(entries);
    el.innerHTML = tree.map((s, si) => {
        const open = !collapsedSubjects.has(s.subject);
        const total = s.chapters.reduce((a, c) => a + c.count, 0);
        return `<div class="paper-group">
            <div class="paper-group-head" onclick="toggleSubject('${s.subject.replace(/'/g, "\\'")}')">
                <span class="paper-group-arrow">${open ? '▼' : '▶'}</span>
                <span class="paper-group-name">${s.subject}</span>
                <span class="paper-group-count">${total}</span>
            </div>
            <div class="paper-group-body" style="display:${open ? 'block' : 'none'}">
                ${s.chapters.map(c => `
                    <button class="cat-chapter${String(curCat) === String(c.id) ? ' on' : ''}" onclick="selectCat(${c.id})">
                        <span class="cat-chapter-name">${c.name}</span>
                        <span class="cat-count">${c.count}</span>
                    </button>`).join('')}
            </div>
        </div>`;
    }).join('');
}

function toggleSubject(subj) {
    if (collapsedSubjects.has(subj)) collapsedSubjects.delete(subj);
    else collapsedSubjects.add(subj);
    renderTree();
}

function selectCat(id) {
    curCat = id;
    renderTree();
    renderMain();
}

// ============ 渲染：题目卡片 ============
function catCard(paper, secTitle, q) {
    const qid = qidOf(paper.id, q.no);
    const fav = isFav(qid);
    const kindLabel = secKindLabel(secTitle);
    const stem = mdBlock(q.stem || '');
    const figHtml = q.img
        ? `<img class="q-fig-img" src="${q.img}" alt="题${q.no}配图" loading="lazy" onclick="zoomAnsImg(this)">` +
          (q.img2 ? `<img class="q-fig-img" src="${q.img2}" alt="题${q.no}配图2" loading="lazy" onclick="zoomAnsImg(this)">` : '')
        : '';
    const options = (q.options && q.options.length)
        ? `<div class="q-options">${q.options.map(o => `<div class="q-opt">${mdInline(o)}</div>`).join('')}</div>`
        : '';
    const ideaHtml = q.idea ? `<div class="q-sec q-idea" hidden>${mdBlock(q.idea)}</div>` : '';
    const ideaBtn = q.idea ? `<button class="q-op" data-act="idea" onclick="toggleQSec(this,'idea')">思路</button>` : '';
    const note = noteGet(qid);
    const hasNote = !!note.trim();
    const noteHtml = hasNote ? `<div class="q-sec q-note"><div class="q-note-preview">${mdBlockWithImg(note)}</div></div>` : '';
    const noteBtn = hasNote ? `<button class="q-op has" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>` : '';
    const paperLink = 'exam.html?paper=' + encodeURIComponent(paper.id);
    return `<div class="q-card" id="q-${qid}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindLabel}</span>
            <span class="q-year"><a href="${paperLink}" title="在真题页打开此套卷">${paper.year}年</a></span>
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="收藏此题">${fav ? '⭐' : '☆'}</button>
        </div>
        <div class="q-body">${stem}${figHtml}${options}</div>
        <div class="q-ops">
            <button class="q-op" data-act="answer" onclick="toggleQSec(this,'answer')">查看答案</button>
            ${ideaBtn}${noteBtn}
        </div>
        ${ideaHtml}${noteHtml}
        <div class="q-sec q-answer" hidden><div class="q-answer-body">${mdBlock(q.answer || '')}</div></div>
    </div>`;
}

// ============ 渲染：主区 ============
function renderMain() {
    const el = document.getElementById('catMain');
    if (curCat == null) {
        el.innerHTML = `<div class="cat-empty">← 选择左侧章节，查看该考点的历年真题</div>`;
        return;
    }
    const entries = activeEntries().filter(e => String(e.catId) === String(curCat));
    const c = cats[curCat];
    entries.sort((a, b) => parseInt(b.paper.year, 10) - parseInt(a.paper.year, 10));
    if (!entries.length) {
        el.innerHTML = `<div class="paper-head"><h1>${c ? c.name : curCat}</h1></div>` +
            `<div class="empty-tip">${favOnly ? '该章节下没有收藏的题目。' : '暂无题目。'}</div>`;
        return;
    }
    const years = new Set(entries.map(e => e.paper.year)).size;
    let html = `<div class="paper-head">
        <h1>${c ? c.name : curCat}</h1>
        <div class="paper-meta">共 ${entries.length} 题 · 跨 ${years} 年</div>
    </div>`;
    if (favOnly) html += `<div class="cat-filter-tip">⭐ 收藏过滤中：仅显示已收藏题目</div>`;
    entries.forEach(e => { html += catCard(e.paper, e.secTitle, e.q); });
    el.innerHTML = html;
    renderMath(el);
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

// ============ 初始化 ============
async function init() {
    const [er, cr] = await Promise.all([
        fetch('data/exam.json'),
        fetch('data/exam_categories.json'),
    ]);
    if (!er.ok) throw new Error('加载真题失败: ' + er.status);
    if (!cr.ok) throw new Error('加载分类失败: ' + cr.status);
    papers = await er.json();
    cats = await cr.json();
    const btn = document.getElementById('favOnly');
    if (btn) btn.classList.toggle('on', favOnly);
    buildEntries();
    renderTree();
    renderMain();
}

init().catch(e => {
    const el = document.getElementById('catMain');
    if (el) el.innerHTML = '<div class="empty-tip">加载失败：' + esc(e.message) + '</div>';
    console.error(e);
});
