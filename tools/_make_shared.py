# -*- coding: utf-8 -*-
"""从 exam.js 逐字抽取共享函数，生成 pwa/js/exam-shared.js
策略：以 exam.js 版本为准（功能超集：delExamNoteImg 支持 textarea、noteHint 支持 quiet 参数）。
抽取后检查未定义引用，确保模块自洽。
"""
import re

SRC = 'pwa/js/exam.js'
OUT = 'pwa/js/exam-shared.js'

# 需要抽取的共享函数（exam 与 category 重复的部分）
FUNCS = ['balanceDollars', 'esc', 'examImgDB', 'examImgGet', 'examImgDel',
         'favGet', 'favSave', 'favTime', 'fmtFavTime', 'fmtFavShort',
         'isFav', 'qidOf', 'migrateFavTimes', 'toggleFav', 'toggleFavOnly',
         'mdInline', 'mdBlock', 'mdBlockWithImg', 'renderMath',
         'noteGet', 'noteHint', 'delExamNoteImg', 'toggleQSec', 'zoomAnsImg']
# 追加：笔记贴图回填（fav 页必须）+ 编辑态读取/写入的三个轻量助手
# 注意：noteInput 牵扯 exam.js 编辑态专属状态（_noteTimer/examImgRefs/_pendingImgs），不抽取
EXTRA = ['fillExamNoteImgs', 'fillOneExamNoteImg', 'noteVal', 'setNoteContent', 'autoResizeNote']
FUNCS = FUNCS + EXTRA

# 模块级常量（exam.js 顶部）
CONSTS = ['FAV_KEY', 'FAV_ONLY_KEY']
# 抽取函数依赖的模块级变量（⚠️ 迁移 exam.js/category.js 时必须删掉它们各自的同名声明，
# 否则 let 重复声明会直接 SyntaxError）
VARS = ['favOnly', '_noteLastRendered', '_examImgDB']

# 生成后打的补丁：把页面专属依赖改为「有则用、无则降级」，
# 使共享模块在只读页面（无编辑器、无 renderCurrent）也能安全工作
PATCHES = [
    # toggleFav: renderCurrent 是真题页专属刷新函数 -> 走可选钩子
    ('    if (favOnly) renderCurrent();',
     '    if (favOnly) refreshAfterFavChange();\n    if (typeof window.onFavChange === \'function\') window.onFavChange();'),
    # toggleFavOnly: 同上
    ('    renderCurrent();\n}',
     '    refreshAfterFavChange();\n}'),
    # noteVal: 富文本编辑器仅真题页有 -> 降级 textContent
    ('    return el.tagName === \'TEXTAREA\' ? el.value : editorToNote(el);',
     '    return el.tagName === \'TEXTAREA\' ? el.value\n        : (typeof editorToNote === \'function\' ? editorToNote(el) : (el.textContent || \'\'));'),
    # setNoteContent: 同上
    ('    if (el.tagName === \'TEXTAREA\') el.value = text;\n    else noteToEditor(el, text);',
     '    if (el.tagName === \'TEXTAREA\') el.value = text;\n    else if (typeof noteToEditor === \'function\') noteToEditor(el, text);\n    else el.textContent = text;'),
    # toggleQSec: 笔记编辑态的输入监听/工具栏是真题页专属
    ('                    ta.addEventListener(\'input\', () => noteInput(ta));\n                    ta.addEventListener(\'paste\', notePasteImg);',
     '                    if (typeof noteInput === \'function\') ta.addEventListener(\'input\', () => noteInput(ta));\n                    if (typeof notePasteImg === \'function\') ta.addEventListener(\'paste\', notePasteImg);'),
    ('                    noteInput(ta);',
     '                    if (typeof noteInput === \'function\') noteInput(ta);'),
    ('                syncNoteToolbar(sec);',
     '                if (typeof syncNoteToolbar === \'function\') syncNoteToolbar(sec);'),
]

# 追加到模块末尾的页面解耦钩子
TAIL = '''
// ============ 收藏变更后的页面刷新（解耦真题页专用 renderCurrent） ============
// 只读页面（如收藏汇总页）可自行实现 window.onFavChange 来响应收藏变化；
// 未实现时若页面存在 renderCurrent（真题页）则调用之，都没有则静默跳过。
function refreshAfterFavChange() {
    if (typeof window.onFavChange === 'function') { window.onFavChange(); return; }
    if (typeof renderCurrent === 'function') renderCurrent();
}
'''


