# -*- coding: utf-8 -*-
"""category.js 套卷化重排 + 掌握三态（6 处修改）"""
import io

p = 'pwa/js/category.js'
s = io.open(p, encoding='utf-8').read()

# ============ 1. catCard：q-head 加掌握 chip ============
old = """            ${st === 'unfamiliar' ? '<span class="q-mark-chip m-unfam" title="不熟">🟡 不熟</span>' : ''}
            ${st === 'unknown' ? '<span class="q-mark-chip m-unk" title="不会">🔴 不会</span>' : ''}"""
new = """            ${st === 'mastered' ? '<span class="q-mark-chip m-mst" title="已掌握">🟢 掌握</span>' : ''}
            ${st === 'unfamiliar' ? '<span class="q-mark-chip m-unfam" title="不熟">🟡 不熟</span>' : ''}
            ${st === 'unknown' ? '<span class="q-mark-chip m-unk" title="不会">🔴 不会</span>' : ''}"""
assert old in s, 'head chip'
s = s.replace(old, new)

# ============ 2. note sec 内按钮移除（编辑/保存统一由 q-ops 承担） ============
old = """    const noteHtml = hasNote
        ? `<div class="q-sec q-note${hasImg ? ' has-img' : ''}" data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml.replace('<div class=', '<div style="display:none" class=')}
            <div class="q-note-preview">${mdBlockWithImg(note)}</div>
            <button class="q-note-editbtn saved" onclick="toggleNoteEdit(this)" title="编辑笔记（编辑中点击保存）">✏️ 编辑</button>
            <div class="q-note-hint"></div>
        </div>`
        : `<div class="q-sec q-note" hidden data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml}
            <div class="q-note-preview" hidden></div>
            <button class="q-note-editbtn" onclick="toggleNoteEdit(this)" title="保存笔记并收起输入框">💾 保存</button>
            <div class="q-note-hint"></div>
        </div>`;"""
new = """    // 套卷形式：note 区内不放编辑/保存按钮，统一由 q-ops 的 ✏️编辑 按钮承担（与真题页同款）；
    // 输入框初始隐藏，由编辑按钮进入编辑态（与 exam.js noteHtml 一致）
    const noteHtml = hasNote
        ? `<div class="q-sec q-note${hasImg ? ' has-img' : ''}" data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml.replace('<div class=', '<div style="display:none" class=')}
            <div class="q-note-preview">${mdBlockWithImg(note)}</div>
            <div class="q-note-hint"></div>
        </div>`
        : `<div class="q-sec q-note" hidden data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml.replace('<div class=', '<div style="display:none" class=')}
            <div class="q-note-preview" hidden></div>
            <div class="q-note-hint"></div>
        </div>`;"""
assert old in s, 'noteHtml'
s = s.replace(old, new)

# ============ 3. q-head 加 📋LaTeX、新增 q-status-rail、q-ops 套卷重排 ============
old = """            ${yearHtml}
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="${fav ? (favTime(qid) ? '收藏于 ' + fmtFavTime(favTime(qid)) : '已收藏') : '收藏此题'}">${fav ? '⭐' : '☆'}</button>
        </div>
        <div class="q-body">${stem}${figHtml}${options}</div>
        <div class="q-ops">
            <button class="q-op" data-act="answer" onclick="toggleQSec(this,'answer')">查看答案</button>
            ${ideaBtn}
            ${tipsBtn}
            <button class="q-op${hasNote ? ' has' : ''}" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>
            <button class="q-op q-save-op" onclick="saveNoteFromOps(this)" title="保存当前笔记（编辑态可用）">💾 保存</button>
            <button class="q-st-btn q-st-unfam${st === 'unfamiliar' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unfamiliar')" title="标记为「不熟」（黄色；再点取消）">不熟</button>
            <button class="q-st-btn q-st-unk${st === 'unknown' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unknown')" title="标记为「不会」（红色；再点取消）">不会</button>
            <button class="q-copy-latex" onclick="copyCatQLatex(this)" title="复制本题 LaTeX 源码（题干+选项+答案，含 $...$ 原始命令）">📋 复制</button>
        </div>"""
