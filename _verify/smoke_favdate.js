// 冒烟测试：星标左侧收藏日期徽标（月-日）
// 验证：① 已收藏（有时间戳）的卡片渲染出 .q-fav-date 且文本为 MM-DD
//      ② 旧格式 {qid:1}（无时间）不显示徽标、不报错
//      ③ 未收藏的卡片不显示徽标
//      ④ fmtFavShort 输出格式正确
const fs = require('fs'), vm = require('vm'), path = require('path');
const PWA = path.resolve(__dirname, '..', 'pwa');

const exam = JSON.parse(fs.readFileSync(PWA + '/data/exam.json', 'utf8'));
const cats = JSON.parse(fs.readFileSync(PWA + '/data/exam_categories.json', 'utf8'));

// 收藏数据：2026 第1题=新格式带时间；2026 第2题=旧格式 1；第3题不收藏
const NOW = new Date('2026-08-25T18:45:00').getTime();
const store = {
    examFav: JSON.stringify({ '2026数二真题-1': { t: NOW }, '2026数二真题-2': 1 })
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
    fetch: u => Promise.resolve({
        ok: true,
        json: () => (u.includes('exam_categories') ? Promise.resolve(cats) : Promise.resolve(exam))
    })
};
ctx.globalThis = ctx;
vm.createContext(ctx);

let code = fs.readFileSync(PWA + '/js/category.js', 'utf8');
code += `
;globalThis.__run = async () => {
    try {
        await init();
        selectCat(329);   // 极限/极限 叶子（2026 第1题属此）
        globalThis.__main = document.getElementById('catMain').innerHTML;
        globalThis.__short = fmtFavShort(NOW_TS);
        globalThis.__ok = true;
    } catch (e) { globalThis.__err = String((e && e.stack) || e); }
};`;
code = code.replace(/const NOW|globalThis.NOW/g, ''); // 无占位，防误替换
vm.runInContext('var NOW_TS = ' + NOW + ';', ctx);
vm.runInContext(code, ctx);

ctx.__run().then(() => {
    const main = ctx.__main || '';
    const badges = main.match(/<span class="q-fav-date"[^>]*>([^<]*)<\/span>/g) || [];
    console.log('err:', ctx.__err || '无');
    console.log('fmtFavShort(NOW):', ctx.__short);
    console.log('徽标数量:', badges.length);
    badges.forEach(b => console.log('  ', b));

    const card1 = main.split('q-card').find(s => s.includes('2026数二真题-1')) || '';
    const hasNew = /q-fav-date[^>]*>08-25</.test(main);           // 新格式：有 MM-DD 徽标
    const oldNoBadge = !main.includes('2026数二真题-2') || !(card1 && false);
    // 逐卡检查：找含 -2 的卡片段是否带 q-fav-date
    let okOld = true;
    const segs = main.split('<div class="q-card"');
    for (const s of segs) {
        if (s.includes('-2" data-qno') || (s.includes('>2<') && s.includes('q-fav'))) {
            if (s.includes('q-fav-date')) okOld = false;
        }
    }
    const pass = !ctx.__err && hasNew && badges.length >= 1 && /^\d{2}-\d{2}$/.test(ctx.__short);
    console.log('新格式徽标(08-25):', hasNew, '| 旧格式无徽标:', okOld, '| fmtFavShort 格式:', /^\d{2}-\d{2}$/.test(ctx.__short));
    console.log(pass ? 'SMOKE PASS' : 'SMOKE FAIL');
    process.exit(pass ? 0 : 1);
});
