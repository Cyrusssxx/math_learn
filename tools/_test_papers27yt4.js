/* 27 押题王四套·第一套接入回归：结构、思路、原图、真题页加载顺序与 SW 预缓存。 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
let pass = 0, fail = 0;
function ok(cond, name) { if (cond) { pass++; console.log('  ✓ ' + name); } else { fail++; console.log('  ✗ ' + name); } }

const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/mn27_yt4_papers.json'), 'utf8'));
ok(d.length === 1, '1 套卷');
ok(d[0].id === 'mn27-yt4-1', '卷 id 为 mn27-yt4-1');
ok(d[0].group === 'mock', '标记为 mock');
ok(d[0].sections.reduce((n, s) => n + s.questions.length, 0) === 22, '共 22 题');
const qs = d[0].sections.flatMap(s => s.questions);
ok(qs.every((q, i) => q.no === i + 1), '题号连续 1..22');
ok(qs.every(q => Number.isInteger(q.siteId) && q.siteSource), '每题保留站点交叉引用');
ok(qs.every(q => q.idea && q.idea.startsWith('「思路」')), '22 题均有思路');
ok(qs.every(q => q.answer.startsWith('【答案】') && q.answer.includes('**【解】**')), '每题含答案+解析');
ok(qs.every(q => !/^\s*-\s+\S/m.test(q.stem)), '题干无 short markdown 列表');
ok(qs.filter(q => q.videos && q.videos.length).length === 0, '站点该套实际 0 条视频（不硬凑）');
const imgs = qs.filter(q => q.ansImg && q.ansImg.length);
ok(imgs.length === 1 && imgs[0].ansImg.length === 2, '1 题 2 张解析原图');
ok(imgs.every(q => q.ansImg.every(p => fs.existsSync(path.join(ROOT, 'pwa', p)))), '原图文件均存在');

const js = fs.readFileSync(path.join(ROOT, 'pwa/js/exam.js'), 'utf8');
ok(js.includes("fetch('data/mn27_yt4_papers.json')"), '真题页并行加载 27 押题王数据');
ok(js.indexOf('mn26_papers.json') < js.indexOf('mn27_yt4_papers.json')
   && js.indexOf('mn27_yt4_papers.json') < js.indexOf('mn27_papers.json'),
   '加载顺序：26 → 27押题王 → 27精选');
const sw = fs.readFileSync(path.join(ROOT, 'pwa/sw.js'), 'utf8');
ok(sw.includes("'data/mn27_yt4_papers.json'"), 'SW 预缓存新数据文件');
imgs.forEach(q => q.ansImg.forEach(p => ok(sw.includes("'" + p + "'"), 'SW 预缓存 ' + p)));

console.log(`\n结果：通过 ${pass}，失败 ${fail}`);
process.exit(fail ? 1 : 0);
