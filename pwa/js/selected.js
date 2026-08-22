// ============ 精选选填 · 复用真题系统核心逻辑（数据源：selected.json） ============

let papers = [];
let curPaper = null;
let favOnly = false;
let sideClosed = localStorage.getItem('examSideClosed') === '1';
const EXAM_POS_KEY = 'selPos'; // localStorage key（与真题隔离）

// ============ 收藏 ============
function qidOf(pid, no) { return pid + '-' + no; }
function isFav(qid) {
    try { return localStorage.getItem('selFav-' + qid) === '1'; } catch(e){return false;}
}
function toggleFav(qid, btn) {
    const v = !isFav(qid);
    try { localStorage.setItem('selFav-' + qid, v ? '1' : ''); } catch(e){}
    if(btn) { btn.classList.toggle('on', v); btn.textContent = v ? '⭐' : '☆'; }
    if(favOnly) renderCurrent();
}
function toggleFavOnly() {
    favOnly = !favOnly;
    document.getElementById('favOnly').classList.toggle('on', favOnly);
    renderCurrent();
}

// ============ 思路 / 笔记 ============
function noteGet(qid) {
    try { return localStorage.getItem('selNote-' + qid) || ''; } catch(e){return '';}
}
let _noteTimer = {};
function noteInput(ta) {
    const qid = ta.dataset.qid;
    clearTimeout(_noteTimer[qid]);
    _noteTimer[qid] = setTimeout(() => {
        try{localStorage.setItem('selNote-'+qid,ta.value);}catch(e){}
        const btn=ta.closest('.q-card')&&ta.closest('.q-card').querySelector('[data-act="note"]');
        if(btn)btn.classList.toggle('has',!!ta.value.trim());
    },500);
}
function toggleQSec(btn,act){
    const card=btn.closest('.q-card');if(!card)return;
    const sec=card.querySelector('.q-sec.q-'+act);if(!sec)return;
    const open=sec.hidden;sec.hidden=!open;btn.classList.toggle('on',open);
    if(act==='note'&&open){const ta=sec.querySelector('textarea');if(ta)ta.focus();}
}

