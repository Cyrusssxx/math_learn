"""把大观园题库中「900 题」与「姜晓千」的题目抽成独立题库 → pwa/data/dagyuan_bank.json

为什么要独立文件而不是并进 core_bank：
  用户的分类题库有三个数据源（真题 / 核心题库 / 大观园），大观园是**另一套书**，
  独立成源才能单独切换、单独统计，互不影响。

⚠️ 铁律（见 2026-10-04 P0 事故）：`no` 是收藏/笔记的隐式主键（qidOf = `paperId-<no>`），
   **必须全卷唯一**，新题只能用 max(no)+1 之后的号；且这些题不设 linkedQid（不与真题抢主键）。

用法：python tools/_gen_dagyuan_bank.py [--dry-run]
"""
import io, json, re, sys, os, argparse, unicodedata
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DG = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
OUT = ROOT + '/pwa/data/dagyuan_bank.json'
CATS = ROOT + '/pwa/data/exam_categories.json'


def norm(s):
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', str(s or ''))
    s = re.sub(r'<!--[\s\S]*?-->', '', s)
    s = re.sub(r'\$[^$]*\$', 'Q', s)
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\s　]', '', s)
    return re.sub(r'[，。、；：？！,.;:?!"\'（）()\[\]{}【】<>《》·—\-_*~`#|]', '', s)


def build_mapper():
    """大观园节点 id -> 我们的 catId：先 id 直连，再同名，最后沿父链上溯"""
    C = {str(c['id']): c for c in json.load(open(DG + 'categories.json', encoding='utf-8'))['items']}
    ours = json.load(open(CATS, encoding='utf-8'))
    O = {str(v['id']): v for v in ours.values()}
    name2oid = defaultdict(list)
    for oid, v in O.items():
        name2oid[v['name']].append(oid)

    def mapper(cid):
        seen, cur = set(), str(cid)
        while cur and cur not in seen:
            seen.add(cur)
            if cur in O:
                return cur
            node = C.get(cur)
            if not node:
                return None
            nm = (node.get('name') or '').strip()
            if nm in name2oid:
                return name2oid[nm][0]
            p = node.get('parentId')
            cur = str(p) if p not in (None, '') else None
        return None
    return mapper, O, C


def chapter_of(O, cid):
    seen, cur = set(), str(cid)
    while cur and cur not in seen:
        seen.add(cur)
        v = O.get(cur)
        if not v:
            return None
        if v['level'] == 1:
            return v['name']
        if v['level'] == 0:
            return v['name']
        cur = str(v.get('parentId'))
    return None


# 数二范围外：数二只考「高数（不含无穷级数、空间解析几何、三重积分、曲线曲面积分）」+「线代」。
# 大观园把概率统计/级数/数学一专项也编进了同一套分类树，入库前按其**二级章节名**剔除。
SHU2_EXCLUDE = {
    '概率统计', '级数', '数学一专项', '归档分类', '归档分类 #961',
    '曲线积分与曲面积分', '空间解析几何与三重积分', '多元积分', '曲线积分', '曲面积分',
}


def dg_path(q, C):
    """大观园自己的完整分类路径（一级学科 → 二级章节 → …），用于范围过滤"""
    cids = q.get('categoryIds') or []
    if not cids:
        return []
    p, node = [], C.get(str(cids[0]))
    while node and len(p) < 8:
        p.append((node.get('name') or '').strip())
        node = C.get(str(node.get('parentId')))
    return list(reversed(p))


def dg_chapter(q, C):
    """二级章节名（用于兜底归章）"""
    p = dg_path(q, C)
    return p[1] if len(p) >= 2 else (p[0] if p else None)


def kind_of(q):
    if q.get('options'):
        return 'choice'
    stem = q.get('stem') or ''
    if re.search(r'_{3,}|＿{2,}|填空', stem):
        return 'blank'
    if re.search(r'证明|求证|证[:：]', stem):
        return 'proof'
    return 'calc'


