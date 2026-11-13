# math-note 项目长期记忆（2026-11-05 精简重组，详情见每日日志）

## 0. 协作纪律
- 提交默认 commit + push 到 Cyrusssxx/math_learn，**只 stage 指定路径**；交付汇总含审计结果 / commit hash / `git ls-remote` 远程 HEAD / CACHE_VER / push 确认五项。
- 大改动先复述需求并指明信息缺失；修完一个错误主动扫同类（真题卷优先）；小数据改动手动优先、不写脚本；报错先查缓存/源数据再判 bug；UI 问题要真机复现。
- 全套 runner：`E:/workbuddy-data/binaries/node/workspace/_run_all.js`（12 项）。

## 1. 构建与部署
- 新增数据文件必须加 `pwa/sw.js` 的 `PRECACHE`；pre-commit（`.githooks/pre-commit`）自动跑 `build_assets_ver.py`（html `?v=`）+ `build_sw.py`（CACHE_VER）并 `git add`；`common.js` 自动重载提示。
- **hidden 铁律**：带 `hidden` 的元素 CSS 不能声明 `display`（作者样式压过 UA），需同级 `[hidden]{display:none}` 兜底；排查 `_scan_hidden_conflict.js`。
- **jsdom 盲区**：外链 css 不加载（内联后再断言）；不实现 UA hidden；不解析 CSS 变量（改 `.matches(sel)` + CSS 源文本正则）；脚本必须 `process.exit()`；逐篇渲染 30+ 篇会卡死（抽函数配假数据）。新增断言必须**反向验证**。
- CSS 变量白名单：`--bg --bg-side --bg-hover --bg-active --text --text-dim --text-faint --accent --strong --border --shadow --mk-* --hl-*`；**没有 `--bg-card`**（曾致暗色白底浅字）。跨页共用组件样式要在每个 css 都写（`.all-ans-btn` 漏过）。

## 2. 数据资产（pwa/data/）
| 文件 | 内容 | 加载方 |
|---|---|---|
| `exam.json` | 数二真题 27 卷 607 题 | exam.js / category.js |
| `core_bank.json` | 核心题库 741 题 | category.js（core） |
| `dgy_items.json` | 大观园习题 1346 题 | category.js（exam） |
| `xd_bank.json` | 线代重点题 333 题 | category.js |
| `bank_questions.json` | 大观园真题 827 题 | category.js |
| `ys27_items.json` | 27 模拟卷精选题 37 题（qid `ys27-N`，第 4 个独立大分类 50000） | category.js（**不分 srcMode，始终并入**） |
| `notes.json` | 讲义笔记 33 篇 | notes.html / cards.html |
| `exam_categories.json` | 三级分类树（键为 id 字符串，129 节点） | — |

- `practice.json` 是死数据。格式：`exam.json`/`practice.json` 紧凑单行 `separators=(',',':')`；`exam_categories.json`/`bank_questions.json` pretty；**`core_bank.json` = `json.dumps(d, indent=1, ensure_ascii=False)` 无尾换行**（用 `JSON.stringify` 压平会造 4 万行假 diff）。
- ⚠️ 单行紧凑 JSON 必须 `json.loads`→改 dict→`json.dumps`；禁止 inline `python -c` 改反斜杠/正则/JSON（Bash 吃转义），必须写 .py 脚本 + 独立 .py 全量验证。`r"\\X"`=单反斜杠，双反斜杠要 `r"\\\\X"`。
- 修复字段遍历 `q.keys()` 全覆盖（含 `tips` 的 gs/jq/yc/zy）。LaTeX 填空统一 `\underline{\hspace{2cm}}`，纯文本包 `$...$`，`$$` 块内裸写；别误伤 `\int_0`/`|a_n|`（只匹配连续 3+ `\_`）。
- 验证三件套：`tools/_deep_validate.py`、`_audit_latex.py`、`_scan_unpaired.py`；数据改动后全跑，并走 commit（bump CACHE_VER）+ push 闭环（中间坏版本可能被 SW 缓存）。
- qid = `<卷id>-<题号>`；`qidOf()` 经 `linkedQid`（`xd-N`/`core-N`→真题 qid）重定向统一收藏/笔记键。⚠️ **双份数据不保证内容一致**（2023 数二第 5 题曾一处对一处错），改一处要互核。
- 四态：不会 > 不熟 > 已掌握 > 未刷（mastery.js）。localStorage：`examFav {qid:{t:ms}}`、`examStatus`、`examNote-<qid>`、`catSrcMode`、`catUnmarkedFirst`、`qDraw`、`qDrawBF`、`paperList`、`dailyMarks`、`ppViewPos`、`ppNote-<卷id>`。
- `bank_questions.categoryIds` 全是字符串，其余题库数字（渲染器 `String()` 兜过）。

