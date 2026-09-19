# -*- coding: utf-8 -*-
"""mdBlock 兜底增强 v2：\begin 裸行缺 \end{X} 自动补齐（两行间有空行，按 repr 精确匹配）。"""
import io

OLD = "const disp = /\\\\begin\\{/.test(l) || /\\\\end\\{/.test(l);\n\n            out.push('<p>' + mdInline((disp ? '$$' : '$') + l + (disp ? '$$' : '$')) + '</p>');"

NEW = ("const disp = /\\\\begin\\{/.test(l) || /\\\\end\\{/.test(l);\n"
       "            let t = l;\n"
       "            if (disp) {\n"
       "                // 自动补齐缺失的 \\\\end{X}（数据里常见「多行显示块被压成单行」）\n"
       "                const envs = [...t.matchAll(/\\\\begin\\{([^}]+)\\}/g)].map(m => m[1]);\n"
       "                for (const env of envs) {\n"
       "                    const nB = (t.match(new RegExp('\\\\\\\\begin\\\\{' + env + '\\\\}', 'g')) || []).length;\n"
       "                    const nE = (t.match(new RegExp('\\\\\\\\end\\\\{' + env + '\\\\}', 'g')) || []).length;\n"
       "                    for (let k = nB - nE; k > 0; k--) t += '\\\\end{' + env + '}';\n"
       "                }\n"
       "            }\n"
       "            out.push('<p>' + mdInline((disp ? '$$' : '$') + t + (disp ? '$$' : '$')) + '</p>');")

for p in ['pwa/js/exam.js', 'pwa/js/exam-shared.js', 'pwa/js/category.js']:
    s = io.open(p, encoding='utf-8').read()
    if '自动补齐缺失' in s:
        print('已含，跳过:', p)
        continue
    n = s.count(OLD)
    if n:
        io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(OLD, NEW, 1))
        print('已升级 %s（命中 %d 处）' % (p, n))
    else:
        print('!! 仍未匹配:', p)