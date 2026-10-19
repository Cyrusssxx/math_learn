// 355 题内部查重：找「同一道题以不同题源重复出现」的情况
// 目的：验证序言 315 是否为去重后的题数（355-315=40）
const fs = require('fs');
const zx = JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'));

function sig(s) {
    return String(s || '')
        .replace(/[\s\u3000]+/g, '')
        .replace(/[，,。.、；;：:？?！!（）()【】\[\]<>《》"'\-—…·]/g, '')
        .toLowerCase();
}
// 2-gram 集合
function grams(s, n) {
    const t = sig(s);
    const out = new Set();
    for (let i = 0; i + n <= t.length; i++) out.add(t.slice(i, i + n));
    return out;
}
const G = zx.map(q => ({ no: q.no, g: grams(q.body, 3), len: sig(q.body).length }));
const pairs = [];
for (let i = 0; i < G.length; i++) {
    for (let j = i + 1; j < G.length; j++) {
        const a = G[i].g, b = G[j].g;
        let inter = 0;
        for (const x of a) if (b.has(x)) inter++;
        const uni = a.size + b.size - inter;
        const jac = uni ? inter / uni : 0;
        if (jac >= 0.30) pairs.push({ a: G[i].no, b: G[j].no, jac: +jac.toFixed(3), la: G[i].len, lb: G[j].len });
    }
}
pairs.sort((x, y) => y.jac - x.jac);
console.log('相似度 >=0.55 的题对:', pairs.length);
pairs.slice(0, 30).forEach(p => console.log('  #' + p.a + ' ~ #' + p.b, 'jac=' + p.jac, 'len', p.la + '/' + p.lb));
const involved = new Set();
pairs.forEach(p => { involved.add(p.a); involved.add(p.b); });
console.log('涉及题数:', involved.size, '| 若全部合并去重后题数:', 355 - involved.size);
fs.writeFileSync('tools/_zx_dup_pairs.json', JSON.stringify(pairs, null, 1), 'utf8');
