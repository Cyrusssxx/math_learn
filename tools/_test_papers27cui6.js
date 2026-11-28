/* 27 崔命六套卷接入回归：结构、思路、原图、加载顺序（模拟卷最前）、SW 预缓存、大纲措辞。 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
let pass = 0, fail = 0;
function ok(cond, name) { if (cond) { pass++; console.log('  ✓ ' + name); } else { fail++; console.log('  ✗ ' + name); } }

const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/mn27_cui6_papers.json'), 'utf8'));
ok(d.length === 5, '5 套卷');
ok(d.every((p, i) => p.id === 'mn27-cui6-' + (i + 1)), '卷 id 为 mn27-cui6-1..5');
ok(d.every((p, i) => p.title === `27 崔命六套卷·第${['一','二','三','四','五'][i]}套`), '卷标题正确');
ok(d.every(p => p.group === 'mock'), '全部标记为 mock');
const qs = d.flatMap(p => p.sections.flatMap(s => s.questions));
ok(qs.length === 110, '共 110 题');
d.forEach(p => {
    const all = p.sections.flatMap(s => s.questions);
    ok(all.length === 22 && all.every((q, i) => q.no === i + 1), p.id + ' 题号连续 1..22');
});
ok(qs.every(q => q.idea && q.idea.startsWith('「思路」') && q.idea.length > 20), '110 题均有实质思路');
ok(qs.every(q => q.answer.startsWith('【答案】') && q.answer.includes('**【解】**')), '每题含答案+解析');
ok(qs.every(q => q.answer.split('$').length % 2 === 1), '答案 $ 定界符成对');
ok(qs.every(q => !/^\s*-\s+\S/m.test(q.stem)) && qs.every(q => !/^\s*-\s+\S/m.test(q.answer)), '题干/答案无 markdown 列表');
ok(qs.every(q => !/数一|数三|考纲|超纲|曲线积分|方向导数|傅里叶|三重积分|概率/.test(q.idea + q.answer)), '无超纲元话语');
// 选择题答案序列（与 PDF 红色【答案】逐题核对）
const choices = d.map(p => p.sections[0].questions.map(q => q.answer.match(/【答案】选 \(([A-D])\)/)?.[1]).join(''));
const expect = ['CDBACBCBCB', 'CADBACDCCC', 'DBBCDACBCA', 'BDCCADDCAB', 'DCBCADCDAB'];
ok(choices.join(',') === expect.join(','), '选择答案序列与 PDF 一致：' + choices.join(' / '));
// 配图
const figQ = qs.filter(q => q.stem.includes('!['));
ok(figQ.length === 1 && figQ[0].stem.includes('data/img/mn27/mn27_qcui01_03.png'), '卷一 Q3 配图挂载');
ok(fs.existsSync(path.join(ROOT, 'pwa/data/img/mn27/mn27_qcui01_03.png')), '配图文件存在');

// 原图：官方解析 PDF 逐题切图
const imgs = qs.filter(q => q.ansImg && q.ansImg.length);
ok(imgs.length === 110, '110 题全部带答案原图');
let cnt = 0;
d.forEach((p, vi) => p.sections.flatMap(s => s.questions).forEach(q => {
  const mine = q.ansImg.filter(x => x.includes('mn27cui6pdf-'));
  cnt += mine.length;
  ok(mine.length > 0 && mine.every((x, i) => x === `data/img/zx_site/mn27cui6pdf-${vi + 1}-${q.no}_${i}.png`),
     `${p.id} Q${q.no} PDF 图命名与序号连续`);
}));
ok(cnt === 162, 'PDF 切图合计 162 张');
ok(imgs.every(q => q.ansImg.every(p => fs.existsSync(path.join(ROOT, 'pwa', p)))), '全部原图文件均存在');

const js = fs.readFileSync(path.join(ROOT, 'pwa/js/exam.js'), 'utf8');
ok(js.includes("fetch('data/mn27_cui6_papers.json')"), '真题页并行加载崔6数据');
const iCui = js.indexOf('mn27_cui6_papers.json');
ok(iCui < js.indexOf('mn26_papers.json')
   && iCui < js.indexOf('mn27_yt4_papers.json')
   && iCui < js.indexOf('mn27_zs4_papers.json')
   && iCui < js.indexOf("fetch('data/mn27_papers.json')"),
   '加载顺序：崔6 在全部模拟卷最前');
const sw = fs.readFileSync(path.join(ROOT, 'pwa/sw.js'), 'utf8');
ok(sw.includes("'data/mn27_cui6_papers.json'"), 'SW 预缓存新数据文件');
ok(sw.includes("'data/img/mn27/mn27_qcui01_03.png'"), 'SW 预缓存配图');
const swImgs = qs.flatMap(q => q.ansImg);
ok(swImgs.every(p => sw.includes("'" + p + "'")), 'SW 预缓存全部 162 张原图');

console.log(`\n结果：通过 ${pass}，失败 ${fail}`);
process.exit(fail ? 1 : 0);
