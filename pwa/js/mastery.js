/* ============================================================================
   掌握地图（分类页专用悬浮面板）
   ----------------------------------------------------------------------------
   数据来源：当前数据源（真题 / 核心题库）的全部题目 + 知识点树
             + localStorage 的 ⭐收藏(examFav) / 🟡不熟·🔴不会(examStatus)
   口径：每个知识点一色块，四态互斥计数
         不会(红) / 不熟(黄) / 有标记已过关(绿，仅收藏未标不熟不会) / 未标记(灰)
         掌握率 = (总数 − 不会 − 不熟) / 总数
   分级：有「不会」→ 红；否则有「不熟」→ 黄；否则全无标记/已关照 → 绿
   交互：点色块直接在分类页切到该知识点（关闭面板并滚到题目区）
   ============================================================================ */

function mmEsc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
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
            total: 0, unk: 0, unf: 0, favOnly: 0, none: 0,
        });
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null;
        const f = !!fav[qid];
        o.total++;
        if (s === 'unknown') o.unk++;
        else if (s === 'unfamiliar') o.unf++;
        else if (f) o.favOnly++;
        else o.none++;
    }
    // 挂到章节（L1）下
    const chapters = {};
    for (const cid in map) {
        const o = map[cid];
        const ch = cats[String(cats[cid].parentId)];
        const chKey = ch ? ch.id : 0;
        if (!chapters[chKey]) chapters[chKey] = { name: ch ? (ch.display || ch.name) : '其他', rows: [] };
        o.rate = o.total ? (o.total - o.unk - o.unf) / o.total : 1;
        o.level = o.unk > 0 ? 'bad' : (o.unf > 0 ? 'warn' : 'ok');
        chapters[chKey].rows.push(o);
    }
    const CH_ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程',
        '行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
    const groups = Object.values(chapters).map(g => {
        g.rows.sort((a, b) => a.rate - b.rate || b.unk - a.unk || b.total - a.total);   // 最弱在前
        g.total = g.rows.reduce((s, r) => s + r.total, 0);
        g.unk = g.rows.reduce((s, r) => s + r.unk, 0);
        g.unf = g.rows.reduce((s, r) => s + r.unf, 0);
        g.rate = g.total ? (g.total - g.unk - g.unf) / g.total : 1;
        return g;
    });
    groups.sort((a, b) => {
        const ia = CH_ORDER.indexOf(a.name), ib = CH_ORDER.indexOf(b.name);
        return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
    });
    const rows = Object.values(map);
    const t = {
        total: rows.reduce((s, r) => s + r.total, 0),
        unk: rows.reduce((s, r) => s + r.unk, 0),
        unf: rows.reduce((s, r) => s + r.unf, 0),
        favOnly: rows.reduce((s, r) => s + r.favOnly, 0),
        none: rows.reduce((s, r) => s + r.none, 0),
        cats: rows.length,
    };
    t.rate = t.total ? (t.total - t.unk - t.unf) / t.total : 1;
    return { groups, totals: t };
}

const MM_TIP = '掌握率 = (题数 − 🔴不会 − 🟡不熟) / 题数；有「不会」标红、仅「不熟」标黄、无标记标绿。点色块直接切到该知识点。';

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
                    <button class="an-x" onclick="closeMasteryMap()" title="关闭">✕</button>
                </div>
                <div class="an-body" id="mmBody"><div class="an-loading">统计中…</div></div>
                <div class="an-foot">
                    <span class="mm-legend"><i class="mm-dot mm-bad"></i>有🔴不会</span>
                    <span class="mm-legend"><i class="mm-dot mm-warn"></i>仅🟡不熟</span>
                    <span class="mm-legend"><i class="mm-dot mm-ok"></i>无🔴🟡</span>
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
    const bars = `
        <div class="mm-bar"><span class="mm-bar-fill" style="width:${(t.rate * 100).toFixed(1)}%"></span></div>
        <div class="an-ov">
            总体掌握率 <b>${mmPct(t.rate)}</b>（${t.total - t.unk - t.unf} / ${t.total} 题已过关）
            ｜🔴不会 <b>${t.unk}</b> · 🟡不熟 <b>${t.unf}</b> · ⭐收藏未标 <b>${t.favOnly}</b> · 未标记 <b>${t.none}</b>
            ｜知识点 <b>${t.cats}</b> 个
        </div>`;
    const groupsHtml = data.groups.map(g => `
        <div class="mm-group">
            <div class="mm-group-head">
                <span class="mm-group-name">${mmEsc(g.name)}</span>
                <span class="mm-group-meta">${g.rows.length} 个知识点 · ${g.total} 题 · 掌握率 ${mmPct(g.rate)}${g.unk ? ` · 🔴${g.unk}` : ''}${g.unf ? ` · 🟡${g.unf}` : ''}</span>
            </div>
            <div class="mm-grid">
                ${g.rows.map(r => `
                    <button class="mm-cell mm-${r.level}" onclick="mmJump(${r.id})"
                            title="${mmEsc(r.path)}｜共 ${r.total} 题：🔴不会 ${r.unk} · 🟡不熟 ${r.unf} · ⭐收藏未标 ${r.favOnly} · 未标记 ${r.none}｜点此跳转刷题">
                        <span class="mm-cell-name">${mmEsc(r.name)}</span>
                        <span class="mm-cell-rate">${mmPct(r.rate)}</span>
                        <span class="mm-cell-fill" style="width:${(r.rate * 100).toFixed(1)}%"></span>
                        <span class="mm-cell-stat">${r.unk ? `🔴${r.unk} ` : ''}${r.unf ? `🟡${r.unf} ` : ''}${(r.favOnly ? `⭐${r.favOnly} ` : '')}${r.none ? `⚪${r.none}` : ''}<em>/${r.total}</em></span>
                    </button>`).join('')}
            </div>
        </div>`).join('');
    body.innerHTML = bars + groupsHtml;
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
