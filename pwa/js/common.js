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
