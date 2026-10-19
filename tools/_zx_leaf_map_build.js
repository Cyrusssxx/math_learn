// 给 188 道线代臻选题补 categoryIds（真题分类体系 L2 叶子 id）
// 臻选题原来的 categoryIds 只填了章级 id（2-7）或 cat_deep id，分类树只统计 L2，导致线代学科整棵消失。
// 规则：书目录叶名（更细）→ 真题分类 L2 叶子（更粗）。逐条人工核对，按章分组。
const fs = require('fs');
const cats = JSON.parse(fs.readFileSync('pwa/data/exam_categories.json', 'utf8'));
const cb = JSON.parse(fs.readFileSync('pwa/data/core_bank.json', 'utf8'))[0];
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const zxParsed = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const cd = JSON.parse(fs.readFileSync('pwa/data/cat_deep.json', 'utf8'));

const zx2no = {};
for (const r of [r1, r2]) for (const x of r.inserted) zx2no[x.zx] = x.no;
const no2zx = {}; for (const z in zx2no) no2zx[zx2no[z]] = Number(z);
const zxCatByNo = {}; for (const q of zxParsed) zxCatByNo[q.no] = q.cat || '';

// ---- 章级 id（真题分类 L1）→ 该章的默认 L2 叶子（找不到细分时兜底）----
const CH = { 2: '行列式', 3: '矩阵', 4: '向量', 5: '线性方程组', 6: '特征值与特征向量', 7: '二次型' };
const l2ByName = {};
for (const k in cats) {
  const c = cats[k];
  if (c.level !== 2) continue;
  const ch = cats[String(c.parentId)]; if (!ch) continue;
  const sub = cats[String(ch.parentId)]; if (!sub || sub.name !== '线性代数') continue;
  l2ByName[ch.name] = l2ByName[ch.name] || [];
  l2ByName[ch.name].push({ id: c.id, name: c.name });
}
const CH_DEFAULT = {
  行列式: l2ByName['行列式'].find(x => x.name === '具体行列式计算').id,
  矩阵: l2ByName['矩阵'].find(x => x.name === '其他题型').id,
  向量: l2ByName['向量'].find(x => x.name === '向量有关计算').id,
  线性方程组: l2ByName['线性方程组'].find(x => x.name === '方程组求解').id,
  特征值与特征向量: l2ByName['特征值与特征向量'].find(x => x.name === '特征值与特征向量').id,
  二次型: l2ByName['二次型'].find(x => x.name === '标准型').id,
};

// ---- 书目录叶名 → 真题分类 L2 叶子名（人工核对）----
const LEAF_MAP = {
  '具体行列式计算': '具体行列式计算',
  '抽象行列式计算': '抽象行列式计算',
  '部分代数余子式求和': '(代数)余子式相关问题',
  '所有代数余子式求和': '(代数)余子式相关问题',
  '余子式求和': '(代数)余子式相关问题',
  '确定f(x) 中x某次方的系数': '多项式 $f(x)$ 以行列式形式给出',
  '方程根的个数': '多项式 $f(x)$ 以行列式形式给出',
  '高次幂': '高次幂',
  '初等变换与初等矩阵': '初等变换与初等矩阵',
  '求秩': '秩',
  '秩相关推理': '秩',
  '(不)可逆的判定与证明': '逆',
  '抽象逆': '逆',
  '伴随等于转置/本身': '伴随矩阵',
  '分块矩阵伴随': '分块矩阵',
  '分块矩阵秩': '分块矩阵',
  'AB=E': 'AB=口',
  'AB=O': 'AB=口',
  'AB=C': 'AB=口',
  '求各行(列)元素之和': '其他题型',
  '矩阵等价': '其他题型',
  '平方根分解': '矩阵分解',
  '合同分解': '矩阵分解',
  '向量有关计算': '向量有关计算',
  '向量组等价': '向量组等价',
  '线性相关': '线性相关与无关',
  '线性无关': '线性相关与无关',
  '综合': '线性相关与无关',
  '根据线性表示情况确定参数并将向量线性表示': '线性表示',
  '线性表示相关推理': '线性表示',
  '共同线性表示': '线性表示',
  '判断解的情况': '解的判定',
  '已知解的情况确定参数': '解的判定',
  '齐次': '方程组求解',
  '具体矩阵': '方程组求解',
  '解的结构': '方程组求解',
  '已知向量关系求通解': '方程组求解',
  '已知一方程组通解，求另一方程组通解': '方程组求解',
  '根据其他已知条件求解': '方程组求解',
  '可逆': '方程组求解',
  '不可逆': '方程组求解',
  '公共解': '解的关系',
  '同解': '解的关系',
  '两个方程组其他解的关系': '解的关系',
  '抽象矩阵': '特征值与特征向量',
  '求特征值特征向量': '特征值与特征向量',
  '特征相关推理': '特征值与特征向量',
  '判断/证明相似': '相似',
  '根据相似推理': '相似',
  '求可逆矩阵P，使得P逆AP=B': '相似',
  '相似对角化概念': '相似对角化',
  '可相似对角化相关讨论及证明': '相似对角化',
  '相似对角化充要条件': '相似对角化',
  '判断是否可以相似对角化': '相似对角化',
  '求相似对角化的可逆阵P及对角阵Λ': '相似对角化',
  '实对称矩阵概念': '实对称矩阵',
  '求正交矩阵Q': '实对称矩阵',
  '求实对称矩阵A': '实对称矩阵',
  '可逆变换x=Py': '标准型',
  '正交变换x=Qy': '标准型',
  '可逆变换求变换矩阵': '一个二次型变成另一个二次型，求变换矩阵',
  '求二次型的解': '求二次型的解',
  '求二次型最值': '求二次型最值',
  '规范形': '规范形',
  '求正负惯性指数': '正负惯性指数',
  '已知正负惯性指数信息确定参数或其他': '正负惯性指数',
  '合同': '合同',
  '已知正定 反求参数': '正定',
  '正定相关证明': '正定',
};

