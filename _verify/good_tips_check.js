/* good_tips_check.js — 好题点睛渲染 + KaTeX 全量校验
 * 用法: node _verify/good_tips_check.js
 *
 * 注意: katex 必须用 require 加载，不能放进 vm.createContext 沙箱——
 *       跨 realm 传 options 会让 Settings.displayMode 判定失效，产生
 *       "\tag works only in display equations" 之类的假报错。
 *
 * 校验内容:
 *   1. mdrender.mdToHtml 是否把 ::: 点睛 渲染成 tip-fold + 四段 q-tip-sec
 *   2. 渲染结果中是否残留未闭合的 ::: 或点睛原文
 *   3. good.json 全部 $...$ / $$...$$ 能否被 KaTeX 解析（throwOnError）
 *   4. 点睛块内新增公式单独统计（本次改动的质量门禁）
 */
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const katex = require('../pwa/vendor/katex/katex.min.js');

const ROOT = path.resolve(__dirname, '..');
const PWA = path.join(ROOT, 'pwa');

// mdrender.js 是纯字符串处理脚本，放 vm 里取 mdToHtml 即可
const ctx = { console, Math, JSON, RegExp, Date, String, Number, Array, Object, Map, Set };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(PWA, 'js', 'mdrender.js'), 'utf8'), ctx);

const good = JSON.parse(fs.readFileSync(path.join(PWA, 'data', 'good.json'), 'utf8'));

// ---------- 1&2 渲染结构校验 ----------
let foldCnt = 0, secCnt = 0, notesWithTip = 0, leakFold = 0, leakTxt = 0;
const secByCls = { 'tip-gs': 0, 'tip-yc': 0, 'tip-jq': 0, 'tip-zy': 0 };
const problems = [];

for (const n of good) {
    const html = ctx.mdToHtml(n.md);
    const f = (html.match(/class="fold tip-fold"/g) || []).length;
    const s = (html.match(/class="q-tip-sec /g) || []).length;
    foldCnt += f; secCnt += s;
    if (f) notesWithTip++;
    for (const c of Object.keys(secByCls)) {
        secByCls[c] += (html.match(new RegExp('class="q-tip-sec ' + c + '"', 'g')) || []).length;
    }
    const text = html.replace(/<[^>]*>/g, '');
    if (/^:::/m.test(text)) leakFold++;
    // 泄漏判据：点睛原文（**公式** 等标记）出现在纯文本里，说明容器没被解析
    if (/\*\*(公式|易错|技巧|注意)\*\*/.test(text) || /^:::\s*点睛/m.test(text)) leakTxt++;
    if (f && s < f * 2) problems.push(`${n.id}: 点睛块 ${f} 但段落仅 ${s}`);
}

// ---------- 3&4 KaTeX 校验 ----------
/* 行感知提取（比单一正则更贴近浏览器 auto-render 的实际切分）：
 *   - 单行 $$X$$            → display
 *   - 独占一行的 $$         → 进入/退出 display 块（块内整段为 display）
 *   - 其余行内的 $…$        → inline
 * 纯正则跨行非贪婪会在 $ 与 $$ 混排时错位，把 display 块误切成 inline，
 * 从而对 \tag 报出 "works only in display equations" 的假错。
 */
function extractMath(md) {
    const out = [];
    const lines = md.split('\n');
    let buf = null, bufStart = 0;
    lines.forEach((line, li) => {
        const t = line.trim();
        if (buf === null) {
            if (t === '$$') { buf = []; bufStart = li; return; }
            if (/^\$\$.*\$\$$/.test(t) && t.length > 4) {
                out.push({ src: t.slice(2, -2), disp: true, line: li });
                return;
            }
            const re = /\$([^$\n]+?)\$/g;
            let m;
            while ((m = re.exec(line))) out.push({ src: m[1], disp: false, line: li });
        } else {
            if (t === '$$' || /\$\$$/.test(t)) {
                const body = buf.join('\n') + (/\$\$$/.test(t) && t !== '$$' ? '\n' + t.replace(/\$\$$/, '') : '');
                out.push({ src: body.trim(), disp: true, line: bufStart });
                buf = null;
            } else buf.push(line);
        }
    });
    return out;
}

let total = 0, fail = 0, tipTotal = 0, tipFail = 0;
const fails = [];
function check(item, where, isTip) {
    total++;
    if (isTip) tipTotal++;
    // 注意：KaTeX 0.16 的 renderToString 只认 displayMode，传 display 不生效（会静默按 inline 处理，
    // 导致 \tag 报 "works only in display equations" 的假错）。浏览器端 auto-render 传的也是 displayMode。
    try { katex.renderToString(item.src, { displayMode: item.disp, throwOnError: true }); }
    catch (e) {
        fail++;
        if (isTip) tipFail++;
        if (fails.length < 12) {
            fails.push(`${where}${isTip ? ' [点睛]' : ''} L${item.line + 1} ${item.disp ? '$$' : '$'}: ` +
                `${item.src.slice(0, 60)} -> ${String(e.message).slice(0, 55)}`);
        }
    }
}
for (const n of good) {
    const tipRanges = [];
    const tre = /^::: 点睛\s*$([\s\S]*?)^:::\s*$/gm;
    let tm;
    while ((tm = tre.exec(n.md))) tipRanges.push([tm.index, tm.index + tm[0].length]);
    const inTip = (i) => tipRanges.some(([a, b]) => i >= a && i < b);
    // 行首字符偏移，用于判断公式是否落在点睛块内
    const offs = []; let acc = 0;
    for (const l of n.md.split('\n')) { offs.push(acc); acc += l.length + 1; }

    for (const it of extractMath(n.md)) check(it, n.id, inTip(offs[it.line] || 0));
}

console.log('=== 好题点睛渲染校验 ===');
console.log(`好题文件数             : ${good.length}`);
console.log(`含点睛块的文件         : ${notesWithTip}`);
console.log(`tip-fold 折叠块总数    : ${foldCnt}`);
console.log(`q-tip-sec 段落总数     : ${secCnt}`);
console.log(`公式/易错/技巧/注意    : ${secByCls['tip-gs']} / ${secByCls['tip-yc']} / ${secByCls['tip-jq']} / ${secByCls['tip-zy']}`);
console.log(`残留未闭合 :::         : ${leakFold}`);
console.log(`点睛原文泄漏           : ${leakTxt}`);
console.log('=== KaTeX 校验（require 加载，无沙箱）===');
console.log(`全库公式总数           : ${total}`);
console.log(`全库解析失败           : ${fail}`);
console.log(`其中 点睛块内公式      : ${tipTotal}（失败 ${tipFail}）`);
if (fails.length) { console.log('--- 失败样例 ---'); fails.forEach(f => console.log('  ' + f)); }
if (problems.length) { console.log('--- 结构问题 ---'); problems.forEach(p => console.log('  ' + p)); }
const ok = fail === 0 && leakFold === 0 && leakTxt === 0 && problems.length === 0;
console.log(ok ? '\n✅ 全部通过' : '\n❌ 存在问题');
process.exit(ok ? 0 : 1);
