// 给 31 道新图题逐题订正 categoryIds / catId / deepCats（原来用了同章首题的兜底值）
const fs = require('fs');
const cats = JSON.parse(fs.readFileSync('pwa/data/exam_categories.json', 'utf8'));
const cd = JSON.parse(fs.readFileSync('pwa/data/cat_deep.json', 'utf8'));
const zxParsed = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const catOf = {}; for (const q of zxParsed) catOf[q.no] = q.cat || '';
const cb = JSON.parse(fs.readFileSync('pwa/data/core_bank.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const CH = { '行列式': '行列式', '矩阵': '矩阵', '向量': '向量', '方程组': '线性方程组', '线性方程组': '线性方程组', '特征值与特征向量': '特征值与特征向量', '二次型': '二次型' };
const norm = s => String(s || '').replace(/\s+/g, '');

// L2 叶子（真题分类）与 cat_deep 叶子
const l2 = [], deepLeaf = [];
for (const k in cats) { const c = cats[k]; if (c.level !== 2) continue; const ch = cats[String(c.parentId)]; if (!ch) continue; const sub = cats[String(ch.parentId)]; if (sub && sub.name === '线性代数') l2.push({ id: c.id, name: c.name, chName: ch.name }); }
for (const k in cd.nodes) { const n = cd.nodes[k]; const hasKid = Object.values(cd.nodes).some(v => String(v.p) === k); if (!hasKid) deepLeaf.push({ id: k, name: n.n }); }
const l2ByName = {}; for (const x of l2) l2ByName[norm(x.name)] = x;
const deepByName = {}; for (const x of deepLeaf) deepByName[norm(x.name)] = x.id;

// 书目录叶名 → 真题 L2 叶子名（人工核对过的映射）
const MAP = {
    '具体行列式计算': '具体行列式计算', '抽象行列式计算': '抽象行列式计算',
    '部分代数余子式求和': '(代数)余子式相关问题', '所有代数余子式求和': '(代数)余子式相关问题',
    '余子式求和': '(代数)余子式相关问题', '确定f(x) 中x某次方的系数': '多项式 $f(x)$ 以行列式形式给出',
    '方程根的个数': '多项式 $f(x)$ 以行列式形式给出',
    '高次幂': '高次幂', '初等变换与初等矩阵': '初等变换与初等矩阵', '求秩': '秩', '秩相关推理': '秩',
    '(不)可逆的判定与证明': '逆', '抽象逆': '逆', '伴随等于转置/本身': '伴随矩阵',
    '分块矩阵伴随': '分块矩阵', '分块矩阵秩': '分块矩阵', 'AB=E': 'AB=口', 'AB=O': 'AB=口', 'AB=C': 'AB=口',
    '求各行(列)元素之和': '其他题型', '矩阵等价': '其他题型', '平方根分解': '矩阵分解', '合同分解': '矩阵分解',
    '向量有关计算': '向量有关计算', '向量组等价': '向量组等价', '线性相关': '线性相关与无关',
    '线性无关': '线性相关与无关', '综合': '线性相关与无关',
    '根据线性表示情况确定参数并将向量线性表示': '线性表示', '线性表示相关推理': '线性表示', '共同线性表示': '线性表示',
    '判断解的情况': '解的判定', '已知解的情况确定参数': '解的判定', '齐次': '方程组求解', '具体矩阵': '方程组求解',
    '解的结构': '方程组求解', '已知向量关系求通解': '方程组求解', '已知一方程组通解，求另一方程组通解': '方程组求解',
    '根据其他已知条件求解': '方程组求解', '可逆': '方程组求解', '不可逆': '方程组求解',
    '公共解': '解的关系', '同解': '解的关系', '两个方程组其他解的关系': '解的关系',
    '抽象矩阵': '特征值与特征向量', '求特征值特征向量': '特征值与特征向量', '特征相关推理': '特征值与特征向量',
    '判断/证明相似': '相似', '根据相似推理': '相似', '求可逆矩阵P，使得P逆AP=B': '相似',
    '相似对角化概念': '相似对角化', '可相似对角化相关讨论及证明': '相似对角化', '相似对角化充要条件': '相似对角化',
    '判断是否可以相似对角化': '相似对角化', '求相似对角化的可逆阵P及对角阵Λ': '相似对角化',
    '实对称矩阵概念': '实对称矩阵', '求正交矩阵Q': '实对称矩阵', '求实对称矩阵A': '实对称矩阵',
    '可逆变换x=Py': '标准型', '正交变换x=Qy': '标准型', '可逆变换求变换矩阵': '一个二次型变成另一个二次型，求变换矩阵',
    '求二次型的解': '求二次型的解', '求二次型最值': '求二次型最值', '规范形': '规范形',
    '求正负惯性指数': '正负惯性指数', '已知正负惯性指数信息确定参数或其他': '正负惯性指数',
    '合同': '合同', '已知正定 反求参数': '正定', '正定相关证明': '正定',
};
// 章级限定
const OVER = {
    '特征值与特征向量::具体矩阵': '特征值与特征向量', '线性方程组::具体矩阵': '方程组求解',
    '二次型::平方根分解': '正定', '二次型::合同分解': '合同',
};
const CH_DEF = { '行列式': 9, '矩阵': 33, '向量': 118, '线性方程组': 135, '特征值与特征向量': 177, '二次型': 202 };

let fixed = 0;
for (const s of cb[0].sections) {
    if (!LA.includes(s.title)) continue;
    for (const q of s.questions) {
        if (q.no < 1300) continue;
        const zno = q.srcOrder;
        const book = catOf[zno] || '';
        const leaf = book.split('→').pop().trim();
        let l2n = OVER[s.title + '::' + leaf] || OVER[s.title + '::' + norm(leaf)] || null;
        if (!l2n) { const hit = Object.keys(MAP).find(k => norm(k) === norm(leaf)); if (hit) l2n = MAP[hit]; }
        if (!l2n && l2ByName[norm(leaf)]) l2n = l2ByName[norm(leaf)].name;
        let leafId = null;
        if (l2n) { const e = l2ByName[norm(l2n)]; if (e && e.chName === s.title) leafId = e.id; }
        if (!leafId) leafId = CH_DEF[s.title];
        q.categoryIds = [leafId]; q.catId = leafId;
        // deepCats：按书目录叶名找 cat_deep 叶子
        const dn = deepByName[norm(leaf)];
        q.deepCats = dn ? [dn] : [];
        fixed++;
    }
}
fs.writeFileSync('pwa/data/core_bank.json', JSON.stringify(cb), 'utf8');
console.log('已订正', fixed, '道新图题的分类');
