/* 核心题库「收到核心题库」本地增补层
 * 作用：在分类题库页把任意题（真题/大观园/线代补充）一键收进「核心题库」。
 * 存储：localStorage（本机生效）；跨设备请用「导出核心增补」→ 提交到 core_bank.json。
 * 依赖：category.js 传入 catDeep（用于把 deepCats 叶子映射到章节目录）。
 */
(function () {
    'use strict';
    var KEY = 'coreExtraV1';
    var CHAP = { 2: '行列式', 3: '矩阵', 4: '向量', 5: '线性方程组', 6: '特征值与特征向量', 7: '二次型' };

    function load() {
        try {
            var a = JSON.parse(localStorage.getItem(KEY) || '[]');
            return Array.isArray(a) ? a : [];
        } catch (e) { return []; }
    }
    function save(a) {
        try { localStorage.setItem(KEY, JSON.stringify(a)); return true; }
        catch (e) { return false; }
    }
    // 去重签名：题源 + 题干（去空白前 120 字）
    function sig(q) {
        return String(q && q.source || '').trim() + '||' +
            String(q && q.stem || '').replace(/\s+/g, '').slice(0, 120);
    }
    function has(q) {
        var s = sig(q), a = load();
        for (var i = 0; i < a.length; i++) if (sig(a[i]) === s) return true;
        return false;
    }
    function nextNo(a) {
        var m = 9000;
        for (var i = 0; i < a.length; i++) if ((a[i].no || 0) > m) m = a[i].no;
        return m + 1;
    }
    function add(q, meta) {
        if (!q) return { ok: false, msg: '题目数据为空' };
        if (has(q)) return { ok: false, msg: '这道题已在核心题库增补里' };
        var a = load();
        var rec = JSON.parse(JSON.stringify(q));
        rec.no = nextNo(a);
        rec.custom = true;
        rec.addedAt = Date.now();
        rec.srcPaper = (meta && meta.paperId) || '';
        rec.srcNo = (meta && meta.srcNo) != null ? meta.srcNo : null;
        if (!rec.status) rec.status = 'transcribed';
        a.push(rec);
        if (!save(a)) return { ok: false, msg: '本地存储写入失败（可能空间不足）' };
        return { ok: true, no: rec.no };
    }
    function remove(no) {
        var a = load().filter(function (x) { return x.no !== no; });
        return save(a);
    }
    function clear() { return save([]); }
    function list() { return load(); }

    // deepCats 叶子 → 线代章名（高数章节沿用其顶层名，找不到返回 null）
    function chapterOf(leaf, nodes) {
        var c = String(leaf || ''), guard = 0;
        while (c && nodes && nodes[c] && guard++ < 24) {
            if (CHAP[c]) return CHAP[c];
            c = String(nodes[c].p || '');
        }
        return CHAP[c] || null;
    }

    // 把增补题并进核心题库（corePapers），返回并入条数
    function mergeInto(corePapers, catDeep) {
        if (!corePapers || !corePapers.length) return 0;
        var nodes = (catDeep && catDeep.nodes) || {};
        var secs = corePapers[0].sections || [];
        var exist = {};
        for (var i = 0; i < secs.length; i++)
            for (var j = 0; j < (secs[i].questions || []).length; j++)
                exist[sig(secs[i].questions[j])] = 1;
        var arr = load(), n = 0;
        for (var k = 0; k < arr.length; k++) {
            var q = arr[k];
            if (exist[sig(q)]) continue;
            var leaf = (q.deepCats || [])[0];
            var chap = chapterOf(leaf, nodes);
            var sec = null;
            for (var s = 0; s < secs.length; s++) if (secs[s].title === chap) { sec = secs[s]; break; }
            if (!sec) sec = secs[secs.length - 1];   // 章节未知 → 放最后一节，避免丢失
            if (!sec) continue;
            sec.questions.push(q);
            exist[sig(q)] = 1;
            n++;
        }
        return n;
    }

    function exportJson() {
        return JSON.stringify({ v: 1, at: new Date().toISOString(), items: load() }, null, 1);
    }
    function importJson(text) {
        var o = JSON.parse(text);
        var items = Array.isArray(o) ? o : (o && o.items) || [];
        var a = load(), added = 0;
        for (var i = 0; i < items.length; i++) {
            var q = items[i];
            if (!q || has(q)) continue;
            var rec = JSON.parse(JSON.stringify(q));
            rec.no = nextNo(a);
            rec.custom = true;
            a.push(rec); added++;
        }
        save(a);
        return added;
    }

    window.CoreExtra = {
        add: add, remove: remove, clear: clear, list: list, has: has,
        mergeInto: mergeInto, exportJson: exportJson, importJson: importJson, sig: sig
    };
})();
