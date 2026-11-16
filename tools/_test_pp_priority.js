// 拼卷抽题「状态硬优先」回归测试
// 规则：不会/不熟(hot) 全部抽完之前，绝不抽仅收藏(plain)；新标记的 hot 也压过老 plain。
// 用法: node tools/_test_pp_priority.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const SRC = fs.readFileSync(path.join(__dirname, '..', 'pwa', 'js', 'category.js'), 'utf8');
const CUT = SRC.indexOf('init().catch(');
const BODY = SRC.slice(0, CUT);

let pass = 0, fail = 0;
function ok(name, cond, extra) {
    if (cond) pass++;
    else { fail++; console.log('✗ ' + name + (extra ? '\n    ' + extra : '')); }
}

function makeStore() {
    const m = new Map();
    return {
        getItem: k => (m.has(k) ? m.get(k) : null),
        setItem: (k, v) => m.set(k, String(v)),
        removeItem: k => m.delete(k), clear: () => m.clear(),
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
function run(testCode, seed) {
    const sandbox = {
        console, setTimeout, clearTimeout, setInterval, clearInterval,
        URLSearchParams, JSON, Math, Date, Set, Map, Array, Object, String, Number, Boolean, RegExp, isNaN, parseInt, parseFloat,
        localStorage: makeStore(), document: makeDoc(),
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
    sandbox.window = sandbox; sandbox.globalThis = sandbox;
    sandbox.scrollY = 0; sandbox.scrollTo = noop; sandbox.addEventListener = noop;
    vm.createContext(sandbox);
    const DAILY_STUB = "function dailyGet(){try{return JSON.parse(localStorage.getItem('dailyMarks')||'{}');}catch(e){return {};}}\n";
    vm.runInContext(DAILY_STUB + BODY + '\n' + testCode, sandbox, { filename: 'category.js' });
    return sandbox;
}

function mkPaper(kinds, year) {
    const qs = kinds.map((k, i) => ({
        no: i + 1,
        kind: k === '选择' ? 'choice' : k === '填空' ? 'blank' : 'calc',
        stem: '题' + (i + 1), options: k === '选择' ? ['A', 'B'] : [], categoryIds: [1],
    }));
    return { id: 'P', year: year || '', title: 'P', sections: [{ title: '题目', questions: qs }] };
}

/* ===== 场景 1：hot(10) 与 plain(30)，plain 全是最久没碰（ageDays 很大），hot 是今天新标（ageDays=0）
   期望：连抽多卷，30 个 plain 一个都不能先于 hot 被抽；hot 抽完后才轮到 plain。 ===== */
const K = 40;
const kinds = [];
for (let i = 0; i < K; i++) kinds.push(i % 3 === 0 ? '解答' : (i % 3 === 1 ? '填空' : '选择'));
const fav = {}, st = {}, daily = {};
const NOW = Date.now();
for (let i = 0; i < K; i++) {
    const qid = 'P-' + (i + 1);
    fav[qid] = { t: NOW - 1000 };
    if (i < 10) {
        // 前 10 题 = hot，今天新标记（收藏时间很近 → ageDays=0）
        st[qid] = i % 2 === 0 ? 'unknown' : 'unfamiliar';
        fav[qid] = { t: NOW };
    } else {
        // 后 30 题 = plain，30~60 天前收藏（ageDays 很大）
        fav[qid] = { t: NOW - (30 + (i - 10)) * 864e5 };
    }
}
const seed = { papers: [mkPaper(kinds)], fav, st, daily };

const TEST = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = []; ysItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    localStorage.setItem('examStatus', JSON.stringify(JSON.parse(__seed).st));
    localStorage.setItem('qDraw', '{}');
    localStorage.setItem('dailyMarks', '{}');

    // 复刻拼卷多轮（每轮抽 8 题，逐题记 qDraw.d++），记录每道题是第几轮被抽到的
    const order = [];
    for (let t = 0; t < 8; t++) {
        const rec = ppBuild(8);
        for (const it of rec.items) order.push({ qid: it.qid, state: it.state });
        const d = JSON.parse(localStorage.getItem('qDraw') || '{}');
        for (const it of rec.items) { const r = d[it.qid] || { d: 0 }; r.d++; r.ld = Date.now(); d[it.qid] = r; }
        localStorage.setItem('qDraw', JSON.stringify(d));
    }
    window.__order = order;
})();
`;
const sb = run(TEST, seed);
const order = sb.__order || [];
ok('抽题总数 = 40（10 hot + 30 plain）', order.length === 40, '得到 ' + order.length);
const hotQids = new Set(Array.from({ length: 10 }, (_, i) => 'P-' + (i + 1)));
const firstPlainAt = order.findIndex(x => !hotQids.has(x.qid));
const lastHotAt = order.map((x, i) => hotQids.has(x.qid) ? i : -1).filter(i => i >= 0).pop();
ok('所有 hot 在首个 plain 之前抽完', firstPlainAt === -1 || lastHotAt < firstPlainAt,
    `lastHot=${lastHotAt}, firstPlain=${firstPlainAt}`);
ok('前 10 抽全是 hot', order.slice(0, 10).every(x => hotQids.has(x.qid)),
    JSON.stringify(order.slice(0, 10)));
ok('hot 题状态确为 unknown/unfamiliar', order.filter(x => hotQids.has(x.qid)).every(x => x.state === 'unknown' || x.state === 'unfamiliar'));

/* ===== 场景 2：动态新增 hot —— 抽了 2 卷后，把一道原本 plain 的题新标记为 unknown，
   验证它在后续轮次优先于其他 plain 被抽（ageDays 最小但状态 hot）。 ===== */
const seed2 = JSON.parse(JSON.stringify(seed));
const newHotQid = 'P-40';   // 原本 plain
seed2.st[newHotQid] = 'unknown';   // 新标记为不会
seed2.fav[newHotQid] = { t: NOW }; // 刚碰过 → ageDays≈0

const TEST2 = `
;(function () {
    examPapers = JSON.parse(__seed).papers;
    corePapers = []; bankItems = []; ysItems = [];
    localStorage.setItem('examFav', JSON.stringify(JSON.parse(__seed).fav));
    localStorage.setItem('examStatus', JSON.stringify(JSON.parse(__seed).st));
    localStorage.setItem('qDraw', '{}');
    localStorage.setItem('dailyMarks', '{}');
    const order = [];
    // 抽 1 卷（8 题），先把初始 10 个 hot 抽掉一部分
    for (let t = 0; t < 6; t++) {
        const rec = ppBuild(8);
        for (const it of rec.items) order.push({ qid: it.qid, state: it.state });
        const d = JSON.parse(localStorage.getItem('qDraw') || '{}');
        for (const it of rec.items) { const r = d[it.qid] || { d: 0 }; r.d++; r.ld = Date.now(); d[it.qid] = r; }
        localStorage.setItem('qDraw', JSON.stringify(d));
    }
    window.__order2 = order;
})();
`;
const sb2 = run(TEST2, seed2);
const order2 = sb2.__order2 || [];
const newHotAt = order2.findIndex(x => x.qid === newHotQid);
ok('动态新标记的 hot 被抽到', newHotAt >= 0, 'idx=' + newHotAt);
// 初始 hot 共 10 题；P-40 新 hot 也是 hot，所以 11 个 hot 应 precedes 所有 plain
const hotSet2 = new Set([...Array.from({ length: 10 }, (_, i) => 'P-' + (i + 1)), newHotQid]);
const firstPlain2 = order2.findIndex(x => !hotSet2.has(x.qid));
const lastHot2 = order2.map((x, i) => hotSet2.has(x.qid) ? i : -1).filter(i => i >= 0).pop();
ok('新 hot 与初始 hot 全部先于 plain 抽完', firstPlain2 === -1 || lastHot2 < firstPlain2,
    `lastHot=${lastHot2}, firstPlain=${firstPlain2}`);

/* ===== 场景 3：用户可见文案必须反映「状态硬优先」，不能残留「同一档内不会/不熟优先」旧说法 ===== */
const CATJS = fs.readFileSync(path.join(__dirname, '..', 'pwa', 'js', 'category.js'), 'utf8');
ok('弹窗初始文案已更新', /不会 \/ 不熟抽完才抽仅收藏/.test(CATJS));
ok('弹窗动态文案已更新', /不会 \/ 不熟全部抽完才抽仅收藏/.test(CATJS));
ok('拼卷入口副文案已更新', /不会 \/ 不熟抽完才抽仅收藏/.test(CATJS));
ok('无「同一档内不会 / 不熟优先」旧说法', CATJS.indexOf('同一档内不会 / 不熟优先') < 0);

console.log(`\n结果：${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
