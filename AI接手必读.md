# AI 接手必读 · math-note

> **这份文档写给下一个接手的人/AI。** 目标：读完这 300 行，能直接干活且不踩历史坑。
> 数据字段细节、源站抓取接口看 **`网站说明.md`**（那份是"数据字典 + 抓取手册"）；
> 本文是"**约定、规则、状态**"——即那些"不看就会做错"的东西。
>
> 最后更新：2026-11-03 ｜ 线上 `CACHE_VER = mathcards-ebb2edc377`

---

## 0. 30 秒速览

| 项 | 值 |
|---|---|
| 是什么 | 个人**考研数学（数二）**复习站：32 篇笔记 + 1113 道核心题库 + 27 套真题 |
| 形态 | 纯静态 PWA，**无后端**；收藏/标记/笔记/批注全在浏览器本地 |
| 线上 | `https://cyrusssxx.github.io/math_learn/pwa/` |
| 仓库 | `github.com/Cyrusssxx/math_learn`，分支 `main`，站点根目录 `pwa/` |
| 发布 | `git push` 即发布；pre-commit 自动重算 `?v=` 和 `CACHE_VER` |
| 主力页面 | `category.html`（核心题库）> `index.html`（笔记）> `exam.html`（真题） |

三条命令（改完必走）：

```bash
cd pwa && python -m http.server 8080          # 本地看效果（必须 http，file:// 会被 fetch 拦）
node tools/_check_core_bank.js                 # KaTeX / 考纲 / 结构
git add -A && git commit -m "..." && git push origin main   # 发布
```

---

## 1. 用户是谁、怎么用

- 考**数二**（不考数一），PC 为主、手机偶尔。
- **主力是「核心题库」**（分类页左上角 `📘 核心题库 ⇄ 📝 真题` 切换，默认核心题库）。
  真题模式、大观园模式不是主战场——涉及题库的改动优先保证核心题库的体验与数据正确。
- 他在意四件事，按优先级：
  1. **分支归属必须和源站一致**（他是按"位置"记题的，静默移动一道题 = 让它消失）
  2. **思路要好读**（①②③ 逐行，不是散文）
  3. **题源/题号准确**（他会核对）
  4. **首屏快、图片快**
- 沟通偏好：**直接给结论 + 可执行步骤**，少铺垫；不要"好的我来帮您"这类客套。
  涉及删数据/改结构，先列清单再动手。

---

## 2. 代码与数据地图

### 页面 → 文件

| 页面 | 作用 | 主 JS |
|---|---|---|
| `pwa/index.html` | 笔记站（三栏：目录树 / 正文 / 本页目录） | `reader.js` + `annotate.js` + `mdrender.js` |
| `pwa/category.html` | **主力刷题页**：分类树、掌握地图、拼卷、复测 | `category.js` |
| `pwa/exam.html` | 按套卷刷真题（27 套，计时 + 答题卡） | `exam.js` |
| `pwa/fav.html` | 收藏汇总 | `fav.js` |
| `pwa/cards.html` | 挖空记忆卡 | — |
| `pwa/selected.html` / `good.html` | 选填专项 / 好题集 | — |

### 关键 JS 职责

| 文件 | 负责什么 |
|---|---|
| `category.js` | 分类树、题卡渲染 `catCard`、答案页签 `ansTabsHtml`、拼卷 `pp*`、原图预热 `ansWarm*`、后台数据 `loadExamSources` |
| `reader.js` | 笔记渲染、两级目录（章 `##` + 小节 `###`）、滚动高亮 `highlightToc`、图片灯箱 |
| `annotate.js` | 批注/荧光（锚点 = `笔记id#块序号`）、笔记编辑器 |
| `common.js` | 共享：`hlBg()`、`hlLine()`、`zoomOverlayOpen()` |
| `mdrender.js` | Markdown → HTML（含 `breakLines` 断行规则） |
| `sw.js` | Service Worker 缓存策略 |

### 数据文件（`pwa/data/`）

| 文件 | 大小 | 内容 |
|---|---|---|
| `core_bank.json` | 2.37 MB | **1113 题**（高数 759 + 线代 354），主力数据 |
| `exam.json` | 1.20 MB | 27 套数二真题（2000–2026），607 题 |
| `notes.json` | 0.38 MB | **32 篇笔记的唯一权威**（没有 md 源文件） |
| `cat_deep.json` | 0.05 MB | 知识点细分类树 `{nodes:{id:{n,p}}}` |
| `exam_categories.json` | 0.02 MB | 章节骨架（level 0 学科 / 1 章 / 2 节） |
| `bank_questions.json` / `dgy_items.json` | 0.74 / 2.33 MB | 大观园补充题 / 条目 |
| `data/img/` | **194 MB** | 题干图 + 原图解析（`ansImg` 共 514 张 / 140 MB） |

