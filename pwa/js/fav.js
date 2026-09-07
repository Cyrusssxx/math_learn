/* 真题收藏汇总页：跨全部套卷汇聚收藏题，支持排序/筛选/搜索与导出。
 * 依赖 js/exam-shared.js 提供的渲染、收藏、笔记贴图能力。
 * 数据源：data/exam.json（全量真题）+ data/exam_categories.json（知识点分组）
 */
let papers = [];
let catMap = null;
let favList = [];        // [{qid, paper, q, t}]
let sortBy = 'year';     // year | time | topic
let markSel = { fav: true, unfamiliar: true, unknown: true }; // 收藏 / 不熟 / 不会 多选筛选（默认全选，并集去重）
let keyword = '';
let hideAnswer = false;

// ============ 初始化 ============
async function initFav() {
    try {
        const [pResp, cResp] = await Promise.all([
            fetch('data/exam.json'),
            fetch('data/exam_categories.json').catch(() => null)
        ]);
        papers = await pResp.json();
        if (cResp && cResp.ok) catMap = await cResp.json();
    } catch (e) {
        document.getElementById('favBody').innerHTML = '<div class="empty-tip">数据加载失败：' + esc(String(e)) + '</div>';
        return;
    }
    buildFavList();
    renderFav();
}

// 构建候选池：收藏 ∪ 不熟 ∪ 不会（按 qid 去重，各来源独立标注；三选筛选在 visibleItems 做并集）
function buildFavList() {
    const favs = favGet();
    const statuses = statusGet();
    const pool = new Map();   // qid -> { qid, paper, q, t, fav, status }
    const push = (qid, srcFav, srcStatus) => {
        const idx = qid.lastIndexOf('-');
        if (idx < 0) return;
        const paperId = qid.slice(0, idx);
        const no = parseInt(qid.slice(idx + 1), 10);
        if (!Number.isFinite(no)) return;
        const paper = papers.find(p => p.id === paperId);
        if (!paper) return;                 // 套卷已下架等异常情况，跳过而非崩
        let q = null;
        for (const s of paper.sections || []) {
            const hit = (s.questions || []).find(x => x.no === no);
            if (hit) { q = hit; break; }
        }
        if (!q) return;
        const cur = pool.get(qid) || { qid, paper, q, t: 0, fav: false, status: null };
        if (srcFav) { cur.fav = true; const v = favs[qid]; cur.t = (v && typeof v === 'object') ? (v.t || 0) : 0; }
        if (srcStatus) cur.status = srcStatus;
        pool.set(qid, cur);
    };
    for (const qid of Object.keys(favs)) push(qid, true, null);
    for (const qid in statuses) push(qid, false, statuses[qid]);
    favList = [...pool.values()];
}

// ============ 筛选 / 排序 ============
function matchKw(item) {
    if (!keyword) return true;
    const k = keyword.toLowerCase();
    const q = item.q;
    const note = noteGet(item.qid);
    const hay = [q.stem, q.answer, q.idea, note, (q.options || []).join(' '),
    q.tips ? Object.values(q.tips).join(' ') : ''].filter(Boolean).join('\n').toLowerCase();
    return hay.includes(k);
}

function visibleItems() {
    // 三选筛选：勾选类别取并集（去重由 buildFavList 完成）；全不勾 → 空
    return favList.filter(it => {
        const m = markSel;
        const hit = (m.fav && it.fav) || (m.unfamiliar && it.status === 'unfamiliar') || (m.unknown && it.status === 'unknown');
        return hit && matchKw(it);
    });
}

function sortItems(list) {
    const arr = list.slice();
    if (sortBy === 'time') {
        arr.sort((a, b) => b.t - a.t);
    } else if (sortBy === 'topic') {
        arr.sort((a, b) => (chapterOf(a.q) === chapterOf(b.q)
            ? (String(b.paper.year).localeCompare(String(a.paper.year)) || a.q.no - b.q.no)
            : chapterOf(a.q).localeCompare(chapterOf(b.q), 'zh')));
    } else {
        arr.sort((a, b) => String(b.paper.year).localeCompare(String(a.paper.year)) || a.q.no - b.q.no);
    }
    return arr;
}

