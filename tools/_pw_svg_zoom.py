from playwright.sync_api import sync_playwright

URL = 'file:///D:/ai%20code/math-note/pwa/index.html'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 900})
    page.goto(URL, wait_until='load')
    page.wait_for_timeout(1500)
    page.evaluate("""() => {
        const i = document.createElement('img');
        i.className = 'li-img';
        i.id = 'testSvg';
        i.src = 'data/img/closed_region_max.svg';
        document.body.appendChild(i);
        i.click();
    }""")
    page.wait_for_timeout(300)
    state = page.evaluate("""() => {
        const i = document.querySelector('#imgLightbox img');
        return {w: i.style.width, h: i.style.height, t: i.style.transform, mw: i.style.maxWidth};
    }""")
    print('open:', state)
    page.mouse.move(600, 450)
    page.mouse.wheel(0, -120)
    page.wait_for_timeout(150)
    state2 = page.evaluate("""() => {
        const i = document.querySelector('#imgLightbox img');
        return {w: i.style.width, h: i.style.height, t: i.style.transform, pct: document.getElementById('lbPct').textContent};
    }""")
    print('zoom:', state2)
    assert state['w'] == '680px' and state['mw'] == 'none'
    assert 'scale' not in state2['t'] and float(state2['w'].replace('px', '')) > 680
    browser.close()
    print('playwright svg zoom ok')