new = """            ${yearHtml}
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="${fav ? (favTime(qid) ? '收藏于 ' + fmtFavTime(favTime(qid)) : '已收藏') : '收藏此题'}">${fav ? '⭐' : '☆'}</button>
            <button class="q-copy-latex" onclick="copyCatQLatex(this)" title="复制本题 LaTeX 源码（题干+选项+答案，含 $...$ 原始命令）">📋 LaTeX</button>
        </div>
        <div class="q-status-rail" data-qid="${qid}">
            <button class="q-st-btn q-st-mst${st === 'mastered' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','mastered')" title="标记为「掌握」（绿色；再点取消）">掌握</button>
            <button class="q-st-btn q-st-unfam${st === 'unfamiliar' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unfamiliar')" title="标记为「不熟」（黄色；再点取消）">不熟</button>
            <button class="q-st-btn q-st-unk${st === 'unknown' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unknown')" title="标记为「不会」（红色；再点取消）">不会</button>
        </div>
        <div class="q-body">${stem}${figHtml}${options}</div>
        <div class="q-ops">
            <button class="q-op" data-act="answer" onclick="toggleQSec(this,'answer')">查看答案</button>
            ${ideaBtn}
            ${tipsBtn}
            <button class="q-op${hasNote ? ' has' : ''}" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>
            <button class="q-op q-note-editbtn${hasNote ? ' saved' : ''}" onclick="toggleNoteEdit(this)" title="编辑笔记（编辑中点击保存）">✏️ 编辑</button>
        </div>"""
assert old in s, 'head/ops'
s = s.replace(old, new)

# ============ 4. toggleQStatus 三态 + chip 同步 + nav 刷新 ============
old = """function toggleQStatus(btn, qid, v) {
    const nv = toggleStatus(qid, v);
    const card = btn.closest('.q-card');
    if (card) {
        card.querySelectorAll('.q-st-btn').forEach(b => {
            const on = b.getAttribute('onclick').includes("'" + qid + "','" + (b.textContent.trim() === '不会' ? 'unknown' : 'unfamiliar') + "'");
            b.classList.remove('on');
        });
        if (nv) {
            const sel = nv === 'unknown' ? '.q-st-unk' : '.q-st-unfam';
            const b = card.querySelector(sel);
            if (b) b.classList.add('on');
        }
        // 若当前在"不熟/不会"筛选下被取消标记，题目应从列表消失
        if (markSel.unfamiliar && nv !== 'unfamiliar' && !markSel.unknown) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
        if (markSel.unknown && nv !== 'unknown' && !markSel.unfamiliar) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
    }
}"""
new = """function toggleQStatus(btn, qid, v) {
    const nv = toggleStatus(qid, v);
    const card = btn.closest('.q-card');
    if (card) {
        card.querySelectorAll('.q-st-btn').forEach(b => b.classList.remove('on'));
        if (nv) {
            const sel = nv === 'unknown' ? '.q-st-unk' : nv === 'mastered' ? '.q-st-mst' : '.q-st-unfam';
            const b = card.querySelector(sel);
            if (b) b.classList.add('on');
        }
        syncStatusChip(card, qid);   // 头部 chip（🟢掌握/🟡不熟/🔴不会）实时同步
        // 若当前在"不熟/不会"筛选下被取消标记，题目应从列表消失
        if (markSel.unfamiliar && nv !== 'unfamiliar' && !markSel.unknown) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
        if (markSel.unknown && nv !== 'unknown' && !markSel.unfamiliar) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
        renderNav();   // 题号球标记实时同步（🟢掌握/🟡不熟/🔴不会）
    }
}
/** 状态 chip 实时同步（点标记按钮即刷新头部徽标，不必整卡重渲染） */
function syncStatusChip(card, qid) {
    if (!card) return;
    card.querySelectorAll('.q-mark-chip.m-mst,.q-mark-chip.m-unfam,.q-mark-chip.m-unk').forEach(x => x.remove());
    const st = statusOf(qid);
    let html = '';
    if (st === 'mastered') html = '<span class="q-mark-chip m-mst" title="已掌握">🟢 掌握</span>';
    else if (st === 'unfamiliar') html = '<span class="q-mark-chip m-unfam" title="不熟">🟡 不熟</span>';
    else if (st === 'unknown') html = '<span class="q-mark-chip m-unk" title="不会">🔴 不会</span>';
    if (!html) return;
    const head = card.querySelector('.q-head');
    if (!head) return;
    const anchor = head.querySelector('.q-fav-date, .q-year, .q-fav, .q-copy-latex');
    if (anchor) anchor.insertAdjacentHTML('beforebegin', html);
    else head.insertAdjacentHTML('beforeend', html);
}"""
assert old in s, 'toggleQStatus'
s = s.replace(old, new)

