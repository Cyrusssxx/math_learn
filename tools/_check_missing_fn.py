# -*- coding: utf-8 -*-
"""静态排查：某页面脚本里「被调用但未在该页加载的脚本中定义」的函数（跨副本漏移植检测）"""
import io, re

PAGES = {
    'category.html': ['js/common.js', 'js/category.js', 'js/mastery.js'],
    'exam.html': ['js/common.js', 'js/exam.js'],
}

BUILTIN = set("""window document localStorage sessionStorage console setTimeout clearTimeout setInterval clearInterval
JSON Object Array String Number Boolean Math Date parseInt parseFloat isNaN isFinite alert confirm prompt fetch Promise
Map Set WeakMap WeakSet RegExp Error TypeError Symbol Proxy Reflect BigInt Intl encodeURIComponent decodeURIComponent
encodeURI decodeURI escape unescape requestAnimationFrame cancelAnimationFrame getSelection getComputedStyle matchMedia
URL Blob File FileReader Image Audio Option Event CustomEvent MouseEvent KeyboardEvent DragEvent FormData Headers Request
Response AbortController AbortSignal Uint8Array Int16Array Int32Array Float32Array Float64Array ArrayBuffer DataView
atob btoa crypto structuredClone queueMicrotask reportError scrollTo scrollBy open close focus blur print
indexedDB caches navigator location history performance devicePixelRatio innerWidth innerHeight scrollY scrollX
isSecureContext String eval Function arguments this super import export await async return typeof instanceof new delete void
if else for while do switch case break continue try catch finally throw class extends constructor get set static""".split())

def defs_and_calls(path):
    s = io.open(path, encoding='utf-8').read()
    s_nc = re.sub(r'//[^\n]*', '', s)                     # 去行注释
    s_nc = re.sub(r'/\*[\s\S]*?\*/', '', s_nc)            # 去块注释
    defs = set(re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)', s_nc))
    defs |= set(re.findall(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=', s_nc))
    defs |= set(re.findall(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*;', s_nc))
    defs |= set(re.findall(r'\b(?:window|globalThis)\.([A-Za-z_$][\w$]*)\s*=', s_nc))   # window.foo = function(){}
    calls = set()
    for m in re.finditer(r'(?<![\w$.])([A-Za-z_$][\w$]*)\s*\(', s_nc):
        name = m.group(1)
        if name in BUILTIN or name in defs:
            continue
        calls.add(name)
    # 排除对象字面量的键、属性名等（粗略）：只剩真正的裸调用
    return defs, calls

for page, scripts in PAGES.items():
    all_defs, all_calls = set(), set()
    per = {}
    for p in scripts:
        d, c = defs_and_calls('D:/ai code/math-note/pwa/' + p)
        per[p] = (d, c)
        all_defs |= d
        all_calls |= c
    missing = sorted(c for c in all_calls if c not in all_defs)
    print('=' * 66)
    print(page, '→ 脚本:', ', '.join(scripts))
    print('  未定义即被调用（疑似跨页漏移植）:', missing if missing else '无 ✅')
    for p, (d, c) in per.items():
        miss = sorted(x for x in c if x not in all_defs)
        if miss:
            print('    [%s] 贡献: %s' % (p, miss))
