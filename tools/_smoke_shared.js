// 共享模块抽取回归测试：
// 把 exam-shared.js 的 mdBlock 与 exam.js 自带的 mdBlock 喂入全部真题字段，逐字节比对输出。
// 一致 => 抽取未改变任何渲染行为。
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const root = path.join(__dirname, '..');

function makeCtx() {
  const store = new Map();
  const el = () => ({
    style: {}, dataset: {}, classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    appendChild() {}, append() {}, remove() {}, focus() {}, insertBefore() {},
    querySelector() { return null; }, querySelectorAll() { return []; },
    addEventListener() {}, removeEventListener() {}, closest() { return null; },
    setAttribute() {}, getAttribute() { return null; }, replaceWith() {},
  });
  const ctx = {
    console,
    localStorage: {
      getItem: k => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
      removeItem: k => store.delete(k),
    },
    window: {},                       // 无 katex -> renderMath 空转
    document: {
      addEventListener() {}, removeEventListener() {},
      createElement: el, createTextNode: () => ({}),
      querySelector: () => null, querySelectorAll: () => [],
      getElementById: () => null, body: { appendChild() {} },
    },
    indexedDB: { open() { return {}; } },
    setTimeout, clearTimeout, Date, JSON, Math, RegExp, Promise,
    URL: function () {}, Blob: function () {}, Image: function () {},
    alert() {}, confirm() { return true; },
  };
  ctx.globalThis = ctx;
  return vm.createContext(ctx);
}

// 从某个 js 文件中按名字抽取函数源码（兼容 async function）
function grab(src, name) {
  const re = new RegExp('^(?:async\\s+)?function ' + name + '\\s*\\(', 'm');
  const m = re.exec(src);
  if (!m) return null;
  let i = src.indexOf('{', m.index);
  let depth = 0, j = i;
  for (; j < src.length; j++) {
    if (src[j] === '{') depth++;
    else if (src[j] === '}') { depth--; if (depth === 0) break; }
  }
  return src.slice(m.index, j + 1);
}

const sharedSrc = fs.readFileSync(path.join(root, 'pwa/js/exam-shared.js'), 'utf8');
const examSrc = fs.readFileSync(path.join(root, 'pwa/js/exam.js'), 'utf8');

// A: 共享模块
const ctxA = makeCtx();
vm.runInContext(sharedSrc, ctxA);

// B: exam.js 原始版本的同样四个函数
const ctxB = makeCtx();
for (const fn of ['balanceDollars', 'esc', 'mdInline', 'mdBlock']) {
  const code = grab(examSrc, fn);
  if (!code) { console.log('❌ exam.js 未找到函数', fn); process.exit(1); }
  vm.runInContext(code, ctxB);
}

console.log('共享模块函数数:', Object.keys(ctxA).filter(k => typeof ctxA[k] === 'function').length);
console.log('exam.js 对照函数已载入:', ['balanceDollars', 'esc', 'mdInline', 'mdBlock'].every(f => typeof ctxB[f] === 'function'));

// ---- 遍历全部真题字段比对 ----
const data = JSON.parse(fs.readFileSync(path.join(root, 'pwa/data/exam.json'), 'utf8'));
let total = 0, diff = 0;
const samples = [];
function cmp(label, text) {
  if (typeof text !== 'string' || !text) return;
  total++;
  let a, b;
  try { a = ctxA.mdBlock(text); } catch (e) { a = 'ERR:' + e.message; }
  try { b = ctxB.mdBlock(text); } catch (e) { b = 'ERR:' + e.message; }
  if (a !== b) {
    diff++;
    if (samples.length < 3) samples.push({ label, a: String(a).slice(0, 200), b: String(b).slice(0, 200) });
  }
}
for (const ex of data) {
  for (const s of ex.sections || []) {
    for (const q of s.questions || []) {
      const tag = ex.year + ' Q' + q.no;
      cmp(tag + ' stem', q.stem);
      cmp(tag + ' answer', q.answer);
      cmp(tag + ' idea', q.idea);
      if (q.tips) for (const k of Object.keys(q.tips)) cmp(tag + ' tips.' + k, q.tips[k]);
      for (const o of q.options || []) cmp(tag + ' option', o);
    }
  }
}
console.log(`\n=== mdBlock 输出比对 ===`);
console.log(`比对字段数: ${total}, 输出不一致: ${diff}`);
samples.forEach(s => {
  console.log('\n差异字段:', s.label);
  console.log('  shared:', s.a);
  console.log('  exam  :', s.b);
});

// ---- 收藏存储往返测试 ----
const c = ctxA;
const qid = c.qidOf('2014数二真题', 1);
console.log(`\n=== 收藏存储往返 ===`);
console.log('qidOf:', qid);
const before = c.isFav(qid);
const f = c.favGet(); f[qid] = { t: 1756900000000 }; c.favSave(f);
console.log('写入后 isFav:', c.isFav(qid), '| favTime:', c.favTime(qid), '| 格式化:', c.fmtFavTime(c.favTime(qid)));
// 注意：favGet() 每次返回新解析的对象，必须先取出再改再存
const g = c.favGet(); delete g[qid]; c.favSave(g);
console.log('删除后 isFav:', c.isFav(qid), '(初始:', before, ')');
console.log('往返结论:', (c.isFav(qid) === before) ? '✅ 写入/删除往返一致' : '❌ 往返异常');

// ---- 关键回归：裸 $$ 独占一行必须开块 ----
const tricky = '开头\n$$\n\\int_0^1 x\\,dx = \\frac12\n$$\n结尾';
const out = ctxA.mdBlock(tricky);
const ok = /<p>\s*\$\$[\s\S]*?\$\$\s*<\/p>/.test(out.replace(/\s+/g, ' ').includes('$$') ? out : out);
console.log('\n=== 裸 $$ 开块回归 ===');
console.log('输入有跨行 $$ ->', JSON.stringify(out));
console.log('是否合成单个 <p>（应为 true）:', /<p>[^<]*\$\$[\s\S]*\$\$[^<]*<\/p>/.test(out));

console.log('\n' + (diff === 0 ? '✅ 抽取后渲染行为与 exam.js 完全一致' : '❌ 存在不一致，需排查'));
