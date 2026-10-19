// 完整找回 167 道：候选 = (同章 ∧ 同真题来源) ∪ _zx_vs_core._mc，再用题干 4-gram 重合度贪心配对
const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const zx = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const vs = JSON.parse(fs.readFileSync('tools/_zx_vs_core.json', 'utf8'));
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const RANGE = [[1, 40, '行列式'], [41, 115, '矩阵'], [116, 146, '向量'], [147, 220, '线性方程组'], [221, 284, '特征值与特征向量'], [285, 355, '二次型']];
const secOf = n => { const r = RANGE.find(x => n >= x[0] && n <= x[1]); return r ? r[2] : null; };
const added = new Set();
for (const r of [r1, r2]) for (const x of r.inserted) added.add(x.zx);
[103, 112, 153, 263, 344].forEach(n => added.add(n));

function ztKeys(s) {
    const out = new Set();
    for (const part of String(s || '').split(/[;；]/)) {
        const t = part.trim(); if (!t) continue;
        if (/880|900|姜晓千|经典|李永乐|李艳芳|余丙森|张宇|押题|超越|八套|四套|三套|六套/.test(t)) continue;
        const ym = t.match(/((?:19|20)\d{2})\s*数/) || t.match(/^\s*((?:19|20)\d{2})/);
        if (!ym) continue;
        const ps = [];
        if (/数一|数学一/.test(t)) ps.push(1);
        if (/数二|数学二/.test(t)) ps.push(2);
        if (/数三|数学三/.test(t)) ps.push(3);
        for (const p of ps) out.add(ym[1] + '/' + p);
    }
    return out;
}
const core = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) core.push({ no: q.no, sec: s.title, keys: ztKeys(q.source), stem: q.stem || '', source: q.source }); }
const coreByNo = {}; for (const c of core) coreByNo[c.no] = c;
const mcMap = {}; for (const v of vs) mcMap[v.no] = (v._mc || []).filter(n => coreByNo[n]);

const norm = t => String(t || '').replace(/[\s\u3000]+/g, '')
    .replace(/[，,。.、；;：:？?！!（）()【】\[\]<>《》"'\-—…·$\\{}]/g, '').toLowerCase();
// 题干 4-gram 集合
function g4(t) { const s = norm(t); const o = new Set(); for (let i = 0; i + 4 <= s.length; i++) o.add(s.slice(i, i + 4)); return o; }

// 候选
const pairs = [];   // {zx, core, score}
for (const q of zx) {
    const sec = secOf(q.no);
    const cand = new Set();
    for (const n of (mcMap[q.no] || [])) if (coreByNo[n].sec === sec) cand.add(n);
    for (const c of core) if (c.sec === sec) for (const k of ztKeys(q.src)) if (c.keys.has(k)) cand.add(c.no);
    if (!cand.size) continue;
    const zb = g4(q.body).size ? q.body : '';
    const bg = g4(zb);
    let bs = -1, bn = null;
    for (const n of cand) {
        const cg = g4(coreByNo[n].stem);
        let inter = 0;
        const [sm, lg] = bg.size < cg.size ? [bg, cg] : [cg, bg];
        for (const x of sm) if (lg.has(x)) inter++;
        const sc = inter / Math.max(1, Math.min(bg.size, cg.size));
        if (sc > bs) { bs = sc; bn = n; }
    }
    pairs.push({ zx: q.no, core: bn, score: +bs.toFixed(4), n: cand.size });
}
// 贪心 1:1（按分数降序）
pairs.sort((a, b) => b.score - a.score);
const usedCore = new Set(), map = {};
for (const p of pairs) {
    if (usedCore.has(p.core)) continue;
    if (map[p.zx] !== undefined) continue;
    map[p.zx] = p.core; usedCore.add(p.core);
}
// 统计
let badAdded = 0, restored = 0;
const bySec = {};
for (const z in map) {
    const zno = Number(z);
    if (added.has(zno)) { badAdded++; continue; }
    restored++;
    const s = secOf(zno); bySec[s] = (bySec[s] || 0) + 1;
}
console.log('配对成功:', Object.keys(map).length);
console.log('  ├ 已补录188中误配的(应为0):', badAdded);
console.log('  └ 需找回的:', restored);
console.log('按章:', JSON.stringify(bySec));
const unmatched = zx.map(q => q.no).filter(n => map[n] === undefined);
console.log('未配对的臻选题:', unmatched.length);
const secCntU = {};
for (const n of unmatched) { const s = secOf(n); secCntU[s] = (secCntU[s] || 0) + 1; }
console.log('未配对按章:', JSON.stringify(secCntU));
const unAdded = unmatched.filter(n => !added.has(n));
console.log('未配对中不属于188的（应是目标167的一部分）:', unAdded.length);
console.log('  题号:', unAdded.join(','));
fs.writeFileSync('tools/_zx_restore_map.json', JSON.stringify({ map, unmatched }, null, 1), 'utf8');
