#!/usr/bin/env node
/* embed_annot.js — 把「导出标注」JSON 里的批注固化进笔记源 md
 * 用法: node tools/embed_annot.js <标注json路径> [--write]
 * 不带 --write 时为 dry-run（只统计，不写文件）
 *
 * 原理：复刻前端 annotate.js 的 sid 分配(keyBlocks: li/p 文档顺序)与
 * 旧哈希锚点迁移(migrateKeys: hash(ownText) remap)，把批注精确插回源 md 条目下。
 */
const fs = require('fs'), vm = require('vm');
const WRITE = process.argv.includes('--write');
const ANNOT_PATH = process.argv[2] || '';
if (!ANNOT_PATH) { console.error('用法: node embed_annot.js <标注json> [--write]'); process.exit(1); }

// ===== KaTeX (node 加载 vendor) =====
const kcode = fs.readFileSync(__dirname + '/../pwa/vendor/katex/katex.min.js', 'utf8');
const fakeEl = () => ({ style: {}, setAttribute() {}, appendChild() {}, getElementsByTagName: () => [], classList: { add() {} }, firstChild: null });
const sb = { module: {}, exports: {}, self: {}, window: {}, document: { createElement: () => fakeEl(), createElementNS: () => fakeEl(), createTextNode: () => ({}), documentElement: { style: {} } }, navigator: { userAgent: 'node' }, setTimeout };
sb.window = sb; vm.createContext(sb); vm.runInContext(kcode, sb);
const katex = sb.module.exports || sb.katex;
const KTEX = t => { try { return katex.renderToString(t, { displayMode: false, throwOnError: false }); } catch (e) { return t; } };
const KDIS = t => { try { return katex.renderToString(t, { displayMode: true, throwOnError: false }); } catch (e) { return t; } };
const unesc = s => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#x27;/g, "'").replace(/&quot;/g, '"');
function hash(s) { let h = 5381; for (let i = 0; i < s.length; i++) h = (h * 33 + s.charCodeAt(i)) >>> 0; return h.toString(36); }

// ===== mdrender（与 pwa/js/mdrender.js 一致）=====
function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function inline(s) {
  return esc(s)
    .replace(/!\[(.*?)\]\((.+?)\)/g, '<img class="li-img" src="$2" alt="$1" loading="lazy">')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/⭐+/g, '<span class="star">$&</span>');
}
function breakLines(text) {
  let inM = false, iffN = 0;
  for (const ch of text) { if (ch === '$') inM = !inM; else if (ch === '⇔' && !inM) iffN++; }
  const cutIff = iffN >= 2;
  const segs = []; let seg = '', inMath = false;
  for (const ch of text) {
    if (ch === '$') inMath = !inMath;
    if (ch === '；' && !inMath) { segs.push(seg); seg = ''; continue; }
    if (cutIff && ch === '⇔' && !inMath) { if (seg) segs.push(seg); seg = '⇔ '; continue; }
    seg += ch;
  }
  if (seg) segs.push(seg);
  if (segs.length > 1) {
    const first = segs[0]; let iM = false, cut = -1;
    for (let i = 0; i < first.length; i++) { if (first[i] === '$') iM = !iM; else if (first[i] === '：' && !iM) { cut = i; break; } }
    if (cut >= 0 && cut < first.length - 1) segs.splice(0, 1, first.slice(0, cut + 1), first.slice(cut + 1));
  }
  return segs.map(inline).join('<br>');
}
/** 块渲染后 ownText（模拟前端 ownText：排除子列表、去空白；br 无文本） */
function blockOwnText(text) {
  const inl = breakLines(text);
  let h = inl.replace(/\$\$([\s\S]+?)\$\$/g, (m, t) => KDIS(unesc(t)))
             .replace(/\$([^$\n]+?)\$/g, (m, t) => KTEX(unesc(t)));
  return h.replace(/<br\s*\/?>/g, '').replace(/<[^>]+>/g, '')
          .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
          .replace(/&#x27;/g, "'").replace(/&quot;/g, '"')
          .replace(/\s+/g, ' ').trim();
}

// ===== 行级块解析（复刻 mdToHtml 的 li/p 文档顺序）=====
function computeSids(md) {
  const lines = md.split('\n').map(l => l.replace(/<!--.*?-->/g, '').replace(/\s+$/, ''));
  const blocks = []; let i = 0;
  function walk(items, start, level) {
    let idx = start;
    while (idx < items.length && items[idx].level >= level) {
      if (items[idx].level > level) { idx++; continue; }
      blocks.push({ type: 'li', level: items[idx].level, text: items[idx].text, line: items[idx].line });
      let j = idx + 1;
      if (j < items.length && items[j].level > level) { const n = walk(items, j, items[j].level); j = n; }
      idx = j;
    }
    return idx;
  }
  while (i < lines.length) {
    const line = lines[i], t = line.trim();
    if (!t || line.startsWith('# ')) { i++; continue; }
    if (line.startsWith('## ')) { i++; continue; }
    if (/^:::\s*fold\b/.test(t) || t === ':::') { i++; continue; }
    if (/^!\[.*?\]\(.+?\)$/.test(t)) { i++; continue; }
    if (/^\s*- /.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*- /.test(lines[i])) { const m = lines[i].match(/^(\s*)- (.*)$/); items.push({ level: Math.floor(m[1].length / 2), text: m[2], line: i }); i++; }
      walk(items, 0, 0); continue;
    }
    if (t.startsWith('|')) { while (i < lines.length && lines[i].trim().startsWith('|')) i++; continue; }
    blocks.push({ type: 'p', text: t, line: i }); i++;
  }
  return blocks;
}

