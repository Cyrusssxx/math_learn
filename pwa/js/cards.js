/* 记忆卡 v2：阅读卡 / 背诵卡分型 + 更稳的拆卡 + 评分前置校验 + 巩固重藏 + 队列动态插队
   - 卡片来源：data/notes.json（高数 gs / 线代 xd），按 ## 章节拆卡，过长按段落/句子二次拆分
   - 分型：可挖空点 ≥2 → 背诵卡（进 SRS 队列）；否则 → 阅读卡（只记阅读进度，不做间隔重复）
   - 交互：点击空位揭示；未全部揭示不允许评分；可「重新隐藏」再记一次；不会卡到期自动插回队列
*/
(function () {
    'use strict';

    const LS_KEY = 'cd_state_v1';
    const DAY = 86400000;
    const MAX_CLOZE = 6;         // 单卡挖空数硬上限（实际值由设置 clozePerCard 决定）
    const DEF_CLOZE = 3;         // 默认单卡挖空数：一卡 3 个空，点一次「显示全部答案」就能过
    const SOFT_LIMIT = 600;      // 单卡目标字数上限：一个语义块（2~4 个知识点），别把整节塞进一张卡
    const CLOZE_MIN = 2;         // 少于该挖空点视为「阅读卡」

    function clozeLimit() {
        const v = ST && ST.settings ? ST.settings.clozePerCard : DEF_CLOZE;
        return clamp(parseInt(v, 10) || DEF_CLOZE, 1, MAX_CLOZE);
    }

    let CARDS = [];
    let ST = null;
    let view = 'study';
    let subject = '';
    let queue = [];               // 背诵卡队列
    let readQueue = [];           // 阅读卡队列（今日未读）
    let CARD_HTML = '';           // 卡片骨架快照（完成态会整体替换 cardWrap，需要能还原）
    let LAST_CANDS = [];            // 上一张卡在 DOM 层收集到的挖空候选（测试探针）
    let LAST_NODES = [];            // 上一张卡 walker 看到的前几个含 $ 的文本节点（测试探针）
    let UNBALANCED = [];             // 诊断用：修完仍 $ 未配平而被丢弃的分片（正常应为 0）
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

    /** 把 md 解析成有序「语义块」：列表项 / 表格 / 图片 / 段落 / 独立显示公式。
     *  列表项是数学笔记里最小的知识点单元（实测 100% 章节都是列表结构），
     *  按块边界切卡才不会把一条知识点劈成两半。 */
    function toBlocks(md) {
        const blocks = [];
        const lines = String(md || '').split('\n');
        let i = 0;
        while (i < lines.length) {
            const l = lines[i];
            if (!l.trim()) { i++; continue; }
            if (/^\s*-\s/.test(l)) {
                let t = l; i++;
                // 吃掉该列表项的缩进续行（子项 / 补充说明）
                while (i < lines.length && lines[i].trim() && !/^\s*-\s/.test(lines[i])) { t += '\n' + lines[i]; i++; }
                blocks.push({ text: t, type: 'item' });
            } else if (l.trim().startsWith('|')) {
                let t = l; i++;
                while (i < lines.length && lines[i].trim().startsWith('|')) { t += '\n' + lines[i]; i++; }
                blocks.push({ text: t, type: 'table' });
            } else if (/^\s*\$\$\s*$/.test(l) || /^\s*\$\$[^$]*\$\$\s*$/.test(l)) {
                blocks.push({ text: l, type: 'display' }); i++;     // $$…$$ 独占行 = 原子块，绝不切开
            } else {
                blocks.push({ text: l, type: typeOfLine(l) }); i++;
            }
        }
        return blocks;
    }
    function typeOfLine(l) {
        if (/^!\[/.test(l.trim())) return 'img';
        if (/^#{1,6}\s/.test(l.trim())) return 'head';
        return 'para';
    }
    /** 卡片是否「$ 配平」：KaTeX auto-render 是按整个容器的文本流配对 $ 的，
     *  一旦某个 $ 对被拆散（拆卡切在公式中间），它会一路配到卡末，
     *  **把中间的整段文字吞进 display 公式**（实测「渐近线」卡丢失 4 段结论）。
     *  这里在拆卡阶段就卡死：行内 $ 不跨行，所以只要每行完整保留就必然配平。 */
    function isBalanced(text) {
        const s = String(text);
        if (/\$\$[^\n]*\$/.test(s)) return false;            // 一行内出现两次 $$（数据异常）
        return (s.match(/\$/g) || []).length % 2 === 0;
    }
    /** 按句子边界切超长文本。分隔符只取 。；！？——逗号在数学式里太常见，
     *  按逗号切会把 $a,b$ 切成两半；最后再兜底做一次按行硬切。 */
    function splitSentences(text, limit) {
        const out = []; let s = '';
        for (const sen of String(text).split(/(?<=[。；！？])/)) {
            if (s && s.length + sen.length > limit) { out.push(s); s = sen; }
            else s += sen;
        }
        if (s.trim()) out.push(s);
        // 兜底：仍超长的（无标点的长串）→ 按行切；再不行按长度硬切
        const fin = [];
        for (const x of out) {
            if (x.length <= limit) { fin.push(x); continue; }
            const lines = x.split('\n'); let cur = '';
            for (const ln of lines) {
                if (cur && cur.length + ln.length + 1 > limit) { fin.push(cur); cur = ln; }
                else cur += (cur ? '\n' : '') + ln;
            }
            if (cur) fin.push(cur);
            for (const y of fin.splice(fin.length - 1)) {
                for (let k = 0; k < y.length; k += limit) fin.push(y.slice(k, k + limit));
            }
        }
        return fin.filter(x => x && x.trim());
    }
    /** 落单的 $（源数据瑕疵，实测 17 处）→ 修成配平，绝不让坏内容进渲染。
     *  ① 同行 $$…$$ → 直接改成行内 $…$（记忆卡是窄卡片，display 公式本就难显示）
     *  ② 仍奇数 → 删掉每行最后一个多余的 $ */
    function stripLoneDollar(t) {
        return t.split('\n').map(line => {
            const s = line.replace(/\$\$([^$\n]+)\$\$/g, '$$$1$$');
            if ((s.match(/\$/g) || []).length % 2 === 0) return s;
            const last = s.lastIndexOf('$');
            return s.slice(0, last) + s.slice(last + 1);
        }).join('\n');
    }
    /** 拆卡收尾：保证每张输出的卡片 $ 必然配平 */
    function emitCard(raw, out) {
        let t = String(raw || '').trim();
        if (!t) return;
        if (!isBalanced(t)) t = stripLoneDollar(t);
        if (isBalanced(t)) out.push(t);
        else UNBALANCED.push(t.slice(0, 60));      // 仍不配平（极端情况）→ 丢弃，绝不送进渲染
    }
    /** 语义块累积成卡：块优先、不切断块；单块超长时先降级拆句再插回序列 */
    function splitLong(md, limit) {
        limit = limit || SOFT_LIMIT;
        md = String(md || '');
        const out = [];
        if (md.length <= limit) { emitCard(md, out); return out; }
        const queue = toBlocks(md);
        let buf = '', len = 0, lastType = '';
        const push = () => { emitCard(buf, out); buf = ''; len = 0; lastType = ''; };
        while (queue.length) {
            const b = queue.shift();
            if (b.text.length > limit && b.type !== 'display') {
                const parts = splitSentences(b.text, limit);
                for (let k = parts.length - 1; k >= 0; k--) queue.unshift({ text: parts[k], type: b.type });
                continue;
            }
            if (len + b.text.length > limit && buf) push();
            // 列表项/显示公式之间用单换行（保持同一个 <ul>），其余块之间空行分段
            const sameList = (lastType === 'item' && b.type === 'item') || (lastType === 'display' && b.type === 'display');
            const sep = (lastType && sameList) ? '\n' : (buf ? '\n\n' : '');
            buf += sep + b.text; len += b.text.length + sep.length; lastType = b.type;
        }
        push();
        return out;
    }

    /* ============ 挖空候选的质量判定 ============
     * 旧规则「见 $ 就挖」实测 32% 的洞是没有记忆价值的（单字符 $n$、纯变量 $x_0$、
     * 加粗标签「核心不等式」、短符号 $x<0$）。新规则只挖「值得回忆的公式」。 */
    const CLOZE_MIN_LEN = 4;      // 短于 4 字符的公式不挖（$n$/$x$/$0$）
    const VARISH_RE = /^[a-zA-Z](_\{?[a-zA-Z0-9]+\}?|\^\{?[a-zA-Z0-9*]+\}?)?$/;   // 纯变量式：x / a_n / x^2
    /* 结构宏：出现这些说明公式「有内容」（分式/积分/求和/极限/根号/希腊字母/函数名）
       注意不含 \to、\Rightarrow、\cdot 这类连接符——它们单独出现（$x\to0$）不是知识点 */
    const STRUCT_RE = /\\d?frac|\\int|\\iint|\\sum|\\prod|\\lim|\\sqrt|\\begin|\\pi|\\theta|\\alpha|\\beta|\\gamma|\\lambda|\\mu|\\sigma|\\varphi|\\sin|\\cos|\\tan|\\cot|\\arc|\\ln|\\log|\\exp|\\mathrm|\\text|\\infty/;
    const REL_RE = /[=<>]|\\le|\\ge|\\ne|\\neq|\\leq|\\geq|\\approx/;

    /** 公式是否值得挖：① 有关系符（等式/不等式）→ 一定是知识点
     *  ② 否则要够长（≥12 字符）且有结构宏（如 \lim_{x\to0}f(x)）
     *  ③ 纯变量、纯符号、太短的都不挖 */
    function isWorthy(inner) {
        const s = String(inner).trim();
        if (s.length < CLOZE_MIN_LEN) return false;
        if (VARISH_RE.test(s)) return false;
        if (REL_RE.test(s)) return true;
        return s.length >= 12 && STRUCT_RE.test(s);
    }
    /** 打分：分数高的先挖。结论式 > 结构式 > 一般；太短降权；笔记里标了 ⚠️/⭐/例 的行再加权 */
    function clozeScore(inner, ctx) {
        const s = String(inner).trim();
        let v = 0;
        if (REL_RE.test(s)) v += 4;                                // 等式/不等式结论：最该记住
        if (/\\d?frac|\\int|\\sum|\\lim|\\sqrt|\\begin/.test(s)) v += 2;
        if (s.length >= 60) v += 1; else if (s.length >= 12) v += 2;
        if (s.length < 8) v -= 2;
        if (ctx && /⚠️|⭐|例[：:（(]/.test(ctx)) v += 2;            // 易错/常考/例题段落里的公式
        return v;
    }
    /** 抽取卡内行内公式（带所在整行上下文，供打分用）。与 DOM 层用同一条正则，
     *  否则「候选数」会和「实际挖空数」对不上（曾因 $$…$$ 未被排除导致 9 张卡不一致） */
    function formulaCands(md) {
        const out = [];
        for (const line of String(md || '').split('\n')) {
            const re = new RegExp(MATH_RE.source, 'g');
            let m;
            while ((m = re.exec(line))) out.push({ inner: m[0].slice(1, -1).trim(), ctx: line });
        }
        return out.filter(c => isWorthy(c.inner));
    }

    function countClozeCandidates(md) { return formulaCands(md).length; }

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
    /* 只挖行内公式（$…$）——加粗在本笔记里多是分类标签（「核心不等式」「三元均值」），
       挖掉没有记忆价值；实测加粗类洞占旧版 12.7%。
       ⚠️ 两侧负向断言 (?<!\$)/(?!\$) 用来排除显示公式 $$…$$：
       $$X$$ 中间的两个 $ 会配成一对，被当成行内公式挖走，既破坏 KaTeX 的 block 渲染，
       又让「候选数」与「实际挖空数」对不上（实测 9 张卡受影响）。 */
    const MATH_RE = /(?<!\$)\$[^$\n]{1,120}\$(?!\$)/g;

    function makeCloze(inner) {
        const sp = document.createElement('span');
        sp.className = 'cd-cloze';
        sp.setAttribute('data-c', inner);
        sp.setAttribute('data-k', 'm');
        sp.title = '点击显示答案';
        sp.textContent = CL_PLACE;
        return sp;
    }

    /** 只跳过已有挖空内部的节点（strong 内的公式仍要挖：**结论：$x=1$** 是重点） */
    function insideCloze(n, container) {
        let p = n.parentNode;
        while (p && p !== container) {
            if (p.nodeType === 1 && p.classList.contains('cd-cloze')) return true;
            p = p.parentNode;
        }
        return false;
    }

    /** 收集容器内值得挖的公式候选：{node, index, len, inner, score, order} */
    function collectCands(container) {
        const list = [];
        LAST_NODES = [];
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
        let n, idx = 0;
        while ((n = walker.nextNode())) {
            const s = n.nodeValue;
            if (!s || !s.trim() || insideCloze(n, container)) continue;
            if (LAST_NODES.length < 8 && s.indexOf('$') >= 0) LAST_NODES.push(s.slice(0, 160));
            const ctx = (n.parentNode && n.parentNode.textContent) || s;
            MATH_RE.lastIndex = 0;
            const hits = [];
            let m;
            while ((m = MATH_RE.exec(s))) {
                const inner = m[0].slice(1, -1).trim();
                if (!isWorthy(inner)) continue;
                hits.push({ index: m.index, len: m[0].length, inner, score: clozeScore(inner, ctx) });
            }
            if (!hits.length) { idx++; continue; }
            hits.sort((a, b) => a.index - b.index);
            const clean = []; let lastEnd = -1;
            for (const h of hits) if (h.index >= lastEnd) { clean.push(h); lastEnd = h.index + h.len; }
            clean.forEach((h, j) => { h.node = n; h.order = idx * 1000 + j; });
            idx++;
            list.push.apply(list, clean);
        }
        return list;
    }

    /** 在已渲染的 HTML 上挖空，返回实际挖出的空数。
     *  选题策略：按 clozeScore 取前 N（结论式/结构式优先），不再按位置均匀采样——
     *  「别乱挖」的意思是挖最有价值的，而不是挖得均匀。 */
    function applyCloze(container, max) {
        max = clamp(max || clozeLimit(), 1, MAX_CLOZE);
        const cands = collectCands(container);
        LAST_CANDS = cands.map(c => ({ inner: c.inner, score: c.score }));
        if (!cands.length) return 0;
        const picked = cands
            .map((c, i) => ({ c, i }))
            .sort((a, b) => (b.c.score - a.c.score) || (a.i - b.i))     // 同分保持文档顺序
            .slice(0, max)
            .map(x => x.c);
        // 替换：同一文本节点内的多个候选一次性处理（避免节点被替换两次）
        const byNode = new Map();
        picked.forEach(p => {
            if (!p.node.parentNode || !container.contains(p.node)) return;
            if (!byNode.has(p.node)) byNode.set(p.node, []);
            byNode.get(p.node).push(p);
        });
        byNode.forEach((hs, node) => {
            const s = node.nodeValue;
            let html = '', last = 0;
            hs.sort((a, b) => a.index - b.index).forEach(h => {
                if (h.index < last) return;
                html += esc(s.slice(last, h.index)) + makeCloze(h.inner).outerHTML;
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
    /** 全部揭示才点亮评分区（仍可点击，未就绪时由 grade() 给出提示）
     *  「显示全部答案」按钮是主控：一次点开全部空位，不用一个一个点 */
    function refreshReady() {
        const a = $('cardActions');
        const rb = $('btnRevealAll');
        if (rb) {
            const left = totalCloze - revealed;
            const b = rb.querySelector('b'), sp = rb.querySelector('span');
            if (b) b.textContent = left > 0 ? '👁 显示全部答案' : '↺ 重新隐藏再记一遍';
            if (sp) sp.textContent = left > 0 ? `还剩 ${left} 个空` : '点一遍巩固';
            rb.classList.toggle('revealed', left <= 0 && totalCloze > 0);
            rb.hidden = totalCloze === 0;
        }
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
            ? `本卡挖了 <b>${totalCloze}</b> 个空 · 点下方「显示全部答案」一次看完，也可单独点某个空`
            : `全部答案已显示 · 评价后进入下一张`;
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
        // 新卡优先（先把没见过的学掉），复习卡随后；筛选态下不受每日额度限制
        queue = queueFilter
            ? fresh.concat(due)
            : fresh.slice(0, newLeft).concat(due.slice(0, revLeft));
        readQueue = pendingRead().slice(0, 30);
        qi = 0; mode = 'cloze';
    }

    /* 说明：旧版有 injectDueCards() 把「10 分钟到期的不会卡」插回当前队列，
       现已按用户要求改为「不会的隔天再看」，同一天不重复滚卡，故移除该机制。 */

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
            <button class="cd-reveal" id="btnRevealAll"><b>👁 显示全部答案</b><span></span></button>
            <button class="cd-grade g0" id="g0"><b>🔴 不会</b><span>明天再看</span></button>
            <button class="cd-grade g1" id="g1"><b>🟡 不熟</b><span>隔更久再看</span></button>
            <button class="cd-grade g2" id="g2"><b>✅ 记得</b><span>拉长间隔</span></button>`;
        $('g0').onclick = () => grade(0); $('g1').onclick = () => grade(1); $('g2').onclick = () => grade(2);
        $('btnRevealAll').onclick = () => {
            if (allRevealed()) hideAll($('cardBody'));
            else revealAll($('cardBody'));
        };
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
        /* 间隔节奏：不会的隔天再看（不再当天 10 分钟插回，避免一天反复滚同几张），
           不熟 ×1.6 且至少 2 天，记得 ×ease 且首记 2 天，间隔满 30 天才算「已熟」 */
        if (g === 0) {
            s.lapses++; s.ease = clamp(s.ease - 0.25, 1.3, 3.0);
            s.interval = 1; s.due = Date.now() + DAY; s.state = 'learning';
        } else if (g === 1) {
            s.ease = clamp(s.ease - 0.15, 1.3, 3.0);
            s.interval = Math.max(2, Math.round((s.interval || 2) * 1.6));
            s.due = Date.now() + s.interval * DAY; s.state = 'learning';
        } else {
            s.reps++;
            s.interval = s.reps <= 1 ? 2 : Math.max(2, Math.round((s.interval || 2) * s.ease));
            s.due = Date.now() + s.interval * DAY;
            s.state = s.interval >= 30 ? 'mastered' : 'review';
        }
        // 新卡与复习卡分开计数，每日新卡上限才真正生效
        if (wasNew) ST.daily.newDone++; else ST.daily.revDone++;
        ST.daily.done++;
        bumpStreak(); saveState();
        qi++;
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
             <div class="cd-field"><label>单卡挖空数（1~${MAX_CLOZE}）</label><input type="number" id="setCloze" min="1" max="${MAX_CLOZE}" value="${clozeLimit()}"></div>
             <div class="cd-hintline">只挖「值得记」的公式（等式/结构式优先，跳过单字符与纯变量）；<br>阅读卡不占用额度；单卡目标长度 ${SOFT_LIMIT} 字以内。挖空数 2~4 比较舒服。</div>`,
            `<button class="cd-btn" onclick="closeModal()">取消</button><button class="cd-btn primary" onclick="saveSettings()">保存</button>`);
    }
    function saveSettings() {
        ST.settings.newPerDay = clamp(parseInt($('setNew').value, 10) || 0, 0, 200);
        ST.settings.revPerDay = clamp(parseInt($('setRev').value, 10) || 0, 0, 999);
        ST.settings.clozePerCard = clamp(parseInt($('setCloze').value, 10) || DEF_CLOZE, 1, MAX_CLOZE);
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
            queueHead: queue.slice(0, 5).map(c => ({ id: c.id, chapter: c.chapter, state: peekOf(c.id).state })),
            lastCands: LAST_CANDS,
            lastNodes: LAST_NODES,
            unbalancedDropped: UNBALANCED.length,   // 修完仍 $ 未配平被丢弃的分片数（应为 0）
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