// ============ Markdown → HTML ============
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function mdInline(s){return esc(s).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');}
function balanceDollars(s){const n=(s.match(/\$\$/g)||[]).length;return n%2===0?s:s+'$$';}
function mdBlock(s){
    s=balanceDollars(s);const lines=s.split('\n');const out=[];let mathBuf=null;
    for(const raw of lines){
        const l=raw.trim();if(!l){if(mathBuf){mathBuf+='\n';}continue;}
        if(mathBuf===null&&l.startsWith('$$')&&!l.endsWith('$$')){mathBuf=l;continue;}
        if(mathBuf!==null){mathBuf+='\n'+l;if(l.endsWith('$$')){out.push('<p>'+mdInline(mathBuf)+'</p>');mathBuf=null;}continue;}
        out.push('<p>'+mdInline(l)+'</p>');
    }if(mathBuf)out.push('<p>'+mdInline(mathBuf)+'</p>');
    return out.join('');
}

// ============ 渲染 ============
function secTag(si){return['一','二'][si]||(si+1);}

function qCard(p,sec,q){
    const qid=qidOf(p.id,q.no),fav=isFav(qid);
    const kindTag=q.kind==='choice'?'选择':'填空';
    const stem=mdBlock(q.stem);
    const figHtml=q.img?`<img class="q-fig-img" src="${q.img}" alt="题${q.no}配图" loading="lazy">${(q.img2?`<img class="q-fig-img" src="${q.img2}" alt="题${q.no}配图2" loading="lazy">`:'')}`:'';
    const options=q.options&&q.options.length?`<div class="q-options">${q.options.map((o,i)=>`<div class="q-opt"><span class="opt-label">${'ABCD'[i]}.</span>${mdInline(o)}</div>`).join('')}</div>`:'';
    const note=noteGet(qid);
    const ideaBtn=q.idea?`<button class="q-op" data-act="idea" onclick="toggleQSec(this,'idea')">思路</button>`:'';
    const ideaHtml=q.idea?`<div class="q-sec q-idea" hidden>${mdBlock(q.idea)}</div>`:'';
    // 答案：优先 q.answer 文本，否则 q.answer_img 图片数组，否则占位
    const ansInner = q.answer ? mdBlock(q.answer) :
        (q.answer_img ? ((Array.isArray(q.answer_img) ? q.answer_img : [q.answer_img])
            .map(s => `<img class="ans-img" src="${s}" alt="题${q.no}答案" loading="lazy" onclick="zoomAnsImg(this)">`).join(''))
            : '<span class="ans-pending">答案整理中…</span>');
    return `<div class="q-card" id="q-${qid}" data-qno="${q.no}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindTag}</span>
            <button class="q-fav${fav?' on':''}" onclick="toggleFav('${qid}',this)" title="收藏此题">${fav?'⭐':'☆'}</button>
        </div>
        <div class="q-body">${stem}${figHtml}${options}</div>
        <div class="q-ops">
            <button class="q-op" data-act="answer" onclick="toggleQSec(this,'answer')">查看答案</button>
            ${ideaBtn}
            <button class="q-op${note.trim()?' has':''}" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>
        </div>
        ${ideaHtml}
        <div class="q-sec q-answer" hidden><div class="q-answer-body">${ansInner}</div></div>
        <div class="q-sec q-note" hidden><textarea class="q-note-input" data-qid="${qid}" placeholder="记下你的思路、易错点…（自动保存）">${esc(note)}</textarea></div>
    </div>`;
}

function renderPaperList(){
    const el=document.getElementById('paperList');
    // 按 group 分组（目录树：组节点 → 套卷节点）
    const groups={};
    papers.forEach(p=>{
        const g=p.group||'其他';
        if(!groups[g])groups[g]=[];
        groups[g].push(p);
    });
    let html='';
    Object.keys(groups).forEach(g=>{
        const items=groups[g];
        const open=paperGroupOpen[g]!==false; // 默认展开
        html+=`<div class="paper-group" data-group="${esc(g)}">
            <div class="paper-group-head" onclick="toggleGroup('${esc(g)}')">
                <span class="paper-group-arrow">${open?'▾':'▸'}</span>
                <span class="paper-group-name">${esc(g)}</span>
                <span class="paper-group-count">${items.length}</span>
            </div>
            <div class="paper-group-body"${open?'':' style="display:none"'}>`;
        items.forEach(p=>{
            html+=`<button class="paper-item${curPaper&&curPaper.id===p.id?' on':''}" data-pid="${p.id}" onclick="openPaper('${p.id}')">
                <span class="paper-name">${esc(p.title.replace(/^24 |^25 /,''))}</span>
            </button>`;
        });
        html+='</div></div>';
    });
    el.innerHTML=html;
}

// 组折叠状态（session 级）
const paperGroupOpen={};

function toggleGroup(name){
    paperGroupOpen[name]=paperGroupOpen[name]===false?true:false;
    const g=document.querySelector(`.paper-group[data-group="${CSS.escape(name)}"]`);
    if(g){
        const body=g.querySelector('.paper-group-body');
        const arrow=g.querySelector('.paper-group-arrow');
        if(body)body.style.display=paperGroupOpen[name]?'':'none';
        if(arrow)arrow.textContent=paperGroupOpen[name]?'▾':'▸';
    }
}

// 搜索：匹配后展开父级组 + 滚动定位 + 高亮目标节点
function searchPaper(kw){
    kw=(kw||'').trim().toLowerCase();
    // 清除旧高亮
    document.querySelectorAll('.paper-item.hl').forEach(n=>n.classList.remove('hl'));
    if(!kw){return;}
    // 找到第一个匹配的套卷（标题或组名）
    let hit=null;
    for(const p of papers){
        const title=p.title.toLowerCase();
        const group=(p.group||'').toLowerCase();
        if(title.includes(kw)||group.includes(kw)){hit=p;break;}
    }
    if(!hit)return;
    const gName=hit.group||'其他';
    // 展开父级组
    paperGroupOpen[gName]=true;
    const g=document.querySelector(`.paper-group[data-group="${CSS.escape(gName)}"]`);
    if(g){
        const body=g.querySelector('.paper-group-body');
        const arrow=g.querySelector('.paper-group-arrow');
        if(body)body.style.display='';
        if(arrow)arrow.textContent='▾';
    }
    // 滚动定位 + 高亮目标
    const item=document.querySelector(`.paper-item[data-pid="${hit.id}"]`);
    if(item){
        item.classList.add('hl');
        item.scrollIntoView({behavior:'smooth',block:'center'});
    }
}

function renderCurrent(){
    const el=document.getElementById('examMain');
    if(!curPaper){el.innerHTML='<div class="loading">请选择一套卷</div>';return;}
    let html=`<div class="paper-head"><h1>${curPaper.title}</h1><div class="paper-meta">共 ${curPaper.sections.reduce((a,s)=>a+s.questions.length,0)} 题</div></div>`;
    let shown=0,total=0;
    curPaper.sections.forEach((sec,si)=>{
        const secQs=sec.questions.filter(q=>!favOnly||isFav(qidOf(curPaper.id,q.no)));
        total+=sec.questions.length;shown+=secQs.length;
        if(!secQs.length)return;
        html+=`<div class="q-section"><div class="q-section-title">${sec.type==='choice'?'一、选择题':'二、填空题'}</div>`;
        secQs.forEach(q=>{html+=qCard(curPaper,sec,q,si);});
        html+='</div>';
    });
    if(favOnly&&shown===0)html+='<div class="empty-tip">还没有收藏的题目，点击题目右上角 ☆ 收藏。</div>';
    el.innerHTML=html+(favOnly?`<div class="fav-count">收藏 ${shown}/${total} 题</div>`:'');
    renderMath(el);renderNav();
}

// ============ 导航 & 位置记忆 ============
function renderNav(){
    const el=document.getElementById('floatQNo');if(!el)return;
    const list=document.getElementById('floatQList');if(!list)return;
    if(!curPaper){el.textContent='—';list.innerHTML='';return;}
    const all=[];
    curPaper.sections.forEach((sec,si)=>{sec.questions.forEach(q=>all.push({no:q.no,tag:secTag(si)}));});
    el.textContent=(curPaper.group||'')+'·'+curPaper.title.replace(/^\d+\s*/,'');
    list.innerHTML=all.map(({no,tag})=>
        `<button class="nav-q${favOnly&&!isFav(qidOf(curPaper.id,no))?' hidden':''}"
         data-navq="${no}" onclick="jumpToQ(${no})">${no}</button>`
    ).join('');
    highlightNav();
}
function highlightNav(){
    const cards=[...document.querySelectorAll('.q-card')],btns=[...document.querySelectorAll('.nav-q')];
    if(!cards.length||!btns.length)return;
    const half=window.innerHeight*0.45;let cur=null;
    for(const c of cards){if(c.getBoundingClientRect().top<=half)cur=c;else break;}
    const curNo=cur?cur.getAttribute('data-qno'):null;
    btns.forEach(b=>b.classList.toggle('on',b.getAttribute('data-navq')===curNo));
}
function saveExamPos(){if(!curPaper)return;let no=null;const half=window.innerHeight*0.45;
    for(const c of document.querySelectorAll('.q-card')){if(c.getBoundingClientRect().top<=half)no=c.getAttribute('data-qno');else break;}
    try{localStorage.setItem(EXAM_POS_KEY,JSON.stringify({paperId:curPaper.id,no}));}catch(e){}
}
function jumpToQ(no){const el=document.getElementById('q-'+qidOf(curPaper.id,no));if(el)el.scrollIntoView({behavior:'smooth',block:'start'});}
let _qPosTimer=null;
document.addEventListener('scroll',()=>{highlightNav();if(!_qPosTimer)_qPosTimer=setTimeout(()=>{_qPosTimer=null;saveExamPos();},600);},{passive:true});
window.addEventListener('resize',highlightNav);
window.addEventListener('beforeunload',saveExamPos);

function renderMath(root){
    if(!window.katex||!root)return;
    try{renderMathInElement(root,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'$',right:'$',display:false}],throwOnError:false});}catch(e){}
}

