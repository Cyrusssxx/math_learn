/* 考研数学笔记 - 批注系统：荧光高亮（选中文字/整块）+ 文字批注，存 localStorage
 * 锚定方式：每个块（li/p）按自身文本哈希生成稳定 key，笔记内容不变则标注永久有效 */

const Annot = (() => {
    const LS = 'notesAnnot';
    let data = {};          // { noteId: { hl:{key:color}, notes:{key:text}, marks:[{k,t,c,n}] } }
    let curId = null;
    let bar = null;         // 浮动工具条
    let barTarget = null;   // 当前操作对象 {block} / {gid}

    try { data = JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) { data = {}; }
    const save = () => localStorage.setItem(LS, JSON.stringify(data));
    const bucket = () => data[curId] || (data[curId] = { hl: {}, notes: {}, marks: [] });
    const escA = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

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

    function keyBlocks(article) {
        const seen = {};
        article.querySelectorAll('li, p').forEach(el => {
            const h = hash(ownText(el));
            const n = seen[h] = (seen[h] || 0) + 1;
            el.dataset.ak = n > 1 ? h + '#' + n : h;
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
        const block = (sc.nodeType === 3 ? sc.parentElement : sc).closest('[data-ak]');
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
        const rec = { k: block.dataset.ak, t, c: color, n: occ };
        if (!wrapText(block, t, color, occ, gidOf(rec))) return false;
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
            bucket().hl[block.dataset.ak] = color;
        } else {
            delete bucket().hl[block.dataset.ak];
        }
        save();
    }

    // ============ 文字批注 ============
    /** 展示态文本：转义后把 [图:id] 占位替换成 img，再异步从 IndexedDB 填 src */
    const noteHtml = t => escA(t).replace(/\[图:([a-z0-9]+)\]/g,
        '<img class="ann-img" data-img="$1" alt="批注图片">');

    function fillImgs(box) {
        box.querySelectorAll('img.ann-img[data-img]').forEach(img => {
            imgGet(img.dataset.img).then(blob => {
                if (blob) img.src = URL.createObjectURL(blob);
                else img.replaceWith('[图片已丢失]');
            });
        });
    }

    /** 编辑框内 Ctrl+V 贴图：存库后在光标处插入 [图:id] 占位 */
    function onPasteImg(e) {
        const it = [...(e.clipboardData?.items || [])].find(i => i.type.startsWith('image/'));
        if (!it) return;
        e.preventDefault();
        const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
        imgPut(id, it.getAsFile()).then(() => {
            const ta = e.target;
            const tag = `[图:${id}]`;
            const p = ta.selectionStart;
            ta.value = ta.value.slice(0, p) + tag + ta.value.slice(ta.selectionEnd);
            ta.selectionStart = ta.selectionEnd = p + tag.length;
        }).catch(() => alert('图片保存失败'));
    }

    function renderNoteBox(block, text, editing) {
        const old = block.querySelector(':scope > .ann-box');
        if (old) old.remove();
        const box = document.createElement('div');
        box.className = 'ann-box';
        if (editing) {
            box.innerHTML = `<textarea class="ann-edit" placeholder="写点批注…（Ctrl+V 可直接贴图）">${escA(text || '')}</textarea>
                <div class="ann-ops"><button onclick="Annot.saveNote(this)">保存</button>
                <button onclick="Annot.cancelNote(this)">取消</button></div>`;
            box.querySelector('textarea').addEventListener('paste', onPasteImg);
        } else {
            box.innerHTML = `<span class="ann-icon">📝</span><span class="ann-text">${noteHtml(text)}</span>
                <span class="ann-ops"><button onclick="Annot.editNote(this)">改</button>
                <button onclick="Annot.delNote(this)">删</button></span>`;
            fillImgs(box);
        }
        const childUl = block.querySelector(':scope > ul');
        block.insertBefore(box, childUl);  // 批注紧跟条目本身文字，在子列表之前
        if (editing) box.querySelector('textarea').focus();
    }

    function saveNote(btn) {
        const block = btn.closest('[data-ak]');
        const text = btn.closest('.ann-box').querySelector('textarea').value.trim();
        const prev = bucket().notes[block.dataset.ak] || '';
        const kept = refsOf(text);
        imgDel(refsOf(prev).filter(id => !kept.includes(id)));  // 删掉不再引用的图
        if (text) bucket().notes[block.dataset.ak] = text;
        else delete bucket().notes[block.dataset.ak];
        save();
        if (text) renderNoteBox(block, text, false);
        else block.querySelector(':scope > .ann-box').remove();
    }

    function cancelNote(btn) {
        const block = btn.closest('[data-ak]');
        const saved = bucket().notes[block.dataset.ak];
        // 丢弃编辑中新贴但未保存的图
        const kept = refsOf(saved || '');
        imgDel(refsOf(btn.closest('.ann-box').querySelector('textarea').value).filter(id => !kept.includes(id)));
        if (saved) renderNoteBox(block, saved, false);
        else block.querySelector(':scope > .ann-box').remove();
    }

    function editNote(btn) {
        const block = btn.closest('[data-ak]');
        renderNoteBox(block, bucket().notes[block.dataset.ak] || '', true);
    }

    function delNote(btn) {
        if (!confirm('确定删除这条批注？')) return;   // 删除需确认，修改不用
        const block = btn.closest('[data-ak]');
        imgDel(refsOf(bucket().notes[block.dataset.ak]));  // 随批注删掉其引用的图
        delete bucket().notes[block.dataset.ak];
        save();
        block.querySelector(':scope > .ann-box').remove();
    }

    // ============ 恢复：正文渲染后调用 ============
    function apply(noteId) {
        curId = noteId;
        const article = document.querySelector('.note-article');
        if (!article) return;
        keyBlocks(article);
        const b = data[noteId];
        if (!b) return;
        const byKey = {};
        article.querySelectorAll('[data-ak]').forEach(el => { byKey[el.dataset.ak] = el; });
        for (const [k, c] of Object.entries(b.hl || {}))
            if (byKey[k]) byKey[k].classList.add('hl-' + c);
        for (const m of b.marks || [])
            if (byKey[m.k]) wrapText(byKey[m.k], m.t, m.c, m.n, gidOf(m));
        for (const [k, t] of Object.entries(b.notes || {}))
            if (byKey[k]) renderNoteBox(byKey[k], t, false);
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
            renderNoteBox(barTarget.block, bucket().notes[barTarget.block.dataset.ak] || '', true);
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
            if (e.target.closest('#annBar')) return;
            setTimeout(() => {
                const sel = getSelection();
                if (!sel.rangeCount || sel.isCollapsed) return;
                const r = sel.getRangeAt(0);
                const cac = r.commonAncestorContainer;
                const el = cac.nodeType === 1 ? cac : cac.parentElement;
                if (!el || !el.closest('#docPane')) return;
                const sc = r.startContainer;
                const block = (sc.nodeType === 3 ? sc.parentElement : sc).closest('[data-ak]');
                if (!block) return;
                showBar('sel', r.getBoundingClientRect(), { block });
            }, 10);
        });

        // 点已有荧光/高亮块 → 修改；点空白 → 收起
        document.addEventListener('click', e => {
            if (e.target.closest('#annBar') || e.target.closest('.ann-box')) return;
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
            hideBar();
        });

        window.addEventListener('scroll', hideBar, { passive: true });
    }

    // ============ 备份：导出 / 导入（合并，批注图片随包 base64） ============
    async function exportAnnot() {
        const ids = new Set();
        for (const b of Object.values(data))
            for (const t of Object.values(b.notes || {})) refsOf(t).forEach(id => ids.add(id));
        const imgs = {};
        for (const id of ids) {
            const blob = await imgGet(id);
            if (blob) imgs[id] = await blobToDataURL(blob);
        }
        const payload = { __fmt: 'math-note-annot', __v: 2, annot: data, imgs };
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
                    Object.assign(dst.notes, src.notes || {});
                    const gids = new Set((dst.marks || []).map(gidOf));
                    for (const m of src.marks || [])
                        if (m && m.k && m.t && !gids.has(gidOf(m))) dst.marks.push(m);
                }
                save();
                alert('导入成功，已合并到现有标注');
                location.reload();
            } catch (e) {
                alert('导入失败: ' + e.message);
            }
            input.value = '';
        };
        rd.readAsText(f);
    }

    initBar();
    return { apply, saveNote, cancelNote, editNote, delNote, exportAnnot, importAnnot };
})();

window.Annot = Annot;  // 顶层 const 不上 window，reader.js 靠 window.Annot 判断
