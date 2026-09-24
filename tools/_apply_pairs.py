# -*- coding: utf-8 -*-
# 应用人工审核确认的 34 条 core→exam 配对（同题，痕迹互通）
import json, io

PAIRS = {
    '564': '2021数二真题-15', '354': '2017数二真题-6', '194': '2020数二真题-15',
    '554': '2007数二真题-19', '200': '2019数二真题-6', '213': '2017数二真题-18',
    '450': '2023数二真题-18', '412': '2015数二真题-5', '92': '2015数二真题-2',
    '69': '2024数二真题-4', '446': '2026数二真题-19', '77': '2013数二真题-20',
    '207': '2022数二真题-3', '377': '2026数二真题-11', '167': '2007数二真题-13',
    '148': '2026数二真题-18', '251': '2019数二真题-16', '484': '2022数二真题-19',
    '485': '2020数二真题-19', '218': '2021数二真题-18', '581': '2021数二真题-20',
    '258': '2000数二真题-3', '353': '2016数二真题-20', '122': '2022数二真题-17',
    '536': '2001数二真题-4', '43': '2024数二真题-2', '101': '2014数二真题-1',
    '250': '2025数二真题-17', '158': '2026数二真题-6', '558': '2024数二真题-18',
    '444': '2012数二真题-16', '197': '2005数二真题-2', '382': '2009数二真题-6',
    '418': '2026数二真题-14',
}

core = json.load(io.open('pwa/data/core_bank.json', encoding='utf-8'))
exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))

# 校验目标 qid 都存在
exist = set()
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            exist.add(v['id'] + '-' + str(q['no']))
missing = [t for t in PAIRS.values() if t not in exist]
assert not missing, '目标 qid 不存在: %s' % missing

applied = 0
skip_linked = []
for s in core[0]['sections']:
    for q in s['questions']:
        no = str(q['no'])
        if no in PAIRS:
            if q.get('linkedQid') and q['linkedQid'] != PAIRS[no]:
                skip_linked.append((no, q['linkedQid']))
                continue
            if not q.get('linkedQid'):
                q['linkedQid'] = PAIRS[no]
                applied += 1

lk = sum(1 for s in core[0]['sections'] for q in s['questions'] if q.get('linkedQid'))
print('本次人工配对应用: %d 条；已有不同链接跳过: %s' % (applied, skip_linked or '无'))
print('core 有链接总数: %d / 606' % lk)

with io.open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='') as fp:
    json.dump(core, fp, ensure_ascii=False, separators=(',', ':'))
print('已写回 core_bank.json')