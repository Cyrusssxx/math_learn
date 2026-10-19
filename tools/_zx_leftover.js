// 逐题源组内配对：找出「同源但确实是另一道题」的漏网题
const fs = require('fs');
const zx = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const core = JSON.parse(fs.readFileSync('pwa/data/core_bank.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const coreQ = [];
for (const s of core[0].sections) if (LA.includes(s.title)) for (const q of s.questions) coreQ.push(q);

function canon(p) {
    let s = String(p || '').replace(/[（）()]/g, '').replace(/[、,，]/g, '')
        .replace(/\s+/g, '').replace(/版/g, '').replace(/重点/g, '').replace(/数一数二/, '数一二');
    s = s.replace(/^2[3-7](?=880|900|李艳芳|张宇|余丙森|押题王|超越|李永乐|哈基米|🐙)/, '');
    s = s.replace(/(\d{2,})$/, '');
    return s;
}
const parts = s => String(s || '').split(/[;；]/).map(canon).filter(Boolean);

function toks(s) {
    const o = [];
    for (const m of String(s || '').matchAll(/[\u4e00-\u9fff]{2,}/g)) o.push(m[0]);
    for (const m of String(s || '').matchAll(/\d{2,}/g)) o.push(m[0]);
    return [...new Set(o)];
}
const df = {};
for (const q of coreQ) for (const t of new Set(toks(q.stem || ''))) df[t] = (df[t] || 0) + 1;
const w = t => 1 / Math.log(2 + Math.max(0, df[t] || 0));
function sim(pt, ct) {
    const cs = new Set(ct);
    let tw = 0, iw = 0;
    for (const t of pt) { const ww = w(t); tw += ww; if (cs.has(t)) iw += ww; }
    return tw ? iw / tw : 0;
}
const jie = cat => String(cat || '').split('→').pop().trim();

// 按规范化题源分组
const gz = {}, gc = {};
for (const q of zx) for (const p of new Set(parts(q.src))) (gz[p] = gz[p] || []).push(q);
for (const q of coreQ) for (const p of new Set(parts(q.source || ''))) (gc[p] = gc[p] || []).push(q);

let leftover = [];
for (const src in gz) {
    const P = gz[src], C = gc[src] || [];
    const used = new Set();
    for (const pq of P) {
        const pt = toks(pq.body), pj = jie(pq.cat);
        let best = -1, bestScore = -1;
        C.forEach((cq, i) => {
            if (used.has(i)) return;
            const cj = (cq.deepCats || []).length ? '' : '';
            const sc = sim(pt, toks(cq.stem || ''));
            if (sc > bestScore) { bestScore = sc; best = i; }
        });
        // 同源组内：内容相似度 ≥0.35 视为同题（PDF 正文乱序，阈值不能高）
        if (best >= 0 && bestScore >= 0.35) used.add(best);
        else leftover.push({ no: pq.no, src: pq.src, cat: pq.cat, score: +bestScore.toFixed(2), page: pq.page });
    }
}
console.log('逐组配对后仍无对应（疑似真缺）:', leftover.length, '题');
for (const l of leftover) console.log('  zx#' + l.no + '  ' + l.cat + '  | ' + l.src + '  | 最佳相似 ' + l.score + ' | P' + l.page);
fs.writeFileSync('tools/_zx_leftover.json', JSON.stringify(leftover, null, 1), 'utf8');
