// 把「甄选题里那 167 道本就在核心库的题」重新找回来。
// 做法：原核心题库线代 346 题（core_orig.json）↔ 甄选题 355 题 做 IDF 加权相似度匹配。
// 阈值标定：已补录的 188 题是确定的「不在库」负样本，它们的最高相似度分布就是阈值下界。
const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const zx = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];

// 已补录的 188 个臻选题号
const added = new Set();
for (const r of [r1, r2]) for (const x of r.inserted) added.add(x.zx);
[103, 112, 153, 263, 344].forEach(n => added.add(n));

// 原核心题库线代题
const coreLA = [];
for (const s of orig.sections) {
    if (!LA.includes(s.title)) continue;
    for (const q of s.questions) coreLA.push({ no: q.no, sec: s.title, text: q.stem || '' });
}
console.log('原核心题库线代:', coreLA.length, '| 臻选题:', zx.length, '| 已补录(负样本):', added.size);

// ---------- 归一化 ----------
function norm(s) {
    return String(s || '')
        .replace(/\$\$?[\s\S]*?\$\$?/g, ' ')
        .replace(/\\[a-zA-Z]+/g, ' ')
        .replace(/[{}[\]()\\/,;:!?。，；：！？、""''（）【】<>《》=+\-*^_|~`]/g, ' ')
        .replace(/[\s\u3000]+/g, '');
}
function toks(s) {
    const t = norm(s);
    const out = [];
    for (const m of t.matchAll(/[\u4e00-\u9fff]{2,}/g)) out.push(m[0]);
    for (const m of t.matchAll(/[A-Za-z]{1,}/g)) out.push(m[0].toLowerCase());
    for (const m of t.matchAll(/\d{1,4}/g)) out.push(m[0]);
    return out;
}
// 中文分词近似：把连续中文串按 2-gram 切，避免整串作为一个 token
function grams(tokens) {
    const out = [];
    for (const t of tokens) {
        if (/[\u4e00-\u9fff]/.test(t)) {
            if (t.length <= 2) out.push(t);
            else for (let i = 0; i + 2 <= t.length; i++) out.push(t.slice(i, i + 2));
        } else out.push(t);
    }
    return out;
}

const coreDocs = coreLA.map(q => ({ ...q, g: grams(toks(q.text)) }));
const zxDocs = zx.map(q => ({ no: q.no, g: grams(toks(q.body)) }));

// ---------- IDF ----------
const df = {};
const bump = gs => { const s = new Set(gs); for (const t of s) df[t] = (df[t] || 0) + 1; };
for (const d of coreDocs) bump(d.g);
for (const d of zxDocs) bump(d.g);
const N = coreDocs.length + zxDocs.length;
const idf = t => Math.log((N + 1) / ((df[t] || 0) + 1)) + 1;

function vec(gs) {
    const tf = {};
    for (const t of gs) tf[t] = (tf[t] || 0) + 1;
    const v = {};
    let nrm = 0;
    for (const t in tf) { const w = (1 + Math.log(tf[t])) * idf(t); v[t] = w; nrm += w * w; }
    nrm = Math.sqrt(nrm) || 1;
    for (const t in v) v[t] /= nrm;
    return v;
}
const CV = coreDocs.map(d => ({ no: d.no, sec: d.sec, v: vec(d.g) }));
const ZV = zxDocs.map(d => ({ no: d.no, v: vec(d.g) }));

function cos(a, b) {
    let s = 0;
    const [sm, lg] = a.size < b.size ? [a, b] : [b, a];
    for (const k in sm) if (lg[k] !== undefined) s += sm[k] * lg[k];
    return s;
}

// ---------- 每个臻选题的最高相似核心题 ----------
const best = {};
for (const z of ZV) {
    let bn = null, bs = 0;
    for (const c of CV) { const s = cos(z.v, c.v); if (s > bs) { bs = s; bn = c; } }
    best[z.no] = { coreNo: bn ? bn.no : null, sec: bn ? bn.sec : '', score: bs };
}
// 负样本（188 已补录）的相似度分布 → 标定阈值
const neg = [...added].map(n => best[n] ? best[n].score : 0).sort((a, b) => b - a);
const pos = zx.map(q => q.no).filter(n => !added.has(n)).map(n => best[n].score).sort((a, b) => b - a);
const q = (arr, p) => arr[Math.min(arr.length - 1, Math.floor(arr.length * p))];
console.log('\n负样本(188, 确定不在库) 相似度: max=' + neg[0].toFixed(3), 'p95=' + q(neg, .05).toFixed(3), 'p50=' + q(neg, .5).toFixed(3));
console.log('候选正样本(167, 应在库) 相似度: max=' + pos[0].toFixed(3), 'p50=' + q(pos, .5).toFixed(3), 'p90=' + q(pos, .9).toFixed(3), 'p10=' + q(pos, .1).toFixed(3));
for (const th of [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]) {
    const nf = neg.filter(s => s >= th).length, pf = pos.filter(s => s >= th).length;
    console.log('  阈值 ' + th.toFixed(2) + ': 负样本误判 ' + nf + '/188 | 正样本命中 ' + pf + '/167');
}
fs.writeFileSync('tools/_zx_best_match.json', JSON.stringify(best, null, 1), 'utf8');
