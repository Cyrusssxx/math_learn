# -*- coding: utf-8 -*-
# 检索真题中与克拉默法则/行列式求解线性方程组相关的题
import json, io, re, os

kw = ['克拉默', '克莱姆', '克拉姆', 'Cramer', 'cramer', '克萊姆']
pat_det = re.compile(r'行列式|系数行列式|唯一解')


def scan(items, tag, getstem):
    hits = []
    for it in items:
        st = str(getstem(it) or '')
        ans = str(it.get('answer') or '')
        exp = str(it.get('explanation') or it.get('idea') or '')
        allt = st + ' ' + ans + ' ' + exp
        if any(k in allt for k in kw):
            hits.append((tag, it, '克拉默关键词'))
    return hits


# 1) 本库真题 exam.json
exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
print('=== 本库 exam.json（27 套数二真题）命中「克拉默/克莱姆/Cramer」 ===')
n = 0
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            t = str(q.get('stem') or '') + ' ' + str(q.get('answer') or '') + ' ' + str(q.get('idea') or '')
            if any(k in t for k in kw):
                n += 1
                print('  %s-%s: %s' % (v['id'], q['no'], str(q.get('stem'))[:120]))
print('小计:', n)

# 2) 行列式/唯一解 相关真题（克拉默法则的适用场景）
print()
print('=== exam.json 中含「行列式」或「唯一解」的题（克拉默法则潜在适用） ===')
c = 0
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            t = str(q.get('stem') or '')
            if pat_det.search(t):
                c += 1
                if c <= 25:
                    print('  %s-%s: %s' % (v['id'], q['no'], t[:130]))
print('小计:', c)