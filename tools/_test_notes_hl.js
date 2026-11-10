/* 笔记主页个人批注高亮配色断言（2026-11-10）
 * 纯静态源文本断言 + 变异反向验证，不依赖 jsdom（jsdom 不解析 CSS 变量 / color-mix）。
 * 运行：node tools/_test_notes_hl.js
 * 覆盖：notes.css 浅/深两套变量与全部 mark / 公式 / 整块 / 编辑态规则、
 *       annotate.js 两处行内样式、范围边界（题库/拼卷色板、共享 hlBg/hlLine 不动）。
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

console.log('=== 1. 浅色 / 深色变量：半透明底色 ===');
const bandNames = ['mk-y2', 'mk-g2', 'mk-b2', 'mk-r2'];
const bandAlpha = { 'mk-y2': ['.55', '.62'], 'mk-g2': ['.52', '.60'], 'mk-b2': ['.52', '.60'], 'mk-r2': ['.52', '.60'] };
bandNames.forEach(n => {
    const v = vals(n);
    ok(n + ' 有浅/深两份', v.length === 2);
    ok(n + ' 浅色为 rgba 半透明', /^rgba\(/.test(v[0] || ''));
    ok(n + ' 深色为 rgba 半透明', /^rgba\(/.test(v[1] || ''));
    ok(n + ' 浅色 alpha = ' + bandAlpha[n][0], has(v[0] || '', bandAlpha[n][0]));
    ok(n + ' 深色 alpha = ' + bandAlpha[n][1], has(v[1] || '', bandAlpha[n][1]));
});
ok('旧实心 --mk-y2: #ffe2ab 已退场', no(css, '--mk-y2: #ffe2ab'));
ok('旧实心 --mk-g2: #bfeab0 已退场', no(css, '--mk-g2: #bfeab0'));
ok('旧实心 --mk-b2: #b3ddff 已退场', no(css, '--mk-b2: #b3ddff'));
ok('旧实心 --mk-r2: #ffbccb 已退场', no(css, '--mk-r2: #ffbccb'));

console.log('=== 2. 下划线淡档变量 --mk-*-line ===');
const lineNames = ['mk-y-line', 'mk-g-line', 'mk-b-line', 'mk-r-line'];
lineNames.forEach(n => {
    const v = vals(n);
    ok(n + ' 浅/深两份齐全', v.length === 2);
    ok(n + ' 浅色 40% 不透明度', has(v[0] || '', '.40'));
    ok(n + ' 深色 38% 不透明度', has(v[1] || '', '.38'));
});
ok('实色 --hl-*-line 仍保留（fallback / 旧用途）', vals('hl-y-line').length === 2 && has(vals('hl-y-line')[0], '#e0a94f'));

console.log('=== 3. 底色浓度：公式高亮 / 整块高亮 ===');
const soft = { 'hl-y-soft': ['.22', '.12'], 'hl-g-soft': ['.22', '.13'], 'hl-b-soft': ['.22', '.14'], 'hl-r-soft': ['.20', '.12'] };
Object.keys(soft).forEach(n => {
    const v = vals(n);
    ok(n + ' 浅色降到 ' + soft[n][0], v.length === 2 && has(v[0], soft[n][0]));
    ok(n + ' 深色降到 ' + soft[n][1], v.length === 2 && has(v[1], soft[n][1]));
});
const block = { 'hl-y-block': ['.12', '.09'], 'hl-g-block': ['.14', '.10'], 'hl-b-block': ['.14', '.11'], 'hl-r-block': ['.12', '.09'] };
Object.keys(block).forEach(n => {
    const v = vals(n);
    ok(n + ' 浅色降到 ' + block[n][0], v.length === 2 && has(v[0], block[n][0]));
    ok(n + ' 深色降到 ' + block[n][1], v.length === 2 && has(v[1], block[n][1]));
});
ok('旧 --hl-y-soft: rgba(224, 176, 110, .32) 退场', no(css, '--hl-y-soft: rgba(224, 176, 110, .32)'));
ok('旧 --hl-g-soft .34 退场', no(css, '--hl-g-soft: rgba(110, 205, 110, .34)'));
ok('上一轮用户选定的主色 --mk-y 仍为 #ffe8b8', has(vals('mk-y')[0] || '', '#ffe8b8'));

console.log('=== 4. mark 规则：30% 半透明带 + 淡下划线 ===');
const mk = body('mark.mk {');
ok('mark.mk 厚度仍为 1px', has(mk, 'text-decoration-thickness: 1px'));
ok('mark.mk 下划线 offset 3px → 4px', has(mk, 'text-underline-offset: 4px'));
ok('mark.mk 仍是 underline', has(mk, 'text-decoration-line: underline'));
const mkMap = { 'mark.mk-y': 'mk-y-line', 'mark.mk-g': 'mk-g-line', 'mark.mk-b': 'mk-b-line', 'mark.mk-r': 'mk-r-line' };
Object.keys(mkMap).forEach(sel => {
    const b = body(sel + ' {');
    ok(sel + ' 底色带降到 30%', has(b, '0 30%, transparent 30%'));
    ok(sel + ' 不再有 52% 带', no(b, '52%'));
    ok(sel + ' 下划线用 ' + mkMap[sel], has(b, 'text-decoration-color: var(--' + mkMap[sel] + ')'));
});
ok('含 KaTeX 仍整段取消下划线', has(css, 'mark.mk:has(.katex), mark.note-hl:has(.katex) { text-decoration-line: none; }'));
ok('含 KaTeX 的 note-hl 也改用 --nhl-bg', has(css, 'mark.note-hl:has(.katex) { background: linear-gradient(to top, var(--nhl-bg, var(--nhl)) 0 30%, transparent 30%); }'));
ok('全文 mark 规则不再出现 52% 实心带', no(css, '0 52%, transparent 52%'));

console.log('=== 5. mark.note-hl：修好 --nhl-bg 定义了却没用 ===');
const nh = body('mark.note-hl {');
ok('背景改用 --nhl-bg（半透明）', has(nh, 'var(--nhl-bg, var(--nhl))'));
ok('带高降到 30%', has(nh, '0 30%, transparent 30%'));
ok('不再用不透明 --nhl 涂 52%', no(nh, '0 52%'));
ok('color-mix 40% 淡下划线', has(nh, 'color-mix(in srgb, var(--nhl-line, var(--nhl)) 40%, transparent)'));
ok('保留实色 fallback（老浏览器不更差）', has(nh, 'text-decoration-color: var(--nhl-line, var(--nhl));'));
ok('offset 4px', has(nh, 'text-underline-offset: 4px'));

console.log('=== 6. 批注编辑态 / 公式高亮 / 整块竖条 ===');
const ann = body('.ann-text mark, .ann-edit mark {');
ok('显式 background 覆盖 UA 亮黄', has(ann, 'background: var(--hl-y-soft)'));
ok('border-bottom 2px 实色 → 1px 淡档', has(ann, 'border-bottom: 1px solid var(--mk-y-line)'));
ok('旧 2px solid var(--hl-y-line) 退场', no(css, 'border-bottom: 2px solid var(--hl-y-line)'));
const fmlMap = { 'katex.fml-hl-y': 'mk-y-line', 'katex.fml-hl-g': 'mk-g-line', 'katex.fml-hl-b': 'mk-b-line', 'katex.fml-hl-r': 'mk-r-line' };
Object.keys(fmlMap).forEach(sel => {
    const b = body('.' + sel + ' {');
    ok(sel + ' 底部线 1px 淡档', has(b, 'inset 0 -1px 0 var(--' + fmlMap[sel] + ')'));
});
ok('旧 inset 0 -2px 实线全部退场', no(css, 'inset 0 -2px 0 var(--hl-y-line)'));
const pMap = { 'p.hl-y': 'mk-y-line', 'p.hl-g': 'mk-g-line', 'p.hl-b': 'mk-b-line', 'p.hl-r': 'mk-r-line' };
Object.keys(pMap).forEach(sel => {
    const b = body(sel + ' {');
    ok(sel + ' 竖条 2px 淡档', has(b, 'inset 2px 0 0 var(--' + pMap[sel] + ')'));
});
ok('旧 3px 实色竖条退场', no(css, 'inset 3px 0 0 var(--hl-y-line)'));

console.log('=== 7. annotate.js 两处行内样式同步 ===');
ok('新增 hlLineSoft 助手', has(js, 'function hlLineSoft(hex)'));
ok('hlLineSoft 输出 40% 不透明度', has(js, ",.4)'"));
ok('annSoftenHl 用 annHlRgba(hexc, .55)', has(js, 'annHlRgba(hexc, .55)'));
ok('annSoftenHl 用 30% 半透明带', has(js, "annHlRgba(hexc, .55) + ' 0 30%,transparent 30%)'"));
ok('annSoftenHl 用 1px 淡线', has(js, "'1px solid ' + hlLineSoft(hexc)"));
ok('令牌渲染用 annHlRgba(mf[2], .55)', has(js, 'annHlRgba(mf[2], .55)'));
ok('令牌渲染用 hlLineSoft(mf[2])', has(js, "hlLineSoft(mf[2])"));
ok('旧 0 52%,transparent 52% 内联串退场', no(js, '0 52%,transparent 52%'));
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
    .replace('--mk-y2: rgba(255, 226, 171, .55);', '--mk-y2: #ffe2ab;')
    .replace('text-underline-offset: 4px;', 'text-underline-offset: 3px;')
    .replace('border-bottom: 1px solid var(--mk-y-line);', 'border-bottom: 2px solid var(--hl-y-line);');
ok('变异①：实心 --mk-y2 会被「rgba 半透明」断言拒绝', !/^rgba\(/.test(vals('mk-y2', mutCss)[0] || ''));
ok('变异②：offset 3px 会被「4px」断言拒绝', no(body('mark.mk {', mutCss), 'text-underline-offset: 4px'));
ok('变异③：2px 实线会被「1px 淡档」断言拒绝', no(body('.ann-text mark, .ann-edit mark {', mutCss), '1px solid var(--mk-y-line)'));
const mutJs = js
    .replace('annHlRgba(hexc, .55)', 'hexc')
    .replace('annHlRgba(mf[2], .55)', 'mf[2]');
ok('变异④：去掉 annHlRgba(hexc,.55) 会被断言拒绝', no(mutJs, 'annHlRgba(hexc, .55)'));
ok('变异⑤：去掉 annHlRgba(mf[2],.55) 会被断言拒绝', no(mutJs, 'annHlRgba(mf[2], .55)'));
ok('真实源码本身通过前面全部断言', fail === 0);

console.log('\n通过 ' + pass + ' 项，失败 ' + fail + ' 项');
process.exit(fail ? 1 : 0);
