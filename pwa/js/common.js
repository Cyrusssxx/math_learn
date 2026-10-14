/* 数学记忆卡片 - 前端通用JS：夜间模式 + 今日学习计时器（改自 408 刷题 common.js） */

// ============ 夜间模式：尽早给 <html> 加 .dark，减少闪白 ============
function isDarkOn() {
    return localStorage.getItem('darkMode') === '1';
}

function applyDark() {
    document.documentElement.classList.toggle('dark', isDarkOn());
}

applyDark();

// ============ 接管浏览器的滚动恢复 ============
// 浏览器默认 scrollRestoration='auto'，刷新后会自行把页面滚回「刷新前的位置」，
// 与页面自己用 localStorage 做的定位（真题题号 / 笔记章节+滚动量）互相覆盖，表现为：
//   F5 普通刷新 → 浏览器的恢复后执行并赢，看不到跳转（甚至停在顶部）
//   Ctrl+Shift+R 强刷 → Chrome 硬性重载不做滚动恢复（重置到顶部），只剩 JS 定位生效 → 看到「自动跳转」
// 这里统一切成 manual，滚动位置完全交给各页面自己的逻辑，两种刷新行为一致。
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

// ============ 今日学习计时器（按天累计，存localStorage，页面不可见时暂停） ============
(function () {
    const el = document.getElementById('navTimer');
    if (!el) return;

    const today = new Date().toISOString().slice(0, 10);
    if (localStorage.getItem('studyTimerDate') !== today) {
        localStorage.setItem('studyTimerDate', today);
        localStorage.setItem('studyTimerSec', '0');
    }

    function fmt(sec) {
        const h = String(Math.floor(sec / 3600)).padStart(2, '0');
        const m = String(Math.floor(sec % 3600 / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        return `${h}:${m}:${s}`;
    }

    function render() {
        el.textContent = '⏱ ' + fmt(parseInt(localStorage.getItem('studyTimerSec') || '0', 10));
    }

    render();
    setInterval(() => {
        if (document.hidden) return;  // 切走标签页/窗口时暂停计时
        const sec = parseInt(localStorage.getItem('studyTimerSec') || '0', 10) + 1;
        localStorage.setItem('studyTimerSec', String(sec));
        render();
    }, 1000);
})();

// ============ 夜间模式开关（样式全部由 CSS .dark 接管） ============
function renderDarkSwitch() {
    const btn = document.getElementById('darkSwitch');
    const state = document.getElementById('darkState');
    if (!btn || !state) return;
    const on = isDarkOn();
    btn.classList.toggle('on', on);
    state.textContent = on ? '开' : '关';
}

function toggleDark() {
    localStorage.setItem('darkMode', isDarkOn() ? '0' : '1');
    applyDark();
    renderDarkSwitch();
}

renderDarkSwitch();

// ============ Service Worker 注册 + 新版本自动刷新 ============
// 部署新版本后，旧 SW 仍控制当前页面；这里监听新 SW 激活并自动重载，
// 避免「强刷一次还是旧版」的困扰（SW 双刷新问题）。
(function registerSW() {
    if (!('serviceWorker' in navigator)) return;
    let reloaded = false;
    // 仅当页面原本就已被 SW 控制（即部署前的旧版本）时，才在 controllerchange 后重载，
    // 避免「首次访问 SW 刚 claim」也触发一次多余刷新。
    const wasControlled = !!navigator.serviceWorker.controller;
    function showUpdateBanner(reg) {
        if (document.getElementById('swUpdateBanner')) return;
        const b = document.createElement('div');
        b.id = 'swUpdateBanner';
        b.innerHTML = '发现新版本，<a href="#" id="swUpdateReload">点击刷新</a>';
        b.setAttribute('style', 'position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:9999;' +
            'background:var(--accent,#2b8a6b);color:#fff;padding:8px 14px;border-radius:8px;' +
            'cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.25);font-size:14px');
        b.querySelector('#swUpdateReload').addEventListener('click', e => {
            e.preventDefault();
            if (reg && reg.waiting) reg.waiting.postMessage({ type: 'SKIP_WAITING' });
            location.reload();
        });
        document.body.appendChild(b);
    }
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js').then(reg => {
            reg.addEventListener('updatefound', () => {
                const nw = reg.installing;
                if (!nw) return;
                nw.addEventListener('statechange', () => {
                    if (nw.state === 'installed' && navigator.serviceWorker.controller) showUpdateBanner(reg);
                });
            });
            if (reg.waiting && navigator.serviceWorker.controller) showUpdateBanner(reg);
        }).catch(err => console.warn('SW 注册失败（file:// 下属正常）:', err));
        // 新 SW 接管后自动重载一次，确保拿到最新资源（仅限原本已被控制的页面）
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (reloaded || !wasControlled) return;
            reloaded = true;
            location.reload();
        });
    });
})();

