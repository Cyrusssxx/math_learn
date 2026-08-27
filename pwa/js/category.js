/* 真题分类浏览页：左=二级分类树（学科/章节，可折叠、含题数），右=选中章节的跨年真题
 * 分类口径：大观园「知识点/章节」体系（exam_categories.json 的 12 个二级章节）。
 * 复用 exam.js 的渲染 / 收藏辅助函数（独立副本，避免改动 exam.js 既有行为）。 */

const FAV_KEY = 'examFav';            // { qid: {t: 时间戳} }，qid = 套卷id-题no

// ============ 悬浮分类抽屉 ============
function toggleCatDrawer() {
    const drawer = document.getElementById('catDrawer');
    const overlay = document.getElementById('catDrawerOverlay');
    const trigger = document.getElementById('catDrawerTrigger');
    const isOpen = drawer.classList.toggle('open');
    overlay.classList.toggle('open', isOpen);
    trigger.classList.toggle('hidden', isOpen);
}
function closeCatDrawer() {
    document.getElementById('catDrawer').classList.remove('open');
    document.getElementById('catDrawerOverlay').classList.remove('open');
    document.getElementById('catDrawerTrigger').classList.remove('hidden');
}

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
    // 收藏夹视图下，实时刷新列表（取消收藏即移出）
    if (viewMode === 'fav') renderMain();
}

let viewMode = 'cat';   // 'cat' | 'fav'：分类浏览 / 收藏夹
function toggleFavView() {
    viewMode = (viewMode === 'fav') ? 'cat' : 'fav';
    const btn = document.getElementById('favOnly');
    if (btn) btn.classList.toggle('on', viewMode === 'fav');
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
        (_, id) => `<span class="exam-note-img-wrap"><img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)"><button type="button" class="exam-note-img-del" title="删除图片" onclick="delExamNoteImg('${id}', this)">×</button></span>`);
}
// 分类页（只读预览）单图删除：删 IndexedDB + 删文本占位 + 重渲染预览 + 同步「笔记」标记
function delExamNoteImg(id, btn) {
    const wrap = btn.closest('.q-note');
    if (!wrap) return;
    const qid = wrap.dataset.qid;
    if (!qid) return;
    let v = noteGet(qid);
    const re = new RegExp('\\[图:' + id + '\\]', 'g');
    v = v.replace(re, '').replace(/\s{2,}/g, ' ').trim();
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
    if (open) {
        renderMath(sec);
        fillExamNoteImgs(sec);
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
    if (allAnsOpen) {
        renderMath(root);
        fillExamNoteImgs(root);
    }
    btn.classList.toggle('on', allAnsOpen);
    btn.textContent = allAnsOpen ? '🔽 收起全部答案' : '🔼 展开全部答案';
}

// ============ 数据 ============
let papers = [];
let cats = {};          // { id: {id,name,path,parent} }
let allEntries = [];    // { paper, secTitle, q, catId }
let curCat = null;      // 选中的分类节点 id（任意层级）

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
    return allEntries;
}

// 清洗标签：去 LaTeX $...$、去空白、截断（用于分类树显示）
function cleanLabel(s) {
    return (s || '').replace(/\$[^$]*\$/g, '').replace(/\$/g, '').replace(/\s+/g, '').slice(0, 22);
}

// ============ 完整多级分类树（参照大观园层级） ============
// 由 exam_categories.json 的 parentId 还原 L0~L8 整棵树；
// 题数从叶子向上累计：父节点显示其整棵子树的题数（含后代）。
let childrenMap = {};   // parentId(str) -> [childId]
let directCount = {};   // catId(str) -> 直接挂在该节点的题数
let subCount = {};      // catId(str) -> 子树题数（自身 + 全部后代）
const collapsedNodes = new Set();   // 收起（不显示子节点）的节点 id

function buildTreeData() {
    childrenMap = {};
    for (const id in cats) {
        const pid = cats[id].parentId;
        if (pid != null) {
            const pk = String(pid);
            (childrenMap[pk] || (childrenMap[pk] = [])).push(id);
        }
    }
    directCount = {};
    for (const e of allEntries) {
        const cid = String(e.catId);
        if (cats[cid]) directCount[cid] = (directCount[cid] || 0) + 1;
    }
    subCount = {};
    const propagate = (id) => {
        let total = directCount[id] || 0;
        for (const ch of (childrenMap[id] || [])) total += propagate(ch);
        subCount[id] = total;
        return total;
    };
    for (const id in cats) if (cats[id].level === 0) propagate(id);
    // 默认展开到 L1，L2 及以上收起，避免初始过长
    collapsedNodes.clear();
    for (const id in cats) if ((cats[id].level || 0) >= 2) collapsedNodes.add(id);
}

