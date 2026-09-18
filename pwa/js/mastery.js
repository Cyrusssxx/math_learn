/* ============================================================================
   掌握地图（分类页专用悬浮面板）
   ----------------------------------------------------------------------------
   数据来源：当前数据源（真题 / 核心题库）的全部题目 + 知识点树
             + localStorage 的 ⭐收藏(examFav) / 🟡不熟·🔴不会(examStatus)
   口径：每个知识点一色块，四态互斥计数
         🔴不会 / 🟡不熟 / ✅已掌握(mastered) / ⚪未刷(无任何标记)
         **掌握率 = 已掌握题数 / 总题数**（未刷、未标记的题一律计 0，不算已掌握）
   分级：有「不会」→ 红；否则有「不熟」→ 黄；仍有未刷 → 灰(待刷)；全部已掌握 → 绿
   排序：按薄弱分降序（不会×3 + 不熟×2 + 未刷×1），即错误多、待刷多的排最前
   默认只呈现薄弱项：隐藏「已 100% 掌握」的知识点（可用面板内开关显示全部）
   ============================================================================ */

function mmEsc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

// 面板视图状态：mmShowAll = 显示全部知识点（默认 false = 只看薄弱）；mmSortBy = 'weak'|'chapter'
let mmShowAll = false;
let mmSortBy = 'weak';

function toggleMmShowAll() {
    mmShowAll = !mmShowAll;
    openMasteryMap();
}

/** 汇总当前 allEntries 的掌握情况：返回按章节分组的 rows */
function mmCollect() {
    const st = (typeof statusGet === 'function') ? (statusGet() || {}) : {};
    const fav = (typeof favGet === 'function') ? (favGet() || {}) : {};
    const map = {};
    for (const e of allEntries) {
        const cid = String(e.catId);
        const c = cats[cid];
        if (!c || c.level !== 2) continue;                       // 只统计 L2 知识点
        const o = map[cid] || (map[cid] = {
            id: Number(cid), name: c.display || c.name, path: c.path || '',
            total: 0, unk: 0, unf: 0, mst: 0, none: 0,
        });
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null;
        const f = !!fav[qid];
        o.total++;
        // 三态互斥 + 未刷：不会 / 不熟 / 已过关(收藏且无薄弱标记) / 未刷(无任何痕迹 → 计 0 掌握)
        if (s === 'unknown') o.unk++;
        else if (s === 'unfamiliar') o.unf++;
        else if (f) o.mst++;          // 刷过且未留薄弱标记 → 已过关
        else o.none++;                // 未刷 → 0 掌握
    }
    // 挂到章节（L1）下
    const chapters = {};
    for (const cid in map) {
        const o = map[cid];
        const ch = cats[String(cats[cid].parentId)];
        const chKey = ch ? ch.id : 0;
        if (!chapters[chKey]) chapters[chKey] = { name: ch ? (ch.display || ch.name) : '其他', rows: [] };
        // 掌握率 = 已掌握 / 总数（未刷、未标记一律 0，不算已掌握）
        o.rate = o.total ? o.mst / o.total : 0;                       // 掌握率 = 已过关 / 总数（未刷计 0）
        o.weakRate = o.total ? (o.unk + o.unf) / o.total : 0;         // 薄弱率 =（不会+不熟）/ 总数
        o.level = o.unk > 0 ? 'bad' : (o.unf > 0 ? 'warn' : (o.none > 0 ? 'todo' : 'ok'));
        chapters[chKey].rows.push(o);
    }
    const CH_ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程',
        '行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
    const groups = Object.values(chapters).map(g => {
        // 薄弱优先：先按「不会+不熟」比率降序，再按不会数、不熟数、题数
        g.rows.sort((a, b) => b.weakRate - a.weakRate || b.unk - a.unk || b.unf - a.unf || b.total - a.total);
        g.total = g.rows.reduce((s, r) => s + r.total, 0);
        g.unk = g.rows.reduce((s, r) => s + r.unk, 0);
        g.unf = g.rows.reduce((s, r) => s + r.unf, 0);
        g.mst = g.rows.reduce((s, r) => s + r.mst, 0);
        g.none = g.rows.reduce((s, r) => s + r.none, 0);
        g.rate = g.total ? g.mst / g.total : 0;
        g.weakRate = g.total ? (g.unk + g.unf) / g.total : 0;
        return g;
    });
    // 章节之间同样按薄弱率降序：不会/不熟比率高的章排最前
    groups.sort((a, b) => b.weakRate - a.weakRate);
    // 默认按「薄弱率」降序（不会/不熟比率高的章置顶）；mmSortBy==='chapter' 时改回学科固定顺序
    if (mmSortBy === 'chapter') {
        groups.sort((a, b) => {
            const ia = CH_ORDER.indexOf(a.name), ib = CH_ORDER.indexOf(b.name);
            return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
        });
    }
    const rows = Object.values(map);
    const t = {
        total: rows.reduce((s, r) => s + r.total, 0),
        unk: rows.reduce((s, r) => s + r.unk, 0),
        unf: rows.reduce((s, r) => s + r.unf, 0),
        mst: rows.reduce((s, r) => s + r.mst, 0),
        none: rows.reduce((s, r) => s + r.none, 0),
        cats: rows.length,
    };
    t.rate = t.total ? t.mst / t.total : 0;
    t.weakCats = rows.filter(r => r.rate < 1).length;
    return { groups, totals: t };
}

