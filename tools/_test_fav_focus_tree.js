/* 左栏章节树端到端：抽取真实 renderTree() + applyFavFocus()，用真实 notes.json 渲染整棵树，
 * 断言「树重建 → 自动补刷标记」链路成立（DOM 单测用手造 DOM，未覆盖此路径）。 */
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
let notes = JSON.parse(fs.readFileSync(path.join(ROOT, 'pwa/data/notes.json'), 'utf-8'));
notes = notes.filter(n => !n.id.startsWith('21记'));   // 与 init() 一致：主站隐藏 21记
const SUBJECT_NAMES = { zy: '考前21记', gs: '高等数学', xd: '线性代数' };

const dom = new JSDOM('<!doctype html><html><body><div id="navTree"></div></body></html>', { url: 'http://localhost/' });
const { window } = dom;
window.localStorage.setItem('examFav', snap.data.examFav);
window.localStorage.setItem('examStatus', snap.data.examStatus);
window.localStorage.setItem('openGroups', '{}');

const code = [
    extract('esc'), extract('weakFavQids'), extract('computeFocusLevels'), extract('applyFavFocus'), extract('renderTree')
].join('\n');
const openFiles = {};
const run = new Function('favFocus', 'cur', 'document', 'localStorage', 'FOCUS_HOT_LABEL',
    'notes', 'SUBJECT_NAMES', 'openFiles', 'openGroups', '_treeBuilt',
    code + '; return { renderTree, applyFavFocus };'
)(favFocus, { id: '高数2-一元微分' }, window.document, window.localStorage, '⭐',
  notes, SUBJECT_NAMES, openFiles, JSON.parse('{}'), false);

// 首次渲染整棵树（tree-ch 默认隐藏，但 DOM 存在）
run.renderTree();
const tree = window.document.getElementById('navTree');
const totalCh = tree.querySelectorAll('.tree-ch').length;
ok(totalCh > 100, `整棵树应含大量章锚点（实际 ${totalCh}）`);

const hot = () => tree.querySelectorAll('.tree-ch.ff-hot');
const warm = () => tree.querySelectorAll('.tree-ch.ff-warm');
const first = hot().length;
ok(first > 0, `真实树应产生 ff-hot 标记（实际 ${first}）`);
ok(warm().length > 0, `真实树应产生 ff-warm 标记（实际 ${warm().length}）`);

// 每个 hot 章必须有 ⭐，且 ⭐ 是首节点
let starOK = true, crossOK = true;
const levels = new Function('favFocus', 'cur', 'document', 'localStorage', 'FOCUS_HOT_LABEL',
    [extract('weakFavQids'), extract('computeFocusLevels')].join('\n') + '; return computeFocusLevels;'
)(favFocus, { id: '高数2-一元微分' }, window.document, window.localStorage, '⭐');
const lv = levels();
hot().forEach(a => {
    if (!a.firstChild || a.firstChild.className !== 'ff-star') starOK = false;
    const key = a.dataset.note + '|' + a.dataset.ch;
    if (lv[key] !== 'hot') crossOK = false;   // 等级必须与该章 key 一致，不能串笔记
});
ok(starOK, '所有 hot 章的首节点应是 ⭐');
ok(crossOK, '所有 hot 章的等级应与自身 data-note|data-ch 对应（跨笔记不串）');

// 重建树（模拟 toggleFile 展开/收起）：标记不应丢失或叠加
openFiles['高数2-一元微分'] = true;
run.renderTree();
run.renderTree();
ok(hot().length === first, `重建后 hot 数应稳定（${first} → ${hot().length}）`);
let noDup = true;
hot().forEach(a => { if (a.querySelectorAll('.ff-star').length !== 1) noDup = false; });
ok(noDup, '重建后每个 hot 章应恰好 1 个 ⭐（不叠加）');

console.log(`左栏树端到端：${pass} 通过 / ${fail} 失败（hot=${hot().length} warm=${warm().length} 章锚点=${totalCh}）`);
process.exit(fail ? 1 : 0);
