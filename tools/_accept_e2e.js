// 端到端 DOM 执行测试：手动注入 selected.html 的真实脚本链到 jsdom 并执行 init()
const fs = require('fs');
const { JSDOM } = require('jsdom');
const ROOT = 'D:/ai code/math-note/pwa';

const dom = new JSDOM(`<!DOCTYPE html><html><head></head><body>
  <header><span id="examSub"></span><button id="favOnly"></button></header>
  <aside><div id="paperList"></div></aside>
  <main id="examMain"><div class="loading">加载中…</div></main>
  <div id="floatQ"><span id="floatQNo"></span><div id="floatQList"></div></div>
  <span id="darkState"></span>
</body></html>`, { runScripts: 'outside-only', url: 'http://localhost/pwa/selected.html', pretendToBeVisual: true });
const { window } = dom;
const doc = window.document;

// 注入真实脚本（顺序同 selected.html 的 defer 链）
window.eval(fs.readFileSync(ROOT + '/js/common.js', 'utf8'));
window.eval(fs.readFileSync(ROOT + '/vendor/katex/katex.min.js', 'utf8'));
window.eval(fs.readFileSync(ROOT + '/vendor/katex/auto-render.min.js', 'utf8'));
console.log('katex 已加载:', !!window.katex, '| auto-render 已加载:', !!window.renderMathInElement);

// 拦截 fetch -> 本地 selected.json
const data = JSON.parse(fs.readFileSync(ROOT + '/data/selected.json', 'utf8'));
window.fetch = (p) => Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve(JSON.parse(JSON.stringify(data))) });

// 执行 selected.js（会调用 init()）
try { window.eval(fs.readFileSync(ROOT + '/js/selected.js', 'utf8')); }
catch (e) { console.log('选中 selected.js 执行抛错:', e.message); process.exit(1); }

setTimeout(() => {
  const cards = doc.querySelectorAll('.q-card');
  const katex = doc.querySelectorAll('.katex');
  const imgs = doc.querySelectorAll('.ans-img');
  let left = '$';
  const w = doc.createTreeWalker(doc.body, window.NodeFilter.SHOW_TEXT, null);
  let n; while ((n = w.nextNode())) { if (n.nodeValue && n.nodeValue.includes('$')) left += '|' + n.nodeValue.slice(0, 40); }
  console.log('=== 端到端 DOM 执行测试 ===');
  console.log('题目卡片 .q-card:', cards.length, '(期望 16 = 第一套卷)');
  console.log('.katex 公式渲染数:', katex.length, '(期望 >0)');
  console.log('答案 <img.ans-img> 数:', imgs.length, '(期望 >0，方案A答案图)');
  console.log('残留 $ 文本:', left === '$' ? '(无)' : left);
  console.log('渲染后 .katex-error:', doc.querySelectorAll('.katex-error').length);
  console.log('paperList 套卷按钮数:', doc.querySelectorAll('#paperList .paper-item').length, '(期望 31)');
  console.log('examMain 是否仍显示“加载中”:', doc.getElementById('examMain').textContent.includes('加载中'));
  if (cards.length === 16 && katex.length > 0 && imgs.length > 0 && left === '$') {
    console.log('RESULT: PASS ✅ 页面真实渲染链路完全正常');
  } else {
    console.log('RESULT: FAIL ❌ 见上');
    process.exitCode = 1;
  }

  // 交互路径验证（直接调用全局函数，模拟真实点击，避开 jsdom 内联 onclick 绑定限制）
  try {
    const c0 = doc.querySelector('.q-card'); const qid0 = c0.id.replace('q-', '');
    window.toggleFav(qid0, c0.querySelector('.q-fav'));
    const favStored = window.localStorage.getItem('selFav-' + qid0) === '1';
    window.toggleQSec(c0.querySelector('[data-act=answer]'), 'answer');
    const ansOpen = c0.querySelector('.q-answer').hidden === false;
    window.toggleFavOnly();
    const filtered = doc.querySelectorAll('.q-card').length === 1;
    console.log('--- 交互验证 ---');
    console.log('收藏写入:', favStored, '| 答案展开:', ansOpen, '| 只看收藏过滤到1题:', filtered);
    console.log('交互 RESULT:', (favStored && ansOpen && filtered) ? 'PASS ✅' : 'FAIL ❌');
  } catch (e) { console.log('交互验证抛错:', e.message); }
}, 800);
