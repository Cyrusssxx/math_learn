# math-note 项目长期记忆（2026-11-14 精简；细节见 11-13 / 11-14 日志）

## 0. 协作纪律
- 默认 commit + push 到 Cyrusssxx/math_learn，**只 stage 指定路径**；交付汇总含审计 / commit hash / `git ls-remote` 远程 HEAD / CACHE_VER / push 五项。
- 大改动先复述需求并指明信息缺失；修完一个错误主动扫同类；小数据改动手动优先；报错先查缓存/源数据；UI 问题真机复现。
- 全套 runner：`E:/workbuddy-data/binaries/node/workspace/_run_all.js`（12 项）。新增断言必须**反向验证**；变异测试用**新对象**（复用缓存对象会假通过）。

## 1. 构建与部署
- 新增数据文件必须加 `pwa/sw.js` 的 `PRECACHE`；pre-commit 自动跑 `build_assets_ver.py` + `build_sw.py` 并 `git add`。
- **hidden 铁律**：带 `hidden` 的元素 CSS 不能声明 `display`，需同级 `[hidden]{display:none}`。
- **jsdom 盲区**：外链 css 不加载（内联后再断言）；不实现 UA hidden；不解析 CSS 变量（改 `.matches(sel)` + CSS 源文本正则）；脚本必须 `process.exit()`；逐篇渲染 30+ 篇会卡死。
- CSS 变量白名单：`--bg --bg-side --bg-hover --bg-active --text --text-dim --text-faint --accent --strong --border --shadow --mk-* --hl-*`；**没有 `--bg-card`**。`_scan_hidden_conflict.js` 已不存在。

## 2. 数据资产（pwa/data/）
| 文件 | 内容 | 加载方 |
|---|---|---|
| `exam.json` | 数二真题 27 卷 607 题 | exam.js / category.js |
| `core_bank.json` | 核心题库 741 题 | category.js（core） |
| `dgy_items.json` / `xd_bank.json` / `bank_questions.json` | 大观园习题 1346 / 线代重点 333 / 大观园真题 827 | category.js |
| `ys27_items.json` | 27 模拟卷精选题 37 题（qid `ys27-N`，L0=50000） | category.js（不分 srcMode，始终并入） |
| `mn27_papers.json` | 27 精选十套卷（数二）10 套 220 题，`group='mock'`，qid `mn27-XX-N` | exam.js |
| `notes.json` / `exam_categories.json` | 讲义笔记 33 篇 / 三级分类树 129 节点 | notes.html·cards.html / — |

- `practice.json` 死数据。`exam.json` 紧凑单行；**`core_bank.json` = `json.dumps(d, indent=1, ensure_ascii=False)` 无尾换行**；`notes.json` = indent=2 无尾换行。⚠️ 单行紧凑 JSON 必须 `json.loads`→改 dict→`json.dumps`；禁止 inline `python -c` 改反斜杠/正则/JSON，必须写 .py 脚本 + 独立 .py 全量验证。
- 修复字段遍历 `q.keys()` 全覆盖（含 `tips` 的 gs/jq/yc/zy）。填空统一 `\underline{\hspace{2cm}}`；别误伤 `\int_0`。
- 校验套件：`_deep_validate.py` / `_audit_latex.py` / `_scan_unpaired.py` / `_audit_ys27.py` / `_audit_mn27.py` / `_mn27_check.py`；JS 回归 `_test_pp_counter.js`(51) / `_test_notes_hl.js`(182) / `_test_cat_search.js`(44)。
- qid = `<卷id>-<题号>`；`qidOf()` 经 `linkedQid` 重定向。⚠️ **双份数据不保证内容一致**，改一处要互核。四态：不会 > 不熟 > 已掌握 > 未刷。localStorage：`examFav`、`examStatus`、`examNote-<qid>`、`catSrcMode`、`catUnmarkedFirst`、`qDraw`、`qDrawBF`、`paperList`、`dailyMarks`、`ppViewPos`、`ppNote-<卷id>`、`examReview-<卷id>`、`examGroupOpen`、`examLastPos`。
- `bank_questions.categoryIds` 全是字符串，其余题库数字（渲染器 `String()` 兜过）。

