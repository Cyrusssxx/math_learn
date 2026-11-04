// 拼卷抽题进度 / 「抽过不再抽」回归测试
// 用法: node tools/_test_pp_counter.js
// 做法：把 category.js 整段丢进 vm（截掉末尾的 init()，避免真去操作 DOM），
//       配假题库 + 假 localStorage，直接跑 ppScanPool / ppBuildPool / ppBuild / ppProgHtml。
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const SRC_PATH = process.env.PP_TEST_SRC || path.join(__dirname, '..', 'pwa', 'js', 'category.js');
const SRC = fs.readFileSync(SRC_PATH, 'utf8');
const CUT = SRC.indexOf('init().catch(');
if (CUT < 0) { console.error('✗ 找不到 init() 调用，测试文件需要更新'); process.exit(1); }
const BODY = SRC.slice(0, CUT);

let pass = 0, fail = 0;
function eq(name, got, want) {
    if (JSON.stringify(got) === JSON.stringify(want)) { pass++; }
    else { fail++; console.log(`✗ ${name}\n    得到 ${JSON.stringify(got)}\n    期望 ${JSON.stringify(want)}`); }
}
function ok(name, cond, extra) {
    if (cond) { pass++; } else { fail++; console.log('✗ ' + name + (extra ? '\n    ' + extra : '')); }
}

/* ---------- 假环境 ---------- */
function makeStore() {
    const m = new Map();
    return {
        getItem: k => (m.has(k) ? m.get(k) : null),
        setItem: (k, v) => m.set(k, String(v)),
        removeItem: k => m.delete(k),
        clear: () => m.clear(),
    };
}
function noop() { }
function makeDoc() {
    const el = () => ({
        innerHTML: '', textContent: '', hidden: true, style: {},
        classList: { add: noop, remove: noop, toggle: noop, contains: () => false },
        querySelector: () => null, querySelectorAll: () => [], appendChild: noop, remove: noop,
        setAttribute: noop, getAttribute: () => null, closest: () => null, insertBefore: noop,
    });
    return {
        getElementById: () => null, querySelector: () => null, querySelectorAll: () => [],
        createElement: el, addEventListener: noop, removeEventListener: noop,
        body: { classList: { add: noop, remove: noop, toggle: noop }, appendChild: noop },
        documentElement: { classList: { add: noop, remove: noop, toggle: noop } },
    };
}

/** 在 vm 里跑 category.js + 测试片段；seed 会被注入为 __seed（JSON 字符串） */
function run(testCode, seed, withDaily) {
    const sandbox = {
        console, setTimeout, clearTimeout, setInterval, clearInterval,
        URLSearchParams, JSON, Math, Date, Set, Map, Array, Object, String, Number, Boolean, RegExp, isNaN, parseInt, parseFloat,
        localStorage: makeStore(),
        document: makeDoc(),
        location: { search: '?paper=1', href: 'http://localhost/category.html?paper=1', hash: '' },
        navigator: { userAgent: 'node', clipboard: {} },
        alert: noop, confirm: () => true, prompt: () => null,
        fetch: () => Promise.reject(new Error('no network in test')),
        requestAnimationFrame: fn => setTimeout(fn, 0),
        matchMedia: () => ({ matches: false, addEventListener: noop, addListener: noop }),
        getComputedStyle: () => ({ getPropertyValue: () => '' }),
        IntersectionObserver: function () { this.observe = noop; this.disconnect = noop; },
        __seed: JSON.stringify(seed || {}),
    };
    sandbox.window = sandbox;
    sandbox.globalThis = sandbox;
    sandbox.scrollY = 0;
    sandbox.scrollTo = noop;
    sandbox.addEventListener = noop;
    vm.createContext(sandbox);
    // common.js 的 dailyGet：测试环境不加载 common.js，按需注入一份等价实现
    const DAILY_STUB = withDaily
        ? "function dailyGet(){try{return JSON.parse(localStorage.getItem('dailyMarks')||'{}');}catch(e){return {};}}\n"
        : '';
    vm.runInContext(DAILY_STUB + BODY + '\n' + testCode, sandbox, { filename: 'category.js' });
    return sandbox;
}

