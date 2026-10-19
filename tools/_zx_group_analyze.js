const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const zx = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const RANGE = [[1, 40, '行列式'], [41, 115, '矩阵'], [116, 146, '向量'], [147, 220, '线性方程组'], [221, 284, '特征值与特征向量'], [285, 355, '二次型']];
const secOf = n => { const r = RANGE.find(x => n >= x[0] && n <= x[1]); return r ? r[2] : null; };

// 抽真题来源键：年/卷种
function ztKeys(s) {
    const out = new Set();
    for (const part of String(s || '').split(/[;；]/)) {
        const t = part.trim(); if (!t) continue;
        if (/880|900|姜晓千|经典|李永乐|李艳芳|余丙森|张宇|押题|超越|八套|四套|三套|六套/.test(t)) continue;  // 习题/模拟不作为真题键
        const ym = t.match(/((?:19|20)\d{2})\s*数/) || t.match(/^\s*((?:19|20)\d{2})/);
        if (!ym) continue;
        const y = ym[1];
        const ps = [];
        if (/数一|数学一/.test(t)) ps.push(1);
        if (/数二|数学二/.test(t)) ps.push(2);
        if (/数三|数学三/.test(t)) ps.push(3);
        for (const p of ps) out.add(y + '/' + p);
    }
    return [...out];
}
// 核心题
const core = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) core.push({ no: q.no, sec: s.title, keys: ztKeys(q.source), source: q.source, stem: q.stem || '' }); }
const zxq = zx.map(q => ({ no: q.no, sec: secOf(q.no), keys: ztKeys(q.src), src: q.src, body: q.body || '' }));

// 按 (章, 真题键) 分组
function groupBy(list) {
    const m = {};
    for (const x of list) {
        const ks = x.keys.length ? x.keys : ['NOZT'];
        for (const k of ks) {
            const gk = x.sec + '|' + k;
            (m[gk] = m[gk] || { core: [], zx: [] });
            if (x.stem !== undefined) m[gk].core.push(x.no); else m[gk].zx.push(x.no);
        }
    }
    return m;
}
const G = groupBy(core.concat(zxq));
let both = 0, coreOnly = 0, zxOnly = 0, mismatch = 0;
const mism = [];
for (const g in G) {
    const c = G[g].core.length, z = G[g].zx.length;
    if (c && z) { both += Math.min(c, z); if (c !== z) { mismatch++; mism.push({ g, core: c, zx: z }); } }
    else if (c) coreOnly += c; else zxOnly += z;
}
console.log('同章同真题键分组:');
console.log('  两侧都有题(可配对):', both);
console.log('  仅核心库有:', coreOnly);
console.log('  仅甄选题有:', zxOnly);
console.log('  两侧数量不一致的组:', mismatch);
mism.sort((a, b) => (b.core - b.zx) - (a.core - a.zx)).slice(0, 15).forEach(m => console.log('   ', m.g, 'core=' + m.core, 'zx=' + m.zx));
