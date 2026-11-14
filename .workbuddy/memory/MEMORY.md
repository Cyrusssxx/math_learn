# math-note 项目长期记忆（2026-11-14 精简重组；过程细节见每日日志）

## 0. 协作纪律
- 提交默认 commit + push 到 Cyrusssxx/math_learn，**只 stage 指定路径**；交付汇总含审计结果 / commit hash / `git ls-remote` 远程 HEAD / CACHE_VER / push 确认五项。
- 大改动先复述需求并指明信息缺失；修完一个错误主动扫同类（真题卷优先）；小数据改动手动优先、不写脚本；报错先查缓存/源数据再判 bug；UI 问题要真机复现。
- 全套 runner：`E:/workbuddy-data/binaries/node/workspace/_run_all.js`（12 项）。
- 新增断言必须**反向验证**（变异后断言必须失败）；变异测试要用**新对象**，复用带缓存的对象会假通过。

## 1. 构建与部署
- 新增数据文件必须加 `pwa/sw.js` 的 `PRECACHE`；pre-commit（`.githooks/pre-commit`）自动跑 `build_assets_ver.py`（html `?v=`）+ `build_sw.py`（CACHE_VER）并 `git add`；`common.js` 自动重载提示。
- **hidden 铁律**：带 `hidden` 的元素 CSS 不能声明 `display`（作者样式压过 UA），需同级 `[hidden]{display:none}`；排查 `_scan_hidden_conflict.js`。
- **jsdom 盲区**：外链 css 不加载（内联后再断言）；不实现 UA hidden；不解析 CSS 变量（改 `.matches(sel)` + CSS 源文本正则）；脚本必须 `process.exit()`；逐篇渲染 30+ 篇会卡死（抽函数配假数据）。
- CSS 变量白名单：`--bg --bg-side --bg-hover --bg-active --text --text-dim --text-faint --accent --strong --border --shadow --mk-* --hl-*`；**没有 `--bg-card`**。跨页共用组件样式要在每个 css 都写。

## 2. 数据资产（pwa/data/）
| 文件 | 内容 | 加载方 |
|---|---|---|
| `exam.json` | 数二真题 27 卷 607 题 | exam.js / category.js |
| `core_bank.json` | 核心题库 741 题 | category.js（core） |
| `dgy_items.json` / `xd_bank.json` / `bank_questions.json` | 大观园习题 1346 / 线代重点 333 / 大观园真题 827 | category.js |
| `ys27_items.json` | 27 模拟卷精选题 37 题（qid `ys27-N`，L0 = 50000） | category.js（**不分 srcMode，始终并入**） |
| `notes.json` | 讲义笔记 33 篇 | notes.html / cards.html |
| `exam_categories.json` | 三级分类树（键为 id 字符串，129 节点） | — |

- `practice.json` 是死数据。格式：`exam.json` 紧凑单行 `separators=(',',':')`；`exam_categories.json`/`bank_questions.json` pretty；**`core_bank.json` = `json.dumps(d, indent=1, ensure_ascii=False)` 无尾换行**（`JSON.stringify` 压平会造 4 万行假 diff）；`notes.json` = `indent=2` 无尾换行。
- ⚠️ 单行紧凑 JSON 必须 `json.loads`→改 dict→`json.dumps`；禁止 inline `python -c` 改反斜杠/正则/JSON，必须写 .py 脚本 + 独立 .py 全量验证。`r"\\X"`=单反斜杠，双反斜杠要 `r"\\\\X"`。
- 修复字段遍历 `q.keys()` 全覆盖（含 `tips` 的 gs/jq/yc/zy）。LaTeX 填空统一 `\underline{\hspace{2cm}}`；别误伤 `\int_0`/`|a_n|`（只匹配连续 3+ `\_`）。
- 验证四件套：`_deep_validate.py` / `_audit_latex.py` / `_scan_unpaired.py` / `_audit_ys27.py`；数据改动后全跑 + commit（bump CACHE_VER）+ push 闭环。
- qid = `<卷id>-<题号>`；`qidOf()` 经 `linkedQid`（`xd-N`/`core-N`→真题 qid）重定向统一收藏/笔记键。⚠️ **双份数据不保证内容一致**（2023 数二第 5 题曾一处对一处错），改一处要互核。
- 四态：不会 > 不熟 > 已掌握 > 未刷。localStorage：`examFav {qid:{t:ms}}`、`examStatus`、`examNote-<qid>`、`catSrcMode`、`catUnmarkedFirst`、`qDraw`、`qDrawBF`、`paperList`、`dailyMarks`、`ppViewPos`、`ppNote-<卷id>`、`examReview-<卷id>`。
- `bank_questions.categoryIds` 全是字符串，其余题库数字（渲染器 `String()` 兜过）。

