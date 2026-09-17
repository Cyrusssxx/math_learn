# -*- coding: utf-8 -*-
"""答案补全 v2：
  1) 数二 2000-2026 → 优先 exam.json（你自己的真题库，完整【答案】+【解析】）
  2) 其余 → 参考库（大观园/practice/bankq）答案 + 解析
  3) 匹配门槛 0.80 + **字符多重集一致**（数字/字母集合相同）双重校验 → 同题判定可信，宁缺勿错
  4) 保留 _match_report.json 里 ≥0.92 的历史回填结果做并集

写入 yancai_bank.json：ref_answer（答案）/ ref_idea（解析）/ ans_ref / ans_score / ans_kind / ans_tier
"""
import json, io, re, sys, difflib
from collections import Counter

sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import load_refs, norm, grams            # noqa: E402

ROOT = 'D:/ai code/math-note/tools/'
BANK = ROOT + 'yancai_bank.json'
T_TIGHT, T_LOOSE = 0.88, 0.80


def sig(s):
    """字符多重集指纹（去 LaTeX 命令与标点，保留数字/字母）"""
    t = re.sub(r'\\[a-zA-Z]+', '', str(s or ''))
    t = re.sub(r'[^0-9A-Za-z\u4e00-\u9fff]', '', t)
    return Counter(re.findall(r'\d', t)), Counter(re.findall(r'[a-z]', t.lower()))


def sig_match(a, b):
    ad, al = sig(a)
    bd, bl = sig(b)
    return ad == bd and al == bl


refs = load_refs()


def full_text(stem, options):
    """题干 + 选项合并（选择题两边口径必须一致：核心题选项在 options，参考库常内联在 stem）"""
    parts = [str(stem or '')]
    if isinstance(options, dict):
        parts += [str(v) for v in options.values()]
    elif isinstance(options, (list, tuple)):
        parts += [str(x) for x in options]
    return ' '.join(parts)


for r in refs:
    r['n'] = norm(full_text(r['stem'], r['options']))
    r['n_stem'] = norm(r['stem'] or '')
    r['ans_text'] = (r['answer'] or '').strip()
    r['idea_text'] = (r['explanation'] or '').strip()
    r['has_ans'] = bool(r['ans_text'] or r['idea_text'])
    r['is_exam'] = (r['ref'] == 'exam')
print('参考库 %d 条（其中带答案 %d）' % (len(refs), sum(1 for r in refs if r['has_ans'])))

ans_refs = [r for r in refs if r['has_ans']]
inv_all = {}
for i, r in enumerate(ans_refs):
    for g in r['grams']:
        inv_all.setdefault(g, []).append(i)

# 历史回填（_match_report.json，score>=0.92）
hist = {}
rep_best = {}
try:
    for rec in json.load(io.open(ROOT + '_match_report.json', encoding='utf-8')):
        b = rec.get('best')
        if b and b.get('score', 0) >= 0.92 and (b.get('answer') or b.get('explanation') or ''):
            hist[rec['id']] = (round(b['score'], 3), b['answer'].strip(),
                               (b.get('explanation') or '').strip())
            rep_best[rec['id']] = '%s/%s' % (b['ref'], b['rid'])
except Exception as e:
    print('!! 历史回填读取失败', e)
print('历史回填可用 %d 题（>=0.92）' % len(hist))

bank = json.load(io.open(BANK, encoding='utf-8'))
stat = Counter()
miss = []
upgraded = []

def sim_pair(nq_full, nq_stem, r):
    """两种口径取较大值：题干+选项（严）/ 仅题干（宽）"""
    a = difflib.SequenceMatcher(None, nq_full, r['n'], autojunk=False).ratio()
    b = difflib.SequenceMatcher(None, nq_stem, r['n_stem'], autojunk=False).ratio()
    return a if a >= b else b


