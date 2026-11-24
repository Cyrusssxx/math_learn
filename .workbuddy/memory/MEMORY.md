# math-note 长期记忆（2026-11-16 精简；细节见当日日志）

## 0. 协作纪律
- 默认 commit+push 到 Cyrusssxx/math_learn，**只 stage 指定路径**；交付含审计/commit hash/`git ls-remote` 远程 HEAD/CACHE_VER/push 五项。
- 大改动先复述需求+指明信息缺失；修一个错误主动扫同类；小数据手动优先；报错先查缓存/源数据；UI 真机复现。新断言必须反向验证；变异测试用新对象。`node` 用系统 PATH；`E:/workbuddy-data/...` runner 已失效。

## 1. 构建/部署/测试环境
- 新数据文件加 `pwa/sw.js` 的 `PRECACHE`；pre-commit 自动跑 `build_assets_ver.py`+`build_sw.py` 并 `git add`。
- **hidden 铁律**：带 `hidden` 的元素 CSS 不能声明 `display`，需同级 `[hidden]{display:none}`。
- **jsdom**：外链 css 不加载（内联再断言）；无 UA hidden；不解析 CSS 变量（用 `.matches(sel)`+CSS 源文本正则）；脚本必须 `process.exit()`；逐篇渲染 30+ 篇卡死。jsdom 在 `D:/ai code/408-quiz/node_modules/jsdom`。
- CSS 变量白名单：`--bg --bg-side --bg-hover --bg-active --text --text-dim --text-faint --accent --strong --border --shadow --mk-* --hl-*`；**无 `--bg-card`**。
- agent-browser：`open`/`eval`/`screenshot` 必须同一次 Bash 调用，输出重定向到文件；每次 `open` 新 context，验「注入→跳转→断言」写 `open`→`eval`(setItem+location.href)→`sleep`→`eval`；静态服务器后台起，curl 加 `--noproxy '*'`；顶层 `let` 不在 window 但 eval 可访问。⚠️ 2026-11-21 夜此 CLI 在 Windows 彻底卡死（守护进程 sidecar 残留、所有命令含 `open about:blank` SIGTERM，`doctor --offline --quick` 清一次又崩）→ 改 Playwright（Python `D:/python/python.exe` 已装，chromium 在 `E:/deps_cache/ms-playwright`），持久 profile `E:/deps_cache/browser-profiles/cxymath_pw`。需要真实浏览器任务优先 Playwright。
- PDF 转写：`D:\python\python.exe`+PyMuPDF；KaTeX 字体缺 ToUnicode → 必须渲染 PNG 看图；D 盘 Python 无 `/tmp`，用 `C:\Users\cjx\AppData\Local\Temp\`。

## 2. 数据资产（pwa/data/）
- `exam.json` 数二真题 27 卷 607 题（exam.js/category.js）；`mn27_papers.json` 27 精选十套卷 10 套 220 题（exam.js，qid `mn27-XX-N`）。
- `core_bank.json` 741 / `dgy_items.json` 1346 / `bank_questions.json` 827 / `ys27_items.json` 37（qid `ys27-N`，L0=50000，后 18 题超纲待决策）/ `notes.json` 33 篇（隐藏 21记 后 32 篇）/ `exam_categories.json` 129 节点 / `fav_focus.json` 55 知识点·88 章锚点·3042 qid。`practice.json` 死数据。
- 写回格式：`exam.json` 单行紧凑 `json.dumps(d,ensure_ascii=False)`+`newline=''`；`core_bank.json` indent=1 无尾换行；`notes.json` indent=2 无尾换行。**禁止 inline `python -c` 改 JSON/反斜杠**，必须 .py 脚本 + 独立 .py 全量验证。JSON 单反斜杠会被吃掉（`\frac`→U+000C，护栏 `_audit_syllabus.py` 扫 C0）。
- qid=`<卷id>-<题号>`；`qidOf()` 经 `linkedQid` 重定向；双份数据不保证一致，改一处互核。四态：不会>不熟>已掌握>未刷。localStorage：`examFav`、`examStatus`、`examNote-<qid>`、`catSrcMode`、`qDraw`、`qDrawBF`、`paperList`、`dailyMarks`、`ppHeart`、`examGroupOpen`、`examLastPos`。
- `bank_questions.categoryIds` 全字符串，其余题库数字（渲染器 `String()` 兜）。
- **题目视频链接**：core_bank `q.videos=[{url,label,status}]`（前端 `videoBtnHtml`/`openVideoModal` 只读 url+label，status 仅内部标记 confirmed/candidate）。2026-11-21 补 19 题 49 条（极限40缺/二重9缺）。**数据源 = 大观园正式站 `math.cxyonly.fans` 登录后 `GET /api/v1/questions/{site_qid}/videos`**（主题目 API `/api/questions` 无 video 字段；静态站 `daguan-math-static.pages.dev` 与 cxyonly 本地镜像都无视频）。鉴权 `authorization:Bearer web-session:`+`x-csrf-token` 由页面 JS 动态生成，须 Playwright 持久化 profile 登录后拦截 `/api/questions` 请求截 header 再 `ctx.request.get` 调 API（requests 带 cookie 401）。匹配：core 题 source 与站点 source 体系不同，用题干归一化 `SequenceMatcher`≥0.85 粗筛 + label 年份/卷种/题号核对，错配排除（ratio 高也可能虚高，如 q3899）。详情/脚本见 2026-11-21 日志。
- 校验：`_deep_validate.py`/`_audit_latex.py`/`_scan_unpaired.py`/`_audit_ys27.py`/`_audit_mn27.py`/`_mn27_check.py`；JS `_test_pp_counter.js`(51)`_test_notes_hl.js`(182)`_test_cat_search.js`(44)`_test_pp_heart.js`(34)。

## 2.5 易错本（mistake.js / mistake.css，2026-11-24）
- 侧栏入口条 → 正文区独立视图（`body.mb-open` 隐藏 #docPane 显示 #mbView，左栏目录树+右栏保留不全屏）；状态存 `mistakeView`。数据 localStorage `mistakeNotes`，贴图独立 IndexedDB `mistakeNoteImg`（id `mb` 前缀），与做题/批注贴图完全隔离；全量备份/恢复已接入。
- 编辑器 token 与 exam.js 同源但独立实现（复制隔离，不共用全局变量）：`<c:#hex>`/`<h:#hex>`/`<b>`/`<i>`/`<h1>`/`<h2>`/`[图:id]`；Ctrl+V 多图先同步登记节点再压缩写库（防丢图），保存前 `await waitPendingImgs()`。
- ⚠️ 视图退出**绝不能监听 hashchange**：reader.js 首次异步加载会写一次 hash → 刷新后误判退出；改为 document 捕获阶段点击 `#navTree a, #searchResults a` 才退出。
- ⚠️ 卡片摘要 `plain()` 截断前必须把 `$...$`/`$$...$$` 抽成占位符再还原，直接删 `$` 会让公式变纯文本、直接截会留半截定界符。
- 预设标签 15 个（高数 9 + 线代 6，剔除真题点睛与 21记），硬编码在 mistake.js `PRESET_TAGS`。回归 `tools/_test_mistake.js`（68 项）。

