// 最终匹配规则（保守，宁缺勿滥）：
//   同章 + 题源吻合(真题年/卷种 或 同名习题集/模拟卷) + 中文2-gram Dice>=0.5 + 共享gram>=5
// 不满足 → 该臻选题用图片表示（已在库的 188 直接复用；其余需从 PDF 裁图）
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
function diceSet(a, b) { if (!a.size || !b.size) return 0; let i = 0; const [sm, lg] = a.size < b.size ? [a, b] : [b, a]; for (const x of sm) if (lg.has(x)) i++; return (2 * i) / (a.size + b.size); }
function shared(a, b) { let i = 0; const [sm, lg] = a.size < b.size ? [a, b] : [b, a]; for (const x of sm) if (lg.has(x)) i++; return i; }
// 题源：真题 → 年/卷种；书 → 书名
const BOOKM = /880|900|姜晓千|经典题|李永乐六套|李艳芳三套|余丙森五|张宇八套|押题王四套|李永乐|李艳芳|余丙森|张宇|押题王|超越/;
function srcInfo(s) {
    const zt = new Set(), bk = new Set();
    for (const part of String(s || '').split(/[;；]/)) {
        const t = part.trim(); if (!t) continue;
        const ym = t.match(/((?:19|20)\d{2})\s*[,，]?\s*(?:数|数学)/);
        if (ym) {
            const ps = [];
            if (/数一|数学一/.test(t)) ps.push(1);
            if (/数二|数学二/.test(t)) ps.push(2);
            if (/数三|数学三/.test(t)) ps.push(3);
            for (const p of ps) zt.add(ym[1] + '/' + p);
        }
        const bm = t.match(BOOKM);
        if (bm) bk.add(bm[1]);
    }
    return { zt, bk };
}
function srcOK(a, b) {
    if (!a.zt.size && !a.bk.size) return true;      // 一方无源信息 → 不阻拦
    if (!b.zt.size && !b.bk.size) return true;
    for (const k of a.zt) if (b.zt.has(k)) return true;
    for (const k of a.bk) if (b.bk.has(k)) return true;
    return false;
}
function zxText(no) { const c = clean[String(no)]; let t = c.text || ''; for (const p of (c.meta || '').split(' / ')) t = t.replace(p, ' '); return t; }

const Z = [];
for (const no of Object.keys(clean).map(Number)) {
    const sec = zxSecOf(no); if (!sec) continue;
    const src = (clean[String(no)].meta || '').split(' / ').slice(1).join(';');
    Z.push({ no, sec, ...srcInfo(src), cg: g2(zxText(no)) });
}
const C = [];
for (const s of orig.sections) { if (!LA.includes(s.title)) continue; for (const q of s.questions) C.push({ no: q.no, sec: s.title, ...srcInfo(q.source), cg: g2(q.stem), stem: q.stem || '', source: q.source || '' }); }

const pairs = [];
for (const c of C) {
    let bs = 0, bn = null;
    for (const z of Z) {
        if (z.sec !== c.sec) continue;
        if (!srcOK(c, z)) continue;
        const sh = shared(c.cg, z.cg); if (sh < 5) continue;
        const d = diceSet(c.cg, z.cg); if (d < 0.5) continue;
        if (d > bs) { bs = d; bn = z; }
    }
    if (bn) pairs.push({ coreNo: c.no, sec: c.sec, zxNo: bn.no, dice: +bs.toFixed(3), source: c.source, stem: c.stem });
}
pairs.sort((a, b) => b.dice - a.dice);
const usedZ = new Set(), usedC = new Set(), map = {};
for (const p of pairs) { if (usedZ.has(p.zxNo) || usedC.has(p.coreNo)) continue; map[p.coreNo] = p; usedZ.add(p.zxNo); usedC.add(p.coreNo); }
const list = Object.values(map);
const cov = new Set(list.map(p => p.zxNo));
console.log('可安全用文字题表示的臻选题:', cov.size, '/355');
const buckets = { textIn167: 0, textIn188: 0, img: 0, missing: 0 };
const missing = [];
for (const z of Z) {
    if (cov.has(z.no)) { if (added.has(z.no)) buckets.textIn188++; else buckets.textIn167++; }
    else if (added.has(z.no)) buckets.img++;
    else { buckets.missing++; missing.push(z.no); }
}
console.log(JSON.stringify(buckets, null, 1));
console.log('无线下文字对应、也不在已补录188里的（需从 PDF 裁图补入）:', missing.length);
console.log(' 题号:', missing.join(','));
const secCnt = {}; for (const p of list) secCnt[p.sec] = (secCnt[p.sec] || 0) + 1;
console.log('文字题按章:', JSON.stringify(secCnt));
fs.writeFileSync('tools/_zx_final_pairs.json', JSON.stringify(list, null, 1), 'utf8');
fs.writeFileSync('tools/_zx_missing_img.json', JSON.stringify(missing), 'utf8');
