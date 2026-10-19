// 匹配 v3：以中文 2-gram 为主指标（OCR 对矩阵失真，但中文描述可靠），数字串降权。
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
function g2(t) { const s = norm(t); const o = new Set(); for (let i = 0; i + 2 <= s.length; i++) { const g = s.slice(i, i + 2); if (/^[\u4e00-\u9fff]{2}$/.test(g)) o.add(g); } return o; }
function nums(t) { const s = norm(t); return (s.match(/\d{1,4}/g) || []); }
function zxText(no) { const c = clean[String(no)]; let t = c.text || ''; for (const p of (c.meta || '').split(' / ')) t = t.replace(p, ' '); return t; }
function diceSet(a, b) { if (!a.size || !b.size) return 0; let i = 0; const [sm, lg] = a.size < b.size ? [a, b] : [b, a]; for (const x of sm) if (lg.has(x)) i++; return (2 * i) / (a.size + b.size); }

const Z = [];
for (const no of Object.keys(clean).map(Number)) {
    const sec = zxSecOf(no); if (!sec) continue;
    const src = (clean[String(no)].meta || '').split(' / ').slice(1).join(';');
    Z.push({ no, sec, src, cg: g2(zxText(no)), nums: nums(zxText(no)) });
}
const C = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) C.push({ no: q.no, sec: s.title, source: q.source || '', cg: g2(q.stem), nums: nums(q.stem), stem: q.stem || '' }); }

const pairs = [];
for (const c of C) {
    let bs = -1, bn = null;
    for (const z of Z) {
        if (z.sec !== c.sec) continue;
        const d = diceSet(c.cg, z.cg);
        if (d > bs) { bs = d; bn = z; }
    }
    if (bn) pairs.push({ coreNo: c.no, sec: c.sec, zxNo: bn.no, dice: +bs.toFixed(3), src: c.source, stem: c.stem, zxSrc: bn.src, zxInAdded: added.has(bn.no), ncg: c.cg.size });
}
pairs.sort((a, b) => b.dice - a.dice);
const usedZ = new Set(), usedC = new Set(), map = {};
for (const p of pairs) { if (usedZ.has(p.zxNo) || usedC.has(p.coreNo)) continue; map[p.coreNo] = p; usedZ.add(p.zxNo); usedC.add(p.coreNo); }
const list = Object.values(map);
const q = (a, p) => a.length ? a[Math.floor(a.length * p)].toFixed(3) : '-';
const dl = list.map(x => x.dice).sort((a, b) => b - a);
console.log('配对', list.length, '| Dice 分布 max=' + dl[0], 'p90=' + q(dl, .1), 'p50=' + q(dl, .5), 'p10=' + q(dl, .9));
const inAdded = list.filter(x => x.zxInAdded);
const inNon = list.filter(x => !x.zxInAdded);
const qa = inAdded.map(x => x.dice).sort((a, b) => b - a);
const qn = inNon.map(x => x.dice).sort((a, b) => b - a);
console.log('对应已补录188的:', inAdded.length, 'Dice: max=' + (qa[0] || 0), 'p50=' + q(qa, .5));
console.log('对应未补录167的:', inNon.length, 'Dice: max=' + (qn[0] || 0), 'p50=' + q(qn, .5));
for (const th of [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]) {
    console.log('  阈值 ' + th.toFixed(1) + ': 188里 ' + qa.filter(s => s >= th).length + ' | 167里 ' + qn.filter(s => s >= th).length);
}
const secCnt = {}; for (const p of list) if (!p.zxInAdded) secCnt[p.sec] = (secCnt[p.sec] || 0) + 1;
console.log('需找回按章:', JSON.stringify(secCnt));
const cov = new Set(list.map(p => p.zxNo));
const miss = Object.keys(clean).map(Number).filter(n => !added.has(n) && !cov.has(n));
console.log('未补录167仍未覆盖:', miss.length, '|', miss.join(','));
fs.writeFileSync('tools/_zx_final_pairs.json', JSON.stringify(list, null, 1), 'utf8');
