/* 数学记忆卡片 PWA - Service Worker（改自 408 刷题 sw.js）
 * 预缓存全部页面/样式/脚本/笔记数据/KaTeX/图标，安装后完全离线可用。
 * 升级笔记数据或代码后：改 CACHE_VER 版本号即可让客户端自动换新缓存。
 */
const CACHE_VER = 'mathcards-ca394204f6';

const PRECACHE = [
    'index.html',
    'exam.html',
    'good.html',
    'manifest.webmanifest',
    'css/notes.css',
    'css/exam.css',
    'css/good.css',
    'js/common.js',
    'js/reader.js',
    'js/annotate.js',
    'js/exam.js',
    'js/good.js',
    'js/mdrender.js',
    'data/notes.json',
    'data/exam.json',
    'data/good.json',
    'vendor/katex/katex.min.css',
    'vendor/katex/katex.min.js',
    'vendor/katex/auto-render.min.js',
    'vendor/katex/fonts/KaTeX_AMS-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Caligraphic-Bold.woff2',
    'vendor/katex/fonts/KaTeX_Caligraphic-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Fraktur-Bold.woff2',
    'vendor/katex/fonts/KaTeX_Fraktur-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Main-Bold.woff2',
    'vendor/katex/fonts/KaTeX_Main-BoldItalic.woff2',
    'vendor/katex/fonts/KaTeX_Main-Italic.woff2',
    'vendor/katex/fonts/KaTeX_Main-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Math-BoldItalic.woff2',
    'vendor/katex/fonts/KaTeX_Math-Italic.woff2',
    'vendor/katex/fonts/KaTeX_SansSerif-Bold.woff2',
    'vendor/katex/fonts/KaTeX_SansSerif-Italic.woff2',
    'vendor/katex/fonts/KaTeX_SansSerif-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Script-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Size1-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Size2-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Size3-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Size4-Regular.woff2',
    'vendor/katex/fonts/KaTeX_Typewriter-Regular.woff2',
    'icons/icon-192.png',
    'icons/icon-512.png'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_VER)
            .then(cache => cache.addAll(PRECACHE))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys()
            .then(keys => Promise.all(keys.filter(k => k !== CACHE_VER).map(k => caches.delete(k))))
            .then(() => self.clients.claim())
    );
});

// cache-first：离线优先；缓存未命中再走网络并回填（KaTeX 字体靠这里回填缓存）
self.addEventListener('fetch', (e) => {
    if (e.request.method !== 'GET') return;
    e.respondWith(
        caches.match(e.request, { ignoreSearch: true }).then(hit => {
            if (hit) return hit;
            return fetch(e.request).then(resp => {
                if (resp.ok && new URL(e.request.url).origin === location.origin) {
                    const clone = resp.clone();
                    caches.open(CACHE_VER).then(cache => cache.put(e.request, clone));
                }
                return resp;
            });
        })
    );
});
