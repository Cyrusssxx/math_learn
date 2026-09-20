# -*- coding: utf-8 -*-
"""mdBlock 渲染层增强（4 份同步）：支持「同行首尾 $$」——如 $$\\begin{cases}...\\end{cases}$$ 整行作为显示块渲染。
   定位旧条件：mathBuf === null && l.startsWith('$$') 分支前插入同行首尾判断。"""
import io

NEW = """        // 同行首尾 $$（如 $$\\begin{cases}...\\end{cases}$$）：整行作为显示块直接渲染，
        // 旧条件 (!l.endsWith('$$') || l === '$$') 会把这类合法块排除 → 显示原文
        if (mathBuf === null && l.startsWith('$$') && l.endsWith('$$') && l !== '$$') {
            out.push('<p>' + mdInline(l) + '</p>');
            continue;
        }
"""

for p in ['pwa/js/exam.js', 'pwa/js/exam-shared.js', 'pwa/js/category.js']:
    s = io.open(p, encoding='utf-8').read()
    if '同行首尾' in s:
        print('已含，跳过:', p)
        continue
    anchor = "        if (mathBuf === null && l.startsWith('$$') && (!l.endsWith('$$') || l === '$$')) {"
    if anchor in s:
        s = s.replace(anchor, NEW + anchor, 1)
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print('已增强:', p)
    else:
        print('!! 未找到锚点:', p)

# selected.js 精简版
p = 'pwa/js/selected.js'
s = io.open(p, encoding='utf-8').read()
if '同行首尾' in s:
    print('selected 已含')
else:
    old = "if(mathBuf===null&&l.startsWith('$$')&&!l.endsWith('$$')){mathBuf=l;continue;}"
    new = ("if(mathBuf===null&&l.startsWith('$$')&&l.endsWith('$$')&&l!=='$$'){"
           "out.push('<p>'+mdInline(l)+'</p>');continue;}\n"
           "        " + old)
    if old in s:
        s = s.replace(old, new, 1)
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print('已增强: selected.js')
    else:
        print('!! selected 未找到锚点')
