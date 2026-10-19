// 重建核心题库线代六节 = 355 道臻选题，一题一道，不重不漏。
// 表示策略：原库有文字版的用文字版（质量更高，且能保住用户旧标记）；
//           没有的用图片版（已在库的 188 道复用，剩 24 道用新裁的图）。
const fs = require('fs');
const orig = JSON.parse(fs.readFileSync('tools/_core_orig.json', 'utf8'))[0];
const cur = JSON.parse(fs.readFileSync('pwa/data/core_bank.json', 'utf8'))[0];
const pairs = JSON.parse(fs.readFileSync('tools/_zx_final_pairs.json', 'utf8'));
const cropped = JSON.parse(fs.readFileSync('tools/_zx_missing_cropped.json', 'utf8'));
const r1 = JSON.parse(fs.readFileSync('tools/_zx_insert_report.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync('tools/_zx_insert2_report.json', 'utf8'));
const LA = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
const RANGE = [[1, 40, '行列式'], [41, 115, '矩阵'], [116, 146, '向量'], [147, 220, '线性方程组'], [221, 284, '特征值与特征向量'], [285, 355, '二次型']];
const zxSecOf = n => { const r = RANGE.find(x => n >= x[0] && n <= x[1]); return r ? r[2] : null; };
const zx2core = {}; for (const p of pairs) zx2core[p.zxNo] = p.coreNo;
// 二轮低置信匹配中已人工核对为误配的 7 个（改用裁好的图片表示）
const BAD = new Set([15, 93, 100, 156, 180, 249, 306]);
for (const n of BAD) delete zx2core[n];
const added = {};
for (const r of [r1, r2]) for (const x of r.inserted) added[x.zx] = x.no;
Object.assign(added, { 103: 1173, 112: 1174, 153: 1175, 263: 1176, 344: 1177 });
const cropByNo = {}; for (const c of cropped) cropByNo[c.no] = c;

// 原库题（含全部字段）与当前图题
const origByNo = {}, curByNo = {};
for (const s of orig.sections) for (const q of s.questions) origByNo[q.no] = q;
for (const s of cur.sections) for (const q of s.questions) curByNo[q.no] = q;

// type 推断（新图题用）：从甄选目录 + 题干特征
const catOf = {};
for (const z of JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8'))) catOf[z.no] = z.cat || '';
function guessType(zxNo) {
    const c = catOf[zxNo] || '';
    const leaf = c.split('→').pop().trim();
    if (/选择/.test(leaf) || /判定|判断|证明.*相似|可逆的判定/.test(leaf)) return 'choice';
    return 'calc';
}

let nextNo = 1300;
const buckets = { text: 0, imgReuse: 0, imgNew: 0 };
const newQs = [];
const sections = {};
for (const [, , sec] of RANGE) sections[sec] = [];
for (let no = 1; no <= 355; no++) {
    const sec = zxSecOf(no);
    const coreNo = zx2core[no];
    if (coreNo && origByNo[coreNo]) {
        // 用原库文字题（保持原 no → 用户旧标记复活）
        const q = Object.assign({}, origByNo[coreNo]);
        delete q.fromX; delete q.xdNo;
        sections[sec].push(q);
        buckets.text++;
        continue;
    }
    if (added[no] && curByNo[added[no]]) {
        sections[sec].push(curByNo[added[no]]);
        buckets.imgReuse++;
        continue;
    }
    const cr = cropByNo[no];
    if (!cr || !cr.qimg) { console.log('✗ #' + no + ' 无图可用'); continue; }
    const q = {
        no: nextNo,
        kind: guessType(no) === 'choice' ? 'choice' : 'calc',
        type: guessType(no),
        stem: '（臻选题补录题，完整题面见下方配图）',
        options: [],
        answer: '【答案与解析】完整过程见下方配图（源自《线代臻选题·通用答案》）。\n\n'
            + cr.aimgs.map(a => '![](data/img/' + a.replace('pwa/data/img/', '')).join('\n'),
        idea: '考点：' + (catOf[no] || '').split('→').pop().trim() + '。本题取自《线代臻选题》第 '
            + (JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8')).find(x => x.no === no).page || '?')
            + ' 页（#' + String(no).padStart(3, '0') + '），题面与详解均为原书截图；建议先独立完成再对照解析。',
        categoryIds: [curByNo[added[no]] ? curByNo[added[no]].categoryIds[0] : 0],
        catId: 0,
        deepCats: [],
        linkedQid: null,
        source: (catOf[no] && (JSON.parse(fs.readFileSync('tools/_zx_parsed.json', 'utf8')).find(x => x.no === no).src)) || '',
        srcPage: null,
        srcOrder: no,
        status: 'transcribed',
        key: false,
        img: cr.qimg.replace('pwa/', ''),
    };
    // categoryIds 用同章任一已有题的叶子（兜底）
    if (!q.categoryIds[0]) {
        const anySec = sections[sec][0];
        q.categoryIds = anySec ? anySec.categoryIds.slice() : [9];
        q.catId = q.categoryIds[0];
    } else q.catId = q.categoryIds[0];
    // deepCats 用 deepcat 映射（沿用该题在 cat_deep 的叶子）
    const cd = JSON.parse(fs.readFileSync('pwa/data/cat_deep.json', 'utf8'));
    sections[sec].push(q);
    newQs.push(q);
    buckets.imgNew++;
    nextNo++;
}
console.log('重建结果:', JSON.stringify(buckets), '| 合计', buckets.text + buckets.imgReuse + buckets.imgNew);
// 组装（保持高数在前、线代六章按 PDF 顺序）
const out = [{ id: 'core', year: '', title: '数二核心题库（大观严选题）', file: '', sections: [] }];
for (const s of cur.sections) if (!LA.includes(s.title)) out[0].sections.push(s);
for (const [, , sec] of RANGE) out[0].sections.push({ title: sec, questions: sections[sec] });
fs.writeFileSync('pwa/data/core_bank.json', JSON.stringify(out), 'utf8');
let t = 0; for (const s of out[0].sections) t += s.questions.length;
console.log('核心库总题数:', t);
for (const s of out[0].sections) console.log('  ' + s.title + ' = ' + s.questions.length);
