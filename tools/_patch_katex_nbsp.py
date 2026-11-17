# -*- coding: utf-8 -*-
"""在 auto-render.min.js 的公式渲染前清洗 NBSP(U+00A0)。

根因：渲染层 mdBlock() 为防 HTML 折叠丢空格，把行首/连续普通空格转成 NBSP。
当公式定界符 $...$ / $$...$$ 内部含连续空格时，这些 NBSP 进入 KaTeX tex，
触发 strict:'warn' 的 "Unrecognized Unicode character (160)" 告警。

修复：auto-render 提取出公式 tex 后、调用 katex.render 前，先把 tex 中的
NBSP 还原为普通空格。preProcess 只作用于公式内部，公式外的 NBSP 不受影响。
保留用户传入的 preProcess（在其之前执行清洗）。

幂等：检测到清洗代码已存在则跳过。
"""
import io

PATH = 'pwa/vendor/katex/auto-render.min.js'
OLD = 'n.preProcess&&(a=n.preProcess(a))'
NEW = 'a=a.replace(/\\u00A0/g," "),n.preProcess&&(a=n.preProcess(a))'

raw = io.open(PATH, encoding='utf-8', newline='').read()

if NEW in raw:
    print('[skip] 清洗逻辑已存在，无需改动')
elif OLD not in raw:
    raise SystemExit('[fail] 未找到 preProcess 调用点，中止（auto-render 版本可能已变）')
elif raw.count(OLD) != 1:
    raise SystemExit('[fail] preProcess 调用点不唯一，中止')
else:
    assert raw.count(OLD) == 1
    out = raw.replace(OLD, NEW, 1)
    assert out != raw
    io.open(PATH, 'w', encoding='utf-8', newline='').write(out)
    print('[ok] 已注入 NBSP 清洗（1 处）')
    print('  OLD:', OLD)
    print('  NEW:', NEW)

# 复核
chk = io.open(PATH, encoding='utf-8', newline='').read()
assert chk.count(NEW) == 1, '复核失败：清洗逻辑应恰好 1 处'
print('[verify] 清洗逻辑恰好 1 处；OLD 残留:', chk.count(OLD))
