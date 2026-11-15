# -*- coding: utf-8 -*-
"""mn27_papers.json 题干 ↔ 答案一致性扫描。

产出两类结果：
  [ERROR] 确凿错误（选项字母冲突、流程措辞残留、答案缺失等）→ 退出码 1
  [WARN ] 疑点（题干公式未在解答中复现、罕见数值未呼应等）→ 需人工判读
用法：python tools/_audit_mn27_consistency.py [--verbose]
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
DATA = os.path.join(ROOT, 'pwa', 'data', 'mn27_papers.json')
VERBOSE = '--verbose' in sys.argv
d = json.load(open(DATA, encoding='utf-8'))

errs, warns = [], []

# 转写流水线残留措辞（不应出现在交付数据里）
JUNK = ['按图还原', '任务示例', '待核', 'TODO', '图中文字',
        '请补充', '此处略', '略去', '见原图', '按原文', '转写', '草稿',
        '答案册', '题本', 'OCR', '示例输出', '【配图】',
        '原册', '扫描件', '本本注', '本草稿', '按原册照录', '小易注']

# 规范化 LaTeX：抹平等价写法，便于跨字段比对
def norm(s):
    s = s.replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac')
    s = s.replace('\\limits', '').replace('\\nolimits', '')
    s = re.sub(r'\\(?:mathrm|text|mbox)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\(?:left|right|,|;|!|:|>| )', '', s)
    s = re.sub(r'\\\[\d+pt\]|\\\\|&|=|,|~|\s+', '', s)
    return s

def formulas(s):
    """取出所有 $...$ / $$...$$ 内的公式（跳过纯字母选项等极短片段）。"""
    out = []
    for m in re.finditer(r'\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$', s):
        t = m.group(1) if m.group(1) is not None else m.group(2)
        if t and len(t.strip()) >= 2:
            out.append(t.strip())
    return out

LETTER_TAIL = re.compile(r'(?:故|所以|因此|综上)?\s*选\s*\(?([A-D])\)?')

stem_seen = collections.defaultdict(list)
for p in d:
    pid = p['id']
    for sec in p['sections']:
        for q in sec['questions']:
            qid = f"{pid}-{q['no']}"
            stem, ans, idea = q['stem'], q['answer'], q.get('idea', '')
            tips = ' '.join((q.get('tips') or {}).values())
            full_ans = ans + '\n' + idea + '\n' + tips
            n = q['no']

            # --- 1. 答案头 / 正文结论一致性 ---
            head = ans.split('\n', 1)[0]
            # 构建脚本按【解】定位解析段；正文被截断会在这里暴露
            solve_tail = ans.split('**【解】**', 1)[-1].strip()
            if len(solve_tail) < 60:
                errs.append(f'{qid}: 解析正文异常偏短（{len(solve_tail)} 字符）-> {solve_tail[:50]}')
            m = re.search(r'【答案】\s*(?:选\s*\(?)?([A-D])\)?', head)
            if n <= 10:
                if not m:
                    errs.append(f'{qid}: 选择题答案头未标字母 -> {head[:60]}')
                else:
                    declared = m.group(1)
                    tails = LETTER_TAIL.findall(ans.replace('**', ''))
                    if tails and any(t != declared for t in tails):
                        errs.append(f'{qid}: 答案头 ({declared}) 与正文结论 {tails} 冲突')
                    # 正确选项内容应在解答中出现（规范化后取前 12 字符做锚）
                    opt = q['options'][ord(declared) - 65]
                    opt_body = re.sub(r'^\([A-D]\)\s*', '', opt)
                    anchor = norm(opt_body)[:12]
                    if len(anchor) >= 6 and anchor not in norm(full_ans):
                        warns.append(f'{qid}: 正确选项 ({declared}) 主体未在解答中复现 -> {opt_body[:50]}')
            else:
                if '【答案】选' in head:
                    errs.append(f'{qid}: 非选择题答案头误写「选」')
                if not head.replace('【答案】', '', 1).strip():
                    errs.append(f'{qid}: 答案头为空')

            # --- 2. 流程措辞 / 占位残留 ---
            for w in JUNK:
                if w in stem or w in full_ans:
                    errs.append(f'{qid}: 残留措辞「{w}」')

            # --- 3. 题干公式是否在解答中复现 ---
            nans = norm(full_ans)
            for f in formulas(stem):
                nf = norm(f)
                if len(nf) < 8:
                    continue
                # 长公式只取前 24 字符做锚，避免解答中换了等价写法就误报
                anchor = nf[:24]
                if anchor not in nans:
                    warns.append(f'{qid}: 题干公式未在解答复现 -> {f[:70]}')

            # --- 4. 题干罕见数值是否在解答中出现 ---
            stem_nums = set(re.findall(r'(?<![\w\\])\d{2,}(?![\w])', stem))
            ans_nums = set(re.findall(r'(?<![\w\\])\d{2,}(?![\w])', full_ans))
            for x in sorted(stem_nums - ans_nums):
                if x in ('10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'):
                    continue  # 题号 / 分值
                warns.append(f'{qid}: 题干数值 {x} 未在解答中出现')

            # --- 5. 跨套题干重复（疑似整题误复制） ---
            key = re.sub(r'\s+', '', stem)[:80]
            stem_seen[key].append(qid)

for key, ids in stem_seen.items():
    if len(ids) > 1:
        warns.append(f'题干高度重复（可能是同题不同卷，需确认）: {", ".join(ids)}')

print(f'扫描 {len(d)} 套 / {sum(len(s["questions"]) for p in d for s in p["sections"])} 题')
print(f'确凿错误 {len(errs)} 项，疑点 {len(warns)} 项')
if errs:
    print('\n[ERROR]')
    for e in errs:
        print('  -', e)
if warns and (VERBOSE or not errs):
    print('\n[WARN]')
    for w in warns[:120 if not VERBOSE else len(warns)]:
        print('  -', w)
    if not VERBOSE and len(warns) > 120:
        print(f'  ... 另有 {len(warns)-120} 条，--verbose 查看全部')
if errs:
    sys.exit(1)
print('✓ 无确凿一致性错误（疑点需人工判读）')
