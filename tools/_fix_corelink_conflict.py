# -*- coding: utf-8 -*-
"""修复 coreLink 题号冲突：core 与 xd 题号可能相同，均写无前缀键会互相覆盖，
   导致 qidOf('core', N) 取到别的题（xd）的真题 qid → 笔记/标记串题。
   同时把旧主键迁移函数改为直接用核心题库数据（不再依赖 coreLink 的键形式）。
"""
import io

FP = 'pwa/js/category.js'
s = io.open(FP, encoding='utf-8').read()
orig = s

# 1. core 构建：改为带前缀键
old = """            coreLink = {};
            for (const s of (corePapers[0] && corePapers[0].sections) || []) {
                for (const q of s.questions || []) {
                    if (q.linkedQid) coreLink[q.no] = q.linkedQid;   // 统一主键：真题 qid
                }
            }"""
new = """            coreLink = {};
            for (const s of (corePapers[0] && corePapers[0].sections) || []) {
                for (const q of s.questions || []) {
                    // 带 paperId 前缀，避免与 xd 的同号题互相覆盖（曾导致 qidOf 取到别的题的 qid）
                    if (q.linkedQid) coreLink['core-' + q.no] = q.linkedQid;
                }
            }"""
assert old in s, 'core build'
s = s.replace(old, new, 1)

# 2. xd 构建：移除无前缀覆盖行
old = """                    if (q.linkedQid) {
                        coreLink['xd-' + q.no] = q.linkedQid;
                        coreLink[q.no] = q.linkedQid;
                    }"""
new = """                    if (q.linkedQid) coreLink['xd-' + q.no] = q.linkedQid;"""
assert old in s, 'xd build'
s = s.replace(old, new, 1)

# 3. 迁移函数：改为遍历核心题库数据（q.no → linkedQid），与 coreLink 键形式解耦
old = """function migrateCoreLegacyKeys() {
    try {
        const entries = Object.entries(coreLink);
        if (!entries.length) return;
        const fav = favGet(), st = statusGet();
        let fC = false, sC = false;
        for (const [no, lq] of entries) {
            const oldKey = 'core-' + no;"""
new = """function migrateCoreLegacyKeys() {
    try {
        // 直接用核心题库数据（q.no → linkedQid），不依赖 coreLink 的键形式
        const pairs = [];
        for (const sec of (corePapers[0] && corePapers[0].sections) || []) {
            for (const q of sec.questions || []) {
                if (q.linkedQid) pairs.push([q.no, q.linkedQid]);
            }
        }
        if (!pairs.length) return;
        const fav = favGet(), st = statusGet();
        let fC = false, sC = false;
        for (const [no, lq] of pairs) {
            const oldKey = 'core-' + no;"""
assert old in s, 'migrate head'
s = s.replace(old, new, 1)

io.open(FP, 'w', encoding='utf-8', newline='').write(s)
print('category.js coreLink 冲突修复完成，字节变化:', len(s) - len(orig))