## 3. 笔记页（index.html / reader.js）
- 结构 `{id,subject,order,name,title,chapters[],md}`；**`chapters[i]` ↔ 正文第 i 个 `##` 必须镜像，差异一律以 `##` 为准改 chapters**（改 `##` 会毁划词批注锚点）。体检 `_audit_notes_layout.py`，对齐 `_fix_notes_toc.py --apply`。
- 右侧目录两级（章 `ch-N` → `###` 小节 `h3-N`）；`tocItems()` 用**文档顺序夹取**判归属；小节默认收起、只展开当前章；`savePos/restorePos` 连小节记。
- ⚠️ **`##`/`###` 标题不得写 `$...$`**：目录取渲染后 h3 的 `textContent`，KaTeX 有 mathml + aria-hidden 两份副本 → 公式在目录里变长串。护栏 `tools/_verify_varlimit.py`。
- ⚠️ **给已有笔记加内容只能追加到 `md` 末尾**：`annotate.js` 的 `sid = 笔记id#块序号`（`##`/`###` 不计入，只有 `li`/`p` 分配），中间插入会让后面所有块偏移、已有高亮全错位。改用末尾追加 + 「原 md 是新 md 严格前缀」断言 + 真实 `notesAnnot` 注入回归。
- `stripChNum()` 只剥章标题显示编号，绝不动 `data-ch`/id。章间距用 `padding-top`（`.toc-item + .toc-item`），`.toc-gap-lg` 标已读→未读分界。
- `mdToHtml` 语法：`#`跳过｜`##`/`###`/`####`｜`::: fold/nav/点睛`｜独行 `{#id}`｜独行 `![..](..)`→figure｜`>` 引用｜`---`/`***`/`___`｜`-` 列表｜`|` 表格｜其余 `<p>`；`inline()` 支持 `**bold**`、`![img]`、`[text](#anchor)`、`` `code` ``、`⭐`。⚠️ 新增语法同时补 CSS。
- ⚠️ `reader.js` 与 `mdrender.js` 是两份副本，改渲染逻辑**必须同步**；链路 `emitList→breakLines→inline`。`emitList` 跳级缩进会丢整段列表；`renderTipsBlock` 四段标签之外的行必须追加渲染；KaTeX auto-render 跨元素配对 `$`，输出前 `isBalanced()` + `stripLoneDollar()`。
- **高亮配色（11-13 定档）**：黄色淡杏 `#ffe8b8`（`--mk-y`、`.ab-y`、`ANN_HLS[0]`；深色 `#6b5c33`），按 `y` 键存储。⚠️ **带高固定 46%，只用 alpha 一个维度调浓度**（浅 .72~.74 / 深 .74~.76）；`--nhl-bg` 由 `annHlRgba(c,.72)` 提供，`annSoftenHl`/令牌渲染两处内联同步。⚠️ `.ann-text mark` 与 `mark.note-hl` 特异性相同且靠后，会盖掉 `var(--nhl-bg)` → 选择器必须写 `:not(.note-hl)`。`--hl-*-soft` .21~.22（深 .13~.15）专供公式整块底，`.katex.fml-hl-*` 必须有 `padding:2px 4px` + 圆角 6px。`text-decoration` 会传播进 inline 后代（含 KaTeX，用 `:has` 从父取消）。断言 `tools/_test_notes_hl.js`（182 项，alpha∈[.65,.85) 双向窗口 + 带高锁死 46% + 变异反向验证；CSS 规则体提取正则要**行首锚定**）。
- **移动端目录（≤900px）**：`body.nav-open` + `::before` 遮罩（z25 < sidebar z26 < ☰ z30）；展开时 `.side-head` 用 `padding-top:60px` 整行下移。收起统一走 `closeMobileNav()`；document click 监听要放行 `.menu-btn` 与 sidebar 内部。

