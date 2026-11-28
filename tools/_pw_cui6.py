# -*- coding: utf-8 -*-
"""真机验证 27 崔命六套卷：模拟卷最前、Q3 配图、思路、原图页签、放大与点图关闭。"""
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:8766/exam.html'
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
    page.goto(URL, wait_until='load')
    page.wait_for_timeout(1800)

    state = page.evaluate("""() => {
        const titles = [...document.querySelectorAll('.paper-item')].map(b => b.textContent.trim());
        return {
            groups: [...document.querySelectorAll('.paper-group-head')].map(b => b.textContent.trim()),
            cui: titles.filter(t => t.includes('崔命六套卷')),
            idxCui: titles.findIndex(t => t.includes('崔命六套卷') && t.includes('第一套')),
            idx26: titles.findIndex(t => t.includes('26 押题王四套')),
            idxYt4: titles.findIndex(t => t.includes('押题王四套') && t.includes('第一套')),
            idxZs4: titles.findIndex(t => t.includes('张宇四套') && t.includes('第一套')),
            idx27: titles.findIndex(t => t.includes('精选十套')),
            n: titles.length,
        };
    }""")
    print('list:', state)
    assert len(state['cui']) == 5, '应列出 5 套崔命卷'
    assert state['idxCui'] >= 0, '崔6 第一套应在列表中'
    later = [state[k] for k in ('idx26', 'idxYt4', 'idxZs4', 'idx27') if state[k] >= 0]
    assert all(state['idxCui'] < x for x in later), '崔6 应在所有模拟卷最前'

    # 卷一 Q3（带配图）
    page.goto(URL + '?paper=mn27-cui6-1&no=3', wait_until='load')
    page.wait_for_timeout(1800)
    q3 = page.evaluate("""() => {
        const card = document.getElementById('q-mn27-cui6-1-3') || document.querySelector('.q-card');
        if (!card) return {card:false};
        const imgs = [...card.querySelectorAll('.q-body img')].map(i => ({src:i.getAttribute('src'), w:i.naturalWidth}));
        return {card:true, id:card.id, imgs,
                idea: !!card.querySelector('[data-act="idea"]'),
                ansTab: [...card.querySelectorAll('.q-answer .ans-tab')].map(b=>b.textContent.trim()),
                sub: document.getElementById('examSub')?.textContent};
    }""")
    print('Q3:', q3)
    assert q3['card'] and q3['id'] == 'q-mn27-cui6-1-3'
    assert q3['imgs'] and any('mn27_qcui01_03.png' in i['src'] and i['w'] > 0 for i in q3['imgs']), '配图应加载'
    assert q3['idea'] and q3['ansTab'] == ['文字解析', '原图解析']
    assert '崔命六套卷' in (q3['sub'] or '')

    # 卷五 Q10（人工补锚点）原图
    page.goto(URL + '?paper=mn27-cui6-5&no=10', wait_until='load')
    page.wait_for_timeout(1500)
    page.evaluate("""() => {
        const c = document.querySelector('#q-mn27-cui6-5-10 [data-act="answer"]');
        if (c) c.click();
        const t = [...document.querySelectorAll('#q-mn27-cui6-5-10 .q-answer .ans-tab')].find(b => b.textContent.includes('原图'));
        if (t) t.click();
    }""")
    page.wait_for_timeout(500)
    imgs = page.evaluate("""() => [...document.querySelectorAll('#q-mn27-cui6-5-10 .q-answer img.q-ans-img')]
        .map(i => ({src:i.getAttribute('src'), w:i.naturalWidth, h:i.naturalHeight}))""")
    print('V5Q10 imgs:', imgs)
    assert len(imgs) >= 1 and all(i['w'] > 0 for i in imgs), 'V5Q10 原图应加载'
    assert all('mn27cui6pdf-5-10_' in i['src'] for i in imgs), '原图命名正确'

    # 放大 + 点大图关闭
    page.locator('#q-mn27-cui6-5-10 .q-answer img.q-ans-img').first.click()
    page.wait_for_timeout(300)
    z = page.evaluate("""() => {
        const o = document.getElementById('zoomOverlay');
        return {show: o?.classList.contains('show'), src: o?.querySelector('#zoomImg')?.getAttribute('src')};
    }""")
    print('zoom:', z)
    assert z['show'], '放大遮罩应打开'
    page.locator('#zoomImg').click(position={'x': 60, 'y': 60})
    page.wait_for_timeout(350)
    closed = page.evaluate("() => !document.getElementById('zoomOverlay').classList.contains('show')")
    assert closed, '点大图应关闭'

    assert not errors, 'console errors: ' + str(errors[:5])
    browser.close()
    print('playwright cui6 ok')
