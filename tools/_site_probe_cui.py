# -*- coding: utf-8 -*-
"""探测站点所有题单目录，找「崔命六套卷」。"""
import json, sys
from playwright.sync_api import sync_playwright

PROFILE = r'E:/deps_cache/browser-profiles/cxymath_pw'
BASE = 'https://math.cxyonly.fans'
OUT = r'D:/ai code/math-note/tools/_cui_probe.json'

LISTS = ['mock', 'mock-math-1', 'mock-math-2', 'mock-math-3',
         'complete', 'complete-math-2', 'core-math-2']


def main():
    captured = {}
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            PROFILE, headless=True,
            args=['--disable-blink-features=AutomationControlled'],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def on_req(req):
            if '/api/questions' in req.url and req.method == 'GET':
                h = req.headers
                if 'authorization' in h:
                    captured.update({k: h[k] for k in ('authorization', 'x-csrf-token') if k in h})
        page.on('request', on_req)
        page.goto(BASE + '/practice', wait_until='domcontentloaded', timeout=60000)
        try:
            page.wait_for_response(lambda r: '/api/questions' in r.url, timeout=30000)
        except Exception:
            pass
        page.wait_for_timeout(1200)
        if 'authorization' not in captured:
            print('!! 未截到 auth header', page.url, page.title())
            ctx.close(); sys.exit(2)

        hdr = {k: captured[k] for k in ('authorization', 'x-csrf-token')}
        hdr.update({'Referer': BASE + '/practice', 'Accept': 'application/json',
                    'x-requested-with': 'XMLHttpRequest'})
        out = {}
        for lid in LISTS:
            try:
                r = ctx.request.get(BASE + '/api/question-lists/' + lid + '/directory',
                                    headers=hdr, timeout=60000)
                out[lid] = r.json()
                print(lid, 'status', r.status)
            except Exception as e:
                print(lid, 'ERR', str(e)[:100])
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)

        for lid, obj in out.items():
            data = obj.get('data') or {}
            found = []
            def walk(nodes):
                for n in nodes or []:
                    lab = str(n.get('label', ''))
                    if any(k in lab for k in ('崔', '命六', '小崔')):
                        found.append((n.get('category_id'), lab, n.get('question_count')))
                    walk(n.get('children'))
            walk(data.get('roots'))
            if found:
                print('*** FOUND in', lid, ':', found)
        print('saved ->', OUT)
        ctx.close()


if __name__ == '__main__':
    main()
