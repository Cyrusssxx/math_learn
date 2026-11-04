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


/* ================= 场景 3：按「多久没碰」排序（2026-11-04 规则） =================
 * 口径：ageDays = 距 max(dailyMarks 最后一次动过, 收藏时间) 的天数
 *   —— 收藏时间必须有兜底，否则 2026-10-14 之前收藏的老题（dailyMarks 里没有记录）
 *      会被当成「从没动过」沉到最后，正好与「先做最久没做的」相反（用户 11-04 实际踩到）。 */
function dayKey(daysAgo) {
    const d = new Date();
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() - daysAgo);
    const p = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}
const agoMs = days => new Date(dayKey(days) + 'T00:00:00').getTime();

/* ---- 3a：三档时间 + 一支「今天刚收藏、从没标记过」的新题 ---- */
// 1-10 号：90 天前收藏、30 天前动过 → 30 天档
// 11-20 号：90 天前收藏、10 天前动过 → 10 天档
// 21-30 号：90 天前收藏、今天动过 → 0 天档
// 31-40 号：今天刚收藏、没有 dailyMarks → 也是 0 天档（收藏时间即「碰过」）
// 41 号：收藏记录没有时间戳（老格式）→ 完全无据 → 垫底
const kinds41 = new Array(41).fill('选择');
const fav41 = {};
for (let i = 1; i <= 40; i++) fav41['P1-' + i] = { t: (i <= 30 ? agoMs(90) : agoMs(0)) };
fav41['P1-41'] = 1;                    // 老格式收藏（无 t）
const seedAge = { papers: [mkPaper('P1', kinds41)], fav: fav41, st: {}, d30: dayKey(30), d10: dayKey(10), d0: dayKey(0) };

const TEST_AGE = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    const s = JSON.parse(__seed);
    const dm = {}; dm[s.d30] = {}; dm[s.d10] = {}; dm[s.d0] = {};
    for (let i = 1; i <= 10; i++) dm[s.d30]['P1-' + i] = 'unfamiliar';
    for (let i = 11; i <= 20; i++) dm[s.d10]['P1-' + i] = 'unfamiliar';
    for (let i = 21; i <= 30; i++) dm[s.d0]['P1-' + i] = 'unfamiliar';
    localStorage.setItem('dailyMarks', JSON.stringify(dm));

    const tiers = ppBuildPool();
    const all = tiers.fresh['选择'];
    window.__age1 = {
        池大小: all.length,
        d30: all.filter(it => it.ageDays === 30).length,
        d10: all.filter(it => it.ageDays === 10).length,
        d0: all.filter(it => it.ageDays === 0).length,
        无据: all.filter(it => it.ageDays < 0).length,
    };
    const picked = ppSampleTiered(tiers, '选择', 41, { br: {} });
    window.__age1.order = picked.map(it => it.ageDays);
    window.__age3 = { hasTf: 'tf' in all[0], w等于sw: all.every(it => it.w === it.sw) };
})();
`;
const sbAge = run(TEST_AGE, seedAge, true);
const a1 = sbAge.__age1, a3 = sbAge.__age3;

eq('时间档：池 41 题', a1.池大小, 41);
eq('时间档：30 天档 10 题', a1.d30, 10);
eq('时间档：10 天档 10 题', a1.d10, 10);
eq('新题按收藏时间入档：今天收藏的 10 题落在 0 天档', a1.d0, 20);
eq('完全无时间戳的 1 题判为无据', a1.无据, 1);
ok('时间优先：前 10 题 = 30 天档', a1.order.slice(0, 10).every(d => d === 30), JSON.stringify(a1.order.slice(0, 12)));
ok('时间优先：接着 10 题 = 10 天档', a1.order.slice(10, 20).every(d => d === 10), JSON.stringify(a1.order.slice(10, 22)));
ok('时间优先：再往后才是 0 天档', a1.order.slice(20, 40).every(d => d === 0), JSON.stringify(a1.order.slice(20, 25)));
eq('完全无据的那题垫底', a1.order[40], -1);
eq('旧字段 tf 已删除', a3.hasTf, false);
eq('权重 w = 状态权重 sw', a3.w等于sw, true);

/* ---- 3b：用户实际踩到的坑 —— 9 月初收藏、标了「不会」、dailyMarks 里没有记录 ---- */
// 1-4 号：65 天前收藏、无 dailyMarks、状态 不会   ← 应该最先抽
// 5-8 号：20 天前收藏、20 天前动过、状态 不会
const fav65 = {};
for (let i = 1; i <= 4; i++) fav65['P1-' + i] = { t: agoMs(65) };
for (let i = 5; i <= 8; i++) fav65['P1-' + i] = { t: agoMs(20) };
const st65 = {};
for (let i = 1; i <= 8; i++) st65['P1-' + i] = 'unknown';
const seed65 = { papers: [mkPaper('P1', new Array(8).fill('选择'))], fav: fav65, st: st65, d20: dayKey(20) };

const TEST_65 = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    localStorage.setItem('examStatus', JSON.stringify(JSON.parse(__seed).st));
    const s = JSON.parse(__seed);
    const dm = {}; dm[s.d20] = {};
    for (let i = 5; i <= 8; i++) dm[s.d20]['P1-' + i] = 'unknown';   // 只有 5-8 号有记录
    localStorage.setItem('dailyMarks', JSON.stringify(dm));
    const tiers = ppBuildPool();
    const picked = ppSampleTiered(tiers, '选择', 8, { br: {} });
    window.__old = { ages: picked.map(it => it.ageDays), qids: picked.map(it => it.qid) };
})();
`;
const oldT = run(TEST_65, seed65, true).__old;
eq('老收藏：8 题年龄（前 4 题应是 65 天）', oldT.ages.slice(0, 4), [65, 65, 65, 65]);
eq('老收藏：9 月初那批排在最前（qid 1-4）', oldT.qids.slice(0, 4).sort(), ['P1-1', 'P1-2', 'P1-3', 'P1-4']);

