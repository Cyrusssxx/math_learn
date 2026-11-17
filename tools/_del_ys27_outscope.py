# -*- coding: utf-8 -*-
"""删除 27 精选里的三个数一/数三超纲分类（用户 2026-11-17 确认）。

删除范围（严格前置断言，任一不满足即中止）：
  exam_categories.json : L0 50007/50008/50009 + L2 50071/50081/50082/50083/50091/50092/50093
  ys27_items.json      : sections[6:9]（no=20..37，共 18 题）
  _ys27_stems.py       : 对应 STEMS / YS27_CATS / CHAPTERS 条目（防重跑构建复活）
  _audit_ys27.py       : L1 章节数断言 9 -> 6
  _build_ys27.py       : 打印文案 + 已删题 no=36 的选项例外 + 答案序号按 STEMS 上限过滤

写回格式与原文件一致（两 JSON 均 indent=1，categories 无尾换行、items 有尾换行）。
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')
TOOLS = os.path.join(ROOT, 'tools')

DEL_L0 = {50007, 50008, 50009}
DEL_L2 = {50071, 50081, 50082, 50083, 50091, 50092, 50093}
DEL_ALL = DEL_L0 | DEL_L2
DEL_NOS = set(range(20, 38))


def read(p):
    return io.open(p, encoding='utf-8', newline='').read()


def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


# ============ 1. exam_categories.json ============
p = os.path.join(DATA, 'exam_categories.json')
raw = read(p)
cats = json.loads(raw)
present = [str(x) for x in DEL_ALL if str(x) in cats]
assert len(present) == 10, ('待删分类节点数不符', present)
for k in present:
    del cats[k]
# 无残留父子引用
for k, v in cats.items():
    assert v.get('parentId') not in DEL_ALL, ('残留 parentId', k, v.get('parentId'))
assert json.dumps(json.loads(raw), ensure_ascii=False, indent=1) == raw.rstrip('\n'), \
    '原文件格式非 indent=1 无尾换行，中止'
new_raw = json.dumps(cats, ensure_ascii=False, indent=1)
write(p, new_raw)
print('[1/5] exam_categories.json：删 %d 节点，129 -> %d' % (len(present), len(cats)))

# ============ 2. ys27_items.json ============
p = os.path.join(DATA, 'ys27_items.json')
raw = read(p)
paper = json.loads(raw)
assert isinstance(paper, list) and len(paper) == 1
secs = paper[0]['sections']
assert len(secs) == 9, ('章节数不符', len(secs))
removed = []
for s in secs[6:]:
    for q in s['questions']:
        assert set(q.get('categoryIds') or []) <= DEL_ALL, ('待删题分类超出范围', q['no'])
        removed.append(q['no'])
assert set(removed) == DEL_NOS, ('待删题号不符', sorted(removed))
paper[0]['sections'] = secs[:6]
nos = [q['no'] for s in paper[0]['sections'] for q in s['questions']]
assert nos == list(range(1, 20)), ('剩余题号不连续', nos)
new_raw = json.dumps(paper, ensure_ascii=False, indent=1) + '\n'
assert raw.endswith('\n') and len(new_raw) < len(raw)
write(p, new_raw)
print('[2/5] ys27_items.json：删 3 章 / 18 题，剩 %d 章 / %d 题' % (
    len(paper[0]['sections']), len(nos)))

# ============ 3. _ys27_stems.py ============
p = os.path.join(TOOLS, '_ys27_stems.py')
text = read(p)
start_marker = "    dict(\n        no=20, origin='4', kind='choice', source='李艳芳数一第三套第4题"
end_marker = "\n]\n\n# 三级分类：27 模拟卷精选题"
i = text.index(start_marker)
j = text.index(end_marker, i)
text = text[:i] + text[j:]
for n in sorted(DEL_NOS):
    assert ('no=%d, origin=' % n) not in text, ('STEM 残留 no=%d' % n)
# 删 CATS 与 CHAPTERS 中目标 id 所在行
lines = text.split('\n')
kept = []
for line in lines:
    m = re.search(r'\bid=(\d+),', line)
    if m and int(m.group(1)) in DEL_ALL:
        continue
    m2 = re.match(r"\s*\((\d+),\s*'", line)
    if m2 and int(m2.group(1)) in DEL_ALL:
        continue
    kept.append(line)
text = '\n'.join(kept)
for x in sorted(DEL_ALL):
    assert not re.search(r'\bid=%d\b' % x, text), ('CATS 残留 id=%d' % x)
    assert not re.match(r'\s*\(%d,' % x, text, re.M), ('CHAPTERS 残留 id=%d' % x)
write(p, text)
print('[3/5] _ys27_stems.py：删 18 STEMS + 10 CATS + 3 CHAPTERS')

# ============ 4. _audit_ys27.py ============
p = os.path.join(TOOLS, '_audit_ys27.py')
text = read(p)
old = "    if len(l1) != 9:\n        bad('分类', 'L1 章节数 %d（应为 9）' % len(l1))"
new = "    if len(l1) != 6:\n        bad('分类', 'L1 章节数 %d（应为 6）' % len(l1))"
assert old in text, '审计断言原文未找到'
write(p, text.replace(old, new, 1))
print('[4/5] _audit_ys27.py：L1 章节断言 9 -> 6')

# ============ 5. _build_ys27.py ============
p = os.path.join(TOOLS, '_build_ys27.py')
text = read(p)
old = "print('分类表：新增 %d 个节点（L0 1 + L1 9 + L2 %d），共 %d' % ("
new = "print('分类表：新增 %d 个节点（L0 1 + L1 6 + L2 %d），共 %d' % ("
assert old in text, '构建打印文案未找到'
text = text.replace(old, new, 1)
old2 = """            if q['kind'] == 'choice':
                # no=36 的四个选项是「三平面位置关系」示意图，整组裁成一张图放进题干，
                # 因此 options 为空（其余选择题必须 4 个文字选项）
                assert len(q['options']) == 4 or (not q['options'] and '![' in q['stem']), \\
                    ('选项数不是 4', q['no'])
"""
new2 = """            if q['kind'] == 'choice':
                assert len(q['options']) == 4, ('选项数不是 4', q['no'])
"""
assert old2 in text, 'no=36 选项例外原文未找到'
text = text.replace(old2, new2, 1)
old3 = """    nos = sorted(ans)
    if nos != list(range(1, len(STEMS) + 1)):
"""
new3 = """    max_no = max(s['no'] for s in STEMS)
    nos = sorted(n for n in ans if n <= max_no)   # 忽略已删超纲题的旧答案片段
    if nos != list(range(1, len(STEMS) + 1)):
"""
assert old3 in text, '答案序号检查原文未找到'
text = text.replace(old3, new3, 1)
write(p, text)
print('[5/5] _build_ys27.py：文案/选项例外/答案序号过滤已同步')

print('\n全部删除完成。')
