// 阶段3：把臻选题补录题写入 core_bank.json
// 用法: node tools/_zx_insert.js [--dry]
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const DRY = process.argv.includes('--dry');

const add = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/_zx_add_list.json'), 'utf8'));
const zx = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/_zx_parsed.json'), 'utf8'));
const byNo = {}; for (const q of zx) byNo[q.no] = q;
const cd = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/cat_deep.json'), 'utf8'));
const nodes = cd.nodes;
const hasChild = new Set(Object.values(nodes).map(v => String(v.p)));
const isLeaf = id => !hasChild.has(String(id));

// ===== 考点 → deepCats 叶子 =====
const M = {
  '抽象行列式计算': '10',
  '两个方程组其他解的关系': '168',
  '秩相关推理': '42',
  '正定相关证明': '220',
  '伴随等于转置/本身': '38',
  '求秩': '39',
  '高次幂': '28',
  '分块矩阵秩': '44',
  '判断解的情况': '133',
  '同解': '164',
  '特征相关推理': '183',
  '判断是否可以相似对角化': '194',
  '合同': '209',
  '部分代数余子式求和': '21',
  '所有代数余子式求和': '21',
  '余子式求和': '21',
  '初等变换与初等矩阵': '29',
  'AB=C': '47',
  '求各行(列)元素之和': '52',
  '向量组等价': '121',
  '不可逆': '174',
  '相似对角化充要条件': '192',
  '可逆变换x=Py': '211',
  '正交变换x=Qy': '212',
  '规范形': '204',
  '求二次型最值': '206',
  '合同分解': '51',
  '方程根的个数': '222',
  '(不)可逆的判定与证明': '36',
  'AB=E': '45',
  '线性相关': '128',
  '线性无关': '129',
  '已知解的情况确定参数': '134',
  '解的结构': '148',
  '已知向量关系求通解': '149',
  '根据其他已知条件求解': '153',
  '公共解': '162',
  '可逆': '171',
  '根据相似推理': '186',
  '求可逆矩阵P，使得P逆AP=B': '188',
  '相似对角化概念': '190',
  '可相似对角化相关讨论及证明': '191',
  '求相似对角化的可逆阵P及对角阵Λ': '193',
  '实对称矩阵概念': '195',
  '求实对称矩阵A': '197',
  '可逆变换求变换矩阵': '214',
  '求正负惯性指数': '217',
  '已知正定 反求参数': '219',
  '平方根分解': '51',
};
// 上下文相关的「具体矩阵」：向前找最近一个带完整路径的题，用其章节上下文
function resolveLeaf(q) {
  const segs = String(q.cat || '').split('→').map(x => x.trim());
  const last = segs[segs.length - 1];
  if (last === '具体矩阵') {
    // 向前扫描最近的完整路径
    let ctx = '';
    for (let n = q.no - 1; n >= 1 && !ctx; n--) {
      const pq = byNo[n];
      if (pq && String(pq.cat || '').includes('→')) ctx = pq.cat;
    }
    if (ctx.includes('特征值')) return '184';
    if (ctx.includes('方程组求解')) return '145';
    if (ctx.includes('矩阵')) return '184';
    if (ctx.includes('线性方程组')) return '145';
  }
  if (M[last]) return M[last];
  return null;
}
// deepCats 叶 → 章节名
const CHAP = { 2: '行列式', 3: '矩阵', 4: '向量', 5: '线性方程组', 6: '特征值与特征向量', 7: '二次型' };
function chapOf(leaf) {
  let c = String(leaf);
  while (nodes[c] && nodes[c].p && !CHAP[c]) c = String(nodes[c].p);
  return CHAP[c] || null;
}
function catIdOf(leaf) {
  let c = String(leaf);
  while (nodes[c] && nodes[c].p && !CHAP[c]) c = String(nodes[c].p);
  return Number(c);
}
// 题型推断
function inferType(body) {
  const t = String(body || '');
  if (/(^|\n)\s*[（(]?[ABCD][）).、]/m.test(t) && /(C|D)[）).、]/.test(t)) return 'choice';
  if (/证明/.test(t)) return 'proof';
  if (/=+\s*_|_+$|＝\s*_|填空/.test(t)) return 'blank';
  return 'calc';
}

// ===== 执行 =====
const bank = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/core_bank.json'), 'utf8'));
const sections = bank[0].sections;
let mx = 0; for (const s of sections) for (const q of s.questions) mx = Math.max(mx, q.no);
let no = mx;
const inserted = [], skipped = [];
for (const item of add) {
  const q = byNo[item.no];
  const segs = String(q.cat || '').split('→').map(x => x.trim());
  const zj = segs[segs.length - 1];
  const leaf = resolveLeaf(q);
  if (!leaf || !isLeaf(leaf)) { skipped.push({ no: item.no, why: '考点无叶子映射: ' + zj }); continue; }
  if (!item.qimg) { skipped.push({ no: item.no, why: '无题面截图' }); continue; }
  if (!item.aimgs || !item.aimgs.length) { skipped.push({ no: item.no, why: '无答案图' }); continue; }
  const chap = chapOf(leaf);
  const sec = sections.find(s => s.title === chap);
  if (!sec) { skipped.push({ no: item.no, why: '章节不存在: ' + chap }); continue; }
  const type = inferType(item._body || q.body || '');
  no++;
  const rel = p => p.replace(/^.*pwa\//, '');
  const answerMd = '【答案与解析】完整过程见下方配图（源自《线代臻选题·通用答案》）。\n\n'
    + item.aimgs.map(p => `![](${rel(p)})`).join('\n\n');
  const nq = {
    no,
    kind: type,
    type,
    stem: '（臻选题补录题，完整题面见下方配图）',
    options: [],
    answer: answerMd,
    idea: `考点：${zj}。本题取自《线代臻选题》第 ${item.page} 页（#${String(item.no).padStart(3, '0')}），题面与详解均为原书截图；建议先独立完成再对照解析。`,
    categoryIds: [catIdOf(leaf)],
    catId: catIdOf(leaf),
    deepCats: [leaf],
    linkedQid: null,
    source: q.src,
    srcPage: item.page,
    srcOrder: item.no,
    status: 'transcribed',
    key: false,
    img: rel(item.qimg),
  };
  sec.questions.push(nq);
  inserted.push({ zx: item.no, no, sec: chap, leaf, type });
}
console.log(`插入 ${inserted.length} 题，跳过 ${skipped.length} 题`);
skipped.forEach(s => console.log('  跳过 zx#' + s.no + ': ' + s.why));
if (!DRY) {
  fs.writeFileSync(path.join(ROOT, 'pwa/data/core_bank.json'), JSON.stringify(bank), 'utf8');
  console.log('✅ 已写回 core_bank.json');
}
fs.writeFileSync(path.join(ROOT, 'tools/_zx_insert_report.json'), JSON.stringify({ inserted, skipped }, null, 1), 'utf8');
// 分布
const bySec = {}; inserted.forEach(i => bySec[i.sec] = (bySec[i.sec] || 0) + 1);
console.log('分章:', JSON.stringify(bySec));
const byType = {}; inserted.forEach(i => byType[i.type] = (byType[i.type] || 0) + 1);
console.log('分题型:', JSON.stringify(byType));
