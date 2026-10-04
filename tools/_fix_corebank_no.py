"""修复 core_bank.json 的题号碰撞。

背景：收藏/笔记/掌握度的主键是 qidOf() = `core-<no>`，**不含章节**。
      原数据 606 题的 no 是全卷连续编号（1~606，0 碰撞）；
      但并入重点题时误改成「每章从 1 重新编号」，导致 146 个题号碰撞
      （同一个 core-6 指向极限#6、一元微分#6、矩阵#6 …），
      用户的收藏/笔记因此串题。

修复：不重排原有 606 题的题号（否则存量标记会再次错位），
      只给新增题分配 607 之后的连续题号。
"""
import io, json, re, sys, unicodedata, argparse
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CUR = 'D:/ai code/math-note/pwa/data/core_bank.json'
OLD = 'E:/workbuddy-data/binaries/node/workspace/_core_old.json'


def norm(s):
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', str(s or ''))
    s = re.sub(r'<!--[\s\S]*?-->', '', s)
    s = re.sub(r'\$[^$]*\$', 'Q', s)
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\s　]', '', s)
    return re.sub(r'[，。、；：？！,.;:?!"\'（）()\[\]{}【】<>《》·—\-_*~`#|]', '', s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    cur = json.loads(open(CUR, encoding='utf-8').read())
    old = json.loads(open(OLD, encoding='utf-8').read())

    # 原 606 题的 (题干归一化 -> [原始 no, ...])。
    # ⚠️ 原库本身有 120 道重复题（486 唯一题干 / 606 题），同一题干可能对应多个题号，
    #    必须按多重集顺序分配，不能用 dict[stem] = no（那会丢掉重复项的题号）。
    oldno = {}
    for s in old[0]['sections']:
        for q in s['questions']:
            oldno.setdefault(norm(q.get('stem')), []).append(q.get('no'))
    for v in oldno.values():
        v.sort()
    maxold = max(n for v in oldno.values() for n in v)
    nold = sum(len(v) for v in oldno.values())
    print('原始题库：%d 题（%d 唯一题干，重复题 %d 道），题号 1~%d'
          % (nold, len(oldno), nold - len(oldno), maxold))

    paper = cur[0]
    allq = [q for s in paper['sections'] for q in s['questions']]
    print('当前题库：%d 题' % len(allq))

    dupbefore = Counter(q.get('no') for q in allq)
    print('修复前碰撞：%d 个题号' % len({k: v for k, v in dupbefore.items() if v > 1}))

    # 1) 还原原有题的题号（重复题按出现顺序逐个领取）
    used = set()
    restored = miss = 0
    for q in allq:
        k = norm(q.get('stem'))
        pool = oldno.get(k)
        if pool:
            no = pool.pop(0)
            if q.get('no') != no:
                q['no'] = no
                restored += 1
            used.add(no)
        else:
            miss += 1
    print('还原原始题号：%d 题改回；新增题 %d 题待分配' % (restored, miss))

    # 2) 新题分配 maxold+1 起的连续题号
    #    注意用 `in oldno` 判断，不能用 `oldno.get(k)`——池子被领空后返回 []（falsy），
    #    会把原题误判成新题重新编号。
    nxt = maxold + 1
    assigned = 0
    for s in paper['sections']:
        for q in s['questions']:
            if norm(q.get('stem')) in oldno:
                continue                       # 原题，已领过原始题号
            while nxt in used:
                nxt += 1
            q['no'] = nxt
            used.add(nxt)
            nxt += 1
            assigned += 1
    print('新题分配题号：%d 题（%d ~ %d）' % (assigned, maxold + 1, nxt - 1))

    # 3) 校验
    dup = {k: v for k, v in Counter(q.get('no') for q in allq).items() if v > 1}
    print('修复后碰撞：%d 个题号 %s' % (len(dup), '✓' if not dup else '✗ ' + str(list(dup)[:8])))
    keyed = sum(1 for s in paper['sections'] for q in s['questions'] if q.get('key'))
    print('题库总量：%d 题（重点 %d 道）' % (len(allq), keyed))

    if args.dry_run:
        print('\n[dry-run] 未写盘')
        return
    out = json.dumps(cur, ensure_ascii=False, separators=(',', ':'))
    open(CUR, 'w', encoding='utf-8').write(out)
    print('\n已写入 %s（%d 字节）' % (CUR, len(out)))


if __name__ == '__main__':
    main()
