/* SVG 放大回归：SVG 改真实宽高重绘，位图保留 transform:scale。 */
const fs = require('fs');
const assert = require('assert');
const { JSDOM } = require('D:/ai code/408-quiz/node_modules/jsdom');

const ROOT = 'D:/ai code/math-note/pwa/js/';
const common = fs.readFileSync(ROOT + 'common.js', 'utf8');
const reader = fs.readFileSync(ROOT + 'reader.js', 'utf8');
const frag = reader.slice(reader.indexOf('// ============ 图片放大预览'),
                          reader.indexOf('// ============ KaTeX'));
assert(frag.includes('function openLightbox'), 'reader lightbox fragment missing');

function setup() {
    const dom = new JSDOM('<!doctype html><html><body></body></html>', {
        url: 'http://localhost/', runScripts: 'outside-only', pretendToBeVisual: true,
    });
    const w = dom.window;
    Object.defineProperty(w.HTMLImageElement.prototype, 'naturalWidth', {
        configurable: true,
        get() { const s = this.getAttribute('src') || ''; return s.indexOf('pic.svg') >= 0 ? 680 : s.indexOf('noattr.svg') >= 0 ? 300 : 1200; },
    });
    Object.defineProperty(w.HTMLImageElement.prototype, 'naturalHeight', {
        configurable: true,
        get() { const s = this.getAttribute('src') || ''; return s.indexOf('pic.svg') >= 0 ? 358 : s.indexOf('noattr.svg') >= 0 ? 150 : 800; },
    });
    Object.defineProperty(w.HTMLImageElement.prototype, 'complete', { configurable: true, get() { return true; } });
    w.fetch = () => Promise.resolve({ ok: true, text: () => Promise.resolve('<svg viewBox="0 0 800 400"></svg>') });
    w.eval(common);
    w.eval(frag);
    return w;
}
function wheel(w, node) {
    node.dispatchEvent(new w.WheelEvent('wheel', { deltaY: -100, clientX: 400, clientY: 300, bubbles: true }));
}

const w = setup();

w.zoomOverlayOpen('pic.svg');
let img = w.document.getElementById('zoomImg');
assert.strictEqual(img.style.width, '680px', 'SVG 初始基准宽应等于固有宽');
assert.strictEqual(img.style.maxWidth, 'none', 'SVG 需解除 max-width 钳制');
wheel(w, w.document.getElementById('zoomOverlay'));
assert(Math.abs(parseFloat(img.style.width) - 782) < 0.01, 'SVG 放大改真实宽高');
assert(!img.style.transform.includes('scale'), 'SVG transform 不能带 scale');

w.zoomOverlayOpen('photo.png');
img = w.document.getElementById('zoomImg');
wheel(w, w.document.getElementById('zoomOverlay'));
assert.strictEqual(img.style.width, '', '位图不改真实宽高');
assert(img.style.transform.includes('scale(1.15)'), '位图仍走 transform:scale');

w.openLightbox('pic.svg');
img = w.document.querySelector('#imgLightbox img');
assert.strictEqual(img.style.width, '680px', '笔记页 SVG 初始基准');
wheel(w, w.document.getElementById('imgLightbox'));
assert(Math.abs(parseFloat(img.style.width) - 782) < 0.01, '笔记页 SVG 放大改真实宽高');
assert(!img.style.transform.includes('scale'), '笔记页 SVG transform 不能带 scale');

(async () => {
    w.openLightbox('noattr.svg');
    await new Promise(r => setTimeout(r, 30));
    img = w.document.querySelector('#imgLightbox img');
    assert.strictEqual(img.style.width, '800px', '无 width/height 的 SVG 应从 viewBox 补比例');
    assert.strictEqual(img.style.height, '400px', 'viewBox 补出的高');
    console.log('SVG zoom: 8 assertions passed');
    process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