// 取题目所属「章」名（分类树 path 形如「线性代数 / 行列式 / 具体行列式计算」）
function chapterOf(q) {
    const ids = q.categoryIds || [];
    if (!ids.length || !catMap) return '未分类';
    const node = catMap[String(ids[0])];
    if (!node || !node.path) return '未分类';
    const parts = String(node.path).split(' / ');
    return parts.length > 1 ? parts[1] : (parts[0] || '未分类');
}

// ============ 渲染 ============
function renderFav() {
    const body = document.getElementById('favBody');
    const items = sortItems(visibleItems());

    const sub = document.getElementById('favSub');
    const cnt = document.getElementById('favCount');
    if (sub) sub.textContent = `收藏 ${favList.filter(i => i.fav).length} · 不熟 ${favList.filter(i => i.status === 'unfamiliar').length} · 不会 ${favList.filter(i => i.status === 'unknown').length} ｜ 当前显示 ${items.length} 题`;
    if (cnt) cnt.textContent = `${items.length} / ${favList.length}`;

    if (!favList.length) {
        body.innerHTML = '<div class="empty-tip">还没有收藏或标记任何题目。<br>回到真题页：点击题目右上角 ☆ 收藏，或点题右侧的「不熟/不会」打标记。</div>';
        return;
    }
    if (!items.length) {
        const on = Object.values(markSel).some(Boolean);
        body.innerHTML = on
            ? '<div class="empty-tip">当前筛选条件下没有匹配的题目。试试切换右上方「收藏/不熟/不会」筛选或清空搜索词。</div>'
            : '<div class="empty-tip">已取消全部筛选类别。请至少勾选「收藏 / 不熟 / 不会」中的一项。</div>';
        return;
    }

    let html = '';
    if (sortBy === 'year') {
        const groups = groupBy(items, it => it.paper.year + ' 年');
        html = groups.map(([k, arr]) => groupBlock(k, arr)).join('');
    } else if (sortBy === 'topic') {
        const groups = groupBy(items, it => chapterOf(it.q));
        html = groups.map(([k, arr]) => groupBlock(k, arr)).join('');
    } else {
        html = items.map(it => favCard(it)).join('');
    }
    body.innerHTML = html;

    renderMath(body);
    fillExamNoteImgs(body);
}

function groupBy(arr, keyFn) {
    const m = new Map();
    for (const it of arr) {
        const k = keyFn(it);
        if (!m.has(k)) m.set(k, []);
        m.get(k).push(it);
    }
    return [...m.entries()];
}

function groupBlock(title, arr) {
    return `<div class="fav-group"><div class="fav-group-hd">${esc(String(title))}<span class="fav-group-n">${arr.length} 题</span></div>`
        + arr.map(it => favCard(it)).join('') + '</div>';
}

