# -*- coding: utf-8 -*-
# 扫描所有考「解的情况 / 唯一解 / 无解 / 无穷多解」的真题（克拉默法则判别思路适用）
import json, io, re

exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
pat = re.compile(r'唯一解|无解|无穷多解|解的情况|有解')
rows = []
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            st = str(q.get('stem') or '')
            if pat.search(st):
                rows.append((v['id'], q['no'], st))
print('考「解的情况」的真题:', len(rows))
print()
for pid, no, st in rows:
    # 摘要：取含关键词的那一句
    lines = [l.strip() for l in st.split('\n') if pat.search(l)]
    brief = lines[0][:120] if lines else st[:120]
    print('%-16s %s' % (pid + '-' + str(no), brief))
    print('       %s' % ' '.join(st.split())[:170])
    print()