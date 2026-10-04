"""把大观园题库中 source 含「重点」的题并入 core_bank.json（数二核心题库）

背景：大观园 app 的 questions.json 没有独立的「重点」字段，重点标记混在 source 里
      （如「姜晓千真题同源 150（重点）」「900 题数二第五章 C 类 2(重点)」，全/半角括号混用）。
      本脚本按「source 含『重点』」筛出题目，映射到我们的三级分类树，写进核心题库，
      并给题卡打上 key 标记（前端显示「重点」徽章）。

用法：
    python tools/_merge_zhongdian.py --dry-run    # 只统计不写盘
    python tools/_merge_zhongdian.py             # 实际写入
"""
import io, json, re, sys, os, unicodedata, argparse
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DG = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
CORE = ROOT + '/pwa/data/core_bank.json'
CATS = ROOT + '/pwa/data/exam_categories.json'

KEY_RE = re.compile(r'重点')


def norm(s):
    """题干归一化，用于跨库去重（公式整体压成 Q，规避写法差异）"""
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', str(s or ''))
    s = re.sub(r'<!--[\s\S]*?-->', '', s)
    s = re.sub(r'\$[^$]*\$', 'Q', s)
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[\s　]', '', s)
    return re.sub(r'[，。、；：？！,.;:?!"\'（）()\[\]{}【】<>《》·—\-_*~`#|]', '', s)


def build_mapper():
    """大观园节点 id -> 我们的 catId。先试 id 直连，再试同名，最后沿父链上溯。"""
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
    return mapper, O


def chapter_of(O, cid):
    """取该 catId 所属的章节名（向上走到 level==1；到 level 0 就用学科名）"""
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


def kind_of(q):
    """大观园 type -> 我们的 kind：choice 选择 / blank 填空 / calc 解答 / proof 证明"""
    if q.get('options'):
        return 'choice'
    stem = q.get('stem') or ''
    if re.search(r'_{3,}|＿{2,}|填空', stem):
        return 'blank'
    if re.search(r'证明|求证|证[:：]', stem):
        return 'proof'
    return 'calc'


