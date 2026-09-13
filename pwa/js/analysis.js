/* ============================================================================
   真题「分析与建议」共享面板（真题页 exam.html + 收藏汇总页 fav.html 共用）
   ----------------------------------------------------------------------------
   数据来源：localStorage 的 ⭐收藏(examFav) / 🟡不熟·🔴不会(examStatus)
             + data/exam_categories.json 知识点树（L2 为「知识点」层）
   分析依据：按知识点聚合「薄弱分 = 不会×3 + 不熟×2」，降序排序并分级
             high(≥6) 需加强 / mid(3-5) 关注 / low(1-2) 已跟踪
   闭环：跳转 → category.html?cid=<知识点id> 直接刷该知识点的题
         → 刷完标记变化后，回到本面板点「重新分析」即实时更新等级
   ============================================================================ */
let _anPapers = null, _anCats = null;

/** 面板内转义（不依赖页面其它工具函数） */
function anEsc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

async function _anLoad() {
    if (_anPapers && _anCats) return;
    const [er, cr] = await Promise.all([fetch('data/exam.json'), fetch('data/exam_categories.json')]);
    _anPapers = await er.json();
    _anCats = await cr.json();
}

/** 聚合并排序；返回 { rows, totals } */
async function analysisBuild() {
    await _anLoad();
    const fav = (typeof favGet === 'function') ? (favGet() || {}) : {};
    const st = (typeof statusGet === 'function') ? (statusGet() || {}) : {};
    const map = {};
    for (const p of _anPapers) {
        for (const sec of (p.sections || [])) {
            for (const q of (sec.questions || [])) {
                const qid = p.id + '-' + q.no;
                const f = !!fav[qid], u = st[qid] === 'unfamiliar', k = st[qid] === 'unknown';
                if (!f && !u && !k) continue;
                for (const cid of (q.categoryIds || [])) {
                    const c = _anCats[String(cid)];
                    if (!c || c.level !== 2) continue;      // 只聚合 L2（知识点）
                    const o = map[cid] || (map[cid] = { id: cid, name: c.display || c.name, path: c.path || '', total: 0, fav: 0, unf: 0, unk: 0 });
                    o.total++;
                    if (f) o.fav++;
                    if (u) o.unf++;
                    if (k) o.unk++;
                }
            }
        }
    }
    const rows = Object.values(map).map(o => {
        // 薄弱分：不会 ×3（最高）；不熟与收藏同档 ×2；收藏多者在同分时优先
        const score = o.unk * 3 + (o.unf + o.fav) * 2;
        const level = score >= 6 ? 'high' : (score >= 3 ? 'mid' : 'low');
        return Object.assign({}, o, { score, level, advice: _anAdvice(o, level) });
    }).sort((a, b) => b.score - a.score || b.unk - a.unk || b.fav - a.fav || b.unf - a.unf || a.id - b.id);
    const stVals = Object.values(st);
    return {
        rows,
        totals: {
            fav: Object.keys(fav).length,
            unf: stVals.filter(v => v === 'unfamiliar').length,
            unk: stVals.filter(v => v === 'unknown').length,
        },
    };
}

function _anAdvice(o, level) {
    if (level === 'high') return `**优先攻克**：本知识点共 ${o.total} 题，🔴不会 ${o.unk} 题、🟡不熟 ${o.unf} 题 —— 先把不会的 ${o.unk} 题重做并写出完整步骤，再连做 ${Math.max(6, o.unk * 3)} 题同类题巩固，直到能独立写全。`;
    if (level === 'mid') return `**重点巩固**：本知识点共 ${o.total} 题，🟡不熟 ${o.unf} 题${o.unk ? `、🔴不会 ${o.unk} 题` : ''} —— 建议连续做 ${Math.max(4, o.unf * 2)} 题并当场复盘错因，隔天重做错题。`;
    return `**保持关注**：本知识点共 ${o.total} 题，⭐收藏 ${o.fav} 题${o.unf ? `、🟡不熟 ${o.unf} 题` : ''} —— 抽查 2~3 题保持手感即可。`;
}

const AN_LEVEL_TAG = { high: '🔴 需加强', mid: '🟡 关注', low: '🟢 已跟踪' };

