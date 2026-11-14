# -*- coding: utf-8 -*-
"""mn27_papers.json 专项审计：结构 / LaTeX / 配图 / qid 唯一性。"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
DATA = os.path.join(ROOT, 'pwa', 'data', 'mn27_papers.json')
errs = []
d = json.load(open(DATA, encoding='utf-8'))

# 与真题 qid 不冲突
exam = json.load(open(os.path.join(ROOT, 'pwa', 'data', 'exam.json'), encoding='utf-8'))
exam_ids = {p['id'] for p in exam}
exam_qids = {p['id'] + '-' + str(q['no'])
             for p in exam for s in p.get('sections', []) for q in s.get('questions', [])}

# 卷数不锁死快照：以草稿目录里的题干份数为准（每套一份）
SRC = os.path.join(HERE, 'mn27_ans')
expect = len([f for f in os.listdir(SRC) if re.fullmatch(r'q\d\d_stem\.md', f)])
assert len(d) == expect, f'卷数应为 {expect}（草稿份数），实际 {len(d)}'
seen_qid = set()
seen_pid = set()

for p in d:
    pid = p['id']
    if pid in seen_pid or pid in exam_ids:
        errs.append(f'卷 id 冲突：{pid}')
    seen_pid.add(pid)
    if p.get('group') != 'mock':
        errs.append(f'{pid}: group 不是 mock')
    secs = p.get('sections', [])
    if len(secs) != 3:
        errs.append(f'{pid}: sections 应为 3，实际 {len(secs)}')
    allq = [q for s in secs for q in s.get('questions', [])]
    nos = [q['no'] for q in allq]
    if nos != list(range(1, 23)):
        errs.append(f'{pid}: 题号不连续 {nos}')
    for q in allq:
        n = q['no']
        qid = f'{pid}-{n}'
        if qid in seen_qid or qid in exam_qids:
            errs.append(f'qid 冲突：{qid}')
        seen_qid.add(qid)
        want = 'choice' if n <= 10 else ('blank' if n <= 16 else 'calc')
        if q.get('kind') != want:
            errs.append(f'{qid}: kind={q.get("kind")} 期望 {want}')
        for k in ('stem', 'answer', 'idea'):
            if not (q.get(k) or '').strip():
                errs.append(f'{qid}: 缺 {k}')
        if not q['answer'].startswith('【答案】'):
            errs.append(f'{qid}: answer 未以【答案】开头')
        if '**【解】**' not in q['answer']:
            errs.append(f'{qid}: answer 缺【解】段')
        opts = q.get('options', [])
        if n <= 10:
            if len(opts) != 4:
                errs.append(f'{qid}: 选项数 {len(opts)}')
            for i, o in enumerate(opts):
                if not o.startswith('(' + 'ABCD'[i] + ') '):
                    errs.append(f'{qid}: 第 {i+1} 个选项前缀异常 -> {o[:30]}')
        elif opts:
            errs.append(f'{qid}: 非选择题不应有选项')
        if n >= 17 and '满分' not in q['stem']:
            errs.append(f'{qid}: 解答题缺分值')

        # LaTeX 配对（按字段）
        for k in ('stem', 'answer', 'idea'):
            s = q.get(k) or ''
            if s.count('$') % 2:
                errs.append(f'{qid}.{k}: $ 奇数')
            b = len(re.findall(r'\\begin\{', s))
            e = len(re.findall(r'\\end\{', s))
            if b != e:
                errs.append(f'{qid}.{k}: begin/end = {b}/{e}')
            for ln in s.split('\n'):
                t = ln.strip()
                if t.startswith('$$') and not (t.endswith('$$') and len(t) > 4):
                    errs.append(f'{qid}.{k}: $$ 块未独占行 -> {t[:40]}')
                if re.match(r'^\s*(?:-\s|\d+\.\s)', ln):
                    errs.append(f'{qid}.{k}: 列表前缀 -> {ln.strip()[:40]}')
        for k, v in (q.get('tips') or {}).items():
            if k not in ('gs', 'yc', 'jq', 'zy'):
                errs.append(f'{qid}: 未知 tips 键 {k}')
            if v.count('$') % 2:
                errs.append(f'{qid}.tips.{k}: $ 奇数')

        # 配图引用真实存在
        for src in re.findall(r'!\[[^\]]*\]\(([^)\s]+)\)', q['stem']):
            if not re.match(r'^data/img/[a-zA-Z0-9_./-]+$', src):
                errs.append(f'{qid}: 图片路径不在白名单 {src}')
            if not os.path.isfile(os.path.join(ROOT, 'pwa', src)):
                errs.append(f'{qid}: 图片不存在 {src}')

fig_count = sum(len(re.findall(r'!\[[^\]]*\]\(', q['stem']))
                for p in d for s in p['sections'] for q in s['questions'])
print(f'卷数 {len(d)} / 题数 {len(seen_qid)} / 图片引用 {fig_count}')
if errs:
    print(f'\n发现 {len(errs)} 个问题：')
    for e in errs[:60]:
        print(' -', e)
    sys.exit(1)
print('✓ mn27 数据审计通过')
