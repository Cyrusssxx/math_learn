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
            bucket().hl[block.dataset.sid] = color;
        } else {
            delete bucket().hl[block.dataset.sid];
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
        const block = btn.closest('[data-sid]');
        const text = btn.closest('.ann-box').querySelector('textarea').value.trim();
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
        imgDel(refsOf(btn.closest('.ann-box').querySelector('textarea').value).filter(id => !kept.includes(id)));
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
        let orphans = 0;
        for (const [k, c] of Object.entries(b.hl || {})) {
            if (byKey[k]) byKey[k].classList.add('hl-' + c); else orphans++;
        }
        for (const m of b.marks || []) {
            if (byKey[m.k]) wrapText(byKey[m.k], m.t, m.c, m.n, gidOf(m)); else orphans++;
        }
        for (const [k, t] of Object.entries(b.notes || {})) {
            if (byKey[k]) renderNoteBox(byKey[k], t, false); else orphans++;
        }
        if (orphans > 0 && !_notified) {
            _notified = true;
            annNotify(`有 ${orphans} 条标注因笔记结构变动（增/删/移动条目）已无法定位，可「恢复标注」找回。`, { recover: true });
        }
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

    /** 收集当前笔记里「键不在当前 DOM」的标注 = 待恢复孤儿（含迁移残留 b.orphans） */
    function buildRecoverList() {
        const article = document.querySelector('.note-article');
        if (!article) return [];
        const byKey = {};
        article.querySelectorAll('[data-sid]').forEach(el => byKey[el.dataset.sid] = el);
        const b = data[curId]; if (!b) return [];
        const list = [];
        for (const [k, c] of Object.entries(b.hl || {})) if (!byKey[k]) list.push({ kind: 'hl', key: k, color: c, text: '(整块荧光·' + colorName(c) + ')' });
        for (const [k, t] of Object.entries(b.notes || {})) if (!byKey[k]) list.push({ kind: 'note', key: k, text: t });
        for (const m of (b.marks || [])) if (!byKey[m.k]) list.push({ kind: 'mark', key: m.k, text: m.t, color: m.c, n: m.n });
        const o = b.orphans;
        if (o) {
            for (const [k, c] of Object.entries(o.hl || {})) list.push({ kind: 'hl', key: k, color: c, text: '(整块荧光·' + colorName(c) + ')' });
            for (const [k, t] of Object.entries(o.notes || {})) list.push({ kind: 'note', key: k, text: t });
            for (const m of (o.marks || [])) list.push({ kind: 'mark', key: m.k, text: m.t, color: m.c, n: m.n });
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
        for (const [k, t] of Object.entries(src.notes || {})) if (!dst.notes[k]) dst.notes[k] = t;
        const gids = new Set((dst.marks || []).map(gidOf));
        dst.marks = dst.marks || [];
        for (const m of src.marks || []) if (m && m.k && m.t && !gids.has(gidOf(m))) { dst.marks.push(m); gids.add(gidOf(m)); }
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
            if (e.target.closest('#annBar')) return;
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
    return { apply, saveNote, cancelNote, editNote, delNote, exportAnnot, importAnnot,
             openRecover, closeRecover, claimRecover, smartRecover, loadBackup };
})();

window.Annot = Annot;  // 顶层 const 不上 window，reader.js 靠 window.Annot 判断