## 3. 笔记页（index.html / reader.js）
- 结构 `{id,subject,order,name,title,chapters[],md}`；**`chapters[i]` ↔ 正文第 i 个 `##` 数量/顺序/文字必须镜像，差异一律以 `##` 为准改 chapters**（改 `##` 会移正文、毁划词批注锚点）。体检 `_audit_notes_layout.py`，对齐 `_fix_notes_toc.py --apply`。
- 右侧目录两级（章 `ch-N` → `###` 小节 `h3-N`）；`tocItems()` 用**文档顺序夹取**判归属；小节默认收起、只展开当前章；三级 hash `#/笔记/章/h3号`；`savePos/restorePos` 连小节记。
- ⚠️ **`##`/`###` 标题不得写 `$...$`**：目录取的是渲染后 h3 的 `textContent`，KaTeX 有 mathml `<annotation>` + aria-hidden 两份副本 → 一个 `$x$` 在目录里变成「xxx」，`$\Phi(x)=\int...$` 变成「渲染串 + 原始 LaTeX」长串（2026-11-13 实测；全库仍有 14 处历史标题中招，短公式影响小，未清理）。护栏见 `tools/_verify_varlimit.py`。
- ⚠️ **给已有笔记加内容只能追加到 `md` 末尾**：`annotate.js` 的 `sid = 笔记id#块序号`（`##`/`###` 不计入，只有 `li`/`p` 分配），中间插入会让后面所有块整体偏移、已有高亮/批注全部错位到别的段落。2026-11-13 补《变限积分》时该笔记已有 10 处标注（#28~#82），改走末尾追加 + 「原 md 是新 md 严格前缀」断言 + 真实 `notesAnnot` 注入回归（#78 蓝 / #61·#68·#69·#82 绿、#37 荧光 3 条逐字对上、相邻 #79 干净）。
- `notes.json` 格式 = `json.dumps(d, indent=2, ensure_ascii=False)` 无尾换行（round-trip 与磁盘字节完全一致，可直接 dump 回写）。
- `stripChNum()` 只剥章标题显示编号，绝不动 `data-ch`/id。章间距用 `padding-top`（`.toc-item + .toc-item`），`.toc-gap-lg` 标已读→未读分界。
- `mdToHtml` 语法：`#`跳过｜`##`/`###`/`####`｜`::: fold/nav/点睛`｜独行 `{#id}`｜独行 `![..](..)`→figure｜`>` 引用｜`---`/`***`/`___`｜`-` 列表｜`|` 表格｜其余 `<p>`；`inline()` 支持 `**bold**`、`![img]`、`[text](#anchor)`、`` `code` ``、`⭐`。⚠️ 新增语法同时补 CSS。
- ⚠️ `reader.js` 与 `mdrender.js` 是两份副本，改渲染逻辑**必须同步**；链路 `emitList→breakLines→inline`。
- `emitList` 跳级缩进会丢整段列表（按实际层级递归接管）；`renderTipsBlock` 四段标签之外的行必须追加渲染；KaTeX auto-render 跨元素配对 `$`，每张卡 `$` 配平、`$$` 独占行当原子块、切句只用 `。；！？`、输出前 `isBalanced()` + `stripLoneDollar()`。

