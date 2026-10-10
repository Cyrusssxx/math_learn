/* ============================================================================
   核心题库 · 刷题建议（分类页专用悬浮面板）
   ----------------------------------------------------------------------------
   与「掌握地图」的分工：
     掌握地图 = 看**当前数据源**的整体分布（色块图）
     本面板   = 只针对**核心题库**（core_bank.json，741 题），回答「接下来刷哪个知识点」

   两个口径刻意分开，避免混淆：
     · 薄弱 = 你在**全部题目**（数二真题 + 大观园习题 + 核心题库 + 线代重点题）里
              标记的「不会×2 + 不熟×1」，聚合到 L2 知识点。
              用全库而非只用核心题库：核心题库目前标记很少，只用它算权重会
              让几乎所有知识点都是 0，排不出优先级。
     · 待刷 = **核心题库**里还没掌握的题数 = 未刷 + 不会 + 不熟。
   推荐分 = 薄弱 × 4 + log2(待刷 + 1)，让「有短板 + 还有余粮」的排前面。
   ============================================================================ */

function advEsc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

/** 汇总「薄弱权重」：遍历全库题目，按 qid 去重后读标记，聚合到 L2 知识点 */
function advWeight() {
    const st = (typeof statusGet === 'function') ? (statusGet() || {}) : {};
    const W = {};
    const seen = new Set();
    const add = (paperId, q, cids) => {
        if (!q) return;
        const qid = qidOf(paperId, q.no);
        if (seen.has(qid)) return;              // 同一道题在多库里只算一次
        seen.add(qid);
        const s = st[qid];
        const w = (s === 'unknown') ? 2 : (s === 'unfamiliar' ? 1 : 0);
        if (!w) return;
        for (const cid of (cids || [])) {
            const c = cats[String(cid)];
            if (c && c.level === 2) W[String(cid)] = (W[String(cid)] || 0) + w;
        }
    };
    for (const p of (typeof examPapers !== 'undefined' && examPapers || []))
        for (const s of (p.sections || []))
            for (const q of (s.questions || [])) add(p.id, q, q.categoryIds);
    for (const p of (typeof corePapers !== 'undefined' && corePapers || []))
        for (const s of (p.sections || []))
            for (const q of (s.questions || [])) add(p.id, q, q.categoryIds);
    for (const e of (typeof xdItems !== 'undefined' && xdItems || [])) add(e.paper.id, e.q, e.catIds);
    for (const e of (typeof bankItems !== 'undefined' && bankItems || [])) add(e.paper.id, e.q, e.catIds);
    return W;
}

/** 汇总核心题库的四态（按 L2 知识点 + 总计） */
function advCore() {
    const st = (typeof statusGet === 'function') ? (statusGet() || {}) : {};
    const fav = (typeof favGet === 'function') ? (favGet() || {}) : {};
    const tot = { total: 0, mst: 0, unk: 0, unf: 0, none: 0 };
    const byCid = {};
    for (const p of (typeof corePapers !== 'undefined' && corePapers || [])) {
        for (const s of (p.sections || [])) {
            for (const q of (s.questions || [])) {
                const qid = qidOf(p.id, q.no);
                const s2 = st[qid] || null;
                const f = !!fav[qid];
                // 四态互斥：不会 / 不熟 / 已掌握（显式标记，或已收藏且无薄弱标记）/ 未刷
                const k = (s2 === 'unknown') ? 'unk'
                    : (s2 === 'unfamiliar') ? 'unf'
                        : (s2 === 'mastered' || f) ? 'mst' : 'none';
                tot.total++; tot[k]++;
                for (const cid of (q.categoryIds || [])) {
                    const c = cats[String(cid)];
                    if (!c || c.level !== 2) continue;
                    const o = byCid[cid] || (byCid[cid] = {
                        id: Number(cid), name: c.display || c.name, path: c.path || '',
                        total: 0, mst: 0, unk: 0, unf: 0, none: 0,
                    });
                    o.total++; o[k]++;
                }
            }
        }
    }
    return { tot, byCid };
}

