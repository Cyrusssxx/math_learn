# -*- coding: utf-8 -*-
"""重整合：先移除题库中 p91-119 的旧条目，再从最新 _rest_draft.json 重新收录。"""
import json, io

ROOT = 'D:/ai code/math-note/tools/'
BANK = ROOT + 'yancai_bank.json'

bank = json.load(io.open(BANK, encoding='utf-8'))
before = len(bank['questions'])
bank['questions'] = [q for q in bank['questions'] if not (91 <= q['page'] <= 119)]
print('移除 p91-119 旧条目 %d 条' % (before - len(bank['questions'])))

draft = json.load(io.open(ROOT + '_rest_draft.json', encoding='utf-8'))
existing = {q['id'] for q in bank['questions']}
ok = need = 0
pending = []
for r in draft:
    qid = 'yc-%s-%s' % (r['page'], r['order'])
    if qid in existing:
        continue
    good = (r['score'] is not None and r['score'] >= 0.8 and r['stem'])
    if good:
        opts = r['options']
        if isinstance(opts, list):
            opts = {chr(65 + i): o for i, o in enumerate(opts[:4])} or None
        q = {'id': qid, 'page': r['page'], 'order': r['order'],
             'section_header': r['tag'], 'source': r['source'], 'type': r['type'],
             'stem': r['stem'], 'options': opts, 'catId': None,
             'status': 'ref-matched', 'ref': r['ref'], 'ref_score': r['score']}
        if r.get('answer'):
            q['ref_answer'] = r['answer']
        ok += 1
    else:
        q = {'id': qid, 'page': r['page'], 'order': r['order'],
             'section_header': r['tag'], 'source': r['source'], 'type': r['type'],
             'stem': None, 'options': None, 'catId': None, 'status': 'needs-visual',
             'tl_body': r['body'], 'ref': r['ref'], 'ref_score': r['score']}
        need += 1
        pending.append((qid, r['source'], r['score'], r['body'][:130]))
    bank['questions'].append(q)
    existing.add(qid)

bank['questions'].sort(key=lambda q: (q['page'], q['order']))
bank['meta']['transcribed_pages'] = sorted({q['page'] for q in bank['questions']})
bank['meta']['question_count'] = len(bank['questions'])
bank['meta']['counts'] = {
    'visual': sum(1 for q in bank['questions'] if q['status'] == 'transcribed'),
    'ref-matched': sum(1 for q in bank['questions'] if q['status'] == 'ref-matched'),
    'needs-visual': sum(1 for q in bank['questions'] if q['status'] == 'needs-visual'),
}
with io.open(BANK, 'w', encoding='utf-8', newline='') as f:
    json.dump(bank, f, ensure_ascii=False, indent=1)

print('重新整合：ref-matched %d | needs-visual %d' % (ok, need))
print('题库总数 %d | 分状态 %s' % (len(bank['questions']), bank['meta']['counts']))
print()
print('=== 仍需视觉/人工的 %d 题 ===' % need)
for d in pending:
    print('  [%s] src=%s score=%s' % (d[0], d[1], d[2]))
    print('       %s' % d[3].replace('\n', ' '))
