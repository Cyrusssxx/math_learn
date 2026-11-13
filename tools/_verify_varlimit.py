# -*- coding: utf-8 -*-
"""验证《变限积分》章节追加：目录镜像、锚点未偏移、LaTeX 结构。"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'pwa', 'data', 'notes.json')
NID = '高数3.1-一元积分-计算'
def git_orig():
    """从 HEAD 取改动前的原始 notes.json（比临时备份可靠）。"""
    import subprocess
    return subprocess.run(['git', 'show', 'HEAD:pwa/data/notes.json'],
                          cwd=ROOT, capture_output=True).stdout.decode('utf-8')

fails = []


def ok(name, cond, extra=''):
    print(('  OK  ' if cond else '  X   ') + name + (('  ' + extra) if extra and not cond else ''))
    if not cond:
        fails.append(name)


raw = io.open(P, encoding='utf-8').read()
data = json.loads(raw)

print('=== 1. JSON 格式 ===')
ok('round-trip 与磁盘字节完全一致（indent=2 无尾换行）',
   json.dumps(data, indent=2, ensure_ascii=False) == raw)
ok('文件不以换行结尾', not raw.endswith('\n'))

note = [x for x in data if x['id'] == NID][0]

print('=== 2. chapters 与 ## 逐个镜像 ===')
h2 = [l[3:].split('<!--')[0].strip() for l in note['md'].split('\n') if l.startswith('## ')]
ok('章数一致 chapters=%d, ##=%d' % (len(note['chapters']), len(h2)), len(note['chapters']) == len(h2))
for i, (a, b) in enumerate(zip(note['chapters'], h2)):
    ok('第 %d 章 %r == %r' % (i, a, b), a == b)

print('=== 3. 新章结构 ===')
ok('chapters 末项为「变限积分」', note['chapters'][-1] == '变限积分')
ok('正文末章为「变限积分」', h2[-1] == '变限积分')
ok('原「积分存在性」仍是第 11 章（索引 10）', h2[10] == '积分存在性')
h3 = [l[4:].strip() for l in note['md'].split('\n') if l.startswith('### ')]
tail = note['md'][note['md'].index('## 变限积分'):]
h3_new = [l[4:].strip() for l in tail.split('\n') if l.startswith('### ')]
ok('新章含 8 个小节', len(h3_new) == 8, '实际 %d' % len(h3_new))
print('     小节：' + ' / '.join(h3_new))

# 目录（doc-toc）取的是 h3 的 textContent，KaTeX 的 MathML annotation + aria-hidden
# 会把一个 $x$ 变成 "xxx"、把 $\Phi(x)=\int$ 变成「渲染串 + 原始 LaTeX」的长串。
# 所以小节标题一律写纯文本，不得出现 $。
bad_title = [t for t in h3_new if '$' in t]
ok('小节标题不含 $（否则目录会串成 xxx / 原始 LaTeX）', len(bad_title) == 0, str(bad_title))
bad_h2 = [t for t in h2 if '$' in t]
ok('章标题不含 $', len(bad_h2) == 0, str(bad_h2))

print('=== 4. 关键知识点覆盖 ===')
must = [
    (r'上限代入乘上限导', '求导口诀'),
    (r'f\\left\(\\psi\(x\)\\right\)\\psi\'\(x\)', '一般式公式'),
    (r'被积函数含 x：先分离', '含 x 小节标题'),
    (r'u=x-t', 'x-t 换元'),
    (r'u=xt', 'xt 换元'),
    (r'x\^2-t\^2', '平方换元'),
    (r'提不动就换元', '分离口诀'),
    (r'洛必达', '极限套路'),
    (r'奇偶', '奇偶性'),
    (r'莱布尼茨', '进阶公式'),
    (r'易错点总表', '易错清单'),
]
for pat, name in must:
    ok('覆盖：' + name, re.search(pat, tail) is not None)

print('=== 5. 既有批注锚点未受影响 ===')
old = json.loads(git_orig())
oldnote = [x for x in old if x['id'] == NID][0]
ok('原文 md 是新 md 的严格前缀（只追加、不改写）', note['md'].startswith(oldnote['md']))
ok('原 chapters 是新 chapters 的严格前缀', note['chapters'][:len(oldnote['chapters'])] == oldnote['chapters'])
old_blocks = [l for l in oldnote['md'].split('\n')]
ok('原文行序列在文件头部逐行一致',
   note['md'].split('\n')[:len(old_blocks)] == old_blocks)
print('     原 md 末尾字符 %r，新内容从此处接续' % oldnote['md'][-30:])

print('=== 6. 公式配对 ===')
def dollars_ok(s):
    # 按行检查 $ 个数（$$ 块独占行时按 2 计）
    bad = []
    for i, l in enumerate(s.split('\n')):
        n = l.count('$') - l.count('\\$')
        if n % 2 != 0:
            bad.append((i + 1, l[:70]))
    return bad

bad = dollars_ok(tail)
ok('新章每行 $ 均成对', len(bad) == 0, str(bad[:3]))
ok('无 3 个以上连续 $', '$$$' not in tail.replace('$$', ''))

print()
if fails:
    print('FAILED %d 项：' % len(fails))
    for f in fails:
        print(' -', f)
    sys.exit(1)
print('全部通过')
