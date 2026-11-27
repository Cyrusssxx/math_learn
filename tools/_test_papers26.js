/* 26 押题王四套接入回归：数据结构、视频/原图字段、真题页加载顺序与视频按钮。 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
let pass = 0, fail = 0;
function ok(cond, name) { if (cond) { pass++; console.log('  ✓ ' + name); } else { fail++; console.log('  ✗ ' + name); } }

const raw = fs.readFileSync(path.join(ROOT, 'pwa/data/mn26_papers.json'), 'utf8');
const d = JSON.parse(raw);
ok(d.length === 4, '4 套卷');
ok(d.map(p => p.id).join(',') === 'mn26-1,mn26-2,mn26-3,mn26-4', '卷 id 连续');
ok(d.every(p => p.group === 'mock'), '全部标记为 mock');
ok(d.every(p => p.sections.reduce((n, s) => n + s.questions.length, 0) === 22), '每套 22 题');
const qs = d.flatMap(p => p.sections.flatMap(s => s.questions));
ok(qs.length === 88, '共 88 题');
ok(qs.every(q => Number.isInteger(q.siteId) && q.siteSource), '每题保留站点交叉引用');
ok(qs.every(q => q.answer.startsWith('【答案】') && q.answer.includes('**【解】**')), '每题含答案+完整解析');
const withVideo = qs.filter(q => q.videos && q.videos.length);
ok(withVideo.length === 2, '2 题带视频链接');
ok(withVideo.every(q => q.videos.every(v => v.url && v.label && ['confirmed', 'candidate'].includes(v.status))), '视频字段结构完整');
const withImg = qs.filter(q => q.ansImg && q.ansImg.length);
const imgCount = withImg.reduce((n, q) => n + q.ansImg.length, 0);
ok(withImg.length === 87 && imgCount === 124, '87 题 124 张解析原图（站抓 7 + 答案册 PDF 117）');
const pdfImgs = withImg.flatMap(q => q.ansImg.filter(p => p.includes('mn26pdf-')));
ok(pdfImgs.length === 117, '答案册 PDF 逐题原图 117 张');
ok(!qs.some(q => q.no === 21 && q.id === 'mn26-4' && q.ansImg), '第4套 Q21 原书缺页无原图');
ok(withImg.every(q => q.ansImg.every(p => fs.existsSync(path.join(ROOT, 'pwa', p)))), '原图文件均存在');

const js = fs.readFileSync(path.join(ROOT, 'pwa/js/exam.js'), 'utf8');
ok(js.includes("fetch('data/mn26_papers.json')"), '真题页并行加载 mn26 数据');
ok(js.indexOf('mn26_papers.json') < js.indexOf('mn27_papers.json'), '26 数据在 27 之前加载');
ok(js.includes('examVideoBtnHtml(q)'), '题卡渲染视频按钮');
ok(js.includes('function examOpenVideoModal'), '视频弹窗函数存在');
const sw = fs.readFileSync(path.join(ROOT, 'pwa/sw.js'), 'utf8');
ok(sw.includes("'data/mn26_papers.json'"), 'SW 预缓存新数据文件');
withImg.forEach(q => q.ansImg.forEach(p => ok(sw.includes("'" + p + "'"), 'SW 预缓存 ' + p)));

console.log(`\n结果：通过 ${pass}，失败 ${fail}`);
process.exit(fail ? 1 : 0);