/* ---- 3c：收藏很久但今天刚标记过 → 视为「刚碰过」，不该优先 ---- */
// 1-2 号：60 天前收藏 + 今天标记过 → age 0
// 3-4 号：40 天前收藏、无 dailyMarks → age 40
const favToday = { 'P1-1': { t: agoMs(60) }, 'P1-2': { t: agoMs(60) }, 'P1-3': { t: agoMs(40) }, 'P1-4': { t: agoMs(40) } };
const seedToday = { papers: [mkPaper('P1', new Array(4).fill('选择'))], fav: favToday, st: {}, d0: dayKey(0) };
const TEST_TODAY = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    const s = JSON.parse(__seed);
    const dm = {}; dm[s.d0] = { 'P1-1': 'unknown', 'P1-2': 'unknown' };
    localStorage.setItem('dailyMarks', JSON.stringify(dm));
    const tiers = ppBuildPool();
    const picked = ppSampleTiered(tiers, '选择', 4, { br: {} });
    window.__td = { ages: picked.map(it => it.ageDays), qids: picked.map(it => it.qid) };
})();
`;
const td = run(TEST_TODAY, seedToday, true).__td;
eq('今天刚标记过的老收藏 → age 归零、排到最后', td.ages, [40, 40, 0, 0]);
eq('先抽 40 天前收藏、没再动过的两道', td.qids.slice(0, 2).sort(), ['P1-3', 'P1-4']);


/* ================= 场景 4：备注读写 + 刷新位置读写（2026-11-04） ================= */
const TEST_MISC = `
;(function () {
    // 备注：令牌原样存取；空内容删键
    ppNoteSet('C1', '<h2>失分点</h2>\\n第 3 题 符号算错');
    window.__note1 = ppNoteGet('C1');
    ppNoteSet('C1', '   ');
    window.__note2 = ppNoteGet('C1');
    window.__note3 = localStorage.getItem('ppNote-C1');

    // 刷新位置：拼卷模式下写 { id, y }
    ppCur = { id: 'C9', ts: 1, left: 1, items: [] };
    window.scrollY = 1234;
    ppPosSave();
    window.__pos = ppPosGet();
})();
`;
const sbMisc = run(TEST_MISC, {}, true);

eq('备注：令牌原样存取', sbMisc.__note1, '<h2>失分点</h2>\n第 3 题 符号算错');
eq('备注：空内容读回空串', sbMisc.__note2, '');
eq('备注：空内容删键', sbMisc.__note3, null);
eq('刷新位置：记下卷 id 与滚动值', sbMisc.__pos, { id: 'C9', y: 1234 });

console.log(`\n通过 ${pass} 项，失败 ${fail} 项`);
process.exit(fail ? 1 : 0);
