# -*- coding: utf-8 -*-
"""撤销「⭐ 常用」置顶组：删 PINNED_NOTES 常量 + renderTree 里的置顶块，还原为按学科分组顺序。"""
import io

P = 'D:/ai code/math-note/pwa/js/reader.js'
s = io.open(P, encoding='utf-8').read()

# 1) 删 PINNED_NOTES 常量（两行：注释 + 定义）
for seg in (
    "// 常用置顶：常见公式速查 + 各科真题点睛（按此顺序显示在目录最前，跨学科）\n"
    "const PINNED_NOTES = ['高数0-中学公式速查', '高数20-真题点睛', '线代7-真题点睛'];\n",
):
    assert seg in s, '找不到 PINNED_NOTES 常量块'
    s = s.replace(seg, '', 1)

# 2) 删 renderTree 内的置顶组渲染块
pin_block = """    // ⭐ 常用：置顶到目录最前
    const pinned = PINNED_NOTES.map(id => notes.find(n => n.id === id)).filter(Boolean);
    if (pinned.length) {
        const gOpen = openGroups['pinned'] !== false;
        html += `<div class="tree-group ${gOpen ? 'open' : ''}" onclick="toggleGroup('pinned')">
            <span class="tree-arrow">›</span>⭐ 常用</div>`;
        if (gOpen) for (const n of pinned) html += fileHtml(n);
    }
"""
assert pin_block in s, '找不到置顶组渲染块'
s = s.replace(pin_block, '', 1)

# 3) 学科组内排除已置顶项 → 还原
s = s.replace("notes.filter(n => n.subject === key && !PINNED_NOTES.includes(n.id))",
              "notes.filter(n => n.subject === key)")

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('已撤销：')
print('  PINNED_NOTES 引用残留:', s.count('PINNED_NOTES'))
print('  ⭐ 常用 残留:', s.count('⭐ 常用'))
print('  fileHtml 抽取保留（无害）:', s.count('fileHtml'))