## 4. 跨页副本（exam.js ↔ category.js）
`mdBlockWithImg` / `fillExamNoteImgs` / `zoomAnsImg` / `mdBlock` / `qCard`vs`catCard` / `.q-note` 双框 / `copyTextToClipboard` / `copyQLatex`vs`copyCatQLatex`。
- 答案/思路初始 hidden，**展开后补调 `renderMath` + `fillExamNoteImgs`**。
- `mdBlock` 裸 `$$` 坑：独占一行的 `$$` 要显式放行开块（`(!l.endsWith('$$') || l === '$$')`）。
- `.q-note` 只有 `/\[图:[a-z0-9]+\]/` 命中才加 `.has-img`；纯文字靠 `:not(.has-img) .q-note-preview` 去框。
- ⚠️ **题卡 `mdBlock` 不支持 `- ` 列表**（category.js / exam.js / exam-shared.js 是副本：每行一律包 `<p>`，只认 `**加粗**` / `==高亮==` / `$$` 块 / 笔记令牌）；`- ` 列表只在笔记页 `emitList` 有效。答案里分情况讨论用 `**① …**`。
- ⚠️ **拼卷/复测复制按钮**：`copyCatQLatex` 必须走 `catFindByQid()`（拼卷/复测先 `ppOfQid`，分类页先 `allEntries`，再 `allEntriesAllSources` 兜底）——只查 allEntries 会让 15% 的题**静默失效**。

## 5. 笔记编辑器（contenteditable）
- 编辑器 DOM 即数据载体；贴图后 blob 异步压缩，保存前 `await waitPendingImgs()`。
- 编辑态取不到 blob **绝不 `replaceWith` 文本**（会丢 `[图:id]`→孤图清理删 blob→图永久丢失），只标 `.img-fail`；仅只读态可替换「图片已丢失」。
- 三条保存路径：`saveNoteBtn` / `toggleNoteEdit` 完成分支 / `saveNoteFromOps`。
- 富文本令牌（`mdInline` 先 `esc()` 再白名单还原）：`[图:id]`、`<c:#hex>`、`<h:#hex>`、`<b>/<i>`、`<h1>/<h2>`；`editorToNote`/`noteToEditor`/`mdBlock` **三处都要识别全令牌**。H1/H2 用 `execCommand('formatBlock',false,'H1')` 且禁用 styleWithCSS。

