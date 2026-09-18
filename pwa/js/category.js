/* 真题分类浏览页：左=二级分类树（学科/章节，可折叠、含题数），右=选中章节的跨年真题
 * 分类口径：大观园「知识点/章节」体系（exam_categories.json 的 12 个二级章节）。
 * 复用 exam.js 的渲染 / 收藏辅助函数（独立副本，避免改动 exam.js 既有行为）。 */

const FAV_KEY = 'examFav';            // { qid: 1 }，qid = 套卷id-题no
const FAV_ONLY_KEY = 'examFavOnly';   // 是否只看收藏（常量保留，界面已由三选筛选替代）
const EXAM_STATUS_KEY = 'examStatus';   // { qid: 'unfamiliar' | 'unknown' }：不熟/不会掌握度标记（互斥）

// ============ 收藏存储 ============
// 收藏/标记统一主键：核心题库的题若映射到数二真题（linkedQid），直接沿用真题的 qid，
// 从而与「真题页 / 真题分类」的收藏、不熟、不会标记双向同步。
let coreLink = {};   // core 题 no -> linkedQid（init 时从 corePapers 构建）
function qidOf(paperId, no) {
    if (paperId === 'core') return coreLink[no] || ('core-' + no);
    return paperId + '-' + no;
}

// 旧版核心题库曾用 'core-<no>' 作为收藏/标记/笔记主键；主键统一为真题 qid 后需一次性迁移：
// 目标键为空才搬（不覆盖真题侧已有数据），搬完删旧键，保证用户旧标记/旧笔记不"消失"。
function migrateCoreLegacyKeys() {
    try {
        const entries = Object.entries(coreLink);
        if (!entries.length) return;
        const fav = favGet(), st = statusGet();
        let fC = false, sC = false;
        for (const [no, lq] of entries) {
            const oldKey = 'core-' + no;
            if (fav[oldKey]) { if (!fav[lq]) fav[lq] = fav[oldKey]; delete fav[oldKey]; fC = true; }
            if (st[oldKey]) { if (!st[lq]) st[lq] = st[oldKey]; delete st[oldKey]; sC = true; }
            const nk = 'examNote-' + lq, ok = 'examNote-' + oldKey;
            const v = localStorage.getItem(ok);
            if (v !== null && v !== '') {
                if (!localStorage.getItem(nk)) localStorage.setItem(nk, v);
                localStorage.removeItem(ok);
            }
        }
        if (fC) favSave(fav);
        if (sC) statusSave(st);
    } catch (e) { console.error('核心题库旧主键迁移失败', e); }
}
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
    if (markSel.fav || markSel.unfamiliar || markSel.unknown) { renderTree(); renderMain(); }
}

// 掌握度/收藏多选筛选（默认全选，并集去重；收藏/不熟/不会互不归属）
let markSel = { fav: false, unfamiliar: false, unknown: false }; // 收藏 / 不熟 / 不会 分开筛选；默认都不选 = 显示全部
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
        // 只去普通空格/制表符，保留 NBSP（承载用户打的缩进/连续空格；raw.trim() 会连 NBSP 一起删）
        // 行首普通空格转 NBSP：单个行首空格浏览器不自动转 NBSP，渲染端兜底保留缩进（与 exam.js/exam-shared.js 同步）
        const l = raw
            .replace(/^[ \t]+/, m => m.replace(/[ \t]/g, '\u00A0'))
            .replace(/[ \t]+$/, '')                        // 行尾普通空格照旧删除（NBSP 不在此类）
            .replace(/ {2,}/g, m => m.replace(/ /g, '\u00A0'));   // 行内连续普通空格(2+)转 NBSP：防 HTML 折叠丢空格（单个空格不受影响）
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
                { left: '\\(', right: '\\)', display: false },
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
// ============ 笔记富文本编辑器（2019+ 与真题页同款：contenteditable + 字色/高亮/H标题 + 贴图压缩存 IndexedDB） ============
// 以下为 exam.js 移植副本；两页改动需同步（记忆：mdBlockWithImg/fillExamNoteImgs/zoomAnsImg 等重复副本）

let _noteTimer = {};
// ---- contenteditable 富编辑器：[图:id] 内嵌图片 + 字色/高亮（存储为令牌 <c:#hex>…</c> <h:#hex>…</h>） ----
const NOTE_FMT_RE = /<c:(#[0-9a-fA-F]{6})>|<h:(#[0-9a-fA-F]{6})>|<\/c>|<\/h>|<b>|<\/b>|<i>|<\/i>|<h1>|<\/h1>|<h2>|<\/h2>/g;
/** 存储文本 → 编辑器 DOM：文本/换行原样，[图:id] 变为编辑器内联图片（contenteditable=false，可拖拽排序/删除/点击放大），格式令牌变 span/mark（栈式嵌套） */
function noteToEditor(el, text) {
    el.innerHTML = '';
    const stack = [el];
    const emitText = s => {
        const lines = s.split('\n');
        lines.forEach((line, k) => {
            if (k > 0) stack[stack.length - 1].appendChild(document.createElement('br'));
            if (line) stack[stack.length - 1].appendChild(document.createTextNode(line));
        });
    };
    let i = 0;
    while (i < text.length) {
        const mi = text.indexOf('[图:', i);
        NOTE_FMT_RE.lastIndex = i;
        const mf = NOTE_FMT_RE.exec(text);
        if (mf && (mi < 0 || mf.index <= mi)) {
            emitText(text.slice(i, mf.index));
            const m0 = mf[0];
            if (m0 === '</c>' || m0 === '</h>' || m0 === '</b>' || m0 === '</i>' || m0 === '</h1>' || m0 === '</h2>') {
                if (stack.length > 1) stack.pop();
            } else {
                let node;
                if (m0 === '<b>') node = document.createElement('b');
                else if (m0 === '<i>') node = document.createElement('i');
                else if (m0 === '<h1>') node = document.createElement('h1');
                else if (m0 === '<h2>') node = document.createElement('h2');
                else if (mf[1]) node = Object.assign(document.createElement('span'), { style: 'color:' + mf[1] });
                else node = Object.assign(document.createElement('mark'), { style: 'background:' + mf[2] });
                stack[stack.length - 1].appendChild(node);
                stack.push(node);
            }
            i = mf.index + mf[0].length;
        } else if (mi >= 0) {
            emitText(text.slice(i, mi));
            const m2 = /\[图:([a-z0-9]+)\]/.exec(text.slice(mi));
            if (m2) stack[stack.length - 1].appendChild(noteImgNode(m2[1]));
            i = mi + (m2 ? m2[0].length : 1);
        } else {
            emitText(text.slice(i));
            i = text.length;
        }
    }
}
function appendNoteText(el, chunk) {
    const lines = chunk.split('\n');
    lines.forEach((line, i) => {
        if (i > 0) el.appendChild(document.createElement('br'));
        if (line) el.appendChild(document.createTextNode(line));
    });
}
function noteImgNode(id) {
    const wrap = document.createElement('span');
    wrap.className = 'exam-note-img-wrap';
    wrap.draggable = true;
    const img = document.createElement('img');
    img.className = 'exam-note-img';
    img.dataset.img = id;
    img.alt = '笔记图片';
    img.setAttribute('contenteditable', 'false');
    img.onclick = () => zoomAnsImg(img);
    const del = document.createElement('button');
    del.type = 'button';
    del.className = 'exam-note-img-del';
    del.title = '删除图片';
    del.textContent = '×';
    del.onclick = () => {
        // 编辑态删图前确认：图片 blob 一旦删除无法找回（除非有导出备份）
        if (confirm('删除这张图片？（文字不受影响，删除后需重新插入）')) delExamNoteImg(id, del);
    };
    wrap.append(img, del);
    // 编辑器内拖拽排序：拖动图片调整顺序，落点顺序即存储顺序（editorToNote 按 DOM 位置序列化）
    wrap.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', id);
        e.dataTransfer.effectAllowed = 'move';
        wrap.classList.add('dragging');
    });
    wrap.addEventListener('dragend', () => {
        wrap.classList.remove('dragging');
        document.querySelectorAll('.exam-note-img-wrap.over').forEach(w => w.classList.remove('over'));
    });
    wrap.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; wrap.classList.add('over'); });
    wrap.addEventListener('dragleave', () => wrap.classList.remove('over'));
    wrap.addEventListener('drop', e => {
        e.preventDefault();
        wrap.classList.remove('over');
        const dragged = document.querySelector('.exam-note-img-wrap.dragging');
        if (!dragged || dragged === wrap) return;
        const r = wrap.getBoundingClientRect();
        const after = (e.clientY - r.top) > r.height / 2;
        if (after) wrap.after(dragged); else wrap.before(dragged);
        const sec = wrap.closest('.q-note');
        const ta = sec && sec.querySelector('.q-note-input');
        if (ta) noteInput(ta);   // 顺序变更即落盘 + 刷新预览
    });
    return wrap;
}
/** 编辑器 DOM → 存储文本：图片还原 [图:id]，带格式的文本节点包令牌（字色/高亮/粗体/斜体走行内令牌，H1/H2 走块级令牌包裹整段） */

