// _test_pp_note_tip_and_storage.js —— 拼卷页「未收藏 N 题」tooltip + 左栏串页修复回归
// 断言：① 未收藏提示收进 data-tip、可见为小块；② CSS 窄版浮窗（限宽防裁切）；
//       ③ renderTree 有 PAPER_MODE/HEART_MODE 守卫；④ storage 回调拼卷分支只刷进度不 renderTree；
//       ⑤ 普通分类页 storage 仍走 renderTree（反向：守卫不误伤）。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const js = fs.readFileSync(path.join(ROOT, 'pwa/js/category.js'), 'utf8');
const css = fs.readFileSync(path.join(ROOT, 'pwa/css/category.css'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond) { if (cond) pass++; else { fail++; console.log('FAIL: ' + name); } }

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
const prog = fnBody('ppProgHtml');
const tree = fnBody('renderTree');
const storageAt = js.indexOf("window.addEventListener('storage'");
const storageSeg = storageAt >= 0 ? js.slice(storageAt, storageAt + 900) : '';

// ① 未收藏提示 tooltip
ok('A1 找到 ppProgHtml', prog.length > 100);
ok('A2 未收藏提示收进 data-tip', /pp-note-tip[^>]*data-tip=[^>]*不熟\/不会但未收藏，不参与抽题/.test(prog));
ok('A3 可见文字为小块', /class="pp-note-tip"/.test(prog) && /ⓘ 未收藏 \$\{noFav\} 题/.test(prog));
ok('A4 用 noFav 计数且条件渲染', /未收藏 \$\{noFav\} 题/.test(prog) && /if \(noFav\) h \+=/.test(prog));
ok('A5 旧的整行 pp-pg-note 说明已移除', !/class="pp-pg-note">另有 \$\{noFav\}/.test(prog));

// ② CSS 窄版浮窗
ok('B1 小块选择器限定 paper-mode', /body\.paper-mode \.pp-note-tip\s*\{/.test(css));
ok('B2 小块 inline-flex', /body\.paper-mode \.pp-note-tip\s*\{[^}]*display:\s*inline-flex/.test(css));
ok('B3 hover 展开浮窗', /\.pp-note-tip:hover::after\s*\{\s*display:\s*block/.test(css));
ok('B4 浮窗内容取 data-tip', /\.pp-note-tip::after\s*\{[^}]*content:\s*attr\(data-tip\)/.test(css));
ok('B5 浮窗限宽 <=200px（左栏 200px 防裁切）', /\.pp-note-tip::after\s*\{[^}]*width:\s*(1\d\d|200)px/.test(css));
ok('B6 浮窗可换行', /\.pp-note-tip::after\s*\{[^}]*white-space:\s*normal/.test(css));
ok('B7 浮窗用主题变量', /\.pp-note-tip::after\s*\{[^}]*background:\s*var\(--bg\)/.test(css));

// ③ renderTree 模式守卫
ok('C1 找到 renderTree', tree.length > 100);
ok('C2 守卫 PAPER_MODE', /if \(PAPER_MODE \|\| HEART_MODE\) return;/.test(tree));
ok('C3 守卫在 activeEntries 之前', tree.indexOf('if (PAPER_MODE') < tree.indexOf('const entries = activeEntries'));

// ④ storage 拼卷分支
ok('D1 storage 回调存在', storageSeg.length > 100);
ok('D2 拼卷分支只刷进度+主区', /else if \(PAPER_MODE\) \{ ppSide\(\); renderMain\(\); \}/.test(storageSeg));
ok('D3 拼卷分支不调 renderTree', !/else if \(PAPER_MODE\) \{[^}]*renderTree\(\)/.test(storageSeg));
ok('D4 普通页仍走 renderTree', /else \{ renderTree\(\); renderMain\(\); \}/.test(storageSeg));
ok('D5 REVIEW/HEART 分支保留', /if \(REVIEW_MODE\) \{ renderReview\(\); renderNav\(\); \}/.test(storageSeg) && /else if \(HEART_MODE\) \{ renderHeart\(\); renderNav\(\); \}/.test(storageSeg));

// 反向变异：确认断言不是恒真
const cssMut = css.replace('width: 158px; white-space: normal; word-break: break-all;', 'width: 420px; white-space: nowrap;');
ok('E1 变异 B5/B6：放宽浮窗宽度后限宽断言失败', !/\.pp-note-tip::after\s*\{[^}]*width:\s*(1\d\d|200)px/.test(cssMut));
const prodMut = js.replace('else if (PAPER_MODE) { ppSide(); renderMain(); }', 'else { renderTree(); renderMain(); }');
const storageMut = prodMut.slice(prodMut.indexOf("window.addEventListener('storage'"), prodMut.indexOf("window.addEventListener('storage'") + 900);
ok('E2 变异 D2/D3：去掉拼卷分支后分支断言失败', !/else if \(PAPER_MODE\) \{ ppSide\(\); renderMain\(\); \}/.test(storageMut));
const treeMut = tree.replace('if (PAPER_MODE || HEART_MODE) return;', '');
ok('E3 变异 C2：删守卫后 C2 失败', !/if \(PAPER_MODE \|\| HEART_MODE\) return;/.test(treeMut));

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
