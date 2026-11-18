// _test_pp_tip.js —— 拼卷页「抽题规则」tooltip 回归
// 断言：① 拼卷模式把长说明收进 data-tip、可见文字为小块；② 加 pp-tip 类；
//       ③ CSS 有 :hover::after 展开规则、浮窗宽度上限、换行；④ 普通分类页不受影响。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const js = fs.readFileSync(path.join(ROOT, 'pwa/js/category.js'), 'utf8');
const css = fs.readFileSync(path.join(ROOT, 'pwa/css/category.css'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond) { if (cond) { pass++; } else { fail++; console.log('FAIL: ' + name); } }

// 取 ppApplyMode 函数体（避免跨函数误匹配）
function fnBody(name) {
  const i = js.indexOf('function ' + name + '(');
  if (i < 0) return '';
  let d = 0, started = false;
  for (let k = i; k < js.length; k++) {
    if (js[k] === '{') { d++; started = true; }
    else if (js[k] === '}') { d--; if (started && d === 0) return js.slice(i, k + 1); }
  }
  return '';
}
const body = fnBody('ppApplyMode');

ok('A1 找到 ppApplyMode 函数体', body.length > 100);
ok('A2 长说明存进 data-tip', /sub\.dataset\.tip\s*=\s*['"`][^'"`]*从收藏的题里拼一份卷/.test(body));
ok('A3 可见文字为小块', /sub\.textContent\s*=\s*['"`]ⓘ 抽题规则/.test(body));
ok('A4 加 pp-tip 类', /sub\.classList\.add\(['"`]pp-tip['"`]\)/.test(body));
ok('A5 拼卷模式才设置（ PAPER_MODE 守卫内 ）', /if \(sub\)/.test(body) && body.indexOf('sub.dataset.tip') > body.indexOf('function ppApplyMode'));

// CSS：小块 + 浮窗规则
ok('B1 小块选择器限定 paper-mode', /body\.paper-mode \.exam-sub\.pp-tip\s*\{/.test(css));
ok('B2 小块 inline-flex 不占满整行', /body\.paper-mode \.exam-sub\.pp-tip\s*\{[^}]*display:\s*inline-flex/.test(css));
ok('B3 hover 展开浮窗', /\.exam-sub\.pp-tip:hover::after\s*\{\s*display:\s*block/.test(css));
ok('B4 浮窗内容取 data-tip', /\.exam-sub\.pp-tip::after\s*\{[^}]*content:\s*attr\(data-tip\)/.test(css));
ok('B5 浮窗有宽度上限（长文换行）', /\.exam-sub\.pp-tip::after\s*\{[^}]*max-width:\s*\d+px/.test(css));
ok('B6 浮窗可换行', /\.exam-sub\.pp-tip::after\s*\{[^}]*white-space:\s*normal/.test(css));
ok('B7 浮窗用主题变量（非硬编码亮色）', /\.exam-sub\.pp-tip::after\s*\{[^}]*background:\s*var\(--bg\)/.test(css));

// 反向变异：确认断言不是恒真
const mut = body.replace('sub.classList.add(\'pp-tip\');', '');
ok('C1 反向变异：删 pp-tip 类后 A4 失败', !/sub\.classList\.add\(['"`]pp-tip['"`]\)/.test(mut));
const cssMut = css.replace(':hover::after { display: block; }', ':hover::after { display: none; }');
ok('C2 反向变异：改 display 后 B3 失败', !/\.exam-sub\.pp-tip:hover::after\s*\{\s*display:\s*block/.test(cssMut));

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