// ---- 章级限定：同名叶在不同章含义不同，优先按「章::叶名」查 ----
const LEAF_OVERRIDE = {
  '特征值与特征向量::具体矩阵': '特征值与特征向量',
  '线性方程组::具体矩阵': '方程组求解',
  '二次型::平方根分解': '正定',
  '二次型::合同分解': '合同',
  '矩阵::平方根分解': '矩阵分解',
  '矩阵::合同分解': '矩阵分解',
};

const l2name2id = {};
for (const k in cats) { const c = cats[k]; if (c.level === 2 && l2ByName[CH2name(c)]) l2name2id[norm(c.name)] = c.id; }
function CH2name(c) { const ch = cats[String(c.parentId)]; return ch ? ch.name : ''; }

function norm(s) { return String(s || '').replace(/\s+/g, ''); }

const out = {}; const miss = [];
for (const s of cb.sections) {
  for (const q of s.questions) {
    const secCh = s.title;
    if (!CH[q.categoryIds[0]] && secCh !== '行列式' && secCh !== '矩阵' && secCh !== '向量'
        && secCh !== '线性方程组' && secCh !== '特征值与特征向量' && secCh !== '二次型') continue;
    const zxNo = no2zx[q.no];
    const bookCat = zxNo ? (zxCatByNo[zxNo] || '') : '';
    const bookLeaf = bookCat.split('→').pop().trim();
    // 细分类兜底
    const deepNames = (q.deepCats || []).map(d => (cd.nodes[String(d)] || {}).n || '').filter(Boolean);
    let target = null, via = '';
    // 1) 精确命中 L2 名
    for (const cand of [bookLeaf, ...deepNames]) {
      const n = norm(cand);
      if (l2name2id[norm(cand)]) { target = l2name2id[norm(cand)]; via = 'exact:' + cand; break; }
    }
    // 2) 语义映射（先查章级限定，再查通用映射）
    if (!target) {
      for (const cand of [bookLeaf, ...deepNames]) {
        const n = norm(cand);
        const scoped = LEAF_OVERRIDE[secCh + '::' + cand] || LEAF_OVERRIDE[secCh + '::' + n];
        let l2n = null;
        if (scoped) l2n = scoped;
        else { const hit = Object.keys(LEAF_MAP).find(k => norm(k) === n); if (hit) l2n = LEAF_MAP[hit]; }
        if (l2n && l2name2id[norm(l2n)]) { target = l2name2id[norm(l2n)]; via = 'map:' + cand; break; }
      }
    }
    // 3) 章默认
    if (!target) { target = CH_DEFAULT[CH[q.categoryIds[0]] || secCh]; via = 'chapter-default'; }
    out[q.no] = { leaf: target, via, bookLeaf, deepNames, ch: CH[q.categoryIds[0]] || secCh };
  }
}
fs.writeFileSync('tools/_zx_leaf_map.json', JSON.stringify(out, null, 1), 'utf8');
const byVia = {};
for (const n in out) byVia[out[n].via.split(':')[0]] = (byVia[out[n].via.split(':')[0]] || 0) + 1;
console.log('总数:', Object.keys(out).length, '| 命中方式:', JSON.stringify(byVia));
const def = Object.values(out).filter(x => x.via === 'chapter-default');
console.log('落到章默认的:', def.length);
def.slice(0, 20).forEach(x => console.log('  ', x.ch, '|', x.bookLeaf, '|', x.deepNames.join('/')));
