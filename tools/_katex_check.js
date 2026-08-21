const katex = require('katex');
const fs = require('fs');
const path = 'D:/ai code/math-note/pwa/data/exam.json';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
const re = /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$/g;
let total = 0, fail = 0; const fails = [];
function check(tex, disp, loc) {
  total++;
  try { katex.renderToString(tex, { throwOnError: true, displayMode: disp, strict: false }); }
  catch (e) { fail++; if (fails.length < 30) fails.push({ loc, err: e.message.split('\n')[0], tex: tex.slice(0, 90) }); }
}
for (const p of data) {
  for (const s of p.sections) {
    for (const q of s.questions) {
      for (const blk of [q.stem || '', q.answer || '', q.idea || '']) {
        let m; re.lastIndex = 0;
        while ((m = re.exec(blk))) {
          if (m[1] !== undefined) check(m[1], true, `${p.year} ${s.title} Q${q.no}`);
          else if (m[2] !== undefined) check(m[2], false, `${p.year} ${s.title} Q${q.no}`);
        }
      }
    }
  }
}
console.log('公式总数:', total, '| 渲染失败:', fail, '(' + (fail / total * 100).toFixed(1) + '%)');
for (const f of fails) console.log(' •', f.loc, '|', f.err, '\n    ', f.tex);
