# -*- coding: utf-8 -*-
"""质检：exam.json 被子代理修改的字段，数学内容是否被误改。
   方法：git 取修改前（HEAD~1）与当前，找出被改字段；
   每字段「去 $、去空白」后的纯数学字符序列做相似度比对，<0.97 标记可疑。"""
import json, io, re, subprocess

P = 'D:/ai code/math-note/pwa/data/exam.json'

old = json.loads(subprocess.run(['git', 'show', 'HEAD~1:pwa/data/exam.json'],
                                cwd='D:/ai code/math-note', capture_output=True, text=True,
                                encoding='utf-8').stdout)
cur = json.load(io.open(P, encoding='utf-8'))

old_q = {}
for v in old:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            old_q[(v['id'], str(q['no']))] = q
cur_q = {}
for v in cur:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            cur_q[(v['id'], str(q['no']))] = q


def pure(t):
    t = re.sub(r'\$', '', t)
    t = re.sub(r'\s+', '', t)
    return t


import difflib

changed = []
for key, q in cur_q.items():
    oq = old_q.get(key)
    if not oq:
        continue
    for f in ('stem', 'answer', 'idea'):
        a = oq.get(f) or ''
        b = q.get(f) or ''
        if a == b:
            continue
        pa, pb = pure(a), pure(b)
        ratio = difflib.SequenceMatcher(None, pa, pb).ratio()
        changed.append((key, f, len(a), len(b), round(ratio, 4)))

print('被修改字段: %d 个' % len(changed))
suspect = [c for c in changed if c[4] < 0.97]
print('数学内容差异 ≥3%%（可疑）: %d 个' % len(suspect))
for key, f, la, lb, r in sorted(suspect, key=lambda x: x[4])[:10]:
    print('  %s.%s  旧%d字→新%d字  去$相似度 %.3f' % (key[0] + '-' + key[1], f, la, lb, r))
print()
ok = [c for c in changed if c[4] >= 0.97]
print('仅格式变化（去$后 ≥97%% 一致）: %d 个' % len(ok))
# 无 diff 检查
print()
print('题数核对: 旧 %d / 新 %d' % (len(old_q), len(cur_q)))