def build_answer(q):
    """统一成「【答案】X\\n\\n解析」的格式（分类页只渲染 answer，不单独渲染 idea）"""
    a = str(q.get('answer') or '').strip()
    e = re.sub(r'\n{3,}', '\n\n', str(q.get('explanation') or '').strip())
    head = '【答案】%s' % a if a and not a.startswith('【答案】') else a
    return (head + '\n\n' + e).strip() if e else head


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    core_raw = open(CORE, encoding='utf-8').read()
    core = json.loads(core_raw)
    mapper, O = build_mapper()

    paper = core[0]
    mine = {}
    for s in paper['sections']:
        for q in s.get('questions') or []:
            mine[norm(q.get('stem'))] = q

    allq = json.load(open(DG + 'questions.json', encoding='utf-8'))['items']
    hits = [q for q in allq if KEY_RE.search(q.get('source') or '')]

    # 大观园里同一道题常被多本书重复收录（实测 167 道只有 142 个唯一题干，
    # 最极端的一组 8 个出处：人大2001/浙大2009/江苏省1994/东南大学2010/…）。
    # 按归一化题干去重，并把多个出处合并进 source，避免导入 8 份相同题目。
    merged, order = {}, []
    for q in hits:
        k = norm(q.get('stem'))
        if k not in merged:
            merged[k] = dict(q)
            merged[k]['source'] = str(q.get('source') or '')
            order.append(k)
        else:
            src = str(q.get('source') or '').strip()
            if src and src not in merged[k]['source']:
                merged[k]['source'] = (merged[k]['source'] + '；' + src).strip('；')
    uniq = [merged[k] for k in order]

    flagged = 0
    added = 0
    stat = Counter()
    buckets = defaultdict(list)          # 章节名 -> [题对象]

    for q in uniq:
        cat = None
        for cid in (q.get('categoryIds') or []):
            cat = mapper(cid)
            if cat:
                break
        if not cat:
            stat['无分类'] += 1
            continue
        k = norm(q.get('stem'))
        if k in mine:
            mine[k]['key'] = True       # 已在核心题库里的，只补标记，不重复插入
            flagged += 1
            continue
        obj = {
            'no': 0,          # 占位，写盘前统一分配全卷唯一号
            'kind': kind_of(q),
            'type': kind_of(q),
            'stem': q.get('stem') or '',
            'options': q.get('options') or [],
            'answer': build_answer(q),
            'idea': q.get('explanation') or '',
            'categoryIds': [int(cat)],
            'catId': int(cat),
            'deepCats': [],
            'linkedQid': None,
            'source': q.get('source') or '',
            'srcPage': None,
            'srcOrder': None,
            'status': 'ref-matched',     # 来自参考题库，非我们视觉转写
            'key': True,
        }
        stat[obj['kind']] += 1
        ch = chapter_of(O, cat) or '其他'
        buckets[ch].append(obj)

    # 写入：已有 section 追加，新章节新建（不改动既有 section 的顺序与内容）
    added = sum(len(v) for v in buckets.values())
    title2sec = {s['title']: s for s in paper['sections']}
    for ch, arr in buckets.items():
        sec = title2sec.get(ch)
        if sec is None:
            sec = {'title': ch, 'questions': []}
            paper['sections'].append(sec)
            title2sec[ch] = sec
        sec.setdefault('questions', []).extend(arr)

    # ⚠️ 绝对不要按 section 重排 no！
    # 收藏/笔记/掌握度的主键是 qidOf() = `core-<no>`，**不含章节**（见 category.js:13）。
    # 原库 606 题的 no 是全卷唯一（1~606）；一旦按章节从 1 重编，
    # 同一个 `core-6` 会同时指向极限#6、一元微分#6、矩阵#6 …，
    # 用户的收藏/笔记就会串题（实测 146 个题号碰撞）。
    # 新题只在追加时于 obj 里预留 no=0，由调用方（或 _fix_corebank_no.py）分配全卷唯一号。
    used = {q.get('no') for s in paper['sections'] for q in s.get('questions') or []}
    used.discard(0)
    nxt = (max(used) if used else 0) + 1
    for s in paper['sections']:
        for q in s.get('questions') or []:
            if q.get('no'):
                continue
            while nxt in used:
                nxt += 1
            q['no'] = nxt
            used.add(nxt)
            nxt += 1

    total = sum(len(s.get('questions') or []) for s in paper['sections'])
    keyed = sum(1 for s in paper['sections'] for q in s.get('questions') or [] if q.get('key'))

    print('=== 大观园「重点」题并入核心题库 ===')
    print('  source 含「重点」    : %d 条' % len(hits))
    print('  按题干去重后        : %d 道（%d 条为多出处重复收录）' % (len(uniq), len(hits) - len(uniq)))
    print('  已在库中·仅补标记    : %d 道' % flagged)
    print('  新增入库            : %d 道' % added)
    print('  类型分布            : %s' % dict(stat))
    print('  涉及章节            : %s' % dict((k, len(v)) for k, v in sorted(buckets.items(), key=lambda kv: -len(kv[1]))))
    print('  核心题库总题数      : %d → %d' % (total - added, total))
    print('  带「重点」标记      : %d 道' % keyed)
    unmapped = stat['无分类']
    if unmapped:
        print('  ⚠️ 无分类映射被跳过: %d 道' % unmapped)

    if args.dry_run:
        print('\n[dry-run] 未写盘')
        return

    out = json.dumps(core, ensure_ascii=False, separators=(',', ':'))
    open(CORE, 'w', encoding='utf-8').write(out)
    print('\n已写入 %s（%d 字节）' % (CORE, len(out)))


if __name__ == '__main__':
    main()
