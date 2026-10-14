#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 common.js 的 exportAllData 升级为「含 IndexedDB 贴图」的全量导出，
   并追加 idbDump / idbRestore / importAllData（设备迁移用）。"""
import io

P = 'pwa/js/common.js'

NEW = r'''async function exportAllData() {
    const data = {};
    for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (k) data[k] = localStorage.getItem(k);
    }
    const cntKeys = (k) => { try { return Object.keys(JSON.parse(data[k] || '{}')).length; } catch (e) { return 0; } };
    const cntArr = (k) => { try { const a = JSON.parse(data[k] || '[]'); return Array.isArray(a) ? a.length : 0; } catch (e) { return 0; } };
    const cntPfx = (p) => Object.keys(data).filter(k => k.indexOf(p) === 0).length;

    // IndexedDB 全量（两个库都是「贴图」，Blob → dataURL 才能进 JSON）
    // notesAnnotImg = 笔记标注贴图 ｜ examNoteImg = 做题笔记贴图（category/exam/exam-shared 共用）
    const idb = {};
    try { idb['notesAnnotImg'] = await idbDump('notesAnnotImg', 'imgs'); } catch (e) { }
    try { idb['examNoteImg'] = await idbDump('examNoteImg', 'imgs'); } catch (e) { }
    const imgN = Object.keys(idb['examNoteImg'] || {}).length + Object.keys(idb['notesAnnotImg'] || {}).length;

    const summary = {
        '收藏': cntKeys('examFav'),
        '不熟/不会标记': cntKeys('examStatus'),
        '做题笔记': cntPfx('examNote-'),
        '每日做题': cntKeys('dailyMarks') + ' 天',
        '历史拼卷': cntArr('paperList') + ' 份',
        '好题收藏': cntKeys('goodFav') + ' 题',
        '精选收藏': cntPfx('selFav-') + ' 条',
        '笔记批注': data['notesAnnot'] ? '有' : '无',
        '贴图': imgN + ' 张',
        'localStorage 键总数': Object.keys(data).length,
    };
    const payload = {
        app: 'math-note',
        v: 2,
        exportedAt: new Date().toISOString(),
        note: '设备迁移用全量快照：localStorage 全部键 + IndexedDB 贴图（dataURL）。'
            + '用「导入数据」一键恢复。标注/记忆卡如需单独备份另有各自入口。',
        summary, data, idb,
    };
    const blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = '做题数据-' + dayKeyOf() + '.json';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 30000);
    const lines = Object.keys(summary).map(k => k + '：' + summary[k]).join('\n');
    alert('已导出「做题数据-' + dayKeyOf() + '.json」（'
        + (blob.size / 1048576).toFixed(1) + ' MB）\n\n' + lines
        + '\n\n换新设备：index 页点「导入数据」选这个文件即可。');
}

/* ---------- IndexedDB 读取 / 恢复（导出导入用） ---------- */
/** 读整个 store：{ key: dataURL 或原值 }。库不存在 / 出错一律返回空对象，不阻塞导出。 */
function idbDump(dbName, storeName) {
    return new Promise((resolve) => {
        try {
            const rq = indexedDB.open(dbName);
            rq.onerror = () => resolve({});
            rq.onsuccess = () => {
                const db = rq.result;
                try {
                    const os = db.transaction(storeName).objectStore(storeName);
                    const keysRq = os.getAllKeys();
                    keysRq.onerror = () => { db.close(); resolve({}); };
                    keysRq.onsuccess = () => {
                        const keys = keysRq.result || [];
                        const out = {};
                        if (!keys.length) { db.close(); resolve(out); return; }
                        let done = 0;
                        const fin = () => { if (++done === keys.length) { db.close(); resolve(out); } };
                        keys.forEach(k => {
                            const g = os.get(k);
                            g.onsuccess = () => {
                                const v = g.result;
                                if (v instanceof Blob) {
                                    const fr = new FileReader();
                                    fr.onload = () => { out[k] = fr.result; fin(); };
                                    fr.onerror = () => { out[k] = null; fin(); };
                                    fr.readAsDataURL(v);
                                } else { out[k] = v; fin(); }
                            };
                            g.onerror = () => { out[k] = null; fin(); };
                        });
                    };
                } catch (e) { try { db.close(); } catch (x) { } resolve({}); }
            };
        } catch (e) { resolve({}); }
    });
}
/** 把 { key: dataURL } 写回 store（清空旧数据，覆盖式，配合迁移场景）。 */
function idbRestore(dbName, storeName, records) {
    return new Promise((resolve) => {
        try {
            const rq = indexedDB.open(dbName, 1);
            rq.onupgradeneeded = () => rq.result.createObjectStore(storeName);
            rq.onerror = () => resolve(false);
            rq.onsuccess = () => {
                const db = rq.result;
                try {
                    const tx = db.transaction(storeName, 'readwrite');
                    const os = tx.objectStore(storeName);
                    os.clear();
                    const ids = Object.keys(records || {});
                    if (!ids.length) { db.close(); resolve(true); return; }
                    let pend = ids.length, fin2 = false;
                    const doneOne = () => { if (--pend === 0 && fin2) { db.close(); resolve(true); } };
                    tx.oncomplete = () => { fin2 = true; if (pend === 0) { db.close(); resolve(true); } };
                    ids.forEach(k => {
                        const v = records[k];
                        if (typeof v === 'string' && v.indexOf('data:') === 0) {
                            fetch(v).then(r => r.blob()).then(b => { os.put(b, k); doneOne(); })
                                .catch(() => { os.put(new Blob(), k); doneOne(); });
                        } else { os.put(v, k); doneOne(); }
                    });
                } catch (e) { try { db.close(); } catch (x) { } resolve(false); }
            };
        } catch (e) { resolve(false); }
    });
}
/** 导入：覆盖当前设备的做题数据（localStorage + 两个贴图库）。有确认弹窗。 */
async function importAllData(fileInput) {
    const f = fileInput && fileInput.files && fileInput.files[0];
    if (!f) return;
    let payload = null;
    try { payload = JSON.parse(await f.text()); } catch (e) { alert('文件不是合法 JSON，导入中止。'); return; }
    if (!payload || payload.app !== 'math-note' || !payload.data) {
        alert('这不是本站的导出文件（缺 app/data 字段），导入中止。'); return;
    }
    const s = payload.summary || {};
    const ok = confirm('将【覆盖】当前设备上的全部做题数据：\n\n'
        + '收藏：' + (s['收藏'] || '?') + '\n不熟/不会标记：' + (s['不熟/不会标记'] || '?')
        + '\n做题笔记：' + (s['做题笔记'] || '?') + '\n每日做题：' + (s['每日做题'] || '?')
        + '\n历史拼卷：' + (s['历史拼卷'] || '?') + '\n贴图：' + (s['贴图'] || '?')
        + '\n\n当前设备上的同名数据会被替换。建议先点「导出数据」留一份当前备份。\n\n确定导入？');
    if (!ok) return;
    localStorage.clear();
    for (const k in payload.data) localStorage.setItem(k, payload.data[k]);
    const idb = payload.idb || {};
    await idbRestore('notesAnnotImg', 'imgs', idb['notesAnnotImg'] || {});
    await idbRestore('examNoteImg', 'imgs', idb['examNoteImg'] || {});
    alert('导入完成！页面即将刷新。');
    setTimeout(() => location.reload(), 600);
}'''


def replace_func(src, name, new_body):
    key = 'function ' + name + '('
    start = src.index(key)
    i = start
    depth = 0
    end = None
    while i < len(src):
        ch = src[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1
    assert end, '没找到 ' + name + ' 的结束'
    return src[:start] + new_body + src[end:]


s = io.open(P, encoding='utf-8').read()
s = replace_func(s, 'exportAllData', NEW)
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('完成。common.js 现有', s.count('\n') + 1, '行')
print('含 idbDump:', 'idbDump' in s, '| idbRestore:', 'idbRestore' in s, '| importAllData:', 'importAllData' in s)
