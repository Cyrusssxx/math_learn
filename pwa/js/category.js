/* 分类题库浏览页：左=二级分类树（学科/章节，可折叠、含题数），右=选中章节的跨年真题
 * 分类口径：大观园「知识点/章节」体系（exam_categories.json 的 12 个二级章节）。
 * 复用 exam.js 的渲染 / 收藏辅助函数（独立副本，避免改动 exam.js 既有行为）。 */

const FAV_KEY = 'examFav';            // { qid: 1 }，qid = 套卷id-题no
const FAV_ONLY_KEY = 'examFavOnly';   // 是否只看收藏（常量保留，界面已由三选筛选替代）
const EXAM_STATUS_KEY = 'examStatus';   // { qid: 'unfamiliar' | 'unknown' }：不熟/不会掌握度标记（互斥）

// ============ 每日做题数据 ============
// markDaily / dailyRecent / dailyStreak 定义在 js/common.js（所有页面都加载，
// 这样真题页 exam.js 的那份 toggleStatus/toggleFav 副本也能一并记录）。
// 本页只在 toggleStatus / toggleFav 里调用。

// ============ 收藏存储 ============
// 收藏/标记统一主键：核心题库/线代题库的题若映射到数二真题（linkedQid），直接沿用真题的 qid，
// 从而与「真题页 / 分类题库」的收藏、不熟、不会标记、笔记双向同步。
let coreLink = {};   // 题目 (paperId + '-' + no 或 q.no) -> linkedQid
function qidOf(paperId, no) {
    const k = paperId + '-' + no;
    if (coreLink[k]) return coreLink[k];
    if (paperId === 'core' && coreLink[no]) return coreLink[no];
    if (paperId === 'xd' && coreLink[no]) return coreLink[no];
    return k;
}

// 旧版核心题库曾用 'core-<no>' 作为收藏/标记/笔记主键；主键统一为真题 qid 后需一次性迁移：
// 目标键为空才搬（不覆盖真题侧已有数据），搬完删旧键，保证用户旧标记/旧笔记不"消失"。
function migrateCoreLegacyKeys() {
    try {
        // 直接用核心题库数据（q.no → linkedQid），不依赖 coreLink 的键形式
        const pairs = [];
        for (const sec of (corePapers[0] && corePapers[0].sections) || []) {
            for (const q of sec.questions || []) {
                if (q.linkedQid) pairs.push([q.no, q.linkedQid]);
            }
        }
        if (!pairs.length) return;
        const fav = favGet(), st = statusGet();
        let fC = false, sC = false;
        for (const [no, lq] of pairs) {
            const oldKey = 'core-' + no;
            if (fav[oldKey]) { if (!fav[lq]) fav[lq] = fav[oldKey]; delete fav[oldKey]; fC = true; }
            if (st[oldKey]) { if (!st[lq]) st[lq] = st[oldKey]; delete st[oldKey]; sC = true; }
            const nk = 'examNote-' + lq, ok = 'examNote-' + oldKey;
            const v = localStorage.getItem(ok);
            if (v !== null && v !== '') {
                if (!localStorage.getItem(nk)) localStorage.setItem(nk, v);
                localStorage.removeItem(ok);
            }
        }
        if (fC) favSave(fav);
        if (sC) statusSave(st);
    } catch (e) { console.error('核心题库旧主键迁移失败', e); }
}
/** 线代重点题并入 core_bank 后的一次性主键迁移（2026-10-11）。
 *  背景：线代重点题原为独立文件 xd_bank.json，主键 = qidOf('xd', no)，即
 *  「有 linkedQid → linkedQid，无 → 'xd-<no>'」。物理并入 core_bank 后题号重编
 *  （743 起），主键变为 qidOf('core', 新号)，即「有 linkedQid → linkedQid，无 → 'core-<新号>'」。
 *  所以只有**无 linkedQid** 那批的键变了（'xd-<原号>' → 'core-<新号>'），必须搬迁，
 *  否则用户在这批题上的收藏/标记/笔记会整体消失。
 *  与 migrateCoreLegacyKeys 同策略：目标键为空才搬（不覆盖已有数据），搬完删旧键。
 *  ⚠️ 必须在 coreLink 构建完成之后调用（qidOf 依赖它），且只需跑一次。 */
function migrateXdLegacyKeys() {
    try {
        const pairs = [];
        for (const p of (corePapers || [])) {
            for (const s of (p.sections || [])) {
                for (const q of (s.questions || [])) {
                    if (q.fromX && q.xdNo != null) pairs.push([String(q.xdNo), qidOf('core', q.no)]);
                }
            }
        }
        if (!pairs.length) return;
        const fav = favGet(), st = statusGet();
        let fC = false, sC = false, movedN = 0;
        for (const [oldNo, newKey] of pairs) {
            const oldKey = 'xd-' + oldNo;
            if (oldKey === newKey) continue;          // 有 linkedQid：新旧主键相同，无需搬
            if (fav[oldKey]) { if (!fav[newKey]) fav[newKey] = fav[oldKey]; delete fav[oldKey]; fC = true; movedN++; }
            if (st[oldKey]) { if (!st[newKey]) st[newKey] = st[oldKey]; delete st[oldKey]; sC = true; movedN++; }
            const nk = 'examNote-' + newKey, ok = 'examNote-' + oldKey;
            const v = localStorage.getItem(ok);
            if (v !== null && v !== '') {
                if (!localStorage.getItem(nk)) localStorage.setItem(nk, v);
                localStorage.removeItem(ok);
            }
        }
        if (fC) favSave(fav);
        if (sC) statusSave(st);
        if (movedN) console.info('[迁移] 线代重点题旧主键已搬到新号：' + movedN + ' 项');
    } catch (e) { console.error('线代重点题旧主键迁移失败', e); }
}

/** 错误关联修复的一次性标记迁移（2026-10-11）。
 *  背景：25 组共 133 道题的 linkedQid 是与己无关的真题题（如 41 道极限题都链到
 *  2002数二真题-4），qidOf 重定向让它们共享收藏/标记键 —— 在一道上标记，整组跟着变。
 *  数据侧已清除这些错误 linkedQid，并在两类题上留了迁移线索：
 *    · linkedQidOld —— 清除前的旧键（用户标记可能在这里）
 *    · linkFix.from —— 组内确有一道与真题题同题（相似度 ≥0.6）时的精确迁移目标
 *  本函数把旧键上的用户标记**复制**到该题的新主键（core-<no>）。
 *  ⚠️ 复制而非移动：真题页仍以旧键读标记，两边都可见（同题，语义正确）。
 *  幂等：目标键已有值则跳过，可重复执行。
 *  ⚠️ 与 migrateXdLegacyKeys 的区别：那个搬移（旧键删除），这个复制（旧键保留）。 */
function migrateLinkFixKeys() {
    try {
        const fav = favGet(), st = statusGet();
        let fC = false, sC = false, nC = 0;
        // ⚠️ 防御：同一 old 键只允许迁移到**一道**题。
        //    历史上有 22 个旧键被 132 道题共享（批量清除错误关联留下的），
        //    逐个复制会把同一份笔记灌到 N 道无关题上（2026-10-13 用户报 413/414 串号）。
        //    数据侧已保证唯一，这里再兜一层，避免将来数据回潮又踩同一个坑。
        const seen = new Set();
        for (const p of (corePapers || [])) {
            for (const s of (p.sections || [])) {
                for (const q of (s.questions || [])) {
                    const old = (q.linkFix && q.linkFix.from) || q.linkedQidOld;
                    if (!old) continue;
                    if (seen.has(old)) continue;      // 已被别的题用过，跳过
                    const newKey = qidOf(p.id, q.no);
                    if (newKey === old) continue;
                    seen.add(old);
                    if (fav[old] && !fav[newKey]) { fav[newKey] = fav[old]; fC = true; }
                    if (st[old] && !st[newKey]) { st[newKey] = st[old]; sC = true; }
                    const nk = 'examNote-' + newKey, ok = 'examNote-' + old;
                    const v = localStorage.getItem(ok);
                    if (v !== null && v !== '' && !localStorage.getItem(nk)) {
                        localStorage.setItem(nk, v); nC++;
                    }
                }
            }
        }
        if (fC) favSave(fav);
        if (sC) statusSave(st);
        if (fC || sC || nC) console.info('[迁移] linkFix/linkedQidOld 标记已复制到新主键');
    } catch (err) { console.error('linkFix 标记迁移失败', err); }
}

/** 跨年同题「别名」标记迁移（2026-10-11）。
 *  背景：真题卷之间存在重复题（如 2023-1 与 2016-9 是同一道「斜渐近线」题），
 *  核心题库只收录了其中一份，并用其 linkedQid 作主键。linkedQid 是**一对一**机制
 *  （一道 core 题只能占一个真题键，否则回潮到「一道上标记、整组跟着变」的老 bug），
 *  所以用户在**另一年份**的同题上做的标记/笔记无法靠补 linkedQid 同步。
 *  数据侧改用别名：core 题上标 linkAlias = [同题的其它年份真题键]。
 *  本函数把别名键上的收藏/标记/笔记**复制**到该题主键，使核心题库里能看到。
 *  ⚠️ 复制而非移动：真题页仍以各自年份的键读标记，两边都可见（同题，语义正确）。
 *  ⚠️ 幂等 —— 目标键已有值则跳过，可重复执行。 */
function migrateAliasKeys() {
    try {
        const fav = favGet(), st = statusGet();
        let fC = false, sC = false, nC = 0;
        for (const p of (corePapers || [])) {
            for (const s of (p.sections || [])) {
                for (const q of (s.questions || [])) {
                    const al = q.linkAlias;
                    if (!al || !al.length) continue;
                    const newKey = qidOf(p.id, q.no);
                    for (const old of al) {
                        if (!old || old === newKey) continue;
                        if (fav[old] && !fav[newKey]) { fav[newKey] = fav[old]; fC = true; }
                        if (st[old] && !st[newKey]) { st[newKey] = st[old]; sC = true; }
                        const nk = 'examNote-' + newKey, ok = 'examNote-' + old;
                        const v = localStorage.getItem(ok);
                        if (v !== null && v !== '' && !localStorage.getItem(nk)) {
                            localStorage.setItem(nk, v); nC++;
                        }
                    }
                }
            }
        }
        if (fC) favSave(fav);
        if (sC) statusSave(st);
        if (fC || sC || nC) console.info('[迁移] 跨年同题别名标记已复制到主键');
    } catch (err) { console.error('跨年同题别名标记迁移失败', err); }
}

/** 孤儿笔记接回（2026-10-13）。
 *  背景：历史 bug 让 `ta.dataset.qid` 缺失时仍执行写盘，落出 `examNote-undefined` 键。
 *  用户数据里该键有真实内容「然后谱分解[图:b57da806...]」—— 经比对，其中的图片 id
 *  与 xd-169（线代重点题，已并入 core_bank 的 no=844）笔记里的图片**完全相同**，
 *  可判定是那次保存丢了 qid、没挂到题上的**同一段笔记**，不是新内容。
 *  本函数把它接回 core-844（xd-169 的迁移目标），接完删掉孤儿键。
 *  ⚠️ 防重复的判据是**去掉 [图:id] 令牌后的正文**，不能拿图片 id 判：
 *     这段笔记复用了同一张图，图片 id 在目标笔记里本来就有，
 *     拿 id 判会把该接回的正文也误判成「已存在」（实测踩过）。
 *  ⚠️ 幂等：可重复执行。必须在 migrateXdLegacyKeys() 之后调用。 */
/** 清理「共享旧键」造成的历史误复制（2026-10-13）。
 *  根因：早期 migrateLinkFixKeys 对每道题都执行 old → 主键 的复制，而当年批量清除
 *  错误 linkedQid 时**同一批题留下了同一个 old 键**（22 个旧键被 132 道题共享），
 *  结果同一份笔记被复制到 N 道无关的题上（用户实测：`2007数二真题-13` 的
 *  「n! 别忘了」出现在 no=413/414 等偏导数题上）。
 *  数据侧已把共享组改为「只有真同题迁移、其余写 linkedQidDead」，本函数清理**已发生**
 *  的误复制。判据（都要求与 dead 键逐字节/同时间戳一致，避免误删用户自己的标记）：
 *    · 笔记：主键笔记 === dead 键笔记
 *    · 收藏：fav[主键].t === fav[dead].t（复制时时间戳原样带回，是可靠指纹）
 *  状态值只有三种、无法区分复制与自标，故**不动**（保守）。
 *  ⚠️ 幂等；在 migrateLinkFixKeys 之后调用。 */
function migrateDropDeadCopies() {
    try {
        const fav = favGet();
        let nN = 0, nF = 0;
        for (const p of (corePapers || [])) {
            for (const s of (p.sections || [])) {
                for (const q of (s.questions || [])) {
                    const dead = q.linkedQidDead;
                    if (!dead) continue;
                    const key = qidOf(p.id, q.no);
                    if (!key || key === dead) continue;
                    const nk = 'examNote-' + key, ok = 'examNote-' + dead;
                    const cur = localStorage.getItem(nk), src = localStorage.getItem(ok);
                    if (cur && src && cur === src) { localStorage.removeItem(nk); nN++; }
                    if (fav[key] && fav[dead] && fav[key].t === fav[dead].t) { delete fav[key]; nF++; }
                }
            }
        }
        if (nF) favSave(fav);
        if (nN || nF) console.info('[清理] 移除共享旧键造成的误复制：笔记 ' + nN + ' 条、收藏 ' + nF + ' 条');
    } catch (err) { console.error('误复制清理失败', err); }
}

function migrateOrphanNote() {
    try {
        const ORPHAN = 'examNote-undefined';
        const raw = localStorage.getItem(ORPHAN);
        if (raw === null || raw === '') { localStorage.removeItem(ORPHAN); return; }
        const bare = s => (s || '').replace(/\[图:[a-z0-9]+\]/g, '');
        // 目标题：xd-169 并入 core_bank 后的 no=844
        const q = (corePapers || []).flatMap(p => (p.sections || []).flatMap(s => s.questions || []))
            .find(x => x.fromX && String(x.xdNo) === '169');
        if (!q) { console.warn('[孤儿笔记] 找不到 xd-169 对应的 core 题，保留孤儿键待查'); return; }
        const tgt = qidOf(corePapers[0].id, q.no);
        const tgtKey = 'examNote-' + tgt, cur = localStorage.getItem(tgtKey) || '';
        const frag = bare(raw).trim();
        if (frag && bare(cur).indexOf(frag) < 0) {
            localStorage.setItem(tgtKey, cur ? cur.replace(/\s*$/, '') + '\n' + raw : raw);
            console.info('[孤儿笔记] 已接回 ' + tgt + '：' + frag.slice(0, 40));
        } else {
            console.info('[孤儿笔记] 目标笔记已含该正文，仅清理孤儿键');
        }
        localStorage.removeItem(ORPHAN);
    } catch (err) { console.error('孤儿笔记接回失败', err); }
}

function favGet() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || {}; } catch (e) { return {}; }
}
function favSave(obj) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(obj)); }
    catch (e) { console.error('收藏保存失败:', e); alert('收藏存储空间不足，保存失败。'); }
}
// ============ 掌握度标记（不熟/不会，互斥单选；与收藏独立） ============
function statusGet() {
    try { return JSON.parse(localStorage.getItem(EXAM_STATUS_KEY)) || {}; } catch (e) { return {}; }
}
function statusSave(obj) {
    try { localStorage.setItem(EXAM_STATUS_KEY, JSON.stringify(obj)); } catch (e) { }
}
function statusOf(qid) { return statusGet()[qid] || null; }
// 互斥切换：v='unfamiliar'|'unknown'；同值再次调用则清除（不熟 ⇄ 不会 ⇄ 无）
function toggleStatus(qid, v) {
    const s = statusGet();
    if (s[qid] === v) delete s[qid]; else s[qid] = v;
    statusSave(s);
    markDaily(qid, s[qid] || 'cleared');   // 记入「每日做题」（取消标记也算动过这道题）
    return s[qid] || null;
}
function isFav(qid) { return !!favGet()[qid]; }
function favTime(qid) {
    const v = favGet()[qid];
    return (v && typeof v === 'object') ? (v.t || 0) : 0;
}
function fmtFavTime(ts) {
    if (!ts) return '';
    const d = new Date(ts), p = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
}
function fmtFavShort(ts) {   // 星标旁的短日期：月-日
    if (!ts) return '';
    const d = new Date(ts), p = n => String(n).padStart(2, '0');
    return p(d.getMonth() + 1) + '-' + p(d.getDate());
}
// 一次性迁移：旧格式收藏（{qid:1}，无时间戳）补上「今天」的时间并写回存储
function migrateFavTimes() {
    const f = favGet();
    let changed = false;
    for (const k in f) {
        if (!f[k] || typeof f[k] !== 'object') { f[k] = { t: Date.now() }; changed = true; }
    }
    if (changed) favSave(f);
}
migrateFavTimes();
function toggleFav(qid, btn) {
    const f = favGet();
    if (f[qid]) delete f[qid]; else f[qid] = { t: Date.now() };
    favSave(f);
    markDaily(qid, f[qid] ? 'fav' : 'unfav');   // 记入「每日做题」
    if (btn) {
        const on = !!f[qid];
        btn.classList.toggle('on', on);
        btn.textContent = on ? '⭐' : '☆';
        btn.title = on ? (favTime(qid) ? '收藏于 ' + fmtFavTime(favTime(qid)) : '已收藏（时间未知）') : '收藏此题';
        // 就地同步星标左侧的日期徽标
        const card = btn.closest('.q-card');
        if (card) {
            let badge = card.querySelector('.q-fav-date');
            const t = favTime(qid);
            if (on && t) {
                if (!badge) {
                    badge = document.createElement('span');
                    badge.className = 'q-fav-date';
                    btn.parentNode.insertBefore(badge, btn);
                }
                badge.textContent = fmtFavShort(t);
                badge.title = '收藏于 ' + fmtFavTime(t);
            } else if (badge) badge.remove();
        }
    }
    // 任一筛选开启时，实时刷新分类树与题目列表
    if (markSel.fav || markSel.unfamiliar || markSel.unknown) { renderTree(); renderMain(); }
}

// 掌握度/收藏多选筛选（默认全选，并集去重；收藏/不熟/不会互不归属）
let markSel = { fav: false, unfamiliar: false, unknown: false }; // 收藏 / 不熟 / 不会 分开筛选；默认都不选 = 显示全部
function toggleMark(m) {
    markSel[m] = !markSel[m];
    document.querySelectorAll('.cat-mark').forEach(b => b.classList.toggle('on', markSel[b.dataset.m]));
    const sy = window.scrollY;   // 保持滚动位置，避免树高变化导致弹跳
    renderTree();
    renderMain();
    requestAnimationFrame(() => window.scrollTo(0, sy));
}

// ============ 合并数据：现有数二真题 + 大观园数二真题（统一一棵分类树） ============
let bankItems = [];      // 大观园数二真题（categoryIds 已映射到统一分类体系：知识点 L2 或 年份节点）
// 线代重点题（原 xd_bank.json）已于 2026-10-11 物理并入 core_bank.json，
// 题上带 fromX=true / xdNo=原号；并入后不再有独立的 xdItems 容器。

// ============ Markdown / KaTeX 渲染（与 exam.js 同源） ============
function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function mdInline(s) {
    return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}
function balanceDollars(s) {
    const n = (s.match(/\$\$/g) || []).length;
    return n % 2 === 0 ? s : s + '$$';
}
function mdBlock(s) {
    s = balanceDollars(s);
    const lines = s.split('\n');
    const out = [];
    let buf = null;
    for (const raw of lines) {
        // 只去普通空格/制表符，保留 NBSP（承载用户打的缩进/连续空格；raw.trim() 会连 NBSP 一起删）
        // 行首普通空格转 NBSP：单个行首空格浏览器不自动转 NBSP，渲染端兜底保留缩进（与 exam.js/exam-shared.js 同步）
        const l = raw
            .replace(/^[ \t]+/, m => m.replace(/[ \t]/g, '\u00A0'))
            .replace(/[ \t]+$/, '')                        // 行尾普通空格照旧删除（NBSP 不在此类）
            .replace(/ {2,}/g, m => m.replace(/ /g, '\u00A0'));   // 行内连续普通空格(2+)转 NBSP：防 HTML 折叠丢空格（单个空格不受影响）
        if (!l) { if (buf) buf += '\n'; continue; }
        // 裸 "$$" 独占一行也要开块：'$$'.endsWith('$$') 恒为真，旧条件会让多行显示块整体失效（与 exam.js 同步修）
        if (buf === null && l.startsWith('$$') && l.endsWith('$$') && l !== '$$') { out.push('<p>' + mdInline(l) + '</p>'); continue; }   // 同行首尾 $$：整行显示块
        if (buf === null && l.startsWith('$$') && (!l.endsWith('$$') || l === '$$')) { buf = l; continue; }
        if (buf !== null) {
            buf += '\n' + l;
            if (l.endsWith('$$')) { out.push('<p>' + mdInline(buf) + '</p>'); buf = null; }
            continue;
        }
        // 裸公式行兜底：无 $ 包裹但整行是 LaTeX（且不含中文）→ 自动补 $ 渲染。
        // 数据里偶有漏包 $ 的公式行（如解答中的 g_y=... / g_{xy}=... 连续两行），
        // 不兜底就会以 LaTeX 原文显示（用户看到「公式没渲染」）。
        if (!l.includes('$') && !/[\u4e00-\u9fff]/.test(l) && l.trim().length > 3
            && /\\[a-zA-Z]{2,}/.test(l) && /[=+\-\^_{}]/.test(l)) {
            const disp = /\\begin\{/.test(l) || /\\end\{/.test(l);
            let t = l;
            if (disp) {
                // 自动补齐缺失的 \\end{X}（数据里常见「多行显示块被压成单行」）
                const envs = [...t.matchAll(/\\begin\{([^}]+)\}/g)].map(m => m[1]);
                for (const env of envs) {
                    const nB = (t.match(new RegExp('\\\\begin\\{' + env + '\\}', 'g')) || []).length;
                    const nE = (t.match(new RegExp('\\\\end\\{' + env + '\\}', 'g')) || []).length;
                    for (let k = nB - nE; k > 0; k--) t += '\\end{' + env + '}';
                }
            }
            out.push('<p>' + mdInline((disp ? '$$' : '$') + t + (disp ? '$$' : '$')) + '</p>');
            continue;
        }
        // 笔记标题令牌（<h1>/<h2>）独占整行时作为块级标题输出，不放进 <p>
        if (l.startsWith('<h1>') || l.startsWith('<h2>')) {
            out.push(mdInline(l));
        } else {
            out.push('<p>' + mdInline(l) + '</p>');
        }
    }
    if (buf) out.push('<p>' + mdInline(buf) + '</p>');
    // 笔记令牌还原（与 exam.js 对齐：高亮/字色 → 行内标签，粗体/斜体 → 行内标签，H1/H2 → 块级标题）
    return out.join('')
        .replace(/&lt;h:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/h&gt;/g, '<mark class="note-hl" style="background:$1">$2</mark>')
        .replace(/&lt;c:(#[0-9a-fA-F]{6})&gt;([\s\S]*?)&lt;\/c&gt;/g, '<span style="color:$1">$2</span>')
        .replace(/&lt;b&gt;([\s\S]*?)&lt;\/b&gt;/g, '<b>$1</b>')
        .replace(/&lt;i&gt;([\s\S]*?)&lt;\/i&gt;/g, '<i>$1</i>')
        .replace(/&lt;h1&gt;([\s\S]*?)&lt;\/h1&gt;/g, '<h1>$1</h1>')
        .replace(/&lt;h2&gt;([\s\S]*?)&lt;\/h2&gt;/g, '<h2>$1</h2>')
        .replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (_, alt, src) =>
            /^data\/img\/[a-zA-Z0-9_./-]+$/.test(src)
                ? `<span class="exam-fig-wrap"><img class="exam-fig" src="${src}" alt="${String(alt).replace(/"/g, '&quot;')}" onclick="zoomAnsImg(this)" loading="lazy"></span>`
                : '');
}
function renderMath(root) {
    if (!window.katex || !root) return;
    try {
        renderMathInElement(root, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '\\[', right: '\\]', display: true },
                { left: '\\(', right: '\\)', display: false },
                { left: '$', right: '$', display: false },
            ],
            throwOnError: false,
        });
    } catch (e) { /* ignore */ }
}

