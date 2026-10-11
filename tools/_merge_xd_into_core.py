#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 xd_bank.json（线代重点题 333 题）物理并入 core_bank.json。

设计决策（2026-10-11 用户拍板执行）：
  1. **现有 core 741 题的 no 一律不动** —— no 是收藏/标记/笔记的隐式主键
     （qid = core-<no>，经 linkedQid 重定向）。动了 = 用户标记全丢。
  2. xd 333 题重编 no：743 起连续分配（现有 core no 最大值 742）。
     xd 原 no 有 'SUP01'/'SUP10' 等非数字，且与 core 数字区间有 255 处冲突，必须重编。
  3. **保留原号**：写进 q.xdNo（如 '161'），供 migrateXdLegacyKeys() 把用户旧的
     'xd-161' 标记搬到新主键 —— 这是不可省略的一步，否则用户 31 个标记会消失。
  4. 线上题打 fromX=true + status='merged-xd'：exam 模式要据此把线代重点题并入
     （原本它读 xd_bank.json，并入后改从 core_bank 过滤）。
  5. section 对齐：xd 的「一、行列式」等 6 节去掉序号前缀，与 core 现有 4 个线代节
     按标题合并；core 没有的（行列式/向量）新建。最终 12 节 = 6 高数 + 6 线代。
  6. 字段补全：xd 缺 kind/type/catId，按 rule 推断补齐（UI 渲染依赖 kind）。

用法：
  python tools/_merge_xd_into_core.py --check     # 只体检，不写文件
  python tools/_merge_xd_into_core.py --apply     # 写回 core_bank.json
