// CoreExtra 逻辑单测（localStorage 打桩，无需浏览器）
const fs = require('fs');
const store = {};
global.localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; },
};
global.window = global;
// 载入模块
const code = fs.readFileSync('pwa/js/core-extra.js', 'utf8');
new Function(code)();
const CE = global.CoreExtra;
const nodes = JSON.parse(fs.readFileSync('pwa/data/cat_deep.json', 'utf8')).nodes;
const catDeep = { nodes };

let pass = 0, fail = 0;
function t(name, cond, extra) {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? ' → ' + extra : '')); }
}

console.log('【1】add / 去重');
const q1 = { no: 5, stem: '设 $A$ 为三阶矩阵，求 $|A|$', answer: '答案A', deepCats: ['51'], source: '2020数一', type: 'calc' };
const r1 = CE.add(q1, { paperId: 'exam', srcNo: 5 });
t('首次添加成功', r1.ok && r1.no === 9001, JSON.stringify(r1));
const r2 = CE.add(q1, { paperId: 'exam', srcNo: 5 });
t('同题重复添加被拒', !r2.ok, JSON.stringify(r2));
t('列表长度 1', CE.list().length === 1);
t('has() 命中', CE.has(q1));

console.log('【2】mergeInto 章节归属');
const corePapers = [{ id: 'core', sections: [
  { title: '行列式', questions: [] }, { title: '矩阵', questions: [] },
  { title: '二次型', questions: [] },
] }];
const n = CE.mergeInto(corePapers, catDeep);
t('并入 1 题', n === 1, 'n=' + n);
const sec = corePapers[0].sections.find(s => s.questions.length);
t('落到「二次型」节（deepCats 51 在 二次型/正定 下）', sec && sec.title === '二次型', sec && sec.title);
const n2 = CE.mergeInto(corePapers, catDeep);
t('二次 merge 幂等（不重复并入）', n2 === 0, 'n2=' + n2);

console.log('【3】导出 / 导入');
const json = CE.exportJson();
t('导出含 1 条', JSON.parse(json).items.length === 1);
const added = CE.importJson(json);
t('导入同内容不新增', added === 0, 'added=' + added);
const q2 = { no: 9, stem: '另一道题', deepCats: ['21'], source: '2021数二' };
CE.add(q2, { paperId: 'exam', srcNo: 9 });
const json2 = CE.exportJson();
CE.clear();
t('清空后为 0', CE.list().length === 0);
const a2 = CE.importJson(json2);
t('导入 2 条', a2 === 2, 'a2=' + a2);

console.log('【4】编号递增');
const q3 = { stem: '第三题', deepCats: ['9'], source: 'X' };
const r3 = CE.add(q3, {});
t('新题号 > 9002', r3.ok && r3.no > 9002, 'no=' + r3.no);

console.log(`\n结果：通过 ${pass}，失败 ${fail}`);
process.exit(fail ? 1 : 0);
