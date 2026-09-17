# -*- coding: utf-8 -*-
"""抽查低置信答案匹配（rescue / rescue2 / hist），确认没有张冠李戴。"""
import json, io, sys, difflib
sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import load_refs, norm, grams            # noqa: E402

ROOT = 'D:/ai code/math-note/tools/'
bank = json.load(io.open(ROOT + 'yancai_bank.json', encoding='utf-8'))
refs = load_refs()
byid = {}
for r in refs:
    byid[(r['ref'], str(r['rid']))] = r

low = [q for q in bank['questions'] if q.get('ans_tier') in ('rescue', 'rescue2', 'hist')]
print('低置信层题数：%d（rescue %d / rescue2 %d / hist %d）' % (
    len(low),
    sum(1 for q in low if q['ans_tier'] == 'rescue'),
    sum(1 for q in low if q['ans_tier'] == 'rescue2'),
    sum(1 for q in low if q['ans_tier'] == 'hist')))

for tier in ('rescue2', 'rescue', 'hist'):
    print()
    print('=' * 78)
    print('【%s】' % tier)
    for q in low:
        if q['ans_tier'] != tier:
            continue
        print('-' * 70)
        print('[%s] src=%s score=%s ref=%s' % (q['id'], q.get('source'), q.get('ans_score'), q.get('ans_ref')))
        print('  核心: %s' % (q.get('stem') or '').replace('\n', ' ')[:170])
        k, _, rid = (q.get('ans_ref') or '').partition('/')
        r = byid.get((k, rid))
        if r:
            print('  参考: %s' % (r['stem'] or '').replace('\n', ' ')[:170])
            print('  答案: %s' % (r['answer'] or '').replace('\n', ' ')[:90])
        else:
            print('  !! 参考未找到:', q.get('ans_ref'))