// ============ 思路/点睛 → 批注可粘贴格式（全局 copy 拦截） ============
// 需求：真题页「思路/点睛」手动框选复制到批注笔记时，希望少换行、公式可再渲染为图形。
// 实现：渲染侧 .q-idea / .q-tip-sec 挂 data-copy-md（源 md），.q-tips 挂 data-copy-tips（{段key:md}）。
//       用户在此类容器内复制（含整块跨段框选）时，改写剪贴板为「批注友好 HTML/纯文本」：
//         - **粗体** → <b>（批注保存后为 <b> 令牌，查看加粗）
//         - 每个逻辑行一个 <div>（批注序列化时每块单换行、无多余空行/大段留白）
//         - $...$ / $$...$$ 公式保留源码 —— 批注预览/查看即渲染成公式图形，且可再编辑
// 供各页渲染端挂 data-copy-md / data-copy-tips 用的属性转义（含双引号）
window.copyMdAttr = function (md) {
    return String(md).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
};
// 笔记图片令牌提取（[图:id] → id 数组）。放在 common.js 供真题页/分类页/收藏页共用——
// 原先只在 exam.js 定义，分类页 noteInput 落盘回调调用它会抛 ReferenceError，
// 导致自动保存整段中断（localStorage 不写入、预览不刷新）＝「连续粘贴图片看不到效果」。
window.examImgRefs = function (t) {
    return [...(t || '').matchAll(/\[图:([a-z0-9]+)\]/g)].map(m => m[1]);
};
(function () {
    var TIP_LABEL = { gs: '公式', yc: '易错', jq: '技巧', zy: '注意' };
    function escC(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    // 行内处理：转义 → 公式占位保护 → **加粗** → 还原公式
    function lineToAnnotHtml(line) {
        var h = escC(line);
        var math = [];
        h = h.replace(/(\$\$[\s\S]*?\$\$|\$[^$\n]*?\$)/g, function (m) {
            math.push(m);
            return '\u0000' + (math.length - 1) + '\u0000';
        });
        h = h.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
        h = h.replace(/\u0000(\d+)\u0000/g, function (m, i) { return math[+i]; });
        return h;
    }
    // md → annotate 粘贴 HTML（每非空逻辑行一个 div；顺带在 md 里剥掉多余段落）
    function mdToAnnotHtml(md) {
        if (!md) return '';
        var divs = [];
        String(md).split('\n').forEach(function (raw) {
            var l = raw.trim();
            if (!l) return;
            divs.push('<div>' + lineToAnnotHtml(l) + '</div>');
        });
        return divs.join('');
    }
    // 找选区锚点/终点都落在的「最近批注源容器」
    function srcBox(sel) {
        var node = function (n) { return n && n.nodeType === 3 ? n.parentElement : n; };
        var a = node(sel.anchorNode), f = node(sel.focusNode);
        if (!a || !f) return null;
        var aBox = a.closest('[data-copy-md],[data-copy-tips]');
        var fBox = f.closest('[data-copy-md],[data-copy-tips]');
        if (!aBox || !fBox) return null;
        // 同一容器；或分处不同 q-tip-sec 但同属一个 .q-tips（整块点睛）→ 用 q-tips 容器
        if (aBox === fBox) return aBox;
        var aTips = aBox.closest('.q-tips'), fTips = fBox.closest('.q-tips');
        if (aTips && aTips === fTips) return aTips;
        return null;
    }
    // 组装该容器的批注 HTML：idea=单 md；tip-sec=label+单段；q-tips=整块各段
    function boxToAnnotHtml(box) {
        var tips = box.dataset ? box.dataset.copyTips : null;
        if (tips) {
            var obj = {};
            try { obj = JSON.parse(tips); } catch (e) { obj = {}; }
            var out = [];
            ['gs', 'yc', 'jq', 'zy'].forEach(function (k) {
                var md = obj[k];
                if (!md) return;
                out.push('<div><b>' + (TIP_LABEL[k] || k) + '</b>：</div>' + mdToAnnotHtml(md));
            });
            return out.join('');
        }
        if (box.dataset && box.dataset.copyKey) {   // 单段点睛（带标签）
            var label = TIP_LABEL[box.dataset.copyKey] || box.dataset.copyKey;
            return '<div><b>' + label + '</b>：</div>' + mdToAnnotHtml(box.dataset.copyMd || '');
        }
        return mdToAnnotHtml(box.dataset ? (box.dataset.copyMd || '') : '');
    }

    document.addEventListener('copy', function (e) {
        var sel = window.getSelection && window.getSelection();
        if (!sel || sel.isCollapsed || !sel.rangeCount) return;
        var box = srcBox(sel);
        if (!box) return;               // 思路/点睛外：保持系统默认复制
        // 全选（≥85%）→ 改写为「批注友好」格式；部分选择 → 提取选区内 LaTeX 源码
        // （KaTeX 渲染后的字形不含源码，直接复制粘贴到编辑面板无法再渲染；
        //   把选中的 .katex 还原为 $...$ / $$...$$，文字保持原样，让用户自由复制片段）
        var full = (box.textContent || '').replace(/\s+/g, ' ').trim();
        var part = (String(sel) || '').replace(/\s+/g, ' ').trim();
        if (full && part.length < full.length * 0.85) {
            e.preventDefault();
            var rng = sel.getRangeAt(0);
            // 选区边界落在公式内部时，扩展到完整 .katex（半个公式无法还原）
            function edgeKatex(node) {
                var el = node && node.nodeType === 3 ? node.parentElement : node;
                var k = el && el.closest ? el.closest('.katex') : null;
                return (k && box.contains(k)) ? k : null;
            }
            var sk = edgeKatex(rng.startContainer);
            if (sk) { try { rng.setStartBefore(sk); } catch (e2) { } }
            var ek = edgeKatex(rng.endContainer);
            if (ek) { try { rng.setEndAfter(ek); } catch (e2) { } }
            var tmp2 = document.createElement('div');
            tmp2.appendChild(rng.cloneContents());
            Array.prototype.forEach.call(tmp2.querySelectorAll('.katex'), function (k) {
                var ann = k.querySelector('annotation[encoding="application/x-tex"]');
                var tex = ann ? ann.textContent : '';
                if (!tex) return;
                var disp = !!k.closest('.katex-display');
                k.parentNode.replaceChild(document.createTextNode(disp ? '$$' + tex + '$$' : '$' + tex + '$'), k);
            });
            var text2 = (tmp2.textContent || '').replace(/[ \t]+/g, ' ').replace(/ ?\n ?/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
            try {
                if (e.clipboardData && e.clipboardData.setData) {
                    e.clipboardData.setData('text/plain', text2);
                    e.clipboardData.setData('text/html', tmp2.innerHTML);
                }
            } catch (err) { }
            return;
        }
        e.preventDefault();
        var html = boxToAnnotHtml(box);
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        // 纯文本按「行」拆分（div 间换行），避免长段落全粘在一起
        var parts = [];
        Array.prototype.forEach.call(tmp.querySelectorAll('div'), function (d) { parts.push(d.textContent); });
        if (!parts.length) parts.push(tmp.textContent || '');
        var plain = parts.join('\n').replace(/\n{3,}/g, '\n\n');
        try {
            e.clipboardData.setData('text/html', '<meta charset="utf-8">' + html);
            e.clipboardData.setData('text/plain', plain);
        } catch (err) { /* 个别浏览器只读剪贴板时静默 */ }
    });
})();

// ============ 右栏「本页目录」向左收起（笔记站 index.html） ============
// 过渡全部交给 CSS（.toc transform/opacity + .doc margin-right，均 .15s），
// 这里只切换 body 类与按钮状态，避免 JS 分阶段改样式造成动画抖动。
const TOC_COLLAPSED_KEY = 'notesTocCollapsed';
function applyTocCollapsed(collapsed) {
    const btn = document.getElementById('tocCollapse');
    if (!btn) return;   // 非笔记站页面：不做任何处理
    document.body.classList.toggle('toc-collapsed', collapsed);
    btn.textContent = collapsed ? '‹' : '›';
    btn.title = collapsed ? '展开目录' : '收起目录';
    btn.setAttribute('aria-label', collapsed ? '展开目录' : '收起目录');
}
function toggleTocCollapse() {
    const collapsed = !document.body.classList.contains('toc-collapsed');
    try { localStorage.setItem(TOC_COLLAPSED_KEY, collapsed ? '1' : '0'); } catch (e) { }
    applyTocCollapsed(collapsed);
}
(function restoreTocCollapsed() {
    try {
        if (localStorage.getItem(TOC_COLLAPSED_KEY) === '1') applyTocCollapsed(true);
    } catch (e) { }
})();

// ============ 左栏「文件目录树」向左收起（笔记站 index.html） ============
// 同样只切 body 类，动画交给 CSS（.sidebar transform + .doc margin-left，均 .15s）
const SIDE_COLLAPSED_KEY = 'notesSideCollapsed';
function applySideCollapsed(collapsed) {
    const btn = document.getElementById('sideCollapse');
    if (!btn) return;
    document.body.classList.toggle('side-collapsed', collapsed);
    btn.textContent = collapsed ? '›' : '‹';
    btn.title = collapsed ? '展开目录' : '收起目录';
    btn.setAttribute('aria-label', collapsed ? '展开目录' : '收起目录');
}
function toggleSideCollapse() {
    const collapsed = !document.body.classList.contains('side-collapsed');
    try { localStorage.setItem(SIDE_COLLAPSED_KEY, collapsed ? '1' : '0'); } catch (e) { }
    applySideCollapsed(collapsed);
}
(function restoreSideCollapsed() {
    try {
        if (localStorage.getItem(SIDE_COLLAPSED_KEY) === '1') applySideCollapsed(true);
    } catch (e) { }
})();

// ============ 每日做题数据（2026-10-14）============
// localStorage 'dailyMarks' = { 'YYYY-MM-DD': { qid: 'unknown'|'unfamiliar'|'cleared'|'fav'|'unfav' } }
// 用途：掌握地图置顶显示「每天做了多少题」的打卡数据。
// ⚠️ **只在用户主动操作路径调用**（各页的 toggleStatus / toggleFav）。
//    绝不能改成在 statusSave/favSave 里拦截 —— 那两个函数有 9 处调用，
//    其中 4 处是数据迁移（migrateXxx），会把「搬家」误记成「今天做了题」。
// ⚠️ 同一天同一题只占一条（后写覆盖先写）：计数口径 = 当天做过的**题数**（按 qid 去重）。
// ⚠️ 三处副本都要调用：category.js / exam.js / exam-shared.js 各有一份 toggleStatus·toggleFav。
const DAILY_KEY = 'dailyMarks';
const DAILY_KEEP = 120;               // 只保留最近 120 天，防 localStorage 膨胀

function dailyGet() {
    try { return JSON.parse(localStorage.getItem(DAILY_KEY)) || {}; } catch (e) { return {}; }
}
function dailySave(d) {
    try { localStorage.setItem(DAILY_KEY, JSON.stringify(d)); } catch (e) { }
}
/** 本地日期键 YYYY-MM-DD（用本地时区；别用 toISOString —— 那是 UTC，晚上会差一天） */
function dayKeyOf(ts) {
    const d = ts ? new Date(ts) : new Date();
    const p = n => (n < 10 ? '0' : '') + n;
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}
/** 记一笔「今天动过这道题」。kind 仅用于细分展示，计数按 qid 去重。 */
function markDaily(qid, kind) {
    if (!qid) return;
    const d = dailyGet();
    const k = dayKeyOf();
    if (!d[k]) d[k] = {};
    d[k][qid] = kind;
    const keys = Object.keys(d).sort();
    if (keys.length > DAILY_KEEP) {
        for (const old of keys.slice(0, keys.length - DAILY_KEEP)) delete d[old];
    }
    dailySave(d);
}
/** 最近 n 天的每日题数（从旧到新，含今天）。返回 [{ day:'MM-DD', key:'YYYY-MM-DD', n, by:{unknown,unfamiliar,fav}}] */
function dailyRecent(n) {
    const d = dailyGet();
    const out = [];
    const today = new Date();
    for (let i = n - 1; i >= 0; i--) {
        const dt = new Date(today.getFullYear(), today.getMonth(), today.getDate() - i);
        const key = dayKeyOf(dt);
        const rec = d[key] || {};
        const by = { unknown: 0, unfamiliar: 0, fav: 0 };
        let cnt = 0;
        for (const qid in rec) {
            cnt++;
            const v = rec[qid];
            if (v === 'unknown') by.unknown++;
            else if (v === 'unfamiliar') by.unfamiliar++;
            else if (v === 'fav') by.fav++;
        }
        const p = x => (x < 10 ? '0' : '') + x;
        out.push({ day: p(dt.getMonth() + 1) + '-' + p(dt.getDate()), key, n: cnt, by });
    }
    return out;
}
/** 连续打卡天数（从今天往前数，今天为 0 也能算「断签」前的连续段） */
function dailyStreak() {
    const d = dailyGet();
    const today = new Date();
    let streak = 0;
    for (let i = 0; i < 400; i++) {
        const dt = new Date(today.getFullYear(), today.getMonth(), today.getDate() - i);
        const n = Object.keys(d[dayKeyOf(dt)] || {}).length;
        if (n > 0) streak++;
        else if (i > 0) break;      // 今天还没做不算断（从昨天继续数）
    }
    return streak;
}

// ============ 全量导出做题数据（2026-10-14）============
// 为什么**不做白名单**：键名散落在 10+ 个 js 文件里，且大量键是动态拼的
// （examNote-<qid>、selFav-<id>、selNote-<id>…），白名单必漏。
// 同源下 localStorage 里只有本 app 的数据，**全量导出最稳**。
// ⚠️ 不含 IndexedDB 里的图片（笔记贴图在 imgs store；标注/记忆卡另有各自的导出入口）。
async function exportAllData() {
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
    try { idb['notesAnnotImg'] = await Promise.race([idbDump('notesAnnotImg', 'imgs'), new Promise(r => setTimeout(() => r({}), 4000))]); } catch (e) { }
    try { idb['examNoteImg'] = await Promise.race([idbDump('examNoteImg', 'imgs'), new Promise(r => setTimeout(() => r({}), 4000))]); } catch (e) { }
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
    const race = new Promise((resolve) => {
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
    return Promise.race([race, new Promise(r => setTimeout(() => r({}), 3000))]);
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
                    setTimeout(() => { fin2 = true; if (pend === 0) { db.close(); resolve(true); } }, 500);
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
}
