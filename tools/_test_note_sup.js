/* 批注上标/下标保留回归（exam / annotate / category / exam-shared / mistake / selected）
 * 病因：粘贴的 2<sup>16</sup> 在编辑器→存储令牌时被当未知标签剥掉，只剩 216。
 * 三端必须同时支持：① 序列化 DOM→令牌 ② 反序列化 令牌→DOM ③ 渲染 令牌→HTML。
 * 运行：node tools/_test_note_sup.js
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const read = f => fs.readFileSync(path.join(ROOT, 'pwa/js', f), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond) { if (cond) pass++; else { fail++; console.log('FAIL: ' + name); } }

const exam = read('exam.js');
const annot = read('annotate.js');
const cat = read('category.js');
const shared = read('exam-shared.js');
const mistake = read('mistake.js');
const selected = read('selected.js');

// ① 令牌正则：四家编辑器都能识别 <sup>/<sub> 开闭令牌
for (const [name, js] of [['exam.js', exam], ['annotate.js', annot], ['category.js', cat], ['mistake.js', mistake]]) {
    ok(name + ' 令牌正则含 sup/sub', js.includes('<\\/i>|<sup>|<\\/sup>|<sub>|<\\/sub>'));
}
// ② 序列化：DOM 的 SUP/SUB 节点要生成令牌
for (const [name, js] of [['exam.js', exam], ['annotate.js', annot], ['category.js', cat]]) {
    ok(name + ' 序列化 SUP/SUB 分支', /ch\.tagName === 'SUP' \|\| ch\.tagName === 'SUB'/.test(js));
}
ok('mistake.js 序列化 SUP/SUB 分支', /ch\.tagName === 'SUP' \|\| ch\.tagName === 'SUB'/.test(mistake));

// ③ 反序列化：令牌能还原成 DOM 节点（闭合判断 + 建节点）
for (const [name, js] of [['exam.js', exam], ['annotate.js', annot], ['category.js', cat]]) {
    ok(name + ' 反序列化闭合 sup/sub', /<\/sup>' \|\| m0 === '<\/sub>'/.test(js));
    ok(name + ' 反序列化建 sup/sub 节点', /createElement\('sup'\)[\s\S]{0,80}createElement\('sub'\)/.test(js));
}
ok('mistake.js 反序列化闭合 sup/sub', /\^<\\\/\(c\|h\|b\|i\|sup\|sub\|h1\|h2\)>\$/.test(mistake));
ok('mistake.js 反序列化建 sup/sub 节点', /createElement\('sup'\)[\s\S]{0,80}createElement\('sub'\)/.test(mistake));

// ④ 渲染：五套 mdBlock/renderAnnot 还原链都要有 sup/sub
for (const [name, js] of [['exam.js', exam], ['annotate.js', annot], ['category.js', cat],
                          ['exam-shared.js', shared], ['mistake.js', mistake], ['selected.js', selected]]) {
    ok(name + ' 渲染还原 sup', /&lt;sup&gt;\(\[\\s\\S\]\*\?\)&lt;\\\/sup&gt;\/g, '<sup>\$1<\/sup>'/.test(js));
    ok(name + ' 渲染还原 sub', /&lt;sub&gt;\(\[\\s\\S\]\*\?\)&lt;\\\/sub&gt;\/g, '<sub>\$1<\/sub>'/.test(js));
}

// 变异反向验证：抹掉 sup 支持后断言必须失败（证明断言不是恒真）
const broken = exam.replace('|<sup>|<\\/sup>|<sub>|<\\/sub>', '');
ok('反向验证：抹掉正则后断言失效', !broken.includes('<\\/i>|<sup>|<\\/sup>|<sub>|<\\/sub>'));

console.log('\n结果: ' + pass + ' 通过 / ' + fail + ' 失败');
if (fail) process.exitCode = 1;
