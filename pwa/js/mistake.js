/* 考研数学笔记 - 易错本：自由记录的独立模块
 * 数据：localStorage 'mistakeNotes' = [{id,title,tags:[],body,created,updated,pinned}]
 * 贴图：IndexedDB 'mistakeNoteImg'（与做题笔记 examNoteImg / 批注 notesAnnotImg 完全隔离）
 * 编辑器 token 体系与 exam.js 同源，但全部加 mb 前缀实现，绝不共用全局变量。
 * 视图：body.mb-open 时隐藏 #docPane、显示 #mbView；左栏目录树 + 右栏原样保留。
 */
(function () {
    'use strict';

    // ============ 常量 ============
    var LS = 'mistakeNotes';
    var VIEW_KEY = 'mistakeView';           // '1' = 刷新后仍在易错本
    var IDB_NAME = 'mistakeNoteImg';
    // 预设标签：全部大章节（高数 9 + 线代 6），剔除两篇真题点睛与隐藏的考前21记
    var PRESET_TAGS = [
        '高数0-中学公式速查', '高数1-极限', '高数2-一元微分',
        '高数3.1-一元积分-计算', '高数3.2-一元积分-应用', '高数3.3-反常积分',
        '高数4-微分方程', '高数5-多元微分', '高数6-二重积分',
        '线代1-行列式', '线代2-矩阵', '线代3-向量',
        '线代4-线性方程组', '线代5-特征值与相似', '线代6-二次型'
    ];
    var FMT_RE = /<c:(#[0-9a-fA-F]{6})>|<h:(#[0-9a-fA-F]{6})>|<\/c>|<\/h>|<b>|<\/b>|<i>|<\/i>|<h1>|<\/h1>|<h2>|<\/h2>/g;
    var COLORS = ['#c0392b', '#d35400', '#2980b9', '#27ae60'];
    var HLS = ['#ffe8b8', '#b6efb6', '#b7dcff', '#ffb3ba'];

    // ============ 通用小工具（隔离，不依赖全局 esc / balanceDollars） ============
    function esc(s) {
        return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
    function balanceDollars(s) {
        var n = (String(s).match(/\$\$/g) || []).length;
        return n % 2 === 0 ? s : s + '$$';
    }
    function uid() {
        return 'mb' + (window.crypto && crypto.randomUUID ? crypto.randomUUID().replace(/-/g, '') : (Date.now().toString(36) + Math.random().toString(36).slice(2, 10)));
    }
    function fmtTime(ts) {
        var d = new Date(ts), now = new Date();
        var p = function (n) { return String(n).padStart(2, '0'); };
        if (d.getFullYear() === now.getFullYear())
            return (d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
        return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
    }

    // ============ 数据层 ============
    function load() {
        try {
            var a = JSON.parse(localStorage.getItem(LS) || '[]');
            return Array.isArray(a) ? a : [];
        } catch (e) { return []; }
    }
    function save(list) {
        try { localStorage.setItem(LS, JSON.stringify(list)); return true; }
        catch (e) { alert('保存失败：存储空间可能已满，请到设置里导出数据备份。'); return false; }
    }
    function find(id) {
        var a = load();
        for (var i = 0; i < a.length; i++) if (a[i].id === id) return a[i];
        return null;
    }
    function upsert(rec) {
        var a = load(), hit = false;
        for (var i = 0; i < a.length; i++) if (a[i].id === rec.id) { a[i] = rec; hit = true; break; }
        if (!hit) a.unshift(rec);
        return save(a);
    }

    // ============ 独立贴图库 ============
    var _db = null;
    function imgDB() {
        if (!_db) _db = new Promise(function (res, rej) {
            var rq = indexedDB.open(IDB_NAME, 1);
            rq.onupgradeneeded = function () { rq.result.createObjectStore('imgs'); };
            rq.onsuccess = function () { res(rq.result); };
            rq.onerror = function () { rej(rq.error); };
        });
        return _db;
    }
    function imgPut(id, blob) {
        return imgDB().then(function (d) {
            return new Promise(function (res, rej) {
                var done = false;
                var tx = d.transaction('imgs', 'readwrite');
                tx.objectStore('imgs').put(blob, id);
                tx.oncomplete = function () { done = true; res(); };
                tx.onerror = function () { done = true; rej(tx.error); };
                setTimeout(function () { if (!done) res(); }, 60); // 兜底：个别环境回调不触发
            });
        });
    }
    function imgGet(id) {
        return imgDB().then(function (d) {
            return new Promise(function (res) {
                var rq = d.transaction('imgs').objectStore('imgs').get(id);
                rq.onsuccess = function () { res(rq.result || null); };
                rq.onerror = function () { res(null); };
            });
        });
    }
    function imgDel(ids) {
        if (!ids || !ids.length) return Promise.resolve();
        return Promise.resolve().then(function () {
            // 跨笔记共享保护：仍被其他易错笔记引用的图绝不删
            var all = load(), live = {};
            all.forEach(function (r) { refsOf(r.body).forEach(function (id) { live[id] = 1; }); });
            return ids.filter(function (id) { return !live[id]; });
        }).then(function (toDel) {
            if (!toDel.length) return;
            return imgDB().then(function (d) {
                return new Promise(function (res) {
                    var tx = d.transaction('imgs', 'readwrite');
                    toDel.forEach(function (id) { tx.objectStore('imgs').delete(id); });
                    tx.oncomplete = res; tx.onerror = res;
                });
            });
        });
    }
    function refsOf(t) {
        return String(t || '').match(/\[图:([a-z0-9]+)\]/g) ?
            String(t).match(/\[图:([a-z0-9]+)\]/g).map(function (m) { return m.slice(3, -1); }) : [];
    }
    function compress(file) {
        return new Promise(function (res, rej) {
            var fr = new FileReader();
            fr.onerror = rej;
            fr.onload = function () {
                var im = new Image();
                im.onerror = rej;
                im.onload = function () {
                    var max = 1400, w = im.width, h = im.height;
                    if (w > max || h > max) { var s = Math.min(max / w, max / h); w = Math.round(w * s); h = Math.round(h * s); }
                    var cv = document.createElement('canvas'); cv.width = w; cv.height = h;
                    cv.getContext('2d').drawImage(im, 0, 0, w, h);
                    cv.toBlob(function (b) { b ? res(b) : rej(new Error('compress fail')); }, 'image/jpeg', 0.85);
                };
                im.src = fr.result;
            };
            fr.readAsDataURL(file);
        });
    }
    var _pending = {}, _writing = {};
    function waitPendingImgs() {
        var tasks = Object.keys(_pending).map(function (k) { return _pending[k]; }).filter(Boolean);
        return tasks.length ? Promise.all(tasks).catch(function () { }) : Promise.resolve();
    }

    // ============ 编辑器：token <-> contenteditable DOM（exam.js 同源，独立实现） ============
    function hexColor(v) {
        if (!v) return null;
        var s = String(v).trim();
        if (/^#[0-9a-fA-F]{6}$/.test(s)) return s.toLowerCase();
        if (/^#[0-9a-fA-F]{3}$/.test(s)) return '#' + s.slice(1).split('').map(function (c) { return c + c; }).join('').toLowerCase();
        var m = /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(s);
        if (!m) {
            var t = document.createElement('span'); t.style.color = s;
            m = /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(t.style.color || '');
        }
        return m ? '#' + [1, 2, 3].map(function (k) { return (+m[k]).toString(16).padStart(2, '0'); }).join('') : null;
    }
    function noteToEditor(el, text) {
        el.innerHTML = '';
        var stack = [el];
        function emit(s) {
            s.split('\n').forEach(function (line, k) {
                if (k > 0) stack[stack.length - 1].appendChild(document.createElement('br'));
                if (line) stack[stack.length - 1].appendChild(document.createTextNode(line));
            });
        }
        var i = 0;
        while (i < text.length) {
            var mi = text.indexOf('[图:', i);
            FMT_RE.lastIndex = i;
            var mf = FMT_RE.exec(text);
            if (mf && (mi < 0 || mf.index <= mi)) {
                emit(text.slice(i, mf.index));
                var m0 = mf[0];
                if (/^<\/(c|h|b|i|h1|h2)>$/.test(m0)) { if (stack.length > 1) stack.pop(); }
                else {
                    var node;
                    if (m0 === '<b>') node = document.createElement('b');
                    else if (m0 === '<i>') node = document.createElement('i');
                    else if (m0 === '<h1>') node = document.createElement('h1');
                    else if (m0 === '<h2>') node = document.createElement('h2');
                    else if (mf[1]) { node = document.createElement('span'); node.style.color = mf[1]; }
                    else { node = document.createElement('mark'); node.style.background = mf[2]; }
                    stack[stack.length - 1].appendChild(node); stack.push(node);
                }
                i = mf.index + m0.length;
            } else if (mi >= 0) {
                emit(text.slice(i, mi));
                var m2 = /\[图:([a-z0-9]+)\]/.exec(text.slice(mi));
                if (m2) stack[stack.length - 1].appendChild(imgNode(m2[1]));
                i = mi + (m2 ? m2[0].length : 1);
            } else { emit(text.slice(i)); i = text.length; }
        }
    }
    function editorToNote(el) {
        function run(n, c, h, b, it) {
            var s = '';
            Array.prototype.slice.call(n.childNodes).forEach(function (ch) {
                if (ch.nodeType === 3) {
                    var t = ch.nodeValue.replace(/\u200B/g, '').replace(/ {2,}/g, function (m) { return m.replace(/ /g, '\u00A0'); });
                    if (!t) return;
                    var inner = t;
                    if (it) inner = '<i>' + inner + '</i>';
                    if (b) inner = '<b>' + inner + '</b>';
                    if (h) inner = '<h:' + h + '>' + inner + '</h>';
                    if (c) inner = '<c:' + c + '>' + inner + '</c>';
                    s += inner; return;
                }
                if (ch.nodeType !== 1) return;
                if (ch.tagName === 'BR') { s += '\n'; return; }
                var img = ch.tagName === 'IMG' ? ch : ch.querySelector('img[data-img]');
                if (img && img.dataset.img) { s += '[图:' + img.dataset.img + ']'; return; }
                if (ch.tagName === 'H1' || ch.tagName === 'H2') {
                    // 标题内部的行内格式（加粗/斜体/字色/高亮）必须一起带走，和 exam.js 同源
                    var nc0 = hexColor(ch.style && ch.style.color) || c;
                    var nh0 = hexColor(ch.style && ch.style.backgroundColor) || h;
                    var nb0 = b || /bold/i.test(ch.style && ch.style.fontWeight || '');
                    var ni0 = it || /italic/i.test(ch.style && ch.style.fontStyle || '');
                    s += '<' + ch.tagName.toLowerCase() + '>' + run(ch, nc0, nh0, nb0, ni0) + '</' + ch.tagName.toLowerCase() + '>';
                    return;
                }
                var nc = c, nh = h, nb = b, ni = it;
                var hc = hexColor(ch.style && ch.style.color), hb = hexColor(ch.style && ch.style.backgroundColor);
                if (hc) nc = hc;
                if (hb) nh = hb;
                if (ch.getAttribute && ch.getAttribute('color')) { var fc = hexColor(ch.getAttribute('color')); if (fc) nc = fc; }
                if (ch.getAttribute && ch.getAttribute('bgcolor')) { var fb = hexColor(ch.getAttribute('bgcolor')); if (fb) nh = fb; }
                if (ch.tagName === 'B' || ch.tagName === 'STRONG' || /bold/i.test(ch.style && ch.style.fontWeight)) nb = true;
                if (ch.tagName === 'I' || ch.tagName === 'EM' || /italic/i.test(ch.style && ch.style.fontStyle)) ni = true;
                s += run(ch, nc, nh, nb, ni);
            });
            return s;
        }
        return run(el, null, null, false, false).replace(/\n+$/, '').replace(/^\n+/, '');
    }
    function zoomMb(img) {
        var src = img && img.src; if (!src) return;
        // 复用笔记页/题目页同一套放大遮罩（滚轮缩放、拖动、Esc 关闭），不再新开标签页
        if (typeof window.openLightbox === 'function') window.openLightbox(src);
        else if (typeof window.zoomOverlayOpen === 'function') window.zoomOverlayOpen(src);
    }
    function bindZoom(root) {
        root.querySelectorAll('img[data-img]').forEach(function (img) {
            img.style.cursor = 'zoom-in';
            img.onclick = function (e) { if (e) e.stopPropagation(); zoomMb(img); };
        });
    }
    function imgNode(id) {
        var wrap = document.createElement('span');
        wrap.className = 'mb-img-wrap'; wrap.draggable = true;
        var img = document.createElement('img');
        img.className = 'mb-img'; img.dataset.img = id; img.alt = '易错本图片';
        img.setAttribute('contenteditable', 'false');
        img.onclick = function (e) { if (e) e.stopPropagation(); zoomMb(img); };
        var del = document.createElement('button');
        del.type = 'button'; del.className = 'mb-img-del'; del.textContent = '×'; del.title = '删除图片';
        del.onclick = function () { wrap.remove(); markDirty(); };
        wrap.append(img, del);
        wrap.addEventListener('dragstart', function (e) {
            e.dataTransfer.setData('text/plain', id); e.dataTransfer.effectAllowed = 'move'; wrap.classList.add('dragging');
        });
        wrap.addEventListener('dragend', function () { wrap.classList.remove('dragging'); });
        wrap.addEventListener('dragover', function (e) { e.preventDefault(); wrap.classList.add('over'); });
        wrap.addEventListener('dragleave', function () { wrap.classList.remove('over'); });
        wrap.addEventListener('drop', function (e) {
            e.preventDefault(); wrap.classList.remove('over');
            var dragged = document.querySelector('.mb-img-wrap.dragging');
            if (!dragged || dragged === wrap) return;
            var r = wrap.getBoundingClientRect();
            if ((e.clientY - r.top) > r.height / 2) wrap.after(dragged); else wrap.before(dragged);
            markDirty();
        });
        imgGet(id).then(function (blob) { if (blob) img.src = URL.createObjectURL(blob); });
        return wrap;
    }
    function fillImgs(root) {
        root.querySelectorAll('img[data-img]').forEach(function (img) {
            imgGet(img.dataset.img).then(function (blob) { if (blob) img.src = URL.createObjectURL(blob); });
        });
    }
    function pasteImg(e) {
        var ed = e.target;
        var items = Array.prototype.slice.call((e.clipboardData && e.clipboardData.items) || []);
        var files = items.filter(function (i) { return i.type && i.type.indexOf('image/') === 0; })
            .map(function (i) { return i.getAsFile(); }).filter(Boolean);
        if (!files.length && e.clipboardData && e.clipboardData.getData) {
            var html = '';
            try { html = e.clipboardData.getData('text/html') || ''; } catch (err) { }
            files = Array.prototype.slice.call(html.matchAll(/<img[^>]+src=["'](data:image\/[^"']+)["']/gi)).map(function (m) {
                try {
                    var src = m[1], i = src.indexOf(','), meta = src.slice(5, i);
                    return new File([Uint8Array.from(atob(src.slice(i + 1)), function (c) { return c.charCodeAt(0); })], 'img.png', { type: meta.split(';')[0] });
                } catch (err) { return null; }
            }).filter(Boolean);
        }
        if (!files.length) return; // 纯文本走浏览器默认粘贴，input 事件里 markDirty
        e.preventDefault();
        files.forEach(function (file) { pasteOne(ed, file); });
    }
    function pasteOne(ed, raw) {
        var id = uid();
        var node = imgNode(id);
        var sel = window.getSelection(), range = sel && sel.rangeCount ? sel.getRangeAt(0) : null;
        if (range && ed.contains(range.startContainer)) {
            range.deleteContents(); range.insertNode(node);
            var anchor = document.createTextNode('\u200B');
            node.parentNode.insertBefore(anchor, node.nextSibling);
            try { range.setStart(anchor, 1); range.collapse(true); sel.removeAllRanges(); sel.addRange(range); } catch (e) { }
        } else { ed.appendChild(node); ed.appendChild(document.createTextNode('\u200B')); }
        markDirty();
        var rawPut = imgPut(id, raw).catch(function () { });
        var task = compress(raw).then(function (b) { return imgPut(id, b); }).then(function () { return rawPut; }).then(function () { return true; })
            .catch(function () { return false; }).then(function (ok) {
                if (!ok) { node.remove(); alert('图片保存失败'); }
                delete _pending[id]; markDirty();
            });
        _pending[id] = task;
    }
    function applyFmt(cmd, val) {
        var ed = document.getElementById('mbEditor');
        if (!ed) return;
        var sel = window.getSelection();
        var blockCmd = cmd === 'h1' || cmd === 'h2' || cmd === 'plain' || cmd === 'plainBlock';
        var needSel = !blockCmd;
        if (!sel.rangeCount || !ed.contains(sel.anchorNode) || (sel.isCollapsed && needSel)) {
            mbHint('先选中要设置格式的文字'); return;
        }
        ed.focus();
        try { document.execCommand('styleWithCSS', false, !blockCmd); } catch (e) { }
        if (cmd === 'h1' || cmd === 'h2') document.execCommand('formatBlock', false, cmd.toUpperCase());
        else if (cmd === 'plain') { document.execCommand('formatBlock', false, 'P'); document.execCommand('removeFormat'); }
        else if (cmd === 'plainBlock') document.execCommand('formatBlock', false, 'P'); // 只取消标题，保留加粗/斜体/字色/高亮
        else if (cmd === 'clearHl') document.execCommand('hiliteColor', false, 'transparent'); // 只清高亮，字色不动
        else document.execCommand(cmd, false, val || null);
        markDirty();
    }
    // ============ 格式刷：取 O(1) 次，套 O(1) 次，覆盖粗/斜/字色/高亮/H1·H2 ============
    var _brush = null;
    function selCtx() {
        var ed = document.getElementById('mbEditor');
        var sel = window.getSelection();
        if (!ed || !sel || !sel.rangeCount || !ed.contains(sel.anchorNode)) return null;
        return { ed: ed, sel: sel, range: sel.getRangeAt(0) };
    }
    function captureFormat(ctx) {
        var ed = ctx.ed;
        var node = ctx.range.startContainer;
        if (node && node.nodeType === 3) node = node.parentElement;
        var f = { block: 'P', bold: false, italic: false, color: null, bg: null };
        var el = node;
        while (el && el !== ed) {
            var st = el.style || {};
            if (!f.bold && (el.tagName === 'B' || el.tagName === 'STRONG' || /bold/i.test(st.fontWeight || ''))) f.bold = true;
            if (!f.italic && (el.tagName === 'I' || el.tagName === 'EM' || /italic/i.test(st.fontStyle || ''))) f.italic = true;
            if (!f.color) f.color = hexColor(st.color) || (el.getAttribute && hexColor(el.getAttribute('color')));
            if (!f.bg) f.bg = hexColor(st.backgroundColor || st.background) || (el.getAttribute && hexColor(el.getAttribute('bgcolor')));
            if (el.tagName === 'H1' || el.tagName === 'H2') { f.block = el.tagName; break; }
            el = el.parentElement;
        }
        return f;
    }
    function fmtDesc(f) {
        var a = [f.block === 'H1' ? '大标题' : f.block === 'H2' ? '中标题' : '正文'];
        if (f.bold) a.push('加粗');
        if (f.italic) a.push('斜体');
        if (f.color) a.push('字色 ' + f.color);
        if (f.bg) a.push('高亮 ' + f.bg);
        return a.join(' · ');
    }
    function clearBrush() {
        _brush = null;
        var btn = document.getElementById('mbFmtBrush');
        if (btn) btn.classList.remove('on');
    }
    function execFmt(cmd, val, styleWithCSS) {
        if (typeof styleWithCSS === 'boolean') {
            try { document.execCommand('styleWithCSS', false, styleWithCSS); } catch (e) { }
        }
        try { document.execCommand(cmd, false, val || null); } catch (e) { }
    }
    function setToggle(cmd, want) {
        var cur = false;
        try { cur = !!document.queryCommandState(cmd); } catch (e) { }
        if (cur !== want) execFmt(cmd);
    }
    function toggleBrush() {
        if (_brush) { applyBrush(); return; }
        var ctx = selCtx();
        if (!ctx) { mbHint('先把光标放到要取格式的文字上'); return; }
        _brush = captureFormat(ctx);
        var btn = document.getElementById('mbFmtBrush');
        if (btn) btn.classList.add('on');
        mbHint('已取格式：' + fmtDesc(_brush) + '。选中目标文字后再点一次格式刷套用。');
    }
    function applyBrush() {
        var ctx = selCtx();
        if (!ctx || ctx.range.collapsed) { mbHint('先选中要套用格式的文字'); return; }
        var f = _brush;
        ctx.ed.focus();
        execFmt('removeFormat', null, true);                  // 先清掉目标旧的行内格式
        execFmt('formatBlock', f.block, false);               // H1/H2 与 applyFmt 同源：styleWithCSS=false
        // 标题本身自带粗体：bold 是开关命令，必须先查状态，否则会把 H1/H2 的粗体反着关掉
        setToggle('bold', !!f.bold);
        setToggle('italic', !!f.italic);
        if (f.color) execFmt('foreColor', f.color, true);
        if (f.bg) execFmt('hiliteColor', f.bg, true);
        clearBrush();
        markDirty();
        mbHint('已套用：' + fmtDesc(f));
    }
    function insertFormula(kind) {
        var ctx = selCtx();
        if (!ctx) { mbHint('先把光标放到正文里'); return; }
        ctx.ed.focus();
        var frag = document.createTextNode(kind === 'block' ? '\n$$\n\u200B\n$$\n' : '$\u200B$');
        var r = ctx.range.cloneRange();
        r.deleteContents(); r.insertNode(frag);
        var caret = document.createRange();
        caret.setStart(frag, kind === 'block' ? 4 : 1);
        caret.collapse(true);
        ctx.sel.removeAllRanges(); ctx.sel.addRange(caret);
        markDirty();
    }
    function mbHint(msg) {
        var el = document.getElementById('mbHint');
        if (!el) return;
        el.textContent = msg; el.style.display = 'block';
        clearTimeout(el._t); el._t = setTimeout(function () { el.style.display = 'none'; }, 2200);
    }

    // ============ 正文渲染（token → HTML + KaTeX） ============
    function mdInline(s) {
        return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    }
    function mdBlock(s) {
        s = balanceDollars(s);
        var lines = String(s).split('\n'), out = [], buf = null;
        lines.forEach(function (raw) {
            var l = raw.replace(/^[ \t]+/, function (m) { return m.replace(/[ \t]/g, '\u00A0'); })
                .replace(/[ \t]+$/, '').replace(/ {2,}/g, function (m) { return m.replace(/ /g, '\u00A0'); });
            if (!l) { if (buf) buf += '\n'; return; }
            if (buf === null && l.indexOf('$$') === 0 && l.lastIndexOf('$$') === l.length - 2 && l !== '$$') { out.push('<p>' + mdInline(l) + '</p>'); return; }
            if (buf === null && l.indexOf('$$') === 0 && (l.lastIndexOf('$$') !== l.length - 2 || l === '$$')) { buf = l; return; }
            if (buf !== null) {
                buf += '\n' + l;
                if (l.lastIndexOf('$$') === l.length - 2) { out.push('<p>' + mdInline(buf) + '</p>'); buf = null; }
                return;
            }
            if (l.indexOf('<h1>') === 0 || l.indexOf('<h2>') === 0) out.push(mdInline(l));
            else out.push('<p>' + mdInline(l) + '</p>');
        });
        if (buf) out.push('<p>' + mdInline(buf) + '</p>');
        return out.join('')
            .replace(/&lt;h:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/h&gt;/g, '<mark style="background:$1">$2</mark>')
            .replace(/&lt;c:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/c&gt;/g, '<span style="color:$1">$2</span>')
            .replace(/&lt;b&gt;([\s\S]*?)&lt;\/b&gt;/g, '<b>$1</b>')
            .replace(/&lt;i&gt;([\s\S]*?)&lt;\/i&gt;/g, '<i>$1</i>')
            .replace(/&lt;h1&gt;([\s\S]*?)&lt;\/h1&gt;/g, '<h3 class="mb-doc-h1">$1</h3>')
            .replace(/&lt;h2&gt;([\s\S]*?)&lt;\/h2&gt;/g, '<h4 class="mb-doc-h2">$1</h4>')
            .replace(/\[图:([a-z0-9]+)\]/g, function (_, id) { return '<img class="mb-view-img" data-img="' + id + '" alt="易错本图片">'; });
    }
    function renderMath(root) {
        if (!window.katex || !window.renderMathInElement || !root) return;
        try {
            renderMathInElement(root, {
                delimiters: [
                    { left: '$$', right: '$$', display: true },
                    { left: '\\[', right: '\\]', display: true },
                    { left: '\\(', right: '\\)', display: false },
                    { left: '$', right: '$', display: false }
                ], throwOnError: false
            });
        } catch (e) { }
    }
    // ============ 编辑态下方实时预览（和列表卡片同一套 mdBlock + KaTeX + 贴图） ============
    var _previewT = null;
    function renderPreview() {
        var box = document.getElementById('mbPreview');
        var ed = document.getElementById('mbEditor');
        if (!box || !ed) return;
        var body = editorToNote(ed);
        box.innerHTML = body.trim()
            ? mdBlock(body)
            : '<div class="mb-preview-empty">预览：输入内容后实时显示（公式 / 高亮 / 贴图）</div>';
        renderMath(box); fillImgs(box); bindZoom(box);
    }
    function schedulePreview() {
        var v = document.getElementById('mbEditView');
        if (!v || v.hidden) return;
        clearTimeout(_previewT);
        _previewT = setTimeout(renderPreview, 220);
    }
    function plain(body, max) {
        var t = String(body || '')
            .replace(/<c:[^>]+>|<\/c>|<h:[^>]+>|<\/h>|<\/?b>|<\/?i>|<\/?h1>|<\/?h2>/g, '')
            .replace(/\[图:[a-z0-9]+\]/g, '[图]').replace(/\*\*/g, '');
        // 公式必须先抽成占位符再截断：直接删 $ 会让摘要里的公式变纯文本；
        // 直接截字符串又可能切断 $...$ 造成半截定界符 → KaTeX 跨元素乱配对。
        var fml = [];
        t = t.replace(/\$\$[\s\S]*?\$\$|\$[^$\n]*?\$/g, function (m) { fml.push(m); return '\u0001' + (fml.length - 1) + '\u0002'; });
        t = t.replace(/\s+/g, ' ').trim();
        if (t.length > (max || 90)) t = t.slice(0, max || 90) + '…';
        t = t.replace(/\u0001(\d+)\u0002/g, function (m, i) { return fml[+i] || ''; });
        return t.replace(/[\u0001\u0002]/g, '');
    }

    // ============ 视图渲染 ============
    var TAG_FOLD_AT = 5;   // 筛选栏 / 预设栏默认只显示前 5 个，其余折叠
    var state = { tag: '', kw: '', sort: 'updated', tagFold: true };
    var _dirty = false, _editId = null;
    var _editPreset = {}, _editTagFold = true;   // 编辑态：点选的预设标签 + 预设栏折叠态

    function markDirty() { _dirty = true; var h = document.getElementById('mbHint'); if (h) h.textContent = '未保存的改动'; schedulePreview(); }

    function updateEntry() {
        var n = load().length;
        var c = document.getElementById('mbCount'), b = document.getElementById('mbEntry');
        if (c) c.textContent = n;
        if (b) {
            b.title = '记下易错点，支持公式与贴图 · 共 ' + n + ' 条';
            b.classList.toggle('on', isOpen());
        }
    }
    // 筛选栏标签：只列出「有笔记打过」的标签（预设或自定义都算），按预设顺序排列；默认折叠
    function usedTags() {
        var all = load(), counts = {}, order = {};
        all.forEach(function (r) {
            (r.tags || []).forEach(function (t, i) {
                counts[t] = (counts[t] || 0) + 1;
                if (order[t] === undefined || i < order[t]) order[t] = i;
            });
        });
        var tags = Object.keys(counts);
        tags.sort(function (a, b) {
            var ia = PRESET_TAGS.indexOf(a), ib = PRESET_TAGS.indexOf(b);
            if (ia < 0) ia = 999; if (ib < 0) ib = 999;
            return ia - ib || order[a] - order[b];
        });
        return { tags: tags, counts: counts };
    }
    function renderTags() {
        var box = document.getElementById('mbTags');
        if (!box) return;
        var all = load(), u = usedTags(), tags = u.tags, counts = u.counts;
        var over = tags.length > TAG_FOLD_AT;
        var shown = (over && state.tagFold) ? tags.slice(0, TAG_FOLD_AT) : tags;
        var html = '<button class="mb-chip' + (state.tag === '' ? ' on' : '') + '" onclick="Mistake.setTag(\'\')">全部 ' + all.length + '</button>';
        shown.forEach(function (t) {
            html += '<button class="mb-chip' + (state.tag === t ? ' on' : '') + '" onclick="Mistake.setTag(' + JSON.stringify(t).replace(/"/g, '&quot;') + ')">' + esc(t) + ' ' + counts[t] + '</button>';
        });
        if (over) html += '<button class="mb-chip-fold" onclick="Mistake.toggleTagFold()">' + (state.tagFold ? '展开其余 ' + (tags.length - TAG_FOLD_AT) + ' 个 ▾' : '收起 ▴') + '</button>';
        box.innerHTML = html;
    }
    function toggleTagFold() { state.tagFold = !state.tagFold; renderTags(); }

    // 编辑态预设标签 chips：默认折叠，点选写入 _editPreset
    function renderPresetTags() {
        var box = document.getElementById('mbPresetTags');
        if (!box) return;
        var over = PRESET_TAGS.length > TAG_FOLD_AT;
        var shown = (over && _editTagFold) ? PRESET_TAGS.slice(0, TAG_FOLD_AT) : PRESET_TAGS;
        var html = '';
        shown.forEach(function (t) {
            var on = !!_editPreset[t];
            html += '<button type="button" class="mb-chip' + (on ? ' on' : '') + '" onclick="Mistake.togglePresetTag(' + JSON.stringify(t).replace(/"/g, '&quot;') + ')">' + esc(t) + '</button>';
        });
        if (over) html += '<button type="button" class="mb-chip-fold" onclick="Mistake.togglePresetFold()">' + (_editTagFold ? '展开全部 ' + PRESET_TAGS.length + ' 个 ▾' : '收起 ▴') + '</button>';
        box.innerHTML = html;
    }
    function togglePresetTag(t) { _editPreset[t] = !_editPreset[t]; renderPresetTags(); markDirty(); }
    function togglePresetFold() { _editTagFold = !_editTagFold; renderPresetTags(); }
    function visibleList() {
        var a = load();
        if (state.tag) a = a.filter(function (r) { return (r.tags || []).indexOf(state.tag) >= 0; });
        if (state.kw) {
            var k = state.kw.toLowerCase();
            a = a.filter(function (r) {
                return String(r.title || '').toLowerCase().indexOf(k) >= 0 ||
                    String(r.body || '').toLowerCase().indexOf(k) >= 0 ||
                    (r.tags || []).join(' ').toLowerCase().indexOf(k) >= 0;
            });
        }
        a.sort(function (x, y) {
            if (!!y.pinned !== !!x.pinned) return y.pinned ? 1 : -1;
            return state.sort === 'created' ? (y.created || 0) - (x.created || 0) : (y.updated || 0) - (x.updated || 0);
        });
        return a;
    }
    function renderList() {
        var box = document.getElementById('mbList');
        if (!box) return;
        var a = visibleList();
        document.getElementById('mbTotal').textContent = a.length;
        if (!a.length) {
            box.innerHTML = '<div class="mb-empty">' + (load().length ? '没有匹配的笔记，换个标签或关键词。' : '还没有易错笔记。点「+ 新建」记下第一条。') + '</div>';
            return;
        }
        box.innerHTML = a.map(function (r) {
            return '<div class="mb-card' + (r.pinned ? ' pinned' : '') + '">' +
                '<div class="mb-card-h">' +
                    '<div class="mb-card-title" onclick="Mistake.openEditor(\'' + r.id + '\')">' + esc(r.title || '（无标题）') + '</div>' +
                    '<div class="mb-card-ops">' +
                        (r.pinned ? '<button class="mb-op on" title="取消置顶" onclick="Mistake.unpin(\'' + r.id + '\')">置顶</button>' : '<button class="mb-op" title="置顶" onclick="Mistake.pin(\'' + r.id + '\')">置顶</button>') +
                        '<button class="mb-op" title="编辑" onclick="Mistake.openEditor(\'' + r.id + '\')">编辑</button>' +
                        '<button class="mb-op del" title="删除" onclick="Mistake.del(\'' + r.id + '\')">删</button>' +
                    '</div>' +
                '</div>' +
                '<div class="mb-card-tags">' + (r.tags || []).map(function (t) { return '<span class="mb-tag">' + esc(t) + '</span>'; }).join('') + '</div>' +
                '<div class="mb-card-body" data-id="' + r.id + '">' + mdBlock(r.body) + '</div>' +
                '<div class="mb-card-foot">更新于 ' + fmtTime(r.updated || r.created || Date.now()) + '</div>' +
            '</div>';
        }).join('');
        box.querySelectorAll('.mb-card-body').forEach(function (el) {
            renderMath(el);
            fillImgs(el);
            bindZoom(el);
        });
    }
    function renderAll() { updateEntry(); renderTags(); renderList(); }

    // ============ 编辑态 ============
    function openEditor(id) {
        _editId = id || null;
        var rec = id ? find(id) : null;
        var view = document.getElementById('mbListView');
        var edView = document.getElementById('mbEditView');
        view.hidden = true; edView.hidden = false;
        document.getElementById('mbEditTitle').textContent = rec ? '编辑易错笔记' : '新建易错笔记';
        document.getElementById('mbTitle').value = rec ? (rec.title || '') : '';
        // 标签拆分：预设章节 → chips 点选；自定义 → 输入框
        _editPreset = {}; _editTagFold = true;
        var tags = rec ? (rec.tags || []) : (state.tag ? [state.tag] : []);
        var custom = [];
        tags.forEach(function (t) {
            var pi = PRESET_TAGS.indexOf(t);
            if (pi >= 0) { _editPreset[t] = true; if (pi >= TAG_FOLD_AT) _editTagFold = false; }
            else custom.push(t);
        });
        document.getElementById('mbTagsInput').value = custom.join('、');
        renderPresetTags();
        var ed = document.getElementById('mbEditor');
        noteToEditor(ed, rec ? (rec.body || '') : '');
        fillImgs(ed);
        renderPreview();
        _dirty = false;
        clearBrush();
        document.getElementById('mbHint').textContent = '';
        document.getElementById('mbTitle').focus();
    }
    function closeEditor() {
        if (_dirty && !confirm('有未保存的改动，确定放弃吗？')) return;
        clearBrush();
        _editId = null; _dirty = false;
        document.getElementById('mbEditView').hidden = true;
        document.getElementById('mbListView').hidden = false;
        renderAll();
    }
    async function saveEditor() {
        await waitPendingImgs();
        var title = document.getElementById('mbTitle').value.trim();
        var body = editorToNote(document.getElementById('mbEditor'));
        if (!title && !body.trim()) { mbHint('标题和正文至少填一个'); return; }
        var tags = document.getElementById('mbTagsInput').value.split(/[、,，;；]/)
            .map(function (s) { return s.trim(); }).filter(Boolean);
        // 合并预设 chips 点选（保持预设顺序）+ 自定义输入
        PRESET_TAGS.forEach(function (t) { if (_editPreset[t] && tags.indexOf(t) < 0) tags.push(t); });
        tags.sort(function (a, b) {
            var ia = PRESET_TAGS.indexOf(a), ib = PRESET_TAGS.indexOf(b);
            if (ia < 0) ia = 999; if (ib < 0) ib = 999;
            return ia - ib;
        });
        var now = Date.now(), old = _editId ? find(_editId) : null;
        var rec = {
            id: old ? old.id : uid(),
            title: title || '（无标题）',
            tags: tags,
            body: body,
            created: old ? old.created : now,
            updated: now,
            pinned: old ? !!old.pinned : false
        };
        var oldRefs = old ? refsOf(old.body) : [];
        if (!upsert(rec)) return;
        var newRefs = refsOf(body);
        imgDel(oldRefs.filter(function (id) { return newRefs.indexOf(id) < 0; }));
        clearBrush();
        _dirty = false; _editId = null;
        document.getElementById('mbEditView').hidden = true;
        document.getElementById('mbListView').hidden = false;
        renderAll();
    }
    function del(id) {
        var r = find(id); if (!r) return;
        if (!confirm('确定删除「' + (r.title || '无标题') + '」？此操作不可撤销。')) return;
        var a = load().filter(function (x) { return x.id !== id; });
        save(a); imgDel(refsOf(r.body)); renderAll();
    }
    function pin(id) { var r = find(id); if (r) { r.pinned = true; r.updated = Date.now(); upsert(r); renderAll(); } }
    function unpin(id) { var r = find(id); if (r) { r.pinned = false; upsert(r); renderAll(); } }

    // ============ 视图切换 ============
    function isOpen() { return document.body.classList.contains('mb-open'); }
    function open() {
        document.body.classList.add('mb-open');
        try { localStorage.setItem(VIEW_KEY, '1'); } catch (e) { }
        updateEntry();
        renderAll();
        window.scrollTo(0, 0);
    }
    function close() {
        document.body.classList.remove('mb-open');
        try { localStorage.setItem(VIEW_KEY, '0'); } catch (e) { }
        updateEntry();
    }
    function toggle() { isOpen() ? close() : open(); }
    function setTag(t) { state.tag = (state.tag === t ? '' : t); renderTags(); renderList(); }
    function setKw(k) { state.kw = String(k || '').trim(); renderList(); }
    function setSort(v) { state.sort = v; renderList(); }

    // ============ 启动 ============
    function init() {
        if (!document.getElementById('mbView')) return;
        document.getElementById('mbEditor').addEventListener('paste', pasteImg);
        document.getElementById('mbEditor').addEventListener('input', markDirty);
        ['mbTitle', 'mbTagsInput'].forEach(function (id) {
            document.getElementById(id).addEventListener('input', markDirty);
        });
        var kw = document.getElementById('mbKw');
        if (kw) kw.addEventListener('input', function () { setKw(kw.value); });
        var sort = document.getElementById('mbSort');
        if (sort) sort.addEventListener('change', function () { setSort(sort.value); });
        renderPresetTags();
        // 在易错本视图里点左栏目录/搜索结果跳笔记 → 自动退回笔记视图。
        // ⚠️ 不能用 hashchange：reader.js 首次异步加载完会写一次 hash，刷新后会误判为「用户跳笔记」而退出易错本。
        document.addEventListener('click', function (e) {
            if (!isOpen()) return;
            if (e.target.closest && e.target.closest('#navTree a, #searchResults a')) close();
        }, true);
        renderAll();
        if (localStorage.getItem(VIEW_KEY) === '1') open();
    }

    window.Mistake = {
        init: init, toggle: toggle, open: open, close: close,
        openEditor: openEditor, closeEditor: closeEditor, saveEditor: saveEditor,
        del: del, pin: pin, unpin: unpin, setTag: setTag, setKw: setKw, setSort: setSort,
        applyFmt: applyFmt, toggleBrush: toggleBrush, insertFormula: insertFormula, PRESET_TAGS: PRESET_TAGS,
        toggleTagFold: toggleTagFold, togglePresetTag: togglePresetTag, togglePresetFold: togglePresetFold
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
