/* 回归测试：拼卷页顶栏强制展开（2026-11-17 用户截图反馈）
 * 校验三点：
 *  A. category.js 源码里 restoreTopBar 对 PAPER_MODE 分支直接展开 DOM
 *  B. 该分支不写 localStorage（不污染跨页折叠偏好）
 *  C. 非拼卷页仍从 localStorage 恢复折叠状态（原行为不变）
 */
const fs = require('fs');
const path = require('path');

const SRC = fs.readFileSync(path.resolve(__dirname, '../pwa/js/category.js'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond, extra) {
    if (cond) { pass++; console.log('  ✓ ' + name); }
    else { fail++; console.log('  ✗ ' + name + (extra ? ' — ' + extra : '')); }
}

// 抽取 restoreTopBar 函数体
const m = SRC.match(/function restoreTopBar\(\)\s*\{([\s\S]*?)\n\}/);
ok('找到 restoreTopBar 函数', !!m);
const body = m ? m[1] : '';

console.log('=== A. 拼卷页强制展开 ===');
ok('存在 PAPER_MODE 判断分支', /if\s*\(PAPER_MODE\)/.test(body));
ok('PAPER_MODE 分支移除 examTop 的 collapsed',
   /PAPER_MODE[\s\S]*?classList\.remove\(['"]collapsed['"]\)/.test(body));
ok('PAPER_MODE 分支调用 syncTopH',
   /if\s*\(PAPER_MODE\)[\s\S]*?syncTopH\(\)[\s\S]*?\n\s*\}/.test(body));
ok('PAPER_MODE 分支有 return（不走后续恢复）',
   /if\s*\(PAPER_MODE\)[\s\S]*?return;/.test(body));

console.log('=== B. 不污染跨页折叠偏好 ===');
// PAPER_MODE 分支内（return 之前）不得出现 setItem / toggleTopBar
const paperBranch = (body.match(/if\s*\(PAPER_MODE\)([\s\S]*?)\n\s*\}/) || [])[1] || '';
ok('PAPER_MODE 分支内无 localStorage.setItem',
   !/localStorage\.setItem/.test(paperBranch), paperBranch.slice(0, 100));
ok('PAPER_MODE 分支内无 toggleTopBar 调用',
   !/toggleTopBar\s*\(/.test(paperBranch));

console.log('=== C. 非拼卷页原行为不变 ===');
ok('仍从 localStorage 读 examTopCollapsed',
   /localStorage\.getItem\(TOP_COLLAPSED_KEY\)/.test(body));
ok('非拼卷页仍调用 toggleTopBar 恢复',
   /toggleTopBar\(collapsed\)/.test(body));

console.log('\n结果: ' + pass + ' 通过 / ' + fail + ' 失败');
process.exit(fail ? 1 : 0);
