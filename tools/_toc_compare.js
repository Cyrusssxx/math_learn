// 臻选题目录 vs 核心题库线代目录 逐项对照 + 355 题覆盖核查
const fs = require('fs');
const nodes = JSON.parse(fs.readFileSync('pwa/data/cat_deep.json', 'utf8')).nodes;
const hasChild = new Set(Object.values(nodes).map(v => String(v.p)));
const norm = s => String(s).replace(/\$/g, '').replace(/\s+/g, '').replace(/（/g, '(').replace(/）/g, ')').replace(/，/g, ',');
const byName = {};
for (const id in nodes) {
    const k = norm(nodes[id].n);
    (byName[k] = byName[k] || []).push({ id, leaf: !hasChild.has(id), p: nodes[id].p });
}
function chapOf(id) {
    let c = String(id);
    while (nodes[c] && nodes[c].p && !['2', '3', '4', '5', '6', '7'].includes(c)) c = String(nodes[c].p);
    return c;
}
// PDF 目录（层级缩进表示）
const TOC = `
行列式
 具体行列式计算
 抽象行列式计算
 (代数)余子式相关问题
  代数余子式求和
  部分代数余子式求和
  所有代数余子式求和
  余子式求和
 多项式f(x)以行列式形式给出
  确定f(x) 中x某次方的系数
  方程根的个数
矩阵
 逆
  抽象逆
  (不)可逆的判定与证明
 伴随等于转置/本身
 秩
  求秩
  秩相关推理
 高次幂
 初等变换与初等矩阵
 矩阵等价
 分块矩阵
  分块矩阵伴随
  分块矩阵秩
 AB= □
  AB=E
  AB=O
  AB=C
 求各行(列)元素之和
向量
 向量有关计算
 线性表示
  根据线性表示情况确定参数并将向量线性表示
  线性表示相关推理
  共同线性表示
 向量组等价
 线性相关/无关
  线性相关
  线性无关
  综合
方程组
 解的判定
  判断解的情况
  已知解的情况确定参数
 方程组求解
  齐次
  非齐次
   具体矩阵
   抽象矩阵
    解的结构
    已知向量关系求通解
    已知一方程组通解，求另一方程组通解
    根据其他已知条件求解
 解的关系
  公共解
  同解
  两个方程组其他解的关系
 矩阵方程
  二阶
  可逆
  不可逆
特征值与特征向量
 特征值特征向量
  求特征值特征向量
   具体矩阵
   抽象矩阵
  特征相关推理
 相似
  根据相似推理
  判断/证明相似
  求可逆矩阵P，使得P逆AP=B
 相似对角化
  相似对角化概念
  可相似对角化相关讨论及证明
  相似对角化充要条件
  判断是否可以相似对角化
  求相似对角化的可逆阵P及对角阵Λ
 实对称矩阵
  实对称矩阵概念
  求正交矩阵Q
  求实对称矩阵A
二次型
 标准型
  可逆变换x=Py
  正交变换x=Qy
 规范形
 一个二次型变成另一个二次型，求变换矩阵
  可逆变换求变换矩阵
  正交变换求变换矩阵
  可逆+正交变换求变换矩阵
 求二次型的解
 求二次型最值
 正负惯性指数
  求正负惯性指数
  已知正负惯性指数信息确定参数或其他
 合同
 正定
  已知正定 反求参数
  正定相关证明
  正定矩阵的分解
   平方根分解
   合同分解
`.trim().split('\n');

const CHAPMAP = { '行列式': '2', '矩阵': '3', '向量': '4', '方程组': '5', '特征值与特征向量': '6', '二次型': '7' };
let curChap = null, stack = [];
const missing = [], diff = [];
for (const line of TOC) {
    const ind = (line.match(/^ */) || [''])[0].length;
    const name = line.trim();
    if (ind === 0) { curChap = CHAPMAP[name]; stack = [name]; continue; }
    // 只保留本学科子树内的同名节点
    const k = norm(name);
    const cands = (byName[k] || []).filter(c => chapOf(c.id) === curChap);
    if (!cands.length) missing.push(stack.join(' > ') + ' > ' + name);
    else if (cands.every(c => !c.leaf)) diff.push('非叶子: ' + stack.join(' > ') + ' > ' + name);
}
console.log('=== PDF 目录缺失节点 ===');
if (!missing.length) console.log('  （无）'); else missing.forEach(x => console.log('  ✗ ' + x));
console.log('=== 名称/层级差异 ===');
if (!diff.length) console.log('  （无）'); else diff.forEach(x => console.log('  · ' + x));

// 覆盖核查：355 题是否都有落点
const zx = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const core = JSON.parse(fs.readFileSync('pwa/data/core_bank.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const coreQ = [];
for (const s of core[0].sections) if (LA.includes(s.title)) for (const q of s.questions) coreQ.push(q);
const rep = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const addedZx = new Set(rep.inserted.map(r => r.zx));
[103, 112, 153, 263, 344].forEach(n => addedZx.add(n));
console.log('\n=== 题目覆盖 ===');
console.log('  臻选题 355 题；补录进核心题库 ' + addedZx.size + ' 题；其余按题源/内容判定已在库中');
const notAdded = zx.filter(q => !addedZx.has(q.no));
console.log('  未补录 ' + notAdded.length + ' 题（应全部能在核心题库线代找到同题）');
