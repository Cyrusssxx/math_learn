# -*- coding: utf-8 -*-
# 打印 2008数二-22、2022数二-9 完整内容（克拉默法则相关）
import json, io

exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
for pid, no in (('2008数二真题', '22'), ('2022数二真题', '9')):
    v = next(v for v in exam if v['id'] == pid)
    q = next(q for s in v['sections'] for q in s['questions'] if str(q['no']) == no)
    print('=' * 72)
    print('%s-%s' % (pid, no))
    print('STEM:', q.get('stem'))
    print()
    print('ANSWER:', (q.get('answer') or '')[:600])
    print()
    print('IDEA:', (q.get('idea') or '')[:400])
    print()