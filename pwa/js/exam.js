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
        btn.textContent = on ? '⭐' : '☆';   // 同步切换实心/空心星（之前只切 class 导致 UI 不更新）
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
    syncTopH();
}
function restoreTopBar() {
    const collapsed = localStorage.getItem(TOP_COLLAPSED_KEY) === '1';
    toggleTopBar(collapsed);
}
// 同步顶部栏实际高度到 CSS 变量 --exam-top-h（收起=0），驱动侧栏 sticky 偏移与主体高度
function syncTopH() {
    const top = document.getElementById('examTop');
    const h = (top && !top.classList.contains('collapsed')) ? top.offsetHeight : 0;
    document.documentElement.style.setProperty('--exam-top-h', h + 'px');
}

// ============ 思路 / 笔记（2007 试水：有 idea 字段才显示思路按钮；笔记按题存 localStorage） ============
function noteGet(qid) {
    try { return localStorage.getItem('examNote-' + qid) || ''; } catch (e) { return ''; }
}
let _noteTimer = {};
// ---- contenteditable 富编辑器：[图:id] 内嵌图片 + 字色/高亮（存储为令牌 <c:#hex>…</c> <h:#hex>…</h>） ----
const NOTE_FMT_RE = /<c:(#[0-9a-fA-F]{6})>|<h:(#[0-9a-fA-F]{6})>|<\/c>|<\/h>|<b>|<\/b>|<i>|<\/i>|<h1>|<\/h1>|<h2>|<\/h2>/g;
/** 存储文本 → 编辑器 DOM：文本/换行原样，[图:id] 变内嵌图片，格式令牌变 span/mark（栈式嵌套） */
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
            stack[stack.length - 1].appendChild(noteImgNode(m2[1]));
            i = mi + m2[0].length;
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
    del.onclick = () => delExamNoteImg(id, del);
    wrap.append(img, del);
    return wrap;
}
/** 编辑器 DOM → 存储文本：图片还原 [图:id]，带格式的文本节点包令牌（字色/高亮/粗体/斜体走行内令牌，H1/H2 走块级令牌包裹整段） */
function editorToNote(el) {
    const rgbToHex = v => {
        const m = /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(v || '');
        return m ? '#' + [1, 2, 3].map(k => (+m[k]).toString(16).padStart(2, '0')).join('') : null;
    };
    const isBold = n => (n && n.nodeType === 1) && (n.tagName === 'B' || n.tagName === 'STRONG' || /bold/i.test(n.style.fontWeight || ''));
    const isItalic = n => (n && n.nodeType === 1) && (n.tagName === 'I' || n.tagName === 'EM' || /italic/i.test(n.style.fontStyle || ''));
    // 返回序列化片段；c/h=字色/高亮 hex，b/i=是否处于粗/斜上下文（行内令牌），heading 由 H1/H2 元素单独包块级令牌
    return (function run(n, c, h, b, i) {
        let s = '';
        for (const ch of n.childNodes) {
            if (ch.nodeType === 3) {
                const t = ch.nodeValue.replace(/\u00A0/g, ' ');
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
                    const block = ch.tagName === 'DIV' || ch.tagName === 'P';
                    if (block && s && !s.endsWith('\n')) s += '\n';
                    s += run(ch, c, h, true, i);
                    if (block && s && !s.endsWith('\n')) s += '\n';
                }
                else if (isItalic(ch)) {
                    s += run(ch, c, h, b, true);
                }
                else {
                    let nc = c, nh = h;
                    if (ch.style) {
                        const hc = rgbToHex(ch.style.color); if (hc) nc = hc;
                        const hb = rgbToHex(ch.style.backgroundColor); if (hb) nh = hb;
                    }
                    const block = ch.tagName === 'DIV' || ch.tagName === 'P';
                    if (block && s && !s.endsWith('\n')) s += '\n';
                    s += run(ch, nc, nh, b, i);
                    if (block && s && !s.endsWith('\n')) s += '\n';
                }
            }
        }
        return s;
    })(el, null, null, false, false);
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
function noteInput(ta) {
    const qid = ta.dataset.qid;
    const newVal = noteVal(ta);
    const newRefs = examImgRefs(newVal);
    if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);   // 编辑器自增长，无需 JS 调高
    noteHint(ta, '自动保存中…', true);
    clearTimeout(_noteTimer[qid]);
    _noteTimer[qid] = setTimeout(() => {
        const olds = localStorage.getItem('examNote-' + qid) || '';
        const oldRefs = examImgRefs(olds);
        const orphan = oldRefs.filter(id => !newRefs.includes(id));
        if (orphan.length) examImgDel(orphan);   // 清理不再引用的图，避免存储泄漏
        try { localStorage.setItem('examNote-' + qid, newVal); } catch (e) { }
        const btn = ta.closest('.q-card') && ta.closest('.q-card').querySelector('[data-act="note"]');
        if (btn) btn.classList.toggle('has', !!newVal.trim());
        noteHint(ta, newVal.trim() ? '已保存 ✓' : '笔记是空的，不保存');
        // 编辑态实时预览：内容有变化才重渲染（KaTeX/图片回填开销大，无变化重渲是闪烁根源）
        if (ta.style.display !== 'none') renderNotePreview(ta);
    }, 1500);
}
// 编辑态实时预览：从编辑器当前内容渲染 Markdown + 图片（内容未变直接跳过，避免闪烁）
function renderNotePreview(ta) {
    const sec = ta.closest('.q-note');
    const pv = sec && sec.querySelector('.q-note-preview');
    if (!pv) return;
    const v = noteVal(ta);
    if (_noteLastRendered[ta.dataset.qid] === v) return;   // 内容没变：跳过
    _noteLastRendered[ta.dataset.qid] = v;
    pv.hidden = false;
    pv.innerHTML = mdBlockWithImg(v);
    if (v.includes('$') || v.includes('\\(') || v.includes('\\[')) renderMath(pv);
    fillExamNoteImgs(pv);   // 异步回填 IndexedDB 中的 blob
}
// 笔记区 Ctrl+V 贴图：压缩后存 IndexedDB，再在光标处插入内嵌图片（编辑器）或 [图:id]（textarea）
function notePasteImg(e) {
    const it = [...(e.clipboardData?.items || [])].find(i => i.type.startsWith('image/'));
    if (!it) {
        // 富文本粘贴降级为纯文本，防外来 HTML 污染编辑器
        if (e.target.tagName !== 'TEXTAREA' && e.clipboardData?.getData) {
            e.preventDefault();
            const txt = e.clipboardData.getData('text/plain');
            if (txt) document.execCommand('insertText', false, txt);
        }
        return;
    }
    e.preventDefault();
    const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    const ta = e.target;
    compressImage(it.getAsFile()).then(blob => examImgPut(id, blob)).then(() => {
        if (ta.tagName === 'TEXTAREA') {
            const tag = `[图:${id}]`;
            const p = ta.selectionStart;
            ta.value = ta.value.slice(0, p) + tag + ta.value.slice(ta.selectionEnd);
            ta.selectionStart = ta.selectionEnd = p + tag.length;
        } else {
            ta.focus();
            const sel = getSelection();
            if (sel && sel.rangeCount && ta.contains(sel.anchorNode)) {
                const range = sel.getRangeAt(0);
                range.deleteContents();
                range.insertNode(noteImgNode(id));
                range.collapse(false);
            } else {
                ta.appendChild(noteImgNode(id));
            }
        }
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
    if (open && act !== 'note') {
        renderMath(sec);   // 展开答案/思路时渲染 KaTeX
    }
    if (act === 'note') {
        const ta = sec.querySelector('textarea, .q-note-input[contenteditable]');
        if (ta) {
            if (open) {
                const pv = sec.querySelector('.q-note-preview');
                fillExamNoteImgs(sec.querySelector('.q-note-input'));   // 编辑器内嵌图片回填
                if (pv) fillExamNoteImgs(pv);   // 展开笔记时确保预览里贴图已回填
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
// 笔记格式工具条：对当前选区应用 加粗/斜体/标题/字色/高亮/清除
function applyNoteFormat(sec, cmd, val) {
    const ed = sec.querySelector('.q-note-input');
    if (!ed || ed.style.display === 'none' || !ed.isContentEditable) return;
    const sel = getSelection();
    const inEd = !!sel.rangeCount && ed.contains(sel.anchorNode);
    // 'plain'（转普通正文）允许光标直接停在标题行内，无需先选中文字
    if (!inEd || (sel.isCollapsed && cmd !== 'plain')) {
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
// 空笔记「💾 保存」：立即落盘并收起输入框——非空转为「有笔记」形态（预览 + ✏️ 编辑），空则收起整节
function saveNoteBtn(btn) {
    const sec = btn.closest('.q-note');
    const ta = sec.querySelector('.q-note-input');
    const pv = sec.querySelector('.q-note-preview');
    const qid = ta.dataset.qid;
    clearTimeout(_noteTimer[qid]);
    delete _noteTimer[qid];
    const v = noteVal(ta);
    try { localStorage.setItem('examNote-' + qid, v); } catch (e) { }
    const opBtn = sec.closest('.q-card')?.querySelector('[data-act="note"]');
    if (v.trim()) {
        ta.style.display = 'none';
        btn.style.display = 'none';
        syncNoteToolbar(sec);
        sec.classList.toggle('has-img', /\[图:[a-z0-9]+\]/.test(v));
        if (pv) {
            pv.innerHTML = mdBlockWithImg(v);
            pv.hidden = false;
            if (v.includes('$') || v.includes('\\(') || v.includes('\\[')) renderMath(pv);
            fillExamNoteImgs(pv);
        }
        const edit = sec.querySelector('.q-note-editbtn');
        if (edit) {
            edit.style.display = '';
            edit.textContent = '✏️ 编辑';
            edit.classList.add('saved');
            noteHint(edit, '已保存 ✓');
        }
        if (opBtn) opBtn.classList.add('has');
    } else {
        sec.hidden = true;
        if (opBtn) opBtn.classList.remove('has');
        noteHint(btn, '笔记是空的，未保存');
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
        btn.textContent = '💾 保存';
        btn.classList.remove('saved');   // 再次编辑恢复按钮常态
        noteHint(btn, '');
        ta.style.display = '';
        if (!ta.dataset.bind) {
            ta.addEventListener('input', () => noteInput(ta));
            ta.addEventListener('paste', notePasteImg);
            ta.dataset.bind = '1';
        }
        if (ta.tagName !== 'TEXTAREA' && !ta.childNodes.length) {
            setNoteContent(ta, noteGet(ta.dataset.qid));   // 编辑器首次展开：从存储重建（含内嵌图片）
        }
        fillExamNoteImgs(ta);   // 编辑器内嵌图片回填 blob
        syncNoteToolbar(sec);
        ta.focus();
        if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);
    } else {
        // 完成：清防抖定时器，立即落盘
        clearTimeout(_noteTimer[ta.dataset.qid]);
        delete _noteTimer[ta.dataset.qid];
        const raw = noteVal(ta);
        try { localStorage.setItem('examNote-' + ta.dataset.qid, raw); } catch (e) { }
        const v = raw.trim();
        if (v) {
            btn.textContent = '✏️ 编辑';
            btn.classList.add('saved');   // 保存后淡化按钮
            ta.style.display = 'none';
            syncNoteToolbar(sec);
            if (pv) {
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
            ta.style.display = '';
            setNoteContent(ta, '');
            const sb = sec.querySelector('.q-note-savebtn');
            if (sb) sb.style.display = '';
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
// 外包 .exam-note-img-wrap 以支持单图删除按钮（hover 显示 ×）
function mdBlockWithImg(s) {
    return mdBlock(s)
        .replace(/\[图:([a-z0-9]+)\]/g,
            (_, id) => `<span class="exam-note-img-wrap"><img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)"><button type="button" class="exam-note-img-del" title="删除图片" onclick="delExamNoteImg('${id}', this)">×</button></span>`);
}

// ============ 笔记编辑体验增强（移植自 408-quiz 批注，保留 IndexedDB 架构） ============
// 贴图压缩：最长边 1200px 的 JPEG(0.85)，透明底铺白，控制 IndexedDB 体积
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
    v = v.replace(re, '').replace(/\s{2,}/g, ' ').trim();
    try { localStorage.setItem('examNote-' + qid, v); } catch (e) { }
    examImgDel([id]);
    if (ta) setNoteContent(ta, v);
    const pv = wrap.querySelector('.q-note-preview');
    if (pv && !pv.hidden) {
        pv.innerHTML = mdBlockWithImg(v);
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
        '<textarea class="review-pop-ta" spellcheck="false" placeholder="写下对这套卷的整体点评：难度、易错点、时间分配、复习建议…（自动保存）"></textarea>' +
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
        // 笔记标题令牌（<h1>/<h2>）独占整行时作为块级标题输出，不放进 <p>
        if (l.startsWith('<h1>') || l.startsWith('<h2>')) {
            out.push(mdInline(l));
        } else {
            out.push('<p>' + mdInline(l) + '</p>');
        }
    }
    // 未闭合的 $$ 当普通行
    if (mathBuf) out.push('<p>' + mdInline(mathBuf) + '</p>');
    // 笔记令牌还原（存储经 esc 后形如 &lt;b&gt;…&lt;/b&gt;；高亮/字色 → 行内标签，粗体/斜体 → 行内标签，H1/H2 → 块级标题）
    return out.join('')
        .replace(/&lt;h:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/h&gt;/g, '<mark class="note-hl" style="background:$1">$2</mark>')
        .replace(/&lt;c:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/c&gt;/g, '<span style="color:$1">$2</span>')
        .replace(/&lt;b&gt;([\s\S]*?)&lt;\/b&gt;/g, '<b>$1</b>')
        .replace(/&lt;i&gt;([\s\S]*?)&lt;\/i&gt;/g, '<i>$1</i>')
        .replace(/&lt;h1&gt;([\s\S]*?)&lt;\/h1&gt;/g, '<h1>$1</h1>')
        .replace(/&lt;h2&gt;([\s\S]*?)&lt;\/h2&gt;/g, '<h2>$1</h2>');
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
    const hasImg = /\[图:[a-z0-9]+\]/.test(note);
    // 编辑器：contenteditable 富文本，[图:id] 直接以内嵌图片呈现（不再显示占位文本）
    // 笔记格式工具条：字色 + 高亮 + 清除（作用于选区）
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
            <div class="q-note-preview">${mdBlockWithImg(note)}</div>
            ${NOTE_TOOLBAR}
            ${editorHtml.replace('<div class=', '<div style="display:none" class=')}
            <button class="q-note-editbtn" onclick="toggleNoteEdit(this)" title="编辑笔记">✏️ 编辑</button>
            <div class="q-note-hint"></div>
        </div>`
        : `<div class="q-sec q-note" hidden data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml}
            <div class="q-note-preview" hidden></div>
            <button class="q-note-savebtn" onclick="saveNoteBtn(this)" title="保存笔记并收起输入框">💾 保存</button>
            <button class="q-note-editbtn" style="display:none" onclick="toggleNoteEdit(this)" title="编辑笔记">✏️ 编辑</button>
            <div class="q-note-hint"></div>
        </div>`;
    const ideaBtn = q.idea ? `<button class="q-op" data-act="idea" onclick="toggleQSec(this,'idea')">思路</button>` : '';
    const ideaHtml = q.idea ? `<div class="q-sec q-idea" hidden>${mdBlock(q.idea)}</div>` : '';
    // 📌 点睛：本题专属 公式/易错/技巧/注意 四段块（数据来自源 md ::: 点睛）
    const TIP_META = [
        ['gs', '📌 公式', 'tip-gs'],
        ['yc', '⚠️ 易错', 'tip-yc'],
        ['jq', '💡 技巧', 'tip-jq'],
        ['zy', '🔍 注意', 'tip-zy'],
    ];
    let tipsHtml = '';
    if (q.tips) {
        const secs = TIP_META.filter(([k]) => q.tips[k])
            .map(([k, label, cls]) => `<div class="q-tip-sec ${cls}"><div class="q-tip-label">${label}</div><div class="q-tip-body">${mdBlock(q.tips[k])}</div></div>`).join('');
        if (secs) {
            tipsHtml = `<div class="q-sec q-tips" hidden>${secs}</div>`;
        }
    }
    const tipsBtn = tipsHtml ? `<button class="q-op q-tips-btn" data-act="tips" onclick="toggleQSec(this,'tips')" title="本题专属公式/易错点/技巧/注意">📌 点睛</button>` : '';
    return `<div class="q-card" id="q-${qid}" data-qno="${q.no}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindTag}</span>
            ${fav && favTime(qid) ? `<span class="q-fav-date" title="收藏于 ${fmtFavTime(favTime(qid))}">${fmtFavShort(favTime(qid))}</span>` : ''}
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="${fav ? (favTime(qid) ? '收藏于 ' + fmtFavTime(favTime(qid)) : '已收藏') : '收藏此题'}">${fav ? '⭐' : '☆'}</button>
        </div>
        <div class="q-body">${stem}${figHtml}${options}</div>
        <div class="q-ops">
            <button class="q-op" data-act="answer" onclick="toggleQSec(this,'answer')">查看答案</button>
            ${ideaBtn}
            ${tipsBtn}
            <button class="q-op${hasNote ? ' has' : ''}" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>
        </div>
        ${ideaHtml}
        ${tipsHtml}
        ${noteHtml}
        <div class="q-sec q-answer" hidden><div class="q-answer-body">${mdBlock(q.answer)}</div></div>
    </div>`;
}

function secTag(secIdx) {
    return ['一', '二', '三', '四', '五'][secIdx] || (secIdx + 1);
}

// 一键展开/收起当前卷所有题卡的答案
let examAllAnsOpen = false;
function examToggleAllAnswers(btn) {
    examAllAnsOpen = !examAllAnsOpen;
    const el = document.getElementById('examMain');
    if (!el) return;
    el.querySelectorAll('.q-card').forEach(card => {
        const sec = card.querySelector('.q-answer');
        const b = card.querySelector('.q-op[data-act="answer"]');
        if (sec) sec.hidden = !examAllAnsOpen;
        if (b) {
            b.classList.toggle('on', examAllAnsOpen);
            b.textContent = examAllAnsOpen ? '收起答案' : '查看答案';
        }
    });
    if (examAllAnsOpen) {
        renderMath(el);
        fillExamNoteImgs(el);
    }
    btn.classList.toggle('on', examAllAnsOpen);
    btn.textContent = examAllAnsOpen ? '🔽 收起全部答案' : '🔼 展开全部答案';
}

function renderCurrent() {
    examAllAnsOpen = false;   // 切卷/重绘时重置
    const el = document.getElementById('examMain');
    if (!curPaper) { el.innerHTML = '<div class="loading">请选择一套卷</div>'; return; }
    const review = reviewGet(curPaper.id);
    const reviewText = review.trim();
    let html = `<div class="paper-head">
        <div class="paper-head-top">
            <h1>${curPaper.title}</h1>
            <button class="review-btn${review.trim() ? ' has' : ''}" data-pid="${curPaper.id}" title="写试卷点评" onclick="openReviewPop('${curPaper.id}', this)">▦</button>
        </div>
        <div class="paper-meta">共 ${curPaper.sections.reduce((a, s) => a + s.questions.length, 0)} 题 · 满分 150 分</div>
        ${reviewText ? `<div class="paper-review-line">💬 ${esc(reviewText)}</div>` : ''}
        <button class="all-ans-btn" id="examAllAnsBtn" onclick="examToggleAllAnswers(this)">🔼 展开全部答案</button>
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
    const el = document.getElementById('q-' + qidOf(curPaper.id, no));
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

let _qPosTimer = null;
window.addEventListener('scroll', () => {
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
    // 支持分类页下钻：exam.html?paper=<套卷id> 直接定位到该套卷
    const up = new URLSearchParams(location.search);
    const wantPaper = up.get('paper');
    if (wantPaper) {
        const wp = papers.find(x => x.id === wantPaper);
        if (wp) { startPaper = wp; startNo = null; }
    }
    curPaper = startPaper;
    renderPaperList();
    renderCurrent();
    const sub = document.getElementById('examSub');
    if (sub && curPaper) sub.textContent = curPaper.title;
    // 顶部栏整体折叠（恢复上次状态）+ 高度联动：必须放在定位之前，
    // 否则顶栏由折叠变展开会撑高文档、把刚定位好的题号顶偏。
    restoreTopBar();
    syncTopH();
    // 滚动到上次题号（收藏过滤下该题可能被隐藏，找不到则留在顶部）
    if (startNo) {
        const qid = qidOf(curPaper.id, startNo);
        const go = () => {
            const el = document.getElementById('q-' + qid);
            if (el) el.scrollIntoView({ block: 'start' });
        };
        go();
        // 批注贴图从 IndexedDB 异步回填、KaTeX 渲染都会改变文档高度，稳定后再校准
        requestAnimationFrame(go);
        window.addEventListener('load', go, { once: true });
    }
    if (window.ResizeObserver) {
        new ResizeObserver(syncTopH).observe(document.getElementById('examTop'));
    } else {
        window.addEventListener('resize', syncTopH);
    }
}

init();
