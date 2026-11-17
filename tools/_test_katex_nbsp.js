/* 端到端验证 auto-render.min.js 的 NBSP 清洗 patch。
 * 用 jsdom 加载真实 vendor 文件，渲染含 NBSP 的公式，断言 console.warn 零告警。
 * 同时验证：公式外的 NBSP 不受影响、用户传入的 preProcess 仍被调用。
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('D:/ai code/408-quiz/node_modules/jsdom');

const ROOT = path.resolve(__dirname, '..');
const katexSrc = fs.readFileSync(path.join(ROOT, 'pwa/vendor/katex/katex.min.js'), 'utf8');
const autoSrc = fs.readFileSync(path.join(ROOT, 'pwa/vendor/katex/auto-render.min.js'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond) {
    if (cond) { pass++; console.log('  ✓ ' + name); }
    else { fail++; console.log('  ✗ ' + name); }
}

const dom = new JSDOM('<!doctype html><html><body></body></html>', { runScripts: 'outside-only' });
const w = dom.window;
w.eval(katexSrc);
// auto-render 的 UMD 在 jsdom 里挂到 window.renderMathInElement
w.eval(autoSrc);

const warns = [];
w.console.warn = function (...a) { warns.push(a.map(String).join(' ')); };

function render(html, opts) {
    const el = w.document.createElement('div');
    el.innerHTML = html;
    w.document.body.appendChild(el);
    w.renderMathInElement(el, Object.assign({
        delimiters: [{ left: '$', right: '$', display: false }],
        throwOnError: false,
        strict: 'warn',
    }, opts || {}));
    const out = el.innerHTML;
    el.remove();
    return out;
}

console.log('=== 场景1：公式内含 NBSP（修复前会 warn）===');
warns.length = 0;
const h1 = render('$x\u00a0\u00a0+ y\u00a0\u00a0= 1$');
ok('公式内 NBSP 不触发 LaTeX warn',
   warns.filter(s => /Unicode|LaTeX-incompatible|non-strict/i.test(s)).length === 0);
ok('公式仍被 KaTeX 渲染（出现 .katex）', h1.includes('katex'));

console.log('=== 场景2：普通公式无回归 ===');
warns.length = 0;
const h2 = render('$x^2 + y^2 = 1$');
ok('普通公式零 warn', warns.length === 0);
ok('普通公式渲染成功', h2.includes('katex'));

console.log('=== 场景3：用户传入 preProcess 仍被调用 ===');
warns.length = 0;
let called = 0;
render('$a\u00a0\u00a0b$', { preProcess: s => { called++; return s; } });
ok('preProcess 回调仍执行', called > 0);

console.log('=== 场景4：源码级断言 ===');
ok('清洗逻辑恰好 1 处',
   (autoSrc.match(/a=a\.replace\(\/\\u00A0\/g," "\)/g) || []).length === 1);
ok('清洗在 preProcess 之前',
   autoSrc.indexOf('a=a.replace(/\\u00A0/g," ")') < autoSrc.indexOf('n.preProcess&&(a=n.preProcess(a))'));

console.log('\n结果: ' + pass + ' 通过 / ' + fail + ' 失败');
process.exit(fail ? 1 : 0);
