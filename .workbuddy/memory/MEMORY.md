# math-note 项目长期记忆（精简版）

## PWA 缓存规则
- **新增任何数据文件必须同步加入 `pwa/sw.js` 的 `PRECACHE` 数组**，否则 Service Worker 不缓存、用户刷新加载不到。
- 改完 PRECACHE 后运行 `python tools/build_sw.py` 自动 bump `CACHE_VER`；pre-commit 钩子（`.githooks/pre-commit`）会自动调用并 `git add pwa/sw.js`，前提是 `sw.js` 在暂存区。
- `js/common.js` 已注册 SW 并监听 `updatefound`/`controllerchange`，部署后页面自动重载一次（`wasControlled` 守卫避免首次误触发），并弹「发现新版本，点击刷新」提示条——无需再让用户手动双刷新。

## 分类树层级规则（2026-08-27 回退后）
- **当前分类界面只加载 `exam.json`（真题 607 题）**，不加载 `practice.json`。`git checkout 338ec28^` 回退后为三级分类（2 学科 / 12 章 / 59 知识点），`exam_categories.json` 共 **73 节点**（L0=2, L1=12, L2=59）。
- `category.js` 的 `buildTree` 是**写死三级**版本，与真题数据（全部落 L2）完美匹配。
- **⚠️ 历史教训（大观园版本已废弃）**：曾做过「任意层级叶子通过 `catLink(cid)` 向上归并到章节」和「L0~L8 完整多级树」两版（commit `f503ae5`/`f287f0e`），用户后要求退回。若再导入大观园，需重做这两处改动。

## 架构与数据结构
- **笔记图片**：`[图:id]` 占位符 → `mdBlockWithImg` 渲染 `<img class="exam-note-img" data-img="id">` → `fillExamNoteImgs(root)` 从 IndexedDB（`examNoteImg` DB，`imgs` store）异步取 blob 回填。两页（exam.js / category.js）的 `mdBlockWithImg`/`fillExamNoteImgs`/`zoomAnsImg` 为重复副本，改动须两端同步。
- **试卷数据**：`exam.json`（真题，607 题，唯一被加载）。`practice.json`（大观园 1402 题）文件保留但已从 `sw.js` PRECACHE 移除、不再加载。
- **分类数据**：`exam_categories.json`（73 节点，真题三级版）。
- **题库路径**：大观园源 `D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/`；导入脚本 `tools/import_daguanyuan.py`。
- **KaTeX 关键规则**：`renderMath` 只在初始渲染调用不够——答案/思路段初始 `hidden`，展开（`toggleQSec`/`toggleAllAnswers`/`examToggleAllAnswers`）后**必须补调 `renderMath` + `fillExamNoteImgs`**，否则 `$$` 块显示为原文（commit `3199434`）。回退分类页时此修复必须保留。
- **笔记双框规则**：`exam.js qCard()` / `category.js catCard()` 用 `hasImg = /\[图:[a-z0-9]+\]/.test(note)` 检测，有图才给 `.q-note` 加 `.has-img`；纯文字笔记靠 `.q-note:not(.has-img) .q-note-preview` 去框（`76602fd`）。两处副本须同步。
- **真题笔记编辑/显示**：已移植 408 批注体验——自动保存提示、textarea 自适应、贴图压缩(1200px JPEG)、单图删除(hover 右上×)、完成按钮淡化、编辑态实时预览（未落盘即见图）、卸载冲刷。保留 `[图:id]`+IndexedDB 架构（不移植 408 的 base64，避免爆 5MB）。
- **笔记富文本令牌格式（2026-08-24 定版）**：存 `localStorage` 的 `examNote-*` 用受控令牌，天然防 XSS（`mdInline` 先 `esc()` 再只还原白名单）。令牌集：`[图:id]`（图）、`<c:#rrggbb>…</c>`（字色，闭标签无冒号）、`<h:#rrggbb>…</h>`（高亮底，闭标签无冒号）、`<b>…</b>`/`<i>…</i>`（行内粗斜）、`<h1>…</h1>`/`<h2>…</h2>`（块级标题，独占整行、序列化包裹整段）。序列化 `editorToNote`、反序列化 `noteToEditor`、渲染 `mdBlock`（exam.js+category.js 两页须同步）三处都要识别全令牌集；改其一必同步另两处。
- **H1/H2 实现坑**：`applyNoteFormat` 对 h1/h2 用 `execCommand('formatBlock', false, 'H1'/'H2')` 且**禁用 styleWithCSS**，否则退化成 `<span style>`；粗体/斜体原生 Ctrl+B/I 即可（span-bold 会被 `editorToNote` 归一化为 `<b>` 令牌）。
- **试卷点评**：保存后默认显示全文（`pre-wrap` 换行），不再只取首行折叠。

