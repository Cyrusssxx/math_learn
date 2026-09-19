# -*- coding: utf-8 -*-
"""生成《公式格式问题清单.md》：按字段汇总公式格式问题（供人工确认后批量修）"""
import json, io, sys
from collections import Counter, defaultdict
sys.path.insert(0, 'D:/ai code/math-note/tools')
from _audit_formula_v2 import scan, LATEX_CMD            # noqa: E402

FILES = [('真题卷 exam.json', 'D:/ai code/math-note/pwa/data/exam.json'),
         ('核心题库 core_bank.json', 'D:/ai code/math-note/pwa/data/core_bank.json')]
OUT = 'D:/ai code/math-note/公式格式问题清单.md'

rows = []
for tag, path in FILES:
    d = json.load(io.open(path, encoding='utf-8'))
    if isinstance(d, list) and d and 'sections' in d[0]:
        for vol in d:
            for sec in vol.get('sections', []):
                for q in sec.get('questions', []):
                    for f in ('stem', 'answer', 'idea'):
                        v = q.get(f) or ''
                        if not v:
                            continue
                        e, b = scan(v)
                        if e or b:
                            typ = Counter(k for k, *_ in e)
                            rows.append((tag, '%s 第%s题' % (vol.get('id'), q.get('no')), f, len(e), len(b), dict(typ)))
    else:
        for sec in d[0]['sections']:
            for q in sec['questions']:
                for f in ('stem', 'answer', 'idea'):
                    v = q.get(f) or ''
                    if not v:
                        continue
                    e, b = scan(v)
                    if e or b:
                        typ = Counter(k for k, *_ in e)
                        rows.append((tag, '第%s题' % q.get('no'), f, len(e), len(b), dict(typ)))

by_file = defaultdict(list)
for r in rows:
    by_file[r[0]].append(r)

lines = ['# 公式格式问题清单（$ / $$ 配平体检）', '',
         '> 生成工具：`tools/_audit_formula_v2.py`（token 流状态机：display `$$` / inline `$`）',
         '> 问题类型：**E3 未闭合**（开块不闭合 → 把后续正文吞进公式，导致大片逐字裸奔，最严重）｜',
         '> **E4 裸公式行**（含 LaTeX 命令但未包 `$` → 显示原文）｜E1/E2 嵌套错（多为 E3 的连锁反应）', '']
tot = 0
for tag in by_file:
    rs = by_file[tag]
    tot += len(rs)
    e3 = sum(1 for r in rs if any(k.startswith('E3') for k in r[5]))
    e4 = sum(r[4] for r in rs)
    lines += ['## %s：%d 个字段有问题（其中含 E3 未闭合的 %d 个；裸公式行合计 %d 行）' % (tag, len(rs), e3, e4), '',
              '| 位置 | 字段 | E1/E2 | E3 | 裸公式行 |', '|---|---|---|---|---|']
    for _, where, f, ne, nb, typ in sorted(rs, key=lambda x: -(x[3] + x[4]))[:40]:
        e1 = typ.get('E1 display内单$', 0) + typ.get('E2 inline内$$', 0)
        e3n = sum(v for k, v in typ.items() if k.startswith('E3'))
        lines.append('| %s | %s | %d | %d | %d |' % (where, f, e1, e3n, nb))
    lines.append('')
lines += ['---', '',
          '## 已修复', '',
          '- ✅ **2020 数二第15题 answer**：裸公式行 `\\frac{y}{x}=e^{-1}\\cdots` 补 `$$` 包裹 + 删除多余孤立 `$$`',
          '  （该 `$$` 把「故」「代入 …」正文吞进显示块 → KaTeX 遇 `$` 崩溃 → 逐字裸奔）。',
          '  修复后 28 个公式段 KaTeX 渲染 **0 失败**。', '',
          '## 待处理', '',
          '- 其余字段存在同类（及 E4 裸公式行）问题。批量自动修需按类型设计规则并逐个复检；',
          '  自动修复器 `tools/_fix_formula_safe.py` 已内置「修复 → 复检 → 不过则回滚」安全机制。']
io.open(OUT, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('已写 %s（%d 个字段有问题）' % (OUT, tot))
for tag in by_file:
    print('  %s: %d 个字段' % (tag, len(by_file[tag])))
