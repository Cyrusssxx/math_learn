/* 数学好题刷题模块 - 加载 good.json，按知识板块分组，逐题渲染（复用 mdrender.js 渲染管线） */

let goodNotes = [];
let curNote = null;
let favOnly = false;
let goodFilter = '';
let currentQs = [];                       // 当前专题渲染出的小题 [{idx, title, faved}]
const openBoards = JSON.parse(localStorage.getItem('goodBoards') || '{}');

const BOARD_ORDER = ['函数·极限·连续', '导数与微分', '一元函数积分学', '微分方程',
    '多元微分与积分', '线性代数', '综合与技巧'];

// ============ 知识板块归类（按专题名关键词） ============
function boardOf(name, title) {
    const t = name + ' ' + title;
    if (/矩阵|线性|特征|二次型|相似|正交|无关|方程组/.test(t)) return '线性代数';
    if (/方程/.test(t)) return '微分方程';
    if (/二重积分|多元/.test(t)) return '多元微分与积分';
    if (/积分/.test(t)) return '一元函数积分学';
    if (/导数|微分|泰勒|不等式|放缩|构造|证明/.test(t)) return '导数与微分';
    if (/极限|函数|连续|间断/.test(t)) return '函数·极限·连续';
    return '综合与技巧';
}

// ============ 收藏/错题（localStorage: { topicId: [qIdx,...] }） ============
function getFav() { try { return JSON.parse(localStorage.getItem('goodFav')) || {}; } catch (e) { return {}; } }
function isFav(topicId, qi) { const f = getFav(); return (f[topicId] || []).includes(qi); }

function toggleFav(topicId, qi, btn) {
    const f = getFav();
    const arr = f[topicId] || (f[topicId] = []);
    const i = arr.indexOf(qi);
    if (i >= 0) arr.splice(i, 1); else arr.push(qi);
    if (arr.length === 0) delete f[topicId];
    localStorage.setItem('goodFav', JSON.stringify(f));
    if (btn) {
        const added = i < 0;
        btn.classList.toggle('on', added);
        btn.textContent = added ? '★' : '☆';
    }
    updateTopicFavFlag(topicId);
    renderFloat();
    if (favOnly) renderCurrent();        // 错题本模式下移除即消失
}

function updateTopicFavFlag() { renderSidebar(); }

// ============ 初始化 ============
async function init() {
    const resp = await fetch('data/good.json');
    if (!resp.ok) throw new Error('加载好题数据失败: ' + resp.status);
    goodNotes = await resp.json();
    goodNotes.sort((a, b) => a.order - b.order);
    renderSidebar();
    renderDarkSwitch();
    if (goodNotes[0]) openTopic(goodNotes[0].id);
}

// ============ 左侧专题分组 ============
function renderSidebar() {
    const list = document.getElementById('topicList');
    const fav = getFav();
    const q = goodFilter.trim().toLowerCase();
    const boards = {};
    goodNotes.forEach(n => {
        const b = boardOf(n.name, n.title);
        (boards[b] = boards[b] || []).push(n);
    });
    let html = '';
    for (const b of BOARD_ORDER) {
        if (!boards[b]) continue;
        let items = boards[b];
        if (q) items = items.filter(n => (n.name + n.title).toLowerCase().includes(q));
        if (items.length === 0) continue;
        const closed = openBoards[b] === false;
        const favCnt = items.reduce((s, n) => s + (fav[n.id] ? fav[n.id].length : 0), 0);
        html += `<div class="board-group ${closed ? 'closed' : ''}" data-board="${b}">
            <div class="board-head" onclick="toggleBoard('${b}')">
                <span class="board-arrow">›</span>${b}
                <span class="board-count">${items.length}${favCnt ? (' ·★' + favCnt) : ''}</span>
            </div>
            <div class="board-items">` +
            items.map(n => {
                const on = curNote && curNote.id === n.id;
                const hasFav = !!(fav[n.id] && fav[n.id].length);
                const tag = n.name.split('-')[0].replace('好题', '#');
                const shortTitle = n.title.replace(/^好题\d+\s*/, '');
                return `<button class="topic-item ${on ? 'on' : ''} ${hasFav ? 'has-fav' : ''}"
                        data-id="${n.id}" onclick="openTopic('${n.id}')">
                    <span class="topic-tag">${tag}</span>
                    <span class="topic-name">${esc(shortTitle)}</span>
                    <span class="topic-fav">★</span>
                </button>`;
            }).join('') +
            `</div></div>`;
    }
    if (!html) html = '<div class="empty-tip">无匹配专题</div>';
    list.innerHTML = html;
}

function toggleBoard(b) {
    openBoards[b] = openBoards[b] === false;
    localStorage.setItem('goodBoards', JSON.stringify(openBoards));
    renderSidebar();
}

function openTopic(id) {
    curNote = goodNotes.find(n => n.id === id) || null;
    renderSidebar();
    renderCurrent();
}

function onGoodSearch(v) { goodFilter = v; renderSidebar(); }

