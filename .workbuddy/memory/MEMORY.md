# math-note 项目长期记忆

## 一、构建与部署铁律
- **新增任何数据文件必须同步加入 `pwa/sw.js` 的 `PRECACHE`**，否则 SW 不缓存、用户刷不到。改完跑 `python tools/build_sw.py` bump `CACHE_VER`；pre-commit 钩子（`.githooks/pre-commit`）自动调用并 `git add pwa/sw.js`（前提 sw.js 在暂存区）。`js/common.js` 已自动重载 + 弹「发现新版本」条，无需用户手刷。
- **hidden 铁律**：元素带 `hidden` 属性时，对应 CSS 绝不能声明 `display`——作者样式 `display:flex` 压过 UA 的 `[hidden]{display:none}`，hidden 完全失效。靠 hidden 切显隐的弹层必须补 `[hidden]{display:none}` 兜底（`.bg-panel[hidden]` 写法正确）。排查脚本 `_scan_hidden_conflict.js`。
- **jsdom 盲区**：外链 css 不加载 → 纯 CSS bug 测不出，需内联 style 并断言 `getComputedStyle`；jsdom 不实现 UA 的 `[hidden]{display:none}`，只能断言属性本身。新增断言必须**反向验证**（撤掉修复要转红），否则是假阴性。

## 二、数据资产（pwa/data/）
| 文件 | 内容 | 谁加载 |
|---|---|---|
| `exam.json` | 数二真题 27 卷 607 题 | exam.js + category.js |
| `core_bank.json` | 核心题库（大观严选题）741 题 | category.js（core 模式） |
| `dgy_items.json` | 大观园 900/880/姜晓千习题 1346 题 | category.js（exam 模式） |
| `xd_bank.json` | 线代重点题 333 题 | category.js |
| `bank_questions.json` | 大观园真题 827 题 | category.js |
| `notes.json` | 讲义笔记 33 篇 | notes.html / cards.html |
| `exam_categories.json` | 分类树，dict 以 id **字符串**为键，level 0/1/2 | — |

- `practice.json` 是**死数据**（`grep -r practice.json pwa/` 无结果）。
- **大 JSON 一律紧凑单行**：`exam.json`/`practice.json`/`core_bank.json` 用 `json.dump(..., ensure_ascii=False, separators=(',',':'))`；`exam_categories.json`/`bank_questions.json` 是 pretty-print，改这两个沿用原格式。
- qid = `<卷id>-<题号>`；`qidOf()` 会经 `linkedQid`（`xd-N`/`core-N` → 真题 qid）重定向，统一收藏/笔记键。
- **四态口径**（mastery.js）：不会 > 不熟 > 已掌握（显式 `mastered` 或已收藏且无薄弱标记）> 未刷。
- localStorage：`examFav` `{qid:{t:ms}}`、`examStatus` `{qid:'unknown'|'unfamiliar'|'mastered'}`、`examNote-<qid>`、`catSrcMode`、`catUnmarkedFirst`。
- ⚠️ `bank_questions.categoryIds` 全为**字符串**（827/827），其余题库是数字；渲染器用 `String()` 兜过，暂未改。

## 三、笔记页（notes.html / reader.js）
- 结构 `{id,subject,order,name,title,chapters[],md}`；**`chapters` 驱动右侧目录，`md` 里 `##` 按序编号 `ch-0/ch-1`…两者必须手工同步**（新增 `##` 必须同步插 `chapters`）。
- `inline()` 只支持 `**bold**`、`![img](src)`、`[text](#anchor)`、`⭐`；链路 `emitList→breakLines→inline`。
- ⚠️ `emitList` 跳级缩进会**丢整段列表**（`if(items[i].level>level){i++;continue}`）：笔记里「首项比后续缩进深」很常见。正解=按实际层级递归接管，顶层用本段最小 level 作起点。`mdrender.js` 与 `reader.js` **两份副本必须同步改**。
- ⚠️ `renderTipsBlock` 丢 rest：四段标签（公式/易错/技巧/注意）之外的行必须**追加**渲染；写成「仅当 inner 为空才用 rest」会把其余内容全丢。
- ⚠️ KaTeX auto-render **跨元素配对**：`$` 落单（奇数）会把中间整段文字吞进 display 公式。每张卡 `$` 必须配平；`$$…$$` 独占行当原子块；切句只用 `。；！？`（逗号会切坏 `$a,b$`）；输出前 `isBalanced()` + `stripLoneDollar()`。
- 笔记正文的**结构关键词加粗**（必要条件/充分条件/性质/定义/定理…）由脚本批量生成；规则：不吞相邻词、不拆词（≤8 字）、禁动词字、**合并相邻加粗块**（否则出 `***`）。

