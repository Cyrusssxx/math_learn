# -*- coding: utf-8 -*-
"""ZS2 Q6：把 display 公式里的 \\text{① }/\\text{② } 移到公式外，避免 KaTeX 缺字告警。"""
import json
PATH = r'D:/ai code/math-note/pwa/data/mn27_zs4_papers.json'
d = json.load(open(PATH, encoding='utf-8'))
old = (r'已知反常积分' + '\n\n' + r'$$' + '\n' + r'\text{① }\int_0^{+\infty}\frac{\sin^2x}{x(x+\sin x)}\,\mathrm dx,' + '\n' + r'$$'
       + '\n\n' + r'$$' + '\n' + r'\text{② }\int_0^{+\infty}\frac1{1+x|\sin x|}\,\mathrm dx,' + '\n' + r'$$' + '\n\n' + r'则（ ）。')
new = (r'已知反常积分' + '\n\n'
       + r'① $\displaystyle\int_0^{+\infty}\frac{\sin^2x}{x(x+\sin x)}\,\mathrm dx$，' + '\n\n'
       + r'② $\displaystyle\int_0^{+\infty}\frac1{1+x|\sin x|}\,\mathrm dx$，' + '\n\n'
       + r'则（ ）。')
done = False
for p in d:
    if p['id'] != 'mn27-zs4-2': continue
    for s in p['sections']:
        for q in s['questions']:
            if q['no'] == 6:
                assert q['stem'] == old, repr(q['stem'])
                q['stem'] = new
                done = True
assert done
json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False)
print('fixed ZS2 Q6 stem')
