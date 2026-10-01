# -*- coding: utf-8 -*-
"""修复：任意层级分类节点点击即显示其下全部题目（含后代），箭头单独负责折叠"""
import io, re

FP = 'pwa/js/category.js'
s = io.open(FP, encoding='utf-8').read()
orig = s

# ============ 1. 新增：节点自身 + 全部后代的 id 集合 ============
anchor = "// ============ 渲染：三级分类树 ============"
helper = """// ============ 节点聚合：自身 + 全部后代（点任意层级都能直接看到其下所有题） ============
function catSelfAndDescendants(cid) {
    const out = new Set([String(cid)]);
    const stack = [String(cid)];
    while (stack.length) {
        const cur = stack.pop();
        for (const k in cats) {
            const c = cats[k];
            if (String(c.parentId) === cur && !out.has(k)) { out.add(k); stack.push(k); }
        }
    }
    return out;
}
/** 当前选中的分类集合（缓存，renderMain/renderNav 共用） */
function curCatSet() {
    return curCat == null ? null : catSelfAndDescendants(curCat);
}

"""
assert anchor in s
s = s.replace(anchor, helper + anchor, 1)

# ============ 2. buildTree：学科节点补 id ============
old = "        if (!subjMap[subj.name]) subjMap[subj.name] = { chapters: {} };"
new = "        if (!subjMap[subj.name]) subjMap[subj.name] = { id: subj.id, name: subj.name, display: subj.display, chapters: {} };"
assert old in s
s = s.replace(old, new, 1)

# ============ 3. renderTree：学科头拆「箭头折叠 / 名称选题」 ============
old = """            <div class="paper-group-head" onclick="toggleSubject('${s.subject.replace(/'/g, "\\\\'")}')">
                <span class="paper-group-arrow">${open ? '▼' : '▶'}</span>
                <span class="paper-group-name">${s.subject}</span>
                <span class="paper-group-count">${total}</span>
            </div>"""
new = """            <div class="paper-group-head${String(curCat) === String(s.id) ? ' on' : ''}">
                <span class="paper-group-arrow" onclick="toggleSubject('${s.subject.replace(/'/g, "\\\\'")}')" title="展开/收起本学科">${open ? '▼' : '▶'}</span>
                <span class="paper-group-name" onclick="selectCat(${s.id})" title="查看本学科全部题目">${s.subject}</span>
                <span class="paper-group-count" onclick="selectCat(${s.id})">${total}</span>
            </div>"""
assert old in s, 'subject head'
s = s.replace(old, new, 1)

# ============ 4. renderTree：章节头拆「箭头折叠 / 名称选题」 ============
old = """                        <div class="cat-chapter-head${leafOn ? ' on' : ''}" onclick="toggleChapter(${ch.id})"${chHover} title="${ch.display || ch.name}${deepRootOfChapter(ch.id) ? '（悬停查看下分支）' : ''}">
                            <span class="cat-chapter-arrow">${copen ? '▾' : '▸'}</span>
                            <span class="cat-chapter-name">${ch.display || ch.name}</span>
                            <span class="cat-count">${ch.count}</span>
                        </div>"""
new = """                        <div class="cat-chapter-head${leafOn ? ' on' : ''}"${chHover} title="${ch.display || ch.name}${deepRootOfChapter(ch.id) ? '（悬停查看下分支）' : ''}">
                            <span class="cat-chapter-arrow" onclick="toggleChapter(${ch.id})" title="展开/收起本章">${copen ? '▾' : '▸'}</span>
                            <span class="cat-chapter-name" onclick="selectCat(${ch.id})" title="查看本章全部题目（含各知识点）">${ch.display || ch.name}</span>
                            <span class="cat-count" onclick="selectCat(${ch.id})">${ch.count}</span>
                        </div>"""
assert old in s, 'chapter head'
s = s.replace(old, new, 1)

# ============ 5. renderMain：按「自身 + 后代」过滤 ============
old = """    const entries = activeEntries().filter(e =>
        String(e.catId) === String(curCat) &&
        (!deepSet || (e.q.deepCats || []).some(id => deepSet.has(String(id)))));"""
new = """    const catSet = curCatSet();
    const entries = activeEntries().filter(e =>
        catSet.has(String(e.catId)) &&
        (!deepSet || (e.q.deepCats || []).some(id => deepSet.has(String(id)))));"""
assert old in s, 'renderMain filter'
s = s.replace(old, new, 1)

# ============ 6. renderNav：两处同样改为集合过滤 ============
n = s.count("activeEntries().filter(e => String(e.catId) === String(curCat))")
s = s.replace("activeEntries().filter(e => String(e.catId) === String(curCat))",
              "activeEntries().filter(e => curCatSet().has(String(e.catId)))")
print(f'renderNav 过滤替换 {n} 处')

# ============ 7. selectCat：点上层节点时自动展开，便于看到子节点 ============
old = """function selectCat(id) {
    curCat = id;
    curDeepCat = null;   // 切知识点时退出细分类筛选
    curDeepSelf = false;
    hideDeepFlyNow();"""
new = """function selectCat(id) {
    curCat = id;
    curDeepCat = null;   // 切知识点时退出细分类筛选
    curDeepSelf = false;
    hideDeepFlyNow();
    // 点上层节点（学科/章节）时自动展开，便于看到其子节点
    const node = cats[String(id)];
    if (node && node.level < 2) {
        if (node.level === 1) collapsedChapters.delete(Number(id));
        if (node.level === 0) collapsedSubjects.delete(node.name);
    }"""
assert old in s, 'selectCat'
s = s.replace(old, new, 1)

io.open(FP, 'w', encoding='utf-8', newline='').write(s)
print('category.js 修改完成，改动字节数:', len(s) - len(orig))