### 核心题库分节（改数据前先认准节名）

```
高数 759：极限168 / 一元微分150 / 一元积分200 / 多元微分85 / 二重积分64 / 微分方程92
线代 354：行列式40 / 矩阵75 / 向量31 / 线性方程组73 / 特征值64 / 二次型71
```

---

## 3. 数据模型：4 个必须先懂的概念

### ① `qid` —— 收藏 / 标记 / 笔记的主键

```
qidOf(paperId, no) = `${paperId}-${no}`
核心题库题若带 linkedQid → 直接用 linkedQid
```

**`linkedQid` 一改，收藏/标记/笔记就换抽屉**。改链接必须同时迁移旧键
（`category.js` 的 `migrateCoreLegacyKeys()`：目标为空才搬，不覆盖）。

| 数据 | 存储 | 键 |
|---|---|---|
| 收藏 | localStorage | `examFav` |
| 掌握/不熟/不会 | localStorage | `examStatus` |
| 做题笔记 | localStorage + IndexedDB(图片) | `examNote-<qid>` |
| 笔记批注/荧光 | localStorage | `笔记id#块序号` |

### ② 两套分类，别混

- **节**（`core_bank.sections[].title`）= 书本编排（行列式/矩阵/向量/…）
- **分类树**（`cat_deep` + `exam_categories`）= 知识点语义（矩阵/秩/求秩）
- 线代自 2026-10-26 起已按站点对齐，两者基本一致。

### ③ `srcOrder` = 书上题号，才是真身份

线代臻选题在书上有编号 `#001–#355`，`srcOrder` 就是它，`ansImg` 文件名按它命名。

> **图片永远可信，题干可能是串的**（历史录入事故）。

⚠️ 高数各节也有自己的 `srcOrder`（1..N），会和线代 1..355 撞号——全库比对只能取线代节。

### ④ 「未细分」不是 bug

题挂在"有子节点的中间节点"上，站点本身如此，`_final_verify.js` 报出来不用管。

---

## 4. ⛔ 硬规则（违反会出事故）

### R1 分支归属一律以源站为准

- 核心题库的 `deepCats` / `categoryIds` **必须与 `cxyonly.fans` 完全一致**。
- **禁止**凭"语义更合理"自行调整。发现可疑 → **先报清单**（题号/现分支/建议/依据），用户确认后才动。
- 唯一例外：**题型 `kind`** 可以按数据修正，分支不行。
- 2026-10-29 全量核对：**354/354 与站点一致**（本地把"线性方程组"改名"方程组"，比对时归一化）。
- 顺序也跟站点：`exam_categories.json` 每个节点带 `ord`，`buildTree` 按 `ord` 升序（不是按题数）。

### R2 只写数二考纲内的东西

**禁用词**（用户原话："我不学数一，只学数二，向量空间什么都不会"）：

`ker` / `Im` / `span` / `Col` / `dim` / `⊆` / `N(A)` / `R(A)` / 子空间 / 特征子空间 /
`Jordan` / 若尔当 / 广义特征向量 / 正交补 / 张成 / 幂零 / Cayley-Hamilton / Schur 补 /
相似标准形 / 酉 / 直和 / 商空间

**替代写法**：

| 别写 | 写成 |
|---|---|
| $\ker A$ | 「$Ax=0$ 的全部解 / 基础解系」 |
| $\dim\ker A$ | 「基础解系含 $n-r(A)$ 个向量」 |
| $\operatorname{Im}B$、$\operatorname{Col}(B)$ | 「能由 $B$ 的列向量组线性表示」 |
| $\operatorname{span}\{\alpha\}$ | 「$\alpha$ 的全部倍数 $k\alpha$」 |
| $X\subseteq Y$ | 「……的解都是……的解」 |
| 正交补 | 「与它垂直的方向 / 全体向量」 |
| 特征子空间 | 「属于 $\lambda$ 的特征向量 / $(\lambda E-A)x=0$ 的基础解系」 |
| Cayley-Hamilton | 「$A^2-(\operatorname{tr}A)A+\lvert A\rvert E=O$（按元素验证）」 |

唯一保留：**谱分解**（用户明确认可）。
⚠️ 「奇异值」是另一个词（$A^{\mathrm T}A$ 的特征值开方），别拿来表示「$|A|=0$ 的根」。