function openPaper(id){
    curPaper=papers.find(p=>p.id===id);renderPaperList();renderCurrent();
    const sub=document.getElementById('examSub');if(sub&&curPaper)sub.textContent=curPaper.title;
    const q=document.querySelector('.q-card');if(q)q.scrollIntoView();
}

function toggleDark(){
    const d=document.documentElement.classList.toggle('dark');
    try{localStorage.setItem('darkMode',d?'1':'0');}catch(e){}
    document.getElementById('darkState').textContent=d?'开':'关';
}
function toggleSide(){
    sideClosed = !sideClosed;
    try{localStorage.setItem('examSideClosed', sideClosed ? '1' : '0');}catch(e){}
    const wrap = document.querySelector('.exam-wrap');
    const btn = document.getElementById('sideToggle');
    if (wrap) wrap.classList.toggle('side-closed', sideClosed);
    if (btn) btn.textContent = sideClosed ? '▶' : '◀';
}

// ============ 答案图放大 ============
function zoomAnsImg(img){
    let ov = document.getElementById('zoomOverlay');
    if (!ov) {
        ov = document.createElement('div');
        ov.id = 'zoomOverlay';
        ov.className = 'zoom-overlay';
        ov.onclick = function(){ ov.classList.remove('show'); };
        ov.innerHTML = '<img id="zoomImg" alt="放大答案">';
        document.body.appendChild(ov);
    }
    const big = document.getElementById('zoomImg');
    big.src = img.currentSrc || img.src;
    ov.classList.add('show');
}

