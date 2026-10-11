#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ①：20 道「混入线代分类的高数题」

逐题核对结论（2026-10-11，题干全文 vs core 既有题相似度 + 真题侧权威分类）：
  · 12 道与 core 既有高数题**内容重复**（同题不同写法/带题号前缀）→ 删除，core 里已有正确位置的那份
      766=189 / 865=221 / 1002=375 / 1042=466 （相似度 ≥0.93）
      825=382 / 849=320 / 869=373 / 892=43 / 917=389 / 962=92 / 998=159 / 1043=40 （题干全文逐字相符，仅写法/括注差异）
  · 3 道是 xd 内部重复 → 删除（保留 no 更小的那份）
      931=860 / 921=906 / 961=906
  · 5 道为独立题且 linkedQid 指向的真题**同题**（题干相同）→ 按真题侧权威分类改挂
      860 2000数二-1 / 863 2005数二-5 / 906 2001数二-1 / 913 2004数二-1 / 985 2009数二-2
      权威分类均为「高等数学 / 极限 / 极限」
⚠️ 不重编 no（no 是收藏/标记主键，重编会让用户标记失效；留空洞无妨）
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')

DEL = [766, 825, 849, 865, 869, 892, 917, 962, 998, 1002, 1042, 1043, 931, 921, 961]
KEEP = [860, 863, 906, 913, 985]


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q

    secs = cb[0]['sections']
    before = sum(len(s['questions']) for s in secs)

    # ---- 1) 删除 ----
    killed = []
    for s in secs:
        keep = []
        for q in s['questions']:
            if q['no'] in DEL:
                killed.append((s['title'], q['no'], q.get('xdNo')))
            else:
                keep.append(q)
        s['questions'] = keep

    # ---- 2) 改挂 5 道：categoryIds / catId / deepCats 取真题侧权威值，并移到「极限」节 ----
    moved = []
    moved_qs = []
    for s in secs:
        keep = []
        for q in s['questions']:
            if q['no'] in KEEP:
                lq = q.get('linkedQid')
                z = zp.get(lq) if lq else None
                if not z:
                    raise SystemExit('no=%s 找不到真题侧同题，中止' % q['no'])
                old_cids = q.get('categoryIds')
                q['categoryIds'] = list(z.get('categoryIds') or [])
                q['catId'] = q['categoryIds'][0] if q['categoryIds'] else None
                if z.get('deepCats') is not None:
                    q['deepCats'] = list(z.get('deepCats') or [])
                q['reclassified'] = 'from-线代: %s → 真题权威分类' % old_cids
                moved.append((q['no'], q.get('xdNo'), old_cids, q['categoryIds'], lq))
                moved_qs.append(q)
            else:
                keep.append(q)
        s['questions'] = keep
    # 插到「极限」节
    lim = None
    for s in secs:
        if s['title'] == '极限':
            lim = s
            break
    if lim is None:
        raise SystemExit('未找到「极限」节')
    lim['questions'].extend(moved_qs)

    after = sum(len(s['questions']) for s in secs)
    print('删除 %d 道：' % len(killed))
    for t in killed:
        print('   [%s] no=%s (原xd-%s)' % t)
    print()
    print('改挂 %d 道 → 「极限」节：' % len(moved))
    for t in moved:
        print('   no=%-5s(原xd-%-6s) %s → %s  (linkedQid=%s)' % t)
    print()
    print('题数 %d → %d（应减 15）' % (before, after))
    errs = []
    if after != before - 15:
        errs.append('题数不符')
    nos = [q['no'] for s in secs for q in s['questions']]
    if len(set(nos)) != len(nos):
        errs.append('no 重复')
    if errs:
        print('❌ 自检失败:', errs)
        return 1
    print('✅ 自检通过')
    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
