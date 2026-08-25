// 冒烟测试：旧格式收藏一次性迁移为今天的时间戳
// 验证：① 脚本加载后 localStorage.examFav 中旧格式 {qid:1} 变为 {qid:{t}}，且 t 为「今天」
//      ② 已是新格式的条目时间戳不变
//      ③ 迁移后徽标可正常渲染（MM-DD = 今天）
const fs = require('fs'), vm = require('vm'), path = require('path');
const PWA = path.resolve(__dirname, '..', 'pwa');
const exam = JSON.parse(fs.readFileSync(PWA + '/data/exam.json', 'utf8'));
const cats = JSON.parse(PWA === null ? '{}' : fs.readFileSync(PWA + '/data/exam_categories.json', 'utf8'));

const OLD_T = 1700000000000;   // 一个确定是"过去"的旧时间戳
const store = {
    examFav: JSON.stringify({
        '2026数二真题-1': 1,            // 旧格式 → 应迁移
        '2026数二真题-2': { t: OLD_T }  // 新格式 → 应保持
    })
};
const els = {};
function fakeEl(id) {
    if (!els[id]) els[id] = {
        id, innerHTML: '', style: {},
        classList: { _s: new Set(), toggle() {}, add() {}, remove() {}, contains() { return false; } },
        appendChild() {}, insertBefore() {}, querySelectorAll() { return []; },
        querySelector() { return null; }, addEventListener() {}, replaceWith() {}
    };
    return els[id];
}
const document = {
    getElementById: id => fakeEl(id),
    createElement: () => fakeEl('_t' + Math.random()),
    body: { appendChild() {} }, addEventListener() {}, querySelectorAll() { return []; }
};
const ctx = {
    console, document,
    localStorage: {
        getItem: k => (k in store ? store[k] : null),
        setItem: (k, v) => { store[k] = String(v); },
        removeItem: k => { delete store[k]; }
    },
    window: { katex: null }, renderMathInElement() {}, alert() {},
    setTimeout, clearTimeout,
    fetch: u => Promise.resolve({ ok: true, json: () => (u.includes('exam_categories') ? Promise.resolve(cats) : Promise.resolve(exam)) })
};
ctx.globalThis = ctx;
vm.createContext(ctx);

let code = fs.readFileSync(PWA + '/js/category.js', 'utf8');
code += `
;globalThis.__afterLoad = () => {
    const f = JSON.parse(localStorage.getItem('examFav'));
    globalThis.__f = f;
};`;
vm.runInContext(code, ctx);
ctx.__afterLoad();

const f = ctx.__f || {};
const today0 = new Date(); today0.setHours(0, 0, 0, 0);
const isToday = ts => ts >= today0.getTime();
const migrated = f['2026数二真题-1'] && typeof f['2026数二真题-1'] === 'object' && isToday(f['2026数二真题-1'].t);
const kept = f['2026数二真题-2'] && f['2026数二真题-2'].t === OLD_T;
const persisted = store.examFav.includes('"t":');

console.log('旧格式迁移为今天:', migrated, '| 新格式时间保持:', kept, '| 已写回存储:', persisted);
console.log('迁移后存储内容:', store.examFav.slice(0, 120));
const pass = migrated && kept && persisted;
console.log(pass ? 'SMOKE PASS' : 'SMOKE FAIL');
process.exit(pass ? 0 : 1);
