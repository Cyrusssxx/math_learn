# -*- coding: utf-8 -*-
"""mdBlock 兜底增强：\begin 裸行缺 \end{X} 自动补齐。纯字符串替换（避开正则转义）。"""
import io

PATCH_DISP = """            const disp = /\\\\begin\\{/.test(l) || /\\\\end\\{/.test(l);
            let t = l;
            if (disp) {
                // 自动补齐缺失的 \\end{X}（数据里常见「多行显示块被压成单行」）
                const envs = [...t.matchAll(/\\\\begin\\{([^}]+)\\}/g)].map(m => m[1]);
                for (const env of envs) {
                    const re = new RegExp('\\\\\\\\begin\\\\{' + env + '\\\\}', 'g');
                    const nB = (t.match(re) || []).length;
                    const nE = (t.match(new RegExp('\\\\\\\\end\\\\{' + env + '\\\\}', 'g')) || []).length;
                    for (let k = nB - nE; k > 0; k--) t += '\\\\end{' + env + '}';
                }
            }
            out.push('<p>' + mdInline((disp ? '$$' : '$') + t + (disp ? '$$' : '$')) + '</p>');"""

OLD_DISP = "            const disp = /\\\\begin\\{/.test(l) || /\\\\end\\{/.test(l);\n            out.push('<p>' + mdInline((disp ? '$$' : '$') + l + (disp ? '$$' : '$')) + '</p>');"

for p in ['pwa/js/exam.js', 'pwa/js/exam-shared.js', 'pwa/js/category.js']:
    s = io.open(p, encoding='utf-8').read()
    if '自动补齐缺失' in s:
        print('已含，跳过:', p)
        continue
    if OLD_DISP in s:
        io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(OLD_DISP, PATCH_DISP, 1))
        print('已升级:', p)
    else:
        print('!! 未匹配:', p)