## 四、跨页重复副本（改一处必同步另一处）
`exam.js` 与 `category.js` 有重复实现：`mdBlockWithImg` / `fillExamNoteImgs` / `zoomAnsImg` / `mdBlock` / `qCard`vs`catCard` / `.q-note` 双框逻辑。
- **KaTeX**：答案/思路段初始 `hidden`，展开（`toggleQSec`/`toggleAllAnswers`）后**必须补调 `renderMath` + `fillExamNoteImgs`**。
- **mdBlock 裸 `$$` 坑**：`'$$'.endsWith('$$')` 恒真，独占一行的 `$$` 必须显式放行开块（`(!l.endsWith('$$') || l === '$$')`）。
- **笔记双框**：`hasImg = /\[图:[a-z0-9]+\]/.test(note)` 才给 `.q-note` 加 `.has-img`；纯文字靠 `.q-note:not(.has-img) .q-note-preview` 去框。
- **样式副本易漏**：`.all-ans-btn` 只在 category.css 写过 → exam.css 缺失、按钮不可见。跨页共用组件样式要在每个 css 都写。
- **CSS 变量白名单**：`--bg --bg-side --bg-hover --bg-active --text --text-dim --text-faint --accent --strong --border --shadow --mk-* --hl-*`。**没有 `--bg-card`**（曾误用致暗色模式白底浅字）。

## 五、笔记编辑器（contenteditable，踩坑重灾区）
- **编辑器 DOM 就是数据载体**：贴图后 blob 异步压缩写库（几百 ms），保存前必须 `await waitPendingImgs()`（`_pendingImgTasks`）。
- `fillExamNoteImgs` 在**编辑态**取不到 blob 时**绝不 replaceWith 文本**（会丢 `[图:id]` → 孤图清理删 blob → 图永久丢失），只标 `.img-fail` 占位；**仅只读态**才可替换成「图片已丢失」。
- 三条保存路径：`saveNoteBtn` / `toggleNoteEdit` 完成分支 / `saveNoteFromOps`。
- **富文本令牌**（存 localStorage，天然防 XSS：`mdInline` 先 `esc()` 再只还原白名单）：`[图:id]`、`<c:#rrggbb>…</c>`、`<h:#rrggbb>…</h>`、`<b>`/`<i>`、`<h1>`/`<h2>`（块级，独占整行）。`editorToNote`/`noteToEditor`/`mdBlock` **三处都要识别全令牌集**。
- H1/H2 用 `execCommand('formatBlock', false, 'H1')` 且**禁用 styleWithCSS**，否则退化成 `<span style>`。

## 六、数据修复铁律（LaTeX / JSON）
- ⚠️ **单行紧凑 JSON 必须 `json.loads` → 改 dict → `json.dumps` 写回**：Edit 工具会被参数转义把 `\\` 吃成 `\`，产出 JS `JSON.parse` 拒绝的非法 JSON（python 宽松可过、前端必炸）。
- ⚠️ **禁止 inline `python -c` 做反斜杠/正则/JSON 的 exam.json 修改与验证**：Bash 双引号层层吃反斜杠。**必须写 .py 脚本文件执行**，每轮改完用独立 .py 全量验证。
- **r-string**：`r"\\X"` = 单反斜杠 `\X`；要双反斜杠用 `r"\\\\X"`。
- 修复字段要**遍历 `q.keys()` 全覆盖**（含 `q.tips` 的 gs/jq/yc/zy 四类子键），别硬编码 `['stem','answer','idea']`。
- **LaTeX 填空规范**：统一 `\underline{\hspace{2cm}}`；纯文本处必须包 `$...$`；`$$` 块内必须裸写。合法下标 `\int_0`/`|a_n|` 严禁被误伤（只匹配连续 3+ 个 `\_`）。
- **验证三件套（tools/ 永久保留）**：`_deep_validate.py`（分隔符配平+双转义+污染）、`_audit_latex.py`（结构回归）、`_scan_unpaired.py`（跨行 `$`）。数据改动后三个全跑。
- 数据修复必须走 commit（pre-commit bump CACHE_VER）+ push 闭环；中间损坏版本可能已被 SW 缓存。

## 七、分类页
- **双数据源**：顶栏 `#srcToggle` → `applySrcMode()`/`toggleSrcMode()`，状态存 `catSrcMode`（`'exam'`/`'core'`，默认 exam）。`buildEntries()` 合并 `bankItems` + `dgy_items` + `xdItems`，靠 `qid#catId` 去重。
- **「无标记优先」**：`#unmarkedFirst` → `catUnmarkedFirst`；排序统一走 `compareEntries()`（无标记优先 → 收藏时间倒序 → 年份倒序），浏览与搜索共用。
- **「掌握地图」** `js/mastery.js` + `css/mastery.css`；**必须在 category.js 之后引入**（依赖其全局变量）。
- **「💡建议」** `js/advice.js` + `css/advice.css`（顶栏按钮，核心题库刷题建议）。两套口径：薄弱=全库加权标记（不会×2+不熟，按 qid 去重）；待刷=core_bank 未掌握。排序 `b.w-a.w || b.todo-a.todo || a.id-b.id`（薄弱优先，让该列单调递减）。`advJump` 会先切 core 模式。
- **跨库去重**：`normStem()`（只去 LaTeX **结构**符号，**保留公式内容**——用占位符替换 `$...$` 会毁信息致短题干误配）+ bigram Jaccard。`bank_questions` 19 处重复靠精确题干去重，**不要放宽 source 正则**（实测会误藏 563 道真改写题）。
- 分类器做多级时**先定父级再在父级内分子级**，别把子级关键词全局平铺。
- 历史：大观园多级分类（`catLink` 向上归并 / L0~L8 完整树）做过两版后**用户要求退回**三级（73 节点）。