function editorToNote(el) {
    const rgbToHex = v => {
        const m = /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(v || '');
        return m ? '#' + [1, 2, 3].map(k => (+m[k]).toString(16).padStart(2, '0')).join('') : null;
    };
    // 任意颜色串（hex/rgb/命名色）归一为 #rrggbb；借助临时元素让浏览器自行规范化
    const normColor = v => { if (!v) return null; const tmp = document.createElement('span'); tmp.style.color = v; return rgbToHex(tmp.style.color); };
    const isBold = n => (n && n.nodeType === 1) && (n.tagName === 'B' || n.tagName === 'STRONG' || /bold/i.test(n.style.fontWeight || ''));
    const isItalic = n => (n && n.nodeType === 1) && (n.tagName === 'I' || n.tagName === 'EM' || /italic/i.test(n.style.fontStyle || ''));
    // 提取节点自身携带的「字色/高亮」：style.color / style.backgroundColor，并兼容浏览器 foreColor
    // 生成的 <font color> / <font bgcolor>。元素没带颜色时沿用父级上下文（c/h）。
    // 关键：粗/斜节点上同样可能带颜色（加粗后再上色、或 Chrome 把 font-weight 与 color 写在同一个
    // span 上），过去 isBold/isItalic 分支不读颜色 → 序列化只留下 <b>/<i>，颜色「染不上」。
    const colorOf = (ch, c, h) => {
        let nc = c, nh = h;
        if (ch.style) {
            const hc = normColor(ch.style.color); if (hc) nc = hc;
            const hb = normColor(ch.style.backgroundColor); if (hb) nh = hb;
        }
        const fattr = ch.getAttribute && ch.getAttribute('color');
        if (fattr) { const fc = normColor(fattr); if (fc) nc = fc; }
        const fbg = ch.getAttribute && ch.getAttribute('bgcolor');
        if (fbg) { const fb = normColor(fbg); if (fb) nh = fb; }
        return [nc, nh];
    };
    // 返回序列化片段；c/h=字色/高亮 hex，b/i=是否处于粗/斜上下文（行内令牌），heading 由 H1/H2 元素单独包块级令牌
    let base = (function run(n, c, h, b, i) {
        let s = '';
        for (const ch of n.childNodes) {
            if (ch.nodeType === 3) {
                // 保留 NBSP（\u00A0）：浏览器用它保真「行首空格 / 连续空格」，降级成普通空格会被 trim 与 HTML 折叠吃掉
                const t = ch.nodeValue.replace(/\u200B/g, '').replace(/ {2,}/g, m => m.replace(/ /g, '\u00A0'));  // 只丢弃零宽空格分隔符；连续普通空格转 NBSP（HTML 会折叠连续普通空格，单个空格不受影响）
                if (!t) continue;
                let inner = t;
                if (i) inner = '<i>' + inner + '</i>';
                if (b) inner = '<b>' + inner + '</b>';
                if (h) inner = '<h:' + h + '>' + inner + '</h>';
                if (c) inner = '<c:' + c + '>' + inner + '</c>';
                s += inner;
            } else if (ch.nodeType === 1) {
                if (ch.classList && ch.classList.contains('exam-note-img-wrap')) {
                    const img = ch.querySelector('img[data-img]');
                    if (img) s += '[图:' + img.dataset.img + ']';
                }
                else if (ch.tagName === 'IMG' && ch.dataset.img) s += '[图:' + ch.dataset.img + ']';
                else if (ch.tagName === 'BR') s += '\n';
                else if (ch.tagName === 'H1') {
                    if (s && !s.endsWith('\n')) s += '\n';
                    s += '<h1>' + run(ch, c, h, false, false) + '</h1>' + '\n';
                }
                else if (ch.tagName === 'H2') {
                    if (s && !s.endsWith('\n')) s += '\n';
                    s += '<h2>' + run(ch, c, h, false, false) + '</h2>' + '\n';
                }
                else if (isBold(ch)) {
                    // 粗体节点上的字色/高亮同样要保留（加粗后再上色的常见顺序）
                    const [bc, bh] = colorOf(ch, c, h);
                    const block = ch.tagName === 'DIV' || ch.tagName === 'P';
                    if (block && s && !s.endsWith('\n')) s += '\n';
                    s += run(ch, bc, bh, true, i);
                    if (block && s && !s.endsWith('\n')) s += '\n';
                }
                else if (isItalic(ch)) {
                    const [ic, ih] = colorOf(ch, c, h);
                    s += run(ch, ic, ih, b, true);
                }
                else {
                    let nc = c, nh = h;
                    if (ch.style) {
                        const hc = normColor(ch.style.color); if (hc) nc = hc;
                        const hb = normColor(ch.style.backgroundColor); if (hb) nh = hb;
                    }
                    // 兼容 <font color="..."> / <font bgcolor="...">：部分浏览器 foreColor/hiliteColor 生成 font 而非 span，颜色只在属性上、style.color 为空
                    const fattr = ch.getAttribute && ch.getAttribute('color');
                    if (fattr) { const fc = normColor(fattr); if (fc) nc = fc; }
                    const fbg = ch.getAttribute && ch.getAttribute('bgcolor');
                    if (fbg) { const fb = normColor(fbg); if (fb) nh = fb; }
                    const block = ch.tagName === 'DIV' || ch.tagName === 'P';
                    if (block && s && !s.endsWith('\n')) s += '\n';
                    s += run(ch, nc, nh, b, i);
                    if (block && s && !s.endsWith('\n')) s += '\n';
                }
            }
        }
        return s;
    })(el, null, null, false, false);
    return base;
}
/** 统一取值：textarea.value 或 编辑器序列化文本 */
function noteVal(el) {
    return el.tagName === 'TEXTAREA' ? el.value : editorToNote(el);
}
/** 统一写入 */
function setNoteContent(el, text) {
    if (el.tagName === 'TEXTAREA') el.value = text;
    else noteToEditor(el, text);
}