/* ---------- 造题 ---------- */
function mkPaper(id, kinds, year) {
    const qs = kinds.map((k, i) => ({
        no: i + 1,
        kind: k === '选择' ? 'choice' : k === '填空' ? 'blank' : 'calc',
        stem: '题' + (i + 1),
        options: k === '选择' ? ['A', 'B'] : [],
        categoryIds: [1],
    }));
    return { id, year: year || '', title: id, sections: [{ title: '题目', questions: qs }] };
}

/* ================= 场景 1：60 题，20 不会 / 20 不熟 / 20 仅收藏 ================= */
const kinds60 = [];
for (let i = 0; i < 60; i++) kinds60.push(i % 4 === 0 ? '解答' : (i % 3 === 0 ? '填空' : '选择'));
const papers60 = [mkPaper('P1', kinds60, '2020')];
const fav60 = {}, st60 = {};
for (let i = 0; i < 60; i++) {
    const qid = 'P1-' + (i + 1);
    fav60[qid] = { t: 1000 + i };
    if (i < 20) st60[qid] = 'unknown';
    else if (i < 40) st60[qid] = 'unfamiliar';
}

const TEST1 = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    localStorage.setItem('examStatus', JSON.stringify(JSON.parse(__seed).st));

    // ① 统计
    const s1 = ppScanPool().stats;
    window.__r1 = { u: s1.unknown, f: s1.unfamiliar, p: s1.plain, noFav: s1.noFav, n: ppScanPool().items.length };

    // ② 全都还没抽过 → 60 题可入池
    window.__r2 = ppScanPool().items.filter(it => it.d === 0).length;

    // ③ 手工把 10 道「不会」记为已抽
    const dr = {};
    for (let i = 1; i <= 10; i++) dr['P1-' + i] = { d: 1, ld: Date.now() };
    localStorage.setItem('qDraw', JSON.stringify(dr));
    const s2 = ppScanPool().stats;
    const pool2 = ppBuildPool();
    const poolAll = pool2.fresh['选择'].concat(pool2.fresh['填空'], pool2.fresh['解答']);
    window.__r3 = { uDrawn: s2.unknown.drawn, uAll: s2.unknown.all, poolHasDrawn: poolAll.filter(it => it.d > 0).length, poolSize: poolAll.length };

    // ④ 连拼 3 卷：卷与卷之间不得出现同一 qid
    localStorage.setItem('qDraw', '{}');
    const seen = new Set(); const perPaper = [];
    let dup = 0;
    for (let t = 0; t < 3; t++) {
        const rec = ppBuild(22);
        perPaper.push(rec.items.length);
        for (const it of rec.items) { if (seen.has(it.qid)) dup++; seen.add(it.qid); }
        const d2 = JSON.parse(localStorage.getItem('qDraw') || '{}');
        for (const it of rec.items) { const r = d2[it.qid] || { d: 0 }; r.d++; r.ld = Date.now(); d2[it.qid] = r; }
        localStorage.setItem('qDraw', JSON.stringify(d2));
    }
    window.__r4 = { perPaper, dup, unique: seen.size };

    // ⑤ 抽干后：池空 + 计数器归零 + 提示
    const d3 = {};
    for (let i = 1; i <= 60; i++) d3['P1-' + i] = { d: 1, ld: Date.now() };
    localStorage.setItem('qDraw', JSON.stringify(d3));
    const s3 = ppScanPool().stats;
    window.__r5 = {
        rest: (s3.unknown.all - s3.unknown.drawn) + (s3.unfamiliar.all - s3.unfamiliar.drawn) + (s3.plain.all - s3.plain.drawn),
        items: ppBuild(22).items.length,
        html: ppProgHtml(),
    };

    // ⑥ 标了不会但没收藏 → 不进池，但计入 noFav
    const fav2 = JSON.parse(localStorage.getItem('examFav'));
    delete fav2['P1-1'];
    localStorage.setItem('examFav', JSON.stringify(fav2));
    window.__r6 = ppScanPool().stats;
})();
`;

const sb = run(TEST1, { papers: papers60, fav: fav60, st: st60 });
const r1 = sb.__r1, r2 = sb.__r2, r3 = sb.__r3, r4 = sb.__r4, r5 = sb.__r5, r6 = sb.__r6;

eq('① 统计：不会 20 题', r1.u, { all: 20, drawn: 0 });
eq('① 统计：不熟 20 题', r1.f, { all: 20, drawn: 0 });
eq('① 统计：仅收藏 20 题', r1.p, { all: 20, drawn: 0 });
eq('① 统计：无「未收藏的标记题」', r1.noFav, { unknown: 0, unfamiliar: 0 });
eq('① 池内题数 60', r1.n, 60);
eq('② 未抽的可入池 60 题', r2, 60);

eq('③ 「不会」已抽 10 题', r3.uDrawn, 10);
eq('③ 「不会」总数仍 20', r3.uAll, 20);
eq('③ 已抽的题被排除出池', r3.poolHasDrawn, 0);
eq('③ 池子缩到 50 题', r3.poolSize, 50);

ok('④ 第 1 卷满 22 题', r4.perPaper[0] === 22, '实际 ' + r4.perPaper[0]);
ok('④ 卷与卷零重复', r4.dup === 0, '重复 ' + r4.dup + ' 题');
ok('④ 三卷总量 ≤ 60 且逐卷递减', r4.perPaper.reduce((a, b) => a + b, 0) <= 60 && r4.perPaper[1] <= r4.perPaper[0], JSON.stringify(r4.perPaper));
eq('④ 去重后题数 = 三卷之和', r4.unique, r4.perPaper.reduce((a, b) => a + b, 0));

eq('⑤ 抽干后剩余 0', r5.rest, 0);
eq('⑤ 抽干后拼不出卷', r5.items, 0);
ok('⑤ 计数器显示「剩 0 题」+「已抽完」', /剩 <b>0<\/b>/.test(r5.html) && /已抽完/.test(r5.html), r5.html.slice(0, 160));
ok('⑤ 计数器三行齐全', /不会/.test(r5.html) && /不熟/.test(r5.html) && /仅收藏/.test(r5.html));

eq('⑥ 未收藏的「不会」计入 noFav', r6.noFav.unknown, 1);
eq('⑥ 未收藏的「不会」不进池', r6.unknown.all, 19);

/* ================= 场景 2：计数器渲染细节 ================= */
const kinds5 = ['选择', '填空', '解答', '解答', '选择'];
const fav5 = {}, st5 = {};
for (let i = 0; i < 5; i++) fav5['P1-' + (i + 1)] = { t: 1000 + i };
st5['P1-1'] = 'unknown'; st5['P1-2'] = 'unknown'; st5['P1-3'] = 'unfamiliar';

const TEST2 = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    localStorage.setItem('examStatus', JSON.stringify(JSON.parse(__seed).st));
    localStorage.setItem('qDraw', JSON.stringify({ 'P1-1': { d: 1, ld: Date.now() } }));
    window.__html = ppProgHtml();
})();
`;
const html = run(TEST2, { papers: [mkPaper('P1', kinds5)], fav: fav5, st: st5 }).__html;

