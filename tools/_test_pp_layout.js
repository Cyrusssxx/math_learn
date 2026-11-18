/* 拼卷页布局回归：主区视口内居中（不随左栏收起移动）+ 题号球固定右下角调色盘上方
 * 背景（2026-11-18 用户反馈）：
 *   ① 2026-11-17 曾把 #catMain 改成 margin-left:0 左对齐紧跟左栏，但用户收起左栏后
 *      主区贴到 x=40、右侧空 130+px →「整体题目不随左栏收起、保持居中」。
 *      改回 margin:0 auto：主区恒在视口内居中，左栏开合只影响左栏自身。
 *   ② 题号球之前 ppNavAlign() 按主区右缘动态反算 right，主区居中后收起左栏算成 110px，
 *      球飘到 x≈1095 偏离调色盘正上方。现改为固定：清除内联 right，回到 CSS 默认
 *      right:16px / bottom:82px（刷题页同款），恒钉在 🎨 背景按钮正上方。
 * 跑法：node tools/_test_pp_layout.js
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const CSS = fs.readFileSync(path.join(ROOT, 'pwa/css/category.css'), 'utf8');
const EXAMCSS = fs.readFileSync(path.join(ROOT, 'pwa/css/exam.css'), 'utf8');
const JS = fs.readFileSync(path.join(ROOT, 'pwa/js/category.js'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✓ ' + name); }
  else { fail++; console.log('  ✗ ' + name + (extra ? '\n      ' + extra : '')); }
}

/* 去掉注释后抽规则块，避免注释里的括号干扰 */
function ruleBlock(css, sel) {
  const clean = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const i = clean.indexOf(sel);
  if (i < 0) return null;
  const open = clean.indexOf('{', i);
  const close = clean.indexOf('}', open);
  if (open < 0 || close < 0) return null;
  return clean.slice(open + 1, close);
}
const mainRule = ruleBlock(CSS, 'body.paper-mode #catMain');

console.log('\n[A] 主区视口内居中（不随左栏收起移动）');
ok('A1 存在 body.paper-mode #catMain 规则块', mainRule !== null);
ok('A2 margin-left: auto（居中，非 0 左对齐）',
   mainRule !== null && /margin-left\s*:\s*auto/.test(mainRule), mainRule);
ok('A3 margin-right: auto（居中）',
   mainRule !== null && /margin-right\s*:\s*auto/.test(mainRule), mainRule);
ok('A4 仍有 max-width（避免超宽行长）',
   mainRule !== null && /max-width\s*:\s*\d+px/.test(mainRule), mainRule);
ok('A5 padding-right ≥ 82px（题卡右侧 58px 外挂状态竖条 + 间隙）',
   mainRule !== null && (() => {
     const m = mainRule.match(/padding-right\s*:\s*(\d+)px/);
     return m && Number(m[1]) >= 82;
   })(), mainRule);
ok('A6 没有 margin-left: 0 残留（会破坏居中）',
   mainRule !== null && !/margin-left\s*:\s*0\b/.test(mainRule), mainRule);
ok('A7 没有 margin:0 auto 简写后又被覆盖的风险（本规则同时含 left/right auto）',
   mainRule !== null && /margin-left\s*:\s*auto[\s\S]*margin-right\s*:\s*auto/.test(mainRule), mainRule);

console.log('\n[B] 题号球固定右下角（清除内联 right，回 CSS 默认）');
ok('B1 定义了 ppNavAlign()', /function ppNavAlign\s*\(\s*\)/.test(JS));
ok('B2 ppNavAlign 取 #ppNav 且无 style 时安全退出（不再依赖 #catMain 右缘）',
   /function ppNavAlign[\s\S]{0,300}?getElementById\('ppNav'\)[\s\S]{0,120}?!d\s*\|\|\s*!d\.style/.test(JS));
ok('B3 ppNavAlign 清除内联 right（d.style.right = \'\'）',
   /function ppNavAlign[\s\S]{0,500}?d\.style\.right\s*=\s*''/.test(JS));
ok('B4 不再读主区 getBoundingClientRect（ ceased 跟随主区）',
   !/function ppNavAlign[\s\S]{0,600}?getBoundingClientRect\(\)/.test(JS));
ok('B5 不再读 paddingRight（不再反算题卡右缘）',
   !/function ppNavAlign[\s\S]{0,600}?paddingRight/.test(JS));
ok('B6 不再 Math.max 动态下限（固定值无需下限保护）',
   !/function ppNavAlign[\s\S]{0,900}?Math\.max\(\s*16\s*,/.test(JS));
ok('B7 只清 right，不动 bottom（bottom:82px 与 🎨 互让）',
   !/function ppNavAlign[\s\S]{0,900}?\.style\.bottom\s*=/.test(JS));

console.log('\n[C] 题号球默认定位（CSS 固定值）');
const fqRule = ruleBlock(EXAMCSS, '.float-q {');
ok('C1 .float-q position: fixed', fqRule !== null && /position\s*:\s*fixed/.test(fqRule), fqRule);
ok('C2 .float-q right: 16px（视口右下角）',
   fqRule !== null && /right\s*:\s*16px/.test(fqRule), fqRule);
ok('C3 .float-q bottom: 82px（🎨 背景按钮正上方）',
   fqRule !== null && /bottom\s*:\s*82px/.test(fqRule), fqRule);
ok('C4 调色盘 .bg-fab 也在右下（与题号球同一列）',
   /\.bg-fab\s*\{[^}]*right\s*:\s*1[68]px[^}]*bottom\s*:\s*1[48]px/.test(CSS));

console.log('\n[D] 调用时机（保留，清 right 幂等）');
function fnBody(name) {
  const i = JS.indexOf('function ' + name);
  if (i < 0) return '';
  const j = JS.indexOf('\nfunction ', i + 10);
  return JS.slice(i, j < 0 ? JS.length : j);
}
const rnBody = fnBody('ppRenderNav');
const sideBody = fnBody('applySideState');
ok('D1 ppRenderNav 重建题号后调用 ppNavAlign', /ppNavAlign\(\)/.test(rnBody), rnBody.slice(-200));
ok('D2 窗口 resize 时调用 ppNavAlign',
   /addEventListener\('resize',\s*\(\)\s*=>\s*\{[^}]*ppNavAlign\(\)/.test(JS));
ok('D3 左栏收起/展开后调用 ppNavAlign（applySideState 内）', /ppNavAlign\(\)/.test(sideBody), sideBody);

console.log('\n[E] 不污染其他页面');
ok('E1 主区规则限定 body.paper-mode（不影响分类页/复测页/♥页）',
   /body\.paper-mode #catMain/.test(CSS));
ok('E2 没有无作用域的 #catMain 居中覆盖',
   !/(^|\n)\s*#catMain\s*\{[^}]*margin-left\s*:\s*auto/.test(CSS));

console.log('\n================ 结果: ' + pass + ' 通过 / ' + fail + ' 失败 ================');
process.exit(fail ? 1 : 0);
