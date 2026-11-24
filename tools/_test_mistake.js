/**
 * 易错本回归（2026-11-24）
 *  A. 静态接线：index.html 入口条/视图容器/工具条/脚本顺序、mistake.css 视图切换与 hidden 铁律
 *  B. 纯函数与数据：预设标签 15 个（剔除真题点睛/21记）、localStorage CRUD、筛选/排序/置顶/删除
 *  C. 隔离性：独立 localStorage key 与 IndexedDB 名，绝不碰 examNote/notesAnnot；备份/恢复/预缓存已接入
 *  D. 反向验证：改坏关键锚点必须失败（防测试本身失效）
 * 运行：node tools/_test_mistake.js
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('D:/ai code/408-quiz/node_modules/jsdom');
const ROOT = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(ROOT, p), 'utf8');

const HTML = read('pwa/index.html');
const JS = read('pwa/js/mistake.js');
const CSS = read('pwa/css/mistake.css');
const SW = read('pwa/sw.js');
const COMMON = read('pwa/js/common.js');

let pass = 0, fail = 0;
function ok(name, cond) { if (cond) pass++; else { fail++; console.log('  ✗ ' + name); } }
const has = (s, t) => s.indexOf(t) >= 0;

/* ---------- A. 静态接线 ---------- */
ok('入口条 id=mbEntry 且点击 toggle', /id="mbEntry"[^>]*onclick="Mistake\.toggle\(\)"/.test(HTML));
ok('入口条含计数 mbCount', has(HTML, 'id="mbCount"'));
ok('入口条在搜索框之后、目录树之前', HTML.indexOf('id="mbEntry"') > HTML.indexOf('searchResults') && HTML.indexOf('id="mbEntry"') < HTML.indexOf('id="navTree"'));
ok('视图容器 mbView 存在', has(HTML, 'id="mbView"'));
ok('正文与易错本互斥所需 #docPane 存在', has(HTML, 'id="docPane"'));
ok('列表/编辑两个子视图', has(HTML, 'id="mbListView"') && has(HTML, 'id="mbEditView"'));
ok('编辑子视图默认 hidden', /id="mbEditView" hidden/.test(HTML));
['mbTitle', 'mbTagsInput', 'mbEditor', 'mbKw', 'mbSort', 'mbHint'].forEach(id => ok('编辑/筛选控件 ' + id, has(HTML, 'id="' + id + '"')));
ok('编辑器 contenteditable', /id="mbEditor"[^>]*contenteditable="true"/.test(HTML));
ok('入口样式已引入', has(HTML, 'css/mistake.css'));
ok('mistake.js 在 reader.js 之后引入', HTML.indexOf('js/mistake.js') > HTML.indexOf('js/reader.js'));
ok('CSS 提供 body.mb-open 互斥切换', has(CSS, 'body.mb-open #docPane { display: none; }') && has(CSS, 'body.mb-open #mbView { display: block; }'));
ok('hidden 铁律：三个视图容器都有 [hidden]{display:none}', /#mbEditView\[hidden\], #mbListView\[hidden\], #mbView\[hidden\] \{ display: none; \}/.test(CSS));
ok('保留左栏右栏：mbView 沿用三栏 margin', has(CSS, 'margin-left: 280px') && has(CSS, 'margin-right: 240px'));
ok('响应式：≤900px 左边距归零', /@media \(max-width: 900px\)[\s\S]*#mbView \{ margin-left: 0/.test(CSS));
ok('新建按钮在 HTML，编辑按钮动态生成在 JS', has(HTML, 'Mistake.openEditor()') && has(JS, "Mistake.openEditor(\\'' + r.id"));
ok('JS 暴露 window.Mistake', has(JS, 'window.Mistake = {'));
ok('工具条有格式刷按钮', /id="mbFmtBrush"[^>]*onclick="Mistake\.toggleBrush\(\)"/.test(HTML));
ok('工具条有正文（仅取消标题）按钮', has(HTML, "Mistake.applyFmt('plainBlock')"));
ok('工具条有行内/块公式按钮', has(HTML, "Mistake.insertFormula('inline')") && has(HTML, "Mistake.insertFormula('block')"));
ok('格式刷取粗斜体/字色/高亮/H1·H2', ['function toggleBrush', 'function captureFormat', 'f.bold', 'f.italic', 'f.color', 'f.bg', "f.block = el.tagName"].every(t => has(JS, t)));
ok('格式刷套用 H1/H2 与 applyFmt 同源（styleWithCSS=false）', has(JS, "execFmt('formatBlock', f.block, false)"));
ok('粗斜体只叠加源已有的格式（保护目标加粗）', has(JS, "document.queryCommandState(cmd)") && has(JS, "if (f.bold) setToggle('bold', true)") && !has(JS, "setToggle('bold', !!f.bold)"));
ok('格式刷绝不调用 removeFormat', !has(JS, "execFmt('removeFormat'"));
ok('格式刷套用后保持激活（可连续刷）', has(JS, "// 注意：这里刻意不 clearBrush()，否则格式刷只能用一次"));
ok('Esc 可退出格式刷', has(JS, "e.key === 'Escape' && _brush"));
ok('高亮外显加强（字重+描边）', has(CSS, 'mark { padding: 1px 5px; border-radius: 3px; font-weight: 600; box-shadow: inset 0 0 0 1px rgba(0,0,0,.16); }'));
ok('正文按钮只 formatBlock P 不 removeFormat', /cmd === 'plainBlock'\) document\.execCommand\('formatBlock', false, 'P'\);[^\\n]*/.test(JS) && !/cmd === 'plainBlock'\)[^\\n]*removeFormat/.test(JS));
ok('标题内部行内格式不再被丢弃', has(JS, 'run(ch, nc0, nh0, nb0, ni0)'));
ok('格式刷高亮态样式存在', has(CSS, '.mb-toolbar button.on'));
ok('图片点击不再新开标签页，改走放大遮罩', !has(JS, 'window.open(img.src') && has(JS, 'window.openLightbox') && has(JS, 'function bindZoom'));
ok('编辑态下方有实时预览容器', has(HTML, 'id="mbPreview"') && has(JS, 'function renderPreview') && has(JS, 'function schedulePreview'));
ok('清高亮按钮与透明高亮命令存在', has(HTML, "Mistake.applyFmt('clearHl')") && has(JS, "cmd === 'clearHl'") && has(JS, "'hiliteColor', false, 'transparent'"));
ok('新增纯红字色', has(HTML, "background:#ff0000") && has(HTML, "foreColor','#ff0000'"));
ok('预览容器样式已定义', has(CSS, '.mb-preview {'));
ok('编辑器高亮不用 mark（避免默认黄底清不掉）', /node = document\.createElement\('span'\); node\.style\.backgroundColor = mf\[2\]/.test(JS) && !has(JS, "createElement('mark')"));

