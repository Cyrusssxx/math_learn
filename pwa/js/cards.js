/* 记忆卡 v2：阅读卡 / 背诵卡分型 + 更稳的拆卡 + 评分前置校验 + 巩固重藏 + 队列动态插队
   - 卡片来源：data/notes.json（高数 gs / 线代 xd），按 ## 章节拆卡，过长按段落/句子二次拆分
   - 分型：可挖空点 ≥2 → 背诵卡（进 SRS 队列）；否则 → 阅读卡（只记阅读进度，不做间隔重复）
   - 交互：点击空位揭示；未全部揭示不允许评分；可「重新隐藏」再记一次；不会卡到期自动插回队列
*/
(function () {
    'use strict';

    const LS_KEY = 'cd_state_v1';
    const DAY = 86400000;
    const MAX_CLOZE = 8;         // 单卡最多挖空数
    const SOFT_LIMIT = 1100;      // 单卡目标字数上限
    const CLOZE_MIN = 2;          // 少于该挖空点视为「阅读卡」

    let CARDS = [];
    let ST = null;
    let view = 'study';
    let subject = '';
    let queue = [];               // 背诵卡队列
    let readQueue = [];           // 阅读卡队列（今日未读）
    let qi = 0;
    let revealed = 0, totalCloze = 0;
    let mode = 'cloze';           // 当前学习模式：cloze | read
    let listPage = 1;
    const PAGE_SIZE = 30;

    // ---------------- 工具 ----------------
    const $ = id => document.getElementById(id);
    const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
    const dayKey = (ts) => new Date(ts || Date.now()).toISOString().slice(0, 10);
    const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    function toast(msg) {
        const t = $('cdToast'); t.textContent = msg; t.hidden = false;
        clearTimeout(toast._t); toast._t = setTimeout(() => { t.hidden = true; }, 1500);
    }

    // ---------------- 状态 ----------------
    function defaultState() {
        return {
            cards: {},
            settings: { newPerDay: 20, revPerDay: 120, readWithQueue: false },
            daily: { date: dayKey(), done: 0, newDone: 0, revDone: 0, readDone: 0 },
            streak: { last: '', count: 0 }
        };
    }
    function loadState() {
        try { ST = JSON.parse(localStorage.getItem(LS_KEY)) || defaultState(); }
        catch (e) { ST = defaultState(); }
        const d = defaultState();
        for (const k in d) if (ST[k] === undefined) ST[k] = d[k];
        for (const k in d.settings) if (ST.settings[k] === undefined) ST.settings[k] = d.settings[k];
        if (ST.daily.date !== dayKey()) ST.daily = { date: dayKey(), done: 0, newDone: 0, revDone: 0, readDone: 0 };
    }
    function saveState() { try { localStorage.setItem(LS_KEY, JSON.stringify(ST)); } catch (e) { } }
    function stOf(id) {
        if (!ST.cards[id]) ST.cards[id] = { ease: 2.5, interval: 0, reps: 0, lapses: 0, due: 0, state: 'new', last: 0, star: false, read: 0 };
        return ST.cards[id];
    }

    // ---------------- 拆卡 ----------------
    function splitSections(md) {
        const secs = []; let cur = null;
        for (const ln of String(md || '').split('\n')) {
            const m = /^##\s+(.*)$/.exec(ln);
            if (m) { if (cur && cur.md.trim()) secs.push(cur); cur = { name: m[1].trim(), md: '' }; }
            else if (cur) cur.md += ln + '\n';
        }
        if (cur && cur.md.trim()) secs.push(cur);
        return secs;
    }

    /** 超长段落拆分：先按空行；单块仍超长则按行硬切（避免无空行时无限递归） */
    function splitLong(md, limit) {
        limit = limit || SOFT_LIMIT;
        md = String(md || '');
        if (md.length <= limit) return [md];
        const out = [];
        let buf = '', len = 0;
        const push = () => { if (buf.trim()) out.push(buf.trim()); buf = ''; len = 0; };
        for (const block of md.split(/\n{2,}/)) {
            if (block.length > limit) {
                push();
                if (block.indexOf('\n') < 0) {
                    // 整段一行（无换行）：按句子边界切
                    const sentences = block.split(/(?<=[。；！？])/);
                    let s = '';
                    for (const sen of sentences) {
                        if (s && s.length + sen.length > limit) { out.push(s); s = sen; }
                        else s += sen;
                    }
                    if (s) out.push(s);
                } else {
                    out.push.apply(out, splitByLines(block, limit));
                }
                continue;
            }
            if (len + block.length > limit) push();
            buf += (buf ? '\n\n' : '') + block; len += block.length + 2;
        }
        push();
        return out.length ? out : [md];
    }

    /** 按行硬切，保证每块不超过 limit（单行本身超长时也断开） */
    function splitByLines(text, limit) {
        const out = []; let cur = '', len = 0;
        for (const ln of String(text).split('\n')) {
            if (len + ln.length > limit && cur) { out.push(cur); cur = ''; len = 0; }
            cur += (cur ? '\n' : '') + ln; len += ln.length + 1;
            if (cur.length > limit) { out.push(cur); cur = ''; len = 0; }
        }
        if (cur) out.push(cur);
        return out;
    }

    function countClozeCandidates(md) {
        const s = String(md || '');
        return (s.match(/\$[^$\n]{2,120}\$/g) || []).length
            + (s.match(/\*\*[^*\n]{2,40}\*\*/g) || []).length
            + (s.match(/`[^`\n]{2,60}`/g) || []).length;
    }

    function buildCards(notes) {
        const cards = [];
        for (const n of notes) {
            for (const sec of splitSections(n.md)) {
                const parts = splitLong(sec.md);
                parts.forEach((p, i) => {
                    if (!p || p.trim().length < 20) return;              // 丢弃空/过短碎片
                    const id = n.id + '::' + sec.name + (parts.length > 1 ? '#' + (i + 1) : '');
                    const cands = countClozeCandidates(p);
                    cards.push({
                        id, subject: n.subject || 'gs',
                        noteId: n.id, noteTitle: n.title || n.name,
                        chapter: sec.name, part: parts.length > 1 ? `(${i + 1}/${parts.length})` : '',
                        md: p, custom: false,
                        kind: cands >= CLOZE_MIN ? 'cloze' : 'read',
                        cands
                    });
                });
            }
        }
        return cards;
    }

    // ---------------- 挖空 ----------------
    const CLOZE_RULES = [
        { re: /\$[^$\n]{2,120}\$/g, strip: s => s.replace(/^\$+|\$+$/g, '') },
        { re: /\*\*[^*\n]{2,40}\*\*/g, strip: s => s.replace(/^\*\*|\*\*$/g, '') },
        { re: /`[^`\n]{2,60}`/g, strip: s => s.replace(/^`|`$/g, '') }
    ];
    function applyCloze(container, max) {
        max = max || MAX_CLOZE;
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
        const nodes = []; let n;
        while ((n = walker.nextNode())) if (n.nodeValue && n.nodeValue.trim()) nodes.push(n);
        let made = 0;
        for (const tn of nodes) {
            if (made >= max) break;
            let s = tn.nodeValue, used = false;
            for (const rule of CLOZE_RULES) {
                if (used || made >= max) break;
                rule.re.lastIndex = 0;
                let m, last = 0, out = '';
                while ((m = rule.re.exec(s)) && made < max) {
                    const inner = rule.strip(m[0]);
                    if (!inner || inner.length < 2) continue;
                    out += s.slice(last, m.index);
                    out += `<span class="cd-cloze" data-c="${esc(inner)}" title="点击显示答案">　　　　</span>`;
                    last = m.index + m[0].length; made++; used = true;
                }
                if (used) { out += s.slice(last); s = out; }
            }
            if (used) {
                const frag = document.createElement('span');
                frag.innerHTML = s;
                tn.parentNode.replaceChild(frag, tn);
            }
        }
        return made;
    }
    function revealOne(el) {
        if (el.classList.contains('revealed')) return;
        const ans = el.getAttribute('data-c') || '';
        el.classList.add('revealed');
        if (ans.indexOf('$') >= 0 && window.katex) {
            try { window.katex.render(ans, el, { displayMode: false }); revealed++; updateFoot(); return; } catch (e) { }
        }
        el.textContent = ans; revealed++; updateFoot();
    }
    function revealAll(root) { (root || document).querySelectorAll('.cd-cloze:not(.revealed)').forEach(revealOne); }
    function hideAll(root) {
        (root || document).querySelectorAll('.cd-cloze.revealed').forEach(el => {
            el.classList.remove('revealed'); el.textContent = '　　　　';
            const ans = el.getAttribute('data-c') || '';
            if (ans.indexOf('$') >= 0 && window.katex) { try { window.katex.render('\\color{transparent}{' + ans + '}', el, { displayMode: false }); return; } catch (e) { } }
        });
        revealed = 0; updateFoot();
    }
    function allRevealed() { return revealed >= totalCloze; }
    function updateFoot() {
        const left = totalCloze - revealed;
        if (mode === 'read') { $('cardFoot').innerHTML = '📖 阅读卡：读懂即可，读完点下方「读完了」'; return; }
        $('cardFoot').innerHTML = left > 0
            ? `还剩 <b>${left}</b> 个空 · 点击填空或按 <b>空格</b> 全部显示`
            : `全部答案已显示 · <a href="javascript:;" id="rehide" onclick="hideAll()">↺ 重新隐藏再记一次</a>，然后评价`;
    }

    // ---------------- 队列 ----------------
    function visibleCards() { return CARDS.filter(c => !subject || c.subject === subject); }
    function pendingRead() { return visibleCards().filter(c => c.kind === 'read' && !stOf(c.id).read); }

    function buildQueue() {
        const now = Date.now();
        const due = [], fresh = [];
        for (const c of visibleCards()) {
            if (c.kind !== 'cloze') continue;
            const s = stOf(c.id);
            if (s.state === 'mastered' && s.due > now) continue;
            if (s.state === 'new') fresh.push(c); else due.push(c);
        }
        due.sort((a, b) => stOf(a.id).due - stOf(b.id).due);
        const st = ST.settings;
        const revLeft = Math.max(0, st.revPerDay - ST.daily.revDone);
        const newLeft = Math.max(0, st.newPerDay - ST.daily.newDone);
        queue = due.slice(0, revLeft).concat(fresh.slice(0, newLeft));
        readQueue = pendingRead().slice(0, 30);
        qi = 0; mode = 'cloze';
    }

    /** 把「已到期的不会卡」插回当前队列（10 分钟后到期的卡能自动重新出现） */
    function injectDueCards() {
        const now = Date.now();
        const inQueue = new Set(queue.map(c => c.id));
        const dueNow = visibleCards().filter(c => {
            if (c.kind !== 'cloze' || inQueue.has(c.id)) return false;
            const s = stOf(c.id);
            return s.state === 'learning' && s.due <= now;
        });
        dueNow.forEach(c => queue.splice(clamp(qi + 1, 0, queue.length), 0, c));
    }

    // ---------------- 学习视图 ----------------
    function renderStudy() {
        const now = Date.now();
        let mastered = 0, learning = 0, freshN = 0, starN = 0, dueN = 0;
        visibleCards().forEach(c => {
            const s = stOf(c.id);
            if (c.kind === 'read') { if (!s.read) freshN += 0; return; }
            if (s.state === 'mastered') mastered++;
            else if (s.state === 'learning') learning++;
            else if (s.state === 'new') freshN++;
            else if (s.due <= now) dueN++;
            if (s.star) starN++;
        });
        const readPending = pendingRead().length;
        $('cdStats').innerHTML = `
            <div class="cd-stat warn"><b>${dueN}</b><span>待复习</span></div>
            <div class="cd-stat"><b>${freshN}</b><span>新卡</span></div>
            <div class="cd-stat"><b>${readPending}</b><span>待阅读</span></div>
            <div class="cd-stat"><b>${ST.daily.done}</b><span>今日完成</span></div>
            <div class="cd-stat ok"><b>${mastered}</b><span>已熟</span></div>
            <div class="cd-stat"><b>${learning}</b><span>不熟中</span></div>
            <div class="cd-stat"><b>${ST.streak.count}</b><span>连续天数</span></div>
            <div class="cd-stat"><b>${starN}</b><span>收藏</span></div>`;
        const totalToday = Math.max(1, dueN + freshN);
        $('cdProgressBar').style.width = clamp(ST.daily.done / totalToday * 100, 0, 100) + '%';
        const totalAll = visibleCards().length;
        $('cdSub').textContent = `${totalAll} 张卡 · 背诵 ${totalAll - visibleCards().filter(c => c.kind === 'read').length} · 阅读 ${visibleCards().filter(c => c.kind === 'read').length}`;

        if (mode === 'read') { renderRead(); return; }
        if (qi >= queue.length) { renderDone(dueN, freshN, readPending); return; }
        renderCard();
    }

    function renderDone(dueN, freshN, readPending) {
        const left = dueN + freshN;
        $('cardWrap').innerHTML = `<div class="cd-done">
            <div class="big">${left > 0 ? '🎉' : '💤'}</div>
            <h2>${left > 0 ? '今日背诵队列已清空' : '今天没有到期的卡片'}</h2>
            <p>${left > 0 ? '剩余卡片可在「卡片」列表里手动复习' : '稍后再来，或读几页笔记'}</p>
            <p style="margin-top:12px">
              <button class="cd-btn" onclick="rebuild()">再检查一次</button>
              ${readPending > 0 ? `<button class="cd-btn primary" onclick="startRead()">📖 去读 ${readPending} 张阅读卡</button>` : ''}
            </p></div>`;
        $('cardActions').style.display = 'none';
    }

    function renderCard() {
        const c = queue[qi];
        if (!c) return;
        mode = 'cloze';
        revealed = 0;
        const st = stOf(c.id);
        $('cardActions').style.display = '';
        $('cardActions').innerHTML = `
            <button class="cd-grade g0" id="g0"><b>🔴 不会</b><span>10 分钟后再来</span></button>
            <button class="cd-grade g1" id="g1"><b>🟡 不熟</b><span>缩短间隔</span></button>
            <button class="cd-grade g2" id="g2"><b>✅ 记得</b><span>正常间隔</span></button>`;
        $('g0').onclick = () => grade(0); $('g1').onclick = () => grade(1); $('g2').onclick = () => grade(2);
        setGradeEnabled(false);
        paintHead(c, st);
        $('cardBody').innerHTML = mdToHtml(c.md || '');
        totalCloze = applyCloze($('cardBody'), MAX_CLOZE);
        if (totalCloze === 0) $('cardFoot').innerHTML = '本卡没有可挖空内容 · 可点右上「✓ 已熟」或下方按钮标记';
        else updateFoot();
        renderMath($('cardBody'));
    }

    function paintHead(c, st) {
        const badge = c.kind === 'read' ? '<span class="cd-badge read">📖 阅读</span>'
            : '<span class="cd-badge memo">🧠 背诵</span>';
        $('cardTitle').innerHTML = badge + ' ' + esc(c.chapter || c.noteTitle);
        $('cardSub').textContent = [c.noteTitle, c.part, c.subject === 'gs' ? '高等数学' : '线性代数'].filter(Boolean).join(' · ');
        $('btnStar').classList.toggle('on', !!st.star);
        $('btnStar').textContent = st.star ? '★' : '☆';
        $('btnDone').classList.toggle('on', st.state === 'mastered');
    }

    function setGradeEnabled(on) {
        ['g0', 'g1', 'g2'].forEach(id => { const b = $(id); if (b) b.disabled = !on; });
    }

    // ---- 阅读模式 ----
    function startRead() { mode = 'read'; qi = 0; renderStudy(); }
    function renderRead() {
        if (qi >= readQueue.length) {
            $('cardWrap').innerHTML = `<div class="cd-done"><div class="big">📚</div>
                <h2>阅读卡已读完</h2><p>今日阅读 ${ST.daily.readDone} 张</p>
                <p style="margin-top:12px"><button class="cd-btn primary" onclick="exitRead()">返回背诵队列</button></p></div>`;
            $('cardActions').style.display = 'none';
            return;
        }
        const c = readQueue[qi];
        const st = stOf(c.id);
        $('cardActions').style.display = '';
        $('cardActions').innerHTML = `
            <button class="cd-grade g2" id="gR" style="grid-column:1/-1"><b>📖 读完了</b><span>记录阅读进度</span></button>`;
        $('gR').onclick = finishRead;
        paintHead(c, st);
        $('cardBody').innerHTML = mdToHtml(c.md || '');
        totalCloze = 0; revealed = 0;
        $('cardFoot').innerHTML = '📖 阅读卡：无需死记，读懂即可；读完点下方「读完了」';
        renderMath($('cardBody'));
    }
    function finishRead() {
        const c = readQueue[qi]; if (!c) return;
        const st = stOf(c.id);
        st.read = Date.now();
        ST.daily.readDone = (ST.daily.readDone || 0) + 1;
        ST.daily.done++;
        saveState();
        qi++; renderStudy();
    }
    function exitRead() { mode = 'cloze'; renderStudy(); }
    function rebuild() { buildQueue(); renderStudy(); }

    // ---------------- 评分 / 标记 ----------------
    function grade(g) {
        const c = queue[qi];
        if (!c) return;
        if (!allRevealed()) { toast('先揭示答案再评价'); return; }   // 前置校验：防止盲评
        const s = stOf(c.id);
        s.last = Date.now();
        if (g === 0) {
            s.lapses++; s.ease = clamp(s.ease - 0.2, 1.3, 3.0);
            s.interval = 0; s.due = Date.now() + 10 * 60 * 1000; s.state = 'learning';
        } else if (g === 1) {
            s.ease = clamp(s.ease - 0.15, 1.3, 3.0);
            s.interval = Math.max(1, Math.round((s.interval || 1) * 1.2));
            s.due = Date.now() + s.interval * DAY; s.state = 'learning';
        } else {
            s.reps++;
            s.interval = s.reps <= 1 ? 1 : Math.max(1, Math.round((s.interval || 1) * s.ease));
            s.due = Date.now() + s.interval * DAY;
            s.state = s.interval >= 21 ? 'mastered' : 'review';
        }
        ST.daily.revDone++; ST.daily.done++;
        bumpStreak(); saveState();
        qi++;
        injectDueCards();          // 不会卡到期后自动插回
        renderStudy();
    }
    function bumpStreak() {
        const today = dayKey();
        if (ST.streak.last === today) return;
        ST.streak.count = (ST.streak.last === dayKey(Date.now() - DAY)) ? ST.streak.count + 1 : 1;
        ST.streak.last = today;
    }
    function toggleStar(ev) {
        if (ev) ev.stopPropagation();
        const c = queue[qi] || readQueue[qi]; if (!c) return;
        const s = stOf(c.id);
        s.star = !s.star; saveState();
        $('btnStar').classList.toggle('on', s.star);
        $('btnStar').textContent = s.star ? '★' : '☆';
        toast(s.star ? '已收藏' : '已取消收藏');
    }
    function markDone(ev) {
        if (ev) ev.stopPropagation();
        const c = queue[qi] || readQueue[qi]; if (!c) return;
        const s = stOf(c.id);
        if (s.state === 'mastered') { s.state = 'review'; s.interval = 7; s.due = Date.now() + 7 * DAY; toast('已取消「已熟」'); }
        else {
            s.state = 'mastered'; s.reps = Math.max(s.reps, 5); s.interval = 30; s.due = Date.now() + 30 * DAY;
            if (c.kind === 'read') { s.read = Date.now(); ST.daily.readDone = (ST.daily.readDone || 0) + 1; }
            toast(c.kind === 'read' ? '已标记读过' : '已标记「已熟」，30 天后再复习');
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
        const rows = visibleCards().filter(c => {
            const s = stOf(c.id);
            if (sf === 'read' && c.kind !== 'read') return false;
            if (sf && sf !== 'read' && c.kind === 'read') return false;
            if (sf && sf !== 'read' && s.state !== sf) return false;
            if (stf === '1' && !s.star) return false;
            if (kw && (c.chapter + ' ' + c.noteTitle + ' ' + c.md).toLowerCase().indexOf(kw) < 0) return false;
            return true;
        });
        const total = rows.length;
        const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
        listPage = clamp(listPage, 1, pages);
        const page = rows.slice((listPage - 1) * PAGE_SIZE, listPage * PAGE_SIZE);
        const stateName = { new: '未学', learning: '不熟中', review: '复习中', mastered: '已熟' };
        $('cdTbody').innerHTML = page.map(c => {
            const s = stOf(c.id);
            const iv = c.kind === 'read'
                ? (s.read ? '已读' : '待读')
                : (s.interval === 0 ? '<10 分钟' : (s.interval >= 30 ? Math.round(s.interval / 30) + ' 月' : s.interval + ' 天'));
            const st = c.kind === 'read'
                ? `<span class="cd-state ${s.read ? 'mastered' : 'new'}">${s.read ? '已读' : '待读'}</span>`
                : `<span class="cd-state ${s.state}">${stateName[s.state] || s.state}</span>`;
            return `<tr>
                <td class="cd-title-cell"><b>${s.star ? '★ ' : ''}${c.kind === 'read' ? '📖 ' : ''}${esc(c.chapter || c.noteTitle)}</b>
                    <span>${esc(c.noteTitle)} · ${(c.md || '').length} 字${c.kind === 'cloze' ? ' · ' + Math.min(c.cands, MAX_CLOZE) + ' 空' : ''}</span></td>
                <td>${c.subject === 'gs' ? '高数' : '线代'}</td>
                <td>${st}</td>
                <td>${iv}</td>
                <td>${c.kind === 'read' ? '—' : (s.reps + ' 次' + (s.lapses ? ` / 忘 ${s.lapses}` : ''))}</td>
                <td>
                    <button class="cd-mini" onclick="reviewNow('${esc(c.id)}')">学习</button>
                    ${c.kind === 'read' ? `<button class="cd-mini" onclick="markRead('${esc(c.id)}')">标已读</button>` : ''}
                    <button class="cd-mini" onclick="resetCard('${esc(c.id)}')">重置</button>
                    <button class="cd-mini" onclick="editCard('${esc(c.id)}')">编辑</button>
                    <button class="cd-mini" onclick="removeCard('${esc(c.id)}')">删除</button>
                </td></tr>`;
        }).join('') || `<tr><td colspan="6" style="text-align:center;color:var(--text-faint);padding:22px">没有匹配的卡片</td></tr>`;
        $('cdPager').innerHTML = `共 ${total} 张 · 第 ${listPage}/${pages} 页
            <button class="cd-mini" onclick="listPage--;renderList()">上一页</button>
            <button class="cd-mini" onclick="listPage++;renderList()">下一页</button>`;
    }
    function markRead(id) { const s = stOf(id); s.read = Date.now(); saveState(); renderList(); toast('已标记读过'); }
    function reviewNow(id) {
        const c = CARDS.find(x => x.id === id);
        if (!c) return;
        if (c.kind === 'read') { readQueue = [c]; qi = 0; mode = 'read'; }
        else { queue = [c]; qi = 0; mode = 'cloze'; }
        switchView('study');
    }
    function resetCard(id) {
        const s = stOf(id);
        s.ease = 2.5; s.interval = 0; s.reps = 0; s.lapses = 0; s.due = 0; s.state = 'new'; s.last = 0; s.read = 0;
        saveState(); renderList(); toast('已重置进度');
    }
    function removeCard(id) {
        if (!confirm('确定删除这张卡片？（笔记原文不会被删除）')) return;
        const i = CARDS.findIndex(c => c.id === id);
        if (i >= 0) CARDS.splice(i, 1);
        delete ST.cards[id]; saveState(); renderList(); toast('已删除');
    }

    // ---------------- 编辑 / 设置 / 导入导出 ----------------
    function openEditor(id) {
        const c = id ? CARDS.find(x => x.id === id) : null;
        openModal(c ? '编辑卡片' : '新建卡片',
            `<div class="cd-field"><label>科目</label>
                <select id="edSubject"><option value="gs"${c && c.subject === 'gs' ? ' selected' : ''}>高等数学</option>
                <option value="xd"${c && c.subject === 'xd' ? ' selected' : ''}>线性代数</option></select></div>
             <div class="cd-field"><label>标题（章节名）</label><input id="edTitle" value="${c ? esc(c.chapter) : ''}" placeholder="如：中值定理"></div>
             <div class="cd-field"><label>类型</label>
                <select id="edKind"><option value="auto"${!c || c.custom ? ' selected' : ''}>自动（按可挖空点判定）</option>
                <option value="cloze"${c && c.kind === 'cloze' ? ' selected' : ''}>背诵卡</option>
                <option value="read"${c && c.kind === 'read' ? ' selected' : ''}>阅读卡</option></select></div>
             <div class="cd-field"><label>内容（支持 Markdown 与 $LaTeX$）</label>
                <textarea id="edBody">${c ? esc(c.md) : ''}</textarea>
                <div class="cd-hintline">可挖空点 ≥ ${CLOZE_MIN} 个判为背诵卡，否则为阅读卡（只记阅读进度）</div></div>`,
            `<button class="cd-btn" onclick="closeModal()">取消</button>
             <button class="cd-btn primary" onclick="saveCard('${c ? esc(c.id) : ''}')">保存</button>`);
    }
    function editCard(id) { openEditor(id); }
    function saveCard(id) {
        const title = $('edTitle').value.trim();
        const body = $('edBody').value;
        if (!title && !body.trim()) { toast('标题与内容不能都为空'); return; }
        const subj = $('edSubject').value;
        const kindSel = $('edKind').value;
        const cands = countClozeCandidates(body);
        const kind = kindSel === 'auto' ? (cands >= CLOZE_MIN ? 'cloze' : 'read') : kindSel;
        if (id) {
            const c = CARDS.find(x => x.id === id);
            if (c) { c.chapter = title; c.md = body; c.subject = subj; c.kind = kind; c.cands = cands; }
        } else {
            CARDS.unshift({
                id: 'custom-' + Date.now(), subject: subj, noteId: 'custom', noteTitle: '我的卡片',
                chapter: title || '未命名', part: '', md: body, custom: true, kind, cands
            });
        }
        saveState(); closeModal(); buildQueue(); renderList(); renderStudy(); toast('已保存');
    }
    function openSettings() {
        openModal('设置',
            `<div class="cd-field"><label>每日新卡上限</label><input type="number" id="setNew" min="0" max="200" value="${ST.settings.newPerDay}"></div>
             <div class="cd-field"><label>每日复习上限</label><input type="number" id="setRev" min="0" max="999" value="${ST.settings.revPerDay}"></div>
             <div class="cd-hintline">阅读卡不占用上述额度；单卡挖空上限 ${MAX_CLOZE} 个，单卡目标长度 ${SOFT_LIMIT} 字以内。</div>`,
            `<button class="cd-btn" onclick="closeModal()">取消</button><button class="cd-btn primary" onclick="saveSettings()">保存</button>`);
    }
    function saveSettings() {
        ST.settings.newPerDay = clamp(parseInt($('setNew').value, 10) || 0, 0, 200);
        ST.settings.revPerDay = clamp(parseInt($('setRev').value, 10) || 0, 0, 999);
        saveState(); closeModal(); rebuild(); toast('设置已保存');
    }
    function exportData() {
        const blob = new Blob([JSON.stringify({ v: 2, cards: CARDS, state: ST }, null, 1)], { type: 'application/json' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob); a.download = `记忆卡备份_${dayKey()}.json`; a.click();
        setTimeout(() => URL.revokeObjectURL(a.href), 3000);
        toast('已导出');
    }
    function importData(input) {
        const f = input.files && input.files[0]; if (!f) return;
        const rd = new FileReader();
        rd.onload = () => {
            try {
                const d = JSON.parse(rd.result);
                if (d.cards) { const map = new Set(CARDS.map(c => c.id)); d.cards.forEach(c => { if (!map.has(c.id)) CARDS.push(c); }); }
                if (d.state) {
                    for (const id in (d.state.cards || {})) ST.cards[id] = Object.assign(stOf(id), d.state.cards[id]);
                    if (d.state.settings) Object.assign(ST.settings, d.state.settings);
                    if (d.state.streak) ST.streak = d.state.streak;
                }
                saveState(); rebuild(); renderList(); toast('导入完成');
            } catch (e) { toast('导入失败：文件格式不正确'); }
        };
        rd.readAsText(f); input.value = '';
    }

    // ---------------- 统计 ----------------
    function renderStats() {
        const all = visibleCards(), now = Date.now();
        let mastered = 0, learning = 0, review = 0, fresh = 0, star = 0, dueToday = 0, readAll = 0, readTodo = 0;
        all.forEach(c => {
            const s = stOf(c.id);
            if (c.kind === 'read') { s.read ? readAll++ : readTodo++; return; }
            if (s.state === 'mastered') mastered++;
            else if (s.state === 'learning') learning++;
            else if (s.state === 'review') review++;
            else fresh++;
            if (s.star) star++;
            if (s.state !== 'new' && s.due <= now) dueToday++;
        });
        $('cdStatGrid').innerHTML = [
            ['卡片总数', all.length], ['背诵卡', all.length - readAll - readTodo], ['阅读卡', readAll + readTodo],
            ['已熟', mastered], ['复习中', review], ['不熟中', learning], ['未学', fresh],
            ['今日到期', dueToday], ['今日完成', ST.daily.done], ['连续天数', ST.streak.count], ['收藏', star], ['待阅读', readTodo]
        ].map(([l, v]) => `<div class="cd-statbox"><b>${v}</b><span>${l}</span></div>`).join('');

        const memo = all.filter(c => c.kind === 'cloze');
        const days = [];
        for (let i = 0; i < 7; i++) {
            const s0 = now + i * DAY, e0 = s0 + DAY;
            days.push([i === 0 ? '今天' : (i + 1) + ' 天后',
                memo.filter(c => { const s = stOf(c.id); return s.state !== 'new' && s.due >= s0 && s.due < e0; }).length]);
        }
        const max = Math.max(1, ...days.map(d => d[1]));
        $('cdFuture').innerHTML = days.map(([l, n]) => bar(l, n, max)).join('');
        const subs = [['高等数学', all.filter(c => c.subject === 'gs').length], ['线性代数', all.filter(c => c.subject === 'xd').length]];
        $('cdBySubj').innerHTML = subs.map(([l, n]) => bar(l, n, Math.max(1, ...subs.map(s => s[1])))).join('');
        const byNote = {};
        all.forEach(c => {
            const k = c.noteTitle;
            byNote[k] = byNote[k] || { t: 0, m: 0 };
            byNote[k].t++;
            if (c.kind === 'read' ? stOf(c.id).read : stOf(c.id).state === 'mastered') byNote[k].m++;
        });
        const rows = Object.keys(byNote).map(k => [k, Math.round(byNote[k].m / byNote[k].t * 100), byNote[k].t]).sort((a, b) => b[1] - a[1]);
        $('cdByNote').innerHTML = rows.map(([k, p, t]) => bar(k, p, 100, p + '% · ' + t + ' 张')).join('');
    }
    function bar(label, val, max, vlabel) {
        return `<div class="cd-bar"><span class="lb" title="${esc(label)}">${esc(label)}</span>
            <span class="tr"><span class="fl" style="width:${clamp(val / max * 100, 0, 100)}%"></span></span>
            <span class="vl">${vlabel != null ? vlabel : val}</span></div>`;
    }

    // ---------------- 模态 / 视图 ----------------
    function openModal(t, b, f) { $('cdModalTitle').textContent = t; $('cdModalBody').innerHTML = b; $('cdModalFoot').innerHTML = f; $('cdModal').hidden = false; }
    function closeModal() { $('cdModal').hidden = true; }
    function switchView(v) {
        view = v;
        ['study', 'list', 'stats'].forEach(x => { $('view' + x[0].toUpperCase() + x.slice(1)).hidden = (x !== v); });
        document.querySelectorAll('.cd-tab').forEach(b => b.classList.toggle('on', b.dataset.view === v));
        if (v === 'list') renderList();
        if (v === 'stats') renderStats();
        if (v === 'study') renderStudy();
    }
    function setSubject(s, btn) {
        subject = s;
        document.querySelectorAll('#cdSubj .cd-chip').forEach(b => b.classList.toggle('on', b === btn));
        if (view === 'list') renderList();
        if (view === 'stats') renderStats();
        if (view === 'study') { buildQueue(); renderStudy(); }
    }

    // ---------------- 键盘 / 点击 ----------------
    document.addEventListener('keydown', (e) => {
        if (!$('cdModal').hidden) { if (e.key === 'Escape') closeModal(); return; }
        if (view !== 'study') return;
        if (mode === 'read') { if (e.key === 'Enter') finishRead(); return; }
        if (!queue.length || qi >= queue.length) return;
        const k = e.key.toLowerCase();
        if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); if (allRevealed() && e.key === 'Enter') grade(2); else revealAll($('cardBody')); }
        else if (k === '1') grade(0);
        else if (k === '2') grade(1);
        else if (k === '3') grade(2);
        else if (k === 's') toggleStar();
        else if (k === 'd') markDone();
    });
    document.addEventListener('click', (e) => {
        const cl = e.target.closest && e.target.closest('.cd-cloze');
        if (cl && view === 'study' && !cl.classList.contains('revealed')) revealOne(cl);
        if (cl && view === 'study' && cl.classList.contains('revealed')) setGradeEnabled(true);
    });

    // ---------------- 启动 ----------------
    async function boot() {
        loadState();
        try {
            const notes = await (await fetch('data/notes.json')).json();
            CARDS = buildCards(Array.isArray(notes) ? notes : (notes.items || []));
        } catch (e) { console.error('笔记加载失败', e); CARDS = []; }
        if (typeof renderDarkSwitch === 'function') renderDarkSwitch();
        buildQueue(); renderStudy();
    }
    document.addEventListener('DOMContentLoaded', boot);

    Object.assign(window, {
        switchView, setSubject, grade, toggleStar, markDone, renderList, reviewNow, markRead,
        resetCard, removeCard, openEditor, editCard, saveCard, openSettings, saveSettings,
        exportData, importData, closeModal, renderStudy, rebuild, startRead, exitRead,
        finishRead, hideAll, revealAll,
        __debug: () => ({
            total: CARDS.length,
            memo: CARDS.filter(c => c.kind === 'cloze').length,
            read: CARDS.filter(c => c.kind === 'read').length,
            maxLen: CARDS.reduce((m, c) => Math.max(m, (c.md || '').length), 0),
            minLen: CARDS.reduce((m, c) => Math.min(m, (c.md || '').length), 1e9),
            queueKinds: Array.from(new Set(queue.map(c => c.kind))),
            queueLen: queue.length, readQueueLen: readQueue.length,
            revealed, totalCloze, mode
        })
    });
})();
