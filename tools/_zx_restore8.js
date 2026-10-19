// 组内顺序配对：同章 + 同真题来源(年/卷种) 的题，两边按出现顺序一一对应。
// 仅真题来源用于分组（习题集/模拟卷来源两书记法不一致，不作分组键）。
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

function ztKeys(s) {
    const out = [];
    for (const part of String(s || '').split(/[;；]/)) {
        const t = part.trim(); if (!t) continue;
        if (/880|900|姜晓千|经典|李永乐|李艳芳|余丙森|张宇|押题|超越|八套|四套|三套|六套/.test(t)) continue;
        const ym = t.match(/((?:19|20)\d{2})\s*(?:数|数学)/); if (!ym) continue;
        const ps = [];
        if (/数一|数学一/.test(t)) ps.push(1);
        if (/数二|数学二/.test(t)) ps.push(2);
        if (/数三|数学三/.test(t)) ps.push(3);
        for (const p of ps) { const k = ym[1] + '/' + p; if (!out.includes(k)) out.push(k); }
    }
    return out.sort();
}
// 按「章 + 真题键集合」建立双侧有序列表
const groups = {};
// 核心库
const coreOrder = [];
for (const s of orig.sections) {
    if (!LA.includes(s.title)) continue;
    for (const q of s.questions) {
        const ks = ztKeys(q.source); if (!ks.length) continue;
        coreOrder.push({ no: q.no, sec: s.title, keys: ks, stem: q.stem || '' });
        for (const k of ks) (groups[k + '|' + s.title] = groups[k + '|' + s.title] || { core: [], zx: [] }).core.push(q.no);
    }
}
const zxOrder = [];
for (const no of Object.keys(clean).map(Number)) {
    const sec = zxSecOf(no); if (!sec) continue;
    const src = (clean[String(no)].meta || '').split(' / ').slice(1).join(';');
    const ks = ztKeys(src); if (!ks.length) continue;
    zxOrder.push({ no, sec, keys: ks });
    for (const k of ks) (groups[k + '|' + sec] = groups[k + '|' + sec] || { core: [], zx: [] }).zx.push(no);
}
// 组内顺序配对（数量不同时按 Dice 校正）
const norm = t => String(t || '').toLowerCase().replace(/[^0-9a-z\u4e00-\u9fff]+/g, '');
function g4(t) { const s = norm(t); const o = new Set(); for (let i = 0; i + 4 <= s.length; i++) o.add(s.slice(i, i + 4)); return o; }
function dice(a, b) { if (!a.size || !b.size) return 0; let i = 0; const [sm, lg] = a.size < b.size ? [a, b] : [b, a]; for (const x of sm) if (lg.has(x)) i++; return (2 * i) / (a.size + b.size); }
function zxText(no) { const c = clean[String(no)]; let t = c.text || ''; for (const p of (c.meta || '').split(' / ')) t = t.replace(p, ' '); return t; }
const coreByNo = {}; for (const c of coreOrder) coreByNo[c.no] = c;
const CG = {}; for (const c of coreOrder) CG[c.no] = g4(c.stem);
const ZG = {}; for (const z of zxOrder) ZG[z.no] = g4(zxText(z.no));

const map = {}; const lowConf = [];
for (const g in groups) {
    const cs = groups[g].core, zs = groups[g].zx;
    if (!cs.length || !zs.length) continue;
    if (cs.length === zs.length) {
        for (let i = 0; i < cs.length; i++) {
            const d = dice(CG[cs[i]], ZG[zs[i]]);
            if (map[cs[i]] === undefined) map[cs[i]] = { zxNo: zs[i], dice: +d.toFixed(3), grp: g };
            if (d < 0.2) lowConf.push({ coreNo: cs[i], zxNo: zs[i], dice: +d.toFixed(3), grp: g });
        }
    } else {
        // 数量不等：用 Dice 做最大权匹配（简化：每个 core 取最佳，冲突时留高分）
        const cand = [];
        for (const c of cs) for (const z of zs) cand.push({ c, z, d: dice(CG[c], ZG[z]) });
        cand.sort((a, b) => b.d - a.d);
        const uc = new Set(), uz = new Set();
        for (const p of cand) { if (uc.has(p.c) || uz.has(p.z)) continue; uc.add(p.c); uz.add(p.z); map[p.c] = { zxNo: p.z, dice: +p.d.toFixed(3), grp: g }; }
    }
}
const list = Object.entries(map).map(([c, v]) => ({ coreNo: +c, ...v }));
console.log('组内配对成功:', list.length);
const bySec = {}; for (const p of list) { const c = coreByNo[p.coreNo]; bySec[c.sec] = (bySec[c.sec] || 0) + 1; }
console.log('按章:', JSON.stringify(bySec));
const covered = new Set(list.map(p => p.zxNo));
console.log('覆盖甄选题数:', covered.size, '/355');
console.log('  落在已补录188内:', [...covered].filter(n => added.has(n)).length);
console.log('  落在未补录167内:', [...covered].filter(n => !added.has(n)).length);
console.log('低置信(<0.2)配对:', lowConf.length);
console.log('\n未补录167里仍未覆盖:', Object.keys(clean).map(Number).filter(n => !added.has(n) && !covered.has(n)).join(','));
fs.writeFileSync('tools/_zx_final_pairs.json', JSON.stringify(list, null, 1), 'utf8');