function stripFm(md) {
  const lines = md.split('\n');
  if (lines.length && lines[0].trim() === '---') {
    for (let i = 1; i < lines.length; i++) if (lines[i].trim() === '---') return { md: lines.slice(i + 1).join('\n'), off: i + 1 };
  }
  return { md, off: 0 };
}

// ===== 主流程 =====
const obj = JSON.parse(fs.readFileSync(ANNOT_PATH, 'utf8'));
const annot = (obj && obj.__v === 2) ? (obj.annot || {}) : obj;
const imgs = (obj && obj.__v === 2) ? (obj.imgs || {}) : {};
const SRC_DIR = fs.existsSync('D:/ai code/math/导图') ? 'D:/ai code/math/导图' : null;
const HT_DIR = fs.existsSync('D:/ai code/math/好题') ? 'D:/ai code/math/好题' : null;
const COLOR = { y: '黄', g: '绿', b: '蓝' };

const report = [];
let G_total = 0, G_notes = 0, G_hl = 0, G_marks = 0, G_orphan = 0, G_img = 0;
let imgSaved = 0;
const IMG_DIR = (SRC_DIR || HT_DIR) + '/img';
function fmtNote(t) {
  return t.replace(/\[图:([a-z0-9]+)\]/g, (m, id) => {
    const durl = imgs[id]; if (!durl) return '[图片已丢失]';
    const m2 = /^data:image\/(\w+);base64,(.+)$/.exec(durl); if (!m2) return '[图片无法嵌入]';
    const ext = m2[1] === 'jpeg' ? 'jpg' : m2[1];
    fs.mkdirSync(IMG_DIR, { recursive: true });
    const fp = IMG_DIR + '/' + id + '.' + ext;
    if (!fs.existsSync(fp)) { fs.writeFileSync(fp, Buffer.from(m2[2], 'base64')); imgSaved++; G_img++; }
    return '![批注图片](img/' + id + '.' + ext + ')';
  }).replace(/\n+/g, ' ');
}
function fmtMark(t) { return t.replace(/\n+/g, ' ').slice(0, 120); }

