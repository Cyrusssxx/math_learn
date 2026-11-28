# -*- coding: utf-8 -*-
"""抓取「27张四卷」四套题（category 12981..12984），保留原图顺序。
复用持久化 profile 截 auth/csrf header，然后：
  - /api/questions?...category_id=..&question_list_id=mock-math-2&exam_subject=math_2
  - /api/v1/questions/{id}/assets/{sha256} 下载解析原图
输出 tools/_zs4_raw.json（仅原始抓取，不做加工）"""
import json, os, sys
from playwright.sync_api import sync_playwright

PROFILE = r'E:/deps_cache/browser-profiles/cxymath_pw'
BASE = 'https://math.cxyonly.fans'
CATS = [12981, 12982, 12983, 12984]
OUT = r'D:/ai code/math-note/tools/_zs4_raw.json'
PROBE = r'D:/ai code/math-note/tools/_zs4_probe.json'

def get_headers(ctx, page):
    captured = {}
    def on_req(req):
        if '/api/questions' in req.url and req.method == 'GET':
            h = req.headers
            if 'authorization' in h:
                captured.update({k: h[k] for k in ('authorization', 'x-csrf-token', 'referer', 'user-agent') if k in h})
    page.on('request', on_req)
    page.goto(BASE + '/practice', wait_until='domcontentloaded', timeout=60000)
    try:
        page.wait_for_response(lambda r: '/api/questions' in r.url, timeout=30000)
    except Exception:
        pass
    page.wait_for_timeout(1200)
    if 'authorization' not in captured:
        raise RuntimeError('未截到 auth header（未登录？）')
    hdr = {k: captured[k] for k in ('authorization', 'x-csrf-token') if k in captured}
    hdr['Referer'] = BASE + '/practice'
    hdr['Accept'] = 'application/json'
    return hdr

def main():
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(PROFILE, headless=True,
            args=['--disable-blink-features=AutomationControlled'])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        hdr = get_headers(ctx, page)
        all_data = {}
        for cat in CATS:
            all_items = []
            page = 1
            while True:
                url = (BASE + '/api/questions?category_id=' + str(cat)
                       + '&question_list_id=mock-math-2&exam_subject=math_2'
                       + '&page=' + str(page) + '&per_page=20')
                r = ctx.request.get(url, headers=hdr, timeout=60000)
                data = r.json()
                d = data.get('data', data)
                items = d.get('items') or d.get('list') or d.get('questions') or []
                all_items.extend(items)
                tp = d.get('total_pages', 1)
                if page >= tp or not items:
                    break
                page += 1
            all_data[cat] = {'items': all_items, 'total': d.get('total'), 'total_pages': tp}
            print('cat', cat, 'status', r.status, 'n=', len(all_items), 'total=', d.get('total'))
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=1)
        print('saved ->', OUT)
        ctx.close()

if __name__ == '__main__':
    main()
