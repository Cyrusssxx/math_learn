# -*- coding: utf-8 -*-
"""category.js：浮层新增「本级（不细分）」项 —— 直接挂在当前节点上的题（含回落到底的题），
   使浮层能覆盖该知识点的全部题，消除「明明 27 题却只有 4 题可见」的困惑。"""
import io

P = 'D:/ai code/math-note/pwa/js/category.js'
s = io.open(P, encoding='utf-8').read()
orig = s

# 1) 新增 curDeepSelf / _flyDirect 状态
s = s.replace(
    "let _flySub = {};            // 当前浮层使用的「按知识点」细分类计数表（sub）",
    "let _flySub = {};            // 当前浮层使用的「按知识点」细分类计数表（sub）\n"
    "let _flyDirect = {};         // 同上（direct：直接挂在该节点上的题数）\n"
    "let curDeepSelf = false;     // true = 只筛「本级」题（不含子树）", 1)

# 2) onCatNodeEnter：同时取 direct 表
s = s.replace(
    "    const { sub } = deepCountsForCat(catId);\n"
    "    if (!sub[root]) { scheduleHideDeepFly(60); return; }\n"
    "    _flySub = sub;",
    "    const { sub, direct } = deepCountsForCat(catId);\n"
    "    if (!sub[root]) { scheduleHideDeepFly(60); return; }\n"
    "    _flySub = sub;\n"
    "    _flyDirect = direct;", 1)

# 3) 浮层渲染：本级项（有直接挂在当前节点的题时显示，置顶）
s = s.replace(
    """    el.innerHTML = `<div class="deep-fly-hd" title="${esc(hd)}">${esc(hd)} · 下分支</div>` +
        (kids.length ? kids.map(c => {""",
    """    const selfCnt = _flyDirect[nodeId] || 0;
    const selfItem = selfCnt ? `<div class="deep-item deep-self${curDeepSelf && String(curDeepCat) === String(nodeId) ? ' on' : ''}"
                        data-deep-self="${nodeId}" title="只显示直接挂在本级的题目（未细分到下列分支）">
                        <span class="deep-item-name">▸ 本级（未细分）</span>
                        <span class="deep-item-cnt">${selfCnt}</span>
                    </div>` : '';
    el.innerHTML = `<div class="deep-fly-hd" title="${esc(hd)}">${esc(hd)} · 下分支</div>` + selfItem +
        (kids.length ? kids.map(c => {""", 1)

# 4) 浮层事件：本级项点击
s = s.replace(
    """    el.querySelectorAll('.deep-item').forEach(item => {""",
    """    el.querySelectorAll('.deep-item[data-deep-self]').forEach(item => {
        item.addEventListener('click', ev => { ev.stopPropagation(); selectDeepSelf(item.dataset.deepSelf); });
    });
    el.querySelectorAll('.deep-item[data-deep]').forEach(item => {""", 1)

# 5) selectDeepCat / clearDeepCat 复位 self 标志 + 新增 selectDeepSelf
s = s.replace(
    """function selectDeepCat(id) {
    curDeepCat = String(id);""",
    """function selectDeepSelf(id) {
    curDeepCat = String(id);
    curDeepSelf = true;      // 只筛本级
    hideDeepFlyNow();
    renderMain();
    renderNav();
}
function selectDeepCat(id) {
    curDeepCat = String(id);
    curDeepSelf = false;""", 1)
s = s.replace(
    """function clearDeepCat() {
    curDeepCat = null;""",
    """function clearDeepCat() {
    curDeepCat = null;
    curDeepSelf = false;""", 1)
s = s.replace(
    "    curDeepCat = null;   // 切知识点时退出细分类筛选",
    "    curDeepCat = null;   // 切知识点时退出细分类筛选\n    curDeepSelf = false;", 1)

# 6) renderMain：self 模式只取本级
s = s.replace(
    "    const deepSet = curDeepCat ? deepSubtreeSet(curDeepCat) : null;",
    "    const deepSet = curDeepCat ? (curDeepSelf ? new Set([String(curDeepCat)]) : deepSubtreeSet(curDeepCat)) : null;", 1)

# 7) 提示条：标明「本级」
s = s.replace(
    """    return `<div class="deep-filter-tip">🔎 细分类：<b>${esc(deepPath(curDeepCat))}</b>（${n != null ? n : 0} 题）""",
    """    return `<div class="deep-filter-tip">🔎 细分类：<b>${esc(deepPath(curDeepCat))}</b>${curDeepSelf ? '（本级·未细分）' : ''}（${n != null ? n : 0} 题）""", 1)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('改动生效:', s != orig)
for k in ('curDeepSelf', '_flyDirect', 'selectDeepSelf', 'data-deep-self'):
    print('  %-14s 出现 %d 次' % (k, s.count(k)))