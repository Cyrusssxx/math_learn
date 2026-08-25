// 最小 DOM 桩：验证 toggleAllAnswers 一次性展开/收起当前列表所有答案
const fs = require('fs'), vm = require('vm'), path = require('path');
const PWA = path.resolve('pwa');
const code = fs.readFileSync(PWA + '/js/category.js', 'utf8');

function mkOpt() {
  return { _on: false, textContent: '查看答案', classList: { toggle(c, on) { this._on = !!on; } } };
}
function mkCard() {
  const ans = { hidden: true };
  const opt = mkOpt();
  return {
    querySelector(sel) {
      if (sel === '.q-answer') return ans;
      if (sel === '.q-op[data-act="answer"]') return opt;
      return null;
    }
  };
}
const cards = [mkCard(), mkCard()];
const catMain = {
  querySelectorAll(sel) { return sel === '.q-card' ? cards : []; }
};
const btn = { _on: false, textContent: '', classList: { toggle(c, on) { this._on = !!on; } } };

const document = {
  getElementById(id) { return id === 'catMain' ? catMain : null; },
  createElement() { return {}; },
  body: { appendChild() {} },
  addEventListener() {},
  querySelectorAll() { return []; }
};
const ctx = { console, localStorage: { getItem: () => null, setItem() {} }, document, window: { katex: null }, renderMathInElement() {}, alert() {}, setTimeout, clearTimeout, fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }) };
ctx.globalThis = ctx;
vm.createContext(ctx);
// 只取 toggleAllAnswers 与 allAnsOpen 逻辑，注入桩后调用
const wrapped = code + '\n;globalThis.__toggle = toggleAllAnswers;globalThis.__getState = () => ({ btnOn: false });';
vm.runInContext(wrapped, ctx);

// 初始：答案都 hidden
console.log('初始 card1.ans.hidden =', cards[0].querySelector('.q-answer').hidden, '(应 true)');

ctx.__toggle(btn);
console.log('展开后: card1.ans.hidden =', cards[0].querySelector('.q-answer').hidden, '(应 false)');
console.log('        card2.ans.hidden =', cards[1].querySelector('.q-answer').hidden, '(应 false)');
console.log('        按钮文案 =', JSON.stringify(btn.textContent), '(应 收起全部答案)');
console.log('        按钮 on  =', btn._on, '(应 true)');

ctx.__toggle(btn);
console.log('收起后: card1.ans.hidden =', cards[0].querySelector('.q-answer').hidden, '(应 true)');
console.log('        按钮文案 =', JSON.stringify(btn.textContent), '(应 展开全部答案)');

const pass = cards[0].querySelector('.q-answer').hidden === true && btn.textContent === '🔼 展开全部答案';
console.log('\nALL-ANS SMOKE', pass ? 'PASS' : 'FAIL');
process.exit(pass ? 0 : 1);
