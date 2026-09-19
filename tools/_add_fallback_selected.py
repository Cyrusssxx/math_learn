# -*- coding: utf-8 -*-
"""为 selected.js 的精简版 mdBlock 插入「裸公式行兜底」"""
import io

P = 'pwa/js/selected.js'
s = io.open(P, encoding='utf-8').read()
OLD = "        out.push('<p>'+mdInline(l)+'</p>');\n"
NEW = ("        // 裸公式行兜底：无 $ 但整行是 LaTeX（不含中文）→ 自动补 $ 渲染\n"
       "        if(!l.includes('$')&&!/[\\u4e00-\\u9fff]/.test(l)&&l.trim().length>3"
       "&&/\\\\[a-zA-Z]{2,}/.test(l)&&/[=+\\-^_{}]/.test(l)){out.push('<p>'+mdInline('$'+l+'$')+'</p>');continue;}\n"
       + OLD)
assert OLD in s, '锚点未找到'
if '裸公式行兜底' in s:
    print('已存在，跳过')
else:
    io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(OLD, NEW, 1))
    print('已插入:', P)