## 3. 笔记页（index.html / reader.js）
- `chapters[i]` ↔ 正文第 i 个 `##` **必须镜像**，差异以 `##` 为准（改 `##` 会毁划词批注锚点）。目录两级（章 `ch-N` → 小节 `h3-N`），`tocItems()` 用文档顺序夹取判归属。
- ⚠️ **`##`/`###` 标题不得写 `$...$`**（目录取 textContent，KaTeX 双份副本 → 公式变长串）。护栏 `_verify_varlimit.py`。
- ⚠️ **给已有笔记加内容只能追加到 `md` 末尾**：`annotate.js` 的 `sid = 笔记id#块序号`，中间插入会让后面块偏移、高亮全错位。用「原 md 是新 md 严格前缀」断言 + 真实 `notesAnnot` 注入回归。
- `mdToHtml`：`##`/`###`/`####`｜`::: fold/nav/点睛`｜独行 `{#id}`｜独行 `![..](..)`→figure｜`>`｜`---`｜`-` 列表｜`|` 表格｜其余 `<p>`；`inline()` 支持 `**bold**`、`![img]`、`[text](#anchor)`、`` `code` ``、`⭐`。新增语法同时补 CSS。
- ⚠️ `reader.js` 与 `mdrender.js` 是两份副本，改渲染逻辑**必须同步**；链路 `emitList→breakLines→inline`。`emitList` 跳级缩进会丢整段列表；KaTeX auto-render 跨元素配对 `$`，输出前 `isBalanced()` + `stripLoneDollar()`。
- **高亮配色**：黄淡杏 `#ffe8b8`（`--mk-y`/`.ab-y`/`ANN_HLS[0]`；深色 `#6b5c33`），按 `y` 键。带高固定 46%、只用 alpha 调浓度（浅 .72~.74）；`--nhl-bg` 由 `annHlRgba(c,.72)` 提供，两处内联同步。⚠️ `.ann-text mark` 与 `mark.note-hl` 特异性相同且靠后会盖掉 `var(--nhl-bg)`，选择器必须写 `:not(.note-hl)`。`.katex.fml-hl-*` 要 `padding:2px 4px` + 圆角 6px；`text-decoration` 会传播进 inline 后代（用 `:has` 从父取消）。断言 `_test_notes_hl.js`（CSS 规则体提取正则要行首锚定）。
- **移动端目录（≤900px）**：`body.nav-open` + `::before` 遮罩（z25 < sidebar z26 < ☰ z30）；展开时 `.side-head` 用 `padding-top:60px`。收起统一 `closeMobileNav()`。`stripChNum()` 只剥显示编号，绝不动 `data-ch`/id。

## 4. 跨页副本（exam.js ↔ category.js）
`mdBlockWithImg` / `fillExamNoteImgs` / `zoomAnsImg` / `mdBlock` / `qCard`vs`catCard` / `.q-note` 双框 / `copyQLatex`vs`copyCatQLatex`。
- 答案/思路初始 hidden，**展开后补调 `renderMath` + `fillExamNoteImgs`**；`mdBlock` 裸 `$$` 坑：独占一行的 `$$` 要显式放行开块。
- ⚠️ **题卡 `mdBlock` 不支持 `- ` 列表**（每行一律 `<p>`，只认 `**加粗**`/`==高亮==`/`$$` 块/笔记令牌）；`- ` 只在笔记页 `emitList` 有效。答案分步用 `**① …**`。
- ⚠️ `copyCatQLatex` 必须走 `catFindByQid()`（拼卷/复测先 `ppOfQid`，分类页先 `allEntries`，再 `allEntriesAllSources` 兜底），只查 allEntries 会让 15% 的题静默失效。

