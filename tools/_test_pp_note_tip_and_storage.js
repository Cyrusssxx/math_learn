// _test_pp_note_tip_and_storage.js —— 拼卷进度提示移除 + 左栏串页修复回归
// 断言：① 「未收藏 N 题」tooltip 已彻底移除（JS + CSS 均无残留）；
//       ② renderTree 有 PAPER_MODE/HEART_MODE 守卫；③ storage 回调拼卷分支只刷进度不 renderTree；
//       ④ 普通分类页 storage 仍走 renderTree（反向：守卫不误伤）。
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

// ① 未收藏提示 tooltip 已移除
ok('A1 找到 ppProgHtml', prog.length > 100);
ok('A2 JS 无 pp-note-tip 小块', !/pp-note-tip/.test(prog));
ok('A3 JS 无「未收藏 N 题」文案', !/未收藏 \$\{noFav\}|不参与抽题/.test(prog));
ok('A4 JS 无 noFav 局部变量残留', !/const noFav/.test(prog));
ok('A5 CSS 无 pp-note-tip 样式残留', !/\.pp-note-tip/.test(css));
ok('A6 抽完提示 pp-pg-note.warn 保留', /class="pp-pg-note warn"/.test(prog));

// ② renderTree 模式守卫
ok('B1 找到 renderTree', tree.length > 100);
ok('B2 守卫 PAPER_MODE', /if \(PAPER_MODE \|\| HEART_MODE\) return;/.test(tree));
ok('B3 守卫在 activeEntries 之前', tree.indexOf('if (PAPER_MODE') < tree.indexOf('const entries = activeEntries'));

// ③ storage 拼卷分支
ok('C1 storage 回调存在', storageSeg.length > 100);
ok('C2 拼卷分支只刷进度+主区', /else if \(PAPER_MODE\) \{ ppSide\(\); renderMain\(\); \}/.test(storageSeg));
ok('C3 拼卷分支不调 renderTree', !/else if \(PAPER_MODE\) \{[^}]*renderTree\(\)/.test(storageSeg));
ok('C4 普通页仍走 renderTree', /else \{ renderTree\(\); renderMain\(\); \}/.test(storageSeg));
ok('C5 REVIEW/HEART 分支保留', /if \(REVIEW_MODE\) \{ renderReview\(\); renderNav\(\); \}/.test(storageSeg) && /else if \(HEART_MODE\) \{ renderHeart\(\); renderNav\(\); \}/.test(storageSeg));

// 反向变异：确认断言不是恒真
const jsMut = prog.replace('if (!rest) h +=', 'if (noFav) h += `<span class="pp-note-tip">x</span>`; if (!rest) h +=');
ok('D1 变异 A2：插回小块后 A2 失败', /pp-note-tip/.test(jsMut) && !/pp-note-tip/.test(prog));
const treeMut = tree.replace('if (PAPER_MODE || HEART_MODE) return;', '');
ok('D2 变异 B2：删守卫后 B2 失败', !/if \(PAPER_MODE \|\| HEART_MODE\) return;/.test(treeMut));
const prodMut = js.replace('else if (PAPER_MODE) { ppSide(); renderMain(); }', 'else { renderTree(); renderMain(); }');
const storageMut = prodMut.slice(prodMut.indexOf("window.addEventListener('storage'"), prodMut.indexOf("window.addEventListener('storage'") + 900);
ok('D3 变异 C2：去掉拼卷分支后 C2 失败', !/else if \(PAPER_MODE\) \{ ppSide\(\); renderMain\(\); \}/.test(storageMut));

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
