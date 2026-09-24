# -*- coding: utf-8 -*-
# 给 96 道「答案仅为选项字母」的题展开答案：字母 → 字母 + 选中项完整内容
import json, io, re

P = 'pwa/data/xd_bank.json'
d = json.load(io.open(P, encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]

n = 0
skipped = []
for q in qs:
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

print('展开题数:', n, '| 跳过(无法解码):', skipped)
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(d, fp, ensure_ascii=False, separators=(',', ':'))

# 复查
d2 = json.load(io.open(P, encoding='utf-8'))
q2 = [q for s in d2[0]['sections'] for q in s['questions']]
left = [q['no'] for q in q2 if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', str(q.get('answer') or '').strip()) and re.search(r'[A-Da-d]', str(q.get('answer') or ''))]
print('复查仍为纯字母:', len(left), left[:5])
# 样例
for no in ('309', '34', '38'):
    q = next((x for x in q2 if str(x['no']) == no), None)
    if q:
        print('no=%s answer=%s' % (no, q['answer'][:100]))