## 5. 笔记编辑器（contenteditable）
- 编辑器 DOM 即数据载体；贴图后 blob 异步压缩，保存前 `await waitPendingImgs()`。
- ⚠️ 编辑态取不到 blob **绝不 `replaceWith` 文本**（会丢 `[图:id]` → 孤图清理删 blob → 图永久丢失），只标 `.img-fail`；仅只读态可替换「图片已丢失」。
- 三条保存路径：`saveNoteBtn` / `toggleNoteEdit` 完成分支 / `saveNoteFromOps`。富文本令牌 `[图:id]`、`<c:#hex>`、`<h:#hex>`、`<b>/<i>`、`<h1>/<h2>` 在 `editorToNote`/`noteToEditor`/`mdBlock` **三处都要识别**。H1/H2 用 `execCommand('formatBlock',false,'H1')` 且禁用 styleWithCSS。

## 6. 分类页 / 拼卷
- 双数据源 `#srcToggle`→`applySrcMode()`，存 `catSrcMode`（exam/core，默认 exam）；`buildEntries()` 按 `qid#catId` 去重；排序统一 `compareEntries()`。
- **新增独立大分类（ys27 模式）要改 category.js 7 处**：全局 `ysItems`、`buildEntries()` 末尾无条件 push（不受 srcMode 影响）、`ppScanPool()`、`allEntriesAllSources()`、`ppOfQid()` 的 `_ppIdx`、`catCard()` 的 `yearHtml`、`init()` 的 `Promise.all` fetch。收藏/标记/笔记/搜索/掌握地图/复测走 `qidOf()`+`allEntries` 自动覆盖；**`fav.html`/`analysis.js` 只读 exam.json**。新 L0 用 `ord=60000`。
- 分类页 URL 参数是 **`?cid=<分类id>`**（不是 `?cat=`）；`?review=1` 复测、`?paper=1` 拼卷。
- **分类搜索归一化**：`normFont`（全角→半角/清零宽）→ `searchTokens`（按空白切词，**AND**）→ `searchBlob`（LaTeX 去反斜杠、结构符当分隔、公式内容保留：`\sin x`→`sinx`）→ `entrySearchBlob`（挂 `e._sb`）。**改搜索词必须走 `setCatSearchKw()`**，三处赋值点漏一个就不同步。
- 「掌握地图」mastery.js/css 必须在 category.js **之后**引入；advice.js 两套口径，`advJump` 先切 core。跨库去重 `normStem()` 只去 LaTeX 结构符号 + bigram Jaccard；别放宽 source 正则（会误藏 563 道改写题）。
- **拼卷规则**：池 = `ppScanPool()` 三源；入池=已收藏且未掌握；`qDraw[qid].d>0` 永久排除；`doAt=max(dailyMarks 最后动过, 收藏时间)`；层级优先、层内按 `ageDays` 7 天分档；历史卷回填 `qDrawBF`。`ppNote-<卷id>` 备注⚠️不复用 `applyNoteFormat/noteInput`（会写 `examNote-undefined`）。**题号只把「不会」标红**：`ppNavStates()` 按 `.pp-item` DOM 顺序取实时 `statusGet()`，`ppRefreshNavMarks()` 只 toggle `mark-unk`。
- ⚠️ `pdfNo` 按章节编号 ≠ PDF 按 35 天计划编号；用户口径**只刷核心题库**。exam.json 已知缺陷：2003 数二第 11 题选项 D 应为 `$1>I_2>I_1$`。资料：线代答案册 `D:/cjx/下载/QQ FileRecv/线性代数_真题+重点题_答案册（含目录与页码）.pdf`；大观园源库 `assets/questions.json`（5952 题）。

