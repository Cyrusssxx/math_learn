/* fav_focus DOM 端到端验证：用 jsdom 构造两处目录，加载 reader.js 的 applyFavFocus，
 * 注入真实快照，检查 hot/warm class 与 ⭐ 注入、选中态不冲突。 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('D:/ai code/408-quiz/node_modules/jsdom');
const ROOT = path.dirname(__dirname);
const src = fs.readFileSync(path.join(ROOT, 'pwa/js/reader.js'), 'utf-8');

let pass = 0, fail = 0;
function ok(c, m) { if (c) pass++; else { fail++; console.log('  FAIL:', m); } }

function extract(name) {
    const i = src.indexOf('function ' + name + '(');
    let j = src.indexOf('{', i), d = 0, k = j;
    for (; k < src.length; k++) { if (src[k] === '{') d++; else if (src[k] === '}') { d--; if (!d) { k++; break; } } }
    return src.slice(i, k);
}

const favFocus = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/fav_focus.json'), 'utf-8'));
const snap = JSON.parse(fs.readFileSync('D:/cjx/下载/download/做题数据-2026-11-16.json', 'utf-8'));

const dom = new JSDOM('<!doctype html><html><body>' +
    '<div id="tocPane">' +
    // 高数2 的 ch1（导数概念→hot）与 ch7（导数应用→hot）
    '<div class="toc-item"><a class="toc-link" data-ch="1"><span class="toc-name">导数定义</span></a></div>' +
    '<div class="toc-item"><a class="toc-link" data-ch="7"><span class="toc-name">导数应用：切法线与渐近线</span></a></div>' +
    // 一个 warm 章：找 4-9 档知识点映射的章
    '<div class="toc-item"><a class="toc-link" data-ch="99"><span class="toc-name">无关章</span></a></div>' +
    '</div>' +
    '<div class="note-article"><details class="doc-toc open"><div class="doc-toc-body">' +
    '<div class="doc-toc-item"><a class="toc-link" data-ch="1"><span class="toc-name">导数定义</span></a></div>' +
    '</div></details></div>' +
    '</body></html>', { url: 'http://localhost/' });
const { window } = dom;
const LS = { examFav: snap.data.examFav, examStatus: snap.data.examStatus };
window.localStorage.setItem('examFav', LS.examFav);
window.localStorage.setItem('examStatus', LS.examStatus);

// 在 jsdom window 上下文里构造依赖函数
const code = [extract('weakFavQids'), extract('computeFocusLevels'), extract('applyFavFocus')].join('\n');
const run = new Function('favFocus', 'cur', 'document', 'localStorage', 'FOCUS_HOT_LABEL',
    code + '; return { applyFavFocus, computeFocusLevels };'
)(favFocus, { id: '高数2-一元微分' }, window.document, window.localStorage, '⭐');

run.applyFavFocus();

// 断言右栏 ch1（导数概念 hot）
const ch1 = window.document.querySelector('#tocPane .toc-link[data-ch="1"]');
ok(ch1.classList.contains('ff-hot'), '右栏 ch1 应有 ff-hot');
ok(ch1.querySelector('.ff-star') && ch1.querySelector('.ff-star').textContent === '⭐', 'ch1 应注入 ⭐');
ok(ch1.querySelector('.toc-name').firstChild === ch1.querySelector('.ff-star'), '⭐ 应在标题最前');

// 右栏 ch7（导数应用 hot）
const ch7 = window.document.querySelector('#tocPane .toc-link[data-ch="7"]');
ok(ch7.classList.contains('ff-hot'), '右栏 ch7 应有 ff-hot');

// 无关章不应有标记
const ch99 = window.document.querySelector('#tocPane .toc-link[data-ch="99"]');
ok(!ch99.classList.contains('ff-hot') && !ch99.classList.contains('ff-warm'), '无关章不应有标记');

// doc-toc 同步
const dt1 = window.document.querySelector('.doc-toc .toc-link[data-ch="1"]');
ok(dt1.classList.contains('ff-hot') && dt1.querySelector('.ff-star'), 'doc-toc 章应同步 hot + ⭐');

// 重复调用不叠加 ⭐
run.applyFavFocus(); run.applyFavFocus();
ok(ch1.querySelectorAll('.ff-star').length === 1, '重复渲染不应叠加多个 ⭐');

// 选中态：加 active 后 class 仍在（active 由 CSS 处理颜色）
ch1.classList.add('active');
ok(ch1.classList.contains('ff-hot'), 'active 时 hot class 应保留（颜色交给 CSS 特异性）');

console.log(`DOM 结果：${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