let _noteLastRendered = {};   // qid → 上次渲染预览的文本（内容没变不重渲，防闪烁）
const _pendingImgs = new Set();   // 正在压缩/写库的图 id：orphan 清理必须跳过，否则会被误删
const _pendingImgTasks = {};   // id → 写库 Promise：手动保存前 await，杜绝「压缩未完成就落盘 → 预览图变『图片已丢失』」
/** 等待所有贴图压缩/写库完成（无 pending 立即 resolve；写库失败不抛出） */
function waitPendingImgs() {
    const tasks = Object.values(_pendingImgTasks).filter(Boolean);
    return tasks.length ? Promise.all(tasks).catch(() => { }) : Promise.resolve();
}
function noteInput(ta) {
    const qid = ta.dataset.qid;
    if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);   // 编辑器自增长，无需 JS 调高
    noteHint(ta, '自动保存中…', true);
    clearTimeout(_noteTimer[qid]);
    _noteTimer[qid] = setTimeout(() => {
        // 落盘时重新取实时值，不用 1.5s 前的闭包旧快照：
        // 异步贴图可能已在此期间登记进编辑器，用旧快照会把新贴的图判成"不再引用"而删掉（丢图根因）
        const finalVal = noteVal(ta);
        const newRefs = examImgRefs(finalVal);
        const olds = localStorage.getItem('examNote-' + qid) || '';
        const oldRefs = examImgRefs(olds);
        // 写入中的图（压缩/写库未完成）绝不当孤儿删
        const orphan = oldRefs.filter(id => !newRefs.includes(id) && !_pendingImgs.has(id));
        if (orphan.length) examImgDel(orphan);   // 清理不再引用的图，避免存储泄漏
        try { localStorage.setItem('examNote-' + qid, finalVal); } catch (e) { }
        const btn = ta.closest('.q-card') && ta.closest('.q-card').querySelector('[data-act="note"]');
        if (btn) btn.classList.toggle('has', !!finalVal.trim());
        noteHint(ta, finalVal.trim() ? '已保存 ✓' : '笔记是空的，不保存');
        // 编辑态实时预览：内容有变化才重渲染（KaTeX/图片回填开销大，无变化重渲是闪烁根源）
        if (ta.style.display !== 'none') renderNotePreview(ta);
    }, 1500);
}
// 编辑态实时预览：从编辑器当前内容渲染 Markdown + 图片（内容未变直接跳过，避免闪烁）
function renderNotePreview(ta) {
    if (!ta || ta.style.display === 'none') return;   // 只读态：保存路径已渲染最终只读预览，跳过——避免被覆盖成编辑态样式
    const sec = ta.closest('.q-note');
    const pv = sec && sec.querySelector('.q-note-preview');
    if (!pv) return;
    const v = noteVal(ta);
    if (_noteLastRendered[ta.dataset.qid] === v) return;   // 内容没变：跳过
    _noteLastRendered[ta.dataset.qid] = v;
    pv.hidden = false;
    pv.classList.add('pv-edit');               // 编辑态预览：限高缩短（图片本体现在显示在编辑器内）
    pv.innerHTML = mdBlockWithImg(v, true);
    if (v.includes('$') || v.includes('\\(') || v.includes('\\[')) renderMath(pv);
    fillExamNoteImgs(pv);   // 异步回填 IndexedDB 中的 blob
}
// 笔记区 Ctrl+V 贴图：支持一次粘贴多张图（遍历全部 image item；纯文本 html 内的 data 图也提取），
// 压缩后存 IndexedDB；每张图独立 id/节点/写库任务，杜绝「多图只存一张」。

function notePasteImg(e) {
    const ta = e.target;
    const items = [...(e.clipboardData?.items || [])];
    let files = items.filter(i => i.type.startsWith('image/')).map(it => it.getAsFile()).filter(Boolean);
    // 无独立 image item（Word/网页复制图文混排常只有 text/html）：提取其中的 data: 图兜底
    if (!files.length && e.clipboardData?.getData) {
        let html = '';
        try { html = e.clipboardData.getData('text/html') || ''; } catch (err) { }
        if (html) {
            const srcs = [...html.matchAll(/<img[^>]+src=["'](data:image\/[^"']+)["']/gi)].map(m => m[1]);
            files = srcs.map(src => {
                try {
                    const i = src.indexOf(','), meta = src.slice(5, i);
                    return new File([Uint8Array.from(atob(src.slice(i + 1)), c => c.charCodeAt(0))], 'img.png', { type: meta.split(';')[0] });
                } catch (err) { return null; }
            }).filter(Boolean);
        }
    }
    if (!files.length) {
        // 纯文本粘贴：降级为纯文本，防外来 HTML 污染编辑器
        if (ta.tagName !== 'TEXTAREA' && e.clipboardData?.getData) {
            e.preventDefault();
            const txt = e.clipboardData.getData('text/plain');
            if (txt) document.execCommand('insertText', false, txt);
        }
        return;
    }
    e.preventDefault();
    files.forEach(file => pasteOneNoteImg(ta, file));
}
// 粘贴单张图：登记节点（同步，防保存时序丢令牌）→ 原图落库兜底 → 压缩覆盖 → 回填
function pasteOneNoteImg(ta, raw) {
    // 碰撞免疫：优先 crypto.randomUUID（去连字符后全 [a-z0-9]，匹配现有正则），杜绝毫秒内连贴同 id
    const id = (crypto.randomUUID ? crypto.randomUUID().replace(/-/g, '') : (Date.now().toString(36) + Math.random().toString(36).slice(2, 6)));
    _pendingImgs.add(id);   // 标记写入中：orphan 清理跳过，杜绝「压缩未完成被当孤儿删掉」
    // 关键：同步把图片节点登记进编辑器，让 editorToNote 立刻抓到 [图:id]。
    // 原实现把插入放在 compressImage→examImgPut 两级异步之后，压缩大图要几百 ms，
    // 期间任何保存（1.5s 防抖 / 翻页 flush）都会存下不含该图的版本并触发误删 → 丢图。
    if (ta.tagName === 'TEXTAREA') {
        const tag = `[图:${id}]`;
        const p = ta.selectionStart;
        ta.value = ta.value.slice(0, p) + tag + ta.value.slice(ta.selectionEnd);
        ta.selectionStart = ta.selectionEnd = p + tag.length;
    } else {
        // 编辑器内联：在光标处插入可拖拽图片节点（顺序即存储顺序）
        const node = noteImgNode(id);
        const sel = getSelection();
        const range = sel && sel.rangeCount ? sel.getRangeAt(0) : null;
        if (range && ta.contains(range.startContainer)) {
            range.insertNode(node);
            range.setStartAfter(node);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        } else {
            ta.appendChild(node);
        }
        // 注意：此处绝不能调 fillExamNoteImgs —— blob 尚未写库，
        // 它会在 300ms 重试失败后 replaceWith('[图片已丢失]')，把节点换成文本导致令牌永久丢失。
    }
    noteInput(ta);   // 触发保存 + 预览（此时值里已含令牌）
    // 异步：压缩 → 写库 → 只回填这一张（写完后必定能取到 blob）
    // 兜底策略：先立即写入【原始图】再后台压缩覆盖——IDB 写原图比压缩快一个量级，
    // 即使贴图后立刻关页/切走导致压缩中断，原图 blob 也已落库，不会变成永久「图片已丢失」。
    const rawPut = examImgPut(id, raw).catch(() => { });   // 原图兜底写入失败不影响后续压缩写入
    const imgTask = compressImage(raw).then(blob => examImgPut(id, blob)).then(() => rawPut).then(() => true)
        // 压缩（或压缩写库）偶发失败：原图兜底已先行落库——保留引用、回填原图继续显示，
        // 绝不摘除节点（摘除 = 文本引用永失 → 用户看到"后贴的图消失"，即使 blob 还在 DB）
        .catch(() => fillOneExamNoteImg(ta, id))
        .then(ok => {
            if (ok) { fillOneExamNoteImg(ta, id); renderNotePreview(ta); }   // 回填这张图 + 刷新预览
            else { alert('图片保存失败'); removeExamNoteImgRef(ta, id); }     // 原图兜底也没有才摘除
        }).then(() => {
            _pendingImgs.delete(id);
        });
    _pendingImgTasks[id] = imgTask;
    imgTask.then(() => { delete _pendingImgTasks[id]; }, () => { delete _pendingImgTasks[id]; });
}

function applyNoteFormat(sec, cmd, val) {
    const ed = sec.querySelector('.q-note-input');
    if (!ed || ed.style.display === 'none' || !ed.isContentEditable) return;
    const sel = getSelection();
    const inEd = !!sel.rangeCount && ed.contains(sel.anchorNode);
    // 'plain'（转普通正文）与 'h1'/'h2'（整行设标题）允许光标直接停在行内，无需先选中文字；
    // 其余行内格式（字色/高亮/粗斜）必须先选中文字，否则无作用对象。
    const needSel = cmd !== 'plain' && cmd !== 'h1' && cmd !== 'h2';
    if (!inEd || (sel.isCollapsed && needSel)) {
        noteHint(ed, '先选中要设置格式的文字'); return;
    }
    ed.focus();
    if (cmd === 'h1' || cmd === 'h2') {
        // 标题用 formatBlock 生成 <h1>/<h2> 标签（须显式禁用 styleWithCSS，否则退化成带样式的 <span>）
        try { document.execCommand('styleWithCSS', false, false); } catch (e) { }
        document.execCommand('formatBlock', false, cmd === 'h1' ? 'H1' : 'H2');
    } else if (cmd === 'plain') {
        // 转为普通正文：先去掉 H1/H2 块级标题，再清除字色/高亮/粗斜等内联格式
        try { document.execCommand('styleWithCSS', false, false); } catch (e) { }
        document.execCommand('formatBlock', false, 'P');
        document.execCommand('removeFormat');
    } else {
        try { document.execCommand('styleWithCSS', false, true); } catch (e) { }
        document.execCommand(cmd, false, val || null);
    }
    noteInput(ed);   // 触发自动保存 + 预览刷新
}
/** 工具条显隐与编辑态同步 */
function syncNoteToolbar(sec) {
    if (!sec) return;
    const ed = sec.querySelector('.q-note-input');
    const bar = sec.querySelector('.q-note-toolbar');
    if (bar) bar.hidden = sec.hidden || !ed || ed.style.display === 'none';
}
// 顶部「💾 保存」按钮（.q-ops 行，位于 笔记 右侧）：定位本题卡的笔记区并保存。
// 仅在编辑态（编辑器可见）生效；只读展示态直接提示先编辑，避免误把空编辑器内容覆盖已存笔记。

