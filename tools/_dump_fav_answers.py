# -*- coding: utf-8 -*-
"""导出筛选出的 17 道待抽高数题的完整题干/答案/思路，供逐题人工审查。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


snap = load(r'D:/cjx/下载/download/做题数据-2026-11-16.json')
d = snap['data']
fav = json.loads(d['examFav'])
st = json.loads(d['examStatus'])
draw = json.loads(d['qDraw'])
notes = {k[len('examNote-'):]: v for k, v in d.items() if k.startswith('examNote-')}

cats = load(os.path.join(DATA, 'exam_categories.json'))


def descendants(root_id):
    out = {root_id}
    changed = True
    while changed:
        changed = False
        for k, v in cats.items():
            if v.get('parentId') in out and v['id'] not in out:
                out.add(v['id']); changed = True
    return out


HIGH = descendants(223)
qmap = {}


def ingest(fname, src):
    dd = load(os.path.join(DATA, fname))
    papers = dd if isinstance(dd, list) else dd.get('papers', [])
    for p in papers:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                qid = q.get('linkedQid') or f"{p['id']}-{q['no']}"
                qmap[qid] = (q, src)


for f, s in [('exam.json', 'exam'), ('core_bank.json', 'core'), ('dgy_items.json', 'dgy'), ('ys27_items.json', 'ys27')]:
    ingest(f, s)
bq = load(os.path.join(DATA, 'bank_questions.json'))
for e in bq.get('items', []):
    q = e.get('q', {})
    qmap.setdefault(f"{e.get('paper',{}).get('id','')}-{q.get('no','')}", (q, 'bank'))

rows = []
for qid in fav:
    if st.get(qid) not in ('unknown', 'unfamiliar'):
        continue
    rec = draw.get(qid, {})
    if isinstance(rec, dict) and (rec.get('d') or 0) > 0:
        continue
    if str(notes.get(qid, '') or '').strip():
        continue
    if qid not in qmap:
        continue
    q, src = qmap[qid]
    cids = [int(c) for c in (q.get('categoryIds') or []) if str(c).isdigit()]
    if not any(c in HIGH for c in cids):
        continue
    rows.append((qid, st[qid], src, q))

rows.sort(key=lambda r: len(str(r[3].get('answer') or '')))
out = []
for qid, state, src, q in rows:
    out.append('=' * 90)
    out.append(f"[{state}] {qid}  src={src}  kind={q.get('kind')}  cids={q.get('categoryIds')}")
    out.append('--- 题干 ---')
    out.append(str(q.get('stem') or ''))
    if q.get('options'):
        out.append('--- 选项 ---')
        out.append('\n'.join(str(o) for o in q['options']))
    out.append('--- 答案 ---')
    out.append(str(q.get('answer') or '(空)'))
    out.append('--- 思路 ---')
    out.append(str(q.get('idea') or '(空)'))
    tips = q.get('tips') or {}
    if tips:
        out.append('--- tips ---')
        out.append(json.dumps(tips, ensure_ascii=False, indent=1))

path = os.path.join(ROOT, 'tools', '_fav_answers_dump.txt')
with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print(f'dumped {len(rows)} questions -> {path}')
print('qids:', [r[0] for r in rows])
