# -*- coding: utf-8 -*-
"""在 4 份 mdBlock 副本里插入「裸公式行兜底」：
   无 $ 包裹但整行是 LaTeX（且不含中文）的行，自动补 $ 后按行内公式渲染，
   避免数据里漏包 $ 的公式以原文显示（如题602 的 g_y / g_{xy} 两行）。"""
import io

FILES = ['pwa/js/exam.js', 'pwa/js/exam-shared.js', 'pwa/js/category.js', 'pwa/js/selected.js']

SNIPPET = """        // 裸公式行兜底：无 $ 包裹但整行是 LaTeX（且不含中文）→ 自动补 $ 渲染。
        // 数据里偶有漏包 $ 的公式行（如解答中的 g_y=... / g_{xy}=... 连续两行），
        // 不兜底就会以 LaTeX 原文显示（用户看到「公式没渲染」）。
        if (!l.includes('$') && !/[\\u4e00-\\u9fff]/.test(l) && l.trim().length > 3
            && /\\\\[a-zA-Z]{2,}/.test(l) && /[=+\\-\\^_{}]/.test(l)) {
            out.push('<p>' + mdInline('$' + l + '$') + '</p>');
            continue;
        }
"""

for p in FILES:
    s = io.open(p, encoding='utf-8').read()
    if '裸公式行兜底' in s:
        print('已存在，跳过:', p)
        continue
    anchor = "        // 笔记标题令牌（<h1>/<h2>）独占整行时作为块级标题输出，不放进 <p>"
    if anchor not in s:
        print('!! 未找到锚点:', p)
        continue
    s = s.replace(anchor, SNIPPET + anchor, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('已插入兜底逻辑:', p)
