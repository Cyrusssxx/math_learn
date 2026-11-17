/* 拼卷页布局回归：主区左对齐跟随左栏 + 题号球贴内容右缘
 * 背景（2026-11-17 用户反馈）：
 *   ① 1920 视口下 #catMain 被 .exam-main 的 margin:0 auto 居中 + max-width，内容被推到屏幕中部，
 *      左栏只占 200px 左侧却空 400+px →「都太靠右了」；且收起左栏(200→40)时居中只让主区左移一半，
 *      看起来像布局没跟着动。
 *   ② 题号球 .float-q 是 fixed right:16px，宽屏下钉在屏幕最角落，与内容区脱节 →「看不到右下角的题号栏」。
 * 跑法：node tools/_test_pp_layout.js
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const CSS = fs.readFileSync(path.join(ROOT, 'pwa/css/category.css'), 'utf8');
const JS = fs.readFileSync(path.join(ROOT, 'pwa/js/category.js'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✓ ' + name); }
  else { fail++; console.log('  ✗ ' + name + (extra ? '\n      ' + extra : '')); }
}

/* ---------- 抽出 body.paper-mode #catMain 规则块 ---------- */
function ruleBlock(sel) {
  // 去掉注释后再匹配，避免注释里的花括号干扰
  const clean = CSS.replace(/\/\*[\s\S]*?\*\//g, '');
  const i = clean.indexOf(sel);
  if (i < 0) return null;
  const open = clean.indexOf('{', i);
  const close = clean.indexOf('}', open);
  if (open < 0 || close < 0) return null;
  return clean.slice(open + 1, close);
}
const mainRule = ruleBlock('body.paper-mode #catMain');

console.log('\n[A] 主区左对齐（不再居中）');
ok('A1 存在 body.paper-mode #catMain 规则块', mainRule !== null);
ok('A2 margin-left: 0（不再靠 auto 居中）',
   mainRule !== null && /margin-left\s*:\s*0/.test(mainRule),
   mainRule);
ok('A3 margin-right: auto（吃剩余空间=左对齐，而非撑满）',
   mainRule !== null && /margin-right\s*:\s*auto/.test(mainRule),
   mainRule);
ok('A4 仍有 max-width（避免超宽行长）',
   mainRule !== null && /max-width\s*:\s*\d+px/.test(mainRule),
   mainRule);
ok('A5 padding-right ≥ 82px（题卡右侧 58px 外挂状态竖条 + 间隙，否则 1280 下被视口裁掉）',
   mainRule !== null && (() => {
     const m = mainRule.match(/padding-right\s*:\s*(\d+)px/);
     return m && Number(m[1]) >= 82;
   })(),
   mainRule);
ok('A6 没有残留 margin:0 auto 的简写（会覆盖 A2/A3）',
   mainRule !== null && !/(^|;)\s*margin\s*:\s*0\s+auto/.test(mainRule),
   mainRule);

console.log('\n[B] 题号球对齐函数');
ok('B1 定义了 ppNavAlign()', /function ppNavAlign\s*\(\s*\)/.test(JS));
ok('B2 ppNavAlign 无 #ppNav / 无 #catMain 时安全退出（非拼卷页会调用到）',
   /function ppNavAlign[\s\S]{0,400}?if\s*\(\s*!d\s*\|\|\s*!main\s*\)\s*return/.test(JS));
ok('B3 ppNavAlign 读主区右缘（getBoundingClientRect）',
   /function ppNavAlign[\s\S]{0,600}?getBoundingClientRect\(\)/.test(JS));
ok('B4 ppNavAlign 读主区 padding-right（扣掉内边距才是题卡右缘）',
   /function ppNavAlign[\s\S]{0,600}?paddingRight/.test(JS));
ok('B5 ppNavAlign 把结果写进 style.right（不写死 CSS，随视口重算）',
   /function ppNavAlign[\s\S]{0,900}?d\.style\.right\s*=/.test(JS));
ok('B6 有下限保护 Math.max(16, ...)（窄屏退回默认位置，不飞出视口）',
   /function ppNavAlign[\s\S]{0,900}?Math\.max\(\s*16\s*,/.test(JS));
ok('B7 只改 right，不动 bottom（bottom:82px 是与 🎨 按钮互让的位置）',
   !/function ppNavAlign[\s\S]{0,900}?\.style\.bottom\s*=/.test(JS));

console.log('\n[C] 调用时机');
/** 取某个顶层函数体（从 function xxx 到下一个顶层 function 之间），避免正则跨函数误判 */
function fnBody(name) {
  const i = JS.indexOf('function ' + name);
  if (i < 0) return '';
  const j = JS.indexOf('\nfunction ', i + 10);
  return JS.slice(i, j < 0 ? JS.length : j);
}
const rnBody = fnBody('ppRenderNav');
const sideBody = fnBody('applySideState');
ok('C1 ppRenderNav 重建题号后调用 ppNavAlign',
   /ppNavAlign\(\)/.test(rnBody), rnBody.slice(-200));
ok('C2 窗口 resize 时重算（含原有滚动高亮）',
   /addEventListener\('resize',\s*\(\)\s*=>\s*\{[^}]*ppNavAlign\(\)/.test(JS));
ok('C3 左栏收起/展开后重算（applySideState 内）',
   /ppNavAlign\(\)/.test(sideBody), sideBody);

console.log('\n[D] 不污染其他页面');
ok('D1 主区规则限定 body.paper-mode（不影响分类页/复测页/♥页）',
   /body\.paper-mode #catMain/.test(CSS));
ok('D2 没有新增无作用域的 #catMain margin 覆盖',
   !/(^|\n)\s*#catMain\s*\{[^}]*margin-left\s*:\s*0/.test(CSS));

console.log('\n================ 结果: ' + pass + ' 通过 / ' + fail + ' 失败 ================');
process.exit(fail ? 1 : 0);
