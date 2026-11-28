/* 27 张宇四套卷接入回归：结构、思路、原图（源文件顺序）、加载顺序、SW 预缓存、清洗。 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
let pass = 0, fail = 0;
function ok(cond, name) { if (cond) { pass++; console.log('  ✓ ' + name); } else { fail++; console.log('  ✗ ' + name); } }

const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/mn27_zs4_papers.json'), 'utf8'));
ok(d.length === 4, '4 套卷');
ok(d.every((p, i) => p.id === 'mn27-zs4-' + (i + 1)), '卷 id 为 mn27-zs4-1..4');
ok(d.every(p => p.group === 'mock'), '全部标记为 mock');
const qs = d.flatMap(p => p.sections.flatMap(s => s.questions));
ok(qs.length === 88, '共 88 题');
d.forEach(p => {
    const all = p.sections.flatMap(s => s.questions);
    ok(all.length === 22 && all.every((q, i) => q.no === i + 1), p.id + ' 题号连续 1..22');
});
ok(qs.every(q => Number.isInteger(q.siteId) && q.siteSource), '每题保留站点交叉引用');
ok(qs.every(q => q.idea && q.idea.startsWith('「思路」') && q.idea.length > 20), '88 题均有实质思路');
ok(qs.every(q => q.answer.startsWith('【答案】') && q.answer.includes('**【解】**')), '每题含答案+解析');
ok(qs.every(q => !/^\s*-\s+\S/m.test(q.stem)), '题干无 short markdown 列表');
ok(qs.every(q => !q.answer.includes('asset://')), '答案无残留 asset:// 引用');
ok(qs.every(q => !/数三原卷对照|数二原卷对应|原始参考答案/.test(q.answer)), '答案已剥数三/数二原卷元话语与图段标题');
ok(qs.every(q => q.answer.split('$').length % 2 === 1), '答案 $ 定界符成对');

// 原图：站点「原始参考答案」4 张（源文件顺序）+ 官方答案册 PDF 逐题切图 127 张
const imgs = qs.filter(q => q.ansImg && q.ansImg.length);
ok(imgs.length === 88, '88 题全部带答案原图');
const siteImgs = [
  ['mn27-zs4-2-11_0.png'], ['mn27-zs4-3-11_0.png'],
  ['mn27-zs4-3-20_0.png', 'mn27-zs4-3-20_1.png'],
];
const byId = (v, n) => d[v - 1].sections.flatMap(s => s.questions).find(q => q.no === n);
ok(byId(2, 11).ansImg[0].endsWith(siteImgs[0][0])
   && byId(3, 11).ansImg[0].endsWith(siteImgs[1][0])
   && byId(3, 20).ansImg[0].endsWith(siteImgs[2][0])
   && byId(3, 20).ansImg[1].endsWith(siteImgs[2][1]), '站点 4 张原图文件名与题号/序号一致');
ok(qs.every(q => q.ansImg.some(p => p.includes('mn27zs4pdf-'))), '每题均有官方答案册 PDF 切图');
let pdfCnt = 0;
d.forEach((p, vi) => p.sections.flatMap(s => s.questions).forEach(q => {
  const mine = q.ansImg.filter(x => x.includes('mn27zs4pdf-'));
  pdfCnt += mine.length;
  ok(mine.every((x, i) => x === `data/img/zx_site/mn27zs4pdf-${vi + 1}-${q.no}_${i}.png`),
     `${p.id} Q${q.no} PDF 图命名与序号连续`);
  const siteCnt = q.ansImg.length - mine.length;
  ok(q.ansImg.slice(0, siteCnt).every(x => !x.includes('mn27zs4pdf-')),
     `${p.id} Q${q.no} 站点原图仍在 PDF 图之前`);
}));
ok(pdfCnt === 127, 'PDF 切图合计 127 张');
ok(qs.reduce((n, q) => n + q.ansImg.length, 0) === 131, '原图总计 131 张');
ok(imgs.every(q => q.ansImg.every(p => fs.existsSync(path.join(ROOT, 'pwa', p)))), '全部原图文件均存在');

const js = fs.readFileSync(path.join(ROOT, 'pwa/js/exam.js'), 'utf8');
ok(js.includes("fetch('data/mn27_zs4_papers.json')"), '真题页并行加载 27 张宇四套数据');
ok(js.indexOf('mn27_yt4_papers.json') < js.indexOf('mn27_zs4_papers.json')
   && js.indexOf('mn27_zs4_papers.json') < js.indexOf('mn27_papers.json'),
   '加载顺序：26 → 27押题王 → 27张宇四套 → 27精选');
const sw = fs.readFileSync(path.join(ROOT, 'pwa/sw.js'), 'utf8');
ok(sw.includes("'data/mn27_zs4_papers.json'"), 'SW 预缓存新数据文件');
imgs.forEach(q => q.ansImg.forEach(p => ok(sw.includes("'" + p + "'"), 'SW 预缓存 ' + p)));

console.log(`\n结果：通过 ${pass}，失败 ${fail}`);
process.exit(fail ? 1 : 0);
