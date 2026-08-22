// ============ 整卷选填答案页 ============
// URL 参数: ?pid=y24-cy-01  渲染该卷全部选填题答案图

let papers = [];
let curPaper = null;

function qidOf(pid, no) { return pid + '-' + no; }

function esc(s) {
    return String(s == null ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// 答案图放大（与 selected.js 同一套遮罩）
function zoomAnsImg(img) {
    let ov = document.getElementById('zoomOverlay');
    if (!ov) {
        ov = document.createElement('div');
        ov.id = 'zoomOverlay';
        ov.className = 'zoom-overlay';
        ov.onclick = function () { ov.classList.remove('show'); };
        ov.innerHTML = '<img id="zoomImg" alt="放大答案">';
        document.body.appendChild(ov);
    }
    const big = document.getElementById('zoomImg');
    big.src = img.currentSrc || img.src;
    ov.classList.add('show');
}

function renderAll() {
    const el = document.getElementById('saList');
    if (!curPaper) { el.innerHTML = '<div class="empty-tip">未指定试卷（缺少 ?pid= 参数）</div>'; return; }
    const sub = document.getElementById('examSub');
    if (sub) sub.textContent = curPaper.title;
    document.title = curPaper.title + ' · 整卷选填答案';

    const secTitles = { choice: '一、选择题', fill: '二、填空题' };
    let html = `<div class="sa-paper-head"><h1>${esc(curPaper.title)}</h1><div class="sa-meta">共 ${curPaper.sections.reduce((a, s) => a + s.questions.length, 0)} 题 · 全部答案</div></div>`;
    curPaper.sections.forEach(sec => {
        html += `<div class="sa-sec"><div class="sa-sec-title">${secTitles[sec.type] || sec.type || '题目'}</div>`;
        sec.questions.forEach(q => {
            const imgs = q.answer_img
                ? (Array.isArray(q.answer_img) ? q.answer_img : [q.answer_img])
                : [];
            html += `<div class="sa-q" id="saq-${q.no}">
                <div class="sa-q-no">${q.no}</div>
                ${imgs.length ? imgs.map(s =>
                    `<img class="ans-img" src="${s}" alt="题${q.no}答案" loading="lazy" onclick="zoomAnsImg(this)">`
                ).join('') : `<div class="ans-pending">答案整理中…</div>`}
            </div>`;
        });
        html += '</div>';
    });
    el.innerHTML = html;
    renderNav();
}

// 题号快捷导航
function renderNav() {
    const el = document.getElementById('saNav');
    if (!el) return;
    const all = [];
    curPaper.sections.forEach((sec, si) => {
        sec.questions.forEach(q => all.push({ no: q.no, tag: ['一', '二'][si] || si + 1 }));
    });
    el.innerHTML = all.map(({ no, tag }) =>
        `<button class="sa-nav-q" data-navq="${no}" onclick="jumpToQ(${no})">${no}</button>`
    ).join('');
    // 滚动高亮
    const half = window.innerHeight * 0.4;
    const onScroll = () => {
        let cur = null;
        for (const c of document.querySelectorAll('.sa-q')) {
            if (c.getBoundingClientRect().top <= half) cur = c;
            else break;
        }
        const curNo = cur ? cur.getAttribute('id').slice(4) : null;
        document.querySelectorAll('.sa-nav-q').forEach(b =>
            b.classList.toggle('on', b.getAttribute('data-navq') === curNo));
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
}

function jumpToQ(no) {
    const el = document.getElementById('saq-' + no);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function init() {
    const params = new URLSearchParams(location.search);
    const pid = params.get('pid');
    try {
        const resp = await fetch('data/selected.json');
        if (!resp.ok) throw new Error('加载失败 ' + resp.status);
        papers = (await resp.json()).papers || [];
    } catch (e) {
        document.getElementById('saList').innerHTML =
            `<div class="empty-tip">加载数据失败：${esc(e.message)}</div>`;
        return;
    }
    curPaper = papers.find(p => p.id === pid) || null;
    renderAll();
}

init();