## 3. 笔记页（index.html / reader.js）
- `chapters[i]` ↔ 正文第 i 个 `##` 必须镜像，差异以 `##` 为准（改 `##` 毁批注锚点）。目录两级（章 `ch-N`→小节 `h3-N`），`tocItems()` 按文档顺序夹取判归属。
- ⚠️ `##`/`###` 标题不得写 `$...$`（目录取 textContent，KaTeX 双副本→长串）；护栏 `_verify_varlimit.py`。⚠️ 加内容只能追加到 `md` 末尾（批注 sid=笔记id#块序号），断言「原 md 是新 md 严格前缀」+真实 `notesAnnot` 注入回归。
- `mdToHtml`：`##`/`###`/`####`｜`::: fold/nav/点睛`｜独行 `{#id}`｜独行 `![..](..)`→figure｜`>`｜`---`｜`-` 列表｜`|` 表格｜其余 `<p>`；`inline()` 支持 `**bold**`、`![img]`、`[text](#anchor)`、`` `code` ``、`⭐`。新语法补 CSS。
- ⚠️ `reader.js` 与 `mdrender.js` 两份副本，改渲染必须同步；链路 `emitList→breakLines→inline`。`emitList` 跳级缩进丢整段列表；KaTeX auto-render 跨元素配对 `$`，输出前 `isBalanced()`+`stripLoneDollar()`。
- **高亮配色**：黄淡杏 `#ffe8b8`（`--mk-y`/`.ab-y`/`ANN_HLS[0]`；深色 `#6b5c33`），按 `y` 键。带高 46%、仅 alpha 调浓度；`.ann-text mark` 要写 `:not(.note-hl)` 免覆盖 `--nhl-bg`；`.katex.fml-hl-*` padding 2px 4px+圆角 6px。断言 `_test_notes_hl.js`。
- **移动端目录（≤900px）**：`body.nav-open`+`::before` 遮罩（z25<sidebar z26<☰ z30）；展开 `.side-head` padding-top:60px；收起统一 `closeMobileNav()`。`stripChNum()` 只剥显示编号，绝不动 `data-ch`/id。
- **fav_focus 重点标记**：按「已收藏∩(不会∪不熟)」题数分级（很重点≥10→`ff-hot`+⭐，重点4–9→`ff-warm`），`applyFavFocus()` 标三处：左栏 `#navTree .tree-ch`、右栏 `#tocPane .toc-item`、正文 `.doc-toc`；`storage` 跨标签刷新。⚠️ 左栏铁律：跨笔记 key 用 `data-note|ch`；纯文本锚点无 `.toc-name`，⭐插首位；`renderTree()` 重建 DOM 后末尾补刷。CSS 左栏 `.ff-*` 写在 `:hover` 后并加 `.ff-*:hover` 保色。构建 `tools/_build_fav_focus.py`（显式 RULES，跳过隐藏 21记）。不含纯收藏/mastered；不碰 md；不用 `:has`。测试 `_test_fav_focus{,_dom,_tree,_css}.js`。

