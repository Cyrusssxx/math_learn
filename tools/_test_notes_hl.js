/* 笔记主页个人批注高亮配色断言
 * 2026-11-10 建（整体变淡 / 下划线降档）；2026-11-11 用户反馈「太淡看不见」→ 回调底色可见度。
 * 纯静态源文本断言 + 变异反向验证，不依赖 jsdom（jsdom 不解析 CSS 变量 / color-mix）。
 * 运行：node tools/_test_notes_hl.js
 * 覆盖：notes.css 浅/深两套变量与全部 mark / 公式 / 整块 / 编辑态规则、
 *       annotate.js 三处行内样式、范围边界（题库/拼卷色板、共享 hlBg/hlLine 不动）。
 *
 * 定档口径（11-13 终版）：
 *   行内荧光 —— 带高**固定 46%**（不动），只调 alpha：浅 .72~.74 / 深 .74~.76；
 *   公式整块底 —— `--hl-*-soft` 浅 .21~.22 / 深 .13~.15，且 `.katex.fml-hl-*` 必须有
 *                 `padding: 2px 4px`（背景原本紧贴字形，积分号溢出盒子 → 「范围小」）；
 *   下划线维持 11-10 的淡档（40%/38%、1px、offset 4px），不得回调。
 * 双向护栏：alpha ≥ .85 = 压字回归；alpha < .65 = 过淡看不见。
 *           带高改动（≠46%）= 越界，必须回到「只调一个维度」的方法论。
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const read = p => fs.readFileSync(path.join(ROOT, p), 'utf8');

const css = read('pwa/css/notes.css');
const js = read('pwa/js/annotate.js');
const common = read('pwa/js/common.js');
const catjs = read('pwa/js/category.js');
const examcss = read('pwa/css/exam.css');

let pass = 0, fail = 0;
function ok(name, cond) {
    if (cond) { pass++; }
    else { fail++; console.log('  ✗ ' + name); }
}
const has = (src, s) => src.indexOf(s) >= 0;
const no = (src, s) => src.indexOf(s) < 0;
/** 取某个 CSS 变量在全文里的所有取值（:root 一份、html.dark 一份） */
function vals(name, src) {
    const re = new RegExp('--' + name + ':\\s*([^;]+);', 'g');
    const out = []; let m;
    while ((m = re.exec(src || css))) out.push(m[1].trim());
    return out;
}
/** 取单条规则体（简单规则，不含嵌套花括号） */
function body(sel, src) {
    const s = sel.replace(/\s*\{\s*$/, '');
    // 行首锚定：避免匹配到组合选择器末尾的同名子串（如 p.hl-r 出现在
    // "p.hl-y, p.hl-g, p.hl-b, p.hl-r {" 里，会抓到错误的规则体）
    const re = new RegExp('(?:^|\\n)\\s*' + s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*\\{([^}]*)\\}');
    const m = re.exec(src || css);
    return m ? m[1] : '';
}
/** rgba(...) 的 alpha 数值 */
function alpha(v) {
    const m = /rgba\([^)]*?,\s*([\d.]+)\s*\)/.exec(v || '');
    return m ? parseFloat(m[1]) : NaN;
}
/** 渐变带高：linear-gradient(... 0 46%, transparent 46%)（JS 内联串没有空格） */
function bandPct(src) {
    const m = /0\s+(\d+)%\s*,\s*transparent\s+(\d+)%/.exec(src || '');
    return m && m[1] === m[2] ? +m[1] : NaN;
}
/** 带高锁死 46%：改带高就等于换维度调参，会重演「两个维度一起过冲」的坑 */
const BAND = 46;
const visibleBand = p => p === BAND;
/** alpha 双向窗口：≥.85 压字（色带把字下半截压住），<.65 过淡看不见 */
const alphaOk = a => a >= .65 && a < .85;

