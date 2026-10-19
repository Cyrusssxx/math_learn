// 最终判定：核心库线代题 ↔ 臻选题
// 双条件：① 同章 且 题源有交集（真题年+卷种，或同名习题集/模拟卷） ② Dice >= 0.20
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
function dice(a, b) { if (!a.size || !b.size) return 0; let i = 0; const [sm, lg] = a.size < b.size ? [a, b] : [b, a]; for (const x of sm) if (lg.has(x)) i++; return (2 * i) / (a.size + b.size); }
// 题源键：真题 → 年/卷种；习题集/模拟卷 → 归一化书名
const BOOK = /880|900|姜晓千|经典题|李永乐|李艳芳|余丙森|张宇|押题王|超越|八套|四套|三套|六套/;
function srcKeys(s) {
    const out = new Set();
    for (const part of String(s || '').split(/[;；]/)) {
        const t = part.trim(); if (!t) continue;
        const ym = t.match(/((?:19|20)\d{2})\s*(?:数|数学)/) || t.match(/^\s*((?:19|20)\d{2})/);
        if (ym) {
            const ps = [];
            if (/数一|数学一/.test(t)) ps.push(1);
            if (/数二|数学二/.test(t)) ps.push(2);
            if (/数三|数学三/.test(t)) ps.push(3);
            for (const p of ps) out.add('ZT:' + ym[1] + '/' + p);
            if (!ps.length) out.add('ZT:' + ym[1]);
        } else if (BOOK.test(t)) {
            const bm = t.match(/(880|900|姜晓千|经典题|李永乐六套|李艳芳三套|余丙森五|张宇八套|押题王四套|超越|李永乐|李艳芳|余丙森|张宇|押题王)/);
            if (bm) out.add('BK:' + bm[1]);
        }
    }
    return out;
}
function zxText(no) { const c = clean[String(no)]; if (!c) return ''; let t = c.text || ''; for (const p of (c.meta || '').split(' / ')) t = t.replace(p, ' '); return t; }
// 甄选题
const Z = [];
for (const no of Object.keys(clean).map(Number)) {
    const sec = zxSecOf(no); if (!sec) continue;
    const meta = clean[String(no)].meta || '';
    const src = meta.split(' / ').slice(1).join(';');
    Z.push({ no, sec, src, keys: srcKeys(src), g: g4(zxText(no)) });
}
// 核心库线代题
const C = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) C.push({ no: q.no, sec: s.title, keys: srcKeys(q.source), g: g4(q.stem), stem: q.stem || '' }); }

const pairs = [];
for (const c of C) {
    let bs = 0, bn = null, bkey = false;
    for (const z of Z) {
        if (z.sec !== c.sec) continue;
        let share = false;
        for (const k of c.keys) if (z.keys.has(k)) { share = true; break; }
        if (!share && c.keys.size && z.keys.size) continue;   // 题源无交集 → 跳过
        const d = dice(c.g, z.g);
        if (d < 0.20) continue;
        if (d > bs) { bs = d; bn = z.no; bkey = share; }
    }
    if (bn) pairs.push({ coreNo: c.no, sec: c.sec, zxNo: bn, dice: +bs.toFixed(4), srcShare: bkey, zxInAdded: added.has(bn) });
}
// 1:1 贪心
pairs.sort((a, b) => b.dice - a.dice);
const usedZ = new Set(), usedC = new Set(), map = {};
for (const p of pairs) { if (usedZ.has(p.zxNo) || usedC.has(p.coreNo)) continue; map[p.coreNo] = p; usedZ.add(p.zxNo); usedC.add(p.coreNo); }
const list = Object.values(map);
console.log('核心库线代题中判定为臻选题的:', list.length, '/', C.length);
const secCnt = {}; for (const p of list) secCnt[p.sec] = (secCnt[p.sec] || 0) + 1;
console.log('按章:', JSON.stringify(secCnt));
const dupAdded = list.filter(p => p.zxInAdded);
console.log('其中对应「已补录188」的（当年误加，需去重）:', dupAdded.length);
console.log('对应「未补录167」的（本次要找回）:', list.length - dupAdded.length);
// 覆盖率
const coveredZx = new Set(list.map(p => p.zxNo));
console.log('\n355 臻选题中被核心库文本题覆盖的:', coveredZx.size);
console.log('  其中在已补录188内:', [...coveredZx].filter(n => added.has(n)).length);
console.log('  其中在未补录167内:', [...coveredZx].filter(n => !added.has(n)).length);
const missOf167 = Object.keys(clean).map(Number).filter(n => !added.has(n) && !coveredZx.has(n));
console.log('未补录167里仍无线代文本对应的:', missOf167.length, '|', missOf167.join(','));
fs.writeFileSync('tools/_zx_final_pairs.json', JSON.stringify(list, null, 1), 'utf8');