"""
import io, json, re, sys, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
XD = os.path.join(ROOT, 'pwa/data/xd_bank.json')

# xd section 名 → core section 名（去「一、」这类序号前缀）
SEC_MAP = {
    '一、行列式': '行列式',
    '二、矩阵': '矩阵',
    '三、向量': '向量',
    '四、线性方程组': '线性方程组',
    '五、特征值与特征向量': '特征值与特征向量',
    '六、二次型': '二次型',
}
# 线代节的最终顺序（高数 6 节之后）
LA_ORDER = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型']

RE_BLANK = re.compile(r'\\underline|___|（\s*）|\(\s*\)')
RE_PROOF = re.compile(r'证明|试证|求证')


def guess_kind(q):
    """推断题型：UI 渲染依赖 kind（choice 画选项 / blank 画填空 / calc、proof 画解答）。
    xd 题原本没有 kind 字段，只能按题面特征推断。"""
    if q.get('options'):
        return 'choice'
    st = q.get('stem') or ''
    if RE_BLANK.search(st):
        return 'blank'
    if RE_PROOF.search(st) or RE_PROOF.search(q.get('answer') or ''):
        return 'proof'
    return 'calc'


def main():
    apply = '--apply' in sys.argv
    core = json.loads(io.open(CORE, encoding='utf-8').read())
    xd = json.loads(io.open(XD, encoding='utf-8').read())
    if isinstance(core, dict):
        core = core.get('papers') or core.get('items') or core
    if isinstance(xd, dict):
        xd = xd.get('papers') or xd.get('items') or xd

    paper = core[0]
    cqs = [q for s in paper['sections'] for q in s['questions']]
    xqs = [q for s in xd[0]['sections'] for q in s['questions']]
    print('并入前：core %d 题 / xd %d 题' % (len(cqs), len(xqs)))

    # 已有 xdNo 说明跑过一次 —— 幂等保护
    if any(q.get('fromX') for q in cqs):
        print('⚠️ core_bank 里已存在 fromX 标记，疑似已并入过。中止以避免重复。')
        return 1

    used = set(q['no'] for q in cqs)
    next_no = max(n for n in used if isinstance(n, int)) + 1
    print('新号起点 =', next_no, ' 现有 no 最大值 =', max(n for n in used if isinstance(n, int)))

    # ---- 建节表：高数节保持原序，线代节按 LA_ORDER 重排 ----
    secs = {}
    for s in paper['sections']:
        secs[s['title']] = s
    la_existing = [s['title'] for s in paper['sections'] if s['title'] in LA_ORDER]
    print('core 现有线代节 =', la_existing)

    # ---- 逐题并入 ----
    merged = 0
    no_map = {}          # xd 原号 → 新号（供自检/迁移核对）
    new_la = collections.defaultdict(list)
    kind_dist = collections.Counter()
    for xs in xd[0]['sections']:
        title = SEC_MAP.get(xs['title'], xs['title'])
        if title not in LA_ORDER:
            print('⚠️ 未知 xd 节名，跳过：', xs['title'])
            continue
        for q0 in xs['questions']:
            q = json.loads(json.dumps(q0, ensure_ascii=False))   # 深拷贝
            old_no = str(q0['no'])
            new_no = next_no
            next_no += 1
            no_map[old_no] = new_no
            kind = guess_kind(q0)
            kind_dist[kind] += 1
            cids = [int(c) for c in (q0.get('categoryIds') or [])]
            newq = {
                'no': new_no,
                'kind': kind,
                'type': kind,
                'stem': q0.get('stem', ''),
                'options': q0.get('options') or [],
                'answer': q0.get('answer', ''),
                'idea': q0.get('idea', ''),
                'source': q0.get('source', ''),
                'categoryIds': cids,
                'catId': cids[0] if cids else None,
                'deepCats': q0.get('deepCats') or [],
                'fromX': True,          # 来源标记：exam 模式据此并入
                'xdNo': old_no,         # 原号：用户旧标记迁移用
                'status': 'merged-xd',
            }
            if q0.get('linkedQid'):
                newq['linkedQid'] = q0['linkedQid']
            new_la[title].append(newq)
            merged += 1
    print('并入 %d 题，kind 推断分布 = %s' % (merged, dict(kind_dist)))

    # ---- 重排节：高数节原样 + 线代节（core 原有题在前，xd 并入在后）----
    hi = [s for s in paper['sections'] if s['title'] not in LA_ORDER]
    la = []
    for t in LA_ORDER:
        base = secs.get(t)
        qs = list(base['questions']) if base else []
        qs.extend(new_la.get(t, []))
        la.append({'title': t, 'questions': qs})
    paper['sections'] = hi + la

    # ---- 自检 ----
    allq = [q for s in paper['sections'] for q in s['questions']]
    errs = []
    if len(allq) != len(cqs) + len(xqs):
        errs.append('题数不符 %d != %d' % (len(allq), len(cqs) + len(xqs)))
    nos = [q['no'] for q in allq]
    if len(set(nos)) != len(nos):
        errs.append('no 有重复')
    old_nos = set(q['no'] for q in cqs)
    if not old_nos.issubset(set(nos)):
        errs.append('原有题号被改动')
    if sum(1 for q in allq if q.get('fromX')) != len(xqs):
        errs.append('fromX 数量不符')
    for q in allq:
        if not (q.get('answer') or '').strip():
            errs.append('空 answer: no=%s' % q['no']); break
        if not (q.get('stem') or '').strip():
            errs.append('空 stem: no=%s' % q['no']); break
    print('并入后：%d 题 / %d 节' % (len(allq), len(paper['sections'])))
    for s in paper['sections']:
        print('   %-16s %4d 题' % (s['title'], len(s['questions'])))
    if errs:
        print('❌ 自检失败：'); [print('   - ' + e) for e in errs]
        return 1
    print('✅ 自检通过（题数/唯一性/原号不变/字段完整）')

    if not apply:
        print('（--check 模式，未写文件。加 --apply 写回）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(paper and core, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    # 落一份迁移表备查（旧 xd 号 → 新 core 号）
    mp = os.path.join(ROOT, 'tools/_xd_no_map.json')
    io.open(mp, 'w', encoding='utf-8').write(json.dumps(no_map, ensure_ascii=False, sort_keys=True))
    print('迁移表已写', mp, '（%d 条）' % len(no_map))
    return 0


if __name__ == '__main__':
    sys.exit(main())