## 6. 分类页 / 拼卷
- 双数据源 `#srcToggle`→`applySrcMode()`，存 `catSrcMode`（exam/core，默认 exam）；`buildEntries()` 按 `qid#catId` 去重；「无标记优先」存 `catUnmarkedFirst`，排序统一 `compareEntries()`。
- **新增独立大分类（ys27 模式）要改 category.js 的 7 处**：全局 `ysItems`、`buildEntries()` 末尾无条件 push（**不受 srcMode 影响**）、`ppScanPool()`、`allEntriesAllSources()`、`ppOfQid()` 的 `_ppIdx`、`catCard()` 的 `yearHtml`（显示题源标签而非年份链接）、`init()` 的 `Promise.all` fetch。收藏/标记/笔记/搜索/掌握地图/复测页走 `qidOf()`+`allEntries` 自动覆盖；**`fav.html`/`analysis.js` 只读 exam.json，不会覆盖**。新 L0 用 `ord=60000` 排到真题之后。
- 分类页 URL 参数是 **`?cid=<分类id>`**（不是 `?cat=`）；`?review=1` 复测、`?paper=1` 拼卷。
- **分类搜索归一化（11-14）**：`normFont`（全角→半角/清零宽）→ `searchTokens`（按空白切词，**AND** 语义）→ `searchBlob`（LaTeX **命令去反斜杠、结构符当分隔、公式内容保留**：`\sin x`→`sinx`、`\int_0^{x^2}`→`int0x2`）→ `entrySearchBlob`（每题算一次挂 `e._sb`）。**改搜索词必须走 `setCatSearchKw()`**，三处赋值点（提交搜索 / `selectCat` 退出 / 恢复 `st.search`）漏一个就不同步。测试 `tools/_test_cat_search.js`（44 项 + 2 项变异反向验证）。
- 「掌握地图」mastery.js/css 必须在 category.js **之后**引入；「💡建议」advice.js 两套口径（薄弱=不会×2+不熟加权；待刷=core 未掌握），`advJump` 先切 core。
- 跨库去重 `normStem()` 只去 LaTeX **结构**符号、**保留公式内容** + bigram Jaccard；别放宽 source 正则（会误藏 563 道改写题）。多级分类做过两版后用户要求退回三级。
- **拼卷规则**：池 = `ppScanPool()` 三源；入池=已收藏且未掌握；`qDraw[qid].d>0` **永久排除**；`doAt=max(dailyMarks 最后动过, 收藏时间)`（无记录老题靠收藏时间兜底）；层级优先、层内按 `ageDays` 7 天分档从旧到新；左栏 `ppProgHtml()`；历史卷回填 `qDrawBF`。
- 拼卷 UI：`ppViewPos={id,y}` 刷新还原（用户 wheel/touch/keydown/pointerdown 取消）；右侧 `ppNav` 复用 `.float-q`（`body.paper-mode .float-q{display:none}` 需同级 `.pp-nav` 覆盖 + `[hidden]` 兜底）；`ppNote-<卷id>` 富文本备注，⚠️ 不复用 `applyNoteFormat/noteInput`（会写 `examNote-undefined`），另写 `ppNoteFmt`。
- **拼卷题号只把「不会」标红**：`ppNavStates()` 按 `.pp-item` 的 **DOM 顺序**取实时 `statusGet()`；`ppRefreshNavMarks()` 只 toggle `mark-unk`、不重建 DOM。CSS 用 `.pp-nav .nav-q.mark-unk(.on)` 高权重压过选中蓝底。
- 核心题库与 exam.json 同结构，`categoryIds:[catId]` 挂同一棵树；新格式标准：`answer`=【答案】+空行+【分析】+【解】分步+⚠️易错；`idea`=2~4 句。catId 映射 `tools/_map_catid.py`。
- ⚠️ `pdfNo` 按章节编号 ≠ PDF 按 35 天计划编号。用户口径**只刷核心题库**，统计/建议只看 core_bank。exam.json 已知缺陷：2003 数二第 11 题选项 D 应为 `$1>I_2>I_1$`。
- 资料：线代答案册 `D:/cjx/下载/QQ FileRecv/线性代数_真题+重点题_答案册（含目录与页码）.pdf`；大观园源库 `assets/questions.json`（5952 题）；严选题文字层快照 `tools/_yancai_textlayer.json`。

