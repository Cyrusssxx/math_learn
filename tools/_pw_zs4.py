# -*- coding: utf-8 -*-
"""真机验证 27 张宇四套卷接入 exam.html：试卷分组/顺序、答题卡、思路、原图页签与放大。"""
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

    # 试卷列表：模拟卷分组应含 4 套张宇四套，且顺序在押题王之后
    state = page.evaluate("""() => {
        const titles = [...document.querySelectorAll('.paper-item')].map(b => b.textContent.trim());
        return {
            groups: [...document.querySelectorAll('.paper-group-head')].map(b => b.textContent.trim()),
            zs4: titles.filter(t => t.includes('张宇四套')),
            idxYt4: titles.findIndex(t => t.includes('押题王四套') && t.includes('第一套')),
            idxZs4: titles.findIndex(t => t.includes('张宇四套') && t.includes('第一套')),
            idxMock27: titles.findIndex(t => t.includes('27 精选') || t.includes('27模拟') || t.includes('精选十套')),
            n: titles.length,
        };
    }""")
    print('list:', state)
    assert len(state['zs4']) == 4, '应列出 4 套张宇四卷'
    assert state['idxYt4'] < state['idxZs4'], '张宇四套应在押题王之后'
    assert all('押题王' not in t for t in state['zs4'])

    # 打开第三套第 20 题（带 2 张原图）
    page.evaluate("() => openPaper('mn27-zs4-3')")
    page.wait_for_timeout(400)
    page.evaluate("() => { const b=[...document.querySelectorAll('.float-q-item,.q-nav-item,.qnum-item')].find(x=>x.textContent.trim()==='20'); if(b) b.click(); }")
    page.wait_for_timeout(300)
    # 若题号导航选择器不同，直接用 URL 下钻
    page.goto(URL + '?paper=mn27-zs4-3&no=20', wait_until='load')
    page.wait_for_timeout(1800)
    q = page.evaluate("""() => {
        const card = document.getElementById('q-mn27-zs4-3-20') || document.querySelector('.q-card');
        const tabs = card ? [...card.querySelectorAll('.q-answer .ans-tab')] : [];
        return {
            card: !!card,
            id: card?.id,
            stem: (card?.querySelector('.q-body')?.textContent || '').slice(0, 80),
            hasIdeaBtn: !!card?.querySelector('[data-act="idea"]'),
            hasAnsTab: !!tabs.length,
            tabText: tabs.map(b=>b.textContent.trim()),
            sub: document.getElementById('examSub')?.textContent,
        };
    }""")
    print('Q20:', q)
    assert q['card'], '题卡应渲染'
    assert q['hasIdeaBtn'], '应有思路按钮'
    assert q['hasAnsTab'] and q['tabText'] == ['文字解析', '原图解析'], '应有文字/原图双页签'
    assert '张宇四套' in (q['sub'] or '')

    # 展开答案 → 原图页签 → 2 张图且 src 正确
    page.evaluate("""() => {
        const b = document.querySelector('#q-mn27-zs4-3-20 [data-act="answer"]');
        if (b) b.click();
    }""")
    page.wait_for_timeout(300)
    page.evaluate("""() => {
        const t = [...document.querySelectorAll('#q-mn27-zs4-3-20 .q-answer .ans-tab')].find(b => b.textContent.includes('原图'));
        if (t) t.click();
    }""")
    page.wait_for_timeout(400)
    imgs = page.evaluate("""() => [...document.querySelectorAll('#q-mn27-zs4-3-20 .q-answer img.q-ans-img')].map(i => ({
        src: i.getAttribute('src'), w: i.naturalWidth, h: i.naturalHeight,
    }))""")
    print('imgs:', imgs)
    assert len(imgs) == 2, 'Q20 应有 2 张原图'
    assert all('mn27-zs4-3-20' in i['src'] for i in imgs), '原图路径正确'
    assert all(i['w'] > 0 for i in imgs), '原图应成功加载'

    # 点原图放大 → 再点关闭
    page.locator('#q-mn27-zs4-3-20 .q-answer img.q-ans-img').first.click()
    page.wait_for_timeout(250)
    shown = page.evaluate("() => document.getElementById('zoomOverlay')?.classList.contains('show')")
    assert shown, '点原图应放大'
    page.locator('#zoomImg').click(position={'x': 20, 'y': 20})
    page.wait_for_timeout(250)
    closed = page.evaluate("() => !document.getElementById('zoomOverlay')?.classList.contains('show')")
    assert closed, '点大图应关闭'

    print('console errors:', errors[:5])
    assert not errors, '不应有 console error'
    browser.close()
print('playwright zs4 ok')
