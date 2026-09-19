# -*- coding: utf-8 -*-
"""定位 2020 年含 b=1/(2e) 那道极限题的 answer/idea，检查 $ 配平 / 连续$$ / 跨行 $"""
import json, io, re

ex = json.load(io.open('D:/ai code/math-note/pwa/data/exam.json', encoding='utf-8'))
KEY = 'y}{x}-\\frac1e'      # 特征片段
hit = []
for vol in ex:
    if str(vol.get('year')) != '2020':
        continue
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            for f in ('stem', 'answer', 'idea'):
                v = q.get(f) or ''
                if KEY in v or 'frac1{2e}' in v or '\\frac{1}{2e}' in v:
                    hit.append((q.get('no'), f, v))
print('命中 %d 个字段' % len(hit))
for no, f, v in hit:
    print('=' * 70)
    print('[2020 第%s题 %s] len=%d  $数=%d  $$=%d' % (no, f, len(v), v.count('$'), v.count('$$')))
    print('  连续$$空块:', len(re.findall(r'\$\$\s*\n\s*\$\$', v)))
    # 逐行输出并标出每行 $ 个数（奇数=跨行失配嫌疑）
    for i, line in enumerate(v.split('\n')):
        n = line.count('$')
        mark = ' ⚠️奇数$' if n % 2 else ''
        print('   L%-3d $=%d%s | %s' % (i, n, mark, line[:110]))
