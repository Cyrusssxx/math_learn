# -*- coding: utf-8 -*-
"""核心题库 → 统一分类树 catId 映射（v2）。

关键点：大观园「真题类」条目的 categoryIds 指向年份节点（如 42008），
只有 practice / bank_questions 等条目带**知识点** categoryIds。
因此改为：把「带知识点标签的参考题」当作有标注语料，核心题在其中做匹配取标签；
匹配不上的再用关键词规则兜底。
"""
import json, io, re, sys, difflib
from collections import Counter, defaultdict

sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import load_refs, norm, grams          # noqa: E402

ROOT = 'D:/ai code/math-note/tools/'
BASE = 'D:/ai code/math-note/pwa/data/'
BANK = ROOT + 'yancai_bank.json'

cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))
KH_L1 = ['321', '322', '324', '325', '326', '224', '2', '3', '4', '5', '6', '7']
valid_l2 = {str(k): v.get('name') for k, v in cats.items()
            if v.get('level') == 2 and str(v.get('parentId')) in KH_L1}
print('知识型 L2 节点 %d 个' % len(valid_l2))

# ---- 有标注语料 ----
refs = load_refs()
labeled = []
for r in refs:
    ok = [str(c) for c in (r.get('categoryIds') or []) if str(c) in valid_l2]
    if ok:
        r['lab'] = Counter(ok).most_common(1)[0][0]
        labeled.append(r)
print('带知识点标签的参考题 %d 条' % len(labeled))

inv = defaultdict(list)
for i, r in enumerate(labeled):
    for g in r['grams']:
        inv[g].append(i)

# ---- 关键词兜底 ----
RULES = [
    (['反常积分', '瑕积分', '广义积分'], 228),
    (['二重积分', '累次积分', '交换积分次序', 'dxdy'], 562),
    (['条件极值', '拉格朗日乘数', '最大值和最小值', '多元函数'], 486),
    (['偏导', '全微分', '隐函数', '方向导数', '梯度'], 484),
    (['重极限', '二重极限'], 485),
    (['已知解', '反求'], 758),
    (['解的性质', '解的结构', '上有界', '渐近'], 760),
    (['通解', '特解', '微分方程'], 762),
    (['旋转体', '面积', '体积', '弧长', '做功', '形心', '质心'], 2322),
    (['不定积分', '定积分', '原函数', '换元', '分部'], 2321),
    (['中值定理', '罗尔', '拉格朗日', '柯西', '泰勒'], 368),
    (['导数定义', '可导', '导数概念'], 367),
    (['参数方程', '高阶导数', '求导', '微分'], 366),
    (['极值', '单调', '凹凸', '拐点', '渐近线', '曲率', '最值', '不等式'], 365),
    (['间断', '连续'], 328),
    (['奇偶', '周期', '有界', '函数'], 327),
    (['极限', '无穷小', '洛必达', '数列', '收敛'], 329),
]


# 人工指定（前两层未命中；判定依据为题面特征）
MANUAL = {
    'yc-29-1': 329,    # 当 x→0 时 1/x²·sin(1/x) 是否为无穷小 → 极限
    'yc-29-2': 329,    # ln¹⁰x / x / e^{x/10} 当 x 充分大 → 极限
    'yc-45-1': 329,    # 曲线 y=x·sin(1/x) 当 x>0 的行为 → 极限
    'yc-73-2': 2322,   # 细杆引力 → 定积分物理应用
    'yc-93-5': 486,    # x²+y²≤k·e^{x+y} 恒成立求 k 范围 → 多元最值
    'yc-116-3': 762,   # f(x+Δx)-f(x)=2xf(x)Δx+o(Δx) → 微分方程求解
    'yc-72-5': 2322,   # 速度 v(t)=t+k·sinπt 求 k → 定积分物理应用（原误归线性方程组）
    'yc-102-1': 562,   # ∬_D f(x,y)dxdy 换极坐标 → 二重积分计算（原误归线性方程组）
}


def by_rule(text):
    for kws, cid in RULES:
        for kw in kws:
            if kw in text:
                return cid
    return None


def by_notation(stem):
    """第三层兜底：按数学记号判定（题干里没有中文关键词时用）"""
    s = stem or ''
    if '\\iint' in s or '\\iiint' in s:
        return 562
    if '\\lim' in s:
        return 329
    if '\\partial' in s:
        return 484
    if re.search(r"y''|y'''", s) or ('微分方程' in s):
        return 762
    if "f'(" in s or "f''(" in s or '\\mathrm{d}y' in s:
        return 366
    if '\\int' in s:
        return 2321
    if '切线' in s or '法线' in s:
        return 366
    if '极值' in s or '最值' in s or '单调' in s:
        return 365
    return None


bank = json.load(io.open(BANK, encoding='utf-8'))
stat = Counter()
unmapped = []
weak = []

for q in bank['questions']:
    # 人工指定优先（覆盖任何自动判定）
    if q['id'] in MANUAL:
        q['catId'] = int(MANUAL[q['id']])
        q['catIdSrc'] = 'manual'
        stat['人工指定'] += 1
        continue
    nq = norm(q.get('stem'))
    gq = grams(nq)
    cnt = Counter()
    for g in gq:
        for i in inv.get(g, ()):
            cnt[i] += 1
    cands = [i for i, c in cnt.most_common(500) if c >= max(3, len(gq) * 0.3)]
    best, bestr = 0.0, None
    for i in cands:
        r = labeled[i]
        s = difflib.SequenceMatcher(None, nq, r['norm'], autojunk=False).ratio()
        if s > best:
            best, bestr = s, r
    cid = None
    if bestr and best >= 0.72:
        cid = bestr['lab']
        stat['语料匹配'] += 1
    else:
        text = (q.get('section_header') or '') + ' ' + re.sub(r'\\[a-zA-Z]+', '', q.get('stem') or '')
        cid = by_rule(text)
        if cid:
            stat['关键词兜底'] += 1
            if bestr:
                weak.append((q['id'], q.get('source'), round(best, 2),
                             valid_l2[str(cid)], (q.get('stem') or '')[:70]))
        else:
            cid = by_notation(q.get('stem'))
            if cid:
                stat['记号兜底'] += 1
            elif q['id'] in MANUAL:
                cid = MANUAL[q['id']]
                stat['人工指定'] += 1
            else:
                stat['未映射'] += 1
                unmapped.append((q['id'], q.get('source'), (q.get('stem') or '')[:80]))
                q['catId'] = None
                continue
    q['catId'] = int(cid)
    q['catIdSrc'] = 'corpus' if best >= 0.72 else 'rule'

with io.open(BANK, 'w', encoding='utf-8', newline='') as f:
    json.dump(bank, f, ensure_ascii=False, indent=1)

print()
print('=== 映射结果 ===')
for k, v in stat.most_common():
    print('  %-12s %d' % (k, v))
print()
dist = Counter()
for q in bank['questions']:
    if q.get('catId'):
        ch = cats[str(cats[str(q['catId'])]['parentId'])]['name']
        dist[(ch, valid_l2[str(q['catId'])])] += 1
print('=== 各知识点题数（共 %d） ===' % sum(dist.values()))
for (ch, leaf), n in dist.most_common():
    print('  %-8s %-16s %d' % (ch, leaf, n))
if unmapped:
    print()
    print('=== 未映射 %d 题 ===' % len(unmapped))
    for u in unmapped[:25]:
        print('  [%s] %s | %s' % (u[0], u[1], u[2].replace('\n', ' ')))
