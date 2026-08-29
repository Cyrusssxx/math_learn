// 全量 KaTeX 真实渲染审计：5 个数据文件所有长文本字段的公式逐条渲染（throwOnError）
// 用法: node tools/_katex_check_all.js
const katex = require('katex');
const fs = require('fs');
const path = require('path');
const DATA = path.join(__dirname, '..', 'pwa', 'data');
const re = /\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\$([^$\n]+?)\$|\\\(([\s\S]+?)\\\)/g;

let total = 0, fail = 0;
const fails = [];
function check(tex, disp, loc) {
  total++;
  try {
    katex.renderToString(tex, { throwOnError: true, displayMode: disp, strict: false });
  } catch (e) {
    fail++;
    if (fails.length < 40) fails.push({ loc, err: e.message.split('\n')[0], tex: tex.slice(0, 90) });
  }
}
function scanText(text, loc) {
  if (typeof text !== 'string' || !text.includes('$') && !text.includes('\\(') && !text.includes('\\[')) return;
  let m; re.lastIndex = 0;
  while ((m = re.exec(text))) {
    if (m[1] !== undefined) check(m[1], true, loc);
    else if (m[2] !== undefined) check(m[2], true, loc);
    else if (m[3] !== undefined) check(m[3], false, loc);
    else if (m[4] !== undefined) check(m[4], false, loc);
  }
}
function walk(o, loc) {
  if (typeof o === 'string') scanText(o, loc);
  else if (Array.isArray(o)) o.forEach((v, i) => walk(v, loc + `[${i}]`));
  else if (o && typeof o === 'object') {
    for (const [k, v] of Object.entries(o)) {
      if (k === 'img' || k === 'img2' || k === 'imgs' || k === 'file') continue; // 图片路径不是公式
      walk(v, loc + '.' + k);
    }
  }
}
for (const f of ['exam.json', 'notes.json', 'good.json', 'selected.json', 'practice.json']) {
  const fp = path.join(DATA, f);
  if (!fs.existsSync(fp)) { console.log(f, '不存在，跳过'); continue; }
  const before = [total, fail];
  walk(JSON.parse(fs.readFileSync(fp, 'utf8')), f);
  console.log(`${f}: 公式 ${total - before[0]}，失败 ${fail - before[1]}`);
}
console.log('—— 总计:', total, '| 渲染失败:', fail);
for (const x of fails) console.log(' •', x.loc, '|', x.err, '\n    ', x.tex);
