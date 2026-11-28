# -*- coding: utf-8 -*-
"""崔命六套卷草稿独立校验：题号/字段/答案字母/格式约束。"""
import json, os, re, sys

ROOT = r'D:/ai code/math-note'
DRAFT = os.path.join(ROOT, 'tools', 'cui6_ans')
TEXT = os.path.join(ROOT, 'tools', '_cui6_text')

SEP = re.compile(r'(?====Q(\d+)===)')
BAD_LITERALS = ('【答案】', '【解】', '【思路】', '【易错】')


def blocks(path):
    s = open(path, encoding='utf-8').read()
    parts = SEP.split(s)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        out[int(parts[i])] = parts[i + 1]
    return out


def field(block, tag):
    m = re.search(r'【' + tag + r'】(.*?)(?=\n【|\Z)', block, re.S)
    return m.group(1).strip() if m else ''


def site_answers(vol):
    """从PDF文字层提取红色【答案】字母，按题号顺序。"""
    txt = open(os.path.join(TEXT, f'v{vol}_ans.txt'), encoding='utf-8').read()
    # 文字层中答案形如 【答案】（C） 或 【答案】 C
    got = re.findall(r'【答案】\s*[（(]?\s*([A-D])\s*[)）]?', txt)
    return got


def main():
    errs = []
    summary = []
    for v in range(1, 6):
        tag = f'q{v:02d}'
        sb = blocks(os.path.join(DRAFT, f'{tag}_stem.md'))
        ab = blocks(os.path.join(DRAFT, f'{tag}_ans.md'))
        if sorted(sb) != list(range(1, 23)):
            errs.append(f'{tag} stem 题号异常: {sorted(sb)}')
        if sorted(ab) != list(range(1, 23)):
            errs.append(f'{tag} ans 题号异常: {sorted(ab)}')
        pdf_ans = site_answers(v)
        # PDF 文字层只有选择题 10 个字母可可靠提取；填空/解答为 LaTeX 表达式，
        # 交给视觉转写 + 构建后 KaTeX/内容审计，这里仅校验选择题字母数
        if len(pdf_ans) < 10:
            errs.append(f'{tag} PDF 选择答案提取数={len(pdf_ans)}（应≥10）')
        got_ans = []
        nfig = 0
        for no in range(1, 23):
            s, a = sb.get(no, ''), ab.get(no, '')
            kind = field(s, '题型')
            if not kind:
                errs.append(f'{tag} Q{no} 缺题型')
            if not field(s, '题干'):
                errs.append(f'{tag} Q{no} 缺题干')
            if kind == 'choice':
                for c in 'ABCD':
                    if not field(s, c):
                        errs.append(f'{tag} Q{no} 缺选项 {c}')
            ans = field(a, '答案')
            solve = field(a, '解')
            idea = field(a, '思路')
            yc = field(a, '易错')
            if not ans:
                errs.append(f'{tag} Q{no} 缺答案')
            if len(solve) < 60:
                errs.append(f'{tag} Q{no} 解析过短({len(solve)})')
            if len(idea) < 10:
                errs.append(f'{tag} Q{no} 思路过短')
            if len(yc) < 5:
                errs.append(f'{tag} Q{no} 易错过短')
            if no <= 10:
                m = re.fullmatch(r'([A-D])', ans)
                if not m:
                    errs.append(f'{tag} Q{no} 选择答案格式异常: {ans!r}')
                else:
                    got_ans.append(m.group(1))
            # 正文里不得出现字段字面（去掉行首标签后检查）
            for txtname, txt in (('stem', s), ('ans', a)):
                body = '\n'.join(l for l in txt.split('\n')
                                 if not any(l.startswith(x) for x in BAD_LITERALS))
                for lit in BAD_LITERALS:
                    if lit in body:
                        errs.append(f'{tag} Q{no} {txtname} 正文含禁用字面 {lit}')
            # $ 配对
            for txtname, txt in (('stem', s), ('ans', a)):
                if txt.count('$') % 2:
                    errs.append(f'{tag} Q{no} {txtname} $ 数量奇数')
            # mdBlock 不支持 '- ' 列表（答案与解析正文）
            for l in solve.split('\n'):
                if re.match(r'^\s*-\s+\S', l):
                    errs.append(f'{tag} Q{no} 解析含 markdown 列表')
                    break
            if '【配图】' in s:
                nfig += 1
        if len(got_ans) == 10 and len(pdf_ans) >= 10:
            mism = [(i + 1, got_ans[i], pdf_ans[i]) for i in range(10)
                    if got_ans[i] != pdf_ans[i]]
            if mism:
                errs.append(f'{tag} 答案字母与 PDF 不一致: {mism}')
        summary.append(f'{tag}: 题干{len(sb)} 答案{len(ab)} 配图{nfig} 选择{"".join(got_ans)}')

    print('\n'.join(summary))
    if errs:
        print(f'\nFAIL {len(errs)} 项:')
        for e in errs[:60]:
            print('  -', e)
        sys.exit(1)
    print('\nPASS: 5 套 × 22 题草稿格式与答案一致')


if __name__ == '__main__':
    main()