async function toggleNoteEdit(btn) {
    const sec = btn.closest('.q-note');
    const ta = sec.querySelector('.q-note-input');
    const pv = sec.querySelector('.q-note-preview');
    const editing = ta.style.display !== 'none';
    if (!editing) {
        // 进入编辑：同一按钮文字切为「💾 保存」（编辑态保持可见，点击即保存收起）
        btn.textContent = '💾 保存';
        btn.classList.remove('saved');   // 再次编辑恢复按钮常态
        noteHint(btn, '');
        ta.style.display = '';
        // 单按钮方案：编辑态按钮保持可见，文字已切为「💾 保存」，点击即保存收起
        if (!ta.dataset.bind) {
            ta.addEventListener('input', () => noteInput(ta));
            ta.addEventListener('paste', notePasteImg);
            ta.dataset.bind = '1';
        }
        if (ta.tagName !== 'TEXTAREA') {
            setNoteContent(ta, noteGet(ta.dataset.qid));   // 每次进入编辑都从存储重建（文本 + 内联图片）
            fillExamNoteImgs(ta);   // 兜底回填（缩略图条已在 noteToEditor 内回填）
        } else {
            autoResizeNote(ta);
        }
        syncNoteToolbar(sec);
        delete _noteLastRendered[ta.dataset.qid];   // 强制预览重渲为编辑态（带删除 ×）
        renderNotePreview(ta);   // 进入编辑立即刷新下方预览（× 见 mdBlockWithImg editable）
        ta.focus();
        if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);
    } else {
        // 完成：清防抖定时器，立即落盘（有贴图在写库则先等写库完成，防止存下「读不到图」的版本）
        clearTimeout(_noteTimer[ta.dataset.qid]);
        delete _noteTimer[ta.dataset.qid];
        await waitPendingImgs();
        const raw = noteVal(ta);
        try { localStorage.setItem('examNote-' + ta.dataset.qid, raw); } catch (e) { }
        const v = raw.trim();
        if (v) {
            btn.textContent = '✏️ 编辑';
            btn.classList.add('saved');   // 保存后淡化按钮
            ta.style.display = 'none';
            syncNoteToolbar(sec);
            if (pv) {
                pv.classList.remove('pv-edit');   // 只读态恢复完整高度
                pv.innerHTML = mdBlockWithImg(raw);
                pv.hidden = false;
                if (raw.includes('$') || raw.includes('\\(') || raw.includes('\\[')) renderMath(pv);
                fillExamNoteImgs(pv);   // 无条件回填 [图:id] 贴图，保证编辑完成后实时显示
            }
            noteHint(btn, '已保存 ✓');
        } else {
            // 清空了内容：收起整节，重置为「空笔记」形态（下次展开直接是输入框 + 保存按钮）
            noteHint(btn, '已删除笔记');
            const opBtn = sec.closest('.q-card')?.querySelector('[data-act="note"]');
            sec.hidden = true;
            if (opBtn) opBtn.classList.remove('has');
            if (pv) { pv.classList.remove('pv-edit'); pv.innerHTML = ''; }   // 清空预览并恢复正常高度
            ta.style.display = '';
            setNoteContent(ta, '');
            // 重置为「空笔记」形态：下次展开直接是输入框 + 💾 保存按钮
            btn.textContent = '💾 保存';
            btn.classList.remove('saved');
        }
    }
}

// ============ 试卷点评（按套卷 id 存 localStorage，纯文本，popover 自动保存） ============

function compressImage(file) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => {
            const scale = Math.min(1, 1200 / Math.max(img.width, img.height));
            const canvas = document.createElement('canvas');
            canvas.width = Math.round(img.width * scale);
            canvas.height = Math.round(img.height * scale);
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#fff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            URL.revokeObjectURL(img.src);
            canvas.toBlob(b => b ? resolve(b) : reject(new Error('图片压缩失败')), 'image/jpeg', 0.85);
        };
        img.onerror = () => reject(new Error('图片读取失败'));
        img.src = URL.createObjectURL(file);
    });
}

// textarea 高度自适应：随内容增高，超过 60% 视口高出现滚动条
function autoResizeNote(el) {
    if (!el) return;
    el.style.height = 'auto';
    const maxH = Math.round(window.innerHeight * 0.6);
    el.style.height = Math.min(el.scrollHeight, maxH) + 'px';
    el.style.overflowY = el.scrollHeight > maxH ? 'auto' : 'hidden';
}

// 笔记保存状态提示（自动保存中… / 已保存 ✓ / 已删除图片 …），2s 后淡出。
// quiet=true（打字过程中的"自动保存中…"）：提示已显示时不重启动画，避免反复闪烁
function noteHint(anchor, msg, quiet) {
    const sec = anchor && anchor.closest && anchor.closest('.q-note');
    const el = sec && sec.querySelector('.q-note-hint');
    if (!el) return;
    if (!msg) { el.textContent = ''; el.classList.remove('show'); return; }
    if (quiet && el.classList.contains('show')) { if (el.textContent !== msg) el.textContent = msg; return; }
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.classList.remove('show'); }, 2000);
}

// 单图删除：删 IndexedDB 图 + 从文本删 [图:id] 占位 + 重渲染预览 + 同步「笔记」标记
function delExamNoteImg(id, btn) {
    const wrap = btn.closest('.q-note');
    if (!wrap) return;
    const ta = wrap.querySelector('.q-note-input');
    const qid = (ta && ta.dataset.qid) || wrap.dataset.qid;
    if (!qid) return;
    let v = ta ? noteVal(ta) : noteGet(qid);
    const re = new RegExp('\\[图:' + id + '\\]', 'g');
    // 只摘掉这一个图片令牌；严禁压缩空格/换行（\s{2,} 会把用户的段落空行和缩进空格全吃掉）
    v = v.replace(re, '');
    try { localStorage.setItem('examNote-' + qid, v); } catch (e) { }
    examImgDel([id]);
    if (ta) { setNoteContent(ta, v); fillExamNoteImgs(ta); }
    const pv = wrap.querySelector('.q-note-preview');
    if (pv && !pv.hidden) {
        pv.innerHTML = mdBlockWithImg(v, true);   // 删除后仍处于编辑态；图片本体显示在编辑器内，预览只留 🖼 标记
        if (v.includes('$') || v.includes('\\(') || v.includes('\\[')) renderMath(pv);
        fillExamNoteImgs(pv);
    }
    _noteLastRendered[qid] = v;   // 同步预览渲染缓存，防下次 renderNotePreview 误跳过
    const opBtn = wrap.closest('.q-card') && wrap.closest('.q-card').querySelector('[data-act="note"]');
    if (opBtn) opBtn.classList.toggle('has', !!v.trim());
    noteHint(btn, '已删除图片');
}

// 切题/卸载前冲刷未落盘的输入，防 <防抖窗口内丢字

