# -*- coding: utf-8 -*-
"""剥掉 40 道选择题解析开头冗余的 **答案：X。**（答案已在【答案】行给出）。"""
import json, re
PATH = r'D:/ai code/math-note/pwa/data/mn27_zs4_papers.json'
d = json.load(open(PATH, encoding='utf-8'))
n = 0
for p in d:
    for s in p['sections']:
        for q in s['questions']:
            new, k = re.subn(r'(\*\*【解】\*\*\s*)\*\*答案[:：][A-D][。\.]\*\*\s*', r'\1', q['answer'], count=1)
            if k:
                q['answer'] = new
                n += 1
assert n == 40, n
json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False)
print('剥除冗余答案前缀', n, '处')
