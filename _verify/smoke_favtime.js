// 验证收藏时间：存储升级为 {t} 且兼容旧 {qid:1}
const fs = require('fs'), vm = require('vm'), path = require('path');
const PWA = path.resolve('pwa');
const code = fs.readFileSync(PWA + '/js/category.js', 'utf8');

const store = { examFav: JSON.stringify({ '2026数二真题-1': 1 }) };  // 旧格式
const localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = v; },
  removeItem: k => { delete store[k]; }
};
const ctx = {
  console, localStorage,
  document: { getElementById: () => null, createElement: () => ({}), body: { appendChild() {} }, addEventListener() {}, querySelectorAll: () => [] },
  window: { katex: null }, renderMathInElement() {}, alert() {}, setTimeout, clearTimeout,
  fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
};
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + '\n;globalThis.__favGet=favGet;globalThis.__isFav=isFav;globalThis.__favTime=favTime;globalThis.__fmt=fmtFavTime;globalThis.__toggle=toggleFav;', ctx);

const results = [];
const ok = (name, cond) => { results.push((cond ? 'PASS' : 'FAIL') + ' ' + name); return cond; };

// 旧数据兼容
ok('旧格式 isFav 仍为真', ctx.__isFav('2026数二真题-1') === true);
ok('旧格式 favTime=0（未知时间）', ctx.__favTime('2026数二真题-1') === 0);

// 新收藏写 {t}
ctx.__toggle('2026数二真题-2', null);
const v = ctx.__favGet()['2026数二真题-2'];
ok('新收藏存为对象', v && typeof v === 'object');
ok('新收藏含 t 时间戳', v && typeof v.t === 'number' && v.t > 0);
ok('fmtFavTime 格式化', /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(ctx.__fmt(v.t || 0)));

// 取消收藏删除键
ctx.__toggle('2026数二真题-2', null);
ok('取消收藏后键被删除', !('2026数二真题-2' in ctx.__favGet()));

// 旧数据取消也正常
ctx.__toggle('2026数二真题-1', null);
ok('旧格式也能取消', !('2026数二真题-1' in ctx.__favGet()));

console.log(results.join('\n'));
console.log('\nFAVTIME', results.every(r => r.startsWith('PASS')) ? 'ALL PASS' : 'HAS FAIL');
process.exit(results.every(r => r.startsWith('PASS')) ? 0 : 1);