### R3 思路（idea）的写法

```
**思想：<一句话方法名>**——<关键一步>。
① 用什么工具 + 关键一步；
② ……
③ ……（多小问题目：小问数 = 段数，每问都要有）
```

- **必须**①②③ 逐行，**不要**纯叙述散文（2026-10-29 用户否决过一次，已回退）。
- 长度 150–220 字；「别太简洁了，关键步骤要有」。
- 每题 1–2 处 `**加粗**`，标在"题眼"和"转折点"，不要通篇加粗。
- 首行「思想」是 2026-10-31 起的新规范，线代 4 章已铺（见 §9 进度）。

### R4 笔记正文**中间不能插块**

- 批注/荧光锚点 = `笔记id#块序号`（`annotate.js keyBlocks()` 按所有 `li/p` 的**顺序下标**编号）。
- 在中间插一个 `li/p` → 后面所有块平移，而 `migrateKeys` 只认旧版文本哈希键，
  **平移后的序号仍然"有效"** → 荧光/批注**静默挂到错误段落**。
- 安全做法：新增章节**追加到该篇末尾**；只插 `###` 标题是安全的（不是 li/p）。
- 真要插中间，必须先写 sid 重映射，并跑 `tools/_snap_note_blocks.py before|after` 对比。

### R5 改 JSON 的缩进不能变

| 文件 | 缩进 | 命令 |
|---|---|---|
| `core_bank.json` | **1 空格** | `JSON.stringify(obj, null, 1)` |
| `notes.json` | 2 空格 | `JSON.stringify(obj, null, 2)` |

曾用 `null, 2` 重写 core_bank → 全文件重排、白涨 **274 KB**（2.45MB → 2.73MB）。

### R6 不要手写 `?v=`、不要改 `CACHE_VER`

`.githooks/pre-commit` 自动做：`tools/build_assets_ver.py` 重算所有 `?v=`、
`tools/build_sw.py` 生成新 `CACHE_VER` 并暂存 `pwa/sw.js`。

### R7 改完必须三件事

1. 跑检查脚本（§7）
2. `git push`
3. **抓线上复核**（不能只看本地文件）——`CACHE_VER` + 目标文件关键字

---

## 5. 发布与缓存机制

### Service Worker（`pwa/sw.js`）

| 资源 | 策略 | 说明 |
|---|---|---|
| `data/*.json` | **network-first** | 改 JSON 刷新即生效，不用等换版 |
| HTML/JS/CSS | cache-first | 靠 `CACHE_VER` 换代 |
| `data/img/*` | cache-first，独立 `IMG_CACHE = 'mathcards-img-v1'` | **换代不清**，否则每次发版重下 190MB |

### 首屏瘦身（2026-10-31）

`loadExamSources()` 把 `exam.json` / `bank_questions.json` / `dgy_items.json`（共 4.2MB）
改成**首屏之后**再加载（幂等 Promise）。首屏 10.1s → 2.07s。

⚠️ 副作用：拼卷 `_ppIdx` 在数据到齐前是空的 → 曾误报「这道题已不在题库里」。
修法：数据到了 `_ppIdx = null` 强制重建，并显示「⏳ 正在加载真题数据…」。

### 原图解析的加载策略

1. 题卡渲染时 `<img>` **只挂 `data-src`**，一张图都不拉。
2. 点「查看答案」→ `preloadAnsImgs()` 把 `data-src` 换 `src` **并改 `loading="eager"`**
   （`display:none` 祖先里的 `lazy` 图**永远不会触发**）。
3. 「展开全部答案」只给**当前可见**的页签挂 src（514 张/140MB 不能全拉）。
4. 正文渲染完后**预热前 20 张**（`ansWarmFromDom`），三级门禁：
   `window load` → 后台 JSON 到齐 → `requestIdleCallback`；
   串行 + `new Image()` 不进 DOM + 每个列表只热一次 + 切列表 token 作废。

### 拼卷规则（`ppWeight`）

```
不会 4 : 不熟 2 : 仅收藏 1 : 掌握 0（排除）: 无标记 0（只做兜底）
```
外加：软衰减、7 天内不重复、尽量分散到不同细分支、题量可调（默认 22）。
**真题不加权**（用户 2026-10-30 明确否掉过一版"真题优先"，已回退）。

---

## 6. 题库内容生产规范

### 答案

- 多小问必须分段 `（1）…（2）…`（文字版答案尤其）。
- 可用 `**加粗**` 和 `==半高亮==`（`mdInline` 支持，渲染成 `mark.ans-hl`，淡黄半高 + 下划线）。
- `mark.ans-hl` 的颜色**写死在 `exam.css`**，不跟用户荧光笔变量走（否则和笔记高亮撞色）。

