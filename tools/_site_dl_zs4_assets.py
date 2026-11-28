# -*- coding: utf-8 -*-
"""下载「27张四卷」原始参考答案（源文件顺序）里的原图，按卷/题/序命名。"""
import json, os, re
from playwright.sync_api import sync_playwright

PROFILE = r'E:/deps_cache/browser-profiles/cxymath_pw'
BASE = 'https://math.cxyonly.fans'
RAW = r'D:/ai code/math-note/tools/_zs4_raw.json'
IMGDIR = r'D:/ai code/math-note/pwa/data/img/zx_site'
MAP = r'D:/ai code/math-note/tools/_zs4_asset_map.json'
CAT2NO = {12981: 1, 12982: 2, 12983: 3, 12984: 4}

def get_hdr(ctx, page):
    cap = {}
    def on_req(req):
        if '/api/questions' in req.url and req.method == 'GET':
            h = req.headers
            if 'authorization' in h:
                cap.update({k: h[k] for k in ('authorization', 'x-csrf-token') if k in h})
    page.on('request', on_req)
    page.goto(BASE + '/practice', wait_until='domcontentloaded', timeout=60000)
    try: page.wait_for_response(lambda r: '/api/questions' in r.url, timeout=30000)
    except Exception: pass
    page.wait_for_timeout(1000)
    if 'authorization' not in cap: raise RuntimeError('未截到 auth')
    hdr = dict(cap); hdr['Referer'] = BASE + '/practice'; hdr['Accept'] = 'application/json'
    return hdr

def main():
    raw = json.load(open(RAW, encoding='utf-8'))
    # 按题收集 asset://（仅 explanation_md 中「原始参考答案」段），按出现顺序
    jobs = []
    for cat, obj in raw.items():
        for it in obj['items']:
            exp = it['document'].get('explanation_md') or ''
            if '原始参考答案' not in exp:
                continue
            # 只取「原始参考答案」标题之后的 asset 链接（保持顺序，去重）
            tail = exp.split('原始参考答案', 1)[1]
            refs = re.findall(r'asset://sha256/([0-9a-f]{64})', tail)
            seen = set(); refs = [r for r in refs if not (r in seen or seen.add(r))]
            if refs:
                jobs.append((CAT2NO[int(cat)], it['serial_number'], it['id'], refs))

    amap = {}
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(PROFILE, headless=True,
            args=['--disable-blink-features=AutomationControlled'])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        hdr = get_hdr(ctx, page)
        os.makedirs(IMGDIR, exist_ok=True)
        for paper_no, qno, site_id, refs in jobs:
            paths = []
            for idx, sha in enumerate(refs):
                rel = 'data/img/zx_site/mn27-zs4-%d-%d_%d.png' % (paper_no, qno, idx)
                dst = os.path.join(IMGDIR, 'mn27-zs4-%d-%d_%d.png' % (paper_no, qno, idx))
                r = ctx.request.get(BASE + '/api/v1/questions/%d/assets/%s' % (site_id, sha),
                                    headers=hdr, timeout=60000)
                if r.status != 200 or not r.body().startswith(b'\x89PNG'):
                    raise RuntimeError('下载失败 %s status=%s head=%r' % (rel, r.status, r.body()[:20]))
                open(dst, 'wb').write(r.body())
                print('OK', rel, len(r.body()), 'bytes')
                paths.append(rel)
            amap['%d-%d' % (paper_no, qno)] = {'siteId': site_id, 'paths': paths}
        ctx.close()
    json.dump(amap, open(MAP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('共', sum(len(v['paths']) for v in amap.values()), '张图 ->', MAP)

if __name__ == '__main__':
    main()
