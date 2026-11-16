# -*- coding: utf-8 -*-
"""只读审计：收藏池里「将要抽到 p 卷」的高数题，检查答案是否过于简略 / 可能有误。

入池条件严格复刻 category.js ppScanPool + ppBuildPool：
  已收藏(examFav) ∩ 状态∈{unknown,unfamiliar} ∩ 未掌握 ∩ qDraw.d<=0(未抽过)
  ∩ 高数(categoryIds 归属高等数学 L0=223) ∩ 未写笔记(examNote-<qid> 为空)
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')
SNAP = r'D:/cjx/下载/download/做题数据-2026-11-16.json'

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

snap = load(SNAP)
data = snap['data']
fav = json.loads(data['examFav']) if data.get('examFav') else {}
st = json.loads(data['examStatus']) if data.get('examStatus') else {}
draw = json.loads(data['qDraw']) if data.get('qDraw') else {}
notes = {k[len('examNote-'):]: v for k, v in data.items() if k.startswith('examNote-')}

cats = load(os.path.join(DATA, 'exam_categories.json'))
# 高等数学 L0=223 的所有子孙节点 id
def descendants(root_id):
    out = {root_id}
    changed = True
    while changed:
        changed = False
        for k, v in cats.items():
            pid = v.get('parentId')
            if pid in out and v['id'] not in out:
                out.add(v['id']); changed = True
    return out
HIGH = descendants(223)

# 建 coreLink：core_bank / dgy / bank 里 linkedQid -> 真实 qid
core_link = {}
qmap = {}   # qid -> {paper, no, q, src}

exam = load(os.path.join(DATA, 'exam.json'))
for p in exam:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            qid = f"{p['id']}-{q['no']}"
            qmap[qid] = (p['id'], q['no'], q, 'exam')

def add_papers(fname, src):
    d = load(os.path.join(DATA, fname))
    papers = d if isinstance(d, list) else d.get('papers', [])
    for p in papers:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                qid = f"{p['id']}-{q['no']}"
                lq = q.get('linkedQid')
                if lq:
                    core_link[qid] = lq
                    core_link[str(q['no'])] = lq
                    qid = lq
                qmap[qid] = (p['id'], q['no'], q, src)

for f, s in [('core_bank.json', 'core'), ('dgy_items.json', 'dgy')]:
    add_papers(f, s)
# ys27
ys = load(os.path.join(DATA, 'ys27_items.json'))
for p in (ys if isinstance(ys, list) else ys.get('papers', [])):
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            qid = f"{p['id']}-{q['no']}"
            qmap[qid] = (p['id'], q['no'], q, 'ys27')
# bank_questions
bq = load(os.path.join(DATA, 'bank_questions.json'))
for e in bq.get('items', []):
    q = e.get('q', {})
    paper = e.get('paper', {})
    qid = f"{paper.get('id','')}-{q.get('no','')}"
    qmap.setdefault(qid, (paper.get('id'), q.get('no'), q, 'bank'))

# 筛选
cands = []
for qid in fav:
    s = st.get(qid)
    if s not in ('unknown', 'unfamiliar'):
        continue
    d = draw.get(qid, {})
    if isinstance(d, dict) and (d.get('d') or 0) > 0:
        continue
    nt = str(notes.get(qid, '') or '').strip()
    if nt:
        continue
    if qid not in qmap:
        cands.append({'qid': qid, 'state': s, 'missing': True})
        continue
    pid, no, q, src = qmap[qid]
    cids = [int(c) for c in (q.get('categoryIds') or []) if str(c).isdigit()]
    is_high = any(c in HIGH for c in cids)
    if not is_high:
        continue
    ans = str(q.get('answer') or '')
    idea = str(q.get('idea') or '')
    cands.append({
        'qid': qid, 'state': s, 'src': src, 'pid': pid, 'no': no,
        'kind': q.get('kind'), 'cids': cids,
        'stem': str(q.get('stem') or '').replace('\n', ' ')[:110],
        'answer_len': len(ans), 'idea_len': len(idea),
        'answer': ans, 'idea': idea,
        'tips': q.get('tips', {}),
    })

print('收藏总数', len(fav), '| 标记', len(st), '| 未抽过 qDraw', sum(1 for v in draw.values() if not (isinstance(v, dict) and v.get('d'))))
print('无笔记 + 收藏 + 不会/不熟 + 未抽过 题数', len([c for c in cands if not c.get('missing')]), '| 缺题库映射', len([c for c in cands if c.get('missing')]))
print('=' * 100)
cands_sorted = sorted(cands, key=lambda c: (c.get('answer_len', 0)))
for c in cands_sorted:
    if c.get('missing'):
        print('[MISSING]', c['qid'], c['state']); continue
    print(f"[{c['state']:11}] {c['qid']:24} src={c['src']:5} ans={c['answer_len']:4} idea={c['idea_len']:4} {c['kind']}")
    print('   题干:', c['stem'])
print('=' * 100)
# 答案疑似过短（<120 字）单独列出
short = [c for c in cands if not c.get('missing') and c['answer_len'] < 120]
print('答案 <120 字的题数:', len(short))
for c in short:
    print('  ', c['qid'], 'ans_len', c['answer_len'], 'idea_len', c['idea_len'])