// 取某节点整棵子树（含自身）的所有 id，用于选中节点时拉取其全部题目
function subIdsOf(id) {
    const start = String(id);
    const out = [start];
    const stack = [start];
    while (stack.length) {
        const cur = stack.pop();
        for (const ch of (childrenMap[cur] || [])) { out.push(String(ch)); stack.push(String(ch)); }
    }
    return out;
}

// ============ 渲染：多级分类树（递归，可逐级展开） ============
function treeNodeHtml(id, depth) {
    const cnt = subCount[id] || 0;
    if (!cnt) return '';                     // 空分支不渲染
    const c = cats[id];
    const kids = (childrenMap[id] || []).filter(k => (subCount[k] || 0) > 0);
    const isLeafNode = kids.length === 0;
    const collapsed = collapsedNodes.has(id);
    const selected = String(curCat) === String(id);
    const indent = 8 + depth * 15;
    const arrow = isLeafNode
        ? '<span class="tree-arrow tree-arrow-empty"></span>'
        : `<span class="tree-arrow" onclick="toggleNode('${id}',event)">${collapsed ? '▸' : '▾'}</span>`;
    let html = `<div class="tree-node${selected ? ' on' : ''}" style="padding-left:${indent}px" title="${(c.path || c.name).replace(/"/g, '&quot;')}">
        ${arrow}
        <span class="tree-name" onclick="selectCat('${id}')">${c.display || c.name}</span>
        <span class="cat-count">${cnt}</span>
    </div>`;
    if (!isLeafNode && !collapsed) {
        for (const k of kids) html += treeNodeHtml(k, depth + 1);
    }
    return html;
}

function renderTree() {
    const el = document.getElementById('catTree');
    if (!el) return;
    if (!allEntries.length) {
        el.innerHTML = `<div class="empty-tip">暂无分类数据。</div>`;
        return;
    }
    // 仅渲染有题数的 L0 根（空根 / 归档分类 / 数一数三等自动隐藏）
    const order = ['高等数学', '线性代数', '概率统计', '事件与概率', '一维随机变量', '二维随机变量', '数字特征', '大数定律中心极限定理', '统计初步'];
    const roots = Object.keys(cats).filter(id => (cats[id].level || 0) === 0 && (subCount[id] || 0) > 0);
    roots.sort((a, b) => {
        const ia = order.indexOf(cats[a].name), ib = order.indexOf(cats[b].name);
        const ra = ia < 0 ? 99 : ia, rb = ib < 0 ? 99 : ib;
        return ra - rb || cats[a].name.localeCompare(cats[b].name, 'zh');
    });
    el.innerHTML = roots.map(id => `<div class="tree-root">${treeNodeHtml(id, 0)}</div>`).join('')
        || `<div class="empty-tip">暂无分类数据。</div>`;
}

// 展开/收起某节点（箭头按钮触发，阻止冒泡避免误选中）
function toggleNode(id, ev) {
    if (ev) ev.stopPropagation();
    if (collapsedNodes.has(id)) collapsedNodes.delete(id); else collapsedNodes.add(id);
    renderTree();
}

function selectCat(id) {
    viewMode = 'cat';
    curCat = String(id);
    // 自动展开从根到所选节点的路径，确保高亮节点在抽屉内可见
    let cur = cats[curCat];
    while (cur && cur.parentId != null) {
        collapsedNodes.delete(String(cur.parentId));
        cur = cats[String(cur.parentId)];
    }
    renderTree();
    renderMain();
    closeCatDrawer();   // 选中知识点后自动收起抽屉
    const fb = document.getElementById('favOnly');
    if (fb) fb.classList.remove('on');
}

