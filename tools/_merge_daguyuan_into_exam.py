"""把大观园题库中【900题 + 姜晓千 + 880题】∩ 数二范围的题并入 exam.json（真题/分类题库）。

用户要求：
  - 范围：900题 + 姜晓千 + 880题，且限数二（剔除级数/概率统计/数学一专项等）
  - **排除「选做」题**（用户 2026-10-05 确认）：source 含「选做/选学/加练/选修」的一律不要
  - 并入 exam.json 合并成分类题库，**不单独开数据源**；核心题库 core_bank.json 不动
  - 题卡上显示原书题源

⚠️ 主键铁律：qid = `paperId-<no>`，本文件用独立 paperId（DG900JXB），
   与真题 `<卷id>-<no>`、核心题库 `core-<no>` 天然隔离；且**不设 linkedQid**。

用法：python tools/_merge_daguyuan_into_exam.py [--dry-run]
"""
import io, json, re, sys, os, argparse, unicodedata
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
DG = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
EXAM = ROOT + '/pwa/data/exam.json'
CATS = ROOT + '/pwa/data/exam_categories.json'
PAPER_ID = 'DG900JXB'
# 选做题标记
OPT_RE = re.compile(r'选做|选学|加练|选修')

# 数二不考：级数 / 概率统计 / 数学一专项 / 曲线曲面积分 / 空间解析几何与三重积分 / 归档
SHU2_EXCLUDE = {
    '概率统计', '级数', '数学一专项', '归档分类', '归档分类 #961', '归档分类 #964', '归档分类 #976',
    '曲线积分与曲面积分', '空间解析几何与三重积分', '多元积分', '曲线积分', '曲面积分',
}


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

    dgcats = {str(c['id']): c for c in json.load(open(DG + 'categories.json', encoding='utf-8'))['items']}

    def dg_path(cid):
        p, node = [], dgcats.get(str(cid))
        while node and len(p) < 8:
            p.append((node.get('name') or '').strip())
            node = dgcats.get(str(node.get('parentId')))
        return list(reversed(p))

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
            node = dgcats.get(cur)
            if not node:
                return None
            nm = (node.get('name') or '').strip()
            if nm in name2oid:
                return name2oid[nm][0]
            p = node.get('parentId')
            cur = str(p) if p not in (None, '') else None
        return None

    def chapter_of(cid):
        seen, cur = set(), str(cid)
        while cur and cur not in seen:
            seen.add(cur)
            v = O.get(cur)
            if not v:
                return None
            if v['level'] in (0, 1):
                return v['name']
            cur = str(v.get('parentId'))
        return None

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

    # ---------- 筛选 ----------
    allq = json.load(open(DG + 'questions.json', encoding='utf-8'))['items']
    picked, out_of_scope, n_opt = [], Counter(), 0
    for x in allq:
        s = str(x.get('source') or '')
        if not ('900' in s or '姜晓千' in s or '880' in s):
            continue
        if OPT_RE.search(s) or OPT_RE.search(str(x.get('stem') or '')):
            n_opt += 1
            continue
        cids = x.get('categoryIds') or []
        path = dg_path(cids[0]) if cids else []
        hit = [seg for seg in path if seg in SHU2_EXCLUDE]
        if hit:
            out_of_scope[hit[0]] += 1
            continue
        picked.append(x)

    # 同题多出处 → 去重并合并 source
    merged, order = {}, []
    for x in picked:
        k = norm(x.get('stem'))
        if not k:
            continue
        if k not in merged:
            y = dict(x); y['source'] = str(x.get('source') or '')
            merged[k] = y; order.append(k)
        else:
            s = str(x.get('source') or '').strip()
            if s and s not in merged[k]['source']:
                merged[k]['source'] = (merged[k]['source'] + '；' + s).strip('；')

    # ---------- 剔除与 exam.json 重复 ----------
    # ⚠️ 必须先移除本脚本上一次写入的 entry，再建去重集合；
    #    否则旧 entry 里的题会把自己当成「已有重复」而被剔掉（踩过一次：
    #    重跑后 900题+姜晓千 从 783 道掉到 0 道，来源全变成 880）。
    exam = json.load(open(EXAM, encoding='utf-8'))
    exam = [e for e in exam if e.get('id') != PAPER_ID]
    have = set()
    for e in exam:
        for s in e.get('sections') or []:
            for q in s.get('questions') or []:
                have.add(norm(q.get('stem')))
    dup = sum(1 for k in order if k in have)
    order = [k for k in order if k not in have]

    # ---------- 构题 ----------
    buckets = defaultdict(list)
    nomap = 0
    for k in order:
        q = merged[k]
        cat = None
        for cid in (q.get('categoryIds') or []):
            cat = mapper(cid)
            if cat:
                break
        if not cat:
            p = dg_path((q.get('categoryIds') or [None])[0])
            nm = p[1] if len(p) >= 2 else (p[0] if p else None)
            cand = [oid for oid, v in O.items() if v['level'] == 1 and v['name'] == nm]
            cat = cand[0] if cand else None
        if not cat:
            nomap += 1
            continue
        buckets[chapter_of(cat) or '其他'].append((int(cat), q))

    # ---------- 按章节分 section，章内按 catId 排 ----------
    name2ch = {}
    for v in O.values():
        if v['level'] == 1:
            name2ch[v['id']] = v['name']
    order_ch = []
    for cid in sorted(O, key=lambda x: (O[x].get('order') if isinstance(O[x].get('order'), (int, float)) else 0)):
        if O[cid]['level'] == 1 and O[cid]['name'] not in order_ch:
            order_ch.append(O[cid]['name'])

    sections, total, no = [], 0, 0
    for ch in order_ch + [c for c in buckets if c not in order_ch]:
        if ch not in buckets:
            continue
        arr = sorted(buckets[ch], key=lambda t: t[0])
        qs = []
        for cat, q in arr:
            no += 1
            total += 1
            src = q['source']
            qs.append({
                'no': no,
                'kind': kind_of(q), 'type': kind_of(q),
                'stem': q.get('stem') or '',
                'options': q.get('options') or [],
                'answer': build_answer(q),
                'idea': q.get('explanation') or '',
                'categoryIds': [cat], 'catId': cat, 'deepCats': [],
                'linkedQid': None,                 # 不与真题抢主键
                'source': src,                    # ★ 题卡显示原书题源
                'from': ('900' if '900' in src else '姜晓千' if '姜晓千' in src else '880'),
                'status': 'ref-matched',
                'key': True if '重点' in src else False,
            })
        sections.append({'title': ch, 'questions': qs})

    entry = {
        'id': PAPER_ID, 'year': '', 'file': '',
        'title': '大观园 900题 · 880题 · 姜晓千（数二）',
        'sections': sections,
    }
    exam = exam + [entry]

    print('=== 大观园 900题 + 姜晓千 → 并入 exam.json ===')
    print('  原始条数（三套习题）    : %d' % (len(picked) + sum(out_of_scope.values()) + n_opt))
    print('  选做题排除              : %d 道' % n_opt)
    print('  数二范围外剔除            : %d %s' % (sum(out_of_scope.values()), dict(out_of_scope)))
    print('  按题干去重                : %d 道' % (total + dup + nomap))
    print('  与 exam.json 已有重复剔除: %d 道' % dup)
    print('  无分类映射跳过            : %d 道' % nomap)
    print('  ★ 实际新增                : %d 道' % total)
    print('  题号范围                  : 1 ~ %d（paperId=%s，与真题/核心题库隔离）' % (no, PAPER_ID))
    print('  带「重点」标记            : %d 道' % sum(1 for s in sections for q in s['questions'] if q['key']))
    print('  题型分布                  : %s' % dict(Counter(q['kind'] for s in sections for q in s['questions'])))
    print('  来源分布                  : %s' % dict(Counter(q['from'] for s in sections for q in s['questions'])))
    print('  章节 (%d 个)              : %s' % (len(sections), '、'.join('%s%d' % (s['title'], len(s['questions'])) for s in sections)))

    if args.dry_run:
        print('\n[dry-run] 未写盘')
        return
    out = json.dumps(exam, ensure_ascii=False, separators=(',', ':'))
    open(EXAM, 'w', encoding='utf-8').write(out)
    print('\n已写入 %s（%.1f MB）' % (EXAM, os.path.getsize(EXAM) / 1024 / 1024))


if __name__ == '__main__':
    main()