// ============ 整卷答案 ============
function openPaperAnswers(){
    if (!curPaper) return;
    window.open('selected_ans.html?pid=' + encodeURIComponent(curPaper.id), '_blank');
}

function toggleFloatQ(){
    const fq=document.getElementById('floatQ');if(!fq)return;
    fq.classList.toggle('collapsed');fq.classList.toggle('expanded');
}

async function init(){
    // 恢复侧栏状态
    const wrap0 = document.querySelector('.exam-wrap');
    if (wrap0) wrap0.classList.toggle('side-closed', sideClosed);
    const btn0 = document.getElementById('sideToggle');
    if (btn0) btn0.textContent = sideClosed ? '▶' : '◀';
    const resp=await fetch('data/selected.json');
    if(!resp.ok)throw new Error('加载精选失败:'+resp.status);
    papers=(await resp.json()).papers || [];
    const favBtn=document.getElementById('favOnly');if(favBtn)favBtn.classList.toggle('on',favOnly);
    let startPaper=papers[0]||null,startNo=null;
    try{
        const pos=JSON.parse(localStorage.getItem(EXAM_POS_KEY));
        if(pos&&pos.paperId){const p=papers.find(x=>x.id===pos.paperId);if(p){startPaper=p;startNo=pos.no?parseInt(pos.no,10):null;}}
    }catch(e){}
    curPaper=startPaper;renderPaperList();renderCurrent();
    const sub=document.getElementById('examSub');if(sub&&curPaper)sub.textContent=curPaper.title;
    if(startNo){const q=document.getElementById('q-'+qidOf(curPaper.id,startNo));if(q)q.scrollIntoView({block:'start'});}
}
init();
