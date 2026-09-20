# -*- coding: utf-8 -*-
"""增强质检：列出所有被改字段的 delete/replace 片段，筛出「实质内容被删」（含中文/数字/评分等）"""
import json, io, subprocess, difflib, re

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

HAN = re.compile(r'[\u4e00-\u9fff0-9]')
issues = []
for key, q in cur_q.items():
    oq = old_q.get(key)
    if not oq:
        continue
    for f in ('stem', 'answer', 'idea'):
        a, b = oq.get(f) or '', q.get(f) or ''
        if a == b:
            continue
        sm = difflib.SequenceMatcher(None, a, b)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'delete' and HAN.search(a[i1:i2]) and len(a[i1:i2]) > 8:
                issues.append((key, f, a[i1:i2]))
            elif op == 'replace' and HAN.search(a[i1:i2]) and len(a[i1:i2]) > 12:
                issues.append((key, f, '%r -> %r' % (a[i1:i2][:80], b[j1:j2][:40])))

print('存在实质内容删除/替换的字段: %d 处' % len(issues))
for key, f, frag in issues:
    print('  %s-%s.%s:' % (key[0], key[1], f))
    print('    %s' % frag[:200])