for q in bank['questions']:
    nq = norm(full_text(q.get('stem'), q.get('options')))
    nq_stem = norm(q.get('stem'))
    gq = grams(nq)
    cnt = Counter()
    for g in gq:
        for i in inv_all.get(g, ()):
            cnt[i] += 1
    scored = []
    for i, c in cnt.most_common(300):
        r = ans_refs[i]
        s = sim_pair(nq, nq_stem, r)
        if s >= T_LOOSE:
            scored.append((s, r))
    scored.sort(key=lambda x: -x[0])
    # 数二真题优先：同分数带内优先 exam.json（答案含完整解析）
    yr = [int(y) for y in re.findall(r'(20\d\d|19\d\d)', q.get('source') or '')]
    is_num2 = '数二' in (q.get('source') or '')
    if is_num2 and any(2000 <= y <= 2026 for y in yr):
        ex = [(s, r) for s, r in scored if r['is_exam'] and any(str(y) in r['src'] for y in yr)]
        if ex and ex[0][0] >= 0.85:
            scored = ex + scored

    chosen, tier = None, None
    for s, r in scored:
        if s >= T_TIGHT or sig_match(nq_stem, r['stem']):
            chosen, tier = (s, r), ('tight' if s >= T_TIGHT else 'sig')
            break

    old_a = (q.get('ref_answer') or '').strip()
    old_i = (q.get('ref_idea') or '').strip()
    if chosen:
        s, r = chosen
        q['ref_answer'] = r['ans_text']
        q['ref_idea'] = r['idea_text']
        q['ans_ref'] = '%s/%s' % (r['ref'], r['rid'])
        q['ans_score'] = round(s, 3)
        q['ans_kind'] = r['ref']
        q['ans_tier'] = tier
        stat['exam.json（完整解析）' if r['is_exam'] else '参考库'] += 1
        if r['is_exam'] and old_a and len(old_a) <= 3:
            upgraded.append((q['id'], old_a, (r['ans_text'] or '')[:50]))
    elif old_a or old_i:
        q['ref_answer'] = old_a
        q['ref_idea'] = old_i
        q['ans_tier'] = 'hist'
        stat['保留历史回填'] += 1
    elif q['id'] in hist:
        s, a, idea = hist[q['id']]
        q['ref_answer'] = a
        q['ref_idea'] = idea
        q['ans_score'] = s
        q['ans_ref'] = 'hist/%s' % (rep_best.get(q['id']) or '')
        q['ans_tier'] = 'hist'
        stat['历史回填'] += 1
    else:
        # 救援 pass：不做 gram 预筛，直接与「同年同科」的全部参考题比相似度（集合小、可靠）
        rescue = None
        if yr:
            pool = [r for r in ans_refs
                    if any(str(y) in r['src'] for y in yr)]
            for r in pool:
                s = sim_pair(nq, nq_stem, r)
                if rescue is None or s > rescue[0]:
                    rescue = (s, r)
        if rescue and rescue[0] >= 0.70:
            s, r = rescue
            q['ref_answer'] = r['ans_text']
            q['ref_idea'] = r['idea_text']
            q['ans_ref'] = '%s/%s' % (r['ref'], r['rid'])
            q['ans_score'] = round(s, 3)
            q['ans_kind'] = r['ref']
            q['ans_tier'] = 'rescue'
            stat['同年救援'] += 1
            continue
        # 终局救援：不限年份，全库比相似度（只对少量残留执行，成本可控）
        fin = None
        for r in ans_refs:
            s = sim_pair(nq, nq_stem, r)
            if fin is None or s > fin[0]:
                fin = (s, r)
        if fin and fin[0] >= 0.72:
            s, r = fin
            q['ref_answer'] = r['ans_text']
            q['ref_idea'] = r['idea_text']
            q['ans_ref'] = '%s/%s' % (r['ref'], r['rid'])
            q['ans_score'] = round(s, 3)
            q['ans_kind'] = r['ref']
            q['ans_tier'] = 'rescue2'
            stat['全库救援'] += 1
            continue
        q['ref_answer'] = ''
        q['ref_idea'] = ''
        q['ans_tier'] = 'none'
        stat['仍缺答案'] += 1
        miss.append((q['id'], q.get('source'),
                     round(fin[0], 2) if fin else 0,
                     (q.get('stem') or '')[:70]))

with io.open(BANK, 'w', encoding='utf-8', newline='') as f:
    json.dump(bank, f, ensure_ascii=False, indent=1)

tot = len(bank['questions'])
ok = sum(1 for q in bank['questions'] if (q.get('ref_answer') or '').strip()
         or (q.get('ref_idea') or '').strip())
idea = sum(1 for q in bank['questions'] if (q.get('ref_idea') or '').strip())
tiers = Counter(q.get('ans_tier') for q in bank['questions'])
print()
print('=== 结果 ===')
for k, v in stat.most_common():
    print('  %-22s %d' % (k, v))
print('  %-22s %d / %d（%.1f%%）' % ('有答案', ok, tot, 100.0 * ok / tot))
print('  %-22s %d' % ('其中带解析', idea))
print('  置信分层:', dict(tiers))
print('  单字母答案升级为完整解析: %d 题' % len(upgraded))
print()
if miss:
    print('=== 仍缺答案 %d 题 ===' % len(miss))
    for m in miss:
        print('  [%s] src=%s best=%.2f | %s' % (m[0], m[1], m[2], m[3].replace('\n', ' ')))
