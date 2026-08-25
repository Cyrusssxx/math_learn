/* 数学记忆卡片 PWA - Service Worker（改自 408 刷题 sw.js）
 * 预缓存全部页面/样式/脚本/笔记数据/KaTeX/图标，安装后完全离线可用。
 * 升级笔记数据或代码后：改 CACHE_VER 版本号即可让客户端自动换新缓存。
 */
const CACHE_VER = 'mathcards-9a41b16703';

const PRECACHE = [
    'index.html',
    'exam.html',
    'category.html',
    'good.html',
    'manifest.webmanifest',
    'css/notes.css',
    'css/exam.css',
    'css/category.css',
    'css/good.css',
    'js/common.js',
    'js/reader.js',
    'js/annotate.js',
    'js/exam.js',
    'js/category.js',
    'js/good.js',
    'selected.html',
    'selected_ans.html',
    'js/selected_ans.js',
    'css/selected_ans.css',
    'js/selected.js',
    'data/selected.json',
    'js/mdrender.js',
    'data/notes.json',
    'data/exam.json',
    'data/good.json',
    // 常见函数图形（30 张 SVG，共约 424KB）——预缓存后图形区秒开、离线可用
    'data/img/func_01_const_linear.svg',
    'data/img/func_02_quad.svg',
    'data/img/func_03_abs.svg',
    'data/img/func_04_reciprocal.svg',
    'data/img/func_05_power.svg',
    'data/img/func_06_exp.svg',
    'data/img/func_07_log.svg',
    'data/img/func_08_sin.svg',
    'data/img/func_09_cos.svg',
    'data/img/func_10_tan.svg',
    'data/img/func_11_arcsin.svg',
    'data/img/func_12_arccos.svg',
    'data/img/func_13_arctan.svg',
    'data/img/func_14_sgn.svg',
    'data/img/func_15_floor.svg',
    'data/img/func_16_duigou.svg',
    'data/img/func_17_hyperbolic.svg',
    'data/img/func_18_piecewise.svg',
    'data/img/func_19_lim_sinx_x.svg',
    'data/img/func_20_lim_exp_e.svg',
    'data/img/func_21_disc_removable.svg',
    'data/img/func_22_disc_jump.svg',
    'data/img/func_23_deriv_tangent.svg',
    'data/img/func_24_monotonic_extremum.svg',
    'data/img/func_25_concavity_inflection.svg',
    'data/img/func_26_rolle.svg',
    'data/img/func_27_lagrange.svg',
    'data/img/func_28_integral_area.svg',
    'data/img/func_29_variable_integral.svg',
    'data/img/func_30_ode_decay.svg',
    'data/img/exam_fig/2003_q04.png',
    'data/img/exam_fig/2005_q16.png',
    'data/img/exam_fig/2005_q17.png',
    'data/img/exam_fig/2007_q03.png',
    'data/img/exam_fig/2008_q02.png',
    'data/img/exam_fig/2008_q06.png',
    'data/img/exam_fig/2009_q06.png',
    'data/img/exam_fig/2009_q06_cd.png',
    'data/img/exam_fig/2010_q18.png',
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
            // 逐张缓存 + 失败跳过：避免 addAll 全有或全无——任一资源（如 GitHub Pages 上偶发超时的图片）
            // 失败就导致整个 install 失败、新版本不激活、旧缓存继续用（表现为部分图片加载异常）
            .then(cache => Promise.allSettled(
                PRECACHE.map(url => cache.add(url)
                    .catch(err => console.warn('[sw] 预缓存失败(跳过):', url, err && err.message)))
            ))
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
