// exam.json 全库（27 卷）全字段 KaTeX 渲染检测
const fs = require('fs');
const katex = require('D:/ai code/math-note/pwa/vendor/katex/katex.min.js');
const d = JSON.parse(fs.readFileSync('D:/ai code/math-note/pwa/data/exam.json', 'utf-8'));
const re = /\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$/g;
let total = 0, fail = 0;
const fails = [];
for (const p of d) {
  for (const sec of p.sections) {
    for (const q of sec.questions) {
      const fields = [['stem', q.stem], ['answer', q.answer], ['idea', q.idea || '']];
      (q.options || []).forEach((o, i) => fields.push([`opt${'ABCD'[i]}`, o]));
      Object.entries(q.tips || {}).forEach(([k, v]) => {
        if (typeof v === 'string') fields.push(['tips.' + k, v]);
        else if (Array.isArray(v)) v.forEach((x, j) => fields.push([`tips.${k}[${j}]`, x]));
      });
      for (const [name, txt] of fields) {
        if (!txt || !txt.includes('$')) continue;
        re.lastIndex = 0;
        let m;
        while ((m = re.exec(txt)) !== null) {
          total++;
          const src = m[1] !== undefined ? m[1] : m[2];
          try {
            katex.renderToString(src, { displayMode: m[1] !== undefined, throwOnError: true, strict: 'ignore' });
          } catch (e) {
            fail++;
            if (fails.length < 12) fails.push(`${p.id} Q${q.no} ${name}: ${String(src).slice(0, 60)} :: ${String(e.message).slice(0, 100)}`);
          }
        }
      }
    }
  }
}
console.log(`exam.json KaTeX: total=${total}, fail=${fail}`);
if (fails.length) console.log(fails.join('\n'));
process.exit(fail ? 1 : 0);