// ============ 配图单击放大（复用 exam.css 的 .zoom-overlay 遮罩） ============
function zoomAnsImg(img) {
    let ov = document.getElementById('zoomOverlay');
    if (!ov) {
        ov = document.createElement('div');
        ov.id = 'zoomOverlay';
        ov.className = 'zoom-overlay';
        ov.onclick = function () { ov.classList.remove('show'); };
        ov.innerHTML = '<img id="zoomImg" alt="放大图片">';
        const big = ov.querySelector('#zoomImg');
        big.onclick = function (e) { e.stopPropagation(); };
        document.body.appendChild(ov);
        document.addEventListener('keydown', function onEsc(e) {
            if (e.key === 'Escape') { ov.classList.remove('show'); document.removeEventListener('keydown', onEsc); }
        });
    }
    const big = document.getElementById('zoomImg');
    big.src = img.currentSrc || img.src;
    ov.classList.add('show');
}

// ============ 笔记（仅预览，复用 [图:id] 占位符；编辑在真题页进行） ============
function noteGet(qid) {
    try { return localStorage.getItem('examNote-' + qid) || ''; } catch (e) { return ''; }
}
// ============ 笔记富文本编辑器（2019+ 与真题页同款：contenteditable + 字色/高亮/H标题 + 贴图压缩存 IndexedDB） ============
// 以下为 exam.js 移植副本；两页改动需同步（记忆：mdBlockWithImg/fillExamNoteImgs/zoomAnsImg 等重复副本）

let _noteTimer = {};
// ---- contenteditable 富编辑器：[图:id] 内嵌图片 + 字色/高亮（存储为令牌 <c:#hex>…</c> <h:#hex>…</h>） ----
const NOTE_FMT_RE = /<c:(#[0-9a-fA-F]{6})>|<h:(#[0-9a-fA-F]{6})>|<\/c>|<\/h>|<b>|<\/b>|<i>|<\/i>|<h1>|<\/h1>|<h2>|<\/h2>/g;
/** 存储文本 → 编辑器 DOM：文本/换行原样，[图:id] 变为编辑器内联图片（contenteditable=false，可拖拽排序/删除/点击放大），格式令牌变 span/mark（栈式嵌套） */
function noteToEditor(el, text) {
    el.innerHTML = '';
    const stack = [el];
    const emitText = s => {
        const lines = s.split('\n');
        lines.forEach((line, k) => {
            if (k > 0) stack[stack.length - 1].appendChild(document.createElement('br'));
            if (line) stack[stack.length - 1].appendChild(document.createTextNode(line));
        });
    };
    let i = 0;
    while (i < text.length) {
        const mi = text.indexOf('[图:', i);
        NOTE_FMT_RE.lastIndex = i;
        const mf = NOTE_FMT_RE.exec(text);
        if (mf && (mi < 0 || mf.index <= mi)) {
            emitText(text.slice(i, mf.index));
            const m0 = mf[0];
            if (m0 === '</c>' || m0 === '</h>' || m0 === '</b>' || m0 === '</i>' || m0 === '</h1>' || m0 === '</h2>') {
                if (stack.length > 1) stack.pop();
            } else {
                let node;
                if (m0 === '<b>') node = document.createElement('b');
                else if (m0 === '<i>') node = document.createElement('i');
                else if (m0 === '<h1>') node = document.createElement('h1');
                else if (m0 === '<h2>') node = document.createElement('h2');
                else if (mf[1]) node = Object.assign(document.createElement('span'), { style: 'color:' + mf[1] });
                else node = Object.assign(document.createElement('mark'), { style: 'background:' + mf[2] });
                stack[stack.length - 1].appendChild(node);
                stack.push(node);
            }
            i = mf.index + mf[0].length;
        } else if (mi >= 0) {
            emitText(text.slice(i, mi));
            const m2 = /\[图:([a-z0-9]+)\]/.exec(text.slice(mi));
            if (m2) stack[stack.length - 1].appendChild(noteImgNode(m2[1]));
            i = mi + (m2 ? m2[0].length : 1);
        } else {
            emitText(text.slice(i));
            i = text.length;
        }
    }
}
function appendNoteText(el, chunk) {
    const lines = chunk.split('\n');
    lines.forEach((line, i) => {
        if (i > 0) el.appendChild(document.createElement('br'));
        if (line) el.appendChild(document.createTextNode(line));
    });
}
function noteImgNode(id) {
    const wrap = document.createElement('span');
    wrap.className = 'exam-note-img-wrap';
    wrap.draggable = true;
    const img = document.createElement('img');
    img.className = 'exam-note-img';
    img.dataset.img = id;
    img.alt = '笔记图片';
    img.setAttribute('contenteditable', 'false');
    img.onclick = () => zoomAnsImg(img);
    const del = document.createElement('button');
    del.type = 'button';
    del.className = 'exam-note-img-del';
    del.title = '删除图片';
    del.textContent = '×';
    del.onclick = () => {
        // 编辑模式内直接删除（不弹确认）：与 exam.js 同步
        delExamNoteImg(id, del);
    };
    wrap.append(img, del);
    // 编辑器内拖拽排序：拖动图片调整顺序，落点顺序即存储顺序（editorToNote 按 DOM 位置序列化）
    wrap.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', id);
        e.dataTransfer.effectAllowed = 'move';
        wrap.classList.add('dragging');
    });
    wrap.addEventListener('dragend', () => {
        wrap.classList.remove('dragging');
        document.querySelectorAll('.exam-note-img-wrap.over').forEach(w => w.classList.remove('over'));
    });
    wrap.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; wrap.classList.add('over'); });
    wrap.addEventListener('dragleave', () => wrap.classList.remove('over'));
    wrap.addEventListener('drop', e => {
        e.preventDefault();
        wrap.classList.remove('over');
        const dragged = document.querySelector('.exam-note-img-wrap.dragging');
        if (!dragged || dragged === wrap) return;
        const r = wrap.getBoundingClientRect();
        const after = (e.clientY - r.top) > r.height / 2;
        if (after) wrap.after(dragged); else wrap.before(dragged);
        const sec = wrap.closest('.q-note');
        const ta = sec && sec.querySelector('.q-note-input');
        if (ta) noteInput(ta);   // 顺序变更即落盘 + 刷新预览
    });
    return wrap;
}
/** 编辑器 DOM → 存储文本：图片还原 [图:id]，带格式的文本节点包令牌（字色/高亮/粗体/斜体走行内令牌，H1/H2 走块级令牌包裹整段） */

function editorToNote(el) {
    const rgbToHex = v => {
        const m = /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(v || '');
        return m ? '#' + [1, 2, 3].map(k => (+m[k]).toString(16).padStart(2, '0')).join('') : null;
    };
    // 任意颜色串（hex/rgb/命名色）归一为 #rrggbb；借助临时元素让浏览器自行规范化
    const normColor = v => { if (!v) return null; const tmp = document.createElement('span'); tmp.style.color = v; return rgbToHex(tmp.style.color); };
    const isBold = n => (n && n.nodeType === 1) && (n.tagName === 'B' || n.tagName === 'STRONG' || /bold/i.test(n.style.fontWeight || ''));
    const isItalic = n => (n && n.nodeType === 1) && (n.tagName === 'I' || n.tagName === 'EM' || /italic/i.test(n.style.fontStyle || ''));
    // 提取节点自身携带的「字色/高亮」：style.color / style.backgroundColor，并兼容浏览器 foreColor
    // 生成的 <font color> / <font bgcolor>。元素没带颜色时沿用父级上下文（c/h）。
    // 关键：粗/斜节点上同样可能带颜色（加粗后再上色、或 Chrome 把 font-weight 与 color 写在同一个
    // span 上），过去 isBold/isItalic 分支不读颜色 → 序列化只留下 <b>/<i>，颜色「染不上」。
    const colorOf = (ch, c, h) => {
        let nc = c, nh = h;
        if (ch.style) {
            const hc = normColor(ch.style.color); if (hc) nc = hc;
            const hb = normColor(ch.style.backgroundColor); if (hb) nh = hb;
        }
        const fattr = ch.getAttribute && ch.getAttribute('color');
        if (fattr) { const fc = normColor(fattr); if (fc) nc = fc; }
        const fbg = ch.getAttribute && ch.getAttribute('bgcolor');
        if (fbg) { const fb = normColor(fbg); if (fb) nh = fb; }
        return [nc, nh];
    };
    // 返回序列化片段；c/h=字色/高亮 hex，b/i=是否处于粗/斜上下文（行内令牌），heading 由 H1/H2 元素单独包块级令牌
    let base = (function run(n, c, h, b, i) {
        let s = '';
        for (const ch of n.childNodes) {
            if (ch.nodeType === 3) {
                // 保留 NBSP（\u00A0）：浏览器用它保真「行首空格 / 连续空格」，降级成普通空格会被 trim 与 HTML 折叠吃掉
                const t = ch.nodeValue.replace(/\u200B/g, '').replace(/ {2,}/g, m => m.replace(/ /g, '\u00A0'));  // 只丢弃零宽空格分隔符；连续普通空格转 NBSP（HTML 会折叠连续普通空格，单个空格不受影响）
                if (!t) continue;
                let inner = t;
                if (i) inner = '<i>' + inner + '</i>';
                if (b) inner = '<b>' + inner + '</b>';
                if (h) inner = '<h:' + h + '>' + inner + '</h>';
                if (c) inner = '<c:' + c + '>' + inner + '</c>';
                s += inner;
            } else if (ch.nodeType === 1) {
                if (ch.classList && ch.classList.contains('exam-note-img-wrap')) {
                    const img = ch.querySelector('img[data-img]');
                    if (img) s += '[图:' + img.dataset.img + ']';
                }
                else if (ch.tagName === 'IMG' && ch.dataset.img) s += '[图:' + ch.dataset.img + ']';
                else if (ch.tagName === 'BR') s += '\n';
                else if (ch.tagName === 'H1') {
                    if (s && !s.endsWith('\n')) s += '\n';
                    s += '<h1>' + run(ch, c, h, false, false) + '</h1>' + '\n';
                }
                else if (ch.tagName === 'H2') {
                    if (s && !s.endsWith('\n')) s += '\n';
                    s += '<h2>' + run(ch, c, h, false, false) + '</h2>' + '\n';
                }
                else if (isBold(ch)) {
                    // 粗体节点上的字色/高亮同样要保留（加粗后再上色的常见顺序）
                    const [bc, bh] = colorOf(ch, c, h);
                    const block = ch.tagName === 'DIV' || ch.tagName === 'P';
                    if (block && s && !s.endsWith('\n')) s += '\n';
                    s += run(ch, bc, bh, true, i);
                    if (block && s && !s.endsWith('\n')) s += '\n';
                }
                else if (isItalic(ch)) {
                    const [ic, ih] = colorOf(ch, c, h);
                    s += run(ch, ic, ih, b, true);
                }
                else {
                    let nc = c, nh = h;
                    if (ch.style) {
                        const hc = normColor(ch.style.color); if (hc) nc = hc;
                        const hb = normColor(ch.style.backgroundColor); if (hb) nh = hb;
                    }
                    // 兼容 <font color="..."> / <font bgcolor="...">：部分浏览器 foreColor/hiliteColor 生成 font 而非 span，颜色只在属性上、style.color 为空
                    const fattr = ch.getAttribute && ch.getAttribute('color');
                    if (fattr) { const fc = normColor(fattr); if (fc) nc = fc; }
                    const fbg = ch.getAttribute && ch.getAttribute('bgcolor');
                    if (fbg) { const fb = normColor(fbg); if (fb) nh = fb; }
                    const block = ch.tagName === 'DIV' || ch.tagName === 'P';
                    if (block && s && !s.endsWith('\n')) s += '\n';
                    s += run(ch, nc, nh, b, i);
                    if (block && s && !s.endsWith('\n')) s += '\n';
                }
            }
        }
        return s;
    })(el, null, null, false, false);
    return base;
}
/** 统一取值：textarea.value 或 编辑器序列化文本 */
function noteVal(el) {
    return el.tagName === 'TEXTAREA' ? el.value : editorToNote(el);
}
/** 统一写入 */
function setNoteContent(el, text) {
    if (el.tagName === 'TEXTAREA') el.value = text;
    else noteToEditor(el, text);
}

let _noteLastRendered = {};   // qid → 上次渲染预览的文本（内容没变不重渲，防闪烁）
const _pendingImgs = new Set();   // 正在压缩/写库的图 id：orphan 清理必须跳过，否则会被误删
const _pendingImgTasks = {};   // id → 写库 Promise：手动保存前 await，杜绝「压缩未完成就落盘 → 预览图变『图片已丢失』」
/** 等待所有贴图压缩/写库完成（无 pending 立即 resolve；写库失败不抛出） */
function waitPendingImgs() {
    const tasks = Object.values(_pendingImgTasks).filter(Boolean);
    return tasks.length ? Promise.all(tasks).catch(() => { }) : Promise.resolve();
}
function noteInput(ta) {
    const qid = ta.dataset.qid;
    if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);   // 编辑器自增长，无需 JS 调高
    noteHint(ta, '自动保存中…', true);
    clearTimeout(_noteTimer[qid]);
    _noteTimer[qid] = setTimeout(() => {
        // 落盘时重新取实时值，不用 1.5s 前的闭包旧快照：
        // 异步贴图可能已在此期间登记进编辑器，用旧快照会把新贴的图判成"不再引用"而删掉（丢图根因）
        const finalVal = noteVal(ta);
        const newRefs = examImgRefs(finalVal);
        const olds = localStorage.getItem('examNote-' + qid) || '';
        const oldRefs = examImgRefs(olds);
        // 写入中的图（压缩/写库未完成）绝不当孤儿删
        const orphan = oldRefs.filter(id => !newRefs.includes(id) && !_pendingImgs.has(id));
        if (orphan.length) examImgDel(orphan);   // 清理不再引用的图，避免存储泄漏
        try { localStorage.setItem('examNote-' + qid, finalVal); } catch (e) { }
        const btn = ta.closest('.q-card') && ta.closest('.q-card').querySelector('[data-act="note"]');
        if (btn) btn.classList.toggle('has', !!finalVal.trim());
        noteHint(ta, finalVal.trim() ? '已保存 ✓' : '笔记是空的，不保存');
        // 编辑态实时预览：内容有变化才重渲染（KaTeX/图片回填开销大，无变化重渲是闪烁根源）
        if (ta.style.display !== 'none') renderNotePreview(ta);
    }, 1500);
}
// 编辑态实时预览：从编辑器当前内容渲染 Markdown + 图片（内容未变直接跳过，避免闪烁）
function renderNotePreview(ta) {
    if (!ta || ta.style.display === 'none') return;   // 只读态：保存路径已渲染最终只读预览，跳过——避免被覆盖成编辑态样式
    const sec = ta.closest('.q-note');
    const pv = sec && sec.querySelector('.q-note-preview');
    if (!pv) return;
    const v = noteVal(ta);
    if (_noteLastRendered[ta.dataset.qid] === v) return;   // 内容没变：跳过
    _noteLastRendered[ta.dataset.qid] = v;
    pv.hidden = false;
    pv.classList.add('pv-edit');               // 编辑态预览：限高缩短（图片本体现在显示在编辑器内）
    pv.innerHTML = mdBlockWithImg(v, true);
    if (v.includes('$') || v.includes('\\(') || v.includes('\\[')) renderMath(pv);
    fillExamNoteImgs(pv);   // 异步回填 IndexedDB 中的 blob
}
// 笔记区 Ctrl+V 贴图：支持一次粘贴多张图（遍历全部 image item；纯文本 html 内的 data 图也提取），
// 压缩后存 IndexedDB；每张图独立 id/节点/写库任务，杜绝「多图只存一张」。

function notePasteImg(e) {
    const ta = e.target;
    const items = [...(e.clipboardData?.items || [])];
    let files = items.filter(i => i.type.startsWith('image/')).map(it => it.getAsFile()).filter(Boolean);
    // 无独立 image item（Word/网页复制图文混排常只有 text/html）：提取其中的 data: 图兜底
    if (!files.length && e.clipboardData?.getData) {
        let html = '';
        try { html = e.clipboardData.getData('text/html') || ''; } catch (err) { }
        if (html) {
            const srcs = [...html.matchAll(/<img[^>]+src=["'](data:image\/[^"']+)["']/gi)].map(m => m[1]);
            files = srcs.map(src => {
                try {
                    const i = src.indexOf(','), meta = src.slice(5, i);
                    return new File([Uint8Array.from(atob(src.slice(i + 1)), c => c.charCodeAt(0))], 'img.png', { type: meta.split(';')[0] });
                } catch (err) { return null; }
            }).filter(Boolean);
        }
    }
    if (!files.length) {
        // 纯文本粘贴：降级为纯文本，防外来 HTML 污染编辑器
        if (ta.tagName !== 'TEXTAREA' && e.clipboardData?.getData) {
            e.preventDefault();
            const txt = e.clipboardData.getData('text/plain');
            if (txt) document.execCommand('insertText', false, txt);
        }
        return;
    }
    e.preventDefault();
    files.forEach(file => pasteOneNoteImg(ta, file));
}
// 粘贴单张图：登记节点（同步，防保存时序丢令牌）→ 原图落库兜底 → 压缩覆盖 → 回填
function pasteOneNoteImg(ta, raw) {
    // 碰撞免疫：优先 crypto.randomUUID（去连字符后全 [a-z0-9]，匹配现有正则），杜绝毫秒内连贴同 id
    const id = (crypto.randomUUID ? crypto.randomUUID().replace(/-/g, '') : (Date.now().toString(36) + Math.random().toString(36).slice(2, 6)));
    _pendingImgs.add(id);   // 标记写入中：orphan 清理跳过，杜绝「压缩未完成被当孤儿删掉」
    // 关键：同步把图片节点登记进编辑器，让 editorToNote 立刻抓到 [图:id]。
    // 原实现把插入放在 compressImage→examImgPut 两级异步之后，压缩大图要几百 ms，
    // 期间任何保存（1.5s 防抖 / 翻页 flush）都会存下不含该图的版本并触发误删 → 丢图。
    if (ta.tagName === 'TEXTAREA') {
        const tag = `[图:${id}]`;
        const p = ta.selectionStart;
        ta.value = ta.value.slice(0, p) + tag + ta.value.slice(ta.selectionEnd);
        ta.selectionStart = ta.selectionEnd = p + tag.length;
    } else {
        // 编辑器内联：在光标处插入可拖拽图片节点（顺序即存储顺序）
        const node = noteImgNode(id);
        const sel = getSelection();
        let range = sel && sel.rangeCount ? sel.getRangeAt(0) : null;
        // ⚠️ 真实浏览器下的空行/相邻图场景修正（与 exam.js 同步）：
        // ① 点击「空行」（div 内只有 <br>）时，Chrome 选区常落在该 div 末尾或 <br> 上，
        //    直接 insertNode 会把图插到下一行/块末尾 → 表现为「空行贴不上图」。
        //    归位：锚点在「仅含 <br> 的空块」内时，插入点收到该块开头（即该空行原位）。
        // ② 两张图紧挨时（wrap 间无文本节点）光标无处可落，插入会跑到单侧；
        //    给图片后补零宽文本节点作为「落点」解决。
        if (range && ta.contains(range.startContainer)) {
            const sc = range.startContainer;
            let brHost = (sc.nodeType === 1 && sc.tagName === 'BR') ? sc : null;
            if (!brHost && sc.nodeType === 1) {
                const onlyBr = sc.childNodes.length > 0 && [...sc.childNodes].every(n =>
                    (n.nodeType === 1 && n.tagName === 'BR') || (n.nodeType === 3 && !n.nodeValue.replace(/[\u200B\s]/g, '')));
                if (onlyBr && sc !== ta) brHost = sc;
            }
            if (brHost) {
                try {
                    range.selectNodeContents(brHost);
                    range.collapse(true);
                } catch (e2) { }
            }
        }
        if (range && ta.contains(range.startContainer)) {
            range.deleteContents();
            range.insertNode(node);
            const anchor = document.createTextNode('\u200B');
            node.parentNode.insertBefore(anchor, node.nextSibling);
            try {
                range.setStart(anchor, 1);
                range.collapse(true);
            } catch (e2) { }
            sel.removeAllRanges();
            sel.addRange(range);
        } else {
            ta.appendChild(node);
            ta.appendChild(document.createTextNode('\u200B'));
        }
        // 注意：此处绝不能调 fillExamNoteImgs —— blob 尚未写库，
        // 它会在 300ms 重试失败后 replaceWith('[图片已丢失]')，把节点换成文本导致令牌永久丢失。
    }
    noteInput(ta);   // 触发保存 + 预览（此时值里已含令牌）
    // 异步：压缩 → 写库 → 只回填这一张（写完后必定能取到 blob）
    // 兜底策略：先立即写入【原始图】再后台压缩覆盖——IDB 写原图比压缩快一个量级，
    // 即使贴图后立刻关页/切走导致压缩中断，原图 blob 也已落库，不会变成永久「图片已丢失」。
    const rawPut = examImgPut(id, raw).catch(() => { });   // 原图兜底写入失败不影响后续压缩写入
    const imgTask = compressImage(raw).then(blob => examImgPut(id, blob)).then(() => rawPut).then(() => true)
        // 压缩（或压缩写库）偶发失败：原图兜底已先行落库——保留引用、回填原图继续显示，
        // 绝不摘除节点（摘除 = 文本引用永失 → 用户看到"后贴的图消失"，即使 blob 还在 DB）
        .catch(() => fillOneExamNoteImg(ta, id))
        .then(ok => {
            if (ok) { fillOneExamNoteImg(ta, id); renderNotePreview(ta); }   // 回填这张图 + 刷新预览
            else { alert('图片保存失败'); removeExamNoteImgRef(ta, id); }     // 原图兜底也没有才摘除
        }).then(() => {
            _pendingImgs.delete(id);
        });
    _pendingImgTasks[id] = imgTask;
    imgTask.then(() => { delete _pendingImgTasks[id]; }, () => { delete _pendingImgTasks[id]; });
}

