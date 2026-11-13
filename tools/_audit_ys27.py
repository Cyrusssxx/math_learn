# -*- coding: utf-8 -*-
"""27 模拟卷精选题（ys27_items.json）结构校验。

覆盖：JSON 可解析 / 题号连续 / 分类挂载 / LaTeX 结构（$ 配对、花括号、\\left\\right、begin-end）/
mdBlock 不支持的列表前缀 / 选项数量与题型一致。

用法：python tools/_audit_ys27.py
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')

problems = []


def bad(where, msg):
    problems.append('%s: %s' % (where, msg))


def dollar_pairs(s):
    """统计未配对的 $：先按 $$ 显式配对（逐个找位置，不用「切掉」法——切掉后
    相邻两个显示块之间的换行会被误判成空块），剩下的块里单 $ 必须成对。"""
    out = []
    idx = [m.start() for m in re.finditer(r'\$\$', s)]
    if len(idx) % 2:
        return ['$$ 数量为奇数 %d' % len(idx)]
    for i in range(0, len(idx), 2):
        body = s[idx[i] + 2:idx[i + 1]]
        if not body.strip():
            out.append('存在空的 $$ 显示块（第 %d 个）' % (i // 2 + 1))
    rest = re.sub(r'\$\$[\s\S]*?\$\$', '', s)
    if rest.count('$') % 2:
        out.append('单 $ 数量为奇数 %d' % rest.count('$'))
    return out


def brace_balance(s):
    depth, i = 0, 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth < 0:
                return ['花括号负深度']
        i += 1
    return ['花括号不平衡 depth=%d' % depth] if depth else []


def leftright(s):
    l = len(re.findall(r'\\left(?=[.()\[\]|<>{}\s])', s))
    r = len(re.findall(r'\\right(?=[.()\[\]|<>{}\s])', s))
    return ['\\left(%d) != \\right(%d)' % (l, r)] if l != r else []


def beginend(s):
    envs = re.findall(r'\\begin\{([^}]*)\}', s)
    ends = re.findall(r'\\end\{([^}]*)\}', s)
    return ['begin/end 不匹配 %s vs %s' % (envs, ends)] if envs != ends else []


def list_prefix(s):
    out = []
    for ln in s.split('\n'):
        t = ln.strip()
        if re.match(r'^([-*+]\s|\d+[.)]\s)', t):
            out.append('列表前缀（mdBlock 不支持）: %s' % t[:24])
    return out


def main():
    p = os.path.join(DATA, 'ys27_items.json')
    if not os.path.exists(p):
        raise SystemExit('缺少 %s，先跑 tools/_build_ys27.py' % p)
    papers = json.loads(io.open(p, encoding='utf-8').read())
    cats = json.loads(io.open(os.path.join(DATA, 'exam_categories.json'), encoding='utf-8').read())

    if not isinstance(papers, list) or len(papers) != 1:
        bad('文件', '顶层应为单元素数组（一个 paper）')
    paper = papers[0]
    if paper.get('id') != 'ys27':
        bad('paper.id', paper.get('id'))

    qs = []
    for sec in paper.get('sections', []):
        if not (sec.get('title') or '').strip():
            bad('section', '标题为空')
        for q in sec.get('questions', []):
            qs.append(q)

    nos = [q['no'] for q in qs]
    if nos != sorted(nos) or len(set(nos)) != len(nos):
        bad('题号', '不递增或有重复：%s' % nos)
    if nos != list(range(1, len(nos) + 1)):
        bad('题号', '不是 1..N 连续：%s' % nos)

    qid_seen = set()
    for q in qs:
        tag = 'no=%d' % q['no']
        if 'ys27-%d' % q['no'] in qid_seen:
            bad(tag, 'qid 重复')
        qid_seen.add('ys27-%d' % q['no'])
        for f in ('stem', 'answer', 'idea', 'source'):
            if not (q.get(f) or '').strip():
                bad(tag, '%s 为空' % f)
        for f in ('stem', 'answer', 'idea'):
            s = q.get(f) or ''
            for fn in (dollar_pairs, brace_balance, leftright, beginend, list_prefix):
                for m in fn(s):
                    bad('%s.%s' % (tag, f), m)
        if not (q.get('answer') or '').startswith('【答案】'):
            bad(tag + '.answer', '没有以【答案】开头')
        kind = q.get('kind')
        if kind not in ('choice', 'blank', 'calc'):
            bad(tag, 'kind 非法：%r' % kind)
        if kind == 'choice':
            opts = q.get('options') or []
            if len(opts) != 4 and not (not opts and '![' in (q.get('stem') or '')):
                bad(tag, '选择题选项数 %d' % len(opts))
            # 选项必须带 A./B./C./D. 前缀（catCard 有前缀就不再加标签）
            for i, o in enumerate(opts):
                if not re.match(r'^[A-D][.、]', o.strip()):
                    bad(tag, '第 %d 个选项缺 A./B. 前缀：%s' % (i + 1, o[:20]))
        else:
            if q.get('options'):
                bad(tag, '非选择题却有选项')
        cids = q.get('categoryIds') or []
        if len(cids) != 1:
            bad(tag, 'categoryIds 数量 %d（应为 1）' % len(cids))
        for cid in cids:
            node = cats.get(str(cid))
            if not node:
                bad(tag, '分类 %s 不在 exam_categories.json' % cid)
                continue
            if node.get('level') != 2:
                bad(tag, '分类 %s 不是 L2 叶子' % cid)
            parent = cats.get(str(node.get('parentId')))
            if not parent or parent.get('level') != 1:
                bad(tag, '分类 %s 的父节点不是 L1' % cid)
            grand = cats.get(str(parent.get('parentId'))) if parent else None
            if not grand or grand.get('level') != 0:
                bad(tag, '分类 %s 的祖父节点不是 L0' % cid)

    # 分类树：L0 一个、L1 九章、L2 至少每章一个
    l0 = [c for c in cats.values() if c.get('id') == 50000]
    if len(l0) != 1:
        bad('分类', '50000 节点缺失或重复')
    elif l0[0].get('ord') != 60000:
        bad('分类', '50000 的 ord=%r（应为 60000，排在历年真题之后）' % l0[0].get('ord'))
    l1 = [c for c in cats.values() if c.get('parentId') == 50000]
    if len(l1) != 9:
        bad('分类', 'L1 章节数 %d（应为 9）' % len(l1))

    # 图片引用必须真实存在
    for q in qs:
        for m in re.finditer(r'!\[[^\]]*\]\((data/img/[^)\s]+)\)', q.get('stem') or ''):
            fp = os.path.join(ROOT, 'pwa', m.group(1))
            if not os.path.exists(fp):
                bad('no=%d' % q['no'], '引用的图片不存在：%s' % m.group(1))

    if problems:
        print('✗ %d 处问题：' % len(problems))
        for x in problems:
            print('  - ' + x)
        sys.exit(1)
    print('✓ ys27 校验通过：%d 章 / %d 题；LaTeX 结构、分类挂载、选项与配图全部正常' % (
        len(paper.get('sections', [])), len(qs)))


if __name__ == '__main__':
    main()