## 关键教训（来自实际踩坑）
- **样式副本易漏**：`.all-ans-btn` 只写在 `category.css`，`exam.css` 缺失 → 真题页按钮无样式不可见。跨页共用组件的样式要在每个 css 都有。
- **用户偏好「不开新窗口」是阶段性要求**：曾全量移除 `target="_blank"`，后来又要求 `exam.html` 顶部「🗂 分类」单独改为新标签页（`d11c5d5`）。其余入口保持同窗口。
- **底部导航已删除**：`exam.html` 的 `exam-btm` 底部导航栏连同 CSS 已移除（`99388ff`）。
- **分类器做多级时，先定父级再在父级内分子级**，千万别把子级关键词做成全局平铺匹配，否则通用词跨父级误吞。
- **exam.json 中"条件不足/待核"往往不是真条件不足，而是题面抄错**，先核对真题原貌再下结论。
- **题库交叉比对（mathnote-bank-compare skill）只覆盖题库中有的题**，题库未收录的需用户人工提出或联网核卷。
- **⚠️ 单行紧凑 JSON（exam.json）改动必须用 json.loads→改 dict→json.dumps 写回**：exam.json 是单行 880KB 紧凑 JSON，其中 LaTeX 命令的**文件字面为双反斜杠 `\\dfrac`**。直接用 Edit 工具改会被参数转义把 `\\` 写丢成 `\`，产出 JS `JSON.parse` 拒绝的非法 JSON（python json.loads 宽松可过、前端必炸）。json.dumps(ensure_ascii=False, separators=(',',':')) 自动转义，安全无坑（2026-09-02 踩坑实证：连改 5 次全破坏，最后 json 重写一步到位）。
- **r-string 反斜杠折叠**：python `r"\\X"` = 单反斜杠 `\X`（`\\` 折叠 1 个 `\`）；要双反斜杠需 `r"\\\\X"`。匹配文件字面时用 `raw.find` 单反斜杠能命中 `\\` 的子串，易误判。
- **⚠️ 禁止 inline `python -c` 做反斜杠/正则/JSON 相关的 exam.json 修改与验证（2026-09-03 实证）**：Bash 工具双引号会层层吃反斜杠，`r'\\\\left'` 到达 python 时层数错乱 → 误报 2936 处、产出 `\$\underline` 污染数据。**必须写 .py 脚本文件执行**，且每轮修改后用独立 .py 全量验证。
- **LaTeX 填空横线规范（2026-09-03 定版）**：填空统一 `\underline{\hspace{2cm}}`。**纯文本处必须包 `$...$`（否则显示原文）；`$$` 显示块内必须裸写（包 $ 会让 KaTeX 解析炸）**。合法下标 `\int_0`/`|a_n|`/`\lim_{x\to0}` 严禁被填空正则误伤——匹配只针对连续 3+ 个 `\_` 或纯下划线段。
- **LaTeX 命令双转义检查脚本模式**：扫描逻辑串（json.load 后）中 `\\left`/`\\right` 等 2 反斜杠命令 → replace 为单反斜杠；全量验证 0 残留。数据修复必须走 commit（pre-commit 自动 bump CACHE_VER）+ push 闭环，用户端 SW 才会更新；中间损坏版本可能已被 SW 缓存。
- **浏览器验证 KaTeX 泄漏**：先 unregister 全部 SW + caches.delete 再开页面；检查泄漏要移除 `.katex` 元素后看剩余文本（annotation 副本含原文会误报）。
- **⚠️ mdBlock 裸 `$$` 行坑（2026-09-03）**：`'$$'.endsWith('$$')` 恒为真，独占一行的 `$$` 必须显式放行开块（条件 `(!l.endsWith('$$') || l === '$$')`），否则多行显示块整体失效、公式逐行裸奔。exam.js 与 category.js 两端同步修。
- **⚠️ exam.json 修复字段清单必须含 `q.tips` 字典**：tips 有 gs/jq/yc/zy 四类子键，首轮 `\\left` 修复漏掉 203 处。遍历字段不要硬编码 ['stem','answer','idea']，用 `q.keys()` 全覆盖。
- **跨行失配 `$`**：`$` 开在上一行闭在下一行时，mdBlock 按行拆 `<p>` 导致 KaTeX 无法跨元素配对 → 用 `tools/_scan_unpaired.py` 按行查奇数 `$`，合并回单行。
- **验证脚本三件套（tools/ 永久保留）**：`_deep_validate.py`（分隔符配平+双转义+污染）、`_audit_latex.py`（结构回归）、`_scan_unpaired.py`（跨行 `$`）。数据改动后三个全跑。
- **⚠️ contenteditable 编辑器 DOM 是笔记数据载体（2026-09-06 实证）**：真题页贴图后 blob 异步压缩写库（几百 ms），手动保存前必须 `await waitPendingImgs()`（`_pendingImgTasks` 记录写库 Promise）；`fillExamNoteImgs` 在**编辑态**（同卡编辑器可见）取不到 blob 时**绝不 replaceWith 文本**（换掉=editorToNote 序列化丢 `[图:id]` → 孤图清理删 blob → 图永久丢失），只保留节点标 `.img-fail` 占位；仅只读态才允许替换成「图片已丢失」（数据在文本）。手动保存三条路径：`saveNoteBtn`/`toggleNoteEdit` 完成分支/`saveNoteFromOps`。annotate.js 令牌载体是卡片条（不在编辑器 DOM），同款替换仅伤显示，可不同步。

## 大观严选题 PDF 与参考题库（2026-09-17 新增，关键事实）
- **`D:/ai code/【A4紧凑】数二大观严选题做题本.pdf` 有文字层**（重排版非扫描）。`page.get_text()` 可直接取到权威字符与每题题源标签；结构（分式/根号/积分限）会丢，所以只能做**字符级校验**，不能替代视觉还原。文字层快照：`tools/_yancai_textlayer.json`（脚本 `tools/_extract_textlayer.py`）。
- **参考题库路径**：`D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json`（5952 题，数一/二/三真题 1987-2026，含 source/answer/explanation）。注意解压后是**嵌套目录**（外层与内层同名）。
- 参考库合计 8788 条：大观园 5952 + exam.json 607 + practice.json 1402 + bank_questions.json 827。**数一/数三的核对用本地参考库即可，不必联网**。
- 核心题库容器：`tools/yancai_bank.json`，status 三态：`transcribed`（视觉转写）/`ref-matched`（参考库精确匹配）/`needs-visual`（待核）。
- **exam.json 已知缺陷**：2003数二第11题选项 D 被写坏为 `$1>\dfrac{38}{15}>I_2>I_1$`，正确应为 `$1>I_2>I_1$`（核对大观园与答案 B 均可证）。

## 核心题库接入（2026-09-17 完成，commit f40f798）
- **`pwa/data/core_bank.json`**：数二核心题库 606 题（大观严选题），与 exam.json **同结构**（`[{id,year,title,sections:[{title,questions:[...]}]}]`），
  每题靠 `categoryIds:[catId]` 挂到同一棵 exam_categories.json 知识点树；题卡用 `q.source` 显示原真题题源。
- **分类页数据源切换**：`category.html` 顶栏 `#srcToggle` 按钮 + `js/category.js` 的 `applySrcMode()/toggleSrcMode()`，
  状态存 localStorage **`catSrcMode`**（`'exam'`=数二真题 / `'core'`=核心题库，默认 exam）。
  `buildEntries()` 只在 exam 模式合并 `bankItems`（大观园真题），core 模式不混入。