## 4. 跨页副本（exam.js ↔ category.js）
`mdBlockWithImg`/`fillExamNoteImgs`/`zoomAnsImg`/`mdBlock`/`qCard`vs`catCard`/`.q-note` 双框/`copyQLatex`vs`copyCatQLatex`。
- 答案/思路初始 hidden，展开后补调 `renderMath`+`fillExamNoteImgs`；`mdBlock` 独占一行 `$$` 要显式放行开块。⚠️ 题卡 `mdBlock` 不支持 `- ` 列表（每行 `<p>`，只认 `**加粗**`/`==高亮==`/`$$`/笔记令牌），答案分步用 `**① …**`。
- ⚠️ `copyCatQLatex` 必须走 `catFindByQid()`（拼卷/复测先 `ppOfQid`，分类页先 `allEntries`，再 `allEntriesAllSources` 兜底），只查 allEntries 会让 15% 静默失效。

## 5. 笔记编辑器（contenteditable）
- DOM 即数据载体；贴图后 blob 异步压缩，保存前 `await waitPendingImgs()`。⚠️ 编辑态取不到 blob 绝不 `replaceWith` 文本（丢 `[图:id]`→孤图清理→图永久丢失），只标 `.img-fail`。
- 三条保存路径：`saveNoteBtn`/`toggleNoteEdit` 完成分支/`saveNoteFromOps`。令牌 `[图:id]`、`<c:#hex>`、`<h:#hex>`、`<b>/<i>`、`<h1>/<h2>` 在 `editorToNote`/`noteToEditor`/`mdBlock` 三处都识别。H1/H2 用 `execCommand('formatBlock',false,'H1')` 且禁用 styleWithCSS。

## 6. 分类页 / 拼卷 / ♥
- 双数据源 `#srcToggle`→`applySrcMode()`，存 `catSrcMode`（exam/core 默认 exam）；`buildEntries()` 按 `qid#catId` 去重；排序 `compareEntries()`。URL `?cid=<id>`；`?review=1` 复测、`?paper=1` 拼卷、`?heart=1` ♥ 页。
- **新增独立大分类（ys27 模式）改 category.js 7 处**：全局 `ysItems`、`buildEntries()` 末尾无条件 push、`ppScanPool()`、`allEntriesAllSources()`、`ppOfQid()` 的 `_ppIdx`、`catCard()` 的 `yearHtml`、`init()` fetch。新 L0 用 `ord=60000`。**`fav.html`/`analysis.js` 只读 exam.json**。
- **搜索归一化**：`normFont`（全角→半角/清零宽）→`searchTokens`（空白切词 AND）→`searchBlob`（LaTeX 去反斜杠、结构符分隔、公式内容保留）→`entrySearchBlob`（挂 `e._sb`）。**改词必须走 `setCatSearchKw()`**（三处赋值点）。
- 「掌握地图」mastery.js/css 必须在 category.js 之后；advice.js 两套口径，`advJump` 先切 core。去重 `normStem()` 只去 LaTeX 结构符号+bigram Jaccard；别放宽 source 正则（误藏 563 道改写题）。
- **拼卷规则**：池=`ppScanPool()` 三源；入池=已收藏且未掌握；`qDraw[qid].d>0` 永久排除；`doAt=max(dailyMarks 最后动过,收藏时间)`；层级优先、层内按 `ageDays` 7 天分档；历史卷回填 `qDrawBF`。`ppNote-<卷id>` 备注⚠️不复用 `applyNoteFormat/noteInput`（会写 `examNote-undefined`）。题号只把「不会」标红：`ppNavStates()` 按 `.pp-item` DOM 顺序取实时 `statusGet()`，`ppRefreshNavMarks()` 只 toggle `mark-unk`。
- ♥ 标记：`ppHeart={qid:{t}}`，`heartGet/heartSave/isHeart/toggleHeart`。`catCard` 第 4 个按钮 `.q-st-heart`（♡/♥）只在 `PAPER_MODE||HEART_MODE` 渲染；`?heart=1` 独立页汇总（分页 40、状态筛选、可取消、storage 同步）。⚠️ 全站**不出现「我喜欢」文字**；汇总页首屏 `await loadExamSources()` 后再渲染，否则 core 重定向题号（109/524）错乱+漏题；`renderNav()` 汇总页用 heartList/rvList 题号+状态着色。顶栏 exam.html/category.html 加入口。`mn27-*` 不在 category.js 数据源，不进 ♥ 页。
- ⚠️ `pdfNo` 按章节编号 ≠ PDF 35 天计划编号；用户口径**只刷核心题库**。exam.json 已知缺陷：2003 数二第 11 题选项 D 应为 `$1>I_2>I_1$`。资料：线代答案册 `D:/cjx/下载/QQ FileRecv/线性代数_真题+重点题_答案册（含目录与页码）.pdf`；大观园源库 `assets/questions.json`（5952 题）。

