/* 考研数学笔记 - 纯 Markdown 渲染函数（与 reader.js 内的实现对齐）
 * 独立成文件，供「好题刷题」模块(good.js)直接加载，避免引入 reader.js 的 init() 逻辑。
 * 这些函数只依赖全局 KaTeX auto-render（renderMathInElement），不触碰任何笔记专有状态。
 */

function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** 行内格式：转义 → 图片、加粗、⭐高亮；$...$ 原样保留交给 KaTeX */
function inline(s) {
    return esc(s)
        .replace(/!\[(.*?)\]\((.+?)\)/g, '<img class="li-img" src="$2" alt="$1" loading="lazy">')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/⭐+/g, '<span class="star">$&</span>');
}

/** 长条目分行：公式外的"；"后断行；含 ⇔ 等价链（≥2个）时逐条断行，⇔ 显示在下一行开头。
 *  文字原样保留只插 <br>，textContent 不变 → 已有批注/荧光锆点不失效 */
function breakLines(text) {
    // 先数公式外 ⇔ 个数，决定是否按等价链拆行
    let inM = false, iffN = 0;
    for (const ch of text) {
        if (ch === '$') inM = !inM;
        else if (ch === '⇔' && !inM) iffN++;
    }
    const cutIff = iffN >= 2;

    const segs = [];
    let seg = '', inMath = false;
    for (const ch of text) {
        if (ch === '$') inMath = !inMath;
        if (ch === '；' && !inMath) { segs.push(seg); seg = ''; continue; }
        if (cutIff && ch === '⇔' && !inMath) {
            if (seg) segs.push(seg);
            seg = '⇔ ';   // ⇔ 挪到下一行开头，形成箭头对齐的等价链
            continue;
        }
        seg += ch;
    }
    if (seg) segs.push(seg);
    if (segs.length > 1) {
        const first = segs[0];
        let iM = false, cut = -1;
        for (let i = 0; i < first.length; i++) {
            if (first[i] === '$') iM = !iM;
            else if (first[i] === '：' && !iM) { cut = i; break; }
        }
        if (cut >= 0 && cut < first.length - 1)
            segs.splice(0, 1, first.slice(0, cut + 1), first.slice(cut + 1));
    }
    return segs.map(inline).join('<br>');
}

