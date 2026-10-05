# 自动化执行记忆：core_bank 残留 LaTeX 规范化

## 2026-09-20 执行摘要
任务：修复 core_bank.json 中 56 个残留 LaTeX 原文字段（清单 tools/_todo_core.json）。

结果：
- 56 字段全部处理完成，页面级渲染残留 56→0（全量体检 core 侧 0 残留；剩余 6 个 bad 均为 exam 真题侧，不在本清单）。
- 逐段 katex.renderToString(throwOnError:true) 自检：733 段、失败字段数 0。
- JSON 合法、题数 606 不变；bak 对比 token 级内容一致（仅格式改动+3 处数据残缺留注记：core-146 answer/idea 尾部、core-353 answer/idea 尾部）。
- commit 06e6b9b，远程 HEAD 06e6b9b 已核对。

## 可复用经验（重要）
1. 修复手法按 9 批分层：b1 结构性定界符（空环境对/缺开块/$$$$/行内$$）→ b2 中文行内裸公式 → b3-b9 复杂 AI 长解答逐字段（状态机规范、整段重写）。
2. **根因分类**：
   - `【答案】$$` 同行 → 必须拆成 `【答案】\n$$\n`（mdBlock 只认行首 $$ 开块）。
   - `\begin{aligned}\end{aligned}` 空对 + 后续散内容 → 删空对、内容并入环境。
   - 闭块后直接接 `= X$$`（缺开块）→ X 前补 `$$\n`。
   - 中文行内裸公式（含 \ 命令）→ 包 `$...$`；`\text{则}` 等 → 中文。
   - `\substack{X\nY}` 真实换行 → `X\Y`。
   - `\text{______}` 下划线 → `\text{\_\_\_\_\_\_}`（KaTeX 必炸）。
   - **`$` 后紧跟数字（如 `$4\dfrac`）auto-render 不识别** → 拆成独立显示块。
   - `$$` 块内夹中文文本行（AI 长解答通病）→ 中文行移出块、公式独立成块。
3. 验证链路：`_t_locate_core.js`（页面级残留）→ `_t_kcheck.js`（逐段 throwOnError 严格自检）→ `_t_full.js`（全量体检）→ bak 对比 token 级内容一致性。
4. 数据文件一律 json.loads→改→json.dumps 紧凑单行写回（本轮未破坏，无坑）。

## 待办/遗留
- exam 真题侧仍有 6 个 bad（2021-19 / 2016-23 / 2014-21 / 2006-15 / 2003-13 / 2003-22），非本清单范围，后续如需可单独处理。
