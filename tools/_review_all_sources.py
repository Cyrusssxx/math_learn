# -*- coding: utf-8 -*-
"""复测列表改用「全来源」条目（真题 + 核心题库 + 线代 + 大观园），
   避免 review 只看到当前数据源的标记题。"""
import io

JS = 'pwa/js/category.js'
s = io.open(JS, encoding='utf-8').read()

# 1. 新增全来源条目函数（放在复测模块开头）
anchor = "function rvCardHtml(r) { return catCard(r.paper, r.secTitle, r.q); }"
helper = '''/** 复测用：合并全部来源的题目（真题卷 + 核心题库 + 线代重点题 + 大观园真题），
    不受当前「数二真题 / 核心题库」切换影响，保证所有标记题都能出现在复测页 */
function allEntriesAllSources() {
    const out = [];
    const pushPapers = (papers) => {
        for (const p of (papers || [])) {
            for (const sec of (p.sections || [])) {
                for (const q of (sec.questions || [])) out.push({ paper: p, secTitle: sec.title, q });
            }
        }
    };
    pushPapers(examPapers);
    pushPapers(corePapers);
    for (const list of [xdItems, bankItems]) {
        for (const e of (list || [])) out.push({ paper: e.paper, secTitle: e.secTitle || '', q: e.q });
    }
    return out;
}

'''
assert anchor in s
s = s.replace(anchor, helper + anchor, 1)

# 2. renderReview 遍历改为全来源
old = """    for (const e of allEntries) {
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null, f = !!fav[qid];
        if (!s && !f) continue;
        if (seen.has(qid)) continue;     // 同题多来源（真题/核心题库同源）只保留一条
        seen.add(qid);
        rows.push({ paper: e.paper, secTitle: e.secTitle, q: e.q, qid, st: s, fav: f });
    }"""
new = """    for (const e of allEntriesAllSources()) {
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null, f = !!fav[qid];
        if (!s && !f) continue;
        if (seen.has(qid)) continue;     // 同题多来源（真题/核心题库同源）只保留一条
        seen.add(qid);
        rows.push({ paper: e.paper, secTitle: e.secTitle, q: e.q, qid, st: s, fav: f });
    }"""
assert old in s, 'renderReview 遍历源'
s = s.replace(old, new, 1)

io.open(JS, 'w', encoding='utf-8', newline='').write(s)
print('category.js：复测列表已改为全来源（exam + core + xd + bank）')
