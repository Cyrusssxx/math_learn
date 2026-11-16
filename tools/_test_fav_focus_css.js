/* fav_focus CSS 静态断言：三处目录的重点样式存在、特异性顺序正确、active 覆盖不被盖住。 */
const fs = require('fs');
const path = require('path');
const ROOT = path.dirname(__dirname);
const css = fs.readFileSync(path.join(ROOT, 'pwa/css/notes.css'), 'utf-8');

let p = 0, f = 0;
const ok = (c, m) => { if (c) p++; else { f++; console.log('  FAIL:', m); } };

// 右栏 + doc-toc（既有）
ok(css.includes('.toc-link.ff-warm .toc-name'), '缺 ff-warm 规则');
ok(css.includes('.toc-link.ff-hot .toc-name'), '缺 ff-hot 规则');
ok(css.includes('.ff-star'), '缺 ff-star 规则');
ok(css.includes('.note-article .doc-toc .toc-link.ff-hot'), '缺 doc-toc hot 规则');
ok(css.includes('.toc-link.ff-hot.active .toc-name'), '缺 active 覆盖');
ok(!css.includes(':has(> .toc-link.ff'), '不应残留 :has');
ok(/--strong/.test(css.slice(css.indexOf('.ff-star'))), 'ff-star 应用主强调色');
ok(css.indexOf('.toc-link.ff-warm') > css.indexOf('.toc-link.active {'), 'ff 规则应在 active 主规则之后');

// 左栏 tree-ch（本轮新增）
ok(css.includes('.tree-ch.ff-warm {'), '缺左栏 ff-warm 规则');
ok(css.includes('.tree-ch.ff-hot {'), '缺左栏 ff-hot 规则');
ok(css.includes('.tree-ch.ff-hot:hover'), '缺左栏 hover 保色规则（否则 hover 会把重点色刷回 text-faint）');
// 左栏基准 .tree-ch:hover 在 371 行附近，重点规则必须在它之后才能覆盖
ok(css.indexOf('.tree-ch.ff-warm {') > css.indexOf('.tree-ch:hover'),
   '左栏重点规则必须在 .tree-ch:hover 之后');
// 左栏 hover 保色必须紧跟基础重点规则之后（同级特异性靠后胜出）
ok(css.indexOf('.tree-ch.ff-hot:hover') > css.indexOf('.tree-ch.ff-hot {'),
   '左栏 hover 保色必须在基础 hot 规则之后');

console.log(`CSS：${p} 通过 / ${f} 失败`);
process.exit(f ? 1 : 0);