// ============ 中栏：逐题卡片 ============
function renderTopicCards(note, onlyFav) {
    const raw = mdToHtml(note.md);
    const segs = raw.split(/(?=<h2 id="ch-\d+">)/g);
    let html = '';
    currentQs = [];
    let qi = 0;
    segs.forEach(seg => {
        if (!seg.startsWith('<h2')) { html += `<div class="q-intro">${seg}</div>`; return; }
        if (onlyFav && !isFav(note.id, qi)) { qi++; return; }
        const m = seg.match(/<h2 id="(ch-\d+)">([\s\S]*?)<\/h2>/);
        const title = m ? m[2] : '题';
        const faved = isFav(note.id, qi);
        html += `<section class="q-card" id="q-${seg.match(/ch-(\d+)/)[1]}">
            <div class="q-head">
                <span class="q-no">题${qi + 1}</span>
                <span class="q-title">${title}</span>
                <button class="q-fav ${faved ? 'on' : ''}" data-q="${qi}"
                        onclick="toggleFav('${note.id}', ${qi}, this)" title="收藏/加入错题本">${faved ? '★' : '☆'}</button>
            </div>
            <div class="q-body">${seg.replace(/<h2 id="ch-\d+">[\s\S]*?<\/h2>/, '')}</div>
        </section>`;
        currentQs.push({ idx: qi, title: title, faved: faved });
        qi++;
    });
    return html;
}

function renderCurrent() {
    const el = document.getElementById('goodMain');
    if (!curNote) {
        el.innerHTML = '<div class="loading">选择左侧专题开始刷题…</div>';
        renderFloat();
        return;
    }
    const cards = renderTopicCards(curNote, favOnly);
    let body = `<div class="good-topic-head"><h1>${inline(curNote.title)}</h1>
        <div class="good-topic-meta">${curNote.chapters.length} 个小题 · 点击 ⭐ 收藏到错题本</div></div>` + cards;
    if (favOnly && currentQs.length === 0) {
        body += `<div class="empty-tip">这个专题还没有收藏的题目。<br>关掉「收藏夹」去刷题，点 ⭐ 把做错的收进来。</div>`;
    }
    el.innerHTML = body;
    document.title = curNote.title + ' - 好题刷题';
    renderMath(el);
    window.scrollTo({ top: 0, behavior: 'instant' });
    renderFloat();
}

// ============ 悬浮题号导航 ============
function renderFloat() {
    const list = document.getElementById('floatQList');
    const no = document.getElementById('floatQNo');
    if (!curNote || currentQs.length === 0) { list.innerHTML = ''; no.textContent = '—'; return; }
    no.textContent = '题' + currentQs.length;
    list.innerHTML = currentQs.map((q, i) =>
        `<div class="nav-q ${q.faved ? 'faved' : ''}" data-i="${i}" onclick="gotoQ(${i})">${q.idx + 1}</div>`
    ).join('');
}

function gotoQ(i) {
    const el = document.getElementById('q-' + currentQs[i].idx);
    if (el) el.scrollIntoView({ block: 'start', behavior: 'smooth' });
}

function toggleFloatQ() { document.getElementById('floatQ').classList.toggle('expanded'); }

// 滚动高亮当前题
let _qSpy = null;
window.addEventListener('scroll', () => {
    if (_qSpy) return;
    _qSpy = setTimeout(() => { _qSpy = null; highlightQ(); }, 80);
}, { passive: true });

function highlightQ() {
    if (!curNote || currentQs.length === 0) return;
    let active = -1;
    for (const q of currentQs) {
        const el = document.getElementById('q-' + q.idx);
        if (el && el.getBoundingClientRect().top <= 90) active = q.idx;
        else break;
    }
    document.querySelectorAll('.nav-q').forEach(b =>
        b.classList.toggle('on', parseInt(b.dataset.i, 10) === active));
}

// ============ 收藏夹总开关 ============
function toggleFavOnly() {
    favOnly = !favOnly;
    document.getElementById('favOnly').classList.toggle('on', favOnly);
    if (favOnly) {
        const fav = getFav();
        const hasFav = curNote && fav[curNote.id] && fav[curNote.id].length;
        if (!hasFav) {
            // 当前专题无收藏 → 跳到第一个有收藏的专题
            const id = Object.keys(fav).find(k => fav[k] && fav[k].length);
            if (id) curNote = goodNotes.find(n => n.id === id) || curNote;
        }
    }
    renderSidebar();
    renderCurrent();
}

// ============ 图片灯箱（与笔记站一致） ============
function openLightbox(src) {
    let lb = document.getElementById('imgLightbox');
    if (!lb) {
        lb = document.createElement('div');
        lb.id = 'imgLightbox';
        lb.innerHTML = '<img alt="放大预览">';
        lb.onclick = () => lb.classList.remove('show');
        document.addEventListener('keydown', e => { if (e.key === 'Escape') lb.classList.remove('show'); });
        document.body.appendChild(lb);
    }
    lb.querySelector('img').src = src;
    lb.classList.add('show');
}
document.addEventListener('click', e => {
    const img = e.target.closest('.q-body img, .q-intro img, img.li-img, .md-img img');
    if (img && img.src) { e.stopPropagation(); openLightbox(img.src); }
});

// ============ Service Worker ============
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js').catch(err => {
            console.warn('SW 注册失败（file:// 下属正常，请用 start.bat 启动）:', err);
        });
    });
}

init().catch(e => {
    document.getElementById('goodMain').innerHTML =
        `<div class="error">加载失败: ${esc(e.message)}<br>请用 start.bat 启动后访问 http://localhost:8409</div>`;
});
