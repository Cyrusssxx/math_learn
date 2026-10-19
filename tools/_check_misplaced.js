// 核心题库「串位分支」全面检测：
//  A. 节归属与内容 keyword 不符（线代节里混高数 / 高数节里混线代）
//  B. categoryIds 的叶子父章 ≠ 所在节
//  C. deepCats 的祖先链与 categoryIds 的章不一致
//  D. linkedQid 指向的真题题，其章节与本题节不一致
const fs = require('fs');
const cb = JSON.parse(fs.readFileSync('pwa/data/core_bank.json', 'utf8'))[0];
const cats = JSON.parse(fs.readFileSync('pwa/data/exam_categories.json', 'utf8'));
const cd = JSON.parse(fs.readFileSync('pwa/data/cat_deep.json', 'utf8'));
const exam = JSON.parse(fs.readFileSync('pwa/data/exam.json', 'utf8'));

const GAO = ['极限','一元微分','一元积分','多元微分','二重积分','微分方程'];
const LA = ['行列式','矩阵','向量','线性方程组','特征值与特征向量','二次型'];
const KW_LA = /矩阵|行列式|向量|特征值|特征向量|正交|相似|合同|二次型|伴随|秩|可逆|线性相关|线性无关|线性表示|方程组|特征多项式|对角化|惯性指数|正定|代数余子式|余子式|基础解系|解空间|增广/;
const KW_GAO = /函数|极限|导数|微分|积分|连续|间断|收敛|级数|泰勒|傅里叶|切线|法线|曲率|极值|最值|拐点|不定积分|定积分|换元|分部积分|牛顿|拉格朗日|罗尔|零点定理|介值|原函数|反常/;

function secOf(id) { const c = cats[String(id)]; if (!c) return null; const ch = cats[String(c.parentId)]; return ch ? ch.name : null; }
// deepCats 的最高层章（cat_deep 里有「线性代数」这个 L1 吗？）
function deepChain(id) {
    const out = []; let cur = String(id), g = 0;
    while (cur && g++ < 12) { const n = cd.nodes[cur]; if (!n) break; out.push(n.n); cur = n.p ? String(n.p) : null; }
    return out.reverse();
}
const A = [], B = [], C = [], D = [];
let nText = 0, nImg = 0;
for (const s of cb.sections) {
    const inLA = LA.includes(s.title), inGao = GAO.includes(s.title);
    for (const q of s.questions) {
        if (q.img) nImg++; else nText++;
        const stem = (q.stem || '') + ' ' + (q.idea || '');
        // A：仅对有文字题干的题做 keyword 判断
        if (!q.img && stem.trim().length > 25) {
            const la = (stem.match(new RegExp(KW_LA.source, 'g')) || []).length;
            const ga = (stem.match(new RegExp(KW_GAO.source, 'g')) || []).length;
            if (inLA && ga >= 3 && ga >= la * 2) A.push({ no: q.no, sec: s.title, la, ga, src: q.source, stem: (q.stem || '').replace(/\s+/g, ' ').slice(0, 90) });
            if (inGao && la >= 3 && la >= ga * 2) A.push({ no: q.no, sec: s.title, la, ga, src: q.source, stem: (q.stem || '').replace(/\s+/g, ' ').slice(0, 90) });
        }
        // B：categoryIds 跨章
        for (const c of (q.categoryIds || [])) {
            const p = secOf(c);
            if (p && p !== s.title) B.push({ no: q.no, sec: s.title, leafCh: p, leaf: (cats[String(c)] || {}).name, cid: c });
        }
        // C：deepCats 链与节不符（用 L2 叶子反查章）
        for (const d of (q.deepCats || []).map(String)) {
            const ch = deepChain(d);
            const hit = LA.find(x => ch.includes(x));
            if (hit && !LA.includes(s.title)) C.push({ no: q.no, sec: s.title, deep: d, deepChain: ch.join('>') });
            if (!hit && LA.includes(s.title) && !ch.includes('线性代数') && cd.nodes[d]) {
                // 线代节的题，deepCats 却不在线性代数树下
                const maybe = GAO.find(x => ch.includes(x));
                if (maybe) C.push({ no: q.no, sec: s.title, deep: d, deepChain: ch.join('>') });
            }
        }
        // D：linkedQid 指向真题，真题章节与本题节不符
        if (q.linkedQid) {
            const key = String(q.linkedQid);
            const m = key.match(/^exam-(\d+)-(\d+)/) || key.match(/^(\d+)-(\d+)$/);
            // 真题 qid 形如 'exam-<paperId>-<no>'，逐卷找
            let found = null;
            for (const p of exam) for (const ss of (p.sections || [])) for (const qq of (ss.questions || [])) {
                if (qidEq(qq, p, key)) { found = { paper: p.id, year: p.year, secTitle: ss.title, no: qq.no }; break; }
            }
            if (found && found.secTitle && found.secTitle !== s.title) D.push({ no: q.no, sec: s.title, linkSec: found.secTitle, linkPaper: found.paper, year: found.year, linkNo: found.no });
        }
    }
}
function qidEq(q, paper, key) { return false; }   // linkedQid 形式另行核对，见下

console.log('核心题库', nText + nImg, '题（文字', nText, '/ 图片', nImg, '）\n');
console.log('A. 节归属与内容 keyword 不符：', A.length, '题');
A.slice(0, 25).forEach(x => console.log('   #' + x.no, '[' + x.sec + '] 线代词' + x.la + '/高数词' + x.ga, '|', x.src, '|', x.stem));
console.log('\nB. categoryIds 叶子父章 ≠ 所在节：', B.length, '题');
B.slice(0, 25).forEach(x => console.log('   #' + x.no, '节=' + x.sec, '→ 叶子父章=' + x.leafCh, '(' + x.leaf + ')'));
console.log('\nC. deepCats 链与节不符：', C.length, '题');
C.slice(0, 15).forEach(x => console.log('   #' + x.no, '节=' + x.sec, '| deepCats=' + x.deep, '链=' + x.deepChain));