- **catId 映射方法（可复用）**：大观园「真题类」条目的 categoryIds 指向**年份节点**（如 42008）不可用；
  只有 `practice.json`/`bank_questions.json` 条目带**知识点** categoryIds。做法 = 把带知识点标签的 1435 条参考题
  当有标注语料，核心题在其中匹配取标签（`tools/_map_catid.py`）。三层兜底：语料匹配 → 关键词 → 数学记号 → 人工表。
- **⚠️ 大 JSON 一律紧凑单行**：`exam.json` / `practice.json` / `core_bank.json` 都是
  `json.dump(..., ensure_ascii=False, separators=(',',':'))`（无缩进、无空格）。用 `indent=1` 会产生上万行 diff。
  `exam_categories.json` / `bank_questions.json` 是 pretty-print，改这两个要沿用原格式。
- 核心题库生成/映射脚本：`tools/_gen_core_bank.py`、`tools/_map_catid.py`；源数据 `tools/yancai_bank.json`。

## 分类页新增开关与面板（2026-09-17，commit b0c8505）
- **「无标记优先」**：顶栏 `#unmarkedFirst` 开关，localStorage **`catUnmarkedFirst`**；排序统一走 `compareEntries()`
  （链路：无标记优先 → 收藏时间倒序 → 年份倒序），分类浏览与搜索共用。无标记 = 未收藏且未标不熟/不会。
