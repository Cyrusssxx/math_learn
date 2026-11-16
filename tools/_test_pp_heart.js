/**
 * ♥ 喜欢标记 + 独立筛选页 回归（2026-11-16）
 *   A. 纯函数：heartGet/heartSave/isHeart/toggleHeart（真实 localStorage，含取消/反向验证）
 *   B. catCard 渲染：只在 PAPER_MODE / HEART_MODE 出 ♥ 按钮（正向+反向）
 *   C. 接线/入口/样式静态断言（HEART_MODE、renderMain/init/storage、两页顶栏、CSS）
 * 用法：node tools/_test_pp_heart.js
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('D:/ai code/408-quiz/node_modules/jsdom');
const ROOT = path.resolve(__dirname, '..');
const JS = fs.readFileSync(path.join(ROOT, 'pwa/js/category.js'), 'utf8');
const CSS = fs.readFileSync(path.join(ROOT, 'pwa/css/category.css'), 'utf8');
const CAT_HTML = fs.readFileSync(path.join(ROOT, 'pwa/category.html'), 'utf8');
const EXAM_HTML = fs.readFileSync(path.join(ROOT, 'pwa/exam.html'), 'utf8');

let pass = 0, fail = 0;
function ok(label, cond) { if (cond) pass++; else { fail++; console.log('  ✗ ' + label); } }
function eq(label, got, want) { ok(label + '（得到 ' + JSON.stringify(got) + '）', JSON.stringify(got) === JSON.stringify(want)); }

/* ---------- 感知字符串/正则/注释的函数抽取器（复用 _test_cat_search.js 思路） ---------- */
function extractFn(src, name) {
    const re = new RegExp('function\\s+' + name + '\\s*\\(');
    const m = re.exec(src);
    if (!m) throw new Error('找不到函数 ' + name);
    let i = src.indexOf('{', src.indexOf(')', m.index));
    let depth = 0, prevSig = '(';
    while (i < src.length) {
        const ch = src[i], nx = src[i + 1];
        if (ch === '/' && nx === '/') { const e = src.indexOf('\n', i); if (e < 0) break; i = e; continue; }
        if (ch === '/' && nx === '*') { const e = src.indexOf('*/', i); if (e < 0) break; i = e + 2; continue; }
        if (ch === '"' || ch === "'" || ch === '`') {
            i++;
            while (i < src.length && src[i] !== ch) { if (src[i] === '\\') i++; i++; }
            i++; prevSig = 'Q'; continue;
        }
        if (ch === '/' && /[({[,;:=!&|?+\-*%<>~^]/.test(prevSig)) {
            i++; let inCls = false;
            while (i < src.length) {
                const c = src[i];
                if (c === '\\') { i += 2; continue; }
                if (c === '[') inCls = true;
                else if (c === ']') inCls = false;
                else if (c === '/' && !inCls) { i++; break; }
                else if (c === '\n') break;
                i++;
            }
            while (i < src.length && /[a-z]/.test(src[i])) i++;
            prevSig = 'R'; continue;
        }
        if (ch === '{') depth++;
        else if (ch === '}') { depth--; if (depth === 0) return src.slice(m.index, i + 1); }
        if (!/\s/.test(ch)) prevSig = ch;
        i++;
    }
    throw new Error('抽取失败（括号不配平）: ' + name);
}

/* ---------- A. 存取函数真实 localStorage 测试 ---------- */
const dom = new JSDOM('<!doctype html><html><body><div id="catMain"></div></body></html>', { url: 'http://localhost/' });
const LS = dom.window.localStorage;
const HEART_KEY = 'ppHeart';
let HEART_MODE = false;
const storeFns = new Function('localStorage', 'HEART_KEY', 'getMode',
    [
        extractFn(JS, 'heartGet'),
        extractFn(JS, 'heartSave'),
        extractFn(JS, 'isHeart'),
        extractFn(JS, 'toggleHeart'),
        'return { heartGet, heartSave, isHeart, toggleHeart };',
    ].join('\n').replace(/\bHEART_MODE\b/g, 'getMode()')
)(LS, HEART_KEY, () => HEART_MODE);
const { heartGet, heartSave, isHeart, toggleHeart } = storeFns;

console.log('A. ♥ 存取函数');
eq('初始为空', heartGet(), {});
ok('初始未标记', !isHeart('mn27-01-1'));
const btn = { classList: { toggle(c, on) { this[c] = !!on; } }, textContent: '', title: '' };
const QID = '2000-1';   // 真题 qid（♥ 只可能在拼卷页的题目上标记，来源为真题/核心/大观园/ys27）
const on = toggleHeart(QID, btn);
ok('首次标记返回 true', on === true);
ok('写入存储', isHeart(QID) && !!heartGet()[QID].t);
ok('按钮切到实心 ♥', btn.textContent === '♥' && btn.classList.on === true);
const off = toggleHeart(QID, btn);
ok('再次标记返回 false（取消）', off === false);
ok('取消后从存储移除', !isHeart(QID) && !(QID in heartGet()));
ok('按钮切回空心 ♡', btn.textContent === '♡' && btn.classList.on === false);
// 反向验证：取消后再标记仍能正确写回（防止「只能标记一次」的假通过）
toggleHeart('ys27-3', null);
ok('另一题独立标记', isHeart('ys27-3') && !isHeart(QID));
heartSave({});

/* ---------- B. catCard 条件渲染 ♥ 按钮 ---------- */
console.log('B. catCard 条件渲染');
let PAPER_MODE = false;
const cardFn = new Function('PAPER_MODE', 'getHeartMode',
    [
        extractFn(JS, 'catCard'),
        'return catCard;',
    ].join('\n').replace(/\bHEART_MODE\b/g, 'getHeartMode()')
)(false, () => HEART_MODE);
// catCard 依赖较杂，注入桩；只关心 q-status-rail 的结构
function renderCard(paperMode, heartMode, hearted) {
    PAPER_MODE = paperMode; HEART_MODE = heartMode;
    const card = new Function('PAPER_MODE', 'getHeartMode', 'window', 'qidOf', 'isFav', 'statusOf', 'isHeart',
        'secKindLabel', 'mdBlock', 'mdInline', 'copyMdAttr', 'noteGet', 'videoBtnHtml',
        'coreBankHas', 'CoreExtra', 'favTime', 'fmtFavTime', 'fmtFavShort', 'ansTabsHtml',
        [
            extractFn(JS, 'catCard'),
            'return catCard;',
        ].join('\n').replace(/\bHEART_MODE\b/g, 'getHeartMode()')
    )(paperMode, () => heartMode, { CoreExtra: null },
        () => 'mn27-01-1', () => false, () => null, () => hearted,
        () => '选择', s => s || '', s => s || '', s => String(s || '').replace(/"/g, '&quot;'), () => '', () => '',
        () => false, null, () => 0, () => '', () => '', () => '<div class="ans"></div>'
    )({ id: 'mn27-01', year: 2027 }, '一、选择题', { no: 1, stem: '题面', options: [], answer: 'A' });
    const d = new JSDOM('<div>' + card + '</div>').window.document;
    return d.querySelector('.q-status-rail');
}
let rail = renderCard(false, false, false);
ok('普通分类页不渲染 ♥（反向）', rail && !rail.querySelector('.q-st-heart'));
rail = renderCard(true, false, false);
ok('拼卷页渲染空心 ♡', rail && rail.querySelector('.q-st-heart') && rail.querySelector('.q-st-heart').textContent === '♡');
rail = renderCard(true, false, true);
ok('拼卷页已标记渲染实心 ♥', rail && rail.querySelector('.q-st-heart').textContent === '♥');
rail = renderCard(false, true, true);
ok('♥ 页渲染实心 ♥', rail && rail.querySelector('.q-st-heart').textContent === '♥');
ok('♥ 在状态按钮栏尾部（第 4 个）', rail && rail.children.length === 4 && rail.children[3].classList.contains('q-st-heart'));

/* ---------- C. 接线/入口/样式 ---------- */
console.log('C. 接线/入口/样式');
ok('HEART_MODE 由 ?heart=1 定义', /const\s+HEART_MODE\s*=\s*new URLSearchParams\(location\.search\)\.get\('heart'\)\s*===\s*'1'/.test(JS));
ok('renderMain 分派 renderHeart', /if \(HEART_MODE\)\s*\{\s*renderHeart\(\);\s*return;\s*\}/.test(JS));
ok('init 调 applyHeartMode', /applyHeartMode\(\);\s*\/\/[^\n]*heart=1/.test(JS));
ok('storage 事件含 HEART_KEY', /k === HEART_KEY/.test(JS));
ok('storage 分派 renderHeart', /else if \(HEART_MODE\) renderHeart\(\)/.test(JS));
ok('♥ 页不选分类树', /!REVIEW_MODE && !HEART_MODE && !PAPER_MODE/.test(JS));
ok('two-page 顶栏入口：exam.html', /href="category\.html\?heart=1"[^>]*>\s*♥ 喜欢/.test(EXAM_HTML));
ok('two-page 顶栏入口：category.html', /href="category\.html\?heart=1"[^>]*>\s*♥ 喜欢/.test(CAT_HTML));
ok('♥ 页隐藏自身入口', /body\.heart-mode \.hf-entry \{ display: none/.test(CSS));
ok('♥ 页显示返回分类', /body\.heart-mode \.hf-back \{ display: inline-flex/.test(CSS));
ok('♥ 按钮 hover 色', /\.q-st-btn\.q-st-heart:hover/.test(CSS));
ok('♥ 按钮选中态', /\.q-st-btn\.q-st-heart\.on/.test(CSS));
ok('♥ 页隐藏左栏', /body\.heart-mode #catSide \{ display: none/.test(CSS));
ok('♥ 页筛选条样式', /\.hf-filter \.cat-mark/.test(CSS));
// 反向：不允许 ♥ 进抽题池（拼卷扫描池不得引用 ppHeart/heartGet）
const ppScanPoolStart = JS.indexOf('function ppScanPool()');
const ppScanPoolEnd = JS.indexOf('function ppBuildPool()');
const poolSrc = JS.slice(ppScanPoolStart, ppScanPoolEnd);
ok('抽题池不引用 ♥（反向）', !/heart/i.test(poolSrc));

console.log(`\n结果：${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
