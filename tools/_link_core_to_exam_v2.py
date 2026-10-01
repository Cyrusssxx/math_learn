# -*- coding: utf-8 -*-
"""增强版：归一化保留公式文本（原版把 $...$ 整体删掉导致匹配率低），
   去掉前缀题号 / 卷面标记 / LaTeX 命令差异后重新匹配 core ↔ 数二真题
"""
import json, io, re, difflib, shutil

CORE = 'pwa/data/core_bank.json'
EXAM = 'pwa/data/exam.json'

def norm(s):
    s = str(s or '')
    s = re.sub(r'\\(?:d|t)?frac', 'frac', s)          # \dfrac/\tfrac → \frac
    s = re.sub(r'\\[a-zA-Z]+', '', s)                  # 去 LaTeX 命令名（保留其参数/数字）
    s = s.replace('$', '')
    s = re.sub(r'^\s*[\(\（]?\d{1,2}[\)\）]?\s*[\.\、]?\s*', '', s)   # 去前缀题号 (5) / 13.
    s = re.sub(r'[\(\（]?本题满分[^\)\）]*[\)\）]?', '', s)           # 去卷面分值
    s = re.sub(r'[^0-9a-z\u4e00-\u9fff\u0370-\u03ff]', '', s.lower())
    return s

def parse_year(src):
    m = re.search(r'(19|20)\d{2}', str(src or ''))
    return int(m.group(0)) if m else None

def has_shu2(src):
    return bool(re.search(r'数[一二三]{1,3}', str(src or '')) and '二' in str(src or ''))

with io.open(CORE, encoding='utf-8') as f:
    core = json.load(f)
with io.open(EXAM, encoding='utf-8') as f:
    exam = json.load(f)

exam_idx = {}
for p in exam:
    y = parse_year(p['id'])
    if y is None:
        continue
    exam_idx[y] = [(f"{p['id']}-{q['no']}", norm(q.get('stem', '')), str(q.get('stem'))[:60])
                   for s in p.get('sections', []) for q in s.get('questions', [])]

TH = 0.75
new_links, pairs = [], []
stats = {'cand': 0, 'has': 0, 'new': 0, 'amb': 0, 'none': 0}
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            src = str(q.get('source') or '')
            y = parse_year(src)
            if y is None or not has_shu2(src) or y not in exam_idx:
                continue
            stats['cand'] += 1
            if q.get('linkedQid'):
                stats['has'] += 1
                continue
            a = norm(q.get('stem', ''))
            if len(a) < 8:
                stats['none'] += 1
                continue
            scored = sorted(((difflib.SequenceMatcher(None, a[:200], b[:200]).ratio(), qid, bs) for qid, b, bs in exam_idx[y]),
                            reverse=True)
            best, bestq, bstem = scored[0]
            second = scored[1][0] if len(scored) > 1 else 0
            if best >= TH and (best - second) >= 0.05:
                q['linkedQid'] = bestq
                new_links.append((q.get('no'), bestq, round(best, 3)))
                stats['new'] += 1
                if len(pairs) < 25:
                    pairs.append((round(best, 3), q.get('no'), src, bestq,
                                  str(q.get('stem'))[:48], bstem))
            elif best >= TH:
                stats['amb'] += 1
            else:
                stats['none'] += 1

print('统计:', stats)
print(f"\n新匹配 {len(new_links)} 对（相似度降序，供抽检）:")
for r, no, src, qid, stem, bstem in sorted(pairs, reverse=True):
    print(f'\n[{r}] core no={no} ({src}) ↔ {qid}')
    print(f'   core: {stem}')
    print(f'   exam: {bstem}')

shutil.copy(CORE, CORE + '.bak')
with io.open(CORE, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

with io.open(CORE, encoding='utf-8') as f:
    chk = json.load(f)
linked = sum(1 for p in chk for s in p.get('sections', []) for q in s.get('questions', []) if q.get('linkedQid'))
total = sum(1 for p in chk for s in p.get('sections', []) for q in s.get('questions', []))
print(f'\n写回完成：core {total} 题中 {linked} 题带 linkedQid（{linked / total * 100:.1f}%）')
