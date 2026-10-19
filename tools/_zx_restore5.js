// 从核心库一侧匹配：346 道原线代题里，哪些对应甄选题？
// 判据：4-gram 包含度（Dice）。用「已补录的 188 道」当负样本标定阈值——它们确定不在原库里。
const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const clean = JSON.parse(fs.readFileSync('tools/_zx_clean_text.json', 'utf8'));
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const RANGE = [[1, 40, '行列式'], [41, 115, '矩阵'], [116, 146, '向量'], [147, 220, '线性方程组'], [221, 284, '特征值与特征向量'], [285, 355, '二次型']];
const zxSecOf = n => { const r = RANGE.find(x => n >= x[0] && n <= x[1]); return r ? r[2] : null; };
const added = new Set();
for (const r of [r1, r2]) for (const x of r.inserted) added.add(x.zx);
[103, 112, 153, 263, 344].forEach(n => added.add(n));

const norm = t => String(t || '').toLowerCase().replace(/[^0-9a-z\u4e00-\u9fff]+/g, '');
function g4(t) { const s = norm(t); const o = new Set(); for (let i = 0; i + 4 <= s.length; i++) o.add(s.slice(i, i + 4)); return o; }
function zxText(no) {
    const c = clean[String(no)]; if (!c) return '';
    let t = c.text || '';
    for (const part of (c.meta || '').split(' / ')) t = t.replace(part, ' ');
    return t;
}
// 甄选题分组（按章）
const ZG = {};
for (const no of Object.keys(clean).map(Number)) {
    const s = zxSecOf(no); if (!s) continue;
    (ZG[s] = ZG[s] || []).push({ no, g: g4(zxText(no)), raw: zxText(no) });
}
// 核心库线代题
const core = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) core.push({ no: q.no, sec: s.title, g: g4(q.stem), stem: q.stem || '' }); }

function dice(a, b) {
    if (!a.size || !b.size) return 0;
    let inter = 0;
    const [sm, lg] = a.size < b.size ? [a, b] : [b, a];
    for (const x of sm) if (lg.has(x)) inter++;
    return (2 * inter) / (a.size + b.size);
}
// 每道核心题找最佳甄选
const best = [];
for (const c of core) {
    let bs = 0, bn = null;
    for (const z of (ZG[c.sec] || [])) { const d = dice(c.g, z.g); if (d > bs) { bs = d; bn = z.no; } }
    best.push({ coreNo: c.no, sec: c.sec, zxNo: bn, score: +bs.toFixed(4), stem: c.stem });
}
const sc = best.map(b => b.score).sort((a, b) => b - a);
const pct = (a, p) => a[Math.floor(a.length * p)].toFixed(3);
console.log('346 道原线代题 → 最佳甄选 Dice 分布:');
console.log('  max=' + sc[0], 'p90=' + pct(sc, .1), 'p50=' + pct(sc, .5), 'p10=' + pct(sc, .9));
for (const th of [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]) {
    console.log('  阈值 ' + th.toFixed(2) + ': 命中 ' + sc.filter(s => s >= th).length + '/346');
}
// 负样本校验：若某核心题的最佳甄选属于「已补录188」，说明它是重复题
const dupToAdded = best.filter(b => b.zxNo && added.has(b.zxNo) && b.score >= 0.3);
console.log('\n最佳甄选落在「已补录188」内的核心题（=与补录题重复）:', dupToAdded.length);
fs.writeFileSync('tools/_zx_core_side.json', JSON.stringify(best, null, 1), 'utf8');
