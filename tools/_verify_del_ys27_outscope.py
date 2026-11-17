# -*- coding: utf-8 -*-
"""独立验证超纲分类删除：字段级 diff + 无孤儿 + 语法/格式。不修改任何文件。"""
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')
TOOLS = os.path.join(ROOT, 'tools')

DEL_L0 = {50007, 50008, 50009}
DEL_L2 = {50071, 50081, 50082, 50083, 50091, 50092, 50093}
DEL_ALL = DEL_L0 | DEL_L2
DEL_NOS = set(range(20, 38))

fails = []


def ok(name, cond, extra=''):
    print(('  OK  ' if cond else ' FAIL ') + name + ((' | ' + str(extra)) if extra else ''))
    if not cond:
        fails.append(name)


def git_head(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    r = subprocess.run(['git', 'show', 'HEAD:' + rel], cwd=ROOT,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert r.returncode == 0, (rel, r.stderr.decode('utf-8', 'replace'))
    return r.stdout.decode('utf-8')


# ===== 1. exam_categories.json 字段级 diff =====
print('=== exam_categories.json ===')
p = os.path.join(DATA, 'exam_categories.json')
new_raw = io.open(p, encoding='utf-8', newline='').read()
old = json.loads(git_head(p))
new = json.loads(new_raw)
old_ids, new_ids = set(old), set(new)
ok('删除节点集合精确匹配 10 个目标', old_ids - new_ids == {str(x) for x in DEL_ALL},
   sorted(old_ids - new_ids))
ok('无新增/改名节点', new_ids - old_ids == set(), sorted(new_ids - old_ids))
ok('剩余节点逐字段完全一致', all(old[k] == new[k] for k in new_ids))
ok('节点数 129 -> 119', len(old) == 129 and len(new) == 119, (len(old), len(new)))
ok('写回格式 indent=1 无尾换行',
   new_raw == json.dumps(new, ensure_ascii=False, indent=1))
ok('无残留 parentId 指向已删节点',
   all(v.get('parentId') not in DEL_ALL for v in new.values()))
ok('27精选 L1 章节数 6（50001..50006）',
   sorted(int(k) for k, v in new.items() if v.get('parentId') == 50000) ==
   [50001, 50002, 50003, 50004, 50005, 50006])
ok('50000 根节点仍在', '50000' in new and new['50000'].get('level') == 0)

# ===== 2. ys27_items.json 字段级 diff =====
print('\n=== ys27_items.json ===')
p = os.path.join(DATA, 'ys27_items.json')
new_raw = io.open(p, encoding='utf-8', newline='').read()
old_paper = json.loads(git_head(p))
new_paper = json.loads(new_raw)
ok('仍为单卷结构', len(new_paper) == 1)
old_secs, new_secs = old_paper[0]['sections'], new_paper[0]['sections']
ok('章节数 9 -> 6', len(old_secs) == 9 and len(new_secs) == 6)
ok('前 6 章逐字段完全一致（含题）', old_secs[:6] == new_secs[:6])
ok('删除的恰为后 3 章',
   [s['title'] for s in old_secs[6:]] == ['七、级数与曲线积分', '八、概率论', '九、数一专项'],
   [s['title'] for s in old_secs[6:]])
removed = [q['no'] for s in old_secs[6:] for q in s['questions']]
ok('删除题号 20..37 共 18 题', set(removed) == DEL_NOS and len(removed) == 18, sorted(removed))
nos = [q['no'] for s in new_secs for q in s['questions']]
ok('剩余题号连续 1..19', nos == list(range(1, 20)), nos)
ok('写回格式 indent=1 有尾换行',
   new_raw == json.dumps(new_paper, ensure_ascii=False, indent=1) + '\n')
# 无孤儿分类引用
all_cat_ids = {int(k) for k in new}
orphans = [(q['no'], q['categoryIds']) for s in new_secs for q in s['questions']
           if not set(q.get('categoryIds') or []) <= all_cat_ids]
ok('剩余题无孤儿 categoryIds', not orphans, orphans[:5])
# 全库不再有目标分类 id 的引用
stale = []
for fn in os.listdir(DATA):
    if not fn.endswith('.json') or '.bak' in fn:
        continue
    txt = io.open(os.path.join(DATA, fn), encoding='utf-8').read()
    for x in sorted(DEL_ALL):
        if str(x) in txt:
            stale.append((fn, x))
ok('全库 JSON 无目标分类 id 残留', not stale, stale[:10])

# ===== 3. 工具脚本同步 =====
print('\n=== 工具脚本 ===')
for fn in ('_ys27_stems.py', '_audit_ys27.py', '_build_ys27.py'):
    p = os.path.join(TOOLS, fn)
    txt = io.open(p, encoding='utf-8', newline='').read()
    old_txt = git_head(p)
    ok('%s 语法可编译' % fn, compile(txt, fn, 'exec') is not None)
    if fn == '_ys27_stems.py':
        ok('STEMS 无 no=20..37', all(('no=%d, origin=' % n) not in txt for n in DEL_NOS))
        ok('CATS 无 10 个目标 id', all(not re.search(r'\bid=%d\b' % x, txt) for x in DEL_ALL))
        ok('CHAPTERS 无 3 个目标 L0', all(not re.match(r'\s*\(%d,' % x, txt, re.M) for x in DEL_L0))
        ok('前 19 题 STEM 原样保留',
           all(('no=%d, origin=' % n) in txt for n in range(1, 20)))
    if fn == '_audit_ys27.py':
        ok('断言已改 6', 'len(l1) != 6' in txt and 'len(l1) != 9' not in txt)
    if fn == '_build_ys27.py':
        ok('打印文案已改', 'L0 1 + L1 6' in txt and 'L0 1 + L1 9' not in txt)
        ok('no=36 选项例外已删', 'no=36' not in txt)
        ok('答案序号按上限过滤', 'ignored' not in txt and 'n <= max_no' in txt)

print('\n' + ('=' * 50))
print('失败项：%d' % len(fails))
for f in fails:
    print('  - ' + f)
sys.exit(1 if fails else 0)