function flushNoteSave() {
    for (const qid in _noteTimer) {
        if (_noteTimer[qid]) {
            clearTimeout(_noteTimer[qid]); _noteTimer[qid] = null;
            const ta = document.querySelector('.q-note-input[data-qid="' + qid + '"]');
            if (ta) { try { localStorage.setItem('examNote-' + qid, noteVal(ta)); } catch (e) { } }
        }
    }
}
window.addEventListener('pagehide', flushNoteSave);
async function fillExamNoteImgs(root) {
    if (!root) return;
    // 编辑态（编辑器可见：编辑器 DOM + 下方实时预览）里 img 节点是数据载体——
    // 回填失败绝不能 replaceWith 成文本：换掉 = editorToNote 序列化丢 [图:id] → 孤图清理删 blob → 图片永久丢失。
    // 只读态 img 由存储文本渲染，替换成「图片已丢失」仅影响显示、不伤数据。
    const sec = root.closest && root.closest('.q-note');
    const ed = sec && sec.querySelector('.q-note-input');
    const keepOnFail = !!ed && ed.style.display !== 'none';
    const imgs = root.querySelectorAll('img.exam-note-img[data-img]');
    for (const img of imgs) {
        // 已回填过（blob URL）则跳过，避免重复 createObjectURL 造成内存泄漏
        if (img.src && img.src.startsWith('blob:')) continue;
        let blob = await examImgGet(img.dataset.img);
        if (!blob) {
            // 首屏 / IndexedDB 刚打开时偶发读取失败：短延迟后重试一次（修复「刷新才有」）
            await new Promise(r => setTimeout(r, 300));
            blob = await examImgGet(img.dataset.img);
        }
        if (blob) img.src = URL.createObjectURL(blob);
        else if (_pendingImgTasks[img.dataset.img]) {
            // 图还在压缩/写库：绝不标「图片已丢失」——等写库完成后回填这一张
            const id = img.dataset.img;
            _pendingImgTasks[id].then(() => {
                if (!img.isConnected) return;
                examImgGet(id).then(b => { if (b && img.isConnected) img.src = URL.createObjectURL(b); });
            });
        }
        else if (keepOnFail) {
            // 编辑态取不到 blob（IDB 偶发失败）：保留节点与令牌，仅标记占位——保存不丢，下次进编辑自动重试
            img.classList.add('img-fail');
            img.title = '图片加载失败（保存不会丢失，重新进入编辑可恢复）';
        }
        else img.replaceWith(document.createTextNode('[图片已丢失]'));
    }
}
// 只回填指定一张图（写库完成后调用，此时必定能取到 blob）。
// 与 fillExamNoteImgs 的关键区别：拿不到也绝不 replaceWith('[图片已丢失]')——
// 同步登记的节点在压缩期间本来就没有 blob，误标会把图片节点换成文本、令牌永久丢失。
async function fillOneExamNoteImg(ta, id) {
    if (!ta || !id) return false;
    const img = ta.querySelector('img.exam-note-img[data-img="' + id + '"]');
    if (!img || (img.src && img.src.startsWith('blob:'))) return true;   // 已回填则跳过
    let blob = await examImgGet(id);
    if (!blob) { await new Promise(r => setTimeout(r, 200)); blob = await examImgGet(id); }
    if (blob) { img.src = URL.createObjectURL(blob); return true; }
    return false;
}
// 压缩/写库失败时摘掉这张图的占位节点或文本，避免留下永远取不到 blob 的空图
function removeExamNoteImgRef(ta, id) {
    if (!ta) return;
    if (ta.tagName === 'TEXTAREA') {
        ta.value = ta.value.replace(new RegExp('\\[图:' + id + '\\]', 'g'), '');
    } else {
        const img = ta.querySelector('img.exam-note-img[data-img="' + id + '"]');
        const wrap = img && img.closest('.exam-note-img-wrap');
        if (wrap) wrap.remove(); else if (img) img.remove();
    }
    noteInput(ta);
}

// ============ 配图 / 笔记贴图 单击放大（复用 exam.css 的 .zoom-overlay 遮罩） ============

function examImgPut(id, blob) {
    return examImgDB().then(d => new Promise((res, rej) => {
        const tx = d.transaction('imgs', 'readwrite');
        tx.objectStore('imgs').put(blob, id);
        tx.oncomplete = res; tx.onerror = () => rej(tx.error);
    }));
}

function mdBlockWithImg(s, editable) {
    return mdBlock(s)
        .replace(/\[图:([a-z0-9]+)\]/g,
            (_, id) => editable
                // 编辑态预览：不再渲染图片本体（图片改在编辑器内以缩略图显示，可直接查看/删除/拖拽），
                // 预览区只留一个小标记——避免被大图撑长，预览专注看公式/文字渲染效果
                ? `<span class="exam-note-img-ph" title="图片在编辑器内显示">🖼</span>`
                : `<span class="exam-note-img-wrap"><img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)"></span>`);
}

// ============ 笔记编辑体验增强（移植自 408-quiz 批注，保留 IndexedDB 架构） ============
// 贴图压缩：最长边 1200px 的 JPEG(0.85)，透明底铺白，控制 IndexedDB 体积


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
    // 防跨笔记丢图：先扫描全部 examNote-* 存储，仍被任何笔记引用的图 id 绝不删——
    // 复制含 [图:id] 的笔记文本到其他题目时两侧共享同一 blob，只在一侧删图/清空会误删另一侧的图。
    return Promise.resolve().then(() => {
        const live = new Set();
        try {
            for (let i = 0; i < localStorage.length; i++) {
                const k = localStorage.key(i);
                if (k && k.indexOf('examNote-') === 0) {
                    const v = localStorage.getItem(k) || '';
                    (v.match(/\[图:([a-z0-9]+)\]/g) || []).forEach(t => { const m = /\[图:([a-z0-9]+)\]/.exec(t); if (m) live.add(m[1]); });
                }
            }
        } catch (e) { }
        return ids.filter(id => !live.has(id));
    }).then(toDel => {
        if (!toDel.length) return Promise.resolve();
        return examImgDB().then(d => new Promise(res => {
            const tx = d.transaction('imgs', 'readwrite');
            toDel.forEach(id => tx.objectStore('imgs').delete(id));
            tx.oncomplete = res; tx.onerror = res;
        }));
    });
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
        if (act === 'note') {
            const ta = sec.querySelector('textarea, .q-note-input[contenteditable]');
            if (ta) {
                fillExamNoteImgs(ta);   // 编辑器内嵌图片回填
                const pv = sec.querySelector('.q-note-preview');
                if (pv) fillExamNoteImgs(pv);
                if (!ta.dataset.bind) {
                    ta.addEventListener('input', () => noteInput(ta));
                    ta.addEventListener('paste', notePasteImg);
                    ta.dataset.bind = '1';
                }
                if (ta.style.display !== 'none') {   // 编辑态才聚焦 + 自动保存；只读预览态不动
                    ta.focus();
                    if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);
                    noteInput(ta);
                }
                syncNoteToolbar(sec);
            }
        }
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
// 数据源切换：exam = 数二真题（exam.json，2000-2026）；core = 核心题库（core_bank.json，大观严选题 606 题）
const SRC_MODE_KEY = 'catSrcMode';
let srcMode = (function () { try { return localStorage.getItem(SRC_MODE_KEY) === 'core' ? 'core' : 'exam'; } catch (e) { return 'exam'; } })();
// 无标记优先：把未收藏、未标「不熟/不会」的题排到最前（刷题时先清「没碰过的」）
const UNMARKED_FIRST_KEY = 'catUnmarkedFirst';
let unmarkedFirst = (function () { try { return localStorage.getItem(UNMARKED_FIRST_KEY) === '1'; } catch (e) { return false; } })();
let examPapers = [];    // 真题套卷
let corePapers = [];    // 核心题库（单「卷」，内部按章节分节）
const SRC_META = {
    exam: { label: '📝 数二真题分类', title: '真题分类', sub: '按大观园三级分类（学科 / 章节 / 知识点）· 点击知识点查看跨年真题' },
    core: { label: '📘 核心题库筛选', title: '核心题库', sub: '数二核心题库（大观严选题 606 题）· 按同一棵知识点树筛选，题源标注为原真题年份' },
};
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
        const catsEl = document.getElementById('catSearch');
        localStorage.setItem(CAT_STATE_KEY, JSON.stringify({
            curCat,
            collapsedSubjects: [...collapsedSubjects],
            collapsedChapters: [...collapsedChapters],
            search: catSearchKw || '',
            scrollY: window.scrollY || 0,
        }));
    } catch (e) { }
}

