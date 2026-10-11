#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全量诊断：core_bank 里无 linkedQid 的题 × 真题全卷（exam.json）题干匹配。
找出「实为真题同题/原题却无关联」的 core 题 —— 这些题导致真题侧的标记/笔记
无法在 core 模式下同步显示（用户报障）。

阈值：≥0.85 视为同题（自动补）；0.60~0.85 复核；<0.60 忽略。
一对多处理：同一真题被多道 core 题匹配时，只有相似度最高者获得关联。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def norm(s):
    s = s or ''
    s = re.sub(r'（本题满分[^）]*分）', '', s)   # 真题大题的分值前缀会稀释相似度
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    s = re.sub(r'（\s*）|\(\s*\)|_{2,}|（本题满分\d+分）', '', s)
    return s


def bg(s):
    return set(s[i:i + 2] for i in range(len(s) - 1)) if len(s) > 1 else {s}


def jac(a, b):
    A, B = bg(a), bg(b)
    return len(A & B) / len(A | B) if (A and B) else 0.0


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    e = ann['exam']
    marked = set(json.loads(e['favs']).keys()) | set(json.loads(e['status']).keys()) | set(
        k.replace('examNote-', '') for k in e['notes'])

    # 真题侧索引
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q
    zlist = [(k, norm(q.get('stem'))) for k, q in zp.items()]

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    need = [q for q in qs if not q.get('linkedQid')]
    print('core 无 linkedQid 的题 =', len(need), '/', len(qs))

    # 匹配（取每题最佳真题）
    AUTO, REVIEW, NONE = [], [], []
    for q in need:
        nq = norm(q.get('stem'))
        if len(nq) < 12:
            NONE.append((q, 0, None)); continue
        best_k, best_s = None, 0.0
        for k, zn in zlist:
            s = jac(nq, zn)
            if s > best_s:
                best_k, best_s = k, s
        rec = (q, best_s, best_k)
        (AUTO if best_s >= 0.85 else REVIEW if best_s >= 0.60 else NONE).append(rec)

    print('匹配结果：同题(≥0.85)=%d  复核(0.60~0.85)=%d  无匹配(<0.60)=%d' % (len(AUTO), len(REVIEW), len(NONE)))

    # 一对多处理：同一真题只给相似度最高者
    by_zhen = collections.defaultdict(list)
    for q, s, k in AUTO:
        by_zhen[k].append((s, q))
    assigned, dropped = [], []
    for k, lst in by_zhen.items():
        lst.sort(key=lambda x: -x[0])
        assigned.append((k, lst[0]))
        for s, q in lst[1:]:
            dropped.append((k, q, s))
    print('自动补关联候选 = %d 道（涉及 %d 道真题）；因一对多落选 = %d 道' % (
        len(assigned), len(by_zhen), len(dropped)))

    # 用户标记交集：哪些能立即恢复同步
    hit_marked = [(k, q, s) for k, (s, q) in assigned if k in marked]
    print('其中「该真题上有你的标记/笔记」的 =', len(hit_marked), '道 ← 补齐后你的标记立即在 core 恢复显示')

    # 样例输出
    print()
    # 落盘供修复脚本复用
    out = {'auto': [[k, q['no'], round(s, 3)] for k, (s, q) in assigned],
           'review': [[str(k), q['no'], round(s, 3)] for q, s, k in REVIEW],
           'dropped': [[k, q['no'], round(s, 3)] for k, q, s in dropped]}
    io.open(os.path.join(ROOT, 'tools/_link_gap_scan.json'), 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print('扫描结果已写 tools/_link_gap_scan.json')
    return 0
    print('=== 自动补清单（前 15，含用户标记的优先展示）===')
    show = sorted(hit_marked, key=lambda x: -x[2])[:8] + [x for x in ((k, q, s) for k, (s, q) in assigned) if x[0] not in marked][:7]
    for k, q, s in show:
        print('  core no=%-5s(原xd-%s) ← %-20s 相似=%.2f %s' % (
            q['no'], str(q.get('xdNo')), k, s, '★你有标记' if k in marked else ''))
        print('       core 题干: %s' % (q.get('stem') or '').replace('\n', ' ')[:76])
        print('       真题 题干: %s' % (zp[k].get('stem') or '').replace('\n', ' ')[:76])
    print()
    print('=== 复核档样例（前 8）===')
    for q, s, k in sorted(REVIEW, key=lambda x: -x[1])[:8]:
        print('  core no=%-5s ← %-20s 相似=%.2f' % (q['no'], str(k), s))
        print('       core 题干: %s' % (q.get('stem') or '').replace('\n', ' ')[:76])
        print('       真题 题干: %s' % (zp[k].get('stem') or '').replace('\n', ' ')[:76])



if __name__ == '__main__':
    sys.exit(main())