function applyNoteFormat(sec, cmd, val) {
    const ed = sec.querySelector('.q-note-input');
    if (!ed || ed.style.display === 'none' || !ed.isContentEditable) return;
    const sel = getSelection();
    const inEd = !!sel.rangeCount && ed.contains(sel.anchorNode);
    // 'plain'（转普通正文）与 'h1'/'h2'（整行设标题）允许光标直接停在行内，无需先选中文字；
    // 其余行内格式（字色/高亮/粗斜）必须先选中文字，否则无作用对象。
    const needSel = cmd !== 'plain' && cmd !== 'h1' && cmd !== 'h2';
    if (!inEd || (sel.isCollapsed && needSel)) {
        noteHint(ed, '先选中要设置格式的文字'); return;
    }
    ed.focus();
    if (cmd === 'h1' || cmd === 'h2') {
        // 标题用 formatBlock 生成 <h1>/<h2> 标签（须显式禁用 styleWithCSS，否则退化成带样式的 <span>）
        try { document.execCommand('styleWithCSS', false, false); } catch (e) { }
        document.execCommand('formatBlock', false, cmd === 'h1' ? 'H1' : 'H2');
    } else if (cmd === 'plain') {
        // 转为普通正文：先去掉 H1/H2 块级标题，再清除字色/高亮/粗斜等内联格式
        try { document.execCommand('styleWithCSS', false, false); } catch (e) { }
        document.execCommand('formatBlock', false, 'P');
        document.execCommand('removeFormat');
    } else {
        try { document.execCommand('styleWithCSS', false, true); } catch (e) { }
        document.execCommand(cmd, false, val || null);
    }
    noteInput(ed);   // 触发自动保存 + 预览刷新
}
/** 工具条显隐与编辑态同步 */
function syncNoteToolbar(sec) {
    if (!sec) return;
    const ed = sec.querySelector('.q-note-input');
    const bar = sec.querySelector('.q-note-toolbar');
    if (bar) bar.hidden = sec.hidden || !ed || ed.style.display === 'none';
}
// 顶部「💾 保存」按钮（.q-ops 行，位于 笔记 右侧）：定位本题卡的笔记区并保存。
// 仅在编辑态（编辑器可见）生效；只读展示态直接提示先编辑，避免误把空编辑器内容覆盖已存笔记。
async function saveNoteFromOps(btn) {
    const card = btn.closest('.q-card');
    if (!card) return;
    const sec = card.querySelector('.q-note');
    if (!sec) return;
    const ta = sec.querySelector('.q-note-input');
    if (!ta) return;
    if (sec.hidden) { const nb = card.querySelector('button[data-act="note"]'); if (nb) nb.click(); }
    if (ta.style.display === 'none') { noteHint(ta, '请先点 ✏️编辑 再保存', false); return; }
    const eb = sec.querySelector('.q-note-editbtn');
    if (eb) await toggleNoteEdit(eb);   // 编辑态：同一按钮的「💾 保存」动作，保存并收起
    else {
        if (Object.keys(_pendingImgTasks).length) noteHint(ta, '图片保存中…', true);
        await waitPendingImgs();
        // ⚠️ qid 缺失会写出 'examNote-undefined' 脏键（用户导出数据里实测有），落盘前拦掉
        if (ta.dataset.qid) { try { localStorage.setItem('examNote-' + ta.dataset.qid, noteVal(ta)); } catch (e) { } }
    }
}

async function toggleNoteEdit(btn) {
    // 与 exam.js 同款：按钮既可在 note 区内，也可在 q-ops 行（q-card 层）
    const card0 = btn.closest('.q-card');
    const sec = card0 ? card0.querySelector('.q-note') : btn.closest('.q-note');
    if (!sec) return;
    const ta = sec.querySelector('.q-note-input');
    const pv = sec.querySelector('.q-note-preview');
    const editing = ta.style.display !== 'none';
    if (!editing) {
        // 笔记区未展开：自动展开并同步「笔记」按钮高亮（q-ops 编辑按钮可一步进入编辑）
        if (sec.hidden) {
            sec.hidden = false;
            const nb = card0 && card0.querySelector('[data-act="note"]');
            if (nb) nb.classList.add('on');
            fillExamNoteImgs(ta);
            if (pv) fillExamNoteImgs(pv);
        }
        // 进入编辑：同一按钮文字切为「💾 保存」（编辑态保持可见，点击即保存收起）
        btn.textContent = '💾 保存';
        btn.classList.remove('saved');   // 再次编辑恢复按钮常态
        noteHint(btn, '');
        ta.style.display = '';
        // 单按钮方案：编辑态按钮保持可见，文字已切为「💾 保存」，点击即保存收起
        if (!ta.dataset.bind) {
            ta.addEventListener('input', () => noteInput(ta));
            ta.addEventListener('paste', notePasteImg);
            ta.dataset.bind = '1';
        }
        if (ta.tagName !== 'TEXTAREA') {
            setNoteContent(ta, noteGet(ta.dataset.qid));   // 每次进入编辑都从存储重建（文本 + 内联图片）
            fillExamNoteImgs(ta);   // 兜底回填（缩略图条已在 noteToEditor 内回填）
        } else {
            autoResizeNote(ta);
        }
        syncNoteToolbar(sec);
        delete _noteLastRendered[ta.dataset.qid];   // 强制预览重渲为编辑态（带删除 ×）
        renderNotePreview(ta);   // 进入编辑立即刷新下方预览（× 见 mdBlockWithImg editable）
        ta.focus();
        if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);
    } else {
        // 完成：清防抖定时器，立即落盘（有贴图在写库则先等写库完成，防止存下「读不到图」的版本）
        clearTimeout(_noteTimer[ta.dataset.qid]);
        delete _noteTimer[ta.dataset.qid];
        await waitPendingImgs();
        const raw = noteVal(ta);
        if (ta.dataset.qid) { try { localStorage.setItem('examNote-' + ta.dataset.qid, raw); } catch (e) { } }
        const v = raw.trim();
        if (v) {
            btn.textContent = '✏️ 编辑';
            btn.classList.add('saved');   // 保存后淡化按钮
            ta.style.display = 'none';
            syncNoteToolbar(sec);
            if (pv) {
                pv.classList.remove('pv-edit');   // 只读态恢复完整高度
                pv.innerHTML = mdBlockWithImg(raw);
                pv.hidden = false;
                if (raw.includes('$') || raw.includes('\\(') || raw.includes('\\[')) renderMath(pv);
                fillExamNoteImgs(pv);   // 无条件回填 [图:id] 贴图，保证编辑完成后实时显示
            }
            noteHint(btn, '已保存 ✓');
        } else {
            // 清空了内容：收起整节，重置为「空笔记」形态（下次展开直接是输入框 + 保存按钮）
            noteHint(btn, '已删除笔记');
            const opBtn = sec.closest('.q-card')?.querySelector('[data-act="note"]');
            sec.hidden = true;
            if (opBtn) opBtn.classList.remove('has');
            if (pv) { pv.classList.remove('pv-edit'); pv.innerHTML = ''; }   // 清空预览并恢复正常高度
            ta.style.display = '';
            setNoteContent(ta, '');
            // 重置为「空笔记」形态：下次展开直接是输入框 + 💾 保存按钮
            btn.textContent = '💾 保存';
            btn.classList.remove('saved');
        }
    }
}

// ============ 试卷点评（按套卷 id 存 localStorage，纯文本，popover 自动保存） ============

function compressImage(file) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => {
            const scale = Math.min(1, 1200 / Math.max(img.width, img.height));
            const canvas = document.createElement('canvas');
            canvas.width = Math.round(img.width * scale);
            canvas.height = Math.round(img.height * scale);
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#fff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            URL.revokeObjectURL(img.src);
            canvas.toBlob(b => b ? resolve(b) : reject(new Error('图片压缩失败')), 'image/jpeg', 0.85);
        };
        img.onerror = () => reject(new Error('图片读取失败'));
        img.src = URL.createObjectURL(file);
    });
}

// textarea 高度自适应：随内容增高，超过 60% 视口高出现滚动条
function autoResizeNote(el) {
    if (!el) return;
    el.style.height = 'auto';
    const maxH = Math.round(window.innerHeight * 0.6);
    el.style.height = Math.min(el.scrollHeight, maxH) + 'px';
    el.style.overflowY = el.scrollHeight > maxH ? 'auto' : 'hidden';
}

// 笔记保存状态提示（自动保存中… / 已保存 ✓ / 已删除图片 …），2s 后淡出。
// quiet=true（打字过程中的"自动保存中…"）：提示已显示时不重启动画，避免反复闪烁
function noteHint(anchor, msg, quiet) {
    const sec = anchor && anchor.closest && anchor.closest('.q-note');
    const el = sec && sec.querySelector('.q-note-hint');
    if (!el) return;
    if (!msg) { el.textContent = ''; el.classList.remove('show'); return; }
    if (quiet && el.classList.contains('show')) { if (el.textContent !== msg) el.textContent = msg; return; }
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.classList.remove('show'); }, 2000);
}

// 单图删除：删 IndexedDB 图 + 从文本删 [图:id] 占位 + 重渲染预览 + 同步「笔记」标记
function delExamNoteImg(id, btn) {
    const wrap = btn.closest('.q-note');
    if (!wrap) return;
    const ta = wrap.querySelector('.q-note-input');
    const qid = (ta && ta.dataset.qid) || wrap.dataset.qid;
    if (!qid) return;
    let v = ta ? noteVal(ta) : noteGet(qid);
    const re = new RegExp('\\[图:' + id + '\\]', 'g');
    // 只摘掉这一个图片令牌；严禁压缩空格/换行（\s{2,} 会把用户的段落空行和缩进空格全吃掉）
    v = v.replace(re, '');
    try { localStorage.setItem('examNote-' + qid, v); } catch (e) { }
    examImgDel([id]);
    if (ta) { setNoteContent(ta, v); fillExamNoteImgs(ta); }
    const pv = wrap.querySelector('.q-note-preview');
    if (pv && !pv.hidden) {
        pv.innerHTML = mdBlockWithImg(v, true);   // 删除后仍处于编辑态；图片本体显示在编辑器内，预览只留 🖼 标记
        if (v.includes('$') || v.includes('\\(') || v.includes('\\[')) renderMath(pv);
        fillExamNoteImgs(pv);
    }
    _noteLastRendered[qid] = v;   // 同步预览渲染缓存，防下次 renderNotePreview 误跳过
    const opBtn = wrap.closest('.q-card') && wrap.closest('.q-card').querySelector('[data-act="note"]');
    if (opBtn) opBtn.classList.toggle('has', !!v.trim());
    noteHint(btn, '已删除图片');
}

// 切题/卸载前冲刷未落盘的输入，防 <防抖窗口内丢字

function flushNoteSave() {
    for (const qid in _noteTimer) {
        if (_noteTimer[qid]) {
            clearTimeout(_noteTimer[qid]); _noteTimer[qid] = null;
            const ta = document.querySelector('.q-note-input[data-qid="' + qid + '"]');
            if (ta) { try { localStorage.setItem('examNote-' + qid, noteVal(ta)); } catch (e) { } }
        }
    }
}
window.addEventListener('pagehide', flushNoteSave);
async function fillExamNoteImgs(root) {
    if (!root) return;
    // 编辑态（编辑器可见：编辑器 DOM + 下方实时预览）里 img 节点是数据载体——
    // 回填失败绝不能 replaceWith 成文本：换掉 = editorToNote 序列化丢 [图:id] → 孤图清理删 blob → 图片永久丢失。
    // 只读态 img 由存储文本渲染，替换成「图片已丢失」仅影响显示、不伤数据。
    const sec = root.closest && root.closest('.q-note');
    const ed = sec && sec.querySelector('.q-note-input');
    const keepOnFail = !!ed && ed.style.display !== 'none';
    const imgs = root.querySelectorAll('img.exam-note-img[data-img]');
    for (const img of imgs) {
        // 已回填过（blob URL）则跳过，避免重复 createObjectURL 造成内存泄漏
        if (img.src && img.src.startsWith('blob:')) continue;
        let blob = await examImgGet(img.dataset.img);
        if (!blob) {
            // 首屏 / IndexedDB 刚打开时偶发读取失败：短延迟后重试一次（修复「刷新才有」）
            await new Promise(r => setTimeout(r, 300));
            blob = await examImgGet(img.dataset.img);
        }
        if (blob) img.src = URL.createObjectURL(blob);
        else if (_pendingImgTasks[img.dataset.img]) {
            // 图还在压缩/写库：绝不标「图片已丢失」——等写库完成后回填这一张
            const id = img.dataset.img;
            _pendingImgTasks[id].then(() => {
                if (!img.isConnected) return;
                examImgGet(id).then(b => { if (b && img.isConnected) img.src = URL.createObjectURL(b); });
            });
        }
        else if (keepOnFail) {
            // 编辑态取不到 blob（IDB 偶发失败）：保留节点与令牌，仅标记占位——保存不丢，下次进编辑自动重试
            img.classList.add('img-fail');
            img.title = '图片加载失败（保存不会丢失，重新进入编辑可恢复）';
        }
        else img.replaceWith(document.createTextNode('[图片已丢失]'));
    }
}
// 只回填指定一张图（写库完成后调用，此时必定能取到 blob）。
// 与 fillExamNoteImgs 的关键区别：拿不到也绝不 replaceWith('[图片已丢失]')——
// 同步登记的节点在压缩期间本来就没有 blob，误标会把图片节点换成文本、令牌永久丢失。
async function fillOneExamNoteImg(ta, id) {
    if (!ta || !id) return false;
    const img = ta.querySelector('img.exam-note-img[data-img="' + id + '"]');
    if (!img || (img.src && img.src.startsWith('blob:'))) return true;   // 已回填则跳过
    let blob = await examImgGet(id);
    if (!blob) { await new Promise(r => setTimeout(r, 200)); blob = await examImgGet(id); }
    if (blob) { img.src = URL.createObjectURL(blob); return true; }
    return false;
}
// 压缩/写库失败时摘掉这张图的占位节点或文本，避免留下永远取不到 blob 的空图
function removeExamNoteImgRef(ta, id) {
    if (!ta) return;
    if (ta.tagName === 'TEXTAREA') {
        ta.value = ta.value.replace(new RegExp('\\[图:' + id + '\\]', 'g'), '');
    } else {
        const img = ta.querySelector('img.exam-note-img[data-img="' + id + '"]');
        const wrap = img && img.closest('.exam-note-img-wrap');
        if (wrap) wrap.remove(); else if (img) img.remove();
    }
    noteInput(ta);
}

// ============ 配图 / 笔记贴图 单击放大（复用 exam.css 的 .zoom-overlay 遮罩） ============

function examImgPut(id, blob) {
    return examImgDB().then(d => new Promise((res, rej) => {
        const tx = d.transaction('imgs', 'readwrite');
        tx.objectStore('imgs').put(blob, id);
        tx.oncomplete = res; tx.onerror = () => rej(tx.error);
    }));
}

function mdBlockWithImg(s, editable) {
    return mdBlock(s)
        .replace(/\[图:([a-z0-9]+)\]/g,
            (_, id) => editable
                // 编辑态预览：不再渲染图片本体（图片改在编辑器内以缩略图显示，可直接查看/删除/拖拽），
                // 预览区只留一个小标记——避免被大图撑长，预览专注看公式/文字渲染效果
                ? `<span class="exam-note-img-ph" title="图片在编辑器内显示">🖼</span>`
                : `<span class="exam-note-img-wrap"><img class="exam-note-img" data-img="${id}" alt="笔记图片" onclick="zoomAnsImg(this)"></span>`);
}

// ============ 笔记编辑体验增强（移植自 408-quiz 批注，保留 IndexedDB 架构） ============
// 贴图压缩：最长边 1200px 的 JPEG(0.85)，透明底铺白，控制 IndexedDB 体积


let _examImgDB = null;
function examImgDB() {
    if (!_examImgDB) {
        _examImgDB = new Promise((res, rej) => {
            const rq = indexedDB.open('examNoteImg', 1);
            rq.onupgradeneeded = () => rq.result.createObjectStore('imgs');
            rq.onsuccess = () => res(rq.result);
            rq.onerror = () => rej(rq.error);
        });
    }
    return _examImgDB;
}
function examImgGet(id) {
    return examImgDB().then(d => new Promise(res => {
        const rq = d.transaction('imgs').objectStore('imgs').get(id);
        rq.onsuccess = () => res(rq.result || null);
        rq.onerror = () => res(null);
    }));
}
function examImgDel(ids) {
    if (!ids || !ids.length) return Promise.resolve();
    // 防跨笔记丢图：先扫描全部 examNote-* 存储，仍被任何笔记引用的图 id 绝不删——
    // 复制含 [图:id] 的笔记文本到其他题目时两侧共享同一 blob，只在一侧删图/清空会误删另一侧的图。
    return Promise.resolve().then(() => {
        const live = new Set();
        try {
            for (let i = 0; i < localStorage.length; i++) {
                const k = localStorage.key(i);
                if (k && k.indexOf('examNote-') === 0) {
                    const v = localStorage.getItem(k) || '';
                    (v.match(/\[图:([a-z0-9]+)\]/g) || []).forEach(t => { const m = /\[图:([a-z0-9]+)\]/.exec(t); if (m) live.add(m[1]); });
                }
            }
        } catch (e) { }
        return ids.filter(id => !live.has(id));
    }).then(toDel => {
        if (!toDel.length) return Promise.resolve();
        return examImgDB().then(d => new Promise(res => {
            const tx = d.transaction('imgs', 'readwrite');
            toDel.forEach(id => tx.objectStore('imgs').delete(id));
            tx.oncomplete = res; tx.onerror = res;
        }));
    });
}

// ============ 折叠段落（答案/思路/笔记） ============
function toggleQSec(btn, act) {
    const card = btn.closest('.q-card');
    if (!card) return;
    const sec = card.querySelector('.q-sec.q-' + act);
    if (!sec) return;
    const open = sec.hidden;
    sec.hidden = !open;
    btn.classList.toggle('on', open);
    if (open) {                 // 展开时内容刚可见，需补调 KaTeX 渲染 $$ 块
        renderMath(sec);
        if (act === 'note') {
            const ta = sec.querySelector('textarea, .q-note-input[contenteditable]');
            if (ta) {
                fillExamNoteImgs(ta);   // 编辑器内嵌图片回填
                const pv = sec.querySelector('.q-note-preview');
                if (pv) fillExamNoteImgs(pv);
                if (!ta.dataset.bind) {
                    ta.addEventListener('input', () => noteInput(ta));
                    ta.addEventListener('paste', notePasteImg);
                    ta.dataset.bind = '1';
                }
                if (ta.style.display !== 'none') {   // 编辑态才聚焦 + 自动保存；只读预览态不动
                    ta.focus();
                    if (ta.tagName === 'TEXTAREA') autoResizeNote(ta);
                    noteInput(ta);
                }
                syncNoteToolbar(sec);
            }
        }
    }
}

// 一键展开/收起当前列表所有题卡的答案
let allAnsOpen = false;
function toggleAllAnswers(btn) {
    allAnsOpen = !allAnsOpen;
    const root = document.getElementById('catMain');
    if (!root) return;
    root.querySelectorAll('.q-card').forEach(card => {
        const sec = card.querySelector('.q-answer');
        const b = card.querySelector('.q-op[data-act="answer"]');
        if (sec) sec.hidden = !allAnsOpen;
        if (b) {
            b.classList.toggle('on', allAnsOpen);
            b.textContent = allAnsOpen ? '收起答案' : '查看答案';
        }
    });
    // 批量展开后内容刚可见，需补调 KaTeX 渲染 $$ 块
    renderMath(root);
    root.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
    btn.classList.toggle('on', allAnsOpen);
    btn.textContent = allAnsOpen ? '🔽 收起全部答案' : '🔼 展开全部答案';
}