## 7. 记忆卡（cards.html）
- `notes.json` 按 `##` 拆卡 → 超 `SOFT_LIMIT=440` 二次拆 → 行内 `$...$` 候选 ≥ `CLOZE_MIN=2` 为背诵卡（SRS）。⚠️ 拆卡必须 `stripCmt` 剥 HTML 注释；改 id 会让旧进度失配 → `legacyCardId` 迁移。
- `applyCloze` 按 `clozeScore` 取前 N（`DEF_CLOZE=3`/`MAX_CLOZE=6`），必须在 `renderMath` **之前**。读用 `peekOf(id)`（不写 ST.cards），写才 `stOf(id)`；卡片 id 绝不拼进内联 onclick。测试只用 `_test_cards_v4.js`（49 项），别锁死数据快照。

## 8. 历史教训
- HTML 引用死链 → 公式全不渲染。测试要按 HTML 真实 `<script src>` 顺序拼成**一个函数体**执行。「条件不足/待核」往往是题面抄错，先核真题原貌。
- `agent-browser`：守护进程随 Bash 会话结束 → `open`/`eval`/`screenshot` **同一次 Bash 调用**，输出重定向到文件；⚠️ **每次 `open` 是新 context，localStorage 不跨调用保留**，验「注入→跳转→断言」要写成 `open`→`eval`(setItem + `location.href=…`)→`sleep`→`eval`(断言) 一串；静态服务器 `run_in_background`，curl 加 `--noproxy '*'`；顶层 `let` 不在 window 上但 eval 可直接访问。
- PDF 转写：项目 venv 无 pymupdf，用 `D:\python\python.exe`；KaTeX 子集字体缺 ToUnicode 会让文字层公式破损 → 必须渲染 PNG 后看图转写。D 盘 Python 无 `/tmp`，用 `C:\Users\cjx\AppData\Local\Temp\`。

## 9. 真题页（exam.html / exam.js）
- 左栏 `#paperList`：`curPaper` + `qidOf(p.id,q.no)` 驱动收藏/标记/笔记/试卷点评（`examReview-<卷id>`）/做题模式/悬浮题号导航，`?paper=<id>&no=<题号>` 下钻。题卡题干容器是 **`.q-body`**（不是 `.q-stem`）。
- **两级分组**：`init()` 并行 fetch `exam.json` + `mn27_papers.json`（失败静默降级），`paperGroups()` 按 `p.group==='mock'` 分「数二真题」/「模拟卷」；`renderPaperList()` 两级渲染，`togglePaperGroup()` 折叠态存 `examGroupOpen`。显隐用 `.paper-group-body.collapsed` class，**不用 hidden 属性**。模拟卷不显示 `p.year`。
- `mn27_papers.json` **已全部完成：10 套 220 题**（题本 42 页 = 10 套×4 页×22 题）；草稿 `tools/mn27_ans/qXX_stem.md`+`qXX_ans.md`，构建 `_build_mn27.py`（`PAPERS`/`FIGS` 两表），审计 `_mn27_check.py`（草稿）+ `_audit_mn27.py`（产物，卷数按草稿份数动态算）。
- ⚠️ 该套资料：题本文字层公式破损必须渲染 PNG 看图转写；答案 **01/02 有文字层**（Unicode 数学字母 + 上下标压平 + 分式拆散行，**仍须以渲染图裁定公式**，如 01-Q1 分子是 $2x^{2n}-1$），**03–10 共 86 页零文字层**。多套并行用 subagent 最省时。⚠️ **题干与答案必须交叉核对**：曾出现题干把分子写成 $2^{2n}-1$（漏 x）而答案草稿正确；答案草稿【易错】易混入「任务示例/按图还原」等流程措辞，交付前要扫掉。
- `fav.html` / `analysis.js` 只读 `exam.json`，模拟卷收藏**不会**出现在收藏汇总与分析建议；拼卷池/分类树也不纳入（按套卷刷题定位）。
