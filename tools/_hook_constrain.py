# -*- coding: utf-8 -*-
"""把「deepCats 子树约束」挂到两个数据生成器末尾，避免下次重新生成时又引入越界标签。"""
import io

HOOK = '''

# ---- 生成后自动约束 deepCats 到「知识点对应子树」内（避免浮层看不到题；见 _constrain_deepcats.py）----
try:
    import subprocess, sys as _sys
    subprocess.run([_sys.executable, 'D:/ai code/math-note/tools/_constrain_deepcats.py'],
                   check=False, capture_output=True)
except Exception as _e:
    print('!! deepCats 约束脚本调用失败：%s' % _e)
'''

for p in ('D:/ai code/math-note/tools/_gen_core_bank.py',
          'D:/ai code/math-note/tools/_write_deepcats_exam.py'):
    s = io.open(p, encoding='utf-8').read()
    if '_constrain_deepcats.py' in s:
        print('已挂接过，跳过:', p.split('/')[-1])
        continue
    io.open(p, 'w', encoding='utf-8', newline='').write(s + HOOK)
    print('已挂接:', p.split('/')[-1])