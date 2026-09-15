# -*- coding: utf-8 -*-
"""全量检测：HTML 资源引用 / onclick 函数是否存在 / 分类 id 悬空 / 数据文件合法性"""
import os, re, io, json, glob

PWA = 'pwa'
problems = []

# ---------- 1) HTML 引用资源是否存在 ----------
def _strip_query(u):
    return u.split('?')[0].split('#')[0]

for html in glob.glob(os.path.join(PWA, '*.html')):
    src = io.open(html, encoding='utf-8').read()
    for m in re.finditer(r'<script[^>]+src="([^"]+)"', src):
        # 资源可能带版本号查询串（如 js/selected.js?v=20260830），判存在前先剥离
        u = _strip_query(m.group(1))
        p = os.path.join(PWA, u)
        if not os.path.exists(p):
            problems.append(f'[资源缺失] {os.path.basename(html)} 引用 {m.group(1)} 不存在')
    for m in re.finditer(r'<link[^>]+href="([^"]+\.css)"', src):
        u = _strip_query(m.group(1))
        p = os.path.join(PWA, u)
        if not os.path.exists(p):
            problems.append(f'[资源缺失] {os.path.basename(html)} 引用 {m.group(1)} 不存在')

# ---------- 2) onclick 引用的全局函数是否定义 ----------
# 注意：除 pwa/js/*.js 外，各 HTML 内还有内联 <script> 块（如 exam.html / category.html 的
# 背景自定义模块 handleBgUpload/setBgOverlay/toggleBgPanel 等都在内联脚本里）——必须一并纳入，
# 否则会把「定义在内联脚本中的函数」误报为未定义。
js_all = ''
for f in glob.glob(os.path.join(PWA, 'js', '*.js')):
    js_all += io.open(f, encoding='utf-8').read() + '\n'
for html in glob.glob(os.path.join(PWA, '*.html')):
    src = io.open(html, encoding='utf-8').read()
    for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', src):
        js_all += m.group(1) + '\n'
defined = set(re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', js_all))
defined |= set(re.findall(r'(?:window\.|globalThis\.)([A-Za-z_$][\w$]*)\s*=', js_all))
defined |= set(re.findall(r'^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\(', js_all, re.M))
inline_handlers = set()
for html in glob.glob(os.path.join(PWA, '*.html')):
    src = io.open(html, encoding='utf-8').read()
    for m in re.finditer(r'on(?:click|change|input|focus|mouse\w+|key\w+|submit|blur)="([A-Za-z_$][\w$]*)\(', src):
        inline_handlers.add((os.path.basename(html), m.group(1)))
for html, fn in sorted(inline_handlers):
    if fn not in defined and fn not in ('alert', 'confirm', 'prompt'):
        problems.append(f'[函数未定义] {html} 调用 {fn}() —— JS 中无同名定义')

# ---------- 3) 分类 id 悬空 ----------
try:
    cats = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))
    # 分类表结构 = dict（id → 节点）；也可能为 list / {'nodes': [...]}，三种都兼容
    cat_ids = set()
    def _collect(node):
        if isinstance(node, dict):
            if 'id' in node:
                cat_ids.add(str(node['id']))
            for v in node.values():
                if isinstance(v, (list, dict)):
                    _collect(v)
        elif isinstance(node, list):
            for v in node:
                _collect(v)
    _collect(cats)
    exam = json.load(io.open('pwa/data/exam.json', encoding='utf-8'))
    dangling = {}
    for p in exam:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                for cid in (q.get('categoryIds') or []):
                    if str(cid) not in cat_ids:
                        dangling.setdefault(str(cid), []).append(f"{p.get('year')}Q{q.get('no')}")
    for cid, qs in list(dangling.items())[:10]:
        problems.append(f'[分类悬空] id={cid} 不存在于分类树，被 {len(qs)} 题引用（如 {qs[0]}）')
except Exception as e:
    problems.append(f'[分类检测失败] {e}')

# ---------- 4) 其它数据文件合法性 ----------
for f in glob.glob('pwa/data/*.json'):
    try:
        json.load(io.open(f, encoding='utf-8'))
    except Exception as e:
        problems.append(f'[JSON 非法] {f}: {e}')

print('=' * 60)
if problems:
    print(f'发现 {len(problems)} 个问题：')
    for p in problems:
        print('  ' + p)
else:
    print('全量检测通过：资源引用完整、内联函数均有定义、分类引用无悬空、数据文件全部合法')