def build_answer(q):
    a = str(q.get('answer') or '').strip()
    e = re.sub(r'\n{3,}', '\n\n', str(q.get('explanation') or '').strip())
    head = a if (not a or a.startswith('【答案】')) else '【答案】%s' % a
    return (head + '\n\n' + e).strip() if e else head


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    mapper, O, C = build_mapper()
    allq = json.load(open(DG + 'questions.json', encoding='utf-8'))['items']

    def src_of(x):
        return str(x.get('source') or '')

    picked = [x for x in allq if '900' in src_of(x) or '姜晓千' in src_of(x)]

    # 按题干去重（同题多出处），并把多个出处合并进 source
    merged, order = {}, []
    for x in picked:
        k = norm(x.get('stem'))
        if not k:
            continue
        if k not in merged:
            y = dict(x)
            y['source'] = src_of(x)
            y['_from'] = '900' if '900' in src_of(x) else '姜晓千'
            merged[k] = y
            order.append(k)
        else:
            s = src_of(x)
            if s and s not in merged[k]['source']:
                merged[k]['source'] = (merged[k]['source'] + '；' + s).strip('；')

    buckets, stat, nomap = defaultdict(list), Counter(), 0
    name2oid_all = {v['name']: k for k, v in O.items() if v['level'] == 1}
    skipped_scope = Counter()
    for k in order:
        q = merged[k]
        cat = None
        for cid in (q.get('categoryIds') or []):
            cat = mapper(cid)
            if cat:
                break
        # 数二范围外：路径任一层命中排除名单即剔除
        # （'概率统计'/'归档分类' 是一级学科，'级数'/'数学一专项' 是二级章节，都要查）
        path = dg_path(q, C)
        hit = [seg for seg in path if seg in SHU2_EXCLUDE]
        out_of_scope = hit[0] if hit else None
        if out_of_scope:
            skipped_scope[out_of_scope] += 1
            continue
        if not cat:
            # 大观园只给了顶层节点时，用它自己的章节名兜底（我们的章节同名即可对上）
            nm = dg_chapter(q, C)
            cat = name2oid_all.get(nm) if nm else None
        if not cat:
            nomap += 1
            continue
        src = q['source']
        obj = {
            'no': 0,                       # 占位，写盘前统一分配全卷唯一号
            'kind': kind_of(q), 'type': kind_of(q),
            'stem': q.get('stem') or '',
            'options': q.get('options') or [],
            'answer': build_answer(q),
            'idea': q.get('explanation') or '',
            'categoryIds': [int(cat)], 'catId': int(cat), 'deepCats': [],
            'linkedQid': None,              # 不与真题抢主键
            'source': src,
            'from': q['_from'],
            'status': 'ref-matched',
            'key': True if '重点' in src else False,
        }
        stat[obj['kind']] += 1
        buckets[chapter_of(O, cat) or '其他'].append(obj)

    # 章节按我们分类树的顺序排列，读起来顺
    order_ch = []
    for v in O.values():
        if v['level'] == 1 and v['name'] not in order_ch:
            order_ch.append(v['name'])
    secs, no = [], 0
    for ch in order_ch + [c for c in buckets if c not in order_ch]:
        if ch not in buckets:
            continue
        arr = buckets[ch]
        for q in arr:
            no += 1
            q['no'] = no                    # ⚠️ 全卷唯一
        secs.append({'title': ch, 'questions': arr})

    total = sum(len(s['questions']) for s in secs)
    keyed = sum(1 for s in secs for q in s['questions'] if q['key'])
    print('=== 大观园 900题 + 姜晓千 → dagyuan_bank.json ===')
    print('  原始条数            : %d' % len(picked))
    print('  按题干去重后        : %d 道' % (total + nomap))
    print('  数二范围外被剔除    : %d 道 %s' % (sum(skipped_scope.values()), dict(skipped_scope)))
    print('  无分类映射被跳过    : %d 道' % nomap)
    print('  实际入库            : %d 道' % total)
    print('  题号范围            : 1 ~ %d（全卷唯一）' % no)
    print('  带「重点」标记      : %d 道' % keyed)
    print('  题型分布            : %s' % dict(stat))
    print('  来源分布            : %s' % dict(Counter(q['from'] for s in secs for q in s['questions'])))
    print('  章节 (%d 个)        : %s' % (len(secs), '、'.join('%s%d' % (s['title'], len(s['questions'])) for s in secs)))

    if args.dry_run:
        print('\n[dry-run] 未写盘')
        return
    doc = [{'id': 'dagyuan', 'year': '', 'title': '大观园 900题 + 姜晓千', 'sections': secs}]
    open(OUT, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, separators=(',', ':')))
    print('\n已写入 %s（%d 字节）' % (OUT, os.path.getsize(OUT)))


if __name__ == '__main__':
    main()