def extract_vars(src):
    out = []
    for line in src.split('\n'):
        for v in VARS:
            if re.match(r'^let\s+' + v + r'\s*=', line):
                out.append(line)
    return out


def extract_consts(src):
    out = []
    for line in src.split('\n'):
        for c in CONSTS:
            if line.startswith('const ' + c + ' '):
                out.append(line)
    return out


def extract_func(src, name):
    """抽取函数原文（兼容 `function x(` 与 `async function x(`）"""
    lines = src.split('\n')
    pat = re.compile(r'^(?:async\s+)?function ' + name + r'\s*\(')
    for i, ln in enumerate(lines):
        if pat.match(ln):
            j = i
            while j < len(lines):
                if lines[j] == '}':
                    return '\n'.join(lines[i:j + 1])
                j += 1
    return None


src = open(SRC, encoding='utf-8').read()
parts = []
parts.append("""/* 真题模块公共层：渲染 / 收藏 / 笔记贴图 / IndexedDB
 * 供 exam.js、category.js、fav.js 共用，杜绝多份副本各自漂移。
 * 抽取来源：exam.js（功能超集版本——delExamNoteImg 支持编辑态 textarea，
 * noteHint 支持 quiet 参数；在无 textarea 的只读页面可优雅降级）。
 * ⚠️ 修改本文件会同时影响三个页面，改动后务必三页都回归验证。
 */
""")
parts.append('// ============ 存储键 ============')
parts.append('\n'.join(extract_consts(src)))
parts.append('')
parts.append('// ============ 模块级状态 ============')
parts.append('/* ⚠️ 迁移提醒：exam.js / category.js 若改为引用本文件，务必删除它们各自的同名 let 声明，')
parts.append('   否则 let 重复声明会直接触发 SyntaxError。 */')
parts.append('\n'.join(extract_vars(src)))
parts.append('')
parts.append('// ============ 收藏存储（按题唯一 id：套卷id-题号） ============')

missing = []
got = []
for name in FUNCS:
    body = extract_func(src, name)
    if body is None:
        missing.append(name)
    else:
        got.append(name)
        parts.append(body)
        parts.append('')

# 追加解耦钩子
parts.append(TAIL)

out = '\n'.join(parts)

# ---- 应用降级补丁 ----
applied, failed = 0, []
for old, new in PATCHES:
    if old in out:
        out = out.replace(old, new, 1)
        applied += 1
    else:
        failed.append(old.strip()[:60])

open(OUT, 'w', encoding='utf-8').write(out)

print('已抽取函数 %d 个 -> %s' % (len(got), OUT))
print('模块级变量 %d 个: %s' % (len(extract_vars(src)), ', '.join(extract_vars(src)).split('=')[0] if extract_vars(src) else '无'))
print('降级补丁: 应用 %d / 失败 %d' % (applied, len(failed)))
for f in failed:
    print('   ❌ 未匹配:', f)
if missing:
    print('未找到(需手工处理):', missing)

# ---- 依赖自检：找出模块内引用但未定义的标识符 ----
defined = set(FUNCS) | set(CONSTS)
# 本文件内定义的
for m in re.finditer(r'^function ([a-zA-Z0-9_]+)\s*\(', out, re.M):
    defined.add(m.group(1))
for m in re.finditer(r'^(?:const|let|var) ([a-zA-Z0-9_]+)\s*=', out, re.M):
    defined.add(m.group(1))

BUILTIN = set('''if else for while return function const let var new typeof instanceof in of
try catch finally throw switch case break continue do delete void this true false null undefined
Math JSON Object Array String Number Boolean Date RegExp Promise Set Map document window
localStorage setTimeout clearTimeout requestAnimationFile alert confirm console
indexedDB URL Blob Image canvas encodeURIComponent decodeURIComponent parseInt parseFloat isNaN
Error Map Set Symbol async await class extends super yield static get set
katex renderMathInElement querySelector querySelectorAll'''.split())

used = set()
for m in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', out):
    used.add(m.group(1))

undef = sorted(u for u in used if u not in defined and u not in BUILTIN)
print()
print('=== 依赖自检：模块内调用但未在本文件定义（需确认由调用方/全局提供） ===')
for u in undef:
    print('   ', u)
print('共 %d 个' % len(undef))