console.log('=== 1. 浅色 / 深色变量：alpha 落在「可见但不压字」窗口 ===');
const bandNames = ['mk-y2', 'mk-g2', 'mk-b2', 'mk-r2'];
const bandAlpha = { 'mk-y2': ['.74', '.76'], 'mk-g2': ['.72', '.74'], 'mk-b2': ['.72', '.74'], 'mk-r2': ['.72', '.74'] };
bandNames.forEach(n => {
    const v = vals(n);
    ok(n + ' 有浅/深两份', v.length === 2);
    ok(n + ' 浅色仍为 rgba 半透明（不是不透明实色）', /^rgba\(/.test(v[0] || ''));
    ok(n + ' 深色仍为 rgba 半透明', /^rgba\(/.test(v[1] || ''));
    ok(n + ' 浅色 alpha = ' + bandAlpha[n][0], has(v[0] || '', bandAlpha[n][0]));
    ok(n + ' 深色 alpha = ' + bandAlpha[n][1], has(v[1] || '', bandAlpha[n][1]));
    ok(n + ' 浅色 alpha 在 [.65,.85)（可见且不压字）', alphaOk(alpha(v[0])));
    ok(n + ' 深色 alpha 在 [.65,.85)（可见且不压字）', alphaOk(alpha(v[1])));
});
ok('压字档 .88/.90 已退场', no(css, 'rgba(255, 226, 171, .88)') && no(css, 'rgba(90, 74, 40, .90)'));
ok('压字档 .86/.88 已退场', no(css, 'rgba(191, 234, 176, .86)') && no(css, 'rgba(85, 36, 48, .88)'));
ok('旧实心 --mk-y2: #ffe2ab 已退场', no(css, '--mk-y2: #ffe2ab'));
ok('旧实心 --mk-g2: #bfeab0 已退场', no(css, '--mk-g2: #bfeab0'));
ok('旧实心 --mk-b2: #b3ddff 已退场', no(css, '--mk-b2: #b3ddff'));
ok('旧实心 --mk-r2: #ffbccb 已退场', no(css, '--mk-r2: #ffbccb'));
ok('11-10 过淡 --mk-y2 .55 退场', no(css, '--mk-y2: rgba(255, 226, 171, .55)'));
ok('11-10 过淡 --mk-g2 .52 退场', no(css, '--mk-g2: rgba(191, 234, 176, .52)'));
ok('11-10 过淡深色 --mk-y2 .62 退场', no(css, '--mk-y2: rgba(90, 74, 40, .62)'));

console.log('=== 2. 下划线淡档保持不变（用户明确要求弱化，本轮不动） ===');
const lineNames = ['mk-y-line', 'mk-g-line', 'mk-b-line', 'mk-r-line'];
lineNames.forEach(n => {
    const v = vals(n);
    ok(n + ' 浅/深两份齐全', v.length === 2);
    ok(n + ' 浅色仍是 40% 不透明度', has(v[0] || '', '.40'));
    ok(n + ' 深色仍是 38% 不透明度', has(v[1] || '', '.38'));
});
ok('实色 --hl-*-line 仍保留（fallback / 旧用途）', vals('hl-y-line').length === 2 && has(vals('hl-y-line')[0], '#e0a94f'));
ok('mark.mk 下划线仍是 1px + offset 4px', has(body('mark.mk {'), 'text-decoration-thickness: 1px') && has(body('mark.mk {'), 'text-underline-offset: 4px'));
ok('mark.note-hl 仍是 color-mix 40% 淡下划线', has(body('mark.note-hl {'), 'color-mix(in srgb, var(--nhl-line, var(--nhl)) 40%, transparent)'));

console.log('=== 3. 公式整块底 / 整块高亮：两套浓度各自定档 ===');
/* 公式底（.katex.fml-hl-* 整块铺满，笔画细 → 比行内带更显压）：浅 .21~.22 / 深 .13~.15 */
const soft = { 'hl-y-soft': ['.22', '.13'], 'hl-g-soft': ['.22', '.14'], 'hl-b-soft': ['.22', '.15'], 'hl-r-soft': ['.21', '.13'] };
const softOk = a => a >= .18 && a <= .26;
Object.keys(soft).forEach(n => {
    const v = vals(n);
    ok(n + ' 浅色 = ' + soft[n][0], v.length === 2 && has(v[0], soft[n][0]));
    ok(n + ' 深色 = ' + soft[n][1], v.length === 2 && has(v[1], soft[n][1]));
    ok(n + ' 浅色在 [.18,.26]（不压字也不消失）', softOk(alpha(v[0])));
    ok(n + ' 深色 < .18（暗底不需那么浓）', alpha(v[1]) < .18);
});
const block = { 'hl-y-block': ['.16', '.13'], 'hl-g-block': ['.18', '.14'], 'hl-b-block': ['.18', '.15'], 'hl-r-block': ['.16', '.13'] };
Object.keys(block).forEach(n => {
    const v = vals(n);
    ok(n + ' 浅色回到 ' + block[n][0], v.length === 2 && has(v[0], block[n][0]));
    ok(n + ' 深色回到 ' + block[n][1], v.length === 2 && has(v[1], block[n][1]));
    ok(n + ' 浅色 ≥ .16（不再是 .12 档）', alpha(v[0]) >= .16);
});
ok('旧 --hl-y-soft: rgba(224, 176, 110, .32) 退场', no(css, '--hl-y-soft: rgba(224, 176, 110, .32)'));
ok('11-11 回调档 --hl-y-soft .30 已退场（公式压字）', no(css, '--hl-y-soft: rgba(224, 176, 110, .30)'));
ok('11-11 回调档深色 --hl-y-soft .18 已退场', no(css, '--hl-y-soft: rgba(224, 176, 110, .18)'));
ok('11-10 过淡 --hl-y-block .12 退场', no(css, '--hl-y-block: rgba(224, 176, 110, .12)'));
ok('上一轮用户选定的主色 --mk-y 仍为 #ffe8b8', has(vals('mk-y')[0] || '', '#ffe8b8'));

console.log('=== 4. mark 规则：带高锁死 46% + 淡下划线 ===');
const mk = body('mark.mk {');
ok('mark.mk 厚度仍为 1px', has(mk, 'text-decoration-thickness: 1px'));
ok('mark.mk 下划线 offset 仍为 4px', has(mk, 'text-underline-offset: 4px'));
ok('mark.mk 仍是 underline', has(mk, 'text-decoration-line: underline'));
const mkMap = { 'mark.mk-y': 'mk-y-line', 'mark.mk-g': 'mk-g-line', 'mark.mk-b': 'mk-b-line', 'mark.mk-r': 'mk-r-line' };
Object.keys(mkMap).forEach(sel => {
    const b = body(sel + ' {');
    ok(sel + ' 底色带 = 46%', bandPct(b) === BAND);
    ok(sel + ' 带高未被改动（本轮只调 alpha）', visibleBand(bandPct(b)));
    ok(sel + ' 不再有 52% 带', no(b, '52%'));
    ok(sel + ' 不再是 30%/36% 过淡带', no(b, '0 30%, transparent 30%') && no(b, '0 36%, transparent 36%'));
    ok(sel + ' 下划线用 ' + mkMap[sel], has(b, 'text-decoration-color: var(--' + mkMap[sel] + ')'));
});
ok('含 KaTeX 仍整段取消下划线', has(css, 'mark.mk:has(.katex), mark.note-hl:has(.katex) { text-decoration-line: none; }'));
ok('含 KaTeX 的 mark.mk 也是 46% 带', bandPct(body('mark.mk:has(.katex) {')) === BAND);
ok('含 KaTeX 的 note-hl 仍用 --nhl-bg 且 46% 带', has(css, 'mark.note-hl:has(.katex) { background: linear-gradient(to top, var(--nhl-bg, var(--nhl)) 0 46%, transparent 46%); }'));
ok('全文 mark 规则不再出现 52% 实心带', no(css, '0 52%, transparent 52%'));
ok('全文 mark 规则不再出现 30% 过淡带', no(css, '0 30%, transparent 30%'));
ok('全文 mark 规则不再出现 36% 中间档', no(css, '0 36%, transparent 36%'));

console.log('=== 5. mark.note-hl：--nhl-bg 由 JS 定 .72（不动 common.js） ===');
const nh = body('mark.note-hl {');
ok('背景仍用 --nhl-bg（半透明，不是不透明 --nhl）', has(nh, 'var(--nhl-bg, var(--nhl))'));
ok('带高 = 46%', bandPct(nh) === BAND);
ok('不再用不透明 --nhl 涂 52%', no(nh, '0 52%'));
ok('color-mix 40% 淡下划线保留', has(nh, 'color-mix(in srgb, var(--nhl-line, var(--nhl)) 40%, transparent)'));
ok('保留实色 fallback（老浏览器不更差）', has(nh, 'text-decoration-color: var(--nhl-line, var(--nhl));'));
ok('offset 仍为 4px', has(nh, 'text-underline-offset: 4px'));
ok('令牌渲染 --nhl-bg 用 annHlRgba(c, .72)', has(js, "--nhl-bg:' + annHlRgba(c, .72)"));
ok('压字档 annHlRgba(c, .85) 退场', no(js, "annHlRgba(c, .85)"));
ok('旧 hlBg(c) 传值（.42 太淡）退场', no(js, "--nhl-bg:' + hlBg(c)"));
ok('common.js 的 hlBg 仍是 .42（6 页共用，未被误改）', has(common, ',.42)'));

console.log('=== 6. 批注编辑态 / 公式高亮 / 整块竖条（下划线档不动） ===');
const ann = body('.ann-text mark:not(.note-hl), .ann-edit mark:not(.note-hl) {');
ok('兜底显式 background 覆盖 UA 亮黄', has(ann, 'linear-gradient(to top, var(--mk-y2)'));
ok('兜底也是 46% 半高带（不是整块铺满）', bandPct(ann) === BAND);
ok('兜底改用 --mk-y2（--hl-y-soft 已专供公式 .22）', no(ann, 'var(--hl-y-soft)'));
ok('兜底排除 .note-hl，不抢 --nhl-bg（既有覆盖 bug 已修）', has(css, '.ann-text mark:not(.note-hl), .ann-edit mark:not(.note-hl) {'));
ok('border-bottom 仍是 1px 淡档', has(ann, 'border-bottom: 1px solid var(--mk-y-line)'));
ok('旧 2px solid var(--hl-y-line) 退场', no(css, 'border-bottom: 2px solid var(--hl-y-line)'));
const fmlBase = body('.katex.fml-hl-y, .katex.fml-hl-g, .katex.fml-hl-b, .katex.fml-hl-r {');
ok('公式高亮有内边距（解决「范围小」）', has(fmlBase, 'padding: 2px 4px'));
ok('公式高亮圆角 6px（配合更大底色块）', has(fmlBase, 'border-radius: 6px'));
ok('公式高亮跨行不断角', has(fmlBase, 'box-decoration-break: clone;'));
const fmlMap = { 'katex.fml-hl-y': 'mk-y-line', 'katex.fml-hl-g': 'mk-g-line', 'katex.fml-hl-b': 'mk-b-line', 'katex.fml-hl-r': 'mk-r-line' };
Object.keys(fmlMap).forEach(sel => {
    const b = body('.' + sel + ' {');
    ok(sel + ' 底部线仍是 1px 淡档', has(b, 'inset 0 -1px 0 var(--' + fmlMap[sel] + ')'));
    ok(sel + ' 不再各自写死 4px 圆角', no(b, 'border-radius: 4px'));
});
ok('旧 inset 0 -2px 实线全部退场', no(css, 'inset 0 -2px 0 var(--hl-y-line)'));
const pMap = { 'p.hl-y': 'mk-y-line', 'p.hl-g': 'mk-g-line', 'p.hl-b': 'mk-b-line', 'p.hl-r': 'mk-r-line' };
Object.keys(pMap).forEach(sel => {
    const b = body(sel + ' {');
    ok(sel + ' 竖条仍是 2px 淡档', has(b, 'inset 2px 0 0 var(--' + pMap[sel] + ')'));
});
ok('旧 3px 实色竖条退场', no(css, 'inset 3px 0 0 var(--hl-y-line)'));

console.log('=== 7. annotate.js 三处行内样式同步（CSS 覆盖不到） ===');
ok('新增 hlLineSoft 助手', has(js, 'function hlLineSoft(hex)'));
ok('hlLineSoft 输出仍是 40% 不透明度', has(js, ",.4)'"));
ok('annSoftenHl 用 annHlRgba(hexc, .72)', has(js, 'annHlRgba(hexc, .72)'));
ok('annSoftenHl 用 46% 带', has(js, "annHlRgba(hexc, .72) + ' 0 46%,transparent 46%)'"));
ok('annSoftenHl 用 1px 淡线', has(js, "'1px solid ' + hlLineSoft(hexc)"));
ok('令牌渲染用 annHlRgba(mf[2], .72)', has(js, 'annHlRgba(mf[2], .72)'));
ok('令牌渲染用 46% 带', has(js, "annHlRgba(mf[2], .72) + ' 0 46%,transparent 46%)"));
ok('令牌渲染用 hlLineSoft(mf[2])', has(js, 'hlLineSoft(mf[2])'));
ok('旧 0 52%,transparent 52% 内联串退场', no(js, '0 52%,transparent 52%'));
ok('11-10 过淡 0 30%,transparent 30% 内联串退场', no(js, '0 30%,transparent 30%'));
ok('11-11 中间档 0 36%,transparent 36% 退场', no(js, '0 36%,transparent 36%'));
ok('11-10 过淡 .55 内联串退场', no(js, 'annHlRgba(hexc, .55)') && no(js, 'annHlRgba(mf[2], .55)'));
ok('11-11 压字档 .85 内联串退场', no(js, 'annHlRgba(hexc, .85)') && no(js, 'annHlRgba(mf[2], .85)'));
ok("旧 '2px solid rgb(' 内联串退场", no(js, "'2px solid rgb('"));
ok('旧 hlLine(mf[2]) 实线退场', no(js, "border-bottom:1px solid ' + hlLine(mf[2])"));
ok('ANN_HLS 色板值未动（首格淡杏黄）', has(js, "const ANN_HLS = ['#ffe8b8', '#d3f9d8', '#d0ebff', '#ffe3e3', '#ffdcc4']"));

console.log('=== 8. 范围边界：共享函数与其它页色板未动 ===');
ok('common.js hlBg 仍为 .42', has(common, ',.42)'));
ok('common.js hlLine 仍返回实色 rgb', has(common, "return 'rgb('"));
ok('题库页 NOTE_HLS 未动', has(catjs, 'NOTE_HLS'));
ok('拼卷 PP_NOTE_HLS 未动', has(catjs, 'PP_NOTE_HLS'));
ok('题库/拼卷旧黄 #fff3bf 仍在（本次范围外）', has(catjs, '#fff3bf'));
ok('exam.css 的 note-hl 规则未被波及', has(examcss, '--nhl-line'));

console.log('=== 9. 变异反向验证（证明断言不是恒真） ===');
const mutCss = css
    .replace('--mk-y2: rgba(255, 226, 171, .74);', '--mk-y2: #ffe2ab;')
    .replace('text-underline-offset: 4px;', 'text-underline-offset: 3px;')
    .replace('border-bottom: 1px solid var(--mk-y-line);', 'border-bottom: 2px solid var(--hl-y-line);')
    .replace('0 46%, transparent 46%); text-decoration-color: var(--mk-y-line);', '0 30%, transparent 30%); text-decoration-color: var(--mk-y-line);');
ok('变异①：实心 --mk-y2 会被「rgba 半透明」断言拒绝', !/^rgba\(/.test(vals('mk-y2', mutCss)[0] || ''));
ok('变异②：offset 3px 会被「4px」断言拒绝', no(body('mark.mk {', mutCss), 'text-underline-offset: 4px'));
ok('变异③：2px 实线会被「1px 淡档」断言拒绝', no(body('.ann-text mark:not(.note-hl), .ann-edit mark:not(.note-hl) {', mutCss), '1px solid var(--mk-y-line)'));
ok('变异④：mk-y 带高改 30% 会被「带高锁死 46%」断言拒绝', !visibleBand(bandPct(body('mark.mk-y {', mutCss))));
const mutBand36 = css.replace('0 46%, transparent 46%); text-decoration-color: var(--mk-y-line);', '0 36%, transparent 36%); text-decoration-color: var(--mk-y-line);');
ok('变异④b：带高改 36% 同样被拒绝（带高不参与调参）', !visibleBand(bandPct(body('mark.mk-y {', mutBand36))));
const mutCss2 = css.replace('--mk-y2: rgba(255, 226, 171, .74);', '--mk-y2: rgba(255, 226, 171, .55);');
ok('变异⑤：alpha 过淡 .55 会被窗口断言拒绝', !alphaOk(alpha(vals('mk-y2', mutCss2)[0])));
const mutCss3 = css.replace('--mk-y2: rgba(255, 226, 171, .74);', '--mk-y2: rgba(255, 226, 171, .88);');
ok('变异⑤b：alpha 压字档 .88 同样被拒绝', !alphaOk(alpha(vals('mk-y2', mutCss3)[0])));
const mutJs = js
    .replace('annHlRgba(hexc, .72)', 'hexc')
    .replace('annHlRgba(mf[2], .72)', 'mf[2]')
    .replace("--nhl-bg:' + annHlRgba(c, .72)", "--nhl-bg:' + hlBg(c)");
ok('变异⑥：去掉 annHlRgba(hexc,.72) 会被断言拒绝', no(mutJs, 'annHlRgba(hexc, .72)'));
ok('变异⑦：去掉 annHlRgba(mf[2],.72) 会被断言拒绝', no(mutJs, 'annHlRgba(mf[2], .72)'));
ok('变异⑧：--nhl-bg 换回 hlBg(c) 会被断言拒绝', has(mutJs, "--nhl-bg:' + hlBg(c)"));
const mutFml = css.replace('padding: 2px 4px; border-radius: 6px;', 'border-radius: 6px;');
ok('变异⑨：删掉公式内边距会被「范围小」断言拒绝', no(body('.katex.fml-hl-y, .katex.fml-hl-g, .katex.fml-hl-b, .katex.fml-hl-r {', mutFml), 'padding: 2px 4px'));
const mutSoft = css.replace('--hl-y-soft: rgba(224, 176, 110, .22);', '--hl-y-soft: rgba(224, 176, 110, .30);');
ok('变异⑩：公式底回 .30 会被窗口断言拒绝', !softOk(alpha(vals('hl-y-soft', mutSoft)[0])));
ok('真实源码本身通过前面全部断言', fail === 0);

console.log('\n通过 ' + pass + ' 项，失败 ' + fail + ' 项');
process.exit(fail ? 1 : 0);
