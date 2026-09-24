# -*- coding: utf-8 -*-
# 新导入 109 道中 24 道纯字母答案 → 展开为选项内容（与上轮同标准）
import json, io, re

P = 'pwa/data/xd_bank.json'
xd = json.load(io.open(P, encoding='utf-8'))
secs = xd[0]['sections']
newsec = next(s for s in secs if '1987-1999' in s['title'])

n = 0
skipped = []
for q in newsec['questions']:
    a = str(q.get('answer') or '').strip()
    if not re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', a) or not re.search(r'[A-Da-d]', a):
        continue
    letters = re.findall(r'[A-Da-d]', a)
    opts = q.get('options') or []
    parts = []
    for L in letters:
        i = 'abcd'.index(L.lower())
        if 0 <= i < len(opts):
            txt = re.sub(r'^\s*[（(\[]?[A-Da-d][）)\].、:：]?\s*', '', str(opts[i])).strip()
            parts.append('%s. %s' % (L.upper(), txt))
    if not parts:
        skipped.append(q['no'])
        continue
    q['answer'] = '（%s）' % '；'.join(parts)
    n += 1

print('展开:', n, '| 跳过(无options):', skipped)
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(xd, fp, ensure_ascii=False, separators=(',', ':'))

d2 = json.load(io.open(P, encoding='utf-8'))
s2 = next(s for s in d2[0]['sections'] if '1987-1999' in s['title'])
left = [q['no'] for q in s2['questions']
        if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', str(q.get('answer') or '').strip())
        and re.search(r'[A-Da-d]', str(q.get('answer') or ''))]
print('复查仍纯字母:', len(left))
for q in s2['questions'][:2]:
    if '（' in str(q.get('answer')):
        print('样本 no=%s answer=%s' % (q['no'], str(q['answer'])[:90]))
print('总题数:', sum(len(s['questions']) for s in d2[0]['sections']))