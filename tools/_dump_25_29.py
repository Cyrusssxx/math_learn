# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

for no in (25, 29):
    q = next(q for p in core for s in p['sections'] for q in s['questions'] if q.get('no') == no)
    print('=' * 70)
    print(f"no={no} | source={q.get('source')} | 章节={[s['title'] for p in core for s in p['sections'] if q in s['questions']]}")
    print('--- stem ---')
    print(q.get('stem'))
    print('--- answer (完整) ---')
    print(q.get('answer'))
    print('--- idea ---')
    print(q.get('idea'))
    print('--- tips ---')
    print(json.dumps(q.get('tips', {}), ensure_ascii=False, indent=1))