## 7. 记忆卡（cards.html）
- `notes.json` 按 `##` 拆卡（首个 `##` 前为「概述」）→ 超 `SOFT_LIMIT=440` 按语义块二次拆 → 行内 `$...$` 候选 ≥ `CLOZE_MIN=2` 为背诵卡（SRS），否则阅读卡。
- ⚠️ 拆卡必须 `stripCmt` 剥 HTML 注释（否则 596/686 张卡标题带 `<!-- 源:p12 -->`）；改 id 会让旧进度失配 → `legacyCardId` 迁移。
- 候选同源：`MATH_RE` + `isWorthy`；`applyCloze` 按 `clozeScore` 取前 N，`DEF_CLOZE=3`/`MAX_CLOZE=6`，必须在 `renderMath` **之前**。
- 读用 `peekOf(id)`（不写 ST.cards），写才 `stOf(id)`；`applyStoredCards()` 只改内存不落盘。两个队列共享 qi → 统一 `currentCard()` 按 mode 分流；卡片 id 绝不拼进内联 onclick（用 `data-act`/`data-id` + 委托）。
- 测试只用 `_test_cards_v4.js`（49 项，`makeDom(seed)` + 真 KaTeX）；v3 已废弃。别锁死数据快照，改断言不变量（每个 `##` 至少一卡 + 正文保留率 ≥98%）。

## 8. 历史教训
- HTML 引用死链 → 公式全不渲染。测试要按 HTML 真实 `<script src>` 顺序拼成**一个函数体**执行，分文件 eval 作用域隔离。
- 题库交叉比对只覆盖题库里有的题；「条件不足/待核」往往是**题面抄错**，先核真题原貌。批量加粗：不吞相邻词、不拆词（≤8 字）、合并相邻加粗块（否则 `***`）。
- `agent-browser`：守护进程随 Bash 会话结束 → `open`/`eval`/`screenshot` 必须在**同一次 Bash 调用**，输出重定向到文件（管道被 daemon 挂住）；⚠️ **每次 `open` 是新 context，localStorage 不跨调用保留**，验「注入标记→跳转→断言」要写成 `open`→`eval`(setItem + `location.href=…`)→`sleep`→`eval`(断言) 四步一串；在 about:blank 上读 localStorage 会抛 `SecurityError`（上下文失效信号）；静态服务器要 `run_in_background` 常驻，curl 探测加 `--noproxy '*'`；顶层 `let` 不在 window 上但 eval 可直接访问。
- PDF 转写：项目 venv 无 pymupdf，用 `D:\python\python.exe`；KaTeX 子集字体缺 ToUnicode 会让文字层公式破损 → 必须渲染 PNG 后看图转写。Windows 下 D 盘 Python 无 `/tmp`，用 `C:\Users\cjx\AppData\Local\Temp\`。

## 9. 真题页（exam.html / exam.js）
- 左栏 `#paperList`：`curPaper` + `qidOf(p.id,q.no)` 驱动收藏/标记/笔记/试卷点评（`examReview-<卷id>`）/做题模式/悬浮题号导航，`?paper=<id>&no=<题号>` 下钻。
- **两级分组（11-14）**：`init()` 并行 fetch `exam.json` + `mn27_papers.json`（失败静默降级），`paperGroups()` 按 `p.group==='mock'` 分「数二真题」/「模拟卷」；`renderPaperList()` 两级渲染，`togglePaperGroup()` 折叠态存 `examGroupOpen`（首次两组都展开）。显隐用 `.paper-group-body.collapsed` class，**不用 hidden 属性**（避开 hidden 铁律）。模拟卷不显示 `p.year`，只显示 `p.title`。
- `mn27_papers.json` = 27 精选十套卷，本批 5 套 `mn27-03`~`mn27-07` / 110 题，qid `mn27-XX-N`；草稿 `tools/mn27_ans/qXX_stem.md`+`qXX_ans.md`，构建 `_build_mn27.py`，审计 `_mn27_check.py`（草稿）+ `_audit_mn27.py`（产物）。**剩余 5 套 01/02/08/09/10 未做**。
- ⚠️ 该套资料：题本文字层公式破损必须渲染 PNG 看图转写；答案 **01/02 有文字层**（Unicode 数学字母 + 公式拆散行，仍需重排 LaTeX），**03–10 共 86 页零文字层**（整页扫描图）。用 5 个 subagent 并行逐页转写最省时。
- `fav.html` / `analysis.js` 只读 `exam.json`，模拟卷收藏**不会**出现在收藏汇总与分析建议；拼卷池/分类树也不纳入（按套卷刷题定位）。
