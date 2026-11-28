# -*- coding: utf-8 -*-
"""探测 math.cxyonly.fans 正式站：找「27张四卷」题单 directory 与题目。
复用持久化 profile，截获页面发出的 /api/questions 请求的 authorization/x-csrf-token。"""
import json, re, sys
from playwright.sync_api import sync_playwright

PROFILE = r'E:/deps_cache/browser-profiles/cxymath_pw'
BASE = 'https://math.cxyonly.fans'
OUT = r'D:/ai code/math-note/tools/_zs4_probe.json'

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
                    captured.update({k: h[k] for k in ('authorization', 'x-csrf-token', 'referer', 'origin', 'user-agent') if k in h})
        page.on('request', on_req)

        page.goto(BASE + '/practice', wait_until='domcontentloaded', timeout=60000)
        try:
            page.wait_for_response(lambda r: '/api/questions' in r.url, timeout=30000)
        except Exception:
            pass
        page.wait_for_timeout(1500)

        print('captured headers:', list(captured.keys()))
        if 'authorization' not in captured:
            print('!! 未截到 auth header，可能未登录或页面未发 /api/questions')
            # 尝试打印页面标题和 url 便于诊断
            print('url:', page.url, 'title:', page.title())
            ctx.close()
            sys.exit(2)

        hdr = {k: captured[k] for k in ('authorization', 'x-csrf-token') if k in captured}
        hdr['Referer'] = BASE + '/practice'
        hdr['Accept'] = 'application/json'
        hdr['x-requested-with'] = 'XMLHttpRequest'

        # 1) 所有题单
        r = ctx.request.get(BASE + '/api/question-lists', headers=hdr, timeout=60000)
        lists = r.json()
        # 2) mock-math-2 directory
        r2 = ctx.request.get(BASE + '/api/question-lists/mock-math-2/directory', headers=hdr, timeout=60000)
        directory = r2.json()
        out = {'question_lists': lists, 'mock_math2_directory': directory}
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print('lists:', len(lists) if isinstance(lists, list) else type(lists))
        print('directory keys:', list(directory)[:10] if isinstance(directory, dict) else len(directory))
        print('saved ->', OUT)
        ctx.close()

if __name__ == '__main__':
    main()