const MM_TIP = '掌握率 = 已过关题数 / 总题数（未刷、未标记一律计 0）；已过关 = 已收藏且未标「不熟/不会」。薄弱率 =（🔴不会 + 🟡不熟）/ 总数，章节与知识点按薄弱率降序，默认只显示未 100% 掌握的知识点。';

function mmPct(r) { return Math.round(r * 100) + '%'; }

/** 打开/刷新掌握地图面板 */
function openMasteryMap() {
    let mask = document.getElementById('mmMask');
    if (!mask) {
        mask = document.createElement('div');
        mask.id = 'mmMask';
        mask.className = 'an-mask';
        mask.innerHTML = `
            <div class="an-panel mm-panel" onclick="event.stopPropagation()">
                <div class="an-head">
                    <div>
                        <div class="an-title">📈 掌握地图</div>
                        <div class="an-sub" id="mmSub">按知识点汇总当前数据源的掌握情况 · 点色块直接跳去刷该知识点</div>
                    </div>
                    <div class="mm-headbtns">
                        <button class="an-btn" id="mmShowAllBtn" onclick="toggleMmShowAll()">🎯 只看薄弱</button>
                        <button class="an-x" onclick="closeMasteryMap()" title="关闭">✕</button>
                    </div>
                </div>
                <div class="an-body" id="mmBody"><div class="an-loading">统计中…</div></div>
                <div class="an-foot">
                    <span class="mm-legend"><i class="mm-dot mm-bad"></i>🔴不会</span>
                    <span class="mm-legend"><i class="mm-dot mm-warn"></i>🟡不熟</span>
                    <span class="mm-legend"><i class="mm-dot mm-ok"></i>✅已过关</span>
                    <span class="mm-legend"><i class="mm-dot mm-todo"></i>⚪未刷</span>
                    <span class="mm-note">${MM_TIP}</span>
                    <button class="an-btn" onclick="openMasteryMap()">🔄 刷新</button>
                </div>
            </div>`;
        mask.addEventListener('click', () => closeMasteryMap());
        document.body.appendChild(mask);
    }
    mask.classList.add('show');
    const body = document.getElementById('mmBody');
    if (typeof allEntries === 'undefined' || !allEntries.length) {
        body.innerHTML = '<div class="an-empty">数据还没加载完，稍后再点一次。</div>';
        return;
    }
    const data = mmCollect();
    const t = data.totals;
    const sub = document.getElementById('mmSub');
    if (sub) {
        const srcName = (typeof srcMode !== 'undefined' && srcMode === 'core') ? '核心题库' : '数二真题';
        sub.textContent = `当前数据源：${srcName} · 按知识点汇总掌握情况 · 点色块直接跳去刷该知识点`;
    }
    if (!t.total) {
        body.innerHTML = '<div class="an-empty">当前数据源没有题目。</div>';
        return;
    }
    // 默认只呈现薄弱项：隐藏已 100% 掌握的知识点（mmShowAll 可显示全部）
    const vis = data.groups
        .map(g => Object.assign({}, g, { rows: mmShowAll ? g.rows : g.rows.filter(r => r.rate < 1) }))
        .filter(g => g.rows.length);
    const bars = `
        <div class="mm-bar"><span class="mm-bar-fill" style="width:${(t.rate * 100).toFixed(1)}%"></span></div>
        <div class="an-ov">
            总体掌握率 <b>${mmPct(t.rate)}</b>（✅已掌握 <b>${t.mst}</b> / ${t.total} 题）
            ｜🔴不会 <b>${t.unk}</b> · 🟡不熟 <b>${t.unf}</b> · ⚪未刷 <b>${t.none}</b>
            ｜待攻克知识点 <b>${t.weakCats}</b> / ${t.cats} 个
        </div>`;
    const groupsHtml = vis.length ? vis.map(g => `
        <div class="mm-group">
            <div class="mm-group-head">
                <span class="mm-group-name">${mmEsc(g.name)}</span>
                <span class="mm-group-meta">${g.rows.length} 个知识点 · ${g.total} 题 · 掌握率 ${mmPct(g.rate)}${g.unk ? ` · 🔴${g.unk}` : ''}${g.unf ? ` · 🟡${g.unf}` : ''}${g.none ? ` · ⚪${g.none}` : ''}</span>
            </div>
            <div class="mm-grid">
                ${g.rows.map(r => `
                    <button class="mm-cell mm-${r.level}" onclick="mmJump(${r.id})"
                            title="${mmEsc(r.path)}｜共 ${r.total} 题：🔴不会 ${r.unk} · 🟡不熟 ${r.unf} · ✅已掌握 ${r.mst} · ⚪未刷 ${r.none}｜点此跳转刷题">
                        <span class="mm-cell-name">${mmEsc(r.name)}</span>
                        <span class="mm-cell-rate">${mmPct(r.rate)}</span>
                        <span class="mm-cell-fill" style="width:${(r.rate * 100).toFixed(1)}%"></span>
                        <span class="mm-cell-stat">${r.unk ? `🔴${r.unk} ` : ''}${r.unf ? `🟡${r.unf} ` : ''}${r.mst ? `✅${r.mst} ` : ''}${r.none ? `⚪${r.none}` : ''}<em>/${r.total}</em></span>
                    </button>`).join('')}
            </div>
        </div>`).join('') : `<div class="an-empty">${mmShowAll ? '暂无数据。' : '🎉 按当前标记，所有知识点都已 100% 掌握（可点「显示全部」核对）。'}</div>`;
    body.innerHTML = bars + groupsHtml;
    const sw = document.getElementById('mmShowAllBtn');
    if (sw) {
        sw.classList.toggle('on', mmShowAll);
        sw.textContent = mmShowAll ? '👁 显示全部' : '🎯 只看薄弱';
        sw.title = mmShowAll ? '当前显示全部知识点（点击切回只看薄弱）' : '当前只显示未 100% 掌握的知识点（点击显示全部）';
    }
}

function closeMasteryMap() {
    const mask = document.getElementById('mmMask');
    if (mask) mask.classList.remove('show');
}

/** 点色块 → 切到该知识点（分类页内直接定位，不新开标签） */
function mmJump(cid) {
    closeMasteryMap();
    if (typeof selectCat === 'function') {
        selectCat(Number(cid));            // 内部会 renderTree + renderMain
        const side = document.getElementById('catSide');
        if (side) side.classList.remove('collapsed');   // 窄屏侧栏若收起则展开，让选中态可见
        const main = document.getElementById('catMain');
        if (main && main.scrollIntoView) main.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
