# -*- coding: utf-8 -*-
# 打印 58 对中等相似对照（core no ↔ exam qid，两侧 stem）供人工审核
import json, io, re, difflib

core = json.load(io.open('pwa/data/core_bank.json', encoding='utf-8'))
exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))


def norm(t):
    s = str(t or '')
    s = re.sub(r'\s+', '', s).replace('$', '')
    s = re.sub(r'\\dfrac|\\tfrac', r'\\frac', s)
    s = re.sub(r'\\left|\\right|\\!|\\,', '', s)
    s = s.replace('（', '(').replace('）', ')').replace('，', ',').replace('。', '.')
    return s


exam_map = {}
exam_list = []
for v in exam:
    for sec in v.get('sections', []):
        for q in sec.get('questions', []):
            qid = v['id'] + '-' + str(q['no'])
            ns = norm(q.get('stem'))
            exam_list.append((qid, ns))
            exam_map[qid] = ns

unl = [q for s in core[0]['sections'] for q in s['questions'] if not q.get('linkedQid')]
out = []
for q in unl:
    ns = norm(q.get('stem'))
    if len(ns) < 15:
        continue
    best, best2, bid = 0, 0, None
    probe = ns[:40]
    for qid, es in exam_list:
        if len(es) < 15:
            continue
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
    if 0.75 <= best < 0.92:
        out.append((best, q['no'], bid, best2, ns, exam_map.get(bid, '')))

out.sort(reverse=True)
print('中等相似对数:', len(out))
for r, no, bid, r2, ns, es in out:
    print('=== core-%s -> %s (best=%.3f 2nd=%.3f)' % (no, bid, r, r2))
    print('  CORE:', ns[:110])
    print('  EXAM:', es[:110])