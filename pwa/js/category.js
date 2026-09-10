/* 真题分类浏览页：左=二级分类树（学科/章节，可折叠、含题数），右=选中章节的跨年真题
 * 分类口径：大观园「知识点/章节」体系（exam_categories.json 的 12 个二级章节）。
 * 复用 exam.js 的渲染 / 收藏辅助函数（独立副本，避免改动 exam.js 既有行为）。 */

const FAV_KEY = 'examFav';            // { qid: 1 }，qid = 套卷id-题no
const FAV_ONLY_KEY = 'examFavOnly';   // 是否只看收藏（常量保留，界面已由三选筛选替代）
const EXAM_STATUS_KEY = 'examStatus';   // { qid: 'unfamiliar' | 'unknown' }：不熟/不会掌握度标记（互斥）

// ============ 收藏存储 ============
function qidOf(paperId, no) { return paperId + '-' + no; }
function favGet() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || {}; } catch (e) { return {}; }
}
function favSave(obj) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(obj)); }
    catch (e) { console.error('收藏保存失败:', e); alert('收藏存储空间不足，保存失败。'); }
}
// ============ 掌握度标记（不熟/不会，互斥单选；与收藏独立） ============
function statusGet() {
    try { return JSON.parse(localStorage.getItem(EXAM_STATUS_KEY)) || {}; } catch (e) { return {}; }
}
function statusSave(obj) {
    try { localStorage.setItem(EXAM_STATUS_KEY, JSON.stringify(obj)); } catch (e) { }
}
function statusOf(qid) { return statusGet()[qid] || null; }
// 互斥切换：v='unfamiliar'|'unknown'；同值再次调用则清除（不熟 ⇄ 不会 ⇄ 无）
function toggleStatus(qid, v) {
    const s = statusGet();
    if (s[qid] === v) delete s[qid]; else s[qid] = v;
    statusSave(s);
    return s[qid] || null;
}
function isFav(qid) { return !!favGet()[qid]; }
function favTime(qid) {
    const v = favGet()[qid];
    return (v && typeof v === 'object') ? (v.t || 0) : 0;
}
function fmtFavTime(ts) {
    if (!ts) return '';
    const d = new Date(ts), p = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
}
function fmtFavShort(ts) {   // 星标旁的短日期：月-日
    if (!ts) return '';
    const d = new Date(ts), p = n => String(n).padStart(2, '0');
    return p(d.getMonth() + 1) + '-' + p(d.getDate());
}
// 一次性迁移：旧格式收藏（{qid:1}，无时间戳）补上「今天」的时间并写回存储
function migrateFavTimes() {
    const f = favGet();
    let changed = false;
    for (const k in f) {
        if (!f[k] || typeof f[k] !== 'object') { f[k] = { t: Date.now() }; changed = true; }
    }
    if (changed) favSave(f);
}
migrateFavTimes();
function toggleFav(qid, btn) {
    const f = favGet();
    if (f[qid]) delete f[qid]; else f[qid] = { t: Date.now() };
    favSave(f);
    if (btn) {
        const on = !!f[qid];
        btn.classList.toggle('on', on);
        btn.textContent = on ? '⭐' : '☆';
        btn.title = on ? (favTime(qid) ? '收藏于 ' + fmtFavTime(favTime(qid)) : '已收藏（时间未知）') : '收藏此题';
        // 就地同步星标左侧的日期徽标
        const card = btn.closest('.q-card');
        if (card) {
            let badge = card.querySelector('.q-fav-date');
            const t = favTime(qid);
            if (on && t) {
                if (!badge) {
                    badge = document.createElement('span');
                    badge.className = 'q-fav-date';
                    btn.parentNode.insertBefore(badge, btn);
                }
                badge.textContent = fmtFavShort(t);
                badge.title = '收藏于 ' + fmtFavTime(t);
            } else if (badge) badge.remove();
        }
    }
    // 任一筛选开启时，实时刷新分类树与题目列表
    if (markSel.mix || markSel.unknown) { renderTree(); renderMain(); }
}

