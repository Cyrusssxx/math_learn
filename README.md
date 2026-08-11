# 考研数学笔记（math-cards）

考研数学笔记阅读站 PWA：高等数学 + 线性代数共 17 份笔记，
左侧目录树 + 右侧页内导航 + 全文搜索，KaTeX 公式渲染，完全离线可用。

## 使用

双击 `start.bat`（自动开浏览器 → http://localhost:8409）。

> 必须经 http:// 访问；直接双击 html（file://）时 fetch 与 Service Worker 均不可用。

只有一个页面（仿 Obsidian Publish 三栏布局）：

- 左侧：学科 › 文件 › 章节目录树（点箭头展开章节），顶部搜索框全文检索
- 中间：完整渲染的笔记正文（⚠️易错 / 💡技巧 / 例题 显示为彩色提示块）
- 右侧：本页目录，跟随滚动高亮当前章节
- 左上 🌙 切换夜间模式；URL 形如 `#/高数4-微分方程/2` 可直达某章

## 笔记数据从导图 md 重新生成

```
python -X utf8 tools\build_notes.py
```

- 数据源：`D:\ai code\math\导图\*.md`（frontmatter 剥离，H1=标题，H2=章）
- 输出：`pwa/data/notes.json`（原文打包，渲染在前端 `pwa/js/reader.js` 完成）

**改完数据后**：把 `pwa/sw.js` 里的 `CACHE_VER` 版本号 +1，否则旧缓存不更新。

## 注意

- KaTeX 已本地化在 `pwa/vendor/katex/`（如缺失可运行 `python tools\fetch_katex.py` 重新下载）
- 历史遗留：`tools/build_cards.py`、`tools/test_fsrs.js` 属已下线的记忆卡片体系，仅存档备用
