# -*- coding: utf-8 -*-
"""按行升级 3 份 mdBlock 兜底：\begin 环境 → $$ 包裹"""
import io, re

FILES = ['pwa/js/exam.js', 'pwa/js/exam-shared.js', 'pwa/js/category.js']
PAT = re.compile(r"(\s*)out\.push\('<p>'\s*\+\s*mdInline\('\$'\s*\+\s*l\s*\+\s*'\$'\)\s*\+\s*'</p>'\);")

for p in FILES:
    s = io.open(p, encoding='utf-8').read()
    if 'const disp = ' in s:
        print('已含新逻辑，跳过:', p)
        continue
    def rep(m):
        ind = m.group(1)
        return (ind + "const disp = /\\\\begin\\{/.test(l) || /\\\\end\\{/.test(l);\n"
                + ind + "out.push('<p>' + mdInline((disp ? '$$' : '$') + l + (disp ? '$$' : '$')) + '</p>');")
    s2, n = PAT.subn(rep, s)
    if n:
        io.open(p, 'w', encoding='utf-8', newline='').write(s2)
        print('已升级 %s（%d 处）' % (p, n))
    else:
        print('!! 未匹配:', p)