### 点睛（`tips`）四段

| 键 | 标签 | 写什么 |
|---|---|---|
| `gs` | 📌 公式 | 本题要用的公式/结论 |
| `yc` | ⚠️ 易错 | 最容易错的一步 |
| `jq` | 💡 技巧 | 更快的做法 |
| `zy` | 🔍 注意 | 边界条件、可逆性、前提 |

### 题源（`source`）格式

```
2026数二三（二16、三15）      ← 年份题源：无外层括号，题号进全角括号
2020数二（第22题）
880二次型综合选择（第1题）    ← 书代号用 880/900，不写 0.88k / 0.9k
25李艳芳三套数二第三套        ← 套卷：年份+老师+套数+科目+第几套
姜晓千真题同源150
```

### 两个固定模板

**A. 「求 $P$ 使 $P^{-1}AP=B$」= 两次对角化再传递**

$$A=P_1\Lambda P_1^{-1},\quad B=P_2\Lambda P_2^{-1}\ \Longrightarrow\ P=P_1P_2^{-1}$$

思路首行写「**思想：两次对角化再传递**」，答案分三步：写两式 → 取 $P=P_1P_2^{-1}$ 代入 → 验 $|P|\ne0$。
（$B$ 不可对角化的题，如 1312/1321，只能用不了传递，改按 $AP=PB$ 逐列解。）

**B. 谱分解（实对称专用）**

$$A=\lambda_1\gamma_1\gamma_1^{\mathrm T}+\lambda_2\gamma_2\gamma_2^{\mathrm T}+\lambda_3\gamma_3\gamma_3^{\mathrm T}$$

$\gamma_i$ 单位正交；每个 $\gamma_i\gamma_i^{\mathrm T}$ 是投影矩阵（$P_i^2=P_i$、$P_iP_j=O$、$\sum P_i=E$）；
**已知某些方向上的作用时只写那几项，其余用 $E$ 补**。
已覆盖 8 道：1011 / 1018 / 1152 / 741 / 1161 / 1171 / 1329 / 1330。

---

## 7. 验证纪律（不要凭肉眼判断）

```bash
node tools/_check_core_bank.js   # KaTeX 解析 / 考纲外词汇 / 结构
node tools/_final_verify.js      # 未细分 / 未知节点 / 空 deepCats
```

基线：**KaTeX 报错 0、结构问题 0、未知节点 0、空 deepCats 0**；「未细分」允许非 0；
考纲外命中当前 53 处（历史遗留，改动不应让它增加）。

| 场景 | 怎么验 |
|---|---|
| 公式渲染 | Playwright 打开页面，数 `.katex-error` 必须是 0 |
| 数学结论 | **numpy 验算**（特征值、行列式、$P^{-1}AP$、$P^{\mathrm T}P$ 等），不要手算 |
| 笔记改动 | `tools/_snap_note_blocks.py before` / `after` 对比 `li,p` 文本序列，必须完全一致 |
| 目录跳转 | 点小节 → 标题 `top≈20px`、`active` 高亮正确、hash 变化 |
| 线上是否生效 | `curl` 抓 `sw.js` 的 `CACHE_VER` + 目标文件关键字（加 `?cb=$RANDOM` 破缓存） |

Playwright 已装在 `D:/python`（`D:/python/python.exe`），起本地服务再跑。

---

## 8. 已知坑（按踩过的顺序）

