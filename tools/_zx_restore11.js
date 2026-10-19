// 第二轮：给第一轮漏掉的短题干题补配。
// 规则：同章 + 真题题源相同 + 候选唯一（或多个时取中文 gram 共享最多者）
const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const clean = JSON.parse(fs.readFileSync('tools/_zx_clean_text.json', 'utf8'));
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const prev = JSON.parse(fs.readFileSync('tools/_zx_final_pairs.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const RANGE = [[1, 40, '行列式'], [41, 115, '矩阵'], [116, 146, '向量'], [147, 220, '线性方程组'], [221, 284, '特征值与特征向量'], [285, 355, '二次型']];
const zxSecOf = n => { const r = RANGE.find(x => n >= x[0] && n <= x[1]); return r ? r[2] : null; };
const added = new Set();
for (const r of [r1, r2]) for (const x of r.inserted) added.add(x.zx);
[103, 112, 153, 263, 344].forEach(n => added.add(n));
const norm = t => String(t || '').toLowerCase().replace(/[^0-9a-z\u4e00-\u9fff]+/g, '');
function g2(t) { const s = norm(t); const o = new Set(); for (let i = 0; i + 2 <= s.length; i++) { const g = s.slice(i, i + 2); if (/^[\u4e00-\u9fff]{2}$/.test(g)) o.add(g); } return o; }
function gAll(t) { const s = norm(t); const o = new Set(); for (let i = 0; i + 3 <= s.length; i++) o.add(s.slice(i, i + 3)); return o; }
function shared(a, b) { let i = 0; const [sm, lg] = a.size < b.size ? [a, b] : [b, a]; for (const x of sm) if (lg.has(x)) i++; return i; }
function ztKeys(s) {
    const out = new Set();
    for (const part of String(s || '').split(/[;；]/)) {
        const t = part.trim(); if (!t) continue;
        const ym = t.match(/((?:19|20)\d{2})\s*[,，]?\s*(?:数|数学)/); if (!ym) continue;
        if (/数一|数学一/.test(t)) out.add(ym[1] + '/1');
        if (/数二|数学二/.test(t)) out.add(ym[1] + '/2');
        if (/数三|数学三/.test(t)) out.add(ym[1] + '/3');
    }
    return out;
}
function zxText(no) { const c = clean[String(no)]; let t = c.text || ''; for (const p of (c.meta || '').split(' / ')) t = t.replace(p, ' '); return t; }
const C = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) C.push({ no: q.no, sec: s.title, zt: ztKeys(q.source), source: q.source || '', cg: g2(q.stem), ag: gAll(q.stem), stem: q.stem || '' }); }
const Z = [];
for (const no of Object.keys(clean).map(Number)) {
    const sec = zxSecOf(no); if (!sec) continue;
    const src = (clean[String(no)].meta || '').split(' / ').slice(1).join(';');
    Z.push({ no, sec, zt: ztKeys(src), cg: g2(zxText(no)), ag: gAll(zxText(no)) });
}
const usedCore = new Set(prev.map(p => p.coreNo));
const usedZx = new Set(prev.map(p => p.zxNo));
const extra = [];
for (const z of Z) {
    if (usedZx.has(z.no)) continue;
    if (added.has(z.no)) continue;               // 已在库有图，不必找文字版
    if (!z.zt.size) continue;
    const cands = C.filter(c => c.sec === z.sec && !usedCore.has(c.no) && [...z.zt].some(k => c.zt.has(k)));
    if (!cands.length) continue;
    let pick = null;
    if (cands.length === 1) pick = cands[0];
    else {
        let bs = -1;
        for (const c of cands) { const s = shared(z.ag, c.ag); if (s > bs) { bs = s; pick = c; } }
    }
    if (pick) { usedCore.add(pick.no); usedZx.add(z.no); extra.push({ coreNo: pick.no, sec: z.sec, zxNo: z.no, dice: +(2 * shared(z.cg, pick.cg) / Math.max(1, z.cg.size + pick.cg.size)).toFixed(3), source: pick.source, stem: pick.stem, how: cands.length === 1 ? 'unique' : 'multi' }); }
}
console.log('第二轮补配:', extra.length);
extra.slice(0, 20).forEach(e => console.log('  臻选#' + e.zxNo, '→ core#' + e.coreNo, '(' + e.how + ')', e.source));
const all = prev.concat(extra);
fs.writeFileSync('tools/_zx_final_pairs.json', JSON.stringify(all, null, 1), 'utf8');
const cov = new Set(all.map(p => p.zxNo));
const missing = [];
for (const z of Z) if (!cov.has(z.no) && !added.has(z.no)) missing.push(z.no);
console.log('\n累计覆盖臻选题:', cov.size, '/355');
console.log('仍需裁图的:', missing.length, '|', missing.join(','));
const secCnt = {}; for (const p of all) secCnt[p.sec] = (secCnt[p.sec] || 0) + 1;
console.log('文字题按章:', JSON.stringify(secCnt));
