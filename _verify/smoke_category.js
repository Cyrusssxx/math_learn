// DOM 桩冒烟测试：用真实 exam.json + exam_categories.json 跑 category.js 的 init()，
// 验证三级树渲染（学科/章节/知识点）、favOnly 过滤、年份下钻链接。
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const PWA = path.resolve(__dirname, '..', 'pwa');
const code = fs.readFileSync(path.join(PWA, 'js', 'category.js'), 'utf8');
const exam = JSON.parse(fs.readFileSync(path.join(PWA, 'data', 'exam.json'), 'utf8'));
const cats = JSON.parse(fs.readFileSync(path.join(PWA, 'data', 'exam_categories.json'), 'utf8'));

function findQid(pred) {
    for (const p of exam) for (const s of p.sections) for (const q of s.questions)
        if (pred(p, q)) return p.id + '-' + q.no;
}
// 两个分属不同叶子的收藏题：极限/极限(329) 与 矩阵/逆(24)
const favA = findQid((p, q) => q.categoryIds[0] === 329);
const favB = findQid((p, q) => q.categoryIds[0] === 24);

function runWith(store) {
    const els = {};
    function fakeEl(id) {
        if (!els[id]) els[id] = {
            id, innerHTML: '', style: {},
            classList: { _s: new Set(),
                toggle(c, on) { if (on === undefined) { this._s.has(c) ? this._s.delete(c) : this._s.add(c); } else { on ? this._s.add(c) : this._s.delete(c); } },
                contains(c) { return this._s.has(c); }, add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); } },
            appendChild() {}, querySelectorAll() { return []; }, querySelector() { return null; },
            addEventListener() {}, replaceWith() {},
        };
        return els[id];
    }
    const localStorage = {
        getItem: k => (k in store ? store[k] : null),
        setItem: (k, v) => { store[k] = v; },
        removeItem: k => { delete store[k]; },
    };
    const document = {
        getElementById: id => fakeEl(id),
        createElement: () => fakeEl('_t' + Math.random()),
        body: { appendChild() {} },
        addEventListener() {}, querySelectorAll() { return []; },
    };
    const ctx = {
        console,
        localStorage,
        document,
        window: { katex: null },
        renderMathInElement: () => {},
        alert: () => {},
        setTimeout, clearTimeout,
        fetch: (url) => Promise.resolve({
            ok: true,
            json: () => url.includes('exam_categories') ? Promise.resolve(cats) : Promise.resolve(exam),
        }),
    };
    ctx.globalThis = ctx;
    vm.createContext(ctx);
    const wrapped = code + '\n;globalThis.__run = async () => { try { await init(); globalThis.__tree = document.getElementById("catTree").innerHTML; globalThis.__main = document.getElementById("catMain").innerHTML; try { selectCat(329); globalThis.__mainSel = document.getElementById("catMain").innerHTML; } catch (e) { globalThis.__err2 = String(e && e.stack || e); } globalThis.__ok = true; } catch (e) { globalThis.__err = String(e && e.stack || e); } };';
    vm.runInContext(wrapped, ctx);
    return new Promise(res => {
        ctx.__run().then(() => res({ tree: ctx.__tree || '', main: ctx.__main || '', mainSel: ctx.__mainSel || '', err: ctx.__err }));
    });
}

(async () => {
    // ① 全量
    const full = await runWith({});
    const okFull = full.err === undefined;
    const hasSubject = full.tree.includes('paper-group-head');
    const hasChapter = full.tree.includes('cat-chapter-head');
    const hasLeaf = full.tree.includes('cat-leaf');
    const hasDeriv = full.tree.includes('导数计算');
    console.log('【全量】err=', full.err || '无', '| 学科头', hasSubject, '| 章头', hasChapter, '| 叶子', hasLeaf, '| 含「导数计算」', hasDeriv);

    // ② favOnly（仅收藏 favA/favB）
    const favStore = { examFav: JSON.stringify({ [favA]: 1, [favB]: 1 }), examFavOnly: '1' };
    const fav = await runWith(favStore);
    const favTree = fav.tree;
    const onlyFavLeaves = (favTree.match(/cat-leaf-name">([^<]+)</g) || []).map(s => s.replace(/cat-leaf-name">/, '').replace(/</, ''));
    const totalMatch = (favTree.match(/paper-group-count">(\d+)</g) || []).map(s => +s.replace(/[^0-9]/g, ''));
    const grandTotal = totalMatch.reduce((a, b) => a + b, 0);
    console.log('【收藏】err=', fav.err || '无', '| 树中叶子:', onlyFavLeaves, '| 学科总题数合计:', grandTotal, '(应=2)');

    // ③ 主区下钻链接（点叶子后应有 exam.html?paper= 链接）
    const hasDrill = (full.mainSel || '').includes('exam.html?paper=');
    console.log('【主区】选中叶子后含年份下钻链接:', hasDrill, '| __err2=', full.err2 || '无');

    const pass = okFull && hasSubject && hasChapter && hasLeaf && hasDeriv && !fav.err && grandTotal === 2 && hasDrill;
    console.log(pass ? 'SMOKE PASS ✅' : 'SMOKE FAIL ❌');
    process.exit(pass ? 0 : 1);
})();
