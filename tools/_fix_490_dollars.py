# -*- coding: utf-8 -*-
"""no=490 末尾 $$ 配平（评分段末尾有孤立 $$）"""
import json, io

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

for p in core:
    for s in p['sections']:
        for q in s['questions']:
            if q.get('no') == 490:
                a = str(q.get('answer') or '')
                print('修复前 $$ 数:', a.count('$$'), '| 末尾30字:', repr(a[-30:]))
                # 评分段末尾的孤立 $$（前面无开 $$ 的）删除
                if a.rstrip().endswith('$$'):
                    q['answer'] = a.rstrip()[:-2].rstrip() + '\n'
                # 重新计数，若仍为奇数则在末尾补
                if q['answer'].count('$$') % 2 != 0:
                    q['answer'] += '\n$$'
                print('修复后 $$ 数:', q['answer'].count('$$'))

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))
print('no=490 配平完成')
