// _test_paper_page.js —— 独立拼卷页 paper.html 回归
// 断言：① paper.html 静态骨架写死拼卷（标题/副标题/左栏/隐藏分类控件），强刷首帧不闪分类页；
//       ② PAPER_MODE 判断兼容 paper.html 路径 + 旧 ?paper=1；③ 入口链接指向新页；④ SW 预缓存含新页。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const PWA = path.join(ROOT, 'pwa');
const html = fs.readFileSync(path.join(PWA, 'paper.html'), 'utf8');
const cat = fs.readFileSync(path.join(PWA, 'category.html'), 'utf8');
const exam = fs.readFileSync(path.join(PWA, 'exam.html'), 'utf8');
const js = fs.readFileSync(path.join(PWA, 'js/category.js'), 'utf8');
const sw = fs.readFileSync(path.join(PWA, 'sw.js'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond) { if (cond) pass++; else { fail++; console.log('FAIL: ' + name); } }

// ① 静态骨架写死拼卷（JS 未执行时就是拼卷 → 强刷不闪分类页）
ok('A1 存在 paper.html', html.length > 5000);
ok('A2 title 拼卷', /<title>🎲 拼卷 · 随机收藏题<\/title>/.test(html));
ok('A3 顶栏标题写死拼卷', /<div class="exam-title">🎲 拼卷<\/div>/.test(html));
ok('A4 无分类页标题骨架', !/<div class="exam-title">分类题库<\/div>/.test(html));
ok('A5 副标题写死 tooltip 小块', /id="examSub" data-tip=[^>]*>ⓘ 抽题规则<\/div>/.test(html));
ok('A6 左栏标题写死历史拼卷', /<div class="exam-side-title">历史拼卷<\/div>/.test(html));
ok('A7 无知识点分类骨架', !/<div class="exam-side-title">知识点分类<\/div>/.test(html));
ok('A8 左栏容器直接是 paperList', /<div id="catTree"><div id="paperList"><\/div><\/div>/.test(html));
ok('A9 分类专属按钮静态 hidden', /id="srcToggle" hidden/.test(html) && /id="unmarkedFirst" hidden/.test(html) && /id="yearSortBtn" hidden/.test(html));
ok('A10 cat-marks 静态 hidden', /<div class="cat-marks" hidden>/.test(html));
ok('A11 无指向自身的拼卷链接', !/href="category\.html\?paper=1"/.test(html));
ok('A12 返回分类题库入口', /href="category\.html"[^>]*>🗂 分类题库<\/a>/.test(html));
ok('A13 主区首屏拼卷占位', /🎲 正在准备拼卷…/.test(html));
ok('A14 背景页标识 paper', /const PAGE_ID = 'paper'/.test(html));
ok('A15 背景作用域含 paper', /\{ id: 'paper', label: '拼卷页' \}/.test(html));
ok('A16 保留必要脚本引用', /src="js\/common\.js/.test(html) && /src="js\/category\.js/.test(html));

// ② 模式判断兼容
ok('B1 PAPER_MODE 识别 paper.html', js.indexOf('paper\\.html$/i.test(location.pathname)') >= 0);
ok('B2 仍兼容旧 ?paper=1', /get\('paper'\) === '1'/.test(js));
ok('B3 两入口用 || 连接', /location\.pathname\)\s*\|\|\s*new URLSearchParams/.test(js));
ok('B4 renderTree 守卫仍在', /if \(PAPER_MODE \|\| HEART_MODE\) return;/.test(js));

// ③ 入口链接
ok('C1 category.html 入口改新页', /href="paper\.html"[^>]*>🎲 拼卷/.test(cat));
ok('C2 exam.html 入口改新页', /href="paper\.html"[^>]*>🎲 拼卷/.test(exam));
ok('C3 旧入口已移除', !/href="category\.html\?paper=1"/.test(cat) && !/href="category\.html\?paper=1"/.test(exam));

// ④ SW 预缓存
ok('D1 PRECACHE 含 paper.html', /'paper\.html',/.test(sw));

// 反向变异：确认断言不是恒真
const htmlMut = html.replace('<div class="exam-title">🎲 拼卷</div>', '<div class="exam-title">分类题库</div>');
ok('E1 变异 A3/A4：改回分类标题后断言翻转', /<div class="exam-title">分类题库<\/div>/.test(htmlMut) && !/<div class="exam-title">分类题库<\/div>/.test(html));
const jsMut = js.replace(/\(?:^\|\\\/\)paper\\\.html\$\/i\.test\(location\.pathname\)\s*\|\|\s*/, '');
ok('E2 变异 B1：删 pathname 判断后 B1 失败', !/paper\.html\$\/i\.test\(location\.pathname\)/.test(jsMut));

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