// ============ 数据 ============
let papers = [];
let cats = {};          // { id: {id,name,path,parent} }
let allEntries = [];    // { paper, secTitle, q, catId }
let curCat = null;      // 选中的知识点(L3) id
// 数据源切换：exam = 数二真题（exam.json，2000-2026）；core = 核心题库（core_bank.json，902 题）
// 默认 = 核心题库（用户主要使用核心题库）。
// 2026-10-19：线代臻选题 188 题**全面替代**核心题库的线代部分（原 346 题线代已从 core_bank 移除），
//   不再单独做数据源。⚠️ SRC_MODE_KEY 升版为 catSrcMode2：老键里可能存着 'exam'，
//   直接改默认值对老用户不生效；换键等于把默认值变更推给所有人（只是个 UI 开关偏好，无数据损失）。
const SRC_MODE_KEY = 'catSrcMode2';
const SRC_MODES = ['exam', 'core'];
let srcMode = (function () {
    try {
        const v = localStorage.getItem(SRC_MODE_KEY);
        return SRC_MODES.includes(v) ? v : 'core';
    } catch (e) { return 'core'; }
})();
// 无标记优先：把未收藏、未标「不熟/不会」的题排到最前（刷题时先清「没碰过的」）
const UNMARKED_FIRST_KEY = 'catUnmarkedFirst';
let unmarkedFirst = (function () { try { return localStorage.getItem(UNMARKED_FIRST_KEY) === '1'; } catch (e) { return false; } })();
// 左侧目录栏收起状态（与 exam.html 同款交互，独立键）
const CAT_SIDE_KEY = 'catSideClosed';
let sideClosed = (function () { try { return localStorage.getItem(CAT_SIDE_KEY) === '1'; } catch (e) { return false; } })();
// 年份排序：默认倒序（新题在上面）
const YEAR_SORT_KEY = 'catYearSortDesc';
let yearSortDesc = (function () { try { return localStorage.getItem(YEAR_SORT_KEY) !== '0'; } catch (e) { return true; } })();
let examPapers = [];    // 真题套卷（含后并入的大观园习题卷）
let corePapers = [];    // 核心题库（单「卷」，12 节：高数 6 节 + 线代 6 节=臻选题）
let examStemSet = new Set();   // 真题题干归一化集合（仅真题，不含大观园习题卷）——供大观园题库精确去重

