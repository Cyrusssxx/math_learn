/* 真题模块公共层：渲染 / 收藏 / 笔记贴图 / IndexedDB
 * 供 exam.js、category.js、fav.js 共用，杜绝多份副本各自漂移。
 * 抽取来源：exam.js（功能超集版本——delExamNoteImg 支持编辑态 textarea，
 * noteHint 支持 quiet 参数；在无 textarea 的只读页面可优雅降级）。
 * ⚠️ 修改本文件会同时影响三个页面，改动后务必三页都回归验证。
 */

// ============ 存储键 ============
const FAV_KEY = 'examFav';           // { 套卷id: [题no, ...] } 或 {'qid':1}
const FAV_ONLY_KEY = 'examFavOnly';  // 是否只看收藏

// ============ 模块级状态 ============
/* ⚠️ 迁移提醒：exam.js / category.js 若改为引用本文件，务必删除它们各自的同名 let 声明，
   否则 let 重复声明会直接触发 SyntaxError。 */
let favOnly = localStorage.getItem(FAV_ONLY_KEY) === '1';
let _noteLastRendered = {};   // qid → 上次渲染预览的文本（内容没变不重渲，防闪烁）
let _examImgDB = null;

// ============ 收藏存储（按题唯一 id：套卷id-题号） ============
function balanceDollars(s) {
    const n = (s.match(/\$\$/g) || []).length;
    return n % 2 === 0 ? s : s + '$$';
}

function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

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

function favGet() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || {}; } catch (e) { return {}; }
}

function favSave(obj) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(obj)); }
    catch (e) { console.error('收藏保存失败（可能超出存储配额）:', e); alert('收藏存储空间不足，保存失败。请清理部分收藏后重试。'); }
}

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

function isFav(qid) { return !!favGet()[qid]; }
function favTime(qid) {
    const v = favGet()[qid];
    return (v && typeof v === 'object') ? (v.t || 0) : 0;
}

function qidOf(paperId, no) { return paperId + '-' + no; }
function isFav(qid) { return !!favGet()[qid]; }
function favTime(qid) {
    const v = favGet()[qid];
    return (v && typeof v === 'object') ? (v.t || 0) : 0;
}

function migrateFavTimes() {
    const f = favGet();
    let changed = false;
    for (const k in f) {
        if (!f[k] || typeof f[k] !== 'object') { f[k] = { t: Date.now() }; changed = true; }
    }
    if (changed) favSave(f);
}

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
    if (favOnly) refreshAfterFavChange();
    if (typeof window.onFavChange === 'function') window.onFavChange();
}

function toggleFavOnly() {
    favOnly = !favOnly;
    localStorage.setItem(FAV_ONLY_KEY, favOnly ? '1' : '0');
    const btn = document.getElementById('favOnly');
    if (btn) btn.classList.toggle('on', favOnly);
    refreshAfterFavChange();
}

function mdInline(s) {
    return esc(s)
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
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
        // 裸 "$$" 独占一行也要开块：'$$'.endsWith('$$') 恒为真，旧条件会让多行显示块整体失效
        if (mathBuf === null && l.startsWith('$$') && (!l.endsWith('$$') || l === '$$')) {
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

function mdBlockWithImg(s) {
    return mdBlock(s)
        .replace(/\[图:([a-z0-9]+)\]/g,
            (_, id) => `<span class="exam-note-img-wrap"><img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)"></span>`);
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

function noteGet(qid) {
    try { return localStorage.getItem('examNote-' + qid) || ''; } catch (e) { return ''; }
}

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
        pv.innerHTML = mdBlockWithImg(v);
        if (v.includes('$') || v.includes('\\(') || v.includes('\\[')) renderMath(pv);
        fillExamNoteImgs(pv);
    }
    _noteLastRendered[qid] = v;   // 同步预览渲染缓存，防下次 renderNotePreview 误跳过
    const opBtn = wrap.closest('.q-card') && wrap.closest('.q-card').querySelector('[data-act="note"]');
    if (opBtn) opBtn.classList.toggle('has', !!v.trim());
    noteHint(btn, '已删除图片');
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
                    if (typeof noteInput === 'function') ta.addEventListener('input', () => noteInput(ta));
                    if (typeof notePasteImg === 'function') ta.addEventListener('paste', notePasteImg);
                    ta.dataset.bind = '1';
                }
                if (ta.style.display !== 'none') {   // 编辑态才聚焦 + 自动保存；只读预览态不动
                    ta.focus();
                    if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);
                    if (typeof noteInput === 'function') noteInput(ta);
                }
                if (typeof syncNoteToolbar === 'function') syncNoteToolbar(sec);
            }
        }
    }
}

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

async function fillOneExamNoteImg(ta, id) {
    if (!ta || !id) return;
    const img = ta.querySelector('img.exam-note-img[data-img="' + id + '"]');
    if (!img || (img.src && img.src.startsWith('blob:'))) return;   // 已回填则跳过
    let blob = await examImgGet(id);
    if (!blob) { await new Promise(r => setTimeout(r, 200)); blob = await examImgGet(id); }
    if (blob) img.src = URL.createObjectURL(blob);
}

function noteVal(el) {
    return el.tagName === 'TEXTAREA' ? el.value
        : (typeof editorToNote === 'function' ? editorToNote(el) : (el.textContent || ''));
}

function setNoteContent(el, text) {
    if (el.tagName === 'TEXTAREA') el.value = text;
    else if (typeof noteToEditor === 'function') noteToEditor(el, text);
    else el.textContent = text;
}

function autoResizeNote(el) {
    if (!el) return;
    el.style.height = 'auto';
    const maxH = Math.round(window.innerHeight * 0.6);
    el.style.height = Math.min(el.scrollHeight, maxH) + 'px';
    el.style.overflowY = el.scrollHeight > maxH ? 'auto' : 'hidden';
}


// ============ 收藏变更后的页面刷新（解耦真题页专用 renderCurrent） ============
// 只读页面（如收藏汇总页）可自行实现 window.onFavChange 来响应收藏变化；
// 未实现时若页面存在 renderCurrent（真题页）则调用之，都没有则静默跳过。
function refreshAfterFavChange() {
    if (typeof window.onFavChange === 'function') { window.onFavChange(); return; }
    if (typeof renderCurrent === 'function') renderCurrent();
}
