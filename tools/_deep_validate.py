r"""Deep final validation: delimiter balance + full double-escape scan + pollution check."""
import json, re

with open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

issues = []
qcount = 0

# All known LaTeX commands used in this dataset (from earlier scans)
CMDS = ['left', 'right', 'begin', 'end', 'text', 'Big', 'big', 'Bigg', 'bigg',
        'frac', 'dfrac', 'tfrac', 'sqrt', 'underline', 'overline', 'overset',
        'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'ln', 'log', 'lim',
        'int', 'sum', 'prod', 'infty', 'partial', 'alpha', 'beta', 'gamma',
        'theta', 'pi', 'lambda', 'mu', 'Delta', 'sigma', 'omega', 'varphi',
        'mathrm', 'mathbf', 'boldsymbol', 'displaystyle', 'tfrac', 'cdot',
        'quad', 'qquad', 'hspace', 'to', 'rightarrow', 'times', 'dots']

for ex in data:
    for sec in ex.get('sections', []):
        for q in sec.get('questions', []):
            qcount += 1
            for field in ['stem', 'answer', 'idea']:
                val = q.get(field, '')
                tag = f"{ex.get('year')} Q{q.get('no')} {field}"

                # 1. double-escaped commands
                for c in CMDS:
                    # 双转义特征：逻辑串中「连续 2+ 反斜杠 + 命令」。但矩阵换行符 \\ 后紧跟分式
                    # 会形成 \\\frac（3 反斜杠 = 合法：\\ 换行 + \frac 下一行首元素），必须放行——
                    # 判定：匹配 \\cmd 时若其前一字符也是反斜杠（属于 \\\cmd 的中间段）即视为合法换行。
                    for _m in re.finditer(re.escape('\\\\' + c), val):
                        if _m.start() > 0 and val[_m.start() - 1] == '\\':
                            continue   # \\\cmd：前两个 \\ 是矩阵换行，最后一个 \ 是命令转义，合法
                        issues.append(f"{tag}: \\\\\\\\{c}")
                        break

                # 2. pollution from intermediate fixes
                if '\\$' in val:
                    issues.append(f"{tag}: backslash-dollar")
                if '$$_' in val or '_$$' in val:
                    # plain underscore glued to $$ - suspicious but could be legit (x_$$? no)
                    issues.append(f"{tag}: underscore glued to $$")

                # 3. $$ delimiter balance (even count)
                n2 = val.count('$$')
                if n2 % 2 != 0:
                    issues.append(f"{tag}: unbalanced $$ (count={n2})")

                # 4. $ balance outside $$: remove $$ pairs then count single $
                tmp = val.replace('$$', '\x00')
                # temporary marker; count single $ in segments between markers
                segs = tmp.split('\x00')
                for k, seg in enumerate(segs):
                    if k % 2 == 0:  # outside display blocks
                        n1 = seg.count('$')
                        if n1 % 2 != 0:
                            issues.append(f"{tag}: unbalanced $ outside $$ ({n1})")
                            break

print(f'Exams: {len(data)}, Questions: {qcount}')
if issues:
    print(f'ISSUES: {len(issues)}')
    seen = set()
    for i in issues:
        if i.split(':')[1][:20] not in seen or True:
            print('  ' + i)
        seen.add(i.split(':')[1][:20])
        if len(seen) > 25:
            break
else:
    print('ALL CLEAN - delimiters balanced, no double-escapes, no pollution')
