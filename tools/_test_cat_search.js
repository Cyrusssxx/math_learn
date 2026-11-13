/**
 * 分类页搜索归一化回归（2026-11-14）
 *   背景：原 catSearchMatch 直接 toLowerCase().includes()，且把 $...$ 整块删成空格，
 *        造成「带空格 / 全角 / 公式符号」搜不到。
 *   本测试两层：
 *     A. 纯函数单测（normFont / searchTokens / searchBlob / catSearchMatch）
 *     B. 真实题库跑关键词，打印命中数（防「改完变全零」）
 * 用法：node tools/_test_cat_search.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = fs.readFileSync(path.join(ROOT, 'pwa/js/category.js'), 'utf8');

/* ---------- 从源码里按名字抽取函数（括号配平，避免整文件 eval 撞 DOM） ----------
   难点：函数体里有正则字面量（/\{/、/\\begin\{[^}]*\}/），裸扫花括号会把正则里的 } 当块结束。
   所以这里写一个感知「字符串 / 正则字面量 / 注释」的扫描器。 */
function extractFn(src, name) {
    const re = new RegExp('function\\s+' + name + '\\s*\\(');
    const m = re.exec(src);
    if (!m) throw new Error('找不到函数 ' + name);
    let i = src.indexOf('{', src.indexOf(')', m.index));
    let depth = 0;
    let prevSig = '(';           // 上一个有意义字符，用于判定 / 是正则还是除号
    while (i < src.length) {
        const ch = src[i], nx = src[i + 1];
        if (ch === '/' && nx === '/') { const e = src.indexOf('\n', i); if (e < 0) break; i = e; continue; }
        if (ch === '/' && nx === '*') { const e = src.indexOf('*/', i); if (e < 0) break; i = e + 2; continue; }
        if (ch === '"' || ch === "'" || ch === '`') {
            i++;
            while (i < src.length && src[i] !== ch) { if (src[i] === '\\') i++; i++; }
            i++; prevSig = 'Q'; continue;
        }
        if (ch === '/' && /[({[,;:=!&|?+\-*%<>~^]/.test(prevSig)) {   // 正则字面量
            i++;
            let inCls = false;
            while (i < src.length) {
                const c = src[i];
                if (c === '\\') { i += 2; continue; }
                if (c === '[') inCls = true;
                else if (c === ']') inCls = false;
                else if (c === '/' && !inCls) { i++; break; }
                else if (c === '\n') break;
                i++;
            }
            while (i < src.length && /[a-z]/.test(src[i])) i++;       // flags
            prevSig = 'R'; continue;
        }
        if (ch === '{') depth++;
        else if (ch === '}') { depth--; if (depth === 0) return src.slice(m.index, i + 1); }
        if (!/\s/.test(ch)) prevSig = ch;
        i++;
    }
    throw new Error('抽取失败（括号不配平）: ' + name);
}

const FN_NAMES = ['normFont', 'searchTokens', 'searchBlob', 'entrySearchBlob', 'setCatSearchKw', 'catSearchMatch'];
const body = 'let catSearchKw="";let catSearchToks=[];\n' + FN_NAMES.map(n => extractFn(SRC, n)).join('\n');
// cats 作为外部依赖注入
const factory = new Function('cats', body + '\nreturn {normFont,searchTokens,searchBlob,entrySearchBlob,setCatSearchKw,catSearchMatch,getTok:()=>catSearchToks};');

/* ---------- 断言器 ---------- */
let pass = 0, fail = 0;
function eq(label, got, want) {
    const g = JSON.stringify(got), w = JSON.stringify(want);
    if (g === w) { pass++; }
    else { fail++; console.log(`  ✗ ${label}\n      得到 ${g}\n      期望 ${w}`); }
}
function ok(label, cond, extra) {
    if (cond) pass++;
    else { fail++; console.log(`  ✗ ${label}${extra ? '\n      ' + extra : ''}`); }
}

/* ================= A. 纯函数单测 ================= */
console.log('=== A. 归一化 / 分词 / 匹配 ===');
const M = factory({});
const { normFont, searchTokens, searchBlob, entrySearchBlob, setCatSearchKw, catSearchMatch } = M;

// A1 全角 → 半角、全角空格、零宽
eq('全角字母数字', normFont('ＡＢＣ１２３'), 'ABC123');
eq('全角空格当分隔', normFont('极限　计算'), '极限 计算');
eq('零宽字符清掉', normFont('极\u200B限'), '极限');

// A2 分词：空格 / 多空格 / 制表 / 全角空格 都算分隔
eq('单空格', searchTokens('sin x'), ['sin', 'x']);
eq('多空格', searchTokens('  极限     计算  '), ['极限', '计算']);
eq('全角空格', searchTokens('极限　计算'), ['极限', '计算']);
eq('大小写', searchTokens('SIN X'), ['sin', 'x']);
eq('换行制表', searchTokens('极限\t\n计算'), ['极限', '计算']);
eq('token 内去结构符', searchTokens('$x^2$'), ['x2']);
eq('空串', searchTokens('   '), []);

// A3 LaTeX → 可搜索串（这是最关键的一条：原实现整块删公式）
eq('sin x → sinx', searchBlob('$\\sin x$'), 'sinx');
eq('int_0^x → int0x', searchBlob('$\\int_0^x$'), 'int0x');
eq('int_0^{x^2} → int0x2', searchBlob('$\\int_0^{x^2}$'), 'int0x2');
ok('sqrt{x-t} 保留连字符', searchBlob('$\\sqrt{x-t}$').indexOf('x-t') >= 0, searchBlob('$\\sqrt{x-t}$'));
eq('frac 去反斜杠', searchBlob('$\\frac{1}{2}$'), 'frac12');
eq('begin/end 整块删', searchBlob('$\\begin{cases}a&b\\end{cases}$'), 'ab');
ok('中文原样保留', searchBlob('求极限').indexOf('求极限') === 0);

// A4 匹配：AND 语义 + 公式命中
const mkEntry = (stem, extra) => Object.assign({
    paper: { id: 'p', year: '2026', title: '测试卷' },
    secTitle: '',
    q: { no: 1, stem, answer: '', idea: '' },
    catId: '1',
}, extra || {});
const cats = { '1': { name: '函数极限', path: '高等数学/函数极限' } };
const M2 = factory(cats);
const e1 = mkEntry('求极限 $\\lim\\limits_{x\\to0}\\dfrac{\\sin x}{x}$');
M2.setCatSearchKw('sinx');
ok('搜 sinx 命中 $\\sin x$', M2.catSearchMatch(e1));
M2.setCatSearchKw('极限');
ok('搜中文命中', M2.catSearchMatch(e1));
M2.setCatSearchKw('极限 sinx');
ok('两个词都命中（含空格）', M2.catSearchMatch(e1));
M2.setCatSearchKw('极限　sinx');
ok('全角空格也命中', M2.catSearchMatch(e1));
M2.setCatSearchKw('极限 不存在');
ok('一词不中就整体不中（AND）', !M2.catSearchMatch(e1));
M2.setCatSearchKw('函数极限');
ok('搜知识点路径命中', M2.catSearchMatch(e1));
M2.setCatSearchKw('2026');
ok('搜年份命中', M2.catSearchMatch(e1));
M2.setCatSearchKw('   ');
ok('空词返回 true（不过滤）', M2.catSearchMatch(e1));

// 变限积分换元题：能否搜到
const e2 = mkEntry('求极限 $\\lim\\limits_{x\\to0^+}\\dfrac{\\int_0^x e^t\\sqrt{x-t}\\,dt}{\\sqrt{x^3}}$');
M2.setCatSearchKw('x-t');
ok('搜 x-t 命中 sqrt{x-t}', M2.catSearchMatch(e2));
M2.setCatSearchKw('int0x');
ok('搜 int0x 命中上限积分', M2.catSearchMatch(e2));
M2.setCatSearchKw('sqrtx');
ok('搜 sqrtx 命中 sqrt{x-t} / sqrt{x^3}', M2.catSearchMatch(e2));
ok('sqrt 与 t 之间没有多余分隔', searchBlob('$\\sqrt{x-t}$') === 'sqrtx-t', searchBlob('$\\sqrt{x-t}$'));

// 缓存字段正确写入
ok('_sb 已缓存', typeof e2._sb === 'string' && e2._sb.length > 0);
const firstSb = e2._sb;
M2.setCatSearchKw('随便');
M2.catSearchMatch(e2);
ok('二次调用复用缓存', e2._sb === firstSb);

/* ================= B. 真实题库命中数 ================= */
console.log('=== B. 真实题库 ===');
const catsReal = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/exam_categories.json'), 'utf8'));
const M3 = factory(catsReal);

function loadEntries() {
    const out = [];
    const pushPaper = (p) => {
        for (const s of (p.sections || [])) {
            for (const q of (s.questions || [])) {
                for (const cid of (q.categoryIds || [])) {
                    out.push({ paper: p, secTitle: s.title || '', q, catId: String(cid) });
                }
            }
        }
    };
    for (const f of ['exam.json', 'core_bank.json', 'ys27_items.json']) {
        const fp = path.join(ROOT, 'pwa/data', f);
        if (!fs.existsSync(fp)) continue;
        for (const p of JSON.parse(fs.readFileSync(fp, 'utf8'))) pushPaper(p);
    }
    return out;
}
const entries = loadEntries();
console.log(`  题库条目（qid×分类）: ${entries.length}`);

const KW = ['极限', '极限 计算', 'sinx', 'x-t', 'int0x', '变上限', '洛必达', '2026', '拉格朗日', '特征值'];
const report = {};
for (const kw of KW) {
    const t0 = Date.now();
    M3.setCatSearchKw(kw);
    const hits = entries.filter(M3.catSearchMatch).length;
    report[kw] = { hits, ms: Date.now() - t0 };
    console.log(`  “${kw}” → ${hits} 条 (${Date.now() - t0}ms)`);
}
ok('搜「极限」有结果', report['极限'].hits > 50, '实际 ' + report['极限'].hits);
ok('搜「极限 计算」（带空格）有结果', report['极限 计算'].hits > 0, '实际 ' + report['极限 计算'].hits);
ok('搜「sinx」（公式）有结果', report['sinx'].hits > 0, '实际 ' + report['sinx'].hits);
ok('搜「x-t」（公式）有结果', report['x-t'].hits > 0, '实际 ' + report['x-t'].hits);
ok('搜「int0x」（上限积分）有结果', report['int0x'].hits > 0, '实际 ' + report['int0x'].hits);
ok('搜「洛必达」有结果', report['洛必达'].hits > 0, '实际 ' + report['洛必达'].hits);
ok('搜「2026」有结果', report['2026'].hits > 0, '实际 ' + report['2026'].hits);
ok('首轮全库搜索 < 2000ms', Math.max(...Object.values(report).map(r => r.ms)) < 2000,
   '最慢 ' + Math.max(...Object.values(report).map(r => r.ms)) + 'ms');

/* ================= C. 变异反向验证（证明上面的断言不是恒真） ================= */
console.log('=== C. 变异反向验证 ===');
function buildFrom(src, catsArg) {
    return new Function('cats', 'let catSearchKw="";let catSearchToks=[];\n' +
        FN_NAMES.map(n => extractFn(src, n)).join('\n') +
        '\nreturn {normFont,searchTokens,searchBlob,entrySearchBlob,setCatSearchKw,catSearchMatch};')(catsArg);
}

// 变异 1：去掉「结构符号当分隔」这一步 → `\int_0^x` 里的 _ ^ 会留在结果里，搜 int0x 应失败
const V1SRC = SRC.replace(".replace(/[${}^_&\\\\`*]/g, ' ');             // 结构符号一律当分隔", '');
ok('变异1 替换点存在', V1SRC !== SRC);
if (V1SRC !== SRC) {
    const V1 = buildFrom(V1SRC, cats);
    // ⚠️ 必须用全新 entry：e2 在 A 段已缓存 _sb（正常版算的），复用它会让变异读到干净 blob
    const e2x = mkEntry('求极限 $\\lim\\limits_{x\\to0^+}\\dfrac{\\int_0^x e^t\\sqrt{x-t}\\,dt}{\\sqrt{x^3}}$');
    V1.setCatSearchKw('int0x');
    ok('变异1 后搜 int0x 失败（证明结构化断言有效）', !V1.catSearchMatch(e2x), 'blob=' + V1.entrySearchBlob(e2x));
    const e1x = mkEntry('求极限 $\\lim\\limits_{x\\to0}\\dfrac{\\sin x}{x}$');
    V1.setCatSearchKw('极限');
    ok('变异1 不影响纯中文匹配（说明变异是定点而非全局破坏）', V1.catSearchMatch(e1x));
}

// 变异 2：把 AND 改成 OR（一个词不中也算命中）→ 搜「极限 不存在」应变命中
const V2SRC = SRC.replace('if (blob.indexOf(catSearchToks[i]) < 0) return false;',
                          'if (blob.indexOf(catSearchToks[i]) < 0) return true;');
ok('变异2 替换点存在', V2SRC !== SRC);
if (V2SRC !== SRC) {
    const V2 = buildFrom(V2SRC, cats);
    const e1y = mkEntry('求极限 $\\lim\\limits_{x\\to0}\\dfrac{\\sin x}{x}$');
    V2.setCatSearchKw('极限 不存在');
    ok('变异2 后 AND 失效（证明 AND 断言有效）', V2.catSearchMatch(e1y));
}

/* ================= 汇总 ================= */
console.log(`\n通过 ${pass} 项，失败 ${fail} 项`);
process.exit(fail ? 1 : 0);