ok('计数器：不会 已抽 1 / 未抽 1',
    /<span class="pp-pg-lab">不会<\/span><span class="pp-pg-n">1<\/span><span class="pp-pg-n rest">1<\/span>/.test(html), html);
ok('计数器：总计「剩 4 题」', /剩 <b>4<\/b>/.test(html), html);
ok('计数器：含进度条', /pp-pg-bar"><i style="width:20%"><\/i>/.test(html), html);


/* ================= 场景 3：按「多久没做」排序（2026-11-04 新规则） ================= */
function dayKey(daysAgo) {
    const d = new Date();
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() - daysAgo);
    const p = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}
// 40 道选择题：1-10 号 30 天前动过、11-20 号 10 天前、21-30 号今天、31-40 号从没动过
const kinds40 = new Array(40).fill('选择');
const fav40 = {};
for (let i = 1; i <= 40; i++) fav40['P1-' + i] = { t: 1000 + i };   // 收藏时间：越靠后越晚（旧逻辑会偏爱前面的）
const seedAge = { papers: [mkPaper('P1', kinds40)], fav: fav40, st: {}, d30: dayKey(30), d10: dayKey(10), d0: dayKey(0) };

const TEST_AGE = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    // 只有 1-30 号有「动过」记录，31-40 号从没动过
    const s = JSON.parse(__seed);
    const dm = {};
    dm[s.d30] = {}; dm[s.d10] = {}; dm[s.d0] = {};
    for (let i = 1; i <= 10; i++) dm[s.d30]['P1-' + i] = 'unfamiliar';
    for (let i = 11; i <= 20; i++) dm[s.d10]['P1-' + i] = 'unfamiliar';
    for (let i = 21; i <= 30; i++) dm[s.d0]['P1-' + i] = 'unfamiliar';
    localStorage.setItem('dailyMarks', JSON.stringify(dm));

    const tiers = ppBuildPool();
    const picked = ppSampleTiered(tiers, '选择', 22, { br: {} });
    window.__age1 = {
        n: picked.length,
        前10天档: picked.slice(0, 10).map(it => it.ageDays),
        中10天档: picked.slice(10, 20).map(it => it.ageDays),
        后2天档: picked.slice(20).map(it => it.ageDays),
        有没有没动过的: picked.filter(it => it.ageDays < 0).length,
    };
    // 全池 40 题里各档的数量
    window.__age2 = {
        d30: tiers.fresh['选择'].filter(it => it.ageDays === 30).length,
        d10: tiers.fresh['选择'].filter(it => it.ageDays === 10).length,
        d0: tiers.fresh['选择'].filter(it => it.ageDays === 0).length,
        never: tiers.fresh['选择'].filter(it => it.ageDays < 0).length,
    };
    // 旧字段 tf 应已删除
    window.__age3 = { hasTf: 'tf' in tiers.fresh['选择'][0], w等于sw: tiers.fresh['选择'].every(it => it.w === it.sw) };
})();
`;
const sbAge = run(TEST_AGE, seedAge, true);
const a1 = sbAge.__age1, a2 = sbAge.__age2, a3 = sbAge.__age3;

eq('时间档：池内 30 天档 10 题', a2.d30, 10);
eq('时间档：池内 10 天档 10 题', a2.d10, 10);
eq('时间档：池内 今天档 10 题', a2.d0, 10);
eq('时间档：池内 无记录 10 题', a2.never, 10);
eq('时间优先：抽 22 题', a1.n, 22);
ok('时间优先：前 10 题全是 30 天前的', a1.前10天档.every(d => d === 30), JSON.stringify(a1.前10天档));
ok('时间优先：接着 10 题是 10 天前的', a1.中10天档.every(d => d === 10), JSON.stringify(a1.中10天档));
ok('时间优先：最后 2 题才轮到今天的', a1.后2天档.every(d => d === 0), JSON.stringify(a1.后2天档));
eq('时间优先：从没动过的排最后，一个没抽到', a1.有没有没动过的, 0);
eq('旧字段 tf 已删除', a3.hasTf, false);
eq('权重 w = 状态权重 sw', a3.w等于sw, true);

/* ---- 场景 3b：旧题不够时才轮到「从没动过」 ---- */
const seedMix = { papers: [mkPaper('P1', new Array(10).fill('选择'))], fav: (() => { const f = {}; for (let i = 1; i <= 10; i++) f['P1-' + i] = { t: 1000 + i }; return f; })(), st: {}, d40: dayKey(40) };
const TEST_MIX = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    const s = JSON.parse(__seed);
    const dm = {}; dm[s.d40] = {};
    for (let i = 1; i <= 5; i++) dm[s.d40]['P1-' + i] = 'unknown';   // 只有 1-5 号动过
    localStorage.setItem('dailyMarks', JSON.stringify(dm));
    const tiers = ppBuildPool();
    const picked = ppSampleTiered(tiers, '选择', 6, { br: {} });
    window.__mix = { ages: picked.map(it => it.ageDays), n: picked.length };
})();
`;
const mix = run(TEST_MIX, seedMix, true).__mix;
eq('混合池：抽 6 题', mix.n, 6);
ok('混合池：先抽 5 道 40 天前的', mix.ages.slice(0, 5).every(d => d === 40), JSON.stringify(mix.ages));
ok('混合池：第 6 题才是从没动过的', mix.ages[5] === -1, JSON.stringify(mix.ages));

console.log(`\n通过 ${pass} 项，失败 ${fail} 项`);
process.exit(fail ? 1 : 0);
