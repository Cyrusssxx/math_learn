# -*- coding: utf-8 -*-
# 给 core_bank 无 linkedQid 的题按 stem 匹配 exam.json 补链接（提升真题收藏/标记同步率）
import json, io, re

core = json.load(io.open('pwa/data/core_bank.json', encoding='utf-8'))
exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))

# exam 侧题库：qid -> (norm_stem, prefix30)
def norm(t):
    return re.sub(r'\s+', '', str(t or '')).replace('$', '')

exam_qs = []
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            ns = norm(q.get('stem'))
            exam_qs.append((v['id'] + '-' + str(q['no']), ns))

# 精确索引 + 前缀索引
exact = {}
pref = {}
for qid, ns in exam_qs:
    if len(ns) >= 10:
        exact.setdefault(ns, qid)
        pref.setdefault(ns[:30], qid)

n_total = n_linked = n_new = n_multi = 0
for s in core[0]['sections']:
    for q in s['questions']:
        n_total += 1
        if q.get('linkedQid'):
            n_linked += 1
            continue
        ns = norm(q.get('stem'))
        hit = None
        if len(ns) >= 10 and ns in exact:
            hit = exact[ns]
        elif len(ns) >= 30 and ns[:30] in pref:
            # 前缀命中：若多题同前缀需谨慎——pref 只存首个，检查是否唯一
            p = ns[:30]
            same = [e for e, ens in exam_qs if ens[:30] == p]
            if len(same) == 1:
                hit = same[0]
            else:
                n_multi += 1
        if hit:
            q['linkedQid'] = hit
            n_new += 1

print('core 总题 %d，原有链接 %d，本次补链 %d，前缀多义放弃 %d' % (n_total, n_linked, n_new, n_multi))
with io.open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='') as fp:
    json.dump(core, fp, ensure_ascii=False, separators=(',', ':'))
print('已写回 core_bank.json')