// 只读题卡：默认全部展开（题干 + 答案 + 思路 + 点睛 + 笔记）
function favCard(item) {
    const { qid, paper, q, t, fav, status } = item;
    const kindTag = q.kind === 'choice' ? '选择' : (q.no >= 11 && q.no <= 16 ? '填空' : '解答');
    const stem = mdBlock(q.stem);
    const options = q.options && q.options.length
        ? `<div class="q-options">${q.options.map(o => `<div class="q-opt">${mdInline(o)}</div>`).join('')}</div>` : '';
    const note = noteGet(qid);
    const hasNote = !!note.trim();
    const hasImg = /\[图:[a-z0-9]+\]/.test(note);
    const noteHtml = hasNote
        ? `<div class="q-sec q-note${hasImg ? ' has-img' : ''}" data-qid="${qid}"><div class="q-note-preview">${mdBlockWithImg(note)}</div></div>` : '';
    const answerHtml = q.answer ? `<div class="q-sec q-answer"><div class="q-sec-hd">答案</div>${mdBlock(q.answer)}</div>` : '';
    const ideaHtml = q.idea ? `<div class="q-sec q-idea" data-copy-md="${copyMdAttr(q.idea)}"><div class="q-sec-hd">思路</div>${mdBlock(q.idea)}</div>` : '';

    const TIP_META = [['gs', '📌 公式'], ['yc', '⚠️ 易错'], ['jq', '💡 技巧'], ['zy', '🔍 注意']];
    let tipsHtml = '';
    if (q.tips) {
        const secs = TIP_META.filter(([k]) => q.tips[k])
            .map(([k, label]) => `<div class="q-tip-sec" data-copy-md="${copyMdAttr(q.tips[k])}" data-copy-key="${k}"><div class="q-tip-label">${label}</div><div class="q-tip-body">${mdBlock(q.tips[k])}</div></div>`).join('');
        if (secs) {
            const tipsJson = JSON.stringify(Object.fromEntries(Object.entries(q.tips).filter(([k]) => ['gs','yc','jq','zy'].includes(k) && q.tips[k])));
            tipsHtml = `<div class="q-sec q-tips" data-copy-tips="${copyMdAttr(tipsJson)}"><div class="q-sec-hd">点睛</div>${secs}</div>`;
        }
    }

    return `<div class="q-card" id="q-${qid}" data-qno="${q.no}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindTag}</span>
            <span class="fav-src">${esc(paper.year)} 年数二</span>
            ${fav ? `<span class="q-mark-chip m-fav" title="已收藏">📥 收藏</span>` : ''}
            ${status === 'unfamiliar' ? '<span class="q-mark-chip m-unfam" title="不熟">🟡 不熟</span>' : ''}
            ${status === 'unknown' ? '<span class="q-mark-chip m-unk" title="不会">🔴 不会</span>' : ''}
            ${fav && t ? `<span class="q-fav-date" title="收藏于 ${fmtFavTime(t)}">${fmtFavShort(t)}</span>` : ''}
            <span class="fav-actions">
                <a class="fav-act fav-goto" href="exam.html?paper=${encodeURIComponent(paper.id)}&no=${q.no}" target="_blank" title="在真题页打开此题（新标签页）">↗ 原题</a>
                ${fav
                    ? `<button class="fav-act fav-unfav" onclick="unfavFromList('${qid}')" title="取消收藏此题">⭐ 取消收藏</button>`
                    : `<button class="fav-act" onclick="favFromList('${qid}')" title="收藏此题">☆ 收藏</button>`}
            </span>
        </div>
        <div class="q-body">${stem}${options}</div>
        ${answerHtml}${ideaHtml}${tipsHtml}${noteHtml}
    </div>`;
}

// ============ 交互 ============
function onSortChange() {
    const sel = document.getElementById('sortSel');
    sortBy = sel ? sel.value : 'year';
    renderFav();
}
let _kwTimer = null;
function onSearchInput() {
    clearTimeout(_kwTimer);
    _kwTimer = setTimeout(() => {
        const el = document.getElementById('kwSearch');
        keyword = (el && el.value || '').trim();
        renderFav();
    }, 200);
}
// 标记筛选（收藏/不熟/不会 多选，默认全选；全不勾时给出提示）
function toggleMark(m) {
    markSel[m] = !markSel[m];
    document.querySelectorAll('.fav-mark').forEach(b => b.classList.toggle('on', markSel[b.dataset.m]));
    const box = document.getElementById('markFilter');
    if (box) box.classList.toggle('none-on', !Object.values(markSel).some(Boolean));
    renderFav();
}
// 汇总页内直接收藏（未收藏但打了标记的题也能顺手收藏）
function favFromList(qid) {
    const f = favGet();
    if (f[qid]) return;
    f[qid] = { t: Date.now() };
    favSave(f);
    buildFavList();
    renderFav();
}
// 汇总页内直接取消收藏：删 localStorage → 移出列表 → 重渲染（带确认防误点）
function unfavFromList(qid) {
    if (!confirm('确定取消收藏此题？')) return;
    const f = favGet();
    delete f[qid];
    favSave(f);
    buildFavList();
    renderFav();
}
function toggleHideAnswer() {
    hideAnswer = !hideAnswer;
    document.body.classList.toggle('hide-answer', hideAnswer);
    const b = document.getElementById('hideAnsBtn');
    if (b) { b.classList.toggle('on', hideAnswer); b.textContent = hideAnswer ? '👁 显示答案' : '🙈 隐藏答案'; }
}

// ============ 导出：PDF（浏览器原生打印）============
function exportPDF() {
    window.print();
}