/* ---------- B. jsdom 真实 DOM 行为 ---------- */
const dom = new JSDOM(HTML.replace(/<script[\s\S]*?<\/script>/g, ''), {
    url: 'https://example.test/index.html', pretendToBeVisual: true
});
const { window } = dom;
const { document } = window;
global.window = window;
global.document = document;
global.localStorage = window.localStorage;
global.getSelection = () => ({ rangeCount: 0, isCollapsed: true, anchorNode: null, removeAllRanges() { }, addRange() { } });
global.indexedDB = { open() { return { set onsuccess(v) { }, set onerror(v) { }, set onupgradeneeded(v) { } }; } };
global.alert = () => { };
global.confirm = () => true;
global.Image = window.Image;
global.FileReader = window.FileReader;
global.URL = window.URL;
window.crypto = { randomUUID: () => 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => (Math.random() * 16 | 0).toString(16)) };
window.scrollTo = () => { };
window.renderMathInElement = () => { };
window.katex = {};

// 载入模块（IIFE 自动 init）
new Function('window', 'document', 'localStorage', 'indexedDB', 'getSelection', 'alert', 'confirm', 'Image', 'FileReader', 'URL', JS)(
    window, document, window.localStorage, global.indexedDB, global.getSelection, global.alert, global.confirm, global.Image, global.FileReader, global.URL
);
const M = window.Mistake;
document.dispatchEvent(new window.Event('DOMContentLoaded')); // jsdom 不自动派发，确保 init 执行