- **高亮配色（11-08 定色 / 11-10 降浓度 / 11-11 两轮调参 / 11-13 定档）**：黄色档淡杏黄 `#ffe8b8`（`--mk-y`、`.ab-y`、`ANN_HLS[0]`；深色 `#6b5c33`），按 `y` 键存储，改配色值即自动变色、无需迁移。11-10：实色 52% 带 → `rgba(.52~.55)` 的 30% 带；新增 `--mk-*-line` 下划线淡档（浅 .40 / 深 .38）、offset 4px；修好 `mark.note-hl` 没引用 `--nhl-bg` 的缺陷。⚠️ **方法论铁律：带高固定 46%，只用 alpha 一个维度调控浓度**（先 30%×.52 乘积过冲看不见 → 46%×.88 又压字 → 最终 **46% × 浅 .72~.74 / 深 .74~.76**）。`--nhl-bg` 由 annotate.js 本地 `annHlRgba(c,.72)` 提供（`common.js hlBg/.42` 六页共用，不动），`annSoftenHl` / 令牌渲染两处内联同步 .72 + 46%。⚠️ **`.ann-text mark` 与 `mark.note-hl` 特异性相同且排在后面，会盖掉 `var(--nhl-bg)`（批注自定义色曾恒显示固定黄 .30）—— 选择器必须写 `:not(.note-hl)`**。`--hl-*-soft` **.21~.22（深 .13~.15）专供公式整块底**，且 `.katex.fml-hl-*` 必须有 `padding: 2px 4px` + 圆角 6px（无 padding 时背景紧贴字形、积分号/上下标溢出盒子，视觉「范围小」）；`.ann-text mark` 兜底改用 `--mk-y2` 走 46% 带（`--hl-y-soft` 降档后当兜底只剩 ~10% 看不见）。`--hl-*-block` `.16~.18`；下划线淡档 / 1px / offset 4px / 公式 1px / 竖条 2px 全不动。⚠️ `text-decoration` 会传播进 inline 后代（含 KaTeX 用 `:has` 从父取消）。色板 `ANN_HLS` / `NOTE_HLS` / `PP_NOTE_HLS` 的 hex 不动。断言 `tools/_test_notes_hl.js`（167 项，含 alpha∈[.65,.85) 双向窗口 + 带高锁死 46% + 11 项变异反向验证；CSS 规则体提取正则要**行首锚定**）。

- **移动端目录（≤900px，2026-11-08）**：`body.nav-open` + `body.nav-open::before` 遮罩（z25 < sidebar z26 < ☰ z30）；展开时 `.side-head` 用 `padding-top:60px` **整行下移**避让 ☰（左右让位会把品牌挤成两行，实测否决）。收起统一走 `reader.js` 的 `closeMobileNav()`：点正文/遮罩、Esc、`renderDoc()` 切笔记、`resize>900`；document 的 click 监听要放行 `.menu-btn` 与 sidebar 内部，否则刚展开就被关掉。

## 4. 跨页副本（exam.js ↔ category.js）
`mdBlockWithImg` / `fillExamNoteImgs` / `zoomAnsImg` / `mdBlock` / `qCard`vs`catCard` / `.q-note` 双框 / `copyTextToClipboard` / `copyQLatex`vs`copyCatQLatex`。
- 答案/思路初始 hidden，**展开后补调 `renderMath` + `fillExamNoteImgs`**。
- `mdBlock` 裸 `$$` 坑：独占一行的 `$$` 要显式放行开块（`(!l.endsWith('$$') || l === '$$')`）。
- `.q-note` 只有 `/\[图:[a-z0-9]+\]/` 命中才加 `.has-img`；纯文字靠 `:not(.has-img) .q-note-preview` 去框。
- ⚠️ **题卡 `mdBlock` 不支持 `- ` 列表**（category.js:353 起，exam.js / exam-shared.js 是副本：每行一律包 `<p>`，只认 `**加粗**` / `==高亮==` / `$$` 块 / 笔记令牌）；`- ` 列表只在笔记页 reader.js / mdrender.js 的 `emitList` 里有效。答案里分情况讨论要用 `**① …**` 编号标签，写 `- ` 会留下裸短横线被误读成负号（2026-11-07 题 583 真机实测）。
- ⚠️ **拼卷/复测复制按钮**：题来自三源 `_ppIdx`（examPapers+corePapers+bankItems），`allEntries` 只装当前 srcMode 一源。`copyCatQLatex` 必须走 `catFindByQid()`（拼卷/复测先 `ppOfQid`，分类页先 `allEntries`，再 `allEntriesAllSources` 兜底，找不到给按钮提示）——只查 allEntries 会让 15% 的题**静默失效**（2026-11-05 实测 6/40）。

