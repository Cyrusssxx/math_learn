#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""逐键明细对比 v2：把 category.js 的三个一次性迁移函数（core 旧主键 / xd 旧主键 /
linkFix）纳入计算，得出「用户打开分类页 core 模式后，真正看不到的标记」清单，
并对其中「真题键」在 core 全库里做 top1 相似度复查，找出漏关联的同题。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def norm(s):
    """与项目 normStem 同口径：只剥 LaTeX **结构**符号，保留公式内容。
    ⚠️ 绝不能删 $...$ 内的内容——数学题的主体就是公式，删了会把
       「y'=1/(x+y)^2」和「ydx+(x-3y^2)dy=0」判成 1.000 同题。"""
    s = (s or '')
    # 剥「排版前缀」：core 版常带【例3.47】（2023，数二、三）、【14】、(2) 等，
    # 不剥会把真同题的相似度压到 0.4 以下（实测 2023-19 因此漏网）。
    for _ in range(3):
        s = re.sub(r'^\s*[（(]?\s*本题满分[^）)]*分\s*[）)]?\s*', '', s)
        s = re.sub(r'^\s*【[^】]{1,24}】\s*', '', s)
        s = re.sub(r'^\s*例\s*\d+[.\-]\d+\s*', '', s)
        s = re.sub(r'^\s*[（(]\s*(?:19|20)\d\d[^）)]{0,20}[）)]\s*', '', s)
        s = re.sub(r'^\s*[（(]\s*\d{1,2}\s*[）)]\s*', '', s)
        s = re.sub(r'^\s*\d{1,2}\s*[.、]\s*', '', s)
    s = re.sub(r'\\(?:mathrm|mathbb|mathbf|operatorname)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\(?:left|right|displaystyle|limits|,|;|!|:|\s)+', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)          # 其余 LaTeX 命令名
    s = re.sub(r'[{}\\$\s]', '', s)            # 花括号 / $ / 空白
    s = re.sub(r'[，。、；：,.;:（）()]', '', s)
    return s


def bg(s):
    s = norm(s)
    return set(s[i:i + 2] for i in range(len(s) - 1))


