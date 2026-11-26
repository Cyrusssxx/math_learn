/* 真题页原图解析页签回归：静态断言 + 函数行为 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const src = fs.readFileSync(path.join(ROOT, 'pwa/js/exam.js'), 'utf8');
let pass = 0, fail = 0;
function ok(name, cond) { if (cond) { pass++; console.log('  ✓', name); } else { fail++; console.log('  ✗', name); } }

console.log('=== A. 静态接线');
ok('qCard 答案区用 examAnsTabsHtml', /q-sec q-answer[\s\S]{0,200}\$\{examAnsTabsHtml\(q\)\}/.test(src));
ok('定义 examAnsTabsHtml', /function examAnsTabsHtml\(q\)/.test(src));
ok('定义 preloadExamAnsImgs', /function preloadExamAnsImgs\(root\)/.test(src));
ok('定义 switchExamAnsTab', /function switchExamAnsTab\(btn, which\)/.test(src));
ok('有 ansImg 才出页签', /const tabs = imgs\.length\s*\?/.test(src));
ok('原图 span 用 data-src 延迟挂载', /img class="q-ans-img" data-src=/.test(src));
ok('原图点击走 zoomAnsImg', /onclick="zoomAnsImg\(this\)"/.test(src));
ok('展开答案时预加载', /act === 'answer'\) preloadExamAnsImgs\(sec\)/.test(src));
ok('一键展开时预加载', /preloadExamAnsImgs\(el\)/.test(src));

console.log('=== B. 反向：不得复用分类页全局函数');
ok('不调用 category.js 的 ansTabsHtml', !/\$\{ansTabsHtml\(q\)\}/.test(src));
ok('不覆盖 exam-shared 的 zoomAnsImg', (src.match(/function zoomAnsImg\(/g) || []).length === 1);

console.log('=== C. 函数行为抽取（纯函数片段）');
function fnBody(name) {
    const i = src.indexOf('function ' + name + '(');
    if (i < 0) return '';
    let depth = 0, start = src.indexOf('{', i), j = start;
    for (; j < src.length; j++) { if (src[j] === '{') depth++; else if (src[j] === '}') { depth--; if (!depth) break; } }
    return src.slice(i, j + 1);
}
const helper = fnBody('examAnsTextMeaningful');
const tabsFn = fnBody('examAnsTabsHtml');
const body = helper + '\n' + tabsFn + '\nreturn examAnsTabsHtml;';
const make = new Function('mdBlock', 'esc', body);
const html = make(s => `<p>${s}</p>`, s => String(s).replace(/&/g, '&amp;'));

const withImg = html({ answer: '**【答案】** 计算得 $\\frac{8}{3}$，过程完整。', ansImg: ['data/img/zx_site/ex2009-19_0.webp'] });
ok('有图+有文字→两个页签', (withImg.match(/ans-tab/g) || []).length === 3); // 2 buttons + container class
ok('含原图解析按钮', withImg.includes('原图解析'));
ok('原图默认 hidden', /ans-pane-img" hidden/.test(withImg));
ok('文字解析默认显示', /ans-pane ans-pane-text"><div class="q-answer-body"/.test(withImg));
ok('图片只有 data-src 无 src', /data-src="data\/img\/zx_site/.test(withImg) && !/<img[^>]*\ssrc=/.test(withImg));

const onlyImg = html({ answer: '完整过程见下方配图。', ansImg: ['data/img/zx_site/c316_0.webp'] });
ok('无实质文字→只一个页签', (onlyImg.match(/<button class="ans-tab/g) || []).length === 1);
ok('文字面板 hidden', /ans-pane ans-pane-text" hidden/.test(onlyImg));

const noImg = html({ answer: '普通答案', ansImg: [] });
ok('无图→无页签', !noImg.includes('ans-tabs'));
ok('无图→文字面板显示', /<div class="q-answer-body"><p>普通答案<\/p>/.test(noImg));

console.log(`\n结果：通过 ${pass}，失败 ${fail}`);
process.exit(fail ? 1 : 0);