ok('Mistake API 齐全', M && ['toggle', 'open', 'close', 'openEditor', 'saveEditor', 'del', 'pin', 'unpin', 'setTag', 'setKw', 'setSort'].every(k => typeof M[k] === 'function'));

// 预设标签
ok('预设标签 15 个', M.PRESET_TAGS.length === 15);
ok('含高数1-极限与线代4-线性方程组', M.PRESET_TAGS.includes('高数1-极限') && M.PRESET_TAGS.includes('线代4-线性方程组'));
ok('不含真题点睛', !M.PRESET_TAGS.some(t => t.indexOf('真题点睛') >= 0));
ok('不含考前21记', !M.PRESET_TAGS.some(t => t.indexOf('21记') >= 0));

// 起步空态
ok('初始空列表', document.getElementById('mbTotal').textContent === '0');
ok('空态提示文案', has(document.getElementById('mbList').textContent, '还没有易错笔记'));

// 新建并保存（预设走 chips 点选，自定义走输入框）
ok('编辑态有预设 chips 容器', !!document.getElementById('mbPresetTags'));
ok('预设栏默认折叠', /_editTagFold = true/.test(JS) && has(document.getElementById('mbPresetTags').innerHTML, '展开全部'));
ok('预设 chips 默认只显示 5 个', (document.getElementById('mbPresetTags').querySelectorAll('.mb-chip').length) === 5);
M.openEditor();
document.getElementById('mbTitle').value = '洛必达用错';
document.getElementById('mbTagsInput').value = '易错';
M.togglePresetTag('高数1-极限'); // 点选预设章节
ok('点选预设后 chip 高亮', has(document.getElementById('mbPresetTags').innerHTML, 'mb-chip on'));
document.getElementById('mbEditor').innerHTML = '先提公因式 <b>再求导</b> $x^2$';
const saveP = M.saveEditor();
saveP.then(() => {
    const all = JSON.parse(localStorage.getItem('mistakeNotes'));
    ok('保存后 1 条', all.length === 1);
    ok('标题正确', all[0].title === '洛必达用错');
    ok('标签拆分正确', JSON.stringify(all[0].tags) === JSON.stringify(['高数1-极限', '易错']));
    ok('正文保留 b 令牌', has(all[0].body, '<b>再求导</b>'));
    ok('正文保留公式', has(all[0].body, '$x^2$'));
    ok('有 created/updated', all[0].created > 0 && all[0].updated > 0);
    ok('列表计数刷新', document.getElementById('mbTotal').textContent === '1');
    ok('卡片标题渲染', has(document.getElementById('mbList').textContent, '洛必达用错'));
    ok('卡片摘要保留公式定界符（可渲染）', has(document.getElementById('mbList').innerHTML, '$x^2$'));
    ok('标签 chip 出现在筛选栏', has(document.getElementById('mbTags').textContent, '高数1-极限'));
    ok('自定义标签也出现在筛选栏', has(document.getElementById('mbTags').textContent, '易错'));
    ok('未使用的预设标签不出现在筛选栏', !has(document.getElementById('mbTags').textContent, '高数6-二重积分'));
    ok('卡片正文完整渲染 b 令牌（非纯文本）', has(document.getElementById('mbList').innerHTML, '<b>再求导</b>'));
    ok('标签少时不显示折叠按钮', !has(document.getElementById('mbTags').textContent, '展开') && !has(document.getElementById('mbTags').textContent, '收起'));

    // 置顶 / 取消置顶
    M.pin(all[0].id);
    ok('置顶生效', JSON.parse(localStorage.getItem('mistakeNotes'))[0].pinned === true);
    M.unpin(all[0].id);
    ok('取消置顶生效', JSON.parse(localStorage.getItem('mistakeNotes'))[0].pinned === false);

    // 编辑已有
    M.openEditor(all[0].id);
    ok('编辑态回填标题', document.getElementById('mbTitle').value === '洛必达用错');
    document.getElementById('mbTitle').value = '改过的标题';
    return M.saveEditor().then(() => {
        ok('编辑保存不新增条数', JSON.parse(localStorage.getItem('mistakeNotes')).length === 1);
        ok('编辑标题生效', JSON.parse(localStorage.getItem('mistakeNotes'))[0].title === '改过的标题');

        // 筛选栏折叠：第二条用了第 6 个以后的预设标签，默认折叠时应隐藏
        M.openEditor();
        document.getElementById('mbTitle').value = '二重积分换序';
        document.getElementById('mbTagsInput').value = '高数6-二重积分'; // 自定义填法仍兼容（保存时归一）
        document.getElementById('mbEditor').textContent = '画积分域';
        return M.saveEditor().then(() => {
            ok('两条', JSON.parse(localStorage.getItem('mistakeNotes')).length === 2);
            ok('自定义输入的章节名归一为预设', JSON.parse(localStorage.getItem('mistakeNotes'))[0].tags.indexOf('高数6-二重积分') >= 0);
            // 折叠态：用的标签 = 高数1/6 + 易错 → 前 5 个预设内，未超限；放一条第 15 个标签验证折叠
            M.togglePresetFold();
            ok('预设栏可展开全部 15 个', document.getElementById('mbPresetTags').querySelectorAll('.mb-chip').length >= 15);
            M.togglePresetFold();
            ok('预设栏可收回 5 个', document.getElementById('mbPresetTags').querySelectorAll('.mb-chip').length === 5);
            M.setTag('高数1-极限');
            ok('标签筛选命中 1 条', document.getElementById('mbTotal').textContent === '1');
            M.setTag('高数1-极限'); // 再点取消
            ok('再点标签取消筛选', document.getElementById('mbTotal').textContent === '2');
            M.setKw('换序');
            ok('关键词搜索命中 1 条', document.getElementById('mbTotal').textContent === '1');
            M.setKw('');
            ok('清空搜索恢复 2 条', document.getElementById('mbTotal').textContent === '2');

            // 视图切换与持久化
            ok('默认非易错本视图', !document.body.classList.contains('mb-open'));
            M.open();
            ok('open 加 mb-open', document.body.classList.contains('mb-open'));
            ok('视图状态已持久化', localStorage.getItem('mistakeView') === '1');
            M.close();
            ok('close 移除 mb-open', !document.body.classList.contains('mb-open'));
            ok('视图状态写回 0', localStorage.getItem('mistakeView') === '0');

            // 删除
            const id2 = JSON.parse(localStorage.getItem('mistakeNotes'))[0].id;
            M.del(id2);
            ok('删除后 1 条', JSON.parse(localStorage.getItem('mistakeNotes')).length === 1);

            /* ---------- B2. 格式刷 / 正文 / 公式骨架 / 标题内联 ---------- */
            const fmtCalls = [];
            document.execCommand = (cmd, ui, val) => { fmtCalls.push([cmd, val]); return true; };
            function selText(node, from, to) {
                const r = document.createRange(); r.setStart(node, from); r.setEnd(node, to);
                const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
            }
            M.openEditor();
            const ed2 = document.getElementById('mbEditor');
            // 从存储加载 <h:...> 时必须用 span+background-color，不能生成默认黄底的 <mark>
            localStorage.setItem('mistakeNotes', JSON.stringify([{ id: 'mbhl', title: '高亮', tags: [], body: '<h:#ffe8b8>高亮</h>', created: 1, updated: 1, pinned: false }]));
            M.openEditor('mbhl');
            ok('加载高亮使用 span 而非 mark', !ed2.querySelector('mark') && !!ed2.querySelector('span[style*="background-color"]'));
            M.openEditor();
            ed2.innerHTML = '<h1><b style="color:#c0392b;background-color:#ffe8b8">源</b>文字</h1>';
            selText(ed2.querySelector('b').firstChild, 0, 1);
            fmtCalls.length = 0;
            M.toggleBrush();
            ok('格式刷取到完整格式提示', has(document.getElementById('mbHint').textContent, '大标题 · 加粗 · 字色 #c0392b · 高亮 #ffe8b8'));
            ok('格式刷按钮亮起', document.getElementById('mbFmtBrush').classList.contains('on'));

            ed2.innerHTML = '<h2>目标</h2>';
            selText(ed2.querySelector('h2').firstChild, 0, 2);
            fmtCalls.length = 0;
            M.toggleBrush();
            const brushNames = fmtCalls.map(x => x[0]);
            ok('格式刷不清目标旧格式（加粗不会被抹）', !brushNames.includes('removeFormat'));
            ok('格式刷套用源标题 H1（同源 formatBlock）', fmtCalls.some(x => x[0] === 'formatBlock' && x[1] === 'H1'));
            ok('格式刷套用加粗', brushNames.includes('bold'));
            ok('格式刷套用字色', fmtCalls.some(x => x[0] === 'foreColor' && x[1] === '#c0392b'));
            ok('格式刷套用高亮', fmtCalls.some(x => x[0] === 'hiliteColor' && x[1] === '#ffe8b8'));
            ok('格式刷套用后仍亮着（可连续刷）', document.getElementById('mbFmtBrush').classList.contains('on'));

            ed2.innerHTML = '<h2><b>标题</b></h2>';
            selText(ed2.querySelector('h2 b').firstChild, 0, 2);
            fmtCalls.length = 0;
            M.applyFmt('plainBlock');
            const plainNames = fmtCalls.map(x => x[0]);
            ok('正文按钮只回 P', fmtCalls.some(x => x[0] === 'formatBlock' && x[1] === 'P'));
            ok('正文按钮不清掉粗体/字色/高亮', !plainNames.includes('removeFormat'));

            ed2.innerHTML = '前置';
            selText(ed2.firstChild, 2, 2);
            M.insertFormula('inline');
            ok('行内公式骨架插入', has(ed2.innerHTML, '$\u200B$'));
            ed2.innerHTML = '前置';
            selText(ed2.firstChild, 2, 2);
            M.insertFormula('block');
            ok('块公式骨架插入', has(ed2.innerHTML, '$$'));

            ed2.innerHTML = '<p><span style="color:#c0392b;background-color:#ffe8b8">字色高亮</span></p>';
            selText(ed2.querySelector('span').firstChild, 0, 4);
            fmtCalls.length = 0;
            M.applyFmt('clearHl');
            ok('清高亮只发透明高亮命令，不碰字色', fmtCalls.some(x => x[0] === 'hiliteColor' && x[1] === 'transparent') && !fmtCalls.some(x => x[0] === 'removeFormat'));

            // H1/H2：光标未选字时点字色，自动作用整段标题
            ed2.innerHTML = '<h1>标题</h1>';
            selText(ed2.querySelector('h1').firstChild, 1, 1);
            fmtCalls.length = 0;
            M.applyFmt('foreColor', '#ff0000');
            ok('光标在 H1 内未选字也能改整段字色', fmtCalls.some(x => x[0] === 'foreColor' && x[1] === '#ff0000'));

            // H1 自带粗体：点 B 不能反向关掉
            ed2.innerHTML = '<h1>标题</h1>';
            selText(ed2.querySelector('h1').firstChild, 1, 1);
            fmtCalls.length = 0;
            M.applyFmt('bold');
            ok('H1 点 B 不会把自带粗体关掉', !fmtCalls.some(x => x[0] === 'bold') && has(document.getElementById('mbHint').textContent, '标题本身已加粗'));

            // 上一轮套用后刷子仍开着，先折叠光标退出，再测取格式
            selText(ed2.querySelector('h1').firstChild, 0, 0); M.toggleBrush();
            ok('连续刷中途可退出', !document.getElementById('mbFmtBrush').classList.contains('on'));

            // 选区锚点是元素节点（三击/全选）时也能取到标题内部完整格式
            ed2.innerHTML = '<h1><b><span style="color:#c0392b"><i>源</i></span></b></h1>';
            const hr = document.createRange(); hr.setStart(ed2.querySelector('h1'), 0); hr.setEnd(ed2.querySelector('h1'), 1);
            var hs = window.getSelection(); hs.removeAllRanges(); hs.addRange(hr);
            M.toggleBrush();
            const takeEl = document.getElementById('mbHint').textContent;
            ok('元素锚点也能取到标题内完整格式', ['大标题', '加粗', '斜体', '字色 #c0392b'].every(t => has(takeEl, t)), takeEl);
            // 折叠光标后再点🖌 = 退出格式刷
            ed2.innerHTML = '<p>清刷</p>'; selText(ed2.querySelector('p').firstChild, 0, 0); M.toggleBrush();
            ok('折叠选区点🖌退出格式刷', !document.getElementById('mbFmtBrush').classList.contains('on'));

            // 取格式后，用鼠标选中目标自动套用（Word 手感）
            ed2.innerHTML = '<p><b style="background-color:#ffe8b8">源</b></p>'; selText(ed2.querySelector('p b').firstChild, 0, 1); M.toggleBrush();
            ed2.innerHTML = '<p>目标</p>'; selText(ed2.querySelector('p').firstChild, 0, 2);
            fmtCalls.length = 0;
            ed2.dispatchEvent(new window.MouseEvent('mouseup', { bubbles: true }));
            return new Promise(r => setTimeout(r, 40)).then(() => {
                ok('鼠标选中目标后自动套用格式', !fmtCalls.some(x => x[0] === 'removeFormat') && fmtCalls.some(x => x[0] === 'hiliteColor') && document.getElementById('mbFmtBrush').classList.contains('on'));
                // 连续刷：不重新取格式，直接选第二段，仍应自动套用
                ed2.innerHTML = '<p>第二段</p>'; selText(ed2.querySelector('p').firstChild, 0, 3);
                fmtCalls.length = 0;
                ed2.dispatchEvent(new window.MouseEvent('mouseup', { bubbles: true }));
                return new Promise(r => setTimeout(r, 40));
            }).then(() => {
                ok('格式刷可连续套用第二段（不用重新取格式）', fmtCalls.some(x => x[0] === 'hiliteColor' && x[1] === '#ffe8b8') && document.getElementById('mbFmtBrush').classList.contains('on'));

                ed2.innerHTML = '预览 <b>粗体</b> $x^2$';
                ed2.dispatchEvent(new window.Event('input', { bubbles: true }));
                return new Promise(r => setTimeout(r, 320));
            }).then(() => {
                ok('编辑态实时预览渲染粗体', has(document.getElementById('mbPreview').innerHTML, '<b>粗体</b>'));
                ed2.innerHTML = '<h1><b>重点</b><span style="color:#c0392b">红</span><i>斜</i></h1>';
                return M.saveEditor();
            }).then(() => {
                const recs = JSON.parse(localStorage.getItem('mistakeNotes'));
                ok('标题内部加粗/字色/斜体都写回 token', has(recs[0].body, '<h1><b>重点</b><c:#c0392b>红</c><i>斜</i></h1>'));

                /* ---------- C. 隔离性 ---------- */
                ok('独立 localStorage key', has(JS, "var LS = 'mistakeNotes'"));
                ok('独立 IndexedDB 名', has(JS, "var IDB_NAME = 'mistakeNoteImg'"));
                ok('不写 examNote-', !/localStorage\.setItem\(\s*['"]examNote-/.test(JS));
                ok('不写 notesAnnot', !/localStorage\.setItem\(\s*['"]notesAnnot['"]/.test(JS));
                ok('备份摘要含易错笔记', has(COMMON, "'易错笔记': cntArr('mistakeNotes')"));
                ok('备份导出含 mistakeNoteImg', has(COMMON, "idb['mistakeNoteImg'] = await Promise.race"));
                ok('导入恢复含 mistakeNoteImg', has(COMMON, "idbRestore('mistakeNoteImg', 'imgs'"));
                ok('SW 预缓存 CSS', has(SW, "'css/mistake.css'"));
                ok('SW 预缓存 JS', has(SW, "'js/mistake.js'"));

                /* ---------- D. 反向验证：锚点被改坏必须失败 ---------- */
                ok('[反向] 入口条 onclick 不能是空', !/id="mbEntry"[^>]*onclick="\s*"/.test(HTML));
                ok('[反向] 预设标签不能含数三', !M.PRESET_TAGS.some(t => t.indexOf('数三') >= 0));
                ok('[反向] 不能复用做题笔记的 DB 名', !has(JS, "'examNoteImg'"));
                ok('[反向] 不能复用批注的 DB 名', !has(JS, "'notesAnnotImg'"));

                console.log('\n易错本回归：' + pass + ' 通过 / ' + fail + ' 失败');
                process.exit(fail ? 1 : 0);
            });
        });
    });
}).catch(e => { console.error(e); process.exit(1); });