for (const id of Object.keys(annot)) {
  const b = annot[id];
  const notesN = Object.keys(b.notes || {}).length, hlN = Object.keys(b.hl || {}).length, marksN = (b.marks || []).length;
  if (!notesN && !hlN && !marksN) continue;
  let path = (SRC_DIR ? SRC_DIR + '/' + id + '.md' : '');
  if (!path || !fs.existsSync(path)) path = (HT_DIR && fs.existsSync(HT_DIR + '/' + id + '.md')) ? HT_DIR + '/' + id + '.md' : '';
  if (!fs.existsSync(path)) { report.push({ id, err: '源文件不存在' }); continue; }
  const raw = fs.readFileSync(path, 'utf8');
  const { md, off } = stripFm(raw);
  const blocks = computeSids(md);
  const ownList = blocks.map(bl => blockOwnText(bl.text));
  const byHash = {};
  ownList.forEach((t, i) => { const h = hash(t); (byHash[h] || (byHash[h] = [])).push(i); });
  const remap = oldKey => {
    const m = /^(.*)#(\d+)$/.exec(oldKey);
    const h = m ? m[1] : oldKey, occ = m ? parseInt(m[2], 10) : 1;
    const L = byHash[h];
    return (L && L[occ - 1] !== undefined) ? L[occ - 1] : null;
  };
  const sidOf = k => {
    if (/#\d+$/.test(k)) { const idx = parseInt(k.split('#')[1], 10); return (idx >= 0 && idx < blocks.length) ? idx : null; }
    const hit = remap(k); return (hit !== null && hit < blocks.length) ? hit : null;
  };

  // 组装插入：sid -> 行
  const recBySid = {};
  let perOrphan = 0;
  const add = (sid, kind, payload) => {
    if (sid === null || !blocks[sid]) { G_orphan++; perOrphan++; return; }
    const bl = blocks[sid];
    (recBySid[sid] || (recBySid[sid] = [])).push({ kind, payload });
  };
  for (const [k, t] of Object.entries(b.notes || {})) add(sidOf(k), 'note', t);
  for (const [k, c] of Object.entries(b.hl || {})) add(sidOf(k), 'hl', c);
  for (const m of (b.marks || [])) add(sidOf(m.k), 'mark', { t: m.t, c: m.c });

  // 生成嵌入行文本
  const pad = n => '  '.repeat(n);
  const lines = raw.split('\n');
  const toInsert = []; // {line, text}
  const samples = []; // 抽查：目标条目文本
  for (const [sid, recs] of Object.entries(recBySid)) {
    const bl = blocks[Number(sid)];
    samples.push(mdClip(bl.text, 44));
    const ind = pad(bl.level + 1);
    const outLines = [];
    const noteFirst = recs.filter(r => r.kind === 'note');
    const others = recs.filter(r => r.kind !== 'note');
    for (const r of noteFirst) outLines.push(ind + '- 📝 批注：' + fmtNote(r.payload));
    for (const r of others) {
      if (r.kind === 'hl') outLines.push(ind + '- 🖍️ 荧光·' + (COLOR[r.payload] || r.payload));
      else if (r.kind === 'mark') outLines.push(ind + '- 🖍️ 荧光「' + fmtMark(r.payload.t) + '」·' + (COLOR[r.payload.c] || r.payload.c));
    }
    toInsert.push({ line: bl.line + off, text: outLines.join('\n') });
    G_notes += noteFirst.length; G_hl += recs.filter(r => r.kind === 'hl').length; G_marks += recs.filter(r => r.kind === 'mark').length;
  }
  // 逆序插入
  toInsert.sort((a, b) => b.line - a.line);
  for (const ins of toInsert) lines.splice(ins.line + 1, 0, ins.text);
  const out = lines.join('\n');
  report.push({ id, blocks: blocks.length, embedded: toInsert.length, orphan: perOrphan, samples: samples });
  if (WRITE) fs.writeFileSync(path, out);
}

function mdClip(s, n) { return (s || '').replace(/\s+/g, ' ').trim().slice(0, n); }

console.log('=== 批注嵌入（' + (WRITE ? '写入' : 'DRY-RUN') + '）===');
for (const r of report) {
  console.log('  ' + r.id + ': 块数=' + r.blocks + ' 嵌入条目=' + r.embedded + ' 孤儿=' + r.orphan + (r.err ? '  [' + r.err + ']' : ''));
  if (!WRITE && r.samples && r.samples.length) console.log('    目标示例: ' + r.samples.slice(0, 3).join(' ｜ '));
}
console.log('图片写入:', imgSaved, '张');
