/* 考研数学笔记 - 批注系统：荧光高亮（选中文字/整块）+ 文字批注，存 localStorage
 * 锚定方式：每个块（li/p）按「笔记id#文档顺序」生成位置稳定的 sid；改文字不影响标注，仅结构变动才失效（并有提示） */

const Annot = (() => {
    const LS = 'notesAnnot';
    let data = {};          // { noteId: { hl:{key:color}, notes:{key:text}, marks:[{k,t,c,n}] } }
    let curId = null;
    let bar = null;         // 浮动工具条
    let barTarget = null;   // 当前操作对象 {block} / {gid}

    try { data = JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) { data = {}; }

    /** 配额/写入失败的醒目提示（非阻塞） */
    function quotaWarn() {
        let bar = document.getElementById('annQuotaBar');
        if (!bar) {
            bar = document.createElement('div');
            bar.id = 'annQuotaBar';
            bar.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;background:#c0392b;color:#fff;padding:10px 14px;font-size:13px;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.25)';
            document.body.appendChild(bar);
        }
        bar.innerHTML = '⚠️ 标注存储空间已满，新标注可能未保存！请尽快「导出标注」备份，或清理部分荧光/贴图后重试。 <button style="margin-left:10px;background:#fff;color:#c0392b;border:0;border-radius:4px;padding:2px 8px;cursor:pointer" onclick="this.parentNode.remove()">知道了</button>';
        bar.style.display = 'block';
    }

    /** 一般性提示横幅（用于迁移/孤儿告知）；opts.recover 时附「恢复标注」按钮 */
    function annNotify(msg, opts) {
        let bar = document.getElementById('annNotifyBar');
        if (!bar) {
            bar = document.createElement('div');
            bar.id = 'annNotifyBar';
            bar.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;background:#2d6cdf;color:#fff;padding:10px 14px;font-size:13px;line-height:1.5;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.25)';
            document.body.appendChild(bar);
        }
        let html = msg;
        if (opts && opts.recover)
            html += ' <button style="margin-left:8px;background:#fff;color:#2d6cdf;border:0;border-radius:4px;padding:2px 8px;cursor:pointer" onclick="Annot.openRecover()">恢复标注</button>';
        html += ' <button style="margin-left:10px;background:rgba(255,255,255,.2);color:#fff;border:0;border-radius:4px;padding:2px 8px;cursor:pointer" onclick="this.parentNode.remove()">知道了</button>';
        bar.innerHTML = html;
        bar.style.display = 'block';
    }

    const save = () => {
        try {
            localStorage.setItem(LS, JSON.stringify(data));
        } catch (e) {
            console.error('标注保存失败（可能超出存储配额）:', e);
            quotaWarn();
        }
    };
    const bucket = () => data[curId] || (data[curId] = { hl: {}, notes: {}, marks: [] });
    const escA = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const escAttr = s => escA(s).replace(/"/g, '&quot;');
    /** 公式标注桶：懒创建，避免无标注时污染存储 */
    const ensureFml = () => { const d = data[curId] || (data[curId] = { hl: {}, notes: {}, marks: [] }); return d.fml || (d.fml = {}); };
    const topKatex = node => { let k = node.closest && node.closest('.katex'); while (k && k.parentElement && k.parentElement.closest('.katex')) k = k.parentElement.closest('.katex'); return k; };
    const texOf = el => (el.getAttribute('aria-label') || el.textContent || '').trim();

    // ============ 批注贴图：图片存 IndexedDB（localStorage 放不下），正文里用 [图:id] 占位 ============
    let idb = null;
    function db() {
        if (!idb) idb = new Promise((res, rej) => {
            const rq = indexedDB.open('notesAnnotImg', 1);
            rq.onupgradeneeded = () => rq.result.createObjectStore('imgs');
            rq.onsuccess = () => res(rq.result);
            rq.onerror = () => rej(rq.error);
        });
        return idb;
    }
    const imgPut = (id, blob) => db().then(d => new Promise((res, rej) => {
        const tx = d.transaction('imgs', 'readwrite');
        tx.objectStore('imgs').put(blob, id);
        tx.oncomplete = res; tx.onerror = () => rej(tx.error);
    }));
    const imgGet = id => db().then(d => new Promise(res => {
        const rq = d.transaction('imgs').objectStore('imgs').get(id);
        rq.onsuccess = () => res(rq.result || null); rq.onerror = () => res(null);
    }));
    const imgDel = ids => !ids.length ? Promise.resolve() : db().then(d => new Promise(res => {
        const tx = d.transaction('imgs', 'readwrite');
        ids.forEach(id => tx.objectStore('imgs').delete(id));
        tx.oncomplete = res; tx.onerror = res;
    }));
    const refsOf = t => [...(t || '').matchAll(/\[图:([a-z0-9]+)\]/g)].map(m => m[1]);
    const blobToDataURL = blob => new Promise(res => {
        const rd = new FileReader();
        rd.onload = () => res(rd.result);
        rd.readAsDataURL(blob);
    });

    function hash(s) {
        let h = 5381;
        for (let i = 0; i < s.length; i++) h = (h * 33 + s.charCodeAt(i)) >>> 0;
        return h.toString(36);
    }
    const gidOf = m => m.k + '|' + m.n + '|' + hash(m.t);

    /** 块自身文本（排除子列表/批注框），用于生成稳定 key */
    function ownText(el) {
        const c = el.cloneNode(true);
        c.querySelectorAll('ul, .ann-box').forEach(n => n.remove());
        return c.textContent.replace(/\s+/g, ' ').trim();
    }

    /** 给每个可标注块（li/p）分配「笔记id#文档顺序」的稳定 sid，替代旧版文本哈希锚点 */
    function keyBlocks(article) {
        [...article.querySelectorAll('li, p')].forEach((el, i) => {
            el.dataset.sid = curId + '#' + i;
        });
    }

    /** 块内可标注的文本节点（排除公式内部/子列表/批注框） */
    function textNodes(el) {
        const out = [];
        (function walk(n) {
            for (const c of n.childNodes) {
                if (c.nodeType === 3) out.push(c);
                else if (c.nodeType === 1 && !c.matches('ul, .katex, .ann-box')) walk(c);
            }
        })(el);
        return out;
    }

    /** 在块内第 occ 次出现的 text 上包 <mark>（可跨 strong 等行内元素，逐文本节点分段包） */
    function wrapText(block, text, color, occ, gid) {
        const nodes = textNodes(block);
        let all = '';
        const map = [];
        for (const nd of nodes) { map.push({ nd, start: all.length }); all += nd.nodeValue; }
        let idx = -1;
        for (let i = 0; i <= occ; i++) {
            idx = all.indexOf(text, idx + 1);
            if (idx < 0) return false;
        }
        const end = idx + text.length;
        for (const m of map) {
            const nStart = m.start, nEnd = m.start + m.nd.nodeValue.length;
            const s = Math.max(idx, nStart), e = Math.min(end, nEnd);
            if (s >= e) continue;
            const r = document.createRange();
            r.setStart(m.nd, s - nStart);
            r.setEnd(m.nd, e - nStart);
            const mk = document.createElement('mark');
            mk.className = 'mk mk-' + color;
            mk.dataset.g = gid;
            r.surroundContents(mk);  // 单个文本节点内，安全
        }
        return true;
    }

    // ============ 荧光：选中文字 ============
    function markSelection(color) {
        const sel = getSelection();
        if (!sel.rangeCount || sel.isCollapsed) return false;
        const r = sel.getRangeAt(0);
        const sc = r.startContainer;
        const block = (sc.nodeType === 3 ? sc.parentElement : sc).closest('[data-sid]');
        if (!block) return false;
        const nodes = textNodes(block);
        let all = '';
        const pos = new Map();
        for (const nd of nodes) { pos.set(nd, all.length); all += nd.nodeValue; }
        const t = r.toString();
        if (!t || !pos.has(sc)) return false;
        const gStart = pos.get(sc) + r.startOffset;
        if (all.substr(gStart, t.length) !== t) return false;  // 选区含公式等，降级为整块
        let occ = 0;
        for (let i = all.indexOf(t); i >= 0 && i < gStart; i = all.indexOf(t, i + 1)) occ++;
        const rec = { k: block.dataset.sid, t, c: color, n: occ };
        const g = gidOf(rec);
        const dup = bucket().marks.filter(m => gidOf(m) === g);
        if (dup.length) {
            // 同一块同一段文字已有荧光：改为换色（清掉旧组再包新色），避免嵌套重复标记
            removeMarkGroup(g);
        }
        if (!wrapText(block, t, color, occ, g)) return false;
        bucket().marks.push(rec);
        save();
        sel.removeAllRanges();
        return true;
    }

    function removeMarkGroup(gid) {
        document.querySelectorAll('mark.mk').forEach(mk => {
            if (mk.dataset.g !== gid) return;
            const parent = mk.parentNode;
            while (mk.firstChild) parent.insertBefore(mk.firstChild, mk);
            parent.removeChild(mk);
        });
        const b = bucket();
        b.marks = b.marks.filter(m => gidOf(m) !== gid);
        save();
    }

    function recolorMarkGroup(gid, color) {
        document.querySelectorAll('mark.mk').forEach(mk => {
            if (mk.dataset.g === gid) mk.className = 'mk mk-' + color;
        });
        for (const m of bucket().marks) if (gidOf(m) === gid) m.c = color;
        save();
    }

    // ============ 荧光：整块 ============
    function setBlockHl(block, color) {
        block.classList.remove('hl-y', 'hl-g', 'hl-b');
        if (color) {
            block.classList.add('hl-' + color);
            bucket().hl[block.dataset.sid] = color;
        } else {
            delete bucket().hl[block.dataset.sid];
        }
        save();
    }

    // ============ 文字批注 ============
    /** 批注文本渲染：转义 → [图:id] 转图片 → 公式定界符渲染成公式
     *  支持四类定界符：行内 $...$ / \(...\)，独行 $$...$$ / \[...\] */
    function texToHtml(tex, display) {
        if (!window.katex) return null;
        try {
            return katex.renderToString(tex.trim(), { displayMode: !!display, throwOnError: false, errorColor: '#d9534f' });
        } catch (e) { return null; }
    }
    function renderAnnot(t) {
        let h = escA(t).replace(/\[图:([a-z0-9]+)\]/g,
            '<img class="ann-img" data-img="$1" alt="批注图片">');
        if (window.katex) {
            // 显示模式（独行居中）：$$...$$ 与 \[...\]
            h = h.replace(/\$\$([\s\S]+?)\$\$/g, (m, tex) =>
                '<span class="ann-fml ann-fml-d">' + (texToHtml(tex, true) || m) + '</span>');
            h = h.replace(/\\\[([\s\S]+?)\\\]/g, (m, tex) =>
                '<span class="ann-fml ann-fml-d">' + (texToHtml(tex, true) || m) + '</span>');
            // 行内模式：$...$ 与 \(...\)
            h = h.replace(/\$([^\$\n]+?)\$/g, (m, tex) => texToHtml(tex, false) || m);
            h = h.replace(/\\\(([\s\S]+?)\\\)/g, (m, tex) => texToHtml(tex, false) || m);
        }
        // 富文本令牌还原（与真题页 exam.js mdBlock 同源）：字色 <c:>、高亮底 <h:>、粗 <b>、斜 <i>、标题 <h1>/<h2>
        h = h
            .replace(/&lt;h:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/h&gt;/g, '<mark class="note-hl" style="background:$1">$2</mark>')
            .replace(/&lt;c:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/c&gt;/g, '<span style="color:$1">$2</span>')
            .replace(/&lt;b&gt;([\s\S]*?)&lt;\/b&gt;/g, '<b>$1</b>')
            .replace(/&lt;i&gt;([\s\S]*?)&lt;\/i&gt;/g, '<i>$1</i>')
            .replace(/&lt;h1&gt;([\s\S]*?)&lt;\/h1&gt;/g, '<h1>$1</h1>')
            .replace(/&lt;h2&gt;([\s\S]*?)&lt;\/h2&gt;/g, '<h2>$1</h2>');
        return h;
    }
    const noteHtml = t => renderAnnot(t);

    function fillImgs(box) {
        box.querySelectorAll('img.ann-img[data-img]').forEach(img => {
            imgGet(img.dataset.img).then(blob => {
                if (blob) img.src = URL.createObjectURL(blob);
                else img.replaceWith('[图片已丢失]');
            });
        });
    }
    /** 编辑态实时预览：编辑器在上、预览在下，随输入防抖刷新（与真题页 noteInput 同源思路） */
    function annPreviewOnInput(ed) {
        const box = ed.closest('.ann-box');
        const pv = box && box.querySelector('.ann-preview');
        if (!pv) return;
        clearTimeout(ed._prevT);
        ed._prevT = setTimeout(() => {
            const v = annEditorToNote(ed);
            pv.innerHTML = noteHtml(v);
            fillImgs(pv);
        }, 350);
    }

    /** 编辑框内 Ctrl+V 贴图：存库后不进编辑器 DOM，缩略图卡片出现在编辑框下方 */
    function onPasteImg(e) {
        const it = [...(e.clipboardData?.items || [])].find(i => i.type.startsWith('image/'));
        if (!it) return;
        e.preventDefault();
        const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
        imgPut(id, it.getAsFile()).then(() => {
            const ed = e.target;
            if (!ed.isContentEditable) {   // 降级：理论上不再有 textarea
                const tag = `[图:${id}]`;
                const p = ed.selectionStart;
                ed.value = ed.value.slice(0, p) + tag + ed.value.slice(ed.selectionEnd);
                ed.selectionStart = ed.selectionEnd = p + tag.length;
                return;
            }
            const strip = ed.closest('.ann-box') && ed.closest('.ann-box').querySelector('.ann-imgs');
            if (strip) {
                strip.appendChild(annThumbCard(id));
                strip.hidden = false;
                fillImgs(strip);   // 立即回填缩略图 blob
            }
            annPreviewOnInput(ed);   // 刷新下方实时预览
        }).catch(() => alert('图片保存失败'));
    }

    function renderNoteBox(block, text, editing) {
        const old = block.querySelector(':scope > .ann-box');
        if (old) old.remove();
        const box = document.createElement('div');
        box.className = 'ann-box';
        if (editing) {
            box.innerHTML = annToolbarHtml() +
                `<div class="ann-edit" contenteditable="true" spellcheck="false" data-placeholder="写点批注…（Ctrl+V 可贴图；选中文字可上色/高亮；用 $...$ 写公式会自动渲染）"></div>
                <div class="ann-imgs" hidden></div>
                <div class="ann-preview"></div>
                <div class="ann-ops"><button onclick="Annot.saveNote(this)">保存</button>
                <button onclick="Annot.cancelNote(this)">取消</button></div>`;
            const ed = box.querySelector('.ann-edit');
            if (text) annNoteToEditor(ed, text);
            ed.addEventListener('paste', onPasteImg);
            ed.addEventListener('input', () => annPreviewOnInput(ed));
            if (text) annPreviewOnInput(ed);   // 进入编辑即有内容时立即渲染预览
            box.querySelector('.ann-toolbar').hidden = false;
        } else {
            box.innerHTML = `<span class="ann-icon">📝</span><span class="ann-text" data-raw="${escAttr(text)}">${noteHtml(text)}</span>
                <span class="ann-ops"><button onclick="Annot.editNote(this)">改</button>
                <button onclick="Annot.delNote(this)">删</button></span>`;
            fillImgs(box);
        }
        const childUl = block.querySelector(':scope > ul');
        block.insertBefore(box, childUl);  // 批注紧跟条目本身文字，在子列表之前
        if (editing) box.querySelector('.ann-edit').focus();
    }

    function saveNote(btn) {
        const block = btn.closest('[data-sid]');
        const box = btn.closest('.ann-box');
        const ed = box.querySelector('.ann-edit');
        const text = ed ? annEditorToNote(ed).trim() : '';
        const prev = bucket().notes[block.dataset.sid] || '';
        const kept = refsOf(text);
        imgDel(refsOf(prev).filter(id => !kept.includes(id)));  // 删掉不再引用的图
        if (text) bucket().notes[block.dataset.sid] = text;
        else delete bucket().notes[block.dataset.sid];
        save();
        if (text) renderNoteBox(block, text, false);
        else block.querySelector(':scope > .ann-box').remove();
    }

    function cancelNote(btn) {
        const block = btn.closest('[data-sid]');
        const saved = bucket().notes[block.dataset.sid];
        // 丢弃编辑中新贴但未保存的图
        const kept = refsOf(saved || '');
        const box = btn.closest('.ann-box');
        const ed = box.querySelector('.ann-edit');
        const draft = ed ? annEditorToNote(ed) : '';
        imgDel(refsOf(draft).filter(id => !kept.includes(id)));
        if (saved) renderNoteBox(block, saved, false);
        else block.querySelector(':scope > .ann-box').remove();
    }

    function editNote(btn) {
        const block = btn.closest('[data-sid]');
        renderNoteBox(block, bucket().notes[block.dataset.sid] || '', true);
    }

    function delNote(btn) {
        if (!confirm('确定删除这条批注？')) return;   // 删除需确认，修改不用
        const block = btn.closest('[data-sid]');
        imgDel(refsOf(bucket().notes[block.dataset.sid]));  // 随批注删掉其引用的图
        delete bucket().notes[block.dataset.sid];
        save();
        block.querySelector(':scope > .ann-box').remove();
    }

    // ============ 恢复：正文渲染后调用 ============
    /** 旧版文本哈希锚点 → 位置 sid 的一次性重锚；无法重锚的标注不再静默丢弃，
     *  而是收入 b.orphans 供「恢复标注」手动/智能认领 */
    function migrateKeys(b, blocks) {
        const byHash = {};
        blocks.forEach(el => {
            const h = hash(ownText(el));
            (byHash[h] || (byHash[h] = [])).push({ sid: el.dataset.sid, text: ownText(el) });
        });
        const remap = (oldKey) => {
            const m = /^(.*)#(\d+)$/.exec(oldKey);
            const h = m ? m[1] : oldKey;
            const occ = m ? parseInt(m[2], 10) : 1;
            const list = byHash[h];
            return (list && list[occ - 1]) ? list[occ - 1] : null;
        };
        const orphans = { hl: {}, notes: {}, marks: [] };
        const newHl = {};
        for (const [k, c] of Object.entries(b.hl || {})) {
            const hit = remap(k); if (hit) newHl[hit.sid] = c; else orphans.hl[k] = c;
        }
        b.hl = newHl;
        const newNotes = {};
        for (const [k, t] of Object.entries(b.notes || {})) {
            const hit = remap(k); if (hit) newNotes[hit.sid] = t; else orphans.notes[k] = t;
        }
        b.notes = newNotes;
        const newMarks = [];
        for (const m of (b.marks || [])) {
            const hit = remap(m.k);
            if (hit) newMarks.push({ ...m, k: hit.sid });
            else orphans.marks.push(m);
        }
        b.marks = newMarks;
        return orphans;
    }

    let _notified = false;
    /** 收集正文里「嵌入批注」行（源 md 中「📝 批注：…」已固化为正文内容）的文本集合。
     *  这些批注既在正文可见，又在 localStorage 留有旧锚点的重复副本；后者旧索引已失效，
     *  不应计入「无法定位」提示，也不应重复渲染。 */
    function embeddedNoteTexts(article) {
        const set = new Set();
        article.querySelectorAll('.note-article li, .note-article p').forEach(el => {
            const t = el.textContent.replace(/\s+/g, ' ').trim();
            if (t.startsWith('📝 批注：')) set.add(t.slice('📝 批注：'.length).trim());
        });
        return set;
    }
    function apply(noteId) {
        curId = noteId;
        const article = document.querySelector('.note-article');
        if (!article) return;
        keyBlocks(article);
        const b = data[noteId];
        if (!b) return;
        if (!b.__sid) {
            const orphans = migrateKeys(b, [...article.querySelectorAll('li, p')]);
            b.__sid = true;
            b.orphans = orphans;
            save();
            const oc = Object.keys(orphans.hl).length + Object.keys(orphans.notes).length + orphans.marks.length;
            if (oc > 0)
                annNotify(`已迁移旧版标注；其中 ${oc} 条因内容变动无法定位，可点「恢复标注」找回。`, { recover: true });
        }
        const byKey = {};
        article.querySelectorAll('[data-sid]').forEach(el => { byKey[el.dataset.sid] = el; });
        // 嵌入批注（源 md 中「📝 批注：…」）已是正文内容，其对应的旧 localStorage 批注属重复：
        // 不渲染、不计入「无法定位」，并就地自愈清理（storage 去重）
        const embTexts = embeddedNoteTexts(article);
        const norm = t => (t || '').replace(/\s+/g, ' ').trim();
        let orphans = 0, dirty = false;
        // marks 按 gid 去重（历史重复划荧光会产生同 gid 多条记录）
        if (b.marks && b.marks.length) {
            const seenG = new Set(); const kept = [];
            for (const m of b.marks) {
                const g = gidOf(m);
                if (!seenG.has(g)) { seenG.add(g); kept.push(m); }
            }
            if (kept.length !== b.marks.length) { b.marks = kept; dirty = true; }
        }
        for (const [k, c] of Object.entries(b.hl || {})) {
            if (byKey[k]) byKey[k].classList.add('hl-' + c); else orphans++;
        }
        for (const m of b.marks || []) {
            if (byKey[m.k]) wrapText(byKey[m.k], m.t, m.c, m.n, gidOf(m));
            else if (!embTexts.has(norm(m.t))) orphans++;
        }
        for (const [k, t] of Object.entries(b.notes || {})) {
            if (embTexts.has(norm(t))) { delete b.notes[k]; dirty = true; continue; }  // 与嵌入批注重复 → 清除
            if (byKey[k]) renderNoteBox(byKey[k], t, false);
            else orphans++;
        }
        if (dirty) save();
        if (orphans > 0 && !_notified) {
            _notified = true;
            annNotify(`有 ${orphans} 条标注因笔记结构变动（增/删/移动条目）已无法定位，可「恢复标注」找回。`, { recover: true });
        }
        applyFml();
    }

    // ============ 公式标注：识别 .katex 并恢复（方案 C 混合层） ============
    function applyFml() {
        const article = document.querySelector('.note-article');
        if (!article || !curId) return;
        const b = data[curId]; if (!b || !b.fml) return;
        article.querySelectorAll('.fml-note-mark, .fml-label').forEach(n => n.remove());
        const fml = b.fml, occMap = {};
        [...article.querySelectorAll('.katex')].filter(k => !k.parentElement.closest('.katex')).forEach(el => {
            const tex = texOf(el); if (!tex) return;
            const hk = hash(tex), occ = occMap[hk] || 0; occMap[hk] = occ + 1;
            const key = hk + '#' + occ;
            el.dataset.fid = key;
            const rec = fml[key]; if (!rec) return;
            if (rec.hl) el.classList.add('fml-hl-' + rec.hl);
            if (rec.note) { const s = document.createElement('sup'); s.className = 'fml-note-mark'; s.dataset.fid = key; s.title = '查看/编辑批注'; s.textContent = '📝'; el.after(s); }
            if (rec.label) { const s = document.createElement('span'); s.className = 'fml-label'; s.textContent = rec.label; el.after(s); }
        });
    }

    // ============ 孤儿标注恢复（内容变动后丢失锚点，可手动/智能认领，或从导出备份补充） ============
    let recoverListCache = [];

    const kindName = k => k === 'hl' ? '荧光' : k === 'note' ? '批注' : '选段';
    const colorName = c => c === 'y' ? '黄' : c === 'g' ? '绿' : c === 'b' ? '蓝' : c;

    /** 最长公共子串长度（用于智能匹配；大文本截断抽样避免卡顿） */
    function lcsLen(a, b) {
        if (!a || !b) return 0;
        if (a.length * b.length > 40000) { a = a.slice(0, 400); b = b.slice(0, 400); }
        const m = a.length, n = b.length;
        const dp = Array.from({ length: m + 1 }, () => new Uint16Array(n + 1));
        let best = 0;
        for (let i = 1; i <= m; i++)
            for (let j = 1; j <= n; j++)
                if (a[i - 1] === b[j - 1]) { dp[i][j] = dp[i - 1][j - 1] + 1; if (dp[i][j] > best) best = dp[i][j]; }
        return best;
    }

    /** 收集当前笔记里「键不在当前 DOM」的标注 = 待恢复孤儿（含迁移残留 b.orphans）。
     *  文本已嵌入正文的批注（📝 批注：…）不算丢失，过滤掉以防认领后重复 */
    function buildRecoverList() {
        const article = document.querySelector('.note-article');
        if (!article) return [];
        const byKey = {};
        article.querySelectorAll('[data-sid]').forEach(el => byKey[el.dataset.sid] = el);
        const b = data[curId]; if (!b) return [];
        const norm = t => (t || '').replace(/\s+/g, ' ').trim();
        const emb = embeddedNoteTexts(article);
        const isEmb = t => emb.has(norm(t));
        const list = [];
        for (const [k, c] of Object.entries(b.hl || {})) if (!byKey[k]) list.push({ kind: 'hl', key: k, color: c, text: '(整块荧光·' + colorName(c) + ')' });
        for (const [k, t] of Object.entries(b.notes || {})) if (!byKey[k] && !isEmb(t)) list.push({ kind: 'note', key: k, text: t });
        for (const m of (b.marks || [])) if (!byKey[m.k] && !isEmb(m.t)) list.push({ kind: 'mark', key: m.k, text: m.t, color: m.c, n: m.n });
        const o = b.orphans;
        if (o) {
            for (const [k, c] of Object.entries(o.hl || {})) list.push({ kind: 'hl', key: k, color: c, text: '(整块荧光·' + colorName(c) + ')' });
            for (const [k, t] of Object.entries(o.notes || {})) if (!isEmb(t)) list.push({ kind: 'note', key: k, text: t });
            for (const m of (o.marks || [])) if (!isEmb(m.t)) list.push({ kind: 'mark', key: m.k, text: m.t, color: m.c, n: m.n });
        }
        return list;
    }

    function injectRecoverModal() {
        if (document.getElementById('annRecover')) return;
        const el = document.createElement('div');
        el.id = 'annRecover'; el.className = 'ann-modal'; el.hidden = true;
        el.innerHTML = `<div class="ann-modal-box">
            <div class="ann-modal-head">恢复丢失的标注 <button class="ann-modal-x" onclick="Annot.closeRecover()">✕</button></div>
            <div class="ann-modal-body">
                <p class="ann-rec-intro">下面是当前笔记里<strong>找不到位置</strong>的标注（内容曾改动过）。给每条选一个目标条目，或点「智能匹配」按文字相似度自动认领；也可从导出备份里补充。</p>
                <div id="annRecList"></div>
                <div class="ann-rec-foot">
                    <button class="ann-rec-smart" onclick="Annot.smartRecover()">智能匹配</button>
                    <label class="ann-rec-file">从导出备份补充<input type="file" accept="application/json" onchange="Annot.loadBackup(this)"></label>
                    <button class="ann-rec-done" onclick="Annot.closeRecover()">完成</button>
                </div>
            </div></div>`;
        document.body.appendChild(el);
    }

    function openRecover() {
        injectRecoverModal();
        const modal = document.getElementById('annRecover');
        modal.hidden = false;
        renderRecoverList();
    }
    function closeRecover() { const m = document.getElementById('annRecover'); if (m) m.hidden = true; }

    function renderRecoverList() {
        const listEl = document.getElementById('annRecList');
        if (!listEl) return;
        const list = buildRecoverList();
        recoverListCache = list;
        if (!list.length) { listEl.innerHTML = '<p class="ann-rec-empty">当前笔记没有待恢复的标注 ✅</p>'; return; }
        const blocks = [...document.querySelectorAll('.note-article [data-sid]')];
        const opts = blocks.map((el, i) => `<option value="${el.dataset.sid}">${escA((ownText(el).slice(0, 38)) || ('第' + (i + 1) + '块'))}</option>`).join('');
        listEl.innerHTML = list.map((it, idx) => `
            <div class="ann-rec-row" data-idx="${idx}">
                <div class="ann-rec-prev"><span class="ann-rec-kind k-${it.kind}">${kindName(it.kind)}</span> ${escA(it.text.slice(0, 90))}</div>
                <div class="ann-rec-act">
                    <select class="ann-rec-sel">${opts}</select>
                    <button class="ann-rec-claim" onclick="Annot.claimRecover(${idx})">认领</button>
                </div>
            </div>`).join('');
    }

    /** 从原存储位置（b.hl/notes/marks 或 b.orphans）彻底移除某条标注 */
    function removeEverywhere(key, text, color, n) {
        const b = data[curId]; if (!b) return;
        delete b.hl[key]; delete b.notes[key];
        if (b.marks) b.marks = b.marks.filter(m => !(m.k === key && m.t === text && m.c === color && m.n === n));
        const o = b.orphans;
        if (o) {
            delete o.hl[key]; delete o.notes[key];
            if (o.marks) o.marks = o.marks.filter(m => !(m.k === key && m.t === text && m.c === color && m.n === n));
        }
    }

    function claimWith(it, target) {
        const block = document.querySelector('[data-sid="' + target.replace(/"/g, '\\"') + '"]');
        if (!block) return false;
        const b = data[curId];
        removeEverywhere(it.key, it.text, it.color, it.n);
        if (it.kind === 'hl') {
            b.hl[target] = it.color;
            block.classList.remove('hl-y', 'hl-g', 'hl-b'); block.classList.add('hl-' + it.color);
        } else if (it.kind === 'note') {
            b.notes[target] = it.text;
            renderNoteBox(block, it.text, false);
        } else if (it.kind === 'mark') {
            const rec = { k: target, t: it.text, c: it.color, n: it.n };
            if (!wrapText(block, it.text, it.color, it.n, gidOf(rec))) {  // 文本已变找不到，降级整块荧光
                b.hl[target] = it.color;
                block.classList.remove('hl-y', 'hl-g', 'hl-b'); block.classList.add('hl-' + it.color);
            } else b.marks.push(rec);
        }
        return true;
    }

    function claimRecover(idx) {
        const it = recoverListCache[idx]; if (!it) return;
        const sel = document.querySelector('.ann-rec-row[data-idx="' + idx + '"] .ann-rec-sel');
        const target = sel ? sel.value : null;
        if (!target) return;
        claimWith(it, target);
        save();
        renderRecoverList();
    }

    async function smartRecover() {
        const blocks = [...document.querySelectorAll('.note-article [data-sid]')];
        const list = buildRecoverList();
        let claimed = 0;
        for (const it of list) {
            if (it.kind === 'hl') continue;  // 无文本无法智能匹配
            let bestSid = null, bestLen = 0;
            for (const el of blocks) {
                const L = lcsLen(it.text, ownText(el));
                if (L > bestLen) { bestLen = L; bestSid = el.dataset.sid; }
            }
            const th = Math.max(8, Math.floor(it.text.length * 0.4));
            if (bestSid && bestLen >= th) { claimWith(it, bestSid); claimed++; }
        }
        save();
        renderRecoverList();
        alert(claimed > 0 ? `智能匹配认领了 ${claimed} 条，其余请手动认领。` : '没有可自动匹配的标注，请手动选择目标条目。');
    }

    /** 从导出备份补充当前笔记中缺失的标注（覆盖迁移时被清理的孤儿） */
    async function mergeBackupAnnots(obj) {
        const annot = obj && obj.__v === 2 ? obj.annot || {} : obj;
        const imgs = obj && obj.__v === 2 ? obj.imgs || {} : {};
        if (!annot || typeof annot !== 'object' || Array.isArray(annot)) throw new Error('不是标注备份文件');
        for (const [id, durl] of Object.entries(imgs))
            try { await imgPut(id, await (await fetch(durl)).blob()); } catch (e) { }
        const src = annot[curId];
        if (!src) { alert('该备份里没有当前笔记（' + curId + '）的标注。'); return; }
        const dst = data[curId] || (data[curId] = { hl: {}, notes: {}, marks: [] });
        for (const [k, c] of Object.entries(src.hl || {})) if (!dst.hl[k]) dst.hl[k] = c;
        mergeNotes(dst, src);
        const gids = new Set((dst.marks || []).map(gidOf));
        dst.marks = dst.marks || [];
        for (const m of src.marks || []) if (m && m.k && m.t && !gids.has(gidOf(m))) { dst.marks.push(m); gids.add(gidOf(m)); }
        if (src.fml && Object.keys(src.fml).length) Object.assign(dst.fml || (dst.fml = {}), src.fml);
        save();
        apply(curId);            // 重新应用：能匹配的立即显示，其余进待恢复列表
        renderRecoverList();
        alert('已从备份补充当前笔记的标注，请逐条认领。');
    }

    function loadBackup(input) {
        const f = input.files && input.files[0]; if (!f) return;
        const rd = new FileReader();
        rd.onload = async () => {
            try { await mergeBackupAnnots(JSON.parse(rd.result)); }
            catch (e) { alert('读取备份失败: ' + e.message); }
            input.value = '';
        };
        rd.readAsText(f);
    }

    // ============ 浮动工具条 ============
    function hideBar() { if (bar) bar.hidden = true; barTarget = null; }

    function showBar(mode, rect, target) {
        barTarget = target;
        const btns = ['y', 'g', 'b'].map(c =>
            `<button class="ab-dot ab-${c}" data-act="color" data-c="${c}" title="荧光高亮"></button>`);
        if (mode !== 'mark') btns.push(`<button class="ab-btn" data-act="note">📝批注</button>`);
        if (mode !== 'sel') btns.push(`<button class="ab-btn" data-act="clear">清除</button>`);
        bar.innerHTML = btns.join('');
        bar.dataset.mode = mode;
        bar.hidden = false;
        const w = bar.offsetWidth;
        bar.style.left = Math.max(8, Math.min(innerWidth - w - 8, rect.left + rect.width / 2 - w / 2)) + 'px';
        bar.style.top = Math.max(8, rect.top - 46) + 'px';
    }

    function onBarClick(e) {
        const btn = e.target.closest('button');
        if (!btn) return;
        const mode = bar.dataset.mode;
        const act = btn.dataset.act;
        if (act === 'color') {
            const c = btn.dataset.c;
            if (mode === 'sel') { markSelection(c) || setBlockHl(barTarget.block, c); }
            else if (mode === 'mark') recolorMarkGroup(barTarget.gid, c);
            else setBlockHl(barTarget.block, c);
        } else if (act === 'note') {
            renderNoteBox(barTarget.block, bucket().notes[barTarget.block.dataset.sid] || '', true);
        } else if (act === 'clear') {
            if (mode === 'mark') removeMarkGroup(barTarget.gid);
            else setBlockHl(barTarget.block, null);
        }
        hideBar();
    }

    function initBar() {
        bar = document.createElement('div');
        bar.id = 'annBar';
        bar.hidden = true;
        document.body.appendChild(bar);
        bar.addEventListener('mousedown', e => e.preventDefault());  // 别让点按钮清掉选区
        bar.addEventListener('click', onBarClick);

        // 选中文字 → 弹工具条
        document.addEventListener('mouseup', e => {
            if (e.target.closest('#annBar, #fmlBar, #fmlPop')) return;
            setTimeout(() => {
                const sel = getSelection();
                if (!sel.rangeCount || sel.isCollapsed) return;
                const r = sel.getRangeAt(0);
                const cac = r.commonAncestorContainer;
                const el = cac.nodeType === 1 ? cac : cac.parentElement;
                if (!el || !el.closest('#docPane')) return;
                const sc = r.startContainer;
                const block = (sc.nodeType === 3 ? sc.parentElement : sc).closest('[data-sid]');
                if (!block) return;
                showBar('sel', r.getBoundingClientRect(), { block });
            }, 10);
        });

        // 点已有荧光/高亮块 → 修改；点空白 → 收起
        document.addEventListener('click', e => {
            if (e.target.closest('#annBar, #fmlBar, #fmlPop')) return;
            const fk = topKatex(e.target);
            if (fk && !fk.closest('.ann-box')) {
                const sel = getSelection();
                if (sel && !sel.isCollapsed) return;  // 正在选字，交给 mouseup
                e.preventDefault();
                showFmlBar(fk.getBoundingClientRect(), fk);
                return;
            }
            const fm = e.target.closest('.fml-note-mark');
            if (fm) {
                let k = fm.previousElementSibling;
                while (k && !(k.classList && k.classList.contains('katex'))) k = k.previousElementSibling;
                if (k) { showFmlPop(k); return; }
            }
            const sel = getSelection();
            if (sel && !sel.isCollapsed) return;  // 有选区时交给 mouseup
            const mk = e.target.closest('mark.mk');
            if (mk) {
                e.preventDefault();
                showBar('mark', mk.getBoundingClientRect(), { gid: mk.dataset.g });
                return;
            }
            const blk = e.target.closest('.hl-y, .hl-g, .hl-b');
            if (blk && blk.closest('#docPane') && !e.target.closest('a')) {
                showBar('block', { left: e.clientX, width: 0, top: e.clientY }, { block: blk });
                return;
            }
            hideBars();
        });

        window.addEventListener('scroll', () => { hideBar(); hideFmlBar(); hideFmlPop(); }, { passive: true });
    }

    // ============ 备份：导出 / 导入（合并，批注图片随包 base64） ============
    // ---- 真题页数据打包/恢复（同源 localStorage + examNoteImg IndexedDB）----
    function examImgDbOpen() {
        return new Promise(function (res, rej) {
            const rq = indexedDB.open('examNoteImg', 1);
            rq.onupgradeneeded = () => rq.result.createObjectStore('imgs');
            rq.onsuccess = () => res(rq.result);
            rq.onerror = () => rej(rq.error);
        });
    }
    function examImgGetRaw(db, id) {
        return new Promise(function (res) {
            try {
                const rq = db.transaction('imgs').objectStore('imgs').get(id);
                rq.onsuccess = () => res(rq.result || null);
                rq.onerror = () => res(null);
            } catch (e) { res(null); }
        });
    }
    function examImgPutRaw(db, id, blob) {
        return new Promise(function (res, rej) {
            const tx = db.transaction('imgs', 'readwrite');
            tx.objectStore('imgs').put(blob, id);
            tx.oncomplete = () => res();
            tx.onerror = () => rej(tx.error);
        });
    }
    async function collectExamData() {
        const exam = { notes: {}, favs: null, reviews: {}, imgs: {} };
        for (let i = 0; i < localStorage.length; i++) {
            const k = localStorage.key(i);
            if (k.indexOf('examNote-') === 0) exam.notes[k] = localStorage.getItem(k);
            else if (k.indexOf('examReview-') === 0) exam.reviews[k] = localStorage.getItem(k);
        }
        exam.favs = localStorage.getItem('examFav');
        // 贴图：从所有真题笔记文本抽 [图:id]，回源 IndexedDB 转 base64
        const ids = new Set();
        Object.keys(exam.notes).forEach(k =>
            (exam.notes[k].match(/\[图:([a-z0-9]+)\]/g) || []).forEach(m => ids.add(m.slice(3, -1))));
        if (ids.size) {
            try {
                const db = await examImgDbOpen();
                for (const id of ids) {
                    const blob = await examImgGetRaw(db, id);
                    if (blob) exam.imgs[id] = await blobToDataURL(blob);
                }
            } catch (e) { /* DB 打不开则只导文本 */ }
        }
        return exam;
    }
    async function restoreExamData(exam) {
        if (!exam || typeof exam !== 'object') return false;
        let touched = false;
        for (const [k, v] of Object.entries(exam.notes || {}))
            if (typeof v === 'string') { localStorage.setItem(k, v); touched = true; }
        for (const [k, v] of Object.entries(exam.reviews || {}))
            if (typeof v === 'string') { localStorage.setItem(k, v); touched = true; }
        if (exam.favs) {
            try {
                const cur = JSON.parse(localStorage.getItem('examFav') || '{}');
                const inc = JSON.parse(exam.favs);
                if (inc && typeof inc === 'object') {
                    localStorage.setItem('examFav', JSON.stringify(Object.assign(cur, inc)));
                    touched = true;
                }
            } catch (e) { /* 收藏格式异常跳过 */ }
        }
        const imgIds = Object.keys(exam.imgs || {});
        if (imgIds.length) {
            try {
                const db = await examImgDbOpen();
                for (const id of imgIds)
                    await examImgPutRaw(db, id, await (await fetch(exam.imgs[id])).blob());
                touched = true;
            } catch (e) { /* 图片还原失败不阻塞文本 */ }
        }
        return touched;
    }

    /** 合并批注文本：同笔记内归一化文本已存在则跳过（跨设备合并防重复批注框） */
    function mergeNotes(dst, src) {
        const norm = t => (t || '').replace(/\s+/g, ' ').trim();
        const have = new Set(Object.values(dst.notes || {}).map(norm));
        for (const [k, t] of Object.entries(src || {})) {
            if (have.has(norm(t))) continue;
            dst.notes[k] = t; have.add(norm(t));
        }
    }

    async function exportAnnot() {
        const ids = new Set();
        for (const b of Object.values(data))
            for (const t of Object.values(b.notes || {})) refsOf(t).forEach(id => ids.add(id));
        const imgs = {};
        for (const id of ids) {
            const blob = await imgGet(id);
            if (blob) imgs[id] = await blobToDataURL(blob);
        }
        const payload = { __fmt: 'math-note-annot', __v: 2, annot: data, imgs, exam: await collectExamData() };
        const blob = new Blob([JSON.stringify(payload, null, 1)], { type: 'application/json' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = '数学笔记标注-' + new Date().toISOString().slice(0, 10) + '.json';
        a.click();
        URL.revokeObjectURL(a.href);
    }

    function importAnnot(input) {
        const f = input.files && input.files[0];
        if (!f) return;
        const rd = new FileReader();
        rd.onload = async () => {
            try {
                const obj = JSON.parse(rd.result);
                // v2 格式带图片；旧格式整个对象就是 annot
                const annot = obj && obj.__v === 2 ? obj.annot || {} : obj;
                const imgs = obj && obj.__v === 2 ? obj.imgs || {} : {};
                if (!annot || typeof annot !== 'object' || Array.isArray(annot)) throw new Error('不是标注备份文件');
                for (const [id, durl] of Object.entries(imgs))
                    await imgPut(id, await (await fetch(durl)).blob());
                for (const [id, src] of Object.entries(annot)) {
                    const dst = data[id] || (data[id] = { hl: {}, notes: {}, marks: [] });
                    Object.assign(dst.hl, src.hl || {});
                    mergeNotes(dst, src);
                    const gids = new Set((dst.marks || []).map(gidOf));
                    for (const m of src.marks || [])
                        if (m && m.k && m.t && !gids.has(gidOf(m))) dst.marks.push(m);
                    if (src.fml && Object.keys(src.fml).length) {
                        const df = dst.fml || (dst.fml = {});
                        Object.assign(df, src.fml);
                    }
                }
                save();
                // 真题页数据（笔记/收藏/点评/贴图）随包还原
                const examOk = await restoreExamData(obj.exam);
                alert(examOk ? '导入成功，已合并到现有标注（含真题笔记/收藏/点评）' : '导入成功，已合并到现有标注');
                location.reload();
            } catch (e) {
                alert('导入失败: ' + e.message);
            }
            input.value = '';
        };
        rd.readAsText(f);
    }

    // ============ 公式标注 UI（高亮 / 给公式写批注；不再显示源码） ============
    let fmlBar = null, fmlPop = null;
    let fmlTarget = null, fmlPopTarget = null;

    function hideFmlBar() { if (fmlBar) fmlBar.hidden = true; fmlTarget = null; }
    function hideFmlPop() { if (fmlPop) fmlPop.hidden = true; fmlPopTarget = null; }
    function hideBars() { hideBar(); hideFmlBar(); hideFmlPop(); }
    function showFmlBar(rect, target) {
        fmlTarget = target;
        const btns = [
            '<button class="ab-dot ab-y" data-fact="hl" data-c="y" title="公式高亮·黄"></button>',
            '<button class="ab-dot ab-g" data-fact="hl" data-c="g" title="公式高亮·绿"></button>',
            '<button class="ab-dot ab-b" data-fact="hl" data-c="b" title="公式高亮·蓝"></button>',
            '<button class="ab-btn" data-fact="note" title="给公式写批注 / 打标签">📝批注</button>',
            '<button class="ab-btn" data-fact="clear" title="清除该公式的高亮/批注/标签">清除</button>'
        ].join('');
        fmlBar.innerHTML = btns;
        fmlBar.hidden = false;
        const w = fmlBar.offsetWidth;
        fmlBar.style.left = Math.max(8, Math.min(innerWidth - w - 8, rect.left + rect.width / 2 - w / 2)) + 'px';
        fmlBar.style.top = Math.max(8, rect.top - 46) + 'px';
    }
    function onFmlBarClick(e) {
        const btn = e.target.closest('button'); if (!btn || !fmlTarget) return;
        const fact = btn.dataset.fact, el = fmlTarget;
        if (fact === 'hl') setFmlHl(el, btn.dataset.c);
        else if (fact === 'note') showFmlPop(el);
        else if (fact === 'clear') clearFml(el);
        hideFmlBar();
    }
    function setFmlHl(el, c) {
        const key = el.dataset.fid; const b = ensureFml();
        const rec = b[key] || (b[key] = {});
        el.classList.remove('fml-hl-y', 'fml-hl-g', 'fml-hl-b');
        if (rec.hl === c) delete rec.hl; else { rec.hl = c; el.classList.add('fml-hl-' + c); }
        if (!Object.keys(rec).length) delete b[key];
        save();
    }
    function showFmlPop(el) {
        fmlPopTarget = el;
        const key = el.dataset.fid; const b = data[curId] && data[curId].fml;
        const rec = (b && b[key]) || {};
        fmlPop.querySelector('.fml-pop-edit').value = rec.note || '';
        fmlPop.querySelector('.fml-label-input').value = rec.label || '';
        fmlPop.hidden = false;
        const r = el.getBoundingClientRect();
        fmlPop.style.left = Math.max(8, Math.min(innerWidth - 308, r.left)) + 'px';
        fmlPop.style.top = Math.min(innerHeight - 190, r.bottom + 8) + 'px';
        fmlPop.querySelector('.fml-pop-edit').focus();
    }
    function fmlSaveNote() {
        const el = fmlPopTarget; if (!el) return;
        const key = el.dataset.fid; const b = ensureFml();
        const rec = b[key] || (b[key] = {});
        const note = fmlPop.querySelector('.fml-pop-edit').value.trim();
        const label = fmlPop.querySelector('.fml-label-input').value.trim();
        if (note) rec.note = note; else delete rec.note;
        if (label) rec.label = label; else delete rec.label;
        if (!Object.keys(rec).length) delete b[key];
        save();
        applyFml();
        hideFmlPop(); hideFmlBar();
    }
    const fmlClosePop = () => hideFmlPop();
    function clearFml(el) {
        const key = el.dataset.fid; const b = data[curId];
        if (b && b.fml) { delete b.fml[key]; save(); }
        el.classList.remove('fml-hl-y', 'fml-hl-g', 'fml-hl-b');
        applyFml();
    }
    // 公式放大 / 复制 / 目录（源码展示）已移除
    function initFmlUI() {
        fmlBar = document.createElement('div'); fmlBar.id = 'fmlBar'; fmlBar.hidden = true;
        fmlBar.addEventListener('mousedown', e => e.preventDefault());
        fmlBar.addEventListener('click', onFmlBarClick);
        document.body.appendChild(fmlBar);

        fmlPop = document.createElement('div'); fmlPop.id = 'fmlPop'; fmlPop.className = 'fml-pop'; fmlPop.hidden = true;
        fmlPop.innerHTML = `<div class="fml-pop-head">公式批注 <button onclick="Annot.fmlClosePop()">✕</button></div>
            <textarea class="fml-pop-edit" placeholder="给这个公式写批注…"></textarea>
            <div class="fml-pop-foot">
                <input class="fml-label-input" placeholder="标签，如：洛必达 / 分部积分">
                <button onclick="Annot.fmlSaveNote()">保存</button>
            </div>`;
        document.body.appendChild(fmlPop);
    }

    initBar();
    initFmlUI();

    // ============ 富文本编辑（移植自 exam.js 笔记富文本体系，令牌对齐） ============
    const ANN_FMT_RE = /<c:(#[0-9a-fA-F]{6})>|<h:(#[0-9a-fA-F]{6})>|<\/c>|<\/h>|<b>|<\/b>|<i>|<\/i>|<h1>|<\/h1>|<h2>|<\/h2>/g;
    const ANN_COLORS = ['#e03131', '#e8590c', '#2f9e44', '#1971c2', '#9c36b5'];
    const ANN_HLS = ['#fff3bf', '#d3f9d8', '#d0ebff', '#ffe3e3', '#ffdcc4'];

    // ---- 贴图缩略图条：编辑器内不显示图片，只在编辑框下方以卡片显示（与真题页笔记交互对齐） ----
    function annThumbCard(id) {
        const card = document.createElement('span');
        card.className = 'ann-img-card';
        card.dataset.img = id;
        card.draggable = true;
        const img = document.createElement('img');
        img.dataset.img = id;
        img.alt = '批注图片';
        img.onclick = () => openLightbox(img.src || '');
        const del = document.createElement('button');
        del.type = 'button';
        del.className = 'ann-img-del';
        del.title = '删除图片';
        del.textContent = '×';
        del.onclick = e => {
            e.stopPropagation();
            card.remove();
            const strip = card.parentElement;
            if (strip && !strip.querySelector('.ann-img-card')) strip.hidden = true;
        };
        card.append(img, del);
        // 缩略图条内拖拽排序：拖动调整顺序，顺序即存储顺序（annStripIds 按 DOM 位置序列化）
        card.addEventListener('dragstart', e => { e.dataTransfer.setData('text/plain', id); e.dataTransfer.effectAllowed = 'move'; card.classList.add('dragging'); });
        card.addEventListener('dragend', () => { card.classList.remove('dragging'); document.querySelectorAll('.ann-img-card.over').forEach(c => c.classList.remove('over')); });
        card.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; card.classList.add('over'); });
        card.addEventListener('dragleave', () => card.classList.remove('over'));
        card.addEventListener('drop', e => {
            e.preventDefault();
            card.classList.remove('over');
            const dragged = document.querySelector('.ann-img-card.dragging');
            if (!dragged || dragged === card) return;
            const r = card.getBoundingClientRect();
            const after = (e.clientX - r.left) > r.width / 2;   // 横向条：按左右半区决定插前/插后
            if (after) card.after(dragged); else card.before(dragged);
            const ed = card.closest('.ann-box') && card.closest('.ann-box').querySelector('.ann-edit');
            if (ed) annPreviewOnInput(ed);   // 实时预览同步新顺序（保存后落盘）
        });
        return card;
    }
    function renderAnnStrip(strip, ids) {
        strip.innerHTML = '';
        ids.forEach(id => strip.appendChild(annThumbCard(id)));
        strip.hidden = !ids.length;
        fillImgs(strip);
    }
    function annStripIds(el) {
        const strip = el.closest('.ann-box') && el.closest('.ann-box').querySelector('.ann-imgs');
        return strip ? [...strip.querySelectorAll('.ann-img-card')].map(c => c.dataset.img) : [];
    }

    // 图片节点（批注内嵌）：img.ann-img[data-img] + 删除按钮（contenteditable 内不可编辑）
    function annImgNode(id) {
        const img = document.createElement('img');
        img.className = 'ann-img'; img.dataset.img = id; img.alt = '批注图片';
        img.setAttribute('contenteditable', 'false');
        img.onclick = () => openLightbox(img.src || '');
        const del = document.createElement('button');
        del.type = 'button'; del.className = 'ann-img-del';
        del.title = '删除图片'; del.textContent = '×';
        del.setAttribute('contenteditable', 'false');
        del.onclick = e => { e.stopPropagation(); img.remove(); del.remove(); };
        const wrap = document.createElement('span');
        wrap.className = 'ann-img-wrap'; wrap.append(img, del);
        return wrap;
    }
    // contenteditable DOM → 存储 token 文本（与 exam.js editorToNote 同源；图片走 IMG[data-img]）
    function annEditorToNote(el) {
        const rgbToHex = v => { const m = /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(v || ''); return m ? '#' + [1, 2, 3].map(k => (+m[k]).toString(16).padStart(2, '0')).join('') : null; };
        // 任意颜色串（hex/rgb/命名色）归一为 #rrggbb；借助临时元素让浏览器自行规范化
        const normColor = v => { if (!v) return null; const tmp = document.createElement('span'); tmp.style.color = v; return rgbToHex(tmp.style.color); };
        const isBold = n => (n && n.nodeType === 1) && (n.tagName === 'B' || n.tagName === 'STRONG' || /bold/i.test(n.style.fontWeight || ''));
        const isItalic = n => (n && n.nodeType === 1) && (n.tagName === 'I' || n.tagName === 'EM' || /italic/i.test(n.style.fontStyle || ''));
        let base = (function run(n, c, h, b, i) {
            let s = '';
            for (const ch of n.childNodes) {
                if (ch.nodeType === 3) {
                    const t = ch.nodeValue.replace(/\u00A0/g, ' '); if (!t) continue;
                    let inner = t;
                    if (i) inner = '<i>' + inner + '</i>';
                    if (b) inner = '<b>' + inner + '</b>';
                    if (h) inner = '<h:' + h + '>' + inner + '</h>';
                    if (c) inner = '<c:' + c + '>' + inner + '</c>';
                    s += inner;
                } else if (ch.nodeType === 1) {
                    if (ch.classList && ch.classList.contains('ann-img-wrap')) { const img = ch.querySelector('img[data-img]'); if (img) s += '[图:' + img.dataset.img + ']'; }
                    else if (ch.tagName === 'IMG' && ch.dataset.img) s += '[图:' + ch.dataset.img + ']';
                    else if (ch.tagName === 'BR') s += '\n';
                    else if (ch.tagName === 'H1') { if (s && !s.endsWith('\n')) s += '\n'; s += '<h1>' + run(ch, c, h, false, false) + '</h1>' + '\n'; }
                    else if (ch.tagName === 'H2') { if (s && !s.endsWith('\n')) s += '\n'; s += '<h2>' + run(ch, c, h, false, false) + '</h2>' + '\n'; }
                    else if (isBold(ch)) { const block = ch.tagName === 'DIV' || ch.tagName === 'P'; if (block && s && !s.endsWith('\n')) s += '\n'; s += run(ch, c, h, true, i); if (block && s && !s.endsWith('\n')) s += '\n'; }
                    else if (isItalic(ch)) { s += run(ch, c, h, b, true); }
                    else {
                        let nc = c, nh = h;
                        if (ch.style) { const hc = normColor(ch.style.color); if (hc) nc = hc; const hb = normColor(ch.style.backgroundColor); if (hb) nh = hb; }
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
        // 贴图不进编辑器 DOM：缩略图条中的令牌统一追加到文本末尾
        const stripIds = annStripIds(el);
        if (stripIds.length) {
            if (base && !base.endsWith('\n')) base += '\n';
            base += stripIds.map(id => '[图:' + id + ']').join('');
        }
        return base;
    }
    // token 文本 → contenteditable DOM（与 exam.js noteToEditor 同源；[图:id] 不进编辑器，进下方缩略图条）
    function annNoteToEditor(el, text) {
        el.innerHTML = '';
        const stack = [el];
        const imgIds = [];
        const emitText = s => { const lines = s.split('\n'); lines.forEach((line, k) => { if (k > 0) stack[stack.length - 1].appendChild(document.createElement('br')); if (line) stack[stack.length - 1].appendChild(document.createTextNode(line)); }); };
        let i = 0;
        while (i < text.length) {
            const mi = text.indexOf('[图:', i);
            ANN_FMT_RE.lastIndex = i;
            const mf = ANN_FMT_RE.exec(text);
            if (mf && (mi < 0 || mf.index <= mi)) {
                emitText(text.slice(i, mf.index));
                const m0 = mf[0];
                if (m0 === '</c>' || m0 === '</h>' || m0 === '</b>' || m0 === '</i>' || m0 === '</h1>' || m0 === '</h2>') { if (stack.length > 1) stack.pop(); }
                else { let node; if (m0 === '<b>') node = document.createElement('b'); else if (m0 === '<i>') node = document.createElement('i'); else if (m0 === '<h1>') node = document.createElement('h1'); else if (m0 === '<h2>') node = document.createElement('h2'); else if (mf[1]) node = Object.assign(document.createElement('span'), { style: 'color:' + mf[1] }); else node = Object.assign(document.createElement('mark'), { style: 'background:' + mf[2] }); stack[stack.length - 1].appendChild(node); stack.push(node); }
                i = mf.index + mf[0].length;
            } else if (mi >= 0) {
                emitText(text.slice(i, mi));
                const m2 = /\[图:([a-z0-9]+)\]/.exec(text.slice(mi));
                if (m2) imgIds.push(m2[1]);
                i = mi + m2[0].length;
            } else { emitText(text.slice(i)); i = text.length; }
        }
        // 贴图缩略图条：编辑框下方卡片显示
        const strip = el.closest('.ann-box') && el.closest('.ann-box').querySelector('.ann-imgs');
        if (strip) renderAnnStrip(strip, imgIds);
    }
    function annHint(ed, msg) {
        const box = ed.closest('.ann-box');
        let el = box && box.querySelector('.ann-hint');
        if (!el && box) { el = document.createElement('span'); el.className = 'ann-hint'; box.appendChild(el); }
        if (!el) return;
        if (!msg) { el.textContent = ''; el.classList.remove('show'); return; }
        el.textContent = msg; el.classList.add('show');
        clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove('show'), 2000);
    }
    function annApplyFormat(box, cmd, val) {
        const ed = box.querySelector('.ann-edit');
        if (!ed || !ed.isContentEditable) return;
        const sel = getSelection();
        const inEd = !!sel.rangeCount && ed.contains(sel.anchorNode);
        if (!inEd || (sel.isCollapsed && cmd !== 'plain')) { annHint(ed, '先选中要设置格式的文字'); return; }
        ed.focus();
        if (cmd === 'h1' || cmd === 'h2') {
            try { document.execCommand('styleWithCSS', false, false); } catch (e) { }
            document.execCommand('formatBlock', false, cmd === 'h1' ? 'H1' : 'H2');
        } else if (cmd === 'plain') {
            try { document.execCommand('styleWithCSS', false, false); } catch (e) { }
            document.execCommand('formatBlock', false, 'P');
            document.execCommand('removeFormat');
        } else {
            try { document.execCommand('styleWithCSS', false, true); } catch (e) { }
            document.execCommand(cmd, false, val || null);
        }
    }
    function annToolbarHtml() {
        return `<div class="ann-toolbar" hidden>
            <span class="ann-nt-lab">字色</span>
            ${ANN_COLORS.map(c => `<button type="button" class="ann-nt-c" style="color:${c}" onmousedown="event.preventDefault()" onclick="Annot.applyFmt(this.closest('.ann-box'),'foreColor','${c}')" title="字色 ${c}">A</button>`).join('')}
            <span class="ann-nt-sep"></span>
            <span class="ann-nt-lab">高亮</span>
            ${ANN_HLS.map(c => `<button type="button" class="ann-nt-h" style="background:${c}" onmousedown="event.preventDefault()" onclick="Annot.applyFmt(this.closest('.ann-box'),'hiliteColor','${c}')" title="高亮 ${c}"></button>`).join('')}
            <span class="ann-nt-sep"></span>
            <button type="button" class="ann-nt-b" onmousedown="event.preventDefault()" onclick="Annot.applyFmt(this.closest('.ann-box'),'bold')" title="加粗 (Ctrl+B)"><b>B</b></button>
            <button type="button" class="ann-nt-i" onmousedown="event.preventDefault()" onclick="Annot.applyFmt(this.closest('.ann-box'),'italic')" title="斜体 (Ctrl+I)"><i>I</i></button>
            <button type="button" class="ann-nt-h1" onmousedown="event.preventDefault()" onclick="Annot.applyFmt(this.closest('.ann-box'),'h1')" title="大标题">H1</button>
            <button type="button" class="ann-nt-h2" onmousedown="event.preventDefault()" onclick="Annot.applyFmt(this.closest('.ann-box'),'h2')" title="中标题">H2</button>
            <span class="ann-nt-sep"></span>
            <button type="button" class="ann-nt-x" onmousedown="event.preventDefault()" onclick="Annot.applyFmt(this.closest('.ann-box'),'plain')" title="转为普通正文（去掉标题/字色/高亮）">正文</button>
        </div>`;
    }

    return { apply, saveNote, cancelNote, editNote, delNote, exportAnnot, importAnnot,
             openRecover, closeRecover, claimRecover, smartRecover, loadBackup,
             fmlSaveNote, fmlClosePop, applyFmt: annApplyFormat };
})();

window.Annot = Annot;  // 顶层 const 不上 window，reader.js 靠 window.Annot 判断