## 5. 笔记编辑器（contenteditable）
- 编辑器 DOM 即数据载体；贴图后 blob 异步压缩，保存前 `await waitPendingImgs()`。
- 编辑态取不到 blob **绝不 `replaceWith` 文本**（会丢 `[图:id]`→孤图清理删 blob→图永久丢失），只标 `.img-fail`；仅只读态可替换「图片已丢失」。
- 三条保存路径：`saveNoteBtn` / `toggleNoteEdit` 完成分支 / `saveNoteFromOps`。
- 富文本令牌（`mdInline` 先 `esc()` 再白名单还原）：`[图:id]`、`<c:#hex>`、`<h:#hex>`、`<b>/<i>`、`<h1>/<h2>`（块级独占行）；`editorToNote`/`noteToEditor`/`mdBlock` **三处都要识别全令牌**。
- H1/H2 用 `execCommand('formatBlock',false,'H1')` 且禁用 styleWithCSS。

## 6. 分类页 / 拼卷
- 双数据源 `#srcToggle`→`applySrcMode()`，存 `catSrcMode`（exam/core，默认 exam）；`buildEntries()` 按 `qid#catId` 去重；「无标记优先」存 `catUnmarkedFirst`，排序统一 `compareEntries()`。
- **新增一个"跟真题不重题的独立大分类"（如 ys27，2026-11-13）要改 category.js 的 7 处**：全局 `ysItems`、`buildEntries()` 末尾无条件 push（**不受 srcMode 影响**）、`ppScanPool()`、`allEntriesAllSources()`、`ppOfQid()` 的 `_ppIdx`、`catCard()` 的 `yearHtml`（加 `paper.id===…` 显示题源标签而非年份链接）、`init()` 的 `Promise.all` fetch。收藏/标记/笔记/搜索/掌握地图/复测页走 `qidOf()`+`allEntries`，自动覆盖；**`fav.html`/`analysis.js` 只读 exam.json，不会覆盖**。新 L0 用 `ord=60000` 排到真题（49000/51026）之后。
- 分类页 URL 参数是 **`?cid=<分类id>`**（不是 `?cat=`）；`?review=1` 复测、`?paper=1` 拼卷。
- **分类搜索归一化（2026-11-14）**：`normFont`（全角→半角/清零宽）→ `searchTokens`（按空白切词，**AND** 语义）→ `searchBlob`（LaTeX **命令去反斜杠、结构符当分隔、公式内容保留**：`\sin x`→`sinx`、`\int_0^{x^2}`→`int0x2`）→ `entrySearchBlob`（每题算一次挂 `e._sb`）。**改搜索词必须走 `setCatSearchKw()`**，三处赋值点（提交搜索 / `selectCat` 退出 / 恢复 `st.search`）漏一个就会 `catSearchToks` 不同步。测试 `tools/_test_cat_search.js`（44 项，含变异反向验证）。⚠️ 变异测试要用**新 entry 对象**，复用已缓存 `_sb` 的对象会读到正常版 blob 造成假通过。
- 「掌握地图」mastery.js/css 必须在 category.js **之后**引入；「💡建议」advice.js/css 两套口径（薄弱=不会×2+不熟加权；待刷=core 未掌握），排序 `b.w-a.w || b.todo-a.todo || a.id-b.id`，`advJump` 先切 core。
- 跨库去重 `normStem()` 只去 LaTeX **结构**符号、**保留公式内容** + bigram Jaccard；别放宽 source 正则（会误藏 563 道改写题）。分类器先定父级再在父级内分子级。多级分类做过两版后用户要求退回三级（73 节点）。
- **拼卷规则**：池 = `ppScanPool()` 三源（真题卷/核心题库/大观园）；入池=已收藏且未掌握；`qDraw[qid].d>0` **永久排除**（`ppClearDraw` 清零）；`doAt=max(dailyMarks 最后动过, 收藏时间)`（markDaily 2026-10-14 才上线，无记录老题必须靠收藏时间兜底，否则 9 月最老题垫底）；层级优先、层内按 `ageDays` 7 天分档从旧到新；左栏 `ppProgHtml()` 显示已抽/未抽；历史卷回填 `qDrawBF`。
- 拼卷 UI：`ppViewPos={id,y}` 刷新还原（多次对齐 + 用户 wheel/touch/keydown/pointerdown 取消）；右侧 `ppNav` 复用 `.float-q`（`body.paper-mode .float-q{display:none}` 需同级 `.pp-nav` 覆盖 + `[hidden]` 兜底）；`ppNote-<卷id>` 富文本备注，⚠️ 不复用 `applyNoteFormat/noteInput`（会写 `examNote-undefined`），另写 `ppNoteFmt`。
- **拼卷题号只把「不会」标红**（2026-11-07 用户口径，不熟/掌握/仅收藏暂不显示）：`ppNavStates()` 按 `.pp-item` 的 **DOM 顺序**取 `statusGet()` 实时值（`ppRender` 会按 PP_SEGS 重排，别用 `ppCur.items` 下标硬对）；`ppRefreshNavMarks()` 只 toggle `mark-unk`、不重建 DOM（保住展开态与高亮锚点），由 `toggleQStatus` 触发。CSS 用 `.pp-nav .nav-q.mark-unk(.on)` 高权重压过 exam.css 的选中蓝底，当前题也是实心红。
- 核心题库与 exam.json 同结构，`categoryIds:[catId]` 挂同一棵树；新格式标准：`answer`=【答案】+空行+【分析】+【解】分步+⚠️易错；`idea`=2~4 句概括。catId 映射 `tools/_map_catid.py`。
- ⚠️ `pdfNo` 按章节编号 ≠ PDF 按 35 天计划编号，别拿 pdfNo 当 PDF 题号。用户口径**只刷核心题库**，统计/建议只看 core_bank。exam.json 已知缺陷：2003 数二第 11 题选项 D 应为 `$1>I_2>I_1$`。
- 资料：线代答案册 `D:/cjx/下载/QQ FileRecv/线性代数_真题+重点题_答案册（含目录与页码）.pdf`（正文位图，书末补01—补39）；大观园源库 `assets/questions.json`（5952 题，无科目标记）；严选题 PDF 有文字层，快照 `tools/_yancai_textlayer.json`。