- **「掌握地图」**：`pwa/js/mastery.js` + `pwa/css/mastery.css`（新文件，外壳复用 analysis.css 的 .an-* 结构）。
  掌握率 =（题数 − 不会 − 不熟）/ 题数；四态互斥计数；点色块本页 `selectCat` 跳转。
  **mastery.js 依赖 category.js 的全局变量，必须在 category.js 之后引入**。
- **CSS 变量白名单**（:root/.dark 实际定义的）：`--bg --bg-side --bg-hover --bg-active --text --text-dim
  --text-faint --accent --strong --border --shadow --mk-* --hl-*` 等。**没有 `--bg-card`**（曾误用导致暗色模式白底浅字）。

## 大观园题库的「核心/非核心」与「数二」口径（2026-09-18 查清）
- `assets/questions.json`（5952 题）字段含 **`core`**（核心/非核心）：`core=True` 669 条，`False` 5283 条。
- **数据里没有「数一/数二/数三」标记字段**；app 的科目筛选是**按考纲章节推导**：
  数二 = 高等数学(不含 级数/三重积分/线面积分/空间解析几何) + 线性代数全 + 数二真题。
  app 显示数二：全部 1690 / 高等数学 1064 / 线性代数 328。
- `assets/categories.json` 顶层键是 `{version,total,items}`，真实分类在 `items`（993 节点，含 totalCount）。
- ⚠️ 我们的 `pwa/data/core_bank.json`（606 题）来自 **PDF《大观严选题做题本》**，不等于大观园 `core=True`
  （实测只有 83/606 命中）。两者口径不同，别混用。
- **待办（用户挂起）**：等用户给「核心题」清单 → 再从 questions.json 里按标识（`serial`/`id`）筛选题目接入 PWA。

## 大观园题数口径精确还原（2026-09-24 查清，重要）
- **节点映射福音**：两库线代节点 **同 id 同名**——我们 `exam_categories.json` 的 45 个线代节点是大观园
  164 个节点的**子集**。导入时 catId 可直接复用；大观园深层节点（我们没有的）**沿父链上溯**到我们最近的节点。
- **截图「线性代数 327」= 真题库中「有真题溯源（source 含 `(YYYY 数X)`）+ 排除"数学一专项"(id=8)」的线代题**。
  实测复现 = 328，分布 [行列式30 矩阵78 向量45 线方75 特征值60 二次型40] 与截图逐项吻合（特征值差1=归类边界）。
- **数一/数三线代真题对数二有效**（线代考纲三科基本一致，数一仅多"向量空间"等专项）→ 大观园全数保留；
  我们原只有数二卷线代 191 → 对 328 缺 245（75%）。2026-09-24 已补**老年份(<=1999)** 109 道（70e148d）
  → `xd_bank.json` 370 题，真题模式线代 510 / 核心题库模式 478。
- 大观园 source 是**复合标注**（如 `(2000 数二；25版880 向量基础解答 4)` = 880 题溯源到数二真题）→
  判断"是否真题"要正则匹配年份+科目标记，不能只看是否含练习册关键词。
- app 科目筛选源码：`lib/controllers/app_controller.dart` L54-56（含"数二"或完全不含"数一/数三"）；
  数二不考章节根 id = `{1064 级数, 601 概率统计, 8 线代数学一专项}`（整棵子树剔除）。

## 记忆卡（cards.html，2026-10-02 挖空引擎 v3 定版，commit 5612cdd）
- **架构**：`notes.json`（32 篇）按 `##` 章节拆卡 → >1100 字二次拆 → 可挖空点 ≥2 为背诵卡（SRS）/否则阅读卡；
  状态存 `localStorage['cd_state_v1']`：`cards`(SRS) + `custom/over/hidden`(自建/编辑覆盖/删除隐藏，boot 时 applyStoredCards 回放) + `history`(近 120 天完成量) + `settings`。