// 题干归一化：只删 LaTeX 结构符号、保留公式内容里的字母数字汉字（与数据侧判重口径一致）。
// 切勿把 $...$ 整体替换成占位符——题干会退化成十几个字，短题干互相假匹配。
function normStem(s) {
    return String(s || '')
        .normalize('NFKC')
        .replace(/\[图:[a-z0-9]+\]/g, '')
        .replace(/\\(begin|end)\{[a-z]*matrix\}/g, ' ')
        .replace(/\\(left|right|big|Big|bigg|Bigg|displaystyle|limits|nolimits)\b/g, ' ')
        .replace(/\\[a-zA-Z]+\s*/g, '')
        .replace(/\\/g, '')
        .replace(/[${}&#_^~|]/g, '')
        .replace(/[^\w\u4e00-\u9fff]/g, '');
}
const SRC_META = {
    exam: { label: '📝 真题', title: '分类题库', sub: '按大观园三级分类（学科 / 章节 / 知识点）· 点击知识点查看跨年真题' },
    core: { label: '📘 核心题库', title: '核心题库', sub: '高数 714 题 + 线代臻选题 188 题（线代部分已由臻选题替代）' },
};
const collapsedSubjects = new Set();   // 折叠的学科
const collapsedChapters = new Set();   // 折叠的章节
// 刷新保持：选中分类 + 树折叠态（localStorage 持久化）
const CAT_STATE_KEY = 'catViewState';
try {
    const st = JSON.parse(localStorage.getItem(CAT_STATE_KEY) || '{}');
    if (st.curCat !== undefined && st.curCat !== null) curCat = st.curCat;
    (st.collapsedSubjects || []).forEach(s => collapsedSubjects.add(s));
    (st.collapsedChapters || []).forEach(c => collapsedChapters.add(c));
} catch (e) { }
function saveCatState() {
    try {
        const catsEl = document.getElementById('catSearch');
        localStorage.setItem(CAT_STATE_KEY, JSON.stringify({
            curCat,
            curDeepCat,          // 细分类选中态（刷新后保留，不再被清掉）
            curDeepSelf,
            collapsedSubjects: [...collapsedSubjects],
            collapsedChapters: [...collapsedChapters],
            search: catSearchKw || '',
            scrollY: window.scrollY || 0,
        }));
    } catch (e) { }
}

// ============ 顶部栏整体折叠（与真题页同款） ============
const TOP_COLLAPSED_KEY = 'examTopCollapsed';
function toggleTopBar(force) {
    const top = document.getElementById('examTop');
    const toggle = document.getElementById('examTopToggle');
    if (!top) return;
    const collapsed = (typeof force === 'boolean') ? force : !top.classList.contains('collapsed');
    top.classList.toggle('collapsed', collapsed);
    if (toggle) toggle.classList.toggle('collapsed', collapsed);
    try { localStorage.setItem(TOP_COLLAPSED_KEY, collapsed ? '1' : '0'); } catch (e) { }
    syncTopH();
}
function restoreTopBar() {
    const collapsed = localStorage.getItem(TOP_COLLAPSED_KEY) === '1';
    toggleTopBar(collapsed);
}
// 同步顶部栏实际高度到 CSS 变量 --exam-top-h（收起=0），驱动侧栏 sticky 偏移
function syncTopH() {
    const top = document.getElementById('examTop');
    const h = (top && !top.classList.contains('collapsed')) ? top.offsetHeight : 0;
    document.documentElement.style.setProperty('--exam-top-h', h + 'px');
}

// 由 section 标题判定题型（比 exam.js 的 no 区间启发式更稳：老卷填空/选择编号不固定）
function secKindLabel(t) {
    if (t.includes('选择题')) return '选择';
    if (t.includes('填空题')) return '填空';
    return '解答';
}

function buildEntries() {
    allEntries = [];
    for (const p of papers) {
        for (const sec of p.sections) {
            for (const q of sec.questions) {
                const cids = q.categoryIds || [];
                for (const cid of cids) {
                    allEntries.push({ paper: p, secTitle: sec.title, q, catId: cid });
                }
            }
        }
    }
    // 核心题库题共享一个空 year 的 paper：补每题年份（从题源提取），
    // 否则年份排序出现 NaN、跨年显示为「跨 1 年」、按年份搜索不命中、复制无年份前缀。
    if (srcMode === 'core') {
        for (const e of allEntries) {
            const m = /((?:19|20)\d\d)/.exec(e.q.source || '');
            if (m) e.paper = Object.assign({}, e.paper, { year: m[1] });
        }
    }
    // 合并大观园数二真题进同一棵分类树（仅真题模式；核心题库模式不混入）
    if (srcMode === 'exam') {
        for (const e of bankItems) {
            for (const cid of e.catIds) {
                allEntries.push({ paper: e.paper, secTitle: '', q: e.q, catId: cid });
            }
        }
        // 线代重点题原本是独立文件 xd_bank.json，2026-10-11 已**物理并入 core_bank.json**
        // （题号 743 起，带 fromX=true / xdNo 原号）：
        //   · core 模式：corePapers 已含全部 1074 题，天然就是完整题库，无需再并入；
        //   · exam 模式：需把 fromX 那批并进来，保证真题模式仍能看到线代重点题（行为不变）。
        // 同题去重（按 qid#catId）：同一道题若在真题/大观园/线代重点题里都出现，
        // qidOf 的重定向会让它们得到同一 qid；只按 catId 粒度去重：同一知识点留先入的那条，
        // 同题挂的**其他**知识点仍保留，知识点覆盖不丢。qidOf 的重定向本身必须保留
        // （收藏/标记主键统一到真题侧）。
        const seenQC = new Set();
        for (const e of allEntries) seenQC.add(qidOf(e.paper.id, e.q.no) + '#' + e.catId);
        for (const e of xdMergedEntries()) {
            const qd = qidOf(e.paper.id, e.q.no);
            for (const cid of e.catIds) {
                const key = qd + '#' + cid;
                if (seenQC.has(key)) continue;
                seenQC.add(key);
                allEntries.push({ paper: e.paper, secTitle: '', q: e.q, catId: cid });
            }
        }
    }
}

/** 线代重点题（并入 core_bank 后带 fromX 标记的题）。
 *  exam 模式并入它们时要补 paper.year —— 这批题的 source（如「2015 数一」）能提年份，
 *  而 corePapers[0] 本身没有 year，不补会导致年份排序 NaN、跨年显示错乱。 */
function xdMergedEntries() {
    const out = [];
    for (const p of (corePapers || [])) {
        for (const s of (p.sections || [])) {
            for (const q of (s.questions || [])) {
                if (!q.fromX) continue;
                const ym = /(\d{4})/.exec(q.source || '');
                out.push({
                    paper: { id: p.id, year: ym ? ym[1] : '', title: '线代重点题' },
                    secTitle: '', q, catIds: q.categoryIds || [],
                });
            }
        }
    }
    return out;
}

// 切换数据源：真题 ⇄ 核心题库（同一棵分类树，选中知识点保持不变）
function applySrcMode(persist) {
    // 降级：核心题库数据未加载成功（fetch 失败等）时不进入 core 模式，避免空白页
    if (srcMode === 'core' && (!corePapers || !corePapers.length)) {
        srcMode = 'exam';
        try { localStorage.setItem(SRC_MODE_KEY, 'exam'); } catch (e) { }
    }
    papers = (srcMode === 'core') ? corePapers : examPapers;
    // 切到核心题库时并入本地增补题（catDeep 未就绪的首次初始化由 init 里那次并入兜底）
    if (srcMode === 'core' && window.CoreExtra && catDeep) {
        try { CoreExtra.mergeInto(corePapers, catDeep); } catch (e) { }
    }
    const meta = SRC_META[srcMode] || SRC_META.exam;
    const btn = document.getElementById('srcToggle');
    if (btn) {
        btn.textContent = meta.label;
        btn.title = srcMode === 'core'
            ? '当前：核心题库（高数 + 线代臻选题）。点击切回数二真题'
            : '当前：数二真题（2000-2026）。点击切换到核心题库';
    }
    const t = document.querySelector('.exam-title');
    if (t) t.textContent = meta.title;
    const sub = document.getElementById('examSub');
    if (sub) { sub.textContent = meta.sub || ''; sub.hidden = !meta.sub; }   // 无副标题时整块隐藏
    if (persist) { try { localStorage.setItem(SRC_MODE_KEY, srcMode); } catch (e) { } }
}

function toggleSrcMode() {
    // 两态循环：exam ⇄ core
    const i = SRC_MODES.indexOf(srcMode);
    srcMode = SRC_MODES[(i + 1) % SRC_MODES.length];
    applySrcMode(true);
    buildEntries();
    buildDeepIndex();   // 题集变了，细分类计数跟着重建
    renderTree();
    renderMain();
    renderNav();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============ 「无标记优先」排序开关 ============
/** 该题是否「无任何标记」：未收藏 且 未标不熟/不会 */
function isUnmarked(e) {
    const qid = qidOf(e.paper.id, e.q.no);
    return !isFav(qid) && !statusOf(qid);
}

/** 掌握度分组（2026-10-14 用户二次定稿）：
 *  不会 0 → 不熟 1 → 仅收藏 2 → 掌握+收藏 3 → 无标记 4 → 掌握无收藏 5
 *  逻辑：只收藏的先刷（还没确认掌握）；显式标掌握的里，收藏的更前；
 *        「掌握但没收藏」垫底（大概率是批量标掌握时没收藏的题，参考价值最低）。 */
function masteryRankOf(qid) {
    const st = statusOf(qid);
    if (st === 'unknown') return 0;
    if (st === 'unfamiliar') return 1;
    if (isFav(qid)) return st === 'mastered' ? 3 : 2;   // 掌握+收藏 3 ｜ 仅收藏 2
    return st === 'mastered' ? 5 : 4;                    // 掌握无收藏 5 ｜ 无标记 4
}

/** 排序比较器
 *  默认：按掌握度分组（不会 → 不熟 → 仅收藏 → 掌握+收藏 → 无标记 → 掌握无收藏），
 *        组内「收藏时间倒序 → 年份（倒序/顺序由开关控制）」
 *  开启「⭕ 无标记」：无标记的排最前，其余仍按掌握度分组
 */
function compareEntries(a, b) {
    const qa = qidOf(a.paper.id, a.q.no);
    const qb = qidOf(b.paper.id, b.q.no);
    if (unmarkedFirst) {
        const ua = isUnmarked(a) ? 0 : 1;
        const ub = isUnmarked(b) ? 0 : 1;
        if (ua !== ub) return ua - ub;
        if (ua === 1) {                    // 两者都有标记 → 再按掌握度
            const ra = masteryRankOf(qa), rb = masteryRankOf(qb);
            if (ra !== rb) return ra - rb;
        }
    } else {
        const ra = masteryRankOf(qa), rb = masteryRankOf(qb);
        if (ra !== rb) return ra - rb;
    }
    const ta = favTime(qa);
    const tb = favTime(qb);
    if (ta && tb) return tb - ta;
    // 年份排序（兜底 0：无年份的补充题排到有年份真题之后，避免 NaN 失序淹没真题）
    const ya = parseInt(a.paper.year, 10) || 0;
    const yb = parseInt(b.paper.year, 10) || 0;
    if (yb !== ya) {
        return yearSortDesc ? (yb - ya) : (ya - yb);
    }
    return 0;
}

function syncYearSortBtn() {
    const b = document.getElementById('yearSortBtn');
    if (!b) return;
    b.classList.toggle('on', !yearSortDesc); // 顺序时激活态高亮
    b.setAttribute('aria-pressed', yearSortDesc ? 'false' : 'true');
    b.textContent = yearSortDesc ? '⬇️ 年份' : '⬆️ 年份';
    b.title = yearSortDesc
        ? '当前：年份倒序（最新年份在上面）。点击切换为顺序（老题在上面）'
        : '当前：年份顺序（老题在上面）。点击切换为倒序（新题在上面）';
}

function toggleYearSort() {
    yearSortDesc = !yearSortDesc;
    try { localStorage.setItem(YEAR_SORT_KEY, yearSortDesc ? '1' : '0'); } catch (e) { }
    syncYearSortBtn();
    renderMain();
    renderNav();
}

// ============ 左侧目录栏收起/展开（与 exam.html 同款交互） ============
function toggleSide() {
    sideClosed = !sideClosed;
    try { localStorage.setItem(CAT_SIDE_KEY, sideClosed ? '1' : '0'); } catch (e) { }
    applySideState();
}
function applySideState() {
    const wrap = document.querySelector('.exam-wrap');
    const btn = document.getElementById('sideToggle');
    if (wrap) wrap.classList.toggle('side-closed', sideClosed);
    if (btn) btn.textContent = sideClosed ? '▶' : '◀';
}

function syncUnmarkedFirstBtn() {
    const b = document.getElementById('unmarkedFirst');
    if (!b) return;
    b.classList.toggle('on', unmarkedFirst);
    b.setAttribute('aria-pressed', unmarkedFirst ? 'true' : 'false');
    b.title = unmarkedFirst
        ? '当前：无标记题目已提前（再点恢复「收藏时间/年份」原排序）'
        : '把未做任何标记（未收藏、未标不熟/不会）的题目排到最前';
}

function toggleUnmarkedFirst() {
    unmarkedFirst = !unmarkedFirst;
    try { localStorage.setItem(UNMARKED_FIRST_KEY, unmarkedFirst ? '1' : '0'); } catch (e) { }
    syncUnmarkedFirstBtn();
    renderMain();
    renderNav();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function activeEntries() {
    // 筛选并集：收藏 / 不熟 / 不会 分别勾选；全部未选 → 不过滤（显示全部真题）
    if (!markSel.fav && !markSel.unfamiliar && !markSel.unknown) return allEntries;
    const st = statusGet();
    return allEntries.filter(e => {
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null;
        const f = markSel.fav && isFav(qid);
        const u = markSel.unfamiliar && s === 'unfamiliar';
        const k = markSel.unknown && s === 'unknown';
        return f || u || k;
    });
}

// 清洗标签：去 LaTeX $...$、去空白、截断（用于分类树显示）
function cleanLabel(s) {
    return (s || '').replace(/\$[^$]*\$/g, '').replace(/\$/g, '').replace(/\s+/g, '').slice(0, 22);
}

// 按「学科 → 章节 → 知识点(L3)」三级聚合；只保留有题数的节点；subject 固定序，chapter/leaf 按题数降序
function buildTree(entries) {
    const byCat = {};
    for (const e of entries) byCat[e.catId] = (byCat[e.catId] || 0) + 1;
    const subjMap = {};   // 学科名 -> { chapters: { chId: {id,name,display,count,leaves:[]} } }
    for (const id in cats) {
        const c = cats[id];
        if (c.level !== 2) continue;                 // 仅处理 L3 知识点叶子
        const ch = cats[String(c.parentId)];
        if (!ch || ch.level !== 1) continue;
        const subj = cats[String(ch.parentId)];
        if (!subj) continue;
        const cnt = byCat[c.id] || 0;
        if (cnt <= 0) continue;
        if (!subjMap[subj.name]) subjMap[subj.name] = { id: subj.id, name: subj.name, display: subj.display, chapters: {} };
        const cm = subjMap[subj.name].chapters;
        if (!cm[ch.id]) cm[ch.id] = { id: ch.id, name: ch.name, display: ch.display, count: 0, leaves: [] };
        cm[ch.id].count += cnt;
        cm[ch.id].leaves.push({ id: c.id, name: c.name, display: c.display, count: cnt });
    }
    const order = ['高等数学', '线性代数', '概率统计'];
    const laChapterOrder = ['行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型'];
    const subs = Object.keys(subjMap)
        .filter(s => Object.keys(subjMap[s].chapters).length)
        .sort((a, b) => { const ia = order.indexOf(a), ib = order.indexOf(b); return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib); });
    return subs.map(s => {
        let chapters = Object.values(subjMap[s].chapters);
        if (s === '线性代数') {
            // 线代章节按用户指定固定顺序：行列式 -> 矩阵 -> 向量 -> 线性方程组 -> 特征值与特征向量 -> 二次型
            chapters.sort((a, b) => {
                const ia = laChapterOrder.indexOf(a.name);
                const ib = laChapterOrder.indexOf(b.name);
                return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
            });
        } else {
            chapters.sort((a, b) => b.count - a.count);
        }
        chapters.forEach(ch => ch.leaves.sort((a, b) => b.count - a.count));
        return { subject: s, id: subjMap[s].id, display: subjMap[s].display || s, chapters };
    });
}

// ============ 节点聚合：自身 + 全部后代（点任意层级都能直接看到其下所有题） ============
function catSelfAndDescendants(cid) {
    const out = new Set([String(cid)]);
    const stack = [String(cid)];
    while (stack.length) {
        const cur = stack.pop();
        for (const k in cats) {
            const c = cats[k];
            if (String(c.parentId) === cur && !out.has(k)) { out.add(k); stack.push(k); }
        }
    }
    return out;
}
/** 当前选中的分类集合（缓存，renderMain/renderNav 共用） */
function curCatSet() {
    return curCat == null ? null : catSelfAndDescendants(curCat);
}

// ============ 渲染：三级分类树 ============
function renderTree() {
    const entries = activeEntries();
    const el = document.getElementById('catTree');
    // 触摸设备（无 hover）不挂悬停浮层：手机上 tap 会先触发 mouseenter，
    // 浮层弹出后盖住节点，导致「分支点不动」。触屏一律直接走 onclick。
    // 窄屏也视为触屏（部分安卓浏览器会误报 hover:hover），避免浮层盖住节点导致点不动
    const canHover = (function () {
        try { return !window.matchMedia('(hover: none)').matches && window.innerWidth > 900; }
        catch (e) { return window.innerWidth > 900; }
    })();
    if (!entries.length) {
        el.innerHTML = '<div class="empty-tip">当前筛选条件下没有题目。到真题页点 ☆ 收藏，或点题右侧「不熟/不会」打标记后，这里会按章节汇总。</div>';
        return;
    }
    const tree = buildTree(entries);
    el.innerHTML = tree.map(s => {
        const open = !collapsedSubjects.has(s.subject);
        const total = s.chapters.reduce((a, c) => a + c.count, 0);
        return `<div class="paper-group">
            <div class="paper-group-head${String(curCat) === String(s.id) ? ' on' : ''}">
                <span class="paper-group-arrow" onclick="toggleSubject('${s.subject.replace(/'/g, "\\'")}')" title="展开/收起本学科">${open ? '▼' : '▶'}</span>
                <span class="paper-group-name" onclick="selectCat(${s.id})" title="查看本学科全部题目">${s.subject}</span>
                <span class="paper-group-count" onclick="selectCat(${s.id})">${total}</span>
            </div>
            <div class="paper-group-body" style="display:${open ? 'block' : 'none'}">
                ${s.chapters.map(ch => {
                    const copen = !collapsedChapters.has(ch.id);
                    const leafOn = String(curCat) === String(ch.id);
                    const chHover = (canHover && deepRootOfChapter(ch.id)) ? ` onmouseenter="onChapterNodeEnter(this, ${ch.id})" onmouseleave="scheduleHideDeepFly()"` : '';
                    return `<div class="cat-chapter">
                        <div class="cat-chapter-head${leafOn ? ' on' : ''}"${chHover} title="${ch.display || ch.name}${deepRootOfChapter(ch.id) ? '（悬停查看下分支）' : ''}">
                            <span class="cat-chapter-arrow" onclick="toggleChapter(${ch.id})" title="展开/收起本章">${copen ? '▾' : '▸'}</span>
                            <span class="cat-chapter-name" onclick="selectCat(${ch.id})" title="查看本章全部题目（含各知识点）">${ch.display || ch.name}</span>
                            <span class="cat-count" onclick="selectCat(${ch.id})">${ch.count}</span>
                        </div>
                        <div class="cat-chapter-body" style="display:${copen ? 'block' : 'none'}">
                            ${ch.leaves.map(l => `<button class="cat-leaf${String(curCat) === String(l.id) ? ' on' : ''}" data-cat="${l.id}" onclick="selectCat(${l.id})"${canHover ? ` onmouseenter="onCatNodeEnter(this, ${l.id})" onmouseleave="scheduleHideDeepFly()"` : ''} title="${l.name}${(canHover && deepRootOfCat(l.id)) ? '（悬停查看细分支）' : ''}">
                                <span class="cat-leaf-name">${l.display || l.name}</span>
                                <span class="cat-count">${l.count}</span>
                            </button>`).join('')}
                        </div>
                    </div>`;
                }).join('')}
            </div>
        </div>`;
    }).join('');
}

function toggleSubject(subj) {
    if (collapsedSubjects.has(subj)) collapsedSubjects.delete(subj);
    else collapsedSubjects.add(subj);
    saveCatState();
    renderTree();
}

function toggleChapter(id) {
    if (collapsedChapters.has(id)) collapsedChapters.delete(id);
    else collapsedChapters.add(id);
    saveCatState();
    renderTree();
}

function selectCat(id) {
    curCat = id;
    curDeepCat = null;   // 切知识点时退出细分类筛选
    curDeepSelf = false;
    hideDeepFlyNow();
    // 点上层节点（学科/章节）时自动展开，便于看到其子节点
    const node = cats[String(id)];
    if (node && node.level < 2) {
        if (node.level === 1) collapsedChapters.delete(Number(id));
        if (node.level === 0) collapsedSubjects.delete(node.name);
    }
    // 点知识点（分类树 / 掌握地图跳转）时清掉搜索词：否则 renderMain 被搜索视图挡住，
    // 出现「搜索态下点分类树/掌握地图色块无响应」。
    if (catSearchKw) {
        catSearchKw = '';
        const inp = document.getElementById('catSearch');
        if (inp) inp.value = '';
        const clr = document.getElementById('catSearchClear');
        if (clr) clr.style.display = 'none';
    }
    saveCatState();
    renderTree();
    renderMain();
}

/** 搜索结果「进入此分支」跳转：同页直达该知识点（清搜索词、展开分类树使其可见） */
function jumpBranch(cid) {
    collapsedSubjects.clear();   // 展开全部，保证目标分支在左侧树中可见并高亮
    collapsedChapters.clear();
    selectCat(cid);
    // 目录若处于收起态则自动展开，便于用户看到选中的分支
    if (sideClosed) { sideClosed = false; try { localStorage.setItem(CAT_SIDE_KEY, '0'); } catch (e) { } applySideState(); }
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============ 渲染：题目卡片 ============
function catCard(paper, secTitle, q) {
    const qid = qidOf(paper.id, q.no);
    const fav = isFav(qid);
    const st = statusOf(qid);
    const kindLabel = (q.options && q.options.length) || q.type === 'choice' ? '选择'
        : q.type === 'blank' ? '填空' : q.type === 'calc' ? '解答'
        : q.type === 'proof' ? '证明' : secKindLabel(secTitle);
    const stem = mdBlock(q.stem || '');
    const figHtml = q.img
        ? `<img class="q-fig-img" src="${q.img}" alt="题${q.no}配图" loading="lazy" onclick="zoomAnsImg(this)">` +
          (q.img2 ? `<img class="q-fig-img" src="${q.img2}" alt="题${q.no}配图2" loading="lazy" onclick="zoomAnsImg(this)">` : '')
        : '';
    const options = (q.options && q.options.length)
        ? `<div class="q-options">${q.options.map((o, i) => `<div class="q-opt">${!q.options.some(x => /^\([A-D]\)/.test(x)) ? `<span class="opt-label">${'ABCD'[i]}</span>` : ''}${mdInline(o)}</div>`).join('')}</div>`
        : '';
    const ideaHtml = q.idea ? `<div class="q-sec q-idea" data-copy-md="${copyMdAttr(q.idea)}" hidden>${mdBlock(q.idea)}</div>` : '';
    const ideaBtn = q.idea ? `<button class="q-op" data-act="idea" onclick="toggleQSec(this,'idea')">思路</button>` : '';
    // 📌 点睛：本题专属 公式/易错/技巧/注意（数据来自 exam.json 的 q.tips，与真题页同款）
    const TIP_META = [
        ['gs', '📌 公式', 'tip-gs'],
        ['yc', '⚠️ 易错', 'tip-yc'],
        ['jq', '💡 技巧', 'tip-jq'],
        ['zy', '🔍 注意', 'tip-zy'],
    ];
    let tipsHtml = '', tipsBtn = '';
    if (q.tips && TIP_META.some(([k]) => q.tips[k])) {
        const secs = TIP_META.filter(([k]) => q.tips[k])
            .map(([k, label, cls]) => `<div class="q-tip-sec ${cls}" data-copy-md="${copyMdAttr(q.tips[k])}" data-copy-key="${k}"><div class="q-tip-label">${label}</div><div class="q-tip-body">${mdBlock(q.tips[k])}</div></div>`)
            .join('');
        tipsHtml = `<div class="q-sec q-tips" hidden>${secs}</div>`;
        tipsBtn = `<button class="q-op q-tips-btn" data-act="tips" onclick="toggleQSec(this,'tips')" title="本题专属公式/易错点/技巧/注意">📌 点睛</button>`;
    }
    const note = noteGet(qid);
    const hasNote = !!note.trim();
    const hasImg = /\[图:[a-z0-9]+\]/.test(note);
    // 笔记格式工具条：字色 + 高亮 + 清除（与真题页同款）
    const NOTE_COLORS = ['#e03131', '#e8590c', '#2f9e44', '#1971c2', '#9c36b5', '#495057'];
    const NOTE_HLS = ['#fff3bf', '#d3f9d8', '#d0ebff', '#ffe3e3', '#ffdcc4'];
    const NOTE_TOOLBAR = `<div class="q-note-toolbar" hidden>
        <span class="q-nt-lab">字色</span>
        ${NOTE_COLORS.map(c => `<button type="button" class="q-nt-c" style="color:${c}" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'foreColor','${c}')" title="字色 ${c}">A</button>`).join('')}
        <span class="q-nt-sep"></span>
        <span class="q-nt-lab">高亮</span>
        ${NOTE_HLS.map(c => `<button type="button" class="q-nt-h" style="background:${c}" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'hiliteColor','${c}')" title="高亮 ${c}"></button>`).join('')}
        <span class="q-nt-sep"></span>
        <button type="button" class="q-nt-b" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'bold')" title="加粗 (Ctrl+B)"><b>B</b></button>
        <button type="button" class="q-nt-i" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'italic')" title="斜体 (Ctrl+I)"><i>I</i></button>
        <button type="button" class="q-nt-h1" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'h1')" title="大标题">H1</button>
        <button type="button" class="q-nt-h2" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'h2')" title="中标题">H2</button>
        <span class="q-nt-sep"></span>
        <button type="button" class="q-nt-x" onmousedown="event.preventDefault()" onclick="applyNoteFormat(this.closest('.q-note'),'plain')" title="转为普通正文（去掉标题/字色/高亮）">正文</button>
    </div>`;
    const editorHtml = `<div class="q-note-input" contenteditable="true" spellcheck="false" data-qid="${qid}" data-placeholder="记下你的思路、易错点、类比题…（Ctrl+V 可贴图；选中文字可上色/高亮；用 $...$ 写公式会自动渲染）"></div>`;
    // 套卷形式：note 区内不放编辑/保存按钮，统一由 q-ops 的 ✏️编辑 按钮承担（与真题页同款）；
    // 输入框初始隐藏，由编辑按钮进入编辑态（与 exam.js noteHtml 一致）
    const noteHtml = hasNote
        ? `<div class="q-sec q-note${hasImg ? ' has-img' : ''}" data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml.replace('<div class=', '<div style="display:none" class=')}
            <div class="q-note-preview">${mdBlockWithImg(note)}</div>
            <div class="q-note-hint"></div>
        </div>`
        : `<div class="q-sec q-note" hidden data-qid="${qid}">
            ${NOTE_TOOLBAR}
            ${editorHtml.replace('<div class=', '<div style="display:none" class=')}
            <div class="q-note-preview" hidden></div>
            <div class="q-note-hint"></div>
        </div>`;
    const noteBtn = hasNote ? `<button class="q-op has" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>`
        : `<button class="q-op" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>`;
    const paperLink = 'exam.html?paper=' + encodeURIComponent(paper.id);
    // 核心题库/线代补充题：不显示「年份链接」（非套卷），改显示原真题题源标签
    const yearHtml = paper.id === 'core' || paper.id === 'xd' || paper.id === 'DG900JXB'
        ? (q.source ? `<span class="q-year"><span class="q-year-tag" title="原书题源">${mdInline(q.source)}</span></span>` : '')
        : paper.id === 'bank'
        ? (paper.year ? `<span class="q-year"><span class="q-year-tag">${paper.year}年</span></span>` : '')
        : `<span class="q-year"><a href="${paperLink}" title="在真题页打开此套卷">${paper.year}年</a></span>`;
    // 「收到核心题库」：非核心题库来源的题可一键收进核心题库（本地增补层）
    const isCoreSrc = paper.id === 'core';
    const addedCore = !isCoreSrc && window.CoreExtra && CoreExtra.has(q);
    const addCoreBtn = isCoreSrc ? '' :
        `<button class="q-op q-add-core${addedCore ? ' has' : ''}" onclick="coreAddFromCard(this)" title="收进核心题库（本机保存；首页可导出）">${addedCore ? '✅ 已收进核心题库' : '📥 收到核心题库'}</button>`;
    return `<div class="q-card" id="q-${qid}" data-qno="${q.no}">
        <div class="q-head">
            <span class="q-no">${q.no}</span>
            <span class="q-kind">${kindLabel}</span>
            ${q.key ? '<span class="q-mark-chip m-key" title="大观园题库标注的重点题（多本书重复收录，出处见题源）">重点</span>' : ''}
            ${fav ? `<span class="q-mark-chip m-fav" title="已收藏">📥</span>` : ''}
            ${st === 'mastered' ? '<span class="q-mark-chip m-mst" title="已掌握">🟢 掌握</span>' : ''}
            ${st === 'unfamiliar' ? '<span class="q-mark-chip m-unfam" title="不熟">🟡 不熟</span>' : ''}
            ${st === 'unknown' ? '<span class="q-mark-chip m-unk" title="不会">🔴 不会</span>' : ''}
            ${fav && favTime(qid) ? `<span class="q-fav-date" title="收藏于 ${fmtFavTime(favTime(qid))}">${fmtFavShort(favTime(qid))}</span>` : ''}
            ${yearHtml}
            <button class="q-fav${fav ? ' on' : ''}" onclick="toggleFav('${qid}', this)" title="${fav ? (favTime(qid) ? '收藏于 ' + fmtFavTime(favTime(qid)) : '已收藏') : '收藏此题'}">${fav ? '⭐' : '☆'}</button>
            <button class="q-copy-latex" onclick="copyCatQLatex(this)" title="复制本题 LaTeX 源码（题干+选项+答案，含 $...$ 原始命令）">📋 LaTeX</button>
        </div>
        <div class="q-status-rail" data-qid="${qid}">
            <button class="q-st-btn q-st-mst${st === 'mastered' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','mastered')" title="标记为「掌握」（绿色；再点取消）">掌握</button>
            <button class="q-st-btn q-st-unfam${st === 'unfamiliar' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unfamiliar')" title="标记为「不熟」（黄色；再点取消）">不熟</button>
            <button class="q-st-btn q-st-unk${st === 'unknown' ? ' on' : ''}" onclick="toggleQStatus(this,'${qid}','unknown')" title="标记为「不会」（红色；再点取消）">不会</button>
        </div>
        <div class="q-body">${stem}${figHtml}${options}</div>
        <div class="q-ops">
            <button class="q-op" data-act="answer" onclick="toggleQSec(this,'answer')">查看答案</button>
            ${ideaBtn}
            ${tipsBtn}
            <button class="q-op${hasNote ? ' has' : ''}" data-act="note" onclick="toggleQSec(this,'note')">笔记</button>
            <button class="q-op q-note-editbtn${hasNote ? ' saved' : ''}" onclick="toggleNoteEdit(this)" title="编辑笔记（编辑中点击保存）">✏️ 编辑</button>
            ${addCoreBtn}
        </div>
        ${ideaHtml}${tipsHtml}${noteHtml}
        <div class="q-sec q-answer" data-copy-md="${copyMdAttr(q.answer || '')}" data-copy-key="answer" hidden><div class="q-answer-body">${mdBlock(q.answer || '')}</div></div>
    </div>`;
}


// ===== 「收到核心题库」：把当前卡片的题收进核心题库本地增补层 =====
function catToast(msg) {
    let el = document.getElementById('catToast');
    if (!el) {
        el = document.createElement('div');
        el.id = 'catToast';
        el.setAttribute('style', 'position:fixed;left:50%;bottom:72px;transform:translateX(-50%);z-index:9999;' +
            'background:var(--accent,#2b8a6b);color:#fff;padding:9px 16px;border-radius:8px;font-size:14px;' +
            'box-shadow:0 3px 12px rgba(0,0,0,.28);max-width:80vw;text-align:center;transition:opacity .25s');
        document.body.appendChild(el);
    }
    el.textContent = msg;
    el.style.opacity = '1';
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.style.opacity = '0'; }, 2600);
}
function coreAddFromCard(btn) {
    if (!window.CoreExtra) { catToast('核心增补模块未加载'); return; }
    const card = btn.closest('.q-card');
    if (!card) return;
    const qid = card.id.replace(/^q-/, '');
    let ent = allEntries.find(e => qidOf(e.paper.id, e.q.no) === qid);
    if (!ent) {   // 兜底：qid 重定向等情况下按题号再找一次
        const qno = card.dataset.qno;
        ent = allEntries.find(e => String(e.q.no) === String(qno));
    }
    if (!ent) { catToast('未找到题目数据'); return; }
    const r = CoreExtra.add(ent.q, { paperId: ent.paper.id, srcNo: ent.q.no });
    if (r.ok) {
        btn.textContent = '✅ 已收进核心题库';
        btn.classList.add('has');
        catToast('已收进核心题库（本机）· 新题号 ' + r.no + '，切到「核心题库」即可看到');
    } else {
        catToast(r.msg || '添加失败');
    }
}

// ============ 主列表分批渲染（移动端防卡死） ============
// 整章可达 300+ 题，一次性 innerHTML + KaTeX 会让手机卡死数秒。
// 首屏只渲染 CAT_PAGE 题，滚到底自动追加；KaTeX / 笔记贴图只处理新增批次。
const CAT_PAGE = 24;
let _catEntries = [], _catShown = 0, _catCardFn = null, _catIO = null;

function catBatchAfterRender(batch) {
    renderMath(batch);
    batch.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}
function catUpdateMore() {
    const btn = document.getElementById('catMoreBtn');
    const tip = document.getElementById('catMoreTip');
    const rest = _catEntries.length - _catShown;
    if (btn) {
        btn.style.display = rest > 0 ? '' : 'none';
        btn.textContent = '⬇️ 加载更多题（还剩 ' + rest + ' 题）';
    }
    if (tip) tip.textContent = rest > 0 ? ('已显示 ' + _catShown + ' / ' + _catEntries.length + ' 题')
        : ('已全部加载 ' + _catEntries.length + ' 题');
}
function catAppendMore() {
    const wrap = document.getElementById('catList');
    if (!wrap) return;
    const slice = _catEntries.slice(_catShown, _catShown + CAT_PAGE);
    if (!slice.length) { catUpdateMore(); return; }
    const batch = document.createElement('div');
    batch.className = 'cat-batch';
    batch.innerHTML = slice.map((e, i) => _catCardFn(e, _catShown + i)).join('');
    wrap.appendChild(batch);
    _catShown += slice.length;
    catBatchAfterRender(batch);
    catUpdateMore();
}
function catSetupAutoMore() {
    if (_catIO) { _catIO.disconnect(); _catIO = null; }
    const t = document.getElementById('catBottom');
    if (!t || typeof IntersectionObserver === 'undefined') return;
    _catIO = new IntersectionObserver(es => { if (es.some(x => x.isIntersecting)) catAppendMore(); }, { rootMargin: '900px' });
    _catIO.observe(t);
}
/** 开始渲染一批列表：headHtml 为卷首，cardFn(entry, index) 返回单题 HTML */
function catStartList(entries, headHtml, cardFn) {
    const el = document.getElementById('catMain');
    _catEntries = entries || [];
    _catShown = 0;
    _catCardFn = cardFn || (e => catCard(e.paper, e.secTitle, e.q));
    const more = _catEntries.length > CAT_PAGE
        ? `<div class="rv-bottom" id="catBottom"><button class="exam-btn" id="catMoreBtn" onclick="catAppendMore()">⬇️ 加载更多题</button><span class="rv-more-tip" id="catMoreTip"></span></div>`
        : '';
    el.innerHTML = headHtml + '<div id="catList"></div>' + more;
    catAppendMore();
    catSetupAutoMore();
}

// 状态按钮点击：互斥切换不熟/不会，刷新按钮态 + 若正在搜索结果中刷新列表
function toggleQStatus(btn, qid, v) {
    const nv = toggleStatus(qid, v);
    const card = btn.closest('.q-card');
    if (card) {
        card.querySelectorAll('.q-st-btn').forEach(b => b.classList.remove('on'));
        if (nv) {
            const sel = nv === 'unknown' ? '.q-st-unk' : nv === 'mastered' ? '.q-st-mst' : '.q-st-unfam';
            const b = card.querySelector(sel);
            if (b) b.classList.add('on');
        }
        syncStatusChip(card, qid);   // 头部 chip（🟢掌握/🟡不熟/🔴不会）实时同步
        // 若当前在"不熟/不会"筛选下被取消标记，题目应从列表消失
        if (markSel.unfamiliar && nv !== 'unfamiliar' && !markSel.unknown) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
        if (markSel.unknown && nv !== 'unknown' && !markSel.unfamiliar) { const cc = card; setTimeout(() => { if (cc && cc.isConnected) renderMain(); }, 50); }
        renderNav();   // 题号球标记实时同步（🟢掌握/🟡不熟/🔴不会）
    }
}
/** 状态 chip 实时同步（点标记按钮即刷新头部徽标，不必整卡重渲染） */
function syncStatusChip(card, qid) {
    if (!card) return;
    card.querySelectorAll('.q-mark-chip.m-mst,.q-mark-chip.m-unfam,.q-mark-chip.m-unk').forEach(x => x.remove());
    const st = statusOf(qid);
    let html = '';
    if (st === 'mastered') html = '<span class="q-mark-chip m-mst" title="已掌握">🟢 掌握</span>';
    else if (st === 'unfamiliar') html = '<span class="q-mark-chip m-unfam" title="不熟">🟡 不熟</span>';
    else if (st === 'unknown') html = '<span class="q-mark-chip m-unk" title="不会">🔴 不会</span>';
    if (!html) return;
    const head = card.querySelector('.q-head');
    if (!head) return;
    const anchor = head.querySelector('.q-fav-date, .q-year, .q-fav, .q-copy-latex');
    if (anchor) anchor.insertAdjacentHTML('beforebegin', html);
    else head.insertAdjacentHTML('beforeend', html);
}
// 复制题文本到剪贴板（clipboard API，非安全上下文降级 execCommand）
function copyTextToClipboard(text, btn, okMsg) {
    const flash = () => {
        const old = btn.textContent;
        btn.textContent = okMsg || '已复制 ✓';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = old; btn.classList.remove('copied'); }, 1500);
    };
    const fallback = () => {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); flash(); } catch (e) { btn.textContent = '复制失败'; }
        ta.remove();
    };
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(flash).catch(fallback);
    } else fallback();
}
// 复制本题 LaTeX 源文（题干 + 选项 + 答案，保留 $...$ 原始命令）
function copyCatQLatex(btn) {
    const card = btn.closest('.q-card');
    if (!card) return;
    const qid = card.id.replace(/^q-/, '');
    let hit = null, paper = null;
    for (const e of allEntries) {
        if (qidOf(e.paper.id, e.q.no) === qid) { hit = e.q; paper = e.paper; break; }
    }
    if (!hit) return;
    let text = (paper && paper.year ? paper.year + '年 题' + hit.no + '\n' : '') + (hit.stem || '');
    if (hit.options && hit.options.length) text += '\n' + hit.options.join('\n');
    if (hit.answer) text += '\n' + hit.answer.replace(/^(【答案】)+/, '【答案】');   // 数据自带【答案】前缀，归一防重复
    copyTextToClipboard(text, btn, '已复制 ✓');
}

// ============ 复测页（category.html?review=1）：我的收藏 / 掌握 / 不熟 / 不会 题汇总 ============
const REVIEW_MODE = new URLSearchParams(location.search).get('review') === '1';
let rvFilter = 'all';   // all | fav | mastered | unfamiliar | unknown

/** 顶栏「🔁 复测」→ 新标签页打开复测视图 */
function openReviewPage() {
    // 顶栏入口已改为原生 <a target="_blank">（避免弹窗拦截）；此处保留兼容调用
    window.open('category.html?review=1', '_blank', 'noopener');
}

/** 复测模式初始化：隐藏左树与分类浏览专属控件，改标题 */
function applyReviewMode() {
    if (!REVIEW_MODE) return;
    document.body.classList.add('review-mode');
    const t = document.querySelector('.exam-title');
    if (t) t.textContent = '🔁 复测';
    document.title = '🔁 复测 · 我的标记题';   // 标签页标题（否则仍是「分类题库」，易误以为跳回了分类）
    const sub = document.getElementById('examSub');
    if (sub) {
        sub.textContent = '我的收藏 / 掌握 / 不熟 / 不会 题汇总 · 附带原有笔记 · 与真题页和分类页实时同步';
        sub.hidden = false;
    }
    ['srcToggle', 'unmarkedFirst', 'yearSortBtn'].forEach(id => {
        const b = document.getElementById(id);
        if (b) b.style.display = 'none';
    });
    const marks = document.querySelector('.cat-marks');
    if (marks) marks.style.display = 'none';   // 复测筛选在列表顶部单独渲染
}

function setRvFilter(f) {
    rvFilter = f;
    document.querySelectorAll('.rv-filter .cat-mark').forEach(b => b.classList.toggle('on', b.dataset.rv === f));
    renderReview();
}

/** 复测列表：所有带收藏或状态标记的题（同题去重），附笔记 */
// 复测列表分批渲染：首批 RV_PAGE 题，滚到底部自动追加（并保留「加载更多」按钮兜底）
const RV_PAGE = 40;
let rvShown = RV_PAGE, rvList = [], rvIO = null;

/** 复测用：合并全部来源的题目（真题卷 + 核心题库 + 线代重点题 + 大观园真题），
    不受当前「数二真题 / 核心题库」切换影响，保证所有标记题都能出现在复测页 */
function allEntriesAllSources() {
    const out = [];
    const pushPapers = (papers) => {
        for (const p of (papers || [])) {
            for (const sec of (p.sections || [])) {
                for (const q of (sec.questions || [])) out.push({ paper: p, secTitle: sec.title, q });
            }
        }
    };
    pushPapers(examPapers);
    pushPapers(corePapers);          // 已含并入的线代重点题（fromX）与线代臻选题（替代原 346 题线代）
    for (const list of [bankItems]) {
        for (const e of (list || [])) out.push({ paper: e.paper, secTitle: e.secTitle || '', q: e.q });
    }
    return out;
}

function rvCardHtml(r) { return catCard(r.paper, r.secTitle, r.q); }

/** 只对新增批次做收尾：KaTeX、笔记自动展开、贴图回填（避免整页重算） */
function rvAfterRender(batch) {
    renderMath(batch);
    batch.querySelectorAll('.q-card').forEach(card => {
        const qid = card.id.replace(/^q-/, '');
        if ((noteGet(qid) || '').trim()) {
            const nb = card.querySelector('[data-act="note"]');
            if (nb && !nb.classList.contains('on')) nb.click();
        }
    });
    batch.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

function rvUpdateMore() {
    const btn = document.getElementById('rvMoreBtn');
    const tip = document.getElementById('rvMoreTip');
    const rest = rvList.length - rvShown;
    if (btn) {
        btn.style.display = rest > 0 ? '' : 'none';
        btn.textContent = '⬇️ 加载更多题（还剩 ' + rest + ' 题）';
    }
    if (tip) tip.textContent = rest > 0 ? ('已显示 ' + rvShown + ' / ' + rvList.length + ' 题') : ('已全部加载 ' + rvList.length + ' 题');
}

/** 追加下一批（按钮点击 / 滚动到底自动触发） */
function rvAppendMore() {
    const wrap = document.getElementById('rvList');
    if (!wrap) return;
    const rest = rvList.slice(rvShown, rvShown + RV_PAGE);
    if (!rest.length) { rvUpdateMore(); return; }
    const batch = document.createElement('div');
    batch.className = 'rv-batch';
    batch.innerHTML = rest.map(rvCardHtml).join('');
    wrap.appendChild(batch);
    rvShown += rest.length;
    rvAfterRender(batch);
    rvUpdateMore();
}

/** 滚到底部附近自动加载下一批（浏览器不支持 IntersectionObserver 时按钮仍可用） */
function rvSetupAutoMore() {
    if (rvIO) { rvIO.disconnect(); rvIO = null; }
    const target = document.getElementById('rvBottom');
    if (!target || typeof IntersectionObserver === 'undefined') return;
    rvIO = new IntersectionObserver(es => { if (es.some(x => x.isIntersecting)) rvAppendMore(); }, { rootMargin: '600px' });
    rvIO.observe(target);
}

function renderReview() {
    const el = document.getElementById('catMain');
    const st = statusGet() || {}, fav = favGet() || {};
    const seen = new Set();
    const rows = [];
    for (const e of allEntriesAllSources()) {
        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null, f = !!fav[qid];
        if (!s && !f) continue;
        if (seen.has(qid)) continue;     // 同题多来源（真题/核心题库同源）只保留一条
        seen.add(qid);
        rows.push({ paper: e.paper, secTitle: e.secTitle, q: e.q, qid, st: s, fav: f });
    }
    const counts = {
        all: rows.length,
        fav: rows.filter(r => r.fav).length,
        mastered: rows.filter(r => r.st === 'mastered').length,
        unfamiliar: rows.filter(r => r.st === 'unfamiliar').length,
        unknown: rows.filter(r => r.st === 'unknown').length,
    };
    let list = rvFilter === 'all' ? rows
        : (rvFilter === 'fav' ? rows.filter(r => r.fav) : rows.filter(r => r.st === rvFilter));
    // 排序：不会 → 不熟 → 收藏 → 掌握；同类按年份倒序
    const rank = r => r.st === 'unknown' ? 0 : r.st === 'unfamiliar' ? 1 : (r.fav ? 2 : 3);
    list = list.slice().sort((a, b) => rank(a) - rank(b) || (Number(b.paper.year || 0) - Number(a.paper.year || 0)));
    rvList = list;
    rvShown = Math.min(RV_PAGE, list.length);

    const btns = [['all', `全部 ${counts.all}`], ['fav', `📥 收藏 ${counts.fav}`], ['mastered', `🟢 掌握 ${counts.mastered}`],
                  ['unfamiliar', `🟡 不熟 ${counts.unfamiliar}`], ['unknown', `🔴 不会 ${counts.unknown}`]]
        .map(([k, label]) => `<button class="cat-mark${rvFilter === k ? ' on' : ''}" data-rv="${k}" onclick="setRvFilter('${k}')">${label}</button>`).join('');
    let html = `<div class="paper-head">
        <h1>🔁 复测 · 我的标记题</h1>
        <div class="paper-sub">共 ${counts.all} 题 · 收藏 ${counts.fav} · 掌握 ${counts.mastered} · 不熟 ${counts.unfamiliar} · 不会 ${counts.unknown}｜分批加载（每批 ${RV_PAGE} 题，滚到底自动加载）｜笔记随题附带，标记与笔记改动实时同步</div>
        <div class="rv-filter">${btns}</div>
    </div>`;
    if (!list.length) {
        html += `<div class="empty-tip">当前筛选下没有题目。到真题页或分类页给题目点「☆ 收藏」或标「掌握 / 不熟 / 不会」，这里就会自动出现。</div>`;
        el.innerHTML = html;
        return;
    }
    html += `<div id="rvList"></div>
      <div class="rv-bottom" id="rvBottom">
        <button class="exam-btn" id="rvMoreBtn" onclick="rvAppendMore()">⬇️ 加载更多题</button>
        <span class="rv-more-tip" id="rvMoreTip"></span>
      </div>`;
    el.innerHTML = html;
    const wrap = document.getElementById('rvList');
    const batch = document.createElement('div');
    batch.className = 'rv-batch';
    batch.innerHTML = rvList.slice(0, rvShown).map(rvCardHtml).join('');
    wrap.appendChild(batch);
    rvAfterRender(batch);
    rvUpdateMore();
    rvSetupAutoMore();
}

// 跨标签页实时同步：别处（真题页 / 分类页）改动收藏、标记或笔记 → 复测页自动刷新
window.addEventListener('storage', (e) => {
    const k = e.key || '';
    if (k === FAV_KEY || k === EXAM_STATUS_KEY || k.indexOf('examNote-') === 0) {
        if (REVIEW_MODE) renderReview();
        else { renderTree(); renderMain(); }
    }
});

// ============ 拼卷页（category.html?paper=1）：随机抽收藏题，拼一份真题规模的卷 ============
// 需求（2026-10-14 grill 定稿）：
//   · 抽样：加权随机无放回 —— 不会 5 / 不熟 3 / 只收藏无状态 1 / 已掌握 0（排除）
//   · 池子：严格只从「标记过的题」抽（收藏或有状态）；某题型不够就缩水并在卷首标注
//   · 配比：选择 10 / 填空 6 / 解答 6 = 22 题（2024–2026 数二真题结构），统一 150 分制
//   · 章节：轻约束「至少覆盖 5 章」，不满足重抽（上限 20 次，试不出取覆盖最多的一版）
//   · 卷面：exam 式左栏（历史拼卷）+ 主区（按题型三段）+ 计时器（180 分钟可暂停重置）
const PAPER_MODE = new URLSearchParams(location.search).get('paper') === '1';

/** 卷面结构 + 分值（解答题 4×12 + 2×11 = 70，与选择 50 + 填空 30 合计 150） */
const PP_SHAPE = [
    { kind: '选择', scores: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5] },
    { kind: '填空', scores: [5, 5, 5, 5, 5, 5] },
    { kind: '解答', scores: [12, 12, 12, 12, 11, 11] },
];
const PP_RETRY = 20;        // 重抽次数（取其中章节覆盖最多的一版）
const PP_KEEP = 10;         // 历史卷保留份数
const PP_STORE = 'paperList';
const PP_SECS = 180 * 60;   // 计时总长（秒）

let ppCur = null;           // 当前卷 { id, ts, items:[{qid,kind,score}], left }
let ppTimerId = null;       // 计时器句柄

/** 状态权重：不会 5 / 不熟 3 / 仅收藏无状态 1 / 已掌握 0（排除） */
function ppWeight(qid, st, isFav) {
    const s = st[qid];
    if (s === 'unknown') return 5;
    if (s === 'unfamiliar') return 3;
    if (s === 'mastered') return 0;
    return isFav ? 1 : 0;
}

/** 真实题型。⚠️ q.kind 不可靠（解答题也标 blank），优先看 section.title；
 *  章节式题库（核心题库/大观园）节名不含题型 → 再按题目自身特征判定：
 *  有选项/kind=choice → 选择；有填空横线（含 \text{\_\_\_} 写法）或「（）」且非证明 → 填空；其余 → 解答 */
function ppKindOf(secTitle, q) {
    const t = secTitle || '';
    if (t.indexOf('选择') >= 0) return '选择';
    if (t.indexOf('填空') >= 0) return '填空';
    if (t.indexOf('解答') >= 0) return '解答';
    const stem = String((q && q.stem) || '');
    if ((q && q.options && q.options.length) || (q && q.kind === 'choice')) return '选择';
    const isProof = (q && q.kind === 'proof') || /证明/.test(stem);
    if (!isProof) {
        // 填空特征：连续下划线（含 \text{\_\_\_} 的转义写法）或题干以「（）」收尾
        if (/_{2,}|＿{2,}|\\text\{\\?_|（\s*）\s*$/.test(stem)) return '填空';
    }
    return '解答';
}

/** catId → 章（12 节之一）。运行时从 core_bank 的节归属取众数 ——
 *  那份归属 2026-10-13 已按大观严选题书签重排过，可信（真题 catId 覆盖率 100%）。
 *  2026-10-19 线代臻选题已并入 core_bank（替代原 346 题线代），这里只需 corePapers 一份。 */
let _ppCatCh = null;
function ppChapterOf(q) {
    if (_ppCatCh === null) {
        _ppCatCh = {};
        const tally = {};
        for (const p of (corePapers || [])) {
            for (const s of (p.sections || [])) {
                for (const q2 of (s.questions || [])) {
                    const cids = q2.categoryIds || (q2.catId != null ? [q2.catId] : []);
                    for (const c of cids) {
                        const k = String(c);
                        tally[k] = tally[k] || {};
                        tally[k][s.title] = (tally[k][s.title] || 0) + 1;
                    }
                }
            }
        }
        for (const k in tally) {
            let best = null, bn = -1;
            for (const t in tally[k]) if (tally[k][t] > bn) { bn = tally[k][t]; best = t; }
            _ppCatCh[k] = best;
        }
    }
    const cids = q.categoryIds || (q.catId != null ? [q.catId] : []);
    for (const c of cids) { const ch = _ppCatCh[String(c)]; if (ch) return ch; }
    return null;
}

/** 收集所有源的标记题，按题型分层。⚠️ 收藏横跨 4 个源（真题/核心题库/大观园习题/真题库），
 *  漏掉任何一源都会让部分收藏题永远抽不到。
 *  权重体系（2026-10-14 起）：
 *    sw = 状态权重（不会 5 / 不熟 3 / 仅收藏 1；已掌握排除）
 *    tf = 收藏时间系数（越早越高，1~3，与 sw **相乘**）
 *    w  = sw × tf  ← 抽样实际用这个
 *  这样「早收藏的仅收藏题」(1×3=3) 仍低于「近期不会的题」(5×1=5)，状态优先级不被推翻。 */
function ppBuildPool() {
    const fav = favGet() || {}, st = statusGet() || {};
    const seen = new Set();
    const pool = { '选择': [], '填空': [], '解答': [] };
    const push = (paper, secTitle, q) => {
        const qid = qidOf(paper.id, q.no);
        if (!qid || seen.has(qid)) return;          // 同题多来源只留一条
        seen.add(qid);
        // ⚠️ 严格只抽**收藏**的题（2026-10-14 定：某题型不够就缩水，不放宽到「有状态未收藏」）
        if (!fav[qid]) return;
        const sw = ppWeight(qid, st, true);
        if (sw <= 0) return;                         // 已掌握 → 排除
        pool[ppKindOf(secTitle, q)].push({
            paper, secTitle, q, qid, sw, tf: 1, w: sw,
            state: st[qid] || null, fav: true,
            t: favTime(qid) || 0,
        });
    };
    for (const p of (examPapers || [])) for (const s of (p.sections || [])) for (const q of (s.questions || [])) push(p, s.title, q);
    for (const p of (corePapers || [])) for (const s of (p.sections || [])) for (const q of (s.questions || [])) push(p, s.title, q);
    for (const e of (bankItems || [])) push(e.paper, e.secTitle || '', e.q);

    // 第二遍：按收藏时间在**本池内**的排名给时间系数（最早的 tf=3，最近的 tf=1）。
    // 用池内相对排名而非绝对天数，池子变大/变小都不会让系数失衡。
    const all = pool['选择'].concat(pool['填空'], pool['解答']);
    const ts = all.map(it => it.t).filter(t => t > 0).sort((a, b) => a - b);
    if (ts.length > 1) {
        for (const it of all) {
            let rank = 0;
            if (it.t > 0) {
                let lo = 0, hi = ts.length - 1;             // 二分找 it.t 在有序时间里的位置
                while (lo < hi) { const m = (lo + hi) >> 1; if (ts[m] < it.t) lo = m + 1; else hi = m; }
                rank = lo / (ts.length - 1);                 // 0 = 最早，1 = 最近
            }
            it.tf = 1 + 2 * (1 - rank);
            it.w = it.sw * it.tf;
        }
    }
    return pool;
}

/** 加权无放回抽 k 个（用元素自带的 w 权重） */
function ppSample(arr, k) {
    const pool = (arr || []).slice();
    const out = [];
    for (let n = 0; n < k && pool.length; n++) {
        let total = 0;
        for (const it of pool) total += it.w;
        if (total <= 0) break;
        let r = Math.random() * total, idx = 0;
        for (; idx < pool.length; idx++) { r -= pool[idx].w; if (r <= 0) break; }
        if (idx >= pool.length) idx = pool.length - 1;
        out.push(pool[idx]);
        pool.splice(idx, 1);
    }
    return out;
}

/** 拼一份卷：按配额抽 → 20 次重抽里**取章节覆盖最多的一版**（用户要「知识点覆盖尽量广」，
 *  所以不再满足 5 章就早停）。返回 { items, chapters, pool, short } */
function ppBuild() {
    const pool = ppBuildPool();
    // 选填共 16 题（数二：10 选择 + 6 填空，每题 5 分）。选择题不够时用填空题补足 16 个选填位。
    const CHOICE_MAX = PP_SHAPE[0].scores.length;                       // 10
    const TIANXUAN_N = PP_SHAPE[0].scores.length + PP_SHAPE[1].scores.length;  // 16
    const AN_SCORES = PP_SHAPE[2].scores;                               // [12,12,12,12,11,11]
    let best = null;
    for (let t = 0; t < PP_RETRY; t++) {
        const picked = [];
        // ① 选填 16 位：先抽选择（≤10），差额用填空补齐（都按 5 分计）
        const ch = ppSample(pool['选择'], CHOICE_MAX);
        ch.forEach(it => picked.push(Object.assign({}, it, { kind: '选择', score: 5 })));
        const needFill = TIANXUAN_N - ch.length;
        if (needFill > 0) {
            ppSample(pool['填空'], needFill).forEach(it =>
                picked.push(Object.assign({}, it, { kind: '填空', score: 5 })));
        }
        // ② 解答 6 题
        ppSample(pool['解答'], AN_SCORES.length).forEach((it, i) =>
            picked.push(Object.assign({}, it, { kind: '解答', score: AN_SCORES[i] })));
        if (!picked.length) break;
        const chs = [];
        for (const it of picked) { const ch2 = ppChapterOf(it.q); if (ch2 && chs.indexOf(ch2) < 0) chs.push(ch2); }
        const rec = { items: picked, chapters: chs, pool, short: false };
        if (!best || chs.length > best.chapters.length) best = rec;   // 取覆盖最多
    }
    if (best) { best.short = best.items.length < 22; return best; }
    return { items: [], chapters: [], pool, short: true };
}

/* ---------- 拼卷：qid 索引（按 qid 还原题，供历史卷用；建一次缓存） ---------- */
let _ppIdx = null;
function ppOfQid(qid) {
    if (_ppIdx === null) {
        _ppIdx = {};
        const add = (paper, secTitle, q) => {
            const k = qidOf(paper.id, q.no);
            if (k && !_ppIdx[k]) _ppIdx[k] = { paper, secTitle, q };
        };
        for (const p of (examPapers || [])) for (const s of (p.sections || [])) for (const q of (s.questions || [])) add(p, s.title, q);
        for (const p of (corePapers || [])) for (const s of (p.sections || [])) for (const q of (s.questions || [])) add(p, s.title, q);
        for (const e of (bankItems || [])) add(e.paper, e.secTitle || '', e.q);
    }
    return _ppIdx[qid] || null;
}

/* ---------- 拼卷：历史卷存储（localStorage，保留 PP_KEEP 份） ---------- */
function ppListGet() {
    try { return JSON.parse(localStorage.getItem(PP_STORE) || '[]') || []; } catch (e) { return []; }
}
function ppListSave(list) {
    try { localStorage.setItem(PP_STORE, JSON.stringify((list || []).slice(0, PP_KEEP))); } catch (e) { }
}
/** 把当前卷写回历史（已在列表里则就地更新） */
function ppSaveCur() {
    if (!ppCur) return;
    const list = ppListGet();
    const i = list.findIndex(x => x.id === ppCur.id);
    const rec = {
        id: ppCur.id, ts: ppCur.ts, left: ppCur.left, done: !!ppCur.done,
        items: ppCur.items.map(it => ({ qid: it.qid, kind: it.kind, score: it.score, state: it.state || null })),
    };
    if (i >= 0) list[i] = rec; else list.unshift(rec);
    ppListSave(list);
}
function ppDel(id) {
    ppListSave(ppListGet().filter(x => x.id !== id));
    if (ppCur && ppCur.id === id) {                 // 删的是当前卷 → 切到最新一份，没有就新拼
        const rest = ppListGet();
        if (rest.length) { ppOpen(rest[0].id); } else { ppCur = null; ppNew(); return; }
    }
    ppSide();
}

/* ---------- 拼卷：计时器（180 分钟，可暂停/继续/重置；到时只提醒不强制） ---------- */
function ppClockText(sec) {
    sec = Math.max(0, Math.floor(sec));
    const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
    const p = n => (n < 10 ? '0' : '') + n;
    return p(h) + ':' + p(m) + ':' + p(s);
}
function ppPaintClock() {
    const c = document.getElementById('ppClock');
    if (!c || !ppCur) return;
    c.textContent = ppClockText(ppCur.left);
    c.classList.toggle('over', ppCur.left <= 0);
    const b = document.getElementById('ppTimerBtn');
    if (b) b.textContent = ppCur.running ? '⏸' : '▶';
}
function ppStartTimer() {
    if (ppTimerId) return;
    ppTimerId = setInterval(() => {
        if (!ppCur || !ppCur.running) return;
        ppCur.left = Math.max(0, ppCur.left - 1);
        ppPaintClock();
        if (ppCur.left === 0) {
            ppCur.running = false;
            ppSaveCur();
            const b = document.getElementById('ppBanner');
            if (b) { b.textContent = '⏰ 时间到！可以继续做完，也可以直接对答案。'; b.hidden = false; }
        }
        if (ppCur.left % 15 === 0) ppSaveCur();      // 每 15 秒落盘一次（别每 tick 都写）
    }, 1000);
}
function ppStopTimer() { if (ppTimerId) { clearInterval(ppTimerId); ppTimerId = null; } }
function ppToggleTimer() {
    if (!ppCur) return;
    ppCur.running = !ppCur.running;
    ppPaintClock(); ppSaveCur();
    if (ppCur.running) ppStartTimer();
}
function ppResetTimer() {
    if (!ppCur) return;
    ppCur.left = PP_SECS; ppCur.running = false;
    const b = document.getElementById('ppBanner');
    if (b) b.hidden = true;
    ppPaintClock(); ppSaveCur(); ppStopTimer();
}

/* ---------- 拼卷：左栏「历史拼卷」列表 ---------- */
function ppFmtTs(ts) {
    const d = new Date(ts);
    const p = n => (n < 10 ? '0' : '') + n;
    return p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
}
function ppSide() {
    const box = document.getElementById('paperList');
    if (!box) return;
    const list = ppListGet();
    let html = `<button class="pp-new" onclick="ppNew()">🎲 重新拼卷</button>`;
    if (!list.length) {
        html += `<div class="pp-empty">还没有拼过卷。</div>`;
    } else {
        html += list.map(x => `<div class="pp-row${ppCur && ppCur.id === x.id ? ' on' : ''}" data-pp="${x.id}">
            <span class="pp-row-main" onclick="ppOpen('${x.id}')">${ppFmtTs(x.ts)} · ${x.items.length}题${x.done ? ' ✓' : ''}</span>
            <button class="pp-del" title="删除这份卷" onclick="event.stopPropagation();ppDel('${x.id}')">×</button>
        </div>`).join('');
    }
    box.innerHTML = html;
}

/* ---------- 拼卷：主区渲染（卷首 + 三段题卡） ---------- */
const PP_SEGS = [
    { kind: '选择', title: '一、选择题' },
    { kind: '填空', title: '二、填空题' },
    { kind: '解答', title: '三、解答题' },
];

/** 渲染后处理：KaTeX + 有笔记的自动展开 + 贴图回填（与复测页同款） */
function ppAfterRender(root) {
    renderMath(root);
    root.querySelectorAll('.q-card').forEach(card => {
        const qid = card.id.replace(/^q-/, '');
        if ((noteGet(qid) || '').trim()) {
            const nb = card.querySelector('[data-act="note"]');
            if (nb && !nb.classList.contains('on')) nb.click();
        }
    });
    root.querySelectorAll('.q-note-preview:not([hidden])').forEach(pv => fillExamNoteImgs(pv));
}

function ppRender() {
    const el = document.getElementById('catMain');
    if (!el) return;
    if (!ppCur) {
        el.innerHTML = `<div class="cat-empty">还没有卷。<br>点左栏「🎲 重新拼卷」开始。</div>`;
        return;
    }
    const items = ppCur.items || [];
    // 卷首构成：优先用**拼卷时的状态快照**（做题过程中状态会变，快照才反映当时的选择）
    const st = statusGet() || {};
    const c = { unknown: 0, unfamiliar: 0, plain: 0 };
    for (const it of items) {
        const s = it.state || st[it.qid];
        if (s === 'unknown') c.unknown++;
        else if (s === 'unfamiliar') c.unfamiliar++;
        else c.plain++;
    }
    const total = items.reduce((a, it) => a + (it.score || 0), 0);
    const nCh = (ppCur.chapters || []).length;
    const nChoice = items.filter(it => it.kind === '选择').length;
    const nFill = items.filter(it => it.kind === '填空').length;
    const fillNote = (nChoice < PP_SHAPE[0].scores.length && nFill > PP_SHAPE[1].scores.length)
        ? `｜选择题不足，已用填空题补足 ${PP_SHAPE[0].scores.length + PP_SHAPE[1].scores.length} 个选填位` : '';
    let html = `<div class="paper-head">
        <h1>🎲 拼卷 · ${ppFmtTs(ppCur.ts)}</h1>
        <div class="paper-sub">共 ${items.length} 题 · ${total} 分｜${c.unknown} 不会 · ${c.unfamiliar} 不熟 · ${c.plain} 仅收藏${nCh ? '｜覆盖 ' + nCh + ' 章' : ''}${fillNote}</div>
        <div class="pp-bar">
            <button class="exam-btn" onclick="ppNew()" title="按同样的规则重新抽一份">🎲 重新拼卷</button>
            <div class="pp-timer">
                <span class="pp-clock" id="ppClock">${ppClockText(ppCur.left != null ? ppCur.left : PP_SECS)}</span>
                <button class="pp-tbtn" id="ppTimerBtn" onclick="ppToggleTimer()" title="暂停 / 继续">${ppCur.running ? '⏸' : '▶'}</button>
                <button class="pp-tbtn" onclick="ppResetTimer()" title="重置为 180 分钟">↺</button>
            </div>
        </div>
        <div class="pp-banner" id="ppBanner" hidden></div>
        ${items.length < 22 ? `<div class="pp-short">⚠️ 本卷只有 ${items.length} 题（标记的题不够凑满 22 题；多收藏一些题就能凑齐）</div>` : ''}
    </div>`;
    let n = 0;
    for (const seg of PP_SEGS) {
        const list = items.filter(it => it.kind === seg.kind);
        if (!list.length) continue;
        const sc = list.reduce((a, it) => a + (it.score || 0), 0);
        html += `<h2 class="pp-seg">${seg.title}（共 ${list.length} 题，${sc} 分）</h2>`;
        for (const it of list) {
            n++;
            const found = ppOfQid(it.qid);
            const head = `<div class="pp-item-head">第 ${n} 题 · ${it.score} 分</div>`;
            html += found
                ? `<div class="pp-item">${head}${catCard(found.paper, found.secTitle, found.q)}</div>`
                : `<div class="pp-item">${head}<div class="empty-tip">这道题已不在题库里（${it.qid}）</div></div>`;
        }
    }
    el.innerHTML = html;
    ppAfterRender(el);
    ppPaintClock();
}

/** 拼一份新卷（加入历史列表并切过去） */
function ppNew() {
    const rec = ppBuild();
    const el = document.getElementById('catMain');
    if (!rec.items.length) {
        if (el) el.innerHTML = `<div class="cat-empty">没有可抽的题。<br>请先到分类页 / 真题页给题目点「☆ 收藏」或标「不熟 / 不会」，再回来拼卷。</div>`;
        return;
    }
    ppCur = {
        id: String(Date.now()), ts: Date.now(), left: PP_SECS, running: false, done: false,
        chapters: rec.chapters || [],
        items: rec.items.map(it => ({ qid: it.qid, kind: it.kind, score: it.score, state: it.state || null })),
    };
    ppStopTimer(); ppSaveCur(); ppSide(); ppRender();
}

/** 打开历史卷（⚠️ 一律先暂停：关页期间不该空走时间） */
function ppOpen(id) {
    const rec = ppListGet().find(x => x.id === id);
    if (!rec) return;
    ppCur = {
        id: rec.id, ts: rec.ts, left: rec.left != null ? rec.left : PP_SECS,
        running: false, done: !!rec.done, chapters: rec.chapters || [],
        items: rec.items || [],
    };
    ppStopTimer(); ppSide(); ppRender();
}

/** 拼卷模式初始化：顶栏改文案、隐藏分类专属控件、左栏换成历史拼卷列表 */
function ppApplyMode() {
    if (!PAPER_MODE) return;
    document.body.classList.add('paper-mode');
    const t = document.querySelector('.exam-title');
    if (t) t.textContent = '🎲 拼卷';
    document.title = '🎲 拼卷 · 随机收藏题';
    const sub = document.getElementById('examSub');
    if (sub) {
        sub.textContent = '从标记过的题里随机拼一份 22 题 / 150 分的卷 · 优先「不会 / 不熟」';
        sub.hidden = false;
    }
    ['srcToggle', 'unmarkedFirst', 'yearSortBtn'].forEach(id => {
        const b = document.getElementById(id);
        if (b) b.style.display = 'none';
    });
    const marks = document.querySelector('.cat-marks');
    if (marks) marks.style.display = 'none';
    const st = document.querySelector('.exam-side-title');
    if (st) st.textContent = '历史拼卷';
    const tree = document.getElementById('catTree');
    if (tree) tree.innerHTML = '<div id="paperList"></div>';
}

// ============ 渲染：主区 ============
function renderMain() {
    const el = document.getElementById('catMain');
    if (REVIEW_MODE) { renderReview(); return; }           // 复测模式：标记题汇总
    if (PAPER_MODE) {                                      // 拼卷模式：拼出的卷
        if (!ppCur) {
            const list = ppListGet();
            if (list.length) { ppOpen(list[0].id); return; }   // 有历史卷 → 载入最新一份
            ppNew(); return;                                    // 没有 → 现拼一份
        }
        ppRender(); return;
    }
    if (catSearchKw) { renderSearchResults(); return; }   // 搜索模式：跨分类列表
    if (curCat == null) {
        el.innerHTML = `<div class="cat-empty">← 选择左侧章节，查看该考点的历年真题</div>`;
        return;
    }
    // 细分类筛选：curDeepCat 非空时只取「落在该细分支子树内」的题（按 deepCats 交集判定）
    const deepSet = curDeepCat ? (curDeepSelf ? new Set([String(curDeepCat)]) : deepSubtreeSet(curDeepCat)) : null;
    const catSet = curCatSet();
    const entries = activeEntries().filter(e =>
        catSet.has(String(e.catId)) &&
        (!deepSet || (e.q.deepCats || []).some(id => deepSet.has(String(id)))));
    const c = cats[curCat];
    // 排序：无标记优先（可选）→ 收藏时间倒序 → 年份倒序
    entries.sort(compareEntries);
    if (!entries.length) {
        el.innerHTML = `<div class="paper-head"><h1>${c ? (c.display || c.name) : curCat}</h1><div class="paper-sub">${c ? c.path : ''}</div></div>` +
            (deepSet ? deepFilterTip(0) : '') +
            `<div class="empty-tip">${deepSet ? '该细分支下当前没有题目。' : '该章节下当前筛选没有匹配题目。'}试试切换「收藏/不熟/不会」筛选${deepSet ? '，或点上方「✕ 清除细分类」' : ''}。</div>`;
        return;
    }
    const years = new Set(entries.map(e => e.paper.year)).size;
    const unmarkedN = unmarkedFirst ? entries.filter(isUnmarked).length : 0;
    let html = `<div class="paper-head">
        <h1>${c ? c.display : curCat}</h1>
        <div class="paper-sub">${c ? c.path : ''}</div>
        <div class="paper-meta">共 ${entries.length} 题 · 跨 ${years} 年${unmarkedFirst ? ` · <b>无标记优先</b>（未标记 ${unmarkedN} 题已提前）` : ' · <b>掌握度排序</b>（不会→不熟→收藏→无标记→掌握）'} · ${yearSortDesc ? '<b>年份倒序</b>' : '<b>年份顺序</b>'}</div>
        <button class="all-ans-btn" id="allAnsBtn" onclick="toggleAllAnswers(this)">🔼 展开全部答案</button>
    </div>`;
    if (deepSet) html += deepFilterTip(entries.length);
    const markNames = { fav: '📥收藏', unfamiliar: '🟡不熟', unknown: '🔴不会' };
    const activeMark = Object.keys(markSel).filter(k => markSel[k]);
    if (activeMark.length) html += `<div class="cat-filter-tip">筛选：${activeMark.map(k => markNames[k]).join(' / ')}</div>`;
    catStartList(entries, html);
    renderNav();   // 刷新悬浮题号导航
}
// ============ 顶栏搜索：题干文字 / 年份 / 题号 / 知识点路径 ============
let catSearchKw = '';                 // 当前搜索词（空 = 分类浏览模式）
let catSearchTimer = null;

// 输入中：只更新「清除按钮」显隐，不触发搜索（搜索须按回车确认）
function onCatSearchInput(v) {
    const clr = document.getElementById('catSearchClear');
    if (clr) clr.style.display = (v || '').trim() ? '' : 'none';
}
// 按回车（Enter）确认搜索
function onCatSearch(v) {
    clearTimeout(catSearchTimer);
    const kw = (v || '').trim();
    catSearchKw = kw;
    const clr = document.getElementById('catSearchClear');
    if (clr) clr.style.display = kw ? '' : 'none';
    renderMain();
}

function clearCatSearch() {
    const inp = document.getElementById('catSearch');
    if (inp) inp.value = '';
    catSearchKw = '';
    const clr = document.getElementById('catSearchClear');
    if (clr) clr.style.display = 'none';
    renderTree();   // 退出搜索模式，恢复分类树题数
    renderMain();
}

// 搜索匹配：题干（去 LaTeX 后）、年份、题号、知识点路径 任一命中即算
function catSearchMatch(e) {
    const kw = catSearchKw.toLowerCase();
    if (!kw) return true;
    const q = e.q; const p = e.paper;
    if (String(p.year).toLowerCase().includes(kw)) return true;          // 年份
    if (String(q.no).toLowerCase().includes(kw)) return true;            // 题号
    const stem = (q.stem || '').replace(/\$[^$]*\$/g, ' ').replace(/\s+/g, ' ');
    if (stem.toLowerCase().includes(kw)) return true;                    // 题干文字
    const c = cats[String(e.catId)];
    const path = (c ? (c.path || c.name || c.display || '') : '') ;
    if (path.toLowerCase().includes(kw)) return true;                    // 知识点路径
    if ((q.answer || '').replace(/\$[^$]*\$/g, ' ').toLowerCase().includes(kw)) return true; // 答案文字
    return false;
}

// 搜索模式：主区横跨全分类列出命中题；空关键词回到分类浏览
function renderSearchResults() {
    const el = document.getElementById('catMain');
    const entries = activeEntries().filter(catSearchMatch);
    const sy = window.scrollY;
    // 无标记优先（可选）→ 收藏时间倒序 → 年份倒序
    entries.sort(compareEntries);
    const h = `<div class="paper-head">
        <h1>🔍 “${catSearchKw}”</h1>
        <div class="paper-sub">全库搜索命中 ${entries.length} 题 · 每题上方可点「进入分支」直接去该知识点刷题</div>
        ${entries.length ? `<div class="paper-meta">共 ${entries.length} 题 · 跨 ${new Set(entries.map(e => e.paper.year)).size} 年</div>` : ''}
    </div>`;
    const markNames = { fav: '📥收藏', unfamiliar: '🟡不熟', unknown: '🔴不会' };
    const activeMark = Object.keys(markSel).filter(k => markSel[k]);
    if (activeMark.length) h += `<div class="cat-filter-tip">筛选：${activeMark.map(k => markNames[k]).join(' / ')}</div>`;
    if (!entries.length) {
        el.innerHTML = h + `<div class="empty-tip">没有匹配题目。试试别的关键词，或切换「收藏/不熟/不会」筛选。</div>`;
        return;
    }
    // 逐题惰性生成（分批渲染，避免一次性 1000+ 题卡卡死）；连续同分支只显示一条跳转条
    let lastBranch = '';
    const cardFn = (e) => {
        let one = '';
        const c = cats[String(e.catId)];
        if (c) {
            const path = c.path || c.name || String(e.catId);
            if (path !== lastBranch) {
                lastBranch = path;
                one += `<div class="q-branch-chip" onclick="jumpBranch(${e.catId})" title="展开左侧分类树并进入该知识点分支刷题">
                    <span class="q-branch-path">📂 ${esc(path)}</span>
                    <span class="q-branch-go">进入此分支 →</span>
                </div>`;
            }
        }
        return one + catCard(e.paper, e.secTitle, e.q);
    };
    catStartList(entries, h, cardFn);
    requestAnimationFrame(() => window.scrollTo(0, sy));
    renderNav();
}


// ============ 细分类悬浮窗（大观园 826 节点体系；主树保持三级，悬停弹出下分支） ============
// 数据：cat_deep.json = { nodes: {id:{n,p}}, l2root: {本库L2id: 大观园节点id} }
// 题的细分类标签：q.deepCats = [大观园节点 id, ...]
let catDeep = null;          // { nodes, l2root }
let deepChildren = {};       // 大观园 parentId -> [childId]（原始树：题目过滤/计数用）
let deepChildrenView = {};   // 压缩树（悬停浮层展示用）：跳过与父节点同名的冗余中间层
let curDeepCat = null;       // 当前选中的细分类节点（非空时题目按该子树过滤）
let _flySub = {};            // 当前浮层使用的「按知识点」细分类计数表（sub）
let _flyDirect = {};         // 同上（direct：直接挂在该节点上的题数）
let curDeepSelf = false;     // true = 只筛「本级」题（不含子树）
// 刷新后恢复上次选中的细分类（2026-10-14 用户要求：刷新不该把 🔎 细分类清掉）。
// ⚠️ 必须在这里恢复而不是文件开头 —— curDeepCat/curDeepSelf 是 let，声明前访问会 TDZ 报错。
// ⚠️ 有效性校验（数据变更后节点可能已不存在）放在 loadCatDeep() 里，那时 catDeep 才到手。
try {
    const _ds = JSON.parse(localStorage.getItem(CAT_STATE_KEY) || '{}');
    if (_ds.curDeepCat) {
        curDeepCat = String(_ds.curDeepCat);
        curDeepSelf = !!_ds.curDeepSelf;
    }
} catch (e) { }

async function loadCatDeep() {
    try {
        const r = await fetch('data/cat_deep.json');
        if (!r.ok) return;
        catDeep = await r.json();
        deepChildren = {};
        for (const id in (catDeep.nodes || {})) {
            const p = catDeep.nodes[id].p;
            if (p) (deepChildren[p] = deepChildren[p] || []).push(id);
        }
        for (const p in deepChildren) {
            deepChildren[p].sort((a, b) => (catDeep.nodes[a].n || '').localeCompare(catDeep.nodes[b].n || '', 'zh'));
        }
        buildDeepChildrenView();
        // 恢复的细分类选中态要校验：数据更新后节点可能已不存在 → 清掉，避免主区空过滤
        if (curDeepCat && !(catDeep.nodes || {})[String(curDeepCat)]) {
            curDeepCat = null;
            curDeepSelf = false;
            saveCatState();
        }
    } catch (e) { console.warn('细分类树加载失败，悬停浮层不可用', e); }
}

/** 细分类节点 → 它归属的「分类树节点」id（curCat 可直接用）。
 *  依据：细分类链里会**直接出现分类树 id**，例如
 *      1000(二阶可降解) ← 999 ← 766 ← 762(解微分方程) ← 325(微分方程) ← 223(高等数学)
 *  取链上**最深**的那个命中项 —— 那才是它真正归属的章节/知识点。
 *  用途：点击「另一个大分支的细分类」时，自动把主区切到那个分支（2026-10-14 用户要求）。 */
function deepOwnerCat(id) {
    if (!catDeep || !catDeep.nodes || typeof cats === 'undefined' || !cats) return null;
    let cur = String(id);
    const chain = [];
    for (let i = 0; i < 60 && cur && catDeep.nodes[cur]; i++) {
        chain.push(cur);
        cur = catDeep.nodes[cur].p;
    }
    for (const c of chain) if (cats[c]) return c;      // 链是深→浅，第一个命中即最深归属
    return null;
}

/** 若细分类归属另一个分支，先把主区切过去（复用 selectCat：展开树 + 存状态 + 重渲染） */
function deepEnsureOwner(id) {
    const owner = deepOwnerCat(id);
    if (owner && String(curCat) !== String(owner)) {
        selectCat(owner);       // ⚠️ selectCat 会把 curDeepCat 清空，所以调用方要在它之后再设 curDeepCat
        return true;
    }
    return false;
}

/** 构建「展示用」压缩树：某层子节点若与父节点**同名**（纯冗余的中间层，如 极限→极限），
 *  则跳过它直接用它的子节点（递归）。注意：题目过滤/计数仍走原始 deepChildren，范围不受影响。 */
function buildDeepChildrenView() {
    deepChildrenView = {};
    const same = (a, b) => {
        const na = catDeep.nodes[a], nb = catDeep.nodes[b];
        return !!(na && nb && na.n && na.n === nb.n);
    };
    const expand = (pid, cid, seen) => {
        if (!seen.has(cid) && same(pid, cid) && (deepChildren[cid] || []).length) {
            seen.add(cid);
            const out = [];
            for (const k of deepChildren[cid]) out.push(...expand(cid, k, seen));
            return out;
        }
        return [cid];
    };
    for (const pid in deepChildren) {
        const seen = new Set(), out = [];
        for (const c of deepChildren[pid]) out.push(...expand(pid, c, seen));
        deepChildrenView[pid] = out;
    }
}

/** 按知识点统计细分类题数：direct（直接挂该节点）+ sub（含整棵子树）。
 *  必须按知识点统计——否则浮层显示的是全库题数，与点击后「当前知识点内」的列表对不上（10 vs 8）。
 *  结果按 catId 缓存；题集变化（切源/标记变化）时由 buildDeepIndex() 清空。 */
const _deepCountCache = {};
function deepCountsForCat(catId) {
    const key = String(catId);
    if (_deepCountCache[key]) return _deepCountCache[key];
    if (!catDeep) return { direct: {}, sub: {} };
    const direct = {};
    for (const e of allEntries) {
        if (String(e.catId) !== key) continue;
        for (const id of (e.q.deepCats || [])) {
            if (!catDeep.nodes[id]) continue;
            direct[id] = (direct[id] || 0) + 1;
        }
    }
    const sub = {};
    for (const id in direct) {
        const n = direct[id];
        let cur = id, guard = 0;
        while (cur && catDeep.nodes[cur] && guard++ < 20) {
            sub[cur] = (sub[cur] || 0) + n;
            cur = catDeep.nodes[cur].p;
        }
    }
    return (_deepCountCache[key] = { direct, sub });
}

/** 题集/标记变化后清空按知识点的计数缓存 */
function buildDeepIndex() {
    for (const k in _deepCountCache) delete _deepCountCache[k];
}

/** 细分类节点的完整路径（用于页头提示） */
function deepPath(id) {
    const parts = [];
    let cur = id, guard = 0;
    while (cur && catDeep && catDeep.nodes[cur] && guard++ < 20) {
        parts.unshift(catDeep.nodes[cur].n);
        cur = catDeep.nodes[cur].p;
    }
    return parts.join(' / ');
}

/** 细分类节点的整棵子树 id 集合（含自身），用于题目过滤 */function deepSubtreeSet(id) {
    const out = new Set(), stack = [String(id)];
    while (stack.length) {
        const x = stack.pop();
        if (out.has(x)) continue;
        out.add(x);
        stack.push(...(deepChildren[x] || []));
    }
    return out;
}

/** 本库知识点或章节 → 其对应的大观园细分类根节点（无映射返回 null） */
function deepRootOfCat(catId) {
    if (!catDeep || !catDeep.l2root) return null;
    return catDeep.l2root[String(catId)] || null;
}

/** 章节级别的细分类根节点（线代章节直接对应大观园的章节节点 2~7） */
function deepRootOfChapter(chId) {
    if (!catDeep || !catDeep.nodes) return null;
    const cid = String(chId);
    // 线代 6 大章 id 分别为 2, 3, 4, 5, 6, 7
    if (['2', '3', '4', '5', '6', '7'].includes(cid) && catDeep.nodes[cid]) {
        return cid;
    }
    return null;
}

/** 章节悬停入口：线代 6 大章悬停直接展示该章全部下分支 */
function onChapterNodeEnter(nodeEl, chId) {
    const root = deepRootOfChapter(chId);
    if (!root) { scheduleHideDeepFly(60); return; }
    // 统计属于该章的所有题目在该子树下的细分类分布
    if (!catDeep) { scheduleHideDeepFly(60); return; }
    const key = String(chId);
    const direct = {};
    // 查找该章包含的所有 L3 叶子节点 id
    const childLeaves = new Set();
    for (const id in cats) {
        if (String(cats[id].parentId) === key) childLeaves.add(String(id));
    }
    for (const e of allEntries) {
        if (!childLeaves.has(String(e.catId))) continue;
        for (const id of (e.q.deepCats || [])) {
            if (!catDeep.nodes[id]) continue;
            direct[id] = (direct[id] || 0) + 1;
        }
    }
    const sub = {};
    for (const id in direct) {
        const n = direct[id];
        let cur = id, guard = 0;
        while (cur && catDeep.nodes[cur] && guard++ < 20) {
            sub[cur] = (sub[cur] || 0) + n;
            cur = catDeep.nodes[cur].p;
        }
    }
    if (!sub[root]) { scheduleHideDeepFly(60); return; }
    // 与 onCatNodeEnter 同：根下没有有题的子分支就不弹（避免只剩「本级·未细分」）
    if (!(deepChildrenView[root] || []).some(c => (sub[c] || 0) > 0)) { scheduleHideDeepFly(60); return; }
    _flySub = sub;
    _flyDirect = direct;
    clearTimeout(_flyHideTimer);
    showDeepBrowse(root, 0, nodeEl.getBoundingClientRect());
}

/** 细分类筛选态提示条（页头）：题数用列表实际条数，避免与浮层计数口径不一致 */
function deepFilterTip(n) {
    if (!curDeepCat) return '';
    return `<div class="deep-filter-tip">🔎 细分类：<b>${esc(deepPath(curDeepCat))}</b>${curDeepSelf ? '（本级·未细分）' : ''}（${n != null ? n : 0} 题）
        <button class="deep-clear" onclick="clearDeepCat()" title="退出细分类，回到该知识点全部题">✕ 清除细分类</button></div>`;
}

// ---- 浮层渲染与逐级级联 ----
let _flyHideTimer = null;const _flyLevels = [];   // 当前显示的各层级元素

function _flyEnsure(level) {
    let el = document.getElementById('deepFly' + level);
    if (!el) {
        el = document.createElement('div');
        el.className = 'deep-fly';
        el.id = 'deepFly' + level;
        el.hidden = true;
        // 鼠标进入浮层：取消隐藏；离开则整组收起
        el.addEventListener('mouseenter', () => { clearTimeout(_flyHideTimer); });
        el.addEventListener('mouseleave', () => scheduleHideDeepFly());
        document.body.appendChild(el);
    }
    return el;
}

function hideDeepFlyNow() {
    _flyLevels.forEach(el => { if (el) el.hidden = true; });
    _flyLevels.length = 0;
}
function scheduleHideDeepFly(delay) {
    clearTimeout(_flyHideTimer);
    _flyHideTimer = setTimeout(() => { if (!document.querySelector('.deep-fly:hover')) hideDeepFlyNow(); }, delay || 220);
}

/** 在第 level 层展示 nodeId 的子分支；anchor 为触发元素（用其右缘定位） */
function showDeepBrowse(nodeId, level, anchorRect) {
    // 收起比本层更深的浮层
    for (let i = level; i < _flyLevels.length; i++) if (_flyLevels[i]) _flyLevels[i].hidden = true;
    _flyLevels.length = Math.min(_flyLevels.length, level);
    const kids = (deepChildrenView[nodeId] || []).filter(c => (_flySub[c] || 0) > 0);   // 展示用压缩树
    const el = _flyEnsure(level);
    const hd = catDeep && catDeep.nodes[nodeId] ? catDeep.nodes[nodeId].n : '';
    const selfCnt = _flyDirect[nodeId] || 0;
    const selfItem = selfCnt ? `<div class="deep-item deep-self${curDeepSelf && String(curDeepCat) === String(nodeId) ? ' on' : ''}"
                        data-deep-self="${nodeId}" title="只显示直接挂在本级的题目（未细分到下列分支）">
                        <span class="deep-item-name">▸ 本级（未细分）</span>
                        <span class="deep-item-cnt">${selfCnt}</span>
                    </div>` : '';
    el.innerHTML = `<div class="deep-fly-hd" title="${esc(hd)}">${esc(hd)} · 下分支</div>` + selfItem +
        (kids.length ? kids.map(c => {
            const nm = catDeep.nodes[c] ? catDeep.nodes[c].n : c;
            const cnt = _flySub[c] || 0;
            const hasKids = (deepChildrenView[c] || []).some(k => (_flySub[k] || 0) > 0);
            return `<div class="deep-item${hasKids ? ' has-kids' : ''}${String(curDeepCat) === String(c) ? ' on' : ''}"
                        data-deep="${c}" title="${esc(deepPath(c))}｜共 ${cnt} 题">
                        <span class="deep-item-name">${esc(nm)}</span>
                        <span class="deep-item-cnt">${cnt}</span>
                    </div>`;
        }).join('') : '<div class="deep-empty">该分支下暂无细分类题目</div>');
    el.hidden = false;
    _flyLevels[level] = el;
    // 定位：优先贴 anchor 右缘；右侧空间不足则放左侧
    const w = el.offsetWidth || 200;
    const h = el.offsetHeight || 120;
    let left = anchorRect.right + 8;
    if (left + w > window.innerWidth - 8) left = Math.max(8, anchorRect.left - w - 8);
    let top = anchorRect.top;
    if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - h - 8);
    el.style.left = left + 'px';
    el.style.top = top + 'px';
    // 交互：悬停项目 → 级联下一层；点击项目 → 按该细分支筛选题目
    el.querySelectorAll('.deep-item[data-deep-self]').forEach(item => {
        item.addEventListener('click', ev => { ev.stopPropagation(); selectDeepSelf(item.dataset.deepSelf); });
    });
    el.querySelectorAll('.deep-item[data-deep]').forEach(item => {
        item.addEventListener('mouseenter', () => {
            clearTimeout(_flyHideTimer);
            const cid = item.dataset.deep;
            const hasKids = (deepChildrenView[cid] || []).some(k => (_flySub[k] || 0) > 0);
            if (hasKids) showDeepBrowse(cid, level + 1, item.getBoundingClientRect());
            else { for (let i = level + 1; i < _flyLevels.length; i++) if (_flyLevels[i]) _flyLevels[i].hidden = true; }
        });
        item.addEventListener('click', ev => {
            ev.stopPropagation();
            selectDeepCat(item.dataset.deep);
        });
    });
}

/** 树节点悬停入口：仅对有细分类映射的知识点（L2）生效 */
function onCatNodeEnter(nodeEl, catId) {
    const root = deepRootOfCat(catId);
    if (!root) { scheduleHideDeepFly(60); return; }
    // 计数按「被悬停的这个知识点」统计，与点击后列表口径一致
    const { sub, direct } = deepCountsForCat(catId);
    if (!sub[root]) { scheduleHideDeepFly(60); return; }
    // 细分类根下没有任何有题的子分支 → 题目全挂在「本级」，弹出来只会得到
    // 「▸ 本级（未细分）+ 该分支下暂无细分类题目」，没有可浏览的下分支，干脆不弹
    const kids = (deepChildrenView[root] || []).filter(c => (sub[c] || 0) > 0);
    if (!kids.length) { scheduleHideDeepFly(60); return; }
    _flySub = sub;
    _flyDirect = direct;
    clearTimeout(_flyHideTimer);
    showDeepBrowse(root, 0, nodeEl.getBoundingClientRect());
}

/** 选中细分类分支：只显示该分支（含子树）的题 */
function selectDeepSelf(id) {
    deepEnsureOwner(id);     // 若属于另一个大分支 → 先把主区切过去（会清空 curDeepCat）
    curDeepCat = String(id);
    curDeepSelf = true;      // 只筛本级
    saveCatState();          // 刷新后保留（用户要求）
    hideDeepFlyNow();
    renderMain();
    renderNav();
}
function selectDeepCat(id) {
    deepEnsureOwner(id);     // 同上
    curDeepCat = String(id);
    curDeepSelf = false;
    saveCatState();
    hideDeepFlyNow();
    renderMain();
    renderNav();
}
function clearDeepCat() {
    curDeepCat = null;
    curDeepSelf = false;
    saveCatState();
    hideDeepFlyNow();
    renderMain();
    renderNav();
}
// 点击页面其它地方收起浮层
document.addEventListener('click', () => hideDeepFlyNow());
window.addEventListener('scroll', () => hideDeepFlyNow(), { passive: true });

// ============ 初始化 ============
async function init() {
    // ⚠️ 首屏要读 ~6MB 题库（exam 1.2 + core 1.8 + dgy 2.3 + bank 0.8）再渲染，
    //    此前主区一直空白，复测页（?review=1）尤其明显——左树被隐藏后整页全白，
    //    用户会误判成「页面坏了」。所以第一件事就是放占位提示。
    {
        const el0 = document.getElementById('catMain');
        if (el0) {
            el0.innerHTML = REVIEW_MODE
                ? '<div class="cat-empty">⏳ 正在汇总你的标记题…<br><span style="font-size:13px;opacity:.75">'
                + '首次打开需读取 ~6MB 题库，请稍候（之后有缓存会快很多）</span></div>'
                : '<div class="cat-empty">⏳ 正在加载题库…</div>';
        }
    }
    const [er, cr, br, corer, dgyr] = await Promise.all([
        fetch('data/exam.json'),
        fetch('data/exam_categories.json'),
        fetch('data/bank_questions.json').catch(() => null),
        fetch('data/core_bank.json').catch(() => null),
        fetch('data/dgy_items.json').catch(() => null),
    ]);
    if (!er.ok) throw new Error('加载真题失败: ' + er.status);
    if (!cr.ok) throw new Error('加载分类失败: ' + cr.status);
    // 数据到位 → 换文案。渲染数百张卡片（复测页可达 366 题）同样要时间，
    // 让占位文案跟着推进，用户才能区分「慢」和「卡死」。
    {
        const el0 = document.getElementById('catMain');
        if (el0 && el0.querySelector('.cat-empty')) {
            el0.innerHTML = '<div class="cat-empty">⏳ 正在渲染题目…</div>';
        }
    }
    examPapers = await er.json();
    // 真题题干归一化集合：必须在 concat 大观园习题卷**之前**构建（否则习题卷也会进集合，
    // 导致下面 bankItems 的精确去重把习题卷当真题、误伤大观园的题）
    examStemSet = new Set();
    for (const p of examPapers) {
        for (const s of (p.sections || [])) {
            for (const q of (s.questions || [])) {
                const ns = normStem(q.stem);
                if (ns.length >= 20) examStemSet.add(ns);
            }
        }
    }
    // 大观园 900题·880题·姜晓千（数二习题，非真题）：
    // 只在分类题库里与真题合并成一棵树，**不进 exam.html 的试卷列表**
    // （已从 exam.json 拆出到 dgy_items.json；qid 仍是 DG900JXB-<no>，收藏主键不变）
    if (dgyr && dgyr.ok) {
        try {
            const dgy = await dgyr.json();
            examPapers = examPapers.concat(dgy);
        } catch (e) { console.warn('大观园习题库解析失败', e); }
    }
    cats = await cr.json();
    // 核心题库（大观严选题 606 题，categoryIds 已映射到同一分类体系）
    if (corer && corer.ok) {
        try {
            corePapers = await corer.json();
            coreLink = {};
            for (const s of (corePapers[0] && corePapers[0].sections) || []) {
                for (const q of s.questions || []) {
                    // 带 paperId 前缀，避免与 xd 的同号题互相覆盖（曾导致 qidOf 取到别的题的 qid）
                    if (q.linkedQid) coreLink['core-' + q.no] = q.linkedQid;
                }
            }
            migrateCoreLegacyKeys();   // 旧 'core-N' 收藏/标记/笔记 → 真题 qid（一次性）
            migrateXdLegacyKeys();     // 线代重点题并入后 'xd-<原号>' → 'core-<新号>'（一次性）
            migrateLinkFixKeys();      // 错误 linkedQid 清除后，把冲突主键上的标记复制到真同题（一次性）
            migrateAliasKeys();        // 跨年同题：把 linkAlias 上另一年份的标记复制到主键（一次性）
            migrateOrphanNote();       // 孤儿笔记 examNote-undefined 接回 xd-169（core no=844）
            migrateDropDeadCopies();   // 清理「共享旧键」造成的历史误复制（笔记/收藏）
        } catch (e) { console.error('核心题库解析失败', e); }
    } else {
        console.warn('核心题库 core_bank.json 未加载，仅提供真题源');
    }
    // 大观园真题库（categoryIds 已映射到统一分类体系，与 exam.json 合并一棵树）
    if (br && br.ok) {
        const bq = await br.json();
        const examYears = new Set(examPapers.map(p => String(p.year)));
        bankItems = (bq.items || []).map((it, idx) => {
            const ym = /(\d{4})/.exec(it.source || '');   // 括号格式也能提取年份
            const q = Object.assign({}, it, {
                no: idx + 1,
                idea: it.explanation || '',   // 大观园解析 → 分类页「解析」按钮
            });
            return { paper: { id: 'bank', year: ym ? ym[1] : '', title: it.source || '大观园真题' }, q, catIds: it.categoryIds || [] };
        })
        // 同题去重（两条规则）：
        // ① source 为「(YY)YY 数二(真题)」且已有同年套卷 → 隐藏大观园版（math-note 版已在）；
        //    1987-1999 等老年份与合卷题保留。
        // ② 题干归一化后与真题完全相同 → 一律隐藏。仅靠 ① 会漏掉「无括号 / 合卷(数二三) /
        //    带顿号」等 19 种写法（实测漏网 19 道，同题在分类页显示两遍且 DOM id 重复）。
        //    用精确题干比对而非放宽 source 正则——放宽会误伤 563 道「改写版」真题（实测）。
        //    注意：真题题干集合要在 concat 大观园习题卷之前建，否则会把习题卷也算进去。
        .filter(e => {
            const m = /^\(?(19\d\d|20\d\d) 数二(真题)?\)?$/.exec(e.q.source || '');
            if (m && examYears.has(m[1])) return false;
            const ns = normStem(e.q.stem);
            return !(ns.length >= 20 && examStemSet.has(ns));
        });
    }
    // 线代重点题已物理并入 core_bank.json（2026-10-11），不再单独 fetch xd_bank.json。
    // 三类一次性主键迁移（migrateCoreLegacyKeys / migrateXdLegacyKeys / migrateLinkFixKeys）
    // 都在上方 corePapers 加载块内执行（依赖 coreLink 构建完成）。
    document.querySelectorAll('.cat-mark').forEach(b => b.classList.toggle('on', markSel[b.dataset.m]));
    syncUnmarkedFirstBtn();
    syncYearSortBtn();
    // 恢复的选中分类若已不在分类表里（数据变更），清掉防悬空
    if (curCat !== null && !cats[String(curCat)]) { curCat = null; saveCatState(); }
    // 支持 ?cid=<知识点id> 直达（来自「分析与建议」面板的「跳转刷题」）
    const _cid = new URLSearchParams(location.search).get('cid');
    if (_cid && cats[String(_cid)]) {
        curCat = Number(_cid);
        collapsedSubjects.clear();   // 跳转时全展开，保证该知识点在树中可见
        collapsedChapters.clear();
        saveCatState();
    }
    // 顶栏折叠状态恢复（与真题页共用 examTopCollapsed，保持跨页一致）
    restoreTopBar();
    syncTopH();
    // 左侧目录栏收起状态恢复（与 exam.html 同款交互）
    applySideState();
    // 恢复上次搜索词 + 滚动位置（记忆做题位置）
    try {
        const st = JSON.parse(localStorage.getItem(CAT_STATE_KEY) || '{}');
        if (st.search && !location.search) {   // 有 ?cid 跳转时优先跳转，不回填搜索
            catSearchKw = st.search;
            const inp = document.getElementById('catSearch');
            if (inp) { inp.value = st.search; const clr = document.getElementById('catSearchClear'); if (clr) clr.style.display = ''; }
        }
        const _roll = st.scrollY || 0;
        if (_roll && !location.search) requestAnimationFrame(() => window.scrollTo(0, _roll));
    } catch (e) { }
    applySrcMode(false);   // 先应用上次数据源（exam / core）→ 决定 papers，再建索引
    applyReviewMode();     // 复测模式（?review=1）：隐藏分类树、改标题
    ppApplyMode();         // 拼卷模式（?paper=1）：左栏换历史拼卷、改标题
    // 复测页 / 拼卷页都用不到「细分类树」数据（它只服务分类树的悬停浮层）→ 省一次往返。
    // 其余步骤（buildEntries / buildDeepIndex / renderTree / renderNav）保持不变 ——
    // activeEntries() 等依赖它们，跳过会引入不可预知的副作用。
    if (!REVIEW_MODE && !PAPER_MODE) await loadCatDeep();
    // 本地「收到核心题库」增补层：把用户手动收进来的题并进 corePapers（需 catDeep 解析章节）
    try {
        if (window.CoreExtra && corePapers && corePapers.length) {
            const n = CoreExtra.mergeInto(corePapers, catDeep);
            if (n) console.info('[核心增补] 并入', n, '题');
        }
    } catch (e) { console.warn('核心增补并入失败', e); }
    buildEntries();
    if (!PAPER_MODE) buildDeepIndex();   // 拼卷左栏是历史卷列表，不需要细分类索引
    if (!PAPER_MODE) renderTree();       // ⚠️ 必须跳过：否则分类树会覆盖左栏的卷列表
    renderMain();
    renderNav();
}

// 滚动/切题时记忆位置：节流保存（复用 saveCatState 的 search/scrollY 字段）
let _catPosTimer = null;
function saveCatPosLazy() {
    if (_catPosTimer) return;
    _catPosTimer = setTimeout(() => { _catPosTimer = null; saveCatState(); }, 600);
}
window.addEventListener('scroll', saveCatPosLazy, { passive: true });
window.addEventListener('beforeunload', saveCatState);
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') saveCatState(); });

// ============ 悬浮题号导航（与真题页同款；显示当前选中分类 / 搜索结果的题号） ============
let navCollapsed = false;   // 题号球收起态（默认展开，同真题页）
function toggleFloatQ() {
    navCollapsed = !navCollapsed;
    try { localStorage.setItem('examNavCollapsed', navCollapsed ? '1' : '0'); } catch (e) { }
    const fq = document.getElementById('floatQ');
    if (fq) fq.classList.toggle('collapsed', navCollapsed);
    if (fq) fq.classList.toggle('expanded', !navCollapsed);
}
// 当前列表的题号集合：搜索模式 = 搜索结果；分类模式 = 当前分类全部题
function catNavQNos() {
    const ents = catSearchKw ? activeEntries().filter(catSearchMatch) : (curCat != null ? activeEntries().filter(e => curCatSet().has(String(e.catId))) : []);
    return ents.map(e => e.q.no);
}
function renderNav() {
    const el = document.getElementById('floatQNo');
    if (!el) return;
    // 窄屏（手机）题号球已被 CSS 隐藏：跳过整棵构建，省掉上千个按钮的渲染
    if (window.innerWidth <= 900) {
        el.textContent = '—';
        const l0 = document.getElementById('floatQList');
        if (l0) l0.innerHTML = '';
        return;
    }
    const list = document.getElementById('floatQList');
    const ents = catSearchKw ? activeEntries().filter(catSearchMatch) : (curCat != null ? activeEntries().filter(e => curCatSet().has(String(e.catId))) : []);
    const nos = ents.map(e => e.q.no);
    const uniq = [...new Set(nos)].sort((a, b) => a - b);
    if (!uniq.length) { el.textContent = '—'; if (list) list.innerHTML = ''; return; }
    // 题号 → 掌握状态（不熟/不会），同一 no 多分类重复取任一 entry 状态即可（同题同状态）
    const stMap = {};
    for (const e of ents) {
        if (stMap[e.q.no]) continue;
        const st = statusOf(qidOf(e.paper.id, e.q.no));
        if (st) stMap[e.q.no] = st;
    }
    el.textContent = uniq.length + '题';
    list.innerHTML = uniq.map(no => {
        const st = stMap[no];
        const markCls = st ? (st === 'unknown' ? ' mark-unk' : st === 'mastered' ? ' mark-mst' : ' mark-unf') : '';
        const stTxt = st === 'unknown' ? '·🔴不会' : st === 'mastered' ? '·🟢掌握' : st === 'unfamiliar' ? '·🟡不熟' : '';
        return `<button class="nav-q${markCls}" data-navq="${no}" title="${no} 题${stTxt}" onclick="jumpToQ(${no})">${no}</button>`;
    }).join('');
    highlightNav();
}
function jumpToQ(no) {
    // 分类页：跳到首个 data-qno=no 的题卡（该题可能多分类重复，取当前列表内首个）
    // 分批渲染下目标可能还没生成 → 边加载边找
    const find = () => Array.from(document.querySelectorAll('.q-card[data-qno="' + no + '"]')).find(c => !c.closest('[hidden]'));
    let card = find(), guard = 0;
    while (!card && _catEntries.length > _catShown && guard++ < 80) { catAppendMore(); card = find(); }
    if (card) card.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function highlightNav() {
    // 先看题号球在不在（手机端已被隐藏）：不在就立刻返回，避免白遍历上千张卡片
    const btns = document.querySelectorAll('.nav-q');
    if (!btns.length) return;
    const cards = Array.from(document.querySelectorAll('.q-card'));
    if (!cards.length) return;
    const half = window.innerHeight * 0.45;
    let cur = null;
    for (const c of cards) {
        const r = c.getBoundingClientRect();
        if (r.top <= half) cur = c; else break;
    }
    const curNo = cur ? cur.getAttribute('data-qno') : null;
    btns.forEach(b => b.classList.toggle('on', b.getAttribute('data-navq') === curNo));
}
// 还原题号球收起态 + 每次重渲染后刷新题号
(function restoreNav() {
    try { if (localStorage.getItem('examNavCollapsed') === '1') { navCollapsed = true; } } catch (e) { }
    const fq = document.getElementById('floatQ');
    if (fq) { fq.classList.toggle('collapsed', navCollapsed); fq.classList.toggle('expanded', !navCollapsed); }
})();
// 滚动时高亮题号球：必须 rAF 节流——每次滚动都遍历全部卡片取
// getBoundingClientRect 会强制回流，题多时手机上直接卡成幻灯片
let _navRaf = 0;
function onScrollNav() {
    if (_navRaf) return;
    _navRaf = requestAnimationFrame(() => { _navRaf = 0; highlightNav(); });
}
window.addEventListener('scroll', onScrollNav, { passive: true });

init().catch(e => {
    const el = document.getElementById('catMain');
    if (el) el.innerHTML = '<div class="empty-tip">加载失败：' + esc(e.message) + '</div>';
    console.error(e);
});