## 八、核心题库 / 线代题库
- `core_bank.json` 与 exam.json **同结构**，每题靠 `categoryIds:[catId]` 挂到同一棵分类树；题卡用 `q.source` 显示真题题源。catId 映射脚本 `tools/_map_catid.py`（拿带知识点标签的参考题当语料匹配，三层兜底：语料→关键词→数学记号→人工表）。
- **新格式标准（2026-10-05 定，所有新增/重写题照此）**：`answer` = 【答案】最终答案 + 空行 + 【分析】 + 【解】分步 + ⚠️易错 N 条；`idea` = 对整体解析的**概括**（2~4 句，可用 `**思路概括：**` 前缀）。
- **线代答案册**（用户资料，63MB/496 页）：`D:/cjx/下载/QQ FileRecv/线性代数_真题+重点题_答案册（含目录与页码）.pdf`。正文答案区是**位图**（无文字层），只能视觉识别；书末有**补充题 补01—补39**。
- ⚠️ **`pdfNo` ≠ PDF 题号**：`pdfNo` 按章节顺序（行列式1-30/矩阵31-108/向量109-153/方程组154-228/特征值229-287/二次型288-346）；PDF 按 35 天计划排（段内顺序不同）。**别拿 pdfNo 当 PDF 题号**，会产生整片假警报。可靠对应：目录 A-F 分组→章节→「年份+科目」归一化。
- 用户口径：**只刷核心题库**，统计/建议一律只看 `core_bank.json`。
- exam.json 已知缺陷：2003 数二第 11 题选项 D 应为 `$1>I_2>I_1$`。
- 大观园源库 `assets/questions.json`（5952 题，有 `core` 字段；**没有**数一/二/三标记，app 按考纲章节推导）。大观园线代节点与我们**同 id 同名**（我们是其子集），catId 可复用，深层节点沿父链上溯。
- 大观严选题 PDF 有**文字层**（重排版非扫描），可做字符级校验，不能替代视觉还原；快照 `tools/_yancai_textlayer.json`。

## 九、记忆卡（cards.html，挖空引擎）
- 架构：`notes.json` 按 `##` 拆卡 → >1100 字二次拆 → 可挖空点 ≥2 为背诵卡（SRS）/否则阅读卡；状态存 `localStorage['cd_state_v1']`。
- **挖空规则改一处必同步三处**：`CLOZE_RULES`（文本节点 `$..$`→katex、`` `..` ``）+ `<strong>` 元素级候选 + `countClozeCandidates`（必须与实际挖空**共用同一组长度常量**，否则出「判为背诵卡却挖不出空」的退化卡）。
- ⚠️ 公式正则下限必须 `{1,}`（`$x$`/`$n$` 单字符要参与），否则 `$` 错位、两公式间中文被错配成伪公式。
- **时序铁律**：`applyCloze` 必须在 `renderMath` **之前**。
- **状态读写分家**：读用 `peekOf(id)`（返回 Object.freeze 的默认值，不写 ST.cards），写才用 `stOf(id)`；否则遍历即实例化 359 条状态、写出 ~40KB 垃圾。⚠️ **禁止按行号批量替换 JS**（曾误换 3 处写路径）。
- 两个队列共享 qi：取当前卡必须按 mode 分流（统一走 `currentCard()`）。
- 卡片 id **绝不拼进内联 onclick**（章节名含引号会闭合属性）→ 用 `data-act`/`data-id` + 事件委托。
- 完成态会整体替换 `cardWrap.innerHTML` → `ensureCard()` 用 boot 存的 `CARD_HTML` 快照还原。
- 每日额度 newDone/revDone **分开计数**。
- 测试 `_test_cards_v3.js` / `_test_cards_v4.js`（**必须真加载 KaTeX**；每场景独立 `makeDom(seed)`，否则同 origin 共享 localStorage 互相污染出假失败）。

## 十、历史教训（别再犯）
- **HTML 引用死链 → 公式全不渲染**：`cards.html` 曾写 `vendor/auto-render.min.js`（实际在 `vendor/katex/`）→ `renderMathInElement` 未定义 → `renderMath()` 静默 return。排查脚本 `_scan_deadrefs.js`。**测试要按 HTML 里真实 `<script src>` 顺序拼成一个函数体执行**（分文件 eval 会作用域隔离）。
- 题库交叉比对（mathnote-bank-compare skill）**只覆盖题库里有的题**，未收录的需人工或联网核卷。
- 「条件不足/待核」往往不是真条件不足，而是**题面抄错**，先核对真题原貌再下结论。
