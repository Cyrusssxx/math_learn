// 第二轮补录入库：87 题 → core_bank（编号续 1178 起）
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const DRY = process.argv.includes('--dry');

const add = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/_zx_add2_list.json'), 'utf8'));
const zx = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/_zx_parsed.json'), 'utf8'));
const byNo = {}; for (const q of zx) byNo[q.no] = q;

// cat_deep：先补「解的结构」叶子
const cdPath = path.join(ROOT, 'pwa/data/cat_deep.json');
const cd = JSON.parse(fs.readFileSync(cdPath, 'utf8'));
cd.nodes['2505'] = { n: '解的结构', p: '146' };   // 方程组>方程组求解>非齐次>抽象矩阵>解的结构
const nodes = cd.nodes;
const hasChild = new Set(Object.values(nodes).map(v => String(v.p)));
const isLeaf = id => !hasChild.has(String(id));

const M = {
  '抽象行列式计算': '10', '具体行列式计算': '19',
  '部分代数余子式求和': '2500', '所有代数余子式求和': '2501', '余子式求和': '2502',
  '确定f(x) 中x某次方的系数': '23', '方程根的个数': '222',
  '抽象逆': '35', '(不)可逆的判定与证明': '36', '伴随等于转置/本身': '38',
  '求秩': '39', '秩相关推理': '42', '高次幂': '28',
  '初等变换与初等矩阵': '29', '分块矩阵伴随': '43', '分块矩阵秩': '44',
  'AB=E': '45', 'AB=O': '46', 'AB=C': '47', '求各行(列)元素之和': '52',
  '根据线性表示情况确定参数并将向量线性表示': '124', '线性表示相关推理': '125', '共同线性表示': '126',
  '向量组等价': '121', '线性相关': '128', '线性无关': '129', '综合': '131',
  '判断解的情况': '133', '已知解的情况确定参数': '134', '齐次': '137',
  '解的结构': '2505', '已知向量关系求通解': '149', '根据其他已知条件求解': '153',
  '公共解': '162', '同解': '164', '两个方程组其他解的关系': '168',
  '可逆': '171', '不可逆': '174',
  '特征相关推理': '183', '具体矩阵': 'CTX', '抽象矩阵': 'CTX',
  '根据相似推理': '186', '判断/证明相似': '187', '求可逆矩阵P，使得P逆AP=B': '188',
  '相似对角化概念': '190', '可相似对角化相关讨论及证明': '191', '相似对角化充要条件': '192',
  '判断是否可以相似对角化': '194', '求相似对角化的可逆阵P及对角阵Λ': '193',
  '实对称矩阵概念': '195', '求正交矩阵Q': '198', '求实对称矩阵A': '197',
  '可逆变换x=Py': '211', '正交变换x=Qy': '212', '可逆变换求变换矩阵': '214',
  '规范形': '204', '求二次型最值': '206', '求正负惯性指数': '217',
  '已知正负惯性指数信息确定参数或其他': '218', '合同': '209',
  '已知正定 反求参数': '219', '正定相关证明': '220', '平方根分解': '2503', '合同分解': '2504',
};
const CH = { 2: '行列式', 3: '矩阵', 4: '向量', 5: '线性方程组', 6: '特征值与特征向量', 7: '二次型' };
function chapOf(leaf) {
  let c = String(leaf), g = 0;
  while (nodes[c] && nodes[c].p && g++ < 30) { if (CH[c]) return CH[c]; c = String(nodes[c].p); }
  return CH[c] || null;
}
function catIdOf(leaf) {
  let c = String(leaf), g = 0;
  while (nodes[c] && nodes[c].p && g++ < 30) { if (CH[c]) return Number(c); c = String(nodes[c].p); }
  return Number(c);
}
// 上下文判定（臻选题 编号区间：方程组 #147-220，特征值 #221-284）
function resolveLeaf(item) {
  const segs = String(item.cat || '').split('→').map(x => x.trim());
  const zj = segs[segs.length - 1];
  const v = M[zj];
  if (v !== 'CTX') return v || null;
  // 具体矩阵/抽象矩阵：按编号区间分 流程组(145/138) 或 特征值(184/185)
  if (item.no >= 221 && item.no <= 284) return zj === '具体矩阵' ? '184' : '185';
  return zj === '具体矩阵' ? '145' : '138';
}

if (!DRY) fs.writeFileSync(cdPath, JSON.stringify(cd), 'utf8');

const bank = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/core_bank.json'), 'utf8'));
const secs = bank[0].sections;
let mx = 0; for (const s of secs) for (const q of s.questions) mx = Math.max(mx, q.no);
let no = mx;
const inserted = [], skipped = [];
for (const item of add) {
  const leaf = resolveLeaf(item);
  if (!leaf || !isLeaf(leaf)) { skipped.push({ no: item.no, why: '考点映射: ' + leaf }); continue; }
  if (!item.qimg) { skipped.push({ no: item.no, why: '无题面图' }); continue; }
  if (!item.aimgs || !item.aimgs.length) { skipped.push({ no: item.no, why: '无答案图' }); continue; }
  const chap = chapOf(leaf);
  const sec = secs.find(s => s.title === chap);
  if (!sec) { skipped.push({ no: item.no, why: '章节不存在 ' + chap }); continue; }
  const zj = String(item.cat).split('→').pop().trim();
  no++;
  const rel = p => p.replace(/^.*pwa\//, '');
  sec.questions.push({
    no,
    kind: 'calc', type: 'calc',
    stem: '（臻选题补录题，完整题面见下方配图）',
    options: [],
    answer: '【答案与解析】完整过程见下方配图（源自《线代臻选题·通用答案》）。\n\n'
      + item.aimgs.map(p => `![](${rel(p)})`).join('\n\n'),
    idea: `考点：${zj}。本题取自《线代臻选题》第 ${item.page} 页（#${String(item.no).padStart(3, '0')}），题面与详解均为原书截图。`,
    categoryIds: [catIdOf(leaf)],
    catId: catIdOf(leaf),
    deepCats: [leaf],
    linkedQid: null,
    source: item.src,
    srcPage: item.page,
    srcOrder: item.no,
    status: 'transcribed',
    key: false,
    img: rel(item.qimg),
  });
  inserted.push({ zx: item.no, no, sec: chap, leaf });
}
console.log(`插入 ${inserted.length}，跳过 ${skipped.length}`);
skipped.forEach(s => console.log('  跳过 zx#' + s.no + ': ' + s.why));
const bySec = {}; inserted.forEach(i => bySec[i.sec] = (bySec[i.sec] || 0) + 1);
console.log('分章:', JSON.stringify(bySec));
if (!DRY) {
  fs.writeFileSync(path.join(ROOT, 'pwa/data/core_bank.json'), JSON.stringify(bank), 'utf8');
  console.log('✅ 已写回 core_bank.json');
}
fs.writeFileSync(path.join(ROOT, 'tools/_zx_insert2_report.json'), JSON.stringify({ inserted, skipped }, null, 1), 'utf8');
