# -*- coding: utf-8 -*-
# dry-run：增强 stem 相似度匹配（core 无链接题 → exam 真题），只分析不写盘
import json, io, re, difflib

core = json.load(io.open('pwa/data/core_bank.json', encoding='utf-8'))
exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))


def norm(t):
    s = str(t or '')
    s = re.sub(r'\s+', '', s).replace('$', '')
    s = re.sub(r'\\dfrac|\\frac|\\tfrac', '\\frac', s)   # 分式统一
    s = re.sub(r'\\left|\\right|\\!|\\,', '', s)
    s = re.sub(r'^[（(]?[一二三四五1-9１-９][.、）)]\s*', '', s)   # 题号前缀
    s = s.replace('（', '(').replace('）', ')').replace('，', ',').replace('。', '.')
    s = re.sub(r'[A-Da-d]\)', '', s)   # 选项标记
    return s


exam_qs = []
for v in exam:
    for sec in v.get('sections', []):
        for q in sec.get('questions', []):
            exam_qs.append((v['id'] + '-' + str(q['no']), norm(q.get('stem'))))

unlinked = []
for s in core[0]['sections']:
    for q in s['questions']:
        if not q.get('linkedQid'):
            unlinked.append(q)
print('无链接 core 题:', len(unlinked))

hits, near, none = [], [], []
for q in unlinked:
    ns = norm(q.get('stem'))
    if len(ns) < 15:
        none.append(q); continue
    best, best2, bid = 0.0, 0.0, None
    probe = ns[:40]
    for qid, es in exam_qs:
        if len(es) < 15:
            continue
        # 快筛：前20字 或 相似度粗判
        if ns[:20] == es[:20]:
            r = difflib.SequenceMatcher(None, ns, es).ratio()
        else:
            r = difflib.SequenceMatcher(None, probe, es[:40]).ratio()
            if r < 0.6:
                continue
            r = difflib.SequenceMatcher(None, ns, es).ratio()
        if r > best:
            best2, best, bid = best, r, qid
        elif r > best2:
            best2 = r
    if best >= 0.92 and best - best2 >= 0.05:
        hits.append((q, bid, best, best2))
    elif best >= 0.75:
        near.append((q['no'], round(best, 3), round(best2, 3), ns[:36]))
    else:
        none.append(q)

print('高置信匹配(r>=0.92 且领先0.05):', len(hits))
print('中等相似(0.75~0.92，未达标不配):', len(near))
print('低相似/太短:', len(none))
print('\n--- 高置信样本 8 条（core no -> exam qid | ratio | stem前36） ---')
for q, bid, r, r2 in hits[:8]:
    print('  %s -> %s | %.3f/%.3f | %s' % (q['no'], bid, r, r2, norm(q.get('stem'))[:36]))
print('\n--- 中等相似样本 6 条（疑似同题但有差异，人工判断用） ---')
for row in near[:6]:
    print('  no=%s best=%.3f second=%.3f | %s' % row)
