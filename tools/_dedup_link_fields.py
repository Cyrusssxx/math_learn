#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""关联字段「去冗余 + 去自指」统一化（2026-10-13 用户要求再确认冲突/过多绑定/冗余）。

体检发现三类：
  B2 共 26 道：`linkFix.from` 与 `linkedQidOld` 同值 —— 两处写同一件事；
               且全库**没有一道题只靠 linkedQidOld**（0 道）⇒ linkedQidOld 纯冗余，可废弃。
  B3 共 17 道：`linkFix.from === linkedQid`（自指）—— 迁移源就是主键本身，
               前端 `newKey === old` 会直接 continue，字段无任何作用。
  B4 共  1 道：no=983 `linkedQidDead === linkedQid` —— 该题本就正确关联，
               再登记「死键」自相矛盾（它不需要迁移）。

清理后字段语义单一：
  linkedQid      = 正确关联（主键）
  linkAlias      = 跨年同题别名（会被复制到主键）
  linkFix.from   = 从旧键迁移标记（必须 ≠ linkedQid）
  linkedQidDead  = 曾经的错误关联，仅留痕、不迁移（必须 ≠ linkedQid）
  linkScan       = 自动匹配留痕
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]

    n_old = n_self = n_dead = 0
    for q in qs:
        lq = q.get('linkedQid')
        ff = (q.get('linkFix') or {}).get('from')
        old = q.get('linkedQidOld')
        dead = q.get('linkedQidDead')
        # B2：linkedQidOld 一律删除（信息已被 linkFix.from 覆盖；且无题只靠它）
        if old is not None:
            q.pop('linkedQidOld', None)
            n_old += 1
        # B3：linkFix 自指 → 删除（迁移无意义）
        if ff and lq and ff == lq:
            q.pop('linkFix', None)
            n_self += 1
            ff = None
        # B4：Dead 与主键同值 → 删除（该题已正确关联，不该有死键登记）
        if dead and lq and dead == lq:
            q.pop('linkedQidDead', None)
            n_dead += 1
        # 空 linkFix 对象也清掉
        if isinstance(q.get('linkFix'), dict) and not q['linkFix']:
            q.pop('linkFix', None)

    print('删除 linkedQidOld（冗余）= %d 处' % n_old)
    print('删除自指 linkFix      = %d 处' % n_self)
    print('删除与主键同值的 Dead = %d 处' % n_dead)
    print()

    # ---- 自检 ----
    bad = []
    for q in qs:
        lq = q.get('linkedQid')
        ff = (q.get('linkFix') or {}).get('from')
        dead = q.get('linkedQidDead')
        if q.get('linkedQidOld') is not None:
            bad.append('no=%s 仍有 linkedQidOld' % q['no'])
        if ff and lq and ff == lq:
            bad.append('no=%s linkFix 自指' % q['no'])
        if dead and lq and dead == lq:
            bad.append('no=%s Dead 撞主键' % q['no'])
        if ff and dead and ff == dead:
            bad.append('no=%s linkFix.from 与 Dead 同值' % q['no'])
    # 迁移源唯一性复查
    src = collections.defaultdict(list)
    for q in qs:
        ff = (q.get('linkFix') or {}).get('from')
        if ff:
            src[ff].append(q['no'])
    for k, v in src.items():
        if len(v) > 1:
            bad.append('迁移源 %s 被多题共享 ← %s' % (k, v))
    if bad:
        print('❌ 自检失败 %d 处：' % len(bad))
        for m in bad[:10]:
            print('   ' + m)
        return 1
    print('✅ 自检通过：无冗余 / 无自指 / 无死键撞主键 / 迁移源唯一')
    c = collections.Counter()
    for q in qs:
        sig = []
        if q.get('linkedQid'): sig.append('L')
        if q.get('linkAlias'): sig.append('A')
        if (q.get('linkFix') or {}).get('from'): sig.append('F')
        if q.get('linkedQidDead'): sig.append('D')
        if q.get('linkScan'): sig.append('S')
        c['+'.join(sig) or '(无)'] += 1
    print('字段组合分布：', dict(c.most_common()))
    print('迁移源 %d 个（全部唯一）｜死键 %d 个' % (
        len(src), sum(1 for q in qs if q.get('linkedQidDead'))))

    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