## 7. 记忆卡（cards.html）
- `notes.json` 按 `##` 拆卡（首个 `##` 前为「概述」）→ 超 `SOFT_LIMIT=440` 按语义块二次拆 → 行内 `$...$` 候选 ≥ `CLOZE_MIN=2` 为背诵卡（SRS），否则阅读卡。
- ⚠️ 拆卡必须 `stripCmt` 剥 HTML 注释（否则 596/686 张卡标题带 `<!-- 源:p12 -->`）；改 id 会让旧进度失配 → `legacyCardId` 迁移。
- 候选同源：`MATH_RE` + `isWorthy`，`countClozeCandidates` 与 `collectCands` 同源；`data-k` 只产 `'m'`。`applyCloze` 按 `clozeScore` 取前 N（⚠️/⭐/例 加权），不是均匀采样；`DEF_CLOZE=3`/`MAX_CLOZE=6`。⚠️ `applyCloze` 必须在 `renderMath` **之前**。
- 读用 `peekOf(id)`（不写 ST.cards），写才 `stOf(id)`（⚠️ 禁止按行号批量替换 JS）；`applyStoredCards()` 只改内存不落盘，测试断言落盘要先触发真实写盘。两个队列共享 qi → 统一 `currentCard()` 按 mode 分流；卡片 id 绝不拼进内联 onclick（用 `data-act`/`data-id` + 委托）；完成态替换 `cardWrap.innerHTML` → `ensureCard()` 用 `CARD_HTML` 还原；newDone/revDone 分开计数。
- 测试只用 `_test_cards_v4.js`（49 项，`makeDom(seed)` + 真 KaTeX）；v3 已废弃。别锁死数据快照，改断言不变量（每个 `##` 至少一卡 + 正文保留率 ≥98%）。

## 8. 历史教训
- HTML 引用死链 → 公式全不渲染（`cards.html` 曾把 auto-render 路径写错）。测试要按 HTML 真实 `<script src>` 顺序拼成**一个函数体**执行，分文件 eval 作用域隔离。
- 题库交叉比对只覆盖题库里有的题；「条件不足/待核」往往是**题面抄错**，先核真题原貌。批量加粗：不吞相邻词、不拆词（≤8 字）、合并相邻加粗块（否则 `***`）。
- `agent-browser`：守护进程随 Bash 会话结束 → `open`/`eval`/`screenshot` 必须在**同一次 Bash 调用**，输出重定向到文件（管道被 daemon 挂住）；⚠️ **每次 `open` 是新 context，localStorage 不跨调用保留**，验"注入标记→跳转→断言"要写成 `open`→`eval`(setItem + `location.href=…`)→`sleep`→`eval`(断言) 四步一串；在 about:blank 上读 localStorage 会抛 `SecurityError`（这正是判断上下文失效的信号）；静态服务器要 `run_in_background` 常驻，curl 探测要加 `--noproxy '*'`；顶层 `let` 不在 window 上但 eval 可直接访问。
