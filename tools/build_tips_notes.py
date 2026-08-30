# -*- coding: utf-8 -*-
# build_tips_notes.py — 生成「高数-真题点睛」「线代-真题点睛」两篇聚合笔记挂进笔记站。
# 数据源：pwa/data/exam.json 的 tips 字段 + exam_categories.json 的章名映射。
# 归属链：题目.categoryIds[0]=L2叶子 → 叶子.parentId=L1章 → 章.parentId=L0学科根。
# 输出：D:/ai code/math/导图/高数20-真题点睛.md 与 线代7-真题点睛.md，再跑 build_notes.py 重建。
import json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
EXAM = json.load(open(ROOT / 'pwa' / 'data' / 'exam.json', encoding='utf-8'))
CATS = json.load(open(ROOT / 'pwa' / 'data' / 'exam_categories.json', encoding='utf-8'))
OUT_DIR = ROOT.parent / 'math' / '导图'

# 节点索引：id(str) → 节点
node = {str(c['id']): c for c in CATS.values()}
root_name = {str(c['id']): c['name'] for c in CATS.values() if c['level'] == 0}
# 章：level=1 节点 → (display, 根名)
ch_info = {}
for c in CATS.values():
    if c['level'] == 1:
        ch_info[str(c['id'])] = (c['display'], root_name.get(str(c['parentId']), ''))

def ch_of_leaf(leaf_id):
    """L2 叶子 → (章显示名, 学科根名)；找不到返回 (None, None)"""
    l = node.get(str(leaf_id))
    if not l or l['level'] != 2:
        return (None, None)
    ch = node.get(str(l['parentId']))
    if not ch:
        return (None, None)
    return (ch['display'], root_name.get(str(ch['parentId']), ''))

# 收集：章(cid) → [(year, no, tips)]
chapters = defaultdict(list)
for p in EXAM:
    year = p['year']
    for sec in p['sections']:
        for q in sec['questions']:
            tips = q.get('tips')
            if not tips:
                continue
            cid = (q.get('categoryIds') or [''])[0]
            ch_name, subj = ch_of_leaf(cid)
            if not ch_name:
                continue
            chapters[(subj, ch_name)].append((str(year), q['no'], tips))

def fmt_tips(tips):
    parts = []
    for k, label in (('gs', '公式'), ('yc', '易错'), ('jq', '技巧'), ('zy', '注意')):
        if tips.get(k):
            parts.append(f'**【{label}】** {tips[k].strip()}')
    return ' ；'.join(parts)

def build_note(subj, title):
    # 按章聚合，每章按题数降序
    groups = [(ch_name, items) for (s, ch_name), items in chapters.items() if s == subj]
    groups.sort(key=lambda kv: -len(kv[1]))
    out = [f'# {title}', '']
    for ch_name, items in groups:
        out.append(f'## {ch_name}（{len(items)} 题）')
        out.append('')
        for year, no, tips in items:
            out.append(f'- 📌 **{year}年 {no}题**：{fmt_tips(tips)}')
        out.append('')
    return '\n'.join(out)

gs_n = sum(1 for (s, _), v in chapters.items() if s == '高等数学' for _ in v)
xd_n = sum(1 for (s, _), v in chapters.items() if s == '线性代数' for _ in v)
gsp = OUT_DIR / '高数20-真题点睛.md'
xdp = OUT_DIR / '线代7-真题点睛.md'
gsp.write_text(build_note('高等数学', '高数·真题点睛'), encoding='utf-8')
xdp.write_text(build_note('线性代数', '线代·真题点睛'), encoding='utf-8')
print(f'高数聚合: {gs_n} 题 → {gsp.name}')
print(f'线代聚合: {xd_n} 题 → {xdp.name}')
print('完成。请运行 tools/build_notes.py 重建 notes.json')