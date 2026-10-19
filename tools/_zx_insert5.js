// 补录剩余 5 题（#103 #112 #153 #263 #344）→ core_bank
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const ROOT = path.join(__dirname, '..');
const cd = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/cat_deep.json'), 'utf8'));
const nodes = cd.nodes;
const hasChild = new Set(Object.values(nodes).map(v => String(v.p)));
const isLeaf = id => !hasChild.has(String(id));

const a5 = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/_zx_add5.json'), 'utf8'));
const zx = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/_zx_parsed.json'), 'utf8'));
const byNo = {}; for (const q of zx) byNo[q.no] = q;

// 考点 → 叶子；skipFirstImg: 首图是题面（与题干重复）需剔除
const SPEC = {
  103: { leaf: '45', chap: '矩阵', skipFirst: false },
  112: { leaf: '47', chap: '矩阵', skipFirst: false },
  153: { leaf: '133', chap: '线性方程组', skipFirst: true },
  263: { leaf: '194', chap: '特征值与特征向量', skipFirst: true },
  344: { leaf: '220', chap: '二次型', skipFirst: true },
};
const bank = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/core_bank.json'), 'utf8'));
const secs = bank[0].sections;
let mx = 0; for (const s of secs) for (const q of s.questions) mx = Math.max(mx, q.no);
let no = mx;
const added = [];
for (const k of Object.keys(SPEC)) {
  const z = Number(k), sp = SPEC[k], q = byNo[z];
  if (!isLeaf(sp.leaf)) throw new Error('非叶子: ' + sp.leaf);
  const sec = secs.find(s => s.title === sp.chap);
  if (!sec) throw new Error('无章节: ' + sp.chap);
  let imgs = a5[k].slice(sp.skipFirst ? 1 : 0);
  if (!imgs.length) throw new Error('#' + k + ' 无答案图');
  no++;
  const rel = p => p.replace(/^.*pwa\//, '');
  sec.questions.push({
    no,
    kind: 'choice',
    type: 'choice',
    stem: '（臻选题补录题，完整题面见下方配图）',
    options: [],
    answer: '【答案与解析】完整过程见下方配图（源自《线代臻选题·通用答案》）。\n\n' + imgs.map(p => `![](${rel(p)})`).join('\n\n'),
    idea: `考点：${String(q.cat).split('→').pop().trim()}。本题取自《线代臻选题》第 ${q.page} 页（#${String(z).padStart(3, '0')}），题面与详解均为原书截图。`,
    categoryIds: [Number(sp.leaf)],
    catId: Number(sp.leaf),
    deepCats: [sp.leaf],
    linkedQid: null,
    source: q.src,
    srcPage: q.page,
    srcOrder: z,
    status: 'transcribed',
    key: false,
    img: `data/img/zx_q/zx${String(z).padStart(3, '0')}.png`,
  });
  added.push({ zx: z, no, chap: sp.chap, leaf: sp.leaf, imgs: imgs.length });
}
fs.writeFileSync(path.join(ROOT, 'pwa/data/core_bank.json'), JSON.stringify(bank), 'utf8');
console.log('补录', added.length, '题:', added.map(a => `zx#${a.zx}→core#${a.no}(${a.chap}/${a.leaf})`).join(' '));