## 7. 记忆卡（cards.html）
- `notes.json` 按 `##` 拆卡→超 `SOFT_LIMIT=440` 二次拆→行内 `$...$` 候选≥`CLOZE_MIN=2` 为背诵卡。⚠️ 拆卡须 `stripCmt` 剥 HTML 注释；改 id 会让旧进度失配→`legacyCardId` 迁移。
- `applyCloze` 按 `clozeScore` 取前 N（`DEF_CLOZE=3`/`MAX_CLOZE=6`），必须在 `renderMath` **之前**。读用 `peekOf(id)`（不写 ST.cards），写才 `stOf(id)`；卡片 id 绝不拼进内联 onclick。测试只用 `_test_cards_v4.js`(49)。

## 8. 真题页（exam.html / exam.js）
- 左栏 `#paperList`：`curPaper`+`qidOf(p.id,q.no)` 驱动收藏/标记/笔记/试卷点评（`examReview-<卷id>`）/做题模式/悬浮题号导航，下钻 `?paper=<id>&no=<题号>`。题干容器 `.q-body`。
- **两级分组**：`init()` 并行 fetch `exam.json`+`mn27_papers.json`（失败静默降级），`paperGroups()` 按 `p.group==='mock'` 分「数二真题」/「模拟卷」；`renderPaperList()` 两级渲染，折叠态存 `examGroupOpen`，显隐用 `.collapsed` class 不用 hidden；模拟卷不显示 `p.year`。顶栏单独「🎲 拼卷」入口。
- `mn27_papers.json` 10 套 220 题已完成；草稿 `tools/mn27_ans/qXX_{stem,ans}.md`，构建 `_build_mn27.py`，审计 `_mn27_check.py`（草稿）+`_audit_mn27.py`（产物）。题本文字层破损须看 PNG；答案 01/02 有文字层但公式以图为准（01-Q1 分子 `$2x^{2n}-1$`），03–10 共 86 页零文字层，多套并行用 subagent。⚠️ 题干与答案交叉核对；【易错】别混入流程措辞。
- ⚠️ `_build_mn27.py` 的 `field()` 靠 `【tag】` 定位：草稿正文不得出现 `【答案】/【解】/【思路】/【易错】` 字面（q02 Q4 事故）；护栏 `_mn27_check.py`+`_audit_mn27_consistency.py`（解析≥60 字）。审校 `_katex_mn27.js`(7336)`_katex_exam.js`(24312) 均 0 失败。
- **数二大纲合规**：不考概率统计、无穷级数/傅里叶、三重积分与线面积分、空间解析几何、方向导数梯度、差分方程、伯努利/全微分/欧拉方程（考点名称）、「数一/数三/考纲/超纲」元话语。替换为倒数换元、凑全微分、有限阶麦克劳林、弧长微元定积分、等比有限和+数列极限；别把黎曼和误判级数。`_audit_syllabus.py`（`--selftest`）+`_fix_syllabus.py`+`_verify_syllabus.py`。⚠️ `ys27_items.json` 后 18 题、`core_bank.json` 约 6 题、`dgy_items.json` 3 题为整题超纲，**待用户确认后再删**。
- 十套卷原卷固有瑕疵（已核 PDF，别反复改）：02-Q4 条件矛盾；05-Q1 在 $f(0)=0$ 下 (B)(D) 同真；06-Q6 第二式代 $x=1$ 不自洽；04-Q22 答案册缺 (II)，已补 $B=2E-J/3$。

## 9. 历史教训
- HTML 引用死链→公式全不渲染。测试按 HTML 真实 `<script src>` 顺序拼成**一个函数体**执行。「条件不足/待核」往往是题面抄错，先核真题原貌。
