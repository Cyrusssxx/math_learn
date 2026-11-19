# -*- coding: utf-8 -*-
"""把「收藏∩不会∩不熟∩未抽」候选池里，简略副本的答案同步为同题的详细版。

权威方向（逐题人工核对 stem 一致后确定，见 tools/_同步候选全文.txt）：
  core 详细 -> dgy 简略：
    DG900JXB-27      <- core-753
    DG900JXB-1071    <- core-707   （用户举例的积分方程题）
    DG900JXB-1072    <- core-708
    DG900JXB-1226    <- 排除：core 与 dgy 题干不同（方程系数/初值全不同），是两道题，禁止同步
    DG900JXB-1094    <- core-694
    DG900JXB-257     <- core-930（answer 与 idea 均取 core 详细版；dgy 的 idea 反而更长是因为它把 answer 复制进去了）
  exam 详细 -> core 简略（例外，按「取最详细副本」原则）：
    2024数二真题-16   core-1311 <- exam（core 那份是「与同型选择题相同」的跳步版）

只覆盖 answer / idea 两个字段，绝不改 stem/options/kind。
写回格式：core_bank.json = indent=1 无尾换行；dgy_items.json = 单行紧凑无尾换行；exam.json = 单行紧凑无尾换行。
"""
import json, io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')


def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)


def save(fn, obj, indent=None):
    txt = json.dumps(obj, ensure_ascii=False, indent=indent)
    with io.open(os.path.join(DATA, fn), 'w', encoding='utf-8', newline='') as f:
        f.write(txt)


def index_papers(obj):
    """(paperId, str(no)) -> question dict"""
    idx = {}
    papers = obj if isinstance(obj, list) else obj.get('papers', [])
    for p in papers:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                idx[(p.get('id'), str(q.get('no')))] = q
    return idx


core = load('core_bank.json')
dgy = load('dgy_items.json')
exam = load('exam.json')
ic, idg, ie = index_papers(core), index_papers(dgy), index_papers(exam)

# (目标文件, 目标索引, 目标key, 源索引, 源key, 字段列表)
# 只同步 answer 字段：idea 在各源写法不同（有的把答案整段塞进思路），按用户诉求「答案要详细」，
# idea 一律保留各源原样，避免不必要改动。
PLAN = [
    ('dgy', idg, ('DG900JXB', '27'),   ic, ('core', '753'),  ['answer']),
    ('dgy', idg, ('DG900JXB', '1071'), ic, ('core', '707'),  ['answer']),
    ('dgy', idg, ('DG900JXB', '1072'), ic, ('core', '708'),  ['answer']),
    ('dgy', idg, ('DG900JXB', '1094'), ic, ('core', '694'),  ['answer']),
    ('dgy', idg, ('DG900JXB', '257'),  ic, ('core', '930'),  ['answer']),
    ('core', ic, ('core', '1311'),     ie, ('2024数二真题', '16'), ['answer']),
]

changed = []
for tgt_name, tidx, tkey, sidx, skey, fields in PLAN:
    tq = tidx.get(tkey)
    sq = sidx.get(skey)
    assert tq is not None, '目标题不存在: %s %s' % (tgt_name, tkey)
    assert sq is not None, '源题不存在: %s %s' % (skey,)
    for fld in fields:
        before = str(tq.get(fld) or '')
        after = str(sq.get(fld) or '')
        assert len(after) >= len(before), '同步源反而更短：%s %s %s (%d<%d)' % (tgt_name, tkey, fld, len(after), len(before))
        tq[fld] = sq[fld]
        changed.append((tgt_name, tkey, fld, len(before), len(after)))

save('core_bank.json', core, indent=1)
save('dgy_items.json', dgy, indent=None)

for name, key, fld, b, a in changed:
    print('%-5s %-24s %-7s %4d -> %4d' % (name, str(key), fld, b, a))
print('同步字段数:', len(changed), '| 题数:', len(PLAN))
