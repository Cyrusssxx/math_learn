# -*- coding: utf-8 -*-
# 扫描全库：答案/解析里含「条件不足/待核/对称性/标准取向/标准答案为」等含糊或可疑措辞的题
import json, io, re

exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
pats = ['条件不足', '待核', '对称性的标准取向', '标准取向', '标准答案为', '题目有误', '题目可能有误', '存疑', '无法确定', '无法唯一']
rows = []
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            for f in ('answer', 'idea'):
                t = str(q.get(f) or '')
                for p in pats:
                    if p in t:
                        rows.append((v['id'], q['no'], f, p, t[:70]))
print('命中:', len(rows))
for r in rows[:40]:
    print('  %s-%s.%s [%s] %s' % (r[0], r[1], r[2], r[3], r[4].replace('\n', ' ')))

# 另外：含 f(x+2) 类递推的其它题（同型题检查）
print()
print('=== 含 f(x+2) 的题 ===')
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            st = str(q.get('stem') or '')
            if 'f(x+2)' in st or 'f(x + 2)' in st:
                print('  %s-%s: %s' % (v['id'], q['no'], st[:150]))