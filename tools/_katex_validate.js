// 全数据文件 KaTeX 渲染 + 定界符配平验证（数据改动后必跑，配合 tools/_audit_latex.py）
// 用法: node tools/_katex_validate.js
// 覆盖: notes.json / good.json / selected.json / exam.json 全部字符串字段的 $..$ 与 $$..$$ 块
const fs = require('fs');
let katex;
try { katex = require('katex'); }
catch (e) { katex = require('D:/ai code/math-note/pwa/vendor/katex/katex.min.js'); }

const FILES = [
  'D:/ai code/math-note/pwa/data/notes.json',
  'D:/ai code/math-note/pwa/data/good.json',
  'D:/ai code/math-note/pwa/data/selected.json',
  'D:/ai code/math-note/pwa/data/exam.json',
];
const re = /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$/g;

function extract(blk) {
  const out = []; if (!blk) return out; let m; re.lastIndex = 0;
  while ((m = re.exec(blk))) out.push({ tex: m[1] !== undefined ? m[1] : m[2], disp: m[1] !== undefined });
  return out;
}
function walk(o, path, out) {
  if (typeof o === 'string') out.push({ path, text: o });
  else if (Array.isArray(o)) o.forEach((v, i) => walk(v, path + '[' + i + ']', out));
  else if (o && typeof o === 'object') Object.keys(o).forEach(k => walk(o[k], path + '.' + k, out));
}

let total = 0, fail = 0, balFail = 0;
const fails = [];
for (const f of FILES) {
  const data = JSON.parse(fs.readFileSync(f, 'utf8'));
  const blobs = [];
  walk(data, '', blobs);
  for (const { path, text } of blobs) {
    if ((text.match(/\$/g) || []).length % 2 !== 0) {
      balFail++;
      if (fails.length < 60) fails.push({ f: f.split('/').pop(), path, kind: 'dollar-odd', snippet: text.slice(0, 80) });
    }
    // 行级奇数 $：mdToHtml 按行渲染，若某行 $ 为奇说明公式跨行断开(KaTeX 单$不跨行, 静默漏渲染)。
    // 相邻两行都奇 => 跨行断; 单行孤立奇 => 孤儿 $。都报。
    const lines = text.split('\n');
    for (let li = 0; li < lines.length; li++) {
      if (lines[li].match(/\$/g) && (lines[li].match(/\$/g) || []).length % 2 === 1) {
        const solo = !(li > 0 && (lines[li - 1].match(/\$/g) || []).length % 2 === 1) &&
                     !(li + 1 < lines.length && (lines[li + 1].match(/\$/g) || []).length % 2 === 1);
        if (fails.length < 60) fails.push({ f: f.split('/').pop(), path, kind: solo ? 'dollar-line-solo' : 'dollar-line-pair',
          tex: `行${li} $数奇: ${lines[li].slice(0, 90)}` });
        balFail++;
      }
    }
    for (const { tex, disp } of extract(text)) {
      total++;
      try {
        katex.renderToString(tex, { displayMode: disp, throwOnError: true, strict: false });
      } catch (e) {
        fail++;
        if (fails.length < 60) fails.push({ f: f.split('/').pop(), path, kind: 'katex', tex: tex.slice(0, 120), err: String(e.message || e).slice(0, 140) });
      }
    }
  }
}
console.log('公式总数:', total, '| 渲染失败:', fail, '| 奇数$块/行:', balFail);
if (fails.length) {
  console.log('--- 失败明细 ---');
  for (const x of fails) console.log(`[${x.f}] ${x.kind} ${x.path}\n   ${x.tex || x.snippet}\n   ${x.err || ''}`);
  process.exit(1);
}
console.log('ALL OK');