/** 打开（或重新分析）共享面板 —— 真题页顶部栏 / 收藏汇总页顶部栏同一入口 */
async function openAnalysisPanel() {
    let mask = document.getElementById('anMask');
    if (!mask) {
        mask = document.createElement('div');
        mask.id = 'anMask';
        mask.className = 'an-mask';
        mask.innerHTML = `
            <div class="an-panel" onclick="event.stopPropagation()">
                <div class="an-head">
                    <div>
                        <div class="an-title">📊 分析与建议</div>
                        <div class="an-sub">基于你的 ⭐收藏 / 🟡不熟 / 🔴不会 标记，定位薄弱知识点并给出训练建议</div>
                    </div>
                    <button class="an-x" onclick="closeAnalysisPanel()" title="关闭">✕</button>
                </div>
                <div class="an-body" id="anBody"><div class="an-loading">分析中…</div></div>
                <div class="an-foot">
                    <button class="an-btn" onclick="openAnalysisPanel()">🔄 重新分析</button>
                    <div class="an-note">数据来源：本地 ⭐收藏（examFav）、🟡不熟 / 🔴不会（examStatus）标记 + 知识点分类树；分析依据：按知识点聚合「不会×3 +（不熟 + 收藏）×2」薄弱分降序分级，同分时收藏多的优先。<br>跳转刷题后回到本面板点「重新分析」，等级会随新标记实时更新。</div>
                </div>
            </div>`;
        mask.addEventListener('click', () => closeAnalysisPanel());
        document.body.appendChild(mask);
    }
    mask.classList.add('show');
    const body = document.getElementById('anBody');
    body.innerHTML = '<div class="an-loading">分析中…</div>';
    let data;
    try {
        data = await analysisBuild();
    } catch (e) {
        body.innerHTML = '<div class="an-empty">分析失败：' + anEsc(e.message) + '</div>';
        return;
    }
    const t = data.totals;
    if (!data.rows.length) {
        body.innerHTML = `<div class="an-ov">⭐收藏 ${t.fav} · 🟡不熟 ${t.unf} · 🔴不会 ${t.unk}</div>
            <div class="an-empty">还没有任何标记。先在真题页用 ☆ 收藏、或用「不熟 / 不会」标记题目，再回来分析。</div>`;
        return;
    }
    const high = data.rows.filter(r => r.level === 'high').length;
    const mid = data.rows.filter(r => r.level === 'mid').length;
    const low = data.rows.length - high - mid;
    const rowsHtml = data.rows.map((r, i) => `
        <div class="an-row an-${r.level}">
            <div class="an-rank">${i + 1}</div>
            <div class="an-info">
                <div class="an-name">${anEsc(r.name)}<span class="an-tag an-tag-${r.level}">${AN_LEVEL_TAG[r.level]}</span></div>
                <div class="an-path">${anEsc(r.path)}</div>
                <div class="an-stat">🔴 不会 ${r.unk} · 🟡 不熟 ${r.unf} · ⭐ 收藏 ${r.fav} · 共 ${r.total} 题 · 薄弱分 <b>${r.score}</b></div>
                <div class="an-advice">${anEsc(r.advice).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')}</div>
            </div>
            <button class="an-jump" onclick="analysisJump(${r.id})" title="打开分类页并定位到该知识点">🔁 跳转刷题</button>
        </div>`).join('');
    body.innerHTML = `
        <div class="an-ov">⭐收藏 <b>${t.fav}</b> · 🟡不熟 <b>${t.unf}</b> · 🔴不会 <b>${t.unk}</b> ｜ 涉及知识点 <b>${data.rows.length}</b> 个（🔴需加强 ${high} · 🟡关注 ${mid} · 🟢已跟踪 ${low}）</div>
        <div class="an-list">${rowsHtml}</div>`;
}

function closeAnalysisPanel() {
    const mask = document.getElementById('anMask');
    if (mask) mask.classList.remove('show');
}

/** 跳转到分类页并定位该知识点（新标签，便于对照刷题） */
function analysisJump(cid) {
    window.open('category.html?cid=' + cid, '_blank');
}