// ============ 导出：Markdown（贴图 base64 内嵌，单文件）============
async function exportMarkdown() {
    // 导出范围：始终全部收藏（忽略年份筛选/搜索），与汇总页「所见」解耦
    const items = sortItems(favList);
    if (!items.length) { alert('还没有收藏任何题目，无法导出。'); return; }
    const includeImgs = confirm('是否内嵌笔记贴图？\n\n【确定】贴图以 base64 内嵌进 md（单文件最方便，但贴图多时文件会很大）\n【取消】不内嵌，贴图位置留一行说明文字');

    const lines = [];
    lines.push('# 真题收藏汇总');
    lines.push('');
    lines.push('> 导出时间：' + fmtFavTime(Date.now()));
    lines.push('> 共 ' + items.length + ' 题（全部收藏）');
    lines.push('> 排序：' + ({ year: '按年份', time: '按收藏时间', topic: '按知识点' })[sortBy]);
    lines.push('> 公式保留 LaTeX 源码，在支持数学渲染的编辑器（Obsidian / Typora）中可正常显示。');
    lines.push('');

    const pushQ = async (it) => {
        const q = it.q;
        const kindTag = q.kind === 'choice' ? '选择' : (q.no >= 11 && q.no <= 16 ? '填空' : '解答');
        lines.push('### 第 ' + q.no + ' 题（' + kindTag + '）· ' + it.paper.year + ' 年数二' + (it.t ? ' · 收藏于 ' + fmtFavTime(it.t) : ''));
        lines.push('');
        if (!hideAnswer) {
            if (q.options && q.options.length) { q.options.forEach(o => lines.push('- ' + o)); lines.push(''); }
        } else if (q.options && q.options.length) {
            q.options.forEach(o => lines.push('- ' + o)); lines.push('');
        }
        lines.push(q.stem || '');
        lines.push('');
        if (!hideAnswer) {
            if (q.answer) { lines.push('**【答案】**'); lines.push(''); lines.push(q.answer); lines.push(''); }
            if (q.idea) { lines.push('**【思路】**'); lines.push(''); lines.push(q.idea); lines.push(''); }
            if (q.tips) {
                const T = [['gs', '公式'], ['yc', '易错'], ['jq', '技巧'], ['zy', '注意']];
                const parts = T.filter(([k]) => q.tips[k]).map(([k, label]) => '- **' + label + '**：' + q.tips[k]);
                if (parts.length) { lines.push('**【点睛】**'); lines.push(''); parts.forEach(p => lines.push(p)); lines.push(''); }
            }
        }
        const note = noteGet(it.qid);
        if (note.trim()) {
            lines.push('**【我的笔记】**');
            lines.push('');
            lines.push(await noteWithImages(note, includeImgs));
            lines.push('');
        }
        lines.push('---');
        lines.push('');
    };

    if (sortBy === 'year' || sortBy === 'topic') {
        const keyFn = sortBy === 'year' ? (it => it.paper.year + ' 年') : (it => chapterOf(it.q));
        for (const [k, arr] of groupBy(items, keyFn)) {
            lines.push('## ' + k + '（' + arr.length + ' 题）');
            lines.push('');
            for (const it of arr) await pushQ(it);
        }
    } else {
        for (const it of items) await pushQ(it);
    }

    const blob = new Blob([lines.join('\n')], { type: 'text/markdown;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = '真题收藏汇总-' + new Date().toISOString().slice(0, 10) + '.md';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 3000);
}

// 把笔记里的 [图:id] 替换为 base64 data URI（或占位说明）
async function noteWithImages(note, includeImgs) {
    const ids = [...note.matchAll(/\[图:([a-z0-9]+)\]/g)].map(m => m[1]);
    if (!ids.length) return note;
    if (!includeImgs) {
        return note.replace(/\[图:[a-z0-9]+\]/g,
            () => '\n\n（此处有 1 张笔记贴图，导出时未包含）\n\n');
    }
    let out = note;
    for (const id of ids) {
        let dataUri = null;
        try {
            const blob = await examImgGet(id);
            if (blob) dataUri = await blobToDataURL(blob);
        } catch (e) { /* 读不到就留占位 */ }
        out = out.replace('[图:' + id + ']', dataUri ? '![](' + dataUri + ')' : '（笔记贴图读取失败）');
    }
    return out;
}

function blobToDataURL(blob) {
    return new Promise((res, rej) => {
        const r = new FileReader();
        r.onload = () => res(r.result);
        r.onerror = rej;
        r.readAsDataURL(blob);
    });
}

// 收藏在别的标签页变化时，回到本页自动刷新
window.addEventListener('storage', e => {
    if (e.key === 'examFav' || e.key === 'examStatus') { buildFavList(); renderFav(); }
});

initFav();
