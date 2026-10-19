// 用干净题干重做匹配：找回甄选题中本就在原核心库的那 167 道
const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const clean = JSON.parse(fs.readFileSync('tools/_zx_clean_text.json', 'utf8'));
const vs = JSON.parse(fs.readFileSync('tools/_zx_vs_core.json', 'utf8'));
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const RANGE = [[1, 40, '行列式'], [41, 115, '矩阵'], [116, 146, '向量'], [147, 220, '线性方程组'], [221, 284, '特征值与特征向量'], [285, 355, '二次型']];
const secOf = n => { const r = RANGE.find(x => n >= x[0] && n <= x[1]); return r ? r[2] : null; };
const added = new Set();
for (const r of [r1, r2]) for (const x of r.inserted) added.add(x.zx);
[103, 112, 153, 263, 344].forEach(n => added.add(n));

// 核心库线代题
const core = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) core.push({ no: q.no, sec: s.title, stem: q.stem || '', source: q.source || '' }); }
const coreByNo = {}; for (const c of core) coreByNo[c.no] = c;
const mcMap = {}; for (const v of vs) mcMap[v.no] = (v._mc || []).filter(n => coreByNo[n]);

// 只保留 数字/字母/汉字：数学符号（& \ { } $ 等）和标点全部剥掉，
// 否则 LaTeX 题干与 PDF 文本题干的 4-gram 永远对不上
const norm = t => String(t || '').toLowerCase().replace(/[^0-9a-z\u4e00-\u9fff]+/g, '');
function g4(t) { const s = norm(t); const o = new Set(); for (let i = 0; i + 4 <= s.length; i++) o.add(s.slice(i, i + 4)); return o; }
// 去掉题干里的目录/题源前缀（灰条文字被并进来了）
function zxText(no) {
    const c = clean[String(no)]; if (!c) return '';
    let t = c.text || '';
    const meta = c.meta || '';
    for (const part of meta.split(' / ')) { t = t.replace(part, ' '); }
    return t;
}
const CG = core.map(c => ({ no: c.no, sec: c.sec, g: g4(c.stem), gs: c.stem }));
const pairs = [];
for (const no of Object.keys(clean).map(Number)) {
    const sec = secOf(no);
    const cand = new Set();
    for (const n of (mcMap[no] || [])) if (coreByNo[n].sec === sec) cand.add(n);
    // 全章候选：用 4-gram 命中数做粗筛，避免 O(n*m) 全算太慢但这里 n 不大
    const zg = g4(zxText(no));
    if (!zg.size) continue;
    for (const c of CG) {
        if (c.sec !== sec) continue;
        let inter = 0;
        const sm = zg.size < c.g.size ? zg : c.g, lg = zg.size < c.g.size ? c.g : zg;
        for (const x of sm) if (lg.has(x)) inter++;
        if (inter >= 6) cand.add(c.no);
    }
    if (!cand.size) continue;
    let bs = -1, bn = null;
    for (const n of cand) {
        const c = CG.find(x => x.no === n);
        let inter = 0;
        const sm = zg.size < c.g.size ? zg : c.g, lg = zg.size < c.g.size ? c.g : zg;
        for (const x of sm) if (lg.has(x)) inter++;
        const sc = inter / Math.max(1, Math.min(zg.size, c.g.size));
        if (sc > bs) { bs = sc; bn = n; }
    }
    pairs.push({ zx: no, core: bn, score: +bs.toFixed(4), ncand: cand.size });
}
pairs.sort((a, b) => b.score - a.score);
const used = new Set(), map = {};
for (const p of pairs) { if (used.has(p.core) || map[p.zx] !== undefined) continue; map[p.zx] = p.core; used.add(p.core); }

// 分数分布：负样本(188) vs 候选正样本
const negs = pairs.filter(p => added.has(p.zx)).map(p => p.score).sort((a, b) => b - a);
const poss = pairs.filter(p => !added.has(p.zx)).map(p => p.score).sort((a, b) => b - a);
const pct = (a, p) => a.length ? a[Math.min(a.length - 1, Math.floor(a.length * p))].toFixed(3) : '-';
console.log('负样本(188已补录) 相似度: n=' + negs.length, 'max=' + (negs[0] || 0).toFixed(3), 'p95=' + pct(negs, .05), 'p50=' + pct(negs, .5));
console.log('候选正样本(应找回) 相似度: n=' + poss.length, 'max=' + (poss[0] || 0).toFixed(3), 'p50=' + pct(poss, .5), 'p10=' + pct(poss, .1));
for (const th of [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6]) {
    console.log('  阈值 ' + th.toFixed(2) + ': 负样本过线 ' + negs.filter(s => s >= th).length + '/188 | 正样本过线 ' + poss.filter(s => s >= th).length + '/167');
}
let badAdded = 0, restored = 0; const bySec = {};
for (const z in map) { const n = Number(z); if (added.has(n)) { badAdded++; continue; } restored++; bySec[secOf(n)] = (bySec[secOf(n)] || 0) + 1; }
console.log('\n配对成功', Object.keys(map).length, '| 误入188的', badAdded, '| 需找回', restored);
console.log('按章:', JSON.stringify(bySec));
const un = Object.keys(clean).map(Number).filter(n => map[n] === undefined && !added.has(n));
console.log('仍未配对且非补录:', un.length, '|', un.join(','));
fs.writeFileSync('tools/_zx_restore_map.json', JSON.stringify({ map, scores: pairs }, null, 1), 'utf8');
