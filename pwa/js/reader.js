/* 考研数学笔记 - 阅读器：notes.json 加载 + Markdown 渲染 + 目录树 + 页内导航 + 搜索 */

const SUBJECT_NAMES = { gs: '高等数学', xd: '线性代数', ht: '数学好题' };

let notes = [];            // 全部笔记（notes.json）
let cur = null;            // 当前笔记
let searchIndex = [];      // 扁平搜索索引 [{ni, ci, text}]
let lastHits = [];         // 最近一次搜索的结果（供点击精确定位）
let pendingLocate = null;  // 待定位的命中项（跨笔记跳转渲染完后消费）
const openFiles = {};      // 侧栏文件展开状态（用户点击控制）
const openGroups = JSON.parse(localStorage.getItem('openGroups') || '{}');  // 科目分组收缩状态（默认展开）

// ============ 初始化与路由 ============
async function init() {
    const resp = await fetch('data/notes.json');
    if (!resp.ok) throw new Error('加载笔记数据失败: ' + resp.status);
    notes = await resp.json();
    buildSearchIndex();
    renderTree();
    window.addEventListener('hashchange', route);
    route();
}

/** hash 路由：#/笔记id 或 #/笔记id/章序号 */
function route() {
    const parts = decodeURIComponent(location.hash.replace(/^#\/?/, '')).split('/');
    const note = notes.find(n => n.id === parts[0]) || notes[0];
    const chIdx = parts[1] !== undefined ? parseInt(parts[1], 10) : -1;
    if (note !== cur) {
        cur = note;
        openFiles[note.id] = true;
        renderDoc(note);
        renderToc(note);
        renderTree();
    }
    if (chIdx >= 0) {
        const el = document.getElementById('ch-' + chIdx);
        if (el) el.scrollIntoView({ block: 'start' });
    } else {
        window.scrollTo(0, 0);
    }
    highlightToc();
    if (pendingLocate) {   // 搜索精确定位：盖过上面的章节级滚动
        if (notes[pendingLocate.ni] === cur) locateBlock(pendingLocate);
        pendingLocate = null;
    }
}

// ============ Markdown 渲染（针对导图 md 的语法子集） ============
function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** 行内格式：转义 → 图片、加粗、⭐高亮；$...$ 原样保留交给 KaTeX */
function inline(s) {
    return esc(s)
        .replace(/!\[(.*?)\]\((.+?)\)/g, '<img class="li-img" src="$2" alt="$1" loading="lazy">')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/⭐+/g, '<span class="star">$&</span>');
}

/** 长条目分行：公式外的"；"后断行；若含"；"则首个公式外"："后也断行（引导语单独一行）。
 *  文字原样保留只插 <br>，textContent 不变 → 已有批注/荧光锆点不失效 */
function breakLines(text) {
    const segs = [];
    let seg = '', inMath = false;
    for (const ch of text) {
        if (ch === '$') inMath = !inMath;
        seg += ch;
        if (ch === '；' && !inMath) { segs.push(seg); seg = ''; }
    }
    if (seg) segs.push(seg);
    if (segs.length > 1) {
        const first = segs[0];
        let iM = false, cut = -1;
        for (let i = 0; i < first.length; i++) {
            if (first[i] === '$') iM = !iM;
            else if (first[i] === '：' && !iM) { cut = i; break; }
        }
        if (cut >= 0 && cut < first.length - 1)
            segs.splice(0, 1, first.slice(0, cut + 1), first.slice(cut + 1));
    }
    return segs.map(inline).join('<br>');
}

/** 列表项样式类：⚠️ 易错 / 💡 技巧 / 例：例题；⭐ 叠加常考高亮 */
function liClass(text) {
    const cls = [];
    if (text.includes('⚠️')) cls.push('c-warn');
    else if (text.includes('💡')) cls.push('c-tip');
    else if (/^例[：（(]/.test(text.trim())) cls.push('c-example');
    if (text.includes('⭐')) cls.push('c-star');
    return cls.length ? ` class="${cls.join(' ')}"` : '';
}

/** 递归输出嵌套列表；items = [{level, text}] */
function emitList(items, start, level) {
    let html = '<ul>';
    let i = start;
    while (i < items.length && items[i].level >= level) {
        if (items[i].level > level) { i++; continue; }  // 容错：跳级缩进
        html += `<li${liClass(items[i].text)}>` + breakLines(items[i].text);
        let j = i + 1;
        if (j < items.length && items[j].level > level) {
            const [childHtml, next] = emitList(items, j, items[j].level);
            html += childHtml;
            j = next;
        }
        html += '</li>';
        i = j;
    }
    return [html + '</ul>', i];
}

/** 表格行分列：忽略 $...$ 公式内部的 |（如 $\dfrac{|A|}{\lambda}$） */
function splitRow(line) {
    const s = line.trim().replace(/^\|/, '').replace(/\|$/, '');
    const cells = [];
    let cell = '', inMath = false;
    for (const ch of s) {
        if (ch === '$') inMath = !inMath;
        if (ch === '|' && !inMath) { cells.push(cell.trim()); cell = ''; }
        else cell += ch;
    }
    cells.push(cell.trim());
    return cells;
}

function emitTable(rows) {
    let html = '<table>';
    rows.forEach((cells, r) => {
        if (r === 1) return;  // |---|---| 分隔行
        const tag = r === 0 ? 'th' : 'td';
        html += '<tr>' + cells.map(c => `<${tag}>${inline(c)}</${tag}>`).join('') + '</tr>';
    });
    return html + '</table>';
}

function mdToHtml(md) {
    const lines = md.split('\n').map(l => l.replace(/<!--.*?-->/g, '').replace(/\s+$/, ''));
    const out = [];
    let chIdx = -1;
    let i = 0;
    while (i < lines.length) {
        const line = lines[i];
        if (!line.trim() || line.startsWith('# ')) { i++; continue; }
        if (line.startsWith('## ')) {
            chIdx++;
            out.push(`<h2 id="ch-${chIdx}">${inline(line.slice(3).trim())}</h2>`);
            i++;
        } else if (/^:::\s*fold\b/.test(line.trim())) {
            // 折叠块：::: fold 标题 … :::（答案/解析默认收起）
            const title = line.trim().replace(/^:::\s*fold\s*/, '') || '展开';
            out.push(`<details class="fold"><summary>${inline(title)}</summary><div class="fold-body">`);
            i++;
        } else if (line.trim() === ':::') {
            out.push('</div></details>');
            i++;
        } else if (/^!\[.*?\]\(.+?\)$/.test(line.trim())) {
            // 独行图片：![说明](路径) → figure + 图注
            const m = line.trim().match(/^!\[(.*?)\]\((.+?)\)$/);
            out.push(`<figure class="md-img"><img src="${esc(m[2])}" alt="${esc(m[1])}" loading="lazy">` +
                (m[1] ? `<figcaption>${esc(m[1])}</figcaption>` : '') + '</figure>');
            i++;
        } else if (/^\s*- /.test(line)) {
            const items = [];
            while (i < lines.length && /^\s*- /.test(lines[i])) {
                const m = lines[i].match(/^(\s*)- (.*)$/);
                items.push({ level: Math.floor(m[1].length / 2), text: m[2] });
                i++;
            }
            out.push(emitList(items, 0, 0)[0]);
        } else if (line.trim().startsWith('|')) {
            const rows = [];
            while (i < lines.length && lines[i].trim().startsWith('|')) {
                rows.push(splitRow(lines[i]));
                i++;
            }
            out.push(emitTable(rows));
        } else {
            out.push(`<p>${breakLines(line.trim())}</p>`);
            i++;
        }
    }
    return out.join('\n');
}

function renderDoc(note) {
    const el = document.getElementById('docPane');
    el.innerHTML = `<article class="note-article">
        <div class="doc-crumb">${SUBJECT_NAMES[note.subject]}</div>
        <h1>${inline(note.title)}</h1>
        ${mdToHtml(note.md)}
    </article>`;
    document.title = note.name + ' - 考研数学笔记';
    renderMath(el);
    if (window.Annot) Annot.apply(note.id);  // 公式渲染完再恢复用户标注
}

// ============ 左侧目录树 ============
function toggleFile(id) {
    openFiles[id] = !openFiles[id];
    renderTree();
}

function toggleGroup(key) {
    openGroups[key] = openGroups[key] === false;   // 默认展开（undefined 视为开）→ 点击在 false/true 间切换
    localStorage.setItem('openGroups', JSON.stringify(openGroups));
    renderTree();
}

function renderTree() {
    const el = document.getElementById('navTree');
    const keep = el.scrollTop;
    let html = '';
    for (const key of Object.keys(SUBJECT_NAMES)) {
        const list = notes.filter(n => n.subject === key);
        if (list.length === 0) continue;
        const gOpen = openGroups[key] !== false;
        html += `<div class="tree-group ${gOpen ? 'open' : ''}" onclick="toggleGroup('${key}')">
            <span class="tree-arrow">›</span>${SUBJECT_NAMES[key]}</div>`;
        if (!gOpen) continue;
        for (const n of list) {
            const active = cur && n.id === cur.id;
            const open = !!openFiles[n.id];
            html += `<div class="tree-file ${open ? 'open' : ''} ${active ? 'active' : ''}">
                <div class="tree-file-row">
                    <span class="tree-arrow" onclick="toggleFile('${n.id}')">›</span>
                    <a href="#/${n.id}">${n.name}</a>
                </div>
                <div class="tree-chs">` +
                n.chapters.map((ch, i) =>
                    `<a class="tree-ch" href="#/${n.id}/${i}">${esc(ch)}</a>`).join('') +
                `</div></div>`;
        }
    }
    el.innerHTML = html;
    el.scrollTop = keep;
}

// ============ 右侧「本页目录」+ scrollspy ============
function renderToc(note) {
    const el = document.getElementById('tocPane');
    el.innerHTML = `<div class="toc-title">本页目录</div>` +
        note.chapters.map((ch, i) =>
            `<a class="toc-link" data-ch="${i}" href="#/${note.id}/${i}">${esc(ch)}</a>`).join('');
}

function highlightToc() {
    if (!cur) return;
    const h2s = document.querySelectorAll('.note-article h2');
    let active = -1;
    for (const h of h2s) {
        if (h.getBoundingClientRect().top <= 90) active = parseInt(h.id.slice(3), 10);
        else break;
    }
    document.querySelectorAll('.toc-link').forEach(a =>
        a.classList.toggle('active', parseInt(a.dataset.ch, 10) === active));
}

let _spyTimer = null;
window.addEventListener('scroll', () => {
    if (_spyTimer) return;
    _spyTimer = setTimeout(() => { _spyTimer = null; highlightToc(); }, 80);
}, { passive: true });

// ============ 搜索（标题 + 章节 + 全文行 + 📝批注；知识点优先、好题靠后） ============
const SUBJECT_RANK = { gs: 0, xd: 1, ht: 2 };   // 高数/线代（知识点）在前，好题在后

function buildSearchIndex() {
    searchIndex = [];
    notes.forEach((n, ni) => {
        const r = SUBJECT_RANK[n.subject] ?? 3;
        searchIndex.push({ ni, ci: -1, text: n.title, r, w: 0 });   // 笔记标题
        let ci = -1;
        for (const raw of n.md.split('\n')) {
            const line = raw.replace(/<!--.*?-->/g, '').trim();
            if (!line || line.startsWith('# ') || line.startsWith(':::')) continue;
            if (line.startsWith('## ')) { ci++; searchIndex.push({ ni, ci, text: line.slice(3).trim(), r, w: 1 }); continue; }
            const text = line.replace(/^[-|\s]+/, '').replace(/\*\*/g, '');
            if (text) searchIndex.push({ ni, ci, text, r, w: 2 });
        }
    });
}

function doSearch(q) {
    const box = document.getElementById('searchResults');
    q = q.trim().toLowerCase();
    if (!q) { showHistory(); return; }
    const hits = [];
    searchIndex.forEach((item, idx) => {
        if (item.text.toLowerCase().includes(q)) hits.push({ ...item, idx });
    });
    // 用户自己写的📝批注也可搜索，排最前
    let ann = {};
    try { ann = JSON.parse(localStorage.getItem('notesAnnot')) || {}; } catch (e) { }
    for (const [id, b] of Object.entries(ann)) {
        const ni = notes.findIndex(n => n.id === id);
        if (ni < 0) continue;
        for (const t of Object.values(b.notes || {}))
            if (t.toLowerCase().includes(q))
                hits.push({ ni, ci: -1, text: '📝 ' + t, r: -1, w: 0, idx: -1 });
    }
    // 排序：科目（知识点在前、好题在后）→ 标题/章节/正文 → 原文顺序
    hits.sort((a, b) => a.r - b.r || a.w - b.w || a.idx - b.idx);
    const top = hits.slice(0, 40);
    lastHits = top;
    box.hidden = false;
    box.innerHTML = top.length === 0 ? '<div class="sr-empty">无结果</div>' :
        top.map((h, i) => {
            const n = notes[h.ni];
            const ch = h.ci >= 0 ? n.chapters[h.ci] : '';
            return `<a class="sr-item" href="#/${n.id}${h.ci >= 0 ? '/' + h.ci : ''}" onclick="return locateHit(${i})">
                <span class="sr-path"><span class="sr-tag ${n.subject}">${SUBJECT_NAMES[n.subject]}</span>${n.name}${ch ? ' › ' + esc(ch) : ''}</span>
                <span class="sr-text">${esc(h.text.slice(0, 60))}</span></a>`;
        }).join('');
}

/** 点搜索结果：跳到对应笔记并精确定位到命中行 */
function locateHit(i) {
    const h = lastHits[i];
    if (!h) return false;
    const n = notes[h.ni];
    pendingLocate = h;
    saveHist(document.getElementById('searchInput').value);  // 点了结果才记入历史（证明是有效搜索）
    clearSearch();
    const target = '/' + n.id + (h.ci >= 0 ? '/' + h.ci : '');
    if (decodeURIComponent(location.hash.replace(/^#/, '')) === target) route();  // hash 不变时手动触发
    else location.hash = '#' + target;
    return false;
}

/** 在已渲染正文里找命中行：取行内最长的公式外文本段做锚，瞬时滚到屏幕中央并闪烁。
 *  用 instant 而非平滑滚动：平滑动画可被打断，后台标签页下甚至完全不执行 */
function locateBlock(h) {
    const plain = h.text.replace(/^📝 /, '').split(/\$[^$]*\$/)
        .map(s => s.replace(/\*\*/g, '').trim())
        .sort((a, b) => b.length - a.length)[0] || '';
    if (plain.length < 2) return;
    let best = null;   // 取文本最短的命中块 = 最内层、最精确
    for (const b of document.querySelectorAll('.note-article li, .note-article p, .note-article h2, .note-article td, .note-article .ann-text')) {
        if (b.textContent.includes(plain) && (!best || b.textContent.length < best.textContent.length)) best = b;
    }
    if (!best) return;
    for (let d = best.closest('details'); d; d = d.parentElement.closest('details')) d.open = true;  // 折叠块内命中先展开
    best.scrollIntoView({ block: 'center', behavior: 'instant' });
    best.classList.add('locate-flash');
    setTimeout(() => best.classList.remove('locate-flash'), 1800);
}

function clearSearch() {
    document.getElementById('searchInput').value = '';
    const box = document.getElementById('searchResults');
    box.hidden = true;
    box.innerHTML = '';
}

// ============ 搜索历史（localStorage 最多 5 条，可单删/清空） ============
const HIST_KEY = 'searchHistory';
const getHist = () => { try { return JSON.parse(localStorage.getItem(HIST_KEY)) || []; } catch (e) { return []; } };

function saveHist(term) {
    term = term.trim();
    if (!term) return;
    const h = getHist().filter(t => t !== term);   // 去重后提到最前
    h.unshift(term);
    localStorage.setItem(HIST_KEY, JSON.stringify(h.slice(0, 5)));
}

/** 输入框为空时展示历史列表（聚焦/清空输入时触发） */
function showHistory() {
    const box = document.getElementById('searchResults');
    const h = getHist();
    if (!h.length) { box.hidden = true; box.innerHTML = ''; return; }
    box.hidden = false;
    box.innerHTML = `<div class="sh-head">搜索历史<button class="sh-clear" onclick="clearHist()">清空</button></div>` +
        h.slice(0, 5).map((t, i) => `<div class="sh-item" onclick="useHist(${i})">
            <span class="sh-term">${esc(t)}</span>
            <button class="sh-del" onclick="delHist(event, ${i})" title="删除这条">×</button></div>`).join('');
}

function useHist(i) {
    const t = getHist()[i];
    if (!t) return;
    document.getElementById('searchInput').value = t;
    doSearch(t);
}

function delHist(e, i) {
    e.stopPropagation();   // 别触发整行的 useHist
    const h = getHist();
    h.splice(i, 1);
    localStorage.setItem(HIST_KEY, JSON.stringify(h));
    showHistory();
}

function clearHist() {
    localStorage.removeItem(HIST_KEY);
    const box = document.getElementById('searchResults');
    box.hidden = true;
    box.innerHTML = '';
}

// 点搜索区外部 → 收起下拉（历史/结果都适用）
document.addEventListener('click', e => {
    if (!e.target.closest('.search-box')) {
        const box = document.getElementById('searchResults');
        box.hidden = true;
    }
});

// ============ 图片双击放大（正文图/行内图/批注贴图通用） ============
function openLightbox(src) {
    let lb = document.getElementById('imgLightbox');
    if (!lb) {
        lb = document.createElement('div');
        lb.id = 'imgLightbox';
        lb.innerHTML = '<img alt="放大预览">';
        lb.onclick = () => lb.classList.remove('show');
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') lb.classList.remove('show');
        });
        document.body.appendChild(lb);
    }
    lb.querySelector('img').src = src;
    lb.classList.add('show');
}

document.addEventListener('dblclick', e => {
    const img = e.target.closest('.md-img img, img.li-img, img.ann-img');
    if (img && img.src) openLightbox(img.src);
});

// ============ KaTeX ============
function renderMath(el) {
    if (typeof renderMathInElement !== 'function') return;  // vendor 缺失时降级为原文
    renderMathInElement(el, {
        delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
        ],
        throwOnError: false,
    });
}

// ============ Service Worker ============
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js').catch(err => {
            console.warn('SW 注册失败（file:// 下属正常，请用 start.bat 启动）:', err);
        });
    });
}

init().catch(e => {
    document.getElementById('docPane').innerHTML =
        `<div class="error">加载失败: ${esc(e.message)}<br>请用 start.bat 启动后访问 http://localhost:8409</div>`;
});