# ============ 5. toggleNoteEdit：支持 q-ops 层按钮（自动展开笔记区） ============
old = """async function toggleNoteEdit(btn) {
    const sec = btn.closest('.q-note');
    const ta = sec.querySelector('.q-note-input');
    const pv = sec.querySelector('.q-note-preview');
    const editing = ta.style.display !== 'none';
    if (!editing) {
        // 进入编辑：同一按钮文字切为「💾 保存」（编辑态保持可见，点击即保存收起）
        btn.textContent = '💾 保存';"""
new = """async function toggleNoteEdit(btn) {
    // 与 exam.js 同款：按钮既可在 note 区内，也可在 q-ops 行（q-card 层）
    const card0 = btn.closest('.q-card');
    const sec = card0 ? card0.querySelector('.q-note') : btn.closest('.q-note');
    if (!sec) return;
    const ta = sec.querySelector('.q-note-input');
    const pv = sec.querySelector('.q-note-preview');
    const editing = ta.style.display !== 'none';
    if (!editing) {
        // 笔记区未展开：自动展开并同步「笔记」按钮高亮（q-ops 编辑按钮可一步进入编辑）
        if (sec.hidden) {
            sec.hidden = false;
            const nb = card0 && card0.querySelector('[data-act="note"]');
            if (nb) nb.classList.add('on');
            fillExamNoteImgs(ta);
            if (pv) fillExamNoteImgs(pv);
        }
        // 进入编辑：同一按钮文字切为「💾 保存」（编辑态保持可见，点击即保存收起）
        btn.textContent = '💾 保存';"""
assert old in s, 'toggleNoteEdit'
s = s.replace(old, new)

# ============ 6. renderNav 三态 ============
old = """        const st = stMap[no];
        const markCls = st ? (st === 'unknown' ? ' mark-unk' : ' mark-unf') : '';
        return `<button class="nav-q${markCls}" data-navq="${no}" title="${no} 题${st ? (st === 'unknown' ? '·🔴不会' : '·🟡不熟') : ''}" onclick="jumpToQ(${no})">${no}</button>`;"""
new = """        const st = stMap[no];
        const markCls = st ? (st === 'unknown' ? ' mark-unk' : st === 'mastered' ? ' mark-mst' : ' mark-unf') : '';
        const stTxt = st === 'unknown' ? '·🔴不会' : st === 'mastered' ? '·🟢掌握' : st === 'unfamiliar' ? '·🟡不熟' : '';
        return `<button class="nav-q${markCls}" data-navq="${no}" title="${no} 题${stTxt}" onclick="jumpToQ(${no})">${no}</button>`;"""
assert old in s, 'renderNav'
s = s.replace(old, new)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('category.js 6 处修改完成')
