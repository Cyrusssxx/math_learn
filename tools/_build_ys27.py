# -*- coding: utf-8 -*-
"""把 _ys27_stems.py 的题干 + 5 份答案片段合并成 pwa/data/ys27_items.json，
并把「27模拟卷精选题」三级分类并入 pwa/data/exam_categories.json。

幂等：重复运行只会覆盖这两个文件里对应部分，不动其它分类。
用法：python tools/_build_ys27.py [--check]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from _ys27_stems import STEMS, YS27_CATS, CHAPTERS  # noqa: E402

DATA = os.path.join(ROOT, 'pwa', 'data')
ANS_FILES = ['ansA', 'ansB', 'ansC', 'ansD', 'ansE']
ANS_DIR = os.environ.get('YS27_ANS_DIR', r'C:\Users\cjx\AppData\Local\Temp\ys27')

PAPER_ID = 'ys27'
PAPER_TITLE = '27模拟卷精选题'


def load_answers():
    got = {}
    missing = []
    for name in ANS_FILES:
        p = os.path.join(ANS_DIR, name + '.json')
        if not os.path.exists(p):
            missing.append(name)
            continue
        raw = io.open(p, encoding='utf-8').read().strip()
        try:
            arr = json.loads(raw)
        except Exception as e:                     # 兼容「外面多包一层对象」的写法
            arr = json.loads(raw[raw.index('['):raw.rindex(']') + 1])
            print('  ! %s 需截取数组片段后才可解析：%s' % (name, e))
        for it in arr:
            no = int(it['no'])
            if no in got:
                raise SystemExit('答案重复：no=%d 同时出现在 %s' % (no, name))
            got[no] = it
    return got, missing


def normalize_answer(text):
    """少量统一：原解析里把完整推导写在【分析】下、【解】缺席时，改成【解】，
    避免出现「分析里全是分步推导」的观感错位（渲染本身不受影响）。"""
    t = text.strip()
    if '【分析】' in t and '【解】' not in t:
        head, _, tail = t.partition('【分析】')
        if '**①' in tail or '$$' in tail:
            return head + '【解】' + tail
    return t


def build_paper(ans):
    # 叶子 → 章节
    leaf2chap = {c['id']: c['parentId'] for c in YS27_CATS if c['level'] == 2}
    secs = []
    for cid, title in CHAPTERS:
        qs = []
        for s in STEMS:
            if leaf2chap.get(s['catId']) != cid:
                continue
            a = ans.get(s['no']) or {}
            answer = normalize_answer(a.get('answer') or '')
            idea = (a.get('idea') or '').strip()
            if not answer:
                raise SystemExit('缺少答案：no=%d %s' % (s['no'], s['source']))
            qs.append({
                'no': s['no'],
                'origin': s['origin'],
                'stem': s['stem'],
                'options': s['options'],
                'kind': s['kind'],
                'type': s['kind'],
                'source': s['source'],
                'answer': answer,
                'idea': idea,
                'categoryIds': [s['catId']],
            })
        if qs:
            secs.append({'title': title, 'questions': qs})
    return [{'id': PAPER_ID, 'year': '', 'title': PAPER_TITLE, 'sections': secs}]


def build_cats(existing):
    """把 YS27_CATS 写进分类表（覆盖同名 id），补齐 display/path 字段。"""
    byid = {int(k): v for k, v in existing.items()}
    for c in YS27_CATS:
        parent = byid.get(c['parentId']) if c['parentId'] else None
        path = (parent['path'] + ' / ' + c['name']) if parent else c['name']
        node = {
            'id': c['id'],
            'name': c['name'],
            'display': c['name'],
            'parentId': c['parentId'],
            'level': c['level'],
            'path': path,
            'ord': c['ord'],
        }
        existing[str(c['id'])] = node
        byid[c['id']] = node
    return existing


def main():
    check = '--check' in sys.argv
    ans, missing = load_answers()
    if missing:
        raise SystemExit('答案片段缺失：%s（目录 %s）' % (', '.join(missing), ANS_DIR))
    nos = sorted(ans)
    if nos != list(range(1, len(STEMS) + 1)):
        raise SystemExit('答案序号不连续：%s' % nos)

    paper = build_paper(ans)

    # ---- 写题库 ----
    out = os.path.join(DATA, 'ys27_items.json')
    text = json.dumps(paper, ensure_ascii=False, indent=1) + '\n'
    old = io.open(out, encoding='utf-8').read() if os.path.exists(out) else ''
    print('题库 %s：%d 章 / %d 题，%d 字节（%s）' % (
        os.path.basename(out), len(paper[0]['sections']),
        sum(len(s['questions']) for s in paper[0]['sections']),
        len(text.encode('utf-8')), '无变化' if text == old else '已更新'))
    if not check:
        io.open(out, 'w', encoding='utf-8', newline='\n').write(text)

    # ---- 写分类 ----
    cpath = os.path.join(DATA, 'exam_categories.json')
    craw = io.open(cpath, encoding='utf-8').read()
    cats = json.loads(craw)
    before = len(cats)
    cats = build_cats(cats)
    added = len(cats) - before
    ctext = json.dumps(cats, ensure_ascii=False, indent=1)   # 与仓库原格式一致：indent=1、无尾换行
    print('分类表：新增 %d 个节点（L0 1 + L1 9 + L2 %d），共 %d' % (
        added, len([c for c in YS27_CATS if c['level'] == 2]), len(cats)))
    if not check:
        io.open(cpath, 'w', encoding='utf-8', newline='\n').write(ctext)

    # ---- 自检 ----
    ids = set()
    for s in paper[0]['sections']:
        for q in s['questions']:
            assert q['no'] not in ids, q['no']
            ids.add(q['no'])
            assert q['stem'].count('$$') % 2 == 0, ('$$ 不成对', q['no'])
            if q['kind'] == 'choice':
                # no=36 的四个选项是「三平面位置关系」示意图，整组裁成一张图放进题干，
                # 因此 options 为空（其余选择题必须 4 个文字选项）
                assert len(q['options']) == 4 or (not q['options'] and '![' in q['stem']), \
                    ('选项数不是 4', q['no'])
            else:
                assert not q['options'], ('非选择题却有选项', q['no'])
    print('自检通过：%d 题，$$ 成对，选择题均为 4 个选项' % len(ids))


if __name__ == '__main__':
    main()
