# -*- coding: utf-8 -*-
"""给 _audit_formula_v2.py 的顶层报告逻辑加 main 保护（可被 import 复用而不产生输出）"""
import io, re

P = 'D:/ai code/math-note/tools/_audit_formula_v2.py'
s = io.open(P, encoding='utf-8').read()
if 'if __name__' in s:
    print('已有 main 保护，跳过')
else:
    marker = "for name, path in FILES.items():"
    i = s.index(marker)
    head, tail = s[:i], s[i:]
    # 把最后的报告循环缩进到 main() 里
    body = '\n'.join(('    ' + L) if L.strip() else L for L in tail.rstrip().split('\n'))
    s = head + "def main():\n" + body + "\n\n\nif __name__ == '__main__':\n    main()\n"
    io.open(P, 'w', encoding='utf-8', newline='').write(s)
    print('已加 main 保护')
import subprocess, sys
r = subprocess.run([sys.executable, '-c',
                    "import sys; sys.path.insert(0,'D:/ai code/math-note/tools'); import _audit_formula_v2 as m; print('import OK, scan:', callable(m.scan))"],
                   capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip()[:200])