# -*- coding: utf-8 -*-
# 找用户举例的题（矩阵 a^3+2a+2 / 非齐次方程组无解）并展示全貌
import json, io, re

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]

hits = [q for q in qs if re.search(r'a\^3\s*\+\s*2a\s*\+\s*2', str(q.get('stem') or ''))]
print('匹配题数:', len(hits))
for q in hits:
    print('=' * 70)
    print('no=%s | src=%s' % (q['no'], q.get('source')))
    print('STEM:', (q.get('stem') or '').replace('\n', ' ')[:400])
    print()
    print('OPTIONS:')
    for i, o in enumerate(q.get('options') or []):
        print('   %s. %s' % ('ABCD'[i], str(o)[:80]))
    print()
    print('ANSWER:', repr(q.get('answer')))
    print('IDEA:', (q.get('idea') or '')[:600].replace('\n', ' '))
    print('categoryIds:', q.get('categoryIds'))

# 顺便统计：96 道字母答案题里，有多少能通过 options 解出内容
print()
print('=' * 70)
letter_qs = [q for q in qs if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', str(q.get('answer') or '').strip()) and re.search(r'[A-Da-d]', str(q.get('answer') or ''))]
withopt = [q for q in letter_qs if q.get('options') and len(q['options']) >= 2]
print('字母答案题: %d | 有 options(可解码): %d' % (len(letter_qs), len(withopt)))
print('无 options 的:', [q['no'] for q in letter_qs if not (q.get('options') and len(q['options']) >= 2)])