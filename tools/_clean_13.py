# -*- coding: utf-8 -*-
# 清理 2003-13 的空块垃圾行（$$\n$$、$$$$、孤立 $$ 行）
import json, io

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2003数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '13')
lines = q['answer'].split('\n')
out = []
skip_next = False
for i, L in enumerate(lines):
    st = L.strip()
    if st == '$$$$':
        continue
    if st == '$$':
        # 孤立 $$ 行：若下一行也是 $$ → 删本行；否则保留（可能是块开/闭）
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ''
        if nxt == '$$':
            continue
    out.append(L)
q['answer'] = '\n'.join(out)
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('清理完成，当前结构:')
for L in q['answer'].split('\n')[:8]:
    print('  | %s' % L[:70])
