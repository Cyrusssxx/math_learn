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

    w('## 二、本轮修复（两批共 55 道题）')
    w('')
    w('### 2.1 补漏关联（+17 道）')
    w('')
    w('core 里本就有同题却没关联（如 2019-23 矩阵相似、2023-19 区域面积、2026-4 引力题）。')
    w('比对方向改为「从有标记的真题键**反查** core 全库」，才捞出上一批漏掉的题。')
    w('')
    w('### 2.2 跨年同题别名（+16 道）')
    w('')
    w('真题卷之间有重复题（2023-1 与 2016-9 曾被认为是同一道斜渐近线题），core 只收录')
    w('一份、主键被占。linkedQid 是一对一（多链会回潮「一标记整组变」），故改用 `linkAlias`，')
    w('前端 `migrateAliasKeys()` 把别名上的收藏/标记/笔记**复制**到主键（复制不移动）。')
    w('')
    w('### 2.3 清除假关联（38 道）⚠️ 本轮最严重的问题')
    w('')
    w('高维检测的「D2 关联质量」维度发现：**一批 core 题与其 linkedQid 根本不是同一道题**，')
    w('危害大于漏关联 —— 用户在任一边的标记都会显示在另一道无关的题上。例：')
    w('')
    w('| core 题 | 曾错误关联到 | 实际题干差异 |')
    w('|---|---|---|')
    w('| no=222 | 2022-6 | `f(x)=\\|x(1-x)\\|` ≠ `x_n` 有界数列（sim 0.000） |')
    w('| no=189 | 2016-9 | `y=x·ln(e+1/(x-1))` ≠ `y=x³/(1+x²)+arctan(...)` |')
    w('| no=560 | DG900JXB-1115 | `x=cos t` 化简 `y\'\'-xy\'+y=0` ≠ `x=sin t` 化简 `y\'\'-xy\'-4y=0` |')
    w('| no=1016 | DG900JXB-389 | 特征值 `1,2,-2` ≠ `3,0,0` |')
    w('')
    w('处置：')
    w('')
    w('- **27 道直接清除** linkedQid，保留 `linkedQidOld` → 前端 `migrateLinkFixKeys()`')
    w('  把用户标记**复制**到 `core-<no>`（用户当时是在这道题上做的标记，不能让它消失）。')
    w('- **11 道清除 + 别名转正**：这些题的 `linkAlias` 才是真同题，转正为 linkedQid；')
    w('  错键写入 `linkedQidDead`（仅留痕，**绝不迁移** —— 它本就不是同题）。')
    w('')
    w('修复后关联质量：≥0.80 由 403 → **413**，`<0.20` 由 6 → **0**。')
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