| # | 坑 | 症状 | 正确做法 |
|---|---|---|---|
| 1 | `categoryIds` 写成**章**级 id | 整节题从分类树**彻底消失** | 必须 `level===2` 的节级 id |
| 2 | `notes.json.chapters` 与 md 的 `## ` 不一致 | 左目录与右目录错位 | 改内容后同步 `chapters` |
| 3 | 笔记中间插块 | 荧光/批注**静默挂错段落** | 只追加到篇末（见 R4） |
| 4 | 多行公式用单个 `$` | KaTeX 解析失败、显示原始 LaTeX | 跨行一律 `$$…$$` |
| 5 | `display:none` 里的 `loading="lazy"` | 图片永不加载，点开才现下 | 挂 src 时同时改 `eager` |
| 6 | `JSON.stringify(obj,null,2)` 重写 core_bank | 全文件重排、白涨 274KB | `null, 1` |
| 7 | 同特异性 CSS 状态类顺序 | ⭐ 小节被选中**不变蓝** | `.is-key.active` 单独提特异性 |
| 8 | `highlightToc` 用 `activeH3 === ''` 才展开 | 滚到某章目录不收/不开 | 命中章**或**章内小节 → 必开；锁定期只加不减 |
| 9 | 折叠块（`details`）里标题 rect 全 0 | 高亮跑到别的章 | 跳过 `getBoundingClientRect()` 宽高为 0 的标题 |
| 10 | `linkedQid` 改了没迁旧键 | 收藏/标记/笔记"消失" | 跑 `migrateCoreLegacyKeys` |
| 11 | 题干与图片跨记录拼接 | 串图（图不对题） | 图文必须同源 |
| 12 | LaTeX 里 `\b \f \r \t` 开头命令写进 JSON | 反斜杠被吃、KaTeX 报错 | `\boldsymbol` `\frac` `\right` `\times` 是高危 |
| 13 | 拼卷 `_ppIdx` 在后台数据到达前缓存 | 误报"这道题已不在题库里" | 数据到达后置 `null` 重建 |
| 14 | `color-mix()` 当唯一实现 | 老 Chrome 退实心色 | 关键颜色在 JS 里算好 rgba |

---

## 9. 当前状态与待办

### 已完成（近期）

- 线代 354 题：思路重写（①②逐行）、答案分小问、点睛四段全量、清数一记号、分支对齐站点
- 线代 4 章补「思路首行思想」：**行列式 40/40、线性方程组 73/73、特征值与特征向量 64/64、二次型 71/71**
- 二次型 71 题**题源标签**按《线代臻选题·索引》核对修正（43 处）
- 笔记：32 篇全部有 `###` 小节（共 522 个），重点标 ⭐；目录自动展开、⭐ 选中变蓝已修
- 性能：首屏 2.07s、图片独立缓存、原图预热 20 张（三级门禁）
- 交互：图片灯箱缩放、整块高亮改版、拼卷 4:2:1 + 7 天不重复 + 题量可选

### 待办（用户可能接着提）

| 项 | 状态 |
|---|---|
| **矩阵 75 题、向量 31 题**补「思路首行思想」 | ⬜ 未做（线代还剩这 106 题） |
| 全库题源格式统一 | ⬜ 约 100 处：矩阵章 45 处外层括号、一元积分 6 处 `0.66k`、极限 4 处 |
| `srcOrder` 3 处异常 | ⬜ `1133=207`（应 323）、`1319=214`、`1324=269`；只影响排序 |
| 高数 759 题补「思想」 | ⬜ 未开始（用户只要求过线代） |

### 数据现状快照

```
core_bank 1113 题（高数 759 / 线代 354）
notes.json 32 篇（274 个 ## 章、522 个 ### 小节）
exam.json 27 套 / 607 题（2000–2026 数二）
ansImg 514 张 / 140MB（img 目录共 194MB）
```

---

## 10. 常用命令与脚本速查

```bash
# 本地预览
cd pwa && python -m http.server 8080

# 数据自检
node tools/_check_core_bank.js
node tools/_final_verify.js

# 笔记块序号快照（改笔记正文前必跑）
D:/python/python.exe tools/_snap_note_blocks.py before
# …改内容…
D:/python/python.exe tools/_snap_note_blocks.py after
# 然后逐篇比对 blocks 序列，必须完全一致

# 线上复核
curl -s "https://cyrusssxx.github.io/math_learn/pwa/sw.js?cb=$RANDOM" | grep -o "CACHE_VER = '[^']*'"
curl -s "https://cyrusssxx.github.io/math_learn/pwa/data/core_bank.json?cb=$RANDOM" | head -c 300

# 题源核对（二次型已建好范式，其他章可复用）
node tools/_check_2cx_match.js    # 标了「数二」的题去套卷里找，找不到就是假题源
```

**历史日志**：`.workbuddy-ai/memory/YYYY-MM-DD.md`（按日追加，最近的 10-28 ~ 10-31 信息最密）。
**长期约定**：`.workbuddy-ai/memory/MEMORY.md`（本文是它的超集，冲突时以本文 + 用户最新指令为准）。

---

## 11. 交接检查清单

接手后第一次改动前，确认这几件事：

- [ ] 读过 `网站说明.md`（数据字典）+ 本文（规则）
- [ ] `git status` 干净，`git log -5` 看过最近改动
- [ ] 知道这次要改的是**哪一节**（节名必须与 `core_bank.sections[].title` 完全一致）
- [ ] 知道改完要跑哪两个检查脚本
- [ ] 知道改完要 push + 抓线上复核
- [ ] 涉及分支/顺序 → 先报清单，等用户确认