def sim(a, b):
    A, B = bg(a), bg(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


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

    # ---- 迁移映射（模拟 category.js 三个迁移函数的落点）----
    mig = {}          # 旧键 -> 迁移后的新键
    for q in qs:
        # migrateCoreLegacyKeys: 'core-<no>' -> key_of(q)
        if q.get('linkedQid'):
            mig['core-%s' % q['no']] = q['linkedQid']
        # migrateXdLegacyKeys: 'xd-<xdNo>' -> key_of(q)
        if q.get('fromX') and q.get('xdNo') is not None:
            mig['xd-%s' % q['xdNo']] = key_of(q)
        # migrateLinkFixKeys: linkFix.from / linkedQidOld -> key_of(q)
        old = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if old:
            mig[old] = key_of(q)
    # 迁移落点本身可能不是 core 键（例如 xd 题带 linkedQid 时落点是真题键），
    # 但真题键在 exam 模式下本来就可见，不算「看不到」。
    # 只有落点既不在 core_keys 也不在真题键集合里的才算真丢。
    exam_keys = set(zp)

    e = ann['exam']
    fav = json.loads(e['favs'])
    st = json.loads(e['status'])
    note_keys = set(k.replace('examNote-', '') for k in e['notes'])

    def kinds(k):
        out = []
        if k in fav: out.append('收藏')
        if k in st: out.append('状态:' + st[k])
        if k in note_keys: out.append('笔记')
        return out

    # 跨年同题别名：别名键上的标记会被 migrateAliasKeys 复制到该题主键 → core 可见
    alias_of = set()
    for q in qs:
        for a in (q.get('linkAlias') or []):
            alias_of.add(a)

    # 口径甲（用户口径）：core 模式（核心题库）下能否看到该键的标记
    def vis_core(k):
        if k in core_keys:
            return True
        t = mig.get(k)
        if t and t in core_keys:
            return True
        return k in alias_of

    # 口径乙：任一模式可见（exam 模式原键 or core 模式 or 迁移）
    def vis_any(k):
        if k in core_keys or k in exam_keys:
            return True
        t = mig.get(k)
        return bool(t and (t in core_keys or t in exam_keys))

    allmark = set(fav) | set(st) | note_keys
    unseen = sorted(k for k in allmark if not vis_core(k))   # 口径甲：core 模式看不到
    seen = [k for k in allmark if vis_core(k)]
    unseen_any = sorted(k for k in allmark if not vis_any(k))

    print('用户标注键总数 =', len(allmark))
    print('  [口径甲·核心题库模式] ✓ 能看到 =', len(seen), ' ✗ 看不到 =', len(unseen))
    print('  [口径乙·任一模式]     ✓ 能看到 =', len(allmark) - len(unseen_any),
          ' ✗ 看不到 =', len(unseen_any))
    print()

    # 分类：core 模式看不到的键里，真题键 / 非真题键
    z = [k for k in unseen if k in zp]
    o = [k for k in unseen if k not in zp]
    print('=== A. 真题键，core 模式下看不到（%d 个）===' % len(z))
    bypaper = collections.Counter(k.rsplit('-', 1)[0] for k in z)
    for p, n in bypaper.most_common():
        print('     %-22s %d 个' % (p, n))
    print()
    print('=== B. 非真题键（%d 个）===' % len(o))
    for k in o:
        print('     %-20s %s' % (k, '+'.join(kinds(k))))
    print()

    # ---- 对 A 类做 top1 相似度复查：是否存在「core 里其实有同题但没关联」----
    print('=== C. A 类的 top1 相似度复查（找漏关联的同题）===')

    def full(q):
        """题干 + 选项：选择题的区分信息常在选项里，只比题干会漏。"""
        s = q.get('stem') or ''
        for o in (q.get('options') or []):
            s += ' ' + (o if isinstance(o, str) else (o.get('text') or ''))
        return s

    core_norm = [(q, norm(full(q))) for q in qs]
    hits = []
    for k in z:
        src = full(zp[k])
        best, bq = 0.0, None
        for q, ns in core_norm:
            if not ns:
                continue
            s = sim(src, ns)
            if s > best:
                best, bq = s, q
        hits.append((best, k, bq))
    hits.sort(reverse=True)
    n45 = sum(1 for h in hits if h[0] >= 0.45)
    n60 = sum(1 for h in hits if h[0] >= 0.60)
    print('    A 类 %d 个键中：sim>=0.60 有 %d 个，0.45<=sim<0.60 有 %d 个' % (len(hits), n60, n45))
    print()

    # 分两类：(b) top1 是无关联 core 题 -> 直接补 linkedQid 即可（真漏）
    #         (a) top1 已链到别的真题键    -> 跨年同题重复，需要别名机制
    fixable, alias = [], []
    for best, k, bq in hits:
        if best < 0.60:
            break
        (fixable if key_of(bq) == 'core-%s' % bq['no'] else alias).append((best, k, bq))
    print('    【b】可直接补 linkedQid（core 那道题目前无关联）= %d 个' % len(fixable))
    for best, k, bq in fixable:
        print('       sim=%.3f  %-18s %-12s -> core no=%s' % (best, k, '+'.join(kinds(k)), bq['no']))
        print('           真题: %s' % (zp[k].get('stem') or '').replace('\n', ' ')[:66])
        print('           core: %s' % (bq.get('stem') or '').replace('\n', ' ')[:66])
    print()
    print('    【a】core 那道题已链到别的真题键（跨年同题，需别名机制）= %d 个' % len(alias))
    for best, k, bq in alias:
        print('       sim=%.3f  %-18s %-12s -> %s (core no=%s)' % (
            best, k, '+'.join(kinds(k)), key_of(bq), bq['no']))
        print('           真题: %s' % (zp[k].get('stem') or '').replace('\n', ' ')[:66])
        print('           core: %s' % (bq.get('stem') or '').replace('\n', ' ')[:66])
    print()
    print('    —— 剩余全部候选（按 sim 降序，供人工判）——')
    for best, k, bq in hits:
        print('     sim=%.3f  %-18s %-12s | core no=%-5s key=%s' % (
            best, k, '+'.join(kinds(k)), bq['no'], key_of(bq)))
        print('        真题: %s' % full(zp[k]).replace('\n', ' ')[:96])
        print('        core: %s' % full(bq).replace('\n', ' ')[:96])
    return 0


if __name__ == '__main__':
    sys.exit(main())
