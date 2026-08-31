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
