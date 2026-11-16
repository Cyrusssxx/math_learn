# -*- coding: utf-8 -*-
"""只读审计：收藏(examFav) ∩ 不熟/不会(examStatus) 的题目，按答案长度升序导出。

与 _audit_fav_answer_quality.py 的区别：不限制「未抽过 / 无笔记 / 高数」，
只看当前掌握度为不熟或不会、且已收藏的题 —— 用户要检查这批题的答案质量，
优先处理答案较短者。

输出：
  1) 长度分布统计
  2) 全部候选清单（qid / 来源 / ans / idea 长度 / 题干摘要）
  3) 前 N 道最短题的完整 answer/idea/stem 到 tools/_fav_short_dump.txt
"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')
SNAP = r'D:/cjx/下载/download/做题数据-2026-11-16.json'
DUMP = os.path.join(ROOT, 'tools', '_fav_short_dump2.txt')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


snap = load(SNAP)
data = snap['data']
fav = json.loads(data['examFav']) if data.get('examFav') else {}
st = json.loads(data['examStatus']) if data.get('examStatus') else {}
notes = {k[len('examNote-'):]: v for k, v in data.items() if k.startswith('examNote-')}

# ---------- 建 qid -> 题目 映射（多来源，优先 exam 原文）----------
qmap = {}          # qid -> (pid, no, q, src)
aliases = {}       # core/dgy 的题号或 linkedQid -> 真题 qid

exam = load(os.path.join(DATA, 'exam.json'))
for p in exam:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            qid = f"{p['id']}-{q['no']}"
            qmap[qid] = (p['id'], q['no'], q, 'exam')

for fname, src in [('core_bank.json', 'core'), ('dgy_items.json', 'dgy')]:
    d = load(os.path.join(DATA, fname))
    papers = d if isinstance(d, list) else d.get('papers', [])
    for p in papers:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                native = f"{p['id']}-{q['no']}"
                lq = q.get('linkedQid')
                if lq:
                    aliases[native] = lq
                    aliases[str(q['no'])] = lq
                # 只对真题 qid 缺失时补入（不覆盖 exam 原文）
                target = lq or native
                qmap.setdefault(target, (p['id'], q['no'], q, src))
                qmap.setdefault(native, (p['id'], q['no'], q, src))

ys = load(os.path.join(DATA, 'ys27_items.json'))
for p in (ys if isinstance(ys, list) else ys.get('papers', [])):
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            qid = f"{p['id']}-{q['no']}"
            qmap.setdefault(qid, (p['id'], q['no'], q, 'ys27'))

mn = load(os.path.join(DATA, 'mn27_papers.json'))
for p in (mn if isinstance(mn, list) else mn.get('papers', [])):
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            qid = f"{p['id']}-{q['no']}"
            qmap.setdefault(qid, (p['id'], q['no'], q, 'mn27'))

bq = load(os.path.join(DATA, 'bank_questions.json'))
for e in bq.get('items', []):
    q = e.get('q', {})
    paper = e.get('paper', {})
    qid = f"{paper.get('id', '')}-{q.get('no', '')}"
    qmap.setdefault(qid, (paper.get('id'), q.get('no'), q, 'bank'))


def resolve(qid):
    """core/dgy 旧格式 qid 经别名重定向到真题 qid。"""
    seen = set()
    while qid in aliases and qid not in seen:
        seen.add(qid)
        qid = aliases[qid]
    return qid


# ---------- 筛选 ----------
cands = []
for raw_qid, s in st.items():
    if s not in ('unknown', 'unfamiliar'):
        continue
    if raw_qid not in fav:
        continue
    qid = resolve(raw_qid)
    if qid not in qmap:
        cands.append({'qid': raw_qid, 'state': s, 'missing': True, 'answer_len': 0})
        continue
    pid, no, q, src = qmap[qid]
    ans = str(q.get('answer') or '')
    idea = str(q.get('idea') or '')
    cands.append({
        'qid': qid, 'raw_qid': raw_qid, 'state': s, 'src': src, 'pid': pid, 'no': no,
        'kind': q.get('kind'), 'cids': q.get('categoryIds'),
        'stem': str(q.get('stem') or '').replace('\n', ' ')[:120],
        'answer_len': len(ans), 'idea_len': len(idea),
        'answer': ans, 'idea': idea,
        'options': q.get('options'),
        'tips': q.get('tips', {}),
        'has_note': bool(str(notes.get(raw_qid, '') or '').strip()),
    })

cands.sort(key=lambda c: c.get('answer_len', 0))

print('收藏', len(fav), '| 不熟/不会', sum(1 for s in st.values() if s in ('unknown', 'unfamiliar')),
      '| 不熟/不会∩收藏', len(cands), '| 缺题库映射', sum(1 for c in cands if c.get('missing')))
print('来源分布', Counter(c.get('src', 'MISSING') for c in cands))
lens = [c['answer_len'] for c in cands if not c.get('missing')]
buckets = [(0, 50), (50, 100), (100, 200), (200, 400), (400, 800), (800, 10 ** 9)]
print('答案长度分布:', ' '.join(f'{a}-{b}:{sum(1 for x in lens if a <= x < b)}' for a, b in buckets))
print('=' * 110)
for c in cands:
    if c.get('missing'):
        print(f'[MISSING] {c["qid"]:24} {c["state"]}')
        continue
    flag = 'NOTE' if c['has_note'] else '    '
    print(f'[{c["state"]:11}] {c["qid"]:26} {c["src"]:5} ans={c["answer_len"]:4} idea={c["idea_len"]:4} {flag} {str(c["kind"] or ""):6} {c["stem"][:56]}')

# ---------- 导出前 N 道完整内容 ----------
N = 60
with open(DUMP, 'w', encoding='utf-8') as f:
    n = 0
    for c in cands:
        if c.get('missing') or c['answer_len'] > 260:
            continue
        if n >= N:
            break
        n += 1
        f.write(f'\n{"=" * 100}\n#{n} {c["qid"]}  state={c["state"]} src={c["src"]} ans={c["answer_len"]} idea={c["idea_len"]}\n')
        f.write(f'题干: {c["stem"]}\n')
        if c.get('options'):
            f.write('选项: ' + ' | '.join(str(x) for x in c['options']) + '\n')
        f.write(f'--- answer ---\n{c["answer"]}\n')
        f.write(f'--- idea ---\n{c["idea"]}\n')
        if c.get('tips'):
            f.write(f'--- tips ---\n{json.dumps(c["tips"], ensure_ascii=False)}\n')
print(f'\n导出 {n} 道简短题完整内容 -> {DUMP}')