// ============ 渲染：题目卡片 ============
function catCard(paper, secTitle, q, catLabel) {
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
    const noteHtml = hasNote ? `<div class="q-sec q-note" data-qid="${qid}"><div class="q-note-preview">${mdBlockWithImg(note)}</div><div class="q-note-hint"></div></div>` : '';
    const noteBtn = hasNote ? `<button class="q-op has" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>` : '';
    const paperLink = 'exam.html?paper=' + encodeURIComponent(paper.id);
    const tagHtml = catLabel ? `<span class="q-cat-tag" title="所属考点">${catLabel}</span>` : '';
    return `<div class="q-card" id="q-${qid}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindLabel}</span>
            ${tagHtml}
            ${fav && favTime(qid) ? `<span class="q-fav-date" title="收藏于 ${fmtFavTime(favTime(qid))}">${fmtFavShort(favTime(qid))}</span>` : ''}
            <span class="q-year"><a href="${paperLink}" title="在真题页打开此套卷">${paper.year}年</a></span>
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
    if (viewMode === 'fav') { renderFavView(el); return; }
    if (curCat == null) {
        el.innerHTML = `<div class="cat-empty">点击下方 📂 按钮展开分类抽屉，选择考点查看历年真题</div>`;
        return;
    }
    // 选中任意层级节点：拉取其整棵子树（含自身）的题目，同一题被多个子分类引用时去重
    const subSet = new Set(subIdsOf(String(curCat)));
    const seen = new Set();
    const entries = [];
    for (const e of activeEntries()) {
        if (!subSet.has(String(e.catId))) continue;
        const qid = qidOf(e.paper.id, e.q.no);
        if (seen.has(qid)) continue;
        seen.add(qid);
        entries.push(e);
    }
    const c = cats[curCat];
    entries.sort((a, b) => parseInt(b.paper.year, 10) - parseInt(a.paper.year, 10));
    if (!entries.length) {
        el.innerHTML = `<div class="paper-head"><h1>${c ? c.display : curCat}</h1><div class="paper-sub">${c ? c.path : ''}</div></div>` +
            `<div class="empty-tip">暂无题目。</div>`;
        return;
    }
    const years = new Set(entries.map(e => e.paper.year)).size;
    let html = `<div class="paper-head">
        <h1>${c ? c.display : curCat}</h1>
        <div class="paper-sub">${c ? c.path : ''}</div>
        <div class="paper-meta">共 ${entries.length} 题 · 跨 ${years} 年</div>
        <button class="all-ans-btn" id="allAnsBtn" onclick="toggleAllAnswers(this)">🔼 展开全部答案</button>
    </div>`;
    entries.forEach(e => { html += catCard(e.paper, e.secTitle, e.q); });
    el.innerHTML = html;
    renderMath(el);
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

// 收藏夹视图：不分类，按收藏时间倒序列出所有已收藏题目（每张卡片标注所属考点）
function renderFavView(el) {
    const favEntries = allEntries.filter(e => isFav(qidOf(e.paper.id, e.q.no)));
    if (!favEntries.length) {
        el.innerHTML = `<div class="cat-empty">还没有收藏的题目。<br>到真题页点卡片右上角 ☆ 收藏后，这里会汇总成收藏夹。</div>`;
        return;
    }
    favEntries.sort((a, b) => favTime(qidOf(b.paper.id, b.q.no)) - favTime(qidOf(a.paper.id, a.q.no)));
    let html = `<div class="paper-head">
        <h1>⭐ 收藏夹</h1>
        <div class="paper-meta">共 ${favEntries.length} 题 · 按收藏时间排序（新收藏在前）</div>
        <button class="all-ans-btn" id="allAnsBtn" onclick="toggleAllAnswers(this)">🔼 展开全部答案</button>
    </div>`;
    favEntries.forEach(e => {
        const cid = e.q.categoryIds && e.q.categoryIds[0];
        const cl = cid != null ? cats[String(cid)] : null;
        const label = cl ? (cl.display || cl.name) : '';
        html += catCard(e.paper, e.secTitle, e.q, label);
    });
    el.innerHTML = html;
    renderMath(el);
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

// ============ 初始化 ============
async function init() {
    const [er, pr, cr] = await Promise.all([
        fetch('data/exam.json'),
        fetch('data/practice.json').catch(() => null),  // practice.json 可选
        fetch('data/exam_categories.json'),
    ]);
    if (!er.ok) throw new Error('加载真题失败: ' + er.status);
    if (!cr.ok) throw new Error('加载分类失败: ' + cr.status);
    papers = await er.json();
    // 合并 practice.json（如果存在）
    if (pr && pr.ok) {
        const practice = await pr.json();
        if (Array.isArray(practice)) {
            papers = papers.concat(practice);
        }
    }
    cats = await cr.json();
    const btn = document.getElementById('favOnly');
    if (btn) btn.classList.toggle('on', viewMode === 'fav');
    buildEntries();
    buildTreeData();
    renderTree();
    renderMain();
}

init().catch(e => {
    const el = document.getElementById('catMain');
    if (el) el.innerHTML = '<div class="empty-tip">加载失败：' + esc(e.message) + '</div>';
    console.error(e);
});
