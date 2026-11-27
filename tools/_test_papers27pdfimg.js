/* 27 模拟卷答案册 PDF 原图回归：mn27-03/04/05/06/07 五套 110 题 151 张原图。 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
let pass = 0, fail = 0;
function ok(cond, name) { if (cond) { pass++; console.log('  ✓ ' + name); } else { fail++; console.log('  ✗ ' + name); } }

const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/mn27_papers.json'), 'utf8'));
ok(d.length === 10, 'mn27 共 10 套卷');
const KEYS = ['03', '04', '05', '06', '07'];
const EXPECT = { '03': 33, '04': 32, '05': 29, '06': 28, '07': 29 };
let totalQ = 0, totalImg = 0;
for (const pp of d) {
    const src = pp.source || '';
    const key = src.slice(0, 2);
    const qs = pp.sections.flatMap(s => s.questions);
    if (!KEYS.includes(key)) {
        ok(qs.every(q => !q.ansImg || !q.ansImg.length), `${pp.id} 非目标套卷无 PDF 原图`);
        continue;
    }
    const withImg = qs.filter(q => q.ansImg && q.ansImg.length);
    const refs = withImg.reduce((n, q) => n + q.ansImg.length, 0);
    ok(withImg.length === 22, `${pp.id} 22 题均有 PDF 原图`);
    ok(refs === EXPECT[key], `${pp.id} 原图 ${refs} 张（预期 ${EXPECT[key]}）`);
    ok(withImg.every(q => q.ansImg.every(p => p.startsWith('data/img/zx_site/mn27pdf-' + key + '-'))),
       `${pp.id} 原图命名与套卷匹配`);
    ok(withImg.every(q => q.ansImg.every(p => fs.existsSync(path.join(ROOT, 'pwa', p)))),
       `${pp.id} 原图文件均存在`);
    totalQ += withImg.length; totalImg += refs;
}
ok(totalQ === 110 && totalImg === 151, '5 套合计 110 题 151 张原图');

const sw = fs.readFileSync(path.join(ROOT, 'pwa/sw.js'), 'utf8');
const d2 = d.filter(pp => KEYS.includes((pp.source || '').slice(0, 2)));
let swOk = 0;
for (const pp of d2) for (const q of pp.sections.flatMap(s => s.questions))
    for (const p of q.ansImg || []) if (sw.includes("'" + p + "'")) swOk++;
ok(swOk === 151, 'SW 预缓存全部 151 张原图');
const left = d.filter(pp => !KEYS.includes((pp.source || '').slice(0, 2)));
ok(left.every(pp => pp.sections.flatMap(s => s.questions).every(q => !q.ansImg || !q.ansImg.length)),
   '李林六套等其它 5 套未被误挂原图');

console.log(`\n结果：通过 ${pass}，失败 ${fail}`);
process.exit(fail ? 1 : 0);