- **挖空引擎（改规则必同步三处）**：`CLOZE_RULES`（文本节点 `$..$`→katex、`` `..` ``）+ `<strong>` 元素级候选 + `countClozeCandidates`。
  ⚠️ **公式正则下限必须 {1,}**：$x$/$n$ 单字符公式参与配对，否则 `$` 错位、两公式间中文被错配成伪公式（旧版 1109 处，降级后 17 处）。
  揭示按 `data-k` 分型：m→`katex.render`（texSafe 拦含中文无 \text{} 的答案降级纯文本）、b→`<b>`、c→纯文本。
  `stridePick` 均匀采样：长公式(≥3字符)优先 + 加粗补位≤2 + 单字符补位，额度上限 `settings.clozePerCard`(2~12, 默认 8)。
- **时序铁律**：`applyCloze` 必须在 `renderMath` **之前**（否则公式已成元素）；`renderMath` 在 applyCloze 之后跑（渲染未挖的公式）。
- **就绪态**：`.cd-actions.not-ready` 半透明但不禁用（grade() 拦截并提示还剩 N 空）；空格全揭示后立即点亮。
- **骨架自愈**：完成态/阅读完成态会 `cardWrap.innerHTML` 整体替换 → `ensureCard()` 用 boot 存的 `CARD_HTML` 快照还原，`updateFoot` 需判 `$('cardFoot')` 存在。
- **每日额度**：newDone/revDone 分开计数（新卡必须记 newDone，否则每日新卡上限失效）。
- 学习队列筛选 chips（全部/忘过的 lapses>0/不熟中/收藏）只作用于学习队列且不受额度限制；`injectDueCards` 把 10 分钟到期不会卡插回 qi+1。
- 测试脚本 `E:/workbuddy-data/binaries/node/workspace/_test_cards_v3.js`（31 项断言，**必须真加载 KaTeX**，v2 及更早的测试没加载、公式路径零覆盖）。

## hidden 属性 vs CSS display（2026-10-02 全站排查结论，重要铁律）
- **铁律**：元素 HTML 上带 hidden 属性时，对应 CSS **绝不能**再声明 display——
  作者样式的 display:flex 优先级高于 UA 样式表的 [hidden]{display:none}，hidden 会**完全失效**。
  凡靠 hidden 切换显隐的弹层/面板，必须补一条 [hidden]{display:none} 兜底。
- 项目既有正确写法：exam.css / category.css / notes.css 里都有 .bg-panel[hidden]{display:none}。
  记忆卡页曾漏抄（commit 61f0cf7 修复），症状＝「一进页面就弹空模态框 + 全屏遮罩点不动」。
- 排查脚本：_scan_hidden_conflict.js（扫全站 html 的 hidden 元素 × css 的 display 声明，精确 token 匹配）。
- **jsdom 测试盲区**：外链 link rel=stylesheet 在 jsdom 里不加载 → 纯 CSS bug 一律测不出。
  测试需把 css 内容内联成 style 标签，并用 getComputedStyle(el).display 断言；
  新增断言必须做**反向验证**（临时撤掉修复确认转红），否则可能是假阴性。

## 记忆卡 v4 铁律（2026-10-02 第二轮审查，commit 83709cd）
- **状态读写必须分家**：读用 `peekOf(id)`（返回 **Object.freeze** 的 DEF_CARD_STATE，不写 ST.cards），
  写才用 `stOf(id)`。否则渲染/列表/统计遍历全部卡片就会实例化 359 条默认状态，
  首次 saveState 写入 ~40KB 垃圾且此后每次操作重写全量。冻结是保险：严格模式下误写立刻抛错，
  否则会静默污染共享默认值 → 所有卡瞬间「已熟」。
- **两个队列共享 qi 时取当前卡必须按 mode 分流**：`queue[qi] || readQueue[qi]` 是陷阱
  （阅读模式 qi 在两队列都成立 → 收藏/已熟落到背诵卡上）。统一走 `currentCard()`。
- **卡片 id 绝不拼进内联 onclick**：章节名来自笔记正文，出现单引号/反斜杠会让属性提前闭合、按钮彻底失效。
  用 `data-act`/`data-id` + document 级事件委托（LIST_ACTS 映射）。
- 改 `countClozeCandidates` 的候选规则必须与 `collectCands`（实际挖空）**共用同一组长度常量**，
  否则出现「判为背诵卡却挖不出空」的退化卡（曾因加粗上限 40 vs 60 导致 10 张卡偏差）。
