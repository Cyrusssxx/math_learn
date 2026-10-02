/* 记忆卡：把笔记站内容拆成挖空卡片，用间隔重复（SM-2 简化）调度复习
   - 卡片来源：data/notes.json（高等数学 gs / 线性代数 xd），按 ## 章节拆卡，过长再拆
   - 挖空：渲染前在文本节点上把关键公式 / 加粗术语替换为可点击的空位
   - 交互：点击空位揭示答案；右下「不会 / 不熟 / 记得」评分；右上「收藏 / 已熟」标记
   - 进度：localStorage（cd_state_v1），支持导出 / 导入
*/
(function () {
    'use strict';

    const LS_KEY = 'cd_state_v1';
    const DAY = 86400000;
    const NEW_PER_DAY = 20;      // 默认每日新卡上限
    const REV_PER_DAY = 120;     // 默认每日复习上限

    let CARDS = [];              // 全部卡片
    let ST = null;               // 进度状态
    let view = 'study';
    let subject = '';            // '' | 'gs' | 'xd'
    let queue = [];              // 当前学习队列（卡片对象）
    let qi = 0;                  // 当前索引
    let revealed = 0;            // 本卡已揭示的空数
    let listPage = 1;
    const PAGE_SIZE = 30;

    // ---------------- 工具 ----------------
    const $ = id => document.getElementById(id);
    const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
    const dayKey = (ts) => new Date(ts || Date.now()).toISOString().slice(0, 10);
    const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

    function toast(msg) {
        const t = $('cdToast');
        t.textContent = msg; t.hidden = false;
        clearTimeout(toast._t);
        toast._t = setTimeout(() => { t.hidden = true; }, 1600);
    }

    // ---------------- 状态 ----------------
    function defaultState() {
        return {
            cards: {},                 // id -> {ease, interval, reps, lapses, due, state, last, star}
            settings: { newPerDay: NEW_PER_DAY, revPerDay: REV_PER_DAY },
            daily: { date: dayKey(), done: 0, newDone: 0, revDone: 0 },
            streak: { last: '', count: 0 }
        };
    }
    function loadState() {
        try {
            const raw = localStorage.getItem(LS_KEY);
            ST = raw ? JSON.parse(raw) : defaultState();
        } catch (e) { ST = defaultState(); }
        const d = defaultState();
        for (const k in d) if (ST[k] === undefined) ST[k] = d[k];
        for (const k in d.settings) if (ST.settings[k] === undefined) ST.settings[k] = d.settings[k];
        if (ST.daily.date !== dayKey()) ST.daily = { date: dayKey(), done: 0, newDone: 0, revDone: 0 };
    }
    function saveState() {
        try { localStorage.setItem(LS_KEY, JSON.stringify(ST)); } catch (e) { }
    }
    function stOf(id) {
        if (!ST.cards[id]) {
            ST.cards[id] = { ease: 2.5, interval: 0, reps: 0, lapses: 0, due: 0, state: 'new', last: 0, star: false };
        }
        return ST.cards[id];
    }

    // ---------------- 拆卡 ----------------
    /** 按二级标题（## ）把一篇笔记拆成若干段 */
    function splitSections(md) {
        const lines = String(md || '').split('\n');
        const secs = [];
        let cur = { name: '', lines: [] };
        for (const ln of lines) {
            const m = /^##\s+(.*)$/.exec(ln);
            if (m) {
                if (cur.lines.join('\n').trim()) secs.push(cur);
                cur = { name: m[1].trim(), lines: [] };
            } else cur.lines.push(ln);
        }
        if (cur.lines.join('\n').trim()) secs.push(cur);
        return secs.filter(s => s.name);   // 丢弃无标题的前言段
    }

    /** 段落过长时按空行块再切，每块不超过 LIMIT 字 */
    function splitLong(md, limit) {
        limit = limit || 1100;
        if (md.length <= limit) return [md];
        const blocks = md.split(/\n{2,}/).map(s => s).filter(Boolean);
        const out = []; let buf = [];
        let len = 0;
        for (const b of blocks) {
            if (len + b.length > limit && buf.length) { out.push(buf.join('\n\n')); buf = []; len = 0; }
            buf.push(b); len += b.length + 2;
        }
        if (buf.length) out.push(buf.join('\n\n'));
        return out.length ? out : [md];
    }

    /** 估算一段 md 能挖出多少空（用于决定是否再拆） */
    function countCloze(md) {
        const inline = (String(md).match(/\$[^$\n]{3,}\$/g) || []).length;
        const bold = (String(md).match(/\*\*[^*\n]{2,40}\*\*/g) || []).length;
        return inline + bold;
    }

    function buildCards(notes) {
        const cards = [];
        for (const n of notes) {
            const secs = splitSections(n.md);
            for (const sec of secs) {
                const parts = splitLong(sec.lines.join('\n'));
                parts.forEach((p, i) => {
                    const id = n.id + '::' + sec.name + (parts.length > 1 ? '#' + (i + 1) : '');
                    cards.push({
                        id, subject: n.subject || 'gs',
                        noteId: n.id, noteTitle: n.title || n.name,
                        chapter: sec.name, part: parts.length > 1 ? `(${i + 1}/${parts.length})` : '',
                        md: p, custom: false
                    });
                });
            }
        }
        // 自定义卡片（用户自建）
        for (const c of (ST.cards && ST.cards.__custom ? [] : [])) { }
        return cards;
    }

    // ---------------- 挖空 ----------------
    const CLOZE_RE = [
        { re: /\$\$[\s\S]+?\$\$/g, whole: true },                       // 独立公式块（跳过，太长）
        { re: /\$[^$\n]{2,120}\$/g, whole: true },                      // 行内公式
        { re: /\*\*[^*\n]{2,40}\*\*/g, whole: true },                  // 加粗术语
        { re: /`[^`\n]{2,60}`/g, whole: true }                          // 行内代码
    ];

    /**
     * 在容器内对文本节点做挖空替换；返回挖空数量
     * 已被挖空的公式不再参与后续规则
     */
    function applyCloze(container, maxCloze) {
        maxCloze = maxCloze || 8;
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
        const nodes = [];
        let n;
        while ((n = walker.nextNode())) if (n.nodeValue && n.nodeValue.trim()) nodes.push(n);

        let made = 0;
        for (const textNode of nodes) {
            if (made >= maxCloze) break;
            let s = textNode.nodeValue;
            let used = false;
            for (const rule of CLOZE_RE) {
                if (used || made >= maxCloze) break;
                rule.re.lastIndex = 0;
                let m, last = 0, replaced = '';
                while ((m = rule.re.exec(s)) && made < maxCloze) {
                    const raw = m[0];
                    const inner = rule.whole ? raw.replace(/^\$+|\$+$/g, '').replace(/^\*\*|\*\*$/g, '').replace(/^`|`$/g, '') : raw;
                    if (!inner || inner.length < 2) continue;
                    replaced += s.slice(last, m.index);
                    replaced += `<span class="cd-cloze" data-c="${esc(inner)}" title="点击显示答案">　　　　</span>`;
                    last = m.index + raw.length;
                    made++; used = true;
                }
                if (used) { replaced += s.slice(last); s = replaced; }
            }
            if (used) {
                const frag = document.createElement('span');
                frag.innerHTML = s;
                textNode.parentNode.replaceChild(frag, textNode);
            }
        }
        return made;
    }

    function revealAll(root) {
        (root || document).querySelectorAll('.cd-cloze:not(.revealed)').forEach(el => revealOne(el));
    }
    function revealOne(el) {
        if (el.classList.contains('revealed')) return;
        const ans = el.getAttribute('data-c') || '';
        el.classList.add('revealed');
        if (ans.indexOf('$') >= 0 && window.katex) {
            try { window.katex.render(ans, el, { displayMode: ans.indexOf('$$') === 0 }); return; } catch (e) { }
        }
        el.textContent = ans;
        revealed++;
        updateFoot();
    }
    function updateFoot() {
        const total = $('cdCard').querySelectorAll('.cd-cloze').length;
        const left = total - revealed;
        $('cardFoot').innerHTML = left > 0
            ? `还剩 <b>${left}</b> 个空 · 点击填空或按 <b>空格</b> 全部显示`
            : `全部答案已显示 · 用下方按钮评价这张卡`;
    }

    // ---------------- 队列 ----------------
    function visibleCards() {
        return CARDS.filter(c => !subject || c.subject === subject);
    }
    function buildQueue() {
        const now = Date.now();
        const due = [], fresh = [];
        for (const c of visibleCards()) {
            const s = stOf(c.id);
            if (s.state === 'mastered' && s.due > now) continue;
            if (s.state === 'new') fresh.push(c);
            else due.push(c);
        }
        due.sort((a, b) => stOf(a.id).due - stOf(b.id).due);
        const st = ST.settings;
        // 今日已复习数量（用于限额）
        const revLeft = Math.max(0, st.revPerDay - ST.daily.revDone);
        const newLeft = Math.max(0, st.newPerDay - ST.daily.newDone);
        queue = due.slice(0, revLeft).concat(fresh.slice(0, newLeft));
        qi = 0; revealed = 0;
    }
    function todayTotal() {
        const now = Date.now();
        let due = 0, fresh = 0;
        for (const c of visibleCards()) {
            const s = stOf(c.id);
            if (s.state === 'new') fresh++;
            else if (s.due <= now) due++;
        }
        return { due, fresh };
    }

    // ---------------- 学习视图 ----------------
    function renderStudy() {
        const t = todayTotal();
        const s = stOf;
        let mastered = 0, learning = 0, freshN = 0, starN = 0;
        visibleCards().forEach(c => {
            const st = s(c.id);
            if (st.state === 'mastered') mastered++;
            else if (st.state === 'learning') learning++;
            else if (st.state === 'new') freshN++;
            if (st.star) starN++;
        });
        $('cdStats').innerHTML = `
            <div class="cd-stat warn"><b>${t.due}</b><span>待复习</span></div>
            <div class="cd-stat"><b>${freshN}</b><span>未学新卡</span></div>
            <div class="cd-stat"><b>${ST.daily.done}</b><span>今日已完成</span></div>
            <div class="cd-stat ok"><b>${mastered}</b><span>已熟</span></div>
            <div class="cd-stat"><b>${learning}</b><span>不熟中</span></div>
            <div class="cd-stat"><b>${ST.streak.count}</b><span>连续天数</span></div>
            <div class="cd-stat"><b>${starN}</b><span>收藏</span></div>`;
        const totalToday = Math.max(1, t.due + freshN);
        $('cdProgressBar').style.width = clamp(ST.daily.done / totalToday * 100, 0, 100) + '%';
        $('cdSub').textContent = `共 ${visibleCards().length} 张卡 · ${mastered} 张已熟`;

        if (qi >= queue.length) { renderDone(t); return; }
        renderCard();
    }

    function renderDone(t) {
        $('cardWrap').innerHTML = `<div class="cd-done">
            <div class="big">${t.due + t.fresh > 0 ? '🎉' : '💤'}</div>
            <h2>${t.due + t.fresh > 0 ? '今日队列已清空' : '今天没有到期的卡片'}</h2>
            <p>${t.due + t.fresh > 0 ? '剩余卡片可在「卡片」列表里手动复习' : '稍后再来，或去笔记站继续整理'}</p>
            <p style="margin-top:10px"><button class="cd-btn" onclick="buildQueue();renderStudy();">再检查一次</button></p>
        </div>`;
        $('cardActions').style.display = 'none';
    }

    function renderCard() {
        const c = queue[qi];
        if (!c) return;
        revealed = 0;
        $('cardActions').style.display = '';
        const st = stOf(c.id);
        $('cardTitle').textContent = c.chapter || c.noteTitle;
        const sub = [c.noteTitle, c.part, c.subject === 'gs' ? '高等数学' : '线性代数'].filter(Boolean).join(' · ');
        $('cardSub').textContent = sub;
        $('btnStar').classList.toggle('on', !!st.star);
        $('btnStar').textContent = st.star ? '★' : '☆';
        $('btnDone').classList.toggle('on', st.state === 'mastered');
        $('cardBody').innerHTML = mdToHtml(c.md || '');
        const n = applyCloze($('cardBody'), 8);
        if (n === 0) $('cardFoot').innerHTML = '本卡是阅读卡（无可挖空内容）· 用下方按钮标记掌握情况';
        else updateFoot();
        renderMath($('cardBody'));
    }

    function flipCard() { revealAll($('cardBody')); }

    // ---------------- 评分 / 标记 ----------------
    function grade(g) {
        const c = queue[qi];
        if (!c) return;
        const s = stOf(c.id);
        s.last = Date.now();
        if (g === 0) {                                  // 不会：10 分钟后再来
            s.lapses++; s.ease = clamp(s.ease - 0.2, 1.3, 3.0);
            s.interval = 0; s.due = Date.now() + 10 * 60 * 1000; s.state = 'learning';
        } else if (g === 1) {                          // 不熟：缩短间隔
            s.ease = clamp(s.ease - 0.15, 1.3, 3.0);
            s.interval = Math.max(1, Math.round((s.interval || 1) * 1.2));
            s.due = Date.now() + s.interval * DAY; s.state = 'learning';
        } else {                                        // 记得：正常间隔
            s.reps++;
            s.interval = s.reps <= 1 ? 1 : Math.max(1, Math.round((s.interval || 1) * s.ease));
            s.due = Date.now() + s.interval * DAY;
            s.state = s.interval >= 21 ? 'mastered' : 'review';
        }
        if (s.state !== 'new') ST.daily.revDone++; else ST.daily.newDone++;
        ST.daily.done++;
        bumpStreak();
        saveState();
        qi++;
        renderStudy();
    }

    function bumpStreak() {
        const today = dayKey();
        if (ST.streak.last === today) return;
        const y = dayKey(Date.now() - DAY);
        ST.streak.count = (ST.streak.last === y) ? ST.streak.count + 1 : 1;
        ST.streak.last = today;
    }

    function toggleStar(ev) {
        if (ev) ev.stopPropagation();
        const c = queue[qi]; if (!c) return;
        const s = stOf(c.id);
        s.star = !s.star;
        saveState();
        $('btnStar').classList.toggle('on', s.star);
        $('btnStar').textContent = s.star ? '★' : '☆';
        toast(s.star ? '已收藏' : '已取消收藏');
    }

    function markDone(ev) {
        if (ev) ev.stopPropagation();
        const c = queue[qi]; if (!c) return;
        const s = stOf(c.id);
        if (s.state === 'mastered') {
            s.state = 'review'; s.interval = 7; s.due = Date.now() + 7 * DAY;
            toast('已取消「已熟」标记');
        } else {
            s.state = 'mastered'; s.reps = Math.max(s.reps, 5); s.interval = 30; s.due = Date.now() + 30 * DAY;
            toast('已标记为「已熟」，30 天后再复习');
        }
        saveState();
        $('btnDone').classList.toggle('on', s.state === 'mastered');
        qi++; renderStudy();
    }

    // ---------------- 列表 ----------------
    function renderList() {
        const kw = ($('cdSearch').value || '').trim().toLowerCase();
        const sf = $('cdStateFilter').value;
        const stf = $('cdStarFilter').value;
        let rows = visibleCards().filter(c => {
            const s = stOf(c.id);
            if (sf && s.state !== sf) return false;
            if (stf === '1' && !s.star) return false;
            if (kw) {
                const hay = (c.chapter + ' ' + c.noteTitle + ' ' + c.md).toLowerCase();
                if (hay.indexOf(kw) < 0) return false;
            }
            return true;
        });
        const total = rows.length;
        const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
        listPage = clamp(listPage, 1, pages);
        rows = rows.slice((listPage - 1) * PAGE_SIZE, listPage * PAGE_SIZE);
        const stateName = { new: '未学', learning: '不熟中', review: '复习中', mastered: '已熟' };
        $('cdTbody').innerHTML = rows.map(c => {
            const s = stOf(c.id);
            const iv = s.interval === 0 ? '<10 分钟' : (s.interval >= 30 ? Math.round(s.interval / 30) + ' 月' : s.interval + ' 天');
            return `<tr>
                <td class="cd-title-cell"><b>${s.star ? '★ ' : ''}${esc(c.chapter || c.noteTitle)}</b><span>${esc(c.noteTitle)} · ${(c.md || '').length} 字</span></td>
                <td>${c.subject === 'gs' ? '高数' : '线代'}</td>
                <td><span class="cd-state ${s.state}">${stateName[s.state] || s.state}</span></td>
                <td>${iv}</td>
                <td>${s.reps} 次${s.lapses ? ` / 忘 ${s.lapses}` : ''}</td>
                <td>
                    <button class="cd-mini" onclick="reviewNow('${esc(c.id)}')">复习</button>
                    <button class="cd-mini" onclick="resetCard('${esc(c.id)}')">重置</button>
                    <button class="cd-mini" onclick="editCard('${esc(c.id)}')">编辑</button>
                    <button class="cd-mini" onclick="removeCard('${esc(c.id)}')">删除</button>
                </td></tr>`;
        }).join('') || `<tr><td colspan="6" style="text-align:center;color:var(--text-faint);padding:22px">没有匹配的卡片</td></tr>`;
        $('cdPager').innerHTML = `共 ${total} 张 · 第 ${listPage}/${pages} 页
            <button class="cd-mini" onclick="listPage--;renderList()">上一页</button>
            <button class="cd-mini" onclick="listPage++;renderList()">下一页</button>`;
    }

    function reviewNow(id) {
        const i = queue.findIndex(c => c.id === id);
        if (i >= 0) { qi = i; switchView('study'); return; }
        const c = CARDS.find(x => x.id === id);
        if (!c) return;
        queue = [c]; qi = 0; revealed = 0; switchView('study');
    }
    function resetCard(id) {
        delete ST.cards[id]; saveState(); renderList(); toast('已重置进度');
    }
    function removeCard(id) {
        if (!confirm('确定删除这张卡片？（笔记原文不会被删除）')) return;
        const i = CARDS.findIndex(c => c.id === id);
        if (i >= 0) CARDS.splice(i, 1);
        delete ST.cards[id]; saveState(); renderList(); toast('已删除');
    }

    // ---------------- 卡片编辑 ----------------
    function openEditor(id) {
        const c = id ? CARDS.find(x => x.id === id) : null;
        openModal(c ? '编辑卡片' : '新建卡片',
            `<div class="cd-field"><label>科目</label>
                <select id="edSubject"><option value="gs"${c && c.subject === 'gs' ? ' selected' : ''}>高等数学</option>
                <option value="xd"${c && c.subject === 'xd' ? ' selected' : ''}>线性代数</option></select></div>
             <div class="cd-field"><label>标题（章节名）</label><input id="edTitle" value="${c ? esc(c.chapter) : ''}" placeholder="如：中值定理"></div>
             <div class="cd-field"><label>内容（支持 Markdown 与 $LaTeX$）</label>
                <textarea id="edBody" placeholder="支持 Markdown、$公式$、**加粗**">${c ? esc(c.md) : ''}</textarea>
                <div class="cd-hintline">$...$ 与 **...** 会自动成为挖空点（单卡最多 8 个）</div></div>`,
            `<button class="cd-btn" onclick="closeModal()">取消</button>
             <button class="cd-btn primary" onclick="saveCard('${c ? esc(c.id) : ''}')">保存</button>`);
    }
    function editCard(id) { openEditor(id); }

    function saveCard(id) {
        const title = $('edTitle').value.trim();
        const body = $('edBody').value;
        if (!title && !body.trim()) { toast('标题与内容不能都为空'); return; }
        const subj = $('edSubject').value;
        if (id) {
            const c = CARDS.find(x => x.id === id);
            if (c) { c.chapter = title; c.md = body; c.subject = subj; }
        } else {
            const nid = 'custom-' + Date.now();
            CARDS.unshift({ id: nid, subject: subj, noteId: 'custom', noteTitle: '我的卡片', chapter: title || '未命名', part: '', md: body, custom: true });
        }
        saveState(); closeModal(); renderList(); toast('已保存');
    }

    // ---------------- 设置 ----------------
    function openSettings() {
        openModal('设置',
            `<div class="cd-field"><label>每日新卡上限</label>
                <input type="number" id="setNew" min="0" max="200" value="${ST.settings.newPerDay}"></div>
             <div class="cd-field"><label>每日复习上限</label>
                <input type="number" id="setRev" min="0" max="999" value="${ST.settings.revPerDay}"></div>
             <div class="cd-hintline">提示：每日新卡上限影响「未学新卡」的展示量；修改后立即生效。</div>`,
            `<button class="cd-btn" onclick="closeModal()">取消</button>
             <button class="cd-btn primary" onclick="saveSettings()">保存</button>`);
    }
    function saveSettings() {
        ST.settings.newPerDay = clamp(parseInt($('setNew').value, 10) || 0, 0, 200);
        ST.settings.revPerDay = clamp(parseInt($('setRev').value, 10) || 0, 0, 999);
        saveState(); closeModal(); buildQueue(); renderStudy(); toast('设置已保存');
    }

    // ---------------- 导入导出 ----------------
    function exportData() {
        const blob = new Blob([JSON.stringify({ v: 1, cards: CARDS, state: ST }, null, 1)], { type: 'application/json' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `记忆卡备份_${dayKey()}.json`;
        a.click();
        setTimeout(() => URL.revokeObjectURL(a.href), 3000);
        toast('已导出');
    }
    function importData(input) {
        const f = input.files && input.files[0];
        if (!f) return;
        const rd = new FileReader();
        rd.onload = () => {
            try {
                const d = JSON.parse(rd.result);
                if (d.cards) {
                    const map = new Map(CARDS.map(c => [c.id, c]));
                    d.cards.forEach(c => { if (!map.has(c.id)) CARDS.push(c); });
                }
                if (d.state) {
                    for (const id in (d.state.cards || {})) {
                        ST.cards[id] = Object.assign(stOf(id), d.state.cards[id]);
                    }
                    if (d.state.settings) Object.assign(ST.settings, d.state.settings);
                    if (d.state.streak) ST.streak = d.state.streak;
                }
                saveState(); renderList(); toast('导入完成');
            } catch (e) { toast('导入失败：文件格式不正确'); }
        };
        rd.readAsText(f);
        input.value = '';
    }

    // ---------------- 统计 ----------------
    function renderStats() {
        const all = visibleCards();
        const now = Date.now();
        let mastered = 0, learning = 0, review = 0, fresh = 0, star = 0, dueToday = 0;
        all.forEach(c => {
            const s = stOf(c.id);
            if (s.state === 'mastered') mastered++;
            else if (s.state === 'learning') learning++;
            else if (s.state === 'review') review++;
            else fresh++;
            if (s.star) star++;
            if (s.state !== 'new' && s.due <= now) dueToday++;
        });
        $('cdStatGrid').innerHTML = [
            ['卡片总数', all.length, ''], ['已熟', mastered, ''], ['复习中', review, ''],
            ['不熟中', learning, ''], ['未学', fresh, ''], ['今日到期', dueToday, ''],
            ['今日完成', ST.daily.done, ''], ['连续天数', ST.streak.count, ''], ['收藏', star, '']
        ].map(([l, v]) => `<div class="cd-statbox"><b>${v}</b><span>${l}</span></div>`).join('');

        // 未来 7 天
        const days = [];
        for (let i = 0; i < 7; i++) {
            const s0 = now + i * DAY, e0 = s0 + DAY;
            const n = all.filter(c => { const s = stOf(c.id); return s.state !== 'new' && s.due >= s0 && s.due < e0; }).length;
            days.push([i === 0 ? '今天' : (i + 1) + ' 天后', n]);
        }
        const max = Math.max(1, ...days.map(d => d[1]));
        $('cdFuture').innerHTML = days.map(([l, n]) => bar(l, n, max)).join('');

        // 按科目
        const subs = [['高等数学', all.filter(c => c.subject === 'gs').length], ['线性代数', all.filter(c => c.subject === 'xd').length]];
        const mx2 = Math.max(1, ...subs.map(s => s[1]));
        $('cdBySubj').innerHTML = subs.map(([l, n]) => bar(l, n, mx2)).join('');

        // 按笔记（掌握率）
        const byNote = {};
        all.forEach(c => { (byNote[c.noteTitle] = byNote[c.noteTitle] || { t: 0, m: 0 })[c.noteTitle] || 0; byNote[c.noteTitle].t++; if (stOf(c.id).state === 'mastered') byNote[c.noteTitle].m++; });
        const rows = Object.keys(byNote).map(k => [k, Math.round(byNote[k].m / byNote[k].t * 100), byNote[k].t]);
        rows.sort((a, b) => b[1] - a[1]);
        const mx3 = 100;
        $('cdByNote').innerHTML = rows.map(([k, p, t]) => bar(k, p, mx3, p + '% · ' + t + ' 张')).join('');
    }
    function bar(label, val, max, vlabel) {
        return `<div class="cd-bar"><span class="lb" title="${esc(label)}">${esc(label)}</span>
            <span class="tr"><span class="fl" style="width:${clamp(val / max * 100, 0, 100)}%"></span></span>
            <span class="vl">${vlabel != null ? vlabel : val}</span></div>`;
    }

    // ---------------- 模态 ----------------
    function openModal(title, bodyHtml, footHtml) {
        $('cdModalTitle').textContent = title;
        $('cdModalBody').innerHTML = bodyHtml;
        $('cdModalFoot').innerHTML = footHtml;
        $('cdModal').hidden = false;
    }
    function closeModal() { $('cdModal').hidden = true; }

    // ---------------- 视图 / 科目 ----------------
    function switchView(v) {
        view = v;
        ['study', 'list', 'stats'].forEach(x => { $('view' + x[0].toUpperCase() + x.slice(1)).hidden = (x !== v); });
        document.querySelectorAll('.cd-tab').forEach(b => b.classList.toggle('on', b.dataset.view === v));
        if (v === 'list') renderList();
        if (v === 'stats') renderStats();
        if (v === 'study') { buildQueue(); renderStudy(); }
    }
    function setSubject(s, btn) {
        subject = s;
        document.querySelectorAll('#cdSubj .cd-chip').forEach(b => b.classList.toggle('on', b === btn));
        if (view === 'list') renderList();
        if (view === 'stats') renderStats();
        if (view === 'study') { buildQueue(); renderStudy(); }
    }

    // ---------------- 键盘 ----------------
    document.addEventListener('keydown', (e) => {
        if (!$('cdModal').hidden) { if (e.key === 'Escape') closeModal(); return; }
        if (view !== 'study' || !queue.length || qi >= queue.length) return;
        const k = e.key.toLowerCase();
        if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flipCard(); }
        else if (k === '1') grade(0);
        else if (k === '2') grade(1);
        else if (k === '3') grade(2);
        else if (k === 's') toggleStar();
        else if (k === 'd') markDone();
    });
    document.addEventListener('click', (e) => {
        const cl = e.target.closest && e.target.closest('.cd-cloze');
        if (cl && view === 'study' && !cl.classList.contains('revealed')) { revealOne(cl); }
    });

    // ---------------- 启动 ----------------
    async function boot() {
        loadState();
        try {
            const notes = await (await fetch('data/notes.json')).json();
            CARDS = buildCards(Array.isArray(notes) ? notes : (notes.items || []));
        } catch (e) {
            console.error('笔记加载失败', e);
            CARDS = [];
        }
        if (typeof renderDarkSwitch === 'function') renderDarkSwitch();
        buildQueue();
        renderStudy();
    }
    document.addEventListener('DOMContentLoaded', boot);

    // 暴露给行内 onclick
    window.switchView = switchView; window.setSubject = setSubject; window.flipCard = flipCard;
    window.grade = grade; window.toggleStar = toggleStar; window.markDone = markDone;
    window.renderList = renderList; window.reviewNow = reviewNow; window.resetCard = resetCard;
    window.editCard = editCard; window.removeCard = removeCard; window.openEditor = openEditor;
    window.saveCard = saveCard; window.openSettings = openSettings; window.saveSettings = saveSettings;
    window.exportData = exportData; window.importData = importData; window.closeModal = closeModal;
    window.buildQueue = buildQueue; window.renderStudy = renderStudy;
})();
