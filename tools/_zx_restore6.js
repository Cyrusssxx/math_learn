// 对称核对：355 甄选题各自在原核心库 346 题里的最佳 Dice，
// 看「已补录 188」里有多少其实是重复题（当年误判为缺失）。
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
function zxText(no) { const c = clean[String(no)]; if (!c) return ''; let t = c.text || ''; for (const p of (c.meta || '').split(' / ')) t = t.replace(p, ' '); return t; }
const CG = {};
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; (CG[s.title] = CG[s.title] || []).push({ no: q => 0, g: g4(s.questions[0].stem) }); }
// 重建（上一行写法不对，重写）
const coreBySec = {};
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) (coreBySec[s.title] = coreBySec[s.title] || []).push({ no: q.no, g: g4(q.stem), stem: q.stem || '' }); }
function dice(a, b) { if (!a.size || !b.size) return 0; let i = 0; const [sm, lg] = a.size < b.size ? [a, b] : [b, a]; for (const x of sm) if (lg.has(x)) i++; return (2 * i) / (a.size + b.size); }

const res = [];
for (const no of Object.keys(clean).map(Number)) {
    const sec = zxSecOf(no); if (!sec) continue;
    const g = g4(zxText(no));
    let bs = 0, bn = null;
    for (const c of (coreBySec[sec] || [])) { const d = dice(g, c.g); if (d > bs) { bs = d; bn = c.no; } }
    res.push({ zx: no, sec, coreNo: bn, score: +bs.toFixed(4), inAdded: added.has(no) });
}
res.sort((a, b) => b.score - a.score);
const add = res.filter(r => r.inAdded), non = res.filter(r => !r.inAdded);
const q = (a, p) => a[Math.floor(a.length * p)].score.toFixed(3);
console.log('已补录 188 的最高 Dice: max=' + add[0].score, 'p90=' + q(add, .1), 'p50=' + q(add, .5));
console.log('未补录 167 的最高 Dice: max=' + non[0].score, 'p90=' + q(non, .1), 'p50=' + q(non, .5));
console.log();
for (const th of [0.15, 0.2, 0.25, 0.3, 0.35, 0.4]) {
    console.log('  阈值 ' + th.toFixed(2) + ': 188里过线(重复) ' + add.filter(r => r.score >= th).length + ' | 167里过线(该在库) ' + non.filter(r => r.score >= th).length);
}
const dup = add.filter(r => r.score >= 0.35);
console.log('\n≥0.35 判定为「当年误加」的补录题:', dup.length);
dup.slice(0, 20).forEach(d => console.log('  臻选#' + d.zx, '→ core#' + d.coreNo, 'dice=' + d.score, '|', clean[String(d.zx)].meta.slice(0, 40)));
fs.writeFileSync('tools/_zx_symmetric.json', JSON.stringify(res, null, 1), 'utf8');