- **⚠️ 禁止按行号批量替换 JS**：曾用脚本按 grep 行号把 16 处 stOf→peekOf，3 处写路径被误换。
  批量改动后必须：① 静态扫描（只读函数后 N 行内出现写赋值即报警）；② 逐处人工复核；③ 反向验证。
- 测试用 `_test_cards_v4.js`（6 组独立场景、各自 seed 注入、45 项断言）。**每个场景独立 makeDom(seed)**——
  同一 origin 的多个 jsdom 实例会共享 localStorage，场景间会互相污染（v3 因此出现假失败）。
- **jsdom 不实现 UA 的 [hidden]{display:none}**：依赖该规则的元素只能断言 `hidden` 属性；
  CSS 里写了显式 `[hidden]` 规则的才能断言 getComputedStyle().display。别把前者误判成产品 bug。

## ⚠️ 三类「内容凭空消失」bug（2026-10-02 挖空重做时发现，影响记忆卡+笔记页）
1. **HTML 引用死链 → 公式全不渲染**：`cards.html` 写 `vendor/auto-render.min.js`，实际在 `vendor/katex/`。
   `renderMathInElement` 未定义 → `renderMath()` 静默 return → 全站公式显示原文。
   - 排查脚本 `_scan_deadrefs.js`（扫全站 html 的 src/href + js 里的 fetch json 是否存在）。
   - **测试教训**：harness 手动 eval 依赖文件会**掩盖** HTML 引用错误。必须按 HTML 里真实
     `<script src>` 顺序读本地文件、拼成一个函数体执行（分文件 eval 会作用域隔离，cards.js 看不到 mdToHtml）。
2. **emitList 跳级缩进丢弃整段列表**（`mdrender.js` 与 `reader.js` 两份副本必须同步改）：
   `if (items[i].level > level) { i++; continue; }` 会**丢内容**。笔记里「首项比后续缩进更深」很常见。
   正解：以实际层级递归接管；顶层入口用本段最小 level 作起点，不要写死 0。
3. **renderTipsBlock 丢 rest**：四段标签（公式/易错/技巧/注意）之外的行必须**追加**渲染，
   写成「仅当 inner 为空才用 rest」会导致识别到任意一段就把其余内容全丢。
4. **KaTeX auto-render 跨元素配对**：`$`/`$$` 落单（奇数个）时会把中间整段文字吞进 display 公式。
   拆卡必须保证每张卡的 `$` 配平：`$$…$$` 独占行当原子块；句子切分只用 `。；！？`（逗号会切坏 `$a,b$`）；
   输出前 `isBalanced()` 校验 + `stripLoneDollar()` 修复（同行 `$$x$$` 自动转行内 `$x$`）。
   - 回归断言：揭示全部答案后逐中文片段核对渲染文本（**比对前排除图片 alt / HTML 注释 / `#` 一级标题，否则全是误报**）。

## 线代 346 题库与答案册（2026-10-06）
- **答案册**（用户资料，63MB/496页）：`D:/cjx/下载/QQ FileRecv/线性代数_真题+重点题_答案册（含目录与页码）.pdf`。正文答案区是**位图**（无文字层、无本机 OCR），只能视觉识别；文字层仅含「题号/来源/页码」。书末有**补充题 补01—补39**（p446-496，手写体）。
- **⚠️ 两套编号不是同一套**：`xd_bank.json` 的 `pdfNo` 按**章节顺序**（行列式1-30/矩阵31-108/向量109-153/方程组154-228/特征值229-287/二次型288-346）；PDF 的 001—346 按**35 天计划**排（目录 A-F 段区间与章节一致但**段内顺序不同**）。**别拿 pdfNo 当 PDF 题号**，会产生整片「题干对不上」的假警报。可靠对应：目录 A-F 分组→章节→再按「年份+科目」归一化。
- **结论**：正文 346 道库内一道不缺；补充题 39 道已全部导入，现共 **385** 道（no 用 `SUP01`—`SUP39`）。答案册自身错误：补10 的 `A^*` 印错（已用 `AA^*=|A|E` 判伪并改正）。
- **新格式标准**（用户 2026-10-05 定，后续所有新增/重写题一律照此）：`answer` = 【答案】最终答案 + 空行 + 【分析】+【解】分步 + ⚠️易错 N 条；`idea` = **对整体解析的概括**（2~4 句，可用 `**思路概括：**` 前缀）。