function advScore(w, todo) {
    return w * 4 + (todo > 0 ? Math.log2(todo + 1) : 0);
}function advPct(a, b) { return b ? Math.round(a / b * 100) + '%' : '—'; }

/** 打开/刷新「刷题建议」面板 */
function openStudyAdvice() {
    let mask = document.getElementById('advMask');
    if (!mask) {
        mask = document.createElement('div');
        mask.id = 'advMask';
        mask.className = 'an-mask';
        mask.innerHTML = `
            <div class="an-panel adv-panel" onclick="event.stopPropagation()">
                <div class="an-head">
                    <div>
                        <div class="an-title">💡 核心题库 · 刷题建议</div>
                        <div class="an-sub" id="advSub">按「你的薄弱标记 × 核心题库待刷量」排出优先顺序 · 点一行直达该知识点</div>
                    </div>
                    <div class="adv-headbtns">
                        <button class="an-x" onclick="closeStudyAdvice()" title="关闭">✕</button>
                    </div>
                </div>
                <div class="an-body" id="advBody"><div class="an-loading">统计中…</div></div>
                <div class="an-foot">
                    <span class="adv-legend"><i class="adv-dot adv-bad"></i>不会</span>
                    <span class="adv-legend"><i class="adv-dot adv-warn"></i>不熟</span>
                    <span class="adv-legend"><i class="adv-dot adv-ok"></i>已掌握</span>
                    <span class="adv-legend"><i class="adv-dot adv-todo"></i>待刷</span>
                    <span class="adv-note" id="advNote"></span>
                    <button class="an-btn" onclick="openStudyAdvice()">🔄 刷新</button>
                </div>
            </div>`;
        mask.addEventListener('click', () => closeStudyAdvice());
        document.body.appendChild(mask);
    }
    mask.classList.add('show');
    const body = document.getElementById('advBody');
    if (typeof corePapers === 'undefined' || !corePapers.length) {
        body.innerHTML = '<div class="an-empty">核心题库还没加载完，稍后再点一次。</div>';
        return;
    }
    const W = advWeight();
    const data = advCore();
    const t = data.tot;
    // 组装行：只保留核心题库里有题的 L2 知识点
    const rows = Object.keys(data.byCid).map(cid => {
        const o = data.byCid[cid];
        const w = W[cid] || 0;
        const todo = o.none + o.unk + o.unf;
        return Object.assign({}, o, { w, todo, score: advScore(w, todo) });
    });
    // 排序：薄弱降序 → 待刷降序 → 知识点 id。
    // 刻意不让 log 项越过薄弱档（否则「薄弱 3 但待刷 41」会排到「薄弱 4 但待刷 1」前面，
    // 表格里看就是薄弱列不降序，容易让人以为排错了）。score 仍保留在 title 里做解释。
    rows.sort((a, b) => b.w - a.w || b.todo - a.todo || a.id - b.id);

    // 统计徽章
    const weakCats = rows.filter(r => r.w > 0).length;
    const zeroCats = rows.filter(r => r.todo === 0).length;
    const bars = `
        <div class="adv-ov">
            <div class="adv-ov-main">
                <div class="adv-ov-num"><b>${t.total}</b> 题<span>核心题库总量</span></div>
                <div class="adv-ov-num adv-ok"><b>${t.mst}</b> 题<span>已掌握（${advPct(t.mst, t.total)}）</span></div>
                <div class="adv-ov-num adv-bad"><b>${t.unk}</b> 题<span>不会</span></div>
                <div class="adv-ov-num adv-warn"><b>${t.unf}</b> 题<span>不熟</span></div>
                <div class="adv-ov-num"><b>${t.none}</b> 题<span>未刷（${advPct(t.none, t.total)}）</span></div>
            </div>
            <div class="adv-ov-bar">
                <span class="adv-s adv-mst" style="width:${(t.mst / Math.max(1, t.total) * 100).toFixed(2)}%"></span>
                <span class="adv-s adv-unf" style="width:${(t.unf / Math.max(1, t.total) * 100).toFixed(2)}%"></span>
                <span class="adv-s adv-unk" style="width:${(t.unk / Math.max(1, t.total) * 100).toFixed(2)}%"></span>
                <span class="adv-s adv-none" style="width:${(t.none / Math.max(1, t.total) * 100).toFixed(2)}%"></span>
            </div>
            <div class="adv-ov-tip">
                涉及 <b>${rows.length}</b> 个知识点，其中 <b>${weakCats}</b> 个有薄弱标记${zeroCats ? `，<b>${zeroCats}</b> 个已全部掌握` : ''}。
                排序：<b>薄弱</b>（你在全部题目里标的 不会×2＋不熟）降序，同档再按<b>待刷</b>降序——先补短板，再清存量。
            </div>
        </div>`;

    const list = rows.filter(r => r.todo > 0);
    const done = rows.filter(r => r.todo === 0);
    const rowHtml = (r, i) => `
        <tr class="adv-row${r.w >= 15 ? ' adv-hot' : (r.w > 0 ? ' adv-warm' : '')}" onclick="advJump(${r.id})"
            title="${advEsc(r.path)}｜核心题库 ${r.total} 题：不会 ${r.unk} · 不熟 ${r.unf} · 已掌握 ${r.mst} · 未刷 ${r.none}｜点击跳到该知识点">
            <td class="adv-i">${i + 1}</td>
            <td class="adv-name">
                <b>${advEsc(r.name)}</b>
                <em>${advEsc((r.path || '').replace(/\s*\/\s*[^/]*$/, ''))}</em>
            </td>
            <td class="adv-w">${r.w ? `<span class="adv-badge">${r.w}</span>` : '<span class="adv-dash">—</span>'}</td>
            <td class="adv-todo"><b>${r.todo}</b><em>/ ${r.total}</em></td>
            <td class="adv-bd">
                ${r.unk ? `<span class="adv-t adv-t-unk">不会 ${r.unk}</span>` : ''}
                ${r.unf ? `<span class="adv-t adv-t-unf">不熟 ${r.unf}</span>` : ''}
                ${r.none ? `<span class="adv-t adv-t-none">未刷 ${r.none}</span>` : ''}
            </td>
            <td class="adv-go">刷 →</td>
        </tr>`;

    const tbl = list.length ? `
        <table class="adv-tbl">
            <thead><tr>
                <th style="width:34px">#</th>
                <th>知识点</th>
                <th style="width:58px" title="你在全部题目里标记的「不会×2 + 不熟」">薄弱</th>
                <th style="width:74px" title="核心题库里还没掌握的题数">待刷</th>
                <th style="width:184px">构成</th>
                <th style="width:52px"></th>
            </tr></thead>
            <tbody>${list.map(rowHtml).join('')}</tbody>
        </table>` : `<div class="an-empty">🎉 核心题库里的题都已有标记，没有待刷项了。</div>`;

    const doneHtml = done.length ? `
        <details class="adv-done">
            <summary>已全部掌握的知识点 ${done.length} 个</summary>
            <div class="adv-done-list">${done.map(r => `<span>${advEsc(r.name)}<em>${r.total}</em></span>`).join('')}</div>
        </details>` : '';

    body.innerHTML = bars + tbl + doneHtml;
    const note = document.getElementById('advNote');
    if (note) note.textContent = '薄弱＝全库标记 · 待刷＝核心题库';
}

function closeStudyAdvice() {
    const mask = document.getElementById('advMask');
    if (mask) mask.classList.remove('show');
}

/** 点一行 → 切到核心题库 + 定位该知识点 */
function advJump(cid) {
    closeStudyAdvice();
    if (typeof srcMode !== 'undefined' && srcMode !== 'core' && typeof toggleSrcMode === 'function') {
        try { toggleSrcMode(); } catch (e) { /* 切换失败也不阻断定位 */ }
    }
    if (typeof selectCat === 'function') {
        selectCat(Number(cid));
        const side = document.getElementById('catSide');
        if (side) side.classList.remove('collapsed');
        const main = document.getElementById('catMain');
        if (main && main.scrollIntoView) main.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