/** 列表项样式类：⚠️ 易错 / 💡 技巧 / 例：例题；⭐ 叠加常考高亮 */
function liClass(text) {
    const cls = [];
    if (text.includes('⚠️')) cls.push('c-warn');
    else if (text.includes('💡')) cls.push('c-tip');
    else if (/^例[：（(]/.test(text.trim())) cls.push('c-example');
    if (text.includes('⭐')) cls.push('c-star');
    return cls.length ? ` class="${cls.join(' ')}"` : '';
}

/** 递归输出嵌套列表；items = [{level, text}] */
function emitList(items, start, level) {
    let html = '<ul>';
    let i = start;
    while (i < items.length && items[i].level >= level) {
        if (items[i].level > level) { i++; continue; }  // 容错：跳级缩进
        html += `<li${liClass(items[i].text)}>` + breakLines(items[i].text);
        let j = i + 1;
        if (j < items.length && items[j].level > level) {
            const [childHtml, next] = emitList(items, j, items[j].level);
            html += childHtml;
            j = next;
        }
        html += '</li>';
        i = j;
    }
    return [html + '</ul>', i];
}

/** 表格行分列：忽略 $...$ 公式内部的 |（如 $\dfrac{|A|}{\lambda}$） */
function splitRow(line) {
    const s = line.trim().replace(/^\|/, '').replace(/\|$/, '');
    const cells = [];
    let cell = '', inMath = false;
    for (const ch of s) {
        if (ch === '$') inMath = !inMath;
        if (ch === '|' && !inMath) { cells.push(cell.trim()); cell = ''; }
        else cell += ch;
    }
    cells.push(cell.trim());
    return cells;
}

function emitTable(rows) {
    let html = '<table>';
    rows.forEach((cells, r) => {
        if (r === 1) return;  // |---|---| 分隔行
        const tag = r === 0 ? 'th' : 'td';
        html += '<tr>' + cells.map(c => `<${tag}>${inline(c)}</${tag}>`).join('') + '</tr>';
    });
    return html + '</table>';
}

/** 防御：未闭合的 $$ 会拖垮整篇渲染，奇数时在末尾补一个闭合 $$ 兜底。 */
function balanceDollars(md) {
    const n = (md.match(/\$\$/g) || []).length;
    return n % 2 === 0 ? md : md + '$$';
}
/* ============ 📌 点睛块（::: 点睛 … :::）============
 * 源 md 写法（Obsidian 亦可直接阅读）：
 *   ::: 点睛
 *   - **公式**：…
 *   - **易错**：…
 *   - **技巧**：…
 *   - **注意**：…
 *   :::
 * 渲染为 <details class="fold tip-fold"> + 与真题页一致的 .q-tip-sec 四段块。 */
const TIP_SEC_META = [['公式', 'gs', '📌 公式'], ['易错', 'yc', '⚠️ 易错'],
['技巧', 'jq', '💡 技巧'], ['注意', 'zy', '🔍 注意']];

function renderTipsBlock(md) {
    const secs = new Map(), rest = [];
    let cur = null;
    for (const l of md.split('\n')) {
        const m = l.match(/^\s*[-*]\s*\*\*(公式|易错|技巧|注意)\*\*[：:]\s*([\s\S]*)$/);
        if (m) { cur = m[1]; secs.set(cur, [m[2]]); continue; }
        if (!l.trim()) continue;
        if (cur) secs.get(cur).push(l.trim()); else rest.push(l);
    }
    let inner = '';
    const tipsJson = {};
    for (const [key, cls, label] of TIP_SEC_META) {
        const arr = secs.get(key);
        if (!arr || !arr.join('').trim()) continue;
        const segMd = arr.join('\n');
        tipsJson[cls] = segMd;
        inner += `<div class="q-tip-sec tip-${cls}" data-copy-md="${copyMdAttr(segMd)}" data-copy-key="${cls}"><div class="q-tip-label">${label}</div>` +
            `<div class="q-tip-body">${mdToHtml(segMd)}</div></div>`;
    }
    if (!inner) inner = `<div class="q-tip-body">${mdToHtml(rest.join('\n'))}</div>`;
    return `<details class="fold tip-fold"><summary>📌 点睛</summary><div class="fold-body q-tips" data-copy-tips="${copyMdAttr(JSON.stringify(tipsJson))}">${inner}</div></details>`;
}

function mdToHtml(md) {
    md = balanceDollars(md);
    const lines = md.split('\n').map(l => l.replace(/<!--.*?-->/g, '').replace(/\s+$/, ''));
    const out = [];
    let chIdx = -1;
    let i = 0;
    while (i < lines.length) {
        const line = lines[i];
        if (!line.trim() || line.startsWith('# ')) { i++; continue; }
        if (line.startsWith('## ')) {
            chIdx++;
            out.push(`<h2 id="ch-${chIdx}">${inline(line.slice(3).trim())}</h2>`);
            i++;
        } else if (/^:::\s*fold\b/.test(line.trim())) {
            // 折叠块：::: fold 标题 … :::（答案/解析默认收起）
            const title = line.trim().replace(/^:::\s*fold\s*/, '') || '展开';
            out.push(`<details class="fold"><summary>${inline(title)}</summary><div class="fold-body">`);
            i++;
        } else if (/^:::\s*点睛/.test(line.trim())) {
            // 点睛块：::: 点睛 … :::（公式/易错/技巧/注意 四段，默认收起）
            const body = [];
            i++;
            while (i < lines.length && lines[i].trim() !== ':::') { body.push(lines[i]); i++; }
            i++;   // 跳过闭合 :::
            out.push(renderTipsBlock(body.join('\n')));
        } else if (line.trim() === ':::') {
            out.push('</div></details>');
            i++;
        } else if (/^!\[.*?\]\(.+?\)$/.test(line.trim())) {
            // 独行图片：![说明](路径) → figure + 图注
            const m = line.trim().match(/^!\[(.*?)\]\((.+?)\)$/);
            out.push(`<figure class="md-img"><img src="${esc(m[2])}" alt="${esc(m[1])}" loading="lazy">` +
                (m[1] ? `<figcaption>${esc(m[1])}</figcaption>` : '') + '</figure>');
            i++;
        } else if (/^\s*- /.test(line)) {
            const items = [];
            while (i < lines.length && /^\s*- /.test(lines[i])) {
                const m = lines[i].match(/^(\s*)- (.*)$/);
                items.push({ level: Math.floor(m[1].length / 2), text: m[2] });
                i++;
            }
            out.push(emitList(items, 0, 0)[0]);
        } else if (line.trim().startsWith('|')) {
            const rows = [];
            while (i < lines.length && lines[i].trim().startsWith('|')) {
                rows.push(splitRow(lines[i]));
                i++;
            }
            out.push(emitTable(rows));
        } else {
            out.push(`<p>${breakLines(line.trim())}</p>`);
            i++;
        }
    }
    return out.join('\n');
}

// ============ KaTeX ============
function renderMath(el) {
    if (typeof renderMathInElement !== 'function') return;  // vendor 缺失时降级为原文
    renderMathInElement(el, {
        delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
        ],
        throwOnError: false,
    });
}
