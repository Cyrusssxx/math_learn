// 按「题源年份 + 卷种 + 章」匹配甄选题 ↔ 原核心题库线代题，找回那 167 道
const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const zx = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const added = new Set();
for (const r of [r1, r2]) for (const x of r.inserted) added.add(x.zx);
[103, 112, 153, 263, 344].forEach(n => added.add(n));

// 从 source / src 里抽 (year, papers[]) ；一条可能含多个分号来源
function parseSrc(s) {
    const out = [];
    for (const part of String(s || '').split(/[;；]/)) {
        const t = part.trim(); if (!t) continue;
        const ym = t.match(/((?:19|20)\d{2})/) || t.match(/^\s*(\d{2})\s*年?/);
        if (!ym) { out.push({ year: null, papers: [], raw: t, book: /880|900|姜晓千|经典|李永乐|李艳芳|余丙森|张宇|押题|超越|八套|四套|三套|六套/.test(t) }); continue; }
        let y = ym[1].length === 4 ? ym[1] : '20' + ym[1];
        const papers = [];
        if (/数一|数学一/.test(t)) papers.push(1);
        if (/数二|数学二/.test(t)) papers.push(2);
        if (/数三|数学三/.test(t)) papers.push(3);
        out.push({ year: y, papers, raw: t, book: false });
    }
    return out;
}
// 章名归一（甄选题 src 不带章，用 categoryIds/节）
const CH = { 2: '行列式', 3: '矩阵', 4: '向量', 5: '线性方程组', 6: '特征值与特征向量', 7: '二次型' };
// 原核心题库线代题
const core = [];
for (const s of orig.sections) {
    if (!LA.includes(s.title)) continue;
    for (const q of s.questions) core.push({ no: q.no, sec: s.title, srcs: parseSrc(q.source), source: q.source, stem: q.stem || '' });
}
// 每道核心题能匹配的（年, 卷种）键
const coreKeys = core.map(c => {
    const ys = new Set();
    for (const s of c.srcs) { if (!s.year) continue; for (const p of s.papers) ys.add(s.year + '/' + p); }
    return { no: c.no, sec: c.sec, keys: ys, stem: c.stem, source: c.source };
});
// 臻选题的章（题库里的节）
// 臻选题的章：用 PDF 扉页给出的题号区间（最可靠）
const PDF_RANGE = [[1, 40, '行列式'], [41, 115, '矩阵'], [116, 146, '向量'],
[147, 220, '线性方程组'], [221, 284, '特征值与特征向量'], [285, 355, '二次型']];
function secOfZx(no) { const r = PDF_RANGE.find(x => no >= x[0] && no <= x[1]); return r ? r[2] : null; }

const res = {}; const unmatched = [];
for (const q of zx) {
    const sec = secOfZx(q.no);
    const srcs = parseSrc(q.src);
    // 只保留真题来源（习题集/模拟卷的来源不作为匹配键）
    const zt = srcs.filter(s => s.year);
    let hit = null;
    if (zt.length && sec) {
        const zkeys = new Set();
        for (const s of zt) for (const p of s.papers) zkeys.add(s.year + '/' + p);
        // 找同年同卷种同章的核心题
        const cands = coreKeys.filter(c => c.sec === sec && [...zkeys].some(k => c.keys.has(k)));
        if (cands.length === 1) hit = cands[0];
        else if (cands.length > 1) {
            // 多个候选：用题干相似度挑
            const norm = t => String(t || '').replace(/[\s\u3000]+/g, '').replace(/[，,。.、；;：:？?！!（）()【】\[\]]/g, '').toLowerCase();
            const zt0 = norm(q.body).slice(0, 300);
            let bs = -1;
            for (const c of cands) {
                const ct = norm(c.stem);
                let inter = 0; const a = new Set(); for (let i = 0; i + 4 <= zt0.length; i++) { const g = zt0.slice(i, i + 4); if (ct.includes(g)) a.add(g); }
                inter = a.size;
                if (inter > bs) { bs = inter; hit = c; }
            }
        }
    }
    if (hit) res[q.no] = { coreNo: hit.no, sec: hit.sec, src: q.src };
    else unmatched.push({ no: q.no, sec, src: q.src, zt: zt.map(s => s.year + '/' + s.papers.join('')) });
}
// 校验：188 已补录的不应有匹配
const badAdded = [...added].filter(n => res[n]);
console.log('臻选题能按题源定位到原核心题的:', Object.keys(res).length);
console.log('其中属于已补录188的（应为0）:', badAdded.length, badAdded.slice(0, 10).join(','));
const restored = Object.keys(res).map(Number).filter(n => !added.has(n));
console.log('需找回的（非补录）:', restored.length);
console.log('无法定位的:', unmatched.length);
const secCnt = {};
for (const n of restored) secCnt[res[n].sec] = (secCnt[res[n].sec] || 0) + 1;
console.log('按章分布:', JSON.stringify(secCnt));
console.log('\n无法定位样例:'); unmatched.slice(0, 15).forEach(x => console.log('  #' + x.no, x.sec, '|', x.src, '|', x.zt.join(',')));
fs.writeFileSync('tools/_zx_restore_map.json', JSON.stringify({ res, restored }, null, 1), 'utf8');