// ============ 顶部栏整体折叠（与真题页同款） ============
const TOP_COLLAPSED_KEY = 'examTopCollapsed';
function toggleTopBar(force) {
    const top = document.getElementById('examTop');
    const toggle = document.getElementById('examTopToggle');
    if (!top) return;
    const collapsed = (typeof force === 'boolean') ? force : !top.classList.contains('collapsed');
    top.classList.toggle('collapsed', collapsed);
    if (toggle) toggle.classList.toggle('collapsed', collapsed);
    try { localStorage.setItem(TOP_COLLAPSED_KEY, collapsed ? '1' : '0'); } catch (e) { }
    syncTopH();
}
function restoreTopBar() {
    const collapsed = localStorage.getItem(TOP_COLLAPSED_KEY) === '1';
    toggleTopBar(collapsed);
}
// 同步顶部栏实际高度到 CSS 变量 --exam-top-h（收起=0），驱动侧栏 sticky 偏移
function syncTopH() {
    const top = document.getElementById('examTop');
    const h = (top && !top.classList.contains('collapsed')) ? top.offsetHeight : 0;
    document.documentElement.style.setProperty('--exam-top-h', h + 'px');
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
    // 核心题库题共享一个空 year 的 paper：补每题年份（从题源提取），
    // 否则年份排序出现 NaN、跨年显示为「跨 1 年」、按年份搜索不命中、复制无年份前缀。
    if (srcMode === 'core') {
        for (const e of allEntries) {
            const m = /((?:19|20)\d\d)/.exec(e.q.source || '');
            if (m) e.paper = Object.assign({}, e.paper, { year: m[1] });
        }
    }
    // 合并大观园数二真题进同一棵分类树（仅真题模式；核心题库模式不混入）
    if (srcMode === 'exam') {
        for (const e of bankItems) {
            for (const cid of e.catIds) {
                allEntries.push({ paper: e.paper, secTitle: '', q: e.q, catId: cid });
            }
        }
    }
}

// 切换数据源：真题 ⇄ 核心题库（同一棵分类树，选中知识点保持不变）
function applySrcMode(persist) {
    // 降级：核心题库数据未加载成功（fetch 失败等）时不进入 core 模式，避免空白页
    if (srcMode === 'core' && (!corePapers || !corePapers.length)) {
        srcMode = 'exam';
        try { localStorage.setItem(SRC_MODE_KEY, 'exam'); } catch (e) { }
    }
    papers = (srcMode === 'core') ? corePapers : examPapers;
    const meta = SRC_META[srcMode] || SRC_META.exam;
    const btn = document.getElementById('srcToggle');
    if (btn) {
        btn.textContent = meta.label;
        btn.title = (srcMode === 'core')
            ? '当前：核心题库。点击切回数二真题'
            : '当前：数二真题（2000-2026）。点击切换到核心题库';
    }
    const t = document.querySelector('.exam-title');
    if (t) t.textContent = meta.title;
    const sub = document.getElementById('examSub');
    if (sub) sub.textContent = meta.sub;
    if (persist) { try { localStorage.setItem(SRC_MODE_KEY, srcMode); } catch (e) { } }
}

