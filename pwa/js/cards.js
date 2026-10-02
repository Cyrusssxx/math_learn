/* 记忆卡 v2：阅读卡 / 背诵卡分型 + 更稳的拆卡 + 评分前置校验 + 巩固重藏 + 队列动态插队
   - 卡片来源：data/notes.json（高数 gs / 线代 xd），按 ## 章节拆卡，过长按段落/句子二次拆分
   - 分型：可挖空点 ≥2 → 背诵卡（进 SRS 队列）；否则 → 阅读卡（只记阅读进度，不做间隔重复）
   - 交互：点击空位揭示；未全部揭示不允许评分；可「重新隐藏」再记一次；不会卡到期自动插回队列
*/
(function () {
    'use strict';

    const LS_KEY = 'cd_state_v1';
    const DAY = 86400000;
    const MAX_CLOZE = 12;        // 单卡挖空数硬上限（实际值由设置 clozePerCard 决定）
    const DEF_CLOZE = 8;         // 默认单卡挖空数
    const SOFT_LIMIT = 1100;      // 单卡目标字数上限
    const CLOZE_MIN = 2;          // 少于该挖空点视为「阅读卡」

    function clozeLimit() {
        const v = ST && ST.settings ? ST.settings.clozePerCard : DEF_CLOZE;
        return clamp(parseInt(v, 10) || DEF_CLOZE, 2, MAX_CLOZE);
    }

    let CARDS = [];
    let ST = null;
    let view = 'study';
    let subject = '';
    let queue = [];               // 背诵卡队列
    let readQueue = [];           // 阅读卡队列（今日未读）
    let CARD_HTML = '';           // 卡片骨架快照（完成态会整体替换 cardWrap，需要能还原）
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
            settings: { newPerDay: 20, revPerDay: 120, clozePerCard: DEF_CLOZE },
            daily: { date: dayKey(), done: 0, newDone: 0, revDone: 0, readDone: 0 },
            streak: { last: '', count: 0 },
            custom: [],      // 自建卡片（持久化，刷新不丢）
            over: {},        // 内置卡被编辑后的覆盖：id → {chapter, md, subject, kind, cands}
            hidden: {},      // 被删除的内置卡 id
            history: {}      // date → {done,newDone,revDone,readDone}，用于趋势统计
        };
    }
    function loadState() {
        try { ST = JSON.parse(localStorage.getItem(LS_KEY)) || defaultState(); }
        catch (e) { ST = defaultState(); }
        const d = defaultState();
        for (const k in d) if (ST[k] === undefined || ST[k] === null) ST[k] = d[k];
        if (typeof ST.custom !== 'object' || !Array.isArray(ST.custom)) ST.custom = [];
        ['over', 'hidden', 'history'].forEach(k => { if (typeof ST[k] !== 'object' || Array.isArray(ST[k])) ST[k] = {}; });
        for (const k in d.settings) if (ST.settings[k] === undefined) ST.settings[k] = d.settings[k];
        delete ST.settings.readWithQueue;   // 旧版本未启用的死配置
        if (ST.daily.date !== dayKey()) ST.daily = { date: dayKey(), done: 0, newDone: 0, revDone: 0, readDone: 0 };
    }
    /** 把当天计数落入历史（保留 120 天），供统计页画趋势 */
    function bumpHistory() {
        if (!ST.history) ST.history = {};
        const d = dayKey();
        ST.history[d] = {
            done: ST.daily.done || 0, newDone: ST.daily.newDone || 0,
            revDone: ST.daily.revDone || 0, readDone: ST.daily.readDone || 0
        };
        const keys = Object.keys(ST.history).sort();
        while (keys.length > 120) delete ST.history[keys.shift()];
    }
    function saveState() {
        try { bumpHistory(); localStorage.setItem(LS_KEY, JSON.stringify(ST)); } catch (e) { }
    }
    /** 只读状态：不往 ST.cards 里塞默认条目。
     *  渲染/统计会把全部 350+ 张卡都过一遍，若用 stOf 则一次性实例化全部默认状态，
     *  下次 saveState 就把 ~40KB 垃圾写进 localStorage，且每次操作都要重写全量。
     *  ⚠️ 默认对象必须冻结：本文件是严格模式，一旦有写路径误用 peekOf 会立刻抛错暴露，
     *  而不是静默污染共享对象（那会让「所有未学卡瞬间变成已熟」） */
    const DEF_CARD_STATE = Object.freeze({
        ease: 2.5, interval: 0, reps: 0, lapses: 0, due: 0, state: 'new', last: 0, star: false, read: 0
    });
    function peekOf(id) { return ST.cards[id] || DEF_CARD_STATE; }
    /** 可写状态：仅在真正要改进度时调用（评分/收藏/已熟/重置） */
    function stOf(id) {
        if (!ST.cards[id]) ST.cards[id] = Object.assign({}, DEF_CARD_STATE);
        return ST.cards[id];
    }

    // ---------------- 拆卡 ----------------
    /** 按 `##` 章节拆分。首个 ## 之前的内容（导读/大纲）单独作为「概述」卡返回，
     *  否则这部分内容会被整篇丢弃（实测 32 篇共 596 字）。kind 由 cands 决定，多半是阅读卡，不占 SRS 额度 */
    function splitSections(md) {
        const secs = [];
        const lines = String(md || '').split('\n');
        let cur = null, pre = [];
        for (const ln of lines) {
            const m = /^##\s+(.*)$/.exec(ln);
            if (m) {
                if (cur && cur.md.trim()) secs.push(cur);
                else if (pre.join('\n').trim()) secs.push({ name: '概述', md: pre.join('\n') + '\n', pre: true });
                pre = [];
                cur = { name: m[1].trim(), md: '' };
            } else if (cur) cur.md += ln + '\n';
            else pre.push(ln);
        }
        if (cur && cur.md.trim()) secs.push(cur);
        else if (pre.join('\n').trim()) secs.push({ name: '概述', md: pre.join('\n') + '\n', pre: true });
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

    /** 加粗候选的长度区间 —— countClozeCandidates（判定分型）与 collectCands（实际挖空）必须共用，
     *  否则会出现「判为背诵卡却挖不出空」的退化卡。两处上限不一致时实测有 10 张卡计数偏差。 */
    const BOLD_MIN = 2, BOLD_MAX = 60;

    function countClozeCandidates(md) {
        const s = String(md || '');
        return (s.match(/\$[^$\n]{1,120}\$/g) || []).length
            + (s.match(new RegExp('\\*\\*[^*\\n]{' + BOLD_MIN + ',' + BOLD_MAX + '}\\*\\*', 'g')) || []).length
            + (s.match(/`[^`\n]{1,60}`/g) || []).length;
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

    /** 应用本地改动：隐藏已删卡 → 覆盖被编辑的卡 → 追加自建卡（都在笔记拆卡之后） */
    function applyStoredCards() {
        CARDS = CARDS.filter(c => !ST.hidden[c.id]).map(c => {
            const o = ST.over[c.id];
            return o ? Object.assign({}, c, o) : c;
        });
        (ST.custom || []).forEach(c => {
            if (c && c.id && !CARDS.some(x => x.id === c.id)) CARDS.unshift(Object.assign({ custom: true }, c));
        });
    }

    // ---------------- 挖空 ----------------
    const CL_PLACE = '　　';                                  // 未揭示时的占位宽度
    /* 文本节点级候选：kind m=行内公式（揭示时用 KaTeX 渲染）/ c=行内代码（纯文本揭示）
       加粗 **…** 在 mdToHtml 里已变成 <strong> 元素，走元素级候选（kind b）
       注意公式下限是 {1,}：$x$/$n$ 这类单字符公式必须参与配对，否则 $ 配对错位、
       会把两个公式之间的中文段错配成「伪公式」 */
    const CLOZE_RULES = [
        { kind: 'm', re: /\$[^$\n]{1,120}\$/g, strip: s => s.replace(/^\$+|\$+$/g, '') },
        { kind: 'c', re: /`[^`\n]{1,60}`/g, strip: s => s.replace(/^`+|`+$/g, '') }
    ];

    function makeCloze(inner, kind) {
        const sp = document.createElement('span');
        sp.className = 'cd-cloze';
        sp.setAttribute('data-c', inner);
        sp.setAttribute('data-k', kind);
        sp.title = '点击显示答案';
        sp.textContent = CL_PLACE;
        return sp;
    }

    /** 判定节点是否位于 strong / 已有挖空内（不再作为候选） */
    function insideSkip(n, container) {
        let p = n.parentNode;
        while (p && p !== container) {
            if (p.nodeType === 1 && (p.classList.contains('cd-cloze') || p.tagName === 'STRONG')) return true;
            p = p.parentNode;
        }
        return false;
    }

    /** 收集容器内所有候选：{kind, inner, el?|node+index+len, order} */
    function collectCands(container) {
        const list = [];
        // 元素级：加粗
        Array.from(container.querySelectorAll('strong')).forEach((el, i) => {
            const t = (el.textContent || '').trim();
            if (t.length >= BOLD_MIN && t.length <= BOLD_MAX) list.push({ kind: 'b', el, inner: t, order: -1e6 + i });
        });
        // 文本节点级：行内公式 / 代码
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
        let n, idx = 0;
        while ((n = walker.nextNode())) {
            const s = n.nodeValue;
            if (!s || !s.trim() || insideSkip(n, container)) continue;
            const hits = [];
            for (const rule of CLOZE_RULES) {
                rule.re.lastIndex = 0;
                let m;
                while ((m = rule.re.exec(s))) {
                    const inner = rule.strip(m[0]);
                    if (!inner || inner.length < 2) continue;
                    hits.push({ kind: rule.kind, index: m.index, len: m[0].length, inner });
                }
            }
            if (!hits.length) continue;
            hits.sort((a, b) => a.index - b.index);
            const clean = []; let lastEnd = -1;
            for (const h of hits) if (h.index >= lastEnd) { clean.push(h); lastEnd = h.index + h.len; }
            clean.forEach((h, j) => { h.node = n; h.order = idx * 1000 + j; });
            idx++;
            list.push.apply(list, clean);
        }
        return list;
    }

    /** 组内均匀采样 k 个（保留首尾、等距取点），避免「只挖到卡前半段」 */
    function stridePick(arr, k) {
        if (k <= 0) return [];
        if (arr.length <= k) return arr.slice();
        if (k === 1) return [arr[0]];
        const idxs = new Set();
        for (let i = 0; i < k; i++) idxs.add(Math.round(i * (arr.length - 1) / (k - 1)));
        let j = 0;
        while (idxs.size < k && j < arr.length) { idxs.add(j); j++; }
        return Array.from(idxs).sort((a, b) => a - b).map(i => arr[i]);
    }

    /** 在已渲染的 HTML 上挖空，返回实际挖出的空数 */
    function applyCloze(container, max) {
        max = clamp(max || clozeLimit(), 1, MAX_CLOZE);
        const cands = collectCands(container);
        if (!cands.length) return 0;
        const g = { m: [], b: [], c: [] };
        cands.forEach(c => g[c.kind].push(c));
        Object.keys(g).forEach(k => g[k].sort((a, b) => a.order - b.order));
        // 公式按信息量分两档：长公式（≥3 字符）优先，单字符（$x$/$n$）只作补位
        const mL = g.m.filter(c => c.inner.length >= 3);
        const mS = g.m.filter(c => c.inner.length < 3);
        const bCap = Math.min(g.b.length, 2);                       // 加粗最多补 2 个名额
        const mQ = Math.min(mL.length, Math.max(0, max - bCap));
        const bQ = Math.min(g.b.length, max - mQ);
        const sQ = Math.min(mS.length, Math.max(0, max - mQ - bQ));
        const cQ = Math.min(g.c.length, Math.max(0, max - mQ - bQ - sQ));
        const picked = stridePick(mL, mQ)
            .concat(stridePick(g.b, bQ), stridePick(mS, sQ), stridePick(g.c, cQ));
        // 元素级替换优先（其后其内部文本节点已离开文档，不再被处理）
        picked.filter(p => p.el).forEach(p => p.el.parentNode.replaceChild(makeCloze(p.inner, 'b'), p.el));
        // 文本节点级：同一节点内的多个候选一次性替换
        const byNode = new Map();
        picked.filter(p => p.node).forEach(p => {
            if (!p.node.parentNode || !container.contains(p.node)) return;
            if (!byNode.has(p.node)) byNode.set(p.node, []);
            byNode.get(p.node).push(p);
        });
        byNode.forEach((hs, node) => {
            const s = node.nodeValue;
            let html = '', last = 0;
            hs.sort((a, b) => a.index - b.index).forEach(h => {
                if (h.index < last) return;
                html += esc(s.slice(last, h.index)) +
                    `<span class="cd-cloze" data-c="${esc(h.inner)}" data-k="${h.kind}" title="点击显示答案">${CL_PLACE}</span>`;
                last = h.index + h.len;
            });
            html += esc(s.slice(last));
            const frag = document.createElement('span');
            frag.innerHTML = html;
            node.parentNode.replaceChild(frag, node);
        });
        return picked.length;
    }

    /** 答案是否适合交给 KaTeX：含中文且没写 \text{} 的「伪公式」降级为纯文本 */
    function texSafe(s) {
        return !/[\u4e00-\u9fa5]/.test(s) || /\\text\{/.test(s);
    }

    function revealOne(el) {
        if (el.classList.contains('revealed')) return;
        const ans = el.getAttribute('data-c') || '';
        const k = el.getAttribute('data-k') || 'c';
        el.classList.add('revealed');
        if (k === 'm' && window.katex && texSafe(ans)) {
            try {
                window.katex.render(ans, el, { displayMode: false, throwOnError: false });
                revealed++; refreshReady(); return;
            } catch (e) { /* 降级为纯文本 */ }
        }
        if (k === 'b') el.innerHTML = '<b>' + esc(ans) + '</b>';
        else el.textContent = ans;
        revealed++; refreshReady();
    }
    function revealAll(root) { (root || document).querySelectorAll('.cd-cloze:not(.revealed)').forEach(revealOne); refreshReady(); }
    function hideAll(root) {
        (root || document).querySelectorAll('.cd-cloze.revealed').forEach(el => {
            const ans = el.getAttribute('data-c') || '';
            const k = el.getAttribute('data-k') || 'c';
            el.classList.remove('revealed');
            el.textContent = CL_PLACE;
            if (k === 'm' && window.katex && texSafe(ans)) {
                // 透明渲染同一公式，保证重新隐藏后占位宽度不塌陷
                try { window.katex.render('\\color{transparent}{' + ans + '}', el, { displayMode: false, throwOnError: false }); } catch (e) { }
            }
        });
        revealed = 0; refreshReady();
    }
    function allRevealed() { return revealed >= totalCloze; }
    /** 全部揭示才点亮评分区（仍可点击，未就绪时由 grade() 给出提示） */
    function refreshReady() {
        const a = $('cardActions');
        if (a) a.classList.toggle('not-ready', totalCloze > 0 && !allRevealed());
        updateFoot();
    }
    function updateFoot() {
        const foot = $('cardFoot');
        if (!foot) return;            // 完成态/阅读完成态下卡片区被整体替换，页脚可能不存在
        if (mode === 'read') { foot.innerHTML = '📖 阅读卡：读懂即可，读完点下方「读完了」'; return; }
        if (totalCloze === 0) { foot.innerHTML = '本卡没有可挖空内容 · 可点右上「✓ 已熟」或直接评级'; return; }
        const left = totalCloze - revealed;
        foot.innerHTML = left > 0
            ? `还剩 <b>${left}</b> 个空 · 点击填空或按 <b>空格</b> 全部显示`
            : `全部答案已显示 · <a href="javascript:;" id="rehide" onclick="hideAll()">↺ 重新隐藏再记一次</a>，然后评价`;
    }

    // ---------------- 队列 ----------------
    let queueFilter = '';        // '' 全部 | hard 不会 | learning 不熟 | star 收藏
    function visibleCards() { return CARDS.filter(c => !subject || c.subject === subject); }
    function matchFilter(c) {
        if (!queueFilter) return true;
        const s = peekOf(c.id);
        if (queueFilter === 'hard') return s.lapses > 0;
        if (queueFilter === 'learning') return s.state === 'learning';
        if (queueFilter === 'star') return !!s.star;
        return true;
    }
    function poolCards() { return visibleCards().filter(matchFilter); }
    function pendingRead() { return poolCards().filter(c => c.kind === 'read' && !peekOf(c.id).read); }
    function setQueueFilter(f, btn) {
        queueFilter = f || '';
        document.querySelectorAll('#cdFilters .cd-chip').forEach(b => b.classList.toggle('on', (b.dataset.f || '') === queueFilter));
        buildQueue();
        if (view === 'study') renderStudy();     // 筛选只作用于学习队列，列表/统计页各有自己的筛选器
    }

    function buildQueue() {
        const now = Date.now();
        const due = [], fresh = [];
        for (const c of poolCards()) {
            if (c.kind !== 'cloze') continue;
            const s = peekOf(c.id);
            if (s.state === 'mastered' && s.due > now) continue;
            if (s.state === 'new') fresh.push(c); else due.push(c);
        }
        due.sort((a, b) => peekOf(a.id).due - peekOf(b.id).due);
        const st = ST.settings;
        const revLeft = Math.max(0, st.revPerDay - ST.daily.revDone);
        const newLeft = Math.max(0, st.newPerDay - ST.daily.newDone);
        // 筛选态下（不会/不熟/收藏）不受每日额度限制：用户主动想练就该给
        queue = queueFilter
            ? due.concat(fresh)
            : due.slice(0, revLeft).concat(fresh.slice(0, newLeft));
        readQueue = pendingRead().slice(0, 30);
        qi = 0; mode = 'cloze';
    }

    /** 把「已到期的不会卡」插回当前队列（10 分钟后到期的卡能自动重新出现） */
    function injectDueCards() {
        const now = Date.now();
        const inQueue = new Set(queue.map(c => c.id));
        const dueNow = poolCards().filter(c => {
            if (c.kind !== 'cloze' || inQueue.has(c.id)) return false;
            const s = peekOf(c.id);
            return s.state === 'learning' && s.due <= now;
        });
        dueNow.forEach(c => queue.splice(clamp(qi + 1, 0, queue.length), 0, c));
    }

    // ---------------- 学习视图 ----------------
    function renderStudy() {
        const now = Date.now();
        let mastered = 0, learning = 0, freshN = 0, starN = 0, dueN = 0;
        visibleCards().forEach(c => {
            const s = peekOf(c.id);
            if (s.star) starN++;                       // 阅读卡的收藏也要计入
            if (c.kind === 'read') return;
            if (s.state === 'mastered') mastered++;
            else if (s.state === 'learning') learning++;
            else if (s.state === 'new') freshN++;
            if (s.state !== 'new' && s.due <= now) dueN++;   // 复习中 + 不熟中到期都算「待复习」
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
        const todayTarget = Math.max(1, ST.daily.done + queue.length);
        $('cdProgressBar').style.width = clamp(ST.daily.done / todayTarget * 100, 0, 100) + '%';
        const all = visibleCards(), readN = all.filter(c => c.kind === 'read').length;
        const fname = { hard: ' · 只看不会', learning: ' · 只看不熟', star: ' · 只看收藏' }[queueFilter] || '';
        $('cdSub').textContent = `${all.length} 张卡 · 背诵 ${all.length - readN} · 阅读 ${readN}${fname}`;

        if (mode === 'read') { renderRead(); return; }
        if (qi >= queue.length) { renderDone(dueN, freshN, readPending); return; }
        renderCard();
    }

    function renderDone(dueN, freshN, readPending) {
        if (queueFilter) {
            const nm = { hard: '🔴 不会', learning: '🟡 不熟', star: '★ 收藏' }[queueFilter];
            $('cardWrap').innerHTML = `<div class="cd-done">
                <div class="big">✅</div>
                <h2>「${nm}」筛选下的卡片已过完</h2>
                <p>当前没有符合该筛选的卡片</p>
                <p style="margin-top:12px">
                  <button class="cd-btn primary" onclick="setQueueFilter('', this)">回到全部卡片</button>
                  <button class="cd-btn" onclick="rebuild()">再检查一次</button>
                </p></div>`;
            $('cardActions').style.display = 'none';
            return;
        }
        const left = dueN + freshN;
        $('cardWrap').innerHTML = `<div class="cd-done">
            <div class="big">${left > 0 ? '🎉' : '💤'}</div>
            <h2>${left > 0 ? '今日背诵队列已清空' : '今天没有到期的卡片'}</h2>
            <p>${left > 0 ? '剩余卡片可在「卡片」列表里手动复习，或明天再来' : '稍后再来，或读几页笔记'}</p>
            <p style="margin-top:12px">
              <button class="cd-btn" onclick="rebuild()">再检查一次</button>
              ${readPending > 0 ? `<button class="cd-btn primary" onclick="startRead()">📖 去读 ${readPending} 张阅读卡</button>` : ''}
            </p></div>`;
        $('cardActions').style.display = 'none';
    }

    function renderCard() {
        const c = queue[qi];
        if (!c) return;
        ensureCard();
        mode = 'cloze';
        revealed = 0;
        const st = peekOf(c.id);
        $('cardActions').style.display = '';
        $('cardActions').innerHTML = `
            <button class="cd-grade g0" id="g0"><b>🔴 不会</b><span>10 分钟后再来</span></button>
            <button class="cd-grade g1" id="g1"><b>🟡 不熟</b><span>缩短间隔</span></button>
            <button class="cd-grade g2" id="g2"><b>✅ 记得</b><span>正常间隔</span></button>`;
        $('g0').onclick = () => grade(0); $('g1').onclick = () => grade(1); $('g2').onclick = () => grade(2);
        paintHead(c, st);
        $('cardBody').innerHTML = mdToHtml(c.md || '');
        totalCloze = applyCloze($('cardBody'), clozeLimit());
        renderMath($('cardBody'));
        refreshReady();
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

    /* 评分就绪态改由 refreshReady() 用 .not-ready 类控制：按钮不禁用，点击时给「还剩 N 个空」提示 */
    // ---- 阅读模式 ----
    function startRead() { mode = 'read'; qi = 0; renderStudy(); }
    /** 完成态会把 cardWrap 整体替换掉，回到学习态前先还原卡片骨架 */
    function ensureCard() { if (!$('cardBody') && CARD_HTML) $('cardWrap').innerHTML = CARD_HTML; }
    function renderRead() {
        if (qi >= readQueue.length) {
            $('cardWrap').innerHTML = `<div class="cd-done"><div class="big">📚</div>
                <h2>阅读卡已读完</h2><p>今日阅读 ${ST.daily.readDone} 张</p>
                <p style="margin-top:12px"><button class="cd-btn primary" onclick="exitRead()">返回背诵队列</button></p></div>`;
            $('cardActions').style.display = 'none';
            return;
        }
        const c = readQueue[qi];
        const st = peekOf(c.id);
        ensureCard();
        $('cardActions').style.display = '';
        $('cardActions').innerHTML = `
            <button class="cd-grade g2" id="gR" style="grid-column:1/-1"><b>📖 读完了</b><span>记录阅读进度</span></button>`;
        $('gR').onclick = finishRead;
        paintHead(c, st);
        $('cardBody').innerHTML = mdToHtml(c.md || '');
        totalCloze = 0; revealed = 0;
        renderMath($('cardBody'));
        $('cardActions').classList.remove('not-ready');
        updateFoot();
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
        if (!allRevealed()) {   // 前置校验：防止盲评
            toast(`还剩 ${totalCloze - revealed} 个空没揭示 · 先点开答案再评价`);
            return;
        }
        const s = stOf(c.id);
        const wasNew = s.state === 'new';
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
        // 新卡与复习卡分开计数，每日新卡上限才真正生效
        if (wasNew) ST.daily.newDone++; else ST.daily.revDone++;
        ST.daily.done++;
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
    /** 当前正在显示的卡：阅读模式与背诵模式各用各的队列，
     *  写成 queue[qi] || readQueue[qi] 会在阅读模式下误取背诵卡（qi 在两个队列里都存在） */
    function currentCard() { return mode === 'read' ? readQueue[qi] : queue[qi]; }

    function toggleStar(ev) {
        if (ev) ev.stopPropagation();
        const c = currentCard(); if (!c) return;
        const s = stOf(c.id);
        s.star = !s.star; saveState();
        $('btnStar').classList.toggle('on', s.star);
        $('btnStar').textContent = s.star ? '★' : '☆';
        toast(s.star ? '已收藏' : '已取消收藏');
    }
    function markDone(ev) {
        if (ev) ev.stopPropagation();
        const c = currentCard(); if (!c) return;
        const s = stOf(c.id);
        if (s.state === 'mastered') { s.state = 'review'; s.interval = 7; s.due = Date.now() + 7 * DAY; toast('已取消「已熟」'); }
        else {
            s.state = 'mastered'; s.reps = Math.max(s.reps, 5); s.interval = 30; s.due = Date.now() + 30 * DAY;
            if (c.kind === 'read' && !s.read) { s.read = Date.now(); ST.daily.readDone = (ST.daily.readDone || 0) + 1; }
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
            const s = peekOf(c.id);
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
            const s = peekOf(c.id);
            const iv = c.kind === 'read'
                ? (s.read ? '已读' : '待读')
                : (s.interval === 0 ? '<10 分钟' : (s.interval >= 30 ? Math.round(s.interval / 30) + ' 月' : s.interval + ' 天'));
            const st = c.kind === 'read'
                ? `<span class="cd-state ${s.read ? 'mastered' : 'new'}">${s.read ? '已读' : '待读'}</span>`
                : `<span class="cd-state ${s.state}">${stateName[s.state] || s.state}</span>`;
            return `<tr>
                <td class="cd-title-cell"><b>${s.star ? '★ ' : ''}${c.kind === 'read' ? '📖 ' : ''}${c.custom ? '✎ ' : ''}${esc(c.chapter || c.noteTitle)}</b>
                    <span>${esc(c.noteTitle)} · ${(c.md || '').length} 字${c.kind === 'cloze' ? ' · ' + Math.min(c.cands, clozeLimit()) + ' 空' : ''}</span></td>
                <td>${c.subject === 'gs' ? '高数' : '线代'}</td>
                <td>${st}</td>
                <td>${iv}</td>
                <td>${c.kind === 'read' ? '—' : (s.reps + ' 次' + (s.lapses ? ` / 忘 ${s.lapses}` : ''))}</td>
                <td>
                    <button class="cd-mini" data-act="review" data-id="${esc(c.id)}">学习</button>
                    ${c.kind === 'read' ? `<button class="cd-mini" data-act="markread" data-id="${esc(c.id)}">标已读</button>` : ''}
                    <button class="cd-mini" data-act="reset" data-id="${esc(c.id)}">重置</button>
                    <button class="cd-mini" data-act="edit" data-id="${esc(c.id)}">编辑</button>
                    <button class="cd-mini" data-act="remove" data-id="${esc(c.id)}">删除</button>
                </td></tr>`;
        }).join('') || `<tr><td colspan="6" style="text-align:center;color:var(--text-faint);padding:22px">没有匹配的卡片</td></tr>`;
        $('cdPager').innerHTML = `共 ${total} 张 · 第 ${listPage}/${pages} 页
            <button class="cd-mini" onclick="listPage--;renderList()">上一页</button>
            <button class="cd-mini" onclick="listPage++;renderList()">下一页</button>`;
    }
    /* 列表按钮走 data-act/data-id + 事件委托，不再把卡片 id 拼进 onclick='…' 字符串：
       章节名来自笔记正文，一旦出现单引号 / 反斜杠就会让属性提前闭合、按钮彻底失效 */
    const LIST_ACTS = {
        review: id => reviewNow(id),
        markread: id => markRead(id),
        reset: id => resetCard(id),
        edit: id => editCard(id),
        remove: id => removeCard(id)
    };
    document.addEventListener('click', (e) => {
        const btn = e.target.closest && e.target.closest('[data-act]');
        if (!btn) return;
        const fn = LIST_ACTS[btn.dataset.act];
        if (fn && btn.dataset.id != null) { e.preventDefault(); fn(btn.dataset.id); }
    });
    function markRead(id) {
        const s = stOf(id);
        if (!s.read) { ST.daily.readDone = (ST.daily.readDone || 0) + 1; ST.daily.done++; }
        s.read = Date.now(); saveState(); afterListChange(); toast('已标记读过');
    }
    /** 列表改动后统一收尾：列表必刷；学习视图也要重建队列，
     *  否则被删/被重置的卡仍留在 queue 里（幽灵卡：评完会写回一份被删状态） */
    function afterListChange() {
        renderList();
        buildQueue();
        if (view === 'study') renderStudy();
        if (view === 'stats') renderStats();
    }
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
        s.star = false;
        saveState(); afterListChange(); toast('已重置进度');
    }
    function removeCard(id) {
        if (!confirm('确定删除这张卡片？（笔记原文不会被删除；内置卡删除后不会再生成）')) return;
        const i = CARDS.findIndex(c => c.id === id);
        const c = i >= 0 ? CARDS[i] : null;
        if (i >= 0) CARDS.splice(i, 1);
        if (c && c.custom) ST.custom = (ST.custom || []).filter(x => x.id !== id);
        else { ST.hidden[id] = 1; delete ST.over[id]; }
        delete ST.cards[id]; saveState(); afterListChange(); toast('已删除');
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
                <select id="edKind"><option value="auto"${!c ? ' selected' : ''}>自动（按可挖空点判定）</option>
                <option value="cloze"${c && c.kind === 'cloze' ? ' selected' : ''}>背诵卡</option>
                <option value="read"${c && c.kind === 'read' ? ' selected' : ''}>阅读卡</option></select></div>
             <div class="cd-field"><label>内容（支持 Markdown 与 $LaTeX$）</label>
                <textarea id="edBody">${c ? esc(c.md) : ''}</textarea>
                <div class="cd-hintline">可挖空点 ≥ ${CLOZE_MIN} 个判为背诵卡，否则为阅读卡（只记阅读进度）</div></div>`,
            `<button class="cd-btn" onclick="closeModal()">取消</button>
             <button class="cd-btn primary" id="edSave">保存</button>`);
        $('edSave').onclick = () => saveCard(c ? c.id : '');   // 不把 id 拼进 onclick
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
            if (c) {
                Object.assign(c, { chapter: title, md: body, subject: subj, kind, cands });
                const patch = { chapter: title, md: body, subject: subj, kind, cands };
                if (c.custom) {                       // 自建卡：改持久化副本
                    const t = (ST.custom || []).find(x => x.id === id);
                    if (t) Object.assign(t, patch); else ST.custom.push(Object.assign({ id }, c));
                } else {                              // 内置卡：存覆盖，笔记重新拆卡后仍然生效
                    ST.over[id] = patch;
                }
            }
        } else {
            const nc = {
                id: 'custom-' + Date.now(), subject: subj, noteId: 'custom', noteTitle: '我的卡片',
                chapter: title || '未命名', part: '', md: body, custom: true, kind, cands
            };
            CARDS.unshift(nc);
            ST.custom.push(nc);
        }
        saveState(); closeModal(); buildQueue(); renderList(); renderStudy();
        if (view === 'stats') renderStats();
        toast('已保存');
    }
    function openSettings() {
        openModal('设置',
            `<div class="cd-field"><label>每日新卡上限</label><input type="number" id="setNew" min="0" max="200" value="${ST.settings.newPerDay}"></div>
             <div class="cd-field"><label>每日复习上限</label><input type="number" id="setRev" min="0" max="999" value="${ST.settings.revPerDay}"></div>
             <div class="cd-field"><label>单卡挖空数（2~${MAX_CLOZE}）</label><input type="number" id="setCloze" min="2" max="${MAX_CLOZE}" value="${clozeLimit()}"></div>
             <div class="cd-hintline">阅读卡不占用上述额度；单卡目标长度 ${SOFT_LIMIT} 字以内。挖空数越大越难，建议 6~8。</div>`,
            `<button class="cd-btn" onclick="closeModal()">取消</button><button class="cd-btn primary" onclick="saveSettings()">保存</button>`);
    }
    function saveSettings() {
        ST.settings.newPerDay = clamp(parseInt($('setNew').value, 10) || 0, 0, 200);
        ST.settings.revPerDay = clamp(parseInt($('setRev').value, 10) || 0, 0, 999);
        ST.settings.clozePerCard = clamp(parseInt($('setCloze').value, 10) || DEF_CLOZE, 2, MAX_CLOZE);
        saveState(); closeModal(); rebuild(); toast('设置已保存');
    }
    function exportData() {
        const blob = new Blob([JSON.stringify({ v: 3, cards: CARDS, state: ST }, null, 1)], { type: 'application/json' });
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
                if (d.state) {
                    for (const id in (d.state.cards || {})) ST.cards[id] = Object.assign(stOf(id), d.state.cards[id]);
                    if (d.state.settings) Object.assign(ST.settings, d.state.settings);
                    if (d.state.streak) ST.streak = d.state.streak;
                    if (Array.isArray(d.state.custom)) {
                        const ids = new Set(ST.custom.map(c => c.id));
                        d.state.custom.forEach(c => { if (c && c.id && !ids.has(c.id)) ST.custom.push(c); });
                    }
                    if (d.state.over) Object.assign(ST.over, d.state.over);
                    if (d.state.hidden) Object.assign(ST.hidden, d.state.hidden);
                    if (d.state.history) Object.assign(ST.history, d.state.history);
                } else if (d.cards) {   // 兼容 v2 备份：把未知卡当自建卡收下
                    const ids = new Set(CARDS.map(c => c.id));
                    d.cards.forEach(c => { if (c && c.id && !ids.has(c.id)) ST.custom.push(Object.assign({ custom: true }, c)); });
                }
                saveState(); applyStoredCards(); rebuild(); renderList(); toast('导入完成');
            } catch (e) { toast('导入失败：文件格式不正确'); }
        };
        rd.readAsText(f); input.value = '';
    }

    // ---------------- 统计 ----------------
    function renderStats() {
        const all = visibleCards(), now = Date.now();
        let mastered = 0, learning = 0, review = 0, fresh = 0, star = 0, dueToday = 0, readAll = 0, readTodo = 0, memoN = 0;
        all.forEach(c => {
            const s = peekOf(c.id);
            if (s.star) star++;                             // 阅读卡的收藏也计入
            if (c.kind === 'read') { s.read ? readAll++ : readTodo++; return; }
            memoN++;
            if (s.state === 'mastered') mastered++;
            else if (s.state === 'learning') learning++;
            else if (s.state === 'review') review++;
            else fresh++;
            if (s.state !== 'new' && s.due <= now) dueToday++;
        });
        const rate = memoN ? Math.round(mastered / memoN * 100) + '%' : '—';
        $('cdStatGrid').innerHTML = [
            ['卡片总数', all.length], ['背诵卡', memoN], ['阅读卡', readAll + readTodo],
            ['已熟', mastered], ['复习中', review], ['不熟中', learning], ['未学', fresh],
            ['今日到期', dueToday], ['今日完成', ST.daily.done], ['连续天数', ST.streak.count],
            ['收藏', star], ['待阅读', readTodo], ['掌握率', rate]
        ].map(([l, v]) => `<div class="cd-statbox"><b>${v}</b><span>${l}</span></div>`).join('');

        // 近 14 天完成量（来自 ST.history，跨天累积）
        const tr = [];
        for (let i = 13; i >= 0; i--) {
            const d = dayKey(now - i * DAY);
            const h = (ST.history || {})[d] || {};
            tr.push([i === 0 ? '今天' : d.slice(5), h.done || 0, h.newDone || 0, h.readDone || 0, h.done ? `${h.done} 张` : '0']);
        }
        const tmax = Math.max(1, ...tr.map(t => t[1]));
        $('cdTrend').innerHTML = tr.map(([l, n, nw, r, v]) =>
            bar(l, n, tmax, v)).join('');

        const memo = all.filter(c => c.kind === 'cloze');
        const days = [];
        for (let i = 0; i < 7; i++) {
            const s0 = now + i * DAY, e0 = s0 + DAY;
            days.push([i === 0 ? '今天' : (i + 1) + ' 天后',
                memo.filter(c => { const s = peekOf(c.id); return s.state !== 'new' && s.due >= s0 && s.due < e0; }).length]);
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
            if (c.kind === 'read' ? peekOf(c.id).read : peekOf(c.id).state === 'mastered') byNote[k].m++;
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
        else if (k === 'r') hideAll($('cardBody'));
    });
    document.addEventListener('click', (e) => {
        const cl = e.target.closest && e.target.closest('.cd-cloze');
        if (cl && view === 'study' && !cl.classList.contains('revealed')) revealOne(cl);
    });
    /* 跨标签页同步：另一个标签改了进度/收藏/自建卡，本页重载状态并重绘当前视图，
       避免两个标签互相覆盖（与 category.js 的 storage 监听同思路） */
    window.addEventListener('storage', (e) => {
        if (e.key !== LS_KEY) return;
        const keep = { subject, view, queueFilter, listPage };
        const cur = currentCard();
        const curId = cur ? cur.id : '';
        loadState();
        applyStoredCards();
        subject = keep.subject; view = keep.view; queueFilter = keep.queueFilter; listPage = keep.listPage;
        buildQueue();
        if (curId && mode === 'cloze') {          // 尽量留在原来那张卡，别把用户弹回队首
            const i = queue.findIndex(c => c.id === curId);
            if (i >= 0) qi = i; else qi = Math.min(qi, Math.max(0, queue.length - 1));
        }
        if (view === 'study') renderStudy();
        else if (view === 'list') renderList();
        else renderStats();
        toast('已同步另一标签页的进度');
    });

    // ---------------- 启动 ----------------
    async function boot() {
        loadState();
        CARD_HTML = ($('cardWrap') || {}).innerHTML || '';   // 先存骨架，完成态覆盖后可还原
        try {
            const notes = await (await fetch('data/notes.json')).json();
            CARDS = buildCards(Array.isArray(notes) ? notes : (notes.items || []));
        } catch (e) { console.error('笔记加载失败', e); CARDS = []; }
        applyStoredCards();          // 自建卡 / 编辑覆盖 / 删除隐藏
        if (typeof renderDarkSwitch === 'function') renderDarkSwitch();
        buildQueue(); renderStudy();
    }
    document.addEventListener('DOMContentLoaded', boot);

    Object.assign(window, {
        switchView, setSubject, grade, toggleStar, markDone, renderList, reviewNow, markRead,
        resetCard, removeCard, openEditor, editCard, saveCard, openSettings, saveSettings,
        exportData, importData, closeModal, renderStudy, rebuild, startRead, exitRead,
        finishRead, hideAll, revealAll, setQueueFilter,
        __debug: () => ({
            total: CARDS.length,
            memo: CARDS.filter(c => c.kind === 'cloze').length,
            read: CARDS.filter(c => c.kind === 'read').length,
            custom: CARDS.filter(c => c.custom).length,
            maxLen: CARDS.reduce((m, c) => Math.max(m, (c.md || '').length), 0),
            minLen: CARDS.reduce((m, c) => Math.min(m, (c.md || '').length), 1e9),
            queueKinds: Array.from(new Set(queue.map(c => c.kind))),
            queueLen: queue.length, readQueueLen: readQueue.length,
            revealed, totalCloze, mode, filter: queueFilter,
            clozeLimit: clozeLimit(),
            settings: ST.settings,
            daily: ST.daily,
            stored: { custom: ST.custom.length, over: Object.keys(ST.over).length, hidden: Object.keys(ST.hidden).length, days: Object.keys(ST.history || {}).length }
        }),
        /** 供审计/测试遍历全部卡片（只读快照） */
        __cards: () => CARDS.map(c => ({
            id: c.id, subject: c.subject, noteId: c.noteId, chapter: c.chapter,
            kind: c.kind, cands: c.cands, len: (c.md || '').length, custom: !!c.custom, md: c.md
        })),
        /** 当前卡渲染后的挖空统计（揭示前后都可用） */
        __card: () => {
            const body = $('cardBody');
            const els = Array.from(body.querySelectorAll('.cd-cloze'));
            return {
                total: els.length,
                kinds: els.reduce((a, e) => { const k = e.getAttribute('data-k') || '?'; a[k] = (a[k] || 0) + 1; return a; }, {}),
                katex: body.querySelectorAll('.katex').length,
                strong: body.querySelectorAll('strong').length,
                revealed,
                samples: els.slice(0, 5).map(e => ({ k: e.getAttribute('data-k'), c: e.getAttribute('data-c') }))
            };
        }
    });
})();
