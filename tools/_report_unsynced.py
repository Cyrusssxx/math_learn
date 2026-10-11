#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成「真题标记 ↔ 核心题库」同步状况报告 → tools/_unsynced_report.md

口径：用户标注键 K 在**核心题库（core）模式**下能否看到
      ⟺ 存在 core 题主键 == K，或 K 是某 core 题的 linkAlias（会被复制到主键）。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'
OUT = os.path.join(ROOT, 'tools/_unsynced_report.md')


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())

    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    def key_of(q):
        return q['linkedQid'] if q.get('linkedQid') else 'core-%s' % q['no']

    core_keys = set(key_of(q) for q in qs)
    alias_of = set(a for q in qs for a in (q.get('linkAlias') or []))
    # 三个历史一次性迁移的落点（category.js）：
    #   'core-<no>'→linkedQid / 'xd-<xdNo>'→key_of / linkFix.from|linkedQidOld→key_of
    mig = {}
    for q in qs:
        if q.get('linkedQid'):
            mig['core-%s' % q['no']] = q['linkedQid']
        if q.get('fromX') and q.get('xdNo') is not None:
            mig['xd-%s' % q['xdNo']] = key_of(q)
        old = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if old:
            mig[old] = key_of(q)

    e = ann['exam']
    fav = json.loads(e['favs'])
    st = json.loads(e['status'])
    note_keys = set(k.replace('examNote-', '') for k in e['notes'])

    def kinds(k):
        o = []
        if k in fav: o.append('收藏')
        if k in st: o.append('状态:' + st[k])
        if k in note_keys: o.append('笔记')
        return '+'.join(o) or '—'

    allmark = set(fav) | set(st) | note_keys

    def vis(k):
        if k in core_keys or k in alias_of:
            return True
        t = mig.get(k)
        return bool(t and t in core_keys)

    unseen = sorted(k for k in allmark if not vis(k))
    seen = sorted(k for k in allmark if vis(k))

    L = []
    w = L.append
    w('# 真题标记 ↔ 核心题库 同步报告')
    w('')
    w('数据源：`数学笔记标注-2026-10-11.json`（用户实际标注导出） × `core_bank.json`（核心题库 1059 题）')
    w('')
    w('## 一、总览')
    w('')
    w('| 项 | 数 |')
    w('|---|---|')
    w('| 用户标注键总数 | %d |' % len(allmark))
    w('| ✅ 核心题库模式可见 | %d（%.1f%%） |' % (len(seen), 100.0 * len(seen) / len(allmark)))
    w('| ❌ 核心题库模式看不到 | %d |' % len(unseen))
    w('| 其中：核心题库未收录该题 | %d |' % sum(1 for k in unseen if k in zp))
    w('| 其中：非真题脏键 | %d |' % sum(1 for k in unseen if k not in zp))
    w('')

    w('## 二、本轮修复（+33 道题的标记同步）')
    w('')
    w('- **补 linkedQid 17 道**：core 里本就有同题却没关联（如 2019-23 矩阵相似、2023-19 区域面积）。')
    w('- **加 linkAlias 16 道**：跨年同题（如 2023-1 与 2016-9 是同一道斜渐近线题），')
    w('  core 只收录一份且主键已被占用，改用别名，前端 `migrateAliasKeys()` 把别名上的')
    w('  收藏/标记/笔记**复制**到主键（复制不移动，真题页两边都可见）。')
    w('')

    z = [k for k in unseen if k in zp]
    o = [k for k in unseen if k not in zp]
    w('## 三、仍看不到的 %d 个真题键（核心题库未收录该题）' % len(z))
    w('')
    w('> 性质：核心题库（大观严选题 + 线代重点题，1059 题）**本身没有这道题**，')
    w('> 不是同步失败。这些标记在「真题（exam）模式」下正常显示。')
    w('')
    w('| 卷 | 个数 |')
    w('|---|---|')
    for p, n in collections.Counter(k.rsplit('-', 1)[0] for k in z).most_common():
        w('| %s | %d |' % (p, n))
    w('')
    w('### 明细')
    w('')
    w('| 键 | 标记 | 题干 |')
    w('|---|---|---|')
    for k in z:
        q = zp[k]
        s = (q.get('stem') or '').replace('\n', ' ').replace('|', '\\|')[:52]
        w('| `%s` | %s | %s |' % (k, kinds(k), s))
    w('')

    w('## 四、非真题脏键 %d 个' % len(o))
    w('')
    for k in o:
        w('- `%s`（%s）' % (k, kinds(k)))
    w('')
    w('> `undefined` 是历史 bug 产物：`ta.dataset.qid` 缺失时仍执行了写盘，')
    w('> 落出 `examNote-undefined`。本轮已在 exam.js / category.js 共 5 处写路径加上')
    w('> `if (ta.dataset.qid)` 守卫，不再产生新脏键（旧键内容保留，未删）。')
    w('')

    io.open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
    print('已写', OUT)
    print('可见 %d / 不可见 %d / 总 %d' % (len(seen), len(unseen), len(allmark)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
