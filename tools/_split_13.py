# -*- coding: utf-8 -*-
# 2003-13 L1：一行多块 → 拆成多行块（间隙裸段补 $$）
import json, io

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2003数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '13')

lines = q['answer'].split('\n')


def split_blocks(line):
    parts = line.split('$$')
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:
            out.append('$$' + p + '$$')
        else:
            s = p.strip()
            if s:
                out.append('$$' + s + '$$')
    return '\n'.join(out)


lines[1] = split_blocks(lines[1])
q['answer'] = '\n'.join(lines)
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('2003-13 L1 已拆为多行:')
for L in q['answer'].split('\n')[:6]:
    print('  | ' + L[:70])
