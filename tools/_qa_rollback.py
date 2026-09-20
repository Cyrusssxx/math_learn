# -*- coding: utf-8 -*-
"""QA 回滚：子代理误删内容的 2 个字段恢复为 git HEAD~1 版本（内容完整优先，格式后续精修）"""
import json, io, subprocess

P = 'D:/ai code/math-note/pwa/data/exam.json'
old = json.loads(subprocess.run(['git', 'show', 'HEAD~1:pwa/data/exam.json'],
                                cwd='D:/ai code/math-note', capture_output=True, text=True,
                                encoding='utf-8').stdout)
cur = json.load(io.open(P, encoding='utf-8'))

ROLLBACK = {('2016数二真题', '16', 'answer'), ('2003数二真题', '13', 'answer')}


def getq(d, rid, no):
    for v in d:
        if v['id'] != rid:
            continue
        for s in v.get('sections', []):
            for q in s.get('questions', []):
                if str(q['no']) == no:
                    return q
    return None


done = 0
for rid, no, f in ROLLBACK:
    oq = getq(old, rid, no)
    cq = getq(cur, rid, no)
    if oq and cq:
        cq[f] = oq[f]
        done += 1
        print('已回滚 %s 第%s题.%s（len %d）' % (rid, no, f, len(oq[f])))

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(cur, fp, ensure_ascii=False, separators=(',', ':'))
print('回滚 %d 个字段' % done)
