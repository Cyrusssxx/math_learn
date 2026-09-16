#!/usr/bin/env node
/* 校验 bank_questions.json 精写批次（idx 0-15）：$ 配平、控制字符、KaTeX 渲染 */
const fs = require('fs');
const katex = require('D:/ai code/math-note/pwa/vendor/katex/katex.min.js');
const bank = JSON.parse(fs.readFileSync('D:/ai code/math-note/pwa/data/bank_questions.json', 'utf-8'));
const re = /\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$/g;
let total = 0, fail = 0, bad = 0, checked = 0;
for (const it of bank.items) {
    const txt = it.explanation || '';
    if (!txt.includes('$$') && !txt.includes('\\begin')) continue;   // 只查含公式的精写文本
    checked++;
    for (const line of txt.split('\n')) {
        if (line.trim() && (line.match(/\$/g) || []).length % 2) { console.log('奇数$:', (it.source || '') + ':', line.slice(0, 50)); bad++; }
    }
    if (/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(txt)) { console.log('控制字符:', it.source || ''); bad++; }
    re.lastIndex = 0;
    let m;
    while ((m = re.exec(txt)) !== null) {
        total++;
        try { katex.renderToString(m[1] !== undefined ? m[1] : m[2], { displayMode: m[1] !== undefined, throwOnError: true, strict: 'ignore' }); }
        catch (e) { fail++; if (fail <= 8) console.log('KATEX:', (it.source || '') + ':', String(m[1] !== undefined ? m[1] : m[2]).slice(0, 60)); }
    }
}
console.log('含公式文本数:', checked, '| 公式:', total, '| 失败:', fail, '| 配平/控制字符异常:', bad);