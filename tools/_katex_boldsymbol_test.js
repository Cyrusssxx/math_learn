// 验证 KaTeX 能渲染 \boldsymbol 与 \(...\) 形态的数学内容（避免 bash inline 转义污染）
const fs = require('fs');
const katex = require('D:/ai code/math-note/pwa/vendor/katex/katex.min.js');

const cases = [
    { src: '\\boldsymbol{y-y_0=k(x-x_0)}', disp: false, note: '用户笔记里的原式内容（行内）' },
    { src: '\\boldsymbol{x_1^2+y_1^2=r^2}', disp: false, note: '含上下标' },
    { src: 'y-y_0=k(x-x_0)', disp: false, note: '无 boldsymbol 对照' },
    { src: '\\boldsymbol{y-y_0=k(x-x_0)}', disp: true, note: '块级（若用户用 \\[..\\]）' },
];

let ok = 0, fail = 0;
for (const c of cases) {
    try {
        const html = katex.renderToString(c.src, { displayMode: c.disp, throwOnError: true, strict: 'ignore' });
        const bold = html.includes('font-weight:bold') || html.includes('boldsymbol') || html.includes('mord');
        console.log('OK  ', c.note, '| 输出含数学节点:', bold, '| 长度', html.length);
        ok++;
    } catch (e) {
        console.log('FAIL', c.note, '|', e.message.slice(0, 80));
        fail++;
    }
}
console.log(`\n\boldsymbol 渲染验证: 成功 ${ok} / 失败 ${fail}`);

// 同时确认 delimiters 改动已写入三个文件
for (const f of ['pwa/js/exam.js', 'pwa/js/exam-shared.js', 'pwa/js/category.js']) {
    const s = fs.readFileSync('D:/ai code/math-note/' + f, 'utf-8');
    const has = s.includes("left: '\\\\('");
    console.log(`${f}: \\( 行内定界符已配置 = ${has}`);
}