function toggleSrcMode() {
    srcMode = (srcMode === 'core') ? 'exam' : 'core';
    applySrcMode(true);
    buildEntries();
    renderTree();
    renderMain();
    renderNav();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============ 「无标记优先」排序开关 ============
/** 该题是否「无任何标记」：未收藏 且 未标不熟/不会 */
function isUnmarked(e) {
    const qid = qidOf(e.paper.id, e.q.no);
    return !isFav(qid) && !statusOf(qid);
}

/** 排序比较器：开启「无标记优先」时无标记的排前，其余沿用「收藏时间倒序 → 年份倒序」 */
function compareEntries(a, b) {
    if (unmarkedFirst) {
        const ua = isUnmarked(a) ? 0 : 1;
        const ub = isUnmarked(b) ? 0 : 1;
        if (ua !== ub) return ua - ub;
    }
    const ta = favTime(qidOf(a.paper.id, a.q.no));
    const tb = favTime(qidOf(b.paper.id, b.q.no));
    if (ta && tb) return tb - ta;
    return parseInt(b.paper.year, 10) - parseInt(a.paper.year, 10);
}

function syncUnmarkedFirstBtn() {
    const b = document.getElementById('unmarkedFirst');
    if (!b) return;
    b.classList.toggle('on', unmarkedFirst);
    b.setAttribute('aria-pressed', unmarkedFirst ? 'true' : 'false');
    b.title = unmarkedFirst
        ? '当前：无标记题目已提前（再点恢复「收藏时间/年份」原排序）'
        : '把未做任何标记（未收藏、未标不熟/不会）的题目排到最前';
}

function toggleUnmarkedFirst() {
    unmarkedFirst = !unmarkedFirst;
    try { localStorage.setItem(UNMARKED_FIRST_KEY, unmarkedFirst ? '1' : '0'); } catch (e) { }
    syncUnmarkedFirstBtn();
    renderMain();
    renderNav();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function activeEntries() {
    // 筛选并集：收藏 / 不熟 / 不会 分别勾选；全部未选 → 不过滤（显示全部真题）
    if (!markSel.fav && !markSel.unfamiliar && !markSel.unknown) return allEntries;
    const st = statusGet();
    return allEntries.filter(e => {
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null;
        const f = markSel.fav && isFav(qid);
        const u = markSel.unfamiliar && s === 'unfamiliar';
        const k = markSel.unknown && s === 'unknown';
        return f || u || k;
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
    // 点知识点（分类树 / 掌握地图跳转）时清掉搜索词：否则 renderMain 被搜索视图挡住，
    // 出现「搜索态下点分类树/掌握地图色块无响应」。
    if (catSearchKw) {
        catSearchKw = '';
        const inp = document.getElementById('catSearch');
        if (inp) inp.value = '';
        const clr = document.getElementById('catSearchClear');
        if (clr) clr.style.display = 'none';
    }
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
        : q.type === 'blank' ? '填空' : q.type === 'calc' ? '解答'
        : q.type === 'proof' ? '证明' : secKindLabel(secTitle);
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
    // 笔记格式工具条：字色 + 高亮 + 清除（与真题页同款）
    const NOTE_COLORS = ['#e03131', '#e8590c', '#2f9e44', '#1971c2', '#9c36b5'];
    const NOTE_HLS = ['#fff3bf', '#d3f9d8', '#d0ebff', '#ffe3e3', '#ffdcc4'];
    const NOTE_TOOLBAR = `<div class="q-note-toolbar" hidden>
        <span class="q-nt-lab">字色</span>
        ${NOTE_COLORS.map(c => `<button type="button" class="q-nt-c" style="color:${c}" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'foreColor','${c}')" title="字色 ${c}">A</button>`).join('')}
        <span class="q-nt-sep"></span>
        <span class="q-nt-lab">高亮</span>
        ${NOTE_HLS.map(c => `<button type="button" class="q-nt-h" style="background:${c}" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'hiliteColor','${c}')" title="高亮 ${c}"></button>`).join('')}
        <span class="q-nt-sep"></span>
        <button type="button" class="q-nt-b" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'bold')" title="加粗 (Ctrl+B)"><b>B</b></button>
        <button type="button" class="q-nt-i" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'italic')" title="斜体 (Ctrl+I)"><i>I</i></button>
        <button type="button" class="q-nt-h1" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'h1')" title="大标题">H1</button>
        <button type="button" class="q-nt-h2" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'h2')" title="中标题">H2</button>
        <span class="q-nt-sep"></span>
        <button type="button" class="q-nt-x" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'plain')" title="转为普通正文（去掉标题/字色/高亮）">正文</button>
    </div>`;
    const editorHtml = `<div class="q-note-input" contenteditable="true" spellcheck="false" data-qid="${qid}" data-placeholder="记下你的思路、易错点、类比题…（Ctrl+V 可贴图；选中文字可上色/高亮；用 $...$ 写公式会自动渲染）"></div>`;
    const noteHtml = hasNote
        ? `<div class="q-sec q-note${hasImg ? ' has-img' : ''}" data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml.replace('<div class=', '<div style="display:none" class=')}
            <div class="q-note-preview">${mdBlockWithImg(note)}</div>
            <button class="q-note-editbtn saved" onclick="toggleNoteEdit(this)" title="编辑笔记（编辑中点击保存）">✏️ 编辑</button>
            <div class="q-note-hint"></div>
        </div>`
        : `<div class="q-sec q-note" hidden data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml}
            <div class="q-note-preview" hidden></div>
            <button class="q-note-editbtn" onclick="toggleNoteEdit(this)" title="保存笔记并收起输入框">💾 保存</button>
            <div class="q-note-hint"></div>
        </div>`;
    const noteBtn = hasNote ? `<button class="q-op has" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>`
        : `<button class="q-op" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>`;
    const paperLink = 'exam.html?paper=' + encodeURIComponent(paper.id);
    // 核心题库：不显示「年份链接」（非套卷），改显示原真题题源标签
    const yearHtml = paper.id === 'core'
        ? (q.source ? `<span class="q-year"><span class="q-year-tag" title="原真题题源">${mdInline(q.source)}</span></span>` : '')
        : paper.id === 'bank'
        ? `<span class="q-year"><span class="q-year-tag">${paper.year}年</span></span>`
        : `<span class="q-year"><a href="${paperLink}" title="在真题页打开此套卷">${paper.year}年</a></span>`;
    return `<div class="q-card" id="q-${qid}" data-qno="${q.no}">
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
            <button class="q-st-btn q-st-unfam${st === 'unfamiliar' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unfamiliar')" title="标记为「不熟」（黄色；再点取消）">不熟</button>
            <button class="q-st-btn q-st-unk${st === 'unknown' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unknown')" title="标记为「不会」（红色；再点取消）">不会</button>
            <button class="q-copy-latex" onclick="copyCatQLatex(this)" title="复制本题 LaTeX 源码（题干+选项+答案，含 $...$ 原始命令）">📋 复制</button>
            ${ideaBtn}${noteBtn}
        </div>
        ${ideaHtml}${noteHtml}
        <div class="q-sec q-answer" hidden><div class="q-answer-body">${mdBlock(q.answer || '')}</div></div>
    </div>`;
}


// 状态按钮点击：互斥切换不熟/不会，刷新按钮态 + 若正在搜索结果中刷新列表
function toggleQStatus(btn, qid, v) {
    const nv = toggleStatus(qid, v);
    const card = btn.closest('.q-card');
    if (card) {
        card.querySelectorAll('.q-st-btn').forEach(b => {
            const on = b.getAttribute('onclick').includes("'" + qid + "','" + (b.textContent.trim() === '不会' ? 'unknown' : 'unfamiliar') + "'");
            b.classList.remove('on');
        });
        if (nv) {
            const sel = nv === 'unknown' ? '.q-st-unk' : '.q-st-unfam';
            const b = card.querySelector(sel);
            if (b) b.classList.add('on');
        }
        // 若当前在"不熟/不会"筛选下被取消标记，题目应从列表消失
        if (markSel.unfamiliar && nv !== 'unfamiliar' && !markSel.unknown) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
        if (markSel.unknown && nv !== 'unknown' && !markSel.unfamiliar) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
    }
}
// 复制题文本到剪贴板（clipboard API，非安全上下文降级 execCommand）
function copyTextToClipboard(text, btn, okMsg) {
    const flash = () => {
        const old = btn.textContent;
        btn.textContent = okMsg || '已复制 ✓';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = old; btn.classList.remove('copied'); }, 1500);
    };
    const fallback = () => {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); flash(); } catch (e) { btn.textContent = '复制失败'; }
        ta.remove();
    };
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(flash).catch(fallback);
    } else fallback();
}
// 复制本题 LaTeX 源文（题干 + 选项 + 答案，保留 $...$ 原始命令）
function copyCatQLatex(btn) {
    const card = btn.closest('.q-card');
    if (!card) return;
    const qid = card.id.replace(/^q-/, '');
    let hit = null, paper = null;
    for (const e of allEntries) {
        if (qidOf(e.paper.id, e.q.no) === qid) { hit = e.q; paper = e.paper; break; }
    }
    if (!hit) return;
    let text = (paper && paper.year ? paper.year + '年 题' + hit.no + '\n' : '') + (hit.stem || '');
    if (hit.options && hit.options.length) text += '\n' + hit.options.join('\n');
    if (hit.answer) text += '\n【答案】' + hit.answer;
    copyTextToClipboard(text, btn, '已复制 ✓');
}

// ============ 渲染：主区 ============
function renderMain() {
    const el = document.getElementById('catMain');
    if (catSearchKw) { renderSearchResults(); return; }   // 搜索模式：跨分类列表
    if (curCat == null) {
        el.innerHTML = `<div class="cat-empty">← 选择左侧章节，查看该考点的历年真题</div>`;
        return;
    }
    const entries = activeEntries().filter(e => String(e.catId) === String(curCat));
    const c = cats[curCat];
    // 排序：无标记优先（可选）→ 收藏时间倒序 → 年份倒序
    entries.sort(compareEntries);
    if (!entries.length) {
        el.innerHTML = `<div class="paper-head"><h1>${c ? (c.display || c.name) : curCat}</h1><div class="paper-sub">${c ? c.path : ''}</div></div>` +
            `<div class="empty-tip">该章节下当前筛选没有匹配题目。试试切换「收藏/不熟/不会」筛选。</div>`;
        return;
    }
    const years = new Set(entries.map(e => e.paper.year)).size;
    const unmarkedN = unmarkedFirst ? entries.filter(isUnmarked).length : 0;
    let html = `<div class="paper-head">
        <h1>${c ? c.display : curCat}</h1>
        <div class="paper-sub">${c ? c.path : ''}</div>
        <div class="paper-meta">共 ${entries.length} 题 · 跨 ${years} 年${unmarkedFirst ? ` · <b>无标记优先</b>（未标记 ${unmarkedN} 题已提前）` : ''}</div>
        <button class="all-ans-btn" id="allAnsBtn" onclick="toggleAllAnswers(this)">🔼 展开全部答案</button>
    </div>`;
    const markNames = { fav: '📥收藏', unfamiliar: '🟡不熟', unknown: '🔴不会' };
    const activeMark = Object.keys(markSel).filter(k => markSel[k]);
    if (activeMark.length) html += `<div class="cat-filter-tip">筛选：${activeMark.map(k => markNames[k]).join(' / ')}</div>`;
    entries.forEach(e => { html += catCard(e.paper, e.secTitle, e.q); });
    el.innerHTML = html;
    renderMath(el);
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
    renderNav();   // 刷新悬浮题号导航
}
// ============ 顶栏搜索：题干文字 / 年份 / 题号 / 知识点路径 ============
let catSearchKw = '';                 // 当前搜索词（空 = 分类浏览模式）
let catSearchTimer = null;

function onCatSearch(v) {
    clearTimeout(catSearchTimer);
    catSearchTimer = setTimeout(() => {
        const kw = (v || '').trim();
        catSearchKw = kw;
        const clr = document.getElementById('catSearchClear');
        if (clr) clr.style.display = kw ? '' : 'none';
        renderMain();
    }, 200);
}

function clearCatSearch() {
    const inp = document.getElementById('catSearch');
    if (inp) inp.value = '';
    catSearchKw = '';
    const clr = document.getElementById('catSearchClear');
    if (clr) clr.style.display = 'none';
    renderTree();   // 退出搜索模式，恢复分类树题数
    renderMain();
}

// 搜索匹配：题干（去 LaTeX 后）、年份、题号、知识点路径 任一命中即算
function catSearchMatch(e) {
    const kw = catSearchKw.toLowerCase();
    if (!kw) return true;
    const q = e.q; const p = e.paper;
    if (String(p.year).toLowerCase().includes(kw)) return true;          // 年份
    if (String(q.no).toLowerCase().includes(kw)) return true;            // 题号
    const stem = (q.stem || '').replace(/\$[^$]*\$/g, ' ').replace(/\s+/g, ' ');
    if (stem.toLowerCase().includes(kw)) return true;                    // 题干文字
    const c = cats[String(e.catId)];
    const path = (c ? (c.path || c.name || c.display || '') : '') ;
    if (path.toLowerCase().includes(kw)) return true;                    // 知识点路径
    if ((q.answer || '').replace(/\$[^$]*\$/g, ' ').toLowerCase().includes(kw)) return true; // 答案文字
    return false;
}

// 搜索模式：主区横跨全分类列出命中题；空关键词回到分类浏览
function renderSearchResults() {
    const el = document.getElementById('catMain');
    const entries = activeEntries().filter(catSearchMatch);
    const sy = window.scrollY;
    // 无标记优先（可选）→ 收藏时间倒序 → 年份倒序
    entries.sort(compareEntries);
    const h = `<div class="paper-head">
        <h1>🔍 “${catSearchKw}”</h1>
        <div class="paper-sub">全库搜索命中 ${entries.length} 题（含大观园）</div>
        ${entries.length ? `<div class="paper-meta">共 ${entries.length} 题 · 跨 ${new Set(entries.map(e => e.paper.year)).size} 年</div>` : ''}
    </div>`;
    const markNames = { fav: '📥收藏', unfamiliar: '🟡不熟', unknown: '🔴不会' };
    const activeMark = Object.keys(markSel).filter(k => markSel[k]);
    if (activeMark.length) h += `<div class="cat-filter-tip">筛选：${activeMark.map(k => markNames[k]).join(' / ')}</div>`;
    if (!entries.length) {
        el.innerHTML = h + `<div class="empty-tip">没有匹配题目。试试别的关键词，或切换「收藏/不熟/不会」筛选。</div>`;
        return;
    }
    let html = h;
    entries.forEach(e => { html += catCard(e.paper, e.secTitle, e.q); });
    el.innerHTML = html;
    renderMath(el);
    el.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
    requestAnimationFrame(() => window.scrollTo(0, sy));
    renderNav();
}


// ============ 初始化 ============
async function init() {
    const [er, cr, br, corer] = await Promise.all([
        fetch('data/exam.json'),
        fetch('data/exam_categories.json'),
        fetch('data/bank_questions.json').catch(() => null),
        fetch('data/core_bank.json').catch(() => null),
    ]);
    if (!er.ok) throw new Error('加载真题失败: ' + er.status);
    if (!cr.ok) throw new Error('加载分类失败: ' + cr.status);
    examPapers = await er.json();
    cats = await cr.json();
    // 核心题库（大观严选题 606 题，categoryIds 已映射到同一分类体系）
    if (corer && corer.ok) {
        try {
            corePapers = await corer.json();
            coreLink = {};
            for (const s of (corePapers[0] && corePapers[0].sections) || []) {
                for (const q of s.questions || []) {
                    if (q.linkedQid) coreLink[q.no] = q.linkedQid;   // 统一主键：真题 qid
                }
            }
            migrateCoreLegacyKeys();   // 旧 'core-N' 收藏/标记/笔记 → 真题 qid（一次性）
        } catch (e) { console.error('核心题库解析失败', e); }
    } else {
        console.warn('核心题库 core_bank.json 未加载，仅提供真题源');
    }
    // 大观园真题库（categoryIds 已映射到统一分类体系，与 exam.json 合并一棵树）
    if (br && br.ok) {
        const bq = await br.json();
        const examYears = new Set(examPapers.map(p => String(p.year)));
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
    syncUnmarkedFirstBtn();
    // 恢复的选中分类若已不在分类表里（数据变更），清掉防悬空
    if (curCat !== null && !cats[String(curCat)]) { curCat = null; saveCatState(); }
    // 支持 ?cid=<知识点id> 直达（来自「分析与建议」面板的「跳转刷题」）
    const _cid = new URLSearchParams(location.search).get('cid');
    if (_cid && cats[String(_cid)]) {
        curCat = Number(_cid);
        collapsedSubjects.clear();   // 跳转时全展开，保证该知识点在树中可见
        collapsedChapters.clear();
        saveCatState();
    }
    // 顶栏折叠状态恢复（与真题页共用 examTopCollapsed，保持跨页一致）
    restoreTopBar();
    syncTopH();
    // 恢复上次搜索词 + 滚动位置（记忆做题位置）
    try {
        const st = JSON.parse(localStorage.getItem(CAT_STATE_KEY) || '{}');
        if (st.search && !location.search) {   // 有 ?cid 跳转时优先跳转，不回填搜索
            catSearchKw = st.search;
            const inp = document.getElementById('catSearch');
            if (inp) { inp.value = st.search; const clr = document.getElementById('catSearchClear'); if (clr) clr.style.display = ''; }
        }
        const _roll = st.scrollY || 0;
        if (_roll && !location.search) requestAnimationFrame(() => window.scrollTo(0, _roll));
    } catch (e) { }
    applySrcMode(false);   // 先应用上次数据源（exam / core）→ 决定 papers，再建索引
    buildEntries();
    renderTree();
    renderMain();
    renderNav();
}

// 滚动/切题时记忆位置：节流保存（复用 saveCatState 的 search/scrollY 字段）
let _catPosTimer = null;
function saveCatPosLazy() {
    if (_catPosTimer) return;
    _catPosTimer = setTimeout(() => { _catPosTimer = null; saveCatState(); }, 600);
}
window.addEventListener('scroll', saveCatPosLazy, { passive: true });
window.addEventListener('beforeunload', saveCatState);
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') saveCatState(); });

// ============ 悬浮题号导航（与真题页同款；显示当前选中分类 / 搜索结果的题号） ============
let navCollapsed = false;   // 题号球收起态（默认展开，同真题页）
function toggleFloatQ() {
    navCollapsed = !navCollapsed;
    try { localStorage.setItem('examNavCollapsed', navCollapsed ? '1' : '0'); } catch (e) { }
    const fq = document.getElementById('floatQ');
    if (fq) fq.classList.toggle('collapsed', navCollapsed);
    if (fq) fq.classList.toggle('expanded', !navCollapsed);
}
// 当前列表的题号集合：搜索模式 = 搜索结果；分类模式 = 当前分类全部题
function catNavQNos() {
    const ents = catSearchKw ? activeEntries().filter(catSearchMatch) : (curCat != null ? activeEntries().filter(e => String(e.catId) === String(curCat)) : []);
    return ents.map(e => e.q.no);
}
function renderNav() {
    const el = document.getElementById('floatQNo');
    if (!el) return;
    const list = document.getElementById('floatQList');
    const ents = catSearchKw ? activeEntries().filter(catSearchMatch) : (curCat != null ? activeEntries().filter(e => String(e.catId) === String(curCat)) : []);
    const nos = ents.map(e => e.q.no);
    const uniq = [...new Set(nos)].sort((a, b) => a - b);
    if (!uniq.length) { el.textContent = '—'; if (list) list.innerHTML = ''; return; }
    // 题号 → 掌握状态（不熟/不会），同一 no 多分类重复取任一 entry 状态即可（同题同状态）
    const stMap = {};
    for (const e of ents) {
        if (stMap[e.q.no]) continue;
        const st = statusOf(qidOf(e.paper.id, e.q.no));
        if (st) stMap[e.q.no] = st;
    }
    el.textContent = uniq.length + '题';
    list.innerHTML = uniq.map(no => {
        const st = stMap[no];
        const markCls = st ? (st === 'unknown' ? ' mark-unk' : ' mark-unf') : '';
        return `<button class="nav-q${markCls}" data-navq="${no}" title="${no} 题${st ? (st === 'unknown' ? '·🔴不会' : '·🟡不熟') : ''}" onclick="jumpToQ(${no})">${no}</button>`;
    }).join('');
    highlightNav();
}
function jumpToQ(no) {
    // 分类页：跳到首个 data-qno=no 的题卡（该题可能多分类重复，取当前列表内首个）
    const card = Array.from(document.querySelectorAll('.q-card[data-qno="' + no + '"]')).find(c => !c.closest('[hidden]'));
    if (card) card.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
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
// 还原题号球收起态 + 每次重渲染后刷新题号
(function restoreNav() {
    try { if (localStorage.getItem('examNavCollapsed') === '1') { navCollapsed = true; } } catch (e) { }
    const fq = document.getElementById('floatQ');
    if (fq) { fq.classList.toggle('collapsed', navCollapsed); fq.classList.toggle('expanded', !navCollapsed); }
})();
window.addEventListener('scroll', highlightNav, { passive: true });

init().catch(e => {
    const el = document.getElementById('catMain');
    if (el) el.innerHTML = '<div class="empty-tip">加载失败：' + esc(e.message) + '</div>';
    console.error(e);
});