// 掌握度/收藏多选筛选（默认全选，并集去重；收藏/不熟/不会互不归属）
let markSel = { mix: false, unknown: false }; // 「收藏+不熟」合并 / 「不会」；默认都不选 = 显示全部
function toggleMark(m) {
    markSel[m] = !markSel[m];
    document.querySelectorAll('.cat-mark').forEach(b => b.classList.toggle('on', markSel[b.dataset.m]));
    const sy = window.scrollY;   // 保持滚动位置，避免树高变化导致弹跳
    renderTree();
    renderMain();
    requestAnimationFrame(() => window.scrollTo(0, sy));
}

// ============ 合并数据：现有数二真题 + 大观园数二真题（统一一棵分类树） ============
let bankItems = [];      // 大观园数二真题（categoryIds 已映射到统一分类体系：知识点 L2 或 年份节点）

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
        // 裸 "$$" 独占一行也要开块：'$$'.endsWith('$$') 恒为真，旧条件会让多行显示块整体失效（与 exam.js 同步修）
        if (buf === null && l.startsWith('$$') && (!l.endsWith('$$') || l === '$$')) { buf = l; continue; }
        if (buf !== null) {
            buf += '\n' + l;
            if (l.endsWith('$$')) { out.push('<p>' + mdInline(buf) + '</p>'); buf = null; }
            continue;
        }
        // 笔记标题令牌（<h1>/<h2>）独占整行时作为块级标题输出，不放进 <p>
        if (l.startsWith('<h1>') || l.startsWith('<h2>')) {
            out.push(mdInline(l));
        } else {
            out.push('<p>' + mdInline(l) + '</p>');
        }
    }
    if (buf) out.push('<p>' + mdInline(buf) + '</p>');
    // 笔记令牌还原（与 exam.js 对齐：高亮/字色 → 行内标签，粗体/斜体 → 行内标签，H1/H2 → 块级标题）
    return out.join('')
        .replace(/&lt;h:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/h&gt;/g, '<mark class="note-hl" style="background:$1">$2</mark>')
        .replace(/&lt;c:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/c&gt;/g, '<span style="color:$1">$2</span>')
        .replace(/&lt;b&gt;([\s\S]*?)&lt;\/b&gt;/g, '<b>$1</b>')
        .replace(/&lt;i&gt;([\s\S]*?)&lt;\/i&gt;/g, '<i>$1</i>')
        .replace(/&lt;h1&gt;([\s\S]*?)&lt;\/h1&gt;/g, '<h1>$1</h1>')
        .replace(/&lt;h2&gt;([\s\S]*?)&lt;\/h2&gt;/g, '<h2>$1</h2>')
        .replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (_, alt, src) =>
            /^data\/img\/[a-zA-Z0-9_./-]+$/.test(src)
                ? `<span class="exam-fig-wrap"><img class="exam-fig" src="${src}" alt="${String(alt).replace(/"/g, '&quot;')}" onclick="zoomAnsImg(this)" loading="lazy"></span>`
                : '');
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
// 预览态（只读展示）不带删除按钮——防误点丢图（与 exam.js 同步）
function mdBlockWithImg(s) {
    return mdBlock(s).replace(/\[图:([a-z0-9]+)\]/g,
        (_, id) => `<span class="exam-note-img-wrap"><img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)"></span>`);
}
// 分类页（只读预览）单图删除：删 IndexedDB + 删文本占位 + 重渲染预览 + 同步「笔记」标记
function delExamNoteImg(id, btn) {
    const wrap = btn.closest('.q-note');
    if (!wrap) return;
    const qid = wrap.dataset.qid;
    if (!qid) return;
    let v = noteGet(qid);
    const re = new RegExp('\\[图:' + id + '\\]', 'g');
    // 只摘掉这一个图片令牌；严禁压缩空格/换行（\s{2,} 会把用户的段落空行和缩进空格全吃掉）
    v = v.replace(re, '');
    try { localStorage.setItem('examNote-' + qid, v); } catch (e) { }
    examImgDel([id]);
    const pv = wrap.querySelector('.q-note-preview');
    if (pv) pv.innerHTML = mdBlockWithImg(v);
    const opBtn = wrap.closest('.q-card') && wrap.closest('.q-card').querySelector('[data-act="note"]');
    if (opBtn) opBtn.classList.toggle('has', !!v.trim());
    noteHint(btn, '已删除图片');
}
function noteHint(anchor, msg) {
    const sec = anchor && anchor.closest && anchor.closest('.q-note');
    const el = sec && sec.querySelector('.q-note-hint');
    if (!el) return;
    if (!msg) { el.textContent = ''; el.classList.remove('show'); return; }
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.classList.remove('show'); }, 2000);
}
async function fillExamNoteImgs(root) {
    if (!root) return;
    const imgs = root.querySelectorAll('img.exam-note-img[data-img]');
    for (const img of imgs) {
        if (img.src && img.src.startsWith('blob:')) continue;
        let blob = await examImgGet(img.dataset.img);
        if (!blob) {
            await new Promise(r => setTimeout(r, 300));
            blob = await examImgGet(img.dataset.img);
        }
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
function examImgDel(ids) {
    if (!ids || !ids.length) return Promise.resolve();
    return examImgDB().then(d => new Promise(res => {
        const tx = d.transaction('imgs', 'readwrite');
        ids.forEach(id => tx.objectStore('imgs').delete(id));
        tx.oncomplete = res; tx.onerror = res;
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
    if (open) {                 // 展开时内容刚可见，需补调 KaTeX 渲染 $$ 块
        renderMath(sec);
        if (act === 'note') fillExamNoteImgs(sec.querySelector('.q-note-preview'));
    }
}

// 一键展开/收起当前列表所有题卡的答案
let allAnsOpen = false;
function toggleAllAnswers(btn) {
    allAnsOpen = !allAnsOpen;
    const root = document.getElementById('catMain');
    if (!root) return;
    root.querySelectorAll('.q-card').forEach(card => {
        const sec = card.querySelector('.q-answer');
        const b = card.querySelector('.q-op[data-act="answer"]');
        if (sec) sec.hidden = !allAnsOpen;
        if (b) {
            b.classList.toggle('on', allAnsOpen);
            b.textContent = allAnsOpen ? '收起答案' : '查看答案';
        }
    });
    // 批量展开后内容刚可见，需补调 KaTeX 渲染 $$ 块
    renderMath(root);
    root.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
    btn.classList.toggle('on', allAnsOpen);
    btn.textContent = allAnsOpen ? '🔽 收起全部答案' : '🔼 展开全部答案';
}

// ============ 数据 ============
let papers = [];
let cats = {};          // { id: {id,name,path,parent} }
let allEntries = [];    // { paper, secTitle, q, catId }
let curCat = null;      // 选中的知识点(L3) id
const collapsedSubjects = new Set();   // 折叠的学科
const collapsedChapters = new Set();   // 折叠的章节
// 刷新保持：选中分类 + 树折叠态（localStorage 持久化）
const CAT_STATE_KEY = 'catViewState';
try {
    const st = JSON.parse(localStorage.getItem(CAT_STATE_KEY) || '{}');
    if (st.curCat !== undefined && st.curCat !== null) curCat = st.curCat;
    (st.collapsedSubjects || []).forEach(s => collapsedSubjects.add(s));
    (st.collapsedChapters || []).forEach(c => collapsedChapters.add(c));
} catch (e) { }
function saveCatState() {
    try {
        localStorage.setItem(CAT_STATE_KEY, JSON.stringify({
            curCat,
            collapsedSubjects: [...collapsedSubjects],
            collapsedChapters: [...collapsedChapters],
        }));
    } catch (e) { }
}

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
    // 合并大观园数二真题进同一棵分类树
    for (const e of bankItems) {
        for (const cid of e.catIds) {
            allEntries.push({ paper: e.paper, secTitle: '', q: e.q, catId: cid });
        }
    }
}

function activeEntries() {
    // 筛选并集：mix=收藏∪不熟，unknown=不会；全部未选 → 不过滤（显示全部真题）
    if (!markSel.mix && !markSel.unknown) return allEntries;
    const st = statusGet();
    return allEntries.filter(e => {
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null;
        const mix = markSel.mix && (isFav(qid) || s === 'unfamiliar');
        const unk = markSel.unknown && s === 'unknown';
        return mix || unk;
    });
}

// 清洗标签：去 LaTeX $...$、去空白、截断（用于分类树显示）
function cleanLabel(s) {
    return (s || '').replace(/\$[^$]*\$/g, '').replace(/\$/g, '').replace(/\s+/g, '').slice(0, 22);
}

// 按「学科 → 章节 → 知识点(L3)」三级聚合；只保留有题数的节点；subject 固定序，chapter/leaf 按题数降序
function buildTree(entries) {
    const byCat = {};
    for (const e of entries) byCat[e.catId] = (byCat[e.catId] || 0) + 1;
    const subjMap = {};   // 学科名 -> { chapters: { chId: {id,name,display,count,leaves:[]} } }
    for (const id in cats) {
        const c = cats[id];
        if (c.level !== 2) continue;                 // 仅处理 L3 知识点叶子
        const ch = cats[String(c.parentId)];
        if (!ch || ch.level !== 1) continue;
        const subj = cats[String(ch.parentId)];
        if (!subj) continue;
        const cnt = byCat[c.id] || 0;
        if (cnt <= 0) continue;
        if (!subjMap[subj.name]) subjMap[subj.name] = { chapters: {} };
        const cm = subjMap[subj.name].chapters;
        if (!cm[ch.id]) cm[ch.id] = { id: ch.id, name: ch.name, display: ch.display, count: 0, leaves: [] };
        cm[ch.id].count += cnt;
        cm[ch.id].leaves.push({ id: c.id, name: c.name, display: c.display, count: cnt });
    }
    const order = ['高等数学', '线性代数', '概率统计'];
    const subs = Object.keys(subjMap)
        .filter(s => Object.keys(subjMap[s].chapters).length)
        .sort((a, b) => { const ia = order.indexOf(a), ib = order.indexOf(b); return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib); });
    return subs.map(s => {
        const chapters = Object.values(subjMap[s].chapters).sort((a, b) => b.count - a.count);
        chapters.forEach(ch => ch.leaves.sort((a, b) => b.count - a.count));
        return { subject: s, chapters };
    });
}

// ============ 渲染：三级分类树 ============
function renderTree() {
    const entries = activeEntries();
    const el = document.getElementById('catTree');
    if (!entries.length) {
        el.innerHTML = '<div class="empty-tip">当前筛选条件下没有题目。到真题页点 ☆ 收藏，或点题右侧「不熟/不会」打标记后，这里会按章节汇总。</div>';
        return;
    }
    const tree = buildTree(entries);
    el.innerHTML = tree.map(s => {
        const open = !collapsedSubjects.has(s.subject);
        const total = s.chapters.reduce((a, c) => a + c.count, 0);
        return `<div class="paper-group">
            <div class="paper-group-head" onclick="toggleSubject('${s.subject.replace(/'/g, "\\'")}')">
                <span class="paper-group-arrow">${open ? '▼' : '▶'}</span>
                <span class="paper-group-name">${s.subject}</span>
                <span class="paper-group-count">${total}</span>
            </div>
            <div class="paper-group-body" style="display:${open ? 'block' : 'none'}">
                ${s.chapters.map(ch => {
                    const copen = !collapsedChapters.has(ch.id);
                    const leafOn = String(curCat) === String(ch.id);
                    return `<div class="cat-chapter">
                        <div class="cat-chapter-head${leafOn ? ' on' : ''}" onclick="toggleChapter(${ch.id})">
                            <span class="cat-chapter-arrow">${copen ? '▾' : '▸'}</span>
                            <span class="cat-chapter-name">${ch.display || ch.name}</span>
                            <span class="cat-count">${ch.count}</span>
                        </div>
                        <div class="cat-chapter-body" style="display:${copen ? 'block' : 'none'}">
                            ${ch.leaves.map(l => `<button class="cat-leaf${String(curCat) === String(l.id) ? ' on' : ''}" onclick="selectCat(${l.id})" title="${l.name}">
                                <span class="cat-leaf-name">${l.display || l.name}</span>
                                <span class="cat-count">${l.count}</span>
                            </button>`).join('')}
                        </div>
                    </div>`;
                }).join('')}
            </div>
        </div>`;
    }).join('');
}

function toggleSubject(subj) {
    if (collapsedSubjects.has(subj)) collapsedSubjects.delete(subj);
    else collapsedSubjects.add(subj);
    saveCatState();
    renderTree();
}

function toggleChapter(id) {
    if (collapsedChapters.has(id)) collapsedChapters.delete(id);
    else collapsedChapters.add(id);
    saveCatState();
    renderTree();
}

function selectCat(id) {
    curCat = id;
    saveCatState();
    renderTree();
    renderMain();
}

// ============ 渲染：题目卡片 ============
function catCard(paper, secTitle, q) {
    const qid = qidOf(paper.id, q.no);
    const fav = isFav(qid);
    const st = statusOf(qid);
    const kindLabel = (q.options && q.options.length) || q.type === 'choice' ? '选择'
        : q.type === 'blank' ? '填空' : secKindLabel(secTitle);
    const stem = mdBlock(q.stem || '');
    const figHtml = q.img
        ? `<img class="q-fig-img" src="${q.img}" alt="题${q.no}配图" loading="lazy" onclick="zoomAnsImg(this)">` +
          (q.img2 ? `<img class="q-fig-img" src="${q.img2}" alt="题${q.no}配图2" loading="lazy" onclick="zoomAnsImg(this)">` : '')
        : '';
    const options = (q.options && q.options.length)
        ? `<div class="q-options">${q.options.map((o, i) => `<div class="q-opt">${!q.options.some(x => /^\([A-D]\)/.test(x)) ? `<span class="opt-label">${'ABCD'[i]}</span>` : ''}${mdInline(o)}</div>`).join('')}</div>`
        : '';
    const ideaHtml = q.idea ? `<div class="q-sec q-idea" data-copy-md="${copyMdAttr(q.idea)}" hidden>${mdBlock(q.idea)}</div>` : '';
    const ideaBtn = q.idea ? `<button class="q-op" data-act="idea" onclick="toggleQSec(this,'idea')">思路</button>` : '';
    const note = noteGet(qid);
    const hasNote = !!note.trim();
    const hasImg = /\[图:[a-z0-9]+\]/.test(note);
    const noteHtml = hasNote ? `<div class="q-sec q-note${hasImg ? ' has-img' : ''}" data-qid="${qid}"><div class="q-note-preview">${mdBlockWithImg(note)}</div><div class="q-note-hint"></div></div>` : '';
    const noteBtn = hasNote ? `<button class="q-op has" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>` : '';
    const paperLink = 'exam.html?paper=' + encodeURIComponent(paper.id);
    const yearHtml = paper.id === 'bank'
        ? `<span class="q-year"><span class="q-year-tag">${paper.year}年</span></span>`
        : `<span class="q-year"><a href="${paperLink}" title="在真题页打开此套卷">${paper.year}年</a></span>`;
    return `<div class="q-card" id="q-${qid}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindLabel}</span>
            ${fav ? `<span class="q-mark-chip m-fav" title="已收藏">📥</span>` : ''}
            ${st === 'unfamiliar' ? '<span class="q-mark-chip m-unfam" title="不熟">🟡 不熟</span>' : ''}
            ${st === 'unknown' ? '<span class="q-mark-chip m-unk" title="不会">🔴 不会</span>' : ''}
            ${fav && favTime(qid) ? `<span class="q-fav-date" title="收藏于 ${fmtFavTime(favTime(qid))}">${fmtFavShort(favTime(qid))}</span>` : ''}
            ${yearHtml}
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="${fav ? (favTime(qid) ? '收藏于 ' + fmtFavTime(favTime(qid)) : '已收藏') : '收藏此题'}">${fav ? '⭐' : '☆'}</button>
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
    // 排序：有收藏时间的按收藏时间倒序靠前，其余按年份倒序
    entries.sort((a, b) => {
        const ta = favTime(qidOf(a.paper.id, a.q.no));
        const tb = favTime(qidOf(b.paper.id, b.q.no));
        if (ta && tb) return tb - ta;
        return parseInt(b.paper.year, 10) - parseInt(a.paper.year, 10);
    });
    if (!entries.length) {
        el.innerHTML = `<div class="paper-head"><h1>${c ? (c.display || c.name) : curCat}</h1><div class="paper-sub">${c ? c.path : ''}</div></div>` +
            `<div class="empty-tip">该章节下当前筛选没有匹配题目。试试切换「收藏/不熟/不会」筛选。</div>`;
        return;
    }
    const years = new Set(entries.map(e => e.paper.year)).size;
    let html = `<div class="paper-head">
        <h1>${c ? c.display : curCat}</h1>
        <div class="paper-sub">${c ? c.path : ''}</div>
        <div class="paper-meta">共 ${entries.length} 题 · 跨 ${years} 年</div>
        <button class="all-ans-btn" id="allAnsBtn" onclick="toggleAllAnswers(this)">🔼 展开全部答案</button>
    </div>`;
    const markNames = { mix: '📥收藏+🟡不熟', unknown: '🔴不会' };
    const activeMark = Object.keys(markSel).filter(k => markSel[k]);
    if (activeMark.length) html += `<div class="cat-filter-tip">筛选：${activeMark.map(k => markNames[k]).join(' / ')}</div>`;
    entries.forEach(e => { html += catCard(e.paper, e.secTitle, e.q); });
    el.innerHTML = html;
    renderMath(el);
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

// ============ 初始化 ============
async function init() {
    const [er, cr, br] = await Promise.all([
        fetch('data/exam.json'),
        fetch('data/exam_categories.json'),
        fetch('data/bank_questions.json').catch(() => null),
    ]);
    if (!er.ok) throw new Error('加载真题失败: ' + er.status);
    if (!cr.ok) throw new Error('加载分类失败: ' + cr.status);
    papers = await er.json();
    cats = await cr.json();
    // 大观园真题库（categoryIds 已映射到统一分类体系，与 exam.json 合并一棵树）
    if (br && br.ok) {
        const bq = await br.json();
        const examYears = new Set(papers.map(p => String(p.year)));
        bankItems = (bq.items || []).map((it, idx) => {
            const ym = /^(19\d\d|20\d\d)/.exec(it.source || '');
            const q = Object.assign({}, it, {
                no: idx + 1,
                idea: it.explanation || '',   // 大观园解析 → 分类页「解析」按钮
            });
            return { paper: { id: 'bank', year: ym ? ym[1] : '', title: it.source || '大观园真题' }, q, catIds: it.categoryIds || [] };
        })
        // 同题去重：source 为「(YY)YY 数二(真题)」且现有已有同年套卷 → 隐藏大观园版（math-note 版已在），避免同题两版；1987-1999 等老年份与合卷题保留
        .filter(e => {
            const m = /^\(?(19\d\d|20\d\d) 数二(真题)?\)?$/.exec(e.q.source || '');
            return !(m && examYears.has(m[1]));
        });
    }
    document.querySelectorAll('.cat-mark').forEach(b => b.classList.toggle('on', markSel[b.dataset.m]));
    // 恢复的选中分类若已不在分类表里（数据变更），清掉防悬空
    if (curCat !== null && !cats[String(curCat)]) { curCat = null; saveCatState(); }
    buildEntries();
    renderTree();
    renderMain();
}

init().catch(e => {
    const el = document.getElementById('catMain');
    if (el) el.innerHTML = '<div class="empty-tip">加载失败：' + esc(e.message) + '</div>';
    console.